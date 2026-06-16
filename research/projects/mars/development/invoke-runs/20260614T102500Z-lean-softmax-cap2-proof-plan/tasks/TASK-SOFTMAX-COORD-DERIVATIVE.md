# TASK-SOFTMAX-COORD-DERIVATIVE

Status: `blocked_after_foundation`

Layer: L1

## Purpose

Prove the finite softmax coordinate-direction derivative, or produce a precise blocker report if Mathlib calculus requires a different representation.

## Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`
- optional blocker report: `research/projects/mars/papers/triton-top2-backward-kernel/formal/SOFTMAX-COORDINATE-BLOCKER.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`

## Smallest Working Units

### SWU-LSP-003

Goal: prove coordinate-line support lemmas for `coordLine z k h`.

Expected details:

- value at `h = 0`;
- coordinate `k` perturbation behavior;
- denominator derivative support if useful.

Validation:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

### SWU-LSP-004

Goal: prove:

```text
d/dh softmaxCoord (coordLine z k h) i at h = 0
  = softmaxCoord z i * (indicator(i = k) - softmaxCoord z k)
```

Fallback: if blocked, create `SOFTMAX-COORDINATE-BLOCKER.md` with:

- exact theorem attempted;
- Mathlib API blocker;
- next smallest theorem.

Validation:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

or:

```bash
test -f research/projects/mars/papers/triton-top2-backward-kernel/formal/SOFTMAX-COORDINATE-BLOCKER.md
```

## Done Criteria

- Coordinate derivative theorem builds, or blocker report exists with exact next step.
- No claim says the whole relaxed router is formally proved.

## Completion Evidence

- Foundation file: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`
- Blocker report: `research/projects/mars/papers/triton-top2-backward-kernel/formal/SOFTMAX-COORDINATE-BLOCKER.md`
- Session result: `research/projects/mars/development/task-sessions/20260614T104000Z-task-softmax-coordinate-derivative/RESULT.md`
