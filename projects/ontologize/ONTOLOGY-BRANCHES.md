# Ontology Branches — and how they interact with the product and client work

Explains every branch of the ontology and maps each to the four product layers and to client work.
Produced by refine run [`ontologize-ontology-branches-20260608`](development/refinement-runs/ontologize-ontology-branches-20260608/)
with one branch-evidence-mapper subagent.

Tags: **[SB]** cited source · **[H]** hypothesis. Sources: `ontology-vault` (branch-aware
business↔system + bridge) and the GoldenQuill ontology DAG on `master`
(`goldenquill_ontology_dag_grant_research_synthesis_2026-06-01.md`, meaning/system/operational/bridge).
Candidate design only — no canonical promotion, no pricing/clients; sources read-only.

## Why "branches"

"The ontology" is not one flat model. It is split into **branches** — separate facets of knowledge
that are governed independently and connected by **bridge edges**. This is what lets the system tell
_intended meaning_ apart from _actual behavior_ and detect drift between them, instead of smoothing
them into one blurry truth. [SB ontology-vault branch-aware model]

## The four branches [SB]

| Branch                                               | Definition                                                                | Carries                                                             |
| ---------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **B1 — meaning** (a.k.a. business / domain / intent) | what the company _means_ — policy, rules, value claims, outcomes          | domain concepts, policies, targets, premises, value measures        |
| **B2 — system**                                      | how it's actually _implemented / run_ — artifacts, runtime behavior, data | events, records, services, data shapes, metrics, tests, gates       |
| **B3 — run-context**                                 | one bounded _run context_ (first-class, not optional)                     | run id, org scope, deadline/posture, lifecycle state + depth        |
| **B4 — bridge**                                      | the _connections + evidence between branches_                             | realization, observation, constraint, contradiction, drift findings |

> **Naming:** B3 is named **run-context** in ontologize. The GoldenQuill source calls the same branch
> *operational*; we renamed it to avoid colliding with the Arcanum/CyberAlchemy "Operational Ontology",
> which is a different concept (knowledge about *agent operation* — routes, sigils, prompts), not a
> per-run denominator context (decision: [RECONCILIATION.md](RECONCILIATION.md) §1, resolves R13).
>
> **B3 run-context is load-bearing:** denominators are defined _inside a run context_, so the rule
> "stage ≠ outcome" (GQ-PR-L0-003) and honest metric denominators (GQ-PR-L0-002) are really a _branch
> boundary_. GoldenQuill made this branch first-class precisely because run truth is run-specific. All
> four branches are first-class in ontologize (decision: RECONCILIATION.md §1, resolves R14). [SB]

## Bridge edge types (how branches connect) [SB]

The bridge (B4) edges are `realized_by` · `depends_on` · `observed_by` · `tested_by` · `drifts_from`
· `traced_to`. These — together with the execution, promotion, and control edges — are governed by a
single **edge catalog** (source-type → target-type, cardinality, inverse, acyclicity) in
[DAG-AND-METRICS.md §3](DAG-AND-METRICS.md#3-edge-catalog-how-nodes-connect--governed). That catalog
is the single source of truth; this file keeps only the branch mapping.

> **`drifts_from` vs `contradicts`:** `drifts_from` is the neutral, observed divergence between actual
> behavior (B2/B3) and intended meaning (B1) — it preserves both sides. `contradicts` (a promotion
> edge, added in the catalog) is the *adjudicated* conflict between governance artifacts that **blocks
> promotion** until an owner resolves it. Drift is the raw signal; contradiction is the verdict.

## Branch → product layer

| Branch         | L-ont (cards)                         | L-reg (register)           | L-dag (promotion DAG)                                | L-bi (BI + agents)                                     |
| -------------- | ------------------------------------- | -------------------------- | ---------------------------------------------------- | ------------------------------------------------------ |
| B1 meaning     | **primary** (subject×mechanism cards) | authority class of a field | claim / rule / criterion nodes                       | business outcomes → KPI families                       |
| B2 system      | secondary                             | field → authority mapping  | execution-path nodes (events, records, gate results) | system metrics, agent routing, gate enforcement        |
| B3 run-context | — (run context, not a card)           | org-scope marker           | **lifecycle_state, outcome_event**                   | **run boundary = metric denominators**; agent dispatch |
| B4 bridge      | realization of a card                 | cross-field constraints    | **edges + drift_finding / test_link / evidence_gap** | alignment gates, contradiction paths, feedback loops   |

## Branch → client work

**Cap factory** (continuous production):

- B1 meaning: yield/scheduling/cost policy ("SKU X must hit 95% first-pass yield on line 2").
- B2 system: MES events — `lot_completed`, `defect_logged`, `rework_logged`.
- B3 run-context: the lot-or-order run boundary (assessment decision) + production cycle context.
- B4 bridge: "Q4 line-2 rework spike **drifts_from** the baseline process rule" → candidate → owner decision → revised scheduling rule.

**Logistics** (discrete shipments):

- B1 meaning: routing/SLA/carrier policy ("lane A→B in 3 days, 99%, under $X").
- B2 system: TMS events — `delivered`, `delivery_exception`, `cost_posted`, `claim_filed`.
- B3 run-context: the shipment-id run boundary + carrier/lane/customer context.
- B4 bridge: "lane A→B late **observed_by** the on-time metric when carrier C used in winter" → candidate → routing adjustment → next runs routed better.

## Cross-branch interaction + drift detection [SB]

The improve-over-time loop _is_ a walk across branches:

```text
B2 system events ─▶ B3 run-context metrics (denominators) ─▶ B4 bridge candidate (drifts_from / observed_by)
        ─▶ owner decision (needs evidence from BOTH branches) ─▶ B1 meaning updated (cards/rules)
        ─▶ next runs discovered/routed/scored better
```

Drift rules [SB ontology-vault]: every promoted business behavior with impact needs ≥1 bridge edge or
an explicit evidence gap; drift edges **preserve both** the business expectation and the observed
behavior (no silent smoothing); a bridge claim asserting alignment must cite evidence from both
branches before promotion.

## How this lands in the product offer

- The **ontology** the consulting installs is a _4-branch_ model, not a flat taxonomy — that is the
  differentiator vs ordinary data modeling.
- **Lane choice** ([DELIVERY-LANES.md](DELIVERY-LANES.md)): branch separation + bridge/drift is exactly
  what Lane B's `ontology-vault` provides natively (`map --branch business`); Lane A approximates it
  with disciplined separate sheets + manual bridge links.
- **Per-client:** the assessment populates B1 (their policies), identifies B2 sources (their systems),
  defines B3 run boundary, and the pilot proves a B4 drift→decision→improvement on real data.

## Residue

- B3 run-boundary for cap factory (lot vs order) — assessment. [H]
- Per-vertical event catalog + proof metric — assessment. [H]
- Card runtime concept-graphing is dormant upstream in GoldenQuill (not ours). [SB]
- The run-context branch (the source's *operational* branch) was absent from older ontology templates; now first-class. [SB]
