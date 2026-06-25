---
tags: [inventory, resonantos, living-archive, cav2, ontology-retrieval, semantic-search, rag, determinism, typed-intent, attenuation, viable-system-model, build-from-owned]
node_type: evidence-card
is_session: false
layer: architecture, governance
nature: reference
status: candidate
created: 2026-06-24
sources: [development/resonantos-integration/findings.md, development/resonantos-integration/research.md, development/machine-map/findings.md, "Agent Memory Architecture v7.1 (PDF)", development/cyberalchemy-integration-sdk/findings.md]
---

# Evidence Cards — resonantOS Integration + Ontology-over-RAG

Candidate Inventory read models. Promotion owners = cav2 authority owner / DomainSpec
(domainspec-v2) / the commercialization decision-gate. These cards promote nothing.

## `resonantos-living-archive-dogfood`

- ID: `resonantos-living-archive-dogfood`
- Status: candidate
- Claim or candidate: resonantOS is the **first dogfood host** for the CyberAlchemy SDK. Its
  **Living Archive** (substrate = Agent Memory Architecture v7.1) already owns the read
  substrate; CyberAlchemy layers governance on the WRITE seam. READ ports = `archive-read` /
  `memory-provider` (`living_archive_search`/`read`); WRITE/decision seam = `archive-intake-write`
  (intake-only) + Review Queue (`decide_review` approve/reject/escalate, `promote_review_artifact`).
  Map-vs-decision: substrate governs facts-over-time (OVERLAP, cav2 must not rebuild); no
  authority/decision/promotion field (ADDITIVE gap cav2 fills). Net-new = 4 atoms (provider body,
  port indirection, scope-tag shims, b1/b2 refactor); rest is build-from-owned. The trusted-write
  **provider body** is host-resident + absent from example code — cav2 implements it behind their
  owned `promote_review_artifact`/501 contract. Dogfood generates the data that builds the SDK.
- Source refs: `development/resonantos-integration/findings.md` (§2–§5); `research.md` (E1 code cites).
- Authority level: candidate synthesis (dispatch-verified; promotion provider UNBUILT).
- Promotion owner: cav2 authority owner / commercialization gate.
- Trace: closed dispatch `2026-06-24-resonantos-living-archive-integration` (resolved, 7 agents).
- Residue: provider body + scope-tag shims + port indirection + b1/b2 split all unbuilt.

## `ontology-traversal-over-vector-rag`

