# Explorer returns: RWO-managed Eve research runtime

The strategist persisted the following terminal narratives without changing their wording. Full structured evidence is in the adjacent role receipts.

## Agent 1 — Eve runtime explorer

The smallest sound seam is RWO command intent to one Eve root task session, followed by Eve session events back into RWO accepted-event handling. Disable Eve's agent and Workflow delegation surfaces so the seat model cannot become a scheduler. Use a generic leaf app when roles may be immutable command data; use separately addressable root apps if role prompts and tools must be filesystem-fixed. Before implementation, prove raw task launch, structured completion, duplicate-create handling, task-mode HITL, cancellation, crash recovery, and read-only sandbox behavior in one finite local fixture.

## Agent 2 — RWO control explorer

The smallest sound topology is:

```text
DomainSpec + human authority
  -> durable accepted-fact / gate projector
  -> RWO deterministic compiler and reducer
  -> generic bounded-seat CommandIntent
  -> delivery adapter
  -> eve as leaf executor
  -> validated receipt projection
  -> accepted event back into RWO
```

RWO may own deterministic graph identity, accepted-event reduction, duplicate detection, cursor derivation, and at-most-one immutable command intent. It must not own dispatch confirmation, evidence closure, physical delivery, model/tool approval, or effect claims. Eve must not schedule the research graph.

The current implementation cannot yet run this topology truthfully:

- `WorkGraph/1.0.0` has nodes and single-event edges but no join predicates, wave readiness, branch exclusion, role scopes, or loop semantics.
- One event may satisfy at most one edge; multiple matches reject.
- Payload derivation is only `copy-event-payload`, and the current registry contains only the fixture `job_id` payload schemas.
- The Go runtime stores cursor/outbox only in memory and deliberately has no journal, recovery, retry queue, or delivery.
- `CommandAdapter` exists as a boundary but `Service.Reduce` never invokes it.
- Orchestrate's native receipt schema carries lifecycle metadata and artifact paths, not the research payload itself. Exact downstream synthesis therefore needs a separately declared, content-addressed evidence return or a result handle.

## Agent 3 — Failure and authority explorer

The only sound target is **RWO-owned per-seat scheduling with Eve as a leaf task executor**, but real execution is **DEFERRED**. Current RWO is volatile and has no durable journal, recovery, delivery, or reconciliation path. The frozen Eve corpus also does not prove a caller-addressable, idempotent task-launch API.

At the pinned commit, declared Eve subagents are model-visible tools; cancellation may omit `subagent.completed`; transient model calls and recoverable Workflow steps can retry. The root-only Workflow tool lets the model orchestrate subagents.

DomainSpec owns strategy shape, tension, exact human confirmation, registration, stage readiness, evidence closure, final approval, and degraded-partial-result decisions. RWO/Rust owns accepted-event admission, compiled graph meaning, cursor transition, immutable command identity, duplicate/divergent/rejected classification, and whether a later command is semantically allowed. A durable Go host must own journal/outbox transactions, worker leases and fencing, physical delivery attempts, Eve session correlation, cancellation delivery, recovery, and reconciliation. Eve may own one bounded task session's model loop, internal checkpoints, structured output, restricted tools, and its documented internal retry behavior. Eve session durability is not RWO durability.
