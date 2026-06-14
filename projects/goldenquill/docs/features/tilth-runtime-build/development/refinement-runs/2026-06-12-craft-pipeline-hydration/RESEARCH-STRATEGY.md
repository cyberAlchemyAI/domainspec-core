# Research Strategy - Tilth runtime build

## Dispatch Spec Result

- Dispatch ID: `gq-research-strategy-tilth-runtime-build-2026-06-12`
- Status: `pass`
- Mode: `research`
- Step count: 6
- Patterns: `sequential`, `decision`, `validation`, `synthesis`
- Gates: local-first evidence, external approval, org isolation, claim-evidence validation, owner boundary
- Handoffs: local evidence frame -> research lane map -> external approval decision -> validation ledger -> synthesis handoff
- Subagent strategy: `recommended`, roles `local-evidence-reviewer`, `external-boundary-reviewer`, `claim-validation-reviewer`, join policy `parent_synthesis`, authorization `requires_user_permission`
- Subagent lifecycle: `none`; no agents spawned
- Observability: grouped by `gq-research-strategy-tilth-runtime-build-2026-06-12`
- Promotion guardrail: research strategy is planning evidence only
- Required repairs: none
- Next route: `refine`

## Node

- Craft node: `tilth-runtime-build`
- Title: Tilth runtime build
- Research lane: Tilth runtime build research
- Strategy route: `RESEARCH-DISPATCH.json`
- Existing Refine route: `REFINE-DISPATCH.json`

## Core Research Question

What local-first runtime, vault, routing, ingestion, Scout, drafting, review, and audit evidence is needed for v0.1 without adding a UI layer?

## Local Evidence Boundary

Research starts local-first. Use these evidence classes before any external lookup:

- router.yaml
- architecture docs
- pipeline implementation docs
- workbook runtime rows

## Active Local Gaps

- `GAP-TRB-WORK-PACKS` (block): Runtime rows are still task inventory, not sequenced implementation work packs.
- `GAP-TRB-POSTURE-CANON` (block): Posture row depends on boundary-and-canon correction before execution.
- `GAP-TRB-UI-PHASE` (flag): Operator console row needs phase treatment because v0.1 has no UI layer.
- `GAP-TRB-GOLDEN-IMAGE-HANDOFF` (flag): Golden Image assembly depends on hardware/image signing and runtime packaging handoff.

## External Evidence Classes

External research is not executed by this strategy. If local evidence leaves a named gap and Josh confirms the route, the bounded external classes are:

- current local model/runtime package docs only if a named implementation gap appears
- no cloud vendor dependency decisions without approval

## Validation Focus

headless v0.1 scope, posture vocabulary, local inference/routing feasibility, audit completeness, and Golden Image handoff

## Research Steps

1. Scope the node-specific research question and reject cross-node drift.
2. Build a local evidence baseline from Craft, workbook, and Golden Quill project sources.
3. Map research lanes and select local-only, gap-triggered external, or deferred research.
4. Ask for external-research approval when a named gap requires outside comparison.
5. Validate claims against source class, path or handle expectation, and owner boundary.
6. Hand off findings to the node's Refine route and Invoke first-artifact direction.

## Execution Boundary

No external research, subagents, or runtime-backed stages have run. This strategy becomes executable only after Josh confirms the dispatch route.
