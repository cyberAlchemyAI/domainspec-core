"""Decimal-typed currency arithmetic (architecture v7.0.4-M1 §6).

Three-layer defense against IEEE-754 float drift at the currency
tolerance boundary:

1. Runtime gate — :func:`tolerance_check_currency` and
   :func:`to_currency` raise :class:`CurrencyFloatError` whenever a
   ``float`` value reaches the helper.  The caller maps to
   ``F-CURRENCY-FLOAT-IN-COMPARISON``.
2. AST-lint rule — ``R-CURRENCY-NO-FLOAT-COMPARE`` (lives in
   :mod:`pipeline.linting.r_currency_no_float_compare`).
3. Type-check guard — mypy strict on currency-arithmetic modules
   (project-level config; this module declares its parameter shapes
   precisely).

Explicit-context discipline (RT-07 closure): every helper REQUIRES the
caller to pass :data:`KFR_DECIMAL_CONTEXT` explicitly.  Omitting the
context argument raises :class:`CurrencyContextError` ``omitted``;
passing a different context raises :class:`CurrencyContextError`
``mismatch``.  :func:`assert_kfr_context_active` is invoked on every
helper-call entry and refuses if ``decimal.getcontext()`` has drifted
from :data:`KFR_DECIMAL_CONTEXT`'s semantics (e.g., a third-party
``decimal.localcontext()`` block did not properly restore the global
context).
"""

from __future__ import annotations

import decimal
from dataclasses import dataclass
from decimal import Decimal
from typing import Final, Mapping, Optional


F_CURRENCY_FLOAT_IN_COMPARISON: Final[str] = "F-CURRENCY-FLOAT-IN-COMPARISON"
F_CURRENCY_CONTEXT_OMITTED: Final[str] = "F-CURRENCY-CONTEXT-OMITTED"
F_CURRENCY_CONTEXT_MISMATCH: Final[str] = "F-CURRENCY-CONTEXT-MISMATCH"
F_CURRENCY_DECIMAL_CONTEXT_DRIFT: Final[str] = (
    "F-CURRENCY-DECIMAL-CONTEXT-DRIFT"
)
F_CURRENCY_UNIT_MISMATCH: Final[str] = "F-CURRENCY-UNIT-MISMATCH"


# §6.2.1 fixed Decimal context — sealed at module import.
# Use frozenset for trap comparison since decimal.Context.traps is a
# dict-of-signal-classes-to-bool; we capture the equivalent semantic.
KFR_DECIMAL_CONTEXT: Final[decimal.Context] = decimal.Context(
    prec=28,
    rounding=decimal.ROUND_HALF_EVEN,
    Emin=-99999,
    Emax=99999,
    capitals=1,
    clamp=0,
    flags=[],
    traps=[
        decimal.DivisionByZero,
        decimal.Overflow,
        decimal.InvalidOperation,
    ],
)


# §8.2 canonical-unit conversion table per CF-RT-06 closure. Values are
# exact-rational Decimal scaling factors from the canonical-unit on
# the LHS to the canonical-unit's value scale.
UNIT_CONVERSION_TABLE: Final[Mapping[str, Mapping[str, Decimal]]] = {
    "usd": {
        "usd": Decimal("1"),
        "thousands_usd": Decimal("1000"),
        "millions_usd": Decimal("1000000"),
    },
    "count": {
        "count": Decimal("1"),
    },
    "acres": {
        "acres": Decimal("1"),
        "hectares": Decimal("2.471"),
        "square_meters": Decimal("0.000247"),
    },
    "percentage": {
        "percentage": Decimal("1"),
        "percentage_points": Decimal("1"),
    },
}


class CurrencyFloatError(TypeError):
    """Raised when a float value reaches a currency helper.

    Maps to ``F-CURRENCY-FLOAT-IN-COMPARISON``.
    """


class CurrencyContextError(ValueError):
    """Raised when the explicit Decimal context discipline is violated.

    Maps to ``F-CURRENCY-CONTEXT-OMITTED`` or
    ``F-CURRENCY-CONTEXT-MISMATCH`` based on which discipline failed.
    """

    def __init__(self, message: str, *, failure_code: str) -> None:
        super().__init__(message)
        self.failure_code = failure_code


class CurrencyUnitMismatchError(ValueError):
    """Raised when tolerance comparison receives mismatched units.

    Maps to ``F-CURRENCY-UNIT-MISMATCH``.
    """


class UnitConversionError(ValueError):
    """Raised when an unknown unit is requested for canonicalization."""


