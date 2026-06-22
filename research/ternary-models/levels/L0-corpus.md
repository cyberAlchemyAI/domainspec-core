# L0 Corpus

## Corpus Boundary

The corpus starts from owned, citable work on ternary weights and 1.58-bit LLMs.
It intentionally combines older CNN/BERT ternarization with newer BitNet-native
LLM work so the tower does not confuse "ternary" with one specific model family.

## Source Inventory

| ID | Title | Core claim to learn from | Evidence label |
| --- | --- | --- | --- |
| S1 | BitNet b1.58 | Every weight in the proposed LLM variant is ternary `{-1, 0, 1}`; authors report matching same-size full-precision Transformer results under the same model size and training-token setup. | primary-source |
| S2 | BitNet b1.58 2B4T | Authors report the first open-source native 1-bit LLM at 2B parameters trained on 4T tokens, with efficiency advantages and public weights/code. | primary-source |
| S3 | TernaryBERT | Fine-tuned BERT weights can be ternarized with approximation/loss-aware methods plus distillation; authors report strong GLUE/SQuAD results and 14.9x smaller size. | primary-source |
| S4 | TTQ | Ternary values and ternary assignment can be trained, with scaling factors and reported CNN accuracy retention or improvement in selected settings. | primary-source |
| S5 | TWN | Ternary weights constrained to `+1, 0, -1` plus scaling can reduce memory and multiplication cost versus float32. | primary-source |
| S6 | bitnet.cpp | Official implementation surface for BitNet b1.58-style inference, including CPU/GPU optimized kernels and public usage path. | primary-source |
| R1 | Bitnet.cpp paper | Details a specialized inference system for ternary LLMs and mixed-precision GEMM. | related-source |
| R2 | BitNet a4.8 | Extends the low-bit path to activation quantization and sparsification pressure. | related-source |
| R3 | HF model weights | Public artifact for practical experimentation with BitNet b1.58 2B4T. | related-source |

## Corpus Gaps

- Critical replication sources and third-party negative results are not yet
  included.
- Hardware-specific ternary arithmetic literature is not yet mapped.
- Training-from-scratch recipes need a deeper source pass before implementation
  claims are made.
