---
id: ide-extension-workbench-bridge-demo-v01-layering
project: ide-extension
status: planned
updatedAt: 2026-07-17
invoke_mode: plan
---

# Implementation Layering

## L0 - Visible Manual Loop

Question: Can the workbench make the existing manual bridge understandable and
repeatable without changing authority?

Included:

- bridge recipe panel,
- ready handle display,
- copyable poll and claim command hints,
- admitted receipt display,
- blind-boundary UI tests.

Promotion evidence:

- `npm run test:workbench`
- focused bridge UI test proving no task/skill appears before claim
- manual demo with one admitted receipt

## L1 - Repetition Aids

Question: Can repeated local tests be smoother without adding workers?

Included:

- small "copy result template" affordance,
- clearer claim/result status refresh,
- retained last receipt summary.

Excluded:

- automatic result submission,
- skill execution automation.

## L2 - Reliability And Recovery

Question: Can the operator recover from interrupted or stale claims cleanly?

Included:

- UI display for interrupted/released states,
- operator recovery guidance,
- tests for release/requeue visibility.

## L3 - Worker/Lease Future

Question: Should the manual bridge evolve into automatic polling?

Deferred:

- queue,
- lease,
- worker registry,
- authenticated session identity,
- remote or multi-user operation.

This requires a new governed plan.
