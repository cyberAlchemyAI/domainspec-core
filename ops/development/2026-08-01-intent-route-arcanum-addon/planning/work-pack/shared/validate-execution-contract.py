#!/usr/bin/env python3
"""Fail-closed structural validator for the IRO full-stream contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


COMMON_RUNTIME_OUTPUTS = [
    "CONTEXT-PACK.md", "CONTEXT-PACK.json", "closeout-preflight.json",
    "mutation-admission-request.json", "mutation-admission-receipt.json",
    "terminal-receipt.json", "closeout-sync-request.json",
    "closeout-owner-receipt.json", "continuation-route.json",
]
IRO_001_RUNTIME_OUTPUTS = [
    "OPTION-ADMISSIBILITY-REQUEST.json",
    "OPTION-ADMISSIBILITY-RECEIPT.json", "DECISION.json",
    "DECISION-SUMMARY.md", "decision-bundle.json",
]


EXPECTED = [
    "SWU-IRO-001", "SWU-IRO-002", "SWU-IRO-003", "SWU-IRO-004",
    "SWU-IRO-005", "SWU-IRO-006", "SWU-IRO-007", "SWU-IRO-008",
    "SWU-IRO-009", "SWU-IRO-VERIFY",
]
PAUSES = {
    "SWU-IRO-001", "SWU-IRO-003", "SWU-IRO-005",
    "SWU-IRO-006", "SWU-IRO-007", "SWU-IRO-008",
}


def validate(doc: dict, root: Path) -> list[str]:
    errors: list[str] = []
    if doc.get("schema_version") != "1.1.0":
        errors.append("schema_version must be 1.1.0")
    if doc.get("contract_id") != "IRO-FULL-STREAM":
        errors.append("contract_id must be IRO-FULL-STREAM")
    if doc.get("ordered_units") != EXPECTED:
        errors.append("ordered_units mismatch")
    if doc.get("execution_authority") != "none":
        errors.append("execution_authority must remain none")
    if doc.get("evidence_ceiling") != "frozen-input-contractual-readiness":
        errors.append("evidence ceiling mismatch")
    budgets = doc.get("budgets", {})
    if budgets != {"task_session_requests": 10, "repair_cycles_per_unit": 1, "simultaneous_helpers": 1, "browser_launches": 2, "network_calls": 0}:
        errors.append("budget contract mismatch")
    units = doc.get("units", [])
    if [unit.get("unit_id") for unit in units] != EXPECTED:
        errors.append("unit order mismatch")
        return errors
    allowlist = doc.get("capability_allowlist", {})
    for index, unit in enumerate(units):
        unit_id = unit["unit_id"]
        expected_dependencies = [] if index == 0 else [EXPECTED[index - 1]]
        expected_successor = "__complete__" if index == len(EXPECTED) - 1 else EXPECTED[index + 1]
        if unit.get("depends_on") != expected_dependencies:
            errors.append(f"{unit_id}: dependencies mismatch")
        if unit.get("successor") != expected_successor:
            errors.append(f"{unit_id}: successor mismatch")
        if len(unit.get("coordinator_outputs", [])) != 2:
            errors.append(f"{unit_id}: exactly two coordinator outputs required")
        expected_runtime = [f"{unit_id}/{name}" for name in COMMON_RUNTIME_OUTPUTS]
        if unit_id == "SWU-IRO-001":
            expected_runtime.extend(f"{unit_id}/{name}" for name in IRO_001_RUNTIME_OUTPUTS)
        if unit.get("runtime_outputs") != expected_runtime:
            errors.append(f"{unit_id}: runtime output contract mismatch")
        expected_cursor = f".arcanum/task-session/continuity/IRO-FULL-STREAM-<epoch-id>-{unit_id}.json"
        if unit.get("continuity_cursor") != expected_cursor:
            errors.append(f"{unit_id}: continuity cursor mismatch")
        if unit_id == "SWU-IRO-001" and unit.get("owner_material_scope") != []:
            errors.append("SWU-IRO-001: output-only unit must not declare owner material")
        if unit_id in PAUSES and not unit.get("pause_before_successor"):
            errors.append(f"{unit_id}: required pause missing")
        if unit_id not in PAUSES and unit.get("pause_before_successor") is not None:
            errors.append(f"{unit_id}: unexpected pause")
        if not unit.get("validation_commands"):
            errors.append(f"{unit_id}: validation commands missing")
        task_ref = unit.get("task_ref", "")
        if not task_ref or not (root / task_ref).is_file():
            errors.append(f"{unit_id}: task_ref missing: {task_ref}")
        for capability in unit.get("capabilities", []):
            if unit_id not in allowlist.get(capability, []):
                errors.append(f"{unit_id}: capability not allowlisted: {capability}")
    schemas = doc.get("receipt_schemas", {})
    for name in ("terminal", "closeout_owner", "decision_bundle", "goal_start_approval", "closeout_preflight", "closeout_sync_request", "mutation_admission_request", "mutation_admission_receipt", "continuation_route", "continuity_cursor", "chain_config", "chain_transition"):
        ref = schemas.get(name, "")
        if not ref or not (root / ref).is_file():
            errors.append(f"receipt schema missing: {name}: {ref}")
    runtime = doc.get("runtime_evidence_contract", {})
    if runtime.get("per_unit_outputs") != COMMON_RUNTIME_OUTPUTS:
        errors.append("runtime evidence common output mismatch")
    if runtime.get("iro_001_additional_outputs") != IRO_001_RUNTIME_OUTPUTS:
        errors.append("IRO-001 additional output mismatch")
    chain = doc.get("chain_runtime", {})
    if len(chain.get("transition_receipts", [])) != len(EXPECTED):
        errors.append("chain transition receipt count mismatch")
    return errors


def self_test() -> int:
    minimal = {
        "schema_version": "1.0.0",
        "contract_id": "IRO-FULL-STREAM",
        "ordered_units": [],
        "execution_authority": "none",
        "evidence_ceiling": "frozen-input-contractual-readiness",
        "budgets": {},
        "units": [],
    }
    errors = validate(minimal, Path("."))
    if "ordered_units mismatch" not in errors or "unit order mismatch" not in errors:
        print("SELF_TEST=fail")
        return 1
    print("SELF_TEST=pass")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--contract")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    root = Path(args.root).resolve()
    contract = Path(args.contract) if args.contract else root / "ops/development/2026-08-01-intent-route-arcanum-addon/planning/work-pack/shared/EXECUTION-CONTRACT.json"
    doc = json.loads(contract.read_text(encoding="utf-8"))
    errors = validate(doc, root)
    if errors:
        print("VALIDATION=block")
        for error in errors:
            print(f"BLOCK={error}")
        return 1
    print("VALIDATION=pass")
    print(f"CONTRACT={contract}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
