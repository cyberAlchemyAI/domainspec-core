# Claim Ledger — jua-benchmark

Every load-bearing claim with a source-kind label. Source claims are kept strictly separate from Arcanum/Jusbrasil readings.

**Labels:** [PRIMARY] stated verbatim in paper · [PRIMARY~] from paper via WebFetch table summarization (transcription risk) · [INFERRED] deduced from primary text · [BRIDGE] Jusbrasil reading, NOT a paper claim · [OPEN] unverified.

## A. What JUÁ is

| # | Claim | Source-kind |
|---|---|---|
| A1 | JUÁ is a public benchmark for Brazilian (Portuguese) legal information retrieval. | [PRIMARY] |
| A2 | Motivation: Portuguese legal IR is hard to evaluate systematically because datasets differ in document type, query style, and relevance definition. | [PRIMARY] |
| A3 | JUÁ is intended as *continuous evaluation infrastructure* — shared protocols, common ranking metrics, fixed splits when applicable, and a public leaderboard — not just a static dataset. | [PRIMARY] |
| A4 | Coverage spans jurisprudence retrieval plus legislative, regulatory, and question-driven legal search. | [PRIMARY] |
| A5 | Leaderboard hosted at huggingface.co/spaces/ufca-llms/jua-leaderboard; datasets under HF `ufca-llms`. | [PRIMARY~] |

## B. Collections

| # | Claim | Source-kind |
|---|---|---|
| B1 | JUÁ composes five sub-collections: JUÁ-Juris, JurisTCU, NormasTCU, Ulysses-RFCorpus, BR-TaxQA-R. | [PRIMARY] |
| B2 | JUÁ-Juris = TCU curated jurisprudence, enunciado-based queries; it is the supervision-aligned subset for domain adaptation. | [PRIMARY] |
| B3 | JurisTCU = TCU jurisprudence excerpts with real + synthetic keyword queries; 150 queries, 16,045 docs. | [PRIMARY~] |
| B4 | NormasTCU = TCU normative acts; 46 queries, 14,469 docs. | [PRIMARY~] |
| B5 | Ulysses-RFCorpus = Chamber of Deputies legislative docs; 692 queries. | [PRIMARY~] |
| B6 | BR-TaxQA-R = Federal Revenue Service tax answers + linked references; 715 queries. | [PRIMARY~] |
| B7 | JUÁ-Juris: 1,714 test queries; 15,428 train queries. | [PRIMARY~] |
| B8 | qrels vary by collection: binary (JUÁ-Juris), expert-verified (JurisTCU), 3-level/4 experts (NormasTCU), 3-level/54 consultants (Ulysses), graded 2/1 (BR-TaxQA-R). | [PRIMARY~] |

## C. Baselines & metrics

| # | Claim | Source-kind |
|---|---|---|
| C1 | Pipelines evaluated: lexical (BM25), dense retrieval, and BM25-based / dense reranking. | [PRIMARY] |
| C2 | Dense baselines include Qwen 4B, Qwen 8B, OpenAI 3-small, KaLM Gemma3 12B. | [PRIMARY~] |
| C3 | A domain-adapted Qwen embedding model (Qwen3-Embedding-4B FT; also Qwen 0.6B FT) was fine-tuned on JUÁ-aligned supervision. | [PRIMARY] |
| C4 | Primary metrics: NDCG@10 and MRR@10; complementary MAP@10, Recall@10, P@10. | [PRIMARY] |

## D. Findings (the core result)

| # | Claim | Source-kind |
|---|---|---|
| D1 | **No dominant retrieval paradigm across JUÁ: lexical, dense, and reranking systems exchange positions depending on the dataset, and none is uniformly superior.** (verbatim) | [PRIMARY] |
| D2 | Retrieval methods show "substantial cross-dataset trade-offs"; strong aggregate performance does not guarantee uniform superiority. | [PRIMARY] |
| D3 | Domain adaptation yields its clearest gains on the supervision-aligned JUÁ-Juris subset. | [PRIMARY] |
| D4 | BM25 remains highly competitive on other collections, especially under strong lexical / institutional phrasing cues. | [PRIMARY] |
| D5 | BM25 is the top NDCG@10 performer on NormasTCU (0.364) and Ulysses-RFCorpus (0.531). | [PRIMARY~] |
| D6 | Best overall NDCG@10 = 0.435, by Qwen3-Embedding-4B (FT) as first-stage retriever. | [PRIMARY~] |
| D7 | Per-collection NDCG@10 winners: JUÁ-Juris → Qwen 0.6B (FT) 0.302; JurisTCU → Qwen3-Embedding-4B (FT) Rerank 0.378; NormasTCU → BM25 0.364; Ulysses → BM25 0.531; BR-TaxQA-R → Qwen 8B 0.799. | [PRIMARY~] |
| D8 | On JUÁ-Juris, BM25 is weak (NDCG@10 0.103) while FT Qwen reaches ~0.29–0.30 — the domain-adaptation gain is largest here. | [PRIMARY~] |

## E. Excerpt of results table (Table 2; NDCG@10 / MRR@10) [PRIMARY~ — verify against PDF]

| Model | JUÁ-Juris | JurisTCU | NormasTCU | Ulysses | BR-TaxQA-R | Overall |
|---|---|---|---|---|---|---|
| BM25 | 0.103 / 0.073 | 0.362 / 0.669 | 0.364 / 0.444 | 0.531 / 0.696 | 0.571 / 0.589 | 0.386 / 0.494 |
| Qwen3-Embedding-4B (FT) | 0.290 / 0.230 | 0.363 / 0.641 | 0.305 / 0.474 | 0.441 / 0.624 | 0.777 / 0.800 | 0.435 / 0.554 |

> Note: D6/D7 vs E show minor inconsistencies in reported peaks (e.g., BR-TaxQA-R 0.799 Qwen 8B vs 0.777 FT-4B; JUÁ-Juris 0.302 vs 0.290) because they come from different WebFetch passes over the same tables. These are reconciled-as-pending in `open-residue.md`; treat exact decimals as provisional until the PDF is read.

## F. Bridge readings (NOT paper claims)

| # | Reading | Source-kind |
|---|---|---|
| F1 | JUÁ is the public yardstick for Jus IA's similar-jurisprudence retrieval feature. | [BRIDGE] |
| F2 | The cross-collection-variance finding mirrors Jusbrasil's tribunal-heterogeneity challenge: one retriever tuned globally will under/over-serve specific tribunals/collection types. | [BRIDGE] |
| F3 | JUÁ-Juris (enunciado→excerpt) is the closest analog to similar-jurisprudence retrieval and is where domain adaptation pays off most. | [BRIDGE/INFERRED] |
