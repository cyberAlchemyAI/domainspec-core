# Spec card — pipeline.loop.post_gate_runner (Round 6: POST-gate orchestration)

**STATUS:** SELF-LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal sections: §4.1 step 6–7 (`post_gate_pending` transition + `gate_runner.run_post_gate`), §4.7 POST-gate invocation (unchanged from v1), §3.2.1 RunState post-gate fields, §6 F-PIPE-03 (`post_gate_timeout`), F-PIPE-10 (`logician_called_mid_loop`), F-PIPE-18 (`resume_phase_mismatch`)
- Cross-section anchors: §4 Logician Round 6 `gate_runner.run_post_gate` (PostGateInput → GateRunnerPostResult); §4 Logician Round 2 claim-evidence assembler + canonical-byte-identical signing; §4 Logician Round 3 source-tag verify; §4 Logician Round 5 dossier verify.

**Blueprint hash-at-card:**
- `section_05_pipeline.md`: `34ef007f3ab6d59d`

**Spec-card version:** v1 (pre-staged 2026-04-20 at §5 Round 5 SELF-LOCK)
**Round:** §5 Round 6 — post_gate_runner (`run_post_gate_orchestration` consuming §4 Logician's `gate_runner.run_post_gate`)
**Depends on:** Round 1 (RunState, IterationState, F_PIPE_03/10/18); Round 2 (`checkpoint_atomic`); Round 4 (`invoke_seat` — NOT called directly by Round 6 but part of the forward-dependency lattice); Round 5 (`InnerLoopResult.final_iteration`, `InnerLoopResult.final_checkpoint_hash`); §4 Logician Round 6 (`gate_runner.run_post_gate` + `PostGateInput` + `GateRunnerPostResult`).

---

## Summary

Ship `pipeline/loop/post_gate_runner.py` — the orchestrator bridging §5 revision-loop convergence and §4 Logician POST-gate evaluation. Per blueprint §4.1 step 6–7:

1. Transition `run_state.phase` `inner_loop_iter_{N}` → `post_gate_pending`; write `state-success` checkpoint.
2. Construct `PostGateInput` from the convergent iteration (final_iteration hashes + caller-provided step outcomes).
3. Call §4 Logician's `gate_runner.run_post_gate(input_)`.
4. On PASS → write `state-success` checkpoint with `run_state.post_gate_result_hash` set; return a `PostGateOrchestrationResult`. On FAIL → write `state-failure` + raise dedicated `PipelineFailure` subclass carrying the caller-visible rejection reason.
5. Timeout guard → `F_PIPE_03` (`post_gate_timeout`). Mid-loop-call state-machine guard → `F_PIPE_10` (`logician_called_mid_loop`).

Public API:

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class PostGateOrchestrationResult:
    gate_result: GateRunnerPostResult  # from §4 Logician
    committed_checkpoint_hash: str  # CAS head after the success checkpoint
    post_gate_result_hash: str  # canonical-byte hash of the gate_result JSON
    signed_claim_evidence_map_hash: str | None  # when claim-evidence assembly succeeded

def run_post_gate_orchestration(
    *,
    run_state: RunState,
    inner_loop_result: InnerLoopResult,  # from Round 5
    post_gate_input_factory: PostGateInputFactory,  # Protocol
    gate_runner: GateRunnerProtocol,  # §4 Logician facade
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
    initial_checkpoint_hash: str,  # InnerLoopResult.final_checkpoint_hash
    timeout_ms: int = 120_000,  # INLINE LITERAL — §8 POST_GATE_TIMEOUT_MS pin
) -> PostGateOrchestrationResult: ...
```

**Protocols:**

- `PostGateInputFactory(Protocol, runtime_checkable)` — `(*, run_state, inner_loop_result) -> PostGateInput`. Same E-017 pattern as §5 R5's `SeatContextFactory`: caller owns input-assembly (claim-evidence map reads, source-tag corpus, dossier signoffs); Round 6 just dispatches.
- `GateRunnerProtocol(Protocol, runtime_checkable)` — `run_post_gate(input_: PostGateInput) -> GateRunnerPostResult`. Thin facade over §4 Logician's `GateRunner.run_post_gate`; lets Round 6 inject a test double without importing the full Logician.

## §5 v6 compliance decisions (must confirm at ORIENT)

1. **Inline-literal timeout.** `timeout_ms: int = 120_000` per §8 `POST_GATE_TIMEOUT_MS`. V1 discipline: rebinding the config constant cannot alter dispatch. **Confirm:** does §8 actually pin 120s for POST gate? (Round 4 used 300k/180k/180k for seats; POST gate is a different class of operation — Logician side is deterministic Python, no network.)

2. **Phase transition ordering.** Blueprint §4.1 step 6: phase → `post_gate_pending` + checkpoint BEFORE calling `run_post_gate`. On gate FAIL, we stay in `post_gate_pending` (do NOT transition to a new phase) and write `state-failure`. On gate PASS, we transition to `post_gate_passed` + state-success per step 7. **Confirm** against §4.1 pseudo-code whether `post_gate_passed` phase write happens BEFORE returning to §4.1 step 8 or is an inner concern of Round 6.

3. **A-v1-12 resume behavior.** Round 6 must tolerate resume into `post_gate_pending` (blueprint §4.1 resume set). On resume, Round 6 should NOT write a second phase-transition checkpoint — the phase is already `post_gate_pending`, so step 1 is a no-op idempotency guard. **Confirm** with a dedicated test: a pre-populated `run_state.phase == "post_gate_pending"` should skip the phase-success checkpoint and go straight to `run_post_gate`.

4. **Mid-loop guard (F_PIPE_10).** §4 Logician's `GateRunner` enforces its own PRE → BETWEEN → POST → DONE state machine via `LogicianMidLoopCall`. Round 6's responsibility is to translate that exception into `F_PIPE_10.logician_called_mid_loop` with the caller's context. **Confirm:** is `F_PIPE_10` the correct code? (F-PIPE-10 in §6 is documented; verify trigger-string.)

5. **Timeout enforcement mechanism.** §4 Logician's `run_post_gate` is pure Python (no network). Real timeout is vanishingly unlikely. But §6 F-PIPE-03 defines `post_gate_timeout` — so Round 6 MUST wrap the call with a wall-clock budget check. Simplest: measure `clock.now_ms()` before + after; if elapsed > `timeout_ms`, raise `F_PIPE_03`. No subprocess involved; no alarm handler needed.

6. **`post_gate_result_hash` canonical computation.** Round 6 serializes the `GateRunnerPostResult` to canonical JSON (same canonicalizer as §4 Logician Round 2 claim-evidence) and computes sha3_512[:16] hex. This hash is stored on `RunState.post_gate_result_hash` per §3.2.1 v5. **Confirm:** which canonicalizer — `json.dumps(sort_keys=True, separators=(",", ":"))` or §7.5 specialized?

## Out-of-scope for Round 6

- **Claim-evidence map assembly + signing.** Lives in §4 Logician Round 2. Round 6 consumes `input_.claim_evidence_map` from the caller-assembled `PostGateInput`; never constructs it.
- **Source-tag corpus preparation.** §4 Logician Round 3. Input-factory caller's responsibility.
- **Dossier signoff snapshots.** §4 Logician Round 5. Input-factory caller's responsibility.
- **Operator signoff (§4.1 step 8).** Round 7+ concern.
- **Three-tab delivery (§4.11).** Round 7+ concern.
- **Capstone wiring.** `run_pipeline.py` (Round 10+) composes Round 6 between Round 5 and the signoff orchestrator.

## Test surface (`tests/loop/test_post_gate_runner.py`)

**Happy paths (1 class, ~3 tests):**
- PASS verdict → `state-success` checkpoint written with `post_gate_result_hash` and `signed_claim_evidence_map_hash` populated on RunState.
- Resume into `post_gate_pending` skips the phase-success checkpoint (idempotency guard).
- `post_gate_passed` transition + checkpoint happens AFTER the gate returns PASS.

**Failure dispatch (1 class, ~4 tests):**
- `run_post_gate` returns FAIL → `state-failure` checkpoint + dedicated `PipelineFailure` subclass (e.g., `F_PIPE_16_post_gate_failed` — verify §6 code table).
- `LogicianMidLoopCall` → `F_PIPE_10`.
- Wall-clock elapsed > `timeout_ms` → `F_PIPE_03`.
- `vault_write` raising `F_PIPE_01` from any of the 3 checkpoint calls → propagates.

**A-v1-12 resume (1 class, ~2 tests):**
- Fresh entry: phase `inner_loop_iter_N` → write 2 checkpoints (phase + success-after-gate).
- Resume entry: phase `post_gate_pending` → write 1 checkpoint (only success-after-gate; phase already set).

**Hash threading (1 class, ~2 tests):**
- `initial_checkpoint_hash` from Round 5's `InnerLoopResult.final_checkpoint_hash` is passed verbatim to the first `vault_write` call.
- `committed_checkpoint_hash` on the returned `PostGateOrchestrationResult` equals the CAS head after the final `state-success` write.

**Factory contract (1 class, ~2 tests):**
- `post_gate_input_factory` invoked exactly once, with the live `run_state` and `inner_loop_result`.
- Factory exceptions propagate unwrapped (Round 6 does NOT defensively catch).

## Adversarial surface (`tests/loop/test_adv_post_gate_runner.py`)

- Factory returns a `PostGateInput` that fails §4 Logician's internal validation → `ValueError` from `run_post_gate` → propagates as-is (programmer error, not pipeline failure).
- `gate_result.verdict` is a valid PASS but `post_gate_result_hash` computation raises (malformed result payload) → out-of-scope per §4 Logician's contract; Round 6 SHOULD surface as `F_PIPE_16` with `trigger="post_gate_result_unserializable"`.
- Clock returning non-monotonic ms values → Round 6 must tolerate with `max(elapsed, 0)` clamp (add a pin test).
- `timeout_ms` rebind-resistance — mutating `pipeline.loop.config.POST_GATE_TIMEOUT_MS` does NOT alter dispatch (inline-literal default).
- `F_PIPE_10` is raised even if `gate_runner.state` was pre-set to `STATE_POST` (i.e., if someone called `run_post_gate` twice) — the Logician raises `LogicianMidLoopCall`; Round 6 wraps.
- `state-failure` checkpoint after gate FAIL must NOT transition phase to `post_gate_passed` (regression pin).

## Done definition

- All new tests in `tests/loop/test_post_gate_runner.py` + `tests/loop/test_adv_post_gate_runner.py` green.
- Coverage ≥ 95% on `pipeline/loop/post_gate_runner.py`.
- AST-lint R1–R7 zero violations on the new module.
- Full suite baseline + new-test-count green (target: 2428 + ~25-35 new = ~2450-2465).
- Pre-stage Round 7 spec card (`rate_limiter.py` — §4.8 v2 TokenBucket CAS-reserve + lease-TTL + back-off jitter).

## Lines-of-code target (E-024 4th firing — adversarial multiplier bumped to 3×)

| File | Target | Target ±25% | Comment |
|------|--------|-------------|---------|
| `pipeline/loop/post_gate_runner.py` | 400 | 300–500 | Orchestration + 2 Protocols + 1 result dataclass + 4 failure-code mappings + hash computation + resume idempotency. Simpler than Round 5 (no 3-iteration loop); more complex than Round 3 (more failure paths). Expect ~30% over on actuals → 520. |
| `tests/loop/test_post_gate_runner.py` | 650 | 490–810 | ~13 tests × 1.4× multiplier. |
| `tests/loop/test_adv_post_gate_runner.py` | 600 | 450–750 | ~6 adv tests × 3× multiplier per E-024 lesson-4 (pipeline-orchestrator adv tests consistently 2.5-3× their pre-staged target due to per-test setup ceremony). |

## Self-LOCK eligibility

**Eligible if single-cycle pass.** No network; §4 Logician already LOCKED (all 6 rounds); `gate_runner.run_post_gate` surface is stable; this is pure orchestration + state-machine dispatch. Follow §5 R3/R4/R5 precedent — if single-cycle pass + 95%+ coverage + lint clean, self-LOCK with committee dispatch deferred.

## Round 7+ preview

**Round 7** — `pipeline/loop/rate_limiter.py` — §4.8 v2 TokenBucket CAS-reserve with lease TTL (30s) + back-off jitter (B-v1-02 / B-v1-04 / B-v1-10 closures). First round to touch `RateLimiterState` (Round 1 dataclass) + the vault-read side of CAS loops.

**Rounds 8-10** — Three-tab delivery (§4.11 / §5.9), eval-mode orchestrator (§4.15), capstone `run_pipeline.py` wiring Rounds 3–9 under a single entry point per §9.

## Open questions (resolve at ORIENT)

1. **POST gate timeout constant.** Does §8 define `POST_GATE_TIMEOUT_MS = 120_000`? If not, pick a literal + document as R6 decision. The Logician is deterministic Python so a "timeout" here is really a programmer-error runaway loop; 120s is plenty of head-room.

2. **POST-fail failure code.** §6 F-PIPE table: is there a dedicated `F_PIPE_XX` for "POST-gate returned FAIL verdict"? F-PIPE-03 is `post_gate_timeout`; F-PIPE-16 is `cache_leak_detected` per §6 (verify). If no dedicated code exists, Round 6 may need a new code or reuse the gate_result's rejection payload via a wrapper exception.

3. **`signed_claim_evidence_map_hash` source.** §3.2.1 v5 has this field on RunState. Does `GateRunnerPostResult` carry it, or does Round 6 compute it from `input_.claim_evidence_map`? §4 Logician Round 2 defines the canonical-byte signing — confirm whether the signature hash surfaces on the gate result or only on the input.

4. **Canonicalizer for `post_gate_result_hash`.** Simple `json.dumps(sort_keys=True, separators=(",", ":"))` or §7.5 specialized (with NFC normalization + escape-sequence pins)? If the hash is consumed by later rounds for evidence linking, must match the canonicalizer used there.
