# REFINE-SEED-PROPOSAL — ontologize DAG & metrics

- Run id: `ontologize-dag-metrics-20260608`
- Target: the DAG-and-metrics dimension of `projects/ontologize` (currently abstract in DESIGN/PLAN).
- Operator sentence: "improve this — it's not saying how we structure the DAG, which metrics, the
  events for updating the DAG, which metrics we track, and how we improve it over time; we already
  have a lot of work done there we can reuse."

## Source context (reused, local-first)

- GoldenQuill promotion-record DAG implementation on **master**:
  `projects/goldenquill/pipeline/grant_dag/validate.py` — 5 node types + 11 deterministic rules.
- `projects/goldenquill/docs/strategy/goldenquill_promotion_governance_architecture_design_2026-06-01.md`
  (master) — execution DAG + ontology DAG, six views.
- `projects/goldenquill/docs/client-packages/.../evidence_and_kpi_appendix.md` — KPI families.
- Our prior extraction: `projects/ontologize/sessions/pattern-extraction-receipts.md`.

> Provenance note: the concrete `grant_dag` code lives on `master`, not on the current
> `codex/goldenquill-client-package` branch. It is internal, source-backed evidence read via git.

## Write scope

- New: `projects/ontologize/DAG-AND-METRICS.md` (the concrete design deliverable).
- Tighten: `projects/ontologize/DESIGN.md` (View 5), `projects/ontologize/PLAN.md` (IDS-2/IDS-3).
- Run evidence under this folder. GoldenQuill stays read-only.

## Done criteria

1. DAG node + edge types specified (generic + per-vertical instantiation).
2. Event model: which real events update the DAG.
3. Metric families/KPIs specified, adapted from GoldenQuill, each evidence-linked.
4. Improve-over-time loop specified (candidate → owner decision → promoted lesson → feedback).
5. All claims candidate-tagged; no canonical promotion; no pricing/clients.

## Validation surface

- Each node/edge/event/metric traces to a GoldenQuill source or is marked hypothesis.
- Dispatch route validates against the dispatch-spec validator.
- Final interrogation confirms the four "done criteria" are concretely answered, not restated.

## Preset / research / subagents

- Preset: standard. Research: no-research (local, includes master branch). Subagents: none.
