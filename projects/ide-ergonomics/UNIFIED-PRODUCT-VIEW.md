---
tags: [ide, product, arcanum, unified-spine, workflow, mvp]
node_type: product-view
is_session: false
layer: product
nature: product-brief
status: draft
created: 2026-06-24
supersedes: none
builds_on: PRODUCT-VIEW.md
source_dispatch: 2026-06-24-unified-ide-ergonomics-product-view
---

# Unified Product View: IDE Ergonomics

> **Build-from-owned.** This document does not replace
> [PRODUCT-VIEW.md](PRODUCT-VIEW.md) — it gives the federation of primitives that
> doc already owns a single **organizing spine**, distilled from the four Arcanum
> dispatch/composition sources (Necronomicon, Spellcraft, dispatch-spec, the
> Dispatch Synthesis). The one-sentence product, five-step path, MVP card menu,
> fixture test plan, and Product Boundary in PRODUCT-VIEW.md are inherited
> unchanged. Full evidence and the adversarial review trail:
> [development/unified-product-view/findings.md](development/unified-product-view/findings.md)
> (synthesis) and [research.md](development/unified-product-view/research.md)
> (the three explorer briefs, verbatim).

## One-Sentence Product

IDE Ergonomics is a **restraint-floored, dispatch-grammar-routed, lifecycle-aware**
routing layer for AI work inside an IDE: when a conversation produces a
definition, side note, handoff, route choice, or delegation opportunity, it
surfaces a small owner-safe card that helps the user choose the right *governed*
next step — without ever promoting, executing, or switching routes on its own.

The product is still "the missing moment between noticing useful work and safely
sending that work to the right place" (PRODUCT-VIEW.md §One-Sentence Product).
What is new here is the answer to *why eleven-plus primitives are one product and
not eleven widgets.*

## The Unifying Spine

The research set out three rival "spines," one per source cluster. The finding is
that they are **not rivals** — they are **three altitudes of one spine**, each
answering a different question, stacked so that each holds only where it is
strongest and is fenced by the next one's weak point.

```text
        +-------------------------------------------------------------+
ALTITUDE|  LIFECYCLE PROGRESSION (Spellcraft + Necronomicon funnel)    |
  3     |  Discover > Research > Decide > Define > Design/Plan > Execute
        |  Connective = full-graph reader · single card = one-node view|
        |  strong DEFAULT path, legally bypassable — not hard control  |
        |  <<< the ONLY altitude with card-level decision power:       |
        |      partial order + receipt-debt over the flat peer set >>> |
        +---------------^---------------------------------------------+
                        | positions each route in a progression
        +---------------+---------------------------------------------+
ALTITUDE|  DISPATCH-GRAMMAR ROUTING (dispatch-spec + Dispatch Synthesis)|
  2     |  one dispatch doc, projected: phrase·pattern·capability·     |
        |  handoff·gate·residue·spell-candidate     [LATENT, 3-7 cards]|
        |  expert-summonable, never a full-vocabulary UI dump          |
        |  <<< LATENT: internal coherence only, NO surface decision >>>|
        +---------------^---------------------------------------------+
                        | every route obeys the floor
        +---------------+---------------------------------------------+
ALTITUDE|  RESTRAINT FLOOR (Necronomicon no-promotion guardrails)      |
  1     |  candidate!=promotion · preview!=execution · side-note!=switch|
        |  handoff!=execution-proof · recommendation!=execution        |
        |  per-row boundaries FEDERATION-INHERITED (PRODUCT-VIEW:188-193)
        |  spine's NET add = graduated-trust dial + logged non-action  |
        |  INVARIANT — nothing above may breach it                     |
        +-------------------------------------------------------------+
```

**Altitude 1 — Restraint floor (the invariant).** *May this moment safely
become something?* A conversation moment may become a candidate, draft, preview,
or recorded intent, but never a canonical change, an execution, or a route switch
without an explicit human gate. This is the load-bearing word *safely* in the
product's own definition. **Honest scope:** the per-row boundaries are already in
the existing federation (PRODUCT-VIEW.md:188-193); the spine's *net* contribution
is only the two upgrades below — the graduated-trust dial and logged non-action.

