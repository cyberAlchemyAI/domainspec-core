# TOWER — lesswrong-rationality

A learning tower is a layered scaffold: each layer rests on a verified one below it.
Lower = closer to source; higher = closer to use. The Arcanum bridge layer is always
labeled NON-SOURCE and never rewrites a layer beneath it.

```
                ┌─────────────────────────────┐
   USE          │  LEARNING-PACK.md           │  operator model, borrow/block,
                │  bridge-decisions.md        │  "what to take into Arcanum", cutoff
                └─────────────────────────────┘   ← BRIDGE layer (NON-SOURCE, labeled)
                              ▲
                ┌─────────────────────────────┐
   DISTILL      │  distill.md                 │  one-sentence model, compositional
                │                             │  spine, borrow/analogy/block table
                └─────────────────────────────┘
                              ▲
                ┌─────────────────────────────┐
   GOVERN       │  definitions.md             │  governed defs for load-bearing terms
                │  glossary.md                │  quick glossary (source kind per entry)
                └─────────────────────────────┘
                              ▲
                ┌─────────────────────────────┐
   ADJUDICATE   │  claim-ledger.md            │  every claim + source-kind label
                │  residue/open-residue.md    │  unverified / needs full essays
                │  levels/L1-residue-map.md   │  residue map
                └─────────────────────────────┘
                              ▲
                ┌─────────────────────────────┐
   SOURCE (L0)  │  levels/L0-corpus.md        │  source record, 6-book map,
                │                             │  accessibility note (2026-06-16)
                └─────────────────────────────┘
```

## Layer contract

| Layer | File(s) | Promise | Source-kind discipline |
|---|---|---|---|
| L0 Source | `levels/L0-corpus.md` | Faithful record of what exists, where, what was fetched | `primary-source` only; gaps marked |
| Adjudicate | `claim-ledger.md`, `residue/open-residue.md`, `levels/L1-residue-map.md` | Each claim labeled by source kind; gaps named | full source-kind taxonomy below |
| Govern | `definitions.md`, `glossary.md` | Stable meaning for load-bearing terms | source kind per entry; promotion status |
| Distill | `distill.md` | Smallest coherent model that recomposes | reading layer, labeled as such |
| Use (BRIDGE) | `LEARNING-PACK.md`, `bridge-decisions.md` | Decision-ready takeaways for Arcanum operators | bridge readings labeled NON-SOURCE |

## Source-kind taxonomy (used throughout — from the research-tower sigil)

- **`primary-source`** — stated by the main source (a Sequences essay / book).
- **`related-source`** — stated by a related paper or external source (e.g. Kahneman, Bayes lit).
- **`local-inference`** — inferred from source-backed material; not stated verbatim.
- **`analogy`** — useful Arcanum mapping, **not** source meaning.
- **`operator-reading`** — practical design interpretation for the user (Arcanum bridge).
- **`open-residue`** — unresolved question or future task.

## How to extend

Drop new evidence into `levels/L0-corpus.md` first, label it in `claim-ledger.md`, then let it
flow up. Never promote a claim above the ledger without a source-kind label. Never turn an
`analogy` / `operator-reading` into a `primary-source` claim. **LOCAL-ONLY** — never touch the
public `arcanum` submodule.
