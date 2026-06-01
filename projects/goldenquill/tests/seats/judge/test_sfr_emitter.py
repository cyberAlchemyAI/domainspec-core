"""Round-3 tests for ``pipeline.seats.judge.sfr_emitter``.

Covers the three-block SFR (Premises / Execution / Conclusion) emission,
:class:`SfrLineItem` + :class:`SfrReport` invariants, the
``_resolve_unit_max_points`` rubric walker, and the
``render_sfr_text`` line-oriented renderer.
"""
from __future__ import annotations

from datetime import datetime, timezone
from types import MappingProxyType

import pytest

from pipeline.seats.judge.sfr_emitter import (
    SFR_BLOCK_NAMES,
    SfrLineItem,
    SfrReport,
    emit_sfr,
    render_sfr_text,
)
from pipeline.seats.judge.types import (
    CriterionScore,
    JudgeOutput,
    JudgeVerdict,
    ResponsivenessMap,
    Rubric,
    RubricCriterion,
    RubricSubCriterion,
)


_FIXED_NOW = datetime(2026, 4, 30, 12, 0, tzinfo=timezone.utc)
_RFA_HASH = "b" * 128
_RUBRIC_HASH = "c" * 64


def _build_rubric_with_subs() -> Rubric:
    sub_a = RubricSubCriterion(
        id="a.i",
        name="Tech feasibility",
        max_points=10,
        must_address=("feasibility",),
        tiers=(),
    )
    sub_b = RubricSubCriterion(
        id="a.ii",
        name="Operational efficiency",
        max_points=10,
        must_address=("efficiency",),
        tiers=(),
    )
    crit_a = RubricCriterion(
        id="a",
        name="Venture",
        max_points=20,
        scorer="review_panel",
        subcriteria=(sub_a, sub_b),
        must_address=(),
        tiers=(),
    )
    crit_b = RubricCriterion(
        id="b",
        name="Personnel",
        max_points=20,
        scorer="review_panel",
        subcriteria=(),
        must_address=("qualifications",),
        tiers=(MappingProxyType({"points": 20, "description": "Strong"}),),
    )
    return Rubric(
        program_code="VAPG",
        funder="USDA RD",
        nofo_number="USDA-RBCS-VAPG-2026",
        max_score=100,
        min_score=50,
        criteria=(crit_a, crit_b),
        rubric_sha256=_RUBRIC_HASH,
        loaded_at_utc=_FIXED_NOW,
    )


class _FakeDraft:
    def __init__(self, body: str) -> None:
        self.section_name = "Project Narrative"
        self.section_order = 1
        self.body_text = body
        self.claim_evidence_map: tuple = ()


def _build_verdict(rubric: Rubric, scores: tuple[CriterionScore, ...]) -> JudgeVerdict:
    total_score = sum(s.score for s in scores)
    # max_total = sum of unit max for the scored ids only.
    by_id: dict[str, int] = {}
    for crit in rubric.criteria:
        by_id[crit.id] = crit.max_points
        for sub in crit.subcriteria:
            by_id[sub.id] = sub.max_points
    max_total = sum(by_id[s.criterion_id] for s in scores)
    jo = JudgeOutput(
        criterion_scores=scores,
        total_score=total_score,
        max_total=max_total,
        rubric_sha256=rubric.rubric_sha256,
        rfa_content_sha3_512=_RFA_HASH,
        scored_at_utc=_FIXED_NOW,
    )
    return JudgeVerdict(
        judge_output=jo,
        rubric_program_code=rubric.program_code,
        responsiveness_map=ResponsivenessMap(entries=()),
        assembled_at_utc=_FIXED_NOW,
    )


# ---------------------------------------------------------------------------
# Block-name constant
# ---------------------------------------------------------------------------


class TestBlockNames:
    def test_three_blocks_in_canonical_order(self):
        assert SFR_BLOCK_NAMES == ("Premises", "Execution", "Conclusion")

    def test_block_names_are_strings(self):
        for n in SFR_BLOCK_NAMES:
            assert isinstance(n, str) and n.strip()


