# TASK-GSP-004 — Visible Style And Global Diff Evidence

## Primary Behavior

A visible CSS/style/global mutation always produces explicit diff evidence even
when no component fragment can own it.

## Dependencies

`SWU-GSP-003`.

## Write Scope

- `application/admission.ts`
- diff domain model/types
- projection, preview, and handoff consumers
- unit and focused browser tests

## Rules

1. Preserve existing per-`data-od-id` structural fragments.
2. Compare style raw text or a stable canonical style representation.
3. Report style/global/unattributed evidence in a separate lane.
4. Never describe a CSS-only visible mutation as zero change.
5. Do not invent component attribution when selectors span or miss IDs.

## Acceptance

A CSS-only fixture produces non-empty explicit style/global evidence in the
domain result and pending browser review.

## Validation

```sh
cd projects/ui-prototyping-studio/backend
./node_modules/.bin/tsx --test "src/**/*.test.ts"
./node_modules/.bin/playwright test e2e/governed-state-projection.spec.ts --reporter=list
```
