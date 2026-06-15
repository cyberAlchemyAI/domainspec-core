# Invoke Design - Mathlib Formal Hardening

Mode: `design`
Status: `pass`
Complexity: `medium`

## 1. Context View

The current paper package already has a Lean boundary slice. The user asked
whether Mathlib would improve paper standing, then requested define/design/plan
and execution of that hardening. The improvement should make a stronger
mechanized claim without expanding beyond the evidence boundary.

## 2. High-Level Structure View

Add one formal layer:

```text
Lean core boundary files
  + Mathlib dependency
  + real-valued router adjoint identities
  -> formal report update
  -> paper/review/claim guard update
```

## 3. Low-Level Components View

| Component | Change |
| --- | --- |
| `formal/lakefile.*` | Pin Mathlib `v4.30.0`. |
| `formal/TritonTop2/RealBackwardIdentities.lean` | Prove real finite-sum adjoint identities for dW and dX-router. |
| `formal/TritonTop2.lean` | Import the new theorem module. |
| `formal/FORMAL-VALIDATION-REPORT.md` | Distinguish reducer boundary proofs from Mathlib real-valued theorems. |
| `paper.md` and review artifacts | State stronger formal support without overclaiming. |

## 4. Workflow Process View

1. Verify Mathlib tag and current Lean toolchain.
2. Convert the Lake project to a Mathlib-enabled configuration.
3. Add the real-valued theorem module.
4. Build and repair Lean errors until clean.
5. Update paper/report/review artifacts.
6. Record validation receipt.

## 5. Decision Flow View

| Question | Decision |
| --- | --- |
| Should Mathlib be added just for prestige? | No. It must support specific theorems. |
| Should the first hardening target CAP2 calculus? | No. Start with router linear adjoint identities. |
| Should the formal report imply Triton proof? | No. It remains empirical/test-backed for implementation. |

## 6. Dependency Interface View

| Dependency | Interface | Risk |
| --- | --- | --- |
| Mathlib `v4.30.0` | Lake dependency from `leanprover-community/mathlib4`. | Network/cache required for first build. |
| Lean 4.30.0 | `lean-toolchain`. | Version mismatch would block build. |
| Paper package | Markdown updates. | Must preserve non-claim boundaries. |

## Risks

- Mathlib fetch/build may be slow on first run.
- Sum-rearrangement theorem syntax may need iteration.
- Stronger formal language could accidentally imply full CAP2 proof.

## Next Route

`invoke plan` with one executable work-pack and SWUs.

