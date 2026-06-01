# Spec card — §5 Pipeline Orchestrator Round 13 Capstone (§5 LOCKED-as-a-whole promotion)

**STATUS:** PRE-STAGED 2026-04-21 at §5 Round 12.B SELF-LOCK — awaiting operator review before dispatch

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal sections: §7 Invariants (v2 carries v1 §7.1-§7.9; v4 adds §7.13/§7.14/§7.15; v5 addenda §7.15-freshness + §7.16 canonical-bytes exhaustiveness), §9 Tests (§9.1 unit / §9.2 integration / §9.3 property / §9.5 failure-injection / §9.6 cron)
- Supporting: every §4.* mechanism landed in R1-R12.B (entry points: §4.1 submission-mode `run_pipeline`, §4.15 eval-mode `run_eval_pipeline`)

**Architecture anchor:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 A1-A12 LOCKED 2026-04-19
**Blueprint hash-at-card:** `34ef007f3ab6d59d` (unchanged since §5 v6 LOCK)

**Spec-card version:** v1 (pre-staged at R12.B SELF-LOCK)
**Round:** §5 Round 13 — whole-section capstone (analog of §1 Round J)
**Depends on:** Rounds 1-12.B all LOCKED. §1 Sovereignty Envelope (LOCKED-as-a-whole via Round J). §2 Vault v7.1 (LOCKED). §4 Logician v2.1 + v2.2 (LOCKED). §0.5 Blueprint Interface Index v4 (LOCKED). Ed25519 reference signer from R12.A.

**Precedent rounds (in-section):** R1 foundations (LOCKED) / R2 state_checkpoint (LOCKED) / R3 run_lifecycle (LOCKED) / R4 seat_runner (LOCKED) / R5 revision_loop (LOCKED) / R6 post_gate_runner (LOCKED) / R7 rate_limiter (LOCKED) / R8 cascade (LOCKED) / R9 tab_delivery (LOCKED) / R10 cron_scheduler (LOCKED) / R11 run_pipeline (LOCKED) / R12.A calibration package (LOCKED) / R12.B run_eval_pipeline (LOCKED).

**Precedent rounds (cross-section):** §1 Round J capstone (LOCKED 2026-04-21) — structural template; §3 Scout R8 DISCOVER capstone (LOCKED) — capstone-composition self-LOCK precedent.

---

## Purpose

§5 was built module-by-module across Rounds 1-12.B. Round 13 is the **integration capstone**: verify the thirteen §5 modules compose correctly as a pipeline orchestrator; verify the §7 invariants (§7.1-§7.16) hold end-to-end across submission-mode and eval-mode lifecycles; verify BT5 (per-session provider quota / back-off) holds under fuzz; and package the §9 test-suite discipline (§9.1 unit / §9.2 integration / §9.3 property / §9.5 failure-injection / §9.6 cron) as the canonical §5 harness.

This round does NOT write new §5 code — it writes the cross-module test surface that promotes §5 from LOCKED-per-module (R1-R12.B) to **LOCKED-as-a-whole-section** (R13 capstone verdict). Group 10 outside-audit consumes this surface as proof §5 is coherent.

## Scope

**§5-owned invariants** (per blueprint §7): §7.10 resume guard (F-PIPE-18), §7.11 iterations append-only (F-PIPE-19), §7.12 Cedar-decision presence (F-PIPE-20), §7.13 mode-isolation (F-PIPE-21), §7.14 eval-mode org-isolation (F-EVAL-CROSS-ORG-READ routed to F-PIPE state-failure), §7.15 CalibrationReport non-exportability + verify-time freshness (F-PIPE-21.calibration_signature_stale), §7.16 canonical-bytes exhaustiveness (§5.6.4 exclusion table). R13 writes property tests for these seven.

**§5-owned architecture BT** (per §1 Round J spec card line 24): **BT5 per-session provider quota / back-off**. R13 writes ≥12 property tests for BT5 under the same J.2-style structure.

