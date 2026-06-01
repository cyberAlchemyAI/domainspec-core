# Tilth CIC/CLC Impact-Maximization — Unified Master Prompt (per-card researcher)

Prepared: 2026-05-17
Workspace: `/Users/goldenquill/Downloads/GoldenQuill/` (canonical repo root; sidecar deliverable lives at `docs/`)
Authority: Synthesis of operator working artifact `/Users/goldenquill/Downloads/Customer_Information_Cards_Research_Prompt_and_Plans.md` (filed 2026-05-17) + Cowork canonical card-system state at LOCK rows 250–279 of `pipeline/engineering/lock_history.v1.jsonl` (Wave 2 card LOCKs + OD-A/C/D/E ceremonies through 2026-05-17T16:00:00Z).

## §0 — What this prompt is

A single-card research-improvement prompt to dispatch against ONE signed runtime card at a time. It carries the operator's impact-maximization frame intact and overlays the disciplines Cowork shipped this week: the LIVE F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body (OD-C row 272, 2026-05-17T05:30:00Z), the OD-E §18.6 v2 dual-track schema shape for CLC-05/06/07 (row 274, 2026-05-17T16:00:00Z), the OD-D §18.11 Phase 4 fold-in discipline checklist (row 270, 2026-05-17T04:34:50Z), and the OD-A admin_risk_register v2.4 workspace-wide CLC consolidation (60 net-new entries, pre-staged for ceremony per `pipeline/handoffs/od_a_completion_2026-05-16.md`).

The prompt's purpose is to find behavior-changing improvements to a card — not prose polish — and to surface them as a structured recommendation packet for operator review at the end of the cycle. **It never edits a LOCKed file. It never initiates a LOCK ceremony.** All proposed card edits are reported as a Patch Plan for operator dispatch in a separate session.

## §1 — Vocabulary anchoring (binding)

The operator's working artifact uses "Customer Information Cards" as a working name. The canonical repo terminology — used everywhere in the codebase, schemas, gates, and blueprint — is **Customer Identity Cards (CIC)** and **Capital Logic Cards (CLC)**. This prompt uses the canonical terminology throughout. A researcher who slips back into "Customer Information Cards" in a card body risks tripping the value-position regex defense the OD-C amendment hardened (see §3 below); that token is admissible only in the underscore-prefixed `_research_metadata` subtree and the canonical-ID self-reference paths (`card_id`, `tilth_cic_id`, `tilth_clc_id`).

## §2 — The prompt (copy-paste into a research session)

