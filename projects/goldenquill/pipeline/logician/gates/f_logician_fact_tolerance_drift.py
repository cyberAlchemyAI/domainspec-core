"""F-LOGICIAN-FACT-TOLERANCE-DRIFT — PRE on draft-time KFR read (RT-02 closure).

Per architecture v7.0.4 §4.4.

Tolerance widening is the highest-leverage attack surface in the
F-LOGICIAN-FACT-DRIFT family. A single ``tolerance_pct=50`` write on
a $5M currency fact passes a $2.5M-off claim. The amendment closes
the silent-write path:

* Every per-fact ``tolerance_pct`` change beyond the type-default is
  admin-risk-ledger logged at HIGH severity
  (``ledger_kind="kfr_tolerance_widen"``).
* The ledger entry must be re-signed at the next SP0 review of the
  current grant cycle (``ledger_kind="kfr_tolerance_widen_reconfirm"``).
* This gate fires at draft-time read of any KFR fact whose
  ``tolerance_pct`` is widened beyond the type-default AND has no
  re-confirmation signature in the current grant cycle's ledger.
  HARD_BLOCK.

Type-default tolerances per §4
------------------------------
========================  =============================================
Fact type                 Default tolerance
========================  =============================================
identifier                0.0% (exact match)
legal                     0.0% (exact match)
count                     2.0%
currency                  0.5% (with $2,500 absolute floor — applied
                          by F-LOGICIAN-FACT-DRIFT itself; this gate
                          only watches the ``tolerance_pct`` widening)
percentage                1.0 percentage point absolute (the gate
                          treats the configured ``tolerance_pct`` as
                          the comparison target — operator-side
                          interpretation)
date                      0.0 (exact match)
range                     applied per-bound — the underlying type's
                          rule applies; this gate compares against
                          the underlying-type default
========================  =============================================

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Sequence


F_LOGICIAN_FACT_TOLERANCE_DRIFT: Final[str] = "F-LOGICIAN-FACT-TOLERANCE-DRIFT"

# Canonical ledger kinds per §4.4.
LEDGER_KIND_WIDEN: Final[str] = "kfr_tolerance_widen"
LEDGER_KIND_WIDEN_RECONFIRM: Final[str] = "kfr_tolerance_widen_reconfirm"

# Type-default tolerances per §4 (closes J-01 — tightened currency).
TYPE_DEFAULT_TOLERANCE_PCT: Final[Mapping[str, float]] = {
    "identifier": 0.0,
    "legal": 0.0,
    "count": 2.0,
    "currency": 0.5,
    "percentage": 1.0,
    "date": 0.0,
    "range": 2.0,  # underlying-type default applied per bound
}


@dataclass(frozen=True, kw_only=True)
class FactToleranceDriftResult:
    """Result of F-LOGICIAN-FACT-TOLERANCE-DRIFT check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    fact_id: Optional[str] = None
    type_default_pct: Optional[float] = None
    configured_pct: Optional[float] = None


def _has_current_cycle_reconfirm(
    ledger_entries: Sequence[Mapping[str, Any]],
    fact_id: str,
    grant_cycle_id: str,
) -> bool:
    """True iff a kfr_tolerance_widen_reconfirm row exists for this
    (fact_id, grant_cycle_id) pair with non-empty signed_at_utc."""
    for row in ledger_entries:
        if not isinstance(row, Mapping):
            continue
        if row.get("ledger_kind") != LEDGER_KIND_WIDEN_RECONFIRM:
            continue
        if row.get("fact_id") != fact_id:
            continue
        if row.get("grant_cycle_id") != grant_cycle_id:
            continue
        signed = row.get("signed_at_utc")
        if isinstance(signed, str) and signed.strip():
            return True
    return False


