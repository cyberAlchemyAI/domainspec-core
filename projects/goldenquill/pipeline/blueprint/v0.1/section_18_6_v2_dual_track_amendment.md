---
title: Blueprint §18.6 v2 — CLC schema dual-track structural separation (Option A — top-level track_a:/track_b: containers on multi-track cards)
filed: 2026-05-16
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-17T16:00:00Z — 5-row compound paired-commit at OD-E ceremony fired rows 274-278 (§18.6 v2 = 274; §0.5 v32 paired-commit = 275; 3 × card_cartridge_supersession at 276 market_access supersedes Wave 2 row 258 / 277 credit_underwriting supersedes Wave 2 row 259 / 278 sponsorship_corporate supersedes Wave 2 row 260). Self-LOCK per OD-E parent-handoff carve-out — operator authorized self-LOCK mirroring OD-D / OD-C precedent; L-005 strict two-cycle cross-family Thesis NOT dispatched per operator authorization (8/8 CLC schema validation + 7/7 invariant suite + 3/3 cards clean against OD-C value-position regex layered as Thesis-equivalent evidence). All 5 sigs VERIFIED against pinned cards-publisher pubkey 0b1a0bbf…6f375bd. Operator selected PATH (a) minimal-stub for CLC-06 Track B at this ceremony per operator-stated rationale on the credit-vs-grant axis asymmetry — domain rationale folded into §G of §0.5 v32 amendment + _partition_provenance.domain_clarification block of credit_underwriting.yaml before signing. Post-ceremony status-flip housekeeping supersession row 279 (2026-05-17T16:01:00Z) re-pins this file's LOCKED-status canonical bytes per OD-D row 269 supersession precedent (file's amendment_status text edit post-row-274 sign changes bytes; row 279 captures the new canonical bytes against the same pinned cards-publisher pubkey).
parent_lock: pipeline/blueprint/v0.1/section_18_card_system.md  (§18 v1 — paired with architecture v7.0.11 + §4 v2.x card-hardening + §0.5 v25)
parent_lock_chain:
  - pipeline/blueprint/v0.1/section_18_v1_1_amendment.md  (§18 v1.1 LOCKED 2026-05-16 — narrow-corrective + schema-item-shape-extension precedent + §0.5 v26)
  - pipeline/blueprint/v0.1/section_18_v1_2_amendment.md  (§18 v1.2 LOCKED 2026-05-16T14:00:00Z — narrow-corrective + schema-item-shape-extension precedent + §0.5 v28 + architecture v7.0.12 compound paired-commit)
companion_lock: pipeline/blueprint/v0.1/section_00_5_section_18_6_v2_amendment.md (PENDING DRAFT — §0.5 paired-commit registering ONE marker row anchoring this v2 amendment file; supersession-re-sign rows for CLC-05/06/07 land at LOCK ceremony itself, not at §0.5 v_).
companion_supersession_targets:
  - pipeline.cards.CLC.market_access (lock_history row 258 — Wave 2 LOCK ceremony 2026-05-16)
  - pipeline.cards.CLC.credit_underwriting (lock_history row 259)
  - pipeline.cards.CLC.sponsorship_corporate (lock_history row 260)
