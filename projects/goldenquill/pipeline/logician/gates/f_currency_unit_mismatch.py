"""F-CURRENCY-UNIT-MISMATCH — currency PRE-comparison gate (M1 §8.2).

CF-RT-06 closure.  Tolerance-comparison helpers REQUIRE both sides
share matching unit strings; convertible units (e.g.,
``thousands_usd`` → ``usd``) are normalized BEFORE comparison.

This gate is the wrapper that enforces the requirement at the
gate-runner layer; the conversion machinery itself lives in
:mod:`pipeline.logician.currency.decimal_arithmetic`.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Final, Optional, Tuple

from pipeline.logician.currency.decimal_arithmetic import (
    F_CURRENCY_UNIT_MISMATCH,
    KFR_DECIMAL_CONTEXT,
    UnitConversionError,
    canonicalize_unit,
    convert_to_canonical_unit,
)


@dataclass(frozen=True, kw_only=True)
class CurrencyUnitMismatchResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    canonical_pair: Optional[Tuple[Decimal, Decimal]] = None
    canonical_unit: Optional[str] = None


def check_currency_unit_mismatch(
    *,
    draft_value: Decimal,
    draft_unit: str,
    kfr_value: Decimal,
    kfr_unit: str,
) -> CurrencyUnitMismatchResult:
    """PRE-comparison gate: refuse non-convertible mismatched units.

    Returns canonicalized values + canonical unit on success so the
    caller can use them for the actual tolerance check.
    """
    draft_unit_canon = canonicalize_unit(draft_unit)
    kfr_unit_canon = canonicalize_unit(kfr_unit)
    try:
        draft_canon, draft_canonical = convert_to_canonical_unit(
            draft_value, draft_unit_canon, context=KFR_DECIMAL_CONTEXT
        )
    except UnitConversionError as exc:
        return CurrencyUnitMismatchResult(
            success=False,
            failure_code=F_CURRENCY_UNIT_MISMATCH,
            detail=(
                f"draft unit {draft_unit!r} not convertible: {exc}"
            ),
        )
    try:
        kfr_canon, kfr_canonical = convert_to_canonical_unit(
            kfr_value, kfr_unit_canon, context=KFR_DECIMAL_CONTEXT
        )
    except UnitConversionError as exc:
        return CurrencyUnitMismatchResult(
            success=False,
            failure_code=F_CURRENCY_UNIT_MISMATCH,
            detail=(
                f"kfr unit {kfr_unit!r} not convertible: {exc}"
            ),
        )

    if draft_canonical != kfr_canonical:
        return CurrencyUnitMismatchResult(
            success=False,
            failure_code=F_CURRENCY_UNIT_MISMATCH,
            detail=(
                f"non-convertible canonical units: draft "
                f"{draft_unit!r}→{draft_canonical!r} vs kfr "
                f"{kfr_unit!r}→{kfr_canonical!r}"
            ),
        )

    return CurrencyUnitMismatchResult(
        success=True,
        failure_code=None,
        detail=(
            f"units convertible to canonical {draft_canonical!r}: "
            f"draft={draft_canon} ({draft_unit!r}); kfr={kfr_canon} "
            f"({kfr_unit!r})"
        ),
        canonical_pair=(draft_canon, kfr_canon),
        canonical_unit=draft_canonical,
    )


__all__ = [
    "F_CURRENCY_UNIT_MISMATCH",
    "CurrencyUnitMismatchResult",
    "check_currency_unit_mismatch",
]
