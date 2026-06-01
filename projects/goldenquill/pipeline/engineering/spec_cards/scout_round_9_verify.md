# Spec card — pipeline.scout Round 9 (VERIFY stage — four-verdict per-candidate live-synopsis gate)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md`
  - §3.1 `pipeline.scout.__init__` public re-exports
  - §3.5 Surfaces offered to Section 5 (Pipeline)
  - §4.7 VERIFY stage (four-verdict taxonomy: VERIFIED_FIT / VERIFIED_NOT_FIT / UNVERIFIED / VERIFICATION_FAILED) — **primary implementation target**
  - §4.11 consumed — Round 8's `run_scout_discover` output is Round 9's input
  - §6.7 VERIFY failure codes — new codes `F-SCOUT-V-*`
  - §7 property tests — tiebreak determinism, cap-enforcement, verdict-distribution invariants
  - §8 constants — `SCOUT_CANDIDATE_VERIFY_CAP = 1000`, `SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO = 1.1`, `VERIFY_LIVE_SYNOPSIS_TIMEOUT_S`, `VERIFY_POOL_MAX_WORKERS = 4`
  - `A-v3-01` — secondary tiebreak when two candidates have identical primary sort key; tiebreak seed sourced from Round 8's `run_tiebreak_seed`
  - Architecture line 275–278 — VERIFY records facts (live-synopsis hash, live-fetch timestamp, verdict); Section 4 Logician decides admissibility
  - Autonomy Rule 1 — `checkpoint(stage="verify_candidate_complete")` on success AND failure per candidate
- Section 1 consumed surface: `Session`, `checkpoint`, `record_degradation` — LOCKED.
- Section 2 consumed surface: `vault_write` for per-candidate verify-log emission via injected `VaultWriter` — LOCKED.
- Round 1 consumed: `Candidate` + `VerificationVerdict` frozen kw-only dataclasses — LOCKED.
- Round 4/5/7 consumed: `HTTPClient` + `FDBroker` + `NonceRegistry` Protocols — LOCKED (reused under E-017 sixth/seventh cycle).
- Round 8 consumed: `ScoutDiscoverResult` (candidates + run_tiebreak_seed + run_id + run_wall_ns + signed_health) — LOCKED.

**Blueprint hash-at-card:** `0a82d955f95b0fca` (sha3_512(section_03_scout.md)[:16]) — identical to Rounds 1–8. Re-verify at build-time before Step 1.

**Spec-card version:** v1 (pre-staged 2026-04-21 on Round 8 LOCK close)

**Round:** Scout R9 of 11. Consumes Round 8's `ScoutDiscoverResult`. Emits per-candidate `VerificationVerdict` + aggregate verify-stage state. **REVIEW (§4.8) and Entity Research (§4.9) remain scope for Round 10; `run_scout_discover_verify` capstone remains Round 11.**

---

## Summary

Land one module: `pipeline/scout/verify_stage.py` — §4.7 VERIFY orchestrator. Per-candidate live-synopsis fetch + verdict-assignment, parallel dispatch across ≤4 workers, `SCOUT_CANDIDATE_VERIFY_CAP = 1000` input-cap with A-v3-01 secondary tiebreak, four-verdict taxonomy, Autonomy Rule 1 checkpoint discipline.

**Public surface:**

```python
def verify_candidate(
    *,
    session: SessionLike,
    candidate: Candidate,
    http: HTTPClient,                # E-017 reused from Round 4
    fd_broker: FDBroker,             # E-017 reused from Round 4
    nonce_registry: NonceRegistry,   # E-017 reused from Round 4
    clock: ClockFn,                  # E-017 reused
    synopsis_fetcher: SynopsisFetcher,   # NEW Protocol — per-candidate live-fetch
) -> VerificationVerdict: ...


def verify_all(
    *,
    session: SessionLike,
    discover_result: ScoutDiscoverResult,
    executor_factory: ExecutorFactory,     # E-017 reused from Round 8
    verify_fn: VerifyCandidateCallable = verify_candidate,   # injected for test fakes
    checkpoint_writer: CheckpointWriter,   # E-017 reused from Round 8
    degradation_writer: DegradationWriter, # E-017 reused from Round 8
    clock: ClockFn,
    entropy_fn: EntropyFn,                 # E-017 reused from Round 8 (unused here but threaded for future A-v3-01 extension)
) -> ScoutVerifyResult: ...
```

