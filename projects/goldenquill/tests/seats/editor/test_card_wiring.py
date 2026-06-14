"""Tests for pipeline.seats.editor.card_wiring.

Verifies the Editor-specific projection out of a :class:`CardRuntimeContext`
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


def test_editor_card_view_carries_cic_register_defaults():
    from pipeline.seats.editor.card_wiring import build_editor_card_view

    view = build_editor_card_view(_build_context())
    assert view.cic_slug == "food_systems"
    # Editor needs the register defaults to match draft voice/tone.
    assert "language_register" in view.register_defaults
    assert "tone" in view.register_defaults


def test_editor_card_view_carries_cic_dialect_routing_table():
    from pipeline.seats.editor.card_wiring import build_editor_card_view

    view = build_editor_card_view(_build_context())
    # Editor uses dialect_routing to verify the draft's funder-dialect target.
    assert len(view.dialect_routing_table) >= 4


def test_editor_card_view_carries_cic_admin_risk_register():
    from pipeline.seats.editor.card_wiring import build_editor_card_view

    view = build_editor_card_view(_build_context())
    # Editor flags admin-risk terms in the draft for operator approval.
    flagged = {entry["flagged_term"] for entry in view.admin_risk_term_register}
    assert "food sovereignty" in flagged


def test_editor_card_view_carries_clc_common_red_flags():
    from pipeline.seats.editor.card_wiring import build_editor_card_view

    view = build_editor_card_view(_build_context())
    assert view.clc_slug == "operating_capacity"
    flags = {entry["flag"] for entry in view.common_red_flags}
    # operating_capacity CLC carries these load-bearing reviewer red flags.
    assert "vague_operating_support_request" in flags
    assert "sustainability_as_future_grants" in flags


def test_editor_card_view_carries_clc_reviewer_profile():
    from pipeline.seats.editor.card_wiring import build_editor_card_view

    view = build_editor_card_view(_build_context())
    assert "reviewer_types" in view.reviewer_profile_typical
    assert "reviewer_priorities" in view.reviewer_profile_typical


def test_editor_card_view_carries_clc_narrative_section_patterns():
    from pipeline.seats.editor.card_wiring import build_editor_card_view

    view = build_editor_card_view(_build_context())
    section_names = {entry["section_name"] for entry in view.narrative_section_patterns}
    assert "Capacity Need / Statement of Need" in section_names


def test_editor_card_view_is_frozen():
    import pytest
    from pipeline.seats.editor.card_wiring import build_editor_card_view

    view = build_editor_card_view(_build_context())
    with pytest.raises(Exception):
        view.cic_slug = "other"  # type: ignore[misc]
