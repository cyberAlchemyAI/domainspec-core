# cards_ceremony_batch_synthesis_2026-05-17

**Run 4 / Batch Supervisor Synthesis — unified Patch Plan rolling up Run 2 (14 per-card handbacks) + Run 3 (operator-authored CLC aggregate + OD-E path-(a) ratification).**

| Field | Value |
|---|---|
| Filed | 2026-05-17 |
| Workspace | `/Users/goldenquill/Downloads/GoldenQuill/` |
| Authority | `docs/cic_clc_unified_batch_supervisor_prompt_2026-05-17.md` §3–§6 + the Run 1 `FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2.md` Patch IDs (A1-A5, B1-B20, C1-C4, D1-D6, E1-E5) + operator Run 3 directive ratifying OD-E path (a). |
| Scope cap | Consolidation only. NO LOCKed-file edits. NO LOCK firing. NO git. Sidecar at `docs/` only. NO continuation of Run 2 per-card research depth. |
| Reference discipline | Run 2 handbacks cited by path, never re-quoted (Run 1 L-002). Run 1 patch IDs re-used; net-new patch IDs prefixed `R4-`. |
| Prior-art rollup | Run 1: `docs/card_system_deep_research_2026-05-17/INITIAL_CTO_HANDOFF_BLOCKERS.md` + `FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2.md`. Run 2: 14 handbacks under `docs/cic_*_research_handback_2026-05-17.md` + `docs/clc_*_research_handback_2026-05-17.md`. Run 3: `docs/clc_run_aggregate_2026-05-17.md` (operator independent CLC aggregate). |

---

## §0. One-paragraph rollup

Run 2 produced 14 per-card handbacks totaling **356 findings (12 P0 / 172 P1 / 172 P2)** with **CIC subtotal 160 (0 P0 / 77 P1 / 83 P2)** and **CLC subtotal 196 (12 P0 / 95 P1 / 89 P2)**. Run 3 (the operator-authored CLC aggregate at `docs/clc_run_aggregate_2026-05-17.md`) surfaced **one ceremony-vs-ground-truth integrity incident**: the §18.6 v2 dual-track restructure for CLC-05 / CLC-06 / CLC-07 was signed into `lock_history.v1.jsonl` rows 276/277/278 at 2026-05-17T16:00:00Z but **never written to disk**; the +178-byte delta on the three card files is entirely Wave 2 LOCK lifecycle promotion, not the claimed `track_a:` / `track_b:` / `_partition_provenance:` containers. **Operator has ratified path (a)** — fix-forward via re-run of the restructure WRITE + new supersession LOCK rows 280-286 (3 revocation + 3 realized-with-disk-write + 1 §0.5 paired-commit marker = 7-member compound). Separately, **CLC-07 carries two LIVE OD-C value-position regressions** at `sponsorship_corporate.yaml` line 97 + line 307 (TILTH-CLC-03 + TILTH-CLC-02 slug literals in non-exempt value positions), which fold into the OD-E remediation row 285 sponsorship_corporate re-sign (the restructure rewrites the surrounding scope; FIX-IN-PLACE landed atomically with the restructure write). The residual large cards-ceremony bundles **§18 v1.2 dialect_routing_table re-key (6 CIC cards + CIC schema)** + **Law-5 CLC `common_funders_observed` confirmation pass (up to 8 cards, subset re-signed)** + **schema patch B20 for the `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` field on both schemas** + **14-card content-improvement bundle from Run 2 handbacks routed to supersession-re-sign per OD-E precedent**. Cross-CIC admin-risk-register migration to v3.0 (per_cic_register + per_clc_register cells) is pre-staged for operator approval and **does NOT auto-rewrite** — it is sidecar v3.0-schema-shaped scaffolding only. Documentation-only A1-A5 status: A1 already retired (Run 1 P0-3 stale-claim is corrected by the master-prompt §5 fix); A2-A5 remain pending and routed to a no-LOCK documentation pass. Operator pre-work estimate aggregate: **30-42 hours of content-judgment** (18-30 for §18 v1.2; ~12 for Law-5 + content-improvement reviews; OD-E pre-work is mechanical — the in-memory restructure script per `pipeline/scripts/od_e_restructure_card.py` is canonical and already exists).

---

## §1. Run 3 fold-in: OD-E remediation (path-(a) RATIFIED 2026-05-17 by operator)

### §1.1 Incident recap (compressed; full evidence at `docs/clc_run_aggregate_2026-05-17.md` §4)

The OD-E ceremony at `lock_history.v1.jsonl` rows 274-278 (2026-05-17T16:00:00Z) signed five compound members. Rows 274/275 (blueprint-side §18.6 v2 amendment + §0.5 paired-commit) ARE valid against disk. Rows 276/277/278 (`card_cartridge_supersession` for `market_access.yaml` / `credit_underwriting.yaml` / `sponsorship_corporate.yaml`) **are NOT valid against disk** — the on-disk file SHA3-512 hashes (`bcf1d940..` / `55efb594..` / `696a48d3..`) do not match the row-asserted hashes (`4eb75e92..` / `bc050602..` / `58b61e03..`); the +178 byte delta is the Wave 2 lifecycle promotion only; no `track_a:` / `track_b:` / `_partition_provenance:` block exists on any of the three cards.

