# Spec card — pipeline.loop.revision_loop (Round 5: run_inner_loop + convergence)

**STATUS:** LOCKED-backfilled

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal sections: §4.6 revision-loop control v2 (A-v1-02 / A-v1-07 / A-v1-10 / A-v1-11 / A-v1-15 closures), §3.2.2 IterationState, §6 F-PIPE-05/09/19, §9.8 iteration-cap tests

**Blueprint hash-at-card:**
- `section_05_pipeline.md`: `34ef007f3ab6d59d`
- `section_05_v6_amendment.md`: `16205371322681cf`

**Spec-card version:** v1 (pre-staged 2026-04-20 at §5 Round 4 SELF-LOCK)
**Round:** §5 Round 5 — revision_loop (`run_inner_loop` 3-iteration orchestrator consuming Round 4's `invoke_seat`)
**Depends on:** Round 1 (IterationState, RunState, F_PIPE_05/09/19); Round 2 (`checkpoint_atomic`); Round 3 (RunState lifecycle); Round 4 (`invoke_seat`, `SeatInvocationResult`).

---

## Summary

Ship `pipeline/loop/revision_loop.py` — the 3-iteration Scribe → Editor → Judge orchestrator per §4.6 v2. This is the first round that **composes** Round 4's `invoke_seat` across a multi-seat pipeline step. Adds convergence detection (score-threshold PASS, delta-plateau ≥75) and A-v1-02/07/10/11/15 closure enforcement.

```python
def run_inner_loop(
    *,
    run_state: RunState,
    scribe_charter: SeatCharter,
    editor_charter: SeatCharter,
    judge_charter: SeatCharter,
    scribe_cascade: ProviderCascade,
    editor_cascade: ProviderCascade,
    judge_cascade: ProviderCascade,
    subprocess_launcher: SubprocessLauncher,
    judge_parser: JudgeParserCallable,
    checkpoint_write: CheckpointWriter,
    interrupt_probe: InterruptProbe,
    clock: ClockProtocol,
    sleep: SleepCallable,
) -> IterationState: ...
```

**Core primitive** is the per-iteration body — iter_n ∈ (1, 2, 3):

1. A-v1-10 soft-restart guard: if any existing `IterationState.iter_number >= iter_n`, raise `F_PIPE_19.soft_restart_forbidden`.
2. A-v1-07 phase-invariant assert: `run_state.phase.startswith("inner_loop_iter_")`.
3. Phase transition + `state-success` checkpoint.
4. Invoke Scribe → record landed family IMMEDIATELY → Editor → record → Judge.
5. Parse Judge stdout via injected `JudgeParserCallable`:
   - Parse success → A-v1-15 success checkpoint AFTER parse + interrupt check.
   - Parse failure → `state-failure` checkpoint with `judge_verdict=None, failure_code="F-PIPE-09"` + re-raise `F_PIPE_09.judge_output_malformed`.
6. Convergence check: verdict == "PASS" → return; iter≥2 and delta-plateau ≥75 → return.
7. Exhausted all 3 iterations → `state-failure` checkpoint + raise `F_PIPE_05.iteration_cap_exceeded`.

**Zero runtime LLM calls.** `subprocess_launcher` + `judge_parser` + `checkpoint_write` + `interrupt_probe` are all injected Protocols (E-017).

## Design decisions (pre-staged; revisit at Round 5 ORIENT)

1. **Single entry point `run_inner_loop`.** No per-iteration public helper — the whole 3-iteration envelope is one atomic operation from the caller's view. Private `_run_single_iteration(run_state, iter_n, ...)` factored for testability.

2. **JudgeParserCallable Protocol.** Takes the Judge's raw stdout hash (or the launcher's raw stdout bytes via `SubprocessResult` — TBD at ORIENT) and returns a `JudgeParseResult(verdict, total_score, hash)` or raises `JudgeParseError` (wraps `F_PIPE_09.judge_output_malformed`). A-v1-15 moves parse ordering here, out of Round 4.

3. **InterruptProbe Protocol.** Returns `True` if an operator interrupt has been observed. A-v1-11 positions the call AFTER the success checkpoint; if observed, the current iteration is already durably recorded. Probe check raises `F_PIPE_20.operator_interrupt_observed` (NOT a new error — reuses existing) with the current iteration's final checkpoint sealed.

4. **CheckpointWriter Protocol.** Thin wrapper around Round 2's `checkpoint_atomic`; injected so tests can inspect the sequence of intents without needing a vault fixture. Production wires it to `checkpoint_atomic` directly.

5. **Convergence: delta-plateau at ≥75.** Per §4.6 v1 (preserved in v2) — if `iter_n >= 2` and the last two iterations' `judge_total_score` delta is ≤2 AND both scores ≥75, return with `converged_on="delta_plateau"`. Use inline-literal thresholds (75, 2); no config constant at §8 for these.

