#!/usr/bin/env python3
"""Validate WP-CAL-TEN-L0 admission contracts without executing product work."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


EXPECTED_FRONTIER = [f"SWU-CAL-{index:03d}" for index in range(1, 11)]
TERMINAL = "__complete__"
PLAN_PREFIX = "projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/09-invoke-plan"
EXPECTED_DEPENDENCIES = {
    "SWU-CAL-001": [],
    "SWU-CAL-002": ["SWU-CAL-001"],
    "SWU-CAL-003": ["SWU-CAL-001", "SWU-CAL-002"],
    "SWU-CAL-004": ["SWU-CAL-003"],
    "SWU-CAL-005": ["SWU-CAL-002", "SWU-CAL-004"],
    "SWU-CAL-006": EXPECTED_FRONTIER[:5],
    "SWU-CAL-007": ["SWU-CAL-006"],
    "SWU-CAL-008": ["SWU-CAL-007"],
    "SWU-CAL-009": ["SWU-CAL-008"],
    "SWU-CAL-010": ["SWU-CAL-009"],
}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def schema_errors(instance: dict, schema: dict, label: str) -> list[str]:
    return [
        f"{label}:{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(instance),
            key=lambda item: list(item.path),
        )
    ]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_ref(root: Path, relative: str) -> dict:
    path = root / relative
    return {"path": f"{PLAN_PREFIX}/{relative}", "sha256": sha256(path), "size_bytes": path.stat().st_size}


def binding(root: Path, binding_id: str, owner_ref: str, relative: str, selector: str = "") -> dict:
    return {"binding_id": binding_id, "owner_ref": owner_ref, "artifact_ref": exact_ref(root, relative), "selector": selector}


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def build_wpra_config(root: Path) -> dict:
    contracts = load(root / "work-pack/admission/L0-EXECUTION-CONTRACTS.json")
    targets = load(root / "work-pack/shared/CLOSEOUT-TARGETS.json")
    target_by_unit = {item["swu_id"]: item for item in targets["targets"]}
    allowed_routes = []
    for index, unit in enumerate(contracts["units"]):
        swu_id = unit["swu_id"]
        allowed_routes.extend([
            {
                "route_id": f"task-session-cal-{index + 1:03d}",
                "frontier_swu": swu_id,
                "capability": "task-session",
                "mode": "execute",
                "target": swu_id,
                "write_scope": unit["allowed_writes"],
                "effect_class": "repository-local-reversible",
                "required_inputs": [
                    f"{PLAN_PREFIX}/work-pack/admission/L0-EXECUTION-CONTRACTS.json#/units/{index}",
                    f"{PLAN_PREFIX}/WORK-PACK.md#SWU-manifest-and-navigation",
                ],
                "expected_receipt": unit["terminal_receipt"],
            },
            {
                "route_id": f"closeout-cal-{index + 1:03d}",
                "frontier_swu": swu_id,
                "capability": "invoke",
                "mode": "refresh-apply-approved",
                "target": f"{swu_id}-closeout",
                "write_scope": target_by_unit[swu_id]["target_inventory"],
                "effect_class": "repository-local-reversible",
                "required_inputs": [unit["terminal_receipt"], f"{PLAN_PREFIX}/work-pack/shared/CLOSEOUT-CONTRACT.md", f"{PLAN_PREFIX}/work-pack/shared/CLOSEOUT-TARGETS.json#/targets/{index}"],
                "expected_receipt": unit["closeout_receipt"],
            },
        ])

    execution_bindings = []
    for unit in contracts["units"]:
        execution_bindings.append({
            "task_id": unit["task_id"],
            "swu_id": unit["swu_id"],
            "lifecycle_owner": unit["lifecycle_owner"],
            "authority_class": unit["authority_class"],
            "publication_class": unit["publication_class"],
            "attempt_contract": unit["attempt_contract"],
            "unit_id": unit["swu_id"],
            "dependencies": unit["dependencies"],
            "canonical_successors": unit["canonical_successors"],
            "command": {"argv": unit["command"]["argv"], "cwd": unit["command"]["cwd"], "risk_class": unit["command"]["risk_class"]},
            "validation_contracts": [{key: item[key] for key in ("command_id", "argv", "cwd", "timeout_seconds", "max_output_bytes")} for item in unit["validation_contracts"]],
            "material_writes": unit["material_writes"],
            "execution_outputs": unit["execution_outputs"],
            "allowed_writes": unit["allowed_writes"],
            "material_package": {"package_ref": None, "producer_owner_ref": unit["material_producer_owner"], "producer_receipt_ref": None, "schema_ref": None, "declared_sha256": None, "target_inventory_ref": None},
            "byte_baselines": [],
        })

    status_ref = lambda binding_id, owner, relative, selector: binding(root, binding_id, owner, relative, selector)
    return {
        "schema_version": "2.0.0",
        "admission_timing": "selected-unit-at-task-session",
        "execution_policy": {
            "work_pack_id": "WP-CAL-TEN-L0",
            "route_policy": "automatic-in-scope",
            "allowed_routes": allowed_routes,
            "allowed_routes_digest": canonical_digest(allowed_routes),
            "automatic_decisions": ["internal-tool-selection", "capability-owner-routing", "reversible-local-default", "declared-fallback", "fresh-task-session-resumption"],
            "stop_decisions": contracts["stop_contract"]["classes"],
            "scope_source": "exact-work-pack-and-captured-frontier",
            "validation_policy": "owner-gates-remain-mandatory",
        },
        "audit_id": "wp-cal-ten-l0-one-shot-admission-20260808T164554Z",
        "repository_root": ".",
        "evidence_ceiling": "frozen-input-contractual-readiness",
        "classifier_version": "wpra-plan-once-v1",
        "objective_ref": binding(root, "cal-l0-objective", "invoke-plan", "work-pack/admission/L0-EXECUTION-CONTRACTS.json", "/objective"),
        "closure_receipt_refs": [binding(root, "cal-plan-selection-ready", "invoke-plan", "EXECUTION-ENTRY-VALIDATION.json", "/status")],
        "authority_bindings": {
            "canonical_authority_refs": [
                binding(root, "cal-work-pack", "invoke-plan", "EXECUTION-ENTRY.json", "/work_pack_id"),
                binding(root, "cal-l0-execution-contracts", "invoke-refresh", "work-pack/admission/L0-EXECUTION-CONTRACTS.json", "/work_pack_id"),
                binding(root, "cal-finite-frontier", "implementation-readiness", "work-pack/admission/FINITE-FRONTIER-CONTRACT.json", "/mode"),
                binding(root, "cal-closeout-targets", "invoke-refresh", "work-pack/shared/CLOSEOUT-TARGETS.json", "/work_pack_id"),
            ],
            "semantic_bindings": {
                "owner": binding(root, "cal-semantic-owner", "implementation-readiness", "work-pack/admission/L0-EXECUTION-CONTRACTS.json", "/units"),
                "material": binding(root, "cal-semantic-material", "task-session", "work-pack/admission/L0-EXECUTION-CONTRACTS.json", "/units"),
                "validation": binding(root, "cal-semantic-validation", "task-session", "work-pack/admission/L0-EXECUTION-CONTRACTS.json", "/units"),
                "receipt": binding(root, "cal-semantic-receipt", "task-session", "work-pack/admission/L0-EXECUTION-CONTRACTS.json", "/receipt_contracts"),
                "closeout": binding(root, "cal-semantic-closeout", "invoke-refresh", "work-pack/shared/CLOSEOUT-TARGETS.json", "/targets"),
            },
        },
        "execution_bindings": execution_bindings,
        "receipt_bindings": {
            "terminal_schema_ref": binding(root, "cal-terminal-receipt-schema", "task-session", "work-pack/admission/TASK-SESSION-RECEIPT.schema.json"),
            "semantic_validator_ref": binding(root, "cal-terminal-receipt-validator", "task-session", "work-pack/admission/L0-EXECUTION-CONTRACTS.json", "/receipt_contracts/terminal_validator"),
            "expected_receipt_refs": [binding(root, f"cal-expected-terminal-{index + 1:03d}", "task-session", "work-pack/admission/L0-EXECUTION-CONTRACTS.json", f"/units/{index}/terminal_receipt") for index in range(10)],
        },
        "closeout_bindings": [{
            "unit_id": unit["swu_id"],
            "allowed_delta_policy_ref": binding(root, f"cal-delta-policy-{index + 1:03d}", "invoke-refresh", "work-pack/shared/CLOSEOUT-TARGETS.json", "/allowed_delta_classes"),
            "owner_receipt_contract_ref": binding(root, f"cal-closeout-receipt-contract-{index + 1:03d}", "invoke-refresh", "work-pack/admission/CLOSEOUT-RECEIPT.schema.json"),
            "compensation": {"mode": "none", "rationale": "Task Session preserves prior valid bytes on failure; Invoke Refresh changes plan-only targets after a passing terminal receipt."},
        } for index, unit in enumerate(contracts["units"])],
        "runtime_binding": {"requested_task_session_execution_mode": "finite-frontier", "task_session_admission_receipt_ref": None},
        "status_receipt_refs": {
            "artifact_authored_status": {"value": "candidate", "owner_ref": "invoke-refresh", "receipt_ref": status_ref("cal-authored-candidate", "invoke-refresh", "work-pack/admission/L0-EXECUTION-CONTRACTS.json", "/schema_version")},
            "registry_released_status": {"value": "not-applicable", "owner_ref": "inventory", "receipt_ref": status_ref("cal-registry-not-applicable", "inventory", "work-pack/admission/L0-EXECUTION-CONTRACTS.json", "/authority_effect")},
            "mutation_runtime_ready_status": {"value": "pending-selection", "owner_ref": "implementation-readiness", "receipt_ref": status_ref("cal-runtime-pending", "implementation-readiness", "work-pack/admission/FINITE-FRONTIER-CONTRACT.json", "/approval/state")},
            "audit_verdict": {"value": "pending", "owner_ref": "work-pack-readiness-audit", "receipt_ref": status_ref("cal-audit-pending", "work-pack-readiness-audit", "work-pack/admission/FINITE-FRONTIER-CONTRACT.json", "/approval/state")},
        },
        "lifecycle_status_refs": {
            "plan_artifact_status": {"value": "selection-ready", "owner_ref": "invoke-plan", "receipt_ref": status_ref("cal-plan-artifact-selection-ready", "invoke-plan", "EXECUTION-ENTRY-VALIDATION.json", "/status")},
            "audit_status": {"value": "pending", "owner_ref": "work-pack-readiness-audit", "receipt_ref": status_ref("cal-audit-status-pending", "work-pack-readiness-audit", "work-pack/admission/FINITE-FRONTIER-CONTRACT.json", "/approval/state")},
            "approval_status": {"value": "unapproved", "owner_ref": "human-decision-gate", "receipt_ref": status_ref("cal-approval-unrequested", "human-decision-gate", "work-pack/admission/FINITE-FRONTIER-CONTRACT.json", "/approval/state")},
            "chain_status": {"value": "unarmed", "owner_ref": "implementation-readiness", "receipt_ref": status_ref("cal-chain-unarmed", "implementation-readiness", "work-pack/admission/FINITE-FRONTIER-CONTRACT.json", "/approval/state")},
        },
        "approval_policy": {
            "approval_owner_ref": "human-decision-gate",
            "decision_gate_receipt_ref": binding(root, "cal-decision-gate-state", "human-decision-gate", "work-pack/admission/FINITE-FRONTIER-CONTRACT.json", "/approval/state"),
            "run_budget": {"max_task_session_requests": 10},
            "risk_policy_ref": binding(root, "cal-stop-policy", "invoke-plan", "work-pack/admission/FINITE-FRONTIER-CONTRACT.json", "/stops"),
            "allowed_audit_verdicts": ["pass", "flag"],
            "allowed_flag_classes": ["observability-residue"],
        },
        "continuity_projection": {
            "cursor": "SWU-CAL-001",
            "completed_unit_receipt_refs": [],
            "joined_closeout_receipt_refs": [],
            "projected_next_successor": {
                "unit_id": "SWU-CAL-001",
                "canonical_successor_ref": binding(root, "cal-current-entry-frontier", "invoke-plan", "EXECUTION-ENTRY.json", "/frontier/0"),
                "projection_owner_ref": "invoke-refresh",
                "equivalence_validator_ref": binding(root, "cal-entry-equivalence-validator", "invoke-refresh", "work-pack/admission/validate-admission.py"),
                "continuation_router_verification_receipt_ref": binding(root, "cal-entry-validation-frontier", "implementation-readiness", "EXECUTION-ENTRY-VALIDATION.json", "/frontier/0"),
                "authority_effect": "none",
            },
        },
        "expected_source_snapshot_digest": None,
        "expected_semantic_digest": None,
    }


def validate(root: Path) -> dict:
    admission = root / "work-pack/admission"
    contracts = load(admission / "L0-EXECUTION-CONTRACTS.json")
    frontier = load(admission / "FINITE-FRONTIER-CONTRACT.json")
    entry = load(root / "EXECUTION-ENTRY.json")
    errors = []
    errors.extend(schema_errors(contracts, load(admission / "L0-EXECUTION-CONTRACTS.schema.json"), "execution-contracts"))
    errors.extend(schema_errors(frontier, load(admission / "FINITE-FRONTIER-CONTRACT.schema.json"), "finite-frontier"))

    units = contracts["units"]
    ids = [unit["swu_id"] for unit in units]
    if ids != EXPECTED_FRONTIER:
        errors.append(f"frontier order mismatch: {ids}")
    if frontier["frontier"] != EXPECTED_FRONTIER:
        errors.append("finite-frontier order does not match execution contracts")
    for index, unit in enumerate(units):
        if unit["dependencies"] != EXPECTED_DEPENDENCIES[unit["swu_id"]]:
            errors.append(f"{unit['swu_id']}: dependency contract mismatch")
        expected_successor = EXPECTED_FRONTIER[index + 1] if index < 9 else TERMINAL
        if unit["canonical_successors"] != [expected_successor]:
            errors.append(f"{unit['swu_id']}: canonical successor mismatch")
        material = set(unit["material_writes"])
        outputs = set(unit["execution_outputs"])
        allowed = set(unit["allowed_writes"])
        if material & outputs or material | outputs != allowed:
            errors.append(f"{unit['swu_id']}: allowed writes are not an exact disjoint partition")
        if unit["terminal_receipt"] not in outputs:
            errors.append(f"{unit['swu_id']}: terminal receipt is not an execution output")
        if unit["stop_classes"] != contracts["stop_contract"]["classes"]:
            errors.append(f"{unit['swu_id']}: stop classes drift from common contract")
        for runtime_ref in unit["runtime_refs"]:
            if runtime_ref not in contracts["runtime_contracts"]:
                errors.append(f"{unit['swu_id']}: unknown runtime {runtime_ref}")

    entry_frontier = entry.get("frontier", [])
    if entry_frontier != ["SWU-CAL-001"]:
        errors.append(f"one-unit EXECUTION-ENTRY projection not preserved: {entry_frontier}")
    if entry.get("execution_entry", {}).get("selected_unit") is not None:
        errors.append("EXECUTION-ENTRY unexpectedly selects a unit")

    return {
        "schema_version": "cyberalchemy-lab.admission-validation/v1",
        "work_pack_id": "WP-CAL-TEN-L0",
        "status": "pass" if not errors else "block",
        "validated_frontier": ids,
        "execution_entry_sha256": sha256(root / "EXECUTION-ENTRY.json"),
        "execution_entry_frontier": entry_frontier,
        "product_commands_run": 0,
        "authority_effect": "none",
        "errors": errors,
    }


def validate_terminal(root: Path, receipt_path: Path) -> dict:
    admission = root / "work-pack/admission"
    receipt = load(receipt_path)
    contracts = load(admission / "L0-EXECUTION-CONTRACTS.json")
    errors = schema_errors(receipt, load(admission / "TASK-SESSION-RECEIPT.schema.json"), "terminal-receipt")
    unit = next((item for item in contracts["units"] if item["swu_id"] == receipt.get("swu_id")), None)
    if unit is None:
        errors.append("terminal-receipt: SWU is outside the finite frontier")
    else:
        if receipt_path.as_posix() != unit["terminal_receipt"]:
            errors.append("terminal-receipt: path does not match the unit contract")
        touched = {item["path"] for item in receipt.get("touched_paths", [])}
        if not touched <= set(unit["allowed_writes"]):
            errors.append("terminal-receipt: touched path exceeds allowed writes")
        expected_commands = {item["command_id"] for item in unit["validation_contracts"]}
        observed_commands = {item["command_id"] for item in receipt.get("validation_results", [])}
        if observed_commands != expected_commands:
            errors.append("terminal-receipt: validation command set mismatch")
        if receipt.get("result") == "pass" and any(item.get("status") != "pass" for item in receipt.get("validation_results", [])):
            errors.append("terminal-receipt: pass result contains a non-passing validation")
    return {"schema_version": "cyberalchemy-lab.receipt-validation/v1", "receipt_kind": "task-session", "status": "pass" if not errors else "block", "authority_effect": "none", "errors": errors}


def validate_closeout(root: Path, receipt_path: Path) -> dict:
    admission = root / "work-pack/admission"
    receipt = load(receipt_path)
    targets = load(root / "work-pack/shared/CLOSEOUT-TARGETS.json")
    errors = schema_errors(receipt, load(admission / "CLOSEOUT-RECEIPT.schema.json"), "closeout-receipt")
    target = next((item for item in targets["targets"] if item["swu_id"] == receipt.get("swu_id")), None)
    if target is None:
        errors.append("closeout-receipt: SWU is outside the closeout targets")
    else:
        if receipt_path.as_posix() != target["expected_closeout_receipt"]:
            errors.append("closeout-receipt: path does not match the target contract")
        if not set(receipt.get("changed_paths", [])) <= set(target["target_inventory"]):
            errors.append("closeout-receipt: changed path exceeds target inventory")
        if receipt.get("successor") != target["successor"]:
            errors.append("closeout-receipt: successor mismatch")
        if not set(receipt.get("admitted_delta_classes", [])) <= set(targets["allowed_delta_classes"]):
            errors.append("closeout-receipt: delta class exceeds allowed policy")
        if receipt.get("status") == "pass" and any(item.get("status") != "pass" for item in receipt.get("validation", [])):
            errors.append("closeout-receipt: pass result contains a non-passing validation")
    return {"schema_version": "cyberalchemy-lab.receipt-validation/v1", "receipt_kind": "closeout", "status": "pass" if not errors else "block", "authority_effect": "none", "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan-root", type=Path, required=True)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--terminal-receipt", type=Path)
    modes.add_argument("--closeout-receipt", type=Path)
    modes.add_argument("--build-wpra-config", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.build_wpra_config:
        result = build_wpra_config(args.plan_root)
    elif args.terminal_receipt:
        result = validate_terminal(args.plan_root, args.terminal_receipt)
    elif args.closeout_receipt:
        result = validate_closeout(args.plan_root, args.closeout_receipt)
    else:
        result = validate(args.plan_root)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.build_wpra_config:
        return 0
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
