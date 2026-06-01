---
title: Tilth Architecture — Amendment v7.0.6 (Council and support-agent roster — Red Team surfaced into canonical, Uploader and Intake added for v0.1, Data Collector + Report Generator + Archivist named for forward horizons)
filed: 2026-05-08
operator: Josh Inklovich
amendment_status: SELF-LOCKED 2026-05-09 — textual roster amendment; zero mechanism change; reconciles canonical seat lists with router.yaml on-disk reality (Red Team) and names new agents (Uploader, Intake) for v0.1 plus reserves v0.2 horizon (Data Collector, Report Generator) and v1.x horizon (Archivist) slots.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_3_amendment.md
companion_files_pending_edit:
  - "README.md (Council table — 5 rows to 6 rows adding Red Team; new Support Agents section adding Intake + Uploader; Roadmap mention of v0.2 Data Collector + Report Generator and v1.x Archivist)"
  - "docs/ARCHITECTURE_OVERVIEW.md (Five Seats diagram becomes Six Seats; canonical seat list adds Red Team; new section for support agents)"
  - "CLAUDE.md (council seats description if needed; What NOT to Do guards extended for new agents as relevant)"
  - "pipeline/architecture/v0.1/tilth_architecture_locked.md (Section A council enumeration line adds Red Team to canonical seat list)"
authority_source: router.yaml (Red Team already wired with cross-family rigor design); pipeline/blueprint/v0.1/section_07_scribe.md and section_04_logician.md (split-context drafting and PRE/POST gates compose with the new agent roster); memory/project_archivist_v1x_candidate_seat.md (Archivist v1.x candidate confirmed)
version_wording_discipline: "LOCKED" inside this file refers to on-disk LOCKED state at filing time. Forward-pending agents (Data Collector, Report Generator, Archivist) are named and slot-reserved here; their full specs live in future amendments tied to the v0.2 reporting vertical and v1.x curation work.
---

# Amendment intent

Three roster gaps surfaced in the 2026-05-08 architecture pass:

1. **Red Team is wired in `router.yaml` with cross-family rigor design but missing from canonical seat lists.** README Council table, ARCHITECTURE_OVERVIEW Five Seats diagram, and v7 LOCKED Section A all describe a "5-seat council" while router.yaml carries Scout / Scribe / Editor / Judge / Red Team / Logician with explicit cross-family rigor between Red Team and the other LLM seats (per `router.yaml` red_team comment 2026-04-19). The canonical lists are stale.

2. **v0.1 lacks named submission and onboarding agents.** Two operator workflows currently fall through: (a) at end of grant cycle, no agent assembles and stages the submission package for the funder portal; (b) at client onboarding, no agent ingests org documents into KFR with operator-confirmation discipline. Both functions exist as operator-driven manual work in v0.1; naming and scoping them as agents puts the work where it belongs and clarifies the pipeline.

3. **v0.2 reporting vertical and v1.x curation work need named placeholders.** Memory entries name Data Collector + Report Generator (for v0.2 post-award reporting) and Archivist (for v1.x between-cycle curation) but the architecture has no placeholder slot. v7.0.4 KFR amendment and v7.0.5 Funder Intelligence Database + Match Database amendment will need to reference these agent names cleanly; v7.0.6 reserves the slots so v7.0.4 and v7.0.5 can compose against them.

This amendment is **textual roster reconciliation only**. No A-letter mechanism is modified. No new failure code is introduced. No new Cedar rule, no new admin-risk register row, no new out-of-model anchor. The agents named here for v0.1 (Uploader, Intake) get their full specs in companion blueprint sections — those specs are NOT part of this amendment. The agents reserved for v0.2 / v1.x horizons (Data Collector, Report Generator, Archivist) get their full specs in future architecture amendments aligned to those product milestones.

# What changes (Section A canonical lineup)

**Replace** (the v7 LOCKED + v7.0.3 canonical-lineup summary, currently understated):

> Tilth operates as a five-seat AI council: Scout, Scribe, Editor, Judge, Logician.

**With**:

> Tilth's v0.1 council comprises six seats: Scout (discovery), Scribe (drafting), Editor (clarity review pre-Judge), Judge (scoring against funder rubric), Red Team (adversarial challenge with cross-family rigor against Scribe and Judge), and Logician (deterministic policy gates PRE/POST). Plus two support agents in v0.1: Intake (KFR ingestion at client onboarding) and Uploader (submission package assembly, prepare-and-stage discipline — operator clicks final submit on funder portal). Forward-named for v0.2 reporting vertical: Data Collector (post-award grantee outreach and data acquisition) and Report Generator (post-award reporting using Data Collector's output). Forward-named for v1.x curation horizon: Archivist (between-cycle preservation of Funder Intelligence Database, Match Database, KFR maintenance, lessons.json, audit trail).

