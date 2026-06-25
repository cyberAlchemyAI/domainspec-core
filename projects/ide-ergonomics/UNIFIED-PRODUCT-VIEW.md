---
tags: [ide, product, arcanum, unified-spine, coordinate-space, workflow, mvp]
node_type: product-view
is_session: false
layer: product
nature: product-brief
status: draft
created: 2026-06-24
revised: 2026-06-24
model_shape: open-coordinate-space
supersedes: none
builds_on: PRODUCT-VIEW.md
source_dispatch: 2026-06-24-unified-ide-ergonomics-product-view
revised_by_dispatch: 2026-06-24-spine-model-premature-lock-review
---

# Unified Product View: IDE Ergonomics

> **Build-from-owned.** This document does not replace
> [PRODUCT-VIEW.md](PRODUCT-VIEW.md) — it gives the federation of primitives that
> doc already owns a single **organizing model**. The one-sentence product,
> five-step path, MVP card menu, fixture test plan, and Product Boundary in
> PRODUCT-VIEW.md are inherited unchanged.
>
> **Revised 2026-06-24** after a red-team review (`2026-06-24-spine-model-premature-lock-review`)
> found the original "three-altitude **stack**" had locked a model prematurely: a
> sealed vertical stack forbids a 4th by construction, with no admission procedure
> and no open/closed declaration. This revision replaces the stack with an **open,
> default-deny, gated coordinate space** that models its own evolution. The
> original research synthesis is preserved frozen at
> [development/unified-product-view/findings.md](development/unified-product-view/findings.md)
> (and the verbatim briefs at
> [research.md](development/unified-product-view/research.md)) as the audit record.

## One-Sentence Product

IDE Ergonomics is a **restraint-floored, governed routing layer** for AI work in
an IDE: when a conversation produces a definition, side note, handoff, route
choice, or delegation opportunity, it surfaces a small owner-safe card that helps
the user choose the right *governed* next step — without ever promoting,
executing, or switching routes on its own.

The product is still "the missing moment between noticing useful work and safely
sending that work to the right place" (PRODUCT-VIEW.md §One-Sentence Product).
What this document adds is the answer to *why the eleven-plus primitives are one
product* — and a model that can grow that answer without being rebuilt.

## The Organizing Model: an open coordinate space (not a stack)

Every conversation moment that the product acts on has, simultaneously, a value
on several independent **coordinates**. A primitive is a *point* in this space —
it carries one value per coordinate at once, not a position on a single ladder.
(The earlier "three altitudes of one spine" framing was a **vertical stack**; the
review showed the Primitive→Spine-Role table was already a coordinate grid drawn
as a sealed stack — so the honest shape is a coordinate space, and the set of
coordinates is **open**, not fixed at three.)

```text
  OPEN COORDINATE SPACE  —  a moment / primitive = one value on each axis
  (the set is OPEN at the ceiling, DEFAULT-DENY at the default, gated between)

   ── restraint  ───────●─────────  may it safely become? (the INVARIANT floor;
                                     every other coordinate sits on top of it)
   ── routing    ───●─────────────  where can it go, in what shape? (LATENT
      grammar                        dispatch vocabulary; no surface decision)
   ── work-arc   ───────────●─────  where in the task arc? (Discover→…→Execute;
      lifecycle                      the load-bearing DECISION coordinate)
   ── session    ──────●──────────  where in the moment's own clock? (detected→
      state                          parked→revisited; split out of "lifecycle")
   ── evidence   ──────────●──────  what is owed / shown? (ADMITTED — load-bearing:
      / receipt                      the receipt-debt keystone is denominated here)
   ── input-side ──●──────────────  how literally to take the user's span?
      (candidate)                    (pre-agent; gated — home: intent-latitude-tags/)
   ── social /   ─────────●───────  who is this for / who leads now?
      addressee                      (gated — home: teammate-handoff-memos/)
   ── + …        ─ ─ ─ ─ ─ ─ ─ ─ ─  a new coordinate may be PROPOSED, but is not
                                     live until it passes the admission gate
```

