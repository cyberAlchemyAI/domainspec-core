"""Tests for ``pipeline.logician.gates.f_report_numeric_drift``.

Per §14.9.4 Cycle 1 closures (RT-3a/3b/3c) + v7.0.4-M1 Decimal mandate.
"""
from __future__ import annotations

from decimal import Decimal

import pytest

from pipeline.logician.gates.f_report_numeric_drift import (
    F_REPORT_NUMERIC_DRIFT,
    NumericClaimVsKfr,
    SUB_TAG_FLOAT_COMPARISON_DETECTED,
    SUB_TAG_KFR_FIELD_ABSENT,
    SUB_TAG_KFR_VALUE_MISMATCH_ABOVE_TOLERANCE,
    SUB_TAG_KFR_VALUE_MISMATCH_BELOW_TOLERANCE,
    SUB_TAG_KFR_VALUE_UNIT_MISMATCH,
    SUB_TAG_OPERATIONAL_DATA_VALUE_DRIFT_FROM_KFR,
    SUB_TAG_TOLERANCE_UNSET_FOR_NUMERIC_FIELD,
    VARIANCE_QUANTIZE,
    check_numeric_drift,
    variance_pct,
)


def _row(claim_value, kfr_value=None, kfr_present=True, tolerance=None,
         claim_unit=None, kfr_unit=None, op_data=None):
    return NumericClaimVsKfr(
        claim_id="C", field="f",
        claim_value=claim_value,
        kfr_value=kfr_value,
        kfr_field_present=kfr_present,
        tolerance=tolerance,
        claim_unit=claim_unit,
        kfr_unit=kfr_unit,
        operational_data_value=op_data,
    )


class TestHappyPath:
    def test_exact_match_passes(self):
        r = check_numeric_drift(numeric_rows=[
            _row(Decimal("50"), kfr_value=Decimal("50"), tolerance=Decimal("0")),
        ])
        assert r.success
        assert r.fired_sub_tags == ()

    def test_within_tolerance_passes(self):
        r = check_numeric_drift(numeric_rows=[
            _row(Decimal("52"), kfr_value=Decimal("50"), tolerance=Decimal("5")),
        ])
        assert r.success


class TestKfrValueMismatch:
    def test_above_tolerance_fires(self):
        r = check_numeric_drift(numeric_rows=[
            _row(Decimal("55"), kfr_value=Decimal("50"), tolerance=Decimal("0")),
        ])
        assert not r.success
        assert SUB_TAG_KFR_VALUE_MISMATCH_ABOVE_TOLERANCE in r.fired_sub_tags

    def test_below_tolerance_fires(self):
        r = check_numeric_drift(numeric_rows=[
            _row(Decimal("45"), kfr_value=Decimal("50"), tolerance=Decimal("0")),
        ])
        assert not r.success
        assert SUB_TAG_KFR_VALUE_MISMATCH_BELOW_TOLERANCE in r.fired_sub_tags


class TestUnitMismatch:
    def test_unit_mismatch_fires(self):
        r = check_numeric_drift(numeric_rows=[
            _row(Decimal("50"), kfr_value=Decimal("50"), tolerance=Decimal("0"),
                 claim_unit="kg", kfr_unit="lb"),
        ])
        assert not r.success
        assert SUB_TAG_KFR_VALUE_UNIT_MISMATCH in r.fired_sub_tags


class TestKfrFieldAbsent:
    def test_kfr_field_absent_advisory(self):
        r = check_numeric_drift(numeric_rows=[
            _row(Decimal("50"), kfr_value=None, kfr_present=False, tolerance=None),
        ])
        # Only kfr_field_absent fires — that's advisory; gate passes
        assert r.success
        assert SUB_TAG_KFR_FIELD_ABSENT in r.fired_sub_tags


