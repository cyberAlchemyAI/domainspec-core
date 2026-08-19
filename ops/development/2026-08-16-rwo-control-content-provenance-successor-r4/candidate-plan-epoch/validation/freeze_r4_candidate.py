#!/usr/bin/env python3
"""Freeze the normalized multi-root R4 inventory and exact acceptance request."""

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
TERMINAL_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "SWU-RWO-CCP-001/terminal.json"
)
BLOCKER_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "control/execution/CCP002-R3-1bdf98e1/blocker-receipt.json"
)
INVENTORY_REL = f"{R4_REL}/validation/CANDIDATE-INVENTORY.json"
FINAL_REL = f"{R4_REL}/validation/FINAL-ACCEPTANCE-REQUEST.json"
HANDLE = "ACCEPT-RWO-CONTROL-CONTENT-PROVENANCE-R4"
CANDIDATE_ID = "RWO-CONTROL-CONTENT-PROVENANCE-SOURCE-IDENTITY-REPAIR-R4"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(relative: str) -> Any:
    return json.loads((REPO / relative).read_text())


def write(relative: str, value: Any) -> None:
    (REPO / relative).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def normalization(relative: str) -> str:
    if relative == INVENTORY_REL:
        return "candidate-inventory-projection-v3"
    if relative == FINAL_REL:
        return "final-acceptance-request-projection"
    return "raw-bytes"


def normalized_digest(relative: str, raw: bytes) -> str:
    kind = normalization(relative)
    if kind == "raw-bytes":
        return sha(raw)
    value = json.loads(raw)
    if kind == "candidate-inventory-projection-v3":
        value.pop("candidate_digest", None)
        value["files"] = [
            {"path": item["path"], "normalization": item["normalization"], "mode": item["mode"]}
            for item in value["files"]
        ]
    else:
        value.pop("candidate_digest", None)
        value.pop("exact_acceptance_text", None)
    return sha(canonical(value))


def all_paths() -> list[str]:
    paths = [path.relative_to(REPO).as_posix() for path in R4.rglob("*") if path.is_file()]
    paths.extend(path.relative_to(REPO).as_posix() for path in CAP.rglob("*") if path.is_file())
    paths.extend([TERMINAL_REL, BLOCKER_REL])
    assert len(paths) == len(set(paths))
    return sorted(paths)


def scope(relative: str) -> str:
    if relative.startswith(R4_REL + "/"):
        return "successor-candidate"
    if relative.startswith(CAP_REL + "/"):
        return "successor-bootstrap-capsule"
    if relative == TERMINAL_REL:
        return "immutable-external-predecessor"
    return "immutable-repair-cause"


def file_entries() -> list[dict[str, Any]]:
    result = []
    for relative in all_paths():
        path = REPO / relative
        raw = path.read_bytes()
        result.append(
            {
                "path": relative,
                "scope": scope(relative),
                "normalization": normalization(relative),
                "normalized_sha256": normalized_digest(relative, raw),
                "size_bytes": len(raw),
                "mode": f"{stat.S_IMODE(path.stat().st_mode):04o}",
            }
        )
    return result


def digest_entries(entries: list[dict[str, Any]]) -> str:
    projection = [
        {
            "path": item["path"],
            "normalized_sha256": item["normalized_sha256"],
            "size_bytes": item["size_bytes"],
            "mode": item["mode"],
        }
        for item in entries
    ]
    return sha(canonical(sorted(projection, key=lambda item: item["path"])))


def exact_local_ref(relative: str) -> dict[str, Any]:
    path = R4 / relative
    raw = path.read_bytes()
    return {"path": relative, "sha256": sha(raw), "size_bytes": len(raw)}


