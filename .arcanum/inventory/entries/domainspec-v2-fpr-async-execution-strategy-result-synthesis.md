---
tags: [inventory, strategy-result, dispatch, subagents, research, v2-repo, domainspec, operational-evidence, claim-le-proof, non-collapse]
node_type: synthesis
is_session: false
layer: strategy
nature: synthesis
status: flag
created: 2026-07-16
dispatch_id: 2026-07-16-fpr-async-execution-strategy
dispatch_type: research
working_folder: projects/domainspec-v2/development/first-production-release/research/2026-07-16-async-execution-strategy/
sources: [projects/domainspec-v2/development/first-production-release/research/2026-07-16-async-execution-strategy/research.md, projects/domainspec-v2/development/first-production-release/research/2026-07-16-async-execution-strategy/findings.md, telemetry/agents/subagents-dispatch.yaml, projects/domainspec-v2/.craft/ledger.yml]
---

# DomainSpec v2 FPR Async Execution Strategy Result

This is a non-authority Inventory read model of the resolved research dispatch
`2026-07-16-fpr-async-execution-strategy`. It makes the accepted concurrency
model and implementation gaps searchable without authorizing an FPR mutation,
closing a task, synchronizing Craft, selecting a successor, promoting an
authority artifact, or claiming a measured speedup.

## P1 Trigger Decision

Dispatch was required because the question combined three independently
falsifiable dimensions: formal DAG readiness, empirical shared-resource
independence, and governance authorization. The source corpus crossed the FPR
task graph, receipts, Craft continuation state, owner decisions, implementation
packages, shared runners, Git state, and dispatch-type law. Independent
explorers and attack-vector reviewers were needed to prevent file disjointness,
agent capacity, or accepted-looking evidence from being mistaken for execution
authority.

## Lanes And Subagents

- Goldratt reconstructed the exact FPR-01 through FPR-04 dependency chain,
  critical path, current frontier, and safe precomputation boundary.
- Hewitt mapped file, runner, Git, ledger, inventory, roadmap, and submodule
  collisions and produced the three-slot operating schedule.
- van Lamsweerde separated technically possible work from research, Task
  Session, Decision Gate, source-owner, verification, ratification, and
  synchronization authority.
- Beer synthesized the three lenses into a candidate manual operating model.
- Tetlock attacked precedent and distinguished deployed controls from proposed
  machinery.
- Popper attacked non-vacuity and required machine-discriminating state,
  side-effect, freshness, and speculation boundaries.
- Russell attacked definitional collapse across execution, preparation,
  diagnostics, receipts, task closure, synchronization, and promotion.
- Turing wrote the durable `findings.md` artifact only.
- Vlachopulos independently audited the result and returned `ACCEPT` without a
  writer revision.

## Dependency Flow And Gate State

The executed flow was
`explorers -> synthesizer <-> reviewers -> writer -> auditor`. One bounded
synthesizer/reviewer convergence loop ran. The auditor accepted the first
written findings artifact, so the auditor-to-writer feedback edge did not fire.

- P1 gate: dispatch required.
- Check-tension: the corrected sheet passed independent checker and reviewer
  gates before launch.
- Human gate: explicitly confirmed before registration.
- Registration: exactly one schema-`0.6.0` dispatch row was appended through
  the deterministic appender.
- Closeout: exactly one close row records `exit_reason: resolved`, nine agents,
  no helpers, and `loops_used: 1`.
- Final audit: `ACCEPT`, scoped to the research report only.

The dedicated research-writing and findings-writing packages referenced by the
dispatch pipeline were absent from this checkout. The parent preserved the
three explorer returns verbatim in `research.md`, and the registered writer
alone authored `findings.md` under an explicit one-file fallback contract.

## Accepted Result

The current FPR-01 through FPR-04 execution projection is structurally width
one. Its 14 SWUs form a predecessor-receipt chain, and only one SWU may be
selected for governed mutation at a time. This is a fact about the bounded FPR
projection, not a universal DomainSpec graph law.

Current agent capacity can keep three asynchronous lanes occupied with
registered research, review, diagnostics, and tightly allowlisted preparation.
That does not widen mutation authority and does not prove wall-clock speedup.
Present-day scheduling is manual and parent-enforced; no automated scheduler,
lock manager, snapshot system, or ready-queue controller was found.

## Non-Collapsed Current State

FPR01-002 must remain a state vector rather than a single complete/incomplete
label:

```text
decision_packet         = accepted
tracking                = untracked
task_receipt            = absent
continuation_sync       = stale
successor_authorization = denied
```