amendment_class: schema-shape-extension (Option A — top-level container; not item-shape-extension because we add new top-level properties, not new properties on existing array items)
precedent_pattern: §18 v1.1 + §18 v1.2 narrow-corrective + schema-item-shape-extension amendments (lock_history rows 565 + LOCKED-with-v7.0.12 2026-05-16T14:00:00Z) — both extend a LOCKed schema's contract surface without modifying the parent LOCKed text in-place. §18.6 v2 differs in that the extension is at TOP level (new optional properties `track_a` / `track_b` + new $defs.track_container + new top-level oneOf branch) rather than at item level inside an existing array property. Backward-compatible: all eight existing CLC cards continue to validate under the §18.6 v1 (single-track) oneOf branch after the schema delta lands — the validation outcome flips only when individual cards are restructured into the Option A shape.
threat_severity_at_v0_1_v0_2: LOW — schema-shape extension under v0.1 Beta single-operator deployment. The extension is GATED ON (a) card-by-card opt-in via restructure (no broadcast schema break) and (b) operator-Ed25519 LOCK ceremony supersession-re-sign of the three affected cards before runtime-loader fires. No new failure-code primitives, no new AST-lint rules, no new vocabulary kinds at §0.5. The schema oneOf enforcement is the only new enforcement surface, and it fails-closed against ambiguous mixed-shape cards (track_a present but root-level track-specific fields also present — neither oneOf branch matches → validation fails → Logician F-CARDS-SCHEMA-INVALID predicate fires on production load).
purpose: Resolve OD-E surfaced at WAVE_2_CLOSE_SYNTHESIS.md §CC-5 (2026-05-16). Three Wave 2 CLC cards surfaced "track A vs track B" structural questions that §18.6 v1 schema does NOT currently express: CLC-07 sponsorship_corporate (Track A benefits-exchange contractual vs Track B corp-foundation-as-grant charitable), CLC-06 credit_underwriting (debt-vs-grant framing; Scribe cannot draft grant-language proposals on debt instruments), CLC-05 market_access (SBIR Phase II further-SBIR-funds vs Phase III commercialization-without-SBIR-funds). Per operator schema-shape decision 2026-05-16 PM: Option A picked over B (per-criterion track:) and C (separate child CLC cards) because Option A is explicit enough that Scribe doesn't have to invent aggregation logic (B's weakness) and pays schema cost only on the three affected cards rather than permanently expanding namespace + matrix layer (C's weakness).

companion_code_landed_at_DRAFT:
  - "pipeline/cards/_schema/card_clc.schema.json — schema delta APPLIED 2026-05-16 (DRAFT). Top-level required[] flattened from 14 to 9 (the 6 core track-specific fields moved into oneOf branch 1's conditional required[]); new optional top-level properties `track_a` + `track_b` added with $ref to new $defs.track_container; new top-level oneOf with two mutually-exclusive branches (single-track legacy / multi-track Option A); new $defs.track_container with 8-field required[] (track_name + track_description + 6 core track-specific fields) + 14 optional track-specific properties + item-level not.anyOf defense-in-depth replicating root-level CIC-coupling discipline inside each track container per §18 v1.1 RT-02 fold-in precedent."
  - "pipeline/cards/CLC/sponsorship_corporate.yaml — restructured under track_a (benefits_exchange) + track_b (corp_foundation_grant) per Option A. Pre-existing Track A / Track B markers in field notes guided partition. Shared metadata (schema_version, card_axis, card_id, slug, display_name, funding_mechanism_summary, tilth_clc_id, lifecycle, _research_metadata, _review_handback) remain at root."
  - "pipeline/cards/CLC/credit_underwriting.yaml — restructured under track_a (debt) + track_b (grant) per Option A. Track partition derived from underwriting_criteria semantics (DSCR / collateral / repayment logic → debt; grant-style mission-fit / capacity / outcomes → grant)."
  - "pipeline/cards/CLC/market_access.yaml — restructured under track_a (sbir_phase_ii) + track_b (sbir_phase_iii) per Option A. Track partition derived from SBIR program structure (Phase II = further SBIR R&D funds; Phase III = commercialization without further SBIR funds; private capital + procurement vehicles)."

companion_tests_landed_at_DRAFT: NONE at this DRAFT — schema validation surface uses existing jsonschema Draft202012 surface; pre-existing `tests/cards/test_models_and_schemas.py::test_clc_schema_is_valid_json` contract preserved (root-level `not.anyOf` for forbidden CIC-coupling fields stays intact; slug enum unchanged). v0.2 first wave loader-level F-CARDS-SCHEMA-INVALID predicate body graduates with multi-track partition awareness as part of WS-J first wave.

done_definition:
  - "Schema delta applied to `pipeline/cards/_schema/card_clc.schema.json` — new optional top-level `track_a` + `track_b` properties; new $defs.track_container with required track_name + track_description + 6 core track-specific fields; new top-level oneOf with mutually-exclusive single-track / multi-track branches; root-level `not.anyOf` for forbidden CIC-coupling fields PRESERVED unchanged."
  - "Three multi-track CLC cards (CLC-05 market_access + CLC-06 credit_underwriting + CLC-07 sponsorship_corporate) restructured under Option A shape; shared metadata at root; track-specific content under track_a / track_b containers; pre-existing Track A / Track B markers in field notes used as partition source-of-truth where present; partition judgment surfaced for operator review at LOCK ceremony where ambiguous."
  - "Existing five single-track CLC cards (CLC-01 public_purpose_works + CLC-02 catalytic_change + CLC-03 operating_capacity + CLC-04 research_evidence + CLC-08 shared_assets) UNCHANGED; backward-compatibility verified via jsonschema validation pass under the §18.6 v2 schema."
  - "L-005 strict two-cycle cross-family Thesis (Editor + Judge + Red Team via openclaw bridge per AGENTS.md; no Anthropic-family reviewer) DISPATCHED — reserved for LOCK ceremony per pre-staging discipline; not fired at this DRAFT."
  - "Supersession-re-sign ceremony per OD-1 path (b) / vocab-scrub precedent (lock_history rows 238-249, 2026-05-16T14:30:00Z) PRE-STAGED — handoff at `pipeline/handoffs/od_e_paired_commit_lock_ceremony_2026-05-16.md` enumerates supersession-row count (3 = one per restructured CLC card), supersession ceremony parent_lock_row (this v2 amendment's LOCK row when fired), post-restructure SHA3-512 of each card's canonical bytes, and operator Ed25519 publisher signing slots."
  - "Compound LOCK at the same `lock_timestamp_utc` per §6.17 Option-B: §18.6 v2 + §0.5 v?? paired-commit + 3 × supersession-re-sign rows for CLC-05/06/07 + 1 × Wave 2 LOCK ceremony parent-row cross-reference (since the cards being superseded were LOCKed at Wave 2 ceremony rows 258/259/260 — supersession discipline preserves audit trail per §6.17)."

cowork_thesis_dispatch_status: PENDING at DRAFT — L-005 strict two-cycle Thesis reserved for LOCK ceremony. Cycle 1 + Cycle 2 modeled on `pipeline/validation/v7_0_12_thesis_2026-05-16/` + `pipeline/validation/section_18_v1_2_thesis_2026-05-16/` (precedent for narrow-corrective amendments). Editor = `groq/llama-3.3-70b-versatile`; Judge = `google/gemini-2.5-pro`; Red Team = `groq/openai/gpt-oss-120b`; cross-family rigor (no Anthropic-family reviewer) preserved per L-003.

ws_dispatch: OD-E (this session) — surfaced at WAVE_2_CLOSE_SYNTHESIS.md §CC-5 by Wave 2 Cards Thesis dispatch 2026-05-16; operator schema-shape decision Option A confirmed 2026-05-16 PM.

session_metrics: pipeline/metrics/session_log.jsonl

coordination_note: |
  Concurrent surfaces in flight at this DRAFT:
  - OD-A LOCK ceremony (admin_risk_register.yaml v2.3 workspace-wide migration)
  - §4 v2.x.6 runtime companion (Code session)
  - OD-C / OD-D / OD-I (other Wave 2 close-synthesis operator-decision items)
  - OD-G state-overlay amendment (CC-7) — coordinate IF OD-G targets §18.6 simultaneously
  
  OD-E stays in its lane: the three multi-track CLC cards and their schema. NO touch on:
  - admin_risk_register.yaml v2.3 (OD-A domain)
  - §4 v2.x.6 router dedup (Code domain)
  - cross-card state-overlay (OD-G domain)
  - other CIC / CLC cards beyond CLC-05/06/07
  - Wave 2 LOCK ceremony parent rows (already LOCKED at rows 250-262; supersession appends only)
  - lock_history rows (no new rows appended at this DRAFT; pre-staged paired-commit handoff carries the row spec)
---

# Amendment §18.6 v2 — CLC schema dual-track structural separation (Option A)

## §0. Amendment intent + scope

This schema-shape-extension amendment **refines** (does **not** replace) the §18.6 v1 schema surface with one operator-pinned resolution surfaced at WAVE_2_CLOSE_SYNTHESIS.md §CC-5 (filed 2026-05-16): three multi-mechanism CLC cards (CLC-05 market_access, CLC-06 credit_underwriting, CLC-07 sponsorship_corporate) carry two structurally-distinct funding tracks that §18.6 v1 schema cannot express without forcing Scribe to invent aggregation logic at draft time.

The amendment does NOT modify §18 v1 architectural decisions on the Card System; it does NOT modify §18 v1.1 prose-vs-schema reconciliations; it does NOT modify §18 v1.2 retirement of `funder_political_axis`; it does NOT add new failure-code primitives at this section; it does NOT add new AST-lint rules; it does NOT introduce new vocabulary kinds at §0.5.

The amendment lands three binding deliverables:

1. **Schema extension on CLC schema** — top-level optional `track_a` + `track_b` properties; new `$defs.track_container`; new top-level `oneOf` with mutually-exclusive single-track / multi-track branches. Backward-compatible: all eight existing CLC cards validate unchanged under the v1 (single-track) branch until they are individually restructured into Option A shape.
2. **Three multi-track card restructures** — CLC-05 + CLC-06 + CLC-07 restructured under `track_a` / `track_b` containers. Pre-existing Track A / Track B markers in field notes used as partition source-of-truth where present. Partition judgment surfaced for operator review at LOCK ceremony where ambiguous.
3. **Pre-staged paired-commit LOCK ceremony handoff** — supersession-re-sign of the three previously-LOCKed CLC cards (Wave 2 LOCK rows 258/259/260) per OD-1 path (b) / vocab-scrub-precedent (rows 238-249, 2026-05-16T14:30:00Z). Operator-Ed25519 ceremony NOT fired at this DRAFT.

The amendment composes against §18 v1 LOCK + §18 v1.1 LOCK + §18 v1.2 LOCK + architecture v7.0.11 + §4 v2.x card-hardening + §0.5 v25/v26/v28 chain + Wave 2 LOCK ceremony (rows 250-262, 2026-05-16).

## §1. Operator-pinned resolution — Option A (top-level container, schema-mass-doubles-on-multi-track-cards-only)

### §1.1 Ambiguity statement

§18.6 v1 schema treats each CLC card as a single-mechanism funding logic. Three of eight CLCs (05/06/07) carry two structurally-distinct mechanisms that cannot be collapsed without inviting Scribe-draft errors:

- **CLC-05 market_access** — SBIR Phase II is further SBIR R&D funds with NIH/NSF-style review; SBIR Phase III is commercialization without further SBIR funds, drawing on private capital + procurement vehicles. Underwriting logic differs; reviewer profiles differ; budget conventions differ; reporting cadences differ.
- **CLC-06 credit_underwriting** — debt instruments (CDFI loans, SBA 7(a)/504/Microloan, USDA B&I) underwrite on DSCR + collateral + repayment capacity. Grant-style capital (capitalization grants, loan loss reserve grants, USDA RD grant-loan combos) underwrite on mission-fit + capacity + outcomes. Scribe cannot draft grant-language proposals on debt instruments without producing structurally-incorrect submissions.
- **CLC-07 sponsorship_corporate** — Track A corporate sponsorship is transactional benefits-exchange (audience reach + activation + brand alignment + ROI); Track B corporate-foundation grants behave like foundation grants with CSR overlay (mission-fit + capacity + outcomes + budget). Many applicants treat sponsorship like a grant ("here's our mission, please give") and lose.

### §1.2 On-disk evidence

- Verified at `pipeline/cards/CLC/sponsorship_corporate.yaml` header comment (lines 18-28 of pre-restructure form): "STRUCTURAL NOTE — this CLC differs from grant-style CLCs: Sponsorship is a TRANSACTIONAL BRAND-RELATIONSHIP instrument (audience + benefits exchange), not a charitable transfer. The card encodes BOTH tracks: Track A — corporate sponsorship + cause marketing... Track B — corporate foundation grants..."
- Verified at `pipeline/validation/cards_wave_2_thesis_2026-05-15/WAVE_2_CLOSE_SYNTHESIS.md` §CC-5: "Multi-mechanism CLC cards surfaced 'track A vs track B' structural questions... These are not per-card fixes — they are §18.6 schema amendment candidates (top-level `track_a:` / `track_b:` containers OR per-criterion `track:` attribute)."
- Verified at `pipeline/handoffs/od_e_dual_track_structural_separation_2026-05-16.md` (the dispatch that prompts this amendment): "Three Wave 2 CLC cards surfaced 'track A vs track B' structural questions that §18.6 schema does NOT currently express."

### §1.3 Operator-pinned resolution

**Option A** chosen over B (per-criterion `track:` attribute) and C (separate child CLC cards) at operator decision 2026-05-16 PM. Rationale (operator-stated):

- Option A is **explicit enough that Scribe doesn't have to invent aggregation logic** — Scribe reads `track_a` or `track_b` directly per opportunity; no merge logic at draft time. This is Option B's structural weakness: per-criterion `track:` attributes scatter the partition across every entry, forcing each Scribe call to walk and aggregate.
- Option A **pays schema cost only on the three affected cards** rather than permanently expanding namespace (8 → 11 CLCs under Option C) and the matrix-card layer (8 × 6 → 11 × 6 intersection cells, doubling some). This is Option C's structural weakness: namespace explosion bleeds through every downstream consumer.
- Option A **reversibility is moderate**: a track that proves to merit a full child card later can graduate by appending a new CLC slug at the schema's `slug` enum + the namespace + matrix layer (Option C migration path open), without forcing a §18.6 v3 amendment.

### §1.4 Schema delta — `pipeline/cards/_schema/card_clc.schema.json`

**Before** (v1 — superseded at v2 LOCK):

```json
{
  "required": [
    "schema_version", "card_axis", "card_id", "slug", "display_name",
    "funding_mechanism_summary", "tilth_clc_id",
    "underwriting_criteria", "evidence_weights", "reviewer_profile_typical",
    "common_red_flags", "reporting_requirements_typical", "commitment_tracking_pattern",
    "lifecycle", "_research_metadata"
  ],
  "properties": { ... },
  "not": { "anyOf": [ { "required": ["eligible_cic_subset"] }, ... ] },
  "additionalProperties": true
}
```

**After** (v2 LOCK):

```json
{
  "required": [
    "schema_version", "card_axis", "card_id", "slug", "display_name",
    "funding_mechanism_summary", "tilth_clc_id",
    "lifecycle", "_research_metadata"
  ],
  "properties": {
    ...,
    "track_a": { "description": "...", "$ref": "#/$defs/track_container" },
    "track_b": { "description": "...", "$ref": "#/$defs/track_container" }
  },
  "oneOf": [
    {
      "title": "Single-track shape (legacy, §18.6 v1)",
      "required": [
        "underwriting_criteria", "evidence_weights", "reviewer_profile_typical",
        "common_red_flags", "reporting_requirements_typical", "commitment_tracking_pattern"
      ],
      "not": {
        "anyOf": [
          { "required": ["track_a"] },
          { "required": ["track_b"] }
        ]
      }
    },
    {
      "title": "Multi-track shape (§18.6 v2 Option A — dual-track structural separation)",
      "required": ["track_a", "track_b"],
      "not": {
        "anyOf": [
          { "required": ["underwriting_criteria"] },
          { "required": ["scoring_weight_patterns"] },
          ... // all 14 track-specific fields forbidden at root in multi-track mode
        ]
      }
    }
  ],
  "not": { "anyOf": [ { "required": ["eligible_cic_subset"] }, ... ] },
  "additionalProperties": true,
  "$defs": {
    "track_container": {
      "type": "object",
      "required": [
        "track_name", "track_description",
        "underwriting_criteria", "evidence_weights", "reviewer_profile_typical",
        "common_red_flags", "reporting_requirements_typical", "commitment_tracking_pattern"
      ],
      "properties": {
        "track_name": { "type": "string", "minLength": 1, "description": "Short canonical name for the track (snake_case)." },
        "track_description": { "type": "string", "minLength": 1, "description": "One-paragraph prose description of the track's funding-mechanism semantics + why it is structurally distinct from the sibling track." },
        ... // all 14 track-specific properties optional, plus item-level not.anyOf inside common_funders_observed + provenance_requirements
      },
      "additionalProperties": true,
      "not": { "anyOf": [ { "required": ["eligible_cic_subset"] }, ... ] }
    }
  }
}
```

**Backward-compatibility verification:** All eight existing CLC cards validate unchanged under the §18.6 v2 schema (single-track branch matches). Schema self-validation passes. Existing `tests/cards/test_models_and_schemas.py::test_clc_schema_is_valid_json` contract preserved (root-level `not.anyOf` for forbidden CIC-coupling fields stays intact; slug enum unchanged). Verified 2026-05-16 against `python3 -c "import json; jsonschema.Draft202012Validator.check_schema(...)"` + per-card YAML validation pass.

### §1.5 Rationale — why Option A and not B or C

**Option B (per-criterion `track:` attribute)** would scatter the partition across every entry in `underwriting_criteria` / `scoring_weight_patterns` / `evidence_weights` / etc. Pros: granular; allows shared-across-tracks entries to coexist with track-specific entries in a single list. Cons: opaque without aggregation logic at Scribe — every Scribe call must walk the entries and filter by track per opportunity. Scribe-implementation burden HIGH. Schema-loader burden MEDIUM. Operator-review burden MEDIUM (have to scan attributes to see partition rather than read off a section header).

**Option C (separate child CLC cards e.g. CLC-07a + CLC-07b)** would create three new CLC slugs (CLC-05a/b, CLC-06a/b, CLC-07a/b), expanding the namespace from 8 to 11. Pros: clean — each card is single-mechanism; existing v1 schema requires no change. Cons: matrix-card layer (CIC × CLC) doubles for affected CLCs (6 CICs × 11 CLCs = 66 intersection cells instead of 6 × 8 = 48; net +18). Slug enum at `pipeline/types/identity_capital.py` `CapitalLogicCard` + `pipeline/cards/_schema/card_clc.schema.json` enum + downstream consumers (Scout classification, Scribe routing tables, Judge rubric library, Logician compliance gates) all expand. **Hardcoding a "two-tracks-per-mechanism" pattern into the namespace permanently couples a runtime partition to design-time enum surface — high-blast-radius change for a problem that affects 3 of 8 cards.**

**Option A** keeps the slug enum unchanged (8 CLCs, namespace stable), keeps the matrix layer unchanged (48 intersection cells), and pays schema cost only on the three multi-track cards. Scribe routes by reading `track_a` / `track_b` directly per opportunity (operator-decision at SP0 or Scribe-classification at draft time). Schema-mass-doubles is localized to the three affected cards. Reversibility moderate — a track that proves to merit a full child card can graduate to Option C later without §18.6 v3 amendment.

### §1.6 Operator-decision boundaries reaffirmed

- **No CIC × CLC coupling** introduced at any layer. The `$defs.track_container` carries the same item-level `not.anyOf` defense-in-depth as the root-level discipline. F-CARDS-COUPLING-VIOLATION-EXTENSION continues to enforce.
- **No new failure-code primitives** at §4 v2.x. The pre-existing F-CARDS-SCHEMA-INVALID predicate fires on validation failures (including the new oneOf branch failures — track_a present without track_b, root-level track-specific fields present in multi-track mode, etc.).
- **No new AST-lint rules.** Existing R-CARDS-NO-COUPLING-FIELD continues to scan `pipeline/cards/CIC/**/*.yaml` + `pipeline/cards/CLC/**/*.yaml` unchanged.
- **No new vocabulary kinds at §0.5.** The §0.5 paired-commit registers ONE marker row anchoring this v2 amendment file; no new schema rows (the v2 extension lands under the existing §0.5 v25 `pipeline.cards._schema.card_clc` schema row); no new failure-code rows; no new vocabulary kinds.
- **No matrix-card touch.** §18.7 schema unchanged. Matrix layer at `pipeline/cards/matrix/_FORWARD_COMPAT_ONLY.md` continues to be the only matrix surface at v0.1.

## §2. Card restructure — three multi-track CLCs

### §2.1 CLC-07 sponsorship_corporate — Track A benefits-exchange / Track B corp-foundation-grant

- **track_a** (track_name: `benefits_exchange`): corporate sponsorship + cause marketing + employee giving. Underwriting: audience_fit / brand_alignment / visibility_value / activation_plan / sponsor_benefits / measurable_reach / reputational_safety / relationship_pathway / renewal_potential / community_goodwill. Reviewer profile: CMO / CSR Director / Community Relations / Brand Manager. Decision-maker-driven, rarely scored against a published rubric. Sponsorship deck is the primary application artifact; corporate sponsorship rarely uses forms.
- **track_b** (track_name: `corp_foundation_grant`): corporate-foundation grants. Underwriting: corporate_foundation_mission_fit / corporate_foundation_outcomes_and_capacity. Reviewer profile: corporate foundation program officer + parent-company brand review. Behaves like foundation grants with CSR overlay (mission-fit + capacity + outcomes + budget + parent-company brand-alignment screen). Portals: Foundant + Cybergrants typical. Rubric: foundation-style structured scoring with parent-company brand review layered on.

### §2.2 CLC-06 credit_underwriting — Track A debt / Track B grant

- **track_a** (track_name: `debt`): CDFI loans + SBA 7(a)/504/Microloan + USDA B&I + USDA Community Facilities + Intermediary Relending + revolving loan funds. Underwriting: repayment_capacity / cash_flow / debt_service_coverage (DSCR ≥1.20-1.25x typical) / collateral / credit_history / owner_equity / management_capacity / financial_controls / use_of_funds / risk_mitigation / guarantor_strength / covenant_compliance. Reviewer profile: lenders / credit analysts / loan committees / CDFI underwriters / SBA lenders.
- **track_b** (track_name: `grant`): grant-style capital that behaves like credit-readiness funding — capitalization grants + loan loss reserve grants + USDA RD grant-loan combos + CDFI-fund-administered capacity grants. Underwriting: mission-fit + capacity + outcomes + budget reasonableness + financial-systems-readiness (sub-set of debt-track financial_controls criterion). Reviewer profile: foundation program officers / CDFI Fund staff / USDA RD program officers. Scribe MUST NOT draft grant-language proposals on Track A (debt) opportunities — that's the structural error Option A prevents.

### §2.3 CLC-05 market_access — Track A SBIR Phase II / Track B SBIR Phase III

- **track_a** (track_name: `sbir_phase_ii`): further SBIR R&D funds. Underwriting: research-development-extension criteria from SBIR Phase I demonstration; technical feasibility extended to commercialization-readiness; team capability; intellectual merit + broader impacts (NIH/NSF/DOD/DOE/USDA variations). Reviewer profile: SBIR program managers + peer reviewers (technical SMEs).
- **track_b** (track_name: `sbir_phase_iii`): commercialization without further SBIR funds. Underwriting: market_access criteria from §18.6 v1 — buyer commitments / channel strategy / revenue model / competitive position / delivery capacity / unit economics. Funding source: private capital + procurement vehicles (sole-source contracts available to SBIR Phase II awardees under the SBIR Phase III authority). Reviewer profile: commercial procurement officers / private investors / strategic partners.

### §2.4 Shared root-level metadata across all three cards

The following fields remain at root for all three restructured multi-track cards:

- `schema_version` / `card_axis` / `card_id` / `slug` / `display_name` / `funding_mechanism_summary` / `tilth_clc_id` (card identity)
- `lifecycle` / `_research_metadata` (governance + provenance)
- `_review_handback` / `_schema_status` / `_oq6_anchor` (where present — review/audit metadata, allowed by `additionalProperties: true`)

`funding_mechanism_summary` reads as a single-sentence summary spanning both tracks; per-track summaries live inside `track_a.track_description` + `track_b.track_description`.

## §3. Done-definition + LOCK ceremony pre-staging

Per `companion_supersession_targets` in front-matter: three CLC card LOCK rows (258/259/260, Wave 2 ceremony 2026-05-16) require supersession-re-sign per OD-1 path (b) / vocab-scrub-precedent (rows 238-249, 2026-05-16T14:30:00Z). Pre-staged paired-commit handoff at `pipeline/handoffs/od_e_paired_commit_lock_ceremony_2026-05-16.md` enumerates:

1. **L-005 strict two-cycle cross-family Thesis** — Editor (`groq/llama-3.3-70b-versatile`) + Judge (`google/gemini-2.5-pro`) + Red Team (`groq/openai/gpt-oss-120b`) via osascript → openclaw bridge per AGENTS.md. Audit trail at `pipeline/validation/section_18_6_v2_thesis_<date>/`.
2. **Operator-Ed25519 supersession-re-sign ceremony** — three supersession rows (one per restructured CLC card) appended to `pipeline/engineering/lock_history.v1.jsonl` per the row-239+ pattern (parent_lock_row → Wave 2 ceremony rows 258/259/260; ceremony_parent_row → this v2 amendment's LOCK row).
3. **§0.5 paired-commit amendment** — `pipeline/blueprint/v0.1/section_00_5_section_18_6_v2_amendment.md` registering ONE marker row anchoring this v2 amendment file. No new schema rows. No new failure-code rows. No new vocabulary kinds.
4. **Compound LOCK at the same `lock_timestamp_utc`** per §6.17 Option-B: §18.6 v2 + §0.5 v?? paired-commit + 3 × supersession-re-sign rows.

LOCK ceremony NOT fired at this DRAFT — pre-staging discipline preserved per dispatch constraint "Do not initiate new LOCK ceremonies; if your work needs LOCKing, pre-stage a paired-commit handoff and surface to operator for ceremony."
