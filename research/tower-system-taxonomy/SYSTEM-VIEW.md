---
node_type: system-view
status: design (honest evidence tiers per element)
topic: what the Tower System is architecturally — layers, flow, reuse, load-bearing stances
last_updated: 2026-06-19
companions: PRODUCT-VIEW.md, findings.md, PRECEDENT-RECHECK.md, witness-unit/
---

# Tower System — System View

> The shape-and-stakes view: the architecture explained one layer at a time, what is **given**
> vs **optimized**, the **reuse map** (owned prior work vs genuinely net-new), and the
> **load-bearing stances** that decide whether the whole thing stands. The story is in
> [PRODUCT-VIEW.md](PRODUCT-VIEW.md). Verdicts and evidence come from [findings.md](findings.md)
> and [PRECEDENT-RECHECK.md](PRECEDENT-RECHECK.md).

## 1. What the system is, in one sentence

A **substrate** (knowledge made traversable + inhabitable by personas) plus a small set of
**operations** that consume it (debate, dispatch, design, write, understand), governed by a
**decision policy** for how each agent acts and an **adjudication layer** for how their outputs
resolve. Two faces over one substrate: **learn** (build towers) and **apply** (consume them).

## 2. The layer stack (bottom-up, one layer at a time)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  L4  ADJUDICATION      how a multi-persona run resolves                    │
│        tension · scoring {oracle-consensus · ELO · tournament · synthesis} │
│        · verdict                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│  Lφ  DECISION POLICY   how ONE agent picks its next move within an op      │
│        MOGT: score actions × {quality,cost,latency,safety,escalation}      │
│        → regime {heuristic·weighted_sum·pareto·bargaining} → action        │
├──────────────────────────────────────────────────────────────────────────┤
│  L3  APPLICATION       what you DO with personas (each = 1 tensioned group)│
│        debate · dispatch · design · write · understand                     │
├──────────────────────────────────────────────────────────────────────────┤
│  L2  CONSTRUCTION      how a tower gets built (the "learn" methods)        │
│        distill-build · read-through · promote                              │
├──────────────────────────────────────────────────────────────────────────┤
│  L1  SUBSTRATE         what a tower IS                                      │
│        queryable knowledge graph  +  persona set                           │
└──────────────────────────────────────────────────────────────────────────┘
```

**L1 — Substrate.** A *tower* = a **queryable knowledge graph** (typed nodes + typed edges you
can walk, not prose) + a **persona set** (each persona anchored to a node, carrying a stance).
The persona is the bridge that turns inert knowledge into an actor. *(Note: "tower" as a layer
label collapses into "research-tower output" — the load-bearing new object here is the
queryable graph, not the word "tower". See findings R3.)*

**L2 — Construction (the learn face).** How a tower comes to exist: `distill-build` (agents read
sources and emit the tower), `read-through` (a human reads a source *through* the tower so it
accretes), `promote` (lift existing artifacts into the graph). The learning method *is* the
construction method.

**L3 — Application (the apply face).** What you do with the personas. The unifying primitive:
**every operation instantiates exactly one tensioned persona group.** Debate, subagent
dispatch, design review, writing, comprehension — same move, different operation. *(The label
"application" collapses into the constitution's existing "dispatch"; the real content is
"personas, not ephemeral angles" — findings R3.)*

**Lφ — Decision policy (MOGT).** *The layer the original taxonomy was missing.* Inside any
operation, an individual agent constantly chooses its next move — answer, clarify, call a tool,
consult, escalate, defer, refuse, stop. MOGT scores each candidate action across five
objectives (quality, cost, latency, safety, escalation-risk) and selects via a named regime.
This is **not** scoring/aggregation — it chooses an *action*, not a *winner*. Its
`bargaining_guided` regime is the one touch-point into L4.

**L4 — Adjudication.** How a multi-persona run resolves: **tension** (must be genuine, pairwise),
**scoring** (`oracle-consensus` staged ladder, `ELO`, `tournament`, `synthesis`), **verdict**
(GO/KILL-style object with graded confidence). This answers *"which position won, and how
sure?"* — a different question from Lφ's *"what move next?"*

## 3. Given vs optimized

| Layer / element | Given (the system obeys) | Optimized (the system improves) |
|---|---|---|
| The substrate shape (graph + personas) | **Given** — a tower always has these two parts | which nodes/personas a domain yields |
| Tension (L3/L4) | **Given, hard** — any n≥2 group must be genuinely opposed (constitution P5) | how sharply a pair is tensioned |
| Decision objectives (Lφ) | **Given dimensions** (the 5-vector) | the per-decision action choice |
| Scoring/verdict integrity (L4) | **Given** — owned never killed; claim ≤ proof; graded not vote-counted | which scoring mode fits a case |
| Policy regime (Lφ) / scoring mode (L4) | the **variables under study** | chosen per operation |
| Recursion (towers-in-towers) | **Given it's allowed**; **bounded** by cycle-guards + the three dials | depth per case |

## 4. Data flow (one operation, end to end)

```
build/seed tower ─► query graph ─► instantiate tensioned persona group (P_A,P_B,…)
        (L2)            (L1)                    (L3)
                                                 │
                         each agent's moves governed by ──► Lφ decision policy (MOGT)
                                                 │
                                                 ▼
                              tensioned exchange (debate / dispatch / …)
                                                 │
                                                 ▼
                              L4: tension → scoring → graded verdict
                                                 │
                  ┌──────────────────────────────┴───────────────┐
                  ▼                                               ▼
        recursion: an agent hits a gap → spins a sub-tower    rating update
        (bounded; cycle-guarded)                              (ELO persists, informs next run)
