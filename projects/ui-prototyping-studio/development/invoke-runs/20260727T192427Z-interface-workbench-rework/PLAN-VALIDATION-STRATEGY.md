# Plan Validation Strategy

Status: `draft-pending-plan-distill`

## Validation Surfaces

| Surface | Evidence |
| --- | --- |
| Type and compile | `./node_modules/.bin/tsc -p tsconfig.json --noEmit` |
| Application/domain unit behavior | `./node_modules/.bin/tsx --test "src/**/*.test.ts"` |
| Focused workbench behavior | `./node_modules/.bin/playwright test e2e/workbench-continuity.spec.ts --reporter=list` and task-specific specs |
| Full browser regression | `./node_modules/.bin/playwright test --reporter=list` |
| Design traceability | UPW-FIX-001–024 and UPW-VAL-* matrix review |
| Governance | current-head/staged, acknowledgment, Revert, Export regressions |
| Plan structure | JSON schema/uniqueness checks, link checks, SWU atomicity and dependency validation |

Commands run from `projects/ui-prototyping-studio/backend` use checked-in local
binaries. Corepack/pnpm is not an acceptance dependency.

## Slice Gates

- L0: deterministic projection identity, coherent snapshot, inert poll,
  trailing action refresh, rollback, and bounded context evidence.
- L1: each region passes independently before responsive/copy recomposition.
- L2: keyboard/focus/status and sandbox/route negatives pass, followed by the
  full current suite.
- L3: outside this Plan; automation cannot substitute for its owners.

## Evidence Ceiling

This strategy plans evidence. It does not claim any command has run. Chromium
may be the initial browser ceiling if receipts say so. Human outcomes,
cross-browser generalization, accessibility certification, release,
deployment, and production readiness remain unproved.
