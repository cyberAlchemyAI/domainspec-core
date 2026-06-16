# Invoke Define: Lean Softmax And CAP2 Proof Program

## Objective

Create an execution-ready proof program for the two deferred formal lanes:

1. finite softmax coordinate derivative;
2. CAP2-v0 canonical definition and first fixed-load proof slice.

## Target Artifact

`research/projects/mars/papers/triton-top2-backward-kernel/formal/`

## Definitions

### Softmax Coordinate Derivative

The first softmax theorem should avoid a full Jacobian API. Use a coordinate-line theorem:

```text
softmaxCoord (coordLine z k h) i
```

differentiated at `h = 0`, where:

```text
softmaxDen z = sum_j exp(z j)
softmaxCoord z i = exp(z i) / softmaxDen z
basis k j = if j = k then 1 else 0
coordLine z k h j = z j + h * basis k j
```

Expected derivative:

```text
softmaxCoord z i * (indicator(i = k) - softmaxCoord z k)
```

### CAP2 Definition Freeze

The first CAP2 theorem should not start with calculus. It should freeze the CAP2-v0 definitions from the candidate spec/reference:

```text
capacity = 2.1 / E
over_j = sigmoid((load_j - capacity) / tau_cap)
Z'_tj = Z_tj - mu * over_j
s_tj = sum_{k != j} sigmoid((Z'_tj - Z'_tk) / tau_rank)
G_tj = sigmoid((s_tj - (E - 2 - 0.5)) / tau_gate)
P_tj = softmax(Z'_t)_j
B_tj = G_tj * P_tj
A_tj = B_tj / (epsilon + sum_k B_tk)
```

The load is fixed data in this proof program.

## Non-Goals

- Do not prove hard `Top2` differentiability.
- Do not prove Triton/CUDA implementation correctness.
- Do not claim CAP2 novelty.
- Do not prove dynamic-load gradients.
- Do not jump straight to a full CAP2 derivative before the definition file builds.

## Deliverables

- `INVOKE-DESIGN.md`
- `IMPLEMENTATION-LAYERING.md`
- `INVOKE-PLAN.md`
- `WORK-PACK.md`
- task contracts under `tasks/`
- wave contracts under `waves/`

## Template Selection

Selected shape: split work-pack plus implementation-layering companion.

Reason: this is medium-complexity domain-logic work with multiple theorem files, proof dependencies, and SWUs.

