# Spec card — pipeline.loop.cron_scheduler (Round 10: §4.10 v2 flock + vault-stamp two-layer dedupe)

**STATUS:** PRE-STAGED 2026-04-21 at §5 Round 8 cascade SELF-LOCK (Round 9 tab_delivery landed in parallel)

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal section: §4.10 v2 `fire_once` (blueprint lines 651–687) — two-layer dedupe (local flock + durable vault stamp), DST-safe task-id, CRON_VAULT_RETRY window
- Supporting sections: §8 `CRON_VAULT_RETRY_ATTEMPTS`, `CRON_VAULT_RETRY_WINDOW_SEC`, `CRON_STAMP_TTL_HOURS` (all Round 1 config.py exported); §6 F-PIPE-15 (`cron_dedupe_failure`); §2 vault `write-if-absent` mode + `VaultWriteExists` + `VaultTransientError`; closure A-v1-05 (two-layer dedupe) + B-v1-03 (DST-safe task-id)

**Blueprint hash-at-card:** `34ef007f3ab6d59d` (mirrors R7/R8/R9 — blueprint unchanged since §5 v6 LOCK)

**Spec-card version:** v1 (pre-staged at Round 8 SELF-LOCK)
**Round:** §5 Round 10 — cron_scheduler
**Depends on:** Round 1 (`F_PIPE_15`, `CRON_VAULT_RETRY_ATTEMPTS`, `CRON_VAULT_RETRY_WINDOW_SEC`, `CRON_STAMP_TTL_HOURS`); §2 vault `vault_write` with `write_mode="write-if-absent"` surface + `VaultWriteExists` / `VaultTransientError`; Round 2 `ClockProtocol`, `SleepCallable`, `VaultWriteCallable`.

## Summary

Ship `pipeline/loop/cron_scheduler.py` — §4.10 v2 `fire_once` two-layer dedupe primitive. Per blueprint §4.10 lines 655–687:

1. Compute DST-safe `cron_task_id = f"fund_radar_{YYYY-MM-DD}_{UTC_HH_MM}"` from a caller-supplied ISO anchor (operator decides the base task prefix; Round 10 owns only the id format). Local TZ is NEVER consulted — inclusion of `UTC_HH_MM` distinguishes two 08:30 local firings during DST fall-back (B-v1-03 closure).

2. **Local flock layer.** Non-blocking exclusive flock on `~/.tilth/cron_locks/{cron_task_id}.lock`. Acquired → proceed. Not acquired → short-circuit log + return (dedupe hit at layer 1).

3. **Vault stamp layer.** Under the flock, `vault_write(path=f"cron/fired/{cron_task_id}.stamp", ..., write_mode="write-if-absent")` with retry against `VaultTransientError` (up to `CRON_VAULT_RETRY_ATTEMPTS` = 3, total window `CRON_VAULT_RETRY_WINDOW_SEC` = 60; exponential back-off `min(30, 2**attempt)`s). `VaultWriteExists` → short-circuit log + return (dedupe hit at layer 2). Transient retries exhausted → raise `F_PIPE_15(trigger=f"cron_dedupe_failure:{cron_task_id}")` with flock RETAINED (operator must release).

4. **Downstream invocation.** Only on successful stamp write, invoke the caller-supplied `on_fire` callable (e.g., `invoke_scout_fund_radar`). Flock releases via the context manager after `on_fire` returns.

## Public API (proposed)

```python
@runtime_checkable
class FlockAcquire(Protocol):
    """Injected flock — returns a context manager yielding acquired-bool."""
    def __call__(self, lock_path: pathlib.Path) -> ContextManager[bool]: ...

@runtime_checkable
class OnFireCallable(Protocol):
    def __call__(self, *, cron_task_id: str) -> None: ...

@dataclass(frozen=True, kw_only=True, slots=True)
class CronFireResult:
    cron_task_id: str
    fired: bool                    # True iff on_fire invoked
    dedupe_layer: str | None       # None / "flock" / "vault_stamp"
    attempts: int                  # vault-write attempts consumed

def fire_once(
    *,
    cron_task_id: str,
    on_fire: OnFireCallable,
    flock_acquire: FlockAcquire,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
    lock_dir: pathlib.Path,          # tests inject tmp_path; prod uses ~/.tilth/cron_locks
    max_attempts: int = 3,           # inline-literal default per CRON_VAULT_RETRY_ATTEMPTS
    total_window_sec: int = 60,      # inline-literal default per CRON_VAULT_RETRY_WINDOW_SEC
) -> CronFireResult: ...
```

