import ast
from pathlib import Path

from pipeline.scout._channel_g_types import (
    BoardCategoryEnum,
    CycleStatusEnum,
    DeadlineStatusEnum,
    EligibilityStatusEnum,
    NormalizedScore,
    ScoringStatusEnum,
    SourceFreshnessStatusEnum,
)
from pipeline.scout._channel_g_normalizer import (
    normalize_score,
    normalize_eligibility_status,
    allocate_board_category,
)


def test_missing_score_not_zero():
    score = normalize_score(None)
    assert score.scoring_status == ScoringStatusEnum.UNAVAILABLE
    assert score.normalized_value is None

    score_empty = normalize_score("   ")
    assert score_empty.scoring_status == ScoringStatusEnum.UNAVAILABLE
    assert score_empty.normalized_value is None


def test_unknown_text_score_not_scored():
    score = normalize_score("needs analyst review")
    assert score.scoring_status == ScoringStatusEnum.NOT_YET_SCORED
    assert score.normalized_value is None
    assert score.rationale == "needs analyst review"


def test_fraction_score_normalizes():
    score = normalize_score("4/5")
    assert score.scoring_status == ScoringStatusEnum.SCORED
    assert score.normalized_value == 80.0
    assert score.score_scale == "0-5"


def test_percentage_score_normalizes():
    score = normalize_score("85%")
    assert score.scoring_status == ScoringStatusEnum.SCORED
    assert score.normalized_value == 85.0
    assert score.score_scale == "0-100"


def test_categorical_high_medium_low_normalizes():
    assert normalize_score("High").normalized_value == 85.0
    assert normalize_score("Strong").normalized_value == 85.0
    assert normalize_score("Medium").normalized_value == 50.0
    assert normalize_score("Med").normalized_value == 50.0
    assert normalize_score("Moderate").normalized_value == 50.0
    assert normalize_score("Low").normalized_value == 15.0
    assert normalize_score("Weak").normalized_value == 15.0
    assert normalize_score("High").score_scale == "categorical_high_medium_low"


def test_mixed_score_note_preserves_rationale():
    score = normalize_score("4/5 - strong technical fit")
    assert score.scoring_status == ScoringStatusEnum.SCORED
    assert score.normalized_value == 80.0
    assert score.score_scale == "0-5"
    assert score.rationale == "4/5 - strong technical fit"


def test_bare_low_numeric_does_not_auto_scale_to_high_score():
    score = normalize_score("4")
    assert score.scoring_status == ScoringStatusEnum.NOT_YET_SCORED
    assert score.normalized_value is None
    assert "Bare numeric value requires explicit scale confirmation." in score.rationale


def test_bare_high_numeric_uses_zero_to_100_scale():
    score = normalize_score("85")
    assert score.scoring_status == ScoringStatusEnum.SCORED
    assert score.normalized_value == 85.0
    assert score.score_scale == "0-100"


def test_bare_numeric_with_explicit_alias_context_can_use_1_to_5():
    score = normalize_score("4", alias_context="1-5")
    assert score.scoring_status == ScoringStatusEnum.SCORED
    assert score.normalized_value == 80.0
    assert score.score_scale == "1-5"


def test_unknown_eligibility_not_false():
    status = normalize_eligibility_status("")
    assert status == EligibilityStatusEnum.UNKNOWN


def _make_dummy_score(val: float | None = None) -> NormalizedScore:
    return NormalizedScore(
        scoring_status=ScoringStatusEnum.SCORED if val is not None else ScoringStatusEnum.NOT_YET_SCORED,
        raw_value=str(val) if val is not None else None,
        normalized_value=val,
        score_scale="0-100" if val is not None else None,
        rationale=None,
    )


def test_closed_recurring_becomes_next_cycle():
    cat = allocate_board_category(
        raw_lane_category=None,
        eligibility_status=EligibilityStatusEnum.CONFIRMED_TRUE,
        deadline_status=DeadlineStatusEnum.CLOSED,
        cycle_status=CycleStatusEnum.RECURRING,
        partner_requirement=False,
        partner_confirmed=False,
        has_active_hard_blocker=False,
        source_freshness_status=SourceFreshnessStatusEnum.CURRENT,
        total_score=_make_dummy_score(85.0),
    )
    assert cat == BoardCategoryEnum.NEXT_CYCLE


