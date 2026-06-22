# TOWER — mtng-resonantos

A learning tower is a layered scaffold: each layer rests on a verified one below it.
Lower = closer to source; higher = closer to use. The Arcanum bridge layer is always
labeled NON-SOURCE and never rewrites a layer beneath it.

Target: the **MTNG Review Packet v2** (`02-…/research/MTNG-review-packet-v2-2026-06-17-clean/`,
immutable — ships SHA-256 manifest). MTNG = *Modal Tonal Nodal Graph*, a proposal by Dave
Gardner for ResonantOS. This tower does **not** edit the packet; `L0-corpus.md` records and
points back to it.

```
                ┌─────────────────────────────┐
   USE          │  LEARNING-PACK.md           │  operator model, borrow/block,
                │  bridge-decisions.md        │  "what to take into Arcanum", cutoff
                │  REVIEW.md                  │  ← red-team findings (dispatched, gated)
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
                │  residue/open-residue.md    │  unverified / needs external evidence
                │  levels/L1-residue-map.md   │  residue map
                │  levels/L2-closure-plan.md  │  closure plan
                └─────────────────────────────┘
                              ▲
                ┌─────────────────────────────┐
   SOURCE (L0)  │  levels/L0-corpus.md        │  source record, 9-file packet map,
                │                             │  Analog6 PDF extract, cutoff note
                └─────────────────────────────┘
```

## Layer contract

| Layer | File(s) | Promise | Source-kind discipline |
|---|---|---|---|
| L0 Source | `levels/L0-corpus.md` | Faithful record of what exists in the packet, where, what was extracted | `primary-source` only; gaps marked |
| Adjudicate | `claim-ledger.md`, `residue/open-residue.md`, `levels/L1-residue-map.md`, `levels/L2-closure-plan.md` | Each claim labeled by source kind; gaps named | full source-kind taxonomy below |
| Govern | `definitions.md`, `glossary.md` | Stable meaning for load-bearing terms | source kind per entry; promotion status |
| Distill | `distill.md` | Smallest coherent model that recomposes | reading layer, labeled as such |
| Use (BRIDGE) | `LEARNING-PACK.md`, `bridge-decisions.md`, `REVIEW.md` | Decision-ready takeaways + red-team change requests | bridge/operator readings labeled NON-SOURCE |

## Source-kind taxonomy (from the research-tower sigil — used throughout)

- **`primary-source`** — stated by the main source (MTNG build spec v2, the packet docs).
- **`related-source`** — stated by a related/external source (the 3 outside reviews; OKF spec; ResonantOS repo docs).
- **`local-inference`** — inferred from source-backed material; not stated verbatim.
- **`analogy`** — useful Arcanum mapping, **not** source meaning.
- **`operator-reading`** — practical design interpretation for the user (Arcanum bridge).
- **`open-residue`** — unresolved question or future task.

## Important boundary

The MTNG packet **asserts** the existence of a ResonantOS codebase (Guardian Core, Blackboard,
Bridge Server, Event bus, Provider fabric, Living Archive) and of "Google's Open Knowledge
Format (OKF)". **Neither was fetched or verified by this tower** — no repo, no OKF spec was
read. Every such claim is `related-source` (asserted by spec/reviewers) and lives as open
residue. Do not promote them to `primary-source`. See `residue/open-residue.md`.

## How to extend

Drop new evidence into `levels/L0-corpus.md` first, label it in `claim-ledger.md`, then let it
flow up. Never promote a claim above the ledger without a source-kind label. Never turn an
`analogy` / `operator-reading` into a `primary-source` claim. **LOCAL-ONLY** — never touch the
public `arcanum` submodule, and never edit the immutable packet.
