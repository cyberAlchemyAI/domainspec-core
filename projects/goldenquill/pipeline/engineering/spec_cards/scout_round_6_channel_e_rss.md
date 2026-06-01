# Spec card — pipeline.scout Round 6 (Channel E — RSS / newsletter watchlists)

**STATUS:** SELF-LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md`
  - §4.5 Channel E full spec (lines 533–546) — `channel_e_rss.py` implementation target
  - §6.5 `F-SCOUT-E-01..03` + four reason-tag sub-codes on `F-SCOUT-E-03` (lines 1177–1181)
  - §7.5 Unit-test list (lines 1272–1274) — seed cases
  - §7.16 Property-test list (lines 1377, 1384, 1388) — durable enforcement tests (A-05 / A-v3-08 / A-v4-01 / B-v5-04)
  - §8 `CHANNEL_E_RUNAWAY_MAX = 100`, `RSS_STALE_FEED_DEGRADED_DAYS = 60`, `FEED_POLL_MIN_INTERVAL_MIN = 15` — all present in Round 1 `_constants.py` (verified 2026-04-20 during pre-stage).
  - §2.1 `Candidate` schema — `channel == "E"`, `feed_or_adapter_id = "rss:" + sha3_512(feed_url)[:16].hex()`, `source_key = feed_entry_guid`, `content_hash = sha3_512(entry_body_bytes)`.
- Section 1 consumed surface: `canonical_slug` (if feed-URL canonicalisation is needed — probably not; feed URLs are already IDNA / punycode-normalised at roster load).
- Section 2 consumed surface: `fd_broker.request_fd` (Round Q) + `nonce_registry.reserve/release` (Section 1) — LOCKED.
- Round 4 consumed surface: `HTTPClient` + `HTTPResponse` Protocols + `SessionLike` + `FDBroker` + `NonceRegistry` + `ClockFn` — LOCKED.
- Round 5 consumed surface: `AdapterContext` frozen dataclass + `http_request_with_retries(ctx, method=, url=, host=, …)` + `ScoutConfigError` — LOCKED 2026-04-20 in `pipeline/scout/channel_c_portals.py`. **Do NOT redeclare — import from `pipeline.scout`.**

**Blueprint hash-at-card:** `0a82d955f95b0fca` (sha3_512(section_03_scout.md)[:16]) — identical to Rounds 1–5. Re-verify at build-time before Step 1.

**Spec-card version:** v1 (pre-staged 2026-04-20 on Round 5 LOCK close)
**Round:** Scout R6 of 11. Consumes Round 1 schemas + Round 5 `AdapterContext` / `http_request_with_retries` (re-exported from `pipeline.scout`). Does NOT consume Rounds 2 / 3 / 4 at runtime (Round 4 Protocols reach Round 6 via Round 5's re-export chain).

---

## Summary

Land one module: `pipeline/scout/channel_e_rss.py` — §4.5 adapter-less registry-free dispatcher that iterates a per-run `feed_watchlist: tuple[FeedSpec, ...]` and parses each feed via an **injected FeedParser factory Protocol** (no direct `feedparser` import inside the dispatcher — keeps Scout stdlib-adjacent and tests trivial).

Distinguishing Channel-E shape vs. Channel C/D:

1. **No registry / no decorator.** A feed is identified by its URL, not a canonical slug or ALN. The per-org `rss_watchlist.yaml` IS the list of "adapters" — each entry is a `FeedSpec(feed_url, …)`. Round 6 accepts the watchlist tuple already loaded; loader is out of scope.
2. **Streaming break on entry-token yield** (A-v3-08) — break fires at the first token of entry 101, NOT after entry body deserialisation. The dispatcher consumes the parser as an iterator/generator of parsed-entry dicts and increments a counter on every yield BEFORE running any Candidate construction.
3. **Explicit parser-buffer drain after break** (A-v4-01 + B-v5-04) — `_drain_parser_buffer(parser)` probes `parser.raw_data` → `parser.reset()` → `.drain_api_missing` reason-tag. Buffer-drain is mandatory on every truncation event; absence is a hard bug.
4. **feed-level state classifier is load-bearing** — `OK`, `DEGRADED`, `DEGRADED-stale`, `FAILED`. Stale-but-not-failed is a first-class state (newsletters go dormant). Channel-state rule is **strictly greater than 50% FAILED → FAILED** (unlike Channel C's `≥ 50%`).
5. **Polling min interval** — within a single run a duplicate feed URL in the watchlist is deduped at roster-canonicalisation time. Cross-run cadence lives on Pipeline §5, not here.

Public surface (symmetric to Round 5 dispatcher):

```python
def discover_channel_e(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    http_client: HTTPClient,
    feed_parser_factory: FeedParserFactory,
    feed_watchlist: tuple[FeedSpec, ...],
    clock: ClockFn = _default_clock,
) -> ChannelEDiscoverResult: ...
```

Return: frozen kw_only dataclass —
`candidates: tuple[Candidate, ...]`, `per_feed_state: Mapping[str, str]` (keyed by `feed_or_adapter_id`, NOT raw feed URL), `channel_state: str`, `degradation_events: tuple[ChannelEDegradationEvent, ...]`.

Channel E does not contribute to `backbone_failed`. Its `channel_state` flows into Round 2 `health_tuple` as `channel_e`.

## Design decisions (operator-disposed 2026-04-20, reversible)

1. **Reuse Round 5 `AdapterContext` verbatim.** Do NOT redeclare. `discover_channel_e` constructs the context once at the top and passes it to the per-feed worker. Adds one additional Protocol (`FeedParserFactory`) bundled via a sibling `FeedContext(AdapterContext)` wrapper OR passed alongside — land the simpler shape and document the choice.
2. **Reuse Round 5 `http_request_with_retries` for the HTTP fetch step.** But note: RSS needs the **raw body bytes**, so the call is `method="GET", stream=False` and the returned `HTTPResponse` MUST expose `.content: bytes`. Round 4's `HTTPResponse` already has `content`. No shape change needed.
3. **Inject a `FeedParserFactory` Protocol.** Shape:
   ```python
   class FeedParserFactory(Protocol):
       def parse_streaming(self, raw_body: bytes) -> FeedParseResult: ...
   ```
   where `FeedParseResult` is a frozen dataclass exposing:
   - `bozo: bool` — malformed XML flag
   - `feed_modified_iso: str | None` — feed-level last-modified timestamp (ISO-8601); dispatcher uses this for stale check
   - `entries: Iterator[FeedEntry]` — **lazy iterator** (not a list) producing parsed entry dicts; iteration is what triggers the streaming break
   - `raw_data_buffer: "BufferLike"` — handle the drain helper probes via `hasattr(parser, "raw_data")` / `hasattr(parser, "reset")`. Concrete implementation wraps `feedparser.parse(...)` and exposes the library's internal buffer; test doubles supply a controllable fake.
   The concrete `FeedparserLibFactory` is defined in a dedicated sub-module `pipeline/scout/_feedparser_adapter.py` that is THE ONLY place `import feedparser` appears. Round 6's dispatcher has no direct feedparser dependency.
3b. **`FeedEntry` shape** — frozen dataclass with `guid: str`, `body_bytes: bytes`, `published_iso: str | None`. Canonicalisation of the entry body bytes (UTF-8 normalised, trailing-whitespace-stripped, line-ending-normalised to `\n`) happens inside the factory so `content_hash` is deterministic across feedparser versions.
4. **`feed_or_adapter_id` namespacing asserted in `_build_channel_e_candidate`.** `"rss:" + sha3_512(feed_url_canonical_bytes)[:16].hex()`. Helper asserts the `"rss:"` prefix; an un-prefixed id rejected with AssertionError. This closes RT-v1-MED-05 alongside A-v3-09.
5. **`source_key = feed_entry.guid`.** If guid is empty → adapter emits `F-SCOUT-E-01` with reason-tag `empty_guid` and DEGRADED for that feed — an RSS entry with no guid is malformed.
6. **`content_hash = sha3_512(canonical_body_bytes)`.** Body bytes are what the factory returns via `FeedEntry.body_bytes`. Canonicalisation lives in the factory (see decision 3b).
7. **Streaming break strictly at entry-token yield.** Dispatcher pseudo-code:
   ```python
   entries_seen = 0
   candidates_for_this_feed: list[Candidate] = []
   for entry in parse_result.entries:
       entries_seen += 1
       if entries_seen > CHANNEL_E_RUNAWAY_MAX:   # i.e. on the 101st entry
           _emit_runaway_event(...)               # F-SCOUT-E-03 + reason-tag
           break
       candidates_for_this_feed.append(_build_channel_e_candidate(entry, feed_url))
   ```
   Count-first-then-decide. The 101st `next()` yield triggers the break BEFORE `_build_channel_e_candidate` runs on entry 101. This is the A-v3-08 / RT-v2-MED-04 closure.
8. **Buffer-drain helper with hasattr-dispatch.**
   ```python
   def _drain_parser_buffer(parser_handle: object) -> tuple[bool, str]:
       if hasattr(parser_handle, "raw_data"):
           parser_handle.raw_data = bytearray()
           return (True, "buffer_drained")
       if hasattr(parser_handle, "reset"):
           parser_handle.reset()
           return (True, "buffer_drained")
       return (False, "drain_api_missing")
   ```
   Called **unconditionally** in the `try/finally` on any feed where `entries_seen > 0` (not only on cap-hit — the buffer may hold entry-N+1 bytes even on clean exits). Return tuple feeds the `F-SCOUT-E-03.buffer_drained` vs `.drain_api_missing` reason-tag emission. `.drain_api_missing` → feed flipped to FAILED + admin-risk MEDIUM on the health tuple.
9. **Reason-tag taxonomy on `F-SCOUT-E-03`** (blueprint §6.5):
   - `.streaming_break` — break fired mid-chunk (the streaming path). Co-emitted with `.buffer_drained` or `.drain_api_missing`.
   - `.post_fetch_break` — entire body was already buffered when the 101st entry token yielded. Co-emitted with `.buffer_drained` or `.drain_api_missing`.
   - `.buffer_drained` — emitted iff path (i) or (ii) of `_drain_parser_buffer` ran successfully.
   - `.drain_api_missing` — emitted iff neither `raw_data` nor `reset()` was available on the parser handle. Feed flipped to FAILED (NOT DEGRADED).
   The dispatcher MUST emit exactly one of `.streaming_break` / `.post_fetch_break` AND exactly one of `.buffer_drained` / `.drain_api_missing` on any truncation event. Invariant asserted by a dedicated `TestChannelERunawayReasonTagInvariant` test class.
10. **TLS invalid → `F-SCOUT-E-02` FAILED.** `HTTPClient` is expected to raise a specific exception (reuse Round 4's exception surface if one exists for TLS; else catch `ssl.SSLError` / `ssl.SSLCertVerificationError` by class name). Feed FAILED; admin-risk HIGH. The dispatcher does NOT raise — it records the degradation event and continues to the next feed.
11. **Malformed XML → `F-SCOUT-E-01` DEGRADED.** `bozo=True` on the parse result → emit `F-SCOUT-E-01` with reason-tag `malformed_xml`; the feed is DEGRADED (not FAILED — `bozo` frequently fires on technically-non-compliant-but-still-parseable feeds). Candidates already parsed before the bozo hit ARE kept. Empty-guid entries → `F-SCOUT-E-01.empty_guid` DEGRADED (decision 5).
12. **Stale-feed 60-day threshold → `DEGRADED` with reason-tag `feed_stale_channel_e`.** Checked after successful parse: compute `now - max(entry.published_iso)`; if > `RSS_STALE_FEED_DEGRADED_DAYS`, flip feed to DEGRADED with that reason-tag. State string in `per_feed_state` is `"DEGRADED"` (NOT a separate `"STALE"` state — blueprint §4.5 says "DEGRADED for that feed with reason `feed_stale_channel_e`"). Does NOT prevent candidates from being returned — a stale feed still contributes whatever entries it had.
13. **Per-feed retry ladder = Round 5's shared retry ladder.** Reuse `http_request_with_retries`. Retries on 5xx / TimeoutError / ConnectionError; 4xx non-retriable. HTTP 4xx on a feed → DEGRADED + `F-SCOUT-E-01.http_4xx` reason-tag (not FAILED — 404 on a newsletter is a common dormancy signal). HTTP 5xx-after-retries → FAILED + `F-SCOUT-E-02` (reuse for "server unreachable").
14. **Channel E state aggregation = §4.5 line 546 verbatim.**
    - All feeds OK or DEGRADED-stale → `OK`.
    - Any feed FAILED AND ≤ 50% feeds FAILED → `DEGRADED`.
    - **Strictly greater than 50%** feeds FAILED → `FAILED`. (Boundary test: 5/10 FAILED → DEGRADED; 6/10 FAILED → FAILED; 1/1 FAILED → FAILED; 0/0 feeds → FAILED, same as empty Channel C/D roster.)
    - Denominator = `len(feed_watchlist)` after dedup.
15. **Try/finally lifecycle per feed.** Nonce reserved BEFORE FD (mirror Round 4/5). Release order: FD-inner / nonce-outer. Additional inner step: **buffer drain MUST run between HTTPResponse consumption and FD release** — drain is part of the "reading the body" phase, not cleanup. If drain raises inside its `try`, record `F-SCOUT-E-03.drain_api_missing` and still release FD + nonce via the outer finally. `path_tag` on nonce release: `{"success", "timeout", "http_error", "tls_error", "malformed", "runaway_break", "drain_failed", "exception"}`.
16. **`feed_watchlist` dedup at dispatcher entry.** Same feed URL listed twice in the roster → dedup on canonicalised URL (IDNA-normalised lowercase host + percent-decoded path), keeping first occurrence. Not an error — some orgs may include the same feed in two YAML sections. The `per_feed_state` map shows the feed once.
17. **Feed URL canonicalisation.** Land a small `_canonical_feed_url(raw: str) -> str` helper: IDNA (punycode) the host; lowercase the host; strip trailing `/` (but NOT query or fragment); percent-decode reserved characters. This canonical form is what feeds `sha3_512(feed_url_bytes)[:16]` to build `feed_or_adapter_id`. **Round 6 asserts** two feeds whose raw strings differ only in host-case or trailing slash produce the same `feed_or_adapter_id`.
18. **No module-level side effects on import.** Zero network, zero FD reservations, zero nonce reservations, zero `feedparser.parse()` calls. The `FeedparserLibFactory` constructor MAY import `feedparser` lazily on first `parse_streaming()` call; tests that use test doubles never trigger the real import.

## Public surface

```python
# pipeline/scout/channel_e_rss.py
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable, Iterator, Mapping, Protocol

