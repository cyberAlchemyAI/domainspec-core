---
id: ide-extension-operations-v1-ux
project: ide-extension
title: "Operations V1 UX Plan"
status: design-ready
node_type: ux-plan
updatedAt: 2026-07-12
---

# UX Plan: Operations V1

## User Promise

The user can keep using the current HTML workbench while the agent adds or
replaces content. Each successful change appears as one complete revision, and
a failed or stale operation leaves the visible page intact.

## Primary Journeys

| Journey | User experience | Proof |
| --- | --- | --- |
| Start editing a published page | Agent derives a builder surface from the chosen V0 revision. | Original V0 surface still opens unchanged. |
| Add a section | Agent appends HTML and the displayed page reloads once. | Added controls and content work after reload. |
| Replace the page | Agent submits a complete document replacement. | One new complete revision appears without partial display. |
| Rebuild from project HTML | Agent names a file and exact hash. | Derived surface updates with visible source lineage. |
| Recover from conflict | A stale operation is rejected. | Current page remains usable and agent receives the current revision. |
| Retry safely | Agent repeats an operation after losing the response. | No duplicate section appears. |

## Workbench Behavior

- The canvas remains the primary work area.
- The compact header distinguishes `V0 file` from `Operations V1` and shows the
  current revision.
- While an operation is pending, the current revision remains visible.
- A committed notice reloads only the already-selected operations surface.
- Failure does not blank, redirect, or partially rewrite the canvas.
- Redirect and Refresh remain explicit display controls.
- Revision lineage is inspectable through history, not placed over the canvas.

## States

| State | Meaning | Visible behavior |
| --- | --- | --- |
| Deriving | Exact V0 bytes are being copied into an operations surface. | Keep existing display. |
| Ready | Operations surface has a committed current revision. | Show surface kind and revision. |
| Applying | Kernel is validating and transforming an operation. | Keep current revision interactive. |
| Updated | New complete revision committed. | Reload once when this surface is displayed. |
| Stale | Expected revision is no longer current. | Keep current page; expose current revision to agent. |
| Rejected | Input, parser, or source validation failed. | Keep current page and display concise failure state. |
| Navigation failed | Content exists but redirect/reload failed. | Keep prior display and retain manual Refresh. |

## Region Extension

Future named regions should be visible to the agent through metadata or source,
not decorative workbench overlays by default. A region operation should produce
the same pending, committed, stale, and rejected states as a whole-document
operation.

## UX Non-Goals

- source-code editor or visual drag-and-drop builder;
- collaborative cursors or merges;
- token-by-token DOM streaming;
- security messaging for a trusted-local experiment;
- treating a workbench interaction as proof of an external effect.
