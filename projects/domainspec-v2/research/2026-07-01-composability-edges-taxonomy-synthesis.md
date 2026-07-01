---
node_type: synthesis
is_session: false
status: candidate
created: 2026-07-01
authored_by: inventory (query/synthesis)
scope: DomainSpec v2 — composability, edges, taxonomy (how the three form one executable typed graph)
sources:
  - projects/domainspec-v2/impl/spec/TAXONOMY.md
  - projects/domainspec-v2/impl/spec/RELATIONSHIPS.md
  - projects/domainspec-v2/impl/governance/tags/CODE-TAG-COMPOSABILITY-PATTERNS.md
  - projects/domainspec-v2/impl/governance/tags/tools/check-code-tag-composability.ts
  - projects/domainspec-v2/authority/AUTHORITY-MODEL.md
  - projects/domainspec-v2/authority/constitutions/domainspec-v2-CONSTITUTION.md
  - projects/domainspec-v2/research/spec-ontology-unification/toy/{graph,mapping,catalog,run,verdict}.md
  - projects/domainspec-v2/research/2026-07-01-spec-as-ontology/findings.md
prior_art:
  - .arcanum/inventory/entries/evidence-cards/2026-06-21-authority-node-relationship-taxonomy-cards.md
  - .arcanum/inventory/entries/evidence-cards/2026-06-21-schema-taxonomy-view-primitives-cards.md
  - .arcanum/inventory/entries/evidence-cards/2026-06-21-category-theory-domainspec-language-cards.md
authority: Inventory synthesis (read model). Claims cite sources or are marked inference. No spec/schema/ontology promotion.
---

# Synthesis — Composability, Edges, Taxonomy in DomainSpec v2

## Thesis

The three are **one object at three levels**: DomainSpec v2's spec is an **executable typed graph** —
**taxonomy = the node alphabet**, **edges = which nodes may connect (the law)**, **composability = how
the connected node-patterns must reference each other in code (the realization)**. Taxonomy says *what
exists*, edges say *what may relate*, composability says *how the relation is realized and checked*.

## 1. Taxonomy — the node alphabet (25 types)

`TAXONOMY.md`: **25 meta-concept types** (14 backend — Entity, Value Object, Enum, Operation, Query,
Calculation, Rule, Policy, Workflow, Saga, Interface, Event, Mapping, State Machine; 11 UI). Every concept
maps to **exactly one** type (single-owner invariant). Each type carries: a **layer** (the "Architecture
Mapping Appendix" Layer Dependency Rule — Domain⊳Application⊳Interface/Infra) and **one code pattern**
(e.g. Rule→pure predicate, Operation→use-case factory, State Machine→transition table).
**Owner: layering governance** (`AUTHORITY-MODEL.md`).

- Catalog check (toy T2b): **25/25 types have exactly one pattern** (24 atomic; Event is a composite —
  payload+publisher across 2 layers).
- Practice check (toy T1/T3 on financial-settlement): **100% closure** — every concept classified; the one
  wrinkle (an undeclared `transaction` entity the feature creates) is a *spec-completeness* gap (C10), not
  a taxonomy gap. Prior art frames this same "confidence/status axes must not collapse" discipline
  ([authority-node-relationship-taxonomy cards]).

## 2. Edges — the edge-law (29 typed relations)

`RELATIONSHIPS.md`: **29 typed edges** (15 backend, 8 intra-UI, 6 cross-layer), each with typed endpoints
(`enforces`: Rule→Operation; `exposes`: Interface→Operation/Query; `produces-for`: Operation@A→Entity@B…).
This is the **edge-law**:
- **LAW = layering governance (C6):** a forbidden edge must be *unconstructible* (typed so no endpoint pair
  admits it), not merely flagged.
- **CHECK = validation governance (C11):** `validate-relationships` confirms a feature's declared edges
  conform. The constitution binds them: *"the LAW is layering's, the CHECK is validation's."*

**Coverage finding (toy T2b/M0):** the 29 edges each get a composition rule, **but the catalog under-covers
real relations** — T1 hit **2 relations with no edge type at all**: `Operation→Entity` (read) and
`Operation→ValueObject` (returns). → batch-1 **R3-P1/P2** (and R3-P3: split the Event composite).

## 3. Composability — how patterns compose in code (two levels)

Composability is the **realization** layer: given an edge, how must the two node-patterns reference each
other. It exists at two levels that must agree:

**Spec level (edge→composition rule).** Owned in `CODE-TAG-COMPOSABILITY-PATTERNS.md`: *"Edges describe
domain semantics; composability patterns make them executable."* A 13-row **pattern matrix** (e.g.
`enforces` = Operation calls the Rule before mutation; `orchestrates` = Workflow calls the Operations;
`exposes` = Interface calls the use-case). **The toy (T2/T2b) independently re-derived these same rules** —
a corroboration that the edge→composition mapping is stable/reproducible.

