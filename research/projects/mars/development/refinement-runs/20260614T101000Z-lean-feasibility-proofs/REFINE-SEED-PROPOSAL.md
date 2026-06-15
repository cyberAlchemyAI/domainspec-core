# Refine Seed Proposal: Lean Feasibility Proofs

## Target

Turn the existing feasibility reports into an executable proof roadmap:

- `SOFTMAX-PROOF-FEASIBILITY.md`
- `CAP2-PROOF-FEASIBILITY.md`

## Desired Outcome

A non-executed design and plan that says what it would take to prove the deferred claims in Lean, how much effort/risk to expect, and what the smallest next theorem should be.

## Current State

Lean and Mathlib are installed and working. The package builds, and the fixed-mask proof already passed:

- `fixedMaskDW_adjoint`
- `fixedMaskDXRouter_adjoint`
- `fixedMask_is_data_not_selection_gradient`

The remaining feasibility reports are not blocked by tooling. They are blocked by formal modeling choices.

## Refined Scope

### Lane A: Softmax Calculus

Goal: prove the finite softmax coordinate derivative.

Required modeling choices:

- representation of logits;
- theorem shape: coordinate-direction derivative first, then optional Jacobian;
- denominator positivity package;
- bridge back to router logits without claiming end-to-end relaxed-router proof.

### Lane B: CAP2 Definition And Calculus

Goal: freeze a canonical CAP2-v0 formal definition before proving derivative pieces.

Required modeling choices:

- canonical CAP2-v0 formula aligned with implementation evidence;
- fixed-load versus differentiable-load boundary;
- scalar theorem target;
- relation to softmax/pairwise soft-rank primitives;
- explicit non-novelty and non-global-optimality guards.

## Done Criteria For This Refinement

- Produce a strategy that distinguishes softmax proof work from CAP2 definition work.
- Name the smallest next theorem for each lane.
- Identify effort, dependencies, risks, and validation commands.
- Recommend a next `invoke` or `task-session` route only after the strategy is clear.

