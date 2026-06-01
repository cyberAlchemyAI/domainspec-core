# Round E — `session.py` + `interrupted_state.py` Spec Card

**Section:** 1 (Sovereignty Envelope)
**Modules:** `pipeline/sovereignty/session.py`, `pipeline/sovereignty/interrupted_state.py`
**Dependencies:** Round A (`_types`, `org_slug`, `crypto_primitives`), Round B (`topology`, `audit`), Round C (`keys`), Round D (`isolation`)
**Filed:** 2026-04-19
**Status:** Spec draft (LOCK-ready for implementation)

---

## Purpose

Implements blueprint §2.4 `Session` dataclass, §3.3 session lifecycle (`start_session`/`end_session`), §3.9 interrupted-state (`checkpoint`/`detect_interrupted`/`resume_or_discard`), §4.5 M6 atomic-flush + combined INTERRUPTED state, §4.6 M7 per-session HMAC key lifecycle, §4.7 M10 degradation threshold constant. Single-active-session invariant enforced via `fcntl` advisory lock at `sovereignty/sessions/.active.lock`.

§3.9.1 M14 Vault-as-substrate clarifier: §1 produces `(payload_bytes, manifest_dict)` at checkpoint; §2 v7 Vault owns the actual on-disk write. Since §2 is **Group 5** (not yet built), `interrupted_state` exposes a **vault-commit hook registration pattern**:
- `register_vault_commit_hook(hook: Callable)` — §2 Vault registers a real hook when Group 5 lands.
- `_DEFAULT_VAULT_COMMIT_HOOK` — Phase-0 direct-filesystem implementation that performs the M6 tmp→rename pattern locally. Used when no hook is registered; tests assert that when a mock hook IS registered, it receives `(payload_bytes, manifest_dict)` (not a file path).

## Primitives — `session.py`

### Module-level constants (§8)

```python
SESSION_HMAC_KEY_BYTES = 64                                   # <72 SHA3-512 block
SIGTERM_GRACE_SECONDS = 5
LLM_ACTIVE_CHECKPOINT_INTERVAL_SECONDS = 30
M10_AUTHOR_SEAT_DEGRADATION_THRESHOLD_SECONDS = 1800          # 30 min; read by §5
HMAC_KEY_ROTATION_GRACE_SECONDS = 5                           # v2 reduction from 60
SIGNAL_HANDLER_KEY_ZERO_FIRST = True
SIGNAL_HANDLER_ONE_SHOT_FLAG_NAME = "_shutting_down"
SIGNAL_HANDLER_CHECKPOINT_LOCK_NONBLOCKING = True             # v4 RT-v3 LOW-1
```

### `Session` dataclass (§2.4)

Frozen, kw_only. Fields:
- `session_id: str` (UUID4 canonical hex form)
- `slug: str` (validated via `org_slug.canonical_slug`)
- `started_at: str` (UTC ISO-8601)
- `hmac_key_id: str` (opaque KeyStore handle — never bytes)
- `router_manifest_sha: str`
- `pid: int`
- `status: str` ∈ {`"ACTIVE"`, `"ENDED_CLEAN"`, `"INTERRUPTED"`}
- `interrupted_payload_path: str | None`

Companion mutable runtime state (NOT on the frozen dataclass — tracked via module-level `_active_session_runtime: _SessionRuntime | None`):
- `_hmac_key_buffer: bytearray | None` (for zero-first signal handler)
- `_last_checkpoint_state: dict | None` (latest payload for signal-path checkpoint)

### `start_session(*, envelope, rfa, project_context) -> Session`

Boot-checked preconditions (§3.3):
1. No other ACTIVE session on disk — acquire `sovereignty/sessions/.active.lock` via `fcntl.flock(LOCK_EX | LOCK_NB)`; `BlockingIOError` → `SessionAlreadyActive`.
2. `rfa.session_bound_slug == project_context.slug` — else `SessionSlugMismatch`.
3. `canonical_slug(project_context.slug)` must round-trip — else `InvalidSlug`.
4. `envelope.router_manifest` signature verify OK — else `RouterIntegrityError`.
5. KeyStore HMAC issuance not permitted → `F-KEY-03` propagates.

