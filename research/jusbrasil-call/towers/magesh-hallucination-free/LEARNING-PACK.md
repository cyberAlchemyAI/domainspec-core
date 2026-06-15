# LEARNING PACK — Magesh et al., "Hallucination-Free?" (2024/2025)

The 10-minute accelerator. Source-backed claims, the operator model, borrow/block
decisions, the 5 things to remember for the Jusbrasil call, and an honest cutoff.

---

## Source-backed claims (PRIMARY unless noted)

- Leading RAG legal-research tools **hallucinate 17–33% of the time** — not zero.
  Per tool: **Lexis+ AI 17%**, **Westlaw AI-Assisted Research 33%**, **Ask Practical
  Law AI 17%**. GPT-4 baseline is substantially worse (exact figure varies by slice —
  see cutoff).
- It is the **first preregistered empirical audit** of these closed RAG tools, over
  **202 hand-scored, expert-evaluated open-ended queries**.
- Vendors claimed RAG **"eliminates" / "avoids"** hallucination, even **"100%
  hallucination-free linked legal citations."** The paper's verdict: **"providers'
  claims are overstated."** RAG **reduces, not eliminates.**
- The conceptual core: hallucination is defined as **"incorrect OR misgrounded,"**
  split across two axes — **correctness** (is the legal answer right?) and
  **groundedness** (do the cited sources actually support it?).
- The signature failure RAG does NOT fix is **misgrounding**: a real, valid citation
  to a source that **does not actually support the claim** — invisible to "does the
  case exist?" checks.
- Failures attribute to two stages: **retrieval failure** (bad documents retrieved) vs
  **generation failure** (model misreads good documents — misstates holdings, swaps
  majority/dissent, mis-ranks controlling precedent).
- A distinct failure: **sycophancy / false-premise** — when a user asserts a wrong legal
  premise, tools tend to support it rather than correct it (22 such queries in the set).
- Conclusion: lawyers **retain ultimate responsibility to verify**; how duty splits
  between vendor and user is a **central open question.**

## Operator model (one sentence)

RAG relocates legal hallucination from *fabrication* to *misgrounding*, so an honest
audit scores **correctness and groundedness separately** and reports the union of their
failures — which is precisely what "hallucination-free" marketing hides.

## Borrow / block for Jus IA

**Borrow (carefully):** the two-axis rubric; the "incorrect OR misgrounded" definition;
preregistration; a stratified query set incl. false-premise; retrieval-vs-generation
attribution; incompleteness as a tracked cost.

**Analogy-only:** the 17–33% band (NOT a Jus IA number); US precedent-hierarchy error
taxonomy (re-derive for civil law); the GPT-4 baseline comparison.

**Block:** "hallucination-free" marketing language; citation-existence as a groundedness
proxy; a single blended accuracy score.

**Promotion-candidate:** a preregistered internal Jus IA hallucination audit built from
the borrowed pieces (LOCAL-ONLY).

## The 5 things to remember for the call

1. **"Hallucination-free" is refuted for this exact product category** — leading RAG
   legal tools still hallucinate **17–33%** (Magesh et al., Stanford, JELS 2025).
2. **The transferable asset is the rubric, not the numbers** — correctness ×
   groundedness, with hallucination = "incorrect OR misgrounded." That ports straight to
   Jus IA; the percentages do not.
3. **Misgrounding is the failure to hunt** — real citation, wrong support; it survives
   link-validation and is the core risk for "similar jurisprudence / main theses."
4. **An honest audit must be preregistered, stratified (incl. false-premise), and
   human-scored** — and must track incompleteness as a cost, not a win.
5. **Verification duty stays with the lawyer** — frame Jus IA as augmenting, with
   citations a lawyer can check, never as eliminating the need to check.

## Honest cutoff — what we could NOT verify from fetched material

- The **exact GPT-4 hallucination percentage** — summaries conflict (43% vs 58–82% on
  different slices). "GPT-4 worse than the legal tools" is solid; the single number is not.
- The **full correctness × groundedness crosstab counts** (how many correct-but-
  misgrounded vs incorrect per tool) — not in the abstract/HTML we extracted.
- **Inter-rater reliability** of the expert scorers — not captured.
- The **per-tool retrieval-vs-generation split** (is Westlaw's 33% retrieval- or
  generation-driven?) — not captured.
- Per-tool **accuracy/incompleteness figures (C4)** are from a corroborating third-party
  breakdown (Auryth), consistent with the abstract but not directly re-read from the
  paper's results tables.
- The arXiv **PDF was binary/garbled** and the **Wiley journal page was paywalled (403)**;
  grounding rests on the arXiv abstract + arXiv HTML v1 + Stanford HAI summary +
  corroborating third-party write-ups. Full-PDF confirmation is in `open-residue.md`.
