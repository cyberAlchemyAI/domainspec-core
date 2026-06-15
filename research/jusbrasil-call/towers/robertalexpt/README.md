# Research Tower: RoBERTaLexPT

Lane: `robertalexpt` (one paper, one tower).

**Paper:** RoBERTaLexPT: A Legal RoBERTa Model Pretrained with Deduplication for Portuguese
**Authors:** Garcia, Silva, Siqueira, Gomes, Albuquerque, Souza, Lima, de Carvalho
**Venue/Year:** PROPOR 2024 (16th Intl. Conf. on Computational Processing of Portuguese)
**Landing:** https://aclanthology.org/2024.propor-1.38/

## What this tower is

A local, source-backed learning tower for ONE paper. It lets a reader understand
and decompose the paper without reading it cover to cover, and maps it to the
Jusbrasil ("Jus IA") **encoder/foundation layer** and the "millions of redundant
judicial documents" challenge.

## How to read it (suggested order)

1. `LEARNING-PACK.md` — start here. Source-backed claims, operator model, dedup
   takeaways, 5 things for the call, honest cutoff.
2. `distill.md` — one-sentence model + compositional spine.
3. `TOWER.md` — the tower map (what each file holds, how they connect).
4. `L0-corpus.md` — the source record + section map (date checked 2026-06-10).
5. `claim-ledger.md` — every captured claim with a source-kind label.
6. `glossary.md` / `definitions.md` — terms and governed definitions.
7. `bridge-decisions.md` — Arcanum-reading vs source-claim boundary statuses.
8. `open-residue.md` — what was NOT fetched / remains open.

## Boundary rule

Source claims (paper / authors' released artifacts) are kept strictly separate
from Arcanum readings (our interpretation / Jusbrasil mapping). See
`bridge-decisions.md`. Promotion is LOCAL-ONLY; the arcanum submodule is never
touched by this tower.

## Date checked

All web sources fetched/checked 2026-06-10.
