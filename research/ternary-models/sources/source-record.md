# Source Record

Target: ternary models for neural networks and LLMs

Date checked: 2026-06-17

Boundary: public research and public implementation sources only.

## Primary Sources

| ID | Source | Version / date observed | Source kind | Boundary |
| --- | --- | --- | --- | --- |
| S1 | The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits, https://arxiv.org/abs/2402.17764 | submitted 2024-02-27 | primary-source | BitNet b1.58 proposal and reported training/evaluation claims |
| S2 | BitNet b1.58 2B4T Technical Report, https://arxiv.org/abs/2504.12285 | v2 revised 2025-04-25 | primary-source | 2B parameter, 4T token native 1-bit LLM report |
| S3 | TernaryBERT, https://arxiv.org/abs/2009.12812 | v3 revised 2020-10-10 | primary-source | distillation-aware BERT ternarization |
| S4 | Trained Ternary Quantization, https://arxiv.org/abs/1612.01064 | v3 revised 2017-02-23 | primary-source | classic trainable ternary assignment and scaling factors |
| S5 | Ternary Weight Networks, https://arxiv.org/abs/1605.04711 | v3 revised 2022-11-20 | primary-source | early thresholded ternary weight network formulation |
| S6 | Microsoft BitNet repository, https://github.com/microsoft/BitNet | observed 2026-06-17 | primary-source | official bitnet.cpp implementation surface |

## Related Sources

| ID | Source | Source kind | Why included |
| --- | --- | --- | --- |
| R1 | Bitnet.cpp: Efficient Edge Inference for Ternary LLMs, https://arxiv.org/abs/2502.11880 | related-source | inference-systems path for ternary LLMs |
| R2 | BitNet a4.8, https://arxiv.org/abs/2411.04965 | related-source | activation quantization pressure on 1-bit/ternary models |
| R3 | Microsoft BitNet b1.58 2B4T weights, https://huggingface.co/microsoft/bitnet-b1.58-2B-4T | related-source | public model-weight artifact |
| R4 | Hugging Face BitNet docs, https://huggingface.co/docs/transformers/en/model_doc/bitnet | related-source | deployment-facing model variants and usage boundary |

## Evidence Boundary

Claims in this tower are source-backed starter claims. Performance, latency,
energy, or quality claims are accepted only as source-reported until reproduced
locally or routed through a research evidence harness.
