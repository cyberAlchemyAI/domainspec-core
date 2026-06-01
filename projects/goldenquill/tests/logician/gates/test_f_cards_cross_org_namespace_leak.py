"""Test stub for F-CARDS-CROSS-ORG-NAMESPACE-LEAK gate.

Per F-CLASS-* + F-PACKET-* family precedent: one test file per gate module.
Body NotImplementedError until v0.2 first wave; this stub verifies signature
shape + GATE_ID constant + family-roster discoverability.

Full predicate-body tests land at v0.2 first wave alongside body graduation.
"""

from __future__ import annotations

import pytest


def test_f_cards_cross_org_namespace_leak_imports():
    from pipeline.logician.gates import f_cards_cross_org_namespace_leak  # noqa: F401


def test_f_cards_cross_org_namespace_leak_gate_id():
    from pipeline.logician.gates.f_cards_cross_org_namespace_leak import GATE_ID
    assert GATE_ID == "F-CARDS-CROSS-ORG-NAMESPACE-LEAK"


def test_f_cards_cross_org_namespace_leak_evaluate_exists():
    from pipeline.logician.gates import f_cards_cross_org_namespace_leak
    assert hasattr(f_cards_cross_org_namespace_leak, "evaluate")
    assert callable(f_cards_cross_org_namespace_leak.evaluate)
