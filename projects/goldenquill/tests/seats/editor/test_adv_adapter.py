"""tests/seats/editor/test_adv_adapter.py — defensive branch coverage.

Targets the shape-validation branches of ``adapter.py`` that are unreachable
through corpus-style happy-path inputs but matter for skill-output drift
hardening (per spec card §11 + parent §9 failure modes).

These tests construct minimal-but-malformed skill JSON payloads that
trip each defensive branch in ``_map_*`` helpers, ensuring every
``EditorOutputShapeError`` raise site has an exercising test.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from pipeline.seats.editor import (
    EditorInput,
    EditorOutput,
    EditorOutputShapeError,
    F_EDITOR_OUTPUT_SHAPE,
    SkillSubprocessResult,
    invoke_editor_adapter,
)
from pipeline.seats.editor.adapter import (
    _map_flagged_term,
    _map_gaps,
    _map_readability,
    _map_replacement_options,
    _map_skill_json_to_editor_output,
    _map_taxonomy_check,
    _map_tone_feedback,
    _render_section_drafts_to_markdown,
    _require_int_field,
    _require_list_field,
    _require_str_field,
)


UTC = timezone.utc


def _clock():
    return datetime(2026, 4, 29, 12, 0, tzinfo=UTC)


class _OneShotLauncher:
    def __init__(self, stdout: str):
        self.stdout = stdout

    def __call__(self, **_kwargs):
        return SkillSubprocessResult(stdout=self.stdout, exit_code=0)


def _input() -> EditorInput:
    return EditorInput(
        section_drafts=(
            {
                "section_name": "1.a",
                "section_order": 1,
                "body_text": (
                    "Body text long enough to anchor rewrite-detection "
                    "math under any small replacement set."
                ),
            },
        ),
        rfa_excerpt="rfa",
        dialect="centrist",
        session_id="s",
        org_slug="o",
    )


# ---------------------------------------------------------------------------
# _require_str_field / _require_int_field / _require_list_field
# ---------------------------------------------------------------------------


class TestFieldHelpers:
    def test_require_str_missing_at_top(self):
        with pytest.raises(EditorOutputShapeError, match="missing"):
            _require_str_field({}, "x")

    def test_require_str_missing_nested(self):
        with pytest.raises(EditorOutputShapeError, match="missing"):
            _require_str_field({"a": {}}, "a.b")

    def test_require_str_wrong_type(self):
        with pytest.raises(EditorOutputShapeError, match="must be string"):
            _require_str_field({"a": 1}, "a")

    def test_require_str_empty_when_strip(self):
        with pytest.raises(EditorOutputShapeError, match="non-empty"):
            _require_str_field({"a": "   "}, "a")

    def test_require_str_allow_empty(self):
        assert _require_str_field({"a": ""}, "a", allow_empty=True) == ""

    def test_require_int_missing(self):
        with pytest.raises(EditorOutputShapeError, match="missing"):
            _require_int_field({}, "x")

    def test_require_int_wrong_type(self):
        with pytest.raises(EditorOutputShapeError, match="must be int"):
            _require_int_field({"x": "1"}, "x")

    def test_require_int_rejects_bool(self):
        with pytest.raises(EditorOutputShapeError, match="must be int"):
            _require_int_field({"x": True}, "x")

    def test_require_int_passes(self):
        assert _require_int_field({"x": 7}, "x") == 7

    def test_require_list_missing(self):
        with pytest.raises(EditorOutputShapeError, match="missing"):
            _require_list_field({}, "x")

    def test_require_list_wrong_type(self):
        with pytest.raises(EditorOutputShapeError, match="must be list"):
            _require_list_field({"x": {}}, "x")


# ---------------------------------------------------------------------------
# _render_section_drafts_to_markdown
# ---------------------------------------------------------------------------


class TestRender:
    def test_default_clock_via_invocation(self):
        # Force the default _default_utc_now seam to fire by NOT passing
        # clock= (line 266 default branch).
        launcher = _OneShotLauncher(_minimal_valid_json())
        out = invoke_editor_adapter(_input(), skill_launcher=launcher)
        assert isinstance(out, EditorOutput)

    def test_render_orders_by_section_order(self):
        drafts = (
            {"section_name": "B", "section_order": 2, "body_text": "Bbody"},
            {"section_name": "A", "section_order": 1, "body_text": "Abody"},
        )
        md = _render_section_drafts_to_markdown(drafts)
        assert md.index("## A") < md.index("## B")
        assert md.endswith("\n")


# ---------------------------------------------------------------------------
# _map_replacement_options
# ---------------------------------------------------------------------------


class TestMapReplacementOptions:
    def test_non_object_entry(self):
        with pytest.raises(EditorOutputShapeError, match="options"):
            _map_replacement_options(["not-a-dict"])

    def test_invalid_label(self):
        with pytest.raises(EditorOutputShapeError, match="label"):
            _map_replacement_options(
                [{"label": "Z", "text": "x", "note": ""}]
            )

    def test_missing_text(self):
        with pytest.raises(EditorOutputShapeError, match="text"):
            _map_replacement_options(
                [{"label": "A", "text": "", "note": ""}]
            )

    def test_text_not_string(self):
        with pytest.raises(EditorOutputShapeError, match="text"):
            _map_replacement_options(
                [{"label": "A", "text": 123, "note": ""}]
            )

    def test_note_not_string(self):
        with pytest.raises(EditorOutputShapeError, match="note"):
            _map_replacement_options(
                [{"label": "A", "text": "x", "note": 12}]
            )


# ---------------------------------------------------------------------------
# _map_flagged_term
# ---------------------------------------------------------------------------


class TestMapFlaggedTerm:
    def _base(self) -> dict:
        return {
            "section": "1.a",
            "issue_type": "jargon",
            "severity": "low",
            "original": "vague",
            "issue": "y",
            "options": [
                {"label": "A", "text": "a", "note": ""},
                {"label": "B", "text": "b", "note": ""},
            ],
            "rubric_connection": "",
        }

    def test_invalid_severity(self):
        d = self._base()
        d["severity"] = "catastrophic"
        with pytest.raises(EditorOutputShapeError, match="severity"):
            _map_flagged_term(d, 0)

    def test_missing_section(self):
        d = self._base()
        d["section"] = ""
        with pytest.raises(EditorOutputShapeError, match="section"):
            _map_flagged_term(d, 0)

    def test_section_wrong_type(self):
        d = self._base()
        d["section"] = 123
        with pytest.raises(EditorOutputShapeError, match="section"):
            _map_flagged_term(d, 0)

    def test_missing_original(self):
        d = self._base()
        d["original"] = ""
        with pytest.raises(EditorOutputShapeError, match="original"):
            _map_flagged_term(d, 0)

    def test_missing_issue(self):
        d = self._base()
        d["issue"] = ""
        with pytest.raises(EditorOutputShapeError, match="issue"):
            _map_flagged_term(d, 0)

    def test_options_not_list(self):
        d = self._base()
        d["options"] = "not list"
        with pytest.raises(EditorOutputShapeError, match="options"):
            _map_flagged_term(d, 0)

    def test_rubric_connection_wrong_type(self):
        d = self._base()
        d["rubric_connection"] = 1
        with pytest.raises(EditorOutputShapeError, match="rubric_connection"):
            _map_flagged_term(d, 0)


# ---------------------------------------------------------------------------
# _map_taxonomy_check
# ---------------------------------------------------------------------------


class TestMapTaxonomy:
    def test_non_mapping(self):
        with pytest.raises(EditorOutputShapeError, match="taxonomy_check"):
            _map_taxonomy_check("not a dict")

    def test_category_not_list(self):
        with pytest.raises(EditorOutputShapeError, match="goals_identified"):
            _map_taxonomy_check({"goals_identified": "x"})

    def test_category_entry_empty(self):
        with pytest.raises(EditorOutputShapeError, match="goals_identified"):
            _map_taxonomy_check({"goals_identified": [""]})

    def test_misc_not_list(self):
        with pytest.raises(EditorOutputShapeError, match="miscategorizations"):
            _map_taxonomy_check({"miscategorizations": "x"})

    def test_misc_entry_not_object(self):
        with pytest.raises(EditorOutputShapeError, match="miscategorizations"):
            _map_taxonomy_check({"miscategorizations": ["not-dict"]})

    def test_full_block(self):
        tx = _map_taxonomy_check(
            {
                "goals_identified": ["g"],
                "miscategorizations": [
                    {"excerpt": "e", "stated_as": "g", "should_be": "o", "why": "w"}
                ],
            }
        )
        assert tx.goals_identified == ("g",)
        assert len(tx.miscategorizations) == 1


# ---------------------------------------------------------------------------
# _map_readability
# ---------------------------------------------------------------------------


class TestMapReadability:
    def test_non_mapping(self):
        with pytest.raises(EditorOutputShapeError, match="readability"):
            _map_readability("x")

    def test_score_10_path(self):
        r = _map_readability(
            {"score_10": 9, "grade_level_estimate": "g", "verdict": "v"}
        )
        assert r.score_10 == 9

    def test_grade_level_10_to_12_maps_to_8(self):
        r = _map_readability(
            {"estimated_grade_level": 11, "verdict": "v"}
        )
        assert r.score_10 == 8
        assert r.grade_level_estimate == "grade 11"

    def test_grade_level_below_10_maps_to_6(self):
        r = _map_readability(
            {"estimated_grade_level": 8, "verdict": "v"}
        )
        assert r.score_10 == 6

    def test_grade_level_above_12_maps_to_5(self):
        r = _map_readability(
            {"estimated_grade_level": 14, "verdict": "v"}
        )
        assert r.score_10 == 5

    def test_neither_score_nor_grade_raises(self):
        with pytest.raises(EditorOutputShapeError, match="missing both"):
            _map_readability({"verdict": "v"})

    def test_grade_level_estimate_not_string(self):
        with pytest.raises(EditorOutputShapeError, match="grade_level_estimate"):
            _map_readability(
                {"score_10": 5, "grade_level_estimate": 5, "verdict": "v"}
            )

    def test_verdict_falls_back_to_overall(self):
        r = _map_readability(
            {"score_10": 5, "grade_level_estimate": "g", "overall": "ovr"}
        )
        assert r.verdict == "ovr"

    def test_no_verdict_no_overall_raises(self):
        with pytest.raises(EditorOutputShapeError, match="verdict"):
            _map_readability({"score_10": 5, "grade_level_estimate": "g"})


# ---------------------------------------------------------------------------
# _map_tone_feedback
# ---------------------------------------------------------------------------


class TestMapTone:
    def test_missing_key_message(self):
        with pytest.raises(EditorOutputShapeError, match="key_message"):
            _map_tone_feedback(
                {
                    "readability": {
                        "score_10": 5,
                        "grade_level_estimate": "g",
                        "verdict": "v",
                    }
                }
            )

    def test_fatigue_not_list(self):
        with pytest.raises(EditorOutputShapeError, match="reviewer_fatigue_sections"):
            _map_tone_feedback(
                {
                    "readability": {
                        "score_10": 5,
                        "grade_level_estimate": "g",
                        "verdict": "v",
                        "key_message": "k",
                        "reviewer_fatigue_sections": "x",
                    }
                }
            )

    def test_fatigue_entry_empty(self):
        with pytest.raises(EditorOutputShapeError, match="reviewer_fatigue_sections"):
            _map_tone_feedback(
                {
                    "readability": {
                        "score_10": 5,
                        "grade_level_estimate": "g",
                        "verdict": "v",
                        "key_message": "k",
                        "reviewer_fatigue_sections": [""],
                    }
                }
            )


# ---------------------------------------------------------------------------
# _map_gaps
# ---------------------------------------------------------------------------


class TestMapGaps:
    def test_entry_not_object(self):
        with pytest.raises(EditorOutputShapeError, match="gaps"):
            _map_gaps(["not-dict"])

    def test_section_empty(self):
        with pytest.raises(EditorOutputShapeError, match="section"):
            _map_gaps(
                [{"section": "", "issue": "y", "action_needed": "z"}]
            )

    def test_issue_empty(self):
        with pytest.raises(EditorOutputShapeError, match="issue"):
            _map_gaps(
                [{"section": "s", "issue": "", "action_needed": "z"}]
            )

    def test_action_needed_empty(self):
        with pytest.raises(EditorOutputShapeError, match="action_needed"):
            _map_gaps(
                [{"section": "s", "issue": "y", "action_needed": ""}]
            )


# ---------------------------------------------------------------------------
# _map_skill_json_to_editor_output — top-level mapper
# ---------------------------------------------------------------------------


def _minimal_valid_json() -> str:
    return json.dumps(
        {
            "readability": {
                "score_10": 7,
                "grade_level_estimate": "g",
                "verdict": "ok",
                "key_message": "k",
                "reviewer_fatigue_sections": [],
            },
            "strengths": [],
            "suggestions": [
                {
                    "section": "1.a",
                    "original": "vague",
                    "issue": "y",
                    "issue_type": "jargon",
                    "severity": "low",
                    "options": [
                        {"label": "A", "text": "a", "note": ""},
                        {"label": "B", "text": "b", "note": ""},
                    ],
                    "rubric_connection": "",
                }
            ],
            "gaps": [],
            "quick_wins": [],
            "terms_to_verify": [],
            "taxonomy_check": {},
        }
    )


class TestMapSkillJsonToEditorOutput:
    def test_quick_wins_entry_empty_raises(self):
        skill_json = json.loads(_minimal_valid_json())
        skill_json["quick_wins"] = [""]
        with pytest.raises(EditorOutputShapeError, match="quick_wins"):
            _map_skill_json_to_editor_output(skill_json)

    def test_quick_wins_entry_wrong_type(self):
        skill_json = json.loads(_minimal_valid_json())
        skill_json["quick_wins"] = [123]
        with pytest.raises(EditorOutputShapeError, match="quick_wins"):
            _map_skill_json_to_editor_output(skill_json)

    def test_terms_to_verify_entry_empty(self):
        skill_json = json.loads(_minimal_valid_json())
        skill_json["terms_to_verify"] = [""]
        with pytest.raises(EditorOutputShapeError, match="terms_to_verify"):
            _map_skill_json_to_editor_output(skill_json)

    def test_terms_to_verify_entry_wrong_type(self):
        skill_json = json.loads(_minimal_valid_json())
        skill_json["terms_to_verify"] = [42]
        with pytest.raises(EditorOutputShapeError, match="terms_to_verify"):
            _map_skill_json_to_editor_output(skill_json)

    def test_gaps_not_list(self):
        skill_json = json.loads(_minimal_valid_json())
        skill_json["gaps"] = "not list"
        with pytest.raises(EditorOutputShapeError, match="gaps must be list"):
            _map_skill_json_to_editor_output(skill_json)

    def test_suggestions_entry_not_object(self):
        skill_json = json.loads(_minimal_valid_json())
        skill_json["suggestions"] = ["not-dict"]
        with pytest.raises(EditorOutputShapeError, match="suggestions"):
            _map_skill_json_to_editor_output(skill_json)

    def test_full_set_constructs(self):
        out = _map_skill_json_to_editor_output(json.loads(_minimal_valid_json()))
        assert isinstance(out, EditorOutput)
        assert len(out.flagged_terms) == 1


# ---------------------------------------------------------------------------
# Adapter — additional happy paths and edge cases
# ---------------------------------------------------------------------------


class TestAdapterEdges:
    def test_adapter_works_without_explicit_clock(self):
        launcher = _OneShotLauncher(_minimal_valid_json())
        out = invoke_editor_adapter(_input(), skill_launcher=launcher)
        assert isinstance(out, EditorOutput)

    def test_disable_retry_skips_clarification(self):
        launcher = _OneShotLauncher("not json")
        # First (and only) attempt fails parse → raise without retry.
        with pytest.raises(Exception, match="MALFORMED-JSON"):
            invoke_editor_adapter(
                _input(),
                skill_launcher=launcher,
                clock=_clock,
                enable_retry_with_clarification=False,
            )
