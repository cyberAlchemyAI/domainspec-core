---
title: 48–72h Retrospective — 2026-05-15 → 2026-05-16
date: 2026-05-16
author: Cowork (Claude Opus 4.7)
status: planning artifact; NOT a LOCK ceremony
purpose: snapshot the heavy push that landed between the 5/11 baseline and the 5/16 evening current state; flag what's load-bearing, what's drift, and where the architecture is ahead of the implementation
companion_artifacts:
  - pipeline/planning/current_state_assessment_2026-05-16.md (Codex; broader two-gate framing)
  - pipeline/handoffs/project_wide_reconciliation_audit_prompt_2026-05-16.md (Codex; reconciliation audit prompt)
  - docs/tilth_full_audit_prompt_v1.md (this session; the systematic per-surface audit prompt)
---

# 48–72h Retrospective — 2026-05-15 → 2026-05-16

This is the heavy-push snapshot Josh asked for: state at the 5/11–5/14 baseline, what landed during the 5/15–5/16 surge, what's true on disk now, and the honest read about what's load-bearing vs. what's drifted into ceremony. It is a planning artifact, not a LOCK. Row numbers and file paths are cited so the claims are audit-traceable.

A companion piece — `pipeline/planning/current_state_assessment_2026-05-16.md` (Codex) — covers the same window with a broader two-gate framing (Gate 1 internal replay with Paul / Gate 2 first paid client). This retrospective complements that with workstream-by-workstream attribution, lock_history row-level evidence, and the honest read about architecture-vs-implementation drift.

---

## 1. What we had (~2026-05-11 → 2026-05-14)

**Lock ledger high-water mark on 2026-05-11 evening:** row 213 (architecture v7.0.10 three-posture amendment LOCKED at 20:00Z), capping a cluster of 5/11 evening LOCKs: §17 WPFA v1 + §2 v7.4 Coefficient Registry + §4 v2.x.z WPFA + §0.5 v19 (rows ~205–208 compound quadruple), §11 Intake v1.1 (rows ~209–210), §2 v7.5 + §3 v6 + §4 v2.x.4 funding-goal + §0.5 v20 (rows ~211–214). Source: `pipeline/engineering/lock_history.v1.jsonl` rows <= 213; `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md` for the posture LOCK.

**The five days 2026-05-12 → 2026-05-14 were a deliberate gap.** No daily_logs in `daily_logs/` for those dates; zero LOCK rows in `lock_history.v1.jsonl` with timestamps `2026-05-12*` / `2026-05-13*` / `2026-05-14*`. The next lock_history entry after row 213 is 2026-05-15T14:30:00Z (§16 Reflection Packet v1 LOCK, row 215). The 5/13 reference in this retrospective's title window is calendar-anchored, not work-anchored.

**State at the start of the surge (effective 2026-05-15 morning).** The architecture was on v7.0.10 (three-posture routing canonical: Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign; the "Sanitized" / opaque-slot-token mechanism deprecated; sixteen F-CLASS-* primitives). The §-numbered blueprint was largely LOCKed at v0.1 scope: §11 v1.1, §12, §13 (SPEC LOCKED), §14 v1 (SPEC LOCKED), §15 v1 (Archivist), §16 v1 (Reflection Packet artifact), §17 v1 (WPFA / CycleReceipt), §18 v1 (Card System), §4 Logician at v2.x.4. The Logician carried twelve F-CLASS-* primitives plus the F-WPFA-* and F-PACKET-* families with LIVE shells and predicate bodies still pending realization in several places.

**Known weaknesses going into the surge:**

- **Memory competence** — the 2026-05-11 Architecture Proficiency Assessment scored Dim-8 (memory) at 4/10 and named three Tier-0 Beta-blockers: (1) Reflection Packet v0.2 first-wave activation, (2) unified `tilth memory query` retrieval CLI, (3) MEMORY.md auto-consolidation. Source: `pipeline/planning/architecture_proficiency_assessment_result_2026-05-11.md`.
- **No GitHub CI signal** — the canonical repo `HyphaeNated/GoldenQuill` did not exist yet (it would land 5/15 16:58 EDT as the initial commit `d3bc8b1`). No `.github/`. No PRs. No commit statuses.
- **Sovereignty truth-check pending** — the architecture spoke confidently about local-first / BYOK / boundary enforcement, but the seat-local provider modules (Scribe → Anthropic, Judge → Google, Red Team → Groq) bypassed any shared egress chokepoint. A direct-Anthropic operator glue script (CC-003) lived in the source tree as a fossil.
- **Cards not yet drafted** — §18 v1 LOCKed at architecture level; the actual card YAML fixtures (`pipeline/cards/CIC/food_systems.yaml`, `pipeline/cards/CLC/operating_capacity.yaml`) were v7.0.11 LOCK stubs (~100 lines each), not researched cards.
- **WS-J Slice 3 (Report Generator v0.2 forward-compat row) wiring** — handoff pre-staged at `pipeline/handoffs/ws_j_section_14_slice_3_wiring_2026-05-11.md`, not yet implemented.
- **D-RB-01 (logfire pin gap) + D-RB-02 (process-wide bootstrap shim)** — flagged in `docs/v0_1_beta_deployment_runbook.md` §13, not yet closed.

