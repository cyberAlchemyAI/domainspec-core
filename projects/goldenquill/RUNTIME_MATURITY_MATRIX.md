---
title: Runtime Maturity Matrix — Golden Quill / Tilth
filed: 2026-05-17
basis: cleanup plan v1.1 Track 3 seven-state taxonomy at docs/github_product_truth_cleanup_plan_v1_1_2026-05-17.md §"Track 3 — Runtime maturity labeling"
source_of_truth_rule: one label per system per doc. Any other doc making a claim about a system below cites *this* row, not the other way around. Promotion requires dated evidence — CI/test proof for runtime changes; a lock_history row only when the promoted state changes a LOCKed, signed, or governance-bound artifact.
companion: PROJECT_STATUS.md (the "what works today" snapshot anchored to these states) · pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md (current-vs-superseded §-blueprints)
---

# Runtime Maturity Matrix

The taxonomy is seven states. Reading order is monotonically increasing maturity from `dormant` / `historical` (no live posture) → `schema-scaffold` → `spec-locked` → `asset-signed` → `gate-live` → `runtime-live`. `historical` and `dormant` sit outside the maturity axis (one is an audit-preservation state; the other is a known-future-not-now state); they are listed here so a doc making a claim about *any* surface has a single home for it.

The seven states are codified in cleanup plan v1.1 Track 3 (six in v1, plus `spec-locked` inserted between `schema-scaffold` and `gate-live`; `signed asset` renamed to `asset-signed` for status-verb consistency).

---

## `runtime-live`

The code path is enforced at runtime, exercised by CI on every PR, and would fire on a real customer call today. Fail-closed where applicable. Tests cover the live path deterministically.

- **Provider-boundary outbound enforcement** — `pipeline/orchestrator/provider_boundary.py` `enforce_outbound_boundary` wrapper. LOCKed at §4 v2.x.5 (lock_history row 232, 2026-05-16). The §4 v2.x.6 router-dedup runtime companion landed in main on 2026-05-17 per `daily_logs/2026-05-17.md` — single-wrapper boundary, dual implementation retired, `_dispatch_with_classification_boundary` constructs the wrapper-instrumented `http_post` at every call site. Verified by `tests/orchestrator/` (66 passed in 0.54s, daily_log 2026-05-17).
- **AST-lint provider-call discipline** — `pipeline/linting/r_no_direct_provider_http.py` with the `.direct_provider_call_without_wrapper` sub-tag landed at §4 v2.x.6 §11.1. Fires on any `_call_anthropic` / `_call_openai_style` Call that omits the `http_post=` keyword. Verified by `tests/linting/` (267 passed in 6.50s, daily_log 2026-05-17).
- **F-CLASS-* routing-gate family** — `pipeline/logician/gates/f_class_*.py`. Fail-closed under non-local-only posture when posture / register load fails. Includes `F-CLASS-ROUTING-INDETERMINATE`, `F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL`, `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD`, `F-CLASS-SLOT-ID-NON-OPAQUE`, `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` (the latter two LIVE as defense-in-depth post-Sanitized-deprecation).
- **Six-seat council dispatch path** — Scout / Scribe / Editor / Judge / Red Team / Logician. Cross-family rigor enforced at dispatch (reviewer's model family ≠ author's per L-003). Exercised by 3,004 passing tests under `tests/seats/` per daily_log 2026-05-17 (3 failures are pre-existing capstone-hash drift from in-flight WIP, NOT regressions).
- **Sovereignty primitives** — `pipeline/sovereignty/` (boot, isolation, audit, admin_risk, project_context_envelope, rfa_envelope, router_integrity, session, topology). §1 Sovereignty Envelope LOCKed-as-a-whole at v6 (Round J 2026-04-18).

## `gate-live`

The Logician gate body is LIVE — `evaluate()` returns a real verdict, the predicate enforces, tests exercise it deterministically — but the runtime call site that would invoke it on real customer data is not yet wired or not yet exercised on the production path. Gate fires inside the test substrate; production execution waits on a downstream landing.

- **`F-CARDS-COUPLING-VIOLATION-EXTENSION`** — `pipeline/logician/gates/f_cards_coupling_violation_extension.py`. Predicate body graduated from `NotImplementedError` to LIVE three-layer scan (field-name registry + recursive value-position regex + matrix-card structural rule) at OD-C / §4 v2.x.7 (lock_history row 272, 2026-05-17). Backfill scan 14/14 PASS post-OD-C `sponsorship_corporate.yaml` FIX-IN-PLACE. Runtime card loader is `NotImplementedError` per architecture v7.0.11 §5; the gate fires in tests, not yet at customer card-load time.
- **F-cards-* family (ten gates)** — `f_cards_unsigned_production_load`, `f_cards_private_data_in_card`, `f_cards_schema_invalid`, `f_cards_signature_invalid`, `f_cards_malformed_lifecycle`, `f_cards_coverage_incomplete`, `f_cards_cross_org_namespace_leak`, `f_cards_load_in_wrong_namespace`, plus the two coupling-violation gates. All landed at the Wave 1 + Wave 2 mega-commit `a71f841`. The gates exercise correctly in tests; the runtime loader at architecture v7.0.11 §5 is `NotImplementedError`, so the gates do not fire on real customer card loads at v0.1.
- **F-dialect-* family (apolitical-dialect gates)** — landed at architecture v7.0.12 + §4 logician `v2_x_apolitical_dialect.md` (lock_history rows 234 + 236, 2026-05-16). Gate code present; runtime call-path partial at v0.1.
- **F-FACT-DRIFT / F-LOGICIAN-FACT-DRIFT** — `pipeline/logician/gates/f_logician_fact_drift.py`. Body LIVE; runtime call-site partial at v0.1.

