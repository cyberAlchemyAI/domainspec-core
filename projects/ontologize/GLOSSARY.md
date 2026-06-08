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
- **Evidence-linked KPI** [CA, from KPI families] — a metric bound to its source evidence and
  interpretation limits so it cannot silently drift.
- **Receipt** [GQ] — an auditable artifact stating actual vs counterfactual (cost/energy/effort) with
  every claim traced to its source.
- **Agent council / seats** [GQ] — a set of role-bound agents (discover, draft, review, score,
  challenge) plus a deterministic policy gate.
- **Deterministic gate** [generic, GQ "Logician"] — a code (non-LLM) check that fail-closes; cannot
  be jailbroken or overridden by a prompt.
- **Self-validation / "test your own work"** [GQ] — the rule that each agent validates its own
  output before handoff.
- **Governed learning loop** [GQ] — observe → propose → approve, with privacy and contradiction
  gates, so an organization learns from outcomes without leaking private signal or over-trusting noise.
- **Client-sendable package** [GQ] — the layered deliverable (overview, brief, reference, decisions)
  handed to a buyer.
