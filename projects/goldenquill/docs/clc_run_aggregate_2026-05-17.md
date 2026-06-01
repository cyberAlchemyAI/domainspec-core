# CLC Research Run — Aggregate Report

Prepared: 2026-05-17
Workspace: `/Users/goldenquill/Downloads/GoldenQuill/`
Dispatch authority: `docs/cic_clc_unified_master_prompt_2026-05-17.md` §0–§8
Pattern precedent: 6 CIC handbacks landed earlier 2026-05-17 (sibling files in `docs/cic_*_research_handback_2026-05-17.md`).

This aggregate consolidates 8 parallel sub-agent dispatches against the 8 signed runtime CLC cards. It surfaces cross-card patterns the per-card handbacks could not see individually and routes two operator-actionable surfaces — one stale-claim correction and one ceremony-vs-ground-truth integrity incident — for separate operator dispatch.

## §1 — Deliverables

Eight sidecar handbacks landed at `docs/clc_<slug>_research_handback_2026-05-17.md`:

| Card | Slug | Track shape | File | Lines | Verdict |
|------|------|------------|------|-------|---------|
| TILTH-CLC-01 | public_purpose_works | single_track | `docs/clc_public_purpose_works_research_handback_2026-05-17.md` | ~369 | READY |
| TILTH-CLC-02 | catalytic_change | single_track | `docs/clc_catalytic_change_research_handback_2026-05-17.md` | ~384 | READY |
| TILTH-CLC-03 | operating_capacity | single_track | `docs/clc_operating_capacity_research_handback_2026-05-17.md` | ~485 | READY |
| TILTH-CLC-04 | research_evidence | single_track | `docs/clc_research_evidence_research_handback_2026-05-17.md` | ~310 | READY |
| TILTH-CLC-05 | market_access | multi_track (claimed) | `docs/clc_market_access_research_handback_2026-05-17.md` | ~470 | DEFER (P0-S1 structural) |
| TILTH-CLC-06 | credit_underwriting | multi_track (claimed) | `docs/clc_credit_underwriting_research_handback_2026-05-17.md` | ~408 | DEFER (P0-S1 structural) |
| TILTH-CLC-07 | sponsorship_corporate | multi_track (claimed) | `docs/clc_sponsorship_corporate_research_handback_2026-05-17.md` | ~395 | READY (with structural dependency) |
| TILTH-CLC-08 | shared_assets | single_track | `docs/clc_shared_assets_research_handback_2026-05-17.md` | ~400 | READY |

Aggregate line count: ~3,221 lines across the 8 sidecars.

## §2 — Aggregate stats

### Findings

| Severity | Count | Notes |
|----------|-------|-------|
| **P0** | **6** | 3 structural (CLC-05 / CLC-06 / CLC-07 — shared structural incident below) + 3 from agents framing the structural mismatch differently per card |
| P1 | 100 | Behavior-changing improvements across the eight cards |
| P2 | 107 | Behavior-marginal / polish / forward-binding |
| **Total** | **213** | |

Per-card distribution: CLC-01 27 · CLC-02 24 · CLC-03 33 · CLC-04 31 · CLC-05 28 · CLC-06 17 · CLC-07 30 · CLC-08 23.

### Operator decision queue (aggregate)

**120 operator approvals** required across the 8 handbacks:
CLC-01 11 · CLC-02 14 · CLC-03 18 · CLC-04 21 · CLC-05 10 · CLC-06 18 · CLC-07 17 · CLC-08 11.

### Coupling-discipline regression scan results

| Card | LIVE OD-C value-position regex set | FORBIDDEN_FIELD_REGISTRY scan | Result |
|------|-----------------------------------|------------------------------|--------|
| CLC-01 | clean | clean | NONE |
| CLC-02 | clean | clean | NONE |
| CLC-03 | clean | clean | NONE |
| CLC-04 | clean | clean | NONE |
| CLC-05 | clean (proposed edits) | clean | NONE |
| CLC-06 | clean (Track A proposed edits) | clean | NONE |
| **CLC-07** | **2 PRE-EXISTING hits at lines 97 + 307** (`TILTH-CLC-03` + `TILTH-CLC-02` in non-exempt value positions) | clean | **2 findings (pre-existing card body, not from this run)** |
| CLC-08 | clean | clean | NONE |

