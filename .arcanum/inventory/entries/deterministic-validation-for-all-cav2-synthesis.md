---
tags: [inventory, cav2, authority, determinism, non-collapse, build-from-owned, synthesis]
node_type: synthesis
is_session: false
layer: architecture, governance
nature: explanatory, reference
status: candidate
created: 2026-06-26
boundary: INTERNAL — moat-adjacent (determinism = attestation moat); do NOT copy into public arcanum/
sources:
  - .arcanum/inventory/entries/cav2-authority-and-determinism-synthesis.md
  - cyberAlchemy-v2/disciplines/development/2026-06-26-build-from-owned-validator-HANDOFF.md
  - cyberAlchemy-v2/ontology/promotion-requests/2026-06-23-authority-object-schema-proposal.md
  - cyberAlchemy-v2/authority/AUTHORITY-MODEL.md
---

# Building Deterministic Validation for *All* of CAV2 — the build plan + why it matters

Candidate Inventory synthesis (**promotes nothing**; owners = sigil-development/tools + definitions/
constitution-governance). **Build-from-owned** extension of [[cav2-authority-and-determinism-synthesis]]
(which says *how determinism works*); this entry adds *how we build the validation layer across the
whole corpus*. Claim ≤ proof: **intended, not shipped** — zero validators exist today.

## The one idea
**Every governance rule in CAV2 reduces to the same shape: an SMT query over schema-typed records.**
Once each authority object is a *typed record* (not prose), "are these two distinct?", "is this kind
allowed?", "does an owner already exist?" become **decidable queries returning yes/no + a counter-witness.**

## Step 0 — the foundation that gates everything (OQ-1 / `G2`)
No deterministic check works until the corpus is **typed**: every authority object declares
`instantiates: concept.<kind>`, `specializes: <id>`, owner, status, axes. That typed record **is** the
machine input. This is why "organize the corpus first" (the instantiation chain) is the **precondition**,
not a detour.

> Worked example. "Is `D-candidate` really distinct from `D43`?" → both are records with axes → the
> adapter asks `∃ axis. cand.axis ≠ D43.axis`; if none exists it returns the **collapsing pair** as proof.

## Architecture — one adapter, a family of checks
- **One shared SMT adapter** loads the typed corpus and answers queries. The needed fragment
  (equality/datatypes, `∃` over a finite set — EPR/finite-domain) is **decidable**.
- **Each rule = a query family** on that adapter. Three specced siblings:
  1. **non-collapse** (`CAV2-D29`) — prove two declared objects differ on a real axis.
  2. **closure** (`CAV2-D49`) — default-deny: every `instantiates` must hit an enumerated kind.
  3. **build-from-owned** (`CAV2-C17`) — search the corpus for an owner the candidate coincides-with/specializes.
- **Generalizes:** each AUTHORITY-MODEL non-collapse rule, each `forbidden_collapse`, each
  axis-orthogonality claim → another query. "All of CAV2" = the rule-set, each compiled to a query.

## Migration path — per-rule, not big-bang
Each rule walks `review → mixed → validator`, tracked by its `validation_mode` field. A rule moves to
`validator` **only when the schema fields its query needs have stabilized.** The catalog shows which
rules are review vs validator → coverage is visible, never silently claimed.

## The honest boundary (deterministic core + review shell)
SMT decides *given an encoding*. Two things stay review **permanently**:
1. **The encoding choice** — which axes to type (the machine checks distinctness; it doesn't choose axes).
2. **Absolute non-thinness** — "really structural or a thin re-skin?" = the **count-collapse frontier**
   (Lean). The SMT non-thinness witness is the **FOL shadow of `functorial_strictly_dominates_count`**;
   it gives the *relative* answer, the *absolute* one stays human. Every validator declares its boundary.

## Why it matters
- **Collapses the attestation surface toward ~0** — the moat (attestation + governance-data); a
  deterministic verdict is cheap, repeatable, explainable proof. (Provability/Lean = amplifier, not moat.)
- **Catches drift/collapse/redundancy every time, before authoring** — not "sometimes, on a later sweep."
- **Scales governance past human review** (requisite variety / governance-attenuation).
- **Turns the mold into a machine** — CAV2 self-validating its own authority moves (bounded by `CAV2-D30`).
- **Counters LLM nondeterminism** — stable, reproducible verdicts over frozen typed referents.

## Build order
1. stabilize the authority-object schema (`G2` instantiation chain) → clears OQ-1;
2. build the one shared SMT adapter;
3. implement the 3 sibling query families;
4. migrate rules `review → validator`, one at a time, tracked in the catalog;
5. wire as pre-authoring gates into definitions / constitution / promotion routes.

## Residue
- OQ-1 (schema stability) gates all of it; absolute non-thinness stays the review frontier; intended-not-shipped.

## Boundary
Inventory candidate read-model. Promotes nothing. Owners: sigil-development/tools (build) +
definitions/constitution-governance (the rules). INTERNAL — moat-adjacent.
