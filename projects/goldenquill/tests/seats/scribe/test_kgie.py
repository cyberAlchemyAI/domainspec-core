"""Tests for pipeline.seats.scribe.kgie — KGIE preflight tri-state dispatch.

Blueprint §7 Scribe v1.1.1 §7.4 LOCKED 2026-04-21. Spec card:
`pipeline/engineering/spec_cards/section_07_scribe_round_1_types_and_kgie.md`.

Exercises the PASS / FAIL / NEEDS_OPERATOR_INPUT dispatch under a fixed
clock, plus defensive coercion of malformed project_context data.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import pytest

from pipeline.seats.scribe.kgie import kgie_preflight
from pipeline.seats.scribe.types import (
    DateTimeWithTimezone,
    EvaluationCriterion,
    MatchRequirement,
    RfaExtractedRecord,
    SectionSpec,
)


FIXED_CLOCK_UTC = datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)
SHA_128 = "a" * 128


def _fixed_clock() -> datetime:
    return FIXED_CLOCK_UTC


def _mk_rfa(*, key_terms=None) -> RfaExtractedRecord:
    return RfaExtractedRecord(
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
            EvaluationCriterion(criterion_name="Feasibility", max_points=25),
        ),
        section_structure=(
            SectionSpec(
                section_name="Executive Summary",
                section_order=1,
                limit_kind="words",
                limit_value=500,
            ),
        ),
        required_attachments=("SF-424",),
        key_terms=(key_terms if key_terms is not None else {"specialty_crops": "p.4"}),
        rfa_content_sha3_512=SHA_128,
        extracted_at_utc=FIXED_CLOCK_UTC,
    )


def _happy_project_context() -> dict:
    return {
        "location": {
            "state": "PA",
            "county": "Centre",
            "zone_tags": ("Opportunity Zone",),
            "justice40_tract": "42027011800",
        },
        "rfa_geographic_match": True,
        "identity_affirmations": [
            {
                "claim": "socially-disadvantaged",
                "source_field": "demographics.sda_affirmation",
                "rfa_priority_points": 5,
            }
        ],
        "experience": {
            "years_operating": 3,
            "production_metrics": {"mushrooms_lb_yr": "12000"},
            "certifications": ("USDA-Organic",),
            "partnerships": ("Penn State Extension",),
        },
        "prior_grants": ("2024-VAPG-Planning",),
        "keyword_sources": {
            "specialty_crops": "PROJECT_CONTEXT:operations.crops",
        },
    }


# ---------------------------------------------------------------------------
# PASS tests (≥4)
# ---------------------------------------------------------------------------


class TestKgiePass:
    def test_minimal_pass(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "pass"
        assert r.needed_fields == ()
        assert r.preflight_at_utc == FIXED_CLOCK_UTC

    def test_pass_uses_default_source_trace_anchor(self):
        # When affirmed but keyword_sources has no entry, a synthetic
        # PROJECT_CONTEXT:keyword_sources:<term> anchor is substituted.
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["keyword_sources"] = {}
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "pass"
        assert r.keywords_checked[0].source == (
            "PROJECT_CONTEXT:keyword_sources:specialty_crops"
        )

    def test_pass_with_not_applicable_with_reason(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["keyword_na_reasons"] = {"specialty_crops": "we grow grains only"}
        r = kgie_preflight(
            rfa,
            pc,
            {"specialty_crops": "not_applicable_with_reason"},
            clock=_fixed_clock,
        )
        assert r.status == "pass"
        assert r.keywords_checked[0].na_reason == "we grow grains only"

    def test_pass_multi_keyterm(self):
        rfa = _mk_rfa(
            key_terms={"specialty_crops": "p.4", "women_owned": "p.7"}
        )
        pc = _happy_project_context()
        pc["keyword_sources"] = {
            "specialty_crops": "PROJECT_CONTEXT:operations.crops",
            "women_owned": "PROJECT_CONTEXT:demographics.owner_demo",
        }
        r = kgie_preflight(
            rfa,
            pc,
            {"specialty_crops": "affirmed", "women_owned": "affirmed"},
            clock=_fixed_clock,
        )
        assert r.status == "pass"
        assert len(r.keywords_checked) == 2


# ---------------------------------------------------------------------------
# NEEDS_OPERATOR_INPUT tests (≥4)
# ---------------------------------------------------------------------------


class TestKgieNeedsOperatorInput:
    def test_unanswered_keyword(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert r.status == "needs_operator_input"
        assert "kgie.K:specialty_crops" in r.needed_fields

    def test_missing_state(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["location"] = {}
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "needs_operator_input"
        assert "kgie.G:state" in r.needed_fields
        assert "kgie.G:county" in r.needed_fields

    def test_missing_rfa_geographic_match_flag(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc.pop("rfa_geographic_match")
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "needs_operator_input"
        assert "kgie.G:rfa_geographic_match" in r.needed_fields

    def test_na_missing_reason_degrades_to_unanswered(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        # Operator said NA but supplied no reason — degrades to unanswered.
        r = kgie_preflight(
            rfa,
            pc,
            {"specialty_crops": "not_applicable_with_reason"},
            clock=_fixed_clock,
        )
        assert r.status == "needs_operator_input"
        assert "kgie.K:specialty_crops" in r.needed_fields

    def test_bad_years_operating_adds_gap(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["experience"]["years_operating"] = "not-a-number"
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "needs_operator_input"
        assert "kgie.E:years_operating" in r.needed_fields


# ---------------------------------------------------------------------------
# FAIL tests (≥6)
# ---------------------------------------------------------------------------


class TestKgieFail:
    def test_identity_claim_missing_source(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["identity_affirmations"] = [
            {"claim": "BIPOC-led", "source_field": "", "rfa_priority_points": 3}
        ]
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "fail"

    def test_experience_critical_gap(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["experience"] = {
            "years_operating": 0,
            "production_metrics": {},
            "certifications": (),
            "partnerships": (),
        }
        pc["prior_grants"] = ()
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "fail"

    def test_rfa_geographic_mismatch(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["rfa_geographic_match"] = False
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "fail"

    def test_experience_gap_saved_by_prior_grants(self):
        # 0 years + no certs + no partners BUT prior grants exist → not critical.
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["experience"] = {
            "years_operating": 0,
            "production_metrics": {},
            "certifications": (),
            "partnerships": (),
        }
        # prior_grants still present → not a critical gap.
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "pass"

    def test_experience_gap_saved_by_certifications(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["experience"] = {
            "years_operating": 0,
            "production_metrics": {},
            "certifications": ("USDA-Organic",),
            "partnerships": (),
        }
        pc["prior_grants"] = ()
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "pass"

    def test_experience_gap_saved_by_partnerships(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["experience"] = {
            "years_operating": 0,
            "production_metrics": {},
            "certifications": (),
            "partnerships": ("Penn State Extension",),
        }
        pc["prior_grants"] = ()
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "pass"

    def test_multiple_identity_claims_any_missing_source(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["identity_affirmations"] = [
            {
                "claim": "SDA",
                "source_field": "demographics.sda",
                "rfa_priority_points": 5,
            },
            {
                "claim": "veteran-led",
                "source_field": "",  # empty → Law 5 gap
                "rfa_priority_points": 3,
            },
        ]
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "fail"


# ---------------------------------------------------------------------------
# Edge cases / defensive coercion
# ---------------------------------------------------------------------------


class TestKgieDefensive:
    def test_unknown_affirmation_coerced_to_unanswered(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "sure_why_not"}, clock=_fixed_clock  # type: ignore[dict-item]
        )
        # Unknown → unanswered → needs_operator_input.
        assert r.status == "needs_operator_input"
        assert "kgie.K:specialty_crops" in r.needed_fields

    def test_missing_identity_affirmations_is_not_a_gap(self):
        # Empty tuple of claims: no Law-5 gap can exist.
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["identity_affirmations"] = []
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "pass"
        assert r.identity_claims == ()

    def test_invalid_state_length_routed_to_needed(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["location"]["state"] = "XXX"
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "needs_operator_input"
        assert "kgie.G:state" in r.needed_fields

    def test_non_mapping_location_handled(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["location"] = "Pennsylvania"  # wrong type
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "needs_operator_input"
        assert "kgie.G:state" in r.needed_fields

    def test_non_mapping_experience_handled(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["experience"] = None
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        # 0 years + no certs + no partners + no prior_grants — but prior_grants
        # still lives at top-level. Depends on fixture: prior_grants=("2024...",)
        # means not critical.
        assert r.status == "pass"

    def test_zero_keyterms_never_needs_input_for_keywords(self):
        rfa = _mk_rfa(key_terms={})
        pc = _happy_project_context()
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert r.status == "pass"
        assert r.keywords_checked == ()

    def test_clock_injection_deterministic(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        later = datetime(2029, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        r = kgie_preflight(
            rfa,
            pc,
            {"specialty_crops": "affirmed"},
            clock=lambda: later,
        )
        assert r.preflight_at_utc == later

    def test_negative_priority_points_coerced_to_zero(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["identity_affirmations"] = [
            {
                "claim": "SDA",
                "source_field": "demographics.sda",
                "rfa_priority_points": -5,  # coerced to 0
            }
        ]
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.identity_claims[0].rfa_priority_points == 0
        assert r.status == "pass"

    def test_bad_priority_points_string_adds_gap(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["identity_affirmations"] = [
            {
                "claim": "SDA",
                "source_field": "demographics.sda",
                "rfa_priority_points": "many",
            }
        ]
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        assert r.status == "needs_operator_input"
        assert any(n.startswith("kgie.I:SDA:priority") for n in r.needed_fields)

    def test_identity_affirmation_missing_claim_skipped(self):
        rfa = _mk_rfa()
        pc = _happy_project_context()
        pc["identity_affirmations"] = [
            {"source_field": "x", "rfa_priority_points": 1},  # no claim
            {"claim": "SDA", "source_field": "demo.sda", "rfa_priority_points": 5},
        ]
        r = kgie_preflight(
            rfa, pc, {"specialty_crops": "affirmed"}, clock=_fixed_clock
        )
        # Entry with no claim is silently dropped.
        assert len(r.identity_claims) == 1
        assert r.status == "pass"

    def test_predicate_never_raises_on_fully_missing_context(self):
        rfa = _mk_rfa()
        r = kgie_preflight(
            rfa, {}, {}, clock=_fixed_clock
        )
        # All gaps surface as needed_fields.
        assert r.status == "needs_operator_input"
        assert "kgie.G:state" in r.needed_fields
        assert "kgie.G:county" in r.needed_fields
