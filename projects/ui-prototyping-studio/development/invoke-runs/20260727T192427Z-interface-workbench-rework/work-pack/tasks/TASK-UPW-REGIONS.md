# TASK-UPW-REGIONS — Six Workbench Regions

## Objective

Implement each selected region as an independently reviewable keyed surface,
serially, without coarse rerender or authority changes.

- Layer/wave: L1 / W2
- Source: Architecture View 2, UX Plan Surface Contracts
- Dependencies: SWU-UPW-007
- Shared write scope: `backend/src/cli/studio.ts`, workbench shell/renderer
  modules, focused Playwright specs. Serial execution is mandatory.

| SWU | Primary behavior | Done criteria | Validation | Split analysis |
| --- | --- | --- | --- | --- |
| SWU-UPW-008 | Lifecycle/next-action spine | exact state, identity, progress, next action, connection status; no staged/current collapse | focused state matrix and UPW-FIX-014 | state spine is one identity/action summary; canvas or action controls pass separately |
| SWU-UPW-009 | Current governed canvas | current-head label/frame stays stable when its source identity is unchanged | governed projection + iframe navigation counters | canvas identity is independent from annotation, review, and history |
| SWU-UPW-010 | State-specific contextual inspector | annotation/batch/revision context appears only with required identity; disabled reasons visible | UPW-FIX-003, 006, 008 | inspector context is independent from canvas rendering and durable actions |
| SWU-UPW-011 | Staged review | candidate identity, diff, named Before/current and After/candidate frames, acknowledgment context | UPW-FIX-007, staged/current governance negatives | review evidence can pass before action handlers |
| SWU-UPW-012 | Governed actions and scoped feedback | Accept/Discard/Revert call existing handlers; exact ack gates and `act-msg`/`act-msg2` scopes | UPW-FIX-004, 009–010, 014 | action transport/feedback is independent from review layout |
| SWU-UPW-013 | Collapsed historical lineage | history is labeled non-current, follows active work, retains expansion state | UPW-FIX-013 plus expansion continuity | lineage is a secondary surface and can pass without responsive polish |

Dependencies are serial: 008 -> 009 -> 010 -> 011 -> 012 -> 013.

## Implementation Rules

- Region data comes only from the server projection.
- Outer data uses `textContent`, explicit nodes, and allowlisted attributes.
- Prototype HTML stays in sandboxed route frames.
- Each renderer writes only its mount and has a stable identity/version.
- An unavailable region renders an exact state-specific explanation, not a
  fake action or empty historical card.
- Durable actions retain current application use cases and server stale checks.

## Validation

Each SWU runs its named focused Playwright slice. Task closeout additionally
runs:

`./node_modules/.bin/playwright test e2e/governed-state-projection.spec.ts e2e/action-annotation-mobile.spec.ts --reporter=list`

## Execution Owner And Handoff

Each SWU owner is `subagent`. Handoff includes only that region’s UX contract,
projection fields, current selector anchors, dependency receipt, and expected
UPW evidence. Return the standard SWU result; no region completion selects the
next SWU automatically.
