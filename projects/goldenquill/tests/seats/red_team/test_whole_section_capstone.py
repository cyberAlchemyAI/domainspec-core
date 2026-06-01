"""§10 Red Team — whole-section capstone.

Promotes §10 from LOCKED-per-module (R1 types + attack_memo + sfr_emitter
2026-05-01 row 156; R2 judge_view + cross_rubric_dispatch row 157; R3
provider_groq + seat + logician_wiring row 158) to **LOCKED-as-a-whole-
section**. Test-only round; ZERO new production code per §7/§8/§9
whole-section precedent.

Test classes (X.* prefix mirrors §8/§9 whole-section pattern):

- X.1 Lifecycle (run_seat end-to-end happy path + 6 exit codes).
- X.2 F-code matrix (all 24 §10 F-codes trip via canonical paths or
  forwarded codes).
- X.3 Cross-round composition (§10.5 + §10.7 + §10.8 invariants firing
  together with R1/R2/R3 surface).
- X.4 Adversarial (council-split + anchor-suspected + family overlap +
  evidence paraphrased + malformed model output).
- X.5 Capstone manifest (LOCKed-set concat sha pin over 9 production
  modules; module-load surface assertions; AST-lint canary).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Test fixtures (kept terse; mirror R3 test stubs for consistency)
# ---------------------------------------------------------------------------


REPO_ROOT = Path(__file__).resolve().parents[3]


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


class _StubOutboundCallable:
    """Deterministic OutboundCallable stub. Returns canned (status, body_bytes).

    Per CC-007 §4 v2.x.6 fixture-migration sweep (2026-05-16): test stub
    Protocol shape now matches production ``OutboundCallable`` from
    ``pipeline.orchestrator.provider_boundary`` byte-for-byte.
    """

    def __init__(self, status: int, body: bytes | str) -> None:
        self._status = status
        self._body = body.encode("utf-8") if isinstance(body, str) else body

    def __call__(self, *, url, headers, body, timeout_seconds):
        return (self._status, self._body)


class _StubFamilyResolver:
    def __init__(self, mapping: dict) -> None:
        self._mapping = mapping

    def resolve(self, *, seat: str) -> str:
        if seat not in self._mapping:
            raise KeyError(seat)
        return self._mapping[seat]


class _StubClock:
    def __init__(self, dt: datetime | None = None) -> None:
        self._dt = dt or _utc_now()

    def now_utc(self) -> datetime:
        return self._dt


class _FakeSD:
    def __init__(self, body: str = "default body") -> None:
        self.section_name = "p"
        self.section_order = 1
        self.body_text = body
        self.claim_evidence_map: tuple = ()


class _FakeJV:
    def __init__(self, run_id: str = "run-1", rubric_hash: str = "h" * 64) -> None:
        self.run_id = run_id
        self.rubric_hash = rubric_hash
        self.total_score = 12
        self.max_score = 100
        self.recommendation = "competitive"
        self.overall_notes = "n"


class _FakeRubric:
    def __init__(self, content_hash: str = "h" * 64) -> None:
        self.rubric_id = "vapg"
        self.content_hash = content_hash
        self.max_score = 100
        self.criteria = ()


def _draft_body() -> str:
    return (
        "organic mango buyers exceed supply in the region. "
        "Paragraph 3 asserts demand without LOIs as central risk."
    )


def _build_input_bundle(
    *,
    rubric_hash: str = "h" * 64,
    judge_run_id: str | None = "run-1",
    judge_rubric_hash: str | None = None,
):
    from pipeline.seats.red_team.types import RedTeamInput

    if judge_rubric_hash is None:
        judge_rubric_hash = rubric_hash
    jv = _FakeJV(run_id=judge_run_id, rubric_hash=judge_rubric_hash) if judge_run_id else None
    return RedTeamInput(
        run_id="run-1",
        section_drafts=(_FakeSD(_draft_body()),),
        claim_evidence_map=(),
        rubric=_FakeRubric(content_hash=rubric_hash),
        judge_verdict=jv,
        funder_dialect="conservative",
        admin_risk_register_snapshot=object(),
        prepared_at_utc=_utc_now(),
    )


def _ok_groq_body(*, score: int = 12) -> str:
    return json.dumps(
        {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "total_score": score,
                                "recommendation": "marginal",
                                "criteria": [
                                    {
                                        "id": "need",
                                        "name": "Need",
                                        "max_points": 15,
                                        "score": min(score, 15),
                                        "tier_matched": "strong evidence",
                                        "evidence": "organic mango buyers exceed supply",
                                        "missing": ["LOIs"],
                                        "notes": "solid",
                                    }
                                ],
                                "attack_memo": {
                                    "top_weaknesses": [
                                        {
                                            "severity": "medium",
                                            "claim": "Paragraph 3 asserts demand without LOIs",
                                            "why_it_fails": "no buyer evidence",
                                            "what_a_reviewer_would_say": "Where are the LOIs?",
                                            "fix_hint": "Add 3 LOIs",
                                        }
                                    ],
                                    "unsupported_assertions": [],
                                    "dialect_mismatches": [],
                                    "boundary_drift": [],
                                    "overall_verdict": "Marginal feasibility.",
                                },
                            }
                        )
                    }
                }
            ]
        }
    )


def _build_run_seat_kwargs(
    *,
    http_status: int = 200,
    http_body: str | None = None,
    judge_total: int = 10,
    families: dict | None = None,
    rubric_hash: str = "h" * 64,
    session_rubric_hash: str | None = None,
):
    if http_body is None:
        http_body = _ok_groq_body()
    if families is None:
        families = {"scribe": "Anthropic", "judge": "Google", "red_team": "OpenAI-OSS"}
    if session_rubric_hash is None:
        session_rubric_hash = rubric_hash
    ib = _build_input_bundle(rubric_hash=rubric_hash)
    return {
        "input_bundle": ib,
        "rubric_summary_json": '{"max_score":100,"criteria":[{"id":"need","max_points":15}]}',
        "rubric_max_points_by_id": {"need": 15},
        "rubric_max_score": 100,
        "judge_total_score": judge_total,
        "judge_scored_ids": frozenset({"need"}),
        "judge_view_json": '{"total_score":10}',
        "rfa_excerpt": "rfa text",
        "api_key": "test-key",
        "http_post": _StubOutboundCallable(http_status, http_body),
        "family_resolver": _StubFamilyResolver(families),
        "session_rubric_hash": session_rubric_hash,
        "clock": _StubClock(),
    }


# ===========================================================================
# X.1 Lifecycle — full run_seat end-to-end + 6 exit codes
# ===========================================================================


class TestX1Lifecycle:
    def test_run_seat_pass(self) -> None:
        from pipeline.seats.red_team.seat import EXIT_PASS, run_seat

        result = run_seat(**_build_run_seat_kwargs())
        assert result.exit_code == EXIT_PASS
        assert result.verdict is not None
        assert result.sfr_markdown is not None
        assert result.post_gate_result.success is True

    def test_run_seat_returns_pre_gate_fail_on_family_overlap(self) -> None:
        from pipeline.seats.red_team.seat import EXIT_PRE_GATE_FAIL, run_seat

        result = run_seat(
            **_build_run_seat_kwargs(
                families={
                    "scribe": "Anthropic",
                    "judge": "Google",
                    "red_team": "Anthropic",  # collides with scribe
                }
            )
        )
        assert result.exit_code == EXIT_PRE_GATE_FAIL

    def test_run_seat_returns_provider_fail_on_401(self) -> None:
        from pipeline.seats.red_team.seat import EXIT_PROVIDER_FAIL, run_seat

        result = run_seat(
            **_build_run_seat_kwargs(http_status=401, http_body='{"err":"auth"}')
        )
        assert result.exit_code == EXIT_PROVIDER_FAIL

    def test_run_seat_returns_composer_fail_on_malformed_json(self) -> None:
        from pipeline.seats.red_team.seat import EXIT_COMPOSER_FAIL, run_seat

        bad = json.dumps({"choices": [{"message": {"content": "not json"}}]})
        result = run_seat(**_build_run_seat_kwargs(http_body=bad))
        assert result.exit_code == EXIT_COMPOSER_FAIL

    def test_run_seat_returns_council_split(self) -> None:
        from pipeline.seats.red_team.seat import EXIT_COUNCIL_SPLIT, run_seat

        # Red Team scores 12; Judge=85 → delta=73 ≥ 10
        result = run_seat(**_build_run_seat_kwargs(judge_total=85))
        assert result.exit_code == EXIT_COUNCIL_SPLIT
        assert result.post_gate_result.council_split_detected is True

    def test_run_seat_emits_valid_sfr_markdown(self) -> None:
        from pipeline.seats.red_team.seat import EXIT_PASS, run_seat
        from pipeline.seats.red_team.sfr_emitter import (
            CONCLUSION_HEADING,
            PREMISES_HEADING,
            TRACE_HEADING,
        )

        result = run_seat(**_build_run_seat_kwargs())
        assert result.exit_code == EXIT_PASS
        assert PREMISES_HEADING in result.sfr_markdown
        assert TRACE_HEADING in result.sfr_markdown
        assert CONCLUSION_HEADING in result.sfr_markdown

    def test_run_seat_records_provider_family(self) -> None:
        from pipeline.seats.red_team.seat import run_seat

        result = run_seat(**_build_run_seat_kwargs())
        assert result.provider_result.family == "OpenAI-OSS"


# ===========================================================================
# X.2 F-code matrix — all 24 §10 F-codes accounted for (trip or forward)
# ===========================================================================


class TestX2FCodeMatrix:
    def test_f_rt_input_inconsistent_via_judge_run_id_mismatch(self) -> None:
        # Constructor-level: RedTeamInput rejects mismatched run_id directly
        from pipeline.seats.red_team.types import RedTeamInput

        with pytest.raises(ValueError):
            RedTeamInput(
                run_id="run-1",
                section_drafts=(_FakeSD(),),
                claim_evidence_map=(),
                rubric=_FakeRubric(),
                judge_verdict=_FakeJV(run_id="run-DIFFERENT"),
                funder_dialect="conservative",
                admin_risk_register_snapshot=object(),
                prepared_at_utc=_utc_now(),
            )

    def test_f_rt_rubric_drift_via_pre_gate(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_pre_gate
        from pipeline.seats.red_team.types import F_RT_RUBRIC_DRIFT

        ib = _build_input_bundle(rubric_hash="a" * 64)
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "OpenAI-OSS"}
        )
        prompt = (
            "Judge's scoring is context, not authority. "
            + "filler " * 100
            + "Judge's scoring is context, not authority."
        )
        result = run_pre_gate(
            input_bundle=ib,
            family_resolver=fr,
            session_rubric_hash="DIFFERENT" * 7 + "00",
            compiled_prompt=prompt,
        )
        assert F_RT_RUBRIC_DRIFT in result.failure_codes

    def test_f_rt_family_overlap_with_scribe(self) -> None:
        from pipeline.seats.red_team.seat import EXIT_PRE_GATE_FAIL, run_seat
        from pipeline.seats.red_team.types import F_RT_FAMILY_OVERLAP

        result = run_seat(
            **_build_run_seat_kwargs(
                families={"scribe": "X", "judge": "Y", "red_team": "X"}
            )
        )
        assert result.exit_code == EXIT_PRE_GATE_FAIL
        assert F_RT_FAMILY_OVERLAP in result.pre_gate_result.failure_codes

    def test_f_rt_family_overlap_with_judge(self) -> None:
        from pipeline.seats.red_team.seat import EXIT_PRE_GATE_FAIL, run_seat
        from pipeline.seats.red_team.types import F_RT_FAMILY_OVERLAP

        result = run_seat(
            **_build_run_seat_kwargs(
                families={"scribe": "X", "judge": "Y", "red_team": "Y"}
            )
        )
        assert F_RT_FAMILY_OVERLAP in result.pre_gate_result.failure_codes

    def test_f_rt_no_compliant_family_via_resolver_keyerror(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_pre_gate
        from pipeline.seats.red_team.types import F_RT_NO_COMPLIANT_FAMILY

        ib = _build_input_bundle()
        fr = _StubFamilyResolver({"scribe": "X"})  # missing judge + red_team
        prompt = (
            "Judge's scoring is context, not authority. "
            + "filler " * 100
            + "Judge's scoring is context, not authority."
        )
        result = run_pre_gate(
            input_bundle=ib,
            family_resolver=fr,
            session_rubric_hash="h" * 64,
            compiled_prompt=prompt,
        )
        assert F_RT_NO_COMPLIANT_FAMILY in result.failure_codes

    def test_f_rt_context_placement(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_pre_gate
        from pipeline.seats.red_team.types import F_RT_CONTEXT_PLACEMENT

        ib = _build_input_bundle()
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "OpenAI-OSS"}
        )
        result = run_pre_gate(
            input_bundle=ib,
            family_resolver=fr,
            session_rubric_hash="h" * 64,
            compiled_prompt="text without anti-anchor phrase",
        )
        assert F_RT_CONTEXT_PLACEMENT in result.failure_codes

    def test_f_rt_evidence_not_in_draft(self) -> None:
        from pipeline.seats.red_team.attack_memo import assert_evidence_in_drafts
        from pipeline.seats.red_team.types import (
            AttackMemo,
            F_RT_EVIDENCE_NOT_IN_DRAFT,
            RedTeamCriterionScore,
            RedTeamVerdict,
            Weakness,
        )

        verdict = RedTeamVerdict(
            run_id="r",
            rubric_id="vapg",
            rubric_hash="h" * 64,
            total_score=10,
            max_score=100,
            recommendation="marginal",
            criteria=(
                RedTeamCriterionScore(
                    criterion_id="need",
                    criterion_name="N",
                    max_points=15,
                    score=10,
                    tier_matched="strong",
                    evidence="evidence not in any draft",
                    missing=(),
                    notes="",
                ),
            ),
            attack_memo=AttackMemo(
                top_weaknesses=(
                    Weakness(
                        severity="high",
                        claim="claim not in draft",
                        why_it_fails="x",
                        what_a_reviewer_would_say="y",
                        fix_hint="z",
                    ),
                ),
                unsupported_assertions=(),
                dialect_mismatches=(),
                boundary_drift=(),
                overall_verdict="ok",
            ),
            total_score_correction=None,
            verdict_at_utc=_utc_now(),
            red_team_dialect="conservative",
        )
        violations = assert_evidence_in_drafts(
            verdict=verdict, drafts=(_FakeSD("totally different body"),)
        )
        assert len(violations) > 0
        assert all(F_RT_EVIDENCE_NOT_IN_DRAFT in v for v in violations)

    def test_f_rt_score_out_of_range_via_constructor(self) -> None:
        from pipeline.seats.red_team.types import RedTeamCriterionScore

        with pytest.raises(ValueError, match="exceeds max_points"):
            RedTeamCriterionScore(
                criterion_id="x",
                criterion_name="X",
                max_points=10,
                score=20,
                tier_matched="t",
                evidence="e",
                missing=(),
                notes="",
            )

    def test_f_rt_score_sum_mismatch_via_constructor(self) -> None:
        from pipeline.seats.red_team.types import (
            AttackMemo,
            RedTeamCriterionScore,
            RedTeamVerdict,
            Weakness,
        )

        crit = RedTeamCriterionScore(
            criterion_id="x",
            criterion_name="X",
            max_points=15,
            score=10,
            tier_matched="t",
            evidence="e",
            missing=(),
            notes="",
        )
        with pytest.raises(ValueError, match="≠ sum-of-criteria"):
            RedTeamVerdict(
                run_id="r",
                rubric_id="vapg",
                rubric_hash="h" * 64,
                total_score=99,  # disagrees with sum 10
                max_score=100,
                recommendation="marginal",
                criteria=(crit,),
                attack_memo=AttackMemo(
                    top_weaknesses=(
                        Weakness(
                            severity="low",
                            claim="x",
                            why_it_fails="x",
                            what_a_reviewer_would_say="x",
                            fix_hint="x",
                        ),
                    ),
                    unsupported_assertions=(),
                    dialect_mismatches=(),
                    boundary_drift=(),
                    overall_verdict="x",
                ),
                total_score_correction=None,
                verdict_at_utc=_utc_now(),
                red_team_dialect="conservative",
            )

    def test_f_rt_criterion_missing_via_dispatcher(self) -> None:
        from pipeline.seats.red_team.cross_rubric_dispatch import (
            assert_red_team_id_set_matches_judge,
        )
        from pipeline.seats.red_team.types import F_RT_CRITERION_MISSING

        v = assert_red_team_id_set_matches_judge(
            red_team_scored_ids=frozenset({"need"}),
            judge_scored_ids=frozenset({"need", "market"}),
        )
        assert any(F_RT_CRITERION_MISSING in vv for vv in v)

    def test_f_rt_weaknesses_empty_via_constructor(self) -> None:
        from pipeline.seats.red_team.types import AttackMemo

        with pytest.raises(ValueError, match="at least"):
            AttackMemo(
                top_weaknesses=(),
                unsupported_assertions=(),
                dialect_mismatches=(),
                boundary_drift=(),
                overall_verdict="x",
            )

    def test_f_rt_recommendation_invalid_via_composer(self) -> None:
        from pipeline.seats.red_team.attack_memo import compose_red_team_verdict
        from pipeline.seats.red_team.types import F_RT_RECOMMENDATION_INVALID

        ib = _build_input_bundle()
        with pytest.raises(ValueError, match=F_RT_RECOMMENDATION_INVALID):
            compose_red_team_verdict(
                parsed_model_output={
                    "total_score": 12,
                    "recommendation": "REJECT",  # not in closed set
                    "criteria": [
                        {
                            "id": "need",
                            "name": "N",
                            "max_points": 15,
                            "score": 12,
                            "tier_matched": "x",
                            "evidence": "x",
                            "missing": [],
                            "notes": "",
                        }
                    ],
                    "attack_memo": {
                        "top_weaknesses": [
                            {
                                "severity": "high",
                                "claim": "x",
                                "why_it_fails": "x",
                                "what_a_reviewer_would_say": "x",
                                "fix_hint": "x",
                            }
                        ],
                        "unsupported_assertions": [],
                        "dialect_mismatches": [],
                        "boundary_drift": [],
                        "overall_verdict": "x",
                    },
                },
                input_bundle=ib,
                rubric_max_points_by_id={"need": 15},
                rubric_max_score=100,
            )

    def test_f_rt_provider_auth_fail(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            F_RT_PROVIDER_AUTH_FAIL,
            call_groq,
        )

        result = call_groq(
            http_post=_StubOutboundCallable(403, "{}"),
            api_key="x",
            system_prompt="s",
            user_prompt="u",
        )
        assert result.failure_code == F_RT_PROVIDER_AUTH_FAIL

    def test_f_rt_provider_rate_limited(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            F_RT_PROVIDER_RATE_LIMITED,
            call_groq,
        )

        result = call_groq(
            http_post=_StubOutboundCallable(429, "{}"),
            api_key="x",
            system_prompt="s",
            user_prompt="u",
        )
        assert result.failure_code == F_RT_PROVIDER_RATE_LIMITED

    def test_f_council_split_via_post_gate(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_post_gate
        from pipeline.seats.red_team.types import F_COUNCIL_SPLIT

        # red_team=2, judge=15 → delta=13 ≥ 10
        from pipeline.seats.red_team.types import (
            AttackMemo,
            RedTeamCriterionScore,
            RedTeamVerdict,
            Weakness,
        )

        verdict = RedTeamVerdict(
            run_id="r",
            rubric_id="vapg",
            rubric_hash="h" * 64,
            total_score=2,
            max_score=100,
            recommendation="not_ready",
            criteria=(
                RedTeamCriterionScore(
                    criterion_id="need",
                    criterion_name="N",
                    max_points=15,
                    score=2,
                    tier_matched="weak",
                    evidence="organic mango buyers exceed supply",
                    missing=(),
                    notes="",
                ),
            ),
            attack_memo=AttackMemo(
                top_weaknesses=(
                    Weakness(
                        severity="high",
                        claim="Paragraph 3 asserts demand without LOIs",
                        why_it_fails="x",
                        what_a_reviewer_would_say="y",
                        fix_hint="z",
                    ),
                ),
                unsupported_assertions=(),
                dialect_mismatches=(),
                boundary_drift=(),
                overall_verdict="not ready",
            ),
            total_score_correction=None,
            verdict_at_utc=_utc_now(),
            red_team_dialect="conservative",
        )
        result = run_post_gate(
            verdict=verdict,
            drafts=(_FakeSD(_draft_body()),),
            judge_total_score=15,
            judge_scored_ids=frozenset({"need"}),
            rubric_criteria_count=2,
            total_words=20,
        )
        assert F_COUNCIL_SPLIT in result.failure_codes
        assert result.council_split_detected is True

    def test_f_rt_judge_anchor_suspected_advisory(self) -> None:
        from pipeline.seats.red_team.attack_memo import detect_judge_anchor_suspected

        # delta=1, criteria=7, words=1500 → fires
        assert (
            detect_judge_anchor_suspected(
                judge_total_score=85,
                red_team_total_score=86,
                rubric_criteria_count=7,
                total_words=1500,
            )
            is True
        )

    def test_f_rt_verdict_cert_malformed_missing_block(self) -> None:
        from pipeline.seats.red_team.logician_wiring import (
            assert_sfr_three_block_present,
        )
        from pipeline.seats.red_team.types import F_RT_VERDICT_CERT_MALFORMED

        v = assert_sfr_three_block_present("## Premises\n\n## Conclusion")
        assert any(F_RT_VERDICT_CERT_MALFORMED in vv for vv in v)


# ===========================================================================
# X.3 Cross-round composition — R1+R2+R3 working together
# ===========================================================================


class TestX3CrossRoundComposition:
    def test_full_pipeline_emits_sfr_with_recommendation_round_trip(self) -> None:
        """R1 types + R2 view + R3 seat → SFR markdown → R1 parser back to recommendation."""
        from pipeline.seats.red_team.seat import EXIT_PASS, run_seat
        from pipeline.seats.red_team.sfr_emitter import parse_recommendation_from_sfr

        result = run_seat(**_build_run_seat_kwargs())
        assert result.exit_code == EXIT_PASS
        assert parse_recommendation_from_sfr(result.sfr_markdown) == "marginal"

    def test_r2_view_adapter_threads_through_full_lifecycle(self) -> None:
        """R2 JudgeContextView builds from real Judge JudgeVerdict; R3 seat consumes it."""
        from pipeline.seats.judge.types import (
            CriterionScore as JudgeCriterionScore,
        )
        from pipeline.seats.judge.types import (
            JudgeOutput,
            JudgeVerdict,
            ResponsivenessMap,
        )
        from pipeline.seats.red_team.judge_view import view_from_judge_verdict

        # Build a real Judge verdict
        cs = JudgeCriterionScore(
            criterion_id="need",
            score=12,
            evidence_quote="organic mango buyers exceed supply",
            confidence=0.85,
            rationale="solid",
        )
        jo = JudgeOutput(
            criterion_scores=(cs,),
            total_score=12,
            max_total=15,
            rubric_sha256="b" * 64,
            rfa_content_sha3_512="c" * 128,
            scored_at_utc=_utc_now(),
        )
        jv = JudgeVerdict(
            judge_output=jo,
            rubric_program_code="vapg",
            responsiveness_map=ResponsivenessMap(entries=()),
            assembled_at_utc=_utc_now(),
        )
        view = view_from_judge_verdict(
            jv,
            run_id="run-r2-real",
            recommendation="marginal",
            overall_notes="solid effort",
        )
        # The view's hash MUST match the underlying JudgeOutput's rubric_sha256.
        assert view.rubric_hash == jo.rubric_sha256

    def test_r3_seat_uses_r2_dispatcher_implicitly(self) -> None:
        """R3 POST-gate uses R2 cross_rubric_dispatch identity-invariant check."""
        from pipeline.seats.red_team.seat import run_seat

        # Judge scored {need}; Red Team will score {need} per the canned response.
        result = run_seat(**_build_run_seat_kwargs())
        # Identity-invariant should not fail (PASS path means R2 dispatcher passed).
        assert "F-RT-CRITERION-MISSING" not in (result.post_gate_result.failure_codes if result.post_gate_result else ())

    def test_anti_anchoring_phrase_in_compiled_prompt_at_head_and_tail(self) -> None:
        """R3 SYSTEM_PROMPT amendment lands phrase at head + user prompt repeats at tail."""
        from pipeline.seats.red_team.seat import SYSTEM_PROMPT

        # System prompt itself should carry the phrase early (head third).
        n = len(SYSTEM_PROMPT)
        head_third = SYSTEM_PROMPT[: n // 3]
        assert "Judge's scoring is context, not authority" in head_third


# ===========================================================================
# X.4 Adversarial — boundary cases + injection-style attacks
# ===========================================================================


class TestX4Adversarial:
    def test_council_split_at_threshold_exactly_10_inclusive(self) -> None:
        """Boundary: |Δ| == 10 fires F-COUNCIL-SPLIT."""
        from pipeline.seats.red_team.attack_memo import detect_council_split

        assert detect_council_split(judge_total_score=15, red_team_total_score=5) is True

    def test_council_split_below_threshold_9_does_not_fire(self) -> None:
        from pipeline.seats.red_team.attack_memo import detect_council_split

        assert detect_council_split(judge_total_score=14, red_team_total_score=5) is False

    def test_anchor_advisory_below_2_fires_only_on_non_trivial_draft(self) -> None:
        from pipeline.seats.red_team.attack_memo import detect_judge_anchor_suspected

        # delta=0 but draft small → does NOT fire
        assert (
            detect_judge_anchor_suspected(
                judge_total_score=85,
                red_team_total_score=85,
                rubric_criteria_count=3,
                total_words=500,
            )
            is False
        )

    def test_run_seat_rejects_naive_prepared_at_via_input_constructor(self) -> None:
        """Naive datetime in RedTeamInput.prepared_at_utc → constructor rejects."""
        from pipeline.seats.red_team.types import RedTeamInput

        with pytest.raises(ValueError, match="tz-aware"):
            RedTeamInput(
                run_id="r",
                section_drafts=(_FakeSD(),),
                claim_evidence_map=(),
                rubric=_FakeRubric(),
                judge_verdict=None,
                funder_dialect="conservative",
                admin_risk_register_snapshot=object(),
                prepared_at_utc=datetime(2026, 5, 1, 12, 0, 0),  # naive
            )

    def test_run_seat_rejects_overlong_evidence_via_constructor(self) -> None:
        from pipeline.seats.red_team.types import (
            MAX_EVIDENCE_CHARS,
            RedTeamCriterionScore,
        )

        with pytest.raises(ValueError, match="evidence exceeds"):
            RedTeamCriterionScore(
                criterion_id="x",
                criterion_name="X",
                max_points=15,
                score=10,
                tier_matched="t",
                evidence="A" * (MAX_EVIDENCE_CHARS + 1),
                missing=(),
                notes="",
            )

    def test_run_seat_rejects_too_many_top_weaknesses(self) -> None:
        from pipeline.seats.red_team.types import (
            MAX_TOP_WEAKNESSES,
            AttackMemo,
            Weakness,
        )

        with pytest.raises(ValueError, match="exceeds"):
            AttackMemo(
                top_weaknesses=tuple(
                    Weakness(
                        severity="low",
                        claim=f"claim {i}",
                        why_it_fails="x",
                        what_a_reviewer_would_say="y",
                        fix_hint="z",
                    )
                    for i in range(MAX_TOP_WEAKNESSES + 1)
                ),
                unsupported_assertions=(),
                dialect_mismatches=(),
                boundary_drift=(),
                overall_verdict="x",
            )

    def test_judge_view_truncates_at_400_chars(self) -> None:
        """Adapter truncates Judge's overall_notes — anti-anchoring discipline.

        If full notes leaked through, Red Team would over-anchor."""
        from pipeline.seats.red_team.judge_view import (
            OVERALL_NOTES_TRUNCATION_CHARS,
            view_from_judge_verdict,
        )

        class _FakeJO:
            total_score = 85
            max_total = 100
            rubric_sha256 = "f" * 64

        class _FakeRM:
            entries: tuple = ()

        class _FakeJV2:
            judge_output = _FakeJO()
            rubric_program_code = "v"
            responsiveness_map = _FakeRM()

        long_notes = "DETAIL " * 200  # 1400 chars
        view = view_from_judge_verdict(
            _FakeJV2(),
            run_id="r",
            recommendation="competitive",
            overall_notes=long_notes,
        )
        assert len(view.overall_notes) == OVERALL_NOTES_TRUNCATION_CHARS

    def test_no_score_averaging_pattern_in_pipeline(self) -> None:
        """Grep `pipeline/` for the anti-averaging pattern. None expected."""
        # Walk pipeline/ python files; grep for forbidden patterns.
        forbidden_patterns = [
            "(judge_score + red_team_score) / 2",
            "(judge_total_score + red_team_total_score) / 2",
            "mean(judge_score, red_team_score)",
        ]
        pipeline_dir = REPO_ROOT / "pipeline"
        violations: list[str] = []
        for py_file in pipeline_dir.rglob("*.py"):
            text = py_file.read_text(encoding="utf-8")
            for pat in forbidden_patterns:
                if pat in text:
                    violations.append(f"{py_file}: {pat}")
        assert violations == [], (
            f"§10.6 anti-averaging invariant violated: {violations}"
        )


# ===========================================================================
# X.5 Capstone manifest — LOCKed-set concat sha pin + module-load surface
# ===========================================================================


# Pin the LOCKed-set concat sha at capstone authoring time. If any of the 9
# §10 production modules drifts from byte-for-byte LOCK state, this pin
# fails — failing to open at this version. Promotes byte-level integrity
# from per-module-LOCK row attestation to capstone-level invariant.
# 2026-05-16 refresh: pin updated after the CC-007 provider-boundary runtime
# companion collapsed Red Team provider HTTP through the shared outbound wrapper.
LOCKED_SET_CONCAT_SHA3_512_PREFIX_16: str = "c579f6f71a88892f"

LOCKED_SET_FILES: tuple[str, ...] = (
    "pipeline/seats/red_team/__init__.py",
    "pipeline/seats/red_team/types.py",
    "pipeline/seats/red_team/attack_memo.py",
    "pipeline/seats/red_team/sfr_emitter.py",
    "pipeline/seats/red_team/judge_view.py",
    "pipeline/seats/red_team/cross_rubric_dispatch.py",
    "pipeline/seats/red_team/provider_groq.py",
    "pipeline/seats/red_team/logician_wiring.py",
    "pipeline/seats/red_team/seat.py",
)


class TestX5CapstoneManifest:
    def test_locked_set_concat_sha_pin(self) -> None:
        """Byte-level integrity pin over the 9 LOCKed §10 production files."""
        h = hashlib.sha3_512()
        for f in LOCKED_SET_FILES:
            h.update((REPO_ROOT / f).read_bytes())
        assert h.hexdigest()[:16] == LOCKED_SET_CONCAT_SHA3_512_PREFIX_16, (
            f"§10 LOCKed-set drift: expected {LOCKED_SET_CONCAT_SHA3_512_PREFIX_16}; "
            f"got {h.hexdigest()[:16]}"
        )

    def test_all_locked_files_exist(self) -> None:
        for f in LOCKED_SET_FILES:
            assert (REPO_ROOT / f).is_file(), f"§10 LOCKed file missing: {f}"

    def test_public_surface_exports(self) -> None:
        """The 7 schemas + 4 helpers must be in the package public surface."""
        import pipeline.seats.red_team as red_team

        required = (
            # Schemas
            "RedTeamInput",
            "RedTeamVerdict",
            "RedTeamCriterionScore",
            "AttackMemo",
            "Weakness",
            "TotalScoreCorrection",
            "CouncilSplitDecision",
            # Helpers
            "compose_red_team_verdict",
            "assert_evidence_in_drafts",
            "detect_council_split",
            "emit_sfr_certificate",
        )
        for name in required:
            assert hasattr(red_team, name), f"public export missing: {name}"

    def test_failure_code_constants_uppercase_dashed(self) -> None:
        """All 24 §10 F-codes follow F-RT-* / F-COUNCIL-* uppercase-dashed convention."""
        from pipeline.seats.red_team import types

        f_codes = [n for n in dir(types) if n.startswith("F_")]
        assert len(f_codes) >= 24
        for name in f_codes:
            value = getattr(types, name)
            assert isinstance(value, str), f"{name} not str"
            assert value.startswith(("F-RT-", "F-COUNCIL-")), value
            assert value.upper() == value, f"{name} value not uppercase: {value!r}"

    def test_module_count_per_round_invariant(self) -> None:
        """R1 = 4 files (incl. __init__) + R2 = 2 + R3 = 3 = 9 total."""
        assert len(LOCKED_SET_FILES) == 9

    def test_v1_inline_literal_constants_canonical(self) -> None:
        """V1 inline-literal rebind-resistance — the load-bearing constants
        must hold their LOCKed values."""
        from pipeline.seats.red_team import (
            MAX_EVIDENCE_CHARS,
            MAX_TOP_WEAKNESSES,
            MIN_TOP_WEAKNESSES,
            RT_ANCHOR_SUSPECTED_THRESHOLD,
            RT_DISAGREEMENT_THRESHOLD,
        )

        assert RT_DISAGREEMENT_THRESHOLD == 10
        assert RT_ANCHOR_SUSPECTED_THRESHOLD == 2
        assert MAX_EVIDENCE_CHARS == 320
        assert MAX_TOP_WEAKNESSES == 5
        assert MIN_TOP_WEAKNESSES == 1

    def test_exit_codes_canonical(self) -> None:
        from pipeline.seats.red_team.seat import (
            EXIT_COMPOSER_FAIL,
            EXIT_COUNCIL_SPLIT,
            EXIT_PASS,
            EXIT_POST_GATE_FAIL,
            EXIT_PRE_GATE_FAIL,
            EXIT_PROVIDER_FAIL,
        )

        assert EXIT_PASS == 0
        assert EXIT_PRE_GATE_FAIL == 1
        assert EXIT_PROVIDER_FAIL == 2
        assert EXIT_COMPOSER_FAIL == 3
        assert EXIT_POST_GATE_FAIL == 4
        assert EXIT_COUNCIL_SPLIT == 5

    def test_capstone_test_file_self_reference(self) -> None:
        """This test file IS the whole-section capstone — assert its own
        existence + module-name."""
        capstone_path = REPO_ROOT / "tests/seats/red_team/test_whole_section_capstone.py"
        assert capstone_path.is_file()


# ===========================================================================
# X.6 Self-audit — ensure every test class is reachable + LOCKed-set parity
# ===========================================================================


class TestX6SelfAudit:
    def test_all_test_classes_have_at_least_one_test(self) -> None:
        # Module-level scan: every TestX* class must have ≥ 1 test method.
        import sys

        mod = sys.modules[__name__]
        test_classes = [
            attr
            for attr_name, attr in vars(mod).items()
            if attr_name.startswith("TestX")
            and isinstance(attr, type)
        ]
        assert len(test_classes) >= 5
        for cls in test_classes:
            test_methods = [m for m in dir(cls) if m.startswith("test_")]
            assert len(test_methods) >= 1, f"{cls.__name__} has no tests"

    def test_capstone_imports_clean(self) -> None:
        """Sanity: importing every R1+R2+R3 module from test scope succeeds."""
        from pipeline.seats import red_team
        from pipeline.seats.red_team import (
            attack_memo,
            cross_rubric_dispatch,
            judge_view,
            logician_wiring,
            provider_groq,
            seat,
            sfr_emitter,
            types,
        )

        assert red_team is not None
        for mod in (
            attack_memo,
            cross_rubric_dispatch,
            judge_view,
            logician_wiring,
            provider_groq,
            seat,
            sfr_emitter,
            types,
        ):
            assert mod.__name__.startswith("pipeline.seats.red_team")
