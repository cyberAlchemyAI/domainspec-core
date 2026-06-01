"""§10 Red Team Round 1 — attack_memo composer + SFR emitter tests.

Covers:
- :func:`compose_red_team_verdict` — including the §10.8 computed-from-
  criteria authoritative invariant (auto-correction logged in
  ``total_score_correction``).
- :func:`assert_evidence_in_drafts` — Law 5 verbatim-substring pre-check.
- :func:`detect_council_split` — §10.6 threshold detection (boundary
  inclusive at 10).
- :func:`detect_judge_anchor_suspected` — non-blocking advisory smoke
  check.
- :func:`emit_sfr_certificate` — SFR three-block markdown emission.
- :func:`parse_recommendation_from_sfr` / :func:`parse_total_score_from_sfr` —
  R1 lightweight parser-side helpers (R3's full SFR parser lives in §6).
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from pipeline.seats.red_team.attack_memo import (
    RT_ANCHOR_SUSPECTED_THRESHOLD,
    RT_DISAGREEMENT_THRESHOLD,
    assert_evidence_in_drafts,
    compose_red_team_verdict,
    detect_council_split,
    detect_judge_anchor_suspected,
)
from pipeline.seats.red_team.sfr_emitter import (
    CONCLUSION_HEADING,
    PREMISES_HEADING,
    TRACE_HEADING,
    emit_sfr_certificate,
    parse_recommendation_from_sfr,
    parse_total_score_from_sfr,
)
from pipeline.seats.red_team.types import (
    F_RT_RECOMMENDATION_INVALID,
    F_RT_WEAKNESSES_EMPTY,
    F_RT_WEAKNESS_FIELD_MISSING,
    AttackMemo,
    RedTeamCriterionScore,
    RedTeamVerdict,
    TotalScoreCorrection,
    Weakness,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


class _FakeSectionDraft:
    def __init__(self, name: str, body: str) -> None:
        self.section_name = name
        self.section_order = 1
        self.body_text = body
        self.claim_evidence_map: tuple = ()


class _FakeJudgeVerdict:
    def __init__(self, run_id: str, rubric_hash: str) -> None:
        self.run_id = run_id
        self.rubric_hash = rubric_hash
        self.total_score = 85
        self.max_score = 100
        self.recommendation = "competitive"
        self.overall_notes = "n"


class _FakeRubric:
    def __init__(self, content_hash: str = "h" * 64) -> None:
        self.rubric_id = "vapg_fy26"
        self.content_hash = content_hash
        self.max_score = 100
        self.criteria = ()


def _ok_weakness() -> Weakness:
    return Weakness(
        severity="medium",
        claim="Paragraph 3 asserts demand without LOIs",
        why_it_fails="No buyer evidence",
        what_a_reviewer_would_say="Where are the LOIs?",
        fix_hint="Add 3 buyer LOIs",
    )


def _ok_criterion(score: int = 12) -> RedTeamCriterionScore:
    return RedTeamCriterionScore(
        criterion_id="need",
        criterion_name="Need",
        max_points=15,
        score=score,
        tier_matched="strong evidence",
        evidence="organic mango buyers exceed supply",
        missing=("LOIs",),
        notes="solid framing",
    )


def _ok_verdict(score: int = 12) -> RedTeamVerdict:
    crit = _ok_criterion(score)
    return RedTeamVerdict(
        run_id="run-1",
        rubric_id="vapg_fy26",
        rubric_hash="h" * 64,
        total_score=crit.score,
        max_score=100,
        recommendation="marginal",
        criteria=(crit,),
        attack_memo=AttackMemo(
            top_weaknesses=(_ok_weakness(),),
            unsupported_assertions=(),
            dialect_mismatches=(),
            boundary_drift=(),
            overall_verdict="Marginal feasibility with addressable gaps.",
        ),
        total_score_correction=None,
        verdict_at_utc=_utc_now(),
        red_team_dialect="conservative",
    )


# ---------------------------------------------------------------------------
# detect_council_split
# ---------------------------------------------------------------------------


class TestDetectCouncilSplit:
    def test_threshold_exactly_10_inclusive(self) -> None:
        assert detect_council_split(judge_total_score=85, red_team_total_score=75) is True

    def test_below_threshold_9(self) -> None:
        assert detect_council_split(judge_total_score=85, red_team_total_score=76) is False

    def test_above_threshold(self) -> None:
        assert detect_council_split(judge_total_score=90, red_team_total_score=70) is True

    def test_symmetric(self) -> None:
        # |75 - 85| == |85 - 75|
        assert detect_council_split(judge_total_score=75, red_team_total_score=85) is True

    def test_exact_match(self) -> None:
        assert detect_council_split(judge_total_score=85, red_team_total_score=85) is False

    def test_custom_threshold(self) -> None:
        assert detect_council_split(judge_total_score=85, red_team_total_score=80, threshold=5) is True
        assert detect_council_split(judge_total_score=85, red_team_total_score=81, threshold=5) is False

    def test_default_threshold_canonical(self) -> None:
        assert RT_DISAGREEMENT_THRESHOLD == 10

    def test_negative_judge_score_rejected(self) -> None:
        with pytest.raises(ValueError, match="judge_total_score"):
            detect_council_split(judge_total_score=-1, red_team_total_score=70)

    def test_negative_red_team_score_rejected(self) -> None:
        with pytest.raises(ValueError, match="red_team_total_score"):
            detect_council_split(judge_total_score=85, red_team_total_score=-1)

    def test_negative_threshold_rejected(self) -> None:
        with pytest.raises(ValueError, match="threshold"):
            detect_council_split(judge_total_score=85, red_team_total_score=70, threshold=-1)

    def test_zero_threshold_means_any_disagreement_splits(self) -> None:
        # threshold=0: any non-zero delta splits
        assert detect_council_split(judge_total_score=85, red_team_total_score=84, threshold=0) is True
        assert detect_council_split(judge_total_score=85, red_team_total_score=85, threshold=0) is True


# ---------------------------------------------------------------------------
# detect_judge_anchor_suspected
# ---------------------------------------------------------------------------


class TestDetectJudgeAnchorSuspected:
    def test_advisory_threshold_canonical(self) -> None:
        assert RT_ANCHOR_SUSPECTED_THRESHOLD == 2

    def test_close_agreement_on_non_trivial_draft_fires(self) -> None:
        assert (
            detect_judge_anchor_suspected(
                judge_total_score=85,
                red_team_total_score=86,
                rubric_criteria_count=7,
                total_words=1500,
            )
            is True
        )

    def test_exact_match_on_non_trivial_draft_fires(self) -> None:
        assert (
            detect_judge_anchor_suspected(
                judge_total_score=85,
                red_team_total_score=85,
                rubric_criteria_count=7,
                total_words=1500,
            )
            is True
        )

    def test_disagreement_above_advisory_does_not_fire(self) -> None:
        assert (
            detect_judge_anchor_suspected(
                judge_total_score=85,
                red_team_total_score=83,  # delta exactly 2; not "<"
                rubric_criteria_count=7,
                total_words=1500,
            )
            is False
        )

    def test_short_draft_does_not_fire(self) -> None:
        assert (
            detect_judge_anchor_suspected(
                judge_total_score=85,
                red_team_total_score=85,
                rubric_criteria_count=7,
                total_words=500,  # below threshold
            )
            is False
        )

    def test_few_criteria_does_not_fire(self) -> None:
        assert (
            detect_judge_anchor_suspected(
                judge_total_score=85,
                red_team_total_score=85,
                rubric_criteria_count=4,  # below threshold
                total_words=1500,
            )
            is False
        )

    def test_advisory_at_boundary_5_criteria_1000_words(self) -> None:
        assert (
            detect_judge_anchor_suspected(
                judge_total_score=85,
                red_team_total_score=86,
                rubric_criteria_count=5,
                total_words=1000,
            )
            is True
        )


# ---------------------------------------------------------------------------
# compose_red_team_verdict
# ---------------------------------------------------------------------------


class TestComposeRedTeamVerdict:
    def _input_bundle(self):
        return type(
            "FakeInput",
            (),
            {
                "run_id": "run-1",
                "section_drafts": (_FakeSectionDraft("p", "body"),),
                "claim_evidence_map": (),
                "rubric": _FakeRubric(),
                "judge_verdict": None,
                "funder_dialect": "conservative",
                "admin_risk_register_snapshot": object(),
                "prepared_at_utc": _utc_now(),
            },
        )()

    def _model_output(self, *, total: int = 12, criterion_score: int = 12) -> dict:
        return {
            "total_score": total,
            "recommendation": "marginal",
            "criteria": [
                {
                    "id": "need",
                    "name": "Need",
                    "max_points": 15,
                    "score": criterion_score,
                    "tier_matched": "strong evidence",
                    "evidence": "organic mango buyers exceed supply",
                    "missing": ["LOIs"],
                    "notes": "solid",
                }
            ],
            "attack_memo": {
                "top_weaknesses": [
                    {
                        "severity": "high",
                        "claim": "claim text",
                        "why_it_fails": "why",
                        "what_a_reviewer_would_say": "what",
                        "fix_hint": "fix",
                    }
                ],
                "unsupported_assertions": [],
                "dialect_mismatches": [],
                "boundary_drift": [],
                "overall_verdict": "marginal feasibility",
            },
        }

    def test_constructs_canonical_verdict(self) -> None:
        out = compose_red_team_verdict(
            parsed_model_output=self._model_output(),
            input_bundle=self._input_bundle(),
            rubric_max_points_by_id={"need": 15},
            rubric_max_score=100,
        )
        assert out.total_score == 12
        assert out.recommendation == "marginal"
        assert out.total_score_correction is None

    def test_auto_correction_when_model_total_disagrees(self) -> None:
        mo = self._model_output(total=99, criterion_score=12)
        out = compose_red_team_verdict(
            parsed_model_output=mo,
            input_bundle=self._input_bundle(),
            rubric_max_points_by_id={"need": 15},
            rubric_max_score=100,
        )
        # Authoritative = sum of criteria = 12
        assert out.total_score == 12
        assert out.total_score_correction is not None
        assert out.total_score_correction.model_reported == 99
        assert out.total_score_correction.computed_from_criteria == 12
        assert out.total_score_correction.delta == -87

    def test_invalid_recommendation_raises(self) -> None:
        mo = self._model_output()
        mo["recommendation"] = "reject"
        with pytest.raises(ValueError, match=F_RT_RECOMMENDATION_INVALID):
            compose_red_team_verdict(
                parsed_model_output=mo,
                input_bundle=self._input_bundle(),
                rubric_max_points_by_id={"need": 15},
                rubric_max_score=100,
            )

    def test_empty_top_weaknesses_raises(self) -> None:
        mo = self._model_output()
        mo["attack_memo"]["top_weaknesses"] = []
        with pytest.raises(ValueError, match=F_RT_WEAKNESSES_EMPTY):
            compose_red_team_verdict(
                parsed_model_output=mo,
                input_bundle=self._input_bundle(),
                rubric_max_points_by_id={"need": 15},
                rubric_max_score=100,
            )

    def test_missing_weakness_field_raises(self) -> None:
        mo = self._model_output()
        del mo["attack_memo"]["top_weaknesses"][0]["fix_hint"]
        with pytest.raises(ValueError, match=F_RT_WEAKNESS_FIELD_MISSING):
            compose_red_team_verdict(
                parsed_model_output=mo,
                input_bundle=self._input_bundle(),
                rubric_max_points_by_id={"need": 15},
                rubric_max_score=100,
            )

    def test_max_points_fallback_from_rubric(self) -> None:
        mo = self._model_output()
        del mo["criteria"][0]["max_points"]
        out = compose_red_team_verdict(
            parsed_model_output=mo,
            input_bundle=self._input_bundle(),
            rubric_max_points_by_id={"need": 15},
            rubric_max_score=100,
        )
        assert out.criteria[0].max_points == 15

    def test_max_points_missing_in_both_raises(self) -> None:
        mo = self._model_output()
        del mo["criteria"][0]["max_points"]
        with pytest.raises(ValueError, match="max_points"):
            compose_red_team_verdict(
                parsed_model_output=mo,
                input_bundle=self._input_bundle(),
                rubric_max_points_by_id={},  # no fallback
                rubric_max_score=100,
            )

    def test_criterion_id_missing_raises(self) -> None:
        mo = self._model_output()
        del mo["criteria"][0]["id"]
        with pytest.raises(ValueError, match="id"):
            compose_red_team_verdict(
                parsed_model_output=mo,
                input_bundle=self._input_bundle(),
                rubric_max_points_by_id={"need": 15},
                rubric_max_score=100,
            )

    def test_red_team_dialect_passes_through(self) -> None:
        out = compose_red_team_verdict(
            parsed_model_output=self._model_output(),
            input_bundle=self._input_bundle(),
            rubric_max_points_by_id={"need": 15},
            rubric_max_score=100,
            red_team_dialect="centrist",
        )
        assert out.red_team_dialect == "centrist"


# ---------------------------------------------------------------------------
# assert_evidence_in_drafts
# ---------------------------------------------------------------------------


class TestAssertEvidenceInDrafts:
    def test_pass_clean_evidence(self) -> None:
        draft_body = (
            "organic mango buyers exceed supply in the region. "
            "Paragraph 3 asserts demand without LOIs as central risk."
        )
        v = _ok_verdict()
        violations = assert_evidence_in_drafts(
            verdict=v, drafts=(_FakeSectionDraft("p", draft_body),)
        )
        assert violations == ()

    def test_fail_paraphrased_evidence(self) -> None:
        # Paraphrased — Red Team's evidence not in draft
        draft_body = "Mango buyers in the region exceed local supply."
        v = _ok_verdict()  # Red Team evidence is "organic mango buyers exceed supply"
        violations = assert_evidence_in_drafts(
            verdict=v, drafts=(_FakeSectionDraft("p", draft_body),)
        )
        assert len(violations) > 0
        assert any("F-RT-EVIDENCE-NOT-IN-DRAFT" in v_ for v_ in violations)

    def test_fail_weakness_claim_paraphrased(self) -> None:
        # Evidence in draft but weakness claim paraphrased
        draft_body = "organic mango buyers exceed supply in the region."
        crit = _ok_criterion()
        memo = AttackMemo(
            top_weaknesses=(
                Weakness(
                    severity="high",
                    claim="WRONG QUOTE NOT IN DRAFT",
                    why_it_fails="x",
                    what_a_reviewer_would_say="y",
                    fix_hint="z",
                ),
            ),
            unsupported_assertions=(),
            dialect_mismatches=(),
            boundary_drift=(),
            overall_verdict="ok",
        )
        v = RedTeamVerdict(
            run_id="r",
            rubric_id="vapg",
            rubric_hash="h" * 64,
            total_score=crit.score,
            max_score=100,
            recommendation="marginal",
            criteria=(crit,),
            attack_memo=memo,
            total_score_correction=None,
            verdict_at_utc=_utc_now(),
            red_team_dialect="conservative",
        )
        violations = assert_evidence_in_drafts(
            verdict=v, drafts=(_FakeSectionDraft("p", draft_body),)
        )
        assert any("top_weaknesses[0].claim" in v_ for v_ in violations)

    def test_fail_unsupported_assertion_paraphrased(self) -> None:
        draft_body = "organic mango buyers exceed supply in the region."
        crit = _ok_criterion()
        memo = AttackMemo(
            top_weaknesses=(_ok_weakness(),),
            unsupported_assertions=("NOT IN DRAFT TEXT",),
            dialect_mismatches=(),
            boundary_drift=(),
            overall_verdict="ok",
        )
        # Need to add weakness claim into body too
        body_with_weakness = draft_body + " " + memo.top_weaknesses[0].claim
        v = RedTeamVerdict(
            run_id="r",
            rubric_id="vapg",
            rubric_hash="h" * 64,
            total_score=crit.score,
            max_score=100,
            recommendation="marginal",
            criteria=(crit,),
            attack_memo=memo,
            total_score_correction=None,
            verdict_at_utc=_utc_now(),
            red_team_dialect="conservative",
        )
        violations = assert_evidence_in_drafts(
            verdict=v, drafts=(_FakeSectionDraft("p", body_with_weakness),)
        )
        assert any("unsupported_assertions[0]" in v_ for v_ in violations)


# ---------------------------------------------------------------------------
# emit_sfr_certificate + helpers
# ---------------------------------------------------------------------------


class TestEmitSfrCertificate:
    def test_emits_three_blocks(self) -> None:
        v = _ok_verdict()
        sfr = emit_sfr_certificate(verdict=v)
        assert PREMISES_HEADING in sfr
        assert TRACE_HEADING in sfr
        assert CONCLUSION_HEADING in sfr

    def test_premises_block_first(self) -> None:
        v = _ok_verdict()
        sfr = emit_sfr_certificate(verdict=v)
        # Order: Premises → Trace → Conclusion
        assert sfr.index(PREMISES_HEADING) < sfr.index(TRACE_HEADING) < sfr.index(CONCLUSION_HEADING)

    def test_block_headings_are_canonical(self) -> None:
        assert PREMISES_HEADING == "## Premises"
        assert TRACE_HEADING == "## Execution trace"
        assert CONCLUSION_HEADING == "## Conclusion"

    def test_recommendation_in_conclusion(self) -> None:
        v = _ok_verdict()
        sfr = emit_sfr_certificate(verdict=v)
        rec = parse_recommendation_from_sfr(sfr)
        assert rec == "marginal"

    def test_total_score_in_conclusion(self) -> None:
        v = _ok_verdict(score=12)
        sfr = emit_sfr_certificate(verdict=v)
        ts = parse_total_score_from_sfr(sfr)
        assert ts == (12, 100)

    def test_premises_two_per_criterion(self) -> None:
        v = _ok_verdict()
        sfr = emit_sfr_certificate(verdict=v)
        # 1 criterion → 2 premises (rubric + evidence) + 1 weakness → 1 more = 3 total
        # Count "- P" lines
        p_lines = [line for line in sfr.splitlines() if line.startswith("- P")]
        assert len(p_lines) == 3

    def test_steps_one_per_criterion_plus_one_per_weakness(self) -> None:
        v = _ok_verdict()
        sfr = emit_sfr_certificate(verdict=v)
        t_lines = [line for line in sfr.splitlines() if line.startswith("- T")]
        # 1 criterion-step + 1 weakness-step = 2
        assert len(t_lines) == 2

    def test_overall_verdict_in_conclusion(self) -> None:
        v = _ok_verdict()
        sfr = emit_sfr_certificate(verdict=v)
        assert "overall_verdict:" in sfr
        assert "Marginal feasibility" in sfr

    def test_residuals_listed_in_conclusion(self) -> None:
        v = _ok_verdict()
        sfr = emit_sfr_certificate(verdict=v)
        assert "residuals:" in sfr
        assert "[medium]" in sfr  # weakness severity surfaces

    def test_section_pointer_hint_used(self) -> None:
        v = _ok_verdict()
        sfr = emit_sfr_certificate(
            verdict=v,
            section_pointer_hint="DRAFT:project_description:p3:abc1234",
        )
        assert "DRAFT:project_description:p3:abc1234" in sfr

    def test_default_section_pointer_when_none(self) -> None:
        v = _ok_verdict()
        sfr = emit_sfr_certificate(verdict=v)
        # Default uses section_unknown
        assert "DRAFT:section_unknown" in sfr


class TestParseHelpers:
    def test_parse_recommendation_from_sfr_ok(self) -> None:
        sfr = "## Premises\n\n- P1: x\n\n## Execution trace\n\n- T1: (P1) → ok\n\n## Conclusion\n\nrecommendation: competitive\ntotal_score: 90/100\n"
        assert parse_recommendation_from_sfr(sfr) == "competitive"

    def test_parse_recommendation_missing(self) -> None:
        sfr = "## Premises\n\n- P1: x\n"
        assert parse_recommendation_from_sfr(sfr) is None

    def test_parse_total_score_from_sfr_ok(self) -> None:
        sfr = "## Conclusion\n\ntotal_score: 75/100\n"
        assert parse_total_score_from_sfr(sfr) == (75, 100)

    def test_parse_total_score_missing(self) -> None:
        sfr = "## Conclusion\n\nrecommendation: marginal\n"
        assert parse_total_score_from_sfr(sfr) is None

    def test_parse_total_score_malformed_no_slash(self) -> None:
        sfr = "## Conclusion\n\ntotal_score: 75-100\n"
        assert parse_total_score_from_sfr(sfr) is None

    def test_parse_total_score_malformed_non_int(self) -> None:
        sfr = "## Conclusion\n\ntotal_score: high/perfect\n"
        assert parse_total_score_from_sfr(sfr) is None


# ---------------------------------------------------------------------------
# SFR roundtrip: compose verdict → emit SFR → parse back
# ---------------------------------------------------------------------------


class TestSfrRoundtrip:
    def test_recommendation_survives_roundtrip(self) -> None:
        v = _ok_verdict()
        sfr = emit_sfr_certificate(verdict=v)
        assert parse_recommendation_from_sfr(sfr) == v.recommendation

    def test_total_score_survives_roundtrip(self) -> None:
        v = _ok_verdict(score=8)
        sfr = emit_sfr_certificate(verdict=v)
        assert parse_total_score_from_sfr(sfr) == (8, 100)

    def test_steps_reference_premises(self) -> None:
        # Every step line should reference at least one premise (Pn) — checked
        # for the canonical emit path (parser-level rejection of floating-step
        # is in §6 SFR parser, not this emitter).
        v = _ok_verdict()
        sfr = emit_sfr_certificate(verdict=v)
        for line in sfr.splitlines():
            if line.startswith("- T"):
                assert "P" in line  # at least one P-ref

    def test_conclusion_recommendation_in_closed_set(self) -> None:
        # Round-trip the recommendation and verify it parses back to a value
        # in the closed Literal set.
        from pipeline.seats.red_team.types import _RT_RECOMMENDATIONS

        v = _ok_verdict()
        sfr = emit_sfr_certificate(verdict=v)
        rec = parse_recommendation_from_sfr(sfr)
        assert rec in _RT_RECOMMENDATIONS
