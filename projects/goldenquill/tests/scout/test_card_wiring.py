"""Tests for pipeline.scout.card_wiring.

Verifies the Scout-specific projection out of a :class:`CardRuntimeContext`
surfaces the right CIC + CLC fields per the static seat-dependency registry.
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CIC_PATH = REPO_ROOT / "pipeline" / "cards" / "CIC" / "food_systems.yaml"
CLC_PATH = REPO_ROOT / "pipeline" / "cards" / "CLC" / "operating_capacity.yaml"


def _build_context():
    from pipeline.cards.runtime_context import build_card_runtime_context
    return build_card_runtime_context(
        cic_path=str(CIC_PATH),
        clc_path=str(CLC_PATH),
        environment="production",
    )


def test_scout_card_view_carries_cic_search_vocabulary():
    from pipeline.scout.card_wiring import build_scout_card_view

    view = build_scout_card_view(_build_context())
    assert view.cic_slug == "food_systems"
    assert "core_terms" in view.search_vocabulary
    assert "synonym_map" in view.search_vocabulary
    assert "funder_program_keywords" in view.search_vocabulary
    assert "disqualifier_terms" in view.search_vocabulary


def test_scout_card_view_search_vocabulary_carries_load_bearing_terms():
    from pipeline.scout.card_wiring import build_scout_card_view

    view = build_scout_card_view(_build_context())
    core_terms = {entry["term"] for entry in view.search_vocabulary["core_terms"]}
    # food_systems CIC carries these statutory definitions in Scout's vocab.
    assert "agricultural producer" in core_terms
    assert "specialty crop" in core_terms
    assert "value-added agriculture" in core_terms


def test_scout_card_view_carries_cic_evidence_signals():
    from pipeline.scout.card_wiring import build_scout_card_view

    view = build_scout_card_view(_build_context())
    kinds = {entry["kind"] for entry in view.evidence_signals}
    assert "sales_ledger" in kinds
    assert "buyer_letters_or_letters_of_intent" in kinds


def test_scout_card_view_carries_cic_kfr_fact_classes():
    from pipeline.scout.card_wiring import build_scout_card_view

    view = build_scout_card_view(_build_context())
    classes = {entry["fact_class"] for entry in view.kfr_fact_classes}
    assert "land_tenure" in classes
    assert "annual_revenue" in classes


def test_scout_card_view_carries_cic_admin_risk_register():
    from pipeline.scout.card_wiring import build_scout_card_view

    view = build_scout_card_view(_build_context())
    flagged = {entry["flagged_term"] for entry in view.admin_risk_term_register}
    assert "food sovereignty" in flagged


def test_scout_card_view_carries_clc_underwriting_criteria():
    from pipeline.scout.card_wiring import build_scout_card_view

    view = build_scout_card_view(_build_context())
    assert view.clc_slug == "operating_capacity"
    criteria = {entry["criterion"] for entry in view.underwriting_criteria}
    # operating_capacity CLC underwriting criteria drive Scout's funder-side
    # classification of incoming opportunities.
    assert "capacity_bottleneck" in criteria
    assert "mission_relationship" in criteria


def test_scout_card_view_is_frozen():
    import pytest
    from pipeline.scout.card_wiring import build_scout_card_view

    view = build_scout_card_view(_build_context())
    with pytest.raises(Exception):
        view.cic_slug = "other"  # type: ignore[misc]
