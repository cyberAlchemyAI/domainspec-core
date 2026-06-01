# Spec card — pipeline.loop.run_pipeline (Round 11: §4.1 capstone submission-mode wiring)

**STATUS:** PRE-STAGED 2026-04-21 at §5 Round 10 cron_scheduler SELF-LOCK

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal section: §4.1 submission-mode pipeline entry — the 11-step sequence wiring R1-R10 end-to-end
- Supporting sections: §4.3 run-lifecycle boot (R3 `start_run`), §4.13 atomic CAS (R2 `checkpoint_atomic`), §4.4 seat invocation (R4 `invoke_seat`), §4.5/§4.6 revision loop (R5 `run_inner_loop`), §4.2 POST-gate orchestration (R6 `run_post_gate_orchestration`), §4.8 rate-limiter (R7 `reserve`/`release`/`can_reserve`), §4.9 cascade selection (R8 `select_cascade_level`), §4.10 cron (R10 `fire_once` — optional entrypoint wrapper), §4.11 tab delivery (R9 `deliver_tab`), §6 F-PIPE-* taxonomy (R1 errors)

**Blueprint hash-at-card:** `34ef007f3ab6d59d` (unchanged since §5 v6 LOCK 2026-04-19)

**Spec-card version:** v1 (pre-staged at Round 10 SELF-LOCK)
**Round:** §5 Round 11 — run_pipeline (capstone)
**Depends on:** Rounds 1-10 (all LOCKED). No new primitive rounds remain before capstone — R1-R10 are the full per-step toolkit. §4 Logician v2.2 (LOCKED). §2 Vault (LOCKED).

## Summary

Ship `pipeline/loop/run_pipeline.py` — the §4.1 submission-mode entry point that wires Rounds 1-10 into the end-to-end 11-step sequence:

1. `start_run` → seeds `RunState` (R3); checkpoint 0 via `checkpoint_atomic` (R2).
2. PRE-gate: `pipeline.logician.pre_gate.evaluate(run_state)` — fail-closed on F-PIPE-21/22/F-EVAL-CROSS-ORG-READ.
3. For each seat in (scribe, editor, judge):
   a. `select_cascade_level(...)` (R8) — pick family-clean + capacity-ready level; raises F-PIPE-08 on exhaustion.
   b. `reserve(...)` (R7) — acquire rate-limiter lease on the selected endpoint; on InsufficientTokens, advance cascade + retry.
   c. `invoke_seat(...)` (R4) — run the seat subprocess.
   d. `release(...)` (R7) — release lease.
   e. Checkpoint via `checkpoint_atomic` (R2) after each seat.
4. `run_inner_loop(...)` (R5) — revision loop with MAX_REVISION_ITERATIONS=3 ceiling + interrupt-probe.
5. `run_post_gate_orchestration(...)` (R6) — POST-gate; on reject, write `bypass-pending` checkpoint + raise F-PIPE-13.
6. Sign-off (future-work — v0.2 Ed25519 signing; Round 11 ships a stub that records the envelope_sha256 only).
7. `deliver_tab(...)` (R9) — assemble + write three-tab envelope.
8. Mark `RunState.phase = "tabs_delivered"` + final checkpoint.

Capstone is orchestration-only: no new primitives, no new F-PIPE codes, no new Protocols. All logic was built and tested in R1-R10. Round 11 is a composer.

## Public API (proposed)

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class PipelineRunResult:
    run_id: str
    final_phase: str                     # "tabs_delivered" on success
    iterations_consumed: int             # inner-loop iteration count
    three_tab_envelope_hash: str | None  # None iff short-circuited before R9
    elapsed_ms: int
    bypass_pending: bool                 # True iff POST-gate raised F_PIPE_13

