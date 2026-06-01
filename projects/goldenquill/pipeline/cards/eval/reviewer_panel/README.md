# Reviewer panel — paid expert recruitment + blinded eval protocol

## Reviewer profile mix

Target panel composition (proportions TBD per scenario):

- **Grant reviewers** — current or former federal program officers (USDA, EDA, NSF, EPA, FEMA, DOT), foundation program staff (community development, climate-tech, food-systems philanthropy), state arts/humanities council reviewers, CDFI underwriters. Real review committee experience.
- **Grant writers** — independent practitioners with track records, agency contractors who write at scale, organizational grant officers at applicants. People who do the work the system is trying to do.
- **Funder reps** — foundation program officers, agency review-committee members, corporate-giving officers, sponsorship managers. The people whose minds the card `reviewer_profile_typical` content claims to model.

Mix per scenario depends on the scenario's CLC — a Public Purpose & Works scenario emphasizes federal program officers + engineers + compliance reviewers; a Sponsorship & Corporate Support scenario emphasizes corporate-giving officers + marketing managers; etc. Aim for ≥3 reviewers per draft for inter-rater reliability.

## Payment

Reviewers are PAID at fair market rate per evaluation. Approximate working assumption: $300–$500 per scenario per reviewer (3 drafts × ~30 min each + rubric scoring + free-text comments). Funded via the §18.19.4 funding pathway.

## Blinding protocol

- **Drafts anonymized.** Applicant identity is preserved (fictional applicant), but no system identity tells (no "produced by Tilth", no version strings, no audit-log artifacts). Format normalization across arms — same font, same margins, same section headers, same applicant fictional name across all three drafts of a scenario.
- **Arm identity hidden.** Reviewers do not know which arm produced which draft. Reviewers know there are three drafts per scenario produced by three different systems, but not which is which.
- **Order randomized per reviewer.** Each reviewer sees the three drafts in a random order. Counter-balanced across reviewers within scenario.
- **Reviewer-to-reviewer non-collusion.** Reviewers do not see each other's scores or comments until after all scoring is complete.

## Rubric per scenario

The eval rubric is derived from the scenario's `review_dimensions` block (per `pipeline/cards/eval/scenarios/_SCHEMA.md`). Rubric dimensions come from:

- Active CLC's `underwriting_criteria` + `scoring_weight_patterns` + `common_red_flags` + `reviewer_profile_typical.reviewer_priorities`.
- Funder rubric in `pipeline/rubrics/` library (if present).

**Important:** the rubric is constructed from the card's claimed targets, but the scoring is done by humans. This tests whether the card's claimed reviewer priorities actually align with what real reviewers prioritize — NOT whether the card's Judge agrees with the card's Scribe (which would be circular).

## Outcome measures

Per scenario:

- Per-dimension score (mean, std, inter-rater κ).
- Rank-order preference (which arm did each reviewer prefer overall).
- Likelihood-of-funding judgment (binary or Likert).
- Free-text comments (qualitative signal; coded post-hoc).

Pre-registered primary outcome measure declared in each scenario's pre-registration document.

## Statistical power

Pre-registered per scenario. Default working assumption: power analysis assumes Cohen's d = 0.5 effect size for primary measure (Arm B − Arm A), 80% power, α = 0.05; required n per scenario ≈ 8 reviewers per arm. Adjust per scenario based on outcome-measure type + funded sample-size budget.

## Anti-HARKing discipline

All pre-registrations land at OSF or equivalent BEFORE reviewer drafts distribution. Hypothesis + primary outcome measure + statistical test + analysis plan all locked. Post-registration analyses (secondary outcomes, exploratory comparisons) are explicitly labeled as such in results writeups.

## Public results discipline

Results published regardless of finding direction. Null results published. Negative results published (Arm B < Arm A). Publication includes scenario specs, card versions used, reviewer panel composition, full per-dimension data, rubric text, and pre-registration record. Aimed at a peer-reviewed venue if appropriate; minimum publication is a public archive at the operator's website + OSF.
