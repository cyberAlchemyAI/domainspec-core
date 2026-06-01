"""Tests for pipeline.loop.post_gate_runner — §4.1 step 6-7 POST-gate orchestration.

Blueprint §5 v6 LOCKED 2026-04-19 (§4.1 steps 6-7; §3.2.1 v5 post_gate
hashes; §6 F-PIPE-03 post_gate_timeout).

Round 6 is the first §5 module to consume §4 Logician primitives. These
tests drive the orchestrator through a stub ``GateRunnerProtocol`` and
stub ``PostGateInputFactory`` — no real Logician dispatch is exercised
here (Round 4 Logician tests already cover run_post_gate correctness).

Coverage targets per the spec card:

- Happy path — PASS verdict → phase → post_gate_passed, hashes populated.
- Resume path — entering with phase == "post_gate_pending" skips the
  transition checkpoint (exactly one state-success write).
- Hash threading — ``initial_checkpoint_hash`` threads through as the
  CAS pin on the first ``vault_write`` call.
- Factory contract — invoked exactly once with live run_state +
  inner_loop_result kwargs.
- FAIL dispatch — returned ``passed=False`` → state-failure checkpoint
  + ``PostGateRejected`` carrying the full gate_result.
- Timeout guard — elapsed > timeout_ms → state-failure + F_PIPE_03.
- Mid-loop propagation — ``LogicianMidLoopCall`` writes state-failure
  and re-raises (not wrapped as PostGateRejected).
- Vault error propagation — CAS exhaustion (F_PIPE_01) on the
  phase-transition checkpoint surfaces unwrapped.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.logician import GateRunnerPostResult, LogicianMidLoopCall, PostGateInput
from pipeline.loop.errors import F_PIPE_03
from pipeline.loop.post_gate_runner import (
    PostGateOrchestrationResult,
    PostGateRejected,
    run_post_gate_orchestration,
)
from pipeline.loop.revision_loop import InnerLoopResult
from pipeline.loop.types import IterationState, RunState


# ---------------------------------------------------------------------------
# Fixtures / fakes
# ---------------------------------------------------------------------------


def _mk_runstate(phase: str = "inner_loop_iter_1", **overrides: Any) -> RunState:
    kwargs: dict[str, Any] = dict(
        schema_version=2,
        run_id="run-r6",
        mode="submission",
        rfa_hash="rfa-h",
        project_context_hash="pc-h",
        golden_set_ref=None,
        org_slug="mycosymbiotics",
        session_id="sess",
        phase=phase,
    )
    kwargs.update(overrides)
    return RunState(**kwargs)


def _mk_inner_loop_result(*, hash_: str = "initial-hash") -> InnerLoopResult:
    return InnerLoopResult(
        final_iteration=IterationState(
            iter_number=1,
            started_at_iso="2026-04-20T12:00:00Z",
            completed_at_iso="2026-04-20T12:00:03Z",
        ),
        converged_on="score_threshold",
        iterations_run=1,
        final_checkpoint_hash=hash_,
    )


def _mk_gate_result(
    *,
    passed: bool = True,
    failed_step_number: int | None = None,
    failure_code: str | None = None,
) -> GateRunnerPostResult:
    return GateRunnerPostResult(
        passed=passed,
        failed_step_number=failed_step_number,
        failure_code=failure_code,
        failure_detail="" if passed else "stub failure",
        failure_codes=() if passed else (failure_code or "F-POST-STUB",),
        completed_steps=(),
        claim_evidence_map=None,
        underlying_post_gate_result=None,
    )


@dataclass
class _FakeClock:
    values: list[int] = field(default_factory=list)
    _idx: int = 0
    iso: str = "2026-04-20T12:00:00Z"

    def now_ms(self) -> int:
        if self._idx >= len(self.values):
            return self.values[-1] if self.values else 0
        v = self.values[self._idx]
        self._idx += 1
        return v

    def now_iso(self) -> str:
        return self.iso


@dataclass
class _FakeSleep:
    calls: list[int] = field(default_factory=list)

    def __call__(self, ms: int) -> None:
        self.calls.append(ms)


@dataclass
class _FakeVault:
    """CAS-aware in-process vault fake mirroring Round 2 test pattern."""

    store: dict[str, bytes] = field(default_factory=dict)
    calls: list[dict[str, Any]] = field(default_factory=list)
    override: Any = None

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
            dict(
                path=path,
                payload=payload,
                intent=intent,
                write_mode=write_mode,
                expected_current_file_hash=expected_current_file_hash,
            )
        )
        if self.override is not None:
            return self.override(
                path=path,
                payload=payload,
                intent=intent,
                write_mode=write_mode,
                expected_current_file_hash=expected_current_file_hash,
            )
        import hashlib

        self.store[path] = payload
        return hashlib.sha256(payload).hexdigest()


@dataclass
class _FakeGateRunner:
    result: GateRunnerPostResult | None = None
    raise_exc: BaseException | None = None
    calls: list[Any] = field(default_factory=list)

    def run_post_gate(self, input_: PostGateInput) -> GateRunnerPostResult:
        self.calls.append(input_)
        if self.raise_exc is not None:
            raise self.raise_exc
        assert self.result is not None
        return self.result


@dataclass
class _FakeFactory:
    """One-shot input factory — records every invocation."""

    payload: Any = None
    calls: list[dict[str, Any]] = field(default_factory=list)
    raise_exc: BaseException | None = None

    def __call__(
        self, *, run_state: RunState, inner_loop_result: InnerLoopResult
    ) -> PostGateInput:
        self.calls.append(dict(run_state=run_state, inner_loop_result=inner_loop_result))
        if self.raise_exc is not None:
            raise self.raise_exc
        return self.payload  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Happy paths
# ---------------------------------------------------------------------------


class TestHappyPath:
    def test_pass_verdict_populates_hashes_and_phase(self) -> None:
        rs = _mk_runstate(phase="inner_loop_iter_1")
        ilr = _mk_inner_loop_result(hash_="init-hash")
        gate = _FakeGateRunner(result=_mk_gate_result(passed=True))
        factory = _FakeFactory(payload="opaque-input")
        clock = _FakeClock(values=[1000, 2000])
        vault = _FakeVault()

        result = run_post_gate_orchestration(
            run_state=rs,
            inner_loop_result=ilr,
            post_gate_input_factory=factory,
            gate_runner=gate,
            vault_write=vault,
            clock=clock,
            sleep=_FakeSleep(),
            initial_checkpoint_hash="init-hash",
        )

        assert isinstance(result, PostGateOrchestrationResult)
        assert result.gate_result.passed is True
        assert rs.phase == "post_gate_passed"
        assert rs.post_gate_result_hash == result.post_gate_result_hash
        assert result.signed_claim_evidence_map_hash is None
        # Two state-success writes (phase-transition + success-commit).
        assert [c["intent"] for c in vault.calls] == [
            "state-success",
            "state-success",
        ]

    def test_resume_entry_skips_phase_checkpoint(self) -> None:
        rs = _mk_runstate(phase="post_gate_pending")
        ilr = _mk_inner_loop_result(hash_="resume-hash")
        gate = _FakeGateRunner(result=_mk_gate_result(passed=True))
        factory = _FakeFactory(payload="opaque-input")
        clock = _FakeClock(values=[10, 20])
        vault = _FakeVault()

        result = run_post_gate_orchestration(
            run_state=rs,
            inner_loop_result=ilr,
            post_gate_input_factory=factory,
            gate_runner=gate,
            vault_write=vault,
            clock=clock,
            sleep=_FakeSleep(),
            initial_checkpoint_hash="resume-hash",
        )

        # Only the success checkpoint lands on the resume path.
        assert len(vault.calls) == 1
        assert vault.calls[0]["intent"] == "state-success"
        assert vault.calls[0]["expected_current_file_hash"] == "resume-hash"
        assert rs.phase == "post_gate_passed"
        assert result.gate_result.passed is True

    def test_phase_transitions_to_post_gate_passed(self) -> None:
        rs = _mk_runstate(phase="inner_loop_iter_3")
        gate = _FakeGateRunner(result=_mk_gate_result(passed=True))
        vault = _FakeVault()

        run_post_gate_orchestration(
            run_state=rs,
            inner_loop_result=_mk_inner_loop_result(hash_="h0"),
            post_gate_input_factory=_FakeFactory(payload="x"),
            gate_runner=gate,
            vault_write=vault,
            clock=_FakeClock(values=[0, 5]),
            sleep=_FakeSleep(),
            initial_checkpoint_hash="h0",
        )
        assert rs.phase == "post_gate_passed"


# ---------------------------------------------------------------------------
# Hash threading
# ---------------------------------------------------------------------------


class TestHashThreading:
    def test_initial_checkpoint_hash_pins_first_cas_attempt(self) -> None:
        rs = _mk_runstate(phase="inner_loop_iter_2")
        vault = _FakeVault()
        run_post_gate_orchestration(
            run_state=rs,
            inner_loop_result=_mk_inner_loop_result(hash_="H-INIT"),
            post_gate_input_factory=_FakeFactory(payload="x"),
            gate_runner=_FakeGateRunner(result=_mk_gate_result(passed=True)),
            vault_write=vault,
            clock=_FakeClock(values=[0, 1]),
            sleep=_FakeSleep(),
            initial_checkpoint_hash="H-INIT",
        )
        assert vault.calls[0]["expected_current_file_hash"] == "H-INIT"

    def test_committed_checkpoint_hash_is_final_cas_head(self) -> None:
        rs = _mk_runstate(phase="inner_loop_iter_1")
        vault = _FakeVault()
        result = run_post_gate_orchestration(
            run_state=rs,
            inner_loop_result=_mk_inner_loop_result(hash_="A"),
            post_gate_input_factory=_FakeFactory(payload="x"),
            gate_runner=_FakeGateRunner(result=_mk_gate_result(passed=True)),
            vault_write=vault,
            clock=_FakeClock(values=[0, 1]),
            sleep=_FakeSleep(),
            initial_checkpoint_hash="A",
        )
        # The final CAS head is the sha256 of the second write's payload.
        import hashlib

        expected = hashlib.sha256(vault.calls[-1]["payload"]).hexdigest()
        assert result.committed_checkpoint_hash == expected

    def test_second_cas_pin_is_first_call_return(self) -> None:
        rs = _mk_runstate(phase="inner_loop_iter_1")
        vault = _FakeVault()
        run_post_gate_orchestration(
            run_state=rs,
            inner_loop_result=_mk_inner_loop_result(hash_="init"),
            post_gate_input_factory=_FakeFactory(payload="x"),
            gate_runner=_FakeGateRunner(result=_mk_gate_result(passed=True)),
            vault_write=vault,
            clock=_FakeClock(values=[0, 1]),
            sleep=_FakeSleep(),
            initial_checkpoint_hash="init",
        )
        import hashlib

        first_head = hashlib.sha256(vault.calls[0]["payload"]).hexdigest()
        assert vault.calls[1]["expected_current_file_hash"] == first_head


# ---------------------------------------------------------------------------
# Factory contract
# ---------------------------------------------------------------------------


class TestFactoryContract:
    def test_factory_invoked_exactly_once(self) -> None:
        rs = _mk_runstate(phase="inner_loop_iter_1")
        ilr = _mk_inner_loop_result(hash_="h")
        factory = _FakeFactory(payload="x")
        run_post_gate_orchestration(
            run_state=rs,
            inner_loop_result=ilr,
            post_gate_input_factory=factory,
            gate_runner=_FakeGateRunner(result=_mk_gate_result(passed=True)),
            vault_write=_FakeVault(),
            clock=_FakeClock(values=[0, 1]),
            sleep=_FakeSleep(),
            initial_checkpoint_hash="h",
        )
        assert len(factory.calls) == 1
        assert factory.calls[0]["run_state"] is rs
        assert factory.calls[0]["inner_loop_result"] is ilr

    def test_factory_invoked_after_phase_transition_checkpoint(self) -> None:
        """The factory sees the mutated phase (post_gate_pending)."""
        rs = _mk_runstate(phase="inner_loop_iter_1")
        observed: list[str] = []

        def _capture(
            *, run_state: RunState, inner_loop_result: InnerLoopResult
        ) -> PostGateInput:
            observed.append(run_state.phase)
            return "x"  # type: ignore[return-value]

        run_post_gate_orchestration(
            run_state=rs,
            inner_loop_result=_mk_inner_loop_result(hash_="h"),
            post_gate_input_factory=_capture,
            gate_runner=_FakeGateRunner(result=_mk_gate_result(passed=True)),
            vault_write=_FakeVault(),
            clock=_FakeClock(values=[0, 1]),
            sleep=_FakeSleep(),
            initial_checkpoint_hash="h",
        )
        assert observed == ["post_gate_pending"]


# ---------------------------------------------------------------------------
# Failure dispatch
# ---------------------------------------------------------------------------


class TestFailureDispatch:
    def test_fail_verdict_raises_post_gate_rejected(self) -> None:
        rs = _mk_runstate(phase="inner_loop_iter_1")
        vault = _FakeVault()
        fail_result = _mk_gate_result(
            passed=False, failed_step_number=5, failure_code="F-POST-08.bt11"
        )
        with pytest.raises(PostGateRejected) as ei:
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(hash_="h"),
                post_gate_input_factory=_FakeFactory(payload="x"),
                gate_runner=_FakeGateRunner(result=fail_result),
                vault_write=vault,
                clock=_FakeClock(values=[0, 1]),
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )
        assert ei.value.gate_result is fail_result
        # phase-transition write + state-failure write
        intents = [c["intent"] for c in vault.calls]
        assert intents == ["state-success", "state-failure"]
        # Phase stays at post_gate_pending (no post_gate_passed transition).
        assert rs.phase == "post_gate_pending"
        # Traceability hash pinned on FAIL path too.
        assert rs.post_gate_result_hash is not None

    def test_logician_mid_loop_call_propagates_unwrapped(self) -> None:
        rs = _mk_runstate(phase="inner_loop_iter_1")
        vault = _FakeVault()
        mid_loop = LogicianMidLoopCall("POST", "POST")
        with pytest.raises(LogicianMidLoopCall):
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(hash_="h"),
                post_gate_input_factory=_FakeFactory(payload="x"),
                gate_runner=_FakeGateRunner(raise_exc=mid_loop),
                vault_write=vault,
                clock=_FakeClock(values=[0, 1]),
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )
        # phase-transition + state-failure (from _write_state_failure helper)
        intents = [c["intent"] for c in vault.calls]
        assert intents == ["state-success", "state-failure"]

    def test_timeout_raises_f_pipe_03(self) -> None:
        rs = _mk_runstate(phase="inner_loop_iter_1")
        vault = _FakeVault()
        # Clock calls in order:
        #   1-3: phase-transition checkpoint_atomic (start, elapsed, post)
        #   4:   start_ms before gate_runner.run_post_gate
        #   5:   end_ms after — 200_000 > default 120_000 → F_PIPE_03
        #   6+:  state-failure checkpoint (saturates at 200_000 so its own
        #        elapsed computes 0 — checkpoint completes cleanly).
        clock = _FakeClock(values=[0, 0, 0, 0, 200_000])
        with pytest.raises(F_PIPE_03):
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(hash_="h"),
                post_gate_input_factory=_FakeFactory(payload="x"),
                gate_runner=_FakeGateRunner(result=_mk_gate_result(passed=True)),
                vault_write=vault,
                clock=clock,
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )
        intents = [c["intent"] for c in vault.calls]
        assert intents == ["state-success", "state-failure"]


# ---------------------------------------------------------------------------
# Vault-error propagation (F_PIPE_01 from Round 2)
# ---------------------------------------------------------------------------


class TestVaultErrorPropagation:
    def test_phase_checkpoint_f_pipe_01_surfaces_unwrapped(self) -> None:
        from pipeline.vault.error_codes import VaultCASHeadMismatch

        def _always_cas_miss(
            *,
            path: str,
            payload: bytes,
            intent: str,
            write_mode: str,
            expected_current_file_hash: str | None,
        ) -> str:
            # Only mismatch the CAS-pinned state.json writes. The quarantine
            # marker (state-success / expected_current_file_hash=None) must
            # fall through as a real write.
            if (
                intent == "state-success"
                and expected_current_file_hash is not None
            ):
                raise VaultCASHeadMismatch(
                    "cas",
                    expected_current_file_hash=expected_current_file_hash or "",
                    actual_current_file_hash="other",
                )
            import hashlib as _hl

            return _hl.sha256(payload).hexdigest()

        from pipeline.loop.errors import F_PIPE_01

        rs = _mk_runstate(phase="inner_loop_iter_1")
        vault = _FakeVault(override=_always_cas_miss)
        # Clock monotonically increasing well past 10 s total timeout to
        # exhaust the CAS attempt budget.
        clock = _FakeClock(values=[0, 20_000, 20_001, 20_002, 20_003, 20_004])
        with pytest.raises(F_PIPE_01):
            run_post_gate_orchestration(
                run_state=rs,
                inner_loop_result=_mk_inner_loop_result(hash_="h"),
                post_gate_input_factory=_FakeFactory(payload="x"),
                gate_runner=_FakeGateRunner(result=_mk_gate_result(passed=True)),
                vault_write=vault,
                clock=clock,
                sleep=_FakeSleep(),
                initial_checkpoint_hash="h",
            )
        # Phase must have flipped to quarantined per Round 2 contract.
        assert rs.phase == "quarantined"
