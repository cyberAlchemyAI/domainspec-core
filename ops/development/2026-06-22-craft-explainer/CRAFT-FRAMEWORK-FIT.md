# Craft in the Bigger Framework Model

Research synthesis: where Craft fits in the framework-unification two-axis model
(pipeline × three mechanisms). Each insight is tagged **[public-safe]** (a general
method idea, safe to state at a conceptual level on a public page) or
**[private-keep-internal]** (a private project name, file content, or internal
decision that must NOT be copied onto a public page).

> Sourcing note. The two-axis model and quotes come from the **private**
> `projects/framework-unification/` workspace; the usage example comes from the
> **private** `cyberAlchemy-v2/` project. Craft's own self-description
> (`arcanum/arcana/craft/`) is public Arcanum. Treat the *connections drawn here*
> as enrichment; only re-publish the **[public-safe]** rows.

---

## 1. Craft as the operational home of RESIDUE + recursive self-application

The framework-unification model names two mechanisms that Craft happens to be a
concrete, shipping instance of. The connection is exact, not loose analogy.

### 1a. RESIDUE — "what isn't yet in the schema, tracked as open questions"

The model makes residue a **first-class mechanism**, not an afterthought. From
`CONCEPT-MAP.md` Axis 2, the epistemology mechanism guarantees on every node:

> "**residue** (what wasn't preserved) + the **claim ≤ proof** gate
> (`pass/flag/block`) that stops drift"

and in the node envelope:

> `residue: [{ claim, status: open|closed, ref }]  # epistemology (= your "open questions")`

`SCOPE.md` §3 fixes the *operational* form of residue — the useful, non-mechanical
version available now:

> "The **operational residue accounting** for this workspace ... is a
> **well-defined Open Questions section in every informational object** ... It is
> honest bookkeeping + a human-gated orientation aid — the *useful* residue ledger
> for now. It is **not** a mechanical gate."

Craft IS that operational residue ledger, made structured. Craft's own
`README.md` lists its durable state as "blockers, enablers, decisions, **gaps**,
definitions, next moves" — and `gaps` are defined in `ARCHITECTURE.md` as
"Missing, deferred, weak, or unresolved areas that **remain visible**." A Craft
`gap` row (severity `flag`, treatment `plan`, owner_route) is the residue object
of CONCEPT-MAP made into a typed, linked, indexed row instead of prose. Craft also
carries the same `pass/flag/block` gate vocabulary per context (its `gate` field
and `validate` verdict), which is the claim≤proof gate at the ledger altitude.

- **[public-safe]** Residue (open gaps/questions a transformation did not resolve)
  is a first-class object worth tracking as structured, linked rows — not prose
  buried in docs. A local ledger of gaps/blockers/decisions IS a residue ledger.
- **[public-safe]** A `pass / flag / block` gate per work-unit is the practical,
  human-gated form of "claim ≤ proof" before a mechanical type exists.
- **[private-keep-internal]** The node-envelope YAML, the "claim ≤ proof / Lean
  typed-residue" framing, invariants I1–I10, and the SCOPE §1 novelty-vs-utility
  division of labor are private framework-unification specifics.

### 1b. Recursive self-application — "every stage is the same process at a different altitude"

`CONCEPT-MAP.md` invariant **I9**:

> "**Recursive self-application** — every stage is the same process at a different
> altitude; the pipe runs on itself."

