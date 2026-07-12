---
id: ide-extension-session-content-canvas-design-transport
project: ide-extension
title: "Session Content Workbench Design Transport"
status: refreshed
node_type: design-transport
updatedAt: 2026-07-12
observed_capability: invoke
invoke_mode: refresh
---

# Design Transport: Session Content Workbench

## Target Artifact Provenance

| Field | Value |
| --- | --- |
| Observed capability | `invoke` |
| Original mode | `design` |
| Current state | accepted design refreshed after operator-directed value pivot |
| Target artifact | Session Content Workbench architecture bundle |
| Lifecycle owner | `projects/ide-extension` |
| Runtime mutation | none |
| Required next route | `invoke plan` |

## Operator Correction

The original design optimized for bounded sanitized Markdown attached to a
terminal result. The operator clarified that V0 should optimize for useful
agent-created HTML interactions and explicitly deferred security hardening.

That correction changes the smallest coherent unit from:

```text
terminal result -> immutable Markdown artifact -> safe viewer
```

to:

```text
active session -> workspace HTML publish -> interactive workbench
  -> user event -> session poll
```

The current design artifacts have been refreshed around that unit. The original
[session-content-canvas.dispatch.json](session-content-canvas.dispatch.json)
was replaced by the validated HTML publish/poll dispatch during Invoke refresh.

## Current Decisions

| Decision | Status | Selection |
| --- | --- | --- |
| DG-SCC-001 update | resolved | manual Refresh witness, then automatic complete-revision update |
| DG-SCC-002 representation | resolved | trusted local project HTML artifact |
| DG-SCC-003 coupling | resolved | separate publish and interaction-poll operations |

## Forecast Deltas For Invoke Refresh

1. `SPEC.md`: define the trusted-local interactive workbench experiment.
2. Session CLI: add `canvas publish` and `canvas events` operations.
3. Kernel: add current-surface/revision registry and interaction event store.
4. Server: serve published project HTML and expose current/event endpoints.
5. Workbench: host the current surface and forward generic named JSON events.
6. Update transport: manual Refresh witness followed by EventSource notice.
7. Validation: existing presentation, generated presentation, decision round
   trip, and Craft action round trip.

## Gap Ledger

| Gap | Class | Owner | Effect |
| --- | --- | --- | --- |
| Exact runtime files/interfaces not forecast as SWUs. | plan artifact | `invoke plan` | blocks implementation |
| Security controls absent by design. | accepted V0 limitation | future V1 | blocks production claims, not local experiment |
| A Craft click does not prove task completion. | accepted evidence limitation | session/task runtime | requires separate execution result |

## Gate Status

- Architecture and UX direction: `pass`.
- Human decisions: DG-SCC-001 through DG-SCC-003 resolved; decision gate
  `PASS`.
- Dispatch validation for refreshed design: `pass` after deterministic check.
- Plan activation: `pass`; Invoke plan owns the next artifact set.
