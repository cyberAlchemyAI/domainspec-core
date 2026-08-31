"""Closed, story-safe structural model for a ChapterRun envelope.

This module deliberately performs no I/O. It validates only the structural
contract selected by the Lucifer's Lights pipeline design; later SWUs own
transition legality, authority, dependency freshness, and completion meaning.
"""

from __future__ import annotations

import copy
import math
from dataclasses import dataclass
from enum import Enum


SUPPORTED_SCHEMA_ID = "lucifers-lights.chapter-run"
SUPPORTED_SCHEMA_VERSION = "1.0.0"

RUN_PHASES = frozenset(
    {
        "initialized",
        "context_ready",
        "authoring",
        "author_review",
        "baseline_ready",
        "profile_work",
        "review_pending",
        "closed",
        "superseded",
    }
)
MANUSCRIPT_STATES = frozenset(
    {
        "missing",
        "candidate",
        "review_pending",
        "accepted",
        "correction_requested",
        "superseded",
    }
)
DERIVATIVE_STATES = frozenset(
    {
        "not_selected",
        "eligible",
        "unbound",
        "planned",
        "candidate",
        "review_pending",
        "accepted",
        "stale",
        "blocked",
        "failed",
        "deferred",
    }
)
EFFECT_STATES = frozenset(
    {
        "not_applicable",
        "withheld",
        "authorized",
        "submitted",
        "accepted",
        "rejected_no_effect",
        "unknown",
        "reconciled_no_effect",
        "effect_found",
    }
)
TERMINAL_OUTCOMES = frozenset(
    {"completed", "closed_with_deferrals", "superseded"}
)
DERIVATIVE_PROFILE_ORDER = ("illustrated", "narrated", "motion_comic")


class DiagnosticCode(str, Enum):
    INVALID_TYPE = "invalid_type"
    INVALID_VALUE = "invalid_value"
    MISSING_FIELD = "missing_field"
    UNKNOWN_FIELD = "unknown_field"
    UNSUPPORTED_SCHEMA_VERSION = "unsupported_schema_version"
    FLOAT_NOT_SUPPORTED = "float_not_supported"
    NON_FINITE_NUMBER = "non_finite_number"
    UNSUPPORTED_VALUE = "unsupported_value"
    NON_STRING_KEY = "non_string_key"
    CYCLIC_VALUE = "cyclic_value"
    DUPLICATE_VALUE = "duplicate_value"
    NON_CANONICAL_ORDER = "non_canonical_order"
    INVALID_DIGEST = "invalid_digest"
    INCONSISTENT_COUNT = "inconsistent_count"
    INCONSISTENT_BINDING = "inconsistent_binding"


@dataclass(frozen=True, slots=True, order=True)
class Diagnostic:
    path: str
    code: DiagnosticCode
    message: str


@dataclass(frozen=True, slots=True)
class ChapterRun:
    """Validated ChapterRun value with copy-on-export semantics."""

    _document: dict[str, object]

    def to_document(self) -> dict[str, object]:
        return copy.deepcopy(self._document)


@dataclass(frozen=True, slots=True)
class ValidationResult:
    value: ChapterRun | None
    diagnostics: tuple[Diagnostic, ...]

    @property
    def is_valid(self) -> bool:
        return self.value is not None and not self.diagnostics

    def require(self) -> ChapterRun:
        if not self.is_valid:
            raise ChapterRunValidationError(self.diagnostics)
        assert self.value is not None
        return self.value


class ChapterRunValidationError(ValueError):
    def __init__(self, diagnostics: tuple[Diagnostic, ...]) -> None:
        self.diagnostics = diagnostics
        summary = "; ".join(
            f"{item.path}: {item.code.value}: {item.message}"
            for item in diagnostics
        )
        super().__init__(summary or "invalid ChapterRun")


def _add(
    diagnostics: list[Diagnostic],
    path: str,
    code: DiagnosticCode,
    message: str,
) -> None:
    diagnostics.append(Diagnostic(path, code, message))


