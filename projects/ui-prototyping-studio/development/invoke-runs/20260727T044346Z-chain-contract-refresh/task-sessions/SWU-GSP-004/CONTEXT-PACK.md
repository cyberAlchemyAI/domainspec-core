# Context Pack — SWU-GSP-004

## Contract

- Task: `TASK-GSP-004`
- SWU: `SWU-GSP-004`
- Dependency: joined passing `SWU-GSP-003` receipts.
- Objective: CSS/style/global visible mutations always yield explicit evidence,
  including when structural component counts are zero.
- Allowed writes: diff domain/application, projection, preview, handoff
  consumer, persistence clone, and focused tests/fixture.
- Acceptance-critical validation: typecheck, full units, focused browser
  witness.
- Successor after joined closeout: `SWU-GSP-005` only.

## Current Defect

`diffByOdId` deliberately excludes `<style>` elements. A CSS-only admitted
candidate can therefore report `added=0`, `changed=0`, `removed=0`; projection,
preview, revision, and handoff all preserve that false-zero evidence.

## Evidence Shape

Preserve structural `data-od-id` fragments and counts. Add required lanes:

- `style`: stable before/after style text, added/removed rule counts,
  `changed`, and explicit `global-unattributed` attribution;
- `unattributed`: explicit structural counts whose nearest `data-od-id` is
  absent;
- `visibleChangeCount`: structural total plus one when style text changed.

The lane does not invent component ownership for selectors spanning the page.
The accepted revision and handoff bundle retain the same evidence, and the
pending browser UI renders it separately from per-component fragments.

Strict coverage: pass.
