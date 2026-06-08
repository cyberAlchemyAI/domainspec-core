# Stage 5 — Distill (x-ray the branch structure)

**Verdict: pass.** Research: no-research. Input: branch-evidence-mapper receipt + ontology-vault + GoldenQuill ontology DAG + DAG-AND-METRICS.md.

## Distilled unit

- **4 branches** [SB]: meaning (B1), system (B2), operational (B3), bridge (B4). ontology-vault's
  business≈meaning; GoldenQuill adds operational as first-class (run context → denominator semantics).
- **7 bridge edge types** [SB]: realized_by, depends_on, constrained_by, observed_by, tested_by, drifts_from, traced_to.
- **Layer map**: meaning→L-ont(+reg+dag+bi); system→L-dag(+reg+bi); operational→L-dag/L-reg/L-bi (run boundary = denominators); bridge→L-dag edges/L-bi feedback/L-reg constraints.
- **Client work**: cap factory + logistics examples per branch (mapper §3).
- **Drift detection**: bridge edges preserve both intent + observed behavior; promotion needs both-branch evidence.

Key insight (x-ray): the **operational branch is what makes metrics honest** — denominators are defined
inside a run context, so "stage ≠ outcome" (GQ-PR-L0-003) is a branch boundary, not just a rule.

Output unit → [ONTOLOGY-BRANCHES.md](../../../ONTOLOGY-BRANCHES.md).
