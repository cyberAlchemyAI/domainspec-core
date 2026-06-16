# Learning Pack — UlyssesLegalNER-Br

**Paper:** Albuquerque et al. (2026), PROPOR 2026. **Built:** 2026-06-10. **Depth:** standard.
Read this to understand and decompose the paper for the Jusbrasil call without reading it cover to cover.

## 1. Source-backed claims (all PRIMARY from S1 abstract/BibTeX unless noted)

1. UlyssesLegalNER-Br is a Brazilian legal NER corpus covering **bills, case laws, and laws**, including the **first NER corpus exclusively on Brazilian laws**. [C1, C2]
2. It **expands UlyssesNER-Br** (previously legislative-only) into the full legal domain. [C3]
3. **560 public documents**, **hybrid annotation**, **9 categories / 23 fine-grained types**. [C4, C5, C6]
4. Baselines: **CRF, BiLSTM, BERTimbau**; evaluated on predictive performance, **computational cost**, and label-level results. [C7, C8]
5. **Best micro F1 = 96.18%** (BERTimbau, unified corpus) — "a strong baseline for Brazilian legal NER." [C9]
6. Label level: **6 categories and 7 types > 95% F1**; lowest scores in **71–82%**. [C10]
7. *(Related)* Lineage: **LeNER-Br** (2018, case law) -> **UlyssesNER-Br** (legislative) -> this. **CDJUR-BR** is adjacent. [R1, R3, R4]
8. *(Related)* Predecessor UlyssesNER-Br metrics were far lower (CRF ~80–81%, BERT ~74%) — the new corpus + BERTimbau on the legal domain is a large jump. [R2]

## 2. Operator model (how the artifact "runs")

Input: a Brazilian legal document (bill | case law | statute).
-> Tokenize -> sequence-label each token with one of 23 fine-grained types (grouped into 9 categories).
-> Model = CRF | BiLSTM | **BERTimbau** (best).
Output: typed entity spans. Metric: micro F1 (96.18% ceiling on unified corpus).
**Stops at recognition.** Normalization/linking is downstream and not in this paper. [D6]

## 3. NER-pipeline takeaways (Jusbrasil ingestion: NER / entity normalization)

- The paper supplies a **ready reference for the recognition stage**: a tri-source corpus + a 9/23 schema + a BERTimbau baseline at ~96% micro F1. This is exactly the layer that precedes citation linking and jurisprudence organization. [B1, B4]
- It **closes the statute gap** — the first corpus built exclusively on enacted Brazilian laws — completing the bill/case-law/statute triad an ingestion pipeline must cover. [B2]
- "**Unified corpus** wins" hints a single cross-document-type NER model may beat per-source silos — but the merge semantics are unverified. [B5, O5]
- The **71–82% floor** flags the entity types where downstream **normalization/disambiguation** rules should concentrate — but which types is unknown until the PDF is read. [B6, O2]
- **Normalization itself is not a paper contribution** — do not credit the paper with citation linking. [B7, D6]

## 4. Five things for the call

1. **Headline:** 560 docs, 9 cat / 23 types, BERTimbau **96.18% micro F1** — a strong, citable baseline for Brazilian legal NER across bills + case law + statutes. [C4, C6, C9]
2. **Strategic fit:** it completes the **document-type triad** Jusbrasil ingests and is the **first corpus exclusively on statutes**, the historically thinnest stream. [C1, C2, B2]
3. **Model signal:** transformer (BERTimbau) decisively beats CRF/BiLSTM and beats the old UlyssesNER-Br numbers — validates a transformer-first NER ingestion stack. [C7, C9, R2]
4. **Risk/edge cases:** a per-label floor at **71–82%** means some entity types are still hard — those are the normalization-rule hotspots. [C10, B6]
5. **Open asks before adopting:** confirm the **23 type names** (schema alignment), the **license/download** (reuse rights), and "**unified corpus**" semantics. [O1, O5, O7]

## 5. Honest cutoff

This pack rests on the **publicly accessible landing page (abstract + BibTeX)** and the **GitHub README** (which documents the *predecessor* UlyssesNER-Br, not a dedicated UlyssesLegalNER-Br section). The **paper PDF body was NOT ingested** in this standard pass, so **10 items are open-residue** (open-residue.md): the actual category/type names, per-label tables, document splits, annotation-protocol detail, "unified corpus" definition, compute numbers, license, tagging scheme, data-publication location, and cross-corpus comparisons. **No numbers were invented.** Every figure here traces to the verbatim abstract/BibTeX (S1). Closing the residue requires one WebFetch on `https://aclanthology.org/2026.propor-1.33.pdf`.