# ---------------------------------------------------------------------------
# SfrLineItem invariants
# ---------------------------------------------------------------------------


class TestSfrLineItem:
    def test_happy_path(self):
        li = SfrLineItem(
            criterion_id="b",
            score=15,
            max_points=20,
            confidence=0.9,
            evidence_quote="quote",
            rationale="r",
        )
        assert li.score == 15

    def test_blank_criterion_id_rejected(self):
        with pytest.raises(ValueError, match="criterion_id"):
            SfrLineItem(
                criterion_id="   ",
                score=10,
                max_points=20,
                confidence=0.5,
                evidence_quote="q",
                rationale="r",
            )

    def test_negative_score_rejected(self):
        with pytest.raises(ValueError, match="score"):
            SfrLineItem(
                criterion_id="b",
                score=-1,
                max_points=20,
                confidence=0.5,
                evidence_quote="q",
                rationale="r",
            )

    def test_negative_max_points_rejected(self):
        with pytest.raises(ValueError, match="max_points"):
            SfrLineItem(
                criterion_id="b",
                score=0,
                max_points=-1,
                confidence=0.5,
                evidence_quote="q",
                rationale="r",
            )

    def test_score_above_max_rejected(self):
        with pytest.raises(ValueError, match="max_points"):
            SfrLineItem(
                criterion_id="b",
                score=21,
                max_points=20,
                confidence=0.5,
                evidence_quote="q",
                rationale="r",
            )

    def test_confidence_below_zero_rejected(self):
        with pytest.raises(ValueError, match="confidence"):
            SfrLineItem(
                criterion_id="b",
                score=0,
                max_points=20,
                confidence=-0.1,
                evidence_quote="q",
                rationale="r",
            )

    def test_confidence_above_one_rejected(self):
        with pytest.raises(ValueError, match="confidence"):
            SfrLineItem(
                criterion_id="b",
                score=0,
                max_points=20,
                confidence=1.1,
                evidence_quote="q",
                rationale="r",
            )


# ---------------------------------------------------------------------------
# SfrReport invariants
# ---------------------------------------------------------------------------