class TestToleranceUnset:
    def test_unset_tolerance_surfaces_advisory(self):
        r = check_numeric_drift(numeric_rows=[
            _row(Decimal("50"), kfr_value=Decimal("50"), tolerance=None),
        ])
        # Tolerance unset → advisory + then exact match applied → passes
        assert r.success
        assert SUB_TAG_TOLERANCE_UNSET_FOR_NUMERIC_FIELD in r.fired_sub_tags

    def test_unset_tolerance_then_mismatch_fires_both(self):
        r = check_numeric_drift(numeric_rows=[
            _row(Decimal("51"), kfr_value=Decimal("50"), tolerance=None),
        ])
        assert not r.success
        sub_tags = set(r.fired_sub_tags)
        assert SUB_TAG_TOLERANCE_UNSET_FOR_NUMERIC_FIELD in sub_tags
        assert SUB_TAG_KFR_VALUE_MISMATCH_ABOVE_TOLERANCE in sub_tags


class TestFloatDefectDetection:
    def test_float_claim_value_fires_defect(self):
        # Constructing NumericClaimVsKfr with claim_value as float bypasses
        # dataclass field-type but the gate's runtime check catches it.
        row = NumericClaimVsKfr(
            claim_id="C", field="f",
            claim_value=50.0,  # float — defect
            kfr_value=Decimal("50"),
            kfr_field_present=True, tolerance=Decimal("0"),
        )
        r = check_numeric_drift(numeric_rows=[row])
        assert not r.success
        assert SUB_TAG_FLOAT_COMPARISON_DETECTED in r.fired_sub_tags

    def test_float_tolerance_fires_defect(self):
        row = NumericClaimVsKfr(
            claim_id="C", field="f",
            claim_value=Decimal("50"), kfr_value=Decimal("50"),
            kfr_field_present=True, tolerance=0.5,  # float
        )
        r = check_numeric_drift(numeric_rows=[row])
        assert not r.success
        assert SUB_TAG_FLOAT_COMPARISON_DETECTED in r.fired_sub_tags


class TestOperationalDataDriftFromKfr:
    def test_op_data_drift_fires(self):
        r = check_numeric_drift(numeric_rows=[
            _row(Decimal("50"), kfr_value=Decimal("50"), tolerance=Decimal("0"),
                 op_data=Decimal("48")),
        ])
        assert not r.success
        assert SUB_TAG_OPERATIONAL_DATA_VALUE_DRIFT_FROM_KFR in r.fired_sub_tags

    def test_op_data_match_passes(self):
        r = check_numeric_drift(numeric_rows=[
            _row(Decimal("50"), kfr_value=Decimal("50"), tolerance=Decimal("0"),
                 op_data=Decimal("50")),
        ])
        assert r.success


class TestVariancePct:
    def test_canonical_rounding(self):
        # variance_pct(110, 100) = +10.00 %
        v = variance_pct(actual=Decimal("110"), budgeted=Decimal("100"))
        assert v == Decimal("10.00")

    def test_negative_variance(self):
        v = variance_pct(actual=Decimal("90"), budgeted=Decimal("100"))
        assert v == Decimal("-10.00")

    def test_round_half_up(self):
        v = variance_pct(actual=Decimal("100.005"), budgeted=Decimal("100"))
        # 0.005% → 0.01 with ROUND_HALF_UP
        assert v == Decimal("0.01")

    def test_quantize_precision(self):
        v = variance_pct(actual=Decimal("123.456"), budgeted=Decimal("100"))
        # 23.456% → 23.46
        assert v == Decimal("23.46")
        assert v.as_tuple().exponent == VARIANCE_QUANTIZE.as_tuple().exponent

    def test_zero_budgeted_raises(self):
        with pytest.raises(ZeroDivisionError):
            variance_pct(actual=Decimal("1"), budgeted=Decimal("0"))

    def test_float_arg_raises(self):
        with pytest.raises(TypeError, match="Decimal"):
            variance_pct(actual=0.5, budgeted=Decimal("1"))
        with pytest.raises(TypeError, match="Decimal"):
            variance_pct(actual=Decimal("1"), budgeted=0.5)
