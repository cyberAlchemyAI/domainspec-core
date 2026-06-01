"""Test stub for F-CARDS-COUPLING-VIOLATION-EXTENSION gate.

Per F-CLASS-* + F-PACKET-* family precedent: one test file per gate module.
Body NotImplementedError until v0.2 first wave; this stub verifies signature
shape + GATE_ID constant + family-roster discoverability.

Full predicate-body tests land at v0.2 first wave alongside body graduation.
"""

from __future__ import annotations

import pytest


def test_f_cards_coupling_violation_extension_imports():
    from pipeline.logician.gates import f_cards_coupling_violation_extension  # noqa: F401


def test_f_cards_coupling_violation_extension_gate_id():
    from pipeline.logician.gates.f_cards_coupling_violation_extension import GATE_ID
    assert GATE_ID == "F-CARDS-COUPLING-VIOLATION-EXTENSION"


def test_f_cards_coupling_violation_extension_evaluate_exists():
    from pipeline.logician.gates import f_cards_coupling_violation_extension
    assert hasattr(f_cards_coupling_violation_extension, "evaluate")
    assert callable(f_cards_coupling_violation_extension.evaluate)