def check_fact_tolerance_drift(
    *,
    fact_id: str,
    fact_type: str,
    configured_tolerance_pct: float,
    grant_cycle_id: str,
    ledger_entries: Sequence[Mapping[str, Any]],
    type_defaults: Optional[Mapping[str, float]] = None,
) -> FactToleranceDriftResult:
    """PRE-draft-read gate: widened tolerance requires current-cycle re-confirm.

    Parameters
    ----------
    fact_id
        KFR entry identifier.
    fact_type
        One of the keys in :data:`TYPE_DEFAULT_TOLERANCE_PCT`. Unknown
        types fail-closed.
    configured_tolerance_pct
        The fact's current ``tolerance_pct`` value (the value Scribe
        would consult at draft-time).
    grant_cycle_id
        Identifier of the in-flight grant cycle. Re-confirmation
        signatures are scoped per cycle — a re-confirm in cycle A does
        not authorize the widened tolerance in cycle B.
    ledger_entries
        Admin-risk ledger rows the caller has already loaded. The gate
        scans for ``kfr_tolerance_widen_reconfirm`` rows matching this
        (fact_id, grant_cycle_id) pair.
    type_defaults
        Override type-default mapping (test injection). When None,
        :data:`TYPE_DEFAULT_TOLERANCE_PCT` is used.

    Returns
    -------
    FactToleranceDriftResult. Passes when (a) ``configured_tolerance_pct``
    is at or below the type-default, OR (b) widened above default AND a
    current-cycle reconfirm row is present. Fails when widened without
    reconfirm or fact_type unknown.
    """
    defaults = type_defaults if type_defaults is not None else TYPE_DEFAULT_TOLERANCE_PCT
    if fact_type not in defaults:
        return FactToleranceDriftResult(
            success=False,
            failure_code=F_LOGICIAN_FACT_TOLERANCE_DRIFT,
            detail=(
                f"fact_type {fact_type!r} not in type-default tolerance "
                f"mapping {sorted(defaults.keys())!r}"
            ),
            fact_id=fact_id,
            configured_pct=configured_tolerance_pct,
        )

    type_default = float(defaults[fact_type])
    if configured_tolerance_pct < 0:
        return FactToleranceDriftResult(
            success=False,
            failure_code=F_LOGICIAN_FACT_TOLERANCE_DRIFT,
            detail=(
                f"configured_tolerance_pct={configured_tolerance_pct} negative "
                "— invalid tolerance configuration"
            ),
            fact_id=fact_id,
            type_default_pct=type_default,
            configured_pct=configured_tolerance_pct,
        )

    # Within or at default — clean PASS, no widening signal at all.
    if configured_tolerance_pct <= type_default:
        return FactToleranceDriftResult(
            success=True,
            failure_code=None,
            detail=(
                f"configured_tolerance_pct={configured_tolerance_pct} at or "
                f"below type-default {type_default} for fact_type "
                f"{fact_type!r}"
            ),
            fact_id=fact_id,
            type_default_pct=type_default,
            configured_pct=configured_tolerance_pct,
        )

    # Widened — current-cycle reconfirm required.
    if _has_current_cycle_reconfirm(
        ledger_entries, fact_id, grant_cycle_id
    ):
        return FactToleranceDriftResult(
            success=True,
            failure_code=None,
            detail=(
                f"configured_tolerance_pct={configured_tolerance_pct} widened "
                f"above default {type_default} for fact_type {fact_type!r}; "
                f"current-cycle re-confirmation signature present in ledger"
            ),
            fact_id=fact_id,
            type_default_pct=type_default,
            configured_pct=configured_tolerance_pct,
        )

    return FactToleranceDriftResult(
        success=False,
        failure_code=F_LOGICIAN_FACT_TOLERANCE_DRIFT,
        detail=(
            f"configured_tolerance_pct={configured_tolerance_pct} widened "
            f"above type-default {type_default} for fact_type {fact_type!r}; "
            f"no kfr_tolerance_widen_reconfirm row for fact_id={fact_id!r} "
            f"in grant_cycle_id={grant_cycle_id!r} — HARD_BLOCK at draft-read"
        ),
        fact_id=fact_id,
        type_default_pct=type_default,
        configured_pct=configured_tolerance_pct,
    )


__all__ = [
    "F_LOGICIAN_FACT_TOLERANCE_DRIFT",
    "LEDGER_KIND_WIDEN",
    "LEDGER_KIND_WIDEN_RECONFIRM",
    "TYPE_DEFAULT_TOLERANCE_PCT",
    "FactToleranceDriftResult",
    "check_fact_tolerance_drift",
]
