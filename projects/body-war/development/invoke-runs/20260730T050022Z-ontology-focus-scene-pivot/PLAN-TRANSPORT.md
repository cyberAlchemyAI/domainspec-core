---
module: body-war-ontology-focus-scene-pivot
version: current
status: pass-for-explicit-selection
updatedAt: 2026-07-30
docType: invoke-plan-transport
---

# Invoke Plan Transport

## Classification

- complexity: high
- output mode: split
- layers: L0–L3
- SWUs: 26
- task-shaped SWUs: 0
- first selectable SWU: `SWU-OFSP-001`
- selected SWU: none
- implementation authority: not granted

## Gates

- Define: pass
- Design selection: pass, fixed point
- Design evidence state: `design-validator-pass`
- Dispatch Spec: pass
- Distill Validate: pass after three Balancer rounds
- closeout sync: pass
- planning evidence: validated and observability-recorded
- runtime/acceptance evidence: pending

## Execution Boundary

The next route is not automatic implementation. The user must explicitly select
one dependency-ready SWU. Context Builder then derives the exact pack and one
Task Session executes only that unit.

The recommended first selection is `SWU-OFSP-001`, the independent fixture
oracle. It is test-only and establishes the expected four-node/portal arrays
before any native UI or build source changes.

## Claim Ceiling

This Plan is implementation-ready planning. It does not prove source
implementation, a rebuilt viewer, browser acceptance, comprehension, ontology
promotion, upstream acceptance, release, deployment, or production readiness.
