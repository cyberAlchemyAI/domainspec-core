# Bridge Decisions (Arcanum ← Rationality)

The **NON-SOURCE** layer. Each row maps a corpus idea to an explicit Arcanum stance. These are
`operator-reading` / `analogy`, never corpus claims (reviewer S1 confirmed no leak across the
seam). Statuses reconciled with reviewer **S2** (precedent + non-vacuity gate). Status vocabulary:

- **`borrow-carefully`** — adopt the mechanism with stated guardrails;
- **`analogy-only`** — illuminating comparison, do **not** operationalize;
- **`block`** — do not import (category error / scope mismatch);
- **`promotion-candidate`** — worth promoting; needs a separate governed decision;
- **`already-owned`** — Arcanum already has this mechanism under another name; cite the corpus as
  *motivation*, operationalize nothing new (S2's "build-from-owned" relabel — not a kill);
- **`future-work`** — relevant but under-sourced/undecided.

| id | corpus idea (anchor) | Arcanum target | S2 precedent | witnessed? | status | guardrail / why |
|---|---|---|---|---|---|---|
| B1 | "beliefs pay rent in anticipated experience" (P2) | falsifiability check on spec claims | **P10 claim ≤ proof** (owns it) | no — P10 already produces the verdict | **already-owned** | cite as motivation for P10; the underlying verificationism is contested (R1) |
| B2 | semantic stopsign (B1) | prose lint for governance docs ("robust/aligned/best-practice" that constrain nothing) | none (research-tower labels flag provenance, not vacuity) | **yes** — flag empty terms in `domainspec-subagents-strategy`/constitution prose | **promotion-candidate** | strongest, lowest-baggage borrow; pilot on a doc-set, then a governed promotion |
| B3 | map / territory (R11 origin) | spec ↔ reality correspondence; drift = map diverging | partial — definitions-governance drift checks | weak — would re-describe existing drift checks | **analogy-only** | pedagogy; credit Korzybski, not the corpus |
| B4 | Conservation of Expected Evidence (P4) | review-rubric symmetry (a rubric that can only raise confidence is mis-designed) | partial — check-tension covers *sheets*, not rubrics | **yes** — a one-directional review rubric | **promotion-candidate (scoped to rubric design)** | fills a real gap downstream of check-tension; formalizable |
| B5 | the bottom line / rationalization (P3) | pre-registering dispatch sheets / criterion before running | **experiment-type frozen `criterion.md` at the P2 gate** (owns it) | no — it *is* the existing mechanism | **already-owned** | use as the *rationale* for pre-registration; borrow nothing new; don't overclaim it's proven (L5) |
| B6 | terminal vs. instrumental values (origin `open-residue`) | goal vs. success-metric; guard proxy drift (Detached Lever) | partial — promotion guardrails guard proxy drift indirectly | **yes** — optimizing a reflection/telemetry signal that detached from dispatch quality | **borrow-carefully** | real gap (metric drift in `domainspec-reflect`/telemetry); keep analogy-grade — origin unverified |
| B7 | "optimization process" as a unifying abstraction | (nothing to borrow) | n/a | n/a | **block** | analogy sold as theorem (L3); importing it replicates the overreach tensioning guards against |
| B8 | MWI-style "the debate should be over" on empirically-equivalent options | (anti-pattern, not a borrow) | inverse — violates P10 / rent-criterion | yes, inverted | **block** (keep inverted) | retain as a *guardrail example* for check-tension: high confidence on empirically-equivalent options is a detectable anti-pattern (L2) |
| B9 | Twelve Virtues — "the void" (technique subordinate to intent) | reminder that scaffolding serves the goal | partial — "native skills preferred over nested CLI" ethos (CLAUDE.md) | no — soft/cultural | **future-work** | park until a concrete governance-fatigue problem exists |
| B10 | cult attractor / epistemic viciousness (B6) | community-level: framework drifting into ritual that suppresses error-correction | partial — check-tension counters consensus-collapse at init | weak — cross-dispatch/time drift not covered; bodies `open-residue` | **future-work** | relevant to anti-bias tensioning; needs its own design treatment + sources |

## Tally

already-owned **2** (B1, B5) · analogy-only **1** (B3) · promotion-candidate **2** (B2, B4-scoped)
· borrow-carefully **1** (B6) · block **2** (B7, B8) · future-work **2** (B9, B10).

## Promotion boundary

All rows are **LOCAL-ONLY**. A `promotion-candidate` (B2, B4) is a *flag*, not a promotion — it
requires a separate governed decision (definitions-governance / constitution-governance) before
any vocabulary or behavior enters Inventory, Ontology, sigils, spells, or runtime contracts.
`already-owned` (B1, B5) means **do not re-promote** — the mechanism exists; the corpus only
supplies motivation. Nothing here is written into the public `arcanum` submodule.
