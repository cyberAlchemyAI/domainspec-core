---
doc_type: refine-seed
run_id: 20260615T132005Z-goal-spec-architecture-first
target: ops/development
status: strategy-proposed
updated_at: 2026-06-15
---

# Refine Seed Proposal: Goal Spec Architecture First

## Target

Create an architecture-first goal-spec package for the current DomainSpec Core
ops lane, using `ops/development` as the target-local evidence surface.

## Operator Intent

We need to create the goal spec, architecture first.

## Desired Outcome

Produce a governed, non-executed architecture-first goal-spec plan that can
later be projected into a native Codex goal profile only after the architecture,
selected SWU or work-pack unit, strict context pack, verification surface, and
owner boundaries are explicit.

## Source Context

Primary local evidence:

- `ops/development/NEXT-STEPS.md`
- `ops/development/REFINE-SYNTHESIS-AGENT-ARCHITECTURE.md`
- `ops/development/INVOKE-DESIGN-AGENT-ARCHITECTURE.md`
- `ops/development/INVOKE-PLAN-AGENT-ARCHITECTURE.md`
- `CLAUDE.md`
- `AGENTS.md`
- `SUBMODULE-DISCIPLINE.md`
- `.agents/skills/refine/SKILL.md`
- `.agents/skills/dispatch-spec/SKILL.md`
- `.agents/skills/codex-goal-profile/SKILL.md`

## Write Scope

Allowed before operator confirmation:

- `ops/development/refinement-runs/20260615T132005Z-goal-spec-architecture-first/**`

Deferred until a later approved runtime route:

- root `tools/**`
- root policy documents
- `implementation/domainspec/**`
- `domainspec-lean-formalization/**`
- `arcanum/**`
- generated runtime mirrors
- machine-global Codex home

## Done Criteria

- Refine seed and Dispatch Spec route exist.
- Dispatch route preserves the ten-stage Refine loop.
- Dispatch validates against the repository-local Dispatch Spec validator.
- The strategy preview names the architecture-first route and rejects immediate
  runnable goal projection as premature.
- Runtime-backed stages and subagents are blocked until operator confirmation.
- The eventual plan can identify whether the next route is `codex-goal-profile`,
  `invoke plan`, `task-session`, or a blocker decision.

## Validation Surface

```bash
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py \
  ops/development/refinement-runs/20260615T132005Z-goal-spec-architecture-first/REFINE-DISPATCH.json
```

## Preset

`standard`

## Research Mode

`research-if-gap-appears`

Start with local repository evidence. External research is blocked unless a
named external-context gap appears during Interrogation or Distill and the
operator confirms that research pass.

## Planned Stage Configuration

1. Context Builder evidence baseline: standard, strict, runtime handoff pack.
2. Invoke Define: define the architecture-first goal-spec target.
3. Interrogation refine-review: test ambiguity, owner boundaries, and goal readiness.
4. Research decision: record local-first decision and named-gap trigger.
5. Distill: select the coherent architecture unit.
6. Invoke Redefine / Design: design the architecture-first goal-spec package.
7. Interrogation refine-design-review: review design readiness.
8. Distill Repair: repair selected unit and projection boundary.
9. Invoke Plan: author the non-executed goal-spec work-pack plan.
10. Final Interrogation and Synthesis: decide whether `codex-goal-profile` is ready next.

## Route Decision

Selected route: `architecture-first-goal-spec`.

Rejected route: `immediate-native-goal-profile`.

Reason: `codex-goal-profile` requires a selected work-pack task or SWU, strict
handoff pack, verification surface, and blocker state. Those must be produced
by the architecture-first refinement before a runnable native goal can be safe.
