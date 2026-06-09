# Definitions

Canonical-for-this-project definitions of the load-bearing terms, each with a status:
**source-backed** (proven in GoldenQuill), **seed** (clear but unproven outside GoldenQuill),
**analogy** (borrowed framing), or **candidate** (proposed coinage). None are promoted to canonical
Arcanum or CyberAlchemy vocabulary without owner review.

### Ontology layer (the "what we know" model)

- **Two-axis ontology** — _source-backed._ A company's knowledge modeled as orthogonal subject and
  mechanism axes, matched at runtime. Proven by GoldenQuill's CIC × CLC with the
  `F-CIC-CLC-COUPLING-VIOLATION` guard.
- **Card primitive** — _source-backed._ A field on an ontology card that configures downstream
  behavior (e.g., search vocabulary, evidence schema, language register, reporting rhythm). (Formerly
  "operational primitive"; renamed to free "operational" from overload now that B3 is **run-context**.)
- **Classification register** — _source-backed._ Operator-signed field→authority-class map; gates
  data movement; fail-closed when class is indeterminate.

### DAG layer (the "how knowledge becomes trusted" governance)

- **Promotion record DAG** — _source-backed._ The acyclic chain events → evidence → candidate →
  review → owner decision → promoted/retired, with execution and governance graphs kept orthogonal.
- **Eight promotion primitives** — _source-backed._ Source-truth; evidence≠candidate≠promotion;
  metric≠authority; privacy-safe generalization; mandatory contradiction path; stage≠outcome≠
  validation; propose-vs-approve uses; governance orthogonal to execution.
- **Deterministic gate** — _source-backed._ A zero-token, fail-closed, code-enforced rule (GoldenQuill's
  Logician + the 11-rule L0 validator).
- **Governed edge catalog** — _seed._ A single table governing each DAG edge (source-type→target-type,
  cardinality, named inverse, category, acyclicity). Clear and useful, but unproven outside GoldenQuill's
  edge set; the cardinality/inverse columns are an adaptation.
- **Contradicts edge** — _candidate._ A first-class, symmetric, promotion-blocking edge (PC↔PC or
  PC↔KP). Generalizes GoldenQuill's mandatory contradiction path into a graph rule; patterned on the
  `domainspec/vault` `contradicts` edge.
- **Veracidade (node field)** — _candidate._ A per-node confidence grade {high, medium, low} on the
  three evidence-bearing node types; the formal replacement for hand-written proven/hypothesis prose.
  Borrowed from `domainspec/vault`; convicção deliberately omitted (materialized by OwnerDecision).
- **Evidence refs (node field)** — _candidate._ The list of source/event/test locators backing a node's
  `veracidade`; non-empty is required for `veracidade: high`.

### BI layer (the "decision value" output)

- **Evidence-linked KPI** — _source-backed._ A metric carrying denominator definition, interpretation
  limits, source events, and a promotion owner.
- **Anti-collapse principle** — _analogy._ A metric fails in two independent ways — concept erasure
  (schema drops a dimension) and number hallucination (value distorted) — so every metric reports a
  pair, not a number. Borrowed framing from the DomainSpec schema-residue vs instance-residue
  distinction; interpretive, not a proof for metrics.
- **Counterfactual receipt** — _source-backed._ "Actual vs counterfactual = delta, with proof"
  (GoldenQuill CycleReceipt / WPFA PDF).
- **Governed learning loop** — _source-backed._ observe → propose → approve with privacy and
  contradiction gates.
- **Optimization chain** — _seed._ A sentence-and-contract method that binds a run node/action,
  evidence-linked KPI, response window, analysis method, claim label, and reuse boundary into a named
  BI optimization. Generalized in [OPTIMIZATION-CHAIN-METHOD.md](OPTIMIZATION-CHAIN-METHOD.md).
- **BI optimization** — _seed._ A named decision-improvement output from an optimization chain, such
  as exception resolution acceleration, carrier reliability optimization, or rework reduction insight.

### Agent layer (the "who does the work" execution)

- **Ontology-driven routing** — _source-backed._ Cards + register decide which agent runs and where
  (cloud/local).
- **Four Autonomy Rules** — _source-backed._ Save state always; test your own work; be explicit;
  clean output.
- **Cross-family rigor** — _source-backed._ A reviewer agent must not share a model family with the
  author it reviews.
- **Engine** — _candidate._ The runtime operator of the governed learning loop: 5 agents (Intake, Run
  Tracker, Gate Runner, Promotion Scorer, Receipts/Query) over the 6 node types + a human OwnerDecision
  gate. Adapted from the `domainspec/vault` 5-agent maintenance architecture.
- **`promotion_events` ledger** — _candidate._ An append-only, hash-chained audit log; one row per node
  mutation (INSERT only). Makes the 11 gates auditable after the fact; adapted from the vault's
  `ontology_events` table.

### Product layer (the "what we sell")

- **CyberAlchemy ontology+DAG engagement** — _candidate._ A consulting engagement that installs the
  four layers above over a client's existing data and agents. Generalizes the GoldenQuill proof;
  unproven outside grant intelligence → carries pilot validation.
- **Governance deliverable** — _seed._ The layered client-sendable package as a repeatable artifact.