`SWU-FPR01-001` has a verified PASS receipt, while Craft still points at that
completed unit. The accepted FPR01-002 owner packet preserves decisions, but it
explicitly denies FPR01-003 execution authority. Therefore the authorized
`EXECUTE` queue is empty.

## Manual Operating Epochs

1. **Present stale state:** reconcile the FPR01-001 receipt and Craft, review
   the FPR01-002 packet and missing closure route, and prepare only allowlisted
   questions, invariants, mutants, or checklists.
2. **Authorized mutation:** one Task Session writer mutates the exact selected
   SWU while the other lanes remain side-effect-reviewed diagnostics or
   allowlisted preparation.
3. **Procedural no-write validation:** mutation stops; positive/negative checks
   and static review run over the complete candidate. This is not immutable
   snapshot isolation.
4. **Receipt and independent verification:** the candidate receipt binds the
   evidence, then a named independent verifier accepts or rejects it. Failure
   returns to mutation and revalidation; pass closes the task.
5. **Continuation:** separate approval updates Craft from the verified receipt;
   derived views refresh afterward; only then may the unique successor be
   selected.

Shared runners, build outputs, caches, package state, Git index/worktree,
Craft, roadmap generation, dispatch ledger, inventory, authority changes, and
publication remain parent-serialized until real isolation or lock machinery
exists.

## Proposed Machine Model

The research proposes, but does not implement:

- a deterministic reconciler that computes readiness from receipts, Craft,
  derived views, selection, decisions, context, writer authority, inputs,
  validation plans, and exclusive-resource scheduling;
- a heterogeneous WorkItem record separating operation kind, durable and
  transient writes, authority effect, prerequisites, assumptions, resources,
  and output scope;
- a governed PREP allowlist limited to questions, source indexes, invariants,
  mutant catalogs, checklists, and test plans;
- an explicit prohibition on final schemas, fixtures, validator code,
  canonical artifacts, receipts, generated projections, and successor outputs
  as preparation;
- a freshness manifest whose anchor mismatch moves preparation to `STALE`
  while preserving lineage; and
- priority, maximum speculative distance, TTL, and rework budgets before
  speculative preparation can be optimized safely.

These are implementation gaps, not current controls or new ontology kinds.

## Immediate Governed Move

Preserve the accepted FPR01-002 decisions; do not re-infer them. First define
and obtain owner authorization for an adoption/closure route that explains how
the existing untracked packet is bound into one exact Task Session and receipt.
A narrow authorization may combine FPR01-001 receipt reconciliation, exact
selection of FPR01-002, and an exact Task Session boundary, but it must be
explicitly selected rather than inferred from the packet. Post-task Craft
synchronization remains separately approved.

FPR01-003 remains unauthorized until FPR01-002 closes, its receipt is
independently verified, continuation is synchronized, and the successor is
separately selected.

## Implementation Gaps

1. Deterministic state reconciler and machine `EXEC_READY` report.
2. Governed pre-existing-packet adoption/closure route for FPR01-002.
3. WorkItem, side-effect, and collision schemas.
4. PREP manifest, freshness state, TTL, distance, and rework rules.
5. Explicit blocking or residual edges for Definitions Governance
   reconciliation and import-manifest repair.
6. Runner, cache, dependency, Git, and worktree isolation.
7. A bounded asynchronous code-dispatch owner only after scopes and authority
   semantics are enforceable.
8. Duration, invalidation, collision, and rework telemetry before optimization
   or speedup claims.

## Residue And Claim Boundary

- FPR01-002 adoption semantics are not deployed.
- Definition reconciliation may be a missing FPR01-003 predecessor.
- Import-manifest repair has no explicit blocking/non-blocking edge.
- The current Git observation is point-in-time evidence.
- No duration or resource weights establish temporal benefit.
- Current parent scheduling is procedural rather than mechanically locked.

Auditor acceptance applies only to the bounded research report. It does not
establish FPR completion, runtime correctness, production readiness, execution
authorization, continuation synchronization, canonical promotion, or a general
DomainSpec concurrency theorem.

## Next Human Action

Define the exact FPR01-002 adoption/closure authorization boundary. If approved,
use the verified FPR01-001 receipt to refresh continuation, select FPR01-002,
and run one bounded Task Session that preserves the existing decisions while
validating, tracking, and receipting the packet. Keep post-task Craft sync and
FPR01-003 selection separate.

## Connections

- derives-from -> `projects/domainspec-v2/development/first-production-release/research/2026-07-16-async-execution-strategy/research.md`
- summarizes -> `projects/domainspec-v2/development/first-production-release/research/2026-07-16-async-execution-strategy/findings.md`
- evidenced-by -> `telemetry/agents/subagents-dispatch.yaml`
- continuation-authority -> `projects/domainspec-v2/.craft/ledger.yml`
