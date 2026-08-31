#!/usr/bin/env python3
"""Read-only closure checks for the unconfirmed criterion successor proposal."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPO = Path(__file__).resolve().parents[3]
OPS = Path(__file__).resolve().parent
SHEET = OPS / "criterion-successor-propose.dispatch-sheet.json"
DISPATCH = OPS / "criterion-successor-propose.execution.dispatch.json"
BRIEFINGS = OPS / "criterion-successor-propose.execution-briefings.json"
MATERIAL = OPS / "criterion-successor-propose.material-projection.json"
CLOSURE = OPS / "criterion-successor-propose.preconfirmation-closure.json"
TOURNAMENT = REPO / "arcanum/spells/invoke/development/define-v2-documentation/tournament"


def topology_blockers(dispatch: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    strategy = dispatch.get("subagent_strategy", {})
    waves = strategy.get("execution_waves", [])
    if strategy.get("execution_contract_version") != "arcanum.capability-bound-execution.v0.2":
        blockers.append("successor dispatch does not declare execution contract v0.2")
    expected_waves = [
        ("criterion-and-guide-evidence", ["criterion-designer", "guide-equivalence-auditor"]),
        ("validity-skeptic", ["validity-skeptic"]),
    ]
    if [(wave.get("wave_id"), wave.get("role_ids")) for wave in waves] != expected_waves:
        blockers.append("successor topology is not the exact two-wave design")

    role_by_id = {role.get("role_id"): role for role in strategy.get("roles", []) if isinstance(role, dict)}
    guide = role_by_id.get("guide-equivalence-auditor", {})
    skeptic = role_by_id.get("validity-skeptic", {})
    guide_reads = set(guide.get("briefing_binding", {}).get("briefing", {}).get("read_policy", {}).get("allowed_read_scopes", []))
    guide_forbidden = set(guide.get("briefing_binding", {}).get("briefing", {}).get("read_policy", {}).get("forbidden_read_scopes", []))
    skeptic_reads = set(skeptic.get("briefing_binding", {}).get("briefing", {}).get("read_policy", {}).get("allowed_read_scopes", []))
    skeptic_forbidden = set(skeptic.get("briefing_binding", {}).get("briefing", {}).get("read_policy", {}).get("forbidden_read_scopes", []))
    guide_required = {
        "arcanum/spells/invoke/development/define-v2-documentation/tournament/GUIDE-MANIFEST.json",
        "arcanum/spells/invoke/development/define-v2-documentation/tournament/content/",
        "arcanum/spells/invoke/development/define-v2-documentation/tournament/guides/",
    }
    if not guide_required <= guide_reads:
        blockers.append("guide-equivalence auditor lacks sufficient exact read scopes")
    forbidden_fragments = ("/oracle/", "/runs/", "/trials/", "score_tournament.py")
    if any(any(fragment in scope for fragment in forbidden_fragments) for scope in guide_reads):
        blockers.append("guide-equivalence auditor can read forbidden experimental scopes")
    if not all(any(fragment in scope for scope in guide_forbidden) for fragment in forbidden_fragments):
        blockers.append("guide-equivalence auditor does not explicitly forbid every blind experimental scope")

    skeptic_forbidden_fragments = ("GUIDE-MANIFEST.json", "/guides/", "/oracle/", "score_tournament.py")
    if any(any(fragment in scope for fragment in skeptic_forbidden_fragments) for scope in skeptic_reads):
        blockers.append("validity skeptic can read a forbidden raw guide, manifest, opaque map, or scorer scope")
    if not all(any(fragment in scope for scope in skeptic_forbidden) for fragment in skeptic_forbidden_fragments):
        blockers.append("validity skeptic does not explicitly forbid every required blind scope")
    return blockers


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exact_ref(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"path": path.relative_to(REPO).as_posix(), "sha256": sha256(data), "size": len(data)}


def run(command: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(command, cwd=REPO, check=False, capture_output=True, text=True)
    return completed.returncode, completed.stdout, completed.stderr


def validate() -> dict[str, Any]:
    blockers: list[str] = []
    try:
        sheet = json.loads(SHEET.read_text(encoding="utf-8"))
        dispatch = json.loads(DISPATCH.read_text(encoding="utf-8"))
        json.loads(BRIEFINGS.read_text(encoding="utf-8"))
        material = json.loads(MATERIAL.read_text(encoding="utf-8"))
        closure = json.loads(CLOSURE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "block", "blockers": [f"successor artifact unreadable: {exc}"], "writes": 0}

    code, stdout, stderr = run([
        "/home/vrondelli/.nvm/versions/node/v22.12.0/bin/node",
        str(REPO / "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs"),
        "--validate-sheet", str(SHEET),
    ])
    if code != 0 or "SHEET_VALIDATION=pass" not in stdout or "SCHEMA_VERSION=0.10.0" not in stdout:
        blockers.append(f"sheet validation failed: {stderr or stdout}")

    code, stdout, stderr = run([str(REPO / "arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py"), str(DISPATCH), "--json"])
    try:
        dispatch_result = json.loads(stdout)
    except json.JSONDecodeError:
        dispatch_result = {"validation": "block", "blocks": [stderr or stdout]}
    if code != 0 or dispatch_result.get("validation") != "pass":
        blockers.append(f"Dispatch Spec failed: {dispatch_result}")

    code, stdout, stderr = run([
        "python3", str(REPO / "arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py"),
        "rehearse", str(DISPATCH), "--run-id", "successor-validator",
    ])
    try:
        rehearsal = json.loads(stdout)
    except json.JSONDecodeError:
        rehearsal = {"status": "block", "blockers": [stderr or stdout]}
    if not (
        code == 0 and rehearsal.get("status") == "pass"
        and rehearsal.get("spawn_attempt_count") == 0
        and rehearsal.get("action_document_count") == 0
        and rehearsal.get("host_call_count") == 0
    ):
        blockers.append(f"no-effect rehearsal failed: {rehearsal}")

    blockers.extend(topology_blockers(dispatch))

    contract = sheet.get("experiment_contract", {})
    if contract.get("execution_dispatch_ref") != exact_ref(DISPATCH):
        blockers.append("sheet execution dispatch ref drifted")
    if contract.get("execution_briefings_ref") != exact_ref(BRIEFINGS):
        blockers.append("sheet execution briefings ref drifted")
    package_paths = {
        "source_ref": TOURNAMENT / "CRITERION.json",
        "schema_ref": TOURNAMENT / "criterion.schema.json",
        "renderer_ref": TOURNAMENT / "render_criterion.py",
        "generated_view_ref": TOURNAMENT / "CRITERION.md",
        "protocol_ref": TOURNAMENT / "TOURNAMENT-SPEC.md",
        "guide_manifest_ref": TOURNAMENT / "GUIDE-MANIFEST.json",
        "criterion_validator_ref": TOURNAMENT / "validate_criterion.py",
        "guide_equivalence_validator_ref": TOURNAMENT / "verify_guide_equivalence.py",
    }
    for key, path in package_paths.items():
        if contract.get("criterion_package", {}).get(key) != exact_ref(path):
            blockers.append(f"criterion package ref drifted: {key}")

    node = "/home/vrondelli/.nvm/versions/node/v22.12.0/bin/node"
    code, stdout, stderr = run([
        node,
        str(REPO / "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/material-strategy.cjs"),
        "--compare", str(MATERIAL), str(SHEET),
    ])
    if code != 0:
        blockers.append(f"material projection drifted: {stderr or stdout}")

    closure_schema = json.loads((REPO / "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/preconfirmation-closure.schema.json").read_text(encoding="utf-8"))
    schema_errors = list(Draft202012Validator(closure_schema).iter_errors(closure))
    closure_codes = {item.get("code") for item in closure.get("blockers", []) if isinstance(item, dict)}
    pending_tension = closure.get("status") == "block" and closure_codes == {"subject_tension_evidence_missing"}
    if schema_errors or closure.get("status") not in {"pass", "block"} or closure.get("execution_rehearsal", {}).get("spawn_attempt_count") != 0:
        blockers.append("preconfirmation closure is absent, stale, or structurally invalid")
    elif closure.get("status") == "block" and not pending_tension:
        blockers.append("preconfirmation closure has blockers beyond the expected pending subject-tension gate")
    if closure.get("inputs", {}).get("sheet_ref") != exact_ref(SHEET):
        blockers.append("preconfirmation closure is not bound to current sheet bytes")
    if closure.get("inputs", {}).get("material_projection_ref") != exact_ref(MATERIAL):
        blockers.append("preconfirmation closure is not bound to current material projection")
    if closure.get("material_strategy", {}).get("material_sha256") != material.get("material_sha256"):
        blockers.append("closure material digest differs from the material projection")

    closure_compiler = REPO / "implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/preconfirmation-closure.cjs"
    verify_command = [
        node,
        str(closure_compiler),
        "--sheet", str(SHEET),
        "--material-projection", str(MATERIAL),
        "--receipt", str(CLOSURE),
        "--repo-root", str(REPO),
        "--verify-only", "true",
    ]
    tension_ref = closure.get("inputs", {}).get("tension_evidence_ref")
    if isinstance(tension_ref, dict) and isinstance(tension_ref.get("path"), str):
        verify_command.extend(["--tension-evidence", str(REPO / tension_ref["path"])])
    code, stdout, stderr = run(verify_command)
    try:
        closure_verification = json.loads(stdout)
    except json.JSONDecodeError:
        closure_verification = {"status": "block", "verification": "unreadable", "diagnostic": stderr or stdout}
    expected_verify_code = 0 if closure.get("status") == "pass" else 1
    closure_is_fresh = (
        code == expected_verify_code
        and closure_verification.get("verification") == "exact_recompute"
        and closure_verification.get("status") == closure.get("status")
        and closure_verification.get("spawn_attempt_count") == 0
    )
    if not closure_is_fresh:
        blockers.append(f"preconfirmation closure is not an exact fresh compiler recomputation: {closure_verification}")

    if blockers:
        proposal_readiness = "block"
    elif pending_tension:
        proposal_readiness = "block_pending_subject_tension"
    else:
        proposal_readiness = closure.get("status")

    return {
        "status": "pass" if not blockers else "block",
        "dispatch_spec": dispatch_result.get("validation"),
        "rehearsal": rehearsal,
        "preconfirmation_closure": closure.get("status"),
        "proposal_readiness": proposal_readiness,
        "confirmation": "not_requested",
        "registration": "not_started",
        "writes": 0,
        "blockers": blockers,
    }


def main() -> int:
    result = validate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
