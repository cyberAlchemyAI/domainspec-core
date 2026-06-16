# Refine Result: What It Would Take To Prove The Feasibility Lanes In Lean

Status: `strategy_proposal_ready`

## Short Answer

It is possible, but it is not a one-step proof task.

The softmax proof is a medium Lean/Mathlib calculus project. The CAP2 proof is a two-phase project: first freeze the formal CAP2-v0 definition, then prove derivative pieces. The current fixed-mask proof shows the environment and proof style are viable, but it does not remove the modeling work for softmax or CAP2.

## Lane A: Softmax Proof

### What It Would Take

1. Pick the Lean representation for logits.
   - Recommended first step: `Fin E -> ℝ`.
   - Avoid full matrix/Jacobian APIs at first.

2. Define:

```text
softmaxDen z = sum_j exp(z j)
softmaxCoord z i = exp(z i) / softmaxDen z
basis k j = if j = k then 1 else 0
coordLine z k h j = z j + h * basis k j
```

3. Prove denominator positivity:

```text
0 < softmaxDen z
```

4. Prove the coordinate-direction derivative:

```text
d/dh softmaxCoord (coordLine z k h) i at h = 0
  = softmaxCoord z i * (indicator(i = k) - softmaxCoord z k)
```

5. Only after that, decide whether to generalize to a full Jacobian theorem.

### Effort Estimate

Likely 2-5 focused sessions if we keep the theorem coordinate-direction first.
Likely more if we jump straight to a Fréchet derivative or Jacobian matrix theorem.

### Main Risks

- Picking a representation that makes Mathlib calculus painful.
- Spending time on generality before the useful theorem builds.
- Accidentally implying end-to-end router relaxation is proved.

## Lane B: CAP2 Proof

### What It Would Take

1. Freeze a canonical CAP2-v0 formal definition from the implementation evidence.

2. Decide which quantities are fixed data:
   - fixed load;
   - capacity adjustment;
   - pairwise soft-rank temperature;
   - normalized gated softmax denominator.

3. Split CAP2 into small Lean definitions:

```text
capacityAdjustedLogit
pairwiseSoftRank
sigmoidMembership
normalizedGatedSoftmax
fixedLoadPenalty
```

4. Prove one scalar theorem first, probably not the whole CAP2 derivative:

```text
if load is fixed data, fixedLoadPenalty contributes no derivative through load
```

or, after softmax proof exists:

```text
normalized gated softmax derivative reduces to softmax-style quotient pieces
```

5. Connect the local derivative piece back to the paper with explicit non-claims.

### Effort Estimate

Definition freeze: 1-2 sessions.

First scalar derivative theorem: 2-4 sessions after the definition is stable.

Full CAP2 calculus: likely larger, maybe 1-2 weeks of focused Lean work depending on how much of soft-rank/sigmoid/normalization is formalized.

### Main Risks

- CAP2 implementation and prose may not yet have a single canonical formula.
- Proving the wrong theorem could make the paper look more rigorous while not supporting the real claim.
- CAP2 derivative proof can easily drift into novelty/global-optimality claims, which the package must avoid.

## Recommended Proof Ladder

1. `SoftmaxCoordinateDerivative.lean`
   - coordinate-direction theorem only;
   - no CAP2 dependency.

2. `CAP2Definition.lean`
   - definitions and boundary lemmas only;
   - no derivative theorem yet.

3. `CAP2FixedLoadScalar.lean`
   - one scalar fixed-load derivative or non-derivative lemma.

4. Optional: `SoftmaxJacobian.lean`
   - only after coordinate theorem builds.

5. Optional: `CAP2NormalizedGateDerivative.lean`
   - only after softmax quotient pieces are stable.

## What Would Make This Paper Stronger

The highest-value next proof is not CAP2 first. It is the softmax coordinate derivative. That would move the paper from "router linear algebra is proved" to "a core smooth routing primitive is proved." Then CAP2 can reuse that instead of carrying too much proof burden at once.

## Recommended Next Route

Run `invoke define/design/plan` for a new proof work-pack:

```text
Lean softmax coordinate derivative first; CAP2 canonical definition second.
```

Then execute with `task-session` one theorem at a time.

