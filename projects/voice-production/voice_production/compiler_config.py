"""Closed, immutable configuration for the chapter-neutral voice compiler."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, cast

from .canonical import JsonValue, canonical_sha256


COMPILER_CONFIG_SCHEMA = "voice-production.compiler-config/v1"
CSV_PROFILE = "speaker-line-csv/v1"
SELECTION_ALL = "all-source-rows"
SELECTION_ORDINALS = "source-ordinals"
SEGMENT_ORDER = "source-row-order"
TEXT_REPRESENTATION = "exact"
OUTPUT_GRANULARITY = "segment"
PERFORMANCE_TAG_PROFILE = "explicit-leading-bracket/v1"

_EXPECTED_HEADER = ("speaker", "line")
_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


class CompilerConfigError(ValueError):
    """Raised when a compiler configuration is missing, open, or inconsistent."""


@dataclass(frozen=True, slots=True)
class CompilerConfig:
    """All chapter-varying inputs required by one compilation."""

    schema_version: str
    production_id: str
    expected_source_sha256: str
    source_locator: str
    source_media_type: str
    source_profile: str
    header: tuple[str, ...]
    selection_mode: str
    source_ordinals: tuple[int, ...]
    allowed_speakers: frozenset[str]
    expected_segment_count: int
    performance_tag_profile: str
    expected_tagged_row_count: int
    segment_order: str
    text_representation: str
    default_output_granularity: str
    transformations_require_approval: bool

    def to_document(self) -> dict[str, JsonValue]:
        selection: dict[str, JsonValue] = {"mode": self.selection_mode}
        if self.selection_mode == SELECTION_ORDINALS:
            selection["source_ordinals"] = list(self.source_ordinals)
        return {
            "schema_version": self.schema_version,
            "production_id": self.production_id,
            "source": {
                "expected_sha256": self.expected_source_sha256,
                "locator": self.source_locator,
                "media_type": self.source_media_type,
                "profile": self.source_profile,
                "header": list(self.header),
            },
            "selection": selection,
            "acceptance": {
                "allowed_speakers": sorted(self.allowed_speakers),
                "expected_segment_count": self.expected_segment_count,
                "performance_tags": {
                    "profile": self.performance_tag_profile,
                    "expected_count": self.expected_tagged_row_count,
                },
                "transformations_require_approval": self.transformations_require_approval,
            },
            "output_policy": {
                "segment_order": self.segment_order,
                "text_representation": self.text_representation,
                "default_output_granularity": self.default_output_granularity,
            },
        }

    @property
    def digest(self) -> str:
        return canonical_sha256(self.to_document())


def _closed_object(
    value: object,
    label: str,
    required: set[str],
    optional: set[str] | None = None,
) -> dict[str, Any]:
    if type(value) is not dict:
        raise CompilerConfigError(f"{label} must be an object")
    candidate = cast(dict[str, Any], value)
    allowed = required | (optional or set())
    missing = sorted(required - set(candidate))
    unknown = sorted(set(candidate) - allowed)
    if missing:
        raise CompilerConfigError(f"{label} missing fields: {', '.join(missing)}")
    if unknown:
        raise CompilerConfigError(f"{label} has unknown fields: {', '.join(unknown)}")
    return candidate


def _text(value: object, label: str) -> str:
    if type(value) is not str or not value or value.strip() != value:
        raise CompilerConfigError(f"{label} must be non-empty trimmed text")
    return value


def _integer(value: object, label: str, *, allow_zero: bool = False) -> int:
    minimum = 0 if allow_zero else 1
    if type(value) is not int or value < minimum:
        raise CompilerConfigError(f"{label} must be an integer >= {minimum}")
    return value


def _sha256(value: object, label: str) -> str:
    digest = _text(value, label)
    if _SHA256_RE.fullmatch(digest) is None:
        raise CompilerConfigError(f"{label} must be a lowercase SHA-256 hex string")
    return digest


def _text_array(value: object, label: str, *, canonical_order: bool) -> list[str]:
    if type(value) is not list or not value:
        raise CompilerConfigError(f"{label} must be a non-empty array")
    result = [_text(item, f"{label}[{index}]") for index, item in enumerate(value)]
    if len(result) != len(set(result)):
        raise CompilerConfigError(f"{label} must not contain duplicates")
    if canonical_order and result != sorted(result):
        raise CompilerConfigError(f"{label} must be in canonical sorted order")
    return result


def compiler_config_from_document(value: object) -> CompilerConfig:
    """Validate one closed JSON-shaped compiler configuration."""

    root = _closed_object(
        value,
        "compiler config",
        {
            "schema_version",
            "production_id",
            "source",
            "selection",
            "acceptance",
            "output_policy",
        },
    )
    if root["schema_version"] != COMPILER_CONFIG_SCHEMA:
        raise CompilerConfigError("unsupported compiler config schema")

    source = _closed_object(
        root["source"],
        "compiler config source",
        {"expected_sha256", "locator", "media_type", "profile", "header"},
    )
    profile = _text(source["profile"], "compiler config source profile")
    if profile != CSV_PROFILE:
        raise CompilerConfigError(f"unsupported source profile: {profile}")
    header = tuple(
        _text_array(source["header"], "compiler config source header", canonical_order=False)
    )
    if header != _EXPECTED_HEADER:
        raise CompilerConfigError(
            f"compiler config source header must be exactly {_EXPECTED_HEADER!r}"
        )

    selection = _closed_object(
        root["selection"],
        "compiler config selection",
        {"mode"},
        {"source_ordinals"},
    )
    selection_mode = _text(selection["mode"], "compiler config selection mode")
    if selection_mode == SELECTION_ALL:
        if set(selection) != {"mode"}:
            raise CompilerConfigError(
                "all-source-rows selection must not declare source_ordinals"
            )
        source_ordinals: tuple[int, ...] = ()
    elif selection_mode == SELECTION_ORDINALS:
        if set(selection) != {"mode", "source_ordinals"}:
            raise CompilerConfigError(
                "source-ordinals selection requires source_ordinals"
            )
        raw_ordinals = selection["source_ordinals"]
        if type(raw_ordinals) is not list or not raw_ordinals:
            raise CompilerConfigError("source_ordinals must be a non-empty array")
        ordinals = [
            _integer(item, f"source_ordinals[{index}]")
            for index, item in enumerate(raw_ordinals)
        ]
        if ordinals != sorted(set(ordinals)):
            raise CompilerConfigError("source_ordinals must be unique and sorted")
        source_ordinals = tuple(ordinals)
    else:
        raise CompilerConfigError(f"unsupported selection mode: {selection_mode}")

    acceptance = _closed_object(
        root["acceptance"],
        "compiler config acceptance",
        {
            "allowed_speakers",
            "expected_segment_count",
            "performance_tags",
            "transformations_require_approval",
        },
    )
    speakers = frozenset(
        _text_array(
            acceptance["allowed_speakers"],
            "compiler config allowed_speakers",
            canonical_order=True,
        )
    )
    expected_count = _integer(
        acceptance["expected_segment_count"],
        "compiler config expected_segment_count",
    )
    if selection_mode == SELECTION_ORDINALS and len(source_ordinals) != expected_count:
        raise CompilerConfigError(
            "source_ordinals count must equal expected_segment_count"
        )
    tags = _closed_object(
        acceptance["performance_tags"],
        "compiler config performance_tags",
        {"profile", "expected_count"},
    )
    tag_profile = _text(tags["profile"], "compiler config performance tag profile")
    if tag_profile != PERFORMANCE_TAG_PROFILE:
        raise CompilerConfigError(f"unsupported performance tag profile: {tag_profile}")
    tagged_count = _integer(
        tags["expected_count"],
        "compiler config expected tagged row count",
        allow_zero=True,
    )
    if tagged_count > expected_count:
        raise CompilerConfigError(
            "expected tagged row count exceeds expected segment count"
        )
    if acceptance["transformations_require_approval"] is not True:
        raise CompilerConfigError("transformations_require_approval must be true")

    output = _closed_object(
        root["output_policy"],
        "compiler config output_policy",
        {"segment_order", "text_representation", "default_output_granularity"},
    )
    segment_order = _text(output["segment_order"], "compiler config segment_order")
    text_representation = _text(
        output["text_representation"], "compiler config text_representation"
    )
    granularity = _text(
        output["default_output_granularity"],
        "compiler config default_output_granularity",
    )
    if segment_order != SEGMENT_ORDER:
        raise CompilerConfigError(f"unsupported segment order: {segment_order}")
    if text_representation != TEXT_REPRESENTATION:
        raise CompilerConfigError(
            f"unsupported text representation: {text_representation}"
        )
    if granularity != OUTPUT_GRANULARITY:
        raise CompilerConfigError(f"unsupported output granularity: {granularity}")

    return CompilerConfig(
        schema_version=COMPILER_CONFIG_SCHEMA,
        production_id=_text(root["production_id"], "compiler config production_id"),
        expected_source_sha256=_sha256(
            source["expected_sha256"], "compiler config source expected_sha256"
        ),
        source_locator=_text(source["locator"], "compiler config source locator"),
        source_media_type=_text(source["media_type"], "compiler config source media_type"),
        source_profile=profile,
        header=header,
        selection_mode=selection_mode,
        source_ordinals=source_ordinals,
        allowed_speakers=speakers,
        expected_segment_count=expected_count,
        performance_tag_profile=tag_profile,
        expected_tagged_row_count=tagged_count,
        segment_order=segment_order,
        text_representation=text_representation,
        default_output_granularity=granularity,
        transformations_require_approval=True,
    )


def _reject_constant(token: str) -> None:
    raise CompilerConfigError(f"non-finite JSON token is forbidden: {token}")


def _object_without_duplicate_keys(
    pairs: list[tuple[str, JsonValue]],
) -> dict[str, JsonValue]:
    result: dict[str, JsonValue] = {}
    for key, value in pairs:
        if key in result:
            raise CompilerConfigError(f"duplicate compiler config key: {key!r}")
        result[key] = value
    return result


def compiler_config_from_json_bytes(payload: bytes) -> CompilerConfig:
    """Parse exact UTF-8 JSON bytes without performing file I/O."""

    if type(payload) is not bytes:
        raise CompilerConfigError("compiler config input must be exact bytes")
    try:
        document = json.loads(
            payload.decode("utf-8", errors="strict"),
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except CompilerConfigError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as error:
        raise CompilerConfigError("compiler config must be valid UTF-8 JSON") from error
    return compiler_config_from_document(document)


def require_normalized_config(config: object) -> CompilerConfig:
    """Reject non-config values and forged, non-normalized dataclass instances."""

    if type(config) is not CompilerConfig:
        raise CompilerConfigError("config must be a CompilerConfig")
    normalized = compiler_config_from_document(config.to_document())
    if normalized != config:
        raise CompilerConfigError("compiler config is not normalized")
    return config


__all__ = [
    "COMPILER_CONFIG_SCHEMA",
    "CSV_PROFILE",
    "CompilerConfig",
    "CompilerConfigError",
    "OUTPUT_GRANULARITY",
    "PERFORMANCE_TAG_PROFILE",
    "SEGMENT_ORDER",
    "SELECTION_ALL",
    "SELECTION_ORDINALS",
    "TEXT_REPRESENTATION",
    "compiler_config_from_document",
    "compiler_config_from_json_bytes",
    "require_normalized_config",
]
