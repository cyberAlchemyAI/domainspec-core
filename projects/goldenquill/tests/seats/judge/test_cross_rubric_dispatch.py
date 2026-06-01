"""Tests for §9 R2 cross-rubric dispatcher.

Spec card: ``pipeline/engineering/spec_cards/section_09_judge_round_2_cross_rubric_and_verdict.md``.

Test surface (per spec card §6):

- VAPG 7-criteria routing (a/b/c review_panel + d/e/f state_office +
  g administrator).
- Synthetic 3-criteria rubric routing (one per role).
- Edge: rubric with zero subcriteria (every score unit is a
  RubricCriterion).
- Mixed-coverage rubric (some criteria have subs, others don't) →
  dispatch_score_units flattens correctly.
- parent_criterion_for_unit resolves both criterion-level and
  subcriterion-level units.
- Order preservation within scorer-role buckets.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from pipeline.seats.judge.cross_rubric_dispatch import (
    dispatch_criteria_to_scorers,
    dispatch_score_units,
    parent_criterion_for_unit,
)
from pipeline.seats.judge.rubric_loader import load_rubric
from pipeline.seats.judge.types import (
    Rubric,
    RubricCriterion,
    RubricSubCriterion,
)


UTC = timezone.utc
UTC_NOW = datetime(2026, 4, 29, 12, 0, 0, tzinfo=UTC)
SHA256_VALID = "0" * 64
VAPG_RUBRIC_PATH = (
    Path(__file__).resolve().parents[3]
    / "pipeline"
    / "rubrics"
    / "vapg_fy26.json"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sub(**overrides) -> RubricSubCriterion:
    kw = dict(
        id="x.i",
        name="Sub",
        max_points=10,
        must_address=(),
        tiers=(),
    )
    kw.update(overrides)
    return RubricSubCriterion(**kw)


def _crit(**overrides) -> RubricCriterion:
    kw = dict(
        id="x",
        name="Crit",
        max_points=10,
        scorer="review_panel",
        subcriteria=(),
        must_address=(),
        tiers=({"points": 5, "description": "ok"},),
    )
    kw.update(overrides)
    return RubricCriterion(**kw)


def _rubric_with(criteria: tuple[RubricCriterion, ...], **overrides) -> Rubric:
    sum_max = sum(c.max_points for c in criteria)
    kw = dict(
        program_code="TEST-FY26",
        funder="Test",
        nofo_number="TEST-001",
        max_score=max(sum_max, 1),
        min_score=0,
        criteria=criteria,
        rubric_sha256=SHA256_VALID,
        loaded_at_utc=UTC_NOW,
    )
    kw.update(overrides)
    return Rubric(**kw)


def _vapg_rubric() -> Rubric:
    return load_rubric(VAPG_RUBRIC_PATH, clock=lambda: UTC_NOW)


# ---------------------------------------------------------------------------
# dispatch_criteria_to_scorers
# ---------------------------------------------------------------------------


class TestDispatchCriteriaToScorers:
    def test_vapg_seven_criteria_routing(self):
        rubric = _vapg_rubric()
        out = dispatch_criteria_to_scorers(rubric)
        assert tuple(c.id for c in out["review_panel"]) == ("a", "b", "c")
        assert tuple(c.id for c in out["state_office"]) == ("d", "e", "f")
        assert tuple(c.id for c in out["administrator"]) == ("g",)

    def test_all_three_roles_present_in_output(self):
        rubric = _vapg_rubric()
        out = dispatch_criteria_to_scorers(rubric)
        assert set(out.keys()) == {
            "review_panel",
            "state_office",
            "administrator",
        }

    def test_synthetic_three_criteria_routing(self):
        rubric = _rubric_with(
            (
                _crit(id="x", scorer="review_panel"),
                _crit(id="y", scorer="state_office"),
                _crit(id="z", scorer="administrator"),
            )
        )
        out = dispatch_criteria_to_scorers(rubric)
        assert tuple(c.id for c in out["review_panel"]) == ("x",)
        assert tuple(c.id for c in out["state_office"]) == ("y",)
        assert tuple(c.id for c in out["administrator"]) == ("z",)

    def test_only_one_role_used_returns_empty_buckets_for_others(self):
        rubric = _rubric_with(
            (
                _crit(id="x", scorer="review_panel"),
                _crit(id="y", scorer="review_panel"),
            )
        )
        out = dispatch_criteria_to_scorers(rubric)
        assert tuple(c.id for c in out["review_panel"]) == ("x", "y")
        assert out["state_office"] == ()
        assert out["administrator"] == ()

    def test_order_preserved_within_role_bucket(self):
        rubric = _rubric_with(
            (
                _crit(id="z", scorer="review_panel"),
                _crit(id="a", scorer="review_panel"),
                _crit(id="m", scorer="review_panel"),
            )
        )
        out = dispatch_criteria_to_scorers(rubric)
        assert tuple(c.id for c in out["review_panel"]) == ("z", "a", "m")

    def test_returned_mapping_is_fresh_dict(self):
        rubric = _vapg_rubric()
        out1 = dispatch_criteria_to_scorers(rubric)
        out2 = dispatch_criteria_to_scorers(rubric)
        # Mutating one must not affect the other.
        out1["review_panel"] = ()
        assert tuple(c.id for c in out2["review_panel"]) == ("a", "b", "c")

    def test_returned_buckets_are_tuples(self):
        rubric = _vapg_rubric()
        out = dispatch_criteria_to_scorers(rubric)
        assert isinstance(out["review_panel"], tuple)
        assert isinstance(out["state_office"], tuple)
        assert isinstance(out["administrator"], tuple)

    def test_each_bucket_total_max_points_is_consistent(self):
        rubric = _vapg_rubric()
        out = dispatch_criteria_to_scorers(rubric)
        rp_total = sum(c.max_points for c in out["review_panel"])
        so_total = sum(c.max_points for c in out["state_office"])
        ad_total = sum(c.max_points for c in out["administrator"])
        # 30+20+20 + 5+5+10 + 10 = 100
        assert rp_total == 70
        assert so_total == 20
        assert ad_total == 10
        assert rp_total + so_total + ad_total == 100


# ---------------------------------------------------------------------------
# dispatch_score_units
# ---------------------------------------------------------------------------


class TestDispatchScoreUnits:
    def test_vapg_full_flatten(self):
        rubric = _vapg_rubric()
        units = dispatch_score_units(rubric)
        assert tuple(u.id for u in units) == (
            "a.i",
            "a.ii",
            "a.iii",
            "b",
            "c",
            "d",
            "e",
            "f.i",
            "f.ii",
            "g",
        )

    def test_zero_subcriteria_uses_parent(self):
        rubric = _rubric_with(
            (
                _crit(id="b", scorer="review_panel"),
                _crit(id="c", scorer="review_panel"),
            )
        )
        units = dispatch_score_units(rubric)
        assert tuple(u.id for u in units) == ("b", "c")
        assert all(isinstance(u, RubricCriterion) for u in units)

    def test_all_subcriteria_emitted_no_parent(self):
        sub_a = _sub(id="a.i", max_points=10)
        sub_b = _sub(id="a.ii", max_points=10)
        crit = _crit(
            id="a", scorer="review_panel", subcriteria=(sub_a, sub_b),
            tiers=(),
        )
        rubric = _rubric_with((crit,), max_score=20)
        units = dispatch_score_units(rubric)
        assert tuple(u.id for u in units) == ("a.i", "a.ii")
        assert all(isinstance(u, RubricSubCriterion) for u in units)

    def test_mixed_subcriteria_and_flat_criteria_preserves_ordering(self):
        sub_x = _sub(id="x.i", max_points=10)
        crit_x = _crit(
            id="x", scorer="review_panel", subcriteria=(sub_x,), tiers=()
        )
        crit_y = _crit(id="y", scorer="state_office", max_points=5)
        rubric = _rubric_with((crit_x, crit_y), max_score=15)
        units = dispatch_score_units(rubric)
        assert tuple(u.id for u in units) == ("x.i", "y")

    def test_subcriteria_order_within_parent_preserved(self):
        sub_a = _sub(id="a.i", max_points=10)
        sub_b = _sub(id="a.ii", max_points=10)
        sub_c = _sub(id="a.iii", max_points=10)
        crit = _crit(
            id="a",
            scorer="review_panel",
            subcriteria=(sub_c, sub_a, sub_b),
            tiers=(),
        )
        rubric = _rubric_with((crit,), max_score=30)
        units = dispatch_score_units(rubric)
        assert tuple(u.id for u in units) == ("a.iii", "a.i", "a.ii")

    def test_single_criterion_no_subs_returns_singleton(self):
        rubric = _rubric_with((_crit(id="solo", max_points=10),))
        units = dispatch_score_units(rubric)
        assert len(units) == 1
        assert units[0].id == "solo"

    def test_all_subs_zero_max_points_still_emits_units(self):
        # Edge: zero max_points subcriteria are still real scoring units
        # (the LLM may legitimately score 0 — they are emitted).
        sub_a = _sub(id="a.i", max_points=0)
        sub_b = _sub(id="a.ii", max_points=0)
        crit = _crit(
            id="a",
            scorer="review_panel",
            max_points=0,
            subcriteria=(sub_a, sub_b),
            tiers=(),
        )
        rubric = _rubric_with((crit,), max_score=1)
        units = dispatch_score_units(rubric)
        assert tuple(u.id for u in units) == ("a.i", "a.ii")

    def test_vapg_total_max_points_at_unit_level_matches_rubric(self):
        rubric = _vapg_rubric()
        units = dispatch_score_units(rubric)
        # a.i+a.ii+a.iii (10+10+10) + b (20) + c (20) + d (5) + e (5) +
        # f.i+f.ii (5+5) + g (10) = 100
        assert sum(u.max_points for u in units) == 100


# ---------------------------------------------------------------------------
# parent_criterion_for_unit
# ---------------------------------------------------------------------------


class TestParentCriterionForUnit:
    def test_criterion_unit_is_its_own_parent(self):
        rubric = _vapg_rubric()
        crit_b = next(c for c in rubric.criteria if c.id == "b")
        parent = parent_criterion_for_unit(crit_b, rubric)
        assert parent is crit_b

    def test_subcriterion_resolves_to_parent_criterion(self):
        rubric = _vapg_rubric()
        crit_a = next(c for c in rubric.criteria if c.id == "a")
        sub_a_i = crit_a.subcriteria[0]
        parent = parent_criterion_for_unit(sub_a_i, rubric)
        assert parent is crit_a

    def test_subcriterion_id_unknown_raises_value_error(self):
        rubric = _vapg_rubric()
        ghost = _sub(id="ghost.i", max_points=5)
        with pytest.raises(ValueError, match="not found under any criterion"):
            parent_criterion_for_unit(ghost, rubric)

    def test_resolves_for_every_unit_dispatch_emits(self):
        rubric = _vapg_rubric()
        for unit in dispatch_score_units(rubric):
            parent = parent_criterion_for_unit(unit, rubric)
            assert isinstance(parent, RubricCriterion)
            # Parent's id is in the rubric's criteria.
            assert parent.id in {c.id for c in rubric.criteria}
