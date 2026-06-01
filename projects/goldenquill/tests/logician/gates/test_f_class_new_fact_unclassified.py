"""Unit tests for F-CLASS-NEW-FACT-UNCLASSIFIED (PRE per-cycle)."""

from __future__ import annotations

from pipeline.logician.gates.f_class_new_fact_unclassified import (
    CLASS_CONFIDENTIAL,
    F_CLASS_NEW_FACT_UNCLASSIFIED,
    IncrementalFact,
    PENDING_OPERATOR_REVIEW,
    check_class_new_fact_unclassified,
)


def test_failure_code_constant() -> None:
    assert F_CLASS_NEW_FACT_UNCLASSIFIED == "F-CLASS-NEW-FACT-UNCLASSIFIED"


def test_pending_review_constant() -> None:
    assert PENDING_OPERATOR_REVIEW == "pending_operator_review"


def test_no_facts_passes() -> None:
    r = check_class_new_fact_unclassified(facts=[])
    assert r.success is True


def test_classified_consumed_fact_passes() -> None:
    r = check_class_new_fact_unclassified(
        facts=[
            IncrementalFact(
                fact_id="fact_001",
                class_name=CLASS_CONFIDENTIAL,
                locked_by="operator_signed",
                will_be_consumed_this_cycle=True,
            ),
        ],
    )
    assert r.success is True


def test_pending_review_consumed_fact_fails() -> None:
    r = check_class_new_fact_unclassified(
        facts=[
            IncrementalFact(
                fact_id="fact_002",
                class_name=CLASS_CONFIDENTIAL,
                locked_by=PENDING_OPERATOR_REVIEW,
                will_be_consumed_this_cycle=True,
            ),
        ],
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_NEW_FACT_UNCLASSIFIED
    assert "fact_002" in r.detail


def test_pending_review_NOT_consumed_passes() -> None:
    r = check_class_new_fact_unclassified(
        facts=[
            IncrementalFact(
                fact_id="fact_003",
                class_name=CLASS_CONFIDENTIAL,
                locked_by=PENDING_OPERATOR_REVIEW,
                will_be_consumed_this_cycle=False,
            ),
        ],
    )
    assert r.success is True


def test_pending_review_non_confidential_passes() -> None:
    # Per §3.6 step 1, the default for new facts is confidential. A
    # non-confidential pending fact is an inconsistent state but not
    # itself a leak — caller's classification register check covers it.
    r = check_class_new_fact_unclassified(
        facts=[
            IncrementalFact(
                fact_id="fact_x",
                class_name="public",
                locked_by=PENDING_OPERATOR_REVIEW,
                will_be_consumed_this_cycle=True,
            ),
        ],
    )
    assert r.success is True


def test_multiple_blocked_facts_collected() -> None:
    r = check_class_new_fact_unclassified(
        facts=[
            IncrementalFact(
                fact_id=f"fact_{i:03d}",
                class_name=CLASS_CONFIDENTIAL,
                locked_by=PENDING_OPERATOR_REVIEW,
                will_be_consumed_this_cycle=True,
            )
            for i in range(10)
        ],
    )
    assert r.success is False
    # First five surfaced; total reported in detail.
    assert len(r.blocked_fact_ids) == 5
    assert "+5 more" in r.detail


def test_partial_consumption_only_consumed_blocked() -> None:
    r = check_class_new_fact_unclassified(
        facts=[
            IncrementalFact(
                fact_id="consumed_pending",
                class_name=CLASS_CONFIDENTIAL,
                locked_by=PENDING_OPERATOR_REVIEW,
                will_be_consumed_this_cycle=True,
            ),
            IncrementalFact(
                fact_id="not_consumed_pending",
                class_name=CLASS_CONFIDENTIAL,
                locked_by=PENDING_OPERATOR_REVIEW,
                will_be_consumed_this_cycle=False,
            ),
            IncrementalFact(
                fact_id="consumed_signed",
                class_name=CLASS_CONFIDENTIAL,
                locked_by="operator_signed",
                will_be_consumed_this_cycle=True,
            ),
        ],
    )
    assert r.success is False
    assert r.blocked_fact_ids == ("consumed_pending",)
