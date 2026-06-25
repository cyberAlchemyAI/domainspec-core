---
tags: [ide, ergonomics, unified-spine, restraint-contract, necronomicon, owner-boundary, altitude-1]
node_type: feature
layer: product, workflow, governance
nature: design-seed
status: strategy-proposal
created: 2026-06-24
spine_dimension: restraint-floor
admission: admitted (the invariant floor — every other coordinate sits on it)
promotion_gate: PRODUCT-VIEW.md owner (draft → accepted)
derived_from: development/unified-product-view/research.md#e2--restraint-owner-boundary-spine-initial-position
---

# Restraint Floor (Spine Coordinate)

> **Model revised 2026-06-24** (`2026-06-24-spine-model-premature-lock-review`):
> the spine is an **open coordinate space**, not a vertical stack. This is one
> coordinate (the invariant floor), not "altitude 1" — coordinates are unordered.
> New coordinates are admitted through the gate in
> [../UNIFIED-PRODUCT-VIEW.md](../UNIFIED-PRODUCT-VIEW.md) §"Coordinate Admission".

The **invariant floor** of the IDE Ergonomics coordinate space. It answers one
question for every conversation moment: *may this safely become something?*

> A conversation moment may become a candidate, a draft, a preview, or a recorded
> intent — but it may **not** become a canonical change, an execution, or a route
> switch without an explicit human gate.

This is the load-bearing word *safely* in the product's one-sentence definition
([../PRODUCT-VIEW.md](../PRODUCT-VIEW.md) §One-Sentence Product). It is the
**floor**: every other altitude may exist only on top of it, and nothing above
may breach it. Derived from the E2 explorer brief; see
[../UNIFIED-PRODUCT-VIEW.md](../UNIFIED-PRODUCT-VIEW.md) for how it composes with
the other two altitudes.

## Honest scope (claim ≤ proof)

The adversarial review of the unified view
([../development/unified-product-view/findings.md](../development/unified-product-view/findings.md)
§"Claim ≤ Proof") demoted this altitude from a spine novelty to its honest form:

- **The per-row restraint boundaries are FEDERATION-INHERITED, not new.** They
  already exist in [../PRODUCT-VIEW.md](../PRODUCT-VIEW.md):188-193 —
  "no canonical definition promotion / does not switch the active route /
  handoff is not execution proof".
- **The floor's actual NET contribution is two upgrades** the explorers' weak
  points forced (below). The *contract* is inherited; the *upgrades* are new.

So this package's job is not to invent restraint — it is to (a) name the single
contract all primitives already share, and (b) carry the two upgrades.

## The shared restraint contract

One invariant, re-applied per transition type. Five surface phrasings of the same
rule:

| Primitive | What is BLOCKED | Who owns promotion / the gate |
| --- | --- | --- |
| Definition candidate | no canonical definition promotion | Definitions Governance |
| Side node | does not switch the active route | Necronomicon `side_note_queue`; user intent owns the switch |
| Handoff draft | handoff is not execution proof | next owner (durable start point, not a receipt) |
| Route ambiguity | selection records intent; does not execute | Dispatch Spec route recorded |
| Delegated-run preview | no subagent spawn without explicit approval | Dispatch Spec + explicit user approval |
| Park / ignore | no write by default | none (but the non-action is logged — see below) |
| Self-assembling action | assembled + green ≠ shipped; criterion frozen | decision-gate + real lifecycle owner |

Source backbone: `arcanum/spells/necronomicon/README.md` §No-Promotion Guardrails
(what the harness *may create* vs *must not promote by itself*) and the
[../ERGONOMICS-OPPORTUNITIES.md](../ERGONOMICS-OPPORTUNITIES.md) Anti-Patterns
list — every anti-pattern is a *breach of restraint*, which is the contract
stated as its violations.

## The two net-new upgrades

Both come from the explorers' named weak points and are carried even at MVP:

1. **Graduated-trust dial.** Pure restraint taxes a power user — candidate-first /
   preview-first / gate-on-everything is latency tax for a fluent operator. An
   explicit operator command (e.g. `invoke define`) may route directly, bypassing
   the candidate stage. "Backend" must mean *default-hidden, expert-summonable* —
   not *absent*. This is also what keeps Altitude 2's grammar latent for novices
   yet reachable for experts.
2. **Logged non-action.** Park/ignore is the most-used state, so it must emit a
   workflow-evidence signal even though it writes no artifact — otherwise the
   "more workflow evidence" gain ([../PRODUCT-VIEW.md](../PRODUCT-VIEW.md):122-123)
   is contradicted by its own most-common path.

## Boundary

This altitude does not relocate ownership — it *lifts owner boundaries to the
surface*. The card never assumes an owner's authority; that is precisely the
guarantee that lets Altitude 2's grammar be shown at all (the grammar can be
displayed because the floor guarantees it cannot act).

## Residue

- The graduated-trust dial is an escape hatch where grammar "leaks back" to the
  surface on demand — its exact reach (which commands bypass which stages) is
  unspecified.
- Logged-non-action needs a concrete signal shape so park/ignore evidence is
  usable, not noise.

## Source trail

- [../UNIFIED-PRODUCT-VIEW.md](../UNIFIED-PRODUCT-VIEW.md) — the spine this floor anchors
- [../development/unified-product-view/research.md](../development/unified-product-view/research.md) — E2 brief, verbatim
- [../development/unified-product-view/findings.md](../development/unified-product-view/findings.md) — the demotion to honest scope
- `arcanum/spells/necronomicon/README.md` — no-promotion guardrails, capture-first