**Authority docs at the baseline.** `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md` was the active clearance authority (superseding the 5/10 readiness + launch-posture snapshots). v0.1 was scoped to submission-mode + eval-mode; v0.2 (Data Collector + Report Generator runtime) and v1.x (Archivist) were forward-compat rows in the track registry.

---

## 2. What we did (the 48–72h push, 2026-05-15 morning → 2026-05-16 evening)

49 LOCK ceremonies fired between 2026-05-15T14:30:00Z and 2026-05-16T16:00:00Z (`jq` count on `lock_timestamp_utc >= "2026-05-15"`). Lock_history grew from row 213 to row 262, a net +49. Ten major workstreams landed.

### 2.1 Memory triple-fix (Tier-0 items 1, 2, 3)

Three load-bearing closures against the 5/11 Dim-8 4/10 weakness, all 5/15 (Cowork Opus 4.7 / 4.6).

- **Reflection Packet v0.2 first-wave compound LOCK** at 2026-05-15T19:14:53Z. Five-part paired-commit (rows 220–224): §16 v1.1 (producer-binding) + §2 v7.x (Reflection Packet sub-kind registration) + §4 v2.x.y.1 (predicate bodies live) + §15 v2.x (Archivist Reflection sub-mode SPEC) + §0.5 v24 (Interface Index marker). 18 of 19 F-PACKET-* gates remain `NotImplementedError` at v0.1 (DORMANT-pending per OQ-2(a)); 1 LIVE (`F-PACKET-COVERAGE-INCOMPLETE` META-gate). Sub-kind authored at `pipeline/vault/sub_kinds/reflection_packets.py` but NOT registered in the SUB_KIND_REGISTRY (deferred to v0.2 first wave). Audit trail: `daily_logs/2026-05-15.md` line 399 onwards.
- **`tilth memory query` unified retrieval CLI** LANDED 5/15 (Tier-0 item 2). `pipeline/memory/unified_query.py` (~700 lines) + `pipeline/cli/tilth_memory_query.py` (~280 lines) + 49-test suite passing in 0.29s. Pure-Python BM25 Okapi over 13 registers (9 workspace-scoped + 4 per-org). Law-3 isolation at the adapter boundary: per-org adapters refuse on `None` org, reserved-slug `_TEMPLATE`, path-traversal slugs.
- **MEMORY.md auto-consolidation** LANDED 5/15 (Tier-0 item 3). `pipeline/memory/consolidate_index.py` (~480 lines) + `pipeline/cli/tilth_memory.py` (~250 lines, `consolidate-index` verb) + 28-test suite. **Live consolidation executed same session:** MEMORY.md was 36,939 bytes / 94 entries (over the 24,576-byte Cowork loader cap); post-consolidation 20,012 bytes / 15 entries kept, 79 archived to `_archive_2026-05-15.md`. lock_history row 219 (`lock_class=memory_consolidation`).

**Still open:** the "auto" part is operator-invoked at v0.1 Beta; the session-start size-threshold hook is deferred to v1.x (per the spec). Reflection Packet activation in runtime is the v0.2 first-wave deliverable; current pre-staging at `pipeline/handoffs/ws_reflection_packet_v0_2_first_wave_handoff_2026-05-15.md`.

### 2.2 Cards system (Wave 1 + Wave 2)

The single highest-volume workstream of the surge.

- **Wave 1 research dispatch + handback** 5/15 evening (two parallel Cowork Opus 4.7 sessions). Food Systems CIC (TILTH-CIC-01) at `pipeline/cards/CIC/food_systems.yaml` and Operating Capacity CLC (TILTH-CLC-03) at `pipeline/cards/CLC/operating_capacity.yaml`, both ~430 lines, both schema-valid against `pipeline/cards/_schema/card_{cic,clc}.schema.json`, both coupling-clean against the `FORBIDDEN_FIELD_REGISTRY`. 15 + 14 primary sources cited with ≤2-sentence verbatim quotes.
- **Wave 1 handback decision-queue closures** — operator-pinned five §1 parameter-block resolutions (directory case UPPERCASE, lifecycle field `review_status`, `dialect_routing_table` item schema, `frequency_observed` enum on `common_funders_observed`, `provenance_requirements` additionalProperties shape). Five files edited in one batch; jsonschema + AST-lint + 12/12 coverage all PASS.
- **Wave 1 L-005 strict two-cycle cross-family Thesis** CLEARED on both cards (12/12 dispatches, ~12 min wall-clock). Editor=`groq/llama-3.3-70b-versatile` + Judge=`google/gemini-2.5-pro` + Red Team=`groq/openai/gpt-oss-120b`. Disposition: 9 FOLD-IN + 2 DEFER + 1 BOUND + 3 REJECT-with-rationale (Operating Capacity); Food Systems analogous.
- **Wave 1 LOCK ceremony** fired 2026-05-15T20:30:00Z — rows 226–228 (two card LOCKs + §0.5 v25 paired-commit). Ed25519 signatures against operator-pinned publisher pubkey; `lifecycle.signature_status: signed` + `runtime_load_status: loaded` flips.
- **§18 v1.1 narrow-corrective amendment LOCKED** 2026-05-16T01:05:00Z — rows 229–230. Bakes in the five operator-pinned resolutions as schema-level enforcement (CLC schema mirror-edits + item-level `not.anyOf` defense-in-depth on 5 items). L-005 strict two-cycle CLEARED at FULL live cross-family rigor.
- **Wave 1.1 re-pin verification** closed 2026-05-16T05:39:32Z as **NO-OP row 231** (`cards_repin_noop`). The schema-refinement edits had landed *before* Wave 1 ceremony signing, so SHA-3-512 was already canonical; no re-pin needed.
- **Wave 2 research dispatch + Thesis** 5/16 morning–afternoon — 12 cards (5 CIC: Educator, Public Agency, Arts & Culture, Cooperative, Ecosystem Intermediary; 7 CLC: Public Purpose & Works, Catalytic Change, Research & Evidence, Market Access, Credit & Underwriting, Sponsorship & Corporate Support, Shared Assets). Fan-out via Task subagents in 3 batches of 4 (one recovery batch after openclaw gateway 120s timeout saturation). All 12 reached `lifecycle.cross_family_thesis_status: passed`.
- **Wave 2 LOCK ceremony** fired 2026-05-16T16:00:00Z — rows 250–262 (12 card LOCKs + §0.5 v29 narrow-corrective paired-commit). §0.5 v29 is signature_status flip-only (no new namespace registrations; all 14 card namespaces registered at §0.5 v25 rows 537–550). Audit trail: `pipeline/validation/cards_wave_2_lock_ceremony_2026-05-16/`.
- **§18 v1.2 amendment** LOCKED 2026-05-16T14:00:00Z (row 235) as part of the apolitical-dialect compound — see §2.4.

