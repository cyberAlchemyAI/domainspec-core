---
scope: session orientation — read once at session start
purpose: replace encoding the entire project universe into handoff prompts
created: 2026-04-19
---

# Session Bootstrap — Golden Quill / Tilth

Read this file to orient a new session. Then read task-specific files as needed. Do NOT paste this file's contents into handoff prompts — reference by path.

## Project Identity

**Golden Quill** = physical hardware (128 GB desktop, gold case). One per client.
**Tilth** = agentic software intelligence inside Golden Quill. Six-seat AI council (Scout, Scribe, Editor, Judge, Red Team, Logician) plus support agents (Intake, Uploader for v0.1; Data Collector, Report Generator for v0.2; Archivist for v1.x). Grant intelligence for regenerative agriculture, land/community development, and eco-art.
**FIT Farms** = Josh's operating entity. "FIT Farms Commons" = owner/operator file label. "FIT Farms LLC" under `orgs/` = grant-writing client label.
**Operator:** Josh Inklovich. Solo builder. Does not code. Uses Cowork. Sets the agenda.

## Wake-Up Sequence

Per `/AGENTS.md` — run in order, non-optional:
SOUL.md → USER.md → router.yaml → last two daily_logs → lessons.md → MEMORY.md index → agent-specific overrides → task-specific PROJECT_CONTEXT

## Canonical File Locations

| What | Where |
|------|-------|
| Operating principles (Five Laws, Four Rules) | `/SOUL.md` |
| Operator identity + decision framework | `/USER.md` |
| Agent wake-up + invocation rules | `/AGENTS.md` |
| Model bindings (SOLE source) | `/router.yaml` |
| Memory index | `/MEMORY.md` |
| Lessons (mandatory pre-checks) | `/lessons.md` |
| Locked architecture (v7, A1-A12, LOCKED 2026-04-19) | `pipeline/architecture/v0.1/tilth_architecture_locked.md` |
| Pending v7.0.1 amendment (Section E.P GPP, DRAFT) | `pipeline/architecture/v0.1/architecture_v7_0_1_amendment.md` |
| Blueprints | `pipeline/blueprint/v0.1/` |
| Component analysis template | `pipeline/templates/component_analysis_template.md` |
| Client orgs | `orgs/` (see `orgs/ORG_INDEX.md`) |
| Handoff docs | `Sovereign_Node_Handoff/` |
| Audit trails | `pipeline/validation/` |
| Daily logs | `daily_logs/` |
| Institutional memory (machine) | `pipeline/institutional_memory/lessons.json` |
| Rubrics | `pipeline/rubrics/` |
| Pipeline orchestrator | `pipeline/orchestrator/` |
| Engineering specs | `pipeline/engineering/` |
| Handoff prompts | `pipeline/handoffs/` |
| Integration scope-close (active) | `pipeline/validation/integration_scope_close_2026-04-19/` |
| Session metrics spec | `pipeline/metrics/SESSION_METRICS_SPEC.md` |
| Session metrics log | `pipeline/metrics/session_log.jsonl` |
| Efficiency audit template | `pipeline/templates/efficiency_audit_agent.md` |

## Locked Decisions (v0.1 — closed, do not reopen)

- No LangGraph, no NemoClaw, no Phase 3 orchestration. (Local inference via Ollama/vLLM is in-scope per ADR-001 / v7.0.3 substrate amendment; 70B-class local-routable models for Editor/Red Team/routine-Judge and on-demand 200B-class heavy-Judge swap are in-scope per v7.0.7 classification-driven routing LOCKED 2026-05-10.)
- No Managed Edition, no metered billing — BYOK only
- No UI layer — headless only
- No PA Ag Innovation Grant as dogfood target
- Architecture v7 LOCKED 2026-04-19 (A1-A12). Changes = new audit round.
- v7.0.1 amendment (Section E.P Governance Plan Preflight) is DRAFT — awaiting Tier 1/2/3 GPP + L-005 Thesis round. LOCKs atomically with §4 v2.1.1 + §0.5 v5 paired blueprint amendments.
- 128 GB RAM production floor (retires 64/32 GB references)
- Two-audit cycle per L-005 (not three-round silent revision)

## Active Constraints

- **Dev hardware:** M1 Mac Mini, 8 GB RAM. If it runs here, it flies on 128 GB.
- **Headless only:** no UI in v0.1.
- **BYOK only:** client owns all API keys.
- **Fail-closed:** Logician gates refuse by default. M13 is the only bypass, audited.
- **Cross-family review:** reviewer model family must differ from author's (L-003). **Cowork sessions reach the local openclaw gateway via `mcp__Control_your_Mac__osascript` → `do shell script "PATH=$HOME/.npm-global/bin:$PATH openclaw infer model run --gateway --model X --prompt P --json" with timeout of 600 seconds`.** Three live model IDs: `groq/llama-3.3-70b-versatile` (Editor) / `google/gemini-2.5-pro` (Judge) / `groq/openai/gpt-oss-120b` (Red Team). Working templates: `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`. Section E single-Claude carve-out requires a *logged dispatch failure* to invoke — not a default fallback. Full discipline in `/AGENTS.md` § "Cross-family review — bridge pattern" + § "Section E carve-out — invocation discipline".
- **Path references, not content dumps:** never paste file contents into prompts (L-002).
- **Enforcement-layer existence:** verify on-disk before locking around it (L-006).

