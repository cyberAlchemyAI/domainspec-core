# Spec card — §3 Scout Round 12 Capstone (§3 LOCKED-as-a-whole promotion)

**STATUS:** PRE-STAGED 2026-04-29 — awaiting Scout R11 capstone LOCK before dispatch

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md` v5 LOCKED 2026-04-17
- Principal sections: §5 Blueprint-tracked implementations (BT12 + S11a/b/c), §7 Test criteria (§7.1–§7.16 unit + integration + property + AST corpus), §9 Scout run sequence (15-step DISCOVER → VERIFY → health-sign → REVIEW)
- Supporting: every §4.* mechanism landed in R1–R11 (R1 types/constants, R2 health_tuple, R3 channel_b_cache, R4 channel_a_federal_apis, R5 channels_c_and_d, R6 channel_e_rss, R7 channel_f_websearch, R8 discover capstone, R9 verify_stage, R10 review_stage + entity_research, R11 run orchestrator)

**Architecture anchor:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 A1-A12 LOCKED 2026-04-19
**Spec-card version:** v1 (pre-staged at R10 SELF-LOCK + R11 dispatch staged 2026-04-21)
**Round:** §3 Round 12 — whole-section capstone (analog of §1 Round J / §2 Round K / §5 Round 13)
**Date:** 2026-04-29

**Depends on:** Rounds 1-11 all LOCKED (R11 = first §3 round to require committee — ends Scout's R3-R10 self-LOCK streak intentionally per `pipeline/handoffs/scout_round_11_capstone_dispatch_2026-04-21.md`). §1 Sovereignty Envelope LOCKED-as-a-whole via Round J. §2 Vault LOCKED-as-a-whole via Round K. §0.5 Interface Index v6 + v7 amendments LOCKED.

**Precedent rounds (in-section):** R1 types+constants (LOCKED-backfilled F-03) / R2 health_tuple (LOCKED) / R3 channel_b_cache (LOCKED) / R4 channel_a_federal_apis (LOCKED) / R5 channels_c_and_d (LOCKED) / R6 channel_e_rss (LOCKED) / R7 channel_f_websearch (LOCKED) / R8 discover capstone (LOCKED) / R9 verify_stage (LOCKED) / R10 review_stage + entity_research (LOCKED) / R11 run orchestrator (committee-LOCK pending).

**Precedent rounds (cross-section):** §1 Round J capstone (LOCKED 2026-04-21) + §2 Round K capstone (SELF-LOCKED 2026-04-22) + §5 Round 13 capstone (paste-ready 2026-04-21) — structural templates.

---

## Purpose

§3 Scout was built module-by-module across Rounds 1-11. Round 12 is the **integration capstone**: verify the eighteen §3 modules compose correctly as a six-channel discovery + verify + health-sign + review envelope; verify the §3-owned blueprint-tracked invariants (BT12 + S11a/b/c) hold end-to-end across DISCOVER, VERIFY, REVIEW, and entity-research lifecycles; verify the §7.16 AST red-team regression corpus holds module-set-wide; and package the `tests/scout/` test-suite discipline (`conftest.py` + `_integration` + `_bt_properties` + `_boot_sequence_property`) as the canonical §3 harness.

This round does NOT write new §3 code — it writes the cross-module test surface that promotes §3 from LOCKED-per-module (R1-R11 rows) to **LOCKED-as-a-whole-section** (R12 capstone verdict). Group 10 outside-audit consumes this surface as proof §3 is coherent.

## Scope

**§3-owned blueprint-tracked invariants** (per blueprint §5 lines 1082–1142). Round 12 writes property tests for all four:

- **BT12 — M11 Channel F domain pre-flight** (`channel_f_websearch.py` + `_channel_f_jurisdictions.py`). Default-deny opt-out; allowed-jurisdictions allowlist; per-org denylist override; DNS rebind detection; IDN homograph normalisation; FD release on every CFG exit path; AST-PREFLIGHT-DOMINATES-FD-REQUEST + literal-only `Final[bool]` initializer + cross-module imported-`Final[bool]` resolution + alias-walker termination guard (B-v5-01 / B-v5-02 / B-v5-03 closures).
- **S11a — Per-org source-domain allowlist** (`entity_research.py`). Empty default → every claim force-routes through full operator review; non-allowlisted domain → `force_full_review=True` metadata; AST-NO-INDIRECT-VAULT-READ alias-tracker enforcement.
- **S11b — Cross-domain diversity for HIGH confidence** (`entity_research.py`). Single-domain claims → tier MEDIUM; ≥2 distinct registrable domains → tier HIGH eligible.
- **S11c — Dossier lock verification** (`entity_research.py`). Canonical-path / inode / content-hash three-way binding; FD held across vault_write of sign-off record; final fstat catches mid-with-block swaps; strict `>` size cap at `_MAX_DOSSIER_BYTES = 5 MB`; F-SCOUT-D-01a/b/c/d sub-codes.

**§3-owned discipline lessons** (per §5.9–§5.12; tested as supplemental property/regression coverage, not separate BT classes): L-001 cache-fit-score ≠ elevation; L-002 path references not content dumps (self-discipline; AST-tested via §7.16 corpus); L-003 cross-family review (router-binding-tested); L-004 API key separation (consumer-note property only).

**Out of scope** (owned by other sections):
- BT1–BT4, BT6, BT8 → Section 1 (covered by §1 Round J capstone 2026-04-21).
- BT5 per-session provider quota / back-off → Section 5 (covered by §5 Round 13 capstone — pending).
- BT7 atomic claim-evidence sign-overwrite → Section 4.
- BT9 USER_DATA conversation-anchor integrity → Section 4.
- BT10 grep-check windowing → Section 4.
- BT11 cross-org dossier reference policy → Section 4 (R12 cross-references at K-style §3.2 boundary; no re-implementation).
- BT13 rails report signing → Section 4 (R12 verifies Scout signs only the raw 6-channel tuple, never a derived "overall OK" bit — §7.16 property already enforced; R12 promotes to cross-module composition test).
- BT14 mount-identity tuple → Section 2 (consumed via §3.3 frozen surface; R12 mocks at fixture layer per §2 Round K conftest precedent).

Round 12 touches §1 only through its existing §3.2 consumer surface (`Session`, `start_session`/`end_session`, `resolve_keystore()`, `KeyStore.retrieve()`, `sign_health_tuple`, `hmac_sha3_512`, `canonical_slug`, `within_org_root`, `canonical_path`, `record_admin_risk`, `record_degradation`, `checkpoint`/`detect_interrupted`/`resume_or_discard`, `hmac_audit_writer`, `atomic_flush`, `nonce_registry.reserve`). Touches §2 only through its §3.3 surface (`vault_read`, `research_db_read`, `vault_write`, `fd_broker.request_fd`/`release_fd`, `IdentityTuple`). §4 / §5 are not consumed at runtime — Round 12 is §3-internal composition; §5 entry point `run_scout_discover_verify_review` (R11) is exercised but not driven from §5's `run_pipeline`.

## Integration test surface (cross-module)

Round 12 tests exercise the full §3 public surface as a single start-to-review (DISCOVER → VERIFY → health-sign → REVIEW enqueue) lifecycle plus an operator-driven entity-research pass. Each test exercises ≥3 §3 modules in a single path; many exercise ≥6.

### 12.1 DISCOVER → VERIFY → health-sign → REVIEW lifecycle (calls all eighteen §3 modules end-to-end)

Per blueprint §9 — the 14-step Scout run sequence (with R11's `_build_fit_rationale` bounded LLM fan-out + entity-research composition boundary):

1. `start_session(envelope, rfa, project_context)` — §1 Sovereignty step (consumed as precondition; §1 Round J primitives).
2. `run_scout_discover_verify_review(session)` (§4.11 entry, R11 orchestrator).
3. Scout records `run_wall_ns` + computes deterministic `run_id`.
4. Scout submits 6 DISCOVER channel tasks to bounded 6-worker pool.
5. Per-channel state recorded as each future returns; degradation logged on raise; no channel failure aborts the union.
6. Checkpoint `discover_complete` written.
7. `verify_all(session, candidates)` — bounded 4-worker pool, per-candidate live fetch with 10s timeout; `SCOUT_CANDIDATE_VERIFY_CAP=1000` truncation by `fit_score_cached` desc with per-run-seeded tiebreak.
8. Checkpoint `verify_complete` written with verdict histogram.
9. `assemble_and_sign_health_tuple(session, per_channel, per_channel_a_endpoints, run_wall_ns)` — §1 HMAC.
10. Checkpoint `health_signed` written with `run_id`.
11. SignedHealthTuple JSON written via `vault_write` to per-run run-log.
12. Per `VERIFIED_FIT`: `_build_fit_rationale` (R11 bounded LLM ≤800 tokens, primary `ollama/mistral:7b` per `router.yaml`) → `enqueue_for_review`.
13. `ScoutRunResult` returned to Pipeline.
14. (Operator-driven, separate flow) `run_entity_research(session, roster, force_refresh=False)` — §4.9 dossier triple-lock with S11a/b/c enforcement.

Eight integration classes, one per cross-module composition family:

- **12.1.a** — Channel A (Federal APIs) integration: `channel_a_federal_apis` × `health_tuple` × `nonce_registry` (steps 4-5-9 with Channel A backbone). 3 endpoints × success/timeout/5xx matrix; `backbone_failed` correctness; nonce reservation/release per-attempt.
- **12.1.b** — Channel B (cache) integration: `channel_b_cache` × `vault_reader_adapter` × `IdentityTuple` (steps 4-5 with cache watermarks + identity-tuple verify). 14-day-watermark DEGRADED + S10a forbidden-org-key skip + cap-overflow truncation.
- **12.1.c** — Channels C+D (portals + program pages) integration: `channel_c_portals` × `channel_d_program_pages` × per-page caps (steps 4-5 with adapter registry + per-page-200 cap + per-adapter-500 cap). 3-of-5-adapters-FAILED → channel FAILED.
- **12.1.d** — Channel E (RSS) integration: `channel_e_rss` × `_feedparser_adapter` × runaway truncation (step 4 with `CHANNEL_E_RUNAWAY_MAX=100` break-iteration + `_drain_parser_buffer` API-drift fallback B-v5-04).
- **12.1.e** — Channel F (web search) integration: `channel_f_websearch` × `_channel_f_jurisdictions` × `fd_broker` (step 4 with BT12 default-deny + IDN normalisation + DNS rebind + FD release on every exit).
- **12.1.f** — VERIFY composition: `verify_stage` × `discover` × all 6 channels (step 7 with cache-CRITICAL flipped-by-live-NOT_FIT precedence; bounded 4-worker pool; `SCOUT_CANDIDATE_VERIFY_CAP=1000` deterministic truncation).
- **12.1.g** — Health-sign + checkpoint composition: `health_tuple` × Section-1 `sign_health_tuple` × `checkpoint` (steps 9-11 with run_id uniqueness under backward clock jump A-12).
- **12.1.h** — REVIEW + entity-research composition: `review_stage` × `entity_research` × dossier triple-lock (steps 12-14 with per-(slug, candidate_id) striped lock + force-full-review on non-allowlisted domain + dossier sign-off binding + Law 3 cross-org refusal).

Each integration class: ≥5 adversarial cases (inject Protocol raises at each layer; verify fail-closed propagates; verify no partial state leaks across the channel-dedup union; verify checkpoint landmarks land on success AND failure paths per Autonomy Rule 1).

**≥15 integration tests × 8 classes ≈ ≥30 integration test methods floor** (~60 with parametric expansion).

### 12.2 Per-BT property tests (≥12 per invariant; 4 BTs × 12 = ≥48 property tests floor)

**BT12 — Channel F domain pre-flight.** Property: every outbound URL on `opt_in=False` policy → `F-BT12-01`. Property: jurisdiction-mapping miss → `F-BT12-03` regardless of policy. Property: `_registrable_domain` normalises IDN via `idna.encode` Punycode before allowlist check (A-14 closure). Property: AST-PREFLIGHT-DOMINATES-FD-REQUEST guard accepts only literal-`Final[bool]` initializer (B-v5-01), recursively for cross-module imports bounded to `pipeline.scout.*` ∪ `pipeline.section_02.*` (B-v5-03), with alias-walker termination at `MAX_ALIAS_WALKER_STEPS=1000` (B-v5-02). Property: every `fd_broker.request_fd` rooted in Channel F is CFG-dominated by `_preflight_channel_f`. Adversarial: synthesize 4 module pairs with literal/runtime-derived/env-derived/cross-module-out-of-bounds initializers — verify each acceptance/rejection per refinement.

**S11a — Per-org source-domain allowlist.** Property: empty `source_domains.yaml` → every claim `force_full_review=True`. Property: claim from non-allowlisted registrable domain → `force_full_review=True`. Property: AST-NO-INDIRECT-VAULT-READ alias-tracker rejects (a) `getattr(vr, "__call__")(...)` where `vr` aliases `vault_read`; (b) `functools.partial(vr, ...)()`; (c) any `ast.Attribute` load on the alias other than `.__name__`/`.__module__`. Adversarial: synthesize three modules with `from pipeline.section_02 import vault_read as vr` / `import pipeline.section_02 as sec; vr = sec.vault_read` / `vault_read_direct = vault_read` — verify alias resolution + indirect-call rejection.

**S11b — Cross-domain diversity for HIGH.** Property: 5 claims all from `psu.edu` subdomains → tier MEDIUM (single registrable domain). Property: `psu.edu` + `nsf.gov` claims → tier HIGH eligible. Property: registrable-domain extraction normalises IDN homographs identically to BT12 path. Adversarial: claim corpus with 4 distinct subdomains under one eTLD+1 → MEDIUM (not HIGH); claim corpus with 2 distinct eTLD+1s → HIGH eligible.

**S11c — Dossier lock verification.** Property: `sign_off_dossier` reads `(canonical_path, inode, content_hash)` BEFORE writing the sign-off record (CFG analysis). Property: FD held across `vault_write` of sign-off (instrumentation hook records `fstat(fd).st_ino` at start and end of with-block). Property: `_MAX_DOSSIER_BYTES = 5 MB` strict-`>` enforcement (5 MB body succeeds; 5 MB + 1 byte → `F-SCOUT-D-02`). Property: AST-DOSSIER-SIGNOFF-FD-HELD enforces `vault_write(intent="dossier-signoff-write", ...)` is contained inside `with _open_dossier_body_fd(...) as fd:` scope (A-03 closure). Adversarial: symlink-swap fixture → `F-SCOUT-D-01a`; atomic rename swap → `F-SCOUT-D-01b`; body edit between read-and-signoff → `F-SCOUT-D-01c`; mid-with-block external rename → `F-SCOUT-D-01d`.

### 12.3 Full Scout-run parametric fuzz

Single harness: given a clean session, run `run_scout_discover_verify_review` N times with N distinct org slugs (N parametrized over `[2, 8, 16, 32]`). Verify:

- Every run produces a `ScoutRunResult(success=True, …)` with distinct `run_id`.
- Every run's `SignedHealthTuple` HMAC verifies against §1's per-session key.
- Every run's checkpoint chain (`discover_complete` → `verify_complete` → `health_signed`) terminates valid.
- No cross-org file access succeeds (Law 3 mechanical: org-A run cannot read `orgs/org-B/vault/`).
- Every run's `candidate_id` set is stable across re-runs given identical channel inputs (deterministic prefix derivation per §4.10 `run_tiebreak_seed`).
- VERIFY truncation at `SCOUT_CANDIDATE_VERIFY_CAP=1000` is deterministic across repeats given identical `fit_score_cached` ties.
- `_build_fit_rationale` is never called outside per-`VERIFIED_FIT` enqueue path (AST-NO-LLM-IN-VERIFY corpus check).
- `record_operator_decision` is the only writer of `operator_decision` (AST-NO-AUTO-FILE corpus check).

Counted as a single parameterized test class with ≥ N runs per parametrization = ≥ 58 individual test instances (matching §2 K.3 floor).

### 12.4 §7.16 AST red-team regression corpus (cross-module promotion)

The §7.16 corpus per blueprint lines 1359-1389 already enforces 25+ AST/property invariants per-module. R12 promotes the corpus to **module-set-wide** enforcement: every rule walks `pipeline.scout.**` (every file under the package), not just the canonical module per rule. This catches drift where a rule was authored against `entity_research.py` but a future module repeats the pattern.

**Cross-module AST corpus tests (≥12):**

- AST-NO-AUTO-FILE walks every Scout module for `Assign` to `operator_decision` outside `record_operator_decision` body.
- AST-NO-RAW-SOCKET walks every Scout module for `socket.socket(` outside `fd_broker` helpers.
- AST-NO-DIRECT-OPEN-VAULT walks every Scout module for `open(` on vault paths.
- AST-NO-LLM-IN-VERIFY walks `verify_stage.py` AND any module imported by `verify_stage.py` for LLM-provider imports.
- AST-NO-INDIRECT-VAULT-READ walks every Scout module with full alias tracker (B-v5-02 termination + B-v5-03 cross-module).
- AST-NO-EVAL-IN-SCOUT walks every Scout module for `eval`/`exec`/`compile`.
- AST-NO-SETATTR-OPERATOR-DECISION walks every Scout module for `setattr` / `object.__setattr__` / `ast.Attribute` store on `"operator_decision"`.
- AST-PREFLIGHT-DOMINATES-FD-REQUEST walks every Scout module for `fd_broker.request_fd(kind="https", ...)` calls and verifies CFG dominance by `_preflight_channel_f` with literal-`Final[bool]` guard discipline.
- AST-NONCE-RELEASE-ALWAYS walks `channel_a_federal_apis.py` for `nonce_registry.reserve` ↔ matching `release` on every CFG exit path.
- AST-FD-RELEASE-ALWAYS walks `channel_f_websearch.py` for `fd_broker.request_fd` ↔ matching `release_fd` on every CFG exit path.
- AST-DOSSIER-SIGNOFF-FD-HELD walks `entity_research.py` for `vault_write(intent="dossier-signoff-write", ...)` inside `with _open_dossier_body_fd(...) as fd:` scope.
- AST-RUN-ID-DERIVATION walks `health_tuple.py` for `os.urandom(8)` AND `time.monotonic_ns()` calls before `run_id` computation.

### 12.5 §7 test-suite packaging

The §3 test suite (per blueprint §7 scope definition) becomes the canonical §3 test harness. Round 12 packages:

- `tests/scout/conftest.py` — fixture library (clean session, operator keypair, sample 6-channel discovery corpus with parametrizable failure injection points, sample `EntityRosterEntry`, `CapstoneVaultReader` + `CapstoneFDBroker` stubs, `isolate_active_runtime`-equivalent seam, `SCOUT_CANDIDATE_VERIFY_CAP_OVERRIDE` monkeypatch helper).
- `tests/scout/test_section_3_integration.py` — 12.1 DISCOVER → VERIFY → health-sign → REVIEW + entity-research integration tests (eight classes 12.1.a–h).
- `tests/scout/test_section_3_bt_properties.py` — four §3-owned BT property test classes (BT12 + S11a + S11b + S11c, ≥12 each).
- `tests/scout/test_section_3_boot_sequence_property.py` — N-run parametric fuzz harness (12.3) + module-set-wide §7.16 AST corpus (12.4).

## Dependencies

- Rounds 1-11 all LOCKED on disk. R11 is committee-required (per `pipeline/handoffs/scout_round_11_capstone_dispatch_2026-04-21.md`) — **R12 does NOT dispatch until R11 is sealed.**
- §1 Round J capstone LOCKED 2026-04-21 — Round 12 consumes §1 primitives via the frozen §3.2 consumer surface.
- §2 Round K capstone SELF-LOCKED 2026-04-22 — Round 12 consumes §2 primitives via the frozen §3.3 consumer surface; `IdentityTuple` and FD-broker behaviour validated.
- §4 Logician runtime not consumed — Round 12 references admin-risk register write API as `record_admin_risk` mocked at fixture layer.
- §5 Pipeline runtime not consumed — Round 12 mocks `Session` at fixture layer; the R11 entry point is invoked directly without `run_pipeline` driving it.
- AST-lint R1-R7 clean on all four test files.
- `pyproject.toml` Python pin `>=3.11` + `.venv` 3.14 — run via `scripts/run_tests.sh` or `.venv/bin/python3 -m pytest`.

## Done definition

1. All 4 test files written with ≥48 property tests across the four §3-owned BTs (≥12 per BT) + ≥30 integration tests (12.1) + parametric fuzz harness (12.3) + ≥12 cross-module AST corpus tests (12.4).
2. ≥95% coverage on every §3 module via the union of per-round + cross-module tests; aggregate may report lower than per-round 100% baselines (§1 Round J precedent — coverage drift reported honestly).
3. AST-lint R1-R7 exit 0 on all four test files.
4. Full suite green (current baseline: ≥6219 pass per 2026-04-29 §7 Scribe R3 LOCK; Round 12 adds ≥120 tests → suite should clear 6339+).
5. Code Thesis Committee 5/5 PASS cycle-1 on the Round 12 capstone surface — OR self-LOCK per §1 Round J + §2 Round K + §3 Scout R5-R10 + §5 Pipeline R3-R12.B compositional-round precedent (test-only round composing already-LOCKED primitives; every consumed module has independent committee or self-LOCK on record). **Self-LOCK candidacy strong** — see §"Self-LOCK eligibility" below.
6. Operator signs — **§3 Scout capstone LOCKED-as-a-whole**. Promotes all of Section 3 from LOCKED-per-module to LOCKED-as-a-whole-section.
7. Canonical daily_log LOCK block per gate #12 discipline; §0.5 paired-commit rows (4 test files as Index entries); `lock_history.v1.jsonl` row with `lock_class: "code"`, `scope: "Section 3 capstone — integration + BT12+S11a+S11b+S11c property matrix + Scout-run parametric fuzz + module-set-wide §7.16 AST corpus + §7 test suite"`.
8. MEMORY.md prepend + `memory/project_impl_section_03_round_12_capstone_locked.md`; blueprint §3 v5 header status line amended to include "§3 LOCKED-as-a-whole 2026-04-YY".

## Test criteria

- 12.2: ≥12 property tests per BT × 4 BTs = **≥48 floor**.
- 12.1: ≥15 integration tests × 8 classes (composition families) with ≥5 adversarial cases each parametrically ≈ **≥30 integration test methods floor**.
- 12.3: parametric fuzz harness across N ∈ {2, 8, 16, 32} org slugs = **single parameterized class, ≥58 individual test instances**.
- 12.4: ≥12 cross-module AST corpus tests promoting §7.16 to module-set-wide.
- Total floor: **≥120 tests**. E-024 capstone-shape multiplier 1.3× target ≈ 156 tests. §1 Round J landed 214 tests at 1.26× over 170-floor; §2 Round K landed 230 tests at 1.53× over 150-floor. R12 honest target: ~150-170.
- E-026 formal: use `__module__` lineage checks, not identity, for any cross-module Protocol lineage assertion.
- VERIFY-cap RAM-safety: `monkeypatch.setattr(verify_stage_mod, "SCOUT_CANDIDATE_VERIFY_CAP", N)` for N ∈ {16, 64, 256} — keeps fuzz harness under 200 MB peak per §3 §8 8-GB-dev-target constraint.
- Deterministic hash ops: canonical bytes recipe `json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode("utf-8")` → SHA-3-512; no alternative encodings.
- `@dataclass(frozen=True, kw_only=True)` requirement — Python 3.10+; any `.venv` drift surfaced as collection-error per CLAUDE.md "Running tests — PINNED INTERPRETER".
- AST-walker test stubs use isolated synthetic modules (`tmp_path / "synth_<name>.py"` written + `ast.parse(path.read_text())`) — never monkey-patch `pipeline.scout` at runtime.

## Self-LOCK eligibility

Round 12 is **self-LOCK candidate** under the same precedent that admitted §1 Round J + §2 Round K + §5 Round 13:

- **Test-only round.** Zero new §3 production code. Pure cross-module test surface.
- **Every consumed module has independent LOCK on record.** R1-R10 self-LOCKed per Scout discipline streak (8 consecutive zero-committee-correction rounds). R11 will be committee-LOCKed before R12 dispatches. §1 + §2 LOCKED-as-a-whole. §0.5 + §4 + §5 dependencies LOCKED.
- **Stdlib + intra-package + already-LOCKED imports only.** No LLM, no network, no subprocess in the test files (R11's bounded LLM is exercised via stub provider at fixture boundary).
- **Compositional-round precedent.** §1 J SELF-LOCK (214 tests, 1.26× E-024). §2 K SELF-LOCK (230 tests, 1.53× E-024). §3 R8 SELF-LOCK (DISCOVER capstone). §5 R3-R12.B = 11 consecutive single-cycle SELF-LOCKs. R12 fits the pattern exactly.

**Three self-LOCK self-audit questions** (per §1 Round J + §2 Round K precedent — answer "no" to all three before self-LOCK):

1. **Does any test exercise a path that no per-round suite covered?** If yes, the underlying module has a coverage gap surfaced at composition time — escalate to per-module remediation cycle, not self-LOCK.
2. **Does any §7-invariant test reveal blueprint ambiguity?** If yes, the blueprint needs amendment, not the test — escalate.
3. **Does the AST-corpus module-set-wide promotion (12.4) catch any drift in already-LOCKED modules?** If yes, those modules need walk-back rows + remediation cycles before §3-as-whole can LOCK — escalate.

If all three answer "no", self-LOCK single-cycle.

Committee dispatch remains available if operator prefers belt-and-suspenders.

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Tests | `tests/scout/conftest.py` |
| Tests | `tests/scout/test_section_3_integration.py` |
| Tests | `tests/scout/test_section_3_bt_properties.py` |
| Tests | `tests/scout/test_section_3_boot_sequence_property.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` — Round 12 capstone row; `lock_class: "code"`; `scope: "Section 3 capstone — integration + BT12+S11a+S11b+S11c property matrix + Scout-run parametric fuzz + module-set-wide §7.16 AST corpus + §7 test suite"` |
| Blueprint | Update §3 v5 header status line to include "§3 LOCKED-as-a-whole 2026-04-YY" |
| Memory | `memory/project_impl_section_03_round_12_capstone_locked.md` + MEMORY.md prepend |
| Daily log | Canonical LOCK block per gate #12 (F-AMDT-12 seven required fields) |

## Coupling

- **Downstream unlock:** §3 Scout capstone LOCK-as-a-whole closes Phase 2 of the post-§7 LOCK roadmap (Phase 1 = §5 R13 + §4 Logician Group 7; Phase 2 = §3 Scout closure). Unblocks §10 Red Team blueprint Thesis round (parallel-safe with §8 Editor + §9 Judge once §3 + §5 + §4 are all LOCKED-as-a-whole) and Group 9 E2E integration rounds.
- **§1 Round J + §2 Round K precedent:** Round 12 mirrors both verbatim in shape; the `tests/scout/` directory receives the same four-file capstone layout. R11's `run_scout_discover_verify_review` is the §3 analog of §5's `run_pipeline` — exercised via fixture-bound `Session` without §5 pipeline driving it.
- **R11 inheritance:** Round 12 inherits R11's bounded-LLM `_build_fit_rationale` discipline as a structural test invariant — `verify_stage` must remain LLM-import-free; `_build_fit_rationale` is the only LLM call site outside `entity_research.py` extraction functions.
- **§7.16 corpus promotion:** Round 12's module-set-wide AST corpus is the strongest defence against pattern drift across future §3 maintenance (e.g., a v0.2 channel adapter that re-introduces a `setattr(item, "operator_decision", …)` shape).

---

*Spec card v1 — 2026-04-29 — §3 Scout Round 12 capstone. Promotes §3 LOCKED-per-module → LOCKED-as-a-whole-section. Pre-staged at R10 SELF-LOCK + R11 dispatch staged 2026-04-21. Dispatch when R11 closes — see `pipeline/handoffs/section_03_round_12_handoff_2026-04-29.md`.*
