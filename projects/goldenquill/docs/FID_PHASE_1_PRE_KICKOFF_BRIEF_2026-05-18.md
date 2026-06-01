# FID Phase 1 Pre-Kickoff Brief — 2026-05-18

**Authored:** 2026-05-18 (Cowork session, operator co-authoring)
**Authority:** `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §11 (original six operational decisions) + this session's scope expansion (reviewer-types-first sprint; 16-type roster; hybrid scale-as-field taxonomy)
**Companion (substantive prior work):** `pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md`
**Companion (this session's amendment):** `pipeline/planning/fid_phase_1_dispatch_plan_amendment_2026-05-18.md` (lives in `planning/` because `pipeline/handoffs/` is gitignored — handoff prompts contain operator + client context and stay local)
**Status:** AWAITING OPERATOR CONFIRM. No Week 1 work fires until Josh signs off on the decisions below.

---

## Why this exists

The FID Phase 1 plan (`funder_intelligence_database_research_project_2026-05-16.md` §9.1) and the follow-on dispatch plan (`fid_phase_1_dispatch_plan_2026-05-16.md`) were authored by Cowork in Synthesizer mode on 2026-05-16. Both pre-staged Phase 1 down to a Monday 2026-05-18 anchor — but neither carried operator daylight sign-off on the six §11 operational decisions.

During the 2026-05-18 session that produced this brief, operator surfaced two real gaps in the 2026-05-16 plan:

1. The **reviewer-type taxonomy was inconsistent** (only `state-arts-council-panelist` carried a scale marker in its name) and **missing the local layer entirely** (no community-foundation-program-officer, no redevelopment-authority-panelist, no conservation-district-panel, no municipal-grant-committee, no community-board-panel).
2. The original Phase-1 exemplar-pair scope (~4 reviewer types) was **too narrow for the reviewer-type artifact family** — reviewer types are the most reusable artifact family and the least NOFO-cycle-bound, making them the natural sprint target.

Operator resolved the taxonomy gap as **hybrid C** (decision-shape primary names + geographic scale as in-artifact field) and resolved the scope question as **reviewer-types-first sprint covering all 16 types**. This brief is the operator daylight record of both decisions plus the original six.

## What Phase 1 (revised) is

**Sprint shape:** reviewer-types-first. All 16 reviewer-type artifacts authored, corpus-assembled, structured-extracted, single-cycle-cross-family-audited in ~6-7 weeks. Methodology v1.0 doc + reviewer-heuristics LOCK at sprint close. Exemplar-pair funder + program artifacts (RBDG + companions) run in parallel as the methodology-anchor against a different artifact family (program-shape) so schema gets debugged across two shapes simultaneously.

**Why reviewer-types-first vs original exemplar-pair-first:**

- **Most reusable artifact family.** One reviewer-type artifact covers many funders. Doing all 16 first means downstream funder + program work has them ready as references.
- **Least NOFO-cycle-bound.** No FY26 deadline pressure on reviewer types. Funder + program artifacts are cycle-bound; reviewer types aren't.
- **Heuristics seed already partial.** `skills/scribe-ghostwriter/references/reviewer_heuristics.md` landed 2026-05-16 — partial Pillar-2 corpus already exists for several types.
- **Parallelizable Pillar-1.** Charter authoring is the operator-time bottleneck. Batching all 16 charters in one operator-week is feasible (~9-14 hrs Josh in Week 1).

**What Phase 1 (revised) produces:**

- 16 reviewer-type artifacts at `lifecycle.cross_family_thesis_status: passed` + `lifecycle.draft_status: audited`.
- 1+ companion exemplar program artifact (USDA-RD-RBDG-FY26 default) at the same lifecycle state — methodology-anchor across artifact-family shapes.
- Methodology v1.0 doc at `pipeline/funder_intelligence/_methodology/v1.0.md` (field-test section marked `DORMANT — pending grant drafting reactivation` per 2026-05-16 §0.5).
- Compound paired-commit `F-FID-*` failure-code family LOCK (8 fail-closed gates per planning doc §2.2). Operator-Ed25519-signed; registered in `lock_history.v1.jsonl`.
- Card smart-pointer migration on cards that reference reviewer types (mechanical, lifecycle untouched; ~6-8 CIC + CLC cards touched). Specifically, CLC cards gain `commonly_reviewed_by: [reviewer_type_id, ...]` and reviewer-type artifacts get `commonly_engaged_in_clcs: [clc_id, ...]`.

**Active scope correction (inherited from 2026-05-16):** Pillar 4 (field-test calibration via Tracks A/B/C) is DORMANT — no grant drafting currently active. All three tracks require Tilth to generate competing drafts. Reactivation runs as a separate dispatch when grant drafting reactivates.

**Phase 2 horizon (out of Phase 1 scope, named for clarity):** Remaining funder + program + cascade artifacts for the food_systems × operating_capacity exemplar pair (8 funders + 5 more programs + 3 cascades = 16 more artifacts). Phase 2 is a faster sprint because reviewer-type pointers are pre-built.

## The reviewer-type roster (operator-locked this session — hybrid C)

Decision-shape primary names; geographic scale as in-artifact `scale:` field with `scale_variants:` notes for federal/state/county/local differences. Sixteen types:

| # | Type | Single-CLC or spans many | Notes |
|---|------|-------------------------|-------|
| 1 | federal-program-officer | Spans 6 of 8 CLCs | USDA RD / NIFA / AMS, EPA, EDA, etc. |
| 2 | foundation-program-officer | Catalytic Change, Operating Capacity, Research | National / regional |
| 3 | **community-foundation-program-officer** *(NEW)* | Operating Capacity, Catalytic Change, Shared Assets | Place-based: Heinz, Pittsburgh Foundation, county community foundations |
| 4 | peer-reviewer-academic | Research & Evidence | SARE / AFRI / NIH-style scientific peer review |
| 5 | state-program-officer | Public Purpose, Market Access, Operating Capacity | PA Dept of Ag, PA DCED, state-agency-led |
| 6 | sba-7a-credit-committee | Credit & Underwriting | Single-CLC, committee shape |
| 7 | cdfi-underwriter | Credit & Underwriting | Single-CLC, individual underwriter shape |
| 8 | community-peer-panelist *(RENAMED from state-arts-council-panelist)* | Catalytic Change, Sponsorship, Public Purpose-adjacent | State + county + city arts councils + similar peer-merit citizen panels |
| 9 | irb-human-subjects-reviewer | Research & Evidence | Regulatory gate within CLC, not a funder per se |
| 10 | marketing-manager-sponsorship-reviewer | Sponsorship & Corporate Support | Single-CLC, commercial shape |
| 11 | cooperative-board-peer-reviewer | Shared Assets, Operating Capacity | NCBA-CLUSA, member-driven co-op intermediary review |
| 12 | vapg-style-merit-panel-reviewer | Market Access (within USDA-AMS-VAPG) | Alumni-pool merit scorers, distinct from federal program officers |
| 13 | **redevelopment-authority-panelist** *(NEW)* | Public Purpose & Works, Shared Assets | Federal EDA + state DCED + county redev authorities + URA Pittsburgh; land-use + capital + public-benefit review |
| 14 | **conservation-district-panel** *(NEW)* | Public Purpose & Works, Research | County conservation districts — PA-specific high-relevance for ag work |
| 15 | **municipal-grant-committee** *(NEW)* | Public Purpose, Operating Capacity, Catalytic Change | Township / borough / city small-grant review (Main Street, neighborhood reinvestment) |
| 16 | **community-board-panel** *(NEW)* | Public Purpose, Shared Assets, Operating Capacity | Citizen-advisory beyond arts: planning grants, brownfield review, neighborhood-CDC grants |

Five NEW types added this session; one RENAMED for taxonomy consistency. Net add: ~5 types beyond the 2026-05-16 planning doc.

## The decisions awaiting confirm

### Decision 1: Phase 1 start anchor date

- **Question:** When does Week 1 (charter authoring sprint) begin?
- **Options:** (a) Monday 2026-05-18 (today); (b) push to next operator-working-week (2026-05-25); (c) push further.
- **Recommended default:** (a) Monday 2026-05-18. Rationale: FID scaffold on disk; publisher pubkey pinned; momentum is the asset; further delay returns no calibration signal (Pillar 4 dormant).
- **Override impact:** Push to 2026-05-25 = ~7 day slip; F-FID-* LOCK ceremony moves correspondingly. No structural rework.

### Decision 2: Track A (operator-win replay) calibration

- **Question:** Recruit 2 external reviewers for deep-vs-shallow blind comparison on Josh's 3 confirmed 2026 wins now, or defer?
- **Options:** (a) Recruit now; (b) Cowork drafts recruitment ask; (c) **DORMANT** through Phase 1.
- **Recommended default:** (c) DORMANT through Phase 1. Pillar 4 calibration requires draft generation; no grant drafting active. ~$1,800 cash spend with zero return until drafts exist.
- **Override impact:** Pre-recruitment hedges against future reviewer-availability slippage; adds ~5 operator-hrs Phase 1 outreach.

### Decision 3: Track B (CDFI / regional-foundation partner pilot) calibration

- **Question:** Name 1-2 partner candidates for 5-8 in-pipeline applicant pilot, or defer to Phase 2?
- **Options:** (a) Operator names partners; (b) Cowork drafts partner-outreach packet; (c) **DEFER to Phase 2**.
- **Recommended default:** (c) DEFER. Slowest signal channel (3-9 mo funder turnaround); planning doc §5.2 explicitly marks Track B as optional-for-exemplar / required-for-scale-out.
- **Override impact:** If Josh has a ready partner, parallel partner-discovery is minimal Phase-1 schedule impact; risk = partner expectations against DORMANT pilot timeline.

### Decision 4: Track C (synthetic blinded panel) calibration

- **Question:** Confirm ~$6K cash budget for 10 fictionalized pairs × 3 paid reviewers × $200/review, or defer?
- **Options:** (a) Confirm $6K; (b) Stagger (5 pairs Phase 1, 5 Phase 2 = $3K Phase 1 spend); (c) **DEFER to grant-drafting reactivation**; (d) Reduce reviewer/pair count.
- **Recommended default:** (c) DEFER. Same rationale: Pillar 4 DORMANT; no drafts to compare → no panel needed.
- **Override impact:** (b) Stagger buys methodology-debugging at small-N before full $6K commits; ~25 operator-hrs added for pair construction; signal weak at N=5.

### Decision 5: Operator publisher Ed25519 key for FID artifacts

- **Question:** Reuse Cards publisher key, or dedicated FID publisher key?
- **Options:** (a) Reuse Cards publisher key; (b) Dedicated FID publisher key.
- **Recommended default:** (b) Dedicated FID publisher key. Already PINNED 2026-05-16 at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml` (pubkey `634441fd…81c37b8f`). Operator pastes signing seed in-session per Cards Wave 1.1 precedent. Matches §17 v1 WPFA + v7.0.7 §6.1 separation-of-concerns precedent.
- **Override impact:** (a) Single-key simplicity; revoke pinned FID pubkey + update FID README signature section + lose per-publisher rotation independence.

