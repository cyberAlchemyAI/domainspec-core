# DomainSpec Lean Formalization Next Route Handoff

Date: 2026-06-01
Source dispatch: `domainspec-lean-formalization-research-20260601`

## Recommended Next Route

Run a current-truth refresh before editing research claims or promoting relation language.

Objective:

Refresh `domainspec-lean-formalization` status claims so root docs distinguish:

- total files
- default targets
- declared libraries
- build status
- active `sorry` status
- axiom status
- PR-ready status
- documented research status
- conjectural/open status
- analogy/bridge status

## Why This Comes First

The research route found useful but stale front-door claims:

- Root Lean file counts disagree across docs and local tree.
- `files/new` count and PR-ready count are conflated.
- Some docs say zero `sorry`, but strict local text scan found active sorries.
- Build validation was blocked by toolchain/Mathlib fetch/ref-lock issues.
- Bridge docs contain powerful "same object/isomorphism" language that later qualifies itself.

Until these are refreshed, every downstream relation map or publication edit risks inheriting stale status.

## Suggested Work Units

### W0: Build Environment Repair

Repair Lake/Mathlib state enough to run focused builds without mutating source unexpectedly.

Validation:

- `lake build Bicyclic`
- `lake build Tier1PrizeStatement`
- focused build for `files/new` default targets

Blocked condition:

- repeated Mathlib Git ref-lock or toolchain fetch failure after cleanup.

### W1: Mechanical Inventory Refresh

Generate a machine-backed inventory:

- root top-level Lean files
- nested Lean files
- `files/new` Lean files
- default targets
- declared libraries
- active standalone `sorry` lines
- axioms
- imports and dependency cones for headline files

Validation:

- compare generated counts against `README`, `LEAN-ARCHITECTURE`, `LEAN-TYPES`, `LEAN-TAXONOMY`, and `files/new/README.md`.

### W2: Status Taxonomy Patch

Define canonical status labels:

- theorem-source
- build-evidenced
- sorry-free
- axiom-free
- PR-ready
- documented audit
- conjectural
- analogy
- refuted
- demoted

Validation:

- each front-door claim maps to exactly one label or is rewritten.

### W3: Root Docs Refresh

Patch only status/count/readiness claims. Avoid changing theorem content.

Candidate docs:

- `README.md`
- `LEAN-ARCHITECTURE.md`
- `LEAN-TYPES.md`
- `LEAN-TAXONOMY.md`
- `lean-formalization/files/new/README.md`

Validation:

- no broad "all Lean sorry-free" claim unless mechanically true.
- no "PR-ready" label for declared libraries with active `sorry`.
- thermodynamics stays finite/discrete unless the continuous theorem is supplied.

### W4: Relation Map Deep Pass

After current-truth refresh, map sibling repositories and project snapshots.

Output:

- graph of relation type, owner, evidence path, confidence, and promotion risk.

Validation:

- no candidate relation promoted to canonical ontology or implementation dependency without owner review.

## Handoff Artifacts From This Route

- `ops/development/domainspec-lean-formalization-fanout-receipts.md`
- `ops/development/domainspec-lean-formalization-relation-ledger.md`
- `ops/development/domainspec-lean-formalization-claim-discipline-ledger.md`
- `ops/development/domainspec-lean-formalization-interpretation-tournament.md`
- `ops/development/domainspec-lean-formalization-research-brief.md`
- `ops/development/domainspec-lean-formalization-validation-ledger.md`

## Stop Condition

Stop before mutating theorem/proof source. This handoff authorizes status refresh planning and evidence-gathering only, not proof edits or canonical ontology promotion.
