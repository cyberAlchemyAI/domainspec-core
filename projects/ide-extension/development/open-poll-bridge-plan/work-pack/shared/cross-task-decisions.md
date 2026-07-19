---
module: ide-extension-open-poll-bridge
status: planned
docType: cross-task-decisions
---

# Cross-Task Decisions

| ID | Decision | Applies To | Rationale |
| --- | --- | --- | --- |
| OPB-PD1 | L0 is open singleton availability, not a queue. | all tasks | Proves value with minimum overhead. |
| OPB-PD2 | `agent_ref` is bound at claim time. | contract, API, receipts | Availability should not predict the claimant. |
| OPB-PD3 | Result identity is derived from stored claim state. | API, witness | Prevents terminal identity drift. |
| OPB-PD4 | Ready endpoint query `agent_ref` is ignored or removed as selector. | API, CLI | Backward compatibility may tolerate it, but it cannot decide availability. |
| OPB-PD5 | Codex may remain a default CLI label only. | CLI, UI | Codex is the first use case, not the protocol authority. |
| OPB-PD6 | No background poller, lease, queue, or session registry enters L0. | all tasks | Those are later operational layers. |
