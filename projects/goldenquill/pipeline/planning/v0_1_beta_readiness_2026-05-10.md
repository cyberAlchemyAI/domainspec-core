---
title: v0.1 Beta readiness audit — walk of §6 production-cut checklist
filed: 2026-05-10
operator: Josh
parent_checklist: pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §6
authority: interstitial housekeeping session while WS-L §4 v2.x Cowork Thesis runs
purpose: Mark current state of every §6 readiness box as of today's 15 LOCKs (rows 178–192). Distinguish v0.1 Beta gate items from v0.2 cut items. Identify which boxes flip green when WS-L LOCKs.
superseded_by: pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md
---

# 1. Audit scope

> **Supersession note, 2026-05-11:** this file is a historical readiness walk from before WS-L, Classification Review wrapper, Intake/Uploader full implementation, and the router classification-boundary remediation landed. Use `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md` as the current v0.1 clearance checklist. Do not treat the RED/AMBER rows below as current status without re-verifying against the code tree.

§6 of the dispatch plan is the **v0.2 production cut** readiness checklist. v0.1 Beta is a subset gate — it requires the architectural + blueprint + code stack for `submission_mode` track only, plus classification routing infrastructure. Items related to `report_mode` (Data Collector, Report Generator, multi-channel outreach, BYOK envelope for Twilio/Postmark/MTProto/WhatsApp, state-rules card) are **v0.2 cut blockers only**, not v0.1 Beta blockers.

This audit walks every §6 box and tags it `[BETA]` (v0.1 Beta blocker) or `[V0.2]` (v0.2 cut only). State markers: 🟢 GREEN (done) · 🟡 AMBER (partial / awaiting paired work) · 🔴 RED (not done) · ⚪ N/A.

The architectural commitment in v7.0.7 §4.1 LOCKED 2026-05-10 — `F-CLASS-COVERAGE-INCOMPLETE` PRE-cycle gate — prevents Beta deployment shipping until §4 v2.x realizes the twelve F-CLASS-* primitives at WS-L. **WS-L LOCK is therefore the sole remaining v0.1 Beta architectural gate** (v7.0.4-M1 row 190 cleared the prior gate today). Everything below references this as "post-WS-L."

# 2. Box-by-box walk

## 2.1 Architecture

| Box | Tag | State | Evidence |
|-----|-----|-------|----------|
| v7.0.6 SELF-LOCKED (WS-A) | [BETA] | 🟢 | row 176 SELF-LOCKED 2026-05-09; row 177 CONFIRMED |
| v7.0.7 LOCKED (WS-B) | [BETA] | 🟢 | row 180 LOCKED 2026-05-10; full live cross-family rigor |
| v7.0.4 LOCKED (WS-C) | [BETA] | 🟢 | row 178 LOCKED 2026-05-09 + row 181 VERIFICATION_PASS_NEEDS_M1 (2026-05-10) + row 190 v7.0.4-M1 LOCKED 2026-05-10 (M1 corrective amendment closed all 5 HIGH/P0 + 2 RECOMMENDED + 4 OPTIONAL cross-family findings). v0.1 Beta gate cleared today. |
| v7.0.5 LOCKED (WS-D) | [V0.2] | 🟢 | row 179 LOCKED 2026-05-10; Funder Intel + Match DB + Scout channel G + Stage-5 consent on-ramp. v0.2-shape, but architectural commitments are LOCK-quality. |

**Architecture subtotal:** all four amendments LOCKED. No remaining architectural blockers for v0.1 Beta.

## 2.2 Blueprint