### Decision 6: First FID artifact to dispatch (methodology anchor)

- **Question:** Which artifact does the methodology test against first?
- **Options:** (a) `USDA-RD-RBDG-FY26` program file alone; (b) RBDG paired with USDA-RD funder + 2-CFR-200-UG cascade + federal-program-officer reviewer (4 artifacts; ~30% time savings via shared corpus); (c) Different first artifact.
- **Recommended default:** (a) `USDA-RD-RBDG-FY26` alone Day 1, with operator opt-in to (b) at Monday kick-off. Conservative methodology-debugging signal at minimum coupling; pair-of-four opt-in remains live.
- **Override impact:** (b) ends Week 1 with ~15 charters signed vs ~12 but muddier methodology-debugging signal; (c) Day 1 starts with whatever new artifact's pre-research demands.

### Decision 7: Sprint scope — reviewer-types-first vs. full-21-artifacts vs. other

- **Question:** What's the scope of "all done ASAP"?
- **Options:** (a) Reviewer-types-only (16 reviewer-type artifacts; ~6-7 weeks; ~40-50 hrs Josh); (b) Reviewer-types-first + RBDG-companion methodology-anchor (16 + 1-4 program/funder/cascade artifacts; ~6-7 weeks; ~45-55 hrs Josh); (c) Full Phase-1 21-artifact sprint compressed (8 funders + 6 programs + 3 cascades + 16 reviewer types = 33 artifacts; ~9-10 weeks; ~70-90 hrs Josh); (d) Original 2026-05-16 8-week 21-artifact Phase-1 + reviewer-types deferred (slowest reviewer-type return).
- **Recommended default:** (b) Reviewer-types-first + RBDG methodology-anchor. Rationale: reviewer types are most reusable + least cycle-bound (per "What Phase 1 (revised) is" section); RBDG runs parallel to debug schema across two artifact-family shapes simultaneously, mitigating the exemplar-pair-discipline trade-off.
- **Override impact:** (a) Drops methodology-anchor; risk = reviewer-types-only schema doesn't surface bugs that program-artifacts would. (c) Full sprint locks ~9-10 weeks + ~70-90 hrs Josh; doable but heavier operator commitment. (d) Slowest payback on the most reusable artifact family.

