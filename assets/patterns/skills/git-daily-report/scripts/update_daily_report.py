#!/usr/bin/env python3
"""Generate a daily report strictly from git diff and optionally sync to remote."""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass


TAG_PATTERN = re.compile(
    r"^\s*(?:[-*+]\s*)?(DONE|TODO|NOW|WAITING)\b[:：-]?\s*(.*)$", re.IGNORECASE
)
CLOCK_PATTERN = re.compile(r"=>\s*([0-9]{2}):([0-9]{2}):([0-9]{2})")


@dataclass
class CmdResult:
    stdout: str
    stderr: str
    code: int


def run_cmd(repo: pathlib.Path, *args: str, allow_fail: bool = False) -> CmdResult:
    proc = subprocess.run(
        args,
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0 and not allow_fail:
        cmd = " ".join(args)
        err = (proc.stderr or proc.stdout).strip()
        raise RuntimeError(f"Command failed ({proc.returncode}): {cmd}\n{err}")
    return CmdResult(stdout=proc.stdout, stderr=proc.stderr, code=proc.returncode)


def parse_date(date_text: str | None) -> dt.date:
    if not date_text:
        return dt.date.today()
    return dt.datetime.strptime(date_text, "%Y-%m-%d").date()


def parse_status_entries(status_text: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for raw in status_text.splitlines():
        if not raw.strip():
            continue
        code = raw[:2]
        body = raw[3:] if len(raw) > 3 else ""
        path = body.split(" -> ")[-1].strip()
        if not path:
            continue
        entries.append((code, path))
    return entries


def parse_name_status(name_status_text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in name_status_text.splitlines():
        if not raw.strip():
            continue
        parts = raw.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0].strip()
        path = parts[-1].strip()
        if path:
            result[path] = status
    return result


def parse_numstat(numstat_text: str) -> dict[str, tuple[int | None, int | None]]:
    result: dict[str, tuple[int | None, int | None]] = {}
    for raw in numstat_text.splitlines():
        if not raw.strip():
            continue
        parts = raw.split("\t")
        if len(parts) < 3:
            continue
        add_text, del_text, path = parts[0], parts[1], parts[2]
        added = int(add_text) if add_text.isdigit() else None
        deleted = int(del_text) if del_text.isdigit() else None
        result[path] = (added, deleted)
    return result


def parse_diff_by_file(diff_text: str) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    added: dict[str, list[str]] = defaultdict(list)
    removed: dict[str, list[str]] = defaultdict(list)
    current_path: str | None = None

    for raw in diff_text.splitlines():
        if raw.startswith("diff --git a/"):
            marker = " b/"
            idx = raw.rfind(marker)
            if idx > 0:
                current_path = raw[idx + len(marker) :].strip()
            else:
                current_path = None
            continue
        if current_path is None:
            continue
        if raw.startswith("+++ ") or raw.startswith("--- "):
            continue
        if raw.startswith("+"):
            added[current_path].append(raw[1:])
        elif raw.startswith("-"):
            removed[current_path].append(raw[1:])

    return added, removed


def normalize_text(line: str) -> str:
    text = line.strip()
    text = re.sub(r"^[-*+]\s*", "", text)
    text = text.replace("[[", "").replace("]]", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -:：")


def is_metadata_line(line: str) -> bool:
    text = line.strip()
    if not text or text in {"-", "--", "---"}:
        return True
    if text.startswith((":LOGBOOK:", ":END:", "CLOCK:", "collapsed::", "id::")):
        return True
    if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*::", text):
        return True
    if text.startswith("```"):
        return True
    return False


def trim_text(text: str, limit: int = 80) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def build_net_added_by_file(
    added_by_file: dict[str, list[str]], removed_by_file: dict[str, list[str]]
) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for path, added_lines in added_by_file.items():
        removed_counter = Counter()
        for line in removed_by_file.get(path, []):
            normalized = normalize_text(line)
            if normalized:
                removed_counter[normalized.lower()] += 1

        net_lines: list[str] = []
        for line in added_lines:
            normalized = normalize_text(line)
            if not normalized:
                continue
            key = normalized.lower()
            if removed_counter[key] > 0:
                removed_counter[key] -= 1
                continue
            net_lines.append(line)
        result[path] = net_lines
    return result


def collect_untracked_lines(repo: pathlib.Path, untracked_paths: list[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for path in untracked_paths:
        file_path = repo / path
        if not file_path.exists() or not file_path.is_file():
            continue
        if file_path.suffix.lower() not in {".md", ".txt"}:
            continue
        try:
            result[path] = file_path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
    return result


def unique_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def extract_tagged_items(lines: list[str]) -> tuple[list[str], list[str]]:
    done: list[str] = []
    todo: list[str] = []
    for raw in lines:
        if is_metadata_line(raw):
            continue
        match = TAG_PATTERN.search(raw)
        if not match:
            continue
        tag = match.group(1).upper()
        body = normalize_text(match.group(2))
        body = trim_text(body, 90)
        if not body:
            continue
        if tag == "DONE":
            done.append(body)
        else:
            todo.append(body)
    return unique_keep_order(done), unique_keep_order(todo)


def extract_hours(lines: list[str]) -> str:
    for raw in lines:
        if "工时" not in raw:
            continue
        m_h = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*h", raw, re.IGNORECASE)
        if m_h:
            return f"{m_h.group(1)}h"
        m_cn = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*小时", raw)
        if m_cn:
            return f"{m_cn.group(1)}h"

    total_seconds = 0
    for raw in lines:
        m = CLOCK_PATTERN.search(raw)
        if not m:
            continue
        hh, mm, ss = int(m.group(1)), int(m.group(2)), int(m.group(3))
        total_seconds += hh * 3600 + mm * 60 + ss
    if total_seconds > 0:
        hours = total_seconds / 3600
        text = f"{hours:.1f}".rstrip("0").rstrip(".")
        return f"{text}h（由git diff中的CLOCK累计）"
    return "待补充（git diff 未发现工时字段）"


def pick_file_highlights(net_added_by_file: dict[str, list[str]]) -> dict[str, str]:
    highlights: dict[str, str] = {}
    for path, lines in net_added_by_file.items():
        for raw in lines:
            if is_metadata_line(raw):
                continue
            if TAG_PATTERN.search(raw):
                continue
            text = normalize_text(raw)
            if not text:
                continue
            highlights[path] = trim_text(text, 60)
            break
    return highlights


def build_done_from_diff(
    status_entries: list[tuple[str, str]],
    numstat: dict[str, tuple[int | None, int | None]],
    net_added_by_file: dict[str, list[str]],
    done_tagged: list[str],
) -> list[str]:
    modified = sum(1 for code, _ in status_entries if code != "??")
    created = sum(1 for code, _ in status_entries if code == "??")
    total = len(status_entries)
    done: list[str] = [
        f"基于 git diff 完成 {total} 个文档变更同步（修改 {modified}，新增 {created}）。"
    ]

    if done_tagged:
        done.extend(done_tagged[:5])
        return unique_keep_order(done)[:6]

    highlights = pick_file_highlights(net_added_by_file)
    ranked_paths = sorted(
        net_added_by_file.keys(),
        key=lambda p: (
            (numstat.get(p, (0, 0))[0] or 0) + (numstat.get(p, (0, 0))[1] or 0),
            len(net_added_by_file.get(p, [])),
        ),
        reverse=True,
    )
    for path in ranked_paths[:5]:
        added, deleted = numstat.get(path, (None, None))
        stat_text = ""
        if added is not None and deleted is not None:
            stat_text = f"（+{added}/-{deleted}）"
        prefix = f"更新 {path}{stat_text}"
        highlight = highlights.get(path)
        if highlight:
            done.append(f"{prefix}：{highlight}")
        else:
            done.append(prefix)

    return unique_keep_order(done)[:6]


def build_todo_from_diff(
    todo_tagged: list[str],
    status_entries: list[tuple[str, str]],
) -> list[str]:
    if todo_tagged:
        return todo_tagged[:6]

    tasks: list[str] = []
    for _, path in status_entries[:6]:
        stem = pathlib.Path(path).stem
        tasks.append(f"继续收敛 {stem} 的新增改动并完成验证。")
    if not tasks:
        tasks.append("保持工作区清洁并开始下一阶段任务。")
    return unique_keep_order(tasks)[:6]


def build_markdown(done: list[str], todo: list[str], hours: str) -> str:
    lines = ["今日完成"]
    for idx, item in enumerate(done, 1):
        lines.append(f"{idx}. {item}")
    lines.append("")
    lines.append("明日任务")
    for idx, item in enumerate(todo, 1):
        lines.append(f"{idx}. {item}")
    lines.append("")
    lines.append("工时")
    lines.append(f"1. {hours}")
    return "\n".join(lines)


def build_logseq_block(done: list[str], todo: list[str], hours: str) -> str:
    lines = ["- 日报", "\t- 今日完成"]
    for item in done:
        lines.append(f"\t\t- {item}")
    lines.append("\t- 明日任务")
    for item in todo:
        lines.append(f"\t\t- {item}")
    lines.append("\t- 工时")
    lines.append(f"\t\t- {hours}")
    return "\n".join(lines) + "\n"


def upsert_report_block(journal: pathlib.Path, block: str) -> None:
    block_lines = block.rstrip("\n").splitlines()
    if journal.exists():
        lines = journal.read_text(encoding="utf-8").splitlines()
    else:
        journal.parent.mkdir(parents=True, exist_ok=True)
        lines = []

    start = None
    for idx, line in enumerate(lines):
        if line.strip() == "- 日报":
            start = idx
            break

    if start is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend(block_lines)
    else:
        end = len(lines)
        for idx in range(start + 1, len(lines)):
            if lines[idx].startswith("- "):
                end = idx
                break
        lines = lines[:start] + block_lines + lines[end:]

    journal.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def sync_repo(
    repo: pathlib.Path,
    report_date: dt.date,
    remote: str,
    branch: str | None,
    commit_message: str | None,
) -> str:
    run_cmd(repo, "git", "add", "-A")
    staged = run_cmd(repo, "git", "diff", "--cached", "--name-only").stdout.strip()
    if not staged:
        return "[SYNC] 无可提交改动。"

    message = commit_message or f"docs: {report_date:%Y-%m-%d} 日报回写与文档同步"
    commit = run_cmd(repo, "git", "commit", "-m", message, allow_fail=True)
    if commit.code != 0:
        merged = f"{commit.stdout}\n{commit.stderr}".strip()
        if "nothing to commit" in merged:
            return "[SYNC] 无可提交改动。"
        raise RuntimeError(f"Commit failed:\n{merged}")

    target_branch = branch or run_cmd(repo, "git", "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    push = run_cmd(repo, "git", "push", remote, target_branch, allow_fail=True)
    if push.code != 0:
        merged = f"{push.stdout}\n{push.stderr}".strip()
        raise RuntimeError(f"Push failed:\n{merged}")

    commit_id = run_cmd(repo, "git", "rev-parse", "--short", "HEAD").stdout.strip()
    return f"[SYNC] 已提交并推送：{commit_id} -> {remote}/{target_branch}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a daily report strictly from uncommitted git diff."
    )
    parser.add_argument("--repo", default=".", help="Repository root path.")
    parser.add_argument("--date", help="Date in YYYY-MM-DD, default today.")
    parser.add_argument(
        "--journal-root",
        default="capture/journals",
        help="Journal directory relative to repo.",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Print report only; do not write journal or sync.",
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="After write-back, run git add -A, commit, and push.",
    )
    parser.add_argument("--remote", default="origin", help="Git remote name for --sync.")
    parser.add_argument("--branch", help="Git branch for --sync; default current branch.")
    parser.add_argument("--commit-message", help="Commit message override for --sync.")
    args = parser.parse_args()

    if args.print_only and args.sync:
        print("--print-only and --sync cannot be used together.", file=sys.stderr)
        return 2

    repo = pathlib.Path(args.repo).resolve()
    if not (repo / ".git").exists():
        print(f"Not a git repository: {repo}", file=sys.stderr)
        return 2

    report_date = parse_date(args.date)
    journal_rel = pathlib.Path(args.journal_root) / report_date.strftime("%Y_%m_%d.md")
    journal_path = repo / journal_rel

    status_short = run_cmd(repo, "git", "-c", "core.quotepath=false", "status", "--short").stdout
    name_status_text = run_cmd(
        repo, "git", "-c", "core.quotepath=false", "diff", "--name-status", "HEAD", "--"
    ).stdout
    numstat_text = run_cmd(
        repo, "git", "-c", "core.quotepath=false", "diff", "--numstat", "HEAD", "--"
    ).stdout
    diff_text = run_cmd(
        repo, "git", "-c", "core.quotepath=false", "diff", "--unified=0", "--no-color", "HEAD", "--"
    ).stdout

    status_entries = parse_status_entries(status_short)
    name_status = parse_name_status(name_status_text)
    numstat = parse_numstat(numstat_text)
    added_by_file, removed_by_file = parse_diff_by_file(diff_text)
    net_added_by_file = build_net_added_by_file(added_by_file, removed_by_file)

    untracked_paths = [path for code, path in status_entries if code == "??"]
    untracked_lines = collect_untracked_lines(repo, untracked_paths)
    for path, lines in untracked_lines.items():
        net_added_by_file[path] = lines
        if path not in name_status:
            name_status[path] = "A"

    for _, path in status_entries:
        net_added_by_file.setdefault(path, [])

    flattened_net_lines: list[str] = []
    for path in net_added_by_file:
        flattened_net_lines.extend(net_added_by_file[path])

    done_tagged, todo_tagged = extract_tagged_items(flattened_net_lines)
    hours_text = extract_hours(flattened_net_lines)
    done_items = build_done_from_diff(status_entries, numstat, net_added_by_file, done_tagged)
    todo_items = build_todo_from_diff(todo_tagged, status_entries)

    report = build_markdown(done_items, todo_items, hours_text)
    print(report)

    if args.print_only:
        return 0

    block = build_logseq_block(done_items, todo_items, hours_text)
    upsert_report_block(journal_path, block)
    print(f"\n[OK] 已回写日报: {journal_rel}")

    if args.sync:
        sync_result = sync_repo(
            repo=repo,
            report_date=report_date,
            remote=args.remote,
            branch=args.branch,
            commit_message=args.commit_message,
        )
        print(sync_result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
