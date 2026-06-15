# L0 — Corpus & Source Record

**Date checked:** 2026-06-10 (all numbers below captured from the open-access article on this date)

## Source record

| Field | Value |
|---|---|
| Title | Using deep learning to predict outcomes of legal appeals better than human experts: A study with data from Brazilian federal courts |
| Authors | Elias Jacob de Menezes-Neto (Dept. of Law, Univ. Federal do Rio Grande do Norte, Caicó); Marco Bruno Miranda Clementino (Dept. of Private Law, UFRN, Natal; 6th Federal Court, TRF 5a Região, Natal) |
| Journal | PLOS ONE, vol. 17, issue 7, article e0272287 |
| Published | 2022-07-28 |
| DOI | 10.1371/journal.pone.0272287 |
| Landing (open access) | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0272287 |
| License | PLOS ONE → CC BY (open access; specific license text not re-verified on landing) |
| Dataset released | **BrCAD-5** — "Brazilian Courts Appeals Dataset for the 5th Regional Federal Court". Kaggle: https://www.kaggle.com/eliasjacob/brcad5 · DOI 10.34740/kaggle/dsv/3310186. Contains case number, basic metadata, full text of first-instance + appellate-panel decisions, and target label. Pretrained models hosted alongside. |
| Code | GitHub: https://github.com/eliasjacob/paper_brcad5 |

## Section map (as published)

1. Introduction — legal judgment prediction (LJP) context
2. Institutional Background — Brazilian judiciary structure & Federal Small Claims Courts (Juizados Especiais Federais)
3. Litigiousness and the Judiciary — drivers of case volume
4. The Federal Judiciary — TRF5 specifics
5. NLP with Deep Learning — LSTM, Transformers, BERT, Big Bird foundations
6. Methodology — Our Dataset · Data Preparation · Metrics Strategy (MCC) · Experimental Setup (3 architectures) · Legal Experts' Analysis
7. Results — MCC tables and temporal-stability plots
8. Limitations — first-instance text only; ignores appellate arguments/rebuttals
9. Discussion — comparison to prior LJP work; human-baseline novelty
10. Conclusion — summary + BrCAD-5 release
11. Supporting Information, Acknowledgments, References

## Key quantitative anchors (verbatim / near-verbatim from source)

- Initial corpus: **3,128,292** lawsuits → cleaned working dataset **765,602** appeals (BrCAD-5 size).
- Model split: **Training 612,961** · Validation **76,342** · Test **76,299**.
- Class balance: "appellate panels affirm lower court decisions in **79%** of cases" (Reverse ~21% / Affirm ~79%) — binary task.
- Time window: appeals tried Jan 23, 2006 – Apr 1, 2020; collection window June 2004 – Feb 2020.
- Split method: **time-sequential** (first 80% by appellate-ruling date = train; final 20% split 50/50 into val/test). No K-fold.
- Experts: **22** (5 federal judges + 17 judicial clerks), avg 11 yrs experience (8 yrs on FSCCs), labeled **690** randomly sampled cases, one expert per case, 5–56 labels/participant (μ=31.36, σ=14.67).
- Experts saw **only the first-instance decision full text** — same input as the models.
- Results (Matthews Correlation Coefficient, test set): **ULMFiT 0.3688** · **BERT+LSTM 0.3456** · **Big Bird 0.3271**.
- Human-expert MCC: best individual **0.1253**; group highest estimate (0.99 CI upper) **0.226**.
- CI method: **Fisher r-to-z transformation**, 0.99 confidence interval. All models beat the highest expert estimate (0.226) under that CI.
- No accuracy / F1 / precision / recall reported as primary metrics (MCC only). No traditional baselines (BoW/SVM/logistic) reported.
