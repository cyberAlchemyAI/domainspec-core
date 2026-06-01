# FID Phase 1 Dispatch Plan — Amendment 2026-05-18

**Authored:** 2026-05-18 (Cowork session, operator co-authoring)
**Amends:** `pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md` (original 2026-05-16 Synthesizer-mode plan; lives in `handoffs/` which is gitignored — handoff prompts contain operator + client context and stay local. This amendment lives in `planning/` so the scope-shift record is tracked.)
**Authority:** operator directive 2026-05-18 ("lets get a process for getting them all done ASAP sorted out, shall we?"); operator confirmation 2026-05-18 ("alllll of themm. C works."); operator confirmation 2026-05-18 ("get it" → update brief + dispatch plan + push PR)
**Companion (operator-facing daylight record):** `docs/FID_PHASE_1_PRE_KICKOFF_BRIEF_2026-05-18.md`
**Status:** DRAFT — awaiting operator sign-off via PR thread on the nine pre-kickoff decisions. No Step 1 work fires until daylight confirmation.

> **Read pipeline/SESSION_BOOTSTRAP.md for project orientation before continuing.**

---

## §0 — What this amendment changes

The 2026-05-16 dispatch plan staged Phase 1 as an **exemplar-pair-first** 8-week sequence (21 artifacts across CIC-01 food_systems × CLC-03 operating_capacity; 4 funders + 6 programs + 3 cascades + 4 reviewer types after the §0.5 active-scope correction). The 2026-05-18 session surfaced two real gaps in that plan:

1. **Reviewer-type taxonomy inconsistency + missing local layer.** Original plan had only 4 reviewer types (federal-program-officer · foundation-program-officer · peer-reviewer-academic · state-program-officer). Only `state-arts-council-panelist` carried a scale marker in its name (inconsistency with the rest of decision-shape-named taxonomy). Local-layer review (community foundations, redevelopment authorities, conservation districts, municipal committees, community boards) was entirely absent.
2. **Sprint-target mismatch.** Reviewer types are the most reusable artifact family (one type covers many funders) and the least NOFO-cycle-bound (no FY26 deadline pressure). Original exemplar-pair-first scoping deferred reviewer-types-at-scale to Phase 2, leaving the most reusable artifact family for the slowest payback.

**This amendment resolves both.** Phase 1 (revised) = **reviewer-types-first sprint covering all 16 types** under **hybrid C taxonomy** (decision-shape primary names + geographic scale as in-artifact `scale:` field with `scale_variants:` notes), with **USDA-RD-RBDG-FY26 program artifact running parallel** as the methodology-anchor across artifact-family shapes.

The original 2026-05-16 dispatch plan is preserved as the historical record. This amendment is the LIVE plan once operator signs off via the brief's PR thread.

## §0.5 — Inherited from 2026-05-16 (unchanged by this amendment)

