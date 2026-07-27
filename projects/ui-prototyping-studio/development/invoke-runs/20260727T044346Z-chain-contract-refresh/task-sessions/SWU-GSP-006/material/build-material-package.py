#!/usr/bin/env python3
"""Build the exact implementation material package for SWU-GSP-006."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[8]
SESSION_ROOT = Path(__file__).resolve().parent.parent
STAGED_PREFIX = SESSION_ROOT.relative_to(REPO_ROOT) / "material" / "staged"
OUTPUT = Path(__file__).resolve().parent / "MATERIAL-PACKAGE.json"
PLAN_RUN = (
    "projects/ui-prototyping-studio/development/invoke-runs/"
    "20260727T042935Z-architecture-review-refresh"
)
CHAIN_RUN = (
    "projects/ui-prototyping-studio/development/invoke-runs/"
    "20260727T044346Z-chain-contract-refresh"
)
SESSION_RUN = f"{CHAIN_RUN}/task-sessions/SWU-GSP-006"
MODULE = (
    "projects/ui-prototyping-studio/backend/src/modules/"
    "ui-prototyping-studio"
)
LIFECYCLE_OWNER = (
    "private UI Prototyping Studio implementation via task-session"
)
CONTROL_ARTIFACTS = [
    f"{PLAN_RUN}/work-pack/tasks/TASK-GSP-006-handoff-readiness.md",
    f"{PLAN_RUN}/WORK-PACK.md",
    f"{SESSION_RUN}/context-pack.json",
    f"{MODULE}/domain/models.ts",
    f"{MODULE}/application/export-design-handoff.ts",
    f"{MODULE}/application/session-store.ts",
    f"{MODULE}/infrastructure/file-studio-session-store.ts",
    f"{MODULE}/interface/http-routes.ts",
]
DEPENDENCIES = {
    "chain-preflight": f"{CHAIN_RUN}/CHAIN-STATE.json",
    "gsp-005-closeout": (
        f"{CHAIN_RUN}/closeout/SWU-GSP-005/OWNER-RECEIPT.json"
    ),
}
UPDATE_TARGETS = [
    f"{MODULE}/domain/models.ts",
    f"{MODULE}/application/export-design-handoff.ts",
    f"{MODULE}/application/ui-prototyping-studio.slice.test.ts",
    f"{MODULE}/application/session-store.ts",
    f"{MODULE}/infrastructure/file-studio-session-store.ts",
    f"{MODULE}/interface/http-routes.ts",
]
VALIDATION_COMMANDS = [
    (
        "cd projects/ui-prototyping-studio/backend && "
        "./node_modules/.bin/tsc -p tsconfig.json --noEmit"
    ),
    (
        "cd projects/ui-prototyping-studio/backend && "
        "./node_modules/.bin/tsx --test \"src/**/*.test.ts\""
    ),
]


def exact_ref(path: str) -> dict[str, object]:
    content = (REPO_ROOT / path).read_bytes()
    return {
        "path": path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def main() -> None:
    staged_paths = {
        target: (STAGED_PREFIX / target).as_posix()
        for target in UPDATE_TARGETS
    }
    dependency_ids = list(DEPENDENCIES)
    document = {
        "schema_version": "1.0.0",
        "package_id": "ups-gsp-006-handoff-readiness-20260727",
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": LIFECYCLE_OWNER,
        "authority_class": "private",
        "publication_class": "private",
        "source_artifacts": [
            {**exact_ref(path), "authority_class": "private"}
            for path in CONTROL_ARTIFACTS
        ],
        "changes": [
            {
                "target_path": target,
                "operation": "update",
                "output_ref": exact_ref(staged_paths[target]),
            }
            for target in UPDATE_TARGETS
        ],
        "target_inventory": [
            {
                "target_path": target,
                "lifecycle_owner": LIFECYCLE_OWNER,
                "authority_class": "private",
                "publication_class": "private",
                "dependency_ids": dependency_ids,
            }
            for target in UPDATE_TARGETS
        ],
        "dependencies": [
            {
                "dependency_id": dependency_id,
                "artifact_ref": exact_ref(path),
            }
            for dependency_id, path in DEPENDENCIES.items()
        ],
        "mirror_groups": [],
        "approval": {
            "class": "explicit-apply",
            "owner": LIFECYCLE_OWNER,
            "scope_paths": UPDATE_TARGETS,
            "authority_classes": ["private"],
            "publication_classes": ["private"],
        },
        "validation_commands": VALIDATION_COMMANDS,
    }
    OUTPUT.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
