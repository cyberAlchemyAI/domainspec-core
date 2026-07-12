---
id: ide-extension-session-content-canvas-architecture
project: ide-extension
title: "Session Content Workbench Architecture Bundle"
status: accepted
node_type: architecture-bundle
updatedAt: 2026-07-12
---

# Architecture Bundle: Session Content Workbench

## Design Intent

Add one generic, bidirectional local workbench path to the proven manual
session bridge:

```text
Codex session -> workspace HTML file -> canvas publish -> local kernel
  -> workbench iframe -> user interaction -> local kernel -> session poll
```

The HTML file is the authored artifact. The bridge carries its governed
reference and small interaction events; it does not copy the document body into
chat, result JSON, or the event log.

## V0 Product Boundary

V0 is a trusted-local value experiment. It deliberately allows normal
interactive HTML so we can test whether agent-created work surfaces are useful.
It does not claim hostile-content safety or production readiness.

Representative surfaces:

- standalone presentation;
- interactive decision gate;
- Craft task/action surface.

## Actors And Ownership

| Actor | Owns |
| --- | --- |
| Human operator | Request, review, and interaction choices. |
| Active Codex session | Creating/selecting workspace HTML, publishing revisions, polling interaction events. |
| Local kernel | Current-surface registry, revision metadata, event storage, notification. |
| Browser workbench | Loading the current HTML surface and forwarding its interaction events. |
| HTML surface | Presentation/task UI and calls to the small workbench interaction bridge. |

## High-Level Components

```text
Session CLI
  canvas publish <workspace-relative-path> [--title] [--kind]
  canvas events [--after <cursor>]

Local kernel
  WorkspacePathResolver
  CanvasRegistry
  CanvasRevisionStore
  CanvasEventStore
  CanvasNotificationStream
  StaticWorkspaceFileRoute

Browser workbench
  CanvasHost
  Surface iframe
  InteractionBridge
  Refresh/connection state
```

## Core Contracts

### Publish Request

```json
{
  "workspace_id": "domainspec-core",
  "path": "arcanum/development/example/PRESENTATION.html",
  "title": "Presentation title",
  "kind": "presentation"
}
```

The session sends a workspace-relative path. The kernel verifies that it
resolves beneath the configured project root, reads file metadata, computes a
revision hash, and records the new current surface.

### Published Surface

```json
{
  "surface_id": "surface-...",
  "revision_id": "revision-...",
  "workspace_id": "domainspec-core",
  "path": "arcanum/development/example/PRESENTATION.html",
  "title": "Presentation title",
  "kind": "presentation",
  "content_sha256": "...",
  "published_at": "...",
  "url": "/api/canvas/surfaces/surface-.../revisions/revision-.../content"
}
```

The content URL serves the real project file. The hash identifies a complete
published revision and gives automatic refresh a stable comparison point.

### Interaction Event

```json
{
  "surface_id": "surface-...",
  "revision_id": "revision-...",
  "event_name": "decision.selected",
  "payload": {
    "decision_id": "DG-001",
    "value": "approve"
  }
}
```

The kernel assigns `event_id`, sequence/cursor, and receipt time. The session
polls events after its last cursor. V0 uses at-least-once retrieval with stable
event ids so the session can ignore duplicates.

## Browser Interaction Adapter

The host exposes one small adapter to loaded surfaces:

```js
window.parent.postMessage({
  type: "ide-extension.canvas-event",
  eventName: "decision.selected",
  payload: { decision_id: "DG-001", value: "approve" }
}, "*");
```

The workbench adds authoritative surface/revision metadata and posts the event
to the kernel. Domain-specific behavior remains in the HTML and session; the
bridge only transports named JSON events.

For V0, the iframe is primarily a layout and lifecycle boundary. It is not a
security guarantee.

## Workflow

### Publish And Display

1. Codex creates or selects a project `.html` file.
2. Codex calls `canvas publish` only after a complete save.
3. The kernel resolves the path, hashes the file, records a revision, and makes
   it current.
4. V0-A uses manual Refresh to load the surface.
5. V0-B emits a state-change notice; the workbench fetches current metadata and
   reloads the complete revision.

### Interact And Return

1. The user acts inside the surface.
2. The surface emits a named JSON event to its parent workbench.
3. The workbench binds the current surface/revision and sends the event.
4. The kernel stores it with a stable id and cursor.
5. The session calls `canvas events` and continues from the user's choice.

## Proposed Interfaces

| Interface | Purpose |
| --- | --- |
| `POST /api/canvas/publish` | Register a complete workspace HTML revision as current. |
| `GET /api/canvas/current` | Read current surface/revision metadata. |
| `GET /api/canvas/surfaces/:surfaceId/revisions/:revisionId/content` | Serve the published HTML revision. |
| `POST /api/canvas/events` | Store one interaction from the current surface. |
| `GET /api/canvas/events?after=<cursor>` | Let the active session poll interactions. |
| `GET /api/canvas/notifications` | C1 EventSource notice for current-surface changes. |

## Persistence

V0 needs only:

- current surface metadata;
- append-only revision metadata;
- append-only interaction events with cursor;
- the HTML file itself in the workspace.

The workspace file remains canonical. The kernel does not duplicate its body.
If exact historical replay becomes valuable, immutable snapshots can be added
after the value experiment.

## Validation Strategy

### V0-A

- publish the existing Craft presentation path;
- refresh the workbench;
- use presentation navigation;
- record browser and server evidence.

### V0-B

- ask Codex to create a new presentation;
- publish it;
- observe automatic workbench replacement/reload;
- modify and republish one complete revision.

### V0-C

- publish a decision gate;
- submit one choice and poll it from the session;
- publish a Craft task surface;
- submit one action request and poll it through the same endpoint.

## Honest Claims

Passing V0 supports this claim:

> A trusted local Codex session can publish interactive project HTML to the
> local workbench, and user interactions can return to that session through a
> generic pollable event bridge.

It does not support claims about arbitrary HTML safety, remote agents,
authenticated identity, effect completion, collaboration, or production
readiness.

## Decision Gate Closure

DG-SCC-003 confirms that surface publication and interaction polling are
separate active-session operations rather than attachments to the terminal
result. The architecture decision gate and refreshed dispatch are `PASS`; the
design is ready for Invoke plan.
