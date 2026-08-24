"""Strict chapter-neutral compiler for the local ``speaker,line`` profile.

The compiler is pure: it accepts source bytes plus one explicit immutable
configuration and returns canonical manifest-envelope bytes. It performs no
file, network, credential, provider, or audio operations.
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
from .compiler_config import (
    CompilerConfig,
    require_normalized_config,
)


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


def _validated_source_rows(
    rows: list[list[str]], config: CompilerConfig
) -> list[tuple[int, int, str, str, str | None]]:
    if not rows:
        raise CsvProfileError("source is empty")
    if tuple(rows[0]) != config.header:
        raise CsvProfileError(
            f"header must be exactly {config.header!r}; got {tuple(rows[0])!r}"
        )

    validated: list[tuple[int, int, str, str, str | None]] = []
    for source_ordinal, row in enumerate(rows[1:], start=1):
        row_number = source_ordinal + 1
        if len(row) != 2:
            raise CsvProfileError(
                f"row {row_number}: expected exactly two fields; got {len(row)}"
            )
        speaker, exact_text = row
        if not speaker or not speaker.strip():
            raise CsvProfileError(f"row {row_number}: speaker is blank")
        if not exact_text or not exact_text.strip():
            raise CsvProfileError(f"row {row_number}: line is blank")
        if "\r" in speaker or "\n" in speaker or "\r" in exact_text or "\n" in exact_text:
            raise CsvProfileError(
                f"row {row_number}: embedded newlines are outside the profile"
            )

        validated.append(
            (
                source_ordinal,
                row_number,
                speaker,
                exact_text,
                _leading_performance_tag(exact_text, row_number),
            )
        )
    return validated


def _selected_source_rows(
    rows: list[tuple[int, int, str, str, str | None]],
    config: CompilerConfig,
) -> list[tuple[int, int, str, str, str | None]]:
    if not config.source_ordinals:
        return rows
    lookup = {item[0]: item for item in rows}
    missing = [ordinal for ordinal in config.source_ordinals if ordinal not in lookup]
    if missing:
        raise CsvProfileError(f"selected source ordinals are missing: {missing}")
    return [lookup[ordinal] for ordinal in config.source_ordinals]


def _compile_segments(
    rows: list[list[str]], config: CompilerConfig
) -> list[dict[str, JsonValue]]:
    selected = _selected_source_rows(_validated_source_rows(rows, config), config)
    segments: list[dict[str, JsonValue]] = []
    observed_speakers: set[str] = set()
    tagged_count = 0
    for ordinal, (_, row_number, speaker, exact_text, tag) in enumerate(
        selected, start=1
    ):
        if speaker not in config.allowed_speakers:
            raise CsvProfileError(
                f"row {row_number}: unknown selected speaker {speaker!r}"
            )
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

    if len(segments) != config.expected_segment_count:
        raise CsvProfileError(
            f"expected {config.expected_segment_count} segments; got {len(segments)}"
        )
    if observed_speakers != config.allowed_speakers:
        missing = sorted(config.allowed_speakers - observed_speakers)
        extra = sorted(observed_speakers - config.allowed_speakers)
        raise CsvProfileError(
            f"speaker set does not match config; missing={missing}, extra={extra}"
        )
    if tagged_count != config.expected_tagged_row_count:
        raise CsvProfileError(
            f"expected {config.expected_tagged_row_count} tagged rows; got {tagged_count}"
        )
    return segments


def compile_manifest(
    source_bytes: bytes,
    *,
    config: CompilerConfig,
) -> CompiledManifest:
    """Compile bound source bytes using one explicit normalized config."""

    active_config = require_normalized_config(config)
    if type(source_bytes) is not bytes:
        raise ManifestCompilerError("source must be exact bytes")
    actual_digest = hashlib.sha256(source_bytes).hexdigest()
    if actual_digest != active_config.expected_source_sha256:
        raise SourceDigestMismatch(
            "source digest mismatch: expected "
            f"{active_config.expected_source_sha256}, got {actual_digest}"
        )

    text = _decode_source(source_bytes)
    segments = _compile_segments(_parse_csv(text), active_config)
    envelope = manifest_envelope(
        production_id=active_config.production_id,
        source={
            "locator": active_config.source_locator,
            "sha256": actual_digest,
            "size_bytes": len(source_bytes),
            "media_type": active_config.source_media_type,
            "profile": active_config.source_profile,
            "header": list(active_config.header),
        },
        segments=segments,
        output_policy={
            "segment_order": active_config.segment_order,
            "text_representation": active_config.text_representation,
            "default_output_granularity": active_config.default_output_granularity,
        },
        acceptance_policy={
            "allowed_speakers": sorted(active_config.allowed_speakers),
            "expected_segment_count": active_config.expected_segment_count,
            "expected_tagged_row_count": active_config.expected_tagged_row_count,
            "performance_tag_profile": active_config.performance_tag_profile,
            "transformations_require_approval": active_config.transformations_require_approval,
        },
    )
    return CompiledManifest(canonical_bytes(envelope))
