"""Adversarial tests for F-DEPRECATION-REGISTER-STALENESS (F-AMDT-09).

Covers the seven adversarial cases named by the spec card plus extra
defence-in-depth cases for _parse_iso_datetime_utc corner characters
(trailing Z, empty-string fallback), _find_register_row non-dict rows
skipped, reader_error clipping, and precedence ordering.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

import pytest

from pipeline.logician.gates import f_deprecation_register_staleness as gate_mod
from pipeline.logician.gates.f_deprecation_register_staleness import (
    EVENT_MISSING,
    EVENT_NOT_DEPRECATED_OVERRIDE,
    EVENT_READER_FAIL,
    EVENT_STALE,
    F_AMDT_09_MISSING,
    F_AMDT_09_READER_FAIL,
    F_AMDT_09_STALE,
    STALENESS_WINDOW_HOURS,
    _find_register_row,
    _parse_iso_datetime_utc,
    check_deprecation_register_staleness,
)


# ---------------------------------------------------------------------------
# Helpers (mirrored so this file stands alone from the unit-test module)
# ---------------------------------------------------------------------------


_ANN = datetime(2026, 4, 1, 12, 0, 0, tzinfo=timezone.utc)
_NOW_WITHIN = datetime(2026, 4, 3, 12, 0, 0, tzinfo=timezone.utc)  # +48 h
_NOW_STALE = datetime(2026, 4, 10, 12, 0, 0, tzinfo=timezone.utc)  # +9 d
_MODEL = "moonshotai/kimi-k2-instruct"


class _Clock:
    def __init__(self, now: datetime, *, raises: Optional[BaseException] = None):
        self._now = now
        self._raises = raises

    def now_utc(self) -> datetime:
        if self._raises is not None:
            raise self._raises
        return self._now


class _Register:
    def __init__(self, rows, *, raises: Optional[BaseException] = None):
        self._rows = rows
        self._raises = raises

    def __call__(self):
        if self._raises is not None:
            raise self._raises
        return self._rows


class _Feed:
    def __init__(self, entry, *, raises: Optional[BaseException] = None):
        self._entry = entry
        self._raises = raises

    def __call__(self, affected_model: str):
        if self._raises is not None:
            raise self._raises
        return self._entry


def _feed_entry(announcement: datetime = _ANN) -> dict:
    return {"announcement_iso8601": announcement.isoformat()}


def _reg_row(
    *,
    model: str = _MODEL,
    deprecated: bool = True,
    not_deprecated: bool = False,
    registered_at: Optional[datetime] = _ANN,
) -> dict:
    row: dict = {"affected_model": model}
    if deprecated:
        row["deprecated"] = True
    if not_deprecated:
        row["not_deprecated"] = True
    if registered_at is not None:
        row["registered_at_iso8601"] = registered_at.isoformat()
    return row


def _fm(*, model: str = _MODEL, forced: bool = False) -> dict:
    return {"forced_replacement": forced, "affected_model": model}


# ---------------------------------------------------------------------------
# 1. Spec-card adversarial cases
# ---------------------------------------------------------------------------


def test_adv_clock_raises():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW_WITHIN, raises=OSError("clock disk err")),
        deprecation_register_reader=_Register([_reg_row()]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_READER_FAIL
    assert r.detail.emitted_event == EVENT_READER_FAIL
    assert r.detail.reason_tag == "clock_raised"
    assert r.detail.reader_error is not None
    assert "clock" in r.detail.reader_error
    assert "OSError" in r.detail.reader_error


def test_adv_feed_reader_raises():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW_WITHIN),
        deprecation_register_reader=_Register([_reg_row()]),
        deprecation_feed_reader=_Feed(None, raises=RuntimeError("network down")),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_READER_FAIL
    assert r.detail.reason_tag == "feed_reader_raised"
    assert r.detail.reader_error is not None
    assert "deprecation_feed_reader" in r.detail.reader_error
    assert "RuntimeError" in r.detail.reader_error


def test_adv_register_reader_raises():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW_WITHIN),
        deprecation_register_reader=_Register(
            [], raises=PermissionError("register jsonl unreadable")
        ),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_READER_FAIL
    assert r.detail.reason_tag == "register_reader_raised"
    assert r.detail.reader_error is not None
    assert "deprecation_register_reader" in r.detail.reader_error
    assert "PermissionError" in r.detail.reader_error


def test_adv_staleness_window_hours_rebind_at_module_load():
    # Module-scope sentinel must be exactly 72 at import time.
    assert STALENESS_WINDOW_HOURS == 72
    assert gate_mod.STALENESS_WINDOW_HOURS == 72


def test_adv_staleness_window_hours_rebind_at_runtime(monkeypatch):
    # Rebind module attribute to a value that would flip verdicts if the
    # comparison site honoured the rebind. It must not.
    monkeypatch.setattr(gate_mod, "STALENESS_WINDOW_HOURS", 1, raising=True)

    # Build a scenario where register is 48h behind announcement: under the
    # original `<= 72` comparison this must PASS. If the rebind leaked into
    # the gate body, the comparison would become `<= 1` and the gate would
    # DENY STALE.
    ann = _ANN
    registered = ann - timedelta(hours=48)
    now = ann + timedelta(hours=1)
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(now),
        deprecation_register_reader=_Register(
            [_reg_row(registered_at=registered)]
        ),
        deprecation_feed_reader=_Feed(_feed_entry(announcement=ann)),
    )
    assert r.success is True, (
        "inline-literal 72 must override module-attr rebind"
    )
    assert r.detail.reason_tag == "register_current_within_window"
    assert r.detail.staleness_hours == 48


def test_adv_register_row_has_not_deprecated_override():
    # Operator-asserted `not_deprecated: True` overrides the feed. PASS
    # with an audit event so someone can see the override fired.
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW_STALE),
        deprecation_register_reader=_Register(
            [_reg_row(deprecated=False, not_deprecated=True, registered_at=_ANN)]
        ),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.emitted_event == EVENT_NOT_DEPRECATED_OVERRIDE
    assert r.detail.reason_tag == "register_not_deprecated_override"


def test_adv_negative_staleness_clock_skew():
    # Register's registered_at is AFTER the announcement (impossible but
    # defensive) → treat as PASS with clock-skew event.
    ann = _ANN
    registered = ann + timedelta(hours=6)  # register ahead of feed
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(ann + timedelta(hours=24)),
        deprecation_register_reader=_Register(
            [_reg_row(registered_at=registered)]
        ),
        deprecation_feed_reader=_Feed(_feed_entry(announcement=ann)),
    )
    assert r.success is True
    assert r.detail.reason_tag == "register_ahead_of_feed_clock_skew"
    assert r.detail.emitted_event == "F-AMDT-09-REGISTER-AHEAD-OF-FEED"


# ---------------------------------------------------------------------------
# 2. Defence-in-depth: parse helper + walker edge paths
# ---------------------------------------------------------------------------


def test_adv_parse_iso_datetime_utc_empty_and_nonstr():
    assert _parse_iso_datetime_utc("") is None
    assert _parse_iso_datetime_utc("not-a-datetime") is None


def test_adv_parse_iso_datetime_utc_trailing_z_accepted():
    # `Z` suffix must be accepted and normalised to UTC.
    got = _parse_iso_datetime_utc("2026-04-01T12:00:00Z")
    assert got is not None
    assert got == datetime(2026, 4, 1, 12, 0, 0, tzinfo=timezone.utc)


def test_adv_find_register_row_skips_non_dict_rows():
    # Non-dict rows MUST appear LATER in list order so the reversed walk
    # hits them first and exercises the `continue` branch before landing
    # on the matching dict row.
    rows = [
        _reg_row(model=_MODEL),
        "not a dict",
        42,
        None,
    ]
    row = _find_register_row(rows, _MODEL)
    assert row is not None
    assert row["affected_model"] == _MODEL


def test_adv_reader_error_clipped_at_500_chars():
    # Long exception message must be clipped to ≤500 chars in reader_error.
    huge = "X" * 2000
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW_WITHIN),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed(None, raises=RuntimeError(huge)),
    )
    assert r.success is False
    assert r.detail.reader_error is not None
    # Prefix "deprecation_feed_reader: " + ≤500 clipped payload.
    assert len(r.detail.reader_error) <= len("deprecation_feed_reader: ") + 500


def test_adv_precedence_forced_replacement_checked_before_readers():
    # When forced_replacement is not explicitly False, the gate must no-op
    # BEFORE invoking any reader. Any reader invocation would leak side
    # effects into the happy path.
    feed = _Feed(None, raises=AssertionError("feed must not be called"))
    reg = _Register([], raises=AssertionError("register must not be called"))
    r = check_deprecation_register_staleness(
        amendment_frontmatter={"forced_replacement": True, "affected_model": _MODEL},
        clock=_Clock(_NOW_WITHIN),
        deprecation_register_reader=reg,
        deprecation_feed_reader=feed,
    )
    assert r.success is True
    assert r.detail.reason_tag == "forced_replacement_not_false_noop"


def test_adv_precedence_frontmatter_defects_before_readers():
    # Malformed frontmatter must short-circuit BEFORE any reader fires.
    feed = _Feed(None, raises=AssertionError("feed must not be called"))
    reg = _Register([], raises=AssertionError("register must not be called"))
    r = check_deprecation_register_staleness(
        amendment_frontmatter="this is not a dict",  # type: ignore[arg-type]
        clock=_Clock(_NOW_WITHIN),
        deprecation_register_reader=reg,
        deprecation_feed_reader=feed,
    )
    assert r.success is False
    assert r.detail.reason_tag == "frontmatter_not_dict"
