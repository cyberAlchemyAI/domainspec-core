"""Tests for pipeline.loop.types — dataclass shapes + __post_init__ invariants.

Blueprint §5 v6 §3.2 + §5.6 LOCKED 2026-04-19.
"""

from __future__ import annotations

import dataclasses
from typing import get_args, get_type_hints

import pytest

from pipeline.loop.config import TAB_ORDERING
from pipeline.loop.errors import F_PIPE_16, F_PIPE_21, F_PIPE_22
from pipeline.loop.types import (
    CalibrationReport,
    CalibrationReportItem,
    GoldenSetItem,
    IntentKind,
    IterationState,
    ProviderCascade,
    RateLimiterState,
    RunMode,
    RunPhase,
    RunState,
    SeatCharter,
    SeatKind,
    TabEnvelope,
    TokenBucketProtocol,
)


def _mk_submission_runstate(**overrides) -> RunState:
    kwargs = dict(
        schema_version=2,
        run_id="run-sub",
        mode="submission",
        rfa_hash="r-h",
        project_context_hash="pc-h",
        golden_set_ref=None,
        org_slug="x",
        session_id="s",
        phase="initialized",
    )
    kwargs.update(overrides)
    return RunState(**kwargs)


def _mk_eval_runstate(**overrides) -> RunState:
    kwargs = dict(
        schema_version=2,
        run_id="run-eval",
        mode="eval",
        rfa_hash=None,
        project_context_hash=None,
        golden_set_ref="vault/x/golden_set/manifest.json",
        org_slug="x",
        session_id="s",
        phase="initialized",
    )
    kwargs.update(overrides)
    return RunState(**kwargs)


def _mk_tab_envelope(**overrides) -> TabEnvelope:
    kwargs = dict(
        run_id="r",
        tab_ordering=("live_radar", "deep_brief", "council_draft"),
        live_radar_payload_hash="a",
        deep_brief_payload_hash="b",
        council_draft_payload_hash="c",
        assembled_at_iso="2026-04-20T00:00:00Z",
        envelope_sha256="h",
    )
    kwargs.update(overrides)
    return TabEnvelope(**kwargs)


class TestTypeAliases:
    def test_run_mode_values(self):
        assert set(get_args(RunMode)) == {"submission", "eval"}

    def test_run_phase_exhaustive(self):
        # v7: signoff_pending_council_split added (§5 v7 amendment §3.2.1).
        expected = {
            "initialized",
            "pre_gate_pending",
            "pre_gate_passed",
            "inner_loop_iter_1",
            "inner_loop_iter_2",
            "inner_loop_iter_3",
            "post_gate_pending",
            "post_gate_passed",
            "signoff_pending",
            "signoff_pending_council_split",
            "report_signed",
            "tabs_delivered",
            "finalized",
            "degraded_paused",
            "aborted_trusted_fail",
            "aborted_operator",
            "quarantined",
            "eval_iter_pending",
            "calibration_assembled",
            "calibration_signed",
            "eval_finalized",
        }
        assert set(get_args(RunPhase)) == expected
        assert len(expected) == 21

    def test_seat_kind_values(self):
        # v7: red_team added (§5 v7 amendment §4.5a + §10).
        assert set(get_args(SeatKind)) == {"scribe", "editor", "judge", "red_team"}

    def test_intent_kind_exhaustive(self):
        expected = {
            "state-success",
            "state-failure",
            "state-quarantine",
            "golden-set-read",
            "golden-set-write",
            "three-tab-deliver",
            "bypass-pending",
            "bypass-authorization",
            "admin-risk-append",
            "cron-stamp",
        }
        assert set(get_args(IntentKind)) == expected


class TestTokenBucketProtocol:
    def test_protocol_runtime_checkable(self):
        class Bucket:
            capacity = 100
            tokens = 50.0
            refill_rate_per_sec = 1.0

        assert isinstance(Bucket(), TokenBucketProtocol)


class TestIterationState:
    def test_valid_iter_numbers(self):
        for n in (1, 2, 3):
            IterationState(iter_number=n)

    def test_invalid_iter_zero(self):
        with pytest.raises(ValueError, match="iter_number must be in"):
            IterationState(iter_number=0)

    def test_invalid_iter_four(self):
        with pytest.raises(ValueError, match="iter_number must be in"):
            IterationState(iter_number=4)

    def test_defaults(self):
        i = IterationState(iter_number=1)
        assert i.seat_draft_hashes == {}
        assert i.judge_verdict is None
        assert i.failure_code is None
        assert i.completed_at_iso is None


