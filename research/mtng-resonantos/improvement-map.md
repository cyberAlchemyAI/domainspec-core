# Improvement Map (NON-SOURCE)

How this repository's verified capabilities should improve the MTNG v2 proposal —
the **forward** mapping (repo capability → MTNG gap). This complements
`bridge-decisions.md`, which runs the **reverse** mapping (MTNG idea → Arcanum).
Nothing here promotes anything into Arcanum: it is **advice to MTNG only**. Every
row is an `operator-reading`/`adaptation`, never a source claim. **Promotion
boundary: local-only.** The eight consolidated gaps are taken from this tower's
`REVIEW.md` (C1–C8). Two sweepers fed this file: a GOVERNANCE-corpus sweep and an
EVIDENCE/ENGINEERING-corpus sweep; the parent already verified (P8) that the
load-bearing skill features cited below are real, so those are treated as
confirmed and the rest is marked `(unverified)` where a sweeper asserted a
capability without citing the skill mechanism.

## Master table — one best repo capability per gap

| Gap | Severity | Best repo capability (exact skill) | Verdict | Concrete adaptation for MTNG | Surfaced by |
|-----|----------|-------------------------------------|---------|------------------------------|-------------|
| **C1** value prop untested | blocker | `experiment` + `research-evidence-harness` | adapt | Freeze a `criterion.md` (one falsifiable hypothesis, non-goals, falsification condition + mechanical verdict rule, discrimination check) with baseline = flat summary+template; build the harness (dry-run fixtures, validator-recall metric calculator, evidence-status guard) to feed it; one live run renders SURVIVED/FALSIFIED/INVALID. See "contested lever" below. | both |
| **C2** Phase-0 integration unmapped | blocker | `architecture-pattern-inventory` | adapt | This *is* Phase 0: run the structure/layer/pattern/testing/observability mappers against the real ResonantOS repo to produce the integration mapping table + dependency rules, holding the "separate observed from recommended" discipline. If repo absent, the non-mutating gate forces the "declare standalone" fork instead. Author the result as the Context + Dependency-interface views (`invoke design`) as a one-page table. | both |
| **C3** mode detection unmeasured | major | `research-evidence-harness` | adapt | Pre-register the accuracy claim ("recall ≥ X on N labelled routing-signature fixtures", names/categories fixed before seeing data) and compute it with the reviewer-rubric/metric calculator over labelled fixtures (≥1 passing + ≥1 failing, stated threshold). Measure to **falsify**, not to bless substring detection (still `block` per BD-10). | both |
| **C4** recombination has no algorithm | major | `residuality-spec` | adapt | Run in audit mode on §17 to surface merge-under-failure stressors (required-node-unsatisfied, conflicting outputs, partial completion); Step 3 sets desired residue = emit-with-blocked-section; Step 5 yields a `conflicts[]` degradation-spec field. This produces the **degradation/residue spec**, not the merge predicate itself — the predicate is an `engineer-view` contract job. | both |
| **C5** engine authority undefined | major | `engineer-view` | borrow | Author the engine acceptance-policy as a `decision_inventory` (one verdict per stance, RESOLVED/OPEN/CRITICAL, cited authority); the contracts/enums lane pins `AuditEvent.actor_ref` to a closed enum that distinguishes engine-auto from human; the authority-on-every-verdict invariant forces the policy to name its source. Policy *content* (which threshold accepts) stays a `decision-gate` call. | both |
| **C6** apparatus over-scoped | minor | `implementation-layering` | adapt | Apply the value/cost layer-boundary heuristic to the 8 artifacts: L0 = the 3 kept (issue-packet + validator-report + audit-log) as the minimum-working-unit POC; defer contribution-records + OKF to a later layer gated on "a named consumer exists." The anti-pattern "calling a layer a POC while including production-scale concerns" *is* C6's diagnosis. Trimming is a planning verdict, not proof — loops back to C1. | evidence |
| **C7** per-signal overhead unbudgeted | minor | `research-evidence-harness` | adapt | Add a `RunProfile.budget` field to the run schema (positive integer, no unlimited default — `dispatch-spec` `token_budget` discipline); the harness's metric calculators measure per-signal cost against it. This is a schema field, not a cost model — the model itself is engineering. | both |
| **C8** node-schema drift / OKF | minor | `definitions-governance` | borrow | Make one canonical BranchNode the canonical source; run its drift audit (conflicting wording / stale anchors / undefined terms / narrative-redefining-authority / missing refs → remediation items with target files) to fix §14-vs-§22-vs-§23 drift; DomainSpec concept-registry dup/drift detection keyed by ID flags duplicates ("same ID, different type → flag, never auto-merge"). The OKF half stays unresolvable from the repo — needs the external spec. | governance |

Note on C8: the EVIDENCE sweep also reached C8 via `engineer-view`/`paired-views`
(one-home-per-term Invariant 1, name-once-decide-once Invariant 2) as a
*structural* enforcer. Both routes agree the repo can flag the drift; neither
chooses *which* schema is canonical — that is a `decision-gate` call. Single best
capability above is `definitions-governance` because it ships the drift-audit
enumeration directly.

## The contested lever — C1

The two sweepers disagreed on what is *primary* for C1, and the disagreement is
worth resolving cleanly rather than averaging.

