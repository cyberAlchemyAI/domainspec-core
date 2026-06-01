"""F-WPFA-COUNTERFACTUAL-INFLATION — PRE-emission gate. [§5.1.WPFA.7]

Trigger: counterfactual computed using a baseline model NOT actually in
the SN-LLC-signed registry. Defends against deployment-side number
inflation (a malicious deployment that quietly substitutes a high-cost
flagship to inflate the savings claim).

PRE-gate verifies receipt's ``baseline_model_id`` matches the loaded
registry's ``baseline_model_id`` EXACTLY (string identity, not contains
or pattern match).

M13: NOT bypassable for buyer-attested receipts (structural audit-integrity
gate). Internal-only receipts permit M13 with HIGH-severity admin-risk
entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional


F_WPFA_COUNTERFACTUAL_INFLATION: Final[str] = "F-WPFA-COUNTERFACTUAL-INFLATION"


@dataclass(frozen=True, kw_only=True)
class CounterfactualInflationResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    receipt_baseline: Optional[str] = None
    registry_baseline: Optional[str] = None


def check_f_wpfa_counterfactual_inflation(
    *,
    receipt_baseline_model_id: str,
    registry_baseline_model_id: str,
    is_buyer_attested: bool = False,
) -> CounterfactualInflationResult:
    """PRE-emission: receipt baseline_model_id MUST equal registry baseline."""
    if (
        not isinstance(receipt_baseline_model_id, str)
        or not receipt_baseline_model_id
    ):
        return CounterfactualInflationResult(
            success=False,
            failure_code=F_WPFA_COUNTERFACTUAL_INFLATION,
            detail="receipt_baseline_model_id missing or empty",
        )
    if (
        not isinstance(registry_baseline_model_id, str)
        or not registry_baseline_model_id
    ):
        return CounterfactualInflationResult(
            success=False,
            failure_code=F_WPFA_COUNTERFACTUAL_INFLATION,
            detail="registry_baseline_model_id missing or empty",
        )
    if receipt_baseline_model_id != registry_baseline_model_id:
        return CounterfactualInflationResult(
            success=False,
            failure_code=F_WPFA_COUNTERFACTUAL_INFLATION,
            detail=(
                f"receipt baseline_model_id {receipt_baseline_model_id!r} != "
                f"registry baseline_model_id {registry_baseline_model_id!r} — "
                "deployment-side counterfactual inflation guard fires"
                + (" (buyer-attested — M13 NOT permitted)" if is_buyer_attested else "")
            ),
            receipt_baseline=receipt_baseline_model_id,
            registry_baseline=registry_baseline_model_id,
        )
    return CounterfactualInflationResult(
        success=True,
        failure_code=None,
        detail=f"baseline {receipt_baseline_model_id!r} matches registry",
        receipt_baseline=receipt_baseline_model_id,
        registry_baseline=registry_baseline_model_id,
    )


__all__ = [
    "F_WPFA_COUNTERFACTUAL_INFLATION",
    "CounterfactualInflationResult",
    "check_f_wpfa_counterfactual_inflation",
]
