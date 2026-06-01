"""F-REPORT-NUMERIC-DRIFT — POST scribe-equivalent.

Per §14 Report Generator v1 LOCKED 2026-05-10 §14.9.4 (Cycle 1 RT-3a/3b/3c
closures + v7.0.4-M1 Decimal mandate).

Trigger: a numeric claim in ``draft_<v>.md`` differs from KFR-derived
expected value beyond per-field tolerance.

**Decimal mandate (v7.0.4-M1).** ALL numeric comparisons use
``decimal.Decimal``. ANY ``float`` value in the predicate body is a
defect — the gate's first-executable-statement asserts Decimal type on
every numeric-touching code path. Canonical rounding mode is
``decimal.ROUND_HALF_UP`` (banker's rounding rejected per accounting
norm). AST-lint rule R-REPORT-DECIMAL-MANDATE (registered in Slice 3)
adds module-level defense; this gate body adds runtime defense.

Sub-tags (canonical at §14 v1 LOCK):

* ``.kfr_value_mismatch_above_tolerance``
* ``.kfr_value_mismatch_below_tolerance``
* ``.kfr_value_unit_mismatch`` — composes with F-DATACOLLECTOR-KFR-DRIFT
  per §13 v1
* ``.float_comparison_detected`` — defect-detection: caller supplied a
  float in a numeric path
* ``.kfr_field_absent`` — advisory: claim references field not in KFR
* ``.tolerance_unset_for_numeric_field`` — v0.2 default is exact match
  (tolerance=0); operator may set per-field tolerance in
  proposal_commitments
* ``.operational_data_value_drift_from_kfr`` — operational-data value
  differs from KFR canonical
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from typing import Final, Mapping, Optional, Sequence

F_REPORT_NUMERIC_DRIFT: Final[str] = "F-REPORT-NUMERIC-DRIFT"

SUB_TAG_KFR_VALUE_MISMATCH_ABOVE_TOLERANCE: Final[str] = (
    ".kfr_value_mismatch_above_tolerance"
)
SUB_TAG_KFR_VALUE_MISMATCH_BELOW_TOLERANCE: Final[str] = (
    ".kfr_value_mismatch_below_tolerance"
)
SUB_TAG_KFR_VALUE_UNIT_MISMATCH: Final[str] = ".kfr_value_unit_mismatch"
SUB_TAG_FLOAT_COMPARISON_DETECTED: Final[str] = ".float_comparison_detected"
SUB_TAG_KFR_FIELD_ABSENT: Final[str] = ".kfr_field_absent"
SUB_TAG_TOLERANCE_UNSET_FOR_NUMERIC_FIELD: Final[str] = (
    ".tolerance_unset_for_numeric_field"
)
SUB_TAG_OPERATIONAL_DATA_VALUE_DRIFT_FROM_KFR: Final[str] = (
    ".operational_data_value_drift_from_kfr"
)

# v7.0.4-M1 canonical rounding mode + variance precision.
VARIANCE_QUANTIZE: Final[Decimal] = Decimal("0.01")
VARIANCE_ROUNDING: Final[str] = ROUND_HALF_UP

# v0.2 default tolerance when proposal_commitments evaluation_criteria
# omits per-field tolerance.
DEFAULT_NUMERIC_TOLERANCE: Final[Decimal] = Decimal("0")


@dataclass(frozen=True, kw_only=True)
class NumericDriftFinding:
    sub_tag: str
    claim_id: Optional[str]
    field: Optional[str]
    detail: str


@dataclass(frozen=True, kw_only=True)
class NumericDriftResult:
    success: bool
    failure_code: Optional[str]
    findings: tuple[NumericDriftFinding, ...] = field(default_factory=tuple)

    @property
    def fired_sub_tags(self) -> tuple[str, ...]:
        seen: list[str] = []
        for f in self.findings:
            if f.sub_tag not in seen:
                seen.append(f.sub_tag)
        return tuple(seen)


@dataclass(frozen=True, kw_only=True)
class NumericClaimVsKfr:
    """One numeric-claim-vs-KFR row supplied by the caller for evaluation.

    Per the v7.0.4-M1 Decimal mandate: every numeric-typed field
    (claim_value, kfr_value, tolerance) MUST be ``decimal.Decimal``. The
    gate's defense-in-depth asserts this; ``float`` triggers the
    ``.float_comparison_detected`` defect sub-tag.

    Unit fields are strings; mismatch (e.g. "kg" vs "lb") fires
    ``.kfr_value_unit_mismatch``.

    Tolerance handling:

    * ``tolerance is None`` → ``.tolerance_unset_for_numeric_field``
      advisory; gate then applies ``DEFAULT_NUMERIC_TOLERANCE`` (exact
      match) and may still fire the above/below sub-tag if not equal.
    * ``tolerance == Decimal(0)`` → exact match required.
    * ``tolerance > 0`` → |claim - kfr| ≤ tolerance permitted.
    """

    claim_id: str
    field: str
    claim_value: Decimal
    kfr_value: Optional[Decimal]
    kfr_field_present: bool
    tolerance: Optional[Decimal]
    claim_unit: Optional[str] = None
    kfr_unit: Optional[str] = None
    operational_data_value: Optional[Decimal] = None


def _is_decimal_or_none(v: object) -> bool:
    return v is None or isinstance(v, Decimal)


def check_numeric_drift(
    *,
    numeric_rows: Sequence[NumericClaimVsKfr],
) -> NumericDriftResult:
    """Walk numeric claims; collect drift findings.

    Defense-in-depth runtime assertion of Decimal mandate per v7.0.4-M1.
    Any float in a numeric-typed input path triggers
    ``.float_comparison_detected`` (the gate caller's substrate is the
    defect; the gate surfaces it as a sub-tag rather than raising).
    """
    findings: list[NumericDriftFinding] = []
    for row in numeric_rows:
        # Decimal mandate runtime defense
        for name, val in (
            ("claim_value", row.claim_value),
            ("kfr_value", row.kfr_value),
            ("tolerance", row.tolerance),
            ("operational_data_value", row.operational_data_value),
        ):
            if isinstance(val, float):
                findings.append(
                    NumericDriftFinding(
                        sub_tag=SUB_TAG_FLOAT_COMPARISON_DETECTED,
                        claim_id=row.claim_id,
                        field=row.field,
                        detail=(
                            f"{name}={val!r} is float; Decimal mandate per "
                            f"v7.0.4-M1 / R-REPORT-DECIMAL-MANDATE"
                        ),
                    )
                )
                # Skip the rest of this row's checks — defect surfaced
                break
        else:
            # No float defect — proceed.
            if not row.kfr_field_present:
                findings.append(
                    NumericDriftFinding(
                        sub_tag=SUB_TAG_KFR_FIELD_ABSENT,
                        claim_id=row.claim_id,
                        field=row.field,
                        detail=(
                            f"KFR lacks field {row.field!r}; claim value "
                            f"{row.claim_value} cannot be cross-validated"
                        ),
                    )
                )
                continue

            assert isinstance(row.claim_value, Decimal), (
                "claim_value must be Decimal at this point (Decimal mandate)"
            )
            kfr_v = row.kfr_value
            assert isinstance(kfr_v, Decimal), (
                "kfr_value must be Decimal when kfr_field_present is True"
            )

            if row.claim_unit is not None and row.kfr_unit is not None:
                if row.claim_unit != row.kfr_unit:
                    findings.append(
                        NumericDriftFinding(
                            sub_tag=SUB_TAG_KFR_VALUE_UNIT_MISMATCH,
                            claim_id=row.claim_id,
                            field=row.field,
                            detail=(
                                f"claim_unit={row.claim_unit!r} != "
                                f"kfr_unit={row.kfr_unit!r}"
                            ),
                        )
                    )
                    continue

            tolerance = row.tolerance
            if tolerance is None:
                findings.append(
                    NumericDriftFinding(
                        sub_tag=SUB_TAG_TOLERANCE_UNSET_FOR_NUMERIC_FIELD,
                        claim_id=row.claim_id,
                        field=row.field,
                        detail=(
                            f"tolerance unset for field {row.field!r}; "
                            f"applying default tolerance={DEFAULT_NUMERIC_TOLERANCE}"
                        ),
                    )
                )
                tolerance = DEFAULT_NUMERIC_TOLERANCE

            diff = row.claim_value - kfr_v
            if diff > tolerance:
                findings.append(
                    NumericDriftFinding(
                        sub_tag=SUB_TAG_KFR_VALUE_MISMATCH_ABOVE_TOLERANCE,
                        claim_id=row.claim_id,
                        field=row.field,
                        detail=(
                            f"claim={row.claim_value} > KFR={kfr_v} + "
                            f"tolerance={tolerance}"
                        ),
                    )
                )
            elif diff < -tolerance:
                findings.append(
                    NumericDriftFinding(
                        sub_tag=SUB_TAG_KFR_VALUE_MISMATCH_BELOW_TOLERANCE,
                        claim_id=row.claim_id,
                        field=row.field,
                        detail=(
                            f"claim={row.claim_value} < KFR={kfr_v} - "
                            f"tolerance={tolerance}"
                        ),
                    )
                )

            # Operational-data vs KFR (composes with F-LOGICIAN-FACT-DRIFT)
            if row.operational_data_value is not None:
                assert isinstance(row.operational_data_value, Decimal)
                if row.operational_data_value != kfr_v:
                    findings.append(
                        NumericDriftFinding(
                            sub_tag=SUB_TAG_OPERATIONAL_DATA_VALUE_DRIFT_FROM_KFR,
                            claim_id=row.claim_id,
                            field=row.field,
                            detail=(
                                f"operational_data={row.operational_data_value} "
                                f"!= KFR={kfr_v}; operator must reconcile"
                            ),
                        )
                    )

    fail_subtags = {
        SUB_TAG_KFR_VALUE_MISMATCH_ABOVE_TOLERANCE,
        SUB_TAG_KFR_VALUE_MISMATCH_BELOW_TOLERANCE,
        SUB_TAG_KFR_VALUE_UNIT_MISMATCH,
        SUB_TAG_FLOAT_COMPARISON_DETECTED,
        SUB_TAG_OPERATIONAL_DATA_VALUE_DRIFT_FROM_KFR,
    }
    has_failure = any(f.sub_tag in fail_subtags for f in findings)
    if has_failure:
        return NumericDriftResult(
            success=False,
            failure_code=F_REPORT_NUMERIC_DRIFT,
            findings=tuple(findings),
        )
    # Only advisories fired (KFR_FIELD_ABSENT / TOLERANCE_UNSET) — pass
    # but surface findings for the operator review surface.
    return NumericDriftResult(
        success=True,
        failure_code=None,
        findings=tuple(findings),
    )


def variance_pct(
    *,
    actual: Decimal,
    budgeted: Decimal,
) -> Decimal:
    """Per RT-3b — variance_pct using canonical ROUND_HALF_UP rounding.

    Used by the financial_summary composer at WS-J Slice 2 (composer
    wiring); the helper lives here so the rounding mode is canonical
    across the gate + composer surface.

    Raises ZeroDivisionError when ``budgeted == 0``; caller wraps in a
    presentation-friendly N/A.
    """
    if not isinstance(actual, Decimal):
        raise TypeError(
            f"variance_pct: actual must be Decimal (v7.0.4-M1 mandate); got "
            f"{type(actual).__name__}"
        )
    if not isinstance(budgeted, Decimal):
        raise TypeError(
            f"variance_pct: budgeted must be Decimal (v7.0.4-M1 mandate); got "
            f"{type(budgeted).__name__}"
        )
    if budgeted == Decimal(0):
        raise ZeroDivisionError("variance_pct: budgeted is zero")
    variance = actual - budgeted
    return (variance / budgeted * Decimal(100)).quantize(
        VARIANCE_QUANTIZE, rounding=VARIANCE_ROUNDING
    )


__all__ = [
    "DEFAULT_NUMERIC_TOLERANCE",
    "F_REPORT_NUMERIC_DRIFT",
    "NumericClaimVsKfr",
    "NumericDriftFinding",
    "NumericDriftResult",
    "SUB_TAG_FLOAT_COMPARISON_DETECTED",
    "SUB_TAG_KFR_FIELD_ABSENT",
    "SUB_TAG_KFR_VALUE_MISMATCH_ABOVE_TOLERANCE",
    "SUB_TAG_KFR_VALUE_MISMATCH_BELOW_TOLERANCE",
    "SUB_TAG_KFR_VALUE_UNIT_MISMATCH",
    "SUB_TAG_OPERATIONAL_DATA_VALUE_DRIFT_FROM_KFR",
    "SUB_TAG_TOLERANCE_UNSET_FOR_NUMERIC_FIELD",
    "VARIANCE_QUANTIZE",
    "VARIANCE_ROUNDING",
    "check_numeric_drift",
    "variance_pct",
]
