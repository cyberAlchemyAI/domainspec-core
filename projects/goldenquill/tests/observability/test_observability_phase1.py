"""Phase 1 observability tests — §9.36–§9.40 plus adversarial coverage.

Blueprint §5 v6 §9.36–§9.40 LOCKED 2026-04-19.
"""

from __future__ import annotations

import datetime
import pytest

from pipeline.observability import (
    InvocationRecord,
    INVOCATION_RECORD_SCHEMA_VERSION,
    STRWindow,
    STRWindowResult,
    compute_str,
    STR_WINDOW_MIN_SESSIONS,
    STR_WINDOW_MAX_AGE_DAYS,
)
from pipeline.observability._record import InvocationRecord as _InvocationRecord


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_record(**overrides) -> InvocationRecord:
    defaults = dict(
        run_id="run-001",
        seat="scribe",
        timestamp="2026-04-19T12:00:00Z",
        model_family_resolved="claude",
        token_count_input=100,
        token_count_output=50,
        success_flag=1,
        latency_ms=300,
    )
    defaults.update(overrides)
    return InvocationRecord(**defaults)


def _make_window_with_sessions(n: int, ref_date: datetime.date) -> STRWindow:
    w = STRWindow(seat="scribe")
    for i in range(n):
        w.add_session(
            session_id=f"sess-{i}",
            session_date=ref_date,
            str_values=[0.5, 0.8, 1.0],
        )
    return w


# ---------------------------------------------------------------------------
# §9.36 — InvocationRecord isolation invariant
# ---------------------------------------------------------------------------

class TestInvocationRecordIsolation:
    """§9.36: InvocationRecord must never appear in SubmissionBundle or CalibrationReport."""

    def test_invocation_record_not_in_submission_bundle(self):
        # Structural proxy test: §5.7.2 forbids InvocationRecord inside
        # SubmissionBundle or CalibrationReport. SubmissionBundle does not exist
        # in v0.1, so this test verifies the negative: no bundle-attachment API
        # exists on the record. The true invariant (attempt-to-bundle rejection)
        # must be tested when SubmissionBundle is implemented.
        rec = _make_record()
        assert not hasattr(rec, "to_bundle")
        assert not hasattr(rec, "to_submission")
        assert not hasattr(rec, "to_calibration_report")

    def test_invocation_record_is_frozen(self):
        rec = _make_record()
        with pytest.raises((AttributeError, TypeError)):
            rec.success_flag = 0  # type: ignore[misc]

    def test_schema_version_constant(self):
        assert INVOCATION_RECORD_SCHEMA_VERSION == 1

    def test_schema_version_constant_is_one(self):
        # The module-load assert fires at import time (not testable at runtime
        # without reimport tricks). This test verifies the constant value is
        # still 1, which is the precondition the assert guards.
        import pipeline.observability._record as mod
        assert mod.INVOCATION_RECORD_SCHEMA_VERSION == 1


# ---------------------------------------------------------------------------
# §9.37 — compute_str: zero token sum returns None
# ---------------------------------------------------------------------------

class TestComputeStrZeroTokenSum:
    """§9.37: compute_str returns None when token_count_input + token_count_output == 0."""

    def test_both_zero(self):
        assert compute_str(1, 0, 0) is None

    def test_input_zero_output_zero_failure(self):
        assert compute_str(0, 0, 0) is None

    def test_success_flag_zero_both_zero(self):
        result = compute_str(0, 0, 0)
        assert result is None


# ---------------------------------------------------------------------------
# §9.38 — compute_str: basic ratio
# ---------------------------------------------------------------------------

class TestComputeStrBasicRatio:
    """§9.38: compute_str returns success_flag / (input + output)."""

    def test_success_ratio(self):
        result = compute_str(1, 100, 50)
        assert result == pytest.approx(1 / 150)

    def test_failure_ratio_is_zero(self):
        result = compute_str(0, 100, 50)
        assert result == pytest.approx(0.0)

    def test_result_in_unit_interval_success(self):
        result = compute_str(1, 500, 500)
        assert result is not None
        assert 0.0 <= result <= 1.0

    def test_result_in_unit_interval_failure(self):
        result = compute_str(0, 1, 999)
        assert result is not None
        assert 0.0 <= result <= 1.0

    def test_only_input_tokens(self):
        result = compute_str(1, 200, 0)
        assert result == pytest.approx(1 / 200)

    def test_only_output_tokens(self):
        result = compute_str(1, 0, 400)
        assert result == pytest.approx(1 / 400)

    def test_single_token_success(self):
        assert compute_str(1, 1, 0) == pytest.approx(1.0)

    def test_single_token_failure(self):
        assert compute_str(0, 1, 0) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# §9.39 — STRWindow: below MIN_SESSIONS returns None
