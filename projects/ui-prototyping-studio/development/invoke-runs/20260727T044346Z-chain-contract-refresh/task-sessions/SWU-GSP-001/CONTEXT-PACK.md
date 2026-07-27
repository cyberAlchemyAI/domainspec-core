# Context Pack — SWU-GSP-001

## Contract

- Task: `TASK-GSP-001`
- SWU: `SWU-GSP-001`
- Objective: make checked-in CLI/preview startup deterministic, local, and
  fail-fast.
- Allowed writes:
  - `backend/e2e/helpers.ts`
  - one helper-focused Playwright spec
- Acceptance-critical validation:
  `cd backend && ./node_modules/.bin/playwright test --reporter=list`
- Successor after joined closeout: `SWU-GSP-002` only.

## Controlling Sources

1. Parent work-pack and common closeout contract.
2. `TASK-GSP-001-evidence-harness.md`.
3. This strict context pack.
4. Current `backend/e2e/helpers.ts` bytes.

## Current Defects

- helper commands route through ambient `pnpm exec tsx`;
- failed CLI results merge stderr into stdout and omit command, args, signal,
  and distinct diagnostics;
- preview startup clears its timeout on premature exit without resolving or
  rejecting;
- shutdown sends an unbounded kill request without a fallback.

## Decisions

### Readiness probe

- Option A: add a new `/health` application route. This expands the task write
  scope and changes product code.
- Option B: probe the existing `/state` endpoint. This proves the process is
  listening, the selected session loads, and the HTTP server can serve a
  deterministic response.

Selected: Option B as the named accepted equivalent. Classification:
nonconsequential and reversible.

### Failure witness

Add one helper-focused Playwright scenario that starts preview with a missing
session and requires a prompt diagnostic rejection. Classification:
nonconsequential and reversible.

## Constraints

- Resolve `node_modules/.bin/tsx` relative to the backend package, independent
  of caller cwd.
- Preserve existing successful helper return shape while adding diagnostics.
- Do not create a `/tmp` shim.
- Keep explicit shutdown bounded with a SIGKILL fallback.
- No product source or lifecycle projection changes in this Task Session.

Strict coverage: pass.
