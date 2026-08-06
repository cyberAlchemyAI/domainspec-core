# TASK-ABP-RUNTIME — Repair Runtime and Parity Boundaries

Objective: repair the two independently reproduced Orchestrate defects and establish generated-package parity.

Dependencies: L1 model and immutable current canonical source identity.

## SWU-ABP-009 — Exact receipt set

- Behavior: reducer consumes only the persisted expected action-receipt manifest.
- Write scope: `arcanum/runtime/orchestrate/`
- Acceptance: unrelated JSON cannot affect a wave; missing/duplicate expected receipt blocks.
- Validation: new regression plus existing Orchestrate suite.

## SWU-ABP-010 — Run-global action IDs

- Behavior: allocate unique action IDs across the complete run before any host spawn.
- Write scope: `arcanum/runtime/orchestrate/`
- Acceptance: no cross-wave collision; replay remains blocked.
- Validation: multi-wave regression and existing event validator.

## SWU-ABP-011 — Generated parity

- Behavior: compare canonical/generated identity and behavior for WPRA, Task Session, Continuation Router, Orchestrate, and the later protocol package.
- Write scope: unavailable until an exact package sync contract selects canonical and generated paths.
- Acceptance: byte expectations plus fixture behavior pass or block with exact divergence.
- Validation: package-specific sync/check commands; never partial forced bootstrap.

SWU-009 and SWU-010 are separate because input-set admission and action identity are independently reviewable. They may run concurrently only in isolated branches; their shared canonical write scope requires serialized integration.

Closeout targets are `WORK-PACK.md`, this task, and `evidence-index.json`; canonical changes additionally require their lifecycle owner receipt. No commit/push is authorized.

