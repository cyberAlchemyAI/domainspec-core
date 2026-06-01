"""F-CURRENCY-FLOAT-IN-COMPARISON — currency PRE-runtime gate (M1 §6.4).

DC-CF-02 closure leg 1 (runtime).  The Decimal helpers raise
:class:`pipeline.logician.currency.decimal_arithmetic.CurrencyFloatError`
whenever a ``float`` value reaches a currency comparison.  This gate
is the Logician-side surface that maps the helper failure into a
structured result.

The actual float-rejection logic lives in
:mod:`pipeline.logician.currency.decimal_arithmetic`; this gate is
the thin wrapper that callers (Scribe / Editor pipeline) invoke.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Final, Optional

from pipeline.logician.currency.decimal_arithmetic import (
    KFR_DECIMAL_CONTEXT,
    CurrencyContextError,
    CurrencyFloatError,
    tolerance_check_currency,
)


F_CURRENCY_FLOAT_IN_COMPARISON: Final[str] = "F-CURRENCY-FLOAT-IN-COMPARISON"


@dataclass(frozen=True, kw_only=True)
class CurrencyFloatResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    within_tolerance: Optional[bool] = None


def check_currency_float_in_comparison(
    *,
    draft: Decimal,
    kfr: Decimal,
    tolerance_pct: Decimal = Decimal("0.005"),
    tolerance_floor: Decimal = Decimal("2500"),
) -> CurrencyFloatResult:
    """PRE-runtime gate: refuse floats reaching the tolerance comparison.

    On float-input, fails with ``F-CURRENCY-FLOAT-IN-COMPARISON``.
    On any other context discipline failure, the returned
    ``failure_code`` carries the more-specific code (e.g.,
    ``F-CURRENCY-CONTEXT-OMITTED``) so the gate-runner can dispatch.
    """
    try:
        within = tolerance_check_currency(
            draft,
            kfr,
            tolerance_pct=tolerance_pct,
            tolerance_floor=tolerance_floor,
            context=KFR_DECIMAL_CONTEXT,
        )
    except CurrencyFloatError as exc:
        return CurrencyFloatResult(
            success=False,
            failure_code=F_CURRENCY_FLOAT_IN_COMPARISON,
            detail=str(exc),
        )
    except CurrencyContextError as exc:
        return CurrencyFloatResult(
            success=False,
            failure_code=getattr(exc, "failure_code", "F-CURRENCY-CONTEXT-OMITTED"),
            detail=str(exc),
        )
    return CurrencyFloatResult(
        success=True,
        failure_code=None,
        detail=(
            f"currency tolerance check passed (within={within}); "
            "no float input detected"
        ),
        within_tolerance=within,
    )


__all__ = [
    "F_CURRENCY_FLOAT_IN_COMPARISON",
    "CurrencyFloatResult",
    "check_currency_float_in_comparison",
]
