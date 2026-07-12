---
id: ide-extension-session-content-canvas-design
project: ide-extension
title: "Session Content Workbench Design Package"
status: refreshed
node_type: development-package
updatedAt: 2026-07-12
invoke_mode: design
phase_status: pass
---

# Session Content Workbench Design Package

This package designs a trusted-local value experiment: a Codex session creates
or selects an interactive HTML file, publishes it into the local workbench, and
receives user interaction events back through the bridge.

The target is a generic agent-created work surface, demonstrated by a
presentation, a decision gate, and a Craft task/action surface. Security
hardening is deferred until the bidirectional loop proves useful.

## Package Index

| Artifact | Purpose |
| --- | --- |
| [EXPERIMENT-BRIEF.md](EXPERIMENT-BRIEF.md) | Defines the three V0 value witnesses and honest proof boundary. |
| [DECISIONS.md](DECISIONS.md) | Records trusted local HTML and the remaining publish/poll decision. |
| [ARCHITECTURE-BUNDLE.md](ARCHITECTURE-BUNDLE.md) | Defines file publication, automatic refresh, and interaction return. |
| [UX-PLAN.md](UX-PLAN.md) | Defines the user-facing presentation, decision, and Craft journeys. |
| [GLOSSARY-CONSISTENCY.md](GLOSSARY-CONSISTENCY.md) | Defines the local workbench transport terms. |
| [IMPLEMENTATION-LAYERING-SEED.md](IMPLEMENTATION-LAYERING-SEED.md) | Orders display, automatic update, and interaction proof. |
| [DESIGN-TRANSPORT.md](DESIGN-TRANSPORT.md) | Records the operator correction and the required refresh route. |
| [INVOKE-RESULT.md](INVOKE-RESULT.md) | Reports the current decision-gate status. |
| [session-content-canvas.dispatch.json](session-content-canvas.dispatch.json) | Historical pre-pivot dispatch; retained as superseded evidence and not valid for planning. |

## Current Result

- V0 content: trusted local interactive `.html` files under the project root.
- Transport: publish a complete workspace-file revision by reference.
- Display: manual Refresh witness, followed immediately by automatic update.
- Return path: typed HTML interaction event stored by the kernel and retrieved
  by session polling.
- Decision status: DG-SCC-001 through DG-SCC-003 resolved; gate `PASS`.
- Refresh status: `pass`; the accepted design dispatch replaces the superseded
  Markdown route.
- Runtime mutation: none.

## Next Route

Use the refreshed design to produce an Invoke plan for V0-A through V0-C.
