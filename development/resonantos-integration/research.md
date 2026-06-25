# research.md — collected explorer returns (verbatim)

Dispatch: `2026-06-24-resonantos-living-archive-integration` (research). Three explorers,
pairwise tensioned on the source-corpus × methodology composite axis. Returns are verbatim;
the cited synthesis is in `findings.md`.

---

## E1 — EMPIRICAL (resonantOS CODE) — Living Archive integration seam map

All files in `/home/vrondelli/projects/resonantos-vnext/`. All cited files present; none missing.

### 1. Capability/surface model — manifest, EXACT (`public/addons/living-archive.json`)

`requestedCapabilities` (all `granted:false` by default; flipped true only via the `recommended-memory-system` grantPreset, lines 67–104):

- `memory-provider` — `scope:"system"`, `revocationBehavior:"hard-stop"` (L26–29). The system-wide provider slot — also fills `systemSlots[0].id="memory-system" role:"default-provider" replaceable:true` (L106–113).
- `filesystem` — `shared`, `hard-stop` (L31–35).
- `providers` — `shared`, `revocationBehavior:"degrade"` (L37–41) — the ONLY degrade-on-revoke cap (provider fabric routing for ingest, connector `ingest-provider-route` L165–172).
- `archive-read` — `shared`, `hard-stop` (L43–47). `archiveIntegration.readScopes: ["active-memory/context","system-memory/context"]` (L125).
- `archive-intake-write` — `scope:"intake-only"`, `hard-stop` (L49–53). `archiveIntegration.intakeWriteScopes: ["Memory/INTAKE"]`, `canRequestIngest:true`, `canWriteKnowledgePages:false` (L124–129). **This is THE governed-write seam.**

`revocationBehavior` semantics enum is host-enforced at `src/sdk/addons/validation.ts:45` → `["hard-stop","degrade","hide-surface"]`. `intake-only` is a first-class `CapabilityScope` at `validation.ts:44` and `src/core/contracts.ts:19`; archive write modes enum `["none","intake-only"]` at `validation.ts:72`.

Surfaces (manifest L10–23):
- `living-archive-workspace` — `type:"page"`, label "Memory Workspace" (L12–16): configure sources, inspect intake, review memory operations, manage provider — the READ/lookup + provider-management surface.
- `living-archive-review` — `type:"panel"`, label "Review Queue", "Review memory intake and promotion requests before trusted writes" (L18–22) — **the promotion gate surface.**

`runtimeIsolation.boundary:"host-mediated-service"` + `requiresReviewedGrant:true` (L62–66); `runtimeType:"local-service"` (L9). Validated against `validation.ts:49` boundary enum.

### 2. Host-mediated contract enforcement (src/)

- `ADDON_CAPABILITIES` registry: `src/sdk/addons/contracts.ts:62–76` (archive-read L64, archive-intake-write L65, memory-provider L67).
- Validation invariants that BIND a scope to its capability:
  - `validation.ts:397–404` — archive read scopes require `archive-read` (`archive-read-scope-requires-capability`).
  - `validation.ts:410–417` — archive intake write scopes require `archive-intake-write`.
  - `validation.ts:936–945` — `archiveReadMode !== "none"` requires `archive-read`.
  - `validation.ts:945–951` — `archiveWriteMode === "intake-only"` requires `archive-intake-write`.
