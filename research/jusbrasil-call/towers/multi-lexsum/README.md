# Research Tower — Multi-LexSum

A local, source-backed learning tower for ONE paper:

> **Multi-LexSum: Real-World Summaries of Civil Rights Lawsuits at Multiple Granularities**
> Shen, Lo, Yu, Dahlberg, Schlanger, Downey — NeurIPS 2022 Datasets & Benchmarks Track
> arXiv: [2206.10883](https://arxiv.org/abs/2206.10883) · Site: https://multilexsum.github.io/

## Why this paper (Jusbrasil / Jus IA)

Multi-LexSum is the closest public benchmark to Jus IA's **"principais teses" / main-theses**
feature: it compresses many long source documents into expert summaries at **controlled
granularity** (one sentence → multi-paragraph), over **multi-document case files often >200
pages**. It doubles as a long-document summarization reference.

## How to read this tower

Read in this order; each file is short and links forward.

| Order | File | What it gives you |
|------|------|-------------------|
| 1 | `LEARNING-PACK.md` | The payload: source-backed claims, operator model, 5 things for the call, honest cutoff. Start here if short on time. |
| 2 | `TOWER.md` | Map of the tower + reading paths. |
| 3 | `L0-corpus.md` | Source record + section map (date checked 2026-06-10). |
| 4 | `claim-ledger.md` | Every claim with a source-kind label. |
| 5 | `glossary.md` | Plain-language terms. |
| 6 | `definitions.md` | Governed canonical definitions. |
| 7 | `distill.md` | One-sentence model, compositional spine, borrow/analogy/block for main-theses. |
| 8 | `bridge-decisions.md` | Adopt / adapt / reject decisions for Jus IA. |
| 9 | `open-residue.md` | What is NOT yet grounded (do not trust beyond this). |

## Provenance discipline

- **Source claims** (from the paper/site) are labeled and separated from **Arcanum readings**
  (our interpretation for Jus IA).
- **No invented numbers.** Anything not fetched is in `open-residue.md`, not asserted.
- **LOCAL-ONLY.** Nothing here promotes into the `arcanum` submodule.

Date checked: **2026-06-10**.
