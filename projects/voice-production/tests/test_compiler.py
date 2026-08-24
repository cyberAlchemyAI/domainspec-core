from __future__ import annotations

import ast
import copy
import csv
import hashlib
import inspect
import io
import os
import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from typing import Any


STAGING_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(STAGING_ROOT))

from voice_production import compiler  # noqa: E402
from voice_production.canonical import verify_envelope  # noqa: E402
from voice_production.compiler import (  # noqa: E402
    CsvProfileError,
    ManifestCompilerError,
    SourceDigestMismatch,
    compile_manifest,
)
from voice_production.compiler_config import (  # noqa: E402
    CompilerConfigError,
    compiler_config_from_document,
    compiler_config_from_json_bytes,
)


CSV_RELATIVE_PATH = Path(
    "projects/lucifers-lights/drafts/graphic-novel/chapter-01/audio/"
    "elevenlabs-voiceover-studio.csv"
)
CONFIG_RELATIVE_PATH = Path(
    "projects/lucifers-lights/factory/voice/chapter-01.json"
)
SYNTHETIC_SOURCE = STAGING_ROOT / "tests/fixtures/chapter-02-synthetic.csv"
SYNTHETIC_CONFIG = STAGING_ROOT / "tests/fixtures/chapter-02-compiler-config.json"
CHAPTER_01_SOURCE_SHA256 = (
    "99ed4a664bba57b0f090a043382fc1de3d5dac5ed5147cbb8fde92c4497dbfa3"
)
CHAPTER_01_MANIFEST_DIGEST = (
    "84b26ccb9c71b4bd90cca36bffd7fb9066230446293e0bc4e4e9018b0c70a77d"
)
CHAPTER_01_CANONICAL_SHA256 = (
    "5e2f55e0fb795cd6dee552d961567e58a22aa36757e6508059133504fa640376"
)
ALLOWED_SPEAKERS = frozenset({"ELENA", "LUCIFER", "MARA", "RUTH", "SYSTEM"})
EXPECTED_TAGS = {
    1: "[measured, intimate]",
    7: "[guarded]",
    36: "[softly, fascinated]",
    54: "[quietly]",
    56: "[coldly]",
    65: "[tense]",
    101: "[quietly, urgent]",
    108: "[unsettled]",
    112: "[darkly]",
}


def source_path() -> Path:
    configured = os.environ.get("VPA_SOURCE_CSV")
    if configured:
        return Path(configured)
    return REPOSITORY_ROOT / CSV_RELATIVE_PATH


def parse_rows(payload: bytes) -> list[list[str]]:
    return list(
        csv.reader(
            io.StringIO(payload.decode("utf-8"), newline=""),
            strict=True,
        )
    )


