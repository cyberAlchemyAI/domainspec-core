# Spec card — pipeline.loop.seat_runner (Round 4: invoke_seat + cascade level selection)

**STATUS:** LOCKED-backfilled

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal sections: §4.3 (Scribe invocation), §4.4 (Editor invocation), §4.5 (Judge invocation), §4.6 (revision-loop control), §3.2.3 SeatCharter, §3.2.4 ProviderCascade, §6 F-PIPE-07/08/09/17 (seat-specific failures), §8 subprocess timeouts

**Blueprint hash-at-card:**
- `section_05_pipeline.md`: `34ef007f3ab6d59d`
- `section_05_v6_amendment.md`: `16205371322681cf`

**Spec-card version:** v1 (pre-staged 2026-04-20 at §5 Round 3 SELF-LOCK)
**Round:** §5 Round 4 — seat_runner (invoke_seat skeleton + cascade advance)
**Depends on:** Round 1 (SeatCharter, ProviderCascade, IterationState, F_PIPE_07/08/09/17); Round 2 (`checkpoint_atomic`, ClockProtocol, SleepCallable); Round 3 (`start_run`, `resume_run`, RunState).

---

## Summary

Ship `pipeline/loop/seat_runner.py` — the first round that **consumes** `SeatCharter` + `ProviderCascade` from Round 1's data surface. Provides `invoke_seat(...)` per §4.3/§4.4/§4.5 with minimal-env subprocess launch + cascade level selection + timeout-to-cascade-advance.

```python
def invoke_seat(
    *,
    seat_kind: Literal["scribe", "editor", "judge"],
    run_state: RunState,
    iteration_number: int,
    charter: SeatCharter,
    cascade: ProviderCascade,
    subprocess_launcher: SubprocessLauncher,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
) -> SeatInvocationResult: ...
```

**Cascade level selection** is the key new primitive:
- Start at `cascade.current_level`.
- On timeout (`F-PIPE-07` / `-08` / `-09`), **advance to next level**; if none left, raise `F_PIPE_17.cascade_exhausted`.
- Return `(output_hash, landed_family, landed_model_id)` — A-v1-02 tuple.

**Zero runtime LLM calls.** `SubprocessLauncher` is an injected Protocol — production wires §2 Vault's `seat_launch`; tests inject a deterministic subprocess stub.

## Design decisions (pre-staged; revisit at Round 4 ORIENT)

1. **One public entry point.** `invoke_seat(seat_kind=..., ...)` dispatches on `seat_kind`. Per-seat wrappers `invoke_scribe` / `invoke_editor` / `invoke_judge` are thin one-liners (they just pin `seat_kind` + appropriate timeout constant).

2. **Timeout values pinned by Round 1 constants.** `SCRIBE_SUBPROCESS_TIMEOUT_MS = 300_000`, `EDITOR_SUBPROCESS_TIMEOUT_MS = 180_000`, `JUDGE_SUBPROCESS_TIMEOUT_MS = 180_000`. Use inline literals at the dispatch site — rebind-resistant.

3. **Minimal-env subprocess (A-v1-13).** The launcher receives only:
   `PATH`, `HOME`, `TILTH_SESSION_ID`, `TILTH_RUN_ID`, `TILTH_ORG_SLUG`, `TILTH_SEAT_KIND`.
   No BYOK tokens, no API keys. The subprocess reads its own keys via vault-inside-subprocess binding (§2 Vault's seat-launch contract — not Round 4's concern).

4. **Cross-family constraint validation (§4.4/§4.5).** At `invoke_editor` dispatch, assert Editor's charter `primary_provider_family != Scribe.actual_landed_family` (from `run_state.run_iteration_families_so_far["scribe"]`). Mismatch raises `F_PIPE_08.same_family_as_scribe`. At `invoke_judge`, assert Judge's family differs from BOTH Scribe and Editor's actual landed families — raises `F_PIPE_09.same_family_as_scribe_or_editor`.

5. **Cascade advance is in-memory.** `cascade.current_level` increments on timeout; the new `ProviderCascade` is returned alongside the result so the caller can persist it. Round 4 does NOT mutate the frozen Round-1 dataclass in place (frozen); it returns a fresh `ProviderCascade`.

6. **Judge parse checkpoint ordering (A-v1-15).** Judge parse is part of `invoke_seat` for `seat_kind="judge"`. On parse failure, Round 4 raises `F_PIPE_09.judge_parse_failed`; the caller (revision loop, Round 5) writes `state-failure` with `judge_verdict=None`. Round 4 does NOT write the success checkpoint itself — that's the revision loop's job (A-v1-15 closure moves this responsibility up a level).

7. **AST-lint R2 compliance.** `seat_runner.py` MUST NOT import `pipeline.logician` — enforced by Round 1's AST-lint R2 LOOP_LOGICIAN_BAN. Round 4 will verify the module lives under `pipeline/loop/` and carries no forbidden imports.

## Public API

```python
from dataclasses import dataclass
from typing import Literal, Protocol, runtime_checkable

@runtime_checkable
class SubprocessLauncher(Protocol):
    def __call__(
        self,
        *,
        seat_kind: str,
        env: dict[str, str],
        stdin_payload: bytes,
        timeout_ms: int,
    ) -> SubprocessResult: ...

@dataclass(frozen=True, kw_only=True, slots=True)
class SubprocessResult:
    exit_code: int
    stdout: bytes
    stderr: bytes
    timed_out: bool
    landed_family: str   # family the subprocess actually ran on
    landed_model_id: str

@dataclass(frozen=True, kw_only=True, slots=True)
class SeatInvocationResult:
    output_hash: str
    landed_family: str
    landed_model_id: str
    cascade_after: ProviderCascade
    level_advances: int  # how many levels were burned this invocation

def invoke_seat(...) -> SeatInvocationResult: ...
```

