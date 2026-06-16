# TOWER.md — Build map

**Lane:** `menezes-neto-outcome-prediction` · **Built:** 2026-06-10 · **Depth:** standard

## What a "tower" is here

A local, source-backed learning structure for ONE paper. Each floor lets a reader understand and decompose the paper without reading it cover to cover. Source claims (what the paper says) are kept strictly separate from Arcanum readings (our interpretation for the Jusbrasil call).

## Floors

```
L0  corpus + section map ........... L0-corpus.md      (what the source IS; date-checked)
L1  glossary + definitions ......... glossary.md, definitions.md  (vocabulary)
L2  claim ledger ................... claim-ledger.md   (every claim, source-kind labeled)
L3  distill ....................... distill.md        (one-sentence model + spine + borrow/block)
L4  bridge decisions .............. bridge-decisions.md (what transfers to the product, statuses)
L5  learning pack ................. LEARNING-PACK.md  (the synthesized payload for the call)
R   residue ....................... open-residue.md   (unresolved / out of scope)
```

## Build logic

1. **Fetch first, claim second.** All numbers come from two WebFetch passes of the open-access PLOS ONE article (2026-06-10). No invented figures. Where the paper does not report a metric (e.g. accuracy/F1), the ledger says so explicitly.
2. **Source vs reading separation.** Ledger entries are tagged `PRIMARY` (the paper) or `ARCANUM-READING` (our inference). Bridge decisions are all readings; they cite the primary claims they rest on.
3. **Headline anchor.** Best model ULMFiT MCC 0.3688 vs human-expert best individual MCC 0.1253 (paper abstract). "~3x" in the brief resolves to ~2.9x on best-individual, and "almost three times" in the authors' own words.
4. **Caution as a first-class artifact.** The OAB-ethics / "promising results" framing is recorded as a real constraint in `bridge-decisions.md`, not buried.
5. **LOCAL-ONLY.** Everything lives under `research/jusbrasil-call/towers/…`. The `arcanum` submodule is never touched.

## Provenance of numbers

Two prompts against `https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0272287`:
- Pass 1: dataset, models, results, expert comparison, eval setup, caveats, ethics, section map.
- Pass 2: authors, pub metadata, BrCAD-5 dataset, code availability, abstract verbatim, CI method, expert-information conditions.
