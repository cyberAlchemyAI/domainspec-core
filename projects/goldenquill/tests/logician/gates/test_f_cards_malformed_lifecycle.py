"""Tests for F-CARDS-MALFORMED-LIFECYCLE gate."""

from __future__ import annotations


def test_f_cards_malformed_lifecycle_imports():
    from pipeline.logician.gates import f_cards_malformed_lifecycle  # noqa: F401


def test_f_cards_malformed_lifecycle_gate_id():
    from pipeline.logician.gates.f_cards_malformed_lifecycle import GATE_ID
    assert GATE_ID == "F-CARDS-MALFORMED-LIFECYCLE"


def test_f_cards_malformed_lifecycle_evaluate_exists():
    from pipeline.logician.gates import f_cards_malformed_lifecycle
    assert hasattr(f_cards_malformed_lifecycle, "evaluate")
    assert callable(f_cards_malformed_lifecycle.evaluate)


def test_f_cards_malformed_lifecycle_rejects_draft_runtime_card():
    from pipeline.logician.gates.f_cards_malformed_lifecycle import evaluate

    outcome = evaluate(
        card_path="pipeline/cards/CIC/example.yaml",
        lifecycle_block={
            "draft_status": "draft",
            "review_status": "passed",
            "cross_family_thesis_status": "passed",
            "signature_status": "signed",
            "runtime_load_status": "loaded",
            "runtime_loadable": True,
            "signed_at": "2026-05-17T20:30:00Z",
            "signed_by": "founder",
            "content_hash": "sha256:" + "0" * 64,
        },
    )

    assert outcome.passed is False
    assert "Loader refuses draft cards" in outcome.message


def test_f_cards_malformed_lifecycle_accepts_signed_runtime_card_block():
    from pipeline.logician.gates.f_cards_malformed_lifecycle import evaluate

    outcome = evaluate(
        card_path="pipeline/cards/CIC/example.yaml",
        lifecycle_block={
            "draft_status": "signed",
            "review_status": "passed",
            "cross_family_thesis_status": "passed",
            "signature_status": "signed",
            "runtime_load_status": "loaded",
            "runtime_loadable": True,
            "signed_at": "2026-05-17T20:30:00Z",
            "signed_by": "founder",
            "content_hash": "sha256:" + "0" * 64,
        },
    )

    assert outcome.passed is True
