"""F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER — POST-write gate.

Per §13 Data Collector v1 LOCKED 2026-05-10 §13.16.2 RT-28 closure +
Cycle-2 RT-C2-10 closure (consent_tier enum validation).

After any write to ``orgs/<slug>/vault/operational/grants/<grant_id>/
period_<n>/beneficiary_records/``, verify the written record carries a
``consent_tier`` field whose value is in the v7.0.5 §6 enumerated literal
set ``{my_eyes_only, matchable_to_opportunities, composable_with_others}``.
Missing or out-of-enum → fail-closed write-rollback.

Composes defense-in-depth with AST-lint
``R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED`` (compile-time) +
``R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM`` (Pydantic-schema-time)
per §13.16.6.4 + Cycle-2 RT-C2-10.

Sub-tags:

* ``.consent_tier_missing``
* ``.consent_tier_out_of_enum``
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Mapping, Optional

F_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER: Final[str] = (
    "F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER"
)

PERMITTED_CONSENT_TIERS: Final[frozenset[str]] = frozenset({
    "my_eyes_only",
    "matchable_to_opportunities",
    "composable_with_others",
})

SUB_TAG_CONSENT_TIER_MISSING: Final[str] = ".consent_tier_missing"
SUB_TAG_CONSENT_TIER_OUT_OF_ENUM: Final[str] = ".consent_tier_out_of_enum"


@dataclass(frozen=True, kw_only=True)
class BeneficiaryConsentTierResult:
    """Result of F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER check."""

    success: bool
    failure_code: Optional[str]
    sub_tag: Optional[str]
    detail: str
    record_id: Optional[str] = None


def check_beneficiary_consent_tier(
    *,
    record: Mapping[str, object],
    record_id: Optional[str] = None,
) -> BeneficiaryConsentTierResult:
    """POST-write check on beneficiary_records sub-kind.

    Returns FAIL with rollback signal if ``consent_tier`` missing or
    out-of-enum. Caller is responsible for executing the rollback (this
    gate is purely a predicate).
    """
    if "consent_tier" not in record:
        return BeneficiaryConsentTierResult(
            success=False,
            failure_code=F_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER,
            sub_tag=SUB_TAG_CONSENT_TIER_MISSING,
            detail=(
                "beneficiary_records write missing required consent_tier "
                "field; rollback required"
            ),
            record_id=record_id,
        )
    consent_tier = record.get("consent_tier")
    if not isinstance(consent_tier, str) or consent_tier not in PERMITTED_CONSENT_TIERS:
        return BeneficiaryConsentTierResult(
            success=False,
            failure_code=F_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER,
            sub_tag=SUB_TAG_CONSENT_TIER_OUT_OF_ENUM,
            detail=(
                f"consent_tier={consent_tier!r} not in permitted set "
                f"{sorted(PERMITTED_CONSENT_TIERS)}; rollback required"
            ),
            record_id=record_id,
        )
    return BeneficiaryConsentTierResult(
        success=True,
        failure_code=None,
        sub_tag=None,
        detail=f"consent_tier={consent_tier!r} valid",
        record_id=record_id,
    )


__all__ = [
    "BeneficiaryConsentTierResult",
    "F_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER",
    "PERMITTED_CONSENT_TIERS",
    "SUB_TAG_CONSENT_TIER_MISSING",
    "SUB_TAG_CONSENT_TIER_OUT_OF_ENUM",
    "check_beneficiary_consent_tier",
]
