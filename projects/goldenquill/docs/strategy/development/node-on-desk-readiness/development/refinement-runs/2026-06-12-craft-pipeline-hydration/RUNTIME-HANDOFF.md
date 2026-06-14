# Runtime Handoff - Golden Quill node-on-desk readiness

## Runtime Boundary

- Runtime: `codex-native-skills`
- Adapter: `codex-skill`
- Owner: `refine`
- Status: `not_run`
- Runtime run folder: `blocked until Josh confirms the strategy`

## Runtime Objective

Run the canonical Refine loop for `node-on-desk-readiness` using parent-owned native runtime dispatch and produce `RESULT.md`.

## Dispatch Route

- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch schema: `.agents/skills/dispatch-spec/dispatch.schema.yml`
- Dispatch validation: `pass`
- Dispatch ID: `gq-craft-hydration-node-on-desk-readiness-2026-06-12`
- Technique catalog: `.agents/skills/dispatch-spec/TECHNIQUE-CATALOG.md`
- Technique overlays: `baseline_sequence`, `route_menu_for_ambiguity`, `memory_residue_for_context_recovery`

## Stage Receipt Contract

Every runtime-backed stage must return `dispatch_id`, `step_id`, `capability_ref`, `status`, `artifacts`, `validation`, `observer_status`, `blockers`, `residue`, and `handoff_note`. Approved delegated reviewers must also return `agent_id`, `role_id`, `spawn_status`, `join_status`, `close_status`, and `reroute`.

Deprecated command files, slash commands, and command-resolution checks are not active success gates. This handoff targets native skill execution after confirmation.

## Handoff Requirements

- Context Builder handoff pack: `blocked until approved runtime run`
- Handoff index: `blocked until approved runtime run`
- Strict coverage: `block`
- Runtime adapter profile: `codex native skill surface`
- Runtime status: `not_run`
- Dispatch route validation: `pass`
- Run manifest: `RUN-MANIFEST.md`
- Evidence index: `evidence-index.json`

## Blocked Fields

- `runtime_execution`: Josh has not yet confirmed the strategy.
- `subagent_execution`: Dispatch recommends reviewers, but authorization is `requires_user_permission`.
- `external_research`: Research mode is `research-if-gap-appears`; any external pass requires a named gap and confirmation.
