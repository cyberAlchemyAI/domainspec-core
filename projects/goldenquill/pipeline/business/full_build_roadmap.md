# Tilth v0.1 Full Build Roadmap — NOW to Last Character Audited

**Filed:** 2026-04-19
**Scope parent:** `pipeline/validation/integration_scope_close_2026-04-19/01_scope_pin.md`
**Engineering parent:** `pipeline/engineering/da_vinci_engineer_prompt_v2.md`
**Provisioning parent:** `pipeline/engineering/provisioning_manifest_v0.1.md`

---

## Preamble — LOCKED Is Provisional

**LOCKED on an internal two-audit cycle ≠ sealed.** Every LOCK in this roadmap is the *internal* audit outcome: Thesis Team passed, §0.5 paired commit landed, round-close synthesis filed. It is not yet sovereign-audited by an impartial outside reviewer.

**Real LOCK = internal two-audit + outside-impartial audit + operator signature.** The outside-audit step is the one that turns provisional into sealed. Until then:

- Code treats every spec claim as a **citation**, not an axiom. If the code can't honor the spec, the spec is wrong — not the code. Kick it back to Thesis.
- Every downstream reader (code author, reviewer, operator) may surface an issue that reopens a provisional LOCK. No shame in that loop; it is how the system earns trust.
- Architecture amendments (v7.1, v7.2) and blueprint amendments (§4 v2.3, v2.4, v2.5, §5 v6) are provisional when their round closes. Outside audit is scheduled before Group 10 ship gate.

**The bet this roadmap is making:** the intelligence level of the council + clean process + cross-family segmentation + *qualified outside monitoring* is sufficient to run smoothly. The outside audit is not decorative — it is load-bearing. Skipping it collapses the trust model to same-family self-judgment.

---

## Current State Snapshot

| Artifact | Status |
|---|---|
| Architecture v7 (A1-A12) | LOCKED-internal 2026-04-19; outside audit pending |
| Blueprint §0.5 Interface Index v4 | LOCKED-internal 2026-04-19 |
| Blueprint §1 Sovereignty Envelope v5/v6 | LOCKED-internal 2026-04-18 |
| Blueprint §2 Vault Topology v7.1 | LOCKED-internal (referenced) |
| Blueprint §3 Scout | LOCKED-internal (referenced) |
| Blueprint §4 Logician v2.1 | LOCKED-internal 2026-04-18 |
| Blueprint §5 Pipeline v5 | LOCKED-internal 2026-04-18; v6 IN FLIGHT |
| GPP-DET tool (`gpp_det.py`) | EXISTS, PASS on scope-close docs |
| GPP Council Dispatch + Manifest tools | EXISTS on disk, audit pending |
| **Section 1** (14 modules total) | Round A LOCKED-internal (3 modules, 88 tests green); Rounds B + C code-complete on disk, internal audit underway |
| Sections 2–5 | Not started (scaffolds only) |

---

## Section 1 — Module-Level Map (14 modules, Rounds A–J)

Topologically ordered by dependency chain per operator's near-term plan:

| Round | Modules | Status | Dependencies |
|---|---|---|---|
| A | `_types.py`, `crypto_primitives.py`, `org_slug.py` | LOCKED-internal (88 tests green) | — |
| B | `audit.py`, `topology.py` | Code complete; internal audit underway | Round A |
| C | `keys.py` | Code complete; internal audit underway (`cryptography` lib added) | Round A + `zero_bytes` |
| D | `isolation.py` | Not started | Round B topology |
| E | `session.py`, `interrupted_state.py` | Not started | Round C keys, Round B audit |
| F | `admin_risk.py`, `degradation_log.py` | Not started | Round B audit, Round C keys |
| G | `rfa_envelope.py`, `project_context_envelope.py` | Not started | Round A crypto, Round D isolation, Round E session |
| H | `router_integrity.py` | Not started | Round A crypto, Round C keys |
| I | `boot.py` | Not started | Everything above |
| J | Section-1 integration + BT property tests | Not started | All of Section 1 |

Round A's E-001…E-004 lessons feed Round B spec cards as pre-checks.

---

## Task Sequence

### ═══ GROUP 1 — GPP Hardening (Phase 0) + §5 v6 Re-Lock ═══

Phase 0 is Code; §5 v6 is Cowork. Run in parallel.

