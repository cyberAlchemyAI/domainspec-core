"""Adversarial tests for F-COMMITTEE-DEGRADATION-TIMEOUT (F-AMDT-08).

Covers the seven adversarial cases named by the spec card plus three
additional flavours that exercise reader_error clipping, malformed
sentinel date characters, and the empty-locked-at defence.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

import pytest

from pipeline.logician.gates import f_committee_degradation_timeout as gate_mod
from pipeline.logician.gates.f_committee_degradation_timeout import (
    EVENT_CLOCK_SKEW_WARN,
    EVENT_READER_FAIL,
    EVENT_SUSPEND,
    F_AMDT_08_READER_FAIL,
    F_AMDT_08_SUSPEND,
    _parse_iso_datetime_utc,
    check_committee_degradation_timeout,
)


# ---------------------------------------------------------------------------
# Helpers (mirrored from the unit-test file so the two modules stay standalone)
# ---------------------------------------------------------------------------


_LOCKED_AT = datetime(2026, 3, 23, 0, 0, 0, tzinfo=timezone.utc)


class _Clock:
    def __init__(self, now: datetime, *, raises: Optional[BaseException] = None):
        self._now = now
        self._raises = raises

    def now_utc(self) -> datetime:
        if self._raises is not None:
            raise self._raises
        return self._now


class _LockHistory:
    def __init__(self, rows, *, raises: Optional[BaseException] = None):
        self._rows = rows
        self._raises = raises

    def __call__(self):
        if self._raises is not None:
            raise self._raises
        return self._rows


class _DailyLog:
    def __init__(self, text, *, raises: Optional[BaseException] = None):
        self._text = text
        self._raises = raises
        self.calls: list[str] = []

    def __call__(self, date_iso: str):
        self.calls.append(date_iso)
        if self._raises is not None:
            raise self._raises
        return self._text


def _dep_row(
    *,
    event_id: str = "en003-kimi-k2-2026-03-23",
    locked_at: str = _LOCKED_AT.isoformat(),
) -> dict:
    return {
        "module": "pipeline.logician.en003_kimi_k2_event",
        "deprecation_triggered_replacement": True,
        "deprecation_event_id": event_id,
        "lock_timestamp_utc": locked_at,
    }


def _now_plus(days: int, seconds: int = 0) -> datetime:
    return _LOCKED_AT + timedelta(days=days, seconds=seconds)


# ---------------------------------------------------------------------------
# Spec-card adversarial cases — threshold rebind defence-in-depth
# ---------------------------------------------------------------------------


def test_adv_warn_threshold_days_rebind_at_module_load():
    """Spec case 1 — rebinding ``WARN_THRESHOLD_DAYS`` at module scope must
    NOT change the silent-vs-WARN boundary (the inline-literal ``14`` wins).

    Day 13 must still be silent PASS even after rebind to 99; day 14 must
    still emit WARN.
    """
    before = gate_mod.WARN_THRESHOLD_DAYS
    setattr(gate_mod, "WARN_THRESHOLD_DAYS", 99)
    try:
        r13 = check_committee_degradation_timeout(
            clock=_Clock(_now_plus(13)),
            lock_history_reader=_LockHistory([_dep_row()]),
            daily_log_reader=_DailyLog(None),
        )
        assert r13.success is True
        assert r13.detail.reason_tag == "within_warn_window_silent"
        assert r13.detail.emitted_event == ""

        r14 = check_committee_degradation_timeout(
            clock=_Clock(_now_plus(14)),
            lock_history_reader=_LockHistory([_dep_row()]),
            daily_log_reader=_DailyLog(None),
        )
        assert r14.success is True
        assert r14.detail.reason_tag == "warn_window_reached"
        assert r14.detail.emitted_event == "F-AMDT-08-WARN"
    finally:
        setattr(gate_mod, "WARN_THRESHOLD_DAYS", before)


def test_adv_suspend_threshold_days_rebind_at_runtime():
    """Spec case 2 — rebinding ``SUSPEND_THRESHOLD_DAYS`` at runtime must
    NOT change the WARN-vs-SUSPEND boundary. Day 29 must still be WARN
    (PASS); day 30 must still be SUSPEND (DENY) absent a sign-off.
    """
    before = gate_mod.SUSPEND_THRESHOLD_DAYS
    setattr(gate_mod, "SUSPEND_THRESHOLD_DAYS", 0)
    try:
        r29 = check_committee_degradation_timeout(
            clock=_Clock(_now_plus(29)),
            lock_history_reader=_LockHistory([_dep_row()]),
            daily_log_reader=_DailyLog(None),
        )
        assert r29.success is True
        assert r29.detail.reason_tag == "warn_window_reached"

        r30 = check_committee_degradation_timeout(
            clock=_Clock(_now_plus(30)),
            lock_history_reader=_LockHistory([_dep_row()]),
            daily_log_reader=_DailyLog(None),
        )
        assert r30.success is False
        assert r30.failure_code == F_AMDT_08_SUSPEND
        assert r30.detail.emitted_event == EVENT_SUSPEND
    finally:
        setattr(gate_mod, "SUSPEND_THRESHOLD_DAYS", before)


def test_adv_escalate_threshold_days_rebind_at_runtime():
    """Spec case 3 — rebinding ``ESCALATE_THRESHOLD_DAYS`` at runtime must
    NOT change the SUSPEND-vs-ESCALATE boundary. Day 59 must still be
    SUSPEND; day 60 must still be ESCALATE (unconditional deny).
    """
    before = gate_mod.ESCALATE_THRESHOLD_DAYS
    setattr(gate_mod, "ESCALATE_THRESHOLD_DAYS", 99999)
    try:
        r59 = check_committee_degradation_timeout(
            clock=_Clock(_now_plus(59)),
            lock_history_reader=_LockHistory([_dep_row()]),
            daily_log_reader=_DailyLog(None),
        )
        assert r59.success is False
        assert r59.failure_code == F_AMDT_08_SUSPEND

        # A future-date sign-off that would clear SUSPEND must NOT clear
        # ESCALATE.
        today_iso_60 = _now_plus(60).date().isoformat()
        signoff = (
            "F-AMDT-08 acknowledged: deprecation-replacement Thesis commitment"
            " target 2027-01-01"
        )
        r60 = check_committee_degradation_timeout(
            clock=_Clock(_now_plus(60)),
            lock_history_reader=_LockHistory([_dep_row()]),
            daily_log_reader=_DailyLog({today_iso_60: signoff}.get(today_iso_60)),
        )
        assert r60.success is False
        assert r60.failure_code == "F-AMDT-08-ESCALATE"
        assert r60.detail.emitted_event == "F-AMDT-08-ESCALATE"
    finally:
        setattr(gate_mod, "ESCALATE_THRESHOLD_DAYS", before)


# ---------------------------------------------------------------------------
# Spec-card adversarial cases — fail-closed reader failures
# ---------------------------------------------------------------------------


def test_adv_clock_raises():
    """Spec case 4 — clock.now_utc() raises → DENY F-AMDT-08-READER-FAIL."""
    r = check_committee_degradation_timeout(
        clock=_Clock(_LOCKED_AT, raises=OSError("ntp offline")),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "clock_raised"
    assert r.detail.emitted_event == EVENT_READER_FAIL
    assert r.detail.reader_error is not None
    assert "OSError" in r.detail.reader_error


def test_adv_lock_history_reader_raises():
    """Spec case 5 — lock_history_reader() raises → DENY fail-closed."""
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(5)),
        lock_history_reader=_LockHistory([], raises=PermissionError("denied")),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "lock_history_reader_raised"
    assert r.detail.emitted_event == EVENT_READER_FAIL
    assert r.detail.reader_error is not None
    assert "PermissionError" in r.detail.reader_error


def test_adv_daily_log_reader_raises_in_suspend_tier():
    """Spec case 6 — daily_log_reader raises during SUSPEND tier resolve
    → DENY F-AMDT-08-READER-FAIL. A reader failure must NOT silently
    pass through as though the sign-off had been found.
    """
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(45)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None, raises=RuntimeError("disk detached")),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "daily_log_reader_raised"
    assert r.detail.emitted_event == EVENT_READER_FAIL
    assert r.detail.reader_error is not None
    assert "RuntimeError" in r.detail.reader_error
    assert r.detail.days_elapsed == 45


def test_adv_days_elapsed_negative_clock_skew():
    """Spec case 7 — clock returns a moment *before* locked_at (NTP anomaly
    / wall-clock rewound). Gate carves out to silent-PASS but emits
    ``F-AMDT-08-CLOCK-SKEW-WARN`` for audit trail.
    """
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(-5)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "clock_skew_detected"
    assert r.detail.emitted_event == EVENT_CLOCK_SKEW_WARN
    assert r.detail.days_elapsed == -5

    # Boundary — clock exactly 1 second behind → still negative timedelta
    # .days attribute is ``-1`` (Python rounds toward -inf), so still skew.
    r1s = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(0, seconds=-1)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(None),
    )
    assert r1s.success is True
    assert r1s.detail.reason_tag == "clock_skew_detected"
    assert r1s.detail.emitted_event == EVENT_CLOCK_SKEW_WARN


# ---------------------------------------------------------------------------
# Defence-in-depth flavours (not spec-card-named)
# ---------------------------------------------------------------------------


def test_adv_reader_error_clipped_at_500_chars():
    """Oversized exception message must be clipped to 500 chars in
    reader_error. The ``lock_history_reader: `` prefix is *then* added,
    so the final string may be longer than 500.
    """
    huge = "x" * 5000
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(5)),
        lock_history_reader=_LockHistory([], raises=RuntimeError(huge)),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.detail.reader_error is not None
    # Prefix "lock_history_reader: " is 21 chars; clipped body ≤ 500; so
    # total ≤ 521.
    assert len(r.detail.reader_error) <= 521
    assert r.detail.reader_error.startswith("lock_history_reader: ")


@pytest.mark.parametrize(
    "garbage",
    [
        "1234-56-78",  # plausible YYYY-MM-DD shape but invalid month/day
        "abcd-ef-gh",  # 10 chars, non-numeric at every position
        "2026-13-40",  # invalid month + day
        "YYYY-MM-DD",  # literal placeholder
    ],
)
def test_adv_malformed_sentinel_date_rejected(garbage):
    """Sign-off sentinel with a 10-char but unparseable date → SUSPEND DENY.

    Closes the tail branch in ``_read_daily_log_signoff_future_date``
    where ``date.fromisoformat`` raises ``ValueError``.
    """
    signoff = (
        "F-AMDT-08 acknowledged: deprecation-replacement Thesis commitment"
        f" target {garbage}"
    )
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(45)),
        lock_history_reader=_LockHistory([_dep_row()]),
        daily_log_reader=_DailyLog(signoff),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_SUSPEND
    assert r.detail.reason_tag == "suspend_window_no_valid_signoff"


def test_adv_locked_at_empty_string_rejected():
    """An empty string in ``lock_timestamp_utc`` must NOT parse as
    "now" (which would produce days=0 silent PASS and smuggle an
    in-flight deprecation past the gate). Instead, it is flagged as
    missing-timestamp → F-AMDT-08-READER-FAIL.

    Closes the empty-string branch in ``_parse_iso_datetime_utc``.
    """
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(45)),
        lock_history_reader=_LockHistory([_dep_row(locked_at="")]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "deprecation_row_missing_lock_timestamp"


def test_adv_parse_iso_datetime_utc_empty_and_nonstr():
    """Direct exercise of ``_parse_iso_datetime_utc`` defensive branches.

    The main entry guards empty strings at the dict-read site, but the
    helper must remain safe in isolation — empty string / non-str / garbage
    → None (never raise).
    """
    assert _parse_iso_datetime_utc("") is None
    assert _parse_iso_datetime_utc("   ") is None  # whitespace-only
    # Non-str — helper tolerates (defensive; static type says ``str``).
    assert _parse_iso_datetime_utc(None) is None  # type: ignore[arg-type]
    assert _parse_iso_datetime_utc(42) is None  # type: ignore[arg-type]
    assert _parse_iso_datetime_utc("not-a-timestamp") is None


def test_adv_precedence_order_reader_check_before_threshold_check():
    """Defence-in-depth — a malformed lock_history row must land on
    reader-fail BEFORE any tier comparison, so a row that *would* otherwise
    land on ESCALATE cannot silently leak ESCALATE as the failure code.
    """
    # Row with missing event_id — should land on reader-fail regardless of
    # elapsed days (clock is 200d ahead which would otherwise ESCALATE).
    bad_row = {
        "module": "pipeline.logician.en003_kimi_k2_event",
        "deprecation_triggered_replacement": True,
        "lock_timestamp_utc": _LOCKED_AT.isoformat(),
    }
    r = check_committee_degradation_timeout(
        clock=_Clock(_now_plus(200)),
        lock_history_reader=_LockHistory([bad_row]),
        daily_log_reader=_DailyLog(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_08_READER_FAIL
    assert r.detail.reason_tag == "deprecation_row_missing_event_id"
