---
tags: [resonantos, living-archive, cav2, integration, governance, promotion, synthesis]
node_type: synthesis
status: candidate
created: 2026-06-24
sources:
  - development/resonantos-integration/research.md (E1, E2, E3 verbatim explorer returns)
  - resonantos-vnext/public/addons/living-archive.json
  - resonantos-vnext/examples/living-archive-mcp.mjs
  - resonantos-vnext/examples/living-archive-memory-service.mjs
  - resonantos-vnext/src/core/policies.ts
  - resonantos-vnext/src/sdk/addons/validation.ts
  - "Agent Memory Architecture v7.1" (PDF, 11pp)
  - cyberAlchemy-v2/authority/AUTHORITY-MODEL.md
---

# findings.md — cav2 ↔ resonantOS Living Archive integration

## 1. One-line answer

resonantOS's Living Archive owns the **READ map and the fact-over-time substrate**; cav2/CyberAlchemy plugs into the **WRITE/decision seam** (intake → Review Queue → promotion) — and that promotion executor is a contractually-named, host-resident attach-point we must **implement**, not an existing provider we wrap (E1 caveat 1).

## 2. What-backs-what table

| Living Archive seam (resonantOS) | What it backs on our side | Evidence |
|---|---|---|
| READ: `archive-read` / `memory-provider` caps; `living_archive_search`/`search()`, `living_archive_read`/`read()` | our **capture (R1)** + **lookup (R2)** — host substrate *is* the store | E1 §4 READ ports (mcp L667/L430, L668/L481; manifest L43–47, L26–29); E3 §A row "READ ports" |
| WRITE-IN (intake-only): `archive-intake-write` cap; `living_archive_write_intake`/`writeIntake()` → `INTAKE/mcp/*`, `living_archive_request_ingest`/`requestIngest()` → `INTAKE/review-queue/` | cav2 **governed store** (b2 overlay) — where intake lands as `candidate` | E1 §4 governed-write (mcp L669/L506, L670/L548); `policies.ts:42–46`; E3 §A "Governed store" |
| REVIEW surface: `living-archive-review` panel ("Review Queue"); `living_archive_review_queue`/`reviewQueue()` | cav2 **promotion lifecycle (D48) / default-deny (D49)** — the queue *is* the ladder | E1 §1 (manifest L18–22), §4 (mcp L671/L618); E3 §A "Promotion lifecycle" |
| DECIDE/PROMOTE: `living_archive_decide_review` (approve/reject/escalate, L313), `living_archive_promote_review_artifact` ("only MCP path to trusted knowledge writes", L321); action `archive-knowledge-write` gated by `canWriteKnowledgePages` | cav2 **promotion gate + authority-triage decision** map onto the existing enum | E1 §4 promotion ports (mcp L677, L681), §2 (`policies.ts:47–49`); E3 §A "Authority-triage", "Promotion lifecycle" |

The split is enforced **in the host** at `policies.ts:28–51` `canPerformArchiveAction` — `archive-knowledge-write → policy.canWriteKnowledgePages`, and the manifest pins that `false` (L128). The trusted-write privilege is therefore a slot the overlay grants, not a default (E1 §4).

## 3. Additive-vs-Overlap verdict matrix

Map-vs-decision line: **the substrate governs FACTS-over-time; cav2 governs AUTHORITY / DECISIONS / PROMOTION.**

