"""pipeline.seats.scribe.types — §7 Scribe Round 1 shape-only dataclasses.

Blueprint §7 Scribe v1.1.1 LOCKED 2026-04-21
(pipeline/blueprint/v0.1/section_07_scribe.md):
- §7.3 Phase 0 RFA extraction contract → RfaExtractedRecord + support shapes
- §7.4 Phase 1 KGIE preflight contract → KgiePreflightResult + support shapes
- §7.13 failure-code constants → F_SCRIBE_* string constants

Round 1 ships only *shape* — zero drafting, zero LLM calls. ``__post_init__``
enforces construction-time invariants (sha hex length, timezone awareness,
status-field closed enumeration, identity-source presence). Algorithmic
behaviour lands at R2 (drafting phases) and R3 (subprocess entry).

Every frozen dataclass is ``kw_only=True`` so field additions in v0.2 cannot
silently reorder positional calls (A-13 memory-layout discipline).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from types import MappingProxyType
from typing import Final, Literal, Mapping

# ---------------------------------------------------------------------------
# Type aliases (§7.4 KGIE tri-state; §7.5 dialect register)
# ---------------------------------------------------------------------------

KgieStatus = Literal["pass", "fail", "needs_operator_input"]

KeywordAffirmation = Literal["affirmed", "not_applicable_with_reason", "unanswered"]

# Inline-literal frozen sets — V1 rebind-resistance (§5 R1 precedent).
_KGIE_STATUS_VALID: Final[frozenset[str]] = frozenset(
    {"pass", "fail", "needs_operator_input"}
)
_KEYWORD_AFFIRMATION_VALID: Final[frozenset[str]] = frozenset(
    {"affirmed", "not_applicable_with_reason", "unanswered"}
)

# §7.13 failure-code strings — MUST match the blueprint verbatim (row numbers
# in §0.5 v7 amendment noted inline). Kept as plain strings: exception
# classes live in ``pipeline.logician`` at R3 wiring time; R1 only needs the
# code symbols so Logician PRE-gate slots can reference them.
F_SCRIBE_RFA_MISSING: Final[str] = "F-SCRIBE-RFA-MISSING"            # §0.5 v7 row 132
F_SCRIBE_RFA_DRIFT: Final[str] = "F-SCRIBE-RFA-DRIFT"                # §0.5 v7 row 133
F_SCRIBE_PHASE_0_MISSING: Final[str] = "F-SCRIBE-PHASE-0-MISSING"    # §0.5 v7 row 134
F_SCRIBE_KGIE_FAIL: Final[str] = "F-SCRIBE-KGIE-FAIL"                # §0.5 v7 row 135


# ---------------------------------------------------------------------------
# Timezone-aware datetime wrapper (§7.3 + §7.4 offset-aware pin)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class DateTimeWithTimezone:
    """Wrapper around :class:`datetime.datetime` that refuses naive inputs.

    §7.3 pins ``deadline: DateTimeWithTimezone`` as offset-aware. Using a
    wrapper type documents the invariant at the type layer and catches
    ``datetime.utcnow()``-without-tz bugs at construction time rather than
    when a downstream consumer compares tz-aware vs tz-naive values (which
    raises ``TypeError`` at a less informative site).
    """

    datetime: datetime

    def __post_init__(self) -> None:
        if self.datetime.tzinfo is None:
            raise ValueError(
                "DateTimeWithTimezone requires an offset-aware datetime "
                "(datetime.tzinfo is None). §7.3 pin."
            )


# ---------------------------------------------------------------------------
# §7.3 Phase 0 — RfaExtractedRecord and its nested shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class MatchRequirement:
    """§7.3 match-requirement sub-shape: ratio + cash/in-kind + allowable sources."""

    ratio_applicant_to_federal: Decimal  # e.g. Decimal("1.0") = 1:1 match
    cash_vs_in_kind: Literal["cash", "in_kind", "either", "mix"]
    allowable_sources: tuple[str, ...]


@dataclass(frozen=True, kw_only=True, slots=True)
class EvaluationCriterion:
    """§7.3 one entry per criterion the RFA's rubric pins."""

    criterion_name: str
    max_points: int
    sub_criteria: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.max_points < 0:
            raise ValueError(
                f"EvaluationCriterion.max_points must be >= 0; got "
                f"{self.max_points!r} for {self.criterion_name!r}."
            )
        if not self.criterion_name.strip():
            raise ValueError("EvaluationCriterion.criterion_name is empty.")


