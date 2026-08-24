from __future__ import annotations

import ast
import hashlib
import inspect
import os
import socket
import sys
import unittest
from pathlib import Path
from unittest import mock


STAGING_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(STAGING_ROOT))

from voice_production import fakes  # noqa: E402
from voice_production.compiler import compile_manifest  # noqa: E402
from voice_production.compiler_config import (  # noqa: E402
    compiler_config_from_json_bytes,
)
from voice_production.fakes import (  # noqa: E402
    CompositeContractError,
    FakeProjectAdapter,
    FakeSegmentAdapter,
    SegmentRetryDenied,
)


CSV_PATH = Path(
    "projects/lucifers-lights/drafts/graphic-novel/chapter-01/audio/"
    "elevenlabs-voiceover-studio.csv"
)
CONFIG_PATH = Path("projects/lucifers-lights/factory/voice/chapter-01.json")
PROJECT_REQUIREMENTS = [
    "composite-output",
    "project-reference",
    "correlation-honesty",
]


def source_path() -> Path:
    configured = os.environ.get("VPA_SOURCE_CSV")
    return Path(configured) if configured else REPOSITORY_ROOT / CSV_PATH


class SecretResolverSpy:
    def __init__(self) -> None:
        self.called = False

    def __call__(self, *_args, **_kwargs):
        self.called = True
        raise AssertionError("secret resolution is outside composite preparation")


class CompositePlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.compiler_config = compiler_config_from_json_bytes(
            (REPOSITORY_ROOT / CONFIG_PATH).read_bytes()
        )
        cls.manifest = compile_manifest(
            source_path().read_bytes(), config=cls.compiler_config
        ).as_envelope()
        cls.selected = ["segment-001", "segment-002", "segment-003"]
        cls.schema_sha = hashlib.sha256(b"synthetic-project-schema-v1").hexdigest()
        cls.binding = {
            "binding_ref": "synthetic-project-binding-A",
            "model_ref": "synthetic-project-model-A",
            "settings": {"mode": "project"},
        }

    def adapter(self) -> FakeProjectAdapter:
        return FakeProjectAdapter(
            adapter_id="fake-project",
            adapter_version="1.0.0",
            schema_locator="synthetic-schema://project/v1",
            schema_sha256=self.schema_sha,
        )

    def prepared(self, *, secret_resolver=None):
        adapter = self.adapter()
        query = adapter.query(
            self.manifest,
            selected_segment_ids=self.selected,
            required_capabilities=PROJECT_REQUIREMENTS,
            transport_mode="synthetic-project",
            binding_model_settings_descriptor=self.binding,
        )
        profile = adapter.evaluate(query)
        plan = adapter.prepare(
            self.manifest,
            query,
            profile,
            secret_resolver=secret_resolver,
        )
        return adapter, query, profile, plan

    def correlation_map(self, suffix: str = "A") -> dict[str, str]:
        return {
            segment_id: f"synthetic-marker-{index:03d}-{suffix}"
            for index, segment_id in enumerate(self.selected, start=1)
        }

    def test_segment_fake_behavior_is_preserved(self) -> None:
        adapter = FakeSegmentAdapter(
            adapter_id="fake-segment",
            adapter_version="1.0.0",
            schema_locator="synthetic-schema://segment/v1",
            schema_sha256=hashlib.sha256(b"segment-schema").hexdigest(),
        )
        query = adapter.query(
            self.manifest,
            selected_segment_ids=self.selected,
            required_capabilities=["correlated-segment-output"],
            transport_mode="synthetic-segment",
            binding_model_settings_descriptor={"binding": "segment-A"},
        )
        profile = adapter.evaluate(query)
        plan = adapter.prepare(self.manifest, query, profile)
        self.assertEqual(len(plan.value["expected_outputs"]), len(self.selected))
        self.assertTrue(
            all(
                item["output_granularity"] == "segment"
                for item in plan.value["expected_outputs"]
            )
        )

    def test_fixed_inputs_are_byte_stable(self) -> None:
        first = self.prepared()
        second = self.prepared()
        for left, right in zip(first[1:], second[1:], strict=True):
            self.assertEqual(left.canonical_envelope_bytes, right.canonical_envelope_bytes)
            self.assertEqual(left.digest, right.digest)
        projection_a = first[0].project(first[3])
        projection_b = second[0].project(second[3])
        self.assertEqual(projection_a.canonical_bytes_value, projection_b.canonical_bytes_value)
        self.assertEqual(projection_a.digest, projection_b.digest)

    def test_plan_and_projection_expose_one_composite_output(self) -> None:
        adapter, _query, profile, plan = self.prepared()
        outputs = plan.value["expected_outputs"]
        operations = plan.value["operations"]
        self.assertEqual(profile.value["output_granularity"], "composite")
        self.assertEqual(len(outputs), 1)
        self.assertEqual(len(operations), 1)
        self.assertEqual(outputs[0]["output_granularity"], "composite")
        self.assertEqual(operations[0]["expected_output_granularity"], "composite")
        self.assertEqual(outputs[0]["segment_ids"], self.selected)
        self.assertEqual(
            outputs[0]["composite_group_id"],
            operations[0]["composite_group_id"],
        )

        projection = adapter.project(plan)
        value = projection.value
        self.assertEqual(value["output_granularity"], "composite")
        self.assertEqual(len(value["artifacts"]), 1)
        self.assertFalse(value["artifacts"][0]["materialized"])
        self.assertTrue(value["native_project_ref"].startswith("synthetic-project:"))

    def test_segment_state_is_unknown_without_correlation(self) -> None:
        adapter, _query, _profile, plan = self.prepared()
        value = adapter.project(plan).value
        self.assertIsNone(value["correlation_map"])
        self.assertIsNone(value["correlation_map_digest"])
        self.assertEqual(value["correlation_method"], "none")
        self.assertEqual(value["correlation_confidence"], "unknown")
        self.assertTrue(
            all(item["state"] == "unknown" for item in value["segment_states"])
        )

    def test_validated_map_marks_correlation_without_claiming_completion(self) -> None:
        adapter, _query, _profile, plan = self.prepared()
        value = adapter.project(plan, correlation_map=self.correlation_map()).value
        self.assertEqual(value["correlation_method"], "explicit-synthetic-map")
        self.assertEqual(value["correlation_confidence"], "synthetic-derived")
        self.assertTrue(
            all(item["state"] == "correlated" for item in value["segment_states"])
        )
        self.assertNotIn("succeeded", str(value).casefold())
        self.assertNotIn("accepted", str(value).casefold())

    def test_incomplete_ambiguous_or_blank_correlation_is_rejected(self) -> None:
        adapter, _query, _profile, plan = self.prepared()
        invalid_maps = [
            {"segment-001": "marker-001"},
            {**self.correlation_map(), "segment-999": "marker-999"},
            {**self.correlation_map(), "segment-001": ""},
            {segment_id: "same-marker" for segment_id in self.selected},
        ]
        for value in invalid_maps:
            with self.subTest(value=value):
                with self.assertRaises(CompositeContractError):
                    adapter.project(plan, correlation_map=value)

    def test_correlation_mutation_rebinds_receipt_and_gate_inputs(self) -> None:
        adapter, _query, _profile, plan = self.prepared()
        map_a = self.correlation_map("A")
        map_b = self.correlation_map("A")
        map_b["segment-002"] = "synthetic-marker-002-B"
        projection_a = adapter.project(plan, correlation_map=map_a)
        projection_b = adapter.project(plan, correlation_map=map_b)
        self.assertNotEqual(projection_a.digest, projection_b.digest)
        self.assertNotEqual(
            projection_a.value["correlation_map_digest"],
            projection_b.value["correlation_map_digest"],
        )
        self.assertNotEqual(
            projection_a.value["receipt_input_digest"],
            projection_b.value["receipt_input_digest"],
        )
        self.assertNotEqual(
            projection_a.value["gate_input_digest"],
            projection_b.value["gate_input_digest"],
        )

    def test_segment_retry_is_denied_without_native_segment_evidence(self) -> None:
        adapter, _query, _profile, plan = self.prepared()
        for projection in [
            adapter.project(plan),
            adapter.project(plan, correlation_map=self.correlation_map()),
        ]:
            with self.subTest(correlation=projection.value["correlation_method"]):
                with self.assertRaisesRegex(SegmentRetryDenied, "no native"):
                    adapter.prepare_segment_retry(projection, ["segment-001"])

    def test_socket_dns_and_secret_helpers_are_denied_and_unused(self) -> None:
        spy = SecretResolverSpy()
        denied = AssertionError("network helper must not be used")
        with (
            mock.patch.object(socket, "socket", side_effect=denied),
            mock.patch.object(socket, "create_connection", side_effect=denied),
            mock.patch.object(socket, "getaddrinfo", side_effect=denied),
            mock.patch.object(socket, "gethostbyname", side_effect=denied),
        ):
            adapter, _query, _profile, plan = self.prepared(secret_resolver=spy)
            projection = adapter.project(plan, secret_resolver=spy)
        self.assertFalse(spy.called)
        self.assertEqual(plan.value["effect_estimates"]["external_effects"], 0)
        self.assertFalse(projection.value["artifacts"][0]["materialized"])

    def test_import_and_claim_surfaces_remain_bounded(self) -> None:
        tree = ast.parse(inspect.getsource(fakes))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imports.add(node.module.split(".", 1)[0])
        self.assertFalse(imports & {"http", "requests", "socket", "subprocess", "urllib"})
        source = inspect.getsource(fakes).casefold()
        for forbidden_claim in (
            "elevenlabs works",
            "studio is compatible",
            "provider success",
            "providers are replaceable",
        ):
            with self.subTest(forbidden_claim=forbidden_claim):
                self.assertNotIn(forbidden_claim, source)


if __name__ == "__main__":
    unittest.main()