- Runtime grant + action gate (the host's actual enforcement point a plumber must satisfy):
  - `src/core/policies.ts:28–51` `canPerformArchiveAction(state, actorId, action, scope)` — `archive-read` checks `policy.readScopes` (L39–40); `archive-intake-write` checks `policy.intakeWriteScopes` prefix-match (L42–46); `archive-knowledge-write` → `policy.canWriteKnowledgePages` (L47–49); else `canRequestIngest` (L50). **The intake/knowledge split is enforced HERE.**
  - `src/core/policies.ts:56–66` `isCapabilityGranted(installation, capability, expectedScope)` — note L65: `scope:"system"` grant satisfies ANY expected scope (so the `memory-provider` system grant is the super-grant).
- `AddOnMemoryAccessContract`: `contracts.ts:460–462` (`archiveReadMode`, `archiveWriteMode`). `ArchiveAction` type: `contracts.ts:75` = `archive-read | archive-intake-write | archive-knowledge-write`(+request).
- Default archive policy actor rows showing the SAME shape live actors use: `src/core/defaults.ts:825–856` — e.g. a review actor with `intakeWriteScopes:["_LivingArchive/REVIEW"]` (L833–834) and an external-agent actor `intakeWriteScopes:["_LivingArchive/INTAKE/external-agents"]` (L842); knowledge-write described as blocked for ordinary add-ons (L856).

### 3. What the examples ACTUALLY do

**Memory service (`examples/living-archive-memory-service.mjs`) — HTTP host surface**
- `createLivingArchiveMemoryService(options)` L109 → wraps `createLivingArchiveBridge` L115; HTTP `POST /memory/:operation` router L117–165 (route regex L128).
- **Operation→tool map** `memoryOperationToTool` L54–63: `status`, `search`, `read`, `intake-write`→`living_archive_write_intake`, `ingest-request`→`living_archive_request_ingest`, `review-queue`, `review-artifacts`, `lint`.
- **`providerOnlyOperations`** Set L65–72: `process-ingest-request`, `decide-review`, `promote-review-artifact`, `maintenance-cycle`, `background-cycle`, `semantic-lint` → return **HTTP 501** with `boundary.trustedKnowledgeWrites:false`, reason "Trusted wiki writes require Strategist-owned ingest/review inside the desktop host" (L135–147). **This local service deliberately CANNOT promote — the promotion gate is host-only.**

**MCP bridge (`examples/living-archive-mcp.mjs`) — what it exposes to external clients**
- `createLivingArchiveBridge(config)` L370; `backend` = `"host-http"` if `memoryServiceUrl` set else `"portable-folder"` (L375). `proxy()` L377–382 forwards to the host HTTP service.
- 15 tools `livingArchiveTools` L202–368. Handlers `handlers` L665–698. JSON-RPC stdio server `runStdioServer` L764, `handleJsonRpc` L726 (`tools/call` L751).
- **READ ports** (back by `archive-read`/`memory-provider`):
  - `living_archive_status` L666 / `status()` L384–428.
  - `living_archive_search` L667 / `search()` L430–479 (scoped by domains).
  - `living_archive_read` L668 / `read()` L481–504 (guarded path resolve `resolveMemoryPath` L109–116; root-escape guard `pathInside` L97–100).
- **GOVERNED-WRITE ports** (back by `archive-intake-write`, intake-only):
  - `living_archive_write_intake` L669 / `writeIntake()` L506–546 — writes to `INTAKE/mcp/{bucket}/{fileName}` ONLY (L518–521), filename pattern guard `writeFileNamePattern` L35/L513, writes `.metadata.json` with sha256 L522–539. Tool desc L243: "Never writes trusted AI Memory pages directly."
  - `living_archive_request_ingest` L670 / `requestIngest()` L548–593 — queues a JSON request into `INTAKE/review-queue/` (L558–561) stamped `boundary.trustedKnowledgeWrite:false, requiresStrategistOwnedIngest:true` (L579–582).
- **PROMOTION-GATE ports** (proxy-only; portable mode throws `portableUnsupported` L632–636):
  - `living_archive_review_queue` L671 / `reviewQueue()` L618–623 (reads `INTAKE/review-queue`).
  - `living_archive_review_artifacts` L672 / `reviewArtifacts()` L625–630 (reads `AI_MEMORY/provenance/review-artifacts`).
  - `living_archive_process_ingest_request` L673, `living_archive_decide_review` L677 (action enum approve/reject/escalate L313), `living_archive_promote_review_artifact` L681 — desc L321: **"This is the only MCP path to trusted knowledge writes."** Plus `maintenance_cycle` L685, `background_cycle` L689, `semantic_lint` L694. All `proxy(...).catch → portableUnsupported`.
- Test confirms the boundary: `examples/living-archive-memory-service.test.mjs` L86–89 (review-queue len 1, `requiresStrategistOwnedIngest:true`), L91–92 (`trustedKnowledgeWrite:false`), L123–128 (`promote-review-artifact` → 501 "full ResonantOS host provider").

### 4. POSITION — defended, honestly

**The seam IS already built and the position holds.** Exact named hooks a plumber attaches CyberAlchemy's governed-write overlay to:

- **Governed-write IN** → capability `archive-intake-write` (manifest L49–53, scope `intake-only`), enforced at `policies.ts:42–46`; entrypoints `living_archive_write_intake`/`writeIntake()` (mcp L669/L506) and `living_archive_request_ingest`/`requestIngest()` (L670/L548) → land in `INTAKE/mcp/*` and `INTAKE/review-queue/`.
- **Promotion gate** → surface `living-archive-review` (manifest L18–22) + entrypoints `living_archive_decide_review` (L677, approve/reject/escalate) and `living_archive_promote_review_artifact` (L681, "only MCP path to trusted knowledge writes"). The `archive-knowledge-write` action (`policies.ts:47–49`, `canWriteKnowledgePages`) is the trusted-write privilege CyberAlchemy's overlay would govern — and manifest pins it `false` (L128), so the overlay slots in as the thing that grants it.
- **READ ports** → `archive-read` (L43–47) + `memory-provider` (L26–29, system super-grant via `policies.ts:65`); entrypoints `living_archive_search`/`search()` (L667/L430) for lookup and `living_archive_read`/`read()` (L668/L481) for capture/fetch; surface `living-archive-workspace` (L12–16).

**Honest caveats / tension reported:**
1. The portable example service **explicitly refuses** all promotion ops (501, `providerOnlyOperations` L65–72; portable handlers throw `portableUnsupported` L632). So the promotion gate is a CONTRACT/seam, not a runnable implementation in these examples — `process/decide/promote` exist only as proxied tool *names* pointing at "the full ResonantOS host provider" which is NOT in this repo's example code. A plumber attaching an overlay attaches at the proxy boundary (the host HTTP `:operation` it 501s), i.e. CyberAlchemy would supply the missing provider, not merely overlay an existing one.
2. `intake-only` write physically resolves only under `INTAKE/` (mcp L518) — the seam is genuinely intake-scoped, so the overlay cannot widen write target without the host's `archive-knowledge-write` grant. That is the wanted property, but means the overlay's trusted-write must run host-side (Strategist-owned), not in the MCP/portable layer.
3. `decide_review` already carries the approve/reject/escalate vocabulary (L313) — CyberAlchemy's governance would map onto this enum rather than introduce a new one.

Net: position SUPPORTED for the read + intake + review-queue seam (fully built and tested); PARTIALLY-SUPPORTED for promotion — the gate is contractually defined and named end-to-end, but the trusted-write executor is host-resident and absent from example code, so it's an attach-point for an overlay to *implement*, not an existing implementation to wrap.

---

## E2 — FORMAL/ARCHITECTURAL (the PDF) — Substrate governance map (Agent Memory Architecture v7.1)

**Corpus:** "Agent Memory Architecture v7.1" PDF, 11 pages. Citations to the PDF's internal page numbering. Position to defend: the living archive **already performs rich fact-over-time governance**, so a cav2-style governance integration risks redundancy — reported honestly where it holds and where it does not.

### 1. Two-loop separation — fast deterministic retrieval vs. slow model-driven maintenance
**What it is (p.1, p.2, p.4–7):** Retrieval is "fast, deterministic, no neural models" — pure Gremlin graph traversal over WaveDB + USearch ANN, ~10–50ms, invariant "Only one GPU call per query… everything before Bonsai is CPU/disk" (p.2, p.5). The slow loop is async, model-driven, per ingestion event (~25–90ms) and "evolves meaning" (p.1, p.6).
**ADDITIVE vs OVERLAP:** an **execution-tier split (read-path/write-path), orthogonal to authority governance**. Governs *latency/determinism*, not *who may assert a fact* or *whether a decision is promotable*. cav2 promotion gates neither implemented nor contradicted — they sit *on top of* the slow loop's write step. **Orthogonal → ADDITIVE.**

### 2. Property graph in WaveDB + USearch ANN
**What it is (p.2–3):** Typed directed edges (`e/{edge_id}`) carry four governance-bearing properties: `validity_start`, `validity_end`, `utility_score`, `confidence` (p.3). USearch = HNSW ANN semantic entry (p.2–3); GraphQL schema "enforces node/edge types and required properties" (p.3).
**ADDITIVE vs OVERLAP:** the edge property set is the substrate's **entire native governance vocabulary over facts** — *fact-scoped*, not *authority-scoped*. `confidence` is a per-edge scalar, not a provenance/authority tier; no `authority_kind`, `decision_id`, `promotion_stage`, `owner`. So schema enforcement of *fact shape* **overlaps** any cav2 re-imposition of fact-shape (redundant there), but there is **no field for decision lineage or promotion state** — clean gap. **Mixed: OVERLAP on fact-shape/confidence, ADDITIVE/gap on authority-typing.**

### 3. Temporal truth model — validity windows + supersession
**What it is (p.7, p.11):** "Facts have validity windows. Superseded facts are retained but marked invalid" (p.1). Default queries traverse `validity_end > now (or ∞)`; `asOf("2025-03-01")` historical traversal; stale detection = `validity_end < now but != null` (p.7). "A fact isn't deleted; it's invalidated. The graph remembers what it used to believe and when that changed" (p.7).
**ADDITIVE vs OVERLAP:** **the strongest case for redundancy, but narrow.** The substrate genuinely owns *governance-of-facts-over-time*: temporal validity, non-destructive supersession, `asOf` reconstruction, stale flagging. Re-implementing those would **directly overlap/redundant**. Honest boundary: it governs **truth-validity of an atomic fact**, not **authority/canonicality of an assertion** — `validity_end` answers "is this still *true*?", not "is this the *canonical/promoted* statement, who *decided*, against which constitution/definition?". **OVERLAP on temporal fact-history; ADDITIVE on authority/canonicality.**

### 4. Dream-state consolidation — replay / prune / lucid-dream contradiction resolution via Bonsai
**What it is (p.7):** REPLAY (MoE SSM) replays high-utility traces, JEPA re-scores, detects contradictions, flags stale edges. PRUNING tombstones low-utility edges, removes orphans, merges redundant facts. LUCID DREAM: if contradictions flagged, "Wake Bonsai → Read conflicting facts + context → Adjudicate: **supersede / merge / annotate** → Write resolution." Verifier (Bonsai 8B ternary) "resolve[s] contradictions, adjudicate[s] stale facts" (p.4).
**ADDITIVE vs OVERLAP:** a genuine contradiction-adjudication engine — looks like it overlaps cav2 decision governance, but: (a) adjudication is **model-driven and per-contradiction, not authority-grounded** (no constitution, no decision ID, no rationale ledger, no override-by-authority path — just a graph write); (b) it adjudicates **FACTS in conflict, not DECISIONS/PROMOTIONS** ("two documents claim X and not-X" is factual; cav2 decisions are a different object class it never represents); (c) pruning is **utility-thresholded, not policy-governed**. **OVERLAP on factual contradiction resolution** (cav2 must not rebuild); **ADDITIVE on decision-as-first-class-object, rationale capture, authority-grounded adjudication.**

### 5. Self-Model "I don't know" percolation gate
**What it is (p.4, p.11):** "Logic over graph stats," CPU, query-time; "Track[s] graph density, gate[s] mind-waking, decide[s] 'I don't know'" (p.4); prevents hallucination in sparse regimes (p.1); threshold "empirically learned… domain-dependent" (p.11).
**ADDITIVE vs OVERLAP:** a **coverage/abstention gate keyed on graph density** (epistemic sufficiency), not authority sufficiency. Abstains when it knows *too little*; does NOT abstain when a fact is *un-promoted/un-reviewed/below an authority tier*. Different questions. **Orthogonal → ADDITIVE** (a promotion gate composes WITH it: density-pass AND authority-pass).

### 6. Chat-vs-code profiles
**What it is (p.7–8):** "core architecture is identical. Only the ingestion adapter and timing model change." `MemoryConfig` exposes profile flags (p.8).
**ADDITIVE vs OVERLAP:** parameterizes **ingestion mechanics**, not governance policy; no knob for authority tiers/review/promotion. **Orthogonal → ADDITIVE.**

### Bottom line — precise FACT vs AUTHORITY partition
**Substrate ALREADY owns (governance-of-FACTS-over-time — cav2 should NOT rebuild; OVERLAP):** temporal validity + non-destructive supersession + `asOf` + stale detection (p.7,11); per-edge `confidence`/`utility_score` (p.3); factual contradiction detection (JEPA/replay) + resolution (Bonsai supersede/merge/annotate) (p.4,7); utility-based pruning/merge (p.7); coverage abstention "I don't know" (p.4,11); schema enforcement of node/edge shape (p.3).
**Substrate does NOT own (governance-of-AUTHORITY/DECISIONS/PROMOTION — clean ADDITIVE gaps):** no authority-typing (`confidence` ≠ canonicality) (p.3); no decision-as-first-class-object (adjudication writes a mutation, not a decision w/ ID/options/owner/rationale) (p.7); no promotion lifecycle/gate (pruning is a scalar threshold, not a policy) (p.7); no constitution/definition grounding for adjudication (p.7); no provenance-of-authority/override path.
**Verdict (honest):** redundancy risk is **real but bounded to the temporal-fact lane**. Re-implementing validity windows / supersession / stale detection / contradiction resolution would be **redundant**. Authority, decisions, promotion are **absent from the data model** (no field/object/gate) → cav2 governance is **orthogonal and additive**, PROVIDED it grounds on the substrate's temporal/confidence primitives rather than duplicating them. Clean seam: cav2 supplies *authority typing + decision ledger + promotion gate* as a layer that **reads** `validity`/`confidence`/`utility` and **writes** an authority dimension the substrate has no field for today.

---

## E3 — INTEGRATION-DESIGN (our cav2 + SDK) — seam map + public explainer + boundary list

**Position:** the adopted value is the cav2 WRITE/decision overlay *specifically*. The READ side decouples cleanly onto the host substrate; the WRITE side does not, and *that non-decoupling is the product* (findings.md §1–§3).

### A. SEAM MAP — cav2 element → Living-Archive seam → adopted-overlay vs net-new plumbing

| cav2 element | Source | Maps onto seam as | ADOPTED overlay / NET-NEW plumbing |
|---|---|---|---|
| **Governed store** | AUTHORITY-MODEL Core Flow :32–42; findings §3 | Write target behind `archive-intake-write`; CyberAlchemy owns governed store, host owns read MAP | **ADOPTED** (W-b2 overlay) |
| **Authority-triage front door** | findings §2/§3; authority-triage SKILL.md:87 | Intake classifier: "does writing this govern future work?" → candidate vs authority | **ADOPTED** as the decision; *port-aware classifier mode* **NET-NEW** (slice 1) |
| **Promotion lifecycle (D48) / default-deny (D49)** | AUTHORITY-MODEL :63–69; findings §2 | The Review Queue: capture enters `candidate`, never auto-promotes; owner-routed gated decision | **ADOPTED** — Review Queue *is* the promotion ladder |
| **Scope-tags** (user-memory/project-instructions/runtime-rules/knowledge-store) | findings §4 | Stamped at `archive-intake-write`; queue reads per scope, never melts | **NET-NEW plumbing** (scope-tagged shims/adapters, slice 2) — concept is cav2, adapters unbuilt |
| **Inventory** (candidate store) | findings §5,§8; inventory SKILL.md | Backs Review Queue candidate records | **SPLIT**: b1 generic store = portable; b2 governance overlay (`promotion_owner`/`trace`/`residue`/kind/status) = ADOPTED cav2; the b1/b2 split = NET-NEW (slice 3) |
| **Authority Kinds** | AUTHORITY-MODEL :48–61 | Typed vocabulary promoted *into* | **ADOPTED** |
| **Narrowest-Owner Rule** | AUTHORITY-MODEL :90–104 | Routing behind the queue | **ADOPTED** |
| **READ ports (R1 capture / R2 lookup)** | findings §2 | Host Living Archive *is* the substrate | host-owned; CyberAlchemy only adapts (when host has no store, CyberAlchemy *is* the store — findings §1 C2) |

**Bottom line:** resonantOS adopts the **b2 governance overlay + authority-triage front-door + promotion/Review-Queue lifecycle** on the WRITE seam; the READ seam stays host-owned. Genuinely net-new = three slices (findings §5): (1) port indirection freeing hard-coded `.arcanum/` paths, (2) scope-tagged per-runtime adapters, (3) b1/b2 store split. None built today (findings §8).

### B. PUBLIC-SAFE EXPLAINER (for a resonantOS teammate)
- **CyberAlchemy (internally "cav2") = the governance layer that decides what your archive may *rely on*.** Sits on the write side; does not replace the Living Archive.
- **Living Archive vs governance layer:** Living Archive = memory substrate, owns the MAP ("what is here"). CyberAlchemy owns the governed store + decisions ("does writing this govern future work?").
- **Capture vs governed-write:** capture = evidence, `status: candidate`, never short-circuits to authority. Governed-write = promoting a candidate into something relied on (Core Flow :32–42).
- **Promotion / Review-Queue:** explicit, owner-routed, gated; **default-deny** — unenumerated kinds stay blocked until a decision adds them (D49, :63–69). The Review Queue *is* this ladder.
- **Authority-triage front door:** every intake passes "does writing this govern future work?" → routes to the **narrowest responsible owner** (:90–104).
- **Scope-tags:** each record carries one of `user-memory`/`project-instructions`/`runtime-rules`/`knowledge-store`, read per scope — one intake port spans many substrates by tagging, never melting.
- **How it relates:** cav2 is the authority spine under two intended efforts — **Saturn** (convergence loop closing intent↔reality with evidence) and **DomainSpec** (typed-intent layer), both **intended, not shipped** (Decision 1 :16–26). Posture: AI augments human work, never replaces it (Decision 2 :27–36).

### C. DO-NOT-EXPOSE list
**SAFE:** cav2/CyberAlchemy by name; governed store, promotion lifecycle, authority kinds, authority-triage, scope-tags, candidate-vs-authority, Narrowest-Owner Rule; Saturn & DomainSpec *named but framed intended-not-shipped* (:24–26); that a deterministic engine exists + its *results* (determinism, byte-stability, mutation 38.75%→54.37%, spec 96%, self-derive fixpoint) (engine-moat Decision 2 :33–37); the open calculus (C1–C4, 25 meta-types, 29 edges, `T=f(C,R,Δ)`) (:43); the free wedge (layering/tag/alignment audits + LLM test generator) (Decision 1 :19–24).
**DO NOT EXPOSE:** the moat stack as internal analysis + paid-boundary mechanics; the engine *algorithm* (`parse→δ→key→emit`, L0–L4, Option-C id-map, tier split, fenced regions, Lean proof internals) (:38–42); the internal layer-map / 8-layer stack (:43); internal names **MARS / MOGT / Necronomicon** (:42–43 — refer to "the capture harness" generically); private prose from `cyberAlchemy-v2/`/`framework-unification/`/`implementation/` (:40–41). Every outward artifact runs a `boundaries.md` scrub before leaving.
**Guard line:** *Describe the governance model freely; Saturn/DomainSpec as intended-not-shipped; cite engine results but never the algorithm; never write MARS/MOGT/Necronomicon or the L0–L4 / parse→δ→key→emit internals.*
