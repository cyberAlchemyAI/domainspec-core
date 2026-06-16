# Claim Ledger

Source-kind labels: **[PRIMARY]** = stated in S1 (ACL landing/abstract/BibTeX). **[RELATED]** = S2/S3 lineage/context. **[OPEN-RESIDUE]** = not verified from accessible source; do not fabricate. **[READING]** = Arcanum interpretation, not a paper claim.

## Primary-source claims (S1)

| ID | Claim | Label | Source |
|---|---|---|---|
| C1 | UlyssesLegalNER-Br is a corpus of Brazilian legal documents for NER covering **bills, case laws, and laws**. | [PRIMARY] | S1 abstract |
| C2 | It includes the **first NER corpus based exclusively on Brazilian laws**. | [PRIMARY] | S1 abstract |
| C3 | It **expands the UlyssesNER-Br corpus**, previously focused only on the Brazilian legislative domain. | [PRIMARY] | S1 abstract |
| C4 | The corpus has **560 public documents**. | [PRIMARY] | S1 abstract |
| C5 | Documents annotated using a **hybrid approach**. | [PRIMARY] | S1 abstract |
| C6 | Schema is organized in **9 categories and 23 fine-grained types**. | [PRIMARY] | S1 abstract |
| C7 | Baseline architectures: **CRF, BiLSTM, and BERTimbau**. | [PRIMARY] | S1 abstract |
| C8 | Evaluated on predictive performance, **computational cost**, and label-level results. | [PRIMARY] | S1 abstract |
| C9 | Best **micro F1 = 96.18%**, achieved by **BERTimbau on the unified corpus**. | [PRIMARY] | S1 abstract |
| C10 | At label level, **6 categories and 7 types** scored F1 > 95%; lowest scores fell in the **71–82%** interval. | [PRIMARY] | S1 abstract |
| C11 | Authors (9) led by Hidelberg O. Albuquerque; senior authors incl. Adriano L. I. Oliveira and André C. P. L. F. de Carvalho. | [PRIMARY] | S1 BibTeX |
| C12 | Venue PROPOR 2026, Salvador, Brazil, April 2026; pages 331–341; ISBN 979-8-89176-387-6. | [PRIMARY] | S1 BibTeX |

## Related-source claims (S2 / S3)

| ID | Claim | Label | Source |
|---|---|---|---|
| R1 | Predecessor **UlyssesNER-Br** family: PL-corpus (Chamber of Deputies bills + legislative consultations), C-corpus (user comments on bills), ST-corpus (referenced). | [RELATED] | S2 |
| R2 | Predecessor UlyssesNER-Br reported metrics: CRF 80.8% (categories)/81.04% (types); BiLSTM-CRF+GloVe 76.89% (cat)/59.67% (types); fine-tuned BERT 73.90%. **These are the OLD corpus, not UlyssesLegalNER-Br.** | [RELATED] | S2 |
| R3 | **LeNER-Br** (PROPOR 2018) is the foundational Brazilian legal NER dataset; UlyssesNER-Br/UlyssesLegalNER-Br are successors in that line. | [RELATED] | S3 |
| R4 | **CDJUR-BR** (arXiv 2305.18315) is a parallel fine-grained Brazilian legal NER golden collection — adjacent SOTA context. | [RELATED] | S3 |
| R5 | README lists no explicit license / download links / UlyssesLegalNER-Br-specific section. | [RELATED] | S2 |

## Open-residue claims (NOT verified — see open-residue.md)

| ID | Item | Label |
|---|---|---|
| O1 | The **names** of the 9 categories and 23 fine-grained types. | [OPEN-RESIDUE] |
| O2 | Per-label F1 table (which 6 categories / 7 types exceed 95%; which sit at 71–82%). | [OPEN-RESIDUE] |
| O3 | Document-count split across bills / case laws / laws; train/dev/test splits. | [OPEN-RESIDUE] |
| O4 | Definition of "hybrid approach" annotation (manual + automatic? IAA scores?). | [OPEN-RESIDUE] |
| O5 | Definition of "unified corpus" (merge of all three doc types vs. per-domain). | [OPEN-RESIDUE] |
| O6 | Computational-cost numbers (train/inference time, params). | [OPEN-RESIDUE] |
| O7 | License and public download URL for UlyssesLegalNER-Br data/models. | [OPEN-RESIDUE] |
| O8 | Tagging scheme (BIO/BILOU) and tokenization details. | [OPEN-RESIDUE] |

## Arcanum readings (interpretation only — not paper claims)

| ID | Reading | Label |
|---|---|---|
| A1 | The 96.18% micro F1 on the *unified* corpus suggests cross-domain training helps; the 71–82% floor likely tracks rare/ambiguous fine-grained types (relevant to Jusbrasil normalization edge cases). | [READING] |
| A2 | "First NER corpus exclusively on Brazilian laws (statutes)" fills the exact gap between LeNER-Br (case law focus) and UlyssesNER-Br (legislative bills) — completing the bill/case-law/statute triad Jusbrasil ingests. | [READING] |

## Appendix — BibTeX (verbatim, S1)

```bibtex
@inproceedings{albuquerque-etal-2026-ulysseslegalner,
    title = "{U}lysses{L}egal{NER}-Br: from Legislative to Legal, a comprehensive corpus of {B}razilian legal documents for Named Entity Recognition",
    author = "Albuquerque, Hidelberg O.  and Souza, Ellen  and Lucena, Danilo C. G.  and Albuquerque, H{\'e}ldon J. O.  and Silva, N{\'a}dia F. F. da  and Dias, M{\'a}rcio de S.  and Nunes, Rafael O.  and Oliveira, Adriano L. I.  and Carvalho, Andr{\'e} C. P. L. F. de",
    booktitle = "Proceedings of the 17th International Conference on Computational Processing of {P}ortuguese ({PROPOR} 2026) - Vol. 1",
    month = apr, year = "2026", address = "Salvador, Brazil",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.propor-1.33/",
    pages = "331--341", ISBN = "979-8-89176-387-6"
}
```
