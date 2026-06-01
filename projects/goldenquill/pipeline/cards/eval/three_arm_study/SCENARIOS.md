# Three-Arm Study — Scenario Inventory + Reviewer Mix + Outcome Pre-Registration

**Status:** v0.1 Beta skeleton per Embedding Plan §A.3 P2-4. Scenario fixture authoring + paid reviewer recruitment land in Phase 5 (v0.2-late horizon).
**Source canon:** `Cards_Prompts_and_Research_Plans_v2_fused.md` §8 + §10.
**Companion files:** `pipeline/cards/eval/scenarios/_SCHEMA.md` (authoring schema), `arm_a_uncarded_tilth/`, `arm_b_carded_tilth/`, `arm_c_frontier_baseline/`, `pipeline/cards/eval/six_forms_of_value/RUBRIC.md`.

## The four scenarios (per §10)

Selected to cover the breadth of the card system and surface the most distinct reviewer dialects. Each scenario authors one fictional applicant against one real public RFA, runs through all three arms, and gets scored by a paid reviewer panel matched to the scenario's CLC.

| # | Scenario slug | CIC × CLC | Distinct reviewer dialect | Realistic example RFA target (Phase 5 to confirm cycle live) |
|---|---------------|-----------|----------------------------|--------------------------------------------------------------|
| 1 | `food_systems_market_access` | `food_systems` × `market_access` | USDA RBCS commercialization reviewer + ag-marketing professional + value-added producer-cooperative consultant | USDA VAPG FY26 (Value-Added Producer Grant) |
| 2 | `public_agency_public_purpose_works` | `public_agency` × `public_purpose_works` | Federal program officer (retired) + municipal CFO + public works engineer | EPA CWSRF / DOT RAISE / HUD CDBG (whichever cycle is live at Phase 5 fixture authoring) |
| 3 | `arts_culture_sponsorship_corporate` | `arts_culture` × `sponsorship_corporate` | Corporate-foundation program officer + cultural-organization development director + sponsorship-relations consultant | Mellon / NEA + named corporate-foundation sponsorship cycle |
| 4 | `ecosystem_intermediary_research_evidence` | `ecosystem_intermediary` × `research_evidence` | NSF / AFRI program officer + applied-research methodologist + intermediary-portfolio evaluator | NSF SBIR / USDA AFRI evaluation-component / Kauffman intermediary RFP |

Scenarios 1–4 are the v0.1 / v0.2 scope. Additional scenarios (e.g. cooperative × shared_assets, educator × catalytic_change) become candidates for the v1.x extension if Phase 5 surfaces signal worth scaling.

## Why these four

- **Each pairs a structurally distinct CIC with a structurally distinct CLC.** No CIC or CLC repeats. The four scenarios collectively exercise all six CIC archetypes minus educator + cooperative, and four of the eight CLC archetypes. The remaining CICs / CLCs ride to v1.x extension.
- **Each surfaces a reviewer dialect the prior scenario does not.** USDA commercialization reviewers, municipal CFOs, corporate-foundation officers, and NSF/AFRI evaluators read drafts differently. Drafts that win one reviewer dialect can lose another. The cards encode that variation; the study tests whether they encode it well.
- **Each has a recruitable paid-reviewer pool.** USDA RBCS network, retired federal program officers, corporate-foundation alumni, applied-research evaluators — all have professional bodies with public membership rosters that surface candidates.
- **Each maps onto a fundable evaluation pitch.** Per §8.5, Research & Evidence (CLC-04), Catalytic Change (CLC-02), and Market Access (CLC-05) are the strongest CLCs for an evaluation-funding pitch; scenarios 1 and 4 hit two of them. Scenarios 2 and 3 are CDBG/RAISE/Mellon-paid-reviewer-realistic.

## Reviewer mix per scenario

Each scenario recruits 3–5 reviewers per the §8.4 pattern. Reviewer composition is pre-declared so post-hoc reviewer-mix tuning cannot move results.

