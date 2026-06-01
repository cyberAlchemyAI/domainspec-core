---
title: Golden Quill / Tilth — Project Status
filed: 2026-05-17
snapshot_basis: lock_history.v1.jsonl logical row 279 (physical line 283) · daily_log 2026-05-17 · PR #4 (`product-github-housekeeping`) CI green on Python 3.11 + 3.12
maturity_vocabulary: RUNTIME_MATURITY_MATRIX.md (7-state taxonomy — `runtime-live` / `gate-live` / `asset-signed` / `spec-locked` / `schema-scaffold` / `dormant` / `historical`)
companion_index: pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md
posture: calm-front-door snapshot. Anchored to evidence (file paths, row numbers, test counts). Designed to go stale fast — dated, then refreshed.
---

# Project Status — Golden Quill / Tilth

## Current state in plain language

Golden Quill is a one-week-old (initial commit 2026-05-15) private monorepo carrying a serious, expensively-architected sovereign funding-intelligence product called **Tilth**. PR #4 (`product-github-housekeeping`) is the canonical product landing path — it contains PR #3 verbatim plus the Cards Wave 1 + Wave 2 architecture, ten new Logician F-cards-* gates, the §4 v2.x.5 / v2.x.6 router refactor, and the §18 card-system amendments — and it is CI-green on the Python 3.11 + 3.12 wheel-smoke + lint + AST-lint + serial-pytest matrix as of operator-confirmed 2026-05-17. The repository's *engineering surface* is well ahead of its *human-readable surface*; the cleanup plan at `docs/github_product_truth_cleanup_plan_v1_1_2026-05-17.md` Track 2 (navigation) — of which this file is the front-door artifact — exists to close that gap without damaging anything LOCKed or historical.

## What works now (runtime-live)

These surfaces are exercised on every PR's CI run; they would fire on real customer execution today.

- **Provider-boundary enforcement.** `pipeline/orchestrator/provider_boundary.py` carries the `enforce_outbound_boundary` wrapper LOCKed at §4 v2.x.5 (lock_history row 232, 2026-05-16). The §4 v2.x.6 router-dedup runtime companion landed in main on 2026-05-17 per `daily_logs/2026-05-17.md` — `_enforce_cloud_boundary_pre` / `_enforce_cloud_boundary_post` are DELETED from `pipeline/orchestrator/router.py`, the wrapper is the sole boundary, and `_dispatch_with_classification_boundary` constructs the wrapper-instrumented `http_post` at every call site. Verified by `tests/orchestrator/` → **66 passed in 0.54s**.
- **AST-lint provider-call discipline.** `pipeline/linting/r_no_direct_provider_http.py` carries the `.direct_provider_call_without_wrapper` sub-tag added at §4 v2.x.6 §11.1. Fires on any `_call_anthropic` / `_call_openai_style` call that omits the `http_post=` keyword. Verified by `tests/linting/` → **267 passed in 6.50s**.
- **Six-seat council dispatch path.** Scout / Scribe / Editor / Judge / Red Team / Logician. Cross-family rigor enforced at dispatch (reviewer's model family ≠ author's). Tests under `tests/seats/` exercise this on every PR — current count **3,004 passed / 3 failed**, where the three failures are pre-existing capstone-hash drift from in-flight WIP (operator confirmed, NOT regressions from any LOCK ceremony — see daily_log 2026-05-17 §"§4 v2.x.6 runtime companion landed" verification block).
- **Logician F-* gate suite.** `pipeline/logician/gates/` contains 137 gate modules covering F-CLASS-* routing, F-INTAKE-*, F-UPLOADER-*, F-cards-*, F-dialect-*, F-PIPE-*, F-WPFA-*, F-PACKET-*, F-LOGICIAN-* families. The §4 v2.1 Logician core LOCKed 2026-04-19 (committee Round-A); the F-CLASS-* family is fully runtime-live and gates routing decisions on customer data today.
- **Cross-PR aggregate test pass count.** PR #4 head merge commit (`4288d16`) reports `10,584 passed / 3 skipped / 1 xfailed` under the serial-pytest matrix CI runs (per the form/function analysis at `docs/github_form_and_function_analysis_2026-05-16.md` §3.2).
- **Sovereignty primitives.** `pipeline/sovereignty/` (boot, isolation, audit, admin_risk, project_context_envelope, rfa_envelope, router_integrity, session, topology). The §1 Sovereignty Envelope LOCKed-as-a-whole at v6 (multi-row chain ending Round J 2026-04-18).

