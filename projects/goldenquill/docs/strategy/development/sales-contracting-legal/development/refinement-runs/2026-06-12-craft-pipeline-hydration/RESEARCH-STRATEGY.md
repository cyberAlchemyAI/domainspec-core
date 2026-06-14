# Research Strategy - Sales, contracting, and legal

## Dispatch Spec Result

- Dispatch ID: `gq-research-strategy-sales-contracting-legal-2026-06-12`
- Status: `pass`
- Mode: `research`
- Step count: 6
- Patterns: `sequential`, `decision`, `validation`, `synthesis`
- Gates: local-first evidence, external approval, org isolation, claim-evidence validation, owner boundary
- Handoffs: local evidence frame -> research lane map -> external approval decision -> validation ledger -> synthesis handoff
- Subagent strategy: `recommended`, roles `local-evidence-reviewer`, `external-boundary-reviewer`, `claim-validation-reviewer`, join policy `parent_synthesis`, authorization `requires_user_permission`
- Subagent lifecycle: `none`; no agents spawned
- Observability: grouped by `gq-research-strategy-sales-contracting-legal-2026-06-12`
- Promotion guardrail: research strategy is planning evidence only
- Required repairs: none
- Next route: `refine`

## Node

- Craft node: `sales-contracting-legal`
- Title: Sales, contracting, and legal
- Research lane: sales, contracting, and legal research
- Strategy route: `RESEARCH-DISPATCH.json`
- Existing Refine route: `REFINE-DISPATCH.json`

## Core Research Question

What legal, sales, qualification, disclosure, insurance, deposit, and invoicing evidence is needed before the first LOI or customer agreement?

## Local Evidence Boundary

Research starts local-first. Use these evidence classes before any external lookup:

- workbook sales rows
- Golden Quill sovereignty promise
- locked BYOK/customer data boundaries

## Active Local Gaps

- `GAP-SCL-SALES-MATERIALS` (flag): One-pager, demo, segment framing, and pipeline tracker need claims-register evidence before use.
- `GAP-SCL-LEGAL-FIRST-LOI` (block): Legal, LOI, data policy, procurement language, and insurance are onboard-now before first LOI signs.
- `GAP-SCL-DEPOSIT-INVOICING` (flag): Deposit handling, invoicing, and cost tracking need bookkeeper trigger at first revenue.

## External Evidence Classes

External research is not executed by this strategy. If local evidence leaves a named gap and Josh confirms the route, the bounded external classes are:

- fractional legal scope
- AI/data-policy language patterns
- procurement and insurance checklist references
- only after approval

## Validation Focus

legal-first gates, disclosure rules, customer agreement dependencies, data-policy terms, and first-revenue finance handoff

## Research Steps

1. Scope the node-specific research question and reject cross-node drift.
2. Build a local evidence baseline from Craft, workbook, and Golden Quill project sources.
3. Map research lanes and select local-only, gap-triggered external, or deferred research.
4. Ask for external-research approval when a named gap requires outside comparison.
5. Validate claims against source class, path or handle expectation, and owner boundary.
6. Hand off findings to the node's Refine route and Invoke first-artifact direction.

## Execution Boundary

No external research, subagents, or runtime-backed stages have run. This strategy becomes executable only after Josh confirms the dispatch route.