### §1.2 Ratified resolution shape (path (a), per operator 2026-05-17)

Re-run the in-memory restructure WRITE step against disk + dispatch a new compound LOCK ceremony at a new `lock_timestamp_utc` that:

1. Records three explicit supersession-revocation rows for the failed claims (rows 276/277/278).
2. Lands three new `card_cartridge_supersession` rows actually delivering the restructure to disk (canonical bytes verified by post-write SHA3-512 re-read).
3. Anchors with one `§0.5 paired-commit` marker row.

**Member count: 7.** Roster:

| Row | Lock_class | File | Purpose |
|---|---|---|---|
| 280 | `supersession_revocation` | `pipeline/engineering/lock_history.v1.jsonl` annotation pointer to row 276 | Records row 276 SHA3-512 claim is unverifiable against disk; supersedes the claim, not the amendment |
| 281 | `supersession_revocation` | annotation pointer to row 277 | Same for credit_underwriting (also captures L-024 verbatim carve-out chain break) |
| 282 | `supersession_revocation` | annotation pointer to row 278 | Same for sponsorship_corporate |
| 283 | `card_cartridge_supersession` | `pipeline/cards/CLC/market_access.yaml` | Restructure WRITTEN; `track_a = sbir_phase_ii` / `track_b = sbir_phase_iii` partition realized; canonical bytes + SHA3-512 re-read-verified before signature emission |
| 284 | `card_cartridge_supersession` | `pipeline/cards/CLC/credit_underwriting.yaml` | Restructure WRITTEN; `track_a = debt` (full) / `track_b = grant` (MINIMAL-STUB per L-024 carve-out, with `_partition_provenance.domain_clarification.l_024_candidate` body verbatim from operator); SHA3-512 re-read-verified |
| 285 | `card_cartridge_supersession` | `pipeline/cards/CLC/sponsorship_corporate.yaml` | Restructure WRITTEN; `track_a = benefits_exchange` / `track_b = corp_foundation_grant`; **CLC-07 OD-C FIX-IN-PLACE folded atomically** (line 97 + line 307 slug literals replaced with display names during write); SHA3-512 re-read-verified |
| 286 | `§0.5 paired-commit` | `pipeline/blueprint/v0.1/section_00_5_section_18_6_v2_amendment.md` (re-fire marker block) | Compound parent registration at the new `lock_timestamp_utc` |

**Standing discipline going forward (L-025 graduated to enforcement):** every `card_cartridge_supersession` row written must be preceded by a ceremony-script preflight that (a) writes the new card bytes to disk, (b) re-reads the file, (c) computes SHA3-512 from the re-read bytes, and (d) compares to the in-memory SHA3-512 before signature emission. Mismatch = abort. The preflight runs at the ceremony script layer (not loader; loader is unchanged at v0.1). L-026 (mirror-of-L-025-at-card-layer) lands as a lessons-only row; the script-side enforcement was the gap that produced the original OD-E miss.

### §1.3 Knock-ons absorbed by OD-E remediation

The OD-E remediation **absorbs** the following original-Patch-Queue items because they were premised on the §18.6 v2 restructure landing:

- **Patch B8** (`pipeline/cards/_schema/card_clc.schema.json` dual-track delta) — Row 283/284/285 write paths assume schema already permits `track_a:` / `track_b:` / `_partition_provenance:`. Status: schema delta is **assumed live at OD-E re-fire**; per Run 1 §2 Batch B, the schema patch is a separate compound-member; recommendation is to fold the schema-patch row INTO the 7-member OD-E remediation as an 8th member if the schema is also not yet on disk. **Pre-write verification step:** before OD-E re-fire, operator confirms `git status` on `card_clc.schema.json` and whether the schema delta is on disk. If on-disk: 7 members. If not: 8 members (add schema row at position 280, shift others).
- **Patches B9-B11** (the 3 multi-track CLC card re-signs) — fully absorbed by rows 283/284/285. These Patch IDs are now SUBSUMED by OD-E remediation rows.
- **CLC-07 OD-C FIX-IN-PLACE** (line 97 underwriting_criteria[11].description + line 307 narrative_section_patterns[8].note) — fully absorbed by row 285. The restructure rewrites the surrounding `track_b.underwriting_criteria` + `track_b.narrative_section_patterns` scope; the slug literals must be replaced with display names during the write. **Post-write verification:** Cowork regression test = "scan card body for `TILTH-CLC-NN` slug literals in non-exempt paths; expect 0 findings post-OD-E rewrite." Mismatch = abort.

### §1.4 Standalone OD-C-followon supersession (pre-staged; operator-discretion option)

If operator opts to fire CLC-07 OD-C FIX-IN-PLACE **before** OD-E re-fire (e.g., to clear the regression flag faster than the OD-E ceremony cycle allows), pre-staged shape:

| Row | Lock_class | File | Purpose |
|---|---|---|---|
| N | `card_cartridge_supersession` | `pipeline/cards/CLC/sponsorship_corporate.yaml` | line 97 + line 307 slug literals replaced with display names; embedded `ed25519_signature` re-emitted; `content_hash` updated; SHA3-512 re-read-verified |

