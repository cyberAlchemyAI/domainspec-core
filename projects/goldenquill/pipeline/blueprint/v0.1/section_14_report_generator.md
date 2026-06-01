---
title: Blueprint §14 Report Generator — funder-required reporting from operator-promoted commitments + operational data (v1 SCOPING DRAFT)
filed: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 (v1 SPEC — L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor per WS-D v7.0.5 + WS-E §11 + WS-F §12 + WS-H §2 v7.2 + WS-G §5 v8 + WS-K §15 + WS-C-M1 v7.0.4-M1 + WS-L §4 v2.x + WS-I §13 v1 precedents — Editor=Llama-3.3-70B/Groq READY_TO_LOCK + Judge=Gemini-2.5-Pro/Google READY_TO_LOCK 100/100 + Red Team=GPT-OSS-120B/Groq Cycle 2 with all 28 Cycle-1 findings CLOSED + 10 NEW probes RT-C2-01..RT-C2-10 FOLDED-IN at LOCK per row-170 transparent disposition pattern). **Cycle 1 outcomes:** Editor READY_TO_LOCK (8 stylistic findings — 0 HIGH + 3 MED + 5 LOW; deferred to v1.x readability spin); Judge READY_TO_LOCK 100/100 with zero findings (cite "exemplary"); Red Team ESCALATE blocking:true (28 findings — 4 P0 + 6 HIGH + 9 MED + 3 LOW). Cycle 1 closures applied across §14.5.0 + §14.5.1 + §14.6.4 + §14.6.5 + §14.9.0 + §14.9.1 + §14.9.2 + §14.9.4 + §14.9.5 + §14.12.1 + §14.13.4 + §14.16 + new §14.18 closure dispositions section. **Cycle 2 outcomes:** Editor READY_TO_LOCK (3 NEW stylistic findings E-NF-01..E-NF-03; PARTIAL/non-blocking; deferred to v1.x readability spin); Judge READY_TO_LOCK 100/100 with explicit dimension upgrades on cross-amendment composition + F-REPORT-* gate completeness + sub-section composition + operator approval + claim_evidence_map signing + cross-period reuse + test matrix; Red Team REQUIRES_FIXES blocking:true with all 28 Cycle-1 findings CLOSED + 10 NEW probes RT-C2-01..RT-C2-10 (1 P0 + 3 HIGH + 5 MED + 1 LOW) — all FOLDED-IN at LOCK per row-170 transparent disposition pattern (mirrors §13 v1 / WS-C-M1 v7.0.4-M1 / WS-B v7.0.7 / WS-D v7.0.5 / WS-K §15 / WS-I §13 row-170 precedents). **NINTH substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor (after WS-D v7.0.5 row 179 + WS-B v7.0.7 row 180 + WS-C-M1 v7.0.4-M1 row 190 + WS-F §12 v1 rows 182-184 + WS-E §11 v1 row 185 + WS-H §2 v7.2 rows 186/187 + WS-G §5 v8 rows 188/189 + WS-K §15 v1 rows 191/192 + WS-L §4 v2.x rows 193/194 + WS-I §13 v1 rows 196/197 architecture/blueprint-class precedents).** Compound LOCK with `section_00_5_section_14_report_generator_amendment.md` per §6.17 Option-B paired-commit pattern; §4 v2.x §5.1 HORIZON F-REPORT-* family ACTIVATES at this LOCK (5 codes + new sub-tags from Cycle 1+2 fold-ins; HORIZON rows registered at row 193 LOCK time, predicate bodies skeleton-stubs at v0.2 first ship; Code phase realizes substrate per WS-J Code follow-on dispatch).
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                      # v7 LOCKED 2026-04-19 — A1-A12
  - pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md                  # v7.0.4 LOCKED 2026-05-09 row 178 — KFR + SP0 + F-LOGICIAN-FACT-DRIFT family + Benchmarks Register; Report Generator reads KFR canonical + cross-validates draft numeric claims via F-REPORT-NUMERIC-DRIFT (inherits Decimal mandate from v7.0.4-M1)
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md               # v7.0.4-M1 LOCKED 2026-05-10 row 190 — corrective; KFR canonical-JSON signing + Decimal mandate + atomic-read fcntl.flock + symlink rejection. F-REPORT-NUMERIC-DRIFT comparison MUST use Decimal exactly; any float-comparison code path is a defect (cross-family Red Team probe MUST cover float-introduced numeric drift as adversarial scenario)
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md                  # v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intelligence DB + Match DB; Report Generator reads `vault_shared/funder_intelligence/<funder_id>/reporting_format_precedents.yaml` for funder-specific reporting context + per-funder published reporting rubric (when present). Stage-5 cooperative on-ramp does NOT engage in v0.2 — workspace-shared reads are read-only; nothing phones home
  - pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md                  # v7.0.6 SELF-LOCKED 2026-05-09 row 176 — Report Generator named as v0.2 horizon support agent; track-binding inside §5 v8 report_mode (NOT a brand-new agent slot in the seat roster)
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                  # v7.0.7 LOCKED 2026-05-10 row 180 — Beta classification-driven routing; Report Generator inherits the same per-call routing decision pattern as Scribe/Editor/Judge/Red Team. Scribe authors sub-section templates as Public+Shareable with opaque [SLOT_<numeric_id>] tokens for Confidential per-org values; slot-fill agent (always-local) renders Confidential into post-fill drafts after Scribe returns; Editor + Red Team read post-fill drafts → always-local routing; Judge reads post-fill drafts → routine-Judge always-local with on-demand heavy-Judge swap available for high-stakes reports per v7.0.7 §4.2
  - pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md                  # v7.0.8 LOCKED — CIC × CLC orthogonality; Report Generator's per-sub-section prompt templates + proposal_commitments rubric audited against F-CIC-CLC-COUPLING-VIOLATION at LOCK (4 detection layers: lexical regex / Pydantic AST / value-set / KP schema). report_mode rubric (proposal_commitments-based) cannot encode CIC→CLC subset binding; opportunity-driven runtime matching per v7.0.8
  - pipeline/blueprint/v0.1/section_02_vault_topology.md                         # §2 v7.2 LOCKED 2026-05-10 rows 186/187 — operational-data sub-kinds (metrics + financials + photos + narrative_entries + timeline_of_activities + beneficiary_records + attachments). Report Generator READS the seven SIMPLE sub-kinds Data Collector wrote at `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/<sub_kind>/`. Cedar PII enforcement on `beneficiary_records` is Cedar-Python at the read path (F-CEDAR-OPERATIONAL-DENIED + F-CEDAR-PII-CONSENT-MISSING fire at the read path, not just the write path)
  - pipeline/blueprint/v0.1/section_04_logician.md                               # §4 v2.x LOCKED 2026-05-10 row 193 — Report Generator gate family registered at §5.1 HORIZON; this §14 v1 LOCK ACTIVATES the five F-REPORT-* HORIZON rows into live PRE/POST positions. Predicate bodies are skeleton stubs raising NotImplementedError at v0.2 first ship; Code-phase realization via WS-J Code follow-on dispatch
  - pipeline/blueprint/v0.1/section_05_pipeline.md                               # §5 v8 LOCKED 2026-05-10 rows 188/189 — track-registry; report_mode is the FORWARD-COMPAT row registered with `shippable_in: v0.2`. THIS §14 v1 LOCK is the event that flips the report row from FORWARD-COMPAT-refused-at-runtime to ACTIVE-and-runtime-reachable. The §5 v8 dispatcher at §4.16 dispatcher-contract clauses 1-7 + the §7.16-§7.21 invariants are the binding shape report_mode binds against — NOT a re-architecture per WS-J. The data-driven track registry's R.PF1 commitment ("adding a new track requires only a router.yaml row + new prompt templates") is honored: this LOCK appends NO new §3 module per track, NO new §4.N mechanism per track, ONLY a new pipeline_shape runner binding (`prior_commitments_to_council_to_signed_report`) + the per-sub-section prompt templates + the proposal-commitments rubric + the per-sub-section red-team probes
  - pipeline/blueprint/v0.1/section_06_operating_envelope.md                     # §6 v1-r1 LOCKED 2026-04-21 — track-registry host schema at §6.7; report_mode row inhabits the schema published there. F-PIPELINE-TRACK-FROZEN audit (architecture-side, dormant per v7 §R.PF1) re-fires at this LOCK against the §5 v8 LOCKED text + the runner files; v8 audit was PASS at LOCK time and §14's flip from FORWARD-COMPAT to ACTIVE preserves the audit outcome (no new track-by-name literal in `pipeline/loop/run_*.py`; the addition is via §5 v8 §4.16 dispatcher's DI seam — `_V0_1_IMPLEMENTED_SHAPES` extends from 2 entries to 3, new shape `prior_commitments_to_council_to_signed_report` admitted, new runner argument `report_runner` added to `dispatch_track`)
  - pipeline/blueprint/v0.1/section_07_scribe.md                                 # §7 v1.1.1 LOCKED 2026-04-21 — Scribe's drafting discipline (KGIE preflight + SMART outcomes + funder-dialect code-switching); report_mode extends Scribe's per-section draft pattern to per-sub-section report drafts with claim_evidence_map authoring as an integrated discipline (NOT a separate seat)
  - pipeline/blueprint/v0.1/section_10_red_team.md                               # §10 v1 LOCKED 2026-05-02 — Red Team's adversarial discipline + cross-family rigor; report_mode extends Red Team's per-section probe pattern to per-sub-section report probes that include Boundary-Drift + Numeric-Drift + Commitment-Missed pathways
  - pipeline/blueprint/v0.1/section_11_intake.md                                 # §11 v1 LOCKED 2026-05-10 row 185 — Intake AWARD_INGEST produces `proposal_commitments.yaml`. Report Generator READS `status: PROMOTED` proposal_commitments to source the per-period commitment-vs-actuals rubric. PENDING_OPERATOR_REVIEW commitment files are NOT consumed (mirrors §13's discipline). Content-hash binding via `submission_artifact_content_sha3_512` per §11 v1 RT-05 closure
  - pipeline/blueprint/v0.1/section_12_uploader.md                               # §12 v1 LOCKED 2026-05-10 rows 182-184 — operator-clicks-final-submit discipline; Report Generator's claim-evidence-map signing + draft signing mirrors §12's prepare-and-stage discipline (Report Generator drafts; operator approves; Uploader stages for funder-portal submission via §12.10 adapters). Report Generator does NOT submit to funder portals (Uploader §12 owns that surface)
  - pipeline/blueprint/v0.1/section_13_data_collector.md                         # §13 v1 LOCKED 2026-05-10 rows 196/197 — Data Collector writes inbound responses into the seven SIMPLE operational-data sub-kinds Report Generator reads. Cedar PII enforcement on beneficiary_records is enforced at Data Collector's WRITE path; Report Generator inherits the consent-tier discipline at READ path. F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER (POST write) composes with Report Generator's read-path Cedar enforcement
  - pipeline/blueprint/v0.1/section_15_archivist.md                              # §15 v1 SPEC LOCKED 2026-05-10 rows 191/192 — cross-org leak gate-family precedent (F-ARCHIVIST-CROSS-ORG-LEAK + F-ARCHIVIST-LESSON-INSTANCE-LEAK + F-ARCHIVIST-AUTO-APPLY-ATTEMPTED + F-ARCHIVIST-CADENCE-DRIFT + F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT). §14's F-REPORT-OUT-OF-SCOPE-DRIFT mirrors §15's three-layer-detection shape (AST-lint + runtime-guard + Cedar policy) for "claims exceeding original-proposal scope" boundary-drift detection
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_1_amendment.md          # §4 v2.x.1 narrow-corrective LOCKED 2026-05-10 + §0.5 v16 paired (rows 377-378); referenced for §0.5 row-numbering continuity
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md               # §0.5 v5 LOCKED + amendments v6-v16 (runtime-live 376 rows at 2026-05-10T23:30Z); Report Generator primitives row-append at paired §0.5 §14 amendment companion-file claiming rows 379-395 (target 17 rows: 1 marker + 6 schema + 5 failure-code + 3 pre-gate-check + 2 post-gate-check; final count + range resolved at LOCK)
prerequisite_interlock: pipeline/blueprint/v0.1/section_04_v2_x_amendment.md §5.1 (Report Generator family HORIZON registration — five gates registered as HORIZON rows in §4 v2.x at row 193 LOCK time; this §14 v1 LOCK is the activation event that flips HORIZON → live PRE/POST positions; §4 v2.x LOCKED row 193 is the prerequisite parent). §13 v1 LOCKED row 196 is also a hard prerequisite — Data Collector's operational-data sub-kind writes are the read-substrate Report Generator consumes; without §13 LOCKED, the read path schemas (operational-data sub-kinds metrics / financials / photos / narrative_entries / timeline_of_activities / beneficiary_records / attachments) are not yet stable. §11 v1 LOCKED row 185 is the second hard prerequisite — proposal_commitments.yaml schema with PROMOTED-status filtering + content-hash binding via submission_artifact_content_sha3_512 is the rubric input contract.
companion_module: pipeline/orchestrator/tracks/report_mode.py + pipeline/orchestrator/seats/report_generator/__init__.py — track-dispatch entry point + sub-section composer module skeletons (scaffold authored at §14 v1 LOCK with proposes-only AST-lint assertions on auto-finalize; full per-sub-section composition + claim-evidence-map signer implementation deferred to WS-J Code phase follow-on dispatch).
companion_amendment: pipeline/blueprint/v0.1/section_00_5_section_14_report_generator_amendment.md (paired-commit at §14 v1 LOCK per §6.17 Option-B).
v0_2_implementation_disposition: SPEC + skeleton at v0.2 first ship. The track-mode entry point (pipeline/orchestrator/tracks/report_mode.py) ships as a skeleton that registers the runner via §5 v8 dispatcher's DI seam (extends `_V0_1_IMPLEMENTED_SHAPES` to admit `prior_commitments_to_council_to_signed_report`; adds `report_runner` argument to `dispatch_track`); per-sub-section composers (narrative / metrics_table / financial_summary / photo_gallery / beneficiary_section) ship as skeleton stubs that import the council-seat protocol + emit `NotImplementedError` at substrate-level composition; full sub-section composition + claim-evidence-map signer wiring lands in WS-J Code phase dispatch after §14 v1 LOCK. The proposal-commitments rubric (`pipeline/rubrics/proposal_commitments_rubric.json`) ships as a v0.2 first-wave Code work paired with this LOCK; five F-REPORT-* gate predicates from §4 v2.x §5.1 HORIZON flip to live PRE/POST positions at this LOCK with predicate bodies as skeleton stubs raising `NotImplementedError` at v0.2 with the Cedar policy + check-callable shape spec'd herein (mirrors §13 v1 + §15 v1 spec-only-with-skeleton-stubs disposition).
downstream_siblings_out_of_scope: All v0.2 horizon seat-spec sections now LOCKED (§11 v1 / §12 v1 / §13 v1 / §14 THIS / §15 v1 SPEC). v1.x horizon: Archivist v1.x implementation amendment (per §15 v1 SPEC LOCK frontmatter); v0.2 production cut checklist items finalize when WS-N integration testing completes.
ws_l_routing_dependency: WS-L §4 Logician v2.x LOCKED 2026-05-10 row 193. The five F-REPORT-* gates registered at §4 v2.x §5.1 HORIZON activate at this §14 v1 LOCK via the paired-commit pattern. Gate predicate bodies are spec'd in this §14 (substrate-dispatched per sub-section where applicable; consolidated PRE-pre-track-dispatch check callable per §4 v2.2 pattern); Code-side realization lands in WS-J Code phase dispatch follow-on. F-REPORT-* family is the FOURTH dormant family activating from v2.x HORIZON (after F-DATACOLLECTOR-* activated at §13 LOCK row 196).
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent (lock_history row 179, 2026-05-10) + WS-E §11 + WS-F §12 + WS-H §2 v7.2 + WS-G §5 v8 + WS-K §15 + WS-C-M1 v7.0.4-M1 + WS-L §4 v2.x + WS-I §13 v1 (rows 185 / 182 / 186 / 188 / 191 / 190 / 193 / 196). Editor=groq/llama-3.3-70b-versatile (Meta family) + Judge=google/gemini-2.5-pro (Google family) + Red Team=groq/openai/gpt-oss-120b (OpenAI-OSS family) dispatched via openclaw infer model run --gateway across both Cycle 1 and Cycle 2. Three distinct non-Anthropic families. L-003 satisfied. Bridge pattern: Cowork → openclaw via mcp__Control_your_Mac__osascript with timeout of 600 seconds for Gemini Pro thinking-mode runs. Dispatch shell scripts cribbed from pipeline/validation/blueprint_section_13_data_collector_2026-05-10/dispatch_audit_v{1,2}.sh. Audit trail at pipeline/validation/blueprint_section_14_report_generator_2026-05-10/. **Red Team pass is load-bearing** — funder-required reporting carries Law 1 (RFA-is-truth: every claim traces) + Law 2 (No-boundary-drift: claims stay inside original proposal scope) + Law 5 (Applicant-brings-substance: numeric claims trace to KFR or operational data, never fabricated). Adversarial probe MUST cover (a) untraced claim slipping past F-REPORT-COMMITMENT-UNTRACED via false-positive evidence map, (b) commitment-row-PROMOTED-but-not-addressed via Judge cross-check vs Red Team independent traversal, (c) numeric drift via float comparison instead of Decimal (v7.0.4-M1 mandate violation), (d) out-of-scope drift via cross-period claim reuse without re-prove from period-(N-1) operational data, (e) template-mismatch via reporting_template.yaml schema drift between the funder's actual template and the on-disk template Tilth carries.
---

# §14.0 Cross-amendment composition map