@dataclass(frozen=True, kw_only=True, slots=True)
class SectionSpec:
    """§7.3 one entry per RFA-required section: name + limits + content cues."""

    section_name: str
    section_order: int
    limit_kind: Literal["words", "characters", "pages", "none"] = "none"
    limit_value: int | None = None
    required_content_cues: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.section_order < 1:
            raise ValueError(
                f"SectionSpec.section_order must be >= 1; got {self.section_order!r}."
            )
        if self.limit_kind == "none":
            if self.limit_value is not None:
                raise ValueError(
                    "SectionSpec.limit_value must be None when limit_kind == 'none'."
                )
        else:
            if self.limit_value is None or self.limit_value <= 0:
                raise ValueError(
                    f"SectionSpec.limit_value must be a positive int when "
                    f"limit_kind={self.limit_kind!r}; got {self.limit_value!r}."
                )


_SHA3_512_HEX_LEN: Final[int] = 128
_HEX_CHARS: Final[frozenset[str]] = frozenset("0123456789abcdef")


def _is_lowercase_hex(s: str) -> bool:
    return len(s) > 0 and all(ch in _HEX_CHARS for ch in s)


@dataclass(frozen=True, kw_only=True, slots=True)
class RfaExtractedRecord:
    """§7.3 Phase 0 output — RFA content flattened into a verifiable shape.

    At v0.1 the record is operator-hand-populated (extractor is v0.2
    roadmap). At LOCK the shape is fixed; downstream consumers (R2 drafting,
    R3 subprocess entry, Logician PRE-gate) rely on every invariant below.
    """

    program_name: str
    cfda_or_aln: str | None
    eligible_applicant_types: tuple[str, ...]
    eligible_project_activities: tuple[str, ...]
    award_ceiling: Decimal | None
    award_floor: Decimal | None
    match_requirement: MatchRequirement | None
    deadline: DateTimeWithTimezone
    evaluation_criteria: tuple[EvaluationCriterion, ...]
    section_structure: tuple[SectionSpec, ...]
    required_attachments: tuple[str, ...]
    key_terms: Mapping[str, str]
    rfa_content_sha3_512: str
    extracted_at_utc: datetime

    def __post_init__(self) -> None:
        if not self.program_name.strip():
            raise ValueError("RfaExtractedRecord.program_name is empty.")
        if len(self.rfa_content_sha3_512) != _SHA3_512_HEX_LEN:
            raise ValueError(
                f"RfaExtractedRecord.rfa_content_sha3_512 must be "
                f"{_SHA3_512_HEX_LEN} hex chars (full SHA-3-512); got "
                f"{len(self.rfa_content_sha3_512)!r}."
            )
        if not _is_lowercase_hex(self.rfa_content_sha3_512):
            raise ValueError(
                "RfaExtractedRecord.rfa_content_sha3_512 must be lowercase hex "
                "per §2 vault canonical-bytes discipline."
            )
        if self.extracted_at_utc.tzinfo is None:
            raise ValueError(
                "RfaExtractedRecord.extracted_at_utc must be timezone-aware."
            )
        if (
            self.award_ceiling is not None
            and self.award_floor is not None
            and self.award_ceiling < self.award_floor
        ):
            raise ValueError(
                f"RfaExtractedRecord.award_ceiling ({self.award_ceiling}) "
                f"< award_floor ({self.award_floor})."
            )
        # Freeze key_terms mapping into a MappingProxy if a plain dict was
        # passed — prevents downstream mutation.
        if not isinstance(self.key_terms, MappingProxyType):
            # Frozen dataclass: use object.__setattr__ to replace.
            object.__setattr__(
                self, "key_terms", MappingProxyType(dict(self.key_terms))
            )


