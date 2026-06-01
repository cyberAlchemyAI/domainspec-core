"""F-DATACOLLECTOR-KFR-DRIFT — POST-inbound advisory drift gate.

Per §13 Data Collector v1 LOCKED 2026-05-10 §13.9.5.

ADVISORY ONLY — NOT fail-closed. Surfaces inbound numeric responses that
drift from KFR-derived expected values for operator reconciliation. The
operator decides whether the inbound or the KFR is authoritative.

Sub-tags:

* ``.numeric_field_above_tolerance``
* ``.numeric_field_below_tolerance``
* ``.unit_mismatch``

Composes with F-LOGICIAN-FACT-DRIFT (v7.0.4 §4) — Data Collector surfaces
drift at inbound time (advisory); Report Generator enforces no-drift at
draft-time (fail-closed). The operator reconciles via SP0 KFR Freshness
Review at start of next reporting cycle.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

F_DATACOLLECTOR_KFR_DRIFT: Final[str] = "F-DATACOLLECTOR-KFR-DRIFT"

SUB_TAG_ABOVE_TOLERANCE: Final[str] = ".numeric_field_above_tolerance"
SUB_TAG_BELOW_TOLERANCE: Final[str] = ".numeric_field_below_tolerance"
SUB_TAG_UNIT_MISMATCH: Final[str] = ".unit_mismatch"

DEFAULT_TOLERANCE_PCT: Final[float] = 0.10  # ±10%


@dataclass(frozen=True, kw_only=True)
class KfrDriftResult:
    """Result of an F-DATACOLLECTOR-KFR-DRIFT advisory check.

    Note: ``advisory=True`` and ``success=False`` simultaneously means
    "advisory fired"; the inbound write proceeds regardless. Caller routes
    the advisory to the operator review surface.
    """

    success: bool
    failure_code: Optional[str]
    sub_tag: Optional[str]
    detail: str
    advisory: bool = True
    drift_pct: Optional[float] = None
    inbound_value: Optional[float] = None
    kfr_value: Optional[float] = None
    inbound_unit: Optional[str] = None
    kfr_unit: Optional[str] = None
    field_class: Optional[str] = None


def check_kfr_drift(
    *,
    field_class: str,
    inbound_value: float,
    inbound_unit: str,
    kfr_value: float,
    kfr_unit: str,
    tolerance_pct: float = DEFAULT_TOLERANCE_PCT,
) -> KfrDriftResult:
    """POST-inbound-write advisory drift check.

    Returns ``success=True`` (no advisory) when value within tolerance and
    units match. Otherwise the result carries a sub_tag and the inbound
    write still succeeds — caller surfaces the advisory at the next
    operator review (``tilth data-collector classify-inbound`` or v1.1
    ``reconcile-drift``).
    """
    if inbound_unit != kfr_unit:
        return KfrDriftResult(
            success=False,
            failure_code=F_DATACOLLECTOR_KFR_DRIFT,
            sub_tag=SUB_TAG_UNIT_MISMATCH,
            detail=(
                f"unit mismatch for field_class={field_class!r}: "
                f"inbound_unit={inbound_unit!r} vs kfr_unit={kfr_unit!r}"
            ),
            inbound_value=inbound_value,
            kfr_value=kfr_value,
            inbound_unit=inbound_unit,
            kfr_unit=kfr_unit,
            field_class=field_class,
        )
    if kfr_value == 0:
        # Zero KFR baseline — drift_pct is undefined; treat any non-zero
        # inbound as above-tolerance.
        if inbound_value == 0:
            return KfrDriftResult(
                success=True,
                failure_code=None,
                sub_tag=None,
                detail=(
                    f"both inbound and KFR are zero for "
                    f"field_class={field_class!r}; no drift"
                ),
                drift_pct=0.0,
                inbound_value=inbound_value,
                kfr_value=kfr_value,
                inbound_unit=inbound_unit,
                kfr_unit=kfr_unit,
                field_class=field_class,
            )
        sub_tag = (
            SUB_TAG_ABOVE_TOLERANCE
            if inbound_value > 0
            else SUB_TAG_BELOW_TOLERANCE
        )
        return KfrDriftResult(
            success=False,
            failure_code=F_DATACOLLECTOR_KFR_DRIFT,
            sub_tag=sub_tag,
            detail=(
                f"KFR baseline is zero but inbound={inbound_value} for "
                f"field_class={field_class!r}; advisory fired"
            ),
            drift_pct=float("inf"),
            inbound_value=inbound_value,
            kfr_value=kfr_value,
            inbound_unit=inbound_unit,
            kfr_unit=kfr_unit,
            field_class=field_class,
        )
    drift = (inbound_value - kfr_value) / kfr_value
    abs_drift = abs(drift)
    if abs_drift > tolerance_pct:
        sub_tag = (
            SUB_TAG_ABOVE_TOLERANCE
            if drift > 0
            else SUB_TAG_BELOW_TOLERANCE
        )
        return KfrDriftResult(
            success=False,
            failure_code=F_DATACOLLECTOR_KFR_DRIFT,
            sub_tag=sub_tag,
            detail=(
                f"drift {drift*100:.2f}% exceeds tolerance "
                f"{tolerance_pct*100:.2f}% for field_class={field_class!r} "
                f"(inbound={inbound_value} {inbound_unit}, kfr={kfr_value} "
                f"{kfr_unit})"
            ),
            drift_pct=drift,
            inbound_value=inbound_value,
            kfr_value=kfr_value,
            inbound_unit=inbound_unit,
            kfr_unit=kfr_unit,
            field_class=field_class,
        )
    return KfrDriftResult(
        success=True,
        failure_code=None,
        sub_tag=None,
        detail=(
            f"drift {drift*100:.2f}% within tolerance "
            f"{tolerance_pct*100:.2f}% for field_class={field_class!r}"
        ),
        drift_pct=drift,
        inbound_value=inbound_value,
        kfr_value=kfr_value,
        inbound_unit=inbound_unit,
        kfr_unit=kfr_unit,
        field_class=field_class,
    )


__all__ = [
    "DEFAULT_TOLERANCE_PCT",
    "F_DATACOLLECTOR_KFR_DRIFT",
    "KfrDriftResult",
    "SUB_TAG_ABOVE_TOLERANCE",
    "SUB_TAG_BELOW_TOLERANCE",
    "SUB_TAG_UNIT_MISMATCH",
    "check_kfr_drift",
]
