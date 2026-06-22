# Distilled Knowledge

## One-Sentence Model

Ternary models compress weights into `{-1, 0, +1}` and only become operationally
valuable when training, scaling factors, activation handling, and inference
kernels are aligned.

## Compositional Spine

```text
ternary weight representation
  -> training or ternarization recipe
  -> scale/activation/accumulator handling
  -> storage and kernel implementation
  -> measured memory, latency, energy, quality trade-off
```

## What To Borrow

- The `{-1, 0, +1}` representation as the local anchor for ternary weights.
- The distinction between native low-bit training and post-training
  ternarization.
- The requirement that efficiency claims include hardware/runtime conditions.
- The systems insight that specialized kernels are part of the method, not an
  optional optimization.

## What To Keep Analogy-Only

- "1-bit" as a marketing phrase. Locally, prefer "ternary-weight" or
  "1.58-bit weight" when the source means three values.
- "Matches full precision" unless all source conditions are named.
- "Runs on CPU" as a universal feasibility claim.

## What To Block

- Claiming novelty for ternary weights.
- Treating source benchmark tables as local evidence.
- Promoting BitNet-specific terms into canonical architecture vocabulary before
  a separate governance decision.
