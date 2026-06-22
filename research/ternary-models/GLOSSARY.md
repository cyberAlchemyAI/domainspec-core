# Glossary

## Ternary Model

- Source kind: local-inference
- Local meaning: a model whose important learned weights are represented with
  three values, usually `{-1, 0, +1}`.
- Arcanum reading: a compressed model form where "zero" is an active design
  choice, not just a missing number.
- Promotion status: local-only
- Misuse warning: do not use this as a claim that all operations are ternary or
  all hardware speedups are automatic.
- Evidence: S1, S3, S4, S5 in `sources/source-record.md`.

## BitNet b1.58

- Source kind: primary-source
- Local meaning: a 1-bit LLM variant where weights are ternary `{-1, 0, 1}`.
- Arcanum reading: a native low-bit recipe, not merely post-training
  compression of a finished full-precision model.
- Promotion status: local-only
- Misuse warning: do not generalize reported matching performance without
  matching training and benchmark conditions.
- Evidence: https://arxiv.org/abs/2402.17764.

## Native 1-bit LLM

- Source kind: primary-source
- Local meaning: an LLM trained under the low-bit/ternary recipe rather than
  merely quantized after full-precision training.
- Arcanum reading: the training path is part of the architecture contract.
- Promotion status: local-only
- Misuse warning: "native" does not mean every tensor is 1-bit.
- Evidence: https://arxiv.org/abs/2504.12285.

## Ternarization

- Source kind: primary-source
- Local meaning: the process of mapping or learning weights into ternary values.
- Arcanum reading: a lossy compression-and-structure operation that must be
  paired with a training or distillation recipe.
- Promotion status: local-only
- Misuse warning: do not collapse thresholded ternarization, trained assignment,
  and native training into one method.
- Evidence: S3, S4, S5.

## Ternary Inference Kernel

- Source kind: related-source
- Local meaning: an implementation that exploits ternary weights for efficient
  matrix operations or lookup-table paths.
- Arcanum reading: the systems layer that turns representation into actual
  latency/energy benefit.
- Promotion status: local-only
- Misuse warning: low-bit weights without matching kernels may save memory but
  not speed.
- Evidence: S6 and R1.
