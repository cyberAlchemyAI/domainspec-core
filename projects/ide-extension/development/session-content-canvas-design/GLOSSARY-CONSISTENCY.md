---
id: ide-extension-session-content-canvas-glossary
project: ide-extension
title: "Session Content Workbench Glossary Consistency"
status: accepted
node_type: glossary-consistency
updatedAt: 2026-07-12
---

# Session Content Workbench Glossary Consistency

## Scope

These are local experiment terms. They do not promote or redefine Arcanum-wide
vocabulary.

## Existing Terms Reused

| Term | Reuse |
| --- | --- |
| Workbench | The local browser application that hosts the agent-created surface. |
| Session | The active Codex process that creates/publishes a surface and polls interactions. |
| Poll | An explicit session request for pending work or user interaction. |
| Project root | The configured local filesystem boundary used to resolve a published file path. |

## Local Candidate Terms

| Term | Working definition | Owner |
| --- | --- | --- |
| HTML surface | A real interactive `.html` file created or selected by the session under the project root. | session/workspace |
| Canvas | The main workbench region that loads the current HTML surface. | browser workbench |
| Canvas publish | Registration of one complete HTML file revision as the current workbench surface. | session -> kernel |
| Surface id | Stable identity for a logical work surface across revisions. | local kernel |
| Revision id | Identity of one complete published file state, derived with its hash. | local kernel |
| Interaction event | A small named JSON payload emitted by the HTML surface and stored for session polling. | surface -> workbench -> kernel |
| Automatic update | Notification that a complete new revision exists, followed by browser fetch/reload. | kernel/workbench |
| Streaming | User-visible progressive workbench updates through complete published revisions, not partial HTML token delivery. | product behavior |

## Required Distinctions

### File Versus Bridge Message

The HTML file is the authored artifact. A publish message references it; it does
not contain the entire file body.

### Interaction Request Versus Effect Completion

A `craft.action.requested` event records what the user asked for. It does not
prove that the Craft action ran or completed.

### Trusted Local V0 Versus Safe Arbitrary HTML

V0 intentionally runs trusted local HTML to test usefulness. Passing V0 does
not establish a security claim for hostile HTML, remote agents, or production
deployment.

### Complete Revision Versus Partial Stream

The workbench changes only after the session publishes a complete saved
revision. This preserves a usable page while still producing a live experience.

## Consistency Result

- Result: `pass`.
- Canonical conflicts: none.
- Local candidate terms: eight.
- Remaining blockers: none; DG-SCC-003 confirms separate publish and poll
  operations.
