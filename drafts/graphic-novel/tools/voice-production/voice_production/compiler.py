"""Strict compiler for the local ``speaker,line`` source profile.

The compiler is pure: it accepts source bytes and returns an immutable wrapper
around canonical manifest-envelope bytes.  It performs no file, network,
credential, provider, or audio operations.
"""

from __future__ import annotations

import csv
import hashlib
import io
import re
from dataclasses import dataclass
from typing import cast

from .canonical import (
    JsonValue,
    canonical_bytes,
    canonical_loads,
    require_valid_envelope,
)
from .contracts import (
    MANIFEST_SCHEMA_ID,
    ContractEnvelope,
    manifest_envelope,
)


CSV_PROFILE = "speaker-line-csv/v1"
CHAPTER_01_SOURCE_SHA256 = (
    "4e4883ad8f2f0de5028ea238c8dcba6d43b57252225aa41c628c9e0d15992868"
)
CHAPTER_01_SOURCE_LOCATOR = (
    "drafts/graphic-novel/chapter-01/audio/elevenlabs-voiceover-studio.csv"
)
CHAPTER_01_PRODUCTION_ID = "graphic-novel.chapter-01.voice-production"
EXPECTED_HEADER = ("speaker", "line")
EXPECTED_SEGMENT_COUNT = 112
EXPECTED_TAGGED_ROW_COUNT = 9
ALLOWED_SPEAKERS = frozenset({"ELENA", "LUCIFER", "MARA", "RUTH", "SYSTEM"})

_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
_LEADING_TAG_RE = re.compile(r"^\[([^\[\]\r\n]+)\](?=\s|$)")


class ManifestCompilerError(ValueError):
    """Base failure for input outside the accepted source profile."""


class SourceDigestMismatch(ManifestCompilerError):
    """Raised when source bytes do not match their declared binding."""


class CsvProfileError(ManifestCompilerError):
    """Raised when decoded CSV does not match the narrow profile."""


@dataclass(frozen=True, slots=True)
class CompiledManifest:
    """An immutable canonical manifest artifact.

    ``as_envelope`` returns a detached copy, so modifying that copy cannot alter
    the canonical bytes retained by this object.
    """

    canonical_envelope_bytes: bytes

    def __post_init__(self) -> None:
        if type(self.canonical_envelope_bytes) is not bytes:
            raise TypeError("canonical_envelope_bytes must be bytes")
        envelope = self.as_envelope()
        if envelope["schema_id"] != MANIFEST_SCHEMA_ID:
            raise ValueError("compiled artifact is not a manifest envelope")

    def as_envelope(self) -> ContractEnvelope:
        parsed = canonical_loads(self.canonical_envelope_bytes)
        if type(parsed) is not dict:
            raise ValueError("compiled manifest envelope must be an object")
        envelope = cast(dict[str, JsonValue], parsed)
        require_valid_envelope(envelope)
        return cast(ContractEnvelope, envelope)

    @property
    def digest(self) -> str:
        return cast(str, self.as_envelope()["digest"])

    @property
    def value(self) -> dict[str, JsonValue]:
        value = self.as_envelope()["value"]
        if type(value) is not dict:
            raise ValueError("compiled manifest value must be an object")
        return cast(dict[str, JsonValue], value)


def _require_sha256(value: str, name: str) -> str:
    if type(value) is not str or _SHA256_RE.fullmatch(value) is None:
        raise ManifestCompilerError(
            f"{name} must be a lowercase SHA-256 hex string"
        )
    return value


def _decode_source(source_bytes: bytes) -> str:
    if type(source_bytes) is not bytes:
        raise ManifestCompilerError("source must be exact bytes")
    try:
        text = source_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise CsvProfileError("source is not valid UTF-8") from exc
    if "\x00" in text:
        raise CsvProfileError("source contains a NUL character")
    return text


def _parse_csv(text: str) -> list[list[str]]:
    try:
        return list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except (csv.Error, UnicodeError) as exc:
        raise CsvProfileError("source is malformed CSV") from exc


def _leading_performance_tag(exact_text: str, row_number: int) -> str | None:
    match = _LEADING_TAG_RE.match(exact_text)
    if match is None:
        if exact_text.startswith("["):
            raise CsvProfileError(
                f"row {row_number}: malformed leading performance tag"
            )
        return None
    if not match.group(1).strip():
        raise CsvProfileError(
            f"row {row_number}: performance tag must not be blank"
        )
    return match.group(0)


