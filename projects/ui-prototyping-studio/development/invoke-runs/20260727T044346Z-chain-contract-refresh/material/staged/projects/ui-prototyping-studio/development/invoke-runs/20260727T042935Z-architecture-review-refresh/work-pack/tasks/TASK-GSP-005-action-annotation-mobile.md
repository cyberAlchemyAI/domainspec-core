# TASK-GSP-005 — Action, Annotation, And Mobile Trust

## Primary Behavior

Durable Accept/Revert actions require actor-neutral explicit acknowledgment,
while annotation and narrow-screen comparison remain inspectable.

## Dependencies

`SWU-GSP-004`.

## Write Scope

- `backend/src/cli/studio.ts`
- focused desktop/mobile Playwright spec

## Decision

Acknowledgment is actor-neutral. Human and agent actors may acknowledge through
the same explicit contract when already authorized by the owning route.
Acknowledgment records inspection intent; it does not grant authority.

## Rules

1. Show candidate/revision identity, target state, and diff recap before
   Accept/Revert.
2. Require explicit confirmation state before the request is posted.
3. Do not expose Export as a browser mutation.
4. Disable annotation until a real target exists; constrain severity values.
5. Show selected target and captured-comment count.
6. At 390px, before/after panes stack or segment without horizontal document
   overflow.

## Acceptance

Desktop and 390px Playwright assertions prove the confirmation gate,
annotation unavailable/selected states, and inspectable comparison layout.

## Validation

```sh
cd projects/ui-prototyping-studio/backend
./node_modules/.bin/playwright test e2e/action-annotation-mobile.spec.ts --reporter=list
```

## Closeout

This task binds `SWU-GSP-005` to the Common Task Session Closeout Contract in
the parent work-pack. Its only admissible successor is `SWU-GSP-006`.
