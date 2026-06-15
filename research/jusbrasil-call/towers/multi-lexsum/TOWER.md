# TOWER.md — Multi-LexSum learning tower

Lane: **multi-lexsum** · One paper · Depth: standard · Date checked: 2026-06-10

## Tower layers

```
L0  Corpus / source record        -> L0-corpus.md
L1  Claims (source-kind labeled)   -> claim-ledger.md
L2  Language (glossary + defs)     -> glossary.md, definitions.md
L3  Distillation (model + spine)   -> distill.md
L4  Bridge to Jus IA (decisions)   -> bridge-decisions.md
L5  Learning pack (the payload)    -> LEARNING-PACK.md
L6  Residue (honesty boundary)     -> open-residue.md
```

## Reading paths

- **Call prep (fast):** `LEARNING-PACK.md` -> "5 things for the call".
- **Build / decompose intent:** `distill.md` -> `bridge-decisions.md`.
- **Audit trust:** `claim-ledger.md` -> `open-residue.md` -> `L0-corpus.md`.

## Source-kind legend (used throughout)

- **[S]** Source claim — stated by the paper or official site.
- **[S-site]** From the official project site (multilexsum.github.io), not the PDF body.
- **[A]** Arcanum reading — our interpretation/bridge for Jus IA. Not the paper's claim.
- **[O]** Open / not yet grounded — see `open-residue.md`.

## Status

- Grounded: abstract, granularity definitions, dataset size, source-doc scale, license.
- Not grounded yet: baseline model names + ROUGE numbers, case count, split sizes,
  per-case document counts. -> `open-residue.md`.
