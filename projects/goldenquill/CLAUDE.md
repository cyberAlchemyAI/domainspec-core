# Golden Quill — Claude Instructions

You are working inside the Golden Quill workspace. Josh is the sole operator. Before taking any action, run the workspace wake-up sequence in `/AGENTS.md` (read SOUL.md → USER.md → router.yaml → last two daily_logs → lessons.md → MEMORY.md index → agent-specific overrides → task-specific PROJECT_CONTEXT). This CLAUDE.md is a Cowork-specific supplement — it does not replace the workspace files and must not be read alone.

## Who Josh Is

Solo builder. 25+ years project management in skilled trades and workforce development. Co-founder of MycoSymbiotics Cooperative. Founder of FIT Farms. Has won three competitive grants in 2026 using his existing Claude skills. He knows what he's doing.

**Josh does not code.** He uses Cowork (Claude desktop app), not Claude Code CLI. He cannot write or run code himself. Any technical setup must be done BY Claude through available tools (osascript, bash sandbox, file tools). He will run terminal commands as a last resort

## How to Work with Josh

- **Answer the question he asks.** Do not redirect his focus. Do not lecture about priorities or deadlines. He sets the agenda.
- **Dialogue over deliverables.** Do not dump files on him unless he explicitly asks for a file. Think out loud, propose, let him steer.
- **Ground yourself in existing docs before proposing anything.** The handoff folder, memory files, and skills already contain extensive decisions. Read before suggesting.
- **Push-back is welcome** — but constructive, not redirecting. He will override you hard when you're wrong. Don't sandbag for politeness.
- **When he says build, he means build** — but "build" means Claude does the technical work, not Josh typing into a terminal.
- **He underspecifies intentionally.** He wants you to interrogate and think, not execute blind.

## The Product Naming Chain: Golden Quill · Tilth · Cultivator · Sovereign Node

Canonical naming per `memory/project_sovereign_node_stage5.md` (updated 2026-05-06).

**Golden Quill** = the physical hardware product. A 128 GB desktop supercomputer in a custom gold protective case — reference SKUs today are the **Apple M3 Ultra Mac Studio**, the **AMD GX-10** class, and the **NVIDIA Spark** (DGX Spark / ASUS Ascent GX10). What the client buys and owns. One Golden Quill per client. *(Earlier 64 GB and 32 GB references in prior docs are stale — 128 GB is the canonical floor.)*

**Tilth** = the agentic software intelligence running inside one Golden Quill. Named for the condition of soil prepared for growing. Tilth is the six-seat AI council (Scout, Scribe, Editor, Judge, Red Team, Logician) plus a small set of support agents (Intake, Uploader for v0.1; Data Collector and Report Generator for v0.2 horizon; Archivist for v1.x horizon), the Cedar policies, the Five Operating Laws, the admin-risk register, the classification register, the entire grant intelligence stack. One Tilth per Golden Quill.

**Cultivator** = the per-employee phone interface (Telegram-bot in v0.1). Voice, photo, and text capture that feeds each employee's slice of Tilth. Per-employee layer, not per-machine.

**Sovereign Node** (no LLC) = the future cooperative-owned compute commons. The role formerly called "MaatAI" — coordinates opt-in cross-Tilth signals at member-set consent tiers, holds deeper corpus. **Stage 5 only — out of scope for v0.1, v1, v1.x.** Internal term until Stage 5 is an active build. **Not a nickname for individual Golden Quills.** Never appears in customer-facing v1 / v1.x materials.

**Sovereign Node LLC** (with LLC) = stale/provisional entity language in older docs. It is not the current operating legal entity for v0.1. Today, **FIT Farms LLC** is the real legal entity and **Golden Quill** is its project. When the project spins out, a new LLC can be formed and the docs should be updated then.

**Disambiguation rule:** "FIT Farms LLC" = current operating legal entity. "Golden Quill" = the project/product. "Sovereign Node" (no LLC) or "Stage-5 Sovereign Node" or "the Sovereign Node commons" = Stage-5 commons infrastructure (future). Do not present "Sovereign Node LLC" as a currently active legal entity unless Josh explicitly updates the entity posture. ("MaatAI" retired as a name 2026-05-06; replace any surviving reference with "Sovereign Node" in the Stage-5 sense.)

**"One Sovereign Node, Many Tilths."** Stage-5 positioning only. Each Tilth stays sovereign on its Golden Quill; cross-Tilth sharing exists only if the client opts in (consent tiers: my-eyes-only / matchable-to-opportunities / composable-with-others).

**Messaging tagline (current):** *"A cooperative of member-owners, sharing only what they choose, on the terms they set."*

**Five-stage product arc:** Stage 1 Solo operator (v0.1, current build — one Tilth, Josh's) → Stage 2 Twelve Tilths (12-deployment fleet milestone — proves the model at small-fleet scale; each Tilth is a separate client's Golden Quill; Cultivator reaches multi-seat per Tilth; Law 3 isolation tested across the fleet) → Stage 3 Cooperative org (multi orgs share hardware tier, Law 3 extended) → Stage 4 Contractor federation (independent operators, each own Golden Quill, selective shared posture) → Stage 5 Sovereign Node commons online (cooperative-owned compute; cross-Tilth network effect engages per consent tier).

**Brand line:** "Golden Quill — regenerative grant intelligence."

**Six Customer Identity Categories** *(canonical naming per drawing TILTH-CIC-REVIEW-01, 2026-05-08; supersedes the prior "six-sector scope" at the customer-facing layer; full per-category card files live at `assets/cards/customer_identification/`):*