Return: frozen kw_only `ScoutVerifyResult(verdicts: Mapping[str, VerificationVerdict], per_candidate_fetch_states: Mapping[str, str], aggregate_state: str, cap_applied: bool, cap_degrade_ratio_crossed: bool, verify_degradation_events: tuple[VerifyDegradationEvent, ...])`.

**Scope delimiter:** Round 9 does NOT enqueue for REVIEW (that's Round 10). Round 9 does NOT dispatch `_build_fit_rationale` LLM calls (that's Round 11 §4.11 capstone-of-capstones). Round 9 does NOT modify the REVIEW queue; it only emits `VerificationVerdict` records.

---

## Design decisions (operator-disposed 2026-04-21, reversible — pre-staged, author Midas v2.1)

1. **Four-verdict taxonomy verbatim per §4.7 / Round 1 `VerificationVerdict` frozen kw-only dataclass.**
   - `VERIFIED_FIT` — live-synopsis fetched, LLM gate passed (deferred to Round 11), deadline in future, funder kind matches.
   - `VERIFIED_NOT_FIT` — live-synopsis fetched, funder kind mismatch OR deadline past OR obvious ineligibility.
   - `UNVERIFIED` — candidate has no live endpoint (Channel F-sourced or archived cache only); deterministic fallback, NOT a failure.
   - `VERIFICATION_FAILED` — fetch attempted and raised / timed out / returned non-2xx after retries. F-SCOUT-V-01 emitted.
2. **Per-candidate live-synopsis fetch under `VERIFY_LIVE_SYNOPSIS_TIMEOUT_S`** — timeout → `VERIFICATION_FAILED` + F-SCOUT-V-01. `HTTPClient` + `FDBroker` + `NonceRegistry` reused from Round 4 via E-017.
3. **`SynopsisFetcher` NEW Protocol (E-017 eighth firing)** — injected at `verify_candidate` boundary; default binds to an inline HTTP-fetch+parse helper; tests inject fakes.
4. **Parallel `verify_all` via injected `ExecutorFactory`** — reuses Round 8's `ExecutorFactory` Protocol verbatim (zero duplicate Protocol surface). Max workers bounded by `VERIFY_POOL_MAX_WORKERS = 4` (§8 pin).
5. **Input cap `SCOUT_CANDIDATE_VERIFY_CAP = 1000`** — if `len(discover_result.candidates) > 1000`, truncate deterministically and set `cap_applied=True`. Truncation order: primary by channel A→F, secondary by `candidate_id` ascending (lexicographic).
6. **A-v3-01 secondary tiebreak** — when two candidates share the same primary sort key (channel + candidate_id), consume Round 8's `discover_result.run_tiebreak_seed` for a deterministic-per-run HMAC-SHA3-512 of `candidate_id` to break the tie. Same seed across a run → same tiebreak; different seeds across runs → different tiebreaks. Pure-stdlib HMAC, no keystore.
7. **`SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO = 1.1`** — if `len(discover_result.candidates) > 1000 * 1.1 = 1100`, emit F-SCOUT-V-03 DEGRADED event (operator-signal that upstream DISCOVER is running hot). Below 1100 but above 1000 = silent truncation.
8. **Autonomy Rule 1 checkpoint discipline** — four landmarks: `verify_start`, `verify_candidate_complete` (per candidate on success AND failure), `verify_complete`, `verify_interrupted`.
9. **Per-candidate exception isolation** — `verify_candidate` raising `Exception` caught at `verify_all` boundary; emits F-SCOUT-V-02 + assigns `VERIFICATION_FAILED`; pool continues. KeyboardInterrupt / SystemExit re-raised as `ScoutVerifyInterrupted`.
10. **Aggregate state taxonomy** — `OK` if all candidates yielded `VERIFIED_*` (FIT or NOT_FIT); `DEGRADED` if any `UNVERIFIED` or `VERIFICATION_FAILED` present but <50%; `FAILED` if ≥50% `VERIFICATION_FAILED`.
11. **`UNVERIFIED` is deterministic, not a failure** — a candidate whose source is Channel F (web search, no live-synopsis endpoint) OR Channel B cache (archived, no live-endpoint) MUST resolve to `UNVERIFIED` without attempting a fetch. Tracked via a candidate attribute / source-channel inspection (spec-card deviation if schema needs amendment).
12. **No LLM calls** — the FIT/NOT_FIT gate inside VERIFY is structural only: deadline future, funder_kind match, jurisdiction allowed. LLM-based fit rationale is Round 11 scope. `F-SCOUT-V-04 StructuralFitMismatch` informational event on NOT_FIT.
13. **`checkpoint_writer` + `degradation_writer` reused from Round 8** — no new Protocol surface.
14. **Zero direct filesystem / vault calls** — all persistence through injected Protocols. AST-lint R1/R3 clean.
15. **Zero `eval` / `exec` / `setattr` on operator decisions** — R4/R5 clean.
16. **Public re-exports via `pipeline/scout/__init__.py`** — `verify_candidate`, `verify_all`, `ScoutVerifyResult`, `VerifyDegradationEvent`, `ScoutVerifyInterrupted`, `SynopsisFetcher`, `VerifyCandidateCallable`. Bump `__version__` to `0.1.0-scout-r9`. No breaking change to Rounds 1–8 surface.
17. **Seed-consumption boundary** — `verify_all` consumes `discover_result.run_tiebreak_seed` at input-cap-application time only. Pure-function HMAC derivation; no state mutation. Tests pin the seed byte-string + candidate list + observe deterministic truncation order.

