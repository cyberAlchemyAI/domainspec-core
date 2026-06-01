# Spec card — pipeline.vault.dispatcher (§2 Vault v7.1 §4.10.7 compound-transaction life-cycle — caller side of the §4.11 predicate)

**STATUS:** PRE-STAGED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.7.1 (lock at begin, held through commit/abort — single `vault/.write.lock`, no nesting)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.7.2 (in-memory staging, hash-at-stage-time, caps)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.7.3 (commit sequence under held lock — 6 steps, step 3 invokes §4.11 predicate)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.7.4 (5-step lock-release order on EVERY abort path — anti-DoS invariant)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.7.5 (per-file persist failure undo chain → F-VAULT-27)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.7.6 (crash between persists — §5.4 boot-gate recovery, COMPOUND_RECOVERY_SCAN_LINES=16)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.7.7 (staging-dict observability via `MappingProxyType`)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.7.8 (TTL enforcement sweep, COMPOUND_TXN_TTL_SECONDS=600)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.7.9 (token non-logging + print-prohibition → F-LOGICIAN-TOKEN-LEAK)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.5 (signed compound-kind registry, v0.1 enumeration `{index_amendment}`)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §4.10.6 (txn_token hard-gate at dispatcher entry — SIMPLE rejects `txn_token`, COMPOUND requires it)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §3.5 (path-level write lock topology)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §2.10 (`CompoundTxnState` + `StagedWrite` frozen dataclasses; runtime integrity check surface `F-VAULT-COMPOUND-INTEGRITY.*`)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §8 (constants: MAX_COMPOUND_TXN_BYTES=64 MiB, MAX_STAGED_WRITES_PER_TXN=8, MAX_STAGED_BYTES_PER_TXN=128 MiB, COMPOUND_TXN_TTL_SECONDS=600, COMPOUND_RECOVERY_SCAN_LINES=16, APPEND_CAS_HASH_CHUNK_BYTES=65536, TXN_TOKEN_REDACTION_PATTERN, token_urlsafe shape)
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` §7.18.1-13 (compound-transaction property tests — 13 vectors authoritative for test surface)
- `pipeline/blueprint/v0.1/section_04_logician.md` §4.11 (compound-commit predicate — consumed as a function, NOT re-implemented here)
- `pipeline/blueprint/v0.1/section_04_logician.md` §4.12 (PRE-append predicate — guards admin-risk ledger writes emitted by this dispatcher)
- `pipeline/blueprint/v0.1/section_05_pipeline.md` §5.4 (pipeline boot-gate — owns the crash-recovery scan invocation path specified in §4.10.7.6)

**Blueprint hash-at-card:** `<to-fill-at-implementation-time>` — author runs `python scripts/check_blueprint_drift.py` to compute the 16-char SHA3-512 prefix of `section_02_vault_topology.md` v7.1, `section_04_logician.md` v2.1, and `section_05_pipeline.md` v6 and pastes them here before Committee dispatch.

**Spec-card version:** v1
**Round:** Vault-dispatcher-compound-txn-R1 (caller side of Option-B compound-transaction enforcement; pairs with `pipeline/engineering/spec_cards/compound_commit.md` filed 2026-04-20 for the §4.11 predicate module)
**Futureproofing scope:** §4.1 public-API boundary; §4.6 BLUEPRINT_DEPS pinning; §4.7 schema-version pin on every on-disk artefact this module touches (admin-risk ledger rows, compound-recovery scan header); §4.9 regression discipline (every §7.18 vector preserved forever); §4.10 type hints; §4.11 docstring blueprint anchors. Additional scope: extensibility for new `CompoundTxnKind` values added at a future Section 2 / Section 4 LOCK cycle — this module MUST read its enumeration from `pipeline.logician.compound_commit.V0_1_COMPOUND_TXN_REGISTRY` (single source of truth) rather than shadowing a second copy.

**Companion artefacts (must land in the same commit):**
- `pipeline/logician/compound_commit.py` — §4.11 predicate module shipped under a sibling spec card (`pipeline/engineering/spec_cards/compound_commit.md`). This card CALLS `compound_commit_predicate` and depends on its `__all__` surface; the two cards must Committee-dispatch in the same round so the Committee sees the full caller-callee pair.
- `pipeline/logician/cedar_policies/compound_commit.cedar` — SKELETON on disk 2026-04-20; activated by the companion card's LOCK. This caller-side card does NOT activate the Cedar file; it consumes the activation via the predicate's return value.
- `pipeline/vault/tests/test_compound_txn.py` — the §7.18.1-13 test file (13 vectors) lives alongside this module.

---

## Summary

Ship the caller side of the Option-B compound-transaction life-cycle: the Section 2 vault dispatcher module's four public entry points (`begin_compound_txn`, `vault_write` under an active `txn_token`, `commit_compound_txn`, `abort_compound_txn`) plus their lock-discipline, staging-discipline, TTL-sweep, token-redaction, and crash-recovery primitives. The §4.11 compound-commit predicate is CALLED by this module at §4.10.7.3 step 3 — it is authored in a sibling module (`pipeline/logician/compound_commit.py`) under a companion spec card and is NOT re-implemented here.

Shipping this card completes the runtime invocation chain for the v0.1 `index_amendment` compound kind:

```
caller → begin_compound_txn(kind="index_amendment", session_id=S)
       → vault_write(txn_token=T, intent="index-update", path=…, data=…)       # stage only
       → vault_write(txn_token=T, intent="index-amendment-audit-append", …)    # stage only
       → commit_compound_txn(txn_token=T, session_id=S)
           ↳ step 1: runtime integrity check (§2.10)                            → F-VAULT-COMPOUND-INTEGRITY.*
           ↳ step 2: snapshot pre_commit_bytes, enforce MAX_COMPOUND_TXN_BYTES  → F-VAULT-COMPOUND-OVERSIZE.*
           ↳ step 3: CALL compound_commit_predicate(txn, registry, cedar)       → F-VAULT-24/25/26 or F-CEDAR-COMPOUND-DENIED.*
           ↳ step 4: persist each StagedWrite per write_mode primitive
           ↳ step 5: release vault/.write.lock
           ↳ step 6: return CommitResult
