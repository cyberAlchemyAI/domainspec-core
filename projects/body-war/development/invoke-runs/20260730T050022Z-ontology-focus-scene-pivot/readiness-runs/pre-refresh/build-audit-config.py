#!/usr/bin/env python3
"""Build the exact pre-refresh adapter for the generic readiness audit."""

from __future__ import annotations

import hashlib
import json
import re
import shlex
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[7]
RUN_ROOT = Path(
    "projects/body-war/development/invoke-runs/"
    "20260730T050022Z-ontology-focus-scene-pivot"
)
WORKBENCH_ROOT = (
    "cyberAlchemy-v2/implementation/ontology-evidence-workbench"
)
TASK_PATHS = [
    RUN_ROOT / "work-pack/tasks/TASK-FOUNDATION.md",
    RUN_ROOT / "work-pack/tasks/TASK-PROJECTION.md",
    RUN_ROOT / "work-pack/tasks/TASK-STATE.md",
    RUN_ROOT / "work-pack/tasks/TASK-NATIVE-UI.md",
    RUN_ROOT / "work-pack/tasks/TASK-ACCEPTANCE.md",
    RUN_ROOT / "work-pack/tasks/TASK-RELIABILITY.md",
    RUN_ROOT / "work-pack/tasks/TASK-PACKAGE.md",
]
CLOSEOUT_PATH = RUN_ROOT / "work-pack/shared/CLOSEOUT-CONTRACT.md"
CONTEXT_PATH = RUN_ROOT / "work-pack/shared/CONTEXT.md"
WORK_PACK_PATH = RUN_ROOT / "WORK-PACK.md"
TERMINAL_SCHEMA_PATH = RUN_ROOT / "TASK-SESSION-RECEIPT.schema.json"
TASK_SESSION_REQUEST_SCHEMA = Path(
    "arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json"
)
DRY_RUN_PATH = RUN_ROOT / "IMPLEMENTATION-READINESS-DRY-RUN.md"


