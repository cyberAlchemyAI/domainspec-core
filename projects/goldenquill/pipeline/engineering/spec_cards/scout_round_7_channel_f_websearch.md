# Spec card — pipeline.scout Round 7 (Channel F — client-material-driven web search + BT12 pre-flight)

**STATUS:** SELF-LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md`
  - §4.6 Channel F full spec (lines 548–602) — `channel_f_websearch.py` implementation target
  - §5.1 BT12 M11 Channel F domain pre-flight (lines 1084–1092)
  - §6.6 (re-verify at build time) — `F-SCOUT-F-01..06` + `F-BT12-01..07` taxonomy
  - §7 unit/property tests — seed cases for preflight dominance, FD release discipline, Brave BYOK path
  - §8 constants — re-verify any Channel-F-specific constants
  - `A-v3-07` (RT-v2-MED-03) → new AST rule **`R7 AST-PREFLIGHT-DOMINATES-FD-REQUEST`** (ARCH-05 LOCKED — enforces CFG-dominance of `_preflight_channel_f` over every `fd_broker.request_fd` call in this module; `pipeline/scout/channel_f_*.py` is the scope specifically hard-coded for R7)
  - `A-06` (CRIT-06, FD leak on Channel F pre-flight failure) → §4.6 ordering: pre-flight → FD request → `try/finally` release on every exit; `F-SCOUT-F-04` reason-tag
  - `A-08` (MED-02, Channel F policy read bypasses vault) → §4.6 `_load_channel_f_policy` routes through `vault_read` with `intent="channel-f-policy-read"`; `F-BT12-05`
  - `A-14` (MED-08, IDN homograph bypass) → §4.6 `_registrable_domain` uses `idna.encode(host, uts46=True)` before eTLD+1; `F-BT12-06`
  - `A-v3-04` (CRIT-02 + MED-01) → post-`vault_read` strict-equality intent check via `_assert_intent_matches`; `F-BT12-07`
- Section 1 consumed surface: `SessionLike` — LOCKED.
- Section 2 consumed surface: `vault_read` (Round Q' LOCKED) — called via injected `VaultReader` Protocol for policy-file read + identity-tuple equality check.
- Round 4 consumed surface: `HTTPClient` + `HTTPResponse` Protocols + `FDBroker` + `NonceRegistry` + `ClockFn` — LOCKED.
- Round 5 consumed surface: `AdapterContext` + `http_request_with_retries` — LOCKED. Re-used verbatim; **do NOT redeclare.**
- Round 6 consumed surface: `rss:` prefix pattern (A-v3-09) is the per-channel analogue of Channel F's `websearch:` prefix.
- **NEW:** ARCH-05 R7 `AST-PREFLIGHT-DOMINATES-FD-REQUEST` — already LOCKED; this module is the first production consumer. The rule's scope is `pipeline/scout/channel_f_*.py`. It enforces CFG-dominance of a module-scope `Final[bool]` preflight sentinel (B-v5-01 literal init; B-v5-03 cross-module bounded-surface resolve) over every `fd_broker.request_fd` call. **Build-time must pass `scripts/run_lint.sh pipeline/scout/channel_f_websearch.py` with zero R7 violations.**

**Blueprint hash-at-card:** `0a82d955f95b0fca` (sha3_512(section_03_scout.md)[:16]) — identical to Rounds 1–6. Re-verify at build-time before Step 1.

**Spec-card version:** v1 (pre-staged 2026-04-20 on Round 6 LOCK close)

**Round:** Scout R7 of 11. Consumes Round 1 schemas + Round 5 `AdapterContext` / `http_request_with_retries` + Section 2 `vault_read` via injected Protocol. **First production consumer of ARCH-05 R7** AST rule.

---

## Summary

Land one module: `pipeline/scout/channel_f_websearch.py` — §4.6 client-material-driven web search dispatcher. **The only channel that runs LLM- or operator-initiated queries.** BT12 jurisdiction pre-flight gates every outbound fetch. Pre-flight strictly dominates every FD acquisition (AST-enforced at R7 lint).

**Two providers (policy-selected):**
- **Default:** SearxNG self-hosted on the Golden Quill. Localhost request (`127.0.0.1:searxng_port`). Does not leave the machine; SearxNG fetches upstream per its own meta-search config.
- **Fallback:** Brave Search API BYOK. Opt-in per `orgs/{slug}/scout/channel_f_policy.yaml`. Per-session operator disclosure required.

**Default-deny under BT12:** `opt_in=False` is the default. `allowed_jurisdictions=frozenset()` is the default. Unknown jurisdiction → reject. If `opt_in=False` or policy file absent: Scout does NOT call SearxNG at all. `channel_state = "OK"` trivially (no work attempted). Health tuple still records `channel_f="OK"` — the five other channels carry the DISCOVER union.

**Public surface:**

```python
def discover_channel_f(
    *,
    session: SessionLike,
    fd_broker: FDBroker,
    nonce_registry: NonceRegistry,
    http_client: HTTPClient,
    vault_reader: VaultReader,                # NEW Protocol — returns (bytes, IdentityTuple)
    query_plan: tuple[ChannelFQuery, ...],    # per-run operator-approved queries
    clock: ClockFn = _default_clock,
) -> ChannelFDiscoverResult: ...
```

Return: frozen kw_only dataclass —
`candidates: tuple[Candidate, ...]`, `channel_state: str`, `degradation_events: tuple[ChannelFDegradationEvent, ...]`, `disclosure_rows: tuple[ChannelFDisclosureRow, ...]`, `preflight_reject_count: int`.

Channel F does NOT contribute to `backbone_failed`. Its `channel_state` flows into Round 2 `health_tuple` as `channel_f`.

---

## Design decisions (operator-disposed 2026-04-20, reversible)

1. **Module-scope `_CHANNEL_F_PREFLIGHT_GATE: Final[bool] = True` sentinel** — required by ARCH-05 R7 rule. The R7 rule checks CFG-dominance of this sentinel over every `fd_broker.request_fd` call. Literal-init at module scope; NEVER reassigned.
2. **Pre-flight STRICTLY before FD request** (A-06 closure) — `_preflight_channel_f(session, candidate_url)` runs and returns (or raises) BEFORE any `fd_broker.request_fd(kind="https", host=...)` call. A raised `ChannelFNotOptedIn` / `ChannelFJurisdictionReject` / `ChannelFURLPunycodeError` exits the path with zero FDs held. **Second hop (click-through URL fetch) repeats pre-flight before the second FD.**
3. **`try/finally` FD release on every exit** (A-06 closure) — every `fd_broker.request_fd` is followed by `try: … finally: fd_broker.release_fd(fd)`. Path tags: `{success, fetch_error, parse_error, preflight_reject_after_acquire, exception}`. Exhaustive sequence of rejections cannot exhaust the FD pool (no FD held across rejection boundary).
4. **Policy file read via injected `VaultReader`** (A-08 closure) — `_load_channel_f_policy(session, vault_reader)` calls `vault_reader.vault_read(path=f"orgs/{session.slug}/scout/channel_f_policy.yaml", intent="channel-f-policy-read", session_id=session.session_id, slug=session.slug)`. Direct filesystem open forbidden (Scout PRE-gate + AST-lint R3 catches). E-017 pattern.
5. **Post-`vault_read` intent equality check** (A-v3-04 closure) — `_assert_intent_matches(identity, expected="channel-f-policy-read")` after NFC normalisation + whitespace strip. Deviation → `F-BT12-07 IntentMismatchPostRead`; fail-closed (Channel F stays OK-trivial for run).
6. **Intent string declared `Final[str]`** (A-v3-04 static check) — `_INTENT_CHANNEL_F_POLICY_READ: Final[str] = "channel-f-policy-read"`. Call-site and contract intent are both sourced from this literal.
7. **`_registrable_domain` uses Punycode / UTS46** (A-14 closure) — `idna.encode(host, uts46=True).decode("ascii")` before eTLD+1 extraction via the statically compiled jurisdiction table shipped with the package. Denylist + allowlist comparisons happen exclusively in Punycode form. IDN homograph (Cyrillic `а` vs Latin `a`) cannot slip. `idna.IDNAError` → `F-BT12-06 ChannelFURLPunycodeError` (reject as default-deny).
8. **Statically compiled jurisdiction table** — ship as `pipeline/scout/_channel_f_jurisdictions.py` with a frozen `MappingProxyType[str, str]` (eTLD → ISO country code). No lazy loading. Unknown eTLD → jurisdiction=None → reject per BT12.
9. **SearxNG first-hop FD:** `kind="https"`, `host="127.0.0.1"`, `port=policy.searxng_port`. Second-hop FDs go to resolved click-through hosts (each with its own pre-flight).
10. **Brave BYOK first-hop FD:** `kind="https"`, `host="api.search.brave.com"`. Requires `opt_in=True` AND `BRAVE-BYOK` in `allowed_jurisdictions` (US by default, operator-configurable).
11. **Per-session disclosure row per outbound hop** — each `request_fd` call emits a `ChannelFDisclosureRow(domain=..., count=1, hop="first"|"click_through", timestamp_utc=...)`. Aggregate `disclosure_rows` returned in `ChannelFDiscoverResult`. Section 5 downstream writes to `orgs/{slug}/scout/run_log/{run_id}.channel_f.jsonl` — Round 7 does NOT write the file (scope delimiter).
12. **`disclosure_rows` carry domain + count ONLY** — no query text, no body excerpt. Per §4.6 line 598. Operator-visible via rails report.
13. **Content-body sha3_512 hashing** — every fetched body gets hashed into the Candidate's `content_hash`. Body bytes NEVER retained past Candidate construction.
14. **Channel state rule** (§4.6 line 600) —
    - Pre-flight + fetch succeeded on every attempted request → OK
    - Any fetch failed POST pre-flight → DEGRADED
    - SearxNG (or Brave, when opted in) unreachable at all → FAILED
    - **Pre-flight rejections do NOT flip channel state** — expected outcomes, logged as admin-risk `LOW` entries
15. **Opt-out short-circuit** (§4.6 line 602) — if `vault_read` returns FileNotFound OR `policy.opt_in is False`: skip ALL Channel F work. Return `ChannelFDiscoverResult(candidates=(), channel_state="OK", degradation_events=(), disclosure_rows=(), preflight_reject_count=0)`. No FDs requested. No nonces reserved.
16. **Channel-F `feed_or_adapter_id` prefix** — A-v3-09 analogue: `websearch:{provider}:{sha3_512(canonical_search_url)[:16]}` where provider ∈ `{"searxng", "brave"}`. Asserted by `_build_channel_f_candidate`.
17. **`ChannelFQuery` input shape** — frozen kw_only dataclass `ChannelFQuery(query_text: str, max_results: int = 10, hydrate_clickthrough: bool = False)`. The dispatcher does NOT construct queries itself — it receives an operator-approved plan. Query construction is Scribe/operator responsibility.
18. **No retry on Channel F** — policy decision. BT12 rejections are terminal. Fetch failures are terminal (single try). Retrying invites rate-limiting from SearxNG meta-search engines. Document rationale in module docstring.

---

## Failure codes

| Code | Raised when | State effect |
|------|-------------|--------------|
| F-BT12-01 | `policy.opt_in is False` | Channel F opt-out short-circuit (state OK-trivial) |
| F-BT12-02 | Domain on per-org `disallowed_registrable_domains` | Pre-flight reject (state unchanged) |
| F-BT12-03 | Domain has no known jurisdiction | Pre-flight reject (default-deny, state unchanged) |
| F-BT12-04 | Domain jurisdiction not in `allowed_jurisdictions` | Pre-flight reject (state unchanged) |
| F-BT12-05 | `vault_read` returns malformed / identity-tuple mismatch | Fail-closed (state OK-trivial; no traffic) |
| F-BT12-06 | URL fails `idna.encode(host, uts46=True)` | Pre-flight reject (state unchanged) |
| F-BT12-07 | Post-`vault_read` intent string deviates after NFC+strip normalisation | Fail-closed (state OK-trivial; no traffic) |
| F-SCOUT-F-01 | Fetch failed POST pre-flight (HTTP 4xx/5xx / timeout / connection error) | DEGRADED + MEDIUM event |
| F-SCOUT-F-02 | SearxNG (or Brave, when opted in) unreachable on first-hop | FAILED + HIGH event |
| F-SCOUT-F-03 | Result parse error (JSON decode / schema mismatch) | DEGRADED + MEDIUM event |
| F-SCOUT-F-04 | FD release path tag (informational, every release) | LOW event |
| F-SCOUT-F-05 | `vault_reader.vault_read` raises before identity check | FAILED + HIGH event |
| F-SCOUT-F-06 | Content-body hash mismatch on secondary validation (future-proofing) | DEGRADED + MEDIUM event |

---

## Constants to pin

Re-verify at build time:
- `CHANNEL_F = "F"`
- `FEED_PREFIX_WEBSEARCH = "websearch:"` (A-v3-09 analogue)
- `_INTENT_CHANNEL_F_POLICY_READ: Final[str] = "channel-f-policy-read"`
- `_CHANNEL_F_PREFLIGHT_GATE: Final[bool] = True` (ARCH-05 R7 sentinel)
- `_CHANNEL_F_MAX_RESULTS_PER_QUERY = 10` (default; policy can lower)
- `_CHANNEL_F_MAX_QUERIES_PER_RUN = 5` (operator can lower via query_plan size)

---

## Minimum test surface (floor ≥ 60; expect ~90 given E-024 1.5× multiplier)

Must cover:

1. **`TestChannelFOptOut`** — policy `opt_in=False` short-circuits (zero FDs, zero nonces, channel_state OK); missing policy file short-circuits; stale policy file (identity-tuple mismatch) fail-closed; F-BT12-05 tagged on malformed vault_read return.
2. **`TestChannelFPreflightDominance`** — pre-flight strictly before every `request_fd` (observed via counting broker); pre-flight reject → zero FDs held; click-through pre-flight repeated before second FD.
3. **`TestChannelFBT12Rules`** — F-BT12-01 opt-out; F-BT12-02 denylist; F-BT12-03 unknown jurisdiction; F-BT12-04 jurisdiction not allowed; F-BT12-06 Punycode error; F-BT12-07 intent mismatch after NFC drift.
4. **`TestChannelFIDNHomograph`** — Cyrillic-`а` vs Latin-`a` distinct in Punycode; `xn--80aaa...` denylist hit works; mixed-script host rejected.
5. **`TestChannelFFDLifecycle`** — FD released on success, fetch_error, parse_error, preflight_reject_after_acquire, exception; nonce released on every path; FD before nonce on release.
6. **`TestChannelFSearxNGPath`** — happy single-query single-result; localhost FD host/port shape; second-hop FD to resolved URL; disclosure row per hop.
7. **`TestChannelFBravePath`** — BYOK requires opt_in=True + BRAVE-BYOK in allowed_jurisdictions; otherwise F-BT12-04 reject; first-hop FD to `api.search.brave.com`.
8. **`TestChannelFStateAggregation`** — OK (all succeeded); DEGRADED (any fetch failed post pre-flight); FAILED (SearxNG unreachable first-hop); **pre-flight rejections DO NOT flip state** (state remains OK if all other work succeeded).
9. **`TestChannelFDisclosureRows`** — domain + count only (NO query text, NO body excerpt); one row per outbound hop; timestamp_utc populated from injected clock.
10. **`TestChannelFNoModuleSideEffects`** — import opens zero FDs, zero nonces, zero vault reads; jurisdiction table is frozen `MappingProxyType`.
11. **`TestChannelFKWOnly`** — positional call to `discover_channel_f` rejected.
12. **`TestASTLintRegression`** — `lint_tree(pipeline/scout/channel_f_websearch.py, DEFAULT_RULES)` clean; **R7 dominance assertion specifically verified** (inject a synthetic copy with a `request_fd` NOT dominated by the preflight gate → R7 violation raised).
13. **`TestPublicSurface`** — `__version__` range-check `rN ≥ 7` (E-025); `discover_channel_f` reachable via `pipeline.scout`; F-BT12-* + F-SCOUT-F-* codes present.
14. **`TestSharedProtocolReuse`** — `AdapterContext` + `http_request_with_retries` imported from `channel_c_portals` (`__module__` lineage check per E-026 formal).
15. **`TestChannelFContentHashing`** — every fetched body sha3_512 hashed into `Candidate.content_hash`; body bytes NOT retained in Candidate or event.

---

## Engineering risks to pre-flight

- **ARCH-05 R7 is production-fresh** — Round 7 is the first module to exercise R7 in production. If R7 raises a false positive against a perfectly safe dominance pattern, we hit the rule with well-scoped code and can refine the rule (or the code). Budget 1 cycle of R7 tuning if needed.
- **BT12 statically-compiled jurisdiction table** — table coverage is load-bearing. Ship with eTLD entries for all ISO country-code TLDs + gTLDs that Scout plausibly sees. Unknown eTLD reject is the correct default, but a sparse table increases false-positive rejects. Aim for ≥ 250 entries.
- **Disclosure-row sensitivity** — NEVER include query text. NEVER include body excerpt. The BT12 threat model explicitly guards against exfiltration via disclosure. R3 AST-lint check (`no direct file I/O`) catches the most obvious path. Add a test that feeds distinctive query text and confirms it does NOT appear in any disclosure_row.
- **Injected `VaultReader` Protocol is new** — Round 7 is the first Scout round to consume Section 2's `vault_read` in production. Use the E-017 pattern: Protocol declared in `channel_f_websearch.py`, concrete `Section2VaultReader` stub lives in a sibling `_vault_reader_adapter.py` (pattern mirror of Round 6's `_feedparser_adapter.py`). Keep `channel_f_websearch.py` stdlib-adjacent + Section-2-injected.

---

## Spec-card version history

- **v1 (2026-04-20)** — pre-staged on Round 6 LOCK close. Operator-disposed decisions 1-18 above. Author: Midas. Blueprint hash pinned `0a82d955f95b0fca`.