---

## Failure codes (VERIFY-stage-introduced)

| Code | Raised when | State effect |
|------|-------------|--------------|
| F-SCOUT-V-01 | Live-synopsis fetch times out OR returns non-2xx after retries OR raises transport exception | `verdict = VERIFICATION_FAILED` + HIGH event |
| F-SCOUT-V-02 | `verify_candidate` raises `Exception` non-transport (programming error) | `verdict = VERIFICATION_FAILED` + HIGH event + pool continues |
| F-SCOUT-V-03 | Input-cap degrade ratio crossed (`len > 1000 * 1.1`) | MEDIUM DEGRADED event + truncation |
| F-SCOUT-V-04 | Structural FIT gate rejects candidate (deadline past / funder mismatch / jurisdiction) | INFORMATIONAL event; `verdict = VERIFIED_NOT_FIT` |
| F-SCOUT-V-05 | `interrupt_probe()` returns True mid-pool | Cancel pending + `ScoutVerifyInterrupted` raised |
| F-SCOUT-V-06 | `run_tiebreak_seed` not 16 bytes OR zero-length | FAILED verify + re-raise (Round 8 invariant violation at handoff boundary) |
| F-SCOUT-V-07 | Aggregate `VERIFICATION_FAILED` ratio ≥ 50% | `aggregate_state = "FAILED"` + HIGH event |

---

## Constants to pin

Re-verify at build time against §8:
- `SCOUT_CANDIDATE_VERIFY_CAP = 1000`
- `SCOUT_CANDIDATE_VERIFY_CAP_DEGRADE_RATIO = 1.1` (float, stored as `11/10` rational if float-determinism concerns arise)
- `VERIFY_LIVE_SYNOPSIS_TIMEOUT_S` (pinned; default 10s per §8)
- `VERIFY_POOL_MAX_WORKERS = 4`
- Per-verdict inline-literal strings in function bodies (rebind-resistant) — module-scope `Final[str]` already declared in `_constants.py` as `VERDICT_VERIFIED_FIT` / `VERDICT_VERIFIED_NOT_FIT` / `VERDICT_UNVERIFIED` / `VERDICT_VERIFICATION_FAILED`.

---

## Minimum test surface (floor ≥ 70; expect ~105 given E-024 multiplier)

Must cover:

