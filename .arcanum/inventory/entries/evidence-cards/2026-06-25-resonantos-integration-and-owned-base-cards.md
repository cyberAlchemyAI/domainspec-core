---
tags: [inventory, resonantos, living-archive, cav2, integration, importance, govern-importance, build-from-owned, claim-le-proof, boundary, evidence-card]
node_type: evidence-card
is_session: false
layer: architecture, governance, market
nature: reference
status: candidate
created: 2026-06-25
sources:
  - development/resonantos-integration/findings.md
  - development/resonantos-integration/RESONANTOS-INTEGRATION-GUIDE.md
  - development/resonantos-integration/research.md
  - development/resonantos-integration/owned-base/findings.md
  - development/resonantos-integration/owned-base/BASE-FOR-VICTOR.md
  - development/resonantos-integration/owned-base/research.md
  - resonantos-vnext/public/addons/living-archive.json
  - resonantos-vnext/examples/living-archive-mcp.mjs
  - resonantos-vnext/src/core/policies.ts
  - "Agent Memory Architecture v7.1 (PDF, Victor Morrow)"
  - arcanum/spells/necronomicon/README.md
  - arcanum/arcana/inventory/
---

# Evidence Cards — resonantOS Living-Archive Integration + Owned Base + Importance

Candidate Inventory read models from two closed research dispatches
(`2026-06-24-resonantos-living-archive-integration`,
`2026-06-24-resonantos-owned-base-and-importance`). Promotion owners = the SDK/integration
decision-gate / cav2 authority owner / sigil-development. These cards promote nothing.

## `living-archive-write-seam`

