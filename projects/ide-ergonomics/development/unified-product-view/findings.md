---
tags: [ide, product, arcanum, unified-spine, synthesis]
node_type: findings
is_session: false
layer: product
nature: unified-product-view
status: draft
created: 2026-06-24
---

# Findings: The Unified IDE Ergonomics Product View

## Product (one sentence)

IDE Ergonomics is a **restraint-floored, dispatch-grammar-routed, lifecycle-aware**
routing layer for AI work in an IDE: when a conversation produces a definition,
side note, handoff, route choice, or delegation opportunity, it surfaces a small
owner-safe card that helps the user choose the right *governed* next step —
without ever promoting, executing, or switching routes on its own
(PRODUCT-VIEW.md §One-Sentence Product; E2 thesis).

## The Unifying Spine

The three explorer briefs are not three rival spines; they are **three altitudes
of one spine**, and that is why a synthesis can subsume rather than pick. Each
explorer found a real organizing object, but each object lives at a different
height and answers a different question. They stack:

1. **Restraint floor (E2) — the invariant (federation-inherited).** *What may
   this moment safely become?* A conversation moment may become a candidate,
   draft, preview, or recorded intent, but never a canonical change, execution,
   or route switch without an explicit human gate (E2 §1). This is the
   load-bearing word "safely" in the product's own definition (PRODUCT-VIEW.md
   §One-Sentence Product). It is the **floor**: every other layer may exist only
   on top of it, and nothing above may breach it. **Honest scope:** the
   per-row restraint (no canonical promotion / does not switch the active route /
   handoff is not execution proof) is **already stated by the existing
   federation** at PRODUCT-VIEW.md:188-193 — the spine does not introduce it.
   The floor altitude's actual **net contribution** is only the two upgrades
   carried below: the **graduated-trust dial** and the **logged non-action**.
   It earns its place as the inherited+upgraded guarantee, not as a spine
   novelty.