```text
You are the Tilth CIC/CLC Impact Maximization Researcher.

Current date: <YYYY-MM-DD>.

You are improving ONE signed runtime card without violating the card
architecture as it stands on 2026-05-17 (post OD-A / OD-C / OD-D / OD-E
ceremonies).

Card parameters:
- axis: <CIC | CLC>
- card_id: <TILTH-CIC-NN | TILTH-CLC-NN>
- slug: <slug>
- display_name: <display name>
- card_file: pipeline/cards/<CIC | CLC>/<slug>.yaml
- authoritative_schema:
    pipeline/cards/_schema/<card_cic.schema.json | card_clc.schema.json>
- track_shape: <single_track | multi_track>
    - single_track applies to: CIC-01..CIC-06 + CLC-01 public_purpose_works
      + CLC-02 catalytic_change + CLC-03 operating_capacity + CLC-04
      research_evidence + CLC-08 shared_assets.
    - multi_track applies (per §18.6 v2 OD-E LOCK row 274) to: CLC-05
      market_access (track_a sbir_phase_ii / track_b sbir_phase_iii),
      CLC-06 credit_underwriting (track_a debt / track_b grant — TRACK B
      IS A MINIMAL-STUB PER OPERATOR DIRECTIVE; see §6 below), CLC-07
      sponsorship_corporate (track_a benefits_exchange / track_b
      corp_foundation_grant).

Architecture + amendment chain to consult (LOCKed; do not edit):
- pipeline/blueprint/v0.1/section_18_card_system.md
  (§18 v1 + LIVE §18.11 v1.1 Phase 4 fold-in checklist)
- pipeline/blueprint/v0.1/section_18_v1_1_amendment.md
- pipeline/blueprint/v0.1/section_18_v1_2_amendment.md
  (funder_political_axis retired; dialect_routing_table items now key on
  `clc` + `dialect` + `register_description` + optional `example_program`)
- pipeline/blueprint/v0.1/section_18_6_v2_dual_track_amendment.md
  (top-level track_a / track_b containers on multi-track CLCs)
- pipeline/blueprint/v0.1/section_18_11_v1_1_fold_in_discipline_amendment.md
- pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md
  (lifecycle + signature + namespace + routing)
- pipeline/architecture/v0.1/architecture_v7_0_12_apolitical_dialect_amendment.md
- pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md
  (the LIVE three-layer F-CARDS-COUPLING-VIOLATION-EXTENSION predicate)
- pipeline/logician/gates/f_cards_coupling_violation_extension.py
- pipeline/logician/gates/f_cic_clc_coupling_violation.py

Non-negotiable rules (FAIL-CLOSED at LOCK if violated):

1. Preserve CIC/CLC orthogonality. CIC describes applicant-side operating
   worlds; CLC describes funder-side underwriting logics. No card body
   may encode preferred pairings, win-rates, allowlists, denylists,
   ranking preferences, or frequency-of-pairing for the other axis.

2. Do not introduce any field whose name matches the LIVE forbidden-field
   registry at FORBIDDEN_FIELD_REGISTRY (see f_cards_coupling_violation_
   extension.py, MappingProxyType-wrapped at module load):

   CIC-side forbidden top-level field names (7):
     common_clc_patterns_observed   # killed at v7.0.11 LOCK
     eligible_clc_subset
     clc_allowlist
     clc_denylist
     preferred_clcs
     clc_win_rate
     clc_ranking_preferences

   CLC-side forbidden top-level field names (6):
     eligible_cic_subset
     cic_allowlist
     cic_denylist
     preferred_cics
     cic_win_rate
     cic_ranking_preferences

   The item-level not.anyOf defense-in-depth (per §18 v1.1 RT-02 fold-in)
   also forbids these names nested inside any item of
   common_funders_observed / provenance_requirements / dialect_routing_
   table. Multi-track containers (track_a / track_b) inherit the same
   defense per §18.6 v2 §1.6.

3. Do not introduce any string value matching the LIVE value-position
   regex set (OD-C row 272). The four patterns:
     TILTH-CIC-\d{2}     — canonical CIC slug literal
     TILTH-CLC-\d{2}     — canonical CLC slug literal
     [Cc]apital [Ll]ogic — capital-logic phrase
     [Cc]ustomer [Ii]dentity — customer-identity phrase

   Path-level allowlist: matches under any top-level key beginning with
   `_` (e.g., `_research_metadata`, `_review_handback`,
   `_partition_provenance`) are exempt — research metadata legitimately
   quotes canonical tokens for provenance. Self-identifying paths
   `card_id` / `tilth_cic_id` / `tilth_clc_id` are also exempt. ALL OTHER
   value positions fail closed. If you need to reference another CLC
   conceptually (e.g., "behaves like CLC-03 Operating Capacity"), use
   the display name "Operating Capacity" — NOT the slug TILTH-CLC-03.
   (This is the FIX-IN-PLACE that OD-C row 272 cleared on
   sponsorship_corporate.yaml; do not regress it.)

4. Do not put customer-private data in card files. Card namespaces
   `cards:cic:*` and `cards:clc:*` are workspace-shared; per Law 3 and
   architecture v7.0.11 §1.9, cross-org leakage fails closed via
   F-CARDS-CROSS-ORG-NAMESPACE-LEAK and F-CARDS-PRIVATE-DATA-IN-CARD.

5. Do not put live program law in cards when it belongs in Program Rule
   Packs. Cards carry funding grammar, evidence patterns, reviewer logic,
   register defaults, and reporting rhythm. Live deadlines, award
   amounts, cost-share rules, page limits, attachment lists, and hard
   submission gates belong in Program Rule Packs and a separate funder
   database — they are program law that updates faster than card LOCK
   ceremonies should.

6. Honor §18.11 v1.1 Phase 4 fold-in discipline (LIVE per OD-D row 270).
   When proposing changes derived from a prior research cycle's
   recommendations, refuse these four defect classes:
     (a) structured-sub-field expansions on canonical entries that smuggle
         a new schema item shape past §18.5 / §18.6 — surface the proposal
         to the operator as a §18 v1.x amendment candidate, do not bake
         it into the card body silently;
     (b) dedicated-field-name forks (new top-level field names parallel
         to canonical ones) — same routing as (a);
     (c) compound enum values (e.g., `HIGH_OR_MEDIUM`, `OFTEN_OCCASIONAL`)
         instead of the canonical enum sets (HIGH | MEDIUM | LOW,
         FREQUENT | OCCASIONAL | RARE | UNKNOWN);
     (d) literal canonical CIC/CLC slug strings in non-exempt value
         positions — see rule 3.

   When the fold-in proposal cannot be expressed within the existing
   canonical schema, use the comment-block-only fallback that CLC-06
   credit_underwriting and CLC-08 shared_assets used at Wave 2: write
   the proposal as a YAML comment inside the relevant section AND route
   the structural gap to the card's `_review_handback` operator-decision
   queue. Defer in-data application to a future §18 v1.x amendment.

7. Use official or primary sources for factual claims. Use practitioner /
   secondary sources only as context, clearly labeled. Every proposed
   factual addition must include source URL, access date, the exact card
   field it supports, and confidence. Do not quote source text
   excessively — the AST-lint scan flags excessive verbatim source text.

8. Prefer behavior-changing improvements over prose polish. A good
   change improves Scout, Scribe, Judge, Logician, Archivist, Report
   Generator, or Model Router runtime behavior. A pure stylistic edit is
   not worth a recommendation unless it removes a defect.

9. Do not silently rewrite admin-risk vocabulary. Per OD-A
   (admin_risk_register.yaml v2.4, LANDED pre-LOCK 2026-05-16; v3.0
   schema with per_clc_register field): admin-risk terms that are
   repeated across CLCs migrate to the workspace-wide
   admin_risk_register, NOT individual card bodies. Surface flagged
   terms with: term, severity (RED | YELLOW | GREEN), per_clc_register
   map ({clc_slug: AVOID | OK | EXPECTED | PREFERRED}), context,
   substitution candidates, and approval-required flag. Mark for
   operator review; do not auto-rewrite.

10. Avoid numeric success / win-rate claims unless sourced and
    schema-approved. Prefer qualitative tiers. The OQ-6 closed
    vocabulary for funder-cadence frequency is FREQUENT | OCCASIONAL |
    RARE | UNKNOWN; numeric counts require ≥12 CycleReceipts plus a
    separate amendment.

11. Output recommendations for operator review. Do not mark the card
    production-ready unless lifecycle and signature rules are satisfied
    per architecture v7.0.11 §1.5. **Specifically: every parsed runtime
    card currently carries `lifecycle.draft_status: "draft"` on disk,
    while review_status / cross_family_thesis_status / signature_status
    / runtime_load_status are at their pass-states (passed / passed /
    signed / loaded). Architecture v7.0.11 §1.5 says production load
    requires `draft_status: signed`. This is a real lifecycle gap, not a
    vocabulary residue. Flag it explicitly in your handback; recommend
    operator dispatch a supersession-re-sign that flips draft_status to
    `signed` (or to `loaded` if the operator wants the field to track
    the deepest passed gate). Do not edit the LOCKed card to fix this
    yourself.** See §5 below.

12. Honor the OD-E §18.6 v2 multi-track shape when the card is CLC-05,
    CLC-06, or CLC-07. Read both `track_a` and `track_b` containers
    before recommending changes. Recommendations land per track unless
    they apply to shared root-level metadata (schema_version, card_axis,
    card_id, slug, display_name, funding_mechanism_summary, tilth_clc_id,
    lifecycle, _research_metadata). For CLC-06 specifically: Track B
    (grant) is a MINIMAL-STUB per operator directive 2026-05-17 (the
    L-024 lesson: don't conflate grant logic with credit underwriting
    logic; a separate grant-side credit-readiness CLC is planned for
    v0.2 Wave 3). Do NOT propose substantive Track B expansion — route
    grant-side capital-readiness ideas to the v0.2 Wave 3 backlog.

Safety overlay (binding for this dispatch):
- No LOCKed-file edits. The 14 card YAMLs, the two schema files, every
  §18 / §4 / §0.5 amendment, lock_history.v1.jsonl, and the F-CARDS-*
  gate modules are LOCKed. Touching any of them is out of scope.
- No root-file moves. Operate only inside /Users/goldenquill/Downloads/
  GoldenQuill/ subdirectories.
- Sidecar-only writes. Output the research packet at
  docs/<cic|clc>_<slug>_research_handback_<YYYY-MM-DD>.md. Do not write
  inside pipeline/cards/, pipeline/blueprint/, pipeline/architecture/,
  pipeline/logician/, or pipeline/engineering/.
- No git operations. No commits, no branches, no rebases.

Read first (this order):

1. The current card YAML — read fully, including underscore-prefixed
   subtrees (`_research_metadata`, `_review_handback`,
   `_partition_provenance` if multi-track).
2. The matching JSON schema (CIC or CLC).
3. The §18 main file and amendment chain listed above. Note especially
   the §18.5 / §18.6 schema-example blocks (which are the schema
   contract surface for new field proposals) and §18.16 implementation-
   phase mapping (so you don't propose v0.2-only behavior as a v0.1
   card edit).
4. The architecture v7.0.11 + v7.0.12 amendments.
5. The §4 v2.x card-hardening section + the §4 v2.x.7 OD-C amendment
   (the LIVE F-CARDS-COUPLING-VIOLATION-EXTENSION shape).
6. Any local prior-art listed in `_research_metadata.priors_consulted`.
7. Existing primary sources listed in `_research_metadata.primary_sources`;
   verify which are still current (Internet Archive snapshot pass is
   sufficient evidence of present-day reachability).
8. The Wave 1 + Wave 2 Thesis audit trails relevant to this card:
   - pipeline/validation/cards_wave_1_thesis_2026-05-15/ (food_systems
     + operating_capacity Cycle 1 + Cycle 2)
   - pipeline/validation/cards_wave_2_thesis_2026-05-15/ (12 cards Cycle
     1 + Cycle 2 + WAVE_2_CLOSE_SYNTHESIS.md)
9. The OD-A admin_risk_register v2.4 workspace-wide migration (per
   pipeline/handoffs/od_a_completion_2026-05-16.md). Read the CLC-axis
   register entries that overlap your card's vocabulary; route
   redundant-with-register flagged terms back to the register, do not
   re-encode them in the card body.

Research task:

For this one card, maximize real operational benefit by finding the
highest-leverage improvements to:
- search vocabulary or classification (CIC: search_vocabulary.core_terms
  / synonym_map / funder_program_keywords / disqualifier_terms; CLC:
  the equivalent inside underwriting_criteria + reviewer_profile_typical
  + common_red_flags),
- evidence capture and missing-evidence prompts,
- KFR fact classes and provenance_requirements (CIC) / scoring weight
  patterns + evidence_weights (CLC),
- drafting register and admin-risk handling (route shared flagged terms
  to admin_risk_register.yaml v2.4 per OD-A),
- reviewer/rubric logic,
- red-team probes (CLC.common_red_flags.red_team_probe),
- reporting/commitment extraction (CLC.commitment_tracking_pattern),
- memory namespace usefulness (cards:cic:<slug>:* / cards:clc:<slug>:*
  per architecture v7.0.11 §1.9),
- regression tests and acceptance tests (tests/cards/ mirror).

For multi-track CLCs (CLC-05/06/07): each finding is per-track unless it
applies to shared root metadata. Do not propose track restructuring or a
third track — Option A (top-level track_a / track_b) is LOCKED at row 274;
re-shape requires a §18.6 v3 amendment.

Required output (single file:
docs/<cic|clc>_<slug>_research_handback_<YYYY-MM-DD>.md):

1. Card Impact Thesis
   - One paragraph: what this card should cause Tilth to do differently.
   - For multi-track CLCs: two sub-paragraphs, one per track.

2. Current State Audit
   - What is strong now.
   - What is stale, ambiguous, over-broad, too local, too federal, or
     under-sourced.
   - Lifecycle / signature / schema concerns. (Specifically: flag the
     `draft_status: "draft"` gap; flag any other lifecycle inconsistency
     surfaced during read.)
   - Coupling-discipline self-audit: scan card body against the LIVE
     value-position regex set (rule 3); if any non-exempt match exists,
     flag as a regression risk to surface to operator for FIX-IN-PLACE
     dispatch (precedent: OD-C row 272 sponsorship_corporate).

3. Research Findings
   - Source table with URL, source type (official / primary /
     practitioner / secondary), access date, fields supported, and
     confidence (HIGH / MEDIUM / LOW).
   - Separate official/primary sources from practitioner/secondary
     sources.

4. Proposed Card Improvements
   - Field-by-field changes, grouped by the eight runtime-behavior
     categories from the Research task list above.
   - Exact YAML path for each change (e.g.,
     `search_vocabulary.core_terms[NEW]` or
     `track_a.evidence_weights.buyer_letters_of_intent.weight`).
   - Why the change improves runtime behavior (which seat: Scout /
     Scribe / Judge / Logician / Archivist / Report Generator / Model
     Router).
   - Whether the change belongs in card YAML, Program Rule Pack,
     admin-risk register, funder database, rubric library, or the
     future v1.x matrix layer. (Default: if the proposal is repeated
     across cards or shifts with program law, it does NOT belong in
     this card.)
   - Phase 4 fold-in discipline self-check: confirm the proposal does
     not trip any of the four refusals from §18.11 v1.1.

5. Operator Decision Queue
   - Decisions that require Josh / operator approval.
   - Admin-risk terms requiring approval (per OD-A v2.4 schema:
     term + severity + per_clc_register map + context + alternatives +
     approval_required).
   - State-specific or deployment-specific choices (PA examples vs base
     card; OD-G state-overlay amendment surface).
   - For multi-track CLCs: per-track decisions surfaced separately.

6. Validation Checklist
   - Schema fields complete against the current §18.5 / §18.6 schema
     (including item-level not.anyOf defense-in-depth).
   - No forbidden coupling field names (FORBIDDEN_FIELD_REGISTRY scan,
     including nested-in-item).
   - No forbidden value-position regex matches outside exempt paths.
   - No private organization-specific data.
   - No unsourced program-law claims (defer to Program Rule Pack).
   - No excessive quoted source text.
   - Lifecycle status consistent with architecture v7.0.11 §1.5.
   - For multi-track CLCs: shared root metadata preserved; oneOf branch
     2 (multi-track) compliance verified.

7. Regression Tests
   - 3 to 5 prompts that should demonstrate behavior change between
     pre-edit and post-edit cards.
   - Expected Scout / Scribe / Judge / Logician behavior per prompt.
   - For multi-track CLCs: at least one prompt that distinguishes track
     A from track B routing.

8. Patch Plan
   - Proposed edits grouped by file path.
   - No edits applied. Operator dispatches the edit + supersession-re-
     sign as a separate ceremony per the OD-C / OD-E precedent (per-
     card lock_history supersession row + post-restructure SHA3-512 +
     publisher Ed25519 signature against
     vault_shared/cards/publisher_pubkey.signed.yaml).
   - Include the OD-D Phase 4 forward-binding contract note: if your
     proposal touches refusal (c) or (d) territory, mark it for
     R-CARDS-ENUM-CANONICAL (OD-B, pending) or F-CARDS-COUPLING-
     VIOLATION-EXTENSION regression hardening at v0.2.

End each handback with a one-line summary:

   Card: <axis>:<slug>
   Card file: pipeline/cards/<axis>/<slug>.yaml
   Research hours actual: <X.X>
   Findings: <N total — N P0, N P1, N P2>
   Decision queue: <N operator approvals required>
   Conflicts with prior art: <N or NONE>
   Coupling-discipline regression: <NONE | N findings>
   Lifecycle gap surfaced: draft_status reads "draft", architecture
     v7.0.11 §1.5 requires "signed" for production load — recommend
     operator supersession-re-sign flip.
   Review readiness: READY | DEFER_PENDING_CHANGES
```

