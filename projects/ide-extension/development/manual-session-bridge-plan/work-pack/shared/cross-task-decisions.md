# Cross-Task Decisions

## Approved Product Decisions

| ID | Decision | Source |
| --- | --- | --- |
| DG-MSB-001 | L0 is read/preview-only. | approved `DECISIONS.md` |
| DG-MSB-002 | Authorization and execution use separate typed receipts. | approved `DECISIONS.md` |
| DG-MSB-003 | Only the operator releases/requeues interrupted claims. | approved `DECISIONS.md` |
| DG-MSB-004 | Session refs are local and unattested. | approved `DECISIONS.md` |
| DG-MSB-005 | Exactly one proposal is selected ready in the desk before poll. | approved `DECISIONS.md` |

## Planning Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| DEC-MSBP-001 | Preserve v1 event logs and add version-aware v2 reducers; never rewrite history. | Brownfield state may exist in checked-in or temporary roots. |
| DEC-MSBP-002 | Evolve `receipt.schema.json` as a discriminated union: legacy v1, v2 authorization, v2 skill execution. | Keeps one registered receipt boundary while making claims non-overlapping. |
| DEC-MSBP-003 | Approval authorization is consumed by admitted terminal result, not by claim; operator release may reuse it only in L0 read-only mode. | Required by selected recovery policy. |
| DEC-MSBP-004 | Pending rejection remains existing behavior; approved/ready cancellation revokes authorization, preserves its receipt, and terminalizes as blocked/revoked. | Fail-closed operator control without erasing audit history. |
| DEC-MSBP-005 | Session helper is a one-shot HTTP CLI/protocol, not an executor or background poller. | Makes manual Codex operation reproducible without adding a worker. |
| DEC-MSBP-006 | Real manual witness is last and manual-owned; deterministic claimant tests are the automated oracle. | Avoids treating chat behavior as the only regression surface. |

## Assumptions

- Event version 2 is emitted only after v1 replay tests pass.
- Existing legacy receipts remain inspectable and are projected with an honest
  legacy kind without changing stored events.
- `ready_for_poll` singleton enforcement is inside the serialized mutation
  boundary, not a UI-only check.
- Operator/session actor classes are kernel-created descriptors; callers cannot
  supply identity claims.
- The CLI prints JSON and never stores skill/prompt data outside the active
  process unless the session explicitly writes a bounded result file.

## Deferred Decisions

- Timed leases and automatic retries: L1.
- Authenticated session identity and pairing: L2/L3.
- Write/network effect enforcement: L2 executor adapter.
- Persistent worker, push/wake, IDE packaging: L3.
