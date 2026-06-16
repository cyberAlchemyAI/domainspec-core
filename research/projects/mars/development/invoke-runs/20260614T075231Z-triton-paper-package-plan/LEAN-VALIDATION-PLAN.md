# Lean Validation Plan - Triton Top2 Paper Package

Status: `ready-for-task-session`

## Objective

Create a small Lean/Lake project inside the Mars paper package and use it to
validate the mathematical claim boundary for the Triton Top2 paper.

## Task Slice

### TASK-TTP-005L - Lean Setup And Formal Scope

Goal: verify local Lean tooling, scaffold a repo-owned Lake project, and write
the formal scope document/report skeleton.

Validation:

```sh
lean --version
lake --version
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

### TASK-TTP-005M - Lean Boundary Proof Slice

Goal: encode the fixed-mask/fixed-load boundary and prove or stub the first
small router algebra obligations.

Recommended first targets:

- finite-sum shape of `dW = dZ^T @ X`;
- finite-sum shape of `dX_router = dZ @ W`;
- fixed auxiliary contribution boundary;
- non-theorem declarations in prose, not fake theorem claims.

Validation:

```sh
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
test -f FORMAL-VALIDATION-REPORT.md
```

## Done Criteria

- Lean/Lake project builds locally.
- Formal validation report says exactly what Lean proved, stubbed, or deferred.
- Paper work treats Lean as formal boundary evidence, not implementation proof.

## Next Route

Run after `TASK-TTP-005` and before `TASK-TTP-006`.