**Altitude 2 — Dispatch-grammar routing (the vocabulary).** *Where can it go, in
what shape?* Every primitive is a projection of one Arcanum dispatch document —
the "missing middle between poetic operator language and executable sigil
sequences" (ARCANUM-DISPATCH-SYNTHESIS.md:13). **Honest scope:** this layer is
**latent** — the user never sees the grammar and never decides anything *because*
of it. It earns its place as *internal coherence*: it is the reason the many
distinct owners read as **one** dispatch vocabulary rather than coincidentally
adjacent widgets. Surfacing it as UI is the "dashboard with no next action" fail
(PRODUCT-VIEW.md:251) and violates "routing does not require full schema
injection" (WEAVER-EXTRACTION.md:115).

**Altitude 3 — Lifecycle progression (the load-bearing axis).** *Where in the
larger arc of work does this moment sit?* The governed funnel
Discover → Research → Decide → Define → Design/Plan → Execute
(necronomicon/README.md). **At the card the user actually sees, this is the only
altitude that does irreducible decision work:** it converts the federation's flat
set of co-equal *peer* routes into a **partially-ordered progression** carrying
**receipt-debt** between the same primitives. Connective is the full-graph reader
that sees all pending state at once; a single transition card is the degenerate
**one-node view** of that same graph.

### Claim ≤ proof — what the spine actually buys

Verified by the dispatch's adversarial review (a `definitional-soundness`
skeptic), the honest framing is **not** "three altitudes each do work the others
can't." It is narrower and survives:

- The restraint floor's per-row boundaries are **federation-inherited**, not a
  spine novelty (net add = dial + logged non-action).
- The grammar altitude is **latent** — internal coherence, zero surface decision.
- Only the **lifecycle altitude** does card-level decision work: the partial
  order + receipt-debt is the one thing the flat federation structurally cannot
  express.

So the spine **survives on one genuinely-subsuming axis** (lifecycle ordering +
receipt-debt), resting on an inherited+upgraded restraint floor and a latent
unifying grammar. That is still a real unification — just an honestly-scoped one.

## The Witness: "evidence rail" through both paths

The concrete proof the spine is **not a re-skin** (from PRODUCT-VIEW.md §The
Story, :38-51).

**Today — the flat federation** turns the moment into **six unordered, co-equal
peer routes**, each an island with its own owner and boundary:

| Peer route | Owner | Boundary |
| --- | --- | --- |
| Definition candidate ("evidence rail") | Definitions Governance | no canonical promotion |
| Side node (observability tangent) | workflow memory | does not switch the active route |
| Handoff draft | next owner | handoff is not execution proof |
| Route ambiguity | Dispatch Spec | records intent, does not execute |
| Delegated-run preview (two-lane split) | Dispatch Spec + user | no spawn without approval |
| Park / ignore | none | no write by default |

The menu can show all six, but it has **no structure to say one route owes
another anything**, or that one should come first.

**Through the spine** — the **identical six routes** get lifecycle tags:
side-node = *Discover*, "evidence rail" = *Define*, handoff = *Design/Plan*,
route-ambiguity = *Decide*, two-lane split = *Research*. That induces a partial
order over the *same* routes, and the order makes **receipt-debt** expressible:

> "Routing the **handoff** (Design/Plan) now skips the **Define** receipt the
> 'evidence rail' term still owes."

A statement the flat peer-menu **structurally cannot make**. The restraint
boundaries are identical in both paths (inherited, not new); the grammar is
latent in both (unseen). The single observable difference is the ordering +
receipt-debt — exactly the lifecycle altitude's irreducible contribution. *(One
worked span — it establishes the axis is real, not that every span produces a
debt.)*

## Primitive → Spine-Role Mapping

Every existing primitive, placed on all three altitudes: its restraint-floor
invariant, its (latent) grammar role, and its lifecycle stage. Two primitives
attach to the grammar **by analogy only** — marked, not smoothed over.

