---
title: Blueprint §11 Intake — KFR ingestion + AWARD_INGEST extraction (v1 SCOPING DRAFT)
filed: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 (v1 — L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor per WS-D v7.0.5 precedent — Editor=Llama-3.3-70B/Groq READY_TO_LOCK + Judge=Gemini-2.5-Pro/Google READY_TO_LOCK 100/100 + Red Team=GPT-OSS-120B/Groq PASS blocking:false). Cycle 1 surfaced 23 findings (1 P0 + 5 HIGH + 10 MED + 7 LOW) including 1 P0 from Red Team (RT-01); all closures applied across §11.0/§11.5.0/§11.6.0/§11.6.2/§11.7/§11.9.1/§11.9.2/§11.9.3/§11.9.7/§11.9.8/§11.9.9/§11.9.10/§11.9.11/§11.10/§11.11/§11.13. Cycle 2 verified all 23 closures CLOSED with zero new design concerns and zero new attack paths. Compound LOCK with `section_00_5_section_11_intake_amendment.md` per §6.17 Option-B paired-commit pattern.
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                      # v7 LOCKED 2026-04-19 — A1-A12
  - pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md                  # v7.0.4 LOCKED 2026-05-09 row 178 — KFR + SP0 + F-LOGICIAN-FACT-DRIFT family + Intake module spec (3 modes: BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST) + Benchmarks Register + F-EXTRACTOR-FABRICATION + F-EXTRACTOR-AWARD-SIGNATURE-INVALID
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md                  # v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intelligence DB + Match DB; Intake's local vector substrate (FAISS/Chroma + bge-large-en-v1.5) is the same family as Funder Intel DB indexing per v7.0.4 §5
  - pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md                  # v7.0.6 SELF-LOCKED 2026-05-09 row 176 + verified row 177 — Intake named as v0.1 support agent (always-local; KFR ingestion owner)
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                  # v7.0.7 LOCKED 2026-05-10 — classification-driven routing; Intake routing is always-local-by-default (Intake processes mixed-classification source docs and Confidential proposal artifacts; no subset is safely cloud-routable without per-file pre-classification UX); F-CLASS-NEW-FACT-UNCLASSIFIED defaults INCREMENTAL facts to confidential pending operator re-classification.
  - pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md                 # v7.0.10 LOCKED 2026-05-11 — Three-posture routing model (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign) supersedes the v7.0.7 four-posture-implicit framing at the customer-facing layer. Intake's always-local routing posture is unchanged at v7.0.10 (Intake is on the always-local agents list under all three customer-facing postures); per-field classification register stays at 4 values (public, shareable, confidential, operator_flagged). Classification Review step 3 + step 4 amended at v7.0.10 to add deployment-posture selection alongside per-field classification — Intake's Classification Review UI surfaces both the per-field 4-class register decisions AND the deployment-level 3-posture selection. F-CLASS-REGISTER-* gates carry sub-tag extensions for the posture-signature trail (`.posture_unsigned`, `.posture_invalid`, `.posture_hash_mismatch`); no new top-level F-CLASS-* gate added at v7.0.10 for the register-signature layer.
  - pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md                  # v7.0.8 LOCKED — CIC × CLC orthogonality; Intake schema and prompt templates carry F-CIC-CLC-COUPLING-VIOLATION audit at LOCK
  - pipeline/blueprint/v0.1/section_02_vault_topology.md                         # v7.1 LOCKED — Intake writes pending_facts queue + KFR via Vault-owned primitives; never raw open()
  - pipeline/blueprint/v0.1/section_04_logician.md                               # v2.x in flight — Intake's PRE-queue gate F-EXTRACTOR-FABRICATION + AWARD_INGEST signature gates registered via §4 v2.x amendment (WS-L); §11 is the authority on gate codes and exact-match semantics
  - pipeline/blueprint/v0.1/section_05_pipeline.md                               # v6 LOCKED — §5 SP0 invokes KFR query; Intake is the upstream that prevents drift from entering KFR (composes against F-LOGICIAN-FACT-DRIFT family at SP0)
  - pipeline/blueprint/v0.1/section_06_operating_envelope.md                     # v1-r1 LOCKED — vector store substrate sits under §6 envelope discipline (frozen at Golden Image per ADR-001)
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md               # §0.5 v5 LOCKED — Intake primitives row-append at paired §0.5 §11 amendment companion-file
prerequisite_interlock: pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md (v7.0.4 LOCKED 2026-05-09 row 178 — KFR schema + Intake module spec + AWARD_INGEST mode pre-LOCK addition + F-EXTRACTOR-FABRICATION exact-match semantics + F-EXTRACTOR-AWARD-SIGNATURE-INVALID two-track signature verification — all pinned in v7.0.4; §11 is the seat-lifecycle wrapper around that spec).
companion_module: pipeline/orchestrator/seats/intake.py (scaffold authored at §11 LOCK; mode dispatch + dataclass schemas + F-EXTRACTOR-FABRICATION predicate; full local-vector-store substrate + LLM extraction wired downstream by Code session per WS-E Code phase).
companion_amendment: pipeline/blueprint/v0.1/section_00_5_section_11_intake_amendment.md (paired-commit at §11 v1 LOCK per §6.17 Option-B).
downstream_siblings_out_of_scope: §13 Data Collector, §14 Report Generator (both v0.2 horizon — but both consume Intake outputs: WS-J Report Generator reads `proposal_commitments.yaml` produced by AWARD_INGEST; WS-I Data Collector cross-validates inbound numeric responses against KFR populated by BULK_INGEST + INCREMENTAL_INGEST).
ws_b_routing_dependency: WS-B v7.0.7 Thesis still in flight at §11 LOCK time. Per dispatch packet WS-E note: §11 ships with always-local routing posture per v7.0.7 SCOPING DRAFT. If WS-B LOCK changes the routing posture, §11 v1.0.1 amendment lands.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) per WS-D v7.0.5 LOCK precedent (lock_history row 179, 2026-05-10). Editor=groq/llama-3.3-70b-versatile (Meta family) + Judge=google/gemini-2.5-pro (Google family) + Red Team=groq/openai/gpt-oss-120b (OpenAI-OSS family) dispatched via openclaw infer model run --gateway across both Cycle 1 and Cycle 2. Three distinct non-Anthropic families. L-003 satisfied. Bridge pattern: Cowork → openclaw via mcp__Control_your_Mac__osascript with timeout of 600 seconds for Gemini Pro thinking-mode runs. Dispatch shell scripts cribbed from pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh. Audit trail at pipeline/validation/blueprint_section_11_intake_2026-05-10/.
cycle_1_changelog_2026_05_10:
  - "RT-01 (P0): §11.9.1 F-EXTRACTOR-FABRICATION extended with unique-page-match check — gate confirms source_quote first occurrence in document is on source_page; multi-page-match candidates flagged for manual review with explicit operator multiple_page_match=true tag."
  - "RT-02 (HIGH): §11.9.1 markdown line-bounding formal spec added — source_quote MUST be a single line in the raw file (no line-wrap concatenation); gate compares against raw line buffer."
  - "RT-03 (MED): §11.5.1 schema permits source_paragraph_id as alternative to source_page for DOCX (paragraph-index anchoring); §11.9.1 gate compares against paragraph text directly for DOCX sources."
  - "RT-04 (MED): §11.9.1 mode-tolerance hard-coded to AWARD_INGEST via immutable input-bundle dispatch (NOT readable from config); test in §11.13.2 confirms."
  - "RT-05 (HIGH): §11.4.3 + §11.9.2 — F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal sub-tag .hash_mismatch added; SignedClaimEvidenceMap MUST include SHA3-512 of submission artifact bytes; gate recomputes + compares (mirrors §12 Uploader F-UPLOADER-SIGNATURE-MISSING.hash_mismatch precedent)."
  - "RT-06 (HIGH): §11.9.3 tamper-evident attestation bypass — interactive prompt at CLI for --award-doc-unsigned-attestation; ledger-write-before-process discipline; bypass log via §2 Vault write intent."
  - "RT-07 (MED): §11.4 + §11.9.NEW — operator config Ed25519 signature requirement; F-INTAKE-CONFIG-SIGNATURE-INVALID gate."
  - "RT-08 (MED): §11.7 TTY check on tilth intake review --confirm-batch; --yes / --force are NOT v0.1 args."
  - "RT-09 (HIGH): §11.9.NEW + §11.10 — F-INTAKE-EMBEDDING-NS-MISMATCH gate; pre-tool guard asserts org_slug arg matches input dataclass org_slug for every Pydantic AI tool call against the local vector store."
  - "RT-10 (MED): §11.8 compound key for embedding storage — orgs/<slug>/vault/intake/embeddings/<org_slug>_<doc_hash>/; collision-detect guard."
  - "RT-11 (HIGH): §11.6.2 + §11.9.4 — TOCTOU-safe watcher; Path.resolve() + is_file() + not is_symlink() + os.O_NOFOLLOW; F-INTAKE-WATCHER-TOCTOU gate (or sub-tag of ORG-CROSS-REF; explode pattern preserved)."
  - "RT-12 (LOW): §11.9.7 periodic state-file sanity check at every run start (not just post-write)."
  - "RT-13 (MED): §11.10 sealed embedding endpoint to localhost or unix:// socket only; F-INTAKE-EMBEDDING-ENDPOINT-INVALID gate."
  - "RT-14 (LOW): §11.13 + §11.15 LOCK-time check — F-CIC-CLC-COUPLING-VIOLATION audit; static analysis confirms no overlap in CIC × CLC enumeration identifier space."
  - "RT-15 (MED): §11.6.2 watcher quarantines unsupported-format files at intake/quarantine/unsupported/."
  - "E-1 (MED): §11.6 three-mode summary table prepended."
  - "E-3 (MED): §11.5 schema delta table from v7.0.4 KFR conventions."
  - "E-4 (HIGH): §11.11 PROJECT_CONTEXT migration step-by-step explicit narrative; MIGRATION_BULK_INGEST dispatch behavior pinned."
  - "E-5 (MED): §11.0 preamble added with cross-amendment composition map."
  - "E-7 (MED): §11.13 tests added for new gates from Cycle 1 closures."
  - "Final §11.9 gate roster: 12 codes (was 8). §0.5 §11 amendment row count: 24 rows (was 18). Range claim adjusts from 233-250 to 233-256."
---

# §11.0 Cross-amendment composition map (per E-5 closure)

```
v7 LOCKED 2026-04-19 (A1-A12)
  ├─ v7.0.4 LOCKED 2026-05-09 row 178 — KFR + SP0 + F-LOGICIAN-FACT-DRIFT + Intake module spec (3 modes) + F-EXTRACTOR-FABRICATION exact-match + F-EXTRACTOR-AWARD-SIGNATURE-INVALID two-track + Benchmarks Register
  │    │
  │    └─→ §11 Intake (THIS) — seat-lifecycle wrapper around v7.0.4 §5 module spec; owns operator-review UX, mode dispatch, F-INTAKE-* family
  │
  ├─ v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intel DB + Match DB + Scout channel G + F-VECTOR-NS-MISMATCH discipline (binds §11.10 routing posture + §11.8 substrate)
  ├─ v7.0.6 SELF-LOCKED 2026-05-09 row 176 — Intake named v0.1 support agent + Archivist v1.x curation slot
  ├─ v7.0.7 SCOPING DRAFT — classification routing; §11.10 always-local hard-coded per SCOPING DRAFT (v1.0.1 amendment if WS-B LOCK changes posture)
  └─ v7.0.8 LOCKED — CIC × CLC orthogonality; §11 schemas + extraction prompt template audit clean at LOCK

§11 → companion edits at LOCK (compound paired-commit per §6.17 Option-B):
  ├─ §0.5 §11 amendment (24 rows; range 233-256 to avoid §12 collision)
  ├─ §4 v2.x amendment (registers F-EXTRACTOR-* + F-INTAKE-* gate family — Code session, parallel)
  ├─ orgs/_TEMPLATE/intake/ scaffold
  ├─ pipeline/orchestrator/seats/intake.py module skeleton
  └─ tests/seats/intake/skeleton_tests.py
```

# §11.1 Purpose and scope

Intake is the **KFR ingestion + AWARD_INGEST extraction** support agent of the Tilth pipeline. It is the upstream that prevents fabricated, untraced, or drift-prone facts from entering the Key Facts Register at all — and the agent that captures operator-confirmed proposal commitments at award acceptance for downstream Report Generator (§14, v0.2) consumption. Intake never writes the canonical KFR directly; it produces an operator-review queue with verbatim-quote-with-page provenance per candidate fact, and the operator confirms each entry before it promotes to the canonical register.

**v0.1 scope.** Three modes — operator-explicit at v0.1 (no daemon, no scheduler):

1. **BULK_INGEST** (white-glove onboarding) — operator drops a folder of org documents into `orgs/<slug>/intake/inbox/`, invokes Intake, Intake sweeps the folder, extracts candidate facts with verbatim-quote provenance, queues them in `orgs/<slug>/vault/kfr/pending_facts.yaml` for operator review.
2. **INCREMENTAL_INGEST** (continuous operations) — operator drops a single new document during operations, Intake processes it on arrival. Trigger is **filesystem watcher OR operator-explicit (both)** per §11.14 default — watcher fires on new files in `orgs/<slug>/intake/inbox/`; operator-explicit `tilth intake incremental --org <slug> --doc <path>` invocation also valid.
3. **AWARD_INGEST** (award acceptance, pre-LOCK addition per dispatch packet decision 8h default per v7.0.4 §5.3) — operator marks a submitted proposal as WON via `tilth intake award-ingest --org <slug> --grant <grant_id> --award-doc <path>`, Intake verifies operator + funder signatures on the submission artifact and award document, extracts `proposal_commitments.yaml` with verbatim-quote-from-won-proposal provenance, queues commitment rows for operator structuring before promotion.

**Out of scope for v0.1 (explicit non-goals).** Intake does NOT write KFR canonical entries directly (operator confirmation is the gate). Intake does NOT auto-promote pending_facts (the autopromote-by-confidence-threshold path per §11.14 default OQ-1 is operator-confirmed-batch, not silent-auto-write — see §11.7). Intake does NOT generate proposal text (Scribe, §7). Intake does NOT score, edit, or attack drafts (Judge, Editor, Red Team, §§9–10). Intake does NOT submit (Uploader, §12). Intake does NOT run grant cycles (§5 Pipeline). Intake does NOT collect post-award outcome data (Data Collector, §13, v0.2). Intake does NOT generate funder-ready reports (Report Generator, §14, v0.2). Intake does NOT curate the Funder Intelligence Database between cycles (Archivist, §15, v1.x).

**Substance comes from the operator's documents (Laws 1 + 5).** Every candidate fact has a `source_doc` + `source_page` + verbatim `source_quote`. The exact-match validator (F-EXTRACTOR-FABRICATION, §11.9.1) rejects any candidate whose quote does not literally appear in its source doc at its source page per the v7.0.4 §5.2 normalization discipline (Unicode NFC + whitespace normalization PASS; OCR-substitution + page-off-by-one + ellipsis-substring REJECTED). Intake fabricates nothing.

# §11.2 Five Operating Laws — enforcement mapping

Framework: per `pipeline/templates/component_analysis_template.md`

