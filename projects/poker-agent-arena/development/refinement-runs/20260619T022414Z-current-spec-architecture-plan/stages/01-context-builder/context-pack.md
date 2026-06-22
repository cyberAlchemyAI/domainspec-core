# Context Pack: Poker Agent Arena Current Spec, Architecture, And Plan

Status: pass
Owner: `context-builder` via parent Refine coordinator
Mode: `standard --strict --emit both --handoff runtime`

## Target

`projects/poker-agent-arena`

## Evidence Baseline

Root artifacts:

- `projects/poker-agent-arena/SPEC.md`: defines the local competition harness, M0/M1/M2 scope, primary contracts, acceptance gates, and open decisions.
- `projects/poker-agent-arena/GLOSSARY.md`: defines arena terms including observation allowlist, deterministic fallback, transcript replay, seed orbit, and hidden-information canary.
- `projects/poker-agent-arena/DESIGN.md`: sketches context, high-level components, protocol envelopes, fallback flow, transcript material, workflow, and dependency interface.
- `projects/poker-agent-arena/IMPLEMENTATION-LAYERING.md`: sequences L0 toy CLI contract, L1 Hold'em engine parity, L2 reliability leaderboard, and L3 novelty appendix.
- `projects/poker-agent-arena/WORK-PACK.md`: defines `WP-PAA-001`, `SWU-PAA-001` through `SWU-PAA-007`, and the next route as `task-session`.
- `projects/poker-agent-arena/INVOKE-RESULT.md`: records first-artifact status as `flag`, ready for L0 review but not runtime proof.

Prior dispatch evidence:

- `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/poker-agent-arena-mechanics.dispatch.json`
- `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/findings.md`
- `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/research.md`
- `projects/poker-agent-arena/development/dispatches/20260619-agent-arena-mechanics/subagent-run/REVIEW-REPAIR.md`

## Current Coherent Unit

The current artifact set already converges on one unit: an L0 toy-game-first CLI contract. It is not yet executable proof. Its next useful shape is a protocol/schema and fixture skeleton package that can be handed to `task-session` without silently selecting a Hold'em engine or enabling adjusted leaderboard scoring.

## Evidence Constraints

- Root artifacts are read-only for this Refine run.
- Prior dispatch evidence is read-only for this Refine run.
- Runtime implementation is out of scope.
- External research is not active unless a named gap appears and the operator confirms.

## Key Risks To Test

- Planning artifacts may be mistaken for runtime proof.
- The design names components but not concrete file/module ownership.
- The first SWU may still be too broad unless schema and fixture skeleton outputs are sharpened.
- Hidden-information boundaries are declared but need fixture-level proof.
- Deterministic fallback must be abuse-resistant, not merely legal.
