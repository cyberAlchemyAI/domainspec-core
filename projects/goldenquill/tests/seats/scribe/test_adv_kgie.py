"""Adversarial + property-style tests for pipeline.seats.scribe.kgie.

Blueprint §7 Scribe v1.1.1 LOCKED 2026-04-21. Spec card:
`pipeline/engineering/spec_cards/section_07_scribe_round_1_types_and_kgie.md`.

Hand-rolled randomized tests (hypothesis not installed in the .venv; the
§1 Round J precedent uses random-seeded iteration instead). Plus a set of
adversarial malformed-input tests that assert the predicate never raises.
"""

from __future__ import annotations

import random
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from pipeline.seats.scribe.kgie import kgie_preflight
from pipeline.seats.scribe.types import (
    DateTimeWithTimezone,
    EvaluationCriterion,
    KgiePreflightResult,
    MatchRequirement,
    RfaExtractedRecord,
    SectionSpec,
)


CLOCK = datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)
SHA_128 = "f" * 128


def _fixed_clock() -> datetime:
    return CLOCK


def _mk_rfa(*, key_terms=None) -> RfaExtractedRecord:
    return RfaExtractedRecord(
        program_name="Some Program",
        cfda_or_aln="10.352",
        eligible_applicant_types=("x",),
        eligible_project_activities=("y",),
        award_ceiling=Decimal("100000"),
        award_floor=Decimal("1000"),
        match_requirement=None,
        deadline=DateTimeWithTimezone(
            datetime=datetime(2027, 1, 1, tzinfo=timezone.utc)
        ),
        evaluation_criteria=(EvaluationCriterion(criterion_name="A", max_points=10),),
        section_structure=(SectionSpec(section_name="Intro", section_order=1),),
        required_attachments=(),
        key_terms=(key_terms if key_terms is not None else {}),
        rfa_content_sha3_512=SHA_128,
        extracted_at_utc=CLOCK,
    )


def _happy_context() -> dict:
    return {
        "location": {
            "state": "PA",
            "county": "Centre",
            "zone_tags": (),
            "justice40_tract": None,
        },
        "rfa_geographic_match": True,
        "identity_affirmations": [],
        "experience": {
            "years_operating": 5,
            "production_metrics": {},
            "certifications": ("USDA-Organic",),
            "partnerships": (),
        },
        "prior_grants": (),
    }


# ---------------------------------------------------------------------------
# Property-style: status closed-set and return-type invariants
# ---------------------------------------------------------------------------


class TestStatusClosedSet:
    """Across many randomized inputs the result is always well-formed."""

    @pytest.mark.parametrize("seed", list(range(20)))
    def test_status_always_in_closed_set(self, seed: int):
        rng = random.Random(seed)
        rfa = _mk_rfa(
            key_terms={f"term_{i}": f"p.{i}" for i in range(rng.randint(0, 4))}
        )
        pc = _happy_context()
        # Randomize a few dimensions.
        pc["rfa_geographic_match"] = rng.choice([True, False])
        if rng.random() < 0.5:
            pc["location"].pop("state", None)
        if rng.random() < 0.3:
            pc["identity_affirmations"] = [
                {
                    "claim": "SDA",
                    "source_field": rng.choice(["demo.sda", ""]),
                    "rfa_priority_points": rng.randint(0, 10),
                }
            ]
        affirmations = {
            term: rng.choice(["affirmed", "not_applicable_with_reason", "unanswered"])
            for term in rfa.key_terms
        }
        r = kgie_preflight(rfa, pc, affirmations, clock=_fixed_clock)
        assert isinstance(r, KgiePreflightResult)
        assert r.status in {"pass", "fail", "needs_operator_input"}
        assert r.preflight_at_utc == CLOCK

    @pytest.mark.parametrize("seed", list(range(20)))
    def test_keyword_checks_length_matches_rfa_key_terms(self, seed: int):
        rng = random.Random(seed)
        n = rng.randint(0, 5)
        key_terms = {f"t_{i}": f"p.{i}" for i in range(n)}
        rfa = _mk_rfa(key_terms=key_terms)
        pc = _happy_context()
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert len(r.keywords_checked) == n

    @pytest.mark.parametrize("seed", list(range(10)))
    def test_needs_input_implies_nonempty_needed_fields(self, seed: int):
        rng = random.Random(seed)
        rfa = _mk_rfa(key_terms={"x": "p.1"})
        pc = _happy_context()
        # Force at least one dimension to be unanswered with some probability.
        if rng.random() < 0.5:
            pc["location"].pop("county", None)
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        if r.status == "needs_operator_input":
            assert len(r.needed_fields) >= 1

    @pytest.mark.parametrize("seed", list(range(10)))
    def test_pass_implies_empty_needed_fields(self, seed: int):
        # Construction invariant already checks this, but exercise the
        # predicate dispatch to ensure it never emits PASS with needed.
        rng = random.Random(seed)
        n = rng.randint(0, 3)
        rfa = _mk_rfa(key_terms={f"t_{i}": f"p.{i}" for i in range(n)})
        pc = _happy_context()
        affirmations = {f"t_{i}": "affirmed" for i in range(n)}
        r = kgie_preflight(rfa, pc, affirmations, clock=_fixed_clock)
        if r.status == "pass":
            assert r.needed_fields == ()

    def test_determinism_under_fixed_clock(self):
        """Same inputs + same clock → byte-identical result."""
        rfa = _mk_rfa(key_terms={"x": "p.1"})
        pc = _happy_context()
        r1 = kgie_preflight(rfa, pc, {"x": "affirmed"}, clock=_fixed_clock)
        r2 = kgie_preflight(rfa, pc, {"x": "affirmed"}, clock=_fixed_clock)
        assert r1 == r2

    def test_default_clock_produces_tz_aware(self):
        rfa = _mk_rfa()
        pc = _happy_context()
        r = kgie_preflight(rfa, pc, {})
        assert r.preflight_at_utc.tzinfo is not None