# ---------------------------------------------------------------------------
# §7.4 KGIE — KgiePreflightResult and its nested shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class KeywordCheck:
    """§7.4 K — one entry per RFA key_term."""

    term: str
    applicant_affirmation: KeywordAffirmation
    source: str | None  # source_field_in_project_context when affirmed; else None
    na_reason: str | None = None  # required when affirmation == "not_applicable_with_reason"

    def __post_init__(self) -> None:
        if self.applicant_affirmation not in _KEYWORD_AFFIRMATION_VALID:
            raise ValueError(
                f"KeywordCheck.applicant_affirmation must be one of "
                f"{sorted(_KEYWORD_AFFIRMATION_VALID)}; got "
                f"{self.applicant_affirmation!r}."
            )
        if self.applicant_affirmation == "affirmed" and not (
            self.source and self.source.strip()
        ):
            raise ValueError(
                f"KeywordCheck({self.term!r}): affirmed entries require a "
                f"non-empty source pointer."
            )
        if self.applicant_affirmation == "not_applicable_with_reason" and not (
            self.na_reason and self.na_reason.strip()
        ):
            raise ValueError(
                f"KeywordCheck({self.term!r}): 'not_applicable_with_reason' "
                f"requires a non-empty na_reason."
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class GeographyRecord:
    """§7.4 G — state, county, zones, Justice40, rfa-match boolean."""

    state: str  # USPS 2-letter code
    county: str
    zone_tags: tuple[str, ...]
    justice40_tract: str | None
    rfa_geographic_match: bool

    def __post_init__(self) -> None:
        if len(self.state) != 2 or not self.state.isalpha() or not self.state.isupper():
            raise ValueError(
                f"GeographyRecord.state must be a 2-letter uppercase USPS code; "
                f"got {self.state!r}."
            )
        if not self.county.strip():
            raise ValueError("GeographyRecord.county is empty.")


@dataclass(frozen=True, kw_only=True, slots=True)
class IdentityClaim:
    """§7.4 I — one entry per SDA / BIPOC / women-led / etc. claim.

    Blueprint §7.4 + §7.2 Law 5: every claim must trace to an affirmative
    applicant statement. Empty ``source_field_in_project_context`` is a
    Law-5 violation and fails KGIE.
    """

    claim: str
    source_field_in_project_context: str
    rfa_priority_points: int

    def __post_init__(self) -> None:
        if not self.claim.strip():
            raise ValueError("IdentityClaim.claim is empty.")
        if self.rfa_priority_points < 0:
            raise ValueError(
                f"IdentityClaim.rfa_priority_points must be >= 0; got "
                f"{self.rfa_priority_points!r}."
            )
        # source_field_in_project_context can be empty — KGIE predicate flags
        # that at status-dispatch time, NOT at construction. A missing source
        # is test-fixture-important data, not a shape bug.


@dataclass(frozen=True, kw_only=True, slots=True)
class ExperienceSummary:
    """§7.4 E — years, production, prior grants, certifications, partnerships."""

    years_operating: int
    production_metrics: Mapping[str, str]
    prior_grants: tuple[str, ...]
    certifications: tuple[str, ...]
    partnerships: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.years_operating < 0:
            raise ValueError(
                f"ExperienceSummary.years_operating must be >= 0; got "
                f"{self.years_operating!r}."
            )
        if not isinstance(self.production_metrics, MappingProxyType):
            object.__setattr__(
                self,
                "production_metrics",
                MappingProxyType(dict(self.production_metrics)),
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class KgiePreflightResult:
    """§7.4 KGIE preflight output — four dimensions + tri-state + needed fields.

    ``status`` is dispatched by :func:`pipeline.seats.scribe.kgie.kgie_preflight`
    based on aggregated evidence: any unanswered affirmation → needs_input;
    any identity without source / any E critical gap / geography no-match →
    fail; otherwise pass.
    """

    status: KgieStatus
    keywords_checked: tuple[KeywordCheck, ...]
    geography_verified: GeographyRecord
    identity_claims: tuple[IdentityClaim, ...]
    experience_summary: ExperienceSummary
    needed_fields: tuple[str, ...]
    preflight_at_utc: datetime

    def __post_init__(self) -> None:
        if self.status not in _KGIE_STATUS_VALID:
            raise ValueError(
                f"KgiePreflightResult.status must be one of "
                f"{sorted(_KGIE_STATUS_VALID)}; got {self.status!r}."
            )
        if self.preflight_at_utc.tzinfo is None:
            raise ValueError(
                "KgiePreflightResult.preflight_at_utc must be timezone-aware."
            )
        if self.status == "pass":
            if self.needed_fields != ():
                raise ValueError(
                    f"KgiePreflightResult(status='pass') cannot carry "
                    f"needed_fields; got {self.needed_fields!r}."
                )
            for claim in self.identity_claims:
                if not claim.source_field_in_project_context.strip():
                    raise ValueError(
                        f"KgiePreflightResult(status='pass') has identity "
                        f"claim {claim.claim!r} with empty source_field — "
                        f"§7.2 Law 5 violation."
                    )
            if not self.geography_verified.rfa_geographic_match:
                raise ValueError(
                    "KgiePreflightResult(status='pass') requires "
                    "geography_verified.rfa_geographic_match == True."
                )
        elif self.status == "needs_operator_input":
            if len(self.needed_fields) < 1:
                raise ValueError(
                    "KgiePreflightResult(status='needs_operator_input') "
                    "requires at least one entry in needed_fields."
                )
        # status == "fail": no invariant on needed_fields; FAIL can be the
        # dispatch outcome when evidence is present but invalid.


__all__ = [
    # Phase 0 shapes
    "RfaExtractedRecord",
    "MatchRequirement",
    "EvaluationCriterion",
    "SectionSpec",
    "DateTimeWithTimezone",
    # KGIE shapes
    "KgiePreflightResult",
    "KgieStatus",
    "KeywordAffirmation",
    "KeywordCheck",
    "GeographyRecord",
    "IdentityClaim",
    "ExperienceSummary",
    # Failure-code constants (§7.13)
    "F_SCRIBE_RFA_MISSING",
    "F_SCRIBE_RFA_DRIFT",
    "F_SCRIBE_PHASE_0_MISSING",
    "F_SCRIBE_KGIE_FAIL",
]