```

Every abort path (caller-explicit, predicate-denial, integrity-anomaly, oversize, per-file persist failure, TTL expiry) follows the 5-step lock-release order in §4.10.7.4; ledger appends NEVER happen under the held transaction lock.

Landing this closes the "caller-side half" of the Option-B compound-transaction decision (project memory `project_option_b_compound_txn_decision.md`). Establishes the dispatcher pattern for subsequent compound kinds (eventual `report_submission` at v0.2, `content_publish` at v0.2+ — all row-append, no dispatcher refactor).

## Design decisions

1. **Dispatcher, not executor of policy.** This module orchestrates the lock-staging-persist-abort flow; it delegates the admit/deny decision to `pipeline.logician.compound_commit.compound_commit_predicate`. The dispatcher's job is to build a well-formed `CompoundTxn` input, call the predicate, and act on `admit`. Rationale: Law 4 (fail-closed) + separation of concerns — predicate is pure decision, dispatcher is impure I/O.

2. **Single `.write.lock`, single acquire per transaction.** §4.10.7.1 pins this: the path-level write lock is acquired ONCE at `begin_compound_txn` and held until `commit_compound_txn` / `abort_compound_txn` returns. No staged `vault_write` re-acquires; no nested `flock` calls; no secondary lock file except the distinct `vault/.compound_txn.lock` that guards the staging-dict swap (which never overlaps with `.write.lock`). Rationale: Option-B v2's "serialise at commit" was retired in v7.1 precisely because serialise-at-begin is the simpler, deadlock-free model — do not reintroduce the complexity.

3. **Staging is in-memory; on-disk state only mutates at commit step 4.** `vault_write` under an active `txn_token` builds a frozen `StagedWrite` (hash pinned at stage-time per §2.10), atomically swaps the dispatcher's staging dict under `.compound_txn.lock`, and returns. No `.tmp/` files, no partial writes, no filesystem side effects during staging. Rationale: (a) crash during staging loses the txn cleanly (memory evaporates with the process; lock is released by OS on exit); (b) no half-amended intermediate state is ever visible on disk.

4. **Lock-release order on every abort is invariant, not advisory.** §4.10.7.4 specifies the 5-step sequence (detect → discard staging → release `.write.lock` → append admin-risk via its own lock acquire/release → return). Every abort path in the module MUST route through a single internal `_abort_with_release(txn_token, abort_code, evidence) -> AbortResult` helper; no abort path is allowed to inline a different order. Rationale: this is the anti-DoS invariant RT-v3-M-01 surfaced against Option-B v2; the helper-only discipline makes the invariant mechanically auditable (grep for `flock(LOCK_UN)` must return exactly one site — the one inside the helper).

5. **Caller-supplied `session_id` is verified against every StagedWrite AND against the CedarEvaluator's active-session lookup.** The dispatcher does NOT trust `txn.session_id` as authoritative on its own; it cross-checks against `cedar.lookup_session(S)` AND asserts every staged write carries the same `session_id`. Redundancy is deliberate: single-point failure would let a stolen token commit across a terminated session.

6. **Compound-kind enumeration is read from the companion predicate module, not shadowed.** The dispatcher imports `V0_1_COMPOUND_TXN_REGISTRY` from `pipeline.logician.compound_commit`; it does NOT maintain a second copy. Rationale: ARCH-04 R2 (`LOOP_LOGICIAN_BAN`) permits public-API imports from `pipeline.logician`; a shadow enumeration would drift silently at v0.2 when a new kind is added to the predicate side but not here. Single source of truth.

7. **Token is a bearer secret; redaction is load-bearing, not cosmetic.** §4.10.7.9's token redaction (log filter + print prohibition + 8-char-prefix-only in exception messages) is enforced by two mechanisms: (a) the dispatcher's `logging.Logger` is wrapped in a `TokenRedactionFilter` at module boot (the regex matches `TXN_TOKEN_REDACTION_PATTERN` from §8); (b) admin-risk ledger appends pass through Section 4 §4.12 PRE-append predicate which rejects records containing a raw-token-shaped string with `F-LOGICIAN-TOKEN-LEAK`. Neither layer alone is sufficient — (a) guards dispatcher-owned writes, (b) guards dispatcher-forwarded writes.

8. **Runtime integrity check precedes oversize check precedes predicate call.** Step order inside §4.10.7.3 is not permutable: integrity (phase 1) catches tampered `StagedWrite`/`CompoundTxnState` before either the oversize pre-read or the predicate wastes compute; oversize (phase 2) catches a 65 MiB bomb before step 3 reads any bytes off disk for hashing. Rationale: fail-cheap, fail-early — keep the expensive phases (predicate's hash-binding phase, Cedar dispatch) behind the cheap phases.

9. **No WAL at v0.1; boot-gate recovery covers crash-during-commit.** §4.10.7.6 is explicit: a write-ahead log is a v0.2 candidate. At v0.1, crash between persist #1 and persist #2 leaves the on-disk Index updated but the audit stamp missing. Recovery is §5.4 boot-gate's job — this module exposes the `scan_recent_index_amendment_audit_stamps(scan_lines=COMPOUND_RECOVERY_SCAN_LINES)` helper that §5.4 calls. This module does NOT run recovery on its own boot; it only exposes the helper.

10. **TTL sweep is pre-transaction-begin, not background.** §4.10.7.8 runs the sweep at every `begin_compound_txn` call under `.compound_txn.lock`. No background thread, no daemon process. Rationale: (a) keeps the module synchronous and deterministic; (b) sweep cost is amortised across txn begins and is O(|staging_dict|) which is bounded by `MAX_STAGED_WRITES_PER_TXN` × live-txn-count, a small constant at v0.1 (single operator). Per-kind TTL override is explicitly v0.2 backlog (Option-B design §15 item 5).

11. **Staging-dict observability is read-only through MappingProxyType.** §4.10.7.7: external modules can observe the staging dict via `_staging_view()` but cannot mutate it; only the dispatcher's own atomic swap under `.compound_txn.lock` writes. Same-uid hostile Python can bypass via `ctypes` / `object.__setattr__`; that is Bucket-A same-uid-peer out-of-model per Section 1 v6 trusted-operator envelope. The module documents the boundary; it does not attempt to harden against it.

12. **Failure codes are single-source-of-truth — this module emits a fixed closed set.** Emitted set is documented in the "Failure codes" section below. New codes require a spec-card amendment + blueprint §6 row-append; silent new codes at implementation time are a Committee-blocking finding.

## Public API (goes in `__all__`)

```python
# pipeline/vault/dispatcher.py
__all__ = [
    # Futureproofing pin (§4.6)
    "BLUEPRINT_DEPS",
    # Public dataclasses (re-exported shapes from §2.10)
    "CompoundTxnState",          # the live transaction handle
    "CompoundTxnKind",           # Literal type alias — v0.1: Literal["index_amendment"]
    "CommitResult",              # success return type of commit_compound_txn
    "AbortResult",               # return type of every abort path
    "StagedWrite",               # re-export of §2.10 inner record
    "TxnToken",                  # NewType["TxnToken", str] — typed token alias
    # Entry points (four)
    "begin_compound_txn",
    "vault_write",               # EXISTING §4.10 entry point — this card extends its txn_token code path, NOT its SIMPLE path
    "commit_compound_txn",
    "abort_compound_txn",
    # Boot-gate recovery helper (consumed by §5.4)
    "scan_recent_index_amendment_audit_stamps",
    # Observability helper (read-only)
    "staging_view",              # returns types.MappingProxyType[TxnToken, CompoundTxnState]
]
```

- `TxnToken = NewType("TxnToken", str)` — module-level NewType alias. Shape matches `secrets.token_urlsafe(32)` (43 base64url characters, 32 bytes of entropy). Typed rather than raw `str` so callers cannot accidentally cross bearer tokens with non-secret strings.
- `begin_compound_txn(kind: CompoundTxnKind, session_id: str) -> TxnToken` — atomically: (a) runs TTL sweep; (b) acquires `vault/.write.lock`; (c) validates `kind` against `V0_1_COMPOUND_TXN_REGISTRY` — unknown → `F-VAULT-28.unknown_txn_kind`, NO lock acquired, NO token minted; (d) validates `session_id` against CedarEvaluator active-session registry — missing/terminal → `F-VAULT-26`, release lock per §4.10.7.4; (e) mints `TxnToken` via `secrets.token_urlsafe(32)`; (f) initialises `CompoundTxnState` with `staged_writes=()`, records `created_at_monotonic_ns`; (g) stores in staging dict under `.compound_txn.lock`; (h) returns token.
- `vault_write(*, intent: str, path: str, data: bytes | str, session_id: str, txn_token: Optional[TxnToken] = None) -> VaultWriteResult` — EXISTING entry point; this card extends the `txn_token is not None` branch:
  1. §4.10.6 hard-gate: SIMPLE intent with `txn_token` → `F-VAULT-28.simple_intent_with_txn_token`; COMPOUND intent without `txn_token` → `F-VAULT-28.compound_intent_without_txn_token`.
  2. Validate token exists in staging dict → `F-VAULT-28.unknown_txn_token` if not.
  3. Validate session_id matches `CompoundTxnState.session_id` → `F-VAULT-26.compound_txn_session_mismatch` if not.
  4. Validate `path` against §4.10.5 `path_allowlist` for the bound `txn_kind` → `F-VAULT-PATH-ALLOWLIST-DENY` if not.
  5. Compute `data_sha3_512 = sha3_512_hex(canonical_bytes(data))` in the current call frame; NEVER lazy-defer (hash-at-stage-time is the §4.10.7.2 invariant).
  6. Construct a new frozen `StagedWrite(intent_tag, path, data, data_sha3_512, session_id)`.
  7. Atomically swap the `CompoundTxnState` in the staging dict under `.compound_txn.lock` with an extended `staged_writes` tuple.
  8. Enforce caps: `MAX_STAGED_WRITES_PER_TXN` (8), `MAX_STAGED_BYTES_PER_TXN` (128 MiB). Overflow → `F-VAULT-24.compound_txn_cap_exceeded`, route through `_abort_with_release`.
  9. Return `VaultWriteResult(status="staged", staged_write_index=N, staged_total_bytes=B)`.
- `commit_compound_txn(txn_token: TxnToken, session_id: str) -> CommitResult | AbortResult` — implements the §4.10.7.3 6-step sequence; returns `CommitResult` on permit, `AbortResult` on any failure. Every failure path routes through `_abort_with_release`.
- `abort_compound_txn(txn_token: TxnToken, *, reason: str = "caller_explicit", payload: Optional[Mapping[str, object]] = None) -> AbortResult` — caller-explicit abort. `payload` is passed to Section 4 §4.12 PRE-append predicate; a payload containing raw bytes or a raw-token-shaped string is rejected with `F-LOGICIAN-ABORT-PAYLOAD-LEAK` (§7.18.8). Routes through `_abort_with_release`.
- `scan_recent_index_amendment_audit_stamps(scan_lines: int = COMPOUND_RECOVERY_SCAN_LINES) -> RecoveryScanResult` — read-only helper exposed to §5.4 boot-gate. Reads the last `scan_lines` entries of admin-risk ledger filtered to `ledger_kind="index_amendment"`, computes the canonical-bytes SHA-3-512 of the current on-disk Index, returns `RecoveryScanResult(current_index_hash, matching_audit_stamps: tuple[AuditStampRecord, ...], orphaned: bool)`. §5.4 decides whether to boot-fail with `F-INDEX-STALE.orphaned_index_file` or accept; this helper NEVER writes.
- `staging_view() -> Mapping[TxnToken, CompoundTxnState]` — returns `types.MappingProxyType` wrapping the staging dict. External modules observe; they cannot mutate.

## Data structures

`CompoundTxnState` (frozen, kw_only) per §2.10:
```python
@dataclass(frozen=True, kw_only=True)
class CompoundTxnState:
    txn_token: TxnToken
    txn_kind: CompoundTxnKind
    session_id: str
    staged_writes: tuple[StagedWrite, ...]
    created_at_monotonic_ns: int
    # Populated at commit step 2, not at begin:
    pre_commit_bytes: Optional[tuple[tuple[str, bytes], ...]] = None
