---
module: tower-witness-unit
version: current
status: draft
updatedAt: 2026-06-18
docType: work-pack
invoke_mode: plan
---

# WORK-PACK: Tower System — Witness Unit

## Control Fields

| Field | Value | Notes |
|---|---|---|
| workPackGateStatus | block | D1/D2/D3 carry design-open blockers (B-001..B-003); resolve before mutation-capable execution. |
| complexity | medium | 6 tasks; net-new domain logic (D1/D2/D3); no cross-repo; no durable migration; unresolved design gates. |
| outputMode | single-file | Execution-ready inline; split into work-pack/tasks/* recommended before parallel multi-worker execution (flagged gap). |
| executionPackRef | n/a | Single coordinator; add if parallelized. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0 is this unit. |
| activeLayerWindow | L0 | |
| readinessProfile | pilot | Witness/proof, not production. |

## Objective Summary

- Objective: build the 5-step DDD witness trace (C1→C5) proving D1/D2/D3 are non-vacuous.
- Primary inputs: [SPEC.md](SPEC.md), [DESIGN.md](DESIGN.md), [GLOSSARY.md](GLOSSARY.md), findings.md.
- Success condition: acceptance A1–A5 (SPEC) pass; the trace emits a **graded** verdict on the DDD proposition.
- **Precondition (DEC-6 / B-004): Phase 0 = run MOGT experiments E1→E2 for evidence before this tower build starts.** See SPEC Sequencing + IMPLEMENTATION-LAYERING P0.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
|---|---|---|---|---|---|
| S-001 | Queryable DDD tower-graph fixture (C1) | L0 | W0 | research-tower | a query returns nodes/edges (A1) |
| S-002 | Persona schema + node→stance rule (C2; D1+D2) | L0 | W1 | S-001 | tensioned pair validated, disagreement genuine (A2,A3) |
| S-003 | Debate run (C3) | L0 | W1 | S-002, robot-talks | two positions + axis on the proposition |
| S-004 | Scoring substrate + resolution (C4; D3) | L0 | W2 | S-003 | graded confidence, layers 2–3 executed (A4) |
| S-005 | Verdict emit + end-to-end trace (C5) | L0 | W2 | S-004 | graded verdict emitted (A5) |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
|---|---|---|---|---|---|---|---|
| TASK-FIXTURE | C1 queryable DDD graph fixture | L0 | low | W0 | DESIGN §3 C1 | ready | not-started |
| TASK-D1 | C2 persona content schema | L0 | medium | W1 | SPEC FR-2; DESIGN §3 C2 | blocked (B-001) | not-started |
| TASK-D2 | C2 node→opposable-stance rule | L0 | high | W1 | SPEC FR-3; DESIGN §3 C2, R-1 | blocked (B-002) | not-started |
| TASK-DEBATE | C3 robot-talks adapter | L0 | low | W1 | DESIGN §3 C3 | ready-after D1/D2 | not-started |
| TASK-D3 | C4 ELO store + oracle-consensus resolution | L0 | high | W2 | SPEC FR-5; DESIGN §3 C4 | blocked (B-003) | not-started |
| TASK-VERIFY | C5 verdict + end-to-end A1–A5 | L0 | medium | W2 | SPEC acceptance | ready-after-implementation | not-started |

## Layer-mapped waves

- **W0 (L0 seed):** TASK-FIXTURE. Layer question: does a queryable graph object exist? Promotion evidence: A1 query example.
- **W1 (L0 core):** TASK-D1, TASK-D2, TASK-DEBATE. Layer question: can a graph-anchored persona hold an opposable stance producing genuine tension? Promotion evidence: A2, A3.
- **W2 (L0 close):** TASK-D3, TASK-VERIFY. Layer question: does scoring grade the debate (not degenerate to majority) and emit a verdict? Promotion evidence: A4, A5.

## Implementation-detail specs (medium/high tasks)

### TASK-D1 — persona content schema (medium)
- Purpose/decision: define the artifact that lets a persona hold a debate position.
- Inputs: graph node, contested proposition. Outputs: `Persona{anchor, stance, criteria, voice?, provenance[]}`.
- State touched: persona store (new).
- Rules: schema MUST include a `stance` (not provenance-only); MUST be distinguishable from the constitution's ephemeral `angle` (durable + anchored + stance-bearing).
- Edge cases: node with no defensible stance for the proposition → reject pair. Failure mode: provenance-only persona → A2 fail.
- Acceptance: a written persona instance validates and carries a stance (A2).

### TASK-D2 — node→opposable-stance rule (high; R-1)
- Purpose/decision: turn (node, proposition) into an *opposable* stance so two personas disagree, not compose.
- Inputs: two related nodes + one contested proposition. Outputs: two opposable stances.
- Algorithm (proposed): (1) state the proposition as a yes/no on a shared object; (2) for each node, derive its interest/criterion w.r.t. the object; (3) assign the stance that maximizes that node's criterion; (4) assert pair is opposable iff the two criteria conflict on the object (not merely differ).
- Rules/edge cases: adjacency alone (e.g. "aggregate lives-in bounded-context") is composition → NOT a valid tension; reject and re-pick. Failure mode: manufactured disagreement → A3 fail (reviewer catches).
- Acceptance: A3 — reviewer confirms genuine, proposition-grounded disagreement.

### TASK-D3 — ELO store + oracle-consensus (high)
- Purpose/decision: grade the debate via the staged ladder.
- Inputs: ≥3 judge votes over the debate; persona ratings. Outputs: `{outcome, confidence, layer_resolved}` + rating updates.
- Data/state: `RatingStore{rating[persona]=1000 init, K=24}`.
- Algorithm: L1 unanimous if agreement ≥0.9 → resolve; else L2 supermajority if mean-confidence ≥0.66 with text overlap → resolve; else L3 confidence×ELO-weighted argmax → resolve; else (<0.45) L4 human-flag. Then update ratings: winner +K(1−E), loser −K·E.
- Edge cases: tie → fall to next layer; all-disagree → human-flag. Failure mode: skipping L2/L3 (degenerate majority) → A4 fail.
- Acceptance: A4 — graded confidence, L2/L3 demonstrably executable.

## Smallest Working Units (manifest)

| SWU ID | Parent Task | Source Anchors | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation | Exec Owner | Handoff |
|---|---|---|---|---|---|---|---|---|---|
| SWU-TWU-001 | TASK-FIXTURE | DESIGN §3 C1 | none | fixtures/ddd-tower.{graph} | 3 nodes+2 edges, query works | A1 query example | run query, see nodes | subagent | seed DDD graph object |
| SWU-TWU-002 | TASK-D1 | SPEC FR-2 | 001 | persona schema file | schema fields present, stance required | A2 instance validates | validate one persona | subagent | implement D1 schema + 1 instance |
| SWU-TWU-003 | TASK-D2 | SPEC FR-3, DESIGN R-1 | 001,002 | stance-rule module | rule yields 2 opposable stances | A3 reviewer ok | reviewer check genuine tension | manual+subagent | implement D2 rule + reviewer gate |
| SWU-TWU-004 | TASK-DEBATE | DESIGN §3 C3 | 002,003 | debate adapter | 2 positions + axis emitted | positions on proposition | run robot-talks adapter | subagent | thin robot-talks adapter |
| SWU-TWU-005 | TASK-D3 | SPEC FR-5 | 004 | scorer module | graded confidence, L2/L3 run | A4 graded + layers executed | run on ≥3 votes | subagent | implement ELO+oracle-consensus |
| SWU-TWU-006 | TASK-VERIFY | SPEC acceptance | 001-005 | trace runner + report | end-to-end verdict graded | A1–A5 all pass | run full trace | manual | AUDIT/VERIFY exemption-eligible closure |

Expected SWU result shape: per plan.md `swu_id/result/receipt_kind/files_touched/validation/blockers/residue/reroute/handoff_note`.

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target |
|---|---|---|---|---|---|
| B-001 | TASK-D1 | persona `stance`/`criteria` field semantics open (what makes a defensible stance) | design | resolve in spellcraft design or decision-gate | before W1 |
| B-002 | TASK-D2 | the opposable-stance algorithm is proposed, not proven (R-1, the hardest risk) | design | prototype on DDD proposition; if it can't beat adjacency-composition, PIVOT | before W1 |
| B-003 | TASK-D3 | oracle-consensus thresholds (0.9/0.66/0.45) + K-factor are proposals | design | confirm values or run a small sweep | before W2 |
| B-004 | cross-task (sequencing) | Phase 0 MOGT evidence (E1→E2) must run before tower build commits (DEC-6) — de-risks reusing the owned-but-unproven MOGT decision layer | research operator | run MOGT experiments via experiment-harness | before W0 |

## Gate Checks

1. workPackGateStatus = block until B-001..B-003 resolved (they affect A2/A3/A4 acceptance).
2. Medium complexity: split task files recommended before parallel execution (current single-file is execution-ready for a single coordinator).
3. Layer mappings consistent with IMPLEMENTATION-LAYERING (all tasks L0).
4. Every non-exempt SWU has parent task, write scope, done criteria, acceptance evidence, validation — present.
5. TASK-VERIFY is closure-only (VERIFY) — SWU-exemption-eligible.

## Next route

**Phase 0 (do first, DEC-6 / B-004): run MOGT experiments for evidence.** Hand off to the MOGT project lifecycle / `experiment-harness` — run first-wave **E1 → E2** in `arcanum/research/mogt-agentic-conversation/experiments/` to upgrade claims C1–C4 off *insufficient evidence*. This de-risks reusing the owned MOGT decision layer.

**Phase 1 (after evidence): build the tower witness-unit.** Then `spellcraft` (design/install/validate the spell composing C1–C5), reusing a validated MOGT for the decision/action-selection layer. Within Phase 1, resolve B-002 first (the opposable-stance pivot/continue decision).

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-06-18 | Initial work-pack (invoke plan, witness unit L0) | invoke |
