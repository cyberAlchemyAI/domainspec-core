#!/usr/bin/env python3
"""Stage the exact Continuation route repair discovered by readiness audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[7]
RUN_ROOT = Path(
    "projects/body-war/development/invoke-runs/"
    "20260730T050022Z-ontology-focus-scene-pivot"
)
TARGET = RUN_ROOT / "CONTINUATION.json"
STAGED = HERE / "staged" / TARGET
OWNER = "private Body War OFSP planning owner via invoke:refresh"


def ref(path: Path) -> dict[str, Any]:
    content = (ROOT / path).read_bytes()
    return {
        "path": path.as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def main() -> int:
    continuation = {
        "schema_version": "body-war.invoke-continuation.v2",
        "run_id": "20260730T050022Z-ontology-focus-scene-pivot",
        "state": "blocked-runtime-admission",
        "selected_swu": None,
        "first_selectable_swu": None,
        "selection_allowed": False,
        "selection_requires": [
            "work-pack-readiness-plan-contract-pass",
            "runtime-admission-pass",
            "explicit-user-selection",
            "task-session-preflight",
        ],
        "runtime_blockers": [
            {
                "id": "OFSP-MATERIAL-PACKAGE-ADMISSION",
                "unit_count": 22,
                "owner": "invoke material producer plus selected Task Session",
                "claim": "material units lack current exact material-package admission",
            },
            {
                "id": "OFSP-NON-MATERIAL-TASK-ADMISSION",
                "unit_count": 7,
                "owner": "task-session lifecycle via sigil-development",
                "claim": "output-only and audit-only units have no truthful routed execution mode",
            },
        ],
        "automatic_execution": False,
        "authority_effect": "none",
        "release_admission": "not-granted",
        "completed_gates": [
            "define-pass",
            "design-validator-pass",
            "dispatch-spec-pass",
            "distill-validation-pass",
            "work-pack-readiness-plan-contract-pass",
            "terminal-receipt-semantics-pass",
        ],
        "next_route": "task-session-runtime-contract-repair",
    }
    STAGED.parent.mkdir(parents=True, exist_ok=True)
    STAGED.write_text(
        json.dumps(continuation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    refresh_rel = HERE.parent.relative_to(ROOT)
    final_report = (
        RUN_ROOT
        / "readiness-runs/post-refresh-final/work-pack-readiness-report.json"
    )
    final_signals = (
        RUN_ROOT / "readiness-runs/post-refresh-final/REFRESH-SIGNAL-PACK.json"
    )
    sources = [
        TARGET,
        RUN_ROOT / "WORK-PACK.md",
        final_report,
        final_signals,
        refresh_rel / "audit-closeout/REFRESH-HANDOFF-RESULT.json",
    ]
    dependencies = [
        {
            "dependency_id": "final-readiness-audit",
            "artifact_ref": ref(final_report),
        },
        {
            "dependency_id": "audit-closed-work-pack",
            "artifact_ref": ref(RUN_ROOT / "WORK-PACK.md"),
        },
    ]
    staged_rel = STAGED.relative_to(ROOT)
    package = {
        "schema_version": "1.0.0",
        "package_id": "body-war-ofsp-continuation-route-repair-20260730T061441Z",
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": OWNER,
        "authority_class": "private",
        "publication_class": "private",
        "source_artifacts": [
            {**ref(path), "authority_class": "private"} for path in sources
        ],
        "changes": [
            {
                "target_path": TARGET.as_posix(),
                "operation": "update",
                "output_ref": ref(staged_rel),
            }
        ],
        "target_inventory": [
            {
                "target_path": TARGET.as_posix(),
                "lifecycle_owner": OWNER,
                "authority_class": "private",
                "publication_class": "private",
                "dependency_ids": [
                    "final-readiness-audit",
                    "audit-closed-work-pack",
                ],
            }
        ],
        "dependencies": dependencies,
        "mirror_groups": [],
        "approval": {
            "class": "explicit-apply",
            "owner": OWNER,
            "scope_paths": [TARGET.as_posix()],
            "authority_classes": ["private"],
            "publication_classes": ["private"],
        },
        "validation_commands": [
            "python3 -m json.tool <staged>/CONTINUATION.json",
            (
                "python3 arcanum/spells/work-pack-readiness-audit/scripts/"
                "audit_work_pack.py --config <final-config> "
                "--output-dir <final-handoff-audit-run>"
            ),
        ],
    }
    (HERE / "MATERIAL-PACKAGE.json").write_text(
        json.dumps(package, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"targets": 1, "package_id": package["package_id"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
