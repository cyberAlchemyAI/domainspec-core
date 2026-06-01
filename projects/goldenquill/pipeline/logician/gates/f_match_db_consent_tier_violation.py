"""F-MATCH-DB-CONSENT-TIER-VIOLATION — PRE-write gate (sovereignty + Law 4, P1).

Per architecture v7.0.5 §5.5 + companion `section_04_v7_0_5_companion.md`.

Two trigger surfaces:

* **Trigger A (forward-design — Stage-5 only):** a commons-side query attempts
  to read Match Database content beyond what the consent tier permits.
  v0.1 always trivially passes this leg because no commons-side query path
  exists.

* **Trigger B (v0.1-active):** any mutation of a Match DB entry's
  `consent_tier` field that lacks a fresh
  `operator_signature_per_consent_tier_change` row in the entry's
  `audit_chain`.

The gate enforces Trigger B at the Match DB write wrapper. No silent
upgrade path — moving an entry from `my_eyes_only` to
`composable_with_others` requires operator-signed write even by the
operator's own admin privileges.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Sequence


F_MATCH_DB_CONSENT_TIER_VIOLATION: Final[str] = "F-MATCH-DB-CONSENT-TIER-VIOLATION"

# Canonical audit_chain row kind for consent_tier mutation evidence.
CONSENT_TIER_SIGNATURE_KIND: Final[str] = "operator_signature_per_consent_tier_change"

# Permitted consent tiers per v7.0.5 §4.
PERMITTED_CONSENT_TIERS: Final[frozenset[str]] = frozenset({
    "my_eyes_only",
    "matchable_to_opportunities",
    "composable_with_others",
})


@dataclass(frozen=True, kw_only=True)
class ConsentTierViolationResult:
    """Result of F-MATCH-DB-CONSENT-TIER-VIOLATION check."""

    success: bool
    failure_code: Optional[str]
    detail: str


def _extract_tier(entry: Optional[Mapping[str, Any]]) -> Optional[str]:
    if entry is None:
        return None
    tier = entry.get("consent_tier")
    return tier if isinstance(tier, str) else None


def _has_fresh_consent_signature(audit_chain: Sequence[Mapping[str, Any]]) -> bool:
    """True iff `audit_chain` contains a row whose `kind` is the canonical
    consent-tier signature kind AND whose `signed_at_utc` is non-empty."""
    for row in audit_chain:
        if not isinstance(row, Mapping):
            continue
        if row.get("kind") != CONSENT_TIER_SIGNATURE_KIND:
            continue
        signed = row.get("signed_at_utc")
        if isinstance(signed, str) and signed.strip():
            return True
    return False


def check_match_db_consent_tier_violation(
    *,
    prior_entry: Optional[Mapping[str, Any]],
    new_entry: Mapping[str, Any],
    audit_chain: Sequence[Mapping[str, Any]],
) -> ConsentTierViolationResult:
    """PRE-write gate: consent_tier mutation requires fresh operator signature.

    Parameters
    ----------
    prior_entry
        The Match DB entry before the proposed write, or None for a new
        entry. The gate compares `prior_entry["consent_tier"]` to
        `new_entry["consent_tier"]` to detect mutation.
    new_entry
        The Match DB entry after the proposed write.
    audit_chain
        Audit chain rows the write will append. The gate scans for a
        canonical consent-tier signature row.

    Returns
    -------
    ConsentTierViolationResult. Passes when (a) `consent_tier` did not
    change, OR (b) tier changed AND audit_chain contains a fresh
    `operator_signature_per_consent_tier_change` row. Fails when tier
    changed AND no fresh signature row is present, OR when the new tier
    is not in the permitted enum.
    """
    new_tier = _extract_tier(new_entry)
    if new_tier is None:
        return ConsentTierViolationResult(
            success=False,
            failure_code=F_MATCH_DB_CONSENT_TIER_VIOLATION,
            detail="new_entry missing consent_tier field",
        )
    if new_tier not in PERMITTED_CONSENT_TIERS:
        return ConsentTierViolationResult(
            success=False,
            failure_code=F_MATCH_DB_CONSENT_TIER_VIOLATION,
            detail=(
                f"new_entry consent_tier {new_tier!r} not in permitted set "
                f"{sorted(PERMITTED_CONSENT_TIERS)!r}"
            ),
        )

    prior_tier = _extract_tier(prior_entry)
    if prior_tier == new_tier:
        return ConsentTierViolationResult(
            success=True,
            failure_code=None,
            detail=f"consent_tier unchanged ({new_tier!r})",
        )

    # Mutation detected (or new entry — prior_tier is None and new_tier is set).
    # Both cases require a fresh operator signature row in the audit chain.
    if _has_fresh_consent_signature(audit_chain):
        return ConsentTierViolationResult(
            success=True,
            failure_code=None,
            detail=(
                f"consent_tier mutation {prior_tier!r} → {new_tier!r} "
                "carries fresh operator signature row"
            ),
        )
    return ConsentTierViolationResult(
        success=False,
        failure_code=F_MATCH_DB_CONSENT_TIER_VIOLATION,
        detail=(
            f"consent_tier mutation {prior_tier!r} → {new_tier!r} lacks "
            f"required {CONSENT_TIER_SIGNATURE_KIND!r} audit_chain row "
            "with non-empty signed_at_utc"
        ),
    )