## Five Operating Laws (summary — canonical in SOUL.md)

1. RFA Is Truth — every claim traces to RFA or PROJECT_CONTEXT
2. No Boundary Drift — stay inside RFA scope
3. Org Isolation — one PROJECT_CONTEXT per session, never cross-reference
4. Apolitical Language + Admin-Risk — code-switch dialect, never silently rewrite flagged terms
5. Applicant Brings Substance — no fabricated credentials/data/partnerships

## Four Autonomy Rules (summary — canonical in SOUL.md)

1. Save State Always (success AND failure)
2. Test Your Own Work (validate before marking complete)
3. Be Explicit (input path, output path, scope, done-definition)
4. Clean Output (strip fences/fluff/commentary, validate format)

## Council Seats (six — roles only; model bindings in router.yaml; per v7.0.6 SELF-LOCKED 2026-05-09)

- **Scout** — two-stage discovery (DISCOVER wide → VERIFY live → REVIEW human gate)
- **Scribe** — drafts proposals with KGIE preflight, SMART outcomes, funder dialect
- **Editor** — clarity review, jargon flagging, goal/output/outcome/objective sorting
- **Judge** — scores against funder's rubric, then cross-checks rubric library
- **Red Team** — adversarial challenge with cross-family rigor against Scribe and Judge; >10pt disagreement triggers council split (human decides per Law 4)
- **Logician** — deterministic Python + Cedar validation, fail-closed, all Five Laws as PRE/POST gates

## Support Agents (per v7.0.6)

- **Intake** (v0.1, onboarding, always-local) — KFR bulk-ingestion at white-glove setup; verbatim-quote provenance; operator confirms each fact
- **Uploader** (v0.1, submission, always-local) — submission package assembly; prepare-and-stage discipline only — operator clicks final submit
- **Data Collector** (v0.2 horizon) — grantee/sub-awardee outreach (email/SMS/voice/Telegram/WhatsApp); compliance-first
- **Report Generator** (v0.2 horizon) — funder-ready reports from Data Collector data; Logician PRE/POST discipline
- **Archivist** (v1.x horizon, between-cycle) — Funder Intelligence DB, Match DB, KFR maintenance, lessons memory, audit trail
- **WPFA Cycle Accountant** (v0.1, cycle-close, always-local) — emits typed CycleReceipt at every cycle close; computes actual vs counterfactual dollars + watt-hours per the SN-LLC-signed Coefficient Registry; operator Ed25519 attestation gates buyer-facing PDF; deterministic module (no LLM-routed sub-agents). §17 v1 LOCKED 2026-05-11 (rows 205-208).

## Operational Gears

- **Sparring Partner** — seat generates options, human decides
- **Co-Pilot** — human provides direction, seat executes and refines (DEFAULT)
- **Synthesizer** — full delegation, human reviews final output only

## Session Efficiency Rules

- **Batch questions.** Collect all open questions into one message. Do not ask sequentially.
- **Match Josh's register.** Terse, decisive, no ceremony. Thorough but not performative.
- **Reference, don't repeat.** Point to `pipeline/templates/component_analysis_template.md` instead of restating framework. Point here instead of re-explaining the project in handoffs.
- **Batch file operations.** Plan reads/writes before executing. Minimize round trips.
- **Path references only.** Never paste file contents into prompts (L-002).
- **No redirect.** Answer the question asked. Do not lecture about priorities.

## Six-Sector Scope

Workforce of the future, future-proof education, regenerative agriculture, urban/soilless ag, land and community development, eco-art.

## Product Arc

Stage 1 Solo operator (v0.1, current — one Tilth, Josh's) → Stage 2 Twelve Tilths (12-deployment fleet milestone — proves model at small-fleet scale; multi-seat Cultivator per Tilth; Law 3 isolation tested across fleet) → Stage 3 Cooperative org → Stage 4 Contractor federation → Stage 5 Sovereign Node commons online (cooperative-owned compute; cross-Tilth network effect engages per consent tier).

Stages 2-5 are future. "Sovereign Node" (no LLC) is internal-only Stage-5 naming for the commons compute. Disambiguate from "Sovereign Node LLC" (parent legal entity, real today). MaatAI retired as a name 2026-05-06; full naming chain in `memory/project_sovereign_node_stage5.md`. Motto: "One Sovereign Node, Many Tilths."
