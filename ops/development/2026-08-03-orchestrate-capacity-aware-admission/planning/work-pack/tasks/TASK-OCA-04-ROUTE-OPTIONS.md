---
taskId: TASK-OCA-04
swuId: SWU-OCA-004
status: planned
layer: L1
wave: W4
---

# Capacity route options

## Objective and boundary

Turn a capacity block into neutral, feasible choices without changing the
validated or approved route. Consumers may explain the choices; Orchestrate
does not select them.

Primary behavior: each option states capability availability, semantic impact,
and whether validation and renewed confirmation are required.

Independent acceptance boundary: infeasible choices are absent or explicitly
unavailable, and no projection writes a dispatch, action, registration, or
approval record.

## Source anchors and future write scope

- add `arcanum/runtime/orchestrate/schemas/capacity-route-option.schema.json`
- add `arcanum/runtime/orchestrate/schemas/capacity-route-capabilities.schema.json`
- add `arcanum/runtime/orchestrate/scripts/project_capacity_routes.py`
- edit `arcanum/runtime/orchestrate/SKILL.md`
- add `arcanum/runtime/orchestrate/tests/capacity-route-options/capability-fixtures.json`
- add `arcanum/runtime/orchestrate/tests/capacity-route-options/option-fixtures.json`
- add `arcanum/runtime/orchestrate/tests/capacity-route-options/test_capacity_route_options.py`

## Implementation detail

Consume one versioned, non-authoritative capability-map document supplied by
the caller; absent, stale, or invalid maps default to no offered execution
routes. Project options such as smaller wave, ordered/serial execution, inline
work, fresh session, host queue, defer, or cancel only from declared capabilities.
For each option include owner, feasibility state, changed semantics, required
route validation, required confirmation, and non-authority explanation. Any
change to role count, concurrency, order, session, or capability graph is
material and must return to Dispatch Spec and the appropriate approval gate.
Do not leak private host/account diagnostics.

Tests cover absent capability, semantically invalid serialization, approval
flags, stable ordering, neutral schema projection, and a no-side-effect check.

## Done and evidence

- schema and option matrix pass;
- no option is mistaken for an execution action or authorization;
- consumer text can be layered outside the public runtime contract;
- the current topology remains byte-identical after projection.

Dependency: `SWU-OCA-003` terminal receipt. Owner: Orchestrate route-projection
owner. Closeout uses the `SWU-OCA-004` inventory row.