6. **IterationState append ordering is strict.** Append happens INSIDE the try/except — parse failure still appends an `IterationState` with `failure_code="F-PIPE-09"` before re-raising. Other `PipelineFailure` subclasses likewise append with the caught code before re-raising. This preserves A-v1-15's "never recorded as success" contract while ensuring the failure IS recorded.

7. **ProviderCascade persistence.** Round 4 returns `cascade_after` (a fresh ProviderCascade). Round 5 persists this into `run_state` between seats — but NOT across iterations. Each iteration starts with the operator-provided cascades at their original `current_level=0` (unless operator pins a higher start). Document this; adversarial test locks it.

8. **run_iteration_families_so_far reset per iteration.** A-v1-02 says "record IMMEDIATELY" (between seats WITHIN an iteration). Between iterations the dict is CLEARED so iter_2's Scribe is not artificially family-constrained by iter_1's Scribe landed. Document this nuance; spec-card decision to revisit at ORIENT if §4.6 is ambiguous.

9. **AST-lint R2 compliance.** `revision_loop.py` MUST NOT import `pipeline.logician`. R2's target_glob already covers it per Round 1's setup.

## Public API

```python
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

@dataclass(frozen=True, kw_only=True, slots=True)
class JudgeParseResult:
    verdict: Literal["PASS", "FAIL"]
    total_score: int
    hash: str  # stable hash of the structured parsed payload

@runtime_checkable
class JudgeParserCallable(Protocol):
    def __call__(self, *, raw_stdout_hash: str) -> JudgeParseResult: ...
    # Raises JudgeParseError (subclass of F_PIPE_09) on malformed payload.

@runtime_checkable
class InterruptProbe(Protocol):
    def __call__(self) -> bool: ...

@runtime_checkable
class CheckpointWriter(Protocol):
    def __call__(
        self, *, run_state: RunState, intent: str,
        expected_current_file_hash: str | None,
    ) -> CheckpointResult: ...

def run_inner_loop(...) -> IterationState: ...
```

## Test surface (main `tests/loop/test_revision_loop.py`)

**Happy path (3 classes, ~12 tests):**
- Iter-1 PASS verdict → return immediately, 1 state-success checkpoint, `converged_on="score_threshold"`.
- Iter-2 PASS verdict → 2 state-success checkpoints, `run_iteration_families_so_far` captures iter_2's families (not iter_1's).
- Iter-3 PASS verdict → 3 state-success checkpoints.
- Delta-plateau at iter_2 (scores 80 → 81) → `converged_on="delta_plateau"`, return with iter_n=2.
- Delta-plateau at iter_3 (scores 80 → 81 → 82) → `converged_on="delta_plateau"`, return with iter_n=3.

**Iteration-cap (1 class, ~3 tests):**
- All 3 iterations FAIL + no plateau → `F_PIPE_05.iteration_cap_exceeded` raised + state-failure checkpoint.
- Last `IterationState.converged_on == "cap_reached"` recorded before raise.

**Judge parse failure (1 class, ~3 tests):**
- Iter-1 Judge parse fails → `F_PIPE_09.judge_output_malformed` re-raised, state-failure checkpoint, iter-1 IterationState has `judge_verdict=None, failure_code="F-PIPE-09"`.
- Iter-2 Judge parse fails after iter-1 success → iter-1 intact, iter-2 state-failure appended, raise propagates.

