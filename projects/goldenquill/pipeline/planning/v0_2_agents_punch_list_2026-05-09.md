---
title: V0.2 (Reporting Vertical) Agent Punch List + V8 Forward Sketch
filed: 2026-05-09
operator: Josh
format: planning memo (per Josh request 2026-05-09)
scope: Tilth v0.2 horizon — Section R.3 grant reporting vertical + the seat roster v7.0.6 named but did not spec
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md (v7 LOCKED 2026-04-19; A6 = Section R.3 reporting commitment + R.PF1 track registry pull-forward + R.PF2 vault operational-data pull-forward)
  - pipeline/blueprint/v0.1/section_06_operating_envelope.md (v1-r1 LOCKED 2026-04-21; track-registry host)
  - pipeline/blueprint/v0.1/section_07_scribe.md (v1.1.1 LOCKED 2026-04-21; pins Scribe out-of-scope for reporting at v0.1, leaves the door for v0.2)
  - pipeline/blueprint/v0.1/section_10_red_team.md (v1.1 LOCKED 2026-05-02)
parent_amendments_in_flight:
  - architecture_v7_0_4 (KFR + Intake module — SCOPING DRAFT, requires Thesis)
  - architecture_v7_0_5 (Funder Intelligence DB + Match DB + Archivist curation-slot — SCOPING DRAFT, requires Thesis)
  - architecture_v7_0_6 (roster — Intake/Uploader named v0.1; Data Collector/Report Generator named v0.2; Archivist v1.x — SCOPING DRAFT, SELF-LOCK candidate)
  - architecture_v7_0_7 (classification-driven routing + Classification Review stage — SCOPING DRAFT, requires Thesis)
authority: Josh 2026-05-09 ("generate a comprehensive report on what needs done for V2. We need all of our agents designed."; clarified V2 = v0.2 reporting vertical; Archivist needs fleshed out; Data Collector data-flow needs design; new seats need architecture + blueprint)
---

# 1. What v0.2 actually is

v0.2 = the **grant reporting vertical** (Section R.3) plus the agent roster work that v7.0.6 named but did not spec. It is NOT TDSL (R.1) and NOT the content-production vertical (R.2). Those are also v0.2-horizon but are explicitly out of scope for this punch list.

The product claim from R.3 is precise: a single won grant generates 4–10 reports across its lifecycle; reports are short (10–30 pp), low-research (substance is in operational data already in hand), high willingness-to-pay ($500–1500 each, 80%+ margin), and structurally lower-hallucination-risk than writing because Scribe works **backward from documented substance** instead of forward from intent.

The architecture has committed v0.1 to two pull-forwards that v0.2 R.3 depends on. **R.PF1** binds §5 Pipeline to a track-registry abstraction so adding a `report` track is a router.yaml row + prompt template, not a §5 re-architecture. **R.PF2** binds §2 Vault to operational-data sub-kinds (metrics / financials / photos / narrative entries / timelines / beneficiary records) without breaking the funder/grant artifact schemas. Both are dormant PRE-gates today; both activate at the next §5 / §2 spin.

# 2. What the locked architecture already gives us (v0.2 inheritance)

Before listing what's missing, the inheritance is meaningful. v0.2 does not start from zero.

The Five Operating Laws and Four Autonomy Rules apply unchanged. The cross-family rigor discipline applies unchanged (a v0.2 Report-Judge cannot share a provider family with a v0.2 Report-Scribe). The Logician PRE/POST gate pattern applies unchanged. The §0.5 Blueprint Interface Index applies — every new v0.2 primitive registers a row. The classification register and Classification Review stage from v7.0.7 govern routing for every new seat (Data Collector touches phone numbers and contact PII; Report Generator touches operational data with mixed classification; both need explicit posture). The KFR from v7.0.4 is the substrate Report Generator pulls quantitative substance from. The Funder Intelligence DB + Match DB from v7.0.5 sit under Archivist's curation slot. The track-registry from §6 v1-r1 is what `report_mode` registers into. None of this is invented for v0.2; v0.2 is the first round that actually *exercises* these primitives end-to-end on a non-grant-writing track.

# 3. The agent gap — what v7.0.6 named but did not spec

| Agent | Layer | Status today | What's missing |
|---|---|---|---|
| Intake | v0.1 support | Named in v7.0.6; module spec drafted in v7.0.4 §5 | No blueprint section. v7.0.4 still SCOPING DRAFT. Operator-review UX undesigned. |
| Uploader | v0.1 support | Named in v7.0.6 | No module spec, no blueprint section, no portal-format catalogue, no failure-code family. |
| Data Collector | v0.2 horizon | Named in v7.0.6 | No spec at all. CAN-SPAM / TCPA / consent-capture posture undesigned. Substrate undesigned. |
| Report Generator | v0.2 horizon | Named in v7.0.6 | No spec at all. Composition with KFR + Original-proposal-commitments rubric undesigned. |
| Archivist | v1.x horizon | Named in v7.0.6; curation slot reserved by v7.0.5 | No spec at all. Boundary with Editor (clarity-during-drafting vs preservation-between-cycles) undesigned. Cadence for KFR refresh / Funder corpus curation / lessons-delta integration undesigned. Josh wants this fleshed out for v0.2 even though it was named v1.x — bring it forward. |

That is the body of work this punch list is about.

# 4. Cross-cutting work that any v0.2 agent depends on

Three things must land before any v0.2 agent gets a blueprint round, because every agent reads or writes against them.

**4a. v7.0.4 + v7.0.5 + v7.0.7 must clear Thesis and LOCK.** v7.0.6 SELF-LOCKs after operator review. The other three need full Editor / Judge / Red Team rounds. Sequence per the amendments themselves: v7.0.6 first (lightest, roster only), v7.0.7 in parallel (different concern), then v7.0.4 and v7.0.5 because they reference seat names and routing decisions stabilized by v7.0.6 + v7.0.7. v0.2 agent design is downstream of all four.

