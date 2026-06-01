"""§10 Red Team Round 1 — types module tests.

Spec card: ``pipeline/blueprint/v0.1/section_10_red_team.md`` (§10 v1
SCOPING DRAFT) + ``pipeline/blueprint/v0.1/section_05_v7_amendment.md``
(CouncilSplitDecision shape).

Coverage targets:
- Frozen-dataclass invariants on every shape (slots+frozen + kw_only).
- Construction-time invariants (closed-set Literal checks, length caps,
  range checks, computed-from-criteria invariant).
- Forward-Protocol structural conformance.
- Failure-code string constants present + correctly-formatted.
- V1 inline-literal module-load asserts on closed-set frozensets +
  length-cap constants.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from pipeline.seats.red_team.types import (
    F_COUNCIL_SPLIT,
    F_RT_EVIDENCE_NOT_IN_DRAFT,
    F_RT_FAMILY_OVERLAP,
    F_RT_INPUT_INCONSISTENT,
    F_RT_INPUT_MISSING,
    F_RT_JUDGE_ANCHOR_SUSPECTED,
    F_RT_VERDICT_CERT_MALFORMED,
    F_RT_WEAKNESSES_EMPTY,
    F_RT_WEAKNESS_FIELD_MISSING,
    MAX_EVIDENCE_CHARS,
    MAX_NOTES_CHARS,
    MAX_OPERATOR_RATIONALE_CHARS,
    MAX_OVERALL_VERDICT_CHARS,
    MAX_TOP_WEAKNESSES,
    MAX_WEAKNESS_FIELD_CHARS,
    MIN_TOP_WEAKNESSES,
    AttackMemo,
    ClaimEvidenceLike,
    CouncilSplitDecision,
    JudgeVerdictLike,
    RedTeamCriterionScore,
    RedTeamInput,
    RedTeamVerdict,
    RubricLike,
    SectionDraftLike,
    TotalScoreCorrection,
    Weakness,
    _COUNCIL_SPLIT_DECISIONS,
    _RT_DIALECTS,
    _RT_RECOMMENDATIONS,
    _WEAKNESS_SEVERITIES,
)


# ---------------------------------------------------------------------------
# Helpers — minimal valid fixtures
# ---------------------------------------------------------------------------


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _ok_weakness(severity: str = "high") -> Weakness:
    return Weakness(
        severity=severity,  # type: ignore[arg-type]
        claim="Paragraph 3 asserts market demand",
        why_it_fails="No buyer interviews cited",
        what_a_reviewer_would_say="Where is the demand evidence?",
        fix_hint="Add 3 buyer LOIs to capacity section",
    )


def _ok_attack_memo() -> AttackMemo:
    return AttackMemo(
        top_weaknesses=(_ok_weakness("high"),),
        unsupported_assertions=("8 years operating",),
        dialect_mismatches=("market efficiency",),
        boundary_drift=("scope creep into Phase 2",),
        overall_verdict="Marginal feasibility with addressable gaps.",
    )


def _ok_criterion(score: int = 12, max_points: int = 15) -> RedTeamCriterionScore:
    return RedTeamCriterionScore(
        criterion_id="need",
        criterion_name="Need",
        max_points=max_points,
        score=score,
        tier_matched="strong evidence of unmet market need",
        evidence="organic mango buyers in tri-county region exceed supply",
        missing=("comparable products analysis",),
        notes="Solid framing; need quantitative buyer LOIs.",
    )


def _ok_verdict(
    *, total_score: int | None = None, criteria: tuple[RedTeamCriterionScore, ...] | None = None
) -> RedTeamVerdict:
    if criteria is None:
        criteria = (_ok_criterion(),)
    if total_score is None:
        total_score = sum(c.score for c in criteria)
    return RedTeamVerdict(
        run_id="run-abc-123",
        rubric_id="vapg_fy26",
        rubric_hash="0" * 64,
        total_score=total_score,
        max_score=100,
        recommendation="marginal",
        criteria=criteria,
        attack_memo=_ok_attack_memo(),
        total_score_correction=None,
        verdict_at_utc=_utc_now(),
        red_team_dialect="conservative",
    )


# ---------------------------------------------------------------------------
# Closed-set frozenset module-load asserts (V1 inline-literal)
# ---------------------------------------------------------------------------


class TestClosedSetFrozensets:
    def test_weakness_severities_canonical(self) -> None:
        assert _WEAKNESS_SEVERITIES == frozenset({"high", "medium", "low"})

    def test_recommendations_canonical(self) -> None:
        assert _RT_RECOMMENDATIONS == frozenset({"competitive", "marginal", "not_ready"})

    def test_dialects_canonical(self) -> None:
        assert _RT_DIALECTS == frozenset(
            {"conservative", "centrist", "progressive", "soul_fire"}
        )

    def test_council_split_decisions_canonical(self) -> None:
        assert _COUNCIL_SPLIT_DECISIONS == frozenset(
            {"proceed_with_judge", "proceed_with_red_team", "revise", "drop"}
        )

    def test_length_caps_canonical(self) -> None:
        assert MAX_EVIDENCE_CHARS == 320
        assert MAX_NOTES_CHARS == 480
        assert MAX_OVERALL_VERDICT_CHARS == 480
        assert MAX_WEAKNESS_FIELD_CHARS == 320
        assert MAX_TOP_WEAKNESSES == 5
        assert MIN_TOP_WEAKNESSES == 1
        assert MAX_OPERATOR_RATIONALE_CHARS == 480


# ---------------------------------------------------------------------------
# Failure-code string constants
# ---------------------------------------------------------------------------


class TestFailureCodes:
    def test_council_split_canonical(self) -> None:
        assert F_COUNCIL_SPLIT == "F-COUNCIL-SPLIT"

    def test_rt_input_missing(self) -> None:
        assert F_RT_INPUT_MISSING == "F-RT-INPUT-MISSING"

    def test_rt_input_inconsistent(self) -> None:
        assert F_RT_INPUT_INCONSISTENT == "F-RT-INPUT-INCONSISTENT"

    def test_rt_evidence_not_in_draft(self) -> None:
        assert F_RT_EVIDENCE_NOT_IN_DRAFT == "F-RT-EVIDENCE-NOT-IN-DRAFT"

    def test_rt_family_overlap(self) -> None:
        assert F_RT_FAMILY_OVERLAP == "F-RT-FAMILY-OVERLAP"

    def test_rt_judge_anchor_suspected(self) -> None:
        assert F_RT_JUDGE_ANCHOR_SUSPECTED == "F-RT-JUDGE-ANCHOR-SUSPECTED"

    def test_rt_verdict_cert_malformed(self) -> None:
        assert F_RT_VERDICT_CERT_MALFORMED == "F-RT-VERDICT-CERT-MALFORMED"

    def test_rt_weaknesses_empty(self) -> None:
        assert F_RT_WEAKNESSES_EMPTY == "F-RT-WEAKNESSES-EMPTY"

    def test_rt_weakness_field_missing(self) -> None:
        assert F_RT_WEAKNESS_FIELD_MISSING == "F-RT-WEAKNESS-FIELD-MISSING"


# ---------------------------------------------------------------------------
# Weakness shape
# ---------------------------------------------------------------------------


class TestWeaknessShape:
    def test_constructs_with_required_fields(self) -> None:
        w = _ok_weakness()
        assert w.severity == "high"
        assert w.claim == "Paragraph 3 asserts market demand"

    def test_invalid_severity_rejected(self) -> None:
        with pytest.raises(ValueError, match="severity"):
            Weakness(
                severity="critical",  # type: ignore[arg-type]
                claim="x",
                why_it_fails="y",
                what_a_reviewer_would_say="z",
                fix_hint="w",
            )

    def test_empty_claim_rejected(self) -> None:
        with pytest.raises(ValueError, match="claim"):
            Weakness(
                severity="high",
                claim="",
                why_it_fails="y",
                what_a_reviewer_would_say="z",
                fix_hint="w",
            )

    def test_empty_why_it_fails_rejected(self) -> None:
        with pytest.raises(ValueError, match="why_it_fails"):
            Weakness(
                severity="high",
                claim="x",
                why_it_fails="",
                what_a_reviewer_would_say="z",
                fix_hint="w",
            )

    def test_overlong_field_rejected(self) -> None:
        with pytest.raises(ValueError, match="exceeds"):
            Weakness(
                severity="high",
                claim="A" * (MAX_WEAKNESS_FIELD_CHARS + 1),
                why_it_fails="y",
                what_a_reviewer_would_say="z",
                fix_hint="w",
            )

    def test_is_frozen(self) -> None:
        w = _ok_weakness()
        with pytest.raises((AttributeError, Exception)):
            w.severity = "low"  # type: ignore[misc]

    @pytest.mark.parametrize("severity", ["high", "medium", "low"])
    def test_all_severities_accepted(self, severity: str) -> None:
        w = _ok_weakness(severity)
        assert w.severity == severity


# ---------------------------------------------------------------------------
# AttackMemo shape
# ---------------------------------------------------------------------------


class TestAttackMemoShape:
    def test_constructs_with_required_fields(self) -> None:
        memo = _ok_attack_memo()
        assert len(memo.top_weaknesses) == 1

    def test_empty_top_weaknesses_rejected(self) -> None:
        with pytest.raises(ValueError, match="at least"):
            AttackMemo(
                top_weaknesses=(),
                unsupported_assertions=(),
                dialect_mismatches=(),
                boundary_drift=(),
                overall_verdict="x",
            )

    def test_too_many_weaknesses_rejected(self) -> None:
        with pytest.raises(ValueError, match="exceeds"):
            AttackMemo(
                top_weaknesses=tuple(_ok_weakness() for _ in range(MAX_TOP_WEAKNESSES + 1)),
                unsupported_assertions=(),
                dialect_mismatches=(),
                boundary_drift=(),
                overall_verdict="x",
            )

    def test_empty_unsupported_assertion_rejected(self) -> None:
        with pytest.raises(ValueError, match="unsupported_assertions"):
            AttackMemo(
                top_weaknesses=(_ok_weakness(),),
                unsupported_assertions=("",),
                dialect_mismatches=(),
                boundary_drift=(),
                overall_verdict="x",
            )

    def test_empty_overall_verdict_rejected(self) -> None:
        with pytest.raises(ValueError, match="overall_verdict"):
            AttackMemo(
                top_weaknesses=(_ok_weakness(),),
                unsupported_assertions=(),
                dialect_mismatches=(),
                boundary_drift=(),
                overall_verdict="",
            )

    def test_overlong_overall_verdict_rejected(self) -> None:
        with pytest.raises(ValueError, match="exceeds"):
            AttackMemo(
                top_weaknesses=(_ok_weakness(),),
                unsupported_assertions=(),
                dialect_mismatches=(),
                boundary_drift=(),
                overall_verdict="A" * (MAX_OVERALL_VERDICT_CHARS + 1),
            )

    def test_non_tuple_lists_rejected(self) -> None:
        with pytest.raises(TypeError, match="must be tuple"):
            AttackMemo(
                top_weaknesses=(_ok_weakness(),),
                unsupported_assertions=["x"],  # type: ignore[arg-type]
                dialect_mismatches=(),
                boundary_drift=(),
                overall_verdict="ok",
            )


# ---------------------------------------------------------------------------
# RedTeamCriterionScore shape
# ---------------------------------------------------------------------------


class TestRedTeamCriterionScoreShape:
    def test_constructs_with_required_fields(self) -> None:
        c = _ok_criterion()
        assert c.score == 12

    def test_score_exceeds_max_rejected(self) -> None:
        with pytest.raises(ValueError, match="exceeds max_points"):
            _ok_criterion(score=20, max_points=15)

    def test_negative_score_rejected(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            RedTeamCriterionScore(
                criterion_id="x",
                criterion_name="X",
                max_points=10,
                score=-1,
                tier_matched="t",
                evidence="e",
                missing=(),
                notes="",
            )

    def test_negative_max_points_rejected(self) -> None:
        with pytest.raises(ValueError, match="max_points"):
            RedTeamCriterionScore(
                criterion_id="x",
                criterion_name="X",
                max_points=-5,
                score=0,
                tier_matched="t",
                evidence="e",
                missing=(),
                notes="",
            )

    def test_empty_criterion_id_rejected(self) -> None:
        with pytest.raises(ValueError, match="criterion_id"):
            RedTeamCriterionScore(
                criterion_id="",
                criterion_name="X",
                max_points=10,
                score=5,
                tier_matched="t",
                evidence="e",
                missing=(),
                notes="",
            )

    def test_empty_tier_matched_rejected(self) -> None:
        with pytest.raises(ValueError, match="tier_matched"):
            RedTeamCriterionScore(
                criterion_id="x",
                criterion_name="X",
                max_points=10,
                score=5,
                tier_matched="",
                evidence="e",
                missing=(),
                notes="",
            )

    def test_empty_evidence_rejected(self) -> None:
        with pytest.raises(ValueError, match="evidence"):
            RedTeamCriterionScore(
                criterion_id="x",
                criterion_name="X",
                max_points=10,
                score=5,
                tier_matched="t",
                evidence="",
                missing=(),
                notes="",
            )

    def test_evidence_exceeds_cap_rejected(self) -> None:
        with pytest.raises(ValueError, match="evidence exceeds"):
            RedTeamCriterionScore(
                criterion_id="x",
                criterion_name="X",
                max_points=10,
                score=5,
                tier_matched="t",
                evidence="A" * (MAX_EVIDENCE_CHARS + 1),
                missing=(),
                notes="",
            )

    def test_notes_exceeds_cap_rejected(self) -> None:
        with pytest.raises(ValueError, match="notes exceeds"):
            RedTeamCriterionScore(
                criterion_id="x",
                criterion_name="X",
                max_points=10,
                score=5,
                tier_matched="t",
                evidence="e",
                missing=(),
                notes="A" * (MAX_NOTES_CHARS + 1),
            )

    def test_missing_must_be_tuple(self) -> None:
        with pytest.raises(TypeError, match="missing must be tuple"):
            RedTeamCriterionScore(
                criterion_id="x",
                criterion_name="X",
                max_points=10,
                score=5,
                tier_matched="t",
                evidence="e",
                missing=["a"],  # type: ignore[arg-type]
                notes="",
            )

    def test_score_at_max_points_accepted(self) -> None:
        c = _ok_criterion(score=15, max_points=15)
        assert c.score == 15

    def test_score_zero_accepted(self) -> None:
        c = _ok_criterion(score=0, max_points=15)
        assert c.score == 0


# ---------------------------------------------------------------------------
# TotalScoreCorrection shape
# ---------------------------------------------------------------------------


class TestTotalScoreCorrection:
    def test_constructs_with_consistent_delta(self) -> None:
        c = TotalScoreCorrection(
            model_reported=85, computed_from_criteria=87, delta=2
        )
        assert c.delta == 2

    def test_inconsistent_delta_rejected(self) -> None:
        with pytest.raises(ValueError, match="delta"):
            TotalScoreCorrection(
                model_reported=85, computed_from_criteria=87, delta=3
            )

    def test_negative_delta_accepted(self) -> None:
        # Model overcounted (reported 90, criteria sum 85 → delta = -5).
        c = TotalScoreCorrection(
            model_reported=90, computed_from_criteria=85, delta=-5
        )
        assert c.delta == -5


# ---------------------------------------------------------------------------
# RedTeamVerdict shape
# ---------------------------------------------------------------------------


class TestRedTeamVerdict:
    def test_constructs_with_required_fields(self) -> None:
        v = _ok_verdict()
        assert v.total_score == 12  # = sum-of-criteria
        assert v.recommendation == "marginal"

    def test_computed_total_invariant_violation_rejected(self) -> None:
        crit = _ok_criterion(score=12)
        # Pass total_score that disagrees with sum-of-criteria → reject.
        with pytest.raises(ValueError, match="≠ sum-of-criteria"):
            RedTeamVerdict(
                run_id="r",
                rubric_id="vapg",
                rubric_hash="0" * 64,
                total_score=99,  # wrong
                max_score=100,
                recommendation="marginal",
                criteria=(crit,),
                attack_memo=_ok_attack_memo(),
                total_score_correction=None,
                verdict_at_utc=_utc_now(),
                red_team_dialect="conservative",
            )

    def test_total_exceeds_max_rejected(self) -> None:
        crit = _ok_criterion(score=15, max_points=15)
        with pytest.raises(ValueError, match="exceeds max_score"):
            RedTeamVerdict(
                run_id="r",
                rubric_id="vapg",
                rubric_hash="0" * 64,
                total_score=15,
                max_score=10,
                recommendation="marginal",
                criteria=(crit,),
                attack_memo=_ok_attack_memo(),
                total_score_correction=None,
                verdict_at_utc=_utc_now(),
                red_team_dialect="conservative",
            )

    def test_invalid_recommendation_rejected(self) -> None:
        with pytest.raises(ValueError, match="recommendation"):
            RedTeamVerdict(
                run_id="r",
                rubric_id="vapg",
                rubric_hash="0" * 64,
                total_score=12,
                max_score=100,
                recommendation="reject",  # type: ignore[arg-type]
                criteria=(_ok_criterion(),),
                attack_memo=_ok_attack_memo(),
                total_score_correction=None,
                verdict_at_utc=_utc_now(),
                red_team_dialect="conservative",
            )

    def test_invalid_dialect_rejected(self) -> None:
        with pytest.raises(ValueError, match="red_team_dialect"):
            RedTeamVerdict(
                run_id="r",
                rubric_id="vapg",
                rubric_hash="0" * 64,
                total_score=12,
                max_score=100,
                recommendation="marginal",
                criteria=(_ok_criterion(),),
                attack_memo=_ok_attack_memo(),
                total_score_correction=None,
                verdict_at_utc=_utc_now(),
                red_team_dialect="militant",  # type: ignore[arg-type]
            )

    def test_naive_datetime_rejected(self) -> None:
        with pytest.raises(ValueError, match="tz-aware"):
            RedTeamVerdict(
                run_id="r",
                rubric_id="vapg",
                rubric_hash="0" * 64,
                total_score=12,
                max_score=100,
                recommendation="marginal",
                criteria=(_ok_criterion(),),
                attack_memo=_ok_attack_memo(),
                total_score_correction=None,
                verdict_at_utc=datetime(2026, 5, 1, 12, 0, 0),  # naive
                red_team_dialect="conservative",
            )

    def test_empty_criteria_rejected(self) -> None:
        with pytest.raises(ValueError, match="non-empty tuple"):
            RedTeamVerdict(
                run_id="r",
                rubric_id="vapg",
                rubric_hash="0" * 64,
                total_score=0,
                max_score=100,
                recommendation="not_ready",
                criteria=(),
                attack_memo=_ok_attack_memo(),
                total_score_correction=None,
                verdict_at_utc=_utc_now(),
                red_team_dialect="conservative",
            )

    def test_correction_field_optional(self) -> None:
        v = _ok_verdict()
        assert v.total_score_correction is None
        # Now construct with a correction
        crit = _ok_criterion(score=12)
        v2 = RedTeamVerdict(
            run_id="r",
            rubric_id="vapg",
            rubric_hash="0" * 64,
            total_score=12,
            max_score=100,
            recommendation="marginal",
            criteria=(crit,),
            attack_memo=_ok_attack_memo(),
            total_score_correction=TotalScoreCorrection(
                model_reported=15, computed_from_criteria=12, delta=-3
            ),
            verdict_at_utc=_utc_now(),
            red_team_dialect="conservative",
        )
        assert v2.total_score_correction is not None
        assert v2.total_score_correction.delta == -3

    def test_attack_memo_must_be_attack_memo(self) -> None:
        with pytest.raises(TypeError, match="AttackMemo"):
            RedTeamVerdict(
                run_id="r",
                rubric_id="vapg",
                rubric_hash="0" * 64,
                total_score=12,
                max_score=100,
                recommendation="marginal",
                criteria=(_ok_criterion(),),
                attack_memo={"foo": "bar"},  # type: ignore[arg-type]
                total_score_correction=None,
                verdict_at_utc=_utc_now(),
                red_team_dialect="conservative",
            )


# ---------------------------------------------------------------------------
# RedTeamInput + Forward-Protocols
# ---------------------------------------------------------------------------


class _FakeClaimEvidence:
    def __init__(self, evidence_kind: str, source_pointer: str) -> None:
        self.evidence_kind = evidence_kind
        self.source_pointer = source_pointer


class _FakeSectionDraft:
    def __init__(self, section_name: str, body_text: str) -> None:
        self.section_name = section_name
        self.section_order = 1
        self.body_text = body_text
        self.claim_evidence_map: tuple = ()


class _FakeJudgeVerdict:
    def __init__(
        self, run_id: str, rubric_hash: str, total_score: int = 85, max_score: int = 100
    ) -> None:
        self.run_id = run_id
        self.rubric_hash = rubric_hash
        self.total_score = total_score
        self.max_score = max_score
        self.recommendation = "competitive"
        self.overall_notes = "Solid effort"


class _FakeRubric:
    def __init__(self, rubric_id: str = "vapg_fy26", content_hash: str = "h" * 64) -> None:
        self.rubric_id = rubric_id
        self.content_hash = content_hash
        self.max_score = 100
        self.criteria = ()


class TestRedTeamInput:
    def test_constructs_with_required_fields(self) -> None:
        ri = RedTeamInput(
            run_id="run-1",
            section_drafts=(_FakeSectionDraft("project", "body"),),
            claim_evidence_map=(),
            rubric=_FakeRubric(),
            judge_verdict=_FakeJudgeVerdict(run_id="run-1", rubric_hash="h" * 64),
            funder_dialect="conservative",
            admin_risk_register_snapshot=object(),
            prepared_at_utc=_utc_now(),
        )
        assert ri.run_id == "run-1"

    def test_judge_verdict_run_id_mismatch_rejected(self) -> None:
        with pytest.raises(ValueError, match="judge_verdict.run_id"):
            RedTeamInput(
                run_id="run-1",
                section_drafts=(_FakeSectionDraft("p", "b"),),
                claim_evidence_map=(),
                rubric=_FakeRubric(),
                judge_verdict=_FakeJudgeVerdict(run_id="run-DIFFERENT", rubric_hash="h" * 64),
                funder_dialect="conservative",
                admin_risk_register_snapshot=object(),
                prepared_at_utc=_utc_now(),
            )

    def test_rubric_hash_mismatch_rejected(self) -> None:
        with pytest.raises(ValueError, match="rubric_hash"):
            RedTeamInput(
                run_id="run-1",
                section_drafts=(_FakeSectionDraft("p", "b"),),
                claim_evidence_map=(),
                rubric=_FakeRubric(content_hash="h" * 64),
                judge_verdict=_FakeJudgeVerdict(run_id="run-1", rubric_hash="DIFFERENT"),
                funder_dialect="conservative",
                admin_risk_register_snapshot=object(),
                prepared_at_utc=_utc_now(),
            )

    def test_judge_verdict_optional(self) -> None:
        ri = RedTeamInput(
            run_id="run-1",
            section_drafts=(_FakeSectionDraft("p", "b"),),
            claim_evidence_map=(),
            rubric=_FakeRubric(),
            judge_verdict=None,  # M13 bypass scenario
            funder_dialect="conservative",
            admin_risk_register_snapshot=object(),
            prepared_at_utc=_utc_now(),
        )
        assert ri.judge_verdict is None

    def test_empty_section_drafts_rejected(self) -> None:
        with pytest.raises(ValueError, match="section_drafts"):
            RedTeamInput(
                run_id="run-1",
                section_drafts=(),
                claim_evidence_map=(),
                rubric=_FakeRubric(),
                judge_verdict=None,
                funder_dialect="conservative",
                admin_risk_register_snapshot=object(),
                prepared_at_utc=_utc_now(),
            )

    def test_invalid_dialect_rejected(self) -> None:
        with pytest.raises(ValueError, match="funder_dialect"):
            RedTeamInput(
                run_id="run-1",
                section_drafts=(_FakeSectionDraft("p", "b"),),
                claim_evidence_map=(),
                rubric=_FakeRubric(),
                judge_verdict=None,
                funder_dialect="militant",  # type: ignore[arg-type]
                admin_risk_register_snapshot=object(),
                prepared_at_utc=_utc_now(),
            )

    def test_naive_prepared_at_rejected(self) -> None:
        with pytest.raises(ValueError, match="tz-aware"):
            RedTeamInput(
                run_id="run-1",
                section_drafts=(_FakeSectionDraft("p", "b"),),
                claim_evidence_map=(),
                rubric=_FakeRubric(),
                judge_verdict=None,
                funder_dialect="conservative",
                admin_risk_register_snapshot=object(),
                prepared_at_utc=datetime(2026, 5, 1, 12, 0, 0),
            )


class TestForwardProtocols:
    def test_section_draft_protocol_structural(self) -> None:
        sd = _FakeSectionDraft("p", "b")
        assert isinstance(sd, SectionDraftLike)

    def test_judge_verdict_protocol_structural(self) -> None:
        jv = _FakeJudgeVerdict(run_id="x", rubric_hash="y")
        assert isinstance(jv, JudgeVerdictLike)

    def test_rubric_protocol_structural(self) -> None:
        r = _FakeRubric()
        assert isinstance(r, RubricLike)

    def test_claim_evidence_protocol_structural(self) -> None:
        ce = _FakeClaimEvidence("RFA", "RFA:vapg.pdf:lines/40-60")
        assert isinstance(ce, ClaimEvidenceLike)


# ---------------------------------------------------------------------------
# CouncilSplitDecision shape
# ---------------------------------------------------------------------------


class TestCouncilSplitDecision:
    def test_constructs_with_required_fields(self) -> None:
        d = CouncilSplitDecision(
            decision="proceed_with_judge",
            judge_total_score=85,
            red_team_total_score=70,
            delta_absolute=15,
            operator_signoff_at_iso="2026-05-01T22:00:00Z",
            operator_rationale="Judge's framing matched RFA scope",
        )
        assert d.decision == "proceed_with_judge"

    def test_invalid_decision_rejected(self) -> None:
        with pytest.raises(ValueError, match="decision"):
            CouncilSplitDecision(
                decision="abstain",  # type: ignore[arg-type]
                judge_total_score=85,
                red_team_total_score=70,
                delta_absolute=15,
                operator_signoff_at_iso="2026-05-01T22:00:00Z",
                operator_rationale="x",
            )

    def test_delta_must_match(self) -> None:
        with pytest.raises(ValueError, match="delta_absolute"):
            CouncilSplitDecision(
                decision="proceed_with_judge",
                judge_total_score=85,
                red_team_total_score=70,
                delta_absolute=10,  # actual abs(85-70) = 15
                operator_signoff_at_iso="2026-05-01T22:00:00Z",
                operator_rationale="x",
            )

    def test_negative_score_rejected(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            CouncilSplitDecision(
                decision="proceed_with_judge",
                judge_total_score=-1,
                red_team_total_score=70,
                delta_absolute=71,
                operator_signoff_at_iso="2026-05-01T22:00:00Z",
                operator_rationale="x",
            )

    def test_empty_rationale_rejected(self) -> None:
        with pytest.raises(ValueError, match="operator_rationale"):
            CouncilSplitDecision(
                decision="proceed_with_judge",
                judge_total_score=85,
                red_team_total_score=70,
                delta_absolute=15,
                operator_signoff_at_iso="2026-05-01T22:00:00Z",
                operator_rationale="",
            )

    def test_overlong_rationale_rejected(self) -> None:
        with pytest.raises(ValueError, match="exceeds"):
            CouncilSplitDecision(
                decision="revise",
                judge_total_score=85,
                red_team_total_score=70,
                delta_absolute=15,
                operator_signoff_at_iso="2026-05-01T22:00:00Z",
                operator_rationale="A" * (MAX_OPERATOR_RATIONALE_CHARS + 1),
            )

    def test_below_threshold_delta_accepted(self) -> None:
        # Constructor accepts any non-negative delta — POST-gate (not type)
        # enforces the threshold (§10.6 commentary).
        d = CouncilSplitDecision(
            decision="drop",
            judge_total_score=85,
            red_team_total_score=82,
            delta_absolute=3,
            operator_signoff_at_iso="2026-05-01T22:00:00Z",
            operator_rationale="Operator chose to drop despite delta < 10",
        )
        assert d.delta_absolute == 3

    @pytest.mark.parametrize(
        "decision",
        ["proceed_with_judge", "proceed_with_red_team", "revise", "drop"],
    )
    def test_all_decisions_accepted(self, decision: str) -> None:
        d = CouncilSplitDecision(
            decision=decision,  # type: ignore[arg-type]
            judge_total_score=85,
            red_team_total_score=70,
            delta_absolute=15,
            operator_signoff_at_iso="2026-05-01T22:00:00Z",
            operator_rationale="x",
        )
        assert d.decision == decision
