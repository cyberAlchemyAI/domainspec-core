# Spec card — pipeline.loop.run_lifecycle (Round 3: start_run + resume_run)

**STATUS:** SELF-LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal sections: §4.1 run lifecycle (v2 + v5 resume-phase validation + schema-enforcement); §3.2.1 RunState (mode-discriminated union construction); §6 F-PIPE-18, F-PIPE-22 (resume-phase mismatch + schema-downgrade); §8 (no new constants)

**Blueprint hash-at-card:**
- `section_05_pipeline.md`: `34ef007f3ab6d59d`
- `section_05_v6_amendment.md`: `16205371322681cf`

**Spec-card version:** v1 (pre-staged 2026-04-20 during §5 Round 2 SELF-LOCK)
**Round:** §5 Round 3 — run_lifecycle (start_run + resume_run)
**Depends on:** Round 1 (RunState, F_PIPE_*, config constants); Round 2 (`checkpoint_atomic`, `_assert_runstate_schema_current`, `CheckpointResult`, injected Protocols)

---

## Summary

Ship `pipeline/loop/run_lifecycle.py` — the two orchestrator entry points that wrap Round 2's checkpoint primitive with full lifecycle semantics.

```python
def start_run(
    *,
    mode: Literal["submission", "eval"],
    org_slug: str,
    session_id: str,
    rfa_hash: str | None,
    project_context_hash: str | None,
    golden_set_ref: str | None,
    run_id_factory: RunIdFactory,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
) -> RunState: ...

def resume_run(
    run_id: str,
    *,
    vault_read: VaultReadCallable,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
) -> RunState: ...
```

**Zero runtime LLM calls.** All vault I/O via injected Protocols; all timestamps via `ClockProtocol`. Round 2's `checkpoint_atomic` is the ONLY checkpoint path — `run_lifecycle` never touches the vault directly.

## Design decisions (pre-staged; revisit at Round 3 ORIENT)

1. **`start_run` enforces mode-discriminated union at `RunState(...)` construction.** The dataclass `__post_init__` already raises `F_PIPE_21` on cross-mode field presence (Round 1 shipped that). `start_run` surfaces those invariants to the caller as a clean `F_PIPE_21` rather than a bare `ValueError`.

2. **`start_run` writes the initial checkpoint via `checkpoint_atomic` with `expected_current_file_hash=None` + `intent="state-success"`.** The vault-write contract is `write-if-absent` under the hood but Round 2's public API takes `write_mode="overwrite"` for all cases; the `None` hash pin semantics are what signal "new file" to Section 2 Vault.

3. **`resume_run` validation order (v5 MA-07 / MB-05 strict):**
   - Step 1: Read the stored `RunState` via injected `vault_read`.
   - Step 2: `_assert_runstate_schema_current(rs)` — FIRST, before phase check. On `F_PIPE_22`, wrap with a `state-failure` checkpoint (via `_write_state_failure_wrapper`) then re-raise.
   - Step 3: Validate `rs.phase ∈ allowed_resume_set` (submission + eval phase sets, dispatched on `rs.mode`). On mismatch, write a quarantine marker + raise `F_PIPE_18.resume_phase_mismatch`.
   - Step 4: If `rs.phase == "degraded_paused"`, require `rs.bypass_pending_checkpoint_ref is not None`; else raise `F_PIPE_18`.

4. **Allowed resume phase sets are INLINE FROZENSETS.** V1 discipline — a module-attribute rebinding cannot broaden the set. Two sets, one per mode:
   - Submission mode: `{pre_gate_pending, pre_gate_passed, inner_loop_iter_1, inner_loop_iter_2, inner_loop_iter_3, post_gate_pending, signoff_pending, degraded_paused}`
   - Eval mode: `{eval_iter_pending, calibration_assembled}`

5. **`RunIdFactory` is injected.** A `Protocol` with `__call__(self) -> str`. Tests inject a deterministic ULID stub; production injects the real ULID generator.

6. **`VaultReadCallable` is a new injected Protocol.** Signature: `(path: str) -> bytes`. Raises `VaultError` subclasses on failure. `run_lifecycle` is the first round to need reads (Round 2 was write-only).

## Public API

```python
@runtime_checkable
class VaultReadCallable(Protocol):
    def __call__(self, *, path: str) -> bytes: ...

@runtime_checkable
class RunIdFactory(Protocol):
    def __call__(self) -> str: ...

def start_run(...) -> RunState: ...
def resume_run(...) -> RunState: ...

# Internal helpers (prefix _)
def _deserialize_runstate(payload: bytes) -> RunState: ...
def _allowed_resume_phases_for(mode: str) -> frozenset[str]: ...
```

## Test surface

- **start_run submission happy path:** constructs RunState with mode="submission", writes checkpoint, returns rs with phase="initialized".
- **start_run eval happy path:** mode="eval", golden_set_ref non-None, no rfa_hash — returns rs; mode-discriminated union enforced.
- **start_run cross-mode invariant:** submission + non-None golden_set_ref → F_PIPE_21 at RunState construction.
- **resume_run happy path:** valid stored bytes → RunState; phase in allowed set → returned.
- **resume_run schema downgrade:** stored rs.schema_version=1 → F_PIPE_22 raised AFTER state-failure checkpoint written.
- **resume_run phase mismatch:** stored phase="finalized" (not in allowed resume set) → F_PIPE_18 + quarantine marker.
- **resume_run degraded_paused without bypass_pending_checkpoint_ref:** F_PIPE_18.
- **Adversarial:** rebind allowed-phase frozenset in-process → `resume_run` still enforces inline-literal set.
- **Integration:** start_run → mutate phase → checkpoint → resume_run → returns a structurally-equal RunState.

## Done definition

- All new tests in `tests/loop/test_run_lifecycle.py` + `tests/loop/test_adv_run_lifecycle.py` green
- Coverage ≥ 95% on `pipeline/loop/run_lifecycle.py`
- AST-lint zero violations
- Full suite baseline + new-test-count green
- Pre-stage Round 4 spec card (`seat_runner.py` — per-seat subprocess invocation skeleton)

## Lines-of-code target

| File | Target | Target ±25% |
|------|--------|-------------|
| `pipeline/loop/run_lifecycle.py` | 320 | 240–400 |
| `tests/loop/test_run_lifecycle.py` | 450 | 340–560 |
| `tests/loop/test_adv_run_lifecycle.py` | 160 | 120–200 |

## Round 4+ preview

After Round 3 LOCK, Round 4 covers `pipeline/loop/seat_runner.py` — `invoke_seat(seat_kind, run_state, ...)` minimal-env subprocess launch + cross-family cascade level selection + timeout-to-cascade-advance. First round that consumes a SeatCharter + ProviderCascade from Round 1's data surface.
