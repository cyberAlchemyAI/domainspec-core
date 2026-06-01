---
title: Paul Norton — Tilth × Amnesia Labs Alignment Brief
audience: Paul Norton (incoming platform engineer); operator (Josh) reviews first
authored: 2026-05-15
authored_by: Tilth core (Cowork session, opus 4.7)
status: living document; no LOCK
companion_files:
  - docs/platform_engineer_onboarding.md (full project surface)
  - docs/platform_engineer_quick_reference.md (daily-driver one-pager)
  - docs/grant_writing_technical_acumen_inventory_2026-05-15.md (CIC × CLC card inventory; appended to brief 2026-05-15 PM)
  - pipeline/handoffs/deep_research_cic_clc_card_handoff_2026-05-15.md (parameterized research dispatch; appended to brief 2026-05-15 PM)
parent_assessment: pipeline/planning/architecture_proficiency_assessment_result_2026-05-11.md
evidence_pack: pipeline/validation/architecture_proficiency_2026-05-11/evidence_pack.md
amnesia_labs_sources:
  - Brain (https://amnesia-labs.com/brain) — uploaded PDF + crawl
  - JIT (https://amnesia-labs.com/jit) — uploaded PDF + crawl
  - docs (https://docs.amnesia-labs.com) — 37-page exhaustive crawl 2026-05-15
---

# Paul Norton — Tilth × Amnesia Labs Alignment Brief

This is the document you read after `docs/platform_engineer_onboarding.md` if you want to know *where your existing work converges with the highest-leverage gap in the Tilth architecture*. The onboarding pack tells you what the system is. 

We did a thorough architecture proficiency assessment 4 days ago — 8 dimensions, 80 points possible, total 47/80. The result file is `pipeline/planning/architecture_proficiency_assessment_result_2026-05-11.md`. The summary you need to internalize: **six of eight dimensions clear the Beta bar; one dimension (memory competence) does not, and it scores 4/10.** Memory is the single load-bearing gap between "ready to ship" and "ship-shaped."

Your work at Amnesia Labs — **Brain** (four-store memory architecture, Thalamus routing, learning loop) and **JIT** (just-in-time delivery of memory + skills + plugins + docs) — is structurally the closest thing to a built answer to that gap that we've reviewed. This brief lays out where the fit is real and where the sovereignty constraints of Tilth break the off-the-shelf integration.

---

## 1. Tilth in one page — what you're inheriting

**What ships:** A 128 GB-RAM-floor desktop appliance ("Golden Quill") that runs a fixed graph of six AI council seats (Scout / Scribe / Editor / Judge / Red Team / Logician) plus support agents (Intake, Uploader, Data Collector, Report Generator, Archivist, WPFA Cycle Accountant). The customer owns the hardware. The customer owns the API keys (BYOK). The pipeline writes federal / state / foundation grant proposals end-to-end and stages them for the operator to submit. Today Josh has won 6 competitive grants in 2026 using the prior generation of this stack.

**Where it sits architecturally:** v0.1 Beta is structurally ready — 1,869 tests pass; Cedar fails closed; Logician deterministic policy gates have zero token cost; signed-asset trust chain is *ahead* of where industry just-realized-it-needs-to-be after the MCP tool-poisoning disclosures earlier this year. The architectural gate for v0.1 Beta cleared on 2026-05-10 (lock_history row 193).

**Where it has been moving:** ~37 LOCKs between 2026-05-09 and 2026-05-15 (lock_history rows 178 → 214). The tentative future substrate is Pydantic AI + Logfire + Ollama/vLLM + Cedar + 110-ish failure-code modules across 20 families. The §0.5 Interface Index has crossed 500 runtime-live rows. Architecture decisions land via a "LOCK ceremony" + cross-family Thesis dispatch through a local openclaw gateway after Opus 4.7 and directed by Opus 4.7 (Editor=Llama/Groq, Judge=Gemini/Google, Red Team=GPT-OSS/Groq).

**Top 3 things that ship well:**

1. Sovereignty + signed-asset trust chain
2. Logician deterministic gates (zero token cost, fail-closed stability)
3. Cross-family Thesis rigor as default

**Top 3 things that threaten desk-Beta:**

1. Memory architecture fragmented across 13 registers with no unified API (Dim 8 = 4/10)
2. Per-cycle token-cost KPI absent (Dim 1 — sales objection on BYOK bill)
3. §0.5 ceremony at 505 rows exceeds value-at-risk per surface (Dim 6)

**Top 3 real customer-blocking gaps:**

1. Reflection Packet runtime-on (LOCKed but dormant — cross-cycle learning today is operator-curated only)
2. OCR / VLM-based parsing for legacy scanned RFAs (real onboarding-corpus degradation at 40-70% of customer archives)
3. Operator-facing past-grant portfolio query surface

If you're optimizing for impact, the convergence between your work and #1 + the memory architecture is the story. Sections 4 + 5 + 7 below are the load-bearing ones for you.

---

## 2. The Alpha set — what works today on a customer's desk

These are the surfaces that are running well enough to ship.

| Surface | State | Why it works |
|---|---|---|
| **Six-seat council pipeline** (Scout → Scribe → Editor → Judge → Red Team → Logician) | Full module trees on disk under `pipeline/orchestrator/seats/*/` including provider adapters, cross_rubric_dispatch, sfr_emitter, logician_wiring | Real substrate, not sketches. Cross-family rigor enforced. 1869 tests pass. |
| **Submission_mode track + eval_mode track** | ACTIVE in §5 v8 track registry; `report_mode` track is FORWARD-COMPAT (refuses at runtime via `F-PIPE-TRACK-NOT-SHIPPABLE` until v0.2) | Track-registry abstraction is built; report_mode lights up at v0.2 without re-wiring. |
| **Classification register + 3-posture routing** | Architecture v7.0.7 LOCKED (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign). Operator-signed Ed25519 register. 12 F-CLASS-* gate primitives. | This is the structural foundation that makes the appliance sovereign. |
| **Cedar policy evaluator** | Loaded at module import. `CedarEngine.is_ready() is True` check + `CriticalPolicyError(BaseException)` on failure (subclasses BaseException so try/except Exception can't swallow). Bootstrap pattern replicated across Data Collector + Report Generator. | Fail-closed by design. |
| **Logician gates** | ~110 failure codes across F-CLASS / F-INTAKE / F-UPLOADER / F-CEDAR / F-REPORT / F-ARCHIVIST / F-DATACOLLECTOR / F-WPFA / F-PACKET / F-FACT-DRIFT / F-LOGICIAN families. PRE + POST gates wrap every seat call. Zero token cost. | The firewall. Treat as the most stable layer. |
| **Signed-asset trust chain** | Router-template, Coefficient Registry, classification register, CycleReceipt, buyer-PDF — all Ed25519. White-glove pins publisher pubkey. Verifies before applying. | *Ahead of industry* post-MCP-poisoning. |
| **KFR (Key Facts Register) per-org** | Verbatim-quote-with-page provenance, SP0 freshness, derivation-chain integrity, AWARD_INGEST commitment extraction, content-hash binding. Architecture v7.0.4 + v7.0.4-M1 cleared the canonicalization + Decimal-mandate + atomic-read gates. | The authoritative source-of-truth substrate. Per-org, signed, never bleeds across Law 3 boundary. |
| **Intake** (v0.1) | Three modes (BULK / INCREMENTAL / AWARD). 11 owned F-INTAKE-* codes. Smoke green 2026-05-11. Watcher TOCTOU bounded by A1+A4. | White-glove onboarding works. |
| **Uploader** (v0.1) | Four portal adapters (Grants.gov Workspace, SAM.gov, Common Grant Application, copy-paste fallback). 10 owned gates + `R-UPLOADER-NO-SUBMIT` AST-lint. Three-layer auto-submit defense. Smoke green 2026-05-11. | Prepare-and-stage works. Operator clicks final submit. |
| **WPFA Cycle Accountant** (§17) | 12 F-WPFA-* codes with LIVE predicate bodies (first §4 amendment with live bodies). Coefficient Registry signed-asset. Decimal mandate extends to energy (int micro-watt-hours). Operator Ed25519 gates buyer-PDF emission. | Cycle-close accounting is the sales lever — every receipt links to coefficient + cycle_id + Logfire trace_id. |
| **Cross-family Thesis** | osascript → openclaw bridge pattern. Editor=Llama/Groq + Judge=Gemini/Google + Red Team=GPT-OSS/Groq. L-005 two-cycle discipline + row-170 transparent fold-in disposition pattern. | This is how decisions get audited. Working dispatch templates at `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`. |

Alway open to consideration.  

---

## 3. The Beta set — what's LOCKed but in flight

These are surfaces that have a SPEC but are not yet running, or are partially running and need finalization work. Your platform/ops work has the most leverage on the ones marked ⭐.

| Surface | State | What "in flight" means |
|---|---|---|
| **⭐ Reflection Packet** (§16) | LOCKED 2026-05-15 (rows 216-218). 19 F-PACKET-* codes — **18 raise NotImplementedError; 1 LIVE META gate**. Hook is dormant at v0.1 Beta by design. | v0.2 first-wave compound LOCK will activate producer-flip (Packet 1 PENDING at cycle-close + Packet 2 BACKFILL at decision-observed with operator Ed25519). Pre-staged handoff at `pipeline/handoffs/ws_reflection_packet_v0_2_first_wave_handoff_2026-05-15.md`. **This is the single highest-leverage v0.2 first-wave delivery.** |
| **⭐ Funding Goal** (§2 v7.5) | LOCKED 2026-05-11 (rows 211-214). SPEC-ONLY at v0.2. STUB F-FG-* family. R-FG-STUB-ONLY-AT-V0_2 AST-lint refuses any code that tries to call FundingGoal in v0.1. | Persistent per-org funding intent across grant cycles. Drives Scout DISCOVER goal-aware ranking + Match DB goal-aware composite score. Ships alongside §14 Report Generator at v0.2 first wave. |
| **WS-J §14 Report Generator code phase** | Slice 1 + Slice 2 LANDED 2026-05-11. Slice 3 pre-staged (`pipeline/handoffs/ws_j_section_14_slice_3_wiring_2026-05-11.md`) — `run_report_pipeline` + `finalize_operator_signed_report` + AST-lint rules + first-wave marker hash binding. | `report_mode` track flips `shippable_in: v0.2` to `true` when Slice 3 lands. Five sub-section composers + Cedar bootstrap + legacy beneficiary_records consent_tier_history migration shim — all built and tested. |
| **WS-WPFA code phase** | Spec rows 205-208 LOCKED. Predicate-body finalization + orchestrator wiring + buyer-PDF substrate pre-staged at `pipeline/handoffs/ws_wpfa_code_phase_handoff_2026-05-11.md`. | First paid Beta sales-lever artifact. Operator Ed25519 attestation gates buyer PDF; SN-LLC inaugural Q3-2026 registry publication is downstream. |
| **WS-I §13 Data Collector code phase** | §13 v1 LOCKED 2026-05-10. Code phase landed (5 channel modules: email/SMS/voice/telegram/whatsapp). Tests 131/131 + 4348 broader pass. | Channel substrate wiring done. State-rules card (PA/CA/FL/TX/NY) is v0.2 first wave; SN-LLC-signed. |
| **§15 Archivist** (v1.x horizon) | SPEC LOCKED 2026-05-10 (rows 191/192). Module skeleton + 27 skeleton tests pass. Proposes-only AST assertions structurally enforced. Three-layer defense (AST-lint + runtime guard + Cedar policy). | Runtime implementation deferred to v1.x. v0.2 cadence is operator-driven manual invocation. Reflection sub-mode under §15 lands as part of Reflection Packet v0.2 first-wave. |
| **v7.0.10 architecture sweep** | LOCKED 2026-05-11 (row 215). 3-posture routing canonical; Sanitized/opaque-slot-token posture DEPRECATED; 4 new F-CLASS gates. | Posture-mid-cycle changes and split-context allow-list now have predicate bodies. |
| **Classification Review operator UX wrapper** | LANDED 2026-05-10. Orchestrator + CLI + 7/7 integration tests + scaffold at `orgs/_TEMPLATE/`. | Customer onboarding gate. White-glove playbook subset at `docs/white_glove_v0_1_beta.md` §2. |

**Reading the table above:** any row marked ⭐ is where memory architecture work compounds. Reflection Packet + Funding Goal are both *memory* problems wearing different costumes.

---

## 4. The weaknesses — honest read

### Dimension 8 (Memory) = 4/10 — the load-bearing gap

The system has 13 distinct memory registers and **no unified retrieval API**:

```
Register                        Where it lives                                       Owner
─────────────────────────────────────────────────────────────────────────────────────────────
Cowork session memory           context window of the running Claude session         ephemeral
lessons.md + lessons.json       /lessons.md (human) + pipeline/institutional_memory/  operator-curated
daily_logs                      daily_logs/YYYY-MM-DD.md                              operator
lock_history.v1.jsonl           pipeline/engineering/lock_history.v1.jsonl            engineering
PROJECT_CONTEXT per-org         orgs/<slug>/PROJECT_CONTEXT.md                        per-org
KFR (Key Facts Register)        orgs/<slug>/vault/kfr/                                per-org, signed
classification register         orgs/<slug>/vault/classification/register.yaml        per-org, signed
Reflection Packet               orgs/<slug>/vault/operational/reflection_packets/     DORMANT v0.1
Funder Intel DB                 vault_shared/funder_intelligence/                     SPEC LOCKED, not built
Match DB                        orgs/<slug>/vault/match_db/                           SPEC LOCKED, not built
cache-ledger                    pipeline/observability/cache/                         per-call
session_log.jsonl               pipeline/metrics/session_log.jsonl                    per-session
CycleReceipt                    orgs/<slug>/vault/operational/cycle_receipts/         per-cycle, signed
```

Each register has its own access pattern (grep / read / yaml.load / sqlite open). **Per-cycle this is fine. Cross-cycle this is archaeology.** A Founding-12 customer with 5+ years of submission history will ask "show me every USDA submission I've ever made" in onboarding hour 1, and there is no answer that doesn't involve the operator browsing the tree by hand.

### The MEMORY.md overflow problem (observable today)

`memory/MEMORY.md` is the index file loaded into every new Cowork session. As of the assessment session: **35.6 KB. Limit: 24.4 KB.** The system reminder during that very session said: *"index entries are too long. Only part of it was loaded."*

The `consolidate-memory` skill exists but does not appear to fire on any threshold trigger — it runs only on operator invocation. On a customer's desk , MEMORY.md retrieval will silently degrade.

### Cross-cycle learning is operator-curated only

Today's mechanism for "this customer learned something on grant N that should influence grant N+1" = a human writes a lesson in `lessons.md` with an L-NNN tag. The infrastructure for automated cross-cycle learning is LOCKed (Reflection Packet at row 218); the runtime is DORMANT.

### Comparison points (industry posture, 2026 Q1-Q2)

- **Hermes Agent v0.13.0** (May 2026) shipped automatic reflection-after-task with 30% migration from OpenClaw in <90 days. Three memory layers (session / episodic SQLite / procedural skills).
- **Anthropic Memory + Letta** — three-tier memory pattern.
- **Mem0** — "bolt-on memory layer" for AI agents; production deployments at scale.

Tilth's design is *conceptually at parity* with all of these. **It is shipping behind all of them.**

### Other weaknesses worth knowing about

- **No `tilth metrics cycle-cost <cycle_id>` CLI.** The Coefficient Registry computes per-call energy + dollar coefficients; the per-cycle rollup that answers "what did this grant cost to write" is not assembled from CycleReceipt today. Sales objection on BYOK bill is unaddressed.
- **VLM-based parsing absent.** pypdf + python-docx + openpyxl substrate returns near-empty text on scanned RFAs (40-70% of legacy archives). F-EXTRACTOR-FABRICATION catches hallucinated extractions but cannot rescue extractions that don't happen.
- **EXIF / GPS / PII strip on `photos` sub-kind not specified.** Beneficiary GPS leak path is structural.
- **§0.5 Interface Index at 505 rows / 102 KB / 818 lines.** No automated test verifies that each row maps to a runtime import. Below the threshold where any single Thesis seat can hold the index in working memory.
- **L-005 two-cycle "fold-in-at-LOCK" workaround is a third round in disguise.** Three orthogonal F-* gate families (F-CLASS / F-WPFA / F-PACKET / F-REFLECTION) with AST-lint cross-family-import ban — organizational hygiene presented as runtime enforcement.

---

## 5. Where your work fits — Brain + JIT mapped onto Tilth gaps

This is the part of the doc you came here for. Both products map onto Tilth's weakest dimension *directly and structurally*.

### What Brain is (in Tilth ops vocabulary)

A four-store memory layer with a deterministic intent classifier (the "Thalamus") that routes queries to the right store, applies an outcome-weighted scoring formula, and exposes five MCP tool primitives (`r` recall / `s` store / `ss` session / `p` profile / `f` feedback).

**Four stores:**
- **Sensory** — recency buffer (<1 hour, working memory)
- **Episodic** — vector / semantic-similarity store (the workhorse)
- **Semantic** — knowledge graph (concept nodes + typed edges)
- **Chronological** — timestamped event timeline (time-range queries)

**Scoring math (authoritative, from `/reference/scoring-formula`):**
```
final_score = similarity × decay_factor × outcome_weight
decay_factor = 1 / (1 + decay_rate × age_days)
filter:  final_score ≥ score_threshold
```

**Outcome weights:** `success=1.2`, `neutral=1.0`, `failure=0.3` (asymmetric — failed approaches need 3.3× more similarity to rank equally).

**Class decay multipliers** (per episode `type`): `lesson=0.4` (2.5× slower), `decision=0.6` (1.7× slower), `session=1.0`, `default=1.0`.

**~25-field profile config** per namespace (full schema in `/reference/profile-field-reference`): `store_weights`, `decay_rate`, `score_threshold`, `outcome_tracking`, `retrieval_mode` (flat | parent-child), `cache_ttl_seconds`, `prefetch_enabled`, `max_results_per_store`, `response_format` (structured | text | minimal | **packed**), `abbreviation_dict`, `compression_preset` (brainpack | conversation), `context_brief_max_tokens`, `outcome_weights.*`, `reputation_low_threshold`, `reputation_high_threshold`, `reputation_min_outcomes`, `class_decay_multipliers.*`.

**BrainPack** — AI-native compression format claiming ~65% token reduction. **Packed format + abbreviation_dict** claims ~68% reduction on agent-consumed output.

**Concept reputation** — aggregate of outcomes on linked episodes; background Leiden community detection clusters related concepts.

### What JIT is

The delivery model for everything an agent needs to think — memory **plus skills, plugins, docs, conventions**. The Thalamus pulls only what the current task asks for, ranked by `semantic relevance × prior outcome`. Three steps, zero LLM calls, millisecond overhead.

Replaces "preload 47 skills + 12 plugins + 9 READMEs + 6 conventions into context just in case" with "thalamus → skill:deploy_ci (0.91) + plugin:docker_ops (0.77) — 3 artifacts delivered."

### The direct map onto Tilth gaps

| Tilth gap (from §4) | Brain primitive | JIT primitive |
|---|---|---|
| **13 registers, no unified retrieval API** | Thalamus intent classifier + four-store routing is the answer | — |
| **MEMORY.md overflowing today** | `response_format="packed"` + `abbreviation_dict` (~68% reduction). Decay + outcome weighting auto-prunes stale entries. | — |
| **Cross-cycle learning dormant** | Outcome weights (success 1.2× / failure 0.3×) + concept reputation accrual is *exactly* the substrate Reflection Packet was designed to feed | — |
| **No `tilth memory query` CLI** | Five-tool API surface (r/s/ss/p/f) is the working contract; wrappable as Pydantic AI tools | — |
| **Skill preloading bloat** | — | JIT Skills directly. `/brainpack-skills` already compresses Cowork SKILL.md files (Tilth-equivalent: pipeline/templates/skills/ + plugin skills) |
| **MEMORY.md auto-consolidation absent** | Brain's intelligent forgetting + temporal decay does this structurally — stale context deprioritized automatically | — |
| **Past-grant portfolio query absent** | Semantic store (knowledge graph) + cross-namespace discovery (under Law 3 constraints) + parent-child retrieval mode | — |
| **§0.5 Interface Index at 505 rows** | — | JIT for docs — surface only what current task asks for, ranked by relevance × outcome |
| **§0.5 not verifiable as runtime-mapped** | — | JIT discovery would force the issue — if an index entry never gets pulled, it pays no rent (vs. today paying paired-commit ceremony) |
| **No funder-mindset modeling (Dim 7)** | Concept reputation + Leiden community detection on funder knowledge graph; a USDA reviewer's concept cluster vs. a Surdna Foundation reviewer's cluster | — |

**The convergence in one sentence:** your built architecture for "AI memory that gets smarter over time + just-in-time delivery of everything an agent needs to think" is structurally what Tilth's weakest dimension is trying to build. Tilth's lessons.md + Reflection Packet schema + Match DB SPEC are the same shape; they have not yet been built into a running substrate.

### The honest disclaimers

1. **Brain is hosted SaaS** at `brain.amnesia-labs.com`. Tilth is local-sovereign. **Brain in its current shape cannot ship inside a Golden Quill appliance** — there is no self-host mode documented anywhere on the site (we crawled all 37 pages).
2. **Brain has no per-fact classification primitive.** Confidential / operator_flagged content cannot be routed to Brain under Tilth's v7.0.10 routing model without violating F-CLASS gates.
3. **Brain has no Ed25519-signed-by-operator action discipline.** Step-up auth is browser-based, account-bound — not headless-Logician-verifiable.
4. **Brain retains data indefinitely by default.** "Temporal decay only affects ranking, not storage" (FAQ verbatim). Tilth's Sovereignty Promise requires operator-controlled retention.
5. **Brain's namespace `discover` mode encourages cross-org bleed.** Tilth's Law 3 (Org Isolation) makes this structurally forbidden.

These disclaimers are not blockers — they are deployment-shape constraints that define *how* Brain/JIT lands inside Tilth, not *whether* it lands. See §7.

---

## 6. Why this isn't just convergence — it's complementary

Tilth has the disciplines Brain is missing. Brain has the runtime memory layer Tilth is missing.

### What Tilth has that Brain doesn't

- **Per-fact classification** (public / shareable / confidential / operator_flagged) with Ed25519-signed operator attestation
- **Cedar policy authoritative layer** with fail-closed `CriticalPolicyError(BaseException)` discipline
- **AST-lint structural enforcement** (e.g., `R-UPLOADER-NO-SUBMIT`, `R-ARCHIVIST-NO-CANONICAL-MUTATE`)
- **Logician deterministic gate primitives** — PRE + POST every seat call, zero token cost
- **Cross-family Thesis rigor** — Editor + Judge + Red Team must run on different model families
- **Signed-asset trust chain** for router-template, Coefficient Registry, KFR, CycleReceipt, classification register, buyer PDF
- **Verbatim-quote-with-page provenance** at every fact (the KFR primitive)
- **Decimal mandate** for monetary + energy quantities; no float arithmetic
- **Law 3 Org Isolation** — per-org Vault with structural cross-org leak prevention
- **content-hash binding** between proposal_commitments.yaml and submitted draft

### What Brain has that Tilth doesn't

- **Four-store backend** with deterministic routing (Sensory + Episodic + Semantic + Chronological)
- **Working scoring formula** with documented `similarity × decay × outcome_weight` math
- **Outcome-weighted ranking** that learns from feedback automatically
- **Concept reputation accrual** + background Leiden community detection
- **JIT delivery model** for skills + plugins + docs + conventions
- **BrainPack compression** (~65% reduction) + packed-format delivery (~68% reduction)
- **Operational portal UI** (tuning dashboard, episode management, graph explorer)
- **Working production traffic** through `brain.amnesia-labs.com` MCP endpoint
- **Five-tool API surface** that is clean, typed, and wrappable as Pydantic AI tools

### The merge thesis

Tilth's discipline + Brain's substrate = the first local-sovereign agent memory layer with operator-signed audit trail, per-fact classification, and outcome-weighted ranking that ships.

Industry has a long list of memory-layer products (Mem0, Letta, Hermes, Anthropic Memory). **None of them are sovereign.** All of them are SaaS or BYO-cloud-resources. The Golden Quill defensibility thesis  requires: workflow design + data access + authority + evals + audit trails — all owned by the customer. Brain's architecture is the missing piece if Tilth ports it into the appliance.

---

## 7. Possible deployment shapes — 


 Brain self-hostable variant inside Golden Quill (license required)

**What:** Amnesia Labs licenses Tilth a self-hostable Brain variant that runs *inside* the Golden Quill appliance. Brain becomes the **substrate that powers Reflection Packet runtime + Match DB + Funder Intel DB + unified `tilth memory query` CLI**. The four-store backend handles the substrate; Tilth's Cedar + Logician + classification register sit *above* Brain and gate every write/read.

**Pros:** Brain becomes the answer to Dim 8. The 13-register fragmentation collapses into the four-store backend with one routing layer. Reflection Packet's "what worked rises, what didn't fades" maps directly onto Brain's outcome weights. JIT skill delivery lands automatically.

**Cons:** Requires a license deal. Requires Brain to be packagable as a Golden-Image-shipped component (Pydantic AI + Logfire + Ollama/vLLM substrate plus Brain). Requires per-org isolation by namespace prefix discipline + an AST-lint rule + a Cedar policy preventing `discover` mode from crossing org slugs. Requires Brain's profile config to be operator-Ed25519-signed (today it's not).

**When:** This is the strategically correct move if a deal is possible. It accelerates v0.2 first wave by months and turns Brain into the running substrate behind the most expensive-to-build-from-scratch Tilth gap.



---

## 8. First-90-day load-bearing focus areas

 your first-90-day surface is roughly:

| # | Surface | Effort | Why |
|---|---|---|---|
| 1 | **Brain × Tilth integration shape definition**  — write the spec card, run a Thesis dispatch, get to a LOCK | 2-3 sessions | Without this, every downstream item is speculative. |
| 2 | **Reflection Packet v0.2 first-wave compound LOCK** — handoff already pre-staged at `pipeline/handoffs/ws_reflection_packet_v0_2_first_wave_handoff_2026-05-15.md` | 1-2 sessions + 1 LOCK round | The 18 NotImplementedError gates flip to LIVE. The highest-leverage Dim-4 + Dim-8 unblock. |
| 3 | **`tilth memory query` unified retrieval CLI** — Mem0-shape, Law-3-isolated, joins KFR + lessons + lock_history + CycleReceipt + classification register. If Shape B: this is a thin wrapper over Brain. If Shape A: this is the bridge. | 2-3 sessions | A Founding-12 customer asks *"show me every USDA submission I've ever made"* in onboarding hour 1. |
| 4 | **MEMORY.md auto-consolidation trigger** on size threshold (e.g., >20 KB → fire consolidate-memory skill automatically). | <1 session | MEMORY.md is overflowing in dev today. On a customer's desk after 3 months, retrieval silently degrades. |
| 5 | **`tilth metrics cycle-cost <cycle_id>` CLI** joining session_log + cache-ledger + Coefficient Registry. | 1 session | Customer's BYOK bill is the sales objection. Show them per-grant cost. |
| 6 | **Backup/restore story across all 13 memory registers** (or 4 stores if Shape B). Customer-contract item per Alpha Checklist #28. | 1 session doc + 1 session impl | Sovereignty Promise requires it. M3 Ultra SSD fails on day 90 — what's the procedure? |
| 7 | **VLM fallback path at Intake** (PaddleOCR VL or Granite 4.0 3B Vision) when pypdf returns degraded confidence. §11 v1.2 amendment. | 2 sessions | 40-70% of legacy customer archives are scanned PDFs. |
| 8 | **EXIF / GPS / PII strip on `photos` sub-kind insert.** Pre-write hook; opt-in retain. | <1 session | Structural PII leak path. Cheap fix. |

Items 1-3 are where memory-architecture work compounds. The rest are platform-engineering load-balanced across stability + token-efficiency + effectiveness pillars.

---

## 9. Honest read on integration risks

These are not blockers — they are things we will need to be careful about.

**Risk 1: Sovereignty regression.** Any deployment shape that routes confidential facts to a cloud service is a Law-3 violation. Shape A is fine for public/shareable only; Shape B requires that Brain self-hostable variant is genuinely off-network. The F-CLASS-* gate family must treat Brain as a cloud destination unless the runtime can prove it is inside the appliance's network namespace.

**Risk 2: Concurrent writes across council seats.** Brain's docs say multi-agent concurrent writes are "handled without conflicts" — mechanism unspecified (no CRDT, no MVCC, no Lamport-clock detail documented). For Tilth's council pipeline (multiple seats writing to the same namespace) we need a clear contract on ordering and conflict resolution. This is a question for Paul to answer before integration LOCK.

**Risk 3: Feedback loop is LLM-emitted.** Brain's `f()` outcome feedback is the agent's self-report of "did this help?" There is no operator audit hook today. For Tilth, every Reflection Packet outcome must be operator-Ed25519-signed before it weights the ranking. This requires either a Brain extension (operator-signed feedback) or a Tilth wrapper layer that intercepts `f()` calls.

**Risk 4: Cross-namespace `discover` mode.** Brain's default is "let knowledge bleed usefully across projects." Tilth's default is "per-org Vault, never cross." Disabling `discover` mode + enforcing namespace-prefix discipline at the wrapper layer is required.

**Risk 5: Profile updates as configuration drift.** Brain's `p(action="set")` lets the LLM update its own routing profile. For Tilth, profile changes must be operator-Ed25519-signed (same trust mechanism as router-template + classification register).

**Risk 6: Vault step-up auth is browser-based.** Brain's Vault uses browser-MFA for sensitive actions. Tilth's discipline is operator-Ed25519-signed attestation in audit log. These are different trust models; they need to align if Brain Vault is integrated.

**Risk 7: Class decay multiplier `lesson=0.4` is faster than Tilth wants.** A 2.5× slower decay still implies eventually fading lesson relevance. Tilth's `lessons.md` is *forever* — lessons are mandatory pre-checks across all sessions. The class decay multipliers may need a `permanent=0.0` entry for Tilth's most-load-bearing lesson class.

---

## 10. What surfaced after this brief was first filed today — card realization workstream + Dim 7 deeper truth

This section consolidates what landed in the same session that produced the brief above. It is additive — nothing earlier retracts. If you read only one of these subsections, read 10.4 (the merge thesis enrichment).

### 10.1 Honest deeper truth — Dim 7 is structurally weaker than 7/10 suggests

The 2026-05-11 proficiency assessment scored Dim 7 (Council Topology) at 7/10 with the line *"the architecture has dialect; it does not have mindset."* A runtime check later in this same session (CIC × CLC card investigation dispatched against the actual code tree, not against CLAUDE.md narrative) confirmed: the architecture has dialect — Law 4 funder-dialect code-switch is implemented globally in `pipeline/seats/scribe/dialect.py` — but **no funder-mindset card per CIC or per CLC**.

The 14 cards at `assets/cards/customer_identification/*.png` and `assets/cards/capital_logic/*.png` document grant-writing acumen as four-quadrant visual artifacts (Operating Reality · Tilth Configuration · Evidence Signals · Funding/Reporting Rhythm) and promise five primitives per card (Search Vocabulary · Evidence Schema · Language Register · Reporting Rhythm · Capital Logic Activation). The runtime currently has:

- 2 closed-set enums at `pipeline/types/identity_capital.py` — `CustomerIdentityCategory` (6 literals) + `CapitalLogicCard` (8 literals) + display dictionaries + `canonical_cic_count()` + `canonical_clc_count()`.
- 4 validation gates: `F-CIC-CLC-ENUM-DRIFT` + `F-CIC-CLC-COUPLING-VIOLATION` + `F-CIC-CLC-MATCH-NULL` + `F-MULTI-CIC-CHOICE-UNRESOLVED`.
- **Zero per-CIC behavioral differentiation in Scribe / Scout / Judge / Editor.** Confirmed: Scribe reads `cic_active` from PROJECT_CONTEXT for gate validation; does not switch behavior on it.
- **Zero per-CLC underwriting differentiation.** Judge's cross-rubric dispatch is real but per-program (one rubric so far: VAPG FY26 — 100pt 7-criterion), not per-CLC.

This makes Dim 7's effective score closer to 5/10 once the runtime check is honored. The substrate is real (full module trees for each seat); the mindset modeling per card is not implemented. Encoding it is the card-realization workstream.

### 10.2 The 14 cards — what needs to be runtime-encoded

Full inventory at `docs/grant_writing_technical_acumen_inventory_2026-05-15.md`. The shape:

- **6 CIC cards** (one per Customer Identity Card): Food Systems, Educator, Public Agency, Arts & Culture, Cooperative, Ecosystem Intermediary. **14 fields per card**: identity + search vocabulary + evidence schema + KFR fact-class extension + language register + dialect routing + admin-risk term register + reporting cadence + metrics_table_template + capacity signals + compliance burdens + risk register + observational CLC patterns + observational funder corpus.
- **8 CLC cards** (one per Capital Logic Card): Public Purpose & Works, Catalytic Change, Operating Capacity, Research & Evidence, Market Access, Credit & Underwriting, Sponsorship & Corporate Support, Shared Assets. **13 fields per card**: identity + underwriting criteria + scoring weight patterns + evidence weights + application forms + narrative section patterns + budget structure conventions + reviewer profile + portal list + red flags + reporting requirements + compliance obligations + commitment tracking pattern.
- **(CIC × CLC) intersection knowledge** lives as concept-graph weighted edges (observational/advisory only — `F-CIC-CLC-COUPLING-VIOLATION` continues to fail-close any subset eligibility binding per architecture v7.0.8).

The cards encode what makes a Food Systems applicant differ from a Cooperative applicant in Scribe's vocabulary, what makes a Catalytic Change funder differ from a Public Purpose funder in Judge's scoring weights, and what framing pivots make an unusual intersection legible to that funder's reviewers.

### 10.3 The deep-research dispatch — how the cards get populated

Parameterized prompt at `pipeline/handoffs/deep_research_cic_clc_card_handoff_2026-05-15.md`. Fires per card (14 dispatches total; parallelizable). Five-phase workflow: **Phase 1** prior-art absorption (8 file paths mandatory before web research, per L-002 reference-not-content discipline); **Phase 2** primary research (read 5 awarded applications per CIC OR 3 exemplary NOFOs per CLC; verbatim-quote-with-page provenance); **Phase 3** YAML drafting (Schema A for CIC + Schema B for CLC; required-field flagging for operator-curate cells); **Phase 4** self-validation per Rule 2 (schema completeness + provenance + L-002 + F-CIC-CLC-COUPLING-VIOLATION + cross-reference against existing knowledge packs + card content fidelity); **Phase 5** hand-back. Cross-family Thesis on each card before LOCK (Editor / Judge / Red Team on different model families per L-005 two-cycle discipline). Operator Ed25519-signs each card before runtime load.

Effort: 2-4h research + 30-60 min operator review + ~$15-30 Thesis spend per card. Total 14 cards ≈ 60-80 operator-hours serialized OR 3-5 weeks parallelized — same order of magnitude as authoring a single full grant proposal.

**Wave 1 (schema validation):** Food Systems CIC + Operating Capacity CLC. Six open operator decisions surfaced before Wave 1 fires (handoff §8): sector-vs-CIC reconciliation / Brain × Tilth deployment shape / output path convention / verbatim-quote-length bar / admin_risk approval default / win-rate quantification policy.

### 10.4 The merge thesis enrichment — where your work most directly carries grant-writing substance

Section 6 of this brief said *"Tilth's discipline + Brain's substrate = the first local-sovereign agent memory layer with operator-signed audit trail, per-fact classification, and outcome-weighted ranking that ships."* That's true at the substrate layer. With cards in scope, the thesis enriches:

**Tilth's grant-writing acumen (encoded as 14 cards) + Brain's substrate = the first sovereign agent memory layer with *substance* per customer archetype and per capital logic — not just retrieval primitives.**

Industry's memory-layer products (Mem0, Letta, Hermes, Anthropic Memory) all provide retrieval mechanics. **None of them carry grant-writing substance.** None of them differentiate behavior per customer archetype. The card-realization workstream is what turns Brain's four-store backend into a grant-intelligence engine, not just a memory cache.

This is also where your work most directly carries grant-writing substance. The platform-engineering work of standing up Brain and integrating it under Tilth's classification + signing discipline is the **substrate work**. The card research is the **content work**. The two are separable but co-designed — the card schema gates the namespace + profile config + concept-graph design. If Shape B (self-hostable Brain inside Golden Quill) lands, both workstreams converge into your operating surface.

### 10.5 Updated impact on the proficiency assessment

Combined impact of CIC × CLC card realization + Reflection Packet v0.2 first-wave compound LOCK (the latter LOCKED earlier today at lock_history rows 216-218):

| Dim | Pre-update | Post-update | Why |
|---|---|---|---|
| Dim 7 Council Topology | 7/10 (honest read: closer to 5/10 per §10.1) | ~9/10 | Funder-mindset card per card unlocks behavioral differentiation in Scribe + Judge + Red Team |
| Dim 8 Memory | 4/10 | ~7/10 | Reflection Packet runtime + unified retrieval CLI + auto-consolidation |
| Dim 4 End-to-end cycle | 6/10 | ~8/10 | Cross-cycle learning live; card-aware drafting tightens funder-fit |
| Other dims | unchanged | unchanged | |
| **Total** | **47/80** | **~55/80** | comfortably past Beta-ready on the desk-Beta thesis |

### 10.6 What Shape B (per §7 above) gains with cards in scope

If Brain self-hostable variant lands inside Golden Quill, the cards land as Brain seed data per the namespace + profile-config + concept-graph mapping at `docs/grant_writing_technical_acumen_inventory_2026-05-15.md` §6. Per-CIC profile config example:

```yaml
# tilth:cic:food_systems
store_weights: {episodic: 0.30, semantic: 0.50, chronological: 0.15, sensory: 0.05}
decay_rate: 0.005          # ~200-day half-life — card knowledge is slow-changing
score_threshold: 0.55
retrieval_mode: parent-child
outcome_weights: {success: 1.5, neutral: 1.0, failure: 0.2}
class_decay_multipliers: {lesson: 0.2, decision: 0.4, session: 1.0, default: 1.0}
```

Concept-graph seed example for Food Systems: evidence concepts (`soil_health_evidence`, `market_access_evidence`, `cooperative_structure_evidence`, `production_capacity_signal`) linked to CLC concepts by weighted advisory edges (e.g., `{from: "cooperative_structure_evidence", to: "operating_capacity_clc", type: "demonstrates", weight: 0.9}`) — NOT subset eligibility bindings (F-CIC-CLC-COUPLING-VIOLATION continues to fail-close those).

Wrapper discipline required to preserve Law 3 Org Isolation: a new `R-BRAIN-CROSS-ORG-DISCOVER-FORBIDDEN` AST-lint rule plus an `F-BRAIN-CROSS-ORG-LEAK` Logician gate. Profile updates must be operator-Ed25519-signed (same trust mechanism as router-template + classification register). Brain's `discover` mode is default-on and cross-namespace by design; the wrapper layer must constrain it to per-org namespace whitelists.

### 10.7 Updated §8 first-90-day item #1

Section 8 first-90-day item #1 was *"Brain × Tilth integration shape definition (Shape A or B) — write the spec card, run a Thesis dispatch, get to a LOCK."* With cards in scope, that item expands into sub-items:

| Sub-item | What it is |
|---|---|
| 1a | Brain × Tilth integration shape decision (Shape A / B / C) |
| 1b | CIC × CLC card schema review + 6 open-operator-decision pass at `pipeline/handoffs/deep_research_cic_clc_card_handoff_2026-05-15.md` §8 |
| 1c | Wave 1 dispatch (Food Systems CIC + Operating Capacity CLC for schema validation) |
| 1d | Cross-family Thesis on first 2 cards (L-005 two-cycle discipline) |
| 1e | Operator Ed25519-sign + runtime-load mechanism implementation per chosen shape |

The rest of §8 first-90-day items (Reflection Packet v0.2 first-wave / unified memory-query CLI / MEMORY.md auto-consolidation / cycle-cost CLI / backup-restore / VLM fallback / EXIF strip) remain unchanged.

### 10.8 What's now in flight vs what was in flight when the brief was first filed

The brief's original §3 Beta-set table listed Reflection Packet as *"LOCKED 2026-05-15 (rows 216-218). 19 F-PACKET-* codes — 18 raise NotImplementedError; 1 LIVE META gate."* That LOCK landed in the same session as this brief — confirmed at `pipeline/engineering/lock_history.v1.jsonl` rows 216-218. The v0.2 first-wave compound LOCK (producer-flip + sub-kind registration + 18 predicate-body NotImplementedError→LIVE flips) is pre-staged at `pipeline/handoffs/ws_reflection_packet_v0_2_first_wave_handoff_2026-05-15.md` and is still the highest-leverage Dim 4 + Dim 8 single unblock.

New since the brief was first filed:

- Grant-writing technical acumen inventory (§10.2) — written today
- Deep-research dispatch packet (§10.3) — written today
- CIC × CLC runtime investigation (§10.1) — confirmed cards are diagrams; runtime is type-safety + 4 gates + zero behavioral differentiation per card

Nothing in the original brief is retracted by this update. The §7 deployment shapes (A / B / C) are unchanged; the only enrichment is §10.6's per-CIC namespace profile + concept-graph seed example showing exactly what Shape B would carry once cards land.

---

## 11. Sources

**Tilth-side primary sources:**

- `pipeline/planning/architecture_proficiency_assessment_result_2026-05-11.md` — 8-dimension assessment, 47/80, full per-dimension scoring + recommendations
- `pipeline/validation/architecture_proficiency_2026-05-11/evidence_pack.md` — evidence backing the assessment
- `pipeline/planning/architecture_proficiency_assessment_prompt_2026-05-11.md` — assessment rubric
- `pipeline/research/advancements_scan_2026-05-15.md` — 60-day SOTA scan (Hermes / Mem0 / Letta / KnowQL / Voxtral / PaddleOCR VL etc.)
- `pipeline/engineering/lock_history.v1.jsonl` — architectural change ledger (218 rows as of crawl)
- `docs/platform_engineer_onboarding.md` — companion: full Tilth surface for incoming engineer
- `docs/platform_engineer_quick_reference.md` — companion: 1-page daily-driver

**Amnesia Labs primary sources (this session):**

- `https://amnesia-labs.com/brain` — Brain marketing page (PDF supplied)
- `https://amnesia-labs.com/jit` — JIT marketing page (PDF supplied)
- `https://docs.amnesia-labs.com/` — full docs index (HTML supplied)
- `https://docs.amnesia-labs.com/getting-started/installation` — installation flow + MCP endpoint + Bearer token auth
- `https://docs.amnesia-labs.com/getting-started/first-session` — five MCP tool primitives surface
- `https://docs.amnesia-labs.com/core-concepts/how-memory-works` — four-store backend (Sensory / Episodic / Semantic / Chronological) + Thalamus router
- `https://docs.amnesia-labs.com/core-concepts/namespaces` — namespace model + discover mode
- `https://docs.amnesia-labs.com/core-concepts/sessions` — work-session boundaries + key_decisions as graph nodes
- `https://docs.amnesia-labs.com/core-concepts/the-learning-loop` — three-timescale feedback (L1 per-recall / L2 weeks / L3 manual)
- `https://docs.amnesia-labs.com/using-brain/storing-knowledge` — `s(target=...)` unified store with five targets
- `https://docs.amnesia-labs.com/using-brain/recalling-knowledge` — `r(query, mode, namespaces[])` with `discover` mode
- `https://docs.amnesia-labs.com/using-brain/giving-feedback` — `f()` agent-driven feedback
- `https://docs.amnesia-labs.com/using-brain/managing-sessions` — `ss(action, ...)` session lifecycle
- `https://docs.amnesia-labs.com/using-brain/cross-namespace-discovery` — `target="cross_reference"` + `mode="discover"`
- `https://docs.amnesia-labs.com/using-brain/vault` — secrets vault with drop-link + `vault-run` helper + step-up auth (BETA)
- `https://docs.amnesia-labs.com/using-brain/well-known-namespaces` — reserved namespaces (vault, errors, conventions, skills, infra, contacts, urls, toolbox)
- `https://docs.amnesia-labs.com/tuning/understanding-profiles` — ~25-field profile config
- `https://docs.amnesia-labs.com/tuning/decay-rate` — half-life table + `decay_factor` formula
- `https://docs.amnesia-labs.com/tuning/store-weights` — defaults + per-domain weighting profiles
- `https://docs.amnesia-labs.com/tuning/score-threshold` — 0.5 default + selectivity bands
- `https://docs.amnesia-labs.com/tuning/outcome-weights` — `success=1.2 / neutral=1.0 / failure=0.3` + class decay multipliers
- `https://docs.amnesia-labs.com/tuning/retrieval-mode` — `flat` vs `parent-child`
- `https://docs.amnesia-labs.com/tuning/packed-format` — `response_format=packed` + `abbreviation_dict` (~68% token reduction)
- `https://docs.amnesia-labs.com/tuning/cache-and-prefetch` — `cache_ttl_seconds=300` default + cache auto-invalidates on writes
- `https://docs.amnesia-labs.com/tuning/profile-recipes` — code-as-config recipes for 7 domains
- `https://docs.amnesia-labs.com/advanced/automation-patterns` — REST API at `/api/v1/` + plugin hook lifecycle + `/brainpack-skills` slash command
- `https://docs.amnesia-labs.com/advanced/compression` — BrainPack ~65% + conversation preset ~70%
- `https://docs.amnesia-labs.com/advanced/concept-reputation` — reputation thresholds + background Leiden community detection
- `https://docs.amnesia-labs.com/advanced/research-tool` — `/knowledge` slash command + parallel research agents
- `https://docs.amnesia-labs.com/reference/tool-reference` — full 5-tool surface signatures
- `https://docs.amnesia-labs.com/reference/glossary` — BrainPack / Thalamus / Vault / Drop link / Step-up auth / Discover mode / Parent-child mode / Class decay multiplier
- `https://docs.amnesia-labs.com/reference/profile-field-reference` — authoritative ~25-field profile config table
- `https://docs.amnesia-labs.com/reference/scoring-formula` — `final_score = similarity × decay_factor × outcome_weight`
- `https://docs.amnesia-labs.com/portal/overview` — portal home
- `https://docs.amnesia-labs.com/portal/tuning-dashboard` — namespace profile editor UI
- `https://docs.amnesia-labs.com/portal/episode-management` — per-namespace episode browser with outcome history
- `https://docs.amnesia-labs.com/portal/graph-explorer` — knowledge-graph visualization
- `https://docs.amnesia-labs.com/troubleshooting/common-issues` — MCP URL canonical form
- `https://docs.amnesia-labs.com/troubleshooting/recall-quality` — tuning-failure decision tree
- `https://docs.amnesia-labs.com/troubleshooting/faq` — **sovereignty-relevant**: indefinite retention, hosted-only deployment, account-isolation as the only privacy primitive

Crawl exhaustive: 37 doc pages reachable + root index. No `/api`, `/openapi`, `/changelog`, `/pricing`, `/terms`, `/privacy`, `/security`, `/legal`, `/sdk`, or `/integrations` pages exist on the docs subdomain (all confirmed 404). No public source repo linked anywhere.

---

**End of brief.** Companion: `docs/platform_engineer_onboarding.md` for full Tilth project surface. Open questions, push-back, or alternative deployment shapes welcome.
