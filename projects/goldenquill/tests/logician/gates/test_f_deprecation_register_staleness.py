"""Unit tests for F-DEPRECATION-REGISTER-STALENESS (F-AMDT-09)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from typing import Optional

import pytest

from pipeline.logician.gates.f_deprecation_register_staleness import (
    EVENT_AMBIGUOUS,
    EVENT_CLOCK_SKEW_REGISTER_AHEAD,
    EVENT_MISSING,
    EVENT_NOT_DEPRECATED_OVERRIDE,
    EVENT_READER_FAIL,
    EVENT_STALE,
    F_AMDT_09,
    F_AMDT_09_AMBIGUOUS,
    F_AMDT_09_MISSING,
    F_AMDT_09_READER_FAIL,
    F_AMDT_09_STALE,
    STALENESS_WINDOW_HOURS,
    DeprecationRegisterStalenessDetail,
    DeprecationRegisterStalenessResult,
    check_deprecation_register_staleness,
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


class _Register:
    def __init__(self, rows, *, raises: Optional[BaseException] = None):
        self._rows = rows
        self._raises = raises
        self.calls = 0

    def __call__(self):
        self.calls += 1
        if self._raises is not None:
            raise self._raises
        return self._rows


class _Feed:
    def __init__(self, entry, *, raises: Optional[BaseException] = None):
        self._entry = entry
        self._raises = raises
        self.calls: list[str] = []

    def __call__(self, affected_model: str):
        self.calls.append(affected_model)
        if self._raises is not None:
            raise self._raises
        if isinstance(self._entry, dict) and any(
            isinstance(k, str) and k == "__by_model__" for k in self._entry
        ):
            return self._entry["__by_model__"].get(affected_model)
        return self._entry


_ANN = datetime(2026, 4, 1, 12, 0, 0, tzinfo=timezone.utc)
_NOW = datetime(2026, 4, 10, 12, 0, 0, tzinfo=timezone.utc)


def _feed_entry(*, announcement: datetime = _ANN) -> dict:
    return {
        "announcement_iso8601": announcement.isoformat(),
        "deprecation_effective_iso8601": announcement.isoformat(),
        "source_url": "https://example.com/deprecation",
    }


def _reg_row(
    *,
    model: str = "moonshotai/kimi-k2-instruct",
    deprecated: bool = True,
    registered_at: Optional[datetime] = _ANN,
    not_deprecated: bool = False,
) -> dict:
    row: dict = {"affected_model": model}
    if deprecated:
        row["deprecated"] = True
    if not_deprecated:
        row["not_deprecated"] = True
    if registered_at is not None:
        row["registered_at_iso8601"] = registered_at.isoformat()
    return row


def _fm(
    *,
    forced: bool = False,
    model: str = "moonshotai/kimi-k2-instruct",
    extra: Optional[dict] = None,
) -> dict:
    fm = {"forced_replacement": forced, "affected_model": model}
    if extra:
        fm.update(extra)
    return fm


# ---------------------------------------------------------------------------
# Baseline / no-op paths
# ---------------------------------------------------------------------------


def test_forced_replacement_true_noop_pass():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(forced=True),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "forced_replacement_not_false_noop"


def test_forced_replacement_missing_is_noop():
    # "forced_replacement" not present → ``get`` returns None → not False → no-op
    r = check_deprecation_register_staleness(
        amendment_frontmatter={"affected_model": "x/y"},
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "forced_replacement_not_false_noop"


def test_forced_replacement_truthy_non_false_is_noop():
    # Truthy non-False (0, "", None) must NOT flip to DENY — only explicit False triggers gate.
    for val in ["false", 0, None, "False", []]:
        r = check_deprecation_register_staleness(
            amendment_frontmatter={"forced_replacement": val, "affected_model": "x/y"},
            clock=_Clock(_NOW),
            deprecation_register_reader=_Register([]),
            deprecation_feed_reader=_Feed(None),
        )
        assert r.success is True, f"val={val!r} unexpectedly denied"
        assert r.detail.reason_tag == "forced_replacement_not_false_noop"


def test_feed_returns_none_passes():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed(None),
    )
    assert r.success is True
    assert r.detail.reason_tag == "feed_reports_no_deprecation"
    assert r.detail.affected_model == "moonshotai/kimi-k2-instruct"


# ---------------------------------------------------------------------------
# Register current vs stale
# ---------------------------------------------------------------------------


def test_register_current_registered_same_time_as_announcement_passes():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([_reg_row(registered_at=_ANN)]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.reason_tag == "register_current_within_window"
    assert r.detail.staleness_hours == 0


def test_register_ahead_of_announcement_passes_clock_skew():
    # Registered 1 hour AFTER announcement (operator saw feed early).
    registered = _ANN + timedelta(hours=1)
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([_reg_row(registered_at=registered)]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.reason_tag == "register_ahead_of_feed_clock_skew"
    assert r.detail.emitted_event == EVENT_CLOCK_SKEW_REGISTER_AHEAD


def test_register_1_hour_behind_passes():
    registered = _ANN - timedelta(hours=1)
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([_reg_row(registered_at=registered)]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.reason_tag == "register_current_within_window"
    assert r.detail.staleness_hours == 1


def test_register_72_hours_behind_passes_at_boundary():
    registered = _ANN - timedelta(hours=72)
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([_reg_row(registered_at=registered)]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.reason_tag == "register_current_within_window"
    assert r.detail.staleness_hours == 72


def test_register_73_hours_behind_denies_stale():
    registered = _ANN - timedelta(hours=73)
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([_reg_row(registered_at=registered)]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_STALE
    assert r.detail.reason_tag == "register_older_than_window"
    assert r.detail.emitted_event == EVENT_STALE
    assert r.detail.staleness_hours == 73


def test_register_1_week_behind_denies_stale():
    registered = _ANN - timedelta(hours=168)
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([_reg_row(registered_at=registered)]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_STALE
    assert r.detail.staleness_hours == 168


# ---------------------------------------------------------------------------
# Register absent
# ---------------------------------------------------------------------------


def test_register_missing_entirely_denies():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_MISSING
    assert r.detail.reason_tag == "register_entry_absent"
    assert r.detail.emitted_event == EVENT_MISSING


def test_register_has_different_model_treated_as_missing():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(model="openai/gpt-4"),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([_reg_row(model="anthropic/claude-2")]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_MISSING


def test_register_has_matching_model_but_deprecated_false_treated_as_missing():
    # Row exists but ``deprecated`` not True and ``not_deprecated`` not True.
    rows = [{"affected_model": "x/y", "deprecated": False,
             "registered_at_iso8601": _ANN.isoformat()}]
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(model="x/y"),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register(rows),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_MISSING


# ---------------------------------------------------------------------------
# Override: not_deprecated: true
# ---------------------------------------------------------------------------


def test_register_not_deprecated_override_passes():
    override_row = {
        "affected_model": "moonshotai/kimi-k2-instruct",
        "not_deprecated": True,
        "registered_at_iso8601": _NOW.isoformat(),
        "evidence_url": "https://example.com/counter-evidence",
    }
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([override_row]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.reason_tag == "register_not_deprecated_override"
    assert r.detail.emitted_event == EVENT_NOT_DEPRECATED_OVERRIDE


def test_register_override_newer_than_deprecated_row_wins():
    # Older deprecated=true then newer not_deprecated=true — most-recent wins.
    older = _reg_row(registered_at=_ANN - timedelta(days=5))
    newer = {
        "affected_model": "moonshotai/kimi-k2-instruct",
        "not_deprecated": True,
        "registered_at_iso8601": _NOW.isoformat(),
    }
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([older, newer]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.reason_tag == "register_not_deprecated_override"


# ---------------------------------------------------------------------------
# Frontmatter defects
# ---------------------------------------------------------------------------


def test_affected_model_missing_denies_ambiguous():
    r = check_deprecation_register_staleness(
        amendment_frontmatter={"forced_replacement": False},
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_AMBIGUOUS
    assert r.detail.reason_tag == "affected_model_missing"


def test_affected_model_not_str_denies_ambiguous():
    r = check_deprecation_register_staleness(
        amendment_frontmatter={"forced_replacement": False, "affected_model": 42},
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_AMBIGUOUS
    assert r.detail.reason_tag == "affected_model_not_str"


def test_affected_model_empty_denies_ambiguous():
    r = check_deprecation_register_staleness(
        amendment_frontmatter={"forced_replacement": False, "affected_model": ""},
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed(None),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_AMBIGUOUS
    assert r.detail.reason_tag == "affected_model_empty"


def test_frontmatter_not_dict_denies_ambiguous():
    for bad in [None, "not a dict", 42, ["list"], ()]:
        r = check_deprecation_register_staleness(
            amendment_frontmatter=bad,  # type: ignore[arg-type]
            clock=_Clock(_NOW),
            deprecation_register_reader=_Register([]),
            deprecation_feed_reader=_Feed(None),
        )
        assert r.success is False
        assert r.failure_code == F_AMDT_09_AMBIGUOUS
        assert r.detail.reason_tag == "frontmatter_not_dict"


# ---------------------------------------------------------------------------
# Reader failures
# ---------------------------------------------------------------------------


def test_feed_reader_raises_denies_reader_fail():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed(None, raises=OSError("net down")),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_READER_FAIL
    assert r.detail.reason_tag == "feed_reader_raised"
    assert "OSError" in (r.detail.reader_error or "")


def test_feed_return_not_dict_or_none_denies():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed("not a dict"),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_READER_FAIL
    assert r.detail.reason_tag == "feed_return_invalid"


def test_feed_announcement_missing_denies():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed({"source_url": "https://e.x"}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_READER_FAIL
    assert r.detail.reason_tag == "feed_announcement_iso8601_missing"


def test_feed_announcement_empty_string_denies():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed({"announcement_iso8601": ""}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "feed_announcement_iso8601_missing"


def test_feed_announcement_unparseable_denies():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([]),
        deprecation_feed_reader=_Feed({"announcement_iso8601": "not-a-timestamp"}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "feed_announcement_iso8601_unparseable"


def test_register_reader_raises_denies_reader_fail():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([], raises=PermissionError("denied")),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_READER_FAIL
    assert r.detail.reason_tag == "register_reader_raised"


def test_register_return_not_list_denies():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register({"not": "a list"}),  # type: ignore[arg-type]
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.detail.reason_tag == "register_return_not_list"


def test_register_row_registered_at_unparseable_denies():
    bad = {
        "affected_model": "moonshotai/kimi-k2-instruct",
        "deprecated": True,
        "registered_at_iso8601": "garbage-timestamp",
    }
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([bad]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_READER_FAIL
    assert r.detail.reason_tag == "register_row_registered_at_iso8601_unparseable"


def test_register_row_missing_registered_at_uses_now_vs_announcement():
    # deprecated=true but no registered_at_iso8601 — gate falls back to
    # now minus announcement as staleness_hours.
    bad = {
        "affected_model": "moonshotai/kimi-k2-instruct",
        "deprecated": True,
    }
    # 9 days = 216 hours; > 72 → STALE.
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([bad]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_STALE
    assert r.detail.staleness_hours == 216


def test_register_row_missing_registered_at_within_72h_passes():
    bad = {
        "affected_model": "moonshotai/kimi-k2-instruct",
        "deprecated": True,
    }
    # 48 hours after announcement.
    now_48h = _ANN + timedelta(hours=48)
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(now_48h),
        deprecation_register_reader=_Register([bad]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.reason_tag == "register_current_within_window"
    assert r.detail.staleness_hours == 48


def test_register_row_missing_registered_at_negative_clamped_to_zero():
    # now is BEFORE announcement — clamps to 0 (clock skew defence).
    bad = {
        "affected_model": "moonshotai/kimi-k2-instruct",
        "deprecated": True,
    }
    now_before = _ANN - timedelta(hours=5)
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(now_before),
        deprecation_register_reader=_Register([bad]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.staleness_hours == 0


def test_register_row_registered_at_non_str_treated_as_missing():
    bad = {
        "affected_model": "moonshotai/kimi-k2-instruct",
        "deprecated": True,
        "registered_at_iso8601": 42,
    }
    now_48h = _ANN + timedelta(hours=48)
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(now_48h),
        deprecation_register_reader=_Register([bad]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.staleness_hours == 48


def test_clock_raises_denies_reader_fail():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW, raises=RuntimeError("ntp offline")),
        deprecation_register_reader=_Register([_reg_row(registered_at=None)]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_READER_FAIL
    assert r.detail.reason_tag == "clock_raised"


def test_clock_returns_non_datetime_denies():
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW, returns="not a datetime"),
        deprecation_register_reader=_Register([_reg_row(registered_at=None)]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_09_READER_FAIL
    assert r.detail.reason_tag == "clock_return_not_datetime"


# ---------------------------------------------------------------------------
# Naive datetime handling
# ---------------------------------------------------------------------------


def test_naive_clock_treated_as_utc():
    bad = {
        "affected_model": "moonshotai/kimi-k2-instruct",
        "deprecated": True,
    }
    naive = datetime(2026, 4, 10, 12, 0, 0)  # tz-naive
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(naive),
        deprecation_register_reader=_Register([bad]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is False  # 9d = 216h > 72h
    assert r.detail.staleness_hours == 216


def test_naive_announcement_treated_as_utc():
    naive_ann = datetime(2026, 4, 1, 12, 0, 0)  # tz-naive
    feed = {
        "announcement_iso8601": naive_ann.isoformat(),
    }
    reg_row = _reg_row(registered_at=_ANN)
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([reg_row]),
        deprecation_feed_reader=_Feed(feed),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Multiple rows — most-recent wins
# ---------------------------------------------------------------------------


def test_multiple_register_rows_most_recent_wins():
    old = _reg_row(registered_at=_ANN - timedelta(days=10))  # stale
    new = _reg_row(registered_at=_ANN - timedelta(hours=1))  # current
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([old, new]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.reason_tag == "register_current_within_window"
    assert r.detail.staleness_hours == 1


def test_multiple_register_rows_non_matching_model_skipped():
    other = _reg_row(model="different/model", registered_at=_NOW)
    target = _reg_row(registered_at=_ANN - timedelta(hours=1))
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([other, target]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.staleness_hours == 1


def test_non_dict_register_rows_skipped():
    rows = ["not a dict", 42, None, _reg_row(registered_at=_ANN)]
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register(rows),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Constants / frozen dataclass identity
# ---------------------------------------------------------------------------


def test_constants():
    assert F_AMDT_09 == "F-AMDT-09"
    assert F_AMDT_09_STALE == "F-AMDT-09-STALE"
    assert F_AMDT_09_MISSING == "F-AMDT-09-MISSING"
    assert F_AMDT_09_AMBIGUOUS == "F-AMDT-09-AMBIGUOUS"
    assert F_AMDT_09_READER_FAIL == "F-AMDT-09-READER-FAIL"
    assert STALENESS_WINDOW_HOURS == 72
    assert EVENT_STALE == "F-AMDT-09-STALE"
    assert EVENT_MISSING == "F-AMDT-09-MISSING"
    assert EVENT_AMBIGUOUS == "F-AMDT-09-AMBIGUOUS"
    assert EVENT_READER_FAIL == "F-AMDT-09-READER-FAIL"
    assert EVENT_NOT_DEPRECATED_OVERRIDE == "F-AMDT-09-NOT-DEPRECATED-OVERRIDE"
    assert EVENT_CLOCK_SKEW_REGISTER_AHEAD == "F-AMDT-09-REGISTER-AHEAD-OF-FEED"


def test_detail_and_result_are_frozen():
    detail = DeprecationRegisterStalenessDetail(
        reason_tag="test", emitted_event="",
        affected_model="", feed_announcement_iso8601="",
        register_registered_at_iso8601="", staleness_hours=0, reader_error=None,
    )
    with pytest.raises(FrozenInstanceError):
        detail.reason_tag = "mutated"  # type: ignore[misc]
    result = DeprecationRegisterStalenessResult(
        success=True, failure_code=None, detail=detail,
    )
    with pytest.raises(FrozenInstanceError):
        result.success = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Parametrized model slug coverage
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "model",
    [
        "moonshotai/kimi-k2-instruct",
        "openai/gpt-4-32k",
        "anthropic/claude-2",
        "google/gemini-1.0-pro",
        "meta/llama-2-70b",
        "mistralai/mistral-7b",
    ],
)
def test_parametric_model_slugs_register_current(model):
    r = check_deprecation_register_staleness(
        amendment_frontmatter=_fm(model=model),
        clock=_Clock(_NOW),
        deprecation_register_reader=_Register([_reg_row(model=model,
                                                        registered_at=_ANN)]),
        deprecation_feed_reader=_Feed(_feed_entry()),
    )
    assert r.success is True
    assert r.detail.affected_model == model