# ---------------------------------------------------------------------------
# Adversarial — predicate never raises on malformed data
# ---------------------------------------------------------------------------


class TestKgieAdversarial:
    def test_list_location_accepted(self):
        rfa = _mk_rfa()
        pc = _happy_context()
        pc["location"] = ["not", "a", "mapping"]
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert r.status == "needs_operator_input"

    def test_zone_tags_as_string_coerced_empty(self):
        rfa = _mk_rfa()
        pc = _happy_context()
        pc["location"]["zone_tags"] = "OZ"  # wrong: should be tuple
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert r.geography_verified.zone_tags == ()

    def test_prior_grants_as_int_coerced_empty(self):
        rfa = _mk_rfa()
        pc = _happy_context()
        pc["prior_grants"] = 42  # wrong type
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert r.experience_summary.prior_grants == ()

    def test_identity_affirmations_not_list_returns_empty(self):
        rfa = _mk_rfa()
        pc = _happy_context()
        pc["identity_affirmations"] = "SDA"  # wrong type
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert r.identity_claims == ()

    def test_non_mapping_identity_entry_skipped(self):
        rfa = _mk_rfa()
        pc = _happy_context()
        pc["identity_affirmations"] = [
            "SDA-claim-as-string",
            {"claim": "BIPOC", "source_field": "demo.bipoc", "rfa_priority_points": 3},
        ]
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert len(r.identity_claims) == 1
        assert r.identity_claims[0].claim == "BIPOC"

    def test_keyword_sources_not_mapping_falls_through(self):
        rfa = _mk_rfa(key_terms={"x": "p.1"})
        pc = _happy_context()
        pc["keyword_sources"] = "not-a-dict"
        r = kgie_preflight(rfa, pc, {"x": "affirmed"}, clock=_fixed_clock)
        # Falls through to synthetic trace anchor.
        assert r.keywords_checked[0].source == "PROJECT_CONTEXT:keyword_sources:x"

    def test_keyword_na_reasons_not_mapping_degrades_to_unanswered(self):
        rfa = _mk_rfa(key_terms={"x": "p.1"})
        pc = _happy_context()
        pc["keyword_na_reasons"] = ["list", "not", "mapping"]
        r = kgie_preflight(
            rfa, pc, {"x": "not_applicable_with_reason"}, clock=_fixed_clock
        )
        assert r.status == "needs_operator_input"

    def test_integer_keyword_term_ignored_gracefully(self):
        # RFA must be validly constructed (str:str), but affirmations map
        # can contain strings not present in RFA.
        rfa = _mk_rfa(key_terms={"x": "p.1"})
        pc = _happy_context()
        r = kgie_preflight(
            rfa,
            pc,
            {"x": "affirmed", "y_not_in_rfa": "affirmed"},
            clock=_fixed_clock,
        )
        # Only the x check exists; extra map key ignored.
        assert len(r.keywords_checked) == 1

    def test_years_operating_float_truncated(self):
        rfa = _mk_rfa()
        pc = _happy_context()
        pc["experience"]["years_operating"] = 7.9
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert r.experience_summary.years_operating == 7

    def test_massive_key_terms_dict_handled(self):
        rfa = _mk_rfa(key_terms={f"t_{i}": f"p.{i}" for i in range(200)})
        pc = _happy_context()
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert len(r.keywords_checked) == 200
        assert r.status == "needs_operator_input"

    def test_no_raise_on_none_project_context_fields(self):
        rfa = _mk_rfa()
        pc = {
            "location": None,
            "rfa_geographic_match": None,
            "identity_affirmations": None,
            "experience": None,
            "prior_grants": None,
        }
        # Must not raise; must return a well-formed KgiePreflightResult.
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert isinstance(r, KgiePreflightResult)

    def test_negative_years_operating_clamped_to_zero(self):
        rfa = _mk_rfa()
        pc = _happy_context()
        pc["experience"]["years_operating"] = -3
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert r.experience_summary.years_operating == 0

    def test_production_metrics_non_mapping_coerced_empty(self):
        rfa = _mk_rfa()
        pc = _happy_context()
        pc["experience"]["production_metrics"] = ["list", "not", "mapping"]
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert dict(r.experience_summary.production_metrics) == {}

    def test_production_metrics_non_string_values_coerced(self):
        rfa = _mk_rfa()
        pc = _happy_context()
        pc["experience"]["production_metrics"] = {"lbs": 12000, "acres": 5.5}
        r = kgie_preflight(rfa, pc, {}, clock=_fixed_clock)
        assert r.experience_summary.production_metrics["lbs"] == "12000"
        assert r.experience_summary.production_metrics["acres"] == "5.5"