**State on disk:** 14 card YAMLs at `pipeline/cards/` (6 CIC + 8 CLC). `lifecycle.signature_status: signed` + `runtime_load_status: loaded` on all. **Caveat (load-bearing):** `pipeline/cards/loader.py` + `pipeline/cards/validators.py` + most `f_cards_*.py` gates still carry `NotImplementedError` bodies (v0.2 first-wave per architecture v7.0.11 §5). "Loaded" is a governance-lifecycle label, not a runtime-state assertion at v0.1.

### 2.3 CC-007 sovereignty truth-check + provider boundary

The single biggest architectural win of the surge — the sovereignty story moved from "the architecture says so" to "the AST-lint refuses anything else."

- **Architectural preflight design memo** authored 5/16 morning. `pipeline/handoffs/cowork_cc007_preflight_design_memo_2026-05-16.md` (~477 lines) + sibling preflight handoff. Five operator-decision items (OD-1..5) surfaced.
- **§4 v2.x.5 Provider Boundary amendment + §0.5 v27 paired-commit** LOCKED 2026-05-16T08:00:00Z — rows 232–233 (10-row paired-commit). Three runtime modules + Cedar policy + AST-lint rule defined.
- **Companion runtime code LANDED** post-LOCK (5/16, same Cowork session). 11-item code list realized: `pipeline/orchestrator/provider_boundary.py` (OutboundCallable Protocol + wrapper); `pipeline/orchestrator/deployment_posture.py` (three-posture state); `pipeline/vault/classification/signed_register_loader.py`; `pipeline/vault/policies/outbound_boundary.cedar` (text-level Cedar fallback); `pipeline/logician/cedar_engine.py`; `pipeline/linting/r_no_direct_provider_http.py` (AST-lint rule registered in DEFAULT_RULES).
- **§4 v2.x.6 fixture-migration sweep** LANDED post-runtime-companion. Seat-local provider modules (Scribe Anthropic, Judge Google, Red Team Groq) refactored toward the shared `OutboundCallable` shape. Red Team Groq dual-path collapsed.
- **Three architectural deferrals closure pass + cleanup markers** — operator directive to pull forward to v0.1 Beta close. Cedarpy stays deferred ("ok"); routes remaining via text-level Cedar fallback.

**Still open (operator-decision):** OD-5 router legacy `_enforce_cloud_boundary_pre/post` is explicitly deferred — it remains load-bearing alongside the new shared wrapper. Cedarpy integration is v0.2 substrate-addition territory.

### 2.4 v7.0.12 Apolitical-Dialect compound LOCK + Vocab-scrub ceremony

A vocabulary correction that touched the architecture + Logician + cards + Interface Index simultaneously.

- **v7.0.12 Apolitical-Dialect compound LOCK CEREMONY** fired 2026-05-16T13:30:00Z..14:00:00Z. Four-amendment paired-commit at single `lock_timestamp_utc=2026-05-16T14:00:00Z` — rows 234–237: architecture v7.0.12 + §18 v1.2 amendment + §4 v2.x apolitical_dialect amendment + §0.5 v28 paired-commit (4 rows). Retires the four-axis political enum (`conservative` / `centrist` / `progressive` / `soul_fire`) workspace-wide; replaces with CLC-keyed register state. F-DIALECT-* family registered.
- **F-DIALECT-* predicate-realization pass** 2026-05-16T18:45:00Z (Cowork session). Three modules + 74 new tests landed: `pipeline/logician/gates/f_dialect_political_axis_leak.py` (PRE-gate order 6.55, three detection layers — field-name regex + token-based + substring), `pipeline/logician/gates/f_dialect_migration_incomplete.py` (PRE-gate order 6.56), `pipeline/linting/r_no_political_axis_literal.py` (3 Rule instances per glob: cards / types / logician-gates). Test result: 2,878 passed + 15 skipped + 1 warning (sandbox).
- **Vocab-scrub LOCK ceremony** 2026-05-16T14:30:00Z — rows 238–249 (12 `vocab_scrub_supersession` rows). Per operator directive after third slip recurrence + audit of full surface area: the term "cartridge" was retired workspace-wide for forward surfaces. Historical audit trails preserved (e.g., `lock_class=card_cartridge` rows in lock_history stay as audit-only continuity).

