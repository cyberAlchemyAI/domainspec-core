# TASK-PROOF-SOFTMAX: Softmax Derivative Feasibility

Status: `complete_feasibility_fallback`

## Purpose

Determine whether a small Mathlib-backed softmax derivative theorem can be added now.

## Write Scope

- Prefer `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxDerivative.lean`.
- If blocked, add `research/projects/mars/papers/triton-top2-backward-kernel/formal/SOFTMAX-PROOF-FEASIBILITY.md`.
- Update `formal/TritonTop2.lean` only if the Lean file builds.
- Update `formal/FORMAL-VALIDATION-REPORT.md`.

## Smallest Useful Work Unit

Define finite softmax with positive denominator and attempt the Jacobian identity:

`d p_i / d z_k = p_i * (indicator(i = k) - p_k)`

Scope it to the simplest finite index representation that builds in the existing Mathlib project.

## Validation

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

If using the feasibility fallback:

```bash
test -f research/projects/mars/papers/triton-top2-backward-kernel/formal/SOFTMAX-PROOF-FEASIBILITY.md
```

## Completion Criteria

- Either `lake build` passes with a theorem slice, or the feasibility report states the exact blocker and the next smallest theorem.
- No paper claim implies the whole router relaxation is formally proved by this theorem alone.

## Completion Evidence

- Feasibility report: `research/projects/mars/papers/triton-top2-backward-kernel/formal/SOFTMAX-PROOF-FEASIBILITY.md`
- Formal report: `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`
- Session result: `research/projects/mars/development/task-sessions/20260614T092000Z-task-proof-softmax/RESULT.md`
