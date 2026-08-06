#!/usr/bin/env python3
"""Stage and apply the bounded IRO runtime-admission contract repair."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
REFRESH_ROOT = Path(__file__).resolve().parent
MATERIAL_ROOT = REFRESH_ROOT / "material"
OUTPUT_ROOT = MATERIAL_ROOT / "outputs"

PREFIX = "ops/development/2026-08-01-intent-route-arcanum-addon/planning"
TARGETS = [
    f"{PREFIX}/WORK-PACK.md",
    f"{PREFIX}/EXECUTION-PACK.md",
    f"{PREFIX}/goals/IRO-FULL-STREAM/GOAL-SIDECAR.md",
    f"{PREFIX}/goals/IRO-FULL-STREAM/IRO-FULL-STREAM.md",
    f"{PREFIX}/work-pack/shared/EXECUTION-CONTRACT.json",
    f"{PREFIX}/work-pack/shared/validate-execution-contract.py",
    f"{PREFIX}/work-pack/shared/CLOSEOUT-SYNC.md",
    f"{PREFIX}/work-pack/shared/RUNTIME-EVIDENCE.md",
    f"{PREFIX}/work-pack/shared/GOAL-START-APPROVAL.schema.json",
    f"{PREFIX}/work-pack/shared/CLOSEOUT-PREFLIGHT.schema.json",
    f"{PREFIX}/work-pack/shared/CLOSEOUT-SYNC-REQUEST.schema.json",
]

COMMON_OUTPUTS = [
    "CONTEXT-PACK.md",
    "CONTEXT-PACK.json",
    "closeout-preflight.json",
    "mutation-admission-request.json",
    "mutation-admission-receipt.json",
    "terminal-receipt.json",
    "closeout-sync-request.json",
    "closeout-owner-receipt.json",
    "continuation-route.json",
]
IRO_001_OUTPUTS = [
    "OPTION-ADMISSIBILITY-REQUEST.json",
    "OPTION-ADMISSIBILITY-RECEIPT.json",
    "DECISION.json",
    "DECISION-SUMMARY.md",
    "decision-bundle.json",
]


def rendered_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exact_ref(path: str, base: Path = ROOT) -> dict[str, object]:
    data = (base / path).read_bytes()
    return {"path": path, "sha256": digest(data), "size_bytes": len(data)}


def write_output(path: str, content: bytes) -> None:
    target = OUTPUT_ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


def append_once(text: str, marker: str, addition: str) -> str:
    return text if marker in text else text.rstrip() + "\n\n" + addition.strip() + "\n"


def build_contract() -> bytes:
    path = ROOT / f"{PREFIX}/work-pack/shared/EXECUTION-CONTRACT.json"
    doc = json.loads(path.read_text())
    doc["schema_version"] = "1.1.0"
    doc["runtime_evidence_contract"] = {
        "per_unit_outputs": COMMON_OUTPUTS,
        "iro_001_additional_outputs": IRO_001_OUTPUTS,
        "continuity_cursor_template": ".arcanum/task-session/continuity/IRO-FULL-STREAM-<epoch-id>-<unit-id>.json",
        "write_profile": "execution-output-only until an owner-approved material package replaces the current unit contract",
        "terminal_write_rule": "terminal-receipt.json is the final unit-local write before closeout routing",
    }
    doc["chain_runtime"] = {
        "approval_receipt": f"{PREFIX}/work-pack/session-evidence/IRO-FULL-STREAM/<epoch-id>/goal-start-approval.json",
        "chain_config": f"{PREFIX}/work-pack/session-evidence/IRO-FULL-STREAM/<epoch-id>/chain-config.json",
        "chain_preflight": f"{PREFIX}/work-pack/session-evidence/IRO-FULL-STREAM/<epoch-id>/chain-preflight.json",
        "state_directory": ".arcanum/task-session-until-blocker/chains/IRO-FULL-STREAM-<epoch-id>",
        "chain_record": ".arcanum/task-session-until-blocker/chains/IRO-FULL-STREAM-<epoch-id>/chain.json",
        "transition_receipts": [
            f".arcanum/task-session-until-blocker/chains/IRO-FULL-STREAM-<epoch-id>/transitions/{index:06d}.json"
            for index in range(1, 11)
        ],
    }
    doc["receipt_schemas"].update({
        "goal_start_approval": f"{PREFIX}/work-pack/shared/GOAL-START-APPROVAL.schema.json",
        "closeout_preflight": f"{PREFIX}/work-pack/shared/CLOSEOUT-PREFLIGHT.schema.json",
        "closeout_sync_request": f"{PREFIX}/work-pack/shared/CLOSEOUT-SYNC-REQUEST.schema.json",
        "mutation_admission_request": ".agents/skills/task-session/schemas/mutation-admission-request.schema.json",
        "mutation_admission_receipt": ".agents/skills/task-session/schemas/mutation-admission-receipt.schema.json",
        "continuation_route": ".agents/skills/continuation-router/continuation-route.schema.json",
        "continuity_cursor": ".agents/skills/task-session/continuity.schema.json",
        "chain_config": ".agents/skills/task-session-until-blocker/schemas/chain-config.schema.json",
        "chain_transition": ".agents/skills/task-session-until-blocker/schemas/chain-transition.schema.json",
    })
    for unit in doc["units"]:
        unit_id = unit["unit_id"]
        suffixes = list(COMMON_OUTPUTS)
        if unit_id == "SWU-IRO-001":
            suffixes.extend(IRO_001_OUTPUTS)
            unit["owner_material_scope"] = []
        unit["runtime_outputs"] = [f"{unit_id}/{name}" for name in suffixes]
        unit["continuity_cursor"] = (
            f".arcanum/task-session/continuity/IRO-FULL-STREAM-<epoch-id>-{unit_id}.json"
        )
    return rendered_json(doc)


def build_validator() -> bytes:
    path = ROOT / f"{PREFIX}/work-pack/shared/validate-execution-contract.py"
    text = path.read_text()
    text = text.replace(
        'if doc.get("schema_version") != "1.0.0":\n        errors.append("schema_version must be 1.0.0")',
        'if doc.get("schema_version") != "1.1.0":\n        errors.append("schema_version must be 1.1.0")',
    )
    text = text.replace(
        'EXPECTED = [\n',
        'COMMON_RUNTIME_OUTPUTS = [\n'
        '    "CONTEXT-PACK.md", "CONTEXT-PACK.json", "closeout-preflight.json",\n'
        '    "mutation-admission-request.json", "mutation-admission-receipt.json",\n'
        '    "terminal-receipt.json", "closeout-sync-request.json",\n'
        '    "closeout-owner-receipt.json", "continuation-route.json",\n'
        ']\n'
        'IRO_001_RUNTIME_OUTPUTS = [\n'
        '    "OPTION-ADMISSIBILITY-REQUEST.json",\n'
        '    "OPTION-ADMISSIBILITY-RECEIPT.json", "DECISION.json",\n'
        '    "DECISION-SUMMARY.md", "decision-bundle.json",\n'
        ']\n\n\n'
        'EXPECTED = [\n',
    )
    needle = '        if len(unit.get("coordinator_outputs", [])) != 2:\n            errors.append(f"{unit_id}: exactly two coordinator outputs required")\n'
    replacement = needle + (
        '        expected_runtime = [f"{unit_id}/{name}" for name in COMMON_RUNTIME_OUTPUTS]\n'
        '        if unit_id == "SWU-IRO-001":\n'
        '            expected_runtime.extend(f"{unit_id}/{name}" for name in IRO_001_RUNTIME_OUTPUTS)\n'
        '        if unit.get("runtime_outputs") != expected_runtime:\n'
        '            errors.append(f"{unit_id}: runtime output contract mismatch")\n'
        '        expected_cursor = f".arcanum/task-session/continuity/IRO-FULL-STREAM-<epoch-id>-{unit_id}.json"\n'
        '        if unit.get("continuity_cursor") != expected_cursor:\n'
        '            errors.append(f"{unit_id}: continuity cursor mismatch")\n'
        '        if unit_id == "SWU-IRO-001" and unit.get("owner_material_scope") != []:\n'
        '            errors.append("SWU-IRO-001: output-only unit must not declare owner material")\n'
    )
    if needle not in text:
        raise RuntimeError("validator insertion point missing")
    text = text.replace(needle, replacement)
    text = text.replace(
        'for name in ("terminal", "closeout_owner", "decision_bundle"):',
        'for name in ("terminal", "closeout_owner", "decision_bundle", "goal_start_approval", "closeout_preflight", "closeout_sync_request", "mutation_admission_request", "mutation_admission_receipt", "continuation_route", "continuity_cursor", "chain_config", "chain_transition"):',
    )
    insert = '    return errors\n\n\ndef self_test()'
    extra = (
        '    runtime = doc.get("runtime_evidence_contract", {})\n'
        '    if runtime.get("per_unit_outputs") != COMMON_RUNTIME_OUTPUTS:\n'
        '        errors.append("runtime evidence common output mismatch")\n'
        '    if runtime.get("iro_001_additional_outputs") != IRO_001_RUNTIME_OUTPUTS:\n'
        '        errors.append("IRO-001 additional output mismatch")\n'
        '    chain = doc.get("chain_runtime", {})\n'
        '    if len(chain.get("transition_receipts", [])) != len(EXPECTED):\n'
        '        errors.append("chain transition receipt count mismatch")\n'
        '    return errors\n\n\ndef self_test()'
    )
    if insert not in text:
        raise RuntimeError("validator final insertion point missing")
    return text.replace(insert, extra).encode()


def exact_ref_schema() -> dict[str, object]:
    return {
        "type": "object", "additionalProperties": False,
        "required": ["path", "sha256", "size_bytes"],
        "properties": {
            "path": {"type": "string", "minLength": 1},
            "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
            "size_bytes": {"type": "integer", "minimum": 0},
        },
    }


def build_schemas() -> dict[str, bytes]:
    exact = exact_ref_schema()
    goal = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://domainspec.local/iro/goal-start-approval/1-0-0",
        "type": "object", "additionalProperties": False,
        "required": ["schema_version", "stream_id", "approval_status", "approval_owner", "approval_source", "approved_at", "epoch_binding", "approved_frontier", "authorized_scope", "denied_scopes", "authority_effect"],
        "properties": {
            "schema_version": {"const": "1.0.0"}, "stream_id": {"const": "IRO-FULL-STREAM"},
            "approval_status": {"const": "approved"}, "approval_owner": {"type": "string", "minLength": 1},
            "approval_source": {"const": "direct-user-start-goal"}, "approved_at": {"type": "string", "format": "date-time"},
            "epoch_binding": {"type": "object", "additionalProperties": False, "required": ["epoch_id", "audit_projection_digest", "canonical_semantic_digest", "source_snapshot_digest", "manifest_ref"], "properties": {
                "epoch_id": {"type": "string", "pattern": "^epoch-[a-f0-9]{24}$"},
                "audit_projection_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
                "canonical_semantic_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
                "source_snapshot_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"}, "manifest_ref": exact}},
            "approved_frontier": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"type": "string", "minLength": 1}},
            "authorized_scope": {"const": "outer-chain-start-and-SWU-IRO-001-execution-outputs-only"},
            "denied_scopes": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"type": "string", "minLength": 1}},
            "authority_effect": {"const": "none"},
        },
    }
    delta_values = [
        "evidence_added", "blocker_opened", "blocker_resolved",
        "status_changed", "route_changed",
    ]
    preflight_target = {
        "type": "object",
        "additionalProperties": False,
        "required": ["path", "baseline", "delta_classes"],
        "properties": {
            "path": {"type": "string", "minLength": 1},
            "baseline": {"type": "string", "pattern": "^(absent|[a-f0-9]{64})$"},
            "delta_classes": {
                "type": "array", "minItems": 1, "uniqueItems": True,
                "items": {"enum": delta_values},
            },
        },
    }
    preflight = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://domainspec.local/iro/closeout-preflight/1-0-0",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version", "task_id", "swu_id", "result",
            "work_pack_ref", "terminal_schema_ref", "owner_schema_ref",
            "targets", "allowed_delta_classes", "validation_commands",
            "canonical_successor", "authority_effect",
        ],
        "properties": {
            "schema_version": {"const": "task-session.closeout-preflight.v1"},
            "task_id": {"type": "string", "minLength": 1},
            "swu_id": {"type": "string", "minLength": 1},
            "result": {"enum": ["PROCEED", "BLOCK"]},
            "work_pack_ref": exact,
            "terminal_schema_ref": exact,
            "owner_schema_ref": exact,
            "targets": {"type": "array", "items": preflight_target},
            "allowed_delta_classes": {
                "type": "array", "minItems": 1, "uniqueItems": True,
                "items": {"enum": delta_values},
            },
            "validation_commands": {
                "type": "array", "minItems": 1,
                "items": {"type": "string", "minLength": 1},
            },
            "canonical_successor": {"type": "string", "minLength": 1},
            "authority_effect": {"const": "none"},
        },
    }
    sync_target = {
        "type": "object",
        "additionalProperties": False,
        "required": ["path", "baseline", "delta_class", "expected_post_state"],
        "properties": {
            "path": {"type": "string", "minLength": 1},
            "baseline": {"type": "string", "pattern": "^(absent|[a-f0-9]{64})$"},
            "delta_class": {"enum": delta_values},
            "expected_post_state": {"type": "string", "minLength": 1},
        },
    }
    sync = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://domainspec.local/iro/closeout-sync-request/1-0-0",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version", "stream_id", "unit_id", "route",
            "source_terminal_ref", "targets", "validation_commands",
            "expected_owner_receipt_path", "canonical_successor",
            "authority_effect",
        ],
        "properties": {
            "schema_version": {"const": "1.0.0"},
            "stream_id": {"const": "IRO-FULL-STREAM"},
            "unit_id": {"type": "string", "minLength": 1},
            "route": {"const": "invoke:refresh:apply-approved"},
            "source_terminal_ref": exact,
            "targets": {"type": "array", "items": sync_target},
            "validation_commands": {
                "type": "array", "minItems": 1,
                "items": {"type": "string", "minLength": 1},
            },
            "expected_owner_receipt_path": {"type": "string", "minLength": 1},
            "canonical_successor": {"type": "string", "minLength": 1},
            "authority_effect": {"const": "none"},
        },
    }
    return {
        f"{PREFIX}/work-pack/shared/GOAL-START-APPROVAL.schema.json": rendered_json(goal),
        f"{PREFIX}/work-pack/shared/CLOSEOUT-PREFLIGHT.schema.json": rendered_json(preflight),
        f"{PREFIX}/work-pack/shared/CLOSEOUT-SYNC-REQUEST.schema.json": rendered_json(sync),
    }


def build_markdown() -> dict[str, bytes]:
    docs: dict[str, bytes] = {}
    runtime_doc = """# Runtime evidence contract

