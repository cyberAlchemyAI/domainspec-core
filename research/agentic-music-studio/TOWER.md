# TOWER — agentic-music-studio

A learning tower is a layered scaffold: each layer rests on a verified one below it.
Lower = closer to source; higher = closer to use. The bridge layer is always labeled
NON-SOURCE and never rewrites a layer beneath it.

```
                ┌─────────────────────────────┐
   USE          │  LEARNING-PACK.md           │  operator model, the 10-process taxonomy,
                │  bridge-decisions.md        │  borrow/block, "what to take into the build", cutoff
                └─────────────────────────────┘   ← BRIDGE layer (NON-SOURCE, labeled)
                              ▲
                ┌─────────────────────────────┐
   DISTILL      │  distill.md                 │  one-sentence model, compositional spine,
                │  findings.md                │  full interface/process taxonomy
                └─────────────────────────────┘
                              ▲
                ┌─────────────────────────────┐
   GOVERN       │  definitions.md             │  governed defs for load-bearing terms
                │  glossary.md                │  quick glossary (source kind per entry)
                └─────────────────────────────┘
                              ▲
                ┌─────────────────────────────┐
   ADJUDICATE   │  claim-ledger.md            │  every claim + source-kind label
                │  residue/open-residue.md    │  unresolved questions / future work
                └─────────────────────────────┘
                              ▲
                ┌─────────────────────────────┐
   SOURCE       │  levels/L0-corpus.md        │  source record, corpus boundary,
                │  research.md                │  working synthesis trail
                └─────────────────────────────┘
```

## Layer contract

- **SOURCE** holds what the cited corpus actually says (TidalCycles, Xenakis/GENDYN, Sethares,
  NIME, Strasheela) plus the boundary of what was *not* read.
- **ADJUDICATE** labels each claim `primary-source`, `related-source`, `local-inference`,
  `analogy`, `operator-reading`, or `open-residue`. The operator's design question is answered
  mostly at `local-inference` / `operator-reading` — and is labeled as such, not dressed up as
  source fact.
- **GOVERN** fixes the meaning of terms the higher layers lean on (spec, objective-function
  steering, stochastic synthesis, dissonance curve, communication process, mapping).
- **DISTILL** compresses to the operator model and lays out the ten communication processes.
- **BRIDGE (NON-SOURCE)** decides what the real build should borrow, treat as analogy only,
  block, promote, or defer — and names the honest cutoff.

## Single load-bearing claim

The studio's intelligence lives in **deterministic engineering and objective-driven search over a
shared spec**, not in generating audio from a prompt. Every interface — voice, live-code, gesture,
annotation — is an *editor of one reproducible spec*. This is the claim everything above SOURCE
depends on; it is `local-inference` (a design stance), defended in `claim-ledger.md` and
`bridge-decisions.md`, not a source result.
