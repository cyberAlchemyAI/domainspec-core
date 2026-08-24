#!/usr/bin/env python3
"""Stage the same-scope WORK-PACK audit-closeout delta."""

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
TARGET = RUN_ROOT / "WORK-PACK.md"
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
    current = (ROOT / TARGET).read_text(encoding="utf-8")
    old = """- plan authored/repaired: pass pending post-refresh audit
- plan evidence: pending
- runtime admission: block
- selected SWU: none
- implementation authority: not granted
- next route: rerun `work-pack-readiness-audit`; then route Task Session
  task-class admission to `sigil-development` and build a material package for
  the first explicitly selected material SWU"""
    new = """- plan authored/repaired: pass at the authoring layer
- plan-contract evidence: external `work-pack-readiness-audit` controls; the
  latest captured run must remain `plan_contract_status: pass`
- target implementation evidence: pending
- runtime admission: block
- selected SWU: none
- implementation authority: not granted
- next route: no SWU selection while runtime admission is blocked; route the
  output-only/audit-only execution-mode gap to the Task Session lifecycle owner
  and build a current material package only after an explicit material-SWU
  selection"""
    if current.count(old) != 1:
        raise SystemExit("expected one WORK-PACK audit-closeout block")
    staged = current.replace(old, new)
    STAGED.parent.mkdir(parents=True, exist_ok=True)
    STAGED.write_text(staged, encoding="utf-8")

    refresh_rel = HERE.parent.relative_to(ROOT)
    post_report = (
        RUN_ROOT
        / "readiness-runs/post-refresh-r2/work-pack-readiness-report.json"
    )
    post_signals = (
        RUN_ROOT / "readiness-runs/post-refresh-r2/REFRESH-SIGNAL-PACK.json"
    )
    sources = [
        TARGET,
        post_report,
        post_signals,
        refresh_rel / "MATERIAL-RECEIPT.json",
        refresh_rel / "REFRESH-HANDOFF-RESULT.json",
    ]
    dependencies = [
        {
            "dependency_id": "post-refresh-readiness-audit",
            "artifact_ref": ref(post_report),
        },
        {
            "dependency_id": "prior-refresh-handoff",
            "artifact_ref": ref(
                refresh_rel / "REFRESH-HANDOFF-RESULT.json"
            ),
        },
    ]
    staged_rel = STAGED.relative_to(ROOT)
    package = {
        "schema_version": "1.0.0",
        "package_id": "body-war-ofsp-work-pack-audit-closeout-20260730T061441Z",
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
                    "post-refresh-readiness-audit",
                    "prior-refresh-handoff",
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
            (
                "python3 arcanum/spells/work-pack-readiness-audit/scripts/"
                "audit_work_pack.py --config <final-config> "
                "--output-dir <final-audit-run>"
            ),
            (
                "git diff --check -- projects/body-war/development/invoke-runs/"
                "20260730T050022Z-ontology-focus-scene-pivot/WORK-PACK.md"
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
