#!/usr/bin/env python3
"""Build the exact Invoke and Task Session admission inputs for SWU-AKV-NV-001."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[7]
ATTEMPT = Path(__file__).resolve().parent
PLAN = REPOSITORY / "projects/animejs/development/implementation/agent-knowledge-vault"
STAGED_ROOT = ATTEMPT / "producer/staged"
TARGET_ROOT = "projects/animejs/ontology/agent-knowledge-vault"
ATTEMPT_ID = "attempt-akv-nv-001-20260804t020214z"
TASK_ID = "TASK-AKV-CONTRACTS"
SWU_ID = "SWU-AKV-NV-001"


def canonical_digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()


def exact(path: Path, *, camel: bool = True) -> dict[str, object]:
    data = path.read_bytes()
    result: dict[str, object] = {
        "path": path.relative_to(REPOSITORY).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    result["sizeBytes" if camel else "size_bytes"] = len(data)
    return result


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


work_pack = json.loads((PLAN / "WORK-PACK.json").read_text())
unit = next(item for item in work_pack["execution_units"] if item["swu_id"] == SWU_ID)
selection_path = PLAN / "readiness/selection-receipt.json"
selection = json.loads(selection_path.read_text())
manifest_path = PLAN / "readiness/audit-output-pass/plan-semantic-manifest.json"
manifest = json.loads(manifest_path.read_text())
task_path = PLAN / unit["task_contract"]

material_writes = unit["material_writes"]
validation_contracts = unit["validation_contracts"]
validation_commands = [" ".join(item["argv"]) for item in validation_contracts]
target_baselines = []
for target in material_writes:
    path = REPOSITORY / target
    if path.exists():
        data = path.read_bytes()
        target_baselines.append({
            "path": target,
            "state": "present",
            "sha256": hashlib.sha256(data).hexdigest(),
            "sizeBytes": len(data),
        })
    else:
        target_baselines.append({
            "path": target,
            "state": "absent",
            "sha256": None,
            "sizeBytes": None,
        })

context = {
    "schema_version": "animejs.agent-knowledge-vault.task-session-context.v1",
    "task_id": TASK_ID,
    "swu_id": SWU_ID,
    "strict_coverage": True,
    "plan_epoch_id": selection["planEpochId"],
    "unit_contract_digest": selection["unitContractDigest"],
    "source_anchors": [
        "projects/animejs/development/refinement-runs/20260803T175423Z-animejs-blocking-defects/stages/08-query-contract-matrix.json",
        "projects/animejs/development/research/2026-08-03-animejs-agent-knowledge-vault/receipts/knowledge-vault-synthesis-reviewer-repair.json",
    ],
    "execution_contract": {
        "writeProfile": "material-bound",
        "materialWrites": material_writes,
        "executionOutputs": [],
        "allowedWrites": material_writes,
        "validationCommands": validation_commands,
        "lifecycleOwner": "ontology-vault",
        "authorityClass": "private",
        "publicationClass": "internal",
    },
    "claim_ceiling": "candidate-local; authority_effect none; no release admission",
}
context_path = ATTEMPT / "CONTEXT-PACK.json"
write_json(context_path, context)

controls = [
    {**exact(task_path), "role": "task-contract", "authorityClass": "private"},
    {**exact(PLAN / "WORK-PACK.json"), "role": "work-pack", "authorityClass": "private"},
    {**exact(context_path), "role": "context-pack", "authorityClass": "private"},
]
plan_binding = {
    "task_id": TASK_ID,
    "swu_id": SWU_ID,
    "plan_epoch_id": selection["planEpochId"],
    "unit_contract_digest": selection["unitContractDigest"],
    "selection_receipt_digest": exact(selection_path)["sha256"],
    "attempt_id": ATTEMPT_ID,
    "validation_contract_digest": canonical_digest(validation_contracts),
    "validation_contracts": validation_contracts,
    "target_baselines": [
        {
            "path": item["path"],
            "state": item["state"],
            "sha256": item["sha256"],
            "size_bytes": item["sizeBytes"],
        }
        for item in target_baselines
    ],
}

package = {
    "schema_version": "1.0.0",
    "package_id": "invoke-animejs-akv-nv-001-20260804t020214z",
    "mutation_mode": "apply-approved",
    "mutation_state": "materialized",
    "lifecycle_owner": "ontology-vault",
    "authority_class": "private",
    "publication_class": "internal",
    "source_artifacts": [
        {
            "path": item["path"],
            "sha256": item["sha256"],
            "size_bytes": item["sizeBytes"],
            "authority_class": item["authorityClass"],
        }
        for item in controls
    ],
    "changes": [
        {
            "target_path": target,
            "operation": "update" if baseline["state"] == "present" else "create",
            "output_ref": exact(STAGED_ROOT / target, camel=False),
        }
        for target, baseline in zip(material_writes, target_baselines, strict=True)
    ],
    "target_inventory": [
        {
            "target_path": target,
            "lifecycle_owner": "ontology-vault",
            "authority_class": "private",
            "publication_class": "internal",
            "dependency_ids": [],
        }
        for target in material_writes
    ],
    "dependencies": [],
    "mirror_groups": [],
    "approval": {
        "class": "explicit-apply",
        "owner": "ontology-vault",
        "scope_paths": material_writes,
        "authority_classes": ["private"],
        "publication_classes": ["internal"],
    },
    "validation_commands": validation_commands,
    "plan_binding": plan_binding,
}
package_path = ATTEMPT / "producer/material-package.json"
write_json(package_path, package)
material_receipt_path = ATTEMPT / "producer/material-package-receipt.json"
material_receipt_ref = (
    exact(material_receipt_path)
    if material_receipt_path.is_file()
    else {
        "path": material_receipt_path.relative_to(REPOSITORY).as_posix(),
        "sha256": "0" * 64,
        "sizeBytes": 0,
    }
)

request = {
    "schemaVersion": "1.2.0",
    "admissionProfile": "plan-once-selected-unit",
    "executionMode": "reusable-mutation",
    "taskId": TASK_ID,
    "swuId": SWU_ID,
    "controlArtifacts": controls,
    "dependencyFrontier": [],
    "materialPackage": exact(package_path),
    "materialReceipt": material_receipt_ref,
    "producerReceiptSchema": exact(REPOSITORY / "arcanum/spells/invoke/schemas/material-package-receipt.schema.json"),
    "materialWrites": material_writes,
    "executionOutputs": [],
    "allowedWrites": material_writes,
    "validationCommands": validation_commands,
    "lifecycleOwner": "ontology-vault",
    "authorityClass": "private",
    "publicationClass": "internal",
    "planAdmission": {
        "planManifest": exact(manifest_path),
        "planManifestSchema": exact(REPOSITORY / "arcanum/spells/work-pack-readiness-audit/schemas/plan-semantic-manifest.schema.json"),
        "selectionReceipt": exact(selection_path),
        "selectionReceiptSchema": exact(REPOSITORY / "arcanum/spells/work-pack-readiness-audit/schemas/selection-receipt.schema.json"),
        "planEpochId": manifest["plan_epoch_id"],
        "unitContractDigest": selection["unitContractDigest"],
        "attemptId": ATTEMPT_ID,
        "targetBaselines": target_baselines,
        "structuredValidationContracts": validation_contracts,
        "validationContractDigest": canonical_digest(validation_contracts),
    },
}
write_json(ATTEMPT / "MUTATION-ADMISSION-REQUEST.template.json", request)
print(f"built {package_path.relative_to(REPOSITORY)}")
