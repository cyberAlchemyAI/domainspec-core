#!/usr/bin/env python3
"""Select and admit one already-staged Anime.js ontology SWU under the frozen plan."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()


def exact(root: Path, path: Path, *, camel: bool = False) -> dict[str, object]:
    data = path.read_bytes()
    result: dict[str, object] = {
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }
    result["sizeBytes" if camel else "size_bytes"] = len(data)
    return result


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def run(argv: list[str], root: Path) -> None:
    completed = subprocess.run(argv, cwd=root, check=False, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="")
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--attempt-dir", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--swu", required=True)
    parser.add_argument("--dependency", action="append", default=[], help="UNIT_ID=receipt/path.json")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    attempt = (root / args.attempt_dir).resolve()
    plan = root / "projects/animejs/development/implementation/agent-knowledge-vault"
    work_pack_path = plan / "WORK-PACK.json"
    work_pack = load(work_pack_path)
    unit = next(item for item in work_pack["execution_units"] if item["swu_id"] == args.swu)
    task_id = unit["task_id"]
    manifest_candidates = [
        plan / "readiness/audit-output-refresh-3/plan-semantic-manifest.json",
        plan / "readiness/audit-output-refresh-2/plan-semantic-manifest.json",
        plan / "readiness/audit-output-refresh-1/plan-semantic-manifest.json",
        plan / "readiness/audit-output-pass/plan-semantic-manifest.json",
    ]
    manifest_path = next(path for path in manifest_candidates if path.is_file())
    manifest = load(manifest_path)
    dependency_paths: dict[str, Path] = {}
    for raw in args.dependency:
        dependency_id, separator, raw_path = raw.partition("=")
        if not separator:
            raise ValueError(f"invalid dependency: {raw}")
        dependency_paths[dependency_id] = (root / raw_path).resolve()
    if set(dependency_paths) != set(unit["dependencies"]):
        raise ValueError(f"dependency frontier mismatch: expected {unit['dependencies']}, got {sorted(dependency_paths)}")

    selection_request = {
        "schemaVersion": "1.0.0",
        "manifestRef": exact(root, manifest_path),
        "auditConfigPath": (plan / "readiness/audit-config.json").relative_to(root).as_posix(),
        "taskId": task_id,
        "swuId": args.swu,
        "explicitConfirmation": {
            "confirmed": True,
            "confirmedBy": "direct-user",
            "confirmationId": "2026-08-03-finish-animejs-ontology",
        },
        "dependencyReceipts": [
            {"dependencyId": dependency_id, "artifactRef": exact(root, path)}
            for dependency_id, path in sorted(dependency_paths.items())
        ],
        "lifecycleEligibility": {
            "eligible": True,
            "state": "selected-by-task-session-until-blocker",
            "evidenceRefs": [exact(root, plan / "readiness/evidence.json")],
        },
    }
    selection_request_path = attempt / "SELECTION-REQUEST.json"
    selection_receipt_path = attempt / "SELECTION-RECEIPT.json"
    write(selection_request_path, selection_request)
    run([
        "python3", "arcanum/spells/work-pack-readiness-audit/scripts/verify_plan_selection.py",
        selection_request_path.relative_to(root).as_posix(),
        "--repository-root", ".",
        "--request-schema", "arcanum/spells/work-pack-readiness-audit/schemas/selection-request.schema.json",
        "--receipt-schema", "arcanum/spells/work-pack-readiness-audit/schemas/selection-receipt.schema.json",
        "--manifest-schema", "arcanum/spells/work-pack-readiness-audit/schemas/plan-semantic-manifest.schema.json",
        "--config-schema", "arcanum/spells/work-pack-readiness-audit/schemas/audit-config-v2.schema.json",
        "--output", selection_receipt_path.relative_to(root).as_posix(),
    ], root)
    selection = load(selection_receipt_path)
    if selection.get("selectionVerdict") != "select":
        raise ValueError(f"selection blocked: {selection.get('reasons')}")

    material_writes = unit["material_writes"]
    validation_contracts = unit["validation_contracts"]
    validation_commands = [" ".join(item["argv"]) for item in validation_contracts]
    target_baselines = []
    for raw in material_writes:
        target = root / raw
        if target.is_file():
            data = target.read_bytes()
            target_baselines.append({"path": raw, "state": "present", "sha256": hashlib.sha256(data).hexdigest(), "sizeBytes": len(data)})
        elif target.exists():
            raise ValueError(f"material target is not a file: {raw}")
        else:
            target_baselines.append({"path": raw, "state": "absent", "sha256": None, "sizeBytes": None})

    context = {
        "schema_version": "animejs.agent-knowledge-vault.task-session-context.v1",
        "task_id": task_id,
        "swu_id": args.swu,
        "strict_coverage": True,
        "plan_epoch_id": selection["planEpochId"],
        "unit_contract_digest": selection["unitContractDigest"],
        "dependency_receipts": [exact(root, path) for _, path in sorted(dependency_paths.items())],
        "execution_contract": {
            "writeProfile": "material-bound",
            "materialWrites": material_writes,
            "executionOutputs": unit["execution_outputs"],
            "allowedWrites": material_writes + unit["execution_outputs"],
            "validationCommands": validation_commands,
            "lifecycleOwner": "ontology-vault",
            "authorityClass": "private",
            "publicationClass": "internal",
        },
        "claim_ceiling": "candidate-local; authority_effect none; no release admission",
    }
    context_path = attempt / "CONTEXT-PACK.json"
    write(context_path, context)
    task_path = plan / unit["task_contract"]
    controls = [
        {**exact(root, task_path, camel=True), "role": "task-contract", "authorityClass": "private"},
        {**exact(root, work_pack_path, camel=True), "role": "work-pack", "authorityClass": "private"},
        {**exact(root, context_path, camel=True), "role": "context-pack", "authorityClass": "private"},
    ]
    package_dependencies = [
        {"dependency_id": dependency_id, "artifact_ref": exact(root, path)}
        for dependency_id, path in sorted(dependency_paths.items())
    ]
    plan_binding = {
        "task_id": task_id,
        "swu_id": args.swu,
        "plan_epoch_id": selection["planEpochId"],
        "unit_contract_digest": selection["unitContractDigest"],
        "selection_receipt_digest": exact(root, selection_receipt_path)["sha256"],
        "attempt_id": args.attempt_id,
        "validation_contract_digest": digest(validation_contracts),
        "validation_contracts": validation_contracts,
        "target_baselines": [
            {"path": item["path"], "state": item["state"], "sha256": item["sha256"], "size_bytes": item["sizeBytes"]}
            for item in target_baselines
        ],
    }
    staged_root = attempt / "producer/staged"
    package = {
        "schema_version": "1.0.0",
        "package_id": f"invoke-{args.swu.lower()}-{args.attempt_id}",
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": "ontology-vault",
        "authority_class": "private",
        "publication_class": "internal",
        "source_artifacts": [
            {"path": item["path"], "sha256": item["sha256"], "size_bytes": item["sizeBytes"], "authority_class": item["authorityClass"]}
            for item in controls
        ],
        "changes": [
            {
                "target_path": target,
                "operation": "update" if baseline["state"] == "present" else "create",
                "output_ref": exact(root, staged_root / target),
            }
            for target, baseline in zip(material_writes, target_baselines, strict=True)
        ],
        "target_inventory": [
            {"target_path": target, "lifecycle_owner": "ontology-vault", "authority_class": "private", "publication_class": "internal", "dependency_ids": sorted(dependency_paths)}
            for target in material_writes
        ],
        "dependencies": package_dependencies,
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
    package_path = attempt / "producer/material-package.json"
    producer_receipt_path = attempt / "producer/material-package-receipt.json"
    write(package_path, package)
    run([
        "python3", "arcanum/spells/invoke/scripts/material_package_validator.py",
        package_path.relative_to(root).as_posix(), "--root", ".", "--schema-dir", "arcanum/spells/invoke/schemas",
        "--output", producer_receipt_path.relative_to(root).as_posix(),
    ], root)

    dependencies = [
        {"dependencyId": dependency_id, "artifactRef": exact(root, path, camel=True)}
        for dependency_id, path in sorted(dependency_paths.items())
    ]
    request = {
        "schemaVersion": "1.2.0",
        "admissionProfile": "plan-once-selected-unit",
        "executionMode": "reusable-mutation",
        "taskId": task_id,
        "swuId": args.swu,
        "controlArtifacts": controls,
        "dependencyFrontier": dependencies,
        "materialPackage": exact(root, package_path, camel=True),
        "materialReceipt": exact(root, producer_receipt_path, camel=True),
        "producerReceiptSchema": exact(root, root / "arcanum/spells/invoke/schemas/material-package-receipt.schema.json", camel=True),
        "materialWrites": material_writes,
        "executionOutputs": unit["execution_outputs"],
        "allowedWrites": material_writes + unit["execution_outputs"],
        "validationCommands": validation_commands,
        "lifecycleOwner": "ontology-vault",
        "authorityClass": "private",
        "publicationClass": "internal",
        "planAdmission": {
            "planManifest": exact(root, manifest_path, camel=True),
            "planManifestSchema": exact(root, root / "arcanum/spells/work-pack-readiness-audit/schemas/plan-semantic-manifest.schema.json", camel=True),
            "selectionReceipt": exact(root, selection_receipt_path, camel=True),
            "selectionReceiptSchema": exact(root, root / "arcanum/spells/work-pack-readiness-audit/schemas/selection-receipt.schema.json", camel=True),
            "planEpochId": selection["planEpochId"],
            "unitContractDigest": selection["unitContractDigest"],
            "attemptId": args.attempt_id,
            "targetBaselines": target_baselines,
            "structuredValidationContracts": validation_contracts,
            "validationContractDigest": digest(validation_contracts),
        },
    }
    request_path = attempt / "MUTATION-ADMISSION-REQUEST.template.json"
    admission_path = attempt / "MUTATION-ADMISSION-RECEIPT.json"
    write(request_path, request)
    run([
        "python3", "arcanum/arcana/task-session/scripts/verify-mutation-readiness.py",
        request_path.relative_to(root).as_posix(), "--repository-root", ".",
        "--request-schema", "arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json",
        "--receipt-schema", "arcanum/arcana/task-session/schemas/mutation-admission-receipt.schema.json",
        "--output", admission_path.relative_to(root).as_posix(),
    ], root)
    admission = load(admission_path)
    print(json.dumps({
        "selection": selection["terminalCode"],
        "admission": admission["admissionVerdict"],
        "mutation_ready": admission["mutationReady"],
        "swu_id": args.swu,
        "plan_epoch_id": selection["planEpochId"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
