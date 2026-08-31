#!/usr/bin/env python3
"""Generate the unconfirmed, no-product terminal-resolution canary."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from prepare_criterion_successor import (
    OPS,
    PREFIX,
    REPO,
    TOURNAMENT,
    TOURNAMENT_PREFIX,
    briefing,
    exact_ref,
    sha256,
    stable_payload,
    write_json,
)


BRIEFINGS_NAME = "terminal-resolution-canary.execution-briefings.json"
DISPATCH_NAME = "terminal-resolution-canary.execution.dispatch.json"
SHEET_NAME = "terminal-resolution-canary.dispatch-sheet.json"
MATERIAL_NAME = "terminal-resolution-canary.material-projection.json"
RECEIPTS = f"{PREFIX}/terminal-resolution-canary.execution/receipts"


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
    criterion = f"{TOURNAMENT_PREFIX}/CRITERION.json"
    blind_scopes = [
        f"{TOURNAMENT_PREFIX}/oracle/",
        f"{TOURNAMENT_PREFIX}/runs/",
        f"{TOURNAMENT_PREFIX}/trials/",
        f"{TOURNAMENT_PREFIX}/score_tournament.py",
    ]
    return {
        "roles": {
            "canary-control": briefing(
                "Terminal gate canary control",
                "Confirm the read-only canary input is readable and return ready without judging the criterion.",
                "Read only the declared canonical criterion source. Return task_status completed, canary_control_status ready, and an empty blockers array. Do not edit, freeze, score, register, or run trials.",
                [criterion],
                [criterion],
                blind_scopes,
                ["task_status", "canary_control_status", "blockers"],
                domain_field="canary_control_status",
            ),
            "terminal-invalid-canary": briefing(
                "Terminal gate invalid-resolution canary",
                "Exercise the final domain gate by returning the predeclared terminal invalid value.",
                "Read only the declared canonical criterion source. This is a runtime-contract canary, not a criterion review: return task_status completed, canary_outcome invalid, and an empty blockers array exactly. Do not edit, freeze, score, register, or run trials.",
                [criterion],
                [criterion],
                blind_scopes,
                ["task_status", "canary_outcome", "blockers"],
                domain_field="canary_outcome",
            ),
        }
    }


def build_dispatch(briefings: dict[str, Any], artifact_sha: str) -> dict[str, Any]:
    criterion = f"{TOURNAMENT_PREFIX}/CRITERION.json"
    control_receipt = f"{RECEIPTS}/control.json"
    terminal_receipt = f"{RECEIPTS}/terminal-invalid.json"
    role_specs = [
        ("canary-control", "canary-control", control_receipt),
        ("terminal-invalid-canary", "terminal-invalid", terminal_receipt),
    ]
    roles = []
    steps = []
    for role_id, step_id, output in role_specs:
        payload = briefings["roles"][role_id]
        roles.append({
            "role_id": role_id,
            "purpose": payload["angle"],
            "owns": output,
            "capability_ref": "experiment",
            "capability_target": criterion,
            "capability_mode": "terminal-resolution-canary",
            "agent_count": 1,
            "mutation_policy": "read-only",
            "write_scope": [],
            "forbidden_write_scopes": payload["write_policy"]["forbidden_write_scopes"],
            "briefing_binding": role_binding(role_id, payload, artifact_sha),
            "depends_on_roles": [],
            "input_refs": [criterion],
            "output_refs": [output],
            "applies_to_steps": [step_id],
        })
        steps.append({
            "step_id": step_id,
            "name": "Read-only control receipt" if role_id == "canary-control" else "Intentional terminal invalid receipt",
            "capability_ref": "experiment",
            "capability_status": "local-extension",
            "capability_metadata": {
                "source": "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/experiment/SKILL.md",
                "validation_note": "The canary exercises only the v0.2 terminal gate and makes no product or trial mutation.",
            },
            "mode": "terminal-resolution-canary",
            "pattern": "validation",
            "parallel": False,
            "techniques": ["sequence"],
            "roles": [role_id],
            "inputs": [{"kind": "artifact", "ref": criterion}],
            "outputs": [{"kind": "receipt", "ref": output}],
            "evidence_artifact": output,
            "stop_conditions": ["stop on any read-scope breach, task failure, missing receipt, or value other than the predeclared canary result"],
        })

    return {
        "dispatch_id": "2026-08-27-invoke-define-v2-terminal-resolution-canary",
        "intent": {
            "raw": "Run one separately confirmed read-only canary whose final role intentionally returns invalid.",
            "objective": "Prove gate_resolved preserves invalid in complete state and unlocks no dependent work.",
            "target_artifact": criterion,
        },
        "mode": "validation",
        "techniques": ["sequence"],
        "steps": steps,
        "gates": [{
            "gate_id": "g-terminal-invalid-canary",
            "kind": "validation",
            "owner": "parent-orchestrator",
            "condition": "Both receipts are admitted and the terminal source returns the intentional invalid value.",
            "applies_after_wave": "terminal-canary",
            "requires_role_receipts": [control_receipt, terminal_receipt],
            "evaluation": {
                "mode": "domain_status",
                "source_role_id": "terminal-invalid-canary",
                "source_field": "canary_outcome",
                "pass_values": ["valid"],
                "resolved_values": ["invalid"],
            },
            "on_fail": "block",
        }],
        "subagent_strategy": {
            "status": "required",
            "trigger": "The terminal-resolution contract requires a separately confirmed live native canary.",
            "explanation": "Two independent singleton roles run in one final wave so the terminal domain outcome can be tested without downstream actions.",
            "context": [
                "The terminal role intentionally returns invalid.",
                "No criterion edit, freeze, tournament trial, publication, product mutation, or deployment is authorized.",
            ],
            "binding_mode": "capability-bound",
            "execution_owner": "parent-orchestrator",
            "execution_contract_version": "arcanum.capability-bound-execution.v0.2",
            "roles": roles,
            "execution_waves": [{
                "wave_id": "terminal-canary",
                "role_ids": ["canary-control", "terminal-invalid-canary"],
                "parallel": True,
                "join_policy": "all",
                "gate_after": "g-terminal-invalid-canary",
                "on_incomplete": "block",
            }],
            "parallelism": "fanout",
            "join_policy": "all",
            "authorization": "requires_user_permission",
            "permission_prompt": "Run the exact read-only terminal-resolution canary after its v0.10 preconfirmation closure passes?",
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
            "The canary outcome authorizes no criterion freeze or tournament trial.",
            "gate_resolved must expose zero dependent actions.",
        ],
    }


def build_sheet(dispatch_ref: dict[str, Any], briefings_ref: dict[str, Any]) -> dict[str, Any]:
    criterion = f"{TOURNAMENT_PREFIX}/CRITERION.json"
    terminal_receipt = f"{RECEIPTS}/terminal-invalid.json"
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
        "dispatch_id": "2026-08-27-invoke-define-v2-terminal-resolution-canary",
        "schema_version": "0.10.0",
        "dispatch_type": "experiment",
        "goal": "Exercise the v0.2 terminal domain gate with an intentional invalid resolution before the successor criterion proposal may run.",
        "context": "This is a separately confirmed, read-only governance canary. Two singleton roles run in one final wave; the terminal role intentionally returns invalid, which must produce gate_resolved with complete state and no dependent actions. No criterion edit, freeze, trial, product mutation, publication, or deployment is authorized.",
        "max_loops": 1,
        "final_approver": "parent",
        "working_folder": f"{TOURNAMENT_PREFIX}/",
        "experiment_contract": {
            "phase": "propose",
            "criterion_output_path": "CRITERION.json",
            "criterion_package": package,
            "execution_dispatch_ref": dispatch_ref,
            "execution_briefings_ref": briefings_ref,
            "pre_freeze_obligations": [{
                "obligation_id": "terminal-invalid-resolution",
                "execution_role_id": "terminal-invalid-canary",
                "receipt_ref": terminal_receipt,
                "gate_id": "g-terminal-invalid-canary",
                "required_read_scopes": [criterion],
                "independent_of_role_ids": ["canary-control"],
            }],
        },
        "groups": [
            {
                "group_id": "canary-control",
                "agents": [{
                    "agent_name": None,
                    "role": "writer",
                    "model": "gpt-5.6-sol",
                    "token_budget": 500,
                    "initial_prompt": "Return only the bound read-only control receipt; do not edit or evaluate the criterion.",
                }],
            },
            {
                "group_id": "terminal-invalid-canary",
                "agents": [{
                    "agent_name": None,
                    "role": "skeptic",
                    "model": "gpt-5.6-sol",
                    "token_budget": 500,
                    "initial_prompt": "Return only the predeclared invalid canary outcome; do not edit or evaluate the criterion.",
                }],
            },
        ],
        "connections": [],
    }


def main() -> int:
    briefings = build_briefings()
    briefings_path = OPS / BRIEFINGS_NAME
    write_json(briefings_path, briefings)

    dispatch = build_dispatch(briefings, sha256(briefings_path.read_bytes()))
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
    write_json(OPS / MATERIAL_NAME, json.loads(completed.stdout))

    print("TERMINAL_CANARY_GENERATION=pass")
    print("CONFIRMATION=not_requested")
    print("REGISTRATION=not_started")
    print("SPAWN_ATTEMPTS=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
