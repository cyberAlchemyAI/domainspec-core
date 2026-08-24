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

from voice_production import fakes, port  # noqa: E402
from voice_production.compiler import compile_manifest  # noqa: E402
from voice_production.fakes import FakeSegmentAdapter  # noqa: E402
from voice_production.port import (  # noqa: E402
    MandatoryCapabilityBlocked,
    PortContractError,
    ProjectionApprovalRequired,
    evaluate_capabilities,
)


CSV_PATH = Path(
    "projects/lucifers-lights/drafts/graphic-novel/chapter-01/audio/"
    "elevenlabs-voiceover-studio.csv"
)
REQUIREMENTS = [
    "correlated-segment-output",
    "exact-text-ledger",
    "static-effect-estimate",
    "transformation-ledger",
]


def source_path() -> Path:
    configured = os.environ.get("VPA_SOURCE_CSV")
    return Path(configured) if configured else REPOSITORY_ROOT / CSV_PATH


class SecretResolverSpy:
    def __init__(self) -> None:
        self.called = False

    def __call__(self, *_args, **_kwargs):
        self.called = True
        raise AssertionError("secret resolver must not be called during preparation")


class SegmentPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = compile_manifest(source_path().read_bytes()).as_envelope()
        cls.selected = ["segment-001", "segment-002", "segment-003"]
        cls.binding = {
            "binding_ref": "synthetic-binding-A",
            "model_ref": "synthetic-model-A",
            "settings": {"pace": "neutral"},
        }
        cls.schema_sha = hashlib.sha256(
            b"synthetic-segment-schema-v1"
        ).hexdigest()

    def adapter(self, **changes) -> FakeSegmentAdapter:
        values = {
            "adapter_id": "fake-segment",
            "adapter_version": "1.0.0",
            "schema_locator": "synthetic-schema://segment/v1",
            "schema_sha256": self.schema_sha,
        }
        values.update(changes)
        return FakeSegmentAdapter(**values)

    def prepared(self, **plan_changes):
        adapter = self.adapter()
        query = adapter.query(
            self.manifest,
            selected_segment_ids=self.selected,
            required_capabilities=REQUIREMENTS,
            transport_mode="synthetic-segment",
            binding_model_settings_descriptor=self.binding,
        )
        profile = adapter.evaluate(query)
        plan = adapter.prepare(
            self.manifest,
            query,
            profile,
            **plan_changes,
        )
        return adapter, query, profile, plan

    def test_fixed_inputs_produce_byte_stable_query_profile_and_plan(self) -> None:
        first = self.prepared()
        second = self.prepared()
        for left, right in zip(first[1:], second[1:], strict=True):
            self.assertEqual(
                left.canonical_envelope_bytes,
                right.canonical_envelope_bytes,
            )
            self.assertEqual(left.digest, right.digest)

    def test_query_rebinds_on_selection_binding_mode_adapter_and_schema(self) -> None:
        base_adapter = self.adapter()

        def digest(
            *,
            adapter=None,
            selected=None,
            binding=None,
            mode="synthetic-segment",
        ):
            current = adapter or base_adapter
            return current.query(
                self.manifest,
                selected_segment_ids=selected or self.selected,
                required_capabilities=REQUIREMENTS,
                transport_mode=mode,
                binding_model_settings_descriptor=binding or self.binding,
            ).digest

        digests = {
            digest(),
            digest(selected=["segment-001", "segment-004"]),
            digest(binding={**self.binding, "model_ref": "synthetic-model-B"}),
            digest(mode="synthetic-batch"),
            digest(adapter=self.adapter(adapter_version="1.0.1")),
            digest(
                adapter=self.adapter(
                    schema_sha256=hashlib.sha256(b"schema-v2").hexdigest()
                )
            ),
        }
        self.assertEqual(len(digests), 6)

    def test_profile_binds_query_and_static_evidence_without_live_claims(self) -> None:
        _adapter, query, profile, _plan = self.prepared()
        value = profile.value
        self.assertEqual(value["query_digest"], query.digest)
        self.assertEqual(value["output_granularity"], "segment")
        self.assertTrue(
            all(item["status"] == "supported" for item in value["decisions"])
        )
        self.assertFalse(value["evidence_basis"][0]["live_account_evidence"])

    def test_status_surface_is_closed_and_mandatory_unknown_blocks(self) -> None:
        adapter = self.adapter()
        query = adapter.query(
            self.manifest,
            selected_segment_ids=self.selected,
            required_capabilities=["live-account-evidence"],
            transport_mode="synthetic-segment",
            binding_model_settings_descriptor=self.binding,
        )
        profile = adapter.evaluate(query)
        self.assertEqual(profile.value["decisions"][0]["status"], "unknown")
        with self.assertRaisesRegex(MandatoryCapabilityBlocked, "unknown"):
            adapter.prepare(self.manifest, query, profile)

        with self.assertRaisesRegex(PortContractError, "exactly cover"):
            evaluate_capabilities(
                query.as_envelope(),
                statuses={},
                evidence_basis=[],
            )

    def test_exact_and_projected_text_are_separate_and_approval_bound(self) -> None:
        exact = self.manifest["value"]["segments"][0]["exact_text"]
        projected = exact.split("] ", 1)[1]
        with self.assertRaises(ProjectionApprovalRequired):
            self.prepared(projected_text_by_segment={"segment-001": projected})

        _adapter, _query, _profile, plan = self.prepared(
            projected_text_by_segment={"segment-001": projected},
            transformation_approval_ref="projection-approval-001",
        )
        record = plan.value["transformations"][0]
        self.assertEqual(record["exact_text"], exact)
        self.assertEqual(record["projected_text"], projected)
        self.assertNotEqual(
            record["exact_text_sha256"], record["projected_text_sha256"]
        )
        self.assertEqual(record["approval_ref"], "projection-approval-001")
        self.assertEqual(len(record["transformations"]), 1)
        self.assertEqual(
            self.manifest["value"]["segments"][0]["exact_text"], exact
        )

    def test_effect_bearing_plan_fields_rebind_digest(self) -> None:
        base = self.prepared()[3]
        projected = self.manifest["value"]["segments"][0]["exact_text"].upper()
        transformed_a = self.prepared(
            projected_text_by_segment={"segment-001": projected},
            transformation_approval_ref="approval-A",
        )[3]
        transformed_b = self.prepared(
            projected_text_by_segment={"segment-001": projected},
            transformation_approval_ref="approval-B",
        )[3]
        output_changed = self.prepared(
            output_descriptor="synthetic-segment-artifact/v2"
        )[3]
        self.assertEqual(
            len({base.digest, transformed_a.digest, transformed_b.digest, output_changed.digest}),
            4,
        )

    def test_segment_fake_projects_one_certain_output_per_selected_segment(self) -> None:
        _adapter, _query, _profile, plan = self.prepared()
        outputs = plan.value["expected_outputs"]
        operations = plan.value["operations"]
        self.assertEqual(len(outputs), len(self.selected))
        self.assertEqual(len(operations), len(self.selected))
        self.assertEqual(
            [item["segment_id"] for item in outputs],
            self.selected,
        )
        self.assertTrue(
            all(item["output_granularity"] == "segment" for item in outputs)
        )
        self.assertTrue(
            all(item["correlation_confidence"] == "certain" for item in outputs)
        )

    def test_socket_dns_and_secret_access_are_denied_and_unused(self) -> None:
        spy = SecretResolverSpy()
        denied = AssertionError("network helper must not be used")
        with (
            mock.patch.object(socket, "socket", side_effect=denied),
            mock.patch.object(socket, "create_connection", side_effect=denied),
            mock.patch.object(socket, "getaddrinfo", side_effect=denied),
        ):
            _adapter, _query, _profile, plan = self.prepared(
                secret_resolver=spy
            )
        self.assertFalse(spy.called)
        self.assertEqual(plan.value["effect_estimates"]["external_effects"], 0)

    def test_stale_query_or_profile_is_rejected(self) -> None:
        adapter = self.adapter()
        query_a = adapter.query(
            self.manifest,
            selected_segment_ids=self.selected,
            required_capabilities=REQUIREMENTS,
            transport_mode="synthetic-segment",
            binding_model_settings_descriptor=self.binding,
        )
        query_b = adapter.query(
            self.manifest,
            selected_segment_ids=["segment-001"],
            required_capabilities=REQUIREMENTS,
            transport_mode="synthetic-segment",
            binding_model_settings_descriptor=self.binding,
        )
        profile_a = adapter.evaluate(query_a)
        with self.assertRaisesRegex(PortContractError, "stale for the query"):
            adapter.prepare(self.manifest, query_b, profile_a)

    def test_import_surface_has_no_effectful_runtime_modules(self) -> None:
        forbidden = {"http", "requests", "socket", "subprocess", "urllib"}
        for module in (port, fakes):
            tree = ast.parse(inspect.getsource(module))
            imports: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    imports.add(node.module.split(".", 1)[0])
            self.assertFalse(imports & forbidden)


if __name__ == "__main__":
    unittest.main()
