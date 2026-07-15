# Task Contract: Rebuild, Navigation, And Workbench Delivery

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-REBUILD-NAVIGATION` |
| Objective | Explicitly rebuild from workspace and control one durable workbench display target. |
| Layer / slice / wave | L2 / OV1-S5 / W4 |
| Execution owner | Task Session, one SWU at a time |
| Execution status | completed; SWU-OV1-008 through SWU-OV1-010 passed |

## Source Handles

- [Navigation boundary](../../../operations-v1-design/ARCHITECTURE-BUNDLE.md#navigation-boundary)
- [OVG-004 selection](../../../operations-v1-design/PLANNING-DECISION-GATE.md#ovg-004-navigation-command-durability)
- `projects/ide-extension/src/kernel/canvas-notifications.mjs`
- `projects/ide-extension/public/demo/l0.html:1052`
- `projects/ide-extension/tests/e2e/session-content-workbench.spec.mjs`

## SWU-OV1-008: Exact Workspace Rebuild

**Goal:** create a new revision from an explicitly named exact-hash workspace
HTML source while preserving operations surface identity and lineage.

**Dependencies:** SWU-OV1-007 pass.

**Exact write scope:** rebuild branch in operations service/server/CLI, source
lineage projection, focused rebuild/path/limit tests, and Task Session evidence.

**Algorithm:** perform operation-id lookup and CAS first; admit workspace path
through existing canonical helper; require caller `expected_sha256` to match
read bytes; enforce 4 MiB source; parse and serialize as a complete document;
enforce 8 MiB result; commit blob then operation event with workspace path/hash
lineage. A later V0 publish never invokes this path implicitly.

**Edge cases:** same source as current serialized result, source drift, missing
path, external symlink, directory, multibyte limit, idempotent retry after source
changes, and stale expected surface revision.

**Done criteria:** exact rebuild advances one operations surface revision,
records source lineage, and never changes V0 publication state or identity.

**Validation:** `npm run test:operations-rebuild`, canvas path tests, and L0/L1
operations suites.

**Execution owner:** local fallback. **Expected result:** rebuild lineage and
drift matrix. **Handoff:** SWU-OV1-009.

## SWU-OV1-009: Durable Target And Transient Refresh Runtime

**Goal:** separate durable workbench selection from V0 current publication and
from transient reload delivery.

**Dependencies:** SWU-OV1-008 pass.

**Exact write scope:** projector navigation reducers, notification hub/runtime
status module, server display/navigation/status/ack routes, navigation schemas
if SWU-001 requires a correction, focused tests, and Task Session evidence.

**Interfaces:**

- `GET /api/canvas/display` returns the admitted displayed V0 or operations
  revision;
- `POST /api/canvas/navigation` accepts redirect or refresh;
- `GET /api/canvas/navigation/:commandId` returns transient status when known;
- `POST /api/canvas/navigation/:commandId/ack` records transient browser load
  result.

**Redirect algorithm:** validate target and immutable body availability; bind
command id to normalized digest; same id/same digest is idempotent, different
digest conflicts; append `canvas.display_target_selected`; project and notify.
Replay recovers the target. V0 publish continues its existing V0 current
behavior and becomes the displayed V0 target; Operations V1 commits never
redirect.

**Refresh algorithm:** validate current display target; retain accepted status
in memory for at most 15 minutes or 128 commands; same id semantics apply while
retained; broadcast refresh notice; browser acknowledgement updates only this
transient store. Restart expires refresh/ack history and recovers the durable
display target without replay.

**Edge cases:** offline browser, same-target redirect, unknown/pruned target,
failed iframe load acknowledgement, duplicate command, server restart, later
non-selected operation commit, and later V0 publication.

**Done criteria:** `/api/canvas/current` remains V0-compatible; redirect survives
restart; refresh does not enter event history; non-selected commits do not
change display.

**Validation:** `npm run test:operations-navigation`, V0 live/replay/publish
suites, and event-log assertions.

**Execution owner:** local fallback. **Expected result:** durable/transient
matrix. **Handoff:** SWU-OV1-010.

## SWU-OV1-010: Browser Display Projection And Acknowledgement

**Goal:** make the local workbench display and interact with the durable target
without replacing a good frame on load failure.

**Dependencies:** SWU-OV1-009 pass.

**Exact write scope:** `public/demo/l0.html`, browser notification handling,
interaction routing needed for operations surfaces, Node UI tests, Playwright
tests/screenshots, and Task Session evidence.

**Browser algorithm:** on startup/reconnect fetch `/api/canvas/display`; load a
new hidden iframe, validate content availability, wait for load, then atomically
swap and acknowledge any command. Revision notices reload only when surface id
matches the display target. Redirect notices refetch display. Refresh notices
reload the same target even when revision id is unchanged. On failure remove
only the pending frame, retain the old frame, and acknowledge failure.

Operations-surface interactions bind to the displayed operations revision and
use the V4 interaction record; existing displayed V0 interactions keep their V3
path and request behavior.

**Viewport matrix:** desktop and mobile; V0 display; operations redirect;
append reload; non-selected commit; manual refresh; reconnect; server restart;
failed target load; trusted script interaction; and open-in-new-tab URL.

**Done criteria:** browser state never displays partial bytes or blank-replaces
a good revision; command status matches actual load outcome; existing approval
desk and canvas journeys remain green.

**Validation:** `npm run test:workbench`, `npm run test:e2e:operations-navigation`,
and existing canvas/bridge Playwright suites.

**Execution owner:** local fallback. **Expected result:** Node/Playwright counts,
desktop/mobile screenshots, and degraded-mode evidence. **Handoff:** SWU-OV1-011.

## Synchronization

The durable target is one local workbench pointer. Do not introduce browser
identity, tabs, durable refresh replay, or navigation job queues in this task.
