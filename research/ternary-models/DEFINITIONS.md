# Definitions

## Definition: Ternary Weight

Status: local-research-only

Source meaning: a learned model weight constrained or mapped into one of three
values, usually `-1`, `0`, or `+1`.

Source kind: primary-source plus local-inference

Evidence: S1, S4, S5 in `sources/source-record.md`.

Formal shape:

```text
w in {-1, 0, +1}
```

Intuition: the model keeps direction and a zero/sparsity option while discarding
continuous magnitude, usually recovering magnitude through scale factors or
training adaptation.

Misuse warning: a ternary weight is not automatically a ternary computation. The
runtime may still use higher-precision activations, accumulators, scales, or
dequantization.

## Definition: Native Ternary LLM

Status: local-research-only

Source meaning: an LLM trained with a ternary-weight architecture/recipe rather
than only compressed after full-precision training.

Source kind: primary-source

Evidence: S1 and S2.

Formal shape:

```text
Transformer-like architecture + BitLinear/ternary weight path + low-bit-aware training recipe
```

Intuition: the low-bit representation is not an export format; it is part of the
learning system.

Misuse warning: native ternary training does not remove the need to measure
accuracy, data quality, activation precision, and hardware-specific kernels.

## Definition: Source-Reported Efficiency Claim

Status: local-research-only

Source meaning: a latency, memory, throughput, or energy claim stated by a paper
or implementation source.

Source kind: local-inference

Evidence: S1, S2, S6, R1.

Formal shape:

```text
claim := metric + benchmark setting + hardware/runtime + source citation
```

Intuition: efficiency claims travel with their test conditions.

Misuse warning: do not convert source-reported efficiency into a repo promise
until measured in our own environment.
