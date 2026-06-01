"""Tests for pipeline.loop.revision_loop — §4.6 run_inner_loop (Round 5).

Blueprint §5 v6 LOCKED 2026-04-19.

Covers the spec card's test surface:

- Happy paths: iter-1 PASS, iter-2 PASS, iter-3 PASS, delta-plateau at iter-2,
  delta-plateau at iter-3.
- Iteration-cap exhaustion → ``F_PIPE_05`` + final state-failure checkpoint.
- Judge parse failure (F_PIPE_09) at iter-1 and iter-2.
- A-v1-02 landed-family recording: scribe → editor → judge immediate record.
- A-v1-10 soft-restart guard: pre-existing iter_n triggers ``F_PIPE_19``.
- A-v1-11 interrupt: probe True after iter-1 → ``F_PIPE_11`` (state durable).
- Inter-iteration ``run_iteration_families_so_far`` reset.
- Convergence: score-threshold vs delta-plateau correctly discriminated.
- CAS checkpoint-hash threading across iterations.
- Per-iteration phase-transition sequence.
- Thin wrapper re-exports via pipeline.loop package.

Adversarial surfaces live in ``test_adv_revision_loop.py``.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.loop.errors import F_PIPE_05, F_PIPE_06, F_PIPE_09, F_PIPE_11, F_PIPE_19
from pipeline.loop.revision_loop import (
    BLUEPRINT_DEPS,
    InnerLoopResult,
    InterruptProbe,
    SeatContextFactory,
    _assert_phase_is_inner_loop_iter,
    _assert_soft_restart_not_forbidden,
    _build_iteration_state_failure,
    _delta_plateau,
    run_inner_loop,
)
from pipeline.loop.seat_runner import (
    SeatInvocationContext,
    SubprocessResult,
)
from pipeline.loop.types import (
    IterationState,
    ProviderCascade,
    RunState,
    SeatCharter,
)


# ---------------------------------------------------------------------------
# Fakes — in-memory vault + deterministic clock + programmable launcher
# ---------------------------------------------------------------------------


@dataclass
class _InMemoryVault:
    """Minimal VaultWriteCallable double.

    Stores all writes; returns sha256(payload) as committed_hash.
    Ignores expected_current_file_hash (CAS exercised in Round 2 tests).
    """

    writes: list[dict[str, Any]] = field(default_factory=list)

    def __call__(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        committed = hashlib.sha256(payload).hexdigest()
        self.writes.append(
            {
                "path": path,
                "intent": intent,
                "write_mode": write_mode,
                "expected_current_file_hash": expected_current_file_hash,
                "committed_hash": committed,
            }
        )
        return committed


@dataclass
class _Clock:
    ticks_iso: list[str] = field(
        default_factory=lambda: [f"2026-04-20T10:00:{n:02d}Z" for n in range(60)]
    )
    ticks_ms: list[int] = field(
        default_factory=lambda: list(range(0, 60_000, 100))
    )
    iso_idx: int = 0
    ms_idx: int = 0

    def now_iso(self) -> str:
        v = self.ticks_iso[min(self.iso_idx, len(self.ticks_iso) - 1)]
        self.iso_idx += 1
        return v

    def now_ms(self) -> int:
        v = self.ticks_ms[min(self.ms_idx, len(self.ticks_ms) - 1)]
        self.ms_idx += 1
        return v


def _no_sleep(_ms: int) -> None:
    return None


@dataclass
class _FakeLauncher:
    """Programmable SubprocessLauncher — returns pre-seeded results per seat."""

    per_seat: dict[str, list[SubprocessResult]] = field(default_factory=dict)
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(
        self,
        *,
        seat_kind: str,
        env: dict[str, str],
        stdin_payload: bytes,
        timeout_ms: int,
        family: str,
        model_id: str,
    ) -> SubprocessResult:
        self.calls.append(
            {
                "seat_kind": seat_kind,
                "family": family,
                "model_id": model_id,
                "stdin_payload": stdin_payload,
            }
        )
        q = self.per_seat.get(seat_kind, [])
        if q:
            return q.pop(0)
        # Default: generic success
        default_stdout = b'{"verdict": "FAIL", "total_score": 50}' if seat_kind == "judge" else b"draft"
        return SubprocessResult(
            exit_code=0,
            stdout=default_stdout,
            stderr=b"",
            timed_out=False,
            landed_family=family,
            landed_model_id=model_id,
        )


def _verdict_result(
    *, family: str = "openai", model_id: str = "gpt-5", verdict: str = "PASS", score: int = 90
) -> SubprocessResult:
    import json

    return SubprocessResult(
        exit_code=0,
        stdout=json.dumps({"verdict": verdict, "total_score": score}).encode("utf-8"),
        stderr=b"",
        timed_out=False,
        landed_family=family,
        landed_model_id=model_id,
    )


def _seat_result(
    *, family: str = "anthropic", model_id: str = "claude-opus-4-7", stdout: bytes = b"draft"
) -> SubprocessResult:
    return SubprocessResult(
        exit_code=0,
        stdout=stdout,
        stderr=b"",
        timed_out=False,
        landed_family=family,
        landed_model_id=model_id,
    )


@dataclass
class _ContextFactory:
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(
        self,
        *,
        seat_kind: str,
        iter_n: int,
        prev_editor_hash: str | None,
        prev_judge_hash: str | None,
        run_state: RunState,
    ) -> SeatInvocationContext:
        self.calls.append(
            {
                "seat_kind": seat_kind,
                "iter_n": iter_n,
                "prev_editor_hash": prev_editor_hash,
                "prev_judge_hash": prev_judge_hash,
            }
        )
        return SeatInvocationContext(
            stdin_payload=f"{seat_kind}-iter-{iter_n}".encode("utf-8"),
            session_id=run_state.session_id,
            path_value="/usr/bin:/bin",
            home_value="/home/tilth",
        )


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def _run_state(
    *,
    run_id: str = "run-test-1",
    session_id: str = "sess-1",
    org_slug: str = "org-fitfarms",
    phase: str = "inner_loop_iter_1",
    iterations: list[IterationState] | None = None,
) -> RunState:
    rs = RunState(
        schema_version=2,
        run_id=run_id,
        mode="submission",
        rfa_hash="rfa-01",
        project_context_hash="pc-01",
        golden_set_ref=None,
        org_slug=org_slug,
        session_id=session_id,
        phase=phase,
    )
    if iterations:
        rs.iterations.extend(iterations)
    return rs


def _charter(seat_kind: str) -> SeatCharter:
    return SeatCharter(
        seat_kind=seat_kind,
        allowed_families=frozenset({"anthropic", "google", "openai"}),
        primary_model="primary",
        cascade_level=0,
        subprocess_timeout_ms=180_000,
    )


def _cascade(seat_kind: str, *, primary_family: str = "anthropic") -> ProviderCascade:
    # Distinct per-seat primary families so Round 4's cross-family guard does
    # not accidentally skip levels in the default happy-path tests.
    levels: tuple[tuple[str, str], ...]
    if seat_kind == "scribe":
        levels = (("anthropic", "claude-opus"), ("google", "gemini"), ("openai", "gpt"))
    elif seat_kind == "editor":
        levels = (("google", "gemini"), ("openai", "gpt"), ("meta", "llama"))
    else:  # judge
        levels = (("openai", "gpt"), ("meta", "llama"), ("mistral", "mixtral"))
    return ProviderCascade(seat_kind=seat_kind, levels=levels, current_level=0)


def _default_deps():
    vault = _InMemoryVault()
    clock = _Clock()
    launcher = _FakeLauncher()
    factory = _ContextFactory()
    return vault, clock, launcher, factory


def _run_with(
    run_state: RunState,
    *,
    launcher: _FakeLauncher,
    factory: _ContextFactory,
    vault: _InMemoryVault,
    clock: _Clock,
    interrupt_probe: InterruptProbe | None = None,
    initial_checkpoint_hash: str | None = None,
) -> InnerLoopResult:
    return run_inner_loop(
        run_state=run_state,
        scribe_charter=_charter("scribe"),
        editor_charter=_charter("editor"),
        judge_charter=_charter("judge"),
        scribe_cascade=_cascade("scribe"),
        editor_cascade=_cascade("editor"),
        judge_cascade=_cascade("judge"),
        context_factory=factory,
        subprocess_launcher=launcher,
        vault_write=vault,
        clock=clock,
        sleep=_no_sleep,
        initial_checkpoint_hash=initial_checkpoint_hash,
        interrupt_probe=interrupt_probe,
    )


# ===========================================================================
# Happy-path convergence
# ===========================================================================


class TestScoreThresholdConvergence:
    def test_iter_1_pass_returns_immediately(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result(family="anthropic", model_id="a1")],
            "editor": [_seat_result(family="google", model_id="g1", stdout=b"editor-draft")],
            "judge": [_verdict_result(family="openai", model_id="gpt-5", verdict="PASS", score=90)],
        }

        result = _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert isinstance(result, InnerLoopResult)
        assert result.converged_on == "score_threshold"
        assert result.iterations_run == 1
        assert result.final_iteration.iter_number == 1
        assert result.final_iteration.judge_verdict == {"verdict": "PASS", "total_score": 90}
        assert result.final_iteration.failure_code is None
        assert len(rs.iterations) == 1
        # phase-success + success-after-seats = 2 writes
        assert len(vault.writes) == 2
        assert all(w["intent"] == "state-success" for w in vault.writes)

    def test_iter_2_pass_after_iter_1_fail(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result(), _seat_result()],
            "editor": [_seat_result(family="google", model_id="g1"), _seat_result(family="google", model_id="g1")],
            "judge": [
                _verdict_result(verdict="FAIL", score=60),
                _verdict_result(verdict="PASS", score=85),
            ],
        }

        result = _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert result.converged_on == "score_threshold"
        assert result.iterations_run == 2
        assert result.final_iteration.iter_number == 2
        assert len(rs.iterations) == 2
        assert rs.iterations[0].judge_verdict == {"verdict": "FAIL", "total_score": 60}
        assert rs.iterations[1].judge_verdict == {"verdict": "PASS", "total_score": 85}

    def test_iter_3_pass_after_iter_1_2_fail(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result() for _ in range(3)],
            "editor": [_seat_result(family="google", model_id="g1") for _ in range(3)],
            "judge": [
                _verdict_result(verdict="FAIL", score=50),
                _verdict_result(verdict="FAIL", score=60),
                _verdict_result(verdict="PASS", score=92),
            ],
        }

        result = _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert result.converged_on == "score_threshold"
        assert result.iterations_run == 3
        assert len(rs.iterations) == 3


class TestDeltaPlateauConvergence:
    def test_iter_2_plateau_80_to_81(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result() for _ in range(2)],
            "editor": [_seat_result(family="google", model_id="g1") for _ in range(2)],
            "judge": [
                _verdict_result(verdict="FAIL", score=80),
                _verdict_result(verdict="FAIL", score=81),
            ],
        }

        result = _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert result.converged_on == "delta_plateau"
        assert result.iterations_run == 2

    def test_iter_3_plateau_75_to_76(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result() for _ in range(3)],
            "editor": [_seat_result(family="google", model_id="g1") for _ in range(3)],
            "judge": [
                _verdict_result(verdict="FAIL", score=50),
                _verdict_result(verdict="FAIL", score=75),
                _verdict_result(verdict="FAIL", score=76),
            ],
        }

        result = _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert result.converged_on == "delta_plateau"
        assert result.iterations_run == 3

    def test_iter_1_delta_plateau_not_detected(self) -> None:
        """Plateau requires iter_n >= 2 (two data points)."""
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result() for _ in range(3)],
            "editor": [_seat_result(family="google", model_id="g1") for _ in range(3)],
            "judge": [
                _verdict_result(verdict="FAIL", score=80),  # iter_1
                _verdict_result(verdict="FAIL", score=60),  # iter_2: delta=20, no plateau
                _verdict_result(verdict="FAIL", score=74),  # iter_3: below-floor, no plateau
            ],
        }

        with pytest.raises(F_PIPE_05):
            _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)


# ===========================================================================
# Iteration-cap exhaustion
# ===========================================================================


class TestIterationCap:
    def test_3_iter_fail_raises_f_pipe_05(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result() for _ in range(3)],
            "editor": [_seat_result(family="google", model_id="g1") for _ in range(3)],
            "judge": [
                _verdict_result(verdict="FAIL", score=50),
                _verdict_result(verdict="FAIL", score=60),  # delta=10
                _verdict_result(verdict="FAIL", score=70),  # delta=10
            ],
        }

        with pytest.raises(F_PIPE_05) as exc_info:
            _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert exc_info.value.trigger == "iteration_cap_exceeded"
        assert exc_info.value.details["iterations_completed"] == 3
        assert exc_info.value.details["iterations_allowed"] == 3
        # Final state-failure checkpoint was written
        assert vault.writes[-1]["intent"] == "state-failure"
        # All three iterations are recorded
        assert len(rs.iterations) == 3

    def test_cap_exceeded_preserves_all_iterations(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result() for _ in range(3)],
            "editor": [_seat_result(family="google", model_id="g1") for _ in range(3)],
            "judge": [
                _verdict_result(verdict="FAIL", score=30),
                _verdict_result(verdict="FAIL", score=60),
                _verdict_result(verdict="FAIL", score=40),
            ],
        }

        with pytest.raises(F_PIPE_05):
            _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert [it.iter_number for it in rs.iterations] == [1, 2, 3]
        assert all(it.failure_code is None for it in rs.iterations)
        assert rs.iterations[0].judge_verdict == {"verdict": "FAIL", "total_score": 30}


# ===========================================================================
# Judge-parse failure (F_PIPE_09)
# ===========================================================================


class TestJudgeParseFailure:
    def test_iter_1_judge_parse_fail(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result()],
            "editor": [_seat_result(family="google", model_id="g1")],
            "judge": [
                SubprocessResult(
                    exit_code=0,
                    stdout=b"not json",
                    stderr=b"",
                    timed_out=False,
                    landed_family="openai",
                    landed_model_id="gpt-5",
                )
            ],
        }

        with pytest.raises(F_PIPE_09):
            _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert len(rs.iterations) == 1
        it = rs.iterations[0]
        assert it.failure_code == "F-PIPE-09"
        assert it.judge_verdict is None
        assert it.seat_draft_hashes["scribe"]
        assert it.seat_draft_hashes["editor"]
        assert "judge" not in it.seat_draft_hashes
        # state-failure checkpoint written
        assert any(w["intent"] == "state-failure" for w in vault.writes)

    def test_iter_2_judge_parse_fail_iter_1_intact(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result(), _seat_result()],
            "editor": [_seat_result(family="google", model_id="g1"), _seat_result(family="google", model_id="g1")],
            "judge": [
                _verdict_result(verdict="FAIL", score=50),
                SubprocessResult(
                    exit_code=0,
                    stdout=b"still not json",
                    stderr=b"",
                    timed_out=False,
                    landed_family="openai",
                    landed_model_id="gpt-5",
                ),
            ],
        }

        with pytest.raises(F_PIPE_09):
            _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert len(rs.iterations) == 2
        # iter-1 success intact
        assert rs.iterations[0].failure_code is None
        assert rs.iterations[0].judge_verdict == {"verdict": "FAIL", "total_score": 50}
        # iter-2 failure stamped
        assert rs.iterations[1].failure_code == "F-PIPE-09"
        assert rs.iterations[1].judge_verdict is None


# ===========================================================================
# Generic PipelineFailure re-raise
# ===========================================================================


class TestGenericPipelineFailure:
    def test_f_pipe_06_from_seat_runner_propagates(self) -> None:
        """Cascade exhaustion from Round 4 → iter IterationState stamped + re-raised."""
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        # Scribe cascade has 3 levels; all timeout → F_PIPE_06
        launcher.per_seat = {
            "scribe": [
                SubprocessResult(
                    exit_code=137, stdout=b"", stderr=b"", timed_out=True,
                    landed_family=f, landed_model_id=m,
                )
                for f, m in (("anthropic", "claude-opus"), ("google", "gemini"), ("openai", "gpt"))
            ],
        }

        with pytest.raises(F_PIPE_06):
            _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert len(rs.iterations) == 1
        assert rs.iterations[0].failure_code == "F-PIPE-06"
        # No scribe hash (Scribe never returned successfully)
        assert rs.iterations[0].seat_draft_hashes == {}


# ===========================================================================
# A-v1-02 landed-family recording
# ===========================================================================


class TestLandedFamilyRecording:
    def test_scribe_family_recorded_before_editor_launches(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result(family="anthropic", model_id="a1")],
            "editor": [_seat_result(family="google", model_id="g1")],
            "judge": [_verdict_result(verdict="PASS", score=90)],
        }

        _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        # After the run, families dict has final state from iter-1
        assert rs.run_iteration_families_so_far["scribe"] == ("anthropic", "a1")
        assert rs.run_iteration_families_so_far["editor"] == ("google", "g1")
        assert rs.run_iteration_families_so_far["judge"][0] == "openai"

    def test_inter_iteration_families_reset(self) -> None:
        """Between iter-1 and iter-2, run_iteration_families_so_far is cleared."""
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [
                _seat_result(family="anthropic", model_id="a1"),
                # iter-2 Scribe can now land on google WITHOUT Editor cross-family block
                # because families are cleared at iter-2 start
                _seat_result(family="google", model_id="g1"),
            ],
            "editor": [
                _seat_result(family="google", model_id="g1"),
                _seat_result(family="openai", model_id="gpt"),
            ],
            "judge": [
                _verdict_result(verdict="FAIL", score=50, family="openai", model_id="gpt"),
                _verdict_result(verdict="PASS", score=90, family="meta", model_id="llama"),
            ],
        }

        result = _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert result.iterations_run == 2
        # Final families dict shows iter-2's state only
        assert rs.run_iteration_families_so_far["scribe"] == ("google", "g1")


# ===========================================================================
# A-v1-07 phase-invariant
# ===========================================================================


class TestPhaseInvariant:
    def test_wrong_entry_phase_raises_assertion(self) -> None:
        rs = _run_state(phase="pre_gate_passed")
        vault, clock, launcher, factory = _default_deps()

        with pytest.raises(AssertionError, match="phase invariant"):
            _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

    def test_phase_advances_per_iteration(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result() for _ in range(2)],
            "editor": [_seat_result(family="google", model_id="g1") for _ in range(2)],
            "judge": [
                _verdict_result(verdict="FAIL", score=50),
                _verdict_result(verdict="PASS", score=90),
            ],
        }

        _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        # Final phase reflects iter-2
        assert rs.phase == "inner_loop_iter_2"


# ===========================================================================
# A-v1-10 soft-restart guard
# ===========================================================================


class TestSoftRestartGuard:
    def test_existing_iter_1_blocks_fresh_start(self) -> None:
        existing = IterationState(iter_number=1)
        rs = _run_state(iterations=[existing])
        vault, clock, launcher, factory = _default_deps()

        with pytest.raises(F_PIPE_19) as exc_info:
            _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert exc_info.value.trigger == "soft_restart_forbidden"
        assert exc_info.value.details["attempted_iter_n"] == 1

    def test_existing_iter_2_blocks_iter_1_entry(self) -> None:
        existing = IterationState(iter_number=2)
        rs = _run_state(iterations=[existing])
        vault, clock, launcher, factory = _default_deps()

        with pytest.raises(F_PIPE_19):
            _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

    def test_assert_helper_raises_on_regression(self) -> None:
        rs = _run_state(iterations=[IterationState(iter_number=3)])
        with pytest.raises(F_PIPE_19):
            _assert_soft_restart_not_forbidden(rs, 1)

    def test_assert_helper_passes_on_clean_state(self) -> None:
        rs = _run_state()
        # Should not raise.
        _assert_soft_restart_not_forbidden(rs, 1)


# ===========================================================================
# A-v1-11 interrupt
# ===========================================================================


class _StepProbe:
    def __init__(self, fire_after: int) -> None:
        self.calls = 0
        self.fire_after = fire_after

    def __call__(self) -> bool:
        self.calls += 1
        return self.calls > self.fire_after


class TestInterruptProbe:
    def test_interrupt_after_iter_1_raises_f_pipe_11(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result()],
            "editor": [_seat_result(family="google", model_id="g1")],
            "judge": [_verdict_result(verdict="FAIL", score=50)],
        }
        probe = _StepProbe(fire_after=0)  # fires on first call

        with pytest.raises(F_PIPE_11) as exc_info:
            _run_with(
                rs, launcher=launcher, factory=factory, vault=vault, clock=clock,
                interrupt_probe=probe,
            )

        assert exc_info.value.trigger == "operator_interrupt_post_checkpoint"
        assert exc_info.value.details["iter_number"] == 1
        # Iter-1 state IS durable
        assert len(rs.iterations) == 1
        assert rs.iterations[0].failure_code is None

    def test_none_probe_disables_interrupt(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result()],
            "editor": [_seat_result(family="google", model_id="g1")],
            "judge": [_verdict_result(verdict="PASS", score=90)],
        }
        result = _run_with(
            rs, launcher=launcher, factory=factory, vault=vault, clock=clock,
            interrupt_probe=None,
        )
        assert result.converged_on == "score_threshold"


# ===========================================================================
# Checkpoint / CAS-hash threading
# ===========================================================================


class TestCheckpointThreading:
    def test_final_checkpoint_hash_matches_last_write(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result()],
            "editor": [_seat_result(family="google", model_id="g1")],
            "judge": [_verdict_result(verdict="PASS", score=90)],
        }

        result = _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert result.final_checkpoint_hash == vault.writes[-1]["committed_hash"]

    def test_cas_hash_threaded_through_iterations(self) -> None:
        """Every write past the first carries the previous committed_hash as expected."""
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result(), _seat_result()],
            "editor": [_seat_result(family="google", model_id="g1"), _seat_result(family="google", model_id="g1")],
            "judge": [
                _verdict_result(verdict="FAIL", score=50),
                _verdict_result(verdict="PASS", score=90),
            ],
        }
        _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock,
                  initial_checkpoint_hash="INIT-HASH")

        # First write should carry "INIT-HASH" as expected_current_file_hash
        assert vault.writes[0]["expected_current_file_hash"] == "INIT-HASH"
        # Each subsequent write should carry the prior committed_hash
        for i in range(1, len(vault.writes)):
            assert vault.writes[i]["expected_current_file_hash"] == vault.writes[i - 1]["committed_hash"]

    def test_per_iteration_writes_two_state_success_checkpoints(self) -> None:
        """Each iteration writes: phase-transition + success-after-seats = 2 state-success."""
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result()],
            "editor": [_seat_result(family="google", model_id="g1")],
            "judge": [_verdict_result(verdict="PASS", score=90)],
        }
        _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)
        success_writes = [w for w in vault.writes if w["intent"] == "state-success"]
        assert len(success_writes) == 2


# ===========================================================================
# Context-factory surface
# ===========================================================================


class TestContextFactory:
    def test_factory_called_three_times_per_iteration(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result()],
            "editor": [_seat_result(family="google", model_id="g1")],
            "judge": [_verdict_result(verdict="PASS", score=90)],
        }
        _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert len(factory.calls) == 3
        assert [c["seat_kind"] for c in factory.calls] == ["scribe", "editor", "judge"]
        # All iter-1 calls have prev_editor_hash=None (first iteration)
        for c in factory.calls:
            assert c["iter_n"] == 1
            assert c["prev_editor_hash"] is None
            assert c["prev_judge_hash"] is None

    def test_iter_2_factory_receives_prev_iter_hashes(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result(stdout=b"iter1-scribe"), _seat_result(stdout=b"iter2-scribe")],
            "editor": [
                _seat_result(family="google", model_id="g1", stdout=b"iter1-editor"),
                _seat_result(family="google", model_id="g1", stdout=b"iter2-editor"),
            ],
            "judge": [
                _verdict_result(verdict="FAIL", score=50),
                _verdict_result(verdict="PASS", score=90),
            ],
        }
        _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        iter2_calls = [c for c in factory.calls if c["iter_n"] == 2]
        assert len(iter2_calls) == 3
        iter1_editor_hash = hashlib.sha256(b"iter1-editor").hexdigest()
        iter1_judge_hash_match = [c for c in factory.calls if c["iter_n"] == 2][0]
        # iter-2 Scribe should receive iter-1's editor + judge hashes
        assert iter1_judge_hash_match["prev_editor_hash"] == iter1_editor_hash
        assert iter1_judge_hash_match["prev_judge_hash"] is not None


# ===========================================================================
# InnerLoopResult shape
# ===========================================================================


class TestInnerLoopResultShape:
    def test_result_is_frozen(self) -> None:
        rs = _run_state()
        vault, clock, launcher, factory = _default_deps()
        launcher.per_seat = {
            "scribe": [_seat_result()],
            "editor": [_seat_result(family="google", model_id="g1")],
            "judge": [_verdict_result(verdict="PASS", score=90)],
        }
        result = _run_with(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)
        with pytest.raises(Exception):
            result.iterations_run = 99  # type: ignore[misc]


# ===========================================================================
# _delta_plateau helper
# ===========================================================================


class TestDeltaPlateauHelper:
    def test_fewer_than_two_iterations_returns_false(self) -> None:
        assert _delta_plateau([]) is False
        assert _delta_plateau([IterationState(iter_number=1)]) is False

    def test_both_scores_below_75_returns_false(self) -> None:
        iters = [
            IterationState(iter_number=1, judge_verdict={"verdict": "FAIL", "total_score": 70}),
            IterationState(iter_number=2, judge_verdict={"verdict": "FAIL", "total_score": 71}),
        ]
        assert _delta_plateau(iters) is False

    def test_one_score_below_75_returns_false(self) -> None:
        iters = [
            IterationState(iter_number=1, judge_verdict={"verdict": "FAIL", "total_score": 74}),
            IterationState(iter_number=2, judge_verdict={"verdict": "FAIL", "total_score": 75}),
        ]
        assert _delta_plateau(iters) is False

    def test_delta_above_2_returns_false(self) -> None:
        iters = [
            IterationState(iter_number=1, judge_verdict={"verdict": "FAIL", "total_score": 80}),
            IterationState(iter_number=2, judge_verdict={"verdict": "FAIL", "total_score": 83}),
        ]
        assert _delta_plateau(iters) is False

    def test_exact_plateau_succeeds(self) -> None:
        iters = [
            IterationState(iter_number=1, judge_verdict={"verdict": "FAIL", "total_score": 75}),
            IterationState(iter_number=2, judge_verdict={"verdict": "FAIL", "total_score": 77}),
        ]
        assert _delta_plateau(iters) is True

    def test_missing_total_score_returns_false(self) -> None:
        iters = [
            IterationState(iter_number=1, judge_verdict={"verdict": "FAIL"}),
            IterationState(iter_number=2, judge_verdict={"verdict": "FAIL", "total_score": 80}),
        ]
        assert _delta_plateau(iters) is False

    def test_non_numeric_score_returns_false(self) -> None:
        iters = [
            IterationState(iter_number=1, judge_verdict={"verdict": "FAIL", "total_score": "eighty"}),
            IterationState(iter_number=2, judge_verdict={"verdict": "FAIL", "total_score": 80}),
        ]
        assert _delta_plateau(iters) is False

    def test_none_judge_verdict_returns_false(self) -> None:
        iters = [
            IterationState(iter_number=1, judge_verdict=None),
            IterationState(iter_number=2, judge_verdict={"verdict": "FAIL", "total_score": 80}),
        ]
        assert _delta_plateau(iters) is False


# ===========================================================================
# Phase-invariant helper
# ===========================================================================


class TestPhaseInvariantHelper:
    def test_correct_phase_passes(self) -> None:
        rs = _run_state(phase="inner_loop_iter_2")
        _assert_phase_is_inner_loop_iter(rs, 2)  # no raise

    def test_wrong_phase_raises_assertion_error(self) -> None:
        rs = _run_state(phase="pre_gate_passed")
        with pytest.raises(AssertionError):
            _assert_phase_is_inner_loop_iter(rs, 1)


# ===========================================================================
# IterationState failure builder
# ===========================================================================


class TestIterationStateFailureBuilder:
    def test_builds_expected_failure_shape(self) -> None:
        it = _build_iteration_state_failure(
            iter_n=2,
            seat_draft_hashes={"scribe": "abc", "editor": "def"},
            failure_code="F-PIPE-09",
            started_at_iso="2026-04-20T10:00:00Z",
            completed_at_iso="2026-04-20T10:00:05Z",
        )
        assert it.iter_number == 2
        assert it.seat_draft_hashes == {"scribe": "abc", "editor": "def"}
        assert it.judge_verdict is None
        assert it.failure_code == "F-PIPE-09"


# ===========================================================================
# Blueprint & structural
# ===========================================================================


class TestStructural:
    def test_blueprint_deps_carries_v6_hash(self) -> None:
        assert BLUEPRINT_DEPS["section_05_pipeline.md"]["version"] == "v6"
        assert (
            BLUEPRINT_DEPS["section_05_pipeline.md"]["hash_sha3_512_prefix16"]
            == "feb5928491e4dc40"
        )

    def test_interrupt_probe_is_runtime_checkable(self) -> None:
        def probe() -> bool:
            return False

        assert isinstance(probe, InterruptProbe)

    def test_context_factory_is_runtime_checkable(self) -> None:
        factory = _ContextFactory()
        assert isinstance(factory, SeatContextFactory)

    def test_package_reexports_round_5_api(self) -> None:
        from pipeline.loop import (
            InnerLoopResult as R_InnerLoopResult,
            InterruptProbe as R_InterruptProbe,
            SeatContextFactory as R_SeatContextFactory,
            run_inner_loop as r_run_inner_loop,
        )
        assert R_InnerLoopResult is InnerLoopResult
        assert R_InterruptProbe is InterruptProbe
        assert R_SeatContextFactory is SeatContextFactory
        assert r_run_inner_loop is run_inner_loop
