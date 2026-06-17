---
id: criterion-c1-validator-spike-2026-06-16
dispatch: 2026-06-16-c1-validator-spike-criterion
dispatch_type: experiment
phase: propose
status: FROZEN
authored_before_run: true
validity: VALID-to-freeze (skeptic re-check pass, 2 zig-zag iterations)
verdict_vocabulary: [SURVIVED, FALSIFIED, INVALID]
grounding:
  - projects/ui-prototyping-studio/development/refinement-runs/20260615-mutation-execution-mechanics/RESULT.md
  - .../stages/06b-validator-model.md
  - .../stages/08-toy-game.md
frozen: 2026-06-16
---

# C-1 Scope-Attribution Criterion (V3 REJECT/NOT_REJECT)

> **Pre-registered, frozen criterion** for the C-1 spike — authored and validity-checked
> **before any run**. The deliverable of an `experiment`-propose dispatch. Read-only downstream:
> any edit is a *new* criterion that re-enters the human gate. Running the spike (build the V3
> fence, materialize fixtures, render the per-fixture verdicts) and adjudicating
> SURVIVED/FALSIFIED is a **separate downstream step**.

## Non-goals

- Does **not** decide which production R2 attribution mechanism (R2-a vs R2-b) the studio ships.
- Does **not** establish that V3 **generalizes** beyond the closed fixture set frozen here.
- No rendering, layout, or visual diffing — only od-id scope attribution over the canonical tree.
- Does **not** validate the baseline revision anchor; the frozen baseline od-id→node binding is
  taken as trusted ground truth.
- Does **not** test acceptanceText satisfaction (human-judged at accept-diff; GAP-ACCEPTANCE-CHECK-007)
  or V9 calibration constants S/B/k/c.

## What V3 is (H1)

**H1.** V3 is a pure function

```
V3(candidateHtml, taskScopeOdIds, frozenBaselineBinding, r1ScopeRuleSpec) -> { REJECT | NOT_REJECT }
```

- `candidateHtml` — the candidate document under test (untrusted; may self-assert od-ids).
- `taskScopeOdIds` — `TaskScope`, the in-scope od-id set. **MUST contain ≥2 od-ids.**
- `frozenBaselineBinding` — a **trusted frozen od-id→node binding** materialized from the baseline
  revision anchor at freeze time. The authority for which node legitimately carries which od-id.
  **Not** derived from `candidateHtml`.
- `r1ScopeRuleSpec` — the frozen R1 scope-rule specification. Carries **no expect labels**.

V3 returns **REJECT** iff, after canonicalization, any attributed change touches a node whose
od-id is **not** in `taskScopeOdIds`, OR the candidate's self-asserted od-id→node association
disagrees with `frozenBaselineBinding`, OR attribution cannot be resolved (⊥ collapse). Otherwise
**NOT_REJECT**.

### Attribution rule (pinned)

- Canonicalize `candidateHtml` with the frozen canonicalizer → the **canonical tree**.
- Each mutated/added node is attributed to the od-id its canonical-tree position resolves to under
  `r1ScopeRuleSpec`.
- **CSS attribution (pinned, mechanism-neutral):** a `<style>` rule is attributed to the od-ids
  whose nodes its selector resolves to over the candidate's canonical tree. A selector spanning
  in-scope and out-of-scope od-ids attributes every resolved out-of-scope od-id ⇒ REJECT.
- **od-id integrity:** every od-id the candidate asserts is checked against `frozenBaselineBinding`;
  a node carrying an od-id bound to a different node (forge/re-tag) is a disagreement ⇒ REJECT.

### Canonicalizer identity (frozen)

- name: `domainspec-html-canon` · version: `1.4.0` · normalization-spec hash: `sha256:c1a9f0e2b7`
  (attribute-order normalization, whitespace collapse, void-element normalization, od-id preservation).
- Any change to name/version/normalization-spec hash is **fixture-set drift** ⇒ INVALID.

### ⊥ / unattributable collapse (explicit)

