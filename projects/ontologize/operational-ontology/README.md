# operational-ontology

Research sub-project under [ontologize](../README.md). It validates one specific
idea for **domainspec-core itself** (not the CyberAlchemy client product):

> Should [`arcanum/disciplines/DISCIPLINES.md`](../../../arcanum/disciplines/DISCIPLINES.md)
> be the **highest category of knowledge** for an **operational ontology branch** —
> on the same authority tier as **axioms** and **constitutions**?

"Operational" here means the **Arcanum/CyberAlchemy Operational Ontology**: knowledge
about *agent operation* — routes, sigils, prompts, disciplines, decisions, lessons —
**not** the per-run `run-context` branch (B3). That naming split is already settled in
[RECONCILIATION.md](../RECONCILIATION.md) and [ONTOLOGY-BRANCHES.md](../ONTOLOGY-BRANCHES.md).

## Status

- Phase: **executed end-to-end 2026-06-12** (all 9 steps; 5-role fanout ran with operator approval).
- Route: [operational-ontology-research.dispatch.json](operational-ontology-research.dispatch.json) —
  `dispatch_id: operational-ontology-research-20260612`, mode `research`, validated **`pass`**.
- **Verdict:** H0 (disciplines = axioms) **refuted as stated**, **reframed and accepted** — the
  operational branch's highest category is an operational *constitution + axiom* set; `DISCIPLINES.md`
  is its disciplined *source/feed* layer, not the apex. See
  [decisions/disciplines-as-axiom.md](decisions/disciplines-as-axiom.md).
- **Branch:** a candidate operational branch (`B-op`) is seeded for domainspec-core —
  [branch/operational-branch-seed.md](branch/operational-branch-seed.md) +
  [node schema](branch/operational-node.schema.yml). Pending ontology-harness acceptance.
- Reading order: [HYPOTHESIS.md](HYPOTHESIS.md) → [TOWER.md](TOWER.md) →
  [sessions/operational-analysis-receipts.md](sessions/operational-analysis-receipts.md) →
  [decisions/disciplines-as-axiom.md](decisions/disciplines-as-axiom.md) → [NEXT.md](NEXT.md).

## The prima-facie tension (why this needs adjudication, not assumption)

The repo **already** defines an authority hierarchy, so the idea is non-trivial:

- **Axiom = L7**, **Constitution = L6** in the Authority Levels table
  ([ONTOLOGY-ARCHITECTURE.md](../../../arcanum/development/cyberalchemy-ontology-lifecycle/ONTOLOGY-ARCHITECTURE.md) §Authority Levels;
  definitions in [BUSINESS-ONTOLOGY.md](../../../arcanum/BUSINESS-ONTOLOGY.md): axioms are
  load-bearing truths, constitutions are governance *derived from* axioms).
- **Disciplines are explicitly forbidden** from claiming promotion authority and cannot
  directly promote registry/ontology/glossary/sigil/spell knowledge
  ([DISCIPLINES.md](../../../arcanum/disciplines/DISCIPLINES.md) Growth Rule; README boundary).

So disciplines-as-axiom is in apparent conflict with current boundaries. The route's job is
to **resolve** that — the likely shape of a coherent answer is *not* "disciplines = axioms"
but "disciplines **feed** an operational axiom/constitution layer they do not themselves
hold." The adjudication step decides this on evidence.

## What the route does

1. **Recover literature** (`context-builder`) — the L0–L7 hierarchy, axiom/constitution
   definitions, the operational-ontology slice, the disciplines catalog, branch-aware model.
2. **Inventory telemetry** (`inventory`) — catalog the scattered observability streams as
   *candidate, non-authoritative* operational evidence (see HYPOTHESIS.md §Telemetry).
3. **Scaffold tower** (`research-tower`) — corpus, authority map, carry-set plan.
4. **Fan out analysis** (`robot-talks`) — five role-bound lanes incl. an adversary that
   tries to *refute* the hypothesis. **Recommended; requires operator approval.**
5. **Adjudicate** (`decision-gate`) — proponent vs skeptic, then a verdict that resolves the
   tension and names the owner + next promotion route.
6. **Define carry-set** (`definitions-governance`) — the candidate node/edge/mutation types
   the operational branch should carry.
7. **Seed the branch** (`ontology-vault`) — a branch-aware candidate skeleton + node schema
   for domainspec-core, with a few telemetry-derived candidate nodes.
8. **Validate + handoff** (`dispatch-spec` → `invoke`) — residue, NEXT, governance handoff.

## Guardrails

- Framework, disciplines, and telemetry are **read-only source evidence**.
- The operational branch, its carry-set, and any disciplines-as-axiom finding are
  **candidates** — no promotion to ontology, constitution, or axiom authority without
  **Constitution Governance** and **ontology-harness** review.
- The analysis fanout (step `fanout-operational-analysis`) is **recommended** and
  **requires operator approval** before delegated subagents run.

## Next

Run the route. First non-delegated stages (recover literature, inventory telemetry,
scaffold tower) can run immediately; pause at the fanout for approval. See HYPOTHESIS.md
for the evidence already gathered while authoring this route.