**A-v1-02 landed-family recording (1 class, ~4 tests):**
- After Scribe returns, `run_state.run_iteration_families_so_far["scribe"]` set BEFORE Editor launches.
- After Editor returns, `run_iteration_families_so_far["editor"]` set BEFORE Judge launches.
- Editor charter's forbidden-family check sees Scribe's actually landed family (not charter's primary).
- Inter-iteration reset: iter_2 starts with `run_iteration_families_so_far == {}`.

**A-v1-07 phase-invariant (1 class, ~2 tests):**
- Pre-existing `run_state.phase == "pre_gate_passed"` at entry → AssertionError on first iteration boundary.
- Between iter_1 and iter_2, `run_state.phase` advances to `"inner_loop_iter_2"`.

**A-v1-10 soft-restart (1 class, ~3 tests):**
- Pre-existing `IterationState(iter_number=2)` in `run_state.iterations` + call → `F_PIPE_19.soft_restart_forbidden` on iter_1 entry.
- Pre-existing iter_number=1 → iter_1 guard fires (iter_1 would be a re-run).

**A-v1-11 interrupt (1 class, ~3 tests):**
- Probe returns True AFTER iter-1 checkpoint → raise (TBD exact code at ORIENT; likely `F_PIPE_20`), iter-1 state intact.
- Probe returns True BEFORE first iteration → never launches Scribe.

**Checkpoint ordering (1 class, ~3 tests):**
- Order of `CheckpointWriter` calls per iteration: (a) state-success at phase-transition, (b) state-success after success, OR (c) state-failure after parse/pipeline failure.
- Parse-failure checkpoint has `judge_verdict=None` in the RunState snapshot passed to CheckpointWriter.

**Convergence combinators (1 class, ~2 tests):**
- Iter-3 PASS after iter-1 FAIL + iter-2 FAIL → return with iter_3 as winner.
- Iter-1 delta-plateau is NOT detected (plateau requires iter_n >= 2).

## Adversarial surface (`tests/loop/test_adv_revision_loop.py`)

- Subprocess returns different landed family than cascade requested (A-v1-02 records the launcher's claim, not the requested family).
- JudgeParseError raised AFTER a successful Scribe + Editor invocation — state-failure still records Scribe + Editor hashes in IterationState.
- Interrupt raised BEFORE any iteration — no checkpoints written, no seats launched.
- InterruptProbe raising an unexpected exception (not bool return) — propagates to caller.
- CheckpointWriter raising VaultError (F_PIPE_01) from Round 2 — propagates; revision_loop does NOT swallow.
- Convergence thresholds (75, 2) rebind-resistance — module-attribute rebind does NOT change dispatch.
- Cascade-exhaustion during Scribe invocation (F_PIPE_07) — state-failure checkpoint + IterationState with failure_code="F-PIPE-07", re-raise.
- Cross-family violation during Editor (F_PIPE_08) — state-failure checkpoint, iter IterationState has Scribe hash + failure_code="F-PIPE-08".

## Done definition

- All new tests in `tests/loop/test_revision_loop.py` + `tests/loop/test_adv_revision_loop.py` green
- Coverage ≥ 95% on `pipeline/loop/revision_loop.py`
- AST-lint R1-R5 zero violations (R2 `loop-logician-ban` is the relevant guard)
- Full suite baseline + new-test-count green (target: 2228 + ~35-50 new = ~2270-2280)
- Pre-stage Round 6 spec card (`post_gate_runner.py` — §4.7 POST-gate orchestration)

## Lines-of-code target

| File | Target | Target ±25% | Comment |
|------|--------|-------------|---------|
| `pipeline/loop/revision_loop.py` | 450 | 340–560 | Three-iteration orchestrator + convergence + checkpoint dispatch |
| `tests/loop/test_revision_loop.py` | 700 | 525–875 | Multi-class happy/fail/convergence; applying E-024 1.5× test multiplier |
| `tests/loop/test_adv_revision_loop.py` | 300 | 225–375 | Applying E-024 2× adversarial multiplier |

E-024 note: Round 4 actuals (main 785 vs target 550 = 1.4×, adv 468 vs target 180 = 2.6×). Round 5 targets pre-expanded.

## Self-LOCK eligibility

**Eligible if single-cycle pass.** No network surface; no LLM calls at test time (launcher + parser + checkpoint-writer all injected); single-file deliverable; pure Protocol composition atop Round 4's `invoke_seat`. Follow Scout R3 / §5 R3 / §5 R4 precedent — if single-cycle pass + 95%+ coverage + lint clean, self-LOCK with committee dispatch deferred.

## Round 6+ preview

**Round 6** — `pipeline/loop/post_gate_runner.py` — §4.7 POST gate orchestration consuming §4 Logician's `gate_runner.run_post_gate`. Dispatches the §4.6 POST-gate sub-pipeline (claim-evidence assembly + source-tag verify + dossier verify) after `run_inner_loop` succeeds.

**Rounds 7-10** — TokenBucket concrete (§4.8 rate-limiter), three-tab delivery (§4.9 / §5.9 tab assembly), eval-mode orchestrator (§4.15 `run_eval_mode`), capstone `run_pipeline.py` wiring rounds 3–9 under a single entry point per §9.

## Open questions (resolve at ORIENT)

1. **JudgeParserCallable input surface.** Takes `raw_stdout_hash: str` or `raw_stdout: bytes`? Round 4 returns only the hash via `SeatInvocationResult`. If Round 5 needs the raw bytes, Round 4's return shape or `SubprocessLauncher` invocation needs to be widened. Provisional decision: parser takes raw bytes + hash, wired via a second `SubprocessResult`-returning helper `invoke_judge_with_raw`. Revisit.

2. **`run_iteration_families_so_far` reset semantics.** Blueprint §4.6 code block does NOT show an explicit reset between iterations. But A-v1-02 rationale says "record IMMEDIATELY" (WITHIN an iteration). Reading strictly, families accumulate ACROSS iterations — in which case iter_2's Scribe would be cross-family-excluded from iter_1's Scribe landed family. Provisional: clear between iterations to match the literal "so far this iteration" semantics implied by the field name. Revisit.

3. **Operator-interrupt error code.** Blueprint mentions `_check_interrupt_post_checkpoint` but does NOT specify the raised failure code. Round 1's F-PIPE-* list does not include a dedicated "operator interrupt observed" code — nearest match is `F_PIPE_20` (exists) or a new sub-trigger. Revisit.
