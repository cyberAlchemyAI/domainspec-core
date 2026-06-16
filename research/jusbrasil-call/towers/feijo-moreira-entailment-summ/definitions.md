# definitions.md — Governed Definitions

These are the canonical definitions the rest of the tower relies on. Each notes its source basis.

## D1. LegalSumm (governed)
**Definition.** A pipeline for abstractive legal summarization that (a) constructs multiple **views** over a long source ruling, (b) generates an **independent candidate summary per view** with a trained summarization model, and (c) uses a **textual-entailment module** to score each candidate's faithfulness to the source and **select** the best.
**Basis:** primary-source (paper abstract) + local-inference for per-view granularity. Internal model identities are open-residue.

## D2. View (governed)
**Definition.** A bounded segment/projection of the source ruling produced so that the (input-length-limited) encoder can process the document; each view yields one candidate summary.
**Basis:** primary-source names "views"; segmentation mechanics are local-inference (open-residue for exact algorithm).

## D3. Entailment / faithfulness gate (governed)
**Definition.** An NLI-based check treating source = premise, candidate summary = hypothesis; a higher entailment score means the summary is better supported by the source. Used as a **selector** (rank/choose candidates), not as a generator.
**Basis:** primary/related-source. The specific NLI model and training data are open-residue.

## D4. Gold summary = ementa (governed)
**Definition.** The training/evaluation target is the human-authored `ementa` (official ruling headnote) from RulingBR; models learn source-text → ementa.
**Basis:** related-source (RulingBR).

## D5. Faithfulness (governed, evaluative)
**Definition.** Property that every assertion in a generated summary is supported by the source ruling; its negation is **hallucination**. Operationalized here via entailment scoring for candidate **selection**.
**Basis:** primary-source (problem framing) + operator-reading (operationalization).

## D6. Hallucination (governed, failure mode)
**Definition.** Generation of summary content that is unrelated to or unsupported by the source — the central risk the paper targets in a legal setting.
**Basis:** primary-source (abstract, verbatim term).
