# TASK-CAP2-DEFINITION

Status: `complete`

Layer: L2

## Purpose

Freeze CAP2-v0 definitions in Lean so later derivative work has a canonical target.

## Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/CAP2Definition.lean`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2.lean`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`

## Source Contract

Definitions must match:

- `research/triton-top2-backward-kernel/CAP2-CANDIDATE-SPEC.md`
- `research/triton-top2-backward-kernel/CAP2-REFERENCE.md`
- `research/triton-top2-backward-kernel/reference/router_torch.py`

## Smallest Working Units

### SWU-LSP-005

Goal: add CAP2-v0 Lean definitions:

- `cap2Capacity`
- `cap2Overload`
- `cap2AdjustedLogit`
- `cap2PairwiseSoftRank`
- `cap2Membership`
- `cap2Gated`
- `cap2WeightDen`
- `cap2Weight`

Validation:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

### SWU-LSP-006

Goal: add fixed-load boundary lemmas:

- load is an explicit argument;
- dynamic load is outside this theorem lane;
- CAP2 definition is candidate-only and non-novelty.

Validation:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

## Done Criteria

- `CAP2Definition.lean` builds.
- Formal report names the definition file.
- No derivative claim is introduced by this definition-only task.

## Completion Evidence

- Lean file: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/CAP2Definition.lean`
- Build: `lake build` passed with 1911 jobs.
- Session result: `research/projects/mars/development/task-sessions/20260614T105000Z-task-cap2-definition/RESULT.md`
