# Spec card — pipeline.scout Round 4 (Channel A — federal APIs)

**STATUS:** SELF-LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md`
  - §4.1 Channel A full spec (lines 412–471) — implementation target
  - §2.1 `Candidate` schema (Round 1 `_types.py`) — DISCOVER row shape
  - §3.3 `fd_broker.request_fd` / `release_fd` and `nonce_registry.reserve` / `release` (Section 1 + §2 Vault primitives) — LOCKED
  - §6.2 F-SCOUT-A-01..04 failure codes (nonce lifecycle, FD lifecycle, response parse, IdentityTuple)
  - §7.1 test surface for `channel_a_federal_apis`
  - §8 `CHANNEL_A_CONNECT_TIMEOUT_S = 10`, `CHANNEL_A_READ_TIMEOUT_S = 30`, `CHANNEL_A_RETRY_COUNT = 3` (already in Round 1 `_constants.py`)
  - §9 intent strings for Channel A response caching + entity-registration snapshots
- Section 1 consumed surface: `nonce_registry.reserve/release`, `hmac_sha3_512`, `record_degradation` — LOCKED.
- Section 2 consumed surface: `fd_broker.request_fd/release_fd` (Round Q) + `vault_write` (Round P) — LOCKED.

**Blueprint hash-at-card:** `0a82d955f95b0fca` (sha3_512(section_03_scout.md)[:16]) — identical to Rounds 1–3.

**Spec-card version:** v1 (pre-staged)
**Round:** Scout R4 of 11. Consumes Round 1 schemas + constants only. Does NOT consume Rounds 2 or 3 at runtime; Round 2 only consumes the channel-A per-endpoint states Round 4 reports.

---

## Summary

Land `pipeline/scout/channel_a_federal_apis.py` — the Channel A DISCOVER adapter. **First Scout round with network I/O.** Three parallel endpoints (grants.gov, sam.gov, usaspending.gov); each independently reports OK / DEGRADED / FAILED. `backbone_failed = True` iff all three FAILED.

Public surface:

```python
def discover_channel_a(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    vault_writer: VaultWriter,
    http_client: HTTPClient,
    clock: ClockFn = _default_clock,
) -> ChannelADiscoverResult: ...
```

Where `ChannelADiscoverResult` is a frozen kw_only dataclass: `candidates: tuple[Candidate, ...]`, `per_endpoint_state: Mapping[str, str]` (keys `grants.gov` / `sam.gov` / `usaspending.gov`; values ∈ `{OK, DEGRADED, FAILED}`), `channel_state: str`, `backbone_failed: bool`, `degradation_events: tuple[DegradationEvent, ...]`.

Only the grants.gov search2 endpoint produces `Candidate` rows. sam.gov writes a cached entity-registration snapshot (for Logician PRE-gate); usaspending.gov writes a cached awards-history snapshot (for Pipeline context). Both snapshot writes go via the injected `VaultWriter`.

## Design decisions (operator-disposed 2026-04-20, reversible)

1. **HTTPClient Protocol seam.** Pattern E-017. `HTTPClient.request(method, url, *, headers, body, connect_timeout_s, read_timeout_s) -> HTTPResponse` returning `HTTPResponse(status, headers, body_bytes, body_sha3_512_hex)`. Production binding wraps `urllib3` (stdlib-compatible; `requests` allowed if already in `pyproject.toml` — check). Tests inject a scripted client that returns a queue of prepared responses + can raise `TimeoutError`, `ConnectionResetError`, etc.
2. **NonceRegistry + FDBroker are separate Protocols.** Do not fuse into a single "network primitives" protocol — they come from different sections (§1 vs §2) and have separate failure codes.
3. **One try/finally ladder per request.** Nonce reserved BEFORE FD obtained. Release order at every exit path: FD first (inner `finally`), then nonce (outer `finally`). Every exit path tagged with one of `{"success", "timeout", "http_error", "connection_reset", "exception"}` in the nonce release call-site. Any un-released nonce is a hard bug — asserted by test that counts reserve/release parity across crafted failures.
4. **Per-endpoint retry schedule = (1s, 2s, 4s) for 5xx / connection-reset; 4xx never retried.** DEGRADED after first retry; FAILED after third. All sleeps injected via `ClockFn.sleep(seconds: float)` so tests can skip wall-clock time.
5. **Response body hash captured in `content_hash`.** sha3_512 of the full page body, not per-row — page-level audit chaining per §4.1 line 444.
6. **Channel-A state aggregation.** Implement `classify_channel_a(per_endpoint)` per §4.1 line 462 verbatim: all-OK → OK; all-FAILED → FAILED; otherwise DEGRADED.
7. **Paging is explicit.** Grants.gov search2 returns a paged response. Round 4 sweeps all pages up to the endpoint's hard cap. Each page = one `HTTPClient.request` call. Nonce + FD released between pages; retries apply per page, not across the sweep.
8. **sam.gov + usaspending.gov do NOT produce candidates.** They write snapshots via `VaultWriter` under paths specified in §4.1 (`vault_shared/cached_entity_registrations/...`, `vault_shared/cached_awards_history/...`) and contribute only to `per_endpoint_state`.
9. **S10a invariant for sam.gov snapshot.** Entity-registration snapshot body MUST NOT carry org identifiers at write time — Round 4 asserts this before calling `vault_writer.write`. F-SCOUT-A-03 covers this (row-level S10a violation caught at adapter).
10. **No module-level side effects on import.** Zero network, zero vault, zero nonce reservations at import time.

## Public surface

```python
# pipeline/scout/channel_a_federal_apis.py
from typing import Protocol, Mapping

