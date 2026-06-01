"""Tests for §9 R2 responsiveness mapper.

Spec card: ``pipeline/engineering/spec_cards/section_09_judge_round_2_cross_rubric_and_verdict.md``.

Test surface (per spec card §6):

- VAPG f/g responsiveness factor extraction (qualifying_categories,
  qualifying_applicants, must_benefit, categories[*].name).
- Empty responsiveness factors (technical-only rubric) → empty
  ResponsivenessMap.
- Duplicate factor entries — input shape that would produce duplicate
  (criterion_id, factor_name) pairs is rejected by ResponsivenessMap.
- Malformed factor lists (non-list values, non-string entries, missing
  ``name`` in categories objects).
- Cross-rubric: build_responsiveness_map raises when criterion_extras
  reference an id absent from the rubric.
- KNOWN_RESPONSIVENESS_FACTOR_KEYS exposed on the public surface.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pipeline.seats.judge.responsiveness_mapper import (
    KNOWN_RESPONSIVENESS_FACTOR_KEYS,
    build_responsiveness_map,
    extract_responsiveness_factors_from_rubric_json,
)
from pipeline.seats.judge.rubric_loader import load_rubric
from pipeline.seats.judge.types import (
    ResponsivenessEntry,
    ResponsivenessMap,
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


def _crit(**overrides) -> RubricCriterion:
    kw = dict(
        id="x",
        name="X",
        max_points=10,
        scorer="review_panel",
        subcriteria=(),
        must_address=(),
        tiers=({"points": 5, "description": "ok"},),
    )
    kw.update(overrides)
    return RubricCriterion(**kw)


def _sub(**overrides) -> RubricSubCriterion:
    kw = dict(
        id="x.i",
        name="X.i",
        max_points=5,
        must_address=(),
        tiers=(),
    )
    kw.update(overrides)
    return RubricSubCriterion(**kw)


def _rubric(criteria: tuple[RubricCriterion, ...]) -> Rubric:
    sum_max = sum(c.max_points for c in criteria)
    return Rubric(
        program_code="TEST-FY26",
        funder="Test",
        nofo_number="TEST-001",
        max_score=max(sum_max, 1),
        min_score=0,
        criteria=criteria,
        rubric_sha256=SHA256_VALID,
        loaded_at_utc=UTC_NOW,
    )


# ---------------------------------------------------------------------------
# KNOWN_RESPONSIVENESS_FACTOR_KEYS surface
# ---------------------------------------------------------------------------


class TestKnownFactorKeys:
    def test_set_is_frozen(self):
        assert isinstance(KNOWN_RESPONSIVENESS_FACTOR_KEYS, frozenset)

    def test_known_keys_match_v1_closed_set(self):
        assert KNOWN_RESPONSIVENESS_FACTOR_KEYS == frozenset(
            {
                "qualifying_categories",
                "qualifying_applicants",
                "must_benefit",
                "categories",
            }
        )

    def test_module_constant_imported_via_seat_surface(self):
        from pipeline.seats.judge import (
            KNOWN_RESPONSIVENESS_FACTOR_KEYS as Re_export,
        )

        assert Re_export is KNOWN_RESPONSIVENESS_FACTOR_KEYS


# ---------------------------------------------------------------------------
# extract_responsiveness_factors_from_rubric_json
# ---------------------------------------------------------------------------


class TestExtractFromRubricJson:
    def test_vapg_extracts_f_and_g_factors(self):
        with VAPG_RUBRIC_PATH.open(encoding="utf-8") as fh:
            rubric_json = json.load(fh)
        out = extract_responsiveness_factors_from_rubric_json(rubric_json)
        # f.i carries qualifying_categories.
        assert "f.i" in out
        assert "qualifying_categories" in out["f.i"]
        # f.ii carries qualifying_applicants + must_benefit.
        assert "f.ii" in out
        assert "qualifying_applicants" in out["f.ii"]
        assert "must_benefit" in out["f.ii"]
        # g carries categories (flattened to names).
        assert "g" in out
        assert "categories" in out["g"]

    def test_vapg_categories_names_extracted_correctly(self):
        with VAPG_RUBRIC_PATH.open(encoding="utf-8") as fh:
            rubric_json = json.load(fh)
        out = extract_responsiveness_factors_from_rubric_json(rubric_json)
        assert out["g"]["categories"] == (
            "Never received VAPG",
            "Grant amount < $125,000",
            "Geographic diversity",
        )

    def test_vapg_qualifying_categories_first_entry(self):
        with VAPG_RUBRIC_PATH.open(encoding="utf-8") as fh:
            rubric_json = json.load(fh)
        out = extract_responsiveness_factors_from_rubric_json(rubric_json)
        assert out["f.i"]["qualifying_categories"][0] == (
            "Beginning Farmer or Rancher"
        )

    def test_vapg_no_factors_under_a_through_e(self):
        with VAPG_RUBRIC_PATH.open(encoding="utf-8") as fh:
            rubric_json = json.load(fh)
        out = extract_responsiveness_factors_from_rubric_json(rubric_json)
        for cid in ("a", "b", "c", "d", "e", "a.i", "a.ii", "a.iii"):
            assert cid not in out, (
                f"unexpected factor entry under criterion {cid!r}"
            )

    def test_empty_rubric_returns_empty_dict(self):
        out = extract_responsiveness_factors_from_rubric_json(
            {"meta": {}, "scoring_criteria": []}
        )
        assert out == {}

    def test_missing_scoring_criteria_returns_empty_dict(self):
        out = extract_responsiveness_factors_from_rubric_json({"meta": {}})
        assert out == {}

    def test_non_mapping_input_rejected(self):
        with pytest.raises(ValueError, match="must be a JSON object"):
            extract_responsiveness_factors_from_rubric_json("oops")  # type: ignore[arg-type]

    def test_non_list_scoring_criteria_rejected(self):
        with pytest.raises(
            ValueError, match="scoring_criteria must be a JSON array"
        ):
            extract_responsiveness_factors_from_rubric_json(
                {"scoring_criteria": "oops"}
            )

    def test_non_mapping_criterion_entry_rejected(self):
        with pytest.raises(
            ValueError, match=r"scoring_criteria\[0\] must be a JSON object"
        ):
            extract_responsiveness_factors_from_rubric_json(
                {"scoring_criteria": ["oops"]}
            )

    def test_criterion_id_missing_rejected(self):
        with pytest.raises(
            ValueError,
            match=r"scoring_criteria\[0\]\.id must be a non-empty string",
        ):
            extract_responsiveness_factors_from_rubric_json(
                {"scoring_criteria": [{}]}
            )

    def test_qualifying_categories_must_be_list(self):
        with pytest.raises(
            ValueError, match="qualifying_categories must be a JSON array"
        ):
            extract_responsiveness_factors_from_rubric_json(
                {
                    "scoring_criteria": [
                        {"id": "x", "qualifying_categories": "oops"}
                    ]
                }
            )

    def test_qualifying_categories_entry_must_be_string(self):
        with pytest.raises(
            ValueError,
            match=r"qualifying_categories\[1\] must be a non-empty string",
        ):
            extract_responsiveness_factors_from_rubric_json(
                {
                    "scoring_criteria": [
                        {
                            "id": "x",
                            "qualifying_categories": ["A", 42, "B"],
                        }
                    ]
                }
            )

    def test_categories_must_be_list(self):
        with pytest.raises(
            ValueError, match="categories must be a JSON array of objects"
        ):
            extract_responsiveness_factors_from_rubric_json(
                {"scoring_criteria": [{"id": "x", "categories": "oops"}]}
            )

    def test_categories_entry_must_be_object(self):
        with pytest.raises(
            ValueError, match=r"categories\[0\] must be a JSON object"
        ):
            extract_responsiveness_factors_from_rubric_json(
                {"scoring_criteria": [{"id": "x", "categories": ["oops"]}]}
            )

    def test_categories_entry_name_required(self):
        with pytest.raises(
            ValueError,
            match=r"categories\[0\]\.name must be a non-empty string",
        ):
            extract_responsiveness_factors_from_rubric_json(
                {
                    "scoring_criteria": [
                        {"id": "x", "categories": [{"max_points": 5}]}
                    ]
                }
            )

    def test_subcriteria_must_be_list(self):
        with pytest.raises(
            ValueError, match="subcriteria must be a JSON array"
        ):
            extract_responsiveness_factors_from_rubric_json(
                {"scoring_criteria": [{"id": "x", "subcriteria": "oops"}]}
            )

    def test_subcriterion_id_required(self):
        with pytest.raises(
            ValueError,
            match=(
                r"scoring_criteria\[0\]\.subcriteria\[0\]\.id must be a "
                r"non-empty string"
            ),
        ):
            extract_responsiveness_factors_from_rubric_json(
                {
                    "scoring_criteria": [
                        {"id": "x", "subcriteria": [{}]}
                    ]
                }
            )

    def test_subcriterion_must_be_object(self):
        with pytest.raises(
            ValueError,
            match=(
                r"scoring_criteria\[0\]\.subcriteria\[0\] must be a JSON object"
            ),
        ):
            extract_responsiveness_factors_from_rubric_json(
                {
                    "scoring_criteria": [
                        {"id": "x", "subcriteria": ["oops"]}
                    ]
                }
            )

    def test_empty_factor_list_skipped_silently(self):
        # An explicit empty list is treated as "no factor" and skipped
        # (would otherwise blow up at ResponsivenessEntry construction).
        out = extract_responsiveness_factors_from_rubric_json(
            {
                "scoring_criteria": [
                    {"id": "x", "qualifying_categories": []}
                ]
            }
        )
        assert out == {}

    def test_unknown_factor_key_silently_ignored(self):
        # Unknown keys are not policed by the mapper — rubric_loader is
        # the schema gate.
        out = extract_responsiveness_factors_from_rubric_json(
            {
                "scoring_criteria": [
                    {"id": "x", "some_unknown_key": ["A", "B"]}
                ]
            }
        )
        assert out == {}

    def test_null_factor_value_skipped(self):
        out = extract_responsiveness_factors_from_rubric_json(
            {
                "scoring_criteria": [
                    {"id": "x", "qualifying_categories": None}
                ]
            }
        )
        assert out == {}


# ---------------------------------------------------------------------------
# build_responsiveness_map
# ---------------------------------------------------------------------------


class TestBuildResponsivenessMap:
    def test_empty_extras_returns_empty_map(self):
        rubric = _rubric((_crit(id="x", scorer="review_panel"),))
        m = build_responsiveness_map(rubric, criterion_extras={})
        assert isinstance(m, ResponsivenessMap)
        assert m.entries == ()

    def test_single_factor_entry_assembled(self):
        rubric = _rubric((_crit(id="g", scorer="administrator"),))
        m = build_responsiveness_map(
            rubric,
            criterion_extras={
                "g": {"categories": ("Never received", "Geographic diversity")}
            },
        )
        assert len(m.entries) == 1
        assert m.entries[0] == ResponsivenessEntry(
            criterion_id="g",
            factor_name="categories",
            factor_values=("Never received", "Geographic diversity"),
        )

    def test_unknown_criterion_id_rejected(self):
        rubric = _rubric((_crit(id="x", scorer="review_panel"),))
        with pytest.raises(
            ValueError, match="criterion_extras key 'ghost'"
        ):
            build_responsiveness_map(
                rubric,
                criterion_extras={"ghost": {"categories": ("A",)}},
            )

    def test_subcriterion_id_accepted(self):
        sub = _sub(id="f.i", max_points=5)
        crit = _crit(
            id="f", scorer="state_office", subcriteria=(sub,), tiers=()
        )
        rubric = _rubric((crit,))
        m = build_responsiveness_map(
            rubric,
            criterion_extras={
                "f.i": {"qualifying_categories": ("Beginning Farmer",)}
            },
        )
        assert len(m.entries) == 1
        assert m.entries[0].criterion_id == "f.i"

    def test_multiple_factors_within_criterion_sorted_by_factor_name(self):
        sub = _sub(id="f.ii", max_points=5)
        crit = _crit(
            id="f", scorer="state_office", subcriteria=(sub,), tiers=()
        )
        rubric = _rubric((crit,))
        m = build_responsiveness_map(
            rubric,
            criterion_extras={
                "f.ii": {
                    "qualifying_applicants": ("X",),
                    "must_benefit": ("Y",),
                }
            },
        )
        # Sorted alphabetically: must_benefit < qualifying_applicants.
        assert tuple(e.factor_name for e in m.entries) == (
            "must_benefit",
            "qualifying_applicants",
        )

    def test_multiple_criteria_emitted_in_rubric_declaration_order(self):
        sub_f = _sub(id="f.i", max_points=5)
        crit_f = _crit(
            id="f", scorer="state_office", subcriteria=(sub_f,), tiers=()
        )
        crit_g = _crit(id="g", scorer="administrator", max_points=10)
        rubric = _rubric((crit_f, crit_g))
        m = build_responsiveness_map(
            rubric,
            criterion_extras={
                "g": {"categories": ("A",)},
                "f.i": {"qualifying_categories": ("B",)},
            },
        )
        # f.i comes before g per rubric declaration order, regardless of
        # criterion_extras dict insertion order.
        assert tuple(e.criterion_id for e in m.entries) == ("f.i", "g")

    def test_vapg_full_round_trip(self):
        rubric = load_rubric(VAPG_RUBRIC_PATH, clock=lambda: UTC_NOW)
        with VAPG_RUBRIC_PATH.open(encoding="utf-8") as fh:
            rubric_json = json.load(fh)
        extras = extract_responsiveness_factors_from_rubric_json(rubric_json)
        m = build_responsiveness_map(rubric, criterion_extras=extras)
        # We expect entries for f.i, f.ii (×2), and g — total 4 entries.
        assert len(m.entries) == 4
        keys = tuple((e.criterion_id, e.factor_name) for e in m.entries)
        assert keys == (
            ("f.i", "qualifying_categories"),
            ("f.ii", "must_benefit"),
            ("f.ii", "qualifying_applicants"),
            ("g", "categories"),
        )

    def test_empty_factor_values_rejected_by_entry(self):
        rubric = _rubric((_crit(id="g", scorer="administrator"),))
        with pytest.raises(
            ValueError, match="factor_values must be non-empty"
        ):
            build_responsiveness_map(
                rubric,
                criterion_extras={"g": {"categories": ()}},
            )

    def test_entries_are_responsiveness_entries(self):
        rubric = _rubric((_crit(id="g", scorer="administrator"),))
        m = build_responsiveness_map(
            rubric, criterion_extras={"g": {"categories": ("X",)}}
        )
        for e in m.entries:
            assert isinstance(e, ResponsivenessEntry)

    def test_returns_responsiveness_map_instance(self):
        rubric = _rubric((_crit(id="g", scorer="administrator"),))
        m = build_responsiveness_map(rubric, criterion_extras={})
        assert isinstance(m, ResponsivenessMap)

    def test_empty_extras_dict_for_one_criterion_skipped(self):
        # criterion_extras key with empty inner dict produces no entries
        # under that criterion (legitimate input — no factors recognized).
        rubric = _rubric((_crit(id="g", scorer="administrator"),))
        m = build_responsiveness_map(
            rubric, criterion_extras={"g": {}}
        )
        assert m.entries == ()
