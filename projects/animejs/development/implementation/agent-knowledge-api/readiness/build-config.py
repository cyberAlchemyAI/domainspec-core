#!/usr/bin/env python3
"""Build the exact WPRA v2 plan-once config for WP-AKVE-001."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PLAN_ROOT = HERE.parent


def repository_root() -> Path:
    for candidate in [HERE, *HERE.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("repository root not found")


ROOT = repository_root()
WORK_PACK_PATH = PLAN_ROOT / "WORK-PACK.json"
EVIDENCE_PATH = HERE / "evidence.json"


def exact(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }


def binding(binding_id: str, owner: str, path: Path, selector: str) -> dict[str, object]:
    return {
        "binding_id": binding_id,
        "owner_ref": owner,
        "artifact_ref": exact(path),
        "selector": selector,
    }


def select(value: object, selector: str) -> object:
    current = value
    for part in selector.strip("/").split("/"):
        if not isinstance(current, dict):
            raise ValueError(f"selector does not resolve to object member: {selector}")
        current = current[part]
    return current


def status(name: str, selector: str) -> dict[str, object]:
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    return {
        "value": select(evidence, selector),
        "owner_ref": f"{name}-owner",
        "receipt_ref": binding(f"{name}-receipt", f"{name}-owner", EVIDENCE_PATH, selector),
    }


def build() -> dict[str, object]:
    plan = json.loads(WORK_PACK_PATH.read_text(encoding="utf-8"))
    attempt = plan["attempt_contract"]
    executions = []
    closeouts = []
    expected = []
    for unit in plan["execution_units"]:
        material_writes = unit["material_writes"]
        execution_outputs = unit["execution_outputs"]
        executions.append({
            "unit_id": unit["unit_id"],
            "task_id": unit["task_id"],
            "swu_id": unit["swu_id"],
            "lifecycle_owner": plan["owner"],
            "authority_class": plan["authority"]["class"],
            "publication_class": plan["publication"]["class"],
            "attempt_contract": attempt,
            "dependencies": unit["dependencies"],
            "canonical_successors": unit["successors"],
            "command": unit["command"],
            "validation_contracts": unit["validation_contracts"],
            "material_writes": material_writes,
            "execution_outputs": execution_outputs,
            "allowed_writes": sorted(set(material_writes + execution_outputs)),
            "material_package": {
                "package_ref": None,
                "producer_owner_ref": plan["material_owner"],
                "producer_receipt_ref": None,
                "schema_ref": None,
                "declared_sha256": None,
                "target_inventory_ref": None,
            },
            "byte_baselines": [],
        })
        closeouts.append({
            "unit_id": unit["unit_id"],
            "allowed_delta_policy_ref": binding(f"allowed-delta-{unit['unit_id']}", "invoke-refresh", EVIDENCE_PATH, "/closeout/allowedDeltaPolicy"),
            "owner_receipt_contract_ref": binding(f"closeout-owner-{unit['unit_id']}", "invoke-refresh", EVIDENCE_PATH, "/closeout/ownerReceiptContract"),
            "compensation": plan["closeout"]["compensation"],
        })
        expected.append(binding(f"expected-terminal-{unit['unit_id']}", "task-session", EVIDENCE_PATH, f"/expectedReceipts/{unit['unit_id']}"))

    return {
        "schema_version": "2.0.0",
        "audit_id": "animejs-akve-plan-semantic-v1",
        "repository_root": ".",
        "admission_timing": "selected-unit-at-task-session",
        "evidence_ceiling": "frozen-input-contractual-readiness",
        "classifier_version": "wpra-plan-semantic-v1",
        "objective_ref": binding("objective", "invoke-plan", WORK_PACK_PATH, "/objective"),
        "closure_receipt_refs": [
            binding("design-exit", "refine", EVIDENCE_PATH, "/closure/design"),
            binding("plan-exit", "invoke-plan", EVIDENCE_PATH, "/closure/plan"),
        ],
        "authority_bindings": {
            "canonical_authority_refs": [binding("canonical-objective", "invoke-plan", WORK_PACK_PATH, "/objective")],
            "semantic_bindings": {
                "owner": binding("semantic-owner", plan["owner"], EVIDENCE_PATH, "/semantic/owner"),
                "material": binding("semantic-material", plan["material_owner"], WORK_PACK_PATH, "/execution_units"),
                "validation": binding("semantic-validation", plan["owner"], WORK_PACK_PATH, "/contract_decisions"),
                "receipt": binding("semantic-receipt", "task-session", WORK_PACK_PATH, "/receipt_contract"),
                "closeout": binding("semantic-closeout", "invoke-refresh", WORK_PACK_PATH, "/closeout"),
            },
        },
        "execution_bindings": executions,
        "receipt_bindings": {
            "terminal_schema_ref": binding("terminal-schema", "task-session", EVIDENCE_PATH, "/receiptContract/terminalSchema"),
            "semantic_validator_ref": binding("terminal-validator", "task-session", EVIDENCE_PATH, "/receiptContract/semanticValidator"),
            "expected_receipt_refs": expected,
        },
        "closeout_bindings": closeouts,
        "runtime_binding": {
            "requested_task_session_execution_mode": "reusable-mutation",
            "task_session_admission_receipt_ref": None,
        },
        "status_receipt_refs": {
            "artifact_authored_status": status("artifact-authored", "/status/artifactAuthored"),
            "registry_released_status": status("registry-released", "/status/registryReleased"),
            "mutation_runtime_ready_status": status("mutation-runtime", "/status/mutationRuntimeReady"),
            "audit_verdict": status("audit-verdict", "/status/auditVerdict"),
        },
        "lifecycle_status_refs": {
            "plan_artifact_status": status("plan-artifact", "/lifecycle/planArtifact"),
            "audit_status": status("audit", "/lifecycle/audit"),
            "approval_status": status("approval", "/lifecycle/approval"),
            "chain_status": status("chain", "/lifecycle/chain"),
        },
        "approval_policy": {
            "approval_owner_ref": "direct-user",
            "decision_gate_receipt_ref": binding("decision", "direct-user", EVIDENCE_PATH, "/decision"),
            "run_budget": {"max_task_session_requests": plan["risk"]["max_task_session_requests"]},
            "risk_policy_ref": binding("risk-policy", "task-session", EVIDENCE_PATH, "/risk"),
            "allowed_audit_verdicts": ["pass", "flag"],
            "allowed_flag_classes": ["observability-residue"],
        },
        "continuity_projection": {
            "cursor": "AKVE-001",
            "completed_unit_receipt_refs": [],
            "joined_closeout_receipt_refs": [],
            "projected_next_successor": {
                "unit_id": "AKVE-001",
                "canonical_successor_ref": binding("first-successor", "invoke-plan", EVIDENCE_PATH, "/successors/AKVE-001"),
                "projection_owner_ref": "work-pack-readiness-audit",
                "equivalence_validator_ref": binding("equivalence-validator", "work-pack-readiness-audit", EVIDENCE_PATH, "/equivalence"),
                "continuation_router_verification_receipt_ref": binding("continuation-verification", "continuation-router", EVIDENCE_PATH, "/continuation"),
                "authority_effect": "none",
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "audit-config.json")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
