#!/usr/bin/env python3
"""Build the exact Invoke Refresh closeout package for SWU-GSP-006."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[8]
CLOSEOUT_ROOT = Path(__file__).resolve().parent.parent
STAGED_PREFIX = CLOSEOUT_ROOT.relative_to(REPO_ROOT) / "material" / "staged"
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
TARGETS = [
    f"{PLAN_RUN}/WORK-PACK.md",
    "projects/ui-prototyping-studio/.craft/ledger.yml",
    "projects/ui-prototyping-studio/CRAFT.md",
]
DEPENDENCIES = {
    "task-session-result": f"{SESSION_RUN}/TASK-SESSION-RESULT.json",
    "closeout-preflight": f"{SESSION_RUN}/CLOSEOUT-PREFLIGHT.json",
}
VALIDATION_COMMANDS = [
    (
        "cd projects/ui-prototyping-studio && python3 "
        "development/invoke-runs/20260727T044346Z-chain-contract-refresh/"
        "scripts/validate-chain-contract.py"
    ),
    (
        "python3 -c \"import yaml; "
        "yaml.safe_load(open('projects/ui-prototyping-studio/.craft/"
        "ledger.yml'))\""
    ),
    "git diff --check -- projects/ui-prototyping-studio",
]
LIFECYCLE_OWNER = (
    "private UI Prototyping Studio planning and Craft owner via invoke:refresh"
)


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
        "package_id": "ups-gsp-006-closeout-20260727",
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": LIFECYCLE_OWNER,
        "authority_class": "private",
        "publication_class": "private",
        "source_artifacts": [
            {**exact_ref(path), "authority_class": "private"}
            for path in list(DEPENDENCIES.values()) + TARGETS
        ],
        "changes": [
            {
                "target_path": target,
                "operation": "update",
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
