# Implementation Layering: Invoke Lifecycle Progress Protocol

## Boundary heuristic

A layer advances only when it answers one new decision question and retains the
earlier fail-closed witnesses. Complexity beyond the demonstrated lifecycle
loop is deferred.

| Layer | Decision question | Minimum working unit | Included | Deferred | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | Who may admit lifecycle transitions, and where may generic contracts live without creating competing authority? | `SWU-ILP-001` owner/source-placement decision | authority split, public/private boundary, source ownership | schemas, integration, migration | signed lifecycle decision naming one owner, source paths, and non-authority projections | proceed only when one owner is named and Invoke/Refresh/Task Session/read models are explicitly excluded from implicit authority |
| L1 | Can deterministic contracts reject incomplete epochs, invalid edges, incompatible roles, and unsafe same-epoch repairs before capability integration? | `SWU-ILP-002` epoch/control-graph validator | epoch issuance, transition relation, local/external readiness, exact supersession rule, red/green fixtures | Plan, Refresh, Task Session mutation | schema and focused validator suites; all causal negative controls fail for named reasons | integrate only if exact digest behavior and one-SWU identity remain unchanged |
| L2 | Can Plan, Refresh, and Task Session exchange the new evidence without owning one another's work? | Plan emits separate authored/readiness verdicts | Plan epoch/readiness, Refresh kinds/drift, Task Session consumption and live admission | legacy migration, telemetry, live proof | owner lifecycle receipts, generated parity, stale/mismatch controls, no target implementation in Refresh | migrate only if each capability remains inside its authority boundary |
| L3 | Can old plans enter safely and can a generic live run demonstrate progress without repair churn? | one legacy plan becomes freshly admitted, not retroactively ready | legacy admission, progress projection, churn detection, generic live experiment, full recomposition | promotion, publication, broader manifest normalization | live run crosses admission without repair Refresh; exact drift still blocks; terminal audit and reflection | lifecycle owner may assess promotion readiness; never infer release |

## Non-regression guardrails

- Task Session executes exactly one SWU.
- Invoke authors; it does not implement target work.
- Refresh performs no target implementation.
- Exact byte mismatch always invalidates the old exact join.
- Task Session independently rereads live controlling evidence before mutation.
- External, delegated, and reusable packages retain exact material validation.
- Same-epoch readiness can advance only when the epoch control digest is
  unchanged.
- Every control change creates a successor epoch and retains the old receipt
  chain.
- Inventory, telemetry, projections, status files, and cursors remain
  non-authoritative.
- Public Arcanum receives generic contracts only.

## Recommended next layer

- Next layer: L0.
- Selected unit: `SWU-ILP-001`.
- Decision unlocked: whether there is a legitimate single transition-admission
  owner and an owner-approved public location for the protocol.
- Mutation: none.
- Major deferred scope: every canonical source edit.

