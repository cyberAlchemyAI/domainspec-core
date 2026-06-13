# Research Strategy - Capital Logic Library

## Dispatch Spec Result

- Dispatch ID: `gq-research-strategy-capital-logic-library-2026-06-12`
- Status: `pass`
- Mode: `research`
- Step count: 6
- Patterns: `sequential`, `decision`, `validation`, `synthesis`
- Gates: local-first evidence, external approval, org isolation, claim-evidence validation, owner boundary
- Handoffs: local evidence frame -> research lane map -> external approval decision -> validation ledger -> synthesis handoff
- Subagent strategy: `recommended`, roles `local-evidence-reviewer`, `external-boundary-reviewer`, `claim-validation-reviewer`, join policy `parent_synthesis`, authorization `requires_user_permission`
- Subagent lifecycle: `none`; no agents spawned
- Observability: grouped by `gq-research-strategy-capital-logic-library-2026-06-12`
- Promotion guardrail: research strategy is planning evidence only
- Required repairs: none
- Next route: `refine`

## Node

- Craft node: `capital-logic-library`
- Title: Capital Logic Library
- Research lane: Capital Logic Library research
- Strategy route: `RESEARCH-DISPATCH.json`
- Existing Refine route: `REFINE-DISPATCH.json`

## Core Research Question

What source universes, expert inputs, card schema evidence, and rule-pack boundaries are needed to hydrate launch cards safely?

## Local Evidence Boundary

Research starts local-first. Use these evidence classes before any external lookup:

- existing promotion-governance Craft ledger
- workbook Capital Logic rows
- card/schema governance docs

## Active Local Gaps

- `GAP-CLL-LAUNCH-CARDS` (flag): Five launch cards need current authoring and validation status captured.
- `GAP-CLL-DOMAIN-EXPERTS` (block): Four segment experts need scoped paid structured input.
- `GAP-CLL-RULE-PACKS` (flag): Recurring funder rule packs need ownership and ongoing maintenance shape.

## External Evidence Classes

External research is not executed by this strategy. If local evidence leaves a named gap and Josh confirms the route, the bounded external classes are:

- segment source universe lists
- recurring funder rule references
- paid expert input requirements after approval

## Validation Focus

card schema, five launch cards, expert-review gaps, source universe boundaries, and no silent promotion into canonical governance

## Research Steps

1. Scope the node-specific research question and reject cross-node drift.
2. Build a local evidence baseline from Craft, workbook, and Golden Quill project sources.
3. Map research lanes and select local-only, gap-triggered external, or deferred research.
4. Ask for external-research approval when a named gap requires outside comparison.
5. Validate claims against source class, path or handle expectation, and owner boundary.
6. Hand off findings to the node's Refine route and Invoke first-artifact direction.

## Execution Boundary

No external research, subagents, or runtime-backed stages have run. This strategy becomes executable only after Josh confirms the dispatch route.
