---
task_id: TASK-DSD1-SAGA
feature_code: DSD1
layer: L2
status: not-started
gate_status: blocked-on-saga-decision-after-swu-007
updatedAt: 2026-07-03
---

# TASK-DSD1-SAGA: Resolve Saga Hardening Versus Collapse

## Objective

Resolve whether Saga is a distinct DS-D1 category or should be collapsed,
deprecated, or routed through another owner path. The plan must not silently
keep Saga only because it exists in fixtures, and must not silently remove it
because it overlaps Workflow.

## Source Anchors

- `projects/domainspec-v2/development/r3-research/ds-d1-metatype-category-boundary/findings.md`
- `projects/domainspec-v2/impl/spec/meta-types/saga.schema.yml`
- `projects/domainspec-v2/impl/spec/meta-types/workflow.schema.yml`
- `projects/domainspec-v2/definitions/relationships/relationships.yml`
- `projects/domainspec-v2/development/meta-type-formalization/WORK-PACK.md`

## Decision Options

| Option | Meaning | Follow-up |
| --- | --- | --- |
| harden | Saga stays first-class and must carry laws Workflow does not. | Run SWU-DSD1-008. |
| collapse | Saga is merged, deprecated, or routed away from DS-D1. | Run SWU-DSD1-009. |

## SWUs

| SWU | Purpose | Write Scope | Gate |
| --- | --- | --- | --- |
| SWU-DSD1-007 | Record Saga fork decision. | Decision record only. | owner decision |
| SWU-DSD1-008 | Harden Saga/Workflow distinction. | Saga/Workflow schemas, fixtures, docs, tests. | conditional |
| SWU-DSD1-009 | Prepare collapse/deprecation packet. | Review/migration packet; no silent authority mutation. | conditional |

## Implementation Notes

- If hardening, Saga needs finite witnesses for participant scope,
  compensation, failure residue, temporal ordering, and cross-owner/multi-service
  transaction behavior.
- Workflow should remain an ordered intra-feature or intra-owner process unless
  a later decision changes its category.
- DS-D8 `orchestrates` pressure is relevant, but DS-D8 does not own the DS-D1
  type boundary.

## Acceptance Evidence

- Saga fork decision exists before any Saga schema mutation.
- Hardening branch rejects bad Saga/Workflow cross-label fixtures.
- Collapse branch names affected signatures, fixtures, validators, projections,
  and migration steps.
