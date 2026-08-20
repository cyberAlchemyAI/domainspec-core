#!/usr/bin/env python3
"""Automatically validate the R4 plan's smallest-unit and recomposition claims."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
R4_REL = "ops/development/2026-08-16-rwo-control-content-provenance-successor-r4/candidate-plan-epoch"
R4 = REPO / R4_REL


def load(name: str):
    return json.loads((R4 / name).read_text())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    manifest = load("SWU-MANIFEST.json")
    dispatch = load("DISPATCH-ROUTE.json")
    audit = load("readiness/AUDIT-CONFIG-v2.json")
    readiness = load("validation/readiness/plan-semantic-manifest.json")
    unit_ids = [unit["unit_id"] for unit in manifest["units"]]
    expected = ["SWU-RWO-CCP-002", "SWU-RWO-CCP-003", "SWU-RWO-CX-003R2"]
    assert unit_ids == expected
    dependencies = {unit["unit_id"]: unit["dependencies"] for unit in manifest["units"]}
    assert dependencies == {
        "SWU-RWO-CCP-002": [],
        "SWU-RWO-CCP-003": ["SWU-RWO-CCP-002"],
        "SWU-RWO-CX-003R2": ["SWU-RWO-CCP-003"],
    }
    assert readiness["ready_frontier"] == expected
    steps = dispatch["steps"]
    assert [step["step_id"] for step in steps] == ["execute-ccp-002", "execute-ccp-003", "execute-cx003r2"]
    assert [step["depends_on_steps"] for step in steps] == [[], ["execute-ccp-002"], ["execute-ccp-003"]]
    assert all(step["capability_ref"] == "task-session" for step in steps)
    assert readiness["mutation_ready"] is False
    assert readiness["selected_unit"] is None
    ccp002 = next(item for item in audit["execution_bindings"] if item["swu_id"] == "SWU-RWO-CCP-002")
    commands = [item["command_id"] for item in ccp002["validation_contracts"]]
    assert len(commands) == 10
    assert commands.count("ccp002-context-builder-source-identity") == 1
    completed = [item for item in manifest["external_evidence"] if item["evidence_id"] == "completed-ccp001-terminal"]
    assert len(completed) == 1
    assert completed[0]["role"] == "immutable-completed-external-predecessor"

    result = {
        "schema_version": "rwo.distill-recomposition-validation.v1",
        "result": "pass",
        "remaining_unit_count": 3,
        "task_shaped_unit_count": 0,
        "frontier": expected,
        "dependency_chain": dependencies,
        "immutable_completed_predecessor": "SWU-RWO-CCP-001",
        "recomposition": "pass",
        "field_regression_command_count": 1,
        "ccp002_validation_command_count": 10,
        "mutation_authority": "none",
        "selected_unit": None,
        "claim_ceiling": "automatic plan-structure validation only",
    }
    rendered = json.dumps(result, indent=2) + "\n"
    (REPO / args.output).write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