Single-row compound; lowest-cost ceremony shape. Pre-stage handoff at `pipeline/handoffs/od_c_followon_sponsorship_corporate_fix_in_place_2026-05-17.md` (Run 2 handback §6 cross-reference at `docs/clc_sponsorship_corporate_research_handback_2026-05-17.md`).

**Recommendation:** fold into OD-E remediation (single ceremony, single `lock_timestamp_utc`, lower cumulative ceremony cost). Standalone only if OD-E is deferred further than the operator's regression-clearance horizon.

---

## §2. §18 v1.2 dialect_routing_table re-key — operator content-judgment decision queue

### §2.1 Status

LOCKed-but-not-applied per Run 1 P0-1 / L2-F0 (`section_18_v1_2_amendment.md:5` carries `LOCKED` frontmatter; on-disk CIC schema + 6 CIC cards still carry the retired `funder_political_axis` 4-axis enum). Operator content-judgment per-row decision is the bottleneck; engineering schema + card patches are mechanical once decisions land.

### §2.2 Per-card decision queue (operator pre-work, ~18-30 hours per amendment FI-9 REVISED line 209)

For each CIC card, operator reads each existing `dialect_routing_table` row (currently keyed on `funder_political_axis`) and decides which of the 8 CLC slugs (`public_purpose_works` / `catalytic_change` / `operating_capacity` / `research_evidence` / `market_access` / `credit_underwriting` / `sponsorship_corporate` / `shared_assets`) captures the funder cluster THAT row served. No heuristic mapping. Per-card content-judgment per row.

| CIC card | Current row count | Source path | Estimated content-judgment hours |
|---|---|---|---|
| `pipeline/cards/CIC/food_systems.yaml` | 5 rows | Run 2 handback `docs/cic_food_systems_research_handback_2026-05-17.md` | 3-5 hrs |
| `pipeline/cards/CIC/educator.yaml` | 5 rows | `docs/cic_educator_research_handback_2026-05-17.md` | 3-5 hrs |
| `pipeline/cards/CIC/public_agency.yaml` | 5 rows | `docs/cic_public_agency_research_handback_2026-05-17.md` | 3-5 hrs |
| `pipeline/cards/CIC/arts_culture.yaml` | 5 rows | `docs/cic_arts_culture_research_handback_2026-05-17.md` | 3-5 hrs |
| `pipeline/cards/CIC/cooperative.yaml` | 5 rows | `docs/cic_cooperative_research_handback_2026-05-17.md` | 3-5 hrs |
| `pipeline/cards/CIC/ecosystem_intermediary.yaml` | 4 rows | `docs/cic_ecosystem_intermediary_research_handback_2026-05-17.md` | 3-5 hrs |
| **Total** | **29 rows** | — | **18-30 hrs** |

**Per-card output:** decision list of N CLC-keyed routing rows replacing N political-axis-keyed routing rows (row count may change; not 1:1). Each row carries `clc:` + `dialect:` (preserved/refined) + `register_description:` (free-form) + optional `example_program:`.

**Companion code patches** (engineering, after operator decisions land):

- `pipeline/seats/scribe/dialect.py` — rewire dialect resolution to read `clc` key instead of `funder_political_axis` (Run 1 Patch B2-B7 dependent companion).
- `pipeline/engineering/agents/references/dialect_codebook.yaml` — re-key from political axis to CLC slug.

### §2.3 Schema delta (Run 1 Patch B1; mechanical once decisions land)

`pipeline/cards/_schema/card_cic.schema.json` lines 208-274 receives the "After" block per `section_18_v1_2_amendment.md:90-140` with FI-5 + FI-6 fold-ins (drop `funder_political_axis`; add `clc` 8-enum + `dialect` + `register_description` + `example_program`; require `[clc, dialect, register_description]`; `additionalProperties: false`).

---

## §3. §18.6 v2 multi-track restructure — STATUS AFTER OD-E PATH (a) RATIFICATION

### §3.1 CLC-05 (market_access)

`track_a = sbir_phase_ii` / `track_b = sbir_phase_iii`. Operator content-judgment per-track decisions surfaced in Run 2 handback at `docs/clc_market_access_research_handback_2026-05-17.md` §5 (28 findings, 1 P0 absorbed by OD-E remediation, 14 P1 + 13 P2 routed to supersession-re-sign per content-improvement bundle in §6). **Decision queue items: 10.** Resolved by OD-E re-fire row 283.

### §3.2 CLC-06 (credit_underwriting)

`track_a = debt` (full content) / `track_b = grant` **MINIMAL-STUB per L-024 carve-out**. Operator-verbatim rationale carried in `_partition_provenance.domain_clarification.l_024_candidate` block. Per master prompt §6 / Run 4 brief: **do NOT propose substantive Track B expansion**. v0.2 Wave 3 backlog item: separate `grant_side_credit_readiness` CLC candidate (per Run 2 handback `docs/clc_credit_underwriting_research_handback_2026-05-17.md` §5; operator decides naming at v0.2 Wave 3 scoping). **Decision queue items: 18 (15 Track A + 3 Track B posture / v0.2 Wave 3 backlog).** Resolved by OD-E re-fire row 284.

