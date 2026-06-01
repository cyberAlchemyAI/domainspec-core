"""Tests for pipeline.seats.judge.dimension_scorer.

Covers:
- Happy path scoring at criterion-level (criterion b, no subcriteria).
- Happy path scoring at subcriterion-level (criterion a.i, max 10).
- LLM out-of-bound score → F_JUDGE_SCORE_OUT_OF_BOUND.
- Unparseable LLM output → F_JUDGE_SCORE_UNPARSEABLE.
- Confidence out-of-bound → F_JUDGE_SCORE_UNPARSEABLE (caught before
  CriterionScore __post_init__).
- LLM raises → propagates (timeouts, transport errors not swallowed).
- Empty section_drafts → ValueError.
- Must-address checklist appears in compiled prompt.
- Clock invocation honored.
- JSON-fenced output unwrapped.
- Extra fields in LLM JSON ignored.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import pytest

from pipeline.seats.judge.dimension_scorer import score_dimension
from pipeline.seats.judge.types import (
    CriterionScore,
    F_JUDGE_SCORE_OUT_OF_BOUND,
    F_JUDGE_SCORE_UNPARSEABLE,
    RubricCriterion,
    RubricSubCriterion,
)


UTC_NOW = datetime(2026, 4, 29, 12, 0, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


class _FakeSectionDraft:
    def __init__(self, name: str, order: int, body: str):
        self.section_name = name
        self.section_order = order
        self.body_text = body
        self.claim_evidence_map: tuple = ()


def _make_llm(response: str):
    captured: dict[str, Any] = {}

    def _call(*, prompt: str, max_tokens: int) -> str:
        captured["prompt"] = prompt
        captured["max_tokens"] = max_tokens
        return response

    return _call, captured


def _crit_b() -> RubricCriterion:
    return RubricCriterion(
        id="b",
        name="Qualifications of Key Personnel",
        max_points=20,
        scorer="review_panel",
        subcriteria=(),
        must_address=(
            "All Key Personnel identified",
            "Qualifications and expertise",
        ),
        tiers=(
            {"points": 0, "description": "Does not address"},
            {"points": "10-14", "description": "Reasonable likelihood"},
        ),
    )


def _sub_a_i() -> RubricSubCriterion:
    return RubricSubCriterion(
        id="a.i",
        name="Technological feasibility",
        max_points=10,
        must_address=("Process description",),
        tiers=({"points": 8, "description": "HIGH likelihood"},),
    )


# ---------------------------------------------------------------------------
# Happy paths
# ---------------------------------------------------------------------------


class TestHappyPath:
    def test_criterion_level_scoring(self):
        draft = _FakeSectionDraft(
            "Qualifications", 1, "Lead investigator has 15 years of experience."
        )
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 18,
                    "evidence_quote": "Lead investigator has 15 years",
                    "confidence": 0.9,
                    "rationale": "Strong qualifications signal",
                }
            )
        )
        cs = score_dimension(
            (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
        )
        assert isinstance(cs, CriterionScore)
        assert cs.criterion_id == "b"
        assert cs.score == 18
        assert cs.confidence == 0.9
        assert "Lead investigator" in cs.evidence_quote

    def test_subcriterion_level_scoring(self):
        draft = _FakeSectionDraft("Tech", 1, "We use solid-state fermentation.")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 8,
                    "evidence_quote": "solid-state fermentation",
                    "confidence": 0.75,
                    "rationale": "Process narrative present",
                }
            )
        )
        cs = score_dimension(
            (draft,), _sub_a_i(), llm_call=llm, clock=lambda: UTC_NOW
        )
        assert cs.criterion_id == "a.i"
        assert cs.score == 8

    def test_zero_score_accepted(self):
        draft = _FakeSectionDraft("S", 1, "absent")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 0,
                    "evidence_quote": "absent",
                    "confidence": 1.0,
                    "rationale": "Does not address criterion",
                }
            )
        )
        cs = score_dimension(
            (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
        )
        assert cs.score == 0

    def test_score_at_max_points_accepted(self):
        draft = _FakeSectionDraft("S", 1, "perfect")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 20,
                    "evidence_quote": "perfect",
                    "confidence": 0.99,
                    "rationale": "All criteria met",
                }
            )
        )
        cs = score_dimension(
            (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
        )
        assert cs.score == 20

    def test_multiple_drafts_in_prompt(self):
        d1 = _FakeSectionDraft("Qualifications", 1, "Lead has 15 years.")
        d2 = _FakeSectionDraft("Personnel", 2, "Co-lead has 10 years.")
        llm, captured = _make_llm(
            json.dumps(
                {
                    "score": 17,
                    "evidence_quote": "Lead has 15 years.",
                    "confidence": 0.85,
                    "rationale": "Strong both",
                }
            )
        )
        score_dimension(
            (d1, d2), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
        )
        assert "Lead has 15 years." in captured["prompt"]
        assert "Co-lead has 10 years." in captured["prompt"]
        assert "Section 1" in captured["prompt"]
        assert "Section 2" in captured["prompt"]

    def test_must_address_in_prompt(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, captured = _make_llm(
            json.dumps(
                {
                    "score": 10,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        score_dimension(
            (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
        )
        assert "All Key Personnel identified" in captured["prompt"]
        assert "Qualifications and expertise" in captured["prompt"]

    def test_must_address_empty_renders_none(self):
        crit = RubricCriterion(
            id="x",
            name="X",
            max_points=10,
            scorer="review_panel",
            subcriteria=(),
            must_address=(),
            tiers=({"points": 5, "description": "ok"},),
        )
        draft = _FakeSectionDraft("S", 1, "body")
        llm, captured = _make_llm(
            json.dumps(
                {
                    "score": 5,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        score_dimension((draft,), crit, llm_call=llm, clock=lambda: UTC_NOW)
        assert "(none)" in captured["prompt"]

    def test_tiers_empty_renders_marker(self):
        # Subcriterion with no tiers — score guidance via parent.
        sub = RubricSubCriterion(
            id="x.i",
            name="Sub",
            max_points=10,
            must_address=("foo",),
            tiers=(),
        )
        draft = _FakeSectionDraft("S", 1, "body")
        llm, captured = _make_llm(
            json.dumps(
                {
                    "score": 5,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        score_dimension((draft,), sub, llm_call=llm, clock=lambda: UTC_NOW)
        assert "score guidance via parent criterion" in captured["prompt"]

    def test_max_tokens_passed_through(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, captured = _make_llm(
            json.dumps(
                {
                    "score": 5,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        score_dimension(
            (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW, max_tokens=512
        )
        assert captured["max_tokens"] == 512

    def test_default_max_tokens(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, captured = _make_llm(
            json.dumps(
                {
                    "score": 5,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        score_dimension(
            (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
        )
        assert captured["max_tokens"] == 1024

    def test_clock_invoked(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 5,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        ticks: list[datetime] = []

        def _clock() -> datetime:
            ticks.append(UTC_NOW)
            return UTC_NOW

        score_dimension((draft,), _crit_b(), llm_call=llm, clock=_clock)
        assert ticks == [UTC_NOW]

    def test_default_clock_invocation(self):
        # Without a clock kwarg, the default tz-aware UTC clock fires once.
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 5,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        cs = score_dimension((draft,), _crit_b(), llm_call=llm)
        assert cs.criterion_id == "b"

    def test_int_confidence_coerced_to_float(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 10,
                    "evidence_quote": "body",
                    "confidence": 1,
                    "rationale": "ok",
                }
            )
        )
        cs = score_dimension(
            (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
        )
        assert cs.confidence == 1.0
        assert isinstance(cs.confidence, float)

    def test_extra_fields_silently_ignored(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 10,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                    "override_max_points": 999,
                    "secret_admin_field": "ignore-me",
                }
            )
        )
        cs = score_dimension(
            (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
        )
        # Extra fields not surfaced on CriterionScore.
        assert not hasattr(cs, "override_max_points")
        assert not hasattr(cs, "secret_admin_field")

    def test_json_with_fenced_block_unwrapped(self):
        draft = _FakeSectionDraft("S", 1, "body")
        fenced = (
            "```json\n"
            + json.dumps(
                {
                    "score": 7,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
            + "\n```"
        )
        llm, _ = _make_llm(fenced)
        cs = score_dimension(
            (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
        )
        assert cs.score == 7

    def test_bare_triple_backtick_fence_unwrapped(self):
        draft = _FakeSectionDraft("S", 1, "body")
        fenced = (
            "```\n"
            + json.dumps(
                {
                    "score": 6,
                    "evidence_quote": "body",
                    "confidence": 0.4,
                    "rationale": "ok",
                }
            )
            + "\n```"
        )
        llm, _ = _make_llm(fenced)
        cs = score_dimension(
            (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
        )
        assert cs.score == 6


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------


class TestFailureModes:
    def test_empty_drafts_rejected(self):
        llm, _ = _make_llm("{}")
        with pytest.raises(ValueError, match="section_drafts must be non-empty"):
            score_dimension((), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW)

    def test_unparseable_llm_output(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm("not even close to JSON")
        with pytest.raises(ValueError, match=F_JUDGE_SCORE_UNPARSEABLE):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_top_level_array_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm("[1, 2, 3]")
        with pytest.raises(ValueError, match="top level must be"):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_score_above_max_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        # crit b max=20; LLM returns 25.
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 25,
                    "evidence_quote": "body",
                    "confidence": 0.9,
                    "rationale": "ok",
                }
            )
        )
        with pytest.raises(ValueError, match=F_JUDGE_SCORE_OUT_OF_BOUND):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_score_below_zero_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": -3,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        with pytest.raises(ValueError, match=F_JUDGE_SCORE_OUT_OF_BOUND):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_score_above_subcriterion_max_rejected(self):
        # a.i max=10; LLM returns 15.
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 15,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        with pytest.raises(ValueError, match=F_JUDGE_SCORE_OUT_OF_BOUND):
            score_dimension(
                (draft,), _sub_a_i(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_confidence_above_one_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 5,
                    "evidence_quote": "body",
                    "confidence": 1.5,
                    "rationale": "ok",
                }
            )
        )
        with pytest.raises(ValueError, match=F_JUDGE_SCORE_UNPARSEABLE):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_confidence_below_zero_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 5,
                    "evidence_quote": "body",
                    "confidence": -0.1,
                    "rationale": "ok",
                }
            )
        )
        with pytest.raises(ValueError, match=F_JUDGE_SCORE_UNPARSEABLE):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_score_missing_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        with pytest.raises(ValueError, match="score"):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_score_string_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": "high",
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        with pytest.raises(ValueError, match="score.*must be an int"):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_score_bool_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": True,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
        )
        with pytest.raises(ValueError, match="score.*must be an int"):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_evidence_quote_missing_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps({"score": 5, "confidence": 0.5, "rationale": "ok"})
        )
        with pytest.raises(ValueError, match="evidence_quote"):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_rationale_missing_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {"score": 5, "evidence_quote": "body", "confidence": 0.5}
            )
        )
        with pytest.raises(ValueError, match="rationale"):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_confidence_missing_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {"score": 5, "evidence_quote": "body", "rationale": "ok"}
            )
        )
        with pytest.raises(ValueError, match="confidence"):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_confidence_string_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 5,
                    "evidence_quote": "body",
                    "confidence": "high",
                    "rationale": "ok",
                }
            )
        )
        with pytest.raises(ValueError, match="confidence.*must be a number"):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_confidence_bool_rejected(self):
        draft = _FakeSectionDraft("S", 1, "body")
        llm, _ = _make_llm(
            json.dumps(
                {
                    "score": 5,
                    "evidence_quote": "body",
                    "confidence": True,
                    "rationale": "ok",
                }
            )
        )
        with pytest.raises(ValueError, match="confidence.*must be a number"):
            score_dimension(
                (draft,), _crit_b(), llm_call=llm, clock=lambda: UTC_NOW
            )

    def test_llm_raises_propagates(self):
        draft = _FakeSectionDraft("S", 1, "body")

        def _raising_llm(*, prompt: str, max_tokens: int) -> str:
            raise RuntimeError("transport timeout")

        with pytest.raises(RuntimeError, match="transport timeout"):
            score_dimension(
                (draft,),
                _crit_b(),
                llm_call=_raising_llm,
                clock=lambda: UTC_NOW,
            )

    def test_llm_returns_non_str_propagates_via_parser(self):
        # If a misbehaving llm returns something json.loads can't decode
        # (binary, None) it should surface as F_JUDGE_SCORE_UNPARSEABLE.
        draft = _FakeSectionDraft("S", 1, "body")

        def _bad_llm(*, prompt: str, max_tokens: int) -> str:
            return ""

        with pytest.raises(ValueError, match=F_JUDGE_SCORE_UNPARSEABLE):
            score_dimension(
                (draft,), _crit_b(), llm_call=_bad_llm, clock=lambda: UTC_NOW
            )