```

`StagedWrite` (frozen, kw_only) per §2.10:
```python
@dataclass(frozen=True, kw_only=True)
class StagedWrite:
    intent_tag: str
    path: str
    data: bytes                      # canonical_bytes already; NOT the raw caller bytes if they were str
    data_sha3_512: str               # 128-char lowercase hex (canonical-bytes hash)
    session_id: str
```

`CommitResult` (frozen, kw_only):
```python
@dataclass(frozen=True, kw_only=True)
class CommitResult:
    status: Literal["committed"]
    txn_token: TxnToken              # retained for callers' audit correlation; token is also redacted in logs
    persisted_hashes: tuple[tuple[str, str], ...]  # (intent_tag, post_image_sha3_512_hex) in write_order_at_persist order
```

`AbortResult` (frozen, kw_only):
```python
@dataclass(frozen=True, kw_only=True)
class AbortResult:
    status: Literal["aborted"]
    txn_token: TxnToken
    failure_code: str                # one of the emitted set below
    phase: Literal["begin", "stage", "commit_phase_1_integrity",
                   "commit_phase_2_oversize", "commit_phase_3_predicate",
                   "commit_phase_4_persist", "commit_phase_4_undo",
                   "ttl_sweep", "caller_explicit"]
    evidence: Mapping[str, object]