1. **Food Systems** *(TILTH-CIC-01 — "Seasonal multi-activity funding world")* — seasonal production, processing, distribution, and access work. *Includes:* farms and growers; value-added processors; distributors and hubs; education and outreach; food access programs; markets and direct sale. *Coverage axis:* Production.
2. **Educator** *(TILTH-CIC-02 — "Compliance-dense learning institution")* — compliance-dense learning institutions and education programs. *Includes:* school districts, charters, and education nonprofits; classroom and program delivery; board governance; state and federal oversight. *Coverage axis:* Learning.
3. **Public Agency** *(TILTH-CIC-03 — "Public-accountability funding environment"; clearer alternative to "Municipal Steward")* — public-sector funding environments with procurement and accountability. *Includes:* local governments and public authorities; budgets and capital plans; procurement and vendor rules; public meetings; cross-department coordination. *Coverage axis:* Public Sector.
4. **Arts & Culture** *(TILTH-CIC-04 — "Merit-plus-sustainability funding world")* — artistic-merit and organizational-sustainability funding world. *Includes:* cultural organizations and artists; performances and exhibitions; programming and engagement; creative production; institutional and independent practice. *Coverage axis:* Culture.
5. **Cooperative** *(TILTH-CIC-05 — "Member-governed ownership system"; simpler name, was "Cooperative Lead")* — member-owned enterprises and democratic governance systems. *Includes:* worker and producer co-ops; member ownership; democratic governance; shared infrastructure; community wealth and reciprocal funding. *Coverage axis:* Member Ownership.
6. **Ecosystem Intermediary** *(TILTH-CIC-06 — "Portfolio-scale ecosystem connector"; clearer alternative to "Capital Intermediary")* — portfolio-scale support organizations and capital connectors. *Includes:* accelerators and incubators; fiscal sponsors; CDFIs and capital connectors; technical assistance providers; coalition and portfolio support organizations. *Coverage axis:* Intermediary Infrastructure.

**What these categories change in Tilth** *(operational primitives — each customer world configures all five):* Search Vocabulary · Evidence Schema · Language Register · Reporting Rhythm · Capital Logic Activation. Each card carries a four-quadrant operational profile (Operating Reality · Tilth Configuration · Evidence Signals · Funding/Reporting Rhythm) that downstream Tilth components must read.

**Frame:** *One system. Multiple funding grammars.* "Together these six customer worlds configure Tilth's search, evidence, drafting, reporting, and capital logic."

## The paired taxonomy: Capital Logic Cards (Eight)

Customer Identity Cards tell Tilth *what world the applicant operates in* (applicant-side). Capital Logic Cards tell Tilth *why and how funding may flow* (funder-side). The two taxonomies are **orthogonal** — any (CIC × CLC) pair is reachable in principle. The opportunity drives which CLC engages, not the customer archetype. A school can absolutely tap a Catalytic Change foundation grant; a farm can tap Sponsorship & Corporate Support; a cooperative can tap Public Purpose & Works. Eight CLCs per drawing TILTH-CLC-00 (`assets/cards/capital_logic/Capital Logic Cards.png`):

1. **Public Purpose & Works** — mandate, eligibility, civic-benefit, public-works funding (USDA RD, EPA, EDA, state agencies)
2. **Catalytic Change** — transition, innovation, demonstration, systems-change funding (foundations, innovation funds, climate funds)
3. **Operating Capacity** — staffing, systems, equipment, readiness funding (capacity grants, operating support, equipment, planning)
4. **Research & Evidence** — inquiry, evaluation, pilots, proof-building funding (SARE, AFRI, evaluation grants, university partners)
5. **Market Access** — buyers, channels, commercialization, demand funding (VAPG, SBA, market development, Build to Scale)
6. **Credit & Underwriting** — loans, guarantees, repayment, finance-readiness funding (CDFIs, SBA lending, USDA loans, revolving funds)
7. **Sponsorship & Corporate Support** — corporate sponsors, gifts, partnerships, brand-aligned funding (corp sponsorship, corp foundations, employee giving, cause marketing)
8. **Shared Assets** — cooperative infrastructure, commons, collective-benefit funding (Community Facilities, co-op funds, food hubs, shared-site investment)

**Match logic (opportunity-driven, not archetype-driven):** opportunity encountered → Scout/Logician identify the CLC the opportunity belongs to (funder-side) → applicant's CIC determines the seat configuration that processes it (Search Vocabulary, Evidence Schema, Language Register, Reporting Rhythm — applicant-side) → CLC determines the underwriting logic and example sources (funder-side) → drafted strategy. CICs and CLCs do **not** have hardcoded coupling; runtime matching is per-opportunity.

**No pre-mapped "Primary Capital Logic Activations" on CIC cards.** An earlier draft baked a CIC→CLC subset binding into each card (e.g., Food Systems → Market Access · Operating Capacity · Shared Assets · Research & Evidence). That binding was a category error — it would falsely constrain customer eligibility to a CLC subset and cause Scout/Logician to deprioritize valid opportunities. Removed from CLAUDE.md and memory 2026-05-08 PM. The PNG cards (`assets/cards/customer_identification/*.png`) still display "Primary Capital Logic Activations" footer bands — those bands need to either come off in regeneration, or be relabeled to "Common patterns observed historically — not a constraint" with explicit caveats.

**CLC closed set (resolved 2026-05-08 PM, Josh):** all capital-logic references in any CIC, doc, or material come from the canonical eight CLCs in TILTH-CLC-00. There are no others. "Validation Signals" was an editorial holdover, not a 9th card. "Market Scout / Capacity Builder / Commons Keeper / Knowledge Seeker" on Food Systems' PNG were creative-named aliases of Market Access / Operating Capacity / Shared Assets / Research & Evidence — but with the binding itself removed, the alias question is moot.

Per `memory/project_capital_logic_cards_v9_state.md`, the broader Cards-vs-Cards architectural reconciliation in the architecture-lock layer is resolved at the visual layer (Cards wins) but the §8/architecture-lock formalization is still pending.

**Next-step research — additional pathways (not retired):** the prior 2026-05-08 morning iteration listed four "additional pathways" beyond the six core CICs — Inventor / Scientist / Researcher; Workforce Developer; Conservationist; Tribal / First Nations. TILTH-CIC-REVIEW-01 does not surface them. Per Josh 2026-05-08 afternoon: these will be explored as next steps; they need more research and exploration before a retain/fold/retire decision lands. Treat as active research backlog, not as discarded categories. Do not drop them silently from any internal materials, and do not include them in V1/V1.x customer-facing copy until research lands.

