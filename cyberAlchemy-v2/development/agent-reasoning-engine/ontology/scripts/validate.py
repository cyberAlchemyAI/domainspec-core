#!/usr/bin/env python3
"""Validate the first-class candidate Agent Reasoning Engine ontology package."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
SCHEMA_PATH = PACKAGE_ROOT / "schemas/agent-reasoning-engine-ontology.schema.json"
GENERATED_ROOT = PACKAGE_ROOT / "domainspec/generated"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def schema_errors(instance: Any, schema: dict[str, Any], ref: str, label: str) -> list[str]:
    wrapper = copy.deepcopy(schema)
    wrapper["$ref"] = ref
    return [
        f"{label}.{'.'.join(str(part) for part in error.path) or '$'}: {error.message}"
        for error in sorted(Draft202012Validator(wrapper).iter_errors(instance), key=lambda item: tuple(str(part) for part in item.path))
    ]


def heading_section_bytes(path: Path, selector: str) -> bytes:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    start = next((index for index, line in enumerate(lines) if line.rstrip("\r\n") == selector), None)
    if start is None:
        raise ValueError(f"selector not found: {selector}")
    end = next((index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")), len(lines))
    return "".join(lines[start:end]).encode()


def validate_sources(registry: dict[str, Any], errors: list[str]) -> set[str]:
    ids: list[str] = []
    for source in registry.get("sources", []):
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("id"))
        ids.append(source_id)
        path = (REPOSITORY_ROOT / str(source.get("path", ""))).resolve()
        try:
            path.relative_to(REPOSITORY_ROOT.resolve())
        except ValueError:
            errors.append(f"source escapes repository: {source_id}")
            continue
        try:
            if source.get("scope_kind") == "whole-file" and source.get("selector") is None:
                selected = path.read_bytes()
            elif source.get("scope_kind") == "heading-section" and isinstance(source.get("selector"), str):
                selected = heading_section_bytes(path, source["selector"])
            else:
                errors.append(f"source scope is invalid: {source_id}")
                continue
        except (OSError, ValueError) as exc:
            errors.append(f"source is not evaluable: {source_id}: {exc}")
            continue
        actual = sha256_bytes(selected)
        if actual != source.get("sha256"):
            errors.append(f"source digest drift: {source_id}: expected {source.get('sha256')}, got {actual}")
    if len(ids) != len(set(ids)):
        errors.append("source ids must be unique")
    required = {"CAP-SEL-CAV2-D65", "CAP-SEL-CAV2-D67", "CAP-SEL-ARE-OWNER-INTENT", "CAP-SEL-ARE-PRODUCT-CAPABILITY", "CAP-SEL-ARE-BUSINESS-ONTOLOGY"}
    if not required.issubset(set(ids)):
        errors.append(f"required D65 predecessor sources are missing: {sorted(required - set(ids))}")
    return set(ids)


def validate_business_ontology(ontology: dict[str, Any], errors: list[str]) -> set[str]:
    node_ids = [item.get("id") for item in ontology.get("nodes", []) if isinstance(item, dict)]
    if len(node_ids) != len(set(node_ids)):
        errors.append("business ontology node ids must be unique")
    relation_ids: list[str] = []
    known = set(node_ids)
    for relation in ontology.get("relations", []):
        if not isinstance(relation, dict):
            continue
        relation_ids.append(str(relation.get("id")))
        if relation.get("source") not in known or relation.get("target") not in known:
            errors.append(f"business relation endpoint does not resolve: {relation.get('id')}")
    if len(relation_ids) != len(set(relation_ids)):
        errors.append("business ontology relation ids must be unique")
    return known


def domainspec_node_ids() -> set[str]:
    feature = load_json(PACKAGE_ROOT / "domainspec/feature.json")
    result: set[str] = set()
    for relative in feature.get("node_sources", []):
        node = load_json(PACKAGE_ROOT / "domainspec" / relative)
        result.add(str(node.get("node_id")))
    return result


def validate_bridge(bridge: dict[str, Any], business_ids: set[str], source_ids: set[str], errors: list[str]) -> None:
    system_ids = domainspec_node_ids()
    implementation_sources = {
        item.get("id") for item in load_json(PACKAGE_ROOT / "sources.json").get("sources", [])
        if isinstance(item, dict) and item.get("role") == "implementation-evidence"
    }
    edge_ids: list[str] = []
    for edge in bridge.get("edges", []):
        if not isinstance(edge, dict):
            continue
        edge_ids.append(str(edge.get("id")))
        if edge.get("source") not in business_ids:
            errors.append(f"bridge business endpoint does not resolve: {edge.get('id')}")
        if edge.get("target") not in system_ids:
            errors.append(f"bridge system endpoint does not resolve: {edge.get('id')}")
        evidence = set(edge.get("evidence_refs", []))
        if not evidence.issubset(source_ids):
            errors.append(f"bridge evidence refs do not resolve: {edge.get('id')}: {sorted(evidence - source_ids)}")
        if edge.get("relation") == "realized_by" and edge.get("realization_status") != "bounded-realization":
            errors.append(f"realized_by edge lacks bounded-realization posture: {edge.get('id')}")
        if edge.get("realization_status") == "bounded-realization" and not evidence.intersection(implementation_sources):
            errors.append(f"bounded realization lacks implementation evidence: {edge.get('id')}")
    if len(edge_ids) != len(set(edge_ids)):
        errors.append("bridge edge ids must be unique")
    gap_ids: list[str] = []
    for gap in bridge.get("gaps", []):
        if not isinstance(gap, dict):
            continue
        gap_ids.append(str(gap.get("id")))
        missing_business = sorted(set(gap.get("business_refs", [])) - business_ids)
        missing_system = sorted(set(gap.get("system_refs", [])) - system_ids)
        if missing_business:
            errors.append(f"bridge gap business refs do not resolve: {gap.get('id')}: {missing_business}")
        if missing_system:
            errors.append(f"bridge gap system refs do not resolve: {gap.get('id')}: {missing_system}")
    if len(gap_ids) != len(set(gap_ids)):
        errors.append("bridge gap ids must be unique")


def validate_product_capability(record: dict[str, Any], support: dict[str, Any], business_ids: set[str], source_ids: set[str], errors: list[str]) -> None:
    shared_schema = load_json(REPOSITORY_ROOT / "cyberAlchemy-v2/capability/schemas/capability.schema.json")
    errors.extend(schema_errors(record, shared_schema, "#/$defs/productCapability", "product capability"))
    support_ids = {item.get("id") for item in support.get("records", []) if isinstance(item, dict)}
    referenced = set(record.get("input_contract_refs", [])) | set(record.get("output_contract_refs", []))
    referenced |= set(record.get("context_policy_refs", [])) | set(record.get("realization_binding_refs", []))
    referenced.add(record.get("obligation_registry_ref"))
    if not referenced.issubset(support_ids):
        errors.append(f"product capability support refs do not resolve: {sorted(referenced - support_ids)}")
    residue_ids = {item.get("id") for item in support.get("residue", []) if isinstance(item, dict)}
    residue_refs = set(record.get("lifecycle_posture", {}).get("residue_refs", []))
    if not residue_refs.issubset(residue_ids):
        errors.append(f"product capability residue refs do not resolve: {sorted(residue_refs - residue_ids)}")
    business_refs = {record.get("product_ref"), record.get("business_ontology_ref"), *record.get("outcome_refs", []), *record.get("participant_refs", []), *record.get("consumer_refs", [])}
    if not business_refs.issubset(business_ids):
        errors.append(f"product capability business refs do not resolve: {sorted(business_refs - business_ids)}")
    evidence_refs = set(record.get("evidence_refs", []))
    if not evidence_refs.issubset(source_ids):
        errors.append(f"product capability evidence refs do not resolve: {sorted(evidence_refs - source_ids)}")
    owner_refs = {ref for route in record.get("owner_routes", []) if isinstance(route, dict) for ref in route.get("source_refs", [])}
    if not owner_refs.issubset(evidence_refs):
        errors.append(f"owner routes contain unregistered capability evidence: {sorted(owner_refs - evidence_refs)}")


def validate_residue(errors: list[str]) -> int:
    ids: list[str] = []
    lines = (PACKAGE_ROOT / "residue.jsonl").read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines, start=1):
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"residue line {index} is invalid JSON: {exc}")
            continue
        ids.append(str(item.get("residue_id")))
        if item.get("authority_effect") != "none":
            errors.append(f"residue line {index} has authority effect")
    if len(ids) != len(set(ids)):
        errors.append("residue ids must be unique")
    return len(lines)


def validate_generated(errors: list[str], sources: dict[str, Any], bridge: dict[str, Any]) -> None:
    project = load_json(PACKAGE_ROOT / "domainspec/project.json")
    profile_path = PACKAGE_ROOT / "domainspec/development-profile.json"
    if project.get("language", {}).get("profile", {}).get("digest") != sha256_file(profile_path):
        errors.append("DomainSpec development profile digest drift")
    required = {"graph.json", "source-manifest.json", "SPEC.md", "markdown-view.json", "build-receipt.json", "system-ontology.json", "system-ontology-receipt.json"}
    missing = sorted(name for name in required if not (GENERATED_ROOT / name).is_file())
    if missing:
        errors.append(f"generated DomainSpec artifacts are missing: {missing}")
        return
    graph_path = GENERATED_ROOT / "graph.json"
    system_path = GENERATED_ROOT / "system-ontology.json"
    build_receipt = load_json(GENERATED_ROOT / "build-receipt.json")
    system = load_json(system_path)
    projection = load_json(GENERATED_ROOT / "system-ontology-receipt.json")
    contract = system.get("implementation_contract", {})
    if system.get("construction_inputs") != sources.get("sources"):
        errors.append("generated system ontology does not preserve exact selected sources")
    if build_receipt.get("source_set_digest") != system.get("source_set_digest"):
        errors.append("generated system ontology source-set binding drift")
    if system.get("source_graph_digest") != sha256_file(graph_path):
        errors.append("generated system ontology graph binding drift")
    if system.get("business_system_bridge", {}).get("bridge_sha256") != sha256_file(PACKAGE_ROOT / "bridge.json"):
        errors.append("generated system ontology bridge binding drift")
    if system.get("compiler", {}).get("projection_builder_sha256") != sha256_file(PACKAGE_ROOT / "scripts/build.ts"):
        errors.append("generated system ontology projection-builder binding drift")
    if contract.get("validator_sha256") != sha256_file(Path(__file__).resolve()):
        errors.append("generated system ontology validator binding drift")
    if contract.get("context_management_realization") != "bounded-semantic-integrity-completion-frontier-recoverable-reasoning-state-codex-gateway-candidate" or contract.get("whole_engine_realization") != "absent":
        errors.append("generated system ontology overclaims complete realization")
    semantic_integrity = next((item for item in contract.get("bounded_partial_realizations", []) if item.get("id") == "context-bound-semantic-integrity@1"), None)
    if not semantic_integrity:
        errors.append("generated system ontology lacks context-bound semantic integrity realization")
    elif any([
        semantic_integrity.get("cross_record_binding_verification") is not True,
        semantic_integrity.get("context_identity_receipt_binding") is not True,
        semantic_integrity.get("historical_unbound_receipt_compatibility") is not True,
        semantic_integrity.get("authority_effect") != "none",
    ]):
        errors.append("generated context-bound semantic integrity realization posture drift")
    recovery = next((item for item in contract.get("bounded_partial_realizations", []) if item.get("id") == "reasoning-state-recovery@1"), None)
    if not recovery:
        errors.append("generated system ontology lacks reasoning-state recovery realization")
    elif any([
        recovery.get("canonical_log_verification") is not True,
        recovery.get("deterministic_disposable_index_rebuild") is not True,
        recovery.get("final_checkpoint_required") is not True,
        recovery.get("source_recheck_before_hydration") is not True,
        recovery.get("external_calls_during_recovery") != 0,
        recovery.get("log_repair") is not False,
        recovery.get("cross_process_coordination") is not False,
        recovery.get("authority_effect") != "none",
    ]):
        errors.append("generated reasoning-state recovery realization posture drift")
    frontier = next((item for item in contract.get("bounded_partial_realizations", []) if item.get("id") == "completed-turn-reasoning-frontier@1"), None)
    if not frontier:
        errors.append("generated system ontology lacks completed-turn frontier realization")
    elif any([
        frontier.get("append_only_frontier") is not True,
        frontier.get("exact_subject_binding") is not True,
        frontier.get("after_completion_checkpoint") is not True,
        frontier.get("recovery_replay_external_calls") != 0,
        frontier.get("automatic_successor_delivery") != "at-most-once-no-retry-after-recovery",
        frontier.get("delivery_acknowledgement") is not False,
        frontier.get("authority_effect") != "none",
    ]):
        errors.append("generated completed-turn frontier realization posture drift")
    for key in ["implementation_binding_status", "static_conformance_status", "runtime_evidence_status"]:
        if contract.get(key) != "not_evaluable":
            errors.append(f"generated implementation contract must keep {key}=not_evaluable")
    if projection.get("deterministic_runs") != 2 or not projection.get("equal_graph_bytes") or not projection.get("equal_system_ontology_bytes"):
        errors.append("projection receipt lacks two-run determinism evidence")
    if projection.get("source_graph_digest") != sha256_file(graph_path):
        errors.append("projection receipt graph digest drift")
    if projection.get("system_ontology_digest") != sha256_file(system_path):
        errors.append("projection receipt system-ontology digest drift")
    if projection.get("status") != "candidate" or projection.get("profile_release_admission") != "not-granted":
        errors.append("unadmitted DomainSpec projection must remain a candidate")


def verify_materialized_build(errors: list[str]) -> None:
    command = [
        str(REPOSITORY_ROOT / "toolchains/node-typescript/bin/node-env"),
        "run", "--project", "projects/domainspec-v2/impl", "--", "node", "--import", "tsx",
        "../../../cyberAlchemy-v2/development/agent-reasoning-engine/ontology/scripts/build.ts", "--emit-json",
    ]
    first = subprocess.run(command, cwd=REPOSITORY_ROOT, capture_output=True, text=True, check=False)
    second = subprocess.run(command, cwd=REPOSITORY_ROOT, capture_output=True, text=True, check=False)
    if first.returncode != 0 or second.returncode != 0:
        diagnostics = (first.stderr or second.stderr).strip().splitlines()
        errors.append(f"DomainSpec build replay failed: {diagnostics[-1] if diagnostics else 'unknown error'}")
        return
    if first.stdout != second.stdout:
        errors.append("DomainSpec build replay is non-deterministic")
        return
    try:
        artifacts = json.loads(first.stdout)
    except json.JSONDecodeError as exc:
        errors.append(f"DomainSpec build replay did not return JSON: {exc}")
        return
    for name, content in artifacts.items():
        if not (GENERATED_ROOT / name).is_file() or (GENERATED_ROOT / name).read_text(encoding="utf-8") != content:
            errors.append(f"materialized DomainSpec artifact is stale: {name}")


def material_digest() -> str:
    paths = [PACKAGE_ROOT.parent / "README.md"]
    paths.extend(
        path for path in PACKAGE_ROOT.rglob("*")
        if path.is_file() and "receipts" not in path.parts and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )
    payload = b"".join(
        path.relative_to(REPOSITORY_ROOT).as_posix().encode() + b"\0" + path.read_bytes()
        for path in sorted(paths)
    )
    return sha256_bytes(payload)


def evaluate(
    *,
    business: dict[str, Any] | None = None,
    bridge: dict[str, Any] | None = None,
    sources: dict[str, Any] | None = None,
    verify_generated_artifacts: bool = True,
    verify_build: bool = False,
) -> dict[str, Any]:
    errors: list[str] = []
    schema = load_json(SCHEMA_PATH)
    profile = load_json(PACKAGE_ROOT / "profile.json")
    business = business or load_json(PACKAGE_ROOT / "business-ontology.json")
    bridge = bridge or load_json(PACKAGE_ROOT / "bridge.json")
    sources = sources or load_json(PACKAGE_ROOT / "sources.json")
    capability = load_json(PACKAGE_ROOT / "product-capability.json")
    support = load_json(PACKAGE_ROOT / "product-capability-support.json")
    errors.extend(schema_errors(profile, schema, "#/$defs/profile", "profile"))
    errors.extend(schema_errors(business, schema, "#/$defs/businessOntology", "business ontology"))
    errors.extend(schema_errors(bridge, schema, "#/$defs/bridgeOntology", "bridge ontology"))
    errors.extend(schema_errors(sources, schema, "#/$defs/sourceRegistry", "source registry"))
    source_ids = validate_sources(sources, errors)
    business_ids = validate_business_ontology(business, errors)
    validate_product_capability(capability, support, business_ids, source_ids, errors)
    validate_bridge(bridge, business_ids, source_ids, errors)
    residue_count = validate_residue(errors)
    if verify_generated_artifacts:
        validate_generated(errors, sources, bridge)
    if verify_build and not errors:
        verify_materialized_build(errors)
    return {
        "schema_version": "cav2-agent-reasoning-engine-ontology-validation/v1",
        "status": "PASS" if not errors else "BLOCK",
        "ontology_type": "business-system-bridge",
        "materialization": "package-required",
        "business_node_count": len(business.get("nodes", [])),
        "business_relation_count": len(business.get("relations", [])),
        "system_node_count": len(domainspec_node_ids()),
        "bridge_edge_count": len(bridge.get("edges", [])),
        "gap_count": len(bridge.get("gaps", [])),
        "residue_count": residue_count,
        "bounded_partial_realizations": 15,
        "context_management_realization": "bounded-semantic-integrity-completion-frontier-recoverable-reasoning-state-codex-gateway-candidate",
        "whole_engine_realization": "absent",
        "domainspec_profile_admission": "not-granted",
        "implementation_binding_status": "not_evaluable",
        "static_conformance_status": "not_evaluable",
        "runtime_evidence_status": "not_evaluable",
        "authority_effect": "none",
        "material_digest": material_digest() if verify_generated_artifacts and not errors else None,
        "errors": errors,
        "claim_ceiling": "Candidate first-class ontology coherence and deterministic projection only; no capability adoption, complete runtime, implementation binding, conformance, publication, release, deployment, or external effect.",
    }


def write_receipt(result: dict[str, Any], receipt_name: str) -> Path:
    if result.get("status") != "PASS":
        raise ValueError("cannot materialize a validation receipt for a blocked result")
    if not receipt_name.startswith("validation-") or not receipt_name.endswith(".json"):
        raise ValueError("receipt name must match validation-*.json")
    if Path(receipt_name).name != receipt_name:
        raise ValueError("receipt name must not contain a path")
    path = PACKAGE_ROOT / "receipts" / receipt_name
    if path.exists():
        raise FileExistsError(f"append-only receipt already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    receipt = {**result, "validated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-build", action="store_true")
    parser.add_argument("--write-receipt", action="store_true")
    parser.add_argument("--receipt-name")
    args = parser.parse_args()
    try:
        if args.write_receipt and not args.receipt_name:
            raise ValueError("--write-receipt requires --receipt-name")
        if args.receipt_name and not args.write_receipt:
            raise ValueError("--receipt-name requires --write-receipt")
        result = evaluate(verify_build=args.verify_build)
        if args.write_receipt:
            receipt_path = write_receipt(result, args.receipt_name)
            result = {**result, "receipt": receipt_path.relative_to(REPOSITORY_ROOT).as_posix()}
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {
            "schema_version": "cav2-agent-reasoning-engine-ontology-validation/v1",
            "status": "BLOCK",
            "authority_effect": "none",
            "errors": [f"ontology package unavailable: {exc}"],
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