def _scan_json_value(
    value: object,
    path: str,
    diagnostics: list[Diagnostic],
    active: set[int],
) -> None:
    """Reject values that cannot participate in the declared JSON model."""

    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if math.isfinite(value):
            _add(
                diagnostics,
                path,
                DiagnosticCode.FLOAT_NOT_SUPPORTED,
                "floating-point numbers are not part of the ChapterRun model",
            )
        else:
            _add(
                diagnostics,
                path,
                DiagnosticCode.NON_FINITE_NUMBER,
                "non-finite numbers are not valid JSON",
            )
        return
    if not isinstance(value, (dict, list)):
        _add(
            diagnostics,
            path,
            DiagnosticCode.UNSUPPORTED_VALUE,
            f"unsupported value type {type(value).__name__}",
        )
        return

    marker = id(value)
    if marker in active:
        _add(
            diagnostics,
            path,
            DiagnosticCode.CYCLIC_VALUE,
            "cyclic containers are not supported",
        )
        return
    active.add(marker)
    try:
        if isinstance(value, dict):
            for key, item in sorted(
                value.items(), key=lambda pair: repr(pair[0])
            ):
                if not isinstance(key, str):
                    _add(
                        diagnostics,
                        path,
                        DiagnosticCode.NON_STRING_KEY,
                        f"object key {key!r} is not a string",
                    )
                    child_path = f"{path}[{key!r}]"
                else:
                    child_path = f"{path}.{key}"
                _scan_json_value(item, child_path, diagnostics, active)
        else:
            for index, item in enumerate(value):
                _scan_json_value(
                    item, f"{path}[{index}]", diagnostics, active
                )
    finally:
        active.remove(marker)


def _object(
    value: object,
    path: str,
    fields: tuple[str, ...],
    diagnostics: list[Diagnostic],
) -> dict[str, object] | None:
    if not isinstance(value, dict):
        _add(
            diagnostics,
            path,
            DiagnosticCode.INVALID_TYPE,
            "expected object",
        )
        return None
    string_keys = {key for key in value if isinstance(key, str)}
    for field in fields:
        if field not in string_keys:
            _add(
                diagnostics,
                f"{path}.{field}",
                DiagnosticCode.MISSING_FIELD,
                "required field is missing",
            )
    for field in sorted(string_keys - set(fields)):
        _add(
            diagnostics,
            f"{path}.{field}",
            DiagnosticCode.UNKNOWN_FIELD,
            "field is not declared by the closed structural contract",
        )
    return value


def _string(
    value: object,
    path: str,
    diagnostics: list[Diagnostic],
) -> str | None:
    if not isinstance(value, str):
        _add(
            diagnostics,
            path,
            DiagnosticCode.INVALID_TYPE,
            "expected string",
        )
        return None
    if not value or value.strip() != value:
        _add(
            diagnostics,
            path,
            DiagnosticCode.INVALID_VALUE,
            "expected a non-empty string without surrounding whitespace",
        )
        return None
    return value


def _optional_string(
    value: object,
    path: str,
    diagnostics: list[Diagnostic],
) -> str | None:
    if value is None:
        return None
    return _string(value, path, diagnostics)


def _nonnegative_integer(
    value: object,
    path: str,
    diagnostics: list[Diagnostic],
) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int):
        _add(
            diagnostics,
            path,
            DiagnosticCode.INVALID_TYPE,
            "expected a non-negative integer",
        )
        return None
    if value < 0:
        _add(
            diagnostics,
            path,
            DiagnosticCode.INVALID_VALUE,
            "integer must be non-negative",
        )
        return None
    return value


def _digest(
    value: object,
    path: str,
    diagnostics: list[Diagnostic],
) -> str | None:
    digest = _string(value, path, diagnostics)
    if digest is None:
        return None
    if len(digest) != 64 or any(
        character not in "0123456789abcdef" for character in digest
    ):
        _add(
            diagnostics,
            path,
            DiagnosticCode.INVALID_DIGEST,
            "expected a lowercase SHA-256 hexadecimal digest",
        )
        return None
    return digest


def _enum_value(
    value: object,
    path: str,
    allowed: frozenset[str],
    diagnostics: list[Diagnostic],
) -> str | None:
    item = _string(value, path, diagnostics)
    if item is not None and item not in allowed:
        _add(
            diagnostics,
            path,
            DiagnosticCode.INVALID_VALUE,
            f"unsupported value {item!r}",
        )
        return None
    return item


def _string_array(
    value: object,
    path: str,
    diagnostics: list[Diagnostic],
    *,
    ordered_by: tuple[str, ...] | None = None,
) -> list[str] | None:
    if not isinstance(value, list):
        _add(
            diagnostics,
            path,
            DiagnosticCode.INVALID_TYPE,
            "expected array",
        )
        return None
    items: list[str] = []
    for index, candidate in enumerate(value):
        item = _string(candidate, f"{path}[{index}]", diagnostics)
        if item is not None:
            items.append(item)
    if len(set(items)) != len(items):
        _add(
            diagnostics,
            path,
            DiagnosticCode.DUPLICATE_VALUE,
            "array values must be unique",
        )
    if ordered_by is None:
        expected = sorted(items)
    else:
        rank = {item: index for index, item in enumerate(ordered_by)}
        for index, item in enumerate(items):
            if item not in rank:
                _add(
                    diagnostics,
                    f"{path}[{index}]",
                    DiagnosticCode.INVALID_VALUE,
                    f"unsupported value {item!r}",
                )
        expected = sorted(items, key=lambda item: rank.get(item, len(rank)))
    if items != expected:
        _add(
            diagnostics,
            path,
            DiagnosticCode.NON_CANONICAL_ORDER,
            "array values are not in canonical order",
        )
    return items


