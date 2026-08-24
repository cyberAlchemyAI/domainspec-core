from __future__ import annotations

import hashlib
import sys
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock


STAGING_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(STAGING_ROOT))

import voice_workflow  # noqa: E402
from voice_production.canonical import (  # noqa: E402
    UnsupportedValueError,
    canonical_bytes,
)
from voice_production.compiler import (  # noqa: E402
    CsvProfileError,
    compile_manifest,
)
from voice_production.compiler_config import (  # noqa: E402
    compiler_config_from_json_bytes,
)


CSV_PATH = Path(
    "projects/lucifers-lights/drafts/graphic-novel/chapter-01/audio/"
    "elevenlabs-voiceover-studio.csv"
)
CONFIG_PATH = Path("projects/lucifers-lights/factory/voice/chapter-01.json")


def source_path() -> Path:
    return REPOSITORY_ROOT / CSV_PATH


class ToyGameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = source_path().read_bytes()
        cls.compiler_config = compiler_config_from_json_bytes(
            (REPOSITORY_ROOT / CONFIG_PATH).read_bytes()
        )
        cls.first = voice_workflow.run_workflow(
            cls.source, compiler_config=cls.compiler_config
        )
        cls.value = cls.first.value

    def test_fixed_inputs_are_byte_stable_and_fixture_is_exact(self) -> None:
        second = voice_workflow.run_workflow(
            self.source, compiler_config=self.compiler_config
        )
        self.assertEqual(
            self.first.canonical_bytes_value, second.canonical_bytes_value
        )
        self.assertEqual(self.first.digest, second.digest)
        source = self.value["source"]
        self.assertEqual(source["sha256"], self.compiler_config.expected_source_sha256)
        self.assertEqual(source["size_bytes"], len(self.source))
        self.assertEqual(source["segment_count"], 112)
        self.assertEqual(source["leading_tag_count"], 9)
        self.assertEqual(source["speakers"], sorted(self.compiler_config.allowed_speakers))
        self.assertEqual(source["order_and_text"], "exact-source-order")
        self.assertEqual(self.value["toy"]["segment_count"], 3)
        self.assertEqual(
            self.value["toy"]["selected_segment_ids"],
            list(voice_workflow.TOY_SEGMENT_IDS),
        )

    def test_separate_toy_artifact_is_bound_without_reopening_csv_profile(self) -> None:
        chapter = compile_manifest(
            self.source, config=self.compiler_config
        ).as_envelope()
        toy, toy_source = voice_workflow._toy_manifest(chapter)
        chapter_segments = chapter["value"]["segments"]
        toy_segments = toy["value"]["segments"]
        self.assertEqual(len(toy_segments), 3)
        self.assertEqual(
            [item["segment_id"] for item in toy_segments],
            list(voice_workflow.TOY_SEGMENT_IDS),
        )
        self.assertEqual(
            [item["exact_text"] for item in toy_segments],
            [item["exact_text"] for item in chapter_segments[:3]],
        )
        self.assertEqual(
            toy["value"]["source"]["sha256"], hashlib.sha256(toy_source).hexdigest()
        )
        self.assertNotEqual(toy["digest"], chapter["digest"])

        literal_three_row_csv = b"\n".join(self.source.splitlines()[:4]) + b"\n"
        with self.assertRaisesRegex(CsvProfileError, "expected 112 segments"):
            compile_manifest(
                literal_three_row_csv,
                config=replace(
                    self.compiler_config,
                    expected_source_sha256=hashlib.sha256(
                        literal_three_row_csv
                    ).hexdigest(),
                ),
            )

    def test_segment_outcomes_reconciliation_and_retry_are_honest(self) -> None:
        segment = self.value["segment"]
        self.assertEqual(segment["expected_output_count"], 3)
        self.assertEqual(
            segment["observed_outcomes"],
            ["accepted", "rejected-no-effect", "unknown"],
        )
        self.assertTrue(segment["unknown_retry_blocked_before_reconciliation"])
        self.assertEqual(segment["unknown_reconciled_to"], "no-effect")
        self.assertEqual(
            segment["retry_selected_segment_ids"],
            ["segment-002", "segment-003"],
        )
        self.assertEqual(
            segment["retry_excluded_operation_ids"], ["operation-001"]
        )
        self.assertTrue(segment["retry_authorization_rebound"])
        self.assertEqual(segment["provider_idempotency_support"], "unsupported")
        self.assertTrue(segment["projection_without_approval_blocked"])
        self.assertTrue(segment["unknown_capability_blocked"])

    def test_composite_output_preserves_unknown_state_and_denies_retry(self) -> None:
        project = self.value["project"]
        self.assertEqual(project["expected_output_count"], 1)
        self.assertEqual(project["output_granularity"], "composite")
        self.assertEqual(project["uncorrelated_segment_states"], ["unknown"] * 3)
        self.assertEqual(project["correlation_confidence"], "unknown")
        self.assertTrue(project["correlation_rebinds_receipt"])
        self.assertTrue(project["correlation_rebinds_gate"])
        self.assertTrue(project["segment_retry_denied"])
        self.assertEqual(project["materialized_artifact_count"], 0)

    def test_authorization_evidence_and_gate_negative_cases_are_proven(self) -> None:
        evidence = self.value["evidence"]
        self.assertEqual(
            evidence["authorization_rejections"],
            [
                "missing",
                "expired",
                "over-budget",
                "wrong-account",
                "wrong-scope",
                "stale-plan",
            ],
        )
        self.assertEqual(
            evidence["gate_mutation_rejections"],
            ["artifact", "authorization", "criterion", "evidence"],
        )
        self.assertTrue(evidence["non_unknown_claims_have_typed_evidence"])
        for field in (
            "authorization_digest",
            "normalized_receipt_digest",
            "gate_receipt_digest",
        ):
            self.assertRegex(evidence[field], r"^[0-9a-f]{64}$")

    def test_every_declared_digest_binding_changes(self) -> None:
        expected = {
            "adapter_version",
            "binding_descriptor",
            "estimate",
            "expected_output",
            "model_descriptor",
            "policy",
            "projected_payload",
            "schema_basis",
            "selection",
            "source_bytes",
            "text",
            "transformation",
            "transport_mode",
        }
        self.assertEqual(set(self.value["binding_proofs"]), expected)
        self.assertTrue(all(self.value["binding_proofs"].values()))

    def test_redacted_summary_and_claim_ceiling(self) -> None:
        text = self.first.text()
        self.assertEqual(
            self.value["claim_ceiling"], voice_workflow.CLAIM_CEILING
        )
        forbidden_values = (
            "synthetic-account-A",
            "native_project_ref",
            "native_effect_ref",
            "projected_text",
            "Presentation is everything",
            "credential-value",
        )
        for forbidden in forbidden_values:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)
        for forbidden_claim in (
            "provider works",
            "studio is compatible",
            "account is authorized",
            "cost is acceptable",
            "voice quality passed",
            "providers are replaceable",
        ):
            with self.subTest(forbidden_claim=forbidden_claim):
                self.assertNotIn(forbidden_claim, text.casefold())

    def test_provider_neutral_adapter_bundle_is_injected(self) -> None:
        defaults = voice_workflow.default_adapters()
        segment = mock.Mock(wraps=defaults.segment)
        project = mock.Mock(wraps=defaults.project)
        result = voice_workflow.run_workflow(
            self.source,
            compiler_config=self.compiler_config,
            adapters=voice_workflow.AdapterBundle(
                segment=segment,
                project=project,
            ),
        )
        self.assertEqual(result.value["claim_ceiling"], voice_workflow.CLAIM_CEILING)
        self.assertGreaterEqual(segment.query.call_count, 4)
        self.assertGreaterEqual(segment.evaluate.call_count, 4)
        self.assertGreaterEqual(segment.prepare.call_count, 4)
        project.query.assert_called()
        project.evaluate.assert_called()
        project.prepare.assert_called()
        project.project.assert_called()

    def test_provider_shaped_csv_and_untyped_options_fail_closed(self) -> None:
        altered = self.source.replace(
            b"speaker,line\n", b"speaker,line,voice_id\n", 1
        )
        with self.assertRaises(CsvProfileError):
            compile_manifest(
                altered,
                config=replace(
                    self.compiler_config,
                    expected_source_sha256=hashlib.sha256(altered).hexdigest(),
                ),
            )
        with self.assertRaises(UnsupportedValueError):
            canonical_bytes({"provider_options": object()})


if __name__ == "__main__":
    unittest.main()
