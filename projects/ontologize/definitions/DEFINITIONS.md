# Ontologize — Canonical Definitions

Maintained under the `definitions-governance` discipline. This surface holds the
**project-canonical** definitions for ontologize — the load-bearing terms that anchor
every other artifact. It sits *above* the layered, client-facing terms in the project-root
[DEFINITIONS.md](../DEFINITIONS.md) and [GLOSSARY.md](../GLOSSARY.md): those describe the
four product layers; this file fixes what the words **ontology** and **ontology node**
mean for the project itself.

**Status vocabulary.** Each term is **candidate** (proposed canonical, awaiting owner
review), **seed** (clear, unproven outside GoldenQuill), or **source-backed** (proven in
GoldenQuill). Nothing here is promoted to canonical Arcanum or CyberAlchemy vocabulary
without an explicit owner-review route — see [DEFINITION-DRIFT-AUDIT.md](DEFINITION-DRIFT-AUDIT.md).

Lookup layer: [DEFINITIONS-INDEX.md](DEFINITIONS-INDEX.md).

---

## DEF-ONT-001 · Ontology — _candidate (canonical)_

**One-line.** An **ontology** (in the ontologize sense) is an *explicit, governed model of
what a company knows* — its subjects and the mechanisms by which it creates value —
**together with the evidence and decisions that make each piece of that knowledge
trustworthy enough to act on.**

**Plain-language intuition (non-normative).** It is not a dictionary of terms and not a flat
taxonomy. It is the company's knowledge written down in a way a machine and a person can both
trust: every claim says which branch of reality it belongs to, how confident we are, what
evidence backs it, and who approved it for reuse. The difference between "we have a data
model" and "we have an ontology" in this sense is governance — the model carries its own proof
and its own decision trail.

**Structural definition (normative).** An ontologize ontology is the composite of five
commitments. A body of knowledge is an ontology *in this sense* only when all five hold:

1. **Branched, not flat.** Knowledge is split into the four ontology branches —
   **B1 meaning**, **B2 system**, **B3 run-context**, **B4 bridge** — so intended meaning is
   kept separate from actual behavior and the two are connected (never smoothed) by bridge
   edges. _[source-backed — `ontology-vault` branch-aware model; see
   [ONTOLOGY-BRANCHES.md](../ONTOLOGY-BRANCHES.md)]_
2. **Typed nodes.** Every assertion is an instance of one of the six **ontology node types**
   (N1–N6); the node type set is the vocabulary of what can be said. _[source-backed —
   GoldenQuill `validate.py` 5 node types + adapted N6; see DEF-ONT-002]_
3. **Edge-governed.** Every relation between nodes obeys a single **edge catalog**
   (source-type → target-type, cardinality, named inverse, category, per-edge acyclicity) —
   relations are a typed contract, not a free graph. _[seed — see
   [DAG-AND-METRICS.md §3](../DAG-AND-METRICS.md)]_
4. **Two orthogonal DAGs.** An immutable **execution DAG** (the audit spine: what happened, in
   order) is kept orthogonal to the **ontology DAG** (what it means / what becomes reusable);
   the ontology graph references the execution record but never rewrites it. _[source-backed —
   promotion-record architecture]_
5. **Promotion-governed.** Knowledge gains reuse authority only through the loop
   evidence → candidate → owner decision → projection, with each evidence-bearing node carrying
   a confidence grade (`veracidade`) and `evidence_refs`. Nothing auto-promotes. _[source-backed
   — eight promotion primitives + 11 L0 gates]_

**Operational interpretation.** A company "has an ontology" in the ontologize sense when its
knowledge is **(a) branched, (b) typed, (c) edge-governed, (d) evidence-graded, and
(e) promotion-gated** — not merely catalogued. The consulting engagement's job is to install
these five properties over the client's existing data and agents.

**Boundary with neighbors.**
- vs **Ontology [generic]** (project GLOSSARY): the generic entry — "an explicit, governed
  model of a company's concepts: subjects and mechanisms" — is the *client-facing* gloss. The
  canonical sense is **strictly stronger**: it additionally requires branch separation, typed
  nodes, a governed edge catalog, and promotion governance. The generic entry is the elevator
  pitch; DEF-ONT-001 is the contract.
- vs **Operational Ontology** (Arcanum/CyberAlchemy): that is knowledge about *agent operation*
  (routes, sigils, prompts) — a different concept. The B3 branch here is **run-context**, a
  per-run denominator context, deliberately renamed to avoid this collision
  ([RECONCILIATION.md](../RECONCILIATION.md) §1).
