# FID Expanded Roster — 8 Funders + 6 Programs

**Status:** DRAFT for operator sign-off — 2026-05-18 (revised same day to tidy cascades to Phase 2)
**Authority:** `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §4.2 (the original exemplar-pair scope) + `docs/FID_PHASE_1_PRE_KICKOFF_BRIEF_2026-05-18.md` (the reviewer-types-first re-scope; 16-type roster).
**Companion:** `pipeline/planning/fid_phase_1_dispatch_plan_amendment_2026-05-18.md` (Phase-1 sprint shape under reviewer-types-first).
**Anchor:** Monday 2026-05-18 (operator-confirmed in pre-kickoff brief Decision 1 default).
**Compressed timeline:** ~5 working weeks from anchor (vs. the 2026-05-16 8-week plan and the 2026-05-18 6-7-week reviewer-types-first plan); see §Compressed timeline plan below.
**Revision note (2026-05-18 PM):** The originally-scoped "3 review-pipeline cascades" primitive (screen / score / consensus) is deferred to Phase 2 research per operator call this session. The substance of stage-aware review may instead land as a `participates_in_review_stages: [...]` field on each of the 16 reviewer-type artifacts in the parallel reviewer-types-first workstream — to be decided by a one-charter spike during that sprint. See §"Deferred to Phase 2 research" below.

---

## Scope summary

This roster restates the **funder-side + program-side** Phase-1 scope under a compressed timeline. The roster is the **non-reviewer half** of the §4.2 exemplar-pair scope from the FID research planning doc — `food_systems` (CIC-01) × `operating_capacity` (CLC-03). The 16 reviewer types referenced in the pre-kickoff brief are out of scope for THIS roster doc — they're authored in a parallel reviewer-types-first sprint. Review-pipeline-cascade structure is deferred to Phase 2 research per operator call this session.

Success looks like: 8 funder + 6 program artifacts at `lifecycle.cross_family_thesis_status: passed` + `lifecycle.draft_status: audited`, the methodology v1.0 doc folded in at LOCK, smart-pointer migration on the two exemplar cards (food_systems + operating_capacity) — all in 5 working weeks once reviewer-types are pre-built. Pillar-4 calibration tracks remain DORMANT (per the active 2026-05-16 scope correction — no grant drafting active) and are out of scope for this sprint.

## The 8 funders

Names and rationale from `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §4.2 verbatim, with operator-discretion slot preserved.

| # | Funder ID | Type | Why this funder (repo-grounded) | Repo citation |
|---|-----------|------|--------------------------------|---------------|
| 1 | `USDA-RD` | Federal agency | Rural Development. Anchors the operating-capacity CLC for ag operators (RBDG, RCDG, CFP). Operator-familiar. | FID planning §4.2; FID lattice `pipeline/funder_intelligence/funders/README.md` |
| 2 | `USDA-NIFA` | Federal agency | National Institute of Food and Agriculture. Anchors Research & Evidence CLC overlay (SARE, AFRI) that often pairs with operating-capacity work. | FID planning §4.2 |
| 3 | `USDA-AMS` | Federal agency | Agricultural Marketing Service. Houses VAPG (rubric already extracted at `pipeline/rubrics/vapg_fy26.json`); Market Access CLC overlay. | FID planning §4.2; `pipeline/rubrics/vapg_fy26.json` |
| 4 | `PA-DEPT-AG` | State agency | PA Dept of Agriculture. State-level Operating Capacity + Public Purpose overlay; existing partial Phase-2 sketches in skills. | FID planning §4.2 |
| 5 | `PA-DCED` | State agency | PA Dept of Community & Economic Development. State public-purpose + redevelopment + operating-capacity overlay. | FID planning §4.2 |
| 6 | `HEINZ-FOUNDATION` | Regional foundation | Pittsburgh-region foundation example for foundation-program-officer dialect calibration. | FID planning §4.2 |
| 7 | `NCBA-CLUSA` | National intermediary | Cooperative intermediary; member-driven cooperative-board-peer-review shape distinct from foundation review (per pre-kickoff brief Decision 9). | FID planning §4.2; pre-kickoff brief Decision 9 |
| 8 | `<operator-choice-state-foundation>` | State foundation | One additional state foundation, operator chooses at Pillar 1 charter authoring per planning doc §4.2. | FID planning §4.2 ("ONE additional state foundation (operator chooses at Pillar 1)") |

