---
title: CyberAlchemy Integration SDK — findings (synthesis)
date: 2026-06-24
status: synthesis (claim ≤ proof; mostly TARGET, thin BUILT wedge)
inputs: [A1 architect, A2 coupling-skeptic, A3 adoption-SDK]
verified_against:
  - arcanum/spells/necronomicon/README.md (CANONICAL Necronomicon owner — the authority source)
  - .agents/skills/necronomicon/SKILL.md (generated projection; hard-coded .arcanum/ write paths :329-344; inventory required :39,:102)
  - development/authority-triage/SKILL.md (hard-coded cav2 sweep targets :79-83; executes AUTHORITY-MODEL/D48/D49 :30-37)
  - .agents/skills/inventory/SKILL.md (index.v0.1 leaks promotion_owner/residue/status/kind :160-194,:227-249)
  - development/moat-stack.md (engine free/paid decision :79-87)
---

# CyberAlchemy Integration SDK — Findings

## 1. THE HONEST CLAIM (lead with this)

**"CyberAlchemy is substrate-agnostic above ANY host memory" is FALSE as stated — it is refuted on the WRITE side.** The defensible, still-valuable, and goal-vindicating form is:

> **CyberAlchemy READS from the host substrate (the host's memory / wiki / notes, via a per-runtime adapter) and brings its OWN governed authority store for the DECISION / WRITE side.**

Why this is honest and *not* a retreat:

- **Read side is genuinely substrate-agnostic — bounded honestly (C2).** The retrieval/lookup INTERFACE is portable: inventory exposes a `lookup` contract that returns matching entries/cards (inventory SKILL.md:35) and ontology-vault has a fallback output shape — both prove a host store can back the read ports without being our schema. A1 and A2 *agree* here (A1: ports A,C decision-layer are substrate-agnostic; A2: "the retrieval/lookup INTERFACE is substrate-agnostic"). **Bound (no silent escape hatch):** READ ports are host-backed **only when the host actually has a store**. **When it does not, CyberAlchemy's own store backs reads — and in that case CyberAlchemy is no longer "above the host," it IS the store.** So "the host store always backs reads" is false; the honest claim is "the host store backs reads when one exists." This bounds C2; it does not weaken the keystone (read-decouples / write-doesn't) — a host *with* a store still decouples the read side cleanly.
- **Write side is NOT.** Governance STATE must be written, and it terminates in owned artifacts. Necronomicon (canonical owner: `arcanum/spells/necronomicon/README.md`) hard-codes 16 write paths under `.arcanum/necronomicon/` (generated SKILL.md:329-344) and **blocks** active substrate work until an inventory substrate exists (SKILL.md:39, :102; inventory is a required dependency). authority-triage's promotion ladder enacts AUTHORITY-MODEL / CAV2-D48 / CAV2-D49 (SKILL.md:30-37) and sweeps literal cav2 paths (:79-83). A2's dilemma is real: "above" forces either (a) write into the host store → couple them to OUR schema, or (b) keep our own `.arcanum/` store. **There is no third door.**

**The resolution vindicates the user's goal precisely.** The user wanted: *a host that already has an LLM-wiki should NOT have to reimplement inventory.* That is TRUE under this claim — **their wiki backs the READ ports**; they do not rebuild the lookup layer. What CyberAlchemy ships is its **own governed store for the write side** — and that store **IS the value the host adopts**, not a burden imposed on them. So A2's accusation ("a shadow `.arcanum/` store means they reimplemented inventory") **dissolves**: CyberAlchemy ships inventory *as the adopted product*, the host does not reimplement anything. (See §3.)

