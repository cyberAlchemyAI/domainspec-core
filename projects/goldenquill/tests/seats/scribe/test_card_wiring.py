"""Tests for pipeline.seats.scribe.card_wiring.

Verifies the Scribe-specific projection out of a :class:`CardRuntimeContext`
surfaces the right CIC + CLC fields per the static seat-dependency registry.
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
CIC_PATH = REPO_ROOT / "pipeline" / "cards" / "CIC" / "food_systems.yaml"
CLC_PATH = REPO_ROOT / "pipeline" / "cards" / "CLC" / "operating_capacity.yaml"


def _build_context():
    from pipeline.cards.runtime_context import build_card_runtime_context
    return build_card_runtime_context(
        cic_path=str(CIC_PATH),
        clc_path=str(CLC_PATH),
        environment="production",
    )


def test_scribe_card_view_carries_cic_register_defaults():
    from pipeline.seats.scribe.card_wiring import build_scribe_card_view

    view = build_scribe_card_view(_build_context())
    assert view.cic_slug == "food_systems"
    assert "language_register" in view.register_defaults
    assert "narrative_voice" in view.register_defaults
    assert "tone" in view.register_defaults


def test_scribe_card_view_carries_cic_dialect_routing_table():
    from pipeline.seats.scribe.card_wiring import build_scribe_card_view

    view = build_scribe_card_view(_build_context())
    axes = {entry["funder_political_axis"] for entry in view.dialect_routing_table}
    # food_systems CIC carries all four canonical funder political axes.
    assert "conservative" in axes
    assert "centrist" in axes
    assert "progressive" in axes
    assert "soul_fire" in axes


def test_scribe_card_view_carries_cic_admin_risk_register():
    from pipeline.seats.scribe.card_wiring import build_scribe_card_view

    view = build_scribe_card_view(_build_context())
    flagged_terms = {entry["flagged_term"] for entry in view.admin_risk_term_register}
    # food_systems CIC flags these load-bearing terms per the card.
    assert "food sovereignty" in flagged_terms
    assert "regenerative agriculture" in flagged_terms


def test_scribe_card_view_carries_cic_narrative_sections_typical():
    from pipeline.seats.scribe.card_wiring import build_scribe_card_view

    view = build_scribe_card_view(_build_context())
    assert "Goals and Outcomes (SMART)" in view.narrative_sections_typical
    assert "Budget and Budget Justification" in view.narrative_sections_typical


def test_scribe_card_view_carries_clc_narrative_section_patterns():
    from pipeline.seats.scribe.card_wiring import build_scribe_card_view

    view = build_scribe_card_view(_build_context())
    assert view.clc_slug == "operating_capacity"
    section_names = {entry["section_name"] for entry in view.narrative_section_patterns}
    # operating_capacity CLC carries these standard capacity-grant sections.
    assert "Capacity Need / Statement of Need" in section_names
    assert "Sustainability Plan" in section_names


def test_scribe_card_view_carries_clc_evidence_weights():
    from pipeline.seats.scribe.card_wiring import build_scribe_card_view

    view = build_scribe_card_view(_build_context())
    # operating_capacity CLC weights workload + staffing + strategic_plan HIGH.
    assert view.evidence_weights["workload_evidence"]["weight"] == "HIGH"
    assert view.evidence_weights["staffing_plan"]["weight"] == "HIGH"
    assert view.evidence_weights["strategic_plan"]["weight"] == "HIGH"


def test_scribe_card_view_carries_clc_budget_structure_conventions():
    from pipeline.seats.scribe.card_wiring import build_scribe_card_view

    view = build_scribe_card_view(_build_context())
    assert "direct_cost_categories" in view.budget_structure_conventions
    assert "indirect_cost_treatment" in view.budget_structure_conventions


def test_scribe_card_view_is_frozen():
    """A12 mandate: ScribeCardView is frozen and rebind-resistant."""

    import pytest
    from pipeline.seats.scribe.card_wiring import build_scribe_card_view

    view = build_scribe_card_view(_build_context())
    with pytest.raises(Exception):
        view.cic_slug = "other"  # type: ignore[misc]
