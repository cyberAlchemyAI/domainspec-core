# Stage 05 — Distill

Capability: `distill` · Mode: `standard` · Overlay: `tournament_for_alternatives` · Status: **pass**
Roles: candidate-a, candidate-b, candidate-c, synthesis · Inputs: refine-review ledger (s03)

## Candidate improvement framings (tournament)

| # | Framing | What it changes | Cost | Owner-boundary risk |
| --- | --- | --- | --- | --- |
| A | **Validity-and-clarity repair** (surgical) | Fix the 2 BLOCK causes + 4 FLAGs so the dispatch passes; fix the `.md` self-test command; add a scope-boundary paragraph. Preserve all lane design. | low | none (writes only `ops/development/infra-spec-*`) |
| B | **Redesign the lanes** (MVP-first restructure) | Collapse 7 lanes into a phased MVP (L1+L2+L7 first), reorder steps, rewrite receipts. | high | low, but destroys reviewed design |
| C | **Defer / document-only** | Record the defects in a note; do not edit the artifacts. | trivial | none |

## Convergence criteria

1. Satisfies the strategy's own non-negotiable (route must pass validation) — A yes, B yes, C no.
2. Preserves reviewed design (B4 no-regression) — A yes, B no, C yes.
3. Lowest reversible cost for highest correctness gain — A best.
4. Resolves the demonstrated conflation risk (B3) — A yes, B yes, C partial.

## Pareto gate / selection

- **C** is dominated: it leaves the strategy non-executable (fails criterion 1).
- **B** wins only criterion 1 and 4 at the price of criterion 2 and high cost; the s03 critic explicitly flagged lane-rewrite as scope creep. Rejected for this run.
- **A dominates**: wins criteria 1–4 at low, fully reversible cost.

## Selected coherent unit

> **A — Validity-and-clarity repair.** Make the existing infra-spec research strategy pass the native validator (receipt-field completeness + capability-handle metadata), repair the `.md` self-test command to the in-checkout validator path, and add a scope-boundary paragraph distinguishing infra-spec from runtime-surface convergence. All 7 lanes, gates, boundary_evidence, and guardrails are preserved verbatim.

## Rejected alternatives (recorded)

- B (lane restructure) — kept as **residue/recommendation**: an MVP-first ordering (L1 cartographer + L2 Lean translator + L7 gap hunter as a cheap first pass) is worth offering, but only with explicit operator sign-off. Not executed.
- C (document-only) — rejected; does not restore executability.

## Recomposition target

The selected unit recomposes into the larger system as: a *validated* strategy route that the existing `validate-research-coverage` gate and the documented self-test command can both actually run, unblocking the strategy's intended next route (read-only fan-out execution).

## Verdict

`pass` — single coherent improvement selected with rejected alternatives recorded as residue.