- ID: `ontology-traversal-over-vector-rag`
- Status: candidate
- Claim or candidate: "RAG work" splits into **grounding/entry** (where to start) vs
  **traversal** (what's related). The ontology **kills traversal** — deterministic typed graph
  navigation (exact label/property-index lookup + adjacency prefix-scan, no vectors) — and only
  **shrinks grounding**. It converts *search-by-similarity* into *navigation-by-structure*; cost
  scales with the **local neighborhood**, correctness comes from **declared edges**, not
  statistical luck. The PDF concedes the direction: USearch is a "semantic **entry point**," used
  only "if semantic entry needed"; the code profile resolves entry by symbol, often skipping
  vectors entirely.
- Source refs: "Agent Memory Architecture v7.1" (p.2–5 fast loop, label/property indexes);
  `development/resonantos-integration/research.md` (E2).
- Authority level: candidate synthesis (architecture inference; collapse-test below).
- Promotion owner: cav2 authority owner / DomainSpec.
- Trace: 2026-06-24 architecture discussion; grounded in the PDF retrieval design.
- Residue: COLLAPSE-TEST — false if the domain is un-modeled (no typed edges to traverse) or the
  query vocabulary is uncontrolled; then vectors are still needed to find the entry node.

## `ingest-time-cost-relocation`

- ID: `ingest-time-cost-relocation`
- Status: candidate
- Claim or candidate: the semantic/ML work is **not eliminated — it relocates from query-time to
  ingest-time.** The PDF runs neural models (GLiNER2/tree-sitter/Mamba/JEPA) **only in the slow
  loop** (extraction/encoding at write); the fast/read loop is "no LLM, sub-50ms" because
  comprehension was paid once at ingest and crystallized into typed edges. CyberAlchemy's
  engineering bet: pay the comprehension cost **once at governed write-time** so reads are cheap,
  exact, and governable. This is the real cost of the cheap-deterministic-read moat.
- Source refs: "Agent Memory Architecture v7.1" (p.1–2 two-loop, p.6 slow-loop ingestion).
- Authority level: candidate synthesis.
- Promotion owner: commercialization decision-gate.
- Trace: 2026-06-24 architecture discussion.
- Residue: the write-time extraction + ontology-maintenance burden is real and un-costed.

## `governance-requires-determinism`

- ID: `governance-requires-determinism`
- Status: candidate — **REVISED/DEMOTED 2026-06-24** by the deterministic-retrieval-thesis dispatch
  (see card [`determinism-is-cost-not-requirement`](2026-06-24-deterministic-retrieval-thesis-cards.md)).
  ⚠️ **The strong claim below ("determinism-at-read is a precondition for authority-at-read") is
  OVER-CLAIMED and superseded.** Corrected position: the requirement is **provenance + a stable
  citable referent** (auditors attest non-deterministic processes routinely); determinism is a
  **cost-dominance optimization** (collapses the attestation surface to ~0), NOT a logical necessity.
  The original claim is retained verbatim below as the captured-but-corrected record.
- Claim or candidate (ORIGINAL, now corrected): the deepest reason to drop read-time semantic search is **governance, not
  efficiency**: you **cannot attest, authorize, or promote a cosine similarity** (fuzzy,
  non-reproducible); a typed edge with provenance IS governable. So **determinism-at-read is a
  precondition for authority-at-read** — "drop semantic search" and cav2 (manufacture authority)
  are the same move. VSM placement: the Agent Memory Architecture is a strong **S2+S4 substrate
  missing S5** (supersession is model-driven, not authority-grounded); **cav2 = the missing S5**,
  and it must sit on the **ontology/graph** (deterministic) not on **vectors** (fuzzy). Ontology
  = the regulator's model (Conant-Ashby); ontology-traversal vs vector-RAG = **structural vs
  statistical attenuation**.
- Source refs: `development/machine-map/findings.md` (S5-missing, Conant-Ashby, requisite variety);
  `development/resonantos-integration/research.md` (E2 fact-vs-authority partition);
  `development/deterministic-retrieval-thesis/findings.md` (§2 Leg 3, §4 A1(c) — the correction).
- Authority level: candidate principle, **CORRECTED** (the cav2=missing-S5 and structural-vs-statistical
  -attenuation parts survive; the "determinism is a precondition" part is demoted to cost-dominance).
- Promotion owner: cav2 authority owner (AUTHORITY-MODEL).
- Trace: 2026-06-24 architecture discussion; demoted 2026-06-24 by deterministic-retrieval-thesis (Lane-A A1(c) + Z3 self-withdrawal).
- Residue: route the CORRECTED principle (recorded gate over a citable referent; determinism = cost) to cav2 authority.

## `typed-intent-discrete-vector`

- ID: `typed-intent-discrete-vector`
- Status: candidate — **REFINED 2026-06-24** by the deterministic-retrieval-thesis dispatch (see card
  [`typed-intent-seed-owned-but-unexecuted`](2026-06-24-deterministic-retrieval-thesis-cards.md)).
  Two corrections: (1) precedent is now **CONFIRMED** — owned by the spec-ontology-unification tower
  (`SEED.md:16-27`) — **but build-from-owned ≠ build-from-proven**: the tower is "not yet executed"
  (`SEED.md:1-6`) and the 1:1 node→pattern assumption is its own open residue (`SEED.md:68`); (2)
  "shrinks the grounding margin toward zero" is over-stated → corrected to **reduce-not-eliminate, to
  a thin governable margin** (discreteness holds only under a node-contract boundary; else closure
  re-inflates to whole-graph RAG).
- Claim or candidate (ORIGINAL, now refined): **DomainSpec (typed intent) shrinks the grounding margin toward zero** by
  delivering each agent a "discrete vector" start point — the query arrives **already-typed**, so
  the residual semantic grounding step collapses. This is the owner's long-held intuition for why
  context-injection / RAG handling is *not* needed in CyberAlchemy: DomainSpec is **already
  linked**, so every agent has a clear discrete start point. Owned by DomainSpec; relates to
  `projects/domainspec-v2/` research + the DomainSpec language (cite, do not redefine).
- Source refs: `projects/domainspec-v2/research/spec-ontology-unification/SEED.md` (:1-6, :16-27, :68);
  `development/deterministic-retrieval-thesis/findings.md` (§2 Leg 1, §4 A2).
- Authority level: candidate (owner = DomainSpec; **precedent CONFIRMED, but owner UNEXECUTED**).
- Promotion owner: DomainSpec (domainspec-v2 research).
- Trace: owner intuition surfaced 2026-06-24; precedent CONFIRMED + refined 2026-06-24 by deterministic-retrieval-thesis.
- Residue: the convert-to-proven move = **execute the spec-ontology-unification tower** (prove the 1:1 condition); contract-completeness unproven.