| Item | Source | Status |
|---|---|---|
| Active scope correction (Pillar 4 calibration DORMANT) | 2026-05-16 dispatch plan §0.5 | UNCHANGED — calibration tracks A/B/C remain DORMANT |
| Publisher Ed25519 key (dedicated FID publisher key; pubkey `634441fd…81c37b8f` pinned at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`) | 2026-05-16 dispatch plan §0 | UNCHANGED — operator-confirms via brief Decision 5 |
| Day-1 first artifact (USDA-RD-RBDG-FY26 default; pair-of-four opt-in at Monday kick-off) | 2026-05-16 dispatch plan §0 + §2 Week 1 | UNCHANGED — operator-confirms via brief Decision 6; now ALSO serves as methodology-anchor across artifact-family shapes |
| Phase 1 start anchor (Monday 2026-05-18) | 2026-05-16 dispatch plan §0 | UNCHANGED — operator-confirms via brief Decision 1 |
| F-FID-* family LOCK at sprint close (paired-commit with methodology v1.0) | 2026-05-16 dispatch plan §1 | UNCHANGED — week 7 of sprint |
| Cross-family audit roster (Editor=meta, Judge=google, Red Team=openai-oss, Author=Anthropic) | 2026-05-16 dispatch plan §3 | UNCHANGED |
| Gateway-saturation cap (2 artifacts × 3 seats = 6 simultaneous calls + seat-stagger) | 2026-05-16 dispatch plan §3 | UNCHANGED |
| L-005 single-cycle audit per artifact, two-cycle maximum, fix-in-place at LOCK | 2026-05-16 dispatch plan §3 | UNCHANGED |
| CycleReceipt → Lessons Memory feedback loop | 2026-05-16 dispatch plan §5 | UNCHANGED |

## §1 — Revised reviewer-type roster (16 types; hybrid C; operator-locked this session)

Per brief Decision 8. Decision-shape primary names; scale handled via in-artifact `scale:` field with `scale_variants:` for federal/state/county/local differences.

| # | artifact_id | CLC clustering | Status |
|---|-------------|----------------|--------|
| 1 | `federal-program-officer` | Spans 6 of 8 CLCs (Public Purpose, Catalytic Change, Operating Capacity, Research, Market Access, Shared Assets) | Inherited from 2026-05-16 plan |
| 2 | `foundation-program-officer` | Catalytic Change, Operating Capacity, Research | Inherited from 2026-05-16 plan |
| 3 | `community-foundation-program-officer` | Operating Capacity, Catalytic Change, Shared Assets | **NEW (2026-05-18)** — place-based foundations split from national/regional |
| 4 | `peer-reviewer-academic` | Research & Evidence | Inherited from 2026-05-16 plan |
| 5 | `state-program-officer` | Public Purpose, Market Access, Operating Capacity | Inherited from 2026-05-16 plan |
| 6 | `sba-7a-credit-committee` | Credit & Underwriting (single-CLC, committee shape) | New for sprint scope |
| 7 | `cdfi-underwriter` | Credit & Underwriting (single-CLC, individual underwriter shape) | New for sprint scope |
| 8 | `community-peer-panelist` | Catalytic Change, Sponsorship, Public Purpose-adjacent | **RENAMED (2026-05-18)** from `state-arts-council-panelist` for taxonomy consistency; covers state + county + city arts councils + similar peer-merit citizen panels via `scale_variants:` |
| 9 | `irb-human-subjects-reviewer` | Research & Evidence (regulatory gate within CLC) | New for sprint scope |
| 10 | `marketing-manager-sponsorship-reviewer` | Sponsorship & Corporate Support (single-CLC) | New for sprint scope |
| 11 | `cooperative-board-peer-reviewer` | Shared Assets, Operating Capacity | **NEW (2026-05-18)** — NCBA-CLUSA + co-op intermediary member-driven review; resolves NCBA-CLUSA mapping gap |
| 12 | `vapg-style-merit-panel-reviewer` | Market Access (within USDA-AMS-VAPG) | **NEW (2026-05-18)** — VAPG alumni-pool merit scorers distinct from federal program officers |
| 13 | `redevelopment-authority-panelist` | Public Purpose & Works, Shared Assets | **NEW (2026-05-18)** — federal EDA + state DCED + county redev + URA Pittsburgh; capital + land-use + public-benefit review |
| 14 | `conservation-district-panel` | Public Purpose & Works, Research | **NEW (2026-05-18)** — county-level; PA-specific high-relevance for urban-ag, brownfield, ag-easement |
| 15 | `municipal-grant-committee` | Public Purpose, Operating Capacity, Catalytic Change | **NEW (2026-05-18)** — township / borough / city small-grant review (Main Street, neighborhood reinvestment) |
| 16 | `community-board-panel` | Public Purpose, Shared Assets, Operating Capacity | **NEW (2026-05-18)** — citizen-advisory beyond arts (planning, brownfield, neighborhood-CDC grants) |

Six new (5 NEW + 1 RENAMED). Eleven inherited or pre-scope. Net add over 2026-05-16 plan: ~12 reviewer types (which had 4 in active Phase-1 scope).

**Universe LOCK file:** `pipeline/funder_intelligence/reviewer_heuristics/_universe.signed.yaml` — operator-Ed25519-signed at Step 1 Day 1; the scope contract for the sprint.

## §2 — Sprint timeline (7 weeks)

### Step 1 — Universe LOCK (Day 1 = Monday 2026-05-18 if Decision 1 confirms default)

**Operator-time: ~2 hrs.**

- Cowork drafts `_universe.signed.yaml` containing the 16-type roster from §1 + cross-references to CLC + CIC cards + scale-variants schema.
- Operator reviews, finalizes (drop / add / adjust), Ed25519-signs in-session against pinned FID publisher pubkey.
- Universe lock = scope contract; any subsequent scope creep requires re-signed universe file.

### Step 2 — Charter sprint (Week 1: 2026-05-18 → 2026-05-22 if Decision 1 confirms default)

**Operator-time: ~9-14 hrs across the week.**

- Cowork drafts all 16 reviewer-type Depth Charters in batches of 4-5 against `pipeline/funder_intelligence/_templates/depth_charter_template.md`.
- Day-1 batch (4 charters): federal-program-officer + foundation-program-officer + peer-reviewer-academic + state-program-officer. Operator signs in single session.
- Days 2-3 batch (5-6 charters): community-foundation-program-officer + community-peer-panelist + cooperative-board-peer-reviewer + vapg-style-merit-panel-reviewer + cdfi-underwriter (+ sba-7a-credit-committee if time).
- Days 4-5 batch (5-7 charters): redevelopment-authority-panelist + conservation-district-panel + municipal-grant-committee + community-board-panel + irb-human-subjects-reviewer + marketing-manager-sponsorship-reviewer (+ sba-7a-credit-committee if not done Days 2-3).
- Parallel: USDA-RD-RBDG-FY26 program charter (methodology-anchor artifact) signed during Days 1-2 alongside reviewer charters. Per brief Decision 6 default RBDG-alone; opt-in to pair-of-four (RBDG + USDA-RD funder + 2-CFR-200-UG cascade + federal-program-officer reviewer) at Monday kick-off.

Week 1 end-state: 17 charters signed (16 reviewer types + 1-4 program/funder/cascade per Decision 6 outcome).

### Step 3 — Corpus assembly (Weeks 2-3: 2026-05-25 → 2026-06-05)

**Operator-time: ~10-15 hrs across 2 weeks.**

- LLM-bulk fetching across all 17 artifacts in parallel. Reviewer-type corpus shape differs from funder/program corpus:
  - **For reviewer types:** FOIA debrief letters where available; published reviewer-training materials (federal: reviewer-orientation slides, agency reviewer-recruitment materials; foundation: published RFP-process pages, IRS Form 990-PF expense narratives that reference review committees; cooperative: NCBA-CLUSA member-review-committee operating procedures); operator + collaborator interview transcripts (Tier-2 default); public reviewer-debrief examples (post-decision applicant write-ups, blog posts by former reviewers).
  - **For RBDG (methodology-anchor):** NOFO + RFA + previous-year award database extracts + published rubric (if FOIA-returned or NOFO-disclosed) + agency program page.
- Reviewer-heuristics seed at `skills/scribe-ghostwriter/references/reviewer_heuristics.md` (2026-05-16 landing) feeds partial Pillar-2 corpus for ~4-6 of the 16 types.
- Operator spot-check on each artifact's corpus before Pillar-2 closure. Manifest-sign each artifact's manifest at closure.

Week 3 end-state: 17 artifacts at Pillar-2 manifest signed. Estimated corpus volume: ~60-120 files total (lighter than funder/program corpus per artifact; reviewer-types are more interpretive than rubric-extractive).

### Step 4 — Extraction sprint (Weeks 4-6: 2026-06-08 → 2026-06-26)

**Operator-time: ~10-15 hrs across 3 weeks.**

Per-artifact dispatch via cross-family openclaw bridge per AGENTS.md § "Cross-family review — bridge pattern":

- Author = Anthropic (Cowork or Codex session per artifact)
- Editor = `groq/llama-3.3-70b-versatile`
- Judge = `google/gemini-2.5-pro`
- Red Team = `groq/openai/gpt-oss-120b`

Per-artifact dispatch packet:
```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.

Task: Author the FID artifact pipeline/funder_intelligence/reviewer_heuristics/<type>.yaml
      (or pipeline/funder_intelligence/programs/<id>.yaml for RBDG)
      per Pillar-3 extraction methodology.

Inputs:
- Pillar-1 Depth Charter (operator-signed): pipeline/funder_intelligence/_research_corpus/<artifact_id>/charter.signed.yaml
- Pillar-2 corpus + manifest: pipeline/funder_intelligence/_research_corpus/<artifact_id>/
- FID schema: pipeline/funder_intelligence/_schema/fid_<family>.schema.json (lands at first artifact closure)
- Extraction methodology: pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md §3.3
- Anti-fabrication discipline: pipeline/funder_intelligence/_research_corpus/README.md §1-5

Done definition:
- All facts carry corpus_ref + verbatim_quote (≤2 sentences each)
- Every quote matches the cited file byte-for-byte
- _confidence: low marker on any source-ambiguous fact (operator spot-check escalation)
- lifecycle.draft_status: audited after L-005 single-cycle audit closes unanimous

Hand back at: draft ready for L-005 single-cycle audit dispatch.
```

L-005 single-cycle audit per artifact (LIGHTER than card Thesis — audit is mostly provenance-chain verification + corpus_ref byte-match + ≤2-sentence quote + rubric-source citation). Pass = unanimous READY_TO_LOCK + zero P0 findings. Fail = REQUIRES_FIXES → author folds → second cycle. Maximum two cycles (L-005). Fix-in-place at LOCK.

**Gateway-saturation cap:** 2 artifacts × 3 seats = 6 simultaneous calls + seat-stagger (Wave-2 lesson). 17 artifacts ÷ 2 = ~9 batches over ~12 working days at ~1 batch/day comfortable cadence.

Week 6 end-state: 17 FID artifacts at `lifecycle.cross_family_thesis_status: passed`.

### Step 5 — Methodology LOCK (Week 7: 2026-06-29 → 2026-07-03)

**Operator-time: ~4-6 hrs.**

- Retrospective doc at `pipeline/funder_intelligence/_methodology/exemplar_pair_retrospective.md` (capturing lessons across the 17 artifacts; reviewer-type-corpus-shape vs program-corpus-shape comparison).
- Methodology v1.0 doc at `pipeline/funder_intelligence/_methodology/v1.0.md` with field-test section marked `DORMANT — pending grant drafting reactivation`.
- F-FID-* family LOCK ceremony: 8 fail-closed gates per planning doc §2.2 — fact-orphan, signature-invalid, corpus-hash-mismatch, classification-leak, cross-artifact-coupling, stale-rubric, reviewer-heuristic-fabrication, coverage-incomplete. Compound paired-commit with methodology v1.0 doc + §0.5 index. Operator-Ed25519-signed; registered in `lock_history.v1.jsonl`.
- Card smart-pointer migration: CLC cards gain `commonly_reviewed_by: [reviewer_type_id, ...]`; reviewer-type artifacts get `commonly_engaged_in_clcs: [clc_id, ...]`. Symmetric many-to-many pointers. Mechanical; lifecycle untouched. ~6-8 CIC + CLC cards touched (whichever pair with completed reviewer types).
- Phase-2 scale-out dispatch plan pre-staged (16 remaining funder + program + cascade artifacts for the exemplar pair).

## §3 — Sprint totals (revised)

| Metric | 2026-05-16 plan (exemplar-pair-first) | 2026-05-18 amendment (reviewer-types-first sprint) |
|---|---|---|
| Duration | 8 weeks | 6-7 weeks |
| Artifacts at sprint close | 21 (8 funders + 6 programs + 3 cascades + 4 reviewer types) | 17 (16 reviewer types + 1 program: RBDG); pair-of-four option adds 3 |
| Operator-hours | ~50 hrs (per 2026-05-16 §2 revised total) | ~45-55 hrs |
| Compute envelope | ~1500 hrs LLM-extraction equivalent | ~700-1000 hrs LLM-extraction equivalent (reviewer-type corpus lighter per artifact) |
| Methodology-anchor coverage | Single artifact-family shape (mostly funder + program) | Two artifact-family shapes (reviewer-type + program via RBDG) |
| Phase 2 sprint payback | Slow — reviewer-types deferred to Phase 2 | Fast — reviewer-types pre-built; Phase 2 = remaining funder + program + cascade artifacts only |

## §4 — Audit gates (unchanged from 2026-05-16 §4)

`F-FID-*` failure-code family realizes as `§4 v2.x.z` follow-on amendment at sprint close (Step 5). Phase-1 audit discipline still enforced by:

- Depth Charter template (Pillar 1 — schema + done definition + tier classification)
- Corpus-management README (`pipeline/funder_intelligence/_research_corpus/README.md` — provenance + ≤2-sentence quote + primary-source-only)
- Cross-family audit (L-005 single-cycle Editor + Judge + Red Team)
- Pre-staged Logician PRE-gate spec (planning doc §2.2 — forward-declared but not LIVE until Step 5 LOCK)

## §5 — Lessons Memory feedback loop (unchanged from 2026-05-16 §5)

Per planning doc §8:

1. Every artifact extraction emits a CycleReceipt (§17 v1 WPFA).
2. Lessons emitted seed `pipeline/funder_intelligence/lessons_seed/<cycle_id>.yaml`.
3. At Archivist v1.x landing, seed migrates to Archivist's canonical store.
4. Bridge mechanism mirrors Reflection Packet v0.1-hook → v0.2-first-wave dormant→live transition.

## §6 — What this amendment does NOT change

- The architecture-layer FID lattice (planning doc §2) — same four artifact families, same signed-asset pattern, same F-FID-* family roster, same consumer mapping.
- The four-pillar methodology (planning doc §3) — Pillar 1 charter → Pillar 2 corpus → Pillar 3 extraction → Pillar 4 calibration (DORMANT).
- The three-tier classification (Tier-1 commons / Tier-2 opt-in / Tier-3 my-eyes-only) — inherited from architecture v7.0.10 unchanged.
- The cross-family audit roster (Editor=meta / Judge=google / Red Team=openai-oss / Author=Anthropic) — unchanged per AGENTS.md bridge pattern.
- The publisher Ed25519 key — same dedicated FID publisher pubkey `634441fd…81c37b8f` pinned at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`.
- Phase-2 horizon scoping — remaining 16 exemplar-pair artifacts (8 funders + 5 more programs + 3 cascades) deferred to Phase 2 as before, but with the 16 reviewer-type artifacts available as references (vs deferred to Phase 2 in the 2026-05-16 plan).

## §7 — Roll-back path

If operator signs the brief with overrides that revert to exemplar-pair-first scoping (brief Decision 7 → option (d)), this amendment dormants and the 2026-05-16 dispatch plan re-activates as the LIVE plan. Universe LOCK file (`_universe.signed.yaml`) would still be authored at Day 1 but with only the 4 original reviewer types from the exemplar pair, with the remaining 12 reviewer types deferred to Phase 2 scale-out per the 2026-05-16 plan.

No artifact work, no card migration, no LOCK ceremony is triggered before operator daylight confirmation via the PR thread on `docs/FID_PHASE_1_PRE_KICKOFF_BRIEF_2026-05-18.md`.

---

## Cross-references

- Original dispatch plan: `pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md`
- Pre-kickoff brief (operator daylight record): `docs/FID_PHASE_1_PRE_KICKOFF_BRIEF_2026-05-18.md`
- Planning doc: `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md`
- RBDG dispatch packet: `pipeline/handoffs/fid_exemplar_usda_rd_rbdg_fy26_dispatch_2026-05-16.md`
- FID lattice: `pipeline/funder_intelligence/README.md`
- Reviewer-heuristics seed: `skills/scribe-ghostwriter/references/reviewer_heuristics.md`
- Cards CIC + CLC: `pipeline/cards/CIC/` + `pipeline/cards/CLC/`
- Cross-family bridge pattern: `AGENTS.md`
