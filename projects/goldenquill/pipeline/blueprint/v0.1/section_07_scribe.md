---
title: Blueprint §7 Scribe — grant-writing seat (v1.1.1 LOCKED)
filed: 2026-04-20 (v1); 2026-04-21 (v1.1 Round-1 author-fixes); 2026-04-21 (v1.1.1 Round-2 narrow-fix carve-out); 2026-04-21 (v1.1.1 LOCKED after §7.15 prerequisite satisfied)
operator: Josh
status: **LOCKED 2026-04-21** — v1.1.1 LOCKED under L-005 two-audit cycle. Round 1 (driver) 2026-04-21: Judge `REQUIRES_MAJOR_MITIGATIONS` 93/100 + 1 CRITICAL `five_laws_cell_silently_delegated` + 3 residuals, Red Team `REQUIRES_MAJOR_MITIGATIONS` 4 HIGH + 2 MEDIUM, Editor `NEEDS_REVISION` 3 top fixes → v1.1 single-pass author fixes resolved all Round 1 findings. Round 2 (verification) 2026-04-21: Editor `READY_TO_LOCK` + Judge `READY_TO_LOCK` **100/100** (Δ +7, zero residuals, CRITICAL cleared) + Red Team `REQUIRES_MAJOR_MITIGATIONS` literal reconciled to `REQUIRES_MINOR_FIXES` per trace-substance (4/6 CLOSED + 2 genuine partials in Class A/B/C/D) → v1.1.1 narrow-fix carve-out applied in-cycle per L-005 (precedent: Vault Batch 2 gate_and_open row 33). Closeout: `pipeline/validation/section_07_thesis_round_2/CLOSEOUT.md`. Prerequisite interlock §7.15 **SATISFIED** — §6 Operating Envelope v1-r1 **LOCKED 2026-04-21** as compound transaction with §0.5 v6. §7 v1.1.1 sealed same day; runtime-live at LOCK.
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                      # v7 LOCKED 2026-04-19 — A1-A12; §D.2 Scribe + §D.7 Opus 4.7 envelope + §D.8 context-rot mitigation
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                  # v7.0.7 LOCKED 2026-05-10 — Beta classification-driven routing: Scribe runs cloud-or-local per per-call classification rule (§1); Classification Review stage canonical (§3); heavy-Judge on-demand swap canonical (§4); per-deployment router.yaml derivation (§6); SN-LLC router-template Ed25519 signing (§6.1). **Superseded by v7.0.10 at the customer-facing posture-vocabulary layer (the §1 four-posture-implicit framing collapses to the v7.0.10 three-posture-explicit framing); v7.0.7 retentions §3 + §4 + §6 + §6.1 remain canonical.**
  - pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md                 # v7.0.10 LOCKED 2026-05-11 — Three-posture routing model (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign) deprecates Sanitized / opaque-slot-token posture; Scribe routes per operator-selected deployment posture composed with per-field classification register. Under Split-Context Hybrid, Scribe's scaffold composition routes cloud against an operator-signed closed-set allow-list (RFA + section-structure-spec + dialect keywords only) and substance composition routes local — *no opaque-slot rendering round-trip*. The slot-fill agent module remains in the runtime tree as defense-in-depth-only — never invoked in normal-path cycle operation under any v7.0.10 posture. F-CLASS-SLOT-ID-NON-OPAQUE + F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED repurposed as defense-in-depth gates (broadened regex `\[SLOT_[^\]]*\]`; firing = bug or attack). v0.1 NOTE: the next §7 spin must consume v7.0.10 by formalizing the **Split-Context Hybrid drafting pattern** in the §7.5 prompt-template and §7.8 invocation contract sections; until then, the operational-today `skills/scribe-ghostwriter/SKILL.md` carries the runtime posture-aware logic per its 2026-05-10 update (slot-fill paths in SKILL.md are obsolete under v7.0.10 and must be removed at the next SKILL.md refresh).
  - pipeline/blueprint/v0.1/section_02_vault_topology.md                         # v7.1 LOCKED 2026-04-19 — Scribe writes drafts via Vault-owned primitives; never raw open()
  - pipeline/blueprint/v0.1/section_04_logician.md                               # v2.1 LOCKED 2026-04-19 — Scribe's PRE-gates and POST-gates are enforced by Logician; v0.1 NOTE: v7.0.7 LOCKED adds twelve F-CLASS-* primitives at architectural layer (Cedar/Python realization at WS-L §4 v2.x amendment per L-006 dormant-binding pattern)
  - pipeline/blueprint/v0.1/section_05_pipeline.md                               # v6 LOCKED 2026-04-18 — Scribe runs under Section 5 seat-runner; emits telemetry per §5 schema
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md               # §0.5 v5 LOCKED 2026-04-19 — Scribe primitives register as rows
prerequisite_interlock: pipeline/blueprint/v0.1/section_06_operating_envelope.md (**LOCKED 2026-04-21 v1-r1** — compound transaction with §0.5 v6 amendment per §6.17). §6 is the host for (a) `router.yaml` schema (architecture A2), (b) SFR format (architecture A3), (c) context-placement lint (architecture A4 — enforces F-CONTEXT-PLACEMENT PRE-gate on every Scribe invocation, including the middle-block F-CONTEXT-MIDDLE-CONTRADICTION sublint per §7.8), (d) track-registry (architecture A6), (e) prompt-template compilation pipeline. §7.15 prerequisite **SATISFIED** at §6 v1-r1 LOCK; §7 v1.1.1 LOCK follows same day without fail-open risk.
companion_skill: skills/scribe-ghostwriter/SKILL.md (operational today; this blueprint lifts its content into blueprint-trunk discipline without modifying the on-disk skill file).
downstream_siblings_out_of_scope: §8 Editor, §9 Judge, §10 Red Team. Each is its own blueprint round; this section pins the handoff contract with each but does not specify them.
---

# §7.1 Purpose and scope

Scribe is the grant-writing seat of the Tilth council. Its job is to draft funder-ready proposal text — section by section — that traces every claim to the RFA or to the applicant's `PROJECT_CONTEXT.md`. Scribe does NOT search for grants (that is Scout, §3), does NOT score proposals (that is Judge, §9), does NOT substantively edit (that is Editor, §8), and does NOT adversarially probe (that is Red Team, §10). Scribe authors; other seats review.

**v0.1 scope.** One seat type: grant writer at $149/seat/month consumption-based pricing (project memory `feedback_dont_drift_from_tilth_trunk.md`). One output shape: draft text in blueprint-declared section structure (§7.5) with evidence citations to RFA or `PROJECT_CONTEXT` (no web synthesis, no cross-org inference). One register at a time (Law 4 — never mix registers in one proposal).

**Out of scope for v0.1 (explicit non-goals).** Scribe does NOT auto-submit to funders. Scribe does NOT generate final PDFs (that is a downstream packaging step). Scribe does NOT write grant reports (that is v0.2 report-vertical per memory `project_report_vertical.md`). Scribe does NOT translate between languages. Scribe does NOT generate figures or graphics.

**Substance comes from the applicant (Law 5).** Scribe shapes their words and data into funder-ready language; Scribe never invents credentials, partnerships, production metrics, or outcomes the applicant has not provided. A `[NEEDED]` field in `PROJECT_CONTEXT` surfaces to the operator as an open question, never as a fabrication target.

# §7.2 Five Operating Laws — enforcement mapping

