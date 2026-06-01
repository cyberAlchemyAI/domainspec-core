# CTO_HANDOFF_BRIEF

**Run 4 / Tilth Card System CTO handoff brief — consolidated P0/P1/P2 + blind-spot posture + sequencing.**

| Field | Value |
|---|---|
| Filed | 2026-05-17 |
| Workspace | `/Users/goldenquill/Downloads/GoldenQuill/` |
| Authority | Run 1 (4 foundation deliverables under `docs/card_system_deep_research_2026-05-17/`) + Run 2 (14 per-card handbacks) + Run 3 (`docs/clc_run_aggregate_2026-05-17.md` operator independent CLC aggregate) + operator path-(a) ratification on OD-E. |
| Cross-reference | `docs/cards_ceremony_batch_synthesis_2026-05-17.md` (Run 4 deliverable 1 — companion to this brief). |
| Out of scope (Run 4) | LOCK ceremony firing, per-card content-judgment, Ed25519 re-signing, git operations, continuation of Run 2 research depth. |

---

## §0. Big picture (one paragraph)

The Tilth Card System is a 14-card LOCKed + signed YAML system (6 CIC + 8 CLC) backed by a schema-conformant loader, a 50+ amendment LOCK-history audit trail, and nine `F-CARDS-*` gate modules. On-disk reality is **better than the planning documents describe** — lifecycle is correctly `signed`, the loader does the right preflight enforcement on lifecycle + coupling at the field-name layer, and the system is architecturally sound. But three concurrent amendments (**§18 v1.2 dialect_routing_table re-key**, **§18.6 v2 dual-track CLC restructure**, **§4 v2.x.7 coupling value-position scan**) all carry `LOCKED` frontmatter while their companion code / schema / card YAML patches are pre-LOCK on disk; one of those three (§18.6 v2) was found by Run 3 to have signed three `card_cartridge_supersession` rows asserting on-disk content that **never landed** — a P0 integrity incident the operator has now ratified path-(a) resolution for. Once OD-E remediation lands (7-8 member compound, fires first; folds CLC-07 OD-C value-position regression FIX-IN-PLACE atomically), the residual work is one LARGE cards-ceremony (9-15 member compound bundling §18 v1.2 + Law-5 CLC + schema patches + 14-card content improvements) plus a v0.2 first-wave engineering sprint to graduate four `NotImplementedError` gate bodies and wire Ed25519 signature verification into the loader. **Roughly 4-6 weeks runway** from current state to v0.2-first-wave-shipping-ready, with the cards-ceremony being the longest single bottleneck (operator content-judgment-bound).

---

## §1. Findings consolidated (Run 1 + Run 2 + Run 3)

### §1.1 Top-line counts

| Run | Source | Findings | P0 | P1 | P2 |
|---|---|---|---|---|---|
| Run 1 | 4 audits under `docs/card_system_deep_research_2026-05-17/` | 28 cross-cutting items | 3 (P0-1, P0-2, P0-3) | 7 (P1-1 to P1-7) | 6 (P2-1 to P2-6) + 5 CR cross-cuts |
| Run 2 CIC | 6 per-card handbacks under `docs/cic_*_research_handback_2026-05-17.md` | 160 | 0 | 77 | 83 |
| Run 2 CLC | 8 per-card handbacks under `docs/clc_*_research_handback_2026-05-17.md` | 196 | 12 | 95 | 89 |
| **Run 2 total** | | **356** | **12** | **172** | **172** |
| Run 3 | `docs/clc_run_aggregate_2026-05-17.md` | 213 (6 P0 / 100 P1 / 107 P2) | 6 (3 framing-of-OD-E + 3 structural) | 100 | 107 |

**Note on Run 3 numbering vs Run 2 numbering:** Run 3 aggregate counts overlap with Run 2 CLC counts (both run against the same 8 CLC cards); Run 3 surfaces ARE Run 2's CLC subset PLUS the OD-E P0 integrity incident framing. The operator's prompt-stated total of **356 findings** is Run 2 only. Run 3 adds 1 net-new P0 (the OD-E ceremony-vs-ground-truth incident) that Run 2 detected per-card but didn't aggregate-frame.

### §1.2 P0 punch list (consolidated; operator-must-resolve before cards-ceremony fires)

