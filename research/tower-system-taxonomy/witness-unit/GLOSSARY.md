---
module: tower-witness-unit
version: current
status: draft
updatedAt: 2026-06-18
docType: glossary
invoke_mode: define
---

# GLOSSARY: Tower System — Witness Unit

Status legend: `linked` = matches an existing repo/owned concept; `candidate` = proposed here, not promoted; `no-match` = new, needs definition. Candidate promotion is never automatic.

| Term | Status | Definition | Source / owner |
|---|---|---|---|
| Tower | candidate | A governed knowledge unit = a queryable knowledge graph + a persona set, built over a source. **Note:** as a *layer label* this collapses into "research-tower output" (findings R3); used here only for the substrate-as-a-whole. | research-tower (partial); findings E3/R3 |
| Queryable knowledge graph | candidate | A traversable graph object (typed nodes + typed edges) you can query — distinct from `research-tower`'s current markdown prose. The real surviving L1 object. | findings E2/E3 (Zettelkasten/RDF/KG owned; queryable-object delta is the add) |
| Graph node | linked | A typed concept in the graph (e.g. `Aggregate`), the anchor target for a persona. | KG/RDF-OWL (W3C); findings E2 |
| Persona | candidate | A durable artifact anchored to a graph node, carrying a `stance`, `criteria`, and `provenance`, able to hold a position in a debate. Distinct from the constitution's ephemeral `angle` by **graph-anchoring + stance**, not by persistence. | D1; findings R3; Cooper 1999 / de Bono 1985 (idiom, build-from-owned) |
| Persona content schema (D1) | candidate | The field set `{anchor, stance, criteria, voice?, provenance}` that makes a persona non-vacuous. | findings R2/D1 |
| Anchor | candidate | A persona field referencing the graph node it derives from. | D1 |
| Opposable-stance rule (D2) | candidate | A deterministic mapping from (node, contested proposition) → an opposable stance, so two personas genuinely disagree rather than compose. | findings R2/D2 |
| Tensioned debate | linked | A two-persona exchange over one contested proposition, run via robot-talks transport with a human gate. | robot-talks |
| Dispatch | linked | The act of instantiating a tensioned group to do work; the constitution's existing router (`dispatch_type`). Used instead of the collapsed label "application". | subagents-strategy constitution; findings R3 |
| Oracle-consensus | candidate | A staged aggregation over judge votes: unanimous → supermajority → ELO-weighted → human-flag. Components owned (self-consistency Wang 2022, LLM-as-a-Jury Verga 2024 *verify*); the staged ladder is the narrow novel part. | findings E1/R3 |
| ELO substrate (D3) | candidate | A rating store (rating per persona/judge, K-factor, update rule) used by oracle-consensus layer 3. Build-from-owned (Chatbot Arena/LMSYS, Chiang 2024, arXiv:2403.04132 *verify*; Elo 1978). | findings E1/D3 |
| Supermajority threshold (D3) | candidate | The fixed fraction at which oracle-consensus layer 2 resolves (value to be set in design). | findings R2/D3 |
| Verdict | linked | The emitted decision object `{proposition, outcome, confidence, route}`, confidence graded by the scoring substrate. | research verdict matrix; findings E3 |
| Witness unit | candidate | The smallest end-to-end instantiation proving the architecture is non-vacuous. | findings R2 |
| MOGT | linked (owned) — CORRECTED | **Multi-Objective Game Theory** for agentic conversation decisions: a per-action decision/selection policy (regimes heuristic/weighted_sum/pareto_guided/bargaining_guided over objectives quality/cost/latency/safety/escalation_risk). NOT a scoring mode — a different layer (decision/action-selection). Prior "dropped" verdict was wrong (fabricated definition). Owned, design-stage/unproven. | `arcanum/research/mogt-agentic-conversation/`; see [../PRECEDENT-RECHECK.md](../PRECEDENT-RECHECK.md) |

## Glossary linking notes

- `linked` terms reuse existing repo/owned concepts — no promotion needed.
- `candidate` terms are this unit's net-new vocabulary; promotion to a canonical glossary requires a separate governed decision (not automatic).
- One `no-match (dropped)` recorded for traceability (MOGT) so the drop is auditable.
