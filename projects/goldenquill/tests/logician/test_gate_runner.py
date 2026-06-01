"""Tests for ``pipeline.logician.gate_runner``.

Round 6 capstone — state machine + 13-step POST-gate orchestrator. Tests cover
the PRE/BETWEEN/POST/DONE state machine, mid-loop call rejection (F-PRE-19),
the 13 POST-gate step ordering with caller-provided + inline-evaluated
outcomes, and integration with Round 2's ``run_post_gate_skeleton``.
"""

from __future__ import annotations

import dataclasses

import pytest

from pipeline.logician.cedar_eval import CedarPolicy
from pipeline.logician.claim_evidence import ClaimEntry, SourceRef, compute_claim_id
from pipeline.logician.gate_runner import (
    F_POST_01_DRAFT_NOT_READY,
    F_POST_02_PRE_INVARIANT_DRIFT,
    POST_GATE_STEP_NAMES,
    POST_GATE_STEP_ORDER,
    STATE_BETWEEN,
    STATE_DONE,
    STATE_POST,
    STATE_PRE,
    VALID_STATES,
    GateRunnerPostResult,
    LogicianGateRunner,
    LogicianMidLoopCall,
    PostGateInput,
    PostGateStepOutcome,
)
from pipeline.logician.post_gate import F_POST_10, F_POST_11
from pipeline.logician.pre_gate import (
    F_PRE_19_LOGICIAN_MID_LOOP_CALL,
    PRE_GATE_CHECK_NAMES,
    CheckOutcome,
    PreGateInput,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _policy(
    *,
    name: str = "org_isolation",
    text: str = "permit(principal, action, resource);",
    sig: bytes = b"\x01\x02",
    head: str = "h" * 128,
) -> CedarPolicy:
    return CedarPolicy(
        name=name,
        text=text,
        operator_signature=sig,
        signed_at_utc="2026-04-19T00:00:00Z",
        m15_ledger_head=head,
    )


def _pass_pre_outcome(check_number: int) -> CheckOutcome:
    return CheckOutcome(
        check_number=check_number,
        check_name=PRE_GATE_CHECK_NAMES[check_number],
        passed=True,
        failure_code=None,
        failure_detail="",
    )


def _fail_pre_outcome(check_number: int, code: str) -> CheckOutcome:
    return CheckOutcome(
        check_number=check_number,
        check_name=PRE_GATE_CHECK_NAMES[check_number],
        passed=False,
        failure_code=code,
        failure_detail="fail",
    )


def _all_pre_pass() -> dict[int, CheckOutcome]:
    return {n: _pass_pre_outcome(n) for n in (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 16, 18)}


def _happy_pre_input(**overrides) -> PreGateInput:
    base = dict(
        caller_outcomes=_all_pre_pass(),
        cedar_policy=_policy(),
        cedar_expected_ledger_head="h" * 128,
        # post-2026-04-29 L-005 narrow-fix (a): signature_verifier is required.
        cedar_signature_verifier=lambda _p: True,
        admin_risk_ok=True,
        admin_risk_sub_failure_code=None,
        admin_risk_failure_detail="",
        dossier_signoff_states=(("entity_a", True),),
        project_context_text="EIN: 12-3456789\nUEI: ABCD\n",
    )
    base.update(overrides)
    return PreGateInput(**base)


def _make_doc_sourced_claim(*, draft_hash: str = "d" * 128, offset: int = 0) -> ClaimEntry:
    text = "Mycelial networks process matter into structured tilth."
    cid = compute_claim_id(draft_hash=draft_hash, draft_offset=offset, claim_text=text)
    return ClaimEntry(
        claim_id=cid,
        draft_offset=offset,
        claim_text=text,
        tag="DOC_SOURCED",
        source_ref=SourceRef(
            source_kind="RFA",
            canonical_path="/rfa/abc.md",
            inode=42,
            content_hash="c" * 128,
            grep_string=text,
            window_size_sentences=2,
        ),
        verify_method="grep_windowed_pm2",
        verify_result="PASS",
        verify_detail="ok",
        rigor_breach_flag=False,
    )


def _make_unsourced_claim(*, draft_hash: str = "d" * 128, offset: int = 1) -> ClaimEntry:
    text = "An unsupported assertion."
    cid = compute_claim_id(draft_hash=draft_hash, draft_offset=offset, claim_text=text)
    return ClaimEntry(
        claim_id=cid,
        draft_offset=offset,
        claim_text=text,
        tag="UNSOURCED",
        source_ref=None,
        verify_method="unresolved",
        verify_result="UNSOURCED",
        verify_detail="no source",
        rigor_breach_flag=False,
    )


def _pass_post_step(step_number: int) -> PostGateStepOutcome:
    return PostGateStepOutcome(
        step_number=step_number,
        step_name=POST_GATE_STEP_NAMES[step_number],
        passed=True,
        failure_code=None,
        failure_detail="",
    )


def _fail_post_step(step_number: int, code: str) -> PostGateStepOutcome:
    return PostGateStepOutcome(
        step_number=step_number,
        step_name=POST_GATE_STEP_NAMES[step_number],
        passed=False,
        failure_code=code,
        failure_detail="fail",
    )


def _all_caller_post_pass() -> dict[int, PostGateStepOutcome]:
    return {n: _pass_post_step(n) for n in (1, 2, 3, 7, 8, 10, 11, 12, 13)}


def _happy_post_input(**overrides) -> PostGateInput:
    base = dict(
        caller_step_outcomes=_all_caller_post_pass(),
        draft_hash="d" * 128,
        rfa_hash="r" * 128,
        session_id="sess-1",
        org_slug="mycosymbiotics_cooperative",
        rfa_url_hash="u" * 128,
        claims=(_make_doc_sourced_claim(),),
        generated_at_utc="2026-04-19T12:00:00Z",
        dossier_verify_failure_codes=(),
        admin_risk_hard_block_count=0,
        rigor_breach_active=False,
    )
    base.update(overrides)
    return PostGateInput(**base)


# ---------------------------------------------------------------------------
# Constants + state names
# ---------------------------------------------------------------------------


class TestConstants:
    def test_states_pinned(self) -> None:
        assert STATE_PRE == "PRE"
        assert STATE_BETWEEN == "BETWEEN"
        assert STATE_POST == "POST"
        assert STATE_DONE == "DONE"
        assert VALID_STATES == frozenset({"PRE", "BETWEEN", "POST", "DONE"})

    def test_post_step_order(self) -> None:
        assert POST_GATE_STEP_ORDER == tuple(range(1, 14))
        assert len(POST_GATE_STEP_ORDER) == 13

    def test_step_names_complete(self) -> None:
        assert set(POST_GATE_STEP_NAMES.keys()) == set(POST_GATE_STEP_ORDER)

    def test_post_failure_codes_pinned(self) -> None:
        assert F_POST_01_DRAFT_NOT_READY == "F-POST-01.draft_not_ready"
        assert F_POST_02_PRE_INVARIANT_DRIFT == "F-POST-02.pre_invariant_drift"


# ---------------------------------------------------------------------------
# Result + step outcome shapes
# ---------------------------------------------------------------------------


class TestResultShapes:
    def test_step_outcome_frozen_kw_only(self) -> None:
        o = _pass_post_step(1)
        assert dataclasses.is_dataclass(o)
        with pytest.raises(dataclasses.FrozenInstanceError):
            o.passed = False  # type: ignore[misc]

    def test_post_input_frozen_kw_only(self) -> None:
        i = _happy_post_input()
        assert dataclasses.is_dataclass(i)
        with pytest.raises(dataclasses.FrozenInstanceError):
            i.draft_hash = "x"  # type: ignore[misc]

    def test_post_result_frozen_kw_only(self) -> None:
        r = GateRunnerPostResult(
            passed=True,
            failed_step_number=None,
            failure_code=None,
            failure_detail="",
            failure_codes=(),
            completed_steps=(),
            claim_evidence_map=None,
            underlying_post_gate_result=None,
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.passed = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Mid-loop exception
# ---------------------------------------------------------------------------


class TestMidLoopCall:
    def test_exception_carries_pre_19_code(self) -> None:
        e = LogicianMidLoopCall("BETWEEN", "POST")
        assert e.code == F_PRE_19_LOGICIAN_MID_LOOP_CALL
        assert F_PRE_19_LOGICIAN_MID_LOOP_CALL in str(e)
        assert e.current_state == "BETWEEN"


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


class TestStateMachine:
    def test_initial_state_pre(self) -> None:
        runner = LogicianGateRunner()
        assert runner.state == STATE_PRE
        assert runner.pre_gate_result is None
        assert runner.post_gate_result is None

    def test_invalid_initial_state_rejected(self) -> None:
        with pytest.raises(ValueError):
            LogicianGateRunner(state="BOGUS")

    def test_pre_pass_then_between(self) -> None:
        runner = LogicianGateRunner()
        result = runner.run_pre_gate(_happy_pre_input())
        assert result.passed is True
        assert runner.state == STATE_PRE  # pre_gate does not auto-advance to BETWEEN
        runner.mark_between()
        assert runner.state == STATE_BETWEEN

    def test_pre_fail_advances_to_done(self) -> None:
        runner = LogicianGateRunner()
        outcomes = _all_pre_pass()
        outcomes[1] = _fail_pre_outcome(1, "F-PRE-01.section_2_lock_missing")
        result = runner.run_pre_gate(_happy_pre_input(caller_outcomes=outcomes))
        assert result.passed is False
        assert runner.state == STATE_DONE

    def test_mark_between_without_passing_pre_raises(self) -> None:
        runner = LogicianGateRunner()
        # State is PRE but no pre_gate_result — caller misuse
        with pytest.raises(RuntimeError):
            runner.mark_between()

    def test_mark_between_after_pre_fail_raises_mid_loop(self) -> None:
        runner = LogicianGateRunner()
        outcomes = _all_pre_pass()
        outcomes[1] = _fail_pre_outcome(1, "F-PRE-01.section_2_lock_missing")
        runner.run_pre_gate(_happy_pre_input(caller_outcomes=outcomes))
        # state is now DONE; mark_between should reject
        with pytest.raises(LogicianMidLoopCall):
            runner.mark_between()

    def test_run_pre_gate_twice_raises(self) -> None:
        runner = LogicianGateRunner()
        runner.run_pre_gate(_happy_pre_input())
        runner.mark_between()
        with pytest.raises(LogicianMidLoopCall):
            runner.run_pre_gate(_happy_pre_input())

    def test_run_post_gate_before_between_raises(self) -> None:
        runner = LogicianGateRunner()
        runner.run_pre_gate(_happy_pre_input())
        # state still PRE — mark_between not called
        with pytest.raises(LogicianMidLoopCall) as ei:
            runner.run_post_gate(_happy_post_input())
        assert ei.value.current_state == STATE_PRE

    def test_run_post_gate_in_pre_state_raises_pre_19(self) -> None:
        runner = LogicianGateRunner()
        with pytest.raises(LogicianMidLoopCall):
            runner.run_post_gate(_happy_post_input())

    def test_post_advances_to_done(self) -> None:
        runner = LogicianGateRunner()
        runner.run_pre_gate(_happy_pre_input())
        runner.mark_between()
        result = runner.run_post_gate(_happy_post_input())
        assert runner.state == STATE_DONE
        assert result.passed is True

    def test_run_post_gate_twice_raises(self) -> None:
        runner = LogicianGateRunner()
        runner.run_pre_gate(_happy_pre_input())
        runner.mark_between()
        runner.run_post_gate(_happy_post_input())
        with pytest.raises(LogicianMidLoopCall):
            runner.run_post_gate(_happy_post_input())


# ---------------------------------------------------------------------------
# POST-gate orchestration — happy path
# ---------------------------------------------------------------------------


def _runner_at_between() -> LogicianGateRunner:
    runner = LogicianGateRunner()
    runner.run_pre_gate(_happy_pre_input())
    runner.mark_between()
    return runner


class TestRunPostGateHappyPath:
    def test_all_13_pass(self) -> None:
        runner = _runner_at_between()
        result = runner.run_post_gate(_happy_post_input())
        assert result.passed is True
        assert result.failed_step_number is None
        assert result.failure_code is None
        assert len(result.completed_steps) == 13
        assert result.claim_evidence_map is not None
        assert result.underlying_post_gate_result is not None
        assert result.underlying_post_gate_result.success is True

    def test_strict_step_order_in_completed(self) -> None:
        runner = _runner_at_between()
        result = runner.run_post_gate(_happy_post_input())
        observed = tuple(s.step_number for s in result.completed_steps)
        assert observed == POST_GATE_STEP_ORDER


# ---------------------------------------------------------------------------
# POST-gate orchestration — caller outcome failures
# ---------------------------------------------------------------------------


class TestPostGateCallerFailures:
    def test_step_1_caller_fail_records_first_failure(self) -> None:
        outcomes = _all_caller_post_pass()
        outcomes[1] = _fail_post_step(1, F_POST_01_DRAFT_NOT_READY)
        runner = _runner_at_between()
        result = runner.run_post_gate(
            _happy_post_input(caller_step_outcomes=outcomes)
        )
        assert result.passed is False
        assert result.failed_step_number == 1
        assert result.failure_code == F_POST_01_DRAFT_NOT_READY
        # Sequence still walks all 13 steps (POST aggregates, not short-circuits)
        assert len(result.completed_steps) == 13

    def test_missing_caller_step_raises(self) -> None:
        outcomes = _all_caller_post_pass()
        del outcomes[12]
        runner = _runner_at_between()
        with pytest.raises(ValueError, match="step #12"):
            runner.run_post_gate(
                _happy_post_input(caller_step_outcomes=outcomes)
            )

    def test_caller_step_wrong_type_raises(self) -> None:
        outcomes = _all_caller_post_pass()
        outcomes[12] = "bogus"  # type: ignore[assignment]
        runner = _runner_at_between()
        with pytest.raises(TypeError, match="PostGateStepOutcome"):
            runner.run_post_gate(
                _happy_post_input(caller_step_outcomes=outcomes)
            )

    def test_caller_step_wrong_step_number_raises(self) -> None:
        outcomes = _all_caller_post_pass()
        outcomes[12] = _pass_post_step(13)
        runner = _runner_at_between()
        with pytest.raises(ValueError, match="step_number"):
            runner.run_post_gate(
                _happy_post_input(caller_step_outcomes=outcomes)
            )


# ---------------------------------------------------------------------------
# POST-gate orchestration — inline step failures
# ---------------------------------------------------------------------------


class TestPostGateInlineFailures:
    def test_step_4_unsourced_claim_fails(self) -> None:
        runner = _runner_at_between()
        result = runner.run_post_gate(
            _happy_post_input(
                claims=(_make_doc_sourced_claim(), _make_unsourced_claim())
            )
        )
        assert result.passed is False
        assert result.failed_step_number == 4
        assert result.failure_code == F_POST_11
        # F_POST_11 also surfaces from step 9 (Round 2 skeleton); deduped in failure_codes
        assert result.failure_codes.count(F_POST_11) == 1

    def test_step_5_dossier_failure_codes_propagate(self) -> None:
        runner = _runner_at_between()
        result = runner.run_post_gate(
            _happy_post_input(
                dossier_verify_failure_codes=(
                    "F-POST-08.dossier_s11c_fail_hash",
                ),
            )
        )
        assert result.passed is False
        assert result.failed_step_number == 5
        assert result.failure_code == "F-POST-08.dossier_s11c_fail_hash"
        assert "F-POST-08.dossier_s11c_fail_hash" in result.failure_codes

    def test_step_6_admin_risk_hard_block_fails(self) -> None:
        runner = _runner_at_between()
        result = runner.run_post_gate(
            _happy_post_input(admin_risk_hard_block_count=2)
        )
        assert result.passed is False
        assert result.failed_step_number == 6
        assert result.failure_code == F_POST_10
        # Round-2 skeleton also flags F-POST-10 at step 9; deduped
        assert result.failure_codes.count(F_POST_10) == 1

    def test_step_9_round2_skeleton_invoked(self) -> None:
        runner = _runner_at_between()
        result = runner.run_post_gate(_happy_post_input())
        # Underlying skeleton produces a populated map even on success
        assert result.underlying_post_gate_result is not None
        assert result.underlying_post_gate_result.claim_evidence_map is not None
        assert result.claim_evidence_map.unsourced_count == 0

    def test_invalid_admin_risk_count_raises(self) -> None:
        runner = _runner_at_between()
        with pytest.raises(ValueError):
            runner.run_post_gate(
                _happy_post_input(admin_risk_hard_block_count=-1)
            )


class TestPostGateInputValidation:
    def test_non_input_raises(self) -> None:
        runner = _runner_at_between()
        with pytest.raises(TypeError):
            runner.run_post_gate("bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# POST-gate aggregate failure semantics
# ---------------------------------------------------------------------------


class TestPostGateAggregate:
    def test_multiple_failures_aggregate(self) -> None:
        # Step 4 fails (UNSOURCED) AND step 6 fails (hard block)
        runner = _runner_at_between()
        result = runner.run_post_gate(
            _happy_post_input(
                claims=(_make_unsourced_claim(),),
                admin_risk_hard_block_count=1,
            )
        )
        assert result.passed is False
        # Earliest failure wins for failed_step_number
        assert result.failed_step_number == 4
        # Aggregate failure_codes contains both F-POST-10 and F-POST-11
        assert F_POST_10 in result.failure_codes
        assert F_POST_11 in result.failure_codes

    def test_completed_steps_marked_correctly(self) -> None:
        runner = _runner_at_between()
        outcomes = _all_caller_post_pass()
        outcomes[7] = _fail_post_step(7, "F-POST-07.structural_compliance_fail")
        result = runner.run_post_gate(
            _happy_post_input(caller_step_outcomes=outcomes)
        )
        # Step 7 marked failed
        step7 = next(s for s in result.completed_steps if s.step_number == 7)
        assert step7.passed is False
        # Step 6 (admin risk, no hard blocks) should pass
        step6 = next(s for s in result.completed_steps if s.step_number == 6)
        assert step6.passed is True
