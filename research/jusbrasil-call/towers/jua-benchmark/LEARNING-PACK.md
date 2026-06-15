# Learning Pack — JUÁ Benchmark

**Paper:** JUÁ — A Benchmark for Information Retrieval in Brazilian Legal Text Collections (Pereira, Fernandes, de Brito, Lotufo, Bonifacio · arXiv:2604.06098 · April 2026)
**For:** Jusbrasil "Jus IA" call — similar-jurisprudence retrieval + tribunal-heterogeneity challenge.
**Date:** 2026-06-10

---

## 1. Source-backed claims (what the paper actually says)

All [PRIMARY] unless flagged [PRIMARY~] (via WebFetch table summary — see `open-residue.md`).

1. JUÁ is a **public benchmark + continuous evaluation infrastructure** for Brazilian (Portuguese) legal IR: shared protocols, common metrics, fixed splits, public leaderboard. [PRIMARY]
2. It composes **five heterogeneous collections** spanning four regimes: jurisprudence (JUÁ-Juris, JurisTCU), normative/regulatory (NormasTCU), legislative (Ulysses-RFCorpus), question-driven tax (BR-TaxQA-R). [PRIMARY]
3. **qrels differ by collection** — binary, expert-verified, 3-level (4 experts), 3-level (54 consultants), graded 2/1 — i.e., the *definition of relevance* itself changes by regime. [PRIMARY~]
4. Systems swept: **BM25 (lexical), dense embedders (Qwen 4B/8B, OpenAI 3-small, KaLM Gemma3 12B), reranking, and domain-adapted Qwen FT** (Qwen3-Embedding-4B FT, Qwen 0.6B FT). [PRIMARY]
5. Primary metrics **NDCG@10 / MRR@10** (+ MAP@10, Recall@10, P@10). [PRIMARY]
6. **Core finding (verbatim):** "no dominant retrieval paradigm across JUÁ: lexical, dense, and reranking systems exchange positions depending on the dataset, and none is uniformly superior." [PRIMARY]
7. **Domain adaptation pays off most on the supervision-aligned JUÁ-Juris subset;** BM25 stays competitive elsewhere, especially under strong lexical/institutional phrasing cues. [PRIMARY]
8. **Where each paradigm wins (NDCG@10):** BM25 tops NormasTCU (~0.364) and Ulysses-RFCorpus (~0.531); domain-adapted Qwen FT tops jurisprudence; best overall ≈ 0.435 (Qwen3-Embedding-4B FT). [PRIMARY~]

## 2. Operator model (how to think about JUÁ in one breath)

> Legal search is not one task — it is several **regimes** that reward different retrievers. JUÁ's contribution is the *measurement apparatus* that makes that visible: put five regimes under one ruler, sweep paradigms, and watch the leaderboard reorder collection by collection. The takeaway is operational, not just academic — **you cannot pick one retriever and declare victory.**

## 3. Evaluation takeaways

- **Per-regime reporting is mandatory.** A single aggregate NDCG hides the trade-offs that decide real quality. Always split by collection type.
- **BM25 is not legacy here.** On normative and legislative text, institutional phrasing makes exact lexical match a strength — BM25 beats dense models on those collections.
- **Domain adaptation is targeted, not universal.** Fine-tuned dense embedders win where aligned supervision exists (JUÁ-Juris); elsewhere the gain shrinks or reverses.
- **qrels heterogeneity caps cross-collection comparison.** Relevance is defined differently per collection — compare *paradigm ordering*, not raw decimals across collections.
- **Reranking helps but does not dominate.** It changes the leader on some collections (JurisTCU) but is not a universal win.

## 4. Five things for the call

1. **JUÁ is the public yardstick for Jus IA's similar-jurisprudence feature** — and JUÁ-Juris (enunciado→excerpt) is the direct analog. Benchmark against it.
2. **The cross-collection-variance finding IS the tribunal-heterogeneity challenge, externally validated:** one globally-tuned retriever will be strong on some tribunals/collections and weak on others. Design for per-regime routing, not a single model.
3. **Keep BM25 in the loop.** It wins on normative/legislative collections; dropping it for "modern" dense-only would regress those regimes.
4. **Invest domain adaptation where supervision is aligned.** The biggest dense gain is on the supervision-rich jurisprudence subset — so curate aligned (query, relevant-excerpt) supervision for Jus IA's jurisprudence corpus first.
5. **Consider the JUÁ leaderboard as external proof** of Jus IA retrieval quality — but verify the HF space's submission terms first (open residue), and never adopt JUÁ's raw decimals as internal targets (qrels differ).

## 5. Honest cutoff — what this pack does NOT settle

- **Exact table numbers are [PRIMARY~]** (WebFetch summary of the PDF). Two passes disagreed on a couple of peaks (BR-TaxQA-R 0.799 vs 0.777; JUÁ-Juris winner 0.302 vs 0.290). **Read the PDF Table 2 before quoting any specific decimal in a deck.** (`open-residue.md` OR-1/OR-2.)
- **Aggregation of the "0.435 overall" is unknown** (macro vs micro vs leaderboard composite). (OR-3.)
- **Domain-adaptation recipe, reranking pipeline depth, and corpus sizes for two collections** were not captured — needed to *reproduce* the JUÁ-Juris gain for Jus IA. (OR-4/5/6.)
- **HF leaderboard + dataset cards not independently opened** — submission terms and per-collection licenses unverified. (OR-7/8/9.)
- **TCU-centricity (3 of 5 collections)** means generalization to other Brazilian tribunals is unverified — directly limits the tribunal-heterogeneity bridge. (OR-10.)
- **No significance/variance data captured** — cannot say which per-collection differences are statistically robust. (OR-11.)

> Bottom line: the *qualitative model and method* (per-regime evaluation, BM25-as-baseline, targeted domain adaptation, heterogeneity-as-constraint) are solidly source-backed and call-ready. The *exact quantitative leaderboard* should be confirmed against the full PDF before external citation.
