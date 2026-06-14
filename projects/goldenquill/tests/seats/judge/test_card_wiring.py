"""Tests for pipeline.seats.judge.card_wiring.

Verifies the Judge-specific projection out of a :class:`CardRuntimeContext`
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


def test_judge_card_view_carries_cic_capacity_signals_required():
    from pipeline.seats.judge.card_wiring import build_judge_card_view

    view = build_judge_card_view(_build_context())
    assert view.cic_slug == "food_systems"
    signals = {entry["signal"] for entry in view.capacity_signals_required}
    # food_systems CIC carries SAM.gov registration as a load-bearing signal.
    assert "active SAM.gov registration + UEI" in signals


def test_judge_card_view_carries_cic_compliance_burdens():
    from pipeline.seats.judge.card_wiring import build_judge_card_view

    view = build_judge_card_view(_build_context())
    frameworks = {entry["framework"] for entry in view.compliance_burdens}
    # food_systems CIC carries 2 CFR 200 as a baseline federal-grant burden.
    assert "2 CFR 200 Uniform Guidance" in frameworks


def test_judge_card_view_carries_clc_underwriting_criteria():
    from pipeline.seats.judge.card_wiring import build_judge_card_view

    view = build_judge_card_view(_build_context())
    assert view.clc_slug == "operating_capacity"
    criteria = {entry["criterion"] for entry in view.underwriting_criteria}
    # operating_capacity CLC carries these load-bearing criteria.
    assert "capacity_bottleneck" in criteria
    assert "sustainability" in criteria


def test_judge_card_view_carries_clc_scoring_weight_patterns():
    from pipeline.seats.judge.card_wiring import build_judge_card_view

    view = build_judge_card_view(_build_context())
    rubrics = {entry["rubric_example"] for entry in view.scoring_weight_patterns}
    assert any("Foundation capacity" in name for name in rubrics)


def test_judge_card_view_carries_clc_evidence_weights():
    from pipeline.seats.judge.card_wiring import build_judge_card_view

    view = build_judge_card_view(_build_context())
    assert view.evidence_weights["workload_evidence"]["weight"] == "HIGH"


def test_judge_card_view_carries_clc_reviewer_profile():
    from pipeline.seats.judge.card_wiring import build_judge_card_view

    view = build_judge_card_view(_build_context())
    assert "reviewer_priorities" in view.reviewer_profile_typical
    assert "common_red_flags_from_reviewer_pov" in view.reviewer_profile_typical


def test_judge_card_view_carries_clc_common_red_flags():
    from pipeline.seats.judge.card_wiring import build_judge_card_view

    view = build_judge_card_view(_build_context())
    flags = {entry["flag"] for entry in view.common_red_flags}
    assert "vague_operating_support_request" in flags
    assert "weak_budget_mapping" in flags


def test_judge_card_view_is_frozen():
    import pytest
    from pipeline.seats.judge.card_wiring import build_judge_card_view

    view = build_judge_card_view(_build_context())
    with pytest.raises(Exception):
        view.cic_slug = "other"  # type: ignore[misc]