**Authority.** `router.yaml` red_team block (Red Team primary `groq/openai/gpt-oss-120b`, fallback `anthropic/claude-haiku-4-5`, escalation `openai/gpt-5.1`); cross-family rigor commentary in `router.yaml` (Red Team distinct family from Scribe / Judge / Editor); memory/project_judge_thesis_review_board.md (Thesis Team = Editor / Judge / Red Team).

# Agent roster — full enumeration with scope marker

| Agent | Layer | Status | Role |
|---|---|---|---|
| Scout | Council seat | LOCKED v7 | Two-stage discovery (DISCOVER + VERIFY across six parallel channel families) |
| Scribe | Council seat | LOCKED v7 | Section-by-section drafting with KGIE preflight, SMART outcomes, funder-dialect code-switching |
| Editor | Council seat | LOCKED v7 (pre-Judge position confirmed 2026-05-08) | Clarity review through different model family eyes; flags issues with 2-3 ranked replacement options |
| Judge | Council seat | LOCKED v7 | Scoring against funder's own rubric first, then library; cross-family rigor with Scribe |
| Red Team | Council seat | LOCKED in router.yaml; canonical lineup add (this amendment) | Adversarial challenge with cross-family rigor against Scribe and Judge; disagreement >10 points triggers human-decides council split (Law 4 tie-breaker) |
| Logician | Council seat | LOCKED v7 | Deterministic Python + Cedar policy gates; PRE before Scout, POST after Judge; zero token cost |
| Intake | Support agent — onboarding | NEW v0.1 (this amendment names it; full spec in v7.0.4 KFR Amendment companion blueprint) | KFR bulk-ingestion from operator-uploaded org documents; extracts candidate facts with verbatim-quote-with-page provenance to `pending_facts.yaml` queue; operator confirms → promotes to KFR |
| Uploader | Support agent — submission | NEW v0.1 (this amendment names it; full spec in v7.0.6 companion blueprint or follow-on amendment) | Submission package assembly; renders final operator-approved proposal to funder-portal-required formats; surfaces "ready to submit" to operator. Prepare-and-stage discipline only — operator clicks final submit on funder portal. Full-submit is OUT OF SCOPE for v0.1 due to federal-portal ToS and operator-accountability constraints. |
| Data Collector | Support agent — post-award | NAMED v0.2 horizon (full spec in v0.2 reporting vertical amendment) | Outreach to grantees and sub-awardees via email / text / voice for performance data, evidence, milestone reports. Compliance-heavy: CAN-SPAM, TCPA, state robocall restrictions, per-recipient consent capture at award acceptance. Stores collected data for Report Generator. |
| Report Generator | Support agent — post-award | NAMED v0.2 horizon (full spec in v0.2 reporting vertical amendment) | Generates funder-ready reports using Data Collector's gathered data. Same Logician PRE/POST discipline as v0.1 council seats. |
| Archivist | Support agent — between-cycle | NAMED v1.x horizon (per memory project_archivist_v1x_candidate_seat.md; full spec in v1.x curation amendment) | Long-running preservation: Funder Intelligence Database (per v7.0.5), Match Database (per v7.0.5), KFR maintenance + expiry tracking (per v7.0.4), lessons.json, audit trail. Currently operator-owned in v0.1; gets seat assignment at v1.x. Distinct from Editor — Editor is clarity-during-drafting; Archivist is preservation-between-cycles. |

# Pipeline placement (v0.1 with this amendment)

```
ONBOARDING (per-client, one-time)
  Intake → operator confirms → KFR populated

DISCOVERY (per-cycle)
  Scout (DISCOVER → VERIFY → REVIEW gate to operator)

DRAFTING + REVIEW (per-cycle, council seats under Section 5 revision-loop control)
  Logician PRE
  → Scribe drafts
  → Editor flags issues with options
  → APPLICANT approves Editor suggestions
  → Scribe revises
  → Judge scores against funder rubric
  → Red Team adversarial challenge
  → council split (>10 pt disagreement → human decides)
  Logician POST

SUBMISSION (per-cycle, end)
  Uploader assembles submission package → operator clicks final submit on funder portal

[v0.2 horizon: POST-AWARD (per-grant, ongoing)
  Data Collector → Report Generator]

[v1.x horizon: BETWEEN-CYCLE (per-client, ongoing)
  Archivist curation]
```

# Cross-family rigor (preserved by this amendment)

Adding Red Team to the canonical lineup formalizes what `router.yaml` already wires:

- Scout: Mistral (local)
- Scribe: Anthropic (Claude Sonnet 4.6) — *Beta target reframes per v7.0.7*
- Editor: Meta (Groq Llama 3.3 70B) — *Beta target reframes per v7.0.7*
- Judge: Google (Gemini 2.5 Pro) — *Beta target reframes per v7.0.7*
- Red Team: OpenAI-OSS (Groq GPT-OSS 120B) / OpenAI direct (GPT-5.1 escalation) — *Beta target reframes per v7.0.7*
- Logician: deterministic Python + Cedar (no LLM)
- Intake + Uploader: local deterministic + small local model where helpful