class TestSeatCharter:
    def test_happy_path(self):
        sc = SeatCharter(
            seat_kind="scribe",
            allowed_families=frozenset({"anthropic"}),
            primary_model="claude-sonnet-4-6",
            cascade_level=0,
            subprocess_timeout_ms=300_000,
        )
        assert sc.seat_kind == "scribe"

    def test_bad_seat_kind(self):
        with pytest.raises(ValueError, match="seat_kind"):
            SeatCharter(
                seat_kind="radar",
                allowed_families=frozenset({"anthropic"}),
                primary_model="c",
                cascade_level=0,
                subprocess_timeout_ms=1,
            )

    def test_negative_cascade_level(self):
        with pytest.raises(ValueError, match="cascade_level"):
            SeatCharter(
                seat_kind="scribe",
                allowed_families=frozenset({"anthropic"}),
                primary_model="c",
                cascade_level=-1,
                subprocess_timeout_ms=1,
            )

    def test_nonpositive_timeout(self):
        with pytest.raises(ValueError, match="subprocess_timeout_ms"):
            SeatCharter(
                seat_kind="scribe",
                allowed_families=frozenset({"anthropic"}),
                primary_model="c",
                cascade_level=0,
                subprocess_timeout_ms=0,
            )

    def test_empty_allowed_families(self):
        with pytest.raises(ValueError, match="allowed_families"):
            SeatCharter(
                seat_kind="scribe",
                allowed_families=frozenset(),
                primary_model="c",
                cascade_level=0,
                subprocess_timeout_ms=1,
            )

    def test_empty_primary_model(self):
        with pytest.raises(ValueError, match="primary_model"):
            SeatCharter(
                seat_kind="scribe",
                allowed_families=frozenset({"anthropic"}),
                primary_model="",
                cascade_level=0,
                subprocess_timeout_ms=1,
            )


class TestProviderCascade:
    def test_happy_path(self):
        pc = ProviderCascade(
            seat_kind="editor",
            levels=(("groq", "llama-3.3-70b-versatile"), ("google", "gemini-2.5-pro")),
            current_level=0,
        )
        assert len(pc.levels) == 2

    def test_bad_seat_kind(self):
        with pytest.raises(ValueError):
            ProviderCascade(
                seat_kind="scout",
                levels=(("g", "m"),),
                current_level=0,
            )

    def test_empty_levels(self):
        with pytest.raises(ValueError, match="levels must be non-empty"):
            ProviderCascade(seat_kind="editor", levels=(), current_level=0)

    def test_current_level_equals_length_means_exhausted(self):
        pc = ProviderCascade(
            seat_kind="editor",
            levels=(("g", "m"),),
            current_level=1,
        )
        assert pc.current_level == len(pc.levels)

    def test_current_level_overflow(self):
        with pytest.raises(ValueError, match="current_level"):
            ProviderCascade(
                seat_kind="editor",
                levels=(("g", "m"),),
                current_level=2,
            )

    def test_current_level_negative(self):
        with pytest.raises(ValueError, match="current_level"):
            ProviderCascade(
                seat_kind="editor",
                levels=(("g", "m"),),
                current_level=-1,
            )

    def test_bad_level_shape(self):
        with pytest.raises(ValueError, match="must be a .family, model_id."):
            ProviderCascade(
                seat_kind="editor",
                levels=(("g",),),  # type: ignore[arg-type]
                current_level=0,
            )

    def test_empty_family_in_level(self):
        with pytest.raises(ValueError):
            ProviderCascade(
                seat_kind="editor",
                levels=(("", "m"),),
                current_level=0,
            )


class TestRateLimiterState:
    def test_defaults(self):
        rls = RateLimiterState()
        assert rls.buckets == {}
        assert rls.lease_holder_id is None
        assert rls.lease_expires_at_iso is None

    def test_both_lease_fields_present(self):
        rls = RateLimiterState(
            lease_holder_id="proc-1",
            lease_expires_at_iso="2026-04-20T01:00:00Z",
        )
        assert rls.lease_holder_id == "proc-1"

    def test_holder_without_expiry_rejected(self):
        with pytest.raises(ValueError, match="both None or both non-None"):
            RateLimiterState(lease_holder_id="proc-1")

    def test_expiry_without_holder_rejected(self):
        with pytest.raises(ValueError, match="both None or both non-None"):
            RateLimiterState(lease_expires_at_iso="2026-04-20T01:00:00Z")


