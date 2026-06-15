# Bridge Decisions — jua-benchmark

How JUÁ (source) maps onto Jusbrasil / Jus IA work. Every row here is a **[BRIDGE]** reading — NOT a paper claim. Statuses: ADOPT (carry into Jus IA evaluation) · WATCH (track, conditionally useful) · HOLD (needs more verification) · REJECT (do not carry).

| # | Bridge decision | Rationale | Status |
|---|---|---|---|
| BR-1 | Use JUÁ as the public yardstick for Jus IA's similar-jurisprudence retrieval. | Freshest (Apr 2026) Brazilian legal IR benchmark with leaderboard + baselines; JUÁ-Juris is the direct analog (enunciado→excerpt). | **ADOPT** |
| BR-2 | Evaluate Jus IA retrieval *per collection regime*, never by one blended metric. | JUÁ's core finding: no paradigm uniformly best; aggregate scores hide regime trade-offs — the tribunal-heterogeneity problem. | **ADOPT** |
| BR-3 | Keep BM25 as a first-class baseline in any Jus IA retrieval bench. | BM25 tops NormasTCU & Ulysses; lexical/institutional phrasing is a feature in legal text. | **ADOPT** |
| BR-4 | Apply domain-adapted dense (fine-tuned embedder) specifically where aligned supervision exists. | Domain adaptation's clearest gain is on the supervision-aligned JUÁ-Juris subset; gains are not free elsewhere. | **ADOPT** |
| BR-5 | Treat tribunal heterogeneity as a first-class design constraint, not an edge case. | JUÁ shows retrieval behavior swings sharply across collection types; one global retriever will under/over-serve specific tribunals. | **ADOPT** |
| BR-6 | Consider submitting/benchmarking a Jus IA retriever to the JUÁ public leaderboard. | Public, continuous-evaluation infrastructure → external credibility for Jus IA retrieval quality. | **WATCH** (verify leaderboard openness/terms by opening the HF space) |
| BR-7 | Reuse JUÁ qrels-construction patterns (expert + consultant graded scales) for internal Jus IA eval sets. | Graded, expert-built qrels are the credible basis for legal relevance. | **WATCH** (qrels details are [PRIMARY~]; confirm in PDF) |
| BR-8 | Adopt JUÁ's exact NDCG/MRR decimals as Jus IA performance targets. | Numbers are [PRIMARY~] with inter-pass inconsistency; qrels definitions differ per collection — cross-system absolute comparison is unsafe. | **REJECT** |
| BR-9 | Assume JUÁ generalizes across all Brazilian tribunals. | 3 of 5 collections are TCU-sourced; broader-tribunal coverage unverified. | **HOLD** |

## Net stance for the call

ADOPT the *method* (per-regime evaluation, BM25-as-baseline, targeted domain adaptation, heterogeneity as a constraint) and the *yardstick role* of JUÁ. REJECT importing raw numbers as targets. HOLD/ WATCH the leaderboard-submission and cross-tribunal-generalization questions pending full-PDF and HF-space verification.
