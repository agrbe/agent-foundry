#!/usr/bin/env python3
"""Inspect a skill folder and propose registry and notice updates."""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

VALID_ORIGINS = {"native", "third_party", "adapted"}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return None


def title_from_name(value: str) -> str:
    parts = [part for part in value.replace("_", "-").split("-") if part]
    return " ".join(part.capitalize() for part in parts)


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
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, f"SKILL.md frontmatter is invalid YAML: {exc}"
    if not isinstance(frontmatter, dict):
        return None, "SKILL.md frontmatter must be a YAML mapping"
    return frontmatter, None


def load_registry(path: Path) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[str]]:
    warnings: List[str] = []
    if not path.exists():
        warnings.append(f"Registry file not found: {path}")
        return {}, [], warnings
    try:
        data = load_yaml_file(path)
    except Exception as exc:  # pragma: no cover - defensive error path
        warnings.append(f"Failed to read registry: {exc}")
        return {}, [], warnings
    if not isinstance(data, dict):
        warnings.append("Registry root is not a YAML mapping")
        return {}, [], warnings
    catalog = data.get("catalog", {})
    skills = catalog.get("skills", []) if isinstance(catalog, dict) else []
    if not isinstance(skills, list):
        warnings.append("registry.yaml catalog.skills is not a list")
        skills = []
    return data, skills, warnings


def detect_origin(
    meta: Optional[Dict[str, Any]],
) -> Tuple[Optional[str], List[str], List[str]]:
    warnings: List[str] = []
    questions: List[str] = []

    if meta is None:
        questions.extend(
            [
                "Is this skill native, third_party, or adapted?",
                "What license applies to this skill?",
            ]
        )
        return None, warnings, questions

    explicit_origin = normalize_text(meta.get("origin"))
    source_repo = normalize_text(meta.get("source_repo"))
    modified = normalize_bool(meta.get("modified_from_source"))

    origin: Optional[str] = None
    if explicit_origin:
        if explicit_origin not in VALID_ORIGINS:
            warnings.append(
                "foundry.yaml declares an invalid origin. Use only native, third_party, or adapted."
            )
        else:
            origin = explicit_origin
    elif source_repo:
        if modified is None:
            questions.append(
                "Was the imported content modified from the upstream source?"
            )
        else:
            origin = "adapted" if modified else "third_party"
    else:
        origin = "native"

    if origin in {"third_party", "adapted"} and not source_repo:
        questions.append(
            "What are the source repo and source path for this external skill?"
        )
    if origin == "adapted" and modified is not True:
        warnings.append("An adapted skill should declare modified_from_source: true.")
    if origin == "third_party" and modified is True:
        warnings.append(
            "A third_party skill should not declare modified_from_source: true."
        )
    if origin == "native" and source_repo:
        warnings.append("A native skill should not declare source_repo.")

    return origin, warnings, questions


def build_registry_entry(
    skill_dir: Path,
    registry_path: Path,
    frontmatter: Dict[str, Any],
    meta: Optional[Dict[str, Any]],
    registry_data: Dict[str, Any],
    origin: Optional[str],
) -> Dict[str, Any]:
    repo = (
        registry_data.get("repo", {})
        if isinstance(registry_data.get("repo"), dict)
        else {}
    )
    repo_owner = normalize_text(repo.get("default_owner"))
    repo_license = normalize_text(repo.get("license"))

    skill_name = normalize_text(frontmatter.get("name")) or skill_dir.name
    description = normalize_text(frontmatter.get("description"))

    meta = meta or {}
    entry: Dict[str, Any] = {
        "id": normalize_text(meta.get("id")) or skill_name,
        "path": relative_path(skill_dir, registry_path.parent),
        "title": normalize_text(meta.get("title")) or title_from_name(skill_name),
        "description": description,
        "origin": origin or normalize_text(meta.get("origin")),
        "owner": normalize_text(meta.get("owner")) or repo_owner,
        "license": normalize_text(meta.get("license")),
        "source_repo": normalize_text(meta.get("source_repo")),
        "source_path": normalize_text(meta.get("source_path")),
        "modified_from_source": normalize_bool(meta.get("modified_from_source")),
        "status": normalize_text(meta.get("status")) or "draft",
    }

    if not entry["license"] and entry["origin"] == "native":
        entry["license"] = repo_license
    if entry["modified_from_source"] is None:
        entry["modified_from_source"] = entry["origin"] == "adapted"

    tags = meta.get("tags")
    if isinstance(tags, list):
        clean_tags = [normalize_text(tag) for tag in tags if normalize_text(tag)]
        if clean_tags:
            entry["tags"] = clean_tags

    return entry