| Box | Tag | State | Evidence |
|-----|-----|-------|----------|
| §11 Intake LOCKED (WS-E) | [BETA] | 🟢 | row 185 LOCKED 2026-05-10; three-mode dispatch BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST; 11 owned gate codes; 17 skeleton tests pass |
| §12 Uploader LOCKED (WS-F) | [BETA] | 🟢 | rows 182/183/184 LOCKED 2026-05-10; submission package assembly; ten F-UPLOADER-* gates; four portal adapters + copy-paste fallback; attachment family deferred to v1.1 |
| §5 v8 track-registry LOCKED (WS-G) | [BETA] | 🟢 | rows 188/189 LOCKED 2026-05-10; submission + eval ACTIVE tracks; report FORWARD-COMPAT row (shippable_in: v0.2, refused at runtime); F-PIPELINE-TRACK-FROZEN dormant gate ACTIVATED |
| §2 v7.2 operational-data sub-kinds LOCKED (WS-H) | [V0.2] | 🟢 | rows 186/187 LOCKED 2026-05-10; 7 SIMPLE schemas + Cedar three-rule cross-product matrix + 4 failure codes; PII discipline on beneficiary_records |
| §13 Data Collector LOCKED (WS-I) | [V0.2] | 🔴 | not dispatched. Pre-staged this session (`pipeline/handoffs/ws_i_section_13_data_collector_v1_handoff_2026-05-10.md`). Fires when WS-G + WS-H + WS-L all LOCKED (G+H done; L pending). |
| §14 Report Generator LOCKED (WS-J) | [V0.2] | 🔴 | not dispatched. Refreshed handoff this session. Fires when WS-G + WS-H + WS-I + WS-L all LOCKED. |
| §15 Archivist spec LOCKED (WS-K) | [V0.2] | 🟢 | rows 191/192 LOCKED 2026-05-10; SPEC-ONLY at v0.2 per decision 8d default; 5 owned gate codes; 27 skeleton tests pass; proposes-only AST assertions structurally enforced |
| §4 Logician v2.x new gate families LOCKED (WS-L) | [BETA] | 🔴 | **SOLE REMAINING v0.1 BETA BLOCKER.** Cowork Thesis currently running. Must register the 12 F-CLASS-* gates from v7.0.7 plus the v0.2 family registrations from WS-C/D/F/I/J/K. |
| §0.5 v6+ paired amendments (WS-M) | mixed | 🟢 (for LOCKED siblings) | each compound-LOCK shipped paired §0.5 amendment atomically: §11 → §0.5 v10 (24 rows); §12 → §0.5 v9 (21 rows); §2 v7.2 → §0.5 v11 (22 rows); §5 v8 → §0.5 v12 (12 rows); §15 → §0.5 v13 (14 rows). Runtime-live row count: 304. |

**Blueprint subtotal:** v0.1 Beta requires §11 + §12 + §5 v8 + §4 v2.x (WS-L). Three of four are GREEN; WS-L pending closes the gate.

## 2.3 Code

| Box | Tag | State | Evidence |
|-----|-----|-------|----------|
| All Logician gates implemented + tested | [BETA] | 🔴 | depends on WS-L. v7.0.4 KFR family + v7.0.7 F-CLASS-* family + v7.0.8 CIC×CLC family + §11/§12/§15 owned gates all need WS-L Logician v2.x registration. Current §4 v2.7 (Uploader gates only — 10 codes + R-UPLOADER-NO-SUBMIT AST-lint) lands in row 22 of recent tail; v2.x consolidation pending. |
| Intake module scaffold + 3 modes | [BETA] | 🟢 (skeleton) / 🟡 (full impl) | §11 v1 SPEC LOCKED row 185 with module skeleton at `pipeline/orchestrator/seats/intake.py` and 17 passing skeleton tests. Three-mode dispatch shape stable. Full BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST implementation is the next code phase (after WS-L). |
| Uploader module + portal adapters | [BETA] | 🟢 (skeleton) / 🟡 (full impl) | §12 v1 LOCKED rows 182-184 with module skeleton + four adapter modules (Grants.gov Workspace / SAM.gov / Common Grant Application / Foundant / Submittable / Fluxx — Path-b scope) + copy-paste fallback. Attachment family deferred to v1.1. Three-layer auto-submit defense (Layers 1+3 EXISTS, Layer 2 ASPIRATIONAL). |
| Data Collector channel modules (5 channels) | [V0.2] | 🔴 | WS-I not dispatched. |
| Report Generator track-mode + sub-section templates + rubric | [V0.2] | 🔴 | WS-J not dispatched. |
| Archivist skeleton (proposes-only) | [V0.2] | 🟢 | row 191 §15 v1 SPEC LOCKED 2026-05-10; module skeleton at `pipeline/orchestrator/seats/archivist/__init__.py`; 27 skeleton tests pass; three-layer defense (AST-lint + runtime guard + Cedar policy) enforces proposes-only |
| Track registry dispatching submission + eval + report | mixed | 🟡 | §5 v8 row 188: submission + eval ACTIVE; report FORWARD-COMPAT row with `shippable_in: v0.2` — refused at runtime via `F-PIPE-TRACK-NOT-SHIPPABLE`. For v0.1 Beta: 🟢 (submission_mode is all v0.1 needs). For v0.2 cut: 🔴 (report_mode shippable=true flip pending WS-J LOCK). |
| §2 sub-kinds round-tripped via Cedar | [V0.2] | 🟢 | §2 v7.2 row 186: 1568 LOC modules + 93 LOC Cedar + 1506 LOC tests; 102 new tests; full round-trip on metrics / financials / photos / narrative_entries / timeline / beneficiary_records / attachments |

