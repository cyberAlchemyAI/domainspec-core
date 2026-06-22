---
node_type: correction
status: resolved
topic: owned-in-repo precedent re-check correcting the first Tower System taxonomy dispatch
dispatch_id: 2026-06-18-owned-in-repo-precedent-recheck
corrects: research/tower-system-taxonomy/findings.md
last_updated: 2026-06-18
---

# Precedent Re-Check — owned-in-repo correction

The first dispatch (`2026-06-18-tower-system-taxonomy`) **killed MOGT** and tagged several elements **net-new / external-precedent** because no searcher swept the repo's own research corpus (`arcanum/research/`). This re-check closes that gap. A found owner is never a kill (research-skill rule) — it relabels **build-from-owned** with a cited path.

## Root cause

The precedent skeptic checked **external** frameworks (OpenIE/NELL, robot-talks, the ELO literature); the structural explorer checked **installed capability** under `.claude/skills/`. The repo's **owned research corpus** — where MOGT, an executed debate dispatch, the AutoBayes tower, and the ontology-branching proof actually live — fell in the seam between "external precedent" and "installed skill" and was searched by neither. Double error: real owned artifacts mislabeled net-new, and one (MOGT) **killed outright on a fabricated definition** ("Mixture of Ground Truths") that was never sourced from its own `DEFINITIONS.md`.

## Fix (process)

The precedent gate must add a mandatory **owned-in-repo sweep**: before any KILL-tautological or GO-net-new verdict, search `arcanum/research/**` (definitions, formal-model, proof-report, tower, findings files) for the element. Owned ≠ proven — record the honest evidence tier (EXECUTED vs design-stage/schema-level).

## Re-verdict table

| element | prior verdict | corrected verdict | owner path | use-mode |
|---|---|---|---|---|
| **MOGT** — multi-objective per-action decision/selection policy (regimes heuristic/weighted_sum/pareto_guided/bargaining_guided; formal `E_t=(s_t,R_t,A_t,O_t,K_t,V_t,U_t,π,τ)`) | **KILL (tautological)** — on a fabricated definition | **REVERSED → REAL-OWNER.** Not tautological, not a peer of ELO/oracle-consensus. It is a **per-action selection policy** — a decision-policy *layer the L4 taxonomy lacked*; it was mis-slotted as a judgment-aggregator. `bargaining_guided` is the one regime touching L4-style role resolution. | `arcanum/research/mogt-agentic-conversation/` (DEFINITIONS.md MOGT-D1–D9; module-formulae/formal-runtime-definition.md) | **build-from-owned, design-stage/unproven** (all 4 claims insufficient evidence, 0 live runs). Reuse; never claim novel or empirical. |
| multi-objective **scoring engine** (5-dim objective vector, Pareto frontier, weighted-sum) | GO net-new, build-from-owned (external) | **RELABELED → REAL-OWNER (schema-level).** external-precedent → **OWN-PRIOR-WORK** | `arcanum/research/mogt-agentic-conversation/` (DEFINITIONS MOGT-D3/D5/D9) | build-from-owned, schema-level (no live runs) |
| multi-agent **debate** construction (A×B preserved dissent) | GO, reuse robot-talks | **RELABELED → REAL-OWNER, EXECUTED.** reuse-a-skill → **OWN-PRIOR-WORK (executed exemplar)** | `arcanum/research/dispatch-composition-attack/`; `observability-adaptation/` | build-from-owned, **executed** (strongest ownership in the set) |
| **distill-build / research-tower** construction (L0→L1→L2→distill) | GO build-from-owned (OpenIE/NELL, external) | **RELABELED → REAL-OWNER, EXECUTED.** external → **OWN-PRIOR-WORK (executed)** | `arcanum/research/autobayes/`; `monoidal-categories-multicategories/` | build-from-owned, **executed** |
| typed **ontology / knowledge graph** (static-markdown form, traceability + drift) | (implied net-new under "queryable graph") | **REAL-OWNER, EXECUTED — static form only.** TOPICAL-ONLY vs *runtime-queryable*. | `arcanum/research/proofs/ontology-vault-branching/` | build-from-owned, executed (static); runtime-queryable remains net-new |
| **persona-as-artifact** (stored/composable persona registry) | GO-conditional (novel) | **UNCHANGED → net-new.** No in-repo owner; MOGT roles + debate angles are *ephemeral*, not stored artifacts. | (none) | remains novel |
| **runtime-queryable graph** | GO net-new | **UNCHANGED → net-new.** Every in-repo graph is static markdown; no query engine. | (none) | remains net-new |
| **ELO / tournament / oracle-consensus** (judgment-aggregation) | the genuine L4 peers | **UNCHANGED → net-new.** No in-repo owner — and confirms MOGT lives in a *different layer*, so the prior KILL's premise (MOGT competing here) was false. | (none) | remains net-new |

## What changes in the taxonomy

1. **MOGT un-killed and re-filed.** It is not an L4 scoring mode. It introduces a **decision / action-selection policy layer** (how an individual agent picks its next move among answer/clarify/tool/consult/escalate/defer/refuse/stop), which the four-layer taxonomy did not have. ELO/oracle-consensus aggregate *judgments*; MOGT selects an *action*.
2. **Three elements flip from external/net-new to OWN-PRIOR-WORK:** the multi-objective scoring engine (schema-level), the debate construction method (executed), and the research-tower/distill construction method (executed). The Tower System should **reuse these owned artifacts**, not reinvent them.
3. **Three elements stay genuinely net-new:** persona-as-artifact, the runtime-queryable graph, and the ELO/oracle-consensus scoring family. These remain the real build risk (and align with the witness-unit's D1/D2/D3).

## Honest caveat (owned ≠ proven)

MOGT and the scoring engine are owned but **design-stage / schema-level with zero live runs** (per their own `MOGT-EVIDENCE-STATUS.md`). The debate, tower, and ontology proof carry **executed** evidence. Cite the tier, never inflate.