## Test surface

- **invoke_seat submission happy path (level 0):** Scribe subprocess returns structured payload → `SeatInvocationResult` with `cascade_after.current_level == 0`, `level_advances == 0`, `landed_family == charter.primary_provider_family`.
- **Timeout → cascade advance:** Level-0 times out, Level-1 succeeds → `level_advances == 1`, `cascade_after.current_level == 1`.
- **Cascade exhaustion:** All levels timeout → `F_PIPE_17.cascade_exhausted` raised.
- **Editor cross-family violation:** Editor charter family == Scribe's landed family → `F_PIPE_08.same_family_as_scribe` raised BEFORE any subprocess launch.
- **Judge three-way cross-family violation:** Judge family collides with Scribe OR Editor → `F_PIPE_09.same_family_as_scribe_or_editor`.
- **Judge parse failure:** subprocess returns well-formed output but parse fails → `F_PIPE_09.judge_parse_failed`.
- **Minimal-env contract (A-v1-13):** launcher's `env` dict contains ONLY the 6 whitelisted keys; any BYOK leak → test fails.
- **Timeout constant pins:** adversarial rebind of `SCRIBE_SUBPROCESS_TIMEOUT_MS` does NOT affect invocation timeout — inline literal at dispatch.
- **Frozen cascade returned fresh:** `cascade is not cascade_after` on level advance (new instance, not mutation).
- **Family recording:** `SeatInvocationResult.landed_family` matches subprocess's reported landed family (not charter's primary — subprocess is the source of truth after cascade advance).

## Done definition

- All new tests in `tests/loop/test_seat_runner.py` + `tests/loop/test_adv_seat_runner.py` green
- Coverage ≥ 95% on `pipeline/loop/seat_runner.py`
- AST-lint R1-R5 zero violations (R2 `loop-logician-ban` is the relevant guard)
- Full suite baseline + new-test-count green
- Pre-stage Round 5 spec card (`revision_loop.py` — `run_inner_loop` 3-iteration orchestrator consuming Round 4's `invoke_seat`)

## Lines-of-code target

| File | Target | Target ±25% |
|------|--------|-------------|
| `pipeline/loop/seat_runner.py` | 380 | 285–475 |
| `tests/loop/test_seat_runner.py` | 550 | 415–685 |
| `tests/loop/test_adv_seat_runner.py` | 180 | 135–225 |

## Self-LOCK eligibility

**Eligible.** No network surface; no LLM calls at test time (subprocess is injected); single-file deliverable; pure Protocol-based seam composition. Follow Scout R3 / §5 R3 precedent — if single-cycle pass + 95%+ coverage + lint clean, self-LOCK with committee dispatch deferred to post-§5 capstone or formal round-bundle review.

## Round 5+ preview

**Round 5** — `pipeline/loop/revision_loop.py` — `run_inner_loop(run_state)` per §4.6 v2 with A-v1-02 / A-v1-07 / A-v1-10 / A-v1-11 / A-v1-15 closures. Consumes Round 4's `invoke_seat`. Iterates `iter_n ∈ (1, 2, 3)`, writes phase boundary checkpoint, calls scribe → editor → judge, records landed families in `run_state.run_iteration_families_so_far`, handles `JudgeParseError` vs other `PipelineError` with different checkpoint intents.

**Round 6** — `pipeline/loop/post_gate_runner.py` — §4.7 POST gate orchestration consuming §4 Logician's `gate_runner.run_post_gate`.

**Rounds 7-10** — TokenBucket (§4.8 rate-limiter concrete), three-tab delivery, eval-mode orchestrator, capstone `run_pipeline.py`.

---

## Post-facto corrections (filed 2026-04-20 at Round 4 build)

Three spec-card errors caught at ORIENT cross-referencing against
`pipeline/loop/errors.py` and blueprint §4.9 line 646. Canonical
resolutions (also pinned in `pipeline/loop/seat_runner.py` module
docstring):

1. **Spec point 2 / Summary "cascade_exhausted"**: referenced
   `F_PIPE_17.cascade_exhausted`. F_PIPE_17 is
   `bypass_authorization_ledger_write_failed`. Correct code is
   **F_PIPE_06** (`rate_limit_exhausted — cascade exhausts + retries`)
   with trigger `cascade_exhausted`. Round 4 raises F_PIPE_06 when any
   timeout was observed during exhaustion.

2. **Spec point 4 / Test surface "same_family_as_scribe_or_editor"**:
   referenced F_PIPE_09. F_PIPE_09 is `judge_output_malformed`. Correct
   code for all cross-family exhaustion is **F_PIPE_08**
   (`cross_family_violation`), consistent with blueprint §4.9 line 646's
   `F_PIPE_08_cross_family_exhausted`. F_PIPE_09 only fires on Judge
   parse failure (trigger `judge_parse_failed`).

3. **Spec point 4 "assert BEFORE any subprocess launch"**: framed
   cross-family as a pre-dispatch assertion. Blueprint §4.9
   `select_cascade_level` consults the live
   `run_iteration_families_so_far` per level and **skips** colliding
   levels. Round 4 implements level-skipping; F_PIPE_08 fires only when
   the cascade exhausts with every remaining level colliding (no
   timeout observed). Preserves the timeout-vs-collision distinction at
   the exhaustion site.

Rationale for these not being architecture changes: they resolve
inconsistencies between the pre-staged spec card and the already-LOCKED
blueprint + Round-1 errors module. Future rounds should treat the
blueprint + errors module as authoritative over pre-staged spec-card
copy.

