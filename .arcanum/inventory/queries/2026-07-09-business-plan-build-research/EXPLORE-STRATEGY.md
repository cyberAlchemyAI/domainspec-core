---
tags: [inventory, strategy-result, dispatch, subagents, research, investor-bp, business-plan, claim-le-proof, public-private-boundary]
node_type: research-strategy
is_session: false
layer: strategy
nature: proposal
status: proposed
created: 2026-07-09
dispatch_id: 2026-07-09-business-plan-build-research
dispatch_type: research
---

# Business Plan Build Research Strategy

## P1 Trigger Decision

Dispatch is justified.

- **Synthesis:** the research must combine external business-plan / investor-plan practice, startup financial model practice, and the existing DomainSpec/CAV2 BP substrates.
- **Context protection:** raw source returns will be much larger than the parent should carry.
- **Isolation:** external BP advice and internal evidence mapping should be independently inspectable before synthesis.
- **Parallelism:** external structure, financial modeling, GTM/adoption, and DomainSpec evidence mapping can run concurrently.

## Goal

Create the research substrate for building the later investor business plan: what a strong business plan should contain, how investor-facing and lender/operating-plan variants differ, what financial/market/GTM evidence is required, and how to map the accepted DomainSpec/CAV2 substrates into a credible BP without overclaiming.

## Source Boundary

### Internal accepted sources

- `.arcanum/inventory/queries/2026-07-06-investor-bp-project-portfolio-research/findings.md`
- `.arcanum/inventory/queries/2026-07-06-ai-assurance-certification-vocabulary-research/findings.md`
- `.arcanum/inventory/queries/2026-07-06-spec-driven-completeness-moat-inventory-research/findings.md`
- `.arcanum/inventory/queries/2026-07-06-novel-model-use-lean-formalization-research/findings.md`
- `.arcanum/inventory/queries/2026-07-06-investor-pitch-blind-spot-review-revised/findings.md`
- `.arcanum/inventory/index.json`
- `.arcanum/inventory/index.md`
- `telemetry/agents/subagents-dispatch.yaml`

### External seed sources

- U.S. SBA, `Write your business plan`: traditional vs lean plans, market analysis, funding request, financial projections, appendix.
- SCORE, `Business Planning & Financial Statements Template Gallery`: templates for business planning, financial statements, sales, marketing, and operations.
- Y Combinator, `How to build your seed round pitch deck` and seed fundraising material: venture-facing pitch/story constraints.
- Sequoia Capital, `Writing a Business Plan`: company purpose, problem, solution, why now, market, competition, business model, team, financials, vision.
- HubSpot for Startups, `Financial Projections Template`: financial projections, sales forecasts, expense budget, cash flow, income statement, balance sheet, break-even analysis.

External sources are current-source pressure, not authority over local claims. The writer must date external market/investor guidance and mark anything time-sensitive for refresh.

## Required Findings Shape

The final `findings.md` must include:

1. **Business-plan anatomy:** what sections a strong BP needs, split by investor deck, traditional financing plan, and internal operating/data-room plan.
2. **Build sequence:** the order in which we should write the BP, including evidence-gathering before prose.
3. **DomainSpec/CAV2 mapping:** which accepted substrate claims belong in executive summary, problem, solution, product, market, GTM, defensibility, team, financials, risks, and appendix.
4. **Metric Trust wedge model:** first ICP, buyer pain, offer shape, pricing hypotheses, pilot package, proof/falsifier gates, and expansion path.
5. **Financial model checklist:** revenue streams, cost drivers, headcount, gross margin assumptions, unit economics, runway, use of funds, scenario model, and sensitivity tests.
6. **Diligence/data-room checklist:** artifacts, proof receipts, maturity table, non-claims box, source links, buyer-validation plan, and next witnesses.
7. **Investor-safe language:** allowed phrases, demoted phrases, forbidden claims, and claim <= proof mapping.
8. **Verdict matrix:** each BP section with owner/source evidence, missing witness, and whether it is ready now, needs validation, or must stay future-only.

## Lanes / Groups

### Group 1: `external-framework-explorers`