def _validate_schema(value: object, diagnostics: list[Diagnostic]) -> None:
    obj = _object(value, "$.schema", ("id", "version"), diagnostics)
    if obj is None:
        return
    schema_id = _string(obj.get("id"), "$.schema.id", diagnostics)
    version = _string(obj.get("version"), "$.schema.version", diagnostics)
    if schema_id is not None and schema_id != SUPPORTED_SCHEMA_ID:
        _add(
            diagnostics,
            "$.schema.id",
            DiagnosticCode.UNSUPPORTED_SCHEMA_VERSION,
            f"unsupported schema id {schema_id!r}",
        )
    if version is not None and version != SUPPORTED_SCHEMA_VERSION:
        _add(
            diagnostics,
            "$.schema.version",
            DiagnosticCode.UNSUPPORTED_SCHEMA_VERSION,
            f"unsupported schema version {version!r}",
        )


def _validate_identity(value: object, diagnostics: list[Diagnostic]) -> None:
    obj = _object(
        value,
        "$.identity",
        ("project_id", "chapter_id", "run_id"),
        diagnostics,
    )
    if obj is None:
        return
    for field in ("project_id", "chapter_id", "run_id"):
        _string(obj.get(field), f"$.identity.{field}", diagnostics)


def _validate_revision(value: object, diagnostics: list[Diagnostic]) -> None:
    obj = _object(
        value, "$.revision", ("number", "prior_digest"), diagnostics
    )
    if obj is None:
        return
    number = _nonnegative_integer(
        obj.get("number"), "$.revision.number", diagnostics
    )
    prior = obj.get("prior_digest")
    if prior is not None:
        _digest(prior, "$.revision.prior_digest", diagnostics)
    if number == 0 and prior is not None:
        _add(
            diagnostics,
            "$.revision.prior_digest",
            DiagnosticCode.INCONSISTENT_BINDING,
            "revision zero cannot bind a prior digest",
        )
    if number is not None and number > 0 and prior is None:
        _add(
            diagnostics,
            "$.revision.prior_digest",
            DiagnosticCode.INCONSISTENT_BINDING,
            "a positive revision requires a prior digest",
        )


def _validate_context_snapshot(
    value: object,
    diagnostics: list[Diagnostic],
) -> tuple[str | None, str | None]:
    obj = _object(
        value,
        "$.context_snapshot",
        ("source", "production", "counts", "speakers", "tags"),
        diagnostics,
    )
    if obj is None:
        return None, None

    source = _object(
        obj.get("source"),
        "$.context_snapshot.source",
        ("kind", "locator", "sha256", "size_bytes", "owner", "status"),
        diagnostics,
    )
    source_locator: str | None = None
    source_digest: str | None = None
    if source is not None:
        kind = _string(
            source.get("kind"), "$.context_snapshot.source.kind", diagnostics
        )
        if kind is not None and kind not in {"repository", "synthetic"}:
            _add(
                diagnostics,
                "$.context_snapshot.source.kind",
                DiagnosticCode.INVALID_VALUE,
                f"unsupported source kind {kind!r}",
            )
        source_locator = _string(
            source.get("locator"),
            "$.context_snapshot.source.locator",
            diagnostics,
        )
        source_digest = _digest(
            source.get("sha256"),
            "$.context_snapshot.source.sha256",
            diagnostics,
        )
        _nonnegative_integer(
            source.get("size_bytes"),
            "$.context_snapshot.source.size_bytes",
            diagnostics,
        )
        _string(
            source.get("owner"),
            "$.context_snapshot.source.owner",
            diagnostics,
        )
        _string(
            source.get("status"),
            "$.context_snapshot.source.status",
            diagnostics,
        )

    production = _object(
        obj.get("production"),
        "$.context_snapshot.production",
        ("production_id", "status"),
        diagnostics,
    )
    if production is not None:
        _string(
            production.get("production_id"),
            "$.context_snapshot.production.production_id",
            diagnostics,
        )
        _string(
            production.get("status"),
            "$.context_snapshot.production.status",
            diagnostics,
        )

    speakers = _string_array(
        obj.get("speakers"), "$.context_snapshot.speakers", diagnostics
    )
    tags = _string_array(
        obj.get("tags"), "$.context_snapshot.tags", diagnostics
    )
    counts = _object(
        obj.get("counts"),
        "$.context_snapshot.counts",
        ("line_count", "speaker_count", "tag_count"),
        diagnostics,
    )
    if counts is not None:
        _nonnegative_integer(
            counts.get("line_count"),
            "$.context_snapshot.counts.line_count",
            diagnostics,
        )
        speaker_count = _nonnegative_integer(
            counts.get("speaker_count"),
            "$.context_snapshot.counts.speaker_count",
            diagnostics,
        )
        tag_count = _nonnegative_integer(
            counts.get("tag_count"),
            "$.context_snapshot.counts.tag_count",
            diagnostics,
        )
        if speakers is not None and speaker_count != len(speakers):
            _add(
                diagnostics,
                "$.context_snapshot.counts.speaker_count",
                DiagnosticCode.INCONSISTENT_COUNT,
                "speaker_count does not match speakers",
            )
        if tags is not None and tag_count != len(tags):
            _add(
                diagnostics,
                "$.context_snapshot.counts.tag_count",
                DiagnosticCode.INCONSISTENT_COUNT,
                "tag_count does not match tags",
            )
    return source_locator, source_digest