from pipeline.scout import (
    Candidate,
    CHANNEL_A,
    CHANNEL_A_CONNECT_TIMEOUT_S,
    CHANNEL_A_READ_TIMEOUT_S,
    CHANNEL_A_RETRY_COUNT,
    HEALTH_OK, HEALTH_DEGRADED, HEALTH_FAILED,
)

class HTTPResponse(Protocol):
    status: int
    headers: Mapping[str, str]
    body_bytes: bytes
    body_sha3_512_hex: str

class HTTPClient(Protocol):
    def request(self, method: str, url: str, *, headers: Mapping[str, str],
                body: bytes | None, connect_timeout_s: float,
                read_timeout_s: float) -> HTTPResponse: ...

class NonceRegistry(Protocol):
    def reserve(self, nonce_hex: str) -> None: ...
    def release(self, nonce_hex: str, *, path_tag: str) -> None: ...

class FDBroker(Protocol):
    def request_fd(self, *, kind: str, host: str) -> int: ...
    def release_fd(self, fd: int) -> None: ...

class VaultWriter(Protocol):
    def write(self, *, path: str, bytes_: bytes, intent: str,
              session_id: str, slug: str) -> None: ...

class ClockFn(Protocol):
    def __call__(self) -> datetime: ...
    def sleep(self, seconds: float) -> None: ...

@dataclass(frozen=True, kw_only=True)
class DegradationEvent:
    endpoint: str
    code: str
    reason_tag: str | None
    severity: str

@dataclass(frozen=True, kw_only=True)
class ChannelADiscoverResult:
    candidates: tuple[Candidate, ...]
    per_endpoint_state: Mapping[str, str]
    channel_state: str
    backbone_failed: bool
    degradation_events: tuple[DegradationEvent, ...]

