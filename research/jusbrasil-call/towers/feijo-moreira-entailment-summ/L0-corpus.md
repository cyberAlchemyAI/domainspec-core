# L0-corpus.md — Source Record

**Date checked:** 2026-06-10

## Primary source
- **Title:** Improving abstractive summarization of legal rulings through textual entailment
- **Authors:** Diego de Vargas Feijó; Viviane P. Moreira (UFRGS — Universidade Federal do Rio Grande do Sul, Porto Alegre, Brazil)
- **Venue:** *Artificial Intelligence and Law*, Volume 31, Issue 1, pages 91–113
- **Year:** 2023 (online 2021)
- **DOI:** 10.1007/s10506-021-09305-4
- **Landing:** https://link.springer.com/article/10.1007/s10506-021-09305-4

### Accessibility
- **Status: PAYLINKED / CLOSED ACCESS.** The Springer landing returns a 303 redirect to an SSO authorize endpoint (`idp.springer.com/authorize`). Full text not retrievable via WebFetch.
- dblp confirms "Closed access" with an Unpaywall hint.
- A related open UFRGS thesis ("Summarizing Legal Rulings", lume.ufrgs.br handle 10183/230669, file 001132167.pdf) likely contains overlapping content but **could not be text-extracted in this environment** (no PDF renderer available). Listed as residue.

### Section map (as known / inferred — paper internals not directly read)
The paper internals are not verified; standard AI&Law structure inferred (local-inference, not a source claim):
- Abstract — RECOVERED (verbatim in claim-ledger).
- Introduction / problem (hallucination in legal summaries) — gist recovered.
- Related work — not read.
- LegalSumm method (views + summarization model + entailment module) — gist recovered.
- Dataset (RulingBR) — provenance recovered via related source.
- Experiments / ROUGE results — **NOT recovered (open-residue)**.
- Conclusion — not read.

## Related source — the dataset
- **Title:** RulingBR: A Summarization Dataset for Legal Texts
- **Authors:** Diego de Vargas Feijó; Viviane P. Moreira
- **Venue:** PROPOR 2018 (13th Intl. Conf. on Computational Processing of the Portuguese Language), Canela, Brazil, Sept 24–26, 2018. Springer LNCS, ch. 10.1007/978-3-319-99722-3_26.
- **Repo:** https://github.com/diego-feijo/rulingbr (open)
- **Contents:** ~10K rulings from the Brazilian Federal Supreme Court (Supremo Tribunal Federal, STF), downloaded/parsed from stf.jus.br, covering 2011–2018.
- **Document sections per ruling:** `ementa` (summary / gold), `relatório` (case report), `voto` (judge vote), `acórdão` (final compiled decision); plus metadata: `area`, `classe`, `relator`, `extrato`.
- **Versions:** v1.1 added manual summary corrections; v1.2 (current) deduplicated (removed 49 near-identical samples), added categorical metadata; includes train/test/validation splits (exact counts not stated in open docs — residue).

## Open indexes consulted
- dblp: https://dblp.org/rec/journals/ail/FeijoM23.html (bib record, closed-access flag)
- ACM DL mirror: https://dl.acm.org/doi/abs/10.1007/s10506-021-09305-4
- ResearchGate listing: publication/356588750
- Semantic Scholar (RulingBR): 93a11cd8b0e3ee837897e24a952434bc4a4ff34a
- Survey context: arXiv 2501.17830 ("A Comprehensive Survey on Legal Summarization")
- UFRGS thesis: https://lume.ufrgs.br/bitstream/handle/10183/230669/001132167.pdf (open, unparsed here)
