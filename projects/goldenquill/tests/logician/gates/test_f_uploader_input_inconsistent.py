"""Unit tests for F-UPLOADER-INPUT-INCONSISTENT (PRE-33).

Per Blueprint §12.9.5 + §4 v2.7 amendment.
"""

from __future__ import annotations

from pipeline.logician.gates.f_uploader_input_inconsistent import (
    F_UPLOADER_INPUT_INCONSISTENT,
    check_uploader_input_inconsistent,
)


def test_failure_code_constant() -> None:
    assert F_UPLOADER_INPUT_INCONSISTENT == "F-UPLOADER-INPUT-INCONSISTENT"


def test_equal_sets_pass() -> None:
    items = [
        ("narrative", "claim_1", "h_a"),
        ("budget", "claim_2", "h_b"),
    ]
    r = check_uploader_input_inconsistent(
        top_level_claim_evidence=items,
        section_drafts_claim_evidence=items,
    )
    assert r.success is True
    assert r.failure_code is None


def test_extra_in_top_level_fails() -> None:
    r = check_uploader_input_inconsistent(
        top_level_claim_evidence=[
            ("narrative", "claim_1", "h_a"),
            ("phantom", "claim_x", "h_x"),
        ],
        section_drafts_claim_evidence=[("narrative", "claim_1", "h_a")],
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_INPUT_INCONSISTENT
    assert ("phantom", "claim_x", "h_x") in r.only_in_top_level


def test_missing_from_top_level_fails() -> None:
    r = check_uploader_input_inconsistent(
        top_level_claim_evidence=[("narrative", "claim_1", "h_a")],
        section_drafts_claim_evidence=[
            ("narrative", "claim_1", "h_a"),
            ("budget", "claim_2", "h_b"),
        ],
    )
    assert r.success is False
    assert ("budget", "claim_2", "h_b") in r.only_in_sections


def test_divergent_payload_same_key_fails() -> None:
    """Same (section, claim_id) tuple keys but divergent hash → mismatch."""
    r = check_uploader_input_inconsistent(
        top_level_claim_evidence=[("narrative", "claim_1", "h_a")],
        section_drafts_claim_evidence=[("narrative", "claim_1", "h_DIFFERENT")],
    )
    assert r.success is False
    assert len(r.only_in_top_level) == 1
    assert len(r.only_in_sections) == 1


def test_both_empty_passes() -> None:
    r = check_uploader_input_inconsistent(
        top_level_claim_evidence=[],
        section_drafts_claim_evidence=[],
    )
    assert r.success is True