## What's spec-locked but not yet runtime

The §-blueprint amendment chain has LOCKed these specs (lock_history row written, signed where applicable) — implementation is pending. See `ACTIVE_BLUEPRINT_INDEX.md` for the current-head amendment per section.

- **§4 v2.x.7 card-coupling-extension predicate (LOCK row 272, 2026-05-17 / OD-C).** The `F-CARDS-COUPLING-VIOLATION-EXTENSION` predicate body has graduated from `NotImplementedError` to LIVE three-layer scan (field-name registry + recursive value-position regex + matrix-card structural rule). The gate fires inside `tests/` substrate today; the runtime call site that would invoke it on customer card loads is v0.2 first-wave per architecture v7.0.11 §5.
- **§18.6 v2 dual-track CLC schema (LOCK row 274 + recovery row 279, 2026-05-17 / OD-E).** Schema-shape-extension for dual-track CLCs (Option A top-level `track_a:` / `track_b:` containers). Three CLC cards (`market_access`, `credit_underwriting`, `sponsorship_corporate`) have been restructured + supersession-re-signed under the new shape (rows 276 / 277 / 278). Runtime card loader still NotImplementedError per architecture v7.0.11 §5; loader graduation is v0.2 first-wave.
- **§18.11 v1.1 fold-in discipline checklist (LOCK row 270, 2026-05-17 / OD-D).** Documentation-only narrow-corrective. Zero runtime enforcement teeth at this amendment (no failure-codes, no AST-lint, no schema delta, no card patches). Forward-binds the OD-B + OD-C runtime-enforcement realization contracts.
- **§13 Data Collector + §14 Report Generator + §15 Archivist + §16 Reflection Packet first-wave.** Section files exist at `pipeline/blueprint/v0.1/section_13_data_collector.md`, `section_14_report_generator.md`, `section_15_archivist.md`, `section_16_reflection_packet.md`. §15 v2.x archivist+reflection amendment LOCKed at row 224 (2026-05-15). §16 v1.1 LOCKed at row 221 + §0.5 v24 paired-commit at row 225. Implementation is explicitly v0.2 / v1.x horizon (see "not in scope at v0.1" below).
- **§17 Watts-Per-Funding-Action (LOCK rows 205 + 207, 2026-05-11).** Coefficient registry + WPFA failure-code family LOCKed. Runtime integration is v0.2.
- **§11 v1.1 Intake amendment (LOCK row 209, 2026-05-11) and §2 v7.4 / v7.5 coefficient-registry / funding-goal amendments (rows 206 + 211).** Specs LOCKed; the BULK_INGEST + INCREMENTAL_INGEST + AWARD_INGEST runtime modes are §11 v1 substrate, present; the v1.1 fold-ins are pending the white-glove-deployment runtime.

## What's signed-asset / governance-state-only

These are Ed25519-signed governance artifacts. They sit in the tree, signatures verify, the operator's pinned cards-publisher pubkey at `vault_shared/cards/publisher_pubkey.signed.yaml = 0b1a0bbf…6f375bd` is the trust root — but **no runtime path loads them for real customer execution at v0.1**. The card loader graduation to live-load is v0.2 first-wave per architecture v7.0.11 §5.

