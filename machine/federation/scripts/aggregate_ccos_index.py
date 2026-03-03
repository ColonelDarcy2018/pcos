#!/usr/bin/env python3
"""Aggregate CCOS index snapshots from multiple projects into CCOS federation index."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class NodeRecord:
    project_id: str
    node_id: str
    scope: str
    enabled: bool
    repo_root: str
    ccos_root: str
    ccos_exists: bool
    index_exists: bool
    index_generated_at: str | None
    stats: dict[str, Any]
    docs_count: int
    warnings: list[str]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate per-project CCOS .index.json into machine/federation."
    )
    parser.add_argument("--ccos-root", default=".", help="CCOS repository root.")
    parser.add_argument(
        "--registry",
        default="machine/federation/project-registry.json",
        help="Registry path relative to CCOS root.",
    )
    parser.add_argument(
        "--output",
        default="machine/federation/ccos-index-federated.json",
        help="Output path relative to CCOS root.",
    )
    parser.add_argument(
        "--include-disabled",
        action="store_true",
        help="Include nodes whose enabled=false in output.",
    )
    return parser.parse_args()


def resolve_path(base: Path, raw: str) -> Path:
    candidate = Path(raw).expanduser()
    if candidate.is_absolute():
        return candidate
    return (base / candidate).resolve()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_nodes(
    ccos_root_path: Path,
    registry: dict[str, Any],
    include_disabled: bool,
) -> list[NodeRecord]:
    records: list[NodeRecord] = []
    projects = registry.get("projects", [])

    for project in projects:
        project_enabled = bool(project.get("enabled", True))
        if (not project_enabled) and (not include_disabled):
            continue

        project_id = str(project.get("project_id", "")).strip()
        repo_root_raw = str(project.get("repo_root", "")).strip()
        repo_root = resolve_path(ccos_root_path, repo_root_raw) if repo_root_raw else ccos_root_path
        nodes = project.get("ccos_nodes", [])

        for node in nodes:
            enabled = bool(node.get("enabled", True))
            if (not enabled) and (not include_disabled):
                continue

            node_id = str(node.get("node_id", "default")).strip() or "default"
            scope = str(node.get("scope", "repo")).strip() or "repo"
            ccos_root = str(node.get("ccos_root", "CCOS")).strip() or "CCOS"
            ccos_path = (repo_root / ccos_root).resolve()
            index_path = ccos_path / ".index.json"

            warnings: list[str] = []
            stats: dict[str, Any] = {}
            index_generated_at: str | None = None
            docs_count = 0

            ccos_exists = ccos_path.is_dir()
            index_exists = index_path.is_file()

            if not ccos_exists:
                warnings.append("CCOS root is missing.")
            if ccos_exists and not index_exists:
                warnings.append("CCOS .index.json is missing; run ccos sync in that project.")

            if index_exists:
                try:
                    payload = load_json(index_path)
                    stats = payload.get("stats", {}) if isinstance(payload, dict) else {}
                    index_generated_at = payload.get("generated_at")
                    docs_count = int(stats.get("docs", 0))
                except Exception as exc:  # noqa: BLE001
                    warnings.append(f"Failed to parse .index.json: {exc}")

            records.append(
                NodeRecord(
                    project_id=project_id,
                    node_id=node_id,
                    scope=scope,
                    enabled=enabled,
                    repo_root=str(repo_root),
                    ccos_root=ccos_root,
                    ccos_exists=ccos_exists,
                    index_exists=index_exists,
                    index_generated_at=index_generated_at,
                    stats=stats,
                    docs_count=docs_count,
                    warnings=warnings,
                )
            )

    return records


def build_output(
    registry_rel: str,
    projects_count: int,
    nodes: list[NodeRecord],
) -> dict[str, Any]:
    nodes_total = len(nodes)
    nodes_enabled = sum(1 for node in nodes if node.enabled)
    nodes_indexed = sum(1 for node in nodes if node.index_exists)

    serializable_nodes: list[dict[str, Any]] = []
    for node in nodes:
        serializable_nodes.append(
            {
                "project_id": node.project_id,
                "node_id": node.node_id,
                "scope": node.scope,
                "enabled": node.enabled,
                "repo_root": node.repo_root,
                "ccos_root": node.ccos_root,
                "ccos_exists": node.ccos_exists,
                "index_exists": node.index_exists,
                "index_generated_at": node.index_generated_at,
                "docs_count": node.docs_count,
                "stats": node.stats,
                "warnings": node.warnings,
            }
        )

    return {
        "schema_version": 1,
        "generated_at": now_iso(),
        "source_registry": registry_rel,
        "summary": {
            "projects": projects_count,
            "nodes_total": nodes_total,
            "nodes_enabled": nodes_enabled,
            "nodes_indexed": nodes_indexed,
        },
        "nodes": serializable_nodes,
    }


def main() -> int:
    args = parse_args()
    hub_root = Path(args.ccos_root).expanduser().resolve()
    registry_path = resolve_path(hub_root, args.registry)
    output_path = resolve_path(hub_root, args.output)

    if not registry_path.is_file():
        print(f"[error] registry not found: {registry_path}")
        return 2

    registry = load_json(registry_path)
    nodes = collect_nodes(
        ccos_root_path=hub_root,
        registry=registry,
        include_disabled=args.include_disabled,
    )
    projects_count = len({node.project_id for node in nodes})
    payload = build_output(
        registry_rel=args.registry,
        projects_count=projects_count,
        nodes=nodes,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = payload["summary"]
    print(
        "[ok] federation index updated: "
        f"projects={summary['projects']} "
        f"nodes={summary['nodes_total']} "
        f"indexed={summary['nodes_indexed']}"
    )
    print(f"[path] {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
