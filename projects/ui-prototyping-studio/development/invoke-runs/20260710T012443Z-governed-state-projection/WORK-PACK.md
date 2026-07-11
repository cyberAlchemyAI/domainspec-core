---
id: ui-prototyping-studio-governed-state-projection-work-pack
project: ui-prototyping-studio
docType: work-pack
invoke_run: invoke-20260710T012443Z-governed-state-projection
status: proposed
updatedAt: 2026-07-10T01:24:43Z
---

# WORK-PACK: Governed State Projection

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Pass for `SWU-GSP-001`; later SWUs carry dependency gates. |
| complexity | medium | More than five tasks and touches runtime preview, diff, e2e, docs, and handoff semantics. |
| outputMode | split | Task and wave files are under `work-pack/`. |
| executionPackRef | `EXECUTION-PACK.md` | Required for medium complexity. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 layer decisions. |
| dispatchTechniqueTrace | `ARCHITECTURE-UPGRADE.md#dispatch-technique-trace` | Full dispatch not required. |
| distillValidationStatus | flag | Plan is executable for first SWU; release-readiness and OD phase-two remain gaps. |
| activeLayerWindow | L0 | Current-head projection first. |
| readinessProfile | pilot | Research-to-implementation repair, not release packaging. |

## Objective Summary

Deliver the governed-state projection spine for UI Prototyping Studio so the
browser/control surface truthfully reflects current governed state, visible
diff evidence, durable reversible actions, and handoff evidence semantics.

Success condition: each SWU has a failing-before/passing-after witness or an
explicit review receipt, and no artifact claims production HTML, Open Design
identity replacement, or fresh checked-in e2e before the evidence exists.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-GSP-001 | Current-head projection and annotation target truth. | L0 | [W1](work-pack/waves/W1-L0-projection-truth.md) | none | Playwright current-head witness. |
| S-GSP-002 | Visible-change diff integrity. | L1 | [W2](work-pack/waves/W2-L1-diff-action-trust.md) | S-GSP-001 | CSS/style fixture and e2e diff receipt. |
| S-GSP-003 | Durable action framing and mobile/annotation first usability. | L1 | [W2](work-pack/waves/W2-L1-diff-action-trust.md) | S-GSP-001 | Playwright confirmation/mobile/annotation receipt. |
| S-GSP-004 | Deterministic e2e harness and handoff evidence semantics. | L2 | [W3](work-pack/waves/W3-L2-evidence-semantics.md) | S-GSP-001 | Standard e2e command; handoff missingRefs test. |
| S-GSP-005 | Docs/test-count sync and minimal OD evidence slice. | L2/L3 | [W3](work-pack/waves/W3-L2-evidence-semantics.md) | S-GSP-002, S-GSP-004 | Docs review; `CraftEvidencePack` fixture. |

## Task Status Board

| Task ID | Goal | Layer | Waves | Gate Status | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-GSP-001](work-pack/tasks/TASK-GSP-001-current-head-projection.md) | Make current head the primary browser projection and annotation target. | L0 | W1 | ready | not-started |
| [TASK-GSP-002](work-pack/tasks/TASK-GSP-002-visible-change-diff.md) | Add visible-change/global-style diff integrity. | L1 | W2 | blocked-by-GSP-001 | not-started |
| [TASK-GSP-003](work-pack/tasks/TASK-GSP-003-action-annotation-mobile.md) | Add durable reversible-action framing plus mobile/annotation first slice. | L1 | W2 | blocked-by-GSP-001 | not-started |
| [TASK-GSP-004](work-pack/tasks/TASK-GSP-004-validation-handoff-docs.md) | Repair e2e harness, handoff evidence semantics, and docs/test-count sync. | L2 | W3 | ready-after-GSP-001 | not-started |
| [TASK-GSP-005](work-pack/tasks/TASK-GSP-005-craft-evidence-pack.md) | Add minimal OD-inspired `CraftEvidencePack` behind Studio gates. | L3 | W3 | blocked-by-GSP-002-GSP-004 | not-started |

## SWU Manifest

| SWU ID | Parent Task | Dependencies | Write Scope | Acceptance Evidence | Validation Surface | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-GSP-001 | [TASK-GSP-001](work-pack/tasks/TASK-GSP-001-current-head-projection.md) | none | `backend/src/cli/studio.ts`; optional application projection helper; e2e spec | Current-head primary preview and annotation use current head after Accept/Revert/external write. | Playwright witness and `/state` assertion. | task-session |
| SWU-GSP-002 | [TASK-GSP-002](work-pack/tasks/TASK-GSP-002-visible-change-diff.md) | SWU-GSP-001 | `application/admission.ts`; domain diff model if needed; tests | CSS/theme visible mutation cannot produce silent zero-diff confidence. | Unit fixture plus e2e pending panel assertion. | task-session |
| SWU-GSP-003 | [TASK-GSP-003](work-pack/tasks/TASK-GSP-003-action-annotation-mobile.md) | SWU-GSP-001 | `backend/src/cli/studio.ts`; preview CSS/tests | Accept/Revert confirmation, mobile comparison, annotation target state. | Playwright desktop/mobile screenshots/assertions. | task-session |
| SWU-GSP-004 | [TASK-GSP-004](work-pack/tasks/TASK-GSP-004-validation-handoff-docs.md) | none | `backend/e2e/helpers.ts`; handoff export use case/schema/tests; docs | Standard e2e no longer depends on ambient Corepack; readiness labels no longer overclaim. | e2e command receipt; unit/slice handoff test; docs review. | task-session |
| SWU-GSP-005 | [TASK-GSP-004](work-pack/tasks/TASK-GSP-004-validation-handoff-docs.md) | SWU-GSP-004 | `ARCHITECTURE.md`; `SPEC.md`; `CRAFT.md`; `PLAN-NEXT.md`; test docs | Docs/test-count/state claims match current evidence. | Review receipt and grep-backed consistency check. | local-fallback |
| SWU-GSP-006 | [TASK-GSP-005](work-pack/tasks/TASK-GSP-005-craft-evidence-pack.md) | SWU-GSP-002, SWU-GSP-004 | new evidence schema/provenance surfaces; tests | Minimal `CraftEvidencePack` cannot bypass Studio gates and marks required/advisory/subjective buckets. | Unit fixture and accepted revision provenance receipt. | task-session |

## Blockers And Gaps

| ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| GAP-GSP-001 | Invoke provenance | This was discovery-mode design from accepted research, not normal design from approved define outputs. | Invoke/Studio owner | Treat plan as proposed architecture package; first task-session validates with code receipt. |
| GAP-GSP-002 | Evidence | Fresh checked-in e2e remains unclaimed until helper path is fixed. | TASK-GSP-004 | Run after SWU-GSP-004. |
| GAP-GSP-003 | UX research | Human-study/control evidence remains future work. | Studio owner | Do not claim release ergonomics from this plan. |
| GAP-GSP-004 | OD phase-two | Broader GeneratorProfile/DesignObjectiveBrief/seeds/CritiqueReview remain deferred. | Studio owner | Reopen only after L0-L2 receipts. |

## Distill Validation

- Smallest coherent unit: `SWU-GSP-001`.
- Recomposition proof: current-head projection is the base projection spine; diff,
  action framing, handoff semantics, and OD evidence all consume it.
- Hidden gaps: normal define approval absent; e2e helper fragility; L1/L2 release
  proof missing.
- Verdict: `flag`, route allowed for `SWU-GSP-001` with gaps carried.

## Recommended Next Route

Run `task-session` on `SWU-GSP-001` only. Do not execute later SWUs until the
current-head projection receipt exists.