- **Cards Wave 1 (LOCK rows 226 + 227, 2026-05-15) — `food_systems.yaml`, `operating_capacity.yaml` at `pipeline/cards/CIC/` + `pipeline/cards/CLC/`. §0.5 v25 paired-commit row 228.**
- **Cards Wave 2 (LOCK rows 250–261, 2026-05-16) — five additional CIC cards (`educator`, `public_agency`, `arts_culture`, `cooperative`, `ecosystem_intermediary`) + six additional CLC cards (`public_purpose_works`, `catalytic_change`, `research_evidence`, `market_access`, `credit_underwriting`, `sponsorship_corporate`, `shared_assets`). §0.5 v29 paired-commit at row 262.** Subsequent OD-E supersession-re-sign on three of these (rows 276 / 277 / 278) after §18.6 v2 dual-track restructure.
- **Card schemas.** `pipeline/cards/_schema/card_cic.schema.json` + `card_clc.schema.json` (signed; loader-time validation deferred to v0.2 first-wave).
- **Classification register.** Operator-curated + Ed25519-signed during white-glove Classification Review. `vault_shared/cards/publisher_pubkey.signed.yaml` carries the cards-publisher trust root; per-org signed registers ship at white-glove. The F-CLASS register and routing gates fail-close any cycle without a signed register.
- **Card lifecycle ledger entries.** Each card carries `lifecycle.lock_history_row` cross-references (e.g., `market_access.yaml` row 258 → supersession_lock_history_row 276 after OD-E).
- **§0.5 interface index paired-commits.** Every blueprint amendment chain entry from §0.5 v5 onward is a signed paired-commit. Latest: §0.5 v32 (LOCK row 275, 2026-05-17) — runtime-live row count in §0.5 internal index now 541.

## What's deliberately not in scope at v0.1

These surfaces are *known-future*. The amendment chain documents them; the runtime path is intentionally inactive at v0.1 so the engineering effort can converge on the submission stack first.

