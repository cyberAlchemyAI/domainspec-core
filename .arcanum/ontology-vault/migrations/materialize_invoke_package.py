#!/usr/bin/env python3
"""Materialize the Invoke ontology package from three immutable legacy receipts.

This migration is private run-local evidence.  It emits only the explicitly
allowed public Invoke ontology and the sanitized CAV2 contract bindings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
ARCANUM = ROOT / "arcanum"
PACKAGE = ARCANUM / "ontology/invoke"
BUSINESS_RECEIPT = ROOT / ".arcanum/ontology-vault/map-2026-08-20-invoke-business.json"
SYSTEM_RECEIPT = ROOT / ".arcanum/ontology-vault/map-2026-08-20-invoke-system.json"
BRIDGE_RECEIPT = ROOT / ".arcanum/ontology-vault/map-2026-08-20-invoke.json"
PRIVATE_RECEIPT = ROOT / ".arcanum/ontology-vault/migrations/invoke-public-package-export.json"

EXPECTED_INPUT_DIGESTS = {
    "business": "9c5e270e10d9b8d3797d707f351a80a9fa08d8d1b8ae7c54bf768c982ac6b2f8",
    "system": "3ade21eec9c394ee45935058bea6caa1aabad3de0e9a410f6ad3d6f4f42ba707",
    "bridge": "2586b0e89acd94645b859898e745b6f2dc9e9eb1cce612825f22c991cc6cf2fc",
}

SOURCE_BINDINGS = {
    "arcanum/spells/invoke/README.md": "SRC-ROOT",
    "arcanum/spells/invoke/define.md": "SRC-DEFINE",
    "arcanum/spells/invoke/design.md": "SRC-DESIGN",
    "arcanum/spells/invoke/plan.md": "SRC-PLAN",
    "arcanum/spells/invoke/handoff.md": "SRC-HANDOFF",
    "arcanum/spells/invoke/refresh.md": "SRC-REFRESH",
    "arcanum/spells/invoke/mode-capabilities.json": "SRC-CAPABILITIES",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_ref(value: str) -> str:
    for path, source_id in SOURCE_BINDINGS.items():
        if value == path:
            return source_id
        if value.startswith(path + ":"):
            locator = value[len(path) + 1 :]
            line_ref = "-L".join(locator.split("-", 1)) if "-" in locator else locator
            return f"{source_id}#L{line_ref}"
    if value == "cyberAlchemy-v2/ontology/RELATION-MODEL.md":
        return "SRC-CAV2-RELATION-MODEL#MC-RELATION"
    if value.startswith(".arcanum/ontology-vault/"):
        return "MIGRATION-INVOKE-PUBLIC-PACKAGE#legacy-receipt"
    return value


def sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: sanitize(child) for key, child in value.items()}
    if isinstance(value, list):
        return [sanitize(child) for child in value]
    if isinstance(value, str):
        value = source_ref(value)
        substitutions = {
            "private candidate projection": "public candidate projection",
            "private CAV2 axis-separation definitions": "public CAV2 contract definitions",
            "private CAV2 definitions": "public CAV2 contract definitions",
            "private authority source": "public contract catalog",
            "CyberAlchemy v2 ontology route plus Invoke product or domain owner": "public model-contract steward plus Invoke product or domain owner",
            "CyberAlchemy v2 relation-contract fields": "public relation-contract fields",
            "CyberAlchemy v2 relation-contract envelope": "public relation-contract envelope",
            "CAV2 candidate relation contract": "public candidate relation contract",
        }
        for old, new in substitutions.items():
            value = value.replace(old, new)
        return value
    return value


def write_bytes(path: Path, content: bytes, apply: bool, changed: list[str]) -> None:
    relative = path.relative_to(ROOT).as_posix()
    if path.exists() and path.read_bytes() == content:
        return
    if path.exists():
        raise RuntimeError(f"refusing to overwrite non-matching existing file: {relative}")
    changed.append(relative)
    if apply:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def write_json(path: Path, value: Any, apply: bool, changed: list[str]) -> None:
    write_bytes(path, (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8"), apply, changed)


def public_sources() -> list[dict[str, str]]:
    records = [
        ("SRC-ROOT", "spells/invoke/README.md", "canonical-invoke-contract", "document"),
        ("SRC-DEFINE", "spells/invoke/define.md", "canonical-invoke-mode-contract", "document"),
        ("SRC-DESIGN", "spells/invoke/design.md", "canonical-invoke-mode-contract", "document"),
        ("SRC-PLAN", "spells/invoke/plan.md", "canonical-invoke-mode-contract", "document"),
        ("SRC-HANDOFF", "spells/invoke/handoff.md", "canonical-invoke-mode-contract", "document"),
        ("SRC-REFRESH", "spells/invoke/refresh.md", "canonical-invoke-mode-contract", "document"),
        ("SRC-CAPABILITIES", "spells/invoke/mode-capabilities.json", "canonical-machine-contract", "document"),
        ("SRC-CAV2-SOURCE-MAP", "arcana/ontology-vault/contracts/cav2-public-export-policy.json", "public-export-policy", "contract_id"),
        ("SRC-CAV2-DEFINITIONS", "arcana/ontology-vault/contracts/cav2-ontology-contracts.json", "public-definition-contracts", "definitions"),
        ("SRC-CAV2-DEFINITIONS-INDEX", "arcana/ontology-vault/contracts/cav2-ontology-contracts.json", "public-definition-index", "definitions[*].origin_id"),
        ("SRC-CAV2-NODE-MODEL", "arcana/ontology-vault/contracts/cav2-ontology-contracts.json", "public-model-contract", "MC-NODE"),
        ("SRC-CAV2-LIFECYCLE-MODEL", "arcana/ontology-vault/contracts/cav2-ontology-contracts.json", "public-model-contract", "MC-LIFECYCLE"),
        ("SRC-CAV2-PACKAGE-MODEL", "arcana/ontology-vault/contracts/cav2-ontology-contracts.json", "public-model-contract", "MC-PACKAGE"),
        ("SRC-CAV2-RELATION-MODEL", "arcana/ontology-vault/contracts/cav2-ontology-contracts.json", "public-model-contract", "MC-RELATION"),
    ]
    return [
        {
            "id": source_id,
            "locator": locator,
            "sha256": sha256(ARCANUM / locator),
            "posture": posture,
            "selector": selector,
            "visibility": "public",
        }
        for source_id, locator, posture, selector in records
    ]


def normalize_business_nodes(receipt: dict[str, Any]) -> list[dict[str, Any]]:
    nodes = sanitize(receipt["ontology"]["nodes"])
    for node in nodes:
        node["model_binding"] = "invoke-business-node/public-contract-v1"
    return nodes


def normalize_system_nodes(receipt: dict[str, Any]) -> list[dict[str, Any]]:
    labels = {
        "S-MODE-ROUTER": "Invoke Mode Router",
        "S-DEFINE-PACK": "Define Artifact Pack",
        "S-DESIGN-PIPELINE": "Design Pipeline",
        "S-PLAN-PACK": "Plan Artifact Pack",
        "S-HANDOFF-PACK": "Handoff Artifact Pack",
        "S-REFRESH-PIPELINE": "Refresh Pipeline",
        "S-CAPABILITY-RESOLVER": "Capability Resolver",
        "S-VALIDATION-SURFACE": "Validation Surface",
        "S-DISPATCH-TRACE": "Dispatch Trace",
    }
    result = []
    for node in receipt["ontology"]["nodes"]:
        result.append(
            {
                "id": node["id"],
                "label": labels[node["id"]],
                "branch": "system",
                "role": node["role"],
                "owner_route": "Invoke development cycle",
                "candidate_status": "candidate",
                "authority_effect": "none",
                "claim": node["claim"],
                "evidence_refs": sanitize(node["evidence_refs"]),
                "evidence_confidence": node["evidence_confidence"],
                "commitment_confidence": node["commitment_confidence"],
                "forbidden_collapse": "Declared contract structure is not observed runtime realization or lifecycle authority.",
            }
        )
    return result


def normalize_relations(records: list[dict[str, Any]], branch: str) -> list[dict[str, Any]]:
    return [
        {
            "id": record["id"],
            "type": record["type"],
            "branch": branch,
            "from": record["from"],
            "to": record["to"],
            "direction": "directed",
            "owner_route": "Invoke product or domain owner" if branch == "business" else "Invoke development cycle",
            "authority_effect": "none",
            "evidence_refs": sanitize(record["evidence_refs"]),
            "forbidden_collapse": "A declared relation does not prove runtime realization, promotion, publication, or authority.",
        }
        for record in records
    ]


def normalize_bridge(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": record["id"],
            "type": record["type"],
            "branch": "bridge",
            "from": record["from"],
            "to": record["to"],
            "direction": "business-to-system",
            "owner_route": "Invoke product or domain owner plus Invoke development cycle",
            "authority_effect": "none",
            "business_evidence_refs": sanitize(record["business_evidence_refs"]),
            "system_evidence_refs": sanitize(record["system_evidence_refs"]),
            "business_confidence": record["business_confidence"],
            "system_confidence": record["system_confidence"],
            "alignment_confidence": record["alignment_confidence"],
            "alignment_state": record["alignment_state"],
            "forbidden_collapse": "Declared cross-view alignment is not observed runtime realization or an authority decision.",
        }
        for record in records
    ]


def normalized_gaps(*receipts: tuple[str, dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for branch, receipt in receipts:
        for gap in receipt["ontology"]["gaps"]:
            record = sanitize(gap)
            record["branch"] = branch
            record["authority_effect"] = "none"
            result.append(record)
    return result


def schema_catalog() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://arcanum.dev/ontology/invoke/package.schema.json",
        "title": "Invoke ontology governed package records",
        "description": "Closed record contracts enforced by scripts/validate.py and the canonical Ontology Vault validator.",
        "$defs": {
            "authorityEffect": {"const": "none"},
            "sourceReference": {"type": "string", "pattern": "^SRC-[A-Z0-9-]+(#.+)?$"},
            "stableId": {"type": "string", "pattern": "^[A-Z]+-[A-Z0-9-]+$"},
            "source": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "locator", "sha256", "posture", "selector", "visibility"],
                "properties": {
                    "id": {"$ref": "#/$defs/stableId"},
                    "locator": {"type": "string"},
                    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                    "posture": {"type": "string"},
                    "selector": {"type": "string"},
                    "visibility": {"const": "public"},
                },
            },
            "relationCore": {
                "type": "object",
                "required": ["id", "type", "branch", "from", "to", "direction", "owner_route", "authority_effect", "forbidden_collapse"],
                "properties": {"authority_effect": {"$ref": "#/$defs/authorityEffect"}},
            },
            "validationReceipt": {
                "type": "object",
                "additionalProperties": False,
                "required": ["schema_version", "package_id", "material_digest", "material_inventory", "status", "checks", "counts", "errors", "authority_effect", "promotion_status", "publication_status"],
            },
        },
        "governed_files": {
            "profile": "profile.json",
            "sources": "sources.json#sources",
            "business_nodes": "nodes/business.json#nodes",
            "system_nodes": "nodes/system.json#nodes",
            "branch_relations": ["relations/business.json#relations", "relations/system.json#relations"],
            "bridge_relations": "relations/bridge.json#relations",
            "views": ["views/business.json", "views/system.json", "views/bridge.json"],
            "residue": "residue.json#gaps",
            "receipts": "receipts/validation-*.json",
        },
    }


def build_files() -> tuple[dict[Path, Any], dict[Path, bytes]]:
    business = load_json(BUSINESS_RECEIPT)
    system = load_json(SYSTEM_RECEIPT)
    bridge = load_json(BRIDGE_RECEIPT)
    business_nodes = normalize_business_nodes(business)
    system_nodes = normalize_system_nodes(system)
    business_relations = normalize_relations(business["ontology"]["relationships"], "business")
    system_relations = normalize_relations(system["ontology"]["relationships"], "system")
    bridge_relations = normalize_bridge(bridge["ontology"]["bridge_edges"])
    gaps = normalized_gaps(("business", business), ("system", system), ("bridge", bridge))
    operation_composition = sanitize(business["ontology"]["operation_composition"])

    profile = {
        "schema_version": "arcanum.ontology.package.profile.v1",
        "package_id": "arcanum.invoke.ontology",
        "subject": "Invoke",
        "status": "candidate",
        "owner_route": "Invoke lifecycle owner",
        "visibility": "public",
        "ontology_types": ["business-domain", "system-runtime", "business-system-bridge"],
        "materialization": {
            "classification": "package-required",
            "triggers": [
                "multiple_branches_or_views",
                "bridge_requested",
                "stable_identity_survives_run",
                "enriches_existing_ontology",
                "reusable_surfaces_required",
            ],
            "legacy_receipts_are_state_stores": False,
        },
        "contract_bindings": {
            "package_materialization": "arcana/ontology-vault/contracts/package-materialization.json",
            "public_export_policy": "arcana/ontology-vault/contracts/cav2-public-export-policy.json",
            "public_contracts": "arcana/ontology-vault/contracts/cav2-ontology-contracts.json",
            "local_schema": "ontology/invoke/schemas/package.schema.json",
        },
        "authority": {
            "effect": "none",
            "ontology_decides_authority": False,
            "arcanum_definition_authority": False,
            "promotion_status": "not_requested",
            "publication_status": "not_requested",
        },
        "validation": {
            "mode": "check-only-by-default",
            "receipt_mode": "explicit-append-only",
            "command": "python3 ontology/invoke/scripts/validate.py",
        },
    }

    sources = {"schema_version": "arcanum.ontology.sources.v1", "package_id": "arcanum.invoke.ontology", "sources": public_sources()}
    operation_document = {
        "schema_version": "arcanum.ontology.invoke.operation-composition.v1",
        "package_id": "arcanum.invoke.ontology",
        "authority_effect": "none",
        "operation_composition": operation_composition,
    }
    residue = {
        "schema_version": "arcanum.ontology.residue.v1",
        "package_id": "arcanum.invoke.ontology",
        "gaps": gaps,
        "authority_boundary": {
            "authority_effect": "none",
            "ontology_decides_authority": False,
            "not_owned": [
                "promotion verdict",
                "publication decision",
                "runtime conformance",
                "release admission",
                "canonical definition authority",
            ],
        },
    }
    preserved = {
        "business_node_ids": [record["id"] for record in business_nodes],
        "system_node_ids": [record["id"] for record in system_nodes],
        "business_relation_ids": [record["id"] for record in business_relations],
        "system_relation_ids": [record["id"] for record in system_relations],
        "bridge_relation_ids": [record["id"] for record in bridge_relations],
        "active_operation_ids": [record["id"] for record in operation_composition["operations"]],
        "deferred_operation_ids": [record["id"] for record in operation_composition["deferred_operations"]],
        "capability_ids": [record["id"] for record in operation_composition["supporting_capabilities"]],
        "phase_count": sum(len(record["phases"]) for record in operation_composition["operations"]),
    }
    migration = {
        "schema_version": "arcanum.ontology.invoke.migration.v1",
        "migration_id": "MIGRATION-INVOKE-PUBLIC-PACKAGE",
        "source_artifact_class": "legacy-invocation-validation-receipts",
        "materialized_as": "durable-governed-package-candidate",
        "preserved": preserved,
        "schema_witness": {
            "id": business["schema_amendment_witness"]["id"],
            "binding": "public package model-contract migration witness",
            "preserved_node_fields": business["schema_amendment_witness"]["delta"]["preserved_node_fields"],
            "added_package_surfaces": ["profile", "sources", "views", "schemas", "validator", "validation_receipts"],
            "relation_envelope_status": "explicit package envelope added without claiming source-model conformance or authority",
            "authority_effect": "none",
        },
        "legacy_receipts_mutated": False,
        "authority_effect": "none",
    }
    history = {
        "schema_version": "arcanum.ontology.invoke.legacy-validation-history.v1",
        "package_id": "arcanum.invoke.ontology",
        "legacy_validations": [
            {
                "legacy_receipt_id": "map-2026-08-20-invoke-business",
                "ontology_type": business["ontology_type"],
                "branch": "business",
                "sha256": EXPECTED_INPUT_DIGESTS["business"],
                "result": business["result"],
                "checks_total": len(business["checks"]),
                "pass_count": sum(check["status"] == "pass" for check in business["checks"]),
                "flag_count": sum(check["status"] == "flag" for check in business["checks"]),
                "validated_at": business["validated_at"],
                "promotion_status": business["promotion_status"],
                "authority_effect": business["authority_effect"],
            },
            {
                "legacy_receipt_id": "map-2026-08-20-invoke-system",
                "ontology_type": system["ontology_type"],
                "branch": "system",
                "sha256": EXPECTED_INPUT_DIGESTS["system"],
                "result": system["result"],
                "checks_total": len(system["checks"]),
                "pass_count": sum(check["status"] == "pass" for check in system["checks"]),
                "flag_count": sum(check["status"] == "flag" for check in system["checks"]),
                "validated_at": system["validated_at"],
                "promotion_status": system["promotion_status"],
                "authority_effect": system["authority_effect"],
            },
            {
                "legacy_receipt_id": "map-2026-08-20-invoke",
                "ontology_type": bridge["ontology_type"],
                "branch": "bridge",
                "sha256": EXPECTED_INPUT_DIGESTS["bridge"],
                "result": bridge["result"],
                "checks_total": len(bridge["checks"]),
                "pass_count": sum(check["status"] == "pass" for check in bridge["checks"]),
                "flag_count": sum(check["status"] == "flag" for check in bridge["checks"]),
                "validated_at": bridge["validated_at"],
                "promotion_status": bridge["promotion_status"],
                "authority_effect": bridge["authority_effect"],
            },
        ],
        "history_posture": "preserved validation evidence; not current package validation",
        "authority_effect": "none",
    }

    json_files: dict[Path, Any] = {
        PACKAGE / "profile.json": profile,
        PACKAGE / "sources.json": sources,
        PACKAGE / "nodes/business.json": {"schema_version": "arcanum.ontology.nodes.v1", "branch": "business", "nodes": business_nodes},
        PACKAGE / "nodes/system.json": {"schema_version": "arcanum.ontology.nodes.v1", "branch": "system", "nodes": system_nodes},
        PACKAGE / "relations/business.json": {"schema_version": "arcanum.ontology.relations.v1", "branch": "business", "relations": business_relations},
        PACKAGE / "relations/system.json": {"schema_version": "arcanum.ontology.relations.v1", "branch": "system", "relations": system_relations},
        PACKAGE / "relations/bridge.json": {"schema_version": "arcanum.ontology.bridge-relations.v1", "branch": "bridge", "relations": bridge_relations},
        PACKAGE / "views/business.json": {
            "schema_version": "arcanum.ontology.view.v1", "id": "VIEW-INVOKE-BUSINESS", "branch": "business",
            "node_refs": preserved["business_node_ids"], "relation_refs": preserved["business_relation_ids"], "imports": [], "authority_effect": "none",
        },
        PACKAGE / "views/system.json": {
            "schema_version": "arcanum.ontology.view.v1", "id": "VIEW-INVOKE-SYSTEM", "branch": "system",
            "node_refs": preserved["system_node_ids"], "relation_refs": preserved["system_relation_ids"], "imports": [], "authority_effect": "none",
        },
        PACKAGE / "views/bridge.json": {
            "schema_version": "arcanum.ontology.view.v1", "id": "VIEW-INVOKE-BRIDGE", "branch": "bridge",
            "node_refs": [], "relation_refs": preserved["bridge_relation_ids"],
            "imports": ["VIEW-INVOKE-BUSINESS", "VIEW-INVOKE-SYSTEM"], "authority_effect": "none",
        },
        PACKAGE / "residue.json": residue,
        PACKAGE / "extensions/operation-composition.json": operation_document,
        PACKAGE / "schemas/package.schema.json": schema_catalog(),
        PACKAGE / "migration/preserved-identities.json": migration,
        PACKAGE / "history/legacy-validation.json": history,
    }

    readme = """# Invoke Ontology Package

