"""F-CIC-CLC-MATCH-NULL — runtime presence check for applicant CIC × opportunity CLC.

PRE-gate at order 6.6. Fires at the start of every grant cycle (and at any
seat invocation that reads either field). Fail-closed AFTER the per-org
migration dormancy expires per v7.0.8 §10. During an org's dormancy window,
the gate emits WARNING logs only (admin-risk LOW severity ledger entry per
cycle attempt) and does not block.

Authority: ``pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md`` §4.2
(LOCKED 2026-05-08).

Subcodes
--------
- ``F-CIC-CLC-MATCH-NULL.cic_unset`` — applicant ``cic_active`` is unset/empty
- ``F-CIC-CLC-MATCH-NULL.cic_invalid`` — applicant ``cic_active`` contains a
  value not in ``CustomerIdentityCategory``
- ``F-CIC-CLC-MATCH-NULL.clc_unset`` — opportunity ``clc_assigned`` is unset
- ``F-CIC-CLC-MATCH-NULL.clc_invalid`` — opportunity ``clc_assigned`` is a
  value not in ``CapitalLogicCard``

Design notes
------------
- Gate code does NO file I/O. The caller (gate_runner / pipeline orchestrator)
  injects parsed PROJECT_CONTEXT data, opportunity record, and migration-state
  reader callable.
- Per-org dormancy clock (per v7.0.8 §10 / Cycle-1 RT-06 fix): the migration
  reader returns ``None`` during dormancy and ``False`` after expiry. Gate
  treats ``None`` as "WARNING only" and ``False`` as "fail-closed enforced."
- Gate is purely deterministic. No LLM call. Zero token cost (per Logician
  discipline in CLAUDE.md § The Council).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, runtime_checkable

from pipeline.types import (
    CAPITAL_LOGIC_CARD_VALUES,
    CUSTOMER_IDENTITY_CATEGORY_VALUES,
)


GATE_ID = "F-CIC-CLC-MATCH-NULL"
PRE_GATE_ORDER = 6.6


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MatchNullResult:
    """Result of running F-CIC-CLC-MATCH-NULL for one (org, opportunity) pair.

    ``passed=True`` means both sides present and valid → cycle proceeds.
    ``passed=False`` AND ``enforced=True`` → fail-closed; pipeline halts.
    ``passed=False`` AND ``enforced=False`` → dormancy WARNING only; cycle proceeds.
    """

    passed: bool
    enforced: bool
    subcodes: tuple[str, ...]
    detail: str


# ---------------------------------------------------------------------------
# Injected dependencies (no direct file I/O in gate code)
# ---------------------------------------------------------------------------


@runtime_checkable
class ProjectContextReaderCallable(Protocol):
    """Returns the ``cic_active`` list for the active org.

    ``None`` signals "field not present in PROJECT_CONTEXT.md."
    Empty list signals "field present but empty."
    Non-empty list of strings is the operator-set CIC selection.

    Raising is the fail-closed signal — caller's responsibility to catch and
    convert to a structured cycle-halt outcome.
    """

    def __call__(self, org_slug: str) -> Optional[list[str]]: ...


@runtime_checkable
class OpportunityCLCReaderCallable(Protocol):
    """Returns the ``clc_assigned`` value for the active opportunity.

    ``None`` signals "Scout VERIFY did not assign a CLC" (e.g., confidence
    below threshold; awaiting operator REVIEW).
    Non-empty string is the CLC ID.

    Raising is the fail-closed signal.
    """

    def __call__(self, opportunity_id: str) -> Optional[str]: ...


@runtime_checkable
class DormancyStateReaderCallable(Protocol):
    """Returns whether F-CIC-CLC-MATCH-NULL is enforced for the given org.

    Returns:
        ``True``  — dormancy expired; fail-closed enforced
        ``False`` — never-attempted-cycle pre-state; gate should not fire
                    yet (no cycle has been attempted, so no WARNING needed)
        ``None``  — dormancy active; emit WARNING but do not block

    Per v7.0.8 §10: each org's dormancy is tracked in
    ``orgs/<slug>/vault/migration_state.yaml`` with ``first_attempt_iso8601``
    and ``dormancy_expires_iso8601`` fields. The reader resolves these against
    a clock and returns the tri-state.

    Raising is the fail-closed signal.
    """

    def __call__(self, org_slug: str) -> Optional[bool]: ...


# ---------------------------------------------------------------------------
# Gate implementation
# ---------------------------------------------------------------------------


def run(
    *,
    org_slug: str,
    opportunity_id: str,
    project_context_reader: ProjectContextReaderCallable,
    opportunity_clc_reader: OpportunityCLCReaderCallable,
    dormancy_reader: DormancyStateReaderCallable,
) -> MatchNullResult:
    """Run F-CIC-CLC-MATCH-NULL for one (org, opportunity) pair.

    The injected readers are the only sanctioned route to PROJECT_CONTEXT.md,
    opportunity records, and migration state. Gate code performs no file I/O.

    Returns a ``MatchNullResult``. The caller decides what to do with
    ``passed=False`` based on ``enforced``.
    """
    # Read both sides (fail-closed if reader raises — caller's responsibility)
    cic_active = project_context_reader(org_slug)
    clc_assigned = opportunity_clc_reader(opportunity_id)

    subcodes: list[str] = []
    detail_parts: list[str] = []

    # ---- CIC side ----
    if cic_active is None or len(cic_active) == 0:
        subcodes.append(f"{GATE_ID}.cic_unset")
        detail_parts.append(
            f"PROJECT_CONTEXT[{org_slug}].cic_active is unset or empty"
        )
    else:
        invalid_cics = [
            cic for cic in cic_active
            if cic not in CUSTOMER_IDENTITY_CATEGORY_VALUES
        ]
        if invalid_cics:
            subcodes.append(f"{GATE_ID}.cic_invalid")
            detail_parts.append(
                f"PROJECT_CONTEXT[{org_slug}].cic_active contains "
                f"non-canonical IDs: {invalid_cics}"
            )

    # ---- CLC side ----
    if clc_assigned is None or clc_assigned == "":
        subcodes.append(f"{GATE_ID}.clc_unset")
        detail_parts.append(
            f"opportunity[{opportunity_id}].clc_assigned is unset"
        )
    elif clc_assigned not in CAPITAL_LOGIC_CARD_VALUES:
        subcodes.append(f"{GATE_ID}.clc_invalid")
        detail_parts.append(
            f"opportunity[{opportunity_id}].clc_assigned has non-canonical "
            f"ID: {clc_assigned!r}"
        )

    # ---- Dormancy resolution ----
    if not subcodes:
        return MatchNullResult(
            passed=True,
            enforced=True,
            subcodes=(),
            detail="both CIC and CLC present and canonical",
        )

    dormancy_state = dormancy_reader(org_slug)

    if dormancy_state is False:
        # Pre-first-attempt — gate does not fire yet.
        return MatchNullResult(
            passed=True,
            enforced=False,
            subcodes=tuple(subcodes),
            detail=(
                "issues found but pre-first-cycle-attempt for org "
                f"{org_slug!r}; dormancy clock not yet started; "
                + "; ".join(detail_parts)
            ),
        )

    enforced = dormancy_state is True
    return MatchNullResult(
        passed=False,
        enforced=enforced,
        subcodes=tuple(subcodes),
        detail=(
            ("ENFORCED: " if enforced else "DORMANCY-WARNING: ")
            + "; ".join(detail_parts)
        ),
    )
