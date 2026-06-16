# Research Tower: Juru — Legal Brazilian LLM from Reputable Sources

**Lane:** `juru-legal-llm`
**Paper:** Juru: Legal Brazilian Large Language Model from Reputable Sources (Malaquias Junior, Pires, Romero, Nogueira — 2024)
**arXiv:** 2403.18140 — https://arxiv.org/abs/2403.18140
**Date checked:** 2026-06-10
**Depth:** standard
**Builder context:** Jusbrasil call prep — foundation-model layer / build-vs-buy decision.

## What this tower is

A local, source-backed learning tower for ONE paper. It lets a reader understand and
decompose Juru without reading it cover to cover, and maps its findings to the Jusbrasil
**foundation-model layer** decision: *continue-pretrain an in-house base model vs RAG over a
frontier model*.

## Read order

1. `LEARNING-PACK.md` — start here. Source-backed claims, operator model, build-vs-buy
   takeaways, 5 things for the call, honest cutoff.
2. `distill.md` — one-sentence model + compositional spine + borrow/analogy/block.
3. `TOWER.md` — map of the tower and how the files compose.
4. `L0-corpus.md` — the source record + section map (the paper itself).
5. `claim-ledger.md` — every captured claim with a source-kind label.
6. `glossary.md` / `definitions.md` — terms, then governed definitions.
7. `bridge-decisions.md` — how (and whether) to carry each idea to Jusbrasil.
8. `open-residue.md` — what we could NOT verify from fetched content.

## Source-kind discipline

Source claims (from the paper) are kept strictly separate from Arcanum/operator readings.
No number in this tower was invented: every quantitative claim is traceable to the fetched
arXiv abstract or HTML body, or it lives in `open-residue.md` as unverified.

## Files

| File | Purpose |
|---|---|
| README.md | This file — orientation + read order |
| TOWER.md | Tower map + composition |
| L0-corpus.md | Source record + section map (date checked 2026-06-10) |
| claim-ledger.md | Claims with source-kind labels |
| glossary.md | Quick term definitions |
| definitions.md | Governed definitions for load-bearing concepts |
| distill.md | One-sentence model + spine + borrow/analogy/block |
| bridge-decisions.md | Per-idea bridge verdicts for Jusbrasil |
| LEARNING-PACK.md | The deliverable read for the call |
| open-residue.md | Unverified / open items |
