#!/usr/bin/env python3
"""Build the exact implementation material package for SWU-GSP-004."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[8]
SESSION_ROOT = Path(__file__).resolve().parent.parent
STAGED_PREFIX = SESSION_ROOT.relative_to(REPO_ROOT) / "material" / "staged"
OUTPUT = Path(__file__).resolve().parent / "MATERIAL-PACKAGE.json"

PACKAGE_ID = "ups-gsp-004-visible-change-diff-20260727"
LIFECYCLE_OWNER = (
    "private UI Prototyping Studio implementation via task-session"
)
PLAN_RUN = (
    "projects/ui-prototyping-studio/development/invoke-runs/"
    "20260727T042935Z-architecture-review-refresh"
)
CHAIN_RUN = (
    "projects/ui-prototyping-studio/development/invoke-runs/"
    "20260727T044346Z-chain-contract-refresh"
)
SESSION_RUN = f"{CHAIN_RUN}/task-sessions/SWU-GSP-004"
APP = (
    "projects/ui-prototyping-studio/backend/src/modules/"
    "ui-prototyping-studio/application"
)
DOMAIN = (
    "projects/ui-prototyping-studio/backend/src/modules/"
    "ui-prototyping-studio/domain"
)
INFRA = (
    "projects/ui-prototyping-studio/backend/src/modules/"
    "ui-prototyping-studio/infrastructure"
)

CONTROL_ARTIFACTS = [
    f"{PLAN_RUN}/work-pack/tasks/TASK-GSP-004-visible-change-diff.md",
    f"{PLAN_RUN}/WORK-PACK.md",
    f"{SESSION_RUN}/context-pack.json",
    f"{APP}/admission.ts",
    f"{APP}/governed-state-projection.ts",
    f"{APP}/export-design-handoff.ts",
    f"{DOMAIN}/models.ts",
    f"{INFRA}/file-studio-session-store.ts",
    "projects/ui-prototyping-studio/backend/src/cli/studio.ts",
]
DEPENDENCIES = {
    "chain-preflight": f"{CHAIN_RUN}/CHAIN-STATE.json",
    "gsp-003-closeout": (
        f"{CHAIN_RUN}/closeout/SWU-GSP-003/OWNER-RECEIPT.json"
    ),
}
UPDATE_TARGETS = [
    f"{DOMAIN}/models.ts",
    f"{APP}/admission.ts",
    f"{APP}/admission.test.ts",
    f"{APP}/governed-state-projection.test.ts",
    f"{APP}/export-design-handoff.ts",
    f"{INFRA}/file-studio-session-store.ts",
    "projects/ui-prototyping-studio/backend/src/cli/studio.ts",
]
CREATE_TARGETS = [
    "projects/ui-prototyping-studio/backend/e2e/fixtures/style-only.html",
    "projects/ui-prototyping-studio/backend/e2e/visible-change-diff.spec.ts",
]
TARGETS = UPDATE_TARGETS + CREATE_TARGETS
VALIDATION_COMMANDS = [
    (
        "cd projects/ui-prototyping-studio/backend && "
        "./node_modules/.bin/tsc -p tsconfig.json --noEmit"
    ),
    (
        "cd projects/ui-prototyping-studio/backend && "
        "./node_modules/.bin/tsx --test \"src/**/*.test.ts\""
    ),
    (
        "cd projects/ui-prototyping-studio/backend && "
        "./node_modules/.bin/playwright test "
        "e2e/visible-change-diff.spec.ts --reporter=list"
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
        target: (STAGED_PREFIX / target).as_posix() for target in TARGETS
    }
    dependency_ids = list(DEPENDENCIES)
    document = {
        "schema_version": "1.0.0",
        "package_id": PACKAGE_ID,
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
                "operation": (
                    "create" if target in CREATE_TARGETS else "update"
                ),
                "output_ref": exact_ref(staged_paths[target]),
            }
            for target in TARGETS
        ],
        "target_inventory": [
            {
                "target_path": target,
                "lifecycle_owner": LIFECYCLE_OWNER,
                "authority_class": "private",
                "publication_class": "private",
                "dependency_ids": dependency_ids,
            }
            for target in TARGETS
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
            "scope_paths": TARGETS,
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