| # | Task | Window | Depends on | Parallel? | Effort |
|---|---|---|---|---|---|
| 1.1 | Fix `gpp_det.py` bug: filter non-model-shaped strings in `router.yaml` walk | Code | — | Yes | Small |
| 1.2 | Fix `gpp_det.py` bug: distinguish TARGET-LOCK wording from current LOCK in VERSION-RESOLVE | Code | — | Yes | Small |
| 1.3 | Fix `gpp_det.py` bug: expand `CITE_EXCLUDE` to skip documented template patterns | Code | — | Yes | Small |
| 1.4 | Unit tests for all 10 DET checks (≥95% coverage on `gpp_det.py`) | Code | 1.1–1.3 | No | Medium |
| 1.5 | Audit `gpp_council_dispatch.py` (Tier 2) + tests | Code | — | Yes | Medium |
| 1.6 | Audit `gpp_manifest.py` (Tier 3 Ed25519 + ML-DSA-65) + tests | Code | — | Yes | Medium |
| 1.7 | Code Thesis Committee review of Phase 0 (5 cross-family, all-pass) | Code | 1.4–1.6 | No | Medium |
| 1.8 | §5 v6 re-lock Thesis round — absorbs Item 2 STR + telemetry-schema pin | Cowork | — | Yes (parallel w/ 1.1–1.7) | Large |
| 1.9 | §0.5 paired-commit: 2 rows (telemetry schema + STR derivation) | Cowork | 1.8 | No | Small |

**Group 1 gate:** Phase 0 merged; §5 v6 LOCKED-internal.

---

### ═══ GROUP 2 — Section 1 Completion (Rounds B–J) ═══

Can start as Phase 0 lands. Mostly serial by dependency chain. Run in the order shown.

| # | Task | Window | Depends on | Parallel? | Effort |
|---|---|---|---|---|---|
| 2.B.1 | Round B — finish internal audit of `audit.py` + `topology.py` (adversarial tests) | Code | 1.7 | No | Medium |
| 2.B.2 | Round B — Code Thesis Committee all-pass | Code | 2.B.1 | No | Medium |
| 2.B.3 | Round B LOCK-internal | Cowork | 2.B.2 | No | Small |
| 2.C.1 | Round C — finish internal audit of `keys.py` (provisioning manifest §3.3/§6.2 updated — `cryptography` dep) | Code | 2.B.3 | No | Medium |
| 2.C.2 | Round C — Code Thesis Committee all-pass | Code | 2.C.1 | No | Medium |
| 2.C.3 | Round C LOCK-internal | Cowork | 2.C.2 | No | Small |
| 2.D | Round D — implement + audit + LOCK `isolation.py` (OrgRootNamespace + TOCTOU closure + within_org_root; macOS canonical-path + inode-snapshot; Linux bind-mount stub) | Code + Cowork | 2.C.3 | No | Large |
| 2.E | Round E — implement + audit + LOCK `session.py` + `interrupted_state.py` (M6 atomic-flush checkpoint) | Code + Cowork | 2.D | No | Large |
| 2.F | Round F — implement + audit + LOCK `admin_risk.py` + `degradation_log.py` (BT3 + BT8, hash-chain from audit.py) | Code + Cowork | 2.E | No | Large |
| 2.G | Round G — implement + audit + LOCK `rfa_envelope.py` + `project_context_envelope.py` (M1 dual-hash + M2 sealing; may add `cedarpy` dep) | Code + Cowork | 2.F | No | Large |
| 2.H | Round H — implement + audit + LOCK `router_integrity.py` (M5 router.yaml HMAC + cross-family runtime invariant) | Code + Cowork | 2.G | No | Large |
| 2.I | Round I — implement + audit + LOCK `boot.py` (integration of all modules; Section 1 boot sequence) | Code + Cowork | 2.H | No | Large |
| 2.J | Round J — Section 1 integration + BT1–BT8 property tests + full boot-sequence property test + §7 test suite | Code | 2.I | No | Large |
| 2.K | Section 1 LOCK-internal (capstone) | Cowork | 2.J | No | Small |

**Group 2 gate:** Section 1 fully LOCKED-internal across all 14 modules.

*(Each Round B–I updates the provisioning manifest §11 changelog on commit.)*

---

### ═══ GROUP 3 — Classifier Research + §4 v2.3 Privacy Router (Design) ═══

