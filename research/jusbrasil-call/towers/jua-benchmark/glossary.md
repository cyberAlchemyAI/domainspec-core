# Glossary — jua-benchmark

Quick terms for reading JUÁ. Fuller governed definitions in `definitions.md`.

| Term | Plain meaning |
|---|---|
| **IR benchmark** | A fixed, shared package of (corpus + queries + relevance judgments + metrics) that lets different retrieval systems be compared on the same footing. JUÁ is one for Brazilian legal text. |
| **qrels** | "Query relevance judgments." The labeled answer key: for each query, which documents are relevant (and sometimes how relevant, on a graded scale). Without qrels you cannot score retrieval. |
| **Dense retrieval** | Encoding query and documents into vectors with a neural embedding model and ranking by vector similarity. Captures semantic/paraphrase matches that exact words miss. JUÁ's Qwen/OpenAI/Gemma embedders are dense retrievers. |
| **BM25** | The classic lexical (bag-of-words) ranking function. Scores documents by term-frequency / inverse-document-frequency overlap with the query. Strong, cheap, and surprisingly hard to beat when queries share vocabulary with documents. |
| **Collection regimes** | Distinct *types* of legal collection — jurisprudence, normative/regulatory, legislative, question-driven — that differ in document shape, query style, and relevance definition. JUÁ's central claim is that retrieval behavior changes regime to regime, so a single retriever is not uniformly best. |

## Supporting terms

| Term | Plain meaning |
|---|---|
| NDCG@10 | Normalized Discounted Cumulative Gain at rank 10: rewards putting relevant docs near the top; handles graded relevance. JUÁ's primary metric. |
| MRR@10 | Mean Reciprocal Rank at 10: 1/(rank of first relevant doc), averaged. Good when one right answer matters. |
| Reranking | A two-stage pipeline: a cheap retriever (e.g., BM25) pulls candidates, then a stronger model re-orders them. |
| Domain adaptation / FT | Fine-tuning a general embedder on in-domain (legal) supervision so it ranks legal text better. JUÁ fine-tunes Qwen on JUÁ-aligned supervision. |
| enunciado | A formal headnote summarizing a jurisprudential thesis; used as the query side of JUÁ-Juris. |
| TCU | Tribunal de Contas da União — Brazil's Federal Audit Court; source of three JUÁ collections. |