### Scenario 1 — Food Systems × Market Access

| Reviewer slot | Profile | Recruitment pool |
|---------------|---------|-------------------|
| R1 | Retired or freelance USDA RBCS / RBS program officer | RBCS alumni network, freelance directories of former federal officers |
| R2 | Value-added producer cooperative consultant | NCBA-CLUSA roster, USDA Cooperative-Development-Center directory |
| R3 | Ag-marketing professional (commercialization track) | American Ag Editors Association, NRCS / SARE reviewer alumni |
| R4 | (optional) Producer-cooperative cofounder with VAPG award history | Public VAPG award abstracts → direct outreach |
| R5 | (optional) State-level ag-business development officer | State-DOA reviewer rosters where published |

### Scenario 2 — Public Agency × Public Purpose & Works

| Reviewer slot | Profile | Recruitment pool |
|---------------|---------|-------------------|
| R1 | Retired federal program officer (CDBG / RAISE / CWSRF) | HUD / DOT / EPA alumni networks |
| R2 | Municipal CFO or public-works finance director | GFOA member directory, NACo membership |
| R3 | Public-works engineer (PE-stamped opinion writer) | ASCE member directory, state PE-roll lookups |
| R4 | (optional) Tribal or rural-municipal public-finance consultant | Tribal Self-Governance alumni, rural-LISC roster |
| R5 | (optional) Independent NEPA / environmental-review specialist | NAEP member roster |

### Scenario 3 — Arts & Culture × Sponsorship & Corporate

| Reviewer slot | Profile | Recruitment pool |
|---------------|---------|-------------------|
| R1 | Corporate-foundation program officer (current or retired) | CECP membership, corporate-foundation alumni network |
| R2 | Cultural-organization development director (10+ years) | AFP membership, cultural-organization development listservs |
| R3 | Sponsorship-relations consultant (arts-sector specialist) | Association of Fundraising Professionals (arts chapter), IEG roster |
| R4 | (optional) Mellon / NEA grants alumni reviewer | NEA peer-panelist alumni network |
| R5 | (optional) Fiscal-sponsor program director | NNFS member directory |

### Scenario 4 — Ecosystem Intermediary × Research & Evidence

| Reviewer slot | Profile | Recruitment pool |
|---------------|---------|-------------------|
| R1 | NSF / AFRI program officer (current or recent) | NSF / NIFA program-officer alumni networks |
| R2 | Applied-research methodologist (intermediary / impact evaluation) | AEA membership, Mathematica / Urban Institute alumni |
| R3 | Intermediary-portfolio evaluator (TA-provider or accelerator) | ANDE membership, ECPF alumni |
| R4 | (optional) CDFI research-evaluation analyst | OFN member directory |
| R5 | (optional) Foundation evaluation officer | Foundations on the Hill / Evaluation Roundtable alumni |

## Pre-registered primary outcomes

Per §8.3, all eight outcomes are pre-registered BEFORE any reviewer sees a draft. Outcomes scored per scenario and aggregated only after every scenario's reviewer panel completes.

| Outcome ID | Outcome | Scoring shape | Six Forms axis | Hypothesis direction |
|------------|---------|---------------|------------------|----------------------|
| O-RUBRIC | Rubric alignment | per-criterion Likert 1–5 | Review | Arm B > Arm A > Arm C |
| O-EVIDENCE | Evidence sufficiency | per-evidence-bucket Likert 1–5 | Evidence | Arm B > Arm A > Arm C |
| O-CONFIDENCE | Reviewer confidence (overall) | Likert 1–7 | Drafting + Review | Arm B > Arm A > Arm C |
| O-REDFLAGS | Red-flag reduction (count of card-flagged failure modes appearing in draft) | integer count | Review + Compliance | Arm B < Arm A; Arm B < Arm C |
| O-FUND-LIKELY | Likelihood-of-funding | Likert 1–7 | composite | Arm B > Arm A > Arm C |
| O-RANK | Overall rank preference across A/B/C | forced-choice ordinal | composite | Arm B preferred most often |
| O-EVID-INTERVIEW | Missing-evidence interview quality (when prompted "what else should the applicant supply?") | qualitative Likert 1–5 | Evidence | Arm B > Arm A; Arm C silent / generic |
| O-LANGUAGE | Reduction in generic AI language | qualitative coding by independent rater | Drafting | Arm B < Arm A < Arm C |