from pipeline.scout import (
    AdapterContext,
    Candidate,
    CHANNEL_E,
    CHANNEL_E_RUNAWAY_MAX,
    RSS_STALE_FEED_DEGRADED_DAYS,
    FEED_POLL_MIN_INTERVAL_MIN,
    HEALTH_OK, HEALTH_DEGRADED, HEALTH_FAILED,
    HTTPClient, HTTPResponse,
    FDBroker, NonceRegistry, SessionLike,
    ClockFn, ScoutConfigError,
    http_request_with_retries,
)


@dataclass(frozen=True, kw_only=True)
class FeedSpec:
    feed_url: str
    feed_url_canonical: str         # computed by _canonical_feed_url at roster load or dispatcher entry
    admin_risk_carry: str | None = None


@dataclass(frozen=True, kw_only=True)
class FeedEntry:
    guid: str
    body_bytes: bytes
    published_iso: str | None


@dataclass(frozen=True, kw_only=True)
class FeedParseResult:
    bozo: bool
    feed_modified_iso: str | None
    entries: Iterator[FeedEntry]
    raw_data_buffer_handle: object   # the parser handle itself; _drain_parser_buffer probes attrs on this


class FeedParserFactory(Protocol):
    def parse_streaming(self, raw_body: bytes) -> FeedParseResult: ...


