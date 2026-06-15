# Invoke Plan: Softmax Coordinate Derivative Proof

Mode: `plan`

Phase status: `pass`

Complexity: `medium`

Reason: the proof crosses Mathlib calculus, finite sums, quotient calculus, algebraic normalization, and paper evidence synchronization.

## Execution Waves

1. `W0-CALCULUS-PRIMITIVES`
2. `W1-DENOMINATOR-DERIVATIVE`
3. `W2-QUOTIENT-DERIVATIVE`
4. `W3-NORMALIZATION-EVIDENCE`

## Task Order

1. `TASK-SCD-LINE-DERIVATIVE`
2. `TASK-SCD-NUMERATOR-DERIVATIVE`
3. `TASK-SCD-DENOMINATOR-DERIVATIVE`
4. `TASK-SCD-QUOTIENT-DERIVATIVE`
5. `TASK-SCD-ALGEBRA-COROLLARIES`
6. `TASK-SCD-PAPER-SYNC`

## Validation

Lean proof tasks:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

Evidence sync task:

```bash
rg -n "softmaxCoord_coordLine_hasDerivAt|EV-FORMAL|NC-|finite softmax" research/projects/mars/papers/triton-top2-backward-kernel
```

## Next Route

`task-session` to [WORK-PACK.md](/home/vrondelli/projects/domainspec-core/research/projects/mars/development/invoke-runs/20260614T142000Z-softmax-coordinate-derivative-proof-plan/WORK-PACK.md)