```

Two recursion sites, kept distinct: **construction recursion** (a domain tower *contains*
concept sub-towers — safe composition) and **application recursion** (an operation spawns a
tower mid-run — the dangerous one, bounded by `distill`'s cycle-guards and the constitution's
three dials).

## 5. Reuse map — the architecture is mostly owned prior work

The integration pattern is a **blackboard architecture** (shared substrate + specialist agents
read/write + an arbitration loop — Hearsay-II/BB1). Per [PRECEDENT-RECHECK.md](PRECEDENT-RECHECK.md):

| Layer / component | Owner | Tier |
|---|---|---|
| L1 tower content | `research-tower` skill; `autobayes`, `monoidal-categories` (in-repo) | **executed** (own prior work) |
| L2 distill-build | same towers above + `distill` | **executed** |
| L3 debate / dispatch | `robot-talks`; `dispatch-composition-attack`, `observability-adaptation`; subagents-strategy constitution | **executed** |
| Lφ decision policy + multi-objective scoring | `mogt-agentic-conversation` (MOGT) | **design-stage / unproven** (0 live runs) |
| L4 tension + aggregation + verdict schema | subagents-strategy constitution + `research` verdict matrix; `anti-bias-vector-composition` (tension *principle* only) | **executed** (governance) |
| **L1 persona-as-artifact** | — none — | **net-new** |
| **L1 runtime-queryable graph object** | — none (all in-repo graphs are static markdown) — | **net-new** |
| **L4 ELO / oracle-consensus scoring family** | — none in-repo — | **net-new** |

Read this as: the *skeleton* is owned and largely executed; the *three net-new pieces* are the
real build, and they map exactly to the witness unit's D1/D2/D3.

## 6. Component inventory (the five runtime components)

From [witness-unit/DESIGN.md](witness-unit/DESIGN.md), the minimal realization:

| Comp | Responsibility | Kind |
|---|---|---|
| C1 Tower-graph | typed nodes/edges + query surface | net-new object over owned content |
| C2 Persona-builder | D1 schema + D2 node→opposable-stance rule | **net-new sub-sigil** |
| C3 Debate-runner | adapter over robot-talks + human gate | reuse |
| C4 Scorer | ELO store + oracle-consensus ladder (D3) | **net-new sub-sigil** |
| C5 Verdict-emitter | graded verdict object | reuse |

C2 and C4 carry all the build risk; C1/C3/C5 are reuse or thin adapters.

## 7. Load-bearing stances (named, not yet decided)

These are the hinges — if any fails, the layer above it is hollow:

- **S1 (D1) — a persona is a real artifact, not a label.** It must carry `{anchor, stance,
  criteria, provenance}` — enough to *hold a position*. Distinct from the constitution's
  ephemeral `angle` by **graph-anchoring + stance, not persistence**. *Open.*
- **S2 (D2) — a graph node can be turned into a genuine disagreement.** Adjacency is
  *composition*, not *conflict*. The opposable-stance rule must manufacture real tension from
  (node, contested proposition). **This is the riskiest stance — it gates the whole debate
  layer.** *Open (the pivot/continue decision).*
- **S3 (D3) — scoring grades, not counts.** Oracle-consensus's middle layers (supermajority,
  ELO-weighted) must actually execute, or it degenerates to majority vote. *Open.*
- **S4 — MOGT is worth reusing.** Owned but unproven; **sequencing decision (DEC-6): run MOGT's
  experiments for evidence before the tower commits to it.** *Open, evidence-gated.*
- **S5 — recursion is bounded.** Towers-in-towers is the feature; the cycle-guard is what keeps
  it from being a footgun. *Given, mechanism reused from `distill`.*

## 8. Evidence boundary (the honest line)

- **Executed (proven the machinery runs in-repo):** tower construction, multi-agent debate with
  preserved tension, governance/verdict scaffolding.
- **Design-stage / unproven:** MOGT (decision policy + multi-objective scoring) — model + harness
  exist, zero live runs.
- **Net-new (no owner, the build):** persona-as-artifact, runtime-queryable graph, ELO/oracle-
  consensus scoring. Equivalent to the witness unit's D1/D2/D3.

The system **stands or falls on S2** (node→genuine-tension). Everything else is either owned or
mechanical; that one stance is where to point the first real experiment after MOGT evidence.

## 9. Where to go next

- Smallest proof of S1–S3: [witness-unit/](witness-unit/) (SPEC/DESIGN/WORK-PACK, L0).
- Foundation evidence first (S4): run MOGT E1→E2 (DEC-6) before tower build.
- Product narrative: [PRODUCT-VIEW.md](PRODUCT-VIEW.md).
