# Lean Validation Design - Triton Top2 Paper Package

Status: `refresh-added`

## Purpose

Add a formal-validation lane to the paper package so the paper can distinguish:

- mathematical boundary claims that can be formalized;
- implementation claims validated by tests and RunPod;
- non-claims that must not be presented as theorems.

Lean is useful here as a claim-boundary tool, not as a replacement for PyTorch,
Triton, benchmark, or FP16 validation.

## Local Tooling Finding

The local machine already has Lean tooling available:

```text
lean 4.30.0
lake 5.0.0-src+d024af0
elan 4.2.2
```

So the execution plan should verify and pin tooling, then scaffold a repo-owned
Lake project. It should not begin by assuming Lean is absent.

## Output Location

Lean paper artifacts should live under:

```text
research/projects/mars/papers/triton-top2-backward-kernel/formal/
```

Planned files:

- `lean-toolchain`
- `lakefile.toml`
- `TritonTop2/FormalBoundary.lean`
- `TritonTop2/FixedLoadCAP2.lean`
- `TritonTop2/RouterAlgebra.lean`
- `FORMAL-VALIDATION-REPORT.md`

## Formal Scope

Paper-useful Lean targets:

1. encode finite index types for token, expert, and dimension axes;
2. encode fixed-mask and fixed-load assumptions as data;
3. encode algebraic definitions for logits and router reductions;
4. formalize simple linear-gradient identities such as:
   - `dW = dZ^T @ X` as a finite-sum algebra target;
   - `dX_router = dZ @ W` as a finite-sum algebra target;
   - auxiliary fixed-`f` contribution shape;
5. formalize non-theorem boundaries:
   - hard Top2 selection is not differentiated;
   - Triton memory behavior is outside Lean scope;
   - FP16 numerical behavior is outside Lean scope.

## Initial Proof Strategy

Start with theorem stubs plus one or two small finite-sum proofs. Prefer:

- PO-005 router weight gradient algebra;
- PO-006 router input gradient algebra;
- PO-004 auxiliary fixed-load/fixed-`f` term.

Defer full real-analysis softmax derivative proofs unless the Lean setup and
finite-sum layer are stable.

## Paper Integration

The paper should include a "Formal Boundary Validation" section only after
`FORMAL-VALIDATION-REPORT.md` exists. The paper may say Lean helped pin the
formal boundary, but should not claim Lean proved the Triton implementation.

