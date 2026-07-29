# Execution Pack: Interface Workbench Rework

Status: `blocked-by-plan-distill`

## Choreography

```text
W0: 001 -> 002 -> 003
  semantic chain

W1: 004 -> 005 -> 006 -> 007
  006 semantically consumes 004; follows 005 for serialization
  007 semantically consumes 005 + 006

W2: 008 -> 009 -> 010 -> 011 -> 012 -> 013
  all consume 007; 012 also consumes 005
  arrows after 008 are serialization-only shared-file order

W3: 014 -> 015
  014 consumes all regions
  015 consumes state-bearing regions and follows 014 for serialization

W4: 016 -> 017 -> 018 -> 019
  candidate only: 016 interaction/status and 017 visual/targets require splits
  018 route admission; semantically consumes 003, follows 017 only for order
  candidate only: 019 sandbox/safe sinks requires a split and fuller context

W5: closure-only verification -> exact closure JSON
```

`SWU-MANIFEST.json` is authoritative for semantic `dependencies`,
`serialization_after`, and successor identity.

## Admission Per SWU

1. Invoke Plan must apply the verified change requests and a new fresh Plan
   Distill must pass.
2. Human selects exactly one `selected_swu`.
3. Context Builder resolves only that task, scope row, assertion row, closeout
   row, Design anchors, and dependency receipts.
4. Task Session hashes every exact existing target and binds future paths to
   `ABSENT`; any mismatch blocks before mutation.
5. The worker returns `task-session.swu-result.v1` with the exact acceptance
   field.
6. Invoke Refresh synchronizes only the row targets/fields and returns
   `invoke.refresh.v1`.
7. The successor becomes a candidate, never selected.

## Parallelism

No parallel product mutation is planned. The manifest nevertheless distinguishes
behavioral dependencies from safe serialization so future planners do not
mistake shared-file ordering for semantic coupling.

## Failure And Recovery

- Scope mismatch: no mutation; route to Invoke Plan refresh.
- Source validation failure: rollback/recover per SWU, emit blocking receipt,
  and do not synchronize a pass.
- Refresh conflict: preserve terminal execution receipt as residue; leave
  successor blocked.
- Closure failure: W5 records the exact failing receipt/assertion and opens a
  new plan route; it does not repair product source.

## Authority

This pack choreographs a blocked candidate only. It neither selects an SWU nor
executes code. Current gate remains blocked by
`plan-redistill-review/findings.md`.