def render_rows(rows: list[list[str]]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def compile_rebound(payload: bytes):
    return compile_manifest(
        payload,
        config=replace(
            CHAPTER_01_CONFIG,
            expected_source_sha256=hashlib.sha256(payload).hexdigest(),
        ),
    )


CHAPTER_01_CONFIG = compiler_config_from_json_bytes(
    (REPOSITORY_ROOT / CONFIG_RELATIVE_PATH).read_bytes()
)


class CompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_bytes = source_path().read_bytes()
        cls.source_rows = parse_rows(cls.source_bytes)

    def test_exact_fixture_compiles_with_order_text_counts_and_source_binding(self) -> None:
        compiled = compile_manifest(self.source_bytes, config=CHAPTER_01_CONFIG)
        envelope = compiled.as_envelope()
        value = envelope["value"]
        segments = value["segments"]

        self.assertTrue(verify_envelope(envelope))
        self.assertEqual(
            hashlib.sha256(self.source_bytes).hexdigest(),
            CHAPTER_01_SOURCE_SHA256,
        )
        self.assertEqual(value["source"]["sha256"], CHAPTER_01_SOURCE_SHA256)
        self.assertEqual(value["source"]["size_bytes"], len(self.source_bytes))
        self.assertEqual(len(segments), 112)
        self.assertEqual({segment["speaker"] for segment in segments}, ALLOWED_SPEAKERS)

        for ordinal, (source_row, segment) in enumerate(
            zip(self.source_rows[1:], segments, strict=True),
            start=1,
        ):
            speaker, exact_text = source_row
            with self.subTest(ordinal=ordinal):
                self.assertEqual(segment["segment_id"], f"segment-{ordinal:03d}")
                self.assertEqual(segment["ordinal"], ordinal)
                self.assertEqual(segment["source_row_number"], ordinal + 1)
                self.assertEqual(segment["speaker"], speaker)
                self.assertEqual(segment["exact_text"], exact_text)
                self.assertEqual(
                    segment["exact_text_sha256"],
                    hashlib.sha256(exact_text.encode("utf-8")).hexdigest(),
                )
                self.assertEqual(
                    segment["leading_performance_tag"],
                    EXPECTED_TAGS.get(ordinal),
                )
        self.assertEqual(
            sum(
                segment["leading_performance_tag"] is not None
                for segment in segments
            ),
            9,
        )
        self.assertEqual(compiled.digest, CHAPTER_01_MANIFEST_DIGEST)
        self.assertEqual(len(compiled.canonical_envelope_bytes), 33923)
        self.assertEqual(
            hashlib.sha256(compiled.canonical_envelope_bytes).hexdigest(),
            CHAPTER_01_CANONICAL_SHA256,
        )

    def test_compilation_is_byte_stable_and_artifact_is_immutable(self) -> None:
        first = compile_manifest(self.source_bytes, config=CHAPTER_01_CONFIG)
        second = compile_manifest(bytes(self.source_bytes), config=CHAPTER_01_CONFIG)
        self.assertEqual(first.canonical_envelope_bytes, second.canonical_envelope_bytes)
        self.assertEqual(first.digest, second.digest)

        with self.assertRaises(FrozenInstanceError):
            first.canonical_envelope_bytes = b"mutated"  # type: ignore[misc]

        detached = first.as_envelope()
        detached["value"]["segments"][0]["exact_text"] = "mutated copy"
        self.assertEqual(
            first.value["segments"][0]["exact_text"],
            self.source_rows[1][1],
        )

    def test_source_digest_mismatch_and_invalid_binding_fail_closed(self) -> None:
        with self.assertRaises(SourceDigestMismatch):
            compile_manifest(self.source_bytes + b"\n", config=CHAPTER_01_CONFIG)
        with self.assertRaises(TypeError):
            compile_manifest(self.source_bytes)  # type: ignore[call-arg]
        with self.assertRaises(CompilerConfigError):
            compile_manifest(self.source_bytes, config="not-a-config")  # type: ignore[arg-type]
        with self.assertRaises(ManifestCompilerError):
            compile_manifest("not-bytes", config=CHAPTER_01_CONFIG)  # type: ignore[arg-type]

    def test_wrong_header_is_rejected(self) -> None:
        rows = copy.deepcopy(self.source_rows)
        rows[0] = ["line", "speaker"]
        with self.assertRaisesRegex(CsvProfileError, "header must be exactly"):
            compile_rebound(render_rows(rows))

    def test_blank_speaker_and_line_fields_are_rejected(self) -> None:
        cases = [
            (0, ""),
            (0, "   "),
            (1, ""),
            (1, "   "),
        ]
        for field_index, replacement in cases:
            rows = copy.deepcopy(self.source_rows)
            rows[1][field_index] = replacement
            with self.subTest(field=field_index, replacement=repr(replacement)):
                with self.assertRaisesRegex(CsvProfileError, "is blank"):
                    compile_rebound(render_rows(rows))

    def test_empty_or_unknown_speaker_is_rejected(self) -> None:
        for speaker in ["", "NARRATOR", "lucifer", " LUCIFER"]:
            rows = copy.deepcopy(self.source_rows)
            rows[1][0] = speaker
            with self.subTest(speaker=repr(speaker)):
                with self.assertRaises(CsvProfileError):
                    compile_rebound(render_rows(rows))

    def test_injected_extra_and_provider_shaped_fields_are_rejected(self) -> None:
        header_injection = copy.deepcopy(self.source_rows)
        header_injection[0].append("voice_id")
        for row in header_injection[1:]:
            row.append("injected")
        with self.assertRaisesRegex(CsvProfileError, "header must be exactly"):
            compile_rebound(render_rows(header_injection))

        row_injection = copy.deepcopy(self.source_rows)
        row_injection[1].append("model_option=injected")
        with self.assertRaisesRegex(CsvProfileError, "exactly two fields"):
            compile_rebound(render_rows(row_injection))

    def test_malformed_csv_and_utf8_are_rejected(self) -> None:
        malformed_csv = b'speaker,line\nLUCIFER,"unterminated\n'
        with self.assertRaisesRegex(CsvProfileError, "malformed CSV"):
            compile_rebound(malformed_csv)

        invalid_utf8 = self.source_bytes + b"\xff"
        with self.assertRaisesRegex(CsvProfileError, "valid UTF-8"):
            compile_rebound(invalid_utf8)

        nul_source = self.source_bytes + b"\x00"
        with self.assertRaisesRegex(CsvProfileError, "NUL"):
            compile_rebound(nul_source)

    def test_closed_profile_counts_speakers_and_tags_are_enforced(self) -> None:
        missing_row = copy.deepcopy(self.source_rows[:-1])
        with self.assertRaisesRegex(CsvProfileError, "expected 112 segments"):
            compile_rebound(render_rows(missing_row))

        missing_speaker = copy.deepcopy(self.source_rows)
        for row in missing_speaker[1:]:
            if row[0] == "RUTH":
                row[0] = "MARA"
        with self.assertRaisesRegex(CsvProfileError, "speaker set does not match"):
            compile_rebound(render_rows(missing_speaker))

        missing_tag = copy.deepcopy(self.source_rows)
        missing_tag[1][1] = missing_tag[1][1].split("] ", 1)[1]
        with self.assertRaisesRegex(CsvProfileError, "expected 9 tagged rows"):
            compile_rebound(render_rows(missing_tag))

        malformed_tag = copy.deepcopy(self.source_rows)
        malformed_tag[1][1] = "[broken tag without terminator"
        with self.assertRaisesRegex(CsvProfileError, "malformed leading"):
            compile_rebound(render_rows(malformed_tag))

    def test_import_surface_contains_no_effectful_runtime_modules(self) -> None:
        tree = ast.parse(inspect.getsource(compiler))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imports.add(node.module.split(".", 1)[0])
        forbidden = {
            "http",
            "requests",
            "socket",
            "subprocess",
            "urllib",
        }
        self.assertFalse(imports & forbidden)

        source = inspect.getsource(compiler)
        for forbidden_name in ("provider_options", "api_key", "voice_id", "model_id"):
            with self.subTest(forbidden_name=forbidden_name):
                self.assertNotIn(forbidden_name, source)

    def test_materially_different_chapter_uses_explicit_selection(self) -> None:
        source = SYNTHETIC_SOURCE.read_bytes()
        config = compiler_config_from_json_bytes(SYNTHETIC_CONFIG.read_bytes())
        compiled = compile_manifest(source, config=config)
        value = compiled.value
        segments = value["segments"]

        self.assertEqual(value["production_id"], "synthetic.chapter-02.voice-production")
        self.assertEqual([item["source_row_number"] for item in segments], [2, 4, 6])
        self.assertEqual(
            [item["speaker"] for item in segments],
            ["NARRATOR", "ORACLE", "NARRATOR"],
        )
        self.assertEqual(
            [item["segment_id"] for item in segments],
            ["segment-001", "segment-002", "segment-003"],
        )
        self.assertEqual(
            [item["leading_performance_tag"] for item in segments],
            [None, "[calmly]", None],
        )
        self.assertNotEqual(compiled.digest, CHAPTER_01_MANIFEST_DIGEST)

    def test_compiler_has_no_chapter_01_defaults(self) -> None:
        source = inspect.getsource(compiler)
        for forbidden in (
            "CHAPTER_01",
            "graphic-novel.chapter-01",
            CHAPTER_01_SOURCE_SHA256,
            "ELENA",
            "LUCIFER",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def test_config_contract_is_closed_and_rejects_duplicate_json_keys(self) -> None:
        unknown = CHAPTER_01_CONFIG.to_document()
        unknown["unexpected"] = True
        with self.assertRaisesRegex(CompilerConfigError, "unknown fields"):
            compiler_config_from_document(unknown)

        duplicate = (
            b'{"schema_version":"voice-production.compiler-config/v1",'
            b'"schema_version":"voice-production.compiler-config/v1"}'
        )
        with self.assertRaisesRegex(CompilerConfigError, "duplicate"):
            compiler_config_from_json_bytes(duplicate)

    def test_selection_contract_is_explicit_and_consistent(self) -> None:
        document = CHAPTER_01_CONFIG.to_document()
        document["selection"] = {
            "mode": "source-ordinals",
            "source_ordinals": [1, 3],
        }
        with self.assertRaisesRegex(
            CompilerConfigError, "count must equal expected_segment_count"
        ):
            compiler_config_from_document(document)


if __name__ == "__main__":
    unittest.main()