2. **Dispatch-grammar routing layer (E1) — the vocabulary.** *Where can this
   moment go, and in what shape?* Every primitive is a projection of a single
   Arcanum dispatch document — operator phrase, route pattern, capability
   reference, frame handoff, gate, residue, spell candidate
   (ARCANUM-DISPATCH-SYNTHESIS.md:19-28; E1 §3). The dispatch object is "the
   missing middle between poetic operator language and executable sigil
   sequences" (ARCANUM-DISPATCH-SYNTHESIS.md:13), and the product names the same
   negative space (PRODUCT-VIEW.md:17-18). This is the **routing vocabulary**:
   it tells the floor *which owners and shapes* a moment can be routed into.
   **Honest scope:** this altitude is **LATENT** (E1's own weak point) and
   therefore carries **no surface-level decision power** — the user never sees
   the grammar and never decides anything *because* of it. It earns its place
   as **internal coherence**: it is the reason the many owners are read as **one
   dispatch vocabulary** rather than coincidentally adjacent widgets. It is not
   a third source of card-level decision work.

3. **Lifecycle progression model (E3) — the position (the load-bearing axis).**
   *Where in the larger arc of work does this moment sit, and what comes next?*
   At the witness — the card the user actually sees — **this is the only
   altitude that does irreducible card-level decision work.** Its keystone: it
   converts the federation's flat set of co-equal **peer** routes into a
   **partially-ordered progression** carrying **receipt-debt** between the same
   primitives. The spine can say "routing the handoff now skips the Define
   receipt the 'evidence rail' term still owes" — an ordering and a debt that
   the flat peer-menu structurally **cannot** express. The governed funnel
   Discover → Research → Decide → Define → Design/Plan → Execute
   (necronomicon/README.md Discovery-To-Definition Funnel) places each card in
   that progression. Connective is the **full-graph reader** that sees all
   pending state at once; a single transition card is a **degenerate one-node
   view** of that same graph (E3 §3). This is the **progression model**, and it
   is the genuinely-subsuming axis on which the spine survives as more than a
   re-skin (see the Witness Walkthrough below).

### Why this subsumes rather than picks

Each explorer's thesis is *true at its own altitude and over-reaches at the
others* — and each explorer said so in Section 4. The subsumption works by
taking each spine **only where it is strongest** and using the others' named
weak points as the boundary that keeps it there:

- **E1 is strongest as architecture, weakest as UI** (E1 §4): the dispatch
  grammar is the right internal model but "must stay LATENT" — full-vocab
  surfacing is the "dashboard with no next action" fail (PRODUCT-VIEW.md:251)
  and violates the Weaver invariant "routing does not require full schema
  injection" (WEAVER-EXTRACTION.md:115). So we adopt the grammar as the
  **latent routing layer**, never as a UI dump. The card shows one bounded
  slice (3-7 capability cards; ARCANUM-DISPATCH-SYNTHESIS.md:22), summoned by
  experts, not the whole vocabulary.

- **E2 is the only thing ALL primitives share** (E2 §3): a single grammar is
  impossible because the substrate has many grammars with different promotion
  rules, but a single restraint contract holds across all of them. So restraint
  is the **floor**, not one layer among peers. But pure restraint taxes the
  power user (E2 §4), so the floor carries a **graduated-trust dial** (below)
  and a **logged-non-action** rule (below).

- **E3 is strongest as organizing model, weakest as build order** (E3 §4): the
  phase-graph is the right *map* of where work sits, but it over-builds the MVP,
  which is "one bounded card" (PRODUCT-VIEW.md:178-184). So lifecycle is the
  **progression model** — and the MVP is explicitly the **single-node view**,
  honoring E3's own caveat that the first proof is one edge, not the graph.

The three stack because they are **answers to three different questions**
(may-it-be-safe / where-can-it-go / where-in-the-arc). But — claim ≤ proof — they
are **not** three co-equal sources of card-level decision power. At the witness,
**only the lifecycle altitude does irreducible decision work**: the partial order
plus receipt-debt is the one thing the flat federation structurally cannot
express. The restraint floor is **federation-inherited** (its per-row boundaries
already live in PRODUCT-VIEW.md:188-193), contributing only the dial and the
logged non-action. The grammar altitude is **latent**, contributing internal
coherence (the many owners are one vocabulary), not surface decisions. So the
honest framing is: the spine **survives on one genuinely-subsuming axis**
(lifecycle ordering + receipt-debt), resting on an inherited+upgraded restraint
floor and a latent unifying grammar. That is still a real unification — just an
honestly-scoped one, not "each altitude does work the others can't."

## Layered Model (diagram)

```text
        +-------------------------------------------------------------+
ALTITUDE|  LIFECYCLE PROGRESSION (E3)        - WHERE IN THE ARC?       |
  3     |  Discover>Research>Decide>Define>Design/Plan>Execute (+Maintain)
        |  Connective = full-graph reader · single card = one-node view|
        |  [strong default path, legally bypassable - NOT hard control]|
        |  <<< ONLY altitude with card-level decision power:           |
        |      partial order + receipt-debt over the flat peer set >>> |
        +---------------^---------------------------------------------+
                        | positions each route in a progression
        +---------------+---------------------------------------------+
ALTITUDE|  DISPATCH-GRAMMAR ROUTING (E1)     - WHERE CAN IT GO?        |
  2     |  one dispatch doc, projected: phrase·pattern·capability·     |
        |  handoff·gate·residue·spell-candidate   [LATENT, 3-7 cards]  |
        |  expert-summonable, never a full-vocab UI dump               |
        |  <<< LATENT: internal coherence only, NO surface decision >>>|
        +---------------^---------------------------------------------+
                        | every route obeys the floor
        +---------------+---------------------------------------------+
ALTITUDE|  RESTRAINT FLOOR (E2)              - MAY IT SAFELY BECOME?   |
  1     |  candidate!=promotion · preview!=execution · side-note!=switch|
        |  handoff!=execution-proof · recommendation!=execution        |
        |  <<< per-row boundaries FEDERATION-INHERITED (PV:188-193);   |
        |      spine's net add = dial + logged non-action only >>>     |
        |  +graduated-trust dial  +logged non-action (park/ignore)     |
        |  INVARIANT - nothing above may breach it                     |
        +-------------------------------------------------------------+
```

Read bottom-up: the floor is the (inherited+upgraded) guarantee, the grammar is
the latent vocabulary that makes the routes one set, and the lifecycle is the one
altitude that does card-level decision work — it orders the routes and surfaces
the receipt-debt between them.

## Witness Walkthrough: "evidence rail" through both paths

This is the concrete proof that the spine is **not a re-skin**. Run the exact
span from the product's own story — the "evidence rail" moment
(PRODUCT-VIEW.md §The Story, :38-51) — through both the flat federation and the
spine, and compare what the user can see.

**Path A — through the flat federation (today).** The moment yields **six
unordered, co-equal peer routes**, each with its own owner and boundary
(PRODUCT-VIEW.md:184-193):

| # | Peer route | Owner | Boundary |
| --- | --- | --- | --- |
| 1 | Definition candidate ("evidence rail") | Definitions Governance | no canonical promotion |
| 2 | Side node (observability tangent) | workflow memory | does not switch the active route |
| 3 | Handoff draft (next session) | next owner | handoff is not execution proof |
| 4 | Route ambiguity (`invoke`/`dispatch-spec`/`task-session`) | Dispatch Spec | records intent, does not execute |
| 5 | Delegated-run preview (two-lane split) | Dispatch Spec + user | no spawn without approval |
| 6 | Park or ignore | none | no write by default |

These are a **flat set**. The menu can show all six, but it has **no structure
to say one route owes another anything**, or that one should come before
another. Each is an island with a boundary.

**Path B — through the spine.** The **identical six routes** receive lifecycle
tags (E3 §2):

| # | Same route | Lifecycle tag |
| --- | --- | --- |
| 1 | "evidence rail" definition | **Define** |
| 2 | observability side node | **Discover** |
| 3 | session handoff | **Design/Plan** |
| 4 | route ambiguity | **Decide** |
| 5 | two-lane split | **Research** |
| 6 | park/ignore | (no stage; logged non-action) |

Tagging induces a **partial order** (Discover → Research → Decide → Define →
Design/Plan) over the *same* six routes, and that order is what makes
**receipt-debt** expressible: the spine can now say

> "Routing the **handoff** (Design/Plan) now skips the **Define** receipt that
> the 'evidence rail' term still owes" —

a statement Path A's flat peer-menu **structurally cannot make**, because it has
no ordering relation between routes 1 and 3 and no notion of a receipt one route
owes before another fires.

**What this proves and bounds.** The restraint boundaries in both tables are
*the same* (Path B inherited them from Path A — the floor is not new). The
grammar that lets all six be read as one dispatch vocabulary is latent in both
(the user sees neither). The **single difference the user could observe** is the
ordering + receipt-debt — which is exactly the lifecycle altitude's irreducible
contribution, and exactly the evidence that the spine subsumes rather than
re-skins. Claim ≤ proof: this is one worked span, not a general guarantee; it
establishes the axis is real, not that every span produces a debt.

## Primitive → Spine-Role Mapping

For every existing primitive: its **restraint-floor invariant** (E2), its
**grammar role** (E1 latent dispatch-doc projection), and its **lifecycle stage**
(E3). Where E1 flagged a primitive as resisting the grammar (intent-latitude,
field-hover), that is marked — claim demoted, not inflated.

| Primitive | Restraint-floor invariant (E2) | Grammar role (E1, latent) | Lifecycle stage (E3) |
| --- | --- | --- | --- |
| Transition card | candidate/draft/preview only; no promotion (PRODUCT-VIEW.md:236-242) | the dispatch doc's intent block, authored live (E1 §3) | the single-node view of the whole graph (E3 §3) |
| Side node | does not switch the active route (PRODUCT-VIEW.md:189) | residue / side_note_queue (E1 §2) | Discover (E3 §2) |
| Handoff (composer + teammate memo) | handoff is not execution proof (PRODUCT-VIEW.md:190) | frame handoff / delegation_boundary (E1 §2) | Design/Plan (E3 §2) |
| Route menu | bounded menu, not open tool drawer (PRODUCT-VIEW.md:158) | route pattern / ChoiceCard, 3-7 cards (WEAVER:43-48) | spans the funnel; renders available stages |
| Subagent preview | no spawn without explicit approval (PRODUCT-VIEW.md:192) | route pattern + gate / subagent_strategy (E1 §2) | Research (E3 §2) |
| Knowledge-entry refs | read-only popup; cite, do not promote (E2 §2) | capability ref + residue / entity_component_reference (E1 §2) | Discover/Research (E3 §2) |
| Field-hover | pure read; no route/gate/handoff effect (E1 §4) | **resists grammar** — LSP peek, fits by analogy only (E1 §4) | Discover/Research (E3 §2) |
| Intent-latitude | acts on the user's message pre-agent; records, not executes (E3 §4) | **resists grammar** — input-side operator phrase, by analogy (E1 §4) | input-side, Decide-adjacent (E3 §2,§4) |
| Route ambiguity | selection records intent; does not execute (PRODUCT-VIEW.md:191) | capability reference (E1 §2) | Decide (E3 §2) |
| Definition candidate | no canonical definition promotion (PRODUCT-VIEW.md:188) | operator phrase → capability ref (definitions-governance) | Define (E3 §2) |
| Craft panel | exports + asks one route question; no auto-route (PRODUCT-VIEW.md:118) | capability ref + gate / scu_swu_reduction (E1 §2) | Execute selection (E3 §2) |
| Connective | recommendation is not execution; governed write path only (E2 §2) | gate Pareto / pareto_gate + tournament over lanes (E1 §2) | **reads ALL stages** — full-graph reader (E3 §3) |
| Self-assembling | assembled + green != shipped; criterion frozen (E2 §2) | spell candidate + validation_loop / toy_game (E1 §2) | Maintain meta-loop over all stages (E3 §2) |
| Evidence rail | receipts/blocked fields shown, never silently mutated (E2 §2) | gate + residue / observability grouped by one dispatch_id (E1 §3) | cross-stage observability spine |

Two primitives (field-hover, intent-latitude) are marked **resists grammar** per
E1 §4: they carry a restraint invariant and a lifecycle stage cleanly, but only
attach to the dispatch grammar by analogy. This is preserved, not smoothed over —
it is exactly the kind of seam a collapse-check should watch.

## MVP Shape

The MVP is **one bounded conversation-transition card = the one-node view of the
lifecycle graph** (E3 §3,§4; PRODUCT-VIEW.md:178-184). It deliberately does *not*
build the phase-graph, the Craft-state read, or Connective — E3 itself names this
over-build as its weak point: "first falsifiable question is 'can a user choose
the right governed route from ONE conversation moment?' — a single edge, not the
graph" (E3 §4).

The MVP card menu (unchanged from the owner; PRODUCT-VIEW.md:184-193):

| Route | User sees | Restraint-floor boundary |
| --- | --- | --- |
| Definition candidate | term, local context, destination, packet preview | no canonical definition promotion |
| Side node | saved aside with class, source span, optional follow-up | does not switch the active route |
| Handoff draft | destination, summary, source refs, gaps, next prompt | handoff is not execution proof |
| Route ambiguity | suggested owners (`invoke`, `dispatch-spec`, `task-session`) | selection records intent; does not execute |
| Delegated-run preview | role cards, receipts, join policy, permission prompt | no subagent spawn without explicit approval |
| Park or ignore | save for later or dismiss | no write by default — **but the non-action is logged** (E2 §4) |

Two restraint upgrades the explorers' weak points require, carried even at MVP:

- **Graduated-trust dial** (E2 §4): an explicit operator command (e.g.
  `invoke define`) may route directly, bypassing the candidate stage, so a
  fluent operator is not taxed by candidate-first/preview-first on every move.
  The dial keeps the grammar latent for novices and *summonable* for experts —
  satisfying E1's "default-hidden, expert-summonable" requirement (E1 §4, E2 §4)
  without surfacing the full vocabulary as controls.
- **Logged non-action** (E2 §4): park/ignore is the most-used state, so it must
  emit a workflow-evidence signal even though it writes no artifact — otherwise
  the "more workflow evidence" gain (PRODUCT-VIEW.md:122-123) is contradicted by
  its own most-common path.

The first proof remains static conversation fixtures, not an IDE plugin
(PRODUCT-VIEW.md:196-224) — the product value under test is the routing decision,
not host integration.

## Owner-Boundary Preservation

The spine **lifts owner boundaries to the IDE surface; it does not relocate
ownership** (E2 §2-3; PRODUCT-VIEW.md §Product Boundary, 302-318). The restraint
floor is precisely the promise that the card never assumes an owner's authority:

- definitions belong to Definitions Governance;
- route shape belongs to Dispatch Spec — the dispatch object *validates* and
  *does not execute* (WEAVER-EXTRACTION.md:115 "ChainWeaver delegates
  execution"); the card must not imply it OWNS the route (E1 §4);
- side notes and handoffs belong to Necronomicon-style workflow memory, which
  "does not promote by itself" (E2 §2);
- execution belongs to Task Session or another approved owner;
- reusable spells route through Spellcraft.

Every "grammar role" in the mapping table is a *projection for display*, never a
transfer of authority. This is the E1 authority risk (E1 §4) discharged by the
E2 floor: the grammar can be shown because the floor guarantees it cannot act.

## Relationship to existing PRODUCT-VIEW.md

This is **build-from-owned, not replace.** The existing
`projects/ide-ergonomics/PRODUCT-VIEW.md` is the **owner** of the IDE Ergonomics
product definition, and this findings document *extends* it — it does not
supersede it. Concretely:

- The **one-sentence product**, the **five-step path**
  (PRODUCT-VIEW.md:129-136), the **MVP card menu** (PRODUCT-VIEW.md:184-193),
  the **fixture test plan** (PRODUCT-VIEW.md:196-224), and the **Product
  Boundary** (PRODUCT-VIEW.md:302-318) are all inherited unchanged. This
  document quotes them as authority, it does not redefine them.
- What this document *adds* is the **organizing spine** — the three-altitude
  subsumption that explains *why* the eleven-plus primitives are one product and
  not eleven widgets, and the two restraint upgrades (graduated-trust dial,
  logged non-action) the explorers' weak points surfaced.
- If a future edit needs to change the product's MVP shape or boundary, the edit
  belongs in PRODUCT-VIEW.md (the owner); this document would then be updated to
  cite it. The dependency points one way: findings.md -> PRODUCT-VIEW.md.

## Claim <= Proof — demotions on record

- The "three orthogonal load-bearing altitudes, each doing work the others
  can't" framing is **demoted**: at the witness, only the **lifecycle** altitude
  does irreducible card-level decision work (partial order + receipt-debt). The
  restraint floor is **federation-inherited** (net add = dial + logged
  non-action); the grammar is **latent internal coherence** with no surface
  decision power. The spine survives on **one** genuinely-subsuming axis, not
  three.
- The dispatch grammar as a *UI* is **demoted to latent backend** (E1 §4); only
  its role as internal routing vocabulary / internal coherence is asserted.
- The phase-graph as a *build target* is **demoted to organizing model**; the
  MVP build is one node (E3 §4).
- field-hover and intent-latitude attach to the grammar **by analogy only**, not
  cleanly (E1 §4) — recorded as a known seam.
- The lifecycle funnel is a **strong default path, not a hard control-flow
  graph** — it is "explicitly NOT mandatory" and legally bypassable (E3 §4).
- E1 §4 self-flagged that the grammar mapping rests on prose docs and was *not*
  checked against `dispatch.schema.yml`; this synthesis inherits that
  unverified-against-schema status and does not upgrade it.

## Source Trail

- [research.md](research.md) — three explorer briefs, preserved verbatim
- [PRODUCT-VIEW.md](../../PRODUCT-VIEW.md) — owner of the product definition
- [ARCANUM-DISPATCH-SYNTHESIS.md](../../../../arcanum/formulae/dispatch-spec/ARCANUM-DISPATCH-SYNTHESIS.md) — dispatch object, vocabulary layers
- [WEAVER-EXTRACTION.md](../../../../arcanum/formulae/dispatch-spec/WEAVER-EXTRACTION.md) — route lifecycle + no-full-schema-injection invariant
- [ERGONOMICS-OPPORTUNITIES.md](../../ERGONOMICS-OPPORTUNITIES.md)
- necronomicon/README.md — Discovery-To-Definition funnel, no-promotion guardrails (cited via E2/E3)
