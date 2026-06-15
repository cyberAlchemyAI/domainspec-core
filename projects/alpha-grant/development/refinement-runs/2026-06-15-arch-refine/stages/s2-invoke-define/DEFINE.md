# s2 — Invoke Define

- Capability: `invoke` · Mode: `define`
- Receipt kind: native-stage · Status: `pass`
- Inputs: `stages/s1-context-builder/context-pack.md`, `REFINE-SEED-PROPOSAL.md`
- Protected context flagged: KU/INVAM, MTA/strain, unverified partner claims (O1, O2, O5)

## What we are defining

The **initial architecture** of the Decentralized Living Library: the structure
that decides *who owns what, which money funds which asset, and which boundaries
must never be crossed* — not the project's marketing or its grant prose.

## Problem statement

The current architecture is expressed as prose across nine sections. It is
*complete as a kit* but *implicit as an architecture*: ownership, authority,
asset-class boundaries, and lane dependencies are described in rules rather than
drawn as a structure. Two consequences:

1. The most consequential decision — the **entity-home** of public collection
   assets — is deferred to the 90-day path, so every downstream ask inherits an
   unresolved owner.
2. The system carries a standing tension (public-benefit infrastructure that
   must stay mission-locked, *living alongside* private commercial IP, co-op
   revenue, and a funding-OS operator). The boundaries section manages this
   tension by prohibition; the architecture does not yet *encode* it.

## Definition of the refined architecture (target)

A refined architecture is one where:

- **D1 — Nodes** are typed by what they may own (public-benefit / private-IP /
  cooperative / university / funding-OS) and by their verification status.
- **D2 — Assets** (collection accessions, DNA vouchers, host cultures, data,
  IP/formulas, brand, donor relationships) each have exactly one owning lane and
  a stated mission-lock or licensing rule.
- **D3 — Asks** map to a node + asset + entity-home + go/no-go owner, never to a
  bare amount.
- **D4 — Entity-home** is a single resolved (or explicitly operator-pending)
  decision that the rest of the architecture hangs from.
- **D5 — Boundaries O1–O6** are expressed as architectural gates, not just
  cautionary text.
- **D6 — A minimum viable spine** is named: the smallest set of nodes + assets +
  asks that stands up the living library and recomposes into the full network.

## In scope

Structure, ownership, authority, asset-class boundaries, entity-home fork, lane
dependency ordering, minimum spine, boundary gates.

## Out of scope

Writing the actual grant proposals; selecting specific funders; financial
modeling of amounts; executing the 90-day path; mutating the source doc.

## Success test

A reader can answer, from one artifact: *which node owns this asset, what funds
it, what entity it lives in, and which boundary protects it* — for every asset
class — and can see the minimum spine that must exist before anything else.
