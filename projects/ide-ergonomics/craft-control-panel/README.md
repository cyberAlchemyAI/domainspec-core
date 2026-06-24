---
tags: [ide, ergonomics, craft, control-panel, decisions, interrogation, refine]
node_type: feature
layer: product, workflow, governance
nature: design-seed
status: strategy-proposal
created: 2026-06-23
---

# Craft Control Panel

An IDE-side ergonomic primitive for turning Craft state into a simple control
panel: export the current ledger state, show what is pending by node, and let the
user choose the next route through interactive question cards.

The panel treats Craft as the project workbench. It does not replace chat and it
does not hide the ledger. It reads `.craft/ledger.yml`, derived indexes, and the
human `CRAFT.md` view, then presents a small set of owner-safe actions such as
Interrogation, Decision Gate, Refine, export state, or defer.

## Why it belongs here

Craft already records contexts, blockers, gaps, decisions, definitions, artifacts,
next moves, and recomposition. The problem is that this state is still mostly
file-shaped. A user has to read the ledger or human view, decide which item is
live, remember which sigil owns the next move, and then ask for the right thing in
chat.

The control panel makes that transition visible:

- export current Craft state into a readable panel;
- show pending work by node instead of aggregate counts;
- expose decision, blocker, gap, and next-move rows as selectable items;
- offer route choices such as `interrogation`, `decision-gate`, `refine`, or
  "defer";
- ask one focused interactive question at a time, in the style of AI chat editor
  experiences, before running a consequential route.

## User Experience

The IDE opens a project control panel:

```text
Craft Control Panel
Scope: projects/arcanum-journey
Gate: flag

Pending by node:
- CTX-AJ-ROOT
  Active gaps: sigil map, Cyber Alchemy inclusion, chapter order
  Next move: make the route map durable as an inventory package

Suggested actions:
1. Refine next move
2. Ask an Interrogation question
3. Open Decision Gate
4. Export state
5. Defer
```

When the user selects a row, the panel asks a single focused question:

```text
What should happen with GAP-AJ-CHAPTER-ORDER-001?

Recommended: Refine the chapter-order target because it needs design before
execution.

Options:
- Refine this gap
- Ask one Interrogation question first
- Defer and keep it visible
- Explain / more context
```

The shape is intentionally close to modern AI editor UX: a small panel, route
buttons, one question at a time, and visible consequences.

## Owner-Safe Route

```text
Craft ledger or all-status export
  -> control-panel state model
  -> user selects a node, row, or next move
  -> interactive route question
  -> selected owner route: interrogation | decision-gate | refine | export | defer
  -> owner capability produces artifact, receipt, or blocked reason
  -> Craft receives the result only through a governed update
```

The panel can recommend a route. It cannot silently edit the ledger, close a
decision, resolve a blocker, or start a refinement run without the user selecting
the action and the owner capability recording proof.

## Primary Actions

- `export_state` - refresh the panel from `.craft/ledger.yml`, generated index,
  and `CRAFT.md`.
- `select_node` - focus one context, blocker, decision, gap, definition, artifact,
  recomposition record, or next move.
- `ask_interrogation` - ask one evidence-backed question and update the target
  artifact only after the answer.
- `open_decision_gate` - resolve a blocker-level multi-option decision with
  explicit trade-offs and an "Explain / more context" choice.
- `start_refine` - create a strategy proposal for a vague gap, design concern,
  project area, or next move before runtime-backed execution.
- `defer` - keep the item visible with no mutation.

## Files

- [SPEC.md](SPEC.md) - state export model, route option contract, interaction
  states, and pass conditions.

## Boundaries

- Strategy proposal only; no IDE extension or panel runtime is built here.
- `.craft/ledger.yml` remains the source of truth. The control panel is a read
  model until a selected owner route returns a receipt.
- `CRAFT.md`, `.craft/index.json`, and any panel export are generated views, not
  authority.
- The panel never resolves raw blockers directly and never treats route-shape
  validation as execution evidence.
