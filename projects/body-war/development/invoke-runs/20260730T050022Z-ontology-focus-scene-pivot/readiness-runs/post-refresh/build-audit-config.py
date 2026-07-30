#!/usr/bin/env python3
"""Build the exact post-refresh adapter from applied plan bytes."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
RUN_ROOT = Path(
    "projects/body-war/development/invoke-runs/"
    "20260730T050022Z-ontology-focus-scene-pivot"
)
PRE_BUILDER_PATH = (
    ROOT / RUN_ROOT / "readiness-runs/pre-refresh/build-audit-config.py"
)
SPEC = importlib.util.spec_from_file_location("pre_builder", PRE_BUILDER_PATH)
assert SPEC is not None and SPEC.loader is not None
PRE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PRE)


def exact_ref(path: Path) -> dict[str, Any]:
    content = (ROOT / path).read_bytes()
    return {
        "path": path.as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def closure_blocks(path: Path) -> dict[str, str]:
    text = (ROOT / path).read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## (TASK-[A-Z-]+)\b.*$", text, re.M))
    result = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1)] = text[match.start() : end]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audit-id",
        default="body-war-ofsp-post-refresh-20260730",
    )
    parser.add_argument(
        "--output",
        default=(HERE / "AUDIT-CONFIG.json").as_posix(),
    )
    args = parser.parse_args()
    blocks, _ = PRE.blocks_by_unit()
    order, successors, receipts = PRE.closeout_rows()
    matrix_path = RUN_ROOT / "work-pack/shared/COMMAND-MATRIX.json"
    matrix = json.loads((ROOT / matrix_path).read_text(encoding="utf-8"))
    matrix_by_id = {unit["unit_id"]: unit for unit in matrix["units"]}
    closure_path = RUN_ROOT / "work-pack/tasks/TASK-CLOSURE.md"
    closures = closure_blocks(closure_path)
    units = []
    for unit_id in order:
        planned = dict(matrix_by_id[unit_id])
        if unit_id in blocks:
            contract_path, _ = blocks[unit_id]
        else:
            contract_path = closure_path
            if unit_id not in closures:
                raise ValueError(f"missing closure contract: {unit_id}")
        planned.update(
            {
                "contract_kind": "full-task",
                "contract_ref": exact_ref(contract_path),
                "dependency_receipts": [],
                "material_package": None,
            }
        )
        if planned["successor"] != successors[unit_id]:
            raise ValueError(f"successor drift: {unit_id}")
        if planned["closeout_receipt"] != receipts[unit_id]:
            if not unit_id.startswith("TASK-"):
                raise ValueError(f"closeout receipt drift: {unit_id}")
        units.append(planned)

    task_paths = PRE.TASK_PATHS
    semantic_validator = (
        RUN_ROOT / "work-pack/shared/validate-task-session-receipt.py"
    )
    continuation_path = RUN_ROOT / "CONTINUATION.json"
    control_paths = [
        *task_paths,
        closure_path,
        PRE.CLOSEOUT_PATH,
        PRE.CONTEXT_PATH,
        matrix_path,
        semantic_validator,
        RUN_ROOT
        / "readiness-runs/pre-refresh-r2/work-pack-readiness-report.json",
    ]
    config = {
        "schema_version": "1.0.0",
        "audit_id": args.audit_id,
        "repository_root": ".",
        "authority_class": "private",
        "publication_class": "private",
        "work_pack": exact_ref(PRE.WORK_PACK_PATH),
        "control_artifacts": [exact_ref(path) for path in control_paths],
        "task_session_request_schema": exact_ref(
            PRE.TASK_SESSION_REQUEST_SCHEMA
        ),
        "terminal_receipt_schema": exact_ref(PRE.TERMINAL_SCHEMA_PATH),
        "terminal_receipt_semantic_validator": exact_ref(semantic_validator),
        "units": units,
        "immutable_paths": [
            (
                "cyberAlchemy-v2/implementation/ontology-evidence-workbench/"
                "upstream/L1-BUILD.lock.json"
            ),
            (
                "cyberAlchemy-v2/implementation/ontology-evidence-workbench/"
                "generated/runs/BODY-WAR-ONTOLOGY-001/presentation-graph.json"
            ),
        ],
        "shared_write_owners": matrix["shared_write_owners"],
        "source_selectors": [
            (
                "projects/body-war/development/reviews/"
                "20260730-ontology-ui-black-box/findings.md"
            ),
            (
                "projects/body-war/development/reviews/"
                "20260730-ontology-ui-black-box/synthesis.md"
            ),
        ],
        "closeout_directory": {
            "path": (RUN_ROOT / "work-pack/closeout").as_posix(),
            "create_if_missing": True,
        },
        "handoff_state": {
            "artifact_ref": exact_ref(continuation_path),
            "expected_fields": {
                "state": "blocked-runtime-admission",
                "selected_swu": None,
                "first_selectable_swu": None,
                "selection_allowed": False,
                "next_route": "task-session-runtime-contract-repair",
            },
        },
        "refresh_targets": [
            PRE.WORK_PACK_PATH.as_posix(),
            PRE.CONTEXT_PATH.as_posix(),
            PRE.CLOSEOUT_PATH.as_posix(),
            PRE.TERMINAL_SCHEMA_PATH.as_posix(),
            matrix_path.as_posix(),
            semantic_validator.as_posix(),
            closure_path.as_posix(),
            continuation_path.as_posix(),
        ],
        "next_owner": "invoke:refresh",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