class TestTabEnvelope:
    def test_happy_path(self):
        te = _mk_tab_envelope()
        assert te.tab_ordering == ("live_radar", "deep_brief", "council_draft")

    def test_is_frozen(self):
        te = _mk_tab_envelope()
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            te.run_id = "other"  # type: ignore[misc]

    def test_reordered_raises_f_pipe_16(self):
        with pytest.raises(F_PIPE_16) as ei:
            _mk_tab_envelope(tab_ordering=("deep_brief", "live_radar", "council_draft"))
        assert ei.value.trigger == "tab_envelope_ordering_violation"

    def test_renamed_raises_f_pipe_16(self):
        with pytest.raises(F_PIPE_16):
            _mk_tab_envelope(tab_ordering=("live_radar", "deep_brief", "bogus"))

    def test_module_tab_ordering_value_matches_dataclass_check(self):
        # Defensive: TAB_ORDERING (config) equals the inline-literal RHS in
        # __post_init__. If these diverge, the inline-literal RHS in
        # __post_init__ is the source of truth.
        assert TAB_ORDERING == ("live_radar", "deep_brief", "council_draft")


class TestGoldenSetItem:
    def test_happy_path(self):
        g = GoldenSetItem(
            item_id="gs-1",
            rfa_hash="r-h",
            project_context_hash="pc-h",
            expected_judge_min_score=75.0,
            expected_topline_claims=("c1", "c2"),
            schema_version=1,
        )
        assert g.expected_judge_min_score == 75.0

    def test_bad_schema_version(self):
        with pytest.raises(F_PIPE_22) as ei:
            GoldenSetItem(
                item_id="gs",
                rfa_hash="r",
                project_context_hash="p",
                expected_judge_min_score=1.0,
                expected_topline_claims=(),
                schema_version=2,
            )
        assert ei.value.trigger == "calibration_report_schema_mismatch"

    def test_score_out_of_range_high(self):
        with pytest.raises(ValueError, match="expected_judge_min_score"):
            GoldenSetItem(
                item_id="gs",
                rfa_hash="r",
                project_context_hash="p",
                expected_judge_min_score=100.5,
                expected_topline_claims=(),
                schema_version=1,
            )

    def test_score_out_of_range_low(self):
        with pytest.raises(ValueError, match="expected_judge_min_score"):
            GoldenSetItem(
                item_id="gs",
                rfa_hash="r",
                project_context_hash="p",
                expected_judge_min_score=-1.0,
                expected_topline_claims=(),
                schema_version=1,
            )


class TestCalibrationReportItem:
    def test_happy_path(self):
        i = CalibrationReportItem(
            item_id="gs-1",
            run_id="run-1",
            actual_judge_score=88.0,
            iterations_taken=2,
            failure_code=None,
            claim_overlap_ratio=0.9,
            str_observation=0.015,
        )
        assert i.iterations_taken == 2

    def test_iterations_over_cap(self):
        with pytest.raises(ValueError, match="iterations_taken"):
            CalibrationReportItem(
                item_id="x",
                run_id="r",
                actual_judge_score=1.0,
                iterations_taken=4,
                failure_code=None,
                claim_overlap_ratio=0.5,
                str_observation=None,
            )

    def test_iterations_negative(self):
        with pytest.raises(ValueError):
            CalibrationReportItem(
                item_id="x",
                run_id="r",
                actual_judge_score=1.0,
                iterations_taken=-1,
                failure_code=None,
                claim_overlap_ratio=0.5,
                str_observation=None,
            )

    def test_overlap_ratio_out_of_range(self):
        with pytest.raises(ValueError, match="claim_overlap_ratio"):
            CalibrationReportItem(
                item_id="x",
                run_id="r",
                actual_judge_score=1.0,
                iterations_taken=1,
                failure_code=None,
                claim_overlap_ratio=1.5,
                str_observation=None,
            )


class TestCalibrationReport:
    def test_happy_path(self):
        r = CalibrationReport(
            schema_version=1,
            run_id="run-1",
            org_slug="x",
            golden_set_manifest_hash="h",
            items=(),
            signed_at_iso="2026-04-20T00:00:00Z",
            signature=None,
        )
        assert r.signature is None

    def test_bad_schema_version_raises_f_pipe_22(self):
        with pytest.raises(F_PIPE_22) as ei:
            CalibrationReport(
                schema_version=2,
                run_id="r",
                org_slug="x",
                golden_set_manifest_hash="h",
                items=(),
                signed_at_iso="t",
                signature=None,
            )
        assert ei.value.trigger == "calibration_report_schema_mismatch"

    def test_empty_org_slug(self):
        with pytest.raises(ValueError, match="org_slug"):
            CalibrationReport(
                schema_version=1,
                run_id="r",
                org_slug="",
                golden_set_manifest_hash="h",
                items=(),
                signed_at_iso="t",
                signature=None,
            )

    def test_empty_run_id(self):
        with pytest.raises(ValueError, match="run_id"):
            CalibrationReport(
                schema_version=1,
                run_id="",
                org_slug="x",
                golden_set_manifest_hash="h",
                items=(),
                signed_at_iso="t",
                signature=None,
            )


