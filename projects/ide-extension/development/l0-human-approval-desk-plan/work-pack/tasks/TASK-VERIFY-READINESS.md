# TASK-VERIFY-READINESS

## Objective

Audit L0 closure against the accepted review, run the complete validation surface, and prepare evidence-backed upstream synchronization proposals.

- Layer/slice: L0 / S-004 closure
- Wave: W3
- Dependencies: SWU-IDEAD-001 through SWU-IDEAD-009
- Gate status: ready-after-implementation
- Smallest Working Unit Exemption: task ID contains `VERIFY`; this task performs closure audit and synchronization proposals, not a new product behavior slice.

## Closure Checks

1. Map AR-CAND-001 through AR-CAND-008 to exact tests, code paths, and evidence artifacts in `work-pack/shared/traceability.md` or a generated closure report.
2. Confirm promotion-only AR-CAND-009 through AR-CAND-011 remain deferred and no L1+ effect entered the diff.
3. Run schema compilation/fixtures, smoke, adversarial, recovery/reference, and Playwright suites from a clean temporary state.
4. Inspect the final browser at desktop and mobile dimensions for text fit, overlap, focus, and evidence visibility.
5. Confirm the server still binds loopback by default and browser code contains no credentials.
6. Confirm every committed receipt reference resolves and event-derived state equals the persisted projection after restart.

## Validation Surface

```text
npm run validate:schemas
npm run smoke
npm run test:adversarial
npm run test:recovery
npm run test:e2e
```

Exact script names may be consolidated during implementation, but the evidence classes may not be dropped.

## Conditional Synchronization

- Update `README.md`, `SPEC.md`, and `ARCHITECTURE.md` only when passing implementation evidence supports the new behavior.
- Prepare a Craft ledger delta replacing the stale Playwright-first frontier with completed repair evidence and the next honest frontier.
- Apply the Craft delta only through an explicit approved Craft operation.
- Update work-pack/task status only with concrete completion receipts.

## Done Criteria

- Full validation is green or the task returns FLAG/BLOCK with exact failing evidence.
- The closure matrix has no unsupported `fixed` claim.
- Documentation/Craft changes are either approved and applied or clearly staged with their required approval.
- The next route is one of: L0 pilot, repair residue, or separately approved L1 planning.
