from __future__ import annotations

import ast
import hashlib
import inspect
import socket
import sys
import unittest
from pathlib import Path
from unittest import mock


CANDIDATE_ROOT = Path(__file__).resolve().parents[1]
VOICE_PRODUCTION_ROOT = (
    Path.cwd() / "drafts/graphic-novel/tools/voice-production"
)
sys.path[:0] = [str(CANDIDATE_ROOT), str(VOICE_PRODUCTION_ROOT)]

from voice_production.canonical import (  # noqa: E402
    canonical_bytes,
)
from voice_production.compiler import compile_manifest  # noqa: E402
from voice_production import elevenlabs_static_projection as projector  # noqa: E402


CSV_PATH = Path(
    "drafts/graphic-novel/chapter-01/audio/elevenlabs-voiceover-studio.csv"
)
SCHEMA_PATH = (
    CANDIDATE_ROOT / "voice_production/elevenlabs_direct_tts_schema.json"
)
SELECTED_SEGMENTS = ["segment-001", "segment-046", "segment-101"]


class SecretResolverSpy:
    def __init__(self) -> None:
        self.called = False

    def __call__(self, *_args, **_kwargs):
        self.called = True
        raise AssertionError("secret resolver must not be called by static L1")


class ElevenLabsStaticProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_bytes = (Path.cwd() / CSV_PATH).read_bytes()
        cls.manifest_artifact = compile_manifest(cls.source_bytes)
        cls.manifest = cls.manifest_artifact.as_envelope()
        cls.manifest_bytes = cls.manifest_artifact.canonical_envelope_bytes
        cls.schema_bytes = SCHEMA_PATH.read_bytes()
        selected = {
            item["segment_id"]: item
            for item in cls.manifest["value"]["segments"]
            if item["segment_id"] in SELECTED_SEGMENTS
        }
        cls.selected_texts = [selected[item]["exact_text"] for item in SELECTED_SEGMENTS]
        cls.bindings = {
            speaker: f"fixture-slot-{speaker.lower()}"
            for speaker in sorted(
                {selected[item]["speaker"] for item in SELECTED_SEGMENTS}
            )
        }

    def project(self, *, schema_bytes: bytes | None = None):
        return projector.project_direct_tts_static(
            self.manifest,
            selected_segment_ids=SELECTED_SEGMENTS,
            schema_basis_bytes=schema_bytes or self.schema_bytes,
            voice_binding_refs=self.bindings,
        )

    def test_schema_is_pinned_and_projection_is_byte_stable_redacted(self) -> None:
        basis = projector.load_pinned_schema_basis(self.schema_bytes)
        self.assertEqual(
            canonical_bytes(basis) + b"\n",
            self.schema_bytes,
        )

        first = self.project()
        second = self.project()
        self.assertEqual(first.query.canonical_envelope_bytes, second.query.canonical_envelope_bytes)
        self.assertEqual(first.profile.canonical_envelope_bytes, second.profile.canonical_envelope_bytes)
        self.assertEqual(first.plan.canonical_envelope_bytes, second.plan.canonical_envelope_bytes)
        self.assertEqual(
            first.l2_prerequisite_query.canonical_envelope_bytes,
            second.l2_prerequisite_query.canonical_envelope_bytes,
        )
        self.assertEqual(
            first.l2_prerequisite_profile.canonical_envelope_bytes,
            second.l2_prerequisite_profile.canonical_envelope_bytes,
        )
        self.assertEqual(first.redacted_snapshot_bytes, second.redacted_snapshot_bytes)

        snapshots = first.redacted_snapshots
        rendered = first.redacted_snapshot_bytes.decode("utf-8")
        self.assertEqual([item["segment_id"] for item in snapshots], SELECTED_SEGMENTS)
        self.assertTrue(
            all(item["body_field_names"] == ["text"] for item in snapshots)
        )
        self.assertTrue(
            all(item["path_template"] == "/v1/text-to-speech/{voice_id}" for item in snapshots)
        )
        self.assertTrue(all(item["method"] == "POST" for item in snapshots))
        for exact_text in self.selected_texts:
            self.assertNotIn(exact_text, rendered)
        for binding in self.bindings.values():
            self.assertNotIn(binding, rendered)

        self.assertEqual(
            first.profile.value["decisions"],
            [
                {
                    "evidence_links": ["evidence-basis-001"],
                    "requirement_ref": projector.STATIC_REQUEST_CAPABILITY,
                    "status": "supported",
                }
            ],
        )
        self.assertEqual(first.plan.value["effect_estimates"]["external_effects"], 0)
        self.assertEqual(
            first.l2_unknown_requirements,
            projector.L2_UNKNOWN_REQUIREMENTS,
        )
        unknown_decisions = first.l2_prerequisite_profile.value["decisions"]
        self.assertEqual(
            {item["requirement_ref"] for item in unknown_decisions},
            set(projector.L2_UNKNOWN_REQUIREMENTS),
        )
        self.assertTrue(all(item["status"] == "unknown" for item in unknown_decisions))

    def test_schema_bytes_rebind_all_digest_bound_static_artifacts(self) -> None:
        baseline = self.project()
        changed_basis = projector.load_pinned_schema_basis(self.schema_bytes)
        changed_basis["source"]["retrieved_on"] = "2026-08-11"
        changed_bytes = canonical_bytes(changed_basis)
        changed = self.project(schema_bytes=changed_bytes)

        self.assertNotEqual(baseline.schema_sha256, changed.schema_sha256)
        self.assertNotEqual(baseline.query.digest, changed.query.digest)
        self.assertNotEqual(baseline.profile.digest, changed.profile.digest)
        self.assertNotEqual(baseline.plan.digest, changed.plan.digest)
        self.assertNotEqual(
            baseline.l2_prerequisite_query.digest,
            changed.l2_prerequisite_query.digest,
        )
        self.assertNotEqual(
            baseline.l2_prerequisite_profile.digest,
            changed.l2_prerequisite_profile.digest,
        )
        self.assertNotEqual(
            baseline.redacted_snapshot_bytes,
            changed.redacted_snapshot_bytes,
        )

    def test_projection_preserves_canonical_manifest_bytes_and_core_boundary(self) -> None:
        self.project()
        self.assertEqual(
            self.manifest_artifact.canonical_envelope_bytes,
            self.manifest_bytes,
        )
        self.assertNotIn(b"voice_binding_ref", self.manifest_bytes)
        self.assertNotIn(b"path_template", self.manifest_bytes)
        self.assertNotIn(b"direct-tts-static", self.manifest_bytes)

    def test_network_dns_and_secret_resolution_are_not_used(self) -> None:
        spy = SecretResolverSpy()
        denied = AssertionError("network or DNS crossed the static L1 boundary")
        with (
            mock.patch.object(socket, "socket", side_effect=denied),
            mock.patch.object(socket, "create_connection", side_effect=denied),
            mock.patch.object(socket, "getaddrinfo", side_effect=denied),
            mock.patch.object(socket, "gethostbyname", side_effect=denied),
        ):
            result = projector.project_direct_tts_static(
                self.manifest,
                selected_segment_ids=SELECTED_SEGMENTS,
                schema_basis_bytes=self.schema_bytes,
                voice_binding_refs=self.bindings,
                secret_resolver=spy,
            )
        self.assertFalse(spy.called)
        self.assertEqual(result.plan.value["effect_estimates"]["external_effects"], 0)

    def test_binding_coverage_and_schema_shape_fail_closed(self) -> None:
        with self.assertRaisesRegex(projector.StaticProjectionError, "exactly"):
            projector.project_direct_tts_static(
                self.manifest,
                selected_segment_ids=SELECTED_SEGMENTS,
                schema_basis_bytes=self.schema_bytes,
                voice_binding_refs={next(iter(self.bindings)): "fixture-slot-only"},
            )

        with self.assertRaisesRegex(projector.StaticProjectionError, "valid UTF-8 JSON"):
            projector.load_pinned_schema_basis(self.schema_bytes + b"{")

        invalid_basis = projector.load_pinned_schema_basis(self.schema_bytes)
        invalid_basis["request"]["body"]["required_fields"] = ["text", "voice_id"]
        with self.assertRaisesRegex(projector.StaticProjectionError, "exactly text"):
            projector.load_pinned_schema_basis(canonical_bytes(invalid_basis))

    def test_import_surface_excludes_effectful_modules(self) -> None:
        tree = ast.parse(inspect.getsource(projector))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imports.add(node.module.split(".", 1)[0])
        self.assertFalse(
            imports & {"http", "requests", "socket", "subprocess", "urllib"}
        )
        source = inspect.getsource(projector).casefold()
        self.assertNotIn("environ[", source)
        self.assertNotIn("getenv(", source)

    def test_native_request_digest_binds_text_and_opaque_binding_without_disclosure(self) -> None:
        baseline = self.project()
        changed_bindings = dict(self.bindings)
        first_speaker = sorted(changed_bindings)[0]
        changed_bindings[first_speaker] = "fixture-slot-changed"
        changed = projector.project_direct_tts_static(
            self.manifest,
            selected_segment_ids=SELECTED_SEGMENTS,
            schema_basis_bytes=self.schema_bytes,
            voice_binding_refs=changed_bindings,
        )
        self.assertNotEqual(baseline.query.digest, changed.query.digest)
        self.assertNotEqual(baseline.plan.digest, changed.plan.digest)
        self.assertNotEqual(
            baseline.redacted_snapshot_bytes,
            changed.redacted_snapshot_bytes,
        )
        self.assertNotIn(
            hashlib.sha256(b"fixture-slot-changed").hexdigest().encode("utf-8"),
            self.manifest_bytes,
        )


if __name__ == "__main__":
    unittest.main()
