# TASK-CAP2-FIXED-LOAD-SCALAR

Status: `complete`

Layer: L3

## Purpose

Prove one fixed-load CAP2 theorem slice, or produce a precise blocker report if the first theorem needs a smaller statement.

## Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/CAP2FixedLoadScalar.lean`
- optional blocker report: `research/projects/mars/papers/triton-top2-backward-kernel/formal/CAP2-FIXED-LOAD-SCALAR-BLOCKER.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2.lean`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`

## Smallest Working Unit

### SWU-LSP-007

Goal: prove a first fixed-load theorem, preferably one of:

- capacity/load pressure is constant along a coordinate-logit perturbation when load is fixed;
- CAP2 adjusted logit derivative with respect to raw logit is identity under fixed load;
- CAP2 fixed-load boundary theorem that blocks dynamic-load interpretation.

Validation:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

Fallback:

```bash
test -f research/projects/mars/papers/triton-top2-backward-kernel/formal/CAP2-FIXED-LOAD-SCALAR-BLOCKER.md
```

## Done Criteria

- A theorem slice builds, or blocker report states the exact next theorem.
- No text implies CAP2 novelty, global routing optimality, or dynamic-load gradients.

## Completion Evidence

- Lean file: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/CAP2FixedLoadScalar.lean`
- Build: `lake build` passed with 1911 jobs.
- Session result: `research/projects/mars/development/task-sessions/20260614T110000Z-task-cap2-fixed-load-scalar/RESULT.md`
