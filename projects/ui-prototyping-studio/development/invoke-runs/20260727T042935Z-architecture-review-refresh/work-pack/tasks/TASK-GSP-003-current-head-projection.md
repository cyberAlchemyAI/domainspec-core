# TASK-GSP-003 — Application-Owned Current-Head Projection

## Primary Behavior

One application-owned typed projection selects the primary current-head
artifact and matching annotation target from fresh governed state.

## Dependencies

`SWU-GSP-002`.

## Write Scope

- new application projection module near `application/current-html.ts`
- `backend/src/cli/studio.ts`
- projection unit tests
- focused Playwright spec

## Inputs And Output

Inputs: fresh session, artifact content port, staged record, revision lineage,
comments, and handoff metadata.

Output: serializable projection containing current-head content/route,
annotation route and revision ID, historical variant references, staged/current
labels, diff lanes, action availability, and evidence status.

## Rules

1. Reuse `resolveCurrentHtml`; the adapter must not decide current truth.
2. Current head is primary after Accept and Revert.
3. Annotation uses the same current content and revision identity.
4. Original variants remain clearly labeled historical lineage.
5. Unavailable content produces an explicit unavailable state.

## Acceptance

Focused browser witnesses prove Accept, Revert, and external-write current head
for the primary preview, annotation iframe, and `/state`.

## Validation

```sh
cd projects/ui-prototyping-studio/backend
./node_modules/.bin/tsc -p tsconfig.json --noEmit
./node_modules/.bin/tsx --test "src/**/*.test.ts"
./node_modules/.bin/playwright test e2e/governed-state-projection.spec.ts --reporter=list
```

## Closeout

This task binds `SWU-GSP-003` to the Common Task Session Closeout Contract in
the parent work-pack. Its only admissible successor is `SWU-GSP-004`.
