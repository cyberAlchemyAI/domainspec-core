---
title: GoldenQuill Production Readiness Refine Run Manifest
date: 2026-05-31
mode: refine-full
target: goldenquill-production-readiness
status: materialized-with-runtime-block
---

# Run Manifest

## Intent

Refine the repository research package into a production-readiness path for GoldenQuill/Tilth, then feed the result into a residuality spec, experiment plan, and invoke design bundle.

## Scope

In scope:

- Production-readiness design for the repository surface already researched on 2026-05-29.
- Current-truth refresh, product surface indexing, implementation status, verification parity, and security/provisioning checks.
- Path-cited design artifacts and experiments.

Out of scope:

- Editing LOCKed architecture text.
- Editing client org contexts.
- Reading any org `PROJECT_CONTEXT.md`; no org was named.
- Implementing the improvement candidates in this run.
- Claiming full runtime-backed model execution for refine/invoke stages.

## Source Inputs

- `docs/strategy/goldenquill_repository_research_strategy_2026-05-29.md`
- `docs/strategy/goldenquill_repository_research_strategy_2026-05-29.dispatch.json`
- `docs/strategy/goldenquill_repository_research_synthesis_2026-05-29.md`
- `docs/strategy/goldenquill_repository_improvement_candidates_2026-05-29.md`
- `docs/strategy/goldenquill_repository_new_improvement_candidates_2026-05-29.md`
- `docs/strategy/goldenquill_repository_research_validation_2026-05-29.md`
- `SOUL.md`
- `USER.md`
- `router.yaml`

## Runtime Surface Check

Resolved command surfaces:

- `refine` resolves to `.codex/commands/refine.md`.
- `invoke` resolves to `.codex/commands/invoke.md`.

Runtime note: this run materializes the refine-full artifact contract locally. It does not claim nested Codex/runtime-backed lifecycle execution. That boundary is recorded as a runtime block, not hidden.

## Outputs

- `evidence-index.json`
- `REFINE-SEED-PROPOSAL.md`
- `REFINE-DISPATCH.json`
- `RUNTIME-HANDOFF.md`
- `RESULT.md`
- `stages/01-context-baseline.md`
- `stages/02-define-frame.md`
- `stages/03-refine-review.md`
- `stages/04-research-decision.md`
- `stages/05-distill.md`
- `stages/06-invoke-design-input.md`
- `stages/07-design-review.md`
- `stages/08-distill-repair.md`
- `stages/09-plan-readiness.md`
- `stages/10-final-synthesis.md`

## Completion Criteria

- The refinement names what must be true before production implementation starts.
- The residuality spec identifies stressors, residues, degradation behavior, and attractors.
- Experiments are measurable and linked to candidate improvements.
- The invoke design has context, high-level structure, low-level components, workflow process, decision flow, and dependency/interface views.
- Dispatch JSON validates against the dispatch-spec validator.

