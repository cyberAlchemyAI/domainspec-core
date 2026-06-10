# autoads

A creative-development pipeline that **generates better ad creatives by measuring ad-network outcomes**,
built as a new vertical of the [`ontologize`](../ontologize/) ontology + DAG governed learning loop.

## Status

- **Phase:** project seed authored and validated. **Not yet executed.**
- **Origin:** refine run [`autoads-seed-20260610`](development/refinement-runs/autoads-seed-20260610/)
  — dispatch validated `pass`; 4-role design fanout; all stages pass/flag (no blocks).
- Outputs are **candidates** pending owner decision. No live ad-network calls, credentials, PII, pricing,
  or named clients. ontologize and GoldenQuill are read-only precedent.

## The idea (one sentence)

autoads installs the ontologize ontology+DAG learning loop over ad-creative production: ad-network
outcomes become governed **events**, the promotion DAG decides which creatives/patterns are trustworthy,
and an auto-research stage proposes the next governed creative candidates.

## The loop — the Creative Learning Cycle

```
Auto-Research --candidate--> Generator --variant--> Network Adapter --outcomes-->
  Measurement --KPI(veracidade)--> Grader --> Promotion DAG --owner decision-->
  {promote | retire} --> Feedback --> (re-parameterizes Generator + Auto-Research memory)
```

## Seed artifacts

- [DEFINE.md](DEFINE.md) — what autoads is, the problem, the unit of value, the ontologize binding.
- [DESIGN.md](DESIGN.md) — pipeline architecture, components, tournament resolutions, data governance.
- [PLAN.md](PLAN.md) — layered non-executed MVP plan with a thin first slice and acceptance gates.
- [development/refinement-runs/autoads-seed-20260610/](development/refinement-runs/autoads-seed-20260610/)
  — full refine evidence (dispatch, stages, subagent receipts, result).

## Next routes

1. `bounded-research` on one target ad network's outcome API + attribution model.
2. `task-session` on PLAN Layer 0 (thin-slice MWU proof, stub adapter, no live spend).
