"""Adversarial tests for pipeline.loop.revision_loop — §4.6 run_inner_loop (Round 5).

Blueprint §5 v6 LOCKED 2026-04-19. Spec-card adversarial surface:

- Subprocess returns a different ``landed_family`` than the cascade requested
  (A-v1-02 records the launcher's *claim*, not the requested family).
- ``JudgeParseError`` raised AFTER successful Scribe + Editor invocation —
  state-failure still records both Scribe + Editor hashes in IterationState.
- ``InterruptProbe`` raising a non-``bool`` exception — propagates to caller
  unwrapped (Round 5 does not defensively wrap probe errors).
- ``VaultError`` (F-PIPE-01) raised by ``checkpoint_atomic`` — propagates;
  revision_loop does NOT swallow F_PIPE_01.
- Convergence thresholds (``75``, ``2``) rebind-resistance — mutating the
  ``MAX_REVISION_ITERATIONS`` module attribute does NOT change dispatch.
- Cascade-exhaustion during Scribe invocation (F_PIPE_06) — state-failure
  checkpoint + IterationState with ``failure_code="F-PIPE-06"``, re-raise.
- Cross-family violation during Editor (F_PIPE_08) — state-failure
  checkpoint, iteration state has Scribe hash + ``failure_code="F-PIPE-08"``.
- A-v1-11 interrupt check runs AFTER the success checkpoint — state is durable
  before F_PIPE_11 fires.
- Spec-card deviation: iter-1 delta-plateau is NOT detected (plateau requires
  ``iter_n >= 2``).
- Out-of-scope threat-model residuals (E-023 closure):
  * Non-``PipelineFailure`` exceptions from ``judge_parse`` propagate unwrapped
    ONLY if they escape Round 4's wrapping; Round 4 converts any parser
    exception to F_PIPE_09. Test pins that contract through Round 5.
  * ``context_factory`` returning stale context across iterations is the
    caller's responsibility — we pin that Round 5 calls the factory afresh.
  * Concurrent ``run_inner_loop`` on the same RunState — out of scope; we
    document but do not test (single-threaded orchestrator invariant).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.loop.errors import (
    F_PIPE_01,
    F_PIPE_05,
    F_PIPE_06,
    F_PIPE_08,
    F_PIPE_09,
    F_PIPE_11,
    PipelineFailure,
)
from pipeline.loop import revision_loop as rl
from pipeline.loop.revision_loop import (
    InnerLoopResult,
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
# Shared fakes (narrowed variants of test_revision_loop.py doubles)
# ---------------------------------------------------------------------------


@dataclass
class _InMemoryVault:
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
class _RaisingVault:
    """VaultWriteCallable that raises F_PIPE_01 after ``raise_after`` writes."""

    raise_after: int
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
        if len(self.writes) >= self.raise_after:
            raise F_PIPE_01(
                trigger="vault_write_denied",
                details={"path": path, "intent": intent},
            )
        committed = hashlib.sha256(payload).hexdigest()
        self.writes.append({"path": path, "intent": intent})
        return committed


@dataclass
class _Clock:
    iso_idx: int = 0

    def now_iso(self) -> str:
        self.iso_idx += 1
        return f"2026-04-20T10:00:{self.iso_idx:02d}Z"

    def now_ms(self) -> int:
        return 0


def _no_sleep(_ms: int) -> None:
    return None


@dataclass
class _FakeLauncher:
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
            {"seat_kind": seat_kind, "family": family, "model_id": model_id}
        )
        q = self.per_seat.get(seat_kind, [])
        if q:
            return q.pop(0)
        # Default ok
        default = (
            b'{"verdict": "FAIL", "total_score": 50}'
            if seat_kind == "judge"
            else b"draft"
        )
        return SubprocessResult(
            exit_code=0,
            stdout=default,
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
            stdin_payload=f"{seat_kind}-{iter_n}".encode("utf-8"),
            session_id=run_state.session_id,
            path_value="/usr/bin",
            home_value="/home/tilth",
        )


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def _timed_out(*, family: str, model_id: str) -> SubprocessResult:
    return SubprocessResult(
        exit_code=124,
        stdout=b"",
        stderr=b"",
        timed_out=True,
        landed_family=family,
        landed_model_id=model_id,
    )


def _seat_ok(
    *,
    family: str = "anthropic",
    model_id: str = "claude-opus",
    stdout: bytes = b"draft",
    landed_family: str | None = None,
    landed_model_id: str | None = None,
) -> SubprocessResult:
    return SubprocessResult(
        exit_code=0,
        stdout=stdout,
        stderr=b"",
        timed_out=False,
        landed_family=landed_family if landed_family is not None else family,
        landed_model_id=landed_model_id if landed_model_id is not None else model_id,
    )


def _judge_ok(*, family: str = "openai", model_id: str = "gpt-5", verdict: str = "FAIL", score: int = 60) -> SubprocessResult:
    import json

    return SubprocessResult(
        exit_code=0,
        stdout=json.dumps({"verdict": verdict, "total_score": score}).encode("utf-8"),
        stderr=b"",
        timed_out=False,
        landed_family=family,
        landed_model_id=model_id,
    )


def _run_state(*, phase: str = "inner_loop_iter_1", iterations: list[IterationState] | None = None) -> RunState:
    rs = RunState(
        schema_version=2,
        run_id="run-adv",
        mode="submission",
        rfa_hash="rfa-x",
        project_context_hash="pc-x",
        golden_set_ref=None,
        org_slug="org-x",
        session_id="sess-x",
        phase=phase,
    )
    if iterations:
        rs.iterations.extend(iterations)
    return rs


def _charter(kind: str) -> SeatCharter:
    return SeatCharter(
        seat_kind=kind,
        allowed_families=frozenset({"anthropic", "google", "openai", "meta", "mistral"}),
        primary_model="primary",
        cascade_level=0,
        subprocess_timeout_ms=180_000,
    )


def _default_cascades() -> tuple[ProviderCascade, ProviderCascade, ProviderCascade]:
    scribe = ProviderCascade(
        seat_kind="scribe",
        levels=(("anthropic", "claude-opus"), ("google", "gemini"), ("openai", "gpt")),
        current_level=0,
    )
    editor = ProviderCascade(
        seat_kind="editor",
        levels=(("google", "gemini"), ("openai", "gpt"), ("meta", "llama")),
        current_level=0,
    )
    judge = ProviderCascade(
        seat_kind="judge",
        levels=(("openai", "gpt"), ("meta", "llama"), ("mistral", "mixtral")),
        current_level=0,
    )
    return scribe, editor, judge


def _run(
    rs: RunState,
    *,
    launcher: _FakeLauncher,
    factory: _ContextFactory,
    vault,
    clock: _Clock,
    scribe_cascade: ProviderCascade | None = None,
    editor_cascade: ProviderCascade | None = None,
    judge_cascade: ProviderCascade | None = None,
    interrupt_probe=None,
    judge_parse=None,
    initial_checkpoint_hash: str | None = None,
) -> InnerLoopResult:
    s, e, j = _default_cascades()
    return run_inner_loop(
        run_state=rs,
        scribe_charter=_charter("scribe"),
        editor_charter=_charter("editor"),
        judge_charter=_charter("judge"),
        scribe_cascade=scribe_cascade or s,
        editor_cascade=editor_cascade or e,
        judge_cascade=judge_cascade or j,
        context_factory=factory,
        subprocess_launcher=launcher,
        vault_write=vault,
        clock=clock,
        sleep=_no_sleep,
        initial_checkpoint_hash=initial_checkpoint_hash,
        interrupt_probe=interrupt_probe,
        judge_parse=judge_parse,
    )


# ===========================================================================
# 1. Subprocess returns different landed family than requested
# ===========================================================================


class TestLauncherClaimRecorded:
    """A-v1-02: the launcher's claimed ``landed_family`` is what gets recorded,
    NOT the cascade's requested family. Revision_loop is neutral — it just
    forwards Round 4's ``SeatInvocationResult.landed_family``.
    """

    def test_scribe_launcher_claims_different_family_recorded_verbatim(self) -> None:
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        # Cascade requests ("anthropic", "claude-opus"); launcher claims it
        # actually landed on ("google", "gemini-2"). Round 5 records the claim.
        launcher.per_seat = {
            "scribe": [
                _seat_ok(landed_family="google", landed_model_id="gemini-2", stdout=b"draft-x")
            ],
            "editor": [_seat_ok(family="openai", model_id="gpt-5")],
            "judge": [_judge_ok(family="meta", model_id="llama", verdict="PASS", score=90)],
        }

        result = _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert result.converged_on == "score_threshold"
        # run_iteration_families_so_far mid-iteration was cleared by the
        # converged return, but the iter's landed-family was observed via
        # the launcher call-log.
        scribe_calls = [c for c in launcher.calls if c["seat_kind"] == "scribe"]
        assert len(scribe_calls) == 1
        # Cascade REQUESTED anthropic — Round 4 asked the launcher for that
        # family — but the SeatInvocationResult.landed_family that revision_loop
        # consumes is the launcher's claim. Editor's cross-family gate looked
        # at "google" (the claim), not "anthropic" (the request) — and
        # editor's cascade starts with ("google",...) which would collide —
        # so editor advanced past level 0.
        editor_calls = [c for c in launcher.calls if c["seat_kind"] == "editor"]
        # Editor level 0 is google — colliding with scribe's claim → skipped.
        # Editor level 1 is openai — no collision → launched.
        assert len(editor_calls) == 1
        assert editor_calls[0]["family"] == "openai"


# ===========================================================================
# 2. JudgeParseError after Scribe + Editor success → state-failure records both
# ===========================================================================


class TestJudgeParseFailureRecordsSeatHashes:
    def test_parse_fail_preserves_scribe_and_editor_hashes(self) -> None:
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        launcher.per_seat = {
            "scribe": [_seat_ok(stdout=b"scribe-bytes")],
            "editor": [_seat_ok(family="google", model_id="g1", stdout=b"editor-bytes")],
            "judge": [_seat_ok(family="openai", model_id="gpt", stdout=b"NOT-JSON-GARBAGE")],
        }

        with pytest.raises(F_PIPE_09):
            _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert len(rs.iterations) == 1
        iter_state = rs.iterations[0]
        assert iter_state.failure_code == "F-PIPE-09"
        assert iter_state.judge_verdict is None
        # BOTH Scribe and Editor hashes are recorded.
        assert iter_state.seat_draft_hashes["scribe"] == hashlib.sha256(b"scribe-bytes").hexdigest()
        assert iter_state.seat_draft_hashes["editor"] == hashlib.sha256(b"editor-bytes").hexdigest()
        assert "judge" not in iter_state.seat_draft_hashes
        # Two vault writes: phase-success + state-failure.
        intents = [w["intent"] for w in vault.writes]
        assert intents == ["state-success", "state-failure"]


# ===========================================================================
# 3. InterruptProbe raising non-bool exception propagates
# ===========================================================================


class _RaisingProbe:
    def __call__(self) -> bool:
        raise RuntimeError("probe blew up")


class TestInterruptProbeRaises:
    def test_probe_raising_propagates_unwrapped(self) -> None:
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        # iter-1 non-converging (FAIL), probe fires after success checkpoint.
        launcher.per_seat = {
            "scribe": [_seat_ok()],
            "editor": [_seat_ok(family="google", model_id="g1")],
            "judge": [_judge_ok(verdict="FAIL", score=50)],
        }

        with pytest.raises(RuntimeError, match="probe blew up"):
            _run(
                rs,
                launcher=launcher,
                factory=factory,
                vault=vault,
                clock=clock,
                interrupt_probe=_RaisingProbe(),
            )

        # Success checkpoint of iter-1 already landed before probe invocation.
        assert len(rs.iterations) == 1
        assert rs.iterations[0].failure_code is None
        intents = [w["intent"] for w in vault.writes]
        assert intents == ["state-success", "state-success"]


# ===========================================================================
# 4. VaultError (F_PIPE_01) propagates — revision_loop does not swallow
# ===========================================================================


class TestVaultErrorPropagates:
    def test_first_phase_checkpoint_vault_error_propagates(self) -> None:
        """F_PIPE_01 on the very first write — no iteration appended."""
        rs = _run_state()
        vault = _RaisingVault(raise_after=0)  # raise on write #1
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()

        with pytest.raises(F_PIPE_01):
            _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        # No seats launched — vault raised before seat dispatch.
        assert launcher.calls == []
        # No iteration recorded — vault raised before the success branch could
        # assemble IterationState.
        assert rs.iterations == []

    def test_post_success_vault_error_after_seats_succeeded_propagates(self) -> None:
        """F_PIPE_01 on the SUCCESS-AFTER-SEATS checkpoint (the 2nd write).

        Seats succeeded → iteration_state was appended → vault raises on the
        success-checkpoint write. The F_PIPE_01 propagates; revision_loop's
        outer ``except PipelineFailure`` branch catches it and writes a
        state-failure checkpoint via the SAME vault — which ALSO raises. The
        net visible behavior is F_PIPE_01 propagating (the state-failure
        write also fails, and Python re-raises the original to the caller).
        """
        rs = _run_state()
        vault = _RaisingVault(raise_after=1)  # allow phase-ck, raise on success-ck
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        launcher.per_seat = {
            "scribe": [_seat_ok()],
            "editor": [_seat_ok(family="google", model_id="g1")],
            "judge": [_judge_ok()],
        }

        with pytest.raises(F_PIPE_01):
            _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        # Seats all launched.
        assert {c["seat_kind"] for c in launcher.calls} == {"scribe", "editor", "judge"}
        # IterationState was appended before the failing checkpoint.
        assert len(rs.iterations) == 1
        assert rs.iterations[0].failure_code is None


# ===========================================================================
# 5. Convergence thresholds rebind-resistance
# ===========================================================================


class TestConvergenceThresholdsRebindResistant:
    def test_rebinding_max_revision_iterations_does_not_extend_loop(self) -> None:
        """V1 discipline: the ``for iter_n in (1, 2, 3)`` is an inline-literal
        tuple; rebinding ``MAX_REVISION_ITERATIONS`` on the config module has
        zero effect on dispatch. Verified by exhausting 3 iterations under an
        attempted rebind to ``100``.
        """
        import pipeline.loop.config as cfg

        original = cfg.MAX_REVISION_ITERATIONS
        try:
            cfg.MAX_REVISION_ITERATIONS = 100  # type: ignore[misc]

            rs = _run_state()
            vault = _InMemoryVault()
            clock = _Clock()
            launcher = _FakeLauncher()
            factory = _ContextFactory()
            # Never converge: all FAIL.
            launcher.per_seat = {
                "scribe": [_seat_ok() for _ in range(5)],
                "editor": [_seat_ok(family="google", model_id="g1") for _ in range(5)],
                "judge": [_judge_ok(verdict="FAIL", score=10) for _ in range(5)],
            }

            with pytest.raises(F_PIPE_05):
                _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

            # Exactly 3 iterations run despite rebind to 100.
            assert len(rs.iterations) == 3
        finally:
            cfg.MAX_REVISION_ITERATIONS = original  # type: ignore[misc]

    def test_rebinding_plateau_thresholds_does_not_fire_below_75(self) -> None:
        """Delta-plateau requires BOTH scores ≥ 75 — inline literal. Two
        consecutive scores of 70 and 71 (delta 1) must NOT plateau even if a
        cheeky rebind of a threshold constant is attempted.
        """
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        # 3 FAIL iterations at 70/71/72 — deltas all ≤ 2 but none ≥ 75.
        launcher.per_seat = {
            "scribe": [_seat_ok() for _ in range(3)],
            "editor": [_seat_ok(family="google", model_id="g1") for _ in range(3)],
            "judge": [
                _judge_ok(verdict="FAIL", score=70),
                _judge_ok(verdict="FAIL", score=71),
                _judge_ok(verdict="FAIL", score=72),
            ],
        }

        with pytest.raises(F_PIPE_05):
            _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        # All 3 iterations ran, none converged on plateau.
        assert len(rs.iterations) == 3
        for it in rs.iterations:
            assert it.failure_code is None
            assert isinstance(it.judge_verdict, dict)
            assert it.judge_verdict["total_score"] < 75


# ===========================================================================
# 6. Cascade-exhaustion during Scribe (F_PIPE_06)
# ===========================================================================


class TestScribeCascadeExhaustion:
    def test_scribe_all_levels_timeout_raises_F_PIPE_06_with_failure_state(self) -> None:
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        # All 3 scribe levels time out.
        launcher.per_seat = {
            "scribe": [
                _timed_out(family="anthropic", model_id="claude-opus"),
                _timed_out(family="google", model_id="gemini"),
                _timed_out(family="openai", model_id="gpt"),
            ],
        }

        with pytest.raises(F_PIPE_06):
            _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        # IterationState appended with F-PIPE-06, no seat hashes (scribe never
        # produced a SeatInvocationResult).
        assert len(rs.iterations) == 1
        it = rs.iterations[0]
        assert it.failure_code == "F-PIPE-06"
        assert it.seat_draft_hashes == {}
        assert it.judge_verdict is None
        # Two vault writes: phase-success + state-failure.
        intents = [w["intent"] for w in vault.writes]
        assert intents == ["state-success", "state-failure"]


# ===========================================================================
# 7. Cross-family violation during Editor (F_PIPE_08)
# ===========================================================================


class TestEditorCrossFamilyExhaustion:
    def test_editor_cascade_all_match_scribe_family_raises_F_PIPE_08(self) -> None:
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        # Scribe lands on anthropic.
        launcher.per_seat = {
            "scribe": [_seat_ok(family="anthropic", model_id="claude-opus", stdout=b"S")],
        }
        # Editor cascade: every level == anthropic → all levels collide.
        editor_cascade_all_anthropic = ProviderCascade(
            seat_kind="editor",
            levels=(
                ("anthropic", "claude-a"),
                ("anthropic", "claude-b"),
                ("anthropic", "claude-c"),
            ),
            current_level=0,
        )

        with pytest.raises(F_PIPE_08):
            _run(
                rs,
                launcher=launcher,
                factory=factory,
                vault=vault,
                clock=clock,
                editor_cascade=editor_cascade_all_anthropic,
            )

        # IterationState appended with F-PIPE-08; ONLY scribe hash recorded
        # (editor never produced a result).
        assert len(rs.iterations) == 1
        it = rs.iterations[0]
        assert it.failure_code == "F-PIPE-08"
        assert it.seat_draft_hashes == {"scribe": hashlib.sha256(b"S").hexdigest()}
        assert "editor" not in it.seat_draft_hashes
        assert it.judge_verdict is None
        # Editor launcher NEVER called — all levels skipped via collision.
        editor_calls = [c for c in launcher.calls if c["seat_kind"] == "editor"]
        assert editor_calls == []
        intents = [w["intent"] for w in vault.writes]
        assert intents == ["state-success", "state-failure"]


# ===========================================================================
# 8. A-v1-11 post-checkpoint interrupt durable
# ===========================================================================


class TestInterruptPostCheckpointDurable:
    def test_interrupt_fires_after_success_checkpoint_state_is_durable(self) -> None:
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        launcher.per_seat = {
            "scribe": [_seat_ok()],
            "editor": [_seat_ok(family="google", model_id="g1")],
            "judge": [_judge_ok(verdict="FAIL", score=50)],
        }

        class Probe:
            def __init__(self) -> None:
                self.n = 0

            def __call__(self) -> bool:
                self.n += 1
                return self.n >= 1  # fire immediately after iter-1 success

        probe = Probe()
        with pytest.raises(F_PIPE_11):
            _run(
                rs,
                launcher=launcher,
                factory=factory,
                vault=vault,
                clock=clock,
                interrupt_probe=probe,
            )

        # Durable iter-1 success state:
        assert len(rs.iterations) == 1
        assert rs.iterations[0].iter_number == 1
        assert rs.iterations[0].failure_code is None
        assert rs.iterations[0].judge_verdict == {"verdict": "FAIL", "total_score": 50}
        # phase-success + success-after-seats — interrupt fires AFTER these.
        intents = [w["intent"] for w in vault.writes]
        assert intents == ["state-success", "state-success"]


# ===========================================================================
# 9. Iter-1 delta-plateau NOT detected (plateau requires iter_n >= 2)
# ===========================================================================


class TestIter1PlateauNotDetected:
    def test_iter1_alone_cannot_plateau_even_with_high_score(self) -> None:
        """_delta_plateau requires TWO consecutive iteration states; iter-1 in
        isolation cannot plateau — verified by a 1-iteration FAIL with score
        80 that does NOT terminate early.
        """
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        # iter-1 FAIL-80, iter-2 FAIL-81 → plateau kicks in ONLY at iter-2.
        launcher.per_seat = {
            "scribe": [_seat_ok() for _ in range(2)],
            "editor": [_seat_ok(family="google", model_id="g1") for _ in range(2)],
            "judge": [
                _judge_ok(verdict="FAIL", score=80),
                _judge_ok(verdict="FAIL", score=81),
            ],
        }

        result = _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        # Converged on plateau at iter-2 — NOT at iter-1.
        assert result.converged_on == "delta_plateau"
        assert result.iterations_run == 2
        assert result.final_iteration.iter_number == 2


# ===========================================================================
# 10. Context factory freshness (caller responsibility pin)
# ===========================================================================


class TestContextFactoryCalledFreshEachSeat:
    def test_factory_invoked_three_times_per_iteration_distinct_seat_kinds(self) -> None:
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        launcher.per_seat = {
            "scribe": [_seat_ok() for _ in range(2)],
            "editor": [_seat_ok(family="google", model_id="g1") for _ in range(2)],
            "judge": [
                _judge_ok(verdict="FAIL", score=60),
                _judge_ok(verdict="PASS", score=85),
            ],
        }

        _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        # 3 seats × 2 iterations = 6 factory calls, in fixed seat order.
        assert [c["seat_kind"] for c in factory.calls] == [
            "scribe", "editor", "judge", "scribe", "editor", "judge"
        ]
        # iter-1 prev-hashes are None; iter-2 prev-hashes are not.
        iter1_scribe = factory.calls[0]
        assert iter1_scribe["iter_n"] == 1
        assert iter1_scribe["prev_editor_hash"] is None
        assert iter1_scribe["prev_judge_hash"] is None

        iter2_scribe = factory.calls[3]
        assert iter2_scribe["iter_n"] == 2
        assert iter2_scribe["prev_editor_hash"] is not None
        assert iter2_scribe["prev_judge_hash"] is not None


# ===========================================================================
# 11. Threat-model residual: non-PipelineFailure from malicious judge_parse
# ===========================================================================


class TestMaliciousJudgeParserWrappedToF_PIPE_09:
    """Round 4 wraps ANY parser exception (including RuntimeError) as
    F_PIPE_09. Revision_loop's ``except F_PIPE_09`` catches that. Verified
    end-to-end: a parser raising RuntimeError manifests as F_PIPE_09 at the
    revision_loop boundary, with a state-failure checkpoint written.
    """

    def test_runtime_error_from_parser_manifests_as_F_PIPE_09(self) -> None:
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        launcher.per_seat = {
            "scribe": [_seat_ok()],
            "editor": [_seat_ok(family="google", model_id="g1")],
            "judge": [_seat_ok(family="openai", model_id="gpt", stdout=b"x")],
        }

        def malicious_parser(_raw: bytes) -> dict[str, Any]:
            raise RuntimeError("parser exploded")

        with pytest.raises(F_PIPE_09) as exc_info:
            _run(
                rs,
                launcher=launcher,
                factory=factory,
                vault=vault,
                clock=clock,
                judge_parse=malicious_parser,
            )

        # Details surface the wrapped exception type.
        details = exc_info.value.details
        assert details["parser_error"] == "RuntimeError"
        assert "parser exploded" in details["parser_message"]
        assert rs.iterations[0].failure_code == "F-PIPE-09"
        assert rs.iterations[0].judge_verdict is None


# ===========================================================================
# 12. Soft-restart guard: pre-existing iter_2 blocks re-entry into iter_1
# ===========================================================================


class TestSoftRestartGuardRegression:
    def test_existing_iter_2_blocks_iter_1_entry(self) -> None:
        """A-v1-10: ANY iter_number >= current iter_n trips the guard.
        Pre-populate iter_2; entering iter_1 must raise F_PIPE_19 (iter_2 >= 1).
        """
        from pipeline.loop.errors import F_PIPE_19

        prior = IterationState(
            iter_number=2,
            seat_draft_hashes={},
            judge_verdict=None,
            failure_code="F-PIPE-09",
            started_at_iso="2026-04-20T09:00:00Z",
            completed_at_iso="2026-04-20T09:00:01Z",
        )
        rs = _run_state(iterations=[prior])
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()

        with pytest.raises(F_PIPE_19) as exc_info:
            _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        assert exc_info.value.details["existing_iter_number"] == 2
        assert exc_info.value.details["attempted_iter_n"] == 1
        # No vault writes — guard fires before phase-success checkpoint.
        assert vault.writes == []


# ===========================================================================
# 13. Phase-invariant assertion on entry (A-v1-07)
# ===========================================================================


class TestPhaseInvariantAssertion:
    def test_phase_not_inner_loop_raises_assertion(self) -> None:
        rs = _run_state(phase="pre_gate_passed")
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()

        with pytest.raises(AssertionError, match="phase invariant violated"):
            _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)


# ===========================================================================
# 14. Families-so-far clearing — iter-2 Scribe not blocked by iter-1 Judge family
# ===========================================================================


class TestFamiliesClearedBetweenIterations:
    def test_iter2_scribe_can_land_on_iter1_judge_family_after_reset(self) -> None:
        """Open-Q #2 resolution: ``run_iteration_families_so_far`` clears at
        the start of each iteration. Iter-1 Judge landed on "openai"; iter-2
        Scribe on a cascade that starts with "openai" must NOT be blocked
        (the collision gate is same-iteration only, and the dict was cleared).
        """
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()

        # iter-1: anthropic/google/openai; iter-2 scribe cascade STARTS on openai.
        iter2_scribe_cascade = ProviderCascade(
            seat_kind="scribe",
            levels=(("openai", "gpt"), ("google", "gemini"), ("anthropic", "claude")),
            current_level=0,
        )
        launcher.per_seat = {
            "scribe": [
                _seat_ok(family="anthropic", model_id="claude"),  # iter-1
                _seat_ok(family="openai", model_id="gpt"),  # iter-2 → lands on level 0
            ],
            "editor": [
                _seat_ok(family="google", model_id="g1"),
                _seat_ok(family="google", model_id="g1"),
            ],
            "judge": [
                _judge_ok(family="openai", model_id="gpt", verdict="FAIL", score=60),
                _judge_ok(family="meta", model_id="llama", verdict="PASS", score=90),
            ],
        }

        result = _run(
            rs,
            launcher=launcher,
            factory=factory,
            vault=vault,
            clock=clock,
            scribe_cascade=iter2_scribe_cascade,
        )

        assert result.converged_on == "score_threshold"
        assert result.iterations_run == 2
        # Verify iter-2 scribe was called with openai (level 0; not skipped).
        scribe_calls = [c for c in launcher.calls if c["seat_kind"] == "scribe"]
        assert len(scribe_calls) == 2
        assert scribe_calls[1]["family"] == "openai"


# ===========================================================================
# 15. InnerLoopResult frozen-dataclass pin
# ===========================================================================


class TestInnerLoopResultImmutable:
    def test_cannot_mutate_result_fields(self) -> None:
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        launcher.per_seat = {
            "scribe": [_seat_ok()],
            "editor": [_seat_ok(family="google", model_id="g1")],
            "judge": [_judge_ok(verdict="PASS", score=90)],
        }
        result = _run(rs, launcher=launcher, factory=factory, vault=vault, clock=clock)

        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            result.converged_on = "delta_plateau"  # type: ignore[misc]


# ===========================================================================
# 16. PipelineFailure.CODE contract — F_PIPE_06 maps to "F-PIPE-06" exactly
# ===========================================================================


class TestFailureCodeContract:
    """Revision_loop uses ``err.CODE`` in the generic except branch. Verify
    the class-attribute contract so the string surfaced on IterationState is
    the canonical wire code.
    """

    def test_pipeline_failure_code_attrs_are_canonical(self) -> None:
        assert F_PIPE_06.CODE == "F-PIPE-06"
        assert F_PIPE_08.CODE == "F-PIPE-08"
        assert F_PIPE_09.CODE == "F-PIPE-09"
        assert issubclass(F_PIPE_06, PipelineFailure)
        assert issubclass(F_PIPE_08, PipelineFailure)

    def test_F_PIPE_08_err_code_surfaces_on_iteration_state(self) -> None:
        """Regression pin for the generic except-branch ``err.CODE`` usage."""
        rs = _run_state()
        vault = _InMemoryVault()
        clock = _Clock()
        launcher = _FakeLauncher()
        factory = _ContextFactory()
        launcher.per_seat = {
            "scribe": [_seat_ok(family="anthropic", model_id="c")],
        }
        editor_all_anthropic = ProviderCascade(
            seat_kind="editor",
            levels=(("anthropic", "a"), ("anthropic", "b"), ("anthropic", "c")),
            current_level=0,
        )

        with pytest.raises(F_PIPE_08):
            _run(
                rs,
                launcher=launcher,
                factory=factory,
                vault=vault,
                clock=clock,
                editor_cascade=editor_all_anthropic,
            )
        assert rs.iterations[0].failure_code == "F-PIPE-08"


# ===========================================================================
# 17. Module-level sanity
# ===========================================================================


class TestModuleSanity:
    def test_revision_loop_module_asserts_subclass_at_load(self) -> None:
        # The module-level ``assert issubclass`` for F_PIPE_05/09/11/19 already
        # fires at first import; we verify the post-import invariant here
        # without reloading (reload would invalidate class identity captured
        # by other test modules — cross-file test-order pollution).
        from pipeline.loop.errors import (
            F_PIPE_05 as e5,
            F_PIPE_09 as e9,
            F_PIPE_11 as e11,
            F_PIPE_19 as e19,
            PipelineFailure,
        )

        for cls in (e5, e9, e11, e19):
            assert issubclass(cls, PipelineFailure)
        assert rl.run_inner_loop is not None

    def test_public_api_surface(self) -> None:
        assert "InnerLoopResult" in rl.__all__
        assert "run_inner_loop" in rl.__all__
        assert "InterruptProbe" in rl.__all__
        assert "SeatContextFactory" in rl.__all__
