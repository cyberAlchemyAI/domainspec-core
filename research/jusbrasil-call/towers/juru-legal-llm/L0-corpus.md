# L0-corpus.md — Source Record + Section Map

**Date checked:** 2026-06-10

## Source record

| Field | Value |
|---|---|
| Title | Juru: Legal Brazilian Large Language Model from Reputable Sources |
| Authors | Roseval Malaquias Junior, Ramon Pires, Roseli Romero, Rodrigo Nogueira |
| Year | 2024 (submitted 2024-03-26; v2 revised 2025-07-28) |
| arXiv ID | 2403.18140 |
| Landing | https://arxiv.org/abs/2403.18140 |
| PDF | https://arxiv.org/pdf/2403.18140 |
| HTML | https://arxiv.org/html/2403.18140v2 |
| Model artifact | Hugging Face `roseval/Juru-7B` (referenced in paper; not independently verified) |
| Fetch method | WebFetch on abstract, PDF, and HTML; HTML body yielded tables |

## What was actually fetched

- **Abstract** — fetched verbatim (high confidence).
- **HTML body / results tables** — fetched via WebFetch summarization (Tables 5/6/7 figures
  and corpus composition). Cross-checked across two fetches with consistent numbers.
- **PDF** — downloaded but local rendering (pdftoppm) unavailable; not read page-by-page.

## Section map (reconstructed from fetched content)

> Section numbering is approximate — reconstructed from the HTML structure, not from a
> verbatim table of contents. Treat headings as a navigation aid, not an exact quote.

1. **Introduction / Motivation** — high compute cost of pretraining limits research; two
   mitigation strategies: domain specialization and pretraining with high-quality data.
2. **Related work** — domain-specialized LLMs; Brazilian/Portuguese LLM landscape;
   continued-pretraining literature.
3. **Corpus / Data** — "reputable Brazilian legal sources"; three named categories:
   - Academic papers (Brazilian higher-ed institutions + national journals)
   - LexML federal regulations/laws (lexml.gov.br)
   - Brazilian Supreme Federal Court (STF) decisions and rulings (32,535 documents cited)
   - Token composition (see claim-ledger): ~1.805B academic + ~60.4M regulations + ~133.3M
     decisions ≈ 1.9B unique tokens.
4. **Method / Training** — continued pretraining of Mistral-7B; ~4 epochs; ~7.96B total
   training tokens; compute ~3.35×10²⁰ FLOPs.
5. **Evaluation** — few-shot evaluation across legal and general-knowledge suites.
   - Legal: OAB-2023, OAB-2024, ENAM-2024 (Brazilian bar/judiciary exams).
   - General PT: ENEM/BLUEX/CPNU/BNDES/REVALIDA and other Brazilian exam suites.
   - General EN: MMLU (college + high-school splits).
6. **Results** — legal mean rises; PT and EN general means fall (catastrophic forgetting).
7. **Discussion / Limitations** — specialization vs forgetting trade-off.
8. **Conclusion.**

## Confidence note

Abstract-level claims are high confidence. Table-level numbers (Sections 5–6) are
WebFetch-summarized; the load-bearing direction (legal up, general down) is robust and
cross-checked. Exact per-benchmark decimals are captured in the ledger with a confidence flag,
and any non-reproducible specific is mirrored in `open-residue.md`.
