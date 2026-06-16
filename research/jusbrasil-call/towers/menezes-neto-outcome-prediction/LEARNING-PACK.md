# LEARNING PACK — Menezes-Neto et al. (2022), for the Jusbrasil call

**Paper:** de Menezes-Neto & Clementino, PLOS ONE 17(7):e0272287 (2022-07-28), open access. DOI 10.1371/journal.pone.0272287.
**Use:** credibility anchor + methodological map for a next Jusbrasil product — **judicial outcome prediction ("Probabilidade de Êxito").**
**All numbers source-checked 2026-06-10. Source claims and our readings are kept separate.**

---

## 1. Source-backed claims (what the paper actually shows)

- **Data.** 765,602 TRF5 Federal Small Claims (Juizados Especiais Federais) appeals (released as **BrCAD-5** on Kaggle); 612,961 train / 76,342 val / 76,299 test. Binary target: appellate panel **affirms** (~79%) vs **reverses** (~21%) the first-instance decision. [D1–D4]
- **Input.** Models and humans saw **only the full text of the first-instance decision** — not appellate arguments or rebuttals. [D6, E3]
- **Models.** Three: **ULMFiT** (best), **BERT+LSTM**, **Big Bird**. No traditional baselines reported. [M1, M3]
- **Headline.** Test-set **MCC: ULMFiT 0.3688 · BERT+LSTM 0.3456 · Big Bird 0.3271**, vs best human expert **0.1253** (group upper-CI 0.226). All models beat the highest expert estimate under a 0.99 Fisher r-to-z CI. ≈**2.9x** the best individual expert ("almost three times," authors' words). [R2–R6]
- **Human baseline.** 22 experienced pros (5 judges + 17 clerks, ~11 yrs experience) labeled 690 same-input cases. This same-inputs head-to-head is the paper's key credibility move. [E2, E3]
- **Evaluation rigor.** **Time-sequential split** (train on past, test on future) to avoid temporal leakage; **MCC** chosen for class imbalance; no drift observed across the test window. [E1, E4]
- **Authors' own caveats.** Labels were hard to obtain (≥2-of-3 weak-signal voting); scope is TRF5 only with no cross-region validation; results are a "promising approach"; models "cannot replace human decision-making"; study was IRB-exempt with **no OAB/bar engagement**. [C1–C6]

> Not in the paper (don't claim it): no accuracy/F1/precision/recall, no calibration analysis, no traditional ML baseline, no multi-region or multi-instance validation, no lawyer-side "win" target. [R7]

## 2. Operator model (how to think about it in one breath)

A high-volume, imbalanced legal corpus + a derived affirm/reverse label + a leakage-safe split + three text models, benchmarked against humans on identical inputs, yields a **real but modest predictive edge that beats experts ~3x relative while staying low in absolute terms.** The three load-bearing joints are the **derived label**, the **time-sequential split**, and the **same-inputs human baseline** — copy those ideas, not the 2022 model stack.

## 3. Next-product takeaways ("Probabilidade de Êxito")

1. **The opportunity is validated, not solved.** Outcome signal exists in decision text and beats experts — enough to justify the product, not to over-promise it. [B1]
2. **Reuse the methodology, modernize the models.** Same-inputs human benchmark + time-sequential eval + MCC/calibration are the durable parts; swap ULMFiT/BERT/BigBird for modern long-context LLMs. [B2, B3, B4]
3. **Redefine the target.** "Êxito" is lawyer-side and multi-outcome; affirm/reverse on first-instance text is a narrow proxy. Needs a per-jurisdiction labeling spec. [B5]
4. **BrCAD-5 is a free cold-start.** Stand up a reproducible TRF5 baseline fast, then expand. [B10]

## 4. Risks (carry these into the room)

- **R-Label:** Labels were reverse-engineered from filenames/regex/metadata — production needs an auditable labeling pipeline or the whole signal is suspect. [B6]
- **R-Absolute:** MCC ≈ 0.37 is a modest ceiling. Ship **probabilities with uncertainty**, never guarantees. [B7]
- **R-Ethics/OAB:** "Promising/assistive" framing + zero OAB engagement = a real professional-ethics exposure for a product that tells lawyers/litigants their odds. This is a CONSTRAINT, not a footnote. [B8]
- **R-Scope:** TRF5-only, first-instance-text-only. National/multi-instance coverage is a harder, more drift-prone problem the paper did not solve. [B9]
- **R-Marketing:** Do NOT claim "predicts your case outcome" as settled. [B11]

## 5. Five things to say on the call

1. "There is **published, open, dataset-backed** Brazilian evidence (765k TRF5 appeals) that models beat experienced judges/clerks at predicting appeal outcomes from the **same text** — best model MCC 0.37 vs expert 0.13, ~3x." 
2. "The win is **relative, not absolute** — MCC 0.37 is a real edge but a low ceiling, so the product must be a **probability with uncertainty**, not a verdict."
3. "Their hardest problem was **labels** (reverse-engineered from filenames/regex). Jusbrasil's defensible **labeling pipeline** is the moat and the risk."
4. "The reusable methodology is a **same-inputs human benchmark + time-sequential evaluation + MCC/calibration** — we should adopt all three and modernize the model stack."
5. "**Professional-ethics / OAB framing is a first-class constraint** the paper skipped — an outcome-probability product is assistive decision support, and we should lead with that."

## 6. Honest cutoff (limits of this tower)

- Built from the **PLOS ONE landing page only** (two WebFetch passes, 2026-06-10). Figures/tables, supplementary files, and the BrCAD-5 dataset/GitHub were **not** independently inspected; numbers rely on the article body as fetched.
- No **calibration**, **per-class**, or **subgroup/fairness** numbers exist to report — the paper gives MCC only.
- "~3x" resolves to ~2.9x vs **best-individual** expert; vs the group's upper-CI estimate (0.226) it is ~1.6x. Use the framing precisely.
- Mapping to "Probabilidade de Êxito" is **our reading**, not the paper's claim. The paper predicts affirm/reverse, not lawyer-side win.
- No independent replication or post-2022 follow-up literature was searched for this tower (out of scope at standard depth).
