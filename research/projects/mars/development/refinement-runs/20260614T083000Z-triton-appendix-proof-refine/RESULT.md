# Refine Run Strategy Proposal

- Target: `research/projects/mars/papers/triton-top2-backward-kernel/`
- Desired outcome: execution-ready non-executed plan for math appendix, next formal proofs, and paper reviewer pass
- Preset: `standard`
- Research: `research-if-gap-appears`
- Dispatch route: `research/projects/mars/development/refinement-runs/20260614T083000Z-triton-appendix-proof-refine/REFINE-DISPATCH.json`
- Selected overlays: baseline sequence, route menu for ambiguity, proof-lane SCU/SWU reduction, owner-boundary guardrails
- Subagent strategy: `recommended`
- Proposed subagents: `proof-scout`, `appendix-reader`, `skeptical-reviewer`
- Join policy: `parent_synthesis`
- Receipt requirements: native stage fields plus subagent lifecycle fields
- Runtime plan after confirmation: run `task-session` on the invoke work-pack; optionally spawn recommended role-bound subagents
- Deferred work: actual appendix writing, formal proof coding, and reviewer pass execution
- Confirmation prompt: Confirm before running the work-pack tasks or spawning subagents.

## Refined Recommendation

Execute the next phase in this order:

1. Write the math appendix first, because it makes the existing Mathlib proof
   understandable.
2. Add the fixed-mask full backward proof next, because it is the strongest
   achievable formal step directly tied to "exact backward."
3. Scope softmax derivative proof as a feasibility lane before committing to a
   full calculus proof.
4. Scope CAP2 fixed-load proof last, because it is higher risk and must not
   become an accidental novelty or full-CAP2 claim.
5. Run the skeptical paper review after the appendix and first formal proof
   land.

