#!/usr/bin/env python3
"""Generate federated daily report with Commit-First and Diff-Fallback strategy."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass


TASKLINE_PATTERN = re.compile(
    r"^\s*(?:taskline_id|taskline|task_id|任务线)\s*[:：]\s*(.+?)\s*$", re.IGNORECASE
)
NEXT_PATTERN = re.compile(
    r"^\s*(?:next|todo|next_actions|明日任务|下一步)\s*[:：]\s*(.+?)\s*$",
    re.IGNORECASE,
)


@dataclass
class CmdResult:
    stdout: str
    stderr: str
    code: int


@dataclass
class CommitDigest:
    subject: str
    taskline_id: str | None
    next_items: list[str]
    hours: float | None


@dataclass
class ProjectSnapshot:
    project_id: str
    repo_root: pathlib.Path
    ok: bool
    changed_files: int
    modified: int
    added: int
    deleted: int
    renamed: int
    conflicted: int
    sample_files: list[str]
    commit_count: int
    commit_samples: list[str]
    commit_tasklines: list[str]
    commit_hours: float | None
    next_items: list[str]
    error: str | None = None


def run_cmd(cwd: pathlib.Path, *args: str, allow_fail: bool = False) -> CmdResult:
    proc = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0 and not allow_fail:
        cmd = " ".join(args)
        err = (proc.stderr or proc.stdout).strip()
        raise RuntimeError(f"Command failed ({proc.returncode}): {cmd}\n{err}")
    return CmdResult(stdout=proc.stdout, stderr=proc.stderr, code=proc.returncode)


def parse_date(raw: str | None) -> dt.date:
    if not raw:
        return dt.date.today()
    return dt.datetime.strptime(raw, "%Y-%m-%d").date()


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).strip(" -:：")


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


def trim_text(text: str, limit: int = 80) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def format_hours(value: float) -> str:
    text = f"{value:.1f}".rstrip("0").rstrip(".")
    return f"{text}h"


def parse_hours_from_text(text: str) -> float | None:
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        low = line.lower()
        if not any(key in low for key in ("hours", "工时", "耗时", "duration")):
            continue

        m_h = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*h\b", line, re.IGNORECASE)
        if m_h:
            return float(m_h.group(1))

        m_cn = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*小时", line)
        if m_cn:
            return float(m_cn.group(1))
    return None


def load_registry(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_projects(registry: dict) -> list[tuple[str, pathlib.Path]]:
    seen: set[str] = set()
    projects: list[tuple[str, pathlib.Path]] = []
    for item in registry.get("projects", []):
        if not bool(item.get("enabled", True)):
            continue

        nodes = item.get("ccos_nodes", [])
        has_enabled_node = any(bool(node.get("enabled", True)) for node in nodes) if nodes else True
        if not has_enabled_node:
            continue

        project_id = str(item.get("project_id", "")).strip()
        repo_root_raw = str(item.get("repo_root", "")).strip()
        if not project_id or not repo_root_raw:
            continue

        key = f"{project_id}::{repo_root_raw}"
        if key in seen:
            continue
        seen.add(key)
        projects.append((project_id, pathlib.Path(repo_root_raw).expanduser()))
    return projects


def parse_git_status_lines(status_text: str) -> tuple[int, int, int, int, int, list[str]]:
    modified = 0
    added = 0
    deleted = 0
    renamed = 0
    conflicted = 0
    sample_files: list[str] = []

    for raw in status_text.splitlines():
        if not raw.strip():
            continue
        code = raw[:2]
        body = raw[3:] if len(raw) > 3 else ""
        path = body.split(" -> ")[-1].strip()
        if path and len(sample_files) < 3:
            sample_files.append(path)

        if code == "??":
            added += 1
            continue
        if "U" in code:
            conflicted += 1
        if "R" in code:
            renamed += 1
        if "D" in code:
            deleted += 1
        if "M" in code:
            modified += 1

    changed_files = modified + added + deleted + renamed + conflicted
    return changed_files, modified, added, deleted, renamed, conflicted, sample_files


def collect_commit_digests(repo_root: pathlib.Path, report_date: dt.date) -> tuple[list[CommitDigest], str | None]:
    start = dt.datetime.combine(report_date, dt.time.min)
    end = start + dt.timedelta(days=1)

    result = run_cmd(
        repo_root,
        "git",
        "-c",
        "core.quotepath=false",
        "log",
        "--no-merges",
        f"--since={start:%Y-%m-%d %H:%M:%S}",
        f"--until={end:%Y-%m-%d %H:%M:%S}",
        "--pretty=format:%H%x1f%s%x1f%b%x1e",
        "--",
        allow_fail=True,
    )
    if result.code != 0:
        merged = (result.stderr or result.stdout).strip()
        return [], merged or "git log 执行失败"

    digests: list[CommitDigest] = []
    for chunk in result.stdout.split("\x1e"):
        item = chunk.strip()
        if not item:
            continue
        parts = item.split("\x1f")
        subject = normalize_text(parts[1]) if len(parts) > 1 else ""
        body = parts[2].strip() if len(parts) > 2 else ""

        taskline = None
        for raw in body.splitlines():
            match = TASKLINE_PATTERN.match(raw)
            if match:
                taskline = normalize_text(match.group(1))
                break

        next_items: list[str] = []
        for raw in body.splitlines():
            match = NEXT_PATTERN.match(raw)
            if not match:
                continue
            next_text = normalize_text(match.group(1))
            if next_text:
                next_items.append(next_text)

        digests.append(
            CommitDigest(
                subject=subject,
                taskline_id=taskline,
                next_items=unique_keep_order(next_items),
                hours=parse_hours_from_text(body),
            )
        )

    return digests, None


def collect_snapshot(project_id: str, repo_root: pathlib.Path, report_date: dt.date) -> ProjectSnapshot:
    if not repo_root.exists():
        return ProjectSnapshot(
            project_id=project_id,
            repo_root=repo_root,
            ok=False,
            changed_files=0,
            modified=0,
            added=0,
            deleted=0,
            renamed=0,
            conflicted=0,
            sample_files=[],
            commit_count=0,
            commit_samples=[],
            commit_tasklines=[],
            commit_hours=None,
            next_items=[],
            error="仓库目录不存在",
        )
    if not (repo_root / ".git").exists():
        return ProjectSnapshot(
            project_id=project_id,
            repo_root=repo_root,
            ok=False,
            changed_files=0,
            modified=0,
            added=0,
            deleted=0,
            renamed=0,
            conflicted=0,
            sample_files=[],
            commit_count=0,
            commit_samples=[],
            commit_tasklines=[],
            commit_hours=None,
            next_items=[],
            error="不是 git 仓库（缺少 .git）",
        )

    status = run_cmd(
        repo_root,
        "git",
        "-c",
        "core.quotepath=false",
        "status",
        "--short",
        allow_fail=True,
    )
    if status.code != 0:
        merged = (status.stderr or status.stdout).strip()
        return ProjectSnapshot(
            project_id=project_id,
            repo_root=repo_root,
            ok=False,
            changed_files=0,
            modified=0,
            added=0,
            deleted=0,
            renamed=0,
            conflicted=0,
            sample_files=[],
            commit_count=0,
            commit_samples=[],
            commit_tasklines=[],
            commit_hours=None,
            next_items=[],
            error=merged or "git status 执行失败",
        )

    changed_files, modified, added, deleted, renamed, conflicted, sample_files = parse_git_status_lines(
        status.stdout
    )

    commits, log_error = collect_commit_digests(repo_root, report_date)
    commit_samples = [trim_text(item.subject, 72) for item in commits[:2] if item.subject]
    commit_tasklines = unique_keep_order(
        [item.taskline_id for item in commits if item.taskline_id]
    )[:3]
    next_items = unique_keep_order(
        [todo for item in commits for todo in item.next_items]
    )[:6]

    hours_values = [item.hours for item in commits if item.hours is not None]
    hours_total = sum(hours_values) if hours_values else None

    return ProjectSnapshot(
        project_id=project_id,
        repo_root=repo_root,
        ok=True,
        changed_files=changed_files,
        modified=modified,
        added=added,
        deleted=deleted,
        renamed=renamed,
        conflicted=conflicted,
        sample_files=sample_files,
        commit_count=len(commits),
        commit_samples=commit_samples,
        commit_tasklines=commit_tasklines,
        commit_hours=hours_total,
        next_items=next_items,
        error=log_error,
    )


def build_done_items(snapshots: list[ProjectSnapshot], index_aggregated: bool) -> list[str]:
    total = len(snapshots)
    healthy = sum(1 for item in snapshots if item.ok)
    committed = [item for item in snapshots if item.ok and item.commit_count > 0]
    diff_fallback = [item for item in snapshots if item.ok and item.commit_count == 0 and item.changed_files > 0]
    blocked = [item for item in snapshots if not item.ok]

    done = [
        f"联邦扫描 {total} 个项目（可访问 {healthy} 个），其中 {len(committed)} 个项目今日有提交。"
    ]
    if index_aggregated:
        done.append("已刷新联邦 CCOS 索引（ccos-index-federated.json）。")

    for item in sorted(committed, key=lambda x: x.commit_count, reverse=True)[:5]:
        summary = "；".join(item.commit_samples) if item.commit_samples else "无提交摘要"
        tail = f"，任务线: {','.join(item.commit_tasklines)}" if item.commit_tasklines else ""
        done.append(f"{item.project_id}：{item.commit_count} 条提交，摘要：{summary}{tail}。")

    for item in sorted(diff_fallback, key=lambda x: x.changed_files, reverse=True)[:3]:
        samples = "、".join(item.sample_files) if item.sample_files else "无示例文件"
        done.append(
            f"{item.project_id}：无今日提交，回退到 git diff 检测 {item.changed_files} 项改动（示例：{samples}）。"
        )

    for item in blocked[:3]:
        done.append(f"{item.project_id}：扫描失败（{item.error}）。")

    return done[:9]


def build_todo_items(snapshots: list[ProjectSnapshot]) -> list[str]:
    todos = unique_keep_order([todo for item in snapshots for todo in item.next_items])
    if todos:
        return todos[:6]

    changed = [item for item in snapshots if item.ok and item.changed_files > 0]
    if not changed:
        return ["各项目工作区已清洁，继续推进下一个里程碑任务。"]

    result: list[str] = []
    for item in sorted(changed, key=lambda x: x.changed_files, reverse=True)[:6]:
        result.append(f"继续收敛 {item.project_id} 的未提交改动，并完成验证后提交。")
    return result


def build_hours_text(snapshots: list[ProjectSnapshot]) -> str:
    values = [item.commit_hours for item in snapshots if item.commit_hours is not None]
    if not values:
        return "待补充（各项目 commit 未提供工时字段）"
    return f"{format_hours(sum(values))}（由各项目 commit 元数据累计）"


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
    lines = ["- 联邦日报", "\t- 今日完成"]
    for item in done:
        lines.append(f"\t\t- {item}")
    lines.append("\t- 明日任务")
    for item in todo:
        lines.append(f"\t\t- {item}")
    lines.append("\t- 工时")
    lines.append(f"\t\t- {hours}")
    return "\n".join(lines) + "\n"


def upsert_block(path: pathlib.Path, block_head: str, block_text: str) -> None:
    block_lines = block_text.rstrip("\n").splitlines()
    if path.exists():
        lines = path.read_text(encoding="utf-8").splitlines()
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = []

    start = None
    for i, line in enumerate(lines):
        if line.strip() == block_head:
            start = i
            break

    if start is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend(block_lines)
    else:
        end = len(lines)
        for i in range(start + 1, len(lines)):
            if lines[i].startswith("- "):
                end = i
                break
        lines = lines[:start] + block_lines + lines[end:]

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


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

    message = commit_message or f"docs: {report_date:%Y-%m-%d} 联邦日报与索引同步"
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


def aggregate_index_if_needed(ccos_root: pathlib.Path, skip: bool) -> bool:
    if skip:
        return False
    script = ccos_root / "machine" / "federation" / "scripts" / "aggregate_ccos_index.py"
    if not script.exists():
        return False
    result = run_cmd(
        ccos_root,
        "python3",
        str(script),
        "--ccos-root",
        str(ccos_root),
        allow_fail=True,
    )
    return result.code == 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate federated daily report with Commit-First and Diff-Fallback strategy."
    )
    parser.add_argument("--ccos-root", default=".", help="CCOS repository root path.")
    parser.add_argument(
        "--registry",
        default="machine/federation/project-registry.json",
        help="Registry file path relative to CCOS root.",
    )
    parser.add_argument("--date", help="Date in YYYY-MM-DD. Default today.")
    parser.add_argument(
        "--journal-root",
        default="capture/journals",
        help="Journal directory relative to CCOS root.",
    )
    parser.add_argument("--print-only", action="store_true", help="Only print report.")
    parser.add_argument("--sync", action="store_true", help="Commit and push after write.")
    parser.add_argument("--remote", default="origin", help="Git remote for --sync.")
    parser.add_argument("--branch", help="Git branch for --sync.")
    parser.add_argument("--commit-message", help="Commit message override for --sync.")
    parser.add_argument(
        "--skip-index-aggregation",
        action="store_true",
        help="Skip running federation index aggregation.",
    )
    args = parser.parse_args()

    if args.print_only and args.sync:
        print("--print-only and --sync cannot be used together.", file=sys.stderr)
        return 2

    ccos_root = pathlib.Path(args.ccos_root).expanduser().resolve()
    if not (ccos_root / ".git").exists():
        print(f"Not a git repository: {ccos_root}", file=sys.stderr)
        return 2

    registry_path = ccos_root / args.registry
    if not registry_path.exists():
        print(f"Registry file not found: {registry_path}", file=sys.stderr)
        return 2

    report_date = parse_date(args.date)
    registry = load_registry(registry_path)
    projects = collect_projects(registry)
    snapshots = [collect_snapshot(project_id, repo_root, report_date) for project_id, repo_root in projects]
    index_aggregated = aggregate_index_if_needed(ccos_root, args.skip_index_aggregation)

    done = build_done_items(snapshots, index_aggregated=index_aggregated)
    todo = build_todo_items(snapshots)
    hours = build_hours_text(snapshots)
    report_text = build_markdown(done, todo, hours)
    print(report_text)

    if args.print_only:
        return 0

    journal_rel = pathlib.Path(args.journal_root) / report_date.strftime("%Y_%m_%d.md")
    journal_path = ccos_root / journal_rel
    block_text = build_logseq_block(done, todo, hours)
    upsert_block(journal_path, "- 联邦日报", block_text)
    print(f"\n[OK] 已回写联邦日报: {journal_rel}")

    if args.sync:
        print(
            sync_repo(
                repo=ccos_root,
                report_date=report_date,
                remote=args.remote,
                branch=args.branch,
                commit_message=args.commit_message,
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
