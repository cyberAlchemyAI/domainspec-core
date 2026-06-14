# Research Strategy - Golden Quill node-on-desk readiness

## Dispatch Spec Result

- Dispatch ID: `gq-research-strategy-node-on-desk-readiness-2026-06-12`
- Status: `pass`
- Mode: `research`
- Step count: 6
- Patterns: `sequential`, `decision`, `validation`, `synthesis`
- Gates: local-first evidence, external approval, org isolation, claim-evidence validation, owner boundary
- Handoffs: local evidence frame -> research lane map -> external approval decision -> validation ledger -> synthesis handoff
- Subagent strategy: `recommended`, roles `local-evidence-reviewer`, `external-boundary-reviewer`, `claim-validation-reviewer`, join policy `parent_synthesis`, authorization `requires_user_permission`
- Subagent lifecycle: `none`; no agents spawned
- Observability: grouped by `gq-research-strategy-node-on-desk-readiness-2026-06-12`
- Promotion guardrail: research strategy is planning evidence only
- Required repairs: none
- Next route: `refine`

## Node

- Craft node: `node-on-desk-readiness`
- Title: Golden Quill node-on-desk readiness
- Research lane: parent readiness recomposition
- Strategy route: `RESEARCH-DISPATCH.json`
- Existing Refine route: `REFINE-DISPATCH.json`

## Core Research Question

What evidence is needed to prove all child nodes add up to a working customer-node readiness path?

## Local Evidence Boundary

Research starts local-first. Use these evidence classes before any external lookup:

- child Craft ledgers
- workbook handoff
- existing Golden Quill architecture and lessons

## Active Local Gaps

- `GAP-NOD-HOURS-RATES` (block): Est. Hrs and Notes / Rate columns are blank across the workbook; staffing and capital budget cannot be computed yet.
- `GAP-NOD-CANON-VOCAB` (block): Workbook posture language includes deprecated vocabulary that must be translated to the current three-posture canon before any customer-facing or engineer-facing surface uses it.
- `GAP-NOD-SEQUENCE` (flag): Workbook lists tasks and roles but not dependency order, done definitions, or recomposition gates.

## External Evidence Classes

External research is not executed by this strategy. If local evidence leaves a named gap and Josh confirms the route, the bounded external classes are:

- none by default
- only compare deployment-readiness patterns if a named gap survives local synthesis

## Validation Focus

child-node coverage, recomposition gates, and no missing first-customer readiness surface

## Research Steps

1. Scope the node-specific research question and reject cross-node drift.
2. Build a local evidence baseline from Craft, workbook, and Golden Quill project sources.
3. Map research lanes and select local-only, gap-triggered external, or deferred research.
4. Ask for external-research approval when a named gap requires outside comparison.
5. Validate claims against source class, path or handle expectation, and owner boundary.
6. Hand off findings to the node's Refine route and Invoke first-artifact direction.

## Execution Boundary

No external research, subagents, or runtime-backed stages have run. This strategy becomes executable only after Josh confirms the dispatch route.
