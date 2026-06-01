"""Unit tests for F-COMMITTEE-DEGRADATION-TIMEOUT (F-AMDT-08)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone, timedelta
from typing import Optional

import pytest

from pipeline.logician.gates.f_committee_degradation_timeout import (
    EVENT_CLOCK_SKEW_WARN,
    EVENT_ESCALATE,
    EVENT_READER_FAIL,
    EVENT_SUSPEND,
    EVENT_WARN,
    F_AMDT_08,
    F_AMDT_08_ESCALATE,
    F_AMDT_08_READER_FAIL,
    F_AMDT_08_SUSPEND,
    ESCALATE_THRESHOLD_DAYS,
    SUSPEND_THRESHOLD_DAYS,
    WARN_THRESHOLD_DAYS,
    CommitteeDegradationTimeoutDetail,
    CommitteeDegradationTimeoutResult,
    check_committee_degradation_timeout,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _Clock:
    def __init__(self, now: datetime, *, raises: Optional[BaseException] = None,
                 returns: object = None):
        self._now = now
        self._raises = raises
        self._returns = returns

    def now_utc(self) -> datetime:
        if self._raises is not None:
            raise self._raises
        if self._returns is not None:
            return self._returns  # type: ignore[return-value]
        return self._now


class _LockHistory:
    def __init__(self, rows, *, raises: Optional[BaseException] = None):
        self._rows = rows
        self._raises = raises
        self.calls = 0

    def __call__(self):
        self.calls += 1
        if self._raises is not None:
            raise self._raises
        return self._rows


class _DailyLog:
    def __init__(self, text, *, raises: Optional[BaseException] = None):
        # text may be a dict date_iso->str/None or a simple str/None.
        self._text = text
        self._raises = raises
        self.calls = []

    def __call__(self, date_iso: str):
        self.calls.append(date_iso)
        if self._raises is not None:
            raise self._raises
        if isinstance(self._text, dict):
            return self._text.get(date_iso)
        return self._text


_LOCKED_AT = datetime(2026, 3, 23, 0, 0, 0, tzinfo=timezone.utc)


def _dep_row(*, event_id: str = "en003-kimi-k2-2026-03-23",
             locked_at: str = _LOCKED_AT.isoformat()) -> dict:
    return {
        "module": "pipeline.logician.en003_kimi_k2_event",
        "deprecation_triggered_replacement": True,
        "deprecation_event_id": event_id,
        "lock_timestamp_utc": locked_at,
    }


def _completion_row(event_id: str = "en003-kimi-k2-2026-03-23") -> dict:
    return {
        "module": "pipeline.some.replacement",
        "deprecation_replacement_complete": True,
        "deprecation_event_id": event_id,
        "lock_timestamp_utc": "2026-05-01T00:00:00Z",
    }


def _now_plus(days: int, seconds: int = 0) -> datetime:
    return _LOCKED_AT + timedelta(days=days, seconds=seconds)


# ---------------------------------------------------------------------------
# Baseline — no deprecation / completed
# ---------------------------------------------------------------------------


def test_no_deprecation_rows_passes_noop():
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(365)),
        lock_history_reader=_LockHistory([{"module": "other"}, {"module": "another"}]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "no_deprecation_in_flight"
    assert r.detail.emitted_event == ""
    assert r.detail.deprecation_event_id == ""


def test_empty_lock_history_passes_noop():
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(0)),
        lock_history_reader=_LockHistory([]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "no_deprecation_in_flight"


def test_deprecation_with_completion_passes_noop():
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(365)),
        lock_history_reader=_LockHistory([_dep_row(), _completion_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "no_deprecation_in_flight"


def test_deprecation_with_mismatched_completion_still_in_flight():
    """Completion row exists but references a different deprecation_event_id."""
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(40)),
        lock_history_reader=_LockHistory([
            _dep_row(event_id="en003-kimi-k2-2026-03-23"),
            _completion_row(event_id="en002-some-other-event"),
        ]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_SUSPEND


# ---------------------------------------------------------------------------
# PASS silent (days < WARN)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("days", [0, 1, 7, 13])
def test_days_below_warn_threshold_passes_silent(days):
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(days)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "within_warn_window_silent"
    assert r.detail.emitted_event == ""
    assert r.detail.days_elapsed == days


# ---------------------------------------------------------------------------
# PASS + WARN (days 14..29)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("days", [14, 15, 20, 29])
def test_warn_window_passes_with_warn_event(days):
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(days)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "warn_window_reached"
    assert r.detail.emitted_event == EVENT_WARN
    assert r.detail.days_elapsed == days


# ---------------------------------------------------------------------------
# SUSPEND window (days 30..59)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("days", [30, 31, 45, 59])
def test_suspend_window_no_signoff_denies(days):
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(days)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_SUSPEND
    assert r.detail.emitted_event == EVENT_SUSPEND
    assert r.detail.days_elapsed == days


def test_suspend_window_with_valid_future_signoff_passes_warn():
    now = _now_plus(40)
    today_iso = now.date().isoformat()
    future_iso = (now.date() + timedelta(days=14)).isoformat()
    stanza = (
        f"Operator preamble\n"
        f"F-AMDT-08 acknowledged: deprecation-replacement Thesis commitment target {future_iso}\n"
        f"-- signed --\n"
    )
    r = check_committee_degradation_timeout(
        clock=_Clock(now),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog({today_iso: stanza}),
    )
    assert r.success is True
    assert r.detail.reason_tag == "suspend_window_signoff_passes"
    assert r.detail.emitted_event == EVENT_WARN


def test_suspend_window_signoff_past_date_denies():
    now = _now_plus(35)
    today_iso = now.date().isoformat()
    past_iso = (now.date() - timedelta(days=2)).isoformat()
    stanza = (
        f"F-AMDT-08 acknowledged: deprecation-replacement Thesis commitment target {past_iso}\n"
    )
    r = check_committee_degradation_timeout(
        clock=_Clock(now),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog({today_iso: stanza}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_SUSPEND


def test_suspend_window_signoff_equals_today_denies_strictly_future_required():
    now = _now_plus(35)
    today_iso = now.date().isoformat()
    stanza = (
        f"F-AMDT-08 acknowledged: deprecation-replacement Thesis commitment target {today_iso}\n"
    )
    r = check_committee_degradation_timeout(
        clock=_Clock(now),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog({today_iso: stanza}),
    )
    assert r.success is False


def test_suspend_window_signoff_malformed_date_denies():
    now = _now_plus(35)
    today_iso = now.date().isoformat()
    stanza = "F-AMDT-08 acknowledged: deprecation-replacement Thesis commitment target 99-XYZ\n"
    r = check_committee_degradation_timeout(
        clock=_Clock(now),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog({today_iso: stanza}),
    )
    assert r.success is False


def test_suspend_window_signoff_missing_date_denies():
    now = _now_plus(40)
    today_iso = now.date().isoformat()
    stanza = "F-AMDT-08 acknowledged: deprecation-replacement Thesis commitment target \n"
    r = check_committee_degradation_timeout(
        clock=_Clock(now),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog({today_iso: stanza}),
    )
    assert r.success is False


def test_suspend_window_signoff_wrong_sentinel_prefix_denies():
    now = _now_plus(40)
    today_iso = now.date().isoformat()
    stanza = "F-AMDT-08 understood: deprecation-replacement Thesis commitment target 2099-01-01\n"
    r = check_committee_degradation_timeout(
        clock=_Clock(now),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog({today_iso: stanza}),
    )
    assert r.success is False


def test_suspend_window_daily_log_missing_denies():
    now = _now_plus(40)
    today_iso = now.date().isoformat()
    r = check_committee_degradation_timeout(
        clock=_Clock(now),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog({today_iso: None}),
    )
    assert r.success is False


# ---------------------------------------------------------------------------
# ESCALATE window (days >= 60) — sign-off does NOT clear
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("days", [60, 61, 100, 365])
def test_escalate_window_denies_unconditionally(days):
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(days)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_ESCALATE
    assert r.detail.emitted_event == EVENT_ESCALATE


def test_escalate_window_with_valid_signoff_still_denies():
    now = _now_plus(70)
    today_iso = now.date().isoformat()
    future_iso = (now.date() + timedelta(days=30)).isoformat()
    stanza = (
        f"F-AMDT-08 acknowledged: deprecation-replacement Thesis commitment target {future_iso}\n"
    )
    r = check_committee_degradation_timeout(
        clock=_Clock(now),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog({today_iso: stanza}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_ESCALATE


# ---------------------------------------------------------------------------
# Multiple deprecation rows — most recent wins
# ---------------------------------------------------------------------------


def test_multiple_deprecation_rows_most_recent_wins():
    old = _dep_row(event_id="en001-old", locked_at="2025-01-01T00:00:00Z")
    new = _dep_row(event_id="en003-kimi-k2-2026-03-23")
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(5)),
        lock_history_reader=_LockHistory([old, new]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "within_warn_window_silent"
    assert r.detail.deprecation_event_id == "en003-kimi-k2-2026-03-23"
    assert r.detail.days_elapsed == 5


def test_multiple_deprecations_newest_completed_oldest_still_inflight():
    """Newest deprecation is completed; older one still in flight → gate
    evaluates the older one because the newest is no longer in flight."""
    old = _dep_row(event_id="en001-old", locked_at="2025-01-01T00:00:00Z")
    new = _dep_row(event_id="en003-kimi-k2-2026-03-23")
    comp_new = _completion_row(event_id="en003-kimi-k2-2026-03-23")
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(400)),
        lock_history_reader=_LockHistory([old, new, comp_new]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_ESCALATE
    assert r.detail.deprecation_event_id == "en001-old"


# ---------------------------------------------------------------------------
# Clock-skew carve-out
# ---------------------------------------------------------------------------


def test_clock_skew_negative_days_passes_with_skew_event():
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(-5)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "clock_skew_detected"
    assert r.detail.emitted_event == EVENT_CLOCK_SKEW_WARN
    assert r.detail.days_elapsed == -5


def test_clock_skew_minus_one_day_is_skew_not_silent_pass():
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(0, seconds=-1)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "clock_skew_detected"
    assert r.detail.emitted_event == EVENT_CLOCK_SKEW_WARN


# ---------------------------------------------------------------------------
# Reader failures
# ---------------------------------------------------------------------------


def test_lock_history_reader_raises_fail_closed():
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(10)),
        lock_history_reader=_LockHistory(None, raises=OSError("disk read error")),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "lock_history_reader_raised"
    assert r.detail.emitted_event == EVENT_READER_FAIL
    assert "OSError" in (r.detail.reader_error or "")


def test_lock_history_reader_returns_non_list_fail_closed():
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(10)),
        lock_history_reader=_LockHistory("not-a-list"),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "lock_history_not_list"


def test_clock_raises_fail_closed():
    r = check_committee_degradation_timeout(
        clock=_Clock(_LOCKED_AT, raises=RuntimeError("clock hw offline")),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "clock_raised"


def test_clock_returns_non_datetime_fail_closed():
    r = check_committee_degradation_timeout(
        clock=_Clock(_LOCKED_AT, returns="2026-04-21"),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "clock_return_not_datetime"


def test_daily_log_reader_raises_in_suspend_window_fail_closed():
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(40)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None, raises=PermissionError("denied")),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "daily_log_reader_raised"
    assert "PermissionError" in (r.detail.reader_error or "")


def test_daily_log_reader_not_called_outside_suspend_window():
    reader = _DailyLog(None)
    check_committee_degradation_timeout(
        clock=_Clock(_now_plus(10)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=reader,
    )
    assert reader.calls == []


def test_daily_log_reader_not_called_in_escalate_window():
    reader = _DailyLog(None)
    check_committee_degradation_timeout(
        clock=_Clock(_now_plus(200)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=reader,
    )
    assert reader.calls == []


def test_daily_log_reader_returns_non_str_non_none_fail_closed():
    now = _now_plus(40)
    today_iso = now.date().isoformat()
    # Daily log "returns" an int (invalid).
    r = check_committee_degradation_timeout(
        clock=_Clock(now),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog({today_iso: 123}),  # type: ignore[dict-item]
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "daily_log_reader_raised"


# ---------------------------------------------------------------------------
# Deprecation row schema defects
# ---------------------------------------------------------------------------


def test_deprecation_row_missing_event_id_fail_closed():
    dep = _dep_row()
    del dep["deprecation_event_id"]
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(5)),
        lock_history_reader=_LockHistory([dep]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "deprecation_row_missing_event_id"


def test_deprecation_row_missing_timestamp_fail_closed():
    dep = _dep_row()
    del dep["lock_timestamp_utc"]
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(5)),
        lock_history_reader=_LockHistory([dep]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "deprecation_row_missing_lock_timestamp"


def test_deprecation_row_timestamp_unparseable_fail_closed():
    dep = _dep_row(locked_at="not-a-timestamp")
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(5)),
        lock_history_reader=_LockHistory([dep]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "deprecation_row_timestamp_unparseable"


def test_deprecation_row_prefers_locked_at_iso8601_over_lock_timestamp_utc():
    dep = _dep_row()
    # Add both fields; locked_at_iso8601 takes precedence per implementation.
    dep["locked_at_iso8601"] = "2026-04-15T00:00:00Z"
    dep["lock_timestamp_utc"] = _LOCKED_AT.isoformat()
    now = datetime(2026, 4, 20, 0, 0, 0, tzinfo=timezone.utc)
    r = check_committee_degradation_timeout(
        clock=_Clock(now),
        lock_history_reader=_LockHistory([dep]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is True
    assert r.detail.days_elapsed == 5


def test_lock_history_rows_may_contain_non_dict_entries_skipped():
    rows = ["garbage", 42, None, _dep_row()]
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(5)),
        lock_history_reader=_LockHistory(rows),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "within_warn_window_silent"


# ---------------------------------------------------------------------------
# Clock tz-naive + tz-aware mixes
# ---------------------------------------------------------------------------


def test_clock_tz_naive_treated_as_utc():
    now_naive = datetime(2026, 3, 23, 0, 0, 0) + timedelta(days=40)
    r = check_committee_degradation_timeout(
        clock=_Clock(now_naive),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_SUSPEND


def test_locked_at_tz_naive_treated_as_utc():
    dep = _dep_row(locked_at="2026-03-23T00:00:00")
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(40)),
        lock_history_reader=_LockHistory([dep]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_SUSPEND


# ---------------------------------------------------------------------------
# Threshold constants + frozen dataclass
# ---------------------------------------------------------------------------


def test_threshold_constants_are_inline_literals():
    assert WARN_THRESHOLD_DAYS == 14
    assert SUSPEND_THRESHOLD_DAYS == 30
    assert ESCALATE_THRESHOLD_DAYS == 60


def test_failure_code_and_event_constants():
    assert F_AMDT_08 == "F-AMDT-08"
    assert F_AMDT_08_SUSPEND == "F-AMDT-08-SUSPEND"
    assert F_AMDT_08_ESCALATE == "F-AMDT-08-ESCALATE"
    assert F_AMDT_08_READER_FAIL == "F-AMDT-08-READER-FAIL"
    assert EVENT_WARN == "F-AMDT-08-WARN"
    assert EVENT_SUSPEND == "F-AMDT-08-SUSPEND"
    assert EVENT_ESCALATE == "F-AMDT-08-ESCALATE"
    assert EVENT_READER_FAIL == "F-AMDT-08-READER-FAIL"
    assert EVENT_CLOCK_SKEW_WARN == "F-AMDT-08-CLOCK-SKEW-WARN"


def test_result_and_detail_frozen():
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(5)),
        lock_history_reader=_LockHistory([]),
        daily_log_reader=_DailyLog(None),
    )
    with pytest.raises(FrozenInstanceError):
        r.success = False  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        r.detail.days_elapsed = 99  # type: ignore[misc]
    assert isinstance(r.detail, CommitteeDegradationTimeoutDetail)
    assert isinstance(r, CommitteeDegradationTimeoutResult)
