# Research Strategy - Hardware and Golden Image

## Dispatch Spec Result

- Dispatch ID: `gq-research-strategy-hardware-golden-image-2026-06-12`
- Status: `pass`
- Mode: `research`
- Step count: 6
- Patterns: `sequential`, `decision`, `validation`, `synthesis`
- Gates: local-first evidence, external approval, org isolation, claim-evidence validation, owner boundary
- Handoffs: local evidence frame -> research lane map -> external approval decision -> validation ledger -> synthesis handoff
- Subagent strategy: `recommended`, roles `local-evidence-reviewer`, `external-boundary-reviewer`, `claim-validation-reviewer`, join policy `parent_synthesis`, authorization `requires_user_permission`
- Subagent lifecycle: `none`; no agents spawned
- Observability: grouped by `gq-research-strategy-hardware-golden-image-2026-06-12`
- Promotion guardrail: research strategy is planning evidence only
- Required repairs: none
- Next route: `refine`

## Node

- Craft node: `hardware-golden-image`
- Title: Hardware and Golden Image
- Research lane: hardware and Golden Image research
- Strategy route: `RESEARCH-DISPATCH.json`
- Existing Refine route: `REFINE-DISPATCH.json`

## Core Research Question

What proof is needed for one approved hardware baseline and a repeatable signed Golden Image process?

## Local Evidence Boundary

Research starts local-first. Use these evidence classes before any external lookup:

- hardware workbook rows
- router/hardware context
- Golden Image and sovereignty architecture

## Active Local Gaps

- `GAP-HGI-REFERENCE-SPEC` (flag): Reference workstation and approved alternative are not yet captured as a testable spec.
- `GAP-HGI-BURN-IN` (flag): Burn-in and acceptance procedure needs thermal, memory, storage, and inference benchmark thresholds.
- `GAP-HGI-IMAGE-VERIFY` (block): Golden Image write process needs repeatable verification evidence per unit.
- `GAP-HGI-BACKUP-RECOVERY` (block): Backup, customer-owned export, and recovery posture need a tested procedure.

## External Evidence Classes

External research is not executed by this strategy. If local evidence leaves a named gap and Josh confirms the route, the bounded external classes are:

- Apple Mac Mini specs
- burn-in practices
- disk encryption/imaging/signing references
- only after approval

## Validation Focus

reference spec, burn-in acceptance, imaging verification, update signing, recovery/export, and per-node repeatability

## Research Steps

1. Scope the node-specific research question and reject cross-node drift.
2. Build a local evidence baseline from Craft, workbook, and Golden Quill project sources.
3. Map research lanes and select local-only, gap-triggered external, or deferred research.
4. Ask for external-research approval when a named gap requires outside comparison.
5. Validate claims against source class, path or handle expectation, and owner boundary.
6. Hand off findings to the node's Refine route and Invoke first-artifact direction.

## Execution Boundary

No external research, subagents, or runtime-backed stages have run. This strategy becomes executable only after Josh confirms the dispatch route.
