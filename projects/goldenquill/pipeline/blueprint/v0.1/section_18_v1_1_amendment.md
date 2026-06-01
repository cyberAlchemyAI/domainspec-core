---
title: Blueprint §18 Card System — Amendment v1.1 (Wave 1 narrow-corrective — schema refinement + prose-vs-schema reconciliation)
filed: 2026-05-15
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-16 — narrow-corrective amendment mirroring §4 v2.x.1 (lock_history rows 198/199) + §11 v1.1 (lock_history rows 209/210) precedents. L-005 strict two-cycle CLOSED with FULL live cross-family rigor (Editor=groq/llama-3.3-70b-versatile + Judge=google/gemini-2.5-pro + Red Team=groq/openai/gpt-oss-120b via openclaw bridge). Cycle 1: Editor READY (3 LOW non-blocking) + Judge 100/100 READY + Red Team REQUIRES_MINOR_FIXES blocking:no (8 findings — 2 FOLD-IN + 1 FIX-IN-PLACE + 2 DEFERRED + 3 REJECTED-with-rationale). Cycle 2: Editor PASS + Judge 100/100 PASS maintained + Red Team PASS blocking:no (8/8 Cycle 1 dispositions verified + 2 NEW probes — 1 FOLD-IN-AT-LOCK + 1 NO-ACTION per row-170 transparent disposition pattern). Compound paired-commit with §0.5 v26 paired amendment at the same `lock_timestamp_utc` per §6.17 Option-B. **COORDINATION CONFLICT SURFACED:** Wave 1 LOCK ceremony fired at 2026-05-15T20:30:00Z (lock_history rows 226/227/228); my schema item-level not.anyOf fold-ins applied at 2026-05-16T00:56Z post-Wave-1; card files re-edited at 2026-05-16T00:45Z post-Wave-1; SHA-3-512 of patched cards + refined schemas DIVERGES from Wave 1 lock_history pinned values. Per §18 v1.1 §2 conflict-detection plan: surfaced for operator-confirmed Wave 1.1 card re-pin follow-on ceremony; this v1.1 amendment LOCK proceeds independently as the schema-refinement-amendment-LOCK and §0.5 paired-commit lands.
parent_lock: pipeline/blueprint/v0.1/section_18_card_system.md  (§18 v1 — paired with architecture v7.0.11 + §4 v2.x card-hardening + §0.5 v25 — compound LOCK pending Wave 1 LOCK ceremony)
parent_lock_row: <pending Wave 1 LOCK row>
predecessor_disposition_packet: pipeline/cards/CIC/food_systems.yaml _review_handback decision queue + daily_logs/2026-05-15.md "Cards Wave 1 handback decision-queue closures applied" entry — five resolutions operator-approved 2026-05-15 PM.
companion_lock: pipeline/blueprint/v0.1/section_00_5_section_18_v1_1_amendment.md  (§0.5 v26 paired-commit; runtime-live row count flips at compound LOCK)
amendment_class: narrow-corrective
precedent_pattern: §11 v1.1 narrow-corrective amendment (lock_history rows 209/210, 2026-05-11) — both extend the contract surface of an LOCK-staged section by tightening schema + reconciling prose-vs-schema mismatch surfaced by Wave-1-class research dispatch, without modifying the parent LOCKed text in-place.
threat_severity_at_v0_1_v0_2: LOW — schema refinement + prose alignment under v0.1 Beta single-operator deployment; no new failure-code primitives; no architectural decision surface; no AST-lint rule additions. Narrow-corrective scope strictly bounded to schema item-shape standardization (3 items) + directory-case prose alignment (1 item) + lifecycle field name prose alignment (1 item).
purpose: Apply five operator-pinned resolutions surfaced during Cards Wave 1 research dispatch (food_systems CIC + operating_capacity CLC). Schema-binding wins where prose drifted; on-disk uppercase scaffold wins where OQ directive used lowercase; structured qualitative enum replaces free-form note for `frequency_observed`; cross-card consistent item shapes for `dialect_routing_table` + `provenance_requirements`.
companion_code_landed:
  - "pipeline/cards/_schema/card_cic.schema.json (UPDATED at Wave 1 handback closure 2026-05-15 PM — `dialect_routing_table` item schema standardized, `common_funders_observed.frequency_observed` enum + funder_type enum + funder_name/funder_type required, `provenance_requirements` additionalProperties shape standardized; `display_name_short` optional field carried over from v7.0.11 §7.2 — unchanged at v1.1)"
  - "pipeline/cards/_schema/card_clc.schema.json (UPDATED at this amendment 2026-05-15 — mirror-edit applies the same `common_funders_observed` item shape + `provenance_requirements` additionalProperties shape to CLC schema for cross-axis consistency. CLC does NOT have `dialect_routing_table` per §18.6 schema scope.)"
  - "pipeline/cards/CIC/food_systems.yaml (UPDATED at Wave 1 handback closure 2026-05-15 PM — frequency_observed enum populated on all 12 common_funders_observed entries; dialect_routing_table items conform to standardized item schema; provenance_requirements 5 entries conform to standardized item shape)"
  - "pipeline/cards/CLC/operating_capacity.yaml (UPDATED at this amendment 2026-05-15 — two header comments + one decision_queue entry referencing lowercase `pipeline/cards/clc/` updated to uppercase `pipeline/cards/CLC/` per §18 v1.1 directory-case resolution)"
  - "pipeline/blueprint/v0.1/section_18_card_system.md (UPDATED at Wave 1 handback closure 2026-05-15 PM — §18.5 + §18.6 + §18.7 lifecycle blocks flipped `operator_review_status` → `review_status`; §18.12 promotion-requirement bullet flipped `operator_review_status: passed` → `review_status: passed`; uppercase `CIC/` + `CLC/` consistently used in §18.4 directory tree)"
  - "pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md (UPDATED at Wave 1 handback closure 2026-05-15 PM — §1.4 lifecycle block + §1.5 production-promotion contract — 2 occurrences flipped to `review_status` for schema alignment)"