def assert_kfr_context_active() -> None:
    """Verify ``decimal.getcontext()`` matches :data:`KFR_DECIMAL_CONTEXT`.

    RT-07 closure — guards against ``decimal.localcontext()`` blocks
    that did not properly restore the global context.  Compares
    ``prec``, ``rounding``, and trap-set semantics explicitly.
    """
    current = decimal.getcontext()
    if current.prec != KFR_DECIMAL_CONTEXT.prec:
        raise CurrencyContextError(
            f"{F_CURRENCY_DECIMAL_CONTEXT_DRIFT}: decimal context "
            f"prec={current.prec} differs from KFR_DECIMAL_CONTEXT.prec="
            f"{KFR_DECIMAL_CONTEXT.prec}",
            failure_code=F_CURRENCY_DECIMAL_CONTEXT_DRIFT,
        )
    if current.rounding != KFR_DECIMAL_CONTEXT.rounding:
        raise CurrencyContextError(
            f"{F_CURRENCY_DECIMAL_CONTEXT_DRIFT}: decimal context "
            f"rounding={current.rounding!r} differs from "
            f"KFR_DECIMAL_CONTEXT.rounding="
            f"{KFR_DECIMAL_CONTEXT.rounding!r}",
            failure_code=F_CURRENCY_DECIMAL_CONTEXT_DRIFT,
        )
    expected_traps = {
        decimal.DivisionByZero,
        decimal.Overflow,
        decimal.InvalidOperation,
    }
    actual_traps = {
        cls for cls, enabled in current.traps.items() if enabled
    }
    missing_traps = expected_traps - actual_traps
    if missing_traps:
        missing = sorted(c.__name__ for c in missing_traps)
        raise CurrencyContextError(
            f"{F_CURRENCY_DECIMAL_CONTEXT_DRIFT}: decimal context "
            f"missing required traps {missing!r}",
            failure_code=F_CURRENCY_DECIMAL_CONTEXT_DRIFT,
        )


def _check_context_discipline(context: Optional[decimal.Context]) -> None:
    if context is None:
        raise CurrencyContextError(
            f"{F_CURRENCY_CONTEXT_OMITTED}: currency helper requires "
            "explicit context=KFR_DECIMAL_CONTEXT (RT-07 closure)",
            failure_code=F_CURRENCY_CONTEXT_OMITTED,
        )
    if context is not KFR_DECIMAL_CONTEXT:
        raise CurrencyContextError(
            f"{F_CURRENCY_CONTEXT_MISMATCH}: currency helper requires "
            "context is KFR_DECIMAL_CONTEXT (identity check)",
            failure_code=F_CURRENCY_CONTEXT_MISMATCH,
        )
    assert_kfr_context_active()


def _refuse_floats(*values: object, label: str = "value") -> None:
    for v in values:
        if isinstance(v, bool):
            # bool subclasses int — treat as float? No, bool is acceptable
            # only as a logical flag, never as a currency operand. We
            # refuse bool here too.
            raise CurrencyFloatError(
                f"{F_CURRENCY_FLOAT_IN_COMPARISON}: {label}={v!r} is "
                "bool — currency arithmetic requires Decimal/int/str"
            )
        if isinstance(v, float):
            raise CurrencyFloatError(
                f"{F_CURRENCY_FLOAT_IN_COMPARISON}: {label}={v!r} is "
                "float — currency arithmetic requires Decimal"
            )


def to_currency(
    value: int | str | Decimal,
    *,
    context: Optional[decimal.Context] = None,
    quantize_to: Decimal = Decimal("0.01"),
) -> Decimal:
    """Canonical conversion to currency-typed Decimal.

    Refuses ``float`` input fail-closed.  Caller MUST pass
    ``context=KFR_DECIMAL_CONTEXT`` explicitly.
    """
    _check_context_discipline(context)
    _refuse_floats(value, label="value")
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise CurrencyFloatError(
                f"{F_CURRENCY_FLOAT_IN_COMPARISON}: Decimal {value!r} "
                "non-finite (NaN / Infinity)"
            )
        canonical = value
    elif isinstance(value, int):
        canonical = Decimal(value)
    elif isinstance(value, str):
        try:
            canonical = Decimal(value, context=context)
        except decimal.InvalidOperation as exc:
            raise CurrencyFloatError(
                f"{F_CURRENCY_FLOAT_IN_COMPARISON}: string value "
                f"{value!r} not parseable as Decimal: {exc}"
            ) from exc
    else:
        raise CurrencyFloatError(
            f"{F_CURRENCY_FLOAT_IN_COMPARISON}: value type "
            f"{type(value).__name__} not in admitted set "
            "{int, str, Decimal}"
        )
    return canonical.quantize(quantize_to, context=context)