| ID | Source | Description | Carry-forward owner | Resolution path |
|---|---|---|---|---|
| **P0-A** | Run 3 §4 + operator path-(a) ratification | §18.6 v2 dual-track restructure NEVER LANDED for CLC-05/06/07; rows 276/277/278 unverifiable | OPERATOR (path-a ratified); ENGINEERING executes re-run + L-025 preflight | OD-E remediation (7-8 member compound; rows 280-286/287) — **fires FIRST**. Detail at `docs/cards_ceremony_batch_synthesis_2026-05-17.md` §1. |
| **P0-B** | Run 2 CLC-07 §2.4 + Run 3 §2 | CLC-07 sponsorship_corporate.yaml lines 97 + 307 carry TILTH-CLC-03 + TILTH-CLC-02 slug literals in non-exempt value positions | OPERATOR + ENGINEERING | Folds into OD-E remediation row 285 atomically. Standalone OD-C-followon pre-staged at `pipeline/handoffs/od_c_followon_sponsorship_corporate_fix_in_place_2026-05-17.md` (optional, fires only if OD-E deferred). |
| **P0-C** | Run 1 P0-1 | §18 v1.2 dialect_routing_table LOCKed-but-not-applied; CIC schema + 6 CIC cards still on retired `funder_political_axis` | OPERATOR (18-30 hrs content-judgment); ENGINEERING (schema + card patches mechanical) | LARGE cards-ceremony (member 3 + members 5-10). |
| **P0-D** | Run 1 P0-2 | Lifecycle enum drift: architecture v7.0.11 §1.4 declares 6 values; schema/models/loader declare 4 | DOCUMENTATION editor; ENGINEERING reviews | Doc-only A5 (carve-out per OD-D row 270 precedent OR full §18 v1.x amendment). |
| **P0-E** | Run 1 P0-3 | Master prompt §5 stale lifecycle-gap claim — all 14 cards already `signed` | OPERATOR (master-prompt sidecar edit) | Doc-only A1 (retired by Run 3 §3 routing per Run 4 brief). |
| **P0-F (Run 2 CLC subset)** | CLC-02 (3) / CLC-03 (2) / CLC-04 (1) / CLC-05 (1; same as P0-A) / CLC-06 (1; same as P0-A) / CLC-07 (4; subsumes P0-B + 2 OD-E framings + 1 OD-C reconciliation gate) | Per-card P0s — vast majority subsume into P0-A, P0-B, or are framing variants | Various; see §1.3 below | Resolved by OD-E remediation + LARGE cards-ceremony. |

**Net P0s requiring distinct operator action:** **3** — P0-A (OD-E remediation), P0-C (§18 v1.2 dialect re-key), P0-D + P0-E (doc-only).

### §1.3 P1 summary (172 items)

P1 items break into 7 cross-card patterns + per-card content improvements:

1. **PRP-delegation discipline (P1 cross-card; Run 3 §5.1).** Cards surface program-law references (2 CFR 200, Davis-Bacon, NEPA, CDFI Fund standards, SBA 7(a), USDA CF) that belong in Program Rule Packs. **CTO blind spot A** (see §2 below) — PRP scaffolding is now LIVE infrastructure; routing pattern is canonical `cross_references_prp:` annotation field (§18 v1.x amendment surface).
2. **OD-A v2.4 admin-risk-register cross-CIC migration (P1 cross-card; Run 3 §5.2 + Run 4 synthesis §7).** ≥3-card recurrence threshold met for DEI / equity / inclusion / racial justice / anti-racist / decolonial / abolition / climate justice — pre-staged for v3.0 migration to per_cic_register + per_clc_register cells. Operator term-by-term approval required.
3. **Reviewer-culture differentiation (P1 cross-card; Run 3 §5.3).** `reviewer_profile_typical` currently lumps federal program officer / foundation program officer / credit committee / blind peer review / corporate brand team into single descriptions. Introduce `reviewer_culture_subtypes:` sub-field with closed-set enum.
4. **FID downstream consumer signals (P1 cross-card; Run 3 §5.4).** CLC-02 / CLC-04 / CLC-05 / CLC-07 surface funder-side intelligence that belongs in the Funder Intelligence Database project, not card body.
5. **F-CARDS-COUPLING-VIOLATION-EXTENSION gate-body graduation (P1 from Run 1 P1-1).** Gate raises `NotImplementedError`; loader covers field-name layer; value-position layer is unprotected at runtime today.
6. **Ed25519 signature verification at loader time (P1 from Run 1 P1-2).** `publisher_pubkey: Optional[bytes] = None` parameter is unused; trust model relies on `content_hash` + LOCK-history audit trail; signature itself never cryptographically verified.
7. **CLC-side Law-5 `common_funders_observed` discipline (P1 from Run 1 P1-3 + Run 4 §5).** Per-card A/B/C disposition pending operator confirmation.

