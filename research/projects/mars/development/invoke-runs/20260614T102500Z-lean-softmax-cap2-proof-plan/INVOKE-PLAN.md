# Invoke Plan: Lean Proof Execution

## Complexity

Medium.

Reason: multiple theorem files, Mathlib calculus, CAP2 definition alignment, and paper evidence synchronization.

## Execution Waves

1. `W0-SOFTMAX-FOUNDATION`: softmax definitions and denominator positivity.
2. `W1-SOFTMAX-DERIVATIVE`: coordinate-direction derivative theorem.
3. `W2-CAP2-DEFINITION`: canonical CAP2-v0 definitions and boundary lemmas.
4. `W3-CAP2-FIRST-SLICE`: first fixed-load CAP2 theorem.
5. `W4-PAPER-SYNC`: evidence, claim guards, and paper review.

## Task Order

1. `TASK-SOFTMAX-FOUNDATION`
2. `TASK-SOFTMAX-COORD-DERIVATIVE`
3. `TASK-CAP2-DEFINITION`
4. `TASK-CAP2-FIXED-LOAD-SCALAR`
5. `TASK-PAPER-SYNC`

## Validation

Every Lean task:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

Every paper sync task:

```bash
rg -n "softmaxCoord|CAP2Definition|dynamic load|novel|Top2|Lean" research/projects/mars/papers/triton-top2-backward-kernel
```