Every unit receives nine exact Task Session support outputs: strict Context
Markdown/JSON, closeout preflight, mutation-admission request/receipt, terminal
receipt, closeout-sync request, joined owner receipt, and Continuation Router
receipt. Each unit also writes one exact repository-local continuity cursor.
IRO-001 adds the four Decision Gate artifacts plus `decision-bundle.json`.

The outer chain writes a Goal-start approval receipt, chain config, preflight,
immutable `chain.json`, and ten numbered transition receipts. These paths are
templates in `EXECUTION-CONTRACT.json` and are concretized by the strict
Context/WPRA epoch. They are execution evidence, never owner material.

No Task Session write is admitted unless its strict Context JSON repeats the
complete `materialWrites`, `executionOutputs`, `allowedWrites`, validation,
lifecycle owner, authority, and publication tuple consumed by
`verify-mutation-readiness.py`.
"""
    docs[f"{PREFIX}/work-pack/shared/RUNTIME-EVIDENCE.md"] = runtime_doc.encode()

    updates = {
        f"{PREFIX}/WORK-PACK.md": (
            "runtime-admission-repair-applied; WPRA regeneration required before execution",
            "## Runtime admission repair\n\nThe prior WPRA epoch omitted Task Session support outputs and is superseded. `RUNTIME-EVIDENCE.md` and execution-contract v1.1 bind the complete per-unit and outer-chain evidence paths. A new strict Context/WPRA epoch is mandatory before Goal activation evidence is written."
        ),
        f"{PREFIX}/EXECUTION-PACK.md": (
            None,
            "## Runtime receipt closure\n\nEvery unit must use the runtime output matrix in `work-pack/shared/RUNTIME-EVIDENCE.md`. The Goal-start approval and chain ledger are outer evidence; unit Context/admission/closeout/router/cursor artifacts remain unit evidence. The earlier six-output IRO-001 projection is superseded and must not be consumed."
        ),
        f"{PREFIX}/goals/IRO-FULL-STREAM/GOAL-SIDECAR.md": (
            None,
            "## Runtime repair state\n\nThe frozen `20260802T013311Z` epoch is superseded because it omitted mandatory Task Session support outputs. Native execution remains not admitted until a new strict Context/WPRA epoch passes and the direct Goal-start instruction is persisted against that exact manifest."
        ),
        f"{PREFIX}/goals/IRO-FULL-STREAM/IRO-FULL-STREAM.md": (
            None,
            "## Runtime evidence matrix\n\nExecution contract v1.1 adds the complete Task Session and outer-chain receipt set. The prior WPRA epoch is stale by the stream's own epoch rule; the next runnable frontier remains IRO-001 only after regeneration and exact Goal-start approval."
        ),
        f"{PREFIX}/work-pack/shared/CLOSEOUT-SYNC.md": (
            None,
            "## Runtime support receipts\n\nBefore a unit write, persist a schema-valid `closeout-preflight.json`. Before closeout dispatch, persist `closeout-sync-request.json`; Continuation Router then persists `continuation-route.json`, joins `closeout-owner-receipt.json`, and Task Session writes the unit-specific continuity cursor declared by the execution contract."
        ),
    }
    for path, (replacement_status, addition) in updates.items():
        text = (ROOT / path).read_text()
        if replacement_status:
            text = text.replace("status: contract-repaired-not-executed", f"status: {replacement_status}")
        docs[path] = append_once(text, addition.splitlines()[0], addition).encode()
    return docs


def stage() -> None:
    outputs = build_markdown()
    outputs[f"{PREFIX}/work-pack/shared/EXECUTION-CONTRACT.json"] = build_contract()
    outputs[f"{PREFIX}/work-pack/shared/validate-execution-contract.py"] = build_validator()
    outputs.update(build_schemas())
    if sorted(outputs) != sorted(TARGETS):
        raise RuntimeError(f"target mismatch: {sorted(set(TARGETS) ^ set(outputs))}")

    for path, data in outputs.items():
        write_output(path, data)

    source_rel = "sources/SOURCE-SIGNAL.md"
    source_text = """# IRO-REFRESH-002 source signal

