# Research Result - Capital Logic Library

- Run: `2026-06-12-craft-pipeline-hydration`
- Dispatch: `gq-research-strategy-capital-logic-library-2026-06-12`
- Mode: LOCAL-FIRST research execution (external research DEFERRED, gate rg03 not authorized)
- Role lenses covered: local-evidence-reviewer (r01-r02), external-boundary-reviewer (r03-r04), claim-validation-reviewer (r05-r06)
- Overall verdict: **PASS** (all claims map to a local source class + concrete path; no loose claims; no external pass executed; owner boundary held)

## Node

- Craft node: `capital-logic-library` (CTX-CLL-ROOT)
- Title: Capital Logic Library
- Research lane: Capital Logic Library research
- Owns: workbook Workstream D (Capital Logic Content); links to (does not own) the root promotion-governance Craft ledger.

## Core Question

What source universes, expert inputs, card schema evidence, and rule-pack boundaries are needed to hydrate launch cards safely?

### r01 Scope (node-specific; cross-node drift rejected)

The question is bounded to **Workstream D — Capital Logic Content** only. Adjacent workbook workstreams are explicitly OUT of this node's research scope and belong to sibling nodes:
- Posture system / Sanitization / Vault / classification (Workstream B) → tilth-runtime-build / hardware nodes.
- Claims register, guardrails-as-tests (Workstream C) → quality-security-proof node.
- Sales/segment framing (Workstream E), white-glove (Workstream F) → sales / white-glove nodes.
This node researches: **card schema + governance, five launch cards + expert review, search seed libraries / source universes, recurring funder rule packs.** Anything outside those four is cross-node drift and is not answered here.

## Findings

Each finding cites a source class and a concrete local path/handle. No external sources were consulted.

- **F1 — Workstream D scope is confirmed local-and-bounded.** Capital Logic Content = (a) card schema + governance, (b) author/validate five launch cards, (c) search seed libraries + source universes per segment, (d) program rule packs for recurring funders. Source class: workbook-handoff. Path: `docs/golden-quill-task-role-breakdown-handoff.md` (Workstream D rows, lines 62-65); echoed in `docs/features/capital-logic-library/.craft/ledger.yml` DESC-CLL-001.

- **F2 — Card schema + governance is local-buildable now (no external input needed).** Task is "Card schema + governance: structure, section-level defaults, testability rules," role Founder + Backend Engineer (Josh + Vlad), effort BUILD. Source class: workbook-handoff. Path: `docs/golden-quill-task-role-breakdown-handoff.md` line 62. No gap is filed against schema — it is a build task, not a research gap. Note: the broader CIC/CLC card architecture (Eight Capital Logic Cards, orthogonality rule) lives in canonical project governance (CLAUDE.md project instructions) and is OWNER-BOUNDARY-protected — this research does not mutate it.

- **F3 — Launch-card status is the active inventory gap (GAP-CLL-LAUNCH-CARDS, flag).** "Author & validate five launch cards (Farmer v1; four in authoring) with paid expert review." Current state captured: one card (Farmer) at v1; four cards in authoring. Source class: workbook-handoff. Path: `docs/golden-quill-task-role-breakdown-handoff.md` line 63; ledger `gaps[0]` (`GAP-CLL-LAUNCH-CARDS`, treatment=inventory, owner=founder). Local evidence states authoring status but does NOT enumerate per-card current authoring/validation status — that capture is the gap's open work, answerable locally from founder knowledge (Josh input), not from the web.

- **F4 — Domain-expert input is the blocking gap (GAP-CLL-DOMAIN-EXPERTS, block).** Four segment experts needed for "structured input + field correction on Educator, Municipal, Arts, Cooperative cards," onboard form = "Contract, paid structured input," role currently unfilled (—). Source class: workbook-handoff. Paths: `docs/golden-quill-task-role-breakdown-handoff.md` line 63 ("paid expert review", "onboard NOW") + Roles & Gaps line 113 (Domain Experts ×4 segments, "Contract, paid structured input"); ledger `gaps[1]` (treatment=onboard, severity=block, owner=founder). This is an **onboarding/contracting** action owned by Josh, NOT a research lookup — paid expert input cannot be substituted by external web research.

- **F5 — Rule packs need an ownership + maintenance shape (GAP-CLL-RULE-PACKS, flag).** "Program rule packs for recurring funders (codified hard requirements)," effort BUILD + ONGOING, role Founder + Backend Engineer (Josh + Vlad). Source class: workbook-handoff. Path: `docs/golden-quill-task-role-breakdown-handoff.md` line 65; ledger `gaps[2]` (treatment=plan, owner=founder-backend). The ONGOING marker means this gap needs a maintenance-ownership decision (who keeps packs current), which is a local planning decision. The *content* of specific funder rules is where a future bounded external pass could apply — see external decision.