Research can run in parallel with Group 1 + 2. Thesis round needs §5 v6.

| # | Task | Window | Depends on | Parallel? | Effort |
|---|---|---|---|---|---|
| 3.1 | Classifier research: presidio-analyzer / small embedding / regex+NER within A1 envelope | Cowork + Scout | — | Yes | Medium |
| 3.2 | Tag classifier EXISTS or reshape Item 1 to contract-only | Cowork | 3.1 | No | Small |
| 3.3 | Draft §4 v2.3 amendment (new §4.14 + 2 F-PRIVACY codes + §11 Law-map) | Cowork | 3.2, 1.8 | No | Large |
| 3.4 | Thesis pass 1: Editor + Judge | Cowork | 3.3 | No | Medium |
| 3.5 | Thesis pass 2: Red Team + Reasoner | Cowork | 3.4 | No | Medium |
| 3.6 | Operator + Opus synthesis → §4 v2.3 LOCK-internal | Cowork | 3.5 | No | Medium |
| 3.7 | v7.1 architecture LOCK-internal (Section A Risk-5 + D.5 + R.6 STR row) | Cowork | 3.6 | No | Medium |
| 3.8 | §0.5 paired commit: 7 rows | Cowork | 3.7 | No | Small |

---

### ═══ GROUP 4 — §4 v2.4+v2.5 Canary + Runtime Integrity (Design) ═══

Serial after Group 3.

| # | Task | Window | Depends on | Parallel? | Effort |
|---|---|---|---|---|---|
| 4.1 | Pin locked-test-vector corpus canonical path | Cowork | 3.6 | — | Small |
| 4.2 | Draft §4 v2.4 Canary + v2.5 Runtime Integrity + `section_04a_canary_harness.md` (7 failure codes) | Cowork | 4.1 | No | Large |
| 4.3 | Thesis pass 1: Editor + Judge | Cowork | 4.2 | No | Medium |
| 4.4 | Thesis pass 2: Red Team + Reasoner | Cowork | 4.3 | No | Medium |
| 4.5 | Operator + Opus synthesis → §4 v2.4+v2.5 LOCK-internal | Cowork | 4.4 | No | Medium |
| 4.6 | v7.2 architecture LOCK-internal (Section E) | Cowork | 4.5 | No | Medium |
| 4.7 | §0.5 paired commit: 15 rows | Cowork | 4.6 | No | Small |
| 4.8 | §5 v6.1 consumer wiring amendment (if needed) | Cowork | 4.6 | No | Small |

**Group 4 gate:** All blueprint amendments LOCKED-internal. 22 total §0.5 rows landed.

---

### ═══ GROUP 5 — Section 2: Vault Implementation ═══

~12 modules. `gate_and_open` is the single biggest; Option-B compound-txn primitives land here.

| # | Task | Window | Depends on | Parallel? | Effort |
|---|---|---|---|---|---|
| 5.1 | Implement Vault core: compound-txn, advisory locks, path-level write-lock, per-org init marker (BT14.a) | Code | 2.K | No | Large |
| 5.2 | Implement artifact stores: claim_evidence, admin_risk ledger, conversation_log, rails_reports, lessons_delta, rfa ingest | Code | 5.1 | No | Large |
| 5.3 | Implement shared vault: process_wrappers, sandbox_profiles, seccomp_filters, cached_opportunities, research_db, rubrics | Code | 5.2 | No | Medium |
| 5.4 | Tests + adversarial + BT property tests | Code | 5.3 | No | Large |
| 5.5 | Code Thesis Committee all-pass | Code | 5.4 | No | Medium |
| 5.6 | Section 2 LOCK-internal + provisioning manifest update | Cowork | 5.5 | No | Small |

---

### ═══ GROUP 6 — Section 3: Scout + Router Implementation ═══

Parallel with Group 5 if bandwidth allows.

| # | Task | Window | Depends on | Parallel? | Effort |
|---|---|---|---|---|---|
| 6.1 | Implement 6 channel families (A–F) — Grants.gov, SAM.gov, USASpending, cached, portals, RSS, Brave Search | Code | 2.K | Yes (w/ Group 5) | Large |
| 6.2 | DISCOVER → VERIFY → REVIEW pipeline with 4 verified-fit statuses | Code | 6.1 | No | Large |
| 6.3 | HTTP client (httpx) + SAM.gov key integration | Code | 6.1 | Yes (w/ 6.2) | Medium |
| 6.4 | Tests + adversarial | Code | 6.2, 6.3 | No | Large |
| 6.5 | Code Thesis Committee all-pass | Code | 6.4 | No | Medium |
| 6.6 | Section 3 LOCK-internal + provisioning manifest update | Cowork | 6.5 | No | Small |

