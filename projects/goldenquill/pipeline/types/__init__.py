"""Canonical cross-cutting types for Tilth.

This package is the home for canonical types that don't belong to any single
seat or stage — types whose closed-set discipline is enforced by architecture
amendments, not by config.

Established by architecture amendment v7.0.8 (LOCKED 2026-05-08) at
``pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md``.
"""

from __future__ import annotations

from pipeline.types.identity_capital import (
    CAPITAL_LOGIC_CARD_VALUES,
    CIC_DISPLAY,
    CLC_DISPLAY,
    CUSTOMER_IDENTITY_CATEGORY_VALUES,
    CapitalLogicCard,
    CustomerIdentityCategory,
    canonical_clc_count,
    canonical_cic_count,
)

__all__ = [
    "CapitalLogicCard",
    "CustomerIdentityCategory",
    "CAPITAL_LOGIC_CARD_VALUES",
    "CUSTOMER_IDENTITY_CATEGORY_VALUES",
    "CIC_DISPLAY",
    "CLC_DISPLAY",
    "canonical_cic_count",
    "canonical_clc_count",
]