Task-id construction lives in a separate helper:

```python
def build_cron_task_id(
    *,
    prefix: str,                    # e.g., "fund_radar"
    utc_iso_anchor: str,            # ISO-8601 UTC (YYYY-MM-DDTHH:MM:...)
) -> str: ...
```

Format: `f"{prefix}_{YYYY-MM-DD}_{HH_MM}"`. Strict validation — anchor must be UTC (ends with `+00:00` or `Z`), `HH:MM` substituted to `HH_MM`.

## §5 v6 compliance decisions (confirm at ORIENT)

1. **Flock primitive.** Blueprint §4.10 line 661 uses `flock_exclusive_noblock(lock_path)`. Round 10 injects `FlockAcquire` (E-017 Protocol — 9th firing). Production wiring supplies `fcntl.flock(..., LOCK_EX | LOCK_NB)` under a `contextlib.contextmanager`. Tests inject a fake that yields `True` / `False` to exercise both branches without touching the real filesystem.

2. **Retry back-off formula.** Blueprint line 683: `sleep(min(30, 2 ** attempt))`. Round 10 inline-literals `30` and `2` at the computation site. `total_window_sec=60` is a defensive cap — the caller's wall-clock budget check fires if `clock.now_ms() - start_ms > 60_000` regardless of attempt count.

3. **CRON_VAULT_RETRY_ATTEMPTS pin.** `pipeline.loop.config.CRON_VAULT_RETRY_ATTEMPTS` = 3. Round 10 inline-literals `max_attempts=3` kwarg default with module-load assert mirroring Round 7's discipline.

4. **F_PIPE_15 trigger.** `cron_dedupe_failure:{cron_task_id}`. Details: `cron_task_id`, `attempts`, `elapsed_ms`, `last_error` (the VaultTransientError.__class__.__name__).

5. **Flock retained on F_PIPE_15 raise.** Blueprint line 682 is explicit: transient exhaustion raises WITHOUT releasing the flock. Round 10 must NOT use `finally`-unlock in the failure path — the context manager must see the exception propagate with the flock held. Tests verify file is still locked at exception time.

6. **Mode-isolation.** `fire_once` is a SUBMISSION-MODE primitive (eval mode does not fire crons). Round 10 does NOT assert mode here — this primitive is called BEFORE `start_run`; there is no `RunState` yet. Mode enforcement is the caller's job.

## Test plan (target coverage ≥95%)

**Happy paths** (`tests/loop/test_cron_scheduler.py`) — ~10 tests:
- First-fire success — flock acquired, stamp written first try, `on_fire` called, CronFireResult(fired=True, dedupe_layer=None, attempts=1).
- Flock contention — `flock_acquire` yields False → CronFireResult(fired=False, dedupe_layer="flock", attempts=0), `on_fire` NOT called.
- Vault stamp already exists → CronFireResult(fired=False, dedupe_layer="vault_stamp", attempts=1), `on_fire` NOT called.
- Vault transient retry-and-win — first attempt raises VaultTransientError, second succeeds; attempts=2.
- `build_cron_task_id` DST-safe (two 08:30 local firings during fall-back produce distinct UTC-anchored ids).
- `build_cron_task_id` format pin (`fund_radar_2026-04-21_12_30`).
- `build_cron_task_id` rejects non-UTC ISO anchor.