This candidate is the durable, reusable ontology for the public Invoke capability. It replaces no canonical Invoke contract and does not turn validation evidence into authority.

The package keeps business and system definitions branch-local, expresses their alignment only in the bridge view, preserves the stable IDs and operation composition from the three legacy validation receipts, and retains unresolved residue instead of silently filling it.

## Public/private boundary

Public CAV2-derived content is limited to the definition and model contracts allowed by the Ontology Vault export policy. The package contains no private source paths or digests, proof material, source scripts, or evidence from other systems. Exact private provenance remains outside this public candidate.

Ontology records describe and validate structure. They do not decide authority, promotion, publication, runtime conformance, release admission, or canonical definition ownership.

## Validate

From the Arcanum repository root:

```bash
python3 ontology/invoke/scripts/validate.py
```

Receipt creation is explicit and append-only:

```bash
python3 ontology/invoke/scripts/validate.py --write-receipt
```
"""
    index_lines = [
        "# Invoke Ontology Index",
        "",
        "- Profile: `profile.json`",
        "- Sources: `sources.json`",
        "- Business view: `views/business.json`",
        "- System view: `views/system.json`",
        "- Bridge view: `views/bridge.json`",
        "- Residue: `residue.json`",
        "- Operation composition: `extensions/operation-composition.json`",
        "- Preserved identities: `migration/preserved-identities.json`",
        "- Validation history: `history/legacy-validation.json`",
        "",
        "## Stable nodes",
        "",
        *[f"- `{record['id']}` — {record['label']} ({record['branch']})" for record in [*business_nodes, *system_nodes]],
        "",
        "## Stable relations",
        "",
        *[f"- `{record['id']}` — {record['from']} {record['type']} {record['to']} ({record['branch']})" for record in [*business_relations, *system_relations, *bridge_relations]],
        "",
    ]
    validator = """#!/usr/bin/env python3