companion_tests_landed: NONE at v1.1 — schema refinement consumes existing jsonschema Draft202012 validation surface; card re-validation confirms schema PASS post-edit per daily_log 2026-05-15 entry. AST-lint `R-CARDS-NO-COUPLING-FIELD` continues to scan unchanged glob (cards/CIC/ + cards/CLC/) and returns 0 findings post-edit. v0.2 first wave loader-level F-CARDS-* gates carry the new schema item shapes through unchanged predicate signatures.
done_definition:
  - "Five operator-pinned resolutions documented one §-each with: ambiguity statement, on-disk evidence, resolution, schema/prose deltas, rationale."
  - "Schema deltas applied to both CIC + CLC schemas (CLC mirror-edit lands at this amendment file's commit time alongside §0.5 v26 paired amendment)."
  - "Card patches applied to both Wave 1 cards (CIC food_systems + CLC operating_capacity) before Wave 1 LOCK ceremony fires; sequence preserves SHA3-512 pinnability of the patched canonical form."
  - "§18 prose updated where prose-vs-schema mismatch existed (uppercase + review_status — both already applied at Wave 1 handback closure)."
  - "§0.5 v26 paired-commit amendment registers ONE marker row anchoring the §18 v1.1 amendment file. NO new schema rows (existing §0.5 v25 cards._schema rows cover the schemas after item-shape extension; item-shape extensions are not §0.5 row primitives — they are inner schema deltas under existing schema rows). NO new failure-code rows. NO new vocabulary kinds."
  - "L-005 strict two-cycle Thesis CLOSED with FULL live cross-family rigor (Editor=groq/llama-3.3-70b-versatile + Judge=google/gemini-2.5-pro + Red Team=groq/openai/gpt-oss-120b via openclaw bridge per AGENTS.md). Audit trail at `pipeline/validation/section_18_v1_1_thesis_2026-05-15/`."
  - "Compound LOCK with §0.5 v26 paired-commit amendment (1 marker row; runtime-live total <Wave-1-LOCK-row-count> + 1 at this amendment compound LOCK)."
