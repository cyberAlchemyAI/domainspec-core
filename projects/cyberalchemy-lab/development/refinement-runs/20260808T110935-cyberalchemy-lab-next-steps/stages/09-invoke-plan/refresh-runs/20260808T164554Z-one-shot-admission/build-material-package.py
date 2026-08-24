#!/usr/bin/env python3
"""Build the exact Invoke material package for the admission-only candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PLAN = "projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/09-invoke-plan"
TARGETS = [
    f"{PLAN}/WORK-PACK.md",
    f"{PLAN}/work-pack/tasks/TASK-CAL-CONTRACTS.md",
    f"{PLAN}/work-pack/tasks/TASK-CAL-PACKAGE.md",
    f"{PLAN}/work-pack/tasks/TASK-CAL-COMPILER.md",
    f"{PLAN}/work-pack/tasks/TASK-CAL-SNAPSHOT.md",
    f"{PLAN}/work-pack/tasks/TASK-CAL-WITNESS.md",
    f"{PLAN}/work-pack/shared/CLOSEOUT-CONTRACT.md",
    f"{PLAN}/work-pack/shared/CLOSEOUT-TARGETS.json",
    f"{PLAN}/work-pack/admission/README.md",
    f"{PLAN}/work-pack/admission/L0-EXECUTION-CONTRACTS.json",
    f"{PLAN}/work-pack/admission/L0-EXECUTION-CONTRACTS.schema.json",
    f"{PLAN}/work-pack/admission/TASK-SESSION-RECEIPT.schema.json",
    f"{PLAN}/work-pack/admission/CLOSEOUT-RECEIPT.schema.json",
    f"{PLAN}/work-pack/admission/FINITE-FRONTIER-CONTRACT.json",
    f"{PLAN}/work-pack/admission/FINITE-FRONTIER-CONTRACT.schema.json",
    f"{PLAN}/work-pack/admission/validate-admission.py",
    f"{PLAN}/work-pack/admission/WPRA-CONFIG.json",
]
UPDATES = set(TARGETS[:8])
SOURCES = [
    "projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/06-invoke-design/ARCHITECTURE.md",
    "projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/08-distill-repair.md",
    f"{PLAN}/EXECUTION-ENTRY.json",
    f"{PLAN}/EXECUTION-ENTRY-VALIDATION.json",
]


def exact(root: Path, relative: str) -> dict:
    path = root / relative
    data = path.read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}


def build(root: Path) -> dict:
    dependencies = [
        {"dependency_id": f"source-{index + 1}", "artifact_ref": exact(root, path)}
        for index, path in enumerate(SOURCES)
    ]
    dependency_ids = [item["dependency_id"] for item in dependencies]
    return {
        "schema_version": "1.0.0",
        "package_id": "invoke-refresh-wp-cal-ten-l0-one-shot-admission-20260808T164554Z",
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": "invoke:refresh",
        "authority_class": "private",
        "publication_class": "internal",
        "source_artifacts": [{**exact(root, path), "authority_class": "private"} for path in SOURCES],
        "changes": [{"target_path": path, "operation": "update" if path in UPDATES else "create", "output_ref": exact(root, path)} for path in TARGETS],
        "target_inventory": [{"target_path": path, "lifecycle_owner": "invoke:refresh", "authority_class": "private", "publication_class": "internal", "dependency_ids": dependency_ids} for path in TARGETS],
        "dependencies": dependencies,
        "mirror_groups": [],
        "approval": {"class": "explicit-apply", "owner": "invoke:refresh", "scope_paths": TARGETS, "authority_classes": ["private"], "publication_classes": ["internal"]},
        "validation_commands": [
            f"python3 {PLAN}/work-pack/admission/validate-admission.py --plan-root {PLAN}",
            f"python3 .agents/skills/work-pack-readiness-audit/scripts/audit_work_pack.py --config {PLAN}/work-pack/admission/WPRA-CONFIG.json --output-dir <fresh-run-local-output>",
            f"test $(sha256sum {PLAN}/EXECUTION-ENTRY.json | cut -d' ' -f1) = 8aff8a6f7cb7a8bbc938a7fae0e5a7cfd07514c3c6a63601a22d3410e394fec9",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(build(args.root), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