### §3.3 CLC-07 (sponsorship_corporate)

`track_a = benefits_exchange` / `track_b = corp_foundation_grant`. Operator content-judgment per-track decisions surfaced in Run 2 handback at `docs/clc_sponsorship_corporate_research_handback_2026-05-17.md` §5 (31 findings, 4 P0: 2 OD-C value-position regressions + 1 §18.6 v2 structural dep + 1 ceremony-reconciliation gate; 14 P1 + 13 P2 routed to supersession-re-sign per content-improvement bundle in §6). **Decision queue items: 17.** Resolved by OD-E re-fire row 285 + OD-C FIX-IN-PLACE atomic fold.

---

## §4. CLC-07 OD-C value-position regression FIX-IN-PLACE

### §4.1 Two LIVE findings (Run 2 handback §2.4 + Run 3 aggregate §2 coupling-discipline regression scan)

| Line | Path | Literal | Defense-in-depth status |
|---|---|---|---|
| 97 | `track_b.underwriting_criteria[11].description` | `TILTH-CLC-03` + `TILTH-CLC-02` | Non-exempt value position — REGRESSION P0 |
| 307 | `track_b.narrative_section_patterns[8].note` | `TILTH-CLC-03` | Non-exempt value position — REGRESSION P0 |

Total 3 hits across 2 paths. Sub-tag fires under LIVE `F-CARDS-COUPLING-VIOLATION-EXTENSION.value_literal_clc_slug` — except the gate body is still `NotImplementedError` (Run 1 P1-1), so these regressions pass silently TODAY. They are surfaced by AST-lint + sidecar regression scan, not by runtime gate.

### §4.2 FIX-IN-PLACE pattern (OD-C row 272 precedent)

Mechanical display-name swap:

- Line 97: replace `Behaves identically to **TILTH-CLC-03** Operating Capacity / **TILTH-CLC-02** Catalytic Change rubrics` with `Behaves identically to Operating Capacity / Catalytic Change rubrics`.
- Line 307: replace `See **TILTH-CLC-03** narrative_section_patterns for foundation-grant scaffold.` with `See the Operating Capacity narrative_section_patterns for foundation-grant scaffold.`

### §4.3 Disposition (post-OD-E-path-(a) ratification)

**FOLD INTO OD-E remediation row 285** (sponsorship_corporate restructure). The `track_b` rewrite operates on the same scope; the line 97 + line 307 slug literals must be expressed in display-name form during the new write. Atomic with the restructure. Standalone OD-C-followon pre-staged at `pipeline/handoffs/od_c_followon_sponsorship_corporate_fix_in_place_2026-05-17.md` is only fired if operator opts to clear the regression flag before OD-E re-fire.

**Post-write verification (mandatory):** Cowork regression scan against the rewritten card body; expect 0 `TILTH-CLC-NN` slug literals in non-exempt value positions. Mismatch = abort OD-E ceremony.

---

## §5. Law-5 CLC `common_funders_observed` confirmation pass — per-card status

### §5.1 Verification pass result (Run 2 + Run 3 cross-check)

Per Run 1 P1-3 and Run 3 aggregate §1: grep across all 8 CLC cards for `^common_funders_observed:` or `draft_funder_candidates_pending_operator_engagement_confirmation` returned zero matches at the time of the initial audit. Per-card status from Run 2 handbacks:

| CLC card | Field state | Status | Action |
|---|---|---|---|
| `public_purpose_works.yaml` | Field state per `docs/clc_public_purpose_works_research_handback_2026-05-17.md` §2 | confirm in handback §2 | A or B |
| `catalytic_change.yaml` | `docs/clc_catalytic_change_research_handback_2026-05-17.md` §2 | operator-confirmed-engagement-only Law-5 discipline cited (handback §2.x footnote re Stage-2+ horizon) | likely A or B |
| `operating_capacity.yaml` | `docs/clc_operating_capacity_research_handback_2026-05-17.md` §2 | confirm in handback §2 | A or B |
| `research_evidence.yaml` | `docs/clc_research_evidence_research_handback_2026-05-17.md` §2 | Law-5 split is the only P0 (per handback summary line 500); cross-card applies to all 8 CLCs | C (subagent-populated; relocate to `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`) |
| `market_access.yaml` | `docs/clc_market_access_research_handback_2026-05-17.md` §2 | confirm in handback §2 | A or B |
| `credit_underwriting.yaml` | `docs/clc_credit_underwriting_research_handback_2026-05-17.md` §2 | confirm in handback §2 | A or B |
| `sponsorship_corporate.yaml` | `docs/clc_sponsorship_corporate_research_handback_2026-05-17.md` §2 | confirm in handback §2 | A or B |
| `shared_assets.yaml` | `docs/clc_shared_assets_research_handback_2026-05-17.md` §2 (decision queue item: 13-entry roster) | C (13-entry candidate roster routed to draft block per handback §5) | C |

Outcomes:

- **A — Field absent/empty:** no action.
- **B — Operator-engagement-confirmed only:** add comment block citing engagement-confirmation timestamp; no structural change; no re-sign needed.
- **C — Subagent-speculative or unconfirmed:** empty `common_funders_observed:`; relocate to `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`; re-sign per OD-E pattern.