### Decision 8: Reviewer-type roster lock (16 types, hybrid C)

- **Question:** Confirm the 16-type roster (above) with hybrid C taxonomy (decision-shape primary names + scale-as-field)?
- **Options:** (a) Confirm 16 + hybrid C as listed; (b) Confirm 16 but use Option A (strip scale entirely from all names, fold scale fully into in-artifact field); (c) Confirm 16 but use Option B (add explicit local-suffix variant types — bloats to ~18-20); (d) Drop one or more of the 5 NEW types; (e) Add additional types operator names.
- **Recommended default:** (a) Confirm 16 + hybrid C. Already in-session-agreed; matches operator's "C works" call. Decision-shape primary keeps semantic clarity; in-artifact scale-variants field handles federal/state/county/local differences without name explosion.
- **Override impact:** (b) Cleanest taxonomy but loses scale-cue at type-name level; reviewers reading Scribe output get less geographic hint. (c) Bloated roster; ~3-4 more charters in Week 1. (d) Reduces sprint scope by 1-3 artifacts; ~3-9 fewer hrs Josh.

### Decision 9: NCBA-CLUSA review mapping + VAPG sub-panel split

- **Question:** NCBA-CLUSA grant review uses cooperative-board-peer-reviewer (member-driven), not foundation-program-officer. And USDA-AMS-VAPG has BOTH a federal-program-officer admin review AND a VAPG-alumni merit-panel scorer pool. Confirm both splits?
- **Options:** (a) Confirm both splits (cooperative-board-peer-reviewer as separate type + vapg-style-merit-panel-reviewer as separate type — already in the 16); (b) Fold NCBA-CLUSA review under foundation-program-officer (lossy; loses cooperative-member-driven nuance); (c) Fold VAPG merit-panel into federal-program-officer (lossy; loses alumni-pool scoring nuance); (d) Fold both.
- **Recommended default:** (a) Confirm both splits. Already baked into the 16-type roster. The lossy framings would have Scribe write credit-committee language indistinguishable across SBA committee vs CDFI underwriter — different decision shapes, same CLC, different framing impact.
- **Override impact:** (b) or (c) reduces roster by 1 each; saves ~3-5 hrs Josh charter work each; trades schema clarity for sprint speed.