**Sector vs. launch market — open reconciliation:** the prior six-sector taxonomy (workforce / education / regen_ag / urban_ag / land_community / eco_art) is still load-bearing in code (Scribe knowledge-pack sector enum, Scout sector tags, PROJECT_CONTEXT `sectors:` field) and in handoff/build-order docs. Customer archetypes are about *who applies*; sectors are about *what kind of work*. Whether the sector enum retires, persists as an internal taxonomy beneath the archetype layer, or remaps to the new launch-market labels is an open question — do not silently rename in code without operator decision.

## Operating Entities: FIT Farms Commons · FIT Farms LLC (two file-naming roles, one legal entity today)

These are **file-naming labels for two distinct roles**, not two legal entities. Both roles are currently filled by Josh's existing for-profit legal entity, **FIT Farms LLC**. Distinct labels keep the roles from crossing wires in the file system.

**FIT Farms Commons** = file label for the **owner / operator role**. The entity that owns the Golden Quill + Tilth + Cultivator stack, signs partner-by-application contracts, ships V1 / V1.x, and — at Stage 5 — becomes a **member-owner** of the cooperative that owns the Sovereign Node commons. The label stays constant across the Stage-1 → Stage-5 governance shift; what changes is that "FIT Farms Commons" stops resolving to FIT Farms LLC alone and resolves to "FIT Farms LLC's member stake in the cooperative." Today, "FIT Farms Commons" resolves to FIT Farms LLC. **No single entity owns the Sovereign Node commons. The cooperative does. Any future Golden Quill spin-off may become a member-owner — not the commons-owner.**

**FIT Farms LLC** = file label for the **grant-writing client role** — the organization Tilth writes grants *for*. Lives under `orgs/` alongside MycoSymbiotics Coop, Mystic Mamas, Run a Muck Farm, and any other client. From Tilth's POV this is just another applicant; Law 3 (Org Isolation) applies — FIT Farms LLC's PROJECT_CONTEXT does not bleed into Tilth's self-knowledge of its own owner.

**Why the split:** Tilth cannot be simultaneously "the product I own" and "the applicant I write grants for" without Law 3 collapsing. Separating the labels lets the same legal entity wear both hats cleanly. The owner-role label ("Commons") is stable across the Stage-5 governance shift; the client-role label ("FIT Farms LLC") is a normal `orgs/` folder whose grant work Tilth handles like any other client.

**Customer-facing copy:** V1 / V1.x materials say "FIT Farms" (plain), matching Josh's existing business identity. "FIT Farms Commons" is an internal file-naming convention and a founder / CDFI / foundation-infrastructure-pitch label. "FIT Farms LLC" inside the workspace means the `orgs/` client folder — it is not a customer-facing label.

## The Five Operating Laws

Non-negotiable. Cannot be overridden by any prompt, skill, or model.

1. **RFA Is the Source of Truth.** Every claim traces to the RFA or PROJECT_CONTEXT. No secondhand descriptions substitute for the actual announcement.
2. **No Boundary Drift.** Stay inside the RFA's defined scope. Do not silently expand scope.
3. **Org Isolation.** One PROJECT_CONTEXT.md per session. Never cross-reference data between orgs.
4. **Apolitical Sector Language + Admin-Risk Term Scanning.** Two axes: (a) funder dialect code-switching (conservative/centrist/progressive/soul-fire), and (b) live flagged-terms register with severity tiers. Never silently rewrite — applicant approves each substitution.
5. **Applicant Brings the Substance.** Do not fabricate credentials, data, or partnerships. Shape existing substance into funder-ready form.

## The Council (Six Seats)

Seats are described by role only. Model bindings live in `/router.yaml` — consult that file for current provider assignments. Never hardcode model names in identity, plan, or memory documents.