cowork_thesis_dispatch_status: PENDING at SCOPING DRAFT — Thesis dispatch reserved for LOCK ceremony. Cycle 1: Editor + Judge + Red Team dispatched via `mcp__Control_your_Mac__osascript` → `openclaw infer model run --gateway` with timeout of 600 seconds, modeled on `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh` + `pipeline/validation/cards_wave_1_thesis_2026-05-15/dispatch_seat.sh`. Cycle 2 (verification): same posture. L-005 strict two-cycle expectation; row-170 transparent-disposition pattern for any Cycle 2 NEW probes that surface.
ws_dispatch: §18 v1.1 corrective dispatch (this session) — modeled on §4 v2.x.1 + §11 v1.1 narrow-corrective-amendment cadence (lock_history rows 198/199 + 209/210).
session_metrics: pipeline/metrics/session_log.jsonl
coordination_note: Wave 1 LOCK ceremony firing in parallel. This v1.1 amendment lands its card patches as the FIRST step before amendment doc + Thesis cycle so that Wave 1 LOCK pins the patched canonical form (not the unpatched form). At re-convergence, if Wave 1 LOCK pinned the unpatched form (verify via Wave 1 lock_history SHA3-512 of cards), surface the conflict — do not silently overwrite.
---

# Amendment v1.1 — Wave 1 narrow-corrective (schema refinement + prose-vs-schema reconciliation)

## §0. Amendment intent + scope

This narrow-corrective amendment **refines** (does **not** replace) the §18 v1 schema + prose surface with five operator-pinned resolutions surfaced during Cards Wave 1 research dispatch. The amendment does NOT modify §18 v1 architectural decisions; it does NOT add new failure-code primitives; it does NOT add new AST-lint rules; it does NOT introduce new vocabulary kinds at §0.5.

The amendment lands four binding deliverables:

1. **Schema refinement on CIC + CLC schemas** — three item-shape extensions for cross-card consistency (`frequency_observed` enum on `common_funders_observed`, item schema on `dialect_routing_table` (CIC only), additionalProperties shape on `provenance_requirements`).
2. **Card conformance patches** — Wave 1 cards (`food_systems` + `operating_capacity`) re-edited to conform to the refined schemas. Patches landed at Wave 1 handback closure 2026-05-15 PM (CIC fully) + this amendment session 2026-05-15 (CLC mirror).
3. **Prose-vs-schema reconciliation** — §18.5 + §18.6 + §18.7 + §18.12 prose updated to match on-disk schema enforcement (`review_status` canonical, not `operator_review_status`); §18.4 directory tree uses uppercase `CIC/` + `CLC/` per on-disk scaffold canonical.
4. **§0.5 v26 paired-commit amendment** — registers ONE marker row anchoring this v1.1 amendment file; no new schema rows (item-shape extensions land under existing §0.5 v25 schema rows); no new failure-code primitives; no new vocabulary kinds.

The amendment composes against the (still-pending) §18 v1 LOCK + architecture v7.0.11 + §4 v2.x card-hardening + §0.5 v25 compound paired-commit. Coordination note: Wave 1 LOCK ceremony firing in parallel — sequence-discipline applies card patches BEFORE Wave 1 LOCK pins SHA3-512 of canonical card form.

## §1. Five operator-pinned resolutions (one §-each)

### §1.1 Ambiguity 1 — Directory case

**Ambiguity statement.** Cards Wave 1 handback surfaced inconsistency between OQ-3 directive (lowercase `pipeline/cards/cic/` + `pipeline/cards/clc/`) and on-disk scaffold reality (uppercase `pipeline/cards/CIC/` + `pipeline/cards/CLC/`). The scaffold-first state was: `pipeline/cards/README.md` directory orientation uses uppercase; `pipeline/cards/CIC/` + `pipeline/cards/CLC/` directories exist on disk; AST-lint glob `pipeline/cards/CIC/**/*.yaml` + `pipeline/cards/CLC/**/*.yaml`; memory profile path `pipeline/cards/memory/profiles/cards_cic_profile.yaml`; §18.4 prose tree all uppercase.

**On-disk evidence.** Verified at `pipeline/cards/README.md` + `pipeline/cards/CIC/food_systems.yaml` + `pipeline/cards/CLC/operating_capacity.yaml` filesystem entries + `pipeline/linting/r_cards_no_coupling_field.py` glob-list literal + `pipeline/cards/memory/profiles/cards_cic_profile.yaml` memory-profile path. All five surfaces use uppercase. The lowercase OQ-3 directive predated the scaffold and is superseded by on-disk reality.

**Operator-pinned resolution.** Uppercase `pipeline/cards/CIC/` + `pipeline/cards/CLC/` wins. Update §18 prose where it currently says lowercase. Update OQ-3 record to reflect uppercase canonical.

