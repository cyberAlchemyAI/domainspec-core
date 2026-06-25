---
tags: [ide, ergonomics, unified-spine, lifecycle-phase-graph, spellcraft, necronomicon, connective, altitude-3]
node_type: feature
layer: product, workflow, governance
nature: design-seed
status: strategy-proposal
created: 2026-06-24
spine_dimension: work-arc-lifecycle
admission: admitted (the load-bearing decision coordinate)
promotion_gate: PRODUCT-VIEW.md owner (draft → accepted)
derived_from: development/unified-product-view/research.md#e3--lifecycle-phase-graph-spine-initial-position
---

# Work-Arc Lifecycle (Spine Coordinate)

> **Model revised 2026-06-24** (`2026-06-24-spine-model-premature-lock-review`):
> the spine is an **open coordinate space**, not a vertical stack. This is one
> coordinate, not "altitude 3" — coordinates are unordered. The review also found
> "lifecycle" was **two overloaded clocks**: this coordinate is the **work-arc**
> clock (the domain task's arc); the moment's own park/revisit/`Maintain` clock is
> now a separate **session-state** coordinate (see
> [../UNIFIED-PRODUCT-VIEW.md](../UNIFIED-PRODUCT-VIEW.md)). Where this README says
> "lifecycle" below, read **work-arc**.

The **progression model** — and, at the card the user actually sees, **the only
coordinate that does irreducible decision work**. It answers: *where in the larger
arc of work does this moment sit, and what comes next?*

The governed funnel
**Discover → Research → Decide → Define → Design/Plan → Execute**
(`arcanum/spells/necronomicon/README.md` Discovery-To-Definition Funnel) places
each card in a progression; Spellcraft's phase contract (`input / output / gate /
failure-policy / handoff / observability`, `arcanum/arcana/spellcraft/SKILL.md`
`<spell-contract>`) is the shape of each node. Derived from the E3 explorer brief;
composes with the other altitudes in
[../UNIFIED-PRODUCT-VIEW.md](../UNIFIED-PRODUCT-VIEW.md).

## Why this is the load-bearing axis

The keystone, confirmed by the unified view's `definitional-soundness` review:
this altitude **converts the federation's flat set of co-equal *peer* routes into
a partially-ordered progression carrying receipt-debt** between the same
primitives.

The witness ([../development/unified-product-view/findings.md](../development/unified-product-view/findings.md)
§"Witness Walkthrough"): the "evidence rail" span routed through the flat
federation yields six unordered peer routes; routed through this altitude they get
lifecycle tags —

| Route | Lifecycle stage |
| --- | --- |
| observability side node | **Discover** |
| two-lane split | **Research** |
| route ambiguity | **Decide** |
| "evidence rail" definition | **Define** |
| session handoff | **Design/Plan** |
| park / ignore | (no stage; logged non-action) |

— which induces a partial order and makes **receipt-debt** expressible:

> "Routing the handoff (Design/Plan) now skips the Define receipt the 'evidence
> rail' term still owes."

A statement the flat peer-menu structurally **cannot** make. That single
observable difference is the spine's irreducible contribution — the proof it is
not a re-skin.

## Connective is the flagship; the card is the one-node view

A card grammar describes one transition; the phase-graph describes *all pending
state at once*. **Connective** is the full-graph reader — it reads Craft state,
human indicators, user-test evidence, and a domain lens, then recommends the next
lane with an **expected receipt** and **expected owner route**
([../ERGONOMICS-OPPORTUNITIES.md](../ERGONOMICS-OPPORTUNITIES.md) §10). A single
transition card is the **degenerate one-node view** of that same graph.

## Honest scope (claim ≤ proof) — build order ≠ organizing model

E3's own named weak point, preserved: the phase-graph is the right *organizing
model* but **over-builds the MVP**. The MVP is **one bounded card = the one-node
view**, not the full graph ([../PRODUCT-VIEW.md](../PRODUCT-VIEW.md):178-184). The
first falsifiable question stays small: *can a user choose the right governed
route from ONE conversation moment?* — a single edge, not the graph. Connective
is the flagship *proof*, built only after the single-node card is shown to work.

## Residue (known seams)

- The funnel is a **strong default path, not a hard control-flow graph** — it is
  "explicitly NOT mandatory" and legally bypassable (e.g. explicit `invoke define`
  routes direct). A bypassable spine is a default, not enforced control flow.
- **Maintain** and **intent-latitude** sit awkwardly: maintain is a meta-loop
  *over* the lifecycle, not a stage *in* the funnel; intent-latitude acts on the
  user's message *before* the agent. Neither is a clean linear node.
- The witness establishes the axis is real on **one** worked span — not that every
  span produces a receipt-debt.

## Source trail

- [../UNIFIED-PRODUCT-VIEW.md](../UNIFIED-PRODUCT-VIEW.md) — the spine this altitude carries
- [../development/unified-product-view/research.md](../development/unified-product-view/research.md) — E3 brief, verbatim
- [../development/unified-product-view/findings.md](../development/unified-product-view/findings.md) — witness walkthrough + scope
- `arcanum/arcana/spellcraft/SKILL.md` (phase contract), `arcanum/spells/necronomicon/README.md` (funnel)
