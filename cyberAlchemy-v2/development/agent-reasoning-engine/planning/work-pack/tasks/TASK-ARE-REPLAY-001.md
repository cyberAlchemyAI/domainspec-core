# TASK-ARE-REPLAY-001 — replay and revalidation

Layer: L1/L2. Depends on L0; SWU-005 also depends on protocol/current-source adapters.

## SWU-ARE-004 — historical replay

- Execution owner recommendation: `subagent`.
- Inputs: retained frame/snapshot/catalog/observations/challenge/decision/
  evaluator bytes plus expected digests and versions.
- Outputs: byte-stable replay outcome/derivation/receipt comparison or typed
  `not-replayable` report.
- Dependencies: G-ARE-L0; no actor protocol required.
- Write scope: `cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/replay/**` and replay fixtures only.

Algorithm: disable network/model/tool/resolver/effect ports; load exact retained
bytes; verify versions/digests; invoke unchanged deterministic evaluator; compare
outcome, derivation, and canonical receipt bytes; emit replay report. Missing or
invalid retained input returns not-replayable and never calls revalidation.

Done when deterministic, missing-byte, version, digest, and zero-call counter
fixtures pass. Verification: `node --test cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/replay/test/*.test.mjs`.

## SWU-ARE-005 — current revalidation

- Execution owner recommendation: `subagent`.
- Inputs: historical receipt handle, current governed source handles, new as-of
  time, current provider adapters.
- Outputs: new run/snapshots/receipt plus comparison and optional `Invalidated`;
  historical artifacts remain immutable.
- Dependencies: SWU-ARE-010/011/012/013/015, SWU-ARE-002/003 when fresh actors
  are required, and incident owner policy for post-effect drift.
- Write scope: `cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/revalidation/**` and drift fixtures only.

Algorithm: allocate new run ID; resolve current intent/authority/catalog/evidence
and time; execute current entry/protocol/evaluator path; compare governed
digests/outcomes; mark prior result invalidated when pinned rules require; route
post-effect cases to incident owner without automatic compensation.

Failure modes: scope expansion, expiry, revocation, catalog mutation, late
defeat, unavailable current source, unresolved incident owner.

Done when drift matrix proves new-run identity, no historical overwrite, typed
invalidity, and explicit incident routing. Verification:
`node --test cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/revalidation/test/*.test.mjs`.

Split rationale: immutable replay and fresh revalidation have opposite provider-
call contracts and independently reviewable acceptance.

Handoff
context is this task, retained L0/L1 receipts, replay/revalidation design rules,
and one selected SWU. Return the result shape in
[`../../EXECUTION-PACK.md`](../../EXECUTION-PACK.md).