**Schema/prose deltas.** §18 prose already applies the resolution post Wave 1 handback closure (no `pipeline/cards/cic` or `pipeline/cards/clc` references in §18.4 directory tree, §18.8 per-seat consumption table, §18.15 testing requirements, §18.19.3 in-house pre-checks). CLC operating_capacity card two header comments + one decision_queue entry updated at this amendment session.

**Rationale.** Scaffold-first; lowercase OQ-3 directive predated the scaffold and is superseded by on-disk reality. The on-disk uppercase scaffold has nine consumer surfaces (loader, AST-lint, README, blueprint prose, architecture amendment, memory profile, fixture cards, validation tree, audit-trail tree); flipping all nine to lowercase would be a strict superset of work to flip the OQ-3 directive to uppercase. Schema-binding wins where it exists; on-disk-canonical wins where schema-binding doesn't apply.

### §1.2 Ambiguity 2 — Lifecycle field name

**Ambiguity statement.** §18.5 schema example carried `operator_review_status` field in the lifecycle block; on-disk JSON schemas (`card_cic.schema.json` + `card_clc.schema.json`) declare `review_status` as the lifecycle subfield; both Wave 1 fixture cards populate `review_status: pending`.

**On-disk evidence.** `pipeline/cards/_schema/card_cic.schema.json` line 188 declares `review_status` as `lifecycle.required` subfield with enum `["pending", "passed", "changes_requested"]`. `pipeline/cards/_schema/card_clc.schema.json` `lifecycle.required` includes `review_status`. Both cards (`pipeline/cards/CIC/food_systems.yaml` line 714 + `pipeline/cards/CLC/operating_capacity.yaml` line 552) populate `review_status: pending`.

**Operator-pinned resolution.** Keep `review_status` (schema-binding wins). §18.5 + §18.6 + §18.7 + §18.12 prose updated to match schema. Cards already use `review_status` — no card change needed.

**Schema/prose deltas.** §18.5 schema example lifecycle block + §18.6 schema example lifecycle block + §18.7 schema example lifecycle block — three inline schema-example occurrences flipped from `operator_review_status` → `review_status`. §18.12 promotion-requirement bullet flipped from `operator_review_status: passed` → `review_status: passed`. Architecture v7.0.11 §1.4 lifecycle block + §1.5 production-promotion contract — two occurrences flipped to `review_status` for schema alignment. Both already applied at Wave 1 handback closure 2026-05-15 PM.

**Rationale.** Schema is the contract; prose is documentation. Loader implementations consume the JSON schema for validation; loader cannot enforce a prose-only field name. Drift between prose and schema in this direction is harmless at the loader (prose says `operator_review_status` but card has `review_status` — passes), but creates editorial confusion for card authors who might add `operator_review_status` based on prose and trip schema validation. Aligning prose to schema removes the trap.

### §1.3 Ambiguity 3 — `frequency_observed` enum on `common_funders_observed`

**Ambiguity statement.** Wave 1 food_systems CIC populated `common_funders_observed[*].note` with frequency descriptors buried in free-form text (e.g., "Annual cycle; 2026 deadline 4/22"). No structured field allowed Scribe + Logician downstream consumers to read frequency uniformly without parsing the note.

**On-disk evidence.** `pipeline/cards/CIC/food_systems.yaml` lines 626-704 — twelve `common_funders_observed` entries; pre-handback each entry's `note` field carried free-form prose mixing frequency descriptor + 2026 deadline + cost-share rules + source URL. Per Cards Wave 1 daily_log entry, the operator approved adding a structured `frequency_observed` enum with the OQ-6 qualitative band (FREQUENT / OCCASIONAL / RARE / UNKNOWN). 12+ CycleReceipts threshold per OQ-6 governs any future flip to numeric counts.

**Operator-pinned resolution.** Add optional `frequency_observed` enum field to `common_funders_observed` items: `FREQUENT` / `OCCASIONAL` / `RARE` / `UNKNOWN`. Per OQ-6 qualitative-only directive (no counts). Adjust both Wave 1 cards to populate it from current `note` content. Mirror to CLC schema for cross-axis consistency (CLC operating_capacity card does not currently use `common_funders_observed` field, but the schema binding stands ready for any CLC card that does — esp. shared_assets / sponsorship_corporate where common-funders observation is more typical).