There is no top and no bottom (except the restraint floor, which is the one
invariant nothing may breach). New coordinates are **addable** — that is the
whole point of replacing the sealed box.

### The coordinates

**restraint floor — the invariant (federation-inherited).** *May this moment
safely become something?* candidate≠promotion, preview≠execution,
side-note≠route-switch, handoff≠execution-proof, recommendation≠execution. The
per-row boundaries are inherited from PRODUCT-VIEW.md:188-193; the model's *net*
addition is the graduated-trust dial + logged non-action. It is the floor every
other coordinate sits on. Home: [restraint-floor/](restraint-floor/README.md).

**routing grammar — the vocabulary (latent).** *Where can it go, in what shape?*
Every primitive is a projection of one Arcanum dispatch document. **Latent**: the
user never sees the grammar and never decides *because* of it — it earns its place
as internal coherence (the many owners are *one* vocabulary). Surfacing it as UI
is the "dashboard with no next action" fail. Home:
[dispatch-grammar-routing/](dispatch-grammar-routing/README.md).

**work-arc lifecycle — the load-bearing decision coordinate.** *Where in the arc
of the task?* The governed funnel Discover→Research→Decide→Define→Design/Plan→Execute.
This is **the only coordinate that does irreducible card-level decision work**: it
turns the federation's flat *peer* routes into a partially-ordered progression
carrying **receipt-debt** (see the Witness). Connective reads the whole space; a
single card is the one-point view. Home:
[lifecycle-progression/](lifecycle-progression/README.md).

**session-state — the moment's own clock (split out of "lifecycle").** *Where in
THIS moment's life — detected, carded, parked, revisited, resolved?* The review
found "lifecycle" was overloaded: the work-arc clock (a property of the domain
task) and the session-state clock (a property of the UI moment — `park`/revisit,
`Maintain`, logged non-action) are two different timers. They are now distinct
coordinates so neither silently carries the other.

**evidence / receipt — ADMITTED (load-bearing today).** *What is owed or shown?*
The model's keystone — **receipt-debt** — is denominated in evidence, yet the
work-arc coordinate returns *null* for it (four mapping rows say "cross-stage /
reads ALL stages / spans the funnel"). Because the keystone already runs on it,
evidence is **admitted now**, not queued (this resolves the one open owner-decision
toward *admit-now*; reversible by the owner). Home: the evidence-rail primitive
(ERGONOMICS-OPPORTUNITIES.md §"Evidence and receipt rail").

**input-side — CANDIDATE (gated).** *How literally should the agent take the
user's span?* All the coordinates above are **output-side** (they act on something
the agent already produced); this one is **pre-agent**. The model already flagged
intent-latitude as "resists grammar, by analogy only, not resolved" — that seam
*is* this coordinate. Candidate pending the admission gate. Home:
[intent-latitude-tags/](intent-latitude-tags/README.md).

**social / addressee — CANDIDATE (gated).** *Who is this for, and who leads now?*
A memo to a person and a memo to a future session sit at the *identical*
(restraint, grammar, work-arc) coordinate and differ only on **addressee** — which
the model currently collapses into one "handoff" row. Candidate pending the gate.
Home: [teammate-handoff-memos/](teammate-handoff-memos/README.md).

## Coordinate Admission & Evolution Lifecycle

This is the model modelling its own growth — the fix for "don't lock a model
before thinking about its own evolution lifecycle."

**Closure posture (explicit).** The coordinate set is **OPEN at the ceiling** (a
new coordinate may be *proposed*) and **DEFAULT-DENY at the default** (a proposed
coordinate is *not live* until it passes the admission gate); gated in between.
This adopts the in-repo precedent `CAV2-D49` *closed authority-kind enumeration /
default-deny* — an authority-bearing taxonomy must declare its closure stance with
a gate, not leave closure as an accident of a box drawing.