- vs **Ontology DAG**: the Ontology DAG is one of the five commitments (#4), not the whole
  ontology; an ontology is branches + nodes + edges + two-DAG split + promotion governance.

**Contradiction path (how this could be wrong).** If a client engagement delivers durable BI
value with only some of the five commitments (e.g. typed + evidence-graded but un-branched),
the "all five are necessary" claim is falsified and the definition weakens to a *graded* model
(a node is an ontology node to the degree it satisfies the five). Validate in the pilot.

---

## DEF-ONT-002 · Ontology node — _candidate (canonical)_

**Definition.** An **ontology node** is a *single typed assertion* in the ontology: one
instance of exactly one of the six ontology node types, carrying a stable identity, a branch
assignment, and — for the three evidence-bearing types — a confidence grade and its evidence.
It is the atomic unit the edge catalog connects and the promotion loop governs.

**The six node types (N1–N6).** _[source-backed — GoldenQuill `validate.py`; N6 adapted]_

| #  | Node type             | Branch (primary) | Role                                                          | Evidence-bearing? |
|----|-----------------------|------------------|--------------------------------------------------------------|-------------------|
| N1 | **OutcomeEvent**      | B2 system        | a source-backed real-world event (must carry `source`)       | no¹               |
| N2 | **LifecycleState**    | B3 run-context   | projection of the deepest verified stage (stage ≠ outcome)   | no                |
| N3 | **MetricObservation** | B3 run-context   | a read-model metric with denominator semantics               | **yes**           |
| N4 | **PromotionCandidate**| B4 bridge        | a proposed reusable lesson/relation, not yet authoritative   | **yes**           |
| N5 | **OwnerDecision**     | B4 bridge        | explicit approve / reject / retire / contradict              | no²               |
| N6 | **KnowledgeProjection**| B1 meaning      | a promoted lesson written into the governed store            | **yes**           |

¹ N1's honesty is its mandatory `source` (sourced or rejected), not a `veracidade` grade.
² N5's commitment is materialized by `approved_allowed_uses`, not a scalar grade.

**Evidence-bearing node fields.** The three evidence-bearing types (N3, N4, N6) carry:
- **`veracidade`** ∈ {high, medium, low} — how much external evidence confirms the node's
  claim. `high` = tested against reality; `medium` = derived from established principle, not yet
  tested in this client's system; `low` = untested projection.
- **`evidence_refs`** — source/event/test locators justifying `veracidade`. **Must be non-empty
  for `high`.** _[adapt — `veracidade` axis borrowed from `domainspec/vault`; single axis,
  convicção dropped by orthogonality heuristic — see [DAG-AND-METRICS.md §2b](../DAG-AND-METRICS.md)]_

**Schema.** The machine-checkable shape of an ontology node is
[schemas/ontology-node.schema.json](../schemas/ontology-node.schema.json) (DEF-ONT-002 is its
prose authority). The schema encodes the per-type required fields and the honesty gates
(`source` on N1; `veracidade` + `evidence_refs` on N3/N4/N6; `denominator` on N3;
`contradiction_path` on N4; `record_kind = promotion_record` on N6).

**Boundary.** An *ontology node* is a knowledge assertion (this definition). It is **not** an
edge (edges are governed separately by the catalog) and **not** a card (a card is a B1-meaning
configuration primitive, not a graph node). A node *type* (N1) is the class; an *ontology node*
is an instance.

---

## DEF-ONT-003 · Ontology branch — _source-backed_

**Definition.** An **ontology branch** is one of four independently governed facets of the
ontology — **B1 meaning**, **B2 system**, **B3 run-context**, **B4 bridge** — connected only by
B4 bridge edges. Branching is what lets the system tell *intended meaning* (B1) apart from
*actual behavior* (B2/B3) and detect **drift** between them instead of smoothing them into one
blurry truth. Full mapping: [ONTOLOGY-BRANCHES.md](../ONTOLOGY-BRANCHES.md). _[source-backed —
`ontology-vault` branch-aware model]_

---

## DEF-ONT-004 · Governed edge / edge catalog — _seed_

**Definition.** A **governed edge** is a typed relation between two ontology nodes whose
legality is fixed by the **edge catalog**: a single table giving each edge its allowed
source-type → target-type pairing, cardinality, named inverse, category
(execution / promotion / structural / control), and whether it must be acyclic. The catalog —
not the author — decides which relations may exist, which makes the graph auditable and the
deterministic gates testable. Catalog: [DAG-AND-METRICS.md §3](../DAG-AND-METRICS.md). _[seed —
generalized from GoldenQuill's edge set; cardinality/inverse columns are an adaptation]_

> **`contradicts` vs `drifts_from`** is load-bearing and lives in the catalog: `drifts_from`
> (MO/OE → KP) is the raw, neutral divergence signal preserving both sides; `contradicts`
> (PC ↔ PC/KP) is the adjudicated conflict that **blocks promotion** until an `OwnerDecision`
> resolves it.
