# Lane-designer subagent receipts (ledger: lane-designer-receipts)

Two approved role-bound subagents (tournament parallelism, join parent_synthesis). Both completed
and closed. Receipts summarized; full findings folded into the distill below.

## Receipt — existing-tools-lane-designer (Lane A)

- **Definition:** install the 4 layers on the client's current stack (ERP/TMS, spreadsheets, BI tool,
  email); no new platform. Boundary: no runtime deterministic gates, no agent-runtime enforcement.
- **Layer mapping [SB ontologize design]:** ontology cards = governed spreadsheet tabs (subject/mechanism
  - matching-rules tab); classification register = access-controlled signed sheet (manual hash, fail-closed
    default = restricted); promotion DAG = append-only event/observation/candidate/decision/projection tables
    (the 6 node types as tables; 11 rules as data-validation + formula checks + manual review); BI = dashboard
    measures with documented denominators + evidence-linked receipt sheet; agents = documented routing rules
    (advisory, not enforced).
- **Cost/capability/sovereignty:** high sovereignty (data stays put), low adoption lift, modular, ~12wk/vertical;
  hard limits = gates advisory not fail-closed, manual evidence composition, spreadsheet ceiling ~10k events/mo,
  weekly/monthly promotion cadence.
- **Wins when:** data-sovereignty required, SMB scale, ERP/TMS exportable, ops lead available, fast PoC, agents deferred.
- **Residue [H]:** run boundary, event catalog, proof metric (assessment); ERP/TMS sync method; DB vs sheet for >10k events.

## Receipt — arcanum-substrate-lane-designer (Lane B)

- **Definition:** install the 4 layers on Arcanum's own sigils — `inventory` (ingest/index/lint/lookup),
  `ontology-vault` (roles/confidence/premises/promote-confidence/branch-aware), `context-builder`
  (selector-evidence + obligation-linked handoff). Boundary: only what the sigils natively provide.
- **Layer mapping [SB skill paths]:**
  - Ontology cards → ontology-vault `map --branch business` roles/axes/edge-rules + inventory entity/concept entries. [SB]
  - **Classification register → NO native match (HARD GAP).** ontology-vault has descriptive "source authority
    rules" only; would need a custom `classification-record` entry type + lint bridge. [H]
  - Promotion DAG → inventory evidence-cards/EvidenceSets (state, source_refs, promotion_owner) + ontology-vault
    `distill-sessions` (promotion candidates) + `promote-confidence` (owner decision, falsification, blocks
    premature promotion) + inventory `lint` (the 11 rules instantiated as custom checks). [SB with gaps]
  - BI + agents → inventory `lookup`/`query` + context-builder obligation-covered handoff packs feed agents;
    no native dashboard UI; no proof-harness for metric-drift-over-time. [SB with gaps]
- **What Arcanum adds:** governed promotion with deterministic lint, audit-immutable source spine,
  evidence-linked context for agents, branch-aware business↔system drift, baked-in cross-sigil pipeline.
- **Cost/capability/sovereignty:** strong governance + sovereignty (stays in client's Arcanum instance);
  hard limits = adoption curve, text-first (no native BI dashboard), Layer-2 gap, no time-series/proof-harness,
  no native reflection cadence.
- **Wins when:** governance/auditability is the point, agent-first ops, willing to adopt harness discipline,
  intent↔implementation drift matters, privacy-sensitive, low BI-UI demand.
- **Residue / bridges needed [H]:** Layer-2 signed register; runtime event→card dispatch; the 11-rule lint
  schema; proof-harness/metric-drift; reflection cadence (e.g., scheduled distill-sessions).