Each of the Five Laws is enforced by a combination of PRE-gates (Logician, before Intake processes), in-seat discipline (Intake's own extraction + queue contract), and PRE-pre-queue gates (Logician, before any candidate enters the operator-review surface). Failure codes are enumerated in §11.9.

**Law 1 — RFA is the source of truth.**
- BULK_INGEST + INCREMENTAL_INGEST: N/A — pre-RFA. Intake runs at white-glove onboarding (BULK) and at continuous-operations cadence (INCREMENTAL), both of which precede any specific RFA. KFR populated by Intake feeds SP0 KFR Freshness Review per v7.0.4 §3, where the RFA-required-fields list is the binding pull surface for facts.
- AWARD_INGEST: the won proposal IS the source-of-truth artifact. Every commitment row's `source_proposal_path` references the operator-signed `draft_<v>.md` that won the award, and `commitment_text` is verbatim from that draft. Pre-extraction verification (§11.9.2) refuses to extract from a proposal artifact whose operator signature does not verify per Section 4 §4.5 `verify_claim_evidence_map` discipline.
- In-seat: Intake's extraction LLM (small local Mistral 7B class — §11.8) is bounded to fact extraction from the source doc bytes; the LLM does NOT invent facts not present in the doc. F-EXTRACTOR-FABRICATION (§11.9.1) is the deterministic gate that catches any drift between extracted `source_quote` and actual source bytes.

**Law 2 — No boundary drift.**
- PRE-gate: Intake's scope is mechanically bounded — BULK_INGEST processes only files under `orgs/<slug>/intake/inbox/`; INCREMENTAL_INGEST processes only the operator-named single doc; AWARD_INGEST processes only the operator-named submission artifact + award document. No web search, no cross-grant reference, no content generation beyond fact extraction from the source.
- In-seat: Intake's extraction prompt is fixed (no operator-tunable prompt at v0.1; tunable only via §11.8 substrate amendment). The LLM is constrained by the prompt to produce `candidate_fact` rows in the v7.0.4 §5.1 schema; structured-output validation rejects any output that doesn't match.
- POST-pre-queue: Pydantic validation on every candidate before it reaches the queue file. Schema violation → reject + audit trail under `pipeline/validation/extractor_rejects/` per v7.0.4 §5.2 reject-with-audit-trail discipline.

**Law 3 — Org isolation.**
- PRE-gate: Intake operates on **exactly one** `orgs/<slug>/` subtree per invocation. The CLI takes `--org <slug>` as a required argument; the watcher (INCREMENTAL_INGEST) is per-org-bound (one watcher process per org or one watcher with per-org event filtering — both Code phase decisions). Cross-org input file paths are PRE-rejected with the same audit-trail discipline as F-UPLOADER-ORG-CROSS-REF.
- In-seat: Intake reads from exactly one `orgs/<slug>/intake/inbox/` and writes to exactly one `orgs/<slug>/vault/kfr/pending_facts.yaml` (BULK + INCREMENTAL) or one `orgs/<slug>/vault/grants/<grant_id>/proposal_commitments.yaml` (AWARD_INGEST). The vector store namespace is per-org-segmented per v7.0.5 F-VECTOR-NS-MISMATCH discipline (the org_slug is a tool-arg-validated parameter on every Pydantic AI tool call against the local vector store).
- POST-gate: every queue write is path-resolve-normalized; any path that resolves outside the declared `org_slug` subtree → hard-block with `F-INTAKE-ORG-CROSS-REF`. (New gate code introduced by §11; registered at §4 v2.x amendment per WS-L.)

**Law 4 — Apolitical sector language + admin-risk term scanning.**
- PRE-gate: Intake produces no narrative text — its outputs are structured candidate facts and commitment rows, not prose. The §7.11 admin-risk scanner (Scribe-side) does NOT fire on Intake outputs because there is no narrative for it to scan.
- In-seat: candidate facts and commitment rows include verbatim source quotes. If an operator's source document contains an admin-risk-flagged term, the verbatim quote preserves it without rewriting — Law 4 forbids silent rewriting of operator-authored material. The operator review surface (§11.7) displays the quote as-is; if the operator wants to flag the term, that's an operator action at promotion time, not an Intake action at extraction time.
- v1.1 horizon: when AWARD_INGEST extracts commitment text from won proposals, the `commitment_text` field carries the verbatim proposal language. The §7.11 admin-risk scanner could fire as an advisory POST-extract surface (catching cases where the won proposal carries language that is flagged in the current admin-risk register but was not flagged at the time of submission). NOT registered at v1; documented here for the v1.1 horizon the same way §12.2 Law 4 cell documents the §12 v1.1 attachment-text horizon.

**Law 5 — Applicant brings the substance.**
- PRE-gate (BULK + INCREMENTAL): the operator chooses which documents enter the inbox. Intake processes only what the operator places there. No web fetch, no automated ingestion of third-party or public-database content. The substance is operator-curated by the act of placing the file in `intake/inbox/`.
- PRE-gate (AWARD_INGEST): the operator explicitly invokes `tilth intake award-ingest` with the award-doc path. The submission artifact path is derived from the named `--grant <grant_id>` (resolved to `orgs/<slug>/vault/grants/<grant_id>/submission/draft_<v>.md`). Both inputs are operator-signed; signature verification is the structural gate (F-EXTRACTOR-AWARD-SIGNATURE-INVALID, §11.9.2 + §11.9.3).
- POST-pre-queue: F-EXTRACTOR-FABRICATION (§11.9.1) is the no-fabrication structural enforcement — any candidate whose quote does not match the source bytes at the source page per v7.0.4 §5.2 normalization is rejected pre-queue. The operator never sees a fabricated candidate.
- Promotion-time: every promoted KFR entry carries `validation.confirmed_by` (operator key id) and `validation.confirmed_when` (UTC timestamp) per v7.0.4 §1 schema. Operator confirmation is the load-bearing transition from candidate to canonical.

# §11.3 Four Autonomy Rules — enforcement mapping

**Rule 1 — Save state always.** Intake persists `IntakeState` to `orgs/<slug>/vault/kfr/intake_state/<run_id>.yaml` on every invocation — both success and failure. State includes: invocation timestamp, mode (BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST), input doc count + paths, candidate count produced, candidates rejected pre-queue (with rejection reason), queue path written, F-EXTRACTOR-FABRICATION rejects logged to `pipeline/validation/extractor_rejects/<run_id>/`, signature verification results (AWARD_INGEST only), failure reason if applicable.

**PRE-gate failure persistence.** When Intake is invoked but a PRE-gate (§11.9 PRE codes including org-isolation + signature verification + Pydantic-schema-violation) fails before extraction starts or mid-extraction, Intake writes `intake_state.yaml` with `assembly_succeeded=False, candidates_produced=0, failure_reason=<gate_code>, failure_detail=<predicate_message>`. No partial pending_facts.yaml is written; no proposal_commitments.yaml is written. The operator surface receives the gate-fail result with the same self-validation envelope as a successful run, just with `overall_status="extraction_failed"` and the failure code surfaced. This guarantees Rule 1 holds even when Intake never reaches the operator-review queue.

**Rule 2 — Test your own work.** Before marking the queue write "ready for operator review," Intake runs the readiness check (§11.7) — a deterministic self-validation pass that confirms: every candidate has source_doc + source_page + source_quote populated, every quote passes F-EXTRACTOR-FABRICATION exact-match validation, the queue file is Pydantic-schema-valid, the queue write succeeded under the §2 Vault write intent, the audit trail under `extractor_rejects/` is consistent with the candidate count math (candidates_emitted_to_LLM = candidates_in_queue + candidates_rejected). The readiness result is persisted alongside `intake_state.yaml`.

**Rule 3 — Be explicit.** Intake's input contract (§11.4) declares exact paths, modes, and done-definitions per mode. Intake's output contract (§11.5) declares exact output paths per mode (pending_facts.yaml for BULK/INCREMENTAL; proposal_commitments.yaml for AWARD_INGEST), schema, and operator-review surface format.

**Rule 4 — Clean output.** Queue files contain only structured candidate-fact rows and commitment rows. No markdown fences, no LLM self-commentary, no Tilth-internal artifacts mixed into the operator-facing queue. `pending_facts.yaml` and `proposal_commitments.yaml` are Pydantic-validated before write. Extractor LLM outputs go through structured-output discipline (Pydantic AI native pattern); raw LLM output never reaches the queue file.

# §11.4 Input contracts (per mode)

Intake fires at three distinct trigger points; each mode has its own input contract.

## §11.4.1 BULK_INGEST input contract

Trigger: operator-explicit at white-glove onboarding via `tilth intake bulk-ingest --org <slug>`.

**Input bundle (`IntakeBulkInput`, frozen, kw_only):**
- `run_id: str` — UUID assigned at CLI invocation; pins the run for state persistence.
- `org_slug: str` — client org slug for vault path resolution (required CLI arg).
- `inbox_dir: str` — vault path to the operator-uploaded folder. Defaults to `orgs/<org_slug>/intake/inbox/`. `Path.resolve()` is called at PRE-gate; the resolved path MUST sit under `orgs/<org_slug>/`. Symlink ingest is rejected (`F-INTAKE-ORG-CROSS-REF`).
- `confidence_autopromote_threshold: float` — operator-set autopromote threshold per §11.14 default OQ-1; default `0.85`. Candidates with `confidence_score >= threshold` AND passing F-EXTRACTOR-FABRICATION are routed to the autopromote-batch surface; the rest go to per-doc batch-confirm. Both surfaces are operator-confirmed before any KFR write.
- `invoked_at_utc: datetime`.

**Bundle invariants (PRE-gate enforced).**
- `inbox_dir` (after `Path.resolve()`) MUST sit under `orgs/<org_slug>/`. Path-traversal-by-symlink → `F-INTAKE-ORG-CROSS-REF` (subclass `.symlink_escape`).
- `inbox_dir` MUST exist and be a directory (not a single file — INCREMENTAL_INGEST is the single-file path). Empty directory → no-op success (writes `intake_state.yaml` with `candidates_produced=0` and `mode_completed=true`).
- `confidence_autopromote_threshold` MUST be in `[0.0, 1.0]`. Out of range → reject at CLI parse time (Pydantic input validation).
- **Operator-config signature (per RT-07 closure).** If `confidence_autopromote_threshold` is sourced from `orgs/<slug>/intake/intake_config.yaml` (per-org default), the config file MUST be Ed25519-signed by an operator key currently active in the Section 1 key catalog. F-INTAKE-CONFIG-SIGNATURE-INVALID (§11.9.NEW) fires at config read time if signature missing, invalid, or signed by a retired key. Per-run CLI override via `--confidence-threshold <float>` does NOT require a signed config (CLI is operator-interactive by definition); BUT the CLI parser explicitly **prohibits** `--yes`, `--auto-confirm`, and `--force` flags at v0.1 (per RT-08 closure) — any such flag triggers an argparse-level rejection. The 0.85 default is hardcoded into the seat module; absent both signed config and CLI override, the hardcoded default applies.

## §11.4.2 INCREMENTAL_INGEST input contract

Trigger: filesystem watcher OR operator-explicit (both per §11.14 default OQ-2). Watcher fires on new file events under `orgs/<slug>/intake/inbox/`; operator-explicit invocation via `tilth intake incremental --org <slug> --doc <path>`.

**Input bundle (`IntakeIncrementalInput`, frozen, kw_only):**
- `run_id: str` — UUID assigned at watcher trigger or CLI invocation.
- `org_slug: str` — client org slug.
- `doc_path: str` — vault path to the single new document. `Path.resolve()` is called at PRE-gate; the resolved path MUST sit under `orgs/<org_slug>/intake/inbox/`. Symlink ingest is rejected.
- `trigger: Literal["watcher", "operator_explicit"]` — provenance of the trigger, recorded in `intake_state.yaml`.
- `confidence_autopromote_threshold: float` — same as BULK; default 0.85. Per-org operator-set in `orgs/<slug>/intake/intake_config.yaml` (Code phase decision: operator may set per-org default to override the v0.1 0.85 system default).
- `invoked_at_utc: datetime`.

**Bundle invariants (PRE-gate enforced).**
- `doc_path` (after `Path.resolve()`) MUST sit under `orgs/<org_slug>/intake/inbox/`. → `F-INTAKE-ORG-CROSS-REF` (subclass `.path_outside_inbox`).
- `doc_path` MUST exist and be a regular file. Missing or non-file → reject with `F-INTAKE-INPUT-MISSING`.
- File extension MUST be in the v1 supported set: `.pdf`, `.docx`, `.txt`, `.md`. Unsupported extension → reject with `F-INTAKE-UNSUPPORTED-FORMAT`. (`.xlsx`, `.csv`, `.html`, `.eml` deferred to v0.1.x per §11.14 OQ-INTAKE-FORMATS.)

## §11.4.3 AWARD_INGEST input contract

Trigger: operator-explicit only at v0.1 per v7.0.4 §5.3. CLI: `tilth intake award-ingest --org <slug> --grant <grant_id> --award-doc <path>`. No watcher, no scheduled-task, no inbox-watcher trigger at v0.1 (filesystem-watcher trigger for AWARD_INGEST deferred to v0.2 WS-E follow-up).

**Input bundle (`IntakeAwardInput`, frozen, kw_only):**
- `run_id: str` — UUID assigned at CLI invocation.
- `org_slug: str` — client org slug.
- `grant_id: str` — grant identifier; resolves to `orgs/<org_slug>/vault/grants/<grant_id>/`. Required CLI arg.
- `submission_artifact_ref: str` — vault path to the operator-signed `draft_<v>.md` from `orgs/<org_slug>/vault/grants/<grant_id>/submission/`. Auto-resolved from `--grant` argument by walking the `submission/` subdirectory and selecting the most recent operator-signed draft (operator can override with `--submission-artifact <path>` at the CLI). `Path.resolve()` is called at PRE-gate; the resolved path MUST sit under `orgs/<org_slug>/vault/grants/<grant_id>/`. Symlink ingest is rejected.
- `award_doc_path: str` — operator-supplied path to the funder's award notification (PDF or DOCX). Required CLI arg. `Path.resolve()` is called at PRE-gate; the resolved path MUST sit under `orgs/<org_slug>/vault/grants/<grant_id>/award/` per the §2 Vault topology convention. (If operator-supplied path is outside the vault subtree, Intake refuses with `F-INTAKE-ORG-CROSS-REF` sub-tag `.award_doc_outside_vault` — operator must first stage the award doc into the vault via the appropriate Vault write intent.)
- `award_doc_unsigned_attestation: bool` — operator attestation flag for funders that do not publish signing keys. If `True`, F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award is bypassed for THIS run only (the bypass is logged to admin-risk ledger at HIGH severity per §11.9.3); if `False` and the funder's signing key is unknown to `vault_shared/funders/<funder_id>/signing_keys.yaml`, Intake refuses with the same gate code. Default: `False`.
- `invoked_at_utc: datetime`.

**Bundle invariants (PRE-gate enforced).**
- `submission_artifact_ref` MUST exist and be a `draft_<v>.md` under the named grant_id's submission/ subtree. Missing or non-matching → `F-INTAKE-INPUT-MISSING` sub-tag `.submission_artifact_absent`.
- `award_doc_path` MUST exist and be a regular file with extension `.pdf` or `.docx`. Missing or non-matching → `F-INTAKE-INPUT-MISSING` sub-tag `.award_doc_absent`.
- Both paths MUST resolve under `orgs/<org_slug>/vault/grants/<grant_id>/`. Cross-org or cross-grant → `F-INTAKE-ORG-CROSS-REF`.
- **Content-hash binding (per RT-05 closure).** The submission artifact's paired `SignedClaimEvidenceMap` (located at `orgs/<slug>/vault/grants/<grant_id>/submission/<draft>.signed_claim_evidence_map.yaml` per Section 4 v2.1 schema) MUST include a `submission_artifact_content_sha3_512` field carrying the SHA3-512 hash of the `draft_<v>.md` bytes. F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal (§11.9.2) recomputes the hash at AWARD_INGEST time and compares against the signed value; mismatch fires the gate's new `.hash_mismatch` sub-tag. Mirrors §12 Uploader's F-UPLOADER-SIGNATURE-MISSING.hash_mismatch precedent — closes the path where a validly-signed claim-evidence-map is paired with a tampered draft file. If the SignedClaimEvidenceMap predates this content-hash binding requirement (i.e., from a draft signed before §11 v1 LOCK), AWARD_INGEST refuses with the same gate code; operator must re-sign the claim-evidence-map under the §11-v1-LOCK-aware Uploader to enable AWARD_INGEST.

# §11.5 Output contracts (per mode)

## §11.5.0 Schema delta from v7.0.4 KFR conventions (per E-3 closure)

Intake's queue and proposal_commitments schemas extend v7.0.4 §1 (KFR fact schema) and v7.0.4 §5.3 (proposal_commitments schema) with the following deltas. All other fields retain v7.0.4 conventions (`populated_at`, `populated_by`, `audit_chain`, `source_doc`, `source_quote`, etc.).

| Schema | Field | Type | Source | Purpose |
|---|---|---|---|---|
| `pending_facts.v1` | `candidate_id` | opaque-uuid | NEW (Intake-introduced) | Per-candidate identifier for audit trail and merge resolution at operator review |
| `pending_facts.v1` | `intake_run_id` | str | NEW (Intake-introduced) | Pins the candidate to the Intake invocation that produced it; enables cross-run accounting per F-INTAKE-QUEUE-INTEGRITY (§11.9.7) |
| `pending_facts.v1` | `extracted_at_utc` | datetime | NEW (Intake-introduced) | When the extraction LLM emitted this candidate; distinct from `populated_at` (which fires only at promotion to canonical KFR) |
| `pending_facts.v1` | `source_paragraph_id` | int OR null | NEW (Intake-introduced per RT-03 closure) | Primary anchor for DOCX substrate (paragraph-walk index); deterministic across renderer versions |
| `pending_facts.v1` | `source_line_id` | int OR null | NEW (Intake-introduced per RT-02 closure) | Primary anchor for TXT/Markdown substrate (zero-based line index in raw line buffer) |
| `pending_facts.v1` | `source_format` | Literal["pdf","docx","txt","md"] | NEW (Intake-introduced) | Source format selector; routes the F-EXTRACTOR-FABRICATION predicate to the appropriate substrate-specific check (§11.9.1.A/B/C/D) |
| `pending_facts.v1` | `confidence_score` | float [0.0, 1.0] | NEW (Intake-introduced) | LLM-emitted confidence; drives autopromote_batch tagging |
| `pending_facts.v1` | `autopromote_batch` | bool | NEW (Intake-introduced) | True iff `confidence_score >= confidence_autopromote_threshold` AND F-EXTRACTOR-FABRICATION PASS |
| `pending_facts.v1` | `multiple_page_match` | bool | NEW (Intake-introduced per RT-01 closure) | Operator-explicit override flag for PDF candidates whose source_quote occurs on multiple pages; routes to per-doc batch-confirm only |
| `proposal_commitments.v1` | `status` | Literal["PENDING_OPERATOR_REVIEW","PROMOTED"] | NEW (Intake-introduced) | Top-level status flag; Report Generator (§14, v0.2) only consumes `PROMOTED` files |
| `proposal_commitments.v1` | `commitment_proposal_offset` | int | per v7.0.4 §5.3 | Byte offset for operator-side highlighting; preserved as-is |
| `proposal_commitments.v1` | `page_tolerance_applied` | bool | NEW (Intake-introduced per RT-01/RT-04 closures) | True iff the commitment's `source_quote` matched at ±1 page tolerance under AWARD_INGEST PDF substrate |
| `proposal_commitments.v1` | `kfr_fact_ref` | str OR null | per v7.0.4 §5.3 | Optional cross-reference to existing KFR fact for F-LOGICIAN-FACT-DRIFT discipline at reporting cycles |

Field names preserve v7.0.4 KFR conventions (snake_case with substrate prefix; UTC-suffixed timestamps; `_at_utc` for datetime fields; `_id` for opaque references). Pydantic schemas live in `pipeline/orchestrator/seats/intake.py` per §11.15 module scaffold.

## §11.5.1 BULK_INGEST + INCREMENTAL_INGEST output

**Output file.** `orgs/<slug>/vault/kfr/pending_facts.yaml` — append-mode (one queue file per org accumulating across runs; promotion to canonical KFR moves entries out of the queue into `register.yaml`). Pydantic-validated before write.

**State file (separate from queue).** `orgs/<slug>/vault/kfr/intake_state/<run_id>.yaml` — per-run Tilth-internal artifact per Rule 1.

**Reject audit trail.** `pipeline/validation/extractor_rejects/<org_slug>/<run_id>/` — one `<reject_id>.yaml` per F-EXTRACTOR-FABRICATION reject (or other PRE-pre-queue rejection), per v7.0.4 §5.2 reject-with-audit-trail discipline. Each reject entry includes: `extracted_fact_payload`, `source_doc`, `source_page`, `attempted_quote`, `actual_source_bytes_at_page` (for diff inspection), `reject_reason_code`, `rejected_at_utc`.

**Operator-review surface.** Operator runs `tilth intake review --org <slug>` to enter the review surface (CLI for v0.1; UI deferred per overall v0.1 headless posture). Surface displays per-doc batches with side-by-side (`extracted fact / source quote / source document at source page`) and offers per-candidate actions: **confirm** (promote to KFR with operator signature), **edit** (modify before promotion), **reject** (drop with audit trail under `pipeline/validation/extractor_review_rejects/`), **merge** (combine with existing KFR entry via key match). Autopromote-batch surface per §11.7 supports operator-confirmed bulk-confirm via single keystroke (operator reviews the autopromote summary and one-click confirms the batch — NOT a silent autopromote).

**Pending facts schema** (per v7.0.4 §5.1 — single-row pattern for the queue):

```yaml
schema_version: pending_facts.v1
org_slug: <client>
queue_populated_at: <utc-timestamp>
queue_populated_by: intake@<run_id>

pending_facts:
  - candidate_id: <opaque-uuid>
    intake_run_id: <run_id>
    extracted_at_utc: <utc-timestamp>
    # ... per v7.0.4 §1 facts: schema (who, what, when_period, when_as_of, when_cadence, when_expiry, where, why, how.{methodology, sample_size, assumptions}, value, unit, projection_or_actual, comparison_anchor.{prior_year_value, benchmark_id}, confidence, required_for_category, required_for_funder)
    source_doc: <absolute path>
    source_page: <integer>
    source_quote: <verbatim quote — F-EXTRACTOR-FABRICATION-validated against source_doc at source_page per v7.0.4 §5.2 exact-match semantics>
    confidence_score: <0.0 - 1.0 from extractor model>
    autopromote_batch: <bool — true iff confidence_score >= confidence_autopromote_threshold>
```

## §11.5.2 AWARD_INGEST output

**Output file.** `orgs/<slug>/vault/grants/<grant_id>/proposal_commitments.yaml` — per v7.0.4 §5.3 schema (one file per grant_id; written once at award acceptance, edited by operator at structuring-time review, re-signed at promotion). Pydantic-validated before write.

**State file.** `orgs/<slug>/vault/kfr/intake_state/<run_id>.yaml` — same path family as BULK + INCREMENTAL state files (Intake state co-locates regardless of mode).

**Pre-extraction signature verification trail.** `pipeline/validation/extractor_signature_verification/<org_slug>/<grant_id>/<run_id>.yaml` — per v7.0.4 §5.3 pre-extraction verification record. Includes: `submission_artifact_path`, `submission_signature_verified_at`, `submission_signature_verified_by_key_id`, `award_doc_path`, `award_doc_signature_verified_at` (or `award_doc_unsigned_attestation_logged_at` if the operator-attestation bypass fired), `award_doc_signing_key_id` (or `null` if unsigned with attestation), and the `F-EXTRACTOR-AWARD-SIGNATURE-INVALID` outcome (PASS / FAIL.proposal / FAIL.award).

**Operator-review surface.** Operator runs `tilth intake award-review --org <slug> --grant <grant_id>` to enter the structuring review surface. Each commitment row is displayed side-by-side with the verbatim proposal quote at its source offset. Operator can: **confirm-as-extracted** (no edits), **structure** (edit `measurable_metric` / `target_value` / `target_unit` / `due_period` to clarify intent — the proposal text may be narrative; the commitment row is structured), **link-to-KFR** (set `kfr_fact_ref: <fact_id>` linking the commitment to an existing KFR fact for F-LOGICIAN-FACT-DRIFT discipline during reporting cycles), **drop** (commitment is ambiguous or operator-judges-not-load-bearing — drop with audit trail), **add** (operator adds a commitment Intake missed — operator-supplied commitment_text MUST quote the proposal verbatim or the row fails Pydantic validation at write).

**Promotion.** Operator-signed at promotion via `tilth intake award-promote --org <slug> --grant <grant_id>`. Promotion writes the operator-signed `proposal_commitments.yaml` per v7.0.4 §5.3 schema with `audit_chain` initialized as `operator_signature_at_award_ingest_completion`. Until promoted, the file carries a `status: PENDING_OPERATOR_REVIEW` field at the top level; F-LOGICIAN-FACT-DRIFT discipline does NOT consume PENDING_OPERATOR_REVIEW commitments (Report Generator at v0.2 only reads `status: PROMOTED` files). This prevents in-flight Intake runs from polluting Report Generator inputs.

# §11.6 Three modes specification

## §11.6.0 Three-mode summary table (per E-1 closure)

| Mode | Trigger | Input | Output | Mode-tolerance flag (RT-04) | Done definition |
|---|---|---|---|---|---|
| **BULK_INGEST** | Operator-explicit at white-glove onboarding (`tilth intake bulk-ingest`) | `IntakeBulkInput` over `orgs/<slug>/intake/inbox/` folder | `pending_facts.yaml` queue + per-run `intake_state.yaml` + `extractor_rejects/` audit trail | Strict (no ±1 page tolerance) — mode flag immutable per input bundle | Queue + state + audit trail consistent; F-EXTRACTOR-FABRICATION verified on every PASS candidate |
| **INCREMENTAL_INGEST** | Filesystem watcher OR operator-explicit (`tilth intake incremental`) — both per OQ-2 default | `IntakeIncrementalInput` over single doc | Same as BULK (append to queue) | Strict (same as BULK) | Same as BULK, scoped to single doc |
| **AWARD_INGEST** | Operator-explicit only at v0.1 (`tilth intake award-ingest`) | `IntakeAwardInput` over operator-signed submission artifact + funder award doc | `proposal_commitments.yaml` with `status: PENDING_OPERATOR_REVIEW` + per-run state + signature-verification trail | ±1 page tolerance allowed with `page_tolerance_applied=true` operator flag per row | Pre-extraction signature verification PASS; PENDING file written; ready for operator structuring review |

**MIGRATION_BULK_INGEST** is a special invocation of BULK_INGEST scoped to a single org's existing `PROJECT_CONTEXT.md` per §11.11; not a fourth registered mode in the dispatcher.

## §11.6.1 BULK_INGEST mode

**When:** white-glove onboarding (one-time per org) OR re-baseline events (operator decides to re-process the inbox folder, e.g., after substantial doc additions).

**Input:** folder of org documents (annual reports, 990s, audited financials, employee rosters, program reports, partnership LOIs, prior grant applications) under `orgs/<slug>/intake/inbox/`.

**Process:**

1. **Sweep.** Walk `inbox_dir` recursively, collecting every supported-format file (per §11.4.1 invariant: `.pdf`, `.docx`, `.txt`, `.md`). Skip hidden files (`.DS_Store`, `.gitkeep`, etc.) and Tilth-internal files (no Tilth-generated artifact under `intake/inbox/` should exist; if found, surface as a warning in `intake_state.yaml` but do not block the sweep).

2. **Index.** For each doc: parse with the format-appropriate parser (`pypdf` for PDF, `python-docx` for DOCX, native read for TXT/MD); embed page-bounded chunks into the per-org local vector store (FAISS or Chroma + bge-large-en-v1.5 per v7.0.4 §5 substrate decision); persist embeddings under `orgs/<slug>/vault/intake/embeddings/<doc_hash>/` for re-use across runs.

3. **Extract.** For each doc: invoke the Pydantic AI agent with the small local LLM (Mistral 7B class — §11.8) using the structured-output extraction prompt. The LLM emits candidate_fact rows in the v7.0.4 §5.1 schema. Structured-output validation (Pydantic) rejects malformed rows pre-queue (no audit-trail logged for malformed rows beyond the LLM-call log; these are Intake-internal failures, not source-content failures).

4. **Verbatim-validate.** For each emitted candidate_fact: run F-EXTRACTOR-FABRICATION (§11.9.1) — verbatim match check per v7.0.4 §5.2 exact-match semantics (Unicode NFC + whitespace normalization PASS; OCR-substitution + page-off-by-one + ellipsis-substring REJECTED in BULK_INGEST mode). FAIL → reject pre-queue, write to `extractor_rejects/<run_id>/` audit trail. PASS → proceed to step 5.

5. **Confidence-tag.** For each PASS candidate: tag with `autopromote_batch: true` if `confidence_score >= confidence_autopromote_threshold` (default 0.85); else `autopromote_batch: false`.

6. **Queue.** Append all PASS candidates to `pending_facts.yaml` (Pydantic-validated batch write via §2 Vault write intent).

7. **State.** Write `intake_state.yaml` with mode_completed=true, doc_count, candidates_produced (queue length delta from this run), candidates_rejected (count from extractor_rejects/), per-doc summary.

**Done definition:** `pending_facts.yaml` contains all extracted-and-validated candidates from this BULK run; `intake_state.yaml` written; reject audit trail consistent; no partial state on disk.

**Operator-next-step:** `tilth intake review --org <slug>` to enter the per-doc batch-confirm + autopromote-batch review surface (§11.7).

## §11.6.2 INCREMENTAL_INGEST mode

**When:** continuous operations — operator drops a new document during normal use (a board minutes report, a quarterly financial, a new partnership LOI, etc.).

**Trigger:** filesystem watcher OR operator-explicit (both — §11.14 default OQ-2). Watcher implementation: per-org watcher process polling `orgs/<slug>/intake/inbox/` for new files (Code phase decision: `watchdog` library is the v0.1 substrate for the Python-side watcher; daemonization via systemd-equivalent / launchd is operator-curated per OS).

**Input:** single new document at `doc_path` under `orgs/<slug>/intake/inbox/`.

**Process:** identical to BULK_INGEST steps 2–7, scoped to the single doc. Skip the sweep step (the doc is already named).

**Done definition:** same as BULK; queue + state + audit trail consistent.

**Operator-next-step:** operator can defer review (queue accumulates; `tilth intake review` displays the union of all unreviewed candidates from BULK and INCREMENTAL runs) or review immediately. The watcher-INCREMENTAL pattern is designed for low-friction "drop a doc, get to review later" workflow; the operator-explicit-INCREMENTAL pattern is designed for "I just need this fact in KFR right now."

**Watcher posture caveats.**
- Watcher does NOT auto-promote anything to KFR. The autopromote-batch surface is operator-confirmed-batch, not silent-auto-write — see §11.7.
- Watcher fires Intake under the same `intake_state.yaml` discipline as operator-explicit; the `trigger` field distinguishes provenance.
- Watcher does NOT process files that are still being written (uses file-stability check: file size unchanged for ≥2 seconds AND file-handle release detected before processing). Avoids partial-file extraction races.
- **TOCTOU-safe file handling (per RT-11 closure).** After the PRE-gate `Path.resolve()` check passes (§11.9.4 path-isolation discipline), the watcher MUST: (a) verify `path.is_file()` AND `not path.is_symlink()` immediately before opening; (b) open with `os.open(path, os.O_RDONLY | os.O_NOFOLLOW)` — `O_NOFOLLOW` makes the open call fail with `ELOOP` if the path is a symlink at the moment of open, closing the time-of-check / time-of-use gap between the PRE-gate resolve and the read; (c) re-validate `Path.resolve()` after open against the original declared org subtree before any extraction work proceeds. Symlink swap mid-window → fail-closed with `F-INTAKE-ORG-CROSS-REF.symlink_escape` (or the explicit `F-INTAKE-WATCHER-TOCTOU` audit-trail subclass row per §11.9.NEW). Same TOCTOU discipline applies to operator-explicit INCREMENTAL invocations and to BULK sweep file-opens.
- **Quarantine for unsupported-format files (per RT-15 closure).** When the watcher detects an unsupported-format file in `intake/inbox/` (per §11.4.2 invariant + F-INTAKE-UNSUPPORTED-FORMAT, §11.9.6), the watcher MUST move the file to `orgs/<slug>/intake/quarantine/unsupported/<timestamp>_<original_name>` (rather than leaving it in `inbox/`). The move uses `os.rename` (atomic on same filesystem); cross-filesystem moves use `shutil.move` with explicit fail-closed on partial-move state. Quarantined files require **explicit operator review and removal** before any future format-support amendment activates support for the file's extension — preserves the operator-trust boundary against latent malicious payloads (e.g., `.xlsx` with embedded VBA macros) that would otherwise sit dormant in `inbox/` indefinitely until a format-support amendment lands. The quarantine surface is per-org-isolated (no cross-org quarantine pool).
- Watcher fails closed: if any PRE-gate (§11.9 PRE codes) fires for a watched doc, the watcher logs to `intake_state.yaml` and surfaces a notification (Code phase decision on notification channel; default: write to `orgs/<slug>/intake/notifications/<run_id>.txt` for operator pickup). The doc remains in `intake/inbox/` for operator inspection — Intake does NOT move or delete files in `inbox/` EXCEPT under the quarantine path above (operator owns inbox lifecycle for in-scope formats; operator must consciously remove quarantined files).

## §11.6.3 AWARD_INGEST mode

**When:** operator marks a submitted proposal as WON. Per v7.0.4 §5.3, operator-explicit only at v0.1.

**Input:** operator-signed submission artifact (auto-resolved from `--grant`) + funder's award document (operator-supplied via `--award-doc`).

**Process:**

1. **Pre-extraction verification.** Run signature verification per v7.0.4 §5.3:
   - Submission artifact: verify operator Ed25519 signature per Section 4 §4.5 `verify_claim_evidence_map` discipline. FAIL → refuse with `F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal` (§11.9.2), write `intake_state.yaml` with failure, log to admin-risk ledger at HIGH severity, exit non-zero.
   - Award document: verify funder signature against `vault_shared/funders/<funder_id>/signing_keys.yaml` (operator-curated per-funder, populated at first AWARD_INGEST per funder, optional). If unsigned AND `award_doc_unsigned_attestation` is `False` → refuse with `F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award` (§11.9.3). If unsigned AND attestation is `True` → bypass with admin-risk-ledger HIGH log; proceed. If signed AND signature fails verification → refuse with `F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award`.

2. **Index won proposal.** Parse `submission_artifact_ref` (`draft_<v>.md` is plain markdown; native read). Embed paragraph-level chunks into per-org-per-grant local vector store namespace. Persist embeddings under `orgs/<slug>/vault/grants/<grant_id>/intake_embeddings/<draft_hash>/`.

3. **Extract commitments.** Invoke Pydantic AI agent with structured-output prompt scoped to commitment extraction. The LLM identifies measurable commitments in the won proposal — sentences and paragraphs that promise outcomes, deliverables, beneficiary counts, financial milestones, or timeline events. Each emitted commitment_row carries: `commitment_text` (verbatim quote from proposal), `commitment_proposal_offset` (byte offset for operator-side highlighting), `source_section` (RFA section name where the commitment lives), `measurable_metric` (LLM-best-effort structuring), `target_value` (LLM-best-effort numeric), `target_unit`, `due_period` (LLM-best-effort temporal extraction).

4. **Verbatim-validate.** For each emitted commitment_row: run F-EXTRACTOR-FABRICATION on `commitment_text` against `submission_artifact_ref` per v7.0.4 §5.2 exact-match semantics. **±1 page tolerance allowed in AWARD_INGEST mode** with operator-confirmation flag (per v7.0.4 §5.2 — proposal documents may reflow when re-rendered post-submit; the ±1 page tolerance is the documented carve-out). Operator-confirmation flag: each commitment row passes a `page_tolerance_applied: bool` field; if `true`, the operator review surface (§11.5.2) flags the row for explicit operator confirmation of the page-offset shift. FAIL beyond ±1 page tolerance → reject pre-queue, audit trail logged.

5. **Queue (PENDING).** Write `proposal_commitments.yaml` with `status: PENDING_OPERATOR_REVIEW` at the top level. The file is on disk and inspectable but is NOT consumed by Report Generator until operator promotes via `tilth intake award-promote`.

6. **State.** Write `intake_state.yaml` with mode_completed=true, signature verification trail path, commitments_produced, commitments_rejected.

**Done definition:** `proposal_commitments.yaml` written with PENDING status; pre-extraction verification trail filed; reject audit trail consistent; `intake_state.yaml` written.

**Operator-next-step:** `tilth intake award-review --org <slug> --grant <grant_id>` to enter the structuring review surface; then `tilth intake award-promote --org <slug> --grant <grant_id>` to operator-sign and flip status to PROMOTED. Until PROMOTED, Report Generator (§14, v0.2) cannot consume the file.

# §11.7 Operator review UX

The BULK + INCREMENTAL operator-review surface is the load-bearing UX for KFR ingestion; AWARD_INGEST has its own structuring surface (§11.5.2). This section covers the BULK + INCREMENTAL surface in detail.

**Surface entry.** `tilth intake review --org <slug>` displays the union of all unreviewed candidates in `pending_facts.yaml`, partitioned into two views:

1. **Autopromote-batch view** (operator-confirmed-batch, NOT silent-auto-write). Lists all candidates with `autopromote_batch: true` (confidence_score ≥ threshold AND F-EXTRACTOR-FABRICATION-validated). Operator sees the count, an aggregate summary by source doc (e.g., "47 candidates from `2024_annual_report.pdf` at confidence ≥ 0.85"), and a per-candidate spot-check sample (default: 5 random candidates per source doc). Operator actions: **confirm-batch** (promote all autopromote candidates to KFR with operator signature; takes one keystroke), **demote-to-review** (move all autopromote candidates to the per-doc batch-confirm view for individual review; takes one keystroke), **per-doc-confirm** (operator confirms autopromote candidates per source doc one at a time, allowing finer-grained control without forcing per-candidate review).

2. **Per-doc batch-confirm view** (operator-confirmed-individual within a per-doc batch). Lists candidates with `autopromote_batch: false` (confidence_score < threshold), grouped by source doc. Operator walks each doc's candidates with side-by-side display (extracted fact / source quote / source document at source page). Per-candidate actions: **confirm** (promote with operator signature), **edit** (modify the candidate before promotion — `value`, `methodology`, `assumptions`, etc. fields may need operator clarification; `source_doc` / `source_page` / `source_quote` are NOT editable by the operator at review time per Law 5 — quote integrity is structural), **reject** (drop with audit trail under `pipeline/validation/extractor_review_rejects/<org_slug>/<run_id>/`), **merge** (combine with existing KFR entry via key match; merge confirmation prompts operator with both entries side-by-side, asks operator to choose: replace existing / keep both / discard new / keep new and archive existing).

**Operator key requirement.** All confirm / edit-then-confirm / merge actions require operator Ed25519 signature per v7.0.4 §1 schema (`validation.confirmed_by` + `validation.confirmed_when` + `audit_chain` initialized with `operator_signature_at_initial_population`). Reject actions do NOT require operator signature (rejecting is non-load-bearing for KFR canonical state); the reject is logged with operator key id for audit but the rejected candidate doesn't enter KFR.

**TTY check on confirm-batch (per RT-08 closure).** The `tilth intake review --confirm-batch` invocation MUST verify `sys.stdin.isatty()` at CLI parse time. Non-TTY invocation (piped from cron, script, or `yes |` pipeline) is rejected with a clear error message: "confirm-batch requires interactive TTY; cannot be scripted at v0.1." `--yes`, `--auto-confirm`, and `--force` flags are explicitly NOT v0.1 args (argparse rejects them with a v0.1-specific error message). This closes the silent-auto-write path where an attacker or careless automation could pipe `yes` into the review CLI and bypass operator scrutiny entirely. Same TTY check applies to `tilth intake award-promote` (§11.5.2) for the AWARD_INGEST PROMOTED-status flip.

**Autopromote-batch is NOT silent-auto-write — emphasized (per E-2 closure).** The 0.85 default threshold + per-org operator-signed config override (per RT-07 closure) + per-run CLI override + interactive TTY confirmation (per RT-08 closure) form a four-layer structural defense against silent autopromotion:
1. **Layer 1 — hardcoded default.** The 0.85 threshold is baked into the seat module; no zero-config default-overshare path exists.
2. **Layer 2 — signed per-org override.** Per-org config tuning requires operator Ed25519 signature; F-INTAKE-CONFIG-SIGNATURE-INVALID fail-closed.
3. **Layer 3 — CLI override.** Per-run threshold override is operator-interactive by definition.
4. **Layer 4 — TTY confirmation.** The "one keystroke" confirm-batch action requires an interactive terminal; cannot be scripted away.

Removing any single layer creates a silent-promote path; all four are structural at v0.1.

**Confidence-threshold autopromote rationale.** The 0.85 default threshold is chosen to bias toward operator-confirmed-batch over per-candidate review at high-confidence extraction. Rationale: a 200-candidate BULK_INGEST from a 990 with 80% high-confidence candidates produces 160 autopromote-batch candidates that operator can confirm in one keystroke after a 5-candidate spot check, plus 40 per-doc-batch-confirm candidates that need individual review. This is the load-bearing UX optimization: per-candidate review of 200 candidates is a 4-hour task; one keystroke + 40-candidate per-doc review is a 30-minute task. Both produce operator-signed KFR entries; the autopromote-batch surface does not skip operator confirmation, it batches it.

**Threshold tuning.** Operator can adjust the threshold per-org via `orgs/<slug>/intake/intake_config.yaml` `confidence_autopromote_threshold` field. CLI override per-run via `--confidence-threshold <float>`. Lower thresholds (e.g., 0.70) produce more autopromote candidates and fewer per-doc-batch candidates; higher thresholds (e.g., 0.95) the reverse. The autopromote-batch surface remains operator-confirmed-batch regardless of threshold — silent-auto-write is structurally prohibited.

**Resumability.** Per Rule 1 (Save State Always), the review session is resumable. Partial-confirm state persists in `orgs/<slug>/vault/kfr/intake_state/<review_session_id>.yaml`. Operator can exit mid-review and resume; previously-confirmed candidates do NOT re-appear; previously-rejected candidates do NOT re-appear; previously-deferred candidates DO re-appear in the next review session (deferred = operator did not act; remains in queue).

# §11.8 Substrate

**Local vector store.** FAISS or Chroma (operator-selected at white-glove per ADR-001 substrate envelope; FAISS default). Stored under `orgs/<slug>/vault/intake/embeddings/<doc_hash>/`. Per-org-segmented namespace; per-grant sub-namespace for AWARD_INGEST embeddings under `orgs/<slug>/vault/grants/<grant_id>/intake_embeddings/`. F-VECTOR-NS-MISMATCH (v7.0.5) discipline applies — every Pydantic AI tool call against the vector store passes `org_slug` (and `grant_id` for AWARD_INGEST) as a tool-arg-validated parameter; cross-org or cross-grant query → fail-closed.

**Embedding model.** bge-large-en-v1.5 (per v7.0.4 §5 substrate decision; same model family as Funder Intelligence DB indexing per v7.0.5; one unified embedding model across Tilth's local vector substrate). Frozen at Golden Image build per ADR-001; no marketplace access from the appliance.

**Extraction LLM.** Small local LLM, Mistral 7B class (per v7.0.4 §5; same model family as Scout's local model per the v7 architecture envelope). Specific binding lives in `/router.yaml` per the SOLE-source-of-binding discipline; the §11 blueprint does NOT hardcode the model name. Always-local routing per §11.10.

**Orchestration.** Pydantic AI agent (per v7.0.3 substrate decision; same orchestration substrate as Scribe / Editor / Judge / Red Team / Logician). Tool composition: parser tools (`pypdf`, `python-docx`, native text read) wrapped as Pydantic AI tools; vector store tools (FAISS / Chroma client) wrapped as Pydantic AI tools with org_slug parameter validation; structured-output extraction prompt with v7.0.4 §5.1 schema as the output Pydantic model.

**Format parsers.** `pypdf` for PDF (text extraction + page-bounded chunking). `python-docx` for DOCX (paragraph-level chunking with style preservation for table detection). Native Python `open()` (mediated by §2 Vault read intent — never raw `open()` on operator-uploaded content) for TXT and MD. Per ADR-001 substrate frozen at Golden Image; no marketplace access.

**OCR.** Out of scope for v0.1 first ship. PDFs with bad OCR output that produce ambiguous source bytes must be re-OCR'd by operator before Intake processes them per v7.0.4 §5.2 (the F-EXTRACTOR-FABRICATION exact-match semantics REJECT OCR-substitution mapping; bridging OCR errors silently is a structural prohibition). v0.1.x candidate: integrate Tesseract or equivalent local OCR (Tesseract ships per ADR-001 envelope; integration is Code work, not architecture).

**No marketplace access from the appliance.** Per ADR-001, every dependency is frozen at Golden Image build. Intake's substrate is exactly: FAISS or Chroma + bge-large-en-v1.5 + Mistral 7B class + pypdf + python-docx + Pydantic AI. Adding a new parser, a new embedding model, or a new extraction LLM at runtime is structurally prohibited (no `pip install` from the appliance; no LLM marketplace fetch). New substrate elements require a Golden Image rebuild + an ADR amendment.

# §11.9 Logician gate family — F-EXTRACTOR-* + F-INTAKE-*

Intake introduces a small focused gate family at v0.1 first ship, all registered in the §4 Logician v2.x amendment (WS-L). All gates are deterministic (Python predicates); zero token cost (apart from the small local-LLM extraction calls themselves — those are routing-gated by the always-local posture per §11.10 and bounded by the input document size).

**v1 gate roster (12 codes — 4 new from Cycle 1 closures: F-INTAKE-EMBEDDING-NS-MISMATCH, F-INTAKE-CONFIG-SIGNATURE-INVALID, F-INTAKE-EMBEDDING-ENDPOINT-INVALID, F-INTAKE-WATCHER-TOCTOU):**

| # | Code | Position | Owner-§ | Notes |
|---|------|----------|---------|-------|
| 1 | F-EXTRACTOR-FABRICATION | PRE pre-queue | §11.9.1 (introduced v7.0.4 §5.2; §11 owns the predicate; §4 v2.x registers) | Verbatim-quote validation per substrate (PDF page-anchor + unique-page-match per RT-01; DOCX paragraph-index per RT-03; TXT/MD line-anchor with single-line constraint per RT-02; mode-immutable from input bundle per RT-04). Sub-tags `.page_mismatch`, `.multiple_page_match`, `.docx_paragraph_mismatch`, `.line_mismatch`, `.markdown_multiline`, `.ocr_substitution`, `.ellipsis_substring`. |
| 2 | F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal | PRE | §11.9.2 (introduced v7.0.4 §5.3; §11 owns the predicate; §4 v2.x registers) | AWARD_INGEST submission artifact signature verification with content-hash binding per RT-05. Sub-tags `.absent`, `.signature_invalid`, `.retired_key`, `.hash_mismatch`, `.legacy_unhashed`. |
| 3 | F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award | PRE | §11.9.3 (introduced v7.0.4 §5.3; §11 owns the predicate; §4 v2.x registers) | AWARD_INGEST award document signature verification with three-layer tamper-evident operator-attestation bypass per RT-06 (interactive prompt + ledger-write-before-process + signed funder-keys file). |
| 4 | F-INTAKE-ORG-CROSS-REF | PRE | §11.9.4 (NEW; §11-introduced; §4 v2.x registers) | Path-isolation discipline. Sub-tags `.symlink_escape`, `.path_outside_inbox`, `.award_doc_outside_vault`, `.cross_grant`. |
| 5 | F-INTAKE-INPUT-MISSING | PRE | §11.9.5 (NEW; §11-introduced; §4 v2.x registers) | Required input file or directory does not exist. Sub-tags `.inbox_dir_absent`, `.doc_absent`, `.submission_artifact_absent`, `.award_doc_absent`. |
| 6 | F-INTAKE-UNSUPPORTED-FORMAT | PRE | §11.9.6 (NEW; §11-introduced; §4 v2.x registers) | Input file extension not in v1 supported set; advisory at INCREMENTAL (file moves to quarantine per RT-15; operator notification emitted); v1.1 horizon: extend supported set per OQ-INTAKE-FORMATS. |
| 7 | F-INTAKE-QUEUE-INTEGRITY | POST + PRE-run-start | §11.9.7 (NEW; §11-introduced; §4 v2.x registers) | Queue file write produced a Pydantic-validation-failing yaml; or queue write succeeded but candidate count math doesn't reconcile; or extractor_rejects/ count doesn't reconcile against state file. Per RT-12, also fires PRE-run-start (re-validates most-recent intake_state.yaml + queue at every Intake invocation). Hard-block. |
| 8 | **F-INTAKE-EMBEDDING-NS-MISMATCH** | PRE-tool-call | §11.9.8 (NEW from RT-09 closure; §11-introduced; §4 v2.x registers) | Pre-tool guard on every Pydantic AI tool call against the local vector store; asserts `org_slug` arg matches input dataclass `org_slug` field (and `grant_id` for AWARD_INGEST). Mismatch → fail-closed. Includes RT-10 compound-key collision-detect for embedding storage path. |
| 9 | **F-INTAKE-CONFIG-SIGNATURE-INVALID** | PRE | §11.9.9 (NEW from RT-07 closure; §11-introduced; §4 v2.x registers) | `intake_config.yaml` Ed25519 signature verification at config read time; signature missing, invalid, or signed by retired key → fail-closed. Per-run CLI override does NOT require signed config but `--yes`/`--auto-confirm`/`--force` flags are explicitly NOT v0.1 args. |
| 10 | **F-INTAKE-EMBEDDING-ENDPOINT-INVALID** | PRE-tool-call | §11.9.10 (NEW from RT-13 closure; §11-introduced; §4 v2.x registers) | Embedding tool endpoint MUST resolve to localhost or unix:// socket; cloud endpoints fail-closed. Endpoint config read from sealed Golden-Image-baked location; runtime override prohibited. |
| 11 | **F-INTAKE-WATCHER-TOCTOU** | PRE-file-open | §11.9.11 (NEW from RT-11 closure; §11-introduced; §4 v2.x registers) | TOCTOU-safe file handling for watcher (and operator-explicit INCREMENTAL + BULK sweep): Path.resolve() + is_file() + not is_symlink() + os.O_NOFOLLOW open + post-open re-validate. Symlink swap mid-window → fail-closed. Audit-trail subclass of F-INTAKE-ORG-CROSS-REF.symlink_escape; preserved as distinct row per §10 explode-pattern. |
| 12 | F-CIC-CLC-COUPLING-VIOLATION | PRE/POST | inherited from v7.0.8 | Intake schema and extraction prompt template MUST audit clean against the four detection layers (lexical regex / Pydantic AST / value-set / KP schema) at LOCK. Per RT-14, LOCK-time check also runs CIC × CLC enumeration overlap detector (no CIC identifier overlaps with any CLC identifier). |

## §11.9.1 F-EXTRACTOR-FABRICATION (PRE pre-queue)

**Purpose.** Reject any extracted candidate whose `source_quote` does not literally appear in `source_doc` at the declared anchor per v7.0.4 §5.2 exact-match semantics, with per-substrate anchor discipline pinned to deterministic predicates. The cheapest gate in the system; runs before operator review.

**Predicate dispatch by source format (per RT-01 + RT-02 + RT-03 + RT-04 closures).** The mode flag (BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST) is read **only** from the immutable `Intake*Input` dataclass passed to the predicate at call time; it is **never** read from `intake_config.yaml` or any mutable runtime config. This guarantees the ±1 page tolerance carve-out applies **only** at AWARD_INGEST, structurally.

**§11.9.1.A PDF substrate (page-anchored).**

1. Read `source_doc` bytes via §2 Vault read intent.
2. Extract page text via `pypdf.PdfReader.pages[source_page-1].extract_text()`.
3. Normalize both `source_quote` and extracted page text per v7.0.4 §5.2 (Unicode NFC + whitespace collapse).
4. **Unique-page-match check (per RT-01 closure).** Compute the first-occurrence page of normalized `source_quote` across all pages of `source_doc` (sequential page-by-page substring scan). If the first-occurrence page is **not** `source_page`, fire `F-EXTRACTOR-FABRICATION.page_mismatch` (sub-tag) — the candidate is rejected even if the quote happens to be a substring of the declared page. If the quote occurs on **multiple** pages (boilerplate header/footer, repeated TOC entries), fire `F-EXTRACTOR-FABRICATION.multiple_page_match` UNLESS the candidate carries `multiple_page_match: true` operator-explicit override (which routes the candidate to the per-doc batch-confirm view §11.7 — never to the autopromote-batch view, regardless of confidence_score).
5. Return PASS iff normalized `source_quote` first-occurrence page == `source_page` AND not multi-page-matching (or operator-override applied).

**§11.9.1.B DOCX substrate (paragraph-index-anchored, per RT-03 closure).**

DOCX files do not carry deterministic page numbers (page-rendering depends on font metrics + library version + OS). Page anchoring is replaced with **paragraph-index anchoring** for DOCX sources at v1:

1. Schema permits `source_paragraph_id: int` as the primary anchor for `format=docx` (§11.5.1 schema delta). `source_page: int | null` is permitted as an advisory secondary anchor only — the gate predicate uses `source_paragraph_id` for verbatim match.
2. Extract paragraph text via `python-docx` paragraph-walk: `Document(source_doc).paragraphs[source_paragraph_id].text`.
3. Normalize both quote and paragraph text per v7.0.4 §5.2.
4. Return PASS iff normalized `source_quote` is a contiguous substring of the normalized paragraph text.

The `source_paragraph_id` is deterministic across runs (paragraph ordering is preserved in the DOCX XML structure regardless of rendering library). Tables and embedded images count as paragraphs in `Document.paragraphs` ordering, but the gate compares against text-content only — DOCX table-cell-level addressing is deferred to v1.1 if needed; v1 DOCX gate scope is paragraph-text-only.

**§11.9.1.C TXT substrate (line-anchored).**

1. Read source bytes via §2 Vault read intent.
2. Extract line at `source_line_id: int` via `source_doc.read().splitlines()[source_line_id]` (zero-based line index).
3. Normalize quote and line per v7.0.4 §5.2.
4. Return PASS iff normalized `source_quote` is a contiguous substring of the normalized line.

**§11.9.1.D Markdown substrate (line-anchored, per RT-02 closure).**

Markdown source docs (PROJECT_CONTEXT migration per §11.11; some `.md` docs in inbox) carry no native page concept. Anchor is `source_line_id: int`, and `source_quote` MUST be a **single line** as it appears in the raw file:

1. Read source bytes via §2 Vault read intent. **Do NOT collapse line endings**; preserve raw line buffer.
2. Split on actual file line endings (LF or CRLF; preserve which one was found via the file's first-line-ending byte).
3. Extract `source_doc_lines[source_line_id]` as the raw line (without trailing line ending).
4. **Single-line constraint (per RT-02 closure).** `source_quote` MUST NOT contain any line-ending character (LF, CR, CRLF). Multi-line quotes are rejected at extractor-LLM output time (Pydantic validation) AND at gate time (defense-in-depth: gate verifies `'\n' not in source_quote and '\r' not in source_quote`).
5. Normalize quote and line per v7.0.4 §5.2.
6. Return PASS iff normalized `source_quote` is a contiguous substring of the normalized line.

The single-line constraint closes the markdown-bypass path where stripping newlines before comparison would make a multi-line "quote" appear verbatim. Test in §11.13.2 enforces.

**Mode-specific tolerance (per RT-04 closure — hard-coded immutable from input dataclass).**
- **BULK_INGEST + INCREMENTAL_INGEST:** strict per v7.0.4 §5.2 — Unicode NFC + whitespace normalization PASS; **OCR-substitution + page/paragraph/line-off-by-one + ellipsis-substring REJECTED**. No tolerance regardless of any config setting.
- **AWARD_INGEST:** ±1 page tolerance allowed per v7.0.4 §5.2 for **PDF substrate ONLY** (proposal documents may reflow when re-rendered post-submit). Each commitment row passes `page_tolerance_applied: bool` field; if `true`, operator review surface (§11.5.2) flags the row for explicit operator confirmation of the page-offset shift. **The mode flag is read from `IntakeAwardInput.mode == "AWARD_INGEST"` only — never from `intake_config.yaml` or any other mutable config.** A unit test in §11.13.2 confirms that flipping `confidence_autopromote_threshold` (or any other config field) does NOT enable ±1 page tolerance in BULK/INCREMENTAL.
- ±1 paragraph tolerance NOT extended to DOCX even at AWARD_INGEST (paragraph-index anchoring is deterministic; tolerance unnecessary).
- ±1 line tolerance NOT extended to TXT/Markdown at AWARD_INGEST (line indexing is deterministic; tolerance unnecessary).

**Position.** PRE-pre-queue. The check fires BEFORE the candidate enters `pending_facts.yaml` — the operator never sees a fabricated candidate. Reject path: write to `pipeline/validation/extractor_rejects/<org_slug>/<run_id>/<reject_id>.yaml` with full diagnostic payload (extracted_fact, source_doc, source_page or source_paragraph_id or source_line_id, attempted_quote, actual_source_bytes_at_anchor diff snippet, normalized_attempt, normalized_source, sub-tag indicating which check fired).

**Severity.** HIGH. Admin-risk ledger logged at HIGH severity per v7.0.4 §5.2.

**Composition with F-LOGICIAN-FACT-DRIFT.** F-EXTRACTOR-FABRICATION is the upstream prevention; F-LOGICIAN-FACT-DRIFT family (v7.0.4 §4) is the downstream draft-time enforcement. Together they form the no-bad-numbers structural guarantee: Intake prevents fabricated facts from entering KFR; Logician prevents drift between Scribe drafts and KFR-canonical values.

## §11.9.2 F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal (PRE)

**Purpose.** Refuse AWARD_INGEST extraction if the won-proposal artifact's operator Ed25519 signature does not verify per Section 4 §4.5 `verify_claim_evidence_map` discipline (v7.0.4 §5.3) AND the signature is not bound to the actual draft file content via SHA3-512 hash.

**Predicate.**

1. Read `submission_artifact_ref` bytes via §2 Vault read intent.
2. Read the artifact's `SignedClaimEvidenceMap` (per Section 4 v2.1 schema; lives alongside `draft_<v>.md` at `orgs/<slug>/vault/grants/<grant_id>/submission/<draft>.signed_claim_evidence_map.yaml`).
3. Verify the operator Ed25519 signature on the SignedClaimEvidenceMap per Section 4 §4.5 verify_claim_evidence_map; signature MUST be from a key currently active in Section 1 key catalog at draft-write time (per Section 4 v2.1 §4.5.2 key-currency discipline).
4. **Content-hash binding check (per RT-05 closure).** The SignedClaimEvidenceMap MUST carry a `submission_artifact_content_sha3_512` field (introduced as a Section 4 v2.x schema requirement at §11 v1 LOCK; mirrors §12 Uploader's `bundle_content_hash` precedent). Compute SHA3-512 of `submission_artifact_ref` bytes; compare against `submission_artifact_content_sha3_512`. Mismatch fires sub-tag `.hash_mismatch` (the signature-was-valid-when-signed-but-the-file-was-tampered case). If the field is absent (legacy claim-evidence-map signed before §11 v1 LOCK), refuse with sub-tag `.legacy_unhashed` and direct operator to re-sign via §11-v1-LOCK-aware Uploader before retrying.
5. Returns PASS iff signature verifies AND key was active at draft-write time AND content-hash matches.

**Sub-tags.**
- `.absent` — `SignedClaimEvidenceMap` file does not exist for this draft.
- `.signature_invalid` — signature verification failed.
- `.retired_key` — signature is from a key that was retired before draft-write time.
- `.hash_mismatch` — signature is valid but file bytes do not match the signed content hash (file was tampered post-signature).
- `.legacy_unhashed` — `SignedClaimEvidenceMap` predates the content-hash binding requirement; operator must re-sign.

**Position.** PRE. Fires BEFORE any extraction work; cheap.

**Failure path.** Refuse AWARD_INGEST + log to admin-risk ledger at HIGH severity (`TAMPER_EVENT` ledger_kind) + write `intake_state.yaml` with `mode_completed=false, failure_reason="F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal.<sub-tag>"` + exit non-zero. Operator must re-fetch a valid signed-and-content-hash-bound artifact before retrying.

**Severity.** HIGH. `TAMPER_EVENT` admin-risk-ledger kind.

## §11.9.3 F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award (PRE)

**Purpose.** Refuse AWARD_INGEST extraction if the funder's award document signature does not verify per v7.0.4 §5.3 (where applicable; funders that don't publish signing keys can be bypassed via `--award-doc-unsigned-attestation` operator flag, with the bypass logged at HIGH severity).

**Predicate.**

1. Read `award_doc_path` bytes via §2 Vault read intent.
2. Look up `vault_shared/funders/<funder_id>/signing_keys.yaml` (operator-curated per-funder, populated at first AWARD_INGEST per funder, optional). The `funder_id` is resolved from the grant's funder binding in `orgs/<slug>/vault/grants/<grant_id>/funder_binding.yaml` (per the §2 Vault topology grant-funder linkage).
3. **Branch (signed funder):** signing key found → verify award document signature against the funder's published signing key per the appropriate signature scheme (PDF digital signature: extract via `pypdf` signature subdict; DOCX embedded signature: extract via `python-docx` `signedinfo` element). Returns PASS iff signature verifies. FAIL → reject + log.
4. **Branch (unsigned funder, attestation provided):** signing key NOT found AND `award_doc_unsigned_attestation == True` → bypass; log to admin-risk ledger at HIGH severity with `attestation_bypass: true`; PASS the gate; proceed.
5. **Branch (unsigned funder, no attestation):** signing key NOT found AND `award_doc_unsigned_attestation == False` → reject; log; refuse extraction.

**Position.** PRE. Fires BEFORE any extraction work; cheap.

**Failure path.** Refuse AWARD_INGEST + log + write `intake_state.yaml` + exit non-zero (same shape as F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal).

**Severity.** HIGH. `TAMPER_EVENT` admin-risk-ledger kind for verification failures; HIGH `BYPASS_EVENT` kind for attestation bypass logs.

**Operator attestation discipline (per RT-06 closure — tamper-evident bypass).** The `--award-doc-unsigned-attestation` flag is intentionally a per-run flag, not a per-funder default. Each AWARD_INGEST invocation against an unsigned-funder award document requires operator to explicitly attest at the CLI; this prevents accidental drift toward "always bypass" patterns. The bypass log accumulates in admin-risk ledger; high-frequency bypasses against the same funder surface as a candidate for "operator should curate this funder's signing key" prompt at the next quarterly admin-risk review.

**Three structural defenses against silent bypass:**

1. **Interactive confirmation prompt.** When `--award-doc-unsigned-attestation` is supplied at the CLI, AWARD_INGEST MUST issue an interactive prompt: `Confirm unsigned-funder bypass for <funder_id> (type "BYPASS-<funder_id>" to confirm):`. Non-TTY invocation (piped input, scripted) is rejected before the prompt fires (per RT-08 TTY-check pattern). Operator must type the funder-specific token literally — no `--yes` or `--force` flag exists in v0.1.
2. **Ledger-write-before-process discipline.** The bypass log entry is written to the admin-risk ledger via the §2 Vault write intent (which is signed) **BEFORE** any extraction work proceeds. If the ledger write fails, AWARD_INGEST aborts. The ledger entry includes: `funder_id`, `award_doc_path`, `operator_key_id`, `confirmed_token` (the typed `BYPASS-<funder_id>` string), `confirmed_at_utc`. The ledger entry is hash-chained via existing M8 monotonic seq_id discipline; a wrapper script that suppresses CLI logging cannot suppress the ledger write (it goes through the Vault, not stdout).
3. **Signed-funder-keys file integrity.** `vault_shared/funders/<funder_id>/signing_keys.yaml` itself MUST be Ed25519-signed by an operator key at every write (a malicious actor cannot add a fake signing-key entry without operator-key access). Curation discipline per F-FUNDER-KEYS-SIGNATURE-INVALID (registered as a v7.0.5 §5 sub-gate at §4 v2.x amendment; cross-references §11.9.3 for completeness).

These three defenses together make silent attestation bypass structurally impossible at v0.1: an attacker would need (a) operator key access to forge signing_keys.yaml, OR (b) interactive operator presence at the CLI to type the BYPASS-<funder_id> token, OR (c) write access to the admin-risk ledger to suppress the bypass log — and (c) is already prevented by the §2 Vault write-intent signature discipline.

## §11.9.4 F-INTAKE-ORG-CROSS-REF (PRE)

**Purpose.** Path-isolation discipline. Refuse Intake invocation when any input path resolves outside the declared `org_slug` (or `org_slug` + `grant_id` for AWARD_INGEST) subtree.

**Predicate.** Per-mode:
- **BULK:** `Path.resolve(inbox_dir)` MUST sit under `orgs/<org_slug>/`.
- **INCREMENTAL:** `Path.resolve(doc_path)` MUST sit under `orgs/<org_slug>/intake/inbox/`.
- **AWARD_INGEST:** `Path.resolve(submission_artifact_ref)` MUST sit under `orgs/<org_slug>/vault/grants/<grant_id>/`. `Path.resolve(award_doc_path)` MUST sit under `orgs/<org_slug>/vault/grants/<grant_id>/award/`. Cross-grant or cross-org → fail.

**Sub-tags.**
- `.symlink_escape` — `Path.resolve()` followed a symlink to a path outside the allowed subtree.
- `.path_outside_inbox` — INCREMENTAL `doc_path` resolves outside `intake/inbox/`.
- `.award_doc_outside_vault` — AWARD_INGEST `award_doc_path` resolves outside the grant's `award/` subtree (operator must first stage the award doc into the vault via the appropriate Vault write intent).
- `.cross_grant` — AWARD_INGEST input paths reference more than one grant_id (impossible by construction at v0.1 since CLI takes `--grant <grant_id>` as a single arg, but the gate enforces structurally).

**Position.** PRE. First gate that runs after CLI input parsing; before any vector store or LLM invocation.

**Severity.** HIGH. `LAW3_VIOLATION` admin-risk-ledger kind.

## §11.9.5 F-INTAKE-INPUT-MISSING (PRE)

**Purpose.** Refuse Intake invocation when a required input file or directory does not exist on disk.

**Predicate.** Per-mode existence checks per §11.4 invariants. Sub-tags `.inbox_dir_absent`, `.doc_absent`, `.submission_artifact_absent`, `.award_doc_absent`.

**Position.** PRE. Runs after F-INTAKE-ORG-CROSS-REF (path-isolation first; existence second).

**Severity.** MEDIUM. Operator-error class (typo, missed staging step). Recoverable by operator; surface clear error message and exit non-zero.

## §11.9.6 F-INTAKE-UNSUPPORTED-FORMAT (advisory at INCREMENTAL; PRE elsewhere)

**Purpose.** Refuse processing of files with extensions not in the v1 supported set (`.pdf`, `.docx`, `.txt`, `.md`).

**Position.** PRE. Runs after F-INTAKE-ORG-CROSS-REF + F-INTAKE-INPUT-MISSING.

**INCREMENTAL behavior.** Watcher-fired INCREMENTAL invocations against unsupported-format files emit an operator notification (per §11.6.2 watcher-posture caveat) and skip processing — the file remains in `inbox/` for operator inspection or removal. This is "advisory" in the sense that the watcher does not crash on unsupported files; it gracefully logs and continues.

**BULK behavior.** Sweep skips unsupported-format files with a warning in `intake_state.yaml`. BULK does not refuse the entire run on unsupported files; it processes the supported subset and reports the skipped files.

**AWARD_INGEST behavior.** Refuses with `F-INTAKE-UNSUPPORTED-FORMAT.award_doc` if the award document is neither PDF nor DOCX. Operator must convert before retrying.

**Severity.** LOW. Advisory; operator-action-required.

**v1.1 horizon.** OQ-INTAKE-FORMATS (per §11.14) tracks the next supported-set extension wave: `.xlsx` (`openpyxl`-readable; financial statements + budget worksheets), `.csv` (native CSV; numeric registers), `.html` (BeautifulSoup-readable; web-fetched org pages), `.eml` (email-message library; partnership LOIs delivered via email). Each addition is a §11 v1.x amendment.

## §11.9.7 F-INTAKE-QUEUE-INTEGRITY (POST + PRE-run-start, per RT-12 closure)

**Purpose.** Catch queue-write integrity failures: Pydantic schema violations on the queue file, candidate-count math mismatches between state file and queue file, extractor_rejects/ count mismatches. Per RT-12 closure, ALSO catch state-file corruption between runs (the gate runs at every Intake run start, not just post-write).

**Predicate (POST — immediate post-write check).**

1. Re-read `pending_facts.yaml` (or `proposal_commitments.yaml` for AWARD_INGEST) immediately after write; Pydantic-validate. FAIL → fire.
2. Compute `candidates_in_queue_delta_this_run` from queue file (entries with `intake_run_id == current_run_id`).
3. Compute `candidates_rejected_count` from `extractor_rejects/<org_slug>/<run_id>/`.
4. Compare against `intake_state.yaml` `candidates_emitted_to_LLM` field. Math: `emitted = in_queue + rejected`. Mismatch → fire.

**Predicate (PRE-run-start — periodic sanity check per RT-12 closure).**

At the start of every Intake invocation (before any input parsing or extraction work):

1. Locate the most recent `intake_state.yaml` for the org under `orgs/<slug>/vault/kfr/intake_state/`.
2. Pydantic-validate the state file against the v1 schema. FAIL → fire `F-INTAKE-QUEUE-INTEGRITY.state_corrupted`; refuse run.
3. Re-validate candidate-count math: `state_candidates_emitted == queue_delta + reject_count_for_that_run`. Mismatch → fire `F-INTAKE-QUEUE-INTEGRITY.cross_run_drift`; refuse run.
4. If no prior state file exists (first invocation for the org), proceed without firing (legitimate new-org case).

This closes the silent-corruption path where between-run filesystem damage (admin script, disk error, partial-write recovery) leaves a malformed state file that subsequent runs would otherwise read uncritically.

**Position.** POST (immediate post-write) + PRE-run-start (sanity check). Both predicates share the same failure code with sub-tags `.post_write_pydantic_fail`, `.post_write_count_mismatch`, `.state_corrupted`, `.cross_run_drift`.

**Failure path.** Hard-block; admin-risk ledger logged at HIGH severity (queue-integrity failure indicates a Tilth-internal bug or filesystem damage, not an operator-action-required issue). Operator notification surfaces the failure with a "contact support / file a bug report" message and includes the corrupted state file path for inspection. PRE-run-start failures are explicit about which prior run's data is suspect.

**Severity.** HIGH. `INTERNAL_INTEGRITY_FAILURE` admin-risk-ledger kind.

## §11.9.8 F-INTAKE-EMBEDDING-NS-MISMATCH (PRE-tool-call, per RT-09 + RT-10 closures)

**Purpose.** Pre-tool guard for every Pydantic AI tool call against the local vector store. Asserts that the `org_slug` (and `grant_id` for AWARD_INGEST) arg passed to the tool matches the input dataclass `org_slug` (and `grant_id`) field. Closes the path where a buggy dispatcher could pass a different org_slug derived from a global default, leading to embeddings stored in the wrong namespace and cross-org vector leakage. Also closes the doc-hash collision path (RT-10) by enforcing compound-key embedding storage path.

**Predicate.**

1. Every Pydantic AI tool call against the local vector store (FAISS or Chroma client) takes `org_slug: str` (and `grant_id: str | None` for AWARD_INGEST mode) as required arguments.
2. The call wrapper compares `org_slug` arg against the calling context's `IntakeBulkInput.org_slug` / `IntakeIncrementalInput.org_slug` / `IntakeAwardInput.org_slug` field. Mismatch → fire sub-tag `.org_slug_mismatch`.
3. For AWARD_INGEST tool calls, ALSO compare `grant_id` arg against `IntakeAwardInput.grant_id`. Mismatch → fire sub-tag `.grant_id_mismatch`.
4. **Compound-key collision detect (per RT-10 closure).** Embedding storage paths use the compound key `orgs/<slug>/vault/intake/embeddings/<org_slug>_<doc_hash>/` (with org_slug prefix in the directory name). Before writing embeddings, verify the directory does not already exist for a DIFFERENT org_slug (cross-org write); if it does (theoretical doc_hash collision), fire sub-tag `.compound_key_collision`.

**Position.** PRE-tool-call. The pre-tool guard runs INSIDE the Pydantic AI tool wrapper; tool execution does not proceed if the guard fails.

**Failure path.** Hard-block; admin-risk ledger logged at HIGH severity (`LAW3_VIOLATION` ledger kind). Run aborts with `intake_state.yaml` `failure_reason="F-INTAKE-EMBEDDING-NS-MISMATCH.<sub-tag>"`.

**Severity.** HIGH. `LAW3_VIOLATION` admin-risk-ledger kind (cross-org leak class).

**Composition with v7.0.5 F-VECTOR-NS-MISMATCH.** F-INTAKE-EMBEDDING-NS-MISMATCH is the Intake-side enforcement of the v7.0.5-architecture-side F-VECTOR-NS-MISMATCH discipline. v7.0.5 says "tool calls must validate org_slug"; §11.9.8 specifies HOW for Intake's tool composition. Same pattern applies to Scout (channel G) and any other v0.1+ component that uses the local vector store; each component owns its own NS-MISMATCH gate per its substrate.

## §11.9.9 F-INTAKE-CONFIG-SIGNATURE-INVALID (PRE, per RT-07 closure)

**Purpose.** Refuse Intake invocation when `intake_config.yaml` is unsigned, has an invalid signature, or is signed by a key not currently active in the Section 1 key catalog. Closes the path where an attacker with filesystem access could replace the config with `confidence_autopromote_threshold: 0.0` (or other dangerous values) and have all candidates flow into autopromote-batch surface for one-keystroke confirmation.

**Predicate.**

1. If `intake_config.yaml` exists at `orgs/<slug>/intake/intake_config.yaml`:
   - Read the file; expect a `SignedConfig` block with `signature: str` (Ed25519, base64-encoded), `signed_by: str` (operator key ID), `signed_at_utc: datetime`, and the config payload.
   - Verify Ed25519 signature against the canonical-bytes serialization of the config payload (same canonical-JSON discipline as §0.5 amendment companion JSON files).
   - Verify `signed_by` key is currently active in Section 1 key catalog at signed_at_utc time (per Section 4 v2.1 §4.5.2 key-currency discipline).
2. Returns PASS iff the file exists AND signature verifies AND key was active. If file does not exist, return PASS (the hardcoded 0.85 default applies; no config write means no attack surface).

**Sub-tags.**
- `.signature_absent` — file exists but no SignedConfig block.
- `.signature_invalid` — signature verification failed.
- `.retired_key` — signed by a key that was retired before the config write timestamp.
- `.canonical_bytes_mismatch` — config payload bytes do not match the signed canonical-JSON representation (whitespace tampering attempt).

**Position.** PRE. Runs at config read time, BEFORE input bundle construction.

**Failure path.** Refuse Intake invocation + log to admin-risk ledger at HIGH severity + clear operator-facing error message ("intake_config.yaml signature invalid; re-sign with operator key or remove the file to fall back to v1 hardcoded defaults"). No `intake_state.yaml` is written for this failure (the run never started).

**Severity.** HIGH. `TAMPER_EVENT` admin-risk-ledger kind.

**Per-run CLI override fallback.** Per RT-08 closure, per-run CLI override via `--confidence-threshold <float>` does NOT require a signed config (CLI is operator-interactive by definition; argparse-time validation rejects out-of-range values). The CLI parser explicitly rejects `--yes`, `--auto-confirm`, and `--force` at v0.1 (these are NOT valid args; their absence is asserted in the test matrix §11.13).

## §11.9.10 F-INTAKE-EMBEDDING-ENDPOINT-INVALID (PRE-tool-call, per RT-13 closure)

**Purpose.** Refuse embedding tool invocation when the configured embedding endpoint is not localhost or unix:// socket. Closes the path where a malicious operator (or a misconfigured `router.yaml`) could point the embedding client at a cloud endpoint and silently exfiltrate raw document text to an external service.

**Predicate.**

1. Embedding tool configuration is read from a sealed Golden-Image-baked location: `/etc/tilth/embedding_endpoint.yaml` (per ADR-001 substrate freeze; runtime override prohibited; the file is part of the Golden Image build and is operator-read-only). Per-deployment customization happens at Golden Image build time, not at appliance runtime.
2. Validate that the `endpoint` field resolves to one of:
   - `http://localhost:<port>/...` (loopback IPv4)
   - `http://127.0.0.1:<port>/...` (loopback IPv4 explicit)
   - `http://[::1]:<port>/...` (loopback IPv6)
   - `unix:///path/to/socket` (Unix domain socket on this host)
3. Any other endpoint scheme or hostname → fire fail-closed.

**Position.** PRE-tool-call. The pre-tool guard runs INSIDE the Pydantic AI embedding tool wrapper; embedding does not proceed if the endpoint is not localhost.

**Failure path.** Hard-block; admin-risk ledger logged at HIGH severity (`SOVEREIGNTY_VIOLATION` ledger kind — non-local endpoint is a phone-home attempt). Run aborts with `intake_state.yaml` `failure_reason="F-INTAKE-EMBEDDING-ENDPOINT-INVALID"`. Operator notification surfaces the failure with the configured endpoint string and a directive to rebuild the Golden Image with a localhost-only endpoint config.

**Severity.** HIGH. `SOVEREIGNTY_VIOLATION` admin-risk-ledger kind.

## §11.9.11 F-INTAKE-WATCHER-TOCTOU (PRE-file-open, per RT-11 closure)

**Purpose.** Refuse file open if the path resolves to a symlink at the moment of open, OR if the resolved path no longer matches the original PRE-gate-validated path (TOCTOU window where an attacker swaps the file for a symlink between PRE-gate `Path.resolve()` and the actual file read).

**Predicate.**

1. After PRE-gate `Path.resolve()` validates the path is in the allowed subtree (per §11.9.4):
2. Verify `path.is_file()` AND `not path.is_symlink()` immediately before opening.
3. Open the file with `os.open(path, os.O_RDONLY | os.O_NOFOLLOW)`. The `O_NOFOLLOW` flag makes `os.open` raise `OSError(ELOOP)` if the path is a symlink at the moment of open. Catch and convert to gate failure.
4. Re-validate `Path.resolve()` after open; the post-open resolve MUST equal the pre-open resolve. Mismatch fires (covers the case where a symlink was swapped between resolve and open in a window briefer than the kernel's symlink check).

**Position.** PRE-file-open. The check runs in the file-open wrapper used by the BULK sweep, INCREMENTAL handler, and watcher; every parser call (pypdf, python-docx, native read) routes through this wrapper.

**Failure path.** Hard-block; admin-risk ledger logged at HIGH severity (`LAW3_VIOLATION` ledger kind — symlink swap is a cross-org attack vector). Run aborts with `intake_state.yaml` `failure_reason="F-INTAKE-WATCHER-TOCTOU"`. The original file remains in `intake/inbox/` for operator inspection (Intake does NOT delete or quarantine TOCTOU-flagged files; operator must investigate the swap manually).

**Severity.** HIGH. `LAW3_VIOLATION` admin-risk-ledger kind.

**Audit-trail relationship to F-INTAKE-ORG-CROSS-REF.symlink_escape.** F-INTAKE-WATCHER-TOCTOU is the runtime detection of a symlink-attack-in-progress; F-INTAKE-ORG-CROSS-REF.symlink_escape is the PRE-gate detection of a symlink already in place at PRE-gate time. Both fire on related but distinct attack sequences; preserved as distinct codes per §10 explode-pattern precedent for audit-trail clarity. A single attack may fire one OR the other depending on attack timing relative to PRE-gate; the test matrix §11.13.4 covers both.

# §11.10 Routing posture (per v7.0.7 + v7.0.10)

**Always-local. Hard-coded. Not operator-overridable at Classification Review.** Per v7.0.7 LOCKED + v7.0.10 LOCKED retentions §3, Intake's per-call routing is on the always-local agents list under all three v7.0.10 customer-facing postures (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign). The operator's posture selection at Classification Review step 3 governs Scribe / Editor / Judge / Red Team / Scout routing; Intake's always-local discipline is structural and independent of posture.

**Rationale.** Intake processes raw operator-uploaded org documents (BULK + INCREMENTAL) and won-proposal artifacts (AWARD_INGEST). These contain mixed-classification content by default — annual reports may be Public; 990s are Public; audited financials are Confidential; employee rosters are Confidential; partnership LOIs are Confidential by default until operator declassifies; won proposals contain the full final draft including any Confidential applicant-specific substance. No subset of Intake's input is safely cloud-routable without per-file operator classification at upload time, and v0.1 has no per-file pre-classification UX.

**Local LLM call.** The extraction LLM (Mistral 7B class per §11.8) runs locally on operator hardware. No cloud frontier model is invoked at any step of any mode.

**Vector store.** Local FAISS or Chroma per §11.8. No cloud vector store. No third-party embedding service.

**Sealed embedding endpoint (per RT-13 closure).** The embedding tool's endpoint configuration is read from a sealed Golden-Image-baked location (`/etc/tilth/embedding_endpoint.yaml` per ADR-001 substrate freeze), validated against a localhost-or-unix-socket allowlist, and refused if the endpoint is anything else. F-INTAKE-EMBEDDING-ENDPOINT-INVALID (§11.9.10) is the deterministic enforcement. Per-deployment customization of the embedding endpoint happens at Golden Image build time, NOT at appliance runtime — operator cannot edit `router.yaml` (or any other runtime config) to redirect the embedding client to a cloud mirror. This closes the silent-exfil-via-misconfigured-endpoint path.

**Pre-tool guard on every vector-store call (per RT-09 closure).** F-INTAKE-EMBEDDING-NS-MISMATCH (§11.9.8) is a PRE-tool-call gate: every Pydantic AI tool call against the local vector store is wrapped to assert the `org_slug` (and `grant_id` for AWARD_INGEST) tool arg matches the input dataclass field; mismatch fails closed. Closes the path where a buggy dispatcher passes a global default org_slug and embeddings land in the wrong namespace. Compound-key embedding storage path (`<org_slug>_<doc_hash>` under each org's vault subtree) closes the doc-hash-collision cross-org-leak path (RT-10).

**Token cost.** Bounded local. Per-doc embedding + extraction cost scales with doc size; one Pydantic AI extraction agent invocation per doc; structured-output bounds the LLM to candidate-fact rows. Logician gate predicates are deterministic Python; AST-lint is deterministic static analysis. No external API token cost at any point.

**v7.0.7 + v7.0.10 LOCK status.** v7.0.7 LOCKED 2026-05-10 confirmed always-local Intake routing per the classification register's `intake → always_local` entry. v7.0.10 LOCKED 2026-05-11 introduced the three-posture customer-facing vocabulary (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign) but left Intake's always-local discipline unchanged across all three postures. The dispatch packet WS-E contingency for posture-changing amendments did not fire; no §11 v1.0.1 amendment is required for v7.0.10.

# §11.11 PROJECT_CONTEXT migration (per v7.0.4 §6 + §6.1)

Pre-v7.0.4: PROJECT_CONTEXT.md held both narrative substance (mission, history, partnerships) and quantitative substance (`[NEEDED]` fields for EIN, UEI, enrollment counts, revenue, etc.). Post-v7.0.4: PROJECT_CONTEXT.md keeps narrative substance only; quantitative substance migrates to KFR with structured schema.

**Migration trigger (per §11.14 default OQ-3).** Intake at first operator review post-LOCK per v7.0.4 §6.1 sequencing rule. The operator's first SP0 review (per v7.0.4 §3) for any current org triggers Intake-driven migration of that org's `[NEEDED]` quantitative fields from `PROJECT_CONTEXT.md` to KFR.

**Migration discipline.** Per v7.0.4 §6.1:
- Orgs migrate in `orgs/ORG_INDEX.md` listing order (first-listed first).
- Each org's first SP0 review post-LOCK is the migration trigger for that org.
- PROJECT_CONTEXT.md edits stage in the same operator-signed `sp0_delta` per v7.0.4 §3.1 — the migration is one delta per org, not per fact.
- Migration is bounded to one grant cycle per org (operator can defer to a later cycle if SP0 prompts for migration during a deadline-pressed cycle); deferred migrations carry to the next cycle's SP0.

**Intake's role in migration.** At the migration trigger, Intake runs in a special **MIGRATION_BULK_INGEST** invocation (operationally identical to BULK_INGEST per §11.6.1 but scoped to the org's existing `PROJECT_CONTEXT.md` as the sole source doc). Intake extracts every `[NEEDED]` numeric/quantitative field, produces candidate KFR entries with `source_doc=PROJECT_CONTEXT.md`, `source_page=null` (markdown is unpaged; F-EXTRACTOR-FABRICATION uses line-bounded section anchoring instead of page anchoring for markdown source docs), `source_quote=verbatim line containing the field`. Operator review at SP0 confirms each migrated entry under the same operator-confirmation discipline as standard BULK_INGEST. Confirmed entries promote to KFR; PROJECT_CONTEXT.md is operator-edited (out of band of Intake) to remove the migrated fields and retain only narrative substance.

**Migration is not autonomous.** Intake does not silently rewrite PROJECT_CONTEXT.md — operator owns that edit. Intake produces the candidate KFR entries; operator confirms them at SP0; operator (separately) edits PROJECT_CONTEXT.md to remove the migrated fields. The two-step decoupling preserves Law 5 (operator owns substance) and Rule 3 (be explicit — Intake's scope is "produce KFR candidates," not "rewrite PROJECT_CONTEXT.md").

**Step-by-step migration narrative (per E-4 closure).** For each org in `orgs/ORG_INDEX.md` listing order, at the org's first SP0 review post-§11 LOCK:

1. **SP0 entry.** Operator runs `tilth pipeline sp0-review --org <slug> --grant <grant_id>` for any in-flight grant cycle. SP0 detects the §11 v1 LOCK has landed AND `orgs/<slug>/vault/kfr/migration_state.yaml` does not exist (or carries `status: PENDING`). SP0 surfaces a migration prompt: "v7.0.4 KFR migration available; migrate org <slug>'s PROJECT_CONTEXT.md `[NEEDED]` numeric fields to KFR? (y/N/defer)".
2. **Operator decision.** y → proceed to step 3. defer → SP0 writes `migration_state.yaml` with `status: DEFERRED, deferred_at_utc, deferred_for_grant: <grant_id>`; migration re-prompts at next cycle's SP0. N → SP0 writes `migration_state.yaml` with `status: SKIPPED_OPERATOR_DECLINED, declined_at_utc`; no further auto-prompt; operator can manually invoke later via `tilth intake migration --org <slug>`.
3. **Intake MIGRATION_BULK_INGEST invocation.** SP0 invokes Intake in MIGRATION_BULK_INGEST mode (operationally identical to BULK_INGEST per §11.6.1 but scoped to `orgs/<slug>/PROJECT_CONTEXT.md` as the sole source doc). The mode flag is read from `IntakeBulkInput.migration_target_path == "orgs/<slug>/PROJECT_CONTEXT.md"` (NOT a fourth dispatcher mode; see §11.6.0 table note).
4. **Candidate review at SP0.** Migration candidates are presented in the operator-review surface (§11.7) as a single-doc batch — no autopromote-batch view (every migration candidate requires per-candidate operator review regardless of confidence_score; rationale: PROJECT_CONTEXT migrations are foundational facts that warrant explicit operator attention). Operator confirms each candidate; confirmed candidates promote to KFR with `validation.confirmed_by, validation.confirmed_when, audit_chain` initialized.
5. **PROJECT_CONTEXT.md edit (operator-owned, separate step).** After operator-confirmed migration candidates promote to KFR, the SP0 surface displays a list of "fields to remove from PROJECT_CONTEXT.md per migrated KFR entries." Operator opens `PROJECT_CONTEXT.md` in their preferred editor (Tilth does NOT auto-edit) and removes the migrated fields manually. Operator-signed sp0_delta records the migration as a single batch per v7.0.4 §3.1 (one delta per org, not per fact). On sp0_delta sign, `migration_state.yaml` updates to `status: COMPLETED, completed_at_utc, migrated_field_count, sp0_delta_id`.

The two-step (Intake produces, operator confirms; operator separately edits MD) decoupling is the Law 5 enforcement mechanism. Intake's scope is bounded; operator's substance ownership is bounded; sp0_delta is the audit trail.

# §11.12 Pipeline placement

Per v7.0.4 SP0 + v7.0.6 amendment pipeline placement:

```
ONBOARDING (one-time per org)
  Intake BULK_INGEST → operator review → KFR populated → ready for first grant cycle
                                                      ↓
                    (PROJECT_CONTEXT migration triggered at first SP0 post-LOCK per v7.0.4 §6.1)

CONTINUOUS OPERATIONS (any time)
  operator drops doc → Intake INCREMENTAL_INGEST (watcher OR operator-explicit) → operator review at next available time → KFR delta promoted

GRANT CYCLE (per submission)
  SP0 KFR Freshness Review (per v7.0.4 §3 — required-for-funder gaps + stale-fact refresh)
    → operator-signed sp0_delta → KGIE → SP1 → drafting → SP2/SP3/SP4 → operator sign-off → Uploader (§12)

AWARD ACCEPTANCE (per won grant)
  operator marks proposal WON → Intake AWARD_INGEST (signature-verify + extract commitments)
    → operator structuring review → operator promote → proposal_commitments.yaml ready
                                                     ↓
                          (Report Generator §14 v0.2 consumes promoted file at reporting cycles)
```

Intake does NOT participate in the §5 inner revision loop. It does NOT fire on eval_mode or report_mode runs (eval_mode reads existing KFR; report_mode is Report Generator, §14, v0.2). Its triggers are: white-glove onboarding (BULK once per org; MIGRATION_BULK at first SP0 post-LOCK per v7.0.4 §6.1), continuous operations (INCREMENTAL on watcher fire or operator command), award acceptance (AWARD_INGEST on operator command per won grant).

# §11.13 Test matrix

Tests live at `tests/seats/intake/`. Each test is a deterministic unit test — no LLM calls (the local extraction LLM is mocked in unit tests; integration tests stub the local-LLM endpoint), no network calls (enforced by `test_intake_zero_network_egress`), no cross-org reads.

## §11.13.1 Mode dispatch tests (v1)

- `test_bulk_ingest_invokes_with_org_slug`: invoke `bulk_ingest(IntakeBulkInput(...))`; assert mode dispatcher routes to BULK handler; assert state file written under `orgs/<slug>/vault/kfr/intake_state/<run_id>.yaml`.
- `test_incremental_ingest_invokes_with_doc_path`: invoke `incremental_ingest(IntakeIncrementalInput(...))`; assert mode dispatcher routes to INCREMENTAL handler; assert single-doc processing.
- `test_incremental_ingest_watcher_trigger_recorded`: invoke with `trigger="watcher"`; assert state file `trigger` field == `"watcher"`.
- `test_incremental_ingest_operator_explicit_trigger_recorded`: invoke with `trigger="operator_explicit"`; assert state file `trigger` field == `"operator_explicit"`.
- `test_award_ingest_invokes_with_grant_id`: invoke `award_ingest(IntakeAwardInput(...))`; assert mode dispatcher routes to AWARD handler; assert pre-extraction signature verification trail file written.
- `test_three_modes_register_in_dispatcher`: introspect the mode dispatcher; assert exactly three modes registered (BULK_INGEST, INCREMENTAL_INGEST, AWARD_INGEST); assert no fourth mode silently leaked through type-checker holes.

## §11.13.2 F-EXTRACTOR-FABRICATION tests (v1, updated for RT-01 / RT-02 / RT-03 / RT-04 closures)

- `test_f_extractor_fabrication_exact_match_pass`: candidate quote == source bytes at page; assert PASS.
- `test_f_extractor_fabrication_unicode_nfc_pass`: candidate quote uses combining accent (NFD); source bytes use composed accent (NFC); assert PASS after NFC normalization.
- `test_f_extractor_fabrication_whitespace_collapse_pass`: candidate quote has multiple internal spaces; source bytes have single spaces (or vice versa); assert PASS after whitespace normalization.
- `test_f_extractor_fabrication_ocr_substitution_reject_in_bulk`: candidate quote has "0" where source bytes have "O"; mode=BULK_INGEST; assert REJECT (`F-EXTRACTOR-FABRICATION.ocr_substitution`).
- `test_f_extractor_fabrication_ocr_substitution_reject_in_incremental`: same, mode=INCREMENTAL_INGEST; assert REJECT.
- `test_f_extractor_fabrication_page_off_by_one_reject_in_bulk`: candidate quote at source_page=5 but actually appears at page 6; mode=BULK_INGEST; assert REJECT (`F-EXTRACTOR-FABRICATION.page_mismatch`).
- `test_f_extractor_fabrication_page_off_by_one_pass_in_award_with_flag`: candidate quote at source_page=5 but actually appears at page 6; mode=AWARD_INGEST + page_tolerance_applied=true; assert PASS with operator-flag set on the row.
- `test_f_extractor_fabrication_ellipsis_substring_reject`: candidate quote contains "..." not present in source bytes; mode=any; assert REJECT (`F-EXTRACTOR-FABRICATION.ellipsis_substring`).
- `test_f_extractor_fabrication_reject_writes_audit_trail`: assert reject path writes complete reject_id.yaml with extracted_fact, source_doc, source_page or source_paragraph_id or source_line_id, attempted_quote, normalized_attempt, normalized_source, reject_reason_code (sub-tag), rejected_at_utc.
- `test_f_extractor_fabrication_pre_pre_queue_position`: assert reject candidates do NOT appear in pending_facts.yaml; assert PASS candidates DO appear; assert operator_review_surface never displays reject candidates.

**Cycle 1 closure tests (per RT-01 + RT-02 + RT-03 + RT-04):**

- `test_f_extractor_fabrication_unique_page_match` (RT-01): PDF source_doc has the candidate quote on page 3 AND page 7 (boilerplate header); candidate declares source_page=3; assert REJECT with sub-tag `.multiple_page_match` UNLESS multiple_page_match=true is set.
- `test_f_extractor_fabrication_unique_page_match_operator_override` (RT-01): same fixture as above with multiple_page_match=true; assert PASS but `autopromote_batch=false` regardless of confidence_score.
- `test_f_extractor_fabrication_first_occurrence_not_declared_page` (RT-01): candidate quote is a genuine substring of declared page 5 BUT also occurs on page 2 (first occurrence); assert REJECT with sub-tag `.page_mismatch` (closes the boilerplate-coincidence bypass).
- `test_f_extractor_fabrication_markdown_multiline_reject` (RT-02): candidate source_quote contains '\n'; mode=BULK_INGEST + format=md; assert REJECT with sub-tag `.markdown_multiline` at gate time AND at Pydantic validation time (defense-in-depth).
- `test_f_extractor_fabrication_markdown_line_anchor_pass` (RT-02): candidate source_quote is a single line that exactly matches `source_doc_lines[source_line_id]` after NFC + whitespace normalization; assert PASS.
- `test_f_extractor_fabrication_docx_paragraph_index_pass` (RT-03): DOCX source with `source_paragraph_id=4`; quote matches paragraphs[4].text; assert PASS regardless of declared `source_page` value.
- `test_f_extractor_fabrication_docx_paragraph_index_mismatch_reject` (RT-03): DOCX source with `source_paragraph_id=4`; quote is in paragraphs[5]; assert REJECT with sub-tag `.docx_paragraph_mismatch`.
- `test_f_extractor_fabrication_mode_from_input_bundle_only` (RT-04): write `intake_config.yaml` with a fictional `extra_award_tolerance: true` field; invoke BULK_INGEST with a candidate that would only PASS at AWARD_INGEST tolerance (off-by-one page); assert REJECT (config field has no effect on tolerance — only `IntakeAwardInput.mode == "AWARD_INGEST"` enables the tolerance).
- `test_f_extractor_fabrication_mode_immutability_against_threshold_flip` (RT-04): flip `confidence_autopromote_threshold` to 0.0 in config; invoke BULK_INGEST with off-by-one candidate; assert REJECT (threshold has no effect on F-EXTRACTOR-FABRICATION tolerance).

## §11.13.3 F-EXTRACTOR-AWARD-SIGNATURE-INVALID tests (v1)

- `test_f_extractor_award_signature_proposal_pass`: submission artifact has valid operator Ed25519 signature from active key; assert PASS.
- `test_f_extractor_award_signature_proposal_fail_invalid_sig`: submission artifact signature does not verify; assert REJECT (`F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal`); assert state file shows mode_completed=false; assert no proposal_commitments.yaml written.
- `test_f_extractor_award_signature_proposal_fail_retired_key`: submission artifact signed by key that was retired before draft-write timestamp; assert REJECT.
- `test_f_extractor_award_signature_award_pass_signed_funder`: award doc has valid funder signature against published key; assert PASS.
- `test_f_extractor_award_signature_award_fail_signed_funder`: award doc signature does not verify against published key; assert REJECT (`F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award`).
- `test_f_extractor_award_signature_award_unsigned_funder_no_attestation`: award doc unsigned, attestation flag=false; assert REJECT.
- `test_f_extractor_award_signature_award_unsigned_funder_with_attestation`: award doc unsigned, attestation flag=true; assert PASS with admin-risk ledger entry logging bypass.
- `test_f_extractor_award_signature_pre_extraction_position`: assert signature gate fires BEFORE any extraction work (no LLM call observed; no embedding work observed); assert state file shows pre-extraction failure.

## §11.13.4 F-INTAKE-ORG-CROSS-REF + F-INTAKE-WATCHER-TOCTOU + F-INTAKE-EMBEDDING-NS-MISMATCH tests (v1)

- `test_f_intake_org_cross_ref_symlink_escape_bulk`: inbox_dir is a symlink to a path outside `orgs/<slug>/`; assert REJECT sub-tag `.symlink_escape`.
- `test_f_intake_org_cross_ref_path_outside_inbox_incremental`: doc_path outside `orgs/<slug>/intake/inbox/`; assert REJECT sub-tag `.path_outside_inbox`.
- `test_f_intake_org_cross_ref_award_doc_outside_vault`: award_doc_path outside `orgs/<slug>/vault/grants/<grant_id>/award/`; assert REJECT sub-tag `.award_doc_outside_vault`.
- `test_f_intake_org_cross_ref_cross_grant_award`: award_doc_path under a different grant_id than the submission_artifact_ref; assert REJECT sub-tag `.cross_grant`.
- `test_f_intake_org_cross_ref_runs_first`: assert ORG-CROSS-REF check fires BEFORE F-INTAKE-INPUT-MISSING (path-isolation precedes existence).

**F-INTAKE-WATCHER-TOCTOU tests (per RT-11 closure):**

- `test_f_intake_watcher_toctou_symlink_at_open`: file is a regular file at PRE-gate; between PRE-gate and file-open, replace it with a symlink pointing outside the org subtree; assert open fails with `OSError(ELOOP)` from `os.O_NOFOLLOW`; assert F-INTAKE-WATCHER-TOCTOU fires.
- `test_f_intake_watcher_toctou_post_open_resolve_mismatch`: simulate a swap where post-open `Path.resolve()` differs from pre-open `Path.resolve()`; assert F-INTAKE-WATCHER-TOCTOU fires with sub-tag `.post_open_resolve_mismatch`.
- `test_f_intake_watcher_toctou_atomic_open_succeeds_for_clean_file`: regular file with no swap; assert open succeeds and extraction proceeds normally.

**F-INTAKE-EMBEDDING-NS-MISMATCH tests (per RT-09 + RT-10 closures):**

- `test_f_intake_embedding_ns_mismatch_org_slug`: dispatcher passes `org_slug="org_b"` to a vector store tool call invoked from an `IntakeBulkInput(org_slug="org_a")` context; assert F-INTAKE-EMBEDDING-NS-MISMATCH fires with sub-tag `.org_slug_mismatch`.
- `test_f_intake_embedding_ns_mismatch_grant_id`: AWARD_INGEST dispatcher passes `grant_id="grant_b"` to a vector store tool call invoked from an `IntakeAwardInput(grant_id="grant_a")` context; assert sub-tag `.grant_id_mismatch`.
- `test_f_intake_embedding_compound_key_collision`: simulate doc_hash collision across two orgs (force same SHA-256 doc_hash); assert second write fires sub-tag `.compound_key_collision`.
- `test_f_intake_embedding_storage_path_compound_key`: assert embedding storage path matches `orgs/<slug>/vault/intake/embeddings/<org_slug>_<doc_hash>/` pattern (org_slug prefix in directory name; not bare `<doc_hash>`).

## §11.13.5 Mode-specific output tests (v1)

- `test_bulk_writes_pending_facts_yaml`: BULK_INGEST run produces `pending_facts.yaml` Pydantic-valid against pending_facts.v1 schema.
- `test_bulk_appends_across_runs`: two BULK_INGEST runs against the same org; assert pending_facts.yaml contains entries from both runs (intake_run_id distinguishes); assert no entry overwritten.
- `test_incremental_appends_to_existing_queue`: INCREMENTAL after BULK; assert INCREMENTAL entries appended (not overwriting BULK entries).
- `test_award_writes_proposal_commitments_yaml_pending_status`: AWARD_INGEST run produces `proposal_commitments.yaml` with `status: PENDING_OPERATOR_REVIEW`; assert Report Generator (mock) refuses to consume PENDING file.
- `test_award_promote_flips_status`: simulate operator promotion (CLI invocation `award-promote`); assert status flips to PROMOTED; assert audit_chain initialized with operator_signature_at_award_ingest_completion.

## §11.13.6 Confidence autopromote tests (v1)

- `test_confidence_autopromote_threshold_default`: candidate with confidence_score=0.86, threshold=0.85; assert `autopromote_batch=true`.
- `test_confidence_autopromote_threshold_below`: candidate with confidence_score=0.84, threshold=0.85; assert `autopromote_batch=false`.
- `test_confidence_autopromote_threshold_per_org_override`: org config sets threshold=0.90; candidate with confidence_score=0.87; assert `autopromote_batch=false` (org override binds).
- `test_confidence_autopromote_cli_override`: CLI `--confidence-threshold 0.70`; candidate with confidence_score=0.75; assert `autopromote_batch=true` (CLI override binds).
- `test_autopromote_batch_does_not_silent_write_kfr`: assert no KFR canonical write happens at Intake invocation; assert KFR canonical write only happens via `tilth intake review` operator-confirm action.

## §11.13.7 Watcher tests (v1)

- `test_watcher_fires_on_new_file`: simulate file write to `orgs/<slug>/intake/inbox/`; assert watcher invokes incremental_ingest with `trigger="watcher"`.
- `test_watcher_skips_partial_write`: simulate file write that takes 5 seconds; assert watcher waits for file-stability + handle-release before invoking.
- `test_watcher_per_org_isolation`: spawn watchers for two orgs; write file to org_a inbox; assert ONLY org_a watcher fires.
- `test_watcher_unsupported_format_advisory`: write `.xlsx` to inbox; assert watcher emits notification but does NOT invoke incremental_ingest; assert file remains in inbox.
- `test_watcher_pre_gate_fail_logs_notification`: write doc that fails F-INTAKE-INPUT-MISSING (e.g., zero-byte file); assert watcher writes notification under `orgs/<slug>/intake/notifications/<run_id>.txt`; assert file remains in inbox.

## §11.13.8 PROJECT_CONTEXT migration tests (v1)

- `test_migration_bulk_extracts_needed_fields`: PROJECT_CONTEXT.md with `[NEEDED]` fields for EIN, UEI, enrollment_fy24; invoke MIGRATION_BULK_INGEST; assert candidate KFR entries produced with source_doc=PROJECT_CONTEXT.md, source_page=null, source_quote=line-bounded.
- `test_migration_does_not_rewrite_project_context`: assert MIGRATION_BULK_INGEST does NOT modify PROJECT_CONTEXT.md (operator-owned edit per §11.11).
- `test_migration_org_index_ordering`: assert migration trigger respects orgs/ORG_INDEX.md listing order (first-listed first).
- `test_migration_one_delta_per_org`: assert single sp0_delta covers the org's full migration (not per-fact deltas).

## §11.13.9 Integration tests (v1)

- `test_end_to_end_bulk_ingest_seeded_org`: seeded test org with 3 small docs (1 PDF, 1 DOCX, 1 MD); invoke BULK_INGEST; assert pending_facts.yaml has expected candidate count, all candidates pass F-EXTRACTOR-FABRICATION, audit trail consistent, state file complete.
- `test_end_to_end_incremental_then_bulk_review`: seed inbox with 1 doc; INCREMENTAL fires; then BULK adds 2 more docs; review surface displays all 3 docs' candidates partitioned by autopromote_batch.
- `test_end_to_end_award_ingest_seeded_grant`: seeded won grant with operator-signed draft + funder-signed award doc; AWARD_INGEST extracts commitments; operator-review-promote round-trip; assert PROMOTED proposal_commitments.yaml consumable by Report Generator stub.
- `test_intake_zero_network_egress`: full Intake run inside sandbox with all network egress blocked (Linux network namespace with no veth, or test-process socket monkey-patch raising on `socket.socket()`); assert run completes with all LLM calls hitting localhost-bound local-LLM endpoint and zero outbound connections.
- `test_intake_cic_clc_orthogonality`: invoke Intake schema + extraction prompt against the v7.0.8 four detection layers (lexical regex / Pydantic AST / value-set / KP schema); assert F-CIC-CLC-COUPLING-VIOLATION audit clean.

## §11.13.10 New gate tests from Cycle 1 closures (v1)

**F-INTAKE-CONFIG-SIGNATURE-INVALID tests (per RT-07 closure):**

- `test_f_intake_config_signature_unsigned_rejected`: `intake_config.yaml` exists but has no SignedConfig block; assert F-INTAKE-CONFIG-SIGNATURE-INVALID sub-tag `.signature_absent` fires; Intake invocation refused.
- `test_f_intake_config_signature_invalid_rejected`: SignedConfig block present but signature does not verify; assert sub-tag `.signature_invalid`.
- `test_f_intake_config_signature_retired_key_rejected`: SignedConfig signed by a key retired before the config write timestamp; assert sub-tag `.retired_key`.
- `test_f_intake_config_canonical_bytes_mismatch`: config payload bytes do not match the signed canonical-JSON representation (whitespace tampering attempt); assert sub-tag `.canonical_bytes_mismatch`.
- `test_f_intake_config_absent_falls_back_to_hardcoded_default`: `intake_config.yaml` does not exist; assert Intake proceeds with hardcoded 0.85 default; no gate fires.
- `test_f_intake_config_cli_override_no_signature_required`: CLI invocation with `--confidence-threshold 0.90`; assert override binds without requiring signed config.
- `test_f_intake_cli_yes_flag_rejected`: CLI invocation with `--yes`; assert argparse rejection at parse time.
- `test_f_intake_cli_auto_confirm_flag_rejected`: CLI invocation with `--auto-confirm`; assert argparse rejection.
- `test_f_intake_cli_force_flag_rejected`: CLI invocation with `--force`; assert argparse rejection.

**F-INTAKE-EMBEDDING-ENDPOINT-INVALID tests (per RT-13 closure):**

- `test_f_intake_embedding_endpoint_localhost_pass`: sealed config has `endpoint: http://localhost:8765/embed`; assert PASS.
- `test_f_intake_embedding_endpoint_127_0_0_1_pass`: endpoint `http://127.0.0.1:8765/embed`; assert PASS.
- `test_f_intake_embedding_endpoint_unix_socket_pass`: endpoint `unix:///tmp/embed.sock`; assert PASS.
- `test_f_intake_embedding_endpoint_external_hostname_rejected`: endpoint `http://api.openai.com/v1/embeddings`; assert F-INTAKE-EMBEDDING-ENDPOINT-INVALID fires; embedding tool refuses.
- `test_f_intake_embedding_endpoint_runtime_override_prohibited`: simulate router.yaml override to point at a remote endpoint; assert sealed config takes precedence; gate fires if override succeeds.

**F-INTAKE-QUEUE-INTEGRITY pre-run-start tests (per RT-12 closure):**

- `test_f_intake_queue_integrity_pre_run_start_state_corrupted`: corrupt `intake_state.yaml` between runs (write malformed YAML); next invocation fires F-INTAKE-QUEUE-INTEGRITY sub-tag `.state_corrupted` at run start.
- `test_f_intake_queue_integrity_pre_run_start_count_drift`: corrupt state file count math between runs; next invocation fires sub-tag `.cross_run_drift` at run start.
- `test_f_intake_queue_integrity_first_invocation_no_prior_state`: first invocation for a new org with no prior state file; assert no gate fires (legitimate empty-state case).

**F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal.hash_mismatch tests (per RT-05 closure):**

- `test_f_extractor_award_signature_proposal_hash_mismatch`: SignedClaimEvidenceMap is valid AND signature verifies AND key is current AND `submission_artifact_content_sha3_512` field present; mutate the draft_<v>.md bytes after signing; AWARD_INGEST recomputes hash and detects mismatch; assert sub-tag `.hash_mismatch` fires.
- `test_f_extractor_award_signature_proposal_legacy_unhashed`: SignedClaimEvidenceMap predates §11 v1 LOCK and lacks `submission_artifact_content_sha3_512` field; assert sub-tag `.legacy_unhashed` fires; operator-facing message directs re-sign.

**F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award tamper-evident bypass tests (per RT-06 closure):**

- `test_f_extractor_award_unsigned_attestation_interactive_prompt`: invoke AWARD_INGEST with `--award-doc-unsigned-attestation` flag against an unsigned-funder award doc; assert interactive prompt fires asking operator to type `BYPASS-<funder_id>`; assert non-TTY input rejects.
- `test_f_extractor_award_unsigned_attestation_ledger_write_before_process`: simulate ledger write failure during attestation bypass; assert AWARD_INGEST aborts BEFORE any extraction work proceeds.
- `test_f_extractor_award_unsigned_attestation_signed_funder_keys_required`: tamper with `vault_shared/funders/<funder_id>/signing_keys.yaml` to add a fake signing key without operator signature; assert F-FUNDER-KEYS-SIGNATURE-INVALID (cross-reference v7.0.5 §5) fires before AWARD_INGEST verification proceeds.

## §11.13.11 v1.x horizon tests (NOT registered at v1)

The following tests land at §11 v1.x amendments alongside the corresponding feature additions:

- `test_intake_supports_xlsx`: BULK_INGEST processes `.xlsx` per OQ-INTAKE-FORMATS v1.1 expansion.
- `test_intake_supports_csv`: BULK_INGEST processes `.csv` per OQ-INTAKE-FORMATS v1.1 expansion.
- `test_intake_ocr_integration`: BULK_INGEST runs Tesseract on PDF with bad OCR layer; produces re-OCR'd source bytes that pass F-EXTRACTOR-FABRICATION (per OQ-INTAKE-OCR v0.1.x).
- `test_award_ingest_admin_risk_advisory_scan`: AWARD_INGEST commitment_text passes through §7.11 admin-risk scanner; flagged terms surface as advisory to operator review (per §11.2 Law 4 v1.1 horizon).

# §11.14 Open questions resolved and deferred

## §11.14.1 Resolved at v1

- **OQ-1: BULK-mode operator review UX (per dispatch packet §WS-E open question).** RESOLVED at v1 with default per dispatch packet: confidence-threshold autopromote ≥0.85 + batch-confirm by source doc for the rest. Per §11.7 + §11.5.1. Threshold is operator-tunable per-org via `intake_config.yaml`; CLI override per-run available. Autopromote is operator-confirmed-batch (one keystroke after spot check), NOT silent-auto-write — preserves the operator-confirmation discipline structurally.
- **OQ-2: INCREMENTAL trigger (per dispatch packet §WS-E open question).** RESOLVED at v1 with default per dispatch packet: filesystem watcher AND operator-explicit, both. Per §11.6.2. Watcher implementation uses `watchdog` library at v0.1; per-org watcher process; daemonization is operator-curated per OS. Operator-explicit invocation always available regardless of watcher state.
- **OQ-3: Migration of existing PROJECT_CONTEXT [NEEDED] fields (per dispatch packet §WS-E open question).** RESOLVED at v1 with default per dispatch packet: Intake at first operator review post-LOCK per v7.0.4 §6.1. Per §11.11. MIGRATION_BULK_INGEST mode invokes during the first SP0 review post-§11 LOCK for each org in `orgs/ORG_INDEX.md` listing order; one sp0_delta per org; deferrable to next cycle if SP0 prompts during a deadline-pressed cycle.

## §11.14.2 Open questions for next-round attention

- **OQ-INTAKE-FORMATS: v1.1 supported-format expansion.** v1 supports `.pdf`, `.docx`, `.txt`, `.md`. v1.1 candidate set: `.xlsx` (`openpyxl`-readable), `.csv` (native), `.html` (BeautifulSoup), `.eml` (email-message library). Each extension addition requires a §11 v1.x amendment registering the parser tool + per-format chunking strategy + per-format F-EXTRACTOR-FABRICATION normalization extension.
- **OQ-INTAKE-OCR: v0.1.x OCR integration.** v1 rejects PDFs with bad OCR layer (per F-EXTRACTOR-FABRICATION exact-match semantics). v0.1.x candidate: integrate Tesseract as the local OCR substrate (Tesseract ships per ADR-001 envelope). Integration is Code work + a §11 v0.1.x amendment registering the OCR tool + the re-OCR'd source bytes flow into F-EXTRACTOR-FABRICATION.
- **OQ-INTAKE-WATCHER-DAEMON: v0.1.x watcher daemonization.** v1 defines watcher posture but treats daemonization as operator-curated per OS. v0.1.x candidate: ship per-OS daemonization scripts (systemd unit for Linux, launchd plist for macOS, Windows Service spec) + per-org watcher config. Code work + a §11 v0.1.x amendment.
- **OQ-INTAKE-INCREMENTAL-AWARD: v0.2 AWARD_INGEST watcher.** v1 AWARD_INGEST is operator-explicit only. v0.2 candidate: filesystem-watcher trigger for AWARD_INGEST when an operator-stages-award-doc file lands under `orgs/<slug>/vault/grants/<grant_id>/award/`. Requires operator-trigger-vs-watcher disambiguation surface (does the watcher fire AWARD_INGEST automatically, or surface a notification asking operator to invoke?). Defer to v0.2 WS-E follow-up.
- **OQ-INTAKE-VECTOR-STORE-CHOICE: FAISS vs Chroma at white-glove.** v1 substrate envelope per ADR-001 includes both. Operator selection at white-glove. v0.1.x candidate: ship a per-org-default selection mechanism via `intake_config.yaml` `vector_store: Literal["faiss", "chroma"]` field. Code work + minor §11 v0.1.x amendment.
- **OQ-INTAKE-LLM-EXTRACTION-PROMPT: prompt versioning.** v1 fixes the extraction prompt at the §11.8 substrate envelope (no operator-tunable prompt). Future v1.x candidate: prompt versioning under `pipeline/engineering/intake/extraction_prompt_v<N>.md` with operator-curated per-org prompt selection (some orgs may benefit from a domain-specific extraction prompt). Defer until evidence of need from white-glove deployments.

# §11.15 Companion edits at LOCK

The following edits land in the same commit as §11 v1 LOCK (compound paired-commit per §6.17 Option-B):

1. **§0.5 §11 amendment** — `pipeline/blueprint/v0.1/section_00_5_section_11_intake_amendment.md` — final inventory **24 rows at v1** post-Cycle-1 closures (per the explode-pattern §10 / §12 precedent applied to F-EXTRACTOR-* + F-INTAKE-* failure-codes):
   - 1 marker row (kind=`marker`): `blueprint.section_anchor.s11_intake.v1`
   - 5 schema/contract rows: `intake.bulk_input.v1`, `intake.incremental_input.v1`, `intake.award_input.v1`, `intake.pending_facts_queue.v1`, `intake.proposal_commitments.v1`
   - 11 failure-code rows (kind=`failure-code`): `intake.failure_code.F-EXTRACTOR-FABRICATION.v1`, `intake.failure_code.F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal.v1`, `intake.failure_code.F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award.v1`, `intake.failure_code.F-INTAKE-ORG-CROSS-REF.v1`, `intake.failure_code.F-INTAKE-INPUT-MISSING.v1`, `intake.failure_code.F-INTAKE-UNSUPPORTED-FORMAT.v1`, `intake.failure_code.F-INTAKE-QUEUE-INTEGRITY.v1`, `intake.failure_code.F-INTAKE-EMBEDDING-NS-MISMATCH.v1` (NEW per RT-09 + RT-10 closures), `intake.failure_code.F-INTAKE-CONFIG-SIGNATURE-INVALID.v1` (NEW per RT-07 closure), `intake.failure_code.F-INTAKE-EMBEDDING-ENDPOINT-INVALID.v1` (NEW per RT-13 closure), `intake.failure_code.F-INTAKE-WATCHER-TOCTOU.v1` (NEW per RT-11 closure)
   - 7 pre-gate-check / post-gate-check rows: `intake.pre_gate.path_isolation.v1` (consolidates F-INTAKE-ORG-CROSS-REF + F-INTAKE-INPUT-MISSING + F-INTAKE-UNSUPPORTED-FORMAT per §4 v2.2 consolidated-check pattern), `intake.pre_gate.award_signature.v1` (consolidates F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal + .award), `intake.pre_gate.verbatim_match.v1` (backs F-EXTRACTOR-FABRICATION; runs PRE-pre-queue per candidate; substrate-dispatched per §11.9.1.A/B/C/D), `intake.pre_gate.embedding_ns_match.v1` (NEW; backs F-INTAKE-EMBEDDING-NS-MISMATCH; PRE-tool-call), `intake.pre_gate.config_signature.v1` (NEW; backs F-INTAKE-CONFIG-SIGNATURE-INVALID), `intake.pre_gate.embedding_endpoint.v1` (NEW; backs F-INTAKE-EMBEDDING-ENDPOINT-INVALID; PRE-tool-call), `intake.pre_gate.toctou_safe_open.v1` (NEW; backs F-INTAKE-WATCHER-TOCTOU; PRE-file-open)
   - (Existing pre/post-gate rows for path_isolation + award_signature + verbatim_match + queue_integrity preserved; queue_integrity now also fires PRE-run-start per RT-12 closure — no new row, additional position annotation.)

   **§0.5 row range note.** §11 LOCKs first per WS-E; §12 v1 amendment is filed at SCOPING DRAFT but not LOCKed. §11 claims rows **233–256** (24 rows; skipping the §12-reserved 212–232 range to avoid collision; if §12 LOCKs after §11, §12's rows hold per its filed amendment). If §12 is withdrawn or renumbered, §11's claim is unaffected.

2. **§4 Logician v2.x amendment (WS-L)** — registers F-EXTRACTOR-FABRICATION + F-EXTRACTOR-AWARD-SIGNATURE-INVALID family + F-INTAKE-ORG-CROSS-REF + F-INTAKE-INPUT-MISSING + F-INTAKE-UNSUPPORTED-FORMAT + F-INTAKE-QUEUE-INTEGRITY + F-INTAKE-EMBEDDING-NS-MISMATCH + F-INTAKE-CONFIG-SIGNATURE-INVALID + F-INTAKE-EMBEDDING-ENDPOINT-INVALID + F-INTAKE-WATCHER-TOCTOU at the Logician PRE/POST sequence (Code session is authoring this in parallel; this blueprint is the authority on the gate codes + sub-tags + exact-match semantics). Updated total: **11 Intake-owned codes** (was 7).

3. **`orgs/_TEMPLATE/intake/` scaffold** — template directory for new client orgs:
   - `orgs/_TEMPLATE/intake/inbox/` (empty directory + `.gitkeep`)
   - `orgs/_TEMPLATE/intake/intake_config.yaml` (operator-tunable per-org config: `confidence_autopromote_threshold: 0.85`, `vector_store: faiss`, `watcher_enabled: false` defaults)
   - `orgs/_TEMPLATE/intake/notifications/` (empty directory + `.gitkeep`)
   - `orgs/_TEMPLATE/vault/kfr/intake_state/` (empty directory + `.gitkeep` — per-run state files land here)

4. **Module scaffold** — `pipeline/orchestrator/seats/intake.py`:
   - Frozen kw_only Pydantic dataclasses for `IntakeBulkInput`, `IntakeIncrementalInput`, `IntakeAwardInput`, `IntakeState`, `PendingFact`, `ProposalCommitment`, `GateResult`.
   - Mode dispatcher with the three modes registered (BULK_INGEST, INCREMENTAL_INGEST, AWARD_INGEST).
   - `f_extractor_fabrication` predicate stub (full implementation downstream by Code session per WS-E Code phase).
   - `f_extractor_award_signature_invalid_proposal` + `f_extractor_award_signature_invalid_award` predicate stubs.
   - `f_intake_org_cross_ref` predicate stub.
   - Module passes AST-lint clean (no `requests.post`, no `httpx`, no `socket`, no raw `subprocess` to non-allow-list targets).

5. **Test suite** — `tests/seats/intake/skeleton_tests.py` per §11.13 — at LOCK ceremony, the skeleton tests validate the three modes register in the dispatcher and the v1 gate codes resolve to imported predicates. Full per-gate test population is downstream (Code session per WS-E Code phase).

6. **Memory file** — `memory/project_blueprint_section_11_intake_locked.md` — written at LOCK ceremony per the standard memory pattern.

7. **MEMORY.md prepend** — index entry for the §11 LOCK.

8. **lock_history row** — appended to `pipeline/engineering/lock_history.v1.jsonl` with `lock_class=blueprint`, `module=pipeline.blueprint.v0_1.section_11_intake`, `parent_lock_row=178` (v7.0.4 LOCK), `unblocks=["WS-J §14 Report Generator (proposal_commitments.yaml is now stable input schema)", "WS-L §4 Logician v2.x (registers Intake gate family)"]`.

9. **daily_log entry** — `daily_logs/2026-05-10.md` — per the standard daily_log pattern (LOCK ceremony summary + companion edits + unblocks).

10. **session_metrics line** — appended to `pipeline/metrics/session_log.jsonl` per `pipeline/metrics/SESSION_METRICS_SPEC.md`.

---

End of §11 Intake blueprint. Thesis Cycles 1+2 ran in this session under LIVE FULL CROSS-FAMILY rigor per WS-D v7.0.5 precedent; LOCK ceremony at the same compound transaction.
