# Spec card — pipeline.scout Round 5 (Channel C — seeded portals + Channel D — federal program pages)

**STATUS:** LOCKED-backfilled

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md`
  - §4.3 Channel C full spec (lines 493–519) — `channel_c_portals.py` implementation target
  - §4.4 Channel D full spec (lines 521–531) — `channel_d_program_pages.py` implementation target
  - §2.1 `Candidate` schema (Round 1 `_types.py`) — DISCOVER row shape
  - §6.2 `F-SCOUT-C-01..03` + `F-SCOUT-CHD-01..03` failure codes
  - §8 `CHANNEL_D_MAX_CANDIDATES_PER_PAGE = 200`, `CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER = 500` (add to Round 1 `_constants.py` if absent — verify pre-build)
  - §9 Channel C / Channel D intent strings (portal-page fetch + program-page fetch)
- Section 1 consumed surface: `canonical_slug(raw) -> str` (NFC + lowercase + strip) — LOCKED in Round D isolation (`pipeline.sovereignty.isolation`).
- Section 2 consumed surface: `fd_broker.request_fd/release_fd` (Round Q) + `nonce_registry.reserve/release` (Section 1) — LOCKED.
- Round 4 consumed surface: `HTTPClient` + `HTTPResponse` Protocols + `SessionLike` + `FDBroker` + `NonceRegistry` + `ChannelADegradationEvent` naming pattern — LOCKED 2026-04-20 in `pipeline/scout/channel_a_federal_apis.py`.

**Blueprint hash-at-card:** `0a82d955f95b0fca` (sha3_512(section_03_scout.md)[:16]) — identical to Rounds 1–4. Re-verify at build-time before Step 1.

**Spec-card version:** v1 (pre-staged 2026-04-20 on Round 4 LOCK close)
**Round:** Scout R5 of 11. Consumes Round 1 schemas + Round 4 HTTP Protocols (re-exported from `pipeline.scout`). Does NOT consume Round 2 / Round 3 at runtime.

---

## Summary

Land two sibling modules in one round because they share ~80% of the same outbound posture (FD broker + nonce + retry ladder + HTTPClient) but differ in registry shape, cap discipline, and state-aggregation rule:

1. `pipeline/scout/channel_c_portals.py` — adapter-per-portal registry keyed by canonical slug (`OrderedDict`), per-org opt-in portal list from `orgs/{slug}/scout/portals.yaml`. Each adapter function returns a `list[Candidate]` with `channel="C"` and `feed_or_adapter_id = "portal:" + cslug`.
2. `pipeline/scout/channel_d_program_pages.py` — adapter-per-ALN registry; each adapter fetches one-or-more federal program pages, parses rows, applies per-page cap (200) + per-adapter cumulative cap (500). Candidates carry `channel="D"` and `feed_or_adapter_id = "aln:" + aln_number`.

Public surface (both modules symmetric to Round 4 `discover_channel_a`):

```python
# channel_c_portals.py
def discover_channel_c(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    http_client: HTTPClient,
    portal_roster: tuple[str, ...],      # per-org opt-in canonical slugs
    clock: ClockFn = _default_clock,
) -> ChannelCDiscoverResult: ...

