"""Unit tests for F-CIC-CLC-MATCH-NULL.

Per architecture v7.0.8 §4.2 (LOCKED 2026-05-08).
"""

from __future__ import annotations

from typing import Optional

import pytest

from pipeline.logician.gates.f_cic_clc_match_null import (
    GATE_ID,
    PRE_GATE_ORDER,
    MatchNullResult,
    run,
)


# ---------------------------------------------------------------------------
# Reader fixtures
# ---------------------------------------------------------------------------


def _pc_reader(per_org: dict[str, Optional[list[str]]]):
    def _r(org_slug: str) -> Optional[list[str]]:
        return per_org.get(org_slug)
    return _r


def _opp_reader(per_opp: dict[str, Optional[str]]):
    def _r(opportunity_id: str) -> Optional[str]:
        return per_opp.get(opportunity_id)
    return _r


def _dorm_reader(per_org: dict[str, Optional[bool]]):
    def _r(org_slug: str) -> Optional[bool]:
        return per_org.get(org_slug, True)  # default to enforced if unknown
    return _r


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_gate_id() -> None:
    assert GATE_ID == "F-CIC-CLC-MATCH-NULL"


def test_pre_gate_order() -> None:
    assert PRE_GATE_ORDER == 6.6


# ---------------------------------------------------------------------------
# Happy path — both sides present and canonical
# ---------------------------------------------------------------------------


def test_both_sides_canonical_passes() -> None:
    r = run(
        org_slug="acme_school",
        opportunity_id="opp_123",
        project_context_reader=_pc_reader({"acme_school": ["educator"]}),
        opportunity_clc_reader=_opp_reader({"opp_123": "public_purpose_works"}),
        dormancy_reader=_dorm_reader({"acme_school": True}),
    )
    assert r.passed is True
    assert r.enforced is True
    assert r.subcodes == ()


def test_multi_cic_canonical_passes() -> None:
    """Multi-CIC org with valid IDs should pass."""
    r = run(
        org_slug="myco_coop",
        opportunity_id="opp_99",
        project_context_reader=_pc_reader(
            {"myco_coop": ["food_systems", "cooperative"]}
        ),
        opportunity_clc_reader=_opp_reader({"opp_99": "shared_assets"}),
        dormancy_reader=_dorm_reader({"myco_coop": True}),
    )
    assert r.passed is True


# ---------------------------------------------------------------------------
# CIC unset / invalid
# ---------------------------------------------------------------------------


def test_cic_unset_enforced_fails() -> None:
    r = run(
        org_slug="org1",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader({"org1": None}),
        opportunity_clc_reader=_opp_reader({"opp_1": "operating_capacity"}),
        dormancy_reader=_dorm_reader({"org1": True}),
    )
    assert r.passed is False
    assert r.enforced is True
    assert f"{GATE_ID}.cic_unset" in r.subcodes


def test_cic_empty_list_treated_as_unset() -> None:
    r = run(
        org_slug="org1",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader({"org1": []}),
        opportunity_clc_reader=_opp_reader({"opp_1": "operating_capacity"}),
        dormancy_reader=_dorm_reader({"org1": True}),
    )
    assert r.passed is False
    assert f"{GATE_ID}.cic_unset" in r.subcodes


def test_cic_invalid_canonical_id_fails() -> None:
    r = run(
        org_slug="org1",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader({"org1": ["not_a_real_cic"]}),
        opportunity_clc_reader=_opp_reader({"opp_1": "operating_capacity"}),
        dormancy_reader=_dorm_reader({"org1": True}),
    )
    assert r.passed is False
    assert f"{GATE_ID}.cic_invalid" in r.subcodes


def test_cic_partially_invalid_fails() -> None:
    """Multi-CIC list with one valid + one invalid still fails on invalid."""
    r = run(
        org_slug="org1",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader(
            {"org1": ["educator", "made_up_cic"]}
        ),
        opportunity_clc_reader=_opp_reader({"opp_1": "operating_capacity"}),
        dormancy_reader=_dorm_reader({"org1": True}),
    )
    assert r.passed is False
    assert f"{GATE_ID}.cic_invalid" in r.subcodes


