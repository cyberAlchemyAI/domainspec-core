#!/usr/bin/env python3
"""Adversarial tests for the OFSP terminal receipt schema."""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent
SCHEMA = json.loads((ROOT.parent.parent / "TASK-SESSION-RECEIPT.schema.json").read_text())
SPEC = importlib.util.spec_from_file_location("semantic", ROOT / "validate-task-session-receipt.py")
assert SPEC and SPEC.loader
SEMANTIC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SEMANTIC)


def base() -> dict:
    return {
        "schema_version": "body-war.invoke.task-session-terminal-receipt.v2",
        "run_id": "run",
        "session_id": "session",
        "dispatch_id": "body-war-ontology-focus-scene-pivot-20260730",
        "step_id": "s1",
        "capability_ref": "task-session",
        "terminal_receipt_kind": "task-session-terminal",
        "status": "pass",
        "unit_id": "SWU-OFSP-001",
        "work_pack_sha256": "a" * 64,
        "successor": "SWU-OFSP-002",
        "execution_class": "material-mutation",
        "files_touched": ["target"],
        "artifacts": [{"path": "target", "sha256": "b" * 64, "size_bytes": 1}],
        "validation": [{"cwd": ".", "argv": ["node", "--test"], "exit_code": 0}],
        "validation_result": "pass",
        "blockers": [],
        "residue": [],
        "attempt_id": None,
        "teardown_result": "not-applicable",
        "expected_closeout_receipt": "closeout.json",
        "authority_effect": "none",
        "claim_ceiling": "bounded",
        "handoff_note": "next",
    }


class ReceiptAdversaries(unittest.TestCase):
    def reject(self, mutate) -> None:
        value = base()
        mutate(value)
        self.assertTrue(list(Draft202012Validator(SCHEMA).iter_errors(value)))

    def test_pass_not_run(self): self.reject(lambda x: x.update(validation_result="not-run"))
    def test_pass_with_blocker(self): self.reject(lambda x: x["blockers"].append("x"))
    def test_pass_without_artifacts(self): self.reject(lambda x: x.update(artifacts=[]))
    def test_pass_without_validation(self): self.reject(lambda x: x.update(validation=[]))
    def test_block_with_pass_validation(self):
        self.reject(lambda x: x.update(status="block", blockers=["x"], validation_result="pass"))
    def test_numeric_hash(self): self.reject(lambda x: x["artifacts"][0].update(sha256=7))
    def test_nested_extra_field(self): self.reject(lambda x: x["artifacts"][0].update(extra=True))
    def test_numeric_unit_id(self): self.reject(lambda x: x.update(unit_id=1))


if __name__ == "__main__":
    unittest.main()
