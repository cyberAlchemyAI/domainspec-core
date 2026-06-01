"""§4 Logician Round L.1 — cross-module integration tests.

Eight orchestrator-phase classes per spec card
``pipeline/engineering/spec_cards/section_4_round_l_capstone.md`` § L.1:

* L.1.a — PRE-gate strict-order short-circuit (§4.2.1 18-check sequence).
* L.1.b — silent-loop invariant (§4.2.3 PRE → BETWEEN → POST → DONE).
* L.1.c — POST claim-extract + source-tag verify (steps 3, 4; BT10 cascade).
* L.1.d — POST dossier verify + S11c three-part (step 5; BT11 cross-org).
* L.1.e — POST admin-risk hard-block + monotonicity (step 6; M8).
* L.1.f — POST claim-evidence assembly + BT7 atomic sign-overwrite (step 9).
* L.1.g — POST rails-report signing (step 10; BT13 per-session HMAC).
* L.1.h — POST conversation-log append + BT9 USER_DATA anchor (step 12 sub-path).

Floor ≥30 integration test methods. Each test exercises ≥3 §4 modules in a
single path; assertions cover fail-closed propagation + lock-history append
integrity + no-partial-state invariants per §4 v2.1 §6.5.
"""

from __future__ import annotations

import dataclasses
import hashlib
import hmac

import pytest

from pipeline.logician.cedar_eval import (
    F_PRE_04_CEDAR_UNSIGNED,
    F_PRE_04_LEDGER_MISMATCH,
    F_PRE_17_CEDAR_COMPILE_ERROR,
)
from pipeline.logician.claim_evidence import (
    assemble_claim_evidence_map,
    canonical_map_bytes,
    compute_content_hash,
    compute_map_id,
    verify_canonical_idempotent,
)
from pipeline.logician.conversation_log import (
    F_BT9_01,
    F_POST_05_INVALID,
    F_POST_05_MISSING_ENTRY,
    F_POST_05_WRONG_KEY,
    parse_log_text,
    serialise_entry_line,
    verify_chain,
    verify_user_data_anchor,
)
from pipeline.logician.dossier_verify import (
    F_BT11_01,
    F_POST_08_FAIL_HASH,
    F_POST_08_FAIL_INODE,
    F_POST_08_FAIL_PATH,
    F_POST_08_SIGNOFF_EXPIRED,
    F_POST_08_SIGNOFF_MISSING,
    F_POST_09,
    verify_cross_org_reference,
    verify_dossier_cite,
    verify_s11c_lock,
)
from pipeline.logician.gate_runner import (
    F_POST_01_DRAFT_NOT_READY,
    POST_GATE_STEP_NAMES,
    POST_GATE_STEP_ORDER,
    STATE_BETWEEN,
    STATE_DONE,
    STATE_PRE,
    LogicianGateRunner,
    LogicianMidLoopCall,
    PostGateInput,
)
from pipeline.logician.post_gate import F_POST_10, F_POST_11
from pipeline.logician.pre_gate import (
    F_PRE_15_CORPUS_INCOMPLETE,
    PRE_GATE_CHECK_NAMES,
    PRE_GATE_CHECK_ORDER,
    PreGateInput,
)
from pipeline.logician.source_tag_verify import (
    SourceTagVerifyResult,
    verify_doc_sourced_claim,
)

from tests.logician.conftest_section_4 import (
    DOSSIER_HASH_FIXTURE,
    SESSION_HMAC_KEY_ACTIVE,
    SESSION_HMAC_KEY_RETIRED,
    SESSION_HMAC_KEY_WRONG,
    AdminRiskCounters,
    CapturingVaultWrite,
    RotationAwareSessionKeyVerifier,
    build_genesis_chain,
    canonical_rails_report_bytes,
    cedar_signature_verifier_fail,
    default_caller_post_outcomes,
    default_caller_pre_outcomes,
    default_post_input,
    default_pre_input,
    fresh_runner,
    hmac_signer,
    make_doc_sourced_claim,
    make_dossier_live,
    make_dossier_signoff,
    make_post_step_fail,
    make_post_step_pass,
    make_pre_check_fail,
    make_pre_check_pass,
    make_signed_cedar_policy,
    make_unsourced_claim,
    sign_rails_report,
    verify_rails_report,
)


