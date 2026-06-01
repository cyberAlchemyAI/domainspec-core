"""Tests for pipeline.seats.scribe.smart — §7.6 SMART + numeric-verbatim."""

from __future__ import annotations

import pytest

from pipeline.seats.scribe.smart import (
    VIOLATION_MISSING_ACHIEVABILITY,
    VIOLATION_MISSING_MEASUREMENT,
    VIOLATION_MISSING_OBJECTIVE,
    VIOLATION_MISSING_OUTCOME,
    VIOLATION_MISSING_TIMELINE,
    VIOLATION_NO_RELEVANCE_POINTER,
    SmartObjective,
    check_numeric_verbatim,
    extract_numeric_tokens,
    validate_smart_objective,
)


# ---------------------------------------------------------------------------
# SmartObjective shape
# ---------------------------------------------------------------------------


def _mk_valid_smart(**overrides: object) -> SmartObjective:
    defaults: dict[str, object] = dict(
        objective_text="Increase specialty-crop throughput 25%",
        outcome_text="Five county farms onboarded to cooperative packhouse",
        measurement_text="Pounds throughput logged via packhouse ERP monthly",
        timeline_text="Q1 2027 through Q4 2028",
        achievability_evidence="Packhouse commissioned 2026; 3 farms under MOU",
        relevance_pointer=("criterion_project_merit",),
    )
    defaults.update(overrides)
    return SmartObjective(**defaults)  # type: ignore[arg-type]


class TestSmartObjectiveShape:
    def test_happy_path_constructs(self) -> None:
        obj = _mk_valid_smart()
        assert obj.objective_text.startswith("Increase")
        assert obj.relevance_pointer == ("criterion_project_merit",)

    def test_is_frozen(self) -> None:
        obj = _mk_valid_smart()
        with pytest.raises(Exception):
            obj.objective_text = "mutated"  # type: ignore[misc]

    def test_empty_objective_rejected(self) -> None:
        with pytest.raises(ValueError, match="objective_text"):
            _mk_valid_smart(objective_text="")

    def test_whitespace_outcome_rejected(self) -> None:
        with pytest.raises(ValueError, match="outcome_text"):
            _mk_valid_smart(outcome_text="   ")

    def test_empty_measurement_rejected(self) -> None:
        with pytest.raises(ValueError, match="measurement_text"):
            _mk_valid_smart(measurement_text="")

    def test_empty_timeline_rejected(self) -> None:
        with pytest.raises(ValueError, match="timeline_text"):
            _mk_valid_smart(timeline_text="")

    def test_empty_achievability_rejected(self) -> None:
        with pytest.raises(ValueError, match="achievability_evidence"):
            _mk_valid_smart(achievability_evidence="")

    def test_non_str_objective_rejected(self) -> None:
        with pytest.raises(ValueError, match="objective_text"):
            _mk_valid_smart(objective_text=123)  # type: ignore[arg-type]

    def test_relevance_pointer_default_empty(self) -> None:
        obj = SmartObjective(
            objective_text="o",
            outcome_text="out",
            measurement_text="m",
            timeline_text="t",
            achievability_evidence="a",
        )
        assert obj.relevance_pointer == ()


# ---------------------------------------------------------------------------
# validate_smart_objective
# ---------------------------------------------------------------------------


class TestValidateSmartObjective:
    def test_valid_with_pointer_returns_empty(self) -> None:
        obj = _mk_valid_smart()
        assert validate_smart_objective(obj) == ()

    def test_no_pointer_triggers_violation(self) -> None:
        obj = _mk_valid_smart(relevance_pointer=())
        violations = validate_smart_objective(obj)
        assert violations == (VIOLATION_NO_RELEVANCE_POINTER,)

    def test_multiple_pointers_pass(self) -> None:
        obj = _mk_valid_smart(
            relevance_pointer=("criterion_a", "criterion_b", "criterion_c"),
        )
        assert validate_smart_objective(obj) == ()

    def test_bypassed_empty_objective_detected(self) -> None:
        obj = _mk_valid_smart()
        object.__setattr__(obj, "objective_text", "")
        violations = validate_smart_objective(obj)
        assert VIOLATION_MISSING_OBJECTIVE in violations

    def test_bypassed_empty_outcome_detected(self) -> None:
        obj = _mk_valid_smart()
        object.__setattr__(obj, "outcome_text", "   ")
        violations = validate_smart_objective(obj)
        assert VIOLATION_MISSING_OUTCOME in violations

    def test_bypassed_empty_measurement_detected(self) -> None:
        obj = _mk_valid_smart()
        object.__setattr__(obj, "measurement_text", "")
        violations = validate_smart_objective(obj)
        assert VIOLATION_MISSING_MEASUREMENT in violations

    def test_bypassed_empty_timeline_detected(self) -> None:
        obj = _mk_valid_smart()
        object.__setattr__(obj, "timeline_text", "")
        violations = validate_smart_objective(obj)
        assert VIOLATION_MISSING_TIMELINE in violations

    def test_bypassed_empty_achievability_detected(self) -> None:
        obj = _mk_valid_smart()
        object.__setattr__(obj, "achievability_evidence", "")
        violations = validate_smart_objective(obj)
        assert VIOLATION_MISSING_ACHIEVABILITY in violations

    def test_all_bypassed_gives_all_codes(self) -> None:
        obj = _mk_valid_smart()
        for f in (
            "objective_text",
            "outcome_text",
            "measurement_text",
            "timeline_text",
            "achievability_evidence",
        ):
            object.__setattr__(obj, f, "")
        object.__setattr__(obj, "relevance_pointer", ())
        violations = validate_smart_objective(obj)
        assert len(violations) == 6
        assert VIOLATION_MISSING_OBJECTIVE in violations
        assert VIOLATION_NO_RELEVANCE_POINTER in violations