**What we still need to learn (across the 8):** funder-officer relationship notes (Tier-3, operator-only), historical award patterns (Tier-1 from USAspending.gov + 990-PFs), funder dialect across each agency, compliance cascade defaults invoked by each funder, current program rosters keyed to FY26.

## The 6 programs

Names and rationale from FID planning §4.2 verbatim.

| # | Program ID | Funder | Dollar range (typical, NEEDED-verified at Pillar 2) | Eligibility class | Fit | PRP status |
|---|-----------|--------|----------------------------------------------------|-------------------|-----|------------|
| 1 | `USDA-AMS-VAPG-FY26` | USDA-AMS | Planning $75K / Working Capital $250K (typical FY24-25 caps; verify FY26) | Independent producers, ag producer groups, farmer/rancher coops, majority-controlled producer-based businesses | Reference depth; rubric already extracted to `pipeline/rubrics/vapg_fy26.json`. Map to Market Access CLC + operating-capacity overlay. | Stub-only in `active_prps.yaml` as `TILTH-PRP-USDA-VAPG-FY26` (entry 6; not yet authored) |
| 2 | `USDA-RD-RBDG-FY26` | USDA-RD | Typically $50K–$500K | Rural public bodies, nonprofits, federally-recognized tribes serving rural areas | Pre-kickoff brief Decision 6 default = methodology-anchor first artifact for the program-shape leg. | No PRP yet; FID-program artifact only |
| 3 | `USDA-RD-RCDG-FY26` | USDA-RD | Typically up to $250K (cooperative development centers) | Nonprofit cooperative development centers (501(c)) | Operating Capacity for cooperative-formation work; pairs with NCBA-CLUSA reviewer mapping. | No PRP yet |
| 4 | `USDA-NIFA-SARE-NE-FY26` | USDA-NIFA | Tiered (Farmer/Rancher up to $30K; Partnership; Research & Education to $250K+) | Producers, researchers, extension, NGOs in NE region | Peer-reviewer-academic dialect calibration; Research & Evidence overlay. | No PRP yet |
| 5 | `PA-DEPT-AG-AGINNOV-FY26` | PA-DEPT-AG | Typically $25K–$500K (PA Ag Innovation has varied tracks) | PA agriculture businesses, processors, infrastructure projects | State-program-officer dialect calibration. **Note:** per CLAUDE.md "What NOT to do," PA Ag Innovation is OFF the table as a dogfood target for v0.1 — this artifact is FID-knowledge-only, not an applicant pursuit. | No PRP yet |
| 6 | `USDA-RD-CFP-FY26` | USDA-RD | Community Facilities — direct loans + grants, tiered to median household income; typical grant cap $50K (varies) | Public bodies, nonprofits, federally-recognized tribes (rural population threshold) | Operating-capacity-flavored; touches DAVIS-BACON cross-cutting cascade. | No PRP yet |

**Cross-references:** the v0.2-first-wave PRPs in `pipeline/program_rule_packs/_manifest/active_prps.yaml` (TILTH-PRP-2CFR200, TILTH-PRP-DAVIS-BACON, TILTH-PRP-NEPA-24CFR58) are compliance-framework cross-cutting regulations consumed by these programs — they're a SEPARATE structural layer from this 6-program roster and from the 3 review-pipeline cascades below.

## Deferred to Phase 2 research — review-pipeline-cascade primitive

The original framing of this roster included **3 review-pipeline cascades** (proposed default: `screen-cascade` → `score-cascade` → `consensus-cascade`) as a fifth FID artifact family alongside funders, programs, compliance_cascades, and reviewer_heuristics. Operator daylight call this session (2026-05-18 PM) deferred this scope to Phase 2 research.

**Why deferred, not adopted, not killed:**

