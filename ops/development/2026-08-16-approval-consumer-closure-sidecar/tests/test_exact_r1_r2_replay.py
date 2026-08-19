#!/usr/bin/env python3
"""Sidecar-only replay of the frozen R1 and acceptance-bound R2 artifacts."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SIDECAR = Path(__file__).resolve().parents[1]
SCRIPT = (
    SIDECAR
    / "candidate/public-arcanum/arcanum/spells/work-pack-readiness-audit/scripts/consumer_closure.py"
)
SPEC = importlib.util.spec_from_file_location("sidecar_consumer_closure", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {SCRIPT}")
CLOSURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLOSURE)

EXECUTION_ROOT = ROOT / (
    "research/2026-08-09-skillopt-arcanum-presentation/development/"
    "refinement-runs/20260816-three-next-steps-plan/execution-series/"
    "20260816-execute-everything"
)


def paths(refresh: str) -> dict[str, Path]:
    candidate = EXECUTION_ROOT / refresh / "candidate-plan-epoch"
    return {
        "execution_contracts": candidate / "SWU-MANIFEST.json",
        "audit_config": candidate / "readiness/AUDIT-CONFIG-v2.json",
        "audit_report": candidate
        / "validation/readiness/work-pack-readiness-report-v2.json",
        "semantic_manifest": candidate
        / "validation/readiness/plan-semantic-manifest.json",
        "selection_handoff": candidate
        / "validation/readiness/selection-handoff.json",
    }


R1 = paths("governed-refresh")
R2 = paths("governed-refresh-r2")


class ExactReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        (SIDECAR / "evidence/tmp").mkdir(parents=True, exist_ok=True)
        cls.r1 = CLOSURE.validate_consumer_closure(ROOT, R1)
        cls.r2 = CLOSURE.validate_consumer_closure(ROOT, R2)

    def test_frozen_r1_blocks_before_acceptance(self) -> None:
        self.assertEqual(self.r1["status"], "block")
        codes = {item["code"] for item in self.r1["failures"]}
        self.assertTrue(
            {
                "STOP_DECISION_TAXONOMY_MISMATCH",
                "IMPLEMENTATION_READINESS_INITIALIZE_REJECTED",
                "CLOSEOUT_ROUTE_COVERAGE_MISMATCH",
                "UNIT_TERMINAL_CLOSEOUT_CONTRACT_INCOMPLETE",
                "CHAIN_WPRA_BINDING_ABSENT",
            }
            <= codes
        )
        details = {
            item["detail"]
            for item in self.r1["failures"]
            if item["code"] == "STOP_DECISION_TAXONOMY_MISMATCH"
        }
        self.assertEqual(
            details,
            {
                "missing-exact-canary-dispatch-confirmation",
                "missing-exact-selector-candidate-acceptance",
            },
        )
        self.assertFalse(self.r1["selection_performed"])
        self.assertFalse(self.r1["mutation_performed"])
        self.assertFalse(self.r1["configured_unit_commands_executed"])

    def test_exact_r2_passes_all_required_consumers(self) -> None:
        self.assertEqual(self.r2["status"], "pass")
        self.assertEqual(self.r2["failures"], [])
        self.assertEqual(
            {item["check_id"] for item in self.r2["check_results"]},
            set(CLOSURE.REQUIRED_CHECK_IDS),
        )
        self.assertTrue(
            all(item["status"] == "pass" for item in self.r2["check_results"])
        )
        manifest = json.loads(R2["semantic_manifest"].read_text(encoding="utf-8"))
        frontier_count = len(manifest["ready_frontier"])
        self.assertEqual(self.r2["metrics"]["frontier_count"], frontier_count)
        route_check = next(
            item
            for item in self.r2["check_results"]
            if item["check_id"] == "frontier-derived-route-coverage"
        )
        self.assertEqual(route_check["details"]["task_route_count"], frontier_count)
        self.assertEqual(route_check["details"]["closeout_route_count"], frontier_count)
        self.assertFalse(self.r2["selection_performed"])
        self.assertFalse(self.r2["mutation_performed"])
        self.assertFalse(self.r2["configured_unit_commands_executed"])

    def test_guard_blocks_r1_presence_only_and_stale_report(self) -> None:
        with tempfile.TemporaryDirectory(dir=SIDECAR / "evidence/tmp") as raw:
            temp = Path(raw)

            r1_receipt = temp / "r1.json"
            CLOSURE.write_receipt(self.r1, r1_receipt)
            r1_draft = temp / "r1-draft.json"
            r1_draft.write_text(
                json.dumps(
                    {
                        "kind": "sidecar-synthetic-guard-probe",
                        **CLOSURE.guarded_draft_binding(ROOT, r1_receipt, R1),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            r1_output = temp / "r1-output.json"
            with self.assertRaises(CLOSURE.ConsumerClosureError):
                CLOSURE.write_guarded_artifact(
                    ROOT, r1_receipt, R1, r1_draft, r1_output
                )
            self.assertFalse(r1_output.exists())

            presence = temp / "presence.json"
            presence.write_text("{}\n", encoding="utf-8")
            presence_draft = temp / "presence-draft.json"
            presence_draft.write_text(
                json.dumps(
                    {
                        "kind": "sidecar-synthetic-guard-probe",
                        **CLOSURE.guarded_draft_binding(ROOT, presence, R2),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            presence_output = temp / "presence-output.json"
            with self.assertRaises(CLOSURE.ConsumerClosureError):
                CLOSURE.write_guarded_artifact(
                    ROOT, presence, R2, presence_draft, presence_output
                )
            self.assertFalse(presence_output.exists())

            r2_receipt = temp / "r2.json"
            CLOSURE.write_receipt(self.r2, r2_receipt)
            r2_draft = temp / "r2-draft.json"
            r2_draft.write_text(
                json.dumps(
                    {
                        "kind": "sidecar-synthetic-guard-probe",
                        **CLOSURE.guarded_draft_binding(ROOT, r2_receipt, R2),
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            stale_paths = dict(R2)
            stale_paths["audit_report"] = R1["audit_report"]
            stale_output = temp / "stale-output.json"
            with self.assertRaisesRegex(
                CLOSURE.ConsumerClosureError, "CLOSURE_RECEIPT_INPUT_STALE"
            ):
                CLOSURE.write_guarded_artifact(
                    ROOT, r2_receipt, stale_paths, r2_draft, stale_output
                )
            self.assertFalse(stale_output.exists())

            stale_draft_value = json.loads(r2_draft.read_text(encoding="utf-8"))
            stale_draft_value["plan_epoch_id"] = "epoch-ffffffffffffffffffffffff"
            stale_draft = temp / "stale-draft.json"
            stale_draft.write_text(json.dumps(stale_draft_value) + "\n", encoding="utf-8")
            stale_draft_output = temp / "stale-draft-output.json"
            with self.assertRaisesRegex(
                CLOSURE.ConsumerClosureError, "GUARDED_DRAFT_BINDING_STALE"
            ):
                CLOSURE.write_guarded_artifact(
                    ROOT, r2_receipt, R2, stale_draft, stale_draft_output
                )
            self.assertFalse(stale_draft_output.exists())

            unbound_value = json.loads(r2_draft.read_text(encoding="utf-8"))
            unbound_value.pop("consumer_closure_receipt_ref")
            unbound_draft = temp / "unbound-draft.json"
            unbound_draft.write_text(json.dumps(unbound_value) + "\n", encoding="utf-8")
            unbound_output = temp / "unbound-output.json"
            with self.assertRaisesRegex(
                CLOSURE.ConsumerClosureError, "GUARDED_DRAFT_BINDING_MISSING"
            ):
                CLOSURE.write_guarded_artifact(
                    ROOT, r2_receipt, R2, unbound_draft, unbound_output
                )
            self.assertFalse(unbound_output.exists())

    def test_failing_report_produces_only_a_block_receipt(self) -> None:
        with tempfile.TemporaryDirectory(dir=SIDECAR / "evidence/tmp") as raw:
            temp = Path(raw)
            failing_report = copy.deepcopy(
                json.loads(R2["audit_report"].read_text(encoding="utf-8"))
            )
            failing_report["verdict"] = "block"
            failing_report["terminal_code"] = "SYNTHETIC_PREACCEPTANCE_BLOCK"
            report_path = temp / "failing-report.json"
            report_path.write_text(
                json.dumps(failing_report, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            failing_paths = dict(R2)
            failing_paths["audit_report"] = report_path
            receipt = CLOSURE.validate_consumer_closure(ROOT, failing_paths)
            self.assertEqual(receipt["status"], "block")
            self.assertIn(
                "IMPLEMENTATION_READINESS_INITIALIZE_REJECTED",
                {item["code"] for item in receipt["failures"]},
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
