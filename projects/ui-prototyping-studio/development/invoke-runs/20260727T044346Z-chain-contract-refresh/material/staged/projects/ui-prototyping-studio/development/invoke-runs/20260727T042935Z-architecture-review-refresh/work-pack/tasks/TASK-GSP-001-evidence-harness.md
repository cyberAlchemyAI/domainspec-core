# TASK-GSP-001 — Deterministic Evidence Harness

## Primary Behavior

Start the Studio CLI and preview through the checked-in local `tsx` executable,
preserve command/stderr diagnostics, and reject immediately when the child
exits before producing its expected result.

## Dependencies

None.

## Write Scope

- `projects/ui-prototyping-studio/backend/e2e/helpers.ts`
- helper-focused test file only if needed

## Rules

1. Resolve the local executable from the backend package, not ambient Corepack
   or global `pnpm`.
2. Capture command, arguments, exit code, signal, stdout, and stderr for a
   failed CLI result.
3. `startPreview` must reject if the child exits before `/health` succeeds.
4. Successful preview shutdown remains explicit and bounded.

## Edge Cases

- missing local `tsx`;
- non-zero CLI exit with no JSON result;
- preview exit before port readiness;
- timeout while the child remains alive;
- normal explicit shutdown.

## Acceptance

- The standard checked-in command runs all current browser scenarios.
- A premature preview exit fails promptly with actionable diagnostics.
- No `/tmp` shim or ambient package-manager route is used.

## Validation

```sh
cd projects/ui-prototyping-studio/backend
./node_modules/.bin/playwright test --reporter=list
```

## Closeout

This task binds `SWU-GSP-001` to the Common Task Session Closeout Contract in
the parent work-pack. Its only admissible successor is `SWU-GSP-002`.
