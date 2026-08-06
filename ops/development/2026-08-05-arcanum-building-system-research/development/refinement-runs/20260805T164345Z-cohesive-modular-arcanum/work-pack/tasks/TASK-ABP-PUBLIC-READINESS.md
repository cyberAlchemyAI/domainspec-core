# TASK-ABP-PUBLIC-READINESS — Lifecycle and Public Boundary

Objective: prepare a public-safe candidate only after private proof and lifecycle admission.

Dependencies: L0–L2 proof, real witness, capability-type decision, and public-write authorization.

## SWU-ABP-016 — Public reconstruction

- Behavior: reconstruct candidate docs/schemas/examples from public canonical sources only.
- Write scope: selected public capability path after lifecycle decision.
- Acceptance: no private parent prose, path, run ID, authority assumption, or payload field.
- Validation: public-boundary and private-marker scans plus source trace.

## SWU-ABP-017 — Generated package parity

- Behavior: sync exactly the selected package and prove canonical/generated parity.
- Write scope: canonical and selected generated package paths named by the lifecycle contract.
- Acceptance: byte and behavioral parity receipt.
- Validation: `arcanum/tools/sync-generated-skill-package.sh` for one selected package plus package fixtures; never partial forced bootstrap.

Lifecycle closeout is owned by Sigil Development or the selected capability lifecycle, with Experiment Harness, Signal Observer, Workflow Reflect, and a separate registry-owner route. This task cannot promote or release the capability.

