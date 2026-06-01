# Spec card — pipeline.loop.state_checkpoint (Round 2: §4.13 atomic CAS envelope)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal sections: §4.1 step 2 `checkpoint_atomic` call; §4.13 atomic CAS-swap + quarantine marker + read-retry + total-timeout; §3.2.1 `quarantine_marker_ref` field; §6 F-PIPE-01 CRIT; §8 `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS=(50,200,800)` + `CHECKPOINT_TOTAL_TIMEOUT_SEC=10`

**Blueprint hash-at-card:**
- `section_05_pipeline.md`: `34ef007f3ab6d59d`
- `section_05_v6_amendment.md`: `16205371322681cf`

**Spec-card version:** v1 (pre-staged 2026-04-20 during §5 Round 1 LOCK)
**Round:** §5 Round 2 — state_checkpoint primitive
**Depends on:** Round 1 (RunState, F_PIPE_01, F_PIPE_22, CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS, CHECKPOINT_TOTAL_TIMEOUT_SEC, RUNSTATE_SCHEMA_VERSION); Section 2 v7 vault primitives (`vault_write` with `write_mode="write-if-absent"` + `expected_current_file_hash`); §2.6 Cedar policy (intent allowlist for `state-success`, `state-failure`, `state-quarantine`)

---

## Summary

Ship `pipeline/loop/state_checkpoint.py` — the single entry point by which `RunState` is persisted between every phase transition in the §5 pipeline. Core API:

```python
def checkpoint_atomic(
    run_state: RunState,
    intent: Literal["state-success","state-failure","state-quarantine"],
    *,
    expected_current_file_hash: str | None,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
) -> CheckpointResult: ...
```

Plus the resume-entry predicate `_assert_runstate_schema_current(rs)` which runs FIRST at the top of `resume_run` (Round 3), BEFORE any phase-set membership check. Round 2 owns the schema-assert helper because it is the first Round to have a concrete call site.

**Zero runtime LLM calls.** Zero vault I/O hard-wired — every vault interaction is via an injected `VaultWriteCallable` Protocol (E-017 pattern) so tests can run the CAS loop without a real vault.

## Design decisions (pre-staged; revisit at Round 2 ORIENT)

1. **CAS retry schedule is inline-literal.** `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS=(50,200,800)` is read from `pipeline.loop.config` but the V1-discipline inline-literal comparison at each retry site uses the literal `(50, 200, 800)` tuple. A rebind of the config constant cannot alter the back-off schedule at the call site.

2. **Total-timeout enforcement is inline-literal.** `CHECKPOINT_TOTAL_TIMEOUT_SEC=10` is likewise imported but the check `elapsed_ms > 10_000` uses the inline literal. Rebind-resistant.

3. **Quarantine marker writes BEFORE `F_PIPE_01` is raised.** A-v1-01 closure — per §4.13 line 819-821. The quarantine marker is a structured record of the last-known-good phase, written via `vault_write(intent="state-success", write_mode="overwrite")` at `vault/pipeline/{run_id}/quarantine.json`. The RunState's `quarantine_marker_ref` field is populated before the exception is raised.

4. **Back-off with deterministic sleep injection.** The back-off between CAS retries is `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS[min(attempt, 2)]` ms. Sleep is injected via a `SleepCallable` Protocol so tests can assert exact sleep durations without real-time waits.

5. **`_assert_runstate_schema_current` uses inline literals.** Per §4.1 step 1 (line 408): `rs.schema_version != 2` OR `rs.schema_version in frozenset({1})`. F_PIPE_22 is raised with `trigger="runstate_schema_downgrade"`; a `state-failure` checkpoint is written BEFORE re-raise. Schema-check precedes phase-check.

6. **`CheckpointResult` is a frozen dataclass.** Fields: `written_at_iso: str`, `committed_hash: str`, `attempt_count: int`, `elapsed_ms: int`, `quarantine_marker_ref: str | None`. Returned on success; raised-through on failure.

7. **AST-lint R1-R5 must remain clean.** Round 2 imports `RunState`, `F_PIPE_01`, `F_PIPE_22` from `pipeline.loop.*` only. No `logician.*` imports, no `llm_client.*` imports, no `open()` on vault paths (all I/O via injected `vault_write`).

## Public API