def build_notice_block(entry: Dict[str, Any]) -> Optional[str]:
    if entry.get("origin") not in {"third_party", "adapted"}:
        return None

    source_repo = normalize_text(entry.get("source_repo"))
    source_path = normalize_text(entry.get("source_path"))
    license_name = normalize_text(entry.get("license"))

    if not source_repo or not license_name:
        return None

    source_text = f"`{source_repo}`"
    if source_path:
        source_text += f" (`{source_path}`)"

    modified_text = "yes" if entry.get("modified_from_source") else "no"
    return "\n".join(
        [
            f"### {entry.get('title')} (`{entry.get('id')}`)",
            f"- Path: `{entry.get('path')}`",
            f"- Origin: `{entry.get('origin')}`",
            f"- Source: {source_text}",
            f"- License: `{license_name}`",
            f"- Modified: `{modified_text}`",
            f"- Owner: `{entry.get('owner')}`",
            f"- Status: `{entry.get('status')}`",
        ]
    )


def comparable_registry_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    comparable = dict(entry)
    if "tags" in comparable and comparable["tags"] is None:
        comparable.pop("tags")
    return comparable


def inspect_skill(
    skill_dir: Path, registry_path: Path, notices_path: Path
) -> Dict[str, Any]:
    report: Dict[str, Any] = {
        "skill_dir": str(skill_dir.resolve()),
        "errors": [],
        "warnings": [],
        "questions": [],
    }

    structure = {
        "SKILL.md": (skill_dir / "SKILL.md").exists(),
        "foundry.yaml": (skill_dir / "foundry.yaml").exists(),
        "LICENSE.txt": (skill_dir / "LICENSE.txt").exists(),
        "agents/openai.yaml": (skill_dir / "agents" / "openai.yaml").exists(),
        "scripts/": (skill_dir / "scripts").is_dir(),
        "references/": (skill_dir / "references").is_dir(),
        "assets/": (skill_dir / "assets").is_dir(),
    }
    report["structure"] = structure

    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        report["errors"].append("SKILL.md is required.")
        report["status"] = "invalid"
        return report

    frontmatter, frontmatter_error = load_frontmatter(skill_md_path)
    if frontmatter_error:
        report["errors"].append(frontmatter_error)
        report["status"] = "invalid"
        return report

    meta_path = skill_dir / "foundry.yaml"
    meta: Optional[Dict[str, Any]] = None
    if meta_path.exists():
        try:
            loaded = load_yaml_file(meta_path)
        except Exception as exc:  # pragma: no cover - defensive error path
            report["errors"].append(f"Failed to read foundry.yaml: {exc}")
            report["status"] = "invalid"
            return report
        if loaded is None:
            meta = {}
        elif isinstance(loaded, dict):
            meta = loaded
        else:
            report["errors"].append("foundry.yaml must be a YAML mapping.")
            report["status"] = "invalid"
            return report
    else:
        report["warnings"].append(
            "foundry.yaml is missing; provenance will require manual confirmation."
        )

    registry_data, registry_skills, registry_warnings = load_registry(registry_path)
    report["warnings"].extend(registry_warnings)

    origin, origin_warnings, origin_questions = detect_origin(meta)
    report["warnings"].extend(origin_warnings)
    report["questions"].extend(origin_questions)

    entry = build_registry_entry(
        skill_dir, registry_path, frontmatter or {}, meta, registry_data, origin
    )
    report["proposed_registry_entry"] = entry
    report["origin"] = entry.get("origin")

    frontmatter_name = normalize_text(frontmatter.get("name"))
    if frontmatter_name and frontmatter_name != skill_dir.name:
        report["warnings"].append(
            "SKILL.md frontmatter name does not match the folder name."
        )
    if (
        normalize_text(entry.get("id"))
        and frontmatter_name
        and entry["id"] != frontmatter_name
    ):
        report["warnings"].append(
            "foundry.yaml id does not match the SKILL.md frontmatter name."
        )

    existing_by_id = None
    existing_by_path = None
    for item in registry_skills:
        if not isinstance(item, dict):
            continue
        if normalize_text(item.get("id")) == normalize_text(entry.get("id")):
            existing_by_id = item
        if normalize_text(item.get("path")) == normalize_text(entry.get("path")):
            existing_by_path = item

    matching_entry = existing_by_id or existing_by_path
    if matching_entry:
        if comparable_registry_entry(matching_entry) == comparable_registry_entry(
            entry
        ):
            report["warnings"].append(
                f"registry.yaml already contains a matching entry for `{entry.get('id')}`."
            )
            report["already_registered"] = True
        else:
            if existing_by_id:
                report["errors"].append(
                    f"registry.yaml already contains skill id `{entry.get('id')}`."
                )
                report["existing_registry_entry_by_id"] = existing_by_id
            if existing_by_path and existing_by_path is not existing_by_id:
                report["errors"].append(
                    f"registry.yaml already contains path `{entry.get('path')}`."
                )
                report["existing_registry_entry_by_path"] = existing_by_path

    if entry.get("origin") in {"third_party", "adapted"}:
        if not normalize_text(entry.get("license")):
            report["questions"].append(
                "What upstream license applies to this external skill?"
            )
        if not structure["LICENSE.txt"]:
            report["errors"].append("External skills must include a local LICENSE.txt.")

    report["notices_path"] = str(notices_path.resolve())
    report["proposed_notice_block"] = build_notice_block(entry)
    if report["errors"] or report["questions"]:
        report["status"] = "needs_input"
    elif report.get("already_registered"):
        report["status"] = "already_registered"
    else:
        report["status"] = "ready_to_apply"
    return report


