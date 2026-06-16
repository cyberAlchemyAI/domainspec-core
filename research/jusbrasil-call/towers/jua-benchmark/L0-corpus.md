# L0 — Source Corpus Record

**Date checked:** 2026-06-10
**Lane:** jua-benchmark

## Source record

| Field | Value |
|---|---|
| Title | JUÁ — A Benchmark for Information Retrieval in Brazilian Legal Text Collections |
| Authors | Jayr Pereira, Leandro Fernandes, Erick de Brito, Roberto Lotufo, Luiz Bonifacio |
| Year | 2026 (submitted 7 April 2026 v1; revised 8 April 2026 v2) |
| arXiv id | 2604.06098 |
| Landing | https://arxiv.org/abs/2604.06098 |
| HTML render | https://arxiv.org/html/2604.06098v2 |
| PDF | https://arxiv.org/pdf/2604.06098 (~951 KB, ~22 pp) |
| Subjects | cs.IR (Information Retrieval), cs.CL (Computation and Language) |
| Leaderboard | https://huggingface.co/spaces/ufca-llms/jua-leaderboard [PRIMARY~ — link reported by HTML fetch, not independently opened] |
| Datasets | Hugging Face, `ufca-llms` organization [PRIMARY~] |

## Accessibility note

- **Landing page (abs):** ACCESSIBLE. Title, authors, abstract, subjects, dates fetched verbatim 2026-06-10.
- **HTML v2:** ACCESSIBLE. Used for collection names, sizes, metrics, baselines, results-table excerpts, qrels construction, section headings.
- **PDF:** Fetched as binary and summarized by WebFetch's small model; NOT read line-by-line by the tower builder. Table numbers therefore carry transcription risk (see `open-residue.md`).
- **Leaderboard / HF datasets:** URLs reported by the HTML fetch but NOT independently opened in this session. Treated as [PRIMARY~].
- No paywall encountered. No fabrication performed. Where a number could not be confirmed, it is marked [OPEN] rather than guessed.

## Section map (from HTML v2) [PRIMARY]

1. **Introduction** — problem: Portuguese legal IR hard to evaluate; datasets differ in document type, query style, relevance definition.
2. **Related Work** — prior IR benchmarks (BEIR referenced) and Brazilian legal datasets (e.g., JurisTCU lineage).
3. **Benchmark Design and Datasets** — the five sub-collections, their corpora, query styles, and qrels construction.
4. **Experiments** — retrieval pipelines: lexical (BM25), dense embedders, reranking; domain-adapted Qwen fine-tuned on JUÁ-aligned supervision.
5. **Results** — per-collection NDCG@10 / MRR@10 (+ MAP@10, Recall@10, P@10); cross-collection trade-off analysis.
6. **Conclusions** — JUÁ as continuous evaluation infrastructure; no dominant paradigm.

## Sub-collections (the JUÁ composite) [PRIMARY for names/roles; [PRIMARY~] for counts]

| Collection | Role / document type | Query style | Queries | Documents |
|---|---|---|---|---|
| JUÁ-Juris | TCU curated jurisprudence excerpts (supervision-aligned subset) | enunciado-based | 1,714 test; 15,428 train | in corpus |
| JurisTCU | TCU jurisprudence excerpts | real + synthetic keyword queries | 150 | 16,045 |
| NormasTCU | TCU normative acts (regulatory/normative) | regulatory queries | 46 | 14,469 |
| Ulysses-RFCorpus | Legislative docs (Chamber of Deputies) w/ operational feedback | legislative consultation | 692 | not specified |
| BR-TaxQA-R | Tax answers + linked reference material (Federal Revenue Service) | question-driven | 715 | not specified |

> TCU = Tribunal de Contas da União (Federal Audit Court). enunciado = a formal headnote/summary statement of a jurisprudential thesis.

## Evaluation surface [PRIMARY]

- **Primary metrics:** NDCG@10, MRR@10.
- **Complementary:** MAP@10, Recall@10, P@10.
- **Protocol:** shared protocols, common ranking metrics, fixed splits when applicable, public leaderboard.

## Baselines / systems evaluated [PRIMARY]

- **Lexical:** BM25.
- **Dense:** Qwen 4B, Qwen 8B, OpenAI `3-small`, KaLM Gemma3 12B.
- **Fine-tuned (domain-adapted):** Qwen3-Embedding-4B (FT), Qwen 0.6B (FT).
- **Reranking:** same dense/FT models applied as rerankers over a first-stage candidate set.

## qrels construction (relevance judgments) [PRIMARY~]

- **JUÁ-Juris:** binary relevance (score = 1) via direct query–document correspondence.
- **JurisTCU:** expert-verified relevance judgments.
- **NormasTCU:** three-level graded scale, four domain experts.
- **Ulysses-RFCorpus:** three-level scale, 54 legislative consultants.
- **BR-TaxQA-R:** graded — primary answers scored 2, linked answers scored 1.
