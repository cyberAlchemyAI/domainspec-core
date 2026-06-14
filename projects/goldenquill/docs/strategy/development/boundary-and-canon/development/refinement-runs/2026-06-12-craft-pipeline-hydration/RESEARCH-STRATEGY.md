# Research Strategy - Boundary and canon

## Dispatch Spec Result

- Dispatch ID: `gq-research-strategy-boundary-and-canon-2026-06-12`
- Status: `pass`
- Mode: `research`
- Step count: 6
- Patterns: `sequential`, `decision`, `validation`, `synthesis`
- Gates: local-first evidence, external approval, org isolation, claim-evidence validation, owner boundary
- Handoffs: local evidence frame -> research lane map -> external approval decision -> validation ledger -> synthesis handoff
- Subagent strategy: `recommended`, roles `local-evidence-reviewer`, `external-boundary-reviewer`, `claim-validation-reviewer`, join policy `parent_synthesis`, authorization `requires_user_permission`
- Subagent lifecycle: `none`; no agents spawned
- Observability: grouped by `gq-research-strategy-boundary-and-canon-2026-06-12`
- Promotion guardrail: research strategy is planning evidence only
- Required repairs: none
- Next route: `refine`

## Node

- Craft node: `boundary-and-canon`
- Title: Boundary and canon
- Research lane: canon and boundary research
- Strategy route: `RESEARCH-DISPATCH.json`
- Existing Refine route: `REFINE-DISPATCH.json`

## Core Research Question

Which workbook terms or assumptions conflict with locked Golden Quill canon and v0.1 boundaries?

## Local Evidence Boundary

Research starts local-first. Use these evidence classes before any external lookup:

- SOUL.md
- USER.md
- router.yaml
- CLAUDE.md
- architecture amendments
- daily logs

## Active Local Gaps

- `GAP-BC-UI-SCOPE` (flag): Workbook includes an operator console UI row; v0.1 has a locked no-UI boundary, so this row needs phase/scoping treatment before execution.

## External Evidence Classes

External research is not executed by this strategy. If local evidence leaves a named gap and Josh confirms the route, the bounded external classes are:

- none unless validating public-facing terminology risk
- no client/org material

## Validation Focus

three-posture vocabulary, no UI layer for v0.1, BYOK/local-first boundaries, and no revived deprecated terms

## Research Steps

1. Scope the node-specific research question and reject cross-node drift.
2. Build a local evidence baseline from Craft, workbook, and Golden Quill project sources.
3. Map research lanes and select local-only, gap-triggered external, or deferred research.
4. Ask for external-research approval when a named gap requires outside comparison.
5. Validate claims against source class, path or handle expectation, and owner boundary.
6. Hand off findings to the node's Refine route and Invoke first-artifact direction.

## Execution Boundary

No external research, subagents, or runtime-backed stages have run. This strategy becomes executable only after Josh confirms the dispatch route.
