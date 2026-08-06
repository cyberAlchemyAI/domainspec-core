# Stage 09 — Invoke Plan

## Plan result

- Invoke mode: `plan`
- Complexity: medium
- Output: split Work Pack plus Implementation Layering and Execution Pack
- Plan artifact status: `flag`
- Mutation gate: `block`
- Execution entry: `blocked`
- Allowed routes: none
- First narrow candidate: SWU-CAPI-001 fresh-process reader witness

The plan is structurally complete but intentionally not mutation-ready. It
contains nine atomic SWUs, exact candidate write scopes, dependencies, evidence,
validation, execution-owner recommendations, closeout sync, W0 baseline gate,
and W1-W5 choreography. The user confirmed refinement and critics, not product
implementation or a new experiment, so `allowedRoutes` remains empty.

## Owner prerequisites

1. Approve or replace the proposed private root
   `implementation/domainspec/tools/craft-consultation-api/`.
2. Select the principal/session and secret-provider port owners; no credentials
   or real secrets are needed for fixture-only work.
3. Give a separate execution request that selects exactly one frontier SWU and
   refreshes the allowed-route projection and digest.

Until then, no Task Session may infer authorization from this plan. Deployment,
public promotion, snapshot replacement, recovery, and legacy adapters remain
outside the active layer window.

## Outputs

- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `EXECUTION-PACK.md`
- `work-pack/tasks/TASK-RUNTIME.md`
- `work-pack/tasks/TASK-CONTRACT.md`
- `work-pack/tasks/TASK-HTTP.md`
- `work-pack/tasks/TASK-ROWS.md`
- `work-pack/tasks/TASK-VERIFY.md`
- `work-pack/waves/W0.md` through `W5.md`