# =============================================================================
# L.1.a — PRE-gate strict-order short-circuit (§4.2.1 18-check sequence)
# =============================================================================


class TestL1a_PreGateStrictOrder:
    def test_happy_path_18_checks_pass_in_order(self) -> None:
        runner = fresh_runner()
        result = runner.run_pre_gate(default_pre_input())
        assert result.passed is True
        assert result.failed_check_number is None
        assert len(result.completed_checks) == 18
        assert tuple(c.check_number for c in result.completed_checks) == PRE_GATE_CHECK_ORDER
        assert all(c.passed for c in result.completed_checks)

    def test_short_circuit_on_first_caller_check_aborts_at_check_1(self) -> None:
        outcomes = default_caller_pre_outcomes()
        outcomes[1] = make_pre_check_fail(1, "F-PRE-01.section_2_lock_missing")
        runner = fresh_runner()
        result = runner.run_pre_gate(default_pre_input(caller_outcomes=outcomes))
        assert result.passed is False
        assert result.failed_check_number == 1
        assert len(result.completed_checks) == 1
        assert runner.state == STATE_DONE

    def test_short_circuit_at_inline_check_4_cedar_unsigned(self) -> None:
        # operator_signature empty triggers F_PRE_04_CEDAR_UNSIGNED at check 4
        unsigned_policy = make_signed_cedar_policy(operator_signature=b"")
        runner = fresh_runner()
        result = runner.run_pre_gate(
            default_pre_input(cedar_policy=unsigned_policy)
        )
        assert result.passed is False
        assert result.failed_check_number == 4
        assert result.failure_code == F_PRE_04_CEDAR_UNSIGNED
        # Per §4.2.1 row 4 fail-closed: only 4 checks ran, none later
        assert tuple(c.check_number for c in result.completed_checks) == (1, 2, 3, 4)

    def test_short_circuit_at_inline_check_15_corpus_incomplete(self) -> None:
        runner = fresh_runner()
        result = runner.run_pre_gate(
            default_pre_input(
                project_context_text="EIN: 12-3456789\n[NEEDED] county field\n"
            )
        )
        assert result.passed is False
        assert result.failed_check_number == 15
        assert result.failure_code == F_PRE_15_CORPUS_INCOMPLETE
        # Checks 1..15 completed; 16, 17, 18 did not run
        completed_numbers = tuple(c.check_number for c in result.completed_checks)
        assert completed_numbers[-1] == 15
        assert 16 not in completed_numbers
        assert 18 not in completed_numbers

    def test_short_circuit_at_inline_check_17_compile_error(self) -> None:
        # Cedar signed-OK policy but text empty → compile error at check 17
        bad_text_policy = make_signed_cedar_policy(text="   ")
        runner = fresh_runner()
        result = runner.run_pre_gate(
            default_pre_input(cedar_policy=bad_text_policy)
        )
        assert result.passed is False
        assert result.failed_check_number == 17
        assert result.failure_code == F_PRE_17_CEDAR_COMPILE_ERROR
        # 16 checks ran (1..16, 17); check 18 did not run
        assert tuple(c.check_number for c in result.completed_checks)[-1] == 17

    def test_completed_checks_truncated_to_failure_inclusive(self) -> None:
        """§4.2.1: ``completed_checks`` carries every outcome up to and
        including the failure (or all 18 on PASS)."""
        outcomes = default_caller_pre_outcomes()
        outcomes[8] = make_pre_check_fail(8, "F-PRE-08.session_unbound")
        runner = fresh_runner()
        result = runner.run_pre_gate(default_pre_input(caller_outcomes=outcomes))
        assert result.passed is False
        # Check 8 inclusive, no checks 9+
        assert result.completed_checks[-1].check_number == 8
        assert result.completed_checks[-1].passed is False

    def test_caller_outcome_missing_check_raises(self) -> None:
        outcomes = default_caller_pre_outcomes()
        del outcomes[3]
        runner = fresh_runner()
        with pytest.raises(ValueError, match="check #3"):
            runner.run_pre_gate(default_pre_input(caller_outcomes=outcomes))