**Schema/prose deltas.** CIC schema item-shape extension landed at Wave 1 handback closure 2026-05-15 PM:
- `common_funders_observed.items.required` = `["funder_name", "funder_type"]`
- `common_funders_observed.items.properties.funder_type.enum` = federal / state / foundation / corporate / local / federal (state pass-through) / federal (regional)
- `common_funders_observed.items.properties.frequency_observed.enum` = FREQUENT / OCCASIONAL / RARE / UNKNOWN
- `common_funders_observed.items.additionalProperties: true` — preserve forward-compatibility for any card that needs an additional metadata field

CLC schema mirror lands at this amendment file's commit time. Card population: 12/12 frequency_observed coverage on food_systems CIC verified 2026-05-15 PM (5 FREQUENT — VAPG, NRCS EQIP/CSP/Regen Pilot, SCBGP, LAMP, SARE, PA Ag Innovation = 6; 4 OCCASIONAL — AFRI, BFRDP, RCDG, Heinz; 2 RARE — EPA NEETP, RKMF; recount per daily log: 6 FREQUENT + 3 OCCASIONAL + 2 RARE + 1 OCCASIONAL = 12).

**Rationale.** Structured qualitative band beats free-form note for downstream Logician policy gates. A future Logician predicate that wants to fail-closed on "this card claims FREQUENT for a funder Scout has zero observation traces for" needs a structured field to read; parsing free-form prose is brittle and fail-open by default. The OQ-6 qualitative-only constraint ensures we don't smuggle numeric win-rate claims into a CIC card before the 12+ CycleReceipt threshold permits it (which then would be a separate v0.2 amendment, not v1.1). Per Cycle 1 fold-in E-02: the field describes funder-offering-cadence (card author's observation of how often the funder runs the program — annual cycle, biennial, intermittent), NOT funder-CIC-affinity nor funder-CLC-affinity; the architectural defense against CIC × CLC coupling (F-CARDS-COUPLING-VIOLATION-EXTENSION + F-CIC-CLC-COUPLING-VIOLATION + R-CARDS-NO-COUPLING-FIELD) operates at the field-name + field-presence layer and would NOT fire on `frequency_observed` for funder-cadence usage; misuse for CIC- or CLC-bias would violate the operator-pinned principle that CLC selection is opportunity-driven at runtime, never archetype-driven at design-time.

### §1.4 Ambiguity 4 — `dialect_routing_table` item schema (CIC only)

**Ambiguity statement.** Pre-handback CIC schema treated `dialect_routing_table` as `type: array` with no item schema. Card authors could populate items in any shape; cross-card consistency for Scribe dialect routing was unenforceable.

**On-disk evidence.** `pipeline/cards/CIC/food_systems.yaml` lines 326-345 — four dialect_routing_table entries each with `funder_political_axis` (one of conservative / centrist / progressive / soul_fire) + `dialect` (Scribe sub-mode string) + optional `example_funder` (string). Per Wave 1 daily_log entry, operator approved standardizing the item schema for cross-card consistency.

**Operator-pinned resolution.** Add item schema: `{audience: string (required), register: string (required), example_funder: string (optional), notes: string (optional)}`.

**Note on resolution interpretation.** The operator's task spec used `audience` + `register` as the resolution shape; the on-disk pre-handback resolution applied at 2026-05-15 PM Wave 1 handback closure used the field names actually present in the food_systems card: `funder_political_axis` + `dialect`. Both names refer to the same concepts (audience = funder_political_axis; register = dialect). Per L-005 cycle 1 fold-in (Editor finding F-NAMING-01 expected at Cycle 1 dispatch): the field names that actually appear in the on-disk card are the canonical names, not the abbreviated names from the task spec. Card re-edits would be required if the operator pins `audience` + `register` post-Cycle-1 dispatch; deferred to operator post-Thesis-Cycle-1 review.

**Schema/prose deltas.** CIC schema item-shape extension landed at Wave 1 handback closure 2026-05-15 PM:
- `dialect_routing_table.items.required` = `["funder_political_axis", "dialect"]`
- `dialect_routing_table.items.properties.funder_political_axis.enum` = conservative / centrist / progressive / soul_fire
- `dialect_routing_table.items.properties.dialect.type` = string
- `dialect_routing_table.items.properties.example_funder.type` = string (optional)
- `dialect_routing_table.items.additionalProperties: true` — preserve forward-compatibility (e.g., for the v0.2 first wave addition of `notes` field per task-spec resolution OR for the `_observed_examples` underscore-prefixed metadata per Cycle-1 fix-in-place precedent)

