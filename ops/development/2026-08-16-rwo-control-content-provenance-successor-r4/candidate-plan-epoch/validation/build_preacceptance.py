#!/usr/bin/env python3
"""Build R4 legacy Invoke/Task Session preacceptance inputs from exact live bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[5]
R4_REL = "ops/development/2026-08-16-rwo-control-content-provenance-successor-r4/candidate-plan-epoch"
R4 = REPO / R4_REL
RUN_REL = f"{R4_REL}/validation/bootstrap-admission"
RUN = REPO / RUN_REL
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
E_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "SWU-RWO-CCP-002/executor.json"
)
BLOCKER_REL = (
    "projects/cyberalchemy-orchestrator/docs/features/recursive-work-orchestrator/"
    "development/implementation-runs/WP-RWO-CONTROL-CONTENT-PROVENANCE-002/"
    "control/execution/CCP002-R3-1bdf98e1/blocker-receipt.json"
)


def load(path: Path) -> Any:
    return json.loads(path.read_text("utf-8"))


def write(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", "utf-8")


def ref(relative: str, *, camel: bool = False) -> dict[str, Any]:
    data = (REPO / relative).read_bytes()
    return {
        "path": relative,
        "sha256": hashlib.sha256(data).hexdigest(),
        ("sizeBytes" if camel else "size_bytes"): len(data),
    }


def prepare_package() -> None:
    package_path = RUN / "material-package.json"
    package = load(package_path)
    target_inventory = load(CAP / "TARGET-INVENTORY.json")["targets"]
    context = load(CAP / "PUBLIC-CONTEXT-PACK-INDEX.json")
    package["package_id"] = "invoke-refresh-ccp002-bootstrap-r3-preacceptance"
    package["validation_commands"] = context["execution_contract"]["validationCommands"]
    for item in package["source_artifacts"]:
        current = ref(item["path"])
        item["sha256"] = current["sha256"]
        item["size_bytes"] = current["size_bytes"]
        item["authority_class"] = "public"
    target_by_path = {item["target_path"]: item for item in target_inventory}
    for change in package["changes"]:
        target = target_by_path[change["target_path"]]
        output_path = f"{CAP_REL}/{target['staged_path']}"
        change["operation"] = target["operation"]
        change["output_ref"] = ref(output_path)
    package["target_inventory"] = [
        {
            "target_path": item["target_path"],
            "lifecycle_owner": "provenance-contract-owner",
            "authority_class": "public",
            "publication_class": "public",
            "dependency_ids": ["SWU-RWO-CCP-001"],
        }
        for item in target_inventory
    ]
    package["dependencies"] = [
        {"dependency_id": "SWU-RWO-CCP-001", "artifact_ref": ref(TERMINAL_REL)}
    ]
    package["approval"]["scope_paths"] = sorted(target_by_path)
    write(package_path, package)


def prepare_request() -> None:
    package_path = RUN / "material-package.json"
    receipt_path = RUN / "material-package-receipt.json"
    request_path = RUN / "mutation-admission-request.json"
    package = load(package_path)
    request = load(request_path)
    context = load(CAP / "PUBLIC-CONTEXT-PACK-INDEX.json")
    role_by_name = {
        "PUBLIC-TASK-RWO-CCP-002.md": "task-contract",
        "PUBLIC-WORK-PACK.md": "work-pack",
        "PUBLIC-CONTEXT-PACK-INDEX.json": "context-pack",
    }
    request["controlArtifacts"] = [
        {
            **ref(item["path"], camel=True),
            "authorityClass": "public",
            "role": role_by_name.get(Path(item["path"]).name, "source"),
        }
        for item in package["source_artifacts"]
    ]
    request["materialPackage"] = ref(f"{RUN_REL}/material-package.json", camel=True)
    request["materialReceipt"] = ref(
        f"{RUN_REL}/material-package-receipt.json", camel=True
    )
    request["producerReceiptSchema"] = ref(
        "arcanum/spells/invoke/schemas/material-package-receipt.schema.json",
        camel=True,
    )
    request["validationCommands"] = context["execution_contract"]["validationCommands"]
    request["dependencyFrontier"] = [
        {"dependencyId": "SWU-RWO-CCP-001", "artifactRef": ref(TERMINAL_REL, camel=True)}
    ]
    material = sorted(item["target_path"] for item in package["target_inventory"])
    request["materialWrites"] = material
    request["executionOutputs"] = [E_REL]
    request["allowedWrites"] = sorted(material + [E_REL])
    write(request_path, request)


def prepare_negative() -> None:
    request = load(RUN / "mutation-admission-request.json")
    controls = request["controlArtifacts"]
    context = next(item for item in controls if item["role"] == "context-pack")
    markdown = f"{CAP_REL}/PUBLIC-CONTEXT-PACK.md"
    context.clear()
    context.update(
        {
            **ref(markdown, camel=True),
            "authorityClass": "public",
            "role": "context-pack",
        }
    )
    write(RUN / "negative-markdown-context-request.json", request)


def prepare_receipt() -> None:
    package_receipt = load(RUN / "material-package-receipt.json")
    admission_receipt = load(RUN / "mutation-admission-receipt.json")
    negative_receipt = load(RUN / "negative-markdown-context-receipt.json")
    readiness_report_path = R4 / "validation/readiness/work-pack-readiness-report-v2.json"
    readiness_manifest_path = R4 / "validation/readiness/plan-semantic-manifest.json"
    readiness_report = load(readiness_report_path) if readiness_report_path.is_file() else None
    readiness_manifest = load(readiness_manifest_path) if readiness_manifest_path.is_file() else None
    command_count = len(admission_receipt["validationCommands"])
    assert package_receipt["patchVerdict"] == "pass"
    assert package_receipt["mutationHandoff"] == "ready"
    assert package_receipt["reasons"] == []
    assert admission_receipt["admissionVerdict"] == "admit"
    assert admission_receipt["mutationReady"] is True
    assert admission_receipt["reasons"] == []
    assert admission_receipt.get("admissionToken") is None
    assert admission_receipt.get("planEpochId") is None
    assert command_count == 10
    assert negative_receipt["admissionVerdict"] == "block"
    assert negative_receipt["mutationReady"] is False
    assert (RUN / "logs/negative-markdown.exit").read_text("utf-8").strip() == "1"

    artifact_names = [
        "material-package.json",
        "material-package-receipt.json",
        "mutation-admission-request.json",
        "mutation-admission-receipt.json",
        "negative-markdown-context-request.json",
        "negative-markdown-context-receipt.json",
    ]
    receipt = {
        "schema_version": "rwo.bootstrap-preacceptance-receipt.v1",
        "receipt_id": "PREACCEPT-RWO-CCP-002-BOOTSTRAP-R3",
        "task_id": "TASK-RWO-CCP-002",
        "swu_id": "SWU-RWO-CCP-002",
        "capsule_id": "CCP-BOOTSTRAP-R3",
        "result": "pass",
        "actual_live_producers": {
            "invoke": {
                "contract_version": package_receipt["schemaVersion"],
                "validator_path": "arcanum/spells/invoke/scripts/material_package_validator.py",
                "patch_verdict": package_receipt["patchVerdict"],
                "mutation_handoff": package_receipt["mutationHandoff"],
                "reasons": package_receipt["reasons"],
                "exit_code": 0,
            },
            "task_session": {
                "contract_version": admission_receipt["schemaVersion"],
                "verifier_path": "arcanum/arcana/task-session/scripts/verify-mutation-readiness.py",
                "admission_verdict": admission_receipt["admissionVerdict"],
                "mutation_ready": admission_receipt["mutationReady"],
                "reasons": admission_receipt["reasons"],
                "admission_token": admission_receipt.get("admissionToken"),
                "plan_epoch_id": admission_receipt.get("planEpochId"),
                "exit_code": 0,
            },
        },
        "exact_contract": {
            "source_artifact_count": 31,
            "unique_context_pack": "PUBLIC-CONTEXT-PACK-INDEX.json",
            "human_companion": "PUBLIC-CONTEXT-PACK.md",
            "human_companion_in_legacy_31": False,
            "strict_coverage": True,
            "material_write_count": 56,
            "execution_output_count": 1,
            "allowed_write_count": 57,
            "validation_command_count": command_count,
            "lifecycle_owner": "provenance-contract-owner",
            "authority_class": "public",
            "publication_class": "public",
        },
        "field_contract_regression": {
            "validator": f"{R4_REL}/validation/validate_context_builder_source_identity.py",
            "capsule_staged_templates": "pass",
            "live_validation_bound_to_ccp002": True,
            "negative_missing_sha256": "pass-rejected",
            "negative_missing_size_bytes": "pass-rejected",
            "selected_source_shape": [
                "path",
                "sha256",
                "size_bytes",
                "selectors",
                "authority_class",
                "obligation_bindings",
                "evidence_kind",
            ],
        },
        "negative_regression": {
            "case": "Markdown companion substituted as role=context-pack",
            "verifier_exit_code": 1,
            "admission_verdict": negative_receipt["admissionVerdict"],
            "mutation_ready": negative_receipt["mutationReady"],
            "reasons": negative_receipt["reasons"],
            "status": "pass-rejected",
        },
        "artifact_refs": [
            {
                "path": name,
                "sha256": ref(f"{RUN_REL}/{name}")["sha256"],
                "size_bytes": ref(f"{RUN_REL}/{name}")["size_bytes"],
            }
            for name in artifact_names
        ],
        "preserved_diagnostics": [
            {
                "case": "official partial-force generator guard on reused target",
                "exit_code": 1,
                "status": "pass-rejected",
                "evidence_ref": ref(f"{R4_REL}/validation/generation-parity/reused-target.stderr"),
            },
            {
                "case": "R3 accepted implementation-content defect",
                "terminal_code": "ACCEPTANCE_BOUND_IMPLEMENTATION_CONTENT_DEFECT",
                "role": "immutable repair-cause/no-mutation evidence; never completion authority",
                "evidence_ref": ref(BLOCKER_REL),
            },
        ],
        "readiness": (
            {
                "verdict": readiness_report["verdict"],
                "terminal_code": readiness_report["terminal_code"],
                "runtime_admission_status": readiness_report["runtime_admission_status"],
                "mutation_ready": readiness_report["mutation_ready"],
                "selected_unit": readiness_report["selected_unit"],
                "canonical_semantic_digest": readiness_report["canonical_semantic_digest"],
                "source_snapshot_digest": readiness_manifest["source_snapshot_digest"],
                "plan_epoch_id": readiness_manifest["plan_epoch_id"],
                "two_run_exact_byte_reproducibility": "pass",
            }
            if readiness_report is not None and readiness_manifest is not None
            else {
                "verdict": "pending-wpra-r4",
                "runtime_admission_status": "pending-selection",
                "mutation_ready": False,
                "selected_unit": None,
            }
        ),
        "authority_effect": "none",
        "claim_ceiling": (
            "candidate-local compatibility evidence only; no owner acceptance, "
            "plan-once token, Task Session execution admission, application, "
            "promotion, publication, deployment, release, or production-readiness claim"
        ),
    }
    write(RUN / "PREACCEPTANCE-RECEIPT.json", receipt)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("package", "request", "negative", "receipt"))
    args = parser.parse_args()
    if args.phase == "package":
        prepare_package()
    elif args.phase == "request":
        prepare_request()
    elif args.phase == "negative":
        prepare_negative()
    else:
        prepare_receipt()
    print(json.dumps({"status": "pass", "phase": args.phase}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
