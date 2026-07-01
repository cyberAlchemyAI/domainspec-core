---
node_type: define
is_session: false
status: candidate
created: 2026-07-01
authored_by: invoke (mode: define)
build_from: ./SEED.md (2026-06-11 — Lane Z anchor + promotion boundary)
informed_by: ../2026-07-01-spec-as-ontology/findings.md (two-plane boundary; Lane Z-vs-A left open for this tower)
target_artifact: spec-ontology-unification toy (Lane Z falsification)
promotion_boundary: LOCAL RESEARCH ONLY — no change to spec schema, code-pattern catalog, agent constitutions, or runtime until a later approved task-session (SEED.md:56-58)
---

# Define — Spec–Ontology Unification Toy (Lane Z falsification)

## Intent

Decide, with evidence, whether DomainSpec's typed spec-graph is a viable **substrate** for the
node→code-pattern / edge→composition model the SEED hypothesizes — i.e. whether "spec == ontology"
(Lane Z) earns a real decision, or whether Lane A (keep separate + generated mapping) is the honest
answer. The 2026-07-01 spec-as-ontology research explicitly **deferred** Lane Z-vs-A to this tower
(its toy was unrun); this define makes the toy runnable and its verdict decidable.

## The falsifiable claim (pre-registered — FREEZE before the run)

> For a real feature, DomainSpec's typed graph (25 TAXONOMY node-types + 29 RELATIONSHIPS edge-types)
> maps to code deterministically and near-1:1, with cross-cutting context bounded by the node's own
> subgraph — making it a sound substrate for bounded/ephemeral implementation agents.

**Toy corpus:** `impl/test-derivation-engine/__fixtures__/financial-settlement/` (small, engine-parseable;
spans Structural + Behavioral + Connective + Lifecycle — Entity, Value Object (Money), Enum
(PaymentMethod/PaymentErrorCode), Operation (ProcessPayment), Rule (MaxAmountRule), Event
(PaymentInitiated), State Machine (PaymentStatus)).

**SURVIVED iff ALL four hold on the corpus:**
1. **Taxonomy closure** — 100% of the feature's concepts classify to exactly one of the 25 types (0 unclassifiable).
2. **Node→pattern near-1:1** — ≥90% of nodes map to exactly one code pattern (TAXONOMY "Architecture Mapping Appendix"); the 0-pattern / >1-pattern exceptions are ≤10% and each documented.
3. **Edge→composition coverage** — ≥90% of the feature's edges map to a named composition rule; gaps ≤10%, each documented.
4. **Bounded cross-cutting context** — every pattern's required inputs are carried by the node + its direct edges (the "spec subgraph"), OR the leak is a NAMED, enumerable carrier (e.g. shared Value Objects via `contains`). 

**FALSIFIED** if any of 1–4 fails materially (taxonomy not closed / node↔pattern materially many-to-many
/ edges uncomposable / patterns routinely need context outside the subgraph → bounded agents can't work).
**INVALID** if the corpus is too trivial to exercise ≥3 TAXONOMY categories (pick a richer feature).

Passing the toy is **substrate viability**, NOT proof of agent cost savings (that needs a later,
separate agent-run experiment) and NOT authority to fuse spec and code — see promotion boundary.

## Glossary

- **spec-graph** — the feature's concepts as typed nodes + typed edges (TAXONOMY × RELATIONSHIPS).
- **node→code-pattern** — the map from a concept-type to an implementation pattern (the TAXONOMY
  functional-style appendix, e.g. Rule → pure predicate, Operation → use-case factory).
- **edge→composition rule** — how two patterns compose across an edge (e.g. `enforces`: the Rule
  predicate is called inside the Operation use-case).
- **near-1:1** — a node maps to exactly one pattern (the failure modes are 0 patterns or >1).
- **taxonomy closure** — every concept fits exactly one of the 25 types; nothing falls outside.
- **cross-cutting context leak** — a pattern needs data not carried by its node's own subgraph.
- **Lane Z / Lane A** — unify (spec==ontology) vs keep-separate-with-generated-mapping (SEED.md:43-53).

## Non-goals (from SEED.md:60-64)

- Committing to "spec == code/ontology" as canonical before the toy proves gains.
- Designing the ephemeral-agent runtime (this decides whether the typed graph is the right substrate,
  not how to ship agents).
- Any spec-schema, engine, or code mutation (promotion boundary).

## Open decisions (surfaced, not decided)

- **DEF-D1 — corpus choice.** financial-settlement (recommended: small, engine-known) vs
  agent-execution-orchestrator (richer, has rules.md). If financial-settlement fails INVALID
  (too trivial), escalate to AEO.
- **DEF-D2 — criterion thresholds.** The 90%/≤10% bars are proposed; the owner FREEZES them at the
  experiment step before the run (experiment discipline — no post-hoc adjustment).
