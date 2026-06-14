---
module: keystone-lift
task: TASK-VERIFY
docType: work-pack-task
updatedAt: 2026-06-14
---

# TASK-VERIFY — Completion verification + M2 contract freeze

Layer: L3 · Wave: W3 · Gate: ready-after-impl
**Smallest Working Unit Exemption:** task ID contains `VERIFY` (closure task).

## Objective
Confirm the keystone success condition and freeze the spec-template contract the M2 pipeline will build on.

## Verdict checklist (PASS/FLAG/BLOCK)
1. invoke `define` dry-run emits a DomainSpec SPEC + aspect docs referencing canonical arcanum IDs. → required for PASS.
2. `module-formulae/` removed; no live references. → required for PASS.
3. TASK-AUDIT green (whole-diff). → required for PASS.
4. arcanum link-checker/definitions-index green. → required for PASS.
5. DS-side wedge references resolve to arcanum; moat cluster still private. → required for PASS.
6. Submodule-first respected: arcanum committed+pushed before any parent gitlink bump (`make bump-check`). → required for PASS.

## M2 contract freeze
Document the stable aspect-doc + Concept Registry contract (the interface test-derivation / doc→metrics / sync-registry consume) in `M2-CONTRACT.md`. Any later change to that interface is a versioned change, not a silent edit.

## Output
`VERIFY-REPORT.md` with the verdict + evidence links. FLAG/BLOCK items route back to the owning task.
