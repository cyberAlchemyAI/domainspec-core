"""Unit tests for F-LOGICIAN-FACT-TOLERANCE-DRIFT (PRE-draft-read, RT-02).

Per architecture v7.0.4 §4.4.
"""

from __future__ import annotations

from pipeline.logician.gates.f_logician_fact_tolerance_drift import (
    F_LOGICIAN_FACT_TOLERANCE_DRIFT,
    LEDGER_KIND_WIDEN,
    LEDGER_KIND_WIDEN_RECONFIRM,
    TYPE_DEFAULT_TOLERANCE_PCT,
    check_fact_tolerance_drift,
)


def _reconfirm(
    fact_id: str,
    grant_cycle_id: str,
    timestamp: str = "2026-05-10T12:00:00Z",
) -> dict:
    return {
        "ledger_kind": LEDGER_KIND_WIDEN_RECONFIRM,
        "fact_id": fact_id,
        "grant_cycle_id": grant_cycle_id,
        "signed_at_utc": timestamp,
    }


def test_failure_code_constant() -> None:
    assert F_LOGICIAN_FACT_TOLERANCE_DRIFT == "F-LOGICIAN-FACT-TOLERANCE-DRIFT"


def test_ledger_kind_constants() -> None:
    assert LEDGER_KIND_WIDEN == "kfr_tolerance_widen"
    assert LEDGER_KIND_WIDEN_RECONFIRM == "kfr_tolerance_widen_reconfirm"


def test_type_default_tolerance_table_includes_all_v7_0_4_types() -> None:
    expected_types = {"identifier", "legal", "count", "currency",
                      "percentage", "date", "range"}
    assert expected_types <= set(TYPE_DEFAULT_TOLERANCE_PCT.keys())


def test_currency_default_is_zero_point_five() -> None:
    # J-01 closure: tightened currency default
    assert TYPE_DEFAULT_TOLERANCE_PCT["currency"] == 0.5


def test_count_default_is_two() -> None:
    assert TYPE_DEFAULT_TOLERANCE_PCT["count"] == 2.0


def test_within_default_passes_without_reconfirm() -> None:
    r = check_fact_tolerance_drift(
        fact_id="enrollment",
        fact_type="count",
        configured_tolerance_pct=2.0,  # exactly at default
        grant_cycle_id="cycle-2026Q2",
        ledger_entries=[],
    )
    assert r.success is True


def test_below_default_passes_without_reconfirm() -> None:
    r = check_fact_tolerance_drift(
        fact_id="enrollment",
        fact_type="count",
        configured_tolerance_pct=1.0,
        grant_cycle_id="cycle-2026Q2",
        ledger_entries=[],
    )
    assert r.success is True


def test_widened_without_reconfirm_fails() -> None:
    r = check_fact_tolerance_drift(
        fact_id="annual_revenue",
        fact_type="currency",
        configured_tolerance_pct=5.0,  # widened from 0.5
        grant_cycle_id="cycle-2026Q2",
        ledger_entries=[],
    )
    assert r.success is False
    assert r.failure_code == F_LOGICIAN_FACT_TOLERANCE_DRIFT
    assert "HARD_BLOCK" in r.detail


def test_widened_with_current_cycle_reconfirm_passes() -> None:
    r = check_fact_tolerance_drift(
        fact_id="annual_revenue",
        fact_type="currency",
        configured_tolerance_pct=5.0,
        grant_cycle_id="cycle-2026Q2",
        ledger_entries=[_reconfirm("annual_revenue", "cycle-2026Q2")],
    )
    assert r.success is True


def test_widened_with_other_cycle_reconfirm_fails() -> None:
    # Reconfirm in cycle A does not authorize widened tolerance in cycle B.
    r = check_fact_tolerance_drift(
        fact_id="annual_revenue",
        fact_type="currency",
        configured_tolerance_pct=5.0,
        grant_cycle_id="cycle-2026Q2",
        ledger_entries=[_reconfirm("annual_revenue", "cycle-2026Q1")],
    )
    assert r.success is False
    assert r.failure_code == F_LOGICIAN_FACT_TOLERANCE_DRIFT


