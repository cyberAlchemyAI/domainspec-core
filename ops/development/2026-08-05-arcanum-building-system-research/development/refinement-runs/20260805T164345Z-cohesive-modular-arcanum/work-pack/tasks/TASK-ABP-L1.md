# TASK-ABP-L1 — Failure Semantics and Second Boundary

Objective: prove an effectful closeout boundary and failure/compatibility behavior before extracting a common public protocol.

Dependencies: L0 receipts and unchanged native-owner invariants.

## SWU-ABP-004 — Task Session to Refresh adapter

- Behavior: project terminal/closeout package into Refresh input while preserving immutable pre-state, expected owner receipt, and no apply authority.
- Write scope: `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/adapters/task-session-refresh/`
- Acceptance: Refresh semantics preserved; cursor cannot precede joined post-Refresh identity.
- Validation: positive/no-op/missing-join/stale-prestate fixtures.

## SWU-ABP-005 — Outcome reconciliation

- Behavior: classify `outcome_unknown` and accept only effect-owner results `effect_absent`, `effect_committed`, or `manual_resolution_required`.
- Write scope: `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/reconciliation/`
- Acceptance: no automatic retry from unknown outcome.
- Validation: crash-window and idempotency-key fixtures.

## SWU-ABP-006 — Causal event projection

- Dependency: before admission, select exactly one mode: (a) fixture-only ephemeral emission with no durable write, or (b) an admitted local persistence owner bound by `DECISION-ABP-EVENTS`. A deferred owner decision cannot create durable storage.
- Behavior: project non-authoritative causal events with handles/digests and field classification.
- Write scope: `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/events/`
- Acceptance: no native verdict rewrite, no private payload by default, and no durable event write in ephemeral mode.
- Validation: hash-link, deduplication, redaction, owner-boundary fixtures, and a persistence-mode assertion that fails closed when neither mode is admitted.

## SWU-ABP-007 — Crash/concurrency fixtures

- Behavior: prove declared first stops for crash-after-effect and effect-boundary CAS/lease conflict.
- Write scope: `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/fixtures/failure/`
- Acceptance: forbidden downstream effects remain absent.
- Validation: deterministic failure runner.

## SWU-ABP-008 — Compatibility/privacy fixtures

- Behavior: prove version skew, downgrade, unknown-field, rollback, single-writer, and payload-taint rules.
- Write scope: `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/fixtures/compatibility/`
- Acceptance: all unsafe cases block; shadow reads never become writes.
- Validation: deterministic compatibility runner plus private-marker scan.

Each SWU has one primary behavior and independent acceptance. Closeout targets are `WORK-PACK.md`, this task, and `evidence-index.json`; Refresh owner receipt required. Successors: 004→005/006→007/008, then L1 gate.
