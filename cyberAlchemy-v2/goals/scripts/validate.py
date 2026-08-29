#!/usr/bin/env python3
"""Validate the private CyberAlchemy v2 Goal package and append a receipt."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
PROJECT_PATH = "projects/pythonconstraint-whole/project.json"
GOAL_PATH = "projects/pythonconstraint-whole/goals/pythonconstraint-whole.goal.json"
MATERIAL_FILES = (
    "README.md",
    "GOAL-DOCUMENT-TYPE.md",
    "profile.json",
    "sources.json",
    PROJECT_PATH,
    GOAL_PATH,
    "ontology/goal-view.json",
    "schemas/goal-package.schema.json",
    "scripts/validate.py",
)


def load(relative_path: str, errors: list[str]) -> dict[str, Any]:
    path = PACKAGE_ROOT / relative_path
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load {relative_path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{relative_path} must contain one JSON object")
        return {}
    return value


def load_repository_json(relative_path: str, errors: list[str]) -> dict[str, Any]:
    path = REPOSITORY_ROOT / relative_path
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load repository record {relative_path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"repository record {relative_path} must contain one JSON object")
        return {}
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_keys(value: dict[str, Any], expected: set[str], label: str, errors: list[str]) -> None:
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing:
        errors.append(f"{label} missing keys: {', '.join(missing)}")
    if extra:
        errors.append(f"{label} unknown keys: {', '.join(extra)}")


def material_digest(errors: list[str]) -> str:
    digest = hashlib.sha256()
    for relative_path in sorted(MATERIAL_FILES):
        path = PACKAGE_ROOT / relative_path
        if not path.is_file():
            errors.append(f"missing material file: {relative_path}")
            continue
        digest.update(relative_path.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def main() -> int:
    errors: list[str] = []
    profile = load("profile.json", errors)
    sources_doc = load("sources.json", errors)
    project = load(PROJECT_PATH, errors)
    goal = load(GOAL_PATH, errors)
    view = load("ontology/goal-view.json", errors)
    schema = load("schemas/goal-package.schema.json", errors)
    research = load_repository_json(
        "cyberAlchemy-v2/research/projects/pythonconstraint-whole/research/pythonconstraint-admission/research.record.json",
        errors,
    )
    experiment = load_repository_json(
        "cyberAlchemy-v2/experiments/projects/pythonconstraint-whole/experiments/pythonconstraint-whole/experiment.record.json",
        errors,
    )

    exact_keys(profile, {
        "schema_ref", "schema_version", "package_id", "package_root", "package_owner",
        "definition_owner", "ontology_owner", "visibility", "status", "authority_effect",
        "canonical_goal_kind", "materialization", "source_registry", "ontology_view",
        "schema_path", "validator_path", "blocked_effects"
    }, "profile", errors)
    if profile.get("package_root") != "cyberAlchemy-v2/goals":
        errors.append("profile package_root is not canonical")
    if profile.get("visibility") != "private" or profile.get("authority_effect") != "none":
        errors.append("profile must remain private with authority_effect none")
    if "$defs" not in schema or not {"profile", "sourceRegistry", "project", "goal", "ontologyView"}.issubset(schema.get("$defs", {})):
        errors.append("schema is missing required definitions")

    source_ids: set[str] = set()
    for index, source in enumerate(sources_doc.get("sources", [])):
        label = f"sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{label} must be an object")
            continue
        exact_keys(source, {"id", "path", "sha256", "posture", "owner_route"}, label, errors)
        source_id = source.get("id")
        if source_id in source_ids:
            errors.append(f"duplicate source id: {source_id}")
        if isinstance(source_id, str):
            source_ids.add(source_id)
        path = REPOSITORY_ROOT / str(source.get("path", ""))
        if not path.is_file():
            errors.append(f"missing source path: {source.get('path')}")
        elif sha256(path) != source.get("sha256"):
            errors.append(f"source digest drift: {source.get('id')}")

    project_keys = {"schema_ref", "schema_version", "project_id", "name", "purpose", "scope", "exclusions", "owner_routes", "goal_refs", "research_refs", "experiment_refs", "evidence_index", "thesis_refs", "lifecycle_state", "challenge_route", "authority_effect"}
    goal_keys = {"schema_ref", "schema_version", "canonical_kind", "goal_id", "title", "project_ref", "outcome", "rationale", "thesis_refs", "scope", "exclusions", "owner_route", "success_conditions", "evidence_requirements", "evidence_refs", "lifecycle_state", "achievement_state", "current_condition", "target_horizon", "revision_history", "challenge_route", "blocked_effects", "authority_effect"}
    exact_keys(project, project_keys, "project", errors)
    exact_keys(goal, goal_keys, "goal", errors)
    if project.get("schema_version") != "cav2-project/v1":
        errors.append("project schema_version is invalid")
    if goal.get("schema_version") != "cav2-goal/v1" or goal.get("canonical_kind") != "goal":
        errors.append("goal kind or schema_version is invalid")
    if not GOAL_PATH.endswith(".goal.json"):
        errors.append("goal carrier must end in .goal.json")
    if goal.get("project_ref") != project.get("project_id"):
        errors.append("goal project_ref does not resolve to the project")
    if goal.get("goal_id") not in project.get("goal_refs", []):
        errors.append("project goal_refs does not include the goal")
    if "CA2-RESEARCH-PYTHONCONSTRAINT-ADMISSION" not in project.get("research_refs", []):
        errors.append("project research_refs does not include the canonical research record")
    if "CA2-EXPERIMENT-PYTHONCONSTRAINT-WHOLE" not in project.get("experiment_refs", []):
        errors.append("project experiment_refs does not include the canonical experiment record")
    if research.get("research_id") not in project.get("research_refs", []):
        errors.append("canonical Research record does not close against project research_refs")
    if research.get("project_ref") != project.get("project_id") or goal.get("goal_id") not in research.get("goal_refs", []):
        errors.append("canonical Research record does not link back to the Project and Goal")
    if experiment.get("experiment_id") not in project.get("experiment_refs", []):
        errors.append("canonical Experiment record does not close against project experiment_refs")
    if experiment.get("project_ref") != project.get("project_id") or goal.get("goal_id") not in experiment.get("goal_refs", []):
        errors.append("canonical Experiment record does not link back to the Project and Goal")
    if project.get("authority_effect") != "none" or goal.get("authority_effect") != "none":
        errors.append("project and goal authority_effect must be none")

    evidence_ids = {item.get("evidence_id") for item in project.get("evidence_index", []) if isinstance(item, dict)}
    condition_ids: set[str] = set()
    all_met = True
    for index, condition in enumerate(goal.get("success_conditions", [])):
        if not isinstance(condition, dict) or set(condition) != {"id", "statement", "evidence_requirement", "status", "evidence_refs"}:
            errors.append(f"success_conditions[{index}] has an invalid shape")
            continue
        condition_id = condition.get("id")
        if condition_id in condition_ids:
            errors.append(f"duplicate success condition: {condition_id}")
        if isinstance(condition_id, str):
            condition_ids.add(condition_id)
        if condition.get("status") not in {"unmet", "partial", "met"}:
            errors.append(f"success condition {condition_id} has invalid status")
        if condition.get("status") != "met":
            all_met = False
        for ref in condition.get("evidence_refs", []):
            if ref not in evidence_ids:
                errors.append(f"success condition {condition_id} has unknown evidence {ref}")
    if goal.get("lifecycle_state") == "achieved" and (not all_met or goal.get("achievement_state") != "proved"):
        errors.append("an achieved goal requires every condition met and achievement_state proved")
    if goal.get("lifecycle_state") != "achieved" and goal.get("achievement_state") == "proved":
        errors.append("achievement_state proved requires lifecycle_state achieved")

    for item in goal.get("evidence_refs", []):
        if item.get("evidence_id") not in evidence_ids:
            errors.append(f"goal has unknown project evidence {item.get('evidence_id')}")
        for condition_ref in item.get("supports_conditions", []):
            if condition_ref not in condition_ids:
                errors.append(f"evidence points to unknown condition {condition_ref}")
        if item.get("source_id") not in source_ids:
            errors.append(f"goal evidence uses unknown source {item.get('source_id')}")

    thesis_node_ids = {ref.get("ontology_node_id") for ref in goal.get("thesis_refs", []) if isinstance(ref, dict)}
    if "CA2-THESIS-GOVERNED-HMI" not in thesis_node_ids:
        errors.append("goal must trace to the CyberAlchemy product thesis node")

    nodes = view.get("nodes", [])
    node_ids = {node.get("id") for node in nodes if isinstance(node, dict)}
    relation_types = {item.get("id") for item in view.get("relation_vocabulary", []) if isinstance(item, dict)}
    for relation in view.get("relations", []):
        if relation.get("source") not in node_ids or relation.get("target") not in node_ids:
            errors.append(f"ontology relation has unknown endpoint: {relation.get('id')}")
        if relation.get("type") not in relation_types:
            errors.append(f"ontology relation has unknown type: {relation.get('id')}")
    for required in {project.get("project_id"), goal.get("goal_id"), "CAV2-D59", "CAV2-D60", "CA2-THESIS-GOVERNED-HMI"}:
        if required not in node_ids:
            errors.append(f"ontology view is missing required node: {required}")

    digest = material_digest(errors)
    status = "PASS" if not errors else "BLOCK"
    receipt = {
        "schema_version": "cav2-goal-package-validation/v1",
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "package_root": "cyberAlchemy-v2/goals",
        "material_digest": digest,
        "counts": {"sources": len(source_ids), "projects": 1, "goals": 1, "success_conditions": len(condition_ids), "ontology_nodes": len(node_ids), "ontology_relations": len(view.get("relations", []))},
        "authority_effect": "none",
        "errors": errors,
    }
    receipts = PACKAGE_ROOT / "receipts"
    receipts.mkdir(exist_ok=True)
    receipt_path = receipts / f"validation-{digest[:16]}.json"
    if not receipt_path.exists():
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