Other P1 items: 4 doc-only Run 1 P1-4/P1-5/P1-6/P1-7 (header comments, gate ownership clarity, two-coupling-gate vocabulary fork, Cards/Cards typography); per-card content improvements aggregated across the 14 handbacks per Run 4 synthesis §6.

### §1.4 P2 summary (172 items)

P2 items are P2-1 through P2-6 from Run 1 (lock_history_row disposition, coverage_axis redundancy, deprecation procedure, `additionalProperties: false`, validators.py, stale README annotations) plus per-card polish-and-forward-binding items aggregated across the 14 handbacks. None are blocking.

---

## §2. Four CTO blind spots — current posture (folded in per Run 4 brief)

### §2.1 Blind spot A — PRP vacuum: ADDRESSED (live infrastructure)

**Status as of 2026-05-17:** **LIVE.** Operator has stood up PRP scaffolding:

- `pipeline/program_rule_packs/loader.py` (341 lines)
- `pipeline/program_rule_packs/_manifest/active_prps.yaml`
- `pipeline/program_rule_packs/_schema/program_rule_pack.schema.json`
- `pipeline/blueprint/v0.1/section_19_program_rule_packs.md` (316 lines)
- 5 deliverables total at `pipeline/program_rule_packs/`

**Posture:** Reference as live infrastructure for live-program-law routing. CTO need not stand it up; instead, integrate the canonical `cross_references_prp:` annotation field (cross-card P1 per §1.3 item 1) into the next §18 v1.x amendment. New PRP candidates surfaced by Run 3: `TILTH-PRP-BABA-IIJA` (CLC-01) / `TILTH-PRP-CDFI-FUND-CERT` (CLC-06) / `TILTH-PRP-USDA-CF` (CLC-08). Operator decides v0.1 vs v0.2 first-wave roster timing.

### §2.2 Blind spot B — Fragile private-data gate: DEFERRED

**Status:** `pipeline/logician/gates/f_cards_private_data_in_card.py` body remains stubbed (`NotImplementedError`).

**Posture:** Deferred to v0.2 first-wave loader graduation per Run 1 CR-3 item 6 + the v0.2 first-wave engineering sprint scope. CTO does not need to stand this up at v0.1. Risk note: until graduated, a Phase-4 researcher who reintroduces private-org-data into a card body gets through silently — but the 14 cards are operator-curated and the threat vector is low at the current 14-card scale. The acceptable risk window is the v0.2 first-wave sprint horizon (2-3 weeks).

### §2.3 Blind spot C — Key rotation policy: LANDED (live policy)

**Status as of 2026-05-17:** **LIVE.** Operator has landed:

- `vault_shared/key_rotation_policy.md` (498 lines on disk; 7 roles inventoried)
- `vault_shared/operator_attestation/publisher_pubkey.signed.yaml` (61 lines; operator-attestation pubkey stub)