# channel_d_program_pages.py
def discover_channel_d(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    http_client: HTTPClient,
    adapter_roster: tuple[str, ...],     # per-org opt-in ALN adapter keys
    clock: ClockFn = _default_clock,
) -> ChannelDDiscoverResult: ...
```

Both return frozen kw_only dataclasses of the shape
`candidates: tuple[Candidate, ...]`, `per_adapter_state: Mapping[str, str]`, `channel_state: str`, `degradation_events: tuple[...DegradationEvent, ...]`.

Neither channel contributes to `backbone_failed` computation directly — the blueprint defines Channel A as the backbone. But each channel's `channel_state` flows into the Round 2 `health_tuple` as `channel_c`/`channel_d` fields.

## Design decisions (operator-disposed 2026-04-20, reversible)

1. **Two sibling modules, one round.** Merge is justified by Protocol-sharing + test-fixture overlap. Split only if committee flags ambiguity during audit.
2. **Reuse Round 4 Protocols verbatim.** `HTTPClient`, `HTTPResponse`, `FDBroker`, `NonceRegistry`, `SessionLike`, `ClockFn` are imported from `pipeline.scout` (re-exported from `channel_a_federal_apis` surface in Round 4). Do NOT redeclare Protocols.
3. **Adapter registry is module-level OrderedDict.** Channel C uses `PORTAL_ADAPTERS: OrderedDict[str, Callable]` keyed by canonical slug (§4.3 line 498). Channel D uses `PROGRAM_PAGE_ADAPTERS: OrderedDict[str, Callable]` keyed by ALN-prefixed key. Per F-OQ-01 (blueprint line 1469), the dicts stay separate in v1.
4. **`register_portal(portal_slug)` decorator raises `ScoutConfigError(F-SCOUT-C-03)` on duplicate canonical slug at import time.** §4.3 A-v3-09 closure. Channel D uses parallel `register_program_page(aln_number)` with `F-SCOUT-CHD-01` for duplicate ALN. Duplicate detection is import-time deterministic — no run-time check.
5. **No built-in adapters in v0.1.** `PORTAL_ADAPTERS` and `PROGRAM_PAGE_ADAPTERS` are empty dicts at module-import. Registration is done by operator modules shipped per-org under `orgs/{slug}/scout/adapters/`. Round 5 provides the registry + dispatcher; first adapter lands in a later round (or per-org config).
6. **Portal roster → adapter iteration order = roster order.** `discover_channel_c` iterates the `portal_roster` tuple in the order given, NOT the insertion order of `PORTAL_ADAPTERS`. This makes runs deterministic per-org regardless of module import order. Missing roster entries (slug in roster but no adapter registered) → per-adapter FAILED with `F-SCOUT-C-01 ChannelCPortalAdapterMissing` (new sub-code).
7. **Per-adapter retry ladder = Round 4's.** Reuse `CHANNEL_A_CONNECT_TIMEOUT_S`, `CHANNEL_A_READ_TIMEOUT_S`, `CHANNEL_A_RETRY_COUNT` (1.0/2.0/4.0 s sleeps — copy the inline-literal back-off pattern from Round 4). Rename internal constants to `_CHANNEL_CD_*` aliases if Ruff objects; do NOT introduce new §8 pins.
8. **Channel C state aggregation = §4.3 line 517 verbatim.** `≥ 50% of registered portals FAILED → FAILED`; any other partial failure → DEGRADED; all OK → OK. Denominator = `len(portal_roster)`, not `len(PORTAL_ADAPTERS)`.
9. **Channel D state aggregation = §4.4 line 531 verbatim.** OK if all adapters succeeded with zero cap events; DEGRADED on any single fetch failure OR any page `F-SCOUT-CHD-02` OR any adapter `F-SCOUT-CHD-03`; FAILED only if all adapters failed.
10. **Per-page cap BEFORE append (Channel D).** Apply `CHANNEL_D_MAX_CANDIDATES_PER_PAGE = 200` strictly before append — iterate parsed rows, increment counter, `break` on 201st. This is the A-04 invariant; committee will challenge any after-the-fact truncation.
11. **Per-adapter cumulative cap BEFORE append (Channel D).** `_channel_d_adapter_candidate_counts: dict[str, int]` local to `discover_channel_d` (NOT module-level — would leak across runs). Check against `CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER = 500` BEFORE append. On hit: emit `F-SCOUT-CHD-03`, flag adapter DEGRADED, skip remaining pages from that adapter.
12. **`feed_or_adapter_id` namespacing asserted by `_build_channel_c_candidate` / `_build_channel_d_candidate`.** Helpers enforce the `"portal:"` / `"aln:"` prefix via assertion — defence against an adapter returning unnamespaced ids that would collide with Channel E (`"rss:"`) or Channel F (`"api:"`).
13. **Try/finally lifecycle identical to Round 4.** Nonce reserved BEFORE FD; release order FD-inner / nonce-outer. `path_tag` on nonce release: `{"success", "timeout", "http_error", "connection_reset", "parse_error", "cap_reached", "exception"}`.
14. **No module-level side effects on import.** Zero network, zero FD reservations, zero nonce reservations. Adapter-registration at import time IS permitted (that is the whole point of the decorator) — but registration must not perform network I/O.
15. **`portals.yaml` loading is out of scope for Round 5.** Round 5 accepts `portal_roster` as an already-loaded `tuple[str, ...]`. The caller (Pipeline §5 `invoke_seat` or a test harness) is responsible for loading `orgs/{slug}/scout/portals.yaml` via `vault_read`. Same for Channel D's `adapter_roster`. This keeps Round 5 a pure adapter-dispatcher.

## Public surface

```python
# pipeline/scout/channel_c_portals.py
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable, Mapping

