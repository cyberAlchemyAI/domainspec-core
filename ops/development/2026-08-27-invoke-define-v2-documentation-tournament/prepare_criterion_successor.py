#!/usr/bin/env python3
"""Generate the unconfirmed Define v2 criterion successor proposal artifacts."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[3]
OPS = Path(__file__).resolve().parent
TOURNAMENT = REPO / "arcanum/spells/invoke/development/define-v2-documentation/tournament"
PREFIX = "ops/development/2026-08-27-invoke-define-v2-documentation-tournament"
TOURNAMENT_PREFIX = "arcanum/spells/invoke/development/define-v2-documentation/tournament"
BRIEFINGS_NAME = "criterion-successor-propose.execution-briefings.json"
DISPATCH_NAME = "criterion-successor-propose.execution.dispatch.json"
SHEET_NAME = "criterion-successor-propose.dispatch-sheet.json"
MATERIAL_NAME = "criterion-successor-propose.material-projection.json"
RECEIPTS = f"{PREFIX}/criterion-successor-propose.execution/receipts"


def stable_payload(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def exact_ref(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(REPO).as_posix(),
        "sha256": sha256(data),
        "size": len(data),
    }


def briefing(
    identity: str,
    angle: str,
    instructions: str,
    input_refs: list[str],
    allowed_reads: list[str],
    forbidden_reads: list[str],
    required_fields: list[str],
    domain_field: str = "domain_gate_status",
) -> dict[str, Any]:
    forbidden_writes = [TOURNAMENT_PREFIX, PREFIX, "telemetry/agents/subagents-dispatch.yaml"]
    return {
        "agent_identity": identity,
        "angle": angle,
        "instructions": instructions,
        "status_semantics": {
            "task_status_field": "task_status",
            "task_complete_value": "completed",
            "task_blocked_value": "blocked",
            "domain_gate_status_field": domain_field,
            "domain_gate_is_separate": True,
        },
        "read_policy": {
            "input_refs": input_refs,
            "allowed_read_scopes": allowed_reads,
            "forbidden_read_scopes": forbidden_reads,
            "required_input_refs_readable": True,
        },
        "write_policy": {
            "mutation_policy": "read-only",
            "write_scope": [],
            "forbidden_write_scopes": forbidden_writes,
        },
        "receipt_shape": {
            "required_fields": required_fields,
            "completion_requires_all_fields": True,
        },
        "authority_ceiling": {
            "summary": "Read-only design evidence. No freeze, trial, scorer, publication, registration, or product authority.",
            "allowed_actions": ["read_declared_inputs", "run_declared_read_only_validator", "return_structured_receipt"],
            "forbidden_actions": [
                "edit_files", "freeze_criterion", "run_trials", "compile_trial_sources",
                "score_tournament", "read_forbidden_scope", "mutate_dispatch_ledger",
                "publish", "promote", "deploy",
            ],
        },
    }


def role_binding(role_id: str, payload: dict[str, Any], artifact_sha: str) -> dict[str, Any]:
    digest = sha256(stable_payload(payload))
    return {
        "contract_version": "arcanum.confirmed-role-briefing.v0.1",
        "source_binding": {
            "artifact_path": BRIEFINGS_NAME,
            "artifact_sha256": artifact_sha,
            "selector": f"/roles/{role_id}",
            "selected_payload_sha256": digest,
        },
        "briefing": payload,
        "briefing_sha256": digest,
    }


def build_briefings() -> dict[str, Any]:
    criterion_inputs = [
        f"{TOURNAMENT_PREFIX}/CRITERION.json",
        f"{TOURNAMENT_PREFIX}/criterion.schema.json",
        f"{TOURNAMENT_PREFIX}/render_criterion.py",
        f"{TOURNAMENT_PREFIX}/CRITERION.md",
        f"{TOURNAMENT_PREFIX}/validate_criterion.py",
        f"{TOURNAMENT_PREFIX}/TOURNAMENT-SPEC.md",
    ]
    guide_inputs = [
        f"{TOURNAMENT_PREFIX}/GUIDE-MANIFEST.json",
        f"{TOURNAMENT_PREFIX}/render_candidates.py",
        f"{TOURNAMENT_PREFIX}/verify_guide_equivalence.py",
        f"{TOURNAMENT_PREFIX}/content/",
        f"{TOURNAMENT_PREFIX}/guides/",
        f"{TOURNAMENT_PREFIX}/shared/",
    ]
    wave_one_receipts = [
        f"{RECEIPTS}/criterion-design.json",
        f"{RECEIPTS}/criterion-validation.json",
        f"{RECEIPTS}/guide-equivalence-audit.json",
        f"{RECEIPTS}/guide-equivalence-validation.json",
    ]
    forbidden_experiment = [
        f"{TOURNAMENT_PREFIX}/oracle/",
        f"{TOURNAMENT_PREFIX}/dispatch/",
        f"{TOURNAMENT_PREFIX}/runs/",
        f"{TOURNAMENT_PREFIX}/trials/",
        f"{TOURNAMENT_PREFIX}/score_tournament.py",
        f"{TOURNAMENT_PREFIX}/build_oracle_sources.py",
    ]
    return {
        "roles": {
            "criterion-designer": briefing(
                "Popper, Karl - machine-first criterion designer",
                "Audit the canonical criterion source and deterministic view without observing experimental results.",
                "Read the canonical JSON, schema, renderer, generated Markdown, protocol, and validator. Run validate_criterion.py read-only and return separate design and validator findings. Do not edit files or claim READY, freeze, or trial authority.",
                criterion_inputs,
                criterion_inputs,
                forbidden_experiment + [f"{TOURNAMENT_PREFIX}/GUIDE-MANIFEST.json", f"{TOURNAMENT_PREFIX}/guides/"],
                ["task_status", "domain_gate_status", "findings", "criterion_validation", "blockers"],
            ),
            "guide-equivalence-auditor": briefing(
                "Kuhn, Thomas - independent guide-equivalence auditor",
                "Verify that the three opaque guides differ only by the order of nine shared sections.",
                "Reconstruct the three expected guides in memory with verify_guide_equivalence.py. Verify exact manifest digests, nine shared sections, byte equality, and order-only variation. Do not read the opaque map, criterion designer analysis, trials, scorer, or results, and do not rewrite artifacts.",
                guide_inputs,
                guide_inputs,
                forbidden_experiment + [f"{TOURNAMENT_PREFIX}/CRITERION.json", f"{TOURNAMENT_PREFIX}/CRITERION.md"],
                ["task_status", "domain_gate_status", "findings", "guide_equivalence_validation", "blockers"],
            ),
            "validity-skeptic": briefing(
                "Lakatos, Imre - blind design-time validity skeptic",
                "Attack falsifiability, discrimination, arithmetic, topology, and reviewer independence from admitted wave-one receipts.",
                "Read the canonical criterion source, schema, generated view, protocol, and the four wave-one receipts. Return proposal_status valid only when the exact candidate is eligible for a later freeze request; return invalid when any defect remains. Stay blind to the opaque map, raw guides, guide manifest, trials, scorer, and results. Do not edit or freeze anything.",
                [
                    f"{TOURNAMENT_PREFIX}/CRITERION.json",
                    f"{TOURNAMENT_PREFIX}/criterion.schema.json",
                    f"{TOURNAMENT_PREFIX}/CRITERION.md",
                    f"{TOURNAMENT_PREFIX}/TOURNAMENT-SPEC.md",
                    *wave_one_receipts,
                ],
                [
                    f"{TOURNAMENT_PREFIX}/CRITERION.json",
                    f"{TOURNAMENT_PREFIX}/criterion.schema.json",
                    f"{TOURNAMENT_PREFIX}/CRITERION.md",
                    f"{TOURNAMENT_PREFIX}/TOURNAMENT-SPEC.md",
                    *wave_one_receipts,
                ],
                forbidden_experiment + [
                    f"{TOURNAMENT_PREFIX}/GUIDE-MANIFEST.json",
                    f"{TOURNAMENT_PREFIX}/content/",
                    f"{TOURNAMENT_PREFIX}/guides/",
                    f"{TOURNAMENT_PREFIX}/render_candidates.py",
                    f"{TOURNAMENT_PREFIX}/verify_guide_equivalence.py",
                ],
                ["task_status", "proposal_status", "findings", "bounded_repair_request", "blockers"],
                domain_field="proposal_status",
            ),
        }
    }


def build_dispatch(briefings: dict[str, Any], artifact_sha: str) -> dict[str, Any]:
    criterion_outputs = [f"{RECEIPTS}/criterion-design.json", f"{RECEIPTS}/criterion-validation.json"]
    guide_outputs = [f"{RECEIPTS}/guide-equivalence-audit.json", f"{RECEIPTS}/guide-equivalence-validation.json"]
    skeptic_output = f"{RECEIPTS}/validity-skeptic.json"
    roles = []
    role_specs = [
        ("criterion-designer", "criterion-design", "Audit the canonical machine-first criterion and run its deterministic validator.", criterion_outputs, []),
        ("guide-equivalence-auditor", "guide-equivalence-audit", "Independently prove that guides vary by section order only.", guide_outputs, []),
        ("validity-skeptic", "validity-skeptic", "Issue a blind design-time valid or invalid verdict from admitted receipts.", [skeptic_output], ["criterion-designer", "guide-equivalence-auditor"]),
    ]
    for role_id, step_id, purpose, outputs, dependencies in role_specs:
        payload = briefings["roles"][role_id]
        role = {
            "role_id": role_id,
            "purpose": purpose,
            "owns": " and ".join(outputs),
            "capability_ref": "experiment",
            "capability_target": f"{TOURNAMENT_PREFIX}/CRITERION.json",
            "capability_mode": "propose-validity",
            "agent_count": 1,
            "mutation_policy": "read-only",
            "write_scope": [],
            "forbidden_write_scopes": payload["write_policy"]["forbidden_write_scopes"],
            "briefing_binding": role_binding(role_id, payload, artifact_sha),
            "depends_on_roles": dependencies,
            "input_refs": payload["read_policy"]["input_refs"],
            "output_refs": outputs,
            "applies_to_steps": [step_id],
        }
        roles.append(role)

    def step(step_id: str, name: str, role_id: str, outputs: list[str], pattern: str, depends: list[str] | None = None):
        payload = briefings["roles"][role_id]
        item = {
            "step_id": step_id,
            "name": name,
            "capability_ref": "experiment",
            "capability_status": "local-extension",
            "capability_metadata": {
                "source": "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/experiment/SKILL.md",
                "validation_note": "The v0.10.0 proposal binds deterministic preconfirmation validation before any execution request.",
            },
            "mode": "propose-validity",
            "pattern": pattern,
            "parallel": step_id != "validity-skeptic",
            "techniques": ["sequence"],
            "roles": [role_id],
            "inputs": [
                {"kind": "receipt" if ref.startswith(RECEIPTS) else "artifact", "ref": ref}
                for ref in payload["read_policy"]["input_refs"]
            ],
            "outputs": [{"kind": "receipt", "ref": ref} for ref in outputs],
            "join_policy": "all",
            "stop_conditions": ["stop on any read-scope breach, validator failure, missing receipt, or blocked task status"],
        }
        if depends:
            item["depends_on_steps"] = depends
        if pattern == "validation":
            item["evidence_artifact"] = outputs[-1]
        if pattern == "dialectic":
            item["convergence_criteria"] = [
                "valid only when all machine and guide invariants pass and no design-time validity defect remains",
                "invalid when any falsifiability, arithmetic, topology, blinding, or reproducibility defect remains",
            ]
        return item

    return {
        "dispatch_id": "2026-08-27-invoke-define-v2-tournament-criterion-successor-propose",
        "intent": {
            "raw": "Evaluate the successor machine-first criterion with independent criterion and guide checks followed by one blind validity skeptic.",
            "objective": "Return valid or invalid without freezing the criterion or starting any tournament trial.",
            "target_artifact": f"{TOURNAMENT_PREFIX}/CRITERION.json",
        },
        "mode": "validation",
        "techniques": ["sequence", "observability_grouping"],
        "steps": [
            step("criterion-design", "Audit canonical criterion and deterministic rendering", "criterion-designer", criterion_outputs, "validation"),
            step("guide-equivalence-audit", "Verify order-only guide equivalence", "guide-equivalence-auditor", guide_outputs, "validation"),
            step("validity-skeptic", "Attack proposal validity from admitted receipts", "validity-skeptic", [skeptic_output], "dialectic", ["criterion-design", "guide-equivalence-audit"]),
        ],
        "gates": [
            {
                "gate_id": "g-wave-one-evidence",
                "kind": "validation",
                "owner": "parent-orchestrator",
                "condition": "Both independent roles and both deterministic validators return passing receipts.",
                "applies_after_wave": "criterion-and-guide-evidence",
                "requires_role_receipts": criterion_outputs + guide_outputs,
                "evaluation": {"mode": "receipt_status"},
                "on_fail": "block",
            },
            {
                "gate_id": "g-proposal-domain-outcome",
                "kind": "quality",
                "owner": "parent-orchestrator",
                "condition": "A valid proposal may proceed only to a later exact freeze request; invalid is a terminal design resolution.",
                "applies_after_wave": "validity-skeptic",
                "requires_role_receipts": [skeptic_output],
                "evaluation": {
                    "mode": "domain_status",
                    "source_role_id": "validity-skeptic",
                    "source_field": "proposal_status",
                    "pass_values": ["valid"],
                    "resolved_values": ["invalid"],
                },
                "on_fail": "block",
            },
        ],
        "subagent_strategy": {
            "status": "required",
            "trigger": "Independent criterion and guide obligations must close before one blind design-time validity decision.",
            "explanation": "Wave one keeps the criterion and guide-equivalence checks in independent singleton roles; wave two sees their receipts but remains blind to raw experimental material.",
            "context": [
                "CRITERION.json is canonical and CRITERION.md is generated.",
                "No freeze, registration, canary, tournament trial, publication, or promotion is authorized.",
            ],
            "binding_mode": "capability-bound",
            "execution_owner": "parent-orchestrator",
            "execution_contract_version": "arcanum.capability-bound-execution.v0.2",
            "roles": roles,
            "execution_waves": [
                {
                    "wave_id": "criterion-and-guide-evidence",
                    "role_ids": ["criterion-designer", "guide-equivalence-auditor"],
                    "parallel": True,
                    "join_policy": "all",
                    "gate_after": "g-wave-one-evidence",
                    "on_incomplete": "block",
                },
                {
                    "wave_id": "validity-skeptic",
                    "role_ids": ["validity-skeptic"],
                    "parallel": False,
                    "join_policy": "all",
                    "depends_on_waves": ["criterion-and-guide-evidence"],
                    "gate_after": "g-proposal-domain-outcome",
                    "on_incomplete": "block",
                },
            ],
            "parallelism": "mixed",
            "join_policy": "all",
            "authorization": "requires_user_permission",
            "permission_prompt": "Run the exact successor criterion proposal after its v0.10.0 preconfirmation closure passes?",
            "receipt_requirements": [
                "agent_id", "role_id", "spawn_status", "join_status", "close_status",
                "dispatch_id", "step_id", "capability_ref", "capability_target",
                "capability_mode", "wave_id", "write_scope", "status", "artifacts",
                "validation", "observer_status", "blockers", "residue", "reroute",
                "handoff_note",
            ],
        },
        "observability": {
            "dispatch_id_required": True,
            "trace_events": ["subagent_spawned", "wave_joined", "gate_decided", "subagent_closed"],
            "signal_grouping": "dispatch_id, run_id, and wave_id",
        },
        "promotion_guardrails": [
            "valid permits only a later exact freeze request.",
            "invalid closes the proposal without freezing.",
            "No outcome starts the six-trial tournament or grants publication authority.",
        ],
    }


def build_sheet(dispatch_ref: dict[str, Any], briefings_ref: dict[str, Any]) -> dict[str, Any]:
    package = {
        "source_ref": exact_ref(TOURNAMENT / "CRITERION.json"),
        "schema_ref": exact_ref(TOURNAMENT / "criterion.schema.json"),
        "renderer_ref": exact_ref(TOURNAMENT / "render_criterion.py"),
        "generated_view_ref": exact_ref(TOURNAMENT / "CRITERION.md"),
        "protocol_ref": exact_ref(TOURNAMENT / "TOURNAMENT-SPEC.md"),
        "guide_manifest_ref": exact_ref(TOURNAMENT / "GUIDE-MANIFEST.json"),
        "criterion_validator_ref": exact_ref(TOURNAMENT / "validate_criterion.py"),
        "guide_equivalence_validator_ref": exact_ref(TOURNAMENT / "verify_guide_equivalence.py"),
    }
    return {
        "dispatch_id": "2026-08-27-invoke-define-v2-tournament-criterion-successor-propose",
        "schema_version": "0.10.0",
        "dispatch_type": "experiment",
        "goal": "Evaluate the machine-first successor criterion and either permit a later exact freeze request or close the proposal invalid before any trial begins.",
        "context": "CRITERION.json is canonical, criterion.schema.json validates its shape, and CRITERION.md is a deterministic view. Wave one separates criterion design from guide-equivalence audit and runs the bound read-only validators. Wave two is blind to the opaque map, raw guides, trials, scorer, and results. This proposal grants no freeze, canary, trial, publication, or promotion authority.",
        "max_loops": 1,
        "final_approver": "parent",
        "working_folder": f"{TOURNAMENT_PREFIX}/",
        "experiment_contract": {
            "phase": "propose",
            "criterion_output_path": "CRITERION.json",
            "criterion_package": package,
            "execution_dispatch_ref": dispatch_ref,
            "execution_briefings_ref": briefings_ref,
            "pre_freeze_obligations": [
                {
                    "obligation_id": "guide-equivalence-independent-audit",
                    "execution_role_id": "guide-equivalence-auditor",
                    "receipt_ref": f"{RECEIPTS}/guide-equivalence-validation.json",
                    "gate_id": "g-wave-one-evidence",
                    "required_read_scopes": [
                        f"{TOURNAMENT_PREFIX}/GUIDE-MANIFEST.json",
                        f"{TOURNAMENT_PREFIX}/content/",
                        f"{TOURNAMENT_PREFIX}/guides/",
                    ],
                    "independent_of_role_ids": ["criterion-designer"],
                },
                {
                    "obligation_id": "blind-validity-skeptic",
                    "execution_role_id": "validity-skeptic",
                    "receipt_ref": f"{RECEIPTS}/validity-skeptic.json",
                    "gate_id": "g-proposal-domain-outcome",
                    "required_read_scopes": [
                        f"{TOURNAMENT_PREFIX}/CRITERION.json",
                        f"{RECEIPTS}/criterion-validation.json",
                        f"{RECEIPTS}/guide-equivalence-validation.json",
                    ],
                    "independent_of_role_ids": ["criterion-designer", "guide-equivalence-auditor"],
                },
            ],
        },
        "anti_bias_global": "criterion semantics versus guide-equivalence and blind validity attack",
        "groups": [
            {
                "group_id": "criterion-and-guide-evidence",
                "n": 2,
                "anti_bias": "methodology (machine-first criterion validation versus byte-level guide-equivalence audit)",
                "predicted_disagreements": [{
                    "pair": [0, 1],
                    "statement": "Agent 0 runs machine-first criterion validation while agent 1 runs byte-level guide-equivalence validation on the methodology axis; a bias in agent 0 toward criterion completeness would be exposed by agent 1 rejecting guide-byte or section-topology drift.",
                }],
                "agents": [
                    {
                        "agent_name": "Popper, Karl", "role": "writer", "model": "gpt-5.6-sol", "token_budget": 2500,
                        "angle": "machine-first falsifiability and deterministic criterion validation",
                        "initial_prompt": "Run only the bound machine-first criterion audit and read-only validator; return the two declared receipts without editing or freezing files.",
                    },
                    {
                        "agent_name": "Kuhn, Thomas", "role": "auditor", "model": "gpt-5.6-sol", "token_budget": 2500,
                        "angle": "independent order-only guide equivalence and manifest integrity",
                        "initial_prompt": "Run only the bound read-only guide-equivalence audit; remain blind to the opaque map, trials, scorer, and results.",
                    },
                ],
            },
            {
                "group_id": "validity-skeptic",
                "agents": [{
                    "agent_name": "Lakatos, Imre", "role": "skeptic", "model": "gpt-5.6-sol", "token_budget": 2500,
                    "initial_prompt": "Consume only the declared criterion and four admitted wave-one receipts. Return valid or invalid while remaining blind to raw guides, opaque mapping, trials, scorer, and results.",
                }],
            },
        ],
        "connections": [{"from": "criterion-and-guide-evidence", "to": "validity-skeptic", "type": "sequential"}],
    }


def main() -> int:
    briefings = build_briefings()
    briefings_path = OPS / BRIEFINGS_NAME
    write_json(briefings_path, briefings)
    briefings_sha = sha256(briefings_path.read_bytes())

    dispatch = build_dispatch(briefings, briefings_sha)
    dispatch_path = OPS / DISPATCH_NAME
    write_json(dispatch_path, dispatch)

    sheet = build_sheet(exact_ref(dispatch_path), exact_ref(briefings_path))
    sheet_path = OPS / SHEET_NAME
    write_json(sheet_path, sheet)

    node = shutil.which("node") or "/home/vrondelli/.nvm/versions/node/v22.12.0/bin/node"
    projector = REPO / "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/material-strategy.cjs"
    completed = subprocess.run([node, str(projector), "--project", str(sheet_path)], check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise SystemExit(completed.stderr or completed.stdout)
    material = json.loads(completed.stdout)
    write_json(OPS / MATERIAL_NAME, material)

    print("SUCCESSOR_PROPOSAL_GENERATION=pass")
    print("CONFIRMATION=not_requested")
    print("REGISTRATION=not_started")
    print("SPAWN_ATTEMPTS=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