# ---------------------------------------------------------------------------

class TestSTRWindowBelowMinSessions:
    """§9.39: query() returns None when fewer than STR_WINDOW_MIN_SESSIONS live sessions."""

    def test_empty_window_returns_none(self):
        w = STRWindow(seat="scribe")
        assert w.query(datetime.date(2026, 4, 19)) is None

    def test_one_below_threshold_returns_none(self):
        ref = datetime.date(2026, 4, 19)
        w = _make_window_with_sessions(STR_WINDOW_MIN_SESSIONS - 1, ref)
        assert w.query(ref) is None

    def test_exactly_min_sessions_returns_result(self):
        ref = datetime.date(2026, 4, 19)
        w = _make_window_with_sessions(STR_WINDOW_MIN_SESSIONS, ref)
        result = w.query(ref)
        assert result is not None

    def test_stale_eviction_drops_below_threshold(self):
        ref = datetime.date(2026, 4, 19)
        old = ref - datetime.timedelta(days=STR_WINDOW_MAX_AGE_DAYS + 1)
        w = STRWindow(seat="scribe")
        for i in range(STR_WINDOW_MIN_SESSIONS):
            w.add_session(f"sess-{i}", old, [0.5])
        # All sessions are stale; eviction should drop below threshold.
        assert w.query(ref) is None

    def test_partial_eviction_can_drop_below_threshold(self):
        ref = datetime.date(2026, 4, 19)
        old = ref - datetime.timedelta(days=STR_WINDOW_MAX_AGE_DAYS + 1)
        w = STRWindow(seat="scribe")
        # 4 stale + 1 live = 5 total, but only 1 live after eviction
        for i in range(4):
            w.add_session(f"old-{i}", old, [0.5])
        w.add_session("live-0", ref, [0.5])
        assert w.query(ref) is None

    def test_min_sessions_constant_is_five(self):
        assert STR_WINDOW_MIN_SESSIONS == 5

    def test_max_age_days_constant_is_thirty(self):
        assert STR_WINDOW_MAX_AGE_DAYS == 30


# ---------------------------------------------------------------------------
# §9.40 — STRWindow: quantile output shape
# ---------------------------------------------------------------------------

class TestSTRWindowQuantileOutputShape:
    """§9.40: query() result has correct TypedDict shape with required quantile keys."""

    REQUIRED_QUANTILE_KEYS = {"min", "p10", "p25", "p50", "p75", "p90", "max"}

    def test_quantile_keys_present(self):
        ref = datetime.date(2026, 4, 19)
        w = _make_window_with_sessions(STR_WINDOW_MIN_SESSIONS, ref)
        result = w.query(ref)
        assert result is not None
        assert set(result["quantiles"].keys()) == self.REQUIRED_QUANTILE_KEYS

    def test_quantile_values_are_floats(self):
        ref = datetime.date(2026, 4, 19)
        w = _make_window_with_sessions(STR_WINDOW_MIN_SESSIONS, ref)
        result = w.query(ref)
        assert result is not None
        for k, v in result["quantiles"].items():
            assert isinstance(v, float), f"quantile {k!r} should be float, got {type(v)}"

    def test_result_fields_present(self):
        ref = datetime.date(2026, 4, 19)
        w = _make_window_with_sessions(STR_WINDOW_MIN_SESSIONS, ref)
        result = w.query(ref)
        assert result is not None
        assert result["seat"] == "scribe"
        assert result["n_sessions"] == STR_WINDOW_MIN_SESSIONS
        assert result["n_invocations"] == STR_WINDOW_MIN_SESSIONS * 3

    def test_quantile_ordering(self):
        ref = datetime.date(2026, 4, 19)
        w = _make_window_with_sessions(STR_WINDOW_MIN_SESSIONS, ref)
        result = w.query(ref)
        assert result is not None
        q = result["quantiles"]
        assert q["min"] <= q["p10"] <= q["p25"] <= q["p50"] <= q["p75"] <= q["p90"] <= q["max"]

    def test_quantile_values_in_unit_interval(self):
        ref = datetime.date(2026, 4, 19)
        w = _make_window_with_sessions(STR_WINDOW_MIN_SESSIONS, ref)
        result = w.query(ref)
        assert result is not None
        for k, v in result["quantiles"].items():
            assert 0.0 <= v <= 1.0, f"quantile {k!r}={v} out of [0,1]"