def exact_ref(path: Path) -> dict[str, Any]:
    content = (REPOSITORY_ROOT / path).read_bytes()
    return {
        "path": path.as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def blocks_by_unit() -> tuple[dict[str, tuple[Path, str]], list[str]]:
    blocks: dict[str, tuple[Path, str]] = {}
    order: list[str] = []
    for path in TASK_PATHS:
        text = (REPOSITORY_ROOT / path).read_text(encoding="utf-8")
        matches = list(re.finditer(r"^## (SWU-OFSP-[0-9]{3})\b.*$", text, re.M))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            unit_id = match.group(1)
            blocks[unit_id] = (path, text[match.start() : end])
            order.append(unit_id)
    return blocks, order


def normalized_id(raw: str) -> str:
    value = raw.strip().strip("`")
    if re.fullmatch(r"[0-9]{3}", value):
        return f"SWU-OFSP-{value}"
    return value


def closeout_rows() -> tuple[list[str], dict[str, str | None], dict[str, str]]:
    text = (REPOSITORY_ROOT / CLOSEOUT_PATH).read_text(encoding="utf-8")
    order: list[str] = []
    successors: dict[str, str | None] = {}
    receipts: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(cells) != 4:
            continue
        raw_unit, _, receipt, raw_successor = cells
        if not (
            re.fullmatch(r"[0-9]{3}", raw_unit)
            or raw_unit.startswith("TASK-")
        ):
            continue
        unit_id = normalized_id(raw_unit)
        successor = None if raw_successor == "none" else normalized_id(raw_successor)
        order.append(unit_id)
        successors[unit_id] = successor
        receipts[unit_id] = receipt
    return order, successors, receipts


def dependencies(block: str, unit_id: str) -> list[str]:
    match = re.search(
        r"- Dependencies:\s*(.*?)(?=\n- (?:Source anchors|Write scope|Owner)|\n##|\Z)",
        block,
        re.S,
    )
    if match is None or "none" in match.group(1).lower():
        return []
    values = [
        normalized_id(value)
        for value in re.findall(r"\b[0-9]{3}\b|TASK-[A-Z-]+", match.group(1))
    ]
    return list(dict.fromkeys(values))


def write_paths(block: str) -> list[str]:
    match = re.search(
        r"- Write scope:\s*(.*?)(?=\n- (?:Done|Validation|Owner)|\n##|\Z)",
        block,
        re.S,
    )
    if match is None:
        return []
    paths = []
    for value in re.findall(r"`([^`]+)`", match.group(1)):
        if "/" not in value or value.startswith(("SPEC.md", "ARCHITECTURE.md")):
            continue
        normalized = value.rstrip("/")
        if "/generated/runs/SWU-OFSP-" in normalized:
            normalized += "/{attempt_id}"
        paths.append(normalized)
    return list(dict.fromkeys(paths))


def validation_commands(block: str) -> list[dict[str, Any]]:
    match = re.search(r"(?:Done/validation|Validation):\s*(.*)", block, re.S)
    if match is None:
        return []
    commands = []
    for candidate in re.findall(r"`([^`]+)`", match.group(1)):
        if not candidate.startswith(("node ", "git ", "python3 ", "bash ")):
            continue
        argv = shlex.split(candidate)
        commands.append(
            {
                "cwd": WORKBENCH_ROOT,
                "argv": argv,
                "expected_exit_code": 0,
                "timeout_seconds": 300,
                "environment": {},
                "runtime_identity": {
                    "executable": argv[0],
                    "version_policy": "resolve and record exact version at Task Session preflight",
                    "hash_policy": "resolve and hash exact executable at Task Session preflight",
                },
                "risk_class": "read-only",
            }
        )
    return commands


def empty_attempt(required: bool) -> dict[str, Any]:
    return {
        "required": required,
        "id_algorithm": "",
        "collision_policy": "fail-if-exists",
        "retention_policy": "retain-receipt-only",
        "teardown_on_success": [],
        "teardown_on_failure": [],
    }


def build_unit(
    unit_id: str,
    contract_path: Path,
    block: str,
    successor: str | None,
    closeout_receipt: str,
) -> dict[str, Any]:
    paths = write_paths(block)
    outputs = [path for path in paths if "/generated/runs/" in path]
    material = [path for path in paths if path not in outputs]
    output_only = unit_id in {
        "SWU-OFSP-014",
        "SWU-OFSP-016",
        "SWU-OFSP-022",
        "SWU-OFSP-023",
    }
    task_class = "output-only" if output_only else "material-mutation"
    parent = contract_path.name
    dispatch_step = {
        "TASK-FOUNDATION.md": "s1",
        "TASK-PROJECTION.md": "s2",
        "TASK-STATE.md": "s3",
        "TASK-NATIVE-UI.md": "s4",
        "TASK-ACCEPTANCE.md": "s5",
        "TASK-RELIABILITY.md": "s6",
        "TASK-PACKAGE.md": "s6",
    }[parent]
    return {
        "unit_id": unit_id,
        "task_class": task_class,
        "state": "planned",
        "requested_execution_mode": "routed-mutation",
        "contract_kind": "full-task",
        "contract_ref": exact_ref(contract_path),
        "dependencies": dependencies(block, unit_id),
        "dependency_receipts": [],
        "successor": successor,
        "dispatch_step": dispatch_step,
        "material_writes": material,
        "execution_outputs": outputs,
        "allowed_writes": material + outputs,
        "validation_commands": validation_commands(block),
        "attempt": empty_attempt(bool(outputs)),
        "material_package": None,
        "terminal_receipt": (
            f"projects/body-war/development/task-sessions/{unit_id}/"
            "TERMINAL-RECEIPT.json"
        ),
        "closeout_receipt": closeout_receipt,
    }


def closure_unit(
    unit_id: str,
    dependency: str,
    successor: str | None,
    closeout_receipt: str,
) -> dict[str, Any]:
    return {
        "unit_id": unit_id,
        "task_class": "audit-only",
        "state": "planned",
        "requested_execution_mode": "routed-mutation",
        "contract_kind": "row-only",
        "contract_ref": exact_ref(CLOSEOUT_PATH),
        "dependencies": [dependency],
        "dependency_receipts": [],
        "successor": successor,
        "dispatch_step": "s6",
        "material_writes": [],
        "execution_outputs": [closeout_receipt],
        "allowed_writes": [closeout_receipt],
        "validation_commands": [],
        "attempt": empty_attempt(False),
        "material_package": None,
        "terminal_receipt": (
            f"projects/body-war/development/task-sessions/{unit_id}/"
            "TERMINAL-RECEIPT.json"
        ),
        "closeout_receipt": closeout_receipt,
    }


def main() -> int:
    blocks, _ = blocks_by_unit()
    order, successors, receipts = closeout_rows()
    units = []
    closure_dependencies = {
        "TASK-VERIFY": "SWU-OFSP-025",
        "TASK-AUDIT-ALIGNMENT": "TASK-VERIFY",
        "TASK-AUDIT-LAYERING": "TASK-AUDIT-ALIGNMENT",
    }
    for unit_id in order:
        if unit_id in blocks:
            path, block = blocks[unit_id]
            units.append(
                build_unit(
                    unit_id,
                    path,
                    block,
                    successors[unit_id],
                    receipts[unit_id],
                )
            )
        else:
            units.append(
                closure_unit(
                    unit_id,
                    closure_dependencies[unit_id],
                    successors[unit_id],
                    receipts[unit_id],
                )
            )

    control_paths = [
        *TASK_PATHS,
        CLOSEOUT_PATH,
        CONTEXT_PATH,
        DRY_RUN_PATH,
    ]
    config = {
        "schema_version": "1.0.0",
        "audit_id": "body-war-ofsp-pre-refresh-20260730",
        "repository_root": ".",
        "authority_class": "private",
        "publication_class": "private",
        "work_pack": exact_ref(WORK_PACK_PATH),
        "control_artifacts": [exact_ref(path) for path in control_paths],
        "task_session_request_schema": exact_ref(TASK_SESSION_REQUEST_SCHEMA),
        "terminal_receipt_schema": exact_ref(TERMINAL_SCHEMA_PATH),
        "terminal_receipt_semantic_validator": None,
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
        "shared_write_owners": [],
        "source_selectors": ["findings.md", "synthesis.md"],
        "closeout_directory": {
            "path": (RUN_ROOT / "work-pack/closeout").as_posix(),
            "create_if_missing": False,
        },
        "refresh_targets": [
            WORK_PACK_PATH.as_posix(),
            CONTEXT_PATH.as_posix(),
            CLOSEOUT_PATH.as_posix(),
            TERMINAL_SCHEMA_PATH.as_posix(),
            *[path.as_posix() for path in TASK_PATHS],
        ],
        "next_owner": "invoke:refresh",
    }
    output = Path(__file__).with_name("AUDIT-CONFIG.json")
    output.write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
