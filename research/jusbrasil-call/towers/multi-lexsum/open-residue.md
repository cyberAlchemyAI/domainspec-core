# open-residue.md — What is NOT yet grounded

Date checked: **2026-06-10**. These are honesty boundaries. Do not assert any of these as fact;
fetch and verify (parse the PDF body of arXiv 2206.10883, or the HuggingFace dataset card)
before using.

| # | Open item | Why open | How to close |
|---|-----------|----------|--------------|
| R1 | **Baseline model names** (e.g., BART, PRIMERA, Longformer, Pegasus-X?) | PDF body did not decode this build; abstract only says SOTA "perform poorly" | Parse PDF §experiments / read dataset card |
| R2 | **Number of distinct cases/lawsuits** | Only the 9,280 *summary* count is grounded; cases ≠ summaries (3 tiers) | PDF §dataset / HF card |
| R3 | **Train/dev/test split sizes** | Not in abstract or site excerpt | PDF / HF card |
| R4 | **ROUGE / metric scores** per model and per granularity tier | PDF body not parsed | PDF §results table |
| R5 | **Documents per case** (how many docs feed one summary) | Site gives doc *types* and page scale, not counts | PDF §dataset stats |
| R6 | **Verbatim section structure** of the paper | Section map in `L0-corpus.md` is inferred from abstract+site | Read rendered PDF TOC |
| R7 | **Exact granularity word counts** confirmation | ~25/~130/~650 are from the site; abstract says "over five hundred words" for long — confirm against PDF | Cross-check PDF |
| R8 | **Whether every case has all three tiers** | Site states one per level; coverage completeness across the corpus unconfirmed | PDF §dataset / HF card |

## Residue count: **8**

## Closing note
Closing R1–R5 mainly requires successfully parsing the arXiv PDF body (it returned undecoded
binary this build) or reading the HuggingFace dataset card. R6–R8 are confirmations against the
rendered paper. None of these change the bridge decisions' ADOPT/ADAPT/REJECT directions; they
gate the DEFER items (B8, B9) and any quoted numbers.
