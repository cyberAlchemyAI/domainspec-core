# TASK-PROOF-CAP2: CAP2 Fixed-Load Derivative Feasibility

Status: `complete_feasibility_fallback`

## Purpose

Determine whether CAP2 fixed-load derivative pieces can be formalized without expanding the paper into a full routing-theory formalization.

## Write Scope

- Prefer `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/CAP2FixedLoadDerivative.lean`.
- If blocked, add `research/projects/mars/papers/triton-top2-backward-kernel/formal/CAP2-PROOF-FEASIBILITY.md`.
- Update `formal/TritonTop2.lean` only if the Lean file builds.
- Update `formal/FORMAL-VALIDATION-REPORT.md`.

## Smallest Useful Work Unit

Prove a fixed-load derivative identity for one CAP2 penalty component or one normalized membership factor. Do not attempt global capacity-constrained routing optimality.

## Validation

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

If using the feasibility fallback:

```bash
test -f research/projects/mars/papers/triton-top2-backward-kernel/formal/CAP2-PROOF-FEASIBILITY.md
```

## Completion Criteria

- Either `lake build` passes with a narrow theorem slice, or the feasibility report names the exact blocker.
- The paper still treats CAP2 as a scoped relaxation/penalty lane, not as a novelty claim.

## Completion Evidence

- Feasibility report: `research/projects/mars/papers/triton-top2-backward-kernel/formal/CAP2-PROOF-FEASIBILITY.md`
- Formal report: `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`
- Session result: `research/projects/mars/development/task-sessions/20260614T093000Z-task-proof-cap2/RESULT.md`
