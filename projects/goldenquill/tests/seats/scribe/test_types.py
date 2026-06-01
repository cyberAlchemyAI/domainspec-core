"""Tests for pipeline.seats.scribe.types — R1 shape invariants + failure codes.

Blueprint §7 Scribe v1.1.1 LOCKED 2026-04-21. Spec card:
`pipeline/engineering/spec_cards/section_07_scribe_round_1_types_and_kgie.md`.

Covers:
- DateTimeWithTimezone naive-refusal.
- MatchRequirement / EvaluationCriterion / SectionSpec construction + invariants.
- RfaExtractedRecord sha hex length + tz awareness + ceiling/floor + key_terms freeze.
- KeywordCheck affirmed requires source / NA requires reason / enum closed-set.
- GeographyRecord USPS 2-letter + non-empty county.
- IdentityClaim allows empty source (KGIE dispatch data).
- ExperienceSummary non-negative years + production_metrics freeze.
- KgiePreflightResult tri-state + pass/needs_input invariants + tz awareness.
- F_SCRIBE_* failure-code string constants match §0.5 v7 rows 132-135.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from decimal import Decimal
from types import MappingProxyType

import pytest

from pipeline.seats.scribe.types import (
    DateTimeWithTimezone,
    EvaluationCriterion,
    ExperienceSummary,
    F_SCRIBE_KGIE_FAIL,
    F_SCRIBE_PHASE_0_MISSING,
    F_SCRIBE_RFA_DRIFT,
    F_SCRIBE_RFA_MISSING,
    GeographyRecord,
    IdentityClaim,
    KeywordCheck,
    KgiePreflightResult,
    MatchRequirement,
    RfaExtractedRecord,
    SectionSpec,
)


UTC_NOW = datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)
SHA_128_A = "a" * 128
SHA_128_MIX = ("0123456789abcdef" * 8)  # 128 hex chars
SHA_128_UPPER = "A" * 128


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mk_geography(**overrides) -> GeographyRecord:
    kwargs = dict(
        state="PA",
        county="Centre",
        zone_tags=("Opportunity Zone",),
        justice40_tract="42027011800",
        rfa_geographic_match=True,
    )
    kwargs.update(overrides)
    return GeographyRecord(**kwargs)


def _mk_experience(**overrides) -> ExperienceSummary:
    kwargs = dict(
        years_operating=3,
        production_metrics={"mushrooms_lb_yr": "12000"},
        prior_grants=("2024-VAPG-Planning",),
        certifications=("USDA-Organic",),
        partnerships=("Penn State Extension",),
    )
    kwargs.update(overrides)
    return ExperienceSummary(**kwargs)


def _mk_identity(**overrides) -> IdentityClaim:
    kwargs = dict(
        claim="socially-disadvantaged",
        source_field_in_project_context="demographics.sda_affirmation",
        rfa_priority_points=5,
    )
    kwargs.update(overrides)
    return IdentityClaim(**kwargs)


def _mk_keyword_check(**overrides) -> KeywordCheck:
    kwargs = dict(
        term="specialty crops",
        applicant_affirmation="affirmed",
        source="PROJECT_CONTEXT:operations.crops",
        na_reason=None,
    )
    kwargs.update(overrides)
    return KeywordCheck(**kwargs)


def _mk_kgie_result(**overrides) -> KgiePreflightResult:
    kwargs = dict(
        status="pass",
        keywords_checked=(_mk_keyword_check(),),
        geography_verified=_mk_geography(),
        identity_claims=(_mk_identity(),),
        experience_summary=_mk_experience(),
        needed_fields=(),
        preflight_at_utc=UTC_NOW,
    )
    kwargs.update(overrides)
    return KgiePreflightResult(**kwargs)


def _mk_rfa(**overrides) -> RfaExtractedRecord:
    kwargs = dict(
        program_name="VAPG FY26",
        cfda_or_aln="10.352",
        eligible_applicant_types=("Agricultural producers",),
        eligible_project_activities=("Value-added processing",),
        award_ceiling=Decimal("250000"),
        award_floor=Decimal("50000"),
        match_requirement=MatchRequirement(
            ratio_applicant_to_federal=Decimal("1.0"),
            cash_vs_in_kind="either",
            allowable_sources=("cash on hand",),
        ),
        deadline=DateTimeWithTimezone(
            datetime=datetime(2026, 10, 1, 17, 0, tzinfo=timezone.utc)
        ),
        evaluation_criteria=(
            EvaluationCriterion(
                criterion_name="Project Feasibility",
                max_points=25,
                sub_criteria=("Labor plan", "Financial plan"),
            ),
        ),
        section_structure=(
            SectionSpec(
                section_name="Executive Summary",
                section_order=1,
                limit_kind="words",
                limit_value=500,
                required_content_cues=("mission",),
            ),
        ),
        required_attachments=("Form SF-424",),
        key_terms={"specialty_crops": "RFA page 4"},
        rfa_content_sha3_512=SHA_128_A,
        extracted_at_utc=UTC_NOW,
    )
    kwargs.update(overrides)
    return RfaExtractedRecord(**kwargs)


# ---------------------------------------------------------------------------
# DateTimeWithTimezone
# ---------------------------------------------------------------------------


class TestDateTimeWithTimezone:
    def test_accepts_tz_aware(self):
        d = DateTimeWithTimezone(datetime=UTC_NOW)
        assert d.datetime == UTC_NOW

    def test_rejects_naive(self):
        naive = datetime(2026, 4, 21, 12, 0, 0)
        with pytest.raises(ValueError, match="offset-aware"):
            DateTimeWithTimezone(datetime=naive)

    def test_non_utc_tz_accepted(self):
        tz_est = timezone(timedelta(hours=-5))
        d = DateTimeWithTimezone(datetime=datetime(2026, 4, 21, 7, 0, tzinfo=tz_est))
        assert d.datetime.tzinfo is tz_est

    def test_is_frozen(self):
        d = DateTimeWithTimezone(datetime=UTC_NOW)
        with pytest.raises((AttributeError, Exception)):
            d.datetime = UTC_NOW  # type: ignore[misc]


# ---------------------------------------------------------------------------
# MatchRequirement / EvaluationCriterion / SectionSpec
# ---------------------------------------------------------------------------


class TestMatchRequirement:
    def test_construction(self):
        m = MatchRequirement(
            ratio_applicant_to_federal=Decimal("1.0"),
            cash_vs_in_kind="cash",
            allowable_sources=("grant funds",),
        )
        assert m.cash_vs_in_kind == "cash"
        assert m.allowable_sources == ("grant funds",)


class TestEvaluationCriterion:
    def test_construction(self):
        c = EvaluationCriterion(criterion_name="Impact", max_points=30)
        assert c.max_points == 30
        assert c.sub_criteria == ()

    def test_negative_points_rejected(self):
        with pytest.raises(ValueError, match=">= 0"):
            EvaluationCriterion(criterion_name="Impact", max_points=-1)

    def test_empty_name_rejected(self):
        with pytest.raises(ValueError, match="criterion_name"):
            EvaluationCriterion(criterion_name="   ", max_points=10)

    def test_zero_points_allowed(self):
        # §7.3 does not preclude a zero-point informational criterion.
        c = EvaluationCriterion(criterion_name="Notes", max_points=0)
        assert c.max_points == 0


class TestSectionSpec:
    def test_none_limit_no_value(self):
        s = SectionSpec(section_name="Intro", section_order=1)
        assert s.limit_kind == "none"
        assert s.limit_value is None

    def test_none_limit_with_value_rejected(self):
        with pytest.raises(ValueError, match="limit_value must be None"):
            SectionSpec(section_name="Intro", section_order=1, limit_value=100)

    def test_words_limit_requires_positive(self):
        with pytest.raises(ValueError, match="positive int"):
            SectionSpec(
                section_name="Intro",
                section_order=1,
                limit_kind="words",
                limit_value=0,
            )

    def test_order_must_be_positive(self):
        with pytest.raises(ValueError, match="section_order"):
            SectionSpec(section_name="Intro", section_order=0)

    def test_valid_words(self):
        s = SectionSpec(
            section_name="Impact",
            section_order=2,
            limit_kind="words",
            limit_value=500,
        )
        assert s.limit_value == 500


# ---------------------------------------------------------------------------
# RfaExtractedRecord
# ---------------------------------------------------------------------------


class TestRfaExtractedRecord:
    def test_happy_path(self):
        rfa = _mk_rfa()
        assert rfa.program_name == "VAPG FY26"
        # key_terms was dict input → should be frozen into MappingProxyType
        assert isinstance(rfa.key_terms, MappingProxyType)

    def test_empty_program_name(self):
        with pytest.raises(ValueError, match="program_name"):
            _mk_rfa(program_name=" ")

    def test_sha_wrong_length(self):
        with pytest.raises(ValueError, match="128 hex chars"):
            _mk_rfa(rfa_content_sha3_512="a" * 127)

    def test_sha_uppercase_rejected(self):
        with pytest.raises(ValueError, match="lowercase hex"):
            _mk_rfa(rfa_content_sha3_512=SHA_128_UPPER)

    def test_sha_non_hex_chars_rejected(self):
        bad = "z" * 128
        with pytest.raises(ValueError, match="lowercase hex"):
            _mk_rfa(rfa_content_sha3_512=bad)

    def test_naive_extracted_at_rejected(self):
        naive = datetime(2026, 4, 21, 12, 0, 0)
        with pytest.raises(ValueError, match="timezone-aware"):
            _mk_rfa(extracted_at_utc=naive)

    def test_ceiling_below_floor_rejected(self):
        with pytest.raises(ValueError, match="< award_floor"):
            _mk_rfa(
                award_ceiling=Decimal("10000"),
                award_floor=Decimal("50000"),
            )

    def test_ceiling_equal_floor_allowed(self):
        # ceiling == floor is a legal fixed-amount grant.
        rfa = _mk_rfa(
            award_ceiling=Decimal("50000"),
            award_floor=Decimal("50000"),
        )
        assert rfa.award_ceiling == rfa.award_floor

    def test_missing_ceiling_or_floor_skips_check(self):
        rfa = _mk_rfa(award_ceiling=None, award_floor=Decimal("50000"))
        assert rfa.award_ceiling is None

    def test_key_terms_already_frozen_passed_through(self):
        frozen = MappingProxyType({"x": "y"})
        rfa = _mk_rfa(key_terms=frozen)
        # Same object when already a proxy — no re-wrap.
        assert rfa.key_terms is frozen


# ---------------------------------------------------------------------------
# KeywordCheck
# ---------------------------------------------------------------------------


class TestKeywordCheck:
    def test_affirmed_requires_source(self):
        with pytest.raises(ValueError, match="non-empty source"):
            KeywordCheck(
                term="specialty crops",
                applicant_affirmation="affirmed",
                source=None,
            )

    def test_affirmed_empty_source_rejected(self):
        with pytest.raises(ValueError, match="non-empty source"):
            _mk_keyword_check(source="   ")

    def test_na_requires_reason(self):
        with pytest.raises(ValueError, match="na_reason"):
            KeywordCheck(
                term="specialty crops",
                applicant_affirmation="not_applicable_with_reason",
                source=None,
                na_reason=None,
            )

    def test_unanswered_allows_null_source(self):
        c = KeywordCheck(
            term="specialty crops",
            applicant_affirmation="unanswered",
            source=None,
        )
        assert c.source is None

    def test_unknown_affirmation_rejected(self):
        with pytest.raises(ValueError, match="applicant_affirmation"):
            KeywordCheck(
                term="x",
                applicant_affirmation="yeah_probably",  # type: ignore[arg-type]
                source=None,
            )


# ---------------------------------------------------------------------------
# GeographyRecord
# ---------------------------------------------------------------------------


class TestGeographyRecord:
    def test_happy_path(self):
        g = _mk_geography()
        assert g.state == "PA"

    def test_non_usps_state_rejected(self):
        with pytest.raises(ValueError, match="USPS"):
            _mk_geography(state="PAX")

    def test_lowercase_state_rejected(self):
        with pytest.raises(ValueError, match="USPS"):
            _mk_geography(state="pa")

    def test_empty_county_rejected(self):
        with pytest.raises(ValueError, match="county"):
            _mk_geography(county="   ")

    def test_no_justice40_tract_allowed(self):
        g = _mk_geography(justice40_tract=None)
        assert g.justice40_tract is None


# ---------------------------------------------------------------------------
# IdentityClaim
# ---------------------------------------------------------------------------


class TestIdentityClaim:
    def test_happy_path(self):
        c = _mk_identity()
        assert c.rfa_priority_points == 5

    def test_empty_claim_rejected(self):
        with pytest.raises(ValueError, match="claim"):
            _mk_identity(claim="   ")

    def test_negative_priority_points_rejected(self):
        with pytest.raises(ValueError, match="rfa_priority_points"):
            _mk_identity(rfa_priority_points=-1)

    def test_empty_source_field_allowed_at_construction(self):
        # §7.4 discipline: empty source_field is KGIE-dispatch data, not a
        # shape bug. kgie_preflight flags it into FAIL at status time.
        c = _mk_identity(source_field_in_project_context="")
        assert c.source_field_in_project_context == ""


# ---------------------------------------------------------------------------
# ExperienceSummary
# ---------------------------------------------------------------------------


class TestExperienceSummary:
    def test_happy_path(self):
        e = _mk_experience()
        assert e.years_operating == 3
        assert isinstance(e.production_metrics, MappingProxyType)

    def test_negative_years_rejected(self):
        with pytest.raises(ValueError, match="years_operating"):
            _mk_experience(years_operating=-1)

    def test_zero_years_allowed(self):
        e = _mk_experience(years_operating=0)
        assert e.years_operating == 0

    def test_production_metrics_frozen(self):
        e = _mk_experience()
        with pytest.raises(TypeError):
            e.production_metrics["new"] = "value"  # type: ignore[index]


# ---------------------------------------------------------------------------
# KgiePreflightResult
# ---------------------------------------------------------------------------


class TestKgiePreflightResult:
    def test_pass_happy_path(self):
        r = _mk_kgie_result()
        assert r.status == "pass"

    def test_pass_cannot_have_needed_fields(self):
        with pytest.raises(ValueError, match="pass.*needed_fields"):
            _mk_kgie_result(needed_fields=("kgie.K:foo",))

    def test_pass_requires_identity_source(self):
        with pytest.raises(ValueError, match="Law 5"):
            _mk_kgie_result(
                identity_claims=(_mk_identity(source_field_in_project_context=""),),
            )

    def test_pass_requires_geographic_match(self):
        with pytest.raises(ValueError, match="rfa_geographic_match"):
            _mk_kgie_result(
                geography_verified=_mk_geography(rfa_geographic_match=False),
            )

    def test_needs_operator_input_requires_at_least_one_field(self):
        with pytest.raises(ValueError, match="needed_fields"):
            _mk_kgie_result(status="needs_operator_input", needed_fields=())

    def test_needs_operator_input_happy_path(self):
        r = _mk_kgie_result(
            status="needs_operator_input",
            needed_fields=("kgie.G:state",),
            geography_verified=_mk_geography(rfa_geographic_match=False),
        )
        assert r.status == "needs_operator_input"

    def test_fail_unconstrained(self):
        # FAIL is the catch-all; needed_fields may be empty and identity-source
        # may be missing without invariant violations.
        r = _mk_kgie_result(
            status="fail",
            needed_fields=(),
            identity_claims=(_mk_identity(source_field_in_project_context=""),),
            geography_verified=_mk_geography(rfa_geographic_match=False),
        )
        assert r.status == "fail"

    def test_unknown_status_rejected(self):
        with pytest.raises(ValueError, match="status"):
            _mk_kgie_result(status="maybe")  # type: ignore[arg-type]

    def test_naive_preflight_at_rejected(self):
        naive = datetime(2026, 4, 21, 12, 0, 0)
        with pytest.raises(ValueError, match="timezone-aware"):
            _mk_kgie_result(preflight_at_utc=naive)


# ---------------------------------------------------------------------------
# Failure-code string constants (§7.13 / §0.5 v7 rows 132-135)
# ---------------------------------------------------------------------------


class TestFailureCodeStrings:
    def test_rfa_missing_spelling(self):
        assert F_SCRIBE_RFA_MISSING == "F-SCRIBE-RFA-MISSING"

    def test_rfa_drift_spelling(self):
        assert F_SCRIBE_RFA_DRIFT == "F-SCRIBE-RFA-DRIFT"

    def test_phase_0_missing_spelling(self):
        assert F_SCRIBE_PHASE_0_MISSING == "F-SCRIBE-PHASE-0-MISSING"

    def test_kgie_fail_spelling(self):
        assert F_SCRIBE_KGIE_FAIL == "F-SCRIBE-KGIE-FAIL"

    def test_all_codes_distinct(self):
        codes = {
            F_SCRIBE_RFA_MISSING,
            F_SCRIBE_RFA_DRIFT,
            F_SCRIBE_PHASE_0_MISSING,
            F_SCRIBE_KGIE_FAIL,
        }
        assert len(codes) == 4
