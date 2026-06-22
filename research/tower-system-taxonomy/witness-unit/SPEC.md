---
module: tower-witness-unit
version: current
status: draft
updatedAt: 2026-06-18
docType: spec
discovery_basis: research/tower-system-taxonomy/findings.md
target_lifecycle: spell (handoff to spellcraft)
invoke_mode: define
---

# SPEC: Tower System — Witness Unit (L0)

## Purpose

Specify the **smallest end-to-end unit that witnesses the Tower System architecture**: one tower → one graph-anchored persona → one two-persona tensioned debate → one scoring resolution → one verdict, on a single concrete domain (Domain-Driven Design). Defining this unit forces the three definitions the research found missing (D1/D2/D3); without it the architecture is unwitnessed (per [findings.md](../findings.md), Gödel non-vacuity pass).

This spec is **scope-bounded to the witness unit**. It is not the full four-layer system.

## Discovery basis

[findings.md](../findings.md) is the discovery (design space, decisions, alternatives, open questions). Load-bearing conclusions carried in:

- The system is a **precedent-clean assembly** over a blackboard-architecture integration pattern (Hearsay-II/BB1), composing existing sigils + net-new primitives (findings R1).
- Novelty lives entirely in **D1/D2/D3** (findings R2). These are this spec's core requirements.
- **MOGT is dropped** (collapses to self-consistency, findings R3). Not in scope.
- The layer labels **"tower" (L1)** and **"application" (L3)** are re-skins; this spec uses the surviving objects — *queryable knowledge graph* and *dispatch* — not the collapsed labels (findings R3).
- A persona is distinct only by **graph-anchoring, not persistence** (findings R3). The schema must lead with the anchor + stance, not "a saved angle".

## In scope (the witness pipeline)

```
[DDD tower: queryable graph]
      │  select one node (e.g. "Aggregate")
      ▼
[persona P_A]  ◀─ graph-anchored, carries a stance derived from the node
      │  pair with a tensioned counterpart P_B (anchored to a node that yields an opposable stance)
      ▼
[2-persona tensioned debate]  ── reuse robot-talks transport + human gate
      │  produces two positions on one contested proposition
      ▼
[scoring resolution]  ── oracle-consensus over judge votes, with a defined threshold + ELO substrate
      ▼
[verdict]  ── reuse the research GO/KILL-style verdict object
```

## Functional requirements

- **FR-1 — Tower fixture.** One DDD tower exists as a *queryable* graph object (nodes + typed edges), not prose. Minimum: 3 nodes (`Aggregate`, `Bounded Context`, `Ubiquitous Language`) + typed edges. Reuse `research-tower` to produce the source-backed content; add the queryable graph object as the net-new surface.
- **FR-2 (D1) — Persona content schema.** A persona is an artifact with: `anchor` (graph node ref), `stance` (the position it holds, derived per D2), `criteria` (what it evaluates positions against), `voice` (optional), `provenance` (source nodes). The schema MUST give a persona enough to *hold a position in a debate* — provenance fields alone are insufficient (findings R2/D1). It MUST be distinguishable from the constitution's ephemeral anti-bias `angle` (durable + graph-anchored + stance-bearing, not a saved angle).
- **FR-3 (D2) — Node→opposable-stance rule.** A deterministic rule that maps a graph node (+ the contested proposition) to an *opposable* stance, such that two personas anchored to related nodes produce genuine disagreement, not mere composition (findings R2/D2: graph adjacency = composition, not tension). The rule names the contested proposition explicitly.
- **FR-4 — Tensioned debate.** Reuse `robot-talks` transport + human gate to run P_A vs P_B on one contested DDD proposition (e.g. "Should the Order aggregate span the Shipping bounded context?"). Output: two positions + their disagreement axis.
- **FR-5 (D3) — Scoring substrate + resolution.** Define: (a) an ELO/rating store (rating per persona, K-factor, update rule), (b) a supermajority threshold value, (c) the oracle-consensus resolution that consumes N judge votes over the debate and returns a graded verdict via the ladder unanimous→supermajority→ELO-weighted→human-flag. Must execute, not degenerate to bare majority vote (findings R2/D3).
- **FR-6 — Verdict.** Emit a verdict object reusing the research GO/KILL-style schema `{proposition, outcome, confidence, route}`. `confidence` MUST carry the graded score from FR-5, not just a majority count.
- **FR-7 — End-to-end witness.** The five steps run as one traced pipeline on the DDD fixture and produce a non-trivial, non-vacuous verdict.

## Non-goals

