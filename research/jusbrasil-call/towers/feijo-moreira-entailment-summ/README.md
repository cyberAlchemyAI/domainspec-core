# Research Tower — Feijó & Moreira: Entailment-Filtered Legal Summarization

**Lane:** `feijo-moreira-entailment-summ`
**Paper:** "Improving abstractive summarization of legal rulings through textual entailment" (de Vargas Feijó & Moreira, 2023, *Artificial Intelligence and Law* 31(1): 91–113). DOI: 10.1007/s10506-021-09305-4
**Built:** 2026-06-10 · **Depth:** standard · **Promotion:** LOCAL-ONLY (no arcanum submodule writes)

## Why this paper for the Jusbrasil call
This is the closest published analogue to **Jus IA's smart-summaries feature**. The paper:
- Generates **ementa-style** abstractive summaries of Brazilian Supreme Court (STF) rulings.
- Uses the **RulingBR** dataset (PROPOR 2018), where the human-written `ementa` is the gold summary.
- Introduces **LegalSumm**, which uses **textual entailment (NLI)** to score candidate summaries for faithfulness to the source and select the most faithful — directly mapping to **faithfulness/hallucination control** in smart summaries.

## How to read this tower (suggested order)
1. `LEARNING-PACK.md` — start here. Source-backed claims, operator model, 5 things for the call, honest cutoff.
2. `TOWER.md` — map of the tower and file roles.
3. `distill.md` — one-sentence model + compositional spine.
4. `glossary.md` / `definitions.md` — terms (ementa, NLI, faithfulness, RulingBR, abstractive summarization).
5. `claim-ledger.md` — every claim with a source-kind label.
6. `L0-corpus.md` — source record, section map, accessibility note.
7. `bridge-decisions.md` — mapping decisions to Jus IA.
8. `open-residue.md` — what is still behind the paywall / unverified.

## Accessibility note
The Springer landing page is **paywalled** (303 redirect to an SSO authorize endpoint). Abstract, bibliographic metadata, and method gist were recovered from open indexes (dblp, ACM/Springer metadata, researchgate listing) and the related open thesis/dataset. **Exact internal numbers (ROUGE tables, dataset split counts, NLI model identity) are open-residue** — see `open-residue.md`. Never invent numbers.