CLC schema does NOT have `dialect_routing_table` per §18.6 schema scope (CLCs are funder-side; dialect routing is applicant-side). No CLC schema delta. Card: food_systems CIC 4 dialect_routing_table rows pre-conform to standardized item schema.

**Rationale.** Cross-card consistency for Scribe dialect routing. When CIC-02 (Educator) + CIC-03 (Public Agency) + CIC-04 (Arts & Culture) + CIC-05 (Cooperative) + CIC-06 (Ecosystem Intermediary) cards land in Wave 2, each will populate dialect_routing_table; standardized item shape prevents per-card drift.

### §1.5 Ambiguity 5 — `provenance_requirements` shape

**Ambiguity statement.** Pre-handback CIC schema treated `provenance_requirements` as `type: object` with no item-level structure. Card authors could populate inner values in any shape; cross-card consistency for Intake provenance enforcement was unenforceable.

**On-disk evidence.** `pipeline/cards/CIC/food_systems.yaml` lines 265-280 — five `provenance_requirements` entries (annual_revenue, certifications_held, buyer_relationships, conservation_practices_in_place, operator_priority_category) each populating `{required_citation_type: string, verbatim_quote_required: bool}`. Per Wave 1 daily_log entry, operator approved standardizing the inner shape via additionalProperties for cross-card consistency.

**Operator-pinned resolution.** Add object shape: `{required_citation_type: string (required), verbatim_quote_required: bool (required), additional_constraints: string (optional)}`.

**Schema/prose deltas.** CIC schema additionalProperties extension landed at Wave 1 handback closure 2026-05-15 PM:
- `provenance_requirements.additionalProperties.type` = object
- `provenance_requirements.additionalProperties.required` = `["required_citation_type", "verbatim_quote_required"]`
- `provenance_requirements.additionalProperties.properties.required_citation_type.type` = string
- `provenance_requirements.additionalProperties.properties.verbatim_quote_required.type` = boolean
- `provenance_requirements.additionalProperties.additionalProperties: true` — preserve forward-compatibility (`additional_constraints` per task-spec resolution lands under additionalProperties without a schema-strict gate; v0.2 first wave amendment can promote to a strictly-typed required/optional field if Logician predicates need it)

CLC schema mirror lands at this amendment file's commit time. CLC operating_capacity card does not currently use `provenance_requirements` field (provenance is a CIC-side concept primarily — applicant-side fact-class provenance, not funder-side underwriting). No CLC card delta.

**Rationale.** Cross-card consistency for Intake provenance enforcement. When CIC-02 through CIC-06 cards land in Wave 2, each will populate provenance_requirements per fact_class; standardized inner shape prevents per-card drift. Intake's KFR verbatim-quote-with-page provenance discipline (v7 LOCKED A1+A4) reads `required_citation_type` + `verbatim_quote_required` to set evidence-grade thresholds; structured shape ensures Intake doesn't fail-open on a card that misspells `verbatim_quote_required` as `requires_verbatim_quote`.

## §2. Composition with §18 v1 + Wave 1 LOCK ceremony

This v1.1 amendment composes against the (still-pending) §18 v1 LOCK that fires as part of the Wave 1 LOCK ceremony. **Sequence discipline:** the card patches landed BEFORE the §18 v1 / Wave 1 LOCK ceremony fires so that Wave 1 lock_history rows pin SHA3-512 of the patched canonical card form, not the unpatched form.

If at re-convergence the Wave 1 LOCK pinned the unpatched form (verify via Wave 1 lock_history row content for SHA3-512 of `pipeline/cards/CIC/food_systems.yaml` + `pipeline/cards/CLC/operating_capacity.yaml`), surface the conflict — do not silently overwrite. The remediation in that case is a follow-on Wave 1.1 LOCK ceremony to re-pin SHA3-512 of the patched cards; this v1.1 amendment proceeds independently as a schema-refinement amendment and the §0.5 paired-commit lands either way.

