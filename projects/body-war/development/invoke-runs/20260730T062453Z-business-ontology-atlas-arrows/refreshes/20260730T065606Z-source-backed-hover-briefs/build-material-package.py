#!/usr/bin/env python3
"""Build the deterministic Invoke Refresh material package from closed staging."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[7]
REFRESH_ROOT = Path(__file__).resolve().parent
RUN_ROOT = REFRESH_ROOT.parents[1]
STAGED_ROOT = REFRESH_ROOT / "material" / "staged"
LIFECYCLE_OWNER = (
    "private Body War business ontology atlas planning owner via invoke:refresh"
)
DEPENDENCY_FILES = {
    "dependency:context-pack": REFRESH_ROOT / "CONTEXT-PACK.md",
    "dependency:refresh-signals": REFRESH_ROOT / "REFRESH-SIGNALS.json",
    "dependency:helper-receipt": REFRESH_ROOT / "HELPER-RECEIPT.md",
    "dependency:staged-target-inventory": (
        REFRESH_ROOT / "STAGED-TARGET-INVENTORY.json"
    ),
    "dependency:staged-validation": REFRESH_ROOT / "STAGED-VALIDATION.md",
}
SOURCE_FILES = [
    REFRESH_ROOT / "CONTEXT-PACK.md",
    REFRESH_ROOT / "INVENTORY-LOOKUP.json",
    REFRESH_ROOT / "HELPER-RECEIPT.md",
    REFRESH_ROOT / "REFRESH-SIGNALS.json",
    REFRESH_ROOT / "TARGET-INVENTORY.json",
    REFRESH_ROOT / "DISPATCH-TRACE.md",
    REFRESH_ROOT / "REFRESH-PATCH-PROPOSAL.md",
    REFRESH_ROOT / "STAGED-TARGET-INVENTORY.json",
    REFRESH_ROOT / "STAGED-VALIDATION.md",
]


def exact_ref(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(REPOSITORY_ROOT).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }


def main() -> None:
    staged_inventory = json.loads(
        (REFRESH_ROOT / "STAGED-TARGET-INVENTORY.json").read_text()
    )
    dependency_ids = list(DEPENDENCY_FILES)
    changes: list[dict[str, object]] = []
    targets: list[dict[str, object]] = []
    scope_paths: list[str] = []

    for item in staged_inventory["targets"]:
        target_path = (RUN_ROOT / item["relative_path"]).relative_to(
            REPOSITORY_ROOT
        ).as_posix()
        output_path = STAGED_ROOT / item["relative_path"]
        output_ref = exact_ref(output_path)
        assert output_ref["sha256"] == item["output_sha256"]
        assert output_ref["size_bytes"] == item["output_size_bytes"]
        changes.append(
            {
                "target_path": target_path,
                "operation": item["operation"],
                "output_ref": output_ref,
            }
        )
        targets.append(
            {
                "target_path": target_path,
                "lifecycle_owner": LIFECYCLE_OWNER,
                "authority_class": "private",
                "publication_class": "private",
                "dependency_ids": dependency_ids,
            }
        )
        scope_paths.append(target_path)

    package = {
        "schema_version": "1.0.0",
        "package_id": (
            "body-war-bwaa-source-backed-hover-briefs-20260730T065606Z"
        ),
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": LIFECYCLE_OWNER,
        "authority_class": "private",
        "publication_class": "private",
        "source_artifacts": [
            {**exact_ref(path), "authority_class": "private"}
            for path in SOURCE_FILES
        ],
        "changes": changes,
        "target_inventory": targets,
        "dependencies": [
            {
                "dependency_id": dependency_id,
                "artifact_ref": exact_ref(path),
            }
            for dependency_id, path in DEPENDENCY_FILES.items()
        ],
        "mirror_groups": [],
        "approval": {
            "class": "explicit-apply",
            "owner": LIFECYCLE_OWNER,
            "scope_paths": scope_paths,
            "authority_classes": ["private"],
            "publication_classes": ["private"],
        },
        "validation_commands": [
            "python3 -m json.tool <each refreshed JSON target>",
            "python3 arcanum/spells/invoke/scripts/design_scope_extractor.py <refreshed manifest> --repository-root <closed overlay> --manifest-schema arcanum/spells/invoke/schemas/design-scope-manifest.schema.json --output <refreshed denominator receipt>",
            "python3 arcanum/spells/invoke/scripts/design_selection_validator.py <refreshed manifest> <refreshed denominator receipt> --authored-concerns <run authored concerns> --planned-witnesses <refreshed witnesses> --schema-dir arcanum/spells/invoke/schemas --output <refreshed selection result>",
            "verify ordered SWU manifest 001 -> 002 -> 005 -> 003 -> 004, five task specs, five closeout rows, and W1 002 -> 005",
            "verify all 22 preimages and staged output digests against STAGED-TARGET-INVENTORY.json",
            "git diff --check -- projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows",
            "verify protected Body War renderer, generator, projection, tests, generated atlas, validators, and receipts retain their recorded SHA-256 digests",
        ],
    }
    destination = REFRESH_ROOT / "material" / "MATERIAL-PACKAGE.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(package, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
