"""Adversarial tests for F-DAILY-LOG-LOCK-BLOCK-MISSING (F-AMDT-12).

Threat model:
  * Module names that differ by punctuation, case, or Unicode must NOT
    match an existing LOCK block.
  * Heading-style near-misses (``## LOCK:foo`` — no space, or ``# LOCK: foo``
    — single hash) must NOT be treated as valid LOCK headings.
  * Field values that LOOK non-empty but contain only whitespace must be
    rejected as empty (post-strip).
  * Reader / clock raising every common exception → fail-closed.
  * Backfill carve-out is narrow — any of the two markers missing or
    truthy-not-True runs the full gate.
  * Block bodies that embed another ``## LOCK:`` heading inside themselves
    must be split at the inner heading (end-of-block discipline).
  * Fields declared multiple times use the first-occurrence value.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

import pytest

from pipeline.logician.gates import (
    F_AMDT_12,
    F_AMDT_12_MALFORMED,
    F_AMDT_12_MISSING,
    F_AMDT_12_READER_FAIL,
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


def _canonical_block(module: str) -> str:
    return (
        f"## LOCK: {module}\n\n"
        "- `lock_timestamp_utc`: 2026-04-21T00:00:00Z\n"
        "- `committee_round`: r\n"
        "- `verdict`: LOCKED\n"
        "- `code_sha3_512_prefix`: aaaa1111bbbb2222\n"
        "- `tests_added_this_module`: 5\n"
        "- `lines_of_code`: 42\n"
        "- `findings_surfaced_at_lock`: 0\n"
    )


# ---------------------------------------------------------------------------
# ADV-1: heading near-miss formats MUST NOT match
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_heading",
    [
        "## LOCK:foo\n",           # no space after colon
        "## lock: foo\n",          # lowercase
        "# LOCK: foo\n",           # single hash
        "### LOCK: foo\n",         # triple hash
        "##LOCK: foo\n",           # no space after ##
        "## LOCK : foo\n",         # space before colon
        "   ## LOCK: foo\n",       # leading whitespace on line
    ],
)
def test_adv_heading_near_miss_not_matched(bad_heading: str) -> None:
    log_text = (
        bad_heading
        + "- `lock_timestamp_utc`: 2026-04-21T00:00:00Z\n"
        + "- `committee_round`: r\n"
        + "- `verdict`: LOCKED\n"
        + "- `code_sha3_512_prefix`: aaaa1111bbbb2222\n"
        + "- `tests_added_this_module`: 5\n"
        + "- `lines_of_code`: 42\n"
        + "- `findings_surfaced_at_lock`: 0\n"
    )
    r = check_daily_log_lock_block(
        staged_row={"module": "foo"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


# ---------------------------------------------------------------------------
# ADV-2: module name near-miss — exact match required
# ---------------------------------------------------------------------------


def test_adv_module_with_dot_vs_underscore_no_match() -> None:
    log_text = _canonical_block("pipeline.scout.types")
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.scout._types"},  # underscore
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


def test_adv_module_case_mismatch_no_match() -> None:
    log_text = _canonical_block("pipeline.Scout")
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.scout"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


def test_adv_module_homoglyph_no_match() -> None:
    # Cyrillic 'o' vs Latin 'o'
    log_text = _canonical_block("pipeline.f\u043e\u043e")
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.foo"},  # Latin o
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


def test_adv_module_trailing_space_in_staged_row() -> None:
    """staged_row['module'] with trailing whitespace doesn't silently normalise."""
    log_text = _canonical_block("pipeline.foo")
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.foo "},  # trailing space
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


def test_adv_module_substring_not_prefix_match() -> None:
    """If block module is 'pipeline.foo.bar' and staged is 'pipeline.foo',
    gate must NOT prefix-match."""
    log_text = _canonical_block("pipeline.foo.bar")
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.foo"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


# ---------------------------------------------------------------------------
# ADV-3: whitespace-only field values are empty
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_value",
    ["   ", "\t", " \t ", "  \t  "],
)
def test_adv_whitespace_only_field_value_is_empty(bad_value: str) -> None:
    log_text = (
        "## LOCK: pipeline.m\n\n"
        f"- `lock_timestamp_utc`:{bad_value}\n"  # no leading space before value
        "- `committee_round`: r\n"
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
    assert "lock_timestamp_utc" in r.detail.missing_fields


# ---------------------------------------------------------------------------
# ADV-4: reader / clock raising every common exception
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "exc_factory",
    [
        lambda: FileNotFoundError("missing"),
        lambda: PermissionError("denied"),
        lambda: OSError("io"),
        lambda: UnicodeDecodeError("utf-8", b"\xff", 0, 1, "reason"),
        lambda: RuntimeError("unexpected"),
        lambda: ValueError("bad"),
    ],
)
def test_adv_daily_log_reader_raises_fail_closed(exc_factory) -> None:
    def _r(_: str):
        raise exc_factory()

    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.m"},
        clock=_CLOCK,
        daily_log_reader=_r,
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_READER_FAIL
    assert r.detail.reason_tag == "daily_log_reader_raised"