```

`RecoveryScanResult` (frozen, kw_only):
```python
@dataclass(frozen=True, kw_only=True)
class RecoveryScanResult:
    current_index_hash: str                                  # SHA-3-512 hex of on-disk Index at scan time
    matching_audit_stamps: tuple[AuditStampRecord, ...]      # empty tuple if no match → orphaned
    scanned_line_count: int                                  # <= COMPOUND_RECOVERY_SCAN_LINES
    orphaned: bool                                           # True iff matching_audit_stamps == ()
```

Constants (re-exported from `pipeline.vault.constants` which pins §8 values):
```python
MAX_COMPOUND_TXN_BYTES = 64 * 1024 * 1024           # 64 MiB pre_commit_bytes cap
MAX_STAGED_WRITES_PER_TXN = 8
MAX_STAGED_BYTES_PER_TXN = 128 * 1024 * 1024        # 128 MiB staging cap
COMPOUND_TXN_TTL_SECONDS = 600
COMPOUND_RECOVERY_SCAN_LINES = 16
APPEND_CAS_HASH_CHUNK_BYTES = 65536
TXN_TOKEN_REDACTION_PATTERN = r"[A-Za-z0-9_\-]{43}"  # matches secrets.token_urlsafe(32) shape
```

## Algorithms

### `begin_compound_txn(kind, session_id)` — §4.10.7.1 + §4.10.7.8

1. **TTL sweep under `.compound_txn.lock`.** Acquire `.compound_txn.lock`. Iterate staging-dict snapshot; for each entry with `now_monotonic_ns - created_at_monotonic_ns > COMPOUND_TXN_TTL_SECONDS * 1_000_000_000`: route through `_ttl_expire(token)` which (a) pops from staging dict, (b) releases that entry's held `vault/.write.lock`, (c) appends `F-VAULT-COMPOUND-TTL-EXPIRED` to admin-risk ledger via SIMPLE `vault_write`. Release `.compound_txn.lock` after sweep.
2. **Validate kind.** If `kind not in V0_1_COMPOUND_TXN_REGISTRY` → return `AbortResult(failure_code="F-VAULT-28.unknown_txn_kind", phase="begin", …)`. NO lock acquired. NO token minted. Append to admin-risk ledger via SIMPLE `vault_write`.
3. **Acquire `vault/.write.lock`.** `flock(LOCK_EX)`. Blocking. The second concurrent compound txn on the same kind serialises here (§4.10.7.1).
4. **Validate session.** Call `cedar.lookup_session(session_id)`; if None or terminal → route through `_abort_with_release` with `failure_code="F-VAULT-26.compound_txn_session_missing_at_begin"`, `phase="begin"`. Lock released per §4.10.7.4.
5. **Mint token.** `txn_token = TxnToken(secrets.token_urlsafe(32))`. Wrapped in the NewType for type-safety; raw string value is the bearer secret.
6. **Initialise state.** `state = CompoundTxnState(txn_token=txn_token, txn_kind=kind, session_id=session_id, staged_writes=(), created_at_monotonic_ns=time.monotonic_ns(), pre_commit_bytes=None)`.
7. **Store under `.compound_txn.lock`.** Atomic dict swap.
8. **Return token.** Log via `_dispatcher_logger.info("compound txn begun kind=%s session=%s token=%s", kind, session_id, txn_token)` — the logger's `TokenRedactionFilter` rewrites the token to `<redacted:token>` before the record reaches any handler.

### `vault_write(..., txn_token=T, ...)` — §4.10.7.2 staging branch

See the 9-step sequence in the Public API entry above. Short-circuit on the first failure; every failure path routes through `_abort_with_release` EXCEPT `F-VAULT-28.simple_intent_with_txn_token` / `F-VAULT-28.compound_intent_without_txn_token` which are dispatcher-entry violations and do not have a live txn to abort.

### `commit_compound_txn(txn_token, session_id)` — §4.10.7.3

1. **Load state.** `state = staging_dict.get(txn_token)`; if None → `AbortResult(failure_code="F-VAULT-28.unknown_txn_token", phase="commit_phase_1_integrity", …)`. No lock held; nothing to release.
2. **Validate session_id.** If `session_id != state.session_id` → route through `_abort_with_release` with `failure_code="F-VAULT-26.compound_txn_session_mismatch_at_commit"`, `phase="commit_phase_1_integrity"`. The `.write.lock` IS held (from begin); release per §4.10.7.4.
3. **Runtime integrity check (phase 1).** Validate `state` is a frozen dataclass instance of `CompoundTxnState`; validate every `StagedWrite` in `state.staged_writes` is a frozen dataclass instance; validate `data_sha3_512` fields match `sha3_512_hex(canonical_bytes(sw.data))` for every staged write (re-hash, don't trust the stored field). Any anomaly → `_abort_with_release(failure_code="F-VAULT-COMPOUND-INTEGRITY.<subtype>", phase="commit_phase_1_integrity", ...)`. Subtypes: `state_not_frozen`, `staged_write_not_frozen`, `data_hash_mismatch`.
4. **Snapshot pre_commit_bytes (phase 2).** For each `sw in state.staged_writes`: read the current on-disk bytes of `sw.path` (empty-bytes if the file does not exist — a `write-if-absent` persist target is expected to not exist pre-commit). Build `pre_commit_bytes = tuple((sw.path, current_bytes) for sw in state.staged_writes)`. Enforce `sum(len(b) for _, b in pre_commit_bytes) <= MAX_COMPOUND_TXN_BYTES`. Overflow → `_abort_with_release(failure_code="F-VAULT-COMPOUND-OVERSIZE.pre_commit_bytes_overflow", phase="commit_phase_2_oversize", ...)`. Update `state` with `pre_commit_bytes` populated (frozen-dataclass `replace`, re-swap under `.compound_txn.lock`).
5. **Invoke §4.11 predicate (phase 3).** Build `CompoundTxn(kind=state.txn_kind, staged_writes=tuple(StagedWriteForPredicate(...) for sw in state.staged_writes), session_id=state.session_id)` — map the dispatcher-owned `StagedWrite` shape to the predicate-module shape. Call `result = compound_commit_predicate(txn, V0_1_COMPOUND_TXN_REGISTRY, cedar)`. On `result.admit == False`: route through `_abort_with_release` with `failure_code=result.failure_code` (one of `F-VAULT-24`, `F-VAULT-25`, `F-VAULT-26`, `F-CEDAR-COMPOUND-DENIED.unknown_kind`, `F-CEDAR-COMPOUND-DENIED.predicate_denied`), `phase="commit_phase_3_predicate"`, `evidence=result.evidence`.
6. **Persist each StagedWrite (phase 4) in `write_order_at_persist` order per §4.10.5.** For each `sw`:
   - `overwrite` → `tmp → fsync → rename(2)`.
   - `write-if-absent` → `renameat2(RENAME_NOREPLACE)` (Linux) / `renamex_np(RENAME_EXCL)` (macOS).
   - `append-cas` → re-read current file head, re-hash with `APPEND_CAS_HASH_CHUNK_BYTES` streaming, compare to `expected_current_file_hash` derived from `sw.pre_image_hash`, append + fsync + rename.
   On any OS error at persist #N where N > 1: invoke the undo chain (§4.10.7.5). Undo success → `_abort_with_release(failure_code="F-VAULT-24.second_persist_failed_undo_succeeded", phase="commit_phase_4_persist", ...)`. Undo failure → `_abort_with_release(failure_code="F-VAULT-27.compound_commit_undo_failed", phase="commit_phase_4_undo", ...)` + write a HIGH-severity forensic record to admin-risk ledger (lock released BEFORE this append per §4.10.7.4).
7. **Release `vault/.write.lock` (step 5 per §4.10.7.3).** `flock(LOCK_UN)`.
8. **Pop state from staging dict under `.compound_txn.lock`.**
9. **Return `CommitResult(status="committed", txn_token=state.txn_token, persisted_hashes=tuple((sw.intent_tag, sw.data_sha3_512) for sw in state.staged_writes))`.**

### `abort_compound_txn(txn_token, reason, payload)` — caller-explicit

1. **Load state.** `state = staging_dict.get(txn_token)`; if None → `AbortResult(failure_code="F-VAULT-28.unknown_txn_token", phase="caller_explicit", …)`. Nothing to release.
2. **Validate payload against Section 4 §4.12 PRE-append predicate.** If predicate rejects with `F-LOGICIAN-ABORT-PAYLOAD-LEAK` or `F-LOGICIAN-TOKEN-LEAK` → surface the rejection to the caller; the abort itself still proceeds (the caller asked to abort and has an actively-held lock; we must release it regardless of payload validity).
3. **Route through `_abort_with_release`.** `failure_code=f"F-VAULT-ABORT-EXPLICIT.{reason}"`, `phase="caller_explicit"`, `evidence={"reason": reason, "payload_accepted": payload_predicate_ok}`.

### `_abort_with_release(txn_token, failure_code, phase, evidence) -> AbortResult` — the lock-release helper

Invariant: every abort path in the module calls this helper. §4.10.7.4 5-step sequence:

1. Look up the `CompoundTxnState` in staging dict; capture whether `.write.lock` is held.
2. Pop the staging-dict entry under `.compound_txn.lock`.
3. If `.write.lock` was held for this txn → `flock(LOCK_UN)` on `vault/.write.lock`.
4. Emit admin-risk ledger append via SIMPLE `vault_write(intent="admin-risk-append", path=<ledger path>, data=<redacted payload>, session_id=state.session_id, txn_token=None)`. The ledger append acquires and releases its own lock independently; it never contends with the released `.write.lock`.
5. Return `AbortResult(status="aborted", txn_token=txn_token, failure_code=failure_code, phase=phase, evidence=evidence)`.

`staged_writes_discarded_at` timestamp in the abort record distinguishes pre-lock-release vs post-lock-release ledger append ordering for §7.18.10 verification.

### `scan_recent_index_amendment_audit_stamps(scan_lines)` — §5.4 boot-gate helper

1. Read admin-risk ledger at its canonical path (§2.10) as line-indexed JSONL.
2. Filter to `ledger_kind == "index_amendment"`; take the last `scan_lines` matches (bounded by `COMPOUND_RECOVERY_SCAN_LINES=16`).
3. Compute `current_index_hash = sha3_512_hex(canonical_bytes(read_index_file_bytes()))`.
4. Compare each audit stamp's `post_index_hash` field to `current_index_hash`; collect matches.
5. Return `RecoveryScanResult(current_index_hash, matching_audit_stamps=tuple(...), scanned_line_count=N, orphaned=(len(matches)==0))`.

This helper is READ-ONLY. It never writes, never modifies the ledger, never mutates any in-memory state. §5.4 boot-gate owns the decision to boot-fail or accept.

## Failure codes

Emitted by this module (closed set — new codes require spec-card + blueprint §6 amendment):

**From `vault_write` dispatcher-entry hard-gate (§4.10.6):**
- **`F-VAULT-28.simple_intent_with_txn_token`** — SIMPLE intent arrived with a non-None `txn_token`.
- **`F-VAULT-28.compound_intent_without_txn_token`** — COMPOUND intent arrived without a `txn_token`.
- **`F-VAULT-28.unknown_txn_token`** — `txn_token` not in staging dict.
- **`F-VAULT-28.unknown_txn_kind`** — `kind` not in `V0_1_COMPOUND_TXN_REGISTRY` at begin.

**From staging (§4.10.7.2):**
- **`F-VAULT-24.compound_txn_cap_exceeded`** — `MAX_STAGED_WRITES_PER_TXN` or `MAX_STAGED_BYTES_PER_TXN` breached.
- **`F-VAULT-PATH-ALLOWLIST-DENY`** — path not in §4.10.5 allowlist for the bound kind.
- **`F-VAULT-26.compound_txn_session_mismatch`** — per-write session_id ≠ CompoundTxnState.session_id.

**From commit (§4.10.7.3):**
- **`F-VAULT-COMPOUND-INTEGRITY.state_not_frozen`** / **`.staged_write_not_frozen`** / **`.data_hash_mismatch`** — §2.10 runtime integrity anomalies at phase 1.
- **`F-VAULT-COMPOUND-OVERSIZE.pre_commit_bytes_overflow`** — phase 2 overflow of MAX_COMPOUND_TXN_BYTES.
- **`F-VAULT-24`** / **`F-VAULT-25`** / **`F-VAULT-26`** — forwarded from §4.11 predicate (phase 3).
- **`F-CEDAR-COMPOUND-DENIED.unknown_kind`** / **`F-CEDAR-COMPOUND-DENIED.predicate_denied`** — forwarded from §4.11 predicate (phase 3, Cedar surface).
- **`F-VAULT-24.second_persist_failed_undo_succeeded`** — persist #N>1 failed; undo restored; no net on-disk change (§4.10.7.5).
- **`F-VAULT-27.compound_commit_undo_failed`** — persist + undo both failed; storage substrate in serious trouble; operator intervention required (§4.10.7.5).

**From abort (§4.10.7.4 + caller-explicit):**
- **`F-VAULT-ABORT-EXPLICIT.<reason>`** — caller-explicit `abort_compound_txn` with caller-supplied reason string. Reason is echoed into the failure code for post-hoc correlation.

**From TTL sweep (§4.10.7.8):**
- **`F-VAULT-COMPOUND-TTL-EXPIRED`** — a staged txn exceeded `COMPOUND_TXN_TTL_SECONDS`; force-aborted at the next `begin_compound_txn`.

**Forwarded from Section 4 §4.12 PRE-append predicate (not emitted by this module, but this module's ledger appends can be rejected with these):**
- `F-LOGICIAN-TOKEN-LEAK` — raw-token-shaped string found in a ledger record payload.
- `F-LOGICIAN-ABORT-PAYLOAD-LEAK` — abort payload contained raw bytes or other forbidden shape.

Not emitted (fail-out-of-scope): `F-INDEX-STALE.*` (those fire at §5.4 boot-gate, consuming this module's `scan_recent_index_amendment_audit_stamps` helper but owned by Section 5).

## Test surface

All 13 §7.18 vectors are authoritative. Each vector is a named test in `pipeline/vault/tests/test_compound_txn.py`:

### §7.18 vectors
- **`test_7_18_1_concurrent_two_session_interposition`** — spawn two sessions; assert exactly one commits, the other fails with the expected SIMPLE-path failure code (`F-VAULT-WRITE-EXISTS` on `write-if-absent` or `F-VAULT-CAS-HEAD-MISMATCH` on `append-cas`); assert zero half-amended state.
- **`test_7_18_2_stage_time_hash_pin_integrity`** — stage with P1; attempt `object.__setattr__` to P2; assert `FrozenInstanceError`; commit; assert persist is P1 byte-identical.
- **`test_7_18_3_frozen_dataclass_attempted_mutation`** — staged_writes tuple has no append; `CompoundTxnState.__setattr__` raises `FrozenInstanceError`; document `object.__setattr__` OUT-OF-MODEL bypass.
- **`test_7_18_4_session_mismatch_rejection_at_vault_write`** — stage with S2 under a txn bound to S1 → `F-VAULT-26.compound_txn_session_mismatch`; no staging; no on-disk mutation.
- **`test_7_18_5_crash_between_persists_simulated`** — mock persist primitive to raise `OSError(EIO)` after persist #1; assert (a) second persist error propagates, (b) `pre_commit_bytes` undo restores, (c) `F-VAULT-24.second_persist_failed_undo_succeeded`, (d) lock released before admin-risk-append per §4.10.7.4.
- **`test_7_18_6_unknown_kind_denial`** — `begin_compound_txn(kind="nonexistent", ...)` → `F-VAULT-28.unknown_txn_kind`; no token minted; no lock acquired.
- **`test_7_18_7a_simple_intent_with_txn_token`** — SIMPLE intent with fake token → `F-VAULT-28.simple_intent_with_txn_token`.
- **`test_7_18_7b_compound_intent_without_txn_token`** — COMPOUND intent without token → `F-VAULT-28.compound_intent_without_txn_token`.
- **`test_7_18_8_abort_payload_deep_inspect_leak`** — `abort_compound_txn(payload={"meta":{"raw_bytes":b"…"}})` → Section 4 §4.12 rejects with `F-LOGICIAN-ABORT-PAYLOAD-LEAK`; ledger append refused; abort itself still completes (lock released).
- **`test_7_18_9_pre_commit_bytes_oversize`** — target file at 65 MiB (> MAX_COMPOUND_TXN_BYTES=64 MiB) → `F-VAULT-COMPOUND-OVERSIZE.pre_commit_bytes_overflow` at §4.10.7.3 step 2; lock released before admin-risk-append; no on-disk mutation.
- **`test_7_18_10_lock_release_on_abort_order`** — instrument the lock primitive; assert sequence `[staging_dict_pop, LOCK_UN, admin_risk_append_open(LOCK_EX), admin_risk_append_close(LOCK_UN), return]` for every abort path (overflow, predicate-denial, caller-explicit).
- **`test_7_18_11_token_redaction_in_logs_and_abort_payloads`** — mint a token; log through dispatcher logger; assert rendered output contains `<redacted:token>`, not raw token. Attempt admin-risk append with `{"txn_token": "<raw>"}`; assert `F-LOGICIAN-TOKEN-LEAK`.
- **`test_7_18_12_simple_v7_regression_under_v7_1_lock_scope`** — every v7 §7.17.5 regression vector (23 vectors) produces byte-identical on-disk state under v7.1; SIMPLE call on a COMPOUND-allowlisted path acquires `.write.lock` exactly as a SIMPLE call on a non-COMPOUND path.
- **`test_7_18_13_ttl_sweep_correctness`** — open txn at T0; advance monotonic clock past `COMPOUND_TXN_TTL_SECONDS + 1`; open second txn; assert (a) first txn force-aborted during begin-sweep, (b) first txn's lock released per §4.10.7.4, (c) `F-VAULT-COMPOUND-TTL-EXPIRED` in ledger, (d) `commit_compound_txn(first_token)` after sweep → `F-VAULT-28.unknown_txn_token`.

### Property tests (above and beyond §7.18)
- `test_prop_every_abort_path_routes_through_abort_helper` — AST-walk the module; assert exactly ONE site calls `flock(LOCK_UN)` on `vault/.write.lock` outside `_abort_with_release` (the commit-success path at §4.10.7.3 step 5), and exactly ONE site calls it inside `_abort_with_release`. Three or more sites → finding.
- `test_prop_staged_writes_is_always_frozen_tuple` — for every `CompoundTxnState` observed during a 1000-txn fuzz run, `isinstance(state.staged_writes, tuple)` and `dataclasses.is_dataclass(sw) and sw.__dataclass_params__.frozen` for every sw.
- `test_prop_staging_view_is_mapping_proxy` — `isinstance(staging_view(), types.MappingProxyType)`; attempted `staging_view()["k"] = v` raises `TypeError`.
- `test_prop_token_shape_matches_secrets_token_urlsafe_32` — 1000 tokens minted; every token matches `re.fullmatch(TXN_TOKEN_REDACTION_PATTERN, token)`.
- `test_prop_hash_at_stage_time_is_immediate` — instrument `sha3_512_hex`; assert it is called exactly ONCE per `vault_write` staging call, in the same call frame; never lazy.

### Adversarial tests
- `test_adv_reused_txn_token_after_commit_is_unknown` — after `commit_compound_txn(T)` returns, `vault_write(txn_token=T, ...)` → `F-VAULT-28.unknown_txn_token`.
- `test_adv_reused_txn_token_after_abort_is_unknown` — same, after `abort_compound_txn`.
- `test_adv_concurrent_commit_and_abort_same_token` — thread A calls `commit_compound_txn(T)`, thread B calls `abort_compound_txn(T)`; assert exactly one wins; the other returns `F-VAULT-28.unknown_txn_token`. No deadlock, no double-release.
- `test_adv_tamper_with_staged_write_data_field_via_object_setattr` — documents the OUT-OF-MODEL bypass; test asserts `object.__setattr__` does bypass the freeze (trusted-operator envelope); `test_7_18_2` ensures the re-hash check at phase 1 catches this when it happens via the supported mutation surface.
- `test_adv_kind_string_with_leading_whitespace` — `begin_compound_txn(kind=" index_amendment", ...)` → `F-VAULT-28.unknown_txn_kind` (kind matching is exact, not trimmed). Documents that caller is responsible for canonicalising `kind` before passing.
- `test_adv_session_id_empty_string_at_begin` — `session_id=""` → Cedar session lookup returns None → `F-VAULT-26`, lock released.
- `test_adv_session_id_whitespace_only_at_begin` — same; no trimming in Cedar lookup.
- `test_adv_begin_during_held_lock_from_simple_path_blocks` — a SIMPLE `vault_write` holds `.write.lock`; concurrent `begin_compound_txn` blocks; assert second call does NOT steal the lock, does NOT throw, simply waits.
- `test_adv_ttl_sweep_during_commit_in_progress_does_not_abort_active_txn` — begin T1 at T0; begin T2 at T0 + TTL - 1s; advance clock to T0 + TTL + 1s; `commit_compound_txn(T2)` in progress when another begin fires the sweep; assert T2 completes cleanly (its `created_at_monotonic_ns` is within window from T2's own begin perspective, not from T1's).

### Corpus tests
- `tests/corpus/vault_dispatcher/v1/pass/` — fixture txn sequences that commit successfully.
- `tests/corpus/vault_dispatcher/v1/fail/` — fixture txn sequences paired with expected `(failure_code, phase)` manifests; covers every failure code in the "Failure codes" closed set above at least once.

### Cross-module guards
- `test_imports_v0_1_registry_from_logician_not_shadowed` — AST-walk this module; assert it imports `V0_1_COMPOUND_TXN_REGISTRY` from `pipeline.logician.compound_commit`; assert no module-local copy is defined. (Enforces Design Decision #6.)
- `test_ast_lint_surface_passes_on_this_module` — run ARCH-04 `DEFAULT_RULES` (R1 LOGICIAN_IMPORT_BAN, R3 LOGICIAN_OPEN_BAN) on `pipeline/vault/dispatcher.py`; assert zero violations. (R1/R3 target `pipeline/logician/**` so this module is not under those rules, but the test verifies via inversion that this module does not leak into Logician territory.)
- `test_no_print_of_txn_token` — AST-walk this module; assert no `print(…)` / `sys.stdout.write(…)` / `sys.stderr.write(…)` call has `txn_token` or a name bound to it in its argument expression.

## Futureproofing commitments

- Public API surface declared in `__all__`; internal helpers (`_abort_with_release`, `_ttl_expire`, `_staging_dict_pop`, `_staging_dict_swap`, `_dispatcher_logger`, `TokenRedactionFilter`) stay module-private.
- Schema version: `AuditStampRecord` in the admin-risk ledger carries `schema_version: "v1"` per §4.2 of engineering_process_v0.1.md. Growth to v2 uses `versioned_load` with explicit migrations.
- `CompoundTxnKind` enumeration is imported from the predicate module — any kind growth at v0.2+ happens there; this dispatcher picks up the new kind automatically without code change.
- Constant values imported from `pipeline.vault.constants`; bump is a single-file edit with a lesson row.
- Crypto-agility: SHA-3-512 canonical-bytes hashing is the v0.1 default; per §4.4 any future crypto-agility refactor wraps the hash in a `HashDigest(algorithm="sha3-512", hex=...)` type — that refactor lands in `pipeline.vault.constants` / `pipeline.crypto.types`; this module only touches the import.
- `BLUEPRINT_DEPS` populated at LOCK:
  ```python
  BLUEPRINT_DEPS = {
      "section_02_vault_topology.md": {
          "sections_implemented": [
              "§2.10", "§3.5", "§4.10.5", "§4.10.6", "§4.10.7.1-9",
              "§7.18.1-13", "§8"
          ],
          "hash_at_lock": "<16-char-prefix>",
          "hash_source_version": "v7.1",
      },
      "section_04_logician.md": {
          "sections_implemented": ["§4.11", "§4.12"],
          "hash_at_lock": "<16-char-prefix>",
          "hash_source_version": "v2.1",
      },
      "section_05_pipeline.md": {
          "sections_implemented": ["§5.4 boot-gate helper"],
          "hash_at_lock": "<16-char-prefix>",
          "hash_source_version": "v6",
      },
  }
  ```
  Drift-guard test `test_blueprint_deps_hashes_match_live_blueprints` fails when any parent blueprint is edited without bumping this pin.
- Regression discipline: every §7.18 vector preserved forever; future dispatcher changes are ADDITIVE (new vectors row-append; §7.18.1-13 must keep passing).
- Extensibility: new `CompoundTxnKind` requires (a) row-append to `V0_1_COMPOUND_TXN_REGISTRY` (handled in companion card), (b) row-append to §4.10.5 path allowlist, (c) row-append §7.18 vectors (happy path + at least one failure path for the new kind).

## Done definition

1. `pipeline/vault/dispatcher.py` implemented with the public API above. Property tests green (abort-helper unique-site AST check, staged_writes frozen-tuple check, staging_view MappingProxyType check, token shape check, hash-at-stage-time check).
2. All 13 §7.18 vectors covered with named tests; every vector red-before-fix, green-after.
3. All 9 adversarial tests green; each exercises a documented threat; none passes vacuously.
4. Corpus fail manifests cover every failure code in the "Failure codes" closed set above at least once.
5. Cross-module guards green: no shadow registry; AST-lint clean; no `print` of `txn_token`.
6. Coverage on `pipeline/vault/dispatcher.py` ≥ 95% (branch coverage — every abort path short-circuit reached).
7. ARCH-04 AST-lint surface passes on the new module: no LLM-client import, no `open()` under a `vault_shared/` or `orgs/` path (the dispatcher's file I/O goes through the existing vault primitives, not raw `open`).
8. `BLUEPRINT_DEPS` populated with live 16-char SHA3-512 prefixes of §2 v7.1 + §4 v2.1 + §5 v6; drift-guard test green.
9. Companion card `pipeline/engineering/spec_cards/compound_commit.md` LOCKs in the same round (same Committee dispatch). The dispatcher depends on the predicate's public API; splitting the commits would leave one broken half on disk.
10. Code Thesis Committee dispatch: 5 cross-family reviewers per `router.yaml` `code_*` rows; all-pass; retry cap 1. Reviewer instructions explicitly name the caller-callee pair so reviewers load both cards into context.
11. `pipeline/validation/vault_dispatcher_compound_txn_r1_<date>/` audit-trail folder created with Committee verdicts + closure narrative.
12. `pipeline/engineering/lock_history.v1.jsonl` telemetry line appended: `{"card":"vault_dispatcher_commit_compound_txn","round":"vault_dispatcher_compound_txn_r1","shipped":["begin","vault_write_staging","commit","abort","ttl_sweep","boot_gate_helper","staging_view"],"failure_codes":["F-VAULT-24","F-VAULT-25","F-VAULT-26","F-VAULT-27","F-VAULT-28","F-VAULT-COMPOUND-INTEGRITY.*","F-VAULT-COMPOUND-OVERSIZE.*","F-VAULT-COMPOUND-TTL-EXPIRED","F-VAULT-ABORT-EXPLICIT.*","F-VAULT-PATH-ALLOWLIST-DENY","F-CEDAR-COMPOUND-DENIED.*"]}`.
13. `daily_logs/2026-04-20.md` (or the LOCK-day log) updated with: card filed, Committee dispatch, LOCK commit hash, paired companion-card LOCK.
14. Engineering lesson `E-NNN` added: "Compound-transaction dispatcher and predicate modules must LOCK in the same Committee round. The caller-side depends on the predicate-side `__all__` surface; splitting the commits leaves a broken half on disk. Pre-check: any spec card whose description cites 'calls <module>.<function>' must ship its callee card in the same round or justify the split in the card front-matter."
15. Downstream unblocks: §5.4 pipeline boot-gate spec card can now pin its compound-recovery scan invocation target (`scan_recent_index_amendment_audit_stamps`); §0.5 Index row for `vault.dispatcher.compound_txn_dispatcher` can be filed as a PENDING_PARENT_BACKFILL → STABLE flip with the LOCK.
16. Next staged (per CLAUDE.md proactive pre-staging): (a) `pipeline/engineering/spec_cards/section_05_boot_gate_compound_recovery.md` — the §5.4 consumer of this module's recovery helper, derivable from blueprint without operator input, OR (b) `pipeline/blueprint/v0.1/section_00_5_v6_cedar_activation_amendment.md` — the §0.5 row-flip amendment that lands with this LOCK (flipping row 103 from PENDING_PARENT_BACKFILL → STABLE).

---

*Spec card v1 — 2026-04-20 — authored under operator delegation ("bang out that writing layer" + "address everything in the discussion to your best understanding and ability"); paired with `pipeline/engineering/spec_cards/compound_commit.md` for same-round Committee dispatch; ready for Midas once blueprint hash prefixes pinned at pre-LOCK preflight.*
