from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_DIRS = [
    "context",
    "knowledge",
    "templates",
    "assets",
    "scripts",
    ".ccos",
]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
WINDOWS_ABS_RE = re.compile(r"^[A-Za-z]:[\\/]")
EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "tel:")


@dataclass
class Issue:
    level: str
    path: str
    message: str


@dataclass
class DocMeta:
    path: str
    id: str | None
    domain: str | None
    tags: list[str]
    related: list[str]
    has_ccos_index: bool


@dataclass
class ValidationResult:
    errors: list[Issue]
    warnings: list[Issue]
    docs: list[DocMeta]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and (
        (value.startswith('"') and value.endswith('"'))
        or (value.startswith("'") and value.endswith("'"))
    ):
        return value[1:-1]
    return value


def parse_inline_list(value: str) -> list[str]:
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return [strip_quotes(value)] if value else []
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [strip_quotes(item.strip()) for item in inner.split(",") if item.strip()]


def extract_frontmatter(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end_idx = text.find("\n---\n", 4)
    if end_idx == -1:
        return None
    return text[4:end_idx]


def parse_ccos_index(frontmatter: str) -> dict[str, object] | None:
    lines = frontmatter.splitlines()
    ccos_index_indent = None
    start_idx = -1

    for idx, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("CCOS-Index:"):
            ccos_index_indent = len(line) - len(stripped)
            if stripped != "CCOS-Index:":
                return {}
            start_idx = idx + 1
            break

    if start_idx == -1:
        return None

    parsed: dict[str, object] = {}
    current_key: str | None = None

    for line in lines[start_idx:]:
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip())
        if indent <= (ccos_index_indent or 0):
            break

        stripped = line.strip()
        if stripped.startswith("- "):
            item = strip_quotes(stripped[2:].strip())
            if current_key and isinstance(parsed.get(current_key), list):
                parsed[current_key].append(item)
            continue

        if ":" not in stripped:
            continue

        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        current_key = key

        if key in {"tags", "related"}:
            if raw_value:
                parsed[key] = parse_inline_list(raw_value)
            else:
                parsed[key] = []
            continue

        parsed[key] = strip_quotes(raw_value) if raw_value else ""

    return parsed


def is_external_target(target: str) -> bool:
    lower = target.lower()
    return lower.startswith(EXTERNAL_SCHEMES)


def is_absolute_local_target(target: str) -> bool:
    if target.startswith("file://"):
        return True
    if target.startswith("/"):
        return True
    if WINDOWS_ABS_RE.match(target):
        return True
    return False


def resolve_repo_root(root_arg: str | None) -> Path:
    start = Path(root_arg or ".").resolve()
    if (start / "CCOS").is_dir():
        return start
    if start.name == "CCOS" and start.is_dir():
        return start.parent
    raise ValueError(
        "Cannot locate repository root. Run inside repo root or pass --root <repo_root>."
    )


def collect_markdown_files(knowledge_root: Path) -> list[Path]:
    return sorted(path for path in knowledge_root.rglob("*.md") if path.is_file())


def validate_required_dirs(repo_root: Path, errors: list[Issue]) -> None:
    ccos_root = repo_root / "CCOS"
    for rel in REQUIRED_DIRS:
        target = ccos_root / rel
        if not target.is_dir():
            errors.append(
                Issue(
                    level="error",
                    path=str(target.relative_to(repo_root)),
                    message="Required directory is missing.",
                )
            )


