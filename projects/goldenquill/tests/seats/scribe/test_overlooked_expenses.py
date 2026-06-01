"""Tests for pipeline.seats.scribe.overlooked_expenses — §7.7."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from pipeline.seats.scribe.overlooked_expenses import (
    DEFAULT_CHECKLIST,
    OverlookedExpenseEntry,
    OverlookedExpensesWalk,
    build_default_checklist_walk,
    build_walk,
    is_finalizable,
)


_FIXED = datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)


def _fixed_clock() -> datetime:
    return _FIXED


# ---------------------------------------------------------------------------
# DEFAULT_CHECKLIST sanity
# ---------------------------------------------------------------------------


class TestDefaultChecklist:
    def test_length_eleven(self) -> None:
        assert len(DEFAULT_CHECKLIST) == 11

    def test_is_tuple_of_str(self) -> None:
        assert isinstance(DEFAULT_CHECKLIST, tuple)
        for item in DEFAULT_CHECKLIST:
            assert isinstance(item, str)
            assert item.strip()

    def test_contains_indirect_costs(self) -> None:
        assert any("Indirect" in item for item in DEFAULT_CHECKLIST)

    def test_no_duplicates(self) -> None:
        assert len(set(DEFAULT_CHECKLIST)) == len(DEFAULT_CHECKLIST)


# ---------------------------------------------------------------------------
# OverlookedExpenseEntry shape
# ---------------------------------------------------------------------------


class TestOverlookedExpenseEntry:
    def test_included_with_rationale(self) -> None:
        entry = OverlookedExpenseEntry(
            item="In-kind space",
            status="included",
            rationale="Donated meeting hall at community center",
        )
        assert entry.status == "included"

    def test_n_a_with_rationale(self) -> None:
        entry = OverlookedExpenseEntry(
            item="Indirect costs (if allowed by RFA)",
            status="n_a",
            rationale="RFA prohibits indirect costs",
        )
        assert entry.status == "n_a"

    def test_needed_with_empty_rationale_ok(self) -> None:
        entry = OverlookedExpenseEntry(
            item="Travel",
            status="needed",
            rationale="",
        )
        assert entry.rationale == ""

    def test_included_without_rationale_rejected(self) -> None:
        with pytest.raises(ValueError, match="rationale"):
            OverlookedExpenseEntry(item="X", status="included", rationale="")

    def test_n_a_without_rationale_rejected(self) -> None:
        with pytest.raises(ValueError, match="rationale"):
            OverlookedExpenseEntry(item="X", status="n_a", rationale="  ")

    def test_empty_item_rejected(self) -> None:
        with pytest.raises(ValueError, match="item"):
            OverlookedExpenseEntry(item="", status="needed", rationale="")

    def test_whitespace_item_rejected(self) -> None:
        with pytest.raises(ValueError, match="item"):
            OverlookedExpenseEntry(item="   ", status="needed", rationale="")

    def test_invalid_status_rejected(self) -> None:
        with pytest.raises(ValueError, match="status"):
            OverlookedExpenseEntry(
                item="X",
                status="bogus",  # type: ignore[arg-type]
                rationale="",
            )

    def test_is_frozen(self) -> None:
        e = OverlookedExpenseEntry(item="X", status="needed")
        with pytest.raises(Exception):
            e.item = "Y"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# OverlookedExpensesWalk shape
# ---------------------------------------------------------------------------


class TestOverlookedExpensesWalk:
    def test_happy_path(self) -> None:
        entries = (
            OverlookedExpenseEntry(item="A", status="included", rationale="done"),
            OverlookedExpenseEntry(item="B", status="needed"),
        )
        walk = OverlookedExpensesWalk(
            walk_at_utc=_FIXED,
            entries=entries,
            needed_count=1,
            rfa_indirect_costs_allowed=True,
        )
        assert walk.needed_count == 1

    def test_needed_count_zero(self) -> None:
        entries = (
            OverlookedExpenseEntry(item="A", status="included", rationale="done"),
            OverlookedExpenseEntry(item="B", status="n_a", rationale="not applicable"),
        )
        walk = OverlookedExpensesWalk(
            walk_at_utc=_FIXED,
            entries=entries,
            needed_count=0,
            rfa_indirect_costs_allowed=False,
        )
        assert walk.needed_count == 0

    def test_needed_count_mismatch_rejected(self) -> None:
        entries = (OverlookedExpenseEntry(item="A", status="needed"),)
        with pytest.raises(ValueError, match="needed_count"):
            OverlookedExpensesWalk(
                walk_at_utc=_FIXED,
                entries=entries,
                needed_count=5,
                rfa_indirect_costs_allowed=None,
            )

    def test_naive_walk_at_rejected(self) -> None:
        entries = (OverlookedExpenseEntry(item="A", status="needed"),)
        with pytest.raises(ValueError, match="timezone-aware"):
            OverlookedExpensesWalk(
                walk_at_utc=datetime(2026, 4, 21, 12, 0, 0),
                entries=entries,
                needed_count=1,
                rfa_indirect_costs_allowed=None,
            )

    def test_negative_needed_count_rejected(self) -> None:
        # needed_count=-1 fails the mismatch guard (actual is always >= 0).
        entries = (OverlookedExpenseEntry(item="A", status="included", rationale="x"),)
        with pytest.raises(ValueError, match="needed_count"):
            OverlookedExpensesWalk(
                walk_at_utc=_FIXED,
                entries=entries,
                needed_count=-1,
                rfa_indirect_costs_allowed=None,
            )


# ---------------------------------------------------------------------------
# build_walk
# ---------------------------------------------------------------------------


class TestBuildWalk:
    def test_from_tuple(self) -> None:
        entries = (
            OverlookedExpenseEntry(item="A", status="needed"),
            OverlookedExpenseEntry(item="B", status="included", rationale="done"),
        )
        walk = build_walk(entries, rfa_indirect_costs_allowed=True, clock=_fixed_clock)
        assert walk.needed_count == 1
        assert walk.walk_at_utc == _FIXED

    def test_from_list_normalized(self) -> None:
        entries = [
            OverlookedExpenseEntry(item="A", status="needed"),
            OverlookedExpenseEntry(item="B", status="needed"),
        ]
        walk = build_walk(entries, rfa_indirect_costs_allowed=None, clock=_fixed_clock)
        assert isinstance(walk.entries, tuple)
        assert walk.needed_count == 2

    def test_default_clock_is_utc(self) -> None:
        entries = (OverlookedExpenseEntry(item="A", status="needed"),)
        walk = build_walk(entries, rfa_indirect_costs_allowed=None)
        assert walk.walk_at_utc.tzinfo == timezone.utc


# ---------------------------------------------------------------------------
# build_default_checklist_walk
# ---------------------------------------------------------------------------


class TestBuildDefaultChecklistWalk:
    def test_all_eleven_items_needed(self) -> None:
        walk = build_default_checklist_walk(
            rfa_indirect_costs_allowed=True, clock=_fixed_clock
        )
        assert len(walk.entries) == 11
        assert walk.needed_count == 11
        for e in walk.entries:
            assert e.status == "needed"
            assert e.rationale == ""

    def test_preserves_default_checklist_order(self) -> None:
        walk = build_default_checklist_walk(
            rfa_indirect_costs_allowed=None, clock=_fixed_clock
        )
        items = tuple(e.item for e in walk.entries)
        assert items == DEFAULT_CHECKLIST

    def test_rfa_indirect_costs_flag_preserved(self) -> None:
        walk = build_default_checklist_walk(
            rfa_indirect_costs_allowed=False, clock=_fixed_clock
        )
        assert walk.rfa_indirect_costs_allowed is False


# ---------------------------------------------------------------------------
# is_finalizable
# ---------------------------------------------------------------------------


class TestIsFinalizable:
    def test_zero_needed_finalizable(self) -> None:
        entries = (
            OverlookedExpenseEntry(item="A", status="included", rationale="done"),
        )
        walk = build_walk(entries, rfa_indirect_costs_allowed=None, clock=_fixed_clock)
        assert is_finalizable(walk) is True

    def test_one_needed_not_finalizable(self) -> None:
        entries = (OverlookedExpenseEntry(item="A", status="needed"),)
        walk = build_walk(entries, rfa_indirect_costs_allowed=None, clock=_fixed_clock)
        assert is_finalizable(walk) is False

    def test_default_checklist_walk_not_finalizable(self) -> None:
        walk = build_default_checklist_walk(
            rfa_indirect_costs_allowed=None, clock=_fixed_clock
        )
        assert is_finalizable(walk) is False