class TestSfrReportInvariants:
    def _make_report(self, **overrides):
        line = SfrLineItem(
            criterion_id="b",
            score=18,
            max_points=20,
            confidence=0.9,
            evidence_quote="q",
            rationale="r",
        )
        kw = {
            "program_code": "VAPG",
            "funder": "USDA",
            "nofo_number": "X",
            "rubric_sha256": _RUBRIC_HASH,
            "rfa_scope_summary": "scope",
            "line_items": (line,),
            "total_score": 18,
            "max_total": 20,
            "percent_score": 18 / 20,
            "pass_threshold": 50,
            "passed": False,
            "mean_confidence": 0.9,
        }
        kw.update(overrides)
        return SfrReport(**kw)

    def test_happy_path(self):
        r = self._make_report()
        assert r.passed is False

    def test_blank_program_rejected(self):
        with pytest.raises(ValueError, match="program_code"):
            self._make_report(program_code="  ")

    def test_blank_funder_rejected(self):
        with pytest.raises(ValueError, match="funder"):
            self._make_report(funder="")

    def test_blank_nofo_rejected(self):
        with pytest.raises(ValueError, match="nofo_number"):
            self._make_report(nofo_number=" ")

    def test_short_rubric_sha_rejected(self):
        with pytest.raises(ValueError, match="rubric_sha256"):
            self._make_report(rubric_sha256="abc")

    def test_uppercase_rubric_sha_rejected(self):
        with pytest.raises(ValueError, match="rubric_sha256"):
            self._make_report(rubric_sha256="A" * 64)

    def test_blank_rfa_scope_rejected(self):
        with pytest.raises(ValueError, match="rfa_scope_summary"):
            self._make_report(rfa_scope_summary="  ")

    def test_empty_line_items_rejected(self):
        with pytest.raises(ValueError, match="line_items"):
            self._make_report(line_items=())

    def test_total_score_drift_rejected(self):
        with pytest.raises(ValueError, match="total_score"):
            self._make_report(total_score=10)  # actual sum is 18

    def test_max_total_drift_rejected(self):
        with pytest.raises(ValueError, match="max_total"):
            self._make_report(max_total=10)  # actual sum is 20

    def test_negative_threshold_rejected(self):
        with pytest.raises(ValueError, match="pass_threshold"):
            self._make_report(pass_threshold=-1)

    def test_percent_score_drift_rejected(self):
        with pytest.raises(ValueError, match="percent_score"):
            self._make_report(percent_score=0.5)  # actual is 0.9

    def test_passed_flag_drift_rejected(self):
        with pytest.raises(ValueError, match="passed"):
            self._make_report(passed=True)  # actual 18 < 50

    def test_mean_confidence_drift_rejected(self):
        with pytest.raises(ValueError, match="mean_confidence"):
            self._make_report(mean_confidence=0.5)

    def test_zero_max_total_forces_zero_pct(self):
        line = SfrLineItem(
            criterion_id="x",
            score=0,
            max_points=0,
            confidence=0.5,
            evidence_quote="q",
            rationale="r",
        )
        r = SfrReport(
            program_code="VAPG",
            funder="USDA",
            nofo_number="X",
            rubric_sha256=_RUBRIC_HASH,
            rfa_scope_summary="scope",
            line_items=(line,),
            total_score=0,
            max_total=0,
            percent_score=0.0,
            pass_threshold=0,
            passed=True,
            mean_confidence=0.5,
        )
        assert r.percent_score == 0.0
        assert r.passed is True


# ---------------------------------------------------------------------------
# emit_sfr
# ---------------------------------------------------------------------------