1. **`TestVerifyCandidateVerifiedFit`** — live-synopsis fetched green, deadline future, funder matches → `VerificationVerdict(verdict=VERIFIED_FIT, ...)`.
2. **`TestVerifyCandidateVerifiedNotFit`** — fetched green, structural gate rejects → `VERIFIED_NOT_FIT` + F-SCOUT-V-04 event.
3. **`TestVerifyCandidateUnverified`** — Channel F-sourced candidate → `UNVERIFIED` without fetch attempted.
4. **`TestVerifyCandidateVerificationFailedTimeout`** — fetch exceeds `VERIFY_LIVE_SYNOPSIS_TIMEOUT_S` → `VERIFICATION_FAILED` + F-SCOUT-V-01.
5. **`TestVerifyCandidateVerificationFailedNon2xx`** — fetch returns 500 after retries → `VERIFICATION_FAILED` + F-SCOUT-V-01.
6. **`TestVerifyCandidateVerificationFailedTransport`** — connection reset → `VERIFICATION_FAILED` + F-SCOUT-V-01.
7. **`TestVerifyAllHappyPath`** — 10 candidates all VERIFIED_FIT, aggregate_state=OK, `verdicts` populated per `candidate_id`.
8. **`TestVerifyAllMixedVerdicts`** — some FIT / some NOT_FIT / some UNVERIFIED → aggregate_state=OK (no failures).
9. **`TestVerifyAllDegradedAggregate`** — one `VERIFICATION_FAILED` in 10 → aggregate_state=DEGRADED, no F-SCOUT-V-07.
10. **`TestVerifyAllFailedAggregate`** — 5/10 `VERIFICATION_FAILED` → aggregate_state=FAILED + F-SCOUT-V-07.
11. **`TestVerifyAllInputCapTruncation`** — 1001 candidates → 1000 verified, `cap_applied=True`, deterministic truncation.
12. **`TestVerifyAllInputCapDegradeRatio`** — 1101 candidates → 1000 verified, `cap_applied=True`, `cap_degrade_ratio_crossed=True` + F-SCOUT-V-03.
13. **`TestVerifyAllBelowDegradeRatio`** — 1050 candidates → silent truncation, no F-SCOUT-V-03.
14. **`TestVerifyAllTiebreakDeterministic`** — same seed + same candidates → same truncation order across two runs.
15. **`TestVerifyAllTiebreakDivergence`** — same candidates + different seeds → different truncation orders when ties exist.
16. **`TestVerifyAllCandidateExceptionIsolation`** — `verify_fn` raises → pool continues, `VERIFICATION_FAILED` assigned + F-SCOUT-V-02.
17. **`TestVerifyAllKeyboardInterruptPassthrough`** — `KeyboardInterrupt` from `verify_fn` re-raised via `ScoutVerifyInterrupted`.
18. **`TestVerifyAllCheckpointDiscipline`** — `verify_start` → `verify_candidate_complete` per candidate on BOTH success and failure → `verify_complete`.
19. **`TestVerifyAllInterruptBetweenCandidates`** — interrupt fires → pending cancelled + `verify_interrupted` checkpoint with `completed_candidate_ids`.
20. **`TestVerifyAllSeedInvariant`** — `run_tiebreak_seed` not 16 bytes → F-SCOUT-V-06 + re-raise before pool start.
21. **`TestVerifyAllDiscoverResultConsumption`** — `ScoutVerifyResult.verdicts` keyed by `candidate_id` matches Round 8's `discover_result.candidates` after truncation.
22. **`TestVerifyAllStructuralGateDeadline`** — candidate with deadline in past → `VERIFIED_NOT_FIT` + F-SCOUT-V-04.
23. **`TestVerifyAllStructuralGateFunderKind`** — candidate whose `funder_kind` is `FUNDER_UNKNOWN` → `VERIFIED_NOT_FIT` if session restricts to known kinds.
24. **`TestVerifyAllInjectedProtocols`** — all seven seams honoured via fakes; defaults produce real-world bindings.
25. **`TestVerifyAllKWOnly`** — positional call to `verify_all` rejected.
26. **`TestVerifyAllPublicSurface`** — `__version__` range-check `rN ≥ 9` (E-025); `verify_all` + `verify_candidate` + `ScoutVerifyResult` reachable via `pipeline.scout`.
27. **`TestVerifyAllNoDirectVault`** — AST-lint R1/R3/R4/R5 clean on `pipeline/scout/verify_stage.py`.

**Adversarial (≥ 5):**
- `TestAdv_SynopsisFetcherReturnsMalformed` — synopsis parser raises → `VERIFICATION_FAILED` + F-SCOUT-V-01.
- `TestAdv_TiebreakSeedConsumedExactlyOnce` — monkeypatch `hmac.new` to record calls; verify seed consumed once per `verify_all`, not per-candidate.
- `TestAdv_FetcherExceedsTimeoutByBigMargin` — synopsis fetch takes 60s against 10s timeout → times out deterministically via clock injection.
- `TestAdv_CandidateWithoutChannelAttribute` — malformed candidate → `VERIFICATION_FAILED` + F-SCOUT-V-02 (programming error path).
- `TestAdv_PoolRaisesBaseException` — `BaseException` from pool re-raised; not caught by `except Exception`.
- `TestAdv_SeedAllZeros` — seed is `b"\x00"*16` (possible but not reserved) → still valid, produces deterministic ordering with HMAC output.