**Still open:** the §5 touched-file list (~25 files: substrate code, skill prompts, agent specs, CLAUDE.md, SOUL.md, SESSION_BOOTSTRAP.md) is migration-pending. The 5 "operator plumbing" pieces of the deferred cards-ceremony got pulled forward (`pipeline/institutional_memory/_audit_decisions.py` + `pipeline/scripts/audit_term_signer.py` + scaffolded 91-row `admin_risk_register_audit_decisions.md`) — the operator-content audit on 91 terms is the next operator action.

### 2.5 Platform Engineer onboarding pack for Paul Norton

A non-LOCK living-doc landing — Paul is Josh's incoming platform engineer.

- **`docs/platform_engineer_onboarding.md`** LANDED 5/15 (Cowork Opus 4.7, earlier same day as the WS-J Slice 3 session). Plus `docs/platform_engineer_quick_reference.md`.
- **§1.5 "Rules vs Guidance — Calibration Invitation" section added** 5/15 PM per operator directive. Frames the 80+ failure codes / Cedar policies / AST-lint rules / paired §0.5 rows: *some* is load-bearing (Law-3 isolation / Law-4 admin-risk / fail-closed auto-submit / KFR verbatim-quote provenance) and stays rigid; *some* may be ceremony that constrains LLM reasoning without commensurate safety gain. Surface-candidate protocol: rule location / what it forecloses / replacement guidance language / failure mode if guidance is enough. Explicit non-blanket-permission qualifier — operator weighs sovereignty + Law-protection per change.
- **Companion brief** `docs/paul_norton_memory_alignment_brief_2026-05-15.md` — maps Paul/Brain/JIT onto Tilth's memory weakness.

**Still open:** Paul is not yet onboarded. The pack exists; the kickoff is pending.

### 2.6 Tandem QA/QC remediation (CC-001 … CC-009)

The most consequential audit cycle of the surge — drove eight of the ten remediation handoffs that bracket Gate 1 / Gate 2.