class TestRunStateHappyPaths:
    def test_submission_happy(self):
        rs = _mk_submission_runstate()
        assert rs.mode == "submission"
        assert rs.phase == "initialized"

    def test_eval_happy(self):
        rs = _mk_eval_runstate()
        assert rs.mode == "eval"

    def test_eval_phase_accepted(self):
        rs = _mk_eval_runstate(phase="eval_iter_pending")
        assert rs.phase == "eval_iter_pending"

    def test_submission_phase_accepted(self):
        rs = _mk_submission_runstate(phase="inner_loop_iter_2")
        assert rs.phase == "inner_loop_iter_2"


class TestRunStateSchemaVersion:
    def test_schema_version_1_rejected(self):
        with pytest.raises(F_PIPE_22) as ei:
            _mk_submission_runstate(schema_version=1)
        assert ei.value.trigger == "runstate_schema_downgrade"

    def test_schema_version_3_rejected(self):
        with pytest.raises(F_PIPE_22) as ei:
            _mk_submission_runstate(schema_version=3)
        assert ei.value.trigger == "runstate_schema_downgrade"

    def test_schema_version_zero_rejected(self):
        with pytest.raises(F_PIPE_22):
            _mk_submission_runstate(schema_version=0)


class TestRunStateModeDiscrimination:
    def test_submission_missing_rfa_hash(self):
        with pytest.raises(F_PIPE_21) as ei:
            _mk_submission_runstate(rfa_hash=None)
        assert ei.value.trigger == "submission_mode_missing_rfa_hash"

    def test_submission_missing_project_context_hash(self):
        with pytest.raises(F_PIPE_21) as ei:
            _mk_submission_runstate(project_context_hash=None)
        assert ei.value.trigger == "submission_mode_missing_project_context_hash"

    def test_submission_with_golden_set_ref(self):
        with pytest.raises(F_PIPE_21) as ei:
            _mk_submission_runstate(golden_set_ref="vault/x/gs/m")
        assert ei.value.trigger == "submission_mode_calibration_intent"

    def test_submission_with_calibration_report_ref(self):
        with pytest.raises(F_PIPE_21) as ei:
            _mk_submission_runstate(calibration_report_ref="vault/x/gs/cr.json")
        assert ei.value.trigger == "submission_mode_has_calibration_ref"

    def test_submission_with_calibration_signature_ref(self):
        with pytest.raises(F_PIPE_21) as ei:
            _mk_submission_runstate(calibration_signature_ref="vault/x/gs/cr.sig")
        assert ei.value.trigger == "submission_mode_has_calibration_ref"

    def test_eval_missing_golden_set_ref(self):
        with pytest.raises(F_PIPE_21) as ei:
            _mk_eval_runstate(golden_set_ref=None)
        assert ei.value.trigger == "eval_mode_missing_golden_set_ref"

    def test_eval_with_rfa_hash(self):
        with pytest.raises(F_PIPE_21) as ei:
            _mk_eval_runstate(rfa_hash="r-h")
        assert ei.value.trigger == "eval_mode_has_rfa_hash"

    def test_eval_with_project_context_hash(self):
        with pytest.raises(F_PIPE_21) as ei:
            _mk_eval_runstate(project_context_hash="pc-h")
        assert ei.value.trigger == "eval_mode_has_project_context_hash"

    def test_eval_with_tab_envelope_hash(self):
        with pytest.raises(F_PIPE_21) as ei:
            _mk_eval_runstate(three_tab_envelope_hash="h")
        assert ei.value.trigger == "eval_mode_has_tab_envelope_hash"


class TestRunStateFieldValidation:
    def test_bad_mode(self):
        with pytest.raises(ValueError, match="mode must be"):
            _mk_submission_runstate(mode="other")

    def test_bad_phase(self):
        with pytest.raises(ValueError, match="phase"):
            _mk_submission_runstate(phase="made_up_phase")

    def test_empty_org_slug(self):
        with pytest.raises(ValueError, match="org_slug"):
            _mk_submission_runstate(org_slug="")

    def test_empty_run_id(self):
        with pytest.raises(ValueError, match="run_id"):
            _mk_submission_runstate(run_id="")


class TestRunStateMutationSemantics:
    """RunState is NOT frozen (slots only) — checkpoint layer copy-on-writes.

    Round 1 documents this choice; round 2 state_checkpoint.py asserts it at
    the point-of-use level.
    """

    def test_not_frozen(self):
        rs = _mk_submission_runstate()
        rs.phase = "pre_gate_pending"  # should succeed
        assert rs.phase == "pre_gate_pending"

    def test_has_slots(self):
        # slots=True means no __dict__
        rs = _mk_submission_runstate()
        assert not hasattr(rs, "__dict__")
