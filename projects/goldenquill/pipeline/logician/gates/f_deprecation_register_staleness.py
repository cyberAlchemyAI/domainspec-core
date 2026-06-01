"""F-DEPRECATION-REGISTER-STALENESS (F-AMDT-09) — PRE-gate.

Fires as a PRE-gate on any amendment whose frontmatter claims
``forced_replacement: false`` AND names a provider / model slug in
``affected_model:``. Cross-checks two independent sources:

1. ``pipeline/vault_shared/deprecation_register.jsonl`` — the operator-
   maintained local register (what the pipeline treats as authoritative).
2. A cached provider-announcement feed (``pipeline/vault_shared/
   deprecation_feed_cache/<provider>.jsonl``) ingested out-of-band.

Closes EN-003 Cycle 4 Red Team finding C4-NEW-01: ``forced_replacement:
false`` evades the F-AMDT-06 (F-DEPRECATION-EXEMPTION-REUSE) path when
the register has not yet been updated to reflect a live deprecation
announcement. The 72-hour window lets weekend-posted announcements land
without forcing same-hour operator updates.

**Rebind resistance.** ``STALENESS_WINDOW_HOURS`` is a module-scope
``Final[int]`` sentinel whose RHS value ``72`` is inlined at the
comparison site (rebinding the module-level name has no behavioural
effect — see ``test_adv_staleness_window_hours_rebind_at_runtime``).

Blueprint anchor: ``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1
(parent LOCK); v2.2 wave-3 delta rows for F-AMDT-09.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Final, Optional

from pipeline.logician.gates._protocols import (
    ClockProtocol,
    DeprecationFeedReaderCallable,
    DeprecationRegisterReaderCallable,
)


F_AMDT_09: Final[str] = "F-AMDT-09"
F_AMDT_09_STALE: Final[str] = "F-AMDT-09-STALE"
F_AMDT_09_MISSING: Final[str] = "F-AMDT-09-MISSING"
F_AMDT_09_AMBIGUOUS: Final[str] = "F-AMDT-09-AMBIGUOUS"
F_AMDT_09_READER_FAIL: Final[str] = "F-AMDT-09-READER-FAIL"

EVENT_STALE: Final[str] = "F-AMDT-09-STALE"
EVENT_MISSING: Final[str] = "F-AMDT-09-MISSING"
EVENT_AMBIGUOUS: Final[str] = "F-AMDT-09-AMBIGUOUS"
EVENT_READER_FAIL: Final[str] = "F-AMDT-09-READER-FAIL"
EVENT_NOT_DEPRECATED_OVERRIDE: Final[str] = "F-AMDT-09-NOT-DEPRECATED-OVERRIDE"
EVENT_CLOCK_SKEW_REGISTER_AHEAD: Final[str] = "F-AMDT-09-REGISTER-AHEAD-OF-FEED"

STALENESS_WINDOW_HOURS: Final[int] = 72


_REASON_NO_OP_FORCED_REPLACEMENT_NOT_FALSE: Final[str] = "forced_replacement_not_false_noop"
_REASON_AFFECTED_MODEL_MISSING: Final[str] = "affected_model_missing"
_REASON_AFFECTED_MODEL_NOT_STR: Final[str] = "affected_model_not_str"
_REASON_AFFECTED_MODEL_EMPTY: Final[str] = "affected_model_empty"
_REASON_FRONTMATTER_NOT_DICT: Final[str] = "frontmatter_not_dict"

_REASON_FEED_REPORTS_NO_DEPRECATION: Final[str] = "feed_reports_no_deprecation"
_REASON_REGISTER_CURRENT: Final[str] = "register_current_within_window"
_REASON_REGISTER_AHEAD_OF_FEED: Final[str] = "register_ahead_of_feed_clock_skew"
_REASON_NOT_DEPRECATED_OVERRIDE: Final[str] = "register_not_deprecated_override"
_REASON_REGISTER_STALE: Final[str] = "register_older_than_window"
_REASON_REGISTER_MISSING: Final[str] = "register_entry_absent"

_REASON_FEED_READER_RAISED: Final[str] = "feed_reader_raised"
_REASON_FEED_RETURN_NOT_DICT_OR_NONE: Final[str] = "feed_return_invalid"
_REASON_FEED_ANNOUNCEMENT_MISSING: Final[str] = "feed_announcement_iso8601_missing"
_REASON_FEED_ANNOUNCEMENT_UNPARSEABLE: Final[str] = "feed_announcement_iso8601_unparseable"

_REASON_REGISTER_READER_RAISED: Final[str] = "register_reader_raised"
_REASON_REGISTER_RETURN_NOT_LIST: Final[str] = "register_return_not_list"
_REASON_REGISTER_ROW_REGISTERED_AT_UNPARSEABLE: Final[str] = (
    "register_row_registered_at_iso8601_unparseable"
)

_REASON_CLOCK_RAISED: Final[str] = "clock_raised"
_REASON_CLOCK_RETURN_NOT_DATETIME: Final[str] = "clock_return_not_datetime"


@dataclass(frozen=True, kw_only=True)
class DeprecationRegisterStalenessDetail:
    """Structured detail for F-AMDT-09 result."""

    reason_tag: str
    emitted_event: str
    affected_model: str
    feed_announcement_iso8601: str
    register_registered_at_iso8601: str
    staleness_hours: int
    reader_error: Optional[str]


@dataclass(frozen=True, kw_only=True)
class DeprecationRegisterStalenessResult:
    success: bool
    failure_code: Optional[str]
    detail: DeprecationRegisterStalenessDetail


def _clip_error(exc: BaseException) -> str:
    return f"{type(exc).__name__}: {exc}"[:500]


def _fail(
    *,
    failure_code: str,
    reason_tag: str,
    emitted_event: str = "",
    affected_model: str = "",
    feed_announcement_iso8601: str = "",
    register_registered_at_iso8601: str = "",
    staleness_hours: int = 0,
    reader_error: Optional[str] = None,
) -> DeprecationRegisterStalenessResult:
    return DeprecationRegisterStalenessResult(
        success=False,
        failure_code=failure_code,
        detail=DeprecationRegisterStalenessDetail(
            reason_tag=reason_tag,
            emitted_event=emitted_event,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_iso8601,
            register_registered_at_iso8601=register_registered_at_iso8601,
            staleness_hours=staleness_hours,
            reader_error=reader_error,
        ),
    )


def _ok(
    *,
    reason_tag: str,
    emitted_event: str = "",
    affected_model: str = "",
    feed_announcement_iso8601: str = "",
    register_registered_at_iso8601: str = "",
    staleness_hours: int = 0,
) -> DeprecationRegisterStalenessResult:
    return DeprecationRegisterStalenessResult(
        success=True,
        failure_code=None,
        detail=DeprecationRegisterStalenessDetail(
            reason_tag=reason_tag,
            emitted_event=emitted_event,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_iso8601,
            register_registered_at_iso8601=register_registered_at_iso8601,
            staleness_hours=staleness_hours,
            reader_error=None,
        ),
    )


def _parse_iso_datetime_utc(raw: str) -> Optional[datetime]:
    """Parse an ISO-8601 timestamp. Accepts trailing Z or explicit offset."""
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


def _find_register_row(
    rows: list[dict], affected_model: str
) -> Optional[dict]:
    """Walk rows from tail; return the most-recent row that names
    ``affected_model`` and carries either ``deprecated: true`` or
    ``not_deprecated: true``. Malformed rows silently skipped.
    """
    for row in reversed(rows):
        if not isinstance(row, dict):
            continue
        if row.get("affected_model") != affected_model:
            continue
        if row.get("not_deprecated") is True:
            return row
        if row.get("deprecated") is True:
            return row
    return None


def check_deprecation_register_staleness(
    *,
    amendment_frontmatter: dict,
    clock: ClockProtocol,
    deprecation_register_reader: DeprecationRegisterReaderCallable,
    deprecation_feed_reader: DeprecationFeedReaderCallable,
) -> DeprecationRegisterStalenessResult:
    """PRE-gate F-DEPRECATION-REGISTER-STALENESS (F-AMDT-09).

    Caller wires this into the amendment promotion hook. Returns a frozen
    result; the caller is responsible for emitting the ``emitted_event``
    (if any) to ``pipeline/metrics/session_log.jsonl``.
    """

    if not isinstance(amendment_frontmatter, dict):
        return _fail(
            failure_code=F_AMDT_09_AMBIGUOUS,
            reason_tag=_REASON_FRONTMATTER_NOT_DICT,
            emitted_event=EVENT_AMBIGUOUS,
        )

    if amendment_frontmatter.get("forced_replacement") is not False:
        return _ok(reason_tag=_REASON_NO_OP_FORCED_REPLACEMENT_NOT_FALSE)

    # Gate only fires on explicit ``false`` claim. Extract affected_model
    # BEFORE touching any reader so ambiguous frontmatter fails fast.
    if "affected_model" not in amendment_frontmatter:
        return _fail(
            failure_code=F_AMDT_09_AMBIGUOUS,
            reason_tag=_REASON_AFFECTED_MODEL_MISSING,
            emitted_event=EVENT_AMBIGUOUS,
        )
    affected_model = amendment_frontmatter["affected_model"]
    if not isinstance(affected_model, str):
        return _fail(
            failure_code=F_AMDT_09_AMBIGUOUS,
            reason_tag=_REASON_AFFECTED_MODEL_NOT_STR,
            emitted_event=EVENT_AMBIGUOUS,
        )
    if affected_model == "":
        return _fail(
            failure_code=F_AMDT_09_AMBIGUOUS,
            reason_tag=_REASON_AFFECTED_MODEL_EMPTY,
            emitted_event=EVENT_AMBIGUOUS,
        )

    try:
        feed_entry = deprecation_feed_reader(affected_model)
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_09_READER_FAIL,
            reason_tag=_REASON_FEED_READER_RAISED,
            emitted_event=EVENT_READER_FAIL,
            affected_model=affected_model,
            reader_error=f"deprecation_feed_reader: {_clip_error(exc)}",
        )

    if feed_entry is None:
        return _ok(
            reason_tag=_REASON_FEED_REPORTS_NO_DEPRECATION,
            affected_model=affected_model,
        )
    if not isinstance(feed_entry, dict):
        return _fail(
            failure_code=F_AMDT_09_READER_FAIL,
            reason_tag=_REASON_FEED_RETURN_NOT_DICT_OR_NONE,
            emitted_event=EVENT_READER_FAIL,
            affected_model=affected_model,
        )

    feed_announcement_raw = feed_entry.get("announcement_iso8601")
    if not isinstance(feed_announcement_raw, str) or feed_announcement_raw == "":
        return _fail(
            failure_code=F_AMDT_09_READER_FAIL,
            reason_tag=_REASON_FEED_ANNOUNCEMENT_MISSING,
            emitted_event=EVENT_READER_FAIL,
            affected_model=affected_model,
        )
    feed_announcement_dt = _parse_iso_datetime_utc(feed_announcement_raw)
    if feed_announcement_dt is None:
        return _fail(
            failure_code=F_AMDT_09_READER_FAIL,
            reason_tag=_REASON_FEED_ANNOUNCEMENT_UNPARSEABLE,
            emitted_event=EVENT_READER_FAIL,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_raw,
        )

    try:
        register_rows = deprecation_register_reader()
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_09_READER_FAIL,
            reason_tag=_REASON_REGISTER_READER_RAISED,
            emitted_event=EVENT_READER_FAIL,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_raw,
            reader_error=f"deprecation_register_reader: {_clip_error(exc)}",
        )
    if not isinstance(register_rows, list):
        return _fail(
            failure_code=F_AMDT_09_READER_FAIL,
            reason_tag=_REASON_REGISTER_RETURN_NOT_LIST,
            emitted_event=EVENT_READER_FAIL,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_raw,
        )

    register_row = _find_register_row(register_rows, affected_model)

    if register_row is not None and register_row.get("not_deprecated") is True:
        # Operator-asserted override: feed is wrong. PASS with event for audit.
        return _ok(
            reason_tag=_REASON_NOT_DEPRECATED_OVERRIDE,
            emitted_event=EVENT_NOT_DEPRECATED_OVERRIDE,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_raw,
        )

    if register_row is None:
        # Feed reports deprecation, register has no entry → MISSING.
        return _fail(
            failure_code=F_AMDT_09_MISSING,
            reason_tag=_REASON_REGISTER_MISSING,
            emitted_event=EVENT_MISSING,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_raw,
        )

    # Register has a deprecated=true row. Check its registered_at
    # timestamp relative to the feed announcement.
    registered_at_raw = register_row.get("registered_at_iso8601", "")
    if not isinstance(registered_at_raw, str):
        registered_at_raw = ""
    registered_at_dt: Optional[datetime] = None
    if registered_at_raw != "":
        registered_at_dt = _parse_iso_datetime_utc(registered_at_raw)
        if registered_at_dt is None:
            return _fail(
                failure_code=F_AMDT_09_READER_FAIL,
                reason_tag=_REASON_REGISTER_ROW_REGISTERED_AT_UNPARSEABLE,
                emitted_event=EVENT_READER_FAIL,
                affected_model=affected_model,
                feed_announcement_iso8601=feed_announcement_raw,
                register_registered_at_iso8601=registered_at_raw,
            )

    try:
        now = clock.now_utc()
    except Exception as exc:
        return _fail(
            failure_code=F_AMDT_09_READER_FAIL,
            reason_tag=_REASON_CLOCK_RAISED,
            emitted_event=EVENT_READER_FAIL,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_raw,
            register_registered_at_iso8601=registered_at_raw,
            reader_error=f"clock: {_clip_error(exc)}",
        )
    if not isinstance(now, datetime):
        return _fail(
            failure_code=F_AMDT_09_READER_FAIL,
            reason_tag=_REASON_CLOCK_RETURN_NOT_DATETIME,
            emitted_event=EVENT_READER_FAIL,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_raw,
            register_registered_at_iso8601=registered_at_raw,
        )
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    now = now.astimezone(timezone.utc)

    if registered_at_dt is None:
        # deprecated=true row with missing registered_at — treat as
        # staleness_hours from announcement to now.
        gap_hours = int((now - feed_announcement_dt).total_seconds() // 3600)
        if gap_hours < 0:
            gap_hours = 0
        # Inline-literal threshold — rebind of STALENESS_WINDOW_HOURS
        # does NOT affect comparison.
        if gap_hours <= 72:
            return _ok(
                reason_tag=_REASON_REGISTER_CURRENT,
                affected_model=affected_model,
                feed_announcement_iso8601=feed_announcement_raw,
                staleness_hours=gap_hours,
            )
        return _fail(
            failure_code=F_AMDT_09_STALE,
            reason_tag=_REASON_REGISTER_STALE,
            emitted_event=EVENT_STALE,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_raw,
            staleness_hours=gap_hours,
        )

    # Compare registered_at vs announcement.
    delta_hours = int(
        (feed_announcement_dt - registered_at_dt).total_seconds() // 3600
    )
    if delta_hours < 0:
        # Register was registered AFTER the announcement — register is
        # ahead of (or clock-skew relative to) the feed. Treat as PASS
        # with CLOCK-SKEW event for audit.
        return _ok(
            reason_tag=_REASON_REGISTER_AHEAD_OF_FEED,
            emitted_event=EVENT_CLOCK_SKEW_REGISTER_AHEAD,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_raw,
            register_registered_at_iso8601=registered_at_raw,
            staleness_hours=delta_hours,
        )

    # delta_hours >= 0 — register is at-or-behind announcement.
    # Inline-literal threshold — rebind of STALENESS_WINDOW_HOURS does
    # NOT affect this comparison.
    if delta_hours <= 72:
        return _ok(
            reason_tag=_REASON_REGISTER_CURRENT,
            affected_model=affected_model,
            feed_announcement_iso8601=feed_announcement_raw,
            register_registered_at_iso8601=registered_at_raw,
            staleness_hours=delta_hours,
        )
    return _fail(
        failure_code=F_AMDT_09_STALE,
        reason_tag=_REASON_REGISTER_STALE,
        emitted_event=EVENT_STALE,
        affected_model=affected_model,
        feed_announcement_iso8601=feed_announcement_raw,
        register_registered_at_iso8601=registered_at_raw,
        staleness_hours=delta_hours,
    )