@dataclass(frozen=True, kw_only=True)
class ChannelESubEvent:
    feed_or_adapter_id: str
    code: str
    reason_tag: str | None
    severity: str


@dataclass(frozen=True, kw_only=True)
class ChannelEDegradationEvent:
    feed_or_adapter_id: str
    code: str
    reason_tag: str | None
    severity: str
    overflow_count: int = 0


@dataclass(frozen=True, kw_only=True)
class ChannelEDiscoverResult:
    candidates: tuple[Candidate, ...]
    per_feed_state: Mapping[str, str]   # feed_or_adapter_id -> {OK, DEGRADED, FAILED}
    channel_state: str
    degradation_events: tuple[ChannelEDegradationEvent, ...]


def discover_channel_e(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    http_client: HTTPClient,
    feed_parser_factory: FeedParserFactory,
    feed_watchlist: tuple[FeedSpec, ...],
    clock: ClockFn = _default_clock,
) -> ChannelEDiscoverResult: ...


# pipeline/scout/_feedparser_adapter.py  (new file, one-line smoke test + concrete factory)
class FeedparserLibFactory:
    def parse_streaming(self, raw_body: bytes) -> FeedParseResult: ...
```

**Re-exports from `pipeline.scout.__init__`:** `discover_channel_e`, `FeedSpec`, `FeedEntry`, `FeedParseResult`, `FeedParserFactory` (Protocol), `FeedparserLibFactory` (concrete), `ChannelESubEvent`, `ChannelEDegradationEvent`, `ChannelEDiscoverResult`. Bump `__version__` to `"0.1.0-scout-r6"`.

## pyproject.toml / dep changes

Add `feedparser>=6.0` under `[project.dependencies]`. Document in the dep comment block:

```toml
    # Round-6 (Channel E RSS dispatcher): feedparser is the only Channel E
    # dependency. Library API drift is handled by _drain_parser_buffer's
    # hasattr-dispatch (B-v5-04 closure). The library import is isolated to
    # pipeline/scout/_feedparser_adapter.py (single entry point).
    "feedparser>=6.0",