**Operator pre-work for C-transition cards:** ~30-60 min per card to confirm engagement status and authorize relocation. Aggregate ~2-4 hours if multiple C-cards.

### §5.2 Schema patch B20 (Run 1; mechanical)

`pipeline/cards/_schema/card_cic.schema.json` (lines 523-553 `_research_metadata`) + `pipeline/cards/_schema/card_clc.schema.json` (lines 373-378) receive an optional `draft_funder_candidates_pending_operator_engagement_confirmation:` property mirroring `common_funders_observed.items` shape. Description per Run 1 Patch B20 text. This makes the draft block schema-known and saves the operator a re-LOCK at every future Law-5 relocation. **Two schema files; either 2 separate compound members or 1 atomic schema-pin row covering both files.**

---

## §6. 14-card content-improvement bundle (Run 2 handback decision queues)

Per-card content improvements from Run 2 handbacks route to cards-ceremony supersession-re-sign per OD-E precedent. Aggregate operator pre-work estimate from handback summary blocks:

| Card axis | Cards | Findings (P0/P1/P2) | Decision-queue items | Re-sign needed? |
|---|---|---|---|---|
| CIC × 6 | food_systems, educator, public_agency, arts_culture, cooperative, ecosystem_intermediary | 24+30+25+28+26+27 = **160** (0 / 77 / 83) | aggregate per-card per handback §5 | YES — bundle into §18 v1.2 re-sign (Patches B2-B7) |
| CLC × 5 single-track | public_purpose_works, catalytic_change, operating_capacity, research_evidence, shared_assets | 27+22+23+23+23 = **118** (6 P0 — 3 framing-of-§18.6-v2 structural + 3 other / 56 P1 / 56 P2) | aggregate per-card per handback §5 | YES — separate supersession-re-sign per card per OD-E precedent |
| CLC × 3 multi-track | market_access, credit_underwriting, sponsorship_corporate | 28+19+31 = **78** (6 P0 — 3 §18.6 v2 structural + 2 OD-C + 1 ceremony-recon / 39 P1 / 33 P2) | absorbed by OD-E re-fire (rows 283/284/285) | YES — folded into OD-E remediation |

**Operator pre-work review (estimate):** ~6-10 hours scanning per-card §5 decision queues and authorizing/declining each. Many decisions are mechanical adopt-as-proposed; per-card §5 surfaces are pre-shaped for fast operator pass.

**Routing recommendation per Run 4 brief:** all content improvements route to cards-ceremony supersession-re-sign per OD-E precedent. Per-card content text is operator-authored / operator-approved (not subagent-fabricated; Law-5 boundary). Compound members for the LARGE cards-ceremony are listed in §8 below.

---

## §7. Cross-CIC admin-risk-register migration (≥3-card recurrence threshold, OD-A v2.4 → v3.0)

### §7.1 Cross-card pattern (Run 2 CIC handbacks)

Five of six CIC handbacks surface the same finding: 7-15 admin_risk_term entries per card, with a meaningful subset shared across ≥3 CIC cards. Sample (from CIC handback §2.5 + §4 decision-queue items):

- **food_systems** + **arts_culture** + **cooperative** + **educator** + **public_agency** + **ecosystem_intermediary** all carry `DEI` / `equity` / `inclusion` admin_risk_term entries (≥3 of 6).
- **arts_culture** + **educator** + **public_agency** all carry `racial justice` / `anti-racist` (≥3 of 6).
- **arts_culture** + **cooperative** + **educator** all carry `decolonial` / `abolition` (3 of 6).
- **food_systems** + **arts_culture** + **educator** + **public_agency** all carry `climate justice` (4 of 6).
- **public_agency** + **cooperative** carry `mutual aid` (2 of 6 — below threshold; stays per-card).

**Threshold for migration per OD-A v2.4 → v3.0:** ≥3-card recurrence routes term to workspace-register migration (per_cic_register + per_clc_register cells). Terms below threshold stay in per-card admin_risk_term_register.

### §7.2 Pre-staged v3.0-schema-shaped entries (operator-approval only; NOT auto-rewritten)

The pre-staged entries below sit at `docs/admin_risk_register_v3_0_scrub_pre_staging_2026-05-17.md` (suggested sidecar; NOT WRITTEN by this dispatch — pre-staged shape only). Each entry below is **operator-approval-required**:

```yaml
# v3.0-schema-shaped pre-staging (NOT auto-applied; operator dispatches separately)
DEI:
  severity: HIGH
  per_cic_register:
    food_systems: AVOID
    educator: AVOID
    public_agency: AVOID
    arts_culture: OPERATOR_DECIDES   # see arts_culture handback §2.5 + §3 verbatim-artist-voice carve-out
    cooperative: AVOID
    ecosystem_intermediary: AVOID
  per_clc_register:
    public_purpose_works: AVOID
    catalytic_change: OPERATOR_DECIDES
    operating_capacity: AVOID
    research_evidence: OK
    market_access: AVOID
    credit_underwriting: AVOID
    sponsorship_corporate: AVOID
    shared_assets: AVOID
  substitution_candidates: [<per source card>]
  reviewer_context: <per source card; merge under operator review>

equity:
  severity: MEDIUM
  per_cic_register: <as above pattern>
  per_clc_register: <as above pattern>
  substitution_candidates: [<merge>]
  reviewer_context: <merge>

# ... similar pre-stage for: inclusion, racial justice, anti-racist, decolonial,
# abolition, climate justice, social justice, marginalized, anti-displacement,
# Indigenous data sovereignty (NEW per ecosystem_intermediary handback §3),
# disrupt(ing) inequity (NEW per educator handback §3),
# environmental justice (REFINE per public_agency handback §3)
```