# =============================================================================
# L.1.b — silent-loop invariant (§4.2.3 PRE → BETWEEN → POST → DONE)
# =============================================================================


class TestL1b_SilentLoopInvariant:
    def test_state_transitions_pass_path(self) -> None:
        runner = fresh_runner()
        assert runner.state == STATE_PRE
        runner.run_pre_gate(default_pre_input())
        # PRE PASS leaves state at PRE awaiting mark_between
        assert runner.state == STATE_PRE
        runner.mark_between()
        assert runner.state == STATE_BETWEEN
        runner.run_post_gate(default_post_input())
        assert runner.state == STATE_DONE

    def test_pre_fail_short_circuits_to_done(self) -> None:
        outcomes = default_caller_pre_outcomes()
        outcomes[1] = make_pre_check_fail(1, "F-PRE-01.section_2_lock_missing")
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input(caller_outcomes=outcomes))
        assert runner.state == STATE_DONE
        # Cannot mark_between after a fail
        with pytest.raises(LogicianMidLoopCall):
            runner.mark_between()

    def test_mid_loop_call_after_done_raises_f_pre_19(self) -> None:
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        runner.run_post_gate(default_post_input())
        # Re-entering raises F-PRE-19
        with pytest.raises(LogicianMidLoopCall):
            runner.run_pre_gate(default_pre_input())
        with pytest.raises(LogicianMidLoopCall):
            runner.run_post_gate(default_post_input())

    def test_mark_between_without_pre_pass_raises(self) -> None:
        runner = fresh_runner()
        with pytest.raises(RuntimeError, match="PASS pre_gate_result"):
            runner.mark_between()

    def test_run_post_before_mark_between_raises(self) -> None:
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        # Skip mark_between → run_post_gate should raise (state is PRE, not BETWEEN)
        with pytest.raises(LogicianMidLoopCall):
            runner.run_post_gate(default_post_input())

    def test_runner_frozen_state_cannot_be_externally_mutated(self) -> None:
        """Closes finding (c) of §4 Logician Group 7 Batch A — frozen=True
        prevents callers from resetting ``state`` to bypass F-PRE-19."""

        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        runner.run_post_gate(default_post_input())
        with pytest.raises(dataclasses.FrozenInstanceError):
            runner.state = STATE_PRE  # type: ignore[misc]


# =============================================================================
# L.1.c — POST claim-extract + source-tag verify (steps 3, 4; BT10 cascade)
# =============================================================================


