# Workflow Compensation v1

Status: canonical project-local runtime contract

This contract defines compensation without changing `DS-D1`, `DS-D8`, or the frozen Workflow v1
realization. It is admitted by the direct owner decision
`DSV2-OWNER-PRODUCT-ONTOLOGY-COMPENSATION-2026-08-29` and bound by baseline
`domainspec-meta-types-current-implemented@3`; baseline `@2` remains immutable historical evidence.

## Formal voice

```text
Compensation = (intent, plan, executor)

intent = (workflow_execution_id, failed_step_id, completed_step_journal)
plan   = topological_order(selected forward-recovery Operations)
executor(plan) = invoke exactly the selected Operations with deterministic idempotency keys

state ∈ {not-required, requested, running, completed, failed}

ordering:
  explicit Operation dependencies dominate;
  otherwise use reverse completed-step order;
  reverse completed-step order is also the deterministic tie-breaker.

authority boundary:
  Workflow evaluation may emit intent and plan but never executes compensation.
  A separate executor invokes the selected forward-recovery Operations.
```

Every compensation target is an ordinary `Operation`. It therefore owns its declared reads, writes, effects,
guard-before-mutation, atomic state-and-outbox boundary, idempotent behavior, events, and failure continuation.
The executor owns only ordering, exact binding, invocation, and compensation state transitions.

## Plain-language voice

Compensation is forward recovery, not time travel and not a database rollback. When part of a Workflow fails,
the Workflow records what completed and asks a separate runner to perform specifically declared recovery
Operations. The runner refuses unknown substitutions and stops at the first failed recovery Operation.

## Domain-context voice

DomainSpec represents both forward steps and compensation targets with the existing
`Workflow --[orchestrates]--> Operation` relationship. A Workflow body maps completed step IDs to compensation
Operation IDs and may declare `operation:depends-on:operation` entries. Generated Workflow artifacts expose the
five-state model and the external executor boundary in TypeScript, Python, and Rust. Target conformance rejects
missing Operation relationships, undeclared executor ownership, direct Workflow execution, dependency cycles,
missing runtime bindings, and substituted Operation IDs.

## State transitions

```text
failure with no selected recovery: not-required
failure with a nonempty plan:      requested -> running -> completed
                                                \-> failed -> retry | escalate | terminal-failure
```

The terminal continuation is owned by the failed compensation Operation binding. Retrying must reuse the same
idempotency key; it may not create another semantic compensation intent.

## Claim ceiling

This is a canonical project-local runtime contract. It does not change DS-D1 or DS-D8, grant publication,
release, deployment, or production authority, or prove durable dispatch and recovery after process restart.