**Operator decision queue (this section):**

1. Approve / decline each cross-CIC migration term-by-term.
2. Approve / decline per-cell `AVOID | OK | EXPECTED | PREFERRED | OPERATOR_DECIDES` values.
3. Approve cross-card substitution_candidates merge (operator merges per-card variants; subagent does NOT auto-merge).
4. Approve net-new register entries (Indigenous data sovereignty / disrupt(ing) inequity / refined environmental justice).

**Workflow shape per Run 3 aggregate §5.2:** sidecar audit + operator-dispatched in-place register edits. NOT a LOCK ceremony for the v0.1 cycle (per Run 3 routing recommendation: 1-2 hours operator time once decisions land). The v3.0 schema delta itself **is** a LOCK item but lands separately as its own §0.5 paired-commit; pre-stage shape outlined here but NOT folded into the cards-ceremony.

### §7.3 Per-CLC-cell cross-coverage verification (Run 3 §5.2)

Run 2 + Run 3 CLC handbacks (CLC-01, CLC-02, CLC-04, CLC-08) surface the same pattern: OD-A migration moved 60 net-new flagged terms into the workspace register, but per-CLC-register cells (`per_clc_register: {clc_slug: AVOID|OK|EXPECTED|PREFERRED}`) are unevenly populated. For some terms this CLC slug is missing from per_clc_register; for others the cell value is stale. **Operator workflow item; not a LOCK ceremony; ~1-2 hours bulk-verification pass against `pipeline/logician/admin_risk_register.yaml` v2.4 + the 8 CLC slugs.**

---

## §8. The LARGE cards-ceremony — §6.17 Option-B compound paired-commit roster

### §8.1 Scope (after OD-E remediation lands)

After OD-E remediation fires (7 members; rows 280-286 or 280-287 depending on schema-row fold), the LARGE cards-ceremony bundles the residual cards-ceremony work into one compound LOCK at one `lock_timestamp_utc`. Modeled on the OD-E 5-row compound at row 274 precedent.

**Ceremony shape:** §6.17 Option-B compound paired-commit per `cic_clc_unified_batch_supervisor_prompt_2026-05-17.md` §4 (lines 315-322).

**Lock_timestamp_utc bucket:** `<NEXT-AVAILABLE-LARGE-CARDS-CEREMONY-UTC>` — operator pins at fire time.

### §8.2 Member count and roster

| Member | Lock_class | File | Patch ID | Purpose |
|---|---|---|---|---|
| 1 | `§18 amendment status flip` | `pipeline/blueprint/v0.1/section_18_v1_2_amendment.md` (frontmatter flip `LOCKED` → `LOCKED_COMPANION_LANDED` per Run 1 CR-1 recommendation if adopted; else no-op) | (Run 1 §18 v1.2) | Mark companion work landed |
| 2 | `§0.5 paired-commit` | `pipeline/blueprint/v0.1/section_00_5_section_18_v1_2_amendment.md` (or equivalent paired-commit file) | Run 1 Batch B compound member 3 | Compound parent registration |
| 3 | `schema` | `pipeline/cards/_schema/card_cic.schema.json` | Run 1 Patch B1 + B20 (CIC half) | §18 v1.2 dialect_routing_table delta + draft_funder_candidates field |
| 4 | `schema` | `pipeline/cards/_schema/card_clc.schema.json` | Run 1 Patch B20 (CLC half) | draft_funder_candidates field (and any other schema fold-in: lock_history_row disposition per Run 1 Patch E1 if operator chooses Option A) |
| 5-10 | `card_cartridge_supersession` × 6 | `pipeline/cards/CIC/{food_systems,educator,public_agency,arts_culture,cooperative,ecosystem_intermediary}.yaml` | Run 1 Patches B2-B7 + Run 2 content-improvement bundle for the 6 CICs | dialect re-key (per operator content-judgment per §2 above) + content improvements per handback §5 decision queue; new Ed25519 signature; new `content_hash`; SHA3-512 re-read verified per L-025 |
| 11-15 | `card_cartridge_supersession` × 5 | `pipeline/cards/CLC/{public_purpose_works,catalytic_change,operating_capacity,research_evidence,shared_assets}.yaml` | Run 2 single-track CLC content-improvement bundle + Run 1 Patches B12-B19 subset for C-transition Law-5 cards | content improvements per handback §5 decision queue + Law-5 relocation if C-transition; new sig; new hash; SHA3-512 re-read verified |

**Total compound member count: 15** (assuming all 5 single-track CLCs are re-signed, and all 6 CICs are re-signed). If only a subset of CLCs require re-sign (e.g., A-transition cards in §5 above are comment-only and need no re-sign), member count drops accordingly.

