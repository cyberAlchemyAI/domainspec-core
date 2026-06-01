"""F-COMMITTEE-DEGRADATION-TIMEOUT (F-AMDT-08) — time-triggered PRE-gate.

Fires as a PRE-gate on every code-LOCK promotion when a
deprecation-triggered replacement Thesis is still in flight. Enforces a
three-tier ceiling so that a temporary four-family Committee posture
cannot silently become the new normal.

**Tiers (elapsed days since `deprecation_triggered_replacement: true`
row sealed).**

- Days ``0..13`` — PASS silent (no emission).
- Days ``14..29`` — PASS with ``F-AMDT-08-WARN`` event.
- Days ``30..59`` — DENY ``F-AMDT-08-SUSPEND`` **unless** today's daily
  log carries a verbatim operator sign-off sentinel with a strictly
  future target date; in that case PASS with ``F-AMDT-08-WARN``
  (acknowledgment is itself audit-logged).
- Days ``>= 60`` — DENY ``F-AMDT-08-ESCALATE`` unconditionally (daily-log
  sign-off does NOT clear; only a fresh architectural Thesis LOCK does).
- Days ``< 0`` (clock skew / NTP anomaly) — PASS silent with
  ``F-AMDT-08-CLOCK-SKEW-WARN`` event.

**Rebind resistance.** ``WARN_THRESHOLD_DAYS``, ``SUSPEND_THRESHOLD_DAYS``,
and ``ESCALATE_THRESHOLD_DAYS`` are module-scope ``Final[int]`` sentinels
whose RHS values ``14 / 30 / 60`` are inlined at the comparison sites
(rebinding the module-level names has no behavioural effect — see
``test_adv_*_threshold_days_rebind_at_runtime``).

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 wave-3 delta rows for F-AMDT-08.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Final, Optional

from pipeline.logician.gates._protocols import (
    ClockProtocol,
    DailyLogReaderCallable,
    LockHistoryReaderCallable,
)


F_AMDT_08: Final[str] = "F-AMDT-08"
F_AMDT_08_SUSPEND: Final[str] = "F-AMDT-08-SUSPEND"
F_AMDT_08_ESCALATE: Final[str] = "F-AMDT-08-ESCALATE"
F_AMDT_08_READER_FAIL: Final[str] = "F-AMDT-08-READER-FAIL"

EVENT_WARN: Final[str] = "F-AMDT-08-WARN"
EVENT_SUSPEND: Final[str] = "F-AMDT-08-SUSPEND"
EVENT_ESCALATE: Final[str] = "F-AMDT-08-ESCALATE"
EVENT_READER_FAIL: Final[str] = "F-AMDT-08-READER-FAIL"
EVENT_CLOCK_SKEW_WARN: Final[str] = "F-AMDT-08-CLOCK-SKEW-WARN"

WARN_THRESHOLD_DAYS: Final[int] = 14
SUSPEND_THRESHOLD_DAYS: Final[int] = 30
ESCALATE_THRESHOLD_DAYS: Final[int] = 60


_REASON_NO_DEPRECATION_IN_FLIGHT: Final[str] = "no_deprecation_in_flight"
_REASON_DEPRECATION_COMPLETED: Final[str] = "deprecation_replacement_complete"
_REASON_WITHIN_WARN_WINDOW_SILENT: Final[str] = "within_warn_window_silent"
_REASON_WARN_WINDOW_REACHED: Final[str] = "warn_window_reached"
_REASON_SUSPEND_WINDOW_SIGN_OFF_PASSES: Final[str] = "suspend_window_signoff_passes"
_REASON_SUSPEND_WINDOW_DENY: Final[str] = "suspend_window_no_valid_signoff"
_REASON_ESCALATE_WINDOW_DENY: Final[str] = "escalate_window_deny"
_REASON_CLOCK_SKEW_WARN: Final[str] = "clock_skew_detected"

_REASON_LOCK_HISTORY_READER_RAISED: Final[str] = "lock_history_reader_raised"
_REASON_LOCK_HISTORY_NOT_LIST: Final[str] = "lock_history_not_list"
_REASON_CLOCK_RAISED: Final[str] = "clock_raised"
_REASON_DAILY_LOG_READER_RAISED: Final[str] = "daily_log_reader_raised"
_REASON_DAILY_LOG_RETURN_INVALID: Final[str] = "daily_log_return_invalid"
_REASON_CLOCK_RETURN_NOT_DATETIME: Final[str] = "clock_return_not_datetime"
_REASON_DEPRECATION_ROW_MISSING_TIMESTAMP: Final[str] = "deprecation_row_missing_lock_timestamp"
_REASON_DEPRECATION_ROW_TIMESTAMP_UNPARSEABLE: Final[str] = "deprecation_row_timestamp_unparseable"
_REASON_DEPRECATION_ROW_MISSING_EVENT_ID: Final[str] = "deprecation_row_missing_event_id"

_SENTINEL_PREFIX: Final[str] = (
    "F-AMDT-08 acknowledged: deprecation-replacement Thesis commitment target "
)


@dataclass(frozen=True, kw_only=True)
class CommitteeDegradationTimeoutDetail:
    """Structured detail for F-AMDT-08 result."""

    reason_tag: str
    emitted_event: str
    days_elapsed: int
    deprecation_event_id: str
    deprecation_locked_at: str
    reader_error: Optional[str]


@dataclass(frozen=True, kw_only=True)
class CommitteeDegradationTimeoutResult:
    success: bool
    failure_code: Optional[str]
    detail: CommitteeDegradationTimeoutDetail


def _clip_error(exc: BaseException) -> str:
    return f"{type(exc).__name__}: {exc}"[:500]


def _fail(
    *,
    failure_code: str,
    reason_tag: str,
    emitted_event: str = "",
    days_elapsed: int = 0,
    deprecation_event_id: str = "",
    deprecation_locked_at: str = "",
    reader_error: Optional[str] = None,
) -> CommitteeDegradationTimeoutResult:
    return CommitteeDegradationTimeoutResult(
        success=False,
        failure_code=failure_code,
        detail=CommitteeDegradationTimeoutDetail(
            reason_tag=reason_tag,
            emitted_event=emitted_event,
            days_elapsed=days_elapsed,
            deprecation_event_id=deprecation_event_id,
            deprecation_locked_at=deprecation_locked_at,
            reader_error=reader_error,
        ),
    )


def _ok(
    *,
    reason_tag: str,
    emitted_event: str = "",
    days_elapsed: int = 0,
    deprecation_event_id: str = "",
    deprecation_locked_at: str = "",
) -> CommitteeDegradationTimeoutResult:
    return CommitteeDegradationTimeoutResult(
        success=True,
        failure_code=None,
        detail=CommitteeDegradationTimeoutDetail(
            reason_tag=reason_tag,
            emitted_event=emitted_event,
            days_elapsed=days_elapsed,
            deprecation_event_id=deprecation_event_id,
            deprecation_locked_at=deprecation_locked_at,
            reader_error=None,
        ),
    )


def _parse_iso_datetime_utc(raw: str) -> Optional[datetime]:
    """Parse a lock_history timestamp. Accepts trailing Z or explicit offset.

    The empty-string / non-str defence is dead under the main entry (the
    caller guards at the dict-read site) but remains here so the helper
    stays safe in isolation. Exercised directly by
    ``test_adv_parse_iso_datetime_utc_empty_and_nonstr``.
    """
    if not isinstance(raw, str) or raw == "":
        return None
    txt = raw.strip()
    if txt.endswith("Z"):
        txt = txt[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(txt)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _find_deprecation_in_flight(rows: list[dict]) -> Optional[dict]:
    """Return most recent deprecation_triggered_replacement=True row whose
    deprecation_event_id has no completion row anywhere in the list.

    Walks from tail for "most recent" semantics. Completion lookup scans the
    full list (row ordering in the file is append-only but completion rows
    may come from later sessions).
    """
    deprecation_rows: list[dict] = []
    completion_event_ids: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("deprecation_triggered_replacement") is True:
            deprecation_rows.append(row)
        if row.get("deprecation_replacement_complete") is True:
            eid = row.get("deprecation_event_id")
            if isinstance(eid, str) and eid != "":
                completion_event_ids.add(eid)

    for dep_row in reversed(deprecation_rows):
        eid = dep_row.get("deprecation_event_id")
        if not isinstance(eid, str) or eid == "":
            return dep_row
        if eid not in completion_event_ids:
            return dep_row
    return None


def _read_daily_log_signoff_future_date(
    *,
    daily_log_reader: DailyLogReaderCallable,
    today: date,
) -> Optional[date]:
    """Return the parsed strictly-future target date from a verbatim sign-off
    sentinel in today's daily log, or ``None`` if absent/malformed/not-future.

    Raises the reader's exception untouched so the caller can classify it
    as ``F-AMDT-08-READER-FAIL``.
    """
    today_iso = today.isoformat()
    text = daily_log_reader(today_iso)
    if text is None:
        return None
    if not isinstance(text, str):
        raise TypeError("daily_log_reader returned non-str, non-None value")
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith(_SENTINEL_PREFIX):
            continue
        tail = stripped[len(_SENTINEL_PREFIX):]
        # tail should be YYYY-MM-DD exactly (10 chars). Allow optional trailing
        # whitespace or punctuation we stripped above already.
        candidate = tail.split()[0] if tail else ""
        if len(candidate) != 10:
            continue
        try:
            target = date.fromisoformat(candidate)
        except ValueError:
            continue
        if target > today:
            return target
    return None


def check_committee_degradation_timeout(
    *,
    clock: ClockProtocol,
    lock_history_reader: LockHistoryReaderCallable,
    daily_log_reader: DailyLogReaderCallable,
) -> CommitteeDegradationTimeoutResult:
    """PRE-gate F-COMMITTEE-DEGRADATION-TIMEOUT (F-AMDT-08).

    Caller wires this into the code-LOCK promotion hook. Returns a frozen
    result; the caller is responsible for emitting the `emitted_event`
    (if any) to `pipeline/metrics/session_log.jsonl`.
    """

    try:
        rows = lock_history_reader()
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_08_READER_FAIL,
            reason_tag=_REASON_LOCK_HISTORY_READER_RAISED,
            emitted_event=EVENT_READER_FAIL,
            reader_error=f"lock_history_reader: {_clip_error(exc)}",
        )

    if not isinstance(rows, list):
        return _fail(
            failure_code=F_AMDT_08_READER_FAIL,
            reason_tag=_REASON_LOCK_HISTORY_NOT_LIST,
            emitted_event=EVENT_READER_FAIL,
        )

    dep_row = _find_deprecation_in_flight(rows)
    if dep_row is None:
        return _ok(reason_tag=_REASON_NO_DEPRECATION_IN_FLIGHT)

    eid = dep_row.get("deprecation_event_id", "")
    if not isinstance(eid, str) or eid == "":
        return _fail(
            failure_code=F_AMDT_08_READER_FAIL,
            reason_tag=_REASON_DEPRECATION_ROW_MISSING_EVENT_ID,
            emitted_event=EVENT_READER_FAIL,
        )

    raw_locked_at = dep_row.get("locked_at_iso8601") or dep_row.get("lock_timestamp_utc")
    if not isinstance(raw_locked_at, str) or raw_locked_at == "":
        return _fail(
            failure_code=F_AMDT_08_READER_FAIL,
            reason_tag=_REASON_DEPRECATION_ROW_MISSING_TIMESTAMP,
            emitted_event=EVENT_READER_FAIL,
            deprecation_event_id=eid,
        )

    locked_at = _parse_iso_datetime_utc(raw_locked_at)
    if locked_at is None:
        return _fail(
            failure_code=F_AMDT_08_READER_FAIL,
            reason_tag=_REASON_DEPRECATION_ROW_TIMESTAMP_UNPARSEABLE,
            emitted_event=EVENT_READER_FAIL,
            deprecation_event_id=eid,
            deprecation_locked_at=raw_locked_at,
        )

    try:
        now = clock.now_utc()
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_08_READER_FAIL,
            reason_tag=_REASON_CLOCK_RAISED,
            emitted_event=EVENT_READER_FAIL,
            deprecation_event_id=eid,
            deprecation_locked_at=raw_locked_at,
            reader_error=f"clock: {_clip_error(exc)}",
        )

    if not isinstance(now, datetime):
        return _fail(
            failure_code=F_AMDT_08_READER_FAIL,
            reason_tag=_REASON_CLOCK_RETURN_NOT_DATETIME,
            emitted_event=EVENT_READER_FAIL,
            deprecation_event_id=eid,
            deprecation_locked_at=raw_locked_at,
        )
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    now = now.astimezone(timezone.utc)

    days_elapsed = (now - locked_at).days

    if days_elapsed < 0:
        return _ok(
            reason_tag=_REASON_CLOCK_SKEW_WARN,
            emitted_event=EVENT_CLOCK_SKEW_WARN,
            days_elapsed=days_elapsed,
            deprecation_event_id=eid,
            deprecation_locked_at=raw_locked_at,
        )

    # Inline-literal thresholds — rebind of the module-scope Final[int]
    # sentinels does NOT affect the comparisons below.
    if days_elapsed < 14:
        return _ok(
            reason_tag=_REASON_WITHIN_WARN_WINDOW_SILENT,
            days_elapsed=days_elapsed,
            deprecation_event_id=eid,
            deprecation_locked_at=raw_locked_at,
        )

    if days_elapsed < 30:
        return _ok(
            reason_tag=_REASON_WARN_WINDOW_REACHED,
            emitted_event=EVENT_WARN,
            days_elapsed=days_elapsed,
            deprecation_event_id=eid,
            deprecation_locked_at=raw_locked_at,
        )

    if days_elapsed < 60:
        today = now.date()
        try:
            signoff_date = _read_daily_log_signoff_future_date(
                daily_log_reader=daily_log_reader,
                today=today,
            )
        except Exception as exc:
            return _fail(
                failure_code=F_AMDT_08_READER_FAIL,
                reason_tag=_REASON_DAILY_LOG_READER_RAISED,
                emitted_event=EVENT_READER_FAIL,
                days_elapsed=days_elapsed,
                deprecation_event_id=eid,
                deprecation_locked_at=raw_locked_at,
                reader_error=f"daily_log_reader: {_clip_error(exc)}",
            )
        if signoff_date is not None:
            return _ok(
                reason_tag=_REASON_SUSPEND_WINDOW_SIGN_OFF_PASSES,
                emitted_event=EVENT_WARN,
                days_elapsed=days_elapsed,
                deprecation_event_id=eid,
                deprecation_locked_at=raw_locked_at,
            )
        return _fail(
            failure_code=F_AMDT_08_SUSPEND,
            reason_tag=_REASON_SUSPEND_WINDOW_DENY,
            emitted_event=EVENT_SUSPEND,
            days_elapsed=days_elapsed,
            deprecation_event_id=eid,
            deprecation_locked_at=raw_locked_at,
        )

    # days_elapsed >= 60
    return _fail(
        failure_code=F_AMDT_08_ESCALATE,
        reason_tag=_REASON_ESCALATE_WINDOW_DENY,
        emitted_event=EVENT_ESCALATE,
        days_elapsed=days_elapsed,
        deprecation_event_id=eid,
        deprecation_locked_at=raw_locked_at,
    )