- **Data Collector (§13).** Post-award outreach (email + SMS + voice + Telegram + WhatsApp). Compliance-first (CAN-SPAM, TCPA, per-recipient consent). v0.2 horizon. Section + amendment present at `pipeline/blueprint/v0.1/section_13_data_collector.md` + `section_00_5_section_13_data_collector_amendment.md`; runtime channel adapters are not in the tree.
- **Report Generator (§14).** Funder-ready reports via `report_mode` track. Section + amendment present; runtime is v0.2.
- **Archivist (§15) + Reflection Packet first-wave (§16).** §15 archivist+reflection amendment LOCKed row 224; §16 v1 + v1.1 LOCKed rows 216 + 221. Long-running curation, lessons memory, audit trail. Implementation is v1.x horizon — explicitly marked "SPEC LOCKED (proposes-only)" in README.
- **Reflection Packet sub-kind in registry.** §16 v1.1 row 221 + §0.5 v24 row 225 LOCK the sub-kind; the sub-kind is **authored but NOT in `SUB_KIND_REGISTRY`** at v0.1 runtime per the cleanup-plan dormant-surface convention.
- **State-rules card (PA / CA / FL / TX / NY).** v0.2 horizon. `pipeline/orchestrator/state_rules_card.py` (post-rename from `state_rules_cartridge.py`) is present as schema-scaffold; per-state rule packs are v0.2.
- **BYOK envelope for Twilio / Postmark / MTProto / WhatsApp Business API.** v0.2 horizon. Tied to Data Collector channels.
- **Fourth-posture "Sanitized" cloud-drafting path.** Deprecated at architecture v7.0.10 LOCK. Two enforcement gates (`F-CLASS-SLOT-ID-NON-OPAQUE` + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED`) remain LIVE as defense-in-depth — either firing is a bug-or-attack signal.
- **Brain / JIT research.** Research-only per cleanup plan v1.1 Track 1; no runtime path.

## What's open for v0.2 / v1.x horizon

- **Runtime card loader graduation** (loader currently `NotImplementedError` per architecture v7.0.11 §5). Folds in: F-CARDS-SIGNATURE-INVALID firing at a real call site, F-CARDS-COUPLING-VIOLATION-EXTENSION firing at card-load time (today fires only in test substrate), signed-register loader trust chain, supersession-re-sign sweep for the three OD-E cards whose embedded signatures went stale during the FIX-IN-PLACE / dual-track restructure.
- **Heavy-Judge swap exercise.** On-demand local 200B-class heavy-Judge pre-loaded at white-glove. Cloud routing of the heavy-Judge binary is structurally absent (`F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD`). Gate 2 (first paid client) blocker.
- **Local-Only / Sovereign posture validation.** `local_only_validated` deployment-manifest field gates "production-validated" customer-facing claims. Currently marked "performance-dependent / under validation" in README per architecture v7.0.10.
- **§4 v2.x.7 follow-ons.** Surfaced in daily_log 2026-05-17: post-fill-draft check moved into wrapper PRE (requires new §4 v2.x.5 amendment to modify LOCKed `provider_boundary.py`); `R-NO-CLOUD-LIKE-LOCAL-PROVIDER` AST-lint per §12.1; property-based drift test per §13.4 RT-C2-04; lock_history row-number collision audit (rows 234/235 appear twice).
- **Reflection Packet activation truth.** Pending operator architectural decision per cleanup plan v1.1 Track 5 "needs engineering judgment" surface.

## Today's freshness

- **lock_history.v1.jsonl** at `pipeline/engineering/lock_history.v1.jsonl` — 283 physical lines, max logical row **279**.
- **Latest LOCKs (all 2026-05-17):**
  - Row 270 — **§18.11 v1.1 fold-in discipline** (OD-D) · `pipeline/blueprint/v0.1/section_18_11_v1_1_fold_in_discipline_amendment.md`
  - Row 271 — **§0.5 v30 paired-commit** for OD-D · `section_00_5_section_18_11_v1_1_amendment.md`
  - Row 272 — **§4 v2.x.7 card-coupling-value-position** (OD-C) · `section_04_v2_x_7_card_coupling_value_position_amendment.md`
  - Row 273 — **§0.5 v31 paired-commit** for OD-C · `section_00_5_section_04_v2_x_7_amendment.md`
  - Row 274 — **§18.6 v2 dual-track schema** (OD-E) · `section_18_6_v2_dual_track_amendment.md`
  - Row 275 — **§0.5 v32 paired-commit** for OD-E · `section_00_5_section_18_6_v2_amendment.md`
  - Rows 276 / 277 / 278 — **CLC card supersession-re-sign** (market_access / credit_underwriting / sponsorship_corporate)
  - Row 279 — **post-ceremony §18.6 v2 status-flip supersession** (recovery row; preserves audit-trail integrity per OD-D row 269 supersession-of-row-241 pattern)
- **Latest runtime landing:** §4 v2.x.6 router-dedup runtime companion landed in main repo on 2026-05-17 per daily_log §"§4 v2.x.6 runtime companion landed." Backing LOCKs at rows 232 / 234 / 235 (2026-05-16).
- **Latest daily_log entry:** `daily_logs/2026-05-17.md` — 189 lines covering OD-D + §4 v2.x.6 runtime companion + OD-C + OD-E ceremonies in narrative order.
- **PR #4 head commit:** `4288d16 test: refresh capstone hash pins` — CI green on Python 3.11 + 3.12 wheel-smoke + lint + AST-lint + serial-pytest.

## Next reads

A new collaborator landing here should read these five — in this order — before opening anything else.

1. **`README.md`** — product narrative + Five Laws + council + three deployment postures + Hardware Targets.
2. **`RUNTIME_MATURITY_MATRIX.md`** *(root, this snapshot's sibling)* — the 7-state honesty layer. Every claim in any doc that uses "loaded" / "live" / "ready" / "signed" should resolve to a row in this matrix.
3. **`pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md`** — current-head amendment per §-section, with lock_history row citations. The blueprint directory has 110+ amendment files; this index tells the reader which is the head without opening any LOCKed amendment file.
4. **`docs/COLLABORATOR_HANDOFF.md`** *(authored by sister session)* — "what is this, what works, what's safe to touch, how to propose work."
5. **`docs/AGENT_CONTEXT_INDEX.md`** *(authored by sister session)* — map of the root wake-up files (`AGENTS.md`, `SOUL.md`, `USER.md`, `MEMORY.md`, `CLAUDE.md`, `HEARTBEAT.md`, `IDENTITY.md`, `SKELETON.md`, `TOOLS.md`, `lessons.md`). Read this before opening any of the eleven root personification files.

The cleanup plan that motivates this navigation layer is `docs/github_product_truth_cleanup_plan_v1_1_2026-05-17.md` (v1.1, ten tracks). The form/function analysis underneath it (C+ → A grading context) is `docs/github_form_and_function_analysis_2026-05-16.md`.