---

### ═══ GROUP 7 — Section 4: Logician Full Implementation ═══

Consumes Section 2 (Vault) + all §4 amendments (Group 4).

| # | Task | Window | Depends on | Parallel? | Effort |
|---|---|---|---|---|---|
| 7.1 | Implement Logician core: all PRE/POST/COMMIT gates, §6 failure-code registry, Cedar runtime | Code | 5.6, 4.7 | No | Large |
| 7.2 | Phase 2a: Privacy Router content-scan PRE-gate (§4.14) + classifier wiring | Code | 7.1 | No | Large |
| 7.3 | Phase 2b: Runtime Integrity family (4a–4d) + Canary edit-time replay gate (§4.15) | Code | 7.1 | No | Large |
| 7.4 | Admin-risk register validation (18 entries) + flagged-term scanning | Code | 7.1 | Yes (w/ 7.2, 7.3) | Medium |
| 7.5 | Tests + adversarial for all §4 gates | Code | 7.2, 7.3, 7.4 | No | Large |
| 7.6 | Code Thesis Committee all-pass | Code | 7.5 | No | Medium |
| 7.7 | Section 4 LOCK-internal + provisioning manifest update | Cowork | 7.6 | No | Small |

---

### ═══ GROUP 8 — Section 5: Pipeline Orchestrator ═══

| # | Task | Window | Depends on | Parallel? | Effort |
|---|---|---|---|---|---|
| 8.1 | Run-lifecycle: session start, seat dispatch, invocation, run-end | Code | 5.6, 6.6, 7.7 | No | Large |
| 8.2 | Phase 1: Telemetry + STR derivation + rolling aggregation | Code | 8.1 | No | Large |
| 8.3 | Run-start PRE-gate batch (key presence, drift-from-locked-router) + run-end rails-report POST-gate | Code | 8.1 | No | Medium |
| 8.4 | Council dispatch: KGIE preflight, gear selection (Sparring/Co-Pilot/Synthesizer) | Code | 8.1 | No | Large |
| 8.5 | M13 bypass mechanism (24–72hr ceiling, signed + audited) | Code | 8.4 | No | Medium |
| 8.6 | Tests + adversarial for Section 5 | Code | 8.2–8.5 | No | Large |
| 8.7 | Code Thesis Committee all-pass | Code | 8.6 | No | Medium |
| 8.8 | Section 5 LOCK-internal + provisioning manifest final update | Cowork | 8.7 | No | Small |

---

### ═══ GROUP 9 — Integration Testing ═══

| # | Task | Window | Depends on | Parallel? | Effort |
|---|---|---|---|---|---|
| 9.1 | E2E pipeline test: Scout → Scribe → Editor → Judge → Logician on VAPG FY26 + test org | Code | 8.8 | No | Large |
| 9.2 | Cross-family runtime test: verify no same-family review paths | Code | 9.1 | No | Medium |
| 9.3 | Sovereignty test: kill all network → pipeline runs local-only on Dev 8GB | Code | 9.1 | Yes | Medium |
| 9.4 | Law 3 isolation test: attempt cross-org read → fail-closed | Code | 9.1 | Yes | Medium |
| 9.5 | Canary test: mutate router.yaml → blocks on STR regression | Code | 9.1 | Yes | Medium |
| 9.6 | Fix + retest | Code | 9.1–9.5 | No | Medium |
| 9.7 | Code Thesis Committee integration review | Code | 9.6 | No | Medium |

---

### ═══ GROUP 10 — Outside-Impartial Audit (the real LOCK) ═══

This is the non-negotiable gate. Every prior LOCK is provisional until this clears.