def run_pipeline(
    *,
    run_id: str,
    org_slug: str,
    session_id: str,
    rfa_hash: str,
    project_context_hash: str,
    seat_charters: tuple[SeatCharter, ...],           # per-seat cascade + token budget
    vault_read: VaultReadCallable,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
    randint: RandIntFn,
    flock_acquire: FlockAcquire | None = None,        # None unless called from a cron wrapper
    subprocess_launcher: SubprocessLauncher,
    pre_gate: Callable[[RunState], PreGateResult],    # logician PRE-gate
    post_gate: GateRunnerProtocol,                    # R6 protocol
    interrupt_probe: InterruptProbe,
    hash_file: HashFileCallable,                      # R9 tab-payload hashing
    max_attempts_per_seat: int = 3,                   # inline-literal MAX_REVISION_ITERATIONS mirror
) -> PipelineRunResult: ...
```

Signature is long; the alternative (a `PipelineConfig` dataclass bundling the injected Protocols) is an ORIENT-time decision — propose a `RunPipelineContext` dataclass at ORIENT.

## §5 v6 compliance decisions (confirm at ORIENT)

1. **Cascade-seat routing.** Blueprint §4.1 step 3 invokes scribe, editor, judge in that order per-iteration. Round 11 inline-literals the ordering — tuple `("scribe", "editor", "judge")` — matching the AST-lint R2 LOOP_LOGICIAN_BAN policy (public logician API only; no dispatch via string parsing).

2. **Cascade retry loop.** When `reserve` returns `InsufficientTokens`, Round 11 advances the cascade `current_level_index` and calls `select_cascade_level` again. Per-seat ceiling: `max_attempts_per_seat=3` (inline-literal default). Ceiling exhaustion raises a new wrapper? NO — raise `F_PIPE_06 rate_limit_exhausted` bare, per Round 7 precedent.

3. **Checkpoint cadence.** Blueprint §4.1 prescribes checkpoints after every state-mutating step. Round 11 checkpoints after: step 1 (start), each seat invocation (step 3e), after revision-loop completion (step 4 end), after POST-gate (step 5 end), after sign-off (step 6 end), after tab delivery (step 7 end). Total: 4 + (N_iterations × 3 seats) checkpoints per run.

4. **Bypass-pending short-circuit.** POST-gate reject writes `bypass-pending` checkpoint via `VaultWriteCallable` (R6 wiring), raises `F_PIPE_13`. Round 11 catches `F_PIPE_13`, records `bypass_pending=True` on the result dataclass, returns (does NOT proceed to sign-off). Operator signs off manually via out-of-band workflow.

5. **Eval-mode routing.** Round 11 is SUBMISSION-MODE-ONLY. Entry asserts `mode="submission"` as inline literal; eval-mode entry is a separate `run_eval_pipeline` (future Round 12). No F_PIPE-21 guard at entry (§4.15 shields land in R9 `deliver_tab` already).

6. **Error propagation.** Any F-PIPE-* exception raised mid-pipeline propagates unchanged; Round 11 does NOT wrap. Best-effort final checkpoint via `_write_state_failure_wrapper` (reuse R2 helper) on exception path.

## Test plan (target coverage ≥95%)

**Happy paths** (`tests/loop/test_run_pipeline.py`) — ~15 tests:
- Zero-iteration happy path (scribe-only RFA) — all three seats land first cascade level; POST-gate passes first try; tab delivered.
- Three-seat linear path — scribe/editor/judge each land their first cascade level; single revision iteration.
- Revision loop — first POST-gate rejects, second iteration passes (R5 composition).
- Cascade advancement — scribe's first level is rate-limited; cascade advances to second level; succeeds.
- Rate-limit exhaustion → `F_PIPE_06`.
- PRE-gate rejects → early exit with F-PIPE-21/22 propagation (no seat invocation).
- POST-gate bypass path — `F_PIPE_13` caught, `bypass_pending=True` on result.
- Cross-family rigor — scribe anthropic, editor forced to google (cascade skips anthropic).
- Checkpoint cadence pin — count the `vault_write` calls at each phase.

**Adversarial** (`tests/loop/test_adv_run_pipeline.py`) — ~20 tests × E-024 2× = ~40 effective:
- Eval-mode entry (violates mode-isolation) → F_PIPE_21 or TypeError (confirm at ORIENT).
- Seat subprocess timeout → checkpoints state-failure, re-raises.
- Rate-limit reserve → release sequence integrity (release always called on success; skipped on InsufficientTokens).
- Bypass-pending marker path writes correct vault path.
- Operator interrupt mid-revision → graceful abort + final checkpoint.
- Rebind resistance — MAX_REVISION_ITERATIONS, TAB_ORDERING, etc. rebound → no behaviour change.
- Deterministic replay — same inputs + same fakes → same PipelineRunResult.
- Partial checkpoint failure — primary vault_write fails with VaultError → state-failure wrapper + re-raise.
- Three-seat all-family-exhausted → F_PIPE_08 from cascade; result not returned.

## Done definition

- [ ] `pipeline/loop/run_pipeline.py` ships `run_pipeline` + `PipelineRunResult` + (optionally) `RunPipelineContext`.
- [ ] ≥95% coverage via the two test files.
- [ ] Full suite green (baseline 4460 → target ≥ 4495 after +35 tests).
- [ ] AST-lint R1-R7 on `pipeline/loop/` clean.
- [ ] `pipeline/loop/__init__.py` re-exports public surface.
- [ ] `lock_history.v1.jsonl` entry.
- [ ] MEMORY.md index + round-recap memory file.
- [ ] Round 12 spec card pre-stage: §4.15 eval-mode orchestrator (`run_eval_pipeline`) OR a closing/audit round.

## Lines-of-code target (E-024 2× multiplier)

| File | Target | Target ±25% | Comment |
|------|--------|-------------|---------|
| `pipeline/loop/run_pipeline.py` | 450 | 340–560 | Capstone is orchestration-only; LOC driven by call-site glue + docstring. Comparable to Round 9 tab_delivery (482 LOC). |
| `tests/loop/test_run_pipeline.py` | 600 | 450–750 | ~15 tests × ~40 LOC with rich fakes for every injected Protocol. |
| `tests/loop/test_adv_run_pipeline.py` | 900 | 675–1125 | ~20 adv tests × 2× multiplier × heavier fakes. |

## Self-LOCK eligibility

**Ambiguous.** Round 11 is the FIRST §5 round that composes all nine injected Protocols simultaneously (vault_read, vault_write, clock, sleep, randint, flock_acquire, subprocess_launcher, pre_gate, post_gate, interrupt_probe, hash_file). If the ORIENT analysis produces a clean step-1-through-step-11 mapping with no cross-round ambiguity, self-LOCK single-cycle follows R3-R10 precedent. If ORIENT surfaces any ambiguity at a composition seam (e.g., how `PreGateResult` shape composes with `F_PIPE_21/22`), escalate to a Thesis Team dispatch under L-005 two-cycle.

## Round 12+ preview

**Round 12** — eval-mode orchestrator (§4.15 `run_eval_pipeline`): golden-set driver + calibration-report (§4.16). Depends on §4 Logician v2.2 eval-mode gates.

**Round 13** — §5 LOCKED-as-a-whole promotion: capstone integration tests + BT-property + fuzz (analog of §1 Round J). Unblocks §5 sign-off.

## Open questions (resolve at ORIENT)

1. **`RunPipelineContext` dataclass.** Ten injected Protocols + ten scalars in the signature is unwieldy. Propose bundling into a `RunPipelineContext(vault_read, vault_write, clock, sleep, randint, flock_acquire, subprocess_launcher, pre_gate, post_gate, interrupt_probe, hash_file)` frozen dataclass. ORIENT-decide: context dataclass OR explicit kwargs.

2. **Sign-off stub.** Blueprint §4.1 step 6 mentions report signing. v0.2 ships Ed25519 signing. Round 11 should ship a stub that records `envelope_sha256` without Ed25519 — explicitly flagged in docstring + lock_history as v0.1 interim.

3. **Rate-limiter release on cascade advance.** When `reserve` succeeds but a downstream seat fails, is the lease released on the failure path? Per Round 7's `release` contract: yes, always. Round 11 pairs `try/finally`-style: every `reserve` has a corresponding `release` in `finally`.

4. **Cron-wrapped entry.** `run_pipeline` is normally called directly. For cron-driven entries, the operator wraps: `fire_once(on_fire=lambda **k: run_pipeline(...))`. Round 11 does NOT include cron-wrapping logic — that's the caller's composition. `flock_acquire` stays optional in the signature for testability (tests don't need cron semantics).

5. **Where does `run_id` come from?** R3 `start_run` generates `run_id` via `RunIdFactory`. Round 11's `run_id` kwarg is the IDEMPOTENCY KEY — caller (cron wrapper) generates + passes. If caller omits, Round 11 delegates to `RunIdFactory`. ORIENT-decide: required kwarg vs optional-with-factory fallback.
