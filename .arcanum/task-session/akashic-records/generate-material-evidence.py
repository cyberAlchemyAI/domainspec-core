#!/usr/bin/env python3
"""Generate and validate parent-private Invoke Refresh material evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def exact_ref(root: Path, relative: str) -> dict[str, object]:
    raw = (root / relative).read_bytes()
    return {
        "path": relative,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
    }


def tracked_at_head(root: Path, relative: str) -> bool:
    return (
        subprocess.run(
            ["git", "cat-file", "-e", f"HEAD:{relative}"],
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent-root", required=True)
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--swu", required=True)
    parser.add_argument("--task-spec", required=True)
    parser.add_argument("--path", action="append", dest="paths", required=True)
    parser.add_argument(
        "--validation-command",
        action="append",
        dest="commands",
        required=True,
    )
    args = parser.parse_args()

    parent = Path(args.parent_root).resolve()
    target = Path(args.target_root).resolve()
    paths = sorted(set(args.paths), key=lambda value: value.encode("utf-8"))
    commands = sorted(set(args.commands), key=lambda value: value.encode("utf-8"))
    output = parent / ".arcanum/task-session/akashic-records" / args.swu
    output.mkdir(parents=True, exist_ok=True)

    work_pack = "development/phase-0-content-contract/plan/WORK-PACK.md"
    source_paths = [work_pack, args.task_spec]
    source_artifacts = [
        {**exact_ref(target, path), "authority_class": "public"}
        for path in source_paths
    ]
    changes = [
        {
            "target_path": path,
            "operation": "update" if tracked_at_head(target, path) else "create",
            "output_ref": exact_ref(target, path),
        }
        for path in paths
    ]
    target_inventory = [
        {
            "target_path": path,
            "lifecycle_owner": "task-session",
            "authority_class": "public",
            "publication_class": "public",
            "dependency_ids": ["work-pack"],
        }
        for path in paths
    ]
    package_id = f"akashic-{args.swu}-20260727"
    package = {
        "schema_version": "1.0.0",
        "package_id": package_id,
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": "task-session",
        "authority_class": "public",
        "publication_class": "public",
        "source_artifacts": source_artifacts,
        "changes": changes,
        "target_inventory": target_inventory,
        "dependencies": [
            {
                "dependency_id": "work-pack",
                "artifact_ref": exact_ref(target, work_pack),
            }
        ],
        "mirror_groups": [],
        "approval": {
            "class": "explicit-apply",
            "owner": "task-session",
            "scope_paths": paths,
            "authority_classes": ["public"],
            "publication_classes": ["public"],
        },
        "validation_commands": commands,
    }
    package_path = output / "material-package.json"
    package_path.write_text(
        json.dumps(package, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    schemas = parent / ".agents/skills/invoke/schemas"
    receipt_path = output / "material-receipt.json"
    subprocess.run(
        [
            "python3",
            str(
                parent
                / ".agents/skills/invoke/scripts/material_package_validator.py"
            ),
            str(package_path),
            "--root",
            str(target),
            "--schema-dir",
            str(schemas),
            "--output",
            str(receipt_path),
        ],
        check=True,
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    handoff_request = {
        "activationSource": "direct-user",
        "mutationMode": "apply-approved",
        "authoredPhaseStatus": "pass",
        "requestedHandoff": "ready",
        "expectedPackageId": package_id,
        "expectedPackageDigest": receipt["packageDigest"],
        "materialReceipt": receipt,
    }
    request_path = output / "refresh-handoff-request.json"
    request_path.write_text(
        json.dumps(handoff_request, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    result_path = output / "refresh-handoff-result.json"
    subprocess.run(
        [
            "python3",
            str(
                parent
                / ".agents/skills/invoke/scripts/refresh_material_handoff.py"
            ),
            str(request_path),
            "--receipt-schema",
            str(schemas / "material-package-receipt.schema.json"),
            "--output",
            str(result_path),
        ],
        check=True,
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    if not result["mutationReady"]:
        raise SystemExit("material handoff is not ready")

    print(
        json.dumps(
            {
                "swu": args.swu,
                "package_id": package_id,
                "package_digest": receipt["packageDigest"],
                "validated_paths": receipt["validatedPaths"],
                "mutation_ready": result["mutationReady"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
