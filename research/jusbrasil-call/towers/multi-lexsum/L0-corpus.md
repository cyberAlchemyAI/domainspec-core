# L0-corpus.md — Source record + section map

Date checked: **2026-06-10**

## Primary source

- **Title:** Multi-LexSum: Real-World Summaries of Civil Rights Lawsuits at Multiple Granularities
- **Authors:** Zejiang Shen, Kyle Lo, Lauren Yu, Nathan Dahlberg, Margo Schlanger, Doug Downey
- **Venue/Year:** NeurIPS 2022, Datasets & Benchmarks Track (paper notes: submitted Jun 22, 2022)
- **arXiv:** 2206.10883 (cs.CL) — landing: https://arxiv.org/abs/2206.10883
- **Official site:** https://multilexsum.github.io/
- **Data host:** HuggingFace Datasets [S-site]
- **Underlying corpus:** Civil Rights Litigation Clearinghouse (CRLC), clearinghouse.net [S]

## Sources actually fetched (this build)

| URL | Status | What it grounded |
|-----|--------|------------------|
| arxiv.org/abs/2206.10883 | OK | Title, authors, abstract, dataset size, doc scale, license |
| multilexsum.github.io | OK | Granularity definitions + word counts, doc types, license breakdown |
| arxiv.org/pdf/2206.10883 | FAILED (binary not decoded) | — (baselines/splits unfetched -> residue) |
| semanticscholar.org/arxiv/2206.10883 | 404 | — |

## Section map (inferred from abstract + site; PDF body not parsed)

A standard Datasets & Benchmarks paper. Expected structure (treat headings as [A] until
PDF verified):

1. Introduction — CRLC summarization is expensive expert labor; motivates the dataset. [S]
2. Dataset construction — sourcing from CRLC, expert authoring + review, guidelines. [S-site]
3. Granularity design — three tiers (tiny / short / long). [S-site]
4. Task setup — multi-document, long inputs (>200 pages/case). [S]
5. Baselines / experiments — SOTA summarizers "perform poorly". [S] (model names = [O])
6. Analysis / limitations / ethics / license. [S]

## Section map status

Headings are **inferred**, not verified against the PDF. Confirm against the rendered PDF
before citing specific section numbers. See `open-residue.md`.