\"\"\"Validate the Invoke ontology package with the canonical Ontology Vault validator.\"\"\"

from pathlib import Path
import subprocess
import sys


ARCANUM_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ARCANUM_ROOT / \"arcana/ontology-vault/scripts/ontology_package.py\"


raise SystemExit(
    subprocess.call(
        [
            sys.executable,
            str(VALIDATOR),
            \"validate-package\",
            \"--package-root\",
            str(Path(__file__).resolve().parents[1]),
            \"--repository-root\",
            str(ARCANUM_ROOT),
            *sys.argv[1:],
        ]
    )
)
"""
    text_files = {
        PACKAGE / "README.md": readme.encode("utf-8"),
        PACKAGE / "INDEX.md": ("\n".join(index_lines)).encode("utf-8"),
        PACKAGE / "scripts/validate.py": validator.encode("utf-8"),
    }
    return json_files, text_files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    inputs = {"business": BUSINESS_RECEIPT, "system": SYSTEM_RECEIPT, "bridge": BRIDGE_RECEIPT}
    actual_digests = {name: sha256(path) for name, path in inputs.items()}
    if actual_digests != EXPECTED_INPUT_DIGESTS:
        raise RuntimeError(f"legacy receipt digest mismatch: {actual_digests}")

    json_files, text_files = build_files()
    changed: list[str] = []
    for path, value in json_files.items():
        write_json(path, value, args.apply, changed)
    for path, content in text_files.items():
        write_bytes(path, content, args.apply, changed)

    public_inventory = []
    for path in sorted([*json_files, *text_files], key=lambda item: item.relative_to(PACKAGE).as_posix()):
        if args.apply:
            digest = sha256(path)
        else:
            if path in json_files:
                payload = (json.dumps(json_files[path], indent=2, sort_keys=True) + "\n").encode("utf-8")
            else:
                payload = text_files[path]
            digest = hashlib.sha256(payload).hexdigest()
        public_inventory.append({"path": path.relative_to(PACKAGE).as_posix(), "sha256": digest})

    private_receipt = {
        "schema_version": "ontology-vault.invoke-public-package-export.v1",
        "migration_id": "MIGRATION-INVOKE-PUBLIC-PACKAGE",
        "status": "candidate-materialized" if args.apply else "preview",
        "private_inputs": [
            {"role": name, "path": path.relative_to(ROOT).as_posix(), "sha256": actual_digests[name]}
            for name, path in inputs.items()
        ],
        "source_rebinding": {
            "private_definition_and_model_sources": "sanitized public contract catalog",
            "public_invoke_sources": "same source IDs with public repository-relative locators and current digests",
            "private_paths_or_digests_in_public_package": False,
        },
        "public_package": "arcanum/ontology/invoke",
        "public_inventory": public_inventory,
        "legacy_receipts_mutated": False,
        "authority_effect": "none",
        "promotion_status": "not_requested",
        "publication_status": "not_requested",
    }
    write_json(PRIVATE_RECEIPT, private_receipt, args.apply, changed)
    print(json.dumps({"mode": "apply" if args.apply else "preview", "changed_paths": changed, "private_receipt": str(PRIVATE_RECEIPT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
