# Glossary

Client-facing terms for the CyberAlchemy ontology + DAG offer. Each entry marks its origin:
**[GQ]** GoldenQuill source language, **[generic]** standard ontology/DAG/BI practice, or
**[CA]** a CyberAlchemy coinage (candidate).

- **Ontology** [generic] — an explicit, governed model of a company's concepts: its subjects
  (who/what it serves) and mechanisms (how value flows), with the attributes and relations that
  drive work.
- **DAG (directed acyclic graph)** [generic] — a graph of steps/records where edges point forward
  with no cycles; used here for both the _execution_ trace (what happened, in order) and the
  _governance_ chain (evidence → candidate → decision).
- **Subject ontology / segment cards** [CA, from CIC] — the "who we serve" axis; archetypes that
  configure search vocabulary, evidence schema, language register, reporting rhythm.
- **Mechanism ontology / value-mechanism cards** [CA, from CLC] — the "how value flows" axis
  (revenue routes, deal types, funding mechanisms); carries underwriting/qualification logic.
- **Orthogonality rule** [GQ] — the two axes are matched at runtime per opportunity, never
  hardcoded as a fixed cross-product.
- **Classification register** [GQ] — an operator-signed map of each data field to an authority
  class (public / shareable / confidential / restricted), gating where data may travel.
- **Promotion record DAG** [GQ] — the governed path by which an observation becomes reusable
  knowledge: events → evidence → candidate → review gates → owner decision → promoted/retired.
- **Promotion candidate** [GQ] — a proposed lesson/relation/insight that is _not yet_ authoritative.
- **Owner decision** [GQ] — the explicit approve / reject / retire / contradict act that promotes or
  blocks a candidate; the only thing that confers reuse authority.
- **Contradiction path** [GQ] — the stated way a candidate could later be proven wrong; required.
- **Governed edge catalog** [CA] — the single table that governs every edge between DAG nodes: its
  allowed source-type → target-type, cardinality, named inverse, category, and whether it must be
  acyclic. Turns a loose edge list into an auditable, testable contract.
- **Drift vs contradiction** [CA, from GQ + vault] — _drift_ is a neutral observed divergence between
  what was intended and what happened (preserves both); _contradiction_ is an adjudicated conflict
  between governance artifacts that **blocks promotion** until an owner resolves it.
- **Evidence-linked KPI** [CA, from KPI families] — a metric bound to its source evidence and
  interpretation limits so it cannot silently drift; reports a _pair_ (dimension + evidence chain),
  never a lone headline number.
- **Concept erasure** [CA, borrowed interpretive grounding] — a metric's _schema_ drops a dimension
  the business carries; the concept is lost before any number is computed. One of the two anti-collapse
  failure axes.
- **Number hallucination** [CA, borrowed interpretive grounding] — a metric's _value_ is fabricated or
  distorted at populate-time (swapped denominator, invented rows/defaults). The other anti-collapse axis.
- **Veracidade** [CA, from vault] — a per-node evidence grade (high/medium/low) carried by metrics,
  candidates, and promoted knowledge; the formal version of "proven vs hypothesis".
- **Evidence refs** [CA, from vault] — the source/event/test locators that back a node's veracidade;
  required to be non-empty for any "high" grade.
- **Receipt** [GQ] — an auditable artifact stating actual vs counterfactual (cost/energy/effort) with
  every claim traced to its source.
- **Agent council / seats** [GQ] — a set of role-bound agents (discover, draft, review, score,
  challenge) plus a deterministic policy gate.
- **Engine** [CA] — the runtime operator of the learning loop: Intake, Run Tracker, Gate Runner,
  Promotion Scorer, and Receipts/Query agents, plus the human Owner-decision gate.
- **Promotion-events ledger** [CA, from vault] — an append-only, tamper-evident audit log with one row
  per node change; even a blocked promotion is recorded.
- **Optimization chain** [CA, from GoldenQuill grant optimization-chain work] — the BI-expression layer
  on top of the engine's loop: a sentence-and-schema contract connecting a run node, an evidence-linked
  KPI (with its `veracidade` grade), an analysis method, and a named BI optimization. Consumes the
  engine's graded output; does not replace it.
- **BI optimization** [CA] — the decision-improvement insight produced by an optimization chain,
  always bounded by claim label, privacy scope, and owner decision.
- **Deterministic gate** [generic, GQ "Logician"] — a code (non-LLM) check that fail-closes; cannot
  be jailbroken or overridden by a prompt.
- **Self-validation / "test your own work"** [GQ] — the rule that each agent validates its own
  output before handoff.
- **Governed learning loop** [GQ] — observe → propose → approve, with privacy and contradiction
  gates, so an organization learns from outcomes without leaking private signal or over-trusting noise.
- **Client-sendable package** [GQ] — the layered deliverable (overview, brief, reference, decisions)
  handed to a buyer.