Canonicalization failure, parse failure, or any mutated node unresolvable to an od-id ⇒ **REJECT**.
Unattributable is never NOT_REJECT.

## Verdict rule (ordered: INVALID → FALSIFIED → SURVIVED)

First match wins.

1. **INVALID** if any of: V3 consumed input **beyond** the four listed (in particular this
   criterion, any expect labels, or fixture identities); the run-time canonicalizer identity ≠ the
   frozen identity; `fixtures.lock` content hashes ≠ the materialized fixture files (drift);
   `taskScopeOdIds` < 2; any fixture's expected verdict was visible to V3.
2. **FALSIFIED** if the run is valid AND V3 disagrees with the pinned expected verdict on **any**
   GOOD / BAD / HELD-OUT fixture (held-out included).
3. **SURVIVED** if the run is valid AND V3 matches **every** fixture. **Interpretation:** V3 is
   correct on this **closed set (incl. held-out)**. Generalization beyond it is **NOT** established
   by this spike.

## Fixtures

`TaskScope = { od-id:A, od-id:B }`. Out-of-scope od-ids: `od-id:X`, `od-id:Z`. All fixtures are
materialized as HTML files at freeze/run-setup and hashed into `fixtures.lock`.

**GOOD (expect NOT_REJECT)**
- **GOOD-1** — text edit confined to the node bound to `A`; od-ids agree with the binding.
- **GOOD-2** — `<style>` rule resolving **only** to nodes bound to `A`,`B` (in-scope CSS).
- **GOOD-3 (byte-adjacency)** — edit to the node bound to `B`, byte-adjacent to an out-of-scope
  `X` sibling. Whole-tree attribution must attribute only to `B`. Kills "subtree-contains-one-id".

**BAD (expect REJECT)**
- **BAD-1** — text edit to a node bound to out-of-scope `X`.
- **BAD-2** — `<style>` rule whose selector spans `A` (in) and `X` (out) ⇒ REJECT.
- **BAD-3 (forge)** — candidate asserts `A` on a node the binding binds to `X` ⇒ disagreement.

**HELD-OUT (sealed; expected verdicts pinned, hidden from V3 during build)**
- **HELD-4 (re-tag, REJECT)** — candidate re-tags `B` onto a node bound elsewhere ⇒ disagreement.
- **HELD-5 (in-scope CSS, NOT_REJECT)** — `<style>` resolving only to `A` via a selector form
  distinct from GOOD-2.
- **HELD-6 (NOT_REJECT)** — in-scope **attribute mutation** on `A` (e.g. `aria-label`).
- **HELD-7 (NOT_REJECT)** — in-scope **node addition** under `B`.
- **HELD-8 (REJECT)** — out-of-scope `Z` via **node deletion**; mechanism + od-id absent from any
  visible BAD shape (anti-overfit).

Closed set: GOOD-1..3, BAD-1..3, HELD-4..8 (11 fixtures). No add/remove/relabel after freeze
without re-issuing the criterion.

## Discrimination

Kills `always-NOT_REJECT` (BAD-1/2/3, HELD-4, HELD-8), `always-REJECT` (GOOD-1/2/3, HELD-5/6/7),
`subtree-contains-one-id` (GOOD-3, BAD-2), `trust-candidate-od-ids` (BAD-3, HELD-4), and
`only-shown-mechanisms` (HELD-8). A FALSIFIED locates the open horn by fixture (false-admit = too
loose / scope-false-reject = too strict / held-out-only = overfit); a SURVIVED clears the scope
dimension of RESIDUE-B on the closed set.

## Reproducibility

Freezing materializes every fixture as an HTML file and records each content hash in
`fixtures.lock` beside this file; the canonicalizer identity is pinned above; `frozenBaselineBinding`
and `r1ScopeRuleSpec` are content-addressed at the same commit. A later adjudicator re-derives only
V3 + the §rule (never re-running the proposer). Same fixtures → same `v3(f)` → same verdict. Any
missing per-fixture output, nondeterministic V3, or drift ⇒ INVALID, never a silent SURVIVED.
