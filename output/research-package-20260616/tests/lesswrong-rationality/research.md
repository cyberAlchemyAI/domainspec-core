# Research — collected returns (verbatim, per P9)

This file collects the dispatch's raw lane returns. The full verbatim per-lane analyses live in
`_dispatch/` (one file per lens reader); the synthesizer draft and the two reviewer returns are
summarized below. The cited synthesis built from these is [findings.md](findings.md).

## Lens-reader returns (group `lens-readers`)

| lane | verbatim return | fetch reality |
|---|---|---|
| E1 charitable / source-internal | [`_dispatch/lens-E1.md`](_dispatch/lens-E1.md) | ~15–16 essay bodies fetched; ~60% of slug URLs 404'd → many concepts title-level `[open-residue]` |
| E2 adversarial / external-literature | [`_dispatch/lens-E2.md`](_dispatch/lens-E2.md) | corpus pages + external-lit web search; 2 URLs misresolved (Bayes essay, "No Universally Compelling Arguments") recovered via mirror/summary |
| E3 historical / lineage | [`_dispatch/lens-E3.md`](_dispatch/lens-E3.md) | sequence listings + keystone essays; terminal/instrumental origin essay 404'd on 4 attempts |

## Synthesizer draft (group `synthesizer`)

Verbatim draft: [`_dispatch/findings-draft.md`](_dispatch/findings-draft.md) — 6 per-book maps,
cross-book spine + adversarial counter-spine, 27-row claim table (P1–P8 / R1–R11 / L1–L5 / O1),
and 10 labeled Arcanum bridge candidates. Every load-bearing claim cites its lens.

## Reviewer returns (group `reviewers`, zig-zag from synthesizer)

**S1 — faithfulness / definitional-soundness gate.** Verdict: no blockers; 2 major + 2 minor
label issues; **the §4 bridge seam holds** (no analogy leaked into a corpus claim). Major: (4)
"mental paintbrush handles" claim tagged `[primary-source]` but `[open-residue]` in its own vocab
line → downgrade; (6) claim P6 labeled flat `[primary-source]` despite being mirror/summary-recovered
→ add provenance qualifier. Minor: split E2's "strongest part" judgment out of P1's primary-source
line; qualify P5's "corroborated" as external-literature backing.

**S2 — precedent + non-vacuity gate on bridge candidates.** Per-candidate verdict: **B1**
(pay-rent→falsifiability) and **B5** (bottom-line→pre-registration) are *already owned* in
Arcanum (P10 claim ≤ proof; experiment-type frozen `criterion.md` at the P2 confirm gate) →
relabel build-from-owned, operationalize nothing new. **B3** mostly owned by definitions-governance
drift checks → analogy-only. **B4** → promotion-candidate scoped to *rubric* design (check-tension
covers sheets, not downstream rubrics). Confirmed: **B2** strongest promotion-candidate (prose
"semantic-stopsign" lint); **B6** borrow-carefully, witnessed by proxy/metric drift in reflection
telemetry; **B7/B8** block; **B9/B10** future-work. Every "owner-in-Arcanum" was confirmed
in-repo (claim ≤ proof held).

All reviewer corrections were applied by the parent (final_approver) in [findings.md](findings.md),
[claim-ledger.md](claim-ledger.md), and [bridge-decisions.md](bridge-decisions.md). Lane
closeout: [gates/closure-gates.md](gates/closure-gates.md).
