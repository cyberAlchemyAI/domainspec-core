# mtng-resonantos — Research Tower

A source-backed learning tower over the **MTNG Review Packet v2**
(`../MTNG-review-packet-v2-2026-06-17-clean/`).

**MTNG** = *Modal Tonal Nodal Graph* — a proposal by Dave Gardner for **ResonantOS** that
turns selected messy work evidence (terminal logs, chat transcripts, git diffs, bug notes)
into reviewable artifacts (developer issue packets, memory candidates, contribution records,
OKF exports). After three outside reviews, V1 was narrowed to a **Post-Hoc Issue Packager**:
on-demand, selected-input, sidecar/CLI, audit-first, *no live runtime orchestration*.

## Why this tower exists

The user asked to (1) build a durable research tower over the packet and (2) **review** the
content. The tower separates what the packet *says* (source) from what it *implies* (inference)
from what we *recommend* (operator/bridge), and the review attacks the spec adversarially.

## Read order

1. `TOWER.md` — the layer map and the source-kind discipline.
2. `levels/L0-corpus.md` — what is in the packet, file by file.
3. `claim-ledger.md` — every load-bearing claim, labeled by source kind.
4. `glossary.md` / `definitions.md` — the vocabulary (Signal → Mode → Node → Validator → Synthesis).
5. `distill.md` — the one-screen model.
6. `LEARNING-PACK.md` — decision-ready operator takeaways + honest cutoff.
7. `bridge-decisions.md` — borrow / analogy-only / block / promotion-candidate / future-work.
8. `REVIEW.md` — red-team change requests (produced by a gated, tensioned review dispatch).
9. `residue/open-residue.md` — what is unverified and what to do next.

## Status

- Depth: **standard→full**.
- Promotion boundary: **local-only**. Nothing here promotes vocabulary or behavior into
  Inventory, Ontology, sigils, spells, or canonical definitions without a separate governed
  promotion decision.
- Source boundary: the ResonantOS codebase and the OKF spec were **not** fetched. All claims
  about them are `related-source` and tracked as residue.
