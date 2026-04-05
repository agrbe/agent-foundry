#!/usr/bin/env python3
"""Generate or update foundry.yaml for a skill folder."""

import argparse
import re
import sys
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

VALID_ORIGINS = {"native", "third_party", "adapted"}
INITIALISMS = {
    "ai": "AI",
    "api": "API",
    "claude": "Claude",
    "codex": "Codex",
    "docx": "DOCX",
    "github": "GitHub",
    "git": "Git",
    "mcp": "MCP",
    "openai": "OpenAI",
    "pdf": "PDF",
    "yaml": "YAML",
}


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


def normalize_string_list(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []
    items: List[str] = []
    for item in value:
        text = normalize_text(item)
        if text and text not in items:
            items.append(text)
    return items


def title_from_name(value: str) -> str:
    parts = [part for part in value.replace("_", "-").split("-") if part]
    titled_parts = [INITIALISMS.get(part.lower(), part.capitalize()) for part in parts]
    return " ".join(titled_parts)


def load_yaml_file(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_frontmatter(path: Path) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        return None, "SKILL.md is missing valid YAML frontmatter."
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, f"SKILL.md frontmatter is invalid YAML: {exc}"
    if not isinstance(frontmatter, dict):
        return None, "SKILL.md frontmatter must be a YAML mapping."
    return frontmatter, None


def load_existing_metadata(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    loaded = load_yaml_file(path)
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise ValueError("foundry.yaml must be a YAML mapping.")
    return loaded


def load_registry_defaults(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {"owner": "", "license": ""}
    loaded = load_yaml_file(path)
    if not isinstance(loaded, dict):
        return {"owner": "", "license": ""}
    repo = loaded.get("repo")
    if not isinstance(repo, dict):
        return {"owner": "", "license": ""}
    return {
        "owner": normalize_text(repo.get("default_owner")),
        "license": normalize_text(repo.get("license")),
    }


def merge_dicts(base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
    result = deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def infer_paths(skill_dir: Path, existing_meta: Dict[str, Any]) -> Dict[str, str]:
    existing_paths = existing_meta.get("paths", {})
    if not isinstance(existing_paths, dict):
        existing_paths = {}

    def prefer(existing_key: str, detected: str) -> str:
        return normalize_text(existing_paths.get(existing_key)) or detected

    return {
        "skill_file": prefer("skill_file", "SKILL.md"),
        "foundry_file": prefer("foundry_file", "foundry.yaml"),
        "license_file": prefer(
            "license_file", "LICENSE.txt" if (skill_dir / "LICENSE.txt").exists() else ""
        ),
        "openai_metadata_file": prefer(
            "openai_metadata_file",
            "agents/openai.yaml" if (skill_dir / "agents" / "openai.yaml").exists() else "",
        ),
        "scripts_dir": prefer("scripts_dir", "scripts" if (skill_dir / "scripts").is_dir() else ""),
        "references_dir": prefer(
            "references_dir", "references" if (skill_dir / "references").is_dir() else ""
        ),
        "assets_dir": prefer("assets_dir", "assets" if (skill_dir / "assets").is_dir() else ""),
    }


def resolve_origin(args: argparse.Namespace, existing_meta: Dict[str, Any]) -> str:
    origin = normalize_text(args.origin) or normalize_text(existing_meta.get("origin")) or "native"
    if origin not in VALID_ORIGINS:
        raise ValueError("origin must be one of: native, third_party, adapted.")
    return origin


def resolve_modified_from_source(
    args: argparse.Namespace, existing_meta: Dict[str, Any], origin: str
) -> bool:
    if args.modified_from_source is not None:
        modified = normalize_bool(args.modified_from_source)
        if modified is None:
            raise ValueError("--modified-from-source must be true or false.")
        return modified
    existing = normalize_bool(existing_meta.get("modified_from_source"))
    if existing is not None:
        return existing
    return origin == "adapted"


def resolve_tags(args: argparse.Namespace, existing_meta: Dict[str, Any]) -> List[str]:
    if args.tag:
        return normalize_string_list(args.tag)
    return normalize_string_list(existing_meta.get("tags"))


def resolve_maintainers(args: argparse.Namespace, existing_meta: Dict[str, Any]) -> List[str]:
    if args.maintainer:
        return normalize_string_list(args.maintainer)
    return normalize_string_list(existing_meta.get("maintainers"))


def resolve_notes(existing_meta: Dict[str, Any]) -> List[str]:
    return normalize_string_list(existing_meta.get("notes"))


def resolve_context(args: argparse.Namespace) -> Dict[str, Any]:
    skill_dir = Path(args.skill_dir)
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        raise ValueError(f"SKILL.md not found at {skill_md_path}")

    frontmatter, frontmatter_error = load_frontmatter(skill_md_path)
    if frontmatter_error:
        raise ValueError(frontmatter_error)

    assert frontmatter is not None
    existing_meta = load_existing_metadata(skill_dir / "foundry.yaml")
    registry_defaults = load_registry_defaults(Path(args.registry))

    skill_name = normalize_text(frontmatter.get("name")) or skill_dir.name
    origin = resolve_origin(args, existing_meta)
    modified_from_source = resolve_modified_from_source(args, existing_meta, origin)

    source_repo = normalize_text(args.source_repo) or normalize_text(existing_meta.get("source_repo"))
    source_path = normalize_text(args.source_path) or normalize_text(existing_meta.get("source_path"))
    source_url = normalize_text(args.source_url) or normalize_text(existing_meta.get("source_url"))
    source_license = normalize_text(args.source_license) or normalize_text(existing_meta.get("source_license"))

    owner = (
        normalize_text(args.owner)
        or normalize_text(existing_meta.get("owner"))
        or registry_defaults["owner"]
    )
    license_name = normalize_text(args.license_name) or normalize_text(existing_meta.get("license"))
    if not license_name and origin == "native":
        license_name = registry_defaults["license"]

    title = normalize_text(args.title) or normalize_text(existing_meta.get("title")) or title_from_name(skill_name)
    description = (
        normalize_text(args.description)
        or normalize_text(existing_meta.get("description"))
        or normalize_text(frontmatter.get("description"))
    )
    status = normalize_text(args.status) or normalize_text(existing_meta.get("status")) or "draft"
    visibility = (
        normalize_text(args.visibility)
        or normalize_text(existing_meta.get("visibility"))
        or "internal"
    )
    license_file = (
        normalize_text(existing_meta.get("license_file"))
        or ("LICENSE.txt" if (skill_dir / "LICENSE.txt").exists() else "")
    )

    if origin == "native":
        source_repo = ""
        source_path = ""
        source_url = ""
        source_license = ""
        modified_from_source = False
    else:
        if not source_repo:
            raise ValueError("source_repo is required for third_party and adapted skills.")
        if not license_name:
            raise ValueError("license is required for third_party and adapted skills.")
        if origin == "third_party" and modified_from_source:
            raise ValueError("third_party skills must use modified_from_source: false.")
        if origin == "adapted" and not modified_from_source:
            raise ValueError("adapted skills must use modified_from_source: true.")

    return {
        "skill_dir": skill_dir,
        "frontmatter": frontmatter,
        "existing_meta": existing_meta,
        "template": args.template,
        "id": normalize_text(existing_meta.get("id")) or skill_name,
        "title": title,
        "description": description,
        "origin": origin,
        "owner": owner,
        "maintainers": resolve_maintainers(args, existing_meta),
        "license": license_name,
        "license_file": license_file,
        "status": status,
        "visibility": visibility,
        "tags": resolve_tags(args, existing_meta),
        "source_repo": source_repo,
        "source_path": source_path,
        "source_url": source_url,
        "source_license": source_license,
        "modified_from_source": modified_from_source,
        "paths": infer_paths(skill_dir, existing_meta),
        "notes": resolve_notes(existing_meta),
        "description_requested": args.description is not None,
        "source_url_requested": args.source_url is not None,
        "source_license_requested": args.source_license is not None,
    }


def build_simple_metadata(context: Dict[str, Any]) -> Dict[str, Any]:
    existing_meta = context["existing_meta"]
    result: Dict[str, Any] = {
        "id": context["id"],
        "title": context["title"],
        "origin": context["origin"],
        "owner": context["owner"],
        "license": context["license"],
        "source_repo": context["source_repo"],
        "source_path": context["source_path"],
        "modified_from_source": context["modified_from_source"],
        "status": context["status"],
    }

    if context["description_requested"] or "description" in existing_meta:
        result["description"] = context["description"]
    if context["license_file"] or "license_file" in existing_meta:
        result["license_file"] = context["license_file"]
    if context["source_url_requested"] or "source_url" in existing_meta:
        result["source_url"] = context["source_url"]
    if context["source_license_requested"] or "source_license" in existing_meta:
        result["source_license"] = context["source_license"]
    if context["tags"] or "tags" in existing_meta:
        result["tags"] = context["tags"]

    for key, value in existing_meta.items():
        if key not in result:
            result[key] = deepcopy(value)
    return result


def build_full_metadata(context: Dict[str, Any]) -> Dict[str, Any]:
    today = date.today().isoformat()
    defaults: Dict[str, Any] = {
        "version": 1,
        "id": context["id"],
        "kind": "skill",
        "title": context["title"],
        "description": context["description"],
        "origin": context["origin"],
        "owner": context["owner"],
        "maintainers": context["maintainers"],
        "license": context["license"],
        "license_file": context["license_file"],
        "status": context["status"],
        "visibility": context["visibility"],
        "tags": context["tags"],
        "source_repo": context["source_repo"],
        "source_path": context["source_path"],
        "source_url": context["source_url"],
        "source_license": context["source_license"],
        "modified_from_source": context["modified_from_source"],
        "paths": context["paths"],
        "targets": {
            "codex": True,
            "claude_code": False,
        },
        "registry": {
            "register": True,
            "category": "",
            "notes": "",
        },
        "review": {
            "reviewed": False,
            "reviewed_by": "",
            "reviewed_at": "",
            "review_notes": "",
        },
        "lifecycle": {
            "created_at": today,
            "updated_at": today,
            "deprecated_at": "",
            "archived_at": "",
        },
        "notes": context["notes"],
    }

    merged = merge_dicts(defaults, context["existing_meta"])

    merged["version"] = merged.get("version", 1) or 1
    merged["id"] = context["id"]
    merged["kind"] = normalize_text(merged.get("kind")) or "skill"
    merged["title"] = context["title"]
    merged["description"] = context["description"]
    merged["origin"] = context["origin"]
    merged["owner"] = context["owner"]
    merged["maintainers"] = context["maintainers"]
    merged["license"] = context["license"]
    merged["license_file"] = context["license_file"]
    merged["status"] = context["status"]
    merged["visibility"] = context["visibility"]
    merged["tags"] = context["tags"]
    merged["source_repo"] = context["source_repo"]
    merged["source_path"] = context["source_path"]
    merged["source_url"] = context["source_url"]
    merged["source_license"] = context["source_license"]
    merged["modified_from_source"] = context["modified_from_source"]
    merged["notes"] = context["notes"]

    paths = merged.get("paths", {})
    if not isinstance(paths, dict):
        paths = {}
    paths = merge_dicts(context["paths"], paths)
    merged["paths"] = paths

    targets = merged.get("targets", {})
    if not isinstance(targets, dict):
        targets = {}
    merged["targets"] = {
        "codex": bool(targets.get("codex", True)),
        "claude_code": bool(targets.get("claude_code", False)),
    }

    registry = merged.get("registry", {})
    if not isinstance(registry, dict):
        registry = {}
    merged["registry"] = {
        "register": bool(registry.get("register", True)),
        "category": normalize_text(registry.get("category")),
        "notes": normalize_text(registry.get("notes")),
    }

    review = merged.get("review", {})
    if not isinstance(review, dict):
        review = {}
    merged["review"] = {
        "reviewed": bool(review.get("reviewed", False)),
        "reviewed_by": normalize_text(review.get("reviewed_by")),
        "reviewed_at": normalize_text(review.get("reviewed_at")),
        "review_notes": normalize_text(review.get("review_notes")),
    }

    lifecycle = merged.get("lifecycle", {})
    if not isinstance(lifecycle, dict):
        lifecycle = {}
    merged["lifecycle"] = {
        "created_at": normalize_text(lifecycle.get("created_at")) or today,
        "updated_at": today,
        "deprecated_at": normalize_text(lifecycle.get("deprecated_at")),
        "archived_at": normalize_text(lifecycle.get("archived_at")),
    }

    ordered: Dict[str, Any] = {}
    ordered_keys = [
        "version",
        "id",
        "kind",
        "title",
        "description",
        "origin",
        "owner",
        "maintainers",
        "license",
        "license_file",
        "status",
        "visibility",
        "tags",
        "source_repo",
        "source_path",
        "source_url",
        "source_license",
        "modified_from_source",
        "paths",
        "targets",
        "registry",
        "review",
        "lifecycle",
        "notes",
    ]
    for key in ordered_keys:
        ordered[key] = merged[key]
    for key, value in merged.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def render_yaml(data: Dict[str, Any]) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=False,
        default_flow_style=False,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", required=True, help="Path to the target skill directory.")
    parser.add_argument(
        "--registry",
        default="registry.yaml",
        help="Path to registry.yaml. Defaults to ./registry.yaml.",
    )
    parser.add_argument(
        "--template",
        choices=("simple", "full"),
        default="simple",
        help="Template shape to generate. Defaults to simple.",
    )
    parser.add_argument("--write", action="store_true", help="Write the result to foundry.yaml.")
    parser.add_argument("--origin", choices=tuple(sorted(VALID_ORIGINS)))
    parser.add_argument("--owner")
    parser.add_argument("--license", dest="license_name")
    parser.add_argument("--status")
    parser.add_argument("--title")
    parser.add_argument("--description")
    parser.add_argument("--source-repo")
    parser.add_argument("--source-path")
    parser.add_argument("--source-url")
    parser.add_argument("--source-license")
    parser.add_argument(
        "--modified-from-source",
        help="Explicit true/false override for modified_from_source.",
    )
    parser.add_argument("--tag", action="append", default=[], help="Repeat to add tags.")
    parser.add_argument(
        "--maintainer", action="append", default=[], help="Repeat to add maintainers."
    )
    parser.add_argument("--visibility")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        context = resolve_context(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.template == "simple":
        metadata = build_simple_metadata(context)
    else:
        metadata = build_full_metadata(context)

    rendered = render_yaml(metadata)
    output_path = Path(args.skill_dir) / "foundry.yaml"

    if args.write:
        output_path.write_text(rendered, encoding="utf-8")
        print(
            f"Wrote {output_path} using the {args.template} template for origin {context['origin']}."
        )
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