**Posture:** Reference as live policy. CTO consumes this when wiring Ed25519 signature verification at loader time (Run 1 P1-2 / blind spot D's dependency). The operator-attestation pubkey stub closes the MISSING-role flag that Run 1 P1-2 surfaced as the publisher-pubkey-location ambiguity. Trust mechanism mirrors v7.0.7 §6.1 router-template byte-for-byte: publisher signs at release; white-glove pins the publisher pubkey at onboarding; loader verifies at boot.

### §2.4 Blind spot D — Operational freeze playbook: OUTSTANDING (next-action item)

**Status:** Not yet authored.

**Posture:** Surface in CTO brief as **outstanding operator-dispatch**. Framing per Run 4 brief:

- **Gate 1 (with Paul):** maintenance-window framing is acceptable. Operator dispatches Paul-Norton-aligned playbook draft per `docs/paul_norton_memory_alignment_brief_2026-05-15.md` precedent.
- **Gate 2 (shadow env):** mandatory. Shadow-environment cutover protocol required before any production-impacting LOCK ceremony fires post-v0.1 Beta.

**Recommended owner:** Operator + platform-engineer (Paul). Draft target: `docs/operational_freeze_playbook_v1_<UTC>.md`. Modeled on Run 1 P1-2 + the v0.1 Beta deployment runbook at `docs/v0_1_beta_deployment_runbook.md`. **CTO-side dependency:** until the playbook lands, the Phase 1 OD-E remediation can fire under maintenance-window framing; the Phase 2 LARGE cards-ceremony **should** wait for the playbook to land before fire (operator decision; the maintenance-window carve-out is acceptable for short-window single-org cycles but not for sustained dev).

---

## §3. Recommended sequencing (operator-time-minimizing)

### §3.1 Phase 0 — Doc-only sweep (no LOCK; engineering-editor bench)

Doc-only Run 1 Batch A: A1 (master prompt §5 sidecar) + A2 (README typography) + A3 (README Wave LOCK comments) + A4 (14-card header comments) + A5 (architecture v7.0.11 §1.4 lifecycle enum reconciliation). **~1-2 hours operator review.** Bundle into a single sidecar pass. Does not block anything downstream.

### §3.2 Phase 1 — OD-E remediation (fires FIRST; operator path-(a) ratified)

Per `docs/cards_ceremony_batch_synthesis_2026-05-17.md` §1.2: 7-8 member compound LOCK at `<OD-E-RE-FIRE-UTC>`. Resolves P0-A (Run 3 §4) + P0-B (CLC-07 OD-C atomic fold).

- **Operator pre-work:** mechanical (re-run `pipeline/scripts/od_e_restructure_card.py`; verify CLC-07 OD-C atomic fold).
- **Engineering pre-work:** wire L-025 ceremony-script preflight (write → re-read → SHA3-512 verify → signature emit). Mandatory.
- **Runway:** ~1-2 days assuming script + preflight are ready.

### §3.3 Phase 2 — LARGE cards-ceremony (fires AFTER Phase 1 + operator content-judgment)

Per `docs/cards_ceremony_batch_synthesis_2026-05-17.md` §8: 9-15 member compound LOCK at `<LARGE-CARDS-CEREMONY-UTC>`. Resolves P0-C (§18 v1.2) + per-card P1/P2 content improvements + Law-5 CLC relocation + schema B1/B8/B20.

- **Operator pre-work:** 30-42 hours aggregate (18-30 hrs dialect re-key + ~2-4 hrs Law-5 + 6-10 hrs content-improvement review).
- **Engineering pre-work:** companion code patches (`pipeline/seats/scribe/dialect.py` + `pipeline/engineering/agents/references/dialect_codebook.yaml`); concurrent with operator pre-work.
- **Runway:** ~1-2 weeks elapsed if operator can dedicate ~10 hrs/week to pre-work.

### §3.4 Phase 3 — Gate-body graduation sprint (Run 1 Batch C; engineering-only)

Per Run 1 Batch C: graduate `f_cards_coupling_violation_extension.py` body + refactor coupling-enforcement ownership clarity + reconcile two-coupling-gate vocabulary + pre-stage `pipeline/scripts/od_c_backfill_scan.py`. **1-2 weeks engineering sprint.** Can run concurrent with Phase 1 + Phase 2.

### §3.5 Phase 4 — v0.2 first-wave loader graduation (Run 1 Batch D; engineering-only)

Per Run 1 Batch D: Ed25519 signature verification at loader time + 4 stubbed gate body graduations + `load_card()` past `NotImplementedError` boundary + `pipeline/cards/registry_loader.py`. **2-3 weeks engineering sprint.** Fires after Phase 1 + 2 lock in card-system invariants.

### §3.6 Phase 5 — Cross-CIC admin-risk-register migration (sidecar; not a LOCK)

Per Run 4 synthesis §7: operator term-by-term approval; in-place register edits at `pipeline/logician/admin_risk_register.yaml`. **1-2 hours operator time once decisions land.** Can fire anytime after Phase 1. V3.0 schema delta itself lands as a separate §0.5 paired-commit LOCK on its own timing.

### §3.7 Phase 6 — Operational freeze playbook (blind spot D)

Operator + Paul author. Surface as outstanding before Phase 4 fires. Maintenance-window framing acceptable for Phase 1; shadow-env mandatory before Phase 2 + Phase 4.

### §3.8 Phase 7 — Deferred cleanup (Run 1 Batch E)

P2 items E1-E5: lock_history_row disposition, coverage_axis derivation, deprecation procedure, `additionalProperties: false`, validators.py. Bundle at convenience.

### §3.9 Total runway

**~4-6 weeks** from current state to v0.2-first-wave-shipping-ready, with Phase 2 (LARGE cards-ceremony) being the longest single bottleneck (operator-content-judgment-bound).

---

## §4. Load-bearing vs governance theater — honest read

Operator wants the truth, not reassurance.

### §4.1 Load-bearing (do not skimp)

1. **OD-E remediation (Phase 1).** This IS the test of whether the lock_history audit trail means anything. If rows 276/277/278 stay unverifiable, every downstream signature-verification graduation premise is broken. **Do not defer.** The L-025 preflight discipline is the structural fix; without it, the OD-E recurrence class repeats.
2. **§18 v1.2 dialect_routing_table re-key (Phase 2 substantial member).** Scribe currently keys dialect routing on a retired political axis. Every register-selection decision Scribe makes today is keying on bad data. This is the most consequential live drift in the system.
3. **Ed25519 signature verification at loader time (Phase 4).** Architecture v7.0.11 declares signature verification production-required; loader does not invoke it. The trust boundary the architecture spec defines exists only on paper until this lands.
4. **F-CARDS-COUPLING-VIOLATION-EXTENSION value-position scan (Phase 3).** The exact mechanism that caught the CLC-07 OD-C regression by sidecar is not yet a runtime gate. Any future card patch can reintroduce slug literals silently. **Until graduated, every operator content-judgment session for §18 v1.2 should be run with a sidecar scan as a pre-commit check.**
5. **L-025 preflight discipline (now standing).** The cleanest single structural defense against the OD-E recurrence class. Wire into the ceremony script layer; not loader.
6. **PRP scaffolding (live; blind spot A).** Now load-bearing once `cross_references_prp:` lands on cards. PRP is where live-program-law goes; cards are where customer-archetype-pattern-recognition goes. Keep the boundary clean.
7. **Operator-attestation pubkey + key rotation policy (live; blind spot C).** Without these, signature verification has nowhere to anchor. They ARE the trust boundary's hardware-equivalent.

### §4.2 Governance theater (do not over-invest)

1. **Architecture v7.0.11 §1.4 lifecycle-enum reconciliation (A5).** Useful for onboarding clarity. Documentation-only. Doesn't change runtime behavior. **Doc-only LOCK carve-out is fine; do not commission a Thesis round.**
2. **Cards/Cards typography fix (A2).** Visual readability only. No runtime impact. **Doc-only sweep.**
3. **Coverage_axis 1:1 redundancy (Run 1 P2-2).** Cosmetic. Decide once; document.
4. **`lock_history_row` / `lock_timestamp_utc` / `supersession_lock_history_row` schema fields (Run 1 P2-1).** These exist in schema but no code consumes them. Either graduate or remove. Either way it's a small patch; the discussion of which is theatrical relative to the patch size.
5. **README "NEEDED — Phase D research" comments (A3).** Stale annotations only.
6. **Two-coupling-gate vocabulary fork (Run 1 P1-6).** F-CIC-CLC-COUPLING-VIOLATION (v7.0.8, LIVE, 4 layers) vs F-CARDS-COUPLING-VIOLATION-EXTENSION (v7.0.11, stub). Reconciling output shapes is engineering-clean-up, not user-visible. **Operator decides amendment vs absorb; either is fine; pick and move.**

### §4.3 Watch (signals to track)

1. **L-025 preflight wiring.** If Phase 1 OD-E remediation fires WITHOUT a wired preflight, the recurrence class is open again. Block Phase 2 until L-025 is wired into the ceremony script tree.
2. **OPERATOR_DECIDES per-cell values in §7 admin-risk-register v3.0 pre-staging.** If operator defers these too long, the workspace-register has uneven coverage and Logician fires inconsistently across CIC archetypes — quality regression that's hard to see except through Scribe register-selection misses.
3. **Cross-family Thesis dispatch bridge pattern.** `mcp__Control_your_Mac__osascript` → openclaw gateway → groq Editor / google Judge / groq Red Team is the canonical pattern. If a Thesis round fires without bridge logging or with a silent single-Claude fallback, that's a discipline regression per AGENTS.md.
4. **Section 19 PRP loader graduation timing.** Blind spot A is live infrastructure but `cross_references_prp:` annotation field on cards is a schema delta that has not been amended yet. Tracker for v0.2 first-wave compound LOCK timing.
5. **L-026 candidate landing.** Mirror-of-L-025 at the card layer (per Run 3 aggregate §4 forward-binding contracts). Lesson-only; no LOCK ceremony; but Track in lessons memory.

### §4.4 Honest read on the system overall

The card system is **architecturally sound** and **operationally fragile in two specific ways**: (a) the ceremony-script tree does not enforce disk-write-verification before signature emission, which produced OD-E; and (b) the runtime trust boundary exists in declaration but not enforcement — Ed25519 verification at the loader is `Optional[bytes] = None`. Both are well-understood patches with clear precedent; neither is an architecture rework. Once both land, this system meets the bar Anthropic-grade research-grade engineering rigor implies.

The **discipline overhead** is real and worth it. The L-002 path-reference discipline, the L-005 two-audit cycle, the §6.17 Option-B compound paired-commit, the cross-family Thesis dispatch — these patterns are slow when measured by tokens, fast when measured by recoverable-from-mistakes. Run 3 surfaced a P0 integrity incident that a less-disciplined system would have shipped silently. **The audit trail caught it.** That's the value proposition.

The **drift hazard** is amendment-vs-disk decoupling — three LOCKed-but-not-applied amendments showed up in Run 1 (P0-1) and one was found to be partially undelivered in Run 3 (the OD-E incident). The recommended workflow change (Run 1 CR-1) adds an `amendment_status: LOCKED_TEXT_PENDING_COMPANION_CEREMONY` value or a separate `companion_ceremony_status:` frontmatter field. **Adopt one of these patterns;** it costs nothing and surfaces the gap that produced OD-E by convention.

---

## §5. P0 carry-forward list (operator-must-resolve before LARGE cards-ceremony fires)

1. **P0-A: OD-E remediation fires (path (a)).** Phase 1; rows 280-286/287. **OPERATOR DISPATCH.**
2. **P0-B: CLC-07 OD-C FIX-IN-PLACE.** Atomic fold into P0-A row 285. **OPERATOR-VERIFIED post-write.**
3. **P0-C: §18 v1.2 dialect_routing_table re-key.** Operator content-judgment 18-30 hours; mechanical engineering after decisions land. **OPERATOR PRE-WORK.**
4. **P0-D: Lifecycle enum reconciliation (A5).** Documentation-only; non-blocking; bundle with Phase 0 sweep. **DOCUMENTATION SWEEP.**
5. **P0-E: Master prompt §5 stale claim.** Documentation-only; non-blocking; A1 sidecar. **OPERATOR DISPATCH or DOCUMENTATION SWEEP.**

**Blockers for LARGE cards-ceremony fire:** P0-A and P0-C are hard blockers (Phase 1 must land first; Phase 2 needs operator content-judgment complete).

**Blockers for v0.2 first-wave loader graduation:** P0-A + the v0.2 sprint scope (Run 1 Batch D); operational freeze playbook (blind spot D) recommended before Phase 4 fires.

---

## §6. Recommended next operator action

**Two viable starting moves; operator picks based on bandwidth.**

### §6.1 Move A — Dispatch the OD-E remediation (RECOMMENDED if engineering bandwidth available)

Fires Phase 1 immediately. Resolves the P0-A integrity incident first. Wires L-025 preflight discipline as the cross-cutting structural fix. **Lowest cumulative ceremony cost** if OD-E and the LARGE cards-ceremony are sequenced atomically (the OD-E remediation lands the §18.6 v2 multi-track work that would otherwise be a Phase 2 member).

**Dispatch shape:** new session at `docs/handoffs/od_e_remediation_path_a_dispatch_<UTC>.md`. Carries:
- L-025 preflight implementation spec (write → re-read → SHA3-512 verify → emit signature).
- 7-8 member compound LOCK roster (per `docs/cards_ceremony_batch_synthesis_2026-05-17.md` §1.2).
- CLC-07 OD-C FIX-IN-PLACE atomic-fold verification step.

### §6.2 Move B — Fire CLC-07 standalone OD-C-followon supersession FIRST (lower-cost option if OD-E is deferred)

If operator wants to clear the CLC-07 regression flag faster than OD-E ceremony cycle allows. Single-row compound; lowest-cost ceremony shape. Pre-stage handoff at `pipeline/handoffs/od_c_followon_sponsorship_corporate_fix_in_place_2026-05-17.md`.

**Trade-off:** clears the regression flag fast but creates a duplicate-ceremony cost when OD-E re-fires (sponsorship_corporate gets re-signed twice). Only choose Move B if OD-E is meaningfully deferred (>1 week).

### §6.3 Recommendation

**Move A.** OD-E remediation is the highest-leverage action available. It (a) resolves the P0 integrity incident; (b) lands the §18.6 v2 multi-track work that would otherwise be a Phase 2 member; (c) folds CLC-07 OD-C FIX-IN-PLACE atomically; (d) installs L-025 preflight as standing discipline. One ceremony, four wins.

---

## §7. What this CTO brief does NOT do

- Does NOT fire any LOCK ceremony (operator dispatches).
- Does NOT author the operational freeze playbook (blind spot D outstanding).
- Does NOT auto-rewrite any card, schema, amendment, or LOCKed file.
- Does NOT continue Run 2 per-card research depth.
- Does NOT touch git.
- Does NOT Ed25519-re-sign (publisher key holder only).
- Does NOT carry per-card content-judgment for §18 v1.2 dialect re-key or 14-card content improvements (operator authors).

---

## §8. Files cited

- Run 1: `docs/card_system_deep_research_2026-05-17/{CARD_LIFECYCLE_AND_LOADER_GOVERNANCE_AUDIT,CANONICAL_NAMING_AND_ORTHOGONALITY_AUDIT,INITIAL_CTO_HANDOFF_BLOCKERS,FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2}.md`
- Run 2: 14 handbacks under `docs/cic_*_research_handback_2026-05-17.md` + `docs/clc_*_research_handback_2026-05-17.md`
- Run 3: `docs/clc_run_aggregate_2026-05-17.md`
- Run 4 companion: `docs/cards_ceremony_batch_synthesis_2026-05-17.md` (synthesis deliverable 1 of 2)
- Master prompts: `docs/cic_clc_unified_master_prompt_2026-05-17.md`, `docs/cic_clc_unified_batch_supervisor_prompt_2026-05-17.md`, `docs/cic_clc_unified_research_plan_2026-05-17.md`
- PRP scaffolding (CTO blind spot A — LIVE): `pipeline/program_rule_packs/{loader.py,_manifest/active_prps.yaml,_schema/program_rule_pack.schema.json}` + `pipeline/blueprint/v0.1/section_19_program_rule_packs.md`
- Key rotation policy (CTO blind spot C — LIVE): `vault_shared/key_rotation_policy.md` + `vault_shared/operator_attestation/publisher_pubkey.signed.yaml`
- OD-E restructure script (Phase 1 dispatch): `pipeline/scripts/od_e_restructure_card.py`
- LOCK history audit trail: `pipeline/engineering/lock_history.v1.jsonl`
- Card system source: `pipeline/cards/{CIC/,CLC/,_schema/,loader.py,registry.yaml,README.md}`
- F-CARDS-* gate modules: `pipeline/logician/gates/f_cards_*.py`
- Amendments: `pipeline/blueprint/v0.1/section_{18_v1_2,18_6_v2_dual_track,04_v2_x_7_card_coupling_value_position}_amendment.md` + `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md`
- AGENTS.md, SOUL.md, `pipeline/SESSION_BOOTSTRAP.md`, `pipeline/metrics/SESSION_METRICS_SPEC.md`

---

**One-line summary:**

CTO inherits a 14-card LOCKed + signed system with 356 catalogued findings (12 P0 / 172 P1 / 172 P2 from Run 2) plus one P0 ceremony-vs-ground-truth integrity incident (Run 3) for which the operator has ratified path (a). Recommended next action: dispatch OD-E remediation (7-8 member compound LOCK; resolves P0-A + P0-B atomically; installs L-025 preflight as standing discipline). PRP scaffolding + key rotation policy are LIVE; private-data gate body deferred to v0.2 first-wave; operational freeze playbook outstanding. Total runway 4-6 weeks to v0.2-first-wave-shipping-ready, with Phase 2 LARGE cards-ceremony as the longest bottleneck (operator content-judgment-bound, 30-42 hours pre-work).

*End of Run 4 synthesis deliverable 2 of 2.*
