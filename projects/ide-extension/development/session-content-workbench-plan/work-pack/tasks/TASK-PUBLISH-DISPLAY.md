# Task Contract: Publish And Display

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-PUBLISH-DISPLAY` |
| Objective | Publish a complete existing project HTML file and operate it in the workbench after Refresh. |
| Layer / slice / wave | V0-A / S-002 / W1 |
| Dependencies | W0 pass |

## SWU-SCW-003: Publish, Current, Content, And CLI

**Goal:** Close the session-to-kernel file-reference path.

**Dependencies:** `SWU-SCW-002` pass.

**Exact write scope:** new focused canvas kernel helper(s), `src/server.mjs`,
`scripts/session-bridge.mjs`, package script help if required, and focused API/
CLI tests. Do not edit browser UI.

**Algorithm:**

1. Configure `workspaceRoot` independently from public/state roots; default to
   the repository root already used as the evidence root.
2. Resolve normalized relative path beneath that root; require regular `.html`.
3. Read complete bytes, compute SHA-256/length, then enter mutation queue.
4. Reconcile state, return existing revision for same path/hash, otherwise
   append `canvas.surface_published` and project it.
5. `GET /api/canvas/current` returns current metadata or `current: null`.
6. Revision content route rereads bytes, checks current hash, and returns HTML;
   changed bytes return `409 revision_changed` until republish.
7. Extend session CLI with `publish --path --title --kind`; print one JSON result
   and preserve existing command exit behavior.

**Edge cases:** missing file, directory, wrong extension, path escape, file
deleted after publish, same-hash duplicate, concurrent publish, append failure,
CLI connection failure.

**Done criteria:** one publish creates one projected revision; duplicate is
idempotent; all invalid inputs leave current state unchanged; restart preserves
metadata; CLI and API agree.

**Validation:** focused API/CLI tests, schema tests, restart test, existing full
bridge suite.

**Handoff:** `SWU-SCW-004` with a current-surface fixture and content URL.

## SWU-SCW-004: Workbench Canvas And Manual Witness

**Goal:** Make the actual interactive HTML the primary work area and prove
manual Refresh using the existing Craft presentation shape.

**Dependencies:** `SWU-SCW-003` pass.

**Exact write scope:** `public/demo/l0.html`, workbench UI tests, e2e harness,
one focused canvas Playwright spec, and screenshot evidence for this SWU.

**Implementation rules:**

1. Add an unframed full-width Canvas band with compact title/kind/revision,
   Refresh, and open-content controls.
2. Keep proposal/approval/connection/history tools compact and usable; do not
   overlay the iframe.
3. Refresh fetches current metadata and loads only a changed complete revision.
4. Iframe receives the revision content URL and allows the normal interactive
   HTML required by trusted-local V0.
5. Preserve the current iframe when refresh fails or reports hash drift; show a
   concise unavailable state.
6. Existing Approval Desk flows and selectors remain compatible.
7. Validate desktop and 390px layouts for overlap, clipping, and usable deck
   navigation.

**Edge cases:** no current surface, 404 content, changed revision, long title,
iframe load failure, repeated Refresh, mobile controls, existing proposal detail.

**Done criteria:** the workbench displays and operates an existing interactive
presentation after Refresh; existing bridge browser tests still pass.

**Validation:** workbench structure tests and Playwright desktop/mobile journey
using a realistic interactive HTML fixture; manually confirm compatibility with
`CRAFT-CAUSAL-CLASS-PRESENTATION.html` without modifying that source.

**Handoff:** W1 exit evidence; `SWU-SCW-005` becomes ready.
