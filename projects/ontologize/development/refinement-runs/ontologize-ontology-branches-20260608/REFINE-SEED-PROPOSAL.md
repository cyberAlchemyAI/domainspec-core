# REFINE-SEED-PROPOSAL — ontology branches

- Run id: `ontologize-ontology-branches-20260608`
- Target: ontologize design — explain all ontology branches and their interactions.
- Operator sentence: "we need to explain and add to the design all branches of the ontology and how
  they interact with the product and client work".

## Interpretation

Enumerate and define every ontology branch, then map each to (a) the four product layers
(L-ont / L-reg / L-dag / L-bi) and (b) client work (cap factory + logistics), including the
cross-branch bridge interactions and drift detection.

## Source context (local-first)

- `.claude/skills/ontology-vault/SKILL.md` + `arcanum/arcana/ontology-vault/README.md` — branch-aware
  ontology (business ↔ system, bridge edges, conventions).
- GoldenQuill ontology DAG on `master`:
  `projects/goldenquill/docs/strategy/goldenquill_ontology_dag_grant_research_synthesis_2026-06-01.md`
  - `..._findings_..._2026-06-01.md` — branches (meaning / system / operational / bridge).
- ontologize: DAG-AND-METRICS.md, DESIGN.md, DELIVERY-LANES.md.

## Write scope

- New: `projects/ontologize/ONTOLOGY-BRANCHES.md`.
- Tighten: DESIGN.md + DAG-AND-METRICS.md (reference the branch model).
- Run evidence under this folder. Sources read-only.

## Done criteria

1. Every branch enumerated + defined, traced to a source (ontology-vault and/or GoldenQuill ontology DAG).
2. Each branch mapped to the four product layers.
3. Each branch mapped to client work (cap factory + logistics manifestation).
4. Cross-branch bridge interactions + drift detection explained.
5. Candidate-tagged; no canonical promotion; no pricing/clients.

## Validation surface

- Each branch traces to a cited source path or is marked hypothesis.
- Dispatch route validates against the dispatch-spec validator.
- Final interrogation confirms branch×layer×client-work coverage is complete, not partial.

## Preset / research / subagents

- Preset: standard. Research: no-research. Subagents: recommended, **approved** — 1 branch-evidence-mapper.
  Join: parent_synthesis.