**Admission gate (the irreducibility test).** A candidate coordinate is admitted
only if it does decision work the existing coordinates **structurally cannot** —
i.e. it survives collapse to every existing coordinate and to every existing
primitive. (This is the same test the work-arc coordinate passed and that the
floor and grammar did *not* — they are demoted to inherited/latent.) The three
candidate coordinates above are the gate's **first admission test**: evidence
already cleared it (load-bearing); input-side and social are pending.

**Owner of the gate.** The gate is owned by the **`PRODUCT-VIEW.md` owner /
a governance review** — **not** the self-assembling-ergonomics loop. (The review
verified that loop is explicitly fenced from canonical mutation — "assembled +
green ≠ shipped", "never edits canonical capabilities" — so routing model-level
admission through it would be circular. The loop builds *primitives*; it cannot
admit *coordinates* to the model that governs it.)

**Promotion path for this document.** This model is `status: draft`. It promotes
to `accepted` when (a) the schema-unverified residue is discharged (the dispatch
grammar mapping is checked against `dispatch.schema.yml`) AND (b) the two candidate
coordinates (input-side, social) have each been run through the admission gate
(admitted or rejected on record). Owner gate: `PRODUCT-VIEW.md` owner.

## The Witness: "evidence rail" through both paths

The concrete proof the model is **not a re-skin** of the flat federation
(PRODUCT-VIEW.md §The Story, :38-51), and the demonstration of the work-arc
coordinate's load-bearing power.

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

**Through the model** — the **identical six routes** get work-arc-coordinate
values: side-node = *Discover*, "evidence rail" = *Define*, handoff =
*Design/Plan*, route-ambiguity = *Decide*, two-lane split = *Research*. That
induces a partial order and makes **receipt-debt** expressible:

> "Routing the **handoff** (Design/Plan) now skips the **Define** receipt the
> 'evidence rail' term still owes."

A statement the flat peer-menu **structurally cannot make**. The restraint
boundaries are identical in both paths (inherited, not new); the grammar is latent
in both (unseen). The single observable difference is the ordering + receipt-debt
— the work-arc coordinate's irreducible contribution, and the proof the model
subsumes rather than re-skins. *(One worked span — it establishes the coordinate
is real, not that every span produces a debt.)*

## Primitive → Coordinate Mapping

Every existing primitive, placed on the coordinates. The set is **open**: the
three rightmost coordinates (evidence, input-side, social) are the admitted /
candidate additions from the review; more may be proposed through the gate.

| Primitive | restraint (invariant) | routing grammar (latent) | work-arc lifecycle | session-state | evidence | input-side | social |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Transition card | candidate/preview only | dispatch `intent` block | one-point view | detected→carded | — | — | — |
| Side node | does not switch route | residue / side_note_queue | Discover | parked | — | — | — |
| Handoff (composer) | not execution proof | frame handoff | Design/Plan | — | receipt due | — | — |
| Teammate memo | no impersonation | frame handoff | Design/Plan | — | — | — | **addressee** |
| Route menu | bounded menu | route pattern / ChoiceCard | spans the funnel | — | — | — | — |
| Subagent preview | no spawn w/o approval | route pattern + gate | Research | — | receipts req | — | role tension |
| Knowledge refs | cite, not promote | capability ref + residue | Discover/Research | stale→refresh | source ref | — | — |
| Field-hover | read-only | resolver (read) | Discover/Research | — | — | **pre-read** | — |
| Intent-latitude | records, not executes | (input-side, by analogy) | — | — | — | **the axis** | — |
| Route ambiguity | records intent | capability reference | Decide | — | — | — | — |
| Definition candidate | no canonical promotion | operator phrase → owner | Define | — | — | — | — |
| Craft panel | one route question | capability ref + gate | Execute selection | — | receipt | — | — |
| Connective | recommendation ≠ execution | gate / pareto + tournament | reads ALL stages | — | expected receipt | indicators | collaboration mode |
| Self-assembling | green ≠ shipped | spell candidate + validation | Maintain (session-state) | meta-loop | frozen criterion | — | owner gate |
| Evidence rail | never silently mutated | observability / one dispatch_id | (returns null) | — | **the axis** | — | — |

