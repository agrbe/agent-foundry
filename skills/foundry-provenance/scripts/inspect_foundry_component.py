#!/usr/bin/env python3
"""Inspect an agent-foundry artifact and propose registry and notice updates."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

VALID_KINDS = {"skill", "agent", "mcp", "hook", "other"}
VALID_ORIGINS = {"native", "third_party", "adapted"}

TITLE_TOKENS = {
    "api": "API",
    "ai": "AI",
    "ui": "UI",
    "ux": "UX",
    "qa": "QA",
    "mcp": "MCP",
    "it": "IT",
    "llm": "LLM",
    "ml": "ML",
    "mlops": "MLOps",
    "nlp": "NLP",
    "sre": "SRE",
    "seo": "SEO",
    "iot": "IoT",
    "m365": "M365",
    "ad": "AD",
    "cpp": "C++",
    "csharp": "C#",
    "dotnet": ".NET",
    "graphql": "GraphQL",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "nextjs": "Next.js",
    "powershell": "PowerShell",
    "wordpress": "WordPress",
    "postgres": "Postgres",
    "php": "PHP",
    "sql": "SQL",
    "websocket": "WebSocket",
    "devops": "DevOps",
}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    lowered = normalize_text(value).lower()
    if lowered in {"true", "yes", "1"}:
        return True
    if lowered in {"false", "no", "0"}:
        return False
    return None


def title_from_slug(value: str) -> str:
    parts = []
    for token in value.replace("_", "-").split("-"):
        if not token:
            continue
        if token in TITLE_TOKENS:
            parts.append(TITLE_TOKENS[token])
        elif re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", token):
            parts.append(token)
        else:
            parts.append(token.capitalize())
    return " ".join(parts)


def relative_path(path: Path, base: Path) -> str:
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path.resolve())


def load_yaml_file(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_frontmatter(path: Path) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        return None, "SKILL.md is missing valid YAML frontmatter"
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, f"SKILL.md frontmatter is invalid YAML: {exc}"
    if not isinstance(data, dict):
        return None, "SKILL.md frontmatter must be a YAML mapping"
    return data, None


def load_registry(path: Path) -> Tuple[Dict[str, Any], Dict[str, List[Dict[str, Any]]], List[str]]:
    warnings: List[str] = []
    if not path.exists():
        warnings.append(f"Registry file not found: {path}")
        return {}, {}, warnings
    try:
        data = load_yaml_file(path)
    except Exception as exc:
        warnings.append(f"Failed to read registry: {exc}")
        return {}, {}, warnings
    if not isinstance(data, dict):
        warnings.append("Registry root is not a YAML mapping")
        return {}, {}, warnings
    catalog = data.get("catalog", {})
    if not isinstance(catalog, dict):
        warnings.append("Registry catalog is not a YAML mapping")
        return data, {}, warnings
    sections: Dict[str, List[Dict[str, Any]]] = {}
    for name, value in catalog.items():
        if isinstance(value, list):
            sections[name] = [item for item in value if isinstance(item, dict)]
    return data, sections, warnings


def find_nearest_file(start: Path, filename: str, stop_at: Path) -> Optional[Path]:
    current = start if start.is_dir() else start.parent
    stop_at = stop_at.resolve()
    while True:
        candidate = current / filename
        if candidate.exists():
            return candidate
        if current.resolve() == stop_at:
            return None
        if current.parent == current:
            return None
        current = current.parent


def infer_kind(path: Path) -> str:
    if path.is_file() and path.name == "SKILL.md":
        return "skill"
    if path.is_file() and path.suffix == ".toml":
        return "agent"
    parts = path.parts
    if "skills" in parts or (path.is_dir() and (path / "SKILL.md").exists()):
        return "skill"
    if "agents" in parts or list(path.glob("*.toml")) or list(path.rglob("*.toml")):
        return "agent"
    if "mcp" in parts or "mcps" in parts:
        return "mcp"
    if "hooks" in parts:
        return "hook"
    return "other"


def detect_origin(
    explicit_origin: str,
    meta: Optional[Dict[str, Any]],
    source_repo: str,
    modified_from_source: Optional[bool],
) -> Tuple[Optional[str], List[str], List[str]]:
    warnings: List[str] = []
    questions: List[str] = []
    meta = meta or {}

    origin = explicit_origin or normalize_text(meta.get("origin"))
    source_repo = source_repo or normalize_text(meta.get("source_repo"))
    if modified_from_source is None:
        modified_from_source = normalize_bool(meta.get("modified_from_source"))

    if origin:
        if origin not in VALID_ORIGINS:
            warnings.append("Origin must be one of native, third_party, or adapted.")
            origin = None
    elif source_repo:
        if modified_from_source is None:
            questions.append("Was the imported content modified from the upstream source?")
        else:
            origin = "adapted" if modified_from_source else "third_party"
    elif meta:
        origin = "native"

    if not origin:
        questions.append("Is this artifact native, third_party, or adapted?")
        return None, warnings, questions

    if origin in {"third_party", "adapted"} and not source_repo:
        questions.append("What are the upstream source repository and source path?")
    if origin == "third_party" and modified_from_source is True:
        warnings.append("A third_party artifact should not declare modified_from_source: true.")
    if origin == "adapted" and modified_from_source is False:
        warnings.append("An adapted artifact should declare modified_from_source: true.")
    if origin == "native" and source_repo:
        warnings.append("A native artifact should not declare source_repo.")

    return origin, warnings, questions


def section_for_kind(kind: str) -> Optional[str]:
    mapping = {
        "skill": "skills",
        "agent": "agents",
        "mcp": "mcps",
        "hook": "hooks",
    }
    return mapping.get(kind)


def comparable_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(entry)
    if "tags" in result and not result["tags"]:
        result.pop("tags")
    return result


def detect_duplicates(
    entries: List[Dict[str, Any]],
    existing: List[Dict[str, Any]],
) -> Tuple[List[str], List[str], int]:
    errors: List[str] = []
    warnings: List[str] = []
    already_registered = 0
    matching_ids: List[str] = []
    for entry in entries:
        by_id = next((item for item in existing if normalize_text(item.get("id")) == normalize_text(entry.get("id"))), None)
        by_path = next((item for item in existing if normalize_text(item.get("path")) == normalize_text(entry.get("path"))), None)
        match = by_id or by_path
        if not match:
            continue
        if comparable_entry(match) == comparable_entry(entry):
            already_registered += 1
            matching_ids.append(normalize_text(entry.get("id")))
            continue
        if by_id:
            errors.append(f"registry.yaml already contains {entry.get('id')} in the target section.")
        if by_path and by_path is not by_id:
            errors.append(f"registry.yaml already contains path `{entry.get('path')}` in the target section.")
    if matching_ids:
        if len(matching_ids) == 1:
            warnings.append(f"registry.yaml already contains a matching entry for `{matching_ids[0]}`.")
        elif len(matching_ids) <= 10:
            warnings.append(
                "registry.yaml already contains matching entries for: "
                + ", ".join(f"`{item}`" for item in matching_ids)
                + "."
            )
        else:
            sample = ", ".join(f"`{item}`" for item in matching_ids[:5])
            warnings.append(
                f"registry.yaml already contains {len(matching_ids)} matching entries; sample: {sample}."
            )
    return errors, warnings, already_registered


def build_notice_block(
    kind: str,
    path: Path,
    origin: str,
    source_repo: str,
    source_path: str,
    license_name: str,
    modified_from_source: bool,
    owner: str,
    count: int,
    repo_root: Path,
) -> Optional[str]:
    if origin not in {"third_party", "adapted"} or not source_repo or not license_name:
        return None
    label = title_from_slug(path.stem if path.is_file() else path.name)
    path_text = relative_path(path, repo_root)
    modified_text = "yes" if modified_from_source else "no"
    if count > 1:
        artifact_label = f"{label} Import"
        included = f"`{count}` imported `{kind}` artifacts"
    else:
        artifact_label = label
        included = f"`1` imported `{kind}` artifact"
    source_line = f"`{source_repo}`"
    if source_path:
        source_line += f" (`{source_path}`)"
    return "\n".join(
        [
            f"### {artifact_label}",
            f"- Path: `{path_text}`",
            f"- Included upstream material: {included}",
            f"- Origin: `{origin}`",
            f"- Source: {source_line}",
            f"- License: `{license_name}`",
            f"- Modified: `{modified_text}`",
            f"- Owner: `{owner}`",
            f"- Status: `draft`",
        ]
    )


def inspect_skill_component(
    path: Path,
    repo_root: Path,
    registry_data: Dict[str, Any],
    sections: Dict[str, List[Dict[str, Any]]],
    args: argparse.Namespace,
) -> Dict[str, Any]:
    report: Dict[str, Any] = {"kind": "skill", "errors": [], "warnings": [], "questions": []}
    skill_dir = path if path.is_dir() else path.parent
    skill_md = skill_dir / "SKILL.md"
    structure = {
        "SKILL.md": skill_md.exists(),
        "foundry.yaml": (skill_dir / "foundry.yaml").exists(),
        "agents/openai.yaml": (skill_dir / "agents" / "openai.yaml").exists(),
        "LICENSE.txt": (skill_dir / "LICENSE.txt").exists(),
        "NOTICE.txt": (skill_dir / "NOTICE.txt").exists(),
        "scripts/": (skill_dir / "scripts").is_dir(),
        "references/": (skill_dir / "references").is_dir(),
        "assets/": (skill_dir / "assets").is_dir(),
    }
    report["structure"] = structure
    if not skill_md.exists():
        report["errors"].append("SKILL.md is required for a skill artifact.")
        report["status"] = "invalid"
        return report
    frontmatter, error = load_frontmatter(skill_md)
    if error:
        report["errors"].append(error)
        report["status"] = "invalid"
        return report
    meta = None
    if (skill_dir / "foundry.yaml").exists():
        loaded = load_yaml_file(skill_dir / "foundry.yaml")
        if loaded is None:
            meta = {}
        elif isinstance(loaded, dict):
            meta = loaded
        else:
            report["errors"].append("foundry.yaml must be a YAML mapping.")
            report["status"] = "invalid"
            return report
    repo = registry_data.get("repo", {}) if isinstance(registry_data.get("repo"), dict) else {}
    origin, origin_warnings, origin_questions = detect_origin(
        normalize_text(args.origin),
        meta,
        normalize_text(args.source_repo),
        normalize_bool(args.modified_from_source),
    )
    report["warnings"].extend(origin_warnings)
    report["questions"].extend(origin_questions)
    owner = normalize_text(args.owner) or normalize_text((meta or {}).get("owner")) or normalize_text(repo.get("default_owner"))
    license_name = normalize_text(args.license) or normalize_text((meta or {}).get("license"))
    if not license_name and origin == "native":
        license_name = normalize_text(repo.get("license"))
    if origin in {"third_party", "adapted"} and not license_name:
        report["questions"].append("What upstream license applies to this external artifact?")
    entry = {
        "id": normalize_text(args.id) or normalize_text((meta or {}).get("id")) or normalize_text(frontmatter.get("name")) or skill_dir.name,
        "path": relative_path(skill_dir, repo_root),
        "title": normalize_text(args.title) or normalize_text((meta or {}).get("title")) or title_from_slug(normalize_text(frontmatter.get("name")) or skill_dir.name),
        "description": normalize_text(frontmatter.get("description")),
        "origin": origin or "",
        "owner": owner,
        "license": license_name,
        "source_repo": normalize_text(args.source_repo) or normalize_text((meta or {}).get("source_repo")),
        "source_path": normalize_text(args.source_path) or normalize_text((meta or {}).get("source_path")),
        "modified_from_source": normalize_bool(args.modified_from_source),
        "status": normalize_text((meta or {}).get("status")) or "draft",
    }
    if entry["modified_from_source"] is None:
        entry["modified_from_source"] = entry["origin"] == "adapted"
    tags = (meta or {}).get("tags")
    if isinstance(tags, list):
        clean_tags = [normalize_text(tag) for tag in tags if normalize_text(tag)]
        if clean_tags:
            entry["tags"] = clean_tags
    report["proposed_registry_entries"] = [entry]
    existing = sections.get("skills", [])
    duplicate_errors, duplicate_warnings, already_registered = detect_duplicates([entry], existing)
    report["errors"].extend(duplicate_errors)
    report["warnings"].extend(duplicate_warnings)
    report["already_registered_count"] = already_registered
    if entry["origin"] in {"third_party", "adapted"} and not structure["LICENSE.txt"]:
        report["errors"].append("External skills should include a local LICENSE.txt.")
    report["proposed_notice_block"] = build_notice_block(
        kind="skill",
        path=skill_dir,
        origin=entry["origin"],
        source_repo=entry["source_repo"],
        source_path=entry["source_path"],
        license_name=entry["license"],
        modified_from_source=bool(entry["modified_from_source"]),
        owner=entry["owner"],
        count=1,
        repo_root=repo_root,
    )
    return report


def inspect_agent_component(
    path: Path,
    repo_root: Path,
    sections: Dict[str, List[Dict[str, Any]]],
    args: argparse.Namespace,
) -> Dict[str, Any]:
    report: Dict[str, Any] = {"kind": "agent", "errors": [], "warnings": [], "questions": []}
    if path.is_file():
        agent_files = [path]
        base_dir = path.parent
    else:
        agent_files = sorted(path.rglob("*.toml"))
        base_dir = path
    structure = {
        "path_is_directory": path.is_dir(),
        "agent_file_count": len(agent_files),
        "README.md": (base_dir / "README.md").exists(),
        "LICENSE.txt": bool(find_nearest_file(path, "LICENSE.txt", repo_root)),
        "NOTICE.txt": bool(find_nearest_file(path, "NOTICE.txt", repo_root)),
    }
    report["structure"] = structure
    if not agent_files:
        report["errors"].append("No .toml agent files were found.")
        report["status"] = "invalid"
        return report
    origin, origin_warnings, origin_questions = detect_origin(
        normalize_text(args.origin),
        None,
        normalize_text(args.source_repo),
        normalize_bool(args.modified_from_source),
    )
    report["warnings"].extend(origin_warnings)
    report["questions"].extend(origin_questions)

    registry_owner = "@agrbe"
    license_name = normalize_text(args.license)
    if origin in {"third_party", "adapted"} and not license_name:
        report["questions"].append("What upstream license applies to this external artifact?")
    owner = normalize_text(args.owner) or registry_owner
    entries: List[Dict[str, Any]] = []
    source_path_root = normalize_text(args.source_path)
    for agent_file in agent_files:
        try:
            data = tomllib.loads(agent_file.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            report["errors"].append(f"Failed to parse {relative_path(agent_file, repo_root)}: {exc}")
            continue
        name = normalize_text(data.get("name"))
        description = normalize_text(data.get("description"))
        if not name or not description:
            report["errors"].append(f"{relative_path(agent_file, repo_root)} is missing `name` or `description`.")
            continue
        source_path = ""
        if source_path_root:
            if path.is_dir():
                source_path = f"{source_path_root.rstrip('/')}/{agent_file.relative_to(path).as_posix()}"
            else:
                source_path = source_path_root
        category = re.sub(r"^\d+-", "", agent_file.parent.name)
        entry: Dict[str, Any] = {
            "id": name,
            "path": relative_path(agent_file, repo_root),
            "title": title_from_slug(name),
            "description": description,
            "origin": origin or "",
            "owner": owner,
            "license": license_name,
            "source_repo": normalize_text(args.source_repo),
            "source_path": source_path,
            "modified_from_source": normalize_bool(args.modified_from_source),
            "status": "draft",
            "tags": ["codex", "subagent", category],
        }
        if entry["modified_from_source"] is None:
            entry["modified_from_source"] = entry["origin"] == "adapted"
        entries.append(entry)
    report["proposed_registry_entries"] = entries
    duplicate_errors, duplicate_warnings, already_registered = detect_duplicates(entries, sections.get("agents", []))
    report["errors"].extend(duplicate_errors)
    report["warnings"].extend(duplicate_warnings)
    report["already_registered_count"] = already_registered
    if origin in {"third_party", "adapted"} and not structure["LICENSE.txt"]:
        report["errors"].append("External agent imports should have a nearby LICENSE.txt.")
    report["proposed_notice_block"] = build_notice_block(
        kind="agent",
        path=path,
        origin=origin or "",
        source_repo=normalize_text(args.source_repo),
        source_path=source_path_root,
        license_name=license_name,
        modified_from_source=bool(normalize_bool(args.modified_from_source)),
        owner=owner,
        count=len(entries),
        repo_root=repo_root,
    )
    return report


def inspect_generic_component(
    path: Path,
    kind: str,
    repo_root: Path,
    registry_data: Dict[str, Any],
    sections: Dict[str, List[Dict[str, Any]]],
    args: argparse.Namespace,
) -> Dict[str, Any]:
    report: Dict[str, Any] = {"kind": kind, "errors": [], "warnings": [], "questions": []}
    structure = {
        "path_exists": path.exists(),
        "path_is_directory": path.is_dir(),
        "README.md": (path / "README.md").exists() if path.is_dir() else False,
        "LICENSE.txt": bool(find_nearest_file(path, "LICENSE.txt", repo_root)),
        "NOTICE.txt": bool(find_nearest_file(path, "NOTICE.txt", repo_root)),
    }
    report["structure"] = structure
    if not path.exists():
        report["errors"].append("Target path does not exist.")
        report["status"] = "invalid"
        return report
    origin, origin_warnings, origin_questions = detect_origin(
        normalize_text(args.origin),
        None,
        normalize_text(args.source_repo),
        normalize_bool(args.modified_from_source),
    )
    report["warnings"].extend(origin_warnings)
    report["questions"].extend(origin_questions)
    repo = registry_data.get("repo", {}) if isinstance(registry_data.get("repo"), dict) else {}
    owner = normalize_text(args.owner) or normalize_text(repo.get("default_owner"))
    license_name = normalize_text(args.license)
    if not license_name and origin == "native":
        license_name = normalize_text(repo.get("license"))
    if origin in {"third_party", "adapted"} and not license_name:
        report["questions"].append("What upstream license applies to this external artifact?")
    description = normalize_text(args.description)
    if not description:
        report["questions"].append("What catalog description should be used for this artifact?")
    section = section_for_kind(kind)
    if not section:
        report["questions"].append("Which registry section should track this artifact?")
    elif section not in sections:
        report["warnings"].append(f"registry.yaml does not currently define catalog.{section}.")
    entry = {
        "id": normalize_text(args.id) or path.stem if path.is_file() else path.name,
        "path": relative_path(path, repo_root),
        "title": normalize_text(args.title) or title_from_slug(path.stem if path.is_file() else path.name),
        "description": description,
        "origin": origin or "",
        "owner": owner,
        "license": license_name,
        "source_repo": normalize_text(args.source_repo),
        "source_path": normalize_text(args.source_path),
        "modified_from_source": normalize_bool(args.modified_from_source),
        "status": "draft",
    }
    if entry["modified_from_source"] is None:
        entry["modified_from_source"] = entry["origin"] == "adapted"
    report["proposed_registry_entries"] = [entry]
    existing = sections.get(section, []) if section else []
    duplicate_errors, duplicate_warnings, already_registered = detect_duplicates([entry], existing)
    report["errors"].extend(duplicate_errors)
    report["warnings"].extend(duplicate_warnings)
    report["already_registered_count"] = already_registered
    if origin in {"third_party", "adapted"} and not structure["LICENSE.txt"]:
        report["errors"].append("External artifacts should have a nearby LICENSE.txt.")
    report["proposed_notice_block"] = build_notice_block(
        kind=kind,
        path=path,
        origin=origin or "",
        source_repo=normalize_text(args.source_repo),
        source_path=normalize_text(args.source_path),
        license_name=license_name,
        modified_from_source=bool(entry["modified_from_source"]),
        owner=owner,
        count=1,
        repo_root=repo_root,
    )
    return report


def finalize_report(report: Dict[str, Any], sections: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    kind = report.get("kind", "")
    section = section_for_kind(kind)
    report["registry_section"] = section
    if section and section not in sections:
        report.setdefault("warnings", []).append(f"catalog.{section} is missing and may need to be created.")
    errors = report.get("errors", [])
    questions = report.get("questions", [])
    proposed_entries = report.get("proposed_registry_entries", [])
    already_registered = int(report.get("already_registered_count", 0))
    if errors:
        report["status"] = "invalid"
    elif questions:
        report["status"] = "needs_input"
    elif proposed_entries and already_registered == len(proposed_entries):
        report["status"] = "already_registered"
    else:
        report["status"] = "ready_to_apply"
    return report


def render_human(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append(f"Path: {report.get('path')}")
    lines.append(f"Kind: {report.get('kind')}")
    lines.append(f"Status: {report.get('status')}")
    section = report.get("registry_section")
    if section:
        lines.append(f"Registry section: catalog.{section}")
    lines.append("")
    lines.append("Structure:")
    for key, value in report.get("structure", {}).items():
        lines.append(f"- {key}: {value}")
    if report.get("errors"):
        lines.append("")
        lines.append("Errors:")
        for item in report["errors"]:
            lines.append(f"- {item}")
    if report.get("warnings"):
        lines.append("")
        lines.append("Warnings:")
        for item in report["warnings"]:
            lines.append(f"- {item}")
    if report.get("questions"):
        lines.append("")
        lines.append("Questions:")
        for item in report["questions"]:
            lines.append(f"- {item}")
    entries = report.get("proposed_registry_entries", [])
    if entries:
        lines.append("")
        lines.append(f"Proposed registry entries: {len(entries)}")
        preview = entries[:3]
        for entry in preview:
            lines.append(
                yaml.safe_dump(entry, sort_keys=False, allow_unicode=False).rstrip()
            )
        if len(entries) > len(preview):
            lines.append(f"... {len(entries) - len(preview)} additional entries omitted")
    notice_block = report.get("proposed_notice_block")
    if notice_block:
        lines.append("")
        lines.append("Proposed notice block:")
        lines.append(notice_block)
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", required=True, help="Artifact file or directory to inspect.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--kind", default="auto", help="One of auto, skill, agent, mcp, hook, other.")
    parser.add_argument("--origin", default="", help="native, third_party, or adapted.")
    parser.add_argument("--owner", default="", help="Override registry owner.")
    parser.add_argument("--license", default="", help="Override detected or default license.")
    parser.add_argument("--source-repo", default="", help="Upstream repository for external content.")
    parser.add_argument("--source-path", default="", help="Upstream source path or source root for bulk imports.")
    parser.add_argument("--modified-from-source", default="", help="true or false.")
    parser.add_argument("--id", default="", help="Override registry id for single-artifact inspections.")
    parser.add_argument("--title", default="", help="Override registry title for single-artifact inspections.")
    parser.add_argument("--description", default="", help="Required for generic MCP, hook, or other artifacts.")
    parser.add_argument("--registry", default="registry.yaml", help="Path to registry.yaml relative to repo root.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of human-readable text.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    path = Path(args.path).resolve()
    registry_path = (repo_root / args.registry).resolve()

    registry_data, sections, registry_warnings = load_registry(registry_path)
    explicit_kind = normalize_text(args.kind)
    kind = infer_kind(path) if explicit_kind in {"", "auto"} else explicit_kind
    if kind not in VALID_KINDS:
        print(f"Unsupported kind: {kind}", file=sys.stderr)
        return 2

    if kind == "skill":
        report = inspect_skill_component(path, repo_root, registry_data, sections, args)
    elif kind == "agent":
        report = inspect_agent_component(path, repo_root, sections, args)
    else:
        report = inspect_generic_component(path, kind, repo_root, registry_data, sections, args)

    report["path"] = relative_path(path, repo_root)
    report.setdefault("warnings", []).extend(registry_warnings)
    report = finalize_report(report, sections)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=False))
    else:
        print(render_human(report))
    return 1 if report.get("errors") else 0


if __name__ == "__main__":
    sys.exit(main())