- **Scout** — Two-stage discovery. DISCOVER reads the union of six parallel channel families (A Federal APIs — Grants.gov search2/fetchOpportunity, SAM.gov, USASpending; B Curated cached datasets — subscription feeds, prior rosters, seeded foundation spreadsheets; C Seeded state/foundation portals; D Federal program pages; E RSS/newsletter watchlists; F Client-material-driven web search . All six are parallel primary — none is a fallback. VERIFY fetches live synopsis before any candidate is elevated to CRITICAL-fit; assigns VERIFIED_FIT, VERIFIED_NOT_FIT, UNVERIFIED (no live endpoint), or VERIFICATION_FAILED. REVIEW is the human gate. Full spec in `/router.yaml`.
- **Scribe** — Writing. Drafts proposals section by section with KGIE preflight, SMART outcomes, overlooked expenses checklist, funder dialect matching. Beta routing per v7.0.10 LOCKED 2026-05-11: classification-driven per-call decision under one of three deployment postures (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign). Under Split-Context Hybrid (operator-most-common for Confidential-bearing grants), Scribe's scaffold composition routes cloud-frontier on RFA + section structure + dialect keywords only; substance composition routes local; no opaque-slot rendering round-trip. v7.0.7-era slot-fill mechanism deprecated per v7.0.10 §2.
- **Editor** — Clarity. Reads Scribe's draft through different eyes. Flags jargon, offers 2-3 concrete replacement options per issue, sorts goals/outputs/outcomes/objectives. Makes grants accessible to people who know their work but don't write grants for a living.
- **Judge** — Scoring. Evaluates drafts against the funder's own rubric first, then cross-checks related rubrics from the library. Cross-family rigor — Judge must not share provider family with Scribe. High-stakes grants (federal long-form / large award / operator-flagged) trigger an on-demand local heavy Judge — a 200B-class model loaded for the cycle (DeepSeek V3 / Qwen 3 235B-A22B / Mistral Large 2 / GPT-OSS 120B per the current signed Golden Quill router template).
- **Red Team** — Adversarial challenge. Fires on every draft. Cross-family rigor against Scribe and Judge — never shares provider family with either. Disagreement of 10 or more points between Judge and Red Team triggers a council split, and the human decides (Law 4 tie-breaker; boundary inclusive at threshold per §10.6).
- **Logician** — Policy enforcement. Deterministic Python + Cedar validation, not AI. Fail-closed. Enforces all Five Laws as PRE/POST gates. Zero token cost. Cannot be overridden.

No seat outranks another. The applicant decides.

## Support Agents

Beyond the council, Tilth runs a small set of support agents handling work around the grant cycle:

- **Intake** (v0.1, onboarding, always-local) — bulk-ingests organization documents at white-glove setup; extracts candidate facts with verbatim-quote-with-page provenance for operator confirmation; populates the Key Facts Register.
- **Uploader** (v0.1, submission, always-local) — assembles operator-approved final proposal into funder-portal-required formats and stages submission. Prepare-and-stage discipline only — operator clicks final submit on funder portal.
- **Data Collector** (v0.2 horizon, post-award) — outreach to grantees and sub-awardees via email, text, voice; gathers performance data, evidence, milestones. Compliance-first (CAN-SPAM, TCPA, per-recipient consent).
- **Report Generator** (v0.2 horizon, post-award) — generates funder-ready reports from Data Collector's gathered data under the same Logician PRE/POST discipline as council seats.
- **Archivist** (v1.x horizon, between-cycle) — long-running curation of Funder Intelligence Database, Match Database, KFR maintenance and expiry tracking, lessons memory, audit trail.

## Beta Model Strategy — Three-Posture Classification-Driven Routing (v7.0.10 LOCKED 2026-05-11)

Tilth's Beta deployment runs a per-agent-call routing decision under one of **three customer-facing postures** (deprecates the v7.0.7 four-posture-implicit framing; the Sanitized / opaque-slot-token posture is retired):

1. **Frontier-Eligible** — customer permits selected project data to route to external/frontier models. Tilth assigns the strongest available model to each role per benchmark fit. Per-field classification register (public, shareable, confidential, operator_flagged — 4 values unchanged from v7.0.7 §2) drives routing: public + shareable fields route cloud; confidential + operator_flagged remain local (operator override via per-grant SP0 + HIGH-severity admin-risk ledger).
2. **Split-Context Hybrid** — frontier models help with structure, section strategy, prompts, funder-language framing, and generic draft scaffolds (operating only on the operator-signed Split-Context allow-list at `orgs/<slug>/vault/classification/split_context_allowlist.yaml`). Confidential local data stays on the node. A local model inserts restricted facts, evidence, metrics, names, and applicant-specific substance separately. *No opaque-slot rendering round-trip*.
3. **Local-Only / Sovereign** — all drafting, review, routing, and evidence use remain local. Maximum-custody posture, **marked as performance-dependent / under validation** until proven against real grant workloads. Customer-facing materials carry explicit under-validation notice; deployment manifest `local_only_validated: bool` field (default false; write-protected; flips only on SN-LLC quarterly validation outcome signature) gates "production-validated" claims on any customer-facing artifact.

For each agent call:
- Posture is the deployment-level decision (operator-signed at white-glove Classification Review step 3 + Ed25519-signed step 4 sign-off).
- If posture == local_only_sovereign → route LOCAL (no further checks).
- Elif posture == frontier_eligible → public/shareable → cloud; confidential/operator_flagged → local; class indeterminate → fail-closed LOCAL default per F-CLASS-ROUTING-INDETERMINATE.
- Elif posture == split_context_hybrid → public/shareable + seat in {scribe_scaffold, scout, intake_classification_review} → cloud frontier (scaffold/structure work only via closed-set allow-list per F-CLASS-SPLIT-CONTEXT-ALLOWLIST PRE-gate + pre-cloud applicant-fact scan per F-CLASS-SPLIT-CONTEXT-LEAK PRE-gate); confidential/operator_flagged → local; class indeterminate OR review-shape seat → fail-closed LOCAL default.

Post-substance-assembly drafts (any draft carrying Confidential-bearing substance — the common case under Frontier-Eligible + always under Split-Context Hybrid) → all subsequent seats local routing (Editor / Red Team / routine-Judge structural local).

Heavy-Judge swap (v7.0.7 §4) remains canonical: 200B-class local model on-demand for federal long-form / large award / operator-flagged grants — **pre-loaded on the Golden Quill appliance** at white-glove (no network fetch; F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD PRE-gate; alternative-update-channel ban; boot-time manifest verification).

Always-local agents: Logician, Intake, Uploader, reflection_agent (Reflection sub-mode of Archivist v0.1 hook per v7.0.9). Cloud-routable agents (only when posture permits AND input class permits): Scribe, Editor, Judge, Red Team, Scout (per channel). The slot-fill agent module stays in the runtime tree as defense-in-depth-only — never invoked in normal-path cycle operation under any v7.0.10 posture.

The classification register — populated during the named **Classification Review** stage in white-glove onboarding (mandatory for v0.1 Beta deployments; v7.0.10 §1.4 extends step 3 + step 4 to include posture selection + posture sign-off) — is the load-bearing primitive. Three-layer defaults: Card-level archetype defaults → operator overrides at white-glove → per-grant SP0 overrides. Operator-signed Ed25519 register at white-glove + per-grant SP0 signature chain. Posture re-selection post-onboarding via `tilth posture select` CLI; mid-cycle changes fail-closed per F-CLASS-POSTURE-MID-CYCLE-CHANGE.

Golden Quill ships router-template updates per v7.0.7 §6.1 publisher-Ed25519-signing + Golden-Quill-verification discipline (unchanged at v7.0.10).

F-CLASS-* failure-code family roster after v7.0.10 LOCK: **sixteen primitives** (ten legitimate-runtime from v7.0.7 §5.1 + two repurposed defense-in-depth — F-CLASS-SLOT-ID-NON-OPAQUE + F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED with broadened regex `\[SLOT_[^\]]*\]` + four new at v7.0.10: POSTURE-MID-CYCLE-CHANGE + SPLIT-CONTEXT-ALLOWLIST + SPLIT-CONTEXT-LEAK + HEAVY-JUDGE-CLOUD-DOWNLOAD). F-CLASS-COVERAGE-INCOMPLETE META PRE-cycle gate scope expands to the sixteen.

Full spec: `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md` (LOCKED 2026-05-11 row 215). v7.0.7 LOCKED 2026-05-10 (row 180) is the historical-precedent authority for the F-CLASS-* family origin + Classification Review stage + heavy-Judge swap + router-template signing.

## The Four Autonomy Rules (Organism Pattern)

These govern how the council pipeline operates:

1. **Save State Always.** Every operation saves state on BOTH success and failure. An agent that only saves wins has amnesia about its losses.
2. **Test Your Own Work (The Magic Step).** Before marking ANY task complete, validate. Scout validates URLs resolve and deadlines are future. Scribe validates sections exist and KGIE passes. Judge validates all 12 dimensions scored and evidence strings appear in drafts. This is Bug #20 — the single `if validate()` that transforms a tool into an autonomous agent.
3. **Be Explicit.** Every task between seats includes: input file path, output file path, exact scope, done definition. No "score the draft" — the actual path, the actual output location, the actual threshold.
4. **Clean Output.** Strip markdown fences from structured data. Strip conversational fluff. Strip LLM self-commentary. Validate format. Never pass raw LLM output to the next seat.

## Operational Gears

Each seat can operate in one of three modes, set by the applicant:

- **Sparring Partner** — seat generates options, human decides
- **Co-Pilot** — human provides direction, seat executes and refines (DEFAULT)
- **Synthesizer** — full delegation, human reviews final output only

## Client Org Isolation

Josh serves multiple clients. Each has its own folder under `orgs/` in the workspace:

```
orgs/
├── ORG_INDEX.md              ← Master index of all clients
├── _TEMPLATE/                ← Blank PROJECT_CONTEXT for new clients
├── mycosymbiotics_cooperative/
├── mycosymbiotics_inc/
├── mystic_mamas/
├── run_a_muck_farm/
└── [future clients]/
```

**Law 3 enforcement:**
- When working on a grant for one org, ONLY read that org's PROJECT_CONTEXT.md.
- NEVER cross-reference data between orgs. Never use one client's info in another's work.
- If a field says [NEEDED], ask Josh. Do not fill it from another org or from inference.
- MycoSymbiotics Cooperative and MycoSymbiotics Inc are SEPARATE entities with separate data.

## Key File Locations

- **Locked architecture (v0.1 canonical):** `pipeline/architecture/v0.1/tilth_architecture_locked.md` — v7 LOCKED 2026-04-19 (A1-A12). The "WHAT." Do not edit in place; architectural changes are a new audit round.
- **Pending amendment:** `pipeline/architecture/v0.1/architecture_v7_0_1_amendment.md` — v7.0.1 DRAFT (Section E.P Governance Plan Preflight). Awaiting Tier 1/2/3 GPP + L-005 two-audit domain-split Thesis round before LOCK. LOCKs atomically with paired §4 v2.1.1 and §0.5 v5 blueprint amendments.
- **Architecture audit trail:** versioned copies under `pipeline/architecture/v0.1/` (v4 2026-04-16, v5-r8 2026-04-17, v6-r2 2026-04-18, v7 A1-A6 2026-04-19).
- **Blueprints (v0.1):** `pipeline/blueprint/v0.1/` — the "HOW." One file per section. Sections audited by the same Thesis Team before lock.
- **Client orgs:** `orgs/` in this workspace folder — one folder per client
- **Skills (source of truth):** `skills/` — scout-discovery, scribe-ghostwriter, judge-rubric, council-pipeline
- **Agent identity:** `SOUL.md` at workspace root
- **Session bootstrap (new-session orientation):** `pipeline/SESSION_BOOTSTRAP.md`
- **Component analysis template:** `pipeline/templates/component_analysis_template.md`
- **OpenClaw config:** `~/.openclaw/` on Josh's Mac Mini
- **OpenClaw agent workspace:** `~/.openclaw/agents/mycosymbiotics/`
- **Session metrics spec:** `pipeline/metrics/SESSION_METRICS_SPEC.md`
- **Session metrics log:** `pipeline/metrics/session_log.jsonl`
- **Efficiency audit template:** `pipeline/templates/efficiency_audit_agent.md`

## Session Efficiency

These directives reduce token waste, round-trip overhead, and repeated boilerplate across Cowork and Code sessions.

**Batch all open questions.** When multiple things are unclear, collect every question into a single message. Do not ask one at a time and wait for answers sequentially.

**Match the operator's register.** Josh is terse and decisive. Responses should be thorough but not ceremonial — no preambles, no restating what he just said, no performative hedging. Get to the substance.

**Reference shared templates, don't repeat framework.** Component analyses, Thesis Team audits, and seat-binding reviews reference `pipeline/templates/component_analysis_template.md` for the Five Laws, Four Rules, failure modes, hardenings checklist, dev-vs-prod context, and standard interface pattern. Only write what's delta for the component under review.

**Batch file operations.** Plan all reads/writes before executing. Minimize round trips — read multiple files in one turn where possible, write multiple outputs in one turn where possible.

**Reference SESSION_BOOTSTRAP.md in handoffs.** When producing handoff prompts for new sessions or agents, write `Read pipeline/SESSION_BOOTSTRAP.md for project orientation` instead of re-explaining the project universe. The bootstrap file covers identity, file locations, locked decisions, active constraints, and pointers to architecture/blueprints.

**Path references, not content dumps.** Per L-002: never paste file contents into prompts. Reference by path. Let the receiving agent read.

**Two-audit cycle, not three-round silent revision.** Per L-005: Audit #1 scoping → fix → Audit #2 verification → lock or escalate. No silent third round.

**Cross-family Thesis dispatch — bridge pattern is the default.** Cowork sessions reach the local openclaw gateway via `mcp__Control_your_Mac__osascript` → `do shell script "PATH=$HOME/.npm-global/bin:$PATH openclaw infer model run --gateway --model X --prompt P --json" with timeout of 600 seconds`. Live model IDs: `groq/llama-3.3-70b-versatile` (Editor) / `google/gemini-2.5-pro` (Judge) / `groq/openai/gpt-oss-120b` (Red Team). Working dispatch templates: `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`. Section E single-Claude carve-out requires a *logged dispatch failure* to invoke (captured curl/openclaw error in the audit trail) — not a default fallback. Full discipline in `/AGENTS.md` § "Cross-family review — bridge pattern" + § "Section E carve-out — invocation discipline".

**Write session metrics on close.** Every session writes a metrics entry to `pipeline/metrics/session_log.jsonl` as its last act before signing off. Run the Session Close Self-Check first. Schema and procedure in `pipeline/metrics/SESSION_METRICS_SPEC.md`.

**Proactive pre-staging.** IF a task completes AND downstream tasks unblock, THEN pre-stage each unblocked task whose spec is derivable from the blueprint/roadmap without operator input — before sign-off, same session. Pre-staging means writing the spec card (per `engineering_process_v0.1.md` §11) if the next task is a module build, OR writing the handoff prompt (per AGENTS.md § Compact handoff payloads) if the next task is a different session, OR surfacing the specific open questions if operator input IS required. If multiple unblocked tasks can run in parallel with no shared dependencies, propose parallel dispatch rather than serial handoff. Do not wait to be asked. Sessions that close without pre-staging leave deployment gaps that manifest as "next?" questions from the operator — which is a failure of this discipline, logged in `self_check_failures`. Exception: next task requires operator-voice content (grant text, client-facing copy), has spec ambiguity only Josh can resolve, is behind an unclosed Thesis round, or depends on an `[NEEDED]` PROJECT_CONTEXT field.

## Session Close Self-Check

Every agent runs this checklist on its own output before closing a session. If any item fails, note it in the session metrics entry under `self_check_failures`.

1. **Batched questions?** — Did I collect all open questions into single messages, or did I ask sequentially?
2. **Template references?** — Did I reference shared templates (`pipeline/templates/component_analysis_template.md`, `pipeline/SESSION_BOOTSTRAP.md`) instead of restating framework structures inline?
3. **Handoff under 50 lines?** — If I produced a handoff prompt, is it under 50 lines (excluding the bootstrap reference)? Over 50 = failed.
4. **Matched operator register?** — Was my tone terse and substance-first, or did I pad with preambles, hedging, or restating what Josh said?
5. **Minimized file round trips?** — Did I batch file reads/writes, or did I do them one at a time across multiple turns?
6. **Logged session metrics?** — Did I write my metrics entry to `pipeline/metrics/session_log.jsonl` as my last act? (Per `pipeline/metrics/SESSION_METRICS_SPEC.md`.)
7. **Pre-staged next task?** — If this session unblocked a downstream task whose spec is derivable without operator input, did I write its spec card / handoff / open-questions surface before sign-off? If I left "next?" for the operator to ask, that's a failure logged in `self_check_failures`.

Sessions under 3 turns with no files read/written and no handoff produced may skip metrics logging — but the self-check still runs mentally.

## What NOT to Do

- Do not propose substrate replacements for v0.1 — the substrate is LOCKED at Pydantic AI + Logfire (orchestration + structured output + observability) + curated Python document parsing utilities (python-docx, openpyxl, pypdf, equivalents) wrapped as Pydantic AI tools, frozen at Golden Image build with no marketplace access from the appliance + Ollama or vLLM (local inference, OpenAI-compatible endpoint) + DSPy + GEPA (offline Card refinement, Library development only) + Logician (deterministic Python + Cedar policy gates, fail-closed, zero-token, all Five Laws as PRE/POST/COMMIT gates) per ADR-001, architecture v7.0.3 amendment (2026-05-08), and on-disk pyproject.toml. (LangGraph and OpenClaw are both removed — LangGraph was never wired; OpenClaw is absorbed by Pydantic AI's agent primitives + structured-output capabilities per ADR-001 §Alternatives Considered.) Phase 2+ horizon items (Stage 2-5 multi-tenant / coop / federation / Stage-5 Sovereign Node commons) stay out-of-scope-for-v0.1.
- Do not propose a Managed Edition or metered billing — BYOK only is locked
- Do not propose a Next.js UI or any UI layer for v0.1 — headless only
- Do not propose PA Ag Innovation Grant as a dogfood target — off the table
- Do not ask what MycoSymbiotics is applying for — irrelevant to the build
- Do not absorb Daniel Crawford's persona into Scribe — he's a real collaborator, not inherited lore
- Do not silently rewrite flagged terms — applicant must approve
- Do not tell Josh what he should be working on when he asks a different question
- Do not loop revisions beyond the two-audit cycle without operator escalation (L-005)
- Do not skip validation (Rule 2 is non-negotiable)
- Do not encode any CIC→CLC subset binding in any code, schema, prompt, knowledge pack, scoring weight, or config — F-CIC-CLC-COUPLING-VIOLATION enforces fail-closed (architecture v7.0.8 amendment, 2026-05-08). CIC and CLC are orthogonal axes; matching is opportunity-driven runtime, never archetype-driven design-time.
- Do not emit `[SLOT_<anything>]` patterns into cloud-routed prompts under any v7.0.10 posture — the Sanitized / opaque-slot-token mechanism is DEPRECATED per architecture v7.0.10 LOCKED 2026-05-11 row 215. F-CLASS-SLOT-ID-NON-OPAQUE + F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED are now defense-in-depth gates with broadened regex `\[SLOT_[^\]]*\]`; firing indicates bug or attack. The v7.0.7 §1 slot-fill agent + opaque-slot-rendering round-trip is structurally absent under all three v7.0.10 postures (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign).
- Do not propose a fourth routing posture or revive the Sanitized vocabulary. The three-posture customer-facing model is canonical per v7.0.10 §1. The substance/structure separation under Split-Context Hybrid (closed-set allow-list + applicant-fact PRE-scan) achieves the "power for drafting + privacy on substance" goal without opaque-slot tokens.
- Do not ship a v0.1 Beta deployment without a completed Classification Review stage and operator Ed25519 sign-off (architecture v7.0.7 LOCKED 2026-05-10). The F-CLASS register/routing gates fail-close unsigned, invalid, indeterminate, confidential-to-cloud, or slot-leaking routes; F-CLASS-COVERAGE-INCOMPLETE separately prevents deployment if any required F-CLASS-* module or test is missing.
- Do not apply a router-template update without verifying the Ed25519 signature against the white-glove-pinned publisher public key — F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID fail-closes any unsigned/wrong-signed update (architecture v7.0.7 §6.1).

## Hardware

Josh's dev node: M1 Mac Mini, 8GB RAM. Client production spec: 128GB+. If v0.1 runs on 8GB it flies on 128GB.

## Running tests — PINNED INTERPRETER

Always run tests via `scripts/run_tests.sh` (or `.venv/bin/python3 -m pytest …` directly). System `python3` on macOS is 3.9 and cannot even *collect* the code under test — `@dataclass(frozen=True, kw_only=True)` requires 3.10+, and `pyproject.toml` pins `>=3.11`. An agent running `python3 -m pytest` will see 8 collection errors and may misreport them as real test failures. The `.venv` uses Python 3.14 and is the only supported interpreter for the suite.

## Current System State

Model bindings: see `/router.yaml`. Provider tier changes update only that file.

Infrastructure (as of 2026-04-14):

- OpenClaw installed with LaunchAgent daemon + dashboard at http://127.0.0.1:18789
- Provider keys: Anthropic (Scribe), Groq Dev tier $20/mo (Scout + Editor + Judge), Google + OpenAI as fallback/escalation — all BYOK
- Custom skills deployed: scout-discovery, scribe-ghostwriter, editor, judge-rubric, logician, council-pipeline
- Tilth agent configured as multi-client system
- MemPalace v3.1.0 installed with OpenClaw MCP integration (ChromaDB 1.5.7, palace at ~/.mempalace)
- Logician built: 8 deterministic validation gates, admin-risk register (18 entries), revision loop counter
- VAPG FY26 rubric extracted and stored in `pipeline/rubrics/vapg_fy26.json` (100 pts, 7 criteria)
- RTK v0.35.0 installed for token compression
- Pipeline directories at `pipeline/`: radar/, drafts/, scores/, validation/, rfa/, editor/, rubrics/, institutional_memory/
- Institutional memory: `pipeline/institutional_memory/lessons.json` (machine-readable) + `/lessons.md` (human-readable, canonical for agent wake-up)
- Client orgs live under `/orgs/` — see `orgs/ORG_INDEX.md` for current roster and status
- PROJECT_CONTEXT.md files have [NEEDED] fields that only Josh can fill (EIN, UEI, SAM status, address, county, production metrics, financials, boilerplate)

## v0.1 Beta Deployment Posture (lock-and-clear active 2026-05-11)

The Beta submission workflow architecture is locked. The current active clearance packet is `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md`, which supersedes the older 2026-05-10 readiness/launch posture snapshots. v0.1 clears when the reproducible submission-mode replay packet exists and the live claim surface stays clean.

- **Intake current-tree proof — SMOKE GREEN 2026-05-11.** Three modes covered: BULK_INGEST (white-glove onboarding bulk doc absorption), INCREMENTAL_INGEST (between-cycle fact additions, new facts default to `confidential`), AWARD_INGEST (proposal_commitments.yaml extraction at award acceptance).
- **Uploader current-tree proof — SMOKE GREEN 2026-05-11.** Four portal adapters covered: Grants.gov Workspace, SAM.gov, Common Grant Application, copy-paste fallback. Foundant / Submittable / Fluxx are Path-b scope per §12 v1 LOCK. Attachments deferred to v1.1.
- **Classification Review operator UX wrapper — LANDED 2026-05-10.** Orchestrator at `pipeline/orchestrator/classification_review.py` + CLI at `pipeline/cli/tilth_review_classify.py` + scaffold at `orgs/_TEMPLATE/classification_review/` + 7/7 integration tests PASS in 0.26s. Per-org register lands at canonical gate-checked path `orgs/<slug>/vault/classification/register.yaml`. F-CLASS-COVERAGE-INCOMPLETE + F-CLASS-REGISTER-UNSIGNED + F-CLASS-REGISTER-SIGNATURE-INVALID + F-CLASS-REGISTER-HASH-MISMATCH all pass post-orchestrator-run.
- **WS-L §4 Logician v2.x LOCKED 2026-05-10** at rows 193/194 — the twelve F-CLASS-* primitives + v0.2-family registrations + KFR residuals + v7.0.4-M1 corrective predicates realized as Cedar/Python deterministic gates. `F-CLASS-COVERAGE-INCOMPLETE` PRE-cycle gate cleared. **v0.1 Beta architectural gate CLEARED.**
- **White-glove playbook subset** — Classification Review + AWARD_INGEST + classification register seeding + first grant cycle dispatch. Authored at `docs/white_glove_v0_1_beta.md`.
- **v0.1 smoke result — GREEN 2026-05-11.** 339 focused tests passed (router classification boundary + F-CLASS + Classification Review + Intake + Uploader + CIC/CLC guard set); `scripts/run_lint.sh pipeline` clean exit 0.

**WPFA cycle-close accounting (§17 v1 LOCKED 2026-05-11; rows 205-208 compound quadruple).** Tilth emits a typed `CycleReceipt` Pydantic artifact at every cycle close, deterministically computing actual dollars + watt-hours consumed vs counterfactual (100% routed to the quarter's publisher-signed flagship baseline) vs regenerative-savings delta. Sub-kind at `orgs/<slug>/vault/operational/cycle_receipts/<cycle_id>.json`. Coefficient Registry signed asset at `vault_shared/wpfa/coefficient_registry/active.yaml` (router/coefficient publisher releases it; white-glove pins the publisher pubkey at onboarding; trust mechanism mirrors v7.0.7 §6.1 router-template byte-for-byte). Operator Ed25519 attestation gates buyer-facing PDF emission (`F-WPFA-OPERATOR-SIGNATURE-MISSING` — M13 NOT permitted; structural attestation boundary). A12 Decimal mandate extended to energy quantities (int micro-watt-hours; no float; AST-lint R-WPFA-DECIMAL-MANDATE-ENERGY enforces). 12 F-WPFA-* failure codes (10 modules; predicate bodies LIVE at LOCK — first §4 amendment with LIVE bodies). Operator dashboard (Cowork HTML artifact) reads per-org + per-quarter rollups; per-fleet placeholder = data-free Stage-2+ marker. Buyer-facing PDF is the sales lever — every claim links to coefficient + cycle_id + Logfire trace_id; weasyprint HTML→PDF; classification register cross-check fails closed on confidential leak. Sibling-not-nested with Reflection Packet (shared input substrate = Logfire span tree; zero shared output/consumer/schema; F-PACKET-* family separation per Path B naming reconciliation).

**Beta deployment fail-closed gates** (any one of these blocks the cycle):
- `F-CLASS-COVERAGE-INCOMPLETE` — the required F-CLASS-* enforcement modules and tests are incomplete or missing from the runtime tree.
- `F-CLASS-REGISTER-UNSIGNED` — register exists but operator Ed25519 signature is missing.
- `F-CLASS-REGISTER-SIGNATURE-INVALID` — signature verification fails against pinned operator public key.
- `F-CLASS-ROUTING-INDETERMINATE` — per-call routing decision cannot determine cloud-vs-local; fail-closed to local.
- `F-CLASS-NEW-FACT-UNCLASSIFIED` — new fact ingested via Intake INCREMENTAL has no classification; defaults to `confidential` pending operator re-classification.
- `F-CLASS-SLOT-ID-NON-OPAQUE` — cloud-routed prompt contains a semantic slot name; only `[SLOT_<numeric_id>]` is admissible.
- `F-CLASS-HIGH-STAKES-FLAG-LEAK` — heavy-Judge swap flag leaked into a cloud payload.
- `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` — router-template update signature does not verify against white-glove-pinned publisher public key; deployment stays on prior pinned version.
- `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` — Coefficient Registry signature does not verify against the white-glove-pinned publisher public key (same trust mechanism as router-template).
- `F-WPFA-COUNTERFACTUAL-INFLATION` — receipt baseline_model_id ≠ Coefficient Registry baseline_model_id (P0 audit-integrity gate; M13 NOT bypassable for buyer-attested receipts).
- `F-WPFA-OPERATOR-SIGNATURE-MISSING` — buyer-facing PDF emission attempted without operator Ed25519 attestation (structural attestation boundary; M13 NOT permitted).
- `F-WPFA-CROSS-ORG-LEAK` — CycleReceipt write whose path slug differs from receipt.org_slug (Law 3 structural).
- `F-WPFA-PDF-CONFIDENTIAL-LEAK` — buyer-facing PDF would render any field whose classification register entry is `confidential` (Law 3 + v7.0.7 structural).

**v0.1 vs v0.2 boundary.** v0.1 Beta ships `submission_mode` (drafting / package assembly / operator-staged submit) and `eval_mode` (Judge / Red Team scoring) of the track registry as ACTIVE. `report_mode` is a FORWARD-COMPAT row that refuses at runtime via `F-PIPE-TRACK-NOT-SHIPPABLE` until WS-J §14 LOCK flips `shippable_in: v0.2` to `true`. The track registry dispatcher does not need re-edit when v0.2 lands — only the registry row gets updated. Data Collector (5 channels: email + SMS + voice + Telegram + WhatsApp) and Report Generator are v0.2-only.

**Reflection Packet v0.1 Beta hook (§16 v1 LOCKED 2026-05-15; rows 216/217/218 compound triple).** Tilth emits a typed `ReflectionPacket` Pydantic artifact at every grant cycle close (Packet 1 PENDING at cycle-close marker; Packet 2 BACKFILL at decision-observed event with operator Ed25519). Sibling-not-nested with WPFA CycleReceipt: zero shared output / consumer / schema / F-* code crossing; one cross-reference at `F-PACKET-SPAN-PROVENANCE-MISSING` ↔ `F-WPFA-SPAN-PROVENANCE-MISSING` (this LOCK resolves §17 v1 §6.5 forward-reference). v0.1 hook DORMANT per OQ-2 (a) — schema authored at `pipeline/vault/sub_kinds/reflection_packets.py` (NOT registered in SUB_KIND_REGISTRY; deferred to v0.2 first wave); 21 `__post_init__` invariants LIVE for testability (length / grammar / type / closed-set / signature shape); 19 F-PACKET-* failure-code signatures registered at `pipeline/logician/gates/f_packet_*.py`; 18 raise `NotImplementedError` at v0.1 hook; 1 (`F-PACKET-COVERAGE-INCOMPLETE`) carries LIVE META-gate body as the dormant-binding lever (mirrors `F-REFLECTION-COVERAGE-INCOMPLETE` row 404 + `F-CLASS-COVERAGE-INCOMPLETE` v7.0.7 §5.1 byte-for-byte). Cedar policy at `pipeline/vault/policies/reflection_packet.cedar` carries 19 rules (18 fail-closed-pending + 1 LIVE). Path B naming reconciliation realized at this LOCK: `F-PACKET-*` (artifact) / `F-REFLECTION-*` (producer; §4 v2.x.2 row 203) / `F-ARCHIVIST-*` (substrate; §15 v1) / `F-WPFA-*` (sibling artifact; §17 v1) — four orthogonal F-* families with AST-lint cross-family-import ban. F-PACKET-* EXCLUDED from `F-CLASS-COVERAGE-INCOMPLETE` META gate per OQ-6-style isolation precedent (same as F-WPFA-* + F-FG-*). v0.2 first wave compound LOCK (§16 v1.1 producer-flip + §2 v7.x sub-kind registration + §4 v2.x.y.1 NotImplementedError → live body flip + META-gate body-realization strengthening per RT-01 fold-in + §15 v2.x Archivist Reflection sub-mode SPEC + §0.5 v?? paired-commit) is the next horizon — pre-staged handoff at `pipeline/handoffs/ws_reflection_packet_v0_2_first_wave_handoff_2026-05-15.md`.

## Grant Writing Context

When using the grant-finder or grant-writer skills that are already installed in this Cowork space, those skills work TODAY. Josh has won three competitive grants with them in 2026. The Sovereign Node / Tilth build is about systematizing and upgrading those skills into a full pipeline that self-improves.

## Institutional Memory

Track repeated failures across grants in `pipeline/institutional_memory/lessons.json`. Frequency increases belief weight. High-frequency + high-severity lessons become mandatory pre-checks. Before each pipeline run, load lessons and pre-check for known failure patterns.

## Sovereignty Promise

This system runs on hardware the operator owns. API keys belong to the operator. Confidential data stays local by default. Public + Shareable content may use explicit approved cloud routes under BYOK and audit logging. If FIT Farms LLC or any future Golden Quill spin-off disappeared tomorrow, the operator would still have their machine, their data, their keys, and their grants. Nothing is held hostage. Every new feature must answer: does this preserve client sovereignty?