CLC-07 pre-existing hits **regress** OD-C row 272 FIX-IN-PLACE (which the daily log claims swapped slugs for display names). Either the on-disk restructure / re-sign was incomplete, or the OD-C scan was incomplete. Bundled into CLC-07's Patch Plan §8.1 as canonical display-name swap (analog of the OD-C row 272 pattern).

### Phase 4 fold-in discipline self-checks

All 8 agents ran self-check; aggregate result:
- Zero refusal-(d) trips (literal canonical CIC/CLC slug strings in proposed non-exempt value positions).
- Zero refusal-(c) trips (compound enum values).
- 1 refusal-(a) trip routed correctly (CLC-02 `reviewer_profile_typical.evaluator_bench_examples` new sub-field → operator-decision-queue for §18 v1.x amendment graduation OR comment-block-only fallback).
- 1 refusal-(b) trip routed correctly (CLC-01 `cross_references_prp:` annotation field → comment-block-only fallback per CLC-06 / CLC-08 Wave 2 precedent).

## §3 — Master prompt §5 stale claim (CORRECTION — operator-actionable)

The master prompt at §5 + closing summary block §`Lifecycle gap surfaced` asserts as a binding contract that "every parsed runtime card currently carries `lifecycle.draft_status: 'draft'` on disk" and requires every handback to flag this as a gap.

**Direct verification 2026-05-17 (this run):**

```
=== draft_status per card (all 14) ===
pipeline/cards/CIC/arts_culture.yaml                    draft_status: "signed"
pipeline/cards/CIC/cooperative.yaml                     draft_status: "signed"
pipeline/cards/CIC/ecosystem_intermediary.yaml          draft_status: "signed"
pipeline/cards/CIC/educator.yaml                        draft_status: "signed"
pipeline/cards/CIC/food_systems.yaml                    draft_status: "signed"
pipeline/cards/CIC/public_agency.yaml                   draft_status: "signed"
pipeline/cards/CLC/catalytic_change.yaml                draft_status: "signed"
pipeline/cards/CLC/credit_underwriting.yaml             draft_status: "signed"
pipeline/cards/CLC/market_access.yaml                   draft_status: "signed"
pipeline/cards/CLC/operating_capacity.yaml              draft_status: "signed"
pipeline/cards/CLC/public_purpose_works.yaml            draft_status: "signed"
pipeline/cards/CLC/research_evidence.yaml               draft_status: "signed"
pipeline/cards/CLC/shared_assets.yaml                   draft_status: "signed"
pipeline/cards/CLC/sponsorship_corporate.yaml           draft_status: "signed"
```

**All 14 cards already read `draft_status: "signed"`.** The diff against the OD-E pre-restructure backups (which was the last bulk-snapshot) confirms the flip was bundled into Wave 2 LOCK lifecycle promotion (e.g., `market_access_pre_restructure.yaml` line 790 reads `"draft"`, current line 790 reads `"signed"`, with 4 new lifecycle metadata fields appended). The gap is **already remediated** — the §18 v1.x.draft_status_normalization amendment that master prompt §5 recommends does NOT need to be dispatched.

Multiple agents (CLC-01, CLC-02, CLC-03, CLC-04, CLC-06, CLC-07, CLC-08) correctly verified this on their own card and flagged the master-prompt claim as stale. CLC-08's framing is canonical: "master prompt §5 universal 'draft_status: draft' claim is STALE for this card and all 14 LOCKed cards per Run 1 priors — no normalization required."

**Routing recommendation (operator dispatch):**
- Update master prompt §5 to read "Verified 2026-05-17: lifecycle gap remediated at Wave 2 LOCK; no §18 v1.x.draft_status_normalization amendment required."
- Update closing summary block template: "Lifecycle gap surfaced: NONE (Wave 2 LOCK lifecycle promotion correctly flipped draft_status to 'signed' on all 14 cards)."
- Sidecar-only edit. No LOCKed file affected.

