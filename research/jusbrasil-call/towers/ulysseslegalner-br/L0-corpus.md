# L0-corpus — Source Record

**Date checked:** 2026-06-10
**Fetch method:** WebFetch (markdown conversion) + WebSearch corroboration.

## Source S1 — ACL Anthology landing page (PRIMARY)

- **URL:** https://aclanthology.org/2026.propor-1.33/
- **Anthology ID:** 2026.propor-1.33
- **PDF:** https://aclanthology.org/2026.propor-1.33.pdf
- **Accessibility (2026-06-10):** Landing page accessible. Abstract + full BibTeX captured verbatim. **PDF body NOT fetched** in this build -> fine-grained enumeration of the 9 categories / 23 types is open-residue.
- **Title (full):** "UlyssesLegalNER-Br: from Legislative to Legal, a comprehensive corpus of Brazilian legal documents for Named Entity Recognition"
- **Authors (9):** Hidelberg O. Albuquerque; Ellen Souza; Danilo C. G. Lucena; Héldon J. O. Albuquerque; Nádia F. F. da Silva; Márcio de S. Dias; Rafael O. Nunes; Adriano L. I. Oliveira; André C. P. L. F. de Carvalho
- **Venue:** PROPOR 2026 (17th International Conference on Computational Processing of Portuguese) — Vol. 1, Salvador, Brazil, April 2026, ACL.
- **Pages:** 331–341. **ISBN:** 979-8-89176-387-6.

### Section map (from landing page)

| Section | Captured? | Notes |
|---|---|---|
| Title / authors / venue / pages / ISBN | Yes | Verbatim from page + BibTeX |
| Abstract | Yes (verbatim) | See claim-ledger C1–C8 |
| BibTeX | Yes (verbatim) | Stored in claim-ledger appendix |
| Introduction / Related Work | No | PDF body only — open-residue |
| Corpus construction / annotation method | Partial | "hybrid approach" named in abstract; details open-residue |
| Entity schema enumeration (9 cat / 23 types) | No | Counts known; names open-residue |
| Experiments / per-label F1 tables | Partial | Headline F1 known; full tables open-residue |
| Computational cost analysis | No | Named in abstract; numbers open-residue |

### Abstract (verbatim, S1)

> "The legal domain presents several challenges for Natural Language Processing (NLP), particularly due to its linguistic complexity and lack of public datasets. Named Entity Recognition (NER), a subarea of NLP, has been successfully used to extract useful knowledge from legal texts. Its widespread use is limited by the lack of legal text corpora. This paper introduces UlyssesLegalNER-Br, a comprehensive corpus of Brazilian legal documents for NER, covering bills, case laws and laws, including the first NER corpus based exclusively on Brazilian laws. This research expand the UlyssesNER-Br corpus, previously focused only on the Brazilian legislative domain. The proposed corpus has 560 public documents annotated using a hybrid approach, organized in 9 categories and 23 fine-grained types, experimentally evaluated with the CRF, BiLSTM, and BERTimbau architectures. The corpus was experimentally evaluated regarding predictive performance, computational cost and label-level results. The best micro F1 96.18% was achieved by BERTimbau on the unified corpus, providing a strong baseline for Brazilian legal NER. At the label level, six categories and seven types presented a F1-score above 95%, while the lowest were distributed in the interval 71-82%."

## Source S2 — GitHub README (RELATED / predecessor resources)

- **URL:** https://github.com/ulysses-camara/ulysses-ner-br
- **Accessibility (2026-06-10):** Accessible. Describes the **predecessor UlyssesNER-Br** family, NOT a dedicated UlyssesLegalNER-Br section.
- **Captured:** corpus versions PL-corpus v1/v2 (Chamber of Deputies bills + legislative consultations), C-corpus v1/v2 (user comments on bills), ST-corpus (referenced, not detailed). Models: CRF, HMM, BiLSTM-CRF+GloVe, fine-tuned BERT. Predecessor metrics (UlyssesNER-Br): CRF 80.8% (categories) / 81.04% (types); BiLSTM-CRF/GloVe 76.89% (cat) / 59.67% (types); fine-tuned BERT 73.90%.
- **Missing from README:** explicit license, dataset download links, UlyssesLegalNER-Br-specific section, full entity-type definitions.
- **Aux:** results spreadsheet https://docs.google.com/spreadsheets/d/1uygceS1sOaSLkBWRXzevWAcWoCNWUbv8-nppoisOXio/

## Source S3 — Web search corroboration (RELATED / context)

- Confirms S1 abstract figures. Surfaces lineage anchors: **LeNER-Br** (PROPOR 2018, first Brazilian legal NER dataset), **UlyssesNER-Br** (legislative corpus, 2022), **CDJUR-BR** (arXiv 2305.18315, fine-grained legal NER golden collection). These are related-source context, not claims of this paper.

## Accessibility note

This build relied on the publicly accessible landing page (S1) and README (S2). The **paper PDF body was not ingested**, so any claim requiring the body (schema names, per-label tables, dataset splits, annotation-protocol detail, computational-cost numbers) is recorded as open-residue and must NOT be fabricated. Re-running WebFetch on the PDF URL would close most residue.
