# FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2

**Phase 8 sections 1-5 of the Tilth Card System Deep Research run, 2026-05-17.**

| Field | Value |
|---|---|
| Filed | 2026-05-17 |
| Workspace | `/Users/goldenquill/Downloads/GoldenQuill/` |
| Scope | Concrete file-level patch queue to land before v0.2 first-wave loader graduation. Grouped by file path. Each entry: current state, proposed change, ceremony shape, parent_lock_row, ceremony_parent_row placeholder, lock_timestamp_utc bucket, no-LOCK-from-this-dispatch disclaimer. |
| Phase boundary | Phase 8.1-5 only. Phase 8.6 (release readiness), 8.7 (customer trust documentation), 8.8 (CTO synthesis) are OUT of Run 1 scope. |
| What this is NOT | A LOCK ceremony. A git commit plan. A code patch. This is a patch-queue **plan** — the operator dispatches each ceremony separately. |
| Authority | Phase 1 + Phase 2 + Phase 3 findings, this run, plus the LOCK precedents at OD-A/C/D/E rows 250-279 of `pipeline/engineering/lock_history.v1.jsonl` (as referenced by the master prompt §0). |

---

## §0. How to read this document

Each patch entry has six fields:

- **File:** target path.
- **Current state:** what's on disk now, with cite.
- **Proposed change:** what the patched file should contain, with reference to the amendment-of-record where applicable.
- **Ceremony shape:** what kind of LOCK ceremony is needed — paired-commit-compound, supersession-re-sign, documentation-only, code-graduation, or no-LOCK-required.
- **Parent lock(s):** the lock_history row(s) this patch depends on or supersedes.
- **Ceremony parent row placeholder:** `<NEXT-AVAILABLE>` — the operator's next ceremony's compound parent row.

Patches are grouped into **five batches**. Each batch lands at one `lock_timestamp_utc` (or carries zero LOCK ceremony if documentation-only). Operator dispatches each batch as a separate session per `AGENTS.md` lane discipline.

**Non-negotiable from operator corrective:** `common_funders_observed` is operator-confirmed engagement only. Any patch touching this field must enforce the split between operator-confirmed engagement (top-level field) and subagent-populated candidates (`_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`).

---

## §1. Batch A — Documentation-only patches (no LOCK ceremony required)

These are sidecar edits + comment-only updates that do not invalidate any `content_hash` and do not require operator signing.

**Ceremony shape:** None. Sidecar / cosmetic edits only.
**Lock_timestamp_utc bucket:** Not applicable.
**Disclaimer:** No LOCK initiated from this batch. Engineering can land in a normal review cycle without operator-Ed25519 ceremony.

### Patch A1 — Master prompt §5 stale lifecycle-gap claim

- **File:** `docs/cic_clc_unified_master_prompt_2026-05-17.md`
- **Current state:** Lines 394-420 declare "Verified on disk 2026-05-17. All 14 card YAMLs (6 CIC + 8 CLC) carry `lifecycle.draft_status: 'draft'`." This is false per Phase 1 §3.2.
- **Proposed change:** Replace §5 paragraph with: *"Verified on disk 2026-05-17. All 14 card YAMLs (6 CIC + 8 CLC) carry `lifecycle.draft_status: 'signed'`; the supersession-re-sign ceremony for draft_status normalization fired before this run (verify via `grep '^  draft_status:' pipeline/cards/CIC/*.yaml pipeline/cards/CLC/*.yaml` → 14 hits, all `signed`). The §CC-N normalization recommendation in `docs/cic_clc_unified_batch_supervisor_prompt_2026-05-17.md` §6 is no longer needed and can be retired."*
- **Cross-update:** Edit `docs/cic_clc_unified_batch_supervisor_prompt_2026-05-17.md:160-172` to retire the proposed §CC-N normalization, OR repurpose it as a "lifecycle-comment-header normalization" item to address Phase 1 §5 stale-header-comment drift.
- **Phase 3 cross-ref:** P0-3.

### Patch A2 — README typography fix (Cards/Cards collision)

