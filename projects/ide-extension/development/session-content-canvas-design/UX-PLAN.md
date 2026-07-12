---
id: ide-extension-session-content-canvas-ux
project: ide-extension
title: "Session Content Workbench UX Plan"
status: accepted
node_type: ux-plan
updatedAt: 2026-07-12
---

# UX Plan: Session Content Workbench

## User Promise

The user asks Codex to make something useful. Instead of only describing the
result in chat, Codex places the actual interactive result in the local
workbench. The user can use it there, and meaningful actions return to the
active session.

## Primary Journeys

| Journey | User experience | Proof |
| --- | --- | --- |
| Open existing HTML | Codex sends a project presentation to the workbench. | The real file loads and its controls work. |
| Create presentation | Codex creates HTML and the workbench updates to it. | The generated file appears without copy/paste. |
| Answer decision | Codex shows a decision gate; the user selects an answer. | The session polls the exact answer. |
| Request Craft action | Codex shows the current task and available action. | The session polls the requested action. |

## Workbench Surface

- The canvas is the main work area, not a small preview card.
- A compact header shows the surface title, kind, revision, connection status,
  refresh, and open-in-browser controls.
- The published HTML owns the canvas body and may include its own navigation,
  forms, visualizations, or task controls.
- Proposal, approval, connection, and history tools remain available around the
  canvas without covering it.
- Manual Refresh proves the first path; automatic update becomes the normal V0
  experience immediately afterward.

## Interaction Contract

An HTML surface emits a generic event rather than calling a Craft- or
decision-specific endpoint:

```json
{
  "event_name": "decision.selected",
  "payload": {
    "decision_id": "DG-001",
    "value": "approve"
  }
}
```

The workbench adds the current `surface_id` and `revision_id`, sends the event
to the local kernel, and shows a small sent/failed state. The session retrieves
the event through the same manual polling posture as the existing bridge.

Representative event names:

- `decision.selected`
- `presentation.navigate`
- `craft.action.requested`
- `surface.submit`

These names demonstrate the generic envelope; they do not create domain
authority inside the browser.

## States

| State | Meaning | User action |
| --- | --- | --- |
| No surface | Nothing has been published in this session. | Ask Codex to create or open one. |
| Publishing | A complete revision is being registered. | Keep the current surface visible. |
| Available | The revision can be loaded. | Use the surface. |
| Updating | A newer complete revision is available. | Automatic reload or manual Refresh. |
| Interaction sent | The bridge stored the user event. | Continue in the workbench or session. |
| Interaction failed | The event was not stored. | Retry without losing the selection. |
| File unavailable | The published path no longer resolves. | Ask Codex to republish or restore it. |

## V0 Acceptance Signals

- Existing and generated HTML fill the available canvas without overlap.
- Presentation controls and decision/task controls are usable on desktop and a
  narrow viewport.
- Updating a revision does not leave a blank or half-rendered canvas.
- Each user submission has visible pending, sent, or failed feedback.
- The session receives exactly the event the user submitted.
- A browser reload restores the current surface.

## Explicit V0 Non-Goals

- hostile HTML containment or production security certification;
- polished editor tooling for HTML source;
- multi-user collaboration;
- direct proof that a requested action completed;
- one specialized UI protocol per skill.

## Gate Result

- UX direction: aligned to trusted-local value discovery.
- Status: `pass`; the bidirectional publish/poll contract is confirmed in
  DG-SCC-003.
