# Claim Ledger

Every claim tagged by source kind. **PRIMARY** = stated by the paper or its official
summaries (arXiv abstract/HTML, HAI). **RELATED** = corroborated by independent
third-party write-ups (Auryth, AI Law Librarians). **LOCAL-INFERENCE** = our reasoning
from the source. **ANALOGY** = cross-domain mapping (US legal AI → Jus IA), not the
authors' claim. **OPERATOR-READING** = Arcanum/Jusbrasil framing. **OPEN-RESIDUE** =
asserted somewhere but not verified in fetched material.

No numbers are invented. Where a figure was not seen, it is marked OPEN-RESIDUE.

---

## Headline quantitative findings (PRIMARY)

| ID | Claim | Tag |
|----|-------|-----|
| C1 | The leading RAG legal-research tools **hallucinate between 17% and 33% of the time**, not zero. | PRIMARY |
| C2 | Per-tool hallucination rates: **Lexis+ AI 17%**, **Westlaw AI-Assisted Research 33%**, **Ask Practical Law AI 17%**. | PRIMARY |
| C3 | **GPT-4 baseline hallucinates far more** than the legal tools (abstract: "reduced relative to GPT-4"; figures variously cited 43%, and 58–82% on harder/incorrect slices). | PRIMARY (exact GPT-4 number — see C2note / OPEN-RESIDUE) |
| C4 | Per-tool accuracy / incompleteness (Auryth breakdown): Lexis+ AI ~65% accurate / 18% incomplete; Westlaw ~42% / 25%; Ask Practical Law ~19% accurate / **62% incomplete**. | RELATED (corroborating; exact crosstab not in arXiv abstract) |
| C5 | Evaluation used **202 preregistered open-ended queries**, hand-scored by legal experts. | PRIMARY |
| C6 | This is the **first preregistered empirical evaluation** of proprietary RAG legal-research tools. | PRIMARY |

> C3note: The exact GPT-4 hallucination figure differs across summaries (43% vs 58–82%
> depending on slice). Treat "GPT-4 worse than the legal tools" as PRIMARY; the precise
> single number is OPEN-RESIDUE pending the full PDF crosstab.

## The groundedness-vs-correctness distinction (PRIMARY — the conceptual core)

| ID | Claim | Tag |
|----|-------|-----|
| C7 | The paper splits response quality into **two independent axes: correctness** (is the legal proposition factually right and relevant?) and **groundedness** (do the cited sources actually support the proposition?). | PRIMARY |
| C8 | A **hallucination** is defined as a response that is **"incorrect OR misgrounded."** Being correct is not sufficient — a correct answer with bogus citation support still counts as a hallucination. | PRIMARY |
| C9 | Scoring uses three categorical labels: **accurate** (correct AND grounded), **incomplete** (refusal or correct-but-ungrounded/partial), **hallucinated** (incorrect OR misgrounded). | PRIMARY |
| C10 | Correctness has values **correct / incorrect / refusal**; groundedness has values **grounded / misgrounded / ungrounded** and is assessed **only for correct responses**. | PRIMARY |
| C11 | A **misgrounded** citation: the cited case is real and the legal statement may sound right, **but the source does not actually support the claim**. This is the subtle, dangerous failure RAG does NOT eliminate. | PRIMARY |

## Retrieval-failure attribution & failure modes (PRIMARY)

| ID | Claim | Tag |
|----|-------|-----|
| C12 | Errors are attributed to **two failure stages: retrieval failure** (irrelevant/poor documents retrieved) **vs generation failure** (model misinterprets the documents it did retrieve). | PRIMARY |
| C13 | A response can be **correct yet misgrounded** when **retrieval is poor** but the model happens to produce the right answer and falsely attributes it to an unrelated source. | PRIMARY |
| C14 | Documented generation failure modes: misunderstanding case holdings; confusing litigant arguments with the court's opinion; misrepresenting which courts control precedent; attributing dissent to the majority. | PRIMARY |
| C15 | **Sycophancy / false-premise failure:** when a user asserts an incorrect legal premise, tools often produce plausible supporting arguments rather than correcting the user. (22 false-premise queries in dataset.) | PRIMARY / RELATED |

