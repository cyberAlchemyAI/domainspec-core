# Execution Pack — WP-CAL-TEN-L0

## Control fields

- Planning gate: `pass`
- Complexity: `medium`
- Baseline wave: W0
- Active layer window: L0
- Work Pack: `WORK-PACK.md`
- Layering: `IMPLEMENTATION-LAYERING.md`
- Readiness profile: pilot mechanics proof, not product/release readiness

## Choreography

```text
W0: CAL-001
  -> W1: CAL-002 -> 003 -> 004 -> 005 -> 006
    -> W2: CAL-007 -> 008
      -> W3: CAL-009 -> 010
        -> stop at synthetic L0; separate corpus-owner L1 route
```

Every arrow requires a passing Task Session execution receipt and a passing Invoke Refresh closeout receipt. The current execution-entry projection exposes only CAL-001; closeout deterministically advances a future one-unit projection.

## Wave table

| Wave | Layer | Tasks | SWUs | Exit gate |
| --- | --- | --- | --- | --- |
| W0 | L0 | CAL-CONTRACTS | 001 | deterministic canonical identity primitive |
| W1 | L0 | CAL-CONTRACTS, CAL-PACKAGE | 002-006 | closed valid synthetic graph |
| W2 | L0 | CAL-COMPILER | 007-008 | deterministic compile plus 15 exact failures |
| W3 | L0 | CAL-SNAPSHOT, CAL-WITNESS | 009-010 | separate package/witness identity and independent evidence |

## Parallelization boundary

No product SWUs are parallelized in this first Work Pack. Dependencies are semantic and byte-bound; overlapping package identity plus one-file closeout projection makes speculative parallelism costlier than the limited speed gain.

## Closure obligations

- Product commands run only in Task Session after a separate execution request.
- Closeout updates only exact plan state/evidence targets.
- Failed acceptance-critical validation blocks before next SWU.
- L0 completion cannot select or admit a real tower and cannot dispatch IDE work.