Five LLM-using council seats run on five distinct provider families today. The "minimum three distinct provider families across the council" requirement is overcovered. v7.0.7 Beta local-first amendment will revise the model strategy (most cloud seats move local); cross-family rigor at the model-weights level is a v7.0.7 concern, not v7.0.6.

# Companion file edits (paired with this amendment)

## README.md
- Council table: add Red Team row (currently 5 rows → 6).
- Add new "## Support Agents" section after Council section, listing Intake (v0.1, onboarding) + Uploader (v0.1, submission) + Data Collector and Report Generator (v0.2 horizon) + Archivist (v1.x horizon).
- Roadmap section: add brief v0.2 mention referencing Data Collector + Report Generator scope.

## docs/ARCHITECTURE_OVERVIEW.md
- "The Five Seats" → "The Six Seats." Update the ASCII diagram to include Red Team (post-Judge adversarial position, with disagreement-triggers-human-decide arrow back to operator).
- Cross-Family Adversarial Rigor section: confirm Red Team's family allocation is canonical, not de-facto.
- Add new "## Support Agents" section parallel to README structure.

## CLAUDE.md
- Council enumeration: update from "five-seat AI council" to "six-seat AI council plus support agents."
- What NOT to Do guards: review for any clauses that assume 5-seat lineup; update if needed.

## pipeline/architecture/v0.1/tilth_architecture_locked.md
- Section A council enumeration: add Red Team. Mark this amendment as the source.
- Section D.x: review for seat-position references; update if needed.

# What this amendment does not do

- Does not modify A1-A12.
- Does not modify Section K hardware tier mapping.
- Does not modify the Five Operating Laws or the Four Autonomy Rules.
- Does not introduce any new council seat beyond surfacing Red Team (already in router.yaml).
- Does not introduce any new failure code, Cedar rule, or admin-risk register row.
- Does not specify Uploader's submission flow (assembly steps, format requirements per portal, retry semantics on partial-submission failures) — that lives in v7.0.6 companion blueprint section or a follow-on submission-flow amendment.
- Does not specify Intake's extraction algorithm (LDR-pattern vs alternative, confidence thresholds, classifier choice) — that lives in v7.0.4 KFR Amendment as the Intake module spec.
- Does not specify v0.2 Data Collector compliance posture (CAN-SPAM / TCPA / consent capture at award acceptance / per-recipient opt-out tracking) — deferred to v0.2 reporting vertical amendment.
- Does not specify v0.2 Report Generator output format, format conversion, or Logician-equivalent gate for outbound report content — deferred to v0.2 amendment.
- Does not specify v1.x Archivist seat scope, model assignment, or boundary with Editor — deferred to v1.x curation amendment.
- Does not change v0.1 substrate decision (Pydantic AI per v7.0.3).
- Does not change Beta model-locality decision (deferred to v7.0.7 Beta local-first amendment).
- Does not modify KFR schema or fact validity model (that's v7.0.4 scope).
- Does not modify Funder Intelligence Database or Match Database schemas (that's v7.0.5 scope).

# Lock-history note

This amendment is the fourth v7.0.x corrective in the v7-Lock-line:

- v7.0.1 (DRAFT): Section E.P Governance Plan Preflight — awaiting Tier 1/2/3 GPP review + L-005 Thesis round before LOCK
- v7.0.2 (SELF-LOCKED 2026-05-04): Section A textual reconciliation — hardware paragraph + scope-locks line aligned with Section K v7 widened triple-target and v10 substrate enumeration as it stood at filing time
- v7.0.3 (SELF-LOCKED 2026-05-08): Section A substrate paragraph aligned with ADR-001 Pydantic-only decision; supersedes v7.0.2's substrate text only
- v7.0.6 (SELF-LOCKED 2026-05-09, this file): Council and support-agent roster — Red Team surfaced into canonical lineup; Intake + Uploader named for v0.1; Data Collector + Report Generator named for v0.2 horizon; Archivist named for v1.x horizon.

Forward-pending: v7.0.4 (KFR Amendment SCOPING DRAFT — composes against Intake), v7.0.5 (Funder Intelligence Database + Match Database SCOPING DRAFT — composes against Archivist's curation slot), v7.0.7 (Beta local-first model strategy + classification-aware split-context Scribe — composes against the seat lineup and the Card-level / operator-onboarding / SP0 three-layer classification model).

# Sequencing note

v7.0.6 (this amendment) lands first because v7.0.4 and v7.0.5 reference Intake and Archivist respectively. With v7.0.6 LOCKED, those references become well-defined.

v7.0.7 Beta local-first amendment can land in parallel to v7.0.6 — they touch different concerns (roster vs model strategy) and don't gate each other.

v7.0.4 KFR and v7.0.5 Funder Intelligence Database land after v7.0.6 + v7.0.7 because both reference seat names and model-locality decisions. SCOPING DRAFTS for v7.0.4 / v7.0.5 can be drafted in parallel to v7.0.6 / v7.0.7 review since the seat names are stable now.