def validate_knowledge_readmes(repo_root: Path, errors: list[Issue]) -> None:
    knowledge_root = repo_root / "CCOS" / "knowledge"
    if not knowledge_root.is_dir():
        return
    for child in sorted(knowledge_root.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        readme_path = child / "README.md"
        if not readme_path.is_file():
            errors.append(
                Issue(
                    level="error",
                    path=str(child.relative_to(repo_root)),
                    message="Missing README.md in knowledge first-level directory.",
                )
            )


def validate_links(
    repo_root: Path,
    file_path: Path,
    text: str,
    errors: list[Issue],
    warnings: list[Issue],
) -> None:
    for match in LINK_RE.finditer(text):
        raw_target = match.group(1).strip()
        if not raw_target or raw_target.startswith("#"):
            continue

        target_no_anchor = raw_target.split("#", 1)[0].strip()
        if not target_no_anchor:
            continue

        if is_external_target(target_no_anchor):
            continue

        if is_absolute_local_target(target_no_anchor):
            errors.append(
                Issue(
                    level="error",
                    path=str(file_path.relative_to(repo_root)),
                    message=f"Absolute local link is forbidden: {raw_target}",
                )
            )
            continue

        resolved = (file_path.parent / target_no_anchor).resolve()
        if not resolved.exists():
            warnings.append(
                Issue(
                    level="warning",
                    path=str(file_path.relative_to(repo_root)),
                    message=f"Link target does not exist: {raw_target}",
                )
            )


def validate_related_links(
    repo_root: Path,
    file_path: Path,
    related: list[str],
    warnings: list[Issue],
) -> None:
    for rel_target in related:
        target = rel_target.strip()
        if not target or target.startswith("#"):
            continue
        if is_external_target(target):
            continue
        if is_absolute_local_target(target):
            warnings.append(
                Issue(
                    level="warning",
                    path=str(file_path.relative_to(repo_root)),
                    message=f"CCOS-Index.related uses absolute local path: {target}",
                )
            )
            continue
        resolved = (file_path.parent / target).resolve()
        if not resolved.exists():
            warnings.append(
                Issue(
                    level="warning",
                    path=str(file_path.relative_to(repo_root)),
                    message=f"CCOS-Index.related target does not exist: {target}",
                )
            )


def extract_doc_meta(
    repo_root: Path,
    file_path: Path,
    warnings: list[Issue],
) -> DocMeta:
    text = file_path.read_text(encoding="utf-8")
    frontmatter = extract_frontmatter(text)
    ccos_index = parse_ccos_index(frontmatter) if frontmatter else None

    has_index = ccos_index is not None
    doc_id = None
    domain = None
    tags: list[str] = []
    related: list[str] = []

    if not has_index:
        warnings.append(
            Issue(
                level="warning",
                path=str(file_path.relative_to(repo_root)),
                message="CCOS-Index front matter is missing.",
            )
        )
    else:
        if isinstance(ccos_index.get("id"), str) and ccos_index.get("id", "").strip():
            doc_id = str(ccos_index["id"]).strip()
        else:
            warnings.append(
                Issue(
                    level="warning",
                    path=str(file_path.relative_to(repo_root)),
                    message="CCOS-Index.id is missing.",
                )
            )

        if isinstance(ccos_index.get("domain"), str) and ccos_index.get("domain", "").strip():
            domain = str(ccos_index["domain"]).strip()

        raw_tags = ccos_index.get("tags")
        if isinstance(raw_tags, list):
            tags = [str(item).strip() for item in raw_tags if str(item).strip()]

        raw_related = ccos_index.get("related")
        if isinstance(raw_related, list):
            related = [str(item).strip() for item in raw_related if str(item).strip()]

        validate_related_links(repo_root, file_path, related, warnings)

    return DocMeta(
        path=str(file_path.relative_to(repo_root)),
        id=doc_id,
        domain=domain,
        tags=tags,
        related=related,
        has_ccos_index=has_index,
    )


def validate_repo(repo_root: Path) -> ValidationResult:
    errors: list[Issue] = []
    warnings: list[Issue] = []
    docs: list[DocMeta] = []

    validate_required_dirs(repo_root, errors)
    validate_knowledge_readmes(repo_root, errors)

    knowledge_root = repo_root / "CCOS" / "knowledge"
    if knowledge_root.is_dir():
        ids: dict[str, str] = {}
        for file_path in collect_markdown_files(knowledge_root):
            text = file_path.read_text(encoding="utf-8")
            validate_links(repo_root, file_path, text, errors, warnings)
            meta = extract_doc_meta(repo_root, file_path, warnings)
            docs.append(meta)

            if meta.id:
                if meta.id in ids:
                    errors.append(
                        Issue(
                            level="error",
                            path=meta.path,
                            message=f"Duplicate CCOS-Index.id '{meta.id}' already used by {ids[meta.id]}",
                        )
                    )
                else:
                    ids[meta.id] = meta.path

    return ValidationResult(errors=errors, warnings=warnings, docs=docs)


def write_index(repo_root: Path, result: ValidationResult) -> None:
    ccos_root = repo_root / "CCOS"
    index_path = ccos_root / ".index.json"
    marker_path = ccos_root / ".ccos" / "last_sync.json"

    doc_items = []
    for meta in result.docs:
        abs_path = repo_root / meta.path
        updated_at = datetime.fromtimestamp(abs_path.stat().st_mtime, tz=timezone.utc).isoformat()
        doc_items.append(
            {
                "path": meta.path,
                "id": meta.id,
                "domain": meta.domain,
                "tags": meta.tags,
                "related": meta.related,
                "has_ccos_index": meta.has_ccos_index,
                "updated_at": updated_at,
            }
        )

    payload = {
        "generated_at": now_iso(),
        "ccos_root": "CCOS",
        "stats": {
            "docs": len(result.docs),
            "errors": len(result.errors),
            "warnings": len(result.warnings),
        },
        "docs": doc_items,
    }

    marker = {
        "last_sync_at": now_iso(),
        "docs": len(result.docs),
        "warnings": len(result.warnings),
    }

    index_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    marker_path.parent.mkdir(parents=True, exist_ok=True)
    marker_path.write_text(
        json.dumps(marker, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def print_issues(issues: list[Issue]) -> None:
    for issue in issues:
        print(f"[{issue.level}] {issue.path}: {issue.message}")


def cmd_validate(repo_root: Path) -> int:
    result = validate_repo(repo_root)
    print_issues(result.errors)
    print_issues(result.warnings)
    print(
        f"[summary] docs={len(result.docs)} errors={len(result.errors)} warnings={len(result.warnings)}"
    )
    return 1 if result.errors else 0


def cmd_sync(repo_root: Path) -> int:
    result = validate_repo(repo_root)
    print_issues(result.errors)
    print_issues(result.warnings)
    if result.errors:
        print("[sync] aborted due to validation errors")
        return 1
    write_index(repo_root, result)
    print("[sync] wrote CCOS/.index.json and CCOS/.ccos/last_sync.json")
    print(
        f"[summary] docs={len(result.docs)} errors={len(result.errors)} warnings={len(result.warnings)}"
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CCOS P0 utility script")
    parser.add_argument("command", choices=["validate", "sync"])
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root path (default: current directory)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo_root = resolve_repo_root(args.root)
    except ValueError as exc:
        print(f"[error] {exc}")
        return 2

    if args.command == "validate":
        return cmd_validate(repo_root)
    if args.command == "sync":
        return cmd_sync(repo_root)
    print(f"[error] unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
