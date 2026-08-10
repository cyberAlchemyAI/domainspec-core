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
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any


STAGING_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STAGING_ROOT))

from voice_production import compiler  # noqa: E402
from voice_production.canonical import verify_envelope  # noqa: E402
from voice_production.compiler import (  # noqa: E402
    ALLOWED_SPEAKERS,
    CHAPTER_01_SOURCE_SHA256,
    CsvProfileError,
    ManifestCompilerError,
    SourceDigestMismatch,
    compile_manifest,
)


CSV_RELATIVE_PATH = Path(
    "drafts/graphic-novel/chapter-01/audio/elevenlabs-voiceover-studio.csv"
)
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
    return Path(__file__).resolve().parents[5] / CSV_RELATIVE_PATH


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
        expected_source_sha256=hashlib.sha256(payload).hexdigest(),
    )


class CompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_bytes = source_path().read_bytes()
        cls.source_rows = parse_rows(cls.source_bytes)

    def test_exact_fixture_compiles_with_order_text_counts_and_source_binding(self) -> None:
        compiled = compile_manifest(self.source_bytes)
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

    def test_compilation_is_byte_stable_and_artifact_is_immutable(self) -> None:
        first = compile_manifest(self.source_bytes)
        second = compile_manifest(bytes(self.source_bytes))
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
            compile_manifest(self.source_bytes + b"\n")
        with self.assertRaises(ManifestCompilerError):
            compile_manifest(
                self.source_bytes,
                expected_source_sha256="not-a-sha256",
            )
        with self.assertRaises(ManifestCompilerError):
            compile_manifest("not-bytes")  # type: ignore[arg-type]

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
        with self.assertRaisesRegex(CsvProfileError, "speaker set is incomplete"):
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


if __name__ == "__main__":
    unittest.main()
