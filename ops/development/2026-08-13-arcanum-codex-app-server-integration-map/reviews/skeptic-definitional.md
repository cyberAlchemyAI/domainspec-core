# Definitional-soundness review

Verdict: `FAIL`.

- `SD-001 FAIL`: transport denominator is false. Classify three inbound transports, disabled listen mode `off`, and outbound code-mode-host connection separately; never collapse process/listener/connection/thread.
- `SD-002 FAIL`: “Arcanum attempt” collapses Orchestrate action/event, Task Session attempt, and App Server thread/turn. Use distinct fields for Orchestrate action/agent, Task Session attempt, process instance, connection, thread, turn, and item/request. Fork requires separately admitted Task Session attempt.
- `SD-003 FAIL`: Task Session does not own domain semantic judgment. Chain raw host terminal → Task Session executor receipt → capability-owner verdict/receipt → Task Session reconciliation → owner-receipt closeout join → Task Session governance terminal receipt.
- `SD-004 FAIL`: generic `receipt` is ambiguous among host result, Orchestrate action receipt, Task Session executor, capability owner, Task Session terminal, proposed Craft apply, and eval result. Name exact schemas and prohibit substitution.
- `SD-005 FAIL`: “explicit Arcanum approval” is untyped. Separate App Server response, route confirmation, Decision Gate record, Goal batch token, capability-owner acceptance, and lifecycle promotion, with owner/scope/digest/one-use/consumed artifact.
- `SD-006 FAIL`: host fork/steer do not create Arcanum transitions. Describe host behavior first, then separately required adapter policy and prior Arcanum binding.
- `SD-007 FLAG`: one thread per attempt/SWU collapses cardinality. Use one executable thread per admitted Task Session attempt, with `swu_id` separate.
- `SD-008 FAIL`: rename “continuous Goal/Craft round” to bounded iterative Goal control loop. Type terminal state by machine; define node done evidence; call Craft artifact a proposed ledger-apply receipt until canonical schema exists.
- `SD-009 FLAG`: make Work-Pack authority explicit: Invoke authors; readiness audits without selecting/admitting; confirmation is prerequisite; Task Session issues live admission.
- `SD-010 FLAG`: eval verdict is fixture/canary evidence only and cannot yield owner receipt, acceptance, promotion, publication, or deployment. Inventory/observability remain projections.
- `SD-011 PASS`: the synthesis correctly denies implementation readiness and separates host success from lifecycle/external claims.

Selectors include canonical Orchestrate runtime/event schema, Task Session mutation/executor/terminal schemas, Work Pack/Implementation Readiness, Decision Gate, Goal, Craft, Inventory, Observed Invocation, and pinned App Server `thread.rs`, `turn.rs`, and `common.rs` cited by the reviewer return.

## Terminal recheck

`PASS`. All SD-001–SD-011 gates are precise. The identity chain now explicitly preserves `process_instance_id -> listener_id -> connection_id -> threadId`, with the outbound connector separate, and all authority/receipt/approval/evidence distinctions remain intact.
