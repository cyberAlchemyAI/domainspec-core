# Refine Seed Proposal — autoads

- **Run id:** `autoads-seed-20260610`
- **Target:** new project `projects/autoads/` (greenfield seed inside `domainspec-core`)
- **Operator sentence:** "create a project seed inside domainspec core called autoads; it uses
  `projects/ontologize/` and auto research and a creative development pipeline that creates better
  creatives, by measuring outcomes from ad networks."

## Source context

- **`projects/ontologize/`** — the method substrate. Provides: the two-axis ontology (subject/segment ×
  value-mechanism), the signed field→authority-class **data-governance register** (fail-closed routing),
  the **promotion DAG** (events → evidence → candidate → review gates → owner decision → promoted/retired,
  11-rule L0 validator), and **evidence-linked KPI families** with `veracidade` grades + `evidence_refs`.
  See `PRODUCT.md`, `DAG-AND-METRICS.md`, `OPTIMIZATION-CHAIN-METHOD.md`.
- **GoldenQuill** (read-only via ontologize) — the reference implementation of the ontology+DAG loop.
- No live ad-network integration, no real campaign data, no pricing/clients are in scope.

## Write scope

- Create only under `projects/autoads/`. Read-only on `projects/ontologize/`, `projects/goldenquill/`,
  and `arcanum/`. No submodule mutation. No external network calls.

## Done criteria

A seed that a future Task Session can pick up, containing:

1. **DEFINE** — what autoads is, the problem, the unit of value, the ontology binding to ontologize.
2. **DESIGN** — the creative-development pipeline architecture: generation → ad-network dispatch →
   outcome measurement → DAG promotion → improved next-gen creatives; plus the auto-research component
   and the ad-network data-governance posture.
3. **PLAN** — a non-executed, MVP-scoped implementation plan with a thin first slice
   (one network × one creative family × one learning loop) and acceptance gates.

## Validation surface

- `REFINE-DISPATCH.json` validates `pass` against `dispatch-spec`.
- Each canonical stage records a native receipt or a blocked reason.
- 4 design subagent receipts collected before synthesis.
- Every product claim labeled `[SB]` source-backed (path), `[adapt]` adaptation, or `[H]` hypothesis.

## Preset, research, subagents (operator-confirmed)

- **Preset:** `full`
- **Research mode:** `research-if-gap-appears`
- **Subagent strategy:** `approved` — 4 role-bound design agents (ontology-reuse, creative-pipeline,
  ad-network-measurement, auto-research).

## Planned stage configuration

| # | Stage | Capability | Mode |
|---|-------|-----------|------|
| 1 | Context Builder baseline | `context-builder` | standard |
| 2 | Invoke Define | `invoke` | define |
| 3 | Interrogation | `interrogation` | refine-review |
| 4 | Research decision | `refine` | research-if-gap-appears |
| 5 | Distill | `distill` | standard |
| 6 | Invoke Redefine/Design | `invoke` | design (+ 4 subagents, fanout) |
| 7 | Interrogation | `interrogation` | refine-design-review |
| 8 | Distill Repair | `distill` | validate |
| 9 | Invoke Plan | `invoke` | plan |
| 10 | Final Interrogation + Synthesis | `interrogation`→`refine` | refine-final |
