# LEARNING-PACK.md — Feijó & Moreira (2023), Entailment-Filtered Legal Summarization

**For:** the Jusbrasil ("Jus IA") call. **Lens:** smart-summaries + faithfulness control.
**Status:** source-backed where possible; numerics are open-residue (paywall). Date: 2026-06-10.

---

## 1. Source-backed claims (what the paper actually says)
- Abstractive summarizers (encoder–decoder) write fluent, human-like summaries but can **hallucinate** — assert unrelated/unsupported facts. *(primary-source)*
- In **legal** use this is high-stakes: practitioners rely on ruling summaries to find **precedents** for legal arguments, so a wrong summary misleads. *(primary-source)*
- Legal rulings are **long** and may exceed the encoder's input limit. *(primary-source)*
- Their method **LegalSumm**: build multiple **views** over the source, generate **independent candidate summaries**, and apply **textual entailment** to judge faithfulness and **select** candidates. *(primary-source)*
- The entailment-based selection **improved ROUGE across all metrics evaluated** (direction only; exact figures are open-residue). *(primary-source, numbers paywalled)*
- Data is **RulingBR**: ~10K Brazilian Supreme Court (STF) rulings, 2011–2018; each ruling's human-written **`ementa` is the gold summary**; sections `ementa/relatório/voto/acórdão` + metadata. *(related-source)*

## 2. Operator model (how it works, in one breath)
Don't trust one draft. **Generate several ementa drafts from different slices of the ruling, then keep the draft the source text most clearly entails.** Faithfulness is enforced by a *selector* (an NLI model scoring source⊨summary), so the base generator doesn't have to be perfect — a cheap, model-agnostic guardrail.

## 3. Faithfulness takeaways (the part Jus IA cares about most)
1. **Entailment ≈ faithfulness signal.** Treat source = premise, summary = hypothesis; high entailment ⇒ supported ⇒ less hallucination. Reusable as a gate over *any* generator (including an LLM).
2. **Candidate-and-rerank beats single-shot** for trustworthiness: the win comes from *selection*, not a better decoder.
3. **ROUGE is necessary but not sufficient.** It rewards overlap with the gold ementa; it can miss legal-substantive errors (wrong holding, wrong citation). Pair the entailment gate with human/qualitative faithfulness review. *(operator-reading)*
4. **Length handling and faithfulness are linked**: chunk-then-select both fits long rulings and creates the candidate pool the entailment gate ranks.

## 4. Five things for the call
1. **Closest published analogue to Jus IA smart summaries**: same target (STF ementa), same dataset family (RulingBR), explicit **hallucination/faithfulness** focus.
2. **Adopt the pattern, not the 2023 weights**: *summarize → entailment-score → select* is model-agnostic and bolts onto a modern LLM generator.
3. **Faithfulness as a measurable gate**: pitch an NLI/entailment scorer (source⊨summary) as a production guardrail + offline regression metric, tuned on Jus IA's court mix.
4. **Be honest about evidence**: cite the *direction* ("improves ROUGE across metrics, targets hallucination") — **do not quote specific ROUGE numbers** (paywalled / open-residue).
5. **Data leverage**: RulingBR is an open seed corpus (github.com/diego-feijo/rulingbr) — check its license before any commercial reuse, and plan to extend beyond STF/2011–2018.

## 5. Honest cutoff
- Paper full text is **paywalled** (Springer 303→SSO). Abstract + bibliographic metadata + method gist recovered from open indexes; RulingBR details from the PROPOR'18 paper/repo.
- **Unverified (open-residue):** base model identity, NLI model/corpus, exact ROUGE figures, view/candidate counts, dataset split sizes, whether hallucination was measured directly, RulingBR license. See `open-residue.md` (10 items).
- The open UFRGS thesis (lume 10183/230669) was downloaded but **not text-extractable in this environment** — best next source to close OR1–OR7.
- **No numbers were invented.** Bridge/analogy items are Arcanum readings, labeled as such in `claim-ledger.md`, not source claims.