**Minimum compound member count if only structural changes:** 9 (members 1-4 + members 5-10 only — 6 CIC re-signs for §18 v1.2 dialect re-key; CLC re-signs deferred to a later ceremony).

### §8.3 Companion code patches (engineering, separate or concurrent)

| Patch | File | Status |
|---|---|---|
| Run 1 B2-B7 companion 1 | `pipeline/seats/scribe/dialect.py` | EDIT — re-wire dialect resolution to read `clc` key instead of `funder_political_axis` |
| Run 1 B2-B7 companion 2 | `pipeline/engineering/agents/references/dialect_codebook.yaml` | EDIT — re-key codebook from political axis to CLC slug |

**Engineering executes these in parallel with operator's cards-ceremony pre-work.** Code-patch LOCK row optional per operator preference (Run 1 Batch C disclaimer pattern).

### §8.4 Pre-ceremony checklist

1. OD-E remediation has fired (rows 280-286/287 LANDED; `lock_history.v1.jsonl` reads three new restructured CLC cards with disk-verified SHA3-512).
2. Operator has completed the per-row content-judgment re-keying for 6 CIC cards (§2 above; 18-30 hours).
3. Operator has completed Law-5 confirmation pass per CLC card (§5 above; ~2-4 hours for any C-transition cards).
4. Operator has reviewed 14-card content-improvement bundles per Run 2 handbacks (§6 above; 6-10 hours scanning).
5. L-025 ceremony-script preflight is wired (writes new bytes, re-reads, verifies SHA3-512 before signature emission). **MANDATORY** per Run 3 OD-E lesson.
6. `F-INDEX-STALE` PRE-gate verifies §0.5 paired-commit at compound LOCK.
7. NO LOCK initiated from this audit dispatch. Operator fires.

---

## §9. Documentation-only patches (Run 1 Batch A) — status update

| Patch | File | Run 1 status | Run 4 status |
|---|---|---|---|
| **A1** — Master prompt §5 stale-claim correction | `docs/cic_clc_unified_master_prompt_2026-05-17.md` (§5 + closing summary block) | P0-3 | **RETIRED per Run 1 P0-3 in conjunction with Run 3 §3 (operator-actionable sidecar fix routed)**. Sidecar edit pending; documentation-only; no LOCK. |
| A2 — README typography fix (Cards/Cards collision) | `pipeline/cards/README.md` + `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md` | P1-7 | **Pending.** Sidecar; documentation-only; no LOCK. Engineering-editor bench item. |
| A3 — README Wave-1/Wave-2 LOCK status comments | `pipeline/cards/README.md` lines 24-39 | P2-6 | **Pending.** Sidecar; documentation-only; no LOCK. Mechanical doc edit. |
| A4 — 14-card header-comment normalization | All 14 cards' top-of-file comment blocks | P1-4 | **Pending.** Cosmetic (comments NOT in canonical-bytes); no re-sign required; bundle with A2-A3 as one doc-only sweep. |
| A5 — Architecture v7.0.11 §1.4 lifecycle enum reconciliation | `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md` §1.4 | P0-2 | **Pending.** Documentation-only carve-out per OD-D row 270 precedent OR full §18 v1.x amendment (operator decides). No companion schema/loader change. |

**Aggregate Batch A operator review time:** ~1-2 hours. None of these block the cards-ceremony. Recommendation: bundle A2-A5 into one doc-only sweep at engineering-editor convenience; A1 sidecar is operator's own master-prompt edit.

---

## §10. Schema patches (Run 1 Batch B subset)

| Patch | File | Status |
|---|---|---|
| **B1** — CIC schema §18 v1.2 dialect delta | `pipeline/cards/_schema/card_cic.schema.json` lines 208-274 | Folds into LARGE cards-ceremony member 3 |
| **B8** — CLC schema §18.6 v2 dual-track delta | `pipeline/cards/_schema/card_clc.schema.json` | **PRE-WRITE VERIFICATION REQUIRED:** confirm on-disk status before OD-E re-fire. If on-disk: OD-E 7 members. If not: OD-E 8 members (schema row prepended). |
| **B20** — Both schemas' draft_funder_candidates field | both schema files | Folds into LARGE cards-ceremony members 3 + 4 |

No other Run 1 Batch B schema patches outside these three.

---

## §11. Compound LOCK ceremony summary (both phases)

### §11.1 Phase 1 — OD-E remediation (operator-authorized path (a); fires FIRST)

- **Member count: 7** (or 8 if §18.6 v2 schema delta is not yet on disk per §3 / §10 B8 verification).
- **Roster:** §1.2 above.
- **lock_timestamp_utc:** `<OD-E-RE-FIRE-UTC>` — operator pins.
- **Operator pre-work:** mechanical (re-run `pipeline/scripts/od_e_restructure_card.py` per Run 3 aggregate §4; verify CLC-07 OD-C FIX-IN-PLACE atomic; L-025 preflight wired).
- **Engineering pre-work:** L-025 preflight implementation.

### §11.2 Phase 2 — LARGE cards-ceremony (fires AFTER Phase 1 + operator content-judgment pre-work)