class TestEmitSfr:
    def test_happy_path_parent_only(self):
        rubric = _build_rubric_with_subs()
        cs_a = CriterionScore(
            criterion_id="a",
            score=15,
            evidence_quote="venture text",
            confidence=0.9,
            rationale="r",
        )
        cs_b = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="personnel text",
            confidence=0.95,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs_a, cs_b))
        report = emit_sfr(
            judge_verdict=verdict,
            rubric=rubric,
            section_drafts=(_FakeDraft("venture text personnel text"),),
            rfa_scope_summary="scope summary",
        )
        assert report.total_score == 33
        assert report.max_total == 40
        assert report.pass_threshold == 50  # default = rubric.min_score
        assert report.passed is False
        assert len(report.line_items) == 2

    def test_subcriteria_path(self):
        rubric = _build_rubric_with_subs()
        cs_a_i = CriterionScore(
            criterion_id="a.i",
            score=8,
            evidence_quote="feasibility text",
            confidence=0.8,
            rationale="r",
        )
        cs_a_ii = CriterionScore(
            criterion_id="a.ii",
            score=9,
            evidence_quote="efficiency text",
            confidence=0.9,
            rationale="r",
        )
        cs_b = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="personnel text",
            confidence=1.0,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs_a_i, cs_a_ii, cs_b))
        report = emit_sfr(
            judge_verdict=verdict,
            rubric=rubric,
            section_drafts=(_FakeDraft("feasibility text efficiency text personnel text"),),
            rfa_scope_summary="scope",
        )
        # Subcriterion max_points (10+10) + parent b max_points (20) = 40
        assert report.max_total == 40
        line_a_i = next(li for li in report.line_items if li.criterion_id == "a.i")
        assert line_a_i.max_points == 10

    def test_passed_flag_true_when_above_threshold(self):
        rubric = _build_rubric_with_subs()
        cs_a = CriterionScore(
            criterion_id="a",
            score=20,
            evidence_quote="x",
            confidence=1.0,
            rationale="",
        )
        cs_b = CriterionScore(
            criterion_id="b",
            score=20,
            evidence_quote="x",
            confidence=1.0,
            rationale="",
        )
        verdict = _build_verdict(rubric, (cs_a, cs_b))
        report = emit_sfr(
            judge_verdict=verdict,
            rubric=rubric,
            section_drafts=(_FakeDraft("x"),),
            rfa_scope_summary="scope",
            pass_threshold=30,
        )
        assert report.passed is True

    def test_program_code_drift_rejected(self):
        rubric = _build_rubric_with_subs()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="text",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,))
        # Construct a rubric with same shape but different program_code.
        crit_b = RubricCriterion(
            id="b",
            name="Personnel",
            max_points=20,
            scorer="review_panel",
            subcriteria=(),
            must_address=("qualifications",),
            tiers=(MappingProxyType({"points": 20, "description": "Strong"}),),
        )
        other_rubric = Rubric(
            program_code="OTHER",
            funder="X",
            nofo_number="Y",
            max_score=100,
            min_score=50,
            criteria=(crit_b,),
            rubric_sha256=_RUBRIC_HASH,
            loaded_at_utc=_FIXED_NOW,
        )
        with pytest.raises(ValueError, match="program_code"):
            emit_sfr(
                judge_verdict=verdict,
                rubric=other_rubric,
                section_drafts=(_FakeDraft("text"),),
                rfa_scope_summary="scope",
            )

    def test_rubric_sha_drift_rejected(self):
        rubric = _build_rubric_with_subs()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="text",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,))
        # Construct same-shape rubric with different sha.
        crit_b = RubricCriterion(
            id="b",
            name="Personnel",
            max_points=20,
            scorer="review_panel",
            subcriteria=(),
            must_address=("qualifications",),
            tiers=(MappingProxyType({"points": 20, "description": "Strong"}),),
        )
        other_rubric = Rubric(
            program_code="VAPG",
            funder="X",
            nofo_number="Y",
            max_score=100,
            min_score=50,
            criteria=(crit_b,),
            rubric_sha256="d" * 64,
            loaded_at_utc=_FIXED_NOW,
        )
        with pytest.raises(ValueError, match="rubric_sha256"):
            emit_sfr(
                judge_verdict=verdict,
                rubric=other_rubric,
                section_drafts=(_FakeDraft("text"),),
                rfa_scope_summary="scope",
            )

    def test_empty_drafts_rejected(self):
        rubric = _build_rubric_with_subs()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="text",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,))
        with pytest.raises(ValueError, match="section_drafts"):
            emit_sfr(
                judge_verdict=verdict,
                rubric=rubric,
                section_drafts=(),
                rfa_scope_summary="scope",
            )

    def test_empty_scope_summary_rejected(self):
        rubric = _build_rubric_with_subs()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="text",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,))
        with pytest.raises(ValueError, match="rfa_scope_summary"):
            emit_sfr(
                judge_verdict=verdict,
                rubric=rubric,
                section_drafts=(_FakeDraft("text"),),
                rfa_scope_summary="   ",
            )

    def test_negative_pass_threshold_rejected(self):
        rubric = _build_rubric_with_subs()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="text",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,))
        with pytest.raises(ValueError, match="pass_threshold"):
            emit_sfr(
                judge_verdict=verdict,
                rubric=rubric,
                section_drafts=(_FakeDraft("text"),),
                rfa_scope_summary="scope",
                pass_threshold=-1,
            )

    def test_unknown_criterion_id_rejected(self):
        rubric = _build_rubric_with_subs()
        # CriterionScore claims a criterion_id not in the rubric.
        cs = CriterionScore(
            criterion_id="zzzz",
            score=10,
            evidence_quote="text",
            confidence=0.9,
            rationale="r",
        )
        # Manually build a verdict that bypasses verdict_assembler's coverage
        # walker (this simulates a corrupted upstream).
        jo = JudgeOutput(
            criterion_scores=(cs,),
            total_score=10,
            max_total=10,
            rubric_sha256=rubric.rubric_sha256,
            rfa_content_sha3_512=_RFA_HASH,
            scored_at_utc=_FIXED_NOW,
        )
        verdict = JudgeVerdict(
            judge_output=jo,
            rubric_program_code=rubric.program_code,
            responsiveness_map=ResponsivenessMap(entries=()),
            assembled_at_utc=_FIXED_NOW,
        )
        with pytest.raises(ValueError, match="zzzz"):
            emit_sfr(
                judge_verdict=verdict,
                rubric=rubric,
                section_drafts=(_FakeDraft("text"),),
                rfa_scope_summary="scope",
            )

    def test_scope_summary_is_stripped(self):
        rubric = _build_rubric_with_subs()
        cs = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="text",
            confidence=0.9,
            rationale="r",
        )
        verdict = _build_verdict(rubric, (cs,))
        report = emit_sfr(
            judge_verdict=verdict,
            rubric=rubric,
            section_drafts=(_FakeDraft("text"),),
            rfa_scope_summary="   scope-with-padding   ",
        )
        assert report.rfa_scope_summary == "scope-with-padding"


