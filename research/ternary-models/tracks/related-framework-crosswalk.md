# Related Framework Crosswalk

Target: ternary models

| Framework or paper | Why included | Source kind | Closes residue | Boundary |
| --- | --- | --- | --- | --- |
| Ternary Weight Networks | Establishes early `{-1,0,+1}` weight constraints, scaling, and thresholding. | primary-source | R-TM-005 | borrow-carefully |
| Trained Ternary Quantization | Shows learned ternary assignment and scale factors. | primary-source | R-TM-005 | borrow-carefully |
| TernaryBERT | Gives Transformer-era post/fine-tuned ternarization plus distillation. | primary-source | R-TM-002 | borrow-carefully |
| BitNet b1.58 | Native ternary-weight LLM anchor. | primary-source | R-TM-002 | borrow-carefully |
| BitNet b1.58 2B4T | Public model-weight and training-scale anchor. | primary-source | R-TM-002 | borrow-carefully |
| bitnet.cpp | Implementation path for practical inference. | primary-source | R-TM-003 | borrow-carefully |
| BitNet a4.8 | Activation quantization and sparsification pressure. | related-source | R-TM-004 | future-work |

## Inclusion Rule

Include related work only when it closes a named residue, clarifies a source
claim, or prevents a dangerous analogy. Do not build unbounded background.
