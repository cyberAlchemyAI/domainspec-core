# Notation Bridge

Target: ternary models

## Local Symbols

| Symbol | Source meaning | Plain-language reading | Shared link | Used in |
| --- | --- | --- | --- | --- |
| `{-1, 0, +1}` | ternary weight set | a weight can be negative, absent/zero, or positive | n/a | all artifacts |
| `W` | weight tensor or matrix | learned model weights before or after ternarization | n/a | definitions, claim ledger |
| `b1.58` | `log2(3)`-style ternary weight information capacity | three possible weight values need about 1.58 bits in the ideal code-length sense | n/a | BitNet artifacts |
| `FP16/BF16` | half-precision floating-point baseline | conventional non-ternary training/inference comparison class | n/a | claim ledger |
| `A4/A8` | activation precision shorthand | activation tensors stored/processed with 4-bit or 8-bit precision | n/a | BitNet a4.8 residue |
| `KV cache` | attention key/value cache | memory used by autoregressive inference beyond weights | n/a | systems residue |
| `scale` | multiplicative factor paired with low-bit weights | a small floating value that restores magnitude lost by ternary coding | n/a | TWN, TTQ |

## Reading Order

1. Read `{-1, 0, +1}` and `b1.58` first.
2. Then read scaling-factor definitions.
3. Then read activation/KV-cache symbols before systems claims.

## Notation Residue

| Symbol | Question | Status | Next route |
| --- | --- | --- | --- |
| `b1.58` | Which storage format actually achieves near-ideal density in each runtime? | open | systems lane |
| `scale` | Per-tensor, per-channel, or learned scale? Sources differ by method. | open | source comparison |
