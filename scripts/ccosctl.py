#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXIT_OK = 0
EXIT_ARG = 2
EXIT_RULE = 3
EXIT_STATE = 4
EXIT_IO = 5

REGISTRY_DEFAULT = "machine/federation/project-registry.json"
FED_INDEX_DEFAULT = "machine/federation/ccos-index-federated.json"
ANCHOR_DOC_NAME = "ccos-unified-protocol.md"
TASK_INDEX_REL = "capture/tasklines/task-index.md"
TASKLINES_REL = "capture/tasklines"
TASK_REQUIRED_FIELDS = ("project_id", "repo_root", "ccos_node")


@dataclass
class LintIssue:
    level: str
    code: str
    message: str


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_local() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def timestamp_local() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def json_load(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def json_dump(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2))


def parse_bool(value: str) -> bool:
    low = value.strip().lower()
    if low in {"1", "true", "yes", "y", "on"}:
        return True
    if low in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"invalid bool value: {value}")


def is_hub_root(path: Path) -> bool:
    return (path / "meta" / ANCHOR_DOC_NAME).is_file() and (
        path / "machine" / "federation" / "project-registry.json"
    ).is_file()


def find_hub_root_from(start: Path) -> Path | None:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if is_hub_root(candidate):
            return candidate
    return None


def resolve_hub_root(raw: str | None) -> Path:
    candidates: list[Path] = []
    if raw:
        candidates.append(Path(raw).expanduser())

    env_root = os.environ.get("CCOS_HUB_ROOT")
    if env_root:
        candidates.append(Path(env_root).expanduser())

    inferred = find_hub_root_from(Path.cwd())
    if inferred:
        candidates.append(inferred)

    candidates.append(Path.home() / "ccos")

    seen: set[Path] = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except FileNotFoundError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if is_hub_root(resolved):
            return resolved

    raise RuntimeError(
        "Cannot locate CCOS hub root. Set --hub-root or CCOS_HUB_ROOT to a valid hub path."
    )


def resolve_path(base: Path, raw: str) -> Path:
    path = Path(raw).expanduser()
    if path.is_absolute():
        return path
    return (base / path).resolve()


def run_subprocess(cmd: list[str], cwd: Path | None = None) -> int:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout.rstrip())
    if proc.stderr:
        print(proc.stderr.rstrip(), file=sys.stderr)
    return proc.returncode


def command_to_text(cmd: list[str]) -> str:
    return " ".join(cmd)