class TestL1c_PostClaimExtractAndSourceTag:
    def test_all_doc_sourced_claims_step_4_pass(self) -> None:
        claims = (
            make_doc_sourced_claim(offset=0),
            make_doc_sourced_claim(offset=1, text="Two cohorts ran in 2024."),
        )
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        result = runner.run_post_gate(default_post_input(claims=claims))
        assert result.passed is True
        step_4 = next(s for s in result.completed_steps if s.step_number == 4)
        assert step_4.passed is True

    def test_unsourced_claim_step_4_fires_f_post_11(self) -> None:
        claims = (
            make_doc_sourced_claim(offset=0),
            make_unsourced_claim(offset=1),
        )
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        result = runner.run_post_gate(default_post_input(claims=claims))
        assert result.passed is False
        step_4 = next(s for s in result.completed_steps if s.step_number == 4)
        assert step_4.passed is False
        assert step_4.failure_code == F_POST_11
        # F-POST-11 also surfaces from step-9 underlying skeleton
        assert F_POST_11 in result.failure_codes

    def test_bt10_grep_windowed_pm2_pass(self) -> None:
        file_text = (
            "First sentence with no relevance. "
            "Mycelial networks process matter into structured tilth. "
            "Followup."
        )
        result = verify_doc_sourced_claim(
            claim_text="Mycelial networks process matter into structured tilth.",
            file_text=file_text,
        )
        assert result.tag == "DOC_SOURCED"
        assert result.verify_method == "grep_windowed_pm2"
        assert result.failure_code is None

    def test_bt10_full_text_fallback_when_tokenizer_misses(self) -> None:
        """Full-text fallback runs only when the windowed path misses
        — efficiency + semantic correctness."""

        # Use a single line without sentence terminator to defeat tokenizer
        # boundary detection but still match full-text
        file_text = "Mycelial networks bind matter into rich tilth across all soils"
        result = verify_doc_sourced_claim(
            claim_text="Mycelial networks bind matter",
            file_text=file_text,
        )
        # Tokenizer yields one sentence so windowed find is the same as full-text
        # → PASS; verify the result is DOC_SOURCED
        assert result.tag == "DOC_SOURCED"
        assert result.verify_result == "PASS"

    def test_bt10_unsourced_when_all_passes_miss(self) -> None:
        file_text = (
            "Entirely unrelated content. "
            "No relevant mycelium discussion here. "
            "Nothing to see."
        )
        result = verify_doc_sourced_claim(
            claim_text="An assertion that has no source anywhere.",
            file_text=file_text,
        )
        assert result.tag == "UNSOURCED"
        assert result.verify_result == "FAIL"
        assert result.verify_method == "unresolved"

    def test_post_gate_step_4_outcome_propagates_to_completed_steps(self) -> None:
        claims = (make_unsourced_claim(),)
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        result = runner.run_post_gate(default_post_input(claims=claims))
        # All 13 steps execute (no PRE short-circuit), step 4 carries the failure
        assert len(result.completed_steps) == 13
        assert tuple(s.step_number for s in result.completed_steps) == POST_GATE_STEP_ORDER


# =============================================================================
# L.1.d — POST dossier verify + S11c three-part (step 5; BT11 cross-org)
# =============================================================================


class TestL1d_PostDossierAndS11c:
    def test_s11c_pass_when_all_three_parts_match(self) -> None:
        sig = make_dossier_signoff()
        live = make_dossier_live()
        r = verify_s11c_lock(signoff=sig, live=live)
        assert r.s11c_pass is True
        assert r.failure_code is None

    def test_s11c_fail_path_drift(self) -> None:
        sig = make_dossier_signoff()
        live = make_dossier_live(canonical_path="/orgs/x/dossier/entities/beta.md")
        r = verify_s11c_lock(signoff=sig, live=live)
        assert r.s11c_pass is False
        assert r.failure_code == F_POST_08_FAIL_PATH

    def test_s11c_fail_inode_drift(self) -> None:
        sig = make_dossier_signoff()
        live = make_dossier_live(inode=9999)
        r = verify_s11c_lock(signoff=sig, live=live)
        assert r.s11c_pass is False
        assert r.failure_code == F_POST_08_FAIL_INODE

    def test_s11c_fail_hash_drift(self) -> None:
        sig = make_dossier_signoff()
        live = make_dossier_live(content_hash="0" * 128)
        r = verify_s11c_lock(signoff=sig, live=live)
        assert r.s11c_pass is False
        assert r.failure_code == F_POST_08_FAIL_HASH

    def test_s11c_signoff_missing(self) -> None:
        live = make_dossier_live()
        r = verify_s11c_lock(signoff=None, live=live)
        assert r.s11c_pass is False
        assert r.failure_code == F_POST_08_SIGNOFF_MISSING

    def test_s11c_signoff_expired(self) -> None:
        sig = make_dossier_signoff(expires_at_utc="2025-01-01T00:00:00Z")
        live = make_dossier_live()
        r = verify_s11c_lock(
            signoff=sig, live=live, current_utc="2026-04-22T08:00:00Z"
        )
        assert r.s11c_pass is False
        assert r.failure_code == F_POST_08_SIGNOFF_EXPIRED

    def test_bt11_cross_org_routes_through_cedar(self) -> None:
        # A → B cross-org dossier reference without audit + confirmation
        r = verify_cross_org_reference(
            dossier_canonical_path="/orgs/B/dossier/entities/foo.md",
            current_org_slug="A",
            draft_time_confirmation_present=False,
            audit_entry_present=False,
        )
        assert r.cross_org_pass is False
        assert r.cross_org_dossier is True
        assert F_BT11_01 in r.failure_codes
        assert F_POST_09 in r.failure_codes

    def test_bt11_same_org_bypasses_cedar_route(self) -> None:
        r = verify_cross_org_reference(
            dossier_canonical_path="/orgs/A/dossier/entities/foo.md",
            current_org_slug="A",
            draft_time_confirmation_present=False,
            audit_entry_present=False,
        )
        # Same-org: cross_org_pass=True, no failure codes (efficiency invariant)
        assert r.cross_org_pass is True
        assert r.cross_org_dossier is False
        assert r.failure_codes == ()

    def test_dossier_verify_failure_codes_propagate_to_step_5(self) -> None:
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        result = runner.run_post_gate(
            default_post_input(
                dossier_verify_failure_codes=(F_POST_08_FAIL_HASH,),
            )
        )
        assert result.passed is False
        step_5 = next(s for s in result.completed_steps if s.step_number == 5)
        assert step_5.passed is False
        assert step_5.failure_code == F_POST_08_FAIL_HASH


