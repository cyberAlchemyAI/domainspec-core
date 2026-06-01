"""Tests for §9 R2 verdict assembler.

Spec card: ``pipeline/engineering/spec_cards/section_09_judge_round_2_cross_rubric_and_verdict.md``.

Test surface (per spec card §6):

- Valid assembly under criterion-level coverage.
- Valid assembly under subcriterion-level coverage.
- Partial sub-coverage → F-JUDGE-CRITERION-MISSING.
- Mixed parent + sub coverage on same criterion → F-JUDGE-CRITERION-MISSING.
- Out-of-bound score → F-JUDGE-SCORE-OUT-OF-BOUND.
- Rubric hash drift between load and assembly → F-JUDGE-RUBRIC-HASH-DRIFT.
- Evidence not in any draft → F-JUDGE-EVIDENCE-NOT-IN-DRAFT.
- Empty / whitespace evidence rejected.
- Empty inputs (criterion_scores / section_drafts) rejected.
- Duplicate criterion_id in scores rejected.
- Score id absent from rubric rejected.
- Total / max_total computation under both coverage modes.
- assembled_at_utc populated by injected clock.
- VAPG full round-trip with realistic per-subcriterion coverage.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from pipeline.seats.judge.responsiveness_mapper import (
    build_responsiveness_map,
    extract_responsiveness_factors_from_rubric_json,
)
from pipeline.seats.judge.rubric_loader import load_rubric
from pipeline.seats.judge.types import (
    CriterionScore,
    JudgeVerdict,
    ResponsivenessMap,
    Rubric,
    RubricCriterion,
    RubricSubCriterion,
    SectionDraftLike,
)
from pipeline.seats.judge.verdict_assembler import assemble_verdict


UTC = timezone.utc
SCORED_AT = datetime(2026, 4, 29, 12, 0, 0, tzinfo=UTC)
ASSEMBLED_AT = datetime(2026, 4, 29, 12, 0, 1, tzinfo=UTC)
SHA256_VALID = "0" * 64
SHA3_512_VALID = "0" * 128
VAPG_RUBRIC_PATH = (
    Path(__file__).resolve().parents[3]
    / "pipeline"
    / "rubrics"
    / "vapg_fy26.json"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _StubDraft:
    section_name: str
    section_order: int
    body_text: str
    claim_evidence_map: tuple = ()


def _draft(body: str = "Quote-A. Quote-B. Quote-C.", *, name: str = "Sec", order: int = 1) -> SectionDraftLike:
    return _StubDraft(
        section_name=name,
        section_order=order,
        body_text=body,
        claim_evidence_map=(),
    )


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
        name="X",
        max_points=10,
        scorer="review_panel",
        subcriteria=(),
        must_address=(),
        tiers=({"points": 5, "description": "ok"},),
    )
    kw.update(overrides)
    return RubricCriterion(**kw)


def _rubric(criteria: tuple[RubricCriterion, ...], **overrides) -> Rubric:
    sum_max = sum(c.max_points for c in criteria)
    kw = dict(
        program_code="TEST-FY26",
        funder="Test",
        nofo_number="TEST-001",
        max_score=max(sum_max, 1),
        min_score=0,
        criteria=criteria,
        rubric_sha256=SHA256_VALID,
        loaded_at_utc=SCORED_AT,
    )
    kw.update(overrides)
    return Rubric(**kw)


def _stub_clock(at: datetime = ASSEMBLED_AT):
    return lambda: at


EMPTY_RM = ResponsivenessMap(entries=())


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


class TestHappyPath:
    def test_criterion_level_coverage_assembles(self):
        rubric = _rubric(
            (
                _crit(id="b", max_points=20),
                _crit(id="c", max_points=20),
            )
        )
        scores = (
            CriterionScore(
                criterion_id="b",
                score=15,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
            CriterionScore(
                criterion_id="c",
                score=12,
                evidence_quote="Quote-B",
                confidence=0.8,
                rationale="ok",
            ),
        )
        v = assemble_verdict(
            scores,
            rubric=rubric,
            section_drafts=(_draft(),),
            rfa_content_sha3_512=SHA3_512_VALID,
            responsiveness_map=EMPTY_RM,
            rubric_sha256_at_score_time=SHA256_VALID,
            scored_at_utc=SCORED_AT,
            clock=_stub_clock(),
        )
        assert isinstance(v, JudgeVerdict)
        assert v.judge_output.total_score == 27
        assert v.judge_output.max_total == 40
        assert v.rubric_program_code == "TEST-FY26"
        assert v.assembled_at_utc == ASSEMBLED_AT

    def test_subcriterion_level_coverage_assembles(self):
        sub_a = _sub(id="a.i", max_points=10)
        sub_b = _sub(id="a.ii", max_points=10)
        crit = _crit(
            id="a",
            scorer="review_panel",
            max_points=20,
            subcriteria=(sub_a, sub_b),
            tiers=(),
        )
        rubric = _rubric((crit,), max_score=20)
        scores = (
            CriterionScore(
                criterion_id="a.i",
                score=8,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
            CriterionScore(
                criterion_id="a.ii",
                score=7,
                evidence_quote="Quote-B",
                confidence=0.85,
                rationale="ok",
            ),
        )
        v = assemble_verdict(
            scores,
            rubric=rubric,
            section_drafts=(_draft(),),
            rfa_content_sha3_512=SHA3_512_VALID,
            responsiveness_map=EMPTY_RM,
            rubric_sha256_at_score_time=SHA256_VALID,
            scored_at_utc=SCORED_AT,
            clock=_stub_clock(),
        )
        assert v.judge_output.total_score == 15
        assert v.judge_output.max_total == 20

    def test_scored_at_carried_into_judge_output(self):
        rubric = _rubric((_crit(id="b", max_points=20),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=10,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        v = assemble_verdict(
            scores,
            rubric=rubric,
            section_drafts=(_draft(),),
            rfa_content_sha3_512=SHA3_512_VALID,
            responsiveness_map=EMPTY_RM,
            rubric_sha256_at_score_time=SHA256_VALID,
            scored_at_utc=SCORED_AT,
            clock=_stub_clock(),
        )
        assert v.judge_output.scored_at_utc == SCORED_AT

    def test_default_clock_used_when_unspecified(self):
        rubric = _rubric((_crit(id="b", max_points=20),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=10,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        before = datetime.now(tz=UTC)
        v = assemble_verdict(
            scores,
            rubric=rubric,
            section_drafts=(_draft(),),
            rfa_content_sha3_512=SHA3_512_VALID,
            responsiveness_map=EMPTY_RM,
            rubric_sha256_at_score_time=SHA256_VALID,
            scored_at_utc=SCORED_AT,
        )
        after = datetime.now(tz=UTC)
        assert before <= v.assembled_at_utc <= after

    def test_evidence_in_second_draft_accepted(self):
        rubric = _rubric((_crit(id="b", max_points=20),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=10,
                evidence_quote="ONLY_IN_SECOND",
                confidence=0.9,
                rationale="ok",
            ),
        )
        drafts = (
            _draft(body="totally unrelated", name="A", order=1),
            _draft(body="contains ONLY_IN_SECOND yes", name="B", order=2),
        )
        v = assemble_verdict(
            scores,
            rubric=rubric,
            section_drafts=drafts,
            rfa_content_sha3_512=SHA3_512_VALID,
            responsiveness_map=EMPTY_RM,
            rubric_sha256_at_score_time=SHA256_VALID,
            scored_at_utc=SCORED_AT,
            clock=_stub_clock(),
        )
        assert v.judge_output.criterion_scores[0].evidence_quote == (
            "ONLY_IN_SECOND"
        )

    def test_responsiveness_map_carried_through(self):
        from pipeline.seats.judge.types import ResponsivenessEntry

        rubric = _rubric((_crit(id="g", scorer="administrator", max_points=10),))
        rmap = ResponsivenessMap(
            entries=(
                ResponsivenessEntry(
                    criterion_id="g",
                    factor_name="categories",
                    factor_values=("Geographic diversity",),
                ),
            )
        )
        scores = (
            CriterionScore(
                criterion_id="g",
                score=5,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        v = assemble_verdict(
            scores,
            rubric=rubric,
            section_drafts=(_draft(),),
            rfa_content_sha3_512=SHA3_512_VALID,
            responsiveness_map=rmap,
            rubric_sha256_at_score_time=SHA256_VALID,
            scored_at_utc=SCORED_AT,
            clock=_stub_clock(),
        )
        assert v.responsiveness_map is rmap


# ---------------------------------------------------------------------------
# Empty inputs
# ---------------------------------------------------------------------------


class TestEmptyInputs:
    def test_empty_criterion_scores_rejected(self):
        rubric = _rubric((_crit(id="b", max_points=20),))
        with pytest.raises(
            ValueError, match="criterion_scores must be non-empty"
        ):
            assemble_verdict(
                (),
                rubric=rubric,
                section_drafts=(_draft(),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )

    def test_empty_section_drafts_rejected(self):
        rubric = _rubric((_crit(id="b", max_points=20),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=10,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError, match="section_drafts must be non-empty"
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )


# ---------------------------------------------------------------------------
# Coverage failures
# ---------------------------------------------------------------------------


class TestCoverageFailures:
    def test_unknown_score_id_rejected(self):
        rubric = _rubric((_crit(id="b", max_points=20),))
        scores = (
            CriterionScore(
                criterion_id="ghost",
                score=10,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError, match="F-JUDGE-CRITERION-MISSING"
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(_draft(),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )

    def test_duplicate_criterion_id_rejected(self):
        rubric = _rubric((_crit(id="b", max_points=20),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=10,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
            CriterionScore(
                criterion_id="b",
                score=15,
                evidence_quote="Quote-B",
                confidence=0.8,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError, match="duplicate.*criterion_id"
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(_draft(),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )

    def test_uncovered_criterion_rejected(self):
        rubric = _rubric(
            (
                _crit(id="b", max_points=20),
                _crit(id="c", max_points=20),
            )
        )
        scores = (
            CriterionScore(
                criterion_id="b",
                score=10,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError,
            match=(
                r"criterion 'c' has no subcriteria and no CriterionScore "
                r"for the criterion id"
            ),
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(_draft(),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )

    def test_uncovered_subcriteria_bearing_criterion_rejected(self):
        # Criterion has subs, but none of them appear in scores AND
        # the parent id doesn't appear either — this hits the "is
        # uncovered" message, distinct from the no-subcriteria case.
        sub_a = _sub(id="a.i", max_points=10)
        crit_a = _crit(
            id="a",
            scorer="review_panel",
            max_points=10,
            subcriteria=(sub_a,),
            tiers=(),
        )
        crit_b = _crit(id="b", max_points=10)
        rubric = _rubric((crit_a, crit_b), max_score=20)
        scores = (
            CriterionScore(
                criterion_id="b",
                score=5,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError, match="criterion 'a' is uncovered"
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(_draft(),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )

    def test_partial_sub_coverage_rejected(self):
        sub_a = _sub(id="a.i", max_points=10)
        sub_b = _sub(id="a.ii", max_points=10)
        crit = _crit(
            id="a",
            scorer="review_panel",
            max_points=20,
            subcriteria=(sub_a, sub_b),
            tiers=(),
        )
        rubric = _rubric((crit,), max_score=20)
        scores = (
            CriterionScore(
                criterion_id="a.i",
                score=8,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError,
            match="partial subcriterion coverage; missing: \\('a.ii',\\)",
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(_draft(),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )

    def test_mixed_parent_and_sub_coverage_rejected(self):
        sub_a = _sub(id="a.i", max_points=10)
        crit = _crit(
            id="a",
            scorer="review_panel",
            max_points=10,
            subcriteria=(sub_a,),
            tiers=(),
        )
        rubric = _rubric((crit,), max_score=10)
        scores = (
            CriterionScore(
                criterion_id="a",
                score=8,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
            CriterionScore(
                criterion_id="a.i",
                score=5,
                evidence_quote="Quote-B",
                confidence=0.9,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError,
            match="covered both at parent level AND at subcriterion level",
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(_draft(),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )

    def test_single_score_for_multi_sub_criterion_under_parent_id_accepted(self):
        # This is the parent-coverage path even when subs exist —
        # legitimate (some rubrics may want a single rolled-up score
        # rather than per-sub LLM calls).
        sub_a = _sub(id="a.i", max_points=10)
        sub_b = _sub(id="a.ii", max_points=10)
        crit = _crit(
            id="a",
            scorer="review_panel",
            max_points=20,
            subcriteria=(sub_a, sub_b),
            tiers=(),
        )
        rubric = _rubric((crit,), max_score=20)
        scores = (
            CriterionScore(
                criterion_id="a",
                score=18,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        v = assemble_verdict(
            scores,
            rubric=rubric,
            section_drafts=(_draft(),),
            rfa_content_sha3_512=SHA3_512_VALID,
            responsiveness_map=EMPTY_RM,
            rubric_sha256_at_score_time=SHA256_VALID,
            scored_at_utc=SCORED_AT,
            clock=_stub_clock(),
        )
        # When parent-covered, max_total contribution is parent.max_points (20).
        assert v.judge_output.max_total == 20
        assert v.judge_output.total_score == 18


# ---------------------------------------------------------------------------
# Score-bound failures
# ---------------------------------------------------------------------------


class TestScoreBoundFailures:
    def test_score_above_unit_max_rejected(self):
        rubric = _rubric((_crit(id="b", max_points=10),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=11,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError, match="F-JUDGE-SCORE-OUT-OF-BOUND"
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(_draft(),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )

    def test_score_at_unit_max_accepted(self):
        rubric = _rubric((_crit(id="b", max_points=10),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=10,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        v = assemble_verdict(
            scores,
            rubric=rubric,
            section_drafts=(_draft(),),
            rfa_content_sha3_512=SHA3_512_VALID,
            responsiveness_map=EMPTY_RM,
            rubric_sha256_at_score_time=SHA256_VALID,
            scored_at_utc=SCORED_AT,
            clock=_stub_clock(),
        )
        assert v.judge_output.total_score == 10

    def test_score_zero_accepted(self):
        rubric = _rubric((_crit(id="b", max_points=10),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=0,
                evidence_quote="Quote-A",
                confidence=0.5,
                rationale="ok",
            ),
        )
        v = assemble_verdict(
            scores,
            rubric=rubric,
            section_drafts=(_draft(),),
            rfa_content_sha3_512=SHA3_512_VALID,
            responsiveness_map=EMPTY_RM,
            rubric_sha256_at_score_time=SHA256_VALID,
            scored_at_utc=SCORED_AT,
            clock=_stub_clock(),
        )
        assert v.judge_output.total_score == 0


# ---------------------------------------------------------------------------
# Hash drift
# ---------------------------------------------------------------------------


class TestHashDrift:
    def test_drift_between_load_and_assembly_rejected(self):
        rubric = _rubric((_crit(id="b", max_points=10),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=8,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError, match="F-JUDGE-RUBRIC-HASH-DRIFT"
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(_draft(),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time="f" * 64,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )


# ---------------------------------------------------------------------------
# Evidence-in-draft (Law 5 pre-check)
# ---------------------------------------------------------------------------


class TestEvidenceInDraft:
    def test_evidence_not_in_any_draft_rejected(self):
        rubric = _rubric((_crit(id="b", max_points=10),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=8,
                evidence_quote="THIS_NEVER_APPEARS",
                confidence=0.9,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError, match="F-JUDGE-EVIDENCE-NOT-IN-DRAFT"
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(_draft(body="Other content here"),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )

    def test_empty_evidence_quote_rejected(self):
        rubric = _rubric((_crit(id="b", max_points=10),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=8,
                evidence_quote=" ",
                confidence=0.9,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError,
            match="evidence_quote is empty or whitespace-only",
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(_draft(),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )

    def test_partial_quote_match_rejected(self):
        rubric = _rubric((_crit(id="b", max_points=10),))
        # Quote requires verbatim full substring match.
        scores = (
            CriterionScore(
                criterion_id="b",
                score=8,
                evidence_quote="Quote-A and Quote-D",
                confidence=0.9,
                rationale="ok",
            ),
        )
        with pytest.raises(
            ValueError, match="F-JUDGE-EVIDENCE-NOT-IN-DRAFT"
        ):
            assemble_verdict(
                scores,
                rubric=rubric,
                section_drafts=(_draft(body="Quote-A. Quote-B."),),
                rfa_content_sha3_512=SHA3_512_VALID,
                responsiveness_map=EMPTY_RM,
                rubric_sha256_at_score_time=SHA256_VALID,
                scored_at_utc=SCORED_AT,
                clock=_stub_clock(),
            )


# ---------------------------------------------------------------------------
# VAPG full round-trip
# ---------------------------------------------------------------------------


class TestVapgRoundTrip:
    def test_full_subcriterion_coverage_roundtrip(self):
        rubric = load_rubric(VAPG_RUBRIC_PATH, clock=lambda: SCORED_AT)
        # Build a section draft whose body_text contains every quote we'll
        # use; the loader uses the rubric_sha256 we'll receive.
        body = "EVID:" + ":".join(f"q-{u}" for u in "abcdefg")
        body += " a.i a.ii a.iii f.i f.ii"
        drafts = (_draft(body=body),)

        # Per-sub coverage where present, per-crit coverage where not.
        scores: list[CriterionScore] = []
        for crit in rubric.criteria:
            if crit.subcriteria:
                for sub in crit.subcriteria:
                    scores.append(
                        CriterionScore(
                            criterion_id=sub.id,
                            score=sub.max_points,
                            evidence_quote=sub.id,
                            confidence=0.9,
                            rationale="ok",
                        )
                    )
            else:
                scores.append(
                    CriterionScore(
                        criterion_id=crit.id,
                        score=min(crit.max_points, 5),
                        evidence_quote=f"q-{crit.id}",
                        confidence=0.9,
                        rationale="ok",
                    )
                )
        # We need to make sure every evidence_quote appears verbatim.
        # Augment body with the per-sub ids and per-crit q-{id} markers.
        body_full = (
            "a.i a.ii a.iii f.i f.ii q-a q-b q-c q-d q-e q-f q-g"
        )
        drafts = (_draft(body=body_full),)

        rubric_json_extras = extract_responsiveness_factors_from_rubric_json(
            __import__("json").loads(VAPG_RUBRIC_PATH.read_text())
        )
        rmap = build_responsiveness_map(
            rubric, criterion_extras=rubric_json_extras
        )
        v = assemble_verdict(
            tuple(scores),
            rubric=rubric,
            section_drafts=drafts,
            rfa_content_sha3_512=SHA3_512_VALID,
            responsiveness_map=rmap,
            rubric_sha256_at_score_time=rubric.rubric_sha256,
            scored_at_utc=SCORED_AT,
            clock=_stub_clock(),
        )
        # max_total should equal the rubric max_score (full coverage).
        assert v.judge_output.max_total == rubric.max_score
        assert v.rubric_program_code == rubric.program_code
        # 4 responsiveness entries (f.i + f.ii×2 + g) per the mapper test.
        assert len(v.responsiveness_map.entries) == 4

    def test_assembled_at_after_scored_at(self):
        rubric = _rubric((_crit(id="b", max_points=10),))
        scores = (
            CriterionScore(
                criterion_id="b",
                score=5,
                evidence_quote="Quote-A",
                confidence=0.9,
                rationale="ok",
            ),
        )
        later = SCORED_AT + timedelta(seconds=10)
        v = assemble_verdict(
            scores,
            rubric=rubric,
            section_drafts=(_draft(),),
            rfa_content_sha3_512=SHA3_512_VALID,
            responsiveness_map=EMPTY_RM,
            rubric_sha256_at_score_time=SHA256_VALID,
            scored_at_utc=SCORED_AT,
            clock=_stub_clock(later),
        )
        assert v.assembled_at_utc == later