- ID: `living-archive-write-seam`
- Status: candidate
- Claim: resonantOS's Living Archive is the **textbook host that already owns a memory
  substrate** — so CyberAlchemy does NOT reimplement inventory; it layers governance on the
  WRITE side. **READ decouples, WRITE doesn't.** The addon manifest exposes the exact seam:
  `archive-read` + `memory-provider` (READ → back capture/lookup), and `archive-intake-write`
  (scope `intake-only`) + the `living-archive-review` **Review Queue** ("review memory intake
  and promotion requests before trusted writes") + `decide_review`(approve/reject/escalate)/
  `promote_review_artifact` (WRITE/decision → where cav2's governed store + promotion lifecycle
  plug in). The READ map stays host-owned; the governed store + decisions are the adopted value.
- Source refs: `resonantos-vnext/public/addons/living-archive.json` (caps L26–53; surfaces
  L10–23); `examples/living-archive-mcp.mjs` (READ search/read; write_intake/request_ingest;
  decide/promote); `development/resonantos-integration/findings.md` §2.
- Authority level: candidate (code-cited, both skeptics + auditor accepted).
- Promotion owner: SDK/integration decision-gate.
- Trace: dispatch 2026-06-24-resonantos-living-archive-integration, E1 seam map.
- Residue: see `promotion-executor-host-resident`.

## `promotion-executor-host-resident`

- ID: `promotion-executor-host-resident`
- Status: candidate
- Claim (claim≤proof correction): the **trusted-write / promotion executor is host-resident and
  ABSENT from the example code** — portable services return HTTP 501 on
  process/decide/promote ("Trusted wiki writes require Strategist-owned ingest/review inside the
  desktop host") and policy pins `canWriteKnowledgePages:false`. So the read+intake+review-queue
  seam is built+tested, but the promotion executor is a **contractually-named attach-point cav2
  must IMPLEMENT** (the provider BODY behind resonantOS's owned `promote_review_artifact` /501
  boundary), **not a turnkey drop-in to wrap**. The contract/name/proxy/501 are THEIR owned asset.
- Source refs: `examples/living-archive-memory-service.mjs` (providerOnlyOperations L65–72, 501
  L135–147); `*.test.mjs` L123–128; `src/core/policies.ts:47–49`; manifest L128;
  `development/resonantos-integration/findings.md` §5.
- Authority level: candidate (non-vacuity skeptic verified by hand).
- Promotion owner: SDK/integration decision-gate.
- Trace: E1 caveat 1; S2 witness round-trip.
- Residue: external-source line cites not re-verified in domainspec-core.

## `additive-vs-overlap-facts-vs-authority`

- ID: `additive-vs-overlap-facts-vs-authority`
- Status: candidate
- Claim: the **map-vs-decision line**. The Living-Archive substrate governs **facts-over-time**
  (temporal validity windows + supersession, dream-state contradiction resolution, self-model
  "I don't know") — cav2 must NOT rebuild these (**OVERLAP**). It has **no field** for
  authority/decisions/promotion (`confidence`≠canonicality; adjudication writes a mutation, not a
  decision-with-ID/owner/rationale) — that is the clean **ADDITIVE** gap cav2 fills. Non-redundant
  at the schema level (nothing to collide with): cav2 writes an authority dimension the substrate
  has no column for, reading `validity`/`confidence`/`utility` rather than duplicating them.
- Source refs: "Agent Memory Architecture v7.1" (pp.1–8); `development/resonantos-integration/findings.md` §3.
- Authority level: candidate synthesis (PDF-cited).
- Promotion owner: cav2 authority owner.
- Trace: E2 fact-vs-authority partition; S2 schema-level non-redundancy check.
- Residue: bounded to the temporal-fact lane; PDF scoring is spec-not-shipped.

## `owned-arcanum-base-blueprint-with-validators`

- ID: `owned-arcanum-base-blueprint-with-validators`
- Status: candidate
- Claim: the concrete OWNED base we can hand a host engineer is a **governance blueprint with
  validators, NOT a shippable memory service**. Three honest tiers: **COPY-THIS (runnable)** =
  inventory evidence-card/EvidenceSet **schemas** (`promotion_owner`, authority-state, provenance,
  trace, residue) + bash/jq **validators** + **arcanum-bootstrap** installers; **PORT-THE-DESIGN
  (markdown)** = necronomicon NO-PROMOTION guardrail + gap-ledger + receipt-debt + restraint-floor,
  definitions-governance, ontology-vault; **YOU-ALREADY-HAVE-THIS** = the host's Review-Queue loop
  (already IS necronomicon's intake→classify→promote) + its recall-importance machinery. The SDK
  is "just a plan" until ported; most arcanum content is LLM-executed skill prose, not code.
- Source refs: `arcanum/arcana/inventory/` (schemas+validators); `arcanum/spells/necronomicon/README.md`;
  `arcanum/tools/{install,bootstrap}_arcanum.sh`; `development/resonantos-integration/owned-base/findings.md` §2,§5.
- Authority level: candidate (E1 harvest; both skeptics verified runnable-vs-design on disk).
- Promotion owner: SDK/integration decision-gate / arcanum-bootstrap.
- Trace: dispatch 2026-06-24-resonantos-owned-base-and-importance, E1 + S2.
- Residue: necronomicon↔Review-Queue match is structural, not demonstrated end-to-end.

## `two-senses-of-importance`

- ID: `two-senses-of-importance`
- Status: candidate
- Claim (answers "how does it decide what is important?"): there are **two different
  importances**. (1) **RECALL-importance** — what to surface/keep/prune — the Living Archive
  ALREADY solves it (per-edge `utility_score`, JEPA relevance, the **Aspirational Model** =
  directional "what the agent WANTS to know", Self-Model density gate); telling it what to recall
  is **REDUNDANT**. (2) **GOVERN/promote-importance** — "may we RELY on / promote this?" — the
  non-redundant gift, realized as the **evidence-confidence vs commitment-confidence** split
  ("high evidence, low commitment: true but not strategically important") + **authored /
  provenance-weighted priors** that override low statistical mass + **authority over the
  thresholds**. It **FEEDS** the existing salience signals, never replaces them. Both axes
  compose; neither subsumes the other.
- Source refs: "Agent Memory Architecture v7.1" (pp.3–8, Aspirational Model p.4);
  `arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md` (confidence split:164–177);
  `development/resonantos-integration/owned-base/findings.md` §4.
- Authority level: candidate (E2 formal + E3 design; S2 composition witness on a net-new low-mass concept).
- Promotion owner: cav2 authority owner / SDK decision-gate.
- Trace: E2 recall-redundant / E3 govern-additive; the non-redundant axis = authored top-down priors.
- Residue: govern-importance runtime unbuilt on BOTH sides (substrate scoring is spec/placeholder).

## `authority-triage-private-boundary`

- ID: `authority-triage-private-boundary`
- Status: candidate
- Claim (boundary, radical candor): **`authority-triage` is PRIVATE** — it lives at repo-root
  `development/authority-triage`, **NOT** in public `arcanum/`; only its evidence-card residue
  surfaces under `arcanum/.arcanum/inventory/entries/`. It must NOT be handed to an external host
  engineer by name or source. The **public-safe analog** for "triage the authority of a knowledge
  claim" = the inventory **evidence-card authority-state + `promotion_owner`** model +
  definitions-governance drift audit. The teammate handoff (`BASE-FOR-VICTOR.md`) uses the public
  analog; the auditor confirmed `authority-triage` is absent.
- Source refs: `development/authority-triage/` (private); `arcanum/arcana/inventory/`;
  `development/resonantos-integration/owned-base/findings.md` §3.
- Authority level: candidate (E1 boundary catch; auditor verified absence).
- Promotion owner: cav2 authority owner (public/private boundary).
- Trace: E1 radical-candor correction; carried into the boundary scrub.
- Residue: prior `RESONANTOS-INTEGRATION-GUIDE.md` leaned on authority-triage by name — superseded by the public analog.