# ---------------------------------------------------------------------------
# extract_numeric_tokens
# ---------------------------------------------------------------------------


class TestExtractNumericTokens:
    def test_empty_text(self) -> None:
        assert extract_numeric_tokens("") == ()

    def test_non_string_input(self) -> None:
        assert extract_numeric_tokens(None) == ()  # type: ignore[arg-type]

    def test_no_numbers(self) -> None:
        assert extract_numeric_tokens("alpha beta gamma delta") == ()

    def test_money_with_commas(self) -> None:
        assert extract_numeric_tokens("We ask for $1,200,000") == ("1200000",)

    def test_money_no_commas(self) -> None:
        assert extract_numeric_tokens("$500 line item") == ("500",)

    def test_money_with_decimal(self) -> None:
        assert extract_numeric_tokens("$12.50 each") == ("12.50",)

    def test_percent_integer(self) -> None:
        assert extract_numeric_tokens("75% match") == ("75",)

    def test_percent_decimal(self) -> None:
        assert extract_numeric_tokens("23.5% growth") == ("23.5",)

    def test_decimal_bare(self) -> None:
        assert extract_numeric_tokens("grew 2.5 tons") == ("2.5",)

    def test_integer_with_commas_bare(self) -> None:
        assert extract_numeric_tokens("12,000 pounds") == ("12000",)

    def test_integer_bare(self) -> None:
        assert extract_numeric_tokens("We have 3 farms") == ("3",)

    def test_mixed_document_order_preserved(self) -> None:
        text = "We ask for $1,200 over 3 years to support 75% of 12 farms."
        tokens = extract_numeric_tokens(text)
        assert tokens == ("1200", "3", "75", "12")

    def test_duplicate_tokens_preserved(self) -> None:
        text = "$100 one time, then another $100 later, $100 always"
        assert extract_numeric_tokens(text) == ("100", "100", "100")

    def test_money_does_not_double_count_integer(self) -> None:
        # The "12" inside "$12.50" must not produce a second "12".
        assert extract_numeric_tokens("$12.50 only") == ("12.50",)

    def test_percent_does_not_double_count_integer(self) -> None:
        assert extract_numeric_tokens("75% alone") == ("75",)


# ---------------------------------------------------------------------------
# check_numeric_verbatim
# ---------------------------------------------------------------------------


class TestCheckNumericVerbatim:
    def test_empty_claim_returns_empty(self) -> None:
        assert check_numeric_verbatim("", "evidence $100") == ()

    def test_all_tokens_match(self) -> None:
        claim = "We ask $1,200 for 3 years"
        evidence = "Budget: $1,200 over 3 years of operation"
        assert check_numeric_verbatim(claim, evidence) == ()

    def test_missing_token_returned(self) -> None:
        claim = "We ask $1,200 for 5 years"
        evidence = "Budget: $1,200 over 3 years"
        assert check_numeric_verbatim(claim, evidence) == ("5",)

    def test_missing_money_returned(self) -> None:
        claim = "We need $999"
        evidence = "Budget: $1,200"
        assert check_numeric_verbatim(claim, evidence) == ("999",)

    def test_unit_normalization_passes(self) -> None:
        # $1,200 (claim) should match 1200 (evidence) after canonicalization
        claim = "We ask $1,200"
        evidence = "We have 1200 in the bank"
        assert check_numeric_verbatim(claim, evidence) == ()

    def test_percent_normalization_passes(self) -> None:
        claim = "75% match"
        evidence = "We can commit 75 in matching"
        assert check_numeric_verbatim(claim, evidence) == ()
