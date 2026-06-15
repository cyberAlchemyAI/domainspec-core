---
doc_type: runtime-handoff
run_id: 20260615T132005Z-goal-spec-architecture-first
status: blocked-awaiting-confirmation
updated_at: 2026-06-15
---

# Runtime Handoff

## Objective

Run the validated architecture-first Refine route for creating a goal-spec
package after the operator approves runtime-backed stages and the recommended
subagent fanout.

## Validated Dispatch Reference

`REFINE-DISPATCH.json`

Dispatch Spec validation: pass with no blocks or flags.

## Permission State

- Runtime-backed stages: `requires_user_permission`
- Delegated subagents: `requires_user_permission`
- External research: `blocked unless named gap appears and operator confirms`
- Submodule mutation: `blocked`
- Generated mirror mutation: `blocked`
- Native Codex goal projection: `deferred until readiness inputs exist`

## Proposed Subagents

| Role | Owns | Affected steps |
| --- | --- | --- |
| `architecture-mapper` | architecture evidence and selected unit proposal | s01, s05, s06 |
| `goal-profile-readiness-auditor` | selected unit, strict pack, verification, blocker readiness | s06, s09, s10 |
| `owner-boundary-auditor` | public/private/generated/runtime write-scope verdict | s03, s07, s10 |

## Receipt Requirements

Every runtime-backed stage must record:

- `dispatch_id`
- `step_id`
- `capability_ref`
- `status`
- `artifacts`
- `validation`
- `observer_status`
- `blockers`
- `residue`
- `handoff_note`

Every delegated subagent must record:

- `agent_id`
- `role_id`
- `spawn_status`
- `join_status`
- `close_status`
- `residue`
- `reroute`
- `artifact_paths`
- `validation_result`

## Runtime Status

Blocked before runtime execution. The only completed work is preflight strategy
materialization and Dispatch Spec validation.
