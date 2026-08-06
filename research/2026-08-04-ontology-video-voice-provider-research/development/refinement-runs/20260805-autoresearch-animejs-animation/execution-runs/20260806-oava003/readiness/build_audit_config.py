#!/usr/bin/env python3
"""Build the OAVA-003 v2 Work Pack Readiness audit config from live owner artifacts."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO = Path(__file__).resolve().parents[8]
RUN_ROOT = Path(__file__).resolve().parents[3]
READINESS_ROOT = Path(__file__).resolve().parent
EVIDENCE_PATH = READINESS_ROOT / "evidence.json"
CONTRACT_PATH = RUN_ROOT / "work-pack" / "execution-contract-oava003.json"
TEMPLATE_PATH = (
    RUN_ROOT
    / "execution-runs"
    / "20260806-oava002"
    / "readiness"
    / "audit-config.json"
)
OUTPUT_PATH = READINESS_ROOT / "audit-config.json"
SCHEMA_PATH = (
    REPO
    / ".agents"
    / "skills"
    / "work-pack-readiness-audit"
    / "schemas"
    / "audit-config-v2.schema.json"
)
EVIDENCE_REL = EVIDENCE_PATH.relative_to(REPO).as_posix()


def canonical_digest(value: object) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def replace_oava(value: object) -> object:
    if isinstance(value, str):
        return (
            value.replace("oava002", "oava003")
            .replace("OAVA-002", "OAVA-003")
            .replace("TASK-OAVA-CONSULTATION", "TASK-OAVA-RUNTIME-ADMISSION")
        )
    if isinstance(value, list):
        return [replace_oava(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_oava(item) for key, item in value.items()}
    return value


def evidence_ref(binding_id: str, owner_ref: str, selector: str) -> dict[str, object]:
    payload = EVIDENCE_PATH.read_bytes()
    return {
        "binding_id": binding_id,
        "owner_ref": owner_ref,
        "artifact_ref": {
            "path": EVIDENCE_REL,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "size_bytes": len(payload),
        },
        "selector": selector,
    }


def replace_evidence_refs(value: object) -> None:
    if isinstance(value, list):
        for item in value:
            replace_evidence_refs(item)
        return
    if not isinstance(value, dict):
        return
    artifact = value.get("artifact_ref")
    if isinstance(artifact, dict) and artifact.get("path") == EVIDENCE_REL:
        payload = EVIDENCE_PATH.read_bytes()
        artifact["sha256"] = hashlib.sha256(payload).hexdigest()
        artifact["size_bytes"] = len(payload)
    for item in value.values():
        replace_evidence_refs(item)


def main() -> None:
    template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    config = replace_oava(copy.deepcopy(template))
    assert isinstance(config, dict)

    config["audit_id"] = "oava003-work-pack-v1.0.0-20260806"
    config["objective_ref"] = evidence_ref(
        "oava003-objective", "invoke:plan:apply-approved", "/objective"
    )
    config["closure_receipt_refs"] = [
        evidence_ref("oava003-define-exit", "refine:define", "/closure_receipts/define"),
        evidence_ref(
            "oava003-plan-exit",
            "invoke:plan:apply-approved",
            "/closure_receipts/plan",
        ),
        evidence_ref(
            "oava003-oava002-dependency",
            "invoke:refresh:apply-approved",
            "/closure_receipts/oava002",
        ),
        evidence_ref(
            "oava003-b001-dependency",
            "invoke:refresh:apply-approved",
            "/closure_receipts/b001",
        ),
    ]

    binding = copy.deepcopy(contract["execution_binding"])
    binding["dependencies"] = []
    config["execution_bindings"] = [binding]
    config["execution_policy"] = copy.deepcopy(contract["execution_policy"])
    assert config["execution_policy"]["allowed_routes_digest"] == canonical_digest(
        config["execution_policy"]["allowed_routes"]
    )

    config["runtime_binding"] = {
        "requested_task_session_execution_mode": "routed-mutation",
        "task_session_admission_receipt_ref": None,
    }
    config["closeout_bindings"] = [
        {
            "unit_id": "SWU-OAVA-003",
            "allowed_delta_policy_ref": evidence_ref(
                "oava003-allowed-delta",
                "invoke:refresh:apply-approved",
                "/closeout/allowed_delta",
            ),
            "owner_receipt_contract_ref": evidence_ref(
                "oava003-closeout-owner-contract",
                "invoke:refresh:apply-approved",
                "/closeout/owner_contract",
            ),
            "compensation": copy.deepcopy(contract["closeout"]["compensation"]),
        }
    ]
    config["continuity_projection"] = {
        "cursor": "SWU-OAVA-003",
        "completed_unit_receipt_refs": [],
        "joined_closeout_receipt_refs": [],
        "projected_next_successor": {
            "unit_id": "SWU-OAVA-003",
            "canonical_successor_ref": evidence_ref(
                "oava003-continuity-successor",
                "invoke:plan:apply-approved",
                "/continuity/canonical_successor",
            ),
            "projection_owner_ref": "work-pack-readiness-audit",
            "equivalence_validator_ref": evidence_ref(
                "oava003-continuity-equivalence",
                "work-pack-readiness-audit",
                "/continuity/equivalence",
            ),
            "continuation_router_verification_receipt_ref": evidence_ref(
                "oava003-continuity-router",
                "continuation-router",
                "/continuity/router_verification",
            ),
            "authority_effect": "none",
        },
    }

    config["approval_policy"]["approval_owner_ref"] = "goal:round-001"
    config["approval_policy"]["decision_gate_receipt_ref"] = evidence_ref(
        "oava003-approval-decision", "goal:round-001", "/approval/decision"
    )
    config["approval_policy"]["run_budget"] = {"max_task_session_requests": 1}
    config["lifecycle_status_refs"]["approval_status"]["value"] = (
        "pending-goal-batch-approval"
    )
    config["lifecycle_status_refs"]["approval_status"]["owner_ref"] = (
        "goal:round-001"
    )
    config["lifecycle_status_refs"]["approval_status"]["receipt_ref"] = evidence_ref(
        "oava003-lifecycle-approval", "goal:round-001", "/status/approval"
    )

    replace_evidence_refs(config)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(config),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        first = errors[0]
        location = "/".join(map(str, first.absolute_path)) or "<root>"
        raise SystemExit(f"AUDIT_CONFIG_INVALID {location}: {first.message}")
    OUTPUT_PATH.write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "output": OUTPUT_PATH.relative_to(REPO).as_posix(),
                "audit_id": config["audit_id"],
                "frontier": [item["unit_id"] for item in config["execution_bindings"]],
                "allowed_routes_digest": config["execution_policy"][
                    "allowed_routes_digest"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