**Code subtotal:** v0.1 Beta needs Logician gates (RED, blocked on WS-L) + full Intake/Uploader implementations (skeletons GREEN, full impl AMBER). When WS-L LOCKs, the Logician gate box flips, and Intake/Uploader full-impl code phase becomes the next critical path.

## 2.4 Integration

| Box | Tag | State | Evidence |
|-----|-----|-------|----------|
| WS-N six end-to-end scenarios pass on M1 8GB dev node | [V0.2] | 🔴 | not dispatched; gating workstream for v0.2 cut. Scenarios 1-2 (Intake BULK + AWARD_INGEST) are v0.1-derivable; 3-6 are v0.2. |
| CIC × CLC orthogonality regression tests pass on every new schema/template | [BETA] | 🟡 | v7.0.8 baseline 84 tests passing; new schemas from §11/§12/§15 LOCKs need re-run + audit at LOCK time. WS-L will re-run on new gate families. |
| Full pytest suite green (>=8164 baseline + v0.2 tests) | [BETA] | 🟡 | each recent LOCK shipped full-suite-green at its commit (rows 184 / 187 / 189 / 192). No regression confirmation since §15 LOCK at row 192; presumed GREEN but needs current-commit verification at WS-L LOCK + every subsequent LOCK. |
| AST-lint R1-R7 clean across pipeline/ + tests/ | [BETA] | 🟡 | same as above — presumed GREEN at each LOCK commit. |

**Integration subtotal:** v0.1 Beta needs CIC×CLC regression + suite-green + AST-lint to stay green through WS-L LOCK. Cheap to verify; not architecturally blocked.

## 2.5 Operations

| Box | Tag | State | Evidence |
|-----|-----|-------|----------|
| Classification Review stage operator-runnable at white-glove | [BETA] | 🟡 | v7.0.7 SPEC GREEN. Operator-facing tooling for "run the Classification Review stage" is downstream of WS-L (gates fire) + Intake INCREMENTAL classification gating. Spec LOCKED; UX is the gap. |
| State-rules card ships PA/CA/FL/TX/NY at first wave | [V0.2] | 🔴 | depends on WS-I (decision 8f default). |
| BYOK envelope documented for Twilio + Postmark/SendGrid + MTProto + WhatsApp Business API | [V0.2] | 🔴 | depends on WS-I. Note: v0.1 Beta BYOK envelope (Anthropic + Groq + Google + OpenAI per CLAUDE.md "Current System State") is already documented and live. |
| First opted-in client for v0.2 R.3 reporting pilot | [V0.2] | 🔴 | operator decision; named only in their own PROJECT_CONTEXT per Law 3, not in Tilth-core artifacts. |