## `asset-signed`

The asset exists, is operator-signed (Ed25519 against the cards-publisher pubkey pinned at `vault_shared/cards/publisher_pubkey.signed.yaml = 0b1a0bbf…6f375bd`), is in the tree, and the signature verifies — but no runtime path loads it for real customer execution at v0.1. Signed-loaded-governance, NOT runtime-injected.

- **Cards Wave 1 + Wave 2 YAML cards** — `pipeline/cards/CIC/{food_systems, educator, public_agency, arts_culture, cooperative, ecosystem_intermediary}.yaml` + `pipeline/cards/CLC/{operating_capacity, public_purpose_works, catalytic_change, research_evidence, market_access, credit_underwriting, sponsorship_corporate, shared_assets}.yaml`. Wave 1 LOCK rows 226 + 227 (2026-05-15); Wave 2 LOCK rows 250–261 (2026-05-16); OD-E supersession-re-sign rows 276 / 277 / 278 (2026-05-17). Embedded `_research_metadata.ed25519_signature` per card; per-card `lifecycle.lock_history_row` cross-reference.
- **Card schemas** — `pipeline/cards/_schema/card_cic.schema.json` + `card_clc.schema.json`. Loader-time validation deferred to v0.2 first-wave per architecture v7.0.11 §5.
- **Cards-publisher pubkey** — `vault_shared/cards/publisher_pubkey.signed.yaml`. Pinned trust root for all card + amendment + lock_history-row signatures at v0.1.
- **§0.5 interface-index paired-commits** — every blueprint-amendment chain entry from §0.5 v5 onward is a signed paired-commit. Latest: §0.5 v32 (LOCK row 275, 2026-05-17); §0.5 internal index runtime-live row count now 541. The §0.5 chain is the canonical signed governance ledger for the blueprint amendment surface.
- **Per-org classification register** — operator-curated + Ed25519-signed during white-glove Classification Review. F-CLASS register + routing gates fail-close any cycle without a signed register. The register-loader at `vault/classification/signed_register_loader.py` (335 lines, landed in PR #4) wires the trust chain.

## `spec-locked`

The specification has landed and is LOCKed via the blueprint amendment chain (lock_history row written, signed if applicable), but the implementation is pending. The spec is more than a scaffold and less than a gate. *New state in cleanup plan v1.1; the canonical example was §4 v2.x.6 runtime companion, which has since landed as `runtime-live`.*

- **§13 Data Collector** — `pipeline/blueprint/v0.1/section_13_data_collector.md` + `section_00_5_section_13_data_collector_amendment.md`. Post-award outreach channel substrate (email + SMS + voice + Telegram + WhatsApp). v0.2 horizon. Spec LOCKed; runtime channel adapters not in tree.
- **§14 Report Generator** — `pipeline/blueprint/v0.1/section_14_report_generator.md` + `section_00_5_section_14_report_generator_amendment.md`. Funder-ready reports via `report_mode` track. v0.2 horizon.
- **§15 Archivist + §15 v2.x archivist-reflection amendment** — LOCK row 224 (2026-05-15). Long-running curation, lessons memory, audit trail. v1.x horizon per README.
- **§16 Reflection Packet + §16 v1.1 amendment** — LOCK rows 216 (v1, 2026-05-15) + 221 (v1.1, 2026-05-15) + §0.5 v22/v24 paired-commits rows 218 + 225. Sub-kind authored at v1.1; activation truth pending operator architectural decision (cleanup plan v1.1 "needs engineering judgment").
- **§17 Watts-Per-Funding-Action** — `section_17_watts_per_funding_action.md` LOCK row 205 + §17 v1 amendment row 207 (2026-05-11) + §0.5 v19 paired-commit row 208. WPFA failure-code family LOCKed; runtime integration v0.2.
- **§4 v2.x.7 card-coupling extension** — LOCK row 272 (2026-05-17 / OD-C). The amendment is LOCKed; the gate body is LIVE (`gate-live`); the runtime call site that triggers the gate on customer card loads is v0.2 first-wave.
- **§18.6 v2 dual-track CLC schema** — LOCK row 274 + recovery row 279 (2026-05-17 / OD-E). Schema-shape-extension for dual-track CLCs. Three CLC cards restructured + supersession-re-signed (rows 276/277/278). Runtime card loader still `NotImplementedError`.
- **§18.11 v1.1 fold-in discipline checklist** — LOCK row 270 (2026-05-17 / OD-D). Documentation-only narrow-corrective; zero runtime enforcement teeth.

## `schema-scaffold`

The shape exists. The fields are named. The tests cover the shape. Implementation is partial or stubbed. No LOCK ceremony has elevated it to `spec-locked` yet — or a LOCK ceremony exists for a parent surface but the specific scaffold here is sub-LOCK.

- **`pipeline/funder_intelligence/`** — corpus discipline real; curation engine partial. Schema fields are named (FunderProfile / FunderHistory / FunderProgramRule); the runtime Match Database query path is v0.2.
- **`pipeline/funder_corpus/`** — PA-foundation dataset (data + tests). Schema-locked per README capabilities table; the runtime Match Database query is v0.2 (`docs/pa_foundation_dataset.md` is the operator-facing scope note).
- **Operational data sub-kinds** — metrics / financials / photos / narrative_entries / timeline / beneficiary_records / attachments. Schema-locked per README; data ingestion is v0.2.
- **State-rules card scaffold** — `pipeline/orchestrator/state_rules_card.py` (post-rename from `state_rules_cartridge.py`). Per-state rule packs (PA / CA / FL / TX / NY) are v0.2; the module shape is present.
- **Match Database / KFR shape** — workspace-shared + per-org reasoning trail schema is named at architecture v7.0.x; runtime curation v0.2.

## `dormant`

Code or doc exists but is not exercised, not on a near-term roadmap, and not load-bearing. Documented so a future contributor knows not to delete it and not to mistake it for a current-truth surface.

- **Reflection Packet sub-kind in `SUB_KIND_REGISTRY`** — §16 v1.1 row 221 + §0.5 v24 row 225 LOCK the sub-kind. The sub-kind is **authored but NOT in `SUB_KIND_REGISTRY`** at v0.1 runtime. Future-activation depends on operator architectural decision (Reflection Packet activation truth, cleanup plan v1.1).
- **Sanitized fourth-posture original drafting path** — deprecated at architecture v7.0.10 LOCK. The cloud Scribe drafting-against-slot-tokens path is *not* exercised; the two defense-in-depth gates (`F-CLASS-SLOT-ID-NON-OPAQUE`, `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED`) remain `runtime-live` as bug-or-attack signals, but the posture itself is dormant.
- **Brain / JIT research surface** — research-only per cleanup plan v1.1 Track 1; no runtime path; not on the v0.1 / v0.2 roadmap.
- **`apps/` directory** — exists at root; not load-bearing for v0.1 product surface per a quick directory survey. Documented in case a contributor wonders.

## `historical`

Captured for audit / prior-art preservation. Explicitly not the current truth. Files in this category are *preserved* (per AGENTS.md discipline) so the audit trail remains intact; they are not deleted, but they are also not current.

- **`pipeline/validation/v7_0_5_thesis_2026-05-09/`** and similar dated thesis-validation directories. Preserved per AGENTS.md.
- **Superseded blueprint files** — `section_00_5_interface_index.v1_preserved_2026-04-18.json`, `section_00_5_interface_index_locked_v2_2026-04-18.md`, `section_02_vault_topology_v4_2026-04-16.md`, `section_02_vault_topology_v7_2026-04-18.md`, `section_04_logician_v2_2026-04-18.md`, `section_05_pipeline_v3_2026-04-18.md`, `tilth_architecture_locked_v{4,5,6,7}_*.md`, `section_1_sovereignty_envelope_v5_2026-04-17.md`, etc. Each was the head at its dated moment; superseded by a later LOCK chain entry.
- **Deleted `state_rules_cartridge.py`** — post-rename to `state_rules_card.py` per the cartridge→card vocab supersession ceremony (lock_history rows 238–249, 2026-05-16). The rename is captured in the vocab_scrub_supersession_ceremony lock-class rows.
- **`king_midas_external_review_brief_2026-04-29.md`** — root-level dated external-review artifact. Historical context.
- **`Improvement_Plan_2026-05-04.md`** — root-level dated planning artifact. Historical context.
- **`CTO_Review_2026-05-04/`** — dated external-review directory. Historical context.

---

## Operating rules

- **One label per system per doc.** A surface cannot be `asset-signed` in one place and `runtime-live` in another. This matrix is the arbiter; other docs cite, they do not redeclare.
- **Promotion requires dated evidence.** CI / test proof for runtime changes (a green run on the commit that wires the runtime). A `lock_history` row **only when the promoted state changes a LOCKed, signed, or governance-bound artifact**. Lightweight matrix corrections — fixing a mislabeled status, refining a description — get a dated entry in `PROJECT_STATUS.md` and do not need a ledger row.
- **`historical` is preservation, not deletion.** A file that moves to `historical` stays in the tree. The state means "audit-trail-preserved, not current truth." Deletion requires a separate operator decision and is not implied by the state label.
- **`dormant` is not a parking lot.** Surfaces enter `dormant` because they are *known-future-not-now* (Reflection Packet sub-kind in registry, Sanitized posture). A surface that is in flight belongs in `spec-locked`, `gate-live`, or `runtime-live`, not `dormant`.
