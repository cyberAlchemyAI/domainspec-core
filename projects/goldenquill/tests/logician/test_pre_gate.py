"""Tests for ``pipeline.logician.pre_gate``.

Round 6 capstone — strict-order 18-check PRE-gate orchestrator. Tests cover
inline-evaluated check predicates, caller-outcome wiring, strict-order
short-circuit semantics, and result shape invariants.
"""

from __future__ import annotations

import dataclasses

import pytest

from pipeline.logician.cedar_eval import CedarPolicy
from pipeline.logician.dossier_verify import F_PRE_14_DOSSIER_UNSIGNED
from pipeline.logician.pre_gate import (
    F_PRE_04_CEDAR_UNSIGNED,
    F_PRE_04_LEDGER_MISMATCH,
    F_PRE_10_ADMIN_RISK_CHAIN_BREAK,
    F_PRE_15_CORPUS_INCOMPLETE,
    F_PRE_17_CEDAR_COMPILE_ERROR,
    F_PRE_19_LOGICIAN_MID_LOOP_CALL,
    PRE_GATE_CHECK_NAMES,
    PRE_GATE_CHECK_ORDER,
    CheckOutcome,
    PreGateInput,
    PreGateResult,
    evaluate_check_04_cedar_policy_signed,
    evaluate_check_10_admin_risk_ledger,
    evaluate_check_14_dossier_signoffs_present,
    evaluate_check_15_corpus_complete,
    evaluate_check_17_cedar_policy_compiles,
    run_pre_gate,
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


def _pass_outcome(check_number: int) -> CheckOutcome:
    return CheckOutcome(
        check_number=check_number,
        check_name=PRE_GATE_CHECK_NAMES[check_number],
        passed=True,
        failure_code=None,
        failure_detail="",
    )


def _fail_outcome(check_number: int, code: str, detail: str = "fail") -> CheckOutcome:
    return CheckOutcome(
        check_number=check_number,
        check_name=PRE_GATE_CHECK_NAMES[check_number],
        passed=False,
        failure_code=code,
        failure_detail=detail,
    )


def _all_pass_caller_outcomes() -> dict[int, CheckOutcome]:
    return {n: _pass_outcome(n) for n in (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 16, 18)}


def _happy_input(**overrides) -> PreGateInput:
    base = dict(
        caller_outcomes=_all_pass_caller_outcomes(),
        cedar_policy=_policy(),
        cedar_expected_ledger_head="h" * 128,
        cedar_signature_verifier=lambda p: True,
        admin_risk_ok=True,
        admin_risk_sub_failure_code=None,
        admin_risk_failure_detail="",
        dossier_signoff_states=(("entity_a", True), ("entity_b", True)),
        project_context_text="EIN: 12-3456789\nUEI: ABCD\nAddress: 1 Main St\n",
    )
    base.update(overrides)
    return PreGateInput(**base)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


class TestConstants:
    def test_18_check_order(self) -> None:
        assert PRE_GATE_CHECK_ORDER == tuple(range(1, 19))
        assert len(PRE_GATE_CHECK_ORDER) == 18

    def test_check_names_complete(self) -> None:
        assert set(PRE_GATE_CHECK_NAMES.keys()) == set(PRE_GATE_CHECK_ORDER)

    def test_pre_19_mid_loop_pinned(self) -> None:
        assert F_PRE_19_LOGICIAN_MID_LOOP_CALL == "F-PRE-19.logician_mid_loop_call"

    def test_pre_15_pinned(self) -> None:
        assert F_PRE_15_CORPUS_INCOMPLETE == "F-PRE-15.corpus_incomplete"


# ---------------------------------------------------------------------------
# Result + outcome shapes
# ---------------------------------------------------------------------------


class TestResultShapes:
    def test_check_outcome_frozen_kw_only(self) -> None:
        o = _pass_outcome(1)
        assert dataclasses.is_dataclass(o)
        with pytest.raises(dataclasses.FrozenInstanceError):
            o.passed = False  # type: ignore[misc]

    def test_pre_gate_result_frozen_kw_only(self) -> None:
        r = PreGateResult(
            passed=True,
            failed_check_number=None,
            failure_code=None,
            failure_detail="",
            completed_checks=(),
        )
        assert dataclasses.is_dataclass(r)
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.passed = False  # type: ignore[misc]

    def test_pre_gate_input_frozen_kw_only(self) -> None:
        i = _happy_input()
        assert dataclasses.is_dataclass(i)
        with pytest.raises(dataclasses.FrozenInstanceError):
            i.project_context_text = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Inline check predicates
# ---------------------------------------------------------------------------


class TestEvaluateCheck15CorpusComplete:
    def test_clean_pass(self) -> None:
        out = evaluate_check_15_corpus_complete("EIN: 12-3456789\n")
        assert out.passed is True
        assert out.check_number == 15

    def test_one_needed_fails(self) -> None:
        out = evaluate_check_15_corpus_complete("EIN: [NEEDED]\n")
        assert out.passed is False
        assert out.failure_code == F_PRE_15_CORPUS_INCOMPLETE
        assert "1" in out.failure_detail

    def test_multiple_needed_count(self) -> None:
        out = evaluate_check_15_corpus_complete("[NEEDED] x [NEEDED] y [NEEDED]")
        assert out.passed is False
        assert "3" in out.failure_detail

    def test_case_sensitive(self) -> None:
        # lowercase [needed] is NOT a violation per blueprint §4.2.2
        out = evaluate_check_15_corpus_complete("EIN: [needed]\n")
        assert out.passed is True

    def test_non_str_raises(self) -> None:
        with pytest.raises(TypeError):
            evaluate_check_15_corpus_complete(123)  # type: ignore[arg-type]


class TestEvaluateCheck17CedarPolicyCompiles:
    def test_happy_pass(self) -> None:
        out = evaluate_check_17_cedar_policy_compiles(_policy())
        assert out.passed is True

    def test_unknown_name_fails(self) -> None:
        out = evaluate_check_17_cedar_policy_compiles(_policy(name="bogus"))
        assert out.passed is False
        assert out.failure_code == F_PRE_17_CEDAR_COMPILE_ERROR

    def test_empty_text_fails(self) -> None:
        out = evaluate_check_17_cedar_policy_compiles(_policy(text="   "))
        assert out.passed is False
        assert out.failure_code == F_PRE_17_CEDAR_COMPILE_ERROR


class TestEvaluateCheck04CedarPolicySigned:
    def test_happy_pass(self) -> None:
        out = evaluate_check_04_cedar_policy_signed(
            _policy(),
            expected_ledger_head="h" * 128,
            signature_verifier=lambda p: True,
        )
        assert out.passed is True

    def test_unsigned_fails(self) -> None:
        out = evaluate_check_04_cedar_policy_signed(
            _policy(sig=b""),
            expected_ledger_head="h" * 128,
            signature_verifier=lambda p: True,
        )
        assert out.passed is False
        assert out.failure_code == F_PRE_04_CEDAR_UNSIGNED

    def test_ledger_mismatch_fails(self) -> None:
        out = evaluate_check_04_cedar_policy_signed(
            _policy(head="h" * 128),
            expected_ledger_head="z" * 128,
            signature_verifier=lambda p: True,
        )
        assert out.passed is False
        assert out.failure_code == F_PRE_04_LEDGER_MISMATCH

    def test_signature_verifier_returns_false(self) -> None:
        out = evaluate_check_04_cedar_policy_signed(
            _policy(),
            expected_ledger_head="h" * 128,
            signature_verifier=lambda p: False,
        )
        assert out.passed is False
        assert out.failure_code == F_PRE_04_CEDAR_UNSIGNED


class TestEvaluateCheck14DossierSignoffsPresent:
    def test_all_signed_pass(self) -> None:
        out = evaluate_check_14_dossier_signoffs_present(
            (("entity_a", True), ("entity_b", True))
        )
        assert out.passed is True

    def test_empty_tuple_pass(self) -> None:
        out = evaluate_check_14_dossier_signoffs_present(())
        assert out.passed is True

    def test_one_unsigned_fails_with_slug_listed(self) -> None:
        out = evaluate_check_14_dossier_signoffs_present(
            (("entity_a", True), ("entity_b", False))
        )
        assert out.passed is False
        assert out.failure_code == F_PRE_14_DOSSIER_UNSIGNED
        assert "entity_b" in out.failure_detail

    def test_multiple_unsigned_sorted(self) -> None:
        out = evaluate_check_14_dossier_signoffs_present(
            (("zebra", False), ("alpha", False), ("bravo", True))
        )
        assert out.passed is False
        assert out.failure_detail.index("alpha") < out.failure_detail.index("zebra")

    def test_non_tuple_raises(self) -> None:
        with pytest.raises(TypeError):
            evaluate_check_14_dossier_signoffs_present(
                [("a", True)]  # type: ignore[arg-type]
            )


class TestEvaluateCheck10AdminRiskLedger:
    def test_ok_pass(self) -> None:
        out = evaluate_check_10_admin_risk_ledger(
            ok=True, sub_failure_code=None, failure_detail=""
        )
        assert out.passed is True

    def test_chain_break_fail(self) -> None:
        out = evaluate_check_10_admin_risk_ledger(
            ok=False,
            sub_failure_code=F_PRE_10_ADMIN_RISK_CHAIN_BREAK,
            failure_detail="hash mismatch at seq 5",
        )
        assert out.passed is False
        assert out.failure_code == F_PRE_10_ADMIN_RISK_CHAIN_BREAK
        assert "seq 5" in out.failure_detail


# ---------------------------------------------------------------------------
# Orchestrator: run_pre_gate
# ---------------------------------------------------------------------------


class TestRunPreGateHappyPath:
    def test_all_18_pass(self) -> None:
        result = run_pre_gate(_happy_input())
        assert result.passed is True
        assert result.failed_check_number is None
        assert result.failure_code is None
        assert len(result.completed_checks) == 18
        for outcome in result.completed_checks:
            assert outcome.passed is True

    def test_strict_order_in_completed_checks(self) -> None:
        result = run_pre_gate(_happy_input())
        observed = tuple(o.check_number for o in result.completed_checks)
        assert observed == PRE_GATE_CHECK_ORDER


class TestRunPreGateShortCircuit:
    def test_check_1_fail_aborts_immediately(self) -> None:
        outcomes = _all_pass_caller_outcomes()
        outcomes[1] = _fail_outcome(1, "F-PRE-01.section_2_lock_missing")
        result = run_pre_gate(_happy_input(caller_outcomes=outcomes))
        assert result.passed is False
        assert result.failed_check_number == 1
        assert result.failure_code == "F-PRE-01.section_2_lock_missing"
        assert len(result.completed_checks) == 1

    def test_check_4_inline_fail_aborts(self) -> None:
        result = run_pre_gate(
            _happy_input(cedar_policy=_policy(sig=b""))
        )
        assert result.passed is False
        assert result.failed_check_number == 4
        assert result.failure_code == F_PRE_04_CEDAR_UNSIGNED
        # Checks 1-3 ran before 4
        assert len(result.completed_checks) == 4

    def test_check_10_inline_fail_aborts(self) -> None:
        result = run_pre_gate(
            _happy_input(
                admin_risk_ok=False,
                admin_risk_sub_failure_code=F_PRE_10_ADMIN_RISK_CHAIN_BREAK,
                admin_risk_failure_detail="broken",
            )
        )
        assert result.passed is False
        assert result.failed_check_number == 10
        assert result.failure_code == F_PRE_10_ADMIN_RISK_CHAIN_BREAK
        assert len(result.completed_checks) == 10

    def test_check_14_inline_fail_aborts(self) -> None:
        result = run_pre_gate(
            _happy_input(dossier_signoff_states=(("entity_a", False),))
        )
        assert result.passed is False
        assert result.failed_check_number == 14
        assert result.failure_code == F_PRE_14_DOSSIER_UNSIGNED

    def test_check_15_inline_fail_aborts(self) -> None:
        result = run_pre_gate(
            _happy_input(project_context_text="EIN: [NEEDED]\n")
        )
        assert result.passed is False
        assert result.failed_check_number == 15
        assert result.failure_code == F_PRE_15_CORPUS_INCOMPLETE

    def test_check_17_inline_fail_aborts(self) -> None:
        # Check 17 needs a compile-fail policy that ALSO survives check 4 (signed).
        # A policy with empty text fails both, but check 4 fires first.
        # An invalid name with valid signature fails check 17 only — but check 4
        # also rejects the unknown name? No — check 4 only verifies signature
        # and ledger head, not the compile. So unknown-name + valid sig + valid
        # head passes check 4 and fails check 17.
        bad_policy = _policy(name="bogus_policy")
        result = run_pre_gate(_happy_input(cedar_policy=bad_policy))
        assert result.passed is False
        assert result.failed_check_number == 17
        assert result.failure_code == F_PRE_17_CEDAR_COMPILE_ERROR

    def test_caller_outcome_fail_at_18(self) -> None:
        outcomes = _all_pass_caller_outcomes()
        outcomes[18] = _fail_outcome(18, "F-PRE-18.scout_pre_verify_unsigned")
        result = run_pre_gate(_happy_input(caller_outcomes=outcomes))
        assert result.passed is False
        assert result.failed_check_number == 18
        assert len(result.completed_checks) == 18


class TestRunPreGateInputValidation:
    def test_non_input_raises(self) -> None:
        with pytest.raises(TypeError):
            run_pre_gate("bogus")  # type: ignore[arg-type]

    def test_missing_caller_outcome_raises(self) -> None:
        outcomes = _all_pass_caller_outcomes()
        del outcomes[7]
        with pytest.raises(ValueError, match="check #7"):
            run_pre_gate(_happy_input(caller_outcomes=outcomes))

    def test_caller_outcome_wrong_type_raises(self) -> None:
        outcomes = _all_pass_caller_outcomes()
        outcomes[7] = "bogus"  # type: ignore[assignment]
        with pytest.raises(TypeError, match="CheckOutcome"):
            run_pre_gate(_happy_input(caller_outcomes=outcomes))

    def test_caller_outcome_check_number_mismatch_raises(self) -> None:
        outcomes = _all_pass_caller_outcomes()
        outcomes[7] = _pass_outcome(8)  # wrong number
        with pytest.raises(ValueError, match="check_number"):
            run_pre_gate(_happy_input(caller_outcomes=outcomes))


class TestRunPreGateOrderPriority:
    def test_earliest_failure_wins(self) -> None:
        # Multiple checks fail simultaneously; orchestrator must report the
        # first one and short-circuit.
        outcomes = _all_pass_caller_outcomes()
        outcomes[2] = _fail_outcome(2, "F-PRE-02.router_yaml_unsigned")
        outcomes[6] = _fail_outcome(6, "F-PRE-06.trust_root_unsigned")
        result = run_pre_gate(
            _happy_input(
                caller_outcomes=outcomes,
                project_context_text="[NEEDED]",
                dossier_signoff_states=(("e", False),),
            )
        )
        assert result.failed_check_number == 2
        assert len(result.completed_checks) == 2