- **Tandem QA/QC pressure-audit prompt** authored + corrected (Codex session 5/16). `pipeline/handoffs/tandem_qa_qc_pressure_audit_prompt_2026-05-16.md`.
- **Pressure audit executed** (Codex session, no repairs). Verdict initially: **ALPHA_READY_FOR_INTERNAL_REPLAY_ONLY**. Audit trail: `pipeline/validation/tandem_qa_qc_pressure_audit_2026-05-16/`. Top 10 findings: packaging excludes runtime modules; Reflection Packet half-activated; cards loaded-but-stubbed; non-green test posture; Judge BLUEPRINT_DEPS hash drift; sovereignty test cascades on host permissions; no CI signal; `data/` 4.9 GB untracked-not-ignored; BYOK doc conflict; Brain/JIT no F-BRAIN/R-BRAIN wrappers.
- **Tandem self-audit + Claude Code half** completed; CI signal validated CC-002. `09_self_audit.md` written.
- **Delta QA/QC pressure audit** completed 5/16 (Codex). Verdict tightened to **NOT_PAUL_READY_AS_A_CLEAN_TECHNICAL_BASELINE** until gate fixes landed.
- **Remediation handoff** authored: `pipeline/handoffs/tandem_qa_qc_remediation_2026-05-16.md` (~190 lines). 10 batched defaults proposed.
- **Operator decisions confirmed** + 7 per-decision handoffs fanned out: `pipeline/handoffs/tandem_qa_qc_remediation_decisions_2026-05-16.md`. CC-001..CC-009 mapped to Gate 1 (PR #2 keepers + CC-003 quarantine + CC-005 doc-fix + TQA-009/010 doc surgery + Logfire disable-by-default) and Gate 2 (CC-004 signed-asset-manifest + CC-007 boundary-injection + CC-008 redaction processor + CC-009 M13 end-to-end + Reflection Packet v0.2 first wave + `R-NO-DIRECT-PROVIDER-HTTP` mature + LIVE/DORMANT manifest).
- **CC-003 quarantine + PR #3 opened** (Codex session 5/16). Direct-Anthropic operator glue quarantined; `R-NO-DIRECT-PROVIDER-HTTP` AST-lint guard added. PR #3 title `ci: land PR2 keepers and CC003 quarantine`. CI run `25963750751` SUCCESS — four jobs green (quality gate × Python 3.11/3.12 + wheel-install CLI smoke × Python 3.11/3.12). Head SHA `2d68a3fc9008f2b9f04078e3deb73bf56c4b9447`.

**Still open:** PR #3 is open + mergeable; not yet merged to origin/main. Local branch `codex-pr2-cc003-cleanup` is ahead 1 / behind 3 relative to its remote. Gate 2 fixes (CC-004, CC-007 finalization, CC-008, CC-009) are in flight per the seven dispatched handoffs.

### 2.7 Beta deployment runbook closures (D-RB-01 + D-RB-02)

- **D-RB-01** — `pyproject.toml` `dependencies` array now pins `"logfire>=0.42"`. Cited in the block-comment with v7.0.4-M1 §8.4.1 mandate + bootstrap-shim entry point + graceful-degrade contract + `LOGFIRE_ENABLED=0` Intake discipline.
- **D-RB-02** — `pipeline/observability/logfire_bootstrap.py` (~230 lines, stdlib-only at import time) authored. `bootstrap_logfire() -> BootstrapResult` is the entry point; wired into `pipeline/__init__.py`. Idempotent. Six terminal outcomes. Graceful degrade: `LOGFIRE_ENABLED=0` → SKIPPED_DISABLED *before* any `import logfire`. 20 new tests + focused v0.1 smoke 339/339 + sovereignty chunk 828+2 skipped + non-sovereignty chunk 9744+1 skipped+1 xfailed+2 pre-existing failures. **Combined: 10,572 passed + 3 skipped + 1 xfailed; zero regressions.**

**Still open:** D-RB-03 (OpenClaw 2026.5.12 available) + D-RB-04 (gateway "no bootstrap files") remain operator-action / investigation respectively. CC-008 (Logfire upload disable-by-default) is a separate handoff under the remediation fan-out.

### 2.8 README hardware cleanup + GitHub private push

- **GitHub remote LIVE** 5/15. Canonical repo `https://github.com/HyphaeNated/GoldenQuill.git` (private). Initial commit `d3bc8b100b30e75f37afcf59483d565ec6ac69e2` 2026-05-15 16:58:41 EDT — "Initial commit: Golden Quill workspace bootstrap" — 1,407 files / 59.3 MB. Author `HyphaeNated <183869525+HyphaeNated@users.noreply.github.com>` (noreply email; no personal email exposure). Pre-push scrub: 6 files of real EINs + home address; 2 client CSVs relocated to `orgs/mystic_mamas/data/`; prior Replit MycoGrant TS app (~33 MB) added to `.gitignore`.
- **README.md cleanup** 5/15 — Pass 1 (Hardware Targets) + Pass 2 (extra-language sweep). Reference SKUs: Apple M3 Ultra Mac Studio, AMD GX-10 class, NVIDIA Spark (DGX Spark / ASUS Ascent GX10). 128 GB floor canonical.

### 2.9 PA foundation funder priorities — full IRS XML pass

- **`pipeline/funder_corpus/pa_foundations.py`** built + run (Codex session 5/15). EO/BMF PA extract (81,374 rows), TEOS XML indexes 2025+2026 (848,341 combined rows), one monthly IRS XML archive (`2026_TEOS_XML_03A.zip`, 247 MB).
- **Outputs** under `data/pa_foundations/processed/` after operator-pinned refinements (asset floor $500k, religious/foreign/scholarship-only out-of-scope filtering, mixed funders stay): 4,316 candidates / 4,245 linked filing rows / 2,064 grant rows / 113 priority funder-year rows / 188 out-of-scope grants excluded ($4.34M).
- **Verification**: minimum `asset_amount` exactly 500,000; verification grep for `SCHOLARSHIP|JEWISH|ISRAEL|CHRIST|CHURCH|AFRICA|CHRISTIAN` returns 0 hits across name/category/keyword columns. Focused tests 7/7.

**Still open:** iterate across all 18 linked 990-PF XML batches; add Form 990 Schedule I extraction for public-charity grantmakers.

### 2.10 FID Phase 1 infrastructure kickoff

- **`pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md`** — the planning authority (504 lines).
- **`pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md`** — dispatch plan (246 lines). Phase 1 active scope = Pillars 1–3 (Depth Charter + corpus assembly + structured extraction); Pillar 4 (field-test calibration via draft comparison) DORMANT pending operator grant-drafting reactivation. Anchor start: Monday 2026-05-18.
- **Directory scaffold** + Depth Charter template + corpus discipline + first-exemplar pre-stage. First FID artifact dispatched: `pipeline/handoffs/fid_exemplar_usda_rd_rbdg_fy26_dispatch_2026-05-16.md` (USDA-RD-RBDG-FY26).
- **Publisher key separation:** dedicated FID Ed25519 keypair (separation-of-concerns from cards-publisher key) — operator generates before first charter signing. Charters can draft unsigned in advance.

**Still open:** the planning-vs-blueprint distinction Josh flagged this evening. FID Phase 1 lives entirely under `pipeline/planning/` + `pipeline/handoffs/`. There is no §-numbered blueprint binding for FID yet. That's correct (Phase 1 = infrastructure + first-exemplar pre-stage, not amendment work), but the dispatch plan does pre-bind operational decisions (publisher key separation, single-exemplar Day-1 dispatch, Pillar 4 dormancy) that a future §-binding round would have to re-litigate or formally ratify.

### 2.11 WS-J Slice 3 (Report Generator) implementation

LANDED 5/15 (Cowork Opus 4.7 session) — `pipeline/orchestrator/tracks/report_mode.py` rewritten per §14.9.0 + first-wave marker hash binding at `pipeline/logician/first_wave_marker.py` (FIRST_WAVE_FUNDER_IDS = {VAPG, NIFA, SARE, EPA_NEETP, SBIR}) + 3 AST-lint rules (`R-REPORT-NO-AUTO-FINALIZE`, `R-REPORT-VAULT-INTENT-REQUIRED`, `R-REPORT-DECIMAL-MANDATE`) + 36 new tests + 3 updated. Test result: 1869 passed + 6 skipped (sandbox). `report_mode` track still gated by `F-PIPE-TRACK-NOT-SHIPPABLE` at runtime (forward-compat row; flips to `shippable_in: v0.2` at WS-J §14 LOCK).

---

## 3. What we have now (state at 2026-05-16 evening)

### 3.1 LOCKed and on disk

- **lock_history.v1.jsonl** at row 264 (264 JSONL lines on disk). The +49 LOCK ceremonies from the surge brought the ledger from 213 → 262, plus the F-DIALECT-* predicate-realization session + the FID Phase 1 dispatch + a few smaller landings.
- **Architecture** v7.0.12 (apolitical-dialect amendment LOCKED at 2026-05-16T14:00:00Z, row 234). Three customer-facing postures canonical (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign); "Sanitized" / opaque-slot-token mechanism deprecated.
- **Blueprint §0.5 Interface Index** at v29 paired-commit (last row 262, 2026-05-16T16:00:00Z). 41 §0.5-amendment files under `pipeline/blueprint/v0.1/` (some interface-index versions; bulk are paired-commits).
- **Blueprint §4 Logician** at v2.x.6 (router-dedup amendment). 22 §4-amendment files. F-CLASS-* (16 primitives) + F-WPFA-* (12 primitives) + F-PACKET-* (19 primitive signatures, 1 LIVE + 18 NotImplementedError-pending) + F-DIALECT-* (live predicate bodies post 18:45Z session) + F-CARDS-* (mostly NotImplementedError pending v0.2 first wave) + F-REPORT-* + F-FG-* + F-CIC-CLC-* + F-GPP-* + F-AMDT-* families registered. **125 `f_*.py` gate modules on disk** (`find pipeline/logician/gates -maxdepth 1 -name 'f_*.py' | wc -l`).
- **Cards** — 14 YAMLs (6 CIC + 8 CLC) at `pipeline/cards/`. All signed, all `runtime_load_status: loaded` (governance label, NOT runtime state). Wave 1 + Wave 2 LOCK ceremonies complete. Audit trails under `pipeline/validation/cards_wave_{1,2}_lock_ceremony_*` and `pipeline/validation/cards_wave_{1,2}_thesis_*`.
- **Provider boundary** code live at `pipeline/orchestrator/provider_boundary.py` + Cedar policy at `pipeline/vault/policies/outbound_boundary.cedar` + `R-NO-DIRECT-PROVIDER-HTTP` AST-lint enforced via DEFAULT_RULES.
- **Memory layer** — `tilth memory query` (BM25 over 13 registers) + `tilth memory consolidate-index` both LANDED + live consolidation executed. MEMORY.md 15 active entries / 79 archived to `_archive_2026-05-15.md`.
- **GitHub** — repo private + initial commit pushed. **PR #3 green** (CI run `25963750751`, four jobs green). **PR #3 not yet merged.**
- **PA foundation corpus** — 4,316-candidate funder dataset locally under `data/`, with docs at `docs/pa_foundation_dataset.md`.

### 3.2 Pending operator decision / pre-staged

- **PR #3 merge to origin/main** — open.
- **OD-5 router legacy `_enforce_cloud_boundary_pre/post` deduplication** — explicitly deferred (CC-007 architectural deferral closure pass).
- **admin_risk_register audit decisions** — 91 terms scaffolded at `pipeline/institutional_memory/admin_risk_register_audit_decisions.md`; operator content audit (audit_status decision + content rebinding) pending.
- **Reflection Packet v0.2 first-wave runtime activation** — pre-staged at `pipeline/handoffs/ws_reflection_packet_v0_2_first_wave_handoff_2026-05-15.md`. Sub-kind module exists but is NOT in SUB_KIND_REGISTRY; 18/19 F-PACKET-* still NotImplementedError.
- **Brain/JIT Shape A/B/C** decision — v0.2 first wave; awaiting alignment-brief next step. No `F-BRAIN-*` / `R-BRAIN-*` enforcement wrappers exist.
- **`runtime_load_status: loaded` cards claim reconciliation** — either fix vocabulary or land F-CARDS loader bodies.
- **Gate-family LIVE/DORMANT manifest** — humans currently infer maturity from docstrings + git history.
- **Paul onboarding kickoff** — pack exists; kickoff pending.

### 3.3 In-flight sessions at the close of this snapshot

- **F-DIALECT-* predicate-realization** session just CLOSED (2026-05-16T18:45:00Z). Plumbing pulled forward in the same session (audit_decisions module + audit_term_signer CLI + scaffolded register).
- **CC-007 v0.2 deferrals cleanup** session — three deferrals pulled forward to v0.1 Beta close; cedarpy stays deferred.
- **Cards Wave 2 LOCK ceremony** — CLOSED (2026-05-16T16:00:00Z). Memory + index updated.

---

## 4. The honest read

This section is the part that matters most. It's the operator-pushback signal.

### 4.1 What's load-bearing

- **CC-007 sovereignty truth-check + provider boundary.** This is the single biggest win of the surge. The "local-first / BYOK" claim moved from architecture text to AST-lint refusal + Cedar policy + Protocol wrapper. Five seat-local provider modules now route through a shared chokepoint. `R-NO-DIRECT-PROVIDER-HTTP` will refuse the next direct-provider-fossil at lint time. Combined with CC-003 quarantine, this closes the most embarrassing pre-surge gap.
- **Memory triple-fix.** The Dim-8 4/10 weakness named at 2026-05-11 is materially closed for v0.1 — query and consolidation CLIs both exist, are tested, and the live MEMORY.md was actually consolidated during the surge. Reflection Packet runtime activation is the v0.2 first-wave deliverable, and the scaffolding is real (sub-kind module authored, 19 F-PACKET-* signatures registered, META-gate body LIVE).
- **Two-gate vocabulary (Gate 1 internal replay / Gate 2 first paid client).** This is a strict improvement over the "Alpha" overload. Codex's `current_state_assessment_2026-05-16.md` made it canonical; the remediation decisions pack maps every CC-* item to one gate.
- **Cards system + apolitical-dialect retirement.** 14 researched cards exist (vs. 2 fixture stubs at the start), each cross-family Thesis'd. The four-axis political enum is gone from the schema, replaced by CLC-keyed register state. F-DIALECT-* bodies are live and tested.
- **GitHub + CI signal.** No GitHub at all → repo pushed + private + PR #3 green across four jobs. Real reproducibility infrastructure now exists.

### 4.2 Where the architecture has gotten ahead of the implementation

This is the part Josh asked me to be plainspoken about.

- **`runtime_load_status: loaded` on every card.** It's a governance lifecycle label, not a runtime state. `pipeline/cards/loader.py` carries `NotImplementedError`. Most `f_cards_*.py` predicates carry `NotImplementedError`. If a customer-facing claim or a Paul-readable doc says "the cards are loaded," that's overclaim. Either rename the lifecycle field (e.g., `lock_status: signed_and_promoted`) or land the loader. The Codex assessment flags this in §3.3 Maturity Table; it's the highest-priority claim-vs-runtime gap.
- **F-PACKET-* family.** 19 signatures registered, 1 LIVE META-gate, 18 raise `NotImplementedError`. The pattern is correct (define the gates at LOCK; activate bodies at v0.2 first wave). But the `F-PACKET-COVERAGE-INCOMPLETE` META-gate body is the *only* enforcement today. A naive reader of `pipeline/logician/gates/` sees 19 modules and assumes coverage. The dormant-vs-live distinction is currently inferable only from reading each predicate body.
- **OD-5 router legacy `_enforce_cloud_boundary_pre/post`.** The new shared provider-boundary wrapper coexists with the old router-internal enforcement. Both are load-bearing today. This is OK for v0.1 (deferred deliberately) but it means there are *two* enforcement paths for the same constraint — one of them is the audit-true source, the other is fossil-pending-removal. The operator decision to defer is recorded; the deferral isn't itself a problem; the *coexistence under the same constraint* needs a lint or a comment header noting which is canonical.
- **§0.5 Interface Index claimed row count vs. on-disk reality.** The lock_history rows say the §0.5 Interface Index is at runtime-live row ~552 (`§0.5 v29 paired-commit; row 538 = 1 marker` → ... → `rows 549–552 = 4 rows`). The actual `pipeline/blueprint/v0.1/section_00_5_interface_index.md` file has 127 table-rows (`grep -c "^|"`). The amendment-file ledger (41 §0.5-prefixed amendment files) has *become* the canonical row store; the .md is the v4 baseline from 2026-04-19. This is the governance-theater concern Josh flagged. The ledger is not invalid — it's auditable, traceable, and signed — but the *human-readable index* is no longer the single-pane-of-glass it was at v4. A future audit needs to consume the per-amendment row enumerations programmatically, not by reading the .md.

### 4.3 Where governance ceremony has accreted

Honest read on the paired-commit pattern: it works, and it's load-bearing for cross-family rigor. It also has a cost.

- **49 LOCK ceremonies in 36 hours.** Most are valid paired-commits — §0.5 v24 (Reflection Packet first-wave: 5-tuple) is real cross-section work, not ceremony. But some are narrower than they look:
  - **Wave 1.1 NO-OP** (row 231) is a *ceremony* row that records "we checked, no re-pin needed." That's defensible audit hygiene (don't silently skip the check) but it's a row whose entire purpose is to make the absence-of-action auditable.
  - **§0.5 v29 narrow-corrective signature_status flip-only** (row 262, Wave 2 paired-commit). Flips 12 lifecycle fields from `unsigned` to `signed`. No new namespaces; no new vocabulary; no new predicates. Defensible — the alternative is silent flips outside the ledger — but it does mean a paired-commit row can be vanishingly thin.
