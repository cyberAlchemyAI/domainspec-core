"""pipeline.loop.post_gate_runner — §4.1 step 6-7 POST-gate orchestration (Round 6).

Blueprint §5 v6 LOCKED 2026-04-19:
- §4.1 step 6 — transition ``inner_loop_iter_{N}`` → ``post_gate_pending`` +
  state-success checkpoint (A-v1-12 resume-phase membership).
- §4.1 step 7 — call §4 Logician ``gate_runner.run_post_gate``.
- §3.2.1 v5 ``RunState.post_gate_result_hash`` +
  ``RunState.signed_claim_evidence_map_hash`` population on PASS.
- §6 F-PIPE-03 ``post_gate_timeout`` (wall-clock guard).

Round 6 is the first §5 module to consume §4 Logician primitives.
Imports go through the public surface ``pipeline.logician`` per
``pipeline.linting.ast_lint`` R2 LOOP_LOGICIAN_BAN — no reach-in to
``pipeline.logician.*`` internals.

**Design decisions (confirmed at Round 6 ORIENT — 2026-04-20)**

1. *POST_GATE_TIMEOUT_MS is an inline-literal default.* Blueprint §8
   does NOT define a POST-gate timeout constant (Round 6 consulted
   ``pipeline.loop.config`` — no matching pin). The §4 Logician body
   is deterministic Python with no network I/O, so the "timeout" guards
   against a programmer-error runaway loop. Round 6 pins ``timeout_ms
   = 120_000`` as an inline-literal kwarg default — rebind-resistant.
   If a future blueprint amendment introduces ``POST_GATE_TIMEOUT_MS``
   in §8, the kwarg default can point at it without altering dispatch.

2. *POST-gate FAIL → local subclass, not a new F-PIPE-XX code.*
   Blueprint §6 v6 §6 LOCKED enumerates 22 F-PIPE codes + F-PIPE-23
   (observability). None map to "POST-gate returned FAIL verdict" —
   the §4 Logician failure codes (F-POST-*) ARE the failure taxonomy
   for a FAIL verdict. Round 6 raises :class:`PostGateRejected`
   (a local ``PipelineFailure`` subclass) carrying the full
   :class:`GateRunnerPostResult` for downstream inspection. The raised
   exception's ``CODE`` is ``POST-GATE-REJECTED`` (NOT an F-PIPE code)
   so it does not collide with :data:`pipeline.loop.errors.F_PIPE_BY_CODE`.

3. *Canonicalizer mirrors Round 2 ``state_checkpoint``.* The
   ``post_gate_result_hash`` is ``sha256(hex)`` over
   ``json.dumps(sort_keys=True, separators=(",", ":"),
   default=_default)`` bytes. Same shape as
   :func:`pipeline.loop.state_checkpoint._canonicalize_runstate`.
   The hash is traceability metadata (pinned onto
   ``RunState.post_gate_result_hash``), not cryptographic attestation.

4. *``LogicianMidLoopCall`` propagates unwrapped.* §4 Logician owns
   the PRE → BETWEEN → POST → DONE state machine. If Round 6 observes
   ``LogicianMidLoopCall`` it is a caller programmer error (the caller
   must have already invoked ``mark_between()`` on the gate_runner
   after PRE-gate PASS). Round 6 writes a state-failure checkpoint
   then re-raises the original ``LogicianMidLoopCall`` — the spec card
   originally proposed translating it to ``F_PIPE_10`` but §6 pins
   F_PIPE_10 = ``signoff_cancelled``, not ``logician_called_mid_loop``.
   ORIENT resolution: surface the Logician's own exception type and
   let the caller dispatch.

5. *Resume-into-``post_gate_pending`` skips the phase-success
   checkpoint.* Blueprint §4.1 A-v1-12 resume set includes
   ``post_gate_pending``. If Round 6 is invoked with
   ``run_state.phase == "post_gate_pending"`` it means the prior
   attempt crashed after the phase-transition checkpoint; the phase
   is already durable and a second write would either be a no-op
   (same bytes → same CAS head) or a needless CAS cycle. Round 6
   short-circuits to directly invoke ``run_post_gate``.

6. *Factory is invoked exactly once.* The factory Protocol builds the
   :class:`PostGateInput`; Round 6 does not defensively catch factory
   exceptions. A factory raising :class:`ValueError` is a programmer
   error and propagates unwrapped.

7. *Wall-clock-elapsed guard uses ``max(elapsed, 0)``.* A
   non-monotonic clock (test fake returning decreasing values) is
   clamped to zero rather than crashing. Production ``clock.now_ms``
   is monotonic (§3.11 trusted-operator envelope) — the clamp is a
   belt on a lint-test fixture.

**Threat model (§3.11 v5 trusted-operator envelope; E-023 closure)**

Round 6 is an internal primitive consumed only by the capstone
``run_pipeline.py`` (Round 10+) and by Round 7+ tests. The following
residuals are OUT-OF-SCOPE for v0.1 and documented by explicit
``test_adv_*`` tests rather than defended at this layer:

- **Factory returns a malformed ``PostGateInput``.** §4 Logician's
  ``_execute_post_gate`` validates ``caller_step_outcomes`` completeness
  and raises ``ValueError`` for missing steps. Round 6 lets that
  propagate unwrapped — programmer error, not pipeline failure.

- **Gate result serialization raises.** If ``GateRunnerPostResult``
  contains a non-JSON-serialisable field, canonicalization raises
  ``TypeError`` → Round 6 writes state-failure, wraps as
  :class:`PostGateRejected` with ``trigger="post_gate_result_unserializable"``.

- **``claim_evidence_map`` structural divergence.** The map comes from
  §4 Logician Round 2's ``run_post_gate_skeleton``. Round 6 trusts
  the shape; ``signed_claim_evidence_map_hash`` is a simple sha256
  over canonical bytes.

- **Operator interruption DURING POST-gate.** §4 Logician's
  ``_execute_post_gate`` is pure Python (no seat subprocess). An
  interrupt observed during dispatch would be consumed only after
  return — but Round 6 never polls. Matches A-v1-11 post-checkpoint
  semantics: the operator can interrupt AFTER the POST-success
  checkpoint via the capstone's poll loop.

Spec card: ``pipeline/engineering/spec_cards/section_05_round_6_post_gate_runner.md``
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Final, Protocol, runtime_checkable

from pipeline.logician import (
    GateRunnerPostResult,
    LogicianMidLoopCall,
    PostGateInput,
)
from pipeline.loop.errors import F_PIPE_03, PipelineFailure
from pipeline.loop.revision_loop import InnerLoopResult
from pipeline.loop.state_checkpoint import (
    ClockProtocol,
    SleepCallable,
    VaultWriteCallable,
    checkpoint_atomic,
)
from pipeline.loop.types import RunState

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.1 step 6 post_gate_pending transition + checkpoint",
            "§4.1 step 7 gate_runner.run_post_gate dispatch",
            "§3.2.1 v5 post_gate_result_hash + signed_claim_evidence_map_hash",
            "§6 F-PIPE-03 post_gate_timeout",
        ],
    },
}


# ---------------------------------------------------------------------------
# Public Protocols (E-017 injected-callable pattern)
# ---------------------------------------------------------------------------


@runtime_checkable
class PostGateInputFactory(Protocol):
    """Caller-owned factory for the :class:`PostGateInput`.

    Round 6 does not assemble the §4 Logician input on its own. Callers
    (capstone ``run_pipeline.py`` in Rounds 10+) thread through the
    claim-evidence map reads, source-tag corpus, dossier signoffs, and
    caller-evaluated step outcomes that :class:`PostGateInput` requires.

    The factory is invoked exactly once per orchestration call with the
    live ``run_state`` and the winning :class:`InnerLoopResult`. Factory
    exceptions propagate unwrapped — Round 6 does NOT defensively catch.
    """

    def __call__(
        self,
        *,
        run_state: RunState,
        inner_loop_result: InnerLoopResult,
    ) -> PostGateInput: ...


@runtime_checkable
class GateRunnerProtocol(Protocol):
    """Thin facade over :class:`pipeline.logician.LogicianGateRunner`.

    The facade lets Round 6 inject a test double without importing the
    whole Logician (tests can pass a stub implementing just this single
    method). Production wires a ``LogicianGateRunner`` instance that has
    already transitioned to ``STATE_BETWEEN`` via its own
    ``mark_between`` call after PRE-gate PASS.
    """

    def run_post_gate(self, input_: PostGateInput) -> GateRunnerPostResult: ...


# ---------------------------------------------------------------------------
# Local exception — POST-gate FAIL verdict
# ---------------------------------------------------------------------------


class PostGateRejected(PipelineFailure):
    """Raised when ``gate_runner.run_post_gate`` returns ``passed=False``.

    Not an F-PIPE-XX code — blueprint §6 v6 LOCKED does not enumerate a
    dedicated code for "POST-gate returned FAIL verdict" (the §4 Logician
    failure codes ARE the taxonomy for a FAIL). ``CODE`` is the literal
    string ``"POST-GATE-REJECTED"`` and is NOT registered in
    :data:`pipeline.loop.errors.F_PIPE_BY_CODE`.

    Carries the full :class:`GateRunnerPostResult` on the ``gate_result``
    attribute so the caller can surface the §4 Logician failure codes
    and completed-step outcomes to the operator.
    """

    CODE: Final[str] = "POST-GATE-REJECTED"
    SEVERITY: Final[str] = "HIGH"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure (no phase transition)"

    def __init__(
        self,
        *,
        gate_result: GateRunnerPostResult,
        trigger: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(trigger=trigger, details=details)
        self.gate_result = gate_result


# ---------------------------------------------------------------------------
# Public result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class PostGateOrchestrationResult:
    """Returned on successful POST-gate orchestration (``gate_result.passed``).

    - ``gate_result``: the raw :class:`GateRunnerPostResult` from §4
      Logician.
    - ``committed_checkpoint_hash``: the CAS head after the final
      ``state-success`` checkpoint that wrote the ``post_gate_passed``
      phase + populated ``RunState.post_gate_result_hash``.
    - ``post_gate_result_hash``: sha256 hex of canonical
      ``gate_result`` bytes (mirrors
      :attr:`RunState.post_gate_result_hash`).
    - ``signed_claim_evidence_map_hash``: sha256 hex of canonical
      ``gate_result.claim_evidence_map`` bytes, or ``None`` when the
      map is absent (the FAIL path never returns this dataclass, so
      ``None`` here means §4 Logician's map-assembly step (9) was
      reached and returned an empty/None map).
    """

    gate_result: GateRunnerPostResult
    committed_checkpoint_hash: str
    post_gate_result_hash: str
    signed_claim_evidence_map_hash: str | None


# ---------------------------------------------------------------------------
# Internal canonicalization
# ---------------------------------------------------------------------------


def _canonical_default(obj: Any) -> Any:
    """``default=`` handler for ``json.dumps`` — mirrors Round 2 shape."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    if isinstance(obj, (frozenset, set)):
        return sorted(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return {"__repr__": repr(obj)}


def _canonical_bytes(payload: Any) -> bytes:
    """Deterministic canonical-bytes for a dataclass / dict / tuple tree."""
    if is_dataclass(payload) and not isinstance(payload, type):
        normalised: Any = asdict(payload)
    else:
        normalised = payload
    return json.dumps(
        normalised,
        sort_keys=True,
        separators=(",", ":"),
        default=_canonical_default,
    ).encode("utf-8")


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Public API — run_post_gate_orchestration
# ---------------------------------------------------------------------------


def run_post_gate_orchestration(
    *,
    run_state: RunState,
    inner_loop_result: InnerLoopResult,
    post_gate_input_factory: PostGateInputFactory,
    gate_runner: GateRunnerProtocol,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
    initial_checkpoint_hash: str,
    timeout_ms: int = 120_000,
) -> PostGateOrchestrationResult:
    """§4.1 step 6-7 — orchestrate the POST-gate evaluation.

    **Sequence:**

    1. If ``run_state.phase != "post_gate_pending"``, transition the
       phase and write a ``state-success`` checkpoint (§4.1 step 6).
       If the phase is already ``"post_gate_pending"`` (resume path,
       A-v1-12), skip — current_hash stays at ``initial_checkpoint_hash``.
    2. Build :class:`PostGateInput` via the caller-supplied factory.
    3. Measure ``clock.now_ms()`` before + after
       ``gate_runner.run_post_gate(input_)``. Any exception during the
       call path writes a ``state-failure`` checkpoint before
       re-raising.
    4. Wall-clock elapsed check: ``max(elapsed, 0) > timeout_ms`` →
       ``state-failure`` + :class:`F_PIPE_03`.
    5. Compute ``post_gate_result_hash`` + optional
       ``signed_claim_evidence_map_hash``.
    6. On ``gate_result.passed``: mutate run_state (phase →
       ``post_gate_passed``, hashes populated), write ``state-success``
       checkpoint, return :class:`PostGateOrchestrationResult`.
    7. On ``gate_result.passed is False``: pin
       ``post_gate_result_hash`` on run_state (traceability), write
       ``state-failure`` checkpoint, raise :class:`PostGateRejected`
       carrying the full gate_result.

    Parameters
    ----------
    run_state
        Live :class:`RunState`. Mutated on both PASS (phase + hashes +
        last_checkpoint_iso) and FAIL (post_gate_result_hash +
        last_checkpoint_iso).
    inner_loop_result
        The winning :class:`InnerLoopResult` from Round 5. Threaded
        through to the factory.
    post_gate_input_factory
        :class:`PostGateInputFactory` — invoked exactly once.
    gate_runner
        :class:`GateRunnerProtocol` — production wires a
        ``LogicianGateRunner`` already in ``STATE_BETWEEN``.
    vault_write, clock, sleep
        Injected Protocols (see module-level docs).
    initial_checkpoint_hash
        CAS head at entry — typically
        ``inner_loop_result.final_checkpoint_hash``.
    timeout_ms
        Wall-clock budget for ``gate_runner.run_post_gate``. Default
        ``120_000`` ms inline-literal (see design decision 1).

    Raises
    ------
    F_PIPE_03
        Wall-clock elapsed exceeded ``timeout_ms``.
    PostGateRejected
        ``gate_result.passed`` returned False. Carries the full
        :class:`GateRunnerPostResult` on ``.gate_result``.
    LogicianMidLoopCall
        §4 Logician's own state-machine guard — caller programmer
        error (gate_runner was not in ``STATE_BETWEEN``). State-failure
        checkpoint lands before re-raise.
    PipelineFailure
        Any other Round 2 checkpoint failure (F_PIPE_01 on CAS
        exhaustion) propagates.
    """

    # Step 1 — phase transition + checkpoint (A-v1-12 resume idempotency).
    current_hash = initial_checkpoint_hash
    # Inline-literal RHS — a rebind of a module attribute cannot fool this.
    if run_state.phase != "post_gate_pending":
        run_state.phase = "post_gate_pending"
        phase_ck = checkpoint_atomic(
            run_state,
            intent="state-success",
            expected_current_file_hash=current_hash,
            vault_write=vault_write,
            clock=clock,
            sleep=sleep,
        )
        current_hash = phase_ck.committed_hash

    # Step 2 — build PostGateInput (factory invoked exactly once).
    post_gate_input = post_gate_input_factory(
        run_state=run_state,
        inner_loop_result=inner_loop_result,
    )

    # Step 3 — dispatch, catching any exception to write state-failure.
    start_ms = clock.now_ms()
    try:
        gate_result = gate_runner.run_post_gate(post_gate_input)
    except LogicianMidLoopCall:
        # Programmer error — §4 Logician's state-machine guard fired.
        # Write state-failure and re-raise the original exception type
        # so the caller can distinguish from a FAIL verdict.
        _write_state_failure(
            run_state,
            current_hash,
            vault_write=vault_write,
            clock=clock,
            sleep=sleep,
        )
        raise
    except Exception:
        _write_state_failure(
            run_state,
            current_hash,
            vault_write=vault_write,
            clock=clock,
            sleep=sleep,
        )
        raise
    end_ms = clock.now_ms()
    elapsed_ms = max(end_ms - start_ms, 0)

    # Step 4 — wall-clock guard. Inline-literal comparison.
    if elapsed_ms > timeout_ms:
        _write_state_failure(
            run_state,
            current_hash,
            vault_write=vault_write,
            clock=clock,
            sleep=sleep,
        )
        raise F_PIPE_03(
            trigger="post_gate_timeout",
            details={
                "run_id": run_state.run_id,
                "elapsed_ms": elapsed_ms,
                "timeout_ms": timeout_ms,
            },
        )

    # Step 5 — compute post_gate_result_hash + claim_evidence hash.
    try:
        post_gate_result_hash = _sha256_hex(_canonical_bytes(gate_result))
    except TypeError as ser_err:
        # Out-of-contract: the §4 Logician result shape should be
        # JSON-serialisable via asdict. If not, write state-failure
        # and surface as PostGateRejected with a dedicated trigger.
        _write_state_failure(
            run_state,
            current_hash,
            vault_write=vault_write,
            clock=clock,
            sleep=sleep,
        )
        raise PostGateRejected(
            gate_result=gate_result,
            trigger="post_gate_result_unserializable",
            details={
                "run_id": run_state.run_id,
                "serialisation_error": repr(ser_err),
            },
        ) from ser_err

    if gate_result.claim_evidence_map is not None:
        signed_claim_evidence_map_hash: str | None = _sha256_hex(
            _canonical_bytes(gate_result.claim_evidence_map)
        )
    else:
        signed_claim_evidence_map_hash = None

    # Step 6 / 7 — branch on gate_result.passed.
    if gate_result.passed:
        run_state.post_gate_result_hash = post_gate_result_hash
        run_state.signed_claim_evidence_map_hash = signed_claim_evidence_map_hash
        run_state.phase = "post_gate_passed"
        success_ck = checkpoint_atomic(
            run_state,
            intent="state-success",
            expected_current_file_hash=current_hash,
            vault_write=vault_write,
            clock=clock,
            sleep=sleep,
        )
        return PostGateOrchestrationResult(
            gate_result=gate_result,
            committed_checkpoint_hash=success_ck.committed_hash,
            post_gate_result_hash=post_gate_result_hash,
            signed_claim_evidence_map_hash=signed_claim_evidence_map_hash,
        )

    # FAIL path — stay in post_gate_pending, write state-failure,
    # raise PostGateRejected with the §4 Logician failure taxonomy.
    run_state.post_gate_result_hash = post_gate_result_hash
    checkpoint_atomic(
        run_state,
        intent="state-failure",
        expected_current_file_hash=current_hash,
        vault_write=vault_write,
        clock=clock,
        sleep=sleep,
    )
    trigger = (
        f"post_gate_step_{gate_result.failed_step_number}_{gate_result.failure_code}"
        if gate_result.failed_step_number is not None
        else "post_gate_unknown_failure"
    )
    raise PostGateRejected(
        gate_result=gate_result,
        trigger=trigger,
        details={
            "run_id": run_state.run_id,
            "failed_step_number": gate_result.failed_step_number,
            "failure_code": gate_result.failure_code,
            "failure_codes": list(gate_result.failure_codes),
            "failure_detail": gate_result.failure_detail,
        },
    )


# ---------------------------------------------------------------------------
# Internal state-failure helper
# ---------------------------------------------------------------------------


def _write_state_failure(
    run_state: RunState,
    expected_current_file_hash: str,
    *,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
) -> None:
    """Best-effort state-failure checkpoint before re-raise / F-PIPE-03.

    Unlike Round 2's ``_write_state_failure_wrapper`` (which writes a
    sidecar ``state_failure.json`` with no CAS tracking), Round 6 writes
    the authoritative ``pipeline/{run_id}/state.json`` with
    ``intent="state-failure"`` + the caller's CAS pin. This keeps the
    CAS head consistent for the caller's next attempt (resume path).
    Any Round 2 failure (CAS exhaustion → F_PIPE_01) propagates
    unwrapped — the primary error still wins via the outer re-raise.
    """
    try:
        checkpoint_atomic(
            run_state,
            intent="state-failure",
            expected_current_file_hash=expected_current_file_hash,
            vault_write=vault_write,
            clock=clock,
            sleep=sleep,
        )
    except Exception:
        # Best-effort — do not mask the primary failure. The primary
        # exception re-raise happens in the caller's except block.
        return


__all__ = [
    "BLUEPRINT_DEPS",
    "GateRunnerProtocol",
    "PostGateInputFactory",
    "PostGateOrchestrationResult",
    "PostGateRejected",
    "run_post_gate_orchestration",
]