- The full four-layer system (L2 construction methods beyond the one fixture; L3 application modes beyond debate; recursion/towers-in-towers).
- MOGT *integration* into the tower (deferred until after MOGT's own evidence run — see Sequencing). MOGT is **not** dropped; it is the owned decision/action-selection policy layer, run first for evidence.
- `read-through` and `promote` construction modes (deferred).
- Persistence/library management beyond a single stored persona pair (durability is asserted by the schema; a library is deferred).
- World-novelty claims: ELO, oracle-consensus, synthesis, KG are build-from-owned (cite owners; net-new only in-repo).

## Acceptance criteria

- A1: the DDD tower graph is queryable (a query returns nodes/edges), proven by one query example.
- A2 (D1): a persona artifact instance is written and validated against the schema; it carries a stance, not just provenance.
- A3 (D2): the node→stance rule produces two opposable stances for one proposition; a reviewer confirms the disagreement is genuine (not composition).
- A4 (D3): oracle-consensus runs on ≥3 judge votes and returns a graded confidence using the threshold + ELO substrate; layers 2 and 3 are demonstrably executable (not skipped).
- A5: the end-to-end trace emits a verdict whose confidence is graded, on the DDD proposition.

## Decisions (carried from findings)

| # | Decision | Basis |
|---|---|---|
| DEC-1 | Scope = witness unit (L0), not full system | findings R2; user (2026-06-18) |
| DEC-2 | Target lifecycle = spell composing sigils | findings R1; user (2026-06-18) |
| DEC-3 | **MOGT is owned, not dropped** — Multi-Objective Game Theory (`arcanum/research/mogt-agentic-conversation/`), a per-action decision/selection policy reused as a distinct layer; prior drop was a fabricated-definition error | [../PRECEDENT-RECHECK.md](../PRECEDENT-RECHECK.md) |
| DEC-4 | Use "queryable knowledge graph" + "dispatch", not labels "tower"/"application" | findings R3 |
| DEC-5 | Persona defined by graph-anchoring + stance, not persistence | findings R3 |
| DEC-6 | **Run MOGT experiments (E1–E4) for evidence BEFORE building the tower** — de-risk by validating the owned-but-unproven MOGT layer first; the tower then reuses a validated MOGT | user (2026-06-18) |

## Reused sigils + owned prior work (assembly)

`research-tower` (tower content) · `robot-talks` (debate transport + human gate) · subagents-strategy constitution + `research` verdict matrix (verdict schema) · `anti-bias-vector-composition` (tension *principle* only — mechanism does not transfer).

**OWN-PRIOR-WORK reused** (corrected by [../PRECEDENT-RECHECK.md](../PRECEDENT-RECHECK.md) — these are your own in-repo projects, not external precedent):

- multi-agent **debate** construction — `arcanum/research/dispatch-composition-attack/`, `observability-adaptation/` (**executed** exemplars).
- **research-tower / distill-build** construction — `arcanum/research/autobayes/`, `monoidal-categories-multicategories/` (**executed**).
- multi-objective **scoring + decision/action-selection policy** — `arcanum/research/mogt-agentic-conversation/` (MOGT; owned, **design-stage/unproven** — evidence run pending, see Sequencing).

## Net-new primitives (this unit introduces — the real build risk)

Persona-as-artifact (D1) · queryable graph object (FR-1) · the **ELO/oracle-consensus** scoring family (D3). These three have **no in-repo owner** (confirmed by PRECEDENT-RECHECK) — they are the genuine net-new work. Multi-objective scoring + decision policy are NOT net-new: owned by MOGT, reused.

## Open gaps → routed to design/plan

- D1/D2/D3 are *named* here but their concrete schemas/rules are designed in DESIGN.md and decomposed in WORK-PACK.md.
- "verify" flags on citations (arXiv IDs, ResonantOS "v4") remain open from findings.

## Sequencing (decision DEC-6: MOGT evidence before tower)

MOGT is owned but **design-stage with zero live runs** (its own `MOGT-EVIDENCE-STATUS.md` rates all four claims *insufficient evidence*). Building the tower on an unproven owned layer is the risk. Decision: run MOGT's existing experiments first.

- **Phase 0 — MOGT evidence (predecessor, do first):** run MOGT experiments in first-wave order **E1 → E2 → E4 → E3** (`arcanum/research/mogt-agentic-conversation/experiments/`) to move claims C1–C4 off *insufficient evidence*. Owner: the MOGT project's own experiment lifecycle (`experiment-harness`). Gate to Phase 1: at least E1+E2 produce live evidence.
- **Phase 1 — tower witness-unit (this SPEC):** build C1–C5. The witness-unit's own scoring (oracle-consensus, D3) is independent of MOGT and could in principle proceed in parallel, but per DEC-6 we hold tower build until Phase-0 evidence exists, so the tower reuses a **validated** MOGT decision layer rather than an unproven one.

## Next route

**Phase 0 first:** run MOGT experiments (E1→E2) via `experiment-harness` in the MOGT project. **Then Phase 1:** `spellcraft` to design/install the tower spell (design + plan for the witness unit are already authored: DESIGN.md, WORK-PACK.md).