| Substrate mechanism (E2) | Verdict | Why |
|---|---|---|
| Two-loop (fast deterministic read / slow model write) | **ADDITIVE / orthogonal** | execution-tier split governs latency/determinism, not who-may-assert; cav2 sits on top of the slow loop's write step (E2 §1, p.1–7) |
| Property graph + per-edge `confidence`/`utility_score` | **MIXED: OVERLAP on fact-shape/confidence, ADDITIVE on authority-typing** | schema enforces fact shape (don't rebuild); but no `authority_kind`/`decision_id`/`promotion_stage`/`owner` field exists (E2 §2, p.2–3) |
| Temporal-truth: validity windows + non-destructive supersession + `asOf` + stale | **OVERLAP — cav2 must NOT rebuild** | substrate owns truth-validity of an atomic fact; `validity_end` answers "still true?" not "canonical/promoted/who-decided?" (E2 §3, p.7,11) |
| Dream-state consolidation (REPLAY/PRUNE/LUCID supersede·merge·annotate via Bonsai) | **MIXED: OVERLAP on factual-contradiction resolution, ADDITIVE on decision-as-object** | adjudication is model-driven, per-contradiction, on FACTS — no constitution, no decision ID, no rationale ledger, no authority override (E2 §4, p.4,7) |
| Self-model "I don't know" percolation gate | **ADDITIVE / orthogonal** | coverage/abstention keyed on graph density (epistemic sufficiency), not authority sufficiency; composes WITH a promotion gate (E2 §5, p.4,11) |
| Chat-vs-code profiles | **ADDITIVE / orthogonal** | parameterizes ingestion mechanics, no knob for tiers/review/promotion (E2 §6, p.7–8) |

**Bottom line (E2):** redundancy risk is real but bounded to the temporal-fact lane. cav2 is orthogonal/additive **provided it reads** `validity`/`confidence`/`utility` rather than duplicating them, and **writes** the authority dimension the substrate has no field for (E2 bottom line, p.3,7).

## 4. Build-from-owned labels

**REUSE (build-from-owned):**
- *Their* Review Queue surface + `decide_review` approve/reject/escalate vocabulary + `promote_review_artifact` — map onto, do not re-invent (E1 §4 caveat 3; E3 §A "Promotion lifecycle").
- *Our* owned assets: inventory (candidate store), authority-triage front door, capture harness — these are existing cav2 capabilities the overlay composes (E3 §A rows "Inventory", "Authority-triage front door"; §B explainer).
- Authority Kinds + Narrowest-Owner Rule — ADOPTED as-is onto routing behind the queue (E3 §A).

**Important (S1 precedent correction): the genuine net-new surface is SMALLER than a first read suggests — it reduces to four atoms; everything else is build-from-owned.** The vocabularies (scope-tags, governance fields, authority kinds) and the stores (inventory) are all OWNED — only their *mechanical separation / indirection / host-side body* is net-new:

**Genuine NET-NEW atoms (none built):**
- **(a) Host-resident trusted-write provider BODY** behind resonantOS's already-named `promote_review_artifact` / 501 boundary (their owned *contract*; ours is only the provider body — see §5).
- **(b) Port indirection** — free hard-coded `.arcanum/` paths so the store is host-pluggable. (This single atom subsumes any "port-aware classifier mode" — the authority-triage classifier itself is owned; only the indirection is new — so it is NOT double-counted.)
- **(c) Per-runtime scope-tag adapter shims** — the scope vocabulary (`user-memory`/`project-instructions`/`runtime-rules`/`knowledge-store`) is OWNED cav2; net-new is ONLY the per-runtime adapter shims that stamp it at `archive-intake-write`.
- **(d) The b1/b2 store-boundary REFACTOR** of an already-owned inventory — inventory + its governance fields (`promotion_owner`/`trace`/`residue`/kind/status) are OWNED (inventory sigil + AUTHORITY-MODEL Core Flow); net-new is ONLY the mechanical separation of a portable b1 store from the b2 governance overlay, not the store or the fields themselves.

## 5. Critical claim ≤ proof correction (E1 caveat 1)

**Honest status — do not overclaim a turnkey drop-in.** The portable example service **explicitly refuses** every promotion op: `providerOnlyOperations` returns **HTTP 501** on `process-ingest-request`/`decide-review`/`promote-review-artifact`, reason "Trusted wiki writes require Strategist-owned ingest/review inside the desktop host" (E1 §3, memory-service L65–72, L135–147; test L123–128 confirms 501 + "full ResonantOS host provider"). Policies pin `canWriteKnowledgePages:false` (manifest L128; `policies.ts:47–49`).

Therefore the promotion/trusted-write executor is **host-resident and ABSENT from the example code**. The boundary is sharp (S1 precedent): the `promote_review_artifact` **contract, tool name, proxy boundary, and 501 reason string are resonantOS's owned assets** — CyberAlchemy supplies only the **provider BODY behind their already-named seam**, not the whole promotion seam (E1 §3; E1 caveat 1). Precise status:
- **Built + tested:** the read + intake + review-queue seam (E1 net: SUPPORTED).
- **Contract only (their contract, our body):** the promotion executor is named end-to-end by resonantOS as a tool surface that 501s; the trusted-write *implementation behind that named boundary* is the piece cav2 supplies (E1 net: PARTIALLY-SUPPORTED).

## 6. Dogfood value

Running resonantOS as the **first host** generates the governed-run data that builds the SDK — build-from-owned at the system level: the integration is not just a deployment, it is the data source for the governance SDK we are trying to ship (dispatch context).

## 7. Residue / open (honest)

- **Host-side trusted-write provider — UNBUILT.** The piece behind the 501 boundary is contractually named but has no implementation in the example repo; cav2 must supply it (E1 caveat 1).
- **Scope-tagged adapters — UNBUILT.** Concept is owned (cav2 scope-tags); the per-runtime shims/adapters do not exist (E3 §A slice 2).
- **b1/b2 store split — UNBUILT.** The generic-vs-governance store separation is designed, not coded (E3 §A slice 3).
- **Port indirection — UNBUILT.** Hard-coded `.arcanum/` paths still bind the store (E3 §A slice 1).
