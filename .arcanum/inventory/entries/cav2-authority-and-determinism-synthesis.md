---
tags: [inventory, cav2, authority, determinism, non-collapse, build-from-owned, moat, synthesis]
node_type: synthesis
is_session: false
layer: governance, architecture, market
nature: explanatory, reference
status: candidate
created: 2026-06-26
boundary: INTERNAL — moat content present (engine determinism, attestation); do NOT copy into public arcanum/
sources:
  - cyberAlchemy-v2/authority/AUTHORITY-MODEL.md
  - cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d48-authority-promotion-lifecycle
  - cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md
  - .arcanum/inventory/entries/deterministic-retrieval-thesis-synthesis.md
  - .arcanum/inventory/entries/machine-map-and-moat-synthesis.md
  - .arcanum/inventory/entries/authority-ontology-governed-artifact-synthesis.md
  - cyberAlchemy-v2/disciplines/development/2026-06-26-build-from-owned-validator-HANDOFF.md
---

# How CAV2 Authority Works, How Determinism Is Created & Used, and Why It Matters

Candidate Inventory synthesis (conceptual; **promotes nothing**; owners = cav2 authority /
definitions-governance / sigil-development). **Build-from-owned** of three existing entries —
[[deterministic-retrieval-thesis-synthesis]], [[machine-map-and-moat-synthesis]],
[[authority-ontology-governed-artifact-synthesis]] — plus this session's organizing + validator
findings ([[cav2-ontology-authority-organizing-synthesis]],
[[non-collapse-and-build-from-owned-definitions-map-synthesis]]). It *integrates*, it does not
restate. Claim ≤ proof: most of this is **intended/candidate**, flagged where it overclaims.

## Part 1 — How CAV2 authority works

**Authority = the DECISION layer:** who/what is allowed to make something *count*, for which
purpose — a permission granted by **owner route**, never by proximity, usefulness, or repetition
(`CAV2-D34`, `D41`). Three layers stay distinct (Non-Collapse rule 2):
- **Authority** = decides (owner route makes it count).
- **Ontology** = the *map* — describes/classifies/routes, **cannot decide** (`AUTHORITY-KINDS`: "do not use them to decide the candidate").
- **Governed artifact** = the *vehicle* — an artifact + owner route; the joint where map and decision meet, which only moves when an owner clears it.

The machinery:
1. **Closed kind set (`CAV2-D49`)** — 9 authority kinds (definition / constitution / discipline /
   decision / spec / runtime_contract / projection / evidence / residue), default-deny for anything
   unenumerated. Each kind's row carries `owner_route` + `authority_surface` — the **bridge** from
   ontology (shape) to authority (where it counts).
2. **One promotion lifecycle (`CAV2-D48`)** — `source evidence → candidate → owner-routed review →
   promoted → (optional) invariant/constitution pressure`, with per-stage gates, an owner route, and
   a stop/demote rule. `D43`/`D46`/Discipline-Growth-Rule/promotion-policy are **instances**.
3. **The apex model (this session)** — **CAV2 = the highest context.** Authority consolidates *up*
   (import-higher); lower contexts (Arcanum, domains) reference *up*. **Domain authority promotes up
   to CAV2 when it proves context-invariant** — the engine: *use domain authority to grow apex authority.*
4. **Non-collapse discipline** (`D22`/`D29` + the 7 AUTHORITY-MODEL rules + `forbidden_collapse`) —
   every kind/axis stays orthogonal; "no axis silently stands in for another."
5. **`claim ≤ proof` (`D38`)** bounds every promotion.

**CAV2 is the reflexive meta-authority MOLD; each domain authority is a CASTING** (it sells castings —
the ontologize thesis). **Honest posture:** this is authority in **method/posture, not yet enforcement**
— review-mode, OQ-1/OQ-2 open. The mold works; it is hand-operated, not yet a machine.

## Part 2 — How determinism is created and used

