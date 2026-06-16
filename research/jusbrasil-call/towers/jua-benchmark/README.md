# Research Tower — JUÁ Benchmark

**Lane:** `jua-benchmark`
**Paper:** JUÁ — A Benchmark for Information Retrieval in Brazilian Legal Text Collections (Pereira et al., arXiv:2604.06098, April 2026)
**Built:** 2026-06-10
**Status:** Complete (landing + HTML v2 fetched; full PDF skimmed via WebFetch — see open-residue for what needs full-text verification)

## What this tower is

A local, source-backed learning tower for ONE paper. It lets a reader understand and decompose JUÁ without reading it cover to cover. Source claims are kept strictly separate from Arcanum/Jusbrasil readings.

## Why it matters for Jusbrasil ("Jus IA")

JUÁ is the freshest Brazilian legal IR benchmark (April 2026): a unified, leaderboard-backed evaluation spanning jurisprudence, legislative/regulatory, and question-driven legal search, with BM25, dense, and domain-adapted Qwen baselines. Its core finding — **retrieval quality varies sharply across legal collection types, with no single dominant paradigm** — is the public yardstick for evaluating Jus IA's **similar-jurisprudence retrieval** feature and the **tribunal-heterogeneity challenge**.

## Read order

1. `LEARNING-PACK.md` — start here: source-backed claims, operator model, eval takeaways, 5 things for the call, honest cutoff.
2. `TOWER.md` — map of the tower and how the files relate.
3. `distill.md` — one-sentence model + compositional spine + borrow/analogy/block.
4. `L0-corpus.md` — source record, section map, accessibility note.
5. `claim-ledger.md` — every claim with source-kind label.
6. `glossary.md` / `definitions.md` — terms.
7. `bridge-decisions.md` — Arcanum/Jusbrasil bridge statuses.
8. `open-residue.md` — what is unverified / needs the full PDF.

## Files

- `README.md` (this file)
- `TOWER.md`
- `L0-corpus.md`
- `claim-ledger.md`
- `glossary.md`
- `definitions.md`
- `distill.md`
- `bridge-decisions.md`
- `LEARNING-PACK.md`
- `open-residue.md`

## Provenance rule

Numbers are quoted from the arXiv HTML v2 render (`https://arxiv.org/html/2604.06098v2`) and the abstract. Nothing is invented. WebFetch summarization of tables introduces a non-zero transcription risk; numbers carrying decision weight are flagged for full-PDF re-verification in `open-residue.md`.