```python
# pipeline/loop/state_checkpoint.py
from pipeline.loop.types import RunState
from pipeline.loop.errors import F_PIPE_01, F_PIPE_22

@dataclass(frozen=True, slots=True, kw_only=True)
class CheckpointResult:
    written_at_iso: str
    committed_hash: str
    attempt_count: int
    elapsed_ms: int
    quarantine_marker_ref: str | None

@runtime_checkable
class VaultWriteCallable(Protocol):
    def __call__(
        self,
        path: str,
        payload: bytes,
        *,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str: ...

@runtime_checkable
class SleepCallable(Protocol):
    def __call__(self, ms: int) -> None: ...

@runtime_checkable
class ClockProtocol(Protocol):
    def now_ms(self) -> int: ...
    def now_iso(self) -> str: ...

def checkpoint_atomic(
    run_state: RunState,
    intent: str,
    *,
    expected_current_file_hash: str | None,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
) -> CheckpointResult: ...

def _assert_runstate_schema_current(rs: RunState) -> None: ...

def _write_quarantine_marker(
    run_state: RunState,
    reason: str,
    *,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
) -> str: ...
```

## Test surface

- **Property:** CAS retry count bounded by `len(CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS) = 3`; total elapsed bounded by `CHECKPOINT_TOTAL_TIMEOUT_SEC * 1000 = 10000`.
- **Happy path:** single-attempt success → CheckpointResult with attempt_count=1, quarantine_marker_ref=None.
- **Retry-and-win:** first 2 attempts return CAS mismatch, 3rd succeeds → attempt_count=3, back-off durations 50+200 ms.
- **Exhaustion → F_PIPE_01:** all 3 attempts CAS-mismatch → quarantine marker written (vault_write called with intent="state-success", path="vault/pipeline/{run_id}/quarantine.json") BEFORE F_PIPE_01 raised; run_state.quarantine_marker_ref populated.
- **Total-timeout → F_PIPE_01:** if clock shows `elapsed_ms > 10_000` between attempts, raise before attempting further retries (with quarantine marker).
- **Resume schema-downgrade:** `_assert_runstate_schema_current(rs)` where `rs.schema_version=1` → F_PIPE_22 raised AFTER a `state-failure` checkpoint was written.
- **Adversarial:** rebind `pipeline.loop.config.CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS` to `(1, 1, 1)` in-process → checkpoint_atomic still back-offs (50, 200, 800) ms per inline literal. Rebind `RUNSTATE_SCHEMA_VERSION` to 1 in-process → `_assert_runstate_schema_current(rs)` still catches `rs.schema_version=1` via inline `!= 2` literal.
- **Integration:** a faked `VaultWriteCallable` that raises `F-VAULT-*` errors on every call → F_PIPE_01 raised with quarantine marker. Idempotent replay (same RunState, same expected_current_file_hash) returns the same committed_hash (A-v1-10 write-if-absent guarantee).

## Done definition

- All new tests in `tests/loop/test_state_checkpoint.py` + `tests/loop/test_adv_state_checkpoint.py` green
- Coverage ≥ 95% on `pipeline/loop/state_checkpoint.py`
- AST-lint zero violations on `pipeline/` tree
- Full suite ≥ 1956 + new-test-count
- Committee dispatch via router.yaml `code_*` rows (5 reviewers, all_pass, retry cap 1)
- Lock history telemetry + memory entry + daily log update
- Pre-stage Round 3 spec card (run_lifecycle.py — `start_run` + `resume_run` orchestrator consuming Round 2's checkpoint primitive)

## Lines-of-code target

| File | Target | Target ±25% |
|------|--------|-------------|
| `pipeline/loop/state_checkpoint.py` | 280 | 210–350 |
| `tests/loop/test_state_checkpoint.py` | 380 | 285–475 |
| `tests/loop/test_adv_state_checkpoint.py` | 150 | 113–188 |

## Round 3+ spec-card preview

After Round 2 LOCK, Round 3 covers `pipeline/loop/run_lifecycle.py` — `start_run(request, golden_set_ref=None) -> RunState` (mode-locking at initialization) + `resume_run(run_id) -> RunState` (reads last checkpoint, runs `_assert_runstate_schema_current`, validates phase is in resume-allowed set). Round 3 is the first round that composes Round 2's checkpoint primitive.