**4b. §5 Pipeline v6 spin (or v8 round) for the track registry.** R.PF1 commits §5 to the registry. v0.2 reporting needs `report_mode` as a registry row. The §6 Operating Envelope already hosts the registry schema (v1-r1 LOCKED). What's pending is §5 actually adopting the registry pattern in place of its current hardcoded `submission_mode` / `eval_mode` enum. F-PIPELINE-TRACK-FROZEN is dormant until that spin and ACTIVATES against §5's LOCKED text at lock time. So the §5 spin is itself audited against the v7 commitment.

**4c. §2 Vault v7.2 (or v8) for operational-data sub-kinds.** R.PF2 commits §2 to extensibility. Operational data types per A6: metrics (numerical time-series), financials (line-item records), photos (binary + EXIF + caption), narrative entries (free-form journal, timestamp + author + tags), timeline of activities (event records), beneficiary records (per-beneficiary, consent-tier-aware). Each gets a SIMPLE sub-kind row, a per-type schema, per-type Cedar gates, and a per-type vault subtree under `orgs/{slug}/vault/operational/`. Beneficiary records carry HIGH-severity admin-risk discipline if PII present. F-VAULT-ARTIFACT-ONLY is dormant until that spin and activates at lock time.

These three workstreams are the rails. Skip any one and the v0.2 agent specs have nothing structural to reference.

# 5. Per-agent punch list

Each agent below carries the same scaffolding: purpose, inputs, outputs, routing posture (per v7.0.7 classification), substrate, Logician gate family needed, blueprint section number to claim, sequencing dependencies, and open questions only Josh can answer. Not full design cards — that's the next round. This is the punch list.

## 5.1 Intake — v0.1 support, but blueprint still missing

**Purpose.** Bulk-ingest a client's org documents at white-glove onboarding; extract candidate facts with verbatim-quote-with-page provenance; queue them for operator review; promote operator-confirmed facts to KFR. Two modes per v7.0.4 §5: BULK (folder drop at onboarding) + INCREMENTAL (single new doc on arrival).

**Inputs.** `orgs/<slug>/intake/inbox/` (operator-uploaded folder of annual reports, 990s, audited financials, employee rosters, program reports, partnership LOIs, prior grant applications).

**Outputs.** `orgs/<slug>/vault/kfr/pending_facts.yaml` (queue) → operator review → promotion to `orgs/<slug>/vault/kfr/register.yaml`. Rejected candidates audit-trailed in `pipeline/validation/extractor_rejects/`.

**Routing posture.** Always-local. Touches raw uploaded org docs (mixed classification, default-conservative). Per v7.0.7 the slot-fill agent and Intake are both pinned local — non-negotiable.

**Substrate.** Per v7.0.4 §5 — FAISS or Chroma vector store + bge-large-en-v1.5 embedding + Pydantic AI tool composition + small local LLM (Mistral 7B class) for fact extraction. Same substrate as Funder Intelligence DB indexing; one unified vector store with per-register namespace.

**Logician gates owned.** F-EXTRACTOR-FABRICATION (PRE pre-queue — rejects any candidate whose `source_quote` does not literally appear in `source_doc` at `source_page`; cheapest gate in the system; runs before operator ever sees a candidate). Composes against F-LOGICIAN-FACT-DRIFT family (POST, owned by Logician §4 amendment) — Intake is the upstream that prevents drift from entering KFR in the first place.

**Blueprint section.** §11 Intake (claim the next §N row in the §0.5 Interface Index). v7.0.4 carries the module spec; the blueprint section is the seat-lifecycle wrapper around that spec.

**Sequencing.** Blocked on v7.0.4 LOCK. Once v7.0.4 LOCKs, §11 blueprint is the next round (parallel-eligible with §12 Uploader).

**Open questions.**
- BULK-mode operator review UX: side-by-side display of (extracted fact / source quote / source document at source page) — but how does the operator move through 200 candidates from a 990 efficiently? Batch-confirm by source doc? Confidence-threshold autopromote with operator audit pass? Pure manual?
- INCREMENTAL trigger: filesystem watcher? Operator-explicit "process this doc"? Both?
- KFR migration of existing PROJECT_CONTEXT `[NEEDED]` numeric fields per v7.0.4 §6 — is the migration done by Intake at first operator review post-v7.0.4 LOCK, or is it a one-shot script Josh runs across all current orgs?

## 5.2 Uploader — v0.1 support, fully unspec'd

**Purpose.** End-of-cycle submission package assembly. Render operator-approved final proposal into funder-portal-required formats. Stage submission. **Operator clicks final submit on funder portal — Uploader does not auto-submit.** Per v7.0.6 this is a federal-portal-ToS + operator-accountability constraint, non-negotiable.

**Inputs.** Operator-approved final draft from §5 Pipeline submission_mode terminus + signed claim_evidence_map + RFA dissection (for portal field mapping).

**Outputs.** `orgs/<slug>/vault/grants/<grant_id>/submission_package/` containing: final-format documents (PDF / DOCX / portal-required), filled portal form fields exported as YAML for operator copy-paste-or-paste-confirm, attachment manifest, submission-readiness checklist surface to operator.

**Routing posture.** Mostly local. Final draft is post-classification-fill (Confidential values already embedded). Per v7.0.7 anything reading a post-fill draft is local-routed structurally. No cloud reasoning needed for assembly — this is mechanical.

**Substrate.** Pydantic AI orchestration over python-docx + pypdf + openpyxl + portal-format adapters (per ADR-001 substrate frozen at Golden Image; no marketplace). Adapters are per-portal (Grants.gov Workspace, SAM.gov, foundation portals); each adapter is a small Python module that takes the canonical submission package and emits portal-specific format.

