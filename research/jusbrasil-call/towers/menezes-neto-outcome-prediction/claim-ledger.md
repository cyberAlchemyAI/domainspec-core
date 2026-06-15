# Claim Ledger

Source-kind labels:
- **PRIMARY** = stated in the paper (PLOS ONE e0272287, checked 2026-06-10).
- **PRIMARY-DERIVED** = arithmetic on primary numbers (calculation shown).
- **ARCANUM-READING** = our interpretation for the Jusbrasil call; NOT a paper claim.

## Dataset

| # | Claim | Kind |
|---|---|---|
| D1 | Initial corpus of 3,128,292 lawsuits cleaned to a 765,602-appeal working dataset (released as BrCAD-5). | PRIMARY |
| D2 | Model splits: 612,961 train / 76,342 validation / 76,299 test. | PRIMARY |
| D3 | Source: Federal Small Claims Courts (Juizados Especiais Federais) within TRF5 (5th Regional Federal Court, 6 states/NE Brazil). | PRIMARY |
| D4 | Binary target: appellate panel **Affirms** vs **Reverses** the first-instance decision; ~79% affirm / ~21% reverse (imbalanced). | PRIMARY |
| D5 | Labels assembled from 3 sources (case metadata, AP-ruling filename, hand-crafted regex) via a voting rule: ≥2 of 3 must agree. Authors note "gathering correct labels was not easy." | PRIMARY |
| D6 | Model input = full text of the **first-instance** court decision only (appellate arguments/rebuttals are NOT seen by the model). | PRIMARY |

## Models

| # | Claim | Kind |
|---|---|---|
| M1 | Three architectures trained: **ULMFiT** (AWD-LSTM language model + classifier), **BERT (Portuguese) + LSTM**, **Big Bird** (long-context transformer, pretrained from scratch on Portuguese Wikipedia + BrWaC). | PRIMARY |
| M2 | Big Bird handles up to **7,680 tokens**; BERT path chunks text into 512-token pieces fed through a unidirectional LSTM (output 1,536) then linear heads. | PRIMARY |
| M3 | No traditional baselines (bag-of-words, SVM, logistic regression) were reported. | PRIMARY |

## Headline results

| # | Claim | Kind |
|---|---|---|
| R1 | Primary metric is **Matthews Correlation Coefficient (MCC)**, chosen because the dataset is imbalanced. | PRIMARY |
| R2 | Test-set MCC: ULMFiT **0.3688** (best) · BERT+LSTM **0.3456** · Big Bird **0.3271**. | PRIMARY |
| R3 | Best individual human expert MCC **0.1253**; group highest estimate (0.99 CI upper bound) **0.226**. | PRIMARY |
| R4 | All three models beat the highest human-expert estimate (0.226) under the 0.99 CI (Fisher r-to-z). | PRIMARY |
| R5 | Authors: models "outperform by almost three times the predictions determined by human experts." | PRIMARY |
| R6 | 0.3688 / 0.1253 ≈ **2.94x** vs best-individual expert; vs the 0.226 group-upper-bound it is ≈1.6x. The "~3x" claim is true against best-individual MCC. | PRIMARY-DERIVED |
| R7 | **No accuracy / F1 / precision / recall reported** as headline metrics. Absolute MCC is modest (≈0.37 on a -1..+1 scale); the win is *relative to humans*, not a high absolute ceiling. | PRIMARY (absence) + ARCANUM-READING (interpretation) |

## Evaluation & experts

| # | Claim | Kind |
|---|---|---|
| E1 | **Time-sequential split**: first 80% by appellate-ruling date = train; final 20% split 50/50 into val/test. Explicitly chosen so "no information from the future would leak into the model." No K-fold/random holdout. | PRIMARY |
| E2 | 22 experts (5 federal judges + 17 clerks), avg 11 yrs federal-court experience (8 on FSCCs), labeled 690 randomly sampled cases, one expert per case. | PRIMARY |
| E3 | Experts saw **only the first-instance decision full text** — identical information to the models (fair head-to-head). | PRIMARY |
| E4 | Authors found "no drift or decrease" in model capacity across the test timeframe. | PRIMARY |

## Caveats raised by the authors

| # | Claim | Kind |
|---|---|---|
| C1 | Time-sensitive split is necessary because "neither random splits nor K-fold cross-validation consider the time-sensitive nature of legal decisions" — a data-leakage concern. | PRIMARY |
| C2 | Label quality was hard; the ≥2-of-3 voting scheme is a mitigation, not a guarantee of clean labels. | PRIMARY |
| C3 | Scope is TRF5 only (6 states); authors are "confident the same logic would apply to all federal courts" but provide **no cross-region validation**. | PRIMARY |
| C4 | Model ignores arguments raised in appeals/rebuttals (input is first-instance text only) — a stated limitation on what is being predicted. | PRIMARY |
| C5 | Framing throughout: a "promising approach"; models "cannot replace human decision-making" but "can assist courts." Assistive, not authoritative. | PRIMARY |
| C6 | Study was IRB/REB-exempt (Brazilian Resolution 510/2016 humanities exception); no PII collected. No OAB / bar-association engagement reported. | PRIMARY |

## Arcanum readings (NOT paper claims — for the Jusbrasil call)

| # | Reading | Rests on |
|---|---|---|
| A1 | This paper is the strongest published proof-of-concept that Brazilian appeal outcomes are predictable from decision text and that models beat experts on equal footing — a credibility anchor for "Probabilidade de Êxito." | R2–R5, E3 |
| A2 | The **modest absolute MCC (~0.37)** means a product must present *probabilities/uncertainty*, never a binary "you will win." Over-claiming would outrun the science. | R7, C5 |
| A3 | **Label leakage is the central reproducibility risk** for any productionization: the target was reverse-engineered from filenames/regex/metadata, not a clean adjudicated field. Jusbrasil must own a defensible labeling pipeline. | D5, C2 |
| A4 | The expert baseline is the paper's most reusable methodological asset — Jusbrasil should replicate a *human-on-same-inputs* benchmark to defend any product claim. | E2, E3 |
| A5 | The "promising results" + assistive framing + no-OAB-engagement is a **deployment constraint**, not a footnote: an outcome-probability product faces professional-ethics scrutiny (lawyer duty, access-to-justice, automation of legal judgment). | C5, C6 |
| A6 | Single-region scope + first-instance-text-only input mean Jusbrasil's national, multi-court, multi-source corpus is both an opportunity (broader) and a harder problem (more drift, more label heterogeneity) than this paper solved. | C3, C4, D6 |
