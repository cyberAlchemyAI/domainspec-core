# TASK-UPW-COORDINATOR — Stable Refresh And Recoverable Commit

Status: `not-started`

## Objective

Replace whole-document reload with an inert, action-fresh coordinator, define
context reconciliation as a pure typed plan, then commit regions and context
atomically.

- Layer/wave: L0 / W1
- Source: `ARCHITECTURE.md#refresh-coordinator`,
  `ARCHITECTURE.md#context-reconciler`, DDR-02–03
- Scope authority: `SWU-SCOPE-INVENTORY.json` rows 004–007
- Acceptance authority: `SWU-ACCEPTANCE-MATRIX.json` assertions 004–007
- Closeout authority: `CLOSEOUT-SYNC-INVENTORY.json` rows 004–007

All omitted implementation paths are unauthorized and all declared paths use
the preflight digest/`ABSENT` contract.

## SWU-UPW-004 — Stable Inert Shell

- Primary behavior: a mounted document has zero side effects for an unchanged
  compatible projection version.
- Semantic dependency: SWU-UPW-003.
- Exact scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-004`.
- Algorithm: mount once; hold applied whole/region versions in ephemeral state;
  fetch through one coordinator entry; validate schema; return before render,
  focus, scroll, or announcement when whole version is already applied.
- Failure: network/schema errors preserve current DOM and expose bounded
  recovery without a false transition.
- Split analysis: shell mount and inert equality gate are one observable proof;
  a mounted shell that still mutates does not close the defect.
- Validation:
  `./node_modules/.bin/playwright test e2e/workbench-continuity.spec.ts --grep "UPW-004 unchanged poll is inert" --reporter=list`.
- Receipt: `validation.assertions.UPW_A_004_INERT`.

## SWU-UPW-005 — Action-Aware Trailing Refresh

- Primary behavior: an action that joins a pre-receipt poll gets exactly one
  trailing refresh before final status.
- Semantic dependency: SWU-UPW-004.
- Exact scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-005`.
- Algorithm:
  1. Store `{flight, flightStartedAt, trailingRequired}`.
  2. Poll callers join a flight without setting the trailing slot.
  3. After an action receipt, compare its completion boundary with the joined
     flight start; if the flight predates the receipt, set the one boolean slot.
  4. Release the current flight, atomically consume the slot, then fetch once.
  5. Await the trailing application before the action reports final state.
  6. Coalesce duplicate callers; never call `location.reload()`.
- Failure: rejected actions do not queue success; failed trailing fetch keeps
  recoverable status and permits a later poll.
- Split analysis: queue state and action-await semantics cannot close freshness
  independently.
- Validation:
  `./node_modules/.bin/playwright test e2e/workbench-continuity.spec.ts --grep "UPW-005 action queues one trailing refresh" --reporter=list`.
- Receipt: `validation.assertions.UPW_A_005_TRAILING`.

## SWU-UPW-006 — Pure Typed Context Transition Plan

- Primary behavior: identity comparisons produce a typed, side-effect-free
  preserve/invalidate plan.
- Semantic dependency: SWU-UPW-004.
- Serialization-only predecessor: SWU-UPW-005, because the work-pack admits one
  candidate at a time; 005 behavior is not an input to this planner.
- Exact scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-006`; `studio.ts` and the shell
  module are explicitly forbidden.
- Data model:
  `WorkbenchContextSnapshot`, `WorkbenchIdentitySet`, and
  `WorkbenchContextTransitionPlan` with one operation per selected target,
  drafts, focus, top scroll, frame scroll, and region expansion.
- Algorithm: compare `{head, odId}`, candidate, revision, frame-source, and
  region identities; emit `preserve` when equal and resolvable; otherwise emit
  exactly one typed invalidation reason for the affected binding; never inspect
  or mutate live DOM.
- Split analysis: preserve and invalidate are exhaustive outcomes of one
  identity decision; splitting duplicates precedence and weakens totality.
- Validation:
  `./node_modules/.bin/tsx --test src/modules/ui-prototyping-studio/interface/workbench-context-plan.test.ts`.
- Receipt: `validation.assertions.UPW_A_006_CONTEXT_PLAN`.

## SWU-UPW-007 — Atomic Region And Context Commit

- Primary behavior: prepared region nodes and the already-typed context plan
  commit or roll back together.
- Semantic dependencies: SWU-UPW-005 and SWU-UPW-006.
- Exact scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-007`; the accepted context-plan
  source and test are read-only/forbidden.
- Algorithm:
  1. Prepare every changed region in detached nodes.
  2. Call SWU-UPW-006 to obtain the context plan without side effects.
  3. Journal prior mounts, local context, focus/scroll, and applied versions.
  4. Commit mounts in fixed region order, then apply the context operations.
  5. On any exception, restore the complete journal and show bounded recovery.
  6. Advance whole/region versions only after the full commit succeeds.
- Failure: renderer N, stale target during commit, missing focus destination,
  or context operation error all restore the same prior governed surface.
- Split analysis: prepare, journal, commit, and rollback are a single
  failure-atomic boundary; any partial child can leave mixed DOM/context.
- Validation:
  `./node_modules/.bin/playwright test e2e/workbench-continuity.spec.ts --grep "UPW-007 renderer failure rolls back regions and context" --reporter=list`.
- Receipt: `validation.assertions.UPW_A_007_ATOMIC_COMMIT`.

## Owner And Synchronization

All four SWUs recommend `subagent` execution and return the standard SWU
receipt. Task Session must select only one exact SWU and Invoke Refresh may
write only the row-specific planning targets/fields in
`CLOSEOUT-SYNC-INVENTORY.json`.
