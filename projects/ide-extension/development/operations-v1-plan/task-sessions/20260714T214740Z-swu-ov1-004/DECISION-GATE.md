# Decision Gate: Operations V1 Interaction Event In V4

- Target scope: `SWU-OV1-004`
- Status: PASS
- Opened: 2026-07-14
- Decisions resolved: 1
- Blockers remaining: 0
- Source: Task Session evidence review

## Blocker Question

How should Operations V1 interaction records enter event version 4 when the
SWU-OV1-001 frozen vocabulary contains only five non-interaction event names,
but SWU-OV1-004 and SWU-OV1-010 require a V4 interaction record?

## Option 1: Reuse `canvas.interaction_recorded` In V4 - Recommended

**Benefit:** preserves the existing semantic event name while `event_version`
selects V0/V3 versus Operations V1/V4 bindings. It keeps browser code and event
queries conceptually simple.

**Cost/risk:** requires an explicit migration note and update to the SWU-001
event vocabulary/test from five to six names. Reducers must strictly distinguish
the V3 and V4 interaction record shapes.

**When to choose:** when interaction means the same user action category across
V0 and Operations surfaces, with versioned target binding.

**Downstream impact:** SWU-004 freezes the six-name V4 vocabulary and reducer;
SWU-010 emits the V4 form for displayed Operations revisions while retaining V3
for displayed V0 revisions.

## Option 2: Add `canvas.operations_interaction_recorded`

**Benefit:** makes Operations V1 interactions visibly distinct in audit queries
and avoids overloading the V3 event name.

**Cost/risk:** adds a new public vocabulary term and branching across browser,
projector, fixtures, and future analytics. It still requires a SWU-001 contract
migration.

**When to choose:** when operations interactions should be treated as a
different audit category rather than a versioned form of Canvas interaction.

**Downstream impact:** SWU-010 and all consumers must use the operations-specific
name; cross-version interaction queries must include both names.

## Option 3: Defer V4 Interaction Until SWU-010

**Benefit:** lets SWU-004 implement derivation/operation replay without changing
the frozen five-name vocabulary now.

**Cost/risk:** SWU-004 cannot honestly claim its declared complete V4 vocabulary
or full projected-state contract. SWU-010 would reopen replay authority and
retroactively migrate SWU-004 fixtures.

**When to choose:** only when early blob/replay progress is more important than
freezing the complete event contract in its owning SWU.

**Downstream impact:** SWU-004 remains FLAG rather than PASS; SWU-005 should not
be promoted under the current gate rule unless the work pack is explicitly
amended.

## Explain / More Context

This does not select an option. It requests a deeper walkthrough of why event
version and event name are separate compatibility axes, which fixtures change,
and how each option affects SWU-010 browser interaction routing.

## Recommendation

Choose **Option 1**. The action is still a Canvas interaction; event version 4
already supplies the Operations V1 semantic boundary. The migration is small,
explicit, and avoids creating two names for one user action category.

## Decision Record

- Selected option: Option 1, reuse `canvas.interaction_recorded` in V4
- Rationale: event version distinguishes V3/V4 target bindings while preserving one semantic Canvas interaction name
- Source of decision: human response `1` on 2026-07-14
- Remaining blockers: none
- Consequential code mutation: authorized within SWU-OV1-004 write scope
- Migration evidence: `../20260714T215322Z-swu-ov1-004-resume/EVENT-V4-MIGRATION.md`