---

## Engineering risks to pre-flight

- **HMAC-SHA3-512 tiebreak determinism** — the HMAC output is deterministic per (seed, candidate_id); tests pin exact byte expectations for 3-4 seed/candidate-id pairs to guard against silent algorithm drift.
- **`VERIFY_POOL_MAX_WORKERS = 4` vs `SCOUT_MAX_WORKERS = 6`** — VERIFY's worker pool is smaller than DISCOVER's because VERIFY is per-candidate (hundreds of fetches) vs DISCOVER's six-channel. Confirm both pins live in `_constants.py` with distinct names; no accidental reuse.
- **Structural FIT gate evolution** — Round 9's structural gate is minimal (deadline + funder kind + jurisdiction). Round 11 layers the LLM rationale on top. Spec card §4.7 may flex the gate boundaries; watch for blueprint divergence and file spec-card deviation notes early.
- **`SynopsisFetcher` Protocol vs `HTTPClient`** — the fetcher is higher-level than `HTTPClient` (it parses synopsis body + extracts verdict-relevant fields). Decide at build time whether to ship `SynopsisFetcher` as a wrapper around `HTTPClient` (keeping Round 4/5/7 Protocols intact) or as an independent Protocol layer. Prefer wrapper for Protocol-minimalism.
- **Channel source inspection for `UNVERIFIED`** — candidates' source channel is currently embedded in `feed_or_adapter_id` prefix (`channel_a_*`, `channel_b_cache_*`, `channel_f_websearch_*`). Parsing this string at verify time is fragile; prefer explicit `channel: Literal["A".."F"]` field if Round 1's `Candidate` dataclass has it. **Verify Round 1 schema at build-time.**
- **E-028 candidate second firing** — if Round 9 has defensive branches that are contract-unreachable (e.g. seed-length invariant), apply `# pragma: no cover` + docstring rationale. Second firing moves E-028 from candidate to formal.
- **No REVIEW enqueue** — Round 9 does NOT touch `ReviewQueueItem` / REVIEW queue. Only emits verdicts. Round 10 enqueues based on Round 9's output.

---

## Lessons-applied-from-start

- **E-017** (injected-Protocol pattern) — eight seams: `HTTPClient`/`FDBroker`/`NonceRegistry`/`ClockFn` reused from Round 4; `ExecutorFactory`/`CheckpointWriter`/`DegradationWriter`/`EntropyFn` reused from Round 8; `SynopsisFetcher` + `VerifyCandidateCallable` new. **Eighth firing in Scout.**
- **E-024** (1.5× multiplier) — spec-card floor ≥70 tests, expect ~105. Adversarial count ≥ 5. **Eighth firing.**
- **E-025** (range-check version pin) — `test_version_pin_rN_ge_9` via tuple comparison. **Applied from start.**
- **E-026** (sys.modules-reload fragility) — import-hygiene tests inspect `pipeline.scout.verify_stage.__dict__` lineage, not `sys.modules`. **Applied from start (fifth firing candidate).**
- **E-027 candidate** (`lint_tree` requires directory) — AST-lint regression tests always pass a directory root.
- **E-028 candidate** (`# pragma: no cover`) — any contract-unreachable defensive branch gets pragma + docstring rationale. Second firing moves E-028 from candidate to formal.

---

## Rounds 10–11 roadmap (NOT this round's scope — for continuity)

- **Round 10:** `review_stage.py` (§4.8) — `ReviewQueueItem` enqueue for each `VERIFIED_FIT` from Round 9. `entity_research.py` (§4.9 M11 entity research pass + S11 dossier hardening). Operator-facing REVIEW queue write via Section 2 `vault_write` + `DossierSignoff` signing.
- **Round 11:** `run_scout_discover_verify(session) -> ScoutRunResult` (§4.11 capstone-of-capstones) — composes Round 8 DISCOVER + Round 9 VERIFY + Round 10 REVIEW + bounded LLM `_build_fit_rationale(session, candidate, verdict)`. §3.5 Pipeline-facing entry. Scout build COMPLETE.

---

## Spec-card version history

- **v1 (2026-04-21)** — pre-staged on Round 8 LOCK close. Operator-disposed decisions 1–17 above. Author: Midas (v2.1). Blueprint hash pinned `0a82d955f95b0fca`.
