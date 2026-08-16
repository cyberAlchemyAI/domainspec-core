from __future__ import annotations

import copy
import hashlib
import math
import sys
import unittest
from pathlib import Path
from typing import Any, Iterator


STAGING_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STAGING_ROOT))

from voice_production.canonical import (  # noqa: E402
    CANONICALIZATION_PROFILE,
    CanonicalizationError,
    EnvelopeError,
    NonCanonicalEncodingError,
    UnsupportedValueError,
    canonical_bytes,
    canonical_loads,
    compute_envelope_digest,
    make_envelope,
    require_valid_envelope,
    verify_envelope,
)
from voice_production.contracts import (  # noqa: E402
    CAPABILITY_PROFILE_SCHEMA_ID,
    CAPABILITY_QUERY_SCHEMA_ID,
    GATE_RECEIPT_SCHEMA_ID,
    MANIFEST_SCHEMA_ID,
    NORMALIZED_RECEIPT_SCHEMA_ID,
    PLAN_SCHEMA_ID,
    capability_profile_envelope,
    capability_query_envelope,
    gate_receipt_envelope,
    manifest_envelope,
    normalized_receipt_envelope,
    plan_envelope,
)


SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
SHA_D = "d" * 64
SHA_E = "e" * 64
SHA_F = "f" * 64


def leaf_paths(value: Any, path: tuple[Any, ...] = ()) -> Iterator[tuple[Any, ...]]:
    if type(value) is dict:
        for key in sorted(value):
            yield from leaf_paths(value[key], (*path, key))
        return
    if type(value) is list:
        for index, item in enumerate(value):
            yield from leaf_paths(item, (*path, index))
        return
    yield path


def replace_leaf(value: Any, path: tuple[Any, ...]) -> None:
    parent = value
    for part in path[:-1]:
        parent = parent[part]
    old = parent[path[-1]]
    if old is None:
        new = "observed"
    elif type(old) is bool:
        new = not old
    elif type(old) is int:
        new = old + 1
    elif type(old) is float:
        new = old + 0.5
    elif type(old) is str:
        new = f"{old}!"
    else:  # pragma: no cover - leaf_paths emits only scalar leaves
        raise AssertionError(type(old))
    parent[path[-1]] = new