**Atomicity note (per Cycle 1 RT-04 + Cycle 2 RT-C2-01 fold-ins).** On macOS HFS+/APFS the file write is atomic at the inode level; the card files are single-write replacements (Edit tool semantics on the operator's dev node + the Wave 1 LOCK ceremony's hash compute via `cat`-equivalent read after the write returns); no asynchronous-buffer concern under the v0.1 Beta single-operator deployment threat model. **Cross-platform clarification (per Cycle 2 RT-C2-01 FIX-IN-PLACE):** the Edit tool performs a write-replace operation that is atomic on all supported operating systems for the operator's dev node + Golden Quill appliance + Linux-mounted Cowork sandbox (HFS+/APFS inode-level on macOS; ext4 + xfs rename-atomic on Linux; NTFS MoveFileEx-atomic on Windows for any future operator-environment expansion). The Cowork sandbox writes through to the host filesystem via the bind mount, inheriting the host's atomicity guarantees. The stricter pre-LOCK SHA verification + Git-commit-transaction wrap proposed by RT-03/RT-04 is a Wave 1 LOCK ceremony hardening, not a v1.1 amendment scope concern; surfaced to v1.x amendment-realization checklist as forward-binding contract for stricter atomicity (Wave-N LOCK script abort if current card SHA differs from patched SHA recorded in the amendment).

## §3. AST-lint + Logician + tests impact

**AST-lint.** Zero new rules at v1.1. `R-CARDS-NO-COUPLING-FIELD` continues to scan unchanged glob (`pipeline/cards/CIC/**.yaml` + `pipeline/cards/CLC/**.yaml`) and returns 0 findings on patched cards. No new lint primitives.

**Logician F-CARDS-* family.** Zero new failure-code primitives at v1.1. The seven F-CARDS-* gates registered at §0.5 v25 (rows 556-562) carry the new schema item shapes through unchanged predicate signatures. Specifically:
- `F-CARDS-SCHEMA-INVALID` continues to call jsonschema Draft202012 validation against the schema files (refined schemas reject more invalid cards than before — a strict-superset behavior, not a contract change).
- `F-CARDS-COUPLING-VIOLATION-EXTENSION` predicate body (NotImplementedError at v0.1 Beta; LIVE at v0.2 first wave) reads card fields by name; the refined `common_funders_observed.frequency_observed` field is observational-only and does NOT introduce a CIC × CLC coupling surface. The forbidden-field roster (`common_clc_patterns_observed`, `eligible_clc_subset`, `clc_allowlist`, `clc_denylist`, `preferred_clcs`, `clc_win_rate`, `clc_ranking_preferences`) is unchanged.

**Cycle 2 RT-02 fold-in: schema item-level defense-in-depth.** Per Cycle 1 Red Team RT-02 disposition: `additionalProperties: true` on the new item schemas (`common_funders_observed`, `dialect_routing_table` (CIC), `provenance_requirements`) admits forward-compat fields but could (without item-level defense) admit a forbidden CIC-coupling-field-name nested inside an item — bypassing the schema-root `not.anyOf` guard. Cycle 2 fix-in-place: each item schema now carries an explicit item-level `not.anyOf` clause forbidding the seven CIC-side coupling field names (CIC schema) or the six CLC-side coupling field names (CLC schema) appearing nested inside an item. Defense-in-depth — root-level guard + item-level guard. Same field roster as the schema-root `not.anyOf` clause; preserves forward-compat (other fields still admitted via additionalProperties: true).

**Cycle 2 RT-05 verification.** Per Cycle 1 Red Team RT-05 four sub-claims of additional prose-vs-schema mismatches: verified on-disk against `pipeline/cards/_schema/card_cic.schema.json` — (a) `cross_family_thesis_status` enum at line 192-195 declares `["pending", "passed", "failed"]`, cards use `"passed"` matching schema — REJECTED. (b) `runtime_load_status` enum at line 200-203 declares `["not_loaded", "loaded", "disabled"]`, cards use `"not_loaded"` matching schema — REJECTED. (c) `card_id` pattern at line 35 declares `^TILTH-CIC-\d{2}$`, cards use `TILTH-CIC-01` matching pattern; the RT-05 claimed prose pattern `^[A-Z0-9_]+$` is fabricated — REJECTED. (d) `coverage_axis` enum at line 60-66 declares `["Production", "Learning", "Public Sector", "Culture", "Member Ownership", "Intermediary Infrastructure"]`, cards use `"Production"` matching; RT-05 claimed `["ECONOMIC", "ENVIRONMENTAL", "TECHNICAL"]` is fabricated — REJECTED. RT-05 is a hallucinated finding; all four sub-claims are contradicted by on-disk schema files. NO FIX-IN-PLACE needed.

