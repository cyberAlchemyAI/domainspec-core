"""pipeline.seats.scribe.overlooked_expenses — §7.7 overlooked-expenses walker.

Blueprint §7 Scribe v1.1.1 §7.7 LOCKED 2026-04-21. Pure data + pure
predicate. Zero I/O, zero LLM, zero external-package imports.

R2 ships the ``OverlookedExpensesWalk`` shape, the default 11-item
checklist per §7.7, and the ``is_finalizable`` predicate. Runtime POST-gate
``F-SCRIBE-OVERLOOKED-EXPENSE-UNRESOLVED`` wiring lands at R3.

Non-bypassable invariant (§7.7): Scribe cannot emit a finalized
`SectionDraft` for the Budget section with ``needed_count > 0``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Final, Literal


ExpenseStatus = Literal["included", "n_a", "needed"]

_EXPENSE_STATUS_VALID: Final[frozenset[str]] = frozenset(
    {"included", "n_a", "needed"}
)


# §7.7 — 11 default checklist items. Closed-set at v1.1; operator may
# supplement via extra entries in a walk (the DEFAULT_CHECKLIST is the
# floor, not the ceiling).
DEFAULT_CHECKLIST: Final[tuple[str, ...]] = (
    "In-kind space and utilities",
    "Volunteer / board labor (match value)",
    "Printing, postage, branding, translation",
    "Audit and grant-reporting costs",
    "Compliance (FDA, GAP, organic, FSMA)",
    "Travel / mileage for outreach",
    "Evaluation / data collection tools",
    "Insurance and legal fees",
    "Packaging, storage, freight",
    "Training and professional development",
    "Indirect costs (if allowed by RFA)",
)


ClockFn = Callable[[], datetime]


def _default_utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


@dataclass(frozen=True, kw_only=True, slots=True)
class OverlookedExpenseEntry:
    """One line-item of the checklist walk."""

    item: str
    status: ExpenseStatus
    rationale: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.item, str) or not self.item.strip():
            raise ValueError("OverlookedExpenseEntry.item must be non-empty.")
        if self.status not in _EXPENSE_STATUS_VALID:
            raise ValueError(
                f"OverlookedExpenseEntry.status must be one of "
                f"{sorted(_EXPENSE_STATUS_VALID)}; got {self.status!r}."
            )
        # When status is "included" or "n_a" the operator has affirmed a
        # disposition — require a non-empty rationale. "needed" may have
        # empty rationale because it routes to operator-fill.
        if self.status in ("included", "n_a") and not self.rationale.strip():
            raise ValueError(
                f"OverlookedExpenseEntry({self.item!r}, status={self.status!r}) "
                f"requires a non-empty rationale."
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class OverlookedExpensesWalk:
    """§7.7 walk record — timestamp + entries + derived count + RFA flag."""

    walk_at_utc: datetime
    entries: tuple[OverlookedExpenseEntry, ...]
    needed_count: int
    rfa_indirect_costs_allowed: bool | None

    def __post_init__(self) -> None:
        if self.walk_at_utc.tzinfo is None:
            raise ValueError(
                "OverlookedExpensesWalk.walk_at_utc must be timezone-aware."
            )
        actual = sum(1 for e in self.entries if e.status == "needed")
        if self.needed_count != actual:
            raise ValueError(
                f"OverlookedExpensesWalk.needed_count={self.needed_count!r} "
                f"does not match actual count of needed entries ({actual})."
            )
        # needed_count >= 0 is implicit: ``actual`` is always >= 0 and the
        # equality check above guarantees ``needed_count == actual``.


def build_walk(
    entries: tuple[OverlookedExpenseEntry, ...] | list[OverlookedExpenseEntry],
    *,
    rfa_indirect_costs_allowed: bool | None,
    clock: ClockFn = _default_utc_now,
) -> OverlookedExpensesWalk:
    """Construct an :class:`OverlookedExpensesWalk` computing ``needed_count``
    correctly from ``entries``.

    Accepts list or tuple; normalizes to tuple. Clock is injected via E-017.
    """
    entries_tuple = tuple(entries)
    needed = sum(1 for e in entries_tuple if e.status == "needed")
    return OverlookedExpensesWalk(
        walk_at_utc=clock(),
        entries=entries_tuple,
        needed_count=needed,
        rfa_indirect_costs_allowed=rfa_indirect_costs_allowed,
    )


def is_finalizable(walk: OverlookedExpensesWalk) -> bool:
    """§7.7 pin — True iff walk can be finalized as a Budget section.

    Finalization requires zero ``status == "needed"`` entries. R3 POST-gate
    ``F-SCRIBE-OVERLOOKED-EXPENSE-UNRESOLVED`` trips when a finalize attempt
    calls this and gets False.
    """
    return walk.needed_count == 0


def build_default_checklist_walk(
    *,
    rfa_indirect_costs_allowed: bool | None,
    clock: ClockFn = _default_utc_now,
) -> OverlookedExpensesWalk:
    """Convenience builder: create a walk with every DEFAULT_CHECKLIST item
    marked ``"needed"`` (initial operator-fill state).

    Used by R3 to bootstrap a fresh walk at budget-section build start.
    """
    entries = tuple(
        OverlookedExpenseEntry(item=item, status="needed", rationale="")
        for item in DEFAULT_CHECKLIST
    )
    return build_walk(
        entries,
        rfa_indirect_costs_allowed=rfa_indirect_costs_allowed,
        clock=clock,
    )


__all__ = [
    "ExpenseStatus",
    "DEFAULT_CHECKLIST",
    "OverlookedExpenseEntry",
    "OverlookedExpensesWalk",
    "ClockFn",
    "build_walk",
    "build_default_checklist_walk",
    "is_finalizable",
]