**Logician gates owned.** New family:
- `F-UPLOADER-PACKAGE-INCOMPLETE` (PRE submit-stage): required-by-RFA section missing from package; required-by-RFA attachment missing; portal field with no value.
- `F-UPLOADER-FORMAT-MISMATCH` (PRE submit-stage): portal requires PDF, package has DOCX; portal page-limit exceeded; portal file-size exceeded.
- `F-UPLOADER-AUTOSUBMIT-ATTEMPTED` (PRE — fail-closed): if Uploader code path attempts final-submit API call, fail-closed. v0.1 prepare-and-stage discipline is structural.
- `F-UPLOADER-SIGNATURE-MISSING` (PRE): operator-approval signature on final draft missing from package manifest.

**Blueprint section.** §12 Uploader.

**Sequencing.** Can land in parallel with §11 Intake. Both are v0.1 support agents; neither blocks the other. Both blocked on v7.0.6 LOCK (already SELF-LOCK candidate).

**Open questions.**
- Portal adapter scope for v0.1: which portals do we cover at first ship? Grants.gov is mandatory (federal). SAM.gov is mandatory (registration / certification). Foundation portals are per-funder and frequently bespoke — do we cover top-N most common (Common Grant Application, Foundant, Submittable, Fluxx) or punt and let operator copy-paste? Recommendation: top-N. Punting feels like a regression from grant-finder/grant-writer's existing capability.
- Final-format generation responsibility: does Uploader own the docx-to-pdf conversion pipeline, or does §6 Operating Envelope publish a format-conversion utility that Uploader and Report Generator both consume?
- Attachment provenance: an attachment is a non-Tilth-generated file (resume, financial statement, letter of support). Where do these live in the vault? Probably under `orgs/{slug}/vault/grants/<grant_id>/attachments/` with operator-confirmed signatures — but this needs §2 to acknowledge the sub-kind. Bleeds into §2 R.PF2 spin.

## 5.3 Data Collector — v0.2 reporting, fully unspec'd, the harder of the two reporting agents

**Purpose.** During an active grant's reporting period, collect operational performance data from grantees and sub-awardees. Channels: email, text, voice. Compliance-heavy. The output of Data Collector becomes the substance Report Generator works backward from.