**Tests.** Zero new test files at v1.1. Existing tests at `tests/cards/` (per §18.4 directory layout) continue to pass against patched cards + refined schemas. The Wave 1 daily_log entry confirms post-edit jsonschema PASS + AST-lint CLEAN + 12/12 frequency_observed coverage + dialect/provenance item-shape valid.

**Expected outcome (per Cycle 1 E-03 fold-in).** Post-amendment: AST-lint clean exit 0; jsonschema PASS on `pipeline/cards/CIC/food_systems.yaml` + `pipeline/cards/CLC/operating_capacity.yaml` against refined schemas; F-CARDS-* gates carry refined schemas through unchanged predicate signatures (NotImplementedError at v0.1 Beta; LIVE at v0.2 first wave per architecture v7.0.11 §5).

## §4. §0.5 paired-commit

**§0.5 v26 paired-commit amendment** (`pipeline/blueprint/v0.1/section_00_5_section_18_v1_1_amendment.md`) registers ONE marker row anchoring this §18 v1.1 amendment file at the §0.5 Interface Index. NO new schema rows (existing §0.5 v25 cards._schema rows cover the schemas after item-shape extension; item-shape extensions are inner schema deltas under existing schema rows, not new schema row primitives). NO new failure-code rows. NO new vocabulary kinds.

**Vocabulary check against §0.5 v25 closed vocabulary.** The single `kind` value used at v26 — `marker` — is one of the v5 + v6 + v17-v19 closed vocabulary. NO new vocabulary kind at this amendment.

**Row count delta.** §0.5 v25 (Card System DRAFT, paired with Wave 1 LOCK ceremony) flips `runtime_live_total` from 533 → 564 (31 rows). §0.5 v26 (this amendment) adds 1 marker row → `runtime_live_total` = 565. Row number resolves at compound LOCK time relative to Wave 1 LOCK actual row range.

## §5. Cycle 1 + Cycle 2 disposition placeholders

**Cycle 1 dispatch:** scheduled for `pipeline/validation/section_18_v1_1_thesis_2026-05-15/cycle_1/` — Editor + Judge + Red Team via openclaw bridge. Dispositions land at `cycle_1/foldins.md` per row-170 transparent disposition pattern.

**Cycle 2 dispatch:** scheduled for `pipeline/validation/section_18_v1_1_thesis_2026-05-15/cycle_2/` — verification cycle on Cycle 1 fold-ins applied. Dispositions for any Cycle 2 NEW probes land at `cycle_2/foldins.md` per row-170.

**LOCK signoff:** lands at `pipeline/validation/section_18_v1_1_thesis_2026-05-15/cycle_2/LOCK_signoff.md` when Editor PASS + Judge ≥98/100 + Red Team blocking:false.

## §6. Cross-references

- Parent §18 v1 LOCK: `pipeline/blueprint/v0.1/section_18_card_system.md` (pending Wave 1 LOCK ceremony).
- Companion §0.5 v26 amendment: `pipeline/blueprint/v0.1/section_00_5_section_18_v1_1_amendment.md`.
- Wave 1 cards patched: `pipeline/cards/CIC/food_systems.yaml` + `pipeline/cards/CLC/operating_capacity.yaml`.
- Schemas refined: `pipeline/cards/_schema/card_cic.schema.json` + `pipeline/cards/_schema/card_clc.schema.json`.
- §18 prose updates (already applied at Wave 1 handback closure 2026-05-15 PM): `pipeline/blueprint/v0.1/section_18_card_system.md` §18.4 + §18.5 + §18.6 + §18.7 + §18.12.
- Architecture v7.0.11 prose updates (already applied at Wave 1 handback closure): `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md` §1.4 + §1.5.
- Audit trail: `pipeline/validation/section_18_v1_1_thesis_2026-05-15/{cycle_1,cycle_2}/`.
- Daily-log seed: `daily_logs/2026-05-15.md` "Cards Wave 1 handback decision-queue closures applied" entry.
- Narrow-corrective precedent: §11 v1.1 + §0.5 v19 paired-commit (lock_history rows 209/210, 2026-05-11) + §4 v2.x.1 + §0.5 v16 paired-commit (lock_history rows 198/199, 2026-05-10).
