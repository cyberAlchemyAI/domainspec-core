# Source Claim Ledger

Target: ternary models

| ID | Claim | Source kind | Evidence | Local reading | Status |
| --- | --- | --- | --- | --- | --- |
| C1 | BitNet b1.58 uses ternary weights `{-1, 0, 1}` for every parameter in the proposed LLM variant. | primary-source | https://arxiv.org/abs/2402.17764 | Treat ternary weights as the central BitNet b1.58 representational claim. | accepted |
| C2 | BitNet b1.58 authors report matching same-size full-precision Transformer performance with lower latency, memory, throughput, and energy cost. | primary-source | https://arxiv.org/abs/2402.17764 | Source-reported only; needs local reproduction before development claims. | open |
| C3 | BitNet b1.58 2B4T is reported as an open-source native 1-bit LLM at 2B parameters trained on 4T tokens. | primary-source | https://arxiv.org/abs/2504.12285 | Use as the current practical source anchor for model-weight experimentation. | accepted |
| C4 | TernaryBERT ternarizes fine-tuned BERT weights with approximation/loss-aware methods plus distillation and reports 14.9x size reduction. | primary-source | https://arxiv.org/abs/2009.12812 | Useful for post/full-model ternarization and distillation lineage. | accepted |
| C5 | TTQ learns ternary values and ternary assignment, using scaling factors at inference. | primary-source | https://arxiv.org/abs/1612.01064 | Useful as a baseline method family for trainable ternary quantization. | accepted |
| C6 | TWN constrains weights to `+1, 0, -1`, minimizes distance to full-precision weights with scaling, and reports compression/multiplication reduction. | primary-source | https://arxiv.org/abs/1605.04711 | Establishes early ternary-weight representation and threshold lineage. | accepted |
| C7 | bitnet.cpp is the official inference framework for BitNet b1.58-style 1-bit LLMs and reports CPU/GPU optimized kernel paths. | primary-source | https://github.com/microsoft/BitNet | Systems work must inspect this before inventing an inference path. | accepted |

## Open Claim Residue

| ID | Question | Blocking artifact | Next route |
| --- | --- | --- | --- |
| OCR1 | Which efficiency claims reproduce on the user's target hardware? | local benchmark report | research-evidence-harness |
| OCR2 | Which training recipe can be afforded locally? | compute/budget plan | task-session after research closure |
| OCR3 | Which public model artifact should be used first? | model selection decision | decision-gate |
