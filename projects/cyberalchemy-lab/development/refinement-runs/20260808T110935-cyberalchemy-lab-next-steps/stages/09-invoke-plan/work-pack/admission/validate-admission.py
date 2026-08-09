#!/usr/bin/env python3
"""Validate WP-CAL-TEN-L0 admission contracts without executing product work."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

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
                "expected_receipt": unit["attempt_receipt_root"],
            },
            {
                "route_id": f"closeout-cal-{index + 1:03d}",
                "frontier_swu": swu_id,
                "capability": "invoke",
                "mode": "refresh-apply-approved",
                "target": f"{swu_id}-closeout",
                "write_scope": target_by_unit[swu_id]["target_inventory"],
                "effect_class": "repository-local-reversible",
                "required_inputs": [unit["terminal_receipt_template"], f"{PLAN_PREFIX}/work-pack/shared/CLOSEOUT-CONTRACT.md", f"{PLAN_PREFIX}/work-pack/shared/CLOSEOUT-TARGETS.json#/targets/{index}"],
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
            "expected_receipt_refs": [binding(root, f"cal-expected-terminal-root-{index + 1:03d}", "task-session", "work-pack/admission/L0-EXECUTION-CONTRACTS.json", f"/units/{index}/attempt_receipt_root") for index in range(10)],
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
                "continuation_router_verification_receipt_ref": binding(root, "cal-entry-validation-frontier", "implementation-readiness", "EXECUTION-ENTRY-VALIDATION.json", "/execution_entry_frontier/0"),
                "authority_effect": "none",
            },
        },
        "expected_source_snapshot_digest": None,
        "expected_semantic_digest": None,
    }


def declared_path_contains(scope: str, path: str) -> bool:
    scope_path = PurePosixPath(scope)
    target_path = PurePosixPath(path)
    return target_path == scope_path or scope_path in target_path.parents


def attempt_leaf(swu_id: str, attempt_id: str) -> str | None:
    prefix = f"WP-CAL-TEN-L0/{swu_id}/"
    if not attempt_id.startswith(prefix):
        return None
    leaf = attempt_id[len(prefix):]
    if not re.fullmatch(r"\d{8}T\d{6}Z-[A-Za-z0-9][A-Za-z0-9._-]*", leaf):
        return None
    return leaf


def expected_terminal_path(unit: dict, receipt: dict) -> str | None:
    leaf = attempt_leaf(unit["swu_id"], receipt.get("attempt_id", ""))
    if leaf is None:
        return None
    return f"{unit['attempt_receipt_root']}/{leaf}.json"


def projected_entry(root: Path, successor: str | None) -> dict:
    entry = load(root / "EXECUTION-ENTRY.json")
    config = build_wpra_config(root)
    routes = [
        route for route in config["execution_policy"]["allowed_routes"]
        if route["frontier_swu"] == successor
    ] if successor is not None else []
    entry["frontier"] = [successor] if successor is not None else []
    entry["execution_policy"]["allowed_routes"] = routes
    entry["execution_policy"]["allowed_routes_digest"] = canonical_digest(routes)
    entry["execution_entry"] = {
        "state": "selection-ready" if successor is not None else "complete",
        "selected_unit": None,
        "route_id": None,
        "next_owner": "implementation-readiness:execute" if successor is not None else "none",
    }
    return entry


def entry_projection_errors(root: Path, entry: dict) -> list[str]:
    frontier = entry.get("frontier", [])
    if not isinstance(frontier, list) or len(frontier) > 1:
        return [f"one-unit EXECUTION-ENTRY projection not preserved: {frontier}"]
    if frontier and frontier[0] not in EXPECTED_FRONTIER:
        return [f"EXECUTION-ENTRY frontier is outside L0: {frontier}"]
    successor = frontier[0] if frontier else None
    expected = projected_entry(root, successor)
    if canonical_digest(entry) != canonical_digest(expected):
        return ["EXECUTION-ENTRY does not equal the current one-unit continuation projection"]
    return []


def projection_record(root: Path, successor: str | None) -> dict:
    entry = projected_entry(root, successor)
    return {
        "path": f"{PLAN_PREFIX}/EXECUTION-ENTRY.json",
        "frontier": entry["frontier"],
        "entry_state": entry["execution_entry"]["state"],
        "selected_unit": None,
        "route_id": None,
        "allowed_routes_digest": entry["execution_policy"]["allowed_routes_digest"],
        "canonical_projection_digest": canonical_digest(entry),
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
        if unit["attempt_receipt_root"] not in outputs:
            errors.append(f"{unit['swu_id']}: execution outputs must include the immutable attempt receipt root")
        if unit["swu_id"] != "SWU-CAL-010" and outputs != {unit["attempt_receipt_root"]}:
            errors.append(f"{unit['swu_id']}: execution output inventory exceeds its immutable attempt receipt root")
        if unit["terminal_receipt_template"] != f"{unit['attempt_receipt_root']}/<attempt-leaf>.json":
            errors.append(f"{unit['swu_id']}: terminal receipt template drift")
        for runtime_ref in unit["runtime_refs"]:
            if runtime_ref not in contracts["runtime_contracts"]:
                errors.append(f"{unit['swu_id']}: unknown runtime {runtime_ref}")

    errors.extend(entry_projection_errors(root, entry))
    return {
        "schema_version": "cyberalchemy-lab.admission-validation/v1",
        "work_pack_id": "WP-CAL-TEN-L0",
        "status": "pass" if not errors else "block",
        "validated_frontier": ids,
        "execution_entry_sha256": sha256(root / "EXECUTION-ENTRY.json"),
        "execution_entry_frontier": entry.get("frontier", []),
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
        legacy = unit.get("legacy_terminal_receipt")
        legacy_match = legacy is not None and receipt_path.as_posix() == legacy["path"]
        if legacy_match:
            if sha256(receipt_path) != legacy["sha256"] or receipt.get("result") != legacy["result"]:
                errors.append("terminal-receipt: preserved legacy receipt identity mismatch")
        else:
            expected_path = expected_terminal_path(unit, receipt)
            if expected_path is None or receipt_path.as_posix() != expected_path:
                errors.append("terminal-receipt: path does not match the immutable attempt template")
            if receipt.get("attempt_receipt_path") != expected_path:
                errors.append("terminal-receipt: self-address does not match the immutable attempt template")
        touched = {item["path"] for item in receipt.get("touched_paths", [])}
        if not all(any(declared_path_contains(scope, path) for scope in unit["allowed_writes"]) for path in touched):
            errors.append("terminal-receipt: touched path exceeds allowed write scope")
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
    contracts = load(admission / "L0-EXECUTION-CONTRACTS.json")
    targets = load(root / "work-pack/shared/CLOSEOUT-TARGETS.json")
    errors = schema_errors(receipt, load(admission / "CLOSEOUT-RECEIPT.schema.json"), "closeout-receipt")
    target = next((item for item in targets["targets"] if item["swu_id"] == receipt.get("swu_id")), None)
    unit = next((item for item in contracts["units"] if item["swu_id"] == receipt.get("swu_id")), None)
    if target is None or unit is None:
        errors.append("closeout-receipt: SWU is outside the closeout targets")
    else:
        if receipt_path.as_posix() != target["expected_closeout_receipt"]:
            errors.append("closeout-receipt: path does not match the target contract")
        if not set(receipt.get("changed_paths", [])) <= set(target["target_inventory"]):
            errors.append("closeout-receipt: changed path exceeds target inventory")
        required_changed = {f"{PLAN_PREFIX}/EXECUTION-ENTRY.json", f"{PLAN_PREFIX}/EXECUTION-ENTRY-VALIDATION.json"}
        if not required_changed <= set(receipt.get("changed_paths", [])):
            errors.append("closeout-receipt: successor projection and its validation must both be recorded")
        if receipt.get("successor") != target["successor"]:
            errors.append("closeout-receipt: successor mismatch")
        if not set(receipt.get("admitted_delta_classes", [])) <= set(targets["allowed_delta_classes"]):
            errors.append("closeout-receipt: delta class exceeds allowed policy")
        if receipt.get("status") == "pass" and any(item.get("status") != "pass" for item in receipt.get("validation", [])):
            errors.append("closeout-receipt: pass result contains a non-passing validation")
        terminal_relative = receipt.get("execution_receipt", {}).get("path", "")
        terminal_path = Path.cwd() / terminal_relative
        if not terminal_relative or not terminal_path.is_file():
            errors.append("closeout-receipt: execution receipt is missing from the repository root")
        elif sha256(terminal_path) != receipt["execution_receipt"]["sha256"]:
            errors.append("closeout-receipt: execution receipt digest mismatch")
        elif validate_terminal(root, Path(terminal_relative))["status"] != "pass":
            errors.append("closeout-receipt: execution receipt does not pass terminal validation")
        expected_projection = projection_record(root, target["successor"])
        if receipt.get("execution_entry_projection") != expected_projection:
            errors.append("closeout-receipt: immutable successor projection binding mismatch")
        if not any(item.get("check_id") == "current-entry-projection" and item.get("status") == "pass" for item in receipt.get("validation", [])):
            errors.append("closeout-receipt: missing current-entry-projection validation")
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
