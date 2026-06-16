# TOWER — Levels & Reading Order

A research tower is a layered climb: raw source at the bottom, a portable accelerator
at the top. Each level only depends on the ones below it.

```
  L4  LEARNING-PACK  ── the accelerator: 5 things for the call + honest cutoff
       │
  L3  DISTILL + BRIDGE  ── one-sentence model, compositional spine, borrow/block for Jusbrasil
       │
  L2  GLOSSARY + DEFINITIONS  ── governed meanings of the load-bearing concepts
       │
  L1  CLAIM-LEDGER  ── every claim, tagged by source kind
       │
  L0  CORPUS  ── the source itself: citation, boundary, section map
```

## Level descriptions

- **L0 — Corpus (`L0-corpus.md`).** The single source of record. Full citation,
  canonical links, date checked (2026-06-10), what the paper does and does NOT cover,
  and a section-by-section map. Everything above cites back to here.

- **L1 — Claims (`claim-ledger.md`).** The paper decomposed into discrete claims, each
  tagged: primary-source, related-source, local-inference, analogy, operator-reading,
  open-residue. Headline numbers (17–33% hallucination, retrieval-vs-generation
  attribution, groundedness≠correctness) live here as primary-source.

- **L2 — Distill of meaning (`glossary.md`, `definitions.md`).** Terms and the 3–5
  load-bearing concepts pinned to formal meaning + intuition + anti-misuse so the
  reader cannot drift on what "hallucination" or "grounded" means in this paper.

- **L3 — Distill of use (`distill.md`, `bridge-decisions.md`).** Collapses the paper to
  a one-sentence model and a compositional spine (how the audit works end to end), then
  decides — explicitly — what Jusbrasil should borrow, treat as analogy-only, or block.

- **L4 — Learning pack (`LEARNING-PACK.md`).** The portable accelerator. Source-backed
  claims + operator model + decisions + the 5 things to remember for the call + an
  honest cutoff of what abstract-level fetching could not verify.

## Recommended reading order

**Fast path (call prep, ~10 min):** L4 only → fall back to L1 for any number you must cite.

**Full path (decomposition, ~30 min):** L0 → L1 → L2 → L3 → L4 → `open-residue.md`.

## Residue lane

`open-residue.md` sits beside the tower, not inside the climb. It collects everything
the climb could not close — primarily exact crosstab figures and appendix detail that
need the full PDF.
