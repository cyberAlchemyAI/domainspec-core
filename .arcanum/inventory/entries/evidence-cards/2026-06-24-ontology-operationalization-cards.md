---
tags: [inventory, machine-map, viable-system-model, cav2, non-collapse, map-vs-decision, observer-executor-split, write-authority-proviso, leverage-point, two-ontologies, regulator-self-model, b-op-branch, domainspec-language, build-from-owned, claim-le-proof, evidence-card]
node_type: evidence-card
is_session: false
layer: architecture, governance
nature: reference
status: candidate
created: 2026-06-24
sources: [development/machine-map/research/2026-06-24-ontology-operationalization/findings.md, development/machine-map/research/2026-06-24-ontology-operationalization/research.md, cyberAlchemy-v2/authority/AUTHORITY-MODEL.md, development/machine-map/findings.md, implementation/domainspec/ADLC-ALIGNMENT.md, implementation/domainspec/RELATIONSHIPS.md, cyberAlchemy-v2/development/research/2026-06-24-ontology-engineering-precedent/findings.md]
---

# Evidence Cards — Operationalizing Ontology in the Machine

Candidate Inventory read models from dispatch `2026-06-24-ontology-operationalization-in-the-machine`
(research; 4 explorers + 2 skeptics; closed `resolved`; both skeptics accepted). Promotion owners =
the DomainSpec plan owner / cav2 authority owner / the commercialization decision-gate. These cards
promote nothing.

## `operationalization-is-build-from-owned`

- ID: `operationalization-is-build-from-owned`
- Status: candidate
- Claim or candidate: operationalizing ontology is **not a build problem — it is finishing +
  wiring of already-owned pieces**. The read-only observer/meter already exists in code
  (`tools/run-async-observer.ts`, `run-fast-observer.ts`, `governance-attenuation-audit.ts`;
  "built, under-performing"); the Edge Law exists in RELATIONSHIPS.md (`validate-relationships.ts`
  checks *label* canonicity, not endpoint-pairs); the binding tools (`validate-orphans.ts`,
  `generate-registry.ts`) exist; the build steps are owned (machine-map §3).
- Source refs: `.../findings.md` §3 + §4; Meadows skeptic return (precedent sweep of
  `implementation/domainspec/tools/`); `implementation/domainspec/ADLC-ALIGNMENT.md` (G11/T8-T10).
- Authority level: candidate synthesis (build-from-owned; field owners also exist — TopBraid EDG, OntoClean, SHACL, GRADE per the precedent findings).
- Promotion owner: DomainSpec plan owner.
- Trace: Meadows precedent gate, verified by reading the `tools/` files.
- Residue: the validator checks labels not endpoint-pairs — the net-new is narrow (endpoint typing).

## `write-authority-proviso-architectural-absence`

- ID: `write-authority-proviso-architectural-absence`
- Status: candidate
- Claim or candidate: the **single invariant** that keeps every operationalization option sound is
  that **no modeling operation may hold a write-edge to a node's `promotion-status`/authority**.
  Every collapse mode (auto-promoting sensor, canonical bidirectional binding, merged "v2"
  ontology, relocated self-model) reduces to that one re-fusion. Soundness must be an
  **architectural absence** of the write-channel, not a relaxable policy
  (`AUTHORITY-MODEL.md:23-25`: "authority moves by owner route, not by proximity").
- Source refs: `.../findings.md` §2; Ashby skeptic return; `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md`
  Non-Collapse rule 2; the "write-authority proviso" from the precedent findings.
- Authority level: candidate (definitional-soundness gate; the load-bearing invariant).
- Promotion owner: cav2 authority owner.
- Trace: Ashby gate — the one re-fusion underneath all collapses.
- Residue: the proviso is UNVERIFIED in code — no path-audit has confirmed no modeling edit writes promotion-status.

## `two-ontologies-language-vs-authority-no-merge`

- ID: `two-ontologies-language-vs-authority-no-merge`
- Status: candidate
- Claim or candidate: the machine carries **two structurally independent ontologies**. **Ontology
  A** = the DomainSpec language schema (L1: 25 meta-types + ~29 typed edges + the Edge Law in
  RELATIONSHIPS.md — already schema-level). **Ontology B** = cav2's authority ontology (9 kinds +
  promotion DAG — not L1). The type-checker is the Edge Law in A; **B must NOT become the
  type-checker**. They ALIGN at code-concept binding (Δ: L1→L2, ADLC v1.9 G11/T8-T10), they do not
  merge. "domainspec-v2" = cav2 governance over schema A + ADLC enforcement of A — earned on
  evidence, never a merged ontology.
- Source refs: `.../research.md` (Lambek return); `.../findings.md` §3/§5;
  `implementation/domainspec/RELATIONSHIPS.md`; `domainspec-lean-formalization/docs/domainspec-two-layer-framework.md`.
