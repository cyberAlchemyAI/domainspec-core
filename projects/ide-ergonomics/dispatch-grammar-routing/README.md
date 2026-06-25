---
tags: [ide, ergonomics, unified-spine, dispatch-grammar, dispatch-composition, latent-layer, altitude-2]
node_type: feature
layer: product, workflow, governance
nature: design-seed
status: strategy-proposal
created: 2026-06-24
spine_dimension: routing-grammar
admission: admitted (latent — internal coherence only, no surface decision power)
promotion_gate: PRODUCT-VIEW.md owner (draft → accepted)
derived_from: development/unified-product-view/research.md#e1--operator-grammar-spine-initial-position
---

# Dispatch-Grammar Routing (Spine Coordinate)

> **Model revised 2026-06-24** (`2026-06-24-spine-model-premature-lock-review`):
> the spine is an **open coordinate space**, not a vertical stack. This is one
> coordinate (the latent routing vocabulary), not "altitude 2" — coordinates are
> unordered. Admission gate: [../UNIFIED-PRODUCT-VIEW.md](../UNIFIED-PRODUCT-VIEW.md)
> §"Coordinate Admission".

The **routing vocabulary** of the IDE Ergonomics coordinate space. It answers:
*where can this moment go, and in what shape?*

Every primitive is a projection of a single Arcanum **dispatch document** — the
"missing middle between poetic operator language and executable sigil sequences"
(`arcanum/formulae/dispatch-spec/ARCANUM-DISPATCH-SYNTHESIS.md`:13). The product
names the same negative space ([../PRODUCT-VIEW.md](../PRODUCT-VIEW.md):17-18).
Derived from the E1 explorer brief; composes with the other altitudes in
[../UNIFIED-PRODUCT-VIEW.md](../UNIFIED-PRODUCT-VIEW.md).

## Honest scope (claim ≤ proof) — this altitude is LATENT

The adversarial review demoted this altitude hard, and the demotion is the most
important thing about this package:

- **It carries NO surface-level decision power.** The user never sees the grammar
  and never decides anything *because* of it.
- **It earns its place as internal coherence** — it is the reason the many
  distinct owners read as **one** dispatch vocabulary rather than coincidentally
  adjacent widgets. That is its whole job.
- **Surfacing it as UI is a failure mode**, not a feature: rendering the full
  vocabulary as controls is the "dashboard with no next action" fail
  ([../PRODUCT-VIEW.md](../PRODUCT-VIEW.md):251) and violates "routing does not
  require full schema injection" (`arcanum/formulae/dispatch-spec/WEAVER-EXTRACTION.md`:115).

So this package is **architecture, not UI**. It defines the internal model; the
card shows one bounded slice (3-7 capability cards), expert-summonable via
Altitude 1's graduated-trust dial, never a full-vocabulary dump.

## Primitive → dispatch-grammar projection (latent)

| Primitive | Vocabulary layer | Composition / technique |
| --- | --- | --- |
| Transition card | operator phrase → structured slots | the dispatch `intent` block, authored live |
| Route menu | route pattern | `route_menu` / ChoiceCard, bounded 3-7 |
| Route ambiguity | capability reference | `invoke` / `dispatch-spec` / `task-session` |
| Side node | residue | `residue_ledger` / `memory_loop` |
| Handoff / teammate memo | frame handoff | `frame_handoff` / `delegation_boundary` |
| Subagent preview | route pattern + gate | `dialectic` / `tournament` / `subagent_strategy` |
| Knowledge refs / field-hover | capability ref + residue | `entity_component_reference` *(by analogy — see seam)* |
| Spell/sigil nudge | spell candidate | `spell_candidate` / validation-loop |
| Evidence rail | gate + residue | `observability` grouped by one `dispatch_id` |
| Craft panel | capability ref + gate | `scu_swu_reduction` |
| Connective | gate (Pareto) | `pareto_gate` + tournament over lanes |
| Self-assembling | spell candidate + gate | `validation_loop` + `toy_game`, frozen criterion |

Why the dispatch object is the right internal model: it is the only artifact that
already carries all five things every card needs — owner, frame handoff, gate,
residue, and a `dispatch_id` to tie siblings. Cards each need one *projection* of
it, not their own data model.

## Boundary

A projection is **for display, never a transfer of authority**. The dispatch
object *validates* route shape; it does not execute or promote (`WEAVER-EXTRACTION.md`:117
"ChainWeaver delegates execution"). The card must never imply it *owns* the route —
that authority risk is discharged by the Altitude 1 floor.

## Residue (known seams)

- **field-hover and intent-latitude attach by analogy only.** field-hover is a
  pure LSP "peek" with no route/gate/handoff; intent-latitude is input-side (acts
  on the user's message before the agent). Neither maps cleanly — recorded, not
  smoothed over.
- **Unverified against schema.** The mapping rests on prose docs and was **not**
  checked against `arcanum/formulae/dispatch-spec/dispatch.schema.yml`. Diff it
  before this mapping becomes build-load-bearing.

## Source trail

- [../UNIFIED-PRODUCT-VIEW.md](../UNIFIED-PRODUCT-VIEW.md) — the spine this layer routes within
- [../development/unified-product-view/research.md](../development/unified-product-view/research.md) — E1 brief, verbatim
- [../development/unified-product-view/findings.md](../development/unified-product-view/findings.md) — the demotion to latent/internal-coherence
- `arcanum/formulae/dispatch-spec/ARCANUM-DISPATCH-SYNTHESIS.md`, `WEAVER-EXTRACTION.md`, `TECHNIQUE-CATALOG.md`