| Primitive | Restraint-floor invariant | Grammar role (latent) | Lifecycle stage |
| --- | --- | --- | --- |
| Transition card | candidate/draft/preview only; no promotion | dispatch `intent` block, authored live | the single-node view of the whole graph |
| Side node | does not switch the active route | residue / side_note_queue | Discover |
| Handoff (composer + teammate memo) | handoff is not execution proof | frame handoff / delegation_boundary | Design/Plan |
| Route menu | bounded menu, not open tool drawer | route pattern / ChoiceCard, 3-7 cards | spans the funnel; renders available stages |
| Subagent preview | no spawn without explicit approval | route pattern + gate / subagent_strategy | Research |
| Knowledge-entry refs | read-only popup; cite, do not promote | capability ref + residue / entity reference | Discover/Research |
| Field-hover | pure read; no route/gate/handoff effect | **resists grammar** — LSP peek, by analogy | Discover/Research |
| Intent-latitude | acts pre-agent; records, not executes | **resists grammar** — input-side, by analogy | input-side, Decide-adjacent |
| Route ambiguity | selection records intent; does not execute | capability reference | Decide |
| Definition candidate | no canonical definition promotion | operator phrase → definitions-governance | Define |
| Craft panel | exports + asks one route question; no auto-route | capability ref + gate / scu_swu_reduction | Execute selection |
| Connective | recommendation is not execution; governed write only | gate Pareto / pareto + tournament over lanes | **reads ALL stages** — full-graph reader |
| Self-assembling | assembled + green != shipped; criterion frozen | spell candidate + validation_loop / toy_game | Maintain meta-loop over all stages |
| Evidence rail | receipts shown, never silently mutated | gate + residue / observability under one dispatch_id | cross-stage observability spine |

## MVP Shape

The MVP is **one bounded conversation-transition card = the one-node view of the
lifecycle graph** (unchanged menu from PRODUCT-VIEW.md:184-193). It deliberately
does *not* build the phase-graph, the Craft-state read, or Connective — that is
the lifecycle spine's named over-build risk. The first falsifiable question stays
small: *can a user choose the right governed route from ONE conversation moment?*

Two restraint upgrades the spine adds, carried even at MVP:

- **Graduated-trust dial** — an explicit operator command (e.g. `invoke define`)
  may route directly, bypassing the candidate stage, so a fluent operator is not
  taxed by candidate-first on every move. Keeps the grammar *latent for novices,
  summonable for experts* — without surfacing the full vocabulary as controls.
- **Logged non-action** — park/ignore is the most-used state, so it must emit a
  workflow-evidence signal even though it writes no artifact; otherwise the "more
  workflow evidence" gain is contradicted by its own most-common path.

First proof remains static conversation fixtures, not an IDE plugin — the value
under test is the routing decision, not host integration.

## Owner-Boundary Preservation

The spine **lifts owner boundaries to the IDE surface; it does not relocate
ownership.** Every "grammar role" above is a *projection for display*, never a
transfer of authority — the grammar can be shown precisely because the restraint
floor guarantees it cannot act.

- definitions → Definitions Governance;
- route shape → Dispatch Spec (the dispatch object *validates*, does not execute);
- side notes & handoffs → Necronomicon-style workflow memory (no self-promotion);
- execution → Task Session or another approved owner;
- reusable spells → Spellcraft; sigils → Sigil Development.

## Demotions on Record (claim ≤ proof)

- "Three orthogonal load-bearing altitudes" → **demoted**: only lifecycle does
  card-level decision work; floor is federation-inherited; grammar is latent.
- Dispatch grammar as *UI* → demoted to latent backend; asserted only as internal
  routing vocabulary / coherence.
- Phase-graph as *build target* → demoted to organizing model; MVP build is one
  node.
- Field-hover and intent-latitude attach to the grammar **by analogy only** —
  recorded as a known seam, not resolved.
- The lifecycle funnel is a **strong default path, not a hard control-flow
  graph** — explicitly bypassable.
- The grammar mapping rests on prose docs and was **not** checked against
  `dispatch.schema.yml`; this view inherits that unverified-against-schema status.

## Source Trail

- [PRODUCT-VIEW.md](PRODUCT-VIEW.md) — owner of the product definition (this view extends it)
- [ERGONOMICS-OPPORTUNITIES.md](ERGONOMICS-OPPORTUNITIES.md) — the 12-pattern federation
- [development/unified-product-view/findings.md](development/unified-product-view/findings.md) — cited synthesis (this view's basis)
- [development/unified-product-view/research.md](development/unified-product-view/research.md) — three explorer briefs, verbatim
- `arcanum/spells/necronomicon/README.md` — restraint floor + discovery→execute funnel
- `arcanum/arcana/spellcraft/SKILL.md` — phase/gate/handoff contract
- `arcanum/formulae/dispatch-spec/ARCANUM-DISPATCH-SYNTHESIS.md` + `WEAVER-EXTRACTION.md` — dispatch grammar + route lifecycle
- Dispatch ledger: `telemetry/agents/subagents-dispatch.yaml` → `2026-06-24-unified-ide-ergonomics-product-view`
