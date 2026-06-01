# Spec card — pipeline.loop.rate_limiter (Round 7: §4.8 v2 TokenBucket CAS-reserve)

**STATUS:** PRE-STAGED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal sections: §4.8 v2 reserve algorithm (line 564), §3.2.5 RateLimiterState v2 lease fields (line 346), §8 constants (`RATE_LIMIT_JITTER_RANGE_MS=(0,300)`, `RATE_LIMIT_LEASE_TTL_SEC=30`, `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS=(50,200,800)`), §6 F-PIPE-06 `rate_limit_exhausted`
- Closure rows: B-v1-02 (CAS lock), B-v1-04 (exponential back-off + jitter), B-v1-10 (30s lease TTL auto-release), A-v1-09 (concurrent-reserve test anchor — `test_rate_limiter_concurrent_reserve_no_overconsumption`)

**Blueprint hash-at-card:**
- `section_05_pipeline.md`: `34ef007f3ab6d59d`

**Spec-card version:** v1 (pre-staged 2026-04-21 at §5 Round 6 SELF-LOCK)
**Round:** §5 Round 7 — rate_limiter (`reserve` + `can_reserve` + `release` on vault-CAS-locked `RateLimiterState`)
**Depends on:** Round 1 (`RateLimiterState` v2 dataclass + `TokenBucketProtocol` declaration + `RATE_LIMIT_JITTER_RANGE_MS` / `RATE_LIMIT_LEASE_TTL_SEC` / `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS` constants + `F_PIPE_06`); Round 2 (`checkpoint_atomic` CAS-retry idiom template — Round 7 reuses the three-tier back-off schedule but with its own jitter addition). No §4 Logician consumption — pure §5 orchestrator primitive.

---

## Summary

Ship `pipeline/loop/rate_limiter.py` — vault-CAS-locked token-bucket reservoir per §4.8 v2. Public surface:

