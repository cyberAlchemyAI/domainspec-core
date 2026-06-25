---
tags: [inventory, cyberalchemy-v2, authority-model, ontology, governed-artifact, meta-authority, b-op-branch, non-collapse, map-vs-decision, governance-vs-ontology, claim-le-proof]
node_type: evidence-card
is_session: false
layer: governance
nature: reference
status: candidate
created: 2026-06-24
sources: [cyberAlchemy-v2/authority/AUTHORITY-MODEL.md, cyberAlchemy-v2/authority/definitions/DEFINITIONS-INDEX.md, projects/ontologize/operational-ontology/branch/operational-node.schema.yml, .arcanum/inventory/entries/evidence-cards/2026-06-23-governed-artifact-primitive-formalization-cards.md, projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md, .arcanum/spells/ergonomics-affordance-lifecycle/README.md]
---

# Evidence Cards — Authority, Ontology, and Governed Artifacts

Candidate Inventory read models from a conceptual synthesis (not a dispatch),
grounded in cav2's authority model + definitions + the B-op node schema. Promotion
owner = cav2 authority owner / definitions-governance. These cards promote nothing.

## `authority-is-permission-by-owner-route`

- ID: `authority-is-permission-by-owner-route`
- Status: candidate
- Claim or candidate: authority (`CAV2-D34`) is "who or what is allowed to make
  something *count*, and only for which purpose" — a **permission attached to an
  owner + scope**, not a property a thing has. Load-bearing rule: "authority moves
  by **owner route**, not by proximity, usefulness, or repetition." Authority is the
  DECISION layer.
- Source refs: `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md` §Authority Rule;
  `CAV2-D34` (DEFINITIONS-INDEX).
- Authority level: candidate (cites canonical definitions).
- Promotion owner: cav2 authority owner.
- Trace: conceptual synthesis 2026-06-24.
- Residue: enforcement is review-mode (OQ-1 open).

## `ontology-models-authority-cannot-decide-it`

- ID: `ontology-models-authority-cannot-decide-it`
- Status: candidate
- Claim or candidate: the authority↔ontology relation is one Non-Collapse rule —
  "**Ontology can model authority, but it cannot decide authority**"
  (AUTHORITY-MODEL §Non-Collapse rule 2). Ontology is the MAP (typed nodes/edges
  describing what is + how it relates); it can contain authority as content
  (governed_by edges, status, authority_level) but cannot perform the owner
  decision. In the authority-kind table ontology is the `Projection` kind (ontology
  route + source owner) which "must not collapse into a promotion decision." The
  direction is one-way: **authority governs ontology, not the reverse.**
- Source refs: `AUTHORITY-MODEL.md` §Non-Collapse rule 2 + §Authority Kinds
  (`Projection` row); `projects/ontologize/operational-ontology/branch/operational-node.schema.yml:8`
  ("this schema assigns no promotion authority" — the rule baked into the schema).
- Authority level: candidate.
- Promotion owner: cav2 authority owner / ontology-harness.
- Trace: conceptual synthesis; the B-op schema's self-denial of promotion authority is the witness.
- Residue: none material.

## `governed-artifact-is-the-vehicle-not-a-primitive`

- ID: `governed-artifact-is-the-vehicle-not-a-primitive`
- Status: candidate
- Claim or candidate: "governed artifact" is NOT a primitive (typed negative, per
  the 2026-06-23 governed-artifact-primitive-formalization finding) — there is just
  `artifact` + the authority model wrapped around it. "Governed" is a
  posture/relationship (routed through an owner gate), not a substance. A governed
  artifact is the UNIT authority acts on and the JOINT where ontology and authority
  meet: it is a node in the map (describable) AND an authority-bearing object that
  only COUNTS once an owner gate clears it AND only if its KIND is an enumerated row
  (`CAV2-D49` default-deny). It carries kind + provenance (`D35`) + traceability
  (`D36`) + posture + gate state.