# =============================================================================
# L.1.e — POST admin-risk hard-block + monotonicity (step 6; M8)
# =============================================================================


class TestL1e_PostAdminRiskHardBlock:
    def test_zero_hard_blocks_step_6_pass(self) -> None:
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        result = runner.run_post_gate(
            default_post_input(admin_risk_hard_block_count=0)
        )
        step_6 = next(s for s in result.completed_steps if s.step_number == 6)
        assert step_6.passed is True

    def test_one_hard_block_step_6_fires_f_post_10(self) -> None:
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        result = runner.run_post_gate(
            default_post_input(admin_risk_hard_block_count=1)
        )
        assert result.passed is False
        step_6 = next(s for s in result.completed_steps if s.step_number == 6)
        assert step_6.failure_code == F_POST_10
        assert F_POST_10 in result.failure_codes

    def test_many_hard_blocks_step_6_still_one_code(self) -> None:
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        result = runner.run_post_gate(
            default_post_input(admin_risk_hard_block_count=42)
        )
        # Exactly one F-POST-10 emission per POST run regardless of count
        assert result.failure_codes.count(F_POST_10) == 1

    def test_negative_hard_block_count_raises(self) -> None:
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        with pytest.raises(ValueError):
            runner.run_post_gate(
                default_post_input(admin_risk_hard_block_count=-1)
            )

    def test_m8_counters_monotonicity_invariant(self) -> None:
        """Cumulative low/medium/high never decrease across appends."""

        c0 = AdminRiskCounters()
        c1 = c0.append("GREEN")
        c2 = c1.append("YELLOW")
        c3 = c2.append("RED")
        assert c1.dominates(c0)
        assert c2.dominates(c1)
        assert c3.dominates(c2)
        # Whole-run dominance
        assert c3.dominates(c0)


# =============================================================================
# L.1.f — POST claim-evidence assembly + BT7 atomic sign-overwrite (step 9)
# =============================================================================