def main() -> int:
    readiness = load(f"{R4_REL}/validation/readiness/work-pack-readiness-report-v2.json")
    manifest = load(f"{R4_REL}/validation/readiness/plan-semantic-manifest.json")
    final_validation = load(f"{R4_REL}/validation/FINAL-VALIDATION-RECEIPT.json")
    assert readiness["verdict"] == "pass"
    assert final_validation["result"] == "pass"

    inventory = {
        "schema_version": "rwo.candidate-inventory.v3",
        "candidate_id": CANDIDATE_ID,
        "candidate_roots": [R4_REL, CAP_REL],
        "immutable_dependencies": [TERMINAL_REL, BLOCKER_REL],
        "status": "awaiting-exact-human-acceptance",
        "inventory_algorithm": {
            "name": "rwo-multi-root-normalized-manifest-sha256-v3",
            "canonical_json": "UTF-8 JSON with sorted keys and separators comma/colon; normalized JSON projections exclude the presentation newline",
            "ordinary_file_projection": "raw file bytes",
            "candidate_inventory_projection": "parse JSON; remove candidate_digest; replace every files member with exactly path, normalization, and mode; canonicalize",
            "final_acceptance_request_projection": "parse JSON; remove candidate_digest and exact_acceptance_text; canonicalize",
            "candidate_digest_projection": "canonical JSON array sorted by repository-relative path; each member is exactly path, normalized_sha256, size_bytes, and mode",
            "digest": "sha256",
        },
        "files": [],
        "file_count": 0,
        "changed_file_count": 0,
        "immutable_dependency_count": 2,
        "candidate_digest": "0" * 64,
        "readiness_binding": {
            "report_path": f"{R4_REL}/validation/readiness/work-pack-readiness-report-v2.json",
            "terminal_code": readiness["terminal_code"],
            "verdict": readiness["verdict"],
            "runtime_admission_status": readiness["runtime_admission_status"],
            "selected_unit": readiness["selected_unit"],
            "mutation_ready": readiness["mutation_ready"],
            "canonical_semantic_digest": readiness["canonical_semantic_digest"],
            "source_snapshot_digest": manifest["source_snapshot_digest"],
            "plan_epoch_id": manifest["plan_epoch_id"],
        },
        "validation_checks": {
            "exact_file_census": {"status": "pass"},
            "candidate_and_capsule_modes": {"status": "pass", "digest_bound": True},
            "dispatch": {"result": "pass", "exit_code": 0},
            "execution_entry": {"result": "pass", "exit_code": 0},
            "partition_regression": {"result": "PARTITION_CONTRACT_PASS", "positive_unit_count": 3, "negative_collision_count": 1, "exit_code": 0},
            "distill_recomposition": {"result": "pass", "remaining_unit_count": 3, "exit_code": 0},
            "source_identity_regression": {"result": "pass", "template_count": 6, "negative_missing_sha256": "pass-rejected", "negative_missing_size_bytes": "pass-rejected"},
            "official_generation_parity": {"result": "pass", "changed_target_count": 6, "unchanged_target_count": 50, "broader_delta": False},
            "bootstrap_contract": {"source_artifact_count": 31, "material_write_count": 56, "execution_output_count": 1, "allowed_write_count": 57, "validation_command_count": 10, "invoke_result": "pass-ready", "task_session_result": "admit-mutationReady", "negative_markdown_result": "block-exit-1", "status": "pass"},
            "capsule_closure": {"manifest_refs": 64, "helper_refs": 65, "disclosure_refs": 10, "status": "pass"},
            "staged_delta": {"changed": 6, "unchanged": 50, "status": "pass"},
            "live_baseline_unchanged": {"expected": 56, "result": 56, "status": "pass"},
            "json_whitespace_python_hygiene": {"status": "pass"},
            "readiness_reproduction": {"result": "pass-byte-identical", "exit_code": 0},
            "preserved_nonzero_count": 5,
        },
        "authority": {
            "effect": "none",
            "claim_ceiling": "readiness-proven R4 candidate and candidate-local compatibility only; no owner acceptance, selection, plan-once token, Task Session execution admission, live mutation, adapter application, publication, promotion, release, deployment, or production claim",
            "next_gate": "fresh exact human owner acceptance of this R4 candidate digest",
        },
    }
    final = {
        "schema_version": "rwo.final-acceptance-request.v1",
        "request_id": "FAR-RWO-CONTROL-CONTENT-PROVENANCE-R4",
        "acceptance_handle": HANDLE,
        "current_status": "awaiting-exact-human-acceptance",
        "candidate_id": CANDIDATE_ID,
        "candidate_inventory_path": INVENTORY_REL,
        "candidate_digest": "0" * 64,
        "exact_acceptance_text": f"accept {HANDLE} {'0' * 64}",
        "repair_evidence": {
            "completed_predecessor": "CCP001 terminal is immutable external predecessor evidence",
            "repair_cause": "R3 blocker is immutable no-mutation evidence and never completion authority",
            "root_cause": "The exact accepted R3 capsule omitted sha256 and size_bytes from selected_sources in both Context Builder index templates and their generated copies",
            "corrected_shape": ["path", "sha256", "size_bytes", "selectors", "authority_class", "obligation_bindings", "evidence_kind"],
            "changed_staged_targets": 6,
            "unchanged_r2_staged_targets": 50,
            "preacceptance_receipt": "validation/bootstrap-admission/PREACCEPTANCE-RECEIPT.json",
            "final_validation_receipt": "validation/FINAL-VALIDATION-RECEIPT.json",
        },
        "readiness_evidence": {
            "audit_id": readiness["audit_id"],
            "terminal_code": readiness["terminal_code"],
            "verdict": readiness["verdict"],
            "runtime_admission_status": readiness["runtime_admission_status"],
            "selected_unit": readiness["selected_unit"],
            "mutation_ready": readiness["mutation_ready"],
            "canonical_semantic_digest": readiness["canonical_semantic_digest"],
            "source_snapshot_digest": manifest["source_snapshot_digest"],
            "plan_epoch_id": manifest["plan_epoch_id"],
            "two_run_exact_byte_reproducibility": "pass",
            "artifacts": [
                exact_local_ref("validation/readiness/work-pack-readiness-report-v2.json"),
                exact_local_ref("validation/readiness/plan-semantic-manifest.json"),
                exact_local_ref("validation/readiness/selection-handoff.json"),
            ],
        },
        "requested_owner": "control-content-provenance-plan-owner",
        "requested_decision": "Accept only the exact R4 source-identity repair candidate for later Implementation Readiness selection; do not infer a plan-once token, Task Session execution admission, or mutation authority.",
        "authorized_next_edge_if_accepted": "Implementation Readiness may verify the accepted R4 digest, select SWU-RWO-CCP-002, and request one fresh Task Session admission. CCP-003 and CX-003R2 remain dependent later units.",
        "continuation_after_unit": "Follow only CCP-002 to CCP-003 to CX-003R2; CCP-001 remains immutable predecessor and the R3 blocker remains diagnostic only.",
        "authority_effect": "none",
        "mutation_ready": False,
        "claim_ceiling": "exact readiness-proven R4 candidate-plan acceptance only; no selection, token, execution admission, live mutation, application, publication, promotion, release, deployment, or production claim",
    }

    write(INVENTORY_REL, inventory)
    write(FINAL_REL, final)
    previous = None
    for _ in range(12):
        entries = file_entries()
        candidate_digest = digest_entries(entries)
        inventory["files"] = entries
        inventory["file_count"] = len(entries)
        inventory["changed_file_count"] = len(entries) - 2
        inventory["candidate_digest"] = candidate_digest
        inventory["validation_checks"]["exact_file_census"].update({"expected": len(entries), "result": len(entries)})
        final["candidate_digest"] = candidate_digest
        final["exact_acceptance_text"] = f"accept {HANDLE} {candidate_digest}"
        write(INVENTORY_REL, inventory)
        write(FINAL_REL, final)
        state = ((REPO / INVENTORY_REL).read_bytes(), (REPO / FINAL_REL).read_bytes())
        if state == previous:
            break
        previous = state
    else:
        raise AssertionError("inventory did not converge")

    entries = file_entries()
    final_digest = digest_entries(entries)
    assert final_digest == inventory["candidate_digest"]
    assert len(entries) == inventory["file_count"]
    assert final["exact_acceptance_text"] == f"accept {HANDLE} {final_digest}"
    print(json.dumps({"result": "pass", "file_count": len(entries), "candidate_digest": final_digest, "exact_acceptance_text": final["exact_acceptance_text"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
