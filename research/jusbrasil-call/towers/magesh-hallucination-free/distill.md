# Distill

## One-sentence model

RAG **reduces but does not eliminate** legal hallucination, because grounding generation
in retrieved sources just relocates the failure from *fabrication* to *misgrounding* —
so any honest audit must score **correctness and groundedness as two separate axes**,
which is exactly what leading vendors' "hallucination-free" marketing avoids.

## Compositional spine (how the audit works end to end)

```
  1. PREREGISTER          fix the query set + scoring rubric before testing
        │                 (202 open-ended queries: general / jurisdiction / false-premise / factual)
        ▼
  2. RUN BLACK-BOX        send each query to each closed tool; capture response + citations
        │                 (Lexis+ AI · Westlaw AIR · Ask Practical Law · GPT-4 baseline)
        ▼
  3. SCORE AXIS 1         correctness: correct / incorrect / refusal
        │                 (judged against the law, by expert humans)
        ▼
  4. SCORE AXIS 2         groundedness (only if correct): grounded / misgrounded / ungrounded
        │                 (did the cited source actually support the claim?)
        ▼
  5. BUCKET               accurate (correct+grounded) · incomplete (refusal/ungrounded) · hallucinated (incorrect OR misgrounded)
        │
        ▼
  6. ATTRIBUTE            for each failure: retrieval failure (bad docs) vs generation failure (misread docs)
        │
        ▼
  7. CONCLUDE             rates (17–33%) refute "hallucination-free"; assign verification duty to the lawyer
```

The spine is the borrowable artifact. Steps 1, 3–6 are domain-agnostic; only the corpus,
language, and expert scorers change.

## What to borrow for a Jus IA audit

- **The two-axis rubric (correctness × groundedness).** Adopt verbatim as the scoring
  schema for an internal Jus IA hallucination audit. This is the highest-value transfer.
- **The hallucination = "incorrect OR misgrounded" definition.** Forces the audit to
  catch misgrounding, the failure most relevant to "similar jurisprudence / main theses."
- **Preregistration discipline.** Fix Jus IA's query set + rubric before running — buys
  credibility and prevents metric-shopping.
- **A stratified query set.** Mirror the four strata: general doctrine, jurisdiction/
  court-hierarchy (STF/STJ/súmulas), **false-premise/adversarial**, and factual recall.
- **Retrieval-vs-generation attribution.** Tag each Jus IA failure by stage so eng knows
  whether to fix the retriever/index or the generation/prompt.
- **Incompleteness as a tracked cost.** Don't let "safe refusal" hide as success; report
  it (Ask Practical Law's 62% incomplete is the cautionary case).

## What is analogy-only

- **The specific 17–33% band.** Product-, corpus-, and language-specific. Jus IA's true
  rate on Brazilian Portuguese + civil-law jurisprudência is unknown until measured.
- **US precedent-hierarchy failure modes** (majority/dissent, controlling circuit) map
  *by analogy* to Brazilian equivalents (súmula vinculante, tribunal hierarchy) but the
  taxonomy of legal-reasoning errors must be re-derived for civil law.
- **Vendor-claim framing** (Casetext/Lexis/TR marketing) is context; Jusbrasil should set
  its own honest external messaging, not import US vendor language.

## What to block

- **Importing the band as a target/benchmark for Jus IA.** Never quote "we're under 17%"
  by analogy — measure locally or say nothing.
- **Citation-existence checks standing in for groundedness.** Blocked: link-validity does
  not detect misgrounding (Definition 4). An audit built only on "does the case exist"
  would falsely report near-zero hallucination.
- **Single blended accuracy score.** Blocked: collapses the diagnostic separation the
  whole method depends on.
- **Marketing "hallucination-free" / "eliminates hallucinations."** Blocked outright —
  the paper's entire thesis is that this claim is false for RAG legal tools.