```

Run `scripts/run_tests.sh` after pyproject bump to confirm `feedparser` resolves in `.venv`.

## Failure-code taxonomy

| Code | Reason-tag | Raised when | State effect |
|------|------------|-------------|--------------|
| `F-SCOUT-E-01` | `malformed_xml` | `bozo=True` on parse result | feed DEGRADED |
| `F-SCOUT-E-01` | `empty_guid` | An entry has empty/missing guid | entry skipped; feed DEGRADED |
| `F-SCOUT-E-01` | `http_4xx` | HTTP 4xx on feed fetch | feed DEGRADED |
| `F-SCOUT-E-02` | `tls_invalid` | TLS cert verification fails | feed FAILED; admin-risk HIGH |
| `F-SCOUT-E-02` | `server_unreachable` | HTTP 5xx-after-retries OR ConnectionError-after-retries OR TimeoutError-after-retries | feed FAILED |
| `F-SCOUT-E-03` | `streaming_break` | Entry 101 token yielded mid-chunk | feed DEGRADED; truncated at 100 |
| `F-SCOUT-E-03` | `post_fetch_break` | Entry 101 token yielded from fully-buffered body | feed DEGRADED; truncated at 100 |
| `F-SCOUT-E-03` | `buffer_drained` | `_drain_parser_buffer` ran successfully via path (i) or (ii) | co-emitted with `.streaming_break` OR `.post_fetch_break` |
| `F-SCOUT-E-03` | `drain_api_missing` | Parser handle exposes neither `raw_data` nor `reset()` | feed FAILED; admin-risk MEDIUM |
| `F-SCOUT-E-04` (new, if needed) | `feed_stale_channel_e` | Latest entry > 60 days old | feed DEGRADED with reason-tag (may emit under F-SCOUT-E-01 — decide during build) |

Decision on whether staleness gets its own code: if it simplifies state-classifier to treat it as a DEGRADED event rather than mixing reason-tags on F-SCOUT-E-01, land `F-SCOUT-E-04`. Otherwise reuse F-SCOUT-E-01 with a `.stale` sub-tag. Mark Open-Q in the LOCK memo.

## Test surface (target ≈ 80 tests, single `tests/scout/test_round_6_channel_e_rss.py`)

### Happy path (4)
- `TestChannelEHappyPath::test_single_feed_with_three_entries_all_ok`
- `TestChannelEHappyPath::test_three_feeds_all_ok`
- `TestChannelEHappyPath::test_empty_feed_zero_entries_still_ok`
- `TestChannelEHappyPath::test_feed_order_preserved_in_output`

### `FeedParserFactory` Protocol (6)
- `TestFeedParserFactory::test_injected_factory_called_with_raw_bytes`
- `TestFeedParserFactory::test_factory_exception_tagged_f_scout_e_01_malformed`
- `TestFeedParserFactory::test_bozo_true_degrades_feed`
- `TestFeedParserFactory::test_bozo_true_with_entries_still_yields_candidates`
- `TestFeedParserFactory::test_empty_guid_emits_f_scout_e_01_empty_guid`
- `TestFeedParserFactory::test_published_iso_parsed_into_candidate`

### Runaway / streaming break (10)
- `TestChannelERunaway::test_200_entries_truncated_at_100_before_candidate_construction` — pre-instrument Candidate `__post_init__` counter; assert 100 exactly.
- `TestChannelERunaway::test_101st_entry_never_constructed` — property test with entry count `N ∈ [0, 1000]`: `len(candidates) == min(N, 100)`.
- `TestChannelERunaway::test_streaming_break_reason_tag_emitted`
- `TestChannelERunaway::test_post_fetch_break_reason_tag_emitted`
- `TestChannelERunaway::test_runaway_reason_tag_invariant_streaming_xor_post_fetch` — exactly one of the two break reason-tags must be present on every truncation event.
- `TestChannelERunaway::test_runaway_reason_tag_invariant_buffer_drained_xor_drain_api_missing` — exactly one of the two drain reason-tags must be present.
- `TestChannelERunaway::test_drain_buffer_path_i_raw_data_replaced` — parser handle with `raw_data` → replaced with empty `bytearray`; `.buffer_drained` emitted.
- `TestChannelERunaway::test_drain_buffer_path_ii_reset_called` — parser handle with `reset()` (no `raw_data`) → `reset()` called; `.buffer_drained` emitted.
- `TestChannelERunaway::test_drain_buffer_path_iii_api_missing_flips_feed_failed` — neither attr → `.drain_api_missing` emitted + feed state `FAILED` + admin-risk MEDIUM event.
- `TestChannelERunaway::test_drain_runs_even_when_entries_below_cap` — 50-entry feed still triggers buffer drain attempt on exit (defence in depth; library may pre-buffer).

### Stale-feed (4)
- `TestChannelEStale::test_feed_with_latest_entry_older_than_60_days_degraded` — reason-tag `feed_stale_channel_e`.
- `TestChannelEStale::test_feed_with_latest_entry_exactly_60_days_inclusive_or_exclusive` — blueprint-literal reading: check blueprint §4.5 wording ("> 60 days" → exclusive). Document decision in code comment.
- `TestChannelEStale::test_stale_feed_still_yields_candidates` — stale flagging does not drop entries.
- `TestChannelEStale::test_stale_feed_classified_ok_at_channel_level_not_failed` — channel-state unaffected by stale flag.

### HTTP failure (10)
- `TestChannelEHTTP::test_tls_invalid_feed_failed_f_scout_e_02`
- `TestChannelEHTTP::test_http_404_feed_degraded_f_scout_e_01_http_4xx`
- `TestChannelEHTTP::test_http_500_retries_then_failed_f_scout_e_02_server_unreachable`
- `TestChannelEHTTP::test_http_500_then_200_degraded_not_failed`
- `TestChannelEHTTP::test_timeout_exhausted_failed`
- `TestChannelEHTTP::test_connection_reset_exhausted_failed`
- `TestChannelEHTTP::test_retry_sleep_sequence_1_0_2_0_4_0`
- `TestChannelEHTTP::test_retries_per_feed_not_cross_feed`
- `TestChannelEHTTP::test_first_success_no_sleeps_observed`
- `TestChannelEHTTP::test_4xx_not_retried`

### State aggregation (7)
- `TestChannelEStateAggregation::test_all_ok_channel_ok`
- `TestChannelEStateAggregation::test_all_degraded_stale_channel_ok` — stale flag does NOT tip channel to DEGRADED.
- `TestChannelEStateAggregation::test_one_failed_of_three_channel_degraded`
- `TestChannelEStateAggregation::test_exactly_5_of_10_failed_channel_degraded` — boundary (strictly > 50%).
- `TestChannelEStateAggregation::test_6_of_10_failed_channel_failed` — boundary.
- `TestChannelEStateAggregation::test_1_of_1_failed_channel_failed`
- `TestChannelEStateAggregation::test_empty_watchlist_channel_failed` — symmetric with Channel C/D empty-roster rule.

### Nonce / FD lifecycle (8)
- `TestChannelENonceFDLifecycle::test_parity_reserve_release_success`
- `TestChannelENonceFDLifecycle::test_fd_released_before_nonce`
- `TestChannelENonceFDLifecycle::test_path_tag_success`
- `TestChannelENonceFDLifecycle::test_path_tag_timeout`
- `TestChannelENonceFDLifecycle::test_path_tag_tls_error`
- `TestChannelENonceFDLifecycle::test_path_tag_runaway_break`
- `TestChannelENonceFDLifecycle::test_path_tag_drain_failed` — `drain_api_missing` path releases FD + nonce with `path_tag="drain_failed"`.
- `TestChannelENonceFDLifecycle::test_one_feed_failing_does_not_starve_fds_for_next_feed`

### Canonicalisation + dedup (5)
- `TestChannelECanonical::test_idna_host_canonicalised`
- `TestChannelECanonical::test_trailing_slash_stripped`
- `TestChannelECanonical::test_host_case_folded`
- `TestChannelECanonical::test_duplicate_feed_url_dedup_keeps_first`
- `TestChannelECanonical::test_same_canonical_url_same_feed_or_adapter_id` — two `FeedSpec`s with different raw strings but same canonical URL produce identical `"rss:" + sha3_512(...)` ids.

### `feed_or_adapter_id` namespacing (3)
- `TestChannelENamespace::test_rss_prefix_asserted`
- `TestChannelENamespace::test_unprefixed_id_rejected`
- `TestChannelENamespace::test_candidate_channel_stamped_channel_e`

### Import-time hygiene (3)
- `TestChannelENoModuleSideEffects::test_import_opens_zero_fds_zero_nonces`
- `TestChannelENoModuleSideEffects::test_feedparser_not_imported_until_factory_called` — `sys.modules.pop("feedparser", None)` before import; assert `"feedparser" not in sys.modules` after `pipeline.scout.channel_e_rss` import.
- `TestChannelEKWOnly::test_positional_call_rejected`

### Cross-module (2)
- `TestSharedProtocolReuse::test_adapter_context_identity` — `AdapterContext` is the same class imported from Round 5.
- `TestSharedProtocolReuse::test_http_request_with_retries_identity` — same function object.

### AST-lint regression (2)
- `TestASTLintRegression::test_lint_channel_e_rss_clean`
- `TestASTLintRegression::test_lint_feedparser_adapter_clean`

### Public surface (5)
- `TestPublicSurface::test_version_pin_rN_ge_6` — E-025 range-check from start.
- `TestPublicSurface::test_discover_channel_e_reachable_via_pipeline_scout`
- `TestPublicSurface::test_f_scout_e_codes_match_blueprint`
- `TestPublicSurface::test_channel_e_constant_equals_E`
- `TestPublicSurface::test_reexports_include_feedspec_and_factory`

Total ≈ 69 tests in the base pass. Expect growth to 80–90 with coverage-gap fills (E-024 fourth firing is now a formal expectation). Coverage target 100% on `channel_e_rss.py` + `_feedparser_adapter.py`.

## Committee dispatch

**Self-LOCK eligible** on first clean single-cycle run **IFF** all three of:
(a) AST-lint green on `channel_e_rss.py` + `_feedparser_adapter.py`,
(b) coverage 100% on both,
(c) full suite green (current baseline: 2521 pass after Round 5).

Otherwise dispatch 5-family Code Thesis Committee per `router.yaml`. Retry-1 permitted per L-005; E-023 closure discipline applies (isomorphic-to-deferred-scope → honest test_adv_* docs, not re-dispatch).

Streaming-parser tests are likely to surface ordering subtleties (generator teardown on break, buffer-drain timing). Budget for one retry cycle.

## Done-definition

1. `pipeline/scout/channel_e_rss.py` written per surface above.
2. `pipeline/scout/_feedparser_adapter.py` written (single-file concrete factory; only place `import feedparser` appears).
3. `pipeline/scout/__init__.py` re-exports all Round-6 symbols + `__version__ = "0.1.0-scout-r6"`.
4. `pyproject.toml` adds `feedparser>=6.0` with comment block.
5. `tests/scout/test_round_6_channel_e_rss.py` — ≥ 69 tests across the classes above.
6. `scripts/run_tests.sh tests/scout/` green.
7. `scripts/run_tests.sh` full suite green (≥ 2521 baseline after Round 5).
8. `scripts/run_lint.sh` clean on both new modules.
9. Coverage = 100% on both new modules.
10. LOCK entry `project_impl_scout_round_6_locked.md` + MEMORY.md pointer.
11. Round 7 spec card pre-staged (`scout_round_7_channel_f_websearch.md`).

## Dependencies and timing

- **Unblocks:** Round 7 (Channel F web-search — reuses the same Protocols + adds BT12 pre-flight); Round 8 (VERIFY stage — consumes the union of all six channels' Candidate streams).
- **Blocked by:** Round 5 LOCK (done 2026-04-20).
- **Risk surface:** medium-high. The streaming-break invariant is the single most-attacked Scout behaviour in the Thesis Team history (A-05 / A-v3-08 / A-v4-01 / B-v5-04 — four successive closures). Getting the token-yield break point exactly right and the buffer-drain hasattr-dispatch exactly right is mandatory, not optional.
- **Out-of-scope surfaces** deferred to later rounds: `rss_watchlist.yaml` loader (Round 6 accepts a pre-loaded tuple); admin-risk health-tuple surface for `drain_api_missing` (wire into Round 2 `health_tuple` in a separate narrow-edit round if needed); Channel F web-search (Round 7).

## Pre-flight checklist

- [ ] Blueprint hash re-verified (`0a82d955f95b0fca`).
- [ ] Round 5 LOCK verified (`project_impl_scout_round_5_locked.md`).
- [ ] Round 1 constants checked — `CHANNEL_E_RUNAWAY_MAX = 100`, `RSS_STALE_FEED_DEGRADED_DAYS = 60`, `FEED_POLL_MIN_INTERVAL_MIN = 15`, `CHANNEL_E = "E"` all present (verified during pre-stage 2026-04-20).
- [ ] AdapterContext + http_request_with_retries reachable from `pipeline.scout` (verified — Round 5 re-exports).
- [ ] `feedparser` added to pyproject.toml and `scripts/run_tests.sh` still resolves a green venv after bump.
- [ ] E-025 version-pin range-check applied from the start (`rN >= 6`).
- [ ] E-024 E-026 reviewed — allocate test-surface budget at 1.5× spec-card ceiling; avoid `importlib.reload(module_under_test)` in adversarial tests.
- [ ] RED→GREEN cycle executed.
- [ ] Committee dispatch executed OR self-LOCK conditions (a+b+c) all met.
- [ ] LOCK entry + MEMORY.md pointer written.
- [ ] Round 7 spec card pre-staged (`pipeline/engineering/spec_cards/scout_round_7_channel_f_websearch.md`).
