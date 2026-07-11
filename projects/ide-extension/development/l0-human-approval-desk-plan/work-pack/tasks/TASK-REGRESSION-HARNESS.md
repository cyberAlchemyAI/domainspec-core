# TASK-REGRESSION-HARNESS

## Objective

Convert the accepted architecture-review reproductions into a deterministic local test harness before repairing production behavior.

- Layer/slice: L0 / S-001
- Wave: W0
- Dependencies: none
- Source contracts: [review findings](../../../architecture-review-2026-07-10/findings.md), [SPEC](../../../../SPEC.md), `src/server.mjs`, `tests/l0-smoke.test.mjs`
- Blockers: none

## Smallest Working Units

### SWU-IDEAD-001: Hostile Regression Harness

- Goal: prove the current implementation exhibits each accepted present-L0 defect through isolated temporary-state servers.
- Write scope: `tests/l0-adversarial.test.mjs`; `package.json` test-script entry only.
- Production write scope: none.
- Dependencies: none.
- Source anchors: findings AR-CAND-001 through AR-CAND-008; `createServer()`; `/api/envelopes/prepare`; `/api/approvals/:id/approve`; `/api/envelopes/run`.
- Related context: `tests/l0-smoke.test.mjs` listen/close/request helpers.

#### Required Cases

1. Caller-selected `approved_by` appears in a durable approval record.
2. Sequential replay creates a second successful receipt.
3. Concurrent replay allows more than one success or receipt.
4. Unknown `root.anything` grant persists.
5. Preparing B leaves pending A visible but unresolvable.
6. Concurrent disposition can make receipt events and projection receipts disagree.
7. A committed receipt has an `after_ref` that does not resolve.
8. Schema-invalid `context_refs` reaches durable state.

The baseline test may initially assert the observed defective outcomes and label them `known defect`; the repair SWUs invert those expectations one finding at a time. Do not use timing sleeps when a barrier/deferred promise can coordinate concurrency.

- Done criteria: all eight cases are deterministic across three consecutive runs and use fresh temporary state.
- Acceptance evidence: TAP output naming each review finding and a Task Session note recording the observed baseline.
- Validation: `npm run test:adversarial` three times; `npm run smoke` remains green.
- Execution owner: local-fallback.
- Handoff note: return the exact test names, observed statuses/counts, and any finding that could not be reproduced.

## Synchronization

Do not mark any architecture finding fixed. Record only baseline evidence and route to `SWU-IDEAD-002` and `SWU-IDEAD-004`.
