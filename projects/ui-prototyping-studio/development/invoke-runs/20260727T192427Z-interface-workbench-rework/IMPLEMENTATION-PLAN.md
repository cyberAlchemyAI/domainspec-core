# Implementation Plan: Stable Governed Interface Workbench

Status: `plan-distill-block`

## Objective

Replace whole-document poll/action reload with a coherent server-versioned
projection and stable six-region workbench while preserving existing governance
boundaries.

## Ordered Plan

1. Establish deterministic whole/region projection identity.
2. Acquire one coherent snapshot through an authoritative store read token,
   exact token equality, one initial attempt plus two retries, and typed
   exhaustion.
3. Serve additive versioned `/state` data from currently admitted internal
   route constructors; defer arbitrary/new route admission to SWU-018.
4. Mount a stable shell whose unchanged poll is inert.
5. Queue exactly one action trailing refresh across an older poll.
6. Compute an identity-bound context transition plan without DOM mutation.
7. Prepare and commit changed regions plus that plan through one rollback
   journal.
8. Add the six semantic regions with direct, primary acceptance assertions.
9. Recompose responsive order and the literal state/action copy matrix.
10. Candidate hardening currently groups interaction/status, visual/target,
    server route admission, and iframe/safe-sink rendering. Fresh Distill keeps
    route admission but requires separate activation/focus, live-status,
    perceivability, target-geometry, iframe-sandbox, and safe-sink children.
11. Run closure-only full regression and receipt/traceability audit.

## Data And Control Flow

```text
file/in-memory store-owned read token
  -> before === after within 1 initial attempt + retryLimit=2
  -> coherent ProjectionSnapshot
  -> six region data objects using current internal routes
  -> canonical server/test digests
  -> additive /state response
  -> single-flight browser coordinator
      -> same version: no side effect
      -> new version:
          detached region preparation
          + pure WorkbenchContextTransitionPlan
          -> journaled commit
              -> success: advance applied versions
              -> failure: rollback mounts/context/versions
      -> action joined older flight: one trailing refresh
```

Later L2 route admission validates all route fields before versioning. The
browser renderer consumes only admitted routes and enforces exact sandbox/safe
sink rules.

## Failure Rules

- Three torn read attempts (initial plus two retries) end in
  `ProjectionSnapshotUnstableError`; no version is emitted.
- SWU-003 fails recoverably on unstable/schema data but makes no arbitrary
  route-admission promise.
- New/external/unknown route families fail closed only after SWU-018 exists.
- Invalid schema, canonical data, or digest never patches the shell.
- Region/context commit failure restores the prior governed surface.
- Action rejection preserves recoverable context and reports through the exact
  state-owned scope.
- No failure path implies Accept, Revert, Export, evidence, release, or human
  outcome success.

## Artifact Ownership

- `WORK-PACK.md`: canonical status, plan gate, task navigation.
- `SWU-MANIFEST.json`: 19 candidate IDs, semantic dependencies, serialization
  order; regeneration is blocked on the verified splits.
- `SWU-SCOPE-INVENTORY.json`: exact mutation authority.
- `SWU-ACCEPTANCE-MATRIX.json`: inverse Design/assertion ownership.
- `CLOSEOUT-SYNC-INVENTORY.json`: receipts and Plan synchronization.
- task files: algorithms, edge cases, handoff.
- wave files: layer questions, order, promotion.
- `EXECUTION-PACK.md`: cross-task choreography only.

## Current Route

Fresh governed Plan Distill returned BLOCK. Apply
`plan-redistill-review/findings.md` through a separately authorized Invoke Plan
remediation, regenerate affected artifacts, and run a new validation. No SWU is
selected; Task Session is not the current owner.
