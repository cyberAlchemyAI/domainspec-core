---
module: ide-extension-session-content-workbench
version: current
status: planned
updatedAt: 2026-07-12
docType: implementation-layering
---

# Implementation Layering: Session Content Workbench

## Purpose

Test whether agent-created HTML surfaces are more useful than chat-only output,
using the smallest local loop that can display a presentation and return a user
choice to the active Codex session.

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included scope | Deferred scope | Exit evidence |
| --- | --- | --- | --- | --- | --- |
| V0-A contracts | Can existing history and runtime express one current HTML surface plus interaction events? | Typed publish/interaction schemas and replayable canvas events. | Spec/architecture deltas, schemas, fixtures, projection state, restart replay. | Server routes, UI, auto-update. | Schema and mixed-history replay tests pass. |
| V0-A display | Can Codex publish an existing project HTML file and can the user operate it after Refresh? | Publish/current/content APIs, CLI publish, full canvas iframe. | Workspace-relative path, revision hash, manual Refresh, presentation navigation. | Automatic notices and return events. | Existing presentation loads and works through the generic route. |
| V0-B live update | Can a complete new revision appear without manual refresh? | EventSource notice followed by current-metadata fetch and iframe reload. | Reconnect, duplicate notice, restart, degraded Refresh. | Partial HTML/token streaming. | Generated deck and one republished revision appear automatically. |
| V0-C interaction | Can one generic HTML event return to the active session? | `postMessage` adapter, event API/store, cursor poll CLI. | Decision and Craft action envelopes, sent/failed UI, at-least-once polling. | Effect completion, specialized skill endpoints. | Decision and Craft events return through one generic path. |
| V0-C live value | Does the loop work with a real Codex session and real project artifacts? | Generated presentation plus Decision/Craft manual witnesses. | Browser screenshots, event/poll evidence, repeatable closure report. | Security hardening, remote/multi-user operation. | Human confirms usefulness and evidence resolves. |
| V1 hardening | Can broader agents/content use the loop safely? | Separate approved hardening design. | Origin/CSP/auth/capabilities/snapshots as justified by V0 evidence. | Generic remote platform. | Threat-specific denial and recovery evidence. |

## Active Window

- Execute V0-A through V0-C sequentially.
- Each layer must produce its value witness before the next layer begins.
- V1 is not part of this work-pack.

## Promotion Rules

- Do not build automatic update until manual publish/display works with the
  actual presentation shape.
- Do not build Decision/Craft-specific endpoints; both use the generic event
  envelope.
- Do not call a Craft action completed merely because its request event was
  polled.
- Do not add security hardening to V0 unless it is needed for the trusted-local
  experiment to function.

## First Unit

`SWU-SCW-001` defines the contract oracle. It is the smallest safe mutation
because projector, API, CLI, and browser work all depend on the same surface,
revision, and interaction vocabulary.