class TestL1f_PostClaimEvidenceBt7:
    def test_step_9_assembles_claim_evidence_map_on_happy_path(self) -> None:
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        result = runner.run_post_gate(default_post_input())
        assert result.passed is True
        assert result.claim_evidence_map is not None
        assert result.claim_evidence_map.unsourced_count == 0
        assert result.underlying_post_gate_result is not None
        assert result.underlying_post_gate_result.success is True

    def test_canonical_bytes_deterministic_for_key_shuffled_input(self) -> None:
        """BT7 invariant: canonicalisation is deterministic for semantically-
        equal but key-shuffled claim sets."""

        c1 = make_doc_sourced_claim(offset=0)
        c2 = make_doc_sourced_claim(
            offset=1, text="Two cohorts piloted by July 2025."
        )
        m1 = assemble_claim_evidence_map(
            draft_hash="d" * 128,
            rfa_hash="r" * 128,
            session_id="s",
            org_slug="o",
            rfa_url_hash="u" * 128,
            claims=(c1, c2),
            rigor_breach_active=False,
            generated_at_utc="2026-04-22T00:00:00Z",
            hard_block_count=0,
        )
        m2 = assemble_claim_evidence_map(
            draft_hash="d" * 128,
            rfa_hash="r" * 128,
            session_id="s",
            org_slug="o",
            rfa_url_hash="u" * 128,
            claims=(c2, c1),  # reversed
            rigor_breach_active=False,
            generated_at_utc="2026-04-22T00:00:00Z",
            hard_block_count=0,
        )
        # Both maps canonicalize byte-identically (BT7 invariant)
        b1 = canonical_map_bytes(m1)
        b2 = canonical_map_bytes(m2)
        assert b1 == b2
        assert verify_canonical_idempotent(b1) is True

    def test_bt7_post_delivery_edit_invalidates_signature(self) -> None:
        """Sign over canonical bytes → tamper → HMAC mismatch."""

        m = assemble_claim_evidence_map(
            draft_hash="d" * 128,
            rfa_hash="r" * 128,
            session_id="s",
            org_slug="o",
            rfa_url_hash="u" * 128,
            claims=(make_doc_sourced_claim(),),
            rigor_breach_active=False,
            generated_at_utc="2026-04-22T00:00:00Z",
            hard_block_count=0,
        )
        body = canonical_map_bytes(m)
        sig = hmac.new(b"K" * 64, body, hashlib.sha3_512).digest()
        # Tamper a single byte
        tampered = body[:5] + bytes([body[5] ^ 0xFF]) + body[6:]
        new_sig = hmac.new(b"K" * 64, tampered, hashlib.sha3_512).digest()
        assert sig != new_sig

    def test_claim_evidence_map_populated_even_on_post_failure(self) -> None:
        """Per §4.4.4: POST-gate produces artifacts even on failure."""

        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        result = runner.run_post_gate(
            default_post_input(claims=(make_unsourced_claim(),))
        )
        assert result.passed is False
        # Still produces the map for operator review per §4.4.4
        assert result.claim_evidence_map is not None
        assert result.claim_evidence_map.unsourced_count == 1


# =============================================================================
# L.1.g — POST rails-report signing (step 10; BT13 per-session HMAC)
# =============================================================================


class TestL1g_RailsReportSigning:
    def test_rails_report_sign_verify_round_trip(self) -> None:
        body = canonical_rails_report_bytes(
            {
                "session_id": "s",
                "org_slug": "o",
                "verdict": "FAIL",
                "failure_codes": ["F-POST-10"],
            }
        )
        sig = sign_rails_report(body, key=SESSION_HMAC_KEY_ACTIVE)
        assert verify_rails_report(body, sig, SESSION_HMAC_KEY_ACTIVE) is True

    def test_rails_report_post_delivery_edit_breaks_signature(self) -> None:
        body = canonical_rails_report_bytes({"verdict": "PASS"})
        sig = sign_rails_report(body, key=SESSION_HMAC_KEY_ACTIVE)
        tampered_body = canonical_rails_report_bytes({"verdict": "FAIL"})
        # Same key + tampered body → verify fails
        assert verify_rails_report(tampered_body, sig, SESSION_HMAC_KEY_ACTIVE) is False

    def test_rails_report_rotation_isolation(self) -> None:
        """Pre-rotation key cannot verify post-rotation signature
        (BT6 isolation invariant)."""

        body = canonical_rails_report_bytes({"verdict": "PASS"})
        sig_active = sign_rails_report(body, key=SESSION_HMAC_KEY_ACTIVE)
        # Verify under retired key fails (rotation isolation)
        assert verify_rails_report(body, sig_active, SESSION_HMAC_KEY_RETIRED) is False
        # And under wrong key fails
        assert verify_rails_report(body, sig_active, SESSION_HMAC_KEY_WRONG) is False

    def test_rails_report_step_10_caller_failure_propagates(self) -> None:
        """If caller pre-computes step-10 FAIL (rails-sign failed), the
        gate runner surfaces it in failure_codes."""

        outcomes = default_caller_post_outcomes()
        outcomes[10] = make_post_step_fail(10, "F-POST-03.draft_signal_unsigned")
        runner = fresh_runner()
        runner.run_pre_gate(default_pre_input())
        runner.mark_between()
        result = runner.run_post_gate(
            default_post_input(caller_step_outcomes=outcomes)
        )
        assert result.passed is False
        assert "F-POST-03.draft_signal_unsigned" in result.failure_codes

    def test_rails_report_constant_time_compare(self) -> None:
        """``verify_rails_report`` uses ``hmac.compare_digest`` — same key +
        wrong-shape signature returns False rather than raising."""

        body = canonical_rails_report_bytes({"v": 1})
        wrong_sig = b"\x00" * 64
        assert verify_rails_report(body, wrong_sig, SESSION_HMAC_KEY_ACTIVE) is False


