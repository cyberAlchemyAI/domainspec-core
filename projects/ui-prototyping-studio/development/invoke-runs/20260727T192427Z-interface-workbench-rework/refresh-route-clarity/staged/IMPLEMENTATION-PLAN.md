# Implementation Plan: Stable Governed Interface Workbench

Status: `draft-blocked-on-plan-repair`

## Implementation Objective

Replace the Studio preview’s whole-document poll/action reload behavior with a
coherent server-versioned projection and stable six-region workbench while
preserving every existing governance boundary.

## Ordered Plan

1. Establish deterministic whole/region projection identity.
2. Make projection assembly coherent under external CLI writes.
3. Serve additive versioned `/state` data and same-snapshot compatibility
   fields.
4. Mount a stable shell whose unchanged poll is inert.
5. Make action completion queue one trailing refresh across an older poll.
6. Make keyed update commit rollback-capable.
7. Preserve or explicitly invalidate identity-bound local context.
8. Add the six semantic regions one at a time.
9. Recompose responsive order and state copy.
10. Harden bounded interaction semantics and frame/route security.
11. Run closure-only full regression and traceability audit.

## Data And Control Flow

```text
store/application read epoch
  -> coherent ProjectionSnapshot
  -> six data regions
  -> canonical server/test digests
  -> additive /state response
  -> single-flight browser coordinator
      -> same version: no side effect
      -> new version: prepare + context plan + commit
          -> success: advance applied versions
          -> failure: rollback mounts/context/versions
      -> action joined older flight: one trailing refresh
```

## Failure Rules

- Torn server reads retry or fail recoverably without a new version.
- Invalid schema, route, canonical data, or digest never patches the shell.
- Partial renderer failure restores the prior governed surface.
- Action rejection preserves recoverable context and reports through the exact
  state scope.
- Stale identity remains an application/server decision.
- No failure path implies Accept, Revert, Export, evidence, or release success.

## Execution Boundary

`WORK-PACK.md` owns current status and exact handoff. Task files own algorithm
detail; wave files own order; `SWU-MANIFEST.json` owns machine identity and
dependencies. Implementation remains serial and one selected SWU at a time.

No SWU is selected by this Plan.

## Current Route

The next owner is `invoke plan` remediation, using
`plan-distill-review/findings.md` as the verified change-request source.
Repairing the Plan is authoring work: it does not execute implementation.
After regeneration, a fresh governed Plan Distill must pass before the human
may select one SWU and before Task Session can be considered.
