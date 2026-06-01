# Final Roadmap to Ship — Tilth v0.1

**Filed:** 2026-04-21 (end of day)
**Supersedes:** `pipeline/business/mvp_tilth_launch_readiness_2026-04-20.md` (§3 Current State + §10 Tactical Plan sections only; §9 Ship Gate + §6 Risk Register + §11 Post-MVP remain canonical)
**Purpose:** Close the gap between "engineering ahead of decision throughput" and "v0.1 SHIP."
**Path selected 2026-04-21 EOD:** **Path A** — full council-seat delivery in pipeline, advisor audit before ship, no split activation. Operator declined Path B (skills-driven Editor/Judge) citing "not in a hurry." OQ-5 split stays emergency reserve only; Day-10 trigger moot under Path A commitment.
**Realistic SHIP target:** 2026-05-30 (aggressive) to 2026-06-30 (comfortable). Advisor audit window is largest variance.
**No GUI / dashboard in v0.1 scope** — operator decision 2026-04-21. Revisit for v0.1.1 or later.
**Read order:** §1 Where We Are → §2 Critical Path → §3 Operator Decision Queue → §4 Swim Lanes → §5 Ship Gate → §6 Week-by-Week.

---

## §1. Where We Are (true state, 2026-04-21 23:00 UTC)

**Today's landings** (80 LOCK rows across last 48 hours):