**Code level (the checker).** `check-code-tag-composability.ts` verifies the *actual code* realizes the
composition (the Operation really calls the Rule, etc.):
- **9 edges are tool-enforced** (CT-COMP-001..009): `enforces, enforces-cross, calculates, applies, exposes(→Op), exposes(→Query), orchestrates, mutates, fetches`.
- **4 documented but "Not yet" enforced:** `produces, transitions, contracts, consumes`.
- **CT-COMP-010/011/012** = structural (target-not-tagged / source-unresolved / target-unresolved).

**Owner: this is drift governance's method** (code↔spec alignment) — distinct from the engine's spec→test
derivation (validation). Composability is where the typed graph becomes *enforceable in the implementation*.

## 4. The unification (the load-bearing picture)

```
TAXONOMY (nodes)  ──typed by──►  each node ⇒ one code pattern      [layering: what exists + its layer]
      │
RELATIONSHIPS (edges) ──edge-law──►  which node pairs may connect   [layering LAW C6 / validation CHECK C11]
      │
COMPOSABILITY  ──per edge──►  how the two patterns reference in code [spec: patterns doc · code: CT-COMP checker = drift]
```

Two enforcement arms sit on this graph:
- **Engine derivation** (validation governance): spec → test obligations (the moat δ-rules) — proves the
  spec is *complete + derivable* (C5/C10).
- **Code-tag composability + drift** (drift governance): the code↔spec graph stays aligned over time
  (C7) — proves the *implementation realizes the graph*.

So "composability, edges, taxonomy" is not three topics — it's the **node / edge / realization** decomposition
of one executable graph, governed by layering (structure), validation (derivation), and drift (alignment).

## 5. The three coverage gaps (the actionable core)

| Gap | Where | Number | Owner route |
| --- | --- | --- | --- |
| **Edge-catalog coverage** | RELATIONSHIPS misses real edge types | ≥2 (op→Entity read, op→VO returns) | batch-1 **R3-P1/P2** |
| **Composability-pattern coverage** | patterns matrix + checker | ~12/29 edges have a pattern; **9/29 tool-enforced**; 4 "not yet"; ~17 unpatterned | drift governance (extend CT-COMP) |
| **Exercise coverage** | the toy tested one feature | 12/25 types, 10/29 edges | 2nd UI-heavy corpus (optional T5) |

These three are *distinct* — catalog completeness (do entries exist), realization completeness (is each
edge enforced in code), and empirical coverage (has a real feature exercised it).

## 6. Verdict context (toy) + interim stance

The spec-as-ontology toy **SURVIVED (narrow+conditional)**: the typed graph is a viable code substrate on
financial-settlement (M1 100 / M2 ~96 / M3 ~96 / M4 bounded), and **every failure traced to a v1-spec-doc
gap, not the hypothesis**. Full unification (Lane Z) is **not** green-lit — the mapping's viability is
equally what Lane A (generate + keep separate) needs; the decider (cheaper agents) is unmeasured. **Interim
stance = the two-plane boundary** (ontology on the authoring plane, derivation on the contract plane;
`2026-07-01-spec-as-ontology/findings.md`).

## 7. Open items → owners
- **R3** (batch-1): add the 2 missing edge types + resolve the Event composite; the 3 proposals are wired.
- **Composability enforcement**: promote the 4 "not yet" patterns + assess the ~17 unpatterned edges (drift governance).
- **Dual-typing**: split Calculation∧Policy nodes (spec-authoring / R6a crosswalk).
- **Empirical**: a 2nd corpus (T5) + the agent-cost experiment (settles Lane Z vs A).

## Residue
- Composability-pattern coverage numbers are read off the patterns-doc matrix + CT-COMP-000..012 codes; the
  exact per-edge enforced set beyond the matrix's "Enforced by Tool" column is not independently re-verified
  against the checker source (inference from the doc + code-tag codes).
- Prior-art cards ([authority-node-relationship-taxonomy]) concern the **cav2 authority** ontology (authority
  kinds/relations), a *different* taxonomy than the DomainSpec 25/29 — cited as adjacent governance
  discipline (relationship-invariant, axis-split), not the same catalog.