def strip_ticks(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        return value[1:-1]
    return value


def safe_task_filename(task_id: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", task_id.strip().lower()).strip("-")
    if not safe:
        safe = "unnamed-task"
    return f"task-{safe}.md"


def source_ccos_path(repo_root: Path) -> str:
    repo = repo_root.resolve()
    try:
        rel = repo.relative_to(Path.home().resolve()).as_posix()
        return f"{rel}/CCOS"
    except ValueError:
        return f"{repo.as_posix()}/CCOS"


def metadata_line(field: str, value: str) -> str:
    return f"- {field}: `{value}`"


def set_metadata_field(text: str, field: str, value: str) -> str:
    lines = text.splitlines()
    target = f"- {field}:"
    replacement = metadata_line(field, value)

    for idx, line in enumerate(lines):
        if line.startswith(target):
            lines[idx] = replacement
            return "\n".join(lines) + "\n"

    # Insert after existing metadata block if possible.
    insert_idx = 1 if lines else 0
    while insert_idx < len(lines) and not lines[insert_idx].startswith("- "):
        insert_idx += 1
    while insert_idx < len(lines) and lines[insert_idx].startswith("- "):
        insert_idx += 1
    lines.insert(insert_idx, replacement)
    return "\n".join(lines) + "\n"


def ensure_progress_log(text: str) -> str:
    if "## Progress Log" in text:
        return text
    suffix = "\n## Progress Log\n"
    if text.endswith("\n"):
        return text + suffix
    return text + "\n" + suffix


def append_progress_log(text: str, message: str) -> str:
    text = ensure_progress_log(text)
    lines = text.splitlines()
    heading_idx = -1
    for idx, line in enumerate(lines):
        if line.strip() == "## Progress Log":
            heading_idx = idx
            break
    if heading_idx < 0:
        lines.extend(["", "## Progress Log"])
        heading_idx = len(lines) - 1

    insert_idx = heading_idx + 1
    while insert_idx < len(lines) and not lines[insert_idx].startswith("## "):
        insert_idx += 1
    lines.insert(insert_idx, f"- {timestamp_local()} {message}")
    return "\n".join(lines) + "\n"


def upsert_section(text: str, heading: str, body: list[str]) -> str:
    lines = text.splitlines()
    start = -1
    for idx, line in enumerate(lines):
        if line.strip() == heading:
            start = idx
            break

    section_lines = [heading, *body]
    if start < 0:
        if lines and lines[-1] != "":
            lines.append("")
        lines.extend(section_lines)
        return "\n".join(lines) + "\n"

    end = start + 1
    while end < len(lines) and not lines[end].startswith("## "):
        end += 1
    lines = lines[:start] + section_lines + lines[end:]
    return "\n".join(lines) + "\n"


def find_task_file_by_id(task_dir: Path, task_id: str) -> Path | None:
    task_id = task_id.strip()
    pattern = re.compile(r"^- taskline_id:\s*`?([^`\n]+)`?\s*$", re.M)

    for path in sorted(task_dir.glob("task-*.md")):
        if path.name == "task-index.md":
            continue
        text = read_text(path)
        match = pattern.search(text)
        if match and match.group(1).strip() == task_id:
            return path

    guessed = task_dir / safe_task_filename(task_id)
    if guessed.exists():
        return guessed
    return None


def ensure_task_index(index_path: Path) -> None:
    if index_path.is_file():
        return
    content = "\n".join(
        [
            "# Taskline Index",
            "",
            "| taskline_id | 标题 | 状态 | 优先级 | 关联项目 | 任务文档 | 来源 CCOS |",
            "|---|---|---|---|---|---|---|",
            "",
        ]
    )
    write_text(index_path, content)


def build_task_index_row(
    task_id: str,
    title: str,
    status: str,
    priority: str,
    project_id: str,
    task_doc: str,
    source_ccos: str,
) -> str:
    cells = [
        f"`{task_id}`",
        title,
        f"`{status}`",
        f"`{priority}`",
        f"`{project_id}`",
        task_doc,
        source_ccos,
    ]
    return "| " + " | ".join(cells) + " |"


def upsert_task_index_row(
    index_path: Path,
    task_id: str,
    title: str,
    status: str,
    priority: str,
    project_id: str,
    task_doc: str,
    source_ccos: str,
) -> None:
    ensure_task_index(index_path)
    lines = read_text(index_path).splitlines()
    row = build_task_index_row(
        task_id=task_id,
        title=title,
        status=status,
        priority=priority,
        project_id=project_id,
        task_doc=task_doc,
        source_ccos=source_ccos,
    )
    marker = f"`{task_id}`"

    for idx, line in enumerate(lines):
        if line.strip().startswith("|") and marker in line:
            lines[idx] = row
            write_text(index_path, "\n".join(lines))
            return

    if lines and lines[-1] != "":
        lines.append("")
    lines.append(row)
    write_text(index_path, "\n".join(lines))


def update_task_index_status(index_path: Path, task_id: str, status: str) -> None:
    if not index_path.is_file():
        return
    lines = read_text(index_path).splitlines()
    marker = f"`{task_id}`"
    for idx, line in enumerate(lines):
        if not (line.strip().startswith("|") and marker in line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        cells[2] = f"`{status}`"
        lines[idx] = "| " + " | ".join(cells) + " |"
        break
    write_text(index_path, "\n".join(lines))


def detect_root_flag(script_path: Path) -> bool:
    try:
        body = read_text(script_path)
    except Exception:  # noqa: BLE001
        return False
    return "--root" in body


def run_node_p0(repo_root: Path, ccos_root: str, command: str) -> int:
    script = repo_root / ccos_root / "scripts" / "ccos_p0.py"
    if not script.is_file():
        print(f"[error] ccos_p0.py not found: {script}")
        return EXIT_IO

    cmd = [sys.executable, str(script), command]
    if detect_root_flag(script):
        cmd.extend(["--root", str(repo_root)])

    print(f"[run] {command_to_text(cmd)}")
    code = run_subprocess(cmd, cwd=repo_root)
    if code == 0:
        return EXIT_OK
    if code == 1:
        return EXIT_RULE
    return EXIT_IO


def load_registry(hub_root: Path, registry_raw: str) -> tuple[Path, dict[str, Any]]:
    registry_path = resolve_path(hub_root, registry_raw)
    if not registry_path.is_file():
        raise FileNotFoundError(f"registry not found: {registry_path}")
    payload = json_load(registry_path)
    if "projects" not in payload or not isinstance(payload["projects"], list):
        raise ValueError("registry schema invalid: missing 'projects' list")
    return registry_path, payload


def cmd_hub_sync_index(args: argparse.Namespace) -> int:
    try:
        hub_root = resolve_hub_root(args.hub_root)
    except RuntimeError as exc:
        print(f"[error] {exc}")
        return EXIT_ARG

    script = hub_root / "machine" / "federation" / "scripts" / "aggregate_ccos_index.py"
    if not script.is_file():
        print(f"[error] aggregation script missing: {script}")
        return EXIT_IO

    cmd = [
        sys.executable,
        str(script),
        "--ccos-root",
        str(hub_root),
        "--registry",
        args.registry,
        "--output",
        args.output,
    ]
    if args.include_disabled:
        cmd.append("--include-disabled")

    print(f"[run] {command_to_text(cmd)}")
    code = run_subprocess(cmd, cwd=hub_root)
    return EXIT_OK if code == 0 else EXIT_IO


def cmd_hub_register_node(args: argparse.Namespace) -> int:
    try:
        hub_root = resolve_hub_root(args.hub_root)
        registry_path, registry = load_registry(hub_root, args.registry)
    except (RuntimeError, FileNotFoundError, ValueError) as exc:
        print(f"[error] {exc}")
        return EXIT_ARG

    projects = registry.get("projects", [])
    project = None
    for item in projects:
        if item.get("project_id") == args.project_id:
            project = item
            break

    if project is None:
        project = {
            "project_id": args.project_id,
            "repo_root": str(resolve_path(hub_root, args.repo_root)),
            "enabled": True,
            "default_branch": args.default_branch or "main",
            "ccos_nodes": [],
        }
        projects.append(project)

    project["project_id"] = args.project_id
    project["repo_root"] = str(resolve_path(hub_root, args.repo_root))
    if args.default_branch:
        project["default_branch"] = args.default_branch
    if args.project_enabled is not None:
        project["enabled"] = args.project_enabled
    elif "enabled" not in project:
        project["enabled"] = True

    nodes = project.get("ccos_nodes")
    if not isinstance(nodes, list):
        nodes = []
        project["ccos_nodes"] = nodes

    node = None
    for item in nodes:
        if item.get("node_id") == args.node_id:
            node = item
            break

    if node is None:
        node = {}
        nodes.append(node)

    node["node_id"] = args.node_id
    node["ccos_root"] = args.ccos_root
    node["scope"] = args.scope
    if args.node_enabled is not None:
        node["enabled"] = args.node_enabled
    elif "enabled" not in node:
        node["enabled"] = True
    if args.note is not None:
        node["note"] = args.note

    registry["updated_at"] = now_iso()
    json_dump(registry_path, registry)

    print(
        "[ok] node registered: "
        f"project_id={args.project_id} node_id={args.node_id} registry={registry_path}"
    )
    return EXIT_OK


def lint_taskline_docs(task_dir: Path) -> tuple[list[LintIssue], list[LintIssue]]:
    errors: list[LintIssue] = []
    warnings: list[LintIssue] = []

    if not task_dir.is_dir():
        errors.append(
            LintIssue(
                level="error",
                code="taskline.dir.missing",
                message=f"taskline directory missing: {task_dir}",
            )
        )
        return errors, warnings

    field_re = {
        field: re.compile(rf"^- {re.escape(field)}:\s*`?.+`?\s*$", re.M)
        for field in TASK_REQUIRED_FIELDS
    }

    for path in sorted(task_dir.glob("task-*.md")):
        if path.name == "task-index.md":
            continue
        text = read_text(path)
        missing = [field for field, pattern in field_re.items() if not pattern.search(text)]
        if missing:
            errors.append(
                LintIssue(
                    level="error",
                    code="taskline.field.missing",
                    message=f"{path}: missing fields: {', '.join(missing)}",
                )
            )

    return errors, warnings


def lint_task_index_links(task_index: Path, task_dir: Path) -> tuple[list[LintIssue], list[LintIssue]]:
    errors: list[LintIssue] = []
    warnings: list[LintIssue] = []

    if not task_index.is_file():
        warnings.append(
            LintIssue(
                level="warning",
                code="taskindex.missing",
                message=f"task index missing: {task_index}",
            )
        )
        return errors, warnings

    lines = read_text(task_index).splitlines()
    for line in lines:
        if not line.strip().startswith("|") or "`" not in line:
            continue
        if "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        task_doc = strip_ticks(cells[5])
        if not task_doc or task_doc == "待创建":
            continue
        path = task_dir / task_doc
        if not path.is_file():
            warnings.append(
                LintIssue(
                    level="warning",
                    code="taskindex.doc.missing",
                    message=f"task index points to missing doc: {task_doc}",
                )
            )
    return errors, warnings


def lint_registry_and_nodes(
    hub_root: Path,
    registry: dict[str, Any],
) -> tuple[list[LintIssue], list[LintIssue]]:
    errors: list[LintIssue] = []
    warnings: list[LintIssue] = []
    projects = registry.get("projects", [])

    if not isinstance(projects, list):
        errors.append(
            LintIssue(
                level="error",
                code="registry.projects.invalid",
                message="registry.projects is not a list",
            )
        )
        return errors, warnings

    for project in projects:
        project_id = str(project.get("project_id", "")).strip()
        if not project_id:
            errors.append(
                LintIssue(
                    level="error",
                    code="registry.project_id.missing",
                    message="project missing project_id",
                )
            )
            continue

        repo_raw = str(project.get("repo_root", "")).strip()
        if not repo_raw:
            errors.append(
                LintIssue(
                    level="error",
                    code="registry.repo_root.missing",
                    message=f"{project_id}: repo_root missing",
                )
            )
            continue
        repo_root = resolve_path(hub_root, repo_raw)
        if not repo_root.is_dir():
            errors.append(
                LintIssue(
                    level="error",
                    code="registry.repo_root.not_found",
                    message=f"{project_id}: repo_root not found: {repo_root}",
                )
            )

        nodes = project.get("ccos_nodes", [])
        if not isinstance(nodes, list) or not nodes:
            errors.append(
                LintIssue(
                    level="error",
                    code="registry.nodes.missing",
                    message=f"{project_id}: ccos_nodes missing or empty",
                )
            )
            continue

        for node in nodes:
            node_id = str(node.get("node_id", "")).strip()
            if not node_id:
                errors.append(
                    LintIssue(
                        level="error",
                        code="registry.node_id.missing",
                        message=f"{project_id}: node with missing node_id",
                    )
                )
                continue

            enabled = bool(node.get("enabled", True))
            ccos_root = str(node.get("ccos_root", "")).strip() or "CCOS"
            ccos_path = repo_root / ccos_root

            if enabled and not ccos_path.is_dir():
                errors.append(
                    LintIssue(
                        level="error",
                        code="node.ccos_root.not_found",
                        message=f"{project_id}/{node_id}: ccos root missing: {ccos_path}",
                    )
                )
                continue

            if not enabled:
                continue

            index_path = ccos_path / ".index.json"
            if not index_path.is_file():
                warnings.append(
                    LintIssue(
                        level="warning",
                        code="node.index.missing",
                        message=f"{project_id}/{node_id}: missing index {index_path}",
                    )
                )

            p0_rules = ccos_path / "protocol" / "p0-rules.md"
            playbook = ccos_path / "protocol" / "ai-playbook.md"

            if not p0_rules.is_file():
                errors.append(
                    LintIssue(
                        level="error",
                        code="node.protocol.p0.missing",
                        message=f"{project_id}/{node_id}: missing {p0_rules}",
                    )
                )
            if not playbook.is_file():
                errors.append(
                    LintIssue(
                        level="error",
                        code="node.protocol.playbook.missing",
                        message=f"{project_id}/{node_id}: missing {playbook}",
                    )
                )

            for protocol_doc in (p0_rules, playbook):
                if not protocol_doc.is_file():
                    continue
                body = read_text(protocol_doc)
                if ANCHOR_DOC_NAME not in body:
                    errors.append(
                        LintIssue(
                            level="error",
                            code="node.protocol.anchor.missing",
                            message=(
                                f"{project_id}/{node_id}: {protocol_doc} missing hub anchor "
                                f"({ANCHOR_DOC_NAME})"
                            ),
                        )
                    )

    return errors, warnings


def run_hub_lint(hub_root: Path, registry_raw: str) -> tuple[list[LintIssue], list[LintIssue]]:
    errors: list[LintIssue] = []
    warnings: list[LintIssue] = []

    required = [
        hub_root / "meta" / ANCHOR_DOC_NAME,
        hub_root / "machine" / "federation" / "scripts" / "aggregate_ccos_index.py",
    ]
    for path in required:
        if not path.is_file():
            errors.append(
                LintIssue(
                    level="error",
                    code="hub.required.missing",
                    message=f"missing required file: {path}",
                )
            )

    try:
        _, registry = load_registry(hub_root, registry_raw)
    except (FileNotFoundError, ValueError) as exc:
        errors.append(
            LintIssue(
                level="error",
                code="registry.load.failed",
                message=str(exc),
            )
        )
        return errors, warnings

    reg_errors, reg_warnings = lint_registry_and_nodes(hub_root, registry)
    errors.extend(reg_errors)
    warnings.extend(reg_warnings)

    task_dir = hub_root / TASKLINES_REL
    task_index = hub_root / TASK_INDEX_REL
    task_errors, task_warnings = lint_taskline_docs(task_dir)
    errors.extend(task_errors)
    warnings.extend(task_warnings)

    idx_errors, idx_warnings = lint_task_index_links(task_index, task_dir)
    errors.extend(idx_errors)
    warnings.extend(idx_warnings)
    return errors, warnings


def cmd_hub_lint(args: argparse.Namespace) -> int:
    try:
        hub_root = resolve_hub_root(args.hub_root)
    except RuntimeError as exc:
        print(f"[error] {exc}")
        return EXIT_ARG

    errors, warnings = run_hub_lint(hub_root, args.registry)
    if args.strict and warnings:
        errors.extend(
            LintIssue(level="error", code=f"strict.{w.code}", message=w.message)
            for w in warnings
        )
        warnings = []

    for issue in errors:
        print(f"[error] {issue.code}: {issue.message}")
    for issue in warnings:
        print(f"[warn] {issue.code}: {issue.message}")

    print(f"[summary] errors={len(errors)} warnings={len(warnings)}")
    return EXIT_OK if not errors else EXIT_RULE


def cmd_node_validate(args: argparse.Namespace) -> int:
    repo_root = resolve_path(Path.cwd(), args.repo_root)
    return run_node_p0(repo_root=repo_root, ccos_root=args.ccos_root, command="validate")


def cmd_node_sync(args: argparse.Namespace) -> int:
    repo_root = resolve_path(Path.cwd(), args.repo_root)
    return run_node_p0(repo_root=repo_root, ccos_root=args.ccos_root, command="sync")


def cmd_node_status(args: argparse.Namespace) -> int:
    repo_root = resolve_path(Path.cwd(), args.repo_root)
    ccos_root = repo_root / args.ccos_root
    script = ccos_root / "scripts" / "ccos_p0.py"
    index_path = ccos_root / ".index.json"
    marker_path = ccos_root / ".ccos" / "last_sync.json"

    payload: dict[str, Any] = {
        "repo_root": str(repo_root),
        "ccos_root": str(ccos_root),
        "script_exists": script.is_file(),
        "index_exists": index_path.is_file(),
        "marker_exists": marker_path.is_file(),
    }
    if marker_path.is_file():
        try:
            payload["marker"] = json_load(marker_path)
        except Exception as exc:  # noqa: BLE001
            payload["marker_error"] = str(exc)

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return EXIT_OK


def cmd_task_start(args: argparse.Namespace) -> int:
    try:
        hub_root = resolve_hub_root(args.hub_root)
    except RuntimeError as exc:
        print(f"[error] {exc}")
        return EXIT_ARG

    task_dir = hub_root / TASKLINES_REL
    task_dir.mkdir(parents=True, exist_ok=True)
    index_path = hub_root / TASK_INDEX_REL

    existing = find_task_file_by_id(task_dir, args.task_id)
    if existing and not args.force:
        print(f"[error] task already exists: {existing}")
        print("Use --force to overwrite existing task document.")
        return EXIT_STATE

    repo_root = resolve_path(Path.cwd(), args.repo_root)
    task_file = existing if existing else (task_dir / safe_task_filename(args.task_id))
    content = "\n".join(
        [
            f"# {args.title}",
            "",
            metadata_line("taskline_id", args.task_id),
            metadata_line("project_id", args.project_id),
            metadata_line("repo_root", str(repo_root)),
            metadata_line("ccos_node", args.node_id),
            metadata_line("status", "in_progress"),
            metadata_line("priority", args.priority),
            metadata_line("updated_at", today_local()),
            metadata_line("updated_by", "ccosctl task start"),
            "",
            "## Background",
            args.summary.strip() if args.summary.strip() else "N/A",
            "",
            "## Progress Log",
            f"- {timestamp_local()} start task",
            "",
        ]
    )
    write_text(task_file, content)

    upsert_task_index_row(
        index_path=index_path,
        task_id=args.task_id,
        title=args.title,
        status="in_progress",
        priority=args.priority,
        project_id=args.project_id,
        task_doc=task_file.name,
        source_ccos=source_ccos_path(repo_root),
    )
    print(f"[ok] task started: {task_file}")
    return EXIT_OK


def load_task_doc(hub_root: Path, task_id: str) -> tuple[Path, str]:
    task_dir = hub_root / TASKLINES_REL
    task_file = find_task_file_by_id(task_dir, task_id)
    if not task_file:
        raise FileNotFoundError(f"task not found: {task_id}")
    return task_file, read_text(task_file)


def cmd_task_checkpoint(args: argparse.Namespace) -> int:
    try:
        hub_root = resolve_hub_root(args.hub_root)
        task_file, text = load_task_doc(hub_root, args.task_id)
    except (RuntimeError, FileNotFoundError) as exc:
        print(f"[error] {exc}")
        return EXIT_ARG

    text = set_metadata_field(text, "status", args.status)
    text = set_metadata_field(text, "updated_at", today_local())
    text = set_metadata_field(text, "updated_by", "ccosctl task checkpoint")
    if args.summary.strip():
        text = append_progress_log(text, args.summary.strip())
    write_text(task_file, text)
    update_task_index_status(hub_root / TASK_INDEX_REL, args.task_id, args.status)
    print(f"[ok] task checkpoint updated: {task_file}")
    return EXIT_OK


def cmd_task_finish(args: argparse.Namespace) -> int:
    checkpoint_args = argparse.Namespace(
        hub_root=args.hub_root,
        task_id=args.task_id,
        status="done",
        summary=args.result,
    )
    code = cmd_task_checkpoint(checkpoint_args)
    if code != EXIT_OK:
        return code

    try:
        hub_root = resolve_hub_root(args.hub_root)
        task_file, text = load_task_doc(hub_root, args.task_id)
    except (RuntimeError, FileNotFoundError) as exc:
        print(f"[error] {exc}")
        return EXIT_ARG

    text = upsert_section(text, "## Result", [args.result.strip() or "N/A"])
    text = upsert_section(text, "## Next Actions", [args.next_actions.strip() or "N/A"])
    text = set_metadata_field(text, "updated_by", "ccosctl task finish")
    write_text(task_file, text)

    lint_errors, lint_warnings = run_hub_lint(hub_root, args.registry)
    for issue in lint_errors:
        print(f"[error] {issue.code}: {issue.message}")
    for issue in lint_warnings:
        print(f"[warn] {issue.code}: {issue.message}")
    if lint_errors:
        print("[finish] blocked: hub lint failed")
        return EXIT_RULE

    print(f"[ok] task finished: {task_file}")
    return EXIT_OK


def cmd_task_close(args: argparse.Namespace) -> int:
    try:
        hub_root = resolve_hub_root(args.hub_root)
        task_file, text = load_task_doc(hub_root, args.task_id)
    except (RuntimeError, FileNotFoundError) as exc:
        print(f"[error] {exc}")
        return EXIT_ARG

    status_match = re.search(r"^- status:\s*`?([^`\n]+)`?\s*$", text, re.M)
    status = status_match.group(1).strip() if status_match else ""
    if status not in {"done", "closed"}:
        print(f"[error] task status must be done before close, current={status or 'unknown'}")
        return EXIT_STATE

    lint_errors, lint_warnings = run_hub_lint(hub_root, args.registry)
    for issue in lint_errors:
        print(f"[error] {issue.code}: {issue.message}")
    for issue in lint_warnings:
        print(f"[warn] {issue.code}: {issue.message}")
    if lint_errors:
        print("[close] blocked: hub lint failed")
        return EXIT_STATE

    text = set_metadata_field(text, "status", "closed")
    text = set_metadata_field(text, "updated_at", today_local())
    text = set_metadata_field(text, "updated_by", "ccosctl task close")
    text = append_progress_log(text, "close task")
    write_text(task_file, text)
    update_task_index_status(hub_root / TASK_INDEX_REL, args.task_id, "closed")
    print(f"[ok] task closed: {task_file}")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CCOS control plane CLI for hub, node and taskline governance.",
    )
    subparsers = parser.add_subparsers(dest="domain", required=True)

    # hub
    hub = subparsers.add_parser("hub", help="Hub-level governance commands")
    hub_sub = hub.add_subparsers(dest="hub_cmd", required=True)

    hub_sync = hub_sub.add_parser("sync-index", help="Aggregate federation index")
    hub_sync.add_argument("--hub-root", default=None, help="Hub root path (default auto-detect)")
    hub_sync.add_argument("--registry", default=REGISTRY_DEFAULT, help="Registry path")
    hub_sync.add_argument("--output", default=FED_INDEX_DEFAULT, help="Output index path")
    hub_sync.add_argument("--include-disabled", action="store_true")
    hub_sync.set_defaults(func=cmd_hub_sync_index)

    hub_reg = hub_sub.add_parser("register-node", help="Register or update one node in registry")
    hub_reg.add_argument("--hub-root", default=None, help="Hub root path (default auto-detect)")
    hub_reg.add_argument("--registry", default=REGISTRY_DEFAULT, help="Registry path")
    hub_reg.add_argument("--project-id", required=True)
    hub_reg.add_argument("--repo-root", required=True)
    hub_reg.add_argument("--node-id", required=True)
    hub_reg.add_argument("--ccos-root", required=True)
    hub_reg.add_argument("--scope", required=True, choices=["repo", "module"])
    hub_reg.add_argument("--project-enabled", type=parse_bool, default=None)
    hub_reg.add_argument("--node-enabled", type=parse_bool, default=None)
    hub_reg.add_argument("--default-branch", default=None)
    hub_reg.add_argument("--note", default=None)
    hub_reg.set_defaults(func=cmd_hub_register_node)

    hub_lint = hub_sub.add_parser("lint", help="Lint registry, node anchors and taskline fields")
    hub_lint.add_argument("--hub-root", default=None, help="Hub root path (default auto-detect)")
    hub_lint.add_argument("--registry", default=REGISTRY_DEFAULT, help="Registry path")
    hub_lint.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    hub_lint.set_defaults(func=cmd_hub_lint)

    # node
    node = subparsers.add_parser("node", help="Node-level commands")
    node_sub = node.add_subparsers(dest="node_cmd", required=True)

    node_validate = node_sub.add_parser("validate", help="Run node validate")
    node_validate.add_argument("--repo-root", default=".", help="Repository root")
    node_validate.add_argument("--ccos-root", default="CCOS", help="CCOS root under repo")
    node_validate.set_defaults(func=cmd_node_validate)

    node_sync = node_sub.add_parser("sync", help="Run node sync")
    node_sync.add_argument("--repo-root", default=".", help="Repository root")
    node_sync.add_argument("--ccos-root", default="CCOS", help="CCOS root under repo")
    node_sync.set_defaults(func=cmd_node_sync)

    node_status = node_sub.add_parser("status", help="Show node status")
    node_status.add_argument("--repo-root", default=".", help="Repository root")
    node_status.add_argument("--ccos-root", default="CCOS", help="CCOS root under repo")
    node_status.set_defaults(func=cmd_node_status)

    # task
    task = subparsers.add_parser("task", help="Taskline commands")
    task_sub = task.add_subparsers(dest="task_cmd", required=True)

    task_start = task_sub.add_parser("start", help="Create new hub taskline record")
    task_start.add_argument("--hub-root", default=None, help="Hub root path (default auto-detect)")
    task_start.add_argument("--task-id", required=True)
    task_start.add_argument("--title", required=True)
    task_start.add_argument("--project-id", required=True)
    task_start.add_argument("--repo-root", required=True)
    task_start.add_argument("--node-id", required=True)
    task_start.add_argument("--priority", default="P1")
    task_start.add_argument("--summary", default="")
    task_start.add_argument("--force", action="store_true", help="Overwrite if task already exists")
    task_start.set_defaults(func=cmd_task_start)

    task_checkpoint = task_sub.add_parser("checkpoint", help="Append task checkpoint")
    task_checkpoint.add_argument("--hub-root", default=None, help="Hub root path (default auto-detect)")
    task_checkpoint.add_argument("--task-id", required=True)
    task_checkpoint.add_argument("--status", required=True)
    task_checkpoint.add_argument("--summary", default="")
    task_checkpoint.set_defaults(func=cmd_task_checkpoint)

    task_finish = task_sub.add_parser("finish", help="Finish task and run hub lint")
    task_finish.add_argument("--hub-root", default=None, help="Hub root path (default auto-detect)")
    task_finish.add_argument("--registry", default=REGISTRY_DEFAULT, help="Registry path")
    task_finish.add_argument("--task-id", required=True)
    task_finish.add_argument("--result", required=True)
    task_finish.add_argument("--next-actions", default="")
    task_finish.set_defaults(func=cmd_task_finish)

    task_close = task_sub.add_parser("close", help="Close task when done + lint clean")
    task_close.add_argument("--hub-root", default=None, help="Hub root path (default auto-detect)")
    task_close.add_argument("--registry", default=REGISTRY_DEFAULT, help="Registry path")
    task_close.add_argument("--task-id", required=True)
    task_close.set_defaults(func=cmd_task_close)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    func = getattr(args, "func", None)
    if not func:
        parser.print_help()
        return EXIT_ARG
    try:
        return int(func(args))
    except KeyboardInterrupt:
        print("[error] interrupted")
        return EXIT_IO


if __name__ == "__main__":
    raise SystemExit(main())
