# claim-ledger.md — Source-Labeled Claims

**Date checked:** 2026-06-10
**Label legend:** primary-source | related-source | local-inference | analogy | operator-reading | open-residue

> Discipline: paper claims (`primary-source`) are kept separate from Jusbrasil readings
> (`analogy` / `operator-reading`). No number here was invented.

## A. Core build facts

| # | Claim | Label | Confidence | Source |
|---|---|---|---|---|
| A1 | Juru is Mistral-7B specialized via **continued pretraining** on Brazilian legal data. | primary-source | high | Abstract |
| A2 | Corpus = **1.9 billion unique tokens** from reputable Brazilian legal sources. | primary-source | high | Abstract |
| A3 | Total tokens processed in training ≈ **7.96 billion** over **~4 epochs**. | primary-source | med | HTML body |
| A4 | Training compute ≈ **3.35×10²⁰ FLOPs**. | primary-source | med | HTML body |
| A5 | Evaluation is **few-shot** across legal and general-knowledge suites. | primary-source | high | Abstract |

## B. Corpus composition (token counts)

| # | Claim | Label | Confidence | Source |
|---|---|---|---|---|
| B1 | Academic papers (Brazilian higher-ed + national journals): **~1,805,059,922 tokens**. | primary-source | med | HTML body |
| B2 | Federal regulations / laws via **LexML**: **~60,402,071 tokens**. | primary-source | med | HTML body |
| B3 | STF decisions and rulings: **~133,295,895 tokens** (cited **32,535 documents**). | primary-source | med | HTML body |
| B4 | B1+B2+B3 ≈ 1.999B ≈ the stated 1.9B "unique tokens" — composition is internally consistent. | local-inference | high | Arithmetic on B1–B3 |
| B5 | Academic papers dominate (~90% of tokens); statute/case law are the minority by volume. | local-inference | high | Ratio from B1–B3 |

## C. Legal benchmark gains (the upside)

| # | Claim | Label | Confidence | Source |
|---|---|---|---|---|
| C1 | On Brazilian legal benchmarks, mean accuracy rises **Mistral-7B 44.5% -> Juru 49.2%** (~+4.7 pts). | primary-source | med | HTML Table (legal mean) |
| C2 | OAB-2023: **48.3% -> 54.5%**; OAB-2024: **49.6% -> 52.0%**; ENAM-2024: **31.2% -> 36.8%**. | primary-source | low-med | HTML Table 5 (per-benchmark decimals less certain) |
| C3 | Gains achieved with a **reduced amount of pretraining data** vs typical from-scratch budgets. | primary-source | high | Abstract |

## D. Catastrophic forgetting (the cost)

| # | Claim | Label | Confidence | Source |
|---|---|---|---|---|
| D1 | Specialization **degrades general-knowledge performance** in BOTH Portuguese and English. | primary-source | high | Abstract |
| D2 | English general (MMLU) mean falls **~61.6% -> ~58.0%** (~−3.6 pts). | primary-source | low-med | HTML Table 6 |
| D3 | Portuguese general mean falls **~50.5% -> ~48.1%** (~−2.4 pts). | primary-source | low-med | HTML Table 7 |
| D4 | Net pattern: **legal up ~+4.7, general down ~2–4 pts** — a real, measured trade-off, not free lunch. | local-inference | high | C1 + D2 + D3 |

## E. Framing claims

| # | Claim | Label | Confidence | Source |
|---|---|---|---|---|
| E1 | Two strategies motivate the work: **domain specialization** and **high-quality-data pretraining**. | primary-source | high | Abstract |
| E2 | "Reputable sources" curation is the data-quality lever (academic + official statute + apex-court text). | primary-source | high | Abstract + HTML body |
| E3 | High pretraining compute cost is the stated barrier the approach tries to lower. | primary-source | high | Abstract |

## F. Jusbrasil readings (kept separate from paper claims)

| # | Claim | Label | Source |
|---|---|---|---|
| F1 | Juru is the **keystone reference** for the in-house continue-pretrain option at the foundation-model layer. | operator-reading | Builder brief |
| F2 | The legal-up/general-down result is the **central build-vs-buy tension**: a specialized base model is narrower, not strictly better. | operator-reading | D4 + brief |
| F3 | A continue-pretrained legal base behaves like a **narrow-band amplifier**: louder in-band (law), quieter out-of-band (general). | analogy | distill.md |
| F4 | For Jus IA's mixed traffic, forgetting argues for **RAG-over-frontier or a router**, not a single specialized base, unless traffic is law-pure. | operator-reading | D1–D4 + brief |

## Open items rolled to residue

- Exact per-benchmark few-shot k (number of shots) — not captured. (open-residue)
- Exact decimal scores for every PT/EN sub-exam — only means captured. (open-residue)
- License / availability terms of `roseval/Juru-7B`. (open-residue)
- Whether any replay/rehearsal mitigation against forgetting was attempted. (open-residue)