def test_hard_blocker_high_fit_becomes_prepare_not_park():
    cat = allocate_board_category(
        raw_lane_category=None,
        eligibility_status=EligibilityStatusEnum.CONFIRMED_TRUE,
        deadline_status=DeadlineStatusEnum.OPEN,
        cycle_status=CycleStatusEnum.CURRENT,
        partner_requirement=False,
        partner_confirmed=False,
        has_active_hard_blocker=True,
        source_freshness_status=SourceFreshnessStatusEnum.CURRENT,
        total_score=_make_dummy_score(85.0),
    )
    assert cat == BoardCategoryEnum.PREPARE


def test_partner_required_unconfirmed_becomes_partner_consortium():
    cat = allocate_board_category(
        raw_lane_category=None,
        eligibility_status=EligibilityStatusEnum.CONFIRMED_TRUE,
        deadline_status=DeadlineStatusEnum.OPEN,
        cycle_status=CycleStatusEnum.CURRENT,
        partner_requirement=True,
        partner_confirmed=False,
        has_active_hard_blocker=False,
        source_freshness_status=SourceFreshnessStatusEnum.CURRENT,
        total_score=_make_dummy_score(85.0),
    )
    assert cat == BoardCategoryEnum.PARTNER_CONSORTIUM


def test_confirmed_false_eligibility_parks():
    cat = allocate_board_category(
        raw_lane_category="Immediate",
        eligibility_status=EligibilityStatusEnum.CONFIRMED_FALSE,
        deadline_status=DeadlineStatusEnum.OPEN,
        cycle_status=CycleStatusEnum.CURRENT,
        partner_requirement=False,
        partner_confirmed=False,
        has_active_hard_blocker=False,
        source_freshness_status=SourceFreshnessStatusEnum.CURRENT,
        total_score=_make_dummy_score(90.0),
    )
    assert cat == BoardCategoryEnum.PARK


def test_unknown_score_falls_to_monitor_not_park():
    cat = allocate_board_category(
        raw_lane_category=None,
        eligibility_status=EligibilityStatusEnum.CONFIRMED_TRUE,
        deadline_status=DeadlineStatusEnum.OPEN,
        cycle_status=CycleStatusEnum.CURRENT,
        partner_requirement=False,
        partner_confirmed=False,
        has_active_hard_blocker=False,
        source_freshness_status=SourceFreshnessStatusEnum.CURRENT,
        total_score=_make_dummy_score(None),
    )
    assert cat == BoardCategoryEnum.MONITOR


def test_raw_alias_cannot_override_hard_exclusion():
    cat = allocate_board_category(
        raw_lane_category="Immediate",
        eligibility_status=EligibilityStatusEnum.CONFIRMED_FALSE,
        deadline_status=DeadlineStatusEnum.OPEN,
        cycle_status=CycleStatusEnum.CURRENT,
        partner_requirement=False,
        partner_confirmed=False,
        has_active_hard_blocker=False,
        source_freshness_status=SourceFreshnessStatusEnum.CURRENT,
        total_score=_make_dummy_score(90.0),
    )
    assert cat == BoardCategoryEnum.PARK


def test_no_banned_imports_in_normalizer():
    normalizer_path = Path(__file__).parent.parent.parent / "pipeline" / "scout" / "_channel_g_normalizer.py"
    banned = {
        "httpx", "requests", "playwright", "selenium",
        "asyncio", "openai", "anthropic", "google.generativeai",
        "csv", "openpyxl", "pathlib"
    }

    with open(normalizer_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(normalizer_path))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base_module = alias.name.split('.')[0]
                assert base_module not in banned, f"Found banned import: {alias.name}"
                assert alias.name not in banned, f"Found banned import: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                base_module = node.module.split('.')[0]
                assert base_module not in banned, f"Found banned import: {node.module}"
                assert node.module not in banned, f"Found banned import: {node.module}"
