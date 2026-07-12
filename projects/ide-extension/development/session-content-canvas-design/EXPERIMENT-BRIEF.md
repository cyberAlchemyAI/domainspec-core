---
id: ide-extension-session-content-canvas-experiment
project: ide-extension
title: "Session-to-Workbench Interactive HTML Experiment"
status: accepted
node_type: experiment-brief
updatedAt: 2026-07-12
---

# Experiment Brief: Session-to-Workbench Interactive HTML

## Research Question

Does it create real user value when an active Codex session can publish an HTML
work surface into the local workbench and receive the user's interactions back
through the bridge?

## Product Hypothesis

Chat is useful for discussion, but many outputs are better as direct
interfaces. If the agent can turn its work into a local interactive surface,
the user can review a presentation, answer a decision gate, or trigger the next
Craft task without translating everything through terminal prose.

## Starting Evidence

- The L0 manual session bridge can prepare, approve, claim, execute, and admit a
  result through the local workbench.
- The browser already projects proposal, result, receipt, and history state.
- The target presentation exists as a standalone interactive HTML file inside
  the project.
- The missing capability is a general session -> HTML surface -> user event ->
  session loop.

## V0 Witnesses

### V0-A: Existing Presentation

1. The session publishes the path of an existing project HTML presentation.
2. The workbench displays it after manual refresh.
3. Presentation navigation and local JavaScript work.

This proves the minimum transport and display path without generation noise.

### V0-B: Generated Presentation And Automatic Update

1. The user asks Codex to create a presentation.
2. Codex writes a standalone `.html` file in the project.
3. Codex publishes the complete revision.
4. The already-open workbench receives a notice and displays or reloads it.

This proves the desired end-product experience. Automatic update follows V0-A;
it is complete-revision delivery, not token-by-token HTML streaming.

### V0-C: Interaction Round Trip

1. Codex publishes a decision-gate surface with selectable actions.
2. The user chooses an action in the HTML surface.
3. The workbench records a typed interaction event through the local kernel.
4. The session polls and receives the exact choice.
5. Repeat the same mechanism with a Craft task surface and a requested action.

This proves that the canvas is a workbench, not only a viewer.

## Candidate Oracle

V0 passes when:

- the referenced existing presentation opens and remains interactive;
- Codex can generate a new project HTML file and publish it without copying its
  body into chat or the terminal result;
- the browser switches to the newest complete revision manually, then
  automatically in the follow-up witness;
- one decision-gate click becomes one pollable session event with matching
  surface, revision, event name, and payload;
- one Craft action request travels through the same generic event path;
- reload preserves the currently published surface and event history;
- the demo can be repeated from a clean local start.

## Evidence Boundary

This experiment can prove a trusted-local bidirectional value loop between a
Codex session and an HTML workbench. It does not prove arbitrary HTML safety,
hostile agent isolation, authenticated identity, remote delivery, external
publication, effect completion, or production readiness.

## Deferred Until Value Is Proven

- sanitization and content-security hardening;
- external resource allowlists;
- authenticated or remote sessions;
- fine-grained capability permissions;
- token-level or partial-DOM streaming;
- collaborative editing and multi-user event ordering;
- claiming that a requested Craft action actually completed.

## Stop Conditions

- The implementation becomes presentation-specific instead of using a generic
  surface publication contract.
- Browser events bypass the bridge and cannot be polled or replayed.
- A partially written HTML revision is displayed as complete.
- Security work displaces the first value witnesses without evidence that it is
  required to run the trusted-local experiment.