**Operations subtotal:** v0.1 Beta needs Classification Review UX. Spec is LOCKED; operator-facing wrapper is the work.

## 2.6 Documentation

| Box | Tag | State | Evidence |
|-----|-----|-------|----------|
| README + ARCHITECTURE_OVERVIEW + CLAUDE.md updated for v0.2 surface | [V0.2] | 🟡 | v7.0.6 SELF-LOCK companion edits landed council roster updates; v0.2 surface updates pending each LOCK's companion edits. For v0.1 Beta: README + CLAUDE.md + ARCHITECTURE_OVERVIEW need a v0.1 Beta launch posture section (TODO). |
| White-glove onboarding playbook updated for Classification Review + AWARD_INGEST + DC consent capture | mixed | 🔴 | Classification Review + AWARD_INGEST are [BETA]; DC consent capture is [V0.2]. Beta-blocking subset of this row is not yet authored. |
| Operator runbook for v0.2 R.3 reporting cycle | [V0.2] | 🔴 | v0.2 only. |
| Open-decisions log §2 closed (8c–8j resolved or default-confirmed) | mixed | 🟡 | 8c (Uploader portal adapter scope) confirmed default at §12 LOCK; 8d (Archivist pull-forward) confirmed default at §15 LOCK; 8e (sub-awardee shared-secret) + 8f (state-rules) defaults stand pending WS-I open; 8g (CIC×CLC orthogonality) auditing per WS in flight; 8h (proposal_commitments rubric extraction) confirmed default at §11 LOCK; 8i (Report Generator track-binding) + 8j (period-N comparison) defaults stand pending WS-J. |

**Documentation subtotal:** v0.1 Beta needs the README/CLAUDE.md/ARCHITECTURE_OVERVIEW v0.1 Beta launch posture section + white-glove playbook subset for Classification Review + AWARD_INGEST. Cheap, paper-only work.

# 3. Summary — what's green, what flips on WS-L, what stays red

## 3.1 GREEN as of today (post 15 LOCKs rows 178–192)

Architecture: v7.0.4 + v7.0.4-M1 + v7.0.5 + v7.0.6 + v7.0.7 + v7.0.8 (and v7.0.1/v7.0.2/v7.0.3 from prior cycles).
Blueprint: §11 v1 + §12 v1 + §5 v8 + §2 v7.2 + §15 v1 SPEC; all §0.5 paired amendments shipped at compound-LOCK.
Code skeletons: Intake (17 tests) + Uploader (skeleton + adapters) + Archivist (27 tests) + §2 sub-kinds (102 new tests) + §5 track-registry dispatcher (37 tests).
Submission-mode track registry: ACTIVE.

## 3.2 Flips GREEN when WS-L §4 v2.x LOCKs

v0.1 Beta gate items:
- §4 Logician v2.x box itself (the LOCK being awaited).
- "All Logician gates implemented + tested" — flips on WS-L LOCK once all v0.2-family + F-CLASS-* + v7.0.4 KFR + v7.0.8 CIC×CLC gates are registered.
- F-CLASS-COVERAGE-INCOMPLETE PRE-cycle gate releases → Beta deployments can run.

That clears the architectural side of v0.1 Beta. The remaining v0.1 Beta blockers post-WS-L are operator-facing UX + paper:
- Classification Review stage operator-runnable wrapper (UX work).
- Intake full-impl code phase (BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST beyond skeleton).
- Uploader full-impl code phase (real adapter wiring beyond skeleton).
- README + CLAUDE.md + ARCHITECTURE_OVERVIEW v0.1 Beta launch posture section.
- White-glove playbook subset for Classification Review + AWARD_INGEST.

## 3.3 Stays RED — v0.2 cut only (NOT v0.1 Beta blockers)

