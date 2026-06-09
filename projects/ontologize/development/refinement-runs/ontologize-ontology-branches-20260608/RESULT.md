# RESULT — ontology branches refinement

- Run id: `ontologize-ontology-branches-20260608`
- Status: **pass**
- Preset: standard · Research: no-research · Subagents: recommended, **approved** (1, completed+closed)

## What changed

Added [ONTOLOGY-BRANCHES.md](../../../ONTOLOGY-BRANCHES.md): the ontology is now explained as a **4-branch
model** with explicit product-layer and client-work interactions.

- **Branches [SB]:** B1 meaning (business/intent) · B2 system (implementation/runtime) · B3 operational
  (run context — first-class) · B4 bridge (cross-branch evidence/drift). Reconciles ontology-vault
  (business/system/bridge) with GoldenQuill's ontology DAG (meaning/system/operational/bridge).
- **7 bridge edge types:** realized_by, depends_on, constrained_by, observed_by, tested_by, drifts_from, traced_to.
- **Branch → product layer** map (each branch × L-ont/L-reg/L-dag/L-bi).
- **Branch → client work** map (cap factory + logistics example per branch).
- **Drift detection**: the improve-over-time loop is a walk across branches; promotion needs evidence
  from both branches; drift edges preserve intent AND observed behavior (no silent smoothing).

## Key insight

The **operational branch is what makes metrics honest** — denominators are defined inside a run
context, so "stage ≠ outcome" and denominator semantics are really a _branch boundary_, not just a
lint rule. This is also why GoldenQuill made operational first-class.

## Stage evidence

Ten canonical stages; one branch-evidence-mapper subagent (spawned→completed→closed,
[stages/04](stages/04-branch-evidence-mapper-receipt.md)). define pass → review flag (3 gaps) →
no-research → distill pass → redesign pass (ONTOLOGY-BRANCHES.md) → design-review flag (2) → repair
pass → plan deltas pass → final synthesis pass.

## Plan deltas applied

DESIGN.md View 1b (ontology branches); DAG-AND-METRICS.md (two DAGs sit across the 4 branches);
assessment (PLAN S1 / WORK-PACK T1) now populates B1, identifies B2 sources, defines B3 run boundary.

## Residue (deferred)

- B3 run boundary for cap factory (lot vs order) — assessment.
- Per-vertical event catalog + proof metric — assessment.
- Card runtime concept-graphing dormant upstream in GoldenQuill (not ours).

## Recommended next routes

- `task-session` → WORK-PACK T1 (assessment now populates the four branches per client).
- Optional `feature-glossary` to fold branch terms into GLOSSARY (candidate only).