Body:
1. `session_id = uuid.uuid4().hex`.
2. Generate `hmac_key = bytearray(secrets.token_bytes(SESSION_HMAC_KEY_BYTES))`.
3. `hmac_key_id = f"tilth.session.{session_id}.hmac.v1"`.
4. `keystore.store(key_id=hmac_key_id, key_bytes=hmac_key, purpose="session_hmac")`.
5. `zero_bytes(hmac_key)` in place.
6. Construct frozen `Session` record; write to `sovereignty/sessions/{session_id}.json` via tmp+rename (cross-fs double-check per §4.5).
7. Install unified signal handler (`SIGTERM`, `SIGINT`) via `signal.signal` + `signal.siginterrupt(..., False)`.
8. Start LLM-active checkpoint thread — writes every `LLM_ACTIVE_CHECKPOINT_INTERVAL_SECONDS` if `_last_checkpoint_state is not None`.
9. Return `Session`.

### `end_session(session, *, status="ENDED_CLEAN") -> None`

1. Cancel checkpoint thread (set stop event; `join(timeout=2)`).
2. Cancel any outstanding HMAC rotation timer.
3. `keystore.zero(session.hmac_key_id)`.
4. Rewrite session record with new `status`.
5. Release `.active.lock`.
6. Clear `_active_session_runtime`.

### `rotate_hmac_key(session) -> Session`

1. Generate new bytearray key + new `key_id` (version bumped).
2. `keystore.store(...)` + `zero_bytes(buf)`.
3. `threading.Timer(HMAC_KEY_ROTATION_GRACE_SECONDS, self._zero_old_key)` — callback invokes `keystore.zero(old_key_id)` + writes `degradation.jsonl` `rotation_grace_complete` event (`signed_by_operator=False`).
4. Return new `Session` with updated `hmac_key_id`.

### Signal handler (§4.5 v3 + v4)

```python
def _unified_signal_handler(signum, frame):
    if _shutting_down.is_set(): return
    _shutting_down.set()
    signal.alarm(SIGTERM_GRACE_SECONDS)
    try:
        # Step 1 — ZERO FIRST (v2 ordering).
        if runtime._hmac_key_buffer is not None:
            zero_bytes(runtime._hmac_key_buffer)
        # Step 2 — v4 NON-BLOCKING lock.
        if _checkpoint_lock.acquire(blocking=False):
            try:
                if runtime._last_checkpoint_state is not None:
                    checkpoint(runtime.session, runtime._last_checkpoint_state)
            finally:
                _checkpoint_lock.release()
        # Step 3 — best-effort keystore zero.
        try: resolve_keystore().zero(runtime.session.hmac_key_id)
        except Exception: pass
    finally:
        os._exit(130 if signum == signal.SIGINT else 143)
```

### `sign_health_tuple(session, tuple_bytes) -> bytes`

```python
with resolve_keystore().retrieve(session.hmac_key_id) as key:
    return hmac_sha3_512(key.view(), tuple_bytes)
```

Round A primitive `hmac_sha3_512(key: memoryview | bytes, data: bytes) -> bytes` — already LOCKED with `min_key_bytes=32`; our 64-byte session key satisfies that.

## Primitives — `interrupted_state.py`

### `VaultCommitHook` Protocol

```python
class VaultCommitHook(Protocol):
    def __call__(
        self, *, org_slug: str, sub_path: str,
        payload_bytes: bytes, manifest: dict,
    ) -> Path: ...
```

- `register_vault_commit_hook(hook: VaultCommitHook) -> VaultCommitHook | None` — returns prior hook (for unit-test replace/restore).
- `_current_vault_commit_hook() -> VaultCommitHook` — falls back to `_default_local_vault_commit` when no hook registered.

### `checkpoint(session, payload) -> Path`

1. Build combined dict: `{session_id, slug, started_at, hmac_key_id, router_manifest_sha, pid, status="INTERRUPTED", interrupted_at: <utc now iso>, interrupted_payload: canonical(payload)}`.
2. Serialize canonical JSON (sorted keys, UTF-8, no whitespace) → `payload_bytes`.
3. Build `manifest_dict = {"kind": "session_interrupted", "session_id": ..., "slug": ..., "sha3_512": sha3_512(payload_bytes).hex()}`.
4. Integrity pre-check: re-hash `payload_bytes` and re-serialize; mismatch → `F-ADM-05` before hand-off (per §3.9.1: §1 failure codes fire on §1-internal integrity, NOT displaced by F-VAULT-COMMIT-*).
5. `hook = _current_vault_commit_hook()`.
6. `path = hook(org_slug=session.slug, sub_path=f"runs/{session.session_id}/interrupted/", payload_bytes=payload_bytes, manifest=manifest_dict)`.
7. Return `path` as **read-only handle** (telemetry only).

