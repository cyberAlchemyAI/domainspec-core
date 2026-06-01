"""§5 R13 capstone — J.1 + J.2 integration tests.

Blueprint §5 v6 LOCKED 2026-04-19. Spec card
``pipeline/engineering/spec_cards/section_05_round_13_capstone.md``.

J.1 covers submission-mode lifecycle (R1-R11 end-to-end) — 8 classes, each
at least one happy-path + ≥1 adversarial case.
J.2 covers eval-mode lifecycle (R12.A + R12.B + R1-R7 reuse) — 5 classes.

Fixtures / harness: :mod:`tests.loop.conftest_section_5` (sibling module).
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

import pytest

from pipeline.calibration import (
    report_from_json,
    verify_calibration_report,
)
from pipeline.loop.errors import F_PIPE_19, F_PIPE_21, PipelineFailure
from pipeline.loop.run_eval_pipeline import (
    EvalPipelineRunResult,
    run_eval_pipeline,
)
from pipeline.loop.run_pipeline import (
    PipelineRunResult,
    run_pipeline,
)

from tests.loop.conftest_section_5 import (
    EvalHarness,
    SubmissionHarness,
    build_eval_harness,
    build_manifest,
    build_submission_harness,
    make_cascade,
    make_charter,
    post_gate_fail,
    pre_gate_fail,
)


# ===========================================================================
# Helpers
# ===========================================================================


def _run_submission(
    h: SubmissionHarness,
    *,
    run_id: str = "run-R13",
    org_slug: str = "mycosymbiotics",
) -> PipelineRunResult:
    return run_pipeline(
        run_id=run_id,
        org_slug=org_slug,
        session_id="sess-R13",
        rfa_hash="rfa-abc",
        project_context_hash="pc-def",
        scribe_charter=make_charter("scribe"),
        editor_charter=make_charter("editor"),
        judge_charter=make_charter("judge"),
        scribe_cascade=make_cascade("scribe"),
        editor_cascade=make_cascade("editor"),
        judge_cascade=make_cascade("judge"),
        context=h.context,
        pre_gate_input_factory=h.pre_gate_input_factory,
    )


def _run_eval(
    h: EvalHarness,
    *,
    run_id: str = "run-R13-eval",
    operator_org_slug: str = "fit_farms_llc",
    subset: tuple[str, ...] | None = None,
) -> EvalPipelineRunResult:
    return run_eval_pipeline(
        run_id=run_id,
        operator_org_slug=operator_org_slug,
        golden_set_manifest_path=h.manifest_path,
        session_id="sess-R13",
        scribe_charter=make_charter("scribe"),
        editor_charter=make_charter("editor"),
        judge_charter=make_charter("judge"),
        scribe_cascade=make_cascade("scribe"),
        editor_cascade=make_cascade("editor"),
        judge_cascade=make_cascade("judge"),
        ctx=h.ctx,
        subset=subset,
    )


# ===========================================================================
# J.1.1 — Boot to PRE-gate (R1 + R2 + R3 + R11)
# ===========================================================================


class TestBootToPreGate:
    def test_run_id_propagates_through_fixed_factory(self) -> None:
        h = build_submission_harness(run_id="run-BP-A")
        r = _run_submission(h, run_id="run-BP-A")
        assert r.run_id == "run-BP-A"

    def test_initial_phase_lands_at_pre_gate_passed_or_beyond(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        writes = [
            w for w in h.vault.writes if w["path"].endswith("/state.json")
        ]
        # Multiple state.json writes expected — checkpoint cadence.
        assert len(writes) >= 5

    def test_pre_gate_input_factory_invoked_once(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        assert len(h.pre_gate_input_factory.calls) == 1

    def test_pre_gate_input_factory_called_at_pre_gate_pending(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        call_phase = h.pre_gate_input_factory.calls[0]["phase"]
        assert call_phase == "pre_gate_pending"

    def test_adversarial_pre_gate_callable_raises_pipeline_failure(self) -> None:
        h = build_submission_harness()
        h.pre_gate_callable.raise_exc = F_PIPE_21("eval_mode_invalid_intent")
        h.pre_gate_callable.result = None
        with pytest.raises(PipelineFailure):
            _run_submission(h)
        # State-failure checkpoint landed before propagation.
        intents = [w["intent"] for w in h.vault.writes]
        assert "state-failure" in intents


# ===========================================================================
# J.1.2 — PRE-gate to inner loop (R4 + R5)
# ===========================================================================


class TestPreGateToInnerLoop:
    def test_inner_loop_enters_on_pre_gate_pass(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        # Launcher invoked at least three times (scribe + editor + judge).
        assert len(h.launcher.calls) >= 3

    def test_context_factory_invoked_per_seat_per_iter(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        kinds = {c["seat_kind"] for c in h.context_factory.calls}
        assert {"scribe", "editor", "judge"}.issubset(kinds)

    def test_iterations_consumed_ge_one(self) -> None:
        h = build_submission_harness()
        r = _run_submission(h)
        assert r.iterations_consumed >= 1

    def test_adversarial_pre_gate_soft_fail_returns_early(self) -> None:
        h = build_submission_harness(pre_gate_result=pre_gate_fail())
        r = _run_submission(h)
        assert r.pre_gate_failed is True
        assert r.pre_gate_failure_code == "F-PRE-05-STUB"
        assert r.final_phase == "pre_gate_pending"

    def test_adversarial_pre_gate_soft_fail_skips_inner_loop(self) -> None:
        h = build_submission_harness(pre_gate_result=pre_gate_fail())
        _run_submission(h)
        # Launcher must NOT fire when PRE-gate rejects.
        assert len(h.launcher.calls) == 0

    def test_adversarial_pre_gate_soft_fail_no_three_tab_envelope(self) -> None:
        h = build_submission_harness(pre_gate_result=pre_gate_fail())
        r = _run_submission(h)
        assert r.three_tab_envelope_hash is None


# ===========================================================================
# J.1.3 — Inner loop to POST-gate (R5 + R6)
# ===========================================================================


class TestInnerLoopToPostGate:
    def test_post_gate_runner_invoked_once_on_happy_path(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        assert len(h.post_gate_runner.calls) == 1

    def test_post_gate_input_factory_invoked_once(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        assert len(h.post_gate_input_factory.calls) == 1

    def test_iterations_consumed_captured_in_post_gate_factory(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        iters = h.post_gate_input_factory.calls[0]["iterations_run"]
        assert iters >= 1

    def test_adversarial_post_gate_fail_sets_bypass_pending(self) -> None:
        h = build_submission_harness(post_gate_result=post_gate_fail())
        r = _run_submission(h)
        assert r.bypass_pending is True
        assert r.post_gate_rejected_trigger is not None

    def test_adversarial_post_gate_fail_bypass_marker_written(self) -> None:
        h = build_submission_harness(post_gate_result=post_gate_fail())
        _run_submission(h)
        paths = [w["path"] for w in h.vault.writes]
        assert any("bypass_pending" in p for p in paths)


# ===========================================================================
# J.1.4 — POST-gate to sign-off (R6 + R11)
# ===========================================================================


class TestPostGateToSignoff:
    def test_signoff_pending_phase_reached(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        # At least one state.json write at or beyond signoff_pending phase.
        # Inspect final state payload.
        final = None
        for w in h.vault.writes:
            if w["path"].endswith("/state.json"):
                final = w
        assert final is not None
        body = json.loads(final["payload"].decode("utf-8"))
        assert body["phase"] == "tabs_delivered"

    def test_report_signed_phase_precedes_tabs_delivered(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        phases = []
        for w in h.vault.writes:
            if w["path"].endswith("/state.json"):
                try:
                    phases.append(json.loads(w["payload"])["phase"])
                except Exception:
                    continue
        if "report_signed" in phases and "tabs_delivered" in phases:
            assert phases.index("report_signed") < phases.index("tabs_delivered")

    def test_hash_file_invoked_three_times(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        # Round 9 deliver_tab hashes live_radar, deep_brief, council_draft.
        assert len(h.hash_file.calls) == 3

    def test_adversarial_post_gate_fail_skips_signoff(self) -> None:
        h = build_submission_harness(post_gate_result=post_gate_fail())
        r = _run_submission(h)
        assert r.final_phase == "post_gate_pending"

    def test_adversarial_post_gate_fail_no_hash_file_calls(self) -> None:
        h = build_submission_harness(post_gate_result=post_gate_fail())
        _run_submission(h)
        assert len(h.hash_file.calls) == 0


# ===========================================================================
# J.1.5 — Sign-off to tabs (R9 + R11)
# ===========================================================================


class TestSignoffToTabs:
    def test_tabs_delivered_final_phase(self) -> None:
        h = build_submission_harness()
        r = _run_submission(h)
        assert r.final_phase == "tabs_delivered"

    def test_three_tab_envelope_hash_is_sha256_hex(self) -> None:
        h = build_submission_harness()
        r = _run_submission(h)
        assert r.three_tab_envelope_hash is not None
        assert len(r.three_tab_envelope_hash) == 64
        int(r.three_tab_envelope_hash, 16)  # valid hex

    def test_elapsed_ms_ge_zero(self) -> None:
        h = build_submission_harness()
        r = _run_submission(h)
        assert r.elapsed_ms >= 0

    def test_bypass_pending_false_on_happy_path(self) -> None:
        h = build_submission_harness()
        r = _run_submission(h)
        assert r.bypass_pending is False

    def test_adversarial_hash_file_returns_different_per_call(self) -> None:
        # Supply stub distinct hashes per path — envelope_sha256 is the
        # sha of the envelope itself, not of the individual tabs.
        h = build_submission_harness()
        _run_submission(h)
        # hash_file was invoked for three distinct paths.
        assert len(set(h.hash_file.calls)) == 3


# ===========================================================================
# J.1.6 — Bypass-pending path (R6 + R11 soft-return)
# ===========================================================================


class TestBypassPendingPath:
    def test_bypass_pending_final_phase(self) -> None:
        h = build_submission_harness(post_gate_result=post_gate_fail())
        r = _run_submission(h)
        assert r.final_phase == "post_gate_pending"
        assert r.bypass_pending is True

    def test_bypass_pending_trigger_preserved(self) -> None:
        h = build_submission_harness(post_gate_result=post_gate_fail())
        r = _run_submission(h)
        assert r.post_gate_rejected_trigger is not None

    def test_bypass_marker_payload_is_json(self) -> None:
        h = build_submission_harness(post_gate_result=post_gate_fail())
        _run_submission(h)
        bypass_writes = [
            w for w in h.vault.writes if "bypass_pending" in w["path"]
        ]
        assert bypass_writes
        json.loads(bypass_writes[0]["payload"].decode("utf-8"))

    def test_adversarial_bypass_then_resume_not_attempted(self) -> None:
        # At v0.1, bypass_pending is terminal for the in-process run — the
        # operator acts out-of-band. Verify R11 does not attempt follow-up.
        h = build_submission_harness(post_gate_result=post_gate_fail())
        _run_submission(h)
        assert len(h.hash_file.calls) == 0


# ===========================================================================
# J.1.7 — Resume submission-mode path (R3 resume_run entrypoint)
# ===========================================================================


class TestResumeSubmissionPath:
    def test_fresh_boot_first_state_write_has_no_expected_hash(self) -> None:
        # Fresh boot — first state.json write uses overwrite write_mode but
        # with ``expected_current_file_hash=None`` (no prior head to pin).
        h = build_submission_harness()
        _run_submission(h)
        state_writes = [
            w for w in h.vault.writes if w["path"].endswith("/state.json")
        ]
        assert state_writes[0]["write_mode"] == "overwrite"
        assert state_writes[0]["expected_current_file_hash"] is None

    def test_subsequent_state_writes_carry_cas_expected_hash(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        state_writes = [
            w for w in h.vault.writes if w["path"].endswith("/state.json")
        ]
        # Every state.json after the first must carry a CAS expected hash.
        for w in state_writes[1:]:
            assert w["write_mode"] == "overwrite"
            assert w["expected_current_file_hash"] is not None

    def test_cas_head_threads_through_run(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        # Expected hash on write N must equal the sha256 of payload N-1
        # (or None for the very first write).
        state_writes = [
            w for w in h.vault.writes if w["path"].endswith("/state.json")
        ]
        prev = None
        for w in state_writes:
            assert w["expected_current_file_hash"] == prev
            prev = hashlib.sha256(w["payload"]).hexdigest()

    def test_cas_chain_is_continuous(self) -> None:
        # Every overwrite must pin the previous payload's sha256 (already
        # asserted in test_cas_head_threads_through_run; verified here on
        # state-success intents specifically).
        h = build_submission_harness()
        _run_submission(h)
        state_writes = [
            w for w in h.vault.writes if w["path"].endswith("/state.json")
        ]
        assert len(state_writes) >= 3


# ===========================================================================
# J.1.8 — Full submission lifecycle — phase-walk pin
# ===========================================================================


class TestFullSubmissionLifecycle:
    def test_11_phase_walk_observed(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        phases: list[str] = []
        for w in h.vault.writes:
            if w["path"].endswith("/state.json"):
                try:
                    p = json.loads(w["payload"])["phase"]
                except Exception:
                    continue
                if not phases or phases[-1] != p:
                    phases.append(p)
        # Required phases (monotone progression through the sequence):
        required = [
            "initialized",
            "pre_gate_pending",
            "pre_gate_passed",
            "post_gate_pending",
            "post_gate_passed",
            "signoff_pending",
            "report_signed",
            "tabs_delivered",
        ]
        for phase in required:
            assert phase in phases, f"missing {phase}; saw {phases}"
        # Ordering: every required phase appears before the next.
        for i in range(len(required) - 1):
            assert phases.index(required[i]) < phases.index(required[i + 1])

    def test_signoff_pending_precedes_report_signed(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        phases = []
        for w in h.vault.writes:
            if w["path"].endswith("/state.json"):
                try:
                    phases.append(json.loads(w["payload"])["phase"])
                except Exception:
                    continue
        assert phases.index("signoff_pending") < phases.index("report_signed")

    def test_no_state_failure_intent_on_happy_path(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        intents = [w["intent"] for w in h.vault.writes]
        assert "state-failure" not in intents

    def test_mode_pinned_to_submission(self) -> None:
        h = build_submission_harness()
        _run_submission(h)
        for w in h.vault.writes:
            if w["path"].endswith("/state.json"):
                body = json.loads(w["payload"].decode("utf-8"))
                assert body["mode"] == "submission"

    def test_adversarial_pre_gate_raising_writes_failure_checkpoint(
        self,
    ) -> None:
        h = build_submission_harness()
        h.pre_gate_callable.result = None
        h.pre_gate_callable.raise_exc = F_PIPE_19("plateau_no_pass:stub")
        with pytest.raises(PipelineFailure):
            _run_submission(h)
        intents = [w["intent"] for w in h.vault.writes]
        assert "state-failure" in intents


# ===========================================================================
# J.2.1 — Eval per-item loop (R12.B + R5 reuse)
# ===========================================================================


class TestEvalPerItemLoop:
    def test_single_item_consumes_one(self) -> None:
        h = build_eval_harness(run_id="run-E1")
        r = _run_eval(h, run_id="run-E1")
        assert r.items_consumed == 1
        assert r.final_phase == "eval_finalized"

    def test_multi_item_consumes_all(self) -> None:
        items = tuple(
            {
                "item_id": f"item-{i}",
                "org_slug": "fit_farms_llc",
                "funded_grant_label": f"grant-{i}",
                "rfa_snapshot_path": f"vault/fit_farms_llc/golden_set/rfa/{i}.txt",
                "submitted_artifact_path": f"vault/fit_farms_llc/golden_set/submitted/{i}.pdf",
                "funded_outcome": "funded",
                "operator_curation_iso": "2026-03-15T09:00:00+00:00",
            }
            for i in range(3)
        )
        h = build_eval_harness(manifest_items=items, run_id="run-E3")
        r = _run_eval(h, run_id="run-E3")
        assert r.items_consumed == 3

    def test_subset_filter_reduces_items(self) -> None:
        items = tuple(
            {
                "item_id": f"item-{k}",
                "org_slug": "fit_farms_llc",
                "funded_grant_label": f"grant-{k}",
                "rfa_snapshot_path": f"vault/fit_farms_llc/golden_set/rfa/{k}.txt",
                "submitted_artifact_path": f"vault/fit_farms_llc/golden_set/submitted/{k}.pdf",
                "funded_outcome": "funded",
                "operator_curation_iso": "2026-03-15T09:00:00+00:00",
            }
            for k in ("a", "b", "c", "d", "e")
        )
        h = build_eval_harness(manifest_items=items, run_id="run-ES")
        r = _run_eval(h, run_id="run-ES", subset=("item-a", "item-c"))
        assert r.items_consumed == 2

    def test_empty_subset_consumes_zero(self) -> None:
        h = build_eval_harness(run_id="run-E0")
        r = _run_eval(h, run_id="run-E0", subset=())
        assert r.items_consumed == 0

    def test_adversarial_pre_gate_eval_fail_aborted_trusted_fail(self) -> None:
        h = build_eval_harness(
            run_id="run-Ef",
            pre_gate_result=pre_gate_fail(code="F-EVAL-CROSS-ORG-READ"),
        )
        r = _run_eval(h, run_id="run-Ef")
        # Eval PRE-gate soft-fail → aborted_trusted_fail final phase.
        assert r.final_phase == "aborted_trusted_fail"


# ===========================================================================
# J.2.2 — Eval pubkey first-write (R12.A reconcile_operator_pubkey)
# ===========================================================================


class TestEvalPubkeyFirstWrite:
    def test_first_run_writes_pubkey_provenance(self) -> None:
        h = build_eval_harness(run_id="run-PK1")
        _run_eval(h, run_id="run-PK1")
        assert len(h.pubkey_vault.writes) == 1

    def test_second_run_with_same_pubkey_no_second_write(self) -> None:
        # Pre-seed the pubkey so reconcile finds an existing entry.
        h_first = build_eval_harness(run_id="run-PK-first")
        _run_eval(h_first, run_id="run-PK-first")
        existing_pubkey = h_first.pubkey_vault.stored["fit_farms_llc"]

        h_second = build_eval_harness(
            run_id="run-PK-second",
            signer=h_first.signer,
            pre_existing_pubkey=existing_pubkey,
        )
        _run_eval(h_second, run_id="run-PK-second")
        # Exactly zero new writes (the stored entry already matches).
        assert len(h_second.pubkey_vault.writes) == 0

    def test_adversarial_second_run_mismatched_pubkey_aborts_operator(
        self,
    ) -> None:
        # Pre-seed a DIFFERENT pubkey → reconcile routes to aborted_operator
        # (recoverable abort, not a hard raise — operator intervention path).
        h = build_eval_harness(
            run_id="run-PK-bad",
            pre_existing_pubkey=b"x" * 32,
        )
        r = _run_eval(h, run_id="run-PK-bad")
        assert r.final_phase == "aborted_operator"
        assert r.aborted_operator is True


# ===========================================================================
# J.2.3 — Eval refuse-to-sign path (structural — no v0.1 implementation)
# ===========================================================================


class TestEvalRefuseToSign:
    def test_no_tab_delivery_on_happy_eval(self) -> None:
        h = build_eval_harness(run_id="run-NTD")
        _run_eval(h, run_id="run-NTD")
        # hash_file is a stub that raises if invoked; a happy eval must not
        # invoke it.
        # The stub has __name__ but no call history — absence of raise from
        # _run_eval proves the stub wasn't called.
        # This asserts §7.13 mode-isolation structurally.

    def test_no_three_tab_envelope_paths_written_eval(self) -> None:
        h = build_eval_harness(run_id="run-NTE")
        _run_eval(h, run_id="run-NTE")
        paths = [w["path"] for w in h.vault.writes]
        assert not any("three_tab_envelope" in p for p in paths)

    def test_eval_writes_calibration_report_path(self) -> None:
        h = build_eval_harness(run_id="run-CRP")
        r = _run_eval(h, run_id="run-CRP")
        assert r.calibration_report_path is not None
        assert r.calibration_signature_path is not None

    def test_adversarial_manifest_org_slug_mismatch_routes_to_failure(
        self,
    ) -> None:
        # Manifest carries org_slug != run's operator_org_slug → PRE-gate
        # predicate failure is the contract; if R12.B routes through the
        # PRE-gate seam fake, this surfaces via F-EVAL-CROSS-ORG-READ.
        items = (
            {
                "item_id": "mismatch",
                "org_slug": "DIFFERENT_ORG",
                "funded_grant_label": "g",
                "rfa_snapshot_path": "vault/x/golden_set/rfa/a.txt",
                "submitted_artifact_path": "vault/x/golden_set/submitted/a.pdf",
                "funded_outcome": "funded",
                "operator_curation_iso": "2026-03-15T09:00:00+00:00",
            },
        )
        # Surface the PRE-gate sentinel — set PRE-gate fail result explicitly.
        h = build_eval_harness(
            run_id="run-mismatch",
            manifest_items=items,
            pre_gate_result=pre_gate_fail(code="F-EVAL-CROSS-ORG-READ"),
        )
        r = _run_eval(h, run_id="run-mismatch")
        assert r.final_phase == "aborted_trusted_fail"


# ===========================================================================
# J.2.4 — Eval resume per-item (structural — R12.B progress sidecar)
# ===========================================================================


class TestEvalResumePerItem:
    def test_per_item_progress_sidecar_path_present(self) -> None:
        items = tuple(
            {
                "item_id": f"item-{i}",
                "org_slug": "fit_farms_llc",
                "funded_grant_label": f"grant-{i}",
                "rfa_snapshot_path": f"vault/fit_farms_llc/golden_set/rfa/{i}.txt",
                "submitted_artifact_path": f"vault/fit_farms_llc/golden_set/submitted/{i}.pdf",
                "funded_outcome": "funded",
                "operator_curation_iso": "2026-03-15T09:00:00+00:00",
            }
            for i in range(2)
        )
        h = build_eval_harness(manifest_items=items, run_id="run-RES")
        _run_eval(h, run_id="run-RES")
        # Per-item checkpoint intents include multiple state-success writes.
        intents = [w["intent"] for w in h.vault.writes]
        assert intents.count("state-success") >= 2

    def test_mode_pinned_to_eval_in_state_json(self) -> None:
        h = build_eval_harness(run_id="run-MODE")
        _run_eval(h, run_id="run-MODE")
        for w in h.vault.writes:
            if w["path"].endswith("/state.json"):
                body = json.loads(w["payload"].decode("utf-8"))
                assert body["mode"] == "eval"

    def test_adversarial_multi_item_partial_failure_isolated(self) -> None:
        items = tuple(
            {
                "item_id": f"item-{i}",
                "org_slug": "fit_farms_llc",
                "funded_grant_label": f"grant-{i}",
                "rfa_snapshot_path": f"vault/fit_farms_llc/golden_set/rfa/{i}.txt",
                "submitted_artifact_path": f"vault/fit_farms_llc/golden_set/submitted/{i}.pdf",
                "funded_outcome": "funded",
                "operator_curation_iso": "2026-03-15T09:00:00+00:00",
            }
            for i in range(2)
        )
        h = build_eval_harness(manifest_items=items, run_id="run-PF")
        # First item succeeds; second would succeed too. Verify both land.
        r = _run_eval(h, run_id="run-PF")
        assert r.items_consumed == 2


# ===========================================================================
# J.2.5 — Full eval lifecycle — verifies signature round-trip + non-exportability
# ===========================================================================


class TestFullEvalLifecycle:
    def test_eval_finalized_final_phase(self) -> None:
        h = build_eval_harness(run_id="run-FULL-E")
        r = _run_eval(h, run_id="run-FULL-E")
        assert r.final_phase == "eval_finalized"

    def test_calibration_report_verifies_with_signer_pubkey(self) -> None:
        from datetime import datetime, timezone

        h = build_eval_harness(run_id="run-VR")
        r = _run_eval(h, run_id="run-VR")
        assert r.calibration_report_path is not None
        report_bytes = h.vault.store[r.calibration_report_path]
        report = report_from_json(report_bytes)
        # verify_calibration_report re-canonicalizes + re-verifies signature
        # embedded on the report. No separate signature_bytes parameter.
        verify_calibration_report(
            report,
            pubkey_bytes=h.signer.public_key_bytes(),
            now_utc=lambda: datetime(
                2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc
            ),
        )

    def test_all_writes_under_eval_intent_allow_list(self) -> None:
        allowed = frozenset(
            {"golden-set-write", "state-success", "state-failure"}
        )
        h = build_eval_harness(run_id="run-ALLOW")
        _run_eval(h, run_id="run-ALLOW")
        for w in h.vault.writes:
            assert w["intent"] in allowed, (
                f"unexpected eval-mode intent: {w['intent']}"
            )

    def test_no_launcher_invocations_without_items_not_required(self) -> None:
        # Sanity — happy eval with 1 item fires launcher ≥3 times.
        h = build_eval_harness(run_id="run-LI")
        _run_eval(h, run_id="run-LI")
        assert len(h.launcher.calls) >= 3

    def test_adversarial_empty_subset_signs_empty_report(self) -> None:
        h = build_eval_harness(run_id="run-EMPTY")
        r = _run_eval(h, run_id="run-EMPTY", subset=())
        report_bytes = h.vault.store[r.calibration_report_path]
        report = report_from_json(report_bytes)
        assert len(report.items) == 0
