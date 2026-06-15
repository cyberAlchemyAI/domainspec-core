# bridge-decisions.md — Paper → Jus IA Smart Summaries

Each decision maps a paper element to the Jus IA smart-summaries / faithfulness-control context. Statuses: **ADOPT** (reuse), **ADAPT** (reuse with change), **WATCH** (track, depends on residue), **HOLD** (don't transfer yet).

| # | Paper element | Jus IA mapping | Status | Note |
|---|---|---|---|---|
| B1 | Ementa as gold summary | Smart summaries already aim to produce ementa-style output | **ADOPT** | Same product target; strong precedent that the task is well-posed on STF data. |
| B2 | Entailment (NLI) faithfulness scorer | A faithfulness gate / hallucination filter on generated summaries | **ADAPT** | Adopt the *idea*; re-train/tune an entailment model on Jus IA's court mix and modern embeddings. |
| B3 | Candidate-generate → rerank → select | Generate N summaries, rank by faithfulness, surface the best | **ADOPT** | Model-agnostic guardrail; works on top of an LLM generator. |
| B4 | Multi-view over long ruling | Long-document chunking + per-chunk summary + aggregation | **ADAPT** | Modern long-context LLMs reduce the length pressure, but chunk-then-select still helps faithfulness + cost. |
| B5 | ROUGE as success metric | Offline eval signal | **WATCH** | Use ROUGE for regression tracking but pair with human faithfulness review; ROUGE alone under-measures legal-substantive errors. |
| B6 | RulingBR (STF-only, 2011–2018) | Training/eval substrate | **ADAPT** | Useful seed corpus; Jus IA's coverage is broader and newer — extend/refresh data. |
| B7 | Specific base summarizer (2023) | Production generator | **HOLD** | Identity is open-residue and pre-LLM; replace with current generator, keep the entailment-selection wrapper. |
| B8 | Reported ROUGE deltas | Quote in the call? | **HOLD** | Numbers are behind paywall — do NOT cite specific figures; cite the *direction* ("improves ROUGE across metrics") only. |

## Net bridge read
The **transferable core is the architecture pattern**, not the 2023 model weights: *summarize → score faithfulness with entailment → select*. It is the most directly product-relevant published analogue for adding a **hallucination guardrail** to Jus IA smart summaries, validated on the same court and the same ementa target.
