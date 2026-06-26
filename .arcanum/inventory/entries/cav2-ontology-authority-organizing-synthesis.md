---
tags: [inventory, cav2, ontology, authority, instantiation, build-from-owned, non-collapse, context-invariant, epistemic-strength, synthesis]
node_type: synthesis
is_session: true
layer: governance, architecture
nature: explanatory, reference, decision-record
status: candidate
created: 2026-06-26
boundary: INTERNAL — references the moat-adjacent engine framing (functor/residue, upward authority promotion) + private cav2 spine; do NOT copy into public arcanum/
sources:
  - cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d23-authority-lifecycle-axis
  - cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d43-pattern-promotion-lifecycle
  - cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d48-authority-promotion-lifecycle
  - cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md
  - cyberAlchemy-v2/ontology/promotion-requests/2026-06-23-authority-object-schema-proposal.md
  - cyberAlchemy-v2/disciplines/development/2026-06-26-build-from-owned-validator-HANDOFF.md
---

# CAV2 Ontology↔Authority Organizing — Session Synthesis (2026-06-26)

Candidate Inventory synthesis (session filing; **promotes nothing**; owners = cav2
definitions-governance / ontology route / decision-gate). Captures the framings and
decisions from the 2026-06-26 thread so the work can resume. Claim ≤ proof: most items
below are **proposed/candidate**, not enacted — the enacted facts are flagged.

## The engine (the throughline)
The purpose — *"a system that builds systems"* — cashes out as: **child/domain contexts
produce authority; whatever proves it holds *beyond its origin domain* is promoted UP to
CAV2 (the apex); the apex accretes what survives.** "Use domain authority to get the broadly-
valid authority." The property we kept trying to name ("generic") is best called
**context-invariant** — what *survives projection across contexts* = the residue/invariant
(`CAV2-D18`/`D29`). (User later leaned toward framing it via the **epistemic-strength ladder**
instead — see Open Questions.)

## Build-from-owned finding: the mechanism is already mostly owned
Do **not** define this net-new. The sweep found the owners:
- **`CAV2-D23` Authority Lifecycle Axis** — the epistemic-strength dimension itself
  (maturity / evidence-confidence / commitment; hypothesis→axiom). Rule: *"no one axis may
  silently stand in for another."* This is the "hypothesis → axiom" definition.
- **`CAV2-D43` Pattern Promotion Lifecycle** — the cross-context promotion path:
  `hypothesis → domain exercise → evidence → generalized abstraction → cross-context exercise
  → owner promotion → authority → invariant/constitution pressure`. Nearly verbatim the engine.
- **`CAV2-D48` Authority Promotion Lifecycle** — the **generalization** of D43/D46/Discipline-
  Growth-Rule to *all* authority kinds. Its own provenance line is a textbook **build-from-owned**
  case ("the shape is visible across owned sources but the unifying object is named in none").