from pipeline.scout import (
    Candidate,
    CHANNEL_C,
    CHANNEL_A_CONNECT_TIMEOUT_S,
    CHANNEL_A_READ_TIMEOUT_S,
    CHANNEL_A_RETRY_COUNT,
    HEALTH_OK, HEALTH_DEGRADED, HEALTH_FAILED,
    HTTPClient, HTTPResponse,
    FDBroker, NonceRegistry, SessionLike,
    ClockFn,
)

PORTAL_ADAPTERS: "OrderedDict[str, Callable[..., list[Candidate]]]" = OrderedDict()

class ScoutConfigError(Exception): ...

def canonical_slug(raw: str) -> str: ...      # import from pipeline.sovereignty.isolation

def register_portal(portal_slug: str) -> Callable: ...   # decorator; raises ScoutConfigError(F-SCOUT-C-03) on duplicate

@dataclass(frozen=True, kw_only=True)
class ChannelCDegradationEvent:
    portal_slug: str
    code: str
    reason_tag: str | None
    severity: str

@dataclass(frozen=True, kw_only=True)
class ChannelCDiscoverResult:
    candidates: tuple[Candidate, ...]
    per_adapter_state: Mapping[str, str]   # cslug -> {OK, DEGRADED, FAILED}
    channel_state: str
    degradation_events: tuple[ChannelCDegradationEvent, ...]

def discover_channel_c(
    *, session, fd_broker, nonce_registry, http_client,
    portal_roster: tuple[str, ...], clock=_default_clock,
) -> ChannelCDiscoverResult: ...


# pipeline/scout/channel_d_program_pages.py
PROGRAM_PAGE_ADAPTERS: "OrderedDict[str, Callable[..., list[Candidate]]]" = OrderedDict()

def register_program_page(aln_number: str) -> Callable: ...   # raises ScoutConfigError(F-SCOUT-CHD-01) on duplicate

@dataclass(frozen=True, kw_only=True)
class ChannelDDegradationEvent:
    aln_number: str
    code: str
    reason_tag: str | None
    severity: str
    overflow_count: int = 0

@dataclass(frozen=True, kw_only=True)
class ChannelDDiscoverResult:
    candidates: tuple[Candidate, ...]
    per_adapter_state: Mapping[str, str]
    channel_state: str
    degradation_events: tuple[ChannelDDegradationEvent, ...]

