from enum import Enum
from pydantic import BaseModel, ConfigDict
import hashlib
from typing import Optional

class CapitalEfficiencySignalType(str, Enum):
    ADVANCE_PAYMENT_REVIEW_SIGNAL = "ADVANCE_PAYMENT_REVIEW_SIGNAL"
    COST_SHARE_OR_MATCH_REVIEW_SIGNAL = "COST_SHARE_OR_MATCH_REVIEW_SIGNAL"
    PRE_AWARD_COST_REVIEW_SIGNAL = "PRE_AWARD_COST_REVIEW_SIGNAL"
    INDIRECT_COST_RECOVERY_REVIEW_SIGNAL = "INDIRECT_COST_RECOVERY_REVIEW_SIGNAL"

class CapitalEfficiencySignal(BaseModel):
    signal_id: str
    signal_type: CapitalEfficiencySignalType
    opportunity_id: str
    professional_review_boundary_note: str
    professional_review_owner: str
    review_required: bool = True

    model_config = ConfigDict(extra="forbid")

def generate_capital_efficiency_signal_id(opportunity_id: str, signal_type: str) -> str:
    """
    Deterministically generate a stable identity hash for a capital-efficiency signal
    derived from the opportunity and the type of signal discovered.
    """
    raw = f"{opportunity_id}:{signal_type}".encode("utf-8")
    h = hashlib.sha256(raw).hexdigest()
    return f"cesig_{h[:16]}"
