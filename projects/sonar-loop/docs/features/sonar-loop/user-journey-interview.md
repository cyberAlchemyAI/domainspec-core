---
feature: sonar-loop
version: current
status: draft
updatedAt: 2026-05-12
docType: interview
owners:
  - sonar-loop
---

# Sonar Loop User-Journey Interview (Grill Mode)

## Objective

Force a buyer-ready user-journey narrative for Sonar Loop that can survive commercialization scrutiny.

This is intentionally a hard interview. If an answer is vague, treat it as unresolved, pick option `D` when needed, and capture a blocker with owner/date.

## Usage Instructions (strict)

1. Run waves in order. Do not move forward if the previous wave has unresolved blockers.
2. For each question, select one option (`A/B/C/D`) and capture supporting evidence.
3. Apply the linked artifact updates immediately after each decision.
4. If any `D` answer remains at wave end, mark the wave as `not converged`.
5. At the end, verify convergence criteria in [Convergence Criteria](#convergence-criteria-when-the-view-is-nailed).

## Canonical Reference Links

- [SPEC.md](SPEC.md)
- [STORIES.md](STORIES.md)
- [workflows.md](workflows.md)
- [operations.md](operations.md)
- [rules.md](rules.md)
- [architecture.md](architecture.md)
- [README.md](../../../README.md)

## Journey Stages In Scope

- Evaluator journey: day 0 to day 1
- Pilot journey: week 1
- Scale journey: month 1
- Operator ongoing journey: steady-state weekly and monthly operations

## Wave Structure (dependency-ordered)

| Wave   | Focus                                   | Depends On       | Primary Journey Stage |
| ------ | --------------------------------------- | ---------------- | --------------------- |
| Wave 1 | Foundation and buyer trigger            | None             | Evaluator day 0-1     |
| Wave 2 | Adoption path and pilot motion          | Wave 1 converged | Pilot week 1          |
| Wave 3 | Proof and risk posture                  | Wave 2 converged | Scale month 1         |
| Wave 4 | Packaging, pricing, and operating model | Wave 3 converged | Operator ongoing      |

---

## Wave 1 - Foundation (Evaluator Day 0-1)

### Q1. Who is the first economic buyer, and what forces action now?

**Why this matters**
Without a named buyer and trigger, the narrative sounds like tooling interest, not a purchase case.

**Options**

- A. Engineering director buying to reduce release risk this quarter.
- B. Platform lead buying to standardize quality governance across repos.
- C. Product engineering manager buying to reduce remediation cycle time.
- D. Unclear buyer or mixed sponsor set (not yet validated).

**Recommendation guidance / tradeoffs**
Prefer one primary buyer for first sale motion. Multi-sponsor narratives can close larger deals but usually slow the first decision.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                                                |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| A      | Refine audience/value framing in [README.md](../../../README.md) and add buyer-specific acceptance language in [STORIES.md](STORIES.md). |
| B      | Emphasize cross-repo governance positioning in [SPEC.md](SPEC.md) and [architecture.md](architecture.md).                                |
| C      | Highlight cycle-time and operator throughput outcomes in [README.md](../../../README.md) and [operations.md](operations.md).             |
| D      | Add blocker + owner in this interview doc and mark buyer proposition as hypothesized in [SPEC.md](SPEC.md).                              |

### Q2. What is the evaluator's day-0 entry condition?

**Why this matters**
Day-0 assumptions drive setup friction. If this is wrong, evaluation fails before value is seen.

**Options**

- A. Existing Sonar + CI + issue tracker are already configured.
- B. Sonar exists, but quality governance policy is inconsistent.
- C. CI exists, Sonar maturity is low, needs guided bootstrap.
- D. Unknown actual starting maturity.

**Recommendation guidance / tradeoffs**
Choose the lowest maturity that still matches your real target buyer. Overstating maturity creates demo success but pilot failure.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                                         |
| ------ | --------------------------------------------------------------------------------------------------------------------------------- |
| A      | Tighten fast-start evaluator path in [workflows.md](workflows.md) and day-0 story steps in [STORIES.md](STORIES.md).              |
| B      | Expand policy alignment checkpoints in [rules.md](rules.md) and [operations.md](operations.md).                                   |
| C      | Add bootstrap branch and guardrails in [workflows.md](workflows.md) and architecture notes in [architecture.md](architecture.md). |
| D      | Add discovery task to quantify maturity bands in [STORIES.md](STORIES.md) and this interview tracker.                             |

### Q3. What is the "first value moment" by day 1?

**Why this matters**
Commercial buyers buy a time-to-value story, not a process description.

**Options**

- A. Deterministic quality gate selection + governed runtime fallback proof.
- B. First actionable finding bundles exported as remediation tasks.
- C. Clear checkpoint control proving safe continue/pause/halt behavior.
- D. No single value moment defined yet.

**Recommendation guidance / tradeoffs**
For commercialization, pick one headline value moment and one secondary proof. More than two weakens sales clarity.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                                           |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| A      | Lead with governance trust signal in [README.md](../../../README.md), supported by [rules.md](rules.md).                            |
| B      | Lead with output utility in [README.md](../../../README.md), backed by [operations.md](operations.md) and [STORIES.md](STORIES.md). |
| C      | Lead with operator control in [README.md](../../../README.md), backed by [workflows.md](workflows.md).                              |
| D      | Flag missing commercialization anchor in [SPEC.md](SPEC.md) and block Wave 2 until resolved.                                        |

### Q4. Which evaluator objection is most likely to kill the deal in day 0-1?

**Why this matters**
The primary objection determines what proof must be visible first.

**Options**

- A. "Fallback/runtime decisions are opaque and risky."
- B. "Export to GitHub/Jira will be brittle."
- C. "This adds process overhead without outcome gain."
- D. "We do not know the top objection yet."

**Recommendation guidance / tradeoffs**
Handle the strongest objection with concrete evidence artifacts, not promises. Unknown objection means weak interview depth.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                                            |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| A      | Strengthen fallback evidence narrative in [rules.md](rules.md), [operations.md](operations.md), and [README.md](../../../README.md). |
| B      | Strengthen API-first export flow and states in [operations.md](operations.md) and [workflows.md](workflows.md).                      |
| C      | Add measurable before/after signals to [SPEC.md](SPEC.md) and operator story acceptance criteria in [STORIES.md](STORIES.md).        |
| D      | Schedule 3 evaluator interviews and hold commercialization claims in [README.md](../../../README.md).                                |

### Wave 1 Decision Capture

| QID | Selected Option | Evidence (quote/data)                                                                                                                             | Required doc updates done? | Owner | Due date |
| --- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----- | -------- |
| Q1  | A               | User stated target includes leaders/managers/directors integrating AI into company workflows; primary buyer locked to one role for sales clarity. | No (pending sync)          |       |          |
| Q2  | C               | User stated highest value is with companies without Sonar and with legacy context, which maps to guided bootstrap.                                | No (pending sync)          |       |          |
| Q3  | B               | Selected in interactive session: first actionable finding bundles exported as remediation tasks.                                                  | No (pending sync)          |       |          |
| Q4  | C               | Selected in interactive session: strongest day-0/1 objection is process overhead vs outcome gain.                                                 | No (pending sync)          |       |          |

---

## Wave 2 - Adoption Path (Pilot Week 1)

### Q5. What is the week-1 pilot entry gate?

**Why this matters**
Pilots fail when entry criteria are fuzzy and teams onboard mismatched repositories.

**Options**

- A. One representative repo with stable CI and Sonar baseline.
- B. Two repos: one stable, one noisy, to prove robustness.
- C. One high-risk repo to maximize urgency and visibility.
- D. Entry gate not defined.

**Recommendation guidance / tradeoffs**
A is usually best for first paid pilot. B gives stronger proof but increases operational complexity.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                                  |
| ------ | -------------------------------------------------------------------------------------------------------------------------- |
| A      | Add pilot qualification checklist to [README.md](../../../README.md) and [STORIES.md](STORIES.md).                         |
| B      | Add dual-repo branching behavior in [workflows.md](workflows.md) and capacity notes in [architecture.md](architecture.md). |
| C      | Add risk controls and escalation criteria in [rules.md](rules.md) and [operations.md](operations.md).                      |
| D      | Keep pilot readiness as blocked in this interview doc and in [SPEC.md](SPEC.md).                                           |

### Q6. What is the default pilot operation mode?

**Why this matters**
The mode decision shapes trust, staffing expectations, and intervention frequency.

**Options**

- A. Assisted-first (human decisions at key gates).
- B. Autonomous-first with strict checkpoint controls.
- C. Hybrid (assisted in week 1, autonomous after proof).
- D. No default mode selected.

**Recommendation guidance / tradeoffs**
C is often strongest for commercialization: fast confidence gain with a clear autonomy progression path.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                           |
| ------ | ------------------------------------------------------------------------------------------------------------------- |
| A      | Prioritize assisted journey in [workflows.md](workflows.md) and acceptance criteria in [STORIES.md](STORIES.md).    |
| B      | Elevate autonomous safeguards in [rules.md](rules.md) and [operations.md](operations.md).                           |
| C      | Add explicit week-1 to month-1 mode transition in [workflows.md](workflows.md) and [README.md](../../../README.md). |
| D      | Mark unresolved operating model blocker in [SPEC.md](SPEC.md).                                                      |

### Q7. What pilot success evidence must exist by the end of week 1?

**Why this matters**
Week-1 success criteria are the bridge between evaluator enthusiasm and purchase confidence.

**Options**

- A. Quality gate progression + fallback evidence completeness.
- B. Remediation task export reliability + triage velocity.
- C. Operator control quality (pause/halt/resume with clean telemetry).
- D. Success metrics not yet selected.

**Recommendation guidance / tradeoffs**
Select one primary metric family and one secondary family. Overloaded scorecards hide weak outcomes.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                                 |
| ------ | ------------------------------------------------------------------------------------------------------------------------- |
| A      | Tighten governance KPI framing in [README.md](../../../README.md) and rule-level evidence fields in [rules.md](rules.md). |
| B      | Strengthen export lifecycle proofs in [operations.md](operations.md) and pilot stories in [STORIES.md](STORIES.md).       |
| C      | Strengthen mode-control telemetry requirements in [workflows.md](workflows.md) and [rules.md](rules.md).                  |
| D      | Add week-1 KPI definition task in [STORIES.md](STORIES.md).                                                               |

### Q8. What converts a pilot to a month-1 scale motion?

**Why this matters**
Without explicit conversion gates, pilots become prolonged trials instead of commercial progress.

**Options**

- A. Repeatable weekly loop with low manual rescue rate.
- B. Proven multi-repo portability with stable outputs.
- C. Governance/legal signoff on fallback and override controls.
- D. Conversion criteria unknown.

**Recommendation guidance / tradeoffs**
Use at least two conversion gates: one operational, one governance/compliance.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                              |
| ------ | ------------------------------------------------------------------------------------------------------ |
| A      | Add conversion threshold language in [README.md](../../../README.md) and [STORIES.md](STORIES.md).     |
| B      | Add scale path architecture assumptions to [architecture.md](architecture.md).                         |
| C      | Add explicit signoff evidence requirements in [rules.md](rules.md) and [operations.md](operations.md). |
| D      | Mark pilot-to-scale path as non-commercial-ready in [SPEC.md](SPEC.md).                                |

### Wave 2 Decision Capture

| QID | Selected Option | Evidence (quote/data)                                                                                        | Required doc updates done? | Owner | Due date |
| --- | --------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------- | ----- | -------- |
| Q5  | B               | Selected in interactive session: dual-repo pilot (one stable + one noisy) to prove robustness.               | No (pending sync)          |       |          |
| Q6  | A               | Selected in interactive session: assisted-first pilot mode for trust and control.                            | No (pending sync)          |       |          |
| Q7  | A               | Selected in interactive session: week-1 proof anchored on gate progression + fallback evidence completeness. | No (pending sync)          |       |          |
| Q8  | A               | Selected in interactive session: conversion gate is repeatable weekly loop with low manual rescue rate.      | No (pending sync)          |       |          |

---

## Wave 3 - Proof and Risk (Scale Month 1)

### Q9. What scale narrative is credible by month 1?

**Why this matters**
Commercial buyers need confidence that value is not limited to a single pilot repository.

**Options**

- A. Single-team, multi-repo standardization.
- B. Cross-team governance model with shared policy contracts.
- C. Portfolio-level trend and quality governance dashboarding.
- D. Scale narrative still unclear.

**Recommendation guidance / tradeoffs**
Choose the smallest scale claim you can prove quickly. Over-claiming scale is a common deal-breaker.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                  |
| ------ | ---------------------------------------------------------------------------------------------------------- |
| A      | Emphasize repeatability claims in [README.md](../../../README.md) and [workflows.md](workflows.md).        |
| B      | Strengthen policy portability constraints in [rules.md](rules.md) and [architecture.md](architecture.md).  |
| C      | Elevate telemetry-driven governance position in [architecture.md](architecture.md) and [SPEC.md](SPEC.md). |
| D      | Keep month-1 scale claims out of [README.md](../../../README.md).                                          |

### Q10. Which proof package addresses the hardest month-1 buyer risk?

**Why this matters**
Scale decisions are risk decisions; your proof package must directly answer risk, not just show activity.

**Options**

- A. Governance proof: fallback + override validity + completion gate traces.
- B. Throughput proof: issue bundling, export states, and closure velocity.
- C. Reliability proof: bounded retries, deterministic failures, and resumability.
- D. No proof package selected.

**Recommendation guidance / tradeoffs**
Governance-heavy buyers prefer A. Delivery-focused buyers prefer B. Regulated teams often require A + C.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                                        |
| ------ | -------------------------------------------------------------------------------------------------------------------------------- |
| A      | Strengthen governance evidence map in [rules.md](rules.md), [operations.md](operations.md), and [README.md](../../../README.md). |
| B      | Strengthen throughput/value narrative in [README.md](../../../README.md) and lifecycle detail in [operations.md](operations.md). |
| C      | Strengthen deterministic failure/restore messaging in [workflows.md](workflows.md) and [architecture.md](architecture.md).       |
| D      | Add a scale-proof definition task in [STORIES.md](STORIES.md).                                                                   |

### Q11. What integration posture is required for scale purchase confidence?

**Why this matters**
At scale, integration friction is purchase friction.

**Options**

- A. GitHub API-first is enough for initial scale.
- B. GitHub + Jira parity is required.
- C. API + custom enterprise adapter extension path is required.
- D. Integration posture unresolved.

**Recommendation guidance / tradeoffs**
If enterprise sales are a target, B is usually minimum. C is strong but only if adapter boundaries are crisp.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                           |
| ------ | ------------------------------------------------------------------------------------------------------------------- |
| A      | Keep GitHub-first pathway primary in [README.md](../../../README.md) and [operations.md](operations.md).            |
| B      | Elevate dual-export parity and failure handling in [operations.md](operations.md) and [workflows.md](workflows.md). |
| C      | Add extension boundary and ownership notes in [architecture.md](architecture.md) and [SPEC.md](SPEC.md).            |
| D      | Mark commercialization integration risk in this interview log and [SPEC.md](SPEC.md).                               |

### Q12. Which month-1 business outcome is the flagship proof for buyers?

**Why this matters**
Month-1 commercialization needs one clear business outcome buyers can repeat internally.

**Options**

- A. Faster remediation cycle completion.
- B. Lower escaped-quality risk.
- C. Higher operator throughput with governed controls.
- D. Business outcome not yet quantified.

**Recommendation guidance / tradeoffs**
Pick one flagship KPI and one supporting KPI. Keep the headline stable across demos, docs, and pilot reports.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                         |
| ------ | ----------------------------------------------------------------------------------------------------------------- |
| A      | Reframe value proposition in [README.md](../../../README.md) and acceptance criteria in [STORIES.md](STORIES.md). |
| B      | Reframe risk-governance value in [README.md](../../../README.md) and [rules.md](rules.md).                        |
| C      | Reframe operational leverage value in [README.md](../../../README.md) and [workflows.md](workflows.md).           |
| D      | Add KPI-definition dependency and block packaging claims in Wave 4.                                               |

### Wave 3 Decision Capture

| QID | Selected Option | Evidence (quote/data)                                                                                                    | Required doc updates done? | Owner | Due date |
| --- | --------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------- | ----- | -------- |
| Q9  | A               | Selected in interactive session: month-1 scale claim is single-team, multi-repo standardization.                         | No (pending sync)          |       |          |
| Q10 | A               | Selected in interactive session: governance proof package is the primary month-1 risk answer.                            | No (pending sync)          |       |          |
| Q11 | A               | Selected in interactive session: GitHub API-first posture is sufficient for initial scale claim.                         | No (pending sync)          |       |          |
| Q12 | C               | Selected in interactive session: flagship month-1 business outcome is higher operator throughput with governed controls. | No (pending sync)          |       |          |

---

## Wave 4 - Packaging, Pricing, and Ongoing Operator Journey

### Q13. What product packaging best matches the buyer journey you just defined?

**Why this matters**
Packaging must match adoption reality. Misaligned packaging increases churn and weakens perceived value.

**Options**

- A. Docs/spec product with implementation optionality.
- B. Guided implementation accelerator package.
- C. Managed quality-loop service package.
- D. Packaging still undefined.

**Recommendation guidance / tradeoffs**
For repository sale narrative, B is often strongest: concrete outcome with controlled delivery scope.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                       |
| ------ | --------------------------------------------------------------------------------------------------------------- |
| A      | Position as governance blueprint in [README.md](../../../README.md) and scope guardrails in [SPEC.md](SPEC.md). |
| B      | Add adoption playbook path in [README.md](../../../README.md) and journey stories in [STORIES.md](STORIES.md).  |
| C      | Add operating responsibilities and controls in [workflows.md](workflows.md) and [rules.md](rules.md).           |
| D      | Mark monetization path unresolved and block pricing commitments.                                                |

### Q14. What pricing axis aligns with buyer value and operator behavior?

**Why this matters**
Pricing that does not match value realization leads to stalled procurement and difficult renewals.

**Options**

- A. Per repository under governance.
- B. Per active cycle/pass volume band.
- C. Per operator seat with included repo allowance.
- D. Pricing axis unknown.

**Recommendation guidance / tradeoffs**
Per-repo is easiest to explain. Cycle-volume can align with value but may feel variable/risky to buyers.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                               |
| ------ | ------------------------------------------------------------------------------------------------------- |
| A      | Align commercialization narrative in [README.md](../../../README.md) with repo-scope outcomes.          |
| B      | Add cycle economics assumptions to [SPEC.md](SPEC.md) and operator stories in [STORIES.md](STORIES.md). |
| C      | Add role/seat usage assumptions to [STORIES.md](STORIES.md) and [operations.md](operations.md).         |
| D      | Keep pricing out of external buyer narrative until validated.                                           |

### Q15. What defines a healthy ongoing operator journey after month 1?

**Why this matters**
Commercial success requires renewal confidence. Renewal confidence comes from predictable ongoing operations.

**Options**

- A. Weekly governed loop with low intervention and clear checkpoint outcomes.
- B. Weekly loop plus monthly policy tuning and risk review.
- C. Continuous loop with operator escalation only on anomalies.
- D. Ongoing operator model not yet defined.

**Recommendation guidance / tradeoffs**
B is usually strongest for enterprise trust: routine execution plus explicit governance review rhythm.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                                                          |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| A      | Add steady-state weekly runbook framing in [workflows.md](workflows.md) and [README.md](../../../README.md).                       |
| B      | Add recurring governance checkpoints in [rules.md](rules.md), [operations.md](operations.md), and [README.md](../../../README.md). |
| C      | Add anomaly-driven controls and telemetry reliance in [architecture.md](architecture.md) and [workflows.md](workflows.md).         |
| D      | Mark renewal narrative as incomplete and keep sales claims conservative.                                                           |

### Q16. What is the expansion path after initial commercialization win?

**Why this matters**
Expansion logic affects both pricing strategy and investor/buyer narrative strength.

**Options**

- A. Land one repo, expand to adjacent repos in same team.
- B. Land one team, expand to platform-wide governance standard.
- C. Land governance use case, expand into broader delivery intelligence workflows.
- D. Expansion path unclear.

**Recommendation guidance / tradeoffs**
A is fastest to prove; B usually yields stronger account growth; C can be powerful but requires a broader roadmap.

**Artifact impact by answer**

| Option | Update this artifact/view                                                                              |
| ------ | ------------------------------------------------------------------------------------------------------ |
| A      | Emphasize repeatable replication play in [README.md](../../../README.md) and [STORIES.md](STORIES.md). |
| B      | Emphasize standardization architecture in [architecture.md](architecture.md) and [SPEC.md](SPEC.md).   |
| C      | Add roadmap assumptions and boundary notes in [SPEC.md](SPEC.md) and [workflows.md](workflows.md).     |
| D      | Add explicit expansion hypothesis and experiment in [STORIES.md](STORIES.md).                          |

### Wave 4 Decision Capture

| QID | Selected Option | Evidence (quote/data)                                                                                   | Required doc updates done? | Owner | Due date |
| --- | --------------- | ------------------------------------------------------------------------------------------------------- | -------------------------- | ----- | -------- |
| Q13 | A               | User asked for A + B; canonical primary locked to A, with B retained as secondary packaging intent.     | No (pending sync)          |       |          |
| Q14 | A               | User prefers one-time purchase (non-SaaS); mapped to per-repository axis with one-time packaging terms. | No (pending sync)          |       |          |
| Q15 | A               | Selected in interactive session: healthy ongoing journey is weekly governed loop with low intervention. | No (pending sync)          |       |          |
| Q16 | A               | Selected in interactive session: expansion is land one repo then expand to adjacent repos in same team. | No (pending sync)          |       |          |

---

## Cross-Wave Decision Ledger (single source of truth)

| Theme                  | Final Decision                                                                                                                                     | Evidence strength (High/Med/Low) | Blockers remaining                                 | Artifact links updated                                       |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| Buyer and trigger      | Q1=A primary buyer anchor (engineering leadership) with broader educational audience as secondary messaging.                                       | Med                              | None                                               | [README.md](../../../README.md), [STORIES.md](STORIES.md)    |
| Day-1 value narrative  | Q3=B: day-1 proof is actionable finding bundles exported into remediation tasks.                                                                   | High                             | None                                               | [README.md](../../../README.md), [SPEC.md](SPEC.md)          |
| Pilot motion           | Q5=B, Q6=A, Q7=A, Q8=A: dual-repo pilot, assisted-first mode, governance evidence week-1 KPI, conversion via repeatable low-rescue loop.           | Med                              | None                                               | [workflows.md](workflows.md), [operations.md](operations.md) |
| Scale proof package    | Q9=A, Q10=A, Q11=A, Q12=C: single-team multi-repo claim with governance proof package, GitHub-first integration, operator-throughput flagship KPI. | Med                              | Validate Jira parity timing for enterprise segment | [rules.md](rules.md), [architecture.md](architecture.md)     |
| Packaging and pricing  | Q13=A primary with B secondary intent; Q14=A mapped to one-time per-repository purchase model (non-SaaS).                                          | Med                              | Validate willingness-to-pay and package boundaries | [README.md](../../../README.md), [SPEC.md](SPEC.md)          |
| Ongoing operator model | Q15=A and Q16=A: weekly governed cadence and repo-by-repo expansion path.                                                                          | High                             | None                                               | [workflows.md](workflows.md), [rules.md](rules.md)           |

## Convergence Criteria (when the view is nailed)

The user-journey view is considered **nailed** only when all criteria below are true.

### Evaluator day 0-1 nailed

- Primary buyer and trigger are explicit (no `D` on Q1).
- Day-0 maturity assumption is explicit and documented (no `D` on Q2).
- One headline day-1 value moment is selected and reflected in [README.md](../../../README.md).
- Top objection has a concrete evidence response path tied to [rules.md](rules.md) and/or [operations.md](operations.md).

### Pilot week 1 nailed

- Pilot entry gate is explicit and testable.
- Default operation mode is selected with tradeoff acknowledged.
- Week-1 success evidence is measurable and mapped into [STORIES.md](STORIES.md).
- Pilot-to-scale conversion gate is explicit and non-ambiguous.

### Scale month 1 nailed

- Scale claim is realistic and supported by one clear proof package.
- Integration posture is explicit (GitHub/Jira/extension) with architecture implications captured.
- One flagship business KPI is selected and appears in commercialization narrative.

### Ongoing operator journey nailed

- Steady-state cadence is clear (weekly/monthly control rhythm).
- Operator intervention expectations are explicit.
- Renewal and expansion logic are clear enough to support packaging/pricing decisions.

### Final gate (all waves)

- No unresolved blocker from Waves 1-3.
- No more than one `D` answer across all 16 questions.
- All "Required doc updates done?" cells are complete.
- Core narrative is internally consistent across [README.md](../../../README.md), [SPEC.md](SPEC.md), [STORIES.md](STORIES.md), [workflows.md](workflows.md), [operations.md](operations.md), [rules.md](rules.md), and [architecture.md](architecture.md).

## Suggested Facilitation Cadence

- Wave 1: 20 minutes
- Wave 2: 20 minutes
- Wave 3: 20 minutes
- Wave 4: 15 minutes
- Convergence review: 10 minutes

If convergence fails, rerun only the failed wave after targeted evidence collection.
