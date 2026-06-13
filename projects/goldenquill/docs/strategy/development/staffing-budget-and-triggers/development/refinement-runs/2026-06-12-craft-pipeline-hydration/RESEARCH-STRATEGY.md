# Research Strategy - Staffing, budget, and triggers

## Dispatch Spec Result

- Dispatch ID: `gq-research-strategy-staffing-budget-and-triggers-2026-06-12`
- Status: `pass`
- Mode: `research`
- Step count: 6
- Patterns: `sequential`, `decision`, `validation`, `synthesis`
- Gates: local-first evidence, external approval, org isolation, claim-evidence validation, owner boundary
- Handoffs: local evidence frame -> research lane map -> external approval decision -> validation ledger -> synthesis handoff
- Subagent strategy: `recommended`, roles `local-evidence-reviewer`, `external-boundary-reviewer`, `claim-validation-reviewer`, join policy `parent_synthesis`, authorization `requires_user_permission`
- Subagent lifecycle: `none`; no agents spawned
- Observability: grouped by `gq-research-strategy-staffing-budget-and-triggers-2026-06-12`
- Promotion guardrail: research strategy is planning evidence only
- Required repairs: none
- Next route: `refine`

## Node

- Craft node: `staffing-budget-and-triggers`
- Title: Staffing, budget, and triggers
- Research lane: staffing and budget trigger research
- Strategy route: `RESEARCH-DISPATCH.json`
- Existing Refine route: `REFINE-DISPATCH.json`

## Core Research Question

What hours, rates, role triggers, and onboarding order are needed to turn role rows into budgetable execution state?

## Local Evidence Boundary

Research starts local-first. Use these evidence classes before any external lookup:

- workbook roles and gaps
- Craft gaps
- Golden Quill first-node assumptions

## Active Local Gaps

- `GAP-SBT-HOURS-RATES` (block): Est. Hrs and Notes / Rate are blank; budget cannot be computed.
- `GAP-SBT-ONBOARD-NOW` (flag): Domain Experts, Legal, and Security Reviewer are onboard-now/near-now roles that need procurement shape and cost.
- `GAP-SBT-ONBOARD-LATER` (flag): Customer Success and Field Tech handoff from Josh/engineers needs deployed-node trigger criteria.

## External Evidence Classes

External research is not executed by this strategy. If local evidence leaves a named gap and Josh confirms the route, the bounded external classes are:

- fractional legal/security/bookkeeping rate ranges
- hardware install/support labor benchmarks
- only after Josh approves bounded comparison

## Validation Focus

blank hours/rates, trigger thresholds, onboard-now vs onboard-later evidence, and budget acceptance criteria

## Research Steps

1. Scope the node-specific research question and reject cross-node drift.
2. Build a local evidence baseline from Craft, workbook, and Golden Quill project sources.
3. Map research lanes and select local-only, gap-triggered external, or deferred research.
4. Ask for external-research approval when a named gap requires outside comparison.
5. Validate claims against source class, path or handle expectation, and owner boundary.
6. Hand off findings to the node's Refine route and Invoke first-artifact direction.

## Execution Boundary

No external research, subagents, or runtime-backed stages have run. This strategy becomes executable only after Josh confirms the dispatch route.