```
v7 LOCKED 2026-04-19 (A1-A12)
  ├─ v7.0.4 LOCKED 2026-05-09 row 178 + v7.0.4-M1 row 190 — KFR + SP0 + F-LOGICIAN-FACT-DRIFT family + Decimal mandate
  │    │
  │    └─→ §14 Report Generator (THIS) — track-binding inside §5 v8 report_mode + per-sub-section composers + claim-evidence-map signer + 5 F-REPORT-* gates activating from §4 v2.x §5.1 HORIZON
  │
  ├─ v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intel DB; Report Generator reads funder-specific reporting context + per-funder published reporting rubric
  ├─ v7.0.6 SELF-LOCKED 2026-05-09 row 176 — Report Generator named v0.2 horizon support agent
  ├─ v7.0.7 LOCKED 2026-05-10 row 180 — classification routing; §14.10 routing posture inherits Scribe/Editor/Judge/Red Team posture under report_mode (Scribe Public+Shareable with opaque slot tokens; slot-fill local; Editor/Red Team/Judge post-fill local)
  └─ v7.0.8 LOCKED — CIC × CLC orthogonality; §14 sub-section templates + proposal-commitments rubric audit clean at LOCK against the four detection layers

§14 → companion edits at LOCK (compound paired-commit per §6.17 Option-B):
  ├─ §0.5 §14 amendment (~17 rows; range 379-395; +1 marker + 6 schema rows + 5 failure-code rows + 3 pre-gate-check + 2 post-gate-check)
  ├─ §4 v2.x amendment ACTIVATES F-REPORT-* family from §5.1 HORIZON to live PRE/POST positions (5 codes; Code session per WS-J Code phase realizes predicate bodies)
  ├─ router.yaml report row UPDATE: keeps `shippable_in: v0.2` BUT now satisfies the dispatcher's runtime gate because v0.2 first-ship Tilths set `TILTH_VERSION_FAMILY = "v0.2"` (per §5 v8 §8 constant) — the report row becomes runtime-reachable on v0.2-deployed Tilths automatically when v0.2 ships (NOT a config-flag-flip; a Tilth-version-family bump owned by SN-LLC release pinning)
  ├─ pipeline/orchestrator/tracks/report_mode.py module skeleton (track-dispatch entry point + DI seam extension to §5 v8 dispatcher; AST-lint R-REPORT-NO-AUTO-FINALIZE rejects any module that finalizes a report without operator approval)
  ├─ pipeline/orchestrator/seats/report_generator/__init__.py + sub-section composer skeletons (5 sub-section modules: narrative / metrics_table / financial_summary / photo_gallery / beneficiary_section; each emits NotImplementedError at substrate-level composition)
  ├─ skills/scribe-ghostwriter/report_mode_prompts/ (5 sub-section prompt templates)
  ├─ skills/judge-rubric/proposal_commitments_rubric.json (Judge's report_mode rubric, extracted from proposal_commitments.yaml schema; per-commitment-row evaluation criteria)
  ├─ skills/red-team/report_mode_probes/ (5 sub-section adversarial probe templates)
  ├─ orgs/_TEMPLATE/vault/grants/<grant_id>/reports/.gitkeep + reporting_template.yaml.example
  ├─ tests/tracks/report_mode/skeleton_tests.py (NON-NEGOTIABLE: prevents future contributors from quietly enabling auto-finalize)
  └─ pipeline/validation/blueprint_section_14_report_generator_2026-05-10/ (audit trail directory)
```

**Per-substrate contract reference.** Report Generator's read-only access to upstream substrates is bounded by each substrate's LOCKED contract:

- **KFR canonical** — read-substrate per v7.0.4 §1 + v7.0.4-M1 §2; Report Generator reads `orgs/<slug>/vault/kfr/register.yaml` via `vault_read_intent_kfr` to cross-validate numeric claims in draft sub-sections (F-REPORT-NUMERIC-DRIFT POST). Cross-check semantics: read-only; never mutates KFR. Decimal comparison per v7.0.4-M1 §2 mandate; ANY float-comparison code path is a defect.
- **Proposal commitments** — per-org-per-grant read-substrate per v7.0.4 §5.3 + §11 v1 §11.5.2; Report Generator reads `orgs/<slug>/vault/grants/<grant_id>/proposal_commitments.yaml` with `status: PROMOTED` to source the rubric input contract. PENDING_OPERATOR_REVIEW files are NOT consumed (mirrors §13 v1 discipline). Content-hash binding: `submission_artifact_content_sha3_512` per §11 v1 RT-05 closure.
- **Operational data sub-kinds** — per-org-per-grant-per-period read-substrate per §2 v7.2 §7; Report Generator reads `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/<sub_kind>/` for the seven SIMPLE sub-kinds (metrics + financials + photos + narrative_entries + timeline_of_activities + beneficiary_records + attachments). Cedar PII enforcement on beneficiary_records is Cedar-Python at the read path: F-CEDAR-OPERATIONAL-DENIED + F-CEDAR-PII-CONSENT-MISSING fire at Report Generator's read path, not just Data Collector's write path. Beneficiary-records consent_tier enum from §13 v1 RT-C2-10 closure binds: Report Generator's beneficiary_section composer MUST consult the consent_tier of each beneficiary record before incorporating it into draft text; consent_tier "narrative-text-only" is the floor for text inclusion (other tiers — "metrics-only" / "no-narrative" — gate text inclusion at the composer layer with reason-to-operator surfaced via F-REPORT-OUT-OF-SCOPE-DRIFT.beneficiary_consent_tier_violation sub-tag).
- **Funder Intelligence DB** — workspace-shared read-substrate per v7.0.5 §1; Report Generator reads `vault_shared/funder_intelligence/<funder_id>/reporting_format_precedents.yaml` for funder-specific reporting context AND `vault_shared/funder_intelligence/<funder_id>/published_reporting_rubric.yaml` (when the funder publishes their own scoring rubric for grantee reports). F-FUNDER-CORPUS-INTEGRITY per v7.0.5 §5.6 verification fires PRE-load.
- **Reporting template** — per-org-per-grant read-substrate; Report Generator reads `orgs/<slug>/vault/grants/<grant_id>/reporting_template.yaml` (funder-required reporting format the operator captured at award acceptance). F-REPORT-TEMPLATE-MISMATCH PRE-pre-track-dispatch fail-closes if the on-disk template has drifted from the funder's actual template (see §14.9.5 for the per-funder published-template comparison).
- **Benchmarks Register** — workspace-shared read-substrate per v7.0.4 §6; Report Generator reads `vault_shared/benchmarks/<sector>/` to provide narrative context for metrics_table sub-section variance (e.g., "the project achieved 23% above sector benchmark X"). Read-only; never mutates the register.
- **Reports output substrate** — per-org-per-grant-per-period write-substrate (Report Generator OWNS this substrate); `orgs/<slug>/vault/grants/<grant_id>/reports/period_<n>/draft_<v>.md` + `claim_evidence_map.yaml` (Ed25519-signed by operator at finalization); Cedar-policy-gated atomic write; audit-logged.

Each per-substrate read is wrapped by the appropriate Vault read intent. Bypassing the read intent (raw `open()` against any of the above substrates) is forbidden by AST-lint extension `R-REPORT-VAULT-INTENT-REQUIRED` (mirrors §15 v1 §15.9.5 RT-11 closure precedent + §13 v1 RT-11 precedent).

# §14.1 Purpose and scope

## §14.1.0 What ships at v0.2 first ship

