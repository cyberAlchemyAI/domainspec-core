"""Tests for the seven dormant F-CARDS-* + F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY
predicate signatures at v7.0.11 LOCK.

Bodies raise NotImplementedError; bodies graduate LIVE at v0.2 first wave.
The tests confirm signature shape + family roster + dormant-state-marker.
"""

from __future__ import annotations

import pytest


_DORMANT_GATE_MODULES = [
    ("pipeline.logician.gates.f_cards_schema_invalid", "F-CARDS-SCHEMA-INVALID"),
    ("pipeline.logician.gates.f_cards_unsigned_production_load", "F-CARDS-UNSIGNED-PRODUCTION-LOAD"),
    ("pipeline.logician.gates.f_cards_signature_invalid", "F-CARDS-SIGNATURE-INVALID"),
    ("pipeline.logician.gates.f_cards_private_data_in_card", "F-CARDS-PRIVATE-DATA-IN-CARD"),
    ("pipeline.logician.gates.f_cards_cross_org_namespace_leak", "F-CARDS-CROSS-ORG-NAMESPACE-LEAK"),
    ("pipeline.logician.gates.f_cards_malformed_lifecycle", "F-CARDS-MALFORMED-LIFECYCLE"),
    ("pipeline.logician.gates.f_cards_load_in_wrong_namespace", "F-CARDS-LOAD-IN-WRONG-NAMESPACE"),
    ("pipeline.logician.gates.f_cards_coupling_violation_extension", "F-CARDS-COUPLING-VIOLATION-EXTENSION"),
    ("pipeline.logician.gates.f_cic_clc_pattern_read_during_eligibility", "F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY"),
]


@pytest.mark.parametrize("module_path,expected_gate_id", _DORMANT_GATE_MODULES)
def test_each_dormant_gate_module_imports(module_path: str, expected_gate_id: str):
    import importlib
    m = importlib.import_module(module_path)
    assert m.GATE_ID == expected_gate_id


@pytest.mark.parametrize("module_path,expected_gate_id", _DORMANT_GATE_MODULES)
def test_each_dormant_gate_has_evaluate(module_path: str, expected_gate_id: str):
    import importlib
    m = importlib.import_module(module_path)
    assert hasattr(m, "evaluate")
    assert callable(m.evaluate)


def test_coupling_violation_extension_FORBIDDEN_FIELD_REGISTRY_is_live():
    """FORBIDDEN_FIELD_REGISTRY is LIVE at v7.0.11 LOCK (independent of the
    predicate body's NotImplementedError state) so R-CARDS-NO-COUPLING-FIELD
    AST-lint can scan card files at build time."""
    from types import MappingProxyType
    from pipeline.logician.gates.f_cards_coupling_violation_extension import (
        FORBIDDEN_FIELD_REGISTRY,
    )
    assert isinstance(FORBIDDEN_FIELD_REGISTRY, MappingProxyType)
    assert "common_clc_patterns_observed" in FORBIDDEN_FIELD_REGISTRY["CIC"]
    assert "eligible_clc_subset" in FORBIDDEN_FIELD_REGISTRY["CIC"]
    assert "eligible_cic_subset" in FORBIDDEN_FIELD_REGISTRY["CLC"]
    assert "preferred_cics" in FORBIDDEN_FIELD_REGISTRY["CLC"]


def test_pattern_read_constants_are_live():
    """ALLOWED_READERS_RETROSPECTIVE + FORBIDDEN_READERS_DURING_ELIGIBILITY +
    ELIGIBILITY_READ_CONTEXTS are LIVE at v7.0.11 LOCK."""
    from pipeline.logician.gates.f_cic_clc_pattern_read_during_eligibility import (
        ALLOWED_READERS_RETROSPECTIVE,
        FORBIDDEN_READERS_DURING_ELIGIBILITY,
        ELIGIBILITY_READ_CONTEXTS,
    )
    assert "Archivist" in ALLOWED_READERS_RETROSPECTIVE
    assert "Scout" in FORBIDDEN_READERS_DURING_ELIGIBILITY
    assert "Scribe" in FORBIDDEN_READERS_DURING_ELIGIBILITY
    assert "Judge" in FORBIDDEN_READERS_DURING_ELIGIBILITY
    assert "eligibility_evaluation" in ELIGIBILITY_READ_CONTEXTS
