# TASK-UPW-COORDINATOR — Stable Refresh And Context

## Objective

Replace whole-document reload with an inert, action-fresh, rollback-capable
coordinator while preserving valid browser-local context.

- Layer/wave: L0 / W1
- Source: `ARCHITECTURE.md` Refresh Coordinator, Context Reconciler, DDR-02–03
- Dependencies: TASK-UPW-PROJECTION complete

## SWU Table

| SWU | Primary behavior | Dependencies | Write scope | Independent acceptance |
| --- | --- | --- | --- | --- |
| SWU-UPW-004 | Stable document and unchanged-poll inertness | 003 | `backend/src/cli/studio.ts`; future `backend/src/modules/ui-prototyping-studio/interface/workbench-shell.ts`; focused unit/E2E tests | two poll intervals cause zero main navigation and zero region patch |
| SWU-UPW-005 | Action-aware queued trailing refresh | 004 | same shell/coordinator module and focused race tests | old poll + completed action produces one trailing fetch and one V1 application |
| SWU-UPW-006 | Rollback-capable keyed commit | 005 | same shell/coordinator module and renderer-failure tests | renderer N failure restores all mounts/context/applied versions |
| SWU-UPW-007 | Identity-bound local context reconciliation | 006 | shell context module, `studio.ts`, mobile/continuity E2E | valid target/drafts/focus/scroll survive; stale binding alone resets with reason |

## Implementation Rules

### SWU-UPW-004

Mount the document once; keep whole and region applied-version maps in
ephemeral browser state. On schema-compatible same version, return before
reconciliation, DOM writes, focus movement, scrolling, or announcements.

Validation:
`./node_modules/.bin/playwright test e2e/workbench-continuity.spec.ts --grep "unchanged" --reporter=list`

Split analysis: shell mounting and inert poll are one proof; a mounted shell
without the no-op gate does not close the verified defect.

### SWU-UPW-005

Store `{flight, trailingRequired}`. Poll callers join without setting trailing.
An action receipt joining a pre-receipt flight sets one trailing slot. Release
the flight, consume the slot exactly once, and await it before final action
status. Coalesce duplicate action callers; never reload.

Validation:
`./node_modules/.bin/playwright test e2e/workbench-continuity.spec.ts --grep "trailing refresh" --reporter=list`

Split analysis: queue flag and action-await semantics jointly define freshness;
either alone can stay stale.

### SWU-UPW-006

Prepare every changed region in detached nodes and compute a context plan.
Journal prior mounts, context, and applied versions. Commit in deterministic
order. On any exception, restore the journal and show bounded recovery; only a
full commit advances applied versions.

Validation:
`./node_modules/.bin/playwright test e2e/workbench-continuity.spec.ts --grep "renderer failure" --reporter=list`

Split analysis: prepare, journal, commit, and rollback are one failure-atomic
behavior; smaller parts cannot satisfy DDR-02.

### SWU-UPW-007

Bind annotation context to `{head, odId}`, acknowledgments to live candidate or
revision identity, iframe scroll to source identity, and expansion state to
region identity. Apply the reconciliation plan only inside successful commit;
announce exact invalidation reason in the matching scope.

Validation:
`./node_modules/.bin/playwright test e2e/workbench-continuity.spec.ts --grep "context" --reporter=list`

Split analysis: preservation and bounded invalidation are the two outcomes of
one identity-reconciliation decision and must be reviewed together.

## Execution Owner And Handoff

All SWUs: `subagent`, serial. Read `WITNESS-CONTRACTS.md` UPW-FIX-002–006,
015, 017–018 and the current `pollScript`/`actScript`. Return the exact SWU
receipt; synchronize only declared planning/evidence targets.
