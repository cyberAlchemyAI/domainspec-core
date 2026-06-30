---
tags: [inventory, cav2, authority, determinism, constitution-governance, build-from-owned, formalization, synthesis]
node_type: synthesis
is_session: false
layer: architecture, governance
nature: explanatory, reference
status: candidate
created: 2026-06-28
boundary: INTERNAL — moat-adjacent (determinism = attestation moat); do NOT copy into public arcanum/
dispatch_id: 2026-06-28-constitution-fol-validation-path
dispatch_type: research
working_folder: cyberAlchemy-v2/development/research/2026-06-28-constitution-fol-validation-path/
sources:
  - cyberAlchemy-v2/development/research/2026-06-28-constitution-fol-validation-path/findings.md
  - .arcanum/inventory/entries/deterministic-validation-for-all-cav2-synthesis.md
  - cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md
  - implementation/domainspec/AXIOMS.md
---

# FOL constitution-validation is a bounded COMPLEMENT — the cross-rule (Row-2) residue

Candidate Inventory synthesis (**promotes nothing**; owners = sigil-development/tools +
definitions/constitution-governance). **Build-from-owned refinement** of
[[deterministic-validation-for-all-cav2-synthesis]] (which already says "every rule = an SMT
query over typed records" and that "the SMT non-thinness witness is the FOL shadow of
`functorial_strictly_dominates_count`"). Claim ≤ proof: **intended, not shipped.**

## What this sharpens (vs the existing deterministic-validation entry)
The existing entry treats validation as one register ("every rule = SMT query"). The
`agent ⊨ spec` register analysis (kodamai dispatch) sharpens it into **three fibres**, only one
of which is the open prize:
- **Row 1 — per-rule `r ⊨ rule`**: already owned in Lean (`AgentPermissionKernel.Satisfies` is a
  FOL formula; `decidePolicy_sound` its sound-complete decider). FOL here is a **RELABEL** — do
  not build it.
- **Row 2 — cross-rule** (consistency / contradiction / `∃ state . state ⊨ whole-constitution`):
  the **genuine open residue.** Proof-theoretically non-distributive — a contradiction is the
  *absence of a common state*, which a per-rule `∀ rule . lint` sweep cannot even state.
- **Row 3 — residue/behavior gluing**: categorical, FOL **provably blind** (`count_blind_agrees`).
  Stays in the Lean spine. (This is the existing entry's "FOL shadow of functorial" line, now named.)

## The witness (why Row 2 is real, not a relabel)
Hand-built + hand-run (Gödel/S2): three CAV2-C nodes each individually lint-clean, joined by a
`governs` cycle C2→C13→C4→C2. The per-rule closure-validator (C-1..C-3 = unary `(kind,location)`
lints) passes **ALL**; a cross-rule `reach(X,X)` catches the cycle. The per-rule lints provably
cannot express **acyclicity** (a transitive-closure property) — **and CAV2-C13
(STABLE-REPOSITORY-CONSTITUTION lines 247–271) already mandates that acyclicity.** So today we
cannot enforce a rule our own constitution requires. Does not collapse to `decidePolicy`.

## Register verdict: COMPLEMENT, not fork, not subsume
FOL/formal-methods is a **complement** to the categorical `agent ⊨ spec` prize
([[kodamai-smithe-correctness-layer-synthesis]]): FOL owns the discrete governance layer (Row 2),
categorical owns the residue/behavior layer (Row 3). Tightest tool = **Cedar** (decidable +
**Lean-verified**, arXiv:2403.04651 — shares the spine's trust base, so it does NOT fork the
foundation); Datalog/PCAS-FORGE (arXiv:2602.16708) = the end-to-end blueprint; Alloy for first
counterexamples. (Refines the existing entry's generic "one shared SMT adapter".)

## Buildable first step + the narrow open residue
1. Formalize the witness — governs-acyclicity + CAV2-C13 cross-rule check — in Cedar/Datalog
   (transitive closure over `governs` edges + the reviewed-exception). It immediately enforces a
   rule our constitution already mandates and catches a defect the per-rule validator misses.
2. The only genuinely precedent-thin residue: **encode the six governance axioms A1–A6
   (`implementation/domainspec/AXIOMS.md`) as formulae** so `axiom ⊨ rule` is checkable. Today the
   AXIOMS→CONSTITUTION "Derivation Chain" is prose attribution ("a default pattern, not a law") —
   not a logical object yet. **Collapse-test:** vacuous if the axiom is merely the rule restated
   (needs a non-`rfl`/non-trivial derivation); the *checking* is owned-by-classical FOL entailment.

## Residue
- Row-2 build-from-owned on Cedar/Datalog; the A1–A6 encoding is the one novel-attempt and carries
  its collapse-test; absolute non-thinness stays the categorical (Row-3) review frontier;
  intended-not-shipped.

## Boundary
Inventory candidate read-model. Promotes nothing. Owners: sigil-development/tools (build) +
definitions/constitution-governance (the rules). INTERNAL — moat-adjacent.
