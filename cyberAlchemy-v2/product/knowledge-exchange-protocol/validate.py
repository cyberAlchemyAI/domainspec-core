#!/usr/bin/env python3
"""Check the private Knowledge Exchange Protocol model without writing state."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


PACKAGE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
PRODUCT_THESIS_SCHEMA = REPOSITORY_ROOT / "cyberAlchemy-v2/product/schemas/product-thesis-record.schema.json"
CAPABILITY_SCHEMA = REPOSITORY_ROOT / "cyberAlchemy-v2/capability/schemas/capability.schema.json"
MATERIAL_FILES = (
    "IDENTITY-DECISION.json",
    "PRODUCT-THESIS.md",
    "README.md",
    "business-ontology.json",
    "grant-encrypted-knowledge-coownership.product-capability.json",
    "product-thesis.record.json",
    "product-thesis.sources.json",
    "schema.json",
    "tests/test_validate.py",
    "validate.py",
)


def load(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path} must contain one JSON object")
        return {}
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def markdown_heading_bytes(path: Path, heading: str) -> bytes | None:
    text = path.read_text(encoding="utf-8")
    marker = f"{heading}\n"
    start = text.find(marker)
    if start < 0:
        return None
    end = text.find("\n## ", start + len(marker))
    selected = text[start:] if end < 0 else text[start:end + 1]
    return selected.encode("utf-8")


def validate_instance(instance: Any, schema: dict[str, Any], label: str, errors: list[str]) -> None:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        errors.append(f"{label} schema invalid: {exc.message}")
        return
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        errors.append(f"{label} schema violation at {location}: {error.message}")


def root_ref_schema(schema: dict[str, Any], definition: str) -> dict[str, Any]:
    """Keep the root $defs available while selecting one validation entrypoint."""
    selected = dict(schema)
    selected.pop("$id", None)
    selected["$ref"] = f"#/$defs/{definition}"
    return selected


def material_digest(errors: list[str]) -> str:
    digest = hashlib.sha256()
    for relative in sorted(MATERIAL_FILES):
        path = PACKAGE_ROOT / relative
        if not path.is_file():
            errors.append(f"missing material file: {relative}")
            continue
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def unique_ids(records: list[Any], field: str, label: str, errors: list[str]) -> set[str]:
    found: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        value = record.get(field)
        if not isinstance(value, str):
            continue
        if value in found:
            errors.append(f"duplicate {label}: {value}")
        found.add(value)
    return found


def validate() -> dict[str, Any]:
    errors: list[str] = []
    local_schema = load(PACKAGE_ROOT / "schema.json", errors)
    identity = load(PACKAGE_ROOT / "IDENTITY-DECISION.json", errors)
    thesis = load(PACKAGE_ROOT / "product-thesis.record.json", errors)
    sources = load(PACKAGE_ROOT / "product-thesis.sources.json", errors)
    capability = load(PACKAGE_ROOT / "grant-encrypted-knowledge-coownership.product-capability.json", errors)
    ontology = load(PACKAGE_ROOT / "business-ontology.json", errors)
    thesis_schema = load(PRODUCT_THESIS_SCHEMA, errors)
    capability_schema = load(CAPABILITY_SCHEMA, errors)

    if local_schema:
        validate_instance(identity, root_ref_schema(local_schema, "identityDecision"), "identity decision", errors)
        validate_instance(sources, root_ref_schema(local_schema, "sourceRegistry"), "source registry", errors)
        validate_instance(ontology, root_ref_schema(local_schema, "businessOntology"), "business ontology", errors)
    if thesis_schema:
        validate_instance(thesis, thesis_schema, "product thesis", errors)
    if capability_schema:
        validate_instance(capability, root_ref_schema(capability_schema, "productCapability"), "product capability", errors)

    source_ids: set[str] = set()
    for source in sources.get("sources", []):
        if not isinstance(source, dict):
            continue
        source_id = source.get("id")
        if isinstance(source_id, str):
            if source_id in source_ids:
                errors.append(f"duplicate source id: {source_id}")
            source_ids.add(source_id)
        path = REPOSITORY_ROOT / str(source.get("path", ""))
        if not path.is_file():
            errors.append(f"missing source: {source.get('path')}")
        elif source.get("digest_scope") == "whole-file":
            if sha256(path) != source.get("sha256"):
                errors.append(f"source digest drift: {source_id}")
        elif source.get("digest_scope") == "markdown-heading":
            selected = markdown_heading_bytes(path, str(source.get("selector", "")))
            if selected is None:
                errors.append(f"source selector missing: {source_id}")
            elif hashlib.sha256(selected).hexdigest() != source.get("sha256"):
                errors.append(f"source selection digest drift: {source_id}")
        else:
            errors.append(f"unknown source digest scope: {source_id}")

    required_sources = {
        "SRC-KEP-DEFINITION-D63",
        "SRC-KEP-DEFINITION-D67",
        "SRC-KEP-PARENT-PRODUCT-THESIS",
        "SRC-KEP-PARENT-PRODUCT-THESIS-RECORD",
        "SRC-KEP-PRODUCT-THESIS-SCHEMA",
        "SRC-KEP-PRODUCT-CAPABILITY-SCHEMA",
    }
    missing_sources = sorted(required_sources - source_ids)
    if missing_sources:
        errors.append(f"missing required sources: {', '.join(missing_sources)}")

    bindings = {
        "product": "CA2-PRODUCT-KNOWLEDGE-EXCHANGE-PROTOCOL",
        "thesis": "CA2-PRODUCT-THESIS-KNOWLEDGE-EXCHANGE-PROTOCOL",
        "project": "CA2-PROJECT-KNOWLEDGE-EXCHANGE-SOLANA-PROOF",
        "goal": "CA2-GOAL-KNOWLEDGE-EXCHANGE-ENCRYPTED-COOWNERSHIP",
        "capability": "CA2-CAP-GRANT-ENCRYPTED-KNOWLEDGE-COOWNERSHIP",
        "ontology": "CA2-ONTOLOGY-KNOWLEDGE-EXCHANGE-BUSINESS",
    }
    expected_pairs = (
        (identity.get("product_id"), bindings["product"], "identity product"),
        (identity.get("thesis_id"), bindings["thesis"], "identity thesis"),
        (identity.get("project_id"), bindings["project"], "identity project"),
        (identity.get("goal_id"), bindings["goal"], "identity goal"),
        (identity.get("capability_id"), bindings["capability"], "identity capability"),
        (thesis.get("product_ref"), bindings["product"], "thesis product"),
        (thesis.get("thesis_id"), bindings["thesis"], "thesis identity"),
        (capability.get("product_ref"), bindings["product"], "capability product"),
        (capability.get("capability_id"), bindings["capability"], "capability identity"),
        (capability.get("business_ontology_ref"), bindings["ontology"], "capability ontology"),
        (ontology.get("product_ref"), bindings["product"], "ontology product"),
        (ontology.get("capability_ref"), bindings["capability"], "ontology capability"),
    )
    for actual, expected, label in expected_pairs:
        if actual != expected:
            errors.append(f"{label} must be {expected}")

    nodes = ontology.get("nodes", [])
    relations = ontology.get("relations", [])
    residue = ontology.get("residue", [])
    node_ids = unique_ids(nodes, "id", "node id", errors)
    unique_ids(relations, "id", "relation id", errors)
    unique_ids(ontology.get("rules", []), "rule_id", "rule id", errors)
    unique_ids(ontology.get("proof_requirements", []), "proof_id", "proof id", errors)
    residue_ids = unique_ids(residue, "residue_id", "residue id", errors)
    selection_ids = unique_ids(ontology.get("source_selections", []), "selection_id", "selection id", errors)

    external_nodes = {"CA2-PRODUCT-CYBERALCHEMY"}
    for relation in relations:
        if not isinstance(relation, dict):
            continue
        for endpoint in ("source", "target"):
            value = relation.get(endpoint)
            if value not in node_ids | external_nodes:
                errors.append(f"dangling relation {relation.get('id')} {endpoint}: {value}")

    local_ref_fields = ("outcome_refs", "participant_refs", "consumer_refs", "input_contract_refs", "output_contract_refs", "context_policy_refs")
    for field in local_ref_fields:
        for value in capability.get(field, []):
            if value not in node_ids:
                errors.append(f"capability {field} has dangling ref: {value}")
    obligation_ref = capability.get("obligation_registry_ref")
    if obligation_ref not in node_ids:
        errors.append(f"capability obligation registry has dangling ref: {obligation_ref}")

    realization_refs = set(capability.get("realization_binding_refs", []))
    declared_bindings = {item.get("binding_ref") for item in residue if isinstance(item, dict) and item.get("binding_ref")}
    if not realization_refs <= declared_bindings:
        errors.append("future realization binding must remain declared as residue")

    evidence_refs = set(capability.get("evidence_refs", []))
    owner_source_refs = {
        ref
        for owner in capability.get("owner_routes", []) if isinstance(owner, dict)
        for ref in owner.get("source_refs", [])
    }
    unknown_selections = sorted((evidence_refs | owner_source_refs) - selection_ids)
    if unknown_selections:
        errors.append(f"capability has unknown source selections: {', '.join(unknown_selections)}")

    lifecycle_residue = set(capability.get("lifecycle_posture", {}).get("residue_refs", []))
    if not lifecycle_residue <= residue_ids:
        errors.append("capability lifecycle posture has dangling residue refs")
    if capability.get("lifecycle_posture", {}).get("commitment", {}).get("value") != "not-adopted":
        errors.append("candidate capability commitment must remain not-adopted")

    rules = {rule.get("rule_id"): rule for rule in ontology.get("rules", []) if isinstance(rule, dict)}
    required_rules = {
        "KEP-RULE-OWNER-SET-MONOTONIC-FIRST-PROOF",
        "KEP-RULE-NO-PUBLIC-SECRETS",
        "KEP-RULE-SEPARATE-KEY-ROLES",
        "KEP-RULE-REISSUE-PRESERVES-STATE",
        "KEP-RULE-COMPROMISE-NEW-EPOCH",
        "KEP-RULE-NO-PAYMENT-FIRST-PROOF",
    }
    missing_rules = sorted(required_rules - set(rules))
    if missing_rules:
        errors.append(f"missing required business rules: {', '.join(missing_rules)}")

    if any(item.get("evidence_state") != "not_evaluable" for item in ontology.get("proof_requirements", []) if isinstance(item, dict)):
        errors.append("model-only proof requirements must remain not_evaluable")

    construction = ontology.get("construction_state", {})
    expected_construction = {
        "canonical_definitions": "current",
        "product_capability": "candidate",
        "business_ontology": "candidate",
        "domainspec_v2_source": "blocked",
        "compiled_graph_and_system_ontology": "not_evaluable",
        "implementation_binding": "not_evaluable",
        "conformance_evidence": "not_evaluable",
    }
    if construction != expected_construction:
        errors.append("D65 construction state may not advance beyond the candidate business ontology")

    carrier = (PACKAGE_ROOT / "PRODUCT-THESIS.md").read_text(encoding="utf-8")
    for marker in (
        "Thesis ID: CA2-PRODUCT-THESIS-KNOWLEDGE-EXCHANGE-PROTOCOL",
        "Canonical definition: CAV2-D63",
        "## Product Identity",
        "## Project",
        "## Goal",
        "## Revision Criteria",
        "## Claim Ceiling",
        "owner set `{A}` to `{A, B}`",
    ):
        if marker not in carrier:
            errors.append(f"product thesis carrier missing marker: {marker}")

    digest = material_digest(errors)
    return {
        "schema_version": "cav2-knowledge-exchange-product-validation/v1",
        "status": "PASS" if not errors else "BLOCK",
        "package_root": "cyberAlchemy-v2/product/knowledge-exchange-protocol",
        "product_id": bindings["product"],
        "project_id": bindings["project"],
        "goal_id": bindings["goal"],
        "capability_id": bindings["capability"],
        "business_ontology_id": bindings["ontology"],
        "material_digest": digest,
        "counts": {
            "sources": len(source_ids),
            "nodes": len(node_ids),
            "relations": len(relations),
            "rules": len(rules),
            "proof_requirements": len(ontology.get("proof_requirements", [])),
            "residue": len(residue_ids),
        },
        "d65_last_evaluable_stage": "capability-local business ontology candidate",
        "authority_effect": "none",
        "claim_ceiling": "Candidate Product, Project, Goal, Product Capability, and business ontology shape only; no adoption, DomainSpec or system-ontology admission, implementation, conformance, cryptographic proof, Solana effect, publication, release, or deployment.",
        "errors": errors,
    }


def main() -> int:
    result = validate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
