"""Tests for pipeline.loop.run_lifecycle — §4.1 start_run + resume_run (Round 3).

Blueprint §5 v6 §4.1 LOCKED 2026-04-19.

Coverage targets:
- start_run happy paths: submission + eval; mode-discriminated union rejection.
- start_run checkpoint write: initial vault_write call with
  expected_current_file_hash=None, intent="state-success".
- resume_run happy path: valid stored bytes → structurally-equal RunState.
- resume_run schema downgrade: F_PIPE_22 raised AFTER state-failure
  checkpoint written (ordering asserted via vault_write call log).
- resume_run phase mismatch: F_PIPE_18 + quarantine marker written BEFORE raise.
- resume_run degraded_paused without bypass_pending_checkpoint_ref: F_PIPE_18
  with trigger="bypass_pending_missing".
- Integration: start_run → mutate phase → checkpoint → resume_run round-trip.
- Nested-dataclass serialization round-trip (IterationState, ProviderCascade,
  RateLimiterState with empty buckets).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any

import pytest

from pipeline.loop.errors import F_PIPE_18, F_PIPE_21, F_PIPE_22
from pipeline.loop.run_lifecycle import (
    RunIdFactory,
    VaultReadCallable,
    _allowed_resume_phases_for,
    _deserialize_runstate,
    resume_run,
    start_run,
)
from pipeline.loop.state_checkpoint import (
    _canonicalize_runstate,
    checkpoint_atomic,
)
from pipeline.loop.types import (
    IterationState,
    ProviderCascade,
    RateLimiterState,
    RunState,
)


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


@dataclass
class _FakeClock:
    iso: str = "2026-04-20T12:00:00Z"
    ms: int = 1000

    def now_ms(self) -> int:
        self.ms += 1
        return self.ms

    def now_iso(self) -> str:
        return self.iso


@dataclass
class _FakeSleep:
    calls: list[int] = field(default_factory=list)

    def __call__(self, ms: int) -> None:
        self.calls.append(ms)


@dataclass
class _FakeVault:
    store: dict[str, bytes] = field(default_factory=dict)
    calls: list[dict[str, Any]] = field(default_factory=list)
    read_calls: list[str] = field(default_factory=list)
    fail_on_read: Exception | None = None

    def __call__(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        self.calls.append(
            {
                "path": path,
                "payload": payload,
                "intent": intent,
                "write_mode": write_mode,
                "expected_current_file_hash": expected_current_file_hash,
            }
        )
        self.store[path] = payload
        return hashlib.sha256(payload).hexdigest()

    def read(self, *, path: str) -> bytes:
        self.read_calls.append(path)
        if self.fail_on_read is not None:
            raise self.fail_on_read
        return self.store[path]


@dataclass
class _FixedRunId:
    value: str = "01JABCDEF0000000000000000"

    def __call__(self) -> str:
        return self.value


def _submission_kwargs(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = dict(
        mode="submission",
        org_slug="mycosymbiotics",
        session_id="sess-1",
        rfa_hash="rfa-h",
        project_context_hash="pc-h",
        golden_set_ref=None,
    )
    base.update(overrides)
    return base


def _eval_kwargs(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = dict(
        mode="eval",
        org_slug="mycosymbiotics",
        session_id="sess-1",
        rfa_hash=None,
        project_context_hash=None,
        golden_set_ref="golden-set-ref-1",
    )
    base.update(overrides)
    return base


def _persist_runstate(vault: _FakeVault, rs: RunState) -> None:
    """Write a canonical RunState to the fake vault under the standard path."""
    path = f"pipeline/{rs.run_id}/state.json"
    vault.store[path] = _canonicalize_runstate(rs)


# ---------------------------------------------------------------------------
# start_run — happy paths
# ---------------------------------------------------------------------------


class TestStartRunSubmissionHappyPath:
    def test_submission_returns_runstate_in_initialized(self) -> None:
        vault = _FakeVault()
        rs = start_run(
            **_submission_kwargs(),
            run_id_factory=_FixedRunId("run-sub-1"),
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert isinstance(rs, RunState)
        assert rs.run_id == "run-sub-1"
        assert rs.mode == "submission"
        assert rs.phase == "initialized"
        assert rs.schema_version == 2
        assert rs.rfa_hash == "rfa-h"
        assert rs.project_context_hash == "pc-h"
        assert rs.golden_set_ref is None
        assert rs.started_at_iso == "2026-04-20T12:00:00Z"
        assert rs.last_checkpoint_iso == "2026-04-20T12:00:00Z"

    def test_submission_writes_initial_checkpoint(self) -> None:
        vault = _FakeVault()
        start_run(
            **_submission_kwargs(),
            run_id_factory=_FixedRunId("run-sub-2"),
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert len(vault.calls) == 1
        call = vault.calls[0]
        assert call["path"] == "pipeline/run-sub-2/state.json"
        assert call["intent"] == "state-success"
        assert call["write_mode"] == "overwrite"
        assert call["expected_current_file_hash"] is None

    def test_submission_canonical_payload_is_valid_json(self) -> None:
        vault = _FakeVault()
        start_run(
            **_submission_kwargs(),
            run_id_factory=_FixedRunId("run-sub-3"),
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        body = vault.calls[0]["payload"]
        loaded = json.loads(body.decode("utf-8"))
        assert loaded["mode"] == "submission"
        assert loaded["phase"] == "initialized"
        assert loaded["schema_version"] == 2


class TestStartRunEvalHappyPath:
    def test_eval_returns_runstate_with_golden_set_ref(self) -> None:
        vault = _FakeVault()
        rs = start_run(
            **_eval_kwargs(),
            run_id_factory=_FixedRunId("run-eval-1"),
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert rs.mode == "eval"
        assert rs.golden_set_ref == "golden-set-ref-1"
        assert rs.rfa_hash is None
        assert rs.project_context_hash is None
        assert rs.phase == "initialized"

    def test_eval_writes_initial_checkpoint(self) -> None:
        vault = _FakeVault()
        start_run(
            **_eval_kwargs(),
            run_id_factory=_FixedRunId("run-eval-2"),
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert len(vault.calls) == 1
        assert vault.calls[0]["intent"] == "state-success"
        assert vault.calls[0]["expected_current_file_hash"] is None


class TestStartRunModeDiscrimination:
    def test_submission_with_golden_set_ref_raises_f_pipe_21(self) -> None:
        vault = _FakeVault()
        with pytest.raises(F_PIPE_21):
            start_run(
                **_submission_kwargs(golden_set_ref="should-not-be-here"),
                run_id_factory=_FixedRunId(),
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )

    def test_submission_missing_rfa_hash_raises_f_pipe_21(self) -> None:
        with pytest.raises(F_PIPE_21):
            start_run(
                **_submission_kwargs(rfa_hash=None),
                run_id_factory=_FixedRunId(),
                vault_write=_FakeVault(),
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )

    def test_submission_missing_project_context_raises_f_pipe_21(self) -> None:
        with pytest.raises(F_PIPE_21):
            start_run(
                **_submission_kwargs(project_context_hash=None),
                run_id_factory=_FixedRunId(),
                vault_write=_FakeVault(),
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )

    def test_eval_missing_golden_set_raises_f_pipe_21(self) -> None:
        with pytest.raises(F_PIPE_21):
            start_run(
                **_eval_kwargs(golden_set_ref=None),
                run_id_factory=_FixedRunId(),
                vault_write=_FakeVault(),
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )

    def test_eval_with_rfa_hash_raises_f_pipe_21(self) -> None:
        with pytest.raises(F_PIPE_21):
            start_run(
                **_eval_kwargs(rfa_hash="should-not-be-here"),
                run_id_factory=_FixedRunId(),
                vault_write=_FakeVault(),
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )

    def test_eval_with_project_context_raises_f_pipe_21(self) -> None:
        with pytest.raises(F_PIPE_21):
            start_run(
                **_eval_kwargs(project_context_hash="should-not-be-here"),
                run_id_factory=_FixedRunId(),
                vault_write=_FakeVault(),
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )


class TestStartRunFactoryContract:
    def test_factory_is_called_once(self) -> None:
        call_count = {"n": 0}

        class _CountingFactory:
            def __call__(self) -> str:
                call_count["n"] += 1
                return "run-counted"

        start_run(
            **_submission_kwargs(),
            run_id_factory=_CountingFactory(),
            vault_write=_FakeVault(),
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert call_count["n"] == 1

    def test_factory_returning_duckarable_string(self) -> None:
        # Simple callable rather than a class implementing Protocol.
        rs = start_run(
            **_submission_kwargs(),
            run_id_factory=lambda: "lambda-run-id",
            vault_write=_FakeVault(),
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert rs.run_id == "lambda-run-id"


# ---------------------------------------------------------------------------
# resume_run — happy paths
# ---------------------------------------------------------------------------


def _mk_stored_submission_runstate(
    *, run_id: str = "run-resume", phase: str = "pre_gate_passed", **overrides: Any
) -> RunState:
    kwargs: dict[str, Any] = dict(
        schema_version=2,
        run_id=run_id,
        mode="submission",
        rfa_hash="rfa-h",
        project_context_hash="pc-h",
        golden_set_ref=None,
        org_slug="mycosymbiotics",
        session_id="sess-1",
        phase=phase,
        started_at_iso="2026-04-20T12:00:00Z",
        last_checkpoint_iso="2026-04-20T12:01:00Z",
    )
    kwargs.update(overrides)
    return RunState(**kwargs)


def _mk_stored_eval_runstate(
    *, run_id: str = "run-eval-resume", phase: str = "eval_iter_pending", **overrides: Any
) -> RunState:
    kwargs: dict[str, Any] = dict(
        schema_version=2,
        run_id=run_id,
        mode="eval",
        rfa_hash=None,
        project_context_hash=None,
        golden_set_ref="golden-set-1",
        org_slug="mycosymbiotics",
        session_id="sess-1",
        phase=phase,
        started_at_iso="2026-04-20T12:00:00Z",
        last_checkpoint_iso="2026-04-20T12:01:00Z",
    )
    kwargs.update(overrides)
    return RunState(**kwargs)


class TestResumeRunSubmissionHappyPath:
    def test_returns_structurally_equal_runstate(self) -> None:
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(phase="pre_gate_passed")
        _persist_runstate(vault, original)

        resumed = resume_run(
            original.run_id,
            vault_read=vault.read,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert resumed.run_id == original.run_id
        assert resumed.mode == original.mode
        assert resumed.phase == original.phase
        assert resumed.schema_version == 2
        assert resumed.rfa_hash == original.rfa_hash

    @pytest.mark.parametrize(
        "phase",
        [
            "pre_gate_pending",
            "pre_gate_passed",
            "inner_loop_iter_1",
            "inner_loop_iter_2",
            "inner_loop_iter_3",
            "post_gate_pending",
            "signoff_pending",
        ],
    )
    def test_every_allowed_submission_phase_resumes(self, phase: str) -> None:
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(phase=phase)
        _persist_runstate(vault, original)

        resumed = resume_run(
            original.run_id,
            vault_read=vault.read,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert resumed.phase == phase

    def test_degraded_paused_with_bypass_ref_resumes(self) -> None:
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(
            phase="degraded_paused",
            bypass_pending_checkpoint_ref="pipeline/run-resume/bypass.json",
        )
        _persist_runstate(vault, original)

        resumed = resume_run(
            original.run_id,
            vault_read=vault.read,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert resumed.phase == "degraded_paused"
        assert resumed.bypass_pending_checkpoint_ref == "pipeline/run-resume/bypass.json"

    def test_read_called_with_correct_path(self) -> None:
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(run_id="run-read-path")
        _persist_runstate(vault, original)
        resume_run(
            "run-read-path",
            vault_read=vault.read,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert vault.read_calls == ["pipeline/run-read-path/state.json"]


class TestResumeRunEvalHappyPath:
    def test_eval_iter_pending_resumes(self) -> None:
        vault = _FakeVault()
        original = _mk_stored_eval_runstate(phase="eval_iter_pending")
        _persist_runstate(vault, original)
        resumed = resume_run(
            original.run_id,
            vault_read=vault.read,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert resumed.mode == "eval"
        assert resumed.phase == "eval_iter_pending"

    def test_calibration_assembled_resumes(self) -> None:
        vault = _FakeVault()
        original = _mk_stored_eval_runstate(phase="calibration_assembled")
        _persist_runstate(vault, original)
        resumed = resume_run(
            original.run_id,
            vault_read=vault.read,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert resumed.phase == "calibration_assembled"


# ---------------------------------------------------------------------------
# resume_run — schema downgrade (F_PIPE_22)
# ---------------------------------------------------------------------------


class TestResumeRunSchemaDowngrade:
    def _write_downgraded_payload(self, vault: _FakeVault, run_id: str) -> None:
        # Construct a VALID RunState first, then mutate schema_version in the
        # serialized payload to simulate an on-disk downgrade.
        rs = _mk_stored_submission_runstate(run_id=run_id)
        payload = _canonicalize_runstate(rs)
        data = json.loads(payload.decode("utf-8"))
        data["schema_version"] = 1
        vault.store[f"pipeline/{run_id}/state.json"] = json.dumps(
            data, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")

    def test_schema_downgrade_raises_f_pipe_22(self) -> None:
        vault = _FakeVault()
        self._write_downgraded_payload(vault, "run-downgrade-1")
        with pytest.raises(F_PIPE_22):
            resume_run(
                "run-downgrade-1",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )

    def test_schema_downgrade_writes_state_failure_BEFORE_raise(self) -> None:
        vault = _FakeVault()
        self._write_downgraded_payload(vault, "run-downgrade-2")
        with pytest.raises(F_PIPE_22):
            resume_run(
                "run-downgrade-2",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        # state-failure checkpoint must have been written.
        failure_writes = [c for c in vault.calls if c["intent"] == "state-failure"]
        assert len(failure_writes) == 1
        assert failure_writes[0]["path"] == "pipeline/run-downgrade-2/state_failure.json"

    def test_schema_downgrade_error_has_expected_details(self) -> None:
        vault = _FakeVault()
        self._write_downgraded_payload(vault, "run-downgrade-3")
        with pytest.raises(F_PIPE_22) as exc_info:
            resume_run(
                "run-downgrade-3",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        assert exc_info.value.details["observed"] == 1
        assert exc_info.value.details["expected"] == 2


# ---------------------------------------------------------------------------
# resume_run — phase mismatch (F_PIPE_18)
# ---------------------------------------------------------------------------


class TestResumeRunPhaseMismatch:
    @pytest.mark.parametrize(
        "forbidden_phase",
        [
            "initialized",
            "finalized",
            "report_signed",
            "tabs_delivered",
            "post_gate_passed",
            "aborted_trusted_fail",
            "aborted_operator",
            "quarantined",
        ],
    )
    def test_forbidden_submission_phase_raises_f_pipe_18(
        self, forbidden_phase: str
    ) -> None:
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(
            run_id="run-bad-phase", phase=forbidden_phase
        )
        _persist_runstate(vault, original)
        with pytest.raises(F_PIPE_18) as exc_info:
            resume_run(
                "run-bad-phase",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        assert exc_info.value.details["observed_phase"] == forbidden_phase

    def test_phase_mismatch_writes_quarantine_BEFORE_raise(self) -> None:
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(
            run_id="run-q-phase", phase="finalized"
        )
        _persist_runstate(vault, original)
        with pytest.raises(F_PIPE_18):
            resume_run(
                "run-q-phase",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        # Quarantine marker written under state-success intent per Round 2 convention.
        q_writes = [
            c for c in vault.calls
            if c["path"] == "pipeline/run-q-phase/quarantine.json"
        ]
        assert len(q_writes) == 1

    def test_eval_mode_with_submission_phase_rejects(self) -> None:
        vault = _FakeVault()
        # eval mode but phase is submission-only.
        original = _mk_stored_eval_runstate(
            run_id="run-eval-sub-phase", phase="pre_gate_pending"
        )
        _persist_runstate(vault, original)
        with pytest.raises(F_PIPE_18):
            resume_run(
                "run-eval-sub-phase",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )

    def test_f_pipe_18_carries_quarantine_ref(self) -> None:
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(
            run_id="run-q-ref", phase="finalized"
        )
        _persist_runstate(vault, original)
        with pytest.raises(F_PIPE_18) as exc_info:
            resume_run(
                "run-q-ref",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        assert exc_info.value.details["quarantine_marker_ref"] == (
            "pipeline/run-q-ref/quarantine.json"
        )


class TestResumeRunDegradedPausedWithoutBypass:
    def test_degraded_paused_no_bypass_ref_raises_f_pipe_18(self) -> None:
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(
            run_id="run-deg-nobypass",
            phase="degraded_paused",
            bypass_pending_checkpoint_ref=None,
        )
        _persist_runstate(vault, original)
        with pytest.raises(F_PIPE_18) as exc_info:
            resume_run(
                "run-deg-nobypass",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        assert exc_info.value.trigger == "bypass_pending_missing"

    def test_degraded_paused_no_bypass_writes_quarantine(self) -> None:
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(
            run_id="run-deg-q",
            phase="degraded_paused",
            bypass_pending_checkpoint_ref=None,
        )
        _persist_runstate(vault, original)
        with pytest.raises(F_PIPE_18):
            resume_run(
                "run-deg-q",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        q_writes = [
            c for c in vault.calls
            if c["path"] == "pipeline/run-deg-q/quarantine.json"
        ]
        assert len(q_writes) == 1


# ---------------------------------------------------------------------------
# Nested-dataclass serialization round-trip
# ---------------------------------------------------------------------------


class TestDeserializationRoundTrip:
    def test_iterations_round_trip(self) -> None:
        original = _mk_stored_submission_runstate(phase="inner_loop_iter_1")
        original.iterations = [
            IterationState(
                iter_number=1,
                seat_draft_hashes={"scribe": "s1"},
                started_at_iso="2026-04-20T12:05:00Z",
            ),
            IterationState(iter_number=2, started_at_iso="2026-04-20T12:10:00Z"),
        ]
        payload = _canonicalize_runstate(original)
        restored = _deserialize_runstate(payload)
        assert len(restored.iterations) == 2
        assert restored.iterations[0].iter_number == 1
        assert restored.iterations[0].seat_draft_hashes == {"scribe": "s1"}
        assert restored.iterations[1].iter_number == 2

    def test_active_cascade_round_trip(self) -> None:
        original = _mk_stored_submission_runstate()
        original.active_cascade = ProviderCascade(
            seat_kind="scribe",
            levels=(("anthropic", "claude"), ("google", "gemini")),
            current_level=1,
        )
        payload = _canonicalize_runstate(original)
        restored = _deserialize_runstate(payload)
        assert restored.active_cascade is not None
        assert restored.active_cascade.seat_kind == "scribe"
        assert restored.active_cascade.levels == (
            ("anthropic", "claude"),
            ("google", "gemini"),
        )
        assert restored.active_cascade.current_level == 1

    def test_rate_limiter_snapshot_empty_buckets_round_trip(self) -> None:
        original = _mk_stored_submission_runstate()
        original.rate_limiter_snapshot = RateLimiterState(
            buckets={},
            last_refill_iso="2026-04-20T12:03:00Z",
            lease_holder_id="holder-1",
            lease_expires_at_iso="2026-04-20T12:03:30Z",
        )
        payload = _canonicalize_runstate(original)
        restored = _deserialize_runstate(payload)
        assert restored.rate_limiter_snapshot is not None
        assert restored.rate_limiter_snapshot.last_refill_iso == "2026-04-20T12:03:00Z"
        assert restored.rate_limiter_snapshot.lease_holder_id == "holder-1"

    def test_run_iteration_families_so_far_round_trip(self) -> None:
        original = _mk_stored_submission_runstate()
        original.run_iteration_families_so_far = {
            "scribe": ("anthropic", "claude"),
            "judge": ("google", "gemini"),
        }
        payload = _canonicalize_runstate(original)
        restored = _deserialize_runstate(payload)
        assert restored.run_iteration_families_so_far == {
            "scribe": ("anthropic", "claude"),
            "judge": ("google", "gemini"),
        }

    def test_minimal_submission_round_trip(self) -> None:
        original = _mk_stored_submission_runstate()
        payload = _canonicalize_runstate(original)
        restored = _deserialize_runstate(payload)
        assert restored.run_id == original.run_id
        assert restored.mode == original.mode
        assert restored.phase == original.phase
        assert restored.rfa_hash == original.rfa_hash


# ---------------------------------------------------------------------------
# Integration — full round-trip
# ---------------------------------------------------------------------------


class TestIntegration:
    def test_start_then_advance_then_resume(self) -> None:
        vault = _FakeVault()
        rs = start_run(
            **_submission_kwargs(),
            run_id_factory=_FixedRunId("run-int-1"),
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        # Simulate phase advance + checkpoint.
        rs.phase = "pre_gate_passed"
        committed_hash = vault.calls[0]["payload"]
        result = checkpoint_atomic(
            rs,
            intent="state-success",
            expected_current_file_hash=hashlib.sha256(committed_hash).hexdigest(),
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert result.attempt_count == 1
        # Resume reads the latest checkpoint bytes.
        resumed = resume_run(
            "run-int-1",
            vault_read=vault.read,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert resumed.run_id == "run-int-1"
        assert resumed.phase == "pre_gate_passed"
        assert resumed.mode == "submission"


# ---------------------------------------------------------------------------
# Allowed-phase helper
# ---------------------------------------------------------------------------


class TestAllowedResumePhasesFor:
    def test_submission_set_matches_blueprint(self) -> None:
        got = _allowed_resume_phases_for("submission")
        assert got == frozenset(
            {
                "pre_gate_pending",
                "pre_gate_passed",
                "inner_loop_iter_1",
                "inner_loop_iter_2",
                "inner_loop_iter_3",
                "post_gate_pending",
                "signoff_pending",
                "signoff_pending_council_split",  # v7 §5 v7 amendment §4.7
                "degraded_paused",
            }
        )

    def test_eval_set_matches_blueprint(self) -> None:
        got = _allowed_resume_phases_for("eval")
        assert got == frozenset(
            {
                "eval_iter_pending",
                "calibration_assembled",
            }
        )

    def test_unknown_mode_returns_empty_frozenset(self) -> None:
        assert _allowed_resume_phases_for("unknown") == frozenset()


# ---------------------------------------------------------------------------
# kw-only discipline
# ---------------------------------------------------------------------------


class TestKWOnly:
    def test_start_run_positional_rejected(self) -> None:
        with pytest.raises(TypeError):
            start_run(  # type: ignore[call-arg]
                "submission",
                "org",
                "sess",
                "rfa",
                "pc",
                None,
                _FixedRunId(),
                _FakeVault(),
                _FakeClock(),
                _FakeSleep(),
            )

    def test_resume_run_positional_run_id_accepted(self) -> None:
        # resume_run takes run_id positionally by design; the rest are kw-only.
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(run_id="run-pos")
        _persist_runstate(vault, original)
        rs = resume_run(
            "run-pos",
            vault_read=vault.read,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert rs.run_id == "run-pos"

    def test_resume_run_all_others_kw_only(self) -> None:
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(run_id="run-kw")
        _persist_runstate(vault, original)
        with pytest.raises(TypeError):
            resume_run(  # type: ignore[misc]
                "run-kw",
                vault.read,
                vault,
                _FakeClock(),
                _FakeSleep(),
            )


# ---------------------------------------------------------------------------
# Protocol discipline
# ---------------------------------------------------------------------------


class TestProtocolDiscipline:
    def test_vault_read_callable_duck_types(self) -> None:
        vault = _FakeVault()
        original = _mk_stored_submission_runstate(run_id="run-duck")
        _persist_runstate(vault, original)

        def _read(*, path: str) -> bytes:
            return vault.store[path]

        rs = resume_run(
            "run-duck",
            vault_read=_read,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert rs.run_id == "run-duck"

    def test_run_id_factory_duck_types(self) -> None:
        vault = _FakeVault()
        rs = start_run(
            **_submission_kwargs(),
            run_id_factory=lambda: "duck-id",
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert rs.run_id == "duck-id"

    def test_public_protocols_runtime_checkable(self) -> None:
        assert isinstance(_FixedRunId(), RunIdFactory)

        class _ReadImpl:
            def __call__(self, *, path: str) -> bytes:
                return b""

        assert isinstance(_ReadImpl(), VaultReadCallable)


# ---------------------------------------------------------------------------
# Package re-exports
# ---------------------------------------------------------------------------


class TestPackageReExports:
    def test_start_run_resume_run_exported(self) -> None:
        import pipeline.loop as loop_pkg

        assert hasattr(loop_pkg, "start_run")
        assert hasattr(loop_pkg, "resume_run")
        assert hasattr(loop_pkg, "RunIdFactory")
        assert hasattr(loop_pkg, "VaultReadCallable")

    def test_exports_present_in_all(self) -> None:
        import pipeline.loop as loop_pkg

        for name in ("start_run", "resume_run", "RunIdFactory", "VaultReadCallable"):
            assert name in loop_pkg.__all__
