#!/usr/bin/env python3
"""Build the exact Invoke material package for SWU-BWAA-001."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[7]
REFRESH = Path(__file__).resolve().parent
MATERIAL = REFRESH / "material"

TARGETS = [
    "projects/body-war/ontology/business/scripts/view-atlas-projection.mjs",
    "projects/body-war/ontology/business/scripts/validate-view-atlas.mjs",
    "projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs",
]

SOURCES = [
    "projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/work-pack/tasks/TASK-BWAA-001.md",
    "projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/WORK-PACK.md",
    "projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/refreshes/20260730T090724Z-swu-bwaa-001-material-admission/CONTEXT-PACK.json",
]

DEPENDENCIES: dict[str, str] = {}

VALIDATION_COMMANDS = [
    "node --test projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs",
    "node projects/body-war/ontology/business/scripts/validate-view-atlas.mjs",
    "git diff --check -- projects/body-war/ontology/business/scripts/view-atlas-projection.mjs projects/body-war/ontology/business/scripts/validate-view-atlas.mjs projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs",
]


def exact_ref(relative: str) -> dict[str, object]:
    data = (REPOSITORY / relative).read_bytes()
    return {
        "path": relative,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }


def staged_ref(target: str) -> dict[str, object]:
    relative = (
        "projects/body-war/development/invoke-runs/"
        "20260730T062453Z-business-ontology-atlas-arrows/refreshes/"
        "20260730T090724Z-swu-bwaa-001-material-admission/material/staged/"
        f"{target}"
    )
    return exact_ref(relative)


def main() -> None:
    inventory = json.loads((REFRESH / "TARGET-INVENTORY.json").read_text())
    inventory_targets = [entry["path"] for entry in inventory["targets"]]
    if inventory_targets != TARGETS:
        raise SystemExit("target inventory order or scope drift")
    for entry in inventory["targets"]:
        live_ref = exact_ref(entry["path"])
        if (
            live_ref["sha256"] != entry["preimage_sha256"]
            or live_ref["size_bytes"] != entry["preimage_size_bytes"]
        ):
            raise SystemExit(f"live preimage drift: {entry['path']}")
        output_ref = staged_ref(entry["path"])
        if (
            output_ref["sha256"] != entry["staged_sha256"]
            or output_ref["size_bytes"] != entry["staged_size_bytes"]
        ):
            raise SystemExit(f"staged output drift: {entry['path']}")

    dependency_ids = list(DEPENDENCIES)
    package = {
        "schema_version": "1.0.0",
        "package_id": "body-war-bwaa-swu-001-material-admission-20260730T090724Z",
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": "body-war.product-ontology-owner",
        "authority_class": "private",
        "publication_class": "internal",
        "source_artifacts": [
            {**exact_ref(source), "authority_class": "private"}
            for source in SOURCES
        ],
        "changes": [
            {
                "target_path": target,
                "operation": "update",
                "output_ref": staged_ref(target),
            }
            for target in TARGETS
        ],
        "target_inventory": [
            {
                "target_path": target,
                "lifecycle_owner": "body-war.product-ontology-owner",
                "authority_class": "private",
                "publication_class": "internal",
                "dependency_ids": dependency_ids,
            }
            for target in TARGETS
        ],
        "dependencies": [
            {
                "dependency_id": dependency_id,
                "artifact_ref": exact_ref(source),
            }
            for dependency_id, source in DEPENDENCIES.items()
        ],
        "mirror_groups": [],
        "approval": {
            "class": "explicit-apply",
            "owner": "body-war.product-ontology-owner",
            "scope_paths": TARGETS,
            "authority_classes": ["private"],
            "publication_classes": ["internal"],
        },
        "validation_commands": VALIDATION_COMMANDS,
    }
    MATERIAL.mkdir(parents=True, exist_ok=True)
    (MATERIAL / "MATERIAL-PACKAGE.json").write_text(
        json.dumps(package, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