def render_human(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append(f"Skill: {report['skill_dir']}")
    lines.append(f"Status: {report.get('status', 'unknown')}")
    lines.append("")
    lines.append("Structure:")
    for key, value in report.get("structure", {}).items():
        marker = "present" if value else "missing"
        lines.append(f"- {key}: {marker}")

    origin = report.get("origin") or "unknown"
    lines.append("")
    lines.append(f"Origin: {origin}")

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

    lines.append("")
    lines.append("Proposed registry entry:")
    lines.append(
        yaml.safe_dump(
            report.get("proposed_registry_entry", {}),
            sort_keys=False,
            allow_unicode=False,
        ).rstrip()
    )

    notice_block = report.get("proposed_notice_block")
    if notice_block:
        lines.append("")
        lines.append("Proposed notice block:")
        lines.append(notice_block)

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skill-dir", required=True, help="Path to the skill directory to inspect."
    )
    parser.add_argument(
        "--registry",
        default="registry.yaml",
        help="Path to registry.yaml. Defaults to ./registry.yaml.",
    )
    parser.add_argument(
        "--third-party-notices",
        default="third_party/THIRD_PARTY_NOTICES.md",
        help="Path to THIRD_PARTY_NOTICES.md.",
    )
    parser.add_argument(
        "--json", action="store_true", help="Print JSON instead of human-readable text."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = inspect_skill(
        skill_dir=Path(args.skill_dir),
        registry_path=Path(args.registry),
        notices_path=Path(args.third_party_notices),
    )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=False))
    else:
        print(render_human(report))
    return 1 if report.get("errors") else 0


if __name__ == "__main__":
    sys.exit(main())
