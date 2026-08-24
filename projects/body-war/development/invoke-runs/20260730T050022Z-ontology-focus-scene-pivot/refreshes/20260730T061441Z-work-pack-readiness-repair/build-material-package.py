#!/usr/bin/env python3
"""Bind staged readiness repairs into one exact Invoke material package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[7]
REFRESH = Path(__file__).resolve().parent
RUN_ROOT = Path(
    "projects/body-war/development/invoke-runs/"
    "20260730T050022Z-ontology-focus-scene-pivot"
)
OWNER = "private Body War OFSP planning owner via invoke:refresh"


def exact_ref(path: Path) -> dict[str, Any]:
    content = (ROOT / path).read_bytes()
    return {
        "path": path.as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def main() -> int:
    refresh_rel = REFRESH.relative_to(ROOT)
    inventory = json.loads(
        (REFRESH / "STAGED-TARGET-INVENTORY.json").read_text(encoding="utf-8")
    )
    targets = [Path(item["target_path"]) for item in inventory]
    sources = [
        RUN_ROOT / "readiness-runs/pre-refresh-r2/work-pack-readiness-report.json",
        RUN_ROOT / "readiness-runs/pre-refresh-r2/REFRESH-SIGNAL-PACK.json",
        RUN_ROOT / "IMPLEMENTATION-READINESS-DRY-RUN.md",
        refresh_rel / "CONTEXT-PACK.md",
        refresh_rel / "INVENTORY-LOOKUP.json",
        refresh_rel / "DISPATCH-TRACE.md",
        refresh_rel / "REFRESH-PATCH-PROPOSAL.md",
        refresh_rel / "STAGED-VALIDATION.md",
        refresh_rel / "build-refresh-material.py",
        refresh_rel / "STAGED-TARGET-INVENTORY.json",
    ]
    for target in targets:
        if (ROOT / target).is_file():
            sources.append(target)

    dependencies = [
        {
            "dependency_id": "readiness-audit-report",
            "artifact_ref": exact_ref(
                RUN_ROOT
                / "readiness-runs/pre-refresh-r2/work-pack-readiness-report.json"
            ),
        },
        {
            "dependency_id": "readiness-refresh-signals",
            "artifact_ref": exact_ref(
                RUN_ROOT
                / "readiness-runs/pre-refresh-r2/REFRESH-SIGNAL-PACK.json"
            ),
        },
        {
            "dependency_id": "strict-refresh-context",
            "artifact_ref": exact_ref(refresh_rel / "CONTEXT-PACK.md"),
        },
        {
            "dependency_id": "staged-validation",
            "artifact_ref": exact_ref(refresh_rel / "STAGED-VALIDATION.md"),
        },
    ]
    dependency_ids = [item["dependency_id"] for item in dependencies]
    changes = []
    target_inventory = []
    for item in inventory:
        target = Path(item["target_path"])
        staged = refresh_rel / "material/staged" / target
        changes.append(
            {
                "target_path": target.as_posix(),
                "operation": item["operation"],
                "output_ref": exact_ref(staged),
            }
        )
        target_inventory.append(
            {
                "target_path": target.as_posix(),
                "lifecycle_owner": OWNER,
                "authority_class": "private",
                "publication_class": "private",
                "dependency_ids": dependency_ids,
            }
        )

    package = {
        "schema_version": "1.0.0",
        "package_id": "body-war-ofsp-work-pack-readiness-repair-20260730T061441Z",
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": OWNER,
        "authority_class": "private",
        "publication_class": "private",
        "source_artifacts": [
            {**exact_ref(path), "authority_class": "private"} for path in sources
        ],
        "changes": changes,
        "target_inventory": target_inventory,
        "dependencies": dependencies,
        "mirror_groups": [],
        "approval": {
            "class": "explicit-apply",
            "owner": OWNER,
            "scope_paths": [path.as_posix() for path in targets],
            "authority_classes": ["private"],
            "publication_classes": ["private"],
        },
        "validation_commands": [
            "python3 -m json.tool <staged>/TASK-SESSION-RECEIPT.schema.json",
            "python3 -m json.tool <staged>/work-pack/shared/COMMAND-MATRIX.json",
            "python3 <staged>/work-pack/shared/test-task-session-receipt.py",
            (
                "python3 arcanum/spells/work-pack-readiness-audit/scripts/"
                "audit_work_pack.py --config <post-refresh-config> "
                "--output-dir <post-refresh-run>"
            ),
            (
                "git diff --check -- projects/body-war/development/invoke-runs/"
                "20260730T050022Z-ontology-focus-scene-pivot"
            ),
        ],
    }
    (REFRESH / "MATERIAL-PACKAGE.json").write_text(
        json.dumps(package, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "package_id": package["package_id"],
                "targets": len(targets),
                "sources": len(sources),
                "dependencies": len(dependencies),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
