# Bridge Decisions

| Concept | Decision | Rationale | Follow-up |
| --- | --- | --- | --- |
| ternary weights `{-1,0,+1}` | borrow-carefully | The source family agrees on the core three-value weight representation. | Use in local tower terms only. |
| "1-bit LLM" | analogy-only | BitNet b1.58 weights are ternary, not binary; "1-bit" is source phrase but can mislead locally. | Prefer "1.58-bit/ternary-weight" in local docs. |
| BitNet b1.58 recipe | borrow-carefully | Strong current source anchor, but performance claims remain source-reported. | Evidence harness before local claims. |
| TernaryBERT distillation path | borrow-carefully | Useful for smaller fine-tuning experiments, but not identical to native LLM training. | Compare against BitNet lane. |
| CPU inference promise | block | Requires hardware/runtime-specific measurement. | Benchmark only after implementation route. |
| canonical repo vocabulary promotion | future-work | Some terms may become useful, but promotion requires separate governance. | definitions-governance after closure. |
