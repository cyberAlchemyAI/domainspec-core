# Invoke Design: Softmax Coordinate Derivative Proof

Mode: `design`

Phase status: `pass`

## Context View

The current Lean file already defines finite softmax over `Fin E` and proves denominator positivity. The remaining work is a calculus proof along a one-coordinate line.

## High-Level Structure View

Add proof lemmas in the existing `TritonTop2.SoftmaxCoordinate` namespace, preferably inside the current file unless the proof grows enough to justify a companion file.

```text
coordLine derivative
  -> numerator exp derivative
  -> denominator sum derivative
  -> quotient derivative
  -> algebraic normalization
  -> optional corollaries
```

## Low-Level Components View

### Component 1: coordinate-line calculus

Purpose: prove the derivative of `fun h => coordLine z k h j`.

Expected derivative: `basis k j`.

### Component 2: numerator calculus

Purpose: compose coordinate-line derivative with `Real.exp`.

Expected derivative at `0`: `Real.exp (z i) * basis k i`.

### Component 3: denominator calculus

Purpose: move derivative through finite sum.

Expected derivative at `0`: `Real.exp (z k)`.

### Component 4: quotient calculus

Purpose: apply quotient rule to numerator over denominator.

Expected raw form:

```text
((Real.exp (z i) * basis k i) * softmaxDen z
  - Real.exp (z i) * Real.exp (z k)) / (softmaxDen z)^2
```

### Component 5: algebraic normalization

Purpose: rewrite the raw quotient derivative into:

```text
softmaxCoord z i * (basis k i - softmaxCoord z k)
```

## Workflow Process View

1. Execute `TASK-SCD-LINE-DERIVATIVE`.
2. Execute `TASK-SCD-NUMERATOR-DERIVATIVE`.
3. Execute `TASK-SCD-DENOMINATOR-DERIVATIVE`.
4. Execute `TASK-SCD-QUOTIENT-DERIVATIVE`.
5. Execute `TASK-SCD-ALGEBRA-COROLLARIES`.
6. Execute `TASK-SCD-PAPER-SYNC`.

## Decision Flow View

- If coordinate-line derivative fails because imports are insufficient, add the narrowest Mathlib calculus import.
- If finite-sum derivative fails, preserve numerator theorem and write a blocker if the exact theorem-shape cannot be found after bounded repair.
- If quotient simplification fails, keep a raw quotient theorem and move normalization to a separate task.
- If final theorem builds, sync paper evidence.

## Dependency Interface View

Source file:

- `formal/TritonTop2/SoftmaxCoordinate.lean`

Existing theorem dependencies:

- `coordLine_zero`
- `coordLine_self`
- `coordLine_of_ne`
- `softmaxDen_pos`
- `softmaxDen_ne_zero`
- `softmaxCoord_def`

Validation dependency:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

## Risks

- Mathlib theorem names may require search.
- Algebra normalization may be harder than the calculus theorem.
- A denominator theorem blocker should not erase successful line or numerator lemmas.
