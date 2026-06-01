"""§13.9.5 — Field validator + KFR drift cross-check (POST-inbound advisory).

Per §13.9.5 + composition with F-LOGICIAN-FACT-DRIFT (v7.0.4 §4) — DC-side
advisory at inbound time; downstream Report Generator enforces fail-closed at
draft-time.

This module provides:

- `ParsedField` — normalized inbound parse output.
- `KfrDriftAdvisory` — drift advisory record per (field, KFR fact) pair.
- `check_numeric_drift` — apply per-field tolerance and unit-mismatch check.

No fail-closed semantics — advisory only. The advisory composes into
F-DATACOLLECTOR-KFR-DRIFT gate at POST inbound write position.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable, Literal, Mapping


DEFAULT_TOLERANCE_PCT: float = 0.10  # ±10% per §13.9.5; operator-tunable per field via KFR

DRIFT_SUB_TAG_ABOVE: str = "numeric_field_above_tolerance"
DRIFT_SUB_TAG_BELOW: str = "numeric_field_below_tolerance"
DRIFT_SUB_TAG_UNIT_MISMATCH: str = "unit_mismatch"


@dataclass(frozen=True, kw_only=True)
class ParsedField:
    """Normalized output from per-channel inbound parser."""
    field_class: str  # e.g. "graduates_count", "expenditures_usd"
    raw_value: object
    numeric_value: Decimal | None
    unit: str | None
    kfr_fact_ref: str | None  # resolved via reporting_template.yaml.kfr_cross_check


@dataclass(frozen=True, kw_only=True)
class KfrDriftAdvisory:
    """POST-inbound advisory record (not fail-closed)."""
    field_class: str
    inbound_value: Decimal
    inbound_unit: str | None
    kfr_fact_id: str
    kfr_value: Decimal
    kfr_unit: str | None
    tolerance_pct: float
    sub_tag: Literal[
        "numeric_field_above_tolerance",
        "numeric_field_below_tolerance",
        "unit_mismatch",
    ]
    relative_drift: float


def check_numeric_drift(
    *,
    inbound_value: Decimal,
    inbound_unit: str | None,
    kfr_fact_id: str,
    kfr_value: Decimal,
    kfr_unit: str | None,
    tolerance_pct: float = DEFAULT_TOLERANCE_PCT,
    field_class: str,
) -> KfrDriftAdvisory | None:
    """Return an advisory if drift exceeds tolerance OR unit mismatch; else None.

    Unit mismatch wins over tolerance check (a dollar-vs-thousands-of-dollars
    confusion makes the tolerance check meaningless).
    """
    if inbound_unit != kfr_unit:
        return KfrDriftAdvisory(
            field_class=field_class,
            inbound_value=inbound_value,
            inbound_unit=inbound_unit,
            kfr_fact_id=kfr_fact_id,
            kfr_value=kfr_value,
            kfr_unit=kfr_unit,
            tolerance_pct=tolerance_pct,
            sub_tag=DRIFT_SUB_TAG_UNIT_MISMATCH,
            relative_drift=0.0,
        )
    if kfr_value == 0:
        # Division-by-zero defense — only fires advisory if inbound also non-zero.
        if inbound_value != 0:
            return KfrDriftAdvisory(
                field_class=field_class,
                inbound_value=inbound_value,
                inbound_unit=inbound_unit,
                kfr_fact_id=kfr_fact_id,
                kfr_value=kfr_value,
                kfr_unit=kfr_unit,
                tolerance_pct=tolerance_pct,
                sub_tag=DRIFT_SUB_TAG_ABOVE,
                relative_drift=float("inf"),
            )
        return None
    relative_drift = float((inbound_value - kfr_value) / kfr_value)
    if abs(relative_drift) <= tolerance_pct:
        return None
    sub_tag = DRIFT_SUB_TAG_ABOVE if relative_drift > 0 else DRIFT_SUB_TAG_BELOW
    return KfrDriftAdvisory(
        field_class=field_class,
        inbound_value=inbound_value,
        inbound_unit=inbound_unit,
        kfr_fact_id=kfr_fact_id,
        kfr_value=kfr_value,
        kfr_unit=kfr_unit,
        tolerance_pct=tolerance_pct,
        sub_tag=sub_tag,
        relative_drift=relative_drift,
    )


def scan_inbound_for_pii_leak(message_bytes: bytes) -> tuple[bool, str | None]:
    """Mirror of F-CLASS-SLOT-ID-NON-OPAQUE applied to outbound message body.

    Returns (leaked, sub_tag). Detects:
    - semantic slot tokens of form `[SLOT_<NON_NUMERIC>]` (e.g. `[SLOT_ANNUAL_REVENUE]`)
    """
    import re
    # Match [SLOT_XXX] where XXX is anything; then check if non-numeric.
    pattern = re.compile(rb"\[SLOT_([A-Z0-9_]+)\]")
    for match in pattern.finditer(message_bytes):
        token = match.group(1).decode("ascii", errors="replace")
        if not token.isdigit():
            return True, "semantic_slot_in_outbound"
    return False, None


__all__ = [
    "DEFAULT_TOLERANCE_PCT",
    "DRIFT_SUB_TAG_ABOVE",
    "DRIFT_SUB_TAG_BELOW",
    "DRIFT_SUB_TAG_UNIT_MISMATCH",
    "KfrDriftAdvisory",
    "ParsedField",
    "check_numeric_drift",
    "scan_inbound_for_pii_leak",
]