| # | Task | Window | Depends on | Parallel? | Effort |
|---|---|---|---|---|---|
| 10.1 | Onboard qualified outside engineering advisor (per Da Vinci v2 §13, DV-F-10 — 10+ yrs distributed systems / AI-ML ops / crypto / LM runtime) | Cowork | 9.7 | — | Medium |
| 10.2 | Advisor reviews architecture v7 + all amendments (v7.1, v7.2) | Outside | 10.1 | Yes (w/ 10.3–10.5) | Large |
| 10.3 | Advisor reviews blueprints §1, §2, §3, §4, §5, §0.5 | Outside | 10.1 | Yes | Large |
| 10.4 | Advisor reviews Section 1–5 code + test suites (crypto primitives, isolation, vault, router, logician, pipeline) | Outside | 10.1 | Yes | Large |
| 10.5 | Advisor reviews GPP tool chain + council-dispatch + manifest signing | Outside | 10.1 | Yes | Medium |
| 10.6 | Advisor signs `pipeline/engineering/real_engineer_validation_<date>.md` per section (pass / needs-revision) | Outside | 10.2–10.5 | No | Small |
| 10.7 | Address any needs-revision findings; re-audit | Code + Cowork | 10.6 | No | Medium–Large |
| 10.8 | Promote every LOCK-internal to LOCK-sealed once outside audit clears | Cowork | 10.7 | No | Small |

**Group 10 gate:** Outside advisor signature on every provisional LOCK. No exceptions.

---

### ═══ GROUP 11 — Final System Ship ═══

| # | Task | Window | Depends on | Parallel? | Effort |
|---|---|---|---|---|---|
| 11.1 | GPP-DET + GPP-COUNCIL pass on full system state | Code + Cowork | 10.8 | No | Medium |
| 11.2 | Final L-006 existence audit | Cowork | 11.1 | No | Medium |
| 11.3 | Provisioning manifest final review (white-glove install tested on fresh machine) | Cowork | 11.2 | No | Medium |
| 11.4 | GPP-SYNTHESIS: operator signs final manifest (Ed25519 + ML-DSA-65 hybrid) | Cowork | 11.3 | No | Small |
| 11.5 | Full test suite green on Dev tier (M1 8GB) | Code | 11.4 | No | Medium |
| 11.6 | Daily log: v0.1 SHIP. Last character of code outside-audited and sealed. | Cowork | 11.5 | No | Small |

**v0.1 SHIP GATE:** 11.6. All sections LOCK-sealed (internal + outside). All tests green. Operator + advisor signatures on manifest.

---

## Parallelism Map

```
Group 1  ████████████████████
Group 2  ·········████████████████████████████████████  (Rounds B→J serial)
Group 3  ███████·················██████████████  (research early, Thesis after 1.8)
Group 4  ···································█████████████████
Group 5  ·····························································████████████
Group 6  ·····························································████████████  (parallel w/ 5)
Group 7  ·········································································████████████████
Group 8  ·····················································································████████████
Group 9  ···································································································██████████
Group 10 ·········································································································████████████  (outside audit)
Group 11 ·······················································································································████
```

**Critical path:** Group 1 → Group 3 → Group 4 → Group 7 (needs both Group 4 + Group 5) → Group 8 → Group 9 → Group 10 → Group 11.

**Off critical path:** Group 2 (Section 1 finish), Group 5 (Vault), Group 6 (Scout).

---

## Counts

- **Total tasks:** ~80
- **Cowork window tasks:** ~30
- **Code window tasks:** ~45
- **Outside-audit tasks:** 8 (Group 10)
- **Blueprint Thesis rounds:** 4 (§5 v6, §4 v2.3, §4 v2.4+v2.5, §5 v6.1 if needed)
- **Code Thesis Committee reviews:** 11+ (Phase 0, Rounds B+C+D+E+F+G+H+I+J, Sec 2/3/4/5, Integration)
- **Architecture LOCKs remaining (internal):** 2 (v7.1, v7.2)
- **Blueprint LOCKs remaining (internal):** §5 v6, §4 v2.3, §4 v2.4, §4 v2.5, section_04a_canary_harness
- **Section 1 modules remaining:** 11 (Rounds B–J)
- **§0.5 rows to land:** 22 across 3 paired commits
- **Outside-audit signature sets:** 1 per section + 1 per architecture-level amendment ≈ 8 signed validation docs

## Memory hygiene note

Every LOCK commit (internal OR sealed) triggers: `daily_logs/` entry, `MEMORY.md` pointer update if mechanism is new, `lessons.md` append if a failure mode was named. Per SOUL.md memory-hygiene discipline: same-turn updates, never deferred.
