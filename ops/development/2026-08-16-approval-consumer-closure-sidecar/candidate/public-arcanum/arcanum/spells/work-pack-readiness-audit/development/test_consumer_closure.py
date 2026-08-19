#!/usr/bin/env python3
"""Public-generic regression tests for the pre-acceptance closure guard."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SPELL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SPELL_ROOT / "scripts" / "consumer_closure.py"
SPEC = importlib.util.spec_from_file_location("consumer_closure", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {SCRIPT}")
CLOSURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLOSURE)


class GuardFixture:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative in CLOSURE.CONSUMER_PATHS.values():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"synthetic consumer: {relative}\n", encoding="utf-8")
        self.inputs: dict[str, Path] = {}
        input_documents = {
            "execution_contracts": {"work_pack_id": "synthetic-work-pack"},
            "audit_config": {
                "audit_id": "synthetic-audit",
                "execution_policy": {"work_pack_id": "synthetic-work-pack"},
            },
            "audit_report": {
                "audit_id": "synthetic-audit",
                "verdict": "pass",
                "terminal_code": "PLAN_SEMANTIC_READY",
            },
            "semantic_manifest": {
                "work_pack_id": "synthetic-work-pack",
                "plan_epoch_id": "epoch-000000000000000000000000",
                "manifest_id": "psm-000000000000000000000000",
            },
            "selection_handoff": {"selection_required": True},
        }
        for name in CLOSURE.INPUT_NAMES:
            path = self.root / "inputs" / f"{name}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(input_documents[name]) + "\n", encoding="utf-8")
            self.inputs[name] = path
        self.draft = self.root / "draft.json"

    def close(self) -> None:
        self.temp.cleanup()

    def receipt(self) -> dict[str, object]:
        payload = {
            "schema_version": "arcanum.wpra.consumer-closure-receipt/1.0.0",
            "status": "pass",
            "check_results": [
                {
                    "check_id": check_id,
                    "status": "pass",
                    "details": {},
                    "failure_codes": [],
                }
                for check_id in CLOSURE.REQUIRED_CHECK_IDS
            ],
            "failures": [],
            "metrics": {"frontier_count": 1},
            "exact_inputs": {
                name: CLOSURE.exact_ref(self.root, path)
                for name, path in self.inputs.items()
            },
            "canonical_consumers": CLOSURE.consumer_refs(self.root),
            "closure_implementation_sha256": CLOSURE.closure_implementation_sha256(),
            "authority_effect": "none",
            "selection_performed": False,
            "mutation_performed": False,
            "configured_unit_commands_executed": False,
            "claim_ceiling": "synthetic contract compatibility only",
        }
        return {**payload, "receipt_digest": CLOSURE.canonical_digest(payload)}

    def write_receipt(self, value: dict[str, object]) -> Path:
        path = self.root / "closure-receipt.json"
        path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
        draft = {
            "kind": "synthetic-acceptance-draft",
            **CLOSURE.guarded_draft_binding(self.root, path, self.inputs),
        }
        self.draft.write_text(json.dumps(draft, sort_keys=True) + "\n", encoding="utf-8")
        return path


class ConsumerClosureGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = GuardFixture()

    def tearDown(self) -> None:
        self.fixture.close()

    def assert_guard_blocks(self, receipt: dict[str, object]) -> None:
        receipt_path = self.fixture.write_receipt(receipt)
        output = self.fixture.root / "acceptance.json"
        with self.assertRaises(CLOSURE.ConsumerClosureError):
            CLOSURE.write_guarded_artifact(
                self.fixture.root,
                receipt_path,
                self.fixture.inputs,
                self.fixture.draft,
                output,
            )
        self.assertFalse(output.exists())

    def test_passing_current_receipt_is_the_only_emission_path(self) -> None:
        receipt_path = self.fixture.write_receipt(self.fixture.receipt())
        output = self.fixture.root / "acceptance.json"
        CLOSURE.write_guarded_artifact(
            self.fixture.root,
            receipt_path,
            self.fixture.inputs,
            self.fixture.draft,
            output,
        )
        self.assertEqual(output.read_bytes(), self.fixture.draft.read_bytes())

    def test_presence_only_receipt_cannot_emit(self) -> None:
        self.assert_guard_blocks({})

    def test_failing_receipt_cannot_emit(self) -> None:
        receipt = self.fixture.receipt()
        receipt["status"] = "block"
        receipt["failures"] = [{"code": "SYNTHETIC_BLOCK", "detail": "blocked"}]
        payload = {key: value for key, value in receipt.items() if key != "receipt_digest"}
        receipt["receipt_digest"] = CLOSURE.canonical_digest(payload)
        self.assert_guard_blocks(receipt)

    def test_stale_input_receipt_cannot_emit(self) -> None:
        receipt_path = self.fixture.write_receipt(self.fixture.receipt())
        self.fixture.inputs["audit_config"].write_text(
            json.dumps({"name": "audit_config", "changed": True}) + "\n",
            encoding="utf-8",
        )
        output = self.fixture.root / "acceptance.json"
        with self.assertRaisesRegex(
            CLOSURE.ConsumerClosureError, "CLOSURE_RECEIPT_INPUT_STALE"
        ):
            CLOSURE.write_guarded_artifact(
                self.fixture.root,
                receipt_path,
                self.fixture.inputs,
                self.fixture.draft,
                output,
            )
        self.assertFalse(output.exists())

    def test_stale_consumer_receipt_cannot_emit(self) -> None:
        receipt_path = self.fixture.write_receipt(self.fixture.receipt())
        consumer = self.fixture.root / next(iter(CLOSURE.CONSUMER_PATHS.values()))
        consumer.write_text("changed consumer\n", encoding="utf-8")
        output = self.fixture.root / "acceptance.json"
        with self.assertRaisesRegex(
            CLOSURE.ConsumerClosureError, "CLOSURE_RECEIPT_CONSUMER_STALE"
        ):
            CLOSURE.write_guarded_artifact(
                self.fixture.root,
                receipt_path,
                self.fixture.inputs,
                self.fixture.draft,
                output,
            )
        self.assertFalse(output.exists())

    def test_authority_bearing_receipt_cannot_emit(self) -> None:
        receipt = self.fixture.receipt()
        receipt["selection_performed"] = True
        payload = {key: value for key, value in receipt.items() if key != "receipt_digest"}
        receipt["receipt_digest"] = CLOSURE.canonical_digest(payload)
        self.assert_guard_blocks(receipt)

    def test_omitted_required_check_cannot_emit(self) -> None:
        receipt = self.fixture.receipt()
        receipt["check_results"].pop()
        payload = {key: value for key, value in receipt.items() if key != "receipt_digest"}
        receipt["receipt_digest"] = CLOSURE.canonical_digest(payload)
        self.assert_guard_blocks(receipt)

    def test_nonpassing_required_check_cannot_emit(self) -> None:
        receipt = self.fixture.receipt()
        receipt["check_results"][0]["status"] = "not-run"
        payload = {key: value for key, value in receipt.items() if key != "receipt_digest"}
        receipt["receipt_digest"] = CLOSURE.canonical_digest(payload)
        self.assert_guard_blocks(receipt)

    def test_stale_validator_digest_cannot_emit(self) -> None:
        receipt = self.fixture.receipt()
        receipt["closure_implementation_sha256"]["validator"] = "0" * 64
        payload = {key: value for key, value in receipt.items() if key != "receipt_digest"}
        receipt["receipt_digest"] = CLOSURE.canonical_digest(payload)
        self.assert_guard_blocks(receipt)

    def test_passing_check_cannot_carry_failure_codes(self) -> None:
        receipt = self.fixture.receipt()
        receipt["check_results"][0]["failure_codes"] = ["SYNTHETIC_FAILURE"]
        payload = {key: value for key, value in receipt.items() if key != "receipt_digest"}
        receipt["receipt_digest"] = CLOSURE.canonical_digest(payload)
        self.assert_guard_blocks(receipt)

    def test_missing_closure_reference_cannot_emit(self) -> None:
        receipt_path = self.fixture.write_receipt(self.fixture.receipt())
        draft = json.loads(self.fixture.draft.read_text(encoding="utf-8"))
        draft.pop("consumer_closure_receipt_ref")
        self.fixture.draft.write_text(json.dumps(draft) + "\n", encoding="utf-8")
        output = self.fixture.root / "acceptance.json"
        with self.assertRaisesRegex(
            CLOSURE.ConsumerClosureError, "GUARDED_DRAFT_BINDING_MISSING"
        ):
            CLOSURE.write_guarded_artifact(
                self.fixture.root,
                receipt_path,
                self.fixture.inputs,
                self.fixture.draft,
                output,
            )
        self.assertFalse(output.exists())

    def test_stale_draft_epoch_cannot_emit(self) -> None:
        receipt_path = self.fixture.write_receipt(self.fixture.receipt())
        draft = json.loads(self.fixture.draft.read_text(encoding="utf-8"))
        draft["plan_epoch_id"] = "epoch-ffffffffffffffffffffffff"
        self.fixture.draft.write_text(json.dumps(draft) + "\n", encoding="utf-8")
        output = self.fixture.root / "acceptance.json"
        with self.assertRaisesRegex(
            CLOSURE.ConsumerClosureError, "GUARDED_DRAFT_BINDING_STALE"
        ):
            CLOSURE.write_guarded_artifact(
                self.fixture.root,
                receipt_path,
                self.fixture.inputs,
                self.fixture.draft,
                output,
            )
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