class CanonicalJsonTests(unittest.TestCase):
    def test_profile_is_deterministic_compact_utf8_and_preserves_arrays(self) -> None:
        value = {"z": "á", "a": {"β": 2, "a": 1}, "array": [2, 1]}
        expected = '{"a":{"a":1,"β":2},"array":[2,1],"z":"á"}'.encode()
        self.assertEqual(canonical_bytes(value), expected)
        self.assertEqual(canonical_bytes(copy.deepcopy(value)), expected)
        self.assertEqual(canonical_loads(expected), value)

    def test_noncanonical_bytes_are_rejected(self) -> None:
        payloads = [
            b'{"b":1,"a":2}',
            b'{"a": 1}',
            b'{"a":1,"a":2}',
            b'{"a":NaN}',
            b'\xff',
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(NonCanonicalEncodingError):
                    canonical_loads(payload)
        with self.assertRaises(UnsupportedValueError):
            canonical_loads("{}")  # type: ignore[arg-type]

    def test_nonfinite_and_unsupported_runtime_values_are_rejected(self) -> None:
        values = [
            math.nan,
            math.inf,
            -math.inf,
            (1, 2),
            {1: "not-a-string-key"},
            b"bytes",
            {"set"},
            "\ud800",
        ]
        for value in values:
            with self.subTest(value=repr(value)):
                with self.assertRaises(CanonicalizationError):
                    canonical_bytes(value)  # type: ignore[arg-type]

        cycle: list[Any] = []
        cycle.append(cycle)
        with self.assertRaises(UnsupportedValueError):
            canonical_bytes(cycle)


class EnvelopeTests(unittest.TestCase):
    def test_digest_excludes_only_its_own_top_level_field(self) -> None:
        envelope = make_envelope(
            "voice-production.test",
            {"nested": {"digest": SHA_A}, "ordered": ["one", "two"]},
        )
        covered = dict(envelope)
        del covered["digest"]
        expected = hashlib.sha256(canonical_bytes(covered)).hexdigest()
        self.assertEqual(envelope["digest"], expected)
        self.assertEqual(compute_envelope_digest(envelope), expected)
        self.assertTrue(verify_envelope(envelope))

        outer_digest_changed = copy.deepcopy(envelope)
        outer_digest_changed["digest"] = SHA_B
        self.assertEqual(compute_envelope_digest(outer_digest_changed), expected)
        self.assertFalse(verify_envelope(outer_digest_changed))

        nested_digest_changed = copy.deepcopy(envelope)
        nested_digest_changed["value"]["nested"]["digest"] = SHA_B
        self.assertNotEqual(compute_envelope_digest(nested_digest_changed), expected)

    def test_shape_profile_and_algorithm_fail_closed(self) -> None:
        envelope = make_envelope("voice-production.test", {"value": 1})
        mutations = [
            ("canonicalization_profile", "unknown/v1"),
            ("digest_algorithm", "sha512"),
            ("schema_id", ""),
            ("digest", "ABC"),
        ]
        for key, value in mutations:
            mutant = copy.deepcopy(envelope)
            mutant[key] = value
            with self.subTest(key=key):
                with self.assertRaises(EnvelopeError):
                    require_valid_envelope(mutant)

        extra = copy.deepcopy(envelope)
        extra["unexpected"] = True
        with self.assertRaises(EnvelopeError):
            require_valid_envelope(extra)


class ProviderNeutralContractTests(unittest.TestCase):
    def setUp(self) -> None:
        source = {
            "locator": "fixture://chapter-01.csv",
            "sha256": SHA_A,
            "media_type": "text/csv",
        }
        self.manifest = manifest_envelope(
            production_id="chapter-01-synthetic",
            source=source,
            segments=[
                {
                    "segment_id": "segment-001",
                    "speaker": "narrator",
                    "exact_text": "Synthetic line.",
                    "exact_text_sha256": SHA_B,
                }
            ],
            output_policy={"granularity": "composite", "format": "synthetic"},
            acceptance_policy={"transformations_require_approval": True},
        )
        self.query = capability_query_envelope(
            manifest_digest=self.manifest["digest"],
            selected_segment_ids=["segment-001", "segment-002"],
            content_characteristics_digest=SHA_C,
            required_capabilities=["text-input", "composite-output"],
            transport_mode="local-synthetic",
            adapter={"id": "synthetic-local", "version": "1"},
            provider_schema_basis={
                "locator": "fixture://native-schema",
                "sha256": SHA_D,
                "observed_at": "2026-08-09T00:00:00Z",
            },
            binding_model_settings_descriptor_digest=SHA_E,
        )
        self.profile = capability_profile_envelope(
            query_digest=self.query["digest"],
            decisions=[
                {
                    "requirement_ref": "text-input",
                    "status": "supported",
                    "evidence_links": ["evidence-001"],
                },
                {
                    "requirement_ref": "composite-output",
                    "status": "translated",
                    "evidence_links": ["evidence-002"],
                },
            ],
            output_granularity="composite",
            retry_granularity="composite",
            idempotency_support="submission-key",
            cancellation_support="unknown",
            evidence_basis=[{"evidence_id": "basis-001", "sha256": SHA_F}],
        )
        self.plan = plan_envelope(
            manifest_digest=self.manifest["digest"],
            capability_profile_digest=self.profile["digest"],
            selected_segment_ids=["segment-001", "segment-002"],
            operations=[
                {
                    "operation_id": "operation-001",
                    "operation_fingerprint": SHA_A,
                    "submission_key": "submission-001",
                    "selected_segment_ids": ["segment-001", "segment-002"],
                    "projected_payload_sha256": SHA_B,
                    "expected_output_granularity": "composite",
                    "composite_group_id": "group-001",
                }
            ],
            expected_outputs=[
                {
                    "output_id": "output-001",
                    "granularity": "composite",
                    "segment_ids": ["segment-001", "segment-002"],
                }
            ],
            effect_estimates={"operation_count": 1, "external_effects": False},
            warnings=["synthetic-only"],
            blocked_requirements=["live-submission"],
            transformations=[
                {
                    "segment_id": "segment-001",
                    "exact_text_sha256": SHA_C,
                    "projected_text_sha256": SHA_D,
                    "transformations": [{"kind": "none", "ordinal": 0}],
                    "approval_ref": "approval-001",
                }
            ],
            native_schema_basis={"locator": "fixture://plan-schema", "sha256": SHA_E},
        )
        self.receipt = normalized_receipt_envelope(
            manifest_digest=self.manifest["digest"],
            capability_profile_digest=self.profile["digest"],
            plan_digest=self.plan["digest"],
            execution_authorization_digest=SHA_F,
            run_id="synthetic-run-001",
            parent_run_id="synthetic-parent-001",
            output_granularity="composite",
            composite_groups=[{"group_id": "group-001", "status": "observed"}],
            claims=[
                {
                    "claim_id": "claim-001",
                    "subject_ref": "artifact-001",
                    "predicate": "exists",
                    "value": True,
                    "evidence_link_ids": ["evidence-001"],
                    "confidence": "observed",
                }
            ],
            evidence_links=[
                {
                    "claim_id": "claim-001",
                    "claim_type": "artifact-existence",
                    "native_locator": "fixture://artifact-001",
                    "native_sha256": SHA_A,
                    "observed_at": "2026-08-09T00:00:00Z",
                    "classification": "synthetic",
                    "redaction_profile": "no-secrets/v1",
                }
            ],
            artifacts=[{"artifact_id": "artifact-001", "sha256": SHA_A}],
            reconciliation_state={"status": "known", "attempt": 1},
        )
        self.gate = gate_receipt_envelope(
            synthesis_receipt_digest=self.receipt["digest"],
            reviewed_artifact_sha256s=[SHA_A, SHA_B],
            criteria_results=[{"criterion": "synthetic", "passed": True}],
            review_scope="local-synthetic-seam",
            reviewer="fixture-reviewer",
            decision="accepted",
            decided_at="2026-08-09T00:00:01Z",
            exceptions=[{"kind": "no-live-provider-proof", "accepted": False}],
        )

    def envelopes(self) -> list[dict[str, Any]]:
        return [
            self.manifest,
            self.query,
            self.profile,
            self.plan,
            self.receipt,
            self.gate,
        ]

    def test_all_contract_kinds_are_versioned_and_verify(self) -> None:
        expected_ids = [
            MANIFEST_SCHEMA_ID,
            CAPABILITY_QUERY_SCHEMA_ID,
            CAPABILITY_PROFILE_SCHEMA_ID,
            PLAN_SCHEMA_ID,
            NORMALIZED_RECEIPT_SCHEMA_ID,
            GATE_RECEIPT_SCHEMA_ID,
        ]
        for envelope, schema_id in zip(self.envelopes(), expected_ids, strict=True):
            with self.subTest(schema_id=schema_id):
                self.assertEqual(envelope["schema_id"], schema_id)
                self.assertEqual(
                    envelope["canonicalization_profile"], CANONICALIZATION_PROFILE
                )
                self.assertEqual(envelope["schema_version"], "1")
                self.assertTrue(verify_envelope(envelope))
                self.assertEqual(canonical_bytes(envelope), canonical_bytes(envelope))

    def test_every_representative_covered_leaf_changes_its_digest(self) -> None:
        for envelope in self.envelopes():
            original_digest = envelope["digest"]
            for path in leaf_paths(envelope):
                if path == ("digest",):
                    continue
                mutant = copy.deepcopy(envelope)
                replace_leaf(mutant, path)
                with self.subTest(schema=envelope["schema_id"], path=path):
                    self.assertNotEqual(
                        compute_envelope_digest(mutant), original_digest
                    )

    def test_values_are_detached_and_provider_specific_escape_hatches_are_absent(self) -> None:
        source = {"locator": "fixture://source", "sha256": SHA_A}
        envelope = manifest_envelope(
            production_id="detachment-fixture",
            source=source,
            segments=[{"segment_id": "segment-001"}],
            output_policy={"granularity": "composite"},
            acceptance_policy={"approval": "required"},
        )
        source["locator"] = "mutated-after-build"
        self.assertEqual(envelope["value"]["source"]["locator"], "fixture://source")

        forbidden_keys = {"provider_options", "voice_id", "model_id", "api_key"}
        forbidden_values = {"elevenlabs"}
        for contract in self.envelopes():
            for path in leaf_paths(contract):
                self.assertFalse(any(part in forbidden_keys for part in path))
                parent = contract
                for part in path:
                    parent = parent[part]
                if type(parent) is str:
                    self.assertNotIn(parent.casefold(), forbidden_values)

    def test_production_id_and_expected_outputs_are_digest_covered(self) -> None:
        manifest_mutant = copy.deepcopy(self.manifest)
        manifest_mutant["value"]["production_id"] = "chapter-01-mutated"
        self.assertNotEqual(
            compute_envelope_digest(manifest_mutant), self.manifest["digest"]
        )

        plan_mutant = copy.deepcopy(self.plan)
        plan_mutant["value"]["expected_outputs"][0]["output_id"] = "output-mutated"
        self.assertNotEqual(compute_envelope_digest(plan_mutant), self.plan["digest"])

    def test_invalid_contract_bindings_fail_before_digesting(self) -> None:
        with self.assertRaises(ValueError):
            capability_query_envelope(
                manifest_digest="not-a-digest",
                selected_segment_ids=["segment-001"],
                content_characteristics_digest=SHA_A,
                required_capabilities=["text-input"],
                transport_mode="local",
                adapter={"id": "synthetic", "version": "1"},
                provider_schema_basis={"locator": "fixture://schema"},
                binding_model_settings_descriptor_digest=SHA_B,
            )
        with self.assertRaises(ValueError):
            capability_profile_envelope(
                query_digest=SHA_A,
                decisions=[
                    {
                        "requirement_ref": "text-input",
                        "status": "assumed",
                        "evidence_links": ["evidence-001"],
                    }
                ],
                output_granularity="composite",
                retry_granularity="composite",
                idempotency_support="unknown",
                cancellation_support="unknown",
                evidence_basis=[{"evidence_id": "basis-001"}],
            )
        with self.assertRaises(ValueError):
            gate_receipt_envelope(
                synthesis_receipt_digest=SHA_A,
                reviewed_artifact_sha256s=[SHA_B],
                criteria_results=[{"criterion": "synthetic", "passed": True}],
                review_scope="local",
                reviewer="fixture-reviewer",
                decision="auto-approved",
                decided_at="2026-08-09T00:00:00Z",
                exceptions=[{"kind": "none"}],
            )


if __name__ == "__main__":
    unittest.main()