Each of the Five Laws is enforced by a combination of PRE-gates (Logician, before Scribe sees the prompt), in-seat discipline (Scribe's own output contract), and POST-gates (Logician, after Scribe returns a draft). This section maps Laws → enforcement sites. Failure codes are enumerated in §7.13.

**Law 1 — RFA is the source of truth.** Three-site trace: Logician PRE-gate → Scribe in-seat claim-evidence contract → Logician POST-gate grep verification. All three sites read the same `claim_evidence_map` shape; the operator's final sign-off (Law 5 POST-gate) is the fourth-site human confirmation.
- PRE-gate: `F-SCRIBE-RFA-MISSING` — Logician refuses the run if the named RFA file is absent from `orgs/<slug>/rfa/` or if its content hash is absent from the session manifest.
- In-seat: Scribe's draft contract requires a `claim_evidence_map` output — every factual claim in the draft maps to either `RFA:<path>:<line-range>` or `PROJECT_CONTEXT:<path>:<field>` or `USER_DATA:<conversation-anchor>` (anchor schema pinned in §7.4a).
- POST-gate: `F-SCRIBE-UNSOURCED-CLAIM` — Logician grep-checks every claim_evidence_map `DOC_SOURCED` entry against the cited file; unsourced or mis-cited → hard-block (architecture §D.5 v3 source-tag verification). Known grep limitation on paraphrased numeric claims is addressed by `F-SCRIBE-PARAPHRASED-NUMERIC` (§7.13) + `F-SCRIBE-SMART-INVENTED-METRIC` (numeric-verbatim invariant §7.6); full semantic-match enforcement is v0.2 roadmap.

**Law 2 — No boundary drift.**
- PRE-gate: `F-SCRIBE-SCOPE-MISSING` — Logician refuses the run if the active scope statement (boundary clauses pulled from RFA Phase 0 extraction) is not present in the compiled prompt at BOTH start and end (§7.10 + architecture §D.8 F-CONTEXT-PLACEMENT).
- In-seat: Scribe's output contract requires every proposed project activity to match at least one RFA "eligible project activity" category; unclear matches surface as a proposal comment `[SCOPE-CHECK]` rather than a silent draft. Scribe's `SectionDraft` carries `eligible_activity_map: tuple[EligibleActivityMatch, ...]` — every activity phrase in `body_text` mapped to the `RfaExtractedRecord.eligible_project_activities` entry it derives from (or `None` with a `[SCOPE-CHECK]` flag).
- POST-gate: **`F-SCRIBE-INELIGIBLE-ACTIVITY`** (Scribe-owned, enforced by Logician) — Logician walks `SectionDraft.eligible_activity_map` and rejects the draft if any entry has no match in `eligible_project_activities` OR if any proposal activity phrase in `body_text` is absent from `eligible_activity_map` (exhaustiveness check). This is a deterministic Logician POST-gate, NOT a delegation to Editor or Judge. Editor and Judge remain downstream clarity/scoring checks but cannot be the primary Law 2 enforcement site (would violate the audit rubric's `five_laws_cell_silently_delegated` invariant).

**Law 3 — Org isolation.**
- PRE-gate: `F-SCRIBE-ORG-CROSS-REF` — Logician refuses the run if the prompt is compiled from more than one `orgs/<slug>/` PROJECT_CONTEXT. One PROJECT_CONTEXT per session is invariant (architecture §D.5 M14 vault-access gating via Cedar `org_isolation` policy).
- In-seat: Scribe's prompt template NEVER ships prior-client examples. Program-specific templates (§7.9) carry ONLY RFA-language examples or generic language; no cross-client carryover.
- POST-gate: `F-LOGICIAN-S10A-NO-ORG-ATTRIBUTES` — Logician scans draft output for references to other org slugs via a Section 4 §4.2.1 PRE-gate row; draft blocked on cross-org leakage.

**Law 4 — Apolitical sector language + admin-risk term scanning.**
- PRE-gate: `F-SCRIBE-DIALECT-UNCLASSIFIED` — Logician refuses the run if the funder's dialect classification (Conservative / Centrist / Progressive / Soul-fire) is not present in the session manifest. Classification comes from Scout's funder record or from operator override.
- In-seat: Scribe code-switches vocabulary and framing per §7.8; substance NEVER changes based on dialect (Law 4 invariant: dialect is stylistic, not substantive).
- POST-gate: `F-SCRIBE-ADMIN-RISK-UNFLAGGED` — Logician scans the draft for admin-risk-register terms; any term at severity ≥ Medium that appears without a corresponding `[ADMIN-RISK:flag]` comment in the draft → hard-block. Operator approves every substitution (Law 4 invariant: never silently rewrite).

**Law 5 — Applicant brings the substance.**
- PRE-gate: `F-SCRIBE-KGIE-FAIL` — Logician refuses the run if the KGIE preflight (§7.4) has not been run and recorded a PASS for the current RFA.
- In-seat: Scribe's output contract forbids sentences of the form `<applicant> has <credential/data/partnership>` unless the claim traces to `PROJECT_CONTEXT` or `USER_DATA`. Invented credentials trip `F-SCRIBE-UNSOURCED-CLAIM` at POST-gate. Dialect code-switching (§7.8) MUST NOT introduce identity claims; Soul-fire vocabulary ("ancestral knowledge", "land rematriation") may only be emitted when `KgiePreflightResult.identity_claims` contains a matching affirmative entry sourced to `PROJECT_CONTEXT.identity_affirmations`.
- POST-gate: **`F-SCRIBE-DIALECT-INDUCED-IDENTITY`** — Logician walks draft body against a closed set of dialect-keyed identity-proxy phrases (schema pinned in §0.5 row `scribe.dialect_identity_proxy_table.v1`); any phrase emitted without a matching entry in `KgiePreflightResult.identity_claims` → hard-block. Covers the "my grandmother taught me → ancestral-knowledge claim" paraphrase-evasion surface. Known residual (v0.2-scoped): closed-set table requires operational curation; novel identity-proxy phrasings not yet in table evade this specific gate until the register is expanded. v0.2 roadmap: supplement the closed-set table with a semantic-embedding similarity check (parallel to qualitative-paraphrase roadmap in §7.6) and grow the table to ≥ 100 phrases across all four dialects.
- POST-gate: Operator final-review gate — "shipped" status requires operator signature on the claim-evidence map (architecture §D.5 v3 role expansion).

# §7.3 Phase 0 — RFA extraction contract

Before any drafting, Scribe invokes the Phase 0 RFA extractor and pins the extracted record to the session manifest. The extractor is a deterministic module, not an LLM call — Scribe reads the extracted record; Scribe does not re-read the raw RFA.

**Extractor input.** The RFA file path under `orgs/<slug>/rfa/` (or `vault_shared/rfas/` for SHARED RFAs, per §2 Vault Topology §2.6).

**Extractor output (`RfaExtractedRecord`, frozen, kw_only):**
- `program_name: str` — official program name.
- `cfda_or_aln: Optional[str]` — CFDA or ALN number if applicable.
- `eligible_applicant_types: tuple[str, ...]` — closed list from RFA.
- `eligible_project_activities: tuple[str, ...]` — closed list from RFA.
- `award_ceiling: Optional[Decimal]` / `award_floor: Optional[Decimal]`.
- `match_requirement: Optional[MatchRequirement]` — frozen (ratio, cash_vs_in_kind, allowable_sources).
- `deadline: DateTimeWithTimezone` — date, time, timezone; offset-aware.
- `evaluation_criteria: tuple[EvaluationCriterion, ...]` — criterion name, max points, sub-criteria if present.
- `section_structure: tuple[SectionSpec, ...]` — per-section page/word/character limits + required content cues (§7.5).
- `required_attachments: tuple[str, ...]` — forms, certifications, letters.
- `key_terms: Mapping[str, str]` — funder's definitions for project-relevant terms (e.g., "specialty crop", "value-added", "beginning farmer").
- `rfa_content_sha3_512: str` — canonical-bytes hash of the RFA file at extraction time.
- `extracted_at_utc: datetime` — extraction timestamp.

**Extractor discipline.** The extractor itself is a v0.2 roadmap item — at v0.1 it is operator-hand-populated from the RFA (§7.14 test surface treats the record as a fixture). Scribe consumes the record shape regardless of extractor provenance, so the LOCK of this section does not depend on the extractor module LOCK. The extractor's eventual module LOCK will row-append to §0.5 Index; Scribe's prompt contract does not change.

**Session-manifest pin.** `rfa_content_sha3_512` is pinned in the session manifest at Phase 0 completion. If the RFA file changes mid-session (operator edit, file replacement), the next Scribe invocation trips `F-SCRIBE-RFA-DRIFT` at Logician PRE-gate — session must re-run Phase 0.

# §7.4 Phase 1 — KGIE preflight contract

KGIE = Keywords, Geography, Identity, Experience. Must PASS before Phase 2 drafting begins.

**K — Keywords.** Funder-specific language present in RFA's `key_terms` is surfaced as a checklist; applicant affirms each term's relevance (or marks N/A with a reason). Scribe's drafts later pull language directly from this checklist — avoids synonym-drift that costs points at Judge scoring.

**G — Geography.** ARC / DRA zone, Justice40 tract, urban / rural designation per USDA, state, county. All pulled from `PROJECT_CONTEXT.location` and verified against RFA's geographic eligibility constraints. Missing geography → stop-and-ask, not infer-from-address.

**I — Identity.** SDA / BIPOC / women-led / veteran / beginning farmer / tribal / urban — whatever applies per RFA priority points. Pulled from `PROJECT_CONTEXT.identity_affirmations`. Each identity claim must trace to an affirmative applicant statement; Scribe never infers identity from name or demographic proxy (Law 5 + anti-fabrication).

**E — Experience.** Years operating, production metrics, prior grants, certifications, degrees, partnerships. Pulled from `PROJECT_CONTEXT.experience` + `PROJECT_CONTEXT.prior_grants`. Scribe may compute derived quantities (e.g., "3-year production trajectory") from supplied data but cannot add new data points.

**KGIE record (`KgiePreflightResult`, frozen, kw_only):**
- `status: Literal["pass", "fail", "needs_operator_input"]`.
- `keywords_checked: tuple[KeywordCheck, ...]` — (term, applicant_affirmation, source).
- `geography_verified: GeographyRecord` — frozen; `state`, `county`, `zone_tags: tuple[str, ...]`, `jsutice40_tract: Optional[str]`, `rfa_geographic_match: bool`.
- `identity_claims: tuple[IdentityClaim, ...]` — (claim, source_field_in_project_context, rfa_priority_points).
- `experience_summary: ExperienceSummary` — years_operating, production_metrics (frozen mapping), prior_grants (frozen tuple), certifications (frozen tuple), partnerships (frozen tuple).
- `needed_fields: tuple[str, ...]` — `[NEEDED]` fields Scribe hit during KGIE; operator-facing open questions.
- `preflight_at_utc: datetime`.

**PASS condition.** `status == "pass"` iff every K entry is affirmed-or-N/A, geography is verified, every I claim has a source, and E has no critical gaps. Any `needed_fields` → `status = "needs_operator_input"`; Scribe halts and surfaces the question list.

**FAIL condition.** Scribe refuses to draft if KGIE fails. There is no "draft with placeholders" path — placeholders regularly survive into submitted drafts and degrade Judge scores.

# §7.4a USER_DATA conversation-anchor schema (v1)

`USER_DATA:<conversation-anchor>` in the `claim_evidence_map` must resolve to a specific, verifiable turn of the operator-Scribe conversation. At v1.1 the anchor schema is:

```
USER_DATA:<session_manifest_run_id>:<turn_ordinal>:<sha3_512(canonical_turn_bytes)[:32]>
```

- `session_manifest_run_id` — the run-scoped UUID pinned in the session manifest at Phase 0.
- `turn_ordinal` — monotonically ascending integer index of the operator turn within the run-scoped append-only conversation log.
- `sha3_512(canonical_turn_bytes)[:32]` — 32-hex-char prefix (128 bits) of the canonical-bytes hash of the turn's UTF-8-NFC-normalized text. Prefix width sized to make birthday-bound collision attack (~2^64 log entries) computationally infeasible for any realistic grant-writing session. Full 128-char (512-bit) hash is stored in the log entry; the prefix is the anchor's compact reference.

**Storage.** Conversation log is persisted as an append-only Vault artifact `orgs/<slug>/conversations/<run_id>.log.jsonl` under §2 Vault SIMPLE-path primitives; each entry carries `turn_ordinal`, `role`, `canonical_turn_sha3_512` (full 128-char hash), and `turn_bytes_canonical`. **Integrity invariant (v1.1 narrow-fix).** The log file is owned by the Vault write-dispatcher under §4.10 kind-class gate `conversation_log`; direct append by any same-uid peer process outside the dispatcher trips `F-PRE-VAULT-KIND-CLASS-UNAUTHORIZED` at PRE-gate. v0.2 roadmap commitment: promote conversation logs under a SIGNED-path Vault lane with per-turn operator signature (parallel to §7.9 template-integrity v0.2 commitment), closing same-uid fabricated-turn-append residual entirely.

**Verification at POST-gate.** `F-SCRIBE-UNSOURCED-CLAIM` resolves each `USER_DATA:<...>` anchor by reading the conversation log, re-canonicalizing the turn text, recomputing the full hash, verifying the 32-hex prefix matches, and grep-checking the claim against the turn body. Anchor resolution failures (missing turn, hash mismatch, run_id drift, turn_ordinal out of order) trip **`F-SCRIBE-CONVERSATION-ANCHOR-INVALID`**.

**Interlock with §6.** §6 Operating Envelope LOCKs the conversation-log persistence contract against the `router.yaml` track-registry; §7 v1.1 pins the anchor SHAPE but defers the read-path implementation to §6's prompt-template compilation pipeline. OQ-7.3 is closed at shape level; implementation binding is an INTERLOCK to §6 v1 LOCK.

# §7.5 Phase 2 — Section-by-section drafting contract

**Terminology pin (Editor clarity discipline).** Across this blueprint and its output contracts:
- **Goals** — the applicant's overall aims (qualitative; narrative framing).
- **Outputs** — tangible deliverables produced during the grant period (e.g., workshops held, acres improved).
- **Outcomes** — measurable changes resulting from outputs (e.g., 30% yield increase).
- **Objectives** — SMART-format specific targets the grant commits to achieving. "SMART objectives" is the canonical operational term throughout §7.6 and the `SmartObjective` shape; "goals" and "outcomes" are narrative constructs; "outputs" are the deliverable tier below outcomes.

Standard section structure (RFA-specific overrides authored per §7.9 templates):

1. **Cover Page** — entity name, EIN / UEI, program, amount requested, contact.
2. **Executive Summary** — one paragraph, hits every evaluation criterion from `RfaExtractedRecord.evaluation_criteria` at least once.
3. **Needs Statement / Problem** — data-driven, every statistic cited to a source, ties to funder priorities from `key_terms`.
4. **Project Description** — what, how, with whom. Activities enumerated must subset `eligible_project_activities`.
5. **SMART Objectives, Outcomes & Measurements** — SMART-format objectives per §7.6 paired with narrative outcome + measurement text.
6. **Work Plan / Timeline** — milestones with dates; timeline length subset of RFA-allowed project duration.
7. **Budget & Budget Narrative** — line items with justification; run Overlooked Expenses checklist (§7.7) before finalize.
8. **Organizational Capacity** — team quals, facilities, prior performance. Every claim sources to `PROJECT_CONTEXT`.
9. **Partnerships & Letters of Support** — who is committed, what they bring. Each partner sourced to `PROJECT_CONTEXT.partnerships` with letter-of-support status.
10. **Evaluation Plan** — how success is measured, who evaluates.
11. **Sustainability** — what happens after the grant period.
12. **Equity / Community Benefits** — if RFA asks for it; OMITTED if not asked.
13. **Attachments checklist** — what is needed (from `RfaExtractedRecord.required_attachments`), what is ready, what is missing.

**Per-section output contract (`SectionDraft`, frozen, kw_only):**
- `section_name: str` — one of the 13 above or a program-specific override.
- `section_order: int`.
- `body_text: str` — the draft text.
- `word_count: int` / `character_count: int`.
- `rfa_section_limit: Optional[SectionLimit]` — (limit_kind ∈ {"words", "characters", "pages"}, limit_value). `None` if RFA does not cap the section.
- `claim_evidence_map: tuple[ClaimEvidence, ...]` — every factual claim in `body_text` maps to an evidence source.
- `eligible_activity_map: tuple[EligibleActivityMatch, ...]` — every proposed project activity phrase in `body_text` mapped to the `RfaExtractedRecord.eligible_project_activities` entry it derives from (or `None` with a `[SCOPE-CHECK]` flag). Load-bearing for `F-SCRIBE-INELIGIBLE-ACTIVITY` POST-gate (§7.2 Law 2).
- `admin_risk_flags: tuple[AdminRiskFlag, ...]` — terms scanned at Medium+ severity that the applicant has not yet approved a substitution for.
- `scope_check_comments: tuple[ScopeCheckComment, ...]` — proposed activities that could be scope drift.
- `draft_dialect: Literal["conservative", "centrist", "progressive", "soul_fire"]` — snapshot of the dialect selected at draft time; re-invocation must match.
- `drafted_at_utc: datetime`.

**Section ordering invariant.** Scribe emits sections in `section_order` ascending; no section is drafted before Phase 0 + Phase 1 PASS. Re-drafting a single section preserves other sections' drafts (idempotent section-level re-runs).

# §7.6 SMART outcome generator contract

Every objective under §7.5 section 5 must produce:

- **S**pecific action — verb + object.
- **M**easurable outcome — number or percentage; no "we hope" or "aim to".
- **A**chievable — given resources and timeline as specified in Phase 0 and KGIE E.
- **R**elevant — to RFA's stated priorities (verified against `key_terms` + `evaluation_criteria`).
- **T**ime-bound — by when, within project duration.

**Output shape per objective (`SmartObjective`, frozen, kw_only):**
- `objective_text: str` — "[Action] by [date]."
- `outcome_text: str` — "[Measurable change]."
- `measurement_text: str` — "[Data collection method]."
- `timeline_text: str` — "[Duration]."
- `achievability_evidence: str` — pointer to `PROJECT_CONTEXT` fields that make this achievable given stated resources.
- `relevance_pointer: tuple[str, ...]` — which RFA `evaluation_criteria` this outcome maps to.

**Scribe invariant.** Scribe NEVER generates a numeric outcome the applicant has not supplied. If the applicant has not supplied a baseline production metric, Scribe cannot write "increase from 200 to 800 lbs/month"; it writes "[baseline needed]" and routes to operator-facing open question.

**Numeric-verbatim invariant (v1.1, closes paraphrase-evasion surface).** Every numeric token in a Scribe draft — years of experience, production quantities, acreage, dollar amounts, percentages — must appear verbatim in the cited evidence source (byte-identical after unit-normalization). Paraphrased numerics ("nearly half a decade" for "3 years", "almost 1,000 lbs" for "800 lbs") are forbidden. Enforcement: POST-gate `F-SCRIBE-PARAPHRASED-NUMERIC` walks each `claim_evidence_map` entry whose claim contains a numeric token; Logician extracts both sides and requires byte-identity after normalization. Qualitative paraphrase remains permitted; numeric paraphrase does not. This closes the Round 1 Red Team R-2 finding at the shape level; full semantic-match enforcement across qualitative paraphrase is v0.2 roadmap.

# §7.7 Overlooked Expenses checklist contract

Before finalizing any budget, Scribe walks the checklist:

- In-kind space and utilities (rent, electricity, water, internet).
- Volunteer / board labor (match value).
- Printing, postage, branding, translation.
- Audit and grant-reporting costs.
- Compliance (FDA, GAP, organic certification, FSMA).
- Travel / mileage for outreach.
- Evaluation / data collection tools.
- Insurance and legal fees.
- Packaging, storage, freight.
- Training and professional development.
- Indirect costs (if allowed by RFA).

**Checklist record (`OverlookedExpensesWalk`, frozen, kw_only):**
- `walk_at_utc: datetime`.
- `entries: tuple[OverlookedExpenseEntry, ...]` — per-line-item: (item, status ∈ {"included", "n_a", "needed"}, rationale).
- `needed_count: int` — count of `status == "needed"`; Scribe halts budget finalization if > 0.
- `rfa_indirect_costs_allowed: Optional[bool]`.

**Non-bypassable invariant.** Scribe cannot emit a finalized `SectionDraft` for section 7 (Budget) with `needed_count > 0`. Operator must resolve each "needed" to "included" or "n_a" before finalize.

# §7.8 Funder dialect code-switching contract (architecture §D.2 + Law 4)

Four dialects. Vocabulary and framing only; substance never changes.

**Conservative / USDA Standard.** Examples: USDA Farm Service Agency RFAs. Vocabulary: production efficiency, economic impact, market competitiveness, return on investment, food security.

**Centrist.** Examples: NSF standard program solicitations. Vocabulary: balanced growth, community resilience, evidence-based, public-private partnership.

**Progressive.** Examples: USDA SARE. Vocabulary: equity, food sovereignty, environmental justice, climate resilience, community self-determination.

**Soul-fire.** Examples: Bread and Roses Community Fund. Vocabulary: land rematriation, ancestral knowledge, healing justice, community power, liberation.

**Selection mechanism.** Dialect is selected per-funder at Phase 0 and pinned to the session manifest. Operator may override (manifest carries `dialect_operator_override: Optional[str]`). Default if unclassified → Conservative / USDA Standard (skill default).

**Register-mix invariant.** Scribe MUST NOT mix registers within one proposal. The compiled prompt carries the selected dialect as a load-bearing constraint at start, middle, AND end of the prompt (architecture §D.8 F-CONTEXT-PLACEMENT + §6 F-CONTEXT-MIDDLE-CONTRADICTION sublint). Register-drift within a single draft is a POST-gate finding `F-SCRIBE-DIALECT-DRIFT`; middle-block contradictory vocabulary (e.g., Progressive phrasing injected into a Conservative-framed body while start/end blocks remain Conservative) is caught by `F-CONTEXT-MIDDLE-CONTRADICTION` (§6-owned, forwarded as blocker to Scribe per §7.13 forwarded codes).

**Dialect DOES NOT affect substance.** Invariant (Law 4 + Law 5): applicant's facts, data, partnerships, and identity claims are identical across all four dialects. Only lexical surface changes. Dialect vocabulary NEVER introduces identity claims absent from `KgiePreflightResult.identity_claims`; enforcement is `F-SCRIBE-DIALECT-INDUCED-IDENTITY` at POST-gate (§7.2 Law 5).

# §7.9 Program-specific templates

Each template augments the standard §7.5 section structure with program-specific required content cues. Templates live under `skills/scribe-ghostwriter/templates/<program>.md` and are loaded by the Scribe seat runner at Phase 0 based on the RFA's program identity.

**VAPG (Value-Added Producer Grant).** Required content cues: feasibility study reference, marketing plan, producer ownership, value-added methodology, independent producer or cooperative status.

**REAP (Rural Energy for America Program).** Required content cues: energy audit, baseline vs projected energy use, payback period, technical report.

**SCBGP (Specialty Crop Block Grant Program).** Required content cues: industry-wide benefit (not just applicant), measurable dissemination plan, specialty crop focus.

**SARE (Sustainable Agriculture Research and Education).** Required content cues: farmer involvement, sustainable ag practices, research / education integration.

**SBIR (Small Business Innovation Research).** Required content cues: technical innovation, commercialization potential, Phase I / II structure.

**AFRI (Agriculture and Food Research Initiative).** Required content cues: scientific merit, clear hypotheses, preliminary data, broader impacts.

**Section 2501 Outreach.** Required content cues: outreach plan for SDA / veterans, capacity-building focus.

**UAIP (Urban Agriculture and Innovative Production).** Required content cues: food access, equity, urban partnerships.

**Template contract (`ProgramTemplate`, frozen, kw_only):**
- `program_code: str` — one of the above or a v0.2 addition.
- `section_overrides: Mapping[str, SectionSpec]` — any section name → augmented SectionSpec.
- `required_content_cues: tuple[str, ...]` — flags Scribe must satisfy in the final draft.
- `dialect_default: Literal["conservative", "centrist", "progressive", "soul_fire"]` — suggested register; operator can override.
- `template_at_utc: datetime`.

**Extensibility.** New programs are row-append to `skills/scribe-ghostwriter/templates/`; each ships with at least one passing corpus fixture (§7.14). No core-module refactor per new program.

**Template-integrity invariant (v1.1, closes tamper-bucket-a surface).** At Phase 0, Scribe's runner reads each program template via the Vault `template-query` primitive and captures `template_content_sha3_512` into the session manifest. At Phase 2 draft compile, the runner RE-reads the template and trips PRE-gate `F-SCRIBE-TEMPLATE-DRIFT` on hash mismatch. This closes the same-uid-peer-tamper window *between* Phase 0 pin and Phase 2 consume without requiring v0.1 templates to migrate into Vault signed-commit storage.

**Known residual threat surfaces (explicit, v0.2-scoped).** The v0.1 hash-pin is an interim control with two acknowledged gaps: (a) pre-Phase-0 tamper — if a same-uid peer modifies the template file *before* the Phase 0 hash-pin is captured, the pinned hash reflects the malicious content and no mismatch fires (TOCTOU at pin-time); (b) loader tampering — substitution of the template-loader binary itself bypasses the file-hash check entirely. Both gaps close when v0.2 migrates `skills/scribe-ghostwriter/templates/` → `vault_shared/scribe_templates/` under §2 Vault SIGNED-path with operator commit-signature verification at both write-time and read-time (parallel to architecture M15 vault-access discipline). v0.1 threat model explicitly assumes single-operator process integrity; the interim hash-pin catches the between-pin-and-consume window which is the operationally most likely attack vector.

# §7.10 Word / character / page limit protocol

If Scribe's draft exceeds the RFA's section limit, Scribe DOES NOT silently compress. Scribe:

1. Emits the uncut draft as `SectionDraft` with `body_text` over the limit; `over_limit_flag: True`.
2. Emits a priority-ranking question to the operator: "This section is over limit. Rank: Keywords and funder language / Outcomes and measurements / Geography-identity qualifiers / Organizational capacity / Narrative flow. Compress in that order of preservation?"
3. After operator ranking, Scribe produces a compliant version AND keeps the uncut draft. Both are returned; operator decides what gets submitted.

**Compliant-version record (`CompressedSectionDraft`, frozen, kw_only):** wraps `SectionDraft` with `source_uncut_draft_sha3_512` + `compression_rationale: tuple[str, ...]`.

# §7.11 Admin-risk term scanning integration with Logician (Law 4 operational)

Scribe's draft output passes through Logician's admin-risk term scanner at POST-gate. The scanner reads the admin-risk register (18 entries at v0.1 per project memory `project_openclaw_state.md`), walks the draft text, and emits a findings record per match.

**Severity tiers.**
- **Low.** Scribe may silently substitute if a substitution mapping exists in the admin-risk register AND the applicant has pre-approved "auto-substitute-low". Otherwise flag.
- **Medium.** Always flag. Scribe produces the draft with an inline `[ADMIN-RISK:<term>:<proposed-substitution>]` comment; operator approves, rejects, or replaces.
- **High.** Always flag AND hard-block draft finalization until operator explicitly approves. `F-SCRIBE-ADMIN-RISK-HIGH-UNAPPROVED` surfaces on attempted finalize.

**Invariant (Law 4).** Scribe NEVER silently rewrites a Medium or High severity term. The applicant reviews and approves each substitution. This invariant is enforced at Logician POST-gate; Scribe's in-seat discipline is correctness-by-construction via prompt template (architecture §D.8 + §6 Operating Envelope).

# §7.12 Editor + Judge handoff contract

**Handoff to Editor (§8).** Scribe emits per-section `SectionDraft` records to the section-ordered drafts manifest `orgs/<slug>/drafts/<run_id>/sections/*.json` (atomic write via Vault primitive per §2 Vault). Editor consumes this manifest; Editor's findings return on `orgs/<slug>/drafts/<run_id>/editor_findings.json`. Editor does NOT re-draft; Editor flags and offers options. Scribe consumes Editor findings at revision time (not v1 scope — revision-loop lives in §8 Editor + §10 Red Team).

**Handoff to Judge (§9).** Judge reads the finalized `SectionDraft` + `claim_evidence_map` and scores against the funder's rubric first, related rubrics next (architecture §D.4). Judge's scores return on `orgs/<slug>/drafts/<run_id>/judge_scores.json`. Scribe consumes Judge scores at revision time only — not in v1 draft flow.

**Handoff to operator.** Final draft + claim-evidence map + admin-risk flags + scope-check comments go to operator for sign-off (architecture §D.5 v3 operator final-review gate). Operator signature on the claim-evidence map → "shipped" status. No draft ships without operator signature — Scribe has no auto-submit path (§7.1 non-goal).

**Cross-family rigor (Section E).** Scribe's provider family MUST NOT match Judge's provider family (architecture §E v2 invariant M5). `router.yaml` schema under §6 Operating Envelope enforces this at pipeline start; Logician PRE-gate `F-ROUTER-FAMILY-COLLISION` fails-closed on violation. v0.1 binding per `/router.yaml` (source of truth — this blueprint cites the live binding and tracks it by reference): Scribe primary = Anthropic Claude (Sonnet 4.6 floor, Opus 4.6/4.7 for xhigh-effort runs with max_tokens ≥ 64000 + beta header `task-budgets-2026-03-13` per §D.7 Block 1); Judge primary = Google Gemini 2.5 Pro (updated 2026-04-19 from prior Alibaba/Groq binding). Router family families for invariant M5 collision check: Anthropic vs Google are distinct families → PASS. If `router.yaml` is updated, this section's text does NOT drift — CLAUDE.md convention pins `router.yaml` as the sole source of truth for model bindings.

# §7.13 Failure codes

Scribe-specific failure codes (emitted by Logician PRE or POST-gates enforcing Scribe invariants):

**PRE-gates (before Scribe runs):**
- **`F-SCRIBE-RFA-MISSING`** — named RFA file absent from `orgs/<slug>/rfa/` or `vault_shared/rfas/`; or content hash absent from session manifest.
- **`F-SCRIBE-RFA-DRIFT`** — RFA file's current SHA-3-512 does not match session-manifest-pinned hash; operator edited RFA mid-session.
- **`F-SCRIBE-SCOPE-MISSING`** — compiled prompt missing scope statement at start OR end (subset of architecture §D.8 F-CONTEXT-PLACEMENT; §6 Operating Envelope lint emits this subclass).
- **`F-SCRIBE-ORG-CROSS-REF`** — prompt compiled with content from more than one `orgs/<slug>/` PROJECT_CONTEXT.
- **`F-SCRIBE-DIALECT-UNCLASSIFIED`** — funder's dialect classification missing from session manifest and no operator override supplied.
- **`F-SCRIBE-KGIE-FAIL`** — KGIE preflight has not PASSED for the current RFA.
- **`F-SCRIBE-PHASE-0-MISSING`** — `RfaExtractedRecord` not pinned in session manifest.
- **`F-SCRIBE-TEMPLATE-UNKNOWN`** — RFA's program identity maps to a template not present in `skills/scribe-ghostwriter/templates/`.
- **`F-SCRIBE-TEMPLATE-DRIFT`** — program template's current SHA-3-512 does not match session-manifest-pinned hash captured at Phase 0 (closes same-uid-peer tamper window per §7.9).
- **`F-SCRIBE-ADMIN-RISK-REGISTER-STALE`** — admin-risk register snapshot age exceeds §7.16 freshness bound at prompt compile time.

**POST-gates (after Scribe emits a draft):**
- **`F-SCRIBE-UNSOURCED-CLAIM`** — a factual claim in `body_text` has no matching `claim_evidence_map` entry, OR the mapped evidence does not grep-match the claim (architecture §D.5 v3 source-tag verification). Known limitation: literal grep does not catch paraphrased *qualitative* claims; numeric paraphrase is caught separately by `F-SCRIBE-PARAPHRASED-NUMERIC`; full semantic-match across qualitative paraphrase is v0.2 roadmap.
- **`F-SCRIBE-PARAPHRASED-NUMERIC`** — numeric token in `body_text` is not byte-identical (after unit-normalization) to its cited evidence source; closes the "3 years → nearly half a decade" paraphrase-evasion surface (§7.6 numeric-verbatim invariant).
- **`F-SCRIBE-DIALECT-INDUCED-IDENTITY`** — dialect-keyed identity-proxy phrase (closed-set table per §0.5 row `scribe.dialect_identity_proxy_table.v1`) emitted without a matching entry in `KgiePreflightResult.identity_claims` (§7.2 Law 5, closes the Soul-fire "my grandmother taught me → ancestral-knowledge claim" surface).
- **`F-SCRIBE-CONVERSATION-ANCHOR-INVALID`** — `USER_DATA:<anchor>` does not resolve against conversation log (missing turn_ordinal, hash mismatch, run_id drift per §7.4a).
- **`F-SCRIBE-ADMIN-RISK-HIGH-UNAPPROVED`** — High-severity admin-risk term present in draft without operator approval.
- **`F-SCRIBE-ADMIN-RISK-UNFLAGGED`** — Medium+ severity term in draft without `[ADMIN-RISK:…]` comment.
- **`F-SCRIBE-DIALECT-DRIFT`** — draft contains vocabulary from more than one dialect register at start/end blocks (middle-block contradictions caught by §6 `F-CONTEXT-MIDDLE-CONTRADICTION`, forwarded).
- **`F-SCRIBE-SECTION-OVER-LIMIT-UNFLAGGED`** — section exceeds `rfa_section_limit` without `over_limit_flag=True` and priority-ranking question surfaced.
- **`F-SCRIBE-OVERLOOKED-EXPENSE-UNRESOLVED`** — Budget section finalized with `OverlookedExpensesWalk.needed_count > 0`.
- **`F-SCRIBE-SMART-INVENTED-METRIC`** — SMART objective carries a numeric baseline or target that has no source in `PROJECT_CONTEXT` or `USER_DATA`.
- **`F-SCRIBE-EVALUATION-CRITERION-MISSING`** — Executive Summary does not touch every `evaluation_criteria` entry at least once.
- **`F-SCRIBE-INELIGIBLE-ACTIVITY`** — proposed activity in `SectionDraft.eligible_activity_map` does not match any entry in RFA's `eligible_project_activities`, OR proposal activity phrase in `body_text` is absent from `eligible_activity_map` (exhaustiveness failure). Primary Scribe-owned POST-gate for Law 2 (§7.2) — NOT a delegation to Editor or Judge.

**Forwarded (not Scribe-emitted but can block Scribe runs):**
- `F-CONTEXT-PLACEMENT` (architecture §D.8 / §6 Operating Envelope).
- `F-ROUTER-FAMILY-COLLISION` (architecture §E / §6 Operating Envelope).
- `F-ROUTER-STALE-API` (architecture §D.7).
- `F-LOGICIAN-S10A-NO-ORG-ATTRIBUTES` (Section 4).
- `F-LOGICIAN-TOKEN-LEAK` (Section 4 §4.12 PRE-append, if any Scribe output touches admin-risk ledger).

# §7.14 Test surface

**Unit tests on the extracted-record + KGIE + SMART + overlooked-expenses shapes.**
- `test_rfa_extracted_record_is_frozen` — every field immutable; `object.__setattr__` OUT-OF-MODEL documentation only.
- `test_kgie_preflight_pass_requires_all_four_dimensions` — constructing a `KgiePreflightResult(status="pass")` with any missing dimension raises invariant violation.
- `test_smart_objective_requires_measurement` — `SmartObjective` with empty `measurement_text` fails construction predicate.
- `test_overlooked_expenses_walk_blocks_finalize_on_needed` — `OverlookedExpensesWalk.needed_count > 0` cannot be finalized as budget section.

**Golden drafts corpus (`tests/corpus/scribe/v1/`).**
- `pass/vapg_happy_path/` — VAPG RFA fixture + PROJECT_CONTEXT fixture + expected draft sections + expected claim-evidence map.
- `pass/reap_happy_path/` — same shape, REAP.
- `pass/scbgp_happy_path/` — same shape, SCBGP.
- `pass/sare_happy_path/` — same shape, SARE.
- `fail/kgie_fails_missing_geography/` — fixture with PROJECT_CONTEXT missing `location.county`; expect `F-SCRIBE-KGIE-FAIL` at PRE-gate.
- `fail/unsourced_claim_in_capacity/` — fixture with body_text claiming "15 years operating" but PROJECT_CONTEXT.experience.years_operating=8; expect `F-SCRIBE-UNSOURCED-CLAIM` at POST-gate.
- `fail/admin_risk_high_unflagged/` — draft containing a High-severity admin-risk term; expect `F-SCRIBE-ADMIN-RISK-HIGH-UNAPPROVED`.
- `fail/dialect_drift/` — draft mixing Conservative and Progressive vocabulary in one section; expect `F-SCRIBE-DIALECT-DRIFT`.
- `fail/over_limit_unflagged/` — section exceeding RFA limit with `over_limit_flag=False`; expect `F-SCRIBE-SECTION-OVER-LIMIT-UNFLAGGED`.
- `fail/ineligible_activity/` — Project Description proposing an activity not in `eligible_project_activities`; expect `F-SCRIBE-INELIGIBLE-ACTIVITY`.

**Property tests.**
- `test_prop_section_order_ascending` — every emitted drafts manifest has monotonically ascending `section_order` values.
- `test_prop_claim_evidence_map_is_exhaustive` — for every 100-sentence random-corpus draft, every sentence with a named entity has at least one `claim_evidence_map` entry.
- `test_prop_dialect_pinned_per_draft` — over 1000 runs with fixed funder classification, `SectionDraft.draft_dialect` is invariant per `run_id`.

**Adversarial tests.**
- `test_adv_applicant_claims_partnership_not_in_project_context` — applicant message says "we partner with Penn State" but `PROJECT_CONTEXT.partnerships` does not list it; Scribe omits from draft (USER_DATA claim path requires conversation-anchor; if Scribe drafts the partnership in, POST-gate catches with `F-SCRIBE-UNSOURCED-CLAIM`).
- `test_adv_funder_dialect_conflict_with_admin_risk_term` — admin-risk register flags a term; progressive dialect would naturally use the term; Scribe must flag rather than silently substitute.
- `test_adv_section_over_limit_after_operator_ranking_still_over` — operator ranks priorities, Scribe compresses, still over limit; Scribe loops (bounded by N=2 per §5 Pipeline revision-loop cap) then hard-stops and surfaces.
- `test_adv_rfa_drift_mid_session` — operator edits the RFA after Phase 0; next Scribe invocation trips `F-SCRIBE-RFA-DRIFT`.
- `test_adv_smart_invented_metric` — prompt applicant supplied "we hope to increase"; Scribe emits `baseline_needed` placeholder, not an invented number; `F-SCRIBE-SMART-INVENTED-METRIC` catches if the placeholder-skip is missed.

**Integration tests (Scribe + Logician + Vault dispatcher).**
- `test_int_scribe_emits_draft_atomically` — drafts manifest is written via §2 Vault dispatcher SIMPLE path; crash mid-write leaves no partial manifest.
- `test_int_scribe_runs_under_seat_runner` — Scribe invoked via §5 Pipeline seat-runner; telemetry schema matches §5 §5.6 per_invocation_telemetry_record.
- `test_int_scribe_cross_family_rigor_enforced` — router.yaml binding sets Scribe and Judge to the same family; pipeline start trips `F-ROUTER-FAMILY-COLLISION`.

# §7.15 Interfaces and forward dependencies

**Upstream (Scribe consumes):**
- Section 0.5 Interface Index — Scribe primitives register as rows (see §7.17).
- Section 2 Vault Topology — `RfaExtractedRecord`, `PROJECT_CONTEXT`, drafts manifest persisted via SIMPLE `vault_write` under §4.10 dispatcher.
- Section 3 Scout — funder identity + dialect classification (when Scout is wired; v0.1 scope may have operator-hand-populated funder records).
- Section 4 Logician — PRE-gates and POST-gates enforcing §7.2 Five-Laws mapping.
- Section 5 Pipeline — seat-runner that invokes Scribe under the track-scoped seat-runner contract (§5 v6 telemetry schema).

**Downstream (Scribe emits to):**
- Section 8 Editor — consumes `SectionDraft` records; emits findings.
- Section 9 Judge — consumes finalized drafts + claim-evidence map; emits scores.
- Section 10 Red Team — consumes draft set for adversarial probe.
- Operator — consumes draft + all review outputs for final sign-off.

**Prerequisite interlock (§6 Operating Envelope) — SATISFIED at §6 v1-r1 LOCK 2026-04-21.** Scribe v1 LOCK was gated on §6 v1 LOCK. §6 v1-r1 LOCKED 2026-04-21 as compound transaction with §0.5 v6 amendment per §6.17; §7 v1.1.1 LOCK sealed same day. Interlock provisions now hold live:
- §6 specifies the `router.yaml` schema so Scribe's provider binding validates against it (A2). ✅
- §6 specifies the SFR format so Scribe's telemetry output conforms (A3). ✅
- §6 specifies the prompt-template compilation pipeline + context-placement lint so Scribe's F-CONTEXT-PLACEMENT subclass (`F-SCRIBE-SCOPE-MISSING`) is enforceable (A4). ✅
- §6 specifies the track-registry so Scribe's invocation binds to a known track (A6). ✅

The discipline "Do not LOCK §7 ahead of §6" was observed: §7 v1 SCOPING DRAFT held at LOCK-READY while Round 1+2 audits completed, and LOCK-sealed only after §6 v1-r1 LOCK landed same day.

**Sibling-out-of-scope pin.** §8 Editor, §9 Judge, §10 Red Team each require their own blueprint round. §7 v1 names the handoff contracts (§7.12) but does NOT specify those sibling seats' internals. Any §8/§9/§10 content added here during Thesis-round audit must be kicked back.

# §7.16 Admin-risk register integration (v0.1)

At v0.1, the admin-risk register has 18 entries (project memory `project_openclaw_state.md`). Scribe consumes the register via a Vault-owned `admin-risk-register-query` skill (pattern parallel to §D.1 `vault-query`); Scribe does NOT open the register file directly. Register entries carry:

- `term: str` — the term or phrase.
- `severity: Literal["low", "medium", "high"]`.
- `suggested_substitution: Optional[str]`.
- `rationale: str` — why this term carries administrative risk for grant review (e.g., "triggers USDA conservative-panel scrutiny", "historically associated with rejected Section 2501 applications").
- `applicable_dialects: tuple[str, ...]` — subset of the four dialects; some terms are risk-free in Progressive but High-severity in Conservative.
- `entry_added_at_utc: datetime` / `entry_added_by: str`.

**Register growth.** New entries are operator-authored with HIGH-severity admin-risk ledger append (register meta-maintenance is itself subject to admin-risk discipline). Register growth is NOT a blueprint amendment; it is an operational register mutation. Blueprint LOCK captures the register's schema, not its contents.

**v0.1 coverage gap acknowledgment (Round 1 Red Team MEDIUM).** The 18-entry v0.1 register is known to miss several high-impact term families: explicitly (a) colonial-era framing ("colonial", "colonization"), (b) climate-emergency terminology ("climate emergency", "climate crisis") — high-risk in Conservative dialect, risk-free in Progressive, (c) political identifiers (candidate and officeholder names), (d) law-enforcement framing ("policing", "prison"). These gaps are the operator's top register-growth targets for v0.1.1 maintenance. Scribe's runtime is NOT blocked on register completeness — register snapshot freshness (≤ 24h per OQ-7.5) is the enforced invariant — but operator is on notice that silent register gaps admit attack surface. The v0.2 register carries a target floor of ≥ 50 entries across the four dialect columns.

**Scribe invariant.** Scribe's compiled prompt carries the current register at compile time (snapshot). Prompt-template lint (§6) verifies the register is non-empty and fresh (snapshot age ≤ 24 hours). Stale snapshot → `F-SCRIBE-ADMIN-RISK-REGISTER-STALE`.

# §7.17 §0.5 Interface Index rows (proposed at LOCK)

At §7 v1 LOCK, row-append to §0.5 (current LOCKED v5, 101 rows; next version slot after pending sibling amendments):

- `scribe.rfa_extracted_record.v1` (schema) — §7.3 `RfaExtractedRecord` shape; parent §7 v1.
- `scribe.kgie_preflight_result.v1` (schema) — §7.4 `KgiePreflightResult` shape; parent §7 v1.
- `scribe.section_draft.v1` (schema) — §7.5 `SectionDraft` shape; parent §7 v1.
- `scribe.smart_objective.v1` (schema) — §7.6 `SmartObjective` shape; parent §7 v1.
- `scribe.overlooked_expenses_walk.v1` (schema) — §7.7 `OverlookedExpensesWalk` shape; parent §7 v1.
- `scribe.program_template.v1` (schema) — §7.9 `ProgramTemplate` shape; parent §7 v1.
- `scribe.dialect_register.v1` (constant) — §7.8 four-value enumeration {conservative, centrist, progressive, soul_fire}; parent §7 v1.
- `scribe.claim_evidence_entry.v1` (schema) — §7.2 Law 1 claim_evidence_map entry shape; parent §7 v1 + §4 v2.1.
- `scribe.admin_risk_flag.v1` (schema) — §7.11 AdminRiskFlag shape; parent §7 v1 + admin-risk register integration.
- `scribe.section_order_invariant.v1` (invariant) — §7.5 ordering invariant; parent §7 v1.
- `scribe.dialect_register_mix_ban.v1` (invariant) — §7.8 Law 4 no-mixing invariant; parent §7 v1 + architecture §D.2.
- `scribe.eligible_activity_match.v1` (schema) — §7.5 `EligibleActivityMatch` shape supporting Law 2 POST-gate; parent §7 v1.1.
- `scribe.conversation_anchor.v1` (schema) — §7.4a USER_DATA conversation-anchor canonical shape; parent §7 v1.1 + §6 v1 (conversation-log persistence).
- `scribe.dialect_identity_proxy_table.v1` (closed-set constant) — §7.2 Law 5 POST-gate table of dialect-keyed identity-proxy phrases; parent §7 v1.1.
- `scribe.failure_code.F-SCRIBE-RFA-MISSING.v1` through `scribe.failure_code.F-SCRIBE-INELIGIBLE-ACTIVITY.v1` — one row per failure code in §7.13; parent §7 v1.1 + §4 v2.1 (Logician enforces each). v1.1 additions: `F-SCRIBE-TEMPLATE-DRIFT`, `F-SCRIBE-PARAPHRASED-NUMERIC`, `F-SCRIBE-DIALECT-INDUCED-IDENTITY`, `F-SCRIBE-CONVERSATION-ANCHOR-INVALID`.
- `scribe.pre_gate.kgie_pass.v1` (pre-gate-check) — §7.4 PASS predicate; parent §7 v1 + §4 v2.1.
- `scribe.post_gate.claim_evidence_grep.v1` (post-gate-check) — §7.13 `F-SCRIBE-UNSOURCED-CLAIM` enforcement; parent §7 v1 + §4 v2.1.
- `scribe.post_gate.ineligible_activity.v1` (post-gate-check) — §7.2 Law 2 Scribe-owned POST-gate enforcement; parent §7 v1.1 + §4 v2.1.
- `scribe.post_gate.numeric_verbatim.v1` (post-gate-check) — §7.6 numeric-verbatim invariant enforcement; parent §7 v1.1 + §4 v2.1.
- `scribe.test.corpus.v1` (test) — §7.14 golden drafts corpus; parent §7 v1.

Row count: approximately 35 rows. At §7 v1.1.1 LOCK 2026-04-21, all rows promote to `stability_tier = LOCKED` via §0.5 parent-backfill (§6 v1-r1 co-committed §0.5 v6 amendment per §6.17; §7 rows row-append as §0.5 v6 → v6.1 narrow amendment per the Option-B compound-txn discipline). Exact row count firms when §0.5 v6.1 sibling commit lands.

# §7.18 Open questions (for Thesis-round attention)

**OQ-7.1 — Scribe re-draft semantics on Editor findings.** v1 scope says revision-loop lives in §8 Editor + §10 Red Team. Where exactly does Scribe's re-draft entry point live? Same `vault_write` dispatcher handling as initial draft, or does re-draft need a distinct intent tag? Leaves a gap in §7.12 Handoff contract; §8 v1 must close.

**OQ-7.2 — Phase 0 RFA extractor module provenance.** v1 says extractor is operator-hand-populated at v0.1 and a module LOCK is v0.2 roadmap. Does Thesis round want to LOCK the extractor module spec now (blocking §7 on an extra module) or row-append at v0.2? Recommendation: defer to v0.2 — shape is pinned, provenance is orthogonal.

**OQ-7.3 — USER_DATA conversation-anchor schema.** CLOSED at v1.1 (§7.4a) + narrowed at v1.1.1 (hash prefix widened to [:32] = 128-bit collision resistance): shape pinned as `USER_DATA:<session_manifest_run_id>:<turn_ordinal>:<sha3_512(canonical_turn_bytes)[:32]>`; persistence to append-only Vault artifact `orgs/<slug>/conversations/<run_id>.log.jsonl` under §4.10 kind-class `conversation_log` gating. Implementation binding (conversation-log persistence primitive, read path from prompt-template compilation) **resolved at §6 v1-r1 LOCK 2026-04-21** — §6's prompt-template compilation pipeline now hosts the anchor-resolver read path.

**OQ-7.4 — Per-program-template dialect-default vs operator-override precedence.** §7.8 says operator override wins over funder-classification default. §7.9 ProgramTemplate carries `dialect_default`. What wins when both a program-template default AND a funder-classification default disagree, AND operator has not overridden? Recommendation: program-template default wins (more specific than funder-classification default), but Thesis round should validate.

**OQ-7.5 — Admin-risk register snapshot-age ceiling.** §7.16 pins snapshot age ≤ 24 hours. Is 24h correct? Too tight (forces snapshot-regen at every run), too loose (stale register risks missed flags)? Tie-break based on register-change-frequency evidence from v0.1 deployment data when available.

**OQ-7.6 — Section 12 (Equity / Community Benefits) OMIT vs empty-stub.** §7.5 says "OMITTED if not asked". Should the drafts manifest include a `SectionDraft(section_name="Equity", body_text=None, omit=True)` marker, or simply not emit the section at all? Clear favorite: explicit OMIT marker with reason (`rfa_did_not_request`) — surfaces the decision for operator review rather than letting it disappear.

**OQ-7.7 — Cross-family rigor binding at v0.1.** Per `/router.yaml` (source of truth, 2026-04-19 update): Scribe primary = Anthropic Claude (Sonnet 4.6 / Opus 4.6-4.7); Judge primary = Google Gemini 2.5 Pro. Editor primary = Meta (Llama 3.3 70B via Groq); Red Team primary = OpenAI-OSS (GPT-OSS-120B via Groq). What is the Editor (§8) cross-family binding constraint? Architecture §D.2 + §D.3 + §D.4 do not pin Editor cross-family — only Judge has the Section E invariant. Recommendation: Editor may share family with Scribe (Editor is clarity-focused, not scoring). §8 Editor blueprint round to validate.

# §7.19 Version history

- **v1 SCOPING DRAFT 2026-04-20.** First blueprint section for Scribe. Lifted from `skills/scribe-ghostwriter/SKILL.md` (operational today) + architecture §D.2 (locked 2026-04-19). Authored under operator directive "bang out that writing layer" + "address everything in the discussion to your best understanding and ability". Awaits Thesis-round audit + verification-round LOCK. Prerequisite interlock: §6 Operating Envelope v1 LOCK.
- **v1.1 Round-1-fixes 2026-04-21.** Thesis Round 1 verdicts (`pipeline/validation/section_07_thesis_round_1/`): Judge REQUIRES_MAJOR_MITIGATIONS 93/100 + 1 critical flag; Red Team REQUIRES_MAJOR_MITIGATIONS 4 HIGH + 2 MEDIUM; Editor NEEDS_REVISION 3 top fixes. Author fixes applied in single pass: (1) Judge CRITICAL `five_laws_cell_silently_delegated` — §7.2 Law 2 POST-gate promoted from delegation to Scribe-owned `F-SCRIBE-INELIGIBLE-ACTIVITY` with `eligible_activity_map` output-shape addition to `SectionDraft`; (2) Judge R-2 — §7.12 Judge binding updated to `google/gemini-2.5-pro` per router.yaml source of truth; (3) Judge R-3 — frontmatter `prerequisite_interlock` updated from "NOT YET AUTHORED" to "SCOPING DRAFT in progress"; (4) Red Team R-1 Law 5 dialect-induced identity — new POST-gate `F-SCRIBE-DIALECT-INDUCED-IDENTITY` + `scribe.dialect_identity_proxy_table.v1`; (5) Red Team R-2 paraphrase-evasion — new POST-gate `F-SCRIBE-PARAPHRASED-NUMERIC` + §7.6 numeric-verbatim invariant; (6) Red Team R-3 template-tamper — new PRE-gate `F-SCRIBE-TEMPLATE-DRIFT` + §7.9 hash-pin + v0.2 signed-commit migration commitment; (7) Red Team HIGH USER_DATA — §7.4a conversation-anchor schema pinned + new POST-gate `F-SCRIBE-CONVERSATION-ANCHOR-INVALID`; (8) Red Team MEDIUM middle-block dialect — §7.8 references `F-CONTEXT-MIDDLE-CONTRADICTION` (§6-forwarded); (9) Red Team MEDIUM register gap — §7.16 adds coverage-gap acknowledgment + v0.2 ≥ 50-entry floor; (10) Editor revisions — §7.5 terminology pin (goals/outputs/outcomes/objectives), §7.2 Law 1 three-site trace narrative, §7.13 failure-code deduplication review. Awaits Round 2 VERIFICATION dispatch.

- **v1.1.1 Round-2 narrow-fix carve-out 2026-04-21.** Thesis Round 2 VERIFICATION verdicts (`pipeline/validation/section_07_thesis_round_2/`): Editor READY_TO_LOCK (clean), Judge READY_TO_LOCK 100/100 (no residuals, all Round 1 closed), Red Team REQUIRES_MAJOR_MITIGATIONS literal but execution trace shows 4/6 residuals CLOSED + 2 genuine partials + remainder are architecturally inherent limits or explicit v0.2 deferrals. Narrow-fix carve-out applied per L-005 (same discipline as Vault Batch 2 gate_and_open closure — narrow author-fixes permitted within the two-audit boundary when verification trace localizes the remaining surface): (1) §7.4a conversation-anchor hash prefix widened [:16] → [:32] (64→128 bits collision resistance, closes Red Team S-10); (2) §7.4a adds Vault §4.10 kind-class `conversation_log` gating + v0.2 SIGNED-path migration commitment (closes Red Team S-11 same-uid fabricated-turn-append surface at v0.2, documents v0.1 interim control); (3) §7.9 adds explicit "Known residual threat surfaces" block naming pre-Phase-0 TOCTOU + loader-tampering as v0.1 assumed-out-of-scope + v0.2 signed-commit closure (closes Red Team S-7/S-8 at threat-model honesty level); (4) §7.2 Law 5 dialect-induced-identity POST-gate adds closed-set table curation commitment + v0.2 semantic-embedding supplement (closes Red Team S-2 at roadmap-honesty level). Red Team S-4 (12 months vs 1 year unit-normalization) is intentional design: unit normalization ALLOWS legitimate unit swaps — not a residual. Red Team S-12 (register 18-entry contents) is out of blueprint-LOCK scope per §7.16 (contents are operational, not blueprint-governed) — closed architecturally.

- **v1.1.1 LOCKED 2026-04-21.** §7.15 prerequisite satisfied by §6 Operating Envelope v1-r1 LOCK 2026-04-21 (compound transaction with §0.5 v6 amendment per §6.17). §7 v1.1.1 sealed same day under L-005 two-audit cycle: Round 1 DRIVER + v1.1 author-fixes + Round 2 VERIFICATION + v1.1.1 narrow-fix carve-out. Frontmatter, §7.15, §7.17, §7.18 OQ-7.3 updated to LOCKED status. All §7.17 interface-index rows promote to `stability_tier = LOCKED` via §0.5 narrow parent-backfill (v6 → v6.1 row-append follow-on). Runtime-live at LOCK. Artifacts: `pipeline/validation/section_07_thesis_round_1/`, `pipeline/validation/section_07_thesis_round_2/` (incl. CLOSEOUT.md). MEMORY: `project_impl_section_07_v1_thesis_rounds_1_2_closeout_2026-04-21.md`.

*End Section 7 — **LOCKED v1.1.1 2026-04-21**. §7.15 prerequisite satisfied by §6 v1-r1 LOCK same day. Runtime-live and load-bearing.*