One-line product form (A2's defensible phrasing, adopted): **"a retrieval ADAPTER over a host store, backed by CyberAlchemy's own governed authority store."**

---

## 2. THE PORT MODEL (reconciling A1's 4 ports + A3's P1–P4)

Split by SIDE. This is the load-bearing reconciliation of A1 (4 ports A–D) and A3 (P1–P4): they describe the same seams; the clean cut is read vs. write.

### READ-side ports — host-backed, substrate-agnostic

| Port | A1 | A3 | Contract (host PROVIDES) | Substrate-neutral? |
|------|----|----|--------------------------|--------------------|
| **R1 capture-surface** | A (read notes/memory) | P1 (memory/knowledge read) | `read_notes()`, `read_model()` — raw capture from host store, **scope-tagged** (§4) | YES |
| **R2 lookup/query** | (read half of B) | P1 | `query()` over the host store **when the host has one**; when it does not, our own store backs reads — and then CA *is* the store, not "above" it (C2 bound, §1) | YES (interface) when host-backed; see §1 C2 bound |

### WRITE-side ports — CyberAlchemy's governed store (NOT neutral)

| Port | A1 | A3 | Split | Substrate-neutral? |
|------|----|----|-------|--------------------|
| **W-b1 generic candidate store** | B (split) | P2 (artifact write) | a plain candidate record store (id, text, source, scope-tag, `status: candidate`) | **portable** |
| **W-b2 governance-schema overlay** | B (split) | P2 | the CAV2 model: `promotion_owner`, `promotion_trace`, `residue`, kind/status enums | **ours — opt-in overlay** |

**The b1/b2 split is the decisive fix A1 named and source confirms.** Port B is *not* substrate-neutral as one unit: inventory's `inventory.index.v0.1` REQUIRES `promotion_owner` (SKILL.md:160,:234), `residue` (:162,:233), `status: candidate` (:189), and a `kind` enum that is promotion-lifecycle vocabulary (:182) — these are CAV2 terms wearing a port-shaped label (A1's "our model with a port-shaped label"). So: **b1 = a generic store any host could hold; b2 = the governance overlay that is CyberAlchemy's product.** A host adopting only b1 gets capture without governance; adopting b2 adopts our authority model (that adoption is the paid value).

### Cross-cutting ports

| Port | A1 | A3 | Contract | Notes |
|------|----|----|----------|-------|
| **S3 run/diff signal** | D (observability sink) | P3 (run/diff signal) | `append_signal()` — host emits run/diff telemetry into the observability sink (`.arcanum/observability/`, Necronomicon SKILL.md:344) | the read-only **observer/meter** — A3's smallest shippable wedge |
| **G4 gate-hook** | C (owner-route handoff) | P4 (gate-hook) | a **declared seam**; default action **"human reviews the diff"** | **MUST be a real seam from day one** |

