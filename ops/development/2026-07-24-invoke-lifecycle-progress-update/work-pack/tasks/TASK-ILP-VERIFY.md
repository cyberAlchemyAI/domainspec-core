# TASK-ILP-VERIFY: Recomposition and Promotion-Readiness Audit

## Objective

Prove ILP-R01 through ILP-R10 recompose without weakening existing gates,
leaking private evidence, or creating shadow authority.

- Layer/slice/wave: L3 / S3 / W3
- Lifecycle owners: Spellcraft, Sigil Development, transition-admission owner
- Dependencies: all SWU receipts
- Smallest Working Unit Exemption: closure-only `VERIFY` task
- Write scope: audit and lifecycle receipts only; any source repair becomes a
  new SWU or successor epoch

## Audit

1. Resolve every requirement through `../shared/TRACEABILITY.md`.
2. Verify all negative and positive controls against real entry points.
3. Verify exact mismatch remains fail-closed.
4. Verify same-epoch control mutation is impossible.
5. Verify every admitted transition names the ratified owner.
6. Verify read models and telemetry never admit or rewrite.
7. Verify Task Session still executes exactly one SWU and revalidates live.
8. Verify Refresh never performs target implementation and declares one kind.
9. Verify legacy plans gain no historical readiness.
10. Verify the live proof crosses admission without repair Refresh.
11. Scan public diffs and fixtures for private names, paths, and evidence.
12. Verify canonical/generated parity and run focused regressions.
13. List residue and return `pass`, `flag`, or `block`; do not promote.

## Validation

- all owner-focused fixture runners;
- Dispatch Spec route validation;
- public/private scan;
- generated parity;
- exact receipt-chain audit;
- scoped repository status and diff review.

## Completion evidence

`work-pack/session-evidence/TASK-ILP-VERIFY/final-audit.json` plus a human-readable
audit report and separate lifecycle-owner receipts.

## Closeout

Use `../shared/CLOSEOUT-CONTRACT.md`. Promotion, registry release, commit, push,
and publication remain separate maintainer decisions.

