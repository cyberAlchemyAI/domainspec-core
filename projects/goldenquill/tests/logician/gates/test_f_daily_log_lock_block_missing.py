"""Unit tests for F-DAILY-LOG-LOCK-BLOCK-MISSING (F-AMDT-12)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

import pytest

from pipeline.logician.gates import (
    F_AMDT_12,
    F_AMDT_12_MALFORMED,
    F_AMDT_12_MISSING,
    F_AMDT_12_READER_FAIL,
    DailyLogBlockDetail,
    DailyLogBlockResult,
    check_daily_log_lock_block,
)


class _FixedClock:
    def __init__(self, iso: str) -> None:
        self._dt = datetime.fromisoformat(iso)

    def now_utc(self) -> datetime:
        return self._dt


_CLOCK = _FixedClock("2026-04-21T00:30:00+00:00")


def _reader(text_by_date: dict[str, Optional[str]]):
    def _r(date_iso: str) -> Optional[str]:
        return text_by_date.get(date_iso)
    return _r


def _canonical_block(
    module: str = "pipeline.logician.gates.f_bootstrap_reuse",
    *,
    lock_ts: str = "2026-04-20T22:30:00Z",
    committee: str = "logician_v2_2_wave_2_f_amdt_01",
    verdict: str = "LOCKED",
    sha: str = "cce8a1efd1612a74",
    tests_added: int = 74,
    loc: int = 127,
    findings: int = 0,
) -> str:
    return (
        f"## LOCK: {module}\n\n"
        f"- `lock_timestamp_utc`: {lock_ts}\n"
        f"- `committee_round`: {committee}\n"
        f"- `verdict`: {verdict}\n"
        f"- `code_sha3_512_prefix`: {sha}\n"
        f"- `tests_added_this_module`: {tests_added}\n"
        f"- `lines_of_code`: {loc}\n"
        f"- `findings_surfaced_at_lock`: {findings}\n"
    )


# ---------------------------------------------------------------------------
# Happy paths
# ---------------------------------------------------------------------------


def test_canonical_block_passes() -> None:
    log_text = "# Daily log 2026-04-21\n\n" + _canonical_block()
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.logician.gates.f_bootstrap_reuse"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is True
    assert r.detail is None


def test_block_after_other_content_passes() -> None:
    log_text = (
        "# Daily log 2026-04-21\n\n"
        "Some preamble text.\n\n"
        "## Other Section\n\n"
        "Prose.\n\n"
        + _canonical_block()
        + "\n## Later Section\n\nMore prose.\n"
    )
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.logician.gates.f_bootstrap_reuse"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is True


def test_multiple_lock_blocks_finds_matching_module() -> None:
    log_text = (
        _canonical_block("pipeline.scout.channel_a")
        + "\n"
        + _canonical_block("pipeline.scout.channel_b", sha="d405ddd9cb7caf53", tests_added=60, loc=482)
        + "\n"
        + _canonical_block("pipeline.scout.channel_c", sha="eedd40b7e42502b9", tests_added=98, loc=673)
    )
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.scout.channel_b"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is True


def test_block_heading_trailing_whitespace_tolerated() -> None:
    log_text = (
        "## LOCK: pipeline.foo   \n\n"  # trailing spaces on heading
        "- `lock_timestamp_utc`: 2026-04-21T00:00:00Z\n"
        "- `committee_round`: round_x\n"
        "- `verdict`: LOCKED\n"
        "- `code_sha3_512_prefix`: aaaa1111bbbb2222\n"
        "- `tests_added_this_module`: 5\n"
        "- `lines_of_code`: 42\n"
        "- `findings_surfaced_at_lock`: 0\n"
    )
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.foo"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is True


def test_tests_added_value_zero_is_valid() -> None:
    """Zero is a legitimate value — the field must be present with '0', not empty."""
    log_text = _canonical_block(tests_added=0, findings=0)
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.logician.gates.f_bootstrap_reuse"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is True


def test_fields_in_any_order_pass() -> None:
    log_text = (
        "## LOCK: pipeline.m\n\n"
        "- `findings_surfaced_at_lock`: 0\n"
        "- `lines_of_code`: 10\n"
        "- `tests_added_this_module`: 20\n"
        "- `code_sha3_512_prefix`: abcd1234abcd1234\n"
        "- `verdict`: LOCKED\n"
        "- `committee_round`: r\n"
        "- `lock_timestamp_utc`: 2026-04-21T00:00:00Z\n"
    )
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.m"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is True


def test_extra_fields_ignored() -> None:
    log_text = _canonical_block() + "- `notes`: extra bullet\n- `reviewer`: anthropic\n"
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.logician.gates.f_bootstrap_reuse"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# MISSING paths
# ---------------------------------------------------------------------------


def test_daily_log_absent_denies() -> None:
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.logician.gates.f_bootstrap_reuse"},
        clock=_CLOCK,
        daily_log_reader=_reader({}),  # reader returns None for every key
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING
    assert r.detail.reason_tag == "daily_log_absent_for_today"
    assert r.detail.today_iso == "2026-04-21"


def test_block_absent_denies() -> None:
    log_text = "# Daily log 2026-04-21\n\nNo lock blocks here.\n"
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.logician.gates.f_bootstrap_reuse"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING
    assert r.detail.reason_tag == "lock_block_heading_not_found"


def test_block_for_different_module_denies() -> None:
    log_text = _canonical_block("pipeline.other_module")
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.target_module"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


# ---------------------------------------------------------------------------
# MALFORMED paths — missing individual fields
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "missing_field",
    [
        "lock_timestamp_utc",
        "committee_round",
        "verdict",
        "code_sha3_512_prefix",
        "tests_added_this_module",
        "lines_of_code",
        "findings_surfaced_at_lock",
    ],
)
def test_missing_single_field_denies_malformed(missing_field: str) -> None:
    block = _canonical_block()
    # Drop the missing_field line
    lines = [l for l in block.split("\n") if f"`{missing_field}`" not in l]
    log_text = "\n".join(lines)
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.logician.gates.f_bootstrap_reuse"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MALFORMED
    assert missing_field in r.detail.missing_fields


def test_multiple_missing_fields_reported_in_detail() -> None:
    log_text = (
        "## LOCK: pipeline.m\n\n"
        "- `lock_timestamp_utc`: 2026-04-21T00:00:00Z\n"
        "- `verdict`: LOCKED\n"
    )
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.m"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MALFORMED
    # 5 fields missing
    assert len(r.detail.missing_fields) == 5
    for field in (
        "committee_round",
        "code_sha3_512_prefix",
        "tests_added_this_module",
        "lines_of_code",
        "findings_surfaced_at_lock",
    ):
        assert field in r.detail.missing_fields


def test_empty_field_value_denies_malformed() -> None:
    log_text = (
        "## LOCK: pipeline.m\n\n"
        "- `lock_timestamp_utc`: 2026-04-21T00:00:00Z\n"
        "- `committee_round`: \n"  # empty value
        "- `verdict`: LOCKED\n"
        "- `code_sha3_512_prefix`: aaaa1111bbbb2222\n"
        "- `tests_added_this_module`: 5\n"
        "- `lines_of_code`: 42\n"
        "- `findings_surfaced_at_lock`: 0\n"
    )
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.m"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MALFORMED
    assert "committee_round" in r.detail.missing_fields


# ---------------------------------------------------------------------------
# Staged row shape failures
# ---------------------------------------------------------------------------


def test_missing_module_field_denies() -> None:
    r = check_daily_log_lock_block(
        staged_row={"verdict": "LOCKED"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": _canonical_block()}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12
    assert r.detail.reason_tag == "staged_row_module_missing"


def test_empty_string_module_denies() -> None:
    r = check_daily_log_lock_block(
        staged_row={"module": ""},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": _canonical_block()}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "staged_row_module_missing"


def test_non_string_module_denies() -> None:
    r = check_daily_log_lock_block(
        staged_row={"module": 42},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": _canonical_block()}),
    )
    assert r.success is False
    assert r.detail.reason_tag == "staged_row_module_missing"


# ---------------------------------------------------------------------------
# Backfill carve-out
# ---------------------------------------------------------------------------


def test_backfill_carveout_passes_without_daily_log() -> None:
    r = check_daily_log_lock_block(
        staged_row={
            "module": "pipeline.old_module",
            "backfilled": True,
            "verdict": "LOCKED-backfilled",
        },
        clock=_CLOCK,
        daily_log_reader=_reader({}),  # no daily log at all
    )
    assert r.success is True


def test_backfill_carveout_requires_both_markers_backfilled_only() -> None:
    """backfilled: true but verdict != 'LOCKED-backfilled' runs full gate."""
    r = check_daily_log_lock_block(
        staged_row={
            "module": "pipeline.old_module",
            "backfilled": True,
            "verdict": "LOCKED",
        },
        clock=_CLOCK,
        daily_log_reader=_reader({}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


def test_backfill_carveout_requires_both_markers_verdict_only() -> None:
    """verdict == 'LOCKED-backfilled' but backfilled != true runs full gate."""
    r = check_daily_log_lock_block(
        staged_row={
            "module": "pipeline.old_module",
            "verdict": "LOCKED-backfilled",
        },
        clock=_CLOCK,
        daily_log_reader=_reader({}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


def test_backfill_carveout_backfilled_string_not_true_runs_gate() -> None:
    """Strict identity: backfilled: 'true' (string) is NOT True; runs full gate."""
    r = check_daily_log_lock_block(
        staged_row={
            "module": "pipeline.old_module",
            "backfilled": "true",
            "verdict": "LOCKED-backfilled",
        },
        clock=_CLOCK,
        daily_log_reader=_reader({}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


# ---------------------------------------------------------------------------
# Reader / clock failure paths
# ---------------------------------------------------------------------------


def test_reader_raises_fail_closed() -> None:
    def _r(_: str):
        raise FileNotFoundError("daily log i/o error")

    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.m"},
        clock=_CLOCK,
        daily_log_reader=_r,
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_READER_FAIL
    assert r.detail.reason_tag == "daily_log_reader_raised"
    assert "FileNotFoundError" in r.detail.reader_error


def test_clock_raises_fail_closed() -> None:
    class _BrokenClock:
        def now_utc(self) -> datetime:
            raise RuntimeError("clock broken")

    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.m"},
        clock=_BrokenClock(),
        daily_log_reader=_reader({"2026-04-21": _canonical_block()}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_READER_FAIL
    assert r.detail.reason_tag == "clock_raised"


# ---------------------------------------------------------------------------
# Result shape
# ---------------------------------------------------------------------------


def test_result_is_frozen() -> None:
    r = check_daily_log_lock_block(
        staged_row={"module": ""},
        clock=_CLOCK,
        daily_log_reader=_reader({}),
    )
    with pytest.raises((AttributeError, TypeError)):
        r.success = True  # type: ignore[misc]


def test_detail_is_frozen() -> None:
    r = check_daily_log_lock_block(
        staged_row={"module": ""},
        clock=_CLOCK,
        daily_log_reader=_reader({}),
    )
    assert r.detail is not None
    with pytest.raises((AttributeError, TypeError)):
        r.detail.reason_tag = "other"  # type: ignore[misc]


def test_success_detail_is_none() -> None:
    log_text = _canonical_block()
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.logician.gates.f_bootstrap_reuse"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.detail is None
    assert r.failure_code is None


# ---------------------------------------------------------------------------
# Block-boundary / next-heading handling
# ---------------------------------------------------------------------------


def test_next_heading_truncates_block_body() -> None:
    """Fields declared AFTER the next ## heading must NOT be seen — that's
    the next block, not this one."""
    log_text = (
        "## LOCK: pipeline.m\n\n"
        "- `lock_timestamp_utc`: 2026-04-21T00:00:00Z\n"
        "- `committee_round`: r\n"
        "\n"
        "## Other Section\n\n"
        "- `verdict`: LOCKED\n"  # these fields belong to the next section
        "- `code_sha3_512_prefix`: abcd1234abcd1234\n"
        "- `tests_added_this_module`: 5\n"
        "- `lines_of_code`: 10\n"
        "- `findings_surfaced_at_lock`: 0\n"
    )
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.m"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MALFORMED
    # First 2 fields present; 5 remaining fields missing
    assert set(r.detail.missing_fields) == {
        "verdict",
        "code_sha3_512_prefix",
        "tests_added_this_module",
        "lines_of_code",
        "findings_surfaced_at_lock",
    }


def test_block_at_end_of_file() -> None:
    log_text = "# Daily log\n\n" + _canonical_block()  # no trailing content
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.logician.gates.f_bootstrap_reuse"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Module name parametrization — exact-match discipline
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "module",
    [
        "pipeline.sovereignty.audit",
        "pipeline.vault.mirror_verify",
        "pipeline.logician.gates.f_bootstrap_reuse",
        "pipeline.loop.seat_runner",
        "pipeline.scout.channel_a_federal_apis",
    ],
)
def test_parametrized_over_module_names(module: str) -> None:
    log_text = _canonical_block(module)
    r = check_daily_log_lock_block(
        staged_row={"module": module},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is True


def test_today_iso_uses_utc_date() -> None:
    """Clock-derived date drives reader key. Clock in UTC 2026-04-21T00:30 →
    today_iso == 2026-04-21."""
    calls: list[str] = []

    def _r(date_iso: str):
        calls.append(date_iso)
        return None

    check_daily_log_lock_block(
        staged_row={"module": "pipeline.m"},
        clock=_CLOCK,
        daily_log_reader=_r,
    )
    assert calls == ["2026-04-21"]


def test_reader_called_exactly_once_per_check() -> None:
    calls: list[str] = []

    def _r(date_iso: str):
        calls.append(date_iso)
        return _canonical_block()

    check_daily_log_lock_block(
        staged_row={"module": "pipeline.logician.gates.f_bootstrap_reuse"},
        clock=_CLOCK,
        daily_log_reader=_r,
    )
    assert len(calls) == 1


def test_reader_not_called_on_backfill_carveout() -> None:
    calls: list[str] = []

    def _r(date_iso: str):
        calls.append(date_iso)
        return _canonical_block()

    r = check_daily_log_lock_block(
        staged_row={
            "module": "pipeline.old",
            "backfilled": True,
            "verdict": "LOCKED-backfilled",
        },
        clock=_CLOCK,
        daily_log_reader=_r,
    )
    assert r.success is True
    assert calls == []
