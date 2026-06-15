# open-residue.md — Unverified / Paywalled Items

Date checked: 2026-06-10. Source blocked by Springer paywall (303 → SSO). Items below are **not fabricated** and would resolve with full-text access (PDF, institutional login, or the open UFRGS thesis once a PDF renderer is available).

| # | Open item | Why open | How to resolve |
|---|---|---|---|
| OR1 | Base summarization model / transformer (e.g. PtT5, BERTSum, mBART, Pegasus…?) | Behind paywall; not in abstract | Read paper §method or thesis §architecture |
| OR2 | Entailment/NLI model + training corpus + language (PT-native vs translated NLI) | Not in abstract | Paper §method |
| OR3 | Exact ROUGE-1/2/L numbers, baseline vs LegalSumm | Results table is paywalled | Paper §experiments — **do not estimate** |
| OR4 | Number of views, view-construction algorithm, candidate count per document | Not in abstract | Paper §method |
| OR5 | RulingBR exact train/test/val counts, document & summary token lengths | Not stated in open docs | RulingBR paper §dataset / repo data files |
| OR6 | Whether human/qualitative faithfulness eval was run (beyond ROUGE) | Not in abstract | Paper §evaluation |
| OR7 | Ablation: entailment-selection vs simple length/score selection | Not in abstract | Paper §experiments |
| OR8 | Inference cost of generating N candidates + scoring | Not discussed in open material | Paper §method/discussion |
| OR9 | Whether the entailment gate reduced *measured* hallucination, not just ROUGE | Core to Jus IA value, unverified | Paper §evaluation |
| OR10 | License / reuse terms of RulingBR for commercial use | No explicit license surfaced on repo | github.com/diego-feijo/rulingbr (check LICENSE) / contact authors |

**Resolution note:** The open thesis PDF (lume.ufrgs.br handle 10183/230669, 001132167.pdf) was downloaded but could not be text-extracted here (no PDF renderer in environment). It is the highest-value next source for OR1–OR7.

**Open-residue count: 10.**
