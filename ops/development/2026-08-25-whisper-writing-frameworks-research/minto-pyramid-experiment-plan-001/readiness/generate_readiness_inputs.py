#!/usr/bin/env python3
"""Generate exact plan inventory, execution entry, and WPRA v2 input bytes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


SCRIPT = Path(__file__).resolve()
PLAN_ROOT = SCRIPT.parents[1]


def find_repository_root() -> Path:
    for candidate in SCRIPT.parents:
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("repository root not found")


REPOSITORY_ROOT = find_repository_root()
RESEARCH_ROOT = PLAN_ROOT.parent
EXPERIMENT_ROOT = RESEARCH_ROOT / "minto-pyramid-experiment-001"
WORK_PACK_ID = "WP-MPX-001"
FRONTIER = ["SWU-MPX-001", "SWU-MPX-002", "SWU-MPX-003"]


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPOSITORY_ROOT.resolve()).as_posix()


def exact(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "path": relative(path),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "size_bytes": len(payload),
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def binding(
    binding_id: str, owner_ref: str, artifact: Path, selector: str
) -> dict[str, Any]:
    return {
        "binding_id": binding_id,
        "owner_ref": owner_ref,
        "artifact_ref": exact(artifact),
        "selector": selector,
    }


def opaque_binding(
    binding_id: str, owner_ref: str, artifact: Path
) -> dict[str, Any]:
    return {
        "binding_id": binding_id,
        "owner_ref": owner_ref,
        "binding_mode": "opaque-exact-artifact",
        "artifact_ref": exact(artifact),
    }


def unit_paths(unit_id: str) -> tuple[list[str], list[str], list[str]]:
    suffix = unit_id.rsplit("-", 1)[-1]
    material_by_suffix = {
        "001": [EXPERIMENT_ROOT / "case/EXPERIMENT-CASE.json"],
        "002": [EXPERIMENT_ROOT / "mechanical/MECHANICAL-VALIDATION.json"],
        "003": [
            EXPERIMENT_ROOT / "review/BLINDING-COMMITMENT.json",
            EXPERIMENT_ROOT / "review/BLINDED-REVIEW-PACKET.json",
            EXPERIMENT_ROOT / "review/HUMAN-REVIEW-RESPONSE.json",
            EXPERIMENT_ROOT / "review/HUMAN-REVIEW-AND-WITNESS.json",
        ],
    }
    material = [relative(path) for path in material_by_suffix[suffix]]
    task_session_outputs = [
        relative(EXPERIMENT_ROOT / f"precloseout/{unit_id}.json"),
        relative(EXPERIMENT_ROOT / f"receipts/{unit_id}.task-session.json"),
    ]
    invoke_outputs = [
        relative(EXPERIMENT_ROOT / f"closeouts/{unit_id}.invoke-refresh.json")
    ]
    return material, task_session_outputs, invoke_outputs


def task_path(unit_id: str) -> Path:
    return {
        "SWU-MPX-001": PLAN_ROOT / "work-pack/tasks/TASK-MPX-001-CASE.md",
        "SWU-MPX-002": PLAN_ROOT / "work-pack/tasks/TASK-MPX-002-MECHANICS.md",
        "SWU-MPX-003": PLAN_ROOT / "work-pack/tasks/TASK-MPX-003-REVIEW.md",
    }[unit_id]


def predecessor_closeout(unit_id: str) -> str | None:
    predecessor = {
        "SWU-MPX-001": None,
        "SWU-MPX-002": "SWU-MPX-001",
        "SWU-MPX-003": "SWU-MPX-002",
    }[unit_id]
    if predecessor is None:
        return None
    return relative(EXPERIMENT_ROOT / f"closeouts/{predecessor}.invoke-refresh.json")


def build_routes() -> list[dict[str, Any]]:
    shared_inputs = [
        relative(PLAN_ROOT / "WORK-PACK.md"),
        relative(PLAN_ROOT / "work-pack/SWU-MANIFEST.json"),
        relative(PLAN_ROOT / "work-pack/shared/VALIDATION-CONTRACTS.json"),
        relative(PLAN_ROOT / "work-pack/shared/CLOSEOUT-CONTRACTS.json"),
        relative(
            PLAN_ROOT
            / "work-pack/validators/validate_minto_experiment.py"
        ),
    ]
    routes: list[dict[str, Any]] = []
    for unit_id in FRONTIER:
        material, task_session_outputs, _ = unit_paths(unit_id)
        required_inputs = [*shared_inputs, relative(task_path(unit_id))]
        if unit_id in {"SWU-MPX-002", "SWU-MPX-003"}:
            required_inputs.append(
                relative(EXPERIMENT_ROOT / "case/EXPERIMENT-CASE.json")
            )
        if unit_id == "SWU-MPX-003":
            required_inputs.append(
                relative(
                    EXPERIMENT_ROOT
                    / "mechanical/MECHANICAL-VALIDATION.json"
                )
            )
        predecessor = predecessor_closeout(unit_id)
        if predecessor is not None:
            required_inputs.append(predecessor)
        routes.append(
            {
                "route_id": f"task-session:{unit_id}",
                "frontier_swu": unit_id,
                "capability": "task-session",
                "mode": "execute",
                "target": relative(task_path(unit_id)),
                "write_scope": [*material, *task_session_outputs],
                "effect_class": "repository-local-reversible",
                "required_inputs": required_inputs,
                "expected_receipt": relative(
                    EXPERIMENT_ROOT / f"receipts/{unit_id}.task-session.json"
                ),
            }
        )
    return routes


def build_execution_entry(routes: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "arcanum.work-pack-execution-entry/v1",
        "work_pack_id": WORK_PACK_ID,
        "admission_timing": "selected-unit-at-task-session",
        "frontier": FRONTIER,
        "execution_policy": {
            "route_policy": "automatic-in-scope",
            "allowed_routes": routes,
            "allowed_routes_digest": canonical_digest(routes),
            "digest_algorithm": (
                "sha256 of RFC8785-compatible canonical JSON for allowed_routes"
            ),
            "automatic_decisions": [
                "internal-tool-selection",
                "capability-owner-routing",
                "reversible-local-default",
                "fresh-task-session-resumption",
            ],
            "stop_decisions": [
                "product-or-semantic-choice",
                "scope-expansion",
                "destructive-or-irreversible-effect",
                "credentials-or-secret-access",
                "external-message-or-network-effect",
                "cost-policy-or-risk-acceptance",
                "authority-promotion-publication-deployment",
                "failed-acceptance-critical-validation",
            ],
            "scope_source": "exact-work-pack-and-captured-frontier",
            "validation_policy": "owner-gates-remain-mandatory",
        },
        "execution_entry": {
            "state": "blocked",
            "selected_unit": None,
            "route_id": None,
            "next_owner": None,
        },
        "pre_execution_owner_prerequisite": {
            "status": "unsatisfied",
            "required": [
                {
                    "prerequisite_id": "exact-final-plan-acceptance",
                    "owner": "repository-owner",
                    "receipt_ref": None,
                },
                {
                    "prerequisite_id": "fresh-direct-execution-intent",
                    "owner": "repository-owner",
                    "receipt_ref": None,
                },
            ],
            "candidate_identity_receipt": exact(
                RESEARCH_ROOT
                / "minto-pyramid-experiment-decision-001/DECISION-RECEIPT.json"
            ),
            "candidate_identity_authority_limit": (
                "Selects Minto Pyramid only; does not accept this plan or "
                "authorize execution."
            ),
        },
        "continuation_rule": (
            "Only an exact joined Invoke closeout activates the unique declared "
            "successor; SWU-MPX-003 additionally stops for genuine human review."
        ),
        "authority_effect": "none",
    }


def plan_inventory_paths() -> list[Path]:
    paths = [
        PLAN_ROOT / "PLANNING-CONTEXT.md",
        PLAN_ROOT / "INVENTORY-LOOKUP.json",
        PLAN_ROOT / "TEMPLATE-SELECTION.json",
        PLAN_ROOT / "IMPLEMENTATION-LAYERING.md",
        PLAN_ROOT / "IMPLEMENTATION-PLAN.md",
        PLAN_ROOT / "WORK-PACK.md",
        PLAN_ROOT / "EXECUTION-PACK.md",
        PLAN_ROOT / "DISPATCH-TECHNIQUE-TRACE.json",
        PLAN_ROOT / "PLAN-DISTILL-VALIDATION.json",
        PLAN_ROOT / "EXECUTION-ENTRY.json",
        PLAN_ROOT / "work-pack/SWU-MANIFEST.json",
        PLAN_ROOT / "work-pack/shared/VALIDATION-CONTRACTS.json",
        PLAN_ROOT / "work-pack/shared/CLOSEOUT-CONTRACTS.json",
        PLAN_ROOT / "work-pack/validators/validate_minto_experiment.py",
        PLAN_ROOT / "readiness/generate_readiness_inputs.py",
        PLAN_ROOT / "work-pack/tasks/TASK-MPX-001-CASE.md",
        PLAN_ROOT / "work-pack/tasks/TASK-MPX-002-MECHANICS.md",
        PLAN_ROOT / "work-pack/tasks/TASK-MPX-003-REVIEW.md",
        PLAN_ROOT / "work-pack/waves/W0-CASE.md",
        PLAN_ROOT / "work-pack/waves/W1-MECHANICS.md",
        PLAN_ROOT / "work-pack/waves/W2-REVIEW.md",
    ]
    missing = [relative(path) for path in paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing final plan inputs: {missing}")
    return paths


def build_plan_inventory() -> dict[str, Any]:
    artifacts = [exact(path) for path in plan_inventory_paths()]
    return {
        "schema_version": "invoke.plan-artifact-inventory.v1",
        "work_pack_id": WORK_PACK_ID,
        "status": "frozen",
        "artifacts": artifacts,
        "artifact_count": len(artifacts),
        "inventory_digest": canonical_digest(artifacts),
        "authority_effect": "none",
    }


def build_audit_bindings(plan_inventory: dict[str, Any]) -> dict[str, Any]:
    expected_receipts = {
        unit: {
            "task_id": {
                "SWU-MPX-001": "TASK-MPX-001-CASE",
                "SWU-MPX-002": "TASK-MPX-002-MECHANICS",
                "SWU-MPX-003": "TASK-MPX-003-REVIEW",
            }[unit],
            "swu_id": unit,
            "result": "pass-or-block",
            "expected_path": relative(
                EXPERIMENT_ROOT / f"receipts/{unit}.task-session.json"
            ),
        }
        for unit in FRONTIER
    }
    closeout_contracts = json.loads(
        (PLAN_ROOT / "work-pack/shared/CLOSEOUT-CONTRACTS.json").read_text(
            encoding="utf-8"
        )
    )
    return {
        "schema_version": "invoke.plan-audit-bindings.v1",
        "objective": {
            "work_pack_id": WORK_PACK_ID,
            "target": "minto-pyramid-experiment-001",
            "decision": (
                "Test the single declared-governing-point-support-hierarchy "
                "decision against support-association-not-declared and produce "
                "one candidate-specific witness without reader or integration "
                "claims."
            ),
            "plan_acceptance_owner": "repository-owner",
            "accepted_candidate": "minto-pyramid",
        },
        "plan_artifacts": plan_inventory,
        "material_policy": {
            "admission_timing": "selected-unit-at-task-session",
            "future_material_is_pending_selection": True,
            "executor_writes_exclude_lifecycle_owner_targets": True,
        },
        "validation_policy": {
            "mechanical_and_human_checks_separate": True,
            "actual_predecessor_bytes_recomputed": True,
            "receipt_self_attestation_insufficient": True,
            "blinding_commitment_chronology_required": True,
            "failed_acceptance_validation_stops": True,
            "reader_outcomes_excluded": True,
        },
        "receipt_contract": {
            "terminal_owner": "task-session",
            "closeout_owner": "invoke",
            "append_only": True,
            "authority_effect": "none",
        },
        "closeout_contract": {
            "owner": "invoke",
            "mode": "refresh:apply-approved",
            "allowed_delta_classes": closeout_contracts[
                "allowed_delta_classes"
            ],
            "contracts": closeout_contracts["contracts"],
        },
        "expected_receipts": expected_receipts,
        "status": {
            "artifact_authored": "pass",
            "registry_released": "not-granted",
            "mutation_runtime_ready": "false",
            "audit_verdict": "pending",
            "plan_artifact": "pass",
            "audit": "not-run",
            "approval": "unapproved",
            "chain": "not-started",
        },
        "risk_policy": {
            "maximum": "bounded-write",
            "network": "forbidden",
            "public_or_private": "private",
        },
        "decision": {
            "candidate_selection": "minto-pyramid",
            "plan_acceptance": "pending",
        },
        "continuity": {
            "cursor": "SWU-MPX-001",
            "equivalence": "exact-semantic-unit-contract",
            "verification": "SWU-MPX-001",
            "status": "plan-only-not-executed",
        },
        "authority_effect": "none",
    }


def build_config(
    routes: list[dict[str, Any]],
    bindings_path: Path,
    inventory_path: Path,
) -> dict[str, Any]:
    decision_path = RESEARCH_ROOT / (
        "minto-pyramid-experiment-decision-001/DECISION-RECEIPT.json"
    )
    closeout_path = RESEARCH_ROOT / (
        "matrix-repair-continuation-001/CLOSEOUT-RECEIPT.json"
    )
    validation_contracts = json.loads(
        (PLAN_ROOT / "work-pack/shared/VALIDATION-CONTRACTS.json").read_text(
            encoding="utf-8"
        )
    )
    closeout_contracts = json.loads(
        (PLAN_ROOT / "work-pack/shared/CLOSEOUT-CONTRACTS.json").read_text(
            encoding="utf-8"
        )
    )
    schemas = {
        "precloseout": REPOSITORY_ROOT
        / ".agents/skills/task-session/schemas/precloseout-execution-receipt.schema.json",
        "owner": REPOSITORY_ROOT
        / ".agents/skills/invoke/schemas/precloseout-refresh-closeout-receipt.schema.json",
        "terminal": REPOSITORY_ROOT
        / ".agents/skills/task-session/schemas/governance-terminal-receipt.schema.json",
        "continuity": REPOSITORY_ROOT
        / ".agents/skills/task-session/continuity.schema.json",
        "router": REPOSITORY_ROOT
        / ".agents/skills/continuation-router/schemas/continuation-route.schema.json",
    }
    semantic_validator = REPOSITORY_ROOT / (
        "arcanum/arcana/task-session/scripts/plan-once-material-controller.py"
    )
    bindings = lambda name, owner, selector: binding(
        name, owner, bindings_path, selector
    )
    execution_bindings = []
    for index, unit_id in enumerate(FRONTIER):
        material, task_session_outputs, _ = unit_paths(unit_id)
        execution_bindings.append(
            {
                "unit_id": unit_id,
                "task_id": {
                    "SWU-MPX-001": "TASK-MPX-001-CASE",
                    "SWU-MPX-002": "TASK-MPX-002-MECHANICS",
                    "SWU-MPX-003": "TASK-MPX-003-REVIEW",
                }[unit_id],
                "swu_id": unit_id,
                "lifecycle_owner": "task-session",
                "authority_class": "private",
                "publication_class": "private",
                "dependencies": [] if index == 0 else [FRONTIER[index - 1]],
                "canonical_successors": (
                    [FRONTIER[index + 1]]
                    if index + 1 < len(FRONTIER)
                    else ["__complete__"]
                ),
                "command": {
                    "argv": [
                        "task-session",
                        "--from",
                        relative(PLAN_ROOT / "WORK-PACK.md"),
                        "--task",
                        {
                            "SWU-MPX-001": "TASK-MPX-001-CASE",
                            "SWU-MPX-002": "TASK-MPX-002-MECHANICS",
                            "SWU-MPX-003": "TASK-MPX-003-REVIEW",
                        }[unit_id],
                        "--swu",
                        unit_id,
                        "--runtime",
                        "codex",
                    ],
                    "cwd": ".",
                    "risk_class": "bounded-write",
                },
                "validation_contracts": validation_contracts["units"][index][
                    "commands"
                ],
                "material_writes": material,
                "execution_outputs": task_session_outputs,
                "allowed_writes": [*material, *task_session_outputs],
                "attempt_contract": {
                    "id_policy": "attempt-id-equals-fresh-task-session-run-id",
                    "collision_policy": (
                        "all-declared-targets-absent-or-exact-separately-accepted-baseline"
                    ),
                    "success_teardown": (
                        "retain-material-postimage-terminal-receipt-and-refresh-closeout"
                    ),
                    "failure_teardown": (
                        "retain-first-failure-and-terminal-block-receipt-without-status-masking"
                    ),
                },
                "material_package": {
                    "package_ref": None,
                    "producer_owner_ref": "task-session",
                    "producer_receipt_ref": None,
                    "schema_ref": None,
                    "declared_sha256": None,
                    "target_inventory_ref": None,
                },
                "byte_baselines": [],
            }
        )
    task_closeouts = []
    for unit_id in FRONTIER:
        task_closeouts.append(
            {
                "unit_id": unit_id,
                "receipt_profile": "precloseout-execution-v1",
                "precloseout_execution_schema_ref": binding(
                    f"precloseout-schema-{unit_id}",
                    "task-session",
                    schemas["precloseout"],
                    "",
                ),
                "expected_owner_receipt_schema_ref": binding(
                    f"owner-schema-{unit_id}",
                    "invoke",
                    schemas["owner"],
                    "",
                ),
                "declared_owner_receipt_schema_identity": (
                    "invoke.precloseout-refresh-closeout-receipt.v1"
                ),
                "final_terminal_schema_ref": binding(
                    f"terminal-schema-{unit_id}",
                    "task-session",
                    schemas["terminal"],
                    "",
                ),
                "continuity_schema_ref": binding(
                    f"continuity-schema-{unit_id}",
                    "task-session",
                    schemas["continuity"],
                    "",
                ),
                "continuation_router_schema_ref": binding(
                    f"router-schema-{unit_id}",
                    "continuation-router",
                    schemas["router"],
                    "",
                ),
            }
        )
    audit_policy = {
        "work_pack_id": WORK_PACK_ID,
        "route_policy": "automatic-in-scope",
        "allowed_routes": routes,
        "allowed_routes_digest": canonical_digest(routes),
        "automatic_decisions": [
            "internal-tool-selection",
            "capability-owner-routing",
            "reversible-local-default",
            "fresh-task-session-resumption",
        ],
        "stop_decisions": [
            "product-or-semantic-choice",
            "scope-expansion",
            "destructive-or-irreversible-effect",
            "credentials-or-secret-access",
            "external-message-or-network-effect",
            "cost-policy-or-risk-acceptance",
            "authority-promotion-publication-deployment",
            "failed-acceptance-critical-validation",
        ],
        "scope_source": "exact-work-pack-and-captured-frontier",
        "validation_policy": "owner-gates-remain-mandatory",
    }
    return {
        "schema_version": "2.0.0",
        "audit_id": "WP-MPX-001-READINESS-20260825T204202Z",
        "repository_root": ".",
        "evidence_ceiling": "frozen-input-contractual-readiness",
        "classifier_version": "wpra-projection-v1",
        "admission_timing": "selected-unit-at-task-session",
        "objective_ref": bindings("objective-mpx", "invoke", "/objective"),
        "closure_receipt_refs": [
            binding(
                "accepted-findings-closeout",
                "invoke",
                closeout_path,
                "/status",
            ),
            binding(
                "minto-candidate-decision",
                "repository-owner",
                decision_path,
                "/status",
            ),
            bindings("frozen-plan-artifacts", "invoke", "/plan_artifacts/status"),
        ],
        "authority_bindings": {
            "canonical_authority_refs": [
                binding(
                    "selected-candidate-authority",
                    "repository-owner",
                    decision_path,
                    "/selectedOption/optionId",
                ),
                binding(
                    "accepted-findings-authority",
                    "invoke",
                    closeout_path,
                    "/result/sha256",
                ),
            ],
            "semantic_bindings": {
                "owner": bindings("semantic-owner", "invoke", "/objective"),
                "material": bindings(
                    "semantic-material", "task-session", "/material_policy"
                ),
                "validation": bindings(
                    "semantic-validation", "task-session", "/validation_policy"
                ),
                "receipt": bindings(
                    "semantic-receipt", "task-session", "/receipt_contract"
                ),
                "closeout": bindings(
                    "semantic-closeout", "invoke", "/closeout_contract"
                ),
            },
        },
        "execution_bindings": execution_bindings,
        "execution_policy": audit_policy,
        "receipt_bindings": {
            "terminal_schema_ref": binding(
                "task-session-terminal-schema",
                "task-session",
                schemas["terminal"],
                "",
            ),
            "semantic_validator_ref": opaque_binding(
                "task-session-terminal-semantic-validator",
                "task-session",
                semantic_validator,
            ),
            "expected_receipt_refs": [
                bindings(
                    f"expected-{unit_id}",
                    "task-session",
                    f"/expected_receipts/{unit_id}",
                )
                for unit_id in FRONTIER
            ],
        },
        "closeout_bindings": [
            {
                "unit_id": unit_id,
                "allowed_delta_policy_ref": bindings(
                    f"closeout-deltas-{unit_id}",
                    "invoke",
                    "/closeout_contract/allowed_delta_classes",
                ),
                "owner_receipt_contract_ref": bindings(
                    f"closeout-contract-{unit_id}",
                    "invoke",
                    f"/closeout_contract/contracts/{index}",
                ),
                "compensation": {
                    "mode": "none",
                    "rationale": (
                        "Readiness executes no SWU; later Task Session failure "
                        "retains exact evidence and stops successors."
                    ),
                },
            }
            for index, unit_id in enumerate(FRONTIER)
        ],
        "task_session_closeout_contracts": task_closeouts,
        "runtime_binding": {
            "requested_task_session_execution_mode": "routed-mutation",
            "task_session_admission_receipt_ref": None,
        },
        "status_receipt_refs": {
            "artifact_authored_status": {
                "value": "pass",
                "owner_ref": "invoke",
                "receipt_ref": bindings(
                    "status-artifact-authored", "invoke", "/status/artifact_authored"
                ),
            },
            "registry_released_status": {
                "value": "not-granted",
                "owner_ref": "release-owner",
                "receipt_ref": bindings(
                    "status-registry-released", "invoke", "/status/registry_released"
                ),
            },
            "mutation_runtime_ready_status": {
                "value": "false",
                "owner_ref": "task-session",
                "receipt_ref": bindings(
                    "status-mutation-runtime-ready",
                    "invoke",
                    "/status/mutation_runtime_ready",
                ),
            },
            "audit_verdict": {
                "value": "pending",
                "owner_ref": "work-pack-readiness-audit",
                "receipt_ref": bindings(
                    "status-audit-verdict", "invoke", "/status/audit_verdict"
                ),
            },
        },
        "lifecycle_status_refs": {
            "plan_artifact_status": {
                "value": "pass",
                "owner_ref": "invoke",
                "receipt_ref": bindings(
                    "status-plan-artifact", "invoke", "/status/plan_artifact"
                ),
            },
            "audit_status": {
                "value": "not-run",
                "owner_ref": "work-pack-readiness-audit",
                "receipt_ref": bindings(
                    "status-audit", "invoke", "/status/audit"
                ),
            },
            "approval_status": {
                "value": "unapproved",
                "owner_ref": "decision-gate",
                "receipt_ref": bindings(
                    "status-approval", "invoke", "/status/approval"
                ),
            },
            "chain_status": {
                "value": "not-started",
                "owner_ref": "implementation-readiness",
                "receipt_ref": bindings(
                    "status-chain", "invoke", "/status/chain"
                ),
            },
        },
        "approval_policy": {
            "approval_owner_ref": "repository-owner",
            "decision_gate_receipt_ref": binding(
                "candidate-identity-only",
                "repository-owner",
                decision_path,
                "/selectedOption/candidateId",
            ),
            "run_budget": {"max_task_session_requests": 3},
            "risk_policy_ref": bindings(
                "risk-policy", "implementation-readiness", "/risk_policy"
            ),
            "allowed_audit_verdicts": ["pass", "flag"],
            "allowed_flag_classes": ["observability-residue"],
        },
        "continuity_projection": {
            "cursor": "SWU-MPX-001",
            "completed_unit_receipt_refs": [],
            "joined_closeout_receipt_refs": [],
            "projected_next_successor": {
                "unit_id": "SWU-MPX-001",
                "canonical_successor_ref": bindings(
                    "canonical-frontier", "invoke", "/continuity/cursor"
                ),
                "projection_owner_ref": "work-pack-readiness-audit",
                "equivalence_validator_ref": bindings(
                    "continuity-equivalence",
                    "work-pack-readiness-audit",
                    "/continuity/equivalence",
                ),
                "continuation_router_verification_receipt_ref": bindings(
                    "continuation-frontier-verification",
                    "invoke",
                    "/continuity/verification",
                ),
                "authority_effect": "none",
            },
        },
    }


def main() -> int:
    routes = build_routes()
    execution_entry_path = PLAN_ROOT / "EXECUTION-ENTRY.json"
    write_json(execution_entry_path, build_execution_entry(routes))

    inventory_path = PLAN_ROOT / "readiness/PLAN-ARTIFACT-INVENTORY.json"
    plan_inventory = build_plan_inventory()
    write_json(inventory_path, plan_inventory)

    bindings_path = PLAN_ROOT / "readiness/AUDIT-BINDINGS.json"
    audit_bindings = build_audit_bindings(plan_inventory)
    if audit_bindings["continuity"]["verification"] != FRONTIER[0]:
        raise RuntimeError(
            "continuation verification must equal the first unfinished frontier unit"
        )
    write_json(bindings_path, audit_bindings)

    config_path = PLAN_ROOT / "readiness/audit-config.json"
    write_json(config_path, build_config(routes, bindings_path, inventory_path))
    print(
        json.dumps(
            {
                "status": "generated",
                "execution_entry": relative(execution_entry_path),
                "allowed_routes_digest": canonical_digest(routes),
                "plan_artifact_inventory": relative(inventory_path),
                "audit_bindings": relative(bindings_path),
                "audit_config": relative(config_path),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
