# TOWER — jua-benchmark

A learning tower is a layered scaffold: each layer rests on a verified one below it. Lower = closer to source; higher = closer to use.

```
                ┌─────────────────────────────┐
   USE          │  LEARNING-PACK.md           │  5 things for the call, operator model,
                │  bridge-decisions.md        │  eval takeaways, Jusbrasil bridge
                └─────────────────────────────┘
                              ▲
                ┌─────────────────────────────┐
   DISTILL      │  distill.md                 │  one-sentence model, compositional
                │                             │  spine, borrow/analogy/block
                └─────────────────────────────┘
                              ▲
                ┌─────────────────────────────┐
   GOVERN       │  definitions.md             │  governed defs (5 terms)
                │  glossary.md                │  quick glossary
                └─────────────────────────────┘
                              ▲
                ┌─────────────────────────────┐
   ADJUDICATE   │  claim-ledger.md            │  every claim + source-kind label
                │  open-residue.md            │  unverified / needs full PDF
                └─────────────────────────────┘
                              ▲
                ┌─────────────────────────────┐
   SOURCE (L0)  │  L0-corpus.md               │  source record, section map,
                │                             │  accessibility note (2026-06-10)
                └─────────────────────────────┘
```

## Layer contract

| Layer | File(s) | Promise | Source-kind discipline |
|---|---|---|---|
| L0 Source | `L0-corpus.md` | Faithful record of what exists, where, and what was fetched | Primary only; accessibility gaps marked |
| Adjudicate | `claim-ledger.md`, `open-residue.md` | Each claim labeled by source kind; gaps named | Primary-source vs. inferred vs. Arcanum-reading vs. open-residue |
| Govern | `definitions.md`, `glossary.md` | Stable meaning for load-bearing terms | Terms defined from source + standard IR usage |
| Distill | `distill.md` | Smallest coherent model that recomposes | Reading layer, labeled as such |
| Use | `LEARNING-PACK.md`, `bridge-decisions.md` | Decision-ready takeaways for the Jusbrasil call | Bridge readings labeled NON-SOURCE |

## Source-kind labels used throughout

- **[PRIMARY]** — stated explicitly in the JUÁ paper (abstract / HTML v2 body).
- **[PRIMARY~]** — from the paper but via WebFetch table summarization; carries transcription risk; flagged for full-PDF re-check.
- **[INFERRED]** — reasonable deduction from primary text, not stated verbatim.
- **[ARCANUM]** / **[BRIDGE]** — Jusbrasil/Jus IA reading; NOT a paper claim.
- **[OPEN]** — unverified; recorded in `open-residue.md`.

## How to extend

Drop new evidence into `L0-corpus.md` first, label it in `claim-ledger.md`, then let it flow up. Never promote a number above the ledger without a source-kind label. LOCAL-ONLY — never touch the `arcanum` submodule.