The first frozen WPRA epoch admitted only business receipts. Live Task Session
requires strict unit Context, closeout preflight, mutation-admission,
closeout-sync, Continuation Router, and continuity evidence; the outer chain
also requires exact approval/config/state/transition paths. The repair adds
those paths for all ten units and marks the earlier epoch superseded.
"""
    source_path = MATERIAL_ROOT / source_rel
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(source_text, encoding="utf-8")

    preimages: dict[str, object] = {}
    for path in TARGETS:
        live = ROOT / path
        preimages[path] = (
            {"state": "present", "sha256": digest(live.read_bytes()), "size_bytes": live.stat().st_size}
            if live.is_file() else {"state": "absent"}
        )
    preimage_path = MATERIAL_ROOT / "inputs/preimage-digests.json"
    preimage_path.parent.mkdir(parents=True, exist_ok=True)
    preimage_path.write_bytes(rendered_json(preimages))

    changes = []
    inventory = []
    for path in TARGETS:
        staged_rel = f"outputs/{path}"
        changes.append({
            "target_path": path,
            "operation": "update" if (ROOT / path).is_file() else "create",
            "output_ref": exact_ref(staged_rel, MATERIAL_ROOT),
        })
        inventory.append({
            "target_path": path,
            "lifecycle_owner": "intent-route-planning-owner",
            "authority_class": "private",
            "publication_class": "internal",
            "dependency_ids": ["runtime-repair-preimages-v1"],
        })
    validation = [
        f"python3 {PREFIX}/work-pack/shared/validate-execution-contract.py --self-test",
        f"python3 {PREFIX}/work-pack/shared/validate-execution-contract.py --root .",
        f"python3 -m json.tool {PREFIX}/work-pack/shared/EXECUTION-CONTRACT.json",
        f"git diff --check -- {PREFIX}",
    ]
    package = {
        "schema_version": "1.0.0",
        "package_id": "iro-refresh-002-runtime-admission-contract-v1",
        "mutation_mode": "apply-approved", "mutation_state": "materialized",
        "lifecycle_owner": "intent-route-planning-owner",
        "authority_class": "private", "publication_class": "internal",
        "source_artifacts": [
            {**exact_ref(source_rel, MATERIAL_ROOT), "authority_class": "private"}
        ],
        "changes": changes, "target_inventory": inventory,
        "dependencies": [{"dependency_id": "runtime-repair-preimages-v1", "artifact_ref": exact_ref("inputs/preimage-digests.json", MATERIAL_ROOT)}],
        "mirror_groups": [],
        "approval": {"class": "explicit-apply", "owner": "intent-route-planning-owner", "scope_paths": TARGETS, "authority_classes": ["private"], "publication_classes": ["internal"]},
        "validation_commands": validation,
    }
    (MATERIAL_ROOT / "material-package.json").write_bytes(rendered_json(package))


def apply() -> None:
    handoff = json.loads((MATERIAL_ROOT / "refresh-handoff-result.json").read_text())
    receipt = json.loads((MATERIAL_ROOT / "material-package-receipt.json").read_text())
    package = json.loads((MATERIAL_ROOT / "material-package.json").read_text())
    if not (handoff.get("mutationReady") is True and receipt.get("patchVerdict") == "pass"):
        raise RuntimeError("material handoff is not ready")
    preimages = json.loads((MATERIAL_ROOT / "inputs/preimage-digests.json").read_text())
    for target in TARGETS:
        live = ROOT / target
        expected = preimages[target]
        if expected["state"] == "present":
            if not live.is_file() or digest(live.read_bytes()) != expected["sha256"]:
                raise RuntimeError(f"live baseline drift: {target}")
        elif live.exists():
            raise RuntimeError(f"expected absent target exists: {target}")
    applied = []
    for change in package["changes"]:
        target = change["target_path"]
        staged = MATERIAL_ROOT / change["output_ref"]["path"]
        live = ROOT / target
        live.parent.mkdir(parents=True, exist_ok=True)
        live.write_bytes(staged.read_bytes())
        data = live.read_bytes()
        applied.append({"target_path": target, "operation": change["operation"], "post_sha256": digest(data), "post_size_bytes": len(data), "staged_byte_parity": data == staged.read_bytes()})
    result = {
        "schema_version": "1.0.0", "refresh_id": "IRO-REFRESH-002",
        "package_id": receipt["packageId"], "package_digest": receipt["packageDigest"],
        "material_receipt_verdict": receipt["patchVerdict"], "handoff_status": handoff["handoffStatus"],
        "mutation_ready": handoff["mutationReady"], "apply_status": "pass",
        "targets": applied,
        "claim_ceiling": "runtime-admission planning contract repaired; new Context/WPRA epoch still required",
    }
    (MATERIAL_ROOT / "material-apply-receipt.json").write_bytes(rendered_json(result))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("stage", "apply"))
    args = parser.parse_args()
    stage() if args.mode == "stage" else apply()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