def _validate_manuscript(
    value: object,
    source_locator: str | None,
    source_digest: str | None,
    diagnostics: list[Diagnostic],
) -> None:
    obj = _object(
        value,
        "$.manuscript",
        ("locator", "sha256", "decision_state", "decision_receipt_ref"),
        diagnostics,
    )
    if obj is None:
        return
    locator = _string(obj.get("locator"), "$.manuscript.locator", diagnostics)
    digest = _digest(obj.get("sha256"), "$.manuscript.sha256", diagnostics)
    _enum_value(
        obj.get("decision_state"),
        "$.manuscript.decision_state",
        MANUSCRIPT_STATES,
        diagnostics,
    )
    _optional_string(
        obj.get("decision_receipt_ref"),
        "$.manuscript.decision_receipt_ref",
        diagnostics,
    )
    if locator is not None and source_locator is not None and locator != source_locator:
        _add(
            diagnostics,
            "$.manuscript.locator",
            DiagnosticCode.INCONSISTENT_BINDING,
            "manuscript locator does not match the context source",
        )
    if digest is not None and source_digest is not None and digest != source_digest:
        _add(
            diagnostics,
            "$.manuscript.sha256",
            DiagnosticCode.INCONSISTENT_BINDING,
            "manuscript digest does not match the context source",
        )


def _validate_derivative_profiles(
    value: object, diagnostics: list[Diagnostic]
) -> None:
    _string_array(
        value,
        "$.derivative_profiles",
        diagnostics,
        ordered_by=DERIVATIVE_PROFILE_ORDER,
    )


def _validate_derivatives(value: object, diagnostics: list[Diagnostic]) -> None:
    if not isinstance(value, dict):
        _add(
            diagnostics,
            "$.derivatives",
            DiagnosticCode.INVALID_TYPE,
            "expected object",
        )
        return
    for node_id in sorted(key for key in value if isinstance(key, str)):
        path = f"$.derivatives.{node_id}"
        node = _object(
            value[node_id],
            path,
            ("id", "kind", "inputs", "state", "binding", "adaptation_ref"),
            diagnostics,
        )
        if node is None:
            continue
        declared_id = _string(node.get("id"), f"{path}.id", diagnostics)
        if declared_id is not None and declared_id != node_id:
            _add(
                diagnostics,
                f"{path}.id",
                DiagnosticCode.INCONSISTENT_BINDING,
                "derivative id does not match its map key",
            )
        _string(node.get("kind"), f"{path}.kind", diagnostics)
        _string_array(node.get("inputs"), f"{path}.inputs", diagnostics)
        _enum_value(
            node.get("state"),
            f"{path}.state",
            DERIVATIVE_STATES,
            diagnostics,
        )
        binding = node.get("binding")
        if binding is not None:
            binding_obj = _object(
                binding,
                f"{path}.binding",
                ("source_id", "source_digest"),
                diagnostics,
            )
            if binding_obj is not None:
                _string(
                    binding_obj.get("source_id"),
                    f"{path}.binding.source_id",
                    diagnostics,
                )
                _digest(
                    binding_obj.get("source_digest"),
                    f"{path}.binding.source_digest",
                    diagnostics,
                )
        _optional_string(
            node.get("adaptation_ref"), f"{path}.adaptation_ref", diagnostics
        )