def discover_channel_d(
    *, session, fd_broker, nonce_registry, http_client,
    adapter_roster: tuple[str, ...], clock=_default_clock,
) -> ChannelDDiscoverResult: ...
```

Re-export from `pipeline.scout.__init__`: `discover_channel_c`, `discover_channel_d`, both `*DiscoverResult` and `*DegradationEvent` dataclasses, `PORTAL_ADAPTERS`, `PROGRAM_PAGE_ADAPTERS`, `register_portal`, `register_program_page`, `canonical_slug` (if not already re-exported from isolation). Bump `__version__` to `"0.1.0-scout-r5"`.

## Failure-code taxonomy

| Code | Raised when | State effect |
|------|-------------|--------------|
| `F-SCOUT-C-01` | Portal slug in roster but no adapter registered | adapter FAILED |
| `F-SCOUT-C-02` | Portal fetch 5xx / connect-reset / timeout — retries exhausted | adapter FAILED |
| `F-SCOUT-C-03` | Duplicate canonical slug at `register_portal` import-time | `ScoutConfigError` raised at import |
| `F-SCOUT-CHD-01` | Duplicate ALN at `register_program_page` import-time | `ScoutConfigError` raised at import |
| `F-SCOUT-CHD-02` | Per-page row count > 200 | page truncated, adapter DEGRADED |
| `F-SCOUT-CHD-03` | Per-adapter cumulative row count reaches 500 | remaining pages skipped, adapter DEGRADED |
| `F-SCOUT-CHD-04` (new) | Program-page fetch 5xx / connect-reset / timeout — retries exhausted | adapter FAILED |
| `F-SCOUT-CHD-05` (new) | Program-page 4xx response | adapter DEGRADED on first; FAILED on all-4xx |

## Test surface (target ≈ 90 tests across both modules — one `tests/scout/test_round_5_channels_c_and_d.py` file)

### Channel C

- `TestChannelCHappyPath` (4) — one adapter OK; three adapters all OK; adapter returning zero candidates is OK (not FAILED); roster order preserved in output.
- `TestChannelCRegistry` (5) — `register_portal` registers under canonical slug; duplicate raises `ScoutConfigError(F-SCOUT-C-03)` at import; NFC drift between raw + cslug detected; `PORTAL_ADAPTERS` empty at module import; deregistration not supported (no public API).
- `TestChannelCAdapterMissing` (3) — roster slug not in registry → adapter FAILED with `F-SCOUT-C-01`; per_adapter_state includes the missing slug; other roster adapters continue.
- `TestChannelCRetryLadder` (6) — 5xx then success → adapter DEGRADED; 5xx×3 → FAILED; connection-reset×3 → FAILED; timeout×3 → FAILED; sleep sequence (1.0, 2.0, 4.0) observed; retries per-adapter not cross-adapter.
- `TestChannelCStateAggregation` (5) — all OK → OK; one FAILED of three → DEGRADED; two FAILED of three → FAILED (≥50%); five of ten FAILED → FAILED (exactly 50%); four of ten FAILED → DEGRADED (below threshold).
- `TestChannelCNonceFDLifecycle` (6) — parity reserve==release per-adapter; FD released before nonce; `path_tag` correct per exit; FD-broker raise → F-SCOUT-C-02 + nonce still released; nonce-reserve raise → F-SCOUT-A-02 reused; one adapter failing does not starve FDs for next adapter.
- `TestChannelCFeedAdapterIdNamespace` (2) — helper asserts `"portal:"` prefix on build; un-prefixed id from adapter rejected with AssertionError.
- `TestChannelCNoModuleSideEffects` (1) — import opens zero FDs, zero nonces.
- `TestChannelCKWOnly` (1) — positional call rejected.

### Channel D

- `TestChannelDHappyPath` (4) — one adapter single-page OK; one adapter multi-page OK; three adapters all OK; adapter returning zero rows OK.
- `TestChannelDRegistry` (4) — `register_program_page` registers under ALN; duplicate raises `F-SCOUT-CHD-01` at import; `PROGRAM_PAGE_ADAPTERS` empty at import; adapter key format asserted.
- `TestChannelDPerPageCap` (5) — 200 rows → 200 candidates, no event; 201 rows → 200 candidates + `F-SCOUT-CHD-02` event; 500 rows → 200 candidates + event + overflow_count=300; cap applied BEFORE append (property test: random N ∈ [0,1000] → `min(N,200)`); multiple pages each capped independently.
- `TestChannelDPerAdapterCap` (5) — adapter at 499 with page of 1 row → OK; adapter at 499 with page of 2 rows → 1 appended, cap hit, `F-SCOUT-CHD-03`; adapter at 500 with more pages → remaining pages skipped; counter is local-to-run (not module-level); other adapters continue after one adapter hits cap.
- `TestChannelDRetryLadder` (5) — 5xx×3 → FAILED via F-SCOUT-CHD-04; 4xx first attempt DEGRADED via F-SCOUT-CHD-05; 4xx×3 → FAILED; timeout×3 → FAILED; sleep sequence observed.
- `TestChannelDStateAggregation` (5) — all OK → OK; any fetch-fail → DEGRADED; any page-cap hit → DEGRADED; any adapter-cap hit → DEGRADED; all adapters failed → FAILED.
- `TestChannelDNonceFDLifecycle` (5) — parity per-page; FD release on cap-reached exit tagged `cap_reached`; nonce release on cap-reached exit; multi-page adapter releases FDs between pages; FD leak on cap-reached is a hard bug (regression test).
- `TestChannelDFeedAdapterIdNamespace` (2) — helper asserts `"aln:"` prefix; un-prefixed id rejected.
- `TestChannelDNoModuleSideEffects` (1) — import opens zero FDs, zero nonces.
- `TestChannelDKWOnly` (1) — positional call rejected.

### Cross-module

- `TestSharedProtocolReuse` (3) — both modules import `HTTPClient` from `pipeline.scout`, not redeclared; fake HTTPClient works against both; same FDBroker fake works against both.
- `TestASTLintRegression` (2) — `lint_tree` clean on `channel_c_portals.py` and `channel_d_program_pages.py`.
- `TestPublicSurface` (4) — `__all__` contract; re-exports reachable; version pin `"0.1.0-scout-r5"`; `F-SCOUT-C-*` + `F-SCOUT-CHD-*` strings match blueprint.

Total ≈ 73 tests in the base pass. May grow to 90+ as committee challenges land. Coverage target 100% on both modules.

## pyproject.toml / dep changes

None. Reuses Round 4's HTTP stack. If Round 4 landed `urllib3 >= 2.0` the dep is already present; Round 5 adds nothing.

## Committee dispatch

**Self-LOCK eligible** on first clean single-cycle run **IFF** all three of:
(a) AST-lint green on both modules,
(b) coverage 100% on both modules,
(c) full suite green (current baseline: 2316 pass after Round 4).

Otherwise dispatch 5-family Code Thesis Committee per `router.yaml`. Retry-1 permitted per L-005; E-023 closure discipline applies (isomorphic-to-deferred-scope = honest test_adv_* docs, not re-dispatch).

If adapter-registry invariant tests (F-SCOUT-C-03 / F-SCOUT-CHD-01 duplicate-raise) prove finicky (Python module-import ordering is subtle), consider carving them into `test_adv_round_5_registry_invariants.py` even on self-LOCK — import-order tests often surface flakes later.

## Done-definition

1. `pipeline/scout/channel_c_portals.py` written per surface above.
2. `pipeline/scout/channel_d_program_pages.py` written per surface above.
3. `pipeline/scout/__init__.py` re-exports + `__version__ = "0.1.0-scout-r5"`.
4. `_constants.py` updated iff `CHANNEL_D_MAX_CANDIDATES_PER_PAGE` / `CHANNEL_D_MAX_TOTAL_CANDIDATES_PER_ADAPTER` absent (check first).
5. `tests/scout/test_round_5_channels_c_and_d.py` — ≥70 tests across the classes above.
6. `scripts/run_tests.sh tests/scout/` green.
7. `scripts/run_tests.sh` full suite green (≥ 2316 baseline after Round 4).
8. `scripts/run_lint.sh` clean on both new modules.
9. Coverage = 100% on both modules.
10. LOCK entry `project_impl_scout_round_5_locked.md` + MEMORY.md pointer.
11. Round 6 spec card pre-staged (`scout_round_6_channel_e_rss.md`).

## Dependencies and timing

- **Unblocks:** Round 6 (Channel E reuses the same Protocols); Round 7 (Channel F); Round 8 VERIFY.
- **Blocked by:** Round 4 LOCK (done 2026-04-20).
- **Risk surface:** medium. The HTTP seam is already LOCKED (Round 4); Round 5's novelty is registry-decorator import-time duplicate-detection and the per-adapter cumulative cap. Both are mechanically simple but have import-order gotchas.
- **Out-of-scope surfaces** deferred to later rounds: `portals.yaml` / `adapter_roster.yaml` loaders (Round 5 accepts already-loaded tuples); built-in adapter implementations (per-org packaged, not landed in `pipeline.scout` directly); A-v3-04 `_assert_intent_matches` for roster-file reads (belongs to the loader, not Round 5).

## Pre-flight checklist

- [ ] Blueprint hash re-verified (`0a82d955f95b0fca`).
- [ ] Round 4 LOCK verified (`project_impl_scout_round_4_locked.md`).
- [ ] Round 1 constants checked — `CHANNEL_D_MAX_*` pins present? (add if missing)
- [ ] HTTPClient / FDBroker / NonceRegistry Protocol imports confirmed reachable from `pipeline.scout`.
- [ ] Pre-existing loop/seat_runner regression (`seat_runner.py:592` missing `raw_stdout` kwarg) confirmed spawned as separate task — Round 5 does not touch `pipeline/loop/`.
- [ ] RED→GREEN cycle executed.
- [ ] Committee dispatch executed OR self-LOCK conditions (a+b+c) all met.
