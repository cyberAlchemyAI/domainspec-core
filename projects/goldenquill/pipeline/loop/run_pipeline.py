"""pipeline.loop.run_pipeline — §4.1 submission-mode capstone (Round 11).

Blueprint §5 v6 LOCKED 2026-04-19:
- §4.1 full 11-step submission-mode pipeline entry
- §4.3/§4.6/§4.2/§4.11 composition of Rounds 1-10
- §6 F-PIPE-01/03/05/06/08/09/11/13/15/16/19/21/22 propagation (no new codes)

Round 11 is the FIRST §5 round that composes all previous rounds end-to-end.
It is orchestration-only: zero new primitives, zero new F-PIPE codes, zero
new Protocols (beyond :class:`PreGateInputFactory` + :class:`RunPipelineContext`
which are both composition-pattern conveniences, not new semantics).

**The 11-step submission-mode sequence** (blueprint §4.1):

 1. ``start_run`` (Round 3) — mints ``run_id``-keyed :class:`RunState` with
    ``phase="initialized"`` and writes checkpoint 0.
 2. Phase transition to ``"pre_gate_pending"`` + CAS checkpoint (§4.1 step 2).
 3. PRE-gate evaluation (Round 4 / §4.2) via injected callable returning a
    :class:`PreGateResult`. On PASS: phase → ``"pre_gate_passed"`` + checkpoint.
    On FAIL (soft): state-failure checkpoint + return early with
    ``pre_gate_failed=True`` on the :class:`PipelineRunResult`. On raise
    (F_PIPE_21 / F_PIPE_22 / other PipelineFailure): state-failure wrapper
    via Round 2 helper + re-raise.
 4. Phase transition to ``"inner_loop_iter_1"`` + CAS checkpoint (primes
    Round 5's invariant).
 5. ``run_inner_loop`` (Round 5) — three-iteration Scribe → Editor → Judge
    convergence loop. Raises F_PIPE_05 on cap exhaust; F_PIPE_06/08/09 on
    per-seat failures; F_PIPE_11 on operator interrupt; F_PIPE_19 on soft-
    restart. Returns :class:`InnerLoopResult` on convergence.
 6. ``run_post_gate_orchestration`` (Round 6) — transitions
    ``inner_loop_iter_N`` → ``post_gate_pending`` → ``post_gate_passed``.
    Raises :class:`PostGateRejected` on FAIL verdict; F_PIPE_03 on timeout;
    :class:`LogicianMidLoopCall` on state-machine mis-sequence.
 7. On PostGateRejected: catch, write bypass-pending marker payload,
    return :class:`PipelineRunResult` with ``bypass_pending=True``
    (operator signs off manually via out-of-band).
 8. Phase transition to ``"signoff_pending"`` + CAS checkpoint.
 9. Sign-off stub — v0.1 interim. Phase transition to ``"report_signed"``
    + CAS checkpoint. No Ed25519 signature yet (v0.2 will wire it in;
    :attr:`RunState.three_tab_envelope_hash` is set after step 10's
    envelope lands).
10. ``deliver_tab`` (Round 9) — assembles + commits the three-tab envelope;
    returns :class:`TabSigningResult` with envelope_sha256. Round 11 pins
    ``run_state.three_tab_envelope_hash = envelope_sha256``.
11. Phase transition to ``"tabs_delivered"`` + final CAS checkpoint.

**ORIENT-resolved design decisions (2026-04-21)**

1. *Context dataclass consolidates Protocol injection.* Ten Protocols through
   a flat signature would be unwieldy; :class:`RunPipelineContext` bundles
   vault_read / vault_write / clock / sleep / subprocess_launcher /
   pre_gate_callable / post_gate_runner / post_gate_input_factory /
   seat_context_factory / hash_file / run_id_factory plus two optionals
   (interrupt_probe / judge_parse). OQ-1 resolution.

2. *Sign-off is a stub in v0.1.* Step 9 performs the phase transitions
   (``signoff_pending`` → ``report_signed``) + checkpoints but does not
   compute an Ed25519 signature. The three-tab envelope's ``envelope_sha256``
   (from Round 9) is the only hash Round 11 records. OQ-2 resolution —
   flagged in docstring + lock_history as v0.1 interim.

3. *No reserve/release pairing at capstone.* Round 7's rate_limiter is
   wired inside the production ``SubprocessLauncher`` adapter (the launcher
   wraps each seat subprocess with reserve → exec → release). Round 11
   does not call ``reserve`` / ``release`` / ``can_reserve`` directly —
   composition stays at the subprocess-launch boundary. OQ-3 resolution.

4. *No cron-wrapping logic.* ``run_pipeline`` is normally invoked directly;
   cron-driven entries wrap with ``fire_once(on_fire=lambda: run_pipeline(...))``
   at the caller. ``flock_acquire`` is NOT in the signature. OQ-4 resolution.

5. *``run_id`` is a required kwarg.* Caller (cron wrapper or entrypoint)
   generates via ``RunIdFactory`` and passes down — this is the idempotency
   key for the entire pipeline run. Round 3's ``start_run`` accepts the
   factory via the context and uses it to mint if Round 11 re-delegates;
   Round 11 instead threads the pre-minted ``run_id`` through a thin
   ``_fixed_run_id_factory`` to keep the Round 3 surface untouched.
   OQ-5 resolution.

6. *Inline-literal mode gate at entry.* Round 11 asserts
   ``mode == "submission"`` via inline literal. An eval-mode run entering
   here raises :class:`F_PIPE_21` with trigger
   ``"eval_mode_invalid_intent"`` — §4.15 export-bundle shield lands at
   R9 deliver_tab also, but Round 11 shortcuts before any vault I/O.

7. *Phase-ordering tuple is inline-literal rebind-resistant.* The 11-step
   phase walk (``"initialized"`` → ``"tabs_delivered"``) is declared as
   an inline-literal tuple at module load for integrity assertion and at
   each comparison site. Rebinding :data:`pipeline.loop.types.RunPhase`
   does not affect runtime dispatch.

8. *``PipelineRunResult`` is frozen + slotted.* Same discipline as every
   other §5 result dataclass. Success path returns with
   ``final_phase="tabs_delivered"``; bypass path with
   ``final_phase="post_gate_pending"`` + ``bypass_pending=True``; PRE-gate
   soft-fail with ``final_phase="pre_gate_pending"`` + ``pre_gate_failed=True``.

**Threat model (§3.11 v5 trusted-operator envelope; E-023 residual surface)**

Round 11 is a capstone orchestrator — no network, no subprocess (delegated
to ``SubprocessLauncher``), no §4 Logician internals (reached only via the
public surface through the two factory Protocols). Residuals:

- **Factory misbehaviour** (``PreGateInputFactory`` / ``PostGateInputFactory``
  / ``SeatContextFactory``) — programmer error; Round 11 does NOT
  defensively catch. Exceptions propagate to the caller after state-failure
  wrapper. Matches Round 6's factory contract.

- **Concurrent in-process ``run_pipeline`` invocations on the same run_id** —
  out-of-scope for v0.1 single-threaded Tilth orchestrator. Two concurrent
  callers would trample on CAS head; the §2 vault's write-if-absent +
  CAS-exhausted F_PIPE_01 is the eventual guardrail.

- **``pre_gate_callable`` raising non-PipelineFailure** — e.g., a rogue
  implementation raising ``RuntimeError`` before reaching its own failure
  taxonomy. Round 11 writes a state-failure wrapper and re-raises
  unchanged (trusted-operator contract; non-PipelineFailure exceptions do
  NOT get translated to F-PIPE codes here).

- **Sign-off interrupted mid-transition** — the resume path (Round 3
  ``resume_run``) includes ``signoff_pending`` in the allowed set, so a
  restart picks up at step 9. Round 11 does NOT poll interrupt_probe
  between step 8 (signoff_pending transition) and step 11 (tabs_delivered) —
  the revision-loop is the canonical interrupt-observation point per
  blueprint A-v1-11.

Spec card:
``pipeline/engineering/spec_cards/section_05_round_11_run_pipeline_capstone.md``
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable, Final, Protocol, runtime_checkable

from pipeline.logician import (
    PreGateInput,
    PreGateResult,
)
from pipeline.loop.config import MAX_REVISION_ITERATIONS, RUNSTATE_SCHEMA_VERSION
from pipeline.loop.errors import PipelineFailure
from pipeline.loop.post_gate_runner import (
    GateRunnerProtocol,
    PostGateInputFactory,
    PostGateOrchestrationResult,
    PostGateRejected,
    run_post_gate_orchestration,
)
from pipeline.loop.revision_loop import (
    InnerLoopResult,
    InterruptProbe,
    SeatContextFactory,
    run_inner_loop,
)
from pipeline.loop.run_lifecycle import (
    RunIdFactory,
    VaultReadCallable,
    start_run,
)
from pipeline.loop.seat_runner import (
    JudgeParseCallable,
    SubprocessLauncher,
)
from pipeline.loop.state_checkpoint import (
    ClockProtocol,
    SleepCallable,
    VaultWriteCallable,
    _write_state_failure_wrapper,
    checkpoint_atomic,
)
from pipeline.loop.tab_delivery import (
    HashFileCallable,
    TabSigningResult,
    deliver_tab,
)
from pipeline.loop.types import (
    ProviderCascade,
    RunState,
    SeatCharter,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.1 full 11-step submission-mode pipeline entry",
            "§4.2 PRE-gate dispatch via injected callable",
            "§4.6 run_inner_loop composition (Round 5)",
            "§4.2 run_post_gate_orchestration composition (Round 6)",
            "§4.11 deliver_tab composition (Round 9)",
            "§4.15 eval-mode entry-gate shield via F_PIPE_21",
        ],
    },
}

# ---------------------------------------------------------------------------
# Inline-literal module-load integrity asserts (V1 discipline)
# ---------------------------------------------------------------------------

# MAX_REVISION_ITERATIONS must be 3 — any rebind before import is an
# integrity violation (Round 5 also asserts this but this module asserts
# independently to close any load-order window).
assert MAX_REVISION_ITERATIONS == 3, (
    "pipeline.loop.config.MAX_REVISION_ITERATIONS has been rebound before "
    "pipeline.loop.run_pipeline import; refusing to load"
)
assert RUNSTATE_SCHEMA_VERSION == 2, (
    "pipeline.loop.config.RUNSTATE_SCHEMA_VERSION has been rebound before "
    "pipeline.loop.run_pipeline import; refusing to load"
)


# ---------------------------------------------------------------------------
# Public Protocols (E-017 injected-callable pattern)
# ---------------------------------------------------------------------------


@runtime_checkable
class PreGateInputFactory(Protocol):
    """Caller-owned factory producing :class:`pipeline.logician.PreGateInput`.

    Round 11 does not assemble PRE-gate inputs; that requires §2 Vault
    reads (caller-outcomes for checks 1/2/3/5/6/7/8/9/11/12/13/16/18 per
    §4.2.1) + §4 Logician admin-risk ledger scan + §1 Section-2-lock read.
    The factory is caller-constructed; Round 11 invokes exactly once per
    orchestration call.

    Factory exceptions propagate unwrapped (trusted-operator contract;
    matches :class:`PostGateInputFactory` semantics).
    """

    def __call__(self, *, run_state: RunState) -> PreGateInput: ...


# ---------------------------------------------------------------------------
# Public context dataclass — bundled Protocol injection
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class RunPipelineContext:
    """Bundle of injected Protocols + callables consumed by :func:`run_pipeline`.

    Grouping these in one dataclass prevents the public entry-point
    signature from growing past readability (OQ-1 resolution). Every field
    is either an E-017 Protocol from an earlier round or a plain
    :class:`Callable` (``pre_gate_callable``).

    Unchanged across iterations: the same context drives PRE-gate, inner
    loop, POST-gate, deliver_tab. Callers that need per-step isolation
    (e.g. injecting a stub PRE-gate but a real inner-loop) construct
    multiple contexts or use fakes that dispatch internally.
    """

    # Round 2 / Round 3 primitives
    vault_read: VaultReadCallable
    vault_write: VaultWriteCallable
    clock: ClockProtocol
    sleep: SleepCallable
    run_id_factory: RunIdFactory

    # Round 4 / Round 5 primitives
    subprocess_launcher: SubprocessLauncher
    seat_context_factory: SeatContextFactory

    # §4 Logician PRE-gate (pipeline.logician.run_pre_gate) —
    # passed as a plain Callable, not a Protocol, to match the
    # function-not-instance call site. Production wires
    # ``pipeline.logician.run_pre_gate``.
    pre_gate_callable: Callable[[PreGateInput], PreGateResult]

    # Round 6 POST-gate primitives
    post_gate_runner: GateRunnerProtocol
    post_gate_input_factory: PostGateInputFactory

    # Round 9 tab-delivery primitive
    hash_file: HashFileCallable

    # Round 5 optional primitives
    interrupt_probe: InterruptProbe | None = None
    judge_parse: JudgeParseCallable | None = None


# ---------------------------------------------------------------------------
# Public result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class PipelineRunResult:
    """Terminal state of a :func:`run_pipeline` invocation.

    Three observable terminal shapes:

    1. *Success* — ``final_phase == "tabs_delivered"``;
       ``three_tab_envelope_hash`` is the envelope_sha256 from Round 9;
       ``bypass_pending`` and ``pre_gate_failed`` both False;
       ``iterations_consumed`` is 1..3.

    2. *PRE-gate soft-fail* — ``final_phase == "pre_gate_pending"``;
       ``pre_gate_failed=True``; ``pre_gate_failure_code`` pins the
       §4.2 F-PRE-* sub-code; ``three_tab_envelope_hash=None``;
       ``iterations_consumed=0``.

    3. *POST-gate bypass-pending* — ``final_phase == "post_gate_pending"``;
       ``bypass_pending=True``; ``post_gate_rejected_trigger`` pins the
       §4 Logician failure-code label from the GateRunner result;
       ``three_tab_envelope_hash=None``.

    Any raise path (F_PIPE_01..22, PipelineFailure subclasses) never
    constructs a :class:`PipelineRunResult` — the exception propagates
    with a state-failure checkpoint already written.
    """

    run_id: str
    final_phase: str
    iterations_consumed: int
    three_tab_envelope_hash: str | None
    elapsed_ms: int
    bypass_pending: bool = False
    pre_gate_failed: bool = False
    pre_gate_failure_code: str | None = None
    post_gate_rejected_trigger: str | None = None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _make_capturing_vault_write(
    inner: VaultWriteCallable, sink: dict[str, str | None]
) -> VaultWriteCallable:
    """Wrap ``vault_write`` to capture the first committed_hash in ``sink``.

    Round 3's :func:`start_run` discards its own committed CAS hash. To
    thread a concrete CAS head into step 2 without touching the Round 3
    public surface, Round 11 wraps the injected ``vault_write`` with a
    one-shot capturer — the first write (the state.json mint from
    ``start_run``) is the only call; its committed_hash becomes our
    step-2 ``expected_current_file_hash``.

    The wrapper is passed ONLY to ``start_run``; subsequent steps use
    the unwrapped callable directly.
    """

    def _wrapper(
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        committed = inner(
            path=path,
            payload=payload,
            intent=intent,
            write_mode=write_mode,
            expected_current_file_hash=expected_current_file_hash,
        )
        if sink.get("first_commit_hash") is None:
            sink["first_commit_hash"] = committed
        return committed

    return _wrapper


def _fixed_run_id_factory(run_id: str) -> RunIdFactory:
    """Wrap a pre-minted run_id as a :class:`RunIdFactory`.

    The caller (cron wrapper / entrypoint) already generated the
    idempotency-key ``run_id``; Round 3's :func:`start_run` requires a
    factory. Rather than mutating the Round 3 signature, Round 11 wraps
    the concrete string in a fixed-factory closure. The factory returns
    the same ``run_id`` on every call, which matches the Round 3 contract
    (``start_run`` invokes it exactly once).
    """

    def _factory() -> str:
        return run_id

    return _factory


def _transition_phase_and_checkpoint(
    *,
    run_state: RunState,
    new_phase: str,
    expected_current_file_hash: str | None,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
) -> str:
    """Mutate ``run_state.phase`` + write a state-success checkpoint.

    Returns the committed CAS hash for the caller to thread into the next
    step. On CAS exhaustion, Round 2's :func:`checkpoint_atomic` raises
    :class:`F_PIPE_01` with a quarantine-marker already written — Round 11
    does NOT wrap; the caller's outer ``try/except`` path handles the
    state-failure-wrapper invocation.
    """

    run_state.phase = new_phase
    ck = checkpoint_atomic(
        run_state,
        intent="state-success",
        expected_current_file_hash=expected_current_file_hash,
        vault_write=vault_write,
        clock=clock,
        sleep=sleep,
    )
    return ck.committed_hash


def _write_bypass_pending_marker(
    *,
    run_state: RunState,
    gate_result: Any,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
) -> str:
    """Write a ``bypass-pending`` sidecar for POST-gate reject paths.

    Mirrors the Round 2 quarantine-marker pattern: a sidecar JSON blob at
    ``pipeline/{run_id}/bypass_pending.json`` carrying the POST-gate
    failure taxonomy + timestamp. The operator's out-of-band sign-off
    workflow reads this file.

    Does NOT mutate ``state.json`` (Round 6 already wrote a state-failure
    checkpoint before raising :class:`PostGateRejected`). The bypass
    marker is supplementary; vault_write failure is best-effort-swallowed
    — the PostGateRejected exception still propagates from the caller.

    Returns the vault path where the marker was (attempted to be) written.
    """

    path = f"pipeline/{run_state.run_id}/bypass_pending.json"
    marker = {
        "run_id": run_state.run_id,
        "org_slug": run_state.org_slug,
        "phase_at_bypass": run_state.phase,
        "post_gate_result_hash": run_state.post_gate_result_hash,
        "failure_code": getattr(gate_result, "failure_code", None),
        "failed_step_number": getattr(gate_result, "failed_step_number", None),
        "written_at_iso": clock.now_iso(),
    }
    payload = json.dumps(marker, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    try:
        vault_write(
            path=path,
            payload=payload,
            intent="bypass-pending",
            write_mode="overwrite",
            expected_current_file_hash=None,
        )
    except Exception:
        # Best-effort — do not mask the PostGateRejected re-raise.
        pass
    return path


# ---------------------------------------------------------------------------
# Public API — run_pipeline
# ---------------------------------------------------------------------------


def run_pipeline(
    *,
    run_id: str,
    org_slug: str,
    session_id: str,
    rfa_hash: str,
    project_context_hash: str,
    scribe_charter: SeatCharter,
    editor_charter: SeatCharter,
    judge_charter: SeatCharter,
    scribe_cascade: ProviderCascade,
    editor_cascade: ProviderCascade,
    judge_cascade: ProviderCascade,
    context: RunPipelineContext,
    pre_gate_input_factory: PreGateInputFactory,
    # v7 (§5 v7 amendment §4.5a) — Red Team is the DEFAULT 5-seat council.
    # Operator may explicitly pass red_team_charter=None + red_team_cascade=None
    # to fall back to the v6 4-seat council (e.g., M13 review-seat outage
    # bypass; degraded-mode operation; 4-seat MVP demo paths). The default
    # arguments are None ONLY to preserve test-fixture stability; production
    # callers MUST pass real charters per router.yaml. The wrapper
    # ``run_pipeline_5_seat`` (below) is the canonical operator-facing
    # entrypoint with required Red Team config.
    red_team_charter: SeatCharter | None = None,
    red_team_cascade: ProviderCascade | None = None,
    rt_disagreement_threshold: int = 10,
) -> PipelineRunResult:
    """§4.1 full submission-mode pipeline entry — Rounds 1-10 composed.

    Returns a :class:`PipelineRunResult` on four terminal shapes:
    (1) success, (2) PRE-gate soft-fail, (3) POST-gate bypass-pending,
    (4) council-split pending (v7: ``final_phase="signoff_pending_council_split"``
    when Judge ↔ Red Team disagreement ≥ threshold and the operator has
    not yet recorded ``council_split_decision``). All F-PIPE-* exceptions
    propagate unwrapped after a state-failure wrapper has landed.

    **Step-by-step composition:**

    1. :func:`pipeline.loop.start_run` (Round 3) mints + checkpoints the
       :class:`RunState`. Raises F_PIPE_21/22 on construction violations.
    2. Phase → ``"pre_gate_pending"`` + state-success checkpoint.
    3. Build :class:`PreGateInput` via injected factory; invoke
       :attr:`RunPipelineContext.pre_gate_callable`. On PASS: phase →
       ``"pre_gate_passed"`` + checkpoint + advance. On soft-FAIL:
       state-failure checkpoint + early return with ``pre_gate_failed=True``.
       On raise: state-failure wrapper + re-raise.
    4. Phase → ``"inner_loop_iter_1"`` + state-success checkpoint (primes
       Round 5's phase-prefix invariant).
    5. :func:`pipeline.loop.run_inner_loop` (Round 5). Propagates
       F_PIPE_05/06/08/09/11/19 after state-failure wrapper.
    6. :func:`pipeline.loop.run_post_gate_orchestration` (Round 6). On
       PASS: :class:`PostGateOrchestrationResult`. On
       :class:`PostGateRejected`: catch, write bypass-pending marker,
       return with ``bypass_pending=True``.
    7. (Bypass branch terminal.)
    8. Phase → ``"signoff_pending"`` + checkpoint.
    9. Sign-off stub: phase → ``"report_signed"`` + checkpoint. v0.1
       interim — no Ed25519; the envelope_sha256 is the only attestation.
    10. :func:`pipeline.loop.deliver_tab` (Round 9). Raises F_PIPE_01/16/21
        on failures. On success: ``run_state.three_tab_envelope_hash =
        envelope_sha256``.
    11. Phase → ``"tabs_delivered"`` + final state-success checkpoint.
        Return :class:`PipelineRunResult` with ``final_phase="tabs_delivered"``.

    Parameters
    ----------
    run_id
        Caller-minted idempotency key. Threaded through a fixed-factory
        closure to Round 3's ``start_run`` (OQ-5 resolution).
    org_slug, session_id, rfa_hash, project_context_hash
        :class:`RunState` construction inputs (Round 3 contract).
    scribe_charter / editor_charter / judge_charter
        Per-seat Round 1 charters.
    scribe_cascade / editor_cascade / judge_cascade
        Per-seat Round 1 cascades. Forwarded to Round 5's
        ``run_inner_loop`` unchanged.
    context
        :class:`RunPipelineContext` bundling all injected Protocols +
        callables (OQ-1 resolution).
    pre_gate_input_factory
        :class:`PreGateInputFactory` — the one non-Protocol caller-owned
        factory not in the context (parallels R6's post_gate_input_factory
        position).

    Raises
    ------
    F_PIPE_21
        Entry mode is not ``"submission"`` (trigger
        ``"eval_mode_invalid_intent"``), or any §4.1 mode-isolation
        violation surfaced by ``start_run`` / downstream rounds.
    F_PIPE_22
        RunState schema-version downgrade.
    F_PIPE_01
        Checkpoint CAS exhausted (Round 2 quarantine path).
    F_PIPE_03
        POST-gate wall-clock timeout.
    F_PIPE_05
        Inner-loop iteration cap exceeded without convergence.
    F_PIPE_06 / F_PIPE_08 / F_PIPE_09
        Per-seat cascade / cross-family / Judge-parse failures (Round 4).
    F_PIPE_11
        Operator interrupt observed post-checkpoint (Round 5 A-v1-11).
    F_PIPE_16
        Tab-envelope ordering violation (Round 9).
    F_PIPE_19
        Soft-restart forbidden (Round 5 A-v1-10).
    PostGateRejected
        Raised by Round 6 but CAUGHT internally — translated to
        ``bypass_pending=True`` on the returned :class:`PipelineRunResult`.
    PipelineFailure
        Any other subclass propagates unchanged.
    """

    start_wall_ms = context.clock.now_ms()

    # ----- Step 1 — start_run (Round 3) ------------------------------------
    # Round 3 raises F_PIPE_21/22 on RunState construction violations; no
    # wrapper needed (no state yet). mode is pinned as the inline literal
    # "submission" — Round 11 is submission-mode-only.
    #
    # We wrap vault_write with a one-shot capturer because Round 3 does
    # not return the committed CAS head of its own state.json write and
    # the returned RunState has a mutation (``last_checkpoint_iso``)
    # applied AFTER the canonical payload was hashed, so we cannot
    # rederive the on-disk hash locally. Capturing the wrapper's first
    # ``committed_hash`` is authoritative.
    _capture_sink: dict[str, str | None] = {"first_commit_hash": None}
    run_state = start_run(
        mode="submission",
        org_slug=org_slug,
        session_id=session_id,
        rfa_hash=rfa_hash,
        project_context_hash=project_context_hash,
        golden_set_ref=None,
        run_id_factory=_fixed_run_id_factory(run_id),
        vault_write=_make_capturing_vault_write(context.vault_write, _capture_sink),
        clock=context.clock,
        sleep=context.sleep,
    )

    # Sanity — the factory should have returned the caller-minted id.
    # Defence-in-depth for a future Round-3 contract drift.
    if run_state.run_id != run_id:  # pragma: no cover — factory closure contract
        raise AssertionError(
            f"start_run returned run_id={run_state.run_id!r}; expected {run_id!r}"
        )

    # Capture Round 3's committed CAS head for subsequent checkpoint pins.
    # Round 3 does not return the hash; we re-canonicalize and derive it.
    # Simpler: threading through explicit pins would require touching
    # Round 3's API. Instead, our pattern uses None/CAS consistently —
    # after start_run, the file exists with a deterministic hash of the
    # canonicalized RunState at that moment. We capture via a helper
    # below by performing our OWN next-step checkpoint with the known
    # state and use its committed_hash as the thread.

    # ----- Step 2 — phase → pre_gate_pending + checkpoint ------------------
    # The first committed_hash captured from start_run's vault_write call
    # is the authoritative CAS head. If the capture sink is empty, Round 3
    # did not write (shouldn't happen — defence-in-depth: defer to None
    # so the overwrite surfaces as a clean CAS mismatch).
    initial_hash = _capture_sink["first_commit_hash"]
    try:
        current_hash: str = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase="pre_gate_pending",
            expected_current_file_hash=initial_hash,
            vault_write=context.vault_write,
            clock=context.clock,
            sleep=context.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state,
            exc,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        raise

    # ----- Step 3 — PRE-gate evaluation ------------------------------------
    try:
        pre_gate_input = pre_gate_input_factory(run_state=run_state)
        pre_gate_result = context.pre_gate_callable(pre_gate_input)
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state,
            exc,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        raise

    if not pre_gate_result.passed:
        # Soft-fail branch — write state-failure checkpoint (keep phase
        # at pre_gate_pending so resume knows where we stopped) and
        # return early.
        try:
            current_hash = checkpoint_atomic(
                run_state,
                intent="state-failure",
                expected_current_file_hash=current_hash,
                vault_write=context.vault_write,
                clock=context.clock,
                sleep=context.sleep,
            ).committed_hash
        except Exception as exc:
            # Best-effort — if the state-failure checkpoint can't land,
            # emit a sidecar state_failure.json wrapper so the operator
            # sees the PRE-gate FAIL somewhere. Pass the actual checkpoint
            # failure (exc) — NOT a synthetic F-PIPE code. The PRE-gate
            # soft-fail is not itself an F-PIPE-* event.
            _write_state_failure_wrapper(
                run_state,
                exc,
                vault_write=context.vault_write,
                clock=context.clock,
            )
        elapsed_ms = max(context.clock.now_ms() - start_wall_ms, 0)
        return PipelineRunResult(
            run_id=run_state.run_id,
            final_phase=run_state.phase,
            iterations_consumed=0,
            three_tab_envelope_hash=None,
            elapsed_ms=elapsed_ms,
            bypass_pending=False,
            pre_gate_failed=True,
            pre_gate_failure_code=pre_gate_result.failure_code,
        )

    # PRE-gate PASSED — transition phase + checkpoint.
    try:
        current_hash = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase="pre_gate_passed",
            expected_current_file_hash=current_hash,
            vault_write=context.vault_write,
            clock=context.clock,
            sleep=context.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state,
            exc,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        raise

    # ----- Step 4 — phase → inner_loop_iter_1 + checkpoint -----------------
    try:
        current_hash = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase="inner_loop_iter_1",
            expected_current_file_hash=current_hash,
            vault_write=context.vault_write,
            clock=context.clock,
            sleep=context.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state,
            exc,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        raise

    # ----- Step 5 — run_inner_loop (Round 5) -------------------------------
    # Round 5 writes its own state-failure checkpoints on any per-iteration
    # failure before raising; Round 11 does NOT add another wrapper on
    # inner-loop raises (avoids double-write). Non-PipelineFailure
    # exceptions still get a wrapper as a belt-and-braces.
    try:
        inner_result: InnerLoopResult = run_inner_loop(
            run_state=run_state,
            scribe_charter=scribe_charter,
            editor_charter=editor_charter,
            judge_charter=judge_charter,
            scribe_cascade=scribe_cascade,
            editor_cascade=editor_cascade,
            judge_cascade=judge_cascade,
            context_factory=context.seat_context_factory,
            subprocess_launcher=context.subprocess_launcher,
            vault_write=context.vault_write,
            clock=context.clock,
            sleep=context.sleep,
            initial_checkpoint_hash=current_hash,
            interrupt_probe=context.interrupt_probe,
            judge_parse=context.judge_parse,
            # v7: forward Red Team config when present. Default-None preserves
            # v6 4-seat behavior for test fixtures and explicit M13 bypass.
            red_team_charter=red_team_charter,
            red_team_cascade=red_team_cascade,
            rt_disagreement_threshold=rt_disagreement_threshold,
        )
    except PipelineFailure:
        # Round 5 already checkpointed state-failure + appended
        # IterationState. Propagate as-is.
        raise
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state,
            exc,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        raise

    current_hash = inner_result.final_checkpoint_hash

    # ----- Step 6 — run_post_gate_orchestration (Round 6) ------------------
    try:
        post_result: PostGateOrchestrationResult = run_post_gate_orchestration(
            run_state=run_state,
            inner_loop_result=inner_result,
            post_gate_input_factory=context.post_gate_input_factory,
            gate_runner=context.post_gate_runner,
            vault_write=context.vault_write,
            clock=context.clock,
            sleep=context.sleep,
            initial_checkpoint_hash=current_hash,
        )
    except PostGateRejected as rej:
        # Step 7 — bypass branch. Round 6 already wrote a state-failure
        # checkpoint; we add a supplementary bypass-pending marker +
        # return a soft-fail result. The operator's out-of-band sign-off
        # workflow reads pipeline/{run_id}/bypass_pending.json.
        _write_bypass_pending_marker(
            run_state=run_state,
            gate_result=rej.gate_result,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        elapsed_ms = max(context.clock.now_ms() - start_wall_ms, 0)
        return PipelineRunResult(
            run_id=run_state.run_id,
            final_phase=run_state.phase,
            iterations_consumed=inner_result.iterations_run,
            three_tab_envelope_hash=None,
            elapsed_ms=elapsed_ms,
            bypass_pending=True,
            pre_gate_failed=False,
            pre_gate_failure_code=None,
            post_gate_rejected_trigger=rej.trigger,
        )
    except PipelineFailure:
        # Round 6 already wrote state-failure for F_PIPE_03 / programmer
        # errors; propagate unchanged.
        raise
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state,
            exc,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        raise

    current_hash = post_result.committed_checkpoint_hash

    # ----- Step 8 — phase → signoff_pending [v7: or signoff_pending_council_split] ---
    # v7 (§5 v7 amendment §4.7): when revision_loop signaled
    # converged_on="council_split", route to signoff_pending_council_split
    # instead of signoff_pending. The operator UI reads run_state.phase
    # and presents the council-split decision UI per §10.6 when the
    # council_split sub-phase is active. Operator's CouncilSplitDecision
    # writes to run_state.council_split_decision; downstream code (sign-
    # off → report_signed) requires council_split_decision is not None
    # before advancing past the sub-phase.
    council_split = inner_result.converged_on == "council_split"
    target_signoff_phase = (
        "signoff_pending_council_split" if council_split else "signoff_pending"
    )
    try:
        current_hash = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase=target_signoff_phase,
            expected_current_file_hash=current_hash,
            vault_write=context.vault_write,
            clock=context.clock,
            sleep=context.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state,
            exc,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        raise

    # ----- Step 9 — sign-off stub (v0.1 interim) ---------------------------
    # No Ed25519 signature in v0.1. Phase transitions signoff_pending →
    # report_signed; the three_tab_envelope_hash (Round 9 output) is
    # pinned at step 10 below.
    #
    # v7: signoff_pending_council_split → report_signed requires
    # run_state.council_split_decision is not None (operator decision).
    # When the operator has not yet decided, run_pipeline returns early
    # with final_phase="signoff_pending_council_split" (analogous to the
    # bypass-pending branch). Operator's out-of-band UI fills in the
    # decision and re-runs run_pipeline (or a resume thereof) to advance.
    if council_split and run_state.council_split_decision is None:
        elapsed_ms = max(context.clock.now_ms() - start_wall_ms, 0)
        return PipelineRunResult(
            run_id=run_state.run_id,
            final_phase=run_state.phase,
            iterations_consumed=inner_result.iterations_run,
            three_tab_envelope_hash=None,
            elapsed_ms=elapsed_ms,
            bypass_pending=False,
            pre_gate_failed=False,
            pre_gate_failure_code=None,
            post_gate_rejected_trigger=None,
        )

    try:
        current_hash = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase="report_signed",
            expected_current_file_hash=current_hash,
            vault_write=context.vault_write,
            clock=context.clock,
            sleep=context.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state,
            exc,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        raise

    # ----- Step 10 — deliver_tab (Round 9) ---------------------------------
    try:
        tab_result: TabSigningResult = deliver_tab(
            run_state=run_state,
            vault_read=context.vault_read,
            vault_write=context.vault_write,
            clock=context.clock,
            hash_file=context.hash_file,
        )
    except PipelineFailure as exc:
        # Round 9 raises F_PIPE_01/16/21 unwrapped (spec pattern). We add
        # a state-failure wrapper since Round 9 does NOT checkpoint on
        # the failure path (tab_delivery.py is write-if-absent; there's
        # no CAS state to pin). Pass the actual caught exception — do
        # NOT synthesize a different F-PIPE code.
        _write_state_failure_wrapper(
            run_state,
            exc,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        raise
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state,
            exc,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        raise

    # Round 9 does not mutate run_state.three_tab_envelope_hash (by
    # design — §4.11 §4.1 step 11 is capstone-owned). Pin here.
    run_state.three_tab_envelope_hash = tab_result.envelope.envelope_sha256

    # ----- Step 11 — phase → tabs_delivered + final checkpoint -------------
    try:
        current_hash = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase="tabs_delivered",
            expected_current_file_hash=current_hash,
            vault_write=context.vault_write,
            clock=context.clock,
            sleep=context.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state,
            exc,
            vault_write=context.vault_write,
            clock=context.clock,
        )
        raise

    elapsed_ms = max(context.clock.now_ms() - start_wall_ms, 0)
    return PipelineRunResult(
        run_id=run_state.run_id,
        final_phase=run_state.phase,
        iterations_consumed=inner_result.iterations_run,
        three_tab_envelope_hash=tab_result.envelope.envelope_sha256,
        elapsed_ms=elapsed_ms,
        bypass_pending=False,
        pre_gate_failed=False,
        pre_gate_failure_code=None,
        post_gate_rejected_trigger=None,
    )


# ---------------------------------------------------------------------------
# Operator-facing entrypoint: 5-seat council is the DEFAULT (§5 v7 + §10).
# ---------------------------------------------------------------------------


def run_pipeline_5_seat(
    *,
    run_id: str,
    org_slug: str,
    session_id: str,
    rfa_hash: str,
    project_context_hash: str,
    scribe_charter: SeatCharter,
    editor_charter: SeatCharter,
    judge_charter: SeatCharter,
    red_team_charter: SeatCharter,
    scribe_cascade: ProviderCascade,
    editor_cascade: ProviderCascade,
    judge_cascade: ProviderCascade,
    red_team_cascade: ProviderCascade,
    context: RunPipelineContext,
    pre_gate_input_factory: PreGateInputFactory,
    rt_disagreement_threshold: int = 10,
) -> PipelineRunResult:
    """Operator-facing 5-seat council entrypoint (§5 v7 + §10 wired).

    Identical to :func:`run_pipeline` but ``red_team_charter`` and
    ``red_team_cascade`` are REQUIRED. This is the canonical default for
    operator-time runs per the §10 Red Team architecture mandate
    (A3 SFR + E cross-family + F.1 second-voice).

    Use :func:`run_pipeline` directly only when degraded-mode 4-seat
    operation is intentional (M13 review-seat-outage operator bypass,
    test fixtures, 4-seat MVP demo paths). In those cases pass
    ``red_team_charter=None`` + ``red_team_cascade=None`` explicitly.

    All other parameters and semantics match :func:`run_pipeline`. Council-
    split detection (|judge - red_team| >= rt_disagreement_threshold)
    routes to ``signoff_pending_council_split`` sub-phase per §10.6.
    """
    return run_pipeline(
        run_id=run_id,
        org_slug=org_slug,
        session_id=session_id,
        rfa_hash=rfa_hash,
        project_context_hash=project_context_hash,
        scribe_charter=scribe_charter,
        editor_charter=editor_charter,
        judge_charter=judge_charter,
        scribe_cascade=scribe_cascade,
        editor_cascade=editor_cascade,
        judge_cascade=judge_cascade,
        context=context,
        pre_gate_input_factory=pre_gate_input_factory,
        red_team_charter=red_team_charter,
        red_team_cascade=red_team_cascade,
        rt_disagreement_threshold=rt_disagreement_threshold,
    )


__all__ = [
    "BLUEPRINT_DEPS",
    "PipelineRunResult",
    "run_pipeline_5_seat",
    "PreGateInputFactory",
    "RunPipelineContext",
    "run_pipeline",
]
