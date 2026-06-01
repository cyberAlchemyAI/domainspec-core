"""pipeline.loop.revision_loop — §4.6 run_inner_loop orchestrator (Round 5).

Blueprint §5 v6 LOCKED 2026-04-19:

- §4.6 Revision-loop control v2 (A-v1-02 / A-v1-07 / A-v1-10 / A-v1-11 /
  A-v1-15 closures) — three-iteration Scribe → Editor → Judge pipeline
- §3.2.2 IterationState (append per iteration; never mutated post-append)
- §3.2.1 RunState (phase mutation + iterations list append + families dict)
- §6 F-PIPE-05 iteration_cap_exceeded / F-PIPE-09 judge_output_malformed /
  F-PIPE-11 operator_interrupt / F-PIPE-19 soft_restart_forbidden
- §9.8 iteration-cap tests
- §8 ``MAX_REVISION_ITERATIONS = 3`` (inline-literal loop bound)

Round 5 is the first round that COMPOSES Round 4's ``invoke_seat`` across
a multi-seat pipeline step. Every subprocess launch still goes through the
injected :class:`SubprocessLauncher` (E-017) — Round 5 adds its own
Protocols (``InterruptProbe``, ``SeatContextFactory``) and consumes Round
2's ``checkpoint_atomic`` + ``VaultWriteCallable`` + ``ClockProtocol`` +
``SleepCallable``.

**Design decisions (confirmed at Round 5 ORIENT — 2026-04-20)**

1. *Iteration cap is an inline-literal ``for iter_n in (1, 2, 3)`` loop.*
   V1 discipline — rebinding :data:`pipeline.loop.config.MAX_REVISION_ITERATIONS`
   cannot alter runtime behaviour. The config constant is a documentation
   pin, not a dispatch input.

2. *Convergence thresholds are inline literals.* Score-threshold PASS uses
   ``verdict_dict.get("verdict") == "PASS"`` (string literal). Delta-plateau
   requires ``iter_n >= 2`` AND both scores ``>= 75`` AND ``abs(delta) <= 2``.
   All four numbers are literal at the predicate site.

3. *``run_iteration_families_so_far`` is CLEARED at the start of each
   iteration.* Blueprint §4.6 pseudo-code does not show an explicit reset,
   but the dict's *semantic* ("so far this iteration") is within-iteration
   per A-v1-02's "record IMMEDIATELY…BEFORE calling the next seat" framing.
   Cross-iteration accumulation would forbid iter-2's Scribe from landing
   on iter-1's Scribe family — unreasonable for a revision loop whose
   Scribe charter is normally pinned to one family. Documented as
   spec-card Open-Q #2 resolution.

4. *Judge parse ordering moved entirely to Round 4 (A-v1-15).* Round 4's
   :func:`invoke_seat` with ``seat_kind="judge"`` parses stdout inline and
   returns :class:`SeatInvocationResult` with ``judge_verdict: dict``.
   Round 5 handles :class:`F_PIPE_09` raised from that parse by writing the
   ``state-failure`` checkpoint with ``IterationState.judge_verdict=None``
   and re-raising. The spec-card's ``JudgeParserCallable`` injection at
   Round 5 is thus MOOT — Round 5 forwards an optional ``judge_parse``
   through to Round 4 for adversarial override but never parses itself.

5. *Operator interrupt uses F_PIPE_11.* The blueprint does not explicitly
   name the code at the ``_check_interrupt_post_checkpoint`` call site;
   :class:`F_PIPE_11` (``operator_interrupt``) matches the A-v1-11 prose
   ("if the interrupt is observed, the current iteration's state is
   already checkpointed"). :class:`F_PIPE_20` is ``cedar_decision_missing``
   — a different concern. Open-Q #3 resolution.

6. *CAS pin threading is explicit.* The caller (Round 3 ``start_run`` /
   Round 6 post_gate_runner) supplies ``initial_checkpoint_hash``; Round 5
   threads the ``CheckpointResult.committed_hash`` through each checkpoint
   call. No implicit vault-read — the caller owns the post-write head.

7. *``IterationState.converged_on`` is NOT a field.* Round 1's
   ``IterationState`` is ``slots=True`` with a fixed field set that does
   not include ``converged_on``. Blueprint §4.6 pseudo-code's
   ``iteration_state.converged_on = "score_threshold"`` assignment would
   raise ``AttributeError`` on that dataclass — the blueprint pseudo-code
   implicitly assumes a richer shape. Round 5 returns a dedicated
   :class:`InnerLoopResult` wrapper that carries ``converged_on`` as a
   sibling field alongside the terminal ``IterationState``. Documented as
   spec-card deviation #1.

8. *Seat context is injected via :class:`SeatContextFactory`.* The
   ``stdin_payload`` Scribe receives depends on iter-n AND on prev-iter
   Editor critique hash + Judge score hash; constructing the literal
   payload bytes is out-of-scope for Round 5 (Round 6 or the capstone
   runner owns seat-prompt assembly). The factory Protocol accepts the
   per-iteration context (seat_kind, iter_n, prev hashes, run_state) and
   returns a :class:`SeatInvocationContext` for Round 4.

9. *A-v1-10 soft-restart guard checks EVERY existing iteration.* Blueprint
   §4.6 line 473 uses ``any(it.iter_number >= iter_n for it in
   run_state.iterations)``. Round 5 mirrors that check exactly. A
   pre-populated iteration with ``iter_number == iter_n`` triggers F_PIPE_19
   on entry to that iter_n.

10. *Per-iteration phase-transition + checkpoint + families-clear ordering
    is:* (a) soft-restart guard, (b) A-v1-07 phase-prefix invariant
    assert, (c) phase = f"inner_loop_iter_{iter_n}", (d)
    families_so_far.clear(), (e) checkpoint_atomic state-success,
    (f) seat dispatch. If the state-success checkpoint fails, we never
    attempt seat dispatch (checkpoint_atomic raises; propagates). If any
    seat raises :class:`PipelineFailure`, a state-failure checkpoint is
    written and the error re-raised.

**Threat model (§3.11 v5 trusted-operator envelope; E-023 closure)**

Round 5 is an internal primitive consumed only by Round 6+ and the
capstone ``run_pipeline.py``. The following residuals are OUT-OF-SCOPE
for v0.1 and documented by explicit ``test_adv_*`` tests rather than
defended at this layer:

- **Concurrent in-process ``run_inner_loop`` invocations on the same
  RunState.** The loop mutates ``run_state.phase``, ``run_state.iterations``,
  and ``run_state.run_iteration_families_so_far``. Two coroutines or
  threads racing here would corrupt the state. Production Tilth runs a
  single-threaded orchestrator per run; concurrency is out-of-scope.

- **``context_factory`` returning stale ``SeatInvocationContext`` across
  iterations.** Round 5 calls the factory afresh each seat invocation;
  a misbehaved factory that returns the same bytes regardless of iter_n
  would cause Scribe to see no revision history. Factory correctness is
  the caller's responsibility (Round 6 / capstone).

- **``subprocess_launcher`` honouring timeout_ms.** Round 4 already
  documents this — Round 5 inherits the residual without re-asserting.

- **Malicious ``judge_parse`` raising non-``F_PIPE_09`` exceptions.**
  Round 4 wraps any parser exception as ``F_PIPE_09``. Round 5's
  ``except F_PIPE_09`` branch is precise; a rogue parser that raises
  ``RuntimeError`` before Round 4 can wrap would propagate and be caught
  by the generic ``except PipelineFailure`` branch only if it is a
  PipelineFailure subclass. Non-PipelineFailure exceptions propagate
  unwrapped — by design (blueprint §4.13 state-failure semantics apply
  only to known failure codes).

Spec card: `pipeline/engineering/spec_cards/section_05_round_5_revision_loop.md`
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Protocol, runtime_checkable

from pipeline.loop.errors import (
    F_PIPE_05,
    F_PIPE_09,
    F_PIPE_11,
    F_PIPE_19,
    PipelineFailure,
)
from pipeline.loop.seat_runner import (
    JudgeParseCallable,
    SeatInvocationContext,
    SeatInvocationResult,
    SubprocessLauncher,
    invoke_editor,
    invoke_judge,
    invoke_red_team,
    invoke_scribe,
)
from pipeline.loop.state_checkpoint import (
    ClockProtocol,
    SleepCallable,
    VaultWriteCallable,
    checkpoint_atomic,
)
from pipeline.loop.types import (
    IterationState,
    ProviderCascade,
    RunState,
    SeatCharter,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.6 run_inner_loop (v2 A-v1-02/07/10/11/15 closures)",
            "§9.8 iteration-cap mechanics",
        ],
    },
}

# Module-load integrity — every F_PIPE_* class referenced below must resolve
# to a PipelineFailure subclass at import time. Rebinding the module
# attribute before first call cannot fool isinstance checks at raise sites,
# but the assertion here catches an import-order regression early.
assert all(
    issubclass(cls, PipelineFailure)
    for cls in (F_PIPE_05, F_PIPE_09, F_PIPE_11, F_PIPE_19)
), (
    "pipeline.loop.revision_loop: F_PIPE_05/09/11/19 did not resolve to "
    "PipelineFailure subclasses at module load; refusing to load"
)


# ---------------------------------------------------------------------------
# Public Protocols (E-017 injected-callable pattern)
# ---------------------------------------------------------------------------


@runtime_checkable
class InterruptProbe(Protocol):
    """A-v1-11 operator-interrupt poll.

    Returns ``True`` iff the operator has signalled interruption (Ctrl-C
    flag on disk, queue message, signal handler — all production details
    out-of-scope for Round 5). Called by :func:`run_inner_loop` AFTER the
    success-checkpoint of each iteration; if True, the current iteration
    is already durably recorded and Round 5 raises :class:`F_PIPE_11`.

    Injecting ``None`` for the ``interrupt_probe`` kwarg disables the
    poll entirely (equivalent to a probe that always returns False).
    Tests inject stubs that return True after a configured iteration to
    pin A-v1-11 post-checkpoint semantics.
    """

    def __call__(self) -> bool: ...


@runtime_checkable
class SeatContextFactory(Protocol):
    """Per-seat-per-iteration context builder.

    Round 5 calls the factory THREE times per iteration (scribe, editor,
    judge). The factory returns a :class:`SeatInvocationContext` that
    Round 4's :func:`invoke_seat` consumes for subprocess stdin + env.

    The factory receives the full per-iteration context: ``seat_kind``,
    ``iter_n``, the raw stdout hashes of the prior iteration's Editor
    and Judge (``prev_editor_hash`` / ``prev_judge_hash``; both ``None``
    on iter_1), and the live ``run_state``. The factory is free to read
    ``run_state.rfa_hash`` / ``project_context_hash`` / etc., but MUST
    NOT mutate the run_state — Round 5 owns the only mutation path.

    Production wires this to a Round 6+ seat-prompt assembler; tests
    inject deterministic stubs that return a fixed
    :class:`SeatInvocationContext` per seat.
    """

    def __call__(
        self,
        *,
        seat_kind: str,
        iter_n: int,
        prev_editor_hash: str | None,
        prev_judge_hash: str | None,
        run_state: RunState,
    ) -> SeatInvocationContext: ...


# ---------------------------------------------------------------------------
# Public result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class InnerLoopResult:
    """Return value of a successful :func:`run_inner_loop` invocation.

    Round 5 returns on either convergence path (score-threshold PASS or
    delta-plateau); iteration-cap exhaustion without convergence raises
    :class:`F_PIPE_05` (never returns an ``InnerLoopResult``).

    - ``final_iteration``: the :class:`IterationState` appended in the
      winning iteration. Its ``judge_verdict`` dict is the Round-4-parsed
      verdict; its ``failure_code`` is ``None`` on both convergence paths.
    - ``converged_on``: one of the string literals ``"score_threshold"``
      (``judge_verdict["verdict"] == "PASS"``) or ``"delta_plateau"`` (two
      consecutive scores ≥ 75 with absolute delta ≤ 2).
    - ``iterations_run``: 1, 2, or 3 — the number of fully-checkpointed
      iterations (inclusive of the winner).
    - ``final_checkpoint_hash``: the CAS head after the last successful
      state-success write. Callers thread this into Round 6's POST-gate
      checkpoint call.
    """

    final_iteration: IterationState
    converged_on: str
    iterations_run: int
    final_checkpoint_hash: str


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _delta_plateau(iterations: list[IterationState]) -> bool:
    """§4.6 / v1 unchanged — delta-plateau detector.

    Returns True iff the last two :class:`IterationState` entries both
    have a parsed ``judge_verdict`` with numeric ``total_score``, BOTH
    scores are ≥ 75, AND the absolute delta is ≤ 2.

    All four thresholds (``75``, ``2``, slice length ``2``, existence
    check for the dict key ``"total_score"``) are inline literals —
    rebinding a module-level constant cannot alter dispatch.

    Callers MUST gate on ``iter_n >= 2`` separately; this function
    returns False on ``len(iterations) < 2`` but does not short-circuit
    the outer iter_n check (V1 belt-and-braces).
    """

    if len(iterations) < 2:
        return False
    last = iterations[-1]
    prev = iterations[-2]
    last_verdict = last.judge_verdict
    prev_verdict = prev.judge_verdict
    if not isinstance(last_verdict, dict) or not isinstance(prev_verdict, dict):
        return False
    last_score = last_verdict.get("total_score")
    prev_score = prev_verdict.get("total_score")
    if not isinstance(last_score, (int, float)):
        return False
    if not isinstance(prev_score, (int, float)):
        return False
    if last_score < 75 or prev_score < 75:
        return False
    if abs(last_score - prev_score) > 2:
        return False
    return True


def _assert_soft_restart_not_forbidden(
    run_state: RunState, iter_n: int
) -> None:
    """A-v1-10 closure — F_PIPE_19 on re-entry into an already-appended iter.

    Mirrors blueprint §4.6 line 473 exactly: ``any(it.iter_number >= iter_n
    for it in run_state.iterations)``. A pre-populated iteration with
    ``iter_number == iter_n`` (soft-restart of the current iter) OR
    ``iter_number > iter_n`` (attempted regression to an earlier iter
    after a higher one appended) both trip the guard.
    """

    for it in run_state.iterations:
        if it.iter_number >= iter_n:
            raise F_PIPE_19(
                trigger="soft_restart_forbidden",
                details={
                    "run_id": run_state.run_id,
                    "attempted_iter_n": iter_n,
                    "existing_iter_number": it.iter_number,
                    "iterations_count": len(run_state.iterations),
                },
            )


def _assert_phase_is_inner_loop_iter(run_state: RunState, iter_n: int) -> None:
    """A-v1-07 closure — phase-prefix invariant at each iteration boundary.

    Belt-and-braces with §4 v2 F-PRE-19 and the §3.5 banned-import static
    check. The caller (Round 3 ``start_run`` / Round 6 pre-gate) is
    expected to set ``run_state.phase = "inner_loop_iter_1"`` before the
    first call; between iterations Round 5 itself updates the phase.

    On failure raises :class:`AssertionError` — this is a programmer-error
    assertion, not a runtime failure code.
    """

    if not run_state.phase.startswith("inner_loop_iter_"):
        raise AssertionError(
            f"run_inner_loop: phase invariant violated at iter_n={iter_n}; "
            f"expected phase.startswith('inner_loop_iter_'); "
            f"got {run_state.phase!r}"
        )


def _build_iteration_state_failure(
    *,
    iter_n: int,
    seat_draft_hashes: dict[str, str],
    failure_code: str,
    started_at_iso: str,
    completed_at_iso: str,
) -> IterationState:
    """A-v1-15 / §4.6 failure-branch IterationState constructor.

    Centralized so the Judge-parse branch (``failure_code="F-PIPE-09"``)
    and the generic PipelineFailure branch (``failure_code=err.code``)
    produce structurally-identical records. ``judge_verdict`` is ``None``
    on both branches — blueprint A-v1-15 contract.
    """

    return IterationState(
        iter_number=iter_n,
        seat_draft_hashes=dict(seat_draft_hashes),
        judge_verdict=None,
        failure_code=failure_code,
        started_at_iso=started_at_iso,
        completed_at_iso=completed_at_iso,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def run_inner_loop(
    *,
    run_state: RunState,
    scribe_charter: SeatCharter,
    editor_charter: SeatCharter,
    judge_charter: SeatCharter,
    scribe_cascade: ProviderCascade,
    editor_cascade: ProviderCascade,
    judge_cascade: ProviderCascade,
    context_factory: SeatContextFactory,
    subprocess_launcher: SubprocessLauncher,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
    initial_checkpoint_hash: str | None,
    interrupt_probe: InterruptProbe | None = None,
    judge_parse: JudgeParseCallable | None = None,
    # v7 NEW (§5 v7 amendment §4.5a) — all OPTIONAL for v6 backward compat.
    # When red_team_charter is None, Red Team is not invoked; the run is
    # the v6 4-seat council. When red_team_charter is provided, Red Team
    # fires after Judge each iteration; council-split detection runs.
    red_team_charter: SeatCharter | None = None,
    red_team_cascade: ProviderCascade | None = None,
    rt_disagreement_threshold: int = 10,
) -> InnerLoopResult:
    """§4.6 v2 — three-iteration Scribe → Editor → Judge revision loop.

    **Per-iteration body (iter_n ∈ (1, 2, 3))**:

    1. A-v1-10 soft-restart guard — any ``IterationState.iter_number >=
       iter_n`` already in ``run_state.iterations`` raises
       :class:`F_PIPE_19`.
    2. A-v1-07 phase-prefix invariant — ``run_state.phase`` must start
       with ``"inner_loop_iter_"``.
    3. Phase transition to ``f"inner_loop_iter_{iter_n}"``;
       ``run_iteration_families_so_far`` cleared; state-success
       checkpoint written.
    4. Scribe invocation → record ``landed_family`` IMMEDIATELY → Editor
       → record → Judge (with inline parse per A-v1-15).
    5. On :class:`F_PIPE_09` from Round 4's Judge parse: append
       ``IterationState`` with ``judge_verdict=None``,
       ``failure_code="F-PIPE-09"``; state-failure checkpoint; re-raise.
    6. On any other :class:`PipelineFailure`: append ``IterationState``
       with the caught code; state-failure checkpoint; re-raise.
    7. On full success: append ``IterationState`` with Scribe/Editor/Judge
       output hashes + parsed ``judge_verdict``; state-success
       checkpoint.
    8. A-v1-11 interrupt check — if ``interrupt_probe()`` returns True,
       raise :class:`F_PIPE_11` (iteration already durably checkpointed).
    9. Convergence: ``verdict == "PASS"`` → return
       ``converged_on="score_threshold"``. ``iter_n >= 2`` AND
       :func:`_delta_plateau` → return ``converged_on="delta_plateau"``.

    **Cap exhaustion**: all 3 iterations complete without convergence →
    one final state-failure checkpoint, then :class:`F_PIPE_05` raised.

    Parameters
    ----------
    run_state
        Live RunState. Mutated on every iteration (phase, iterations list,
        families dict, last_checkpoint_iso).
    scribe_charter / editor_charter / judge_charter
        Per-seat charters (Round 1 dataclass). Round 5 forwards them to
        :func:`invoke_scribe` / :func:`invoke_editor` / :func:`invoke_judge`
        without inspection.
    scribe_cascade / editor_cascade / judge_cascade
        Per-seat ProviderCascades. Round 5 passes them in at iter-1; any
        per-invocation level advances recorded in ``cascade_after`` are
        NOT persisted across iterations — each iteration starts at the
        operator-provided level. (Cross-iteration cascade persistence is
        deferred to Round 6 / capstone.)
    context_factory
        :class:`SeatContextFactory` — called 3× per iteration to build
        per-seat :class:`SeatInvocationContext`.
    subprocess_launcher
        :class:`SubprocessLauncher` forwarded to Round 4 for every seat.
    vault_write, clock, sleep
        Injected Protocols for the CAS checkpoint loop.
    initial_checkpoint_hash
        CAS head at entry — the committed hash of the last write by Round 3
        (``start_run``) or Round 6 (PRE-gate PASS). ``None`` only if the
        ``state.json`` file does not yet exist (first write-if-absent).
    interrupt_probe
        Optional A-v1-11 probe. ``None`` disables the poll.
    judge_parse
        Optional :class:`JudgeParseCallable` forwarded to Round 4's Judge
        invocation. ``None`` uses Round 4's
        :func:`default_judge_parse` (UTF-8 + JSON + non-empty-dict).

    Returns
    -------
    InnerLoopResult
        On convergence — the winning IterationState + metadata.

    Raises
    ------
    F_PIPE_05
        Iteration cap exceeded without convergence.
    F_PIPE_09
        Judge output malformed (re-raised from Round 4 after state-failure
        checkpoint and IterationState append with ``judge_verdict=None``).
    F_PIPE_11
        Operator interrupt observed after a successful iteration
        checkpoint.
    F_PIPE_19
        Soft-restart forbidden (A-v1-10).
    PipelineFailure
        Any other Round 4 / Round 2 failure propagates; a state-failure
        checkpoint + IterationState append land before the re-raise.
    """

    current_hash = initial_checkpoint_hash
    prev_editor_hash: str | None = None
    prev_judge_hash: str | None = None
    iterations_run = 0

    # Inline-literal iteration bound — rebinding
    # pipeline.loop.config.MAX_REVISION_ITERATIONS cannot extend this loop.
    for iter_n in (1, 2, 3):
        _assert_soft_restart_not_forbidden(run_state, iter_n)
        _assert_phase_is_inner_loop_iter(run_state, iter_n)

        run_state.phase = f"inner_loop_iter_{iter_n}"
        run_state.run_iteration_families_so_far.clear()

        started_iso = clock.now_iso()
        phase_ck = checkpoint_atomic(
            run_state,
            intent="state-success",
            expected_current_file_hash=current_hash,
            vault_write=vault_write,
            clock=clock,
            sleep=sleep,
        )
        current_hash = phase_ck.committed_hash

        scribe_result: SeatInvocationResult | None = None
        editor_result: SeatInvocationResult | None = None
        judge_result: SeatInvocationResult | None = None

        try:
            scribe_ctx = context_factory(
                seat_kind="scribe",
                iter_n=iter_n,
                prev_editor_hash=prev_editor_hash,
                prev_judge_hash=prev_judge_hash,
                run_state=run_state,
            )
            scribe_result = invoke_scribe(
                run_state=run_state,
                iteration_number=iter_n,
                charter=scribe_charter,
                cascade=scribe_cascade,
                context=scribe_ctx,
                subprocess_launcher=subprocess_launcher,
                judge_parse=judge_parse,
            )
            # A-v1-02: record IMMEDIATELY + BEFORE next seat.
            run_state.run_iteration_families_so_far["scribe"] = (
                scribe_result.landed_family,
                scribe_result.landed_model_id,
            )

            editor_ctx = context_factory(
                seat_kind="editor",
                iter_n=iter_n,
                prev_editor_hash=prev_editor_hash,
                prev_judge_hash=prev_judge_hash,
                run_state=run_state,
            )
            editor_result = invoke_editor(
                run_state=run_state,
                iteration_number=iter_n,
                charter=editor_charter,
                cascade=editor_cascade,
                context=editor_ctx,
                subprocess_launcher=subprocess_launcher,
                judge_parse=judge_parse,
            )
            run_state.run_iteration_families_so_far["editor"] = (
                editor_result.landed_family,
                editor_result.landed_model_id,
            )

            judge_ctx = context_factory(
                seat_kind="judge",
                iter_n=iter_n,
                prev_editor_hash=prev_editor_hash,
                prev_judge_hash=prev_judge_hash,
                run_state=run_state,
            )
            judge_result = invoke_judge(
                run_state=run_state,
                iteration_number=iter_n,
                charter=judge_charter,
                cascade=judge_cascade,
                context=judge_ctx,
                subprocess_launcher=subprocess_launcher,
                judge_parse=judge_parse,
            )
            run_state.run_iteration_families_so_far["judge"] = (
                judge_result.landed_family,
                judge_result.landed_model_id,
            )

            # v7 NEW (§5 v7 amendment §4.5a) — Red Team after Judge.
            # OPTIONAL: only fires when red_team_charter + red_team_cascade
            # are provided (operator opt-in for v6 backward compat).
            red_team_result: SeatInvocationResult | None = None
            if red_team_charter is not None and red_team_cascade is not None:
                red_team_ctx = context_factory(
                    seat_kind="red_team",
                    iter_n=iter_n,
                    prev_editor_hash=prev_editor_hash,
                    prev_judge_hash=prev_judge_hash,
                    run_state=run_state,
                )
                red_team_result = invoke_red_team(
                    run_state=run_state,
                    iteration_number=iter_n,
                    charter=red_team_charter,
                    cascade=red_team_cascade,
                    context=red_team_ctx,
                    subprocess_launcher=subprocess_launcher,
                    judge_parse=judge_parse,
                )
                # A-v1-02 mirror: record IMMEDIATELY before any subsequent seat.
                run_state.run_iteration_families_so_far["red_team"] = (
                    red_team_result.landed_family,
                    red_team_result.landed_model_id,
                )

        except F_PIPE_09:
            # A-v1-15: Judge parse failure — never recorded as success.
            seat_hashes: dict[str, str] = {}
            if scribe_result is not None:
                seat_hashes["scribe"] = scribe_result.output_hash
            if editor_result is not None:
                seat_hashes["editor"] = editor_result.output_hash
            iteration_state = _build_iteration_state_failure(
                iter_n=iter_n,
                seat_draft_hashes=seat_hashes,
                failure_code="F-PIPE-09",
                started_at_iso=started_iso,
                completed_at_iso=clock.now_iso(),
            )
            run_state.iterations.append(iteration_state)
            checkpoint_atomic(
                run_state,
                intent="state-failure",
                expected_current_file_hash=current_hash,
                vault_write=vault_write,
                clock=clock,
                sleep=sleep,
            )
            raise

        except PipelineFailure as err:
            # Generic PipelineFailure — record observed code, checkpoint,
            # re-raise. Covers F_PIPE_06/07/08 (seat-level failures raised
            # by Round 4) and any future seat-level subclasses.
            seat_hashes_g: dict[str, str] = {}
            if scribe_result is not None:
                seat_hashes_g["scribe"] = scribe_result.output_hash
            if editor_result is not None:
                seat_hashes_g["editor"] = editor_result.output_hash
            iteration_state_g = _build_iteration_state_failure(
                iter_n=iter_n,
                seat_draft_hashes=seat_hashes_g,
                failure_code=err.CODE,
                started_at_iso=started_iso,
                completed_at_iso=clock.now_iso(),
            )
            run_state.iterations.append(iteration_state_g)
            checkpoint_atomic(
                run_state,
                intent="state-failure",
                expected_current_file_hash=current_hash,
                vault_write=vault_write,
                clock=clock,
                sleep=sleep,
            )
            raise

        # All three seats succeeded + Judge parsed. (Red Team is optional
        # per §5 v7 §4.5a; runs after Judge when configured.) Append
        # success state.
        assert judge_result is not None  # narrow for type-checkers
        assert scribe_result is not None
        assert editor_result is not None

        # v7 council-split early-exit detection (§5 v7 §4.6 amendment +
        # §10.6). Fires only when both Judge and Red Team produced verdicts
        # AND |judge_total - red_team_total| >= rt_disagreement_threshold.
        council_split_detected = False
        if (
            red_team_result is not None
            and red_team_result.judge_verdict is not None
            and judge_result.judge_verdict is not None
        ):
            jv_total = judge_result.judge_verdict.get("total_score")
            rt_total = red_team_result.judge_verdict.get("total_score")
            if isinstance(jv_total, int) and isinstance(rt_total, int):
                if abs(jv_total - rt_total) >= rt_disagreement_threshold:
                    council_split_detected = True

        seat_hashes_success: dict[str, str] = {
            "scribe": scribe_result.output_hash,
            "editor": editor_result.output_hash,
            "judge": judge_result.output_hash,
        }
        if red_team_result is not None:
            seat_hashes_success["red_team"] = red_team_result.output_hash

        success_iter = IterationState(
            iter_number=iter_n,
            seat_draft_hashes=seat_hashes_success,
            judge_verdict=judge_result.judge_verdict,
            red_team_verdict=(
                red_team_result.judge_verdict if red_team_result is not None else None
            ),
            failure_code=None,
            started_at_iso=started_iso,
            completed_at_iso=clock.now_iso(),
            exit_reason="council_split" if council_split_detected else "",
        )
        run_state.iterations.append(success_iter)
        success_ck = checkpoint_atomic(
            run_state,
            intent="state-success",
            expected_current_file_hash=current_hash,
            vault_write=vault_write,
            clock=clock,
            sleep=sleep,
        )
        current_hash = success_ck.committed_hash
        iterations_run += 1

        # A-v1-11: interrupt check AFTER the success checkpoint has landed.
        if interrupt_probe is not None and interrupt_probe():
            raise F_PIPE_11(
                trigger="operator_interrupt_post_checkpoint",
                details={
                    "run_id": run_state.run_id,
                    "iter_number": iter_n,
                    "iterations_run": iterations_run,
                },
            )

        # v7 council-split early-exit (§5 v7 §4.6). When detected, exit the
        # loop immediately with a council_split converged_on tag; further
        # revisions cannot resolve seat-disagreement (only the operator can).
        if council_split_detected:
            return InnerLoopResult(
                final_iteration=success_iter,
                converged_on="council_split",
                iterations_run=iterations_run,
                final_checkpoint_hash=current_hash,
            )

        # Convergence checks — inline-literal string + numeric thresholds.
        verdict_dict = success_iter.judge_verdict
        if isinstance(verdict_dict, dict) and verdict_dict.get("verdict") == "PASS":
            return InnerLoopResult(
                final_iteration=success_iter,
                converged_on="score_threshold",
                iterations_run=iterations_run,
                final_checkpoint_hash=current_hash,
            )
        if iter_n >= 2 and _delta_plateau(run_state.iterations):
            return InnerLoopResult(
                final_iteration=success_iter,
                converged_on="delta_plateau",
                iterations_run=iterations_run,
                final_checkpoint_hash=current_hash,
            )

        prev_editor_hash = editor_result.output_hash
        prev_judge_hash = judge_result.output_hash

    # All 3 iterations exhausted without convergence — F_PIPE_05.
    # Write one final state-failure checkpoint BEFORE raising so the
    # operator sees iteration_cap_exceeded persisted.
    checkpoint_atomic(
        run_state,
        intent="state-failure",
        expected_current_file_hash=current_hash,
        vault_write=vault_write,
        clock=clock,
        sleep=sleep,
    )
    raise F_PIPE_05(
        trigger="iteration_cap_exceeded",
        details={
            "run_id": run_state.run_id,
            "iterations_completed": iterations_run,
            "iterations_allowed": 3,
        },
    )


__all__ = [
    "BLUEPRINT_DEPS",
    "InnerLoopResult",
    "InterruptProbe",
    "SeatContextFactory",
    "run_inner_loop",
    "_delta_plateau",
    "_assert_soft_restart_not_forbidden",
    "_assert_phase_is_inner_loop_iter",
    "_build_iteration_state_failure",
]