**G4 is non-negotiable as a declared seam (A3 weak point, COMMERCIALIZATION R-IB-2).** P4 MAY be a no-op at install, but it must NEVER be *silently absent*. Rationale: gates add friction at intent-critical points; agents that author AND approve their own intent worsen escaped bugs (automation-bias circularity); **no gate → no governed-run signal → no data asset → nothing to attest** (which kills the governance-data moat, moat-stack.md layer #1). Default-deny posture matches CAV2-D49 (authority-triage SKILL.md:34, :102). So: install-time default = "human reviews the diff," explicitly present, overridable, never dropped.

---

## 3. THE BOUNDARY (clean): map-vs-decision

```
  HOST                                   CYBERALCHEMY
  ----                                   ------------
  owns the SUBSTRATE / MAP               owns the GOVERNED STORE + DECISIONS
  (their memory / wiki / notes)          (authority / promotion / write)
        |                                       ^
        |  R1 capture, R2 lookup  (read)        |
        +-------------------------------------->+  W-b1 store + W-b2 overlay (write)
                                                |  S3 signal · G4 gate
```

- **Host owns the read substrate (the MAP).** It answers "what is here" from its own store.
- **CyberAlchemy owns the governed store + decisions (the WRITE / authority side).** It answers "does writing this govern future work?" (authority-triage's needs-authority test, SKILL.md:87) and lands governed records in its own store.

This is the **map-vs-decision** boundary (A1). It **dissolves A2's "shadow store = reimplemented inventory"**: the host did not reimplement inventory — CyberAlchemy *ships* it, as the adopted decision layer. The host keeps its map; CyberAlchemy adds the decisions.

**A1↔A2 tension — RESOLVED, not split.** A1: "read decouples cleanly." A2: "write doesn't decouple." Both are correct *about different sides*. The resolution is not a compromise — it is the boundary itself: read = host substrate (decouples), write = CyberAlchemy store (does not, and shouldn't — that coupling IS the product).

---

## 4. THE CATEGORY-ERROR FIX (A2): the capture adapter MUST carry a SCOPE TAG

A2's verified category-error: "any memory system" melts four distinct things that differ on the axis **"does writing here govern future work?"**

| Scope tag | Example host artifact | Authority on the axis |
|-----------|----------------------|-----------------------|
| `user-memory` | Claude Code memory files | **low** — a capture surface, NOT authority |
| `project-instructions` | Codex `AGENTS.md` | medium — project rules, not governed authority |
| `runtime-rules` | copilot-instructions, host runtime config | medium — runtime scope |
| `knowledge-store` | host LLM-wiki / inventory | **governed read-model** when promoted |

**Hard rule:** the R1 capture-surface adapter **MUST stamp every incoming record with one scope tag** and read each per its scope. One port may span all four **only by tagging scope, never by melting them.** A record captured from `user-memory` enters as `status: candidate` and can never short-circuit to authority on capture alone (this is exactly Necronomicon's "capture as evidence, not truth," SKILL.md:42, :103). Deleting the scope tag would re-introduce the read-model-vs-authority collapse A2 flagged.

---

## 5. BUILD-FROM-OWNED + THE NET-NEW SLICE

Per the owned-in-repo precedent rule, the harness owners already exist — the SDK EXTENDS them; it does not net-new them.

| Owned component | Role in the SDK | Verified |
|-----------------|-----------------|----------|
| **Necronomicon** (canonical: `arcanum/spells/necronomicon/README.md`) | the **harness owner** — capture loop, no-promotion guardrail, routing desk, substrate classifier ("a coordinator, memory boundary, and substrate classifier") | SKILL.md MVP loop :35-45, :100-105 |
| **arcanum-bootstrap** | the **per-runtime install** — one canonical source → N generated runtime packages (regenerate-from-canonical) | bootstrap skill (native/codex/claude/copilot adapters) |
| **inventory** | the **default candidate-store TODAY** — single schema, CAV2-coupled (it leaks `promotion_owner`/`residue`/`status`/`kind`; see §8). It is NOT yet split into b1/b2 — that separation is **net-new slice 3 below**, not a current property of inventory. | inventory SKILL.md (index.v0.1) |

**NET-NEW (genuinely unbuilt) = exactly three slices:**

1. **Port indirection** that frees Necronomicon's hard-coded `.arcanum/necronomicon/` write paths (SKILL.md:329-344) and authority-triage's hard-coded cav2 sweep targets (SKILL.md:79-83) — replace literal paths with a resolved substrate handle. This is the decoupling refactor **both A1 and A2 independently named** as the load-bearing debt.
2. **The per-runtime memory adapters** (§6) — the scope-tagged read shims, generated by bootstrap.
3. **The b1/b2 store split** — separate the generic candidate record (b1) from the CAV2 governance overlay (b2) inside inventory's schema.

A1 also asks for an **authority-triage classifier mode** (a substrate-PORT-aware mode) — folded into slice 1.

---

## 6. THE SCOPED FIRST PER-RUNTIME MEMORY ADAPTER (the concrete ask)

### `MemoryAdapter<claude>` — spec

```
MemoryAdapter<claude>
  REQUIRES (host provides):
    read_notes()        -> raw Claude Code memory files (MEMORY.md, memory/*.md)
    read_model(query)   -> host lookup result (may be empty -> fallback to our store)
    write_model(record) -> persist a governed record (lands in CyberAlchemy's store)
    append_signal(evt)  -> run/diff telemetry into .arcanum/observability/

  PROVIDES (to CyberAlchemy):
    normalized, scope-tagged candidate records:
      { id, text, source, scope_tag: "user-memory", status: "candidate" }
      # NO promotion. capture is evidence, not truth. (Necronomicon SKILL.md:42)

  PROVENANCE:
    canonical source -> regenerated per runtime via arcanum-bootstrap
    (one canonical -> N runtime packages; regenerate-from-canonical, never hand-edit)

  BEHAVIOR:
    reads Claude Code memory files as CAPTURE (scope = user-memory, low authority),
    lands them in CyberAlchemy's OWN governed store as status: candidate,
    NEVER as authority. Promotion is a separate, owner-routed, gated decision (G4).
```

### `MemoryAdapter<codex>` — variant

Same `REQUIRES`/`PROVIDES`, two deltas: (1) `read_notes()` reads **`AGENTS.md`**; (2) scope tag = **`project-instructions`** (NOT `user-memory`) — so a record captured from `AGENTS.md` is read as project-scope rules, not user-memory. The scope tag is the *only* thing that changes — proving §4's claim that one port spans substrates *by tagging*, not by melting.

This is the **first per-runtime adapter** (the user's concrete ask) and A3's **first case (a)**: dogfood our own Claude Code memory; G4 is a no-op (we review our own diffs); seeds proof-it-works-on-ourselves.

---

## 7. FREE / PAID + FIRST 3 CASES (A3, per the engine-moat decision)

**FREE (the wedge) — value day one without the host adopting our governance:**
the integration layer + per-runtime adapters + the free audits (layering / tag / alignment) + the **LLM test generator** (the wedge). The free path is the LLM generator.

**PAID (the moat):** the **deterministic engine ALGORITHM** (trade-secret moat — verified, moat-stack.md:79-87, refines layer #5) + governance / authority / attestation (the governance-data asset, moat-stack.md layer #1).

**Boundary rule:** cite + demonstrate engine RESULTS; **never publish the algorithm.** The LLM generator is the free, public path.

**FIRST 3 CASES (ship order):**
- **(a) Claude Code** — dogfood our own memory (§6); G4 no-op; proves it works on ourselves.
- **(b) Codex `AGENTS.md`** — proves vendor-neutrality / cross-tool (the counter-positioning moat, moat-stack.md layer #3).
- **(c) generic host with an existing LLM-wiki** — proves the read-port abstraction (the host's wiki backs R1/R2; they do NOT reimplement inventory — §1's vindication, demonstrated).

**Ship-smallest-first (A3):** the first shippable artifact is the **read-only observer/meter** = S3 run/diff signal + the free audits. It needs no governance adoption by the host, delivers a metric on day one, and widens with customers. **Do NOT pre-sell the unbuilt moat** (§8).

**A1↔A3 tension — made explicit, owner-decision noted.** A1 wants the complete 4-port architecture; A3 wants the minimal wedge (observer/meter first). **Resolution:** the full port set is the TARGET (design all of §2 now so seams exist — especially G4, which must be declared from day one), but only **R2-read + S3 + the free audits are BUILT first**. The rest are declared seams filled with customers. *Owner decision required:* confirm that G4 ships as a declared-but-default-no-op seam in case (a) rather than a fully wired gate — recommended yes (A3), but it is a product call, flagged here.

---

## 8. THE DECOUPLING-DEBT LEDGER (claim ≤ proof)

| Capability | TARGET | BUILT today | Evidence |
|-----------|--------|-------------|----------|
| Substrate indirection (free hard-coded paths) | resolved substrate handle | **hard-coded** `.arcanum/necronomicon/` (16 paths) | Necronomicon SKILL.md:329-344 |
| authority-triage substrate-neutral sweep | port-aware classifier mode | **hard-coded** cav2 literal paths | authority-triage SKILL.md:79-83 |
| Candidate store neutrality | b1 generic / b2 overlay split | **single schema leaks CAV2** (`promotion_owner`, `residue`, `status`, `kind` enums) | inventory SKILL.md:160-194,:227-249 |
| Inventory optional behind a port | host wiki backs read; b1 portable | **inventory is REQUIRED**; Necronomicon blocks without it | Necronomicon SKILL.md:39,:102 |
| Per-runtime memory adapters | scope-tagged shims (claude/codex/...) | **not built** (spec only, §6) | net-new slice 2 |
| Deterministic engine | paid moat | **mostly unbuilt** (trade-secret; algorithm not shipped) | moat-stack.md:79-87 |
| Attestation / governance-data | the durable moat | **deferred** (~0 built; compounds with customers) | moat-stack.md layer #1 (cost ~0, deferred) |

**Honest bottom line:** today the paths are hard-coded (`.arcanum/`), the candidate-store leaks the CAV2 schema, and most of the moat is deferred/unbuilt. **The SDK is a roadmap with a thin REAL adapter at the front** — the free wedge (read-only observer/meter + free audits + the LLM-generator + the first `MemoryAdapter<claude>`). Sell the wedge; design the seams; build the moat with customers. **Do not sell the unbuilt moat as shipped** (vaporware risk, A3).

---

## Tensions — disposition

- **A1 ↔ A2 (read-decouples / write-doesn't):** RESOLVED by the read/write side-split (§2, §3) — both true of different sides; the write coupling IS the product, not a defect.
- **A1 ↔ A3 (complete-architecture / minimal-wedge):** EXPLICIT — full port set is TARGET (design now), R2-read + S3 + free audits + first adapter are BUILT first; **one owner decision flagged** (G4 ships as declared-default-no-op seam in case (a) — recommended, product call).
- **A2 category-error:** FIXED by the mandatory scope tag (§4).