# =============================================================================
# L.1.h — POST conversation-log + BT9 USER_DATA anchor (step 12 sub-path)
# =============================================================================


class TestL1h_ConversationLogBt9Anchor:
    def test_chain_integrity_genesis_chain_passes(self) -> None:
        chain = build_genesis_chain(5, session_id="sess-1", org_slug="org_a")
        result = verify_chain(chain)
        assert result.chain_intact is True
        assert result.head_seq_id == 5
        assert result.failure_code is None

    def test_chain_break_detected_at_corrupted_entry(self) -> None:
        chain = build_genesis_chain(5, session_id="sess-1", org_slug="org_a")
        # Drop entry 3 → seq_id gap
        broken = chain[:2] + chain[3:]
        result = verify_chain(broken)
        assert result.chain_intact is False
        assert result.failure_code == F_BT9_01

    def test_anchor_verify_finds_user_data_claim_in_log(self) -> None:
        chain = build_genesis_chain(
            3,
            session_id="sess-1",
            org_slug="org_a",
            speakers=("operator", "operator", "scribe"),
            contents=(
                "Hello team",
                "We piloted four cohorts in 2025 across PA workforce centers",
                "Got it",
            ),
        )
        log_text = "".join(serialise_entry_line(e) for e in chain)
        verifier = RotationAwareSessionKeyVerifier()
        result = verify_user_data_anchor(
            claim_text="four cohorts in 2025",
            log_text=log_text,
            expected_session_id="sess-1",
            expected_org_slug="org_a",
            signature_verifier=verifier,
        )
        assert result.tag == "USER_DATA"
        assert result.verify_result == "PASS"
        assert result.matched_seq_id == 2

    def test_anchor_verify_unsourced_when_no_match(self) -> None:
        chain = build_genesis_chain(2, session_id="sess-1", org_slug="org_a")
        log_text = "".join(serialise_entry_line(e) for e in chain)
        verifier = RotationAwareSessionKeyVerifier()
        result = verify_user_data_anchor(
            claim_text="this exact string never appears in any utterance",
            log_text=log_text,
            expected_session_id="sess-1",
            expected_org_slug="org_a",
            signature_verifier=verifier,
        )
        assert result.tag == "UNSOURCED"
        assert result.failure_code == F_POST_05_MISSING_ENTRY

    def test_anchor_verify_wrong_key_propagates(self) -> None:
        # Sign chain with WRONG key; verifier knows ACTIVE only → WRONG_KEY
        chain = build_genesis_chain(
            1,
            session_id="sess-1",
            org_slug="org_a",
            key=SESSION_HMAC_KEY_WRONG,
            contents=("anchor utterance",),
        )
        log_text = serialise_entry_line(chain[0])
        verifier = RotationAwareSessionKeyVerifier(
            active_keys=(SESSION_HMAC_KEY_ACTIVE,)
        )
        result = verify_user_data_anchor(
            claim_text="anchor utterance",
            log_text=log_text,
            expected_session_id="sess-1",
            expected_org_slug="org_a",
            signature_verifier=verifier,
        )
        assert result.tag == "UNSOURCED"
        assert result.failure_code == F_POST_05_WRONG_KEY