- **§4 Logician v2.2 gate queue CLOSED** — 12/12 structural amendment-enforcement gates LOCKED. Consolidated §4 v2.2 blueprint amendment LOCKED at 07:16:35Z (first `lock_class: "blueprint"` row in history).
- **§1 Sovereignty Envelope Round J capstone SIGNED OFF** — 214 tests, 2318 LOC. §1 LOCKED-as-a-whole-section. 86% union-drift flagged as v0.1.x measurement fix.
- **§5 Pipeline Round 6 (post_gate_runner) SELF-LOCKED** — 37 tests, 555 LOC, 100% cov.
- **§5 Pipeline Round 7 (rate_limiter) SELF-LOCKED** (row 93) — 642 LOC, 100% cov, 35 tests.
- **§5 Pipeline Round 8 (cascade) SELF-LOCKED** (row 94) — 392 LOC, 100% cov, 41 tests.
- **§5 Pipeline Round 9 (tab_delivery) SELF-LOCKED** — 482 LOC, 100% cov, 44 tests (E-024 4.71×). Landed in parallel dispatch with R8. 9 consecutive §5 self-LOCK rounds, zero committee corrections.
- **§2 Vault Batch 1 formally LOCKED 2026-04-22** — redispatch round closed; 5 promotion rows (lock_history rows 102-106) amending walk-back rows 96-100. F-1/F-1b/F-2..F-5 fix groups all landed.
- **§2 Vault Batch 2 split landing:** 5/6 modules cycle-1 PASS (schemas, layout, identity_tuple, uuid_floor, metadata_homogenizer) → Option-B ratified, landing formal LOCKs. gate_and_open had 2 HIGH findings + dedicated remediation round.
- **§2 Vault Batch 3 committee fired:** 1/6 cycle-1 PASS (atomic_freeze row 43). 5 modules blocked on real findings. Option 2 remediation ratified — split narrow-fix (groups D+E: vault_query_skill + research_db_query_skill BLUEPRINT_DEPS citation corrections, L-005 §8b eligible) from real code (groups A+B+C: vault_write §4.10.4/§4.10.6 implementation + compound_txn constants + mirror_verify disposition). Handoff: `pipeline/handoffs/vault_batch_3_remediation_2026-04-22.md`.
- **Language-compression exploration** parked at `pipeline/handoffs/inter_ai_language_compression_exploration.md` — post-v0.1 strategic research, NOT on critical path.
- **Retry-loop discipline update 2026-04-22:** `feedback_transport_outage_discernment.md` hard rule: 120s total cap, single-shot + 30s health-check, no `attempts × rounds × wait` multiplication. 10-min grinder deleted. E-028 candidate filing pending. Gemini Flash 503 sustained outage was trigger case.
- **E-027 filed + §3.1 codified** — Qwen3-32B non-rubric verdict tokens on consolidated payloads >~80k prompt tokens. Three-row empirical table, three mitigation options. Pre-check now required in spec-card template §11 for any consolidated dispatch targeting `code_reviewer_2=qwen3-32b`. Systemic fix.
- **router.yaml fallbacks cleaned** — lines 77, 81 replaced with honest self-fallback annotations citing Groq Dev-tier catalog reality (2026-04-22). Parallel finding fixed inline per L-012 scope-honest discipline.
- **§4 Logician Group 7 Batch A — DISPATCH READY 2026-04-22.** Pre-stage complete at `pipeline/validation/code_reviews/logician_group_7_batch_a_2026-04-22/`. 4 modules × 5 seats = 20 API calls. All SHAs match handoff pins. Baseline GREEN (159/159 per-module pytest, AST-lint clean, full suite 6074/0fail). E-027 token estimates well-modeled (all under 80k qwen ceiling, no mitigation needed). Cross-family math L-003-compliant (Anthropic + Groq + Google = 3 families across 5 seats). EN-003 round 7. Operator green-lighted; awaiting fire.
- **§4 Group 7 Batch B + Batch C** queued — fire after Batch A LOCKs. Batch B = claim_evidence + source_tag_verify + dossier_verify; Batch C = admin_risk + conversation_log.
- **§5 Round 10 (cron_scheduler) SELF-LOCKED** (row 101) — 464 LOC, 99% cov (1 defensive branch unreachable from valid input), 37 tests. `FlockAcquire` is 9th E-017 firing; `VaultTransientError` owned by R10 (transport-layer, keeps vault package error taxonomy clean). Ten consecutive §5 self-LOCK rounds.
- **§5 Round 11 `run_pipeline` SELF-LOCKED** — 929 LOC module + 1629 LOC tests, 100% cov (150/150 stmts), 59 tests. §4.1 11-step submission-mode pipeline composing R1-R10 end-to-end, zero cross-round behavioral issues. Eighth consecutive §5 single-cycle self-LOCK (R3→R11). Self-LOCK directive validated per §1 Round J precedent.
- **§5 Round 12 SPLIT into R12.A + R12.B** per scope-honest pre-flight (L-011/L-012 discipline).
- **§5 Round 12.A SELF-LOCKED** (row 103) — 1801 LOC, 134 tests, 99% cov. Ed25519 signing + 15-field CalibrationReport + golden-set NFC+realpath. Tenth consecutive §5 single-cycle self-LOCK.
- **§5 Round 12.B SELF-LOCKED** (row 104) — `run_eval_pipeline.py` 1307 LOC, 100% cov, 91 tests. Zero regressions, zero new Protocols (pure composition). Eleventh consecutive §5 single-cycle self-LOCK.
- **§5 R13 capstone paste-ready** — handoff at `pipeline/handoffs/section_05_round_13_handoff_2026-04-21.md`. Test-only; no new §5 code. Target ~123-160 tests. LOCKs §5 as whole-section-promoted.
- **§5 Round 13 queued** — §5 whole-section LOCK capstone (integration + BT-property + fuzz across R1-R12, §1 Round J analog). THIS is the §5 whole-section LOCK round, not R11 or R12.
- **§3 Scout Round 9 (verify_stage) SELF-LOCKED** — 142 tests, 1065 LOC, 100% cov. Scout at 9 consecutive SELF-LOCK rounds, zero committee corrections.
- **Test suite:** 6074 pass / 12 skip (macOS-only sandbox skips will run on M1) / 1 xfail / 0 fail. Heading to ~6086 on M1.
- **§6 Operating Envelope LOCKED** (inferred from Scribe R1 prerequisite interlock satisfaction).
- **§7 Scribe R1 LOCKED** (row 120) — types.py + kgie.py, 165 tests, 100% module cov. §7.6-§7.9 scaffolded but not yet implemented at R1.
- **§7 Scribe R2 LOCKED** (row 121) — 4 modules filled: smart.py §7.6 + overlooked_expenses.py §7.7 + dialect.py §7.8 + program_templates.py §7.9. 189 new tests (354 scribe total). 100% coverage across all 7 scribe files. Zero committee, self-LOCK per §5 R1-foundations precedent. §7.2 Law 5 now has both layers (R1 KGIE + R2 DIALECT_IDENTITY_PROXY_TABLE). **Window caught scope gap: SectionDraft + compress.py not landed; R2 extending before R3.** Full suite 5395 (+189 from R1's 5206).
- **§2 Vault Batch 3 remediation Phase 2 CLOSED** — vault_write + compound_txn + mirror_verify all 5/5 PASS. qwen mirror_verify 8000-token degeneracy bypassed via Groq `reasoning_effort=none`. L-016 filed + E-027 extended (3rd firing, degenerate-repetition sub-pattern). §4 Logician Group 7 unblocked.
- **§2 Vault LOCKED-as-a-whole 2026-04-22** — K.0 fixtures + K.1 integration + K.2 BT14 properties (with BT14d schema-drift fix) + K.3 boot-sequence parametric fuzz (475 LOC, 65 tests, N ∈ {2,8,16,32} orgs + Law 3 cross-org rejection invariant). Self-LOCK per §1 J + §5 R13 precedent. Blueprint title bumped, daily_log gate-#12 block, MEMORY.md prepended. **§4 Group 7 (9-module Thesis dispatch) now UNBLOCKED.**
- **§5 R13 capstone LOCKED** (inferred — test files all on disk, suite reflects landing).
- **§7 Scribe R3 in flight** — all 4 R3 modules on disk: provider_anthropic.py, admin_risk_adapter.py, logician_wiring.py, seat.py. Plus R2 extension closure (section_draft.py + compress.py). LOCK row likely imminent.
- **NEW pipeline.harness.gates** — production wrapper for F-AMDT-02/03/12 enforcement gates. 357 LOC, 100% cov, 52 tests. Committee audit dispatched per operator directive.
- **Handoffs pre-staged for Path A next council-seat rounds:**
  - Scribe R2 (`scribe_round_2_dispatch_2026-04-21.md` + spec card) — §7.5 draft-composition → SectionDraft schema (Editor + Judge consumers)
  - Scribe R3 (`scribe_round_3_dispatch_2026-04-21.md` + spec card) — seat.py + Anthropic provider + admin-risk + Logician wiring; COMMITTEE-REQUIRED (not self-LOCK)
  - Editor R1 (`editor_round_1_dispatch_2026-04-21.md` + spec card) — adapter per OQ-1
  - Judge R1 (`judge_round_1_dispatch_2026-04-21.md` + spec card) — types + rubric primitives + Law 5 evidence-verification hooks

**Critical unlock from today:** §1 Round J capstone LOCK unblocks §2 Vault committee-review dispatch — the longest-standing critical-path dependency.

**The central finding:** engineering has gotten ahead of operator decision throughput. Code production is not the bottleneck. Six operator decisions are (§3 below).

---

## §2. Critical Path to Ship

Linear dependency chain from here:

```
[TODAY] §1 Round J SELF-LOCK
    ↓ (operator sign-off)
§2 Vault committee-review dispatch (17 modules LOCKED-backfilled → formal committee LOCK)
    ↓
§3 Scout Round 10 (REVIEW + entity_research) — split/bundle operator decision
    ↓
§3 Scout Round 11 capstone-of-capstones (run_scout_discover_verify_review) — committee dispatch
    ↓
§4 Logician full committee review (9 non-gate modules beyond v2.1 lock)
    ↓
§5 Pipeline Round 7 rate_limiter (parallel-safe; can overlap with §2/§3/§4 above)
    ↓
§5 capstone LOCK (§5 v6 + v6.1 decisions landed)
    ↓
Council seats as pipeline modules: Scribe + Editor + Judge
  (currently run via OpenClaw skills only; need production code under pipeline/)
    ↓
Group 9 — E2E integration suite (currently 1 file: test_pregate_chain.py)
    ↓
Group 10 — Outside-impartial audit (THE REAL LOCK — advisor not onboarded)
    ↓
Group 11 — First-run acceptance; daily_log "v0.1 SHIP"
```

**Parallel swim lanes** (§4 below) run alongside the critical path.

---

## §3. Operator Decision Queue — CLEARED 2026-04-21

All six decisions cleared in one sitting. Engineering unblocked. Decisions logged in `daily_logs/2026-04-21.md`.

| # | Decision | Outcome |
|---|---|---|
| 3.1 | §1 Round J capstone sign-off | ✓ **SIGNED OFF.** §1 whole-section LOCK. 86% union-drift flagged as v0.1.x measurement fix. §2 Vault dispatch unblocked. |
| 3.2 | Scout R10 split vs. bundle | ✓ **SPLIT.** REVIEW first (self-LOCK eligible), entity_research second. |
| 3.3 | §5 v6.1 seat-output-schema pin | ✓ **PARKED to v2.3.** Not needed for v0.1. §5 capstone closes without v6.1. |
| 3.4 | Admin_risk v2.2 approve + path | ✓ **APPROVED + MOVED.** Canonical: `pipeline/institutional_memory/admin_risk_register.yaml` (v2.2, 772 lines). Legacy DEPRECATED. |
| 3.5 | §6 + §7 Thesis rounds | ✓ **WAIT 48h.** Re-check verdict dirs 2026-04-22 EOD; re-dispatch if empty. |
| 3.6 | Outside-advisor onboarding | ✓ **ALREADY KICKED OFF** by operator ahead of Week 2. |

Engineering has the gates. Code windows fire now.

---

## §4. Parallel Swim Lanes

Three lanes run in parallel. Operator routes Code windows into each.

### Lane A — Critical Path (sequential; blocks ship)

1. §2 Vault committee dispatch (17 modules)
2. Scout R10 + R11 (capstone-of-capstones — 5-family committee)
3. §4 Logician 9-module full committee review
4. §5 capstone LOCK
5. **Council seats as pipeline code** — Scribe, Editor, Judge must move from OpenClaw skills into `pipeline/seats/` (or equivalent) as production modules with Thesis review. Estimated 2-3 Code sessions per seat = 6-9 sessions.
6. Group 9 E2E integration suite (6-8 tests minimum)

### Lane B — Parallel-Safe Code (self-LOCK eligible, no blockers)

- §5 Pipeline Round 7 rate_limiter — spec pre-staged, TokenBucket CAS-reserve pattern, parallel-safe per R3/R4/R5/R6 precedent
- Cedar policy files (`org_isolation.cedar` + `compound_commit.cedar`) — noted as "in another window" but no LOCK row yet; surface and close
- §4 Logician AST-lint R6/R7 confirmation (alias-tracker + CFG-dominance)
- F-06 GPP path injection fix; F-04 structured STATUS field on spec cards

### Lane C — Decision Backlog (operator + Cowork)

- §3 operator-decision queue (six items above)
- Admin_risk v2.2 remaining-entry tagging (~60 entries; top-15 done)
- Outside-advisor pipeline: candidate list + NDA template + scope doc
- Stage 2 readiness-doc skeleton (so transition isn't a cold start post-ship)

---

## §5. Ship Gate (canonical — unchanged from 2026-04-20 doc §9)

Tilth v0.1 MVP is ready to ship when ALL 13 are true. Count remaining NOs weekly.

1. Every module in §§1–5 is LOCK-sealed (internal + outside audit + operator sig)
2. All 12 v2.2 Logician gates implemented, tested, AST-lint clean, LOCK-sealed ✓ **DONE 2026-04-21**
3. §4 v2.2 blueprint amendment LOCK-sealed ✓ **LOCKED-internal 2026-04-21** (sealing pending advisor sig)
4. Full pytest suite green on Dev tier (M1 8GB), zero flakes × 3 consecutive runs
5. AST-lint exit 0 across codebase
6. GPP-DET + GPP-COUNCIL pass on full system state
7. Cedar policies LOCKed, signed, manifest SHA256 canonical
8. `admin_risk_register.yaml` at canonical path, v2.2+ approved, POST step 6 passes
9. Ed25519 cryptographic seal on amendments
10. Outside-audit advisor signatures on arch + blueprints + code + GPP + Cedar (5 min, 8 expected)
11. Operator + advisor signatures on final provisioning manifest (Ed25519 + ML-DSA-65 hybrid)
12. First-run acceptance — live RFA E2E through pipeline, applicant sign-off, ledger entries land
13. Daily-log entry: `"v0.1 SHIP. Last character of code outside-audited and sealed."`

**Current score:** 2/13 concretely satisfied (gates #2 and #3); remaining 11 are scoped and staged.

---

## §6. Week-by-Week (execution-ready)

### Week 1 (2026-04-22 to 2026-04-28) — Decision cascade + §2 dispatch

- **Day 1 (Wed):** Operator sits down and clears §3 decision queue (batched, one session)
- **Day 2-3:** §2 Vault committee-review dispatch kickoff (Code window); Scout R10 split dispatch (Code window); §5 R7 rate_limiter parallel (Code window)
- **Day 4-5:** §2 Vault committee cycle continues; Scout R11 capstone-of-capstones dispatch; Cedar policy files land
- **Day 6:** §4 9-module committee review begins; Week 1 close — update this roadmap with remaining NOs

### Week 2 (2026-04-29 to 2026-05-05) — Council seats + §5 capstone + advisor

- **Day 7-9:** Council seats as pipeline code — Scribe first (Anthropic binding), Editor second (cross-family), Judge third (Google primary). Each seat gets 2-3 Code sessions with Thesis review.
- **Day 10-11:** §5 capstone LOCK; Group 9 E2E integration suite starts (VAPG FY26 + one test org)
- **Day 12:** Advisor onboarding kickoff — NDA signed, scope doc delivered, 5-doc review queue explained
- **Day 13:** Ship-gate rehearsal: dry-run all 13 criteria; generate remaining-NO list
- **Day 14:** Week 2 close

### Week 3 (2026-05-06 to 2026-05-12) — Outside audit begins

- **Day 15-18:** Advisor reviews architecture + blueprints (docs 1 & 2 of 5)
- **Day 19-21:** Advisor reviews code + GPP + Cedar (docs 3, 4, 5 of 5); operator addresses any needs-revision findings in parallel

### Week 4 (2026-05-13 to 2026-05-19) — Seal + first-run

- **Day 22-24:** Audit findings closed; Ed25519 seals applied; all LOCK-internal promoted to LOCK-sealed
- **Day 25-26:** First-run acceptance — live RFA dispatched E2E; applicant sign-off captured
- **Day 27:** Daily log: **"v0.1 SHIP."**

**Realistic SHIP target:** 2026-05-15 (aggressive) to 2026-05-30 (comfortable). Audit window variance is the largest unknown.

---

## §7. What Happens If (contingencies)

| Scenario | Response |
|---|---|
| §6 + §7 Thesis rounds stalled past 48h | Re-dispatch with fresh addressees; escalate to operator-voice decision on scope reduction |
| Advisor onboarding slips > 2 weeks | Maintain candidate pipeline; budget for 1-2 month engagement window; explore advisor-pair arrangement |
| Round J union-drift coverage (86%) flagged by advisor | Measurement fix in v0.1.x; not a ship blocker unless advisor rules otherwise |
| Cedar policies don't land by Week 2 | Python path-slug fallback + degradation-log + operator-review per entry; ship with conditional Cedar enablement |
| First-run grant fails visibly | Expected — bug → fix → lesson cycle; does not block ship gate #12 unless applicant withholds sign-off |
| Groq Dev tier pricing/catalog drift | Cross-family fallbacks via router.yaml; L-009 catalog-vs-tier check; EN-003 family-substitution pattern |
| Council-seat implementation exceeds 6-9 session estimate | Split into v0.1.0 (Scribe + Logician only; first-run minimal pipeline) and v0.1.1 (Editor + Judge added) |

---

## §8. Post-Ship (context; not in v0.1 scope)

Per CLAUDE.md five-stage arc: Stage 2 (multi-Cultivator seats), Stage 3 (coop multi-org), Stage 4 (contractor federation), Stage 5 (MaatAI on Sovereign Node). v0.1 → Stage 2 transition requires Telegram-bot Cultivator + multi-seat permission model + Cedar extensions. Do not scope Stages 2-5 into v0.1.

---

## §9. How to Use This Doc

1. **Read on session open** after CLAUDE.md / SOUL.md / router.yaml per AGENTS.md.
2. **Check §3 Decision Queue.** If your work depends on a pending decision, surface it before coding.
3. **Check §2 Critical Path.** If you're on Lane A, your work blocks ship. If Lane B, parallel-safe.
4. **On session close:** update §1 (true state) and §5 (ship-gate score) if anything changed.
5. **Weekly:** operator reconciles with `pipeline/metrics/session_log.jsonl` + `daily_logs/` for honesty.
6. **When §5 ship gate flips to 13/13:** v0.1 ships. Close this doc with SHIPPED banner. Start Stage 2 readiness doc.

---

*Living document. Update on every session close. Archive when v0.1 ships.*
*Filed 2026-04-21 by Cowork session. Canonical ship-gate reference. Supersedes prior tactical plans.*
