"""§13.9.5 — field validator (KFR drift advisory) tests."""
from __future__ import annotations

from decimal import Decimal

from pipeline.orchestrator.seats.data_collector.field_validator import (
    DEFAULT_TOLERANCE_PCT,
    DRIFT_SUB_TAG_ABOVE,
    DRIFT_SUB_TAG_BELOW,
    DRIFT_SUB_TAG_UNIT_MISMATCH,
    check_numeric_drift,
    scan_inbound_for_pii_leak,
)


def test_drift_within_tolerance_returns_none():
    # 210 vs 200 ±10% → 5% drift → no advisory.
    advisory = check_numeric_drift(
        inbound_value=Decimal("210"), inbound_unit="count",
        kfr_fact_id="kfr-1", kfr_value=Decimal("200"), kfr_unit="count",
        field_class="graduates_count",
    )
    assert advisory is None


def test_drift_above_tolerance():
    # 300 vs 197 ±10% → ~52% drift → above tolerance.
    advisory = check_numeric_drift(
        inbound_value=Decimal("300"), inbound_unit="count",
        kfr_fact_id="kfr-1", kfr_value=Decimal("197"), kfr_unit="count",
        field_class="graduates_count",
    )
    assert advisory is not None
    assert advisory.sub_tag == DRIFT_SUB_TAG_ABOVE
    assert advisory.relative_drift > DEFAULT_TOLERANCE_PCT


def test_drift_below_tolerance():
    advisory = check_numeric_drift(
        inbound_value=Decimal("100"), inbound_unit="count",
        kfr_fact_id="kfr-1", kfr_value=Decimal("200"), kfr_unit="count",
        field_class="graduates_count",
    )
    assert advisory is not None
    assert advisory.sub_tag == DRIFT_SUB_TAG_BELOW


def test_unit_mismatch_wins():
    # Inbound dollars vs KFR thousands-of-dollars.
    advisory = check_numeric_drift(
        inbound_value=Decimal("5000"), inbound_unit="usd",
        kfr_fact_id="kfr-1", kfr_value=Decimal("5"), kfr_unit="usd_thousands",
        field_class="expenditures",
    )
    assert advisory is not None
    assert advisory.sub_tag == DRIFT_SUB_TAG_UNIT_MISMATCH


def test_zero_kfr_with_nonzero_inbound_fires():
    advisory = check_numeric_drift(
        inbound_value=Decimal("10"), inbound_unit="count",
        kfr_fact_id="kfr-1", kfr_value=Decimal("0"), kfr_unit="count",
        field_class="x",
    )
    assert advisory is not None
    assert advisory.sub_tag == DRIFT_SUB_TAG_ABOVE


def test_zero_zero_no_advisory():
    advisory = check_numeric_drift(
        inbound_value=Decimal("0"), inbound_unit="count",
        kfr_fact_id="kfr-1", kfr_value=Decimal("0"), kfr_unit="count",
        field_class="x",
    )
    assert advisory is None


def test_scan_pii_leak_semantic_slot():
    leaked, sub_tag = scan_inbound_for_pii_leak(b"Hello [SLOT_ANNUAL_REVENUE] world")
    assert leaked is True
    assert sub_tag == "semantic_slot_in_outbound"


def test_scan_pii_leak_opaque_slot_ok():
    leaked, sub_tag = scan_inbound_for_pii_leak(b"Hello [SLOT_001] world")
    assert leaked is False
    assert sub_tag is None


def test_scan_pii_leak_no_slot_token():
    leaked, sub_tag = scan_inbound_for_pii_leak(b"plain text no slots")
    assert leaked is False
