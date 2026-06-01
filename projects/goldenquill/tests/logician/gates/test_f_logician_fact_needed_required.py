"""Unit tests for F-LOGICIAN-FACT-NEEDED-REQUIRED (PRE-SP0-sign-out, HARD_BLOCK).

Per architecture v7.0.4 §3.2 (J-04 / RT-08 closure).
"""

from __future__ import annotations

from pipeline.logician.gates.f_logician_fact_needed_required import (
    F_LOGICIAN_FACT_NEEDED_REQUIRED,
    NEEDED_STATUS_VALUES,
    check_fact_needed_required,
)


def _filled_fact(
    fact_id: str = "f1",
    funder: str | list[str] = "USDA-VAPG",
) -> dict:
    return {
        "id": fact_id,
        "what": "annual revenue FY25",
        "status": "FILLED",
        "value": 50000,
        "required_for_funder": funder,
    }


def _needed_fact(
    fact_id: str = "f2",
    what: str = "EIN",
    funder: str | list[str] = "USDA-VAPG",
) -> dict:
    return {
        "id": fact_id,
        "what": what,
        "status": "NEEDED",
        "required_for_funder": funder,
    }


def test_failure_code_constant() -> None:
    assert F_LOGICIAN_FACT_NEEDED_REQUIRED == "F-LOGICIAN-FACT-NEEDED-REQUIRED"


def test_needed_status_values_constant() -> None:
    assert "NEEDED" in NEEDED_STATUS_VALUES
    assert "needed" in NEEDED_STATUS_VALUES


def test_no_needed_facts_passes() -> None:
    r = check_fact_needed_required(
        kfr_facts=[_filled_fact("f1"), _filled_fact("f2")],
        current_rfa_funder_id="USDA-VAPG",
    )
    assert r.success is True
    assert r.gaps == ()


def test_needed_fact_required_for_other_funder_passes() -> None:
    r = check_fact_needed_required(
        kfr_facts=[_needed_fact("f1", funder="NSF-INCLUDES")],
        current_rfa_funder_id="USDA-VAPG",
    )
    assert r.success is True


def test_needed_fact_required_for_current_funder_hard_blocks() -> None:
    r = check_fact_needed_required(
        kfr_facts=[_needed_fact("ein", what="EIN")],
        current_rfa_funder_id="USDA-VAPG",
    )
    assert r.success is False
    assert r.failure_code == F_LOGICIAN_FACT_NEEDED_REQUIRED
    assert "HARD_BLOCK" in r.detail
    assert len(r.gaps) == 1
    assert r.gaps[0].fact_id == "ein"


def test_required_for_funder_as_list_matches() -> None:
    fact = _needed_fact("f", funder=["NSF-INCLUDES", "USDA-VAPG", "EPA-WAT"])
    r = check_fact_needed_required(
        kfr_facts=[fact],
        current_rfa_funder_id="USDA-VAPG",
    )
    assert r.success is False
    assert r.failure_code == F_LOGICIAN_FACT_NEEDED_REQUIRED


def test_lowercase_needed_status_also_blocks() -> None:
    fact = {
        "id": "x",
        "status": "needed",
        "required_for_funder": "USDA-VAPG",
    }
    r = check_fact_needed_required(
        kfr_facts=[fact],
        current_rfa_funder_id="USDA-VAPG",
    )
    assert r.success is False


def test_empty_funder_id_fails_closed() -> None:
    r = check_fact_needed_required(
        kfr_facts=[_filled_fact()],
        current_rfa_funder_id="   ",
    )
    assert r.success is False
    assert r.failure_code == F_LOGICIAN_FACT_NEEDED_REQUIRED
    assert "empty" in r.detail


def test_empty_kfr_passes() -> None:
    r = check_fact_needed_required(
        kfr_facts=[],
        current_rfa_funder_id="USDA-VAPG",
    )
    assert r.success is True


def test_multiple_gaps_all_surfaced() -> None:
    facts = [
        _needed_fact("ein", what="EIN"),
        _needed_fact("uei", what="UEI"),
        _filled_fact("rev"),
        _needed_fact("addr", what="Mailing address"),
    ]
    r = check_fact_needed_required(
        kfr_facts=facts,
        current_rfa_funder_id="USDA-VAPG",
    )
    assert r.success is False
    assert len(r.gaps) == 3
    gap_ids = {g.fact_id for g in r.gaps}
    assert gap_ids == {"ein", "uei", "addr"}


def test_non_mapping_facts_skipped() -> None:
    # Defensive: malformed entries don't crash the gate.
    facts = ["not a dict", None, _filled_fact("ok")]
    r = check_fact_needed_required(
        kfr_facts=facts,
        current_rfa_funder_id="USDA-VAPG",
    )
    assert r.success is True


def test_fact_without_required_for_funder_field_skipped() -> None:
    fact = {
        "id": "f",
        "status": "NEEDED",
        # no required_for_funder
    }
    r = check_fact_needed_required(
        kfr_facts=[fact],
        current_rfa_funder_id="USDA-VAPG",
    )
    assert r.success is True


def test_unidentified_fact_id_falls_back_to_placeholder() -> None:
    fact = {
        "status": "NEEDED",
        "required_for_funder": "USDA-VAPG",
    }
    r = check_fact_needed_required(
        kfr_facts=[fact],
        current_rfa_funder_id="USDA-VAPG",
    )
    assert r.success is False
    assert r.gaps[0].fact_id == "<unidentified>"