## Pre-registration discipline

Before reviewers see any draft, the following must be public:

1. **Hypothesis statement.** "Arm B (Tilth + cards) produces grant drafts that score higher on rubric alignment, evidence sufficiency, and reviewer confidence than Arm A (Tilth without cards) and Arm C (frontier LLM with rudimentary prompt) across N scenarios."
2. **Primary outcome list with scoring shapes** (see above).
3. **Statistical-power analysis** — sample size N per scenario × reviewers, expected effect size, alpha threshold, power calculation. Authored before Phase 5 reviewer recruitment.
4. **Analysis plan** — how outcomes aggregate, how confidence intervals compute, how rank-order preferences combine across reviewers.
5. **Publication commitment** — null or negative results are published unconditionally. No HARKing (Hypothesizing After Results are Known).

The pre-registration document lands at `pipeline/cards/eval/three_arm_study/PRE_REGISTRATION.md` before reviewer panels open. Until that file exists, the study has not started.

## Blinding + randomization

- Reviewers receive drafts with applicant identity stripped + system identity stripped. The same fictional applicant identity is used across all three arms within a scenario, so the only system-identifying signal is the draft itself.
- Format-normalization: drafts are reformatted to a common template (Helvetica 11pt, single-column, no footers). This removes Arm-C-frontier-LLM markdown idiosyncrasies and Arm-B-carded section-heading conventions as confounds.
- Per-reviewer arm ordering is randomized (Latin square if N reviewers ≥ N scenarios; balanced random otherwise).
- Reviewers complete one scenario at a time, blind to whether their next scenario will share arms or scenarios with the prior one.

## Compensation

Per §8.5 + Phase 5 estimate: $1.5K–$3K total reviewer fees per scenario (3–5 reviewers × $300–$600 honorarium). Funded via Phase 5 evaluation-funding pitch (CLC-04 Research & Evidence is the natural target).

## Phase ordering

Per `pipeline/cards/eval/README.md`:

1. **v0.1 Beta LOCK (current):** Skeleton lands (this file + arms/ + scenarios/ schema). Scenario fixtures NOT yet authored.
2. **v0.2:** Funding application drafted + submitted (using Tilth's own grant-finder + grant-writer skills — meta-dogfooding). Scenario fixture authoring begins for scenario 1 (Food Systems × Market Access — first published §10.5 recommendation). Reviewer-recruitment criteria drafted.
3. **v0.2-late / v1.x:** Funding secured → reviewer panel recruited → blinded eval runs for scenario 1 → results published regardless of finding direction.
4. **v1.x post-results:** if Arm B > Arm A → card investment continues, scenarios 2–4 land. If Arm B ≈ Arm A → card investment pauses or pivots. If Arm B < Arm A → card layer rolls back.

## What this skeleton does NOT promise

- Scenario fixtures are not yet authored. The authoring schema at `pipeline/cards/eval/scenarios/_SCHEMA.md` is the contract; fixture YAMLs land per the Phase 5 schedule.
- Reviewer panels are not yet recruited. The pools above are recruitment maps, not signed engagements.
- The pre-registration document is not yet authored. It lands BEFORE Phase 5 reviewer panels open.
- No empirical claim about the cards working exists yet. The claim becomes earnable only after Phase 5 scenario 1 reports.

This skeleton's job is to make sure that, when funding lands, every decision that could bias the study has already been made. No HARKing.
