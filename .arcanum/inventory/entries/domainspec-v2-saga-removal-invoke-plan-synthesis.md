---
tags: [inventory, invoke, plan, work-pack, domainspec-v2, ds-d1, ds-d8, migration, build-from-owned, promotion-guardrail, claim-le-proof]
node_type: synthesis
is_session: false
layer: implementation-plan
nature: reference
status: candidate
created: 2026-07-11
invoke_mode: plan
target: projects/domainspec-v2/development/saga-removal/
sources:
  - projects/domainspec-v2/development/saga-removal/IMPLEMENTATION-PLAN.md
  - projects/domainspec-v2/development/saga-removal/WORK-PACK.md
  - projects/domainspec-v2/development/saga-removal/IMPLEMENTATION-LAYERING.md
  - projects/domainspec-v2/development/saga-removal/PLAN-TRANSPORT.md
  - projects/domainspec-v2/development/ds-d1-improvement-plan/decisions/DEC-DSD1-SAGA-FORK.md
---

# DomainSpec v2 Saga Removal Invoke Plan

This is a non-authority Inventory read model for the Invoke plan at
projects/domainspec-v2/development/saga-removal/. It does not remove Saga,
change DS-D1/DS-D8 authority, or execute any SWU.

## Result

The high-complexity split work-pack plans zero active Saga type/signature
surface while preserving historical research, superseded decisions, telemetry,
Inventory history, and receipts.

The target architecture keeps orchestrates under Workflow, widens its
same/cross-feature scope, adds the finite attribute-one-of criterion, removes
active Saga schemas/fixtures and hard-coded validator expectations, cancels
contradictory Saga-hardening routes, and installs a classified zero-active
reference guard.

## Execution Shape

- 5 task contracts.
- 8 uniquely owned SWUs.
- 4 L0-L3 waves.
- Full Dispatch Spec validation: pass with no flags.
- Distill validation: pass.
- First unit: SWU-SGRM-001, a non-mutating migration packet and live reference
  manifest.

## Boundary

Historical Saga evidence is not a removal target. A future request to erase
research or prior decisions would require a separate destructive governance
decision.

## Residue

- External or persisted consumers are not evidenced; discovery during SGRM-001
  blocks mutation and routes decision-gate.
- DS-D1 intra-feature and DS-D8 same-feature vocabulary remain explicitly
  mapped rather than normalized in this plan.
- Concurrent meta-type registry edits must be consumed from live state at Task
  Session execution time.