### `_default_local_vault_commit(...)` — Phase-0 fallback

Performs M6 tmp+rename locally when no §2 Vault hook is registered:
1. Derive `final_path = repo_root/sovereignty/sessions/{session_id}.json` (the single combined file — v2 schema).
2. **Check A (pre-creation):** `os.stat(tmp_parent).st_dev == os.stat(final_parent).st_dev` — else `CrossFilesystemRename` (`F-ISO-06`).
3. `fd = os.open(tmp_path, O_CREAT|O_WRONLY|O_TRUNC, 0o600)`; `os.write`; `os.fsync(fd)`.
4. **Check B (post-creation, pre-rename):** `os.fstat(fd).st_dev == os.stat(final_parent).st_dev` — else `CrossFilesystemRename`; unlink tmp.
5. `os.close(fd)`; `os.rename(tmp_path, final_path)`.
6. Return `final_path`.

### `detect_interrupted(repo_root) -> Session | None`

- Scan `sovereignty/sessions/*.json`.
- Parse each; collect `status == "INTERRUPTED"`.
- Return newest by `started_at` (or `None`).

### `resume_or_discard(session, *, policy) -> dict | None`

- `policy == "resume"`: load payload from session record; validate against bound RFA + PROJECT_CONTEXT hashes (call `reverify_rfa` + `project_context.verify`); mismatch → `InterruptedStateInvalid`. Return payload.
- `policy == "discard"`: rewrite session with `status="ENDED_CLEAN"` via `checkpoint`-shaped write (tmp+rename); delete `interrupted_payload` field; return `None`.
- `policy == "prompt"`: raise `OperatorDecisionRequired`.

## Failure codes

- `F-SESSION-ALREADY-ACTIVE` — `.active.lock` contention.
- `F-SESSION-SLUG-MISMATCH` — RFA vs PROJECT_CONTEXT slug divergence.
- `F-SESSION-INVALID-SLUG` — canonicalization failure.
- `F-SESSION-RUNTIME-NOT-BOUND` — `sign_health_tuple` called with no active runtime (defensive, indicates test-mode misuse).
- `F-ADM-05` — integrity check mismatch before Vault hand-off.
- `F-ISO-06` — cross-fs rename detected in pre/post double-check (inherited from §4.5 v3).
- `F-VAULT-COMMIT-*` — raised by §2 hook; propagated.

## Test surface (Round E LOCK gate)

### `test_session.py` — unit (~30 cases)

Construction + lifecycle:
- `test_start_session_writes_record_and_locks_active`
- `test_start_session_rejects_concurrent_start_with_session_already_active`
- `test_start_session_rejects_rfa_slug_mismatch`
- `test_start_session_rejects_invalid_slug_canonicalization`
- `test_end_session_writes_ended_clean_and_zeroes_key`
- `test_end_session_cancels_checkpoint_thread`
- `test_end_session_cancels_rotation_timer`

HMAC lifecycle:
- `test_hmac_key_stored_in_keystore_not_returned_as_bytes`
- `test_start_session_zeroes_local_key_bytearray_after_store`
- `test_rotate_hmac_key_issues_new_id_and_schedules_grace_zero`
- `test_rotate_hmac_key_grace_5_seconds_then_zero`
- `test_rotate_hmac_key_timer_cancelled_on_end_session`
- `test_sign_health_tuple_uses_session_key_and_zeroes_on_exit`

Signal handler:
- `test_unified_signal_handler_zeroes_hmac_buffer_before_io` (monkey-patch `checkpoint` to sleep; assert buffer is zero BEFORE checkpoint runs)
- `test_unified_signal_handler_one_shot_flag_ignores_second_signal`
- `test_unified_signal_handler_nonblocking_lock_skips_checkpoint_on_contention`
- `test_unified_signal_handler_alarm_armed_at_5_seconds`
- `test_unified_signal_handler_sigint_exits_130_sigterm_exits_143` (via subprocess harness)

