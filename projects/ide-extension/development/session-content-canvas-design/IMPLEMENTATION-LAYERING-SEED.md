---
id: ide-extension-session-content-canvas-layering-seed
project: ide-extension
title: "Session Content Workbench Implementation Layering Seed"
status: accepted-seed
node_type: implementation-layering-seed
updatedAt: 2026-07-12
---

# Implementation Layering Seed: Session Content Workbench

This seed orders work by product evidence. Invoke plan must turn each active
layer into a bounded SWU from the refreshed design.

## Layer Decision Table

| Layer | Value question | Included boundary | Promotion evidence |
| --- | --- | --- | --- |
| V0-A publish and display | Can a session make an existing project HTML file usable in the workbench? | `canvas publish`, current-surface registry, content route, iframe, manual Refresh. | Existing Craft presentation opens and its navigation works. |
| V0-B generate and update | Can Codex create a new presentation and have it appear automatically? | Generated file, complete revision hash, state-change notice, workbench reload. | New deck appears; one edited revision replaces it without partial display. |
| V0-C interact and return | Can a user action in agent-created HTML return to the active session? | `postMessage` adapter, generic event endpoint/store, cursor-based session poll. | Decision choice and Craft action request both return through the same event path. |
| V1 harden | Can the useful loop safely accept broader content and agents? | Origin/CSP, authentication, permissions, snapshots, denial and recovery behavior. | Threat-specific denial, replay, restart, and rollout evidence. |

## Active Layer Window

- Active sequence: V0-A, then V0-B, then V0-C.
- Stop after any layer that fails to produce the expected user value.
- V1 is explicitly deferred and must not displace V0 evidence.

## Smallest Coherent Value Loop

```text
session writes/selects complete HTML
  -> canvas publish <relative-path>
  -> kernel records current revision
  -> workbench loads the HTML
  -> user submits a surface action
  -> kernel stores the interaction
  -> session polls the event
```

Publishing without a return event proves only a viewer. Interaction without a
generic event envelope creates one-off skill integrations. Partial-file loading
makes the demo unreliable without adding value.

## V0 Non-Goals

- hostile HTML safety or production isolation;
- remote/multi-user sessions;
- token-by-token HTML streaming;
- browser-side proof that a requested effect completed;
- specialized bridge endpoints for presentations, Decision Gate, or Craft;
- collaborative editing or historical content snapshots.

## Promotion Blockers

| Promotion | Blocker until |
| --- | --- |
| Design -> plan | Refreshed Invoke dispatch validates the confirmed publish/poll design. |
| V0-A -> V0-B | Existing presentation works through the generic file-reference path. |
| V0-B -> V0-C | Complete-revision automatic update works without a blank/partial page. |
| V0-C -> V1 | Decision and Craft events demonstrate enough value to justify hardening. |

## Distill Verdict

- Coherent product unit: publish surface, use surface, return interaction.
- First cheap witness: existing project presentation through manual Refresh.
- Generality witness: decision and Craft surfaces share one event envelope.
- Verdict: `pass` for value layering; decision gate and Invoke refresh passed.