def discover_channel_a(
    *, session, fd_broker, nonce_registry, vault_writer,
    http_client, clock=_default_clock,
) -> ChannelADiscoverResult: ...
```

Re-export `discover_channel_a`, `ChannelADiscoverResult`, Channel A protocol types from `pipeline.scout.__init__`. Bump `__version__` to `"0.1.0-scout-r4"`.

## Failure-code taxonomy

| Code | Raised when | State effect |
|------|-------------|--------------|
| `F-SCOUT-A-01` | FD broker raises / FD leak detected | endpoint FAILED; event recorded |
| `F-SCOUT-A-02` | Nonce reserve fails (replay detected) or release parity violated | endpoint FAILED; hard bug surfaced |
| `F-SCOUT-A-03` | Response body parse fails OR S10a violation on sam.gov snapshot | row skipped OR snapshot rejected |
| `F-SCOUT-A-04` | Grants.gov fetchOpportunity IdentityTuple mismatch (VERIFY-side) | file-equivalent abort (out of Round 4 scope — VERIFY is R8) |
| `F-SCOUT-A-05` (new) | All three retries exhausted on 5xx / connection-reset | endpoint FAILED |
| `F-SCOUT-A-06` (new) | 4xx response (non-retriable) | endpoint DEGRADED (first occurrence) or FAILED (all attempts 4xx) |

## Test surface (target ~80 tests — Round 4 is larger than Round 3 due to three endpoints × retry ladder × state transitions)

Lives at `tests/scout/test_round_4_channel_a_federal_apis.py`.

- `TestHappyPath` (6) — each endpoint OK in isolation; all three OK together; grants.gov single-page → N candidates; multi-page sweep → candidates concatenated across pages; sam.gov snapshot written with correct path; usaspending.gov snapshot written.
- `TestPerEndpointRetry` (9) — 5xx then success → DEGRADED; 5xx×3 → FAILED; connection-reset×3 → FAILED; timeout×3 → FAILED; 4xx→first attempt DEGRADED; 4xx×3 → FAILED; (1s, 2s, 4s) sleep schedule observed; retries apply per page not per sweep; connect vs read timeout distinguished.
- `TestNonceFDLifecycle` (8) — parity: reserve count == release count on success + every failure path; FD released before nonce on every exit; `path_tag` values correct per exit; crafted FD-broker raise → F-SCOUT-A-01 + nonce still released; crafted nonce-reserve raise → F-SCOUT-A-02; un-releasable nonce = hard bug (test asserts exception propagates).
- `TestChannelStateAggregation` (5) — all OK → OK; mixed → DEGRADED; all FAILED → FAILED + backbone_failed=True; two FAILED + one OK → DEGRADED + backbone_failed=False; two OK + one FAILED → DEGRADED.
- `TestBackboneFailed` (3) — only set when all three endpoints are FAILED; not set when any endpoint is DEGRADED-only; not set when only one endpoint is FAILED.
- `TestContentHashing` (3) — sha3_512 matches body bytes; carried into Candidate.content_hash; differs across pages.
- `TestS10aSamGovSnapshot` (3) — snapshot with no org identifiers accepted; snapshot containing an org identifier rejected with F-SCOUT-A-03 + vault_writer NOT called; borderline field (non-identifier metadata) accepted.
- `TestHTTPClientCallSite` (4) — connect_timeout_s = 10; read_timeout_s = 30; method/url correct per endpoint; headers include expected API identifiers.
- `TestClockSleepInjection` (3) — retries use injected sleep (no real wall-clock wait); sleep sequence is (1.0, 2.0, 4.0); zero sleeps on first-success path.
- `TestKWOnly` (1) — positional call rejected.
- `TestProtocolDiscipline` (4) — HTTPClient, FDBroker, NonceRegistry, VaultWriter minimal duck-typed fakes work.
- `TestNoModuleSideEffects` (1) — import does not open FDs, touch network, or reserve nonces.
- `TestASTLintRegression` (1) — `lint_tree` clean on `channel_a_federal_apis.py`.
- `TestPublicSurface` (3) — `__all__` contract; re-exports reachable; version pin.
- `TestGrantsGovPagination` (4) — single-page, two-page, empty-page, page-cap terminator.

Total ≈ 58. May grow as failure-code exhaustiveness lands. Coverage target 100% on `channel_a_federal_apis.py`.

## pyproject.toml / dep changes

Check whether `requests` or `urllib3` is already listed. If neither, Round 4 adds `urllib3 >= 2.0` (vendored stdlib-adjacent). No async HTTP — sync only, as the parallelism comes from Pipeline's DISCOVER_POOL_MAX_WORKERS orchestration (Round 11).

## Committee dispatch

Because Round 4 introduces the first live network-side-effect surface in Scout, single-cycle self-LOCK is NOT eligible. Dispatch 5-family Code Thesis Committee per `router.yaml` on first complete test suite. One retry permitted per L-005.

## Done-definition

1. `pipeline/scout/channel_a_federal_apis.py` written per surface above.
2. `pipeline/scout/__init__.py` re-exports + `__version__ = "0.1.0-scout-r4"`.
3. `tests/scout/test_round_4_channel_a_federal_apis.py` — ≥55 tests across classes above.
4. `scripts/run_tests.sh tests/scout/` green.
5. `scripts/run_tests.sh` full suite green.
6. `scripts/run_lint.sh` clean.
7. Coverage on `pipeline.scout.channel_a_federal_apis` = 100%.
8. LOCK entry `project_impl_scout_round_4_locked.md` + MEMORY.md pointer.
9. Round 5 spec card pre-staged (`scout_round_5_channel_c_portals_and_channel_d_program_pages.md`).

## Dependencies and timing

- **Unblocks:** Round 5 (C + D share the HTTPClient Protocol Round 4 defines); Round 6 (E also uses HTTPClient); Round 7 (F uses a search-provider variant); Round 8 VERIFY (re-uses HTTPClient for grants.gov fetchOpportunity).
- **Blocked by:** Round 1 LOCK (done). Round 3 LOCK (done). Round 2 LOCK (done — M7 consumes Round 4's per-endpoint state).
- **Risk surface:** first live HTTP seam — retry ladder must not double-charge nonces; FD/nonce release parity is the highest-priority invariant.

## Pre-flight checklist

- [x] Blueprint hash pinned (`0a82d955f95b0fca`).
- [x] Rounds 1 + 2 + 3 LOCKs verified.
- [x] §1 `nonce_registry` + §2 `fd_broker` + §2 `vault_write` surfaces consumed as Protocols (E-017 reused).
- [ ] RED→GREEN cycle executed.
- [ ] Committee dispatch completed (mandatory for this round — no self-LOCK).