- **File:** `pipeline/cards/README.md`
- **Current state:** Lines 9-11 render both visual layer and runtime layer as bold `**Cards**`. The naming distinction the architecture amendment calls "load-bearing" is invisible at the README surface.
- **Proposed change:** Adopt distinguishable typography:
  ```
  **Cards** = visual / conceptual layer (human-readable; PNGs at `assets/cards/customer_identification/` + `assets/cards/capital_logic/`).
  **cards** = runtime layer (machine-readable; this directory).
  ```
  (Capital-C for visual; lowercase-c for runtime; matches architecture v7.0.11 §1.1's stated intent.)
- **Cross-update:** Edit `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md:51-53` for the same Cards/Cards collision in the architecture text. Same typography fix.
- **Phase 3 cross-ref:** P1-7.

### Patch A3 — README Wave-1/Wave-2 LOCK status comments

- **File:** `pipeline/cards/README.md`
- **Current state:** Lines 24-39 annotate 12 cards as "NEEDED — Phase D research" and 2 cards as "fixture stub at v7.0.11 LOCK." All 14 are now Wave 1 or Wave 2 LOCKed + signed per `registry.yaml` + the on-disk lifecycle blocks (Phase 1 §4 table).
- **Proposed change:** Replace per-card comments with `# signed at Wave N LOCK <UTC date>` annotations. Match the `signed_at` timestamps from each card's lifecycle block (Phase 1 §4 table provides the bucket).
- **Phase 3 cross-ref:** P2-6.

### Patch A4 — Card header-comment normalization (14 cards)

- **Files:** All 14 cards under `pipeline/cards/CIC/*.yaml` + `pipeline/cards/CLC/*.yaml`.
- **Current state:** At least 4 cards (food_systems, public_agency, cooperative, ecosystem_intermediary) carry header comments that read `# Lifecycle: draft. NO Ed25519 signature.` while their lifecycle blocks declare `draft_status: signed`. The other 10 cards' header comments are unaudited but likely similar.
- **Proposed change:** For each card, replace the stale lifecycle-draft assertion in the file header comment block with: `# Lifecycle: signed (Wave N LOCK <UTC date>; supersession-re-sign per OD-N row <row>). Ed25519 signature present in _research_metadata.ed25519_signature; content_hash present in lifecycle.content_hash.` The header comments are not in canonical-bytes (comments are stripped before YAML parse), so this is a documentation-only edit that does NOT invalidate `content_hash` and does NOT require re-signing.
- **Verification:** Re-grep `# Lifecycle: draft` across `pipeline/cards/` — expected zero hits post-patch.
- **Phase 3 cross-ref:** P1-4.

### Patch A5 — Architecture v7.0.11 §1.4 lifecycle enum reconciliation

- **File:** `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md`
- **Current state:** §1.4 (line 82) declares the 6-value enum `draft | reviewed | thesis_passed | signed | loaded | deprecated`. On-disk schema + models + loader unanimously use the 4-value enum `draft | review_passed | signed | deprecated`. (Phase 1 §3.1 + P0-2.)
- **Proposed change:** Replace §1.4 block with:
  ```yaml
  lifecycle:
    draft_status: draft | review_passed | signed | deprecated
    review_status: pending | passed | changes_requested
    cross_family_thesis_status: pending | passed | failed
    signature_status: unsigned | signed | revoked
    runtime_load_status: not_loaded | loaded | disabled
    runtime_loadable: false | true   # the binding boolean runtime-truth flag
  ```
  Add a paragraph explaining the consolidation: "reviewed" → `review_status: passed`; "thesis_passed" → `cross_family_thesis_status: passed`; "loaded" → `runtime_load_status: loaded`. Reference `pipeline/cards/_schema/card_cic.schema.json:391-398` and `pipeline/cards/loader.py:63-77` as the authoritative schema/runtime bytes.
- **Ceremony shape:** Documentation-only carve-out (OD-D row 270 precedent for documentation-only self-LOCK on a §18.x amendment). Operator decides whether to fire a real LOCK ceremony or apply the documentation-only carve-out.
- **Phase 3 cross-ref:** P0-2.

---

## §2. Batch B — The cards-ceremony (compound LOCK; §6.17 Option-B)

This is the largest single ceremony. It bundles three LOCKed-but-not-applied amendments plus operator-decision Law-5 relocations into one §6.17 Option-B compound LOCK at a single `lock_timestamp_utc`. Modeled on the OD-E 5-row compound at row 274 (per master prompt §2.5).

**Ceremony shape:** §6.17 Option-B compound paired-commit. Expected member count: ~12-14 rows (3 amendment rows + 1 marker row + 9 card-supersession rows + optional schema-pin row).

**Lock_timestamp_utc bucket:** `<NEXT-AVAILABLE-CARDS-CEREMONY-UTC>` — to be set by operator at ceremony fire time.

**Constraints frontmatter** (per `cic_clc_unified_batch_supervisor_prompt_2026-05-17.md` §3 / OD-* lane discipline):

- No new top-level failure-code rows from this dispatch.
- No edits to LOCKed amendment text (only schema + card + comment patches).
- No git operations from the dispatching session.
- Operator fires; this patch queue does not.

**Operator pre-work required before ceremony fires:** approximately 30-40 hours of content-judgment work (per §18 v1.2 amendment line 209 FI-9 REVISED estimate + §18.6 v2 multi-track restructure + Phase 4-CLC Law-5 confirmation pass).

### Patch B1 — `pipeline/cards/_schema/card_cic.schema.json` — apply §18 v1.2 dialect_routing_table delta

- **Current state:** Lines 208-274 carry the v1.1 shape with `funder_political_axis` enum `[conservative, centrist, progressive, soul_fire]`, required `[funder_political_axis, dialect]`, additionalProperties: true.
- **Proposed change:** Apply the "After" block from `section_18_v1_2_amendment.md:90-140` (with FI-5/FI-6 Cycle 1 fold-ins at lines 207-208 applied):
  - Drop `funder_political_axis` property entirely.
  - Add `clc` property with the 8-slug enum from `pipeline/types/identity_capital.py` `CapitalLogicCard` (per §18 v1.2 §1.4 amendment text).
  - Add `dialect` property (preserve from v1.1; description updated per amendment).
  - Add `register_description` property (free-form 1-256 chars; FI-6 renamed from `register`).
  - Add `example_program` optional property (free-form 1-256 chars).
  - `required: [clc, dialect, register_description]`.
  - `additionalProperties: false` (FI-5 — replaces ineffective `not: required[funder_political_axis]`).
  - Update the `description` block at line 210 to describe CLC-keyed routing instead of funder-political-axis routing.
- **Parent lock(s):** `section_18_v1_2_amendment.md` LOCK row (referenced in amendment frontmatter; verify via `pipeline/engineering/lock_history.v1.jsonl` greppable by `2026-05-16T14:00:00Z`).
- **Ceremony parent row:** `<NEXT-AVAILABLE-COMPOUND-PARENT>`.
- **Phase 2 cross-ref:** L2-F0; Phase 3 cross-ref: P0-1 item §18 v1.2.

### Patches B2-B7 — All 6 CIC cards' `dialect_routing_table:` blocks

- **Files:** `pipeline/cards/CIC/food_systems.yaml`, `educator.yaml`, `public_agency.yaml`, `arts_culture.yaml`, `cooperative.yaml`, `ecosystem_intermediary.yaml`.
- **Current state:** Each carries 4-5 `dialect_routing_table` items with `funder_political_axis: "<conservative|centrist|progressive|soul_fire>" + dialect: "<scribe sub-mode>" + example_funder: "<one funder>"`. Total: 31 funder_political_axis occurrences across the 6 cards (5+5+5+5+5+4 = 29 in cards + 2 in schema = 31 per Phase 2 §3.1 grep tally).
- **Proposed change (operator-driven; FI-9 REVISED):** For each card, operator reads each existing routing row's dialect content + example_funder + decides which CLC slug captures the funder cluster THAT row served. Re-key each row to:
  ```yaml
  - clc: "<one of the 8 CLC slugs>"
    dialect: "<preserved or refined Scribe sub-mode>"
    register_description: "<free-form description of expected reviewer register>"
    example_program: "<optional program-internal variation hint>"   # optional
  ```
  No reference to the retired `funder_political_axis` value may appear. No heuristic mapping table. Each card's row count may change (a card with 4 political-axis routings might collapse to 3 CLC-keyed routings or expand to 6).
- **Burden:** 3-5 hours per card × 6 cards = 18-30 hours operator work (per §18 v1.2 amendment line 209).
- **Required companion patches:**
  - `pipeline/seats/scribe/dialect.py` — re-wire dialect resolution to read from `clc` key instead of `funder_political_axis` (Phase 2 §3.1 references; module not directly audited but listed in `section_18_v1_2_amendment.md:59` as an evidence surface).
  - `pipeline/engineering/agents/references/dialect_codebook.yaml` — re-key the codebook from political axis to CLC slug (Phase 2 §3.1 references).
- **Re-sign discipline:** Each patched CIC card gets a new Ed25519 signature; `lifecycle.content_hash` updated to match new canonical bytes; new lock_history row appended with `parent_lock_row` pointing to the original Wave 2 LOCK row and `ceremony_parent_row` pointing to the cards-ceremony compound row.
- **Parent lock(s):** Each card's Wave 1 (food_systems) or Wave 2 LOCK row from `lock_history.v1.jsonl`.
- **Phase 2 cross-ref:** L2-F0, L2-F7; Phase 3 cross-ref: P0-1 item §18 v1.2.

### Patch B8 — `pipeline/cards/_schema/card_clc.schema.json` — apply §18.6 v2 dual-track schema delta

- **Current state:** Schema (audited at lines 1-415) is single-track shape — no top-level `track_a` / `track_b` properties, no `$defs.track_container`, no `oneOf` branch.
- **Proposed change:** Apply the §18.6 v2 dual-track schema delta per the amendment text at `pipeline/blueprint/v0.1/section_18_6_v2_dual_track_amendment.md` (full amendment text not audited in Run 1 — Phase 8.6 work). Expected shape: two new optional top-level properties (`track_a` + `track_b`); one new `$defs.track_container` referencing the same nested-item `not.anyOf` defense-in-depth as today's root; a top-level `oneOf` with two mutually-exclusive branches (single-track legacy / multi-track Option A) per master prompt §4.
- **Required engineering verification:** Read `section_18_6_v2_dual_track_amendment.md` in full (Phase 8.6 dispatch — full schema delta not in Run 1 scope) and apply the exact schema delta.
- **Parent lock(s):** §18.6 v2 amendment LOCK row 274 per master prompt §2.5.
- **Phase 2 cross-ref:** L2-F1; Phase 3 cross-ref: P0-1 item §18.6 v2.

### Patches B9-B11 — Three multi-track CLC card restructures

- **Files:** `pipeline/cards/CLC/market_access.yaml`, `pipeline/cards/CLC/credit_underwriting.yaml`, `pipeline/cards/CLC/sponsorship_corporate.yaml`.
- **Current state:** Single-track shape. No `track_a:` / `track_b:` / `_partition_provenance:` blocks (Phase 2 §3.2 grep zero hits).
- **Proposed change:** For each card, partition existing single-track content into `track_a:` + `track_b:` containers per the §18.6 v2 amendment's per-card prescription:
  - **CLC-05 market_access:** `track_a` = `sbir_phase_ii`; `track_b` = `sbir_phase_iii`. Per master prompt §2.5.
  - **CLC-06 credit_underwriting:** `track_a` = `debt` (full content); `track_b` = `grant` **MINIMAL-STUB** per operator directive (master prompt §6 / L-024 carve-out). Track B includes `_partition_provenance.domain_clarification` block carrying the operator's verbatim rationale.
  - **CLC-07 sponsorship_corporate:** `track_a` = `benefits_exchange`; `track_b` = `corp_foundation_grant`. Per master prompt §2.7.
- **Shared root metadata preservation:** `schema_version`, `card_axis`, `card_id`, `slug`, `display_name`, `funding_mechanism_summary`, `tilth_clc_id`, `lifecycle`, `_research_metadata` stay at root. Per-track content under `track_a.*` / `track_b.*`.
- **Burden:** ~4 hours per card × 3 cards = 12 hours operator work (estimate; actual will vary by partition complexity).
- **Re-sign discipline:** Each patched card gets new Ed25519 signature; `lifecycle.content_hash` updated; new supersession rows per OD-E precedent (master prompt §2.5 row 276 / §2.6 row 277 / §2.7 row 278 are the prior precedent rows).
- **Parent lock(s):** Each card's Wave 2 LOCK row + the §18.6 v2 LOCK row 274.
- **Phase 2 cross-ref:** L2-F1; Phase 3 cross-ref: P0-1 item §18.6 v2.

### Patches B12-B19 — CLC Law-5 `common_funders_observed` confirmation pass (8 cards)

- **Files:** All 8 CLC cards.
- **Current state (Phase 2 §6.4):** Grep across CLC cards for `common_funders_observed:` or `draft_funder_candidates_pending_operator_engagement_confirmation` returns zero matches. Either CLC cards omit the field, have populated subagent-speculative funder lists, or have operator-confirmed lists. Status unconfirmed per card.
- **Proposed change (per card):** Phase 4-CLC researcher (separate dispatch) reads each card's `common_funders_observed:` state. Three outcomes per card:
  - **A — Field absent or empty:** No action.
  - **B — Field populated with operator-engagement-confirmed funders only:** No action. Add a comment block citing the operator's engagement confirmation timestamp.
  - **C — Field populated with subagent-speculative or unconfirmed funders:** Apply the Phase E Option 2 cleanup pattern (mirroring the 6 CIC cards):
    1. Empty the top-level `common_funders_observed:` block.
    2. Insert a comment explaining the relocation.
    3. Insert `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` nested block; move the relocated funders there with the same item shape.
    4. Operator graduates any subset of these candidates to the top-level list as engagement confirms (per-card, post-ceremony).
- **Re-sign discipline:** Only cards undergoing a B-or-C transition need re-signing (B is comment-only; C is structural). Bundled in the cards-ceremony compound LOCK.
- **Schema patch (Patch B20 below):** Add the `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` block to both schemas as an optional schema-known field. Saves the operator a re-LOCK at every future Law-5 relocation.
- **Parent lock(s):** Each CLC card's Wave 2 LOCK row.
- **Phase 2 cross-ref:** L2-F5; Phase 3 cross-ref: P1-3.

### Patch B20 — Schema patch for Law-5 draft-candidates block

- **Files:** Both `pipeline/cards/_schema/card_cic.schema.json` + `pipeline/cards/_schema/card_clc.schema.json`.
- **Current state:** `_research_metadata` block in both schemas (CIC: lines 523-553; CLC: lines 373-378) currently has no `draft_funder_candidates_pending_operator_engagement_confirmation` property. The 6 CIC cards use the field but the schema doesn't know about it (passes via `_research_metadata.additionalProperties: true`).
- **Proposed change:** Add an optional `draft_funder_candidates_pending_operator_engagement_confirmation:` property to `_research_metadata` in both schemas. Item shape mirrors `common_funders_observed.items` (same nested `not.anyOf` defense-in-depth). Description: *"Subagent-populated funder candidates pending operator engagement confirmation. Operator graduates entries to top-level `common_funders_observed:` as engagement is confirmed. Per Law 5 + operator's v2.1 reconciliation patch (2026-05-17)."*
- **Also update:** `card_cic.schema.json` + `card_clc.schema.json` description block for `common_funders_observed:` to add: *"Operator-confirmed engagement only. Subagent-populated candidates pending engagement confirmation route to `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`."*
- **Phase 2 cross-ref:** L2-F5 / §6.5 Patch B; Phase 3 cross-ref: P1-3.

### Compound LOCK ceremony shape for Batch B (template)

| Member | Lock_class | File | Purpose |
|---|---|---|---|
| 1 | §18 amendment | `section_18_v1_2_amendment.md` (status flip from LOCKED_TEXT_PENDING_COMPANION to LOCKED_COMPANION_LANDED) | Mark §18 v1.2 fully landed |
| 2 | §18 amendment | `section_18_6_v2_dual_track_amendment.md` (same flip) | Mark §18.6 v2 fully landed |
| 3 | §0.5 paired-commit | `section_00_5_*_amendment.md` marker row | Compound parent row registration |
| 4 | schema | `card_cic.schema.json` | Patch B1 + Patch B20 (CIC half) |
| 5 | schema | `card_clc.schema.json` | Patch B8 + Patch B20 (CLC half) |
| 6-11 | card_cartridge_supersession | 6 CIC cards | Patches B2-B7 |
| 12-14 | card_cartridge_supersession | 3 multi-track CLC cards | Patches B9-B11 |
| 15-22 | card_cartridge_supersession (optional; only B-or-C transitions) | Up to 8 CLC cards | Patches B12-B19 (subset, per Phase 4-CLC findings) |
| (separate) | code | `pipeline/seats/scribe/dialect.py` + `pipeline/engineering/agents/references/dialect_codebook.yaml` | Companion code patches (Patches B2-B7 dependents) |

All compound members land at the same `lock_timestamp_utc`. Per `cic_clc_unified_batch_supervisor_prompt_2026-05-17.md:317-322` (§4 Paired-commit Option-B pattern).

**Pre-ceremony checklist:**

1. Operator completes the per-row content-judgment re-keying for 6 CIC cards (18-30 hours).
2. Operator completes the per-track content partition for 3 multi-track CLC cards (12 hours).
3. Operator completes the per-CLC Law-5 confirmation pass (8 cards; time variable).
4. Phase 4-CLC researcher dispatches return their handbacks (per Phase 4 plan — Run 2 work).
5. F-INDEX-STALE PRE-gate verifies §0.5 paired-commit at compound LOCK.

**No LOCK initiated from this audit dispatch.** Operator fires the cards-ceremony in a separate session.

---

## §3. Batch C — Gate-body graduation sprint (code patches; engineering sprint)

This batch graduates the F-CARDS-COUPLING-VIOLATION-EXTENSION gate body and refactors coupling-enforcement ownership clarity. Engineering work; no operator LOCK ceremony required for the code patches themselves (but the test surface + the gate-body update may want a `code` lock-history row depending on operator preference).

**Ceremony shape:** Engineering-only patches. Optional `code` row in lock_history per operator preference. Modeled on OD-C parent-handoff carve-out (`section_04_v2_x_7_*.md:5` declares LOCKED via self-LOCK without formal Thesis).

**Lock_timestamp_utc bucket:** `<NEXT-AVAILABLE-CODE-CEREMONY-UTC>`.

**Disclaimer:** No new LOCK ceremony initiated from this audit dispatch. Engineering lands patches in a normal PR flow. Operator decides whether to record a `code` lock-history row.

### Patch C1 — Graduate `f_cards_coupling_violation_extension.py` body

- **File:** `pipeline/logician/gates/f_cards_coupling_violation_extension.py`
- **Current state:** Lines 63-82 — `evaluate()` body raises `NotImplementedError`. FORBIDDEN_FIELD_REGISTRY constant at lines 32-53 IS live for AST-lint consumption.
- **Proposed change:** Implement body per §4 v2.x.7 amendment §2 pseudocode (`section_04_v2_x_7_*.md:74-156`). Three sibling scanners:
  - `_scan_field_names(card_body, axis)` — top-level + recursive nested-key scan against `FORBIDDEN_FIELD_REGISTRY[axis]`. Sub-tag `.forbidden_field_name_for_axis`. (NOTE: this already lives in `loader.py:309-344` as `enforce_no_forbidden_coupling`; refactor option below.)
  - `_scan_value_positions(card_body)` — recursive walk over all string values; match against the four `_VALUE_POSITION_PATTERNS` regex set; emit one violation per hit with dotted-path diagnostic. Honor `_VALUE_POSITION_EXEMPT_TOP_LEVEL_PREFIXES = ("_",)` and `_VALUE_POSITION_EXEMPT_PATHS = frozenset({("card_id",), ("tilth_cic_id",), ("tilth_clc_id",)})`.
  - `_scan_matrix_structural(card_body, v1_x_matrix_phase_active)` — fires only on `declared_axis == "MATRIX"` AND `v1_x_matrix_phase_active is False`. Sub-tags `.matrix_binding_eligibility_true` + `.matrix_status_not_forward_compat_only`.
- **Additional change (Phase 2 §4.2 / L2-F3):** Add a fifth pattern to the regex set: `("value_literal_customer_information_legacy_phrase", re.compile(r"[Cc]ustomer [Ii]nformation"))`. Tag as legacy-phrase defense.
- **Aggregator:** `evaluate()` combines all three scanners' outputs and returns a `GateOutcome` with `passed: bool` and `violations: tuple[str, ...]`.
- **Refactor option (Phase 3 cross-ref P1-5):** To resolve the loader-vs-gate ownership ambiguity, extract `_scan_field_names` into a shared helper imported by both `loader.py:enforce_no_forbidden_coupling` and the gate body. Single source of truth for the field-name check.
- **Tests:** Pre-stage 36 tests at `tests/logician/gates/test_f_cards_coupling_violation_extension.py` per §4 v2.x.7 amendment line 17-18: "stub→full 36-test surface; clean-card pass + 13-row field-name parametrize + 2× FIX-IN-PLACE pattern regression + 4× phrase parametrize + 4× underscore-exemption + recursion-walk + multi-violation + 3× matrix-card structural + 2× diagnostic-message shape contract."
- **Phase 1 cross-ref:** L1-F3; Phase 2 cross-ref: L2-F4, L2-F3; Phase 3 cross-ref: P1-1, P1-5.

### Patch C2 — Pre-stage `pipeline/scripts/od_c_backfill_scan.py`

- **File:** `pipeline/scripts/od_c_backfill_scan.py` (CREATE).
- **Current state:** Does not exist. The §4 v2.x.7 amendment line 238 cross-references `outputs/od_c_backfill_scan.py` (Cowork workspace outputs/), which is ephemeral relative to repo state.
- **Proposed change:** Author + commit the backfill-scan script at the canonical `pipeline/scripts/` path. Walks all cards under `pipeline/cards/CIC/` + `pipeline/cards/CLC/`, calls `f_cards_coupling_violation_extension.evaluate()` per card, emits a summary report. Post-graduation, this script should report 14/14 PASS (modulo the legacy "Customer Information" addition, which should also be 14/14 PASS since the legacy phrase is not in any card body today).
- **Workflow change (Phase 3 cross-ref CR-2):** Establish the convention that any operator-runnable script referenced from an amendment must live under `pipeline/scripts/`. Protects against Cowork-session-outputs ephemerality.

### Patch C3 — Refactor coupling-enforcement ownership

- **Files:** `pipeline/cards/loader.py` + `pipeline/logician/gates/f_cards_coupling_violation_extension.py`.
- **Current state:** `loader.py:309-344` (`enforce_no_forbidden_coupling`) and the new gate body (Patch C1) both run a top-level + recursive nested-key scan against `FORBIDDEN_FIELD_REGISTRY`. Code duplication risk.
- **Proposed change:** Extract the field-name scan into a shared helper (e.g., `pipeline/cards/_coupling_helpers.py`). Both the loader and the gate `_scan_field_names` import from this helper. Single source of truth.
- **Phase 3 cross-ref:** P1-5.

### Patch C4 — Reconcile the two-coupling-gate vocabulary

- **Files:** `pipeline/logician/gates/f_cic_clc_coupling_violation.py` + `pipeline/logician/gates/f_cards_coupling_violation_extension.py`.
- **Current state:** v7.0.8 progenitor uses `CouplingFinding.subcode` like `F-CIC-CLC-COUPLING-VIOLATION.layer1_lexical`. v7.0.11 successor uses `GateOutcome.violations` with `(sub-tag .name)` suffix. Two vocabularies.
- **Proposed change:** Author a new §4 v2.x amendment (per Phase 3 P1-6 / cross-ref) that pins the canonical `GateOutcome` + `sub-tag` vocabulary, maps the layer-suffix outputs into the sub-tag vocabulary, and either (a) deprecates the v7.0.8 progenitor's output shape in favor of the successor's, or (b) documents the two as deliberate parallel surfaces with scope boundaries. Operator + amendment author joint decision.
- **No code change in this patch** until the amendment lands.
- **Phase 3 cross-ref:** P1-6.

---

## §4. Batch D — v0.2 first-wave loader graduation sprint

This batch graduates `load_card()` past the `NotImplementedError` boundary and wires the four stubbed signature/lifecycle gates. Engineering sprint; multiple commits; operator decides ceremony shape.

**Ceremony shape:** Code-graduation per v7.0.11 §5 v0.2 first-wave scope. Multiple `code` rows in lock_history per operator preference. Modeled on the `pipeline/validation/v7_0_5_thesis_2026-05-09/` graduation pattern + the `pipeline/validation/section_18_v1_1_thesis_2026-05-15/` narrow-corrective precedent.

**Lock_timestamp_utc bucket:** `<V0_2_FIRST_WAVE_UTC>` — operator pins this.

**Disclaimer:** No new LOCK ceremony initiated from this audit dispatch. Engineering sprint plan.

### Patch D1 — Ed25519 signature verification at loader time

- **File:** `pipeline/cards/loader.py`
- **Current state:** `publisher_pubkey: Optional[bytes] = None` parameter at line 127 is unused. No `nacl.signing.VerifyKey.verify` invocation anywhere. Embedded `_research_metadata.ed25519_signature` (hex string per `models.py:94`) never decoded.
- **Proposed change:**
  - Make `publisher_pubkey: bytes` REQUIRED for `environment == "production"`. Add a precondition check at load_card entry.
  - Add `enforce_signature_validity(card_path, card_body, publisher_pubkey)` between Step 3 (lifecycle) and Step 5 (coupling) of the loader contract. Steps:
    - Read `lifecycle.signature_status` — fail `F-CARDS-UNSIGNED-PRODUCTION-LOAD` if not `signed` and environment is production.
    - Compute `canonical_bytes(card_body=card_body)` per existing function.
    - Decode `_research_metadata.ed25519_signature` from hex.
    - Call `nacl.signing.VerifyKey(publisher_pubkey).verify(canonical_bytes, decoded_sig)`.
    - Raise `CardLifecycleError(F-CARDS-SIGNATURE-INVALID, …)` on any failure.
  - Add `nacl` (PyNaCl) as a dependency if not already present.
  - Publisher pubkey load: read `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`, extract the pubkey bytes, pin against the boot-time-manifest-verified write-protected file per architecture v7.0.11 §1.10 (`architecture_v7_0_11_card_amendment.md:180-189`).
- **Phase 1 cross-ref:** L1-F4, L1-F6, §6.4; Phase 3 cross-ref: P1-2.

### Patch D2 — Graduate `f_cards_signature_invalid.py` body

- **File:** `pipeline/logician/gates/f_cards_signature_invalid.py`
- **Current state:** Lines 26-41 — `evaluate()` body raises `NotImplementedError`.
- **Proposed change:** Implement body. Pattern: delegate to a shared helper that both the loader (Patch D1) and the gate body call. The gate signature is per the module's existing parameters (line 26): `card_path: str, canonical_bytes: bytes, ed25519_signature_hex: str, publisher_pubkey: bytes`. Body decodes the hex signature and calls `nacl.signing.VerifyKey(publisher_pubkey).verify(canonical_bytes, decoded_sig)` inside a try/except; returns `GateOutcome(passed=False, ...)` on failure or `GateOutcome(passed=True, ...)` on pass.
- **Tests:** `tests/logician/gates/test_f_cards_signature_invalid.py` (CREATE) — test valid signature, invalid signature, wrong pubkey, malformed hex, empty signature.
- **Phase 1 cross-ref:** L1-F4; Phase 3 cross-ref: P1-2.

### Patch D3 — Graduate `f_cards_unsigned_production_load.py` body

- **File:** `pipeline/logician/gates/f_cards_unsigned_production_load.py`
- **Current state:** Lines 26-41 — `evaluate()` body raises `NotImplementedError`.
- **Proposed change:** Implement body. Trivial logic: if `environment == "production"` AND `signature_status != "signed"` → `GateOutcome(passed=False, ...)`. Else pass. Matches the architecture v7.0.11 §1.6 #2 spec exactly.
- **Tests:** `tests/logician/gates/test_f_cards_unsigned_production_load.py` (CREATE).
- **Phase 1 cross-ref:** L1-F4; Phase 3 cross-ref: P1-2.

### Patch D4 — Graduate remaining F-CARDS-* gate bodies

- **Files:** `pipeline/logician/gates/f_cards_coverage_incomplete.py`, `pipeline/logician/gates/f_cards_schema_invalid.py`, `pipeline/logician/gates/f_cards_private_data_in_card.py`, `pipeline/logician/gates/f_cards_cross_org_namespace_leak.py`, `pipeline/logician/gates/f_cards_load_in_wrong_namespace.py`.
- **Current state:** Not read in Run 1. Bodies presumed `NotImplementedError` stubs per architecture v7.0.11 §5 v0.2-first-wave deferral pattern.
- **Proposed change:** Audit each gate body's current state (full read; Phase 6 work). For stubs, implement per architecture v7.0.11 §1.6 specs:
  - F-CARDS-COVERAGE-INCOMPLETE (META PRE-cycle gate, WARN/FAIL bifurcation per §1.6 #1) — moderate complexity; requires per-seat depends-on-field declaration registered at loader Step 8.
  - F-CARDS-SCHEMA-INVALID (loader gate) — fails closed if card does not validate against `*_card.schema.json`. Pattern: invoke `jsonschema.validate(card_body, schema)` and translate errors to `GateOutcome.violations`.
  - F-CARDS-PRIVATE-DATA-IN-CARD (loader gate) — fails closed on private-org-data shapes. Pattern: structured field-name + value-position blocklist scan (org_slug, client_name, PROJECT_CONTEXT keys, EIN, UEI, address regex patterns).
  - F-CARDS-CROSS-ORG-NAMESPACE-LEAK (memory retrieval gate) — fails closed when retrieval call mixes `orgs:<slug>:*` + `cards:*` scopes opaquely. Pattern: namespace declaration check at call site.
  - F-CARDS-LOAD-IN-WRONG-NAMESPACE (loader gate) — fails closed if card_axis ≠ namespace axis. Trivial: invoke at loader Step 6 in `resolve_card_namespace`.
- **Phase 3 cross-ref:** CR-3 items 2, 5, 6, 7.

### Patch D5 — Loader graduation past `NotImplementedError` boundary

- **File:** `pipeline/cards/loader.py:163-167`.
- **Current state:** `load_card()` raises `NotImplementedError` after preflight passes.
- **Proposed change:** Implement steps 6-9 of the loader contract:
  - **Step 6:** `resolve_card_namespace` — already LIVE at lines 383-410.
  - **Step 7:** Build memory profile — concept graph nodes + edges per §18 §16. Requires architecture-level decisions on graph shape and storage. Engineering proposes implementation.
  - **Step 8:** Register runtime defaults with consuming seats — per-seat depends-on-field declaration registry. Requires Scout, Scribe, Judge, Logician, Archivist, Report Generator, Model Router APIs that consume `LoadedCard` content.
  - **Step 9:** Record load event in audit log — append to `pipeline/audit/cards_load.v1.jsonl` (or equivalent) with timestamp, card_path, declared_axis, environment, namespace, load result.
- **Return value:** Replace the `NotImplementedError` with `return LoadedCard(namespace=…, card=…, card_path=…, runtime_registered_seats=…, canonical_bytes_sha256=…)`.
- **Phase 1 cross-ref:** L1-F6; Phase 3 cross-ref: CR-3 item 1.

### Patch D6 — Activate `pipeline/cards/registry.yaml` runtime contract

- **File:** `pipeline/cards/registry.yaml`
- **Current state:** Lines 5-117 declare 14 active cards with `active: true` + `required_draft_status: signed` + `required_runtime_loadable: true`. The contract is aspirational at v0.1 (no consumer reads it). Per Phase 1 §6.1 + L1-F6.
- **Proposed change:** Wire up a `pipeline/cards/registry_loader.py` (CREATE) that, at deployment startup:
  - Reads `registry.yaml`.
  - For each `active: true` entry, invokes `load_card(path=…, environment=…, publisher_pubkey=…)`.
  - Aggregates `LoadedCard` results into a runtime cache.
  - Fails startup on any card that fails preflight.
- **Phase 1 cross-ref:** L1-F6.

---

## §5. Batch E — Deferred cleanup (P2 items)

Bundled patches for low-priority items. Operator schedules these at convenience. Each is a small documentation-only or schema-only patch.

**Ceremony shape:** Mix of documentation-only and small schema patches. Each can land independently. No compound ceremony required.

**Disclaimer:** No new LOCK ceremony initiated from this audit dispatch.

### Patch E1 — lock_history_row / lock_timestamp_utc / supersession_lock_history_row disposition

- **Files:** `pipeline/cards/_schema/card_cic.schema.json:458-466` + `pipeline/cards/_schema/card_clc.schema.json:308-316`.
- **Current state:** Three optional schema fields with no corresponding `models.py` declaration and no `loader.py` consumption (Phase 1 §3.4 / L1-F8).
- **Proposed change (operator decision):**
  - **Option A — Graduate:** Add the three fields to `models.py:Lifecycle`. Add to the canonical-bytes exclusion set in `loader.py:_without_signature_and_hash_fields`. Document the housekeeping-vs-identity semantics in a small §18 v1.x amendment.
  - **Option B — Remove:** Drop the three fields from the JSON schema. Lock-history pointers live only in `pipeline/engineering/lock_history.v1.jsonl`, never in the card body.
- **Recommendation:** Option B is cleaner; the lock_history.v1.jsonl is already the source of truth for lock-row data.

### Patch E2 — `coverage_axis` derivation or documentation

- **Files:** `pipeline/cards/_schema/card_cic.schema.json:57-67` + `pipeline/cards/models.py:47-54`.
- **Current state:** 1:1 redundancy between slug enum and coverage_axis enum (Phase 2 §4.3 / L2-F9).
- **Proposed change (operator decision):**
  - **Option A — Derive:** Drop `coverage_axis` field from schema. Loader infers from slug via a lookup table.
  - **Option B — Document:** Add a `description` on `coverage_axis` clarifying it's a 1:1 human-readability redundancy and operator must keep slug + coverage_axis in sync at any future schema expansion.

### Patch E3 — Deprecation procedure documentation

- **File:** `pipeline/cards/README.md` (add new section) OR new §18 v1.x amendment.
- **Current state:** Both schemas allow `draft_status: "deprecated"` + `signature_status: "revoked"` + `runtime_load_status: "disabled"` but no doc explains the transition sequence (Phase 1 §7 / L1-F9).
- **Proposed change:** Add a "Deprecating a card" section covering:
  - The required field-flip ordering: `runtime_loadable: false` FIRST, THEN `runtime_load_status: "disabled"`, THEN `draft_status: "deprecated"` (avoids tripping the `runtime_loadable=false AND runtime_load_status='loaded'` loader fail-close at `loader.py:302-306`).
  - The `signature_status` choice: keep `signed` for the historical artifact OR flip to `revoked` if the publisher key was rotated post-supersession.
  - `registry.yaml` update: remove the entry from `active_cards`, OR add a `deprecated_at` field and a `deprecated: true` flag (operator schema decision).
  - The supersession lock-history-row pattern: parent_lock_row → original LOCK row; ceremony_parent_row → deprecation ceremony parent.

### Patch E4 — Schema `additionalProperties: false` tightening at root

- **Files:** `pipeline/cards/_schema/card_cic.schema.json:594` + `pipeline/cards/_schema/card_clc.schema.json:415`.
- **Current state:** Both schemas declare `additionalProperties: true` at root (Phase 2 §5.2 / L2-F6).
- **Proposed change:** After a full survey of every legitimate field used across the 14 cards (including the underscore-prefixed `_research_metadata` + any other `_*` block), tighten to `additionalProperties: false`. Catches typo-renamed forbidden fields (`eligible_clc_subsett` etc.) and unknown-field drift. The `_research_metadata` block already declares `additionalProperties: true` internally, so blocks remain extensible inside it.

### Patch E5 — Create `pipeline/cards/validators.py` or remove README reference

- **Files:** `pipeline/cards/validators.py` (CREATE or DECIDE NOT TO).
- **Current state:** README line 21 references `validators.py` ("auxiliary self-validation checks") but file does not exist (Phase 3 P2-5).
- **Proposed change (operator decision):**
  - **Option A — Create:** Author the validators module with "Phase 4 card-research-time gates" per the README description. Scope: self-validation checks a researcher runs before LOCK ceremony (KGIE preflight equivalent for cards, schema validation, coupling sanity, lifecycle-state sanity).
  - **Option B — Remove reference:** Edit README line 21 to remove the validators.py mention.

---

## §6. Patch queue summary

| Batch | Count | Operator hours | Engineering effort | Ceremony? |
|---|---|---|---|---|
| A — Documentation-only | 5 patches | ~1-2 hours review | minimal | None |
| B — Cards-ceremony (compound LOCK) | 20 patches (1 + 6 + 1 + 3 + 8 + 1) | 30-40 hours pre-work | small (schema + cards) | YES — §6.17 Option-B compound LOCK |
| C — Gate-body graduation | 4 patches | ~2 hours review | 1-2 weeks sprint | Optional `code` rows |
| D — v0.2 first-wave loader graduation | 6 patches | ~4 hours review | 2-3 weeks sprint | Operator decides |
| E — Deferred cleanup | 5 patches | minor | small | None per patch |
| **Total** | **40 patches** | **~35-50 operator hours** | **~4-5 weeks engineering** | **One major ceremony (B)** |

---

## §7. Cross-references to amendment-of-record texts

For each amendment referenced in this patch queue, the file path:

| Amendment | File path | Where used |
|---|---|---|
| §18 v1.2 | `pipeline/blueprint/v0.1/section_18_v1_2_amendment.md` | Batch B (Patches B1, B2-B7) |
| §18.6 v2 | `pipeline/blueprint/v0.1/section_18_6_v2_dual_track_amendment.md` | Batch B (Patches B8, B9-B11) |
| §18.11 v1.1 | `pipeline/blueprint/v0.1/section_18_11_v1_1_fold_in_discipline_amendment.md` | (referenced but no patch in this queue; Phase 4 work) |
| §4 v2.x.7 | `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md` | Batch C (Patch C1, C2) |
| §4 v2.x apolitical_dialect | `pipeline/blueprint/v0.1/section_04_logician_v2_x_apolitical_dialect.md` | Companion to §18 v1.2; Batch B implicit |
| architecture v7.0.11 | `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md` | Batch A (Patch A2, A5); Batch D (Patch D1 §1.10 reference) |
| architecture v7.0.12 | `pipeline/architecture/v0.1/architecture_v7_0_12_apolitical_dialect_amendment.md` | Companion to §18 v1.2 |
| §0.5 paired-commits | `pipeline/blueprint/v0.1/section_00_5_*_amendment.md` (multiple) | Batch B compound member 3 |

---

## §8. What this patch queue does NOT cover

- **Per-card content quality** — Phases 4-CIC + 4-CLC.
- **Admin-risk register migration to v3.0** — Phase 5.
- **Test surface audit** — Phase 6.
- **Batch supervisor synthesis** — Phase 7.
- **Release readiness, customer trust documentation, full CTO synthesis** — Phase 8.6-8.

These are out of Run 1 scope per the operator's corrective.

---

## §9. Files cited

This patch queue inherits all file citations from Phase 1 + Phase 2 + Phase 3 (see those documents' §9/§8/§7 respectively). Net-new citation in this phase:

| File | Purpose |
|---|---|
| `pipeline/scripts/od_c_backfill_scan.py` | CREATE per Patch C2 |
| `pipeline/cards/_coupling_helpers.py` | CREATE per Patch C3 |
| `pipeline/cards/registry_loader.py` | CREATE per Patch D6 |
| `pipeline/audit/cards_load.v1.jsonl` | CREATE per Patch D5 (audit log destination) |
| `pipeline/cards/validators.py` | CREATE OR remove README reference per Patch E5 |
| `tests/logician/gates/test_f_cards_coupling_violation_extension.py` | CREATE per Patch C1 (36-test surface) |
| `tests/logician/gates/test_f_cards_signature_invalid.py` | CREATE per Patch D2 |
| `tests/logician/gates/test_f_cards_unsigned_production_load.py` | CREATE per Patch D3 |
| `pipeline/seats/scribe/dialect.py` | EDIT per Patch B2-B7 companion code |
| `pipeline/engineering/agents/references/dialect_codebook.yaml` | EDIT per Patch B2-B7 companion code |
| `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml` | READ per Patch D1 (publisher pubkey source) |

---

*End of Phase 8.1-5 deliverable. Phases 8.6-8 fire as separate dispatches.*
