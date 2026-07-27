#!/usr/bin/env python3
"""Build the exact material package for the approved Studio plan refresh."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[6]
REFRESH_ROOT = Path(__file__).resolve().parent.parent
STAGED_PREFIX = REFRESH_ROOT.relative_to(REPO_ROOT) / "material" / "staged"
OUTPUT = Path(__file__).resolve().parent / "MATERIAL-PACKAGE.json"

PACKAGE_ID = "ups-gsp-architecture-review-refresh-apply-20260727"
LIFECYCLE_OWNER = (
    "private UI Prototyping Studio planning and Craft owner via invoke:refresh"
)

RUN_ROOT = (
    "projects/ui-prototyping-studio/development/invoke-runs/"
    "20260727T042935Z-architecture-review-refresh"
)

CREATE_TARGETS = [
    f"{RUN_ROOT}/WORK-PACK.md",
    f"{RUN_ROOT}/EXECUTION-PACK.md",
    f"{RUN_ROOT}/DISTILL-VALIDATION.md",
    f"{RUN_ROOT}/work-pack/tasks/TASK-GSP-001-evidence-harness.md",
    f"{RUN_ROOT}/work-pack/tasks/TASK-GSP-002-store-freshness.md",
    f"{RUN_ROOT}/work-pack/tasks/TASK-GSP-003-current-head-projection.md",
    f"{RUN_ROOT}/work-pack/tasks/TASK-GSP-004-visible-change-diff.md",
    f"{RUN_ROOT}/work-pack/tasks/TASK-GSP-005-action-annotation-mobile.md",
    f"{RUN_ROOT}/work-pack/tasks/TASK-GSP-006-handoff-readiness.md",
    f"{RUN_ROOT}/work-pack/tasks/TASK-GSP-007-docs-craft-closeout.md",
]

UPDATE_TARGETS = [
    (
        "projects/ui-prototyping-studio/development/invoke-runs/"
        "20260710T012443Z-governed-state-projection/README.md"
    ),
    "projects/ui-prototyping-studio/.craft/ledger.yml",
    "projects/ui-prototyping-studio/CRAFT.md",
]

TARGETS = CREATE_TARGETS + UPDATE_TARGETS

DEPENDENCIES = {
    "accepted-review": (
        "projects/ui-prototyping-studio/development/reviews/"
        "20260727-architecture-plan-deep-spec-review/findings.md"
    ),
    "parent-approval": (
        "projects/ui-prototyping-studio/development/reviews/"
        "20260727-architecture-plan-deep-spec-review/PARENT-APPROVAL.md"
    ),
    "refresh-proposal": f"{RUN_ROOT}/REFRESH-PATCH-PROPOSAL.md",
    "strict-context-pack": f"{RUN_ROOT}/context-pack.json",
}


def exact_ref(path: str) -> dict[str, object]:
    content = (REPO_ROOT / path).read_bytes()
    return {
        "path": path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def main() -> None:
    dependency_ids = list(DEPENDENCIES)
    staged_paths = {
        target: (STAGED_PREFIX / target).as_posix() for target in TARGETS
    }
    source_paths = list(DEPENDENCIES.values()) + UPDATE_TARGETS
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
            for path in source_paths
        ],
        "changes": [
            {
                "target_path": target,
                "operation": "create" if target in CREATE_TARGETS else "update",
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
        "validation_commands": [
            (
                "python3 -c \"import yaml; "
                "yaml.safe_load(open('projects/ui-prototyping-studio/.craft/"
                "ledger.yml'))\""
            ),
            (
                "cd projects/ui-prototyping-studio/backend && "
                "./node_modules/.bin/tsc -p tsconfig.json --noEmit"
            ),
            (
                "cd projects/ui-prototyping-studio/backend && "
                "./node_modules/.bin/tsx --test \\\"src/**/*.test.ts\\\""
            ),
            "git diff --check -- projects/ui-prototyping-studio",
        ],
    }
    OUTPUT.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
