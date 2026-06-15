# Definitions (governed) — jua-benchmark

Canonical, stable definitions for the load-bearing terms of this tower. Each carries an intuition and a downstream-drift note (what breaks if the meaning slips).

---

## DEF-1 — IR benchmark
**Definition.** A reusable evaluation package consisting of (a) a document corpus, (b) a set of queries, (c) relevance judgments (qrels) tying queries to relevant documents, and (d) an agreed metric protocol, such that any retrieval system can be scored comparably.
**Intuition.** The "exam paper + answer key + grading rubric" for search systems.
**In JUÁ.** JUÁ bundles five corpora into one benchmark and adds shared protocols, fixed splits, and a public leaderboard — explicitly positioned as *continuous evaluation infrastructure*, not a one-shot dataset. [PRIMARY]
**Drift risk.** If "benchmark" is read as a single dataset, the cross-collection-variance finding (the whole point) disappears.

---

## DEF-2 — qrels (query relevance judgments)
**Definition.** The labeled mapping from each query to the documents judged relevant, optionally with a graded relevance level.
**Intuition.** The answer key. Quality and grading scheme of qrels bound the trustworthiness of every score above them.
**In JUÁ.** qrels are constructed *differently per collection*: binary direct-correspondence (JUÁ-Juris), expert-verified (JurisTCU), 3-level by 4 experts (NormasTCU), 3-level by 54 legislative consultants (Ulysses-RFCorpus), graded 2/1 (BR-TaxQA-R). [PRIMARY~]
**Drift risk.** Comparing NDCG across collections as if qrels were homogeneous over-reads the numbers; relevance *definitions* differ by regime.

---

## DEF-3 — Dense retrieval
**Definition.** Retrieval by encoding queries and documents into dense vectors via a neural model and ranking by vector similarity (e.g., cosine), rather than by lexical term overlap.
**Intuition.** Match on meaning, not just words.
**In JUÁ.** Dense baselines: Qwen 4B/8B, OpenAI 3-small, KaLM Gemma3 12B, plus domain-adapted Qwen3-Embedding-4B (FT) and Qwen 0.6B (FT). [PRIMARY]
**Drift risk.** Treating "dense = always better" contradicts JUÁ's result that BM25 wins on normative/legislative collections.

---

## DEF-4 — BM25
**Definition.** A probabilistic lexical ranking function scoring documents by TF-IDF-style term overlap with the query, with term-frequency saturation and length normalization.
**Intuition.** Strong word-matching baseline; cheap, no training.
**In JUÁ.** Top NDCG@10 on NormasTCU and Ulysses-RFCorpus; competitive overall — "highly competitive ... especially in settings with strong lexical and institutional phrasing cues." [PRIMARY]
**Drift risk.** Dismissing BM25 as legacy misses that institutional/legal phrasing makes lexical match a feature, not a weakness.

---

## DEF-5 — Collection regimes
**Definition.** Distinct categories of legal collection — jurisprudence, normative/regulatory, legislative, question-driven — that differ along document type, query style, and relevance definition, and therefore reward different retrieval paradigms.
**Intuition.** Different "kinds of legal search" are different games; the best player changes by game.
**In JUÁ.** The benchmark is deliberately heterogeneous across regimes; the central finding is that "no dominant retrieval paradigm" holds across them. [PRIMARY]
**Drift risk.** Optimizing a single global retriever and reporting one aggregate score hides the regime-specific trade-offs that matter operationally (the tribunal-heterogeneity problem).