## RAG and vendor claims (PRIMARY)

| ID | Claim | Tag |
|----|-------|-----|
| C16 | Vendors marketed these tools as **"eliminating," "avoiding," or "hallucination-free"** (Casetext 2023, Thomson Reuters 2023, LexisNexis 2023 "100% hallucination-free linked legal citations"). | PRIMARY |
| C17 | The paper's central conclusion: **"providers' claims are overstated."** RAG **reduces** but does not **eliminate** hallucination. | PRIMARY |
| C18 | RAG reduces hallucination by grounding generation in retrieved authority, but **retrieval quality and citation-faithfulness become the new failure surfaces**. | PRIMARY / LOCAL-INFERENCE |

## Methodology / scope (PRIMARY)

| ID | Claim | Tag |
|----|-------|-----|
| C19 | Dataset categories: general legal research (80), jurisdiction/time-specific (70), false-premise (22), factual recall (30). | PRIMARY |
| C20 | Systems are **closed/black-box**; the audit is behavioural (input→output), making systematic assessment hard and motivating manual scoring. | PRIMARY |
| C21 | The four contributions: (1) first systematic assessment of leading legal-research AI; (2) a preregistered 200+ query dataset; (3) a refined hallucination typology; (4) characterizing failure to inform professional-responsibility duties. | PRIMARY |

## Professional-responsibility implications (PRIMARY)

| ID | Claim | Tag |
|----|-------|-----|
| C22 | Because tools hallucinate at material rates, **lawyers retain ultimate responsibility** to supervise and verify AI output; "professional verification remains essential." | PRIMARY |
| C23 | How responsibility should be allocated between vendor and user is framed as a **central open question** for responsible AI-in-law. | PRIMARY |

## Local inferences / operator readings (NOT the authors' claims)

| ID | Claim | Tag |
|----|-------|-----|
| C24 | The correctness×groundedness split is the single most transferable asset of the paper: it is a **scoring rubric**, not a US-law fact, so it ports to any RAG QA system including Jus IA. | OPERATOR-READING |
| C25 | "Misgrounded but correct" is the failure a naive citation-link check (does the cited case exist?) will **miss** — link-validity ≠ support-faithfulness. | LOCAL-INFERENCE |
| C26 | For Jus IA's research-assistant feature (similar jurisprudence, main theses), the highest-risk failure is **misgrounding**: real Brazilian decisions cited that don't support the stated thesis. | OPERATOR-READING |
| C27 | The 62% incompleteness of Ask Practical Law AI shows a **safety-via-refusal** strategy — fewer hallucinations bought with less usefulness; a product-design tradeoff Jusbrasil must dial deliberately. | OPERATOR-READING |

## Cross-domain mappings (ANALOGY ONLY)

| ID | Claim | Tag |
|----|-------|-----|
| C28 | US common-law caselaw retrieval ≈ Brazilian jurisprudência retrieval; precedent-control errors ≈ confusing súmula/tribunal hierarchy. | ANALOGY |
| C29 | The exact 17–33% band is **NOT** transferable to Jus IA — it is product-, corpus-, and language-specific. Brazilian Portuguese + civil-law corpus could be higher or lower. | ANALOGY / LOCAL-INFERENCE |

## Open residue (asserted but unverified here)

| ID | Claim | Tag |
|----|-------|-----|
| C30 | The full per-tool **correctness × groundedness crosstab counts** (how many correct-but-misgrounded vs incorrect). | OPEN-RESIDUE |
| C31 | The single exact **GPT-4 hallucination percentage** (43% vs 58–82% conflict across summaries). | OPEN-RESIDUE |
| C32 | Inter-rater reliability / scoring agreement among the expert annotators. | OPEN-RESIDUE |
| C33 | Whether Westlaw's higher rate (33%) is retrieval-driven or generation-driven (per-tool failure-stage split). | OPEN-RESIDUE |
