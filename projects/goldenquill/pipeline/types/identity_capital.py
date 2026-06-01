"""Canonical Customer Identity Category and Capital Logic Card enums.

These two enums are CLOSED. The CIC set is closed at 6; the CLC set is closed
at 8. Adding entries to either requires a new architecture amendment, not a
config edit. F-CIC-CLC-ENUM-DRIFT (PRE-gate at order 6.45) enforces this at
Tilth startup by hashing this module against an operator-signed reference and
validating the arg counts.

The two enums are ORTHOGONAL axes:

- CIC = applicant-side configuration (who applies; their Search Vocabulary,
  Evidence Schema, Language Register, Reporting Rhythm, and the
  opportunity-driven slot for Capital Logic Activation)
- CLC = funder-side mechanism (how funding may flow; its eligibility logic,
  example sources, and underwriting framing)

Any (CIC × CLC) pair is reachable in principle. The opportunity at hand drives
which CLC engages, not the customer archetype. Code that encodes any
``Mapping[CIC, Collection[CLC]]`` shape — or any field whose values are a
strict subset of either canonical enum in a context keyed by the other —
is a coupling violation; F-CIC-CLC-COUPLING-VIOLATION (PRE-gate at order 6.5)
fail-closes Tilth at startup if any such shape is detected.

Sources of truth (visual layer):

- ``CustomerIdentityCategory`` ← TILTH-CIC-REVIEW-01 + per-CIC cards
  TILTH-CIC-01..06 at ``assets/cards/customer_identification/``
- ``CapitalLogicCard`` ← TILTH-CLC-00 + per-CLC cards TILTH-CLC-01..08 at
  ``assets/cards/capital_logic/``

Architecture authority: ``pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md``
(LOCKED 2026-05-08).
"""

from __future__ import annotations

from typing import Final, Literal, get_args


# ---------------------------------------------------------------------------
# Customer Identity Categories (closed set, n=6)
# ---------------------------------------------------------------------------

CustomerIdentityCategory = Literal[
    "food_systems",
    "educator",
    "public_agency",
    "arts_culture",
    "cooperative",
    "ecosystem_intermediary",
]


# ---------------------------------------------------------------------------
# Capital Logic Cards (closed set, n=8)
# ---------------------------------------------------------------------------

CapitalLogicCard = Literal[
    "public_purpose_works",
    "catalytic_change",
    "operating_capacity",
    "research_evidence",
    "market_access",
    "credit_underwriting",
    "sponsorship_corporate",
    "shared_assets",
]


# ---------------------------------------------------------------------------
# Runtime-introspectable value tuples (used by F-CIC-CLC-ENUM-DRIFT count check
# and by F-CIC-CLC-COUPLING-VIOLATION value-set check)
# ---------------------------------------------------------------------------

CUSTOMER_IDENTITY_CATEGORY_VALUES: Final[tuple[str, ...]] = get_args(
    CustomerIdentityCategory
)
"""Frozen tuple of canonical CIC string values. Length must be 6."""

CAPITAL_LOGIC_CARD_VALUES: Final[tuple[str, ...]] = get_args(CapitalLogicCard)
"""Frozen tuple of canonical CLC string values. Length must be 8."""


# ---------------------------------------------------------------------------
# Display-name lookup tables
#
# These are used ONLY by Editor + customer-facing copy. They MUST NOT be used
# in routing decisions, scoring weights, or coupling logic — display strings
# don't participate in identity/capital semantics.
# ---------------------------------------------------------------------------

CIC_DISPLAY: Final[dict[str, str]] = {
    "food_systems": "Food Systems",
    "educator": "Educator",
    "public_agency": "Public Agency",
    "arts_culture": "Arts & Culture",
    "cooperative": "Cooperative",
    "ecosystem_intermediary": "Ecosystem Intermediary",
}
"""Canonical CIC display names. One entry per ``CustomerIdentityCategory`` value."""

CLC_DISPLAY: Final[dict[str, str]] = {
    "public_purpose_works": "Public Purpose & Works",
    "catalytic_change": "Catalytic Change",
    "operating_capacity": "Operating Capacity",
    "research_evidence": "Research & Evidence",
    "market_access": "Market Access",
    "credit_underwriting": "Credit & Underwriting",
    "sponsorship_corporate": "Sponsorship & Corporate Support",
    "shared_assets": "Shared Assets",
}
"""Canonical CLC display names. One entry per ``CapitalLogicCard`` value."""


# ---------------------------------------------------------------------------
# Closed-set count constants (referenced by F-CIC-CLC-ENUM-DRIFT)
# ---------------------------------------------------------------------------

CANONICAL_CIC_COUNT: Final[int] = 6
"""Frozen at 6 by architecture v7.0.8. Modification requires a new amendment."""

CANONICAL_CLC_COUNT: Final[int] = 8
"""Frozen at 8 by architecture v7.0.8. Modification requires a new amendment."""


def canonical_cic_count() -> int:
    """Return the canonical CIC count (6).

    Used by F-CIC-CLC-ENUM-DRIFT to validate that no entry has been silently
    added or removed from ``CustomerIdentityCategory``. The gate compares this
    against ``len(CUSTOMER_IDENTITY_CATEGORY_VALUES)`` and against the count
    declared in the v7.0.8 amendment text.
    """
    return CANONICAL_CIC_COUNT


def canonical_clc_count() -> int:
    """Return the canonical CLC count (8).

    Used by F-CIC-CLC-ENUM-DRIFT to validate that no entry has been silently
    added or removed from ``CapitalLogicCard``. The gate compares this against
    ``len(CAPITAL_LOGIC_CARD_VALUES)`` and against the count declared in the
    v7.0.8 amendment text.
    """
    return CANONICAL_CLC_COUNT


# ---------------------------------------------------------------------------
# Self-consistency checks at module load
#
# These run unconditionally at import time. They do NOT replace
# F-CIC-CLC-ENUM-DRIFT (which runs at PRE-gate time with hash + signature
# verification); they catch development-time drift between the Literal
# definition and the count constants / display tables.
# ---------------------------------------------------------------------------

assert len(CUSTOMER_IDENTITY_CATEGORY_VALUES) == CANONICAL_CIC_COUNT, (
    f"CustomerIdentityCategory has {len(CUSTOMER_IDENTITY_CATEGORY_VALUES)} "
    f"entries; canonical count is {CANONICAL_CIC_COUNT} per architecture "
    f"v7.0.8. Adding/removing entries requires a new amendment."
)

assert len(CAPITAL_LOGIC_CARD_VALUES) == CANONICAL_CLC_COUNT, (
    f"CapitalLogicCard has {len(CAPITAL_LOGIC_CARD_VALUES)} entries; "
    f"canonical count is {CANONICAL_CLC_COUNT} per architecture v7.0.8. "
    f"Adding/removing entries requires a new amendment."
)

assert set(CIC_DISPLAY.keys()) == set(CUSTOMER_IDENTITY_CATEGORY_VALUES), (
    "CIC_DISPLAY keys do not match CustomerIdentityCategory values."
)

assert set(CLC_DISPLAY.keys()) == set(CAPITAL_LOGIC_CARD_VALUES), (
    "CLC_DISPLAY keys do not match CapitalLogicCard values."
)
