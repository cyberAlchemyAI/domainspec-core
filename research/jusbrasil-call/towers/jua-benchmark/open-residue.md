# Open Residue — jua-benchmark

What is unverified, uncertain, or needs the full PDF. Recorded honestly; nothing here was invented to fill a gap.

## Needs full-PDF line-by-line verification (table numbers are [PRIMARY~])

| # | Residue | Why it matters |
|---|---|---|
| OR-1 | **Inter-pass inconsistency in peak NDCG@10 values.** Two WebFetch passes over Table 2 reported different peaks: BR-TaxQA-R 0.799 (Qwen 8B) vs 0.777 (FT-4B); JUÁ-Juris winner 0.302 (Qwen 0.6B FT) vs 0.290 (FT-4B). | Decision weight on "which model wins where." Resolve by reading the actual PDF Table 2. |
| OR-2 | Exact full Table 2 (all models × all collections × all metrics) not transcribed. | Only BM25 and Qwen3-Embedding-4B (FT) rows captured in full; dense/rerank rows partial. |
| OR-3 | Whether "Overall 0.435" is a macro-average, micro-average, or leaderboard composite. | Aggregation method changes how to read the headline number. |
| OR-4 | Document/corpus sizes for Ulysses-RFCorpus and BR-TaxQA-R ("not specified" in fetch). | Needed to judge collection difficulty. |
| OR-5 | Exact fine-tuning supervision recipe for the domain-adapted Qwen (data, negatives, objective). | Needed to replicate the JUÁ-Juris domain-adaptation gain for Jus IA. |
| OR-6 | Reranking pipeline specifics (first-stage candidate depth, which retriever feeds the reranker). | Affects fair comparison and reproduction. |

## Needs independent source access (not opened this session)

| # | Residue | Action |
|---|---|---|
| OR-7 | HF leaderboard space `ufca-llms/jua-leaderboard` not independently opened; openness/submission terms unknown. | Open the space to confirm BR-6 (submission) and BR-7 (qrels reuse). |
| OR-8 | HF dataset cards under `ufca-llms` not opened; licensing/access of each sub-collection unknown. | Check licenses before any Jus IA reuse. |
| OR-9 | Leaderboard URL itself is [PRIMARY~] (reported by HTML fetch, not clicked). | Confirm exact URL/path. |

## Conceptual / scope residue

| # | Residue | Note |
|---|---|---|
| OR-10 | TCU-centricity: 3 of 5 collections are Federal Audit Court sourced. Generalization to STF/STJ/labor/state tribunals is unverified. | Directly bears on the Jus IA tribunal-heterogeneity bridge (BR-9, HOLD). |
| OR-11 | Statistical-significance / variance reporting across runs not captured. | Whether per-collection differences are significant vs. noise is unknown from fetch. |
| OR-12 | Relationship/overlap between JUÁ-Juris and the pre-existing JurisTCU dataset (lineage) not fully pinned. | Both are TCU jurisprudence; dedup/overlap matters for clean evaluation. |

**Open-residue count: 12.**