**Not in scope (owned elsewhere, referenced only):**
- BT1/BT2/BT3/BT4/BT6/BT8 → Section 1 (Round J covers).
- BT7 atomic claim-evidence sign-overwrite → Section 4.
- BT9 USER_DATA conversation-anchor integrity → Section 4.
- BT10 grep-check windowing → Section 4.
- BT11 cross-org dossier reference policy → Section 4.
- BT12 Channel F domain preflight → Section 3.
- BT13 rails-report signing → Section 4. (§5 consumes BT13 at §7.15; R13 cross-references but does not re-implement.)
- BT14 mount-identity tuple → Section 2.

Cross-section BTs consumed by §5 invariants (BT13 in §7.15) are exercised via §4 Logician's public surface + §1's `within_org_root`; no re-implementation.

## Integration test surface (cross-module)

Round 13 tests exercise the full §5 public surface as a single start-to-tab (submission) or start-to-signed-report (eval) lifecycle. Each test exercises ≥3 §5 modules in a single path; many exercise ≥6.

### J.1 Submission-mode lifecycle (R1-R11 end-to-end)

11-phase RunState trajectory per R11's capstone walk — `initialized` → `pre_gate_pending` → `pre_gate_passed` → `inner_loop_iter_{1..3}` → `post_gate_pending` → `post_gate_passed` → `signoff_pending` → `report_signed` → `tabs_delivered`.

- `config` + `errors` + `types` (R1) — primitive dataclasses instantiated at module boundary.
- `state_checkpoint` (R2) — CAS-head capture + atomic write at every transition.
- `run_lifecycle` (R3) — `start_run` + `resume_run` paths covered (fresh boot + mid-run resume).
- `seat_runner` (R4) — scribe / editor / judge subprocess invocation; minimal-env; tuple return.
- `revision_loop` (R5) — MAX_REVISION_ITERATIONS=3 ceiling; interrupt-probe; first-fail-second-pass revision path.
- `post_gate_runner` (R6) — §4 Logician v2.2 POST-gate composition; `PostGateRejected` soft-return.
- `rate_limiter` (R7) — vault-CAS TokenBucket reserve / release / can_reserve under lease TTL.
- `cascade` (R8) — live landed-family + can_reserve probe; cross-family rigor pin.
- `tab_delivery` (R9) — three-tab envelope assembly + signing; F-PIPE-21 eval-shield entry-assertion.
- `cron_scheduler` (R10) — flock + vault-stamp two-layer dedupe; `fire_once` wrapping `run_pipeline`.
- `run_pipeline` (R11) — 11-step orchestrator composing R1-R10.

Each integration test: ≥5 adversarial cases per class (inject Protocol raises at each layer; verify fail-closed propagates; verify no partial state leaks; verify checkpoint cadence pin holds).

### J.2 Eval-mode lifecycle (R12.A + R12.B + R1-R7 reuse)

Per-item loop over golden-set manifest → per-item `run_inner_loop` (R5) reuse → per-item `run_post_gate_orchestration` (R6) reuse → `CalibrationReport.assemble_from_run` (R12.A) → `sign_report` (R12.A) → `reconcile_operator_pubkey` (R12.A) → final `eval_finalized` phase.

