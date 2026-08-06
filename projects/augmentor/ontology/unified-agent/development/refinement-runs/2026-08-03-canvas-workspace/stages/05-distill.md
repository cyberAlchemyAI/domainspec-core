# Stage 05 — Distill the coherent design unit

- Capability: `distill`
- Mode: `standard`
- Status: `pass`
- Additional agents: none; the approved dispatch authorizes one UX reviewer at
  Stage 07, not extra proposer/balancer agents

## Candidate whole

“Make every visible element part of a minimizable canvas workspace” is too broad
as an implementation unit. It mixes graph rendering, four content surfaces,
responsive policy, keyboard behavior, evidence generation, and source/generated
synchronization.

## Round 1

**Proposer:** use `GraphNodeCard` as the smallest coherent unit because it
directly addresses the screenshot and is independently testable.

**Balancer:** a typography-only unit cannot recompose the user's workspace idea.
It says nothing about where explanation, details, and evidence live or how their
visibility preserves selection.

**Reconciliation:** keep node typography as the first reversible implementation
slice, but not as the design's organizing unit.

## Round 2

**Proposer:** use one `CanvasWorkspaceShell` that owns placement and
presentation-state transitions for the graph viewport, toolbar, two docks, and
tray.

**Balancer:** this becomes task-shaped if it also owns ontology semantics,
content rendering, graph layout algorithms, persistence, and all responsive
polish.

**Reconciliation:** the shell owns only region composition, visibility policy,
focus mode, mobile mutual exclusion, and focus return. Existing components own
semantic controls, inspector content, explanation content, evidence content,
and graph rendering. `GraphNodeCard` remains a separately implementable child.

## Selected SCU

`CanvasWorkspaceShell` — a bounded composition and ephemeral presentation-state
controller for named workspace regions.

It is coherent because placement and visibility transitions must agree. It is
not task-shaped because it does not absorb content ownership, graph semantics,
data generation, routing, memory, or ontology authority.

## Recomposing proof

1. The existing graph becomes `GraphViewport` without changing its data source.
2. Existing controls move into `CanvasToolbar` and retain their handlers.
3. Existing guide/lane explanations render inside `ExplanationDock`.
4. Existing inspector renders inside `DetailsDock`; selection remains outside
   panel state.
5. Existing flows, legend, gaps, and text view render inside `EvidenceTray`.
6. The shell coordinates only visibility and focus; existing render functions
   continue to derive content from semantic state.
7. Source data still enters the canonical template through the existing build
   script, so the generated root HTML remains reproducible.

The SCU recomposes into the existing generated visualization without changing
ontology meaning. Handoff to Design.

