# DomainSpec v2 — Authority Definitions (governance vocabulary)

> Canonical **governance-level** definitions for DomainSpec v2. ID scheme: `DSV2-D*`.
> These are the terms the credibility/governance **constitution rules cite** — distinct from the
> **spec-level** domain vocabulary (`impl/spec/DEFINITIONS.md`, `DS-D*` — meta-types/edge-verbs, pending
> reformulation R7). This surface **references** cav2 IDs (`CAV2-D*`) and **never redefines** them.
> Lookup: [DEFINITIONS-INDEX.md](DEFINITIONS-INDEX.md). Promoted 2026-07-01 from Craft candidates
> `DEF-DSV2-*` (`../../.craft/ledger.yml`).

Each definition carries three voices: **formal** (normative), **plain** (non-normative intuition),
**domain-context** (non-normative, how it's used in v2's current surface).

---

## DSV2-D1: Edge-Law Admissibility

Status: active · Term: edge-law admissibility · Aliases: edge-type admissibility, composes-differently test

**Formal.** An edge type is admissible in the DomainSpec `RELATIONSHIPS` edge-law **iff it contributes a
distinction not silently redundant with an existing axis** — where the axes are `concept-type`,
`relation-kind`, `composition-shape`, and `feature-boundary`. Operationally: **an edge earns its own type
iff it composes into different code.** A distinction that does not is folded into the node type or an
explicit typed coupling flag. This is a domain specialization of **CAV2-D22** (orthogonal classification)
and **CAV2-D29** (axis orthogonality); non-orthogonal couplings are typed per **CAV2-D16**. Corollary:
**widening an edge's *source* endpoint (same target, same semantics) is a clean generalization; changing
its *target* type is an overload — reject.** Scope: governance/classification orthogonality only — **not**
Lean/Hilbert projector orthogonality (excluded from cav2 authority).

**Plain.** An edge only deserves its own name if it actually makes the code compose differently. If it
doesn't, widen an existing edge or add a flag — don't invent a new one. Widening *who* can use an edge is
fine; changing *what it points at* is not.

**Domain-context.** Governs **R3** (RELATIONSHIPS reformulation). Concrete rulings: keep `enforces` ≠
`applies` (guard vs select); collapse `enforces`/`enforces-cross` (same code + cross flag); reject
`queries` for `Calc→Policy` (target change); widen `applies : Policy → {Operation, Calculation}` and
`queries : Behavioral → Entity` (source widen). See `DEC-DSV2-EDGE-ADMISSIBILITY`.

---

## DSV2-D2: Executable Typed Graph

Status: active · Term: executable typed graph · Aliases: spec-as-graph, node/edge/realization decomposition

**Formal.** The DomainSpec v2 spec surface understood as **one typed graph**: **nodes** (`TAXONOMY`
meta-types, each mapping to exactly one code pattern) + **typed edges** (`RELATIONSHIPS` edge-law) +
**composability** (how the connected node-patterns must reference each other in code). Governed on three
axes: **layering** (which nodes exist + may connect), **validation** (spec → derived obligations), **drift**
(code↔spec alignment over time). Two enforcement arms ride the graph: the derivation **engine**
(validation) and the **code-tag composability** checker (drift).

**Plain.** The spec is a typed graph you can build code from: the *things* (nodes), *how they connect*
(edges), and *how each connection turns into code* (composability).

**Domain-context.** The thesis of the composability/edges/taxonomy synthesis
(`../../research/2026-07-01-composability-edges-taxonomy-synthesis.md`) and the substrate the
spec-ontology toy tested (verdict: SURVIVED-narrow).

---

## DSV2-D3: Two-Plane Boundary

Status: active · Term: two-plane boundary · Aliases: authoring-vs-contract plane, ontology-lens boundary

**Formal.** A boundary separating two planes of the spec: **ontology framing governs the AUTHORING
plane** (writing/editing/organizing the spec — where confidence, premises, and ontology tooling are
legitimate) while **deterministic derivation governs the CONTRACT plane** (the crisp, total,
engine-facing spec). **Authority flows contract → authoring, never the reverse**: authoring-plane metadata
is non-authoritative over the crisp docs until an owner route ratifies a consumer.

**Plain.** Use ontology tooling while you *write* the spec, but the strict engine-facing spec stays the
source of truth — help flows one way only.

**Domain-context.** The resolution of the spec-as-ontology research
(`../../research/2026-07-01-spec-as-ontology/findings.md`); the interim stance while `DEC-DSV2-LANE-ZA`
(fuse vs generate) is deferred to an agent-cost experiment.

---

## References (owned, not redefined)
- **CAV2-D22** orthogonal classification · **CAV2-D29** axis orthogonality invariant · **CAV2-D16** typed
  coupling invariant — `[repo-root]/cyberAlchemy-v2/authority/definitions/DEFINITIONS.md`.
- Spec-level vocabulary (`DS-D1` meta-types, `DS-D2` edge verbs) lives in `impl/spec/DEFINITIONS.md`
  (**pending — reformulation R7**), not here.
