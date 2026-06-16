# Distill — jua-benchmark

The smallest coherent model of JUÁ that still recomposes into the full paper.

## One-sentence model

> JUÁ unifies five heterogeneous Brazilian legal collections (jurisprudence, normative, legislative, tax-QA) under one shared protocol, metric set, and public leaderboard, and uses them to show empirically that **no single retrieval paradigm wins everywhere** — BM25 dominates lexically-cued normative/legislative search while domain-adapted dense embedders win on supervision-aligned jurisprudence — so legal IR must be evaluated *per collection regime*, not by one aggregate number.

## Compositional spine (how the parts assemble)

```
Problem:  Portuguese legal IR is unevaluable — datasets differ in doc type,
          query style, relevance definition.
   │
Move 1:   Compose 5 collections into ONE benchmark
          (JUÁ-Juris · JurisTCU · NormasTCU · Ulysses-RFCorpus · BR-TaxQA-R)
   │
Move 2:   Impose a SHARED evaluation layer
          (NDCG@10 / MRR@10 primary; fixed splits; public leaderboard;
           continuous-infrastructure framing)
   │
Move 3:   Run a paradigm sweep
          (BM25 · dense embedders · reranking · domain-adapted Qwen FT)
   │
Result:   Cross-collection VARIANCE is the signal, not noise:
          - BM25 tops NormasTCU & Ulysses (lexical/institutional cues)
          - Domain-adapted Qwen FT tops supervision-aligned JUÁ-Juris
          - No paradigm uniformly superior
   │
Claim:    Legal IR quality is regime-dependent; evaluate per collection.
```

## Borrow / Analogy / Block

**BORROW (take directly into Jusbrasil work):**
- The *per-regime evaluation discipline*: report retrieval metrics split by collection type (jurisprudence vs. normative vs. legislative vs. QA), never a single blended number.
- The *paradigm-sweep template*: always include BM25 as a first-class baseline alongside dense + reranking; do not assume dense wins.
- The *domain-adaptation-where-supervision-exists* heuristic: fine-tuned dense pays off precisely on the subset with aligned supervision (JUÁ-Juris).

**ANALOGY (maps onto Jus IA, not identical):**
- JUÁ "collection regimes" ↔ Jusbrasil "tribunal/collection heterogeneity." A retriever tuned globally behaves like JUÁ's single paradigm — strong somewhere, weak elsewhere.
- JUÁ-Juris enunciado→excerpt retrieval ↔ Jus IA "similar-jurisprudence" feature. Closest public analog; use it as the yardstick.

**BLOCK (do NOT carry over):**
- Do not import JUÁ's exact decimals as Jus IA targets — qrels definitions differ per collection ([PRIMARY~], some inter-pass inconsistency; see open-residue). Use *relative ordering of paradigms*, not absolute scores.
- Do not treat JUÁ coverage as exhaustive of Brazilian legal IR; it is TCU-heavy (3 of 5 collections from the Federal Audit Court). Generalization to other tribunals is unverified.
