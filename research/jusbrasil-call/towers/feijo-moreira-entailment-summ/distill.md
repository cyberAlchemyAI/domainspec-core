# distill.md — Smallest Coherent Model

## One-sentence model
**LegalSumm fights summary hallucination not by making the generator perfect, but by generating several candidate ementa-summaries from different views of a long ruling and then using a textual-entailment model to pick the candidate most faithfully supported by the source.**

## Compositional spine
```
Long legal ruling (RulingBR)
        │
        ▼
[1] VIEW CONSTRUCTION ── split/project source into multiple bounded views
        │                 (handles encoder length limit)
        ▼
[2] CANDIDATE GENERATION ── encoder-decoder summarizer → one candidate per view
        │                    (multiple independent draft ementas)
        ▼
[3] ENTAILMENT SCORING ── NLI module: source(premise) ⊨ candidate(hypothesis)?
        │                   score = faithfulness
        ▼
[4] SELECTION ── keep the most-entailed candidate
        │
        ▼
Output ementa-style summary  ── more faithful + higher ROUGE
```

## Borrow / Analogy / Block

**BORROW (directly reusable for Jus IA smart summaries):**
- The **candidate-generate → entailment-rerank → select** loop as a hallucination guardrail bolted onto any base summarizer.
- Using an **NLI/entailment score as the faithfulness signal** (premise=source, hypothesis=summary).
- **Multi-view / chunking** of long documents to respect encoder limits.
- Treating the **ementa as the gold target** — exactly Jus IA's product target.

**ANALOGY (map with care):**
- "Improves ROUGE" ≠ "improves user-perceived faithfulness" directly; ROUGE rewards overlap with the gold ementa. For Jus IA, pair with human/qualitative faithfulness review.
- Their entailment model was built for STF Portuguese legal text; Jus IA's domain (broader Brazilian courts) may need a re-trained/re-tuned entailment scorer.

**BLOCK (do not borrow blindly):**
- Exact architecture, NLI model, view count, and ROUGE deltas are **open-residue** — do not cite numbers in the call.
- 2023 method predates current LLM summarizers; the *pattern* transfers, but the *base generator* should be modernized (the entailment-selection idea is model-agnostic).
- Don't assume the entailment gate catches all legal-substantive errors (citation/holding errors may still pass surface entailment).