# ---------------------------------------------------------------------------
# CLC unset / invalid
# ---------------------------------------------------------------------------


def test_clc_unset_enforced_fails() -> None:
    r = run(
        org_slug="org1",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader({"org1": ["educator"]}),
        opportunity_clc_reader=_opp_reader({"opp_1": None}),
        dormancy_reader=_dorm_reader({"org1": True}),
    )
    assert r.passed is False
    assert f"{GATE_ID}.clc_unset" in r.subcodes


def test_clc_empty_string_treated_as_unset() -> None:
    r = run(
        org_slug="org1",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader({"org1": ["educator"]}),
        opportunity_clc_reader=_opp_reader({"opp_1": ""}),
        dormancy_reader=_dorm_reader({"org1": True}),
    )
    assert r.passed is False
    assert f"{GATE_ID}.clc_unset" in r.subcodes


def test_clc_invalid_canonical_id_fails() -> None:
    r = run(
        org_slug="org1",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader({"org1": ["educator"]}),
        opportunity_clc_reader=_opp_reader({"opp_1": "validation_signals"}),
        dormancy_reader=_dorm_reader({"org1": True}),
    )
    assert r.passed is False
    assert f"{GATE_ID}.clc_invalid" in r.subcodes


# ---------------------------------------------------------------------------
# Per-org dormancy
# ---------------------------------------------------------------------------


def test_dormancy_active_emits_warning_not_block() -> None:
    """Dormancy active (None) → passed=False AND enforced=False (WARNING)."""
    r = run(
        org_slug="dormant_org",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader({"dormant_org": None}),
        opportunity_clc_reader=_opp_reader({"opp_1": "operating_capacity"}),
        dormancy_reader=_dorm_reader({"dormant_org": None}),
    )
    assert r.passed is False
    assert r.enforced is False
    assert "DORMANCY-WARNING" in r.detail


def test_pre_first_attempt_passes_silently() -> None:
    """Pre-first-attempt (False) → passed=True (no cycle attempted yet)."""
    r = run(
        org_slug="never_run",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader({"never_run": None}),
        opportunity_clc_reader=_opp_reader({"opp_1": None}),
        dormancy_reader=_dorm_reader({"never_run": False}),
    )
    assert r.passed is True
    assert r.enforced is False


def test_dormancy_expired_enforces() -> None:
    """Dormancy expired (True) → fail-closed enforced."""
    r = run(
        org_slug="post_dormancy",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader({"post_dormancy": None}),
        opportunity_clc_reader=_opp_reader({"opp_1": "operating_capacity"}),
        dormancy_reader=_dorm_reader({"post_dormancy": True}),
    )
    assert r.passed is False
    assert r.enforced is True
    assert "ENFORCED" in r.detail


# ---------------------------------------------------------------------------
# All canonical CIC and CLC values pass
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "cic_id",
    [
        "food_systems",
        "educator",
        "public_agency",
        "arts_culture",
        "cooperative",
        "ecosystem_intermediary",
    ],
)
def test_each_canonical_cic_accepted(cic_id: str) -> None:
    r = run(
        org_slug="org1",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader({"org1": [cic_id]}),
        opportunity_clc_reader=_opp_reader({"opp_1": "operating_capacity"}),
        dormancy_reader=_dorm_reader({"org1": True}),
    )
    assert r.passed is True


@pytest.mark.parametrize(
    "clc_id",
    [
        "public_purpose_works",
        "catalytic_change",
        "operating_capacity",
        "research_evidence",
        "market_access",
        "credit_underwriting",
        "sponsorship_corporate",
        "shared_assets",
    ],
)
def test_each_canonical_clc_accepted(clc_id: str) -> None:
    r = run(
        org_slug="org1",
        opportunity_id="opp_1",
        project_context_reader=_pc_reader({"org1": ["educator"]}),
        opportunity_clc_reader=_opp_reader({"opp_1": clc_id}),
        dormancy_reader=_dorm_reader({"org1": True}),
    )
    assert r.passed is True
