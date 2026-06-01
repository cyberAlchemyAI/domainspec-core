"""commitment_id safe-identifier sanitization — backward-compat re-export shim.

Per §11 v1.1 amendment LOCKED 2026-05-11: the canonical declaration of
the commitment_id safe-identifier contract was relocated from this
module to the shared producer/consumer sibling at
``pipeline.orchestrator.seats._commitment_id``. This module is retained
as a backward-compatibility re-export shim so existing §14 v1 LOCK
imports (lock_history rows 200/201, 2026-05-10) continue to resolve
without modification.

DO NOT add new declarations here. New consumers (within §14 or any
other seat) SHOULD import from the canonical home:

    from pipeline.orchestrator.seats._commitment_id import (
        SAFE_COMMITMENT_ID_REGEX,
        SAFE_COMMITMENT_ID_PATTERN,
        COMMITMENT_ID_MAX_LEN,
        CommitmentIdInvalid,
        is_safe_commitment_id,
        sanitize_commitment_id,
    )

This shim preserves the §14 v1 LOCK import surface; the existing §14
modules (``pipeline.logician.gates.f_report_commitment_missed``,
``pipeline.orchestrator.seats.report_generator._schemas``,
``pipeline.logician.gates._report_protocols``) continue to import from
this path. A future §14 minor amendment may migrate those imports to
the canonical home; the shim then retires by removal.

The shim re-exports the public surface (per __all__ below) verbatim.
The exception identity (``CommitmentIdInvalid``) is preserved across
both import paths — ``isinstance(exc, CommitmentIdInvalid)`` works
regardless of which import path the caller used.
"""

from __future__ import annotations

from pipeline.orchestrator.seats._commitment_id import (
    COMMITMENT_ID_MAX_LEN,
    CommitmentIdInvalid,
    SAFE_COMMITMENT_ID_PATTERN,
    SAFE_COMMITMENT_ID_REGEX,
    is_safe_commitment_id,
    sanitize_commitment_id,
)


__all__ = [
    "COMMITMENT_ID_MAX_LEN",
    "CommitmentIdInvalid",
    "SAFE_COMMITMENT_ID_PATTERN",
    "SAFE_COMMITMENT_ID_REGEX",
    "is_safe_commitment_id",
    "sanitize_commitment_id",
]
