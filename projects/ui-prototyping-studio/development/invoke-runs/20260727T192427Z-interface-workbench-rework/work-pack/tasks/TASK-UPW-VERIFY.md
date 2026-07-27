# TASK-UPW-VERIFY — Closure Verification

## Objective

Verify recomposition, full regression, residue, and claim ceilings after
SWU-UPW-001–017 complete.

- Layer/wave: L2 / W5
- Dependencies: all mutation SWU receipts
- Gate: ready-after-W4

## Smallest Working Unit Exemption

Exempt because the task ID includes `VERIFY` and owns closure evidence only. It
must not mutate implementation. Any required source repair opens or routes to a
new SWU; it is not performed inside this task.

## Checks

From `projects/ui-prototyping-studio/backend`:

```bash
./node_modules/.bin/tsc -p tsconfig.json --noEmit
./node_modules/.bin/tsx --test "src/**/*.test.ts"
./node_modules/.bin/playwright test --reporter=list
```

Also verify:

- UPW-FIX-001–024 each has one planned-to-executed receipt mapping;
- all six views and seven selected architecture extensions recompose;
- no `location.reload()` remains in polling or successful action paths;
- current/staged/acknowledgment/Revert/Export gates remain exact;
- no unexpected source, generated, or browser residue;
- human/cross-browser/certification/release gaps remain explicit.

## Completion Evidence

One closure report with exact command results, receipt inventory, failing
checks if any, and next owner. A passing closure report may recommend the
separate human-study/readiness route; it cannot authorize it.