**Adversarial** (`tests/loop/test_adv_cron_scheduler.py`) — ~14 tests × E-024 2× = ~28 effective:
- F_PIPE_15 trigger taxonomy pin.
- Attempts exhausted → F_PIPE_15 with flock STILL HELD at raise-time (fake flock records release calls).
- Total window exceeded before attempts exhausted → F_PIPE_15 with `elapsed_ms > 60_000`.
- Rebind resistance — CRON_VAULT_RETRY_ATTEMPTS / CRON_VAULT_RETRY_WINDOW_SEC / CRON_STAMP_TTL_HOURS rebound → zero behaviour change.
- Non-monotonic clock — elapsed clamped at zero (no negative window).
- `on_fire` raising after successful stamp → exception propagates unwrapped; flock releases via context manager; stamp NOT rolled back (durable).
- `build_cron_task_id` reject empty prefix / empty anchor / timezone-less anchor / missing `T` / malformed `HH:MM`.
- Flock acquired but stamp write raises unexpected exception (not VaultTransientError / VaultWriteExists) — propagates; flock releases.
- Deterministic replay — same task_id + same vault state → same CronFireResult.
- Write-if-absent mode literal-pinned (not rebindable).
- Idempotency across concurrent callers (two processes race; first lands stamp, second sees VaultWriteExists).

## Done definition

- [ ] `pipeline/loop/cron_scheduler.py` ships with `fire_once` + `build_cron_task_id` + `CronFireResult` + `FlockAcquire` + `OnFireCallable` Protocols.
- [ ] 100% coverage via the two test files.
- [ ] Full suite green (baseline 4385 → target ≥ 4418 after +33 tests).
- [ ] AST-lint R1-R7 on `pipeline/loop/` clean.
- [ ] `pipeline/loop/__init__.py` re-exports public surface.
- [ ] `lock_history.v1.jsonl` entry.
- [ ] MEMORY.md index + round-recap memory file.
- [ ] Pre-stage Round 11 spec card (capstone `run_pipeline.py` wiring R1-R10 is the natural next — OR eval-mode orchestrator §4.15 as an alternative if operator prefers a narrower lane first).

## Lines-of-code target (E-024 2× multiplier)

| File | Target | Target ±25% | Comment |
|------|--------|-------------|---------|
| `pipeline/loop/cron_scheduler.py` | 280 | 210–350 | fire_once + build_cron_task_id + 2 Protocols + 1 result dataclass + back-off loop. Comparable to Round 6 post_gate_runner. |
| `tests/loop/test_cron_scheduler.py` | 350 | 260–440 | ~10 tests × ~35 LOC/test with shared FakeFlock / FakeVault / FakeClock. |
| `tests/loop/test_adv_cron_scheduler.py` | 700 | 525–875 | ~14 adv tests × 2× multiplier. |

## Self-LOCK eligibility

**Eligible if single-cycle pass.** §5 orchestrator primitive — no network, no subprocess (the injected `on_fire` is opaque), no §4 Logician consumption. Composes already-LOCKed Round 1 config + Round 2 Protocols + §2 vault write-if-absent surface. Follow §5 R3/R4/R5/R6/R7/R8 precedent.

## Round 11+ preview

**Round 11** — capstone `run_pipeline.py` wiring all §5 rounds end-to-end for submission-mode (start_run → PRE-gate → inner loop → POST-gate → sign-off → tab delivery).

**Round 12** — eval-mode orchestrator (§4.15 golden-set driver), calibration-report (§4.16), capstone eval-mode wiring.

## Open questions (resolve at ORIENT)

1. **Flock library choice.** stdlib `fcntl.flock` (POSIX-only; macOS + Linux confirmed) vs `filelock` package. Round 10 should stay stdlib-only for sovereignty — inject `FlockAcquire` Protocol so production wiring picks.

2. **`on_fire` failure rollback.** If `on_fire` raises AFTER stamp lands, should the stamp be rolled back? Propose: NO. Blueprint §4.10 line 685 is explicit — "Only reached on successful vault write. Flock released by context manager after sweep." The stamp is the durable "this task FIRED" record regardless of downstream success; the cron dedupe contract is "fired once per task_id", not "fired successfully once per task_id". Downstream failure is the caller's problem.

3. **Lock-file hygiene.** Stale `.lock` files from crashed processes linger. Round 10 does NOT sweep — operator boot script or a separate janitor primitive handles that. Document in module docstring.

4. **Task-id collision across prefixes.** Two cron triggers with different prefixes produce distinct task_ids by construction. No cross-prefix collision defense needed.
