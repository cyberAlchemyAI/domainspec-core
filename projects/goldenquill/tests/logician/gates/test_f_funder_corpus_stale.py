"""Unit tests for F-FUNDER-CORPUS-STALE (POST-cite, P2).

Per architecture v7.0.5 §5.6.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from pipeline.logician.gates.f_funder_corpus_stale import (
    DEFAULT_STALE_THRESHOLD_DAYS,
    F_FUNDER_CORPUS_STALE,
    FUNDER_TYPE_STALE_THRESHOLD_DAYS,
    check_funder_corpus_stale,
)


class _FixedClock:
    def __init__(self, t: datetime) -> None:
        self._t = t

    def now(self) -> datetime:
        return self._t


def test_failure_code_constant() -> None:
    assert F_FUNDER_CORPUS_STALE == "F-FUNDER-CORPUS-STALE"


def test_fresh_federal_doc_passes() -> None:
    now = datetime(2026, 5, 10, tzinfo=timezone.utc)
    r = check_funder_corpus_stale(
        funder_type="federal_agency",
        last_relevance_event=now - timedelta(days=100),
        clock=_FixedClock(now),
    )
    assert r.success is True
    assert r.threshold_days == 365


def test_stale_federal_doc_fails() -> None:
    now = datetime(2026, 5, 10, tzinfo=timezone.utc)
    r = check_funder_corpus_stale(
        funder_type="federal_agency",
        last_relevance_event=now - timedelta(days=400),
        clock=_FixedClock(now),
    )
    assert r.success is False
    assert r.failure_code == F_FUNDER_CORPUS_STALE
    assert r.age_days == 400


def test_corporate_giving_tighter_threshold() -> None:
    # corporate_giving threshold is 90 days
    now = datetime(2026, 5, 10, tzinfo=timezone.utc)
    r = check_funder_corpus_stale(
        funder_type="corporate_giving",
        last_relevance_event=now - timedelta(days=100),
        clock=_FixedClock(now),
    )
    assert r.success is False
    assert r.failure_code == F_FUNDER_CORPUS_STALE
    assert r.threshold_days == 90


def test_private_foundation_180_threshold() -> None:
    now = datetime(2026, 5, 10, tzinfo=timezone.utc)
    r = check_funder_corpus_stale(
        funder_type="private_foundation",
        last_relevance_event=now - timedelta(days=170),
        clock=_FixedClock(now),
    )
    assert r.success is True
    assert r.threshold_days == 180


def test_unknown_funder_type_uses_conservative_default() -> None:
    now = datetime(2026, 5, 10, tzinfo=timezone.utc)
    r = check_funder_corpus_stale(
        funder_type="unrecognized_type",
        last_relevance_event=now - timedelta(days=100),
        clock=_FixedClock(now),
    )
    assert r.success is False
    assert r.threshold_days == DEFAULT_STALE_THRESHOLD_DAYS  # 90


def test_expiry_override_takes_precedence() -> None:
    now = datetime(2026, 5, 10, tzinfo=timezone.utc)
    r = check_funder_corpus_stale(
        funder_type="federal_agency",  # default 365
        last_relevance_event=now - timedelta(days=400),
        clock=_FixedClock(now),
        expiry_override_days=730,  # operator override to 2-year window
    )
    assert r.success is True
    assert r.threshold_days == 730


def test_naive_datetime_treated_as_utc() -> None:
    now = datetime(2026, 5, 10, tzinfo=timezone.utc)
    naive = datetime(2026, 4, 1)  # no tzinfo
    r = check_funder_corpus_stale(
        funder_type="federal_agency",
        last_relevance_event=naive,
        clock=_FixedClock(now),
    )
    assert r.success is True


def test_default_clock_uses_real_now() -> None:
    # Without clock, gate uses datetime.now(timezone.utc); test runs against
    # a very recent timestamp to ensure the path resolves.
    very_recent = datetime.now(timezone.utc) - timedelta(seconds=1)
    r = check_funder_corpus_stale(
        funder_type="federal_agency",
        last_relevance_event=very_recent,
    )
    assert r.success is True


def test_funder_type_threshold_table_complete() -> None:
    # Sanity check: all canonical funder_type values per v7.0.5 §5.6 are
    # registered in the threshold table.
    expected_types = {
        "federal_agency",
        "regional_authority",
        "state_agency",
        "private_foundation",
        "community_foundation",
        "corporate_giving",
        "cdfi",
        "county",
        "city",
    }
    assert expected_types.issubset(set(FUNDER_TYPE_STALE_THRESHOLD_DAYS.keys()))