- **The compound paired-commit Option-B pattern** raises the per-change overhead linearly. Apolitical-dialect was a single conceptual change ("retire the four-axis enum") that produced architecture v7.0.12 + §18 v1.2 + §4 v2.x apolitical_dialect + §0.5 v28 — four LOCK rows + ~25-file migration list + 12 vocab-scrub supersession rows + 3-module F-DIALECT-* implementation. That's the *right* surface area for a workspace-wide vocabulary correction. But it's an example of how a small conceptual decision lands as a ~50-row ceremony.
- **41 §0.5-amendment files.** Each is a paired-commit companion to a parent amendment elsewhere. The audit-trail value is real — every row in the lock_history has a path-resolvable amendment file. The cost is that the §0.5 surface is now distributed across 41 files instead of one canonical table. A new auditor cannot answer "what's the current state of the Interface Index?" without a tool. The `tilth memory query` CLI partially solves this (it can query the lock_history register and the memory_files register), but there is no `tilth interface-index render` or `tilth lock-ledger summarize` CLI yet.

### 4.4 Risk of governance theater (specifically)

The §0.5 row-count concern Josh flagged is real but bounded.

- **Real:** the gap between the .md baseline (v4, 127 table rows) and the lock_history-tracked runtime row count (~552 after v29) is large enough that a fresh reader will misread the .md and assume the system is smaller than it is.
- **Bounded:** every claimed row is amendment-file-backed and lock_history-row-anchored. There is no phantom row count. The ledger reconciles.
- **What would tip it into theater:** if a paired-commit landed without a corresponding amendment file, or if an amendment file pre-pinned a behavior that the Logician didn't actually enforce at runtime. Right now neither is happening — every paired-commit row I sampled has a paired amendment .md, and the F-DIALECT-* / F-CLASS-* / F-CARDS-coupling-extension paths actually fire at lint or runtime. The risk is forward-looking: every additional paired-commit raises the auditor's overhead, which raises the chance that a *future* row lands without rigor.

