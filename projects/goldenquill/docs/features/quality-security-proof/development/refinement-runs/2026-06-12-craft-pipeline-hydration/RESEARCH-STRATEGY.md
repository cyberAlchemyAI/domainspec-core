# Research Strategy - Quality, security, and proof

## Dispatch Spec Result

- Dispatch ID: `gq-research-strategy-quality-security-proof-2026-06-12`
- Status: `pass`
- Mode: `research`
- Step count: 6
- Patterns: `sequential`, `decision`, `validation`, `synthesis`
- Gates: local-first evidence, external approval, org isolation, claim-evidence validation, owner boundary
- Handoffs: local evidence frame -> research lane map -> external approval decision -> validation ledger -> synthesis handoff
- Subagent strategy: `recommended`, roles `local-evidence-reviewer`, `external-boundary-reviewer`, `claim-validation-reviewer`, join policy `parent_synthesis`, authorization `requires_user_permission`
- Subagent lifecycle: `none`; no agents spawned
- Observability: grouped by `gq-research-strategy-quality-security-proof-2026-06-12`
- Promotion guardrail: research strategy is planning evidence only
- Required repairs: none
- Next route: `refine`

## Node

- Craft node: `quality-security-proof`
- Title: Quality, security, and proof
- Research lane: quality, security, and proof research
- Strategy route: `RESEARCH-DISPATCH.json`
- Existing Refine route: `REFINE-DISPATCH.json`

## Core Research Question

What evidence package proves guardrails, boundary security, claims, demo integrity, and instrumentation before first customer node?

## Local Evidence Boundary

Research starts local-first. Use these evidence classes before any external lookup:

- Five Laws
- architecture gates
- workbook proof rows
- existing validation templates

## Active Local Gaps

- `GAP-QSP-TEST-PLAN` (block): Guardrails-as-tests need explicit posture, classification, audit-completeness, and fail-closed coverage.
- `GAP-QSP-SECURITY-REVIEWER` (block): Independent security reviewer is onboard-now but not assigned.
- `GAP-QSP-CLAIMS-REGISTER` (flag): External claims need evidence-category mapping before sales material hardens.
- `GAP-QSP-INSTRUMENTATION` (flag): Support hours, usage baselines, and renewal-intent capture need instrument definitions.

## External Evidence Classes

External research is not executed by this strategy. If local evidence leaves a named gap and Josh confirms the route, the bounded external classes are:

- security review scope examples
- test-plan patterns
- claims-register examples
- only after approval

## Validation Focus

guardrails-as-tests, fail-closed behavior, security reviewer scope, claims evidence mapping, demo standard, and instrumentation definitions

## Research Steps

1. Scope the node-specific research question and reject cross-node drift.
2. Build a local evidence baseline from Craft, workbook, and Golden Quill project sources.
3. Map research lanes and select local-only, gap-triggered external, or deferred research.
4. Ask for external-research approval when a named gap requires outside comparison.
5. Validate claims against source class, path or handle expectation, and owner boundary.
6. Hand off findings to the node's Refine route and Invoke first-artifact direction.

## Execution Boundary

No external research, subagents, or runtime-backed stages have run. This strategy becomes executable only after Josh confirms the dispatch route.
