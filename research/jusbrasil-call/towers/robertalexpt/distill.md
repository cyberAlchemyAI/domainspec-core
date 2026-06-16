# distill.md — Smallest Coherent Model

## One-sentence model

> If your legal corpus is mostly **duplicated boilerplate**, then **deduplicating
> it (MinHash/LSH) and pretraining a modest RoBERTa-base on a legal+general
> mix** beats throwing a bigger generic model at the problem — a base-size legal
> encoder (RoBERTaLexPT, 85.41 macro-F1 on PortuLex) outperforms larger generic
> and prior legal models.

## Compositional spine (recompose into the full paper)

1. **Pain** — Portuguese/Brazilian legal corpora are massively redundant
   (repeated ementas, citations, templated decisions).
2. **Materials** — Build LegalPT (legal, 125 GiB) + CrawlPT (general, 163 GiB).
3. **Filter** — MinHash+LSH dedup (5-grams, sig 256, Jaccard > 0.7).
4. **Train** — RoBERTa-base from scratch on the deduplicated legal+general mix.
5. **Measure** — PortuLex (4 legal tasks) → 85.41 avg macro-F1.
6. **Claim** — Dedup is decisive; legal+general mix > legal-only; base beats
   larger generic models.

## Borrow / Analogy / Block

- **Borrow (use directly):** the dedup recipe (MinHash/LSH params) and the
  legal+general mix as a default pretraining recipe for a Portuguese legal
  encoder; the open CC-BY artifacts and PortuLex as an eval harness.

- **Analogy (transfer the shape):** "data hygiene before model size." The lever
  is the *corpus*, not the parameter count — same shape as Jusbrasil's "millions
  of redundant judicial documents" problem: dedup first, then represent.

- **Block (do NOT over-transfer):** results are **Portuguese legal NER +
  classification at base scale**; they do not establish generative/LLM behavior,
  retrieval quality directly, or the exact magnitude of dedup's effect (that
  number is open). Don't extrapolate the 85.41 to unrelated tasks or to a
  quantified "dedup removed X%."
