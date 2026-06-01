# Spec card — pipeline.scout Round 8 (Capstone DISCOVER dispatcher — parallel six-channel fan-out)

**STATUS:** SELF-LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md`
  - §3.1 `pipeline.scout.__init__` public re-exports
  - §3.5 Surfaces offered to Section 5 (Pipeline)
  - §4.11 Scout run orchestration (lines 1017–1081) — **primary implementation target**
  - §4.10 M7 health-tuple assembly (already LOCKED Round 2) — consumed here via `assemble_and_sign_health_tuple`
  - §4.1–§4.6 per-channel `discover_channel_{a,b,c,d,e,f}` entry points — all LOCKED Rounds 3–7
  - §6.1–§6.6 per-channel failure code taxonomy — new capstone codes F-SCOUT-CAPSTONE-*
  - §7 property tests — parallel fan-out invariants, timeout discipline, channel-state aggregation
  - §8 constants — re-verify `SCOUT_CHANNEL_TIMEOUT_SECONDS = 120`, `SCOUT_MAX_WORKERS = 6`
  - `A-04` (CAP-04, candidate volume explosion) → global per-channel LOC cap enforced at DISCOVER-union boundary (already per-channel in Rounds 3–7)
  - Architecture line 270–271 (`backbone_failed` + `≥4/6 channel FAILED` hard-abort) — capstone records the facts; Section 4 Logician decides the abort
  - Autonomy Rule 1 (save state always) — `checkpoint(stage="discover_complete")` on BOTH success AND any channel exception
- Section 1 consumed surface: `Session`, `checkpoint`, `record_degradation`, `resume_or_discard` — LOCKED.
- Section 2 consumed surface: `vault_write` for run-log emission (via injected `VaultWriter` Protocol per E-017) — LOCKED.
- Rounds 1–7 consumed surfaces: All six `discover_channel_{a..f}` public entry points LOCKED. `ScoutRunResult` / `Candidate` / `SignedHealthTuple` frozen kw-only dataclasses LOCKED Round 1/2.
- Round 2 consumed: `assemble_and_sign_health_tuple(session, per_channel_states, per_channel_a_endpoints, run_wall_ns) -> SignedHealthTuple` LOCKED.

**Blueprint hash-at-card:** `0a82d955f95b0fca` (sha3_512(section_03_scout.md)[:16]) — identical to Rounds 1–7. Re-verify at build-time before Step 1.

**Spec-card version:** v1 (pre-staged 2026-04-20 on Round 7 LOCK close)

**Round:** Scout R8 of 11. Consumes ALL Rounds 1–7 primitives. This is the DISCOVER-stage capstone — the entry point Section 5 (Pipeline) invokes to obtain the candidate union + signed health tuple. **VERIFY (§4.7) and REVIEW (§4.8) and Entity Research (§4.9) remain scope for Rounds 9–11.**

---

## Summary

Land one module: `pipeline/scout/discover.py` — §4.11 capstone orchestrator. Parallel fan-out across six channels, union candidate collection, per-channel timeout + isolation, cross-channel dedup, health-tuple assembly + sign, quiesce on interrupt.

**Public surface:**

```python
def run_scout_discover(
    *,
    session: SessionLike,
    channel_fns: ChannelDispatchMap,   # injected — default binds to Rounds 3–7 public entries
    health_signer: HealthTupleSigner,  # injected — default binds to Round 2
    clock: ClockFn = _default_clock,
    executor_factory: ExecutorFactory = _default_executor_factory,
    interrupt_probe: InterruptProbe = _default_interrupt_probe,
    checkpoint_writer: CheckpointWriter,   # injected — Section 1 checkpoint
    degradation_writer: DegradationWriter, # injected — Section 1 record_degradation
) -> ScoutDiscoverResult: ...
```

Return: frozen kw_only dataclass `ScoutDiscoverResult(candidates: tuple[Candidate, ...], per_channel_states: Mapping[str, str], per_channel_a_endpoints: Mapping[str, str], signed_health: SignedHealthTuple, run_id: str, run_tiebreak_seed: bytes, run_wall_ns: int, capstone_degradation_events: tuple[CapstoneDegradationEvent, ...])`.

**Scope delimiter:** Round 8 does NOT invoke VERIFY. The DISCOVER union + signed health tuple is the handoff to Round 9 (VERIFY stage). `run_scout_discover_verify` (the §4.11 sketch combining DISCOVER+VERIFY+REVIEW) lands in Round 11 as the full Section-5-facing entry.

---

## Design decisions (operator-disposed 2026-04-20, reversible)

1. **`executor_factory` injected Protocol** (E-017 pattern, new Protocol) — returns a context-manager-compatible executor with `.submit(fn) -> Future` semantics. Default binds to `concurrent.futures.ThreadPoolExecutor(max_workers=_SCOUT_MAX_WORKERS)`. Tests inject a synchronous fake executor with deterministic scheduling to verify capstone behaviour without thread non-determinism.
2. **`channel_fns` injected dispatch map** — `ChannelDispatchMap = Mapping[Literal["A","B","C","D","E","F"], ChannelDiscoverCallable]`. Default binds to `{"A": discover_channel_a, …, "F": discover_channel_f}`. Tests inject fakes to exercise timeout / exception / state-aggregation paths without touching network.
3. **Per-channel hard timeout `SCOUT_CHANNEL_TIMEOUT_SECONDS = 120`** (pinned in §8) — `fut.result(timeout=120)`. Timeout → `per_channel_states[ch] = "FAILED"` + `F-SCOUT-CAPSTONE-01 ChannelTimeout` + ONE degradation event per timed-out channel. **No retry** — the six channels are parallel primaries; retry is channel-internal (Channel A retry ladder, etc).
4. **`run_wall_ns = clock.time_ns()` captured BEFORE executor spin-up** — written into `SignedHealthTuple` so capstone + health-tuple agree on run wall time. `clock.time_ns()` is used uniformly (not `time.time_ns()`) to allow freeze-time tests (E-017 reuse from Round 5/6).
5. **`run_tiebreak_seed = _fresh_urandom(16)` captured BEFORE executor spin-up** (A-v3-01 closure) — 128-bit per-run entropy, embedded in `SignedHealthTuple.run_entropy`. Consumed downstream by VERIFY tiebreak (Round 9). Generated by injected `EntropyFn` Protocol defaulting to `os.urandom`.
6. **`run_id` generated deterministically from `(session.session_id, run_wall_ns, run_tiebreak_seed)`** — `run_id = sha3_512(canonical(session_id|run_wall_ns|run_tiebreak_seed))[:16].hex()`. Reproducible if all three inputs match; unpredictable to attackers.
7. **Parallel fan-out via `submit` + `as_completed`-like gather** — but written as deterministic `for ch in ("A","B","C","D","E","F"): fut.result(timeout=…)` rather than `as_completed` iteration. Reason: `per_channel_states` iteration order determines degradation-event emission order, which is asserted against. Deterministic iteration avoids flaky event-order tests.
8. **Capstone isolates per-channel exceptions** — any channel raising `Exception` is caught, logged via `degradation_writer` with `F-SCOUT-CAPSTONE-02 ChannelException`, `per_channel_states[ch] = "FAILED"`, and Channel A's `per_channel_a_endpoints` gets `{ep: "FAILED" for ep in backbone_endpoints}`. Other channels continue. **`KeyboardInterrupt` / `SystemExit` re-raised** (not caught by `except Exception`).
9. **Cancellation on interrupt** (A-05 closure, reusing Section 1 `detect_interrupted`) — `interrupt_probe()` consulted between each `fut.result(…)` call. If interrupt signaled, cancel pending futures + write `checkpoint(stage="discover_interrupted", completed_channels=[…])` + raise `ScoutDiscoverInterrupted` (NOT `KeyboardInterrupt` — translated). Pipeline resumes per Section 1 resume discipline.
10. **`checkpoint_writer` (Autonomy Rule 1 — save state always)** — writes after every channel completes (success OR failure), with `stage="discover_channel_complete"`, `channel=ch`, `channel_state=per_channel_states[ch]`, `n_candidates_so_far=len(union)`. Final `stage="discover_complete"` checkpoint written before signed-health assembly.
11. **Cross-channel dedup by `candidate_id` union** — the six channels can independently surface the same opportunity (e.g. a Grants.gov record also appearing via a client-material web search). Union concatenation happens first; dedup by `candidate_id` with **first-writer-wins** per A→B→C→D→E→F ordering (deterministic). Duplicate hits emit `F-SCOUT-CAPSTONE-03 DuplicateCandidate` LOW events with source-channel pair.
12. **Global union cap `SCOUT_UNION_CAP = 6000`** (6 × 1000 per-channel) — if union exceeds cap, emit `F-SCOUT-CAPSTONE-04 UnionCapExceeded` MEDIUM event, truncate deterministically by `(channel, candidate_id)` ascending. Hard-cap the DISCOVER-stage output surface before VERIFY sees it. **VERIFY has its own `SCOUT_CANDIDATE_VERIFY_CAP = 1000`** (pinned in §8, consumed Round 9) — these are distinct caps.
13. **`SignedHealthTuple` assembly via injected `HealthTupleSigner` Protocol** (E-017) — default binds to `assemble_and_sign_health_tuple`. Tests inject deterministic signer to avoid real HMAC keystore access. Protocol returns frozen `SignedHealthTuple`.
14. **`backbone_failed` computed locally** — from `per_channel_a_endpoints` passed through `health_signer`. Capstone does NOT short-circuit on `backbone_failed` (architecture line 271 — Logician decides the abort, not Scout). Scout records the facts and still signs.
15. **Zero direct filesystem / vault calls** — all persistence through injected `checkpoint_writer` + `degradation_writer` + `health_signer` (which internally uses Section 2 `vault_write`). Capstone is stdlib-adjacent (+ Rounds 1–7 surface). `ast_lint` R3 `scout-no-direct-open` clean. `ast_lint` R1 `no-logician-import` clean. Lazy-import any third-party library.
16. **Zero `eval` / `exec` / `setattr` on operator decisions** — R4 + R5 AST-lint rules clean.
17. **Channel F opt-out does NOT propagate** — if Channel F short-circuits (opt-out, no policy file), `per_channel_states["F"] = "OK"` (trivial), zero candidates contributed. Capstone treats this identically to "Channel F ran and found nothing" — no special casing needed.
18. **Per-channel state taxonomy is the channel's, not the capstone's** — Channel B uses watermark-OK; Channel E uses `>50%` FAILED rule; etc. Capstone receives `channel_state: str` from each channel and folds it into `per_channel_states` without re-classification. The capstone's `F-SCOUT-CAPSTONE-*` codes cover CAPSTONE-INTRODUCED failures (timeout, exception, dedup, union-cap), not channel-internal failures.
19. **Public re-exports via `pipeline/scout/__init__.py` update** — `run_scout_discover`, `ScoutDiscoverResult`, `CapstoneDegradationEvent` added alongside Rounds 1–7 surface. **No breaking change** — Rounds 1–7 re-exports remain.

---

## Failure codes (capstone-introduced)

| Code | Raised when | State effect |
|------|-------------|--------------|
| F-SCOUT-CAPSTONE-01 | Channel dispatcher exceeds `SCOUT_CHANNEL_TIMEOUT_SECONDS` | `per_channel_states[ch] = "FAILED"` + HIGH event |
| F-SCOUT-CAPSTONE-02 | Channel dispatcher raises `Exception` (non-`BaseException`) | `per_channel_states[ch] = "FAILED"` + HIGH event |
| F-SCOUT-CAPSTONE-03 | Duplicate `candidate_id` across channels | LOW event (informational, deterministic first-writer-wins) |
| F-SCOUT-CAPSTONE-04 | Union cap `SCOUT_UNION_CAP = 6000` exceeded | MEDIUM event + deterministic truncation |
| F-SCOUT-CAPSTONE-05 | `interrupt_probe()` returns True mid-fan-out | Cancel pending + `ScoutDiscoverInterrupted` raised |
| F-SCOUT-CAPSTONE-06 | `health_signer` raises | FAILED capstone + re-raise (Section 1 signing invariant violated — not recoverable at capstone layer) |
| F-SCOUT-CAPSTONE-07 | `run_id` derivation produces non-16-hex-char output (invariant) | FAILED capstone + re-raise (programming error) |

---

## Constants to pin

Re-verify at build time against §8:
- `SCOUT_MAX_WORKERS = 6`
- `SCOUT_CHANNEL_TIMEOUT_SECONDS = 120`
- `SCOUT_UNION_CAP = 6000`
- Channel ordering `_CAPSTONE_CHANNEL_ORDER: Final[tuple[str, ...]] = ("A", "B", "C", "D", "E", "F")` (module-scope, literal-init, rebind-resistant)

---

## Minimum test surface (floor ≥ 70; expect ~105 given E-024 1.5× multiplier — sixth firing holds)

Must cover:

1. **`TestCapstoneHappyPath`** — all six channels OK, candidates unioned, `per_channel_states` populated, `signed_health` returned, `run_id` matches sha3_512 derivation, checkpoint written on completion.
2. **`TestCapstoneChannelTimeout`** — one channel exceeds 120s timeout → `per_channel_states[ch]="FAILED"` + F-SCOUT-CAPSTONE-01 event; other channels unaffected; capstone completes.
3. **`TestCapstoneChannelException`** — one channel raises `RuntimeError` → `per_channel_states[ch]="FAILED"` + F-SCOUT-CAPSTONE-02 event; Channel A exception also populates `per_channel_a_endpoints` with three "FAILED" entries.
4. **`TestCapstoneBackboneFailed`** — all three Channel A endpoints FAILED → `signed_health.backbone_failed is True`; capstone does NOT short-circuit (Logician decides).
5. **`TestCapstoneFourOfSixFailed`** — ≥4/6 channels FAILED → capstone still signs and returns; Logician hard-abort is downstream.
6. **`TestCapstoneInterrupt`** — `interrupt_probe()` returns True → `ScoutDiscoverInterrupted` raised; pending futures cancelled; interrupted checkpoint written.
7. **`TestCapstoneKeyboardInterruptPassthrough`** — `KeyboardInterrupt` from channel dispatcher re-raised (not caught by `except Exception`).
8. **`TestCapstoneDedup`** — two channels surface same `candidate_id` → first-writer-wins per A→…→F ordering; F-SCOUT-CAPSTONE-03 LOW event emitted with source-channel pair.
9. **`TestCapstoneUnionCap`** — union exceeds 6000 → deterministic truncation + F-SCOUT-CAPSTONE-04 MEDIUM event.
10. **`TestCapstoneRunIdDerivation`** — `run_id = sha3_512(canonical(session_id|run_wall_ns|run_tiebreak_seed))[:16].hex()` — deterministic given inputs; different inputs → different IDs; 16-hex-char output invariant enforced.
11. **`TestCapstoneRunTiebreakSeed`** — 128-bit seed embedded in `SignedHealthTuple.run_entropy`; `EntropyFn` injection honoured; two runs with same session_id but different seeds get different `run_id`.
12. **`TestCapstoneCheckpointDiscipline`** — checkpoint written BEFORE executor spin-up (`stage="discover_start"`), AFTER every channel completes (`stage="discover_channel_complete"`), AND at `stage="discover_complete"` before signed-health assembly.
13. **`TestCapstoneChannelOrderDeterministic`** — per-channel iteration order matches `_CAPSTONE_CHANNEL_ORDER` regardless of future completion order (rebind-resistant via `Final`).
14. **`TestCapstoneNoDirectVault`** — AST-lint R1/R2/R3 clean on `pipeline/scout/discover.py`; no `pipeline.vault` import at module scope; no `open(` call; no `setattr(` on operator decisions.
15. **`TestCapstoneChannelFOptOut`** — Channel F returns trivial OK (zero candidates, opt-out) → capstone treats identically to "ran and found nothing" (no special casing).
16. **`TestCapstoneKWOnly`** — positional call to `run_scout_discover` rejected.
17. **`TestCapstonePublicSurface`** — `__version__` range-check `rN ≥ 8` (E-025); `run_scout_discover` reachable via `pipeline.scout`; `ScoutDiscoverResult` + `CapstoneDegradationEvent` present.
18. **`TestCapstoneInjectedProtocols`** — `executor_factory` / `channel_fns` / `health_signer` / `checkpoint_writer` / `degradation_writer` / `interrupt_probe` / `clock` all honoured via injected fakes; default factories produce real-world bindings.
19. **`TestCapstoneStateAggregation`** — capstone does NOT re-classify per-channel state; receives channel's own state verdict verbatim; folds into `per_channel_states`.
20. **`TestCapstoneSharedProtocolReuse`** — `ClockFn` + `SessionLike` imported from Round 4 via `__module__` lineage check (E-026 formal).

**Adversarial (≥ 5):**
- `TestAdv_ChannelRaisesBaseException` — `except Exception` does not catch `BaseException`; re-raised.
- `TestAdv_InterruptBetweenChannels` — interrupt fires between channel B and C → B captured, C-F cancelled, interrupted checkpoint has `completed_channels=("A","B")`.
- `TestAdv_RunTiebreakSeedNot16Bytes` — `EntropyFn` returning wrong-length bytes raises on `SignedHealthTuple.run_entropy` assembly (F-SCOUT-V-06 from Round 9 spec; capstone's own invariant).
- `TestAdv_HealthSignerRaises` — `HealthTupleSigner` raises → F-SCOUT-CAPSTONE-06 + re-raise (capstone cannot recover from signing failure).
- `TestAdv_ExecutorFactoryReturnsBrokenExecutor` — executor whose `.submit` returns a future that never resolves and never times-out → 120s timeout fires deterministically via clock injection.

---

## Engineering risks to pre-flight

- **E-026 third-firing aftermath** — Round 7 showed full-suite `sys.modules` eviction cascades into downstream tests. Capstone imports from Rounds 1–7 breadth-first; import-hygiene test MUST use `__dict__` lineage inspection (E-026 formal) not `sys.modules` inspection.
- **Deterministic fake executor** — thread non-determinism in the real `ThreadPoolExecutor` makes channel-order tests flaky. Ship a `SequentialFakeExecutor` in test harness that runs submitted callables synchronously in submit-order; use it for all non-concurrency tests. Real `ThreadPoolExecutor` only exercised in `TestCapstoneHappyPath` + 1–2 integration tests.
- **Timeout testing** — clock injection must allow "advance clock past 120s without real wait". Use a `MockClock` with `.advance(seconds)` API; `_default_executor_factory`'s future-resolution is wrapped to consult the mock clock for timeout determination. Design the `ExecutorFactory` Protocol so the timeout signal can be injected without real `time.sleep(120)`.
- **Injected `CheckpointWriter` + `DegradationWriter` Protocols are new surfaces** — Round 2 `assemble_and_sign_health_tuple` already accepts an injected `VaultWriter`. Round 8 adds two more Section-1-facing Protocols. Document them in the module docstring as "capstone-specific seams; Section 5 Pipeline injects concrete bindings". E-017 sixth reuse (Round 8 introduces 3 new Protocols: `ExecutorFactory`, `EntropyFn`, `InterruptProbe` — plus reuses `SessionLike`, `ClockFn`, `VaultWriter` from earlier rounds).
- **`SCOUT_UNION_CAP` deterministic truncation tie-breaking** — when union hits exactly 6000, truncation is a no-op. Pre-flight test harness that exercises 5999 / 6000 / 6001 / 12000 candidate counts to exercise cap boundaries.
- **`run_tiebreak_seed` reproducibility** — the seed is captured BEFORE any channel runs and threaded through `SignedHealthTuple.run_entropy`. Post-run audit must be able to replay VERIFY tiebreak given (seed, candidate set, algorithm). Capstone's job is to generate + embed; replay is Round 9's job. Test: seed captured exactly once, embedded byte-identical.
- **Channel F opt-out short-circuit** — verify that a short-circuited Channel F (zero candidates, state="OK") contributes ZERO work to the union and emits ZERO capstone-level events (it's expected behaviour, not a failure mode).
- **No LLM calls in capstone** — the `_build_fit_rationale(session, cand, verdict)` bounded LLM call sketched in §4.11 line 1070 is **Round 11 scope** (alongside REVIEW stage). Round 8 capstone does NOT call LLMs.

---

## Lessons-applied-from-start

- **E-017** (injected-Protocol pattern) — all seven seams injected via Protocols: `ExecutorFactory`, `ChannelDispatchMap`, `HealthTupleSigner`, `CheckpointWriter`, `DegradationWriter`, `InterruptProbe`, `EntropyFn`, `ClockFn`. Defaults bind to production; tests inject fakes. **Seventh reuse.**
- **E-024** (1.5× multiplier, sixth firing held at R7) — spec-card floor ≥70 tests, expect ~105. Adversarial count ≥5 (Round 6/7 baseline). **Seventh firing — watch for multiplier drift.**
- **E-025** (range-check version pin) — `test_version_pin_rN_ge_8` via tuple comparison. **Applied from start.**
- **E-026** (sys.modules-reload fragility) — import-hygiene test inspects `pipeline.scout.discover.__dict__` lineage, not `sys.modules`. **Applied from start (fourth firing candidate).**
- **E-027 candidate** (`lint_tree` requires directory) — AST-lint regression tests copy module into `tmp_path` directory, never pass file-path singletons. **Applied from start.**
- **E-028 candidate** (`# pragma: no cover` for contract-unreachable defensive branches) — capstone has comparatively few defensive branches (most failure modes are testable); any that DO arise get pragma + docstring rationale. **Applied from start.**

---

## Rounds 9–11 roadmap (NOT this round's scope — for continuity)

- **Round 9:** `verify_stage.py` (§4.7) — VERIFIED_FIT / VERIFIED_NOT_FIT / UNVERIFIED / VERIFICATION_FAILED. Per-candidate `verify_candidate` + parallel `verify_all(max_workers=4)` with `SCOUT_CANDIDATE_VERIFY_CAP = 1000` + A-v3-01 per-run-seeded tiebreak (seed sourced from Round 8's `run_tiebreak_seed`).
- **Round 10:** `review_stage.py` (§4.8) + `entity_research.py` (§4.9 — M11 entity research pass + S11 dossier hardening). REVIEW enqueue only for `VERIFIED_FIT`; Scout never auto-files.
- **Round 11:** `run_scout_discover_verify(session) -> ScoutRunResult` (§4.11 capstone of capstones) — combines Round 8 DISCOVER + Round 9 VERIFY + Round 10 REVIEW + bounded LLM `_build_fit_rationale`. §3.5 Pipeline-facing entry point. Scout build COMPLETE.

---

## Spec-card version history

- **v1 (2026-04-20)** — pre-staged on Round 7 LOCK close. Operator-disposed decisions 1-19 above. Author: Midas (v2.1). Blueprint hash pinned `0a82d955f95b0fca`.