Boundary tests:
- Eval-mode cannot reach `deliver_tab` (R9 entry-assertion + R12.B's structural non-call).
- Submission-mode cannot write under `golden-set-*` intent.
- Operator-refuses-to-sign path (aborted_operator, recoverable).
- Resume semantics per-item (crash after item K of N; resume picks up at K+1 via sidecar progress file).

### J.3 Per-invariant property tests (≥12 per invariant; 7 invariants × 12 = ≥84 property tests floor)

**§7.10 — Resume guard.** Property: `resume_run` refuses to re-enter at `post_gate_passed` (would skip sign-off) or `tabs_delivered` (would skip everything). F-PIPE-18 raised. Property: resume at every legal phase (pre_gate_pending / pre_gate_passed / inner_loop_iter_K / post_gate_pending / signoff_pending / report_signed) resumes cleanly. Adversarial: hand-edited state.json with a phase string that doesn't exist; verify F-PIPE-18.

**§7.11 — Iterations append-only.** Property: `run_state.iterations` length is monotone non-decreasing across checkpoint sequences. Property: any code path that would truncate or reset raises F-PIPE-19. Adversarial: hand-edited state.json with truncated iterations tuple → F-PIPE-19 on resume.

**§7.12 — Cedar-decision presence.** Property: `pre_gate_passed` phase requires `PreGateResult.cedar_decision_ref is not None`. F-PIPE-20 raised if missing. Adversarial: `PreGateResult` constructed with `cedar_decision_ref=None`; verify R11 rejects before `pre_gate_passed` transition.

**§7.13 — Mode-isolation.** Property: eval-mode cannot have `three_tab_envelope_hash != None`; cannot transition to `tabs_delivered`; cannot write under any intent outside `{golden-set-write, state-success, state-failure}`. Property: submission-mode cannot have `calibration_report_ref != None`; cannot write under any intent in `{golden-set-read, golden-set-write}`. Enforced at every checkpoint via `_assert_mode_isolation`. Adversarial: construct a RunState that violates each of the four sub-clauses (2 per mode); verify F-PIPE-21 at the next checkpoint.

**§7.14 — Eval-mode org-isolation (Law 3).** Property: `run_state.mode == "eval"` requires `run_state.org_slug == _read_golden_set_org(run_state.golden_set_ref)`. PRE-gate predicate (§4 Logician v2.1) enforces; §5 routes failure to `state-failure` + `aborted_trusted_fail`. Adversarial: manifest whose embedded operator_org_slug diverges from `run_state.org_slug`; verify F-EVAL-CROSS-ORG-READ PRE-gate fail + `aborted_trusted_fail` RunState.

**§7.15 — CalibrationReport non-exportability + freshness.** Property: no code path surfaces a CalibrationReport, its signature, or a reference to it in any submission-mode tab envelope / export / telemetry bundle. Property: `verify_calibration_report` refuses any signature whose `signed_at_iso` is older than `MAX_CALIBRATION_AGE_DAYS` (90 days); raises F-PIPE-21.calibration_signature_stale. Adversarial: fake clock advances past 90 days; verify stale signature rejected on resume-verify. Adversarial (pipeline-assertion shield): constructed reach where a CalibrationReport field leaks into a submission-mode envelope; verify F-PIPE-21 at envelope-construction.

**§7.16 — CalibrationReport canonical-bytes exhaustiveness.** Property: every field on `CalibrationReport`, `CalibrationReportItem`, `GoldenSetItem` is either canonical-included OR listed in the §5.6.4 exclusion table (currently `{"signature": "the signature cannot cover itself"}`). Adversarial: AST-grep test over the three dataclass definitions — any new field must appear in `canonical_bytes()` OR in the exclusion-table allowlist; CI-blocking failure otherwise.

### J.4 BT5 property tests (≥12; per-session provider quota / back-off)

**BT5 — Per-session provider quota / back-off.** Property: per-endpoint TokenBucket capacity enforced across concurrent `reserve` calls (sum consumed ≤ capacity per window). Property: back-off schedule `(50, 200, 800)` ms + jitter `(0, 300)` ms observed under InsufficientTokens. Property: lease TTL 30s auto-release on crash-before-release. Property: cascade advancement triggered on rate_limit_exhausted; landed-family pin preserved. Adversarial: concurrent fork-race harness (≥8 processes reserving against the same endpoint); verify no over-consumption, no lost leases, no stale locks. Adversarial: clock-skew injection → verify lease TTL still expires correctly (monotonic-ns, not wall-clock, per R7 contract).

### J.5 Full lifecycle fuzz harness (100-run parametric)

Two parallel harnesses — submission-mode + eval-mode — each parameterized over 100 distinct org slugs × 100 distinct run_ids. Each firing:
- Boots through all §5 modules on a fresh vault + fresh RunState.
- Verifies 11-phase (submission) or per-item (eval) trajectory terminates cleanly.
- Verifies every checkpoint's state.json hash-chain is consistent.
- Verifies no cross-run state leakage (Law 3 mechanical — one run's `run_id` never resolves to another's checkpoint).
- Verifies every run's final artifact (three-tab envelope OR signed CalibrationReport) is byte-reproducible on deterministic replay with identical fakes.
- Verifies rate-limiter lease ledger is empty at run end (no orphan leases).

### J.6 §9 test suite packaging

Per §5 blueprint §9 scope definition, §9.1-§9.6 become the canonical §5 test harness. Round 13 packages four files:

- `tests/loop/test_section_5_integration.py` — J.1 + J.2 boot-sequence integration (submission + eval lifecycles).
- `tests/loop/test_section_5_invariants.py` — J.3 seven §7-invariant property test classes.
- `tests/loop/test_section_5_bt5_rate_limit.py` — J.4 BT5 property + concurrent-reserve fork-race harness.
- `tests/loop/test_section_5_fuzz_harness.py` — J.5 100-run parametric fuzz (submission + eval).
- `tests/loop/conftest_section_5.py` — fixture library (clean vault, fake clock, fake randint, fake subprocess launcher, sample golden-set manifest, sample RFA, sample PROJECT_CONTEXT, fake Ed25519 signer).

Existing `tests/loop/conftest.py` is NOT modified — R13 adds a section-5-specific conftest alongside it to avoid perturbing R1-R12.B test surfaces. If fixture collision surfaces at ORIENT, merge into `tests/loop/conftest.py` as an additive extension.

## Dependencies

- All of §5 R1-R12.B LOCKED on disk (baseline 4841 tests after R12.B).
- §1 Sovereignty Envelope LOCKED-as-a-whole (Round J) — §5 consumes `within_org_root`, `SovereigntyEnvelope`, session lifecycle fixtures.
- §2 Vault v7.1 LOCKED — §5 consumes `mount_identity_tuple` + compound-commit primitives + write-if-absent for pubkey first-write.
- §4 Logician v2.1 + v2.2 LOCKED — PRE-gate + POST-gate runtime surfaces consumed via `pipeline.logician.pre_gate` / `pipeline.logician.post_gate` public APIs.
- §0.5 Blueprint Interface Index v4 — paired-commit rows for four new test files + conftest.
- Cedar policy files for Law 3 isolation test in J.5 — present in workspace per prior rounds; mock if unavailable per §2 Protocol contract.
- AST-lint R1-R7 clean on all four test files + conftest.

## Done definition

1. Five test files written (four `test_*.py` + one `conftest_section_5.py`) with ≥96 property tests across seven §5 invariants (≥12 per invariant × 7) + ≥12 BT5 property tests + ≥15 integration tests per lifecycle (J.1 submission + J.2 eval) with ≥5 adversarial per class + 2× 100-run fuzz harnesses (submission + eval).
2. Aggregate coverage target: ≥95% on every §5 module that was LOCKed per-round at 100%. Acknowledge up-front per §1 Round J precedent (line 25 of `project_impl_section_1_round_j_capstone_locked.md`): aggregate-over-package coverage may report lower than per-round 100% baselines because some defensive branches become statically unreachable under the combined fixture set. Report both per-module and aggregate numbers; per-round LOCK evidence stands.
3. AST-lint R1-R7 exit 0 on all five files.
4. Full suite green: R12.B baseline ~4841 → R13 target ≥ 4990 after ~150 new tests (E-024 2× multiplier on adversarial: ~96 property + 12 BT5 + 30 integration + 2×12 fuzz ≈ 150 floor; landed target ≥170 under 2× on adversarial).
5. Code Thesis Committee 5/5 PASS cycle-1 OR self-LOCK per §1 Round J / §3 Scout capstone precedent (see Self-LOCK eligibility section).
6. Operator signs — **§5 capstone LOCKED**. Promotes all of §5 from LOCKED-per-module (R1-R12.B) to LOCKED-as-a-whole-section.
7. Canonical daily_log LOCK block per gate #12 discipline; §0.5 paired-commit rows (five files as Index entries); lock_history row with `lock_class: "code"`, `scope: "§5 capstone — integration + invariant property tests + BT5 + fuzz harness + §9 test suite"`.
8. MEMORY.md prepend + `memory/project_impl_section_05_round_13_capstone_locked.md`.
9. Blueprint §5 v6 status line updated: "Round 13 capstone LOCKED 2026-04-YY — §5 LOCKED-as-a-whole-section."

## Test floor and multiplier

| Bucket | Floor | Under E-024 2× on adversarial | Comment |
|--------|-------|-------------------------------|---------|
| J.1 submission-mode integration | ≥15 (with ≥5 adversarial per class) | ~40 methods | R11 composition path; 8 classes × ~5 tests. |
| J.2 eval-mode integration | ≥10 (with ≥3 adversarial per class) | ~25 methods | R12.B composition path; 5 classes × ~5 tests. |
| J.3 §7 invariant properties | ≥84 (7 × ≥12) | ≥84 | Property tests are non-adversarial floor unless adversarial sub-case. |
| J.4 BT5 property | ≥12 | ≥12 | Single class; includes fork-race concurrent harness as one parameterized test. |
| J.5 fuzz harness | 2 classes (submission + eval) | 2 | 100-run parametric each, counted as a parameterized test class. |
| **Total floor** | **≥123** | **~163** | Line with §1 Round J (170 floor → 214 landed = 1.26×). |

**E-024 retrospective observation (from §1 Round J line 41 of LOCK memory):** capstone-shaped rounds relax to ~1.3× multiplier (vs 1.5× for channel-adapter-shaped modules). R13 target under that relaxed multiplier: ~160-170 tests.

## LOC target (E-024 2× on adversarial only)

| File | Target | ±25% | Comment |
|------|--------|------|---------|
| `tests/loop/conftest_section_5.py` | 400 | 300–500 | Fixture library; fake clock / randint / launcher / signer / golden-set / RFA / PROJECT_CONTEXT. Comparable to §1 Round J conftest (263 LOC) + eval-mode fixtures. |
| `tests/loop/test_section_5_integration.py` | 1200 | 900–1500 | J.1 + J.2 combined; submission 8 classes + eval 5 classes × rich adversarial fakes. |
| `tests/loop/test_section_5_invariants.py` | 1100 | 825–1375 | J.3 seven invariant classes × ≥12 property tests each, with property-test plumbing. |
| `tests/loop/test_section_5_bt5_rate_limit.py` | 500 | 375–625 | J.4 BT5 + fork-race harness (multi-process or threading with vault-CAS fakes). |
| `tests/loop/test_section_5_fuzz_harness.py` | 400 | 300–500 | J.5 two 100-run parametric classes; lean under parametric-fuzz harness style. |
| **Total new LOC** | **~3600** | **2700–4500** | Comparable to §1 Round J total (2318 LOC for 214 tests); R13 scope is wider by one lifecycle (eval). |

## Self-LOCK eligibility

**Lean toward single-cycle self-LOCK.** Precedent chain is strong:

1. §1 Round J capstone (LOCKED 2026-04-21) self-LOCKed cleanly — four test files, no new §1 code, 214 tests, zero cross-module surprises. Explicit rationale (lines 33-35 of LOCK memory): "committee dispatch on a test-only capstone that composes already-reviewed primitives would burn five family-API credits against the same attack surface the Round A-I committees already audited."
2. §5 R3-R12.B = eleven consecutive single-cycle self-LOCKs.
3. §3 Scout R5/R6/R7/R8/R9/R10.1/R10.2 = ten consecutive rounds without committee correction.
4. R11 (composition-heavy capstone composing 10 rounds) self-LOCKed with zero cross-round behavioral issues.
5. R12.B (pure composition over R1-R11 + R12.A) — current round; track record at time of R13 card write.

R13's novel surface is test-harness-shaped: integration path wiring + §7 invariant property-test class shapes + BT5 fork-race harness + 2× 100-run fuzz. No new §5 code. If ORIENT produces a clean cross-module mapping with no composition-seam ambiguity, single-cycle self-LOCK follows §1 Round J precedent. If ORIENT surfaces any invariant-test design ambiguity (e.g., how §7.15 non-exportability is tested against a constructed reach that would never appear in production) — escalate to a single Thesis Team dispatch under L-005 two-cycle.

## Coupling

- **Downstream unlock:** §5 capstone LOCK is the last precondition before §5 Group 5 committee-review dispatch (promotes §5 from LOCKED-per-module to formal committee-LOCK-as-whole) and before whole-build integration rounds (Group 9 E2E).
- **Ed25519 ceremony:** R12.A's `Ed25519ReferenceSigner` is already LOCKED; R13 exercises it under BT13 signing-path assertions in §7.15 property tests. If the Ed25519 seal ceremony runs before R13 LOCK, the capstone LOCK row carries the first §5 Ed25519-signed lock_history entry.
- **§4 Logician v2.2 inheritance:** R13's §7.14 eval-mode org-isolation tests exercise §4's `F-EVAL-CROSS-ORG-READ` PRE-gate predicate. Tests treat §4 Logician as a black-box public-API consumer (no Logician-runtime re-entry from test code).
- **§1 Round J prototype:** R13's 100-run fuzz harness reuses the §1 Round J J.3 fuzz structure (parametric over org slugs + deterministic replay). Reuse the same fuzz-harness pattern; do not re-invent.

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Tests | `tests/loop/conftest_section_5.py` |
| Tests | `tests/loop/test_section_5_integration.py` |
| Tests | `tests/loop/test_section_5_invariants.py` |
| Tests | `tests/loop/test_section_5_bt5_rate_limit.py` |
| Tests | `tests/loop/test_section_5_fuzz_harness.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` — R13 capstone row; `lock_class: "code"`; `scope: "§5 capstone — integration + §7 invariant property tests + BT5 + fuzz + §9 test suite"` |
| Blueprint | §5 v6 status line updated with "Round 13 capstone LOCKED 2026-04-YY" |
| Memory | `memory/project_impl_section_05_round_13_capstone_locked.md` + MEMORY.md prepend |
| Daily log | Canonical LOCK block per gate #12 |

## Open questions (resolve at ORIENT)

1. **Conftest placement — separate vs merged.** R13 proposes `tests/loop/conftest_section_5.py` as a sibling to the existing `tests/loop/conftest.py` to avoid perturbing R1-R12.B test fixtures. Alternative: merge into the existing conftest as an additive extension. ORIENT-decide: separate conftest (recommended — smaller blast radius; rollback is file-delete) vs merged (one source of truth; risk of fixture collision under pytest's collection semantics). **Recommendation: separate file, co-existing.**

2. **Fork-race harness for BT5 J.4.** Options: (a) `multiprocessing` with file-locked vault-CAS fakes; (b) `threading` with a shared in-memory vault + `threading.Lock`; (c) `asyncio` with cooperative concurrency. ORIENT-decide. **Recommendation: threading with in-memory vault fake — closest to §1 Round J's concurrent-append test style; no OS-level fork overhead; deterministic under pytest.**

3. **Deterministic replay in J.5 fuzz.** 100 distinct run_ids × 100 org slugs = 10,000 firings would be too slow. Two options: (a) parameterize 100 × 100 and accept the wall-clock cost with cached fakes; (b) parameterize 100 pairs (run_id, org_slug) and rely on independence proofs. ORIENT-decide. **Recommendation: 100 paired firings (option b); independence is asserted via BT5's per-endpoint token-bucket test, not via J.5.**

4. **§7.16 canonical-bytes AST-grep test owner.** R12.A already shipped a canonical-bytes exhaustiveness check at its own test boundary. R13's §7.16 property class should either (a) re-assert via a cross-module AST-grep test in `test_section_5_invariants.py`, or (b) trust R12.A's existing test and mark §7.16 as "covered at R12.A level; R13 cross-references". ORIENT-decide. **Recommendation: re-assert in R13 as property test — R13 is the whole-section capstone, so invariant coverage must live in the capstone test surface even if previously covered per-round. Defensive belt-and-braces.**

5. **Eval-mode fuzz coverage of `reconcile_operator_pubkey` first-write.** R12.B's existing tests cover first-write-vs-second-write. J.5 fuzz per 100-run org-slug × run-id matrix implicitly exercises many first-writes. ORIENT-decide: add an explicit first-write-twice-per-slug assertion to J.5, or trust R12.A's MA-09 coverage. **Recommendation: add an explicit J.5 assertion — `after 100 runs across 100 org slugs, exactly 100 pubkey_first_write_provenance.json sidecars exist, and exactly zero second-write rejection paths fired.**

6. **Submission-mode vs eval-mode fuzz parallelism.** Run the two fuzz harnesses in the same pytest session (sequential) or split across two CI jobs? ORIENT-decide at harness wire-up. **Recommendation: sequential in one session; total wall-clock ≤5 min per §1 Round J J.3 precedent.**

7. **AST-lint R7 (module-scope `Final[bool]` preflight sentinel).** R13 tests import `pipeline.loop.run_pipeline` + `pipeline.loop.run_eval_pipeline`; the ARCH-05 R7 walker must not flag test-module imports as violations. ORIENT-verify: test files are outside the `pipeline.loop.*` namespace the R7 walker enforces against. **Recommendation: verify R7 domain at ORIENT before writing; if R7 flags test imports, file a narrow R7-exemption instead of weakening R7.**

## Precedent

- §1 Round J capstone (LOCKED 2026-04-21) — four test files, 214 tests, single-cycle self-LOCK; structural template for R13.
- §3 Scout R8 DISCOVER capstone (LOCKED 2026-04-21) — six-channel parallel fan-out capstone; self-LOCK under composition-heavy surface.
- §5 R11 (LOCKED 2026-04-21) — 11-step orchestrator capstone; self-LOCK over 10 prior rounds with zero cross-round behavioral issues.
- §5 R12.B (LOCKED 2026-04-21) — eval-mode sibling capstone; self-LOCK under pure composition of R1-R11 + R12.A primitives.
- E-017 injection-seam discipline (10+ firings) — every Protocol consumed at the R13 test boundary comes through the already-locked public surface of its owner round.
- E-024 2× adversarial multiplier — applied per R11 / R12.A / R12.B precedent; capstone-shaped rounds relax to ~1.3× aggregate (floor honesty).
- E-026 module-lineage discipline — any cross-module Protocol lineage assertion uses `__module__`, not identity.

---

*Spec card v1 — 2026-04-21 — R13 whole-section capstone. Promotes §5 LOCKED-per-module (R1-R12.B) → §5 LOCKED-as-a-whole-section. Pre-staged at R12.B SELF-LOCK. Awaiting operator review before dispatch. Dispatch when R12.B LOCK is operator-signed and the R12.B LOCK row lands in `lock_history.v1.jsonl`.*
