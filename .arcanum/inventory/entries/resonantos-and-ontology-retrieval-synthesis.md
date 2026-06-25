---
tags: [inventory, resonantos, living-archive, cav2, integration, ontology-retrieval, semantic-search, rag, determinism, typed-intent, attenuation, viable-system-model, synthesis]
node_type: synthesis
is_session: false
layer: architecture, governance
nature: reference
status: candidate
created: 2026-06-24
sources:
  - development/resonantos-integration/findings.md
  - development/resonantos-integration/RESONANTOS-INTEGRATION-GUIDE.md
  - development/resonantos-integration/research.md
  - development/machine-map/findings.md
  - "Agent Memory Architecture v7.1 (PDF, Victor Morrow)"
  - development/cyberalchemy-integration-sdk/findings.md
---

# resonantOS Integration + Ontology-over-RAG — Synthesis

Candidate Inventory synthesis (not canonical). Captures two tightly-linked results from
the 2026-06-24 iterations: (1) the **resonantOS Living Archive integration** (first dogfood
host for the CyberAlchemy SDK), and (2) the **ontology-over-semantic-search** architecture
insight it surfaced. Evidence:
[`2026-06-24-resonantos-ontology-retrieval-cards.md`](evidence-cards/2026-06-24-resonantos-ontology-retrieval-cards.md).
Builds on [`machine-map-and-moat-synthesis`](machine-map-and-moat-synthesis.md) and the
integration-SDK findings.

## 1. resonantOS as first dogfood host (governed research dispatch)

`2026-06-24-resonantos-living-archive-integration` (research, closed `resolved`, 7 agents).
resonantOS's **Living Archive** (its agent memory system; substrate = "Agent Memory
Architecture v7.1": WaveDB property graph + USearch ANN + temporal validity windows +
dream-consolidation + self-model) is the textbook SDK case: a host that already owns a
memory substrate, so CyberAlchemy does **not** reimplement inventory — it layers governance
on the write side. Verified seam (code-cited, E1): `archive-read`/`memory-provider` back our
**READ** (capture+lookup); `archive-intake-write` (intake-only) + the **Review Queue**
(`decide_review` approve/reject/escalate + `promote_review_artifact`) is the **WRITE/decision**
seam where cav2's governed store + promotion lifecycle plug in. **Map-vs-decision** holds: the
substrate governs **facts-over-time** (cav2 must NOT rebuild — OVERLAP); it has **no field for
authority/decisions/promotion** (the clean ADDITIVE gap cav2 fills). Honest claim≤proof: the
trusted-write **provider body** is host-resident and ABSENT from example code — CyberAlchemy
implements it behind resonantOS's already-named `promote_review_artifact`/501 boundary (their
owned contract). Net-new reduces to four atoms (provider body, port indirection, scope-tag
shims, b1/b2 store refactor); everything else is build-from-owned. Dogfood value: running
resonantOS generates the governed-run data that **builds** the SDK (build-from-owned at the
system level).

## 2. Ontology-over-semantic-search (the read-path insight)

CyberAlchemy's intent: **drop semantic search on the read path to reduce RAG work.** Sharpened
form (claim≤proof) — semantic search does not vanish, it **relocates twice**:

- **Two different "searches."** *Grounding/entry* ("where do I start?") vs *traversal* ("what's
  related?"). The ontology **kills traversal** (deterministic typed graph navigation — exact
  label/property-index lookup + adjacency prefix-scan, no vectors) and only **shrinks
  grounding** (mapping uncontrolled language → controlled vocabulary). Card:
  `ontology-traversal-over-vector-rag`.
- **Cost relocates query-time → ingest-time.** The PDF still uses neural models — but only in
  the *slow loop* (extraction/encoding at write-time); the fast/read loop is "no LLM, sub-50ms"
  because comprehension was paid once at ingest and crystallized into typed edges. The
  engineering bet: pay at write-time so reads are cheap+exact+governable. Card:
  `ingest-time-cost-relocation`.
- **Typed intent shrinks grounding toward zero.** **DomainSpec** delivers each agent a
  "discrete vector" start point — the query arrives already-typed, so even the grounding step
  collapses. This is the owner's long-held intuition for why context-injection/RAG handling is
  *not* needed: DomainSpec is already linked. Relates to `projects/domainspec-v2/` research +
  the DomainSpec language. Card: `typed-intent-discrete-vector`.

## 3. Why this IS cav2 / machine-map (governance needs determinism)

The deepest reason to drop read-time semantic search is **not** efficiency: **you cannot
attest, authorize, or promote a cosine similarity** (fuzzy, non-reproducible). A typed edge with
provenance *is* governable. So determinism-at-read is a **precondition for authority-at-read** —
the owner's "drop semantic search" intent and cav2 (manufacture authority) are the same move
from two sides. Card: `governance-requires-determinism`. Machine-map (VSM) placement: the Agent
Memory Architecture is a strong **S2 (coordination) + S4 (environment/model)** substrate but is
**missing S5** (its supersession is model-driven, not authority-grounded) — exactly the gap the
machine-map names; **cav2 = the missing S5**. The **ontology = the regulator's model**
(Conant-Ashby requisite variety); ontology-traversal vs vector-RAG = **structural attenuation
vs statistical attenuation** (navigate declared relations vs guess by cosine; clean channel vs
noisy). Ceiling (Ashby/Gödel): you can only economically traverse what you've **modeled** — the
un-modeled margin still needs a semantic fallback to find the door in; typed intent shrinks it.

## 4. Routing (owners — Inventory cannot promote)

- **cav2 authority owner / AUTHORITY-MODEL**: the governance-requires-determinism link (S5 sits
  on ontology, not vectors) is a candidate principle — route if it should become authority.
- **DomainSpec (domainspec-v2 research)**: the typed-intent → discrete-vector claim is owned
  there; this card cites, does not redefine.
- **commercialization decision-gate**: ingest-time relocation is the real engineering bet behind
  the cheap-deterministic-read moat.
- The deeper dispatch (`2026-06-24-...-three-topics`, pending) takes these three threads further.

## 5. Residue / open

- The trusted-write provider body, scope-tag shims, port indirection, b1/b2 split — all UNBUILT.
- "governance-requires-determinism" is a candidate synthesis, not yet governed authority.
- The ingest-time relocation has real, un-costed write-time + ontology-maintenance burden.
- The grounding margin is non-zero outside the modeled domain (requisite-variety ceiling).

## Downstream use

Use when a task asks "how does resonantOS/host-memory integrate", "why drop semantic search /
is RAG still needed", "why ontology not vectors", or "what does DomainSpec typed-intent buy us
on retrieval". Do not cite as canonical — owners are cav2 authority / DomainSpec / the
commercialization gate.
