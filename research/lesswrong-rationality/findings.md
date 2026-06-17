# Findings — *Rationality: A-Z* dissection (cited synthesis)

**Dispatch:** `2026-06-16-lesswrong-rationality-dissection` (`dispatch_type: research`).
**Inputs:** `_dispatch/lens-E1.md` (charitable/internal), `_dispatch/lens-E2.md`
(adversarial/external), `_dispatch/lens-E3.md` (historical/lineage), synthesized in
`_dispatch/findings-draft.md`, then corrected per reviewer findings (S1 faithfulness, S2
precedent/non-vacuity). This file is the **final, accepted** synthesis; every load-bearing
claim cites the lens it rests on (P9). Full claim table → [claim-ledger.md](claim-ledger.md);
bridge decisions → [bridge-decisions.md](bridge-decisions.md).

> **Honesty cut-off (all three lenses concur):** ~60% of direct essay-slug URLs 404'd. Much
> per-book detail is therefore title-level `[open-residue]` and is **not** inflated to
> primary-source confidence. See [residue/open-residue.md](residue/open-residue.md).

## One-paragraph model

The six books are one argument: *the quality of a mind's map of reality bounds everything that
mind can do or protect* (`[local-inference, per lens-E1]`). **B1 Map and Territory** sets the
standard (beliefs are maps; a belief that predicts nothing — "pays no rent" — is social
performance, not knowledge). **B2 How to Actually Change Your Mind** diagnoses the obstacle (the
human algorithm writes "the bottom line" first, then recruits arguments). **B3 The Machine in
the Ghost** grounds the obstacle in history (minds are *adaptation-executors*, not
fitness-maximizers). **B4 Mere Reality** supplies the worldview the map converges on
(reductionist physicalism + Bayes; dissolve mind-projection pseudo-problems). **B5 Mere
Goodness** applies it to value (human values are the fragile output of B3's machine; optimizing a
detached proxy destroys what it claims to serve). **B6 Becoming Stronger** institutionalizes the
art (precise vocabulary, error-correcting community, "something to protect").

## Cross-book spine + adversarial counter-spine

- **Spine** (`[local-inference, per lens-E1; lineage per lens-E3]`): B1 standard → B2 obstacle →
  B3 origin → B4 worldview → B5 value → B6 practice. The B1 epistemic tool is *re-sharpened* by
  each new domain (recurrence matrix in lens-E3).
- **Counter-spine** (`[local-inference, per lens-E2]`): the spine has a fault line — B1's
  rent/verificationist criterion is **contradicted** by B4's Many-Worlds verdict (an
  empirically-equivalent interpretation chosen on simplicity "pays no differential rent"); the
  "optimization process" abstraction unifying B3/B5 is *analogy sold as theorem*; idealizations
  (Solomonoff uncomputable, Bayesian logical omniscience, EU-maximizer minds vs. B2's own biases)
  are presented as the normative skeleton with their inapplicability downplayed.

## What the external literature genuinely backs (per lens-E2)

Evidence = informational entanglement (Shannon); the *core* Kahneman–Tversky biases
(availability, representativeness, anchoring, conjunction — replicated); foresightless evolution
& adaptation-executors (Williams; Tooby & Cosmides); "no universally compelling arguments"
(≈ Hume + orthogonality). What it does **not** back as stated: MWI consensus, Solomonoff as a
usable razor, verificationism, debiasing transfer, morality as a single well-defined computation.

## Reviewer reconciliation (zig-zag loop 1, applied by parent / final_approver)

**S1 (faithfulness) — 0 blockers, 2 major, 2 minor; all applied:**
- *Major* — "words as mental paintbrush handles" (B6) was `[primary-source]` in the draft claim
  but `[open-residue]` in its own vocab line; **downgraded** to `[open-residue]` on the phrasing.
- *Major* — claim **P6** ("No Universally Compelling Arguments / morality = a human computation")
  was recovered via mirror/summary, not a canonical fetched body; **re-labeled**
  `[primary-source — via mirror/summary, not canonical body]`.
- *Minor* — split E2's "strongest part of the corpus" judgment out of P1's `[primary-source]`
  line into `[local-inference, per lens-E2]`; qualified P5's "corroborated" as *external-literature*
  backing (`[related-source]`), not corpus corroboration.
- **Seam verdict: holds.** No `[analogy]`/`[operator-reading]` bridge leaked into a corpus claim.

**S2 (precedent + non-vacuity on bridges) — re-scored 4 candidates; all applied:**
- **B1** ("pay rent" → falsifiability gate) and **B5** (bottom line → pre-registration) are
  **already owned** by Arcanum (P10 claim ≤ proof; experiment-type frozen `criterion.md` at the
  P2 gate) → relabeled from borrow-carefully to **already-owned (cite as motivation, operationalize
  nothing new)**.
- **B3** (map/territory → spec↔reality) is mostly owned by definitions-governance drift checks →
  **analogy-only**.
- **B4** (Conservation of Expected Evidence → review-rubric symmetry) → **promotion-candidate,
  scoped to rubric design** (check-tension already covers *sheets*, not downstream rubrics).
- **Confirmed:** B2 strongest promotion-candidate; B6 borrow-carefully (witnessed: proxy/metric
  drift in reflection telemetry); B7/B8 block; B9/B10 future-work.

## P9 acceptance (final_approver = parent)

Every load-bearing claim above and in [claim-ledger.md](claim-ledger.md) cites a lens return;
the source layer (claims) and bridge layer (Arcanum readings) are strictly separated; the
~60% fetch gap is recorded as residue, not hidden. **Accepted →** `exit_reason: resolved`.

## One-line answer to the dispatch goal

*Rationality: A-Z* is one escalating argument that map-quality bounds capability; it is
source-faithfully mappable across all 6 books, but several keystones (MWI, verificationism,
"fixed computation" metaethics, trainability) are author leaps the external literature does not
license — and of the 10 Arcanum bridge candidates, **2 are already owned, 1 is analogy-only, 2
are scoped promotion-candidates, 2 borrow-carefully, 2 block, 2 future-work** (none promoted).
