# Invoke Plan: Non-Executed Next Route

Status: flag
Owner: `invoke` via parent Refine coordinator
Mode: `plan`

## Recommended Next Route

Run `task-session` on a new preparatory unit:

`SWU-PAA-001R: Repair L0 Contract Handoff`

## Objective

Patch the root spec/design/work-pack artifacts so `SWU-PAA-001` has a concrete output tree, component/state boundaries, transcript redaction split, fixture semantics, fallback-abuse expectations, canary scope, and timing policy.

## Suggested Write Scope

- `projects/poker-agent-arena/DESIGN.md`
- `projects/poker-agent-arena/IMPLEMENTATION-LAYERING.md`
- `projects/poker-agent-arena/WORK-PACK.md`
- optional: `projects/poker-agent-arena/SPEC.md`
- optional: a provenance note under `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/`

## Acceptance Criteria

- `WORK-PACK.md` names the L0 docs/schema/fixture output tree for `SWU-PAA-001`.
- `DESIGN.md` includes the L0 component map and state namespace matrix.
- `IMPLEMENTATION-LAYERING.md` broadens hidden-information canary surfaces and separates transcript-derived diagnostics from scoring-derived fields.
- `SPEC.md`, if touched, resolves seed/replay visibility and deadline policy as contract-freeze targets rather than open runtime choices.
- The next route after repair remains `task-session` on `SWU-PAA-001`, not engine parity or novelty.

## Deferred Work

- Runtime implementation.
- Hold'em engine selection.
- Composite leaderboard scoring.
- Time-bank, bandwidth, adaptation, and explanation-tax mechanics.