## §4 — P0 incident: §18.6 v2 dual-track restructure NEVER LANDED ON DISK (operator-actionable; integrity)

**Severity:** P0 (signed lock_history rows assert content that doesn't exist on disk; classification-register-integrity-equivalent for the cards layer).

**Independent surface points:**
1. CLC-05 agent §P0-S1 finding — direct grep + sha3 comparison.
2. CLC-06 agent §P0-S1 finding — same.
3. CLC-07 agent §3 finding (initial agent miscalled grep as positive but final report corrects to "structural restructure not yet on disk" + routes to operator dependency).
4. This run's own direct verification (below).

**Ground-truth verification (this run, 2026-05-17 post-handback):**

```
=== loose grep for any track_a / track_b / _partition_provenance at top-level ===
pipeline/cards/CLC/catalytic_change.yaml                     0
pipeline/cards/CLC/credit_underwriting.yaml                  0
pipeline/cards/CLC/market_access.yaml                        0
pipeline/cards/CLC/operating_capacity.yaml                   0
pipeline/cards/CLC/public_purpose_works.yaml                 0
pipeline/cards/CLC/research_evidence.yaml                    0
pipeline/cards/CLC/shared_assets.yaml                        0
pipeline/cards/CLC/sponsorship_corporate.yaml                0

=== content_hash vs supersession-row claim ===
market_access         sha256=3b76568028fef5cd.. sha3_512=bcf1d940c09d03fb.. lock_row=258 supersession_row=ABSENT (OD-E claim=276)
credit_underwriting   sha256=5cd7fba5c2d37d18.. sha3_512=55efb594ae2152bf.. lock_row=259 supersession_row=ABSENT (OD-E claim=277)
sponsorship_corporate sha256=7ea6333f23286e66.. sha3_512=696a48d327eae813.. lock_row=260 supersession_row=ABSENT (OD-E claim=278)

=== lock_history rows 276-278 file SHA3-512 claims ===
row 276 ts=2026-05-17T16:00:00Z file_sha3=4eb75e9296cffdf6.. file=pipeline/cards/CLC/market_access.yaml         [MISMATCH — disk reads bcf1d940..]
row 277 ts=2026-05-17T16:00:00Z file_sha3=bc050602bc6869ad.. file=pipeline/cards/CLC/credit_underwriting.yaml   [MISMATCH — disk reads 55efb594..]
row 278 ts=2026-05-17T16:00:00Z file_sha3=58b61e0382e83afc.. file=pipeline/cards/CLC/sponsorship_corporate.yaml [MISMATCH — disk reads 696a48d3..]

=== size delta vs pre-restructure backup ===
market_access             current=88651   backup=88473   delta=+178 bytes
credit_underwriting       current=94085   backup=93907   delta=+178 bytes
sponsorship_corporate     current=71957   backup=71779   delta=+178 bytes

=== diff backup vs current (market_access) — all 178 bytes accounted for ===
4,5c4,5  (header comment flip: PENDING/DRAFT → COMPLETE/SIGNED)
790c790  (draft_status: "draft" → "signed")
794a795,798  (added 4 lifecycle fields: runtime_loadable / signed_at / signed_by / content_hash)
```

**Diagnosis.** The OD-E ceremony at 2026-05-17T16:00:00Z signed five compound-LOCK rows asserting (a) §18.6 v2 amendment + §0.5 v32 paired-commit (rows 274/275, blueprint-side — these MATCH disk per row 279 corrective supersession), and (b) three `card_cartridge_supersession` rows for the cards' "post-restructure canonical bytes" (rows 276/277/278). The blueprint-side rows are valid. The three card-side rows are NOT valid against disk:

- The +178 byte delta is **entirely** the Wave 2 LOCK lifecycle promotion (which actually landed 2026-05-16T16:00:00Z, three days before OD-E).
- No top-level `track_a:` / `track_b:` containers exist.
- No `_partition_provenance:` block with the L-024 verbatim carve-out exists.
- No `supersession_lock_history_row` field exists in the `lifecycle:` block of any of the three cards.
- The CEREMONY_SUMMARY.md narrative + daily-log narrative both describe the restructure as having happened; the artifact evidence contradicts both.

The pre-restructure backups exist at `pipeline/validation/od_e_dual_track_2026-05-16/backup/{market_access,credit_underwriting,sponsorship_corporate}_pre_restructure.yaml` — these are what `current` files actually correspond to (modulo the Wave 2 lifecycle promotion). The intended-restructured files were never written.

**Hypothesis (most likely).** The OD-E ceremony script ran the restructure in-memory, computed canonical bytes + hashes from the in-memory restructured shape, signed them, appended the lock_history rows, flipped the amendment file `amendment_status` to LOCKED — but the `pipeline/cards/CLC/{slug}.yaml` write step was either omitted, was performed against a temp file that was never renamed in, or was rolled back. The lock_history is now asserting hashes that have no corresponding on-disk content.

**Impact.**
- Three signed lock_history rows (276/277/278) are unverifiable against on-disk bytes by the v0.2 first-wave loader graduation. When `F-CARDS-SIGNATURE-INVALID` flips from `NotImplementedError` to LIVE (per architecture v7.0.11 §5), the three cards will fail-closed at load.
- All §18.6 v2 amendment claims about multi-track CLCs (CLC-05/06/07) are not yet realized on disk. CLC-05 and CLC-07 handbacks include per-track YAML-path proposals (`track_a.*` / `track_b.*`) that **cannot land** until the restructure is actually on disk.
- The L-024 verbatim operator carve-out for CLC-06 Track B is recorded in lock_history row 277's `operator_decision_at_ceremony` block + in `section_00_5_section_18_6_v2_amendment.md` §G — but is **NOT on disk** in `credit_underwriting.yaml` `_partition_provenance.domain_clarification.l_024_candidate` as the CEREMONY_SUMMARY narrative claims. The carve-out's authority chain has a broken link.
- L-025 ("Pre-ceremony, amendment files should be authored with `amendment_status: LOCKED <ceremony_timestamp>` from the start, not flipped post-ceremony") was authored on 2026-05-17 specifically to defend against this convention-miss class. The lesson exists; the corresponding ceremony-script linter does not (per L-025 forward-binding: v0.2 ceremony-script linter assertion). The same gap that produced row 279's recovery supersession on the blueprint-side also let the card-side writes be missed entirely.

**Recommended operator dispatch (separate session — Cowork or Claude Code, operator's call):**

Path (a) — RE-RUN the restructure write + new supersession-re-sign ceremony. Take the in-memory restructure script at `pipeline/scripts/od_e_restructure_card.py` (the CLC-05 agent identified it at lines 174-211 as defining the intended `track_a = sbir_phase_ii` / `track_b = sbir_phase_iii` partition with broader §18.6 v1 Market-Access content inheriting to Track B), execute it against the three cards to actually produce the on-disk restructured YAML, then dispatch a new compound-LOCK row 280-282 ceremony at a new `lock_timestamp_utc` superseding rows 276/277/278. This re-pins the canonical bytes to actual disk reality.

Path (b) — REVOKE rows 276/277/278 from lock_history. Mark them with a `revoked: true` field per the (currently un-spec'd) revocation pattern, append a corrective dispatch note, and re-stage the OD-E ceremony freshly. This preserves the historical integrity of lock_history at the cost of leaving §18.6 v2 amendment in a "schema landed but no cards exercise it" state.

Path (c) — DEFER restructure to v0.2 Wave 3. Document the rows 276/277/278 as "premature supersession claims; restructure deferred to v0.2 Wave 3 in scope with the separate grant-side-credit-readiness CLC". This makes the lock_history accurate but leaves the v0.1 fleet with three half-spec'd cards.

Path (a) is the cleanest operationally; path (b) is the cleanest historically; path (c) is the cleanest scope-wise.

**Forward-binding contracts (regardless of path chosen):**
- v0.2 first-wave loader graduation: add SHA3-512 verification at load time per architecture v7.0.11 §5. The on-disk file SHA3-512 must match the `sha3_512` field of the most-recent supersession row in lock_history that names the file; otherwise `F-CARDS-SIGNATURE-INVALID` fires.
- v0.2 ceremony-script linter (L-025 forward action): assert that for any `card_cartridge_supersession` row, the on-disk file at the named path has been written with the asserted bytes BEFORE the row is appended. This closes the OD-E convention-miss class structurally.
- L-026 candidate (separate landing): "Lock_history supersession rows for card files must be paired with a disk-write-verification step that re-reads the file post-write and confirms its SHA3-512 matches the row's `sha3_512` claim BEFORE the signature is computed." Mirror of L-025 at the card layer. Operator-dispatch lesson landing per L-024/L-025 precedent.

## §5 — Cross-card patterns surfaced

### 5.1 PRP-delegation discipline (P1, cross-card)

Surfaced strongly on CLC-01 + CLC-06 + CLC-08, with adjacency-implications on every CLC card:
- CLC-01 proposed `cross_references_prp:` annotation field on `compliance_obligations` / `evidence_weights` / `common_red_flags` items to route 2 CFR 200 / Davis-Bacon / NEPA-24CFR58 live program-law from card body to PRP. Maps to active PRP roster at `pipeline/program_rule_packs/_manifest/active_prps.yaml`.
- CLC-06 Track A surfaces parallel program-law in credit underwriting (CDFI Fund standards, SBA 7(a) eligibility) that belongs in PRP — same routing pattern.
- CLC-08 surfaces USDA Community Facilities Direct Loan procedural law that belongs in PRP.
- All three correctly route to comment-block-only fallback per Wave 2 CLC-06 / CLC-08 precedent (refusal-(a) territory).

**Routing recommendation:** §18 v1.x amendment to introduce a canonical `cross_references_prp:` sub-field shape on `compliance_obligations` / `evidence_weights` / `common_red_flags` items. This is a schema delta with cross-card reach analogous to §18.6 v2. Drop in 5-line MVP first; expand at v0.2 first-wave loader graduation.

**Surfaces new PRP candidates** not yet on the active roster:
- `TILTH-PRP-BABA-IIJA` (Build America Buy America under IIJA implementing rules) — surfaced by CLC-01.
- `TILTH-PRP-CDFI-FUND-CERT` (CDFI Fund certification + underwriting standardization rules) — surfaced by CLC-06.
- `TILTH-PRP-USDA-CF` (USDA Community Facilities Direct Loan procedural law) — surfaced by CLC-08.

### 5.2 OD-A v2.4 admin_risk_register cross-CLC cell verification gap (P1, cross-card)

Multiple agents (CLC-01, CLC-02, CLC-04, CLC-08) surface the same pattern: the OD-A migration moved 60 net-new flagged terms from Wave 2 CLC card bodies into the workspace register, but **per-CLC-register cells** (the `per_clc_register: {clc_slug: AVOID|OK|EXPECTED|PREFERRED}` map) are unevenly populated. For some terms, this card's CLC slug is missing from the per_clc_register entirely; for others, the cell value is stale.

**Routing recommendation:** operator workflow item — bulk verification pass of `admin_risk_register.yaml` v2.4 per_clc_register cell coverage against all 8 CLC slugs. Not a card-body edit; not a LOCK ceremony; sidecar audit + operator-dispatched in-place register edits. Estimated effort: 1-2 hours.

### 5.3 Reviewer-culture differentiation (P1, cross-card)

CLC-02 + CLC-03 + CLC-04 + CLC-06 + CLC-07 all surface variants of the same finding: the `reviewer_profile_typical` block currently lumps disparate reviewer cultures (federal program officer vs foundation program officer vs credit committee vs blind peer review vs corporate brand team) into single descriptions. Reviewer dialect mismatches are a load-bearing denial mode (e.g., CLC-04 agent: "researchers often get rejected because they wrote NSF-style for an AFRI panel").

**Routing recommendation:** §18 v1.x amendment surface — introduce a `reviewer_culture_subtypes:` sub-field shape under `reviewer_profile_typical`, with closed-set culture enum (federal_program_officer / foundation_program_officer / credit_committee / blind_peer_review / corporate_brand_team / community_facilities_field_office / etc.). Cards then specify which subtypes their CLC engages. Drafting agents (Scribe) can then dialect-match per subtype.

### 5.4 Funder Intelligence Database (FID) downstream consumer signals (P1, cross-card)

CLC-02 (foundation strategic pivot tracking), CLC-04 (per-RFA per-priority-area Scout-fetch invariant for AFRI), CLC-05 (per-agency SBIR program drift tracking), CLC-07 (corporate foundation sunset risk) all surface findings that route NATURALLY to the FID research project at `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md`. These are NOT card-body work; they are funder-side intelligence work that informs Scout/Logician per-opportunity matching.

**Routing recommendation:** these findings strengthen the FID kickoff case. Operator should re-read the FID research project §11 (6 ops decisions awaiting operator confirm before kickoff) with these CLC-side signals in mind.

### 5.5 OD-G state-overlay amendment surface (P2, cross-card)

CLC-01 (state-level public-works variations), CLC-06 (state CDFI program variations), CLC-07 (state CCV registration completeness gap — 5 states explicit, "20+ additional states" qualitative; PA-specific rules absent) all surface state-specific knowledge that doesn't fit cleanly in the card body. The OD-G "state-overlay" amendment surface is the canonical destination per the master prompt §2 prompt body rule 11 + §G of various §0.5 amendments.

**Routing recommendation:** OD-G amendment surface remains the canonical destination. Operator-decision on PA-priority-first scope vs all-50-states-scaffold-first scope.

### 5.6 §18.16 implementation-phase mapping respected

All 8 agents correctly avoided proposing v0.2-only behavior as v0.1 card edits (no commitments to Data Collector / Report Generator integration; no proposals depending on the Funder Intelligence Database being live; no proposals depending on PRP loader graduation). v0.1-scope discipline held across the run.

### 5.7 Wave 1 vs Wave 2 prior-art depth asymmetry

CLC-03 (Wave 1 LOCKed) has by far the heaviest prior-art base (Thesis Cycle 1 + Cycle 2 + 4 OD-closures + admin_risk_register v2.4 migration origin). CLC-03 handback came in at ~485 lines — heaviest of the 8 — reflecting that depth. CLC-01 / CLC-02 / CLC-04-08 (Wave 2 LOCKed) had thinner prior-art bases; their handbacks reflect that. Pattern is appropriate and expected.

## §6 — Per-card decision-queue highlights (operator-actionable, sample)

Full decision queues live in each handback's §5. High-priority items per card:

- **CLC-01 (11 decisions):** PRP-delegation discipline annotation field shape; 5 federal/state program rubric additions (HUD 108 / FEMA HMGP / DOT SS4A / DOT Reconnecting Communities / EPA Brownfields); TILTH-PRP-BABA-IIJA roster addition.
- **CLC-02 (14 decisions):** additionality / theory-of-change / proximate leadership admin_risk_register v2.4 candidates; PRI compliance framework scope (v0.1 vs v0.2 Wave 3); reviewer-bench examples sub-field §18 v1.x amendment graduation.
- **CLC-03 (18 decisions):** capacity-vs-program distinguishability red flag + criterion; federal-vs-foundation-vs-TA-provider reviewer subtypes; cost-recovery glide-path discipline; recommendation to bundle CLC-03 + CIC-01 re-sign per Wave 1 paired-LOCK precedent.
- **CLC-04 (21 decisions):** SARE practitioner-readable-summary; AFRI per-RFA Scout invariant; WWC evidence-tier alignment; NIH inclusion-plan + clinical-trial separate-scoring; CBPR + CARE Principles evidence_weights.
- **CLC-05 (10 decisions):** ALL contingent on §18.6 v2 restructure landing on disk (see §4 incident); track_a / track_b YAML-path proposals cannot land otherwise.
- **CLC-06 (18 decisions, 3 v0.2 Wave 3 backlog items):** ALL contingent on §18.6 v2 restructure landing on disk; Track A debt underwriting refinements + Track B carve-out preservation; v0.2 Wave 3 CLC slug naming (`grant_side_credit_readiness` vs `capital_readiness_grant`).
- **CLC-07 (17 decisions):** §18.6 v2 restructure dependency + OD-C row 272 FIX-IN-PLACE re-application (the two pre-existing slug literals at lines 97 + 307 regress OD-C scan); cross-track funder-identity-resolution red flag; state CCV PA-specific rules.
- **CLC-08 (11 decisions):** common_funders_observed 13-entry roster; replacement-reserve 5-15% triangulation; per-CLC-cell verification for 9 migrated admin_risk_register terms; 2024 OMB Uniform Guidance procurement-threshold currency propagation.

## §7 — Discipline checklist (this aggregate)

- Sidecar-only writes (✓ — 8 per-card handbacks + this aggregate in `docs/`; no LOCKed files touched).
- No git operations (✓).
- No edits to `pipeline/cards/` / `pipeline/blueprint/` / `pipeline/architecture/` / `pipeline/logician/` / `pipeline/engineering/` (✓).
- All 14 cards verified for `draft_status` (✓ — all read "signed").
- All 8 CLC cards verified for top-level `track_a:` / `track_b:` / `_partition_provenance:` presence (✓ — confirmed 0/8 present; surfaces P0 incident).
- All 8 handback Patch Plans are sidecar-only (✓).
- Master prompt §1 vocabulary anchor respected throughout (✓ — "Customer Identity Cards"; display names not slugs in non-exempt prose).

## §8 — Recommended next dispatches (operator-prioritized)

1. **HIGH — Resolve §4 P0 incident.** Operator picks path (a) / (b) / (c) from §4 above. Until resolved, CLC-05 / CLC-06 / CLC-07 handbacks cannot land their §4 proposed YAML paths.
2. **MEDIUM — Master prompt §5 stale-claim correction.** 5-minute sidecar edit per §3 above. Unblocks future researcher dispatches from chasing a non-existent gap.
3. **MEDIUM — PRP-delegation `cross_references_prp:` schema delta** (§5.1). §18 v1.x amendment surface. Strong cross-card leverage.
4. **MEDIUM — admin_risk_register v2.4 per-CLC-cell verification pass** (§5.2). Operator workflow item, not a LOCK ceremony.
5. **MEDIUM — `reviewer_culture_subtypes:` sub-field shape** (§5.3). §18 v1.x amendment surface. Strong cross-card leverage on reviewer-dialect matching.
6. **MEDIUM — FID research project re-read with CLC-side signals folded in** (§5.4). Strengthens 6 ops decisions awaiting operator confirm at FID §11.
7. **LOW — L-026 candidate landing** (§4 forward-binding contract). Mirror of L-025 at the card layer. Lesson-only; no LOCK ceremony.
8. **LOW — OD-G state-overlay amendment scoping** (§5.5). Operator-decision on PA-priority-first vs scaffold-first.

The natural NEXT batch dispatch is the Phase 7 cross-card synthesis combining the 14 individual handbacks (6 CIC + 8 CLC) into a unified cards-ceremony Patch Plan for operator review. Per the prior CIC run's recommendation, that should land after this CLC run's deliverables are reviewed.

---

**Aggregate one-line summary:**

Cards: 8 CLC handbacks landed at `docs/clc_<slug>_research_handback_2026-05-17.md`.
Research hours actual total: ~12 (parallel dispatch via 8 sub-agents; ~80 min wall-clock).
Findings total: 213 — 6 P0 (3 structural-incident-shared across CLC-05/06/07 + 3 framing variants) · 100 P1 · 107 P2.
Decision queue total: 120 operator approvals.
Coupling-discipline regression: 2 pre-existing findings on CLC-07 (regress OD-C row 272 FIX-IN-PLACE; bundled into CLC-07 Patch Plan §8.1).
Lifecycle gap: **NONE** — master prompt §5 universal claim is STALE; all 14 cards already read `draft_status: "signed"` on disk per Wave 2 LOCK lifecycle promotion.
Structural-integrity incident surfaced: **§18.6 v2 dual-track restructure NEVER LANDED ON DISK** for CLC-05/06/07; 3 signed lock_history rows (276/277/278) unverifiable against on-disk bytes; operator path (a)/(b)/(c) per §4.
Review readiness: 5 of 8 cards READY · 2 of 8 DEFER pending §4 P0 resolution · 1 of 8 READY-with-structural-dependency.
