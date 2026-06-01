"""F-CURRENCY-DECIMAL-CONTEXT-DRIFT — currency PRE-runtime gate (M1 §6.2.1).

RT-07 closure leg 3.  Catches the case where ``decimal.getcontext()``
has drifted from :data:`KFR_DECIMAL_CONTEXT`'s semantics (e.g., a
``decimal.localcontext()`` block did not properly restore the global
context, or third-party code mutated the context).

The drift check is structural — prec / rounding / traps are
compared against the canonical values; identity is NOT required (the
global context object differs from KFR_DECIMAL_CONTEXT by design,
but its semantics must match).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.logician.currency.decimal_arithmetic import (
    CurrencyContextError,
    F_CURRENCY_DECIMAL_CONTEXT_DRIFT,
    assert_kfr_context_active,
)


@dataclass(frozen=True, kw_only=True)
class CurrencyContextDriftResult:
    success: bool
    failure_code: Optional[str]
    detail: str


def check_currency_decimal_context_drift() -> CurrencyContextDriftResult:
    """PRE-runtime gate: ``decimal.getcontext()`` matches KFR semantics."""
    try:
        assert_kfr_context_active()
    except CurrencyContextError as exc:
        return CurrencyContextDriftResult(
            success=False,
            failure_code=getattr(
                exc,
                "failure_code",
                F_CURRENCY_DECIMAL_CONTEXT_DRIFT,
            ),
            detail=str(exc),
        )
    return CurrencyContextDriftResult(
        success=True,
        failure_code=None,
        detail=(
            "decimal.getcontext() matches KFR_DECIMAL_CONTEXT semantics "
            "(prec, rounding, traps)"
        ),
    )


__all__ = [
    "F_CURRENCY_DECIMAL_CONTEXT_DRIFT",
    "CurrencyContextDriftResult",
    "check_currency_decimal_context_drift",
]