## The 5-step sprint process (assuming Decisions 1, 7, 8 confirmed at default)

**Step 1 — Universe LOCK (Day 1, ~2 hrs Josh).** Roster reviewed, finalized, operator-Ed25519-signed as `pipeline/funder_intelligence/reviewer_heuristics/_universe.signed.yaml`. Scope contract; no scope creep without re-signing.

**Step 2 — Charter sprint (Week 1, ~9-14 hrs Josh).** Cowork drafts all 16 Depth Charters in batches of 4-5 against the existing template. Josh reviews and signs in single sessions per batch. RBDG program charter signed parallel (methodology-anchor artifact). Total signed charters: 17.

**Step 3 — Corpus assembly (Weeks 2-3, ~10-15 hrs Josh).** LLM-bulk fetching + operator spot-check, parallel across all 17 artifacts. Reviewer-type corpus is harder than funder corpus (FOIA debrief letters where available, reviewer-training materials, operator + collaborator interview transcripts at Tier-2, public reviewer-debrief examples). Manifest-sign each artifact's corpus at closure.

**Step 4 — Extraction sprint (Weeks 4-6, ~10-15 hrs Josh).** Per-artifact dispatch via cross-family openclaw bridge. Author=Anthropic, Editor=`groq/llama-3.3-70b-versatile`, Judge=`google/gemini-2.5-pro`, Red Team=`groq/openai/gpt-oss-120b`. Single-cycle L-005 audit per artifact. Gateway-saturation cap = 2 artifacts × 3 seats = 6 simultaneous calls (Wave-2 lesson). 17 artifacts ÷ 2 = ~9 batches over ~12 working days at ~1 batch/day.

**Step 5 — Methodology LOCK (Week 7, ~4-6 hrs Josh).** Retrospective doc + reviewer-heuristics methodology v1.0 + F-FID-* family LOCK (compound paired-commit, 8 gates) + smart-pointer migration on cards that reference reviewer types (mechanical, lifecycle untouched).

**Sprint totals:** 6-7 weeks, ~45-55 hrs Josh, ~700-1000 hrs compute.

## Decision-independent scaffold (already on disk + this commit)