def tolerance_check_currency(
    draft: Decimal,
    kfr: Decimal,
    *,
    tolerance_pct: Decimal = Decimal("0.005"),
    tolerance_floor: Decimal = Decimal("2500"),
    context: Optional[decimal.Context] = None,
) -> bool:
    """Returns True iff ``|draft - kfr| <= max(tolerance_pct * kfr, floor)``.

    All four numeric inputs must be Decimal; any float raises
    :class:`CurrencyFloatError`.  Caller MUST pass
    ``context=KFR_DECIMAL_CONTEXT`` explicitly.
    """
    _check_context_discipline(context)
    _refuse_floats(
        draft,
        kfr,
        tolerance_pct,
        tolerance_floor,
        label="argument",
    )
    if not isinstance(draft, Decimal):
        raise CurrencyFloatError(
            f"{F_CURRENCY_FLOAT_IN_COMPARISON}: draft must be Decimal, "
            f"got {type(draft).__name__}"
        )
    if not isinstance(kfr, Decimal):
        raise CurrencyFloatError(
            f"{F_CURRENCY_FLOAT_IN_COMPARISON}: kfr must be Decimal, "
            f"got {type(kfr).__name__}"
        )
    if not isinstance(tolerance_pct, Decimal):
        raise CurrencyFloatError(
            f"{F_CURRENCY_FLOAT_IN_COMPARISON}: tolerance_pct must be "
            f"Decimal, got {type(tolerance_pct).__name__}"
        )
    if not isinstance(tolerance_floor, Decimal):
        raise CurrencyFloatError(
            f"{F_CURRENCY_FLOAT_IN_COMPARISON}: tolerance_floor must be "
            f"Decimal, got {type(tolerance_floor).__name__}"
        )
    delta = abs(draft - kfr)
    threshold = max(tolerance_pct * kfr, tolerance_floor)
    return delta <= threshold


def canonicalize_unit(unit: str) -> str:
    """Lower-cased + whitespace-stripped canonical unit string."""
    if not isinstance(unit, str):
        raise UnitConversionError(
            f"unit must be str, got {type(unit).__name__}"
        )
    return unit.strip().lower()


def _find_canonical_unit(unit: str) -> Optional[str]:
    for canonical, conversions in UNIT_CONVERSION_TABLE.items():
        if unit in conversions:
            return canonical
    return None


def convert_to_canonical_unit(
    value: Decimal,
    unit: str,
    *,
    context: Optional[decimal.Context] = None,
) -> tuple[Decimal, str]:
    """Convert ``value`` into the canonical unit (e.g., ``thousands_usd`` → ``usd``).

    Returns ``(converted_value, canonical_unit_name)``.  Raises
    :class:`UnitConversionError` on unknown / non-convertible unit.
    """
    _check_context_discipline(context)
    _refuse_floats(value, label="value")
    if not isinstance(value, Decimal):
        raise CurrencyFloatError(
            f"{F_CURRENCY_FLOAT_IN_COMPARISON}: value must be Decimal, "
            f"got {type(value).__name__}"
        )
    canonical_input = canonicalize_unit(unit)
    canonical = _find_canonical_unit(canonical_input)
    if canonical is None:
        raise UnitConversionError(
            f"unit {unit!r} not found in UNIT_CONVERSION_TABLE — known "
            f"canonical units: {sorted(UNIT_CONVERSION_TABLE.keys())!r}"
        )
    factor = UNIT_CONVERSION_TABLE[canonical][canonical_input]
    converted = value * factor
    return converted, canonical


__all__ = [
    "F_CURRENCY_CONTEXT_MISMATCH",
    "F_CURRENCY_CONTEXT_OMITTED",
    "F_CURRENCY_DECIMAL_CONTEXT_DRIFT",
    "F_CURRENCY_FLOAT_IN_COMPARISON",
    "F_CURRENCY_UNIT_MISMATCH",
    "KFR_DECIMAL_CONTEXT",
    "UNIT_CONVERSION_TABLE",
    "CurrencyContextError",
    "CurrencyFloatError",
    "CurrencyUnitMismatchError",
    "UnitConversionError",
    "assert_kfr_context_active",
    "canonicalize_unit",
    "convert_to_canonical_unit",
    "to_currency",
    "tolerance_check_currency",
]