1. `TokenBucket` (concrete implementation of Round 1's `TokenBucketProtocol`).
2. `reserve(endpoint, estimated_tokens)` — acquires lease, refills by wall-clock delta, atomically CAS-writes `RateLimiterState` back to vault. Returns `Reserved(tokens=n)` on success, `InsufficientTokens(available=n, requested=k)` on under-budget. Raises `F_PIPE_06` on retry exhaustion.
3. `can_reserve(endpoint, estimated_tokens)` — read-only inspector (§4.1 step 2 cascade-selection probe). No vault mutation.
4. `release(endpoint)` — CAS-writes the lease fields back to `None` early (optional; expired leases auto-release on the next `reserve` per B-v1-10).

Per §4.8 v2 algorithm (blueprint lines 568–618): `vault_read` current bucket bytes + hash → parse → auto-release expired lease → abort-if-someone-else-holds → refill wall-clock delta → check capacity → reserve tokens + stamp lease → `vault_write` with `expected_current_file_hash` → on CAS mismatch sleep `_backoff_with_jitter(attempt)` + retry → on `CHECKPOINT_CAS_RETRY_MAX` exhaustion raise `F_PIPE_06`.

Public API:

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class Reserved:
    endpoint: str
    tokens: int
    lease_holder_id: str
    lease_expires_at_iso: str
    committed_state_hash: str

@dataclass(frozen=True, kw_only=True, slots=True)
class InsufficientTokens:
    endpoint: str
    available: float
    requested: int

@dataclass(kw_only=True, slots=True)
class TokenBucket:
    capacity: int
    tokens: float
    refill_rate_per_sec: float

def reserve(
    *,
    endpoint: str,
    estimated_tokens: int,
    process_id: str,
    vault_read: VaultReadCallable,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
    randint: RandIntFn,                     # Protocol — Round 7 injected RNG seam
    max_attempts: int = 3,                  # INLINE LITERAL per §4.8 v2 — rebind-resistant
    lease_ttl_sec: int = 30,                # INLINE LITERAL per §8 pin
) -> Reserved | InsufficientTokens: ...

def can_reserve(
    *,
    endpoint: str,
    estimated_tokens: int,
    vault_read: VaultReadCallable,
    clock: ClockProtocol,
) -> bool: ...

def release(
    *,
    endpoint: str,
    process_id: str,
    vault_read: VaultReadCallable,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
    randint: RandIntFn,
    max_attempts: int = 3,
) -> str: ...  # returns new committed_state_hash
```

**Protocols (new — E-017 eighth firing):**

- `RandIntFn(Protocol, runtime_checkable)` — `__call__(a: int, b: int) -> int`. Injection seam for `random.randint`; lets tests fix jitter deterministically without `monkeypatch.setattr(random, ...)`.
- Reuses Round 2's `ClockProtocol` + `SleepCallable` + `VaultReadCallable` + `VaultWriteCallable` — no new clock/vault Protocols.

**Back-off formula (inline-literal, §4.8 blueprint lines 615–618):**

```python
def _backoff_with_jitter_ms(attempt: int, randint: RandIntFn) -> int:
    base_ms = (50, 200, 800)[min(attempt, 2)]   # §8 CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS mirror
    jitter_ms = randint(0, 300)                 # §8 RATE_LIMIT_JITTER_RANGE_MS pin
    return base_ms + jitter_ms
```

## §5 v6 compliance decisions (must confirm at ORIENT)

1. **Max-attempts constant.** §4.8 algorithm (line 570) references `CHECKPOINT_CAS_RETRY_MAX`. Round 1 config.py defines `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS` as a 3-tuple but does NOT define `CHECKPOINT_CAS_RETRY_MAX` as a standalone int. **Confirm:** inline-literal `max_attempts: int = 3` (kwarg default, rebind-resistant) OR introduce a `CHECKPOINT_CAS_RETRY_MAX: Final[int] = 3` constant in config.py? Precedent favors inline-literal (Round 2 `CHECKPOINT_TOTAL_TIMEOUT_SEC` is a §8 pin but the schedule tuple is indexed inline).

2. **Lease auto-release ordering.** §4.8 algorithm clears expired lease BEFORE checking lease-holder (line 580 → 584). Round 7 must preserve ordering to avoid self-block (a process holding an expired lease should be able to re-acquire without sleeping). **Confirm:** the auto-release check uses `_is_past(expires_at_iso)` against `clock.now_ms()` converted to ISO-8601 — or against a direct epoch-ms comparison? Prefer the latter (cheaper + no tz ambiguity); ISO stays on the stored state for human-readable vault audit.

3. **Refill formula.** §4.8 v2 line 590 shows `_refill(state)` as opaque. Token-bucket refill is standard: `tokens = min(capacity, tokens + (elapsed_sec × refill_rate_per_sec))` per bucket. `last_refill_iso` on `RateLimiterState` is the wall-clock anchor. **Confirm:** refill uses `clock.now_ms() - _parse_iso(last_refill_iso)` delta; `last_refill_iso` gets stamped after refill + reserve (so the next caller's delta is from this reserve moment, not from the previous refill).

4. **Canonical bytes for vault-write.** §4.8 line 602 calls `state.canonical()`. Round 1's `RateLimiterState` is a dataclass; Round 7 must define a canonicalizer (sha256-stable key ordering). Follow Round 2 + Round 6 template: `json.dumps(asdict(state), sort_keys=True, separators=(",",":"), default=_rate_limiter_default)`. `TokenBucket` is a mutable dataclass so `asdict` handles it; `RateLimiterState.buckets` is a `dict[str, TokenBucketProtocol]` — all protocol-shaped, Round 7's `TokenBucket` is the only concrete implementation → `asdict` sees `{capacity, tokens, refill_rate_per_sec}` and produces stable JSON.

5. **Vault-write intent.** §4.8 line 603 uses `intent="state-success"` as an explicit interim pattern until a dedicated `rate-limiter-snapshot` intent lands (OQ-2 in blueprint). Round 7 matches: `intent="state-success"`, `session_id="system"`, `slug="rate_limiter"`, `write_mode="overwrite"`, `expected_current_file_hash=current_hash`. Document the interim-intent stance in the module docstring.

6. **`F_PIPE_06` construction.** §6 F-PIPE-06 is `rate_limit_exhausted` with state-failure. Round 7 raises `F_PIPE_06(trigger="cas_retry_exhausted:{endpoint}:{attempts}")` after the last attempt fails. `F_PIPE_06` lives in `pipeline.loop.errors` already (Round 1); no new failure code needed.

## Out-of-scope for Round 7

- **Cascade selection** (§4.9) — Round 8+ concern. Round 7 exposes `can_reserve` as a read-only inspector; `select_cascade_level` composes that in a higher-level module.
- **RateLimiterState bootstrapping** — initial bucket-config load from `router.yaml` lives in Round 3's `start_run` or a dedicated bootstrapper. Round 7 assumes the vault path already has a seeded `RateLimiterState.json`.
- **TokenBucket refill-rate policy** — per-endpoint capacity + refill rates come from `router.yaml` at boot; Round 7 only consumes the current state.
- **Lease handoff / explicit transfer** — not in §4.8 v2. Round 7's `release` is self-release only.
- **Cross-endpoint fairness** — outside §4.8 scope; §4.9 cascade handles fairness across families.

## Test surface (`tests/loop/test_rate_limiter.py`)

**Happy paths (1 class, ~4 tests):**
- `reserve` succeeds first-try → `Reserved(tokens=N, lease_holder_id=PID, lease_expires_at_iso=...)` with correct `committed_state_hash`; vault_write called exactly once with `expected_current_file_hash` == read hash.
- `reserve` with `estimated_tokens > bucket.capacity` immediately after refill → `InsufficientTokens(available=<refilled>, requested=N)`; no vault_write.
- `can_reserve` returns True when bucket has capacity; False when under-budget. No vault_write ever.
- `release` clears `lease_holder_id` + `lease_expires_at_iso` to None; CAS writes once.

**Lease management (1 class, ~3 tests):**
- B-v1-10 expired lease auto-release: pre-state has `lease_holder_id="OTHER"` + `expires_at_iso` 5 minutes in past → current `reserve(process_id="MINE")` succeeds (no sleep).
- Someone-else-holds active lease: pre-state has `lease_holder_id="OTHER"` + `expires_at_iso` 20s in future → `reserve` sleeps, retries up to `max_attempts`, raises `F_PIPE_06` if never freed.
- Self re-acquire on expired lease: pre-state has `lease_holder_id=PID` + expired → re-reserve without sleep (no blocking on our own stale lease).

**CAS retry (1 class, ~3 tests):**
- CAS mismatch on attempt 1 → sleep(`_backoff[0] + jitter`) → retry → succeed on attempt 2. Vault_read called 2×.
- CAS mismatch on all 3 attempts → raise `F_PIPE_06(trigger="cas_retry_exhausted:{endpoint}:3")`.
- Back-off schedule pin: with `randint` stubbed to always return 0, sleep intervals are exactly `(50, 200, 800)` ms → proves §8 schedule constant is honored inline.

**Refill (1 class, ~2 tests):**
- 1 second wall-clock elapsed with `refill_rate_per_sec=10` → tokens increase by 10, capped at `capacity`.
- `last_refill_iso` gets stamped to the post-reserve clock reading (not the pre-read timestamp).

**Factory / Protocol contract (1 class, ~2 tests):**
- `RandIntFn` is `runtime_checkable`; a function `(a,b) -> int` satisfies the Protocol.
- `TokenBucket` satisfies `TokenBucketProtocol` (round-trip `isinstance` check).

## Adversarial surface (`tests/loop/test_adv_rate_limiter.py`)

- **`RATE_LIMIT_JITTER_RANGE_MS` rebind-resistance.** Monkeypatch `pipeline.loop.config.RATE_LIMIT_JITTER_RANGE_MS = (9999, 9999)`; Round 7's `_backoff_with_jitter_ms` still uses `(0, 300)` inline-literal. E-025 discipline (no hard-pin version tests; range-check).
- **`RATE_LIMIT_LEASE_TTL_SEC` rebind-resistance.** Same — `lease_ttl_sec: int = 30` kwarg default is inline-literal.
- **`CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS` rebind-resistance.** Monkeypatch the module-level tuple; `_backoff_with_jitter_ms` still indexes into `(50, 200, 800)` inline.
- **Non-monotonic clock.** `clock.now_ms()` returns a *decreasing* value between read and refill-delta computation → Round 7 must `max(delta_ms, 0)` clamp (no negative refill).
- **Half-present lease (data corruption).** Pre-state has `lease_holder_id="X"` + `lease_expires_at_iso=None` → `RateLimiterState.__post_init__` raises `ValueError`; Round 7 must surface the error *without* wrapping (programmer/data contract violation, not `F_PIPE_06`).
- **Zero-capacity bucket.** `TokenBucket.capacity=0` → every `reserve(estimated_tokens=1)` returns `InsufficientTokens(available=0, requested=1)` — no infinite-retry loop.
- **Zero-refill-rate bucket.** `refill_rate_per_sec=0.0` → refill is a no-op; bucket never recovers after exhaustion (expected per §4.8 capacity-unchanged guarantee).
- **CAS mismatch via hash-shift between read + write.** First `vault_read` returns hash `A`; between read + write another process bumps hash to `B`; Round 7's write with `expected_current_file_hash=A` raises `VaultCASHeadMismatch` → caught, retry, re-read, succeed on attempt 2.
- **`F_PIPE_06` taxonomy pin.** Raised exception is subclass of `PipelineFailure`; `CODE == "F-PIPE-06"`; `trigger` string matches `f"cas_retry_exhausted:{endpoint}:{attempts}"`.
- **`release` idempotency.** Calling `release` when no lease is held → writes an unchanged state, returns the new hash (no-op).
- **`can_reserve` purity.** No vault_write + no sleep + no randint calls; only one vault_read + (optional) clock.now_ms.
- **Concurrent-reserve regression pin** (A-v1-09). Two cooperating coroutines (simulated via deterministic clock + shared fake vault) each try to reserve when total capacity < sum of requests → exactly one succeeds; the other gets `InsufficientTokens` OR `F_PIPE_06`; total consumed ≤ capacity.
- **Empty buckets dict.** `reserve(endpoint="missing")` when `state.buckets` does not contain `"missing"` → `KeyError` (programmer error, not `F_PIPE_06`) — document as contract.

## Done definition

- All new tests in `tests/loop/test_rate_limiter.py` + `tests/loop/test_adv_rate_limiter.py` green.
- Coverage ≥ 95% on `pipeline/loop/rate_limiter.py` (target 100% per Round 6 precedent).
- AST-lint R1–R7 zero violations on the new module (`lint_tree(Path('pipeline/loop/'), DEFAULT_RULES)`).
- Full suite baseline + new-test-count green (target: 4079 + ~40 new = ~4119).
- `pipeline/loop/__init__.py` re-exports Round 7 public surface.
- `pipeline/engineering/lock_history.v1.jsonl` appended with verdict=LOCKED, self-LOCK single-cycle v1.
- MEMORY.md index entry prepended; round-recap memory file written.
- Pre-stage Round 8 spec card (§4.11 three-tab delivery OR §4.9 cascade selection — operator confirms priority).

## Lines-of-code target (E-024 seventh firing — adversarial multiplier reaffirmed at 2×)

| File | Target | Target ±25% | Comment |
|------|--------|-------------|---------|
| `pipeline/loop/rate_limiter.py` | 450 | 340–560 | CAS-reserve loop + refill + release + 2 result dataclasses + 1 concrete TokenBucket + 1 Protocol (RandIntFn) + canonicalizer + back-off helper + F_PIPE_06 dispatch. Comparable complexity to Round 2 (checkpoint_atomic: 553 LOC) but with extra refill arithmetic and lease fields. |
| `tests/loop/test_rate_limiter.py` | 550 | 410–690 | ~14 tests × ~40 LOC/test with shared fixtures. |
| `tests/loop/test_adv_rate_limiter.py` | 900 | 670–1130 | ~14 adv tests × 2× multiplier (E-024 precedent — Round 6 landed 2.08×). |

## Self-LOCK eligibility

**Eligible if single-cycle pass.** Pure §5 orchestrator primitive — no network, no subprocess, no §4 Logician consumption. Dependencies (Round 1 dataclasses + Round 2 CAS idiom) all LOCKED. Follow §5 R3/R4/R5/R6 precedent: single-cycle pass + 95%+ coverage + AST-lint clean → self-LOCK with committee dispatch deferred.

## Round 8+ preview

**Round 8 candidate A** — `pipeline/loop/cascade.py` — §4.9 v2 provider-cascade level selection consulting live landed-family record (A-v1-02 closure). Composes `rate_limiter.can_reserve` from Round 7.

**Round 8 candidate B** — `pipeline/loop/tab_delivery.py` — §4.11 three-tab envelope ordering + signing (TabEnvelope from Round 1 + §2 vault primitives).

**Round 9-12** — eval-mode orchestrator (§4.15), golden-set scoring (§4.14), calibration-report (§4.16), capstone `run_pipeline.py` wiring all §5 rounds.

## Open questions (resolve at ORIENT)

1. **`CHECKPOINT_CAS_RETRY_MAX` existence.** §4.8 line 570 references it as a constant but Round 1 config.py does not define it. Is the intent for §8 to have `CHECKPOINT_CAS_RETRY_MAX: Final[int] = 3` (parallel to the `BACKOFF_SCHEDULE_MS` 3-tuple length), or does Round 7 inline-literal `max_attempts=3` as a kwarg default? Precedent: Round 2 used inline-literal `(50, 200, 800)` indexing rather than reading the §8 tuple constant. Propose inline-literal.

2. **Refill-timestamp format.** `RateLimiterState.last_refill_iso` is an ISO string. Round 7 converts `clock.now_ms()` → ISO-8601 UTC. Which format — `datetime.isoformat(timespec="milliseconds") + "Z"`? Match §2 vault's ISO convention. Verify via grep on vault-layer ISO helpers.

3. **`release` necessity.** §4.8 v2 algorithm does not show an explicit `release`; the lease is naturally released on the next caller's auto-release check when it expires. Should Round 7 expose `release` as a best-practice explicit-close primitive, or omit it to keep the surface minimal? Propose: ship it (symmetric with `reserve`, cheap to implement, tests prove idempotency).

4. **`can_reserve` refill side-effect.** §4.8 v2 `can_reserve` is read-only (no vault_write). But "can I reserve?" logically requires knowing the refilled balance — so `can_reserve` does an in-memory refill computation without persisting. Confirm: `can_reserve` returns `(refilled_in_memory_tokens >= estimated_tokens)`; does NOT stamp `last_refill_iso`. The next real `reserve` does a fresh refill from the unchanged persisted `last_refill_iso`.

5. **Concurrent-reserve test mechanism.** A-v1-09 closure demands `test_rate_limiter_concurrent_reserve_no_overconsumption` — two processes reserving concurrently with total > capacity. Round 7 uses a deterministic fake vault (shared hash counter) + two sequential reservation calls with an interleaved CAS mismatch scenario; not real threading. Confirm: deterministic simulation is acceptable (tests are fake-vault-based across all §5 rounds).