- **F6 — "Search seed libraries + source universes per segment" is a founder-owned local build, with a latent external comparison need.** Task role = Founder (Josh), effort BUILD. Source class: workbook-handoff. Path: `docs/golden-quill-task-role-breakdown-handoff.md` line 64. No standalone gap is filed for it (it is folded under the node's purpose, ledger CTX-CLL-ROOT). The *enumeration* of segment source universes is the one place where external comparison could add value once Josh approves — this is the named external trigger, not a current local blocker.

- **F7 — After-Acceleration horizon confirms cards are an evolving, expert-bench-dependent line, not a one-shot.** "Capital Logic Library: Outcome-data opt-in pipeline; anonymized pattern feedback into cards; offline refinement; new cards & extensions; expert bench expansion." Source class: workbook-handoff. Path: `docs/golden-quill-task-role-breakdown-handoff.md` line 93. This frames the domain-expert gap (F4) as recurring (bench expansion), reinforcing block severity, and is out-of-scope-for-now (post-acceleration horizon).

- **F8 — Promotion-governance ownership boundary is explicit and must be preserved.** The node "links to existing promotion-governance Craft state" and "must not mutate canonical Golden Quill architecture... or promotion-governance state." Source class: node-craft + seed. Paths: `docs/features/capital-logic-library/.craft/ledger.yml` (REL-CLL-PROMO-GOV depends_on_existing_ledger; notes lines 7-9) + `.../REFINE-SEED-PROPOSAL.md` Write Scope (line 26). Research output here is planning evidence only.

## Lane Map (per active gap)

| Gap | Severity | Lane | Rationale + source |
| --- | --- | --- | --- |
| `GAP-CLL-LAUNCH-CARDS` | flag | **local-only** | Per-card authoring/validation status is captured from founder knowledge (Josh) + existing card artifacts; no external input required. Source: handoff line 63 + ledger gaps[0]. |
| `GAP-CLL-DOMAIN-EXPERTS` | block | **deferred (onboarding action, not research)** | Resolution = contracting four paid segment experts (Educator/Municipal/Arts/Cooperative). This is a founder onboarding decision, not a web-research task. Source: handoff lines 63, 113 + ledger gaps[1]. |
| `GAP-CLL-RULE-PACKS` | flag | **local-only for ownership/shape; gap-triggered-external for specific funder rule content** | Ownership + maintenance cadence is a local planning decision (Josh + Vlad). The actual codified hard requirements for named recurring funders is the bounded external trigger if Josh approves. Source: handoff line 65 + ledger gaps[2]. |
| (latent) source universes per segment | n/a (no filed gap) | **gap-triggered-external** | Enumerating segment source universes could benefit from a bounded external comparison pass after approval. Currently a founder-owned local build (handoff line 64). |

## External-Research Decision

**DECISION: DEFERRED — pending operator (Josh) approval (gate rg03).** No web search, WebFetch, or external lookup was executed in this run. The following are the bounded external classes that specific named gaps would trigger IF Josh approves a later pass:

1. **Segment source-universe lists** — triggered by the latent "source universes per segment" need (F6) and to validate launch-card segment coverage (Educator/Municipal/Arts/Cooperative/Farmer). Bounded scope: public funder-directory and segment-source enumeration only. No client org data.
2. **Recurring funder rule references** — triggered by `GAP-CLL-RULE-PACKS` (F5) for the *content* side: codified hard requirements (eligibility, format, deadlines) of named recurring funders, to seed rule packs. Bounded scope: public RFA/program-page text only.
3. **Paid expert input requirements** — triggered by `GAP-CLL-DOMAIN-EXPERTS` (F4): scoping what a paid structured-input engagement for the four segment experts should require. Bounded scope: external comparison of expert-engagement scope norms; the actual hire/contract remains a founder action, not research.

Org isolation (gate rg04) holds across all three classes: none would read any client org PROJECT_CONTEXT under `orgs/`.

## Residue

- **Open blocker:** `GAP-CLL-DOMAIN-EXPERTS` (block) is unresolved and is an onboarding/contracting decision Josh must make; research cannot clear it.
- **Open data gap:** per-card current authoring/validation status (Farmer v1 + four in authoring) is asserted at the aggregate level in the handoff but not enumerated per card locally — needs Josh's capture to close `GAP-CLL-LAUNCH-CARDS`.
- **Open decision:** rule-pack maintenance ownership (who keeps recurring-funder packs current under the ONGOING marker) is undecided.
- **Deferred-external residue:** three bounded external classes listed above await Josh's explicit gate-rg03 approval before any external pass runs.
- **Boundary note:** canonical CIC/CLC card architecture (project CLAUDE.md) and root promotion-governance ledger are owner-boundary-protected; this run did not touch them.

## Next Move

Hand the node back to its Refine route. Recommended single next move: **present the three deferred external-research classes to Josh for an approve/defer decision, and in the same pass have Josh (a) enumerate per-card status to close GAP-CLL-LAUNCH-CARDS locally and (b) decide rule-pack maintenance ownership.** Only the domain-expert contracting (block) requires a separate founder onboarding action outside the research lane. No runtime stage, subagent, or external pass should run until that approval lands.