**The genuine gap:** `D48` is **context-blind** — it has the staged path but NOT the
**cross-context, child→apex direction** nor the **qualifying gate** ("holds beyond its origin
domain"). → **build FROM D48** (add a context dimension + the gate), not a parallel lifecycle.

## Build-from-owned is the DUAL of the non-collapse test
- **Non-collapse:** given two declared objects, prove they're *distinct* (`∃ axis. A≠B`). Catches over-splitting.
- **Build-from-owned:** given one candidate, search the corpus for an owner it *coincides-with / specializes* (`¬∃ separating axis`). Catches redundant net-new.
- Same SMT coincidence core, inverted polarity → **3 siblings share one adapter**: non-collapse,
  closure (`CAV2-D49`), build-from-owned. All **OQ-1 / schema-`G2`-gated.**
- **Trigger = a real process failure this session:** we proposed net-new (`context-invariant
  authority`) *before* sweeping for the owner (D43/D48). Precedent-sweep was a habit, not a gate.

## Two orthogonal axes — do NOT collapse into "context is everything"
Per `CAV2-D29`, keep two coupled-but-orthogonal axes (`CAV2-D16`):
1. **epistemic strength** (`CAV2-D23`) — hypothesis→axiom, *within* a context;
2. **context-scope** — domain-local → context-invariant → apex, *across* contexts (the new dimension on D48).

An **apex axiom = maximal on both.** Counterexample proving orthogonality: a rule can be
axiom-strong yet domain-narrow ("test the artifact that exists"), or weak yet broad. The
rigorous form of "context controls everything" = **authority as a functor over the context
category** (the `FunctorialResidueStructure` connection); context-invariant authority = the
**residue/limit** surviving projection. But that's context-as-*base*, **not** a merge of the two axes.

## Organizing the corpus = the instantiation relation (not flat schema-vs-data)
It is an instantiation **chain**, not a binary: `D48` (meta) → `D43`/`D46`/promotion-policy
(specialize it, yet are themselves schemas) → records (leaf data). **Three orthogonal axes per
definition** — never merge them:
- **kind** — `instantiates: concept.<kind>` (e.g. `concept.definition`); owned by schema-proposal **G2**.
- **meta/instance** — `specializes: <id>` (e.g. `D43 specializes D48`); **the GAP** — today only inline in D48's `instances = {…}`. Same edge the build-from-owned gate needs.
- **tower/subject** — which pillar; owned by `DEFINITION-TOWERS.md`.

## Ontology vs Authority (the two-level split)
- **Ontology** (`cyberAlchemy-v2/ontology/`) = the **structural model / type-system** of authority
  objects: `AUTHORITY-KINDS`, `NODE-MODEL`, `RELATION-MODEL`, `LIFECYCLE-MODEL`, `AUTHORITY-POSTURES`.
  It **classifies + routes; it does NOT make canonical or decide** (per AUTHORITY-KINDS). The *map*.
- **Authority** (`cyberAlchemy-v2/authority/`) = the **actual authority + governance**: definitions
  (D1–D50), constitutions, decisions, `promotion-policy`, `AUTHORITY-MODEL`. Where authority is
  **promoted and counts**. The *territory*.
- **Bridge (concrete):** AUTHORITY-KINDS' `owner_route` + `authority_surface` columns point each
  ontology kind → its authority surface (`kind.definition → authority/definitions/DEFINITIONS.md`).
- A relation like `specializes` needs **both levels**: ontology owns the **edge shape**; authority
  owns its **meaning**.

## Decisions (status-flagged)
| # | Decision | Status |
|---|---|---|
| D1 | **CAV2 = apex context**; import-up / reference-down (CAV2 imports from nothing above; lower contexts reference up) | agreed (not yet a discipline) |
| D2 | Promoted property name candidate = **context-invariant authority** (residue/invariant) | candidate; user prefers epistemic-strength-ladder framing |
| D3 | Mechanism is **build-from-owned** of D23 + D43 + D48; D48 needs a context-dimension extension, not a new lifecycle | agreed |
| D4 | **Build-from-owned gate = dual of non-collapse**; 3 siblings, 1 SMT adapter; OQ-1-gated | **handoff committed `3359af7a`** |
| D5 | **Two orthogonal axes** (strength × context-scope), both fibered over context; don't merge | agreed |
| D6 | Organizing = **instantiation chain**; 3 orthogonal axes (kind / meta-instance / tower) | agreed |
| D7 | `specializes` needs an **ontology** home (edge shape) **and** an **authority** home (meaning) | agreed |
| D8 | `specializes` meaning = **reference/derive, NOT inherit** (each instance earns its own posture; else authority-laundering) | **proposed — pending lock** |
| D9 | Pilot = **D48-cluster instantiation map** as two cross-linked candidate outputs (ontology edge + authority lineage rule) | designed, **not built** |

## Open questions / residue
- **R1** Lock D8 (reference/derive vs inherit) — authority-level decision (decision-gate?).
- **R2** Before building the pilot, **check `RELATION-MODEL.md`** for an existing `instantiates`/`specializes` edge (build-from-owned applied to the edge itself) — **the immediate next action.**
- **R3** Does "context controls everything" (functor frame) hold, or break `D29`? → keep 2-axis unless proven otherwise.
- **R4** Define the **context-scope axis** + the gate property (term: context-invariant) — definitions-governance, build-from D48.
- **R5** Carry-over (pre-session): `ledger` promotion HELD (4/5 review conditions); validating constitution rule for `tracking` pending; the 3 SMT validators OQ-1/`G2`-gated.

## Boundary
Inventory candidate read-model. Promotes nothing. Owners: ontology route (RELATION-MODEL /
schema proposal), authority (AUTHORITY-MODEL / definitions-governance), decision-gate (D8/R1).
INTERNAL — moat-adjacent; do not copy into public `arcanum/`.
