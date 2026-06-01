import pytest
from pipeline.nervous_system.scout_models.capital_efficiency_signals import (
    CapitalEfficiencySignalType,
    generate_capital_efficiency_signal_id,
)
from pipeline.nervous_system.scout_enrichment.capital_efficiency_discovery import discover_capital_efficiency_signals

class DummyOpportunity:
    def __init__(self, opp_id, title, description=""):
        self.opportunity_id = opp_id
        self.title = title
        self.description = description

def test_deterministic_signal_id():
    id1 = generate_capital_efficiency_signal_id("opp_123", "ADVANCE_PAYMENT_REVIEW_SIGNAL")
    id2 = generate_capital_efficiency_signal_id("opp_123", "ADVANCE_PAYMENT_REVIEW_SIGNAL")
    assert id1 == id2
    assert id1.startswith("cesig_")

def test_discover_advance_payment():
    opp = DummyOpportunity("100", "Solar Project - advance payment available")
    signals = discover_capital_efficiency_signals(opp)
    assert len(signals) == 1
    assert signals[0].signal_type == CapitalEfficiencySignalType.ADVANCE_PAYMENT_REVIEW_SIGNAL
    assert signals[0].opportunity_id == "100"

def test_discover_match_waiver():
    opp = DummyOpportunity("101", "Some grant", "matching requirement waived for certain entities.")
    signals = discover_capital_efficiency_signals(opp)
    assert len(signals) == 1
    assert signals[0].signal_type == CapitalEfficiencySignalType.COST_SHARE_OR_MATCH_REVIEW_SIGNAL
    assert signals[0].opportunity_id == "101"

def test_discover_multiple_signals():
    opp = DummyOpportunity(
        "102",
        "Great grant with pre-award costs and advance payment allowed",
        "Also indirect cost recovery is flexible via de minimis rate."
    )
    signals = discover_capital_efficiency_signals(opp)
    assert len(signals) == 3
    types = {s.signal_type for s in signals}
    assert CapitalEfficiencySignalType.ADVANCE_PAYMENT_REVIEW_SIGNAL in types
    assert CapitalEfficiencySignalType.PRE_AWARD_COST_REVIEW_SIGNAL in types
    assert CapitalEfficiencySignalType.INDIRECT_COST_RECOVERY_REVIEW_SIGNAL in types

def test_discover_no_signals():
    opp = DummyOpportunity("103", "Standard grant", "Standard terms.")
    signals = discover_capital_efficiency_signals(opp)
    assert len(signals) == 0

def test_no_id_returns_empty():
    opp = DummyOpportunity(None, "Grant with advance payment")
    signals = discover_capital_efficiency_signals(opp)
    assert len(signals) == 0