- **Purpose:** map how high-quality business plans are structured across SBA/traditional, venture/seed, financial-model, and adoption/GTM frames.
- **Role:** explorer.
- **Runs:** parallel with robot-talks.
- **Anti-bias axis:** composite source-corpus + methodology + temporal-prior.
- **Predicted disagreements:**
  - Drucker vs Porter: Drucker runs lender/operating-plan completeness, Porter runs venture/investor compression; Drucker will expose missing operational substance, Porter will expose investor-story bloat.
  - Drucker vs Goldratt: Drucker asks what sections must exist, Goldratt asks what assumptions make the plan executable; Goldratt exposes prose without numbers, Drucker exposes numbers without business narrative.
  - Drucker vs Christensen: Drucker treats the BP as management system, Christensen treats it as adoption path; Christensen exposes organization-first plans that do not win a beachhead.
  - Porter vs Goldratt: Porter optimizes for investor salience, Goldratt for constraint/accounting realism; Goldratt exposes fundraising theater, Porter exposes spreadsheet burying the pitch.
  - Porter vs Christensen: Porter asks why investors believe the market can be won, Christensen asks how the first adoption pocket actually starts; Christensen exposes TAM-first abstractions.
  - Goldratt vs Christensen: Goldratt asks whether the model closes economically, Christensen asks whether demand can start in one job-to-be-done; each exposes the other's untested assumption.

### Group 2: `domain-substrate-explorers`

- **Purpose:** map the accepted DomainSpec/CAV2 evidence into a BP-ready substrate without claim inflation.
- **Role:** explorer.
- **Runs:** parallel with robot-talks.
- **Anti-bias axis:** composite source-corpus + methodology.
- **Predicted disagreements:**
  - Beer vs Shannon: Beer reads the company as a viable system and compounding machine, Shannon reads the inventory as source/index evidence; Shannon exposes uncited system claims, Beer exposes atomized evidence that loses the company story.
  - Beer vs Turing: Beer emphasizes operating system/reach, Turing emphasizes formal/evidence/proof boundaries; Turing exposes overproof, Beer exposes under-positioning.
  - Beer vs Ashby: Beer asks what the company is becoming, Ashby asks what control loops and feedback channels keep it viable; Ashby exposes strategy without regulation.
  - Shannon vs Turing: Shannon inventories sources and maturity labels, Turing classifies proof/readiness witnesses; Turing exposes source mentions that are not proof, Shannon exposes proof claims missing source anchors.
  - Shannon vs Ashby: Shannon traces artifacts, Ashby traces controls and owner decisions; each exposes missing lineage/control evidence.
  - Turing vs Ashby: Turing looks for named checks and bounded formal witnesses, Ashby looks for governance-control sufficiency; Ashby exposes proof objects that do not regulate use, Turing exposes governance claims without validators.

### Group 3: `synthesizer`

- **Purpose:** reconcile external BP architecture with internal DomainSpec evidence into a candidate BP-building method and section map.
- **Role:** synthesizer.
- **Runs:** after both explorer groups.
- **Output expectation:** candidate BP anatomy, build sequence, claim ladder, financial model outline, data-room checklist, and open gaps.

### Group 4: `reviewers`

- **Purpose:** attack the synthesis before writing.
- **Role:** skeptic.
- **Runs:** after synthesizer, with zig-zag and robot-talks.
- **Anti-bias axis:** attack-vector.
- **Predicted disagreements:**
  - Taleb vs Popper: Taleb attacks fragility and non-vacuity, Popper attacks falsifiability and next witness; Taleb exposes hidden downside, Popper exposes claims with no failure test.
  - Taleb vs Quine: Taleb attacks fragile assumptions and optionality theater, Quine attacks semantic collapse; Taleb exposes unsupported economics, Quine exposes overloaded words like platform, proof, market, wedge, readiness.
  - Popper vs Quine: Popper demands falsifiers for each BP claim, Quine demands definitions for each claim term; Popper exposes unfalsifiable narratives, Quine exposes ambiguous ones.

### Group 5: `writer`

- **Purpose:** write `findings.md` only.
- **Role:** writer.
- **Runs:** after reviewer zig-zag converges.
- **Output expectation:** cited BP-building research substrate with verdict matrix, not final BP prose.

### Group 6: `auditor`

- **Purpose:** final approval of `findings.md`.
- **Role:** auditor.
- **Runs:** after writer; may send one bounded revision back to writer.
- **Output expectation:** ACCEPT or REVISE. Must fail uncited claims, missing external/current source coverage, missing financial model section, missing DomainSpec mapping, missing non-claims, or claim > proof.

## Subagents