**Recommended mitigation (low-cost):**

1. A `tilth interface-index render` CLI that rebuilds the human-readable .md from the lock_history rows + amendment files. Run it as a CI post-LOCK step or as a session-close hook.
2. A `gate_family_status.yaml` (machine-readable) that lists every F-* family with `LIVE | DORMANT | PARTIAL | NotImplementedError` per primitive, generated from AST-parsing each predicate. Mirror it into the README so customer-facing claims can be grounded.

### 4.5 Planning-vs-blueprint distinction (the FID Phase 1 case)

Josh flagged this specifically. The pattern: a planning doc (`pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md`) and a dispatch plan (`pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md`) pre-bind operational decisions that have not gone through a blueprint Thesis round. Specifically: separate publisher key from cards-publisher, Day-1 single-exemplar dispatch, Pillar 4 dormancy, anchor start 2026-05-18.

This is **correct for Phase 1** (Phase 1 is infrastructure + first-exemplar pre-stage, not amendment work — explicit in the dispatch plan §0). But the cost is that when FID grows into a §-numbered blueprint surface (likely §19 or §3-extension), the future blueprint round will have to either ratify or rewrite the Phase-1 decisions. The pre-binding is *audit-traceable* (planning docs are dated and operator-confirmed), but it's not Thesis-reviewed.

