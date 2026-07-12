---
id: ide-extension-manual-session-bridge-design
project: ide-extension
title: "Manual Codex Session Bridge Design Package"
status: approved
node_type: development-package
updatedAt: 2026-07-12
invoke_mode: design
phase_status: pass
---

# Manual Codex Session Bridge Design Package

This package turns the successful blind manual-poll experiment into a governed
design for connecting the local Approval Desk to the currently active Codex
session.

The first bridge is deliberately manual: the operator approves a proposal in
the browser and then says `poll` in the Codex session. Only that explicit poll
allows the session to claim the proposal and discover the requested skill. No
background worker, automatic CLI process, or remote session dispatcher is part
of this design slice.

## Package Index

| Artifact | Purpose |
| --- | --- |
| [DECISIONS.md](DECISIONS.md) | Records the passed decision gate, selected options, deferrals, and assumptions. |
| [EXPERIMENT-EVIDENCE.md](EXPERIMENT-EVIDENCE.md) | Records what the blind poll proved and did not prove. |
| [ARCHITECTURE-BUNDLE.md](ARCHITECTURE-BUNDLE.md) | Defines the six-view bridge architecture, decisions, interfaces, risks, and plan handoff. |
| [UX-PLAN.md](UX-PLAN.md) | Defines the operator workflow and corrects the proposal-task discoverability failure. |
| [GLOSSARY-CONSISTENCY.md](GLOSSARY-CONSISTENCY.md) | Keeps bridge terms local and identifies conflicts with current L0 receipt semantics. |
| [IMPLEMENTATION-LAYERING-SEED.md](IMPLEMENTATION-LAYERING-SEED.md) | Separates the first manual read-only proof from later resilience and enforcement. |
| [manual-session-bridge.dispatch.json](manual-session-bridge.dispatch.json) | Records the cross-capability route, gates, owner boundaries, and expected receipt. |
| [DESIGN-TRANSPORT.md](DESIGN-TRANSPORT.md) | Preserves source selection, template evidence, decisions, gaps, and plan-readiness conditions. |
| [INVOKE-RESULT.md](INVOKE-RESULT.md) | Returns the Invoke design-mode result. |

## Current Result

- Design unit: one approved read/preview skill request, one explicit desk target,
  one operator poll, one atomic claim, late skill disclosure, and one
  kernel-bound execution result.
- Distill verdict: `pass` for that unit.
- Decision gate: `pass`; five blocker decisions and the prior manual-poll
  boundary are recorded in `DECISIONS.md`.
- Invoke phase: `pass`; implementation mismatches remain plan obligations, not
  unresolved design choices.
- Runtime mutation: none in this Invoke run.

## Next Route

Run `invoke plan` against this approved package when planning is requested.
Plan mode should produce the implementation layering artifact, work-pack, SWUs,
and validation strategy; `task-session` remains the owner of source mutation.