| Group | Agent | Role | Angle | Expected output |
|---|---|---|---|---|
| external-framework-explorers | Drucker, Peter | explorer | Traditional/operating/lender BP architecture from SBA/SCORE and management practice. | Section map, completeness checklist, audience variants, operating-plan obligations. |
| external-framework-explorers | Porter, Michael | explorer | Venture/investor plan and deck logic from YC/Sequoia/current investor sources. | Investor narrative map, market/competition/GTM requirements, what belongs in deck vs BP. |
| external-framework-explorers | Goldratt, Eliyahu | explorer | Financial model, constraints, unit economics, capacity, use-of-funds realism. | Financial model checklist, assumptions, scenarios, constraints, sensitivity tests. |
| external-framework-explorers | Christensen, Clayton | explorer | Beachhead adoption, wedge selection, consulting-to-product path. | First-market logic, adoption tests, expansion gates, GTM sequencing. |
| domain-substrate-explorers | Beer, Stafford | explorer | Company system and compounding reach from accepted BP substrates. | Company-system map and how POCs compound into a BP story without overclaiming. |
| domain-substrate-explorers | Shannon, Claude | explorer | Inventory/source evidence and maturity accounting. | Source coverage table, evidence-to-section map, data-room appendix plan. |
| domain-substrate-explorers | Turing, Alan | explorer | Proof/readiness/verification boundaries. | Claim/proof ladder, safe verifiable/provable language, proof object gaps. |
| domain-substrate-explorers | Ashby, W. Ross | explorer | Governance, control loops, owner decisions, operating model. | Operating system map, KPI/control loop plan, risks and governance mechanisms. |
| synthesizer | Simon, Herbert | synthesizer | Reconcile external structure and internal substrate. | Candidate BP-building blueprint and gap map. |
| reviewers | Taleb, Nassim Nicholas | skeptic | Non-vacuity / fragility gate. | REVISE/DROP/ACCEPT by claim; fragile assumptions and exact witnesses. |
| reviewers | Popper, Karl | skeptic | Falsifiability / next-witness gate. | Demotion conditions, missing decisive tests, validation gates. |
| reviewers | Quine, Willard Van Orman | skeptic | Definitional-soundness gate. | Term repairs, forbidden phrases, non-collapse checks. |
| writer | Grove, Andrew | writer | Persist actionable BP-building findings. | `findings.md` with section map, build sequence, claim ladder, financial model, data-room checklist, verdict matrix. |
| auditor | Brandenburg, Martin | auditor | Final coverage and claim-boundary audit. | ACCEPT/REVISE with exact fixes. |

## Dependency Flow

- `external-framework-explorers -> synthesizer`: sequential.
- `domain-substrate-explorers -> synthesizer`: sequential.
- `synthesizer -> reviewers`: zig-zag, `loop_cap: 1`.
- `synthesizer -> external-framework-explorers`: feedback, `loop_cap: 1`, only if material external BP coverage is missing.
- `synthesizer -> domain-substrate-explorers`: feedback, `loop_cap: 1`, only if internal source/evidence mapping is missing.
- `reviewers -> writer`: sequential after reviewer reconciliation.
- `writer -> auditor`: sequential.
- `auditor -> writer`: feedback, `loop_cap: 1`, for bounded revisions.

## Gate / Ledger State

- Check-tension: double PASS.
  - Checker: `019f4567-f45c-7732-a645-353ce6d5fca8` (Mendel) - PASS.
  - Reviewer: `019f4567-f4e2-7992-9df0-d9e79bc741ee` (Hilbert) - PASS.
  - Note: the reviewer flagged role vocabulary only as a non-blocking wording nuance. This sheet uses `explorer`/`skeptic` because the dispatch schema and rubric support those role classes; the gate's `investigate`/`evaluate` wording is treated as an alias pressure, not a failure.
- Human confirmation: required before registration and runtime.
- Registration: unregistered. Do not append ledger row until explicit `confirmed`.
- Closeout expectation: after confirmed run, append dispatch row, run groups by dependency, close all agents, append close row, then add `research.md` and `findings.md` inventory records and update this strategy-result read model.

## Next Human Action

After the check-tension gate double-PASSes, reply `confirmed` to register and run, or request edits to the strategy.

## Non-Goals

- This run does not write the final business plan.
- This run does not create investor-facing claims.
- This run does not make certification/compliance/agent-correctness claims.
- This run does not treat external BP templates as proof that our claims are ready.
