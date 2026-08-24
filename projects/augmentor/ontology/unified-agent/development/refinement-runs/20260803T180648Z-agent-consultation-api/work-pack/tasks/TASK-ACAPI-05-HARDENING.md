# TASK-ACAPI-05: Reliability And Policy Hardening

- Layer/slice: L2 / S-004.
- Dependencies: L1 executed witness; the failure suite also requires
  SWU-ACAPI-010 and SWU-ACAPI-013.
- Blocker: B-004 before fixed production defaults.

## SWU-ACAPI-010: Access-isolated Evidence Cache

- Primary behavior: reuse only immutable authorized evidence within one access
  equivalence class.
- Acceptance: cache key binds all repaired H8 fields; fresh envelopes are built
  per request; no payload crosses principal, policy, or access classes.
- Split analysis: key, immutable payload, and access isolation are one caching
  behavior.
- Write scope:
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/cache.ts`
  and
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/cache.test.ts`.
- Validation: targeted Vitest with two principals and two policy classes.
- Evidence: result 010.

## SWU-ACAPI-013: Deadline And Cancellation Propagation

- Primary behavior: stop candidate scans, joins, hydration, and response work at
  the effective deadline or cancellation signal.
- Acceptance: no read or hydration begins after termination; the result follows
  the mechanical `budget_exceeded` or `temporary_failure` rule.
- Split analysis: deadline and cancellation are two triggers for one bounded
  request-lifetime behavior and one propagation boundary.
- Write scope:
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/deadline.ts`,
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/projection-reader.ts`,
  and
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/deadline.test.ts`.
- Validation: targeted Vitest with deterministic clocks and cancellation probes.
- Evidence: result 013.

## SWU-ACAPI-011: Failure-injection Suite

- Primary behavior: preserve fail-closed result semantics under denial, drift,
  timeout, oversized input, conflicting structured data, and prompt injection.
- Acceptance: QS-04-QS-14 pass against the integrated service; no false
  `no_match`, `ok`, authority, or protected effect.
- Split analysis: one invariant is under test across independent stressors.
- Write scope:
  `../workspace-resonant/2.0.0-alpha/src/core/augmentor-consultation/failure-injection.test.ts`
  only unless a failure exposes one separately admitted repair.
- Validation: targeted Vitest, build, and deterministic counter assertions.
- Evidence: result 011.
