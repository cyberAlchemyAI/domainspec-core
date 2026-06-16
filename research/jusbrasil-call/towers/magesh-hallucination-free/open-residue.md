# Open Residue

Unresolved questions, what needs the full PDF, and follow-ups. IDs cross-reference
`claim-ledger.md`.

## Needs the full PDF / paywalled journal to close

- **R1 (C30).** The full **correctness × groundedness crosstab** per tool — how many
  responses were correct-but-misgrounded vs incorrect vs correct-and-grounded. Only the
  rolled-up accurate/incomplete/hallucinated buckets were recoverable.
- **R2 (C31).** The single **exact GPT-4 hallucination rate.** Fetched summaries conflict
  (43% in some; 58–82% on harder/incorrect slices in others). Resolve against the PDF
  results table.
- **R3 (C32).** **Inter-rater reliability** / annotator-agreement statistics for the
  expert legal scorers, and the exact scoring protocol/rubric wording.
- **R4 (C33).** **Per-tool retrieval-vs-generation attribution split** — is Westlaw's
  higher 33% driven by retrieval failure or generation failure? Drives whether the
  lesson for Jus IA is "fix retrieval" or "fix generation."
- **R5.** Exact wording of the authors' **definitions** of correctness/groundedness/
  hallucination as printed in §4 (we have faithful paraphrases + short quotes from the
  HTML and summaries, not the full definitional prose).
- **R6 (C4).** Confirm the **per-tool accuracy/incompleteness figures** directly from the
  paper's results tables (currently corroborated via Auryth third-party breakdown).
- **R7.** Appendix detail: the **full 202-query list**, the per-category query design
  rationale, and the **"running queries" / evaluation** appendices (methods reproducibility).

## Source-access follow-ups

- The arXiv **PDF fetched as binary/garbled**; the arXiv **HTML v1** was the usable text
  source. Re-extract from a clean PDF (or the law.stanford.edu mirror
  `Legal_RAG_Hallucinations.pdf`) to close R1–R7.
- The **Wiley JELS page returned HTTP 403** (paywall). The 2025 peer-reviewed version may
  differ from the 2024 preprint — check for revised numbers or expanded taxonomy.
- The **Sedona Conference PDF** mirror returned 403; the **Stanford HAI** news page
  returned no body on direct fetch (captured via search snippet only).

## Open conceptual questions for the Jusbrasil application

- **Q1.** How does **groundedness translate to Brazilian civil law** — ementa vs inteiro
  teor, súmula vinculante, persuasive vs binding precedent? The US support-relation
  rubric needs a localized definition (see `bridge-decisions.md` B9/B15).
- **Q2.** What is **Jus IA's actual hallucination rate** on a comparable preregistered
  Portuguese-language set? Entirely unknown — must be measured, not inferred (C29/B8).
- **Q3.** Does Jus IA exhibit the **sycophancy/false-premise failure**, and at what rate,
  on Brazilian leading-question prompts? (B5.)
- **Q4.** What is Jus IA's **incompleteness/refusal rate**, and where should the
  safety-vs-usefulness dial sit for its lawyer users? (C27/B7.)
- **Q5.** Does the **2025 journal version** add any taxonomy refinement or numbers absent
  from the 2024 preprint we grounded on?

## Residue count: 12 open items (R1–R7, Q1–Q5).