The FID research planning doc names only four artifact families. The "3 review-pipeline cascades" primitive was a new addition originating from operator clarification this session, not from §4.2 of the planning doc. A real adversarial pass (Champion vs. Devil's Advocate) on whether to add the primitive surfaced a genuine empirical dispute — not a philosophical one. The strongest Champion claim ("time budgets and heuristics differ by stage, not by reviewer") is true. The strongest Devil's Advocate claim ("cascade-as-free-standing entity doesn't survive contact with funder-specific reality; substance ends up funder-specific footnotes that belong on funder/program artifacts") is also true. Which one wins is decidable by writing one cascade Pillar-1 charter and looking at how much substance lands as genuinely cross-funder vs. as funder-specific footnote. That spike is cheap; the wrong answer baked into Phase 1 is expensive.

**What Phase 1 ships instead:** the cheap interim is a `participates_in_review_stages: [<stage_enum>, ...]` field on each of the 16 reviewer-type artifacts authored in the parallel reviewer-types-first sprint. Enum vocabulary (`screen` / `score` / `consensus` or operator-preferred) is set when the reviewer-types Universe LOCK file is signed. This gives Scribe and Judge stage-aware reviewer lookup at runtime without committing to a fifth primitive.

**The Phase 2 spike (deferred work, surfaced here so it's not forgotten):**

- Author one review-stage Pillar-1 Depth Charter (suggested: `screen-stage`, since it's the most likely to carry genuinely cross-funder substance — admin completeness rules, SAM.gov status checks, page-limit norms).
- Assemble the Pillar-2 corpus.
- Read what landed. If ≤1 page of substance is genuinely shared across federal + foundation + state + CDFI screen stages, drop the primitive — the `participates_in_review_stages:` enum on reviewer types was sufficient. If 3+ pages of cross-funder material, formalize as a new FID artifact family and run the remaining 2 stages.

**Naming reservation:** if Phase 2 spike validates the primitive, the directory should be `pipeline/funder_intelligence/review_stages/` (not `cascades/`) to avoid collision with the existing `compliance_cascades/`. Reserve that path now; do not create until the spike clears.

The 16 reviewer types still get authored as the dominant FID artifact family in the reviewer-types-first sprint. Their per-type artifacts will carry stage-participation as a field, which is enough to support Phase-1 grant drafting workflows when drafting reactivates.

## Compressed timeline plan

Baseline = 2026-05-16 plan (8 weeks, 21 artifacts including 4 reviewer types). Pre-kickoff brief revision (2026-05-18) = 6-7 weeks reviewer-types-first sprint covering 16 reviewer types + 1-4 funder/program/cascade methodology-anchor artifacts. **This compressed roster plan = 5 working weeks for the non-reviewer 8 funder + 6 program artifacts (14 artifacts), executing AFTER the reviewer-types workstream lands.** Total Phase-1 elapsed time end-to-end = ~11-12 weeks (reviewer-types sprint 6-7 weeks → roster sprint 5 weeks; can partially overlap).

| Week | Work | Operator-time budget | Compute budget |
|------|------|----------------------|----------------|
| Week 1 | Pillar-1 Depth Charters for all 14 artifacts (8 funder + 6 program) authored in two batches; operator review + Ed25519 signing in two sittings. Universe LOCK file signed. | ~7-9 hrs Josh | n/a (charter authoring is Cowork-side) |
| Weeks 2-3 | Pillar-2 corpus assembly in parallel across all 14 artifacts. LLM-bulk fetching + operator spot-check. Manifest-sign each artifact's corpus at closure. Funder + program corpus is faster than reviewer-type corpus (more public NOFO + agency-page material). | ~9-11 hrs Josh | ~130-220 hrs LLM-extraction equivalent |
| Weeks 4-5 | Pillar-3 extraction + structuring via cross-family openclaw bridge dispatch. Author=Anthropic, Editor=`groq/llama-3.3-70b-versatile`, Judge=`google/gemini-2.5-pro`, Red Team=`groq/openai/gpt-oss-120b`. Single-cycle L-005 audit per artifact. Gateway-saturation cap = 2 artifacts × 3 seats = 6 simultaneous calls. 14 artifacts ÷ 2 = ~7 batches over ~8 working days. Methodology v1.0 doc updated in week 5; smart-pointer migration on food_systems + operating_capacity cards (mechanical, lifecycle untouched). | ~10-13 hrs Josh | ~400-600 hrs LLM compute |
| **Sprint totals (this roster only)** | **5 weeks; ~26-33 hrs Josh; ~530-820 hrs compute** | | |

**Explicit cuts vs. the 8-week 2026-05-16 plan:**

- **Cut 1: Pillar-4 calibration tracks (Tracks A/B/C) — DORMANT.** Per pre-kickoff brief Decisions 2/3/4 default DORMANT, inherited from the 2026-05-16 active-scope correction. No grant drafting active = no draft-comparison panel. Saves ~$1,800 cash + ~$6K cash + 25-50 operator-hrs.
- **Cut 2: Reviewer-types in this roster — separate workstream.** Per operator clarification, the 16 reviewer types are authored in the parallel reviewer-types-first sprint. Saves ~6-8 hrs operator time in this sprint.
- **Cut 3: 3 review-pipeline cascades deferred to Phase 2 research.** Per operator call this session, the cascade primitive is deferred pending a one-charter spike during the reviewer-types-first sprint. Saves ~4-7 hrs Josh + ~120-200 hrs compute in this sprint vs. carrying the 3 cascade artifacts.
- **Cut 4: Compressed Pillar-1 charter authoring.** Originally Week 1 = single artifact-class charter sprint; compressed = two batches across two sittings (8 funders Monday, 6 programs Wednesday) per pre-kickoff brief's batch-of-4-5 pattern. Saves ~2 operator-hrs vs. one-charter-per-sitting cadence.
- **Cut 5: Parallel Pillar-2 corpus assembly.** Originally Weeks 2-3 sequential per artifact family; compressed = parallel across all 14 artifacts simultaneously. The dependency chain only forces serialization within an artifact (Pillar 1 → Pillar 2 → Pillar 3) not across them.
- **Cut 6: Pillar-3 single-cycle audit (not two-cycle).** Per FID planning §7.3, FID artifacts use single-cycle L-005 audits (lighter than card Thesis) because provenance verification IS the audit. Already in the 2026-05-16 baseline; preserved here, not an additional cut.
- **No cut: Logician F-FID-* coverage.** All 8 F-FID-* failure-code primitives (per FID planning §2.2) still LOCK as a compound paired-commit alongside the methodology v1.0 doc at week-5 close.

**Where the compression risk lives:**

- Parallel Pillar-2 corpus assembly hits gateway-saturation caps faster (Wave-2 lesson — cap was 2 card-pairs × 3 seats = 6 simultaneous calls). 14 artifacts in parallel may need stagger-batching at corpus-fetch time. **Mitigation:** Weeks 2-3 schedule allows up to 14 days of working time; gateway cap allows ~2-3 artifacts per working day in parallel, so 14 ÷ 2.5 ≈ 6 working days of corpus fetch — fits comfortably in 2 weeks.
- Cross-family Thesis dispatch in weeks 4-5 needs the openclaw gateway working. If openclaw is intermittent, the audit slips. **Mitigation:** Wave-2 staggered-batch pattern + the bridge-pattern fallback per `/AGENTS.md`.
- One additional state foundation (Funder #8) is operator-discretion at Pillar 1 — if operator hasn't named it by Monday, charter authoring for that one artifact slips by ~1 day. **Mitigation:** propose 2-3 candidate state foundations in the Monday kick-off so operator can pick from a shortlist.

## Decisions awaiting operator confirm

- **D1 (8th funder identity).** Operator names the one additional state foundation (FID planning §4.2 reserved this as Pillar-1 operator-choice). **Recommended default:** Cowork proposes 2-3 candidates at Monday kick-off (e.g., PA-CCA Cultural & Historical, Allegheny Regional Asset District, McCune Foundation) for operator pick.
- **D2 (sprint sequencing relative to reviewer-types-first).** Run this roster sprint sequentially AFTER the reviewer-types-first 6-7-week sprint (end-to-end ~11-12 weeks), or partially overlap (start Pillar-1 charters for this roster at week 4 of the reviewer-types sprint, accepting ~5-8 extra operator-hrs in the overlap weeks)? **Recommended default:** sequential — overlap risks operator-time saturation at the very moment reviewer-types audits are firing.
- **D3 (`participates_in_review_stages:` enum vocabulary).** With cascades deferred to Phase 2, the interim is a stage-participation enum field on each of the 16 reviewer-type artifacts. Confirm the enum values: `screen` / `score` / `consensus` — or operator-preferred names. **Recommended default:** `screen` / `score` / `consensus`. Locks at the same moment as the reviewer-types Universe LOCK file in the parallel workstream.
- **D4 (PA-DEPT-AG-AGINNOV-FY26 inclusion).** This program is included as a FID knowledge artifact only — NOT as a v0.1 applicant target (per CLAUDE.md "What NOT to do"). Operator confirms inclusion-as-knowledge vs. drop. **Recommended default:** include as knowledge — Tilth needs the dialect even if FIT Farms doesn't apply.

## What this depends on

- **Reviewer-types-first sprint completion** (pre-kickoff brief Step 1-5, weeks 1-7). Without the 16 reviewer-type artifacts and the `_universe.signed.yaml` lock, the cascade × reviewer-type membership table in §"The 3 cascades" above can't reach `validated` lifecycle. **Status:** AWAITING operator daylight sign-off on pre-kickoff brief Decisions 1-9.
- **Cards-aware seat wiring** (currently on `cards-aware-seat-wiring-2026-05-18` branch, dirty). When the seat-wiring lands, the smart-pointer migration on food_systems + operating_capacity cards at week 5 can use the wired loader to verify pointers resolve. **Status:** WIP on branch; expected to land before week 5 of this roster sprint.
- **Signature-roundtrip CI** (`.github/workflows/signature_roundtrip.yml`, landed 2026-05-18 per `docs/project_audit_2026-05-18.md` §13). The compound paired-commit at week 5 (8 F-FID-* primitives + methodology v1.0 doc + smart-pointer card migration) must pass signature-roundtrip CI before merge. **Status:** GREEN on main as of 2026-05-18.
- **FID publisher key** pinned at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml` (PINNED 2026-05-16 per pre-kickoff brief Decision 5 default). **Status:** in place.
- **PRP cross-cutting trio** (2 CFR 200 / Davis-Bacon / NEPA) authored as DRAFTs at `pipeline/program_rule_packs/cross_cutting/`. The 6 programs in this roster will cross-reference these PRPs at Pillar 3 extraction. **Status:** DRAFT bodies on disk; LOCK pending L-005 cross-family Thesis per `pipeline/program_rule_packs/_manifest/active_prps.yaml` notes.
- **AGENTS.md cross-family bridge pattern** working through openclaw gateway. Audit dispatch in weeks 4-5 depends on this. **Status:** working per Wave-2 lessons; gateway-saturation cap respected.

---

## Cross-references

- FID research planning doc (authority): `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` (§4.2 exemplar-pair artifact list; §3 four-pillar methodology; §9.1 original 8-week timeline)
- FID Phase-1 pre-kickoff brief: `docs/FID_PHASE_1_PRE_KICKOFF_BRIEF_2026-05-18.md` (16-type roster; reviewer-types-first sprint shape; 9 operational decisions awaiting confirm)
- FID Phase-1 dispatch plan amendment: `pipeline/planning/fid_phase_1_dispatch_plan_amendment_2026-05-18.md`
- FID lattice README: `pipeline/funder_intelligence/README.md`
- FID compliance-cascade README (distinct primitive from the review-pipeline cascades in this doc): `pipeline/funder_intelligence/compliance_cascades/README.md`
- VAPG FY26 rubric (extracted): `pipeline/rubrics/vapg_fy26.json`
- PRP cross-cutting trio: `pipeline/program_rule_packs/cross_cutting/{TILTH-PRP-2CFR200,TILTH-PRP-DAVIS-BACON,TILTH-PRP-NEPA-24CFR58}/v1.yaml`
- Active PRP manifest: `pipeline/program_rule_packs/_manifest/active_prps.yaml`
- Cards (smart-pointer migration targets at week 5): `pipeline/cards/CIC/food_systems.yaml` + `pipeline/cards/CLC/operating_capacity.yaml`
- Signature-roundtrip CI workflow: `.github/workflows/signature_roundtrip.yml`
- Funder-as-specimen integration thesis: `pipeline/planning/funder_as_specimen_integration_2026-05-16.md`
- Operator clarification 2026-05-18 (this session): "3 cascades" = FID review pipeline stages, not compliance cascades; 16 reviewer types handled in parallel workstream.

---

## Sign-off path

1. Josh reviews this roster + the pre-kickoff brief's 9 decisions (the two are paired — this roster assumes pre-kickoff Decision 7 = (b) reviewer-types-first + RBDG anchor, and Decision 8 = (a) 16-type hybrid C).
2. Josh confirms or overrides D1-D4 above in PR thread. Suggested format:
   ```
   D1 (8th funder): name → <funder> OR ask Cowork to propose shortlist
   D2 (sequencing): sequential / overlap
   D3 (review-stage enum): confirm screen/score/consensus / override → <new vocabulary>
   D4 (PA AG INNOV inclusion as knowledge): confirm include / drop
   ```
3. Cowork updates this roster doc + the dispatch plan amendment at `pipeline/planning/fid_phase_1_dispatch_plan_amendment_2026-05-18.md` to reflect overrides. Paired-commit.
4. Week-1 Pillar-1 charter authoring fires for the 14 roster artifacts once the reviewer-types-first sprint Universe LOCK has been signed (pre-kickoff brief Step 1) — or in parallel if Josh overrides D2 to overlap.
5. Phase 2 review-stage-primitive spike runs during the reviewer-types-first sprint as a separate one-charter Pillar-1 exercise (see §"Deferred to Phase 2 research" above). Outcome — keep or drop the primitive — is decided after the spike clears, not before.
