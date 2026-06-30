# TASK-PACKAGE-BOUNDARY

## Objective

Create the standalone package staging root with manifest, boundary policy, and fixture layout.

## Layer And Slice

- Layer: L0.
- Slice: S-001.
- Wave: W0.

## Source Contracts

- `development/resonantos-integration/RESONANTOS-INTEGRATION-GUIDE.md`
- `development/resonantos-integration/HANDOFF-CARD.md`
- `work-pack/shared/context.md`

## Dependencies

None.

## Blocker State

None.

## Completion State

Completed in `task-session-20260629T164831Z-standalone-package`.

## Smallest Working Units

### SWU-RCI-001

- Goal: create `development/resonantos-integration/standalone-package/` as a scrubbed staging
  package root.
- Dependencies: none.
- Source anchors: integration guide overview, boundary note, handoff card shared-kit section.
- Related context: `work-pack/shared/cross-task-decisions.md` decisions DEC-RCI-001 and DEC-RCI-002.
- Write scope:
  - `development/resonantos-integration/standalone-package/README.md`
  - `development/resonantos-integration/standalone-package/MANIFEST.md`
  - `development/resonantos-integration/standalone-package/boundaries.md`
  - `development/resonantos-integration/standalone-package/fixtures/`
  - `development/resonantos-integration/standalone-package/docs/`
  - `development/resonantos-integration/standalone-package/contracts/`
  - `development/resonantos-integration/standalone-package/tools/`
- Done criteria:
  - Package root exists.
  - README states the package is a governance blueprint with validators, not a runtime service.
  - MANIFEST lists intended package files and empty/future sections.
  - `boundaries.md` denies private parent history, private codenames, engine internals, and turnkey
    runtime claims.
  - Fixture directories exist with `.gitkeep` or placeholder README files.
- Acceptance evidence:
  - File list for package root.
  - Scoped scan against private-only terms and false implementation claims.
- Validation surface:
  - `find development/resonantos-integration/standalone-package -maxdepth 3 -type f | sort`
  - Review `boundaries.md` against `work-pack/shared/context.md`.
- Execution owner: local-fallback.
- Expected result shape:

```yaml
swu_id: SWU-RCI-001
result: pass | flag | block | interrupted
files_touched:
  - development/resonantos-integration/standalone-package/...
validation:
  - file list and boundary scan
blockers:
  - none or blocker
residue:
  - unresolved package sections
reroute: task-session or deferred
handoff_note: update WORK-PACK.md status and W0 exit evidence
```

## Synchronization Rules

After completion, update `WORK-PACK.md`, W0, and `work-pack/shared/traceability.md` if package paths
change.

## Completion Receipt

- Package root: `development/resonantos-integration/standalone-package/`.
- Boundary files: `README.md`, `MANIFEST.md`, and `boundaries.md`.
- Fixture layout: evidence-card, review-queue, and no-promotion fixtures present.