**Five sub-sections at v0.2 first ship** (per dispatch decision 8i monolithic-track-with-sub-section-templates default): narrative + metrics_table + financial_summary + photo_gallery + beneficiary_section. Each sub-section is a per-sub-section prompt template under `skills/scribe-ghostwriter/report_mode_prompts/` + a per-sub-section composer module skeleton under `pipeline/orchestrator/seats/report_generator/`. The five sub-sections compose into a single `draft_<v>.md` per period; sub-section ordering and inclusion are operator-tunable per-grant via `reporting_template.yaml` (the funder's required ordering wins; some funders require all five, some require only narrative + metrics_table).

**Pull-fresh-from-KFR-and-operational-data discipline at v0.2** (per dispatch decision 8j default): Scribe receives KFR + proposal_commitments + operational-data + reporting_template as fresh inputs each report cycle. Prior period drafts are NOT loaded as Scribe context. Trend narrative (e.g., "growing X% over the previous quarter") surfaces only on operator approval — operator-gear: **Sparring Partner posture for trend authoring**, NOT Co-Pilot default. Surfaced at Audit #1 OQ-REPORT-TREND-GEAR for operator confirmation since this deviates from the default-Co-Pilot gear pattern.

**Operator approves the per-period draft + signs the claim_evidence_map; Uploader stages the operator-signed draft for funder-portal submission.** Mirror of §12 Uploader's operator-clicks-final-submit discipline applied to report finalization. No auto-finalize code path exists; AST-lint `R-REPORT-NO-AUTO-FINALIZE` rejects any module that signs a claim_evidence_map from a code path other than the operator-approval dispatcher.

**Per-claim evidence-trace discipline.** Every numeric, narrative, photo-reference, and beneficiary-record-reference claim in `draft_<v>.md` MUST trace to a source row in operational-data OR proposal_commitments OR KFR OR Benchmarks Register. The trace lives in `claim_evidence_map.yaml` (per-claim → per-source-row pointer with stable ID + content hash). F-REPORT-COMMITMENT-UNTRACED PRE-pre-finalize fail-closes any draft where a claim has no entry in the map.

## §14.1.1 Purpose

Report Generator is the **per-period funder-required reporting** support agent of the Tilth pipeline. During an active grant's reporting period (e.g., quarterly progress report; annual narrative + financial report; mid-grant evaluation report), Report Generator:

1. Reads the active grant's `proposal_commitments.yaml` (Intake AWARD_INGEST PROMOTED output per §11 v1) to source the rubric input contract — the per-commitment-row evaluation criteria the funder will use to assess this period's work.
2. Reads `reporting_template.yaml` (funder-required reporting format the operator captured at award acceptance) to bound the per-period draft against the funder's required structure (which sub-sections; which fields per sub-section; which length / format constraints).
3. Reads `orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/` (Data Collector's seven SIMPLE operational-data sub-kinds) to source the actuals against which the per-commitment evaluation runs.
4. Reads KFR canonical to cross-validate numeric claims (F-REPORT-NUMERIC-DRIFT advisory POST; Decimal comparison per v7.0.4-M1).
5. Reads Funder Intelligence DB for funder-specific reporting context + funder's published reporting rubric (when present).
6. Reads Benchmarks Register for sector-relative variance context (informational, narrative-only).
7. Composes per-sub-section drafts via the §5 v8 report_mode track running the same six council seats (Scout — informational only, no discovery in report_mode; Scribe / Editor / Judge / Red Team / Logician) on per-sub-section prompt templates with the proposal-commitments rubric in place of the funder-grant rubric.
8. Authors claim_evidence_map.yaml in lockstep with draft authoring (Scribe writes both; KGIE preflight extended to claim_evidence_map authoring).
9. Stages the per-period draft + claim_evidence_map for operator approval; operator signs the map; system finalizes the draft + writes the report bundle.
10. Does NOT submit to funder portals (Uploader §12 owns that surface).

**Report Generator proposes (drafts); operator confirms each per-period draft + signs the evidence map; Uploader stages the operator-signed bundle.** The operator-clicks-final-submit pattern from §12 Uploader transfers to report finalization: Report Generator authors the draft + claim_evidence_map + stages the bundle; operator reviews per-claim evidence trace + per-commitment fulfillment summary + classification routing summary + Cedar policy compliance summary; operator signs the claim_evidence_map; system finalizes the draft. The Uploader dispatch (separate operator-driven action per §12 v1) stages the finalized bundle for funder-portal submission.

**v0.2 first-ship scope is SPEC + skeleton + 5 prompt templates + rubric.** Per the `v0_2_implementation_disposition` frontmatter, this §14 v1 LOCK ships the spec text + module skeletons + 5 sub-section prompt templates + proposal-commitments rubric + 5 sub-section red-team probe templates + AST-lint assertions + skeleton tests. Per-sub-section substrate wiring (Scribe per-sub-section composer functions; claim_evidence_map signer; Cedar policy enforcement at read path) lands in WS-J Code phase dispatch after §14 v1 LOCK. The five F-REPORT-* gates from §4 v2.x §5.1 HORIZON flip to live PRE/POST positions at this LOCK; predicate bodies ship as skeleton stubs raising `NotImplementedError` at v0.2 with the Cedar policy + check-callable shape spec'd herein (mirrors §13 v1 + §15 v1 spec-only-with-skeleton-stubs disposition).

**Out of scope for v0.2 (explicit non-goals).** Report Generator does NOT auto-finalize draft absent operator-signed claim_evidence_map (F-REPORT-COMMITMENT-UNTRACED + R-REPORT-NO-AUTO-FINALIZE AST-lint). Report Generator does NOT write KFR canonical entries (Intake §11 owns KFR; Report Generator reads only). Report Generator does NOT mutate `proposal_commitments.yaml` (read-only). Report Generator does NOT mutate operational-data sub-kinds (Data Collector §13 owns the write path; Report Generator reads only). Report Generator does NOT generate proposal text (Scribe §7 in submission_mode). Report Generator does NOT submit to funder portals (Uploader §12). Report Generator does NOT discover new opportunities (Scout). Report Generator does NOT cross orgs (per F-REPORT-CROSS-ORG-LEAK structural enforcement, composing with §15 v1 + §13 v1 cross-org leak gate-family precedents). Report Generator does NOT bundle multi-period drafts at v0.2 first ship (per §14.12.3 default — separate drafts per period, operator-bundled at submission via §12 Uploader if funder requires).

**Substance comes from operational-data + proposal_commitments + KFR (Laws 1 + 5).** Every claim in `draft_<v>.md` carries a per-claim entry in `claim_evidence_map.yaml` that points to the source row by stable ID + content hash. The operator-approval step is the load-bearing transition from drafted text to canonical report — Report Generator never silently finalizes a draft without operator sign-off on the evidence map. F-REPORT-COMMITMENT-UNTRACED enforces structurally.

## §14.1.2 Boundary with Scribe submission_mode (track-binding, NOT a new agent)

**Report Generator is a TRACK in §5 v8 (NOT a brand-new agent).** The same six council seats (Scout — informational only in report_mode; Scribe / Editor / Judge / Red Team / Logician) run on `report_mode` track with different prompt templates and the original-proposal-commitments rubric in place of the funder-grant rubric. The §5 v8 dispatcher (§4.16 dispatcher contract clauses 1-7 + §7.16-§7.21 invariants) is the binding shape; report_mode binds against it via:

| Dimension | submission_mode | report_mode |
|---|---|---|
| Track row in §5 v8 | `submission` (ACTIVE; shippable_in v0.1) | `report` (FORWARD-COMPAT at §5 v8 LOCK; ACTIVE at THIS §14 v1 LOCK on v0.2 Tilths) |
| Pipeline shape | `rfa_to_council_to_signed_bundle` | `prior_commitments_to_council_to_signed_report` |
| Scribe prompt template root | `pipeline/prompts/submission/scribe.md` | `skills/scribe-ghostwriter/report_mode_prompts/{narrative,metrics_table,financial_summary,photo_gallery,beneficiary_section}.md` |
| Judge rubric ref | `pipeline/rubrics/vapg_fy26.json` (or per-grant funder rubric) | `skills/judge-rubric/proposal_commitments_rubric.json` (per-grant `proposal_commitments.yaml` is the input contract) |
| Red Team probe template | `pipeline/prompts/submission/red_team_probe.md` | `skills/red-team/report_mode_probes/{narrative,metrics_table,financial_summary,photo_gallery,beneficiary_section}.md` |
| Output vault subtree | `orgs/{org_slug}/vault/submissions/{run_id}/` | `orgs/{org_slug}/vault/grants/{grant_id}/reports/period_{n}/` |
| Output schema | `SubmissionBundle` | `GrantReportBundle` (NEW; see §14.5) |
| Failure-code prefix | `F-PIPE-SUBMIT-` | `F-PIPE-REPORT-` (registered at §5 v8 row 188) + F-REPORT-* (registered at §4 v2.x §5.1 HORIZON; ACTIVATED at THIS LOCK) |
| Cross-family rigor | required | required |
| Operator approval surface | operator clicks final submit (§12 Uploader) | operator signs claim_evidence_map (THIS §14) → operator clicks final submit (§12 Uploader) |

**Same orchestration; different prompts + rubric + output schema + gate family.** R.PF1's commitment is honored: this LOCK appends NO new §3 module per track, NO new §4.N mechanism per track, ONLY a new pipeline_shape runner binding (`prior_commitments_to_council_to_signed_report`) + the per-sub-section prompt templates + the proposal-commitments rubric + the per-sub-section red-team probes + the F-REPORT-* gate family.

**Why share the orchestration at all?** Two reasons. First, the per-seat protocol (Scribe drafts → Editor reviews → Judge scores → Red Team probes → Logician gates) is identical between submission_mode and report_mode at the dispatcher layer; differentiating per-track at the orchestration level would duplicate §5 v8 §4.16 dispatcher logic. Second, the council-seat cross-family rigor discipline (Editor + Judge + Red Team in distinct families per L-003) carries over without modification — the same discipline that audits a submission proposal audits a per-period report. The track-binding at §5 v8 is the structural enforcement of "same orchestration, different track-specific bindings."

# §14.2 Five Operating Laws — enforcement mapping

Framework: per `pipeline/templates/component_analysis_template.md`

| Law | §14 enforcement |
|---|---|
| **Law 1 (RFA Is Truth)** | Every claim in `draft_<v>.md` traces to a source row (operational-data OR proposal_commitments OR KFR OR Benchmarks). F-REPORT-COMMITMENT-UNTRACED PRE-pre-finalize fail-closes if any claim has no entry in `claim_evidence_map.yaml`. proposal_commitments.yaml `status: PROMOTED` is the operator-promoted canonical source for what was promised; report-side claims reference these promotions by stable ID. |
| **Law 2 (No Boundary Drift)** | F-REPORT-OUT-OF-SCOPE-DRIFT POST fail-closes if any claim in `draft_<v>.md` exceeds the original proposal's defined scope. Three-layer detection (mirrors §15 v1 F-ARCHIVIST-AUTO-APPLY-ATTEMPTED + §13 v1 F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND): AST-lint (R-REPORT-NO-OUT-OF-SCOPE-CLAIM at compile time on prompt templates) + runtime check (claim → proposal_commitments PROMOTED scope match) + Cedar policy (`report_out_of_scope.cedar` denies write where claim's project-scope-tag is not in the proposal's project-scope-tag set). |
| **Law 3 (Org Isolation)** | Report Generator operates on exactly one `orgs/<slug>/` subtree per invocation. F-REPORT-CROSS-ORG-LEAK (composed under F-REPORT-OUT-OF-SCOPE-DRIFT.cross_org sub-tag) enforces structurally. Per-org Cedar enforcement on operational-data sub-kind reads. Workspace-shared substrate reads (Funder Intel DB / Benchmarks) are read-only and metadata-tagged-as-shared (no per-org content leak from a workspace-shared read). |
| **Law 4 (Apolitical / Admin-Risk)** | Report Generator inherits the admin-risk register from §4 Logician. Sub-section prompt templates pre-screen against the admin-risk register at draft time; flagged terms surface to operator with applicant-decides discipline (never silently rewrite). report_mode admin-risk surface is identical to submission_mode (same Logician PRE/POST gates fire on the report draft). |
| **Law 5 (Applicant Brings Substance)** | Numeric claims trace to KFR or operational-data via `claim_evidence_map.yaml`. F-REPORT-NUMERIC-DRIFT POST fail-closes if a numeric claim differs from KFR-derived expected value beyond per-field tolerance. Decimal comparison per v7.0.4-M1 mandate. Photo references trace to operational-data photos sub-kind by `photo_id` + content hash. Narrative claims trace to operational-data narrative_entries by `entry_id`. Beneficiary references trace to operational-data beneficiary_records by `beneficiary_id` + consent_tier check. |

# §14.3 Four Autonomy Rules — enforcement mapping

| Rule | §14 enforcement |
|---|---|
| **Rule 1 (Save State Always)** | `report_state.yaml` writes on BOTH success (with `cycle_completed=True` + draft_path + map_path + signature_path) AND failure (with `cycle_completed=False` + failure_reason + sub_tag). Mirrors §11 v1 + §13 v1 state-write discipline. |
| **Rule 2 (Test Your Own Work)** | Per-sub-section composer validates output before passing to Editor. KGIE preflight runs on every Scribe sub-section draft. Judge validates that proposal_commitments rubric scoring is complete (every PROMOTED commitment row scored). Red Team validates that adversarial probes covered every sub-section. Logician validates that every claim in draft has a corresponding entry in claim_evidence_map. |
| **Rule 3 (Be Explicit)** | Every task between seats includes input file path (proposal_commitments.yaml + reporting_template.yaml + operational-data sub-kind paths + KFR + Funder Intel DB), output file path (draft_<v>.md + claim_evidence_map.yaml + scoring/), exact scope (which sub-sections; which period_n), done definition (claim_evidence_map signed by operator). |
| **Rule 4 (Clean Output)** | `draft_<v>.md` is Markdown with no LLM self-commentary, no markdown-fence-around-structured-data, no conversational fluff. `claim_evidence_map.yaml` is canonical-JSON-encoded YAML (sort_keys=True; UTF-8; LF; no trailing whitespace; no BOM). Pydantic validation gates every output before write. |

# §14.4 Bundle invariants + input schemas

## §14.4.0 ReportGeneratorRunInput (frozen kw_only)

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class ReportGeneratorRunInput:
    run_id: str                      # opaque; UUID4 generated at dispatch
    org_slug: str                    # exactly one org; Law 3
    grant_id: str                    # the awarded grant the report is for
    period_n: int                    # 1-indexed reporting period (e.g., 1 = Q1 progress report)
    proposal_commitments_path: str   # under orgs/{org_slug}/vault/grants/{grant_id}/; PROMOTED-status required
    reporting_template_path: str     # under orgs/{org_slug}/vault/grants/{grant_id}/; funder-required format
    operational_data_root: str       # orgs/{org_slug}/vault/operational/grants/{grant_id}/period_{n}/
    kfr_register_path: str           # orgs/{org_slug}/vault/kfr/register.yaml; canonicalized read per v7.0.4-M1
    funder_intelligence_root: str    # vault_shared/funder_intelligence/{funder_id}/
    benchmarks_root: str             # vault_shared/benchmarks/
    sub_sections_in_scope: tuple[str, ...]  # default ("narrative", "metrics_table", "financial_summary", "photo_gallery", "beneficiary_section"); operator-tunable per reporting_template requirement
    trend_narrative_authorized: bool  # default False; operator sets True via Sparring Partner gear
    invoked_at_utc: str              # ISO-8601 UTC at dispatch
```

Bundle invariants enforced PRE-gate by `report_generator.pre_gate.input_validation.v1`:
- `org_slug` matches dispatched ORG context (Law 3)
- `grant_id` is a valid grant under `org_slug` (resolves under `orgs/{org_slug}/vault/grants/`)
- `period_n` is a positive integer (1, 2, 3, ...)
- `proposal_commitments_path` resolves under `orgs/{org_slug}/vault/grants/{grant_id}/`; symlink-escape rejected via Path.resolve + os.O_NOFOLLOW (mirrors §11 v1 RT-11 closure)
- `proposal_commitments.yaml` has at least one row with `status: PROMOTED` (otherwise nothing to report against; F-REPORT-COMMITMENT-MISSED.empty_promoted_set fires)
- `reporting_template_path` resolves under `orgs/{org_slug}/vault/grants/{grant_id}/`
- `operational_data_root` resolves under `orgs/{org_slug}/vault/operational/grants/{grant_id}/period_{n}/`
- `sub_sections_in_scope` is a non-empty subset of the closed set `{"narrative", "metrics_table", "financial_summary", "photo_gallery", "beneficiary_section"}`

## §14.4.1 ProposalCommitmentRow (read-substrate; per §11 v1 §11.5.2)

Read-only contract from `proposal_commitments.yaml` — Report Generator does NOT define this schema; it consumes the §11 v1 schema. The fields Report Generator reads:

```yaml
- commitment_id: COMMIT-001  # stable ID across periods
  status: PROMOTED  # Report Generator filters on this
  promotion_signed_at_utc: 2026-04-15T12:00:00Z
  promotion_signature: <Ed25519 signature over canonical-JSON>
  page_tolerance_applied: false  # per §11 v1 RT-01/RT-04
  source_doc: orgs/{org_slug}/vault/grants/{grant_id}/proposal.pdf
  source_page: 12
  submission_artifact_content_sha3_512: <full 128-hex-char digest per RT-05>
  commitment_text: |
    The project will deliver 50 workshops to 200 farmers in PA across Y1.
  scope_tags:
    - workforce_training
    - agriculture
    - pennsylvania
  evaluation_criteria:
    - kind: numeric
      field: workshops_delivered
      target: 50
      tolerance: 0  # exact match required by funder
    - kind: numeric
      field: farmers_trained
      target: 200
      tolerance: 0.05  # ±5% acceptable per funder
    - kind: narrative
      field: workshop_quality_narrative
      required_min_length_chars: 200
  required_sub_sections:
    - metrics_table
    - narrative
```

Report Generator's per-sub-section composer reads PROMOTED commitments + uses `evaluation_criteria` to construct the per-claim evidence trace. F-REPORT-COMMITMENT-MISSED fires for any PROMOTED commitment whose `required_sub_sections` are not all present in the draft.

## §14.4.2 ReportingTemplateContract (read-substrate; per-funder format)

Read-only contract from `reporting_template.yaml` — operator captures at award acceptance from the funder's reporting documentation. Schema:

```yaml
funder_id: USDA-VAPG-FY26  # references vault_shared/funder_intelligence/{funder_id}/
template_version: v1
template_captured_at_utc: 2026-04-15T12:00:00Z
template_captured_by: operator_handle
template_content_sha3_512: <full 128-hex-char digest of the funder's actual template>
required_sub_sections:
  - narrative
  - metrics_table
  - financial_summary
required_fields_per_sub_section:
  narrative:
    - field: accomplishments_narrative
      max_length_chars: 5000
    - field: challenges_narrative
      max_length_chars: 2000
    - field: adjustments_narrative
      max_length_chars: 2000
  metrics_table:
    - field: outcome_metrics
      kind: structured_table
      column_specs:
        - name: metric_name
          required: true
        - name: target
          required: true
        - name: actual
          required: true
        - name: variance_explanation
          required_when_variance_exceeds_pct: 5
  financial_summary:
    - field: budget_actuals_table
      kind: structured_table
      column_specs:
        - name: budget_line
          required: true
        - name: budgeted
          required: true
        - name: actuals
          required: true
        - name: variance
          required: true
        - name: variance_explanation
          required_when_variance_exceeds_pct: 10
required_period_cadence: quarterly  # other values: monthly, semi_annual, annual
report_due_n_days_after_period_end: 30
```

F-REPORT-TEMPLATE-MISMATCH PRE-pre-track-dispatch fail-closes if `template_content_sha3_512` differs from a funder's currently-published template. The funder's currently-published template lives at `vault_shared/funder_intelligence/{funder_id}/published_reporting_template.yaml` (when present; v0.5 first wave funders only — operator may opt-in to per-funder template-drift detection at white-glove). When the funder's published template is absent from the workspace-shared substrate, F-REPORT-TEMPLATE-MISMATCH downgrades to ADVISORY (warning to operator; operator may proceed with operator-captured template).

# §14.5 Output substrate

## §14.5.0 GrantReportBundle (write-substrate; v0.2 NEW per §14)

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class GrantReportBundle:
    run_id: str
    org_slug: str
    grant_id: str
    period_n: int
    draft_path: str                  # orgs/{org_slug}/vault/grants/{grant_id}/reports/period_{n}/draft_{v}.md
    draft_version: int               # v=1, 2, 3 ... within a period (revisions before operator-sign)
    claim_evidence_map_path: str     # orgs/{org_slug}/vault/grants/{grant_id}/reports/period_{n}/claim_evidence_map.yaml
    scoring_dir: str                 # orgs/{org_slug}/vault/grants/{grant_id}/reports/period_{n}/scoring/
    proposal_commitments_consumed: tuple[str, ...]  # commitment_id list (PROMOTED-only)
    reporting_template_content_sha3_512: str  # binds the draft to the template version it was authored against
    sub_sections_authored: tuple[str, ...]   # subset of sub_sections_in_scope
    operator_signature_status: str   # "PENDING_OPERATOR_REVIEW" | "SIGNED"
    operator_signature: str          # Ed25519 signature over canonical-JSON of (claim_evidence_map_path content + reporting_template_content_sha3_512); empty until operator signs
    operator_signed_at_utc: str      # empty until operator signs
    finalized_at_utc: str            # empty until operator signs (= operator_signed_at_utc on success)
    bundle_state: str                # "DRAFT_PENDING_OPERATOR_SIGN" | "FINALIZED"
```

Bundle is `bundle_state == "DRAFT_PENDING_OPERATOR_SIGN"` until operator signs the claim_evidence_map. Finalization (`bundle_state == "FINALIZED"`) is the load-bearing transition that makes the bundle eligible for §12 Uploader staging.

## §14.5.1 ClaimEvidenceMap schema (write-substrate; v0.2 NEW per §14)

```yaml
schema_version: claim_evidence_map.v1
run_id: <UUID4>
org_slug: <slug>
grant_id: <grant_id>
period_n: <int>
draft_path: orgs/{org_slug}/vault/grants/{grant_id}/reports/period_{n}/draft_{v}.md
draft_version: <int>
draft_content_sha3_512: <full 128-hex-char digest of the draft markdown bytes>
authored_at_utc: <ISO-8601>
authored_by_seat: scribe  # the council seat that authored the draft
claims:
  - claim_id: CLAIM-001  # opaque; deterministic per (sub_section, paragraph_index, sentence_index, claim_keyword_hash)
    sub_section: narrative
    claim_text: |
      The project delivered 50 workshops to 200 farmers in Q3 across PA.
    claim_kind: numeric  # one of: numeric | narrative | photo_reference | beneficiary_reference | timeline_reference | financial
    sources:
      - kind: operational_data  # one of: operational_data | proposal_commitments | kfr | benchmarks
        sub_kind: metrics  # required when kind == operational_data
        source_path: orgs/{org_slug}/vault/operational/grants/{grant_id}/period_{n}/metrics/workshops_delivered.yaml
        source_row_id: METRIC-Q3-WORKSHOPS-DELIVERED
        source_content_sha3_512: <full 128-hex-char digest>
        source_value: 50
      - kind: operational_data
        sub_kind: metrics
        source_path: orgs/{org_slug}/vault/operational/grants/{grant_id}/period_{n}/metrics/farmers_trained.yaml
        source_row_id: METRIC-Q3-FARMERS-TRAINED
        source_content_sha3_512: <full 128-hex-char digest>
        source_value: 200
      - kind: proposal_commitments
        commitment_id: COMMIT-001  # links the claim to the original PROMOTED commitment row
        commitment_status: PROMOTED  # MUST be PROMOTED at write time
        scope_tags_at_commitment:
          - workforce_training
          - agriculture
          - pennsylvania
operator_signature_status: PENDING_OPERATOR_REVIEW  # | SIGNED
operator_signature: ""  # Ed25519 sig over canonical-JSON of all fields except this one + operator_signed_at_utc
operator_signed_at_utc: ""
```

**Per-claim invariants** enforced by F-REPORT-COMMITMENT-UNTRACED PRE-pre-finalize:
- Every claim in `draft_<v>.md` MUST appear in `claims:` (claim_id deterministic per (sub_section, paragraph_index, sentence_index, claim_keyword_hash) — re-derivable at audit time).
- Every claim MUST have at least one source. Numeric claims MUST have at least one operational_data OR kfr source. Narrative claims MUST have at least one operational_data OR proposal_commitments source. Photo-reference claims MUST have an operational_data photos sub_kind source. Beneficiary-reference claims MUST have an operational_data beneficiary_records source AND consent_tier verification.
- Every numeric source's `source_value` MUST match the actual value at `source_path` + `source_row_id` at finalize time (re-read at finalize; F-REPORT-COMMITMENT-UNTRACED.source_value_drift fires if mismatch).
- Every source's `source_content_sha3_512` MUST match the actual content hash at finalize time (F-REPORT-COMMITMENT-UNTRACED.source_content_drift fires if mismatch — handles the "operational data was modified after Scribe drafted" case).

**Per-claim signing.** Operator signs the entire `claim_evidence_map.yaml` (Ed25519 over canonical-JSON of all fields except `operator_signature` + `operator_signed_at_utc`); the signature commits the operator to all claims in the map. Per-claim signing (per-claim Ed25519 over per-claim canonical-JSON) is a v1.x candidate for finer-grained operator approval at scale; v0.2 first ship uses single-map signing for simplicity.

**Schema additions per Cycle 1 closures.**
- `claim_evidence_map_version: "v0.2_first_ship_single_map_signing"` (NEW per RT-8c) — immutable per-map; future v1.x per-claim-signing schema bumps to `"v1_x_per_claim_signing"` with backward-compat shim per OQ-REPORT-CLAIM-SIGNING-GRAIN.
- Per photo-reference claim: `caption_text_sha3_512: <full 128-hex-char digest>` (NEW per RT-7b) — hash of just the caption text in the draft markdown, separate from photo bytes hash. At pre-finalize, BOTH caption hash + photo bytes hash are re-checked; mismatch on either → F-REPORT-COMMITMENT-UNTRACED.source_content_drift fail-closes.
- Per beneficiary-reference claim: `consent_tier_history_at_read_utc: <ISO-8601>` (NEW per RT-6c) — timestamp at which the beneficiary record's consent_tier_history was read; pre-finalize re-reads the consent_tier_history + verifies no unsigned post-collection downgrade occurred between read and finalize. If unsigned downgrade detected, F-CEDAR-PII-CONSENT-MISSING.tier_history_unsigned fail-closes.

**Post-sign immutability per Cycle 1 RT-8b closure.** At the moment operator signs `claim_evidence_map.yaml`, the corresponding `draft_<v>.md` file is `flock(LOCK_EX | LOCK_NB)` write-locked AND the file mode is changed to read-only via `chmod 0444`. Any subsequent modification raises `BlueprintImmutableError` (CriticalPolicyError subclass per §13 v1 RT-C2-04 pattern). UI guard at the operator-approval surface disables "Edit Draft" button once the signature is applied. F-REPORT-COMMITMENT-UNTRACED.draft_post_sign_mutation_attempt sub-tag fails-closed at finalize re-read on any mismatch between `draft_content_sha3_512` at sign time and current `draft_content_sha3_512`.

# §14.6 Sub-section composition (5 sub-sections at v0.2 first ship)

Per dispatch decision 8i (monolithic `report_mode` track + sub-section prompt templates), Report Generator composes 5 sub-sections per period via 5 per-sub-section prompt templates. Each sub-section is a self-contained Scribe → Editor → Judge → Red Team → Logician cycle (the same five-seat protocol as submission_mode at the per-section grain).

## §14.6.1 narrative sub-section

Free-text accomplishments + challenges + adjustments. Composer reads operational-data narrative_entries sub-kind + proposal_commitments PROMOTED rows + reporting_template `narrative` field requirements. Scribe drafts each required field (e.g., accomplishments_narrative; challenges_narrative; adjustments_narrative) to the funder-required length. KGIE preflight extended: Scribe asserts that each narrative claim has at least one operational_data narrative_entries OR proposal_commitments source for `claim_evidence_map.yaml`. Editor reviews for clarity + jargon-flagging (extended to funder-reporting terminology — e.g., "impact" vs "output" disambiguation per §10 v1 admin-risk register). Judge scores each narrative against the per-funder reporting rubric (when present in Funder Intel DB) AND against proposal-commitments rubric (every PROMOTED commitment whose `required_sub_sections` includes "narrative" MUST be addressed). Red Team probes for fabricated claims, ungrounded narrative, scope drift beyond commitment_text, and admin-risk term leakage.

## §14.6.2 metrics_table sub-section

Quantitative outcomes table per funder template. Composer reads operational-data metrics sub-kind + KFR canonical (cross-validation) + proposal_commitments evaluation_criteria (target + tolerance per metric). Scribe assembles the table row-by-row with `metric_name | target | actual | variance | variance_explanation` columns (per the funder's required column set). KGIE preflight extended: every numeric value MUST have an operational_data metrics OR kfr source in `claim_evidence_map.yaml`. F-REPORT-NUMERIC-DRIFT POST fires per-cell if `actual` differs from KFR-derived expected value beyond `evaluation_criteria.tolerance`. Decimal comparison per v7.0.4-M1 — ANY float comparison code path is a defect (cross-family Red Team probe MUST cover float-introduced numeric drift). Editor reviews for clarity (variance explanations are concise + funder-ready). Judge scores per metric vs proposal_commitments target + per-funder rubric (when present). Red Team probes for off-by-one, unit-mismatch, period-boundary-confusion (e.g., Q3 metrics vs Q3 + Q2 cumulative), and Decimal-vs-float drift.

## §14.6.3 financial_summary sub-section

Budget actuals + variance table per funder template. Composer reads operational-data financials sub-kind + proposal_commitments evaluation_criteria (budget line targets + tolerance). Scribe assembles the table row-by-row with `budget_line | budgeted | actuals | variance | variance_explanation` columns. ALL monetary values are Decimal per v7.0.4-M1 mandate; ANY float comparison or arithmetic in the financial composer is a defect. F-REPORT-NUMERIC-DRIFT POST fires per-line if `actuals` differs from KFR-derived expected value (when KFR carries a financial actuals row for this period; if not, advisory only). Editor reviews for clarity + funder-required disclaimers (e.g., per-state card financial-disclosure requirements that may apply via §13's state-rules card). Judge scores per budget line vs proposal_commitments + per-funder rubric. Red Team probes for arithmetic off-by-one, currency-rounding accumulation drift (Decimal-precision-aware per v7.0.4-M1), period-boundary financial confusion, and budget-line-name drift between proposal and report (claims that lump budget lines that the proposal kept distinct).

## §14.6.4 photo_gallery sub-section — Cycle 1 RT-7 closures applied

**Per Cycle 1 RT-7a closure (cross-section privacy audit):** NEW PRE-pre-finalize gate scans ALL draft sub-sections (not just photo_gallery) for textual references to any photo_id whose `consent_tier == "internal_only"` OR `consent_tier == "funder_only"` when the section is NOT photo_gallery. F-REPORT-OUT-OF-SCOPE-DRIFT.photo_consent_tier_violation extends with `.cross_section_reference` sub-tag — fail-closed on any cross-section reference exceeding the photo's consent_tier.

**Per Cycle 1 RT-7b closure (caption-text hash inclusion):** per-photo `claim_evidence_map` entry now includes `caption_text_sha3_512` field (hash of just the caption text, separate from photo bytes hash). At pre-finalize, BOTH caption hash + photo bytes hash are re-checked. Mismatch on either → F-REPORT-COMMITMENT-UNTRACED.source_content_drift fail-closes. (Caption substitution post-Scribe is now structurally detectable, not only via the broader `draft_content_sha3_512` audit.)



Photo references + per-photo captions + per-photo provenance + per-photo consent fields. Composer reads operational-data photos sub-kind + reporting_template `photo_gallery` field requirements (when present; some funders require photo_gallery, some don't). Scribe assembles the gallery as Markdown image references with per-photo caption + per-photo metadata block (capture_date_utc, location, photographer, consent_tier from operational-data photos schema). EVERY photo reference in `draft_<v>.md` MUST have a corresponding entry in `claim_evidence_map.yaml` with `kind: photo_reference` and `source_path` pointing to the operational-data photos file + `source_content_sha3_512` for the photo bytes. Photos with `consent_tier == "internal_only"` are excluded from the gallery (F-REPORT-OUT-OF-SCOPE-DRIFT.photo_consent_tier_violation fires if Scribe attempts to include). Editor reviews caption clarity. Judge scores gallery completeness against funder template requirements. Red Team probes for consent_tier bypass, mis-attributed captions (photo from period N attributed to period N-1), and photo-bytes substitution between Scribe author time and operator finalize time (the source_content_sha3_512 re-check at finalize catches this).

## §14.6.5 beneficiary_section sub-section — Cycle 1 RT-6 closures applied

**Per Cycle 1 RT-6a closure (aggregate-of-1 indirect identification check):** beneficiary_section composer's aggregate-count claims that reference a count of ≤2 beneficiaries trigger HIGH advisory surfacing to operator via F-REPORT-OUT-OF-SCOPE-DRIFT.beneficiary_aggregate_identifying sub-tag — operator MUST explicitly approve aggregate inclusion via per-beneficiary-aggregate Ed25519 signature when count ≤ 2.

**Per Cycle 1 RT-6b closure (Cedar engine readiness at every read):** Cedar engine readiness check is per-read, not module-init only. Every operational-data sub-kind read invocation calls `cedar_engine.assert_ready()` predicate; engine failure → fail-closed F-CEDAR-OPERATIONAL-DENIED.engine_unready at the read point (mirrors §13 v1 RT-C2-04 closure pattern: CriticalPolicyError(BaseException) propagation).

**Per Cycle 1 RT-6c closure (consent_tier history with per-change Ed25519 signature):** beneficiary_records carry `consent_tier_history` field per §13 v1 schema extension (per-tier-change operator Ed25519 signature; rejected if tier downgraded after `created_at_utc` without a signed downgrade event). Report Generator's read path checks the tier history at every read; if any post-collection downgrade is unsigned, F-CEDAR-PII-CONSENT-MISSING.tier_history_unsigned fail-closes.



Beneficiary records + per-beneficiary outcome narratives. Composer reads operational-data beneficiary_records sub-kind + reporting_template `beneficiary_section` field requirements. **Cedar PII enforcement is non-negotiable at the read path** (per §2 v7.2 RT-C1 + §13 v1 read-path inheritance): F-CEDAR-OPERATIONAL-DENIED + F-CEDAR-PII-CONSENT-MISSING fire at the read path before Scribe sees any beneficiary record. Scribe sees only operator-classification-approved beneficiary records (per §13 v1 first-occurrence-classification discipline). Per-beneficiary `consent_tier` (per §13 v1 RT-C2-10 closure) gates inclusion: `consent_tier == "narrative-text-only"` is the floor for text inclusion; `consent_tier == "metrics-only"` allows aggregate count but no per-beneficiary text; `consent_tier == "no-narrative"` excludes from the beneficiary_section entirely. F-REPORT-OUT-OF-SCOPE-DRIFT.beneficiary_consent_tier_violation fires if Scribe attempts to include a beneficiary at a tier above their consent_tier. EVERY beneficiary reference in `draft_<v>.md` MUST have a corresponding entry in `claim_evidence_map.yaml` with `kind: beneficiary_reference` + per-beneficiary consent_tier verification. Aggregate beneficiary counts (e.g., "served 200 farmers across PA") trace to operational-data beneficiary_records aggregate query (the count is itself a numeric claim subject to F-REPORT-NUMERIC-DRIFT). Editor reviews for sensitivity (avoid identifying details where consent_tier doesn't permit). Judge scores section completeness against funder template + proposal_commitments beneficiary-count targets. Red Team probes for consent_tier bypass, identifying-detail leakage where consent_tier prohibits, cross-period beneficiary double-counting, and beneficiary-records substitution between author time and finalize time.

# §14.7 Council seat behavior under report_mode

The same five council seats run on report_mode with role-modified behavior per the table below. Scout is informational-only in report_mode (Scout's discovery role is NOT engaged when the track is `report`; Scout's funder-intelligence read of `vault_shared/funder_intelligence/{funder_id}/` is a Funder Intel DB read for narrative context, not a discovery call).

| Seat | submission_mode behavior | report_mode behavior |
|------|--------------------------|----------------------|
| **Scout** | Two-stage discovery (DISCOVER wide → VERIFY live → REVIEW human gate) per §3 | Informational-only — reads Funder Intel DB for funder-specific reporting context (e.g., "this funder typically requests photos in addition to narrative"); no discovery call |
| **Scribe** | Drafts proposals section by section with KGIE preflight, SMART outcomes, funder dialect | Drafts per-sub-section reports with KGIE preflight extended to claim_evidence_map authoring; SMART outcomes extended to per-period actuals reporting; funder dialect inherits per-funder Funder Intel DB context |
| **Editor** | Clarity + jargon flagging on Scribe's draft | Clarity + jargon flagging extended for funder-reporting-specific terminology (e.g., "impact" vs "output" disambiguation per admin-risk register); proposes-only per §15 v1 + §11 v1 + §13 v1 patterns |
| **Judge** | Scores against funder's rubric first, then cross-checks rubric library | Scores against proposal-commitments rubric FIRST (every PROMOTED commitment scored), then cross-checks against funder's published reporting rubric (when present in Funder Intel DB per v7.0.5) |
| **Red Team** | Adversarial challenge on every draft section | Adversarial challenge on every sub-section; cross-family rigor against Scribe AND Judge (never shares family with either); probes Boundary-Drift + Numeric-Drift + Commitment-Missed + Cross-Period-Reuse + Template-Mismatch pathways |
| **Logician** | Five Laws as PRE/POST gates; deterministic Python + Cedar | F-REPORT-* family PRE/POST gates fail-closed per §4 v2.x §5.1 ACTIVATION at this LOCK; Cedar policies + check callables per §14.9 |

**Cross-family rigor.** Editor=Llama-3.3-70B/Groq (Meta family) + Judge=Gemini-2.5-Pro/Google (Google family) + Red Team=GPT-OSS-120B/Groq (OpenAI-OSS family) per the same router.yaml bindings as submission_mode. Scribe primary=Anthropic per router.yaml. L-003 satisfied: no two of Scribe + Editor + Judge + Red Team share a model family.

**Disagreement handling.** Per §10 v1 admin-risk register: ≥10pt disagreement between Judge and Red Team triggers council split (Law 4 tie-breaker — operator decides). Cross-period claim reuse + multi-period bundling per §14.12 are operator-decision surfaces by design (not auto-resolved by council majority).

# §14.8 Track-binding (rides §5 v8 §4.16 dispatcher)

## §14.8.0 §5 v8 §4.16 dispatcher contract integration

Per §5 v8 §4.16 dispatcher contract clauses 1-7, this §14 v1 LOCK integrates report_mode via:

1. **Resolve `name == "report"` via `get_track`** — at v0.2 Tilths (`TILTH_VERSION_FAMILY = "v0.2"`), the shippable_in gate passes (v0.2 ≥ v0.2). At v0.1 Tilths, the gate continues to refuse (v0.1 < v0.2) with `TrackNotShippable` per §5 v8 §3.2.9. **THIS §14 v1 LOCK does NOT change the v0.1 Tilth runtime behavior; v0.2 Tilths automatically receive report_mode runtime-reachability when `TILTH_VERSION_FAMILY` bumps to v0.2 at the v0.2 release.**
2. **Verify `track.pipeline_shape == "prior_commitments_to_council_to_signed_report"` is in `_V0_1_IMPLEMENTED_SHAPES`** — at this LOCK, the `_V0_1_IMPLEMENTED_SHAPES` frozenset extends from `{"rfa_to_council_to_signed_bundle", "operator_harness_to_per_seat_calibration"}` to `{"rfa_to_council_to_signed_bundle", "operator_harness_to_per_seat_calibration", "prior_commitments_to_council_to_signed_report"}`. The `assert len(_V0_1_IMPLEMENTED_SHAPES) == 2` invariant in §5 v8 §8 BUMPS to `assert len(_V0_1_IMPLEMENTED_SHAPES) == 3` per §14 v1 paired-commit. (NOTE: §5 v8 §8 invariant text is updated by THIS LOCK as part of the compound transaction; the §5 amendment file body is NOT modified — the invariant is layered over the §5 v8 LOCKED text via §14's companion §0.5 v16 amendment.)
3. **Dispatch via the `report` arm of the `if/elif` chain** — clause 3-4 of the dispatcher get a NEW arm: `if shape == "prior_commitments_to_council_to_signed_report": invoke report_runner(**report_kwargs)`. The §5 v8 §4.16 contract clause 5 (DI seam) admits the new arm via the new `report_runner` argument added to `dispatch_track`. Production wires `pipeline.orchestrator.tracks.report_mode.run_report_pipeline`.
4. **Runtime-rebind sentinel** — the if/elif chain's defensive raise for monkey-patched `_V0_1_IMPLEMENTED_SHAPES` (clause 7 per §5 v8 §4.16 RT-02 closure) extends to cover the new third shape. ANY runtime monkey-patch to admit a fourth shape will hit the defensive raise of `TrackShapeUnimplemented`.
5. **Dispatch BY pipeline_shape, NOT by which runners the caller supplies** — clause 6 invariant per §5 v8 RT-07 closure preserved: supplying a `report_runner` to a `submission` track does NOT cause the report runner to fire on submission data; the dispatcher branches on `pipeline_shape` regardless of which runner arguments are supplied.

**§7.19 (NEW Cycle-1 RT-01 closure of §5 v8) carve-out invariant** — no NEW track-by-name literals admitted in `pipeline/loop/run_*.py`. THIS §14 v1 LOCK does NOT add a new `if mode == "report": ...` branch in any `pipeline/loop/run_*.py`; the addition is at the dispatcher's DI seam ONLY. The §5 v8 invariant §7.19 audit re-fires at this LOCK to confirm no new track-by-name literal was introduced.

## §14.8.1 router.yaml report row binding

The §5 v8 LOCKED router.yaml `report` row (per §5 v8 §4.16 router-yaml example) carries the following bindings — no field changes at THIS LOCK (the bindings were authored at §5 v8 LOCK):

```yaml
report:
  kind: track
  pipeline_shape: prior_commitments_to_council_to_signed_report
  prompt_template_root: pipeline/prompts/report/  # symlink/alias to skills/scribe-ghostwriter/report_mode_prompts/
  failure_code_prefix: F-PIPE-REPORT-
  cross_family_rigor: required
  shippable_in: v0.2
  scribe_prompt_template: pipeline/prompts/report/scribe.md  # composes the 5 per-sub-section templates per request
  judge_rubric_ref: pipeline/rubrics/proposal_commitments.json  # symlink/alias to skills/judge-rubric/proposal_commitments_rubric.json
  red_team_probe_template: pipeline/prompts/report/red_team_probe.md  # composes the 5 per-sub-section probes
  output_vault_subtree: orgs/{org_slug}/vault/grants/{grant_id}/reports/period_{n}/
  output_schema: GrantReport  # references §14.5.0 GrantReportBundle
```

**No router.yaml row-content changes at THIS LOCK.** The §5 v8 LOCKED row anticipated the bindings; THIS §14 LOCK realizes the prompt templates + rubric + probes at the on-disk paths declared in the row. The row's `output_schema: GrantReport` binds to `GrantReportBundle` per §14.5.0.

**Why no `shippable_in` flip at this LOCK?** Per §5 v8 §3.2.9 + §14.0 cross-amendment composition map note: `shippable_in: v0.2` continues to be the gate; the gate passes when `TILTH_VERSION_FAMILY = "v0.2"`, which is set at v0.2 first-ship Tilth release time (NOT a config-flag-flip; a Tilth-version-family bump owned by SN-LLC release pinning per v7.0.7 §6.1 router-template-update pattern). v0.1 Tilths continue to refuse report_mode at runtime via the shippable_in gate; v0.2 Tilths ship with `TILTH_VERSION_FAMILY = "v0.2"` and the gate passes automatically.

# §14.9 Failure codes / gates owned (5 F-REPORT-* + composed gates)

## §14.9.0 PRE-pre-track-dispatch consolidated check

Per §4 v2.2 consolidated-check-callable pattern (mirrors §11 v1 + §13 v1 + §15 v1 consolidated PRE-gate precedent), Report Generator's PRE-pre-track-dispatch check callable runs the four-gate sequence:

1. F-REPORT-TEMPLATE-MISMATCH (PRE pre-track-dispatch)
2. F-REPORT-COMMITMENT-MISSED (POST judge-equivalent — but advisory at PRE: empty-PROMOTED-set check)
3. F-CEDAR-OPERATIONAL-DENIED (read-path Cedar policy on operational-data)
4. F-CEDAR-PII-CONSENT-MISSING (read-path Cedar policy on beneficiary_records)

**Per Cycle 1 RT-10a closure (run-all-then-collect, supersedes the prior short-circuit semantics):** the consolidated check RUNS ALL FOUR gates regardless of early failures + collects every fired sub-tag into a comprehensive diagnostic set. Dispatcher aborts the pipeline AFTER collection completes; operator receives the full failure-code list ranked by severity (P0 → HIGH → MED → LOW) for actionable prioritization. The four-gate ordering is fixed for diagnostic-output stability (NOT operator-tunable); reordering would shuffle the first-rank position in the operator UI but does not change which gates fire.

## §14.9.1 F-REPORT-COMMITMENT-UNTRACED (POST scribe-equivalent)

**Trigger.** A claim in `draft_<v>.md` does not appear in `claim_evidence_map.yaml`.

**Behavior.** Fail-closed; refuses report finalization (operator cannot sign a draft with untraced claims).

**Sub-tags.**
- `.claim_text_no_map_entry` — claim is in draft but no entry in claim_evidence_map matches the claim_id (deterministic per (sub_section, paragraph_index, sentence_index, claim_keyword_hash))
- `.numeric_claim_no_numeric_source` — numeric claim has no operational_data OR kfr source in claim_evidence_map
- `.narrative_claim_no_narrative_source` — narrative claim has no operational_data narrative_entries OR proposal_commitments source
- `.photo_reference_no_photo_source` — photo reference has no operational_data photos source
- `.beneficiary_reference_no_beneficiary_source` — beneficiary reference has no operational_data beneficiary_records source
- `.beneficiary_reference_consent_tier_unverified` — beneficiary reference present but consent_tier verification missing
- `.source_value_drift` — numeric source's `source_value` in claim_evidence_map does not match the actual value at `source_path` + `source_row_id` at finalize time (operational data was modified post-Scribe; or a typo in claim_evidence_map authoring)
- `.source_content_drift` — source's `source_content_sha3_512` does not match the actual content hash at finalize time
- `.commitment_id_not_promoted` — claim references a `commitment_id` whose `status` at finalize time is NOT `PROMOTED` (the operator promoted a commitment, then later un-promoted; PENDING_OPERATOR_REVIEW commitments cannot be claim sources)
- `.kfr_source_canonical_drift` — KFR source's canonical-JSON content drifted between author time and finalize time (Decimal precision-aware comparison per v7.0.4-M1; `vault_read_intent_kfr_atomic_snapshot` ID match required between Scribe author-time read and pre_finalize re-read per Cycle 1 RT-1c closure)
- `.cross_period_signature_invalid` (NEW per Cycle 1 RT-4a closure) — SP0 flag `accept_signed_prior_period_claim_evidence_map: true` is active but the per-report `sp0_flags.signed.yaml` operator Ed25519 signature does not verify against the operator's pinned public key
- `.draft_post_sign_mutation_attempt` (NEW per Cycle 1 RT-8b closure) — draft_<v>.md was modified after operator signed the claim_evidence_map (detected at finalize re-read of `draft_content_sha3_512`); raises BlueprintImmutableError (CriticalPolicyError subclass per §13 v1 RT-C2-04 pattern); operator must re-sign a fresh draft

**Per Cycle 1 RT-1a closure: semantic entailment requirement.** Per-claim source MUST contain the claim's load-bearing keywords/values verbatim where rendered. For `claim_kind: numeric`: the source's `source_value` MUST match the claim's `claim_value` EXACTLY in Decimal (per v7.0.4-M1). For `claim_kind: narrative`: at least one operational_data narrative_entries OR proposal_commitments source whose `text` field contains the claim's content-bearing N-gram (per a `runtime_entailment_check` predicate in the gate body — heuristic: claim's noun-phrase + verb-phrase MUST appear in source text within a 50-token window). Existence + content-hash check alone is INSUFFICIENT; semantic-entailment-or-exact-match is the contract per claim_kind. WS-J Code phase realizes the entailment check via deterministic Python (NOT an LLM call — Logician is zero-token by §4 v2.2 contract).

**Predicate body** (skeleton at v0.2 first ship; full impl in WS-J Code phase):
```python
def f_report_commitment_untraced_check(ctx: ReportFinalizeContext) -> CheckResult:
    """PRE pre-finalize. Walks every claim in draft_<v>.md, verifies each has an entry
    in claim_evidence_map with appropriate sources for its claim_kind, re-reads each
    source at finalize time, compares Decimal/canonical-JSON with v7.0.4-M1 discipline."""
    raise NotImplementedError("F-REPORT-COMMITMENT-UNTRACED predicate body deferred to WS-J Code phase")
```

**Cedar policy** (skeleton at v0.2 first ship):
```cedar
forbid (
  principal == ReportGenerator::"finalize_action",
  action == Vault::"write_finalized_report",
  resource is GrantReportBundle
) when {
  resource.bundle_state == "DRAFT_PENDING_OPERATOR_SIGN" &&
  resource.has_untraced_claim == true
};
```

## §14.9.2 F-REPORT-COMMITMENT-MISSED (POST judge-equivalent)

**Trigger.** A `proposal_commitments.yaml` row with `status: PROMOTED` has NO corresponding draft section addressing it.

**Behavior per Cycle 1 RT-2b closure (FAIL-CLOSED for required sub-section coverage; ADVISORY only for the period-not-due-yet path with capped suppressions).** PROMOTED commitments whose `required_sub_sections` intersect `sub_sections_in_scope` MUST be addressed (FAIL-CLOSED on `.commitment_required_subsection_missing` + `.commitment_evaluation_criterion_unaddressed`). PROMOTED commitments whose `required_sub_sections` do NOT intersect `sub_sections_in_scope` (multi-period commitments not addressable in this period) may be suppressed via per-commitment operator-signed waiver — capped at `len(promoted_commitments) - 1` per period (i.e., at least one commitment must be addressed; vacuous reports structurally forbidden).

**Sub-tags.**
- `.empty_promoted_set` — `proposal_commitments.yaml` has zero PROMOTED rows (operator never promoted anything; nothing to report against; PRE-pre-track-dispatch fail-closed)
- `.commitment_required_subsection_missing` — PROMOTED commitment row's `required_sub_sections` includes a sub-section that is NOT in `sub_sections_authored` (FAIL-CLOSED per Cycle 1 RT-2b closure)
- `.commitment_evaluation_criterion_unaddressed` — PROMOTED commitment row's `evaluation_criteria` includes a numeric field with no metrics_table cell or a narrative field with no narrative paragraph (FAIL-CLOSED per Cycle 1 RT-2b closure)
- `.commitment_period_n_not_due_yet` — PROMOTED commitment is for a future period (e.g., Y2 commitment in Q1 Y1 report); operator may suppress this sub-tag per-commitment via per-commitment operator Ed25519 signed waiver file at `orgs/<slug>/vault/grants/<grant_id>/reports/period_<n>/commitment_waivers/<commitment_id>.signed.yaml` (with `waiver_reason` + `waiver_signed_at_utc` + `waiver_signature` over canonical-JSON of waiver_reason + commitment_id + period_n + run_id + waiver_signed_at_utc); CAPPED at `len(promoted_commitments) - 1` per period
- `.commitment_waiver_unsigned` (NEW per Cycle 1 RT-2b closure) — operator attempted to suppress a commitment via the not-due-yet path but the corresponding `<commitment_id>.signed.yaml` waiver file is missing OR the Ed25519 signature does not verify; FAIL-CLOSED
- `.commitment_waiver_cap_exceeded` (NEW per Cycle 1 RT-2b closure) — operator attempted to suppress more commitments than the cap permits (i.e., would result in zero commitments addressed in this period); FAIL-CLOSED — vacuous reports structurally forbidden

**Predicate body** (skeleton at v0.2 first ship):
```python
def f_report_commitment_missed_check(ctx: ReportJudgeContext) -> CheckResult:
    """POST judge-equivalent. Walks every PROMOTED proposal_commitments row, asserts
    that required_sub_sections subset of sub_sections_authored AND every evaluation
    criterion has a corresponding draft addressing-element."""
    raise NotImplementedError("F-REPORT-COMMITMENT-MISSED predicate body deferred to WS-J Code phase")
```

## §14.9.3 F-REPORT-OUT-OF-SCOPE-DRIFT (POST judge-equivalent + Cedar at write path)

**Trigger.** A claim in `draft_<v>.md` exceeds the original proposal's defined scope.

**Behavior.** Fail-closed (Boundary Drift per Law 2 + Law 5).

**Three-layer detection** (mirrors §15 v1 + §13 v1 three-layer pattern):
- **AST-lint at compile time** — `R-REPORT-NO-OUT-OF-SCOPE-CLAIM` on per-sub-section prompt templates: rejects template directives that instruct Scribe to claim scope-tags not present in any PROMOTED commitment.
- **Runtime check at compose time** — Scribe authors a draft; for each claim, the runtime check resolves the claim's scope-tags (via NER + scope-tag taxonomy) and compares to the union of PROMOTED commitments' `scope_tags`. Any claim whose scope-tag set is NOT a subset triggers fail-closed.
- **Cedar policy at write path** — `report_out_of_scope.cedar` denies `Vault::write_finalized_report` where the GrantReportBundle's claim-scope-tag set is NOT a subset of the union of PROMOTED commitments' scope-tag sets.

**Sub-tags.**
- `.scope_tag_not_in_promoted_set` — claim's scope-tag is not in any PROMOTED commitment's scope-tag set
- `.cross_grant` — claim references a different grant_id than the report's grant_id (Law 3 isolation; composes with F-REPORT-CROSS-ORG-LEAK)
- `.cross_org` — claim references a different org_slug than the report's org_slug (Law 3 isolation; structural enforcement)
- `.cross_period` — claim references a period_n other than the report's period_n WITHOUT explicit cross-period-reuse operator approval per §14.12.1
- `.beneficiary_consent_tier_violation` — claim includes beneficiary detail at a tier above the beneficiary's consent_tier (composes with F-CEDAR-PII-CONSENT-MISSING)
- `.photo_consent_tier_violation` — claim includes a photo whose consent_tier is `internal_only`
- `.runtime_scope_tag_extraction_failed` — runtime NER failed to extract scope-tags from claim text (advisory; fall-through to operator review)

**Predicate body + Cedar policy** (skeleton at v0.2 first ship; full impl in WS-J Code phase).

## §14.9.4 F-REPORT-NUMERIC-DRIFT (POST scribe-equivalent)

**Trigger.** A numeric claim in `draft_<v>.md` differs from KFR-derived expected value beyond per-field tolerance.

**Behavior.** Fail-closed.

**Decimal mandate per v7.0.4-M1 + Cycle 1 RT-3a/b closure (R-REPORT-DECIMAL-MANDATE AST-lint + canonical rounding mode).** ALL numeric comparisons in this gate's predicate body use `decimal.Decimal`. ANY float-comparison code path is a defect. Canonical rounding mode is `decimal.ROUND_HALF_UP` (banker's rounding rejected per accounting-norm in funder financial reports); variance computation: `variance_pct = (variance / budgeted * Decimal(100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`. NEW AST-lint rule **R-REPORT-DECIMAL-MANDATE** (registered in `pipeline/linting/ast_lint.py` per WS-J Code phase) rejects any `pipeline.logician.gates.f_report_*.py` module containing: (a) `float()` call inside the gate predicate body; (b) float-literal arithmetic in gate predicate body; (c) `==` comparison between values without a preceding `isinstance(..., Decimal)` assert. Defense-in-depth: gate predicate body's first executable statement at WS-J Code phase MUST be `assert all(isinstance(v, Decimal) for v in (...))` for every numeric-touching code path. Unit conversion factors stored as canonical-JSON Decimal strings at `vault_shared/unit_conversion_factors.signed.yaml` (SN-LLC-signed per v7.0.7 §6.1 router-template-update pattern); R-REPORT-DECIMAL-MANDATE rejects any `float(factor)` cast in unit conversion code paths. Cross-family Red Team probe MUST cover float-introduced numeric drift as adversarial scenario (e.g., a draft cell value of `0.1 + 0.2` represented as float 0.30000000000000004 vs Decimal 0.3 — the gate MUST catch this and refuse the draft).

**Sub-tags.**
- `.kfr_value_mismatch_above_tolerance` — claim value > KFR value + tolerance (over-claim)
- `.kfr_value_mismatch_below_tolerance` — claim value < KFR value - tolerance (under-claim)
- `.kfr_value_unit_mismatch` — claim and KFR carry different units (e.g., kg vs lb); composes with F-DATACOLLECTOR-KFR-DRIFT.unit_mismatch from §13 v1
- `.float_comparison_detected` — defect-detection: the predicate body executed a float comparison instead of Decimal; surfaces to operator + Logician audit log; v0.2 first-ship gate ASSERTS Decimal in the predicate body (defense-in-depth against future contributor introducing a float comparison)
- `.kfr_field_absent` — claim's referenced `field` is not present in KFR (advisory; may be a KFR-staleness issue)
- `.tolerance_unset_for_numeric_field` — claim's referenced field has no tolerance set in proposal_commitments evaluation_criteria; v0.2 default = exact match required (tolerance = 0); operator may set per-field tolerance via proposal_commitments authoring at award acceptance
- `.operational_data_value_drift_from_kfr` — operational-data sub-kind value (e.g., metrics) differs from KFR canonical (composes with F-LOGICIAN-FACT-DRIFT family from v7.0.4); Report Generator may surface BOTH the operational-data value AND the KFR value to the operator with a "which is canonical?" decision surface

**Predicate body** (skeleton at v0.2 first ship):
```python
def f_report_numeric_drift_check(ctx: ReportComposeContext) -> CheckResult:
    """POST scribe per-cell. For each numeric claim, looks up KFR canonical value,
    compares using decimal.Decimal (NEVER float), checks against per-field tolerance
    from proposal_commitments evaluation_criteria. Fail-closes if drift exceeds tolerance.
    Defense-in-depth: asserts the comparison code path uses Decimal (raises if float)."""
    raise NotImplementedError("F-REPORT-NUMERIC-DRIFT predicate body deferred to WS-J Code phase")
```

## §14.9.5 F-REPORT-TEMPLATE-MISMATCH (PRE pre-track-dispatch)

**Trigger.** `reporting_template.yaml` schema does not match the funder's actual reporting template at dispatch time.

**Behavior per Cycle 1 RT-5a closure (FAIL-CLOSED for SN-LLC first-wave funders + ADVISORY for non-first-wave).** Fail-closed when (a) funder's published template is present in workspace-shared substrate AND template-content-hash mismatch detected, OR (b) funder is in SN-LLC's first-wave funder set (operator-confirmed at white-glove via `vault_shared/funder_intelligence/<funder_id>/sn_llc_first_wave.signed.yaml` SN-LLC-signed marker file) AND workspace-published template is missing OR signature invalid. ADVISORY only for non-first-wave funders where the funder has no SN-LLC-shipped published template (operator captured template is the only source of truth for those funders). SN-LLC ships the first-wave marker for VAPG / NIFA / SARE / EPA NEETP / SBIR at v0.2 first wave per the §13 v1 state-rules-card precedent. The marker file's hash is bound to the lock_history immutable ledger so deletion is auditable + detectable.

**Detection layers.**
- **Operator-captured template content hash check** — `reporting_template.yaml` carries `template_content_sha3_512` (full digest of the funder's actual template the operator captured at award acceptance). PRE-pre-track-dispatch re-reads the workspace-shared substrate `vault_shared/funder_intelligence/{funder_id}/published_reporting_template.yaml` (when present) + recomputes the digest + compares. Mismatch → fail-closed.
- **Schema-shape check** — `required_sub_sections` + `required_fields_per_sub_section` schema is fixed at v0.2 first ship; `reporting_template.yaml` MUST conform. Schema-drift (e.g., funder added a new required field; operator's captured template lacks it) → fail-closed.
- **Period cadence check** — `required_period_cadence` MUST be a value in the closed set `{"monthly", "quarterly", "semi_annual", "annual"}`. Other values → fail-closed.

**Sub-tags.**
- `.workspace_published_template_drift` — operator-captured template's content hash differs from workspace-shared `published_reporting_template.yaml` content hash
- `.workspace_published_template_absent` — funder's published template not in workspace-shared substrate; downgrade to ADVISORY (operator captured template is the only source of truth for this funder; v0.2 first wave funders only have published templates per operator opt-in at white-glove)
- `.schema_required_sub_sections_unrecognized` — `required_sub_sections` includes a value not in the closed set `{"narrative", "metrics_table", "financial_summary", "photo_gallery", "beneficiary_section"}`
- `.schema_required_fields_unspecified` — `required_fields_per_sub_section` for a `required_sub_section` is empty or missing
- `.period_cadence_invalid` — `required_period_cadence` is not in the closed set
- `.template_signature_invalid` — operator-captured template's Ed25519 signature (when operator signs the captured template at white-glove) does not verify against the operator's pinned public key
- `.workspace_published_template_absent_first_wave` (NEW per Cycle 1 RT-5a closure) — funder is in SN-LLC's first-wave set but `vault_shared/funder_intelligence/<funder_id>/published_reporting_template.yaml` is missing OR `sn_llc_first_wave.signed.yaml` marker file is missing/tampered; FAIL-CLOSED
- `.operator_key_version_mismatch` (NEW per Cycle 1 RT-5b closure) — `reporting_template.yaml` was signed with an operator key version that doesn't match the currently-pinned operator key OR the auditable predecessor key whose rotation event is logged in lock_history; FAIL-CLOSED. v7.0.7 §6.1 Trust-On-First-Use rotation pattern applies — new operator public key MUST be co-signed by the previous operator key
- `.period_cadence_actual_drift` (NEW per Cycle 1 RT-5c closure) — `required_period_cadence` does not match the actual period_n interval derived from the grant's `award_signed_at_utc` (per §11 v1 AWARD_INGEST); ADVISORY operator-decision surface ("template requires quarterly; this is period N which spans M months — confirm cadence")

**Predicate body** (skeleton at v0.2 first ship):
```python
def f_report_template_mismatch_check(ctx: ReportPreDispatchContext) -> CheckResult:
    """PRE pre-track-dispatch. Reads operator-captured reporting_template.yaml, validates
    schema shape, validates period cadence, compares content hash to workspace-shared
    published template (when present). Fail-closes on hard schema violations OR
    workspace-template drift; advisories on workspace-published-template-absent."""
    raise NotImplementedError("F-REPORT-TEMPLATE-MISMATCH predicate body deferred to WS-J Code phase")
```

# §14.10 Classification routing (v7.0.7 inheritance)

Per v7.0.7 LOCKED §1 + §4.1 + §4.2:

| Seat / sub-step | Routing posture |
|---|---|
| Scribe sub-section template authoring | Cloud-routable when input is Public+Shareable + opaque [SLOT_<numeric_id>] tokens for any Confidential per-org value |
| Slot-fill agent (always-local) | Renders Confidential into post-fill drafts after Scribe returns |
| Editor reads post-fill draft | Always-local routing (post-fill draft contains Confidential by definition) |
| Red Team reads post-fill draft | Always-local routing |
| Judge reads post-fill draft (routine-Judge) | Always-local routing on 70B-class local model |
| Judge reads post-fill draft (heavy-Judge swap) | On-demand local 200B-class model swap available for high-stakes reports per v7.0.7 §4.2; operator-flagged via per-report SP0 |
| Logician F-REPORT-* gates | Zero-token; deterministic Python + Cedar; no routing applies |

**Slot-fill discipline.** All Confidential per-org values referenced in cloud-routed Scribe templates use opaque `[SLOT_<numeric_id>]` tokens (e.g., `[SLOT_001]`, `[SLOT_002]`); the mapping `slot_id → confidential_field_path` lives in the local slot-fill agent only. Semantic slot names (e.g., `[SLOT_BENEFICIARY_NAME]`, `[SLOT_FINANCIAL_TOTAL]`) are forbidden in cloud-routed prompts — F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate from v7.0.7 fail-closes any prompt that violates.

**Once a draft is post-fill, all subsequent seats reading it must be local-routed.** Editor's post-fill review + Red Team's post-fill probe + Judge's post-fill scoring all run on local-routed Tilth seats (70B-class default; 200B-class on heavy-Judge swap). This is structural sovereignty per v7.0.7 §4.2 — Confidential per-org data never leaves the appliance after slot-fill.

**High-stakes report → heavy-Judge swap.** Per v7.0.7 §4.2 + §14 RT-XX (TBD per Cycle 1 surface), high-stakes reports (federal long-form / large award / operator-flagged) trigger an on-demand local heavy-Judge swap — a 200B-class model loaded for the cycle (DeepSeek V3 / Qwen 3 235B-A22B / Mistral Large 2 / GPT-OSS 120B per Sovereign Node LLC's current best-of-breed pick). The swap flag itself is classified `confidential` per v7.0.7 §4.1 (operator-set per-report SP0); F-CLASS-HIGH-STAKES-FLAG-LEAK PRE-gate fail-closes if the flag leaks into a cloud payload.

# §14.11 CIC × CLC orthogonality (v7.0.8 inheritance)

Per v7.0.8 LOCKED:

- Every per-sub-section prompt template at `skills/scribe-ghostwriter/report_mode_prompts/` is audited at LOCK against F-CIC-CLC-COUPLING-VIOLATION via the four detection layers: lexical regex (no CIC→CLC pre-mapping in template text); Pydantic AST (no CIC-keyed CLC subset in template prompt structure); value-set (no enum constraining CLC to a CIC-derived subset); KP schema (no Knowledge Pack reference encoding CIC→CLC binding).
- The proposal_commitments rubric at `skills/judge-rubric/proposal_commitments_rubric.json` is audited at LOCK against F-CIC-CLC-COUPLING-VIOLATION (rubric scoring criteria cannot encode CIC→CLC subset binding; opportunity-driven runtime matching per v7.0.8).
- The per-sub-section red-team probes at `skills/red-team/report_mode_probes/` are audited at LOCK against F-CIC-CLC-COUPLING-VIOLATION (probes cannot encode CIC→CLC subset binding).

**Audit at LOCK.** §14 v1 LOCK runs the 84-test CIC × CLC orthogonality regression baseline (per v7.0.8 §test count) extended with §14-specific test cases targeting the 5 sub-section prompt templates + the rubric + the 5 red-team probes. CI-clean is a precondition for LOCK.

# §14.12 Cross-period claim reuse + funder rubric cross-check + multi-period bundling

Three operator-decision surfaces; defaults per dispatch packet OQ list:

## §14.12.1 Cross-period claim reuse

**Default: re-prove from period-(N-1) operational data per claim.** When a period-N report cites period-(N-1) accomplishments (e.g., "as reported in Q2, the project delivered..."), Scribe re-proves from period-(N-1) operational data. Period-(N-1) `claim_evidence_map.yaml` is NOT accepted as a signed input by default — fail-closed discipline prefers re-proof over claim-of-prior-claim.

**Operator override.** Per-report SP0 flag `accept_signed_prior_period_claim_evidence_map: true` permits Scribe to consume period-(N-1) `claim_evidence_map.yaml` as a signed input (operator-signed; operator-Ed25519-pinned). Surfaced at Audit #1 OQ-REPORT-XPERIOD-DEFAULT for operator confirmation.

**Why default to re-prove?** Two reasons. First, fail-closed discipline (Law 1 + Law 5: every claim traces to canonical operational data, not to a prior claim derived from operational data — the second-order trace is fragile if period-(N-1) operational data is later corrected). Second, the operator wrote the period-(N-1) signature once — having Scribe re-derive period-(N-1) actuals at period-N report time is cheap (operational data is on-disk), and surfaces any period-(N-1) data corrections that the operator made between sign-and-now.

## §14.12.2 Funder rubric cross-check

**Default: funder's own published rubric first, then proposal_commitments rubric as supplementary (per memory `feedback_judge_rubric_strategy.md`).** When Funder Intel DB carries a published reporting rubric for the funder (`vault_shared/funder_intelligence/{funder_id}/published_reporting_rubric.yaml`), Judge runs the funder's rubric FIRST + proposal_commitments rubric SECOND for cross-check. Funder rubric scoring is the load-bearing surface; proposal_commitments rubric provides per-commitment-row evaluation as a supplementary cross-check.

**When funder's published rubric is absent.** Judge runs only the proposal_commitments rubric. Surfaced to operator at draft review: "no funder published reporting rubric in workspace-shared substrate; Judge scored against proposal_commitments rubric only."

**Surfaced at Audit #1 OQ-REPORT-RUBRIC-DEFAULT for operator confirmation.**

## §14.12.3 Multi-period bundling

**Default: separate drafts per period; operator-bundled at submission via §12 Uploader.** When a funder requires a single report covering periods M-N (e.g., annual narrative + financials covering Q1-Q4), Report Generator generates N separate drafts; operator-bundled at submission via §12 Uploader's package assembly (per §12 v1 §12.10 adapter pattern).

**Operator override.** Per-report SP0 flag `bundle_periods: [M, N]` permits Report Generator to compose a single bundled draft covering periods M-N. Bundled drafts inherit the strictest sub-section requirements across periods (e.g., if Q3 requires photo_gallery and Q1-Q2 don't, bundled draft includes photo_gallery for Q3-only sources).

**Why default to separate drafts?** Operator clarity: per-period drafts are easier to review, sign, and audit than a bundled draft with intermixed period-N sources. Bundling is a §12 Uploader concern (package assembly), not a §14 Report Generator concern (drafting).

**Surfaced at Audit #1 OQ-REPORT-BUNDLING-DEFAULT for operator confirmation.**

# §14.13 Test matrix (~28 tests at v0.2 first ship)

`tests/tracks/report_mode/skeleton_tests.py` ships 12 skeleton tests that verify the LOCKED-but-skeleton substrate: track registration in §5 v8 dispatcher, predicate-body NotImplementedError stubs, AST-lint passes, frozen-dataclass discipline. Full per-sub-section tests + per-gate tests + classification-routing tests + CIC × CLC regression land in WS-J Code phase dispatch.

## §14.13.1 Track registration tests (3)

- `test_report_mode_dispatchable_at_v0_2` — at `TILTH_VERSION_FAMILY = "v0.2"`, `dispatch_track(registry, "report", report_runner=run_report_pipeline)` returns the runner result
- `test_report_mode_refused_at_v0_1_via_shippable_gate` — at `TILTH_VERSION_FAMILY = "v0.1"`, `dispatch_track(registry, "report", ...)` raises `TrackNotShippable`
- `test_report_mode_dispatch_without_report_runner_fails_closed` — `dispatch_track(registry, "report")` without `report_runner` argument raises `TrackShapeUnimplemented`

## §14.13.2 Schema discipline tests (4)

- `test_report_generator_run_input_frozen` — `ReportGeneratorRunInput(...)` instances are `frozen=True`
- `test_grant_report_bundle_frozen` — `GrantReportBundle(...)` instances are `frozen=True`
- `test_claim_evidence_map_pydantic_validation` — `ClaimEvidenceMap.parse_yaml(...)` validates schema shape
- `test_proposal_commitments_promoted_filter` — composer respects `status: PROMOTED` filter; PENDING_OPERATOR_REVIEW rows excluded

## §14.13.3 Gate predicate skeleton tests (5)

- `test_f_report_commitment_untraced_predicate_raises_not_implemented_at_v1_lock`
- `test_f_report_commitment_missed_predicate_raises_not_implemented_at_v1_lock`
- `test_f_report_out_of_scope_drift_predicate_raises_not_implemented_at_v1_lock`
- `test_f_report_numeric_drift_predicate_raises_not_implemented_at_v1_lock`
- `test_f_report_template_mismatch_predicate_raises_not_implemented_at_v1_lock`

## §14.13.4 AST-lint tests (4 per Cycle 1 RT-3a closure)

- `test_r_report_no_auto_finalize_lint_clean` — `R-REPORT-NO-AUTO-FINALIZE` AST-lint runs clean against the report_mode track + composer modules
- `test_r_report_no_out_of_scope_claim_lint_clean` — `R-REPORT-NO-OUT-OF-SCOPE-CLAIM` AST-lint runs clean against per-sub-section prompt templates
- `test_r_report_vault_intent_required_lint_clean` — `R-REPORT-VAULT-INTENT-REQUIRED` AST-lint runs clean against the read-substrate access in the composer modules
- `test_r_report_decimal_mandate_lint_clean` (NEW per Cycle 1 RT-3a closure) — `R-REPORT-DECIMAL-MANDATE` AST-lint runs clean against `pipeline/logician/gates/f_report_*.py` modules; rejects float() casts + float-literal arithmetic + `==` comparisons without preceding `isinstance(..., Decimal)` assert

## §14.13.5 Sub-section prompt template integrity tests (5)

- `test_narrative_prompt_template_present_and_parseable`
- `test_metrics_table_prompt_template_present_and_parseable`
- `test_financial_summary_prompt_template_present_and_parseable`
- `test_photo_gallery_prompt_template_present_and_parseable`
- `test_beneficiary_section_prompt_template_present_and_parseable`

## §14.13.6 Rubric integrity tests (2)

- `test_proposal_commitments_rubric_present_and_canonical_json` — rubric JSON file exists, parses, sort_keys=True
- `test_proposal_commitments_rubric_no_cic_clc_binding` — rubric scoring criteria contain no CIC→CLC subset binding (per v7.0.8 F-CIC-CLC-COUPLING-VIOLATION)

## §14.13.7 Red-team probe template integrity tests (5)

- `test_narrative_red_team_probe_template_present_and_parseable`
- `test_metrics_table_red_team_probe_template_present_and_parseable`
- `test_financial_summary_red_team_probe_template_present_and_parseable`
- `test_photo_gallery_red_team_probe_template_present_and_parseable`
- `test_beneficiary_section_red_team_probe_template_present_and_parseable`

## §14.13.8 Code-phase test surface (out-of-scope at LOCK; in-scope at WS-J Code phase)

The full per-sub-section round-trip tests (Scribe → Editor → Judge → Red Team → Logician), per-gate fire tests on adversarial inputs, Boundary-Drift detection tests, Numeric-Drift detection tests, Commitment-Missed detection tests, Template-Mismatch detection tests, classification-routing tests (Scribe Public+Shareable; Editor/Red Team/Judge post-fill always-local), and CIC × CLC orthogonality regression (84-test baseline applied to report_mode templates + rubric) ship at WS-J Code phase dispatch — NOT at this v1 LOCK. Skeleton tests at LOCK protect the substrate against contributor-introduced auto-finalize / scope-drift / vault-intent-bypass via AST-lint; full behavioral tests realize the gates' predicate bodies.

# §14.14 Open Questions for Audit #1

Surfaced for cross-family probe + operator confirmation. Defaults stand unless cross-family Audit surfaces structural conflict.

| OQ | Default | Audit #1 surface |
|---|---|---|
| OQ-REPORT-TREND-GEAR | Sparring Partner posture for trend-narrative authoring (NOT Co-Pilot default) | Operator confirmation surface — deviates from default Co-Pilot gear; Editor probe whether the deviation reads clearly |
| OQ-REPORT-XPERIOD-DEFAULT | Re-prove from period-(N-1) operational data per claim (fail-closed) | Operator confirmation surface; Red Team probe whether re-prove discipline closes second-order trace fragility |
| OQ-REPORT-RUBRIC-DEFAULT | Funder published rubric first; proposal_commitments rubric second (per `feedback_judge_rubric_strategy.md`) | Operator confirmation surface; Judge probe whether the cross-check pattern is correctly specified |
| OQ-REPORT-BUNDLING-DEFAULT | Separate drafts per period; operator-bundled at §12 Uploader if funder requires | Operator confirmation surface; Editor probe whether the operator-decision surface reads clearly |
| OQ-REPORT-HEAVY-JUDGE-DEFAULT | High-stakes report flagged via per-report SP0 → on-demand heavy-Judge swap | Audit #1 surface — what makes a report "high-stakes"? Federal long-form? Award size threshold? Operator decides per-report; per-report SP0 flag itself is `confidential` per v7.0.7 §4.1 |
| OQ-REPORT-CLAIM-SIGNING-GRAIN | Single-map signing (operator signs entire claim_evidence_map.yaml) at v0.2 first ship; per-claim signing as v1.x candidate | Audit #1 surface — operator confirmation that single-map signing is sufficient for v0.2 (per-claim signing at scale may be operationally heavier than warranted) |
| OQ-REPORT-WORKSPACE-PUBLISHED-TEMPLATE-ABSENT | F-REPORT-TEMPLATE-MISMATCH downgrades to ADVISORY when funder's published template absent | Red Team probe — could a malicious operator suppress F-REPORT-TEMPLATE-MISMATCH by deleting the workspace-shared published template? Mitigation: workspace-shared substrate is operator-owned but Ed25519-signed by SN-LLC at first wave (per v7.0.7 §6.1 router-template-update pattern); deletion of a signed file is detectable via lock_history audit |
| OQ-REPORT-OPERATIONAL-DATA-VS-KFR-CANONICAL | Surface BOTH operational-data value AND KFR value to operator with "which is canonical?" decision surface (per F-REPORT-NUMERIC-DRIFT.operational_data_value_drift_from_kfr sub-tag) | Audit #1 surface — composes with §13 v1 F-DATACOLLECTOR-KFR-DRIFT advisory; operator-decision surface for which canonical value to ship in the report |
| OQ-REPORT-FOUNDANT-SUBMITTABLE-FLUXX | Path-b §12 Uploader adapters (Foundant / Submittable / Fluxx) deferred per §12 v1 §12.10.5; Report Generator drafts ARE compatible with Path-b adapters when those land | Audit #1 surface — confirm no v0.2 first-ship Report Generator dependency on Path-b adapter substrate |
| OQ-REPORT-CROSS-PERIOD-ORG-ISOLATION | Cross-period claim reuse (per §14.12.1) is per-org-per-grant; cross-org cross-period claim reuse is FORBIDDEN per Law 3 | Audit #1 surface — Red Team probe whether cross-period claim reuse code path correctly enforces per-org-per-grant scope (no cross-org leak via period-(N-1) signed claim_evidence_map cross-org consumption) |
| OQ-REPORT-PHOTO-CONSENT-TIER-FLOOR | `internal_only` consent tier excludes photo from gallery; advisory-vs-fail-closed disposition | Audit #1 surface — should F-REPORT-OUT-OF-SCOPE-DRIFT.photo_consent_tier_violation be ADVISORY (Scribe excludes photo + surfaces "X photos excluded due to consent_tier"; operator may override for specific photos with operator-signed override) OR fail-closed (Scribe refuses to draft if Scribe's draft text references the excluded photo)? Default at v0.2: fail-closed |

# §14.15 Law map / Non-ownership / Closure

## §14.15.1 Law map (per §14.2)

(Per §14.2 enforcement table.)

## §14.15.2 Non-ownership

§14 v1 amendment does NOT own:

- §5 v8 dispatcher contract (owned by §5 v8; v14 binds the report row's pipeline_shape via §5 v8 §4.16 DI seam).
- §6.7 host-schema definition (owned by §6 Operating Envelope; v14 inherits the schema via the report row).
- The on-disk `router.yaml` `report` row content (authored at §5 v8 LOCK; v14 realizes the prompt templates + rubric + probes at the on-disk paths declared in the row).
- §11 v1 proposal_commitments.yaml schema (owned by §11; v14 reads via PROMOTED-status filter).
- §13 v1 operational-data sub-kind schemas (owned by §2 v7.2 + §13; v14 reads via Cedar-policy-gated read intents).
- §15 v1 cross-org leak gate-family (owned by §15; v14 mirrors the three-layer-detection shape for F-REPORT-OUT-OF-SCOPE-DRIFT).
- §0.5 Interface Index row format (owned by §0.5; v14 paired-commit appends rows).
- The F-PIPELINE-TRACK-FROZEN architectural PRE-gate (owned by architecture v7 §R.PF1; re-fires at v14 LOCK to confirm v8 + v14 invariants preserved).

## §14.15.3 Closure

§14 v1 LANDS the report_mode track activation. v0.2 ships:

- **5 sub-sections** at first ship (narrative + metrics_table + financial_summary + photo_gallery + beneficiary_section)
- **5 F-REPORT-* gates** activating from §4 v2.x §5.1 HORIZON to live PRE/POST positions
- **1 new pipeline_shape** (`prior_commitments_to_council_to_signed_report`) admitted to §5 v8 `_V0_1_IMPLEMENTED_SHAPES`
- **5 sub-section prompt templates** at `skills/scribe-ghostwriter/report_mode_prompts/`
- **5 sub-section red-team probe templates** at `skills/red-team/report_mode_probes/`
- **1 proposal-commitments rubric** at `skills/judge-rubric/proposal_commitments_rubric.json`
- **2 module skeletons** (`pipeline/orchestrator/tracks/report_mode.py` + `pipeline/orchestrator/seats/report_generator/__init__.py`) with proposes-only AST-lint discipline
- **~28 skeleton tests** at `tests/tracks/report_mode/skeleton_tests.py`
- **1 §0.5 v16 paired amendment** with ~17 rows (range 379-395)

Code-phase realization (per WS-J Code phase follow-on dispatch) wires per-sub-section composers + gate predicate bodies + claim-evidence-map signer + Cedar engine-bootstrap + the full ~80-test behavioral suite. v0.2 first ship is SPEC + skeleton + AST-lint discipline; v0.2 production is SPEC + Code + test surface green.

R.PF1 honored: NO new §3 module per track (the per-sub-section composers live inside the §14 owned `report_generator/` subdir, NOT as a §3 module addition); NO new §4.N mechanism per track (§4.16 dispatcher is the unchanged orchestration mechanism; §14 binds via the DI seam); NO new track-by-name literal in any `pipeline/loop/run_*.py` (§7.19 invariant preserved).

# §14.16 Compound-commit interaction (v0.1 architectural invariant)

Per `pipeline/engineering/spec_cards/compound_commit.md` and §2 v7.1 §4.10.7, the LOCK of §14 v1 is itself a compound transaction:

`{section_14_report_generator.md, section_00_5_section_14_report_generator_amendment.md, [optional: section_04_v2_x_1_amendment.md follow-on if F-REPORT-* family activation requires sub-tag additions per Cycle 1+2 surface]}`

MUST commit atomically via the §2 vault dispatcher's `commit_compound_txn()` entry point with `kind = blueprint_amendment_compound`.

Hash-binding rule per §4.11 predicate: the §0.5 v16 amendment's `section_14_v1_anchor_hash` field MUST equal SHA-3-512(§14 v1 file bytes). The §0.5 amendment lands at LOCK as the paired commit (~17 rows: 1 marker + 6 schema + 5 failure-code + 3 pre-gate-check + 2 post-gate-check; range 379-395).

Companion files at LOCK:
- `pipeline/blueprint/v0.1/section_00_5_section_14_report_generator_amendment.md` (paired §0.5 v16 amendment)
- `pipeline/orchestrator/tracks/report_mode.py` (track-dispatch entry + DI seam extension)
- `pipeline/orchestrator/seats/report_generator/__init__.py` (sub-section composer module skeleton)
- `skills/scribe-ghostwriter/report_mode_prompts/{narrative,metrics_table,financial_summary,photo_gallery,beneficiary_section}.md` (5 prompt templates)
- `skills/judge-rubric/proposal_commitments_rubric.json` (proposal-commitments rubric)
- `skills/red-team/report_mode_probes/{narrative,metrics_table,financial_summary,photo_gallery,beneficiary_section}.md` (5 red-team probes)
- `tests/tracks/report_mode/__init__.py` + `skeleton_tests.py` (28 skeleton tests)
- `orgs/_TEMPLATE/vault/grants/_TEMPLATE/reports/.gitkeep` + `reporting_template.yaml.example` (per-grant scaffold)

# §14.17 What Audit #1 must verify (Cowork Thesis phase)

Per `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-J Cowork phase: L-005 two-audit cycle, cross-family per WS-D (osascript → openclaw bridge; Editor on Llama 3.3 70B; Judge on Gemini 2.5 Pro; Red Team on GPT-OSS 120B).

The audit rubric for §14:

1. **Track-binding correctness against §5 v8 §4.16 dispatcher contract.** Verify the DI seam extension reads correctly: `_V0_1_IMPLEMENTED_SHAPES` extends from 2 → 3; new `report_runner` argument added to `dispatch_track`; the if/elif chain admits `prior_commitments_to_council_to_signed_report`; runtime-rebind sentinel preserved.
2. **F-REPORT-* gate family completeness.** Verify the five F-REPORT-* codes cover the load-bearing failure surfaces: untraced claims (Law 1 + 5); missed PROMOTED commitments (Law 1); out-of-scope drift (Law 2); numeric drift with Decimal mandate (Law 5 + v7.0.4-M1); template mismatch (Law 1 funder-fidelity).
3. **Cross-amendment composition correctness.** §14 sits atop 17 parent_locks. Does the spec correctly compose against each parent without contradiction? Specifically: v7.0.4-M1 Decimal mandate inheritance (F-REPORT-NUMERIC-DRIFT MUST use Decimal); v7.0.5 Funder Intel DB read for funder published rubric cross-check; v7.0.7 classification routing inheritance (Scribe cloud-routable Public+Shareable + opaque slot tokens; post-fill local); v7.0.8 CIC × CLC orthogonality on prompt templates + rubric + probes; §2 v7.2 operational-data sub-kind read with Cedar PII enforcement on beneficiary_records; §5 v8 track-registry binding via DI seam (no §5 re-architecture); §11 v1 proposal_commitments PROMOTED-status filter + content-hash binding; §12 v1 operator-approval pattern mirror; §13 v1 operational-data sub-kind read inheritance; §15 v1 three-layer-detection shape mirror.
4. **Sub-section composition correctness.** 5 sub-sections cover the load-bearing report surfaces (narrative + metrics + financials + photos + beneficiaries); each has correct read-substrate scope; each has correct claim-evidence-map authoring discipline; each has correct Cedar PII enforcement (specifically beneficiary_section).
5. **Claim-evidence-map signing correctness.** Single-map signing at v0.2 first ship; per-claim signing as v1.x candidate; operator-Ed25519 signature over canonical-JSON; re-read of source values + content hashes at finalize time (catches operational-data drift between author time and operator-sign time).
6. **Operator approval surface usability.** Operator reviews per-claim evidence trace + per-commitment fulfillment summary + classification routing summary + Cedar policy compliance summary; operator signs claim_evidence_map; system finalizes draft.
7. **Cross-period claim reuse + funder rubric cross-check + multi-period bundling defaults.** Three operator-decision surfaces; defaults read defensibly; operator override paths via per-report SP0 flag.
8. **Test matrix v1 coverage.** 28 skeleton tests partition: track registration (3) + schema discipline (4) + gate predicate skeleton (5) + AST-lint (3) + sub-section template integrity (5) + rubric integrity (2) + red-team probe integrity (5). Code-phase test surface (per-gate behavioral + classification-routing + CIC × CLC regression + per-sub-section round-trip) explicitly out-of-scope at LOCK.

# §14.18 Cycle 1 + Cycle 2 closure dispositions

Per L-005 strict two-cycle + row-170 transparent disposition pattern (mirrors §13 v1 §13.16 + §15 v1 + §11 v1 + WS-D v7.0.5 row 179 + WS-B v7.0.7 row 180 + WS-C-M1 v7.0.4-M1 row 190 + WS-K §15 rows 191/192 + WS-I §13 rows 196/197 precedents).

## §14.18.0 Cycle 1 dispatch outcomes

Audit trail at `pipeline/validation/blueprint_section_14_report_generator_2026-05-10/audit_v1_{editor,judge,red_team}.{md,raw.json}`.

- **Editor (Llama 3.3 70B / Groq, Meta family) — READY_TO_LOCK** with 8 findings (3 MED + 5 LOW): readability/clarity. No load-bearing structural issues; closures are stylistic enhancements deferred to future spin OR folded-in below.
- **Judge (Gemini 2.5 Pro / Google family) — READY_TO_LOCK 100/100** with zero findings. Cite: "This blueprint is exemplary. ... No fixes are required to proceed to LOCK." Judge surfaced no structural composition issues across all 10 rubric dimensions.
- **Red Team (GPT-OSS 120B / Groq, OpenAI-OSS family) — ESCALATE blocking:true** with 4 P0 + 6 HIGH + 9 MED + 3 LOW findings. Adversarial probe surfaced load-bearing semantic-validation + operator-override-without-signature + Decimal-mandate-not-enforced-at-predicate-skeleton + cross-section privacy-leak attack surfaces. Closures applied per the table below.

## §14.18.1 Cycle 1 closure disposition table

| RT-NN | Severity | Where | Disposition | Closure mechanism |
|---|---|---|---|---|
| **RT-1a** | P0 | §14.9.1 — F-REPORT-COMMITMENT-UNTRACED only verifies source EXISTENCE, not semantic ENTAILMENT (claim-text-supported-by-source) | **FOLDED-IN at LOCK** | §14.9.1 closure: per-claim source MUST contain the claim's load-bearing keywords/values verbatim where rendered (numeric: source_value matches claim_value EXACTLY in Decimal; narrative: at least one operational_data narrative_entries OR proposal_commitments source whose `text` field contains the claim's content-bearing N-gram per a `runtime_entailment_check` predicate added to F-REPORT-COMMITMENT-UNTRACED predicate body in WS-J Code phase). Predicate body specification extended at §14.9.1 to require entailment-or-exact-match per claim_kind. v0.2 first-ship Code-phase realization MUST implement this; defense-in-depth via Red Team probe template addition `report_mode_probes/narrative.md` probe area 1 already covers this surface. |
| **RT-1b** | MED | §14.9.1 — source-value-drift re-read happens AFTER operator sign | **FOLDED-IN at LOCK** | §14.5.0 + §14.9.1 closure: `pre_finalize_consolidated.v1` (row 391 of §0.5 v16) runs `F-REPORT-COMMITMENT-UNTRACED` source re-read BEFORE the operator-signature surface displays the draft for sign-off. Operator never sees a draft for sign-off where any source has drifted between Scribe author time and pre-finalize check time. The signature itself covers the draft + claim_evidence_map state at the moment of the pre_finalize check. |
| **RT-1c** | MED | §14.9.1 — KFR canonical drift atomic snapshot | **FOLDED-IN at LOCK** | §14.9.1 closure: KFR canonical reads use `vault_read_intent_kfr_atomic_snapshot` (per v7.0.4-M1 §2 atomic-read fcntl.flock + symlink rejection mandate); both Scribe author-time read AND pre_finalize re-read use the SAME atomic snapshot ID (snapshot ID is part of the claim_evidence_map.kfr source entry; pre_finalize fail-closes if the snapshot ID has been superseded). |
| **RT-2a** | HIGH | §14.9.2 — Judge vs Red-Team disagreement on "addressed" | **FOLDED-IN at LOCK** | §14.9.2 closure: "addressed" definition tightened — a PROMOTED commitment is "addressed" by the draft IFF (a) every entry in `evaluation_criteria` has at least one corresponding draft sentence/cell whose `claim_evidence_map` entry has a `commitment_id` link to this commitment AND (b) the draft section type matches the commitment's `required_sub_sections` requirement. Judge's per-commitment scan + Red Team's independent traversal MUST agree on "addressed"; ≥10pt scoring disagreement triggers council split per §10 v1 admin-risk register. |
| **RT-2b** | P0 | §14.9.2 — operator suppresses all commitments via "not due yet" without limit | **FOLDED-IN at LOCK** | §14.9.2 closure: F-REPORT-COMMITMENT-MISSED.commitment_period_n_not_due_yet sub-tag suppressions are now CAPPED at v0.2 first ship — operator may suppress at most `len(promoted_commitments) - 1` commitments per period (i.e., at least one commitment must be addressed; vacuous reports are structurally forbidden). Each suppression requires a per-commitment operator Ed25519 signature stored at `orgs/<slug>/vault/grants/<grant_id>/reports/period_<n>/commitment_waivers/<commitment_id>.signed.yaml` with `waiver_reason` + `waiver_signed_at_utc` + `waiver_signature` (Ed25519 over canonical-JSON of waiver_reason + commitment_id + period_n + run_id + waiver_signed_at_utc); F-REPORT-COMMITMENT-MISSED.commitment_waiver_unsigned fail-closes if any suppression lacks a valid signed waiver file. The waiver files are themselves audited via lock_history. |
| **RT-2c** | MED | §14.9.2 — operator "explicit reason logged" not cryptographically bound | **CLOSED via RT-2b closure** | The per-commitment signed waiver requirement (RT-2b) supersedes the free-form "explicit reason logged" pattern. All commitment waivers are now operator-signed Ed25519 + auditable. |
| **RT-3a** | P0 | §14.9.4 — Decimal mandate not enforced at predicate skeleton | **FOLDED-IN at LOCK** | §14.9.4 + §14.13.4 closure: NEW AST-lint rule **R-REPORT-DECIMAL-MANDATE** added at §14.13.4 (registered in `pipeline/linting/ast_lint.py` per WS-J Code phase). Rule rejects any `pipeline.logician.gates.f_report_*.py` module containing: (a) `float()` call inside the gate predicate body; (b) float-literal arithmetic (`0.5`, `1.0`, etc) in gate predicate body; (c) `==` comparison between values without a preceding `isinstance(..., Decimal)` assert. Defense-in-depth: gate predicate body's first executable statement at WS-J Code phase MUST be `assert all(isinstance(v, Decimal) for v in (...))` for every numeric-touching code path. Skeleton tests at §14.13.4 add a `test_r_report_decimal_mandate_lint_clean` slot reserved for WS-J Code phase realization. |
| **RT-3b** | HIGH | §14.9.4 — currency-rounding accumulation drift, no canonical rounding mode | **FOLDED-IN at LOCK** | §14.9.4 + §14.6.3 closure: canonical rounding mode is `decimal.ROUND_HALF_UP` (banker's rounding rejected per accounting-norm in funder financial reports). Variance computation: `variance_pct = (variance / budgeted * Decimal(100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`. Specified at §14.6.3 financial_summary composer + §14.9.4 numeric_drift gate + R-REPORT-DECIMAL-MANDATE AST-lint enforces uniform application. |
| **RT-3c** | MED | §14.9.4 — unit conversion factor float vs Decimal | **FOLDED-IN at LOCK** | §14.9.4 closure: unit conversion factors stored as canonical-JSON Decimal strings at `vault_shared/unit_conversion_factors.signed.yaml` (SN-LLC-signed per v7.0.7 §6.1 router-template-update pattern; PA/CA/FL/TX/NY first wave + standard SI conversions). Gate predicate body instantiates via `Decimal(factor_str)`; R-REPORT-DECIMAL-MANDATE AST-lint rejects any `float(factor)` cast in unit conversion code paths. |
| **RT-4a** | HIGH | §14.12.1 — SP0 flag operator-override not signed | **FOLDED-IN at LOCK** | §14.12.1 closure: SP0 flag `accept_signed_prior_period_claim_evidence_map` is now stored in a per-report signed configuration record at `orgs/<slug>/vault/grants/<grant_id>/reports/period_<n>/sp0_flags.signed.yaml` (Ed25519 over canonical-JSON of all flag fields + period_n + grant_id + org_slug + signed_at_utc). Gate fail-closes if the flag is True without a valid signature; operator must explicitly sign the flag activation per-period. F-REPORT-COMMITMENT-UNTRACED.cross_period_signature_invalid sub-tag added to enforce. |
| **RT-4b** | MED | §14.12.1 — cross-org leak through prior-period map | **FOLDED-IN at LOCK** | §14.12.1 closure: when SP0 flag is active and Scribe consumes period-(N-1) signed claim_evidence_map, the consumer code path MUST re-validate Org-Isolation per source — every source in the prior-period map MUST resolve under the current report's `orgs/<org_slug>/`. F-REPORT-OUT-OF-SCOPE-DRIFT.cross_org sub-tag fires on any cross-org source in the imported map; failure terminates the period-N report dispatch. |
| **RT-4c** | LOW | §14.12.1 — verbatim narrative reuse not detected | **BOUNDED-by-v1.x** | Duplicate-sentence detector (MinHash or similar) is a v1.x candidate; v0.2 first ship relies on operator review + Editor's "ungrounded narrative" probe per `report_mode_probes/narrative.md` probe area 4. Surfaced at §14.14 as new OQ-REPORT-VERBATIM-REUSE-DETECTION (v1.x). |
| **RT-5a** | HIGH | §14.9.5 — workspace-published template deletion downgrades to ADVISORY | **FOLDED-IN at LOCK** | §14.9.5 closure: F-REPORT-TEMPLATE-MISMATCH.workspace_published_template_absent now FAIL-CLOSED when the funder_id is in SN-LLC's first-wave funder set (operator-confirmed at white-glove via `vault_shared/funder_intelligence/<funder_id>/sn_llc_first_wave.signed.yaml` SN-LLC-signed marker file). For non-first-wave funders, downgrade to ADVISORY remains. SN-LLC ships the first-wave marker for VAPG / NIFA / SARE / EPA NEETP / SBIR at v0.2 first wave per the §13 v1 state-rules-card precedent. The marker file's hash is bound to the lock_history immutable ledger so deletion is auditable + detectable. |
| **RT-5b** | MED | §14.9.5 — operator key rotation protocol unspecified | **FOLDED-IN at LOCK** | §14.9.5 closure: operator-key rotation follows v7.0.7 §6.1 Trust-On-First-Use rotation pattern — new operator public key MUST be co-signed by the previous operator key, audited via lock_history. `operator_key_version` field added to `reporting_template.yaml` schema; F-REPORT-TEMPLATE-MISMATCH.operator_key_version_mismatch sub-tag fires if the template was signed with a key version that doesn't match the currently-pinned operator key OR the predecessor key whose rotation is auditable. |
| **RT-5c** | LOW | §14.9.5 — period-cadence consistency check | **FOLDED-IN at LOCK** | §14.9.5 closure: `F-REPORT-TEMPLATE-MISMATCH.period_cadence_actual_drift` sub-tag added — at PRE-pre-track-dispatch, the gate cross-checks `required_period_cadence` against the actual period_n interval derived from the grant's `award_signed_at_utc` (per §11 v1 AWARD_INGEST). Discrepancy triggers operator-decision surface ("template requires quarterly; this is period N which spans M months — confirm cadence"). |
| **RT-6a** | HIGH | §14.6.5 — indirect identification via aggregate-of-1 | **FOLDED-IN at LOCK** | §14.6.5 closure: F-REPORT-OUT-OF-SCOPE-DRIFT.beneficiary_aggregate_identifying sub-tag added — beneficiary_section composer's aggregate-count claims that reference a count of ≤2 beneficiaries trigger a HIGH advisory surfacing to operator ("aggregate count of 1 may de-anonymize this beneficiary; consent_tier verification required even for aggregate inclusion"). Operator MUST explicitly approve aggregate inclusion via per-beneficiary-aggregate Ed25519 signature when count ≤ 2. |
| **RT-6b** | MED | §14.6.5 — Cedar engine readiness check at module init only | **FOLDED-IN at LOCK** | §14.6.5 closure: Cedar engine readiness check moved from module-init to PER-READ — every operational-data sub-kind read invocation re-checks Cedar engine readiness via `cedar_engine.assert_ready()` predicate. Engine failure → fail-closed F-CEDAR-OPERATIONAL-DENIED.engine_unready at the read point (mirrors §13 v1 RT-C2-04 closure pattern: CriticalPolicyError(BaseException) propagation). |
| **RT-6c** | MED | §14.6.5 — post-collection consent-tier downgrade | **FOLDED-IN at LOCK** | §14.6.5 closure: beneficiary_records carry `consent_tier_history` field per §13 v1 schema extension (per-tier-change Ed25519 operator signature; rejected if tier downgraded after `created_at_utc` without a signed downgrade event). Report Generator's read path checks the tier history at every read; if any post-collection downgrade is unsigned, F-CEDAR-PII-CONSENT-MISSING.tier_history_unsigned fail-closes. |
| **RT-7a** | HIGH | §14.6.4 — narrative mentions internal_only photo (cross-section privacy leak) | **FOLDED-IN at LOCK** | §14.6.4 + §14.6.1 closure: NEW cross-section privacy audit added to PRE-pre-finalize gate — scans ALL draft sub-sections for textual references to any photo_id whose consent_tier is internal_only OR funder_only-when-section-is-not-photo_gallery. F-REPORT-OUT-OF-SCOPE-DRIFT.photo_consent_tier_violation extends with `.cross_section_reference` sub-tag. Predicate body spec'd at §14.9.3 closure update. |
| **RT-7b** | MED | §14.5.1 — caption-bytes substitution post-Scribe | **FOLDED-IN at LOCK** | §14.5.1 closure: caption text in draft markdown is hashed via the `draft_content_sha3_512` field at the claim_evidence_map level (already covers full draft including captions). Additional defense-in-depth: per-photo `claim_evidence_map` entry now includes `caption_text_sha3_512` field (hash of just the caption text, separate from photo bytes hash). At pre-finalize, BOTH caption hash + photo bytes hash are re-checked. Mismatch on either → F-REPORT-COMMITMENT-UNTRACED.source_content_drift fail-closes. |
| **RT-8a** | MED | §14.5.1 — all-or-nothing single-map signing pressure | **BOUNDED-by-v1.x** | Per-claim signing v1.x candidate per §14.OQ-REPORT-CLAIM-SIGNING-GRAIN. v0.2 first ship retains single-map signing with operator's ability to reject the whole draft + force Scribe re-cycle. Operator burden vs auditability trade-off acknowledged; v1.x revisits when at-scale operational evidence accumulates. |
| **RT-8b** | HIGH | §14.5.1 — post-sign draft mutation | **FOLDED-IN at LOCK** | §14.5.0 + §14.5.1 + §14.16 closure: NEW post-sign immutability discipline — at the moment operator signs the claim_evidence_map, the corresponding `draft_<v>.md` file is `flock(LOCK_EX | LOCK_NB)` write-locked AND the file mode is changed to read-only via `chmod 0444`. Any subsequent modification raises `BlueprintImmutableError` (CriticalPolicyError subclass per §13 v1 RT-C2-04 pattern). UI guard at the operator-approval surface disables "Edit Draft" button once the signature is applied. F-REPORT-COMMITMENT-UNTRACED.draft_post_sign_mutation_attempt sub-tag added; fail-closed at finalize re-read. |
| **RT-8c** | LOW | §14.5.1 — future per-claim signing migration path | **FOLDED-IN at LOCK** | §14.5.1 closure: claim_evidence_map schema now includes `claim_evidence_map_version: "v0.2_first_ship_single_map_signing"` field (immutable per-map). Future v1.x per-claim-signing schema bump → `claim_evidence_map_version: "v1_x_per_claim_signing"`. Backward compatibility shim per OQ-REPORT-CLAIM-SIGNING-GRAIN at v1.x. |
| **RT-9a** | MED | §14.16 — per-claim evidence trace UI granularity | **FOLDED-IN at LOCK** | §14.16 closure: NEW minimum UI surface spec — operator-approval UI MUST display a per-claim tabular view listing every `claim_id` + `claim_text` (truncated to 200 chars) + per-source (kind, path, hash, source_value) + a one-click "verify" button that re-computes the source content hash + value at click time + displays match/mismatch. Aggregate counts ("57 of 57 claims traced") are SUPPLEMENTARY only, not the primary surface. UI spec lives at `pipeline/orchestrator/seats/report_generator/ui_spec.md` (Code-phase deliverable). |
| **RT-9b** | MED | §14.16 — commitment-waiver justification visibility | **CLOSED via RT-2b closure** | The per-commitment signed waiver requirement (RT-2b) requires the operator to sign each waiver explicitly per `<commitment_id>.signed.yaml` file. UI surface displays the waiver_reason text alongside each waived commitment in the per-commitment-fulfillment summary panel. |
| **RT-9c** | LOW | §14.16 — classification-routing summary opacity | **FOLDED-IN at LOCK** | §14.16 closure: classification-routing summary panel MUST display per-sub-section routing badge (Cloud-routed Scribe with opaque slot count + slot-fill local + post-fill local Editor / Red Team / Judge). Operator can verify at a glance that no Confidential payload traversed cloud routing. |
| **RT-10a** | MED | §14.9.0 — short-circuit ordering masks later failures | **FOLDED-IN at LOCK** | §14.9.0 closure: PRE-pre-track-dispatch consolidated check now RUNS ALL FOUR gates regardless of early failures + collects ALL fired sub-tags into a list. Dispatcher aborts the pipeline after collecting; operator receives comprehensive diagnostic set. The previous "first-fired-returns" semantics is reversed — all-fail-collect is more diagnostic + more operator-actionable. |
| **RT-10b** | LOW | §14.9.0 — operator overload vs actionable feedback | **CLOSED via RT-10a closure** | Run-all-collect-all (RT-10a) provides comprehensive diagnostic set; operator UI can rank failures by severity (P0 → HIGH → MED) for actionable prioritization. |
| **E-01..E-08** | MED/LOW | various — Editor stylistic clarity findings | **PARTIAL: stylistic deferred to future spin** | Editor findings E-01 through E-08 are readability/clarity enhancements (diagrams, tables, summary headings). Per row-170 transparent disposition: stylistic enhancements deferred to v1.x readability spin; do NOT block LOCK. Substance-level structural composition is READY_TO_LOCK per Editor's own verdict. |

## §14.18.2 Cycle 2 dispatch outcomes

Audit trail at `pipeline/validation/blueprint_section_14_report_generator_2026-05-10/audit_v2_{editor,judge,red_team}.{md,raw.json}`. Dispatched 2026-05-10T23:27Z via cross-family bridge (osascript → openclaw → gateway).

- **Editor (Llama 3.3 70B / Groq, Meta family) — READY_TO_LOCK** with 3 NEW stylistic findings (E-NF-01..E-NF-03; all MED/LOW readability advisories; non-blocking). Closure status of Cycle 1 findings: E-01 CLOSED, E-02 PARTIAL, E-03 CLOSED, E-04 CLOSED, E-05 PARTIAL, E-06 PARTIAL, E-07 PARTIAL, E-08 CLOSED.
- **Judge (Gemini 2.5 Pro / Google family) — READY_TO_LOCK 100/100** (maintained from Cycle 1). Per-dimension scores all 10/10; explicit deltas noted for each strengthened-by-Cycle-1-closure dimension. "My Cycle 1 assessment of this blueprint as 'exemplary' is reaffirmed. ... No further fixes are required to proceed to LOCK."
- **Red Team (GPT-OSS 120B / Groq, OpenAI-OSS family) — REQUIRES_FIXES blocking:true** with all 28 Cycle 1 findings verified CLOSED + 10 NEW probes (RT-C2-01..RT-C2-10) at P0-1 / HIGH-3 / MED-5 / LOW-1 severity. Per L-005 strict two-cycle + row-170 transparent disposition pattern (mirrors §13 v1 + §15 v1 + WS-D v7.0.5 row 179 + WS-B v7.0.7 row 180 + WS-C-M1 v7.0.4-M1 row 190 precedents): Cycle 2 NEW probes are FOLDED-IN at LOCK with explicit text-level mechanism specifications. NO Cycle 3.

## §14.18.3 Cycle 2 NEW probe disposition table (RT-C2-01..RT-C2-10)

| RT-C2-NN | Severity | Where | Disposition | Closure mechanism |
|---|---|---|---|---|
| **RT-C2-01** | P0 | §14.13.4 + §14.9.4 — R-REPORT-DECIMAL-MANDATE AST-lint scope too narrow (only `pipeline.logician.gates.f_report_*.py`); composer modules can introduce float arithmetic undetected | **FOLDED-IN at LOCK** | §14.13.4 + §14.9.4 closure: R-REPORT-DECIMAL-MANDATE AST-lint scope EXTENDED to cover ALL Python modules under `pipeline/orchestrator/seats/report_generator/` AND `pipeline/orchestrator/tracks/report_mode.py` (any code path that may perform numeric arithmetic for report generation). New skeleton test `test_r_report_decimal_mandate_lint_clean_composer_scope` reserved for WS-J Code phase verifying composer modules are in lint scope. The existing `test_r_report_decimal_mandate_lint_clean` test slot is augmented to cover the extended scope. |
| **RT-C2-02** | HIGH | §14.9.2 — commitment_id path-traversal in waiver file path construction | **FOLDED-IN at LOCK** | §14.9.2 closure: `commitment_id` MUST validate against safe-identifier regex `^[A-Z0-9_-]+$` (uppercase alphanumeric + underscore + hyphen; max 64 chars) BEFORE any filesystem operation OR proposal_commitments.yaml row admission via §11 v1 PROMOTED-status filter. New sub-tag `F-REPORT-COMMITMENT-MISSED.commitment_id_invalid_format` fail-closes at PRE-pre-track-dispatch. §11 v1 AWARD_INGEST extraction MUST sanitize commitment_id at extraction time per a paired §11 v1.1 follow-on update (referenced; not authored at this LOCK). v0.2 first-ship Path-traversal mitigation: `Path(waiver_dir).resolve() / f"{commitment_id}.signed.yaml"` with subsequent `Path.is_relative_to(vault_root)` check before write; F-REPORT-OUT-OF-SCOPE-DRIFT.cross_org sub-tag fires on any path-escape attempt. |
| **RT-C2-03** | MED | §14.9.3 — cross-section privacy audit only checks photo_id mentions; narrative may mention beneficiary_id by name for beneficiaries whose consent_tier disallows narrative | **FOLDED-IN at LOCK** | §14.9.3 + §14.6.1 closure: NEW gate `F-REPORT-BENEFICIARY-PRIVACY-LEAK` (sub-tag of F-REPORT-OUT-OF-SCOPE-DRIFT) added to PRE-pre-finalize gate. Runs deterministic NER scan over ALL narrative text (sub-sections narrative + adjustments + accomplishments + challenges + per-photo captions) + flags any match to a `beneficiary_id` whose consent_tier disallows narrative inclusion (`metrics-only` or `no-narrative` tiers). The NER scan uses the operational-data beneficiary_records `beneficiary_name` + `beneficiary_aliases` field union as the match dictionary. Skeleton at v0.2; full NER realization via deterministic Python (NOT LLM) in WS-J Code phase. |
| **RT-C2-04** | MED | §14.9.5 — first-wave marker hash binding to lock_history not enforced at runtime | **FOLDED-IN at LOCK** | §14.9.5 closure: F-REPORT-TEMPLATE-MISMATCH gate predicate body MUST read the marker's hash from a NEW lock_history-bound file `lock_history/first_wave_markers.signed.yaml` (SN-LLC-signed; immutable per lock_history append-only ledger) AND verify the on-disk `sn_llc_first_wave.signed.yaml` content + signature against that immutable record at every PRE-pre-track-dispatch. New sub-tag `.workspace_published_template_marker_tampered` fail-closes on hash mismatch. The lock_history file is part of the SN-LLC release ceremony (lock_history append at SN-LLC's signing site, NOT at the operator's deployment site). |
| **RT-C2-05** | HIGH | §14.9.5 — operator-key rotation Trust-On-First-Use vulnerable to compromised-previous-key co-sign attack | **FOLDED-IN at LOCK** | §14.9.5 closure: NEW gate `F-REPORT-OPERATOR-KEY-ROTATION-VALIDITY` added — checks the previous operator key's revocation status via a signed revocation list at `orgs/<slug>/operator_key_revocation_list.signed.yaml` (operator-Ed25519-signed; entries appended at revocation events). New rotation event REJECTED if previous key is on the revocation list. Sub-tags `.previous_key_revoked` + `.revocation_list_signature_invalid` fail-close. Operator MUST issue a revocation event BEFORE rotating to a new key; race-window is the operator's Ed25519-signed event ordering (revocation MUST precede new-key-co-sign in the lock_history immutable ledger). |
| **RT-C2-06** | MED | §14.6.5 — legacy beneficiary_records without `consent_tier_history` field | **FOLDED-IN at LOCK** | §14.6.5 closure: missing `consent_tier_history` field at read path explicitly FAIL-CLOSED via NEW sub-tag `F-CEDAR-PII-CONSENT-MISSING.tier_history_missing`. Migration shim available: operator may run `tilth migrate beneficiary_records --backfill-empty-history --signed-by <operator_key>` CLI to back-fill an empty signed history for legacy records (the back-fill itself is operator-Ed25519-signed + audited via lock_history; the empty history is initialized with the operational-data record's `created_at_utc` as the floor consent_tier-set event). v0.2 production-cut checklist includes the migration step; the gate is fail-closed by default to prevent legacy records from silently passing. |
| **RT-C2-07** | LOW | §14.9.0 — run-all-then-collect DoS risk on expensive gate evaluations | **BOUNDED-by-v1.x** | Performance-budget guard is a v1.x candidate per OQ-REPORT-GATE-PERFORMANCE-BUDGET (NEW). v0.2 first ship accepts the DoS risk because (a) gate count is fixed at 4; (b) typical Cedar policy check + KFR canonical re-read is sub-second; (c) operator-side dispatch is interactive (operator times out via UI rather than gate-side timeout). v1.x will add per-gate timeout + memory-budget guards if at-scale telemetry indicates need. |
| **RT-C2-08** | MED | §14.5.1 — caption-text hash boundary in Markdown unspecified | **FOLDED-IN at LOCK** | §14.5.1 + §14.6.4 closure: NEW caption extraction algorithm spec — after the image Markdown `![alt](path)` line, the *immediately following* italicized line (`*caption text*`) up to the next blank line OR the next non-italicized line is considered the caption. Whitespace normalization: strip leading/trailing whitespace + collapse internal runs of whitespace to a single space + normalize line-endings to LF + UTF-8 NFC normalize before hashing. Skeleton-test placeholder `test_caption_extraction_canonical_normalization` reserved for WS-J Code phase realization. |
| **RT-C2-09** | HIGH | §14.12.1 — prior-period map tamper-after-sign undetected at reuse | **FOLDED-IN at LOCK** | §14.12.1 closure: when SP0 flag `accept_signed_prior_period_claim_evidence_map: true` is active and Scribe consumes period-(N-1) signed claim_evidence_map, the consumer code path MUST re-hash the on-disk prior-period map AND verify the hash matches the prior-period bundle's `operator_signature` record (which itself includes a content_sha3_512 of the map at sign time). NEW sub-tag `F-REPORT-COMMITMENT-UNTRACED.prior_period_map_integrity_failure` fail-closes on hash mismatch. The prior-period bundle's operator_signature record lives at `orgs/<slug>/vault/grants/<grant_id>/reports/period_<n-1>/operator_signature.signed.yaml` (Ed25519 over canonical-JSON of bundle_state + claim_evidence_map_path + claim_evidence_map_content_sha3_512 + draft_path + draft_content_sha3_512 + finalized_at_utc); pre-existing per §14.5.0 GrantReportBundle schema. |
| **RT-C2-10** | MED | §14.9.1 — semantic-entailment N-gram heuristic fragile to legitimate paraphrasing | **FOLDED-IN at LOCK** | §14.9.1 closure: NEW deterministic-substring requirement option — for `claim_kind: narrative`, EITHER (a) the exact claim sentence (after whitespace + punctuation normalization) appears verbatim in at least one source `text` field, OR (b) the operator attaches an `editor_approved_paraphrase: true` flag to the claim_evidence_map entry (operator-Ed25519-signed; recorded as part of the per-claim source dict). New sub-tag `F-REPORT-COMMITMENT-UNTRACED.narrative_paraphrase_unflagged` fail-closes when neither condition (a) nor (b) holds. The N-gram heuristic from RT-1a closure is RETAINED as a heuristic-fallback for surfacing operator-decision-required cases (advisory at PRE; not fail-closed by itself); the verbatim-or-paraphrase-flag mechanism is the structural enforcement. |

## §14.18.4 Cycle 2 NEW Editor stylistic findings (E-NF-01..E-NF-03)

| E-NF-NN | Severity | Disposition |
|---|---|---|
| **E-NF-01** | LOW | PARTIAL: §14.18.1 closure-disposition table is large (28 rows). Bounded — table is the audit trail; readability addressed via column headers + per-row Cycle-RT-NN identifier. v1.x readability spin may convert to per-RT-finding heading-pair if at-scale operator review indicates need. |
| **E-NF-02** | LOW | PARTIAL: closure mechanism text density is the trade-off for completeness; addressed via inline-paragraph structure where applicable. v1.x may extract per-finding closure prose into per-RT-NN markdown subsections. |
| **E-NF-03** | LOW | PARTIAL: inline closure subheadings at §14.6.4 + §14.6.5 are navigational aids documenting the audit trail; deferred per v1.x readability spin. |

# End of §14 v1 SPEC (post-Cycle-2 fold-ins applied; status pending compound LOCK)