def _validate_effects(value: object, diagnostics: list[Diagnostic]) -> None:
    if not isinstance(value, dict):
        _add(
            diagnostics,
            "$.effects",
            DiagnosticCode.INVALID_TYPE,
            "expected object",
        )
        return
    for effect_id in sorted(key for key in value if isinstance(key, str)):
        path = f"$.effects.{effect_id}"
        effect = _object(
            value[effect_id],
            path,
            (
                "id",
                "operation",
                "plan_ref",
                "authorization_ref",
                "evidence_ref",
                "state",
            ),
            diagnostics,
        )
        if effect is None:
            continue
        declared_id = _string(effect.get("id"), f"{path}.id", diagnostics)
        if declared_id is not None and declared_id != effect_id:
            _add(
                diagnostics,
                f"{path}.id",
                DiagnosticCode.INCONSISTENT_BINDING,
                "effect id does not match its map key",
            )
        _string(effect.get("operation"), f"{path}.operation", diagnostics)
        for field in ("plan_ref", "authorization_ref", "evidence_ref"):
            _optional_string(effect.get(field), f"{path}.{field}", diagnostics)
        _enum_value(
            effect.get("state"),
            f"{path}.state",
            EFFECT_STATES,
            diagnostics,
        )


def _validate_receipts(value: object, diagnostics: list[Diagnostic]) -> None:
    if not isinstance(value, list):
        _add(
            diagnostics,
            "$.receipts",
            DiagnosticCode.INVALID_TYPE,
            "expected array",
        )
        return
    receipt_ids: list[str] = []
    for index, item in enumerate(value):
        path = f"$.receipts[{index}]"
        receipt = _object(item, path, ("id", "sha256"), diagnostics)
        if receipt is None:
            continue
        receipt_id = _string(receipt.get("id"), f"{path}.id", diagnostics)
        if receipt_id is not None:
            receipt_ids.append(receipt_id)
        _digest(receipt.get("sha256"), f"{path}.sha256", diagnostics)
    if len(receipt_ids) != len(set(receipt_ids)):
        _add(
            diagnostics,
            "$.receipts",
            DiagnosticCode.DUPLICATE_VALUE,
            "receipt ids must be unique",
        )


def validate_chapter_run(value: object) -> ValidationResult:
    """Validate one ChapterRun without mutating it or consulting external state."""

    if isinstance(value, ChapterRun):
        value = value.to_document()

    diagnostics: list[Diagnostic] = []
    _scan_json_value(value, "$", diagnostics, set())
    if diagnostics:
        return ValidationResult(None, tuple(sorted(set(diagnostics))))

    root = _object(
        value,
        "$",
        (
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
        ),
        diagnostics,
    )
    if root is None:
        return ValidationResult(None, tuple(sorted(set(diagnostics))))

    _validate_schema(root.get("schema"), diagnostics)
    _validate_identity(root.get("identity"), diagnostics)
    _validate_revision(root.get("revision"), diagnostics)
    _enum_value(
        root.get("run_phase"), "$.run_phase", RUN_PHASES, diagnostics
    )
    source_locator, source_digest = _validate_context_snapshot(
        root.get("context_snapshot"), diagnostics
    )
    _validate_manuscript(
        root.get("manuscript"), source_locator, source_digest, diagnostics
    )
    _validate_derivative_profiles(root.get("derivative_profiles"), diagnostics)
    _validate_derivatives(root.get("derivatives"), diagnostics)
    _validate_effects(root.get("effects"), diagnostics)
    _validate_receipts(root.get("receipts"), diagnostics)
    _optional_string(root.get("residue_ref"), "$.residue_ref", diagnostics)
    outcome = root.get("terminal_outcome")
    if outcome is not None:
        _enum_value(
            outcome,
            "$.terminal_outcome",
            TERMINAL_OUTCOMES,
            diagnostics,
        )

    stable = tuple(sorted(set(diagnostics)))
    if stable:
        return ValidationResult(None, stable)
    return ValidationResult(ChapterRun(copy.deepcopy(root)), ())


__all__ = [
    "DERIVATIVE_PROFILE_ORDER",
    "DERIVATIVE_STATES",
    "EFFECT_STATES",
    "MANUSCRIPT_STATES",
    "RUN_PHASES",
    "SUPPORTED_SCHEMA_ID",
    "SUPPORTED_SCHEMA_VERSION",
    "TERMINAL_OUTCOMES",
    "ChapterRun",
    "ChapterRunValidationError",
    "Diagnostic",
    "DiagnosticCode",
    "ValidationResult",
    "validate_chapter_run",
]