def _compile_segments(rows: list[list[str]]) -> list[dict[str, JsonValue]]:
    if not rows:
        raise CsvProfileError("source is empty")
    if tuple(rows[0]) != EXPECTED_HEADER:
        raise CsvProfileError(
            f"header must be exactly {EXPECTED_HEADER!r}; got {tuple(rows[0])!r}"
        )

    segments: list[dict[str, JsonValue]] = []
    observed_speakers: set[str] = set()
    tagged_count = 0
    for ordinal, row in enumerate(rows[1:], start=1):
        row_number = ordinal + 1
        if len(row) != 2:
            raise CsvProfileError(
                f"row {row_number}: expected exactly two fields; got {len(row)}"
            )
        speaker, exact_text = row
        if not speaker or not speaker.strip():
            raise CsvProfileError(f"row {row_number}: speaker is blank")
        if speaker not in ALLOWED_SPEAKERS:
            raise CsvProfileError(
                f"row {row_number}: unknown speaker {speaker!r}"
            )
        if not exact_text or not exact_text.strip():
            raise CsvProfileError(f"row {row_number}: line is blank")
        if "\r" in speaker or "\n" in speaker or "\r" in exact_text or "\n" in exact_text:
            raise CsvProfileError(
                f"row {row_number}: embedded newlines are outside the profile"
            )

        tag = _leading_performance_tag(exact_text, row_number)
        if tag is not None:
            tagged_count += 1
        observed_speakers.add(speaker)
        segments.append(
            {
                "segment_id": f"segment-{ordinal:03d}",
                "ordinal": ordinal,
                "source_row_number": row_number,
                "speaker": speaker,
                "exact_text": exact_text,
                "exact_text_sha256": hashlib.sha256(
                    exact_text.encode("utf-8")
                ).hexdigest(),
                "leading_performance_tag": tag,
            }
        )

    if len(segments) != EXPECTED_SEGMENT_COUNT:
        raise CsvProfileError(
            f"expected {EXPECTED_SEGMENT_COUNT} segments; got {len(segments)}"
        )
    if observed_speakers != ALLOWED_SPEAKERS:
        missing = sorted(ALLOWED_SPEAKERS - observed_speakers)
        raise CsvProfileError(f"speaker set is incomplete; missing={missing}")
    if tagged_count != EXPECTED_TAGGED_ROW_COUNT:
        raise CsvProfileError(
            f"expected {EXPECTED_TAGGED_ROW_COUNT} tagged rows; got {tagged_count}"
        )
    return segments


def compile_manifest(
    source_bytes: bytes,
    *,
    expected_source_sha256: str = CHAPTER_01_SOURCE_SHA256,
    source_locator: str = CHAPTER_01_SOURCE_LOCATOR,
    production_id: str = CHAPTER_01_PRODUCTION_ID,
) -> CompiledManifest:
    """Compile bound source bytes into one canonical immutable manifest."""

    expected_digest = _require_sha256(
        expected_source_sha256, "expected_source_sha256"
    )
    if type(source_locator) is not str or not source_locator:
        raise ManifestCompilerError("source_locator must be a non-empty string")
    if type(source_bytes) is not bytes:
        raise ManifestCompilerError("source must be exact bytes")
    actual_digest = hashlib.sha256(source_bytes).hexdigest()
    if actual_digest != expected_digest:
        raise SourceDigestMismatch(
            f"source digest mismatch: expected {expected_digest}, got {actual_digest}"
        )

    text = _decode_source(source_bytes)
    segments = _compile_segments(_parse_csv(text))
    envelope = manifest_envelope(
        production_id=production_id,
        source={
            "locator": source_locator,
            "sha256": actual_digest,
            "size_bytes": len(source_bytes),
            "media_type": "text/csv; charset=utf-8",
            "profile": CSV_PROFILE,
            "header": list(EXPECTED_HEADER),
        },
        segments=segments,
        output_policy={
            "segment_order": "source-row-order",
            "text_representation": "exact",
            "default_output_granularity": "segment",
        },
        acceptance_policy={
            "allowed_speakers": sorted(ALLOWED_SPEAKERS),
            "expected_segment_count": EXPECTED_SEGMENT_COUNT,
            "expected_tagged_row_count": EXPECTED_TAGGED_ROW_COUNT,
            "performance_tag_profile": "explicit-leading-bracket/v1",
            "transformations_require_approval": True,
        },
    )
    return CompiledManifest(canonical_bytes(envelope))