Two primitives that the old 3-coordinate model could only footnote as "resists
grammar" now have a home: intent-latitude on the **input-side** coordinate,
teammate memo on the **social** coordinate. That is the open coordinate set doing
the work the sealed stack could not.

## MVP Shape

Unchanged from the owner (PRODUCT-VIEW.md:184-193): **one bounded
conversation-transition card = the one-point view of the coordinate space.** The
MVP does *not* build the full space, the Craft-state read, or Connective. First
falsifiable question stays small: *can a user choose the right governed route from
ONE conversation moment?*

Two restraint upgrades carried even at MVP: the **graduated-trust dial** (explicit
commands bypass the candidate stage so power users aren't taxed) and **logged
non-action** (park/ignore emits a workflow-evidence signal — and now sits cleanly
on the **session-state** coordinate).

## Owner-Boundary Preservation

The model **lifts owner boundaries to the surface; it does not relocate
ownership.** Every "grammar role" is a projection for display, never a transfer of
authority — the grammar can be shown precisely because the restraint floor
guarantees it cannot act.

- definitions → Definitions Governance;
- route shape → Dispatch Spec (the dispatch object *validates*, does not execute);
- side notes & handoffs → Necronomicon-style workflow memory (no self-promotion);
- execution → Task Session or another approved owner;
- reusable spells → Spellcraft; sigils → Sigil Development;
- **coordinate admission → the `PRODUCT-VIEW.md` owner / governance review** (the new gate).

## Demotions on Record (claim ≤ proof)

- The original **"three altitudes" stack** is superseded by the open coordinate
  space — the review showed "three" traced to *three explorer agents*, not to the
  structure, and the table was already a coordinate grid drawn as a sealed stack.
- Only the **work-arc lifecycle** coordinate does card-level decision work; the
  restraint floor is federation-inherited (net add = dial + logged non-action) and
  the grammar coordinate is latent (internal coherence only).
- **evidence/receipt** is admitted (load-bearing); **input-side** and **social**
  are *candidate* coordinates pending the admission gate — not yet load-bearing.
- field-hover and intent-latitude attach to the grammar **by analogy only**; under
  the open space they are placed on the input-side coordinate instead.
- The work-arc funnel is a **strong default path, not a hard control-flow graph** —
  explicitly bypassable.
- The grammar mapping was **not** checked against `dispatch.schema.yml`; this
  remains the residue gating draft→accepted promotion.
- Dropped under review (refuted): the "stack→coordinates is just a relabel"
  objection (the substance is the *open* set + the missing coordinates, not the
  word); routing coordinate admission through the self-assembling loop (circular).

## Source Trail

- [PRODUCT-VIEW.md](PRODUCT-VIEW.md) — owner of the product definition (this view extends it)
- [ERGONOMICS-OPPORTUNITIES.md](ERGONOMICS-OPPORTUNITIES.md) — the 12-pattern federation
- Coordinate homes: [restraint-floor/](restraint-floor/README.md), [dispatch-grammar-routing/](dispatch-grammar-routing/README.md), [lifecycle-progression/](lifecycle-progression/README.md), [intent-latitude-tags/](intent-latitude-tags/README.md), [teammate-handoff-memos/](teammate-handoff-memos/README.md)
- [development/unified-product-view/findings.md](development/unified-product-view/findings.md) — frozen research synthesis (pre-revision)
- [development/unified-product-view/research.md](development/unified-product-view/research.md) — three explorer briefs, verbatim
- Dispatch ledger: `telemetry/agents/subagents-dispatch.yaml` → `2026-06-24-unified-ide-ergonomics-product-view` (build) and `2026-06-24-spine-model-premature-lock-review` (this revision)