**Recommended discipline:** when a planning doc pre-binds operational decisions, the dispatch plan should explicitly enumerate them as "Phase-1 operating assumptions subject to future §-binding Thesis review." The current FID dispatch plan §0 does this for the four ratified decisions. Good. The watchpoint is the *next* planning doc.

### 4.6 Where local workspace ≠ canonical Git

The local dirty workspace at `/Users/goldenquill/Downloads/GoldenQuill` contains the bulk of the surge work. PR #3 only carries CC-003 quarantine + PR #2 keepers. Specifically:

- 14 card YAMLs are local-only (Wave 1 LOCK + Wave 1.1 NO-OP + Wave 2 LOCK all happened locally, signed against an operator-pinned publisher pubkey, but the YAMLs are not in canonical Git).
- F-DIALECT-* runtime code + 74 tests are local-only.
- CC-007 §4 v2.x.5 + runtime companion + v2.x.6 fixture migration are local-only.
- FID Phase 1 scaffold + dispatch + handoff are local-only.
- PA foundation corpus + `data/` (4.9 GB) is local-only and not yet ignored in canonical Git (PR #3 quarantines but doesn't add an authoritative `.gitignore` rule yet).

The Codex `current_state_assessment_2026-05-16.md` calls this out in §3.2 Brittle. The remediation path is: merge PR #3 → land the Wave 1 + Wave 2 + CC-007 + F-DIALECT-* + FID Phase 1 + PA-corpus-ignore work as a follow-on PR (or several scoped PRs). The risk if not merged soon: future audits will keep producing the same "local says X, canonical Git says Y" finding and the divergence will compound.

### 4.7 Bottom-line

The surge moved Tilth materially closer to **Gate 1 (internal replay with Paul)**. The sovereignty story is structurally true now, the memory weakness is closed for v0.1, the cards substrate is researched and signed (with the lifecycle-label caveat), CI is real, and the two-gate vocabulary has retired the ambiguous "Alpha" framing. Gate 2 (first paid client) is still meaningfully open — CC-004 signed-asset-manifest, CC-007 finalization, CC-008 Logfire redaction processor, CC-009 M13 end-to-end, Reflection Packet v0.2 runtime activation, and the cards loader. These are scoped, dispatched (seven handoffs fanned out), and tractable.

The biggest remaining risk is not technical — it's that the local dirty workspace and the canonical Git history diverge further before a clean reconciliation lands. The second-biggest is the architecture/implementation gap on cards-loaded and F-PACKET-* — both are claim surfaces that a Gate-2 customer or external auditor would probe first, and both currently fail an honest reading.

Sources: `pipeline/engineering/lock_history.v1.jsonl` rows 213–264; `daily_logs/2026-05-15.md` + `daily_logs/2026-05-16.md`; `pipeline/planning/current_state_assessment_2026-05-16.md`; `pipeline/handoffs/tandem_qa_qc_remediation_decisions_2026-05-16.md`; `pipeline/validation/tandem_qa_qc_pressure_audit_2026-05-16/00_executive_verdict.md`; `pipeline/handoffs/cowork_cc007_preflight_design_memo_2026-05-16.md`; `pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md`; CLAUDE.md (operating laws + architectural pins).