- Authority level: candidate (Lambek; verified against the L1/L2/Δ two-layer framework).
- Promotion owner: DomainSpec plan owner / cav2 authority owner.
- Trace: Lambek language-layer explorer; Ashby confirmed merge = collapse.
- Residue: relates `category-theory-domainspec-language-synthesis` (the L1/L2/Δ model) and `domainspec-v2`.

## `leverage-point-finish-the-built-observer`

- ID: `leverage-point-finish-the-built-observer`
- Status: candidate
- Claim or candidate: the **single highest-leverage act** is to **finish + baseline the already-built
  read-only observer** — on Meadows' leverage ladder it is the *missing information-feedback loop*
  (the highest structural leverage short of rules/goals/paradigm); it "makes the rest falsifiable".
  Corrections: (d) reconcile-spine is a **precondition, not a lever**; (g) "domainspec-v2" naming
  without structural change is **anti-leverage**.
- Source refs: `.../findings.md` §4; Meadows skeptic return (leverage ranking);
  `development/machine-map/findings.md` §3 (the meta-metric gap, observer "built, under-performing").
- Authority level: candidate (Meadows leverage gate).
- Promotion owner: DomainSpec plan owner.
- Trace: Meadows leverage ladder, re-ranked from the draft's (d)→(a) to (a)-first-as-finish.
- Residue: sequence (reconcile-first vs meter-first) is an owner's call depending on cycle scope.

## `schema-drift-eliminable-instance-drift-not`

- ID: `schema-drift-eliminable-instance-drift-not`
- Status: candidate
- Claim or candidate: a v2 type-system change can make **schema-level drift unconstructible** — if
  the registry validator enforces the Edge Law's typed endpoint-pairs, a wrong-meta-type edge (e.g.
  Entity `enforces` Operation) is *structurally rejected* at registration ("well-typed = can't-drift").
  **Instance-level drift CANNOT** be type-eliminated — even a faithful schema functor leaves the
  runtime round-trip able to fail; "the audit is permanently double" (needs behavioral contracts /
  test derivation).
- Source refs: `.../research.md` (Lambek Q3); `domainspec-lean-formalization/docs/domainspec-two-layer-framework.md` §3.6/§5; `implementation/domainspec/RELATIONSHIPS.md` (Edge Law).
- Authority level: candidate (Lambek; grounded in the two-layer framework's schema-vs-instance independence).
- Promotion owner: DomainSpec plan owner.
- Trace: Lambek Q3; Ashby confirmed the validator stays Ontology-A-only (no promotion-status column).
- Residue: endpoint typing of the validator is the narrow net-new build.

## `review-time-not-run-time-regulator-decay`

- ID: `review-time-not-run-time-regulator-decay`
- Status: candidate
- Claim or candidate: a running operational ontology is **correct at review-time, not run-time** —
  `drift-flagged` is a **manual** sensor (no background process; OQ-1), `drift_owner`/`drift_route`
  have no enforced update cycle. Two opposite vectors run on the same ontology: the **archive
  hardens** (append-only ledger D26, promoted definitions, residue D18, challenge contracts D40)
  while the **live regulator-model drifts** — a fidelity risk for the *whole* control loop (a stale
  S5 model tells cav2 it regulates a system that no longer matches reality).
- Source refs: `.../research.md` (Forrester return); `cyberAlchemy-v2/ontology/NODE-MODEL.md`,
  `LIFECYCLE-MODEL.md`, `PACKAGE-MODEL.md`; `cyberAlchemy-v2/authority/DEFINITION-DRIFT-AUDIT.md`.
- Authority level: candidate (Forrester operational-dynamics explorer).
- Promotion owner: cav2 authority owner (per-kind drift routes; no cross-cutting maintenance owner exists).
- Trace: Forrester; reserves the Conant-Ashby re-fusion verdict to Ashby.
- Residue: maintenance scales linearly with promoted artifacts; review bandwidth does not (OQ-1).

## `cav2-relocation-default-deny`

- ID: `cav2-relocation-default-deny`
- Status: candidate
- Claim or candidate: relocating the machine-map / the ontology-regulator MODEL **inside cav2** is
  **DEFAULT-DENY** until two proofs land: (1) cav2 **is** DomainSpec's S5 (today this is *analogy,
  not a cited link*, machine-map §1) AND (2) the contained self-model is proven **write-incapable**.
  Otherwise the regulator (S5-outer) re-fuses with the regulated object system (Conant-Ashby
  violation), and a self-model that can write cav2's own promotion-status is the map deciding its
  own authority. Co-locating with machine-map (current placement) is the sound default.
- Source refs: `.../findings.md` §5; Ashby skeptic return; `development/machine-map/findings.md` §1
  (cav2=S5 = analogy); `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md` (Non-Collapse).
- Authority level: candidate (Ashby definitional-soundness gate; the deepest target).
- Promotion owner: cav2 authority owner (the relocation is an owner decision, gated on the two proofs).
- Trace: user-raised relocation hunch → Ashby Conant-Ashby self-model analysis.
- Residue: this is the Conant-Ashby self-modeling question in concrete form; both proofs are open.