**The central correction (claim ≤ proof, from the deterministic-retrieval thesis):** "deterministic
ontology" is a **misnomer**. The ontology is **non-deterministically *authored*** (model-driven
write-time extraction = a *quarantined non-deterministic generator*). What is deterministic is **only
the post-promotion frozen typed referent + the recorded gate over it**.

**How it is CREATED** (three moves):
- **Quarantine the generator** — the non-deterministic (LLM) extraction runs at *write* time, behind a
  **recorded owner gate** (cav2 = the missing System-5 that confers authority on a frozen referent).
- **Freeze a stable, citable, typed referent** — the promoted object stops moving; it can be cited.
- **Relocate cost to ingest** — the cheap deterministic *read* is *purchased* by a model-heavy governed
  *write* loop (epoch-scoped; pays on the **authority dimension** + stable-schema/high-read regimes;
  FALSE as unconditional — re-ingestion at each ontology epoch is the unbounded tail).

**How it is USED** (two surfaces):
- **Deterministic retrieval** — read = **typed-intent → discrete subgraph traversal** (the query
  arrives *already a node*), not vector-RAG denoising. Holds only under a **node-contract boundary** on
  cross-feature edges (else transitive closure re-inflates to whole-graph RAG). KEYSTONE, build-from-owned, **not yet proven**.
- **Deterministic governance validators (this session)** — three **SMT/FOL siblings sharing one
  adapter**, reducing governance checks to decidable queries over **schema-typed records** with
  counter-witnesses on failure:
  - **non-collapse** (`D29`) — prove two declared dimensions are distinct;
  - **closure** (`D49`) — default-deny unenumerated kinds;
  - **build-from-owned** (`C17`) — search the corpus for an owner the candidate coincides-with/specializes.
  All **gated by OQ-1 / schema-`G2`** — the authority-object schema (the instantiation chain) must
  stabilize first.

**Where determinism STOPS (the hybrid boundary):** the **encoding choice** (which axes) + **absolute
non-thinness** (the *count-collapse frontier* from the lean repo) stay review/owner. The FOL
non-thinness witness is the **shadow of `functorial_strictly_dominates_count`** — determinism gives the
*relative* answer; the absolute call stays human.

## Part 3 — Why it matters

- **It collapses the attestation surface toward ~0.** Per [[machine-map-and-moat-synthesis]] the moat is
  **attestation + governance-data + vertical**. Determinism's payoff is *cost-dominance*: a result that
  provably follows from frozen referents + recorded gates is **cheap, repeatable proof** → auditable,
  board-WTP governance. **Demotion (claim ≤ proof):** determinism is an *optimization, not a necessity* —
  the real requirement is **provenance + a citable referent** (auditors attest non-deterministic
  processes routinely). Provability (Lean/cat-theory) is a **conjectural amplifier, NOT the moat** (the
  framing is inverted from the original).
- **It counters the LLM failure modes** (agent misbinding / superposition / nondeterminism): a frozen
  typed referent + recorded gate gives the agent a **stable thing to bind to**, instead of regenerating.
- **It is the engine moat** (memory: engine-algorithm-proprietary): cite + demonstrate results, **never
  publish the algorithm**; the LLM generator is the free path.
- **It makes read trivial** ([[read-trivial-via-selective-promotion-synthesis]]): cost-trivial (pre-paid
  write) + signal-trivial (default-deny).

**Honest bottom line:** the value is **roadmap value, intended-not-shipped** — Saturn is mostly unbuilt,
meta-authority is posture not enforcement, the validators are OQ-1-gated. Determinism is the *lever*; the
build order is schema-`G2` → the validators → the read-only observer/meter.

## Residue / open
- OQ-1 (schema stability) gates all three validators; the `specializes` instantiation chain is the precondition.
- Leg-1 (typed-intent→discrete) + the node-contract boundary remain **unproven** (own open residue).
- Absolute non-thinness (count-collapse) stays the review frontier.

## Boundary
Inventory candidate read-model. Promotes nothing. Owners: cav2 authority / definitions-governance /
sigil-development (validators) / decision-gate. INTERNAL — moat-adjacent.