**Inputs.** `orgs/<slug>/vault/grants/<grant_id>/reporting_schedule.md` (Scout-derived, per R.3 spec); `orgs/<slug>/vault/grants/<grant_id>/proposal_commitments.yaml` (extracted from won proposal — what we said we'd report on); `orgs/<slug>/vault/grants/<grant_id>/sub_awardees.yaml` (per-sub-awardee contact + consent capture); KFR (for cross-validation of reported numbers against operator-curated facts).

**Outputs.** Per-reporting-period structured collection: `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/` containing metrics, narrative responses, photo uploads (with EXIF + caption + sub-awardee attribution), beneficiary records, financial line items, milestone confirmations. All written into the §2 R.PF2 operational-data sub-kinds.

**Routing posture.** Always-local for outbound message composition (touches contact PII, sub-awardee identifiers, sometimes unconfirmed beneficiary data). Cloud-routable for content drafting of NEW outbound prompts WHEN the operator has classified the prompt-template content as Public + Shareable. Inbound responses are always-local on receipt — they may contain Confidential operational data and must classification-route at storage time.

**Substrate.** This is where the agent gets large. Sub-modules:
- **Outreach engine.** Email (SMTP via operator's BYOK provider — Postmark / SendGrid / Mailgun-equivalent), SMS (Twilio / Plivo / equivalent), voice (Twilio Voice or operator-pinned PSTN gateway). All BYOK.
- **Consent ledger.** Per-recipient consent capture at award acceptance; per-channel opt-in (email vs SMS vs voice may have separate consents); per-recipient opt-out tracking with same-day enforcement; CAN-SPAM unsubscribe links on every email; TCPA prior-express-written-consent on every SMS or voice; state-specific layering (PA / CA / FL / TX have stricter rules than federal floor).
- **Response intake.** Email-thread parser (subject-line regexp + threading + reply quoting strip), SMS short-form parser (free text + structured prompts via Twilio Studio-equivalent flows), voice (transcription via local Whisper-class model — same substrate as the rest of the local model stack).
- **Field validation.** Per-collected-data-point: Pydantic schema validation at intake. Numeric fields cross-checked against KFR for sanity (a reported "300 graduates" against KFR's "197 graduates FY25" surfaces F-DATA-COLLECTOR-KFR-DRIFT to operator).
- **Classification-aware storage.** Per v7.0.7 — every inbound data point gets a classification tag at storage time. Defaults from the field-class registry; operator override per-cycle.

**Logician gates owned.** New family:
- `F-DATACOLLECTOR-CONSENT-MISSING` (PRE outbound): no per-channel consent on file for this recipient → fail-closed, no message sent. CAN-SPAM / TCPA enforcement at the gate, not in policy prose.
- `F-DATACOLLECTOR-OPT-OUT-ACTIVE` (PRE outbound): recipient opted-out on this channel → fail-closed.
- `F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED` (PRE outbound): per-recipient per-channel rolling window cap (operator-set; default conservative — e.g., 1 outbound message per 7 days per recipient per channel) → fail-closed.
- `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND` (PRE outbound): outbound message body contains other recipients' PII (sub-awardee A's content leaking into sub-awardee B's message) → fail-closed.
- `F-DATACOLLECTOR-KFR-DRIFT` (POST inbound, advisory not fail-closed): inbound numeric field outside tolerance vs KFR — surface to operator at next SP0, do not block storage.
- `F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET` (PRE storage): inbound data point arrives with no classification tag and no card-default match → fail-closed; queue for operator classification.

**Blueprint section.** §13 Data Collector.

**Sequencing.** Blocked on v7.0.4 LOCK (KFR cross-validation), v7.0.5 LOCK (Match DB outcome tracking — Data Collector flips Match DB entries from `awarded` into `awarded → reporting_active`), v7.0.6 LOCK, v7.0.7 LOCK (classification routing for inbound storage). Also blocked on §2 R.PF2 spin (the operational-data sub-kinds Data Collector writes into). Probably the most-blocked agent in the v0.2 set.

**Open questions.**
- **Voice channel: in or out for v0.2 first ship?** Voice is the most TCPA-exposed channel and the highest-friction substrate. Recommendation: ship v0.2 with email + SMS only; voice is v0.2.x. But this is a Josh call — voice may be a real differentiator with rural sub-awardees who don't email reliably.
- **Telegram / WhatsApp / Signal in scope?** Memory entry `project_tilth_phone_field_layer.md` calls Telegram out as the Cultivator substrate. Cultivator is per-employee for the *operator's* org; Data Collector is reaching outward to *grantees and sub-awardees*. They're different audiences with different consent surfaces. Recommendation: keep them separate. Telegram for Cultivator (operator's employees, opt-in by employment), email + SMS for Data Collector (external recipients, formal consent capture).
- **Sub-awardee identity verification.** When a sub-awardee responds with "we trained 47 farmers this quarter," how do we trust the source? Recommendation: per-sub-awardee shared-secret token at award acceptance, embedded in every outbound message; inbound responses validate the token. Alternative: per-recipient signed-link with expiring tokens. Punt to the blueprint round but Josh should weigh in early.
- **State-law layering.** The compliance matrix (PA / CA / FL / TX / NY robocall + SMS + email rules) is real engineering work. Does Sovereign Node LLC ship a state-rules card that Data Collector consumes per recipient address-of-record, or is this operator-curated per client?

## 5.4 Report Generator — v0.2 reporting, the easier-but-still-substantial one

**Purpose.** Generate funder-ready reports using Data Collector's gathered operational data + KFR + the original won proposal's commitments. Same Logician PRE/POST discipline as v0.1 council seats per v7.0.6. **Lower hallucination risk than grant writing because Scribe-equivalent works backward from documented substance** — but the discipline is not weaker, it's the same.

**Inputs.** `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/` (Data Collector output), `orgs/<slug>/vault/grants/<grant_id>/proposal_commitments.yaml` (the rubric Judge-equivalent scores against — what we promised), `orgs/<slug>/vault/grants/<grant_id>/reporting_template.yaml` (funder-required format), KFR (org-side cross-validation), Funder Intelligence DB (funder dialect + reporting-format precedents from prior cycles).

**Outputs.** `orgs/<slug>/vault/grants/<grant_id>/reports/period_<n>/draft_<v>.md` plus signed claim_evidence_map (every reported claim traces to operational data + period; over-claiming → flagged; missing-required-section → flagged).

**Routing posture.** Classification-driven per v7.0.7. Reports often contain mixed-classification data (operational metrics typically Shareable; beneficiary stories often Confidential; financial detail often Confidential). Slot-fill agent does the post-fill assembly; cloud agents see the Public + Shareable framing only. Same pattern as v0.1 grant-writing council.

**Substrate.** This is a *track* in the §5 track-registry, not a brand-new orchestration. Per R.PF1 the entire reporting pipeline is:
- §5 dispatches `report_mode` track
- Scribe-equivalent (same seat, different prompt template — `scribe_report_template`) drafts
- Editor-equivalent (same seat, different rubric — clarity rubric tuned for funder reporting register vs proposal register) reviews
- Judge-equivalent (same seat, different rubric — `original_proposal_commitments.yaml` instead of `funder_rubric.yaml`) scores
- Red Team-equivalent (same seat, different probe template — "would a program officer kick this back?" probe instead of "would a reviewer reject this proposal?") attacks
- Logician PRE/POST applies the same gate framework with the new rubric

This is the strongest argument for the track-registry pattern: Report Generator is **not a new agent** in the council sense. It's the **same six seats** running on a different track. The "agent" name is shorthand for the orchestration that loads the report-track prompts and rubrics. v7.0.6 named it as a distinct agent for roster-clarity reasons; the implementation is a track binding.

**Logician gates owned.** Family:
- `F-REPORT-COMMITMENT-UNTRACED` (POST scribe-equivalent): a claim in the report is not traceable to either an operational-data source OR a KFR entry OR a commitment in the original proposal → fail-closed.
- `F-REPORT-COMMITMENT-MISSED` (POST judge-equivalent): an entry in `proposal_commitments.yaml` has no corresponding section in the draft report → fail-closed (incomplete reporting).
- `F-REPORT-OUT-OF-SCOPE-DRIFT` (POST judge-equivalent): the report describes activities outside the original proposal's `eligible_activity_map` → fail-closed (over-reporting / scope drift).
- `F-REPORT-NUMERIC-DRIFT` (POST scribe-equivalent): reported numeric vs Data Collector's stored numeric vs KFR — if the three diverge beyond tolerance, fail-closed (operator must reconcile before report ships).
- `F-REPORT-TEMPLATE-MISMATCH` (PRE): funder-required reporting template specifies sections that the draft does not cover → fail-closed.

**Blueprint section.** §14 Report Generator (or §R.3 if we choose to mirror the architecture-section name; recommendation is §14 to keep blueprint numbering linear and reference R.3 in the section preamble).

**Sequencing.** Blocked on §13 Data Collector (Report Generator consumes Data Collector output), §5 v6 spin (track registry must accept `report_mode`), R.PF2 (operational-data sub-kinds the report reads from), v7.0.4 LOCK (KFR cross-validation), v7.0.5 LOCK (Funder Intelligence DB for reporting-format precedents). The most-blocked agent.

**Open questions.**
- **Track-registry binding granularity.** Does each section type within a report (narrative / metrics-table / financial-summary / photo-gallery) get its own sub-track, or is the report-track monolithic with sub-section prompt templates inside it? Recommendation: monolithic track + sub-section prompt templates inside; matches grant-writing's "one track, many section prompts."
- **Report-rubric extraction.** `proposal_commitments.yaml` needs to be extracted from the won proposal at award time. Who extracts it? Probably Intake-adjacent at award acceptance, but Intake is currently scoped to client-onboarding, not grant-event-driven. Either Intake gets a third mode (AWARD-INGEST), or this is a Data-Collector setup phase, or it's a new Archivist function. Open.
- **Period-N comparison.** Many funder reports want trend comparison vs prior period. Does Report Generator load period_<n-1> draft as context, or does it pull from KFR + operational data fresh and let the funder do the trend math? Recommendation: pull fresh, surface trend in narrative when operator-approved; do not over-rely on prior-draft context (Law 5: substance comes from the applicant, not from prior Tilth output).

## 5.5 Archivist — v1.x slot, but Josh wants it pulled forward

This is the agent Josh specifically named ("archivist needs fleshed out"). v7.0.6 reserves the slot for v1.x; v7.0.4 §9 and v7.0.5 §6 both bind their curation work to that slot. Josh is signaling that the slot needs *design*, not just naming, *now* — even if the implementation horizon stays v1.x, the architecture / blueprint can land in the v0.2 wave so v0.2 ships with the curation surface visible.

**Purpose.** Long-running between-cycle preservation work. Distinct from Editor (clarity-during-drafting) by time horizon and substrate. Editor reviews a draft a Scribe just produced; Archivist tends the corpus a council has accumulated across cycles.

**Inputs.** Read-mostly across:
- `vault_shared/funder_intelligence/` (per v7.0.5) — funder corpus, quarterly curation cadence
- `orgs/<slug>/match_database/` (per v7.0.5) — per-org Scout reasoning trail, lessons-delta integration, Law-3 segmented
- `orgs/<slug>/vault/kfr/` (per v7.0.4) — expiry tracking, refresh-prompt surfacing for SP0, deprecated-fact archival
- `pipeline/institutional_memory/lessons.json` — append-only audit trail; pattern-detection across cycles
- `vault_shared/benchmarks/` (per v7.0.4 §7) — external peer benchmarks; freshness tracking
- `orgs/<slug>/vault/grants/<grant_id>/reports/` (per v0.2 R.3) — completed reports archive, prior-period reference for Report Generator

**Outputs.** Surface-to-operator artifacts:
- Quarterly curation digest per workspace: stale Funder Intelligence docs flagged for promotion-or-drop; new docs since last review awaiting promotion; integrity-check failures.
- Per-org KFR refresh digest: facts approaching expiry; facts past expiry without operator-acknowledged STALE; pending-facts queue size; suggested merges with existing KFR entries.
- Match Database lessons-delta proposals: cross-cycle patterns ("this funder declined this client 3 cycles in a row — surface to operator before next proposal"); not auto-applied.
- Lessons.json patches: proposed lessons.md entries from Tilth-internal pattern detection (single-quill, NOT fleet-wide; fleet-wide patterns are R.6 Telemetry Commons).

**Routing posture.** Always-local. Archivist reads classified content (Confidential KFR entries, per-client Match DB narratives) and produces operator-facing digests. Per v7.0.7 anything reading post-fill / classified-Confidential content is local-routed structurally.

**Substrate.** Pydantic AI agent with tool composition over the existing FAISS/Chroma indexes (KFR + Funder Intelligence + Match DB share substrate per v7.0.4 / v7.0.5). Small local LLM for narrative summarization in operator digests. Scheduled-task-driven (per the existing schedule skill — Mondays 8:30 AM cron from the Monday fund-radar memory is the precedent pattern; Archivist runs on its own quarterly + weekly cadences).

**Cadences.** Two natural rhythms:
- **Weekly tick** (light): KFR expiry scan, pending-facts queue summary, Match DB lessons-delta scan, lessons.json append from any pattern detected this week.
- **Quarterly curation review** (heavy): Funder Intelligence promotion/drop pass, Match DB outcome-rollup digest, Benchmarks Register freshness pass, lessons.json full review for proposed lessons.md diffs.

**Logician gates owned.** Family:
- `F-ARCHIVIST-CROSS-ORG-LEAK` (PRE — fail-closed): if Archivist's quarterly digest aggregates content across orgs in any operator-facing surface, fail-closed. Per-org digests stay per-org. Workspace-level aggregation (e.g., "across all your clients, X% of KFR facts are stale") is allowed because workspace-aggregate is operator-only context, not cross-org content leakage — but this needs explicit gate logic.
- `F-ARCHIVIST-LESSON-INSTANCE-LEAK` (PRE — fail-closed): proposed lessons.json patches must be pattern-level, not instance-level (matches R.6 Telemetry Commons invariant). A proposed lesson "Funder X declined Client Y for reason Z" fails the gate; "Federal program officers in this category often decline in cycles where applicants undercount sub-awardees" passes.
- `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` (PRE — fail-closed): Archivist generates *proposals*, never auto-applies KFR refreshes, lessons.md patches, Match DB action-state changes, or Funder Intelligence promotion decisions. Operator confirms every change.
- `F-ARCHIVIST-CADENCE-DRIFT` (PRE): scheduled cadence missed by > 2x interval — surface to operator (the absence of Archivist running is itself a signal).

**Boundary with Editor.** Editor is in the inner loop (clarity review per draft); Archivist is in the outer loop (curation between cycles). They share zero runtime path. They share no substrate (Editor reads SectionDraft + RubricCriterion; Archivist reads KFR + Funder Intelligence + Match DB + lessons.json). The seat-name distinction is sharp; v0.2 should resist any pull to merge them. Memory `project_archivist_v1x_candidate_seat.md` already documents the distinction; v0.2 blueprint should pin it explicitly.

**Boundary with Logician.** Logician is deterministic Cedar + Python in the inner loop; zero token cost. Archivist runs an LLM (small + local) for digest narrative + pattern detection. The work is different in kind. They share no concern.

**Blueprint section.** §15 Archivist (claim the v1.x horizon section number now; populate the spec in the v0.2 wave; LOCK at v1.x when the seat actually ships).

**Sequencing.** Blocked on v7.0.4 LOCK + v7.0.5 LOCK (those define the substrates Archivist curates). Can be drafted in parallel with §13 Data Collector + §14 Report Generator since none of them share runtime path. **Recommendation:** spec Archivist in the v0.2 wave per Josh's note; ship implementation at v1.x; the spec is not load-bearing for v0.2 production but is load-bearing for v0.2 design coherence (KFR + Funder Intelligence DB + Match DB all reference Archivist's curation slot, and an unspec'd referenced slot is a design-debt flag for the Thesis Team).

**Open questions.**
- **Pull-forward degree.** Spec only, or spec + stub the operator-facing weekly/quarterly digest in v0.2 with operator manually running the cadence? Recommendation: spec only at v0.2; operator-driven cadence stays operator-driven until v1.x adds the scheduled-task wiring. Avoids the risk of a half-built Archivist creating a maintenance vacuum where neither operator nor Archivist owns the work.
- **Lessons.json append authority.** Currently operator-curated. v1.x Archivist proposes; operator approves. But who **writes** the file? Recommendation: Archivist drafts a `lessons_proposals.json` queue; operator-confirmed entries promote to `lessons.json`. Same pattern as Intake → KFR. Mirrors the Tilth-wide promotion discipline.
- **Cross-cycle memory model.** Match Database carries cycle outcomes per (client × funder). Across cycles, patterns emerge — this client always declines this funder, this funder always declines small farms regardless of client, this client+funder combination wins when the third co-applicant is present, etc. Pattern detection is the high-value Archivist work. But the substrate for cross-cycle pattern detection (graph database? expanded vector store? structured aggregation?) is unsourced in v7.0.5. Open question: does Archivist need its own substrate, or compose against existing Match DB + Funder Intelligence DB indexes?

# 6. Vault and pipeline work that v0.2 forces

R.PF1 and R.PF2 are dormant pull-forwards today. v0.2 is what activates them.

**§5 v6 spin (track registry).** §5 currently hardcodes `submission_mode` and `eval_mode`. v0.2 demands `report_mode`. Per R.PF1, the spin must refactor to a registry pattern hosted in §6 (already LOCKED with the registry schema); §5 becomes track-agnostic dispatcher. F-PIPELINE-TRACK-FROZEN audits the spin at lock time. This is a §5 v6 round, not a v0.2 amendment.

**§2 v7.2 spin (operational-data sub-kinds).** §2 currently has SIMPLE + COMPOUND with `index_amendment` as the only COMPOUND sub-kind. v0.2 needs SIMPLE sub-kinds for: metrics, financials, photos, narrative entries, timeline of activities, beneficiary records. Per R.PF2 each gets a per-type schema, per-type Cedar gates, per-type vault subtree. F-VAULT-ARTIFACT-ONLY audits the spin at lock time. Beneficiary records carry HIGH-severity admin-risk discipline if PII present — Cedar policy work, not just schema work. This is a §2 v7.2 round, not a v0.2 amendment.

**§4 Logician new gate families.** Each agent above declared a gate family. Logician §4 needs an amendment that registers them all with v2.x sequencing into the existing PRE/POST table. The existing `section_04_v2_2_consolidated_amendment.md` precedent is the format pattern. Estimated: ~20 new gates across v0.2 agents.

**§0.5 Interface Index expansion.** Each new blueprint section (§11 Intake / §12 Uploader / §13 Data Collector / §14 Report Generator / §15 Archivist) adds rows. Per the §0.5 v3 → v4+ cadence, this is a paired amendment with each section's LOCK.

# 7. Sequencing — what blocks what

The dependency graph is:

```
v7.0.6 SELF-LOCK (roster — already candidate)
    │
    ├──→ v7.0.7 Thesis + LOCK (classification routing)
    │       │
    │       └──→ v7.0.4 Thesis + LOCK (KFR — references seat names from v7.0.6)
    │       └──→ v7.0.5 Thesis + LOCK (Funder Intel DB + Match DB — references Archivist slot from v7.0.6)
    │
    └──→ §11 Intake blueprint round (depends on v7.0.4 LOCK)
    └──→ §12 Uploader blueprint round (depends on v7.0.6 LOCK only)
    
After v7.0.4 + v7.0.5 + v7.0.7 all LOCKed:
    │
    ├──→ §5 v6 spin (track registry) ◄── F-PIPELINE-TRACK-FROZEN audits at lock time
    ├──→ §2 v7.2 spin (operational-data sub-kinds) ◄── F-VAULT-ARTIFACT-ONLY audits at lock time
    │       │
    │       └──→ §13 Data Collector blueprint round
    │       └──→ §14 Report Generator blueprint round (depends on §13 + §5 v6 + §2 v7.2)
    │       └──→ §15 Archivist blueprint round (parallel-eligible with §13/§14)
    │
    └──→ §4 Logician v2.x amendment registering all new gate families
    └──→ §0.5 v6+ Interface Index amendments paired with each blueprint LOCK

When all v0.2 sections LOCK:
    │
    └──→ v0.2 production cut — Tilth ships R.3 reporting vertical to first opted-in client
```

Critical path: v7.0.6 → v7.0.4 → §5 v6 + §2 v7.2 → §13 → §14. Archivist (§15) can swim in parallel. Intake (§11) and Uploader (§12) can swim in parallel after v7.0.6.

Realistic timeline: each of v7.0.4 / v7.0.5 / v7.0.7 needs a Thesis round. Each blueprint round needs a Thesis round. The L-005 two-audit cycle averages ~2 sessions per round. v0.2 is on the order of 15–20 Thesis cycles. At the current cadence (per session_log.jsonl), that's a multi-week-to-multi-month effort, not a single push.

# 8. Open decisions only Josh can make

The following are blocking or near-blocking for v0.2 design and need Josh's call before the spec rounds open. Batched per the operator-batch-questions discipline.

**8a. Voice channel for Data Collector v0.2 — in or out?** Email + SMS + voice = full TCPA exposure + voice substrate complexity. Email + SMS = lower compliance surface, possibly weaker product for rural sub-awardees who don't email reliably.

**8b. Telegram / WhatsApp for Data Collector — in or out?** Cultivator owns Telegram for the operator's own employees. If Data Collector also uses Telegram for external grantees, the substrate is reused but the consent surface is different. Recommendation: keep separate (Telegram = Cultivator only, email + SMS = Data Collector only).

**8c. Foundation portal adapter scope for Uploader v0.1.** Top-N adapters (Common Grant Application + Foundant + Submittable + Fluxx covers the bulk) or punt to operator copy-paste? Top-N is more product, more code to maintain.

**8d. Archivist pull-forward degree.** Spec-only at v0.2 with implementation deferred to v1.x, or spec + stubbed weekly/quarterly digest at v0.2 with operator running the cadence manually? Recommendation: spec-only.

**8e. Sub-awardee identity verification model for Data Collector.** Per-recipient shared-secret token at award acceptance, or per-message expiring signed link, or operator-pinned per-client choice?

**8f. State-law layering for Data Collector.** SN-LLC-shipped state-rules card (operator opts in) or operator-curated per-client classification?

**8g. CIC × CLC orthogonality preservation in v0.2 substrate.** v7.0.8 LOCKED CIC × CLC orthogonality with four PRE-gates. Every new register schema (KFR, Funder Intel DB, Match DB, operational-data sub-kinds) and every new agent prompt template MUST preserve the no-coupling invariant. Logician F-CIC-CLC-COUPLING-VIOLATION applies regardless. Operator confirmation: the v0.2 spec rounds will explicitly audit each new schema and prompt template against the four detection layers (lexical regex / Pydantic AST / value-set / KP schema).

**8h. Original proposal commitments rubric extraction.** Who extracts `proposal_commitments.yaml` from the won proposal at award acceptance? Intake third mode (AWARD-INGEST), Data Collector setup phase, or new Archivist function?

**8i. Report Generator track-binding granularity.** Monolithic `report_mode` track with sub-section prompt templates inside, or separate sub-tracks per report-section-type (`report_narrative` / `report_metrics` / `report_financial` / etc)? Recommendation: monolithic.

**8j. Report period-N comparison context.** Pull fresh and let funder do trend math, or load period_<n-1> draft as Scribe context for trend narrative? Recommendation: pull fresh.

# 9. Sketch — what doesn't fit v7 (V8 forward-look)

Most of v0.2 fits the v7 architectural lock cleanly because v7 was designed with R.1/R.2/R.3 commitments and R.PF1/R.PF2 pull-forwards in mind. The work above is *amendment + spin* shaped, not *architecture-round* shaped. But there are pressure points where v0.2 strains the v7 frame and a v8 round becomes more honest.

**v8 candidate concern 1 — Multi-track concurrent runtime.** v7 designs for one track running at a time per Tilth (a session is in submission_mode OR eval_mode, never both). v0.2 introduces a real possibility: a client has an active grant-writing cycle in submission_mode and an active reporting cycle in report_mode for a different grant, simultaneously. §5's revision-loop and inner-loop discipline assumes one session, one track. Concurrent tracks may want concurrent sessions on the same Tilth — and §2 Vault's signed-commit discipline (M15) becomes the contention point. v0.2 may be able to serialize-enforce one-track-at-a-time with operator-level scheduling (manual lockout); v0.3+ probably needs concurrent-track architecture. v8 is the honest place for this.

**v8 candidate concern 2 — Multi-Tilth fleet operations (Stage 2 at twelve deployments).** Stage 2 in the product arc is twelve Tilths in operation. Each Tilth is sovereign. The Funder Intelligence DB curation work at twelve deployments creates a coordination problem v7 does not address: who curates the workspace-shared funder corpus, whose curation overrides whose, how does cross-Tilth corpus contribution work without the Stage-5 Sovereign Node commons being live? v7.0.5 §6 reserves the Archivist curation slot but does not address inter-Tilth coordination. v8 with a multi-Tilth coordination section (call it Section M-Multi) becomes the right shape.

**v8 candidate concern 3 — Cultivator integration.** Cultivator is the per-employee phone interface for the operator's own org. Memory `project_tilth_phone_field_layer.md` parks it as v2 (Stage 2-ish). v0.2's Data Collector reaches outward; Cultivator reaches inward to the operator's own employees. v7 has no architectural seat for inward employee data ingestion — every PROJECT_CONTEXT today assumes operator-curated facts, not employee-curated facts. v8 with a Cultivator section (call it Section P-Phone) is the right shape, and it composes against KFR (employee-curated facts feed KFR via Cultivator at v0.3+).

**v8 candidate concern 4 — Sandbox / parallel-compare orchestrator.** Memory `project_capital_logic_cards_v9_state.md` parks MyCel + Console (Cards × MyCel × Console × Judge composition for reframer / parallel-compare) to the Sandbox per CLC v2 §14. v0.1 and v0.2 ship single-card-at-a-time. v8 is where multi-card parallel-compare gets real architecture; v0.2 should preserve the option but not implement.

**v8 candidate concern 5 — Federation primitives for R.1 TDSL.** R.1 TDSL is named in v7 but the federation substrate (IPFS / Hypercore / libp2p / Tilth-native) is unselected. v0.2 doesn't ship R.1 — but v8 is when R.1 substrate selection lands honestly, and it composes against R.4 / R.5 / R.6 Commons (already in v7). The TDSL substrate decision is an architecture-round-sized concern.

**Recommendation on v8 framing.** v0.2 amendments stay as v7.0.x amendments — they fit. v8 should land when *multiple* of the above pressure points become active simultaneously, which is roughly the Stage-2 fleet milestone. Premature v8 fragments the architectural lock; postponed v8 leaves v0.2 carrying weight v7 was not designed for. Watch for the moment when a v7.0.x amendment can no longer be expressed without contradicting another v7 commitment — that's the v8 trigger.

# 10. What this memo is NOT

- Not a per-agent design card. Per-agent design cards are the next round (v0.2 amendment Thesis-prep work).
- Not a LOCK-class artifact. This is a planning memo. No precedence-table changes, no failure-code registrations, no §0.5 row additions.
- Not a substrate decision. ADR-001 still holds. Pydantic AI substrate stays. Local model class for Intake / Data Collector / Report Generator / Archivist is per-agent within the existing Mistral 7B / Whisper / bge-large-en-v1.5 envelope; deviation requires a separate ADR.
- Not a customer-facing artifact. Section R is internal; v0.2 is an internal product milestone; this memo is for the build, not the website or sales pitch.
- Not a v0.1 spec change. v0.1 ships grant-writing only. v0.2 spec work runs alongside v0.1 production cut; v0.1 ships first, v0.2 ships when the seat work above is done.

# 11. Immediate next actions (in order, by Josh's call)

1. **Confirm or override the Archivist pull-forward** (open question 8d). Spec-only at v0.2 vs spec + stubbed cadence.
2. **Land v7.0.6 SELF-LOCK** (already candidate; operator review pending).
3. **Open Thesis rounds for v7.0.4 + v7.0.5 + v7.0.7** in parallel (different concerns; no inter-amendment dependency until LOCK).
4. **After v7.0.7 LOCK**, Classification Review stage gets a small implementation pass (operator-facing white-glove flow). Preconditions §13 Data Collector and §14 Report Generator.
5. **§11 Intake blueprint round** opens after v7.0.4 LOCK (parallel-eligible with §12 Uploader after v7.0.6 LOCK).
6. **§5 v6 spin + §2 v7.2 spin** open after v7.0.4 + v7.0.5 + v7.0.7 all LOCK.
7. **§13 Data Collector + §14 Report Generator + §15 Archivist** rounds open after §5 v6 + §2 v7.2 LOCK.
8. **v0.2 production cut** when all v0.2 sections LOCK.

# Appendix A — Five Laws + Four Rules adherence per v0.2 agent

| Agent | Law 1 (RFA truth) | Law 2 (boundary) | Law 3 (org isolation) | Law 4 (sector + admin-risk) | Law 5 (applicant substance) |
|---|---|---|---|---|---|
| Intake | N/A — pre-RFA | Operator-confirmed scope per fact | One PROJECT_CONTEXT per client per session | N/A — pre-draft | F-EXTRACTOR-FABRICATION enforces no fabricated facts |
| Uploader | RFA-required-fields drives package completeness | Package contents bounded by §2 vault subtree of THIS grant | One grant_id per session | N/A — assembly only | All inputs operator-signed |
| Data Collector | Reporting schedule traces to RFA + award letter | Sub-awardee universe bounded by award documents | Per-org Data Collector instance, never cross-org | Inbound text scanned for admin-risk terms; flagged to operator | Substance = sub-awardee response, never fabricated |
| Report Generator | Original proposal commitments + RFA-required-format are dual sources of truth | F-REPORT-OUT-OF-SCOPE-DRIFT enforces | One grant_id per session, one client | Funder dialect reused from grant-writing cycle | F-REPORT-COMMITMENT-UNTRACED enforces |
| Archivist | N/A — between-cycle | Workspace-aggregate vs per-org distinction is the boundary | F-ARCHIVIST-CROSS-ORG-LEAK enforces | Pattern-level vs instance-level lessons (mirrors R.6 invariant) | Proposes only; operator confirms every change |

| Agent | Rule 1 (save state) | Rule 2 (test own work) | Rule 3 (be explicit) | Rule 4 (clean output) |
|---|---|---|---|---|
| Intake | Pending-facts queue persisted on every extraction batch | F-EXTRACTOR-FABRICATION is the validation step | Per-fact: source_doc + source_page + source_quote explicit | YAML schema Pydantic-validated before queue write |
| Uploader | Submission package staged to vault on every assembly attempt | F-UPLOADER-PACKAGE-INCOMPLETE + F-UPLOADER-FORMAT-MISMATCH are the validation steps | Portal field map explicit per portal | Package manifest YAML schema Pydantic-validated |
| Data Collector | Outbound message + inbound response logged on send + receipt | F-DATACOLLECTOR-CONSENT-MISSING + F-DATACOLLECTOR-OPT-OUT-ACTIVE pre-send; F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET post-receipt | Per-recipient consent ledger entry explicit per channel | Inbound parse output schema-validated at storage |
| Report Generator | Draft persisted on every revision cycle | F-REPORT-COMMITMENT-UNTRACED + F-REPORT-COMMITMENT-MISSED + F-REPORT-OUT-OF-SCOPE-DRIFT at POST | Claim-evidence map explicit per reported claim | Draft passes through same SFR three-block discipline as v0.1 council seats |
| Archivist | Digest persisted on every cadence tick | F-ARCHIVIST-AUTO-APPLY-ATTEMPTED is the validation that Archivist proposes-only | Per-curation-action: rationale + source + proposed-action explicit | Operator-facing digest schema-validated; operator-facing summary in canonical format |

# Appendix B — Section number claims (for §0.5 Interface Index)

Reserve in §0.5 for v0.2 wave:

- §11 Intake (v0.1 LOCK target post-v7.0.4)
- §12 Uploader (v0.1 LOCK target post-v7.0.6)
- §13 Data Collector (v0.2 LOCK target)
- §14 Report Generator (v0.2 LOCK target)
- §15 Archivist (v0.2 spec; v1.x LOCK target)

These section numbers are not reserved on disk yet. The §0.5 amendment paired with the first v0.2 LOCK should claim them all at once to prevent re-numbering churn across the v0.2 wave.

---

End of memo. Self-check + session metrics owed at session close per AGENTS.md §Session Close.
