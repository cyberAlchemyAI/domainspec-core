# L2 — Closure Plan (the governed dispatch route)

How the tower's upper layers get built and closed, via a governed `dispatch_type: research`
subagent dispatch under `.claude/skills/domainspec-subagents-strategy`.

## Why a dispatch (P1 trigger)

- **synthesis** — 6 books + many sequences must be combined into one map. ✅
- **context protection** — raw essay text ≫ what the tower needs. ✅
- **parallelism** — the 6 books are independent reading lanes. ✅

Three triggers hold → dispatch is warranted (not inline work).

## Dispatch sheet (proposed — subject to check-tension gate + human confirm)

- **dispatch_id:** `2026-06-16-lesswrong-rationality-dissection`
- **dispatch_type:** `research` (LIVE)
- **working_folder:** `research/lesswrong-rationality/`
- **max_loops:** 1 · **final_approver:** `parent` (parent performs the P9 citation-acceptance check)
- **anti_bias_global:** source fidelity vs useful borrowing — keep what the corpus *says*
  strictly separate from what Arcanum *may adopt*.

### Groups (revised after check-tension gate v1 reproved a disjoint-book partition)

> **Gate finding (2026-06-16):** an earlier `book-readers` group (6 explorers, one per book)
> was reproved by both check-tension agents — a disjoint-book partition is *coverage*, not
> anti-bias *tension* (fails Test 3 spread: all six share one corpus; Test 4: no writable
> pairwise disagreement). Per-book ownership moved to the **coverage layer** (the synthesizer's
> deliverable); the explorer group is re-tensioned on **reading stance across the whole corpus**.

| group_id | role(s) | n | anti_bias axis | job |
|---|---|---|---|---|
| `lens-readers` | explorer | 3 | composite **methodology × source-corpus × temporal-prior** — all three read the *whole* 6-book corpus through a different stance, so they engage the same concepts and can disagree | E1 charitable/steelman source-internal · E2 adversarial/critical vs external academic literature (Kahneman/Tversky, Jaynes, cog-sci) · E3 historical-lineage / cross-book concept-tracing (2006–2009 origins) |
| `synthesizer` | writer | 1 | — | **deep per-book maps for all 6 books** (coverage) + cross-book spine + faithful claim synthesis + **labeled** bridge candidates, each citing a lens-reader return |
| `reviewers` | skeptic | 2 | attack-vector (faithfulness/definitional gate vs precedent/non-vacuity-on-bridges gate) | attack the draft: (1) source↔bridge boundary leaks & misrepresentation; (2) are bridge candidates real borrowable mechanisms or vacuous analogy → borrow / analogy-only / block |

Deep per-book coverage (the user's "all 6, deep" ask) is preserved: each of the 3 lenses spans
all 6 books, giving the synthesizer 18 lens-views (6 books × 3 stances) to build 6 deep book
maps + the cross-book spine — every book gets a charitable, a critical, and a historical reading.

### Connections (dependency-scheduled)

- `lens-readers → synthesizer` — **sequential** (synthesizer needs the 3 lens passes)
- `synthesizer → reviewers` — **zig-zag**, `loop_cap: 1` (synthesizer opens with the draft;
  reviewers attack; synthesizer revises once)

### Lens enforcement (user choice: "both, clearly separated")

The faithful layer (claim-ledger, glossary, definitions, distill) carries **only**
`primary-source` / `related-source` / `local-inference`. The Arcanum bridge layer
(bridge-decisions, LEARNING-PACK bridge section) carries **only** `analogy` /
`operator-reading`, always labeled NON-SOURCE. Reviewer skeptic #1 guards exactly this seam.

## Reconciliation → tower fill

Returns land in `research.md` + `findings.md` (working_folder). The parent then reconciles into:
`claim-ledger.md`, `glossary.md`, `definitions.md`, `distill.md`, `bridge-decisions.md`,
`LEARNING-PACK.md`, and updates `residue/` + `L1-residue-map.md`. Every book-reader lane gets a
row in the [subagent closeout ledger](../gates/closure-gates.md) with an integration decision.

## Status

`PROPOSED` → `check-tension gate (v1 reproved → revised → v2 both PASS)` → `human confirm
(2026-06-16)` → `register + run` → `reconcile` → **`CLOSED resolved`**. Recorded in
`telemetry/agents/subagents-dispatch.yaml` (dispatch row + close row). All 6 lanes integrated;
see [../gates/closure-gates.md](../gates/closure-gates.md).