Constants:
- `test_constants_have_expected_values` (assert all §8 numbers)

### `test_interrupted_state.py` — unit (~20 cases)

Checkpoint emission:
- `test_checkpoint_emits_vault_commit_call_not_direct_filesystem_write` (§3.9.1 required test)
- `test_checkpoint_path_return_is_read_only_handle` (§3.9.1 required test)
- `test_atomic_flush_integrity_error_before_vault_commit_raises_f_adm_05_not_f_vault` (§3.9.1 required test)
- `test_checkpoint_payload_canonical_json_sorted_keys`
- `test_checkpoint_manifest_contains_sha3_512_of_payload`

Vault hook registration:
- `test_register_vault_commit_hook_returns_prior_hook_for_restore`
- `test_no_hook_registered_falls_back_to_default_local_vault_commit`
- `test_hook_receives_org_slug_and_sub_path_and_bytes`

Default local fallback (Phase-0):
- `test_default_local_vault_commit_performs_tmp_rename`
- `test_default_local_vault_commit_pre_create_st_dev_mismatch_raises_f_iso_06`
- `test_default_local_vault_commit_post_create_st_dev_mismatch_raises_f_iso_06`
- `test_default_local_vault_commit_post_rename_is_atomic` (either old or new, never partial)

Detection + policy:
- `test_detect_interrupted_returns_newest_interrupted_session`
- `test_detect_interrupted_returns_none_when_no_interrupted`
- `test_resume_validates_rfa_and_project_context_hashes`
- `test_resume_raises_interrupted_state_invalid_on_hash_mismatch`
- `test_discard_rewrites_session_ended_clean_and_clears_payload`
- `test_prompt_policy_raises_operator_decision_required`

### `test_session_adversarial.py` — adversarial probes (~10 cases)

Per Autonomy Rule 2 + cumulative lessons E-007..E-010:
- `test_adv_two_processes_race_for_active_lock_only_one_wins` (subprocess harness)
- `test_adv_signal_during_start_session_before_handler_installed_leaves_no_orphan_lock`
- `test_adv_signal_during_keystore_store_zeroes_buffer_and_exits_cleanly`
- `test_adv_rotation_race_signal_during_grace_zeroes_old_key_on_exit_watchdog`
- `test_adv_checkpoint_thread_holds_lock_signal_handler_skips_without_deadlock`
- `test_adv_second_sigterm_during_checkpoint_is_no_op` (one-shot flag)
- `test_adv_remount_between_check_a_and_check_b_raises_f_iso_06_mocked` (monkey-patch `os.fstat` to return different `st_dev` mid-write)
- `test_adv_vault_hook_raises_is_not_swallowed_by_integrity_checker` (F-VAULT-COMMIT-* propagates)
- `test_adv_sign_health_tuple_after_end_session_raises_key_not_found`
- `test_adv_post_end_session_second_end_is_idempotent_noop`

E-007 monkeypatch discipline: every test monkeypatches `session.resolve_keystore` / `interrupted_state._current_vault_commit_hook` (the names AS IMPORTED IN THE MODULE UNDER TEST), not the source modules.

### BT property tests (feed Round J)

- BT6: HMAC key lifecycle — issued at start, zeroed at end, NEVER observable in keystore after end_session.
- BT8: Degradation-log event for `rotation_grace_complete` is append-only + hash-chained per Round B audit.

## Provisioning manifest delta

No new Python deps. Uses stdlib `uuid`, `signal`, `threading`, `fcntl`, `os`, `json`, `secrets`.

## LOC estimate

- `session.py`: ~380 LOC (applying E-005 sub-system sizing: Session dataclass + start/end + rotation + signal handler + constants + sign_health_tuple = 5 sub-systems × ~60 LOC + 80 overhead).
- `interrupted_state.py`: ~260 LOC (per blueprint §1 module inventory row — checkpoint + hook registration + default fallback + detect + resume/discard = 4 sub-systems × ~55 LOC + 40 overhead).

Target range: session.py **340–430**; interrupted_state.py **230–300**.

## Handoff

Implementation proceeds under king-midas solo operation: build → green → adversarial → self-audit → commit committee dispatch via `round_e_2026-04-19/dispatch_round_e.py`. Committee runs v1 under two-cycle L-005 discipline. LOCK when ≥4/5 PASS and no unaddressed HIGH findings.
