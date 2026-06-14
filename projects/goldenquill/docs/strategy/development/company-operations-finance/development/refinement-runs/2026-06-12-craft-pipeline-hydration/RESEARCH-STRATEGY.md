# Research Strategy - Company operations and finance

## Dispatch Spec Result

- Dispatch ID: `gq-research-strategy-company-operations-finance-2026-06-12`
- Status: `pass`
- Mode: `research`
- Step count: 6
- Patterns: `sequential`, `decision`, `validation`, `synthesis`
- Gates: local-first evidence, external approval, org isolation, claim-evidence validation, owner boundary
- Handoffs: local evidence frame -> research lane map -> external approval decision -> validation ledger -> synthesis handoff
- Subagent strategy: `recommended`, roles `local-evidence-reviewer`, `external-boundary-reviewer`, `claim-validation-reviewer`, join policy `parent_synthesis`, authorization `requires_user_permission`
- Subagent lifecycle: `none`; no agents spawned
- Observability: grouped by `gq-research-strategy-company-operations-finance-2026-06-12`
- Promotion guardrail: research strategy is planning evidence only
- Required repairs: none
- Next route: `refine`

## Node

- Craft node: `company-operations-finance`
- Title: Company operations and finance
- Research lane: company operations and finance research
- Strategy route: `RESEARCH-DISPATCH.json`
- Existing Refine route: `REFINE-DISPATCH.json`

## Core Research Question

What operating-floor evidence is needed for entity hygiene, bookkeeping, support triage, Node Care, and validation packet maintenance?

## Local Evidence Boundary

Research starts local-first. Use these evidence classes before any external lookup:

- workbook operations rows
- Golden Quill business constraints
- current Craft ledgers

## Active Local Gaps

- `GAP-COF-ENTITY-HYGIENE` (flag): Entity hygiene, banking, bookkeeping, filing, and insurance need operating checklist.
- `GAP-COF-SUPPORT-TRIAGE` (block): Support channel, issue log, and triage rules need boundaries for support absorbs vs engineering sees.
- `GAP-COF-NODE-CARE-OPS` (flag): Node Care updates, source-index maintenance, quarterly check-ins, and vault care need operating cadence.
- `GAP-COF-VALIDATION-PACKET` (flag): Investor/funder relations and validation packet maintenance need evidence ownership.

## External Evidence Classes

External research is not executed by this strategy. If local evidence leaves a named gap and Josh confirms the route, the bounded external classes are:

- basic bookkeeping cadence references
- support triage patterns
- only after approval

## Validation Focus

first-revenue setup, ongoing support ownership, issue log routing, Node Care ops, and validation packet cadence

## Research Steps

1. Scope the node-specific research question and reject cross-node drift.
2. Build a local evidence baseline from Craft, workbook, and Golden Quill project sources.
3. Map research lanes and select local-only, gap-triggered external, or deferred research.
4. Ask for external-research approval when a named gap requires outside comparison.
5. Validate claims against source class, path or handle expectation, and owner boundary.
6. Hand off findings to the node's Refine route and Invoke first-artifact direction.

## Execution Boundary

No external research, subagents, or runtime-backed stages have run. This strategy becomes executable only after Josh confirms the dispatch route.
