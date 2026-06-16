# Bridge Decisions — Applying Magesh et al. to Jusbrasil / Jus IA

Each row carries one explicit status:
**BORROW-CAREFULLY** · **ANALOGY-ONLY** · **BLOCK** · **PROMOTION-CANDIDATE** · **FUTURE-WORK**.

Context: Jus IA is a RAG legal-research assistant (smart summaries, main theses, similar
jurisprudence, transcription). The research-assistant feature is the direct analogue of
the tools this paper audits. Jusbrasil itself names hallucination risk as a core NLP
challenge — this paper is its closest published mirror.

---

| # | Item from paper | Decision | Rationale / how to apply |
|---|-----------------|----------|--------------------------|
| B1 | **Correctness × groundedness two-axis rubric** | **BORROW-CAREFULLY** | Adopt as the scoring schema for an internal Jus IA audit. "Carefully" = re-validate the groundedness criterion against Brazilian citation conventions (acórdãos, súmulas, ementa vs. inteiro teor). |
| B2 | **Hallucination = "incorrect OR misgrounded"** | **BORROW-CAREFULLY** | Use as the headline audit metric. Ensure misgrounding is human/LLM-verified against the *inteiro teor*, not just citation existence. |
| B3 | **Preregistration of query set + rubric** | **BORROW-CAREFULLY** | Preregister Jus IA's audit set before testing for defensibility. Internal preregistration (dated, version-controlled) is enough; public preregistration is a later option. |
| B4 | **Stratified query set (4 categories)** | **BORROW-CAREFULLY** | Build Jus IA strata: general doutrina, jurisdiction/tribunal-hierarchy, false-premise/adversarial, factual recall. Sizes/weights must reflect real Jus IA usage, not copy the US 80/70/22/30. |
| B5 | **False-premise / sycophancy test category** | **BORROW-CAREFULLY** + **PROMOTION-CANDIDATE** | High value: lawyers ask leading questions. Strong candidate to promote into a reusable Jusbrasil eval pattern. |
| B6 | **Retrieval-vs-generation failure attribution** | **BORROW-CAREFULLY** | Tag each failure by stage so the retriever/index team and the generation/prompt team get separated signal. |
| B7 | **Incompleteness tracked as a cost** | **BORROW-CAREFULLY** | Report Jus IA refusal/incompleteness rate alongside hallucination; tune the safety-vs-usefulness dial deliberately. |
| B8 | **The specific 17–33% hallucination band** | **ANALOGY-ONLY** | Indicates "material residual risk exists for RAG legal tools." NOT a Jus IA number or target. Never quote as our rate. |
| B9 | **US precedent-hierarchy / majority-dissent error taxonomy** | **ANALOGY-ONLY** | Conceptually maps to Brazilian súmula vinculante / tribunal hierarchy errors, but the civil-law error taxonomy must be re-derived, not transplanted. |
| B10 | **GPT-4 baseline comparison** | **ANALOGY-ONLY** + **FUTURE-WORK** | The "RAG beats raw chatbot" finding supports Jus IA's architecture choice; an internal Jus IA-vs-raw-LLM baseline is future-work. |
| B11 | **Vendor "hallucination-free" marketing language** | **BLOCK** | Do not adopt or echo. The paper's thesis is that this claim is false for RAG legal tools; using it would invite the same critique. |
| B12 | **Citation-existence check as a groundedness proxy** | **BLOCK** | Insufficient — misses misgrounding (Definition 4). Must not be the basis of any "hallucination-free" claim. |
| B13 | **Single blended accuracy metric** | **BLOCK** | Destroys the diagnostic separation; do not report Jus IA quality as one number. |
| B14 | **A preregistered internal Jus IA hallucination audit** | **PROMOTION-CANDIDATE** | The natural Jusbrasil deliverable seeded by this tower: rubric (B1/B2) + stratified preregistered set (B3/B4/B5) + attribution (B6) + cost tracking (B7). |
| B15 | **Portuguese / civil-law adaptation of the rubric** | **FUTURE-WORK** | Validate groundedness scoring against Brazilian sources; build a localized error taxonomy. |
| B16 | **Inter-rater reliability protocol for legal scorers** | **FUTURE-WORK** | Paper's IRR detail is open-residue; design Jus IA's scorer-agreement protocol from scratch. |

## Promotion boundary

All statuses are **LOCAL-ONLY**. PROMOTION-CANDIDATE means "candidate to become a
reusable Jusbrasil internal asset," **never** a write into the `arcanum` submodule.