# ---------------------------------------------------------------------------
# Adversarial / edge-case tests (Da Vinci §8 step 6)
# ---------------------------------------------------------------------------

class TestInvocationRecordValidation:
    """Adversarial: invalid field values must raise ValueError."""

    def test_success_flag_invalid(self):
        with pytest.raises(ValueError, match="success_flag"):
            _make_record(success_flag=2)

    def test_success_flag_negative(self):
        with pytest.raises(ValueError, match="success_flag"):
            _make_record(success_flag=-1)

    def test_token_count_input_negative(self):
        with pytest.raises(ValueError, match="token_count_input"):
            _make_record(token_count_input=-1)

    def test_token_count_output_negative(self):
        with pytest.raises(ValueError, match="token_count_output"):
            _make_record(token_count_output=-1)

    def test_latency_ms_negative(self):
        with pytest.raises(ValueError, match="latency_ms"):
            _make_record(latency_ms=-1)

    def test_run_id_empty(self):
        with pytest.raises(ValueError, match="run_id"):
            _make_record(run_id="")

    def test_seat_empty(self):
        with pytest.raises(ValueError, match="seat"):
            _make_record(seat="")

    def test_timestamp_empty(self):
        with pytest.raises(ValueError, match="timestamp"):
            _make_record(timestamp="")

    def test_model_family_resolved_empty(self):
        with pytest.raises(ValueError, match="model_family_resolved"):
            _make_record(model_family_resolved="")

    def test_valid_success_flag_zero(self):
        rec = _make_record(success_flag=0)
        assert rec.success_flag == 0

    def test_valid_success_flag_one(self):
        rec = _make_record(success_flag=1)
        assert rec.success_flag == 1

    def test_valid_zero_tokens_allowed(self):
        rec = _make_record(token_count_input=0, token_count_output=0)
        assert rec.token_count_input == 0
        assert rec.token_count_output == 0


