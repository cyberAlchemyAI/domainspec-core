# Research Tower — Menezes-Neto et al. (2022), Outcome Prediction

**Lane:** `menezes-neto-outcome-prediction`
**Paper:** de Menezes-Neto & Clementino (2022). *Using deep learning to predict outcomes of legal appeals better than human experts: A study with data from Brazilian federal courts.* PLOS ONE 17(7): e0272287. DOI: 10.1371/journal.pone.0272287 (open access).
**Built:** 2026-06-10 · **Depth:** standard · **Promotion:** LOCAL-ONLY (does not touch the arcanum submodule)

## Why this tower exists (Jusbrasil framing)

This is the **credibility anchor for a next Jusbrasil product: judicial outcome prediction ("Probabilidade de Êxito"),** the natural sibling to "Jus IA." The paper is the strongest published evidence that a model can predict Brazilian legal-appeal outcomes *and beat experienced human experts on the same task with the same inputs*. It also surfaces the methodological cautions (label provenance, time-sensitive splits, single-region scope, "promising results" framing) that a product team must respect before shipping a probability number to lawyers and litigants.

## How to read this tower

| Read order | File | What you get |
|---|---|---|
| 1 | `LEARNING-PACK.md` | The payload: source-backed claims, operator model, next-product takeaways + risks, 5 things for the call, honest cutoff. **Read this first if you only read one file.** |
| 2 | `TOWER.md` | Map of the tower and the build logic. |
| 3 | `distill.md` | One-sentence model, compositional spine, borrow/analogy/block. |
| 4 | `claim-ledger.md` | Every captured claim with source-kind labels (primary vs Arcanum reading). |
| 5 | `L0-corpus.md` | Source record + paper section map (date checked 2026-06-10). |
| 6 | `glossary.md` / `definitions.md` | Terms (LJP, JEF, ULMFiT/BERT/BigBird, calibration, label leakage) and governed defs. |
| 7 | `bridge-decisions.md` | Bridge statuses incl. the OAB-ethics / "promising results" caution as a real constraint. |
| 8 | `open-residue.md` | What this tower does NOT settle. |

## One-line takeaway

On 612,961 TRF5 small-claims appeals, ULMFiT/BERT/BigBird all beat 22 human experts at predicting affirm-vs-reverse (best model MCC **0.3688** vs experts **0.1253**, ~2.9x), using **only the first-instance decision text** — a real but *modest-absolute* signal that validates the outcome-prediction opportunity while warning that the absolute ceiling is low and the framing is "promising," not "deployable as a guarantee."
