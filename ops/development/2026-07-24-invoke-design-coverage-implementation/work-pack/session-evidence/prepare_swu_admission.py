#!/usr/bin/env python3
"""Prepare exact Invoke material and Task Session admission receipts for one SWU.

This private session helper performs evidence assembly only. It never writes a
declared target, changes a work-pack status, or runs implementation validation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[5]
PACKAGE = ROOT / "ops/development/2026-07-24-invoke-design-coverage-implementation"
EVIDENCE = PACKAGE / "work-pack/session-evidence"
WORK_PACK = PACKAGE / "WORK-PACK.md"
SHARED_CONTEXT = PACKAGE / "work-pack/shared/CONTEXT.md"
INVOKE = ROOT / "arcanum/spells/invoke"
TASK_SESSION = ROOT / "arcanum/arcana/task-session"


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def exact(path: Path, snake: bool = False) -> dict[str, Any]:
    content = path.read_bytes()
    result = {
        "path": str(path.relative_to(ROOT)),
        "sha256": hashlib.sha256(content).hexdigest(),
    }
    result["size_bytes" if snake else "sizeBytes"] = len(content)
    return result


def parse_pair(raw: str) -> tuple[str, str]:
    key, sep, value = raw.partition("=")
    if not sep or not key or not value:
        raise ValueError(f"expected KEY=VALUE, got {raw!r}")
    return key, value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--swu-id", required=True)
    parser.add_argument("--task-file", required=True)
    parser.add_argument("--change", action="append", default=[], help="TARGET=STAGED")
    parser.add_argument("--dependency", action="append", default=[], help="ID=RECEIPT")
    parser.add_argument("--validation", action="append", default=[])
    parser.add_argument("--authority", choices=("public", "private"), default="public")
    parser.add_argument(
        "--publication", choices=("public", "private", "internal"), default="public"
    )
    parser.add_argument("--owner", default="spellcraft")
    args = parser.parse_args()

    if not args.change or not args.validation:
        raise SystemExit("at least one --change and --validation are required")

    evidence_dir = EVIDENCE / args.swu_id
    task_file = ROOT / args.task_file
    changes = [parse_pair(item) for item in args.change]
    dependencies = [parse_pair(item) for item in args.dependency]

    context = {
        "schema_version": "task-session-context-pack.v1",
        "task_id": args.task_id,
        "swu_id": args.swu_id,
        "strict_coverage": True,
        "work_pack": str(WORK_PACK.relative_to(ROOT)),
        "task_contract": str(task_file.relative_to(ROOT)),
        "sources": [
            str(WORK_PACK.relative_to(ROOT)),
            str(task_file.relative_to(ROOT)),
            str(SHARED_CONTEXT.relative_to(ROOT)),
        ],
        "dependency_frontier": [item[0] for item in dependencies],
        "write_scope": sorted(item[0] for item in changes),
        "validation": sorted(set(args.validation)),
        "constraints": [
            "apply only exact staged bytes after admissionVerdict=admit",
            "preserve unrelated dirty changes",
            "do not infer promotion, publication, commit, or push authority",
        ],
    }
    context_path = evidence_dir / "context-pack.json"
    dump(context_path, context)
    (evidence_dir / "CONTEXT-PACK.md").write_text(
        f"# Context Pack: {args.swu_id}\n\n"
        f"Strict coverage binds `{args.task_id}` to {len(changes)} exact target(s), "
        f"{len(dependencies)} dependency receipt(s), and {len(args.validation)} "
        "validation command(s). Canonical mutation remains gated by the material "
        "and mutation-admission receipts in this directory.\n",
        encoding="utf-8",
    )

    controls = [
        (task_file, "task-contract"),
        (WORK_PACK, "work-pack"),
        (context_path, "context-pack"),
    ]
    source_artifacts = []
    control_artifacts = []
    for path, role in controls:
        source = exact(path, snake=True)
        source["authority_class"] = args.authority
        source_artifacts.append(source)
        control = exact(path)
        control["role"] = role
        control["authorityClass"] = args.authority
        control_artifacts.append(control)

    package_dependencies = []
    request_dependencies = []
    for dependency_id, raw_path in dependencies:
        dependency_path = ROOT / raw_path
        package_dependencies.append(
            {"dependency_id": dependency_id, "artifact_ref": exact(dependency_path, True)}
        )
        request_dependencies.append(
            {"dependencyId": dependency_id, "artifactRef": exact(dependency_path)}
        )

    package_changes = []
    inventory = []
    for target, staged in changes:
        target_path = ROOT / target
        staged_path = ROOT / staged
        if not staged_path.is_file():
            raise SystemExit(f"missing staged output: {staged}")
        package_changes.append(
            {
                "target_path": target,
                "operation": "update" if target_path.exists() else "create",
                "output_ref": exact(staged_path, True),
            }
        )
        inventory.append(
            {
                "target_path": target,
                "lifecycle_owner": args.owner,
                "authority_class": args.authority,
                "publication_class": args.publication,
                "dependency_ids": [item[0] for item in dependencies],
            }
        )

    package_doc = {
        "schema_version": "1.0.0",
        "package_id": f"invoke-design-coverage-{args.swu_id.lower()}",
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": args.owner,
        "authority_class": args.authority,
        "publication_class": args.publication,
        "source_artifacts": source_artifacts,
        "changes": package_changes,
        "target_inventory": inventory,
        "dependencies": package_dependencies,
        "mirror_groups": [],
        "approval": {
            "class": "explicit-apply",
            "owner": args.owner,
            "scope_paths": sorted(item[0] for item in changes),
            "authority_classes": [args.authority],
            "publication_classes": [args.publication],
        },
        "validation_commands": sorted(set(args.validation)),
    }
    package_path = evidence_dir / "material-package.json"
    dump(package_path, package_doc)

    producer = load_module(
        "invoke_material_package_validator",
        INVOKE / "scripts/material_package_validator.py",
    )
    material_receipt = producer.validate_material_package(
        package_doc,
        ROOT,
        producer.load_json(INVOKE / "schemas/material-package.schema.json"),
        producer.load_json(INVOKE / "schemas/material-package-receipt.schema.json"),
    )
    material_receipt_path = evidence_dir / "material-receipt.json"
    dump(material_receipt_path, material_receipt)
    if material_receipt["patchVerdict"] != "pass":
        print(json.dumps(material_receipt, indent=2, sort_keys=True))
        return 1

    request = {
        "schemaVersion": "1.0.0",
        "executionMode": "reusable-mutation",
        "taskId": args.task_id,
        "swuId": args.swu_id,
        "controlArtifacts": control_artifacts,
        "dependencyFrontier": request_dependencies,
        "materialPackage": exact(package_path),
        "materialReceipt": exact(material_receipt_path),
        "producerReceiptSchema": exact(
            INVOKE / "schemas/material-package-receipt.schema.json"
        ),
        "allowedWrites": sorted(item[0] for item in changes),
        "validationCommands": sorted(set(args.validation)),
        "lifecycleOwner": args.owner,
        "authorityClass": args.authority,
        "publicationClass": args.publication,
    }
    request_path = evidence_dir / "mutation-admission-request.json"
    dump(request_path, request)

    consumer = load_module(
        "task_session_mutation_readiness",
        TASK_SESSION / "scripts/verify-mutation-readiness.py",
    )
    admission = consumer.resolve_mutation_admission(
        request,
        ROOT,
        consumer.load_json(
            TASK_SESSION / "schemas/mutation-admission-request.schema.json"
        ),
    )
    admission_path = evidence_dir / "mutation-admission-receipt.json"
    dump(admission_path, admission)
    print(
        json.dumps(
            {
                "swu_id": args.swu_id,
                "material": material_receipt["patchVerdict"],
                "admission": admission["admissionVerdict"],
                "mutation_ready": admission["mutationReady"],
                "reasons": admission["reasons"],
            },
            sort_keys=True,
        )
    )
    return 0 if admission["mutationReady"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
