---
module: one-shot-admission-prototype
version: candidate
status: validated-candidate-local
updatedAt: 2026-07-30
docType: work-pack
---

# WORK-PACK: One-shot admission prototype

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | block | Normal governed Task Session handoff is intentionally unavailable. |
| candidateLocalGateStatus | pass | User explicitly selected Candidate-Local Prototype Fast Lane option A. |
| complexity | high | Public submodule, private integration evidence, generated parity, and multiple reusable spells. |
| outputMode | split | Task and wave contracts are separate. |
| executionPackRef | `EXECUTION-PACK.md` | Ordered candidate-local execution. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 decision boundaries. |
| dispatchTechniqueTrace | `dispatch.json` | Full cross-capability/public-private route. |
| distillValidationStatus | pass | Role-simulated Proposer/Balancer review is recorded in `DISTILL-VALIDATION.md`. |
| swuAtomicityStatus | pass | Nine single-behavior SWUs after Distill split repair. |
| firstUnitNarrownessStatus | pass | SWU-OAP-001 is schema-only and reversible. |
| closeoutSyncStatus | block | Explicitly deferred by the selected fast lane and Handoff Notice. |
| activeLayerWindow | L0 | Public contract and deterministic proof first. |
| readinessProfile | prototype | No promotion or release claim. |

## Objective Summary

- Objective: implement a working local candidate for WPRA exact admission
  projection plus approved-epoch finite-frontier execution.
- Primary inputs: accepted research SHA-256
  `ba739376af94416d3c880bece01fe6698d60c615a4caf0ae64b0d1b4668617ce`,
  current WPRA and chain contracts, and the user-approved fast lane.
- Success condition: all nine ordered SWUs pass their acceptance checks, the
  19 private fixtures execute, and no public/private or authority boundary is
  crossed.

## Explicit Fast-lane Boundary

This work pack is executable only under the Candidate-Local Prototype Fast
Lane selected by the user. It is not mutation-ready evidence for normal Task
Session admission. The parent executes the finite order directly, preserves
write scopes, and stops on the first acceptance-critical failure. Deferred
governance is owned by the Handoff Notice.

## Frozen Frontier

| Order | SWU | Parent | Primary behavior | Dependencies | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | `SWU-OAP-001` | [TASK-WPRA-CONTRACT](work-pack/tasks/TASK-WPRA-CONTRACT.md) | Add additive WPRA projection/audit contracts. | none | pass |
| 2 | `SWU-OAP-002` | [TASK-WPRA-RUNTIME](work-pack/tasks/TASK-WPRA-RUNTIME.md) | Generate and audit the no-authority projection. | OAP-001 | pass |
| 3 | `SWU-OAP-003` | [TASK-CHAIN-CONTRACT](work-pack/tasks/TASK-CHAIN-CONTRACT.md) | Add additive chain, transition, and NO_OP contracts. | OAP-001 | pass |
| 4 | `SWU-OAP-004` | [TASK-CHAIN-RUNTIME](work-pack/tasks/TASK-CHAIN-RUNTIME.md) | Enforce approved epoch, cursor, risk, and budget. | OAP-003 | pass |
| 5 | `SWU-OAP-005` | [TASK-CHAIN-RUNTIME](work-pack/tasks/TASK-CHAIN-RUNTIME.md) | Enforce semantic NO_OP and owner-routed compensation. | OAP-004 | pass |
| 6 | `SWU-OAP-006` | [TASK-INTEGRATION](work-pack/tasks/TASK-INTEGRATION.md) | Execute the 19 private frozen-input fixtures. | OAP-002, OAP-005 | pass |
| 7 | `SWU-OAP-007` | [TASK-SYNC](work-pack/tasks/TASK-SYNC.md) | Sync only the WPRA generated skill package. | OAP-002, OAP-006 | pass |
| 8 | `SWU-OAP-008` | [TASK-SYNC](work-pack/tasks/TASK-SYNC.md) | Sync only the chain generated skill package. | OAP-005, OAP-006 | pass |
| 9 | `SWU-OAP-009` | [TASK-VERIFY](work-pack/tasks/TASK-VERIFY.md) | Run aggregate validation and emit the prototype report. | OAP-007, OAP-008 | pass |

No newly discovered work may join this frontier.

## SWU Atomicity Review

| SWU | Independent boundary | Candidate child units | Retained-boundary rationale | Verdict |
| --- | --- | --- | --- | --- |
| OAP-001 | WPRA schemas parse and cross-reference without runtime code. | manifest; config; report | They define one WPRA projection boundary and version migration. | pass |
| OAP-002 | WPRA emits or blocks one projection with stable codes. | generator; validator; tests | Generator without its validator has no reviewable behavior. | pass |
| OAP-003 | Chain schemas parse and bind the WPRA manifest vocabulary. | config; transition; NO_OP | They define one public chain-consumption boundary. | pass |
| OAP-004 | Chain accepts or rejects one epoch/cursor transition. | state store; epoch check; budget/risk | Each participates in one decision: whether a next request is legal. | pass |
| OAP-005 | Chain accepts a semantic NO_OP or stops at compensation. | NO_OP; compensation | Both close the post-execution transition without selecting another SWU. | pass |
| OAP-006 | Exactly 19 private cases produce receipts. | positive; negatives; controls | One aggregate experiment is the accepted research boundary. | pass |
| OAP-007 | WPRA generated mirrors equal canonical output. | Codex; Claude | One package sync owns both runtime mirrors. | pass |
| OAP-008 | Chain generated mirrors equal canonical output. | Codex; Claude | One package sync owns both runtime mirrors. | pass |
| OAP-009 | One aggregate report proves every declared validation. | individual commands | Closure is meaningful only over the complete validation set. | pass |

## Validation Strategy

- Parse every new JSON schema and fixture.
- Preserve and rerun the WPRA v1 suite.
- Run the new WPRA v2 suite.
- Run chain legacy and epoch-aware fixtures.
- Run all 19 private replay cases and verify forbidden transitions.
- Regenerate only the two named skill packages.
- Run package parity, scoped whitespace, public/private literal scan, and
  offline parent-gitlink immutability. Defer network-backed `make bump-check`
  until an authorized submodule commit/push route exists.

## Blockers And Residue

| ID | State | Meaning | Owner |
| --- | --- | --- | --- |
| B-GOV-001 | deferred-approved | Normal per-SWU Task Session/Refresh/Continuation closeout is not run. | Future governance owner via Handoff Notice |
| B-UPSTREAM-001 | deferred-approved | Invoke/Interview/Decision Gate receipt hardening remains outside prototype. | Spellcraft/Invoke owners |
| B-PROMOTE-001 | blocked | Registry, promotion, publication, release, and deployment are not authorized. | Human/lifecycle owners |

## Forbidden Scope

- `arcanum/arcana/task-session/**`
- `arcanum/spells/invoke/**`
- registries, promotion receipts, Git commits/pushes, deployment
- Body War product source mutation
- private DomainSpec/Saturn/cyberAlchemy prose inside `arcanum/`
- external network requests

## Handoff

- Governed Task Session handoff: blocked and intentionally deferred.
- Candidate-local route: complete; see `PROTOTYPE-VALIDATION.md`.
- Deferred lifecycle route: Handoff Notice locator, populated before product
  mutation.