class TestSTRWindowAdversarial:
    """Adversarial: edge cases in session management and eviction."""

    def test_add_session_filters_none_values(self):
        ref = datetime.date(2026, 4, 19)
        w = STRWindow(seat="judge")
        w.add_session("s1", ref, [None, None, None])
        # All None — no defined values stored; n_invocations should be 0.
        # But below threshold anyway, so query returns None.
        assert w.query(ref) is None

    def test_window_with_all_none_values_above_session_threshold_returns_none(self):
        ref = datetime.date(2026, 4, 19)
        w = STRWindow(seat="judge")
        for i in range(STR_WINDOW_MIN_SESSIONS):
            w.add_session(f"s{i}", ref, [None, None])
        # all_values will be empty → query returns None
        assert w.query(ref) is None

    def test_cutoff_boundary_inclusive(self):
        ref = datetime.date(2026, 4, 19)
        cutoff = ref - datetime.timedelta(days=STR_WINDOW_MAX_AGE_DAYS)
        w = STRWindow(seat="scribe")
        for i in range(STR_WINDOW_MIN_SESSIONS):
            w.add_session(f"s{i}", cutoff, [0.5, 1.0])
        # Exactly on the cutoff date — should NOT be evicted (>= cutoff).
        result = w.query(ref)
        assert result is not None

    def test_cutoff_boundary_just_outside(self):
        ref = datetime.date(2026, 4, 19)
        just_old = ref - datetime.timedelta(days=STR_WINDOW_MAX_AGE_DAYS + 1)
        w = STRWindow(seat="scribe")
        for i in range(STR_WINDOW_MIN_SESSIONS):
            w.add_session(f"s{i}", just_old, [0.5, 1.0])
        assert w.query(ref) is None

    def test_eviction_is_in_place(self):
        ref = datetime.date(2026, 4, 19)
        old = ref - datetime.timedelta(days=STR_WINDOW_MAX_AGE_DAYS + 1)
        w = STRWindow(seat="scribe")
        for i in range(STR_WINDOW_MIN_SESSIONS):
            w.add_session(f"old-{i}", old, [0.5])
        for i in range(STR_WINDOW_MIN_SESSIONS):
            w.add_session(f"live-{i}", ref, [0.5])
        # After first query, stale sessions are evicted permanently.
        w.query(ref)
        result = w.query(ref)
        assert result is not None
        assert result["n_sessions"] == STR_WINDOW_MIN_SESSIONS

    def test_default_reference_date_uses_today(self, monkeypatch):
        import pipeline.observability._str_window as mod
        fixed_today = datetime.date(2026, 4, 19)
        monkeypatch.setattr(mod.datetime, "date", type("_D", (), {
            "today": staticmethod(lambda: fixed_today),
            "__new__": datetime.date.__new__,
        }))
        # Just verifies no TypeError — reference_date=None path executes.
        w = STRWindow(seat="scribe")
        result = w.query(reference_date=None)
        assert result is None  # empty window

    def test_raw_sessions_for_canary_returns_list(self):
        ref = datetime.date(2026, 4, 19)
        w = STRWindow(seat="scribe")
        w.add_session("s1", ref, [0.5, 1.0])
        raw = w._raw_sessions_for_canary()
        assert isinstance(raw, list)
        assert len(raw) == 1
        sid, sdate, vals = raw[0]
        assert sid == "s1"
        assert sdate == ref
        assert vals == [0.5, 1.0]

    def test_single_value_quantiles(self):
        ref = datetime.date(2026, 4, 19)
        w = STRWindow(seat="scribe")
        for i in range(STR_WINDOW_MIN_SESSIONS):
            w.add_session(f"s{i}", ref, [0.5])
        result = w.query(ref)
        assert result is not None
        q = result["quantiles"]
        # All values identical → all quantiles equal.
        assert q["min"] == q["p50"] == q["max"] == pytest.approx(0.5)

    def test_single_total_value_across_all_sessions(self):
        # Covers percentile() n==1 fast-path (line 142).
        ref = datetime.date(2026, 4, 19)
        w = STRWindow(seat="scribe")
        # 4 sessions with no values (all None filtered), 1 session with 1 value.
        for i in range(STR_WINDOW_MIN_SESSIONS - 1):
            w.add_session(f"empty-{i}", ref, [None, None])
        w.add_session("one-value", ref, [0.75])
        result = w.query(ref)
        assert result is not None
        q = result["quantiles"]
        assert q["min"] == q["p10"] == q["p50"] == q["p90"] == q["max"] == pytest.approx(0.75)

    def test_large_session_count(self):
        ref = datetime.date(2026, 4, 19)
        w = _make_window_with_sessions(100, ref)
        result = w.query(ref)
        assert result is not None
        assert result["n_sessions"] == 100

    def test_seat_name_preserved_in_result(self):
        ref = datetime.date(2026, 4, 19)
        w = STRWindow(seat="judge")
        for i in range(STR_WINDOW_MIN_SESSIONS):
            w.add_session(f"s{i}", ref, [1.0])
        result = w.query(ref)
        assert result is not None
        assert result["seat"] == "judge"

    def test_mixed_live_and_stale_sessions(self):
        ref = datetime.date(2026, 4, 19)
        old = ref - datetime.timedelta(days=STR_WINDOW_MAX_AGE_DAYS + 1)
        w = STRWindow(seat="scribe")
        # 3 stale + 5 live = 5 live after eviction
        for i in range(3):
            w.add_session(f"old-{i}", old, [0.1])
        for i in range(5):
            w.add_session(f"live-{i}", ref, [0.9, 1.0])
        result = w.query(ref)
        assert result is not None
        assert result["n_sessions"] == 5
        assert result["n_invocations"] == 10


class TestSTRWindowResultType:
    """Verify STRWindowResult is exported and has the right keys."""

    def test_str_window_result_is_typed_dict(self):
        from typing import get_type_hints
        hints = get_type_hints(STRWindowResult)
        assert "seat" in hints
        assert "n_sessions" in hints
        assert "n_invocations" in hints
        assert "quantiles" in hints
