"""Test stub for F-CARDS-SIGNATURE-INVALID gate.

Per F-CLASS-* + F-PACKET-* family precedent: one test file per gate module.
Body NotImplementedError until v0.2 first wave; this stub verifies signature
shape + GATE_ID constant + family-roster discoverability.

Full predicate-body tests land at v0.2 first wave alongside body graduation.
"""

from __future__ import annotations

import pytest


def test_f_cards_signature_invalid_imports():
    from pipeline.logician.gates import f_cards_signature_invalid  # noqa: F401


def test_f_cards_signature_invalid_gate_id():
    from pipeline.logician.gates.f_cards_signature_invalid import GATE_ID
    assert GATE_ID == "F-CARDS-SIGNATURE-INVALID"


def test_f_cards_signature_invalid_evaluate_exists():
    from pipeline.logician.gates import f_cards_signature_invalid
    assert hasattr(f_cards_signature_invalid, "evaluate")
    assert callable(f_cards_signature_invalid.evaluate)
