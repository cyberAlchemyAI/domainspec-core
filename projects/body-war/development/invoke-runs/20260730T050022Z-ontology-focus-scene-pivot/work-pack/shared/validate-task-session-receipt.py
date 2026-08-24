#!/usr/bin/env python3
"""Validate Body War OFSP terminal receipt semantics against an audit config."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def validate(receipt: dict[str, Any], config: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors = [
        f"schema:{'/'.join(map(str, error.absolute_path)) or '<root>'}:{error.message}"
        for error in Draft202012Validator(schema).iter_errors(receipt)
    ]
    by_id = {unit["unit_id"]: unit for unit in config["units"]}
    unit = by_id.get(receipt.get("unit_id"))
    if unit is None:
        errors.append("unit is outside captured audit frontier")
        return sorted(errors)
    expected = {
        "step_id": unit["dispatch_step"],
        "work_pack_sha256": config["work_pack"]["sha256"],
        "successor": unit["successor"],
        "execution_class": unit["task_class"],
        "expected_closeout_receipt": unit["closeout_receipt"],
    }
    for key, value in expected.items():
        if receipt.get(key) != value:
            errors.append(f"{key} mismatch")
    touched = set(receipt.get("files_touched", []))
    allowed = set(unit["allowed_writes"])
    if not touched <= allowed:
        errors.append("files_touched escapes allowed writes")
    artifact_paths = {
        item.get("path")
        for item in receipt.get("artifacts", [])
        if isinstance(item, dict)
    }
    if not artifact_paths <= allowed:
        errors.append("artifact path escapes allowed writes")
    required_attempt = unit["attempt"]["required"]
    if required_attempt and not receipt.get("attempt_id"):
        errors.append("attempt_id required for attempt-producing unit")
    if not required_attempt and receipt.get("attempt_id") is not None:
        errors.append("attempt_id forbidden for non-attempt unit")
    if receipt.get("status") == "pass" and receipt.get("teardown_result") == "block":
        errors.append("pass receipt cannot carry blocked teardown")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--audit-config", type=Path)
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--closure-task")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.closure_task:
        raise SystemExit(
            "closure execution is not implemented by the semantic validator; "
            "Task Session output-only admission remains blocked"
        )
    if not (args.receipt and args.audit_config and args.schema):
        raise SystemExit("--receipt, --audit-config, and --schema are required")
    errors = validate(load(args.receipt), load(args.audit_config), load(args.schema))
    result = {"verdict": "pass" if not errors else "block", "errors": errors}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