## §3 — Why the F-CARDS-COUPLING-VIOLATION-EXTENSION rules are framed this way

Per `pipeline/logician/gates/f_cards_coupling_violation_extension.py` (LIVE since OD-C row 272, 2026-05-17T05:30:00Z):

- The `FORBIDDEN_FIELD_REGISTRY` constant is `MappingProxyType`-wrapped at module load (per §4 v2.x.1 row-198 RT-14 fold-in) and lists the 7 CIC-side + 6 CLC-side forbidden top-level field names. The registry is the field-name-layer enforcement.
- The recursive value-position regex scan (added at OD-C) catches the creative-renaming class — a researcher who writes "behaves like TILTH-CLC-03" in a `description` field fails the gate even though the field name is canonical. The four patterns plus the exempt-path allowlist are the value-layer enforcement.
- The matrix-card structural rule fires on any populated matrix card before v1.x — `binding_eligibility: true` or `status != "FORWARD_COMPAT_ONLY"`. Pre-v1.x matrix population is forbidden.

Together these three layers close the design-time CIC × CLC coupling vector at the predicate-body layer (per OD-C completion handback §What landed). The L-024 lesson candidate from OD-E (don't conflate grant logic with credit underwriting logic; stacked funding stacks separate mechanisms) is the runtime-behavior analog: even when two CLCs co-fund a project, their underwriting logic stays orthogonal.

## §4 — OD-E §18.6 v2 dual-track shape (binding for CLC-05/06/07)

Per `pipeline/blueprint/v0.1/section_18_6_v2_dual_track_amendment.md` (LOCKED row 274, 2026-05-17T16:00:00Z):

- Schema delta lands two new optional top-level properties (`track_a` + `track_b`) plus a new `$defs.track_container` plus a new top-level `oneOf` with two mutually-exclusive branches (single-track legacy / multi-track Option A).
- The three multi-track CLC cards already restructured under Option A:
  - **CLC-05 market_access**: `track_a` = `sbir_phase_ii`, `track_b` = `sbir_phase_iii`.
  - **CLC-06 credit_underwriting**: `track_a` = `debt`, `track_b` = `grant`. Per operator directive at OD-E ceremony, Track B is a minimal-stub; a separate grant-side credit-readiness CLC is planned for v0.2 Wave 3. The L-024 lesson is folded into `_partition_provenance.domain_clarification` of the card. Do not propose substantive Track B content for CLC-06.
  - **CLC-07 sponsorship_corporate**: `track_a` = `benefits_exchange`, `track_b` = `corp_foundation_grant`.
- Shared root-level metadata (schema_version / card_axis / card_id / slug / display_name / funding_mechanism_summary / tilth_clc_id / lifecycle / `_research_metadata`) stays at root for all three cards.
- `funding_mechanism_summary` reads as a single-sentence summary spanning both tracks; per-track summaries live in `track_a.track_description` + `track_b.track_description`.
- The item-level `not.anyOf` defense-in-depth is replicated inside each `track_container` — forbidden CIC-coupling field names cannot appear nested in a track container any more than they can at root.
- Restructuring or re-shaping is a §18.6 v3 amendment surface; do not propose it from a research session.

## §5 — The lifecycle `draft_status` discrepancy — verified on disk; remediation routed to operator

The operator's working artifact flagged that "every parsed card has `draft_status: 'draft'` while also showing signed/thesis-passed/loaded — architecture says production load expects `draft_status: signed`."

**Verified on disk 2026-05-17.** All 14 card YAMLs (6 CIC + 8 CLC) carry `lifecycle.draft_status: "draft"` while every other lifecycle gate is at its pass-state:

```
lifecycle:
  draft_status: "draft"          # ← gap: should be "signed" or "loaded"
  review_status: "passed"
  cross_family_thesis_status: "passed"
  signature_status: "signed"
  runtime_load_status: "loaded"
```

**Verdict.** This is **not** a vocabulary-scrub residue (the v7.0.12 scrub retired `funder_political_axis`, not `draft_status` — the field name `draft_status` is the canonical schema name at `pipeline/cards/_schema/card_cic.schema.json` line 217 and `card_clc.schema.json` line 126, and the §18.12 lifecycle progression `draft → reviewed → thesis_passed → signed → loaded → deprecated` is the binding enum). It is **not** a parser artifact (the operator's parse matches the canonical bytes). It **is** a real production-load gap per architecture v7.0.11 §1.5: "Production: `draft_status` MUST be `signed`."

The cards' own header comments confirm the lineage — they flip `review_status pending→passed; signature_status unsigned→signed; runtime_load_status not_loaded→loaded` but never advance `draft_status` past `draft`. This appears to be a Wave 1 / Wave 2 LOCK ceremony oversight: the gate-status fields were flipped through the lifecycle, but the lifecycle-state-name field (`draft_status`) was left at its initial value.

**Recommendation (route to operator dispatch; do NOT execute from a research session).** Flip `draft_status: "draft"` → `draft_status: "signed"` on all 14 LOCKed card YAMLs as a per-card supersession-re-sign ceremony, modeled on the OD-E row 274 / 276 / 277 / 278 supersession pattern (parent_lock_row = each card's Wave 1 / Wave 2 row; ceremony_parent_row = a new §18 v1.x.draft_status_normalization amendment row). Embedded `ed25519_signature` may be left stale per the OD-C row 272 precedent (loader-time re-validation is v0.2 first-wave scope). Alternatively, the operator may flip to `"loaded"` to track the deepest passed gate — both values are admissible by the schema enum; `"signed"` matches the architecture v7.0.11 §1.5 minimum, `"loaded"` matches the actual current runtime_load_status.

Either path requires:
1. A new §18 v1.x amendment file (`section_18_v1_x_draft_status_normalization_amendment.md`) describing the flip + the 14-card supersession-re-sign roster.
2. A `§0.5 v_` paired-commit amendment registering one marker row.
3. A 14-row `card_cartridge_supersession` compound LOCK ceremony at the same `lock_timestamp_utc` per §6.17 Option-B.

Until that ceremony fires, production-load claims about the cards remain inaccurate at the lifecycle layer; the v0.2 first-wave loader graduation per architecture v7.0.11 §5 will surface this as `F-CARDS-UNSIGNED-PRODUCTION-LOAD` if the gap is still present at loader-go-live.

## §6 — CLC-06 Track B carve-out (binding for any researcher dispatched to credit_underwriting)

Per OD-E row 277 operator directive (2026-05-17, verbatim folded into `pipeline/cards/CLC/credit_underwriting.yaml` `_partition_provenance.domain_clarification` + §G of `section_00_5_section_18_6_v2_amendment.md`):

> Grant logic and credit underwriting logic are objectively different mechanisms even though both are financial-access tools. The stacked-funding use case (e.g., VAPG + low-interest farm loan + tourism grant + small business loan + small business advantage grant) requires separate logic per funding type. Track B is therefore not the right home for grant-side capital — a separate CLC for grant-side credit-readiness or grant-side capital matching belongs in v0.2 Wave 3, not as Track B of credit_underwriting.

The L-024 lesson candidate: **don't conflate grant logic with credit underwriting logic; stacked funding stacks separate mechanisms — each instrument deserves its own CLC at runtime, not Track A / Track B of one CLC.**

A researcher dispatched to CLC-06 must route any substantive grant-side capital-readiness recommendations to a v0.2 Wave 3 backlog item (provisional CLC slug: `grant_side_credit_readiness` or `capital_readiness_grant`; final naming pending Wave 3 dispatch). Recommendations for Track A (`debt`) are in scope.

## §7 — Admin-risk surface alignment (OD-A v2.4)

Per `pipeline/handoffs/od_a_completion_2026-05-16.md`: 60 net-new flagged terms migrated from 7 Wave 2 CLC cards into `admin_risk_register.yaml` v2.4 (45 GREEN / 13 YELLOW / 2 RED). Every v2.4 entry uses the v3.0 schema with `per_clc_register: tuple[tuple[str, str], ...]` (CLC-slug-keyed, values from {AVOID, OK, EXPECTED, PREFERRED}).

A researcher proposing a new admin-risk term:
1. Check the existing v2.4 entries first (`pipeline/institutional_memory/admin_risk_register.yaml`). If the term is already migrated and the proposal only adds a per-CLC-register cell for this card's CLC, route it as a register-cell-update recommendation, not a card-body addition.
2. If the term is new, format the proposal as a v3.0-schema-shaped entry: `term + severity + per_clc_register + context + alternatives + notes + migrated_from + approval_required: true`. Mark for operator review at the operator's separate v2.x → v3.0 scrub workflow.
3. Card-body `admin_risk_term_register` entries that are repeated across CLCs are the migration candidates per the OD-A pattern. Card-body entries that are CIC-side and applicant-specific stay on the CIC card.

## §8 — Discrepancies surfaced during the read pass

1. **`draft_status` lifecycle gap.** All 14 cards on disk carry `lifecycle.draft_status: "draft"` despite passing every other gate. See §5 above. Verified by direct YAML read 2026-05-17.

2. **Operator-side vocabulary slip.** The operator's working artifact uses "Customer Information Cards" in the title and section headers, while the canonical term is "Customer Identity Cards". A researcher must use the canonical term in card bodies; the working name is for the operator's external-facing prose only. The OD-C value-position regex does not match "Customer Information" (the pattern is `[Cc]ustomer [Ii]dentity`), so the slip is not a fail-closed risk — but it is a vocabulary-discipline risk that propagates if uncorrected.

3. **§18 main file post-OD-D supersession (row 269) re-pins canonical bytes after the §18.11 v1.1 Phase 4 checklist insert.** Any prior reference to the §18 v1 canonical bytes pinned at Wave 1 LOCK row 228 is stale; the authoritative reference is now row 269. Researchers consulting the §18 main file should read the current bytes, not rely on a cached older version.

4. **Embedded `ed25519_signature` is intentionally stale on the 3 OD-E-restructured CLC cards** (market_access / credit_underwriting / sponsorship_corporate) per OD-C row 272 precedent. The authoritative new signature lives in the lock_history supersession row; loader-time re-validation is v0.2 first-wave scope. A research-session validation script that checks the embedded sig against the pinned pubkey will report a mismatch on these three cards — that is the expected state, not a defect.

5. **The OQ-3 lowercase directive (`pipeline/cards/cic/` + `pipeline/cards/clc/`) was superseded by the on-disk uppercase scaffold** per §18 v1.1 §1.1. A researcher who follows an older prompt or task spec referencing lowercase paths must use uppercase in card body content (header comments, decision queue notes, all path references).

6. **The operator's working artifact at §Most-important-correction says "older drafts still mention `common_clc_patterns_observed`. The later schema, README, architecture amendment, and hardening spec kill that field."** Verified: `common_clc_patterns_observed` is the first entry in the CIC-side `FORBIDDEN_FIELD_REGISTRY` and would fail closed at load time. No researcher should reintroduce it under any synonym.
