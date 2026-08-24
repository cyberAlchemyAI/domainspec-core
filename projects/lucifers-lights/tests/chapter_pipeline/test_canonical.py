from __future__ import annotations

import ast
import copy
import json
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chapter_pipeline import (  # noqa: E402
    ChapterRunValidationError,
    DiagnosticCode,
    canonical_bytes,
    canonical_identity,
    canonical_sha256,
    validate_chapter_run,
)


FIXTURE_ROOT = Path(__file__).with_name("fixtures")
CHAPTER_01_DIGEST = "19274758db11e975cf76d8ac51028e1f31a251d6105aa8fd0152ae7ca53a2fe1"
CHAPTER_01_SIZE = 1015
CHAPTER_02_DIGEST = "e6aa70ece11dac28b59c363828d07f4255e98599b66e27444f5d296bfa4286a5"
CHAPTER_02_SIZE = 1017
TOP_LEVEL_FIELDS = {
    "schema",
    "identity",
    "revision",
    "run_phase",
    "context_snapshot",
    "manuscript",
    "derivative_profiles",
    "derivatives",
    "effects",
    "receipts",
    "residue_ref",
    "terminal_outcome",
}


def load_fixture(name: str) -> dict[str, object]:
    return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))


def reverse_mapping_order(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: reverse_mapping_order(item)
            for key, item in reversed(list(value.items()))
        }
    if isinstance(value, list):
        return [reverse_mapping_order(item) for item in value]
    return value


class CanonicalIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chapter_01 = load_fixture("chapter-01-structural.json")
        cls.chapter_02 = load_fixture("chapter-02-synthetic.json")

    def assert_has_code(
        self,
        value: object,
        code: DiagnosticCode,
    ) -> None:
        result = validate_chapter_run(value)
        self.assertFalse(result.is_valid)
        self.assertIn(code, {item.code for item in result.diagnostics})

    def test_fixture_canonical_vectors(self) -> None:
        vectors = (
            (self.chapter_01, CHAPTER_01_DIGEST, CHAPTER_01_SIZE),
            (self.chapter_02, CHAPTER_02_DIGEST, CHAPTER_02_SIZE),
        )
        for fixture, expected_digest, expected_size in vectors:
            with self.subTest(chapter_id=fixture["identity"]["chapter_id"]):
                identity = canonical_identity(fixture)
                self.assertEqual(identity.sha256, expected_digest)
                self.assertEqual(len(identity.canonical_bytes), expected_size)
                self.assertEqual(canonical_sha256(fixture), expected_digest)
                self.assertEqual(canonical_bytes(fixture), identity.canonical_bytes)
                self.assertFalse(identity.canonical_bytes.endswith(b"\n"))
                self.assertNotIn(b": ", identity.canonical_bytes)
                self.assertEqual(
                    json.loads(identity.canonical_bytes),
                    fixture,
                )

    def test_mapping_order_does_not_change_identity(self) -> None:
        reordered = reverse_mapping_order(self.chapter_01)
        self.assertEqual(
            canonical_bytes(self.chapter_01),
            canonical_bytes(reordered),
        )
        self.assertEqual(
            canonical_sha256(self.chapter_01),
            canonical_sha256(reordered),
        )

    def test_admitted_content_change_changes_identity(self) -> None:
        changed = copy.deepcopy(self.chapter_01)
        changed["context_snapshot"]["production"]["production_id"] = (
            "production-candidate-002"
        )
        self.assertNotEqual(
            canonical_sha256(self.chapter_01),
            canonical_sha256(changed),
        )

    def test_inputs_are_not_mutated(self) -> None:
        source = copy.deepcopy(self.chapter_01)
        before = copy.deepcopy(source)
        canonical_identity(source)
        self.assertEqual(source, before)

    def test_logical_chapter_run_shape_is_exact(self) -> None:
        self.assertEqual(set(self.chapter_01), TOP_LEVEL_FIELDS)
        self.assertEqual(set(self.chapter_02), TOP_LEVEL_FIELDS)
        for legacy_field in (
            "schema_version",
            "chapter_id",
            "source",
            "bindings",
            "counts",
            "speakers",
            "tags",
            "state",
        ):
            self.assertNotIn(legacy_field, self.chapter_01)

    def test_fixtures_are_story_safe_and_materially_different(self) -> None:
        chapter_text = (FIXTURE_ROOT / "chapter-01-structural.json").read_text(
            encoding="utf-8"
        )
        for forbidden in (
            '"prose"',
            '"paragraphs"',
            '"author_acceptance"',
            '"accepted"',
        ):
            self.assertNotIn(forbidden, chapter_text)
        self.assertEqual(
            self.chapter_01["context_snapshot"]["source"]["sha256"],
            "ee57d5c8ef0ccd927d0ed267d6cc75ca38da8a71f93683bf68b9864352d2a64e",
        )
        self.assertEqual(
            self.chapter_01["manuscript"]["decision_state"], "candidate"
        )
        selectors = (
            lambda item: item["identity"]["chapter_id"],
            lambda item: item["derivative_profiles"],
            lambda item: item["context_snapshot"]["counts"],
            lambda item: item["context_snapshot"]["speakers"],
            lambda item: item["context_snapshot"]["tags"],
            lambda item: item["context_snapshot"]["production"][
                "production_id"
            ],
        )
        for selector in selectors:
            self.assertNotEqual(
                selector(self.chapter_01),
                selector(self.chapter_02),
            )

    def test_story_safe_structural_metadata_is_confined_to_context(self) -> None:
        context = self.chapter_01["context_snapshot"]
        self.assertEqual(
            set(context), {"source", "production", "counts", "speakers", "tags"}
        )
        for field in ("counts", "speakers", "tags", "production"):
            self.assertNotIn(field, set(self.chapter_01) - {"context_snapshot"})

    def test_unsupported_schema_version_is_stable(self) -> None:
        invalid = copy.deepcopy(self.chapter_01)
        invalid["schema"]["version"] = "999.0.0"
        first = validate_chapter_run(invalid)
        second = validate_chapter_run(invalid)
        self.assertEqual(first.diagnostics, second.diagnostics)
        self.assertEqual(
            [item.code for item in first.diagnostics],
            [DiagnosticCode.UNSUPPORTED_SCHEMA_VERSION],
        )

    def test_floats_and_non_finite_values_are_rejected(self) -> None:
        cases = (
            (1.25, DiagnosticCode.FLOAT_NOT_SUPPORTED),
            (float("nan"), DiagnosticCode.NON_FINITE_NUMBER),
            (float("inf"), DiagnosticCode.NON_FINITE_NUMBER),
        )
        for number, code in cases:
            with self.subTest(number=number):
                invalid = copy.deepcopy(self.chapter_01)
                invalid["context_snapshot"]["counts"]["line_count"] = number
                self.assert_has_code(invalid, code)

    def test_unknown_and_missing_fields_are_rejected(self) -> None:
        unknown = copy.deepcopy(self.chapter_01)
        unknown["authority"] = {"accepted": True}
        self.assert_has_code(unknown, DiagnosticCode.UNKNOWN_FIELD)

        nested_unknown = copy.deepcopy(self.chapter_01)
        nested_unknown["context_snapshot"]["source"]["resolved_path"] = (
            "/tmp/chapter.md"
        )
        self.assert_has_code(nested_unknown, DiagnosticCode.UNKNOWN_FIELD)

        missing = copy.deepcopy(self.chapter_01)
        del missing["manuscript"]
        self.assert_has_code(missing, DiagnosticCode.MISSING_FIELD)

    def test_malformed_bindings_and_profiles_are_rejected(self) -> None:
        malformed_binding = copy.deepcopy(self.chapter_01)
        malformed_binding["derivatives"]["visual-plan"] = {
            "id": "visual-plan",
            "kind": "visual-plan",
            "inputs": [],
            "state": "unbound",
            "binding": "source-digest-only",
            "adaptation_ref": None,
        }
        self.assert_has_code(malformed_binding, DiagnosticCode.INVALID_TYPE)

        invalid_profiles = copy.deepcopy(self.chapter_01)
        invalid_profiles["derivative_profiles"] = "illustrated"
        self.assert_has_code(invalid_profiles, DiagnosticCode.INVALID_TYPE)

        duplicate_profiles = copy.deepcopy(self.chapter_02)
        duplicate_profiles["derivative_profiles"] = ["narrated", "narrated"]
        self.assert_has_code(duplicate_profiles, DiagnosticCode.DUPLICATE_VALUE)

    def test_non_json_values_and_keys_are_rejected(self) -> None:
        tuple_value = copy.deepcopy(self.chapter_01)
        tuple_value["context_snapshot"]["speakers"] = ("speaker-alpha",)
        self.assert_has_code(tuple_value, DiagnosticCode.UNSUPPORTED_VALUE)

        byte_value = copy.deepcopy(self.chapter_01)
        byte_value["context_snapshot"]["source"]["locator"] = b"chapter.md"
        self.assert_has_code(byte_value, DiagnosticCode.UNSUPPORTED_VALUE)

        non_string_key = copy.deepcopy(self.chapter_01)
        non_string_key[1] = "not-json"
        self.assert_has_code(non_string_key, DiagnosticCode.NON_STRING_KEY)

    def test_cycles_are_rejected_without_recursion_failure(self) -> None:
        cyclic = copy.deepcopy(self.chapter_01)
        cyclic["cycle"] = cyclic
        self.assert_has_code(cyclic, DiagnosticCode.CYCLIC_VALUE)

    def test_digest_count_and_source_bindings_are_enforced(self) -> None:
        bad_digest = copy.deepcopy(self.chapter_01)
        bad_digest["context_snapshot"]["source"]["sha256"] = "NOT-A-DIGEST"
        self.assert_has_code(bad_digest, DiagnosticCode.INVALID_DIGEST)

        bad_speaker_count = copy.deepcopy(self.chapter_02)
        bad_speaker_count["context_snapshot"]["counts"]["speaker_count"] = 1
        self.assert_has_code(bad_speaker_count, DiagnosticCode.INCONSISTENT_COUNT)

        bad_tag_count = copy.deepcopy(self.chapter_01)
        bad_tag_count["context_snapshot"]["counts"]["tag_count"] = 99
        self.assert_has_code(bad_tag_count, DiagnosticCode.INCONSISTENT_COUNT)

        bad_source_binding = copy.deepcopy(self.chapter_01)
        bad_source_binding["manuscript"]["sha256"] = "2" * 64
        self.assert_has_code(
            bad_source_binding, DiagnosticCode.INCONSISTENT_BINDING
        )

        accepted_without_receipt = copy.deepcopy(self.chapter_01)
        accepted_without_receipt["manuscript"]["decision_state"] = "accepted"
        accepted_without_receipt["manuscript"]["decision_receipt_ref"] = None
        self.assert_has_code(
            accepted_without_receipt, DiagnosticCode.INCONSISTENT_BINDING
        )

    def test_identifier_arrays_are_unique_and_canonical(self) -> None:
        unsorted_tags = copy.deepcopy(self.chapter_02)
        unsorted_tags["context_snapshot"]["tags"] = list(
            reversed(unsorted_tags["context_snapshot"]["tags"])
        )
        self.assert_has_code(unsorted_tags, DiagnosticCode.NON_CANONICAL_ORDER)

        duplicate_speakers = copy.deepcopy(self.chapter_02)
        duplicate_speakers["context_snapshot"]["speakers"] = [
            "speaker-alpha",
            "speaker-alpha",
        ]
        self.assert_has_code(duplicate_speakers, DiagnosticCode.DUPLICATE_VALUE)

        profile_order = copy.deepcopy(self.chapter_02)
        profile_order["derivative_profiles"] = ["narrated", "illustrated"]
        self.assert_has_code(profile_order, DiagnosticCode.NON_CANONICAL_ORDER)

    def test_boolean_is_not_an_integer_count(self) -> None:
        invalid = copy.deepcopy(self.chapter_01)
        invalid["context_snapshot"]["counts"]["line_count"] = True
        self.assert_has_code(invalid, DiagnosticCode.INVALID_TYPE)

    def test_protected_content_fields_fail_closed(self) -> None:
        invalid = copy.deepcopy(self.chapter_01)
        invalid["effects"]["narration"] = {
            "id": "narration",
            "operation": "synthesize",
            "plan_ref": None,
            "authorization_ref": None,
            "evidence_ref": None,
            "state": "withheld",
            "credential": "must-not-enter-state",
        }
        self.assert_has_code(invalid, DiagnosticCode.UNKNOWN_FIELD)

    def test_invalid_envelope_raises_typed_error_on_identity_request(self) -> None:
        invalid = copy.deepcopy(self.chapter_01)
        invalid["schema"]["version"] = "2.0.0"
        with self.assertRaises(ChapterRunValidationError) as raised:
            canonical_bytes(invalid)
        self.assertEqual(
            raised.exception.diagnostics[0].code,
            DiagnosticCode.UNSUPPORTED_SCHEMA_VERSION,
        )

    def test_validated_model_round_trips_to_same_identity(self) -> None:
        validated = validate_chapter_run(self.chapter_02).require()
        exported = validated.to_document()
        exported["identity"]["chapter_id"] = "caller-mutation"
        self.assertEqual(
            canonical_identity(validated),
            canonical_identity(self.chapter_02),
        )

    def test_product_import_surface_is_pure(self) -> None:
        allowed_roots = {
            "__future__",
            "canonical",
            "copy",
            "dataclasses",
            "enum",
            "hashlib",
            "json",
            "math",
            "model",
        }
        imported: set[str] = set()
        for product_file in (
            PROJECT_ROOT / "chapter_pipeline" / "__init__.py",
            PROJECT_ROOT / "chapter_pipeline" / "model.py",
            PROJECT_ROOT / "chapter_pipeline" / "canonical.py",
        ):
            tree = ast.parse(product_file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imported.add((node.module or "model").split(".")[0])
        self.assertLessEqual(imported, allowed_roots)


if __name__ == "__main__":
    unittest.main()
