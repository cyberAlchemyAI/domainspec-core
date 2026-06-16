# claim-ledger.md — Claims with Source-Kind Labels

Labels: **primary-source** (2023 paper abstract/metadata) · **related-source** (RulingBR PROPOR'18 / thesis / repo) · **local-inference** · **analogy** (→ Jus IA) · **operator-reading** · **open-residue**.

Date checked: 2026-06-10.

## A. The problem framing

- **C1** The standard approach to abstractive summarization is an encoder–decoder: the encoder captures source meaning, the decoder generates the summary. — **primary-source** (abstract, near-verbatim).
- **C2** Such summaries can resemble human writing but may contain unrelated or unfaithful information; this is called **hallucination**. — **primary-source** (abstract).
- **C3** Hallucination is a serious issue for legal texts because legal practitioners rely on these summaries when searching for precedents to support legal arguments. — **primary-source** (abstract).
- **C4** Legal documents tend to be very long and may not be fed entirely to the encoder (input-length limit). — **primary-source** (abstract).

> Abstract verbatim (recovered via open search of Springer/ACM metadata): "The standard approach for abstractive text summarization is to use an encoder-decoder architecture. The encoder is responsible for capturing the general meaning from the source text, and the decoder is in charge of generating the final text summary. While this approach can compose summaries that resemble human writing, some may contain unrelated or unfaithful information. This problem is called 'hallucination' and it represents a serious issue in legal texts as legal practitioners rely on these summaries when looking for precedents, used to support legal arguments." — treat as recovered, not page-verified.

## B. The method (LegalSumm)

- **C5** The proposed method is named **LegalSumm**. — **primary-source** (abstract).
- **C6** LegalSumm creates different **"views"** over the source text. — **primary-source** (abstract). *Interpretation:* the long ruling is split/projected into multiple partial views so the (length-limited) encoder can be applied per view. — **local-inference**.
- **C7** It trains summarization models to generate **independent versions of summaries** (one candidate per view). — **primary-source** (abstract) + **local-inference** (one candidate per view).
- **C8** It applies an **entailment (NLI) module** to judge how faithful each candidate summary is with respect to the source text. — **primary-source / related-source** (stated in surfaced descriptions of the method).
- **C9** The entailment scores are used to **select** among candidate summaries (pick the most faithful / best-supported). — **primary-source** (the "select candidate summaries" claim).
- **C10** The selection approach **improves ROUGE in all metrics evaluated** vs. the base summarization output. — **primary-source** (surfaced result statement). *Exact ROUGE numbers:* **open-residue**.

## C. The data (ementa-as-gold setup)

- **C11** RulingBR contains ~10K rulings from the Brazilian Federal Supreme Court (STF), 2011–2018, parsed from stf.jus.br. — **related-source**.
- **C12** Each ruling has sections: `ementa`, `relatório`, `voto`, `acórdão`, plus metadata (`area`, `classe`, `relator`, `extrato`). — **related-source**.
- **C13** The human-written **`ementa` is used as the ground-truth / gold summary**; models learn to generate it from the fuller decision text. — **related-source**.
- **C14** RulingBR has shorter documents and summaries than typical English news datasets, and provides train/test/validation splits. — **related-source**. *Exact split counts & lengths:* **open-residue**.
- **C15** Dataset evolved across versions; v1.2 deduplicated (removed 49 near-identical samples) and added categorical metadata. — **related-source**.

## D. Bridge to Jus IA (analogy / readings — NOT source claims)

- **C16** LegalSumm's ementa-generation task ≈ Jus IA's **smart-summaries** feature (generate ementa-style summaries of court rulings). — **analogy**.
- **C17** The entailment module ≈ a **faithfulness gate**: an automatic check that a candidate summary is entailed by (supported by) the source before it is shown. — **analogy / operator-reading**.
- **C18** "Generate several candidates, score by entailment, select the most faithful" is a reusable **candidate-and-rerank pattern** for hallucination control that does not require the base generator to be perfect. — **operator-reading**.
- **C19** The "views over long source" technique is a pragmatic response to encoder length limits; for production it maps to **chunking + per-chunk generation + aggregation/selection**. — **operator-reading / local-inference**.

## E. Open-residue claims (do not fabricate)
- **OR1** Base summarization model / transformer architecture used. — **open-residue**.
- **OR2** Which NLI model / entailment dataset trained the entailment module (and language: Portuguese vs translated). — **open-residue**.
- **OR3** Exact ROUGE-1/2/L numbers, baseline vs LegalSumm. — **open-residue**.
- **OR4** Number of views, view-construction algorithm, candidate count. — **open-residue**.
- **OR5** RulingBR train/test/val sizes, token-length distributions. — **open-residue**.
- **OR6** Whether human/qualitative faithfulness evaluation was done beyond ROUGE. — **open-residue**.