- §13 Data Collector blueprint (WS-I) + channel modules (5 channels).
- §14 Report Generator blueprint (WS-J) + track-mode module.
- State-rules card (PA/CA/FL/TX/NY).
- BYOK envelope for Twilio + Postmark/SendGrid + MTProto + WhatsApp Business API.
- First opted-in v0.2 R.3 reporting pilot client identification.
- WS-N integration scenarios 3–6 (Data Collector outreach, Report Generator drafting, Uploader full pipeline, Archivist cadences).
- White-glove playbook DC-consent-capture subset.
- Operator runbook for v0.2 R.3 reporting cycle.
- Decisions 8e + 8f + 8i + 8j resolved beyond defaults.

# 4. Critical path to v0.1 Beta deployment

```
WS-L §4 v2.x LOCK (in flight)
    │
    ├──→ Intake full-impl code phase (BULK_INGEST + INCREMENTAL_INGEST + AWARD_INGEST beyond skeleton)
    ├──→ Uploader full-impl code phase (adapter wiring beyond skeleton)
    ├──→ Classification Review stage operator UX wrapper
    └──→ Documentation: v0.1 Beta launch posture (README + CLAUDE.md + ARCHITECTURE_OVERVIEW) + white-glove subset
         │
         └──→ v0.1 Beta deployment-ready
```

Estimated post-WS-L work to v0.1 Beta cut: ~5–8 sessions (3 for Intake/Uploader full-impl + 1 for Classification Review UX + 1 for docs + 1–2 for first dogfood deployment dry run + integration probe).

v0.2 cut requires the above plus WS-I + WS-J + WS-N + operator decisions 8e/8f/8i/8j + DC consent capture playbook + operator runbook. v0.2 cut is weeks-to-months out at current cadence per dispatch plan §8.

# 5. Observations + recommendations

1. **WS-L is genuinely the bottleneck.** Today's 15 LOCKs cleared every other architectural and blueprint blocker for v0.1 Beta. The §6 checklist looks like a wall of red boxes only because most rows are v0.2-cut-only; tagged-by-scope, v0.1 Beta is one LOCK away from architectural completeness.

2. **Skeletons-to-full-impl is the next undercount.** Intake + Uploader passed at SPEC LOCK with skeleton tests. The full-impl code phase (real adapters, real classification gating wired through, real PROJECT_CONTEXT migration script) is not enumerated as a §6 row. Should appear in any v0.1 Beta cut checklist that supersedes this audit's borrowing of §6.

3. **Classification Review UX wrapper is the highest-leverage paper-light v0.1 Beta task.** v7.0.7 makes it mandatory for Beta; spec LOCKED; operator-facing tooling not yet built. Cheaper than another blueprint round and gates first-customer deployment.

4. **§5 v8 report FORWARD-COMPAT row is the right shape.** Submission+eval ACTIVE, report stub refusing at runtime via `F-PIPE-TRACK-NOT-SHIPPABLE` until WS-J LOCK flips `shippable_in: v0.2` to `true`. Track registry dispatcher does not need re-edit when v0.2 lands — only the registry row gets updated. R.PF1 commitment honored.

5. **Open decisions 8e/8f/8i/8j are all default-locked at WS-I/WS-J open.** No operator-decision gate blocks WS-L. Confirm 8h (proposal_commitments extraction owner) honored at §11 LOCK and 8c (Uploader portal scope) honored at §12 LOCK — both done.

6. **v0.1 Beta launch posture document missing.** A "what we ship at v0.1 Beta" surface description (one-pager) does not yet exist in `pipeline/planning/`. Worth authoring post-WS-L as a public-facing scope-pin parallel to this internal audit.

# 6. Audit-trail anchor

This file pairs with daily_log 2026-05-10 and session_metrics entry for the interstitial housekeeping session that produced WS-I + WS-J handoffs alongside it. No LOCK ceremony — informational artifact filed as decision-support for the operator while WS-L Thesis runs.

When WS-L LOCKs, supersede this audit with a v0.1 Beta cut checklist that:
- Drops the v0.2 rows entirely.
- Adds skeleton-to-full-impl rows for Intake + Uploader.
- Adds Classification Review UX wrapper as an explicit Beta gate.
- Adds the v0.1 Beta launch posture documentation row.

End of audit.
