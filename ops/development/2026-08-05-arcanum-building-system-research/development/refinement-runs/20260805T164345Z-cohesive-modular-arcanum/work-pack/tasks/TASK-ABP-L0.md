# TASK-ABP-L0 — Prove One Bilateral Boundary

Objective: prove WPRA selected-unit → Task Session entry projection without modifying owner contracts.

Dependencies: admitted protocol capability/steward decision from `TASK-ABP-READINESS`.

## SWU-ABP-001 — Selection projector

- Primary behavior: deterministically project one current WPRA selection receipt into an OBTC envelope while preserving the native handle, digest, `authority_effect:none`, and Task Session consumer.
- Split analysis: schema projection and validation are independently testable, so validation is SWU-002.
- Write scope: `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/adapters/wpra-task-session/`
- Done: golden projection plus missing/stale field diagnostics; no owner writes.
- Validation: exact JSON comparison and native receipt hash preservation.
- Execution owner: Task Session/local fallback under later approval.

## SWU-ABP-002 — Structural validator

- Primary behavior: return stable structural pass/block diagnostics without invoking semantic policy or effects.
- Split analysis: one pure validation behavior; fixtures are SWU-003.
- Write scope: `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/protocol/`
- Done: role singularity, identity/digest, version, gate/receipt, replay/freshness checks; forbidden semantic/effect call test.
- Validation: schema fixtures and forbidden-operation test.
- Execution owner: Task Session/local fallback under later approval.

## SWU-ABP-003 — L0 shadow fixtures

- Primary behavior: compare native boundary fixtures to projected envelopes without a second authoritative write.
- Split analysis: the suite first proves field and diagnostic preservation. A stronger semantic-preservation claim is a separate consumer-owner judgment and requires a Task Session owner-native shadow acceptance/compatibility receipt.
- Write scope: `ops/development/2026-08-05-arcanum-building-system-research/prototype/build-protocol/fixtures/l0/`
- Done: positive plus stale/version/role/digest/kernel-policy negatives pass; native bytes unchanged; Task Session owner-native shadow acceptance is present before any semantic-equivalence wording is admitted.
- Validation: fixture runner, source hashes before/after, scoped whitespace check, and exact owner-native acceptance receipt check.
- Execution owner: Task Session/local fallback under later approval.

Closeout for each SWU: synchronize `WORK-PACK.md`, this task, and `evidence-index.json`; expected owner receipt is Invoke Refresh apply-approved/no-op. Successors are 001→002→003; after 003, `SWU-ABP-004` only when the L0 gate passes.
