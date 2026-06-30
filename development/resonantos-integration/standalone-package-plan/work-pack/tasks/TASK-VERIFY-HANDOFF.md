# TASK-VERIFY-HANDOFF

## Objective

Verify the package, record scrub evidence, and prepare a private-repo handoff checklist.

## Layer And Slice

- Layer: L3.
- Slice: S-004.
- Wave: W3.

## Source Contracts

- `development/resonantos-integration/HANDOFF-CARD.md`
- `work-pack/shared/traceability.md`
- `work-pack/shared/cross-task-gaps.md`

## Dependencies

- `SWU-RCI-006`.

## Completion State

Completed in `task-session-20260629T164831Z-standalone-package`.

## Smallest Working Unit Exemption

This is a closure task, but it still carries one explicit SWU because it writes verification and
handoff artifacts.

## Smallest Working Units

### SWU-RCI-007

- Goal: verify package completeness and prepare private-repo handoff artifacts.
- Dependencies: `SWU-RCI-006`.
- Source anchors: handoff card checklist and boundary log.
- Related context: external private repo is already separate fresh-history surface.
- Write scope:
  - `standalone-package/VERIFY.md`
  - `standalone-package/SCRUB-REPORT.md`
  - `standalone-package/HANDOFF.md`
- Done criteria:
  - Manifest completeness check recorded.
  - Scrub report is clean or records blockers.
  - Handoff distinguishes local staging from external private repository mutation.
  - External collaboration target remains deferred unless a later request selects one.
- Acceptance evidence:
  - Scrub report.
  - Manifest/file-list check.
  - Handoff checklist.
- Validation surface:
  - Scoped grep denylist.
  - File list vs manifest review.
- Execution owner: manual.
- Handoff note: update external repository only after explicit owner approval.

## Synchronization Rules

If scrub finds private-only material, stop before external handoff and route repairs to the relevant
task.

## Completion Receipt

- `VERIFY.md`, `SCRUB-REPORT.md`, `HANDOFF.md`, and `DECISIONS.md` exist in the package.
- Scrub scan passed for local/private names and private paths.
- No active blocker remains for local package creation.
