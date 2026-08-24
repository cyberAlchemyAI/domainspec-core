#!/usr/bin/env python3
"""Closed-world validator for the Lucifer's Lights candidate ontology."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
ONTOLOGY_DIR = SCRIPT_PATH.parent.parent
PROJECT_DIR = ONTOLOGY_DIR.parent
REPO_ROOT = ONTOLOGY_DIR.parents[2]


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_ref(raw: str) -> Path:
    prefix = "[repo-root] "
    if raw.startswith(prefix):
        return REPO_ROOT / raw[len(prefix) :]
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    return ONTOLOGY_DIR / candidate


def add_error(errors: list[dict[str, str]], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    repeated: set[str] = set()
    for value in values:
        if value in seen:
            repeated.add(value)
        seen.add(value)
    return repeated


def cycle_exists(edges: list[dict[str, Any]], predicate: str) -> bool:
    adjacency: dict[str, list[str]] = {}
    for row in edges:
        if row.get("predicate") == predicate:
            adjacency.setdefault(row["source_id"], []).append(row["target_id"])

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> bool:
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        for target_id in adjacency.get(node_id, []):
            if visit(target_id):
                return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    return any(visit(node_id) for node_id in adjacency)


def validate_profile(
    profile: dict[str, Any], ontology: dict[str, Any], errors: list[dict[str, str]]
) -> None:
    required = {
        "runtime_profile_version",
        "profile_id",
        "profile_status",
        "repository",
        "owner_route",
        "ontology_type_selection",
        "source_boundary",
        "runtime_modes",
        "runtime_outputs",
        "owner_gates",
        "residue_and_observability",
        "authority_ceiling",
    }
    for field in sorted(required - set(profile)):
        add_error(errors, "PROFILE_REQUIRED_FIELD_MISSING", field)

    selection = profile.get("ontology_type_selection", {})
    if selection.get("ontology_type") != ontology.get("ontology_type"):
        add_error(errors, "PROFILE_TYPE_MISMATCH", "profile and ontology type differ")
    if selection.get("ontology_type_alias") != ontology.get("ontology_type_alias"):
        add_error(errors, "PROFILE_ALIAS_MISMATCH", "profile and ontology alias differ")

    catalog_path = REPO_ROOT / ".agents/skills/ontology-vault/catalogs/ontology-types.json"
    catalog = load_json(catalog_path)
    catalog_ids = {row["ontology_type_id"] for row in catalog.get("types", [])}
    if selection.get("ontology_type") not in catalog_ids:
        add_error(errors, "UNKNOWN_ONTOLOGY_TYPE", str(selection.get("ontology_type")))

    boundary = profile.get("source_boundary", {})
    for field in (
        "base_ontology_refs",
        "local_ontology_refs",
        "local_owner_refs",
        "source_spine_refs",
        "implementation_runtime_refs",
        "allowed_use",
        "blocked_use",
    ):
        if field not in boundary:
            add_error(errors, "PROFILE_SOURCE_BOUNDARY_MISSING", field)
    for field in (
        "base_ontology_refs",
        "local_ontology_refs",
        "local_owner_refs",
        "source_spine_refs",
        "implementation_runtime_refs",
    ):
        for raw in boundary.get(field, []):
            if not resolve_ref(raw).exists():
                add_error(errors, "PROFILE_REF_MISSING", f"{field}: {raw}")

    modes = profile.get("runtime_modes", {})
    if modes.get("default") not in modes.get("allowed", []):
        add_error(errors, "PROFILE_DEFAULT_RUNTIME_NOT_ALLOWED", str(modes.get("default")))
    if "agents" in modes.get("allowed", []) and modes.get("agent_backend") == "blocked":
        add_error(errors, "PROFILE_AGENT_MODE_CONTRADICTION", "agents allowed while backend blocked")

    outputs = profile.get("runtime_outputs", {})
    required_blocked = {
        "promotion-verdict",
        "spec-mutation",
        "canonical-source-mutation",
        "runtime-conformance-verdict",
        "generated-projection-as-authority",
    }
    missing_blocked = required_blocked - set(outputs.get("blocked", []))
    if missing_blocked:
        add_error(
            errors,
            "PROFILE_BLOCKED_OUTPUT_MISSING",
            ", ".join(sorted(missing_blocked)),
        )
    if not outputs.get("allowed"):
        add_error(errors, "PROFILE_ALLOWED_OUTPUTS_EMPTY", "allowed outputs are required")

    for gate in profile.get("owner_gates", []):
        for field in ("gate_id", "movement", "owner_route", "required_evidence", "blocked_until"):
            if not gate.get(field):
                add_error(errors, "PROFILE_OWNER_GATE_INCOMPLETE", f"{gate.get('gate_id')}: {field}")
    if not profile.get("owner_gates"):
        add_error(errors, "PROFILE_OWNER_GATES_EMPTY", "at least one owner gate is required")

    residue = profile.get("residue_and_observability", {})
    for field in ("residue_route", "observability_route", "inventory_read_model_route"):
        if field not in residue:
            add_error(errors, "PROFILE_RESIDUE_FIELD_MISSING", field)

    ceiling = profile.get("authority_ceiling", {})
    if ceiling.get("authority_effect") != "none":
        add_error(errors, "AUTHORITY_EFFECT_ESCALATION", "profile authority_effect must be none")


def validate_ontology(
    ontology: dict[str, Any], profile: dict[str, Any]
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    if ontology.get("status") != "candidate-local":
        add_error(errors, "ONTOLOGY_STATUS_INVALID", str(ontology.get("status")))
    if ontology.get("authority_effect") != "none":
        add_error(errors, "AUTHORITY_EFFECT_ESCALATION", "ontology authority_effect must be none")
    if ontology.get("ontology_type") != "knowledge-vault":
        add_error(errors, "ONTOLOGY_TYPE_INVALID", str(ontology.get("ontology_type")))
    if ontology.get("ontology_type_alias") != "whisper-story-ontology":
        add_error(errors, "ONTOLOGY_ALIAS_INVALID", str(ontology.get("ontology_type_alias")))

    validate_profile(profile, ontology, errors)

    source_rows = ontology.get("source_registry", [])
    source_ids = [row.get("source_id", "") for row in source_rows]
    for repeated in sorted(duplicates(source_ids)):
        add_error(errors, "DUPLICATE_SOURCE_ID", repeated)
    known_sources = set(source_ids)
    live_unhashed = 0
    for row in source_rows:
        raw_path = row.get("path")
        if not raw_path:
            add_error(errors, "SOURCE_PATH_MISSING", row.get("source_id", "unknown"))
            continue
        path = resolve_ref(raw_path)
        if not path.exists():
            add_error(errors, "SOURCE_FILE_MISSING", f"{row.get('source_id')}: {path}")
            continue
        expected = row.get("sha256")
        if expected:
            actual = file_digest(path)
            if actual != expected:
                add_error(
                    errors,
                    "SOURCE_DIGEST_MISMATCH",
                    f"{row.get('source_id')}: expected {expected}, observed {actual}",
                )
        else:
            live_unhashed += 1
            if row.get("digest_policy") != "live-owner-source":
                add_error(errors, "SOURCE_DIGEST_POLICY_MISSING", row.get("source_id", "unknown"))

    vocabulary = ontology.get("vocabulary", {})
    reused_kinds = {row["kind"] for row in vocabulary.get("reused_kinds", [])}
    local_kinds = {row["kind"] for row in vocabulary.get("local_entity_kinds", [])}
    expected_local_kinds = {
        "CandidateCharacterEntity",
        "CandidatePlaceEntity",
        "CandidateEncounterEntity",
    }
    if local_kinds != expected_local_kinds:
        add_error(
            errors,
            "LOCAL_KIND_SET_CHANGED",
            f"expected {sorted(expected_local_kinds)}, observed {sorted(local_kinds)}",
        )
    allowed_kinds = reused_kinds | local_kinds
    evidence_states = set(vocabulary.get("evidence_confidence", []))
    commitment_states = set(vocabulary.get("commitment_confidence", []))
    intent_states = set(vocabulary.get("intent_states", []))
    knowledge_roles = set(vocabulary.get("knowledge_roles", []))

    node_rows = ontology.get("nodes", [])
    node_ids = [row.get("node_id", "") for row in node_rows]
    for repeated in sorted(duplicates(node_ids)):
        add_error(errors, "DUPLICATE_NODE_ID", repeated)
    nodes_by_id = {row.get("node_id"): row for row in node_rows}
    for row in node_rows:
        node_id = row.get("node_id", "unknown")
        for field in (
            "node_id",
            "kind",
            "label",
            "status",
            "owner",
            "evidence_confidence",
            "commitment_confidence",
            "intent_state",
            "evidence_refs",
            "properties",
        ):
            if field not in row:
                add_error(errors, "NODE_REQUIRED_FIELD_MISSING", f"{node_id}: {field}")
        if row.get("kind") not in allowed_kinds:
            add_error(errors, "UNKNOWN_KIND", f"{node_id}: {row.get('kind')}")
        if row.get("evidence_confidence") not in evidence_states:
            add_error(errors, "UNKNOWN_EVIDENCE_STATE", f"{node_id}: {row.get('evidence_confidence')}")
        if row.get("commitment_confidence") not in commitment_states:
            add_error(errors, "UNKNOWN_COMMITMENT_STATE", f"{node_id}: {row.get('commitment_confidence')}")
        if row.get("intent_state") not in intent_states:
            add_error(errors, "UNKNOWN_INTENT_STATE", f"{node_id}: {row.get('intent_state')}")
        for source_ref in row.get("evidence_refs", []):
            if source_ref not in known_sources:
                add_error(errors, "UNKNOWN_SOURCE_REF", f"{node_id}: {source_ref}")

    policy_rows = vocabulary.get("edge_policies", [])
    policy_by_predicate = {row.get("predicate"): row for row in policy_rows}
    if len(policy_by_predicate) != len(policy_rows):
        add_error(errors, "DUPLICATE_EDGE_POLICY", "predicate policy names must be unique")

    edge_rows = ontology.get("edges", [])
    edge_ids = [row.get("edge_id", "") for row in edge_rows]
    for repeated in sorted(duplicates(edge_ids)):
        add_error(errors, "DUPLICATE_EDGE_ID", repeated)
    for row in edge_rows:
        edge_id = row.get("edge_id", "unknown")
        source_id = row.get("source_id")
        target_id = row.get("target_id")
        predicate = row.get("predicate")
        if source_id not in nodes_by_id or target_id not in nodes_by_id:
            add_error(errors, "UNKNOWN_ENDPOINT", f"{edge_id}: {source_id} -> {target_id}")
            continue
        policy = policy_by_predicate.get(predicate)
        if not policy:
            add_error(errors, "UNKNOWN_PREDICATE", f"{edge_id}: {predicate}")
            continue
        source_kind = nodes_by_id[source_id].get("kind")
        target_kind = nodes_by_id[target_id].get("kind")
        if source_kind not in policy.get("source_kinds", []) or target_kind not in policy.get("target_kinds", []):
            add_error(
                errors,
                "INVALID_ENDPOINT_PAIR",
                f"{edge_id}: {source_kind} -{predicate}-> {target_kind}",
            )
        if row.get("policy_owner") != policy.get("owner"):
            add_error(
                errors,
                "POLICY_OWNER_MISMATCH",
                f"{edge_id}: expected {policy.get('owner')}, observed {row.get('policy_owner')}",
            )
        for source_ref in row.get("evidence_refs", []):
            if source_ref not in known_sources:
                add_error(errors, "UNKNOWN_SOURCE_REF", f"{edge_id}: {source_ref}")

    for policy in policy_rows:
        if policy.get("cycle_policy") == "forbidden" and cycle_exists(edge_rows, policy["predicate"]):
            add_error(errors, "FORBIDDEN_EDGE_CYCLE", policy["predicate"])

    record_rows = ontology.get("knowledge_records", [])
    record_ids = [row.get("record_id", "") for row in record_rows]
    for repeated in sorted(duplicates(record_ids)):
        add_error(errors, "DUPLICATE_RECORD_ID", repeated)
    for row in record_rows:
        record_id = row.get("record_id", "unknown")
        for field in (
            "record_id",
            "role",
            "statement",
            "subject_refs",
            "source_refs",
            "evidence_state",
            "commitment_state",
            "intent_state",
            "owner",
            "transport_visibility",
        ):
            if field not in row:
                add_error(errors, "RECORD_REQUIRED_FIELD_MISSING", f"{record_id}: {field}")
        if row.get("role") not in knowledge_roles:
            add_error(errors, "UNKNOWN_KNOWLEDGE_ROLE", f"{record_id}: {row.get('role')}")
        if row.get("evidence_state") not in evidence_states:
            add_error(errors, "UNKNOWN_EVIDENCE_STATE", f"{record_id}: {row.get('evidence_state')}")
        if row.get("commitment_state") not in commitment_states:
            add_error(errors, "UNKNOWN_COMMITMENT_STATE", f"{record_id}: {row.get('commitment_state')}")
        if row.get("intent_state") not in intent_states:
            add_error(errors, "UNKNOWN_INTENT_STATE", f"{record_id}: {row.get('intent_state')}")
        for node_ref in row.get("subject_refs", []):
            if node_ref not in nodes_by_id:
                add_error(errors, "UNKNOWN_SUBJECT_REF", f"{record_id}: {node_ref}")
        for source_ref in row.get("source_refs", []):
            if source_ref not in known_sources:
                add_error(errors, "UNKNOWN_SOURCE_REF", f"{record_id}: {source_ref}")
        if row.get("role") == "reserve_material" and row.get("commitment_state") != "reserve":
            add_error(errors, "RESERVE_COMMITMENT_INVALID", record_id)
        if row.get("role") == "mystery" and row.get("commitment_state") in {"author-accepted", "frozen-baseline"}:
            add_error(errors, "MYSTERY_PROMOTION_FORBIDDEN", record_id)
        if row.get("role") == "derivative_drift" and len(set(row.get("source_refs", []))) < 2:
            add_error(errors, "DRIFT_EVIDENCE_INCOMPLETE", record_id)

    chapter_gate = ontology.get("current_state", {}).get("chapter_gate")
    if chapter_gate == "pending-author-review":
        for row in [*node_rows, *record_rows]:
            commitment = row.get("commitment_confidence", row.get("commitment_state"))
            if commitment in {"author-accepted", "frozen-baseline"}:
                row_id = row.get("node_id", row.get("record_id", "unknown"))
                add_error(errors, "PREMATURE_COMMITMENT_PROMOTION", row_id)

    mentioned_targets = {
        row["target_id"] for row in edge_rows if row.get("predicate") == "mentions"
    }
    for row in node_rows:
        if row.get("kind") in local_kinds and row.get("node_id") not in mentioned_targets:
            add_error(errors, "LOCAL_NODE_NOT_MENTIONED", row.get("node_id", "unknown"))

    participating_encounters = {
        row["target_id"] for row in edge_rows if row.get("predicate") == "participates_in"
    }
    located_encounters = {
        row["source_id"] for row in edge_rows if row.get("predicate") == "occurs_at"
    }
    for row in node_rows:
        if row.get("kind") == "CandidateEncounterEntity":
            if row.get("node_id") not in participating_encounters:
                add_error(errors, "ENCOUNTER_WITHOUT_PARTICIPANT", row.get("node_id", "unknown"))
            if row.get("node_id") not in located_encounters:
                add_error(errors, "ENCOUNTER_WITHOUT_PLACE", row.get("node_id", "unknown"))

    result = "policy-pass" if not errors else "policy-fail"
    return {
        "result": result,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "sources": len(source_rows),
            "live_unhashed_sources": live_unhashed,
            "nodes": len(node_rows),
            "edges": len(edge_rows),
            "knowledge_records": len(record_rows),
            "edge_policies": len(policy_rows),
        },
    }


def apply_mutation(ontology: dict[str, Any], fixture: dict[str, Any]) -> None:
    mutation = fixture["mutation"]
    operation = mutation["op"]
    if operation == "append_node":
        ontology["nodes"].append(mutation["value"])
    elif operation == "append_edge":
        ontology["edges"].append(mutation["value"])
    elif operation == "append_record":
        ontology["knowledge_records"].append(mutation["value"])
    elif operation == "replace_edge_policy_owner":
        edge_id = mutation["edge_id"]
        for row in ontology["edges"]:
            if row["edge_id"] == edge_id:
                row["policy_owner"] = mutation["value"]
                return
        raise ValueError(f"fixture edge not found: {edge_id}")
    else:
        raise ValueError(f"unsupported fixture mutation: {operation}")


def run_self_test(
    ontology: dict[str, Any], profile: dict[str, Any], fixture_path: Path
) -> dict[str, Any]:
    fixture_doc = load_json(fixture_path)
    results: list[dict[str, Any]] = []
    failures: list[str] = []
    for fixture in fixture_doc.get("fixtures", []):
        candidate = copy.deepcopy(ontology)
        apply_mutation(candidate, fixture)
        result = validate_ontology(candidate, profile)
        codes = {row["code"] for row in result["errors"]}
        passed = (
            result["result"] == fixture.get("expected_result")
            and fixture.get("expected_error") in codes
        )
        results.append(
            {
                "fixture_id": fixture["fixture_id"],
                "observed_result": result["result"],
                "expected_error": fixture.get("expected_error"),
                "observed_errors": sorted(codes),
                "pass": passed,
            }
        )
        if not passed:
            failures.append(fixture["fixture_id"])
    return {
        "result": "pass" if not failures else "fail",
        "fixtures": results,
        "failures": failures,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ontology",
        type=Path,
        default=ONTOLOGY_DIR / "whisper-story-ontology.json",
    )
    parser.add_argument(
        "--profile",
        type=Path,
        default=ONTOLOGY_DIR / "runtime-profile.json",
    )
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=ONTOLOGY_DIR / "fixtures/closed-world-negatives.json",
    )
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ontology = load_json(args.ontology.resolve())
    profile = load_json(args.profile.resolve())
    baseline = validate_ontology(ontology, profile)
    self_test = (
        run_self_test(ontology, profile, args.fixtures.resolve())
        if args.self_test
        else {"result": "not-run", "fixtures": [], "failures": []}
    )
    receipt = {
        "validator_contract": "lucifers-lights-whisper-story-validator/v1",
        "ontology_id": ontology.get("ontology_id"),
        "ontology_version": ontology.get("version"),
        "ontology_type": ontology.get("ontology_type"),
        "ontology_type_alias": ontology.get("ontology_type_alias"),
        "runtime_mode": profile.get("runtime_modes", {}).get("default"),
        "result": baseline["result"],
        "authority_effect": "none",
        "ontology_sha256": file_digest(args.ontology.resolve()),
        "profile_sha256": file_digest(args.profile.resolve()),
        "policy_sha256": canonical_digest(ontology.get("vocabulary", {}).get("edge_policies", [])),
        "counts": baseline["counts"],
        "errors": baseline["errors"],
        "warnings": baseline["warnings"],
        "negative_self_test": self_test,
        "human_gate": "pending",
        "maximum_claim": "mechanically validated candidate-local authoring ontology",
    }
    print(json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True))
    if baseline["result"] != "policy-pass" or self_test["result"] == "fail":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