- **GOVERNANCE stance (`experiment`):** freezing a criterion is
  necessary-but-not-sufficient, not primary. The primary work is a baseline
  strong enough to lose to plus a metric a flat summary could actually fail
  (validator recall on seeded-missing-info fixtures), which the discrimination
  check forces *before* the freeze. A frozen-but-weak criterion survives
  trivially and teaches nothing; the freeze makes the result *honest*, not
  *favorable*.
- **EVIDENCE stance (`research-evidence-harness`):** building the harness and
  measuring *is* primary; a frozen criterion is necessary-but-insufficient
  without something to measure. But the harness alone is equally hollow — its own
  guardrail forbids upgrading claims from synthetic fixture data, so a harness
  without a frozen criterion is just apparatus.

Both stances, read honestly, collapse to the **same ordered pair** — each just
named its own half as "primary." The reconciled recommendation:

1. **Freeze the criterion first** (`experiment`) — cheapest move. Author
   `criterion.md`: one falsifiable hypothesis (not two joined by "and"),
   non-goals, falsification condition + mechanical verdict rule, and a
   discrimination check stating what SURVIVED and what FALSIFIED each teach.
   Baseline = flat summary + template. Because a solo dev is both designer and
   skeptic, the 2-role P2 dispatch gate collapses to "write it down, then don't
   edit it" — keep the criterion artifact and its immutability, drop the
   dispatch ceremony.
2. **Build the harness to feed it** (`research-evidence-harness`) — seed N
   missing-info fixtures, implement the validator-recall metric calculator,
   wire the evidence-status guard. Dry-run on fixtures first; live second.
3. **Run once, live** — the single live run renders SURVIVED / FALSIFIED /
   INVALID against the frozen criterion. Until that run exists, **C1 stays a
   blocker** — neither freezing nor building, alone or together, discharges it.

The order matters because the cheap, irreversible-by-policy step (freeze) must
precede the expensive step (build), so the yardstick cannot be quietly bent to
fit whatever the harness happens to produce.

## Do this first — cheapest, highest-leverage reuse, in order

1. **Freeze C1's `criterion.md`** (`experiment`). Hours of writing; gates
   everything that claims value, and is the precondition for an honest C1 run.
2. **Pick the canonical BranchNode and run the drift audit** (C8,
   `definitions-governance`). Pure-text remediation list; removes the §14/§22/§23
   contradictions that make every later schema reference ambiguous.
3. **Author the engine-policy `decision_inventory` + pin `actor_ref` enum** (C5,
   `engineer-view`). Small table; unblocks the audit-trail meaning of every
   recorded engine action.
4. **Layer the 8 artifacts** (C6, `implementation-layering`). A planning verdict
   that shrinks the build surface to L0's three artifacts before any code.
5. **Build the C1 harness and run it once** (C3 reuses it; C7 adds the budget
   field) (`research-evidence-harness`). Most expensive; renders the C1 verdict
   and produces the C3 accuracy number and the C7 cost measurement in one pass.
6. **Map the integration surface** (C2, `architecture-pattern-inventory`) — only
   once the ResonantOS repo is in hand (see below).
7. **Residue-audit §17 for C4** (`residuality-spec`) — produces the
   degradation/`conflicts[]` spec that any later merge predicate must satisfy.

## Where repo reuse does NOT help

- **C2 when the repo is absent.** `architecture-pattern-inventory` requires the
  ResonantOS repo in hand; with no repo, no mapping is possible and the only
  honest path is the "declare standalone CLI" fork. The repo cannot supply the
  external codebase it would map.
- **C8, the OKF half.** The drift audit fixes the BranchNode schema, but the
  "OKF mis-named / unverified" sub-gap needs the external OKF/R-OKF spec fetched
  and pinned (consistent with BD-8). No repo capability substitutes for the
  missing spec.
- **C6 as a decision (not a sequence).** `implementation-layering` can *sequence*
  the artifacts L0→later, but whether the trimmed set is *sufficient* is a
  product-scope decision the repo does not make. The GOVERNANCE sweep found no
  governance skill that trims scope (the nearest, `distill`, is a transmutation,
  not a scope gate). Layering orders the build; it does not prove the trim
  correct — that loops back to the C1 harness.
- **C4/C5/C7 content vs. container.** The repo supplies *shapes*: the
  `conflicts[]`/residue spec (not the merge algorithm), the `decision_inventory`
  + enum (not which threshold accepts), the budget field (not the cost model).
  The classifier, the merge predicate, and the cost model are engineering, not
  governance or evidence artifacts.
- **The dispatch-tension skills are empty here.** `check-tension`, `anti-bias`
  (anti-bias-vector-composition), and `register-dispatch` govern multi-agent
  tension and fan-out. MTNG v1 is a single-dev, no-fan-out tool, so these
  address none of C1–C8 — there is no multi-agent dispatch to tension or record.
- **Already-blocked-on-own-merits items** (runtime-orchestrator BD-6,
  Branch-Pressure-Score BD-7) are not C1–C8 gaps and get no repo lift here.

## Closing note

This file is **advisory to MTNG**. It maps verified repository capabilities onto
the proposal's gaps so an external author could borrow the *shapes* that already
exist here. It **promotes nothing into Arcanum** — no Inventory entry, no
ontology node, no sigil, no canonical definition — and any such promotion would
require a separate governed decision. Where a sweeper asserted a capability
without citing the skill mechanism, the claim is marked `(unverified)`; none
load-bearing in this map were. `claim ≤ proof`: until MTNG runs the one live C1
experiment, C1 remains a blocker no matter how much apparatus is built.
