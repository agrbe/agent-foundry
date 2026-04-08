#!/usr/bin/env python3
"""Validate multi-agent router metadata against the repository catalog."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

import yaml

VALID_EXECUTION_TYPES = {"read_only", "write_capable"}
VALID_BUILT_INS = {"default", "explorer", "worker"}


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def build_report(router_path: Path, registry_path: Path) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []

    if not router_path.exists():
        return {"errors": [f"Router file not found: {router_path}"], "warnings": [], "stats": {}}
    if not registry_path.exists():
        return {"errors": [f"Registry file not found: {registry_path}"], "warnings": [], "stats": {}}

    try:
        router = load_yaml(router_path)
    except Exception as exc:
        return {"errors": [f"Failed to read router file: {exc}"], "warnings": [], "stats": {}}
    try:
        registry = load_yaml(registry_path)
    except Exception as exc:
        return {"errors": [f"Failed to read registry file: {exc}"], "warnings": [], "stats": {}}

    if not isinstance(router, dict):
        return {"errors": ["router.yaml root must be a mapping"], "warnings": [], "stats": {}}
    if not isinstance(registry, dict):
        return {"errors": ["registry.yaml root must be a mapping"], "warnings": [], "stats": {}}

    policies = router.get("policies")
    if not isinstance(policies, dict):
        errors.append("router.yaml must contain a policies mapping.")
        policies = {}

    decision_model = router.get("decision_model")
    if not isinstance(decision_model, dict):
        errors.append("router.yaml must contain a decision_model mapping.")
        decision_model = {}

    work_modes = router.get("work_modes")
    if not isinstance(work_modes, dict) or not work_modes:
        errors.append("router.yaml must contain a non-empty work_modes mapping.")
        work_modes = {}

    domains = router.get("domains")
    if not isinstance(domains, dict) or not domains:
        errors.append("router.yaml must contain a non-empty domains mapping.")
        domains = {}

    built_in_roles = router.get("built_in_roles")
    if not isinstance(built_in_roles, dict):
        errors.append("router.yaml must contain a built_in_roles mapping.")
        built_in_roles = {}

    route_groups = router.get("route_groups")
    if not isinstance(route_groups, dict):
        errors.append("router.yaml must contain a route_groups mapping.")
        route_groups = {}

    agent_routes = router.get("agent_routes")
    if not isinstance(agent_routes, dict) or not agent_routes:
        errors.append("router.yaml must contain a non-empty agent_routes mapping.")
        agent_routes = {}

    examples = router.get("decision_examples")
    if not isinstance(examples, list):
        errors.append("router.yaml decision_examples must be a list.")
        examples = []

    catalog = registry.get("catalog", {})
    if not isinstance(catalog, dict):
        errors.append("registry.yaml catalog must be a mapping.")
        catalog = {}

    registry_agents = catalog.get("agents", [])
    if not isinstance(registry_agents, list):
        errors.append("registry.yaml catalog.agents must be a list.")
        registry_agents = []

    registry_agent_ids: Set[str] = set()
    for entry in registry_agents:
        if isinstance(entry, dict) and entry.get("id"):
            registry_agent_ids.add(str(entry["id"]).strip())

    visible_modes = decision_model.get("modes", {})
    if not isinstance(visible_modes, dict) or not visible_modes:
        errors.append("decision_model.modes must be a non-empty mapping.")
        visible_modes = {}
    mode_ids = set(visible_modes.keys())

    canonical_skill_raw = str(policies.get("canonical_skill", "")).strip()
    prompt_summary_raw = str(policies.get("prompt_summary", "")).strip()
    if not canonical_skill_raw:
        errors.append("policies.canonical_skill is required.")
    else:
        canonical_skill = Path(canonical_skill_raw)
        if not (repo_root_from_script() / canonical_skill).exists():
            errors.append(f"Canonical skill path does not exist: {canonical_skill}")
    if not prompt_summary_raw:
        errors.append("policies.prompt_summary is required.")
    else:
        prompt_summary = Path(prompt_summary_raw)
        if not (repo_root_from_script() / prompt_summary).exists():
            errors.append(f"Prompt summary path does not exist: {prompt_summary}")

    built_in_ids = set(built_in_roles.keys())
    missing_built_ins = VALID_BUILT_INS - built_in_ids
    extra_built_ins = built_in_ids - VALID_BUILT_INS
    if missing_built_ins:
        errors.append(f"Missing built-in roles: {sorted(missing_built_ins)}")
    if extra_built_ins:
        errors.append(f"Unknown built-in roles: {sorted(extra_built_ins)}")

    known_route_targets = registry_agent_ids | built_in_ids
    grouped_agents: Set[str] = set()
    for group_name, members in route_groups.items():
        if not isinstance(members, list) or not members:
            errors.append(f"route_groups.{group_name} must be a non-empty list.")
            continue
        for member in members:
            member_id = str(member).strip()
            grouped_agents.add(member_id)
            if member_id not in agent_routes:
                errors.append(
                    f"route_groups.{group_name} references {member_id}, but no agent_routes entry exists."
                )

    for role_id, config in built_in_roles.items():
        if not isinstance(config, dict):
            errors.append(f"built_in_roles.{role_id} must be a mapping.")
            continue
        execution_type = str(config.get("execution_type", "")).strip()
        if execution_type not in VALID_EXECUTION_TYPES:
            errors.append(
                f"built_in_roles.{role_id}.execution_type must be one of {sorted(VALID_EXECUTION_TYPES)}."
            )

    routed_agents: Set[str] = set()
    for agent_id, config in agent_routes.items():
        routed_agents.add(agent_id)
        if agent_id not in registry_agent_ids:
            errors.append(f"agent_routes.{agent_id} is not present in registry.yaml catalog.agents.")
        if not isinstance(config, dict):
            errors.append(f"agent_routes.{agent_id} must be a mapping.")
            continue

        execution_type = str(config.get("execution_type", "")).strip()
        if execution_type not in VALID_EXECUTION_TYPES:
            errors.append(
                f"agent_routes.{agent_id}.execution_type must be one of {sorted(VALID_EXECUTION_TYPES)}."
            )

        for key in ("work_modes", "domains", "preferred_for", "avoid_for", "pair_with"):
            values = normalize_list(config.get(key))
            if key in {"work_modes", "domains"} and not values:
                errors.append(f"agent_routes.{agent_id}.{key} must be a non-empty list.")
            if key == "work_modes":
                unknown = sorted(set(values) - set(work_modes.keys()))
                if unknown:
                    errors.append(f"agent_routes.{agent_id}.work_modes contains unknown values: {unknown}")
            elif key == "domains":
                unknown = sorted(set(values) - set(domains.keys()))
                if unknown:
                    errors.append(f"agent_routes.{agent_id}.domains contains unknown values: {unknown}")
            elif key == "pair_with":
                unknown = sorted(set(values) - known_route_targets)
                if unknown:
                    errors.append(f"agent_routes.{agent_id}.pair_with contains unknown ids: {unknown}")

        fallback_priority = config.get("fallback_priority")
        if not isinstance(fallback_priority, int):
            errors.append(f"agent_routes.{agent_id}.fallback_priority must be an integer.")

    unrouted_registry_agents = sorted(registry_agent_ids - routed_agents)
    if unrouted_registry_agents:
        warnings.append(
            f"{len(unrouted_registry_agents)} registry agents do not have curated routes yet."
        )

    for example in examples:
        if not isinstance(example, dict):
            errors.append("Each decision example must be a mapping.")
            continue
        example_id = str(example.get("id", "<unknown>")).strip()
        mode = str(example.get("expected_mode", "")).strip()
        if mode not in mode_ids:
            errors.append(f"decision_examples.{example_id}.expected_mode is invalid: {mode}")
        work_mode = str(example.get("work_mode", "")).strip()
        if work_mode not in work_modes:
            errors.append(f"decision_examples.{example_id}.work_mode is invalid: {work_mode}")
        domain = str(example.get("domain", "")).strip()
        if domain not in domains:
            errors.append(f"decision_examples.{example_id}.domain is invalid: {domain}")
        for agent_id in normalize_list(example.get("recommended_agents")):
            if agent_id not in known_route_targets:
                errors.append(
                    f"decision_examples.{example_id}.recommended_agents contains unknown id: {agent_id}"
                )

    report = {
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "registry_agent_count": len(registry_agent_ids),
            "curated_route_count": len(routed_agents),
            "route_group_count": len(route_groups),
            "built_in_role_count": len(built_in_roles),
            "decision_example_count": len(examples),
        },
        "unrouted_registry_agents": unrouted_registry_agents,
    }
    return report


def print_human(report: Dict[str, Any]) -> None:
    errors = report.get("errors", [])
    warnings = report.get("warnings", [])
    stats = report.get("stats", {})

    print("Multi-Agent Router Validation")
    print(f"- Registry agents: {stats.get('registry_agent_count', 0)}")
    print(f"- Curated routes: {stats.get('curated_route_count', 0)}")
    print(f"- Route groups: {stats.get('route_group_count', 0)}")
    print(f"- Built-in roles: {stats.get('built_in_role_count', 0)}")
    print(f"- Decision examples: {stats.get('decision_example_count', 0)}")

    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")

    unrouted = report.get("unrouted_registry_agents", [])
    if unrouted:
        preview = ", ".join(unrouted[:20])
        suffix = "" if len(unrouted) <= 20 else ", ..."
        print(f"\nUnrouted registry agents ({len(unrouted)}): {preview}{suffix}")


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    repo_root = repo_root_from_script()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--router",
        default=str(repo_root / "skills/multi-agent-router/router.yaml"),
        help="Path to router.yaml.",
    )
    parser.add_argument(
        "--registry",
        default=str(repo_root / "registry.yaml"),
        help="Path to registry.yaml.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of the human summary.",
    )
    parser.add_argument(
        "--fail-on-unrouted",
        action="store_true",
        help="Treat unrouted registry agents as an error.",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    report = build_report(Path(args.router), Path(args.registry))
    if args.fail_on_unrouted and report.get("unrouted_registry_agents"):
        report.setdefault("errors", []).append("Unrouted registry agents are present.")

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)

    return 1 if report.get("errors") else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