| Asset | Path | Status |
|---|---|---|
| FID lattice root + family dirs | `pipeline/funder_intelligence/{funders,programs,compliance_cascades,reviewer_heuristics,_research_corpus,_schema,_templates,_methodology,_kpi,_calibration,lessons_seed}/` | On disk (2026-05-16) |
| Lattice README | `pipeline/funder_intelligence/README.md` | On disk (2026-05-16) |
| Depth Charter template | `pipeline/funder_intelligence/_templates/depth_charter_template.md` | On disk (2026-05-16) |
| Publisher pubkey (pinned) | `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml` | PINNED 2026-05-16 |
| Publisher pubkey register | `vault_shared/funder_intelligence/register.yaml` | On disk (2026-05-16) |
| Track A/B/C directory stubs | `pipeline/funder_intelligence/_calibration/track_{a,b,c}/.gitkeep` | On disk (DORMANT per Decisions 2/3/4) |
| Lessons-seed dir | `pipeline/funder_intelligence/lessons_seed/` | On disk (2026-05-16) |
| Original Phase 1 dispatch plan | `pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md` | On disk (2026-05-16) |
| Original RBDG dispatch packet | `pipeline/handoffs/fid_exemplar_usda_rd_rbdg_fy26_dispatch_2026-05-16.md` | On disk (2026-05-16) |
| **Dispatch plan amendment (this session)** | `pipeline/planning/fid_phase_1_dispatch_plan_amendment_2026-05-18.md` | **NEW this commit** |
| Phase 1 weekly tracker | `pipeline/funder_intelligence/_methodology/phase_1_week_tracker.md` | NEW this commit (empty-state tracker; no decision-dependence) |

Nothing new in this commit is decision-dependent. The brief surfaces; the amendment doc documents the scope shift; the tracker is an empty append-only ledger. The reviewer-heuristics universe-lock file (`_universe.signed.yaml`) is NOT pre-built — it's Step 1 of the sprint and requires operator-Ed25519 signing.

## Sign-off path

1. Josh reviews this brief + the amendment doc.
2. Josh confirms or overrides each of the nine decisions in one comment (PR thread). Suggested format:

   ```
   D1 (start date): confirm / override → <new value>
   D2 (Track A): confirm / override → <new value>
   D3 (Track B): confirm / override → <new value>
   D4 (Track C): confirm / override → <new value>
   D5 (publisher key): confirm / override → <new value>
   D6 (first artifact): confirm / override → <new value>
   D7 (sprint scope): confirm / override → <new value>
   D8 (reviewer roster): confirm / override → <new value>
   D9 (NCBA-CLUSA + VAPG splits): confirm / override → <new value>
   ```

3. Cowork updates the amendment doc §0 + the dispatch plan §0 if any default is overridden (paired-commit; signature re-issued where applicable).
4. Phase 1 (revised) Day-1 work fires — Step 1 Universe LOCK + Step 2 first charter batch per Decision 6 outcome.

No code changes, no card migration, no F-FID-* LOCK ceremony are touched by this brief or the amendment. Paperwork-and-daylight; substance is the prior 2026-05-16 dispatch plan + this session's scope expansion.

---

## Cross-references

- Planning doc: `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` (§11 six original decisions; §9.1 Phase-1 timeline; §3 four-pillar methodology; §2 FID lattice architecture; §4.2 original 21-artifact exemplar-pair scope)
- Original dispatch plan: `pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md`
- This session's amendment: `pipeline/planning/fid_phase_1_dispatch_plan_amendment_2026-05-18.md`
- RBDG dispatch packet: `pipeline/handoffs/fid_exemplar_usda_rd_rbdg_fy26_dispatch_2026-05-16.md` (Decision-6 default's Day-1 work)
- FID lattice: `pipeline/funder_intelligence/README.md` (decision-independent scaffold on disk)
- Reviewer-heuristics seed: `skills/scribe-ghostwriter/references/reviewer_heuristics.md` (partial Pillar-2 corpus for several types)
- Funder-as-specimen thesis: `pipeline/planning/funder_as_specimen_integration_2026-05-16.md`
- WPFA Coefficient Registry signed-asset precedent: `pipeline/blueprint/v0.1/section_17_wpfa_v1.md`
- Architecture v7.0.7 white-glove Classification Review: `pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md`
- Architecture v7.0.10 three-posture routing (Tier-1/2/3 inheritance): `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md`
- Five Operating Laws: `/SOUL.md` (Law 1 RFA-is-truth; Law 5 applicant-brings-substance)
- AGENTS.md cross-family bridge pattern: Pillar-3 audit transport
