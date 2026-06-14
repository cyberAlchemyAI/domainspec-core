# Research Strategy - White-glove delivery and Node Care

## Dispatch Spec Result

- Dispatch ID: `gq-research-strategy-white-glove-delivery-node-care-2026-06-12`
- Status: `pass`
- Mode: `research`
- Step count: 6
- Patterns: `sequential`, `decision`, `validation`, `synthesis`
- Gates: local-first evidence, external approval, org isolation, claim-evidence validation, owner boundary
- Handoffs: local evidence frame -> research lane map -> external approval decision -> validation ledger -> synthesis handoff
- Subagent strategy: `recommended`, roles `local-evidence-reviewer`, `external-boundary-reviewer`, `claim-validation-reviewer`, join policy `parent_synthesis`, authorization `requires_user_permission`
- Subagent lifecycle: `none`; no agents spawned
- Observability: grouped by `gq-research-strategy-white-glove-delivery-node-care-2026-06-12`
- Promotion guardrail: research strategy is planning evidence only
- Required repairs: none
- Next route: `refine`

## Node

- Craft node: `white-glove-delivery-node-care`
- Title: White-glove delivery and Node Care
- Research lane: white-glove delivery and Node Care research
- Strategy route: `RESEARCH-DISPATCH.json`
- Existing Refine route: `REFINE-DISPATCH.json`

## Core Research Question

What delivery, onboarding, training, vault build, source universe, first packet, support, and Day 60 evidence turns first installs into a repeatable service?

## Local Evidence Boundary

Research starts local-first. Use these evidence classes before any external lookup:

- workbook white-glove rows
- Golden Quill sovereignty promise
- client onboarding constraints

## Active Local Gaps

- `GAP-WGD-PLAYBOOK` (block): Pre-deployment through training sessions needs a repeatable delivery playbook.
- `GAP-WGD-CS-HANDOFF` (flag): Customer Success and Field Tech transition from Josh/engineers needs trigger and checklist training.
- `GAP-WGD-DAY60` (flag): Day 60 review needs metrics, support-load evidence, renewal signal, and next-cycle plan shape.

## External Evidence Classes

External research is not executed by this strategy. If local evidence leaves a named gap and Josh confirms the route, the bounded external classes are:

- customer-success onboarding patterns
- hardware deployment checklist examples
- only after approval

## Validation Focus

pre-deployment questionnaire, Day 0 install, vault build, first opportunity packet, training sessions, support loop, and Day 60 metrics

## Research Steps

1. Scope the node-specific research question and reject cross-node drift.
2. Build a local evidence baseline from Craft, workbook, and Golden Quill project sources.
3. Map research lanes and select local-only, gap-triggered external, or deferred research.
4. Ask for external-research approval when a named gap requires outside comparison.
5. Validate claims against source class, path or handle expectation, and owner boundary.
6. Hand off findings to the node's Refine route and Invoke first-artifact direction.

## Execution Boundary

No external research, subagents, or runtime-backed stages have run. This strategy becomes executable only after Josh confirms the dispatch route.
