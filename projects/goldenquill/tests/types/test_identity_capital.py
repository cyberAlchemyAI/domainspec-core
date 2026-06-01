"""Unit tests for the canonical CIC and CLC enums.

Verifies the closed-set discipline established by architecture v7.0.8 §1
(LOCKED 2026-05-08).
"""

from __future__ import annotations

from typing import get_args

from pipeline.types import (
    CAPITAL_LOGIC_CARD_VALUES,
    CIC_DISPLAY,
    CLC_DISPLAY,
    CUSTOMER_IDENTITY_CATEGORY_VALUES,
    CapitalLogicCard,
    CustomerIdentityCategory,
    canonical_cic_count,
    canonical_clc_count,
)
from pipeline.types.identity_capital import (
    CANONICAL_CIC_COUNT,
    CANONICAL_CLC_COUNT,
)


# ---------------------------------------------------------------------------
# Closed-set count discipline
# ---------------------------------------------------------------------------


def test_cic_canonical_count_is_six() -> None:
    """Per v7.0.8 §1, CIC set is closed at 6."""
    assert canonical_cic_count() == 6
    assert CANONICAL_CIC_COUNT == 6


def test_clc_canonical_count_is_eight() -> None:
    """Per v7.0.8 §1 + TILTH-CLC-00, CLC set is closed at 8."""
    assert canonical_clc_count() == 8
    assert CANONICAL_CLC_COUNT == 8


def test_cic_literal_arg_count_matches_canonical() -> None:
    """Cross-check: get_args(CustomerIdentityCategory) length == 6."""
    assert len(get_args(CustomerIdentityCategory)) == 6
    assert len(CUSTOMER_IDENTITY_CATEGORY_VALUES) == 6


def test_clc_literal_arg_count_matches_canonical() -> None:
    """Cross-check: get_args(CapitalLogicCard) length == 8."""
    assert len(get_args(CapitalLogicCard)) == 8
    assert len(CAPITAL_LOGIC_CARD_VALUES) == 8


# ---------------------------------------------------------------------------
# Canonical IDs (regression-pin against silent rename)
# ---------------------------------------------------------------------------


def test_cic_canonical_ids() -> None:
    """Pin the exact six CIC IDs from TILTH-CIC-REVIEW-01."""
    expected = (
        "food_systems",
        "educator",
        "public_agency",
        "arts_culture",
        "cooperative",
        "ecosystem_intermediary",
    )
    assert CUSTOMER_IDENTITY_CATEGORY_VALUES == expected


def test_clc_canonical_ids() -> None:
    """Pin the exact eight CLC IDs from TILTH-CLC-00."""
    expected = (
        "public_purpose_works",
        "catalytic_change",
        "operating_capacity",
        "research_evidence",
        "market_access",
        "credit_underwriting",
        "sponsorship_corporate",
        "shared_assets",
    )
    assert CAPITAL_LOGIC_CARD_VALUES == expected


# ---------------------------------------------------------------------------
# Display tables
# ---------------------------------------------------------------------------


def test_cic_display_keys_match_enum_values() -> None:
    """Display table must have exactly one entry per canonical CIC."""
    assert set(CIC_DISPLAY.keys()) == set(CUSTOMER_IDENTITY_CATEGORY_VALUES)


def test_clc_display_keys_match_enum_values() -> None:
    """Display table must have exactly one entry per canonical CLC."""
    assert set(CLC_DISPLAY.keys()) == set(CAPITAL_LOGIC_CARD_VALUES)


def test_cic_display_values_nonempty() -> None:
    for cic_id, display in CIC_DISPLAY.items():
        assert display.strip(), f"CIC {cic_id!r} has empty display name"


def test_clc_display_values_nonempty() -> None:
    for clc_id, display in CLC_DISPLAY.items():
        assert display.strip(), f"CLC {clc_id!r} has empty display name"


# ---------------------------------------------------------------------------
# No CIC×CLC overlap (sanity check — IDs in different namespaces)
# ---------------------------------------------------------------------------


def test_cic_and_clc_id_namespaces_disjoint() -> None:
    """A canonical CIC ID and a canonical CLC ID must never collide.

    Defends against accidental rename that creates a CIC entry matching a CLC
    entry (which would make Layer-3 value-set checks ambiguous).
    """
    cic_set = set(CUSTOMER_IDENTITY_CATEGORY_VALUES)
    clc_set = set(CAPITAL_LOGIC_CARD_VALUES)
    overlap = cic_set & clc_set
    assert overlap == set(), f"CIC×CLC ID overlap detected: {overlap}"
