#!/usr/bin/env python3
"""Build the exact initial WP-ORRI-001 accepted-stream evidence."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPO = Path(__file__).resolve().parents[6]
RUN = Path(__file__).resolve().parents[1]
PLAN = REPO / "ops/development/2026-08-25-orchestrate-runtime-integrity/development/refinement-runs/20260825T185820Z-orchestrate-runtime-integrity-one-shot/stages/09-invoke-plan"
DECISION = PLAN.parents[1] / "decisions/ORRI-PLAN-ACCEPTANCE-001/OWNER-SELECTION-RECEIPT.json"
IR_ROOT = REPO / ".agents/skills/implementation-readiness"
WPRA_ROOT = REPO / ".agents/skills/work-pack-readiness-audit"
CHAIN_ROOT = REPO / ".agents/skills/task-session-until-blocker"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def write_json(relative: str, value: dict[str, Any]) -> Path:
    target = RUN / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def exact_ref(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(REPO).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }


def validate(value: Any, schema_path: Path, label: str) -> None:
    schema = read_json(schema_path)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(value),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        first = errors[0]
        location = "/".join(map(str, first.absolute_path)) or "<root>"
        raise ValueError(f"{label} invalid at {location}: {first.message}")


def verify_candidate() -> None:
    manifest = read_json(PLAN / "CANDIDATE-MANIFEST.json")
    for item in manifest["artifacts"]:
        path = REPO / item["path"]
        if exact_ref(path) != item:
            raise ValueError(f"accepted candidate drift: {item['path']}")
    if manifest["candidate_digest"] != "0f7b326607865b65bdd705b94258b395712b42ece32d1a897436a4240b366fb1":
        raise ValueError("accepted candidate digest differs")


def main() -> int:
    verify_candidate()
    sys.path.insert(0, str(IR_ROOT / "scripts"))
    sys.path.insert(0, str(WPRA_ROOT / "scripts"))
    readiness = load_module(
        "orri_readiness_execution", IR_ROOT / "scripts/readiness_execution.py"
    )
    contracts = load_module(
        "orri_execution_contracts", IR_ROOT / "scripts/execution_contracts.py"
    )
    selector = load_module(
        "orri_plan_selection", WPRA_ROOT / "scripts/verify_plan_selection.py"
    )

    audit_config_path = PLAN / "readiness/AUDIT-CONFIG-v2.json"
    audit_report_path = PLAN / "readiness/audit-output-final/work-pack-readiness-report-v2.json"
    manifest_path = PLAN / "readiness/audit-output-final/plan-semantic-manifest.json"
    handoff_path = PLAN / "readiness/audit-output-final/selection-handoff.json"
    contracts_path = PLAN / "EXECUTION-ENTRY-CLOSURE.json"
    work_pack_path = PLAN / "WORK-PACK.md"
    audit_config = read_json(audit_config_path)
    audit_report = read_json(audit_report_path)
    manifest = read_json(manifest_path)
    ready_frontier = list(manifest["ready_frontier"])
    policy = readiness.compile_execution_policy(audit_config, audit_report)
    frontier = list(policy["frontier"])
    binding_frontier = [
        binding["unit_id"] for binding in audit_config["execution_bindings"]
    ]
    if frontier != [f"SWU-ORRI-{index:03d}" for index in range(1, 10)]:
        raise ValueError("accepted policy frontier differs")
    if binding_frontier != frontier:
        raise ValueError("accepted execution bindings differ from the policy frontier")
    if not ready_frontier or frontier[: len(ready_frontier)] != ready_frontier:
        raise ValueError("WPRA ready frontier is not an ordered policy prefix")
    entry = readiness.compile_readiness_entry(policy, audit_report)
    source_invocation_id = "WP-ORRI-001-direct-execution-20260825"
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    binding = contracts.build_execution_intent_binding(
        policy,
        entry,
        source_invocation_id=source_invocation_id,
        created_at=created_at,
        execution_mode="finite-frontier",
    )
    binding_path = write_json("intent/execution-intent-binding.json", binding)

    initial = audit_config["execution_bindings"][0]
    selection_request = {
        "schemaVersion": "1.0.0",
        "manifestRef": exact_ref(manifest_path),
        "auditConfigPath": audit_config_path.relative_to(REPO).as_posix(),
        "taskId": initial["task_id"],
        "swuId": initial["swu_id"],
        "executionIntentBinding": readiness.selection_intent_projection(binding),
        "dependencyReceipts": [],
        "lifecycleEligibility": {
            "eligible": True,
            "state": "exact-candidate-accepted-and-direct-execution-requested",
            "evidenceRefs": [exact_ref(DECISION)],
        },
    }
    selection_request_path = write_json("selection/SWU-ORRI-001.request.json", selection_request)
    selection_receipt = selector.select_unit(
        selection_request,
        REPO,
        read_json(WPRA_ROOT / "schemas/selection-request.schema.json"),
        read_json(WPRA_ROOT / "schemas/plan-semantic-manifest.schema.json"),
        read_json(WPRA_ROOT / "schemas/audit-config-v2.schema.json"),
    )
    validate(selection_receipt, WPRA_ROOT / "schemas/selection-receipt.schema.json", "selection receipt")
    if selection_receipt["selectionVerdict"] != "select":
        raise ValueError(f"initial selection blocked: {selection_receipt['reasons']}")
    selection_receipt_path = write_json("selection/SWU-ORRI-001.receipt.json", selection_receipt)

    fast_request, fast_receipt = readiness.compile_plan_once_fast_entry(
        policy, audit_config, audit_report, selection_receipt, binding
    )
    fast_request_path = write_json("fast-entry/SWU-ORRI-001.request.json", fast_request)
    fast_receipt_path = write_json("fast-entry/SWU-ORRI-001.receipt.json", fast_receipt)

    epoch_approval = {
        "schema_version": "task-session-until-blocker.epoch-approval/v1",
        "approval_status": "approved",
        "approval_owner_ref": "user:WP-ORRI-001-direct-execution",
        "plan_epoch_id": manifest["plan_epoch_id"],
        "audit_projection_digest": audit_report["audit_projection_digest"],
        "canonical_semantic_digest": manifest["canonical_semantic_digest"],
        "source_snapshot_digest": manifest["source_snapshot_digest"],
        "manifest_ref": exact_ref(manifest_path),
        "audit_config_ref": exact_ref(audit_config_path),
        "execution_contracts_ref": exact_ref(contracts_path),
        "authority_effect": "chain-selection-only",
        "source_owner_selection_ref": exact_ref(DECISION),
        "source_execution_intent_ref": exact_ref(binding_path),
        "claim_ceiling": "Approves only deterministic selection inside the accepted WP-ORRI-001 finite stream; it grants no mutation, publication, promotion, deployment, or external-effect authority.",
    }
    epoch_approval_path = write_json("stream/epoch-approval.json", epoch_approval)

    chain_config = {
        "schema_version": "1.0.0",
        "chain_id": "WP-ORRI-001-accepted-stream",
        "repository_root": ".",
        "state_directory": (RUN / "stream/chain-state").relative_to(REPO).as_posix(),
        "scope_id": "WP-ORRI-001",
        "manifest_ref": exact_ref(manifest_path),
        "audit_report_ref": exact_ref(audit_report_path),
        "wpra_v2": {
            "audit_config_ref": exact_ref(audit_config_path),
            "execution_contracts_ref": exact_ref(contracts_path),
            "selection_handoff_ref": exact_ref(handoff_path),
            "initial_selection_request_ref": exact_ref(selection_request_path),
            "initial_selection_receipt_ref": exact_ref(selection_receipt_path),
        },
        "frontier_binding_mode": "accepted-policy-frontier",
        "audit_verdict": audit_report["verdict"],
        "audit_flags": list(audit_report["flags"]),
        "approved_epoch": {
            "epoch_id": manifest["plan_epoch_id"],
            "audit_projection_digest": audit_report["audit_projection_digest"],
            "canonical_semantic_digest": manifest["canonical_semantic_digest"],
            "source_snapshot_digest": manifest["source_snapshot_digest"],
            "decision_gate_approval_receipt_ref": exact_ref(epoch_approval_path),
            "approval_owner_ref": "user:WP-ORRI-001-direct-execution",
            "approval_status": "approved",
        },
        "finite_frontier": frontier,
        "run_budget": {"max_task_session_requests": len(frontier)},
        "risk_ceiling": "bounded-write",
        "allowed_task_session_flags": ["observability-residue"],
        "persistence": {"mode": "append-only-hash-chain", "collision_policy": "exclusive-create"},
        "compensation": {
            "mode": "none",
            "rationale": "Each Task Session owns exact reversible preimages and the stream stops before exposing a successor on failure.",
        },
    }
    validate(chain_config, CHAIN_ROOT / "schemas/chain-config.schema.json", "chain config")
    chain = load_module(
        "orri_task_session_until_blocker_chain",
        CHAIN_ROOT / "scripts/run_chain.py",
    )
    normalized_manifest, chain_preflight = chain.preflight(chain_config, REPO)
    if normalized_manifest is None or chain_preflight.get("terminal_code") != "CHAIN_PREFLIGHT_READY":
        raise ValueError(f"chain preflight blocked: {chain_preflight}")
    if normalized_manifest["canonical_plan_graph"]["finite_frontier"] != frontier:
        raise ValueError("normalized chain frontier differs from the accepted policy")
    if normalized_manifest["ready_frontier"] != ready_frontier:
        raise ValueError("normalized chain changed the WPRA ready frontier")
    if [item["unit_id"] for item in normalized_manifest["execution_bindings"]] != frontier:
        raise ValueError("normalized execution bindings do not cover the policy frontier")
    chain_config_path = write_json("stream/chain-config.json", chain_config)

    automatic = list(policy["automatic_decisions"])
    stop = list(policy["stop_decisions"])
    acceptance = {
        "schema_version": "task-session-until-blocker.finite-stream-execution-acceptance/v1",
        "approval_status": "approved",
        "supervisor_id": "WP-ORRI-001-supervisor",
        "scope_id": "WP-ORRI-001",
        "work_pack_id": policy["work_pack_id"],
        "work_pack_semantic_digest": policy["work_pack_semantic_digest"],
        "allowed_routes_digest": policy["allowed_routes_digest"],
        "source_invocation_id": source_invocation_id,
        "execution_mode": "finite-frontier",
        "captured_frontier": frontier,
        "chain_config_ref": exact_ref(chain_config_path),
        "fast_entry_request_ref": exact_ref(fast_request_path),
        "fast_entry_receipt_ref": exact_ref(fast_receipt_path),
        "max_task_session_requests": len(frontier),
        "risk_ceiling": "bounded-write",
        "automatic_decisions": automatic,
        "stop_decisions": stop,
        "authority_effect": "bounded-execution-only",
        "claim_ceiling": "Admits only nine ordered repository-local reversible Task Sessions with fresh per-unit mutation admission and owner closeout; no Git, publication, promotion, deployment, network, or external message authority.",
    }
    validate(acceptance, CHAIN_ROOT / "schemas/finite-stream-execution-acceptance.schema.json", "stream acceptance")
    acceptance_path = write_json("stream/finite-stream-execution-acceptance.json", acceptance)

    supervisor = {
        "schema_version": "1.1.0",
        "supervisor_id": "WP-ORRI-001-supervisor",
        "repository_root": ".",
        "state_directory": (RUN / "stream/supervisor-state").relative_to(REPO).as_posix(),
        "scope_id": "WP-ORRI-001",
        "work_pack_ref": exact_ref(work_pack_path),
        "owner_input_refs": [exact_ref(DECISION), exact_ref(binding_path)],
        "captured_frontier": frontier,
        "max_epochs": len(frontier),
        "risk_ceiling": "bounded-write",
        "allowed_task_session_flags": ["observability-residue"],
        "epoch_policy": {
            "mode": "accepted-finite-stream",
            "max_task_session_requests": len(frontier),
            "fresh_readiness_required": False,
            "approval_authority_effect": "bounded-execution-only",
        },
        "accepted_stream": {
            "chain_config_ref": exact_ref(chain_config_path),
            "execution_acceptance_ref": exact_ref(acceptance_path),
            "initial_fast_entry_request_ref": exact_ref(fast_request_path),
            "initial_fast_entry_receipt_ref": exact_ref(fast_receipt_path),
        },
        "persistence": {"mode": "append-only-hash-chain", "collision_policy": "exclusive-create"},
        "compensation": {
            "mode": "none",
            "rationale": "The supervisor performs no product mutation and stops at the first failed gate.",
        },
    }
    validate(supervisor, CHAIN_ROOT / "schemas/multi-epoch-supervisor-config.schema.json", "supervisor config")
    supervisor_path = write_json("stream/supervisor-config.json", supervisor)

    evidence_paths = [
        binding_path,
        selection_request_path,
        selection_receipt_path,
        fast_request_path,
        fast_receipt_path,
        epoch_approval_path,
        chain_config_path,
        acceptance_path,
        supervisor_path,
    ]
    evidence_manifest = {
        "schema_version": "orri.initial-stream-evidence-manifest/v1",
        "work_pack_id": "WP-ORRI-001",
        "candidate_digest": "0f7b326607865b65bdd705b94258b395712b42ece32d1a897436a4240b366fb1",
        "source_invocation_id": source_invocation_id,
        "artifacts": [exact_ref(path) for path in evidence_paths],
        "product_mutation_count": 0,
        "chain_preflight": chain_preflight,
        "authority_effect": "bounded-execution-only",
    }
    manifest_output = write_json("stream/initial-evidence-manifest.json", evidence_manifest)
    print(json.dumps({"status": "pass", "supervisor_config": exact_ref(supervisor_path), "evidence_manifest": exact_ref(manifest_output)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
