# L0 — Corpus (Source Record)

## Full citation

Magesh, V., Surani, F., Dahl, M., Suzgun, M., Manning, C. D., & Ho, D. E. (2025).
*Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools.*
Journal of Empirical Legal Studies. (Preprint: arXiv:2405.20362, submitted 2024-05-30.)
Affiliation: Stanford RegLab / Stanford Institute for Human-Centered AI (HAI) / Stanford Law School.

## Links (date checked: 2026-06-10)

- arXiv landing: https://arxiv.org/abs/2405.20362  — fetched OK.
- arXiv HTML (v1): https://arxiv.org/html/2405.20362v1  — fetched OK (primary text source for typology/methods).
- arXiv PDF: https://arxiv.org/pdf/2405.20362  — fetched but binary/garbled; not text-extracted.
- Journal (Wiley JELS): https://onlinelibrary.wiley.com/doi/full/10.1111/jels.12413  — HTTP 403 (paywalled).
- Stanford HAI plain-language summary: https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-or-more-benchmarking-queries  — title/summary captured via search; direct fetch returned no body.
- Stanford Law copy: https://law.stanford.edu/wp-content/uploads/2024/05/Legal_RAG_Hallucinations.pdf  — known mirror, not separately fetched.
- Independent breakdown (Auryth): https://auryth.ai/en/blog/stanford-hallucination-study-legal-ai/  — fetched OK (corroborating, related-source).
- Independent commentary (AI Law Librarians): https://www.ailawlibrarians.com/2026/02/19/what-the-science-says-about-hallucinations-in-legal-research/  — fetched OK (related-source).

## What the paper IS (source boundary — covered)

- The **first preregistered empirical evaluation** of proprietary, RAG-based AI legal
  research tools.
- Tools audited: **Lexis+ AI** (LexisNexis), **Westlaw AI-Assisted Research** and
  **Ask Practical Law AI** (Thomson Reuters). Baseline: **GPT-4** (general chatbot).
- Domain: **US** legal research (caselaw, doctrine, jurisdiction/precedent questions).
- A **manually hand-scored** evaluation: 202 open-ended queries, expert legal scorers.
- A **conceptual contribution**: a typology splitting *correctness* from *groundedness*,
  and a definition of hallucination as "incorrect **or** misgrounded."
- A **professional-responsibility** argument about lawyers' duty to verify AI output.

## What the paper is NOT (source boundary — out of scope)

- Not Brazilian law, Portuguese-language tools, or civil-law systems. (Jusbrasil/Jus IA
  is in this gap — application is by analogy, see `bridge-decisions.md`.)
- Not a large-N or automated benchmark — N=202, manual scoring; authors flag scale as a limit.
- Not an evaluation of document drafting, summarization quality per se, or non-research
  features (focus is legal-research Q&A).
- Not a controlled disclosure of vendor internals — systems are closed/black-box; the
  audit is behavioural (input→output), not architectural.
- Not a longitudinal study — a snapshot of tool behaviour at time of testing (2024).
- Does not publish (in fetched material) the full per-tool correctness×groundedness
  crosstab counts — see `open-residue.md`.

## Section map (arXiv HTML v1)

1. **Introduction** — vendor "hallucination-free" claims; what the audit shows.
2. **Background** — legal AI products, prior hallucination findings in general LLMs.
3. **Retrieval-Augmented Generation (RAG)** — how RAG is supposed to reduce hallucination.
4. **Conceptualizing Legal Hallucinations** — the *correctness* × *groundedness*
   framework; definitions of accurate / incomplete / hallucinated.
5. **Methodology** — the 202-query preregistered dataset, query categories, scoring rubric.
6. **Results** — per-tool hallucination/accuracy/incompleteness rates; failure-mode analysis.
7. **Limitations** — sample size, closed access, manual scoring, snapshot-in-time.
8. **Implications** — professional responsibility; supervision/verification duties.
9. **Conclusion.**
10. Acknowledgments.
11–13. **Appendices** — Query Descriptions, Running Queries, Query Evaluation.

## Dataset composition (primary-source, from arXiv HTML v1)

- Total: **202** preregistered open-ended queries.
- **General legal research** — 80 queries (~39.6%): common-law doctrine, published
  practice bar-exam questions, holding questions.
- **Jurisdiction/time-specific** — 70 queries (~34.7%): circuit splits, overturned
  cases, recent developments.
- **False-premise** — 22 queries (~10.9%): queries embedding a mistaken legal premise.
- **Factual recall** — 30 queries (~14.9%): basic facts (e.g., year a case was decided).