def test_widened_with_reconfirm_for_other_fact_fails() -> None:
    r = check_fact_tolerance_drift(
        fact_id="annual_revenue",
        fact_type="currency",
        configured_tolerance_pct=5.0,
        grant_cycle_id="cycle-2026Q2",
        ledger_entries=[_reconfirm("acres_planted", "cycle-2026Q2")],
    )
    assert r.success is False
    assert r.failure_code == F_LOGICIAN_FACT_TOLERANCE_DRIFT


def test_unknown_fact_type_fails_closed() -> None:
    r = check_fact_tolerance_drift(
        fact_id="x",
        fact_type="invented_type",
        configured_tolerance_pct=0.0,
        grant_cycle_id="cycle-x",
        ledger_entries=[],
    )
    assert r.success is False
    assert r.failure_code == F_LOGICIAN_FACT_TOLERANCE_DRIFT
    assert "not in type-default" in r.detail


def test_negative_tolerance_fails_closed() -> None:
    r = check_fact_tolerance_drift(
        fact_id="x",
        fact_type="count",
        configured_tolerance_pct=-1.0,
        grant_cycle_id="cycle-x",
        ledger_entries=[],
    )
    assert r.success is False
    assert r.failure_code == F_LOGICIAN_FACT_TOLERANCE_DRIFT
    assert "negative" in r.detail


def test_identifier_zero_default_widening_requires_reconfirm() -> None:
    # Identifiers default to 0% — any positive tolerance is widening.
    r = check_fact_tolerance_drift(
        fact_id="ein",
        fact_type="identifier",
        configured_tolerance_pct=0.01,
        grant_cycle_id="cycle-2026Q2",
        ledger_entries=[],
    )
    assert r.success is False


def test_reconfirm_with_empty_signed_at_utc_does_not_count() -> None:
    bad_reconfirm = {
        "ledger_kind": LEDGER_KIND_WIDEN_RECONFIRM,
        "fact_id": "rev",
        "grant_cycle_id": "c",
        "signed_at_utc": "   ",
    }
    r = check_fact_tolerance_drift(
        fact_id="rev",
        fact_type="currency",
        configured_tolerance_pct=10.0,
        grant_cycle_id="c",
        ledger_entries=[bad_reconfirm],
    )
    assert r.success is False
    assert r.failure_code == F_LOGICIAN_FACT_TOLERANCE_DRIFT


def test_widen_only_kind_does_not_unblock() -> None:
    # Only RECONFIRM rows authorize; the original WIDEN row is informational.
    widen_row = {
        "ledger_kind": LEDGER_KIND_WIDEN,
        "fact_id": "rev",
        "grant_cycle_id": "c",
        "signed_at_utc": "2026-05-10T00:00:00Z",
    }
    r = check_fact_tolerance_drift(
        fact_id="rev",
        fact_type="currency",
        configured_tolerance_pct=10.0,
        grant_cycle_id="c",
        ledger_entries=[widen_row],
    )
    assert r.success is False


def test_type_defaults_override_used_when_supplied() -> None:
    # Test injection seam — supply override mapping.
    r = check_fact_tolerance_drift(
        fact_id="x",
        fact_type="custom",
        configured_tolerance_pct=3.0,
        grant_cycle_id="c",
        ledger_entries=[],
        type_defaults={"custom": 5.0},
    )
    assert r.success is True


def test_result_carries_diagnostic_fields() -> None:
    r = check_fact_tolerance_drift(
        fact_id="annual_revenue",
        fact_type="currency",
        configured_tolerance_pct=10.0,
        grant_cycle_id="c",
        ledger_entries=[],
    )
    assert r.fact_id == "annual_revenue"
    assert r.type_default_pct == 0.5
    assert r.configured_pct == 10.0