- Source refs: `.arcanum/inventory/entries/evidence-cards/2026-06-23-governed-artifact-primitive-formalization-cards.md`
  (`governed-artifact-primitive-typed-negative`); `AUTHORITY-MODEL.md` §Authority
  Kinds + §Authority Postures; `CAV2-D34/D35/D36/D49`.
- Authority level: candidate.
- Promotion owner: definitions-governance (for the base term `artifact`).
- Trace: conceptual synthesis + prior typed-negative finding.
- Residue: whether the base term `artifact` passes `CAV2-D31` is an open definitions-governance review.

## `cav2-is-reflexive-meta-authority-mold`

- ID: `cav2-is-reflexive-meta-authority-mold`
- Status: candidate
- Claim or candidate: CAV2 is a **system/meta authority** — authority-about-authority.
  It decides no domain facts; it decides how anything BECOMES authority: the kinds
  (`D49`), the promotion lifecycle (`D48` — "the single staged path by which any
  authority-bearing candidate acquires authority"), the owner routes, the gates
  (`D37`). `D41` defines it as "the traffic map for what is allowed to count, who can
  make it count, and what it must not be confused with." Layering: **system/meta
  authority (CAV2 + Arcanum method) = the MOLD; a domain authority = the CASTING**
  (a client's governed ontology; ontologize's BI governance; our ergonomics
  coordinate-model + admission gate). CAV2 is reflexive — it governs itself too
  (the operational-ontology B-op branch = CAV2 modelling its own operations as a
  domain). This is the CyberAlchemy/ontologize product thesis: ontologize SELLS
  castings (installs a domain authority manufactured with the CAV2 method).
- Source refs: `AUTHORITY-MODEL.md` (Core Flow, kinds, postures);
  `CAV2-D41/D48/D49/D37` (DEFINITIONS-INDEX); `projects/ontologize/PRODUCT.md`.
- Authority level: candidate synthesis.
- Promotion owner: cav2 authority owner.
- Trace: conceptual synthesis answering "is CAV2 a meta-authority?".
- Residue: meta-authority in METHOD/POSTURE, not yet ENFORCEMENT — review-mode (OQ-1 kind-enumeration not validator-backed; OQ-2 invariant/axiom not first-class). The mold works; it is hand-operated, not yet a machine.

## `b-op-encodes-non-collapse-and-the-map-decision-split`

- ID: `b-op-encodes-non-collapse-and-the-map-decision-split`
- Status: candidate
- Claim or candidate: in the B-op schema, authority/ontology/governed-artifact are
  distinct: a **governed artifact = a typed node** (operational_discipline/decision/
  policy/constitution/axiom/capability/route); **ontology = the whole node+edge
  graph** (the map); **authority = the promotion act** (status candidate→premise→
  promoted, authority_level L0-L7) fired by the owner gate (ontology-harness accept +
  Constitution Governance apex), plus the `governed_by` edge that binds once promoted.
  Mapped onto the ergonomics harness: MAP = the 7 coordinate axes + placement table +
  backlog descriptions + dialectic findings; DECISION = the admission gate + owner
  routes + default-deny + restraint floor + the status transitions; VEHICLE = the
  affordance-lifecycle spell. The harness is **mostly decision + a thin taxonomy-map,
  no typed-graph ontology** — which is why "governance-yes / ontology-no". Bridge:
  re-encode the discipline/decisions/lessons/spell as B-op nodes to gain a real ontology.
- Source refs: `projects/ontologize/operational-ontology/branch/operational-node.schema.yml`
  (node_type enum, edge enum, status ladder, line 8 no-promotion-authority);
  `projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md` (coordinate model);
  `.arcanum/spells/ergonomics-affordance-lifecycle/README.md`.
- Authority level: candidate synthesis.
- Promotion owner: operational-ontology branch owner / ontology-harness.
- Trace: deliverables A (node/edge picture) + B (map vs decision) 2026-06-24.
- Residue: the bridge (artifacts → B-op nodes) is not executed; B-op is candidate pending ontology-harness acceptance.
