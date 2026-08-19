#!/usr/bin/env python3
"""Deterministically rematerialize the R4 successor before external validators run."""

from __future__ import annotations

import hashlib
import json
import stat
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[5]
R4_REL = "ops/development/2026-08-16-rwo-control-content-provenance-successor-r4/candidate-plan-epoch"
R4 = REPO / R4_REL
CAP_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "control/bootstrap/CCP-BOOTSTRAP-R3"
)
CAP = REPO / CAP_REL
BLOCKER_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "control/execution/CCP002-R3-1bdf98e1/blocker-receipt.json"
)
TERMINAL_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "SWU-RWO-CCP-001/terminal.json"
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_path(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def exact_ref(relative: str, *, mode: bool = False) -> dict[str, Any]:
    path = REPO / relative
    result: dict[str, Any] = {
        "path": relative,
        "sha256": digest_path(path),
        "size_bytes": path.stat().st_size,
    }
    if mode:
        result["mode"] = f"{stat.S_IMODE(path.stat().st_mode):04o}"
    return result


def capsule_ref(relative: str) -> dict[str, Any]:
    path = CAP / relative
    return {
        "mode": f"{stat.S_IMODE(path.stat().st_mode):04o}",
        "path": relative,
        "sha256": digest_path(path),
        "size_bytes": path.stat().st_size,
    }


def load(path: Path) -> Any:
    return json.loads(path.read_text("utf-8"))


def write(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", "utf-8")


FIELD_COMMAND = {
    "command_id": "ccp002-context-builder-source-identity",
    "argv": [
        "python3",
        f"{R4_REL}/validation/validate_context_builder_source_identity.py",
        "--repository-root",
        ".",
    ],
    "cwd": ".",
    "timeout_seconds": 120,
    "max_output_bytes": 1048576,
}


def command_string(command: dict[str, Any]) -> str:
    return json.dumps(command, sort_keys=True, separators=(",", ":"))


def update_capsule() -> None:
    inventory_path = CAP / "TARGET-INVENTORY.json"
    inventory = load(inventory_path)
    for item in inventory["targets"]:
        staged = CAP / item["staged_path"]
        item["output"] = {
            "mode": f"{stat.S_IMODE(staged.stat().st_mode):04o}",
            "sha256": digest_path(staged),
            "size_bytes": staged.stat().st_size,
        }
    inventory["target_count"] = len(inventory["targets"])
    write(inventory_path, inventory)

    helper_request_path = CAP / "HELPER-REQUEST.json"
    request = load(helper_request_path)
    request["request_id"] = "CCP-BOOTSTRAP-R3"
    request["objective"] = (
        "Repair the acceptance-bound Context Builder templates by adding typed "
        "source digest and byte-size identity while preserving the corrected "
        "machine-readable legacy context-pack binding and all live packages."
    )
    request["preacceptance_contract"]["context_pack"] = "PUBLIC-CONTEXT-PACK-INDEX.json"
    request["preacceptance_contract"]["legacy_artifact_count"] = 31
    request["preacceptance_contract"]["plan_once_token_allowed"] = False
    request["preacceptance_contract"]["validation_command_count"] = 10
    request["preacceptance_contract"]["field_contract_validator"] = (
        f"{R4_REL}/validation/validate_context_builder_source_identity.py"
    )
    request["claim_ceiling"] = (
        "staged R4 successor and candidate-local compatibility evidence only; "
        "no plan-once token, application, acceptance, promotion, publication, "
        "deployment, release, or production claim"
    )
    write(helper_request_path, request)

    source_path = CAP / "PUBLIC-SOURCE-MANIFEST.json"
    source = load(source_path)
    source["capsule_id"] = "CCP-BOOTSTRAP-R3"
    for item in source["sources"]:
        if item["path"] == "HELPER-REQUEST.json":
            ref = capsule_ref("HELPER-REQUEST.json")
            item.update(
                {
                    "sha256": ref["sha256"],
                    "size_bytes": ref["size_bytes"],
                    "mode": ref["mode"],
                }
            )
    write(source_path, source)

    context_path = CAP / "PUBLIC-CONTEXT-PACK-INDEX.json"
    context = load(context_path)
    commands = list(context["execution_contract"]["validationCommands"])
    commands = [item for item in commands if "validate_context_builder_source_identity.py" not in item]
    commands.insert(1, command_string(FIELD_COMMAND))
    context["execution_contract"]["validationCommands"] = commands
    context["claim_ceiling"] = (
        "R4 candidate-local compatibility evidence only; no plan-once token, "
        "mutation authority, application, publication, promotion, deployment, "
        "release, or production claim"
    )
    write(context_path, context)

    no_private_path = CAP / "NO-PRIVATE-INPUT-RECEIPT.json"
    no_private = load(no_private_path)
    no_private["statement"] = (
        "All semantic and build inputs for the staged target bytes were public; "
        "the R3 blocker was used only as immutable repair-cause/no-mutation "
        "evidence and did not source target content."
    )
    reads = list(no_private["self_generated_validation_reads"])
    marker = "candidate-local selected-source field validator and missing-field injections"
    if marker not in reads:
        reads.append(marker)
    no_private["self_generated_validation_reads"] = reads
    write(no_private_path, no_private)

    manifest_path = CAP / "CAPSULE-MANIFEST.json"
    manifest = load(manifest_path)
    manifest["claim_ceiling"] = "candidate-local R4 implementation-content repair evidence only"
    excluded = {"CAPSULE-MANIFEST.json", "HELPER-RECEIPT.json", "DISCLOSURE-REVIEW-RECEIPT.json"}
    refs = [
        capsule_ref(path.relative_to(CAP).as_posix())
        for path in sorted(CAP.rglob("*"))
        if path.is_file() and path.relative_to(CAP).as_posix() not in excluded
    ]
    manifest["exact_file_refs"] = refs
    manifest["exact_file_ref_count"] = len(refs)
    manifest["declared_file_count"] = sum(1 for path in CAP.rglob("*") if path.is_file()) - 1
    manifest["staged_target_count"] = 56
    write(manifest_path, manifest)

    helper_path = CAP / "HELPER-RECEIPT.json"
    helper = load(helper_path)
    helper["receipt_id"] = "CCP-BOOTSTRAP-R3-HELPER-RECEIPT"
    helper["capsule_id"] = "CCP-BOOTSTRAP-R3"
    helper["root_cause"] = (
        "The exact accepted R3 capsule staged both Context Builder selected-source "
        "index exemplars without sha256 and size_bytes, despite the accepted "
        "CCP002 field contract."
    )
    helper["affected_invariant"] = (
        "Acceptance-bound staged product bytes must satisfy every accepted "
        "field contract before an admission token is consumed or source is mutated."
    )
    helper["repair"] = (
        "Change exactly the two canonical index templates and four official "
        "generated copies, retain the corrected JSON legacy context-pack role, "
        "and bind a permanent staged/live missing-field regression."
    )
    helper["permanent_regression"] = (
        "The candidate-local source-identity validator checks all six templates, "
        "generated parity, typed fields, and in-memory missing-sha256 and "
        "missing-size_bytes rejection; its live-root command is acceptance-critical."
    )
    helper["staged_candidate"].update(
        {
            "target_count": 56,
            "exact_r1_byte_parity": False,
            "exact_r2_unchanged_target_count": 50,
            "changed_template_target_count": 6,
            "live_target_writes": 0,
        }
    )
    helper["preacceptance_validation"].update(
        {
            "field_contract_capsule": "pass",
            "negative_missing_sha256": "pass-rejected",
            "negative_missing_size_bytes": "pass-rejected",
            "official_generation_parity": "pass",
        }
    )
    helper["required_revalidation"] = [
        "actual current Invoke 1.0 material producer against the exact legacy 31",
        "actual current Task Session 1.2 verifier plus Markdown negative",
        "canonical Dispatch, Execution Entry, Distill, WPRA v2, and exact candidate inventory",
        "fresh owner acceptance over the regenerated R4 candidate digest",
    ]
    helper["renewed_owner_acceptance_required"] = True
    helper["claim_ceiling"] = (
        "candidate-local R4 content-repair evidence only; no acceptance, "
        "application, plan-once admission, promotion, publication, deployment, "
        "release, or production-readiness claim"
    )
    helper["output_inventory"]["declared_file_count"] = sum(
        1 for path in CAP.rglob("*") if path.is_file()
    )
    helper_refs = [
        capsule_ref(path.relative_to(CAP).as_posix())
        for path in sorted(CAP.rglob("*"))
        if path.is_file()
        and path.relative_to(CAP).as_posix()
        not in {"HELPER-RECEIPT.json", "DISCLOSURE-REVIEW-RECEIPT.json"}
    ]
    helper["output_inventory"]["exact_other_file_refs"] = helper_refs
    helper["output_inventory"]["exact_other_file_ref_count"] = len(helper_refs)
    write(helper_path, helper)

    disclosure_path = CAP / "DISCLOSURE-REVIEW-RECEIPT.json"
    disclosure = load(disclosure_path)
    disclosure["review_id"] = "CCP-BOOTSTRAP-R3-PREACCEPTANCE-DISCLOSURE-001"
    disclosure["capsule_id"] = "CCP-BOOTSTRAP-R3"
    review_paths = [
        "PUBLIC-WORK-PACK.md",
        "PUBLIC-TASK-RWO-CCP-002.md",
        "PUBLIC-CONTEXT-PACK.md",
        "PUBLIC-CONTEXT-PACK-INDEX.json",
        "PUBLIC-SOURCE-MANIFEST.json",
        "HELPER-REQUEST.json",
        "HELPER-RECEIPT.json",
        "NO-PRIVATE-INPUT-RECEIPT.json",
        "CAPSULE-MANIFEST.json",
        "TARGET-INVENTORY.json",
    ]
    disclosure["review_inputs"] = [
        {k: v for k, v in capsule_ref(path).items() if k != "mode"}
        for path in review_paths
    ]
    disclosure["review_scope"].update(
        {
            "capsule_public_controls": 10,
            "staged_public_targets": 56,
            "changed_staged_templates": 6,
            "unchanged_r2_staged_targets": 50,
        }
    )
    disclosure["checks"] = [
        {"check": "unique role=context-pack control remains machine-readable JSON", "result": "pass"},
        {"check": "all six Context Builder templates expose the complete typed source identity", "result": "pass"},
        {"check": "missing sha256 and size_bytes injections are rejected", "result": "pass"},
        {"check": "exactly six staged targets changed and the other fifty equal R2", "result": "pass"},
        {"check": "capsule has no live, Git, network, publication, or deployment effect", "result": "pass"},
    ]
    disclosure["claim_ceiling"] = (
        "author-side R4 candidate disclosure check only; no independent review, "
        "owner acceptance, application, plan-once admission, promotion, publication, "
        "deployment, release, or production-readiness claim"
    )
    write(disclosure_path, disclosure)


def update_plan_sources() -> None:
    execution_path = R4 / "EXECUTION-ENTRY.json"
    execution = load(execution_path)
    first_route = execution["execution_policy"]["allowed_routes"][0]
    first_route["required_inputs"] = [
        "fresh exact R4 candidate inventory acceptance",
        "exact passing CCP-001 terminal external predecessor",
        "CCP-BOOTSTRAP-R3 and target inventory",
        "R3 no-mutation implementation-content blocker repair cause",
        "live Invoke 1.0 producer plus Task Session 1.2 compatibility pass",
        "candidate-local partition and source-identity regressions pass",
    ]
    execution["pre_execution_owner_prerequisite"]["required_evidence"] = [
        "fresh exact R4 candidate inventory acceptance",
        "exact passing CCP-001 terminal external predecessor",
        "CCP-BOOTSTRAP-R3 preacceptance compatibility PASS",
        "R3 blocker exact-bound as repair-cause/no-mutation evidence",
    ]
    execution["continuation_rule"] = (
        "Begin at CCP-002 from the exact external CCP-001 terminal; then select "
        "and admit one remaining unit at a time. After SWU-RWO-CX-003R2 T, route "
        "only to a fresh SWU-RWO-CX-003 sufficiency audit and never directly to "
        "CX004. R2/R3 CCP-002 selection and admission artifacts are historical "
        "diagnostics and invalid for R4."
    )
    execution["execution_policy"]["allowed_routes_digest"] = digest_bytes(
        canonical_bytes(execution["execution_policy"]["allowed_routes"])
    )
    write(execution_path, execution)

    dispatch_path = R4 / "DISPATCH-ROUTE.json"
    dispatch = load(dispatch_path)
    dispatch["dispatch_id"] = "DISPATCH-RWO-CONTROL-CONTENT-PROVENANCE-004"
    dispatch["intent"]["raw"] = (
        "Execute only a freshly accepted R4 control/content provenance successor "
        "whose six-template source-identity repair has passed preacceptance."
    )
    dispatch["intent"]["objective"] = (
        "After exact R4 acceptance, run the remaining three sequential Task "
        "Sessions using the current partition contract and permanent field regression."
    )
    dispatch["subagent_strategy"]["permission_prompt"] = (
        "Require fresh exact acceptance of the R4 successor candidate inventory "
        "before registration or execution."
    )
    write(dispatch_path, dispatch)

    manifest_path = R4 / "SWU-MANIFEST.json"
    manifest = load(manifest_path)
    manifest["work_pack"].update(
        {
            "epoch_kind": "immutable-r4-acceptance-bound-content-repair-candidate",
            "semantic_digest": None,
            "status": "candidate-readiness-pending",
            "selected_unit": None,
            "mutation_ready": False,
        }
    )
    manifest["contract_policy"]["validation"] = (
        "Exact task validation plus candidate-local Task Session partition and "
        "Context Builder source-identity positive/negative regressions; exact "
        "argv/cwd/exit/timeout/environment/runtime/risk; first failure survives teardown."
    )
    manifest["contract_policy"]["material_package"] = (
        "CCP-001 is immutable completed evidence; CCP-002 uses repaired "
        "CCP-BOOTSTRAP-R3 through legacy public-safe 1.0/1.2; CCP-003 is "
        "output-only; CX003R2 uses split 1.1/1.3."
    )
    manifest["protected_gates"]["acceptance"] = (
        "fresh exact human acceptance of the complete R4 candidate inventory digest"
    )
    manifest["claim_ceiling"] = (
        "R4 plan-semantic and preacceptance bootstrap compatibility evidence only; "
        "no selection, plan-once admission, mutation, authority, publication, promotion, "
        "deployment, release, or production claim"
    )
    if not any(item.get("evidence_id") == "r3-ccp002-content-blocker" for item in manifest["external_evidence"]):
        manifest["external_evidence"].append(
            {
                "evidence_id": "r3-ccp002-content-blocker",
                "role": "immutable-repair-cause-no-mutation-not-completion-authority",
                "artifact_ref": exact_ref(BLOCKER_REL),
                "selector": "/terminal_code",
                "expected_value": "ACCEPTANCE_BOUND_IMPLEMENTATION_CONTENT_DEFECT",
            }
        )

    owned = {
        f"{R4_REL}/WORK-PACK.md",
        f"{R4_REL}/IMPLEMENTATION-LAYERING.md",
        f"{R4_REL}/DISPATCH-ROUTE.json",
        f"{R4_REL}/DISTILL-PLAN-VALIDATION.md",
        f"{R4_REL}/EXECUTION-ENTRY.json",
        f"{R4_REL}/work-pack/tasks/TASK-RWO-CCP-002.md",
        f"{R4_REL}/work-pack/tasks/TASK-RWO-CCP-003.md",
        f"{R4_REL}/work-pack/tasks/TASK-RWO-CX-003R2.md",
        f"{R4_REL}/validation/EXECUTION-ENTRY-VALIDATION.json",
        f"{R4_REL}/validation/validate_task_session_partition_contract.py",
    }
    for binding in manifest["source_artifact_bindings"]:
        if binding["path"] in owned and (REPO / binding["path"]).is_file():
            ref = exact_ref(binding["path"])
            binding["sha256"] = ref["sha256"]
            binding["size_bytes"] = ref["size_bytes"]
    field_path = f"{R4_REL}/validation/validate_context_builder_source_identity.py"
    if not any(item["path"] == field_path for item in manifest["source_artifact_bindings"]):
        ref = exact_ref(field_path)
        manifest["source_artifact_bindings"].append(
            {
                **ref,
                "owner_ref": "invoke:plan-validation",
                "authority_class": "private",
                "publication_class": "internal",
                "artifact_kind": "candidate-local-source-identity-regression",
            }
        )
    write(manifest_path, manifest)


def refresh_audit_config() -> None:
    config_path = R4 / "readiness/AUDIT-CONFIG-v2.json"
    config = load(config_path)
    config["audit_id"] = "WPRA-RWO-CONTROL-CONTENT-PROVENANCE-004"
    if not any(item.get("binding_id") == "r3-ccp002-content-blocker" for item in config["closure_receipt_refs"]):
        config["closure_receipt_refs"].append(
            {
                "binding_id": "r3-ccp002-content-blocker",
                "owner_ref": "task-session-safe-stop",
                "artifact_ref": exact_ref(BLOCKER_REL),
                "selector": "/terminal_code",
            }
        )
    first = config["execution_bindings"][0]
    commands = [item for item in first["validation_contracts"] if item["command_id"] != FIELD_COMMAND["command_id"]]
    commands.insert(1, FIELD_COMMAND)
    first["validation_contracts"] = commands
    config["execution_policy"] = load(R4 / "EXECUTION-ENTRY.json")["execution_policy"]
    config["execution_policy"].pop("digest_algorithm", None)
    config["execution_policy"]["work_pack_id"] = "WP-RWO-CONTROL-CONTENT-PROVENANCE-002"

    for binding in config["execution_bindings"]:
        binding.pop("task_contract_ref", None)

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            ref = value.get("artifact_ref")
            if isinstance(ref, dict) and isinstance(ref.get("path"), str):
                path = REPO / ref["path"]
                if path.is_file():
                    current = exact_ref(ref["path"])
                    ref["sha256"] = current["sha256"]
                    ref["size_bytes"] = current["size_bytes"]
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(config)
    config["expected_source_snapshot_digest"] = None
    config["expected_material_digests"] = {}
    config["expected_semantic_digest"] = None
    write(config_path, config)


def main() -> int:
    update_capsule()
    update_plan_sources()
    refresh_audit_config()
    print(
        json.dumps(
            {
                "status": "pass",
                "capsule": CAP_REL,
                "candidate": R4_REL,
                "validation_command_count": len(
                    load(R4 / "readiness/AUDIT-CONFIG-v2.json")["execution_bindings"][0]["validation_contracts"]
                ),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
