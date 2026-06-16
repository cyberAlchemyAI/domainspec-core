# TASK-SOFTMAX-FOUNDATION

Status: `complete`

Layer: L0

## Purpose

Add finite softmax definitions and denominator positivity in Lean.

## Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2.lean`

## Smallest Working Units

### SWU-LSP-001

Goal: create `SoftmaxCoordinate.lean` with definitions:

- `softmaxDen`
- `softmaxCoord`
- `basis`
- `coordLine`

Dependencies: none beyond current Lean package.

Validation:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

### SWU-LSP-002

Goal: prove denominator positivity, preferably:

```text
softmaxDen_pos : 0 < softmaxDen z
```

Dependencies: `SWU-LSP-001`.

Validation:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

## Done Criteria

- Softmax definitions build.
- Denominator positivity theorem builds.
- The file is imported from `TritonTop2.lean`.

## Handoff Note

Use `Fin E -> Real` first. Do not switch to a Jacobian/Frechet derivative model in this task.

## Completion Evidence

- Lean file: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`
- Build: `lake build` passed with 1911 jobs.
- Session result: `research/projects/mars/development/task-sessions/20260614T103000Z-task-softmax-foundation/RESULT.md`
