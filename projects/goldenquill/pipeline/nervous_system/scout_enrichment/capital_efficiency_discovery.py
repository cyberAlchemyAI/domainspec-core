from typing import Any
from pipeline.nervous_system.scout_models.capital_efficiency_signals import (
    CapitalEfficiencySignal,
    CapitalEfficiencySignalType,
    generate_capital_efficiency_signal_id,
)

PROFESSIONAL_REVIEW_BOUNDARY_NOTE = (
    "Scout identified this as a potential capital-efficiency review signal. "
    "Eligibility, timing, dollar value, claimability, and documentation requirements "
    "must be reviewed by the appropriate accountant, payroll provider, agency, "
    "legal/tax professional, or other appropriate reviewer."
)

PROFESSIONAL_REVIEW_OWNER = "Tax Professional"

def discover_capital_efficiency_signals(opportunity: Any) -> tuple[CapitalEfficiencySignal, ...]:
    """
    Deterministically scan an opportunity read-model for keywords and phrases
    indicating capital efficiency possibilities (e.g. advance payments, match waivers).
    Returns synthetic, deterministic sidecar signals linked to the opportunity's identity.
    """
    signals: list[CapitalEfficiencySignal] = []

    # Try to extract an ID from the opportunity
    opp_id = getattr(opportunity, "id", None) or getattr(opportunity, "opportunity_id", None)
    if not opp_id:
        # If we can't get an ID, we can't link a signal reliably
        return tuple(signals)

    opp_id_str = str(opp_id)

    title = str(getattr(opportunity, "title", getattr(opportunity, "opportunity_title", ""))).lower()
    description = str(getattr(opportunity, "description", "")).lower()

    combined_text = f"{title} {description}"

    # Heuristics for ADVANCE_PAYMENT_REVIEW_SIGNAL
    if "advance payment" in combined_text or "advanced payment" in combined_text:
        signals.append(
            CapitalEfficiencySignal(
                signal_id=generate_capital_efficiency_signal_id(opp_id_str, CapitalEfficiencySignalType.ADVANCE_PAYMENT_REVIEW_SIGNAL.value),
                signal_type=CapitalEfficiencySignalType.ADVANCE_PAYMENT_REVIEW_SIGNAL,
                opportunity_id=opp_id_str,
                professional_review_boundary_note=PROFESSIONAL_REVIEW_BOUNDARY_NOTE,
                professional_review_owner=PROFESSIONAL_REVIEW_OWNER,
            )
        )

    # Heuristics for COST_SHARE_OR_MATCH_REVIEW_SIGNAL
    if "match waiver" in combined_text or "waiver of match" in combined_text or "matching requirement waived" in combined_text:
        signals.append(
            CapitalEfficiencySignal(
                signal_id=generate_capital_efficiency_signal_id(opp_id_str, CapitalEfficiencySignalType.COST_SHARE_OR_MATCH_REVIEW_SIGNAL.value),
                signal_type=CapitalEfficiencySignalType.COST_SHARE_OR_MATCH_REVIEW_SIGNAL,
                opportunity_id=opp_id_str,
                professional_review_boundary_note=PROFESSIONAL_REVIEW_BOUNDARY_NOTE,
                professional_review_owner=PROFESSIONAL_REVIEW_OWNER,
            )
        )

    # Heuristics for PRE_AWARD_COST_REVIEW_SIGNAL
    if "pre-award cost" in combined_text or "preaward cost" in combined_text or "pre-award spending" in combined_text:
        signals.append(
            CapitalEfficiencySignal(
                signal_id=generate_capital_efficiency_signal_id(opp_id_str, CapitalEfficiencySignalType.PRE_AWARD_COST_REVIEW_SIGNAL.value),
                signal_type=CapitalEfficiencySignalType.PRE_AWARD_COST_REVIEW_SIGNAL,
                opportunity_id=opp_id_str,
                professional_review_boundary_note=PROFESSIONAL_REVIEW_BOUNDARY_NOTE,
                professional_review_owner=PROFESSIONAL_REVIEW_OWNER,
            )
        )

    # Heuristics for INDIRECT_COST_RECOVERY_REVIEW_SIGNAL
    if "indirect cost recovery" in combined_text or "de minimis rate" in combined_text or "nicra" in combined_text:
        signals.append(
            CapitalEfficiencySignal(
                signal_id=generate_capital_efficiency_signal_id(opp_id_str, CapitalEfficiencySignalType.INDIRECT_COST_RECOVERY_REVIEW_SIGNAL.value),
                signal_type=CapitalEfficiencySignalType.INDIRECT_COST_RECOVERY_REVIEW_SIGNAL,
                opportunity_id=opp_id_str,
                professional_review_boundary_note=PROFESSIONAL_REVIEW_BOUNDARY_NOTE,
                professional_review_owner=PROFESSIONAL_REVIEW_OWNER,
            )
        )

    return tuple(signals)
