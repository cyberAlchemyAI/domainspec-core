# TOWER.md — Structure & File Roles

**Lane:** feijo-moreira-entailment-summ
**Subject:** LegalSumm — entailment-filtered abstractive summarization of legal rulings.

## Tower layers

| Layer | File | Role |
|---|---|---|
| L0 — Corpus | `L0-corpus.md` | Source record, section map (as known), date checked, paywall accessibility note. |
| L1 — Terms | `glossary.md` | Plain-language definitions of the 5 core terms. |
| L1 — Governed defs | `definitions.md` | Canonical, governed definitions used elsewhere in the tower. |
| L2 — Claims | `claim-ledger.md` | Every claim with a source-kind label (primary / related / inference / analogy / operator-reading / open-residue). |
| L3 — Distill | `distill.md` | One-sentence model, compositional spine, borrow/analogy/block. |
| L3 — Bridge | `bridge-decisions.md` | Mapping decisions Paper → Jus IA smart summaries, with statuses. |
| L4 — Pack | `LEARNING-PACK.md` | The deliverable read: source-backed claims, operator model, faithfulness takeaways, 5 things for the call, honest cutoff. |
| Residue | `open-residue.md` | Unverified / paywalled items, with what would resolve each. |
| Entry | `README.md` | Orientation + read order. |

## Source-kind labels (used throughout)
- **primary-source** — stated in the 2023 paper's open abstract/metadata.
- **related-source** — from the RulingBR paper (PROPOR 2018), thesis, or other open works by the same authors.
- **local-inference** — reasoned by the tower builder from source claims (clearly marked).
- **analogy** — mapping to Jus IA; an Arcanum reading, not a source claim.
- **operator-reading** — how an operator should interpret/apply the idea.
- **open-residue** — not verifiable from open sources (behind paywall) — never fabricated.

## Build provenance
- Springer landing paywalled (303 → SSO). Open metadata via dblp, search-surfaced Springer/ACM abstract, RulingBR GitHub + Semantic Scholar, UFRGS thesis listing.
- PDF text extraction of the open thesis was **not** possible in this environment (no PDF renderer); deeper internals are residue.