- **Member count: 15 (max) / 9 (minimum if Law-5 + content-improvement CLC re-signs deferred).**
- **Roster:** §8.2 above.
- **lock_timestamp_utc:** `<LARGE-CARDS-CEREMONY-UTC>` — operator pins.
- **Operator pre-work:** §2 (18-30 hrs dialect re-key) + §5 (~2-4 hrs Law-5) + §6 (~6-10 hrs content-improvement bundle review). Aggregate **30-42 hours**.
- **Engineering pre-work:** §8.3 companion code patches.

### §11.3 Cross-CIC admin-risk-register migration (§7) — sidecar workflow, NOT a LOCK ceremony

Operator approval queue described in §7.2 + §7.3. Fires as in-place register edits (1-2 hours operator time once decisions land). The v3.0 schema delta itself is a separate §0.5 paired-commit LOCK landing on its own timing.

---

## §12. Law-5 CLC verification — per-card summary (from §5 cross-referenced)

| CLC card | Law-5 status (Run 2 handback §2) | Action | Re-sign? |
|---|---|---|---|
| public_purpose_works | confirm per handback | A or B | likely no |
| catalytic_change | operator-confirmed-engagement Stage-2+ horizon discipline cited | likely A or B | no |
| operating_capacity | confirm per handback | A or B | likely no |
| research_evidence | Law-5 split flagged as cross-card P0 | C — relocate | yes |
| market_access | confirm per handback | A or B | absorbed by OD-E |
| credit_underwriting | confirm per handback | A or B | absorbed by OD-E |
| sponsorship_corporate | confirm per handback | A or B | absorbed by OD-E |
| shared_assets | 13-entry candidate roster routed to draft block per handback §5 | C — relocate | yes |

**Operator decision queue:** confirm A/B/C per card based on the handback §2 finding for each. Pre-stage shape is identical to the 6-CIC Phase E Option 2 cleanup pattern.

---

## §13. What this synthesis does NOT do

- Does NOT fire any LOCK ceremony (operator dispatches).
- Does NOT auto-rewrite any card body, schema, amendment, or LOCKed file.
- Does NOT re-quote per-card handback content (Run 1 L-002 path-reference discipline).
- Does NOT continue Run 2 per-card research depth.
- Does NOT auto-migrate the cross-CIC admin-risk-register (operator approves term-by-term).
- Does NOT Ed25519-re-sign (publisher key holder only).
- Does NOT touch git.

---

## §14. Files cited

- `docs/cic_clc_unified_master_prompt_2026-05-17.md`
- `docs/cic_clc_unified_batch_supervisor_prompt_2026-05-17.md`
- `docs/cic_clc_unified_research_plan_2026-05-17.md`
- `docs/clc_run_aggregate_2026-05-17.md` (Run 3 operator-authored CLC aggregate)
- `docs/card_system_deep_research_2026-05-17/INITIAL_CTO_HANDOFF_BLOCKERS.md`
- `docs/card_system_deep_research_2026-05-17/FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2.md`
- `docs/card_system_deep_research_2026-05-17/CARD_LIFECYCLE_AND_LOADER_GOVERNANCE_AUDIT.md`
- `docs/card_system_deep_research_2026-05-17/CANONICAL_NAMING_AND_ORTHOGONALITY_AUDIT.md`
- 6 CIC handbacks at `docs/cic_*_research_handback_2026-05-17.md`
- 8 CLC handbacks at `docs/clc_*_research_handback_2026-05-17.md`
- `pipeline/blueprint/v0.1/section_18_v1_2_amendment.md`
- `pipeline/blueprint/v0.1/section_18_6_v2_dual_track_amendment.md`
- `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md`
- `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md`
- `pipeline/cards/_schema/card_cic.schema.json`, `card_clc.schema.json`
- `pipeline/cards/registry.yaml`
- `pipeline/cards/loader.py`
- `pipeline/logician/gates/f_cards_*.py`
- `pipeline/logician/admin_risk_register.yaml`
- `pipeline/scripts/od_e_restructure_card.py` (canonical in-memory restructure script per Run 3 aggregate §4)
- `pipeline/engineering/lock_history.v1.jsonl`
- `pipeline/program_rule_packs/` (PRP scaffolding — CTO blind spot A live infrastructure)
- `pipeline/blueprint/v0.1/section_19_program_rule_packs.md`
- `vault_shared/key_rotation_policy.md`
- `vault_shared/operator_attestation/publisher_pubkey.signed.yaml`

---

**One-line summary:**

Cards-ceremony patch plan: **OD-E remediation** (7-8 member compound, path (a) ratified — fires FIRST; folds CLC-07 OD-C FIX-IN-PLACE atomically into row 285) THEN **LARGE cards-ceremony** (9-15 member compound — bundles §18 v1.2 dialect re-key for 6 CICs + Law-5 CLC relocation + 14-card content improvements + schema B1/B8/B20). Aggregate operator pre-work 30-42 hours (post-OD-E). Cross-CIC admin-risk-register migration pre-staged for operator term-by-term approval; sidecar workflow, NOT a LOCK ceremony. L-025 ceremony-script preflight is standing discipline going forward.

*End of Run 4 synthesis deliverable 1 of 2.*