@pytest.mark.parametrize(
    "exc_factory",
    [
        lambda: RuntimeError("clock broken"),
        lambda: OSError("time_t error"),
        lambda: ValueError("bad timezone"),
    ],
)
def test_adv_clock_raises_fail_closed(exc_factory) -> None:
    class _BrokenClock:
        def now_utc(self) -> datetime:
            raise exc_factory()

    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.m"},
        clock=_BrokenClock(),
        daily_log_reader=_reader({}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_READER_FAIL
    assert r.detail.reason_tag == "clock_raised"


# ---------------------------------------------------------------------------
# ADV-5: backfill carve-out strictness
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bogus_backfilled",
    ["true", "True", 1, 1.0, [True]],
)
def test_adv_backfill_truthy_not_True_runs_full_gate(bogus_backfilled: object) -> None:
    r = check_daily_log_lock_block(
        staged_row={
            "module": "pipeline.m",
            "backfilled": bogus_backfilled,
            "verdict": "LOCKED-backfilled",
        },
        clock=_CLOCK,
        daily_log_reader=_reader({}),  # no daily log
    )
    # Gate runs normally since backfilled is not strictly True → no daily
    # log found → F-AMDT-12-MISSING
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


@pytest.mark.parametrize(
    "bogus_verdict",
    ["LOCKED-BACKFILLED", "locked-backfilled", "LOCKED backfilled", "SELF-LOCKED-pending-committee"],
)
def test_adv_backfill_verdict_near_miss_runs_full_gate(bogus_verdict: str) -> None:
    r = check_daily_log_lock_block(
        staged_row={
            "module": "pipeline.m",
            "backfilled": True,
            "verdict": bogus_verdict,
        },
        clock=_CLOCK,
        daily_log_reader=_reader({}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING


def test_adv_backfill_carveout_without_evidence_path_passes() -> None:
    """Evidence-path check is OUT OF SCOPE for F-AMDT-12; carve-out passes
    regardless of backfill_evidence_path presence (separate gate responsibility)."""
    r = check_daily_log_lock_block(
        staged_row={
            "module": "pipeline.old",
            "backfilled": True,
            "verdict": "LOCKED-backfilled",
            # no backfill_evidence_path
        },
        clock=_CLOCK,
        daily_log_reader=_reader({}),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# ADV-6: block body containing an inner LOCK heading is split at the inner
# ---------------------------------------------------------------------------


def test_adv_nested_lock_heading_splits_block_body() -> None:
    log_text = (
        "## LOCK: pipeline.outer\n\n"
        "- `lock_timestamp_utc`: 2026-04-21T00:00:00Z\n"
        "- `committee_round`: r\n"
        "\n"
        "## LOCK: pipeline.inner\n\n"
        "- `verdict`: LOCKED\n"  # inner block's fields
        "- `code_sha3_512_prefix`: aaaa1111bbbb2222\n"
        "- `tests_added_this_module`: 5\n"
        "- `lines_of_code`: 42\n"
        "- `findings_surfaced_at_lock`: 0\n"
    )
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.outer"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MALFORMED
    # Outer block only had 2 fields; 5 missing
    assert len(r.detail.missing_fields) == 5


# ---------------------------------------------------------------------------
# ADV-7: reader returns empty string (zero-byte log exists vs None)
# ---------------------------------------------------------------------------


def test_adv_empty_string_log_denies_block_not_found() -> None:
    """Reader returning '' (empty string) means log exists but has no content
    — distinct from None. Gate reaches block-search and fails there."""
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.m"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": ""}),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MISSING
    assert r.detail.reason_tag == "lock_block_heading_not_found"


# ---------------------------------------------------------------------------
# ADV-8: duplicate field lines — first wins
# ---------------------------------------------------------------------------


def test_adv_duplicate_field_first_wins_passes_if_first_nonempty() -> None:
    log_text = (
        "## LOCK: pipeline.m\n\n"
        "- `lock_timestamp_utc`: 2026-04-21T00:00:00Z\n"
        "- `committee_round`: r\n"
        "- `verdict`: LOCKED\n"
        "- `verdict`: OVERRIDE\n"  # duplicate
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
    # First verdict is non-empty → PASS (duplicate handling is caller's concern)
    assert r.success is True


def test_adv_first_field_empty_second_nonempty_fails() -> None:
    log_text = (
        "## LOCK: pipeline.m\n\n"
        "- `lock_timestamp_utc`:\n"  # empty (first)
        "- `lock_timestamp_utc`: 2026-04-21T00:00:00Z\n"  # non-empty (second)
        "- `committee_round`: r\n"
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
    # First occurrence wins and is empty → MALFORMED
    assert r.success is False
    assert r.failure_code == F_AMDT_12_MALFORMED
    assert "lock_timestamp_utc" in r.detail.missing_fields


# ---------------------------------------------------------------------------
# ADV-9: large daily log with many LOCK blocks — finds target quickly
# ---------------------------------------------------------------------------


def test_adv_large_log_finds_target_block() -> None:
    many_blocks = []
    for i in range(200):
        many_blocks.append(_canonical_block(f"pipeline.mod_{i:03d}"))
    many_blocks.append(_canonical_block("pipeline.target"))
    for i in range(200, 400):
        many_blocks.append(_canonical_block(f"pipeline.mod_{i:03d}"))
    log_text = "\n".join(many_blocks)
    r = check_daily_log_lock_block(
        staged_row={"module": "pipeline.target"},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# ADV-10: module name containing markdown special characters must still
# match character-for-character
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "module",
    [
        "pipeline.logician.gates._protocols",  # leading underscore
        "pipeline.scout.channel_a_federal_apis",
        "pipeline.sovereignty.audit",
        "pipeline.loop.state_checkpoint",
    ],
)
def test_adv_underscore_heavy_module_names_match(module: str) -> None:
    log_text = _canonical_block(module)
    r = check_daily_log_lock_block(
        staged_row={"module": module},
        clock=_CLOCK,
        daily_log_reader=_reader({"2026-04-21": log_text}),
    )
    assert r.success is True