Craft is a direct instance of this. Craft is defined (`ARCHITECTURE.md` Scope) as
"a sigil for **project-local recursive ledgers** ... durable state for **nested
development contexts**." Its `contexts` row family holds "**Recursive
project-like units**"; `open_child_context` spawns a sub-context with its own
blockers/decisions/gaps, and `recompose` requires evidence that the child folds
back into the parent before closure (a Decision-Flow rule: "Child context closure
requires recomposition evidence"). That open-child → work → recompose loop is the
same process at a lower altitude — I9 implemented as a storage contract.

- **[public-safe]** A development ledger should be **recursive**: any context can
  open a child context with its own blockers/decisions/gaps, and a child must
  **recompose** (prove it fits the parent) before it can close. Same method, every
  altitude. This prevents nested work from silently vanishing.
- **[private-keep-internal]** The invariant numbering (I9), the "pipe runs on
  itself" phrasing, and the TUNING-LOOP signal taxonomy are private.

---

## 2. How Craft relates to the pipeline / node envelope / claim≤proof gate

- **Pipeline (Axis 1).** The model's pipeline is `define → research → findings →
  discovery → plan → spec → stories → tests → implement → verify → emit-signals`.
  Craft is **not a stage** in that pipeline — it is the cross-cutting *memory and
  coordination surface* that runs alongside it. A Craft context records what stage
  a unit is at (cyberAlchemy-v2 contexts carry `Stage: define | plan | execute |
  validate`) and routes to the owning capability, but Craft does not author the
  stage artifact. Its `interaction-boundary` is explicit: "Craft records route
  memory and local ledger state; it does not rewrite native results."
  **[public-safe]** A ledger that tracks which lifecycle stage each work-unit is at
  — without owning the stage's output — is the orientation layer over a pipeline.

- **Node envelope.** The envelope is `identity + intent + connections + body +
  residue + epistemic`. Craft rows mirror the envelope minus `body`: stable
  `*_id` (identity), purpose/description (intent), typed `relations`/`links`
  (connections), `gaps`/`decisions` (residue), and `gate` pass/flag/block
  (epistemic). Craft is the envelope applied to *coordination state* rather than to
  pipeline content. **[private-keep-internal]** The exact envelope schema is private.

- **Claim ≤ proof gate.** Craft enforces a behavioral analogue: raw blockers
  "cannot be resolved directly" (must be refined with closure criteria first);
  role fields are "advisory until backed by an owner policy, decision, route
  contract, receipt, or explicit human evidence"; route-shape evidence is
  distinguished from execution evidence. **[public-safe]** Don't let a claim
  ("this is resolved", "this role is assigned") exceed its evidence — require a
  refinement/closure-condition before a blocker can close, and separate
  "validated the shape" from "ran it."

---

## 3. How cyberAlchemy-v2 actually uses Craft (concrete usage)

cyberAlchemy-v2 is a **private** consolidation project. It uses Craft as its
single live coordination ledger (`.craft/ledger.yml`, 36 KB, source of truth;
`CRAFT.md` the linked human view; `.craft/index.json` derived). Concrete pattern:

- **One ledger, eight sibling contexts** (`CTX-CAV2-ROOT`, `-SPACES`,
  `-DEF-TOWERS`, `-AUTHORITY-IMPORTS`, `-CONSTITUTION-TOWERS`, `-CRAFT-SURFACE`,
  `-BOUNDARY`, `-EXECUTION`), each with its own `Stage` and `gate: flag`.
- **Decisions tracked with blocking state** — e.g. visible-spaces and
  public/private boundary decisions are `active, blocking`; a definition-
  localization decision is `closed`. Each blocker links to its decision and names a
  lane (`governance` / `architecture`) and role (`definitions_governance`,
  `decision_gate`) with `human_required: true`.
- **Gaps as the residue surface** — term-clustering, duplicate-detection,
  constitution-clustering, local-representation gaps sit `active` with owner routes
  to other skills (`definitions-governance`, `constitution-governance`,
  `invoke plan then task-session`).
- **A "Pending By Node" table** — exactly the all-status/pending-by-node contract
  Craft's SKILL mandates, so the human can see what each context still owes.
- **One context literally named `Craft Execution Surface`**, whose purpose is "make
  Craft the local executable ledger for definition towers, blockers, decisions,
  gaps, next moves, and later recomposition" — i.e. the project self-consciously
  adopts Craft as its execution spine while heavier capabilities author artifacts.
- **A Boundary Check footer** asserting no public/canonical surfaces were mutated —
  Craft used as the safe private staging surface before extraction.

- **[private-keep-internal]** All context IDs, decision IDs, the public/private and
  visible-spaces decisions, the term/definition counts (149 candidates, etc.), and
  the project's intent to become a standalone repo are private specifics — do NOT
  copy these onto a public page.
- **[public-safe]** The *shape* of usage is publishable: one ledger, several
  sibling contexts each at a stage, decisions with blocking flags, gaps as residue
  with owner-routes, a pending-by-node status table, and a boundary-check footer.

---

## 4. Strongest one-paragraph "why Craft matters in the system"

> The framework model says every meaningful unit of work carries three things that
> usually get lost: where it came from (provenance), whether its claims are backed
> by evidence (a pass/flag/block gate), and what it did NOT resolve (residue) — and
> that the lifecycle is recursive, the same method re-applied at every altitude.
> Craft is the small, shipping, human-readable instrument that makes those
> properties *durable across sessions* for real project state. It is the
> operational home of residue (gaps, blockers, and open decisions as typed, linked,
> indexed rows instead of forgotten prose) and of recursive self-application (child
> contexts that must recompose into their parent before closing). It coordinates
> rather than executes — recording which stage each unit is at and routing to the
> capability that owns the output, while never overwriting that capability's
> verdict. In one line: Craft is the framework's memory and gate-keeping ledger —
> the place the system remembers what is still open, why it is open, and what must
> be proven before it can close. **[public-safe]** (stated without any private
> project name or internal decision).

---

## Public-safe vs private — quick reference

| Insight | Tag |
|---|---|
| Residue = structured, linked gap/blocker/decision rows, not prose | public-safe |
| pass/flag/block as the human-gated form of claim ≤ proof | public-safe |
| Recursive ledger: child contexts must recompose before closing | public-safe |
| Ledger coordinates lifecycle stages without owning their artifacts | public-safe |
| Don't let a claim exceed its evidence (refine blockers before closing) | public-safe |
| Usage shape: sibling contexts, blocking decisions, gaps-as-residue, pending-by-node, boundary footer | public-safe |
| The node-envelope YAML schema, invariants I1–I10, claim≤proof/Lean typed-residue | private-keep-internal |
| The novelty(Lean)-vs-utility(operational) division of labor (SCOPE §1) | private-keep-internal |
| All cyberAlchemy-v2 names, IDs, decisions, counts, extraction intent | private-keep-internal |
| framework-unification internal pipeline order, TUNING-LOOP signal taxonomy | private-keep-internal |