# ---------------------------------------------------------------------------
# render_sfr_text
# ---------------------------------------------------------------------------


class TestRenderSfrText:
    def _build_two_line_report(self) -> SfrReport:
        rubric = _build_rubric_with_subs()
        cs_a = CriterionScore(
            criterion_id="a",
            score=15,
            evidence_quote="venture text",
            confidence=0.9,
            rationale="rationale-a",
        )
        cs_b = CriterionScore(
            criterion_id="b",
            score=18,
            evidence_quote="personnel text",
            confidence=0.95,
            rationale="rationale-b",
        )
        verdict = _build_verdict(rubric, (cs_a, cs_b))
        return emit_sfr(
            judge_verdict=verdict,
            rubric=rubric,
            section_drafts=(_FakeDraft("venture text personnel text"),),
            rfa_scope_summary="scope summary",
        )

    def test_three_blocks_present(self):
        report = self._build_two_line_report()
        text = render_sfr_text(report)
        assert "# Premises" in text
        assert "# Execution" in text
        assert "# Conclusion" in text

    def test_premises_block_carries_rubric_metadata(self):
        report = self._build_two_line_report()
        text = render_sfr_text(report)
        assert "VAPG" in text
        assert "USDA RD" in text
        assert "USDA-RBCS-VAPG-2026" in text
        assert _RUBRIC_HASH in text
        assert "scope summary" in text

    def test_execution_block_has_score_table(self):
        report = self._build_two_line_report()
        text = render_sfr_text(report)
        assert "| Criterion | Score | Max | Confidence |" in text
        assert "| a | 15 | 20 |" in text
        assert "| b | 18 | 20 |" in text

    def test_execution_block_has_evidence_quotes(self):
        report = self._build_two_line_report()
        text = render_sfr_text(report)
        assert "venture text" in text
        assert "personnel text" in text
        assert "rationale-a" in text
        assert "rationale-b" in text

    def test_conclusion_block_has_total_and_pass(self):
        report = self._build_two_line_report()
        text = render_sfr_text(report)
        assert "Total: 33 / 40" in text
        assert "Pass threshold: 50" in text
        assert "Passed: False" in text

    def test_no_markdown_fences(self):
        report = self._build_two_line_report()
        text = render_sfr_text(report)
        assert "```" not in text

    def test_deterministic_repeated_calls(self):
        report = self._build_two_line_report()
        a = render_sfr_text(report)
        b = render_sfr_text(report)
        assert a == b

    def test_block_headers_use_canonical_names(self):
        report = self._build_two_line_report()
        text = render_sfr_text(report)
        for block in SFR_BLOCK_NAMES:
            assert f"# {block}" in text

    def test_percent_score_rendered(self):
        report = self._build_two_line_report()
        text = render_sfr_text(report)
        # 33/40 = 82.5%
        assert "82.5%" in text
