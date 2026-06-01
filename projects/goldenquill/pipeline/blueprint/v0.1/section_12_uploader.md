---
title: Blueprint §12 Uploader — submission package assembly (v1 LOCKED 2026-05-10)
filed: 2026-05-09
locked: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 — L-005 strict two-cycle PASS per `pipeline/validation/v12_v1_thesis_2026-05-09/audit_v2_synthesis.md` with FULL live cross-family rigor (Editor=Llama 3.3 70B/Groq, Judge=Gemini-2.5-Pro/Google, Red Team=GPT-OSS-120B/Groq). Compound-LOCKed per §6.17 Option-B paired-commit pattern with `section_00_5_section_12_uploader_amendment.md` (§0.5 v9 — 21 rows promote PARENT_UNLOCKED → STABLE) + `section_04_v2_x_uploader_gates_amendment.md` (§4 v2.7).
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                      # v7 LOCKED 2026-04-19 — A1-A12
  - pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md                  # v7.0.6 roster — Uploader named as v0.1 support agent; prepare-and-stage discipline
  - pipeline/blueprint/v0.1/section_02_vault_topology.md                         # v7.1 LOCKED — Uploader writes submission packages via Vault-owned primitives; never raw open()
  - pipeline/blueprint/v0.1/section_04_logician.md                               # v2.1 LOCKED — Uploader's PRE/POST gates enforced by Logician; v2.7 amendment registers F-UPLOADER-* family + R-UPLOADER-NO-SUBMIT AST-lint
  - pipeline/blueprint/v0.1/section_05_pipeline.md                               # v6 LOCKED — Uploader consumes §5 submission_mode terminus output (SubmissionBundle)
  - pipeline/blueprint/v0.1/section_06_operating_envelope.md                     # v1-r1 LOCKED — format-conversion utilities; prompt-template compilation pipeline
  - pipeline/blueprint/v0.1/section_07_scribe.md                                 # v1.1.1 LOCKED — Uploader consumes SectionDraft + claim_evidence_map emitted by Scribe; §7.11 admin-risk scanner is the v1.1 forward-dep for attachment text scanning
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md               # §0.5 v5 LOCKED — Uploader primitives row-append at paired §0.5 §12 amendment companion-file
prerequisite_interlock: pipeline/blueprint/v0.1/section_05_pipeline.md (§5 v6 LOCKED — Uploader receives the SubmissionBundle at the submission_mode terminus; §5 v7 amendment wires Red Team into the inner loop; Uploader fires AFTER operator sign-off on the council's final verdict).
companion_module: pipeline/orchestrator/seats/uploader.py (scaffold authored at §12 LOCK; per-portal adapter modules at pipeline/orchestrator/seats/uploader_adapters/).
companion_amendment: pipeline/blueprint/v0.1/section_00_5_section_12_uploader_amendment.md (paired-commit at §12 v1 LOCK per §6.17 Option-B).
downstream_siblings_out_of_scope: §13 Data Collector, §14 Report Generator (both v0.2 horizon). §12 pins the submission-assembly contract; it does NOT spec post-award reporting.
prefix_pass_changelog_2026_05_09:
  - "HIGH-1 F-UPLOADER-AUTOSUBMIT-ATTEMPTED defense rewritten across all three layers (AST-lint allow-list, network-namespace process isolation, RuntimeError + dual __post_init__/vault-write-time invariant check). See §12.9.3."
  - "HIGH-2 attachments fully deferred to v1.1 pending §2 v7.2 attachments sub-kind LOCK. §12.6 rescoped to v1.1 horizon; §12.4 input contract drops the attachments field at v1; §12.10 adapters lose attachment-handling references at v1; §12.13 attachment-tampered/-missing tests deferred to v1.1 wave. See §OQ-12.4 for the §2-v7.2-paired alternative path."
  - "HIGH-3 adapter scope honest-cut to four (Grants.gov + SAM.gov + Common Grant App + copy_paste). Foundant / Submittable / Fluxx adapter sections moved to v0.1.x deferral footer at §12.10. Per-funder config curation pipeline tracked at §OQ-12.6."
  - "HIGH-4 Law 4 cell forecloses honestly at v1 (no text generation, no attachment text); §12 v1.1 plan adds F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED POST-attachment-stage gate citing §7.11 admin-risk scanner — gate NOT registered at v1."
  - "HIGH-5 portal field disambiguation honest-cut to small local-LLM call (Mistral 7B class, always-local, 5–50 fields per submission); cloud routing prohibited. New PRE-gate F-UPLOADER-FIELD-MAP-CLOUD-ROUTED registered at v1."
  - "MEDIUM 1 §12.4 spec'd submission-bundle-read Vault read intent for the F-UPLOADER-SIGNATURE-MISSING predicate's bytes-source."
  - "MEDIUM 2 path normalization invariant added at §12.4; cross-org content-surface scanning deferred to v0.2 at §OQ-12.5."
  - "MEDIUM 3 §12.3 PRE-gate failure persistence path spec'd (uploader_state.yaml writes on PRE-gate fail before assembly)."
  - "MEDIUM 4 uploader_state.yaml moved out of submission_package/ to orgs/<slug>/vault/grants/<grant_id>/uploader_state/<run_id>.yaml."
  - "MEDIUM 5 §12.8 content-mutation tolerance model spec'd (whitespace collapse, page-break un-pagination, table structural-hash); benchmarked VAPG fixture committed to v1.1."
  - "MEDIUM 6 added integration test test_uploader_zero_network_egress (sandbox-network-blocked Uploader run + socket monkey-patch / packet-capture assertion)."
  - "LOW 1 four portal adapters at v0.1 first ship wording unified across §12.1 / §12.10 / §12.13 / §12.15."
  - "LOW 2 punch-list cite reformatted to L-019 form: pipeline/planning/v0_2_agents_punch_list_2026-05-09.md §5.2 OQ-1."
  - "LOW 3 OQ-12.X items renumbered OQ-12.1 through OQ-12.6 in order."
  - "LOW 4 §12.1 reworded (per decision 8c default — operator confirmation pending)."
  - "LOW 5 §12.13.1 test_f_uploader_format_mismatch_* split into three sub-tag tests."
  - "LOW 6 §12.15 §0.5 row-count aligned with companion amendment (final inventory: 1 marker + 4 schema/contract + 10 failure-code + 6 pre/post-gate-check = 21 rows at v1)."
audit_1_changelog_2026_05_10:
  - "RT-1a/b §12.9.3 Layer 1 — explicit eval/exec/compile/__import__/pickle/marshal/object.__setattr__/socket/multiprocessing/etc. NOT-in-allow-list block-named for foreclosure clarity; AST attribute-chain resolution discipline documented; aliased-import normalization called out."
  - "RT-1c §12.9.3 Layer 2 — re-tagged Linux-ASPIRATIONAL / macOS-ASPIRATIONAL per L-006; explicit Layer-existence-audit table; correctness load on all platforms is Layer 1 + Layer 3."
  - "RT-1d/e §12.9.3 Layer 3 — struck the `Vault.write_uploader_output` redundant-check claim (function does not exist on disk); corrected the `dataclasses.replace` misconception (CPython re-fires __post_init__); pointed at `tests/seats/uploader/test_uploader_dataclasses_replace_closure.py` as test of record."
  - "RT-1f/g/h §12.9.3 — added explicit out-of-Layer-3-scope bypass treatment (object.__setattr__, pickle, marshal, subclass override); UploaderOutput finalized via `@typing.final` + `__init_subclass__`-raise; Layer 1 forecloses any in-uploader-code attacker call site."
  - "RT-2a §12.7 readiness checklist item 2 — explicit operator-facing-only / not Vault-persisted / not exported to portal-package note added."
  - "RT-4a §12.2 Law 4 cell — added LibreOffice headers/footers/page-numbers cross-reference clarifying boilerplate inheritance from Scribe-authored DOCX (already §7.11-scanned upstream); Uploader does not insert content."
  - "RT-4b §12.2 Law 4 cell — v1.1 horizon extended to include admin-risk scan over portal_fields.yaml LLM-disambiguated values (defense-in-depth)."
  - "RT-5a §12.9.6 — inline `FieldMapCallContext` schema definition added; covered by `uploader.pre_gate.field_map_routing.v1` row 229 per consolidation pattern (no new §0.5 row); wiring discipline + Pydantic AI `before_model_request` hook documented."
  - "RT-5b §12.11 — `always_local: hard_coded` constraint tagged as v7.0.7-LOCK-bound; cross-reference to v7.0.7 §6 reservation; F-UPLOADER-FIELD-MAP-CLOUD-ROUTED catches any wrapper escape until v7.0.7 LOCKs."
  - "RT-5c §12 LOCK-ceremony companion edit — predicate file `pipeline/logician/gates/f_uploader_field_map_cloud_routed.py` authored as v1-LOCK companion (was placeholder). EXISTS at compound-LOCK time."
  - "L-006 companion-edit existence audit — `orgs/_TEMPLATE/uploader/` scaffold dirs + `orgs/_TEMPLATE/vault/grants/_TEMPLATE_GRANT/uploader_state/` dir + `tests/seats/uploader/test_uploader_zero_network_egress.py` stub authored as v1-LOCK companion edits per §12.15."
  - "Editor E3 §12 §12.9 — brief inline 'explode pattern' clarification added at first reference."
---

# §12.1 Purpose and scope

Uploader is the **submission package assembly** support agent of the Tilth pipeline. Its job is to take the operator-approved final proposal — the output of the §5 Pipeline submission_mode terminus after council review (Scribe → Editor → Judge → Red Team → operator sign-off) — and assemble it into the format(s) required by the target funder portal, stage the package for operator review, and surface a submission-readiness checklist. **Uploader does NOT auto-submit.** The operator clicks final submit on the funder portal. This constraint is non-negotiable — it derives from federal portal Terms of Service (Grants.gov Workspace requires human submission attestation) and the operator-accountability principle that the applicant, not the tool, bears legal responsibility for the submission.

**v0.1 scope.** One support agent type: end-of-cycle submission package assembler. One input shape: the `SubmissionBundle` from §5 submission_mode terminus plus the signed `claim_evidence_map` and the `RfaExtractedRecord` (for portal field mapping). One output shape: a staged submission package under `orgs/<slug>/vault/grants/<grant_id>/submission_package/` containing portal-format documents, filled portal field exports, and a submission-readiness checklist surfaced to the operator. Operator-uploaded attachments (resumes, financial statements, letters of support, certifications, forms) are **deferred to v1.1** pending §2 v7.2 `attachments` sub-kind LOCK — at v1 the operator manually attaches non-Tilth-generated files at portal upload time after reviewing the staged narrative + portal_fields export. See §12.6 and §OQ-12.4.

**Adapter scope (per decision 8c default — operator confirmation pending).** Four portal adapters at v0.1 first ship:

1. **Grants.gov Workspace** — federal mandatory. SF-424 family field mapping per Grants.gov submission rules (PDF required, filename conventions). At v1, operator manually attaches SF-424A/B/C and any required attachments at portal upload time after reviewing the narrative package.
2. **SAM.gov** — federal registration/certification. Entity validation + representation-letter staging.
3. **Common Grant Application** — foundation standard. Covers a large share of US foundation portals.
4. **Copy-paste fallback** — for any portal not covered by adapters 1–3. Exports the canonical submission package as a structured YAML field map + document set that the operator manually enters into the portal. Every field carries a clear label, the source section, and the value to paste.

Foundation-platform adapters (Foundant / Submittable / Fluxx) are **deferred to v0.1.x** pending the per-funder config curation pipeline (§OQ-12.6) — stub adapters without curated per-funder field-mapping tables would mislead the operator. See §12.10 footer.

**Out of scope for v0.1 (explicit non-goals).** Uploader does NOT submit. Uploader does NOT generate proposal text (that is Scribe, §7). Uploader does NOT score (Judge, §9; Red Team, §10). Uploader does NOT ingest documents (Intake, §11). Uploader does NOT produce reports (Report Generator, §14). Uploader does NOT interact with portal APIs for live submission — every portal interaction at v0.1 is offline assembly; the operator pastes or uploads into the portal manually. Live portal API integration is a v0.2+ roadmap item gated on per-portal API access agreements and ToS review.

**Substance comes from the council (Laws 1 + 5).** Uploader does not generate content. Every byte in the submission package traces to the council's signed output. At v1 there is no operator-uploaded-attachment surface inside Uploader (deferred per §12.6); at v1.1, attachments enter via the §2 v7.2 `attachments` sub-kind with provenance schema. Uploader is a mechanical assembler, not a creative agent.

# §12.2 Five Operating Laws — enforcement mapping

Framework: per `pipeline/templates/component_analysis_template.md`

Each of the Five Laws is enforced by a combination of PRE-gates (Logician, before Uploader processes the bundle), in-seat discipline (Uploader's own assembly contract), and POST-gates (Logician, after Uploader stages the package). Failure codes are enumerated in §12.9.

**Law 1 — RFA is the source of truth.**
- PRE-gate: `F-UPLOADER-RFA-MISSING` — Logician refuses the run if the `RfaExtractedRecord` is absent from the input bundle or if its `rfa_content_sha3_512` does not match the session manifest pin.
- In-seat: Uploader's portal field mapping is driven entirely by `RfaExtractedRecord.section_structure` + `RfaExtractedRecord.required_attachments`. Every portal field traces to an RFA-extracted requirement. Uploader never invents portal fields not in the RFA.
- POST-gate: `F-UPLOADER-PACKAGE-INCOMPLETE` — Logician walks the `RfaExtractedRecord.section_structure` against the staged submission package manifest; any RFA-required narrative section missing from the package → hard-block. (At v1 the `required_attachments` walk is informational only — operator manually attaches; at v1.1 the walk hard-blocks.)

**Law 2 — No boundary drift.**
- PRE-gate: Uploader's scope is mechanically bounded — it processes the `SubmissionBundle` contents and nothing else. No web search, no cross-grant reference, no content generation. Path normalization (`Path.resolve()`) runs on every input path; symlinks are rejected.
- In-seat: Uploader's assembly logic reads the `SubmissionBundle.section_drafts`. It does NOT add content, remove content, or modify content beyond format conversion (e.g., docx-to-pdf rendering). Any content mutation beyond format rendering would trip `F-UPLOADER-CONTENT-MUTATION` (§12.9).
- POST-gate: `F-UPLOADER-CONTENT-MUTATION` — deterministic diff between input `SectionDraft.body_text` and output document extracted text under the §12.8 tolerance model; non-whitespace / non-format-artifact delta → hard-block. Uploader is a renderer, not an editor.

**Law 3 — Org isolation.**
- PRE-gate: `F-UPLOADER-ORG-CROSS-REF` — Logician refuses the run if the input bundle references more than one `orgs/<slug>/` path. One grant_id per Uploader session. All input paths are `Path.resolve()`-normalized; any path that resolves outside the bundle's declared `org_slug` subtree → hard-block.
- In-seat: Uploader reads from exactly one `orgs/<slug>/vault/grants/<grant_id>/` subtree.
- POST-gate: `F-LOGICIAN-S10A-NO-ORG-ATTRIBUTES` (forwarded from §4) — submission package scanned for cross-org slug references; package blocked on leakage. Semantic content-surface scanning (looking for another org's *substantive content* having leaked into this org's narrative through an upstream bug) is deferred to v0.2 — see §OQ-12.5.

**Law 4 — Apolitical sector language + admin-risk term scanning.**
- PRE-gate: N/A at v1 — Uploader does not generate text. The council's POST-gates (`F-SCRIBE-ADMIN-RISK-UNFLAGGED`, §7.11) have already enforced Law 4 on all narrative content before it reaches Uploader.
- In-seat: Uploader does NOT modify text content. Format conversion (docx-to-pdf) is a rendering operation that preserves content byte-for-byte at the text layer per §12.8 tolerance model. Uploader does NOT code-switch, does NOT substitute terms, does NOT rewrite.
- POST-gate: text content is the council's signed output; any mutation including dialect-shift would trip `F-UPLOADER-CONTENT-MUTATION`. **Honest scope foreclosure at v1:** because attachments are deferred (§12.6) and Uploader generates no prose, the Law 4 enforcement surface inside Uploader is closed. **Boilerplate inheritance from rendered DOCX:** LibreOffice headless rendering inherits headers, footers, and page-numbering directly from the source DOCX. Any admin-risk-laden text in those positions was authored upstream by Scribe (§7.5) or applied via an org's DOCX template, both of which are scanned by `F-SCRIBE-ADMIN-RISK-UNFLAGGED` (§7.11) before the bundle reaches Uploader. The §12.8.1 tolerance model excludes page-number footers and repeated headers from the body-text diff specifically because those positions are deterministically inherited from the source — Uploader does not insert content into them. **v1.1 horizon:** when attachments land, the new POST-attachment-stage gate `F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED` fires the §7.11 admin-risk scanner on extracted attachment text; any Severity ≥ Medium term without an operator-acknowledged `[ADMIN-RISK:flag]` in attachment metadata → hard-block. The same v1.1 horizon adds an admin-risk pass over `portal_fields.yaml` LLM-disambiguated values (per §12.11) as defense-in-depth — even though the source values trace to already-scanned upstream content, an audit pass on the Uploader-emitted output catches drift. (Both v1.1 gates NOT registered at v1; documented here so the §7 v1 fix precedent — `five_laws_cell_silently_delegated` per §7 v1.1.1 closeout — is not repeated when attachments land.)

**Law 5 — Applicant brings the substance.**
- PRE-gate: `F-UPLOADER-SIGNATURE-MISSING` — operator-approval signature on the final draft (architecture §D.5 v3 role expansion) must be present in the input bundle. Uploader refuses to assemble a package the operator has not signed off on. The signature predicate reads `submission_bundle_bytes` via the §2-owned `submission-bundle-read` Vault read intent (§12.4).
- In-seat: Every document in the submission package traces to a `SectionDraft` from the signed `SubmissionBundle`. No fabricated content. (At v1.1, attachments add a second provenance-tracked source per §12.6 v1.1 horizon.)
- POST-gate: Manifest integrity check — every file in the staged package is enumerated in `submission_manifest.yaml` with source provenance and content hash. Files not in the manifest → hard-block. Files in the manifest not on disk → hard-block.

# §12.3 Four Autonomy Rules — enforcement mapping

**Rule 1 — Save state always.** Uploader persists `UploaderState` to `orgs/<slug>/vault/grants/<grant_id>/uploader_state/<run_id>.yaml` on every assembly attempt — both success and failure. State includes: assembly timestamp, adapter used, sections assembled, sections failed, readiness checklist result, failure reason if applicable.

**PRE-gate failure persistence.** When Uploader is invoked but a PRE-gate (§12.9 PRE codes) fails before assembly starts, Uploader writes `uploader_state.yaml` (at the path above) with `assembly_succeeded=False, sections_assembled=(), failure_reason=<gate_code>, failure_detail=<predicate_message>`. No partial submission package is written; no manifest is written; the operator surface receives the gate-fail result with the same self-validation-result envelope as a successful run, just with `overall_status="not_ready"` and the failure code surfaced. This guarantees Rule 1 holds even when Uploader never reaches assembly.

**Rule 2 — Test your own work.** Before marking the package "ready for operator review," Uploader runs the readiness checklist (§12.7) — a deterministic self-validation pass that checks completeness, format compliance, file sizes, page counts, filename conventions, and manifest integrity. The checklist result is persisted alongside the package.

**Rule 3 — Be explicit.** Uploader's input contract (§12.4) declares exact paths, formats, and done-definitions. Uploader's output contract (§12.5) declares exact output paths, manifest schema, and readiness-checklist format.

**Rule 4 — Clean output.** Submission package contains only portal-required documents and metadata. No markdown fences, no LLM self-commentary, no Tilth-internal artifacts. `submission_manifest.yaml` is Pydantic-validated before write. Portal field export YAML is schema-validated per adapter.

# §12.4 Input contract

Uploader fires at the §5 Pipeline submission_mode terminus, AFTER the operator has signed off on the council's final verdict. Uploader is the last step before the operator goes to the funder portal.

**Input bundle (`UploaderInput`, frozen, kw_only):**
- `run_id: str` — §5 Pipeline run-scoped UUID; pins the input bundle to the completed council run.
- `grant_id: str` — funder-program identifier for vault path resolution.
- `org_slug: str` — client org slug for vault path resolution.
- `submission_bundle_ref: str` — vault path to the signed `SubmissionBundle` from §5 submission_mode terminus. `Path.resolve()` is called at PRE-gate; the resolved path MUST sit under `orgs/<org_slug>/vault/grants/<grant_id>/`. Symlink ingest is rejected.
- `section_drafts: tuple[SectionDraft, ...]` — finalized, operator-signed drafts from Scribe (§7.5); ordered by `section_order` ascending.
- `claim_evidence_map: tuple[ClaimEvidence, ...]` — flattened claim-evidence map across all sections.
- `rfa_extracted_record: RfaExtractedRecord` — Phase 0 RFA extraction (§7.3); drives portal field mapping, required-attachments checklist, section-structure validation.
- `operator_signature: OperatorSignature` — the operator's sign-off on the final draft. Contains `signed_at_utc`, `signer_id`, `bundle_content_hash` (SHA3-512 of the `SubmissionBundle` bytes).
- `target_portal: Literal["grants_gov", "sam_gov", "common_grant_app", "copy_paste"]` — selects the portal adapter. Operator-set at Uploader invocation; defaults to `"copy_paste"` if not specified. (Foundation-platform values `"foundant" | "submittable" | "fluxx"` are NOT in the v1 Literal — added at v0.1.x per §OQ-12.6.)
- `portal_config: PortalConfig | None` — per-portal configuration overrides. `None` for `grants_gov`, `sam_gov`, `common_grant_app`, and `copy_paste` (those use RFA-derived configuration only).
- `prepared_at_utc: datetime`.

**Note on attachments at v1.** The `attachments: tuple[AttachmentRef, ...]` field is **NOT present at v1** per §12.6 deferral. It is reintroduced at v1.1 alongside §2 v7.2 `attachments` sub-kind LOCK. At v1, Uploader's package contains only narrative + portal field export; the operator attaches non-Tilth files (resumes, SF-424 forms, financials, etc.) at portal upload time.

**Bundle invariants (PRE-gate enforced).**
- `operator_signature.bundle_content_hash` MUST equal the SHA3-512 hash of the `SubmissionBundle` bytes on disk at `submission_bundle_ref`. The bytes are read via the §2-owned `submission-bundle-read` Vault read intent (intent name: `submission-bundle-read`; path: `orgs/<slug>/vault/grants/<grant_id>/submission_bundle.yaml`; capability: read-only). Mismatch → `F-UPLOADER-SIGNATURE-MISSING` (subclass `.hash_mismatch`; bundle was modified after operator sign-off; hard-block). The legacy `F-UPLOADER-SIGNATURE-MISMATCH` code is preserved for audit-trail clarity but folds into the same predicate at the check level.
- `claim_evidence_map` MUST be the union of `section_drafts[*].claim_evidence_map` — inconsistency → `F-UPLOADER-INPUT-INCONSISTENT`.
- `rfa_extracted_record.rfa_content_sha3_512` MUST match the session manifest pin — mismatch → `F-UPLOADER-RFA-MISSING`.
- `submission_bundle_ref` (after `Path.resolve()`) MUST sit under `orgs/<org_slug>/vault/grants/<grant_id>/`. Path-traversal-by-symlink → `F-UPLOADER-ORG-CROSS-REF` (subclass `.symlink_escape`).

# §12.5 Output contract

**Output directory.** `orgs/<slug>/vault/grants/<grant_id>/submission_package/` — one directory per grant submission attempt. Versioned by `run_id` if multiple attempts exist.

**State directory (separate from package).** `orgs/<slug>/vault/grants/<grant_id>/uploader_state/<run_id>.yaml` — Tilth-internal artifact per Rule 1. NOT inside `submission_package/` — the package is what the operator hand-uploads to the portal; uploader_state is internal-only and must not leak into the operator's portal upload.

**Output artifacts (under `submission_package/<run_id>/`):**

1. **`submission_manifest.yaml`** — Pydantic-validated manifest listing every file in the package with:
   - `file_name: str` — as staged on disk.
   - `portal_file_name: str` — filename required by the portal (portal conventions may differ from Tilth naming).
   - `format: Literal["pdf", "docx", "xlsx", "yaml", "txt", "other"]`.
   - `source: Literal["council_draft", "portal_field_export", "readiness_checklist"]`. (At v1.1, `"attachment"` is added to the Literal; not at v1.)
   - `source_ref: str` — vault path to the source artifact (SectionDraft path).
   - `content_sha3_512: str` — hash of the staged file.
   - `page_count: int | None` — for PDF/DOCX; `None` for non-paginated formats.
   - `file_size_bytes: int`.
   - `portal_section: str | None` — which portal section this file maps to (from `RfaExtractedRecord.section_structure`).

2. **Portal-format documents** — council drafts rendered into the portal-required format:
   - If portal requires PDF: docx-to-pdf conversion via the format-conversion utility (§12.8).
   - If portal requires DOCX: pass-through (Scribe's native output format per §7.5).
   - If portal requires plain text: text extraction from DOCX with formatting stripped.
   - Page-count and file-size validation against RFA limits (§12.7 readiness checklist).

3. **Portal field export** — `portal_fields.yaml` — a structured YAML file mapping every portal form field to its value, source, and instructions:
   - `field_id: str` — portal-specific field identifier.
   - `field_label: str` — human-readable label.
   - `value: str` — the value to enter (extracted from `RfaExtractedRecord`, `PROJECT_CONTEXT`, or `SectionDraft` per the adapter's field-mapping table; portal-field disambiguation may invoke a small local-LLM call per §12.11).
   - `source: str` — provenance (e.g., `"RFA:program_name"`, `"PROJECT_CONTEXT:organization.legal_name"`, `"SectionDraft:executive_summary:paragraph_1"`).
   - `instructions: str` — adapter-specific instructions for the operator (e.g., "Paste into Grants.gov Workspace field 'Project Abstract'").

4. **Readiness checklist** — `readiness_checklist.yaml` — the self-validation result (§12.7).

(At v1.1, `attachment_manifest.yaml` is added per §12.6 v1.1 horizon. Not at v1.)

# §12.6 Attachment provenance — DEFERRED TO v1.1

**v1 scope:** Operator-uploaded attachments are NOT staged by Uploader at v0.1 first ship. Operator manually attaches non-Tilth-generated files (SF-424 family forms, organizational charts, resumes, letters of support, audited financial statements, certifications, maps) directly at portal upload time after reviewing the staged narrative + portal_fields export. The §12.7 readiness checklist surfaces a "manual-attach checklist" listing every entry in `RfaExtractedRecord.required_attachments` so the operator has a visible to-do list when they reach the portal.

**Why deferred.** The original v1 SCOPING DRAFT pinned `attachments: tuple[AttachmentRef, ...]` against an `attachments` sub-kind in §2 Vault Topology that does not exist on disk — §2 v7.2 amendment (WS-H) is unfiled. Per L-006 (verify on-disk before locking around it), §12 v1 cannot LOCK around a §2 sub-kind that has no committed schema, Cedar policy, or intent rows. Two paths were considered:

- **(a) Compound-LOCK §12 v1 with §2 v7.2 amendment.** Requires §2 v7.2 to enter the v0.2 critical path before §12 LOCK. Adds a new prerequisite-interlock + a paired Thesis round to the WS-F dispatch.
- **(b) Scope §12 v1 to "narrative + portal_fields only — operator manually attaches."** §12 v1 LOCKs narrowly; §12 v1.1 adds attachment staging once §2 v7.2 LOCKs.

**Path (b) chosen** for §12 v1 LOCK. Path (a) is preserved as an alternative in §OQ-12.4 for operator decision; if operator overrides at LOCK ceremony, §12 v1 reverts to (a) and adds §2 v7.2 to the prerequisite-interlock chain.

**v1.1 horizon.** When §2 v7.2 LOCKs with the `attachments` sub-kind row, §12 v1.1 amendment reintroduces:
- `AttachmentRef` schema: file_path under `orgs/<slug>/vault/grants/<grant_id>/attachments/`, original_file_name, content_sha3_512, uploaded_at_utc, uploaded_by, optional rfa_attachment_match.
- `AttachmentProvenance` companion: hash_verified_at_assembly, format_at_assembly.
- New gates: `F-UPLOADER-ATTACHMENT-MISSING` (PRE), `F-UPLOADER-ATTACHMENT-TAMPERED` (PRE), `F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED` (POST-attachment-stage; §7.11 scanner; closes the Law 4 surface — see §12.2 Law 4 v1.1 horizon note).
- `attachment_manifest.yaml` output artifact and the `"attachment"` value on `submission_manifest.source` Literal.

# §12.7 Readiness checklist

The readiness checklist is Uploader's self-validation (Rule 2). It runs deterministically after package assembly and before surfacing the package to the operator. The checklist result is persisted as `readiness_checklist.yaml`.

**Checklist items at v1:**

1. **Section completeness.** Every entry in `RfaExtractedRecord.section_structure` has a corresponding document in the submission package. Missing section → FAIL with section name.

2. **Manual-attach checklist.** Every entry in `RfaExtractedRecord.required_attachments` is surfaced as a WARN-level operator to-do (not FAIL — at v1 the operator manually attaches at portal upload time per §12.6). Each item includes the RFA-required attachment name and the operator-facing instruction. **Operator-facing only:** the manual-attach list is rendered into the operator-surface `readiness_checklist.yaml` summary; it is NOT persisted to Vault as a separate artifact, NOT included in the staged `submission_package/` directory exported to the operator's portal upload, and NOT logged into any audit trail that exits the org's Vault subtree. The list exists solely to give the operator a visible to-do at portal upload time and is discarded after the run.

3. **Format compliance.** Every document matches the portal's required format (PDF where PDF is required, DOCX where DOCX is required). Mismatch → FAIL with expected vs. actual format.

4. **Page-count compliance.** If `RfaExtractedRecord.section_structure[i].page_limit` is set, the corresponding document's page count MUST be ≤ that limit. Exceeded → FAIL with section name, limit, actual count.

5. **File-size compliance.** Portal-specific file-size limits (e.g., Grants.gov per-attachment limit of variable MB; foundation portals vary). Exceeded → FAIL with filename, limit, actual size.

6. **Filename convention compliance.** Portal-specific filename rules (e.g., Grants.gov requires no spaces, specific prefixes). Non-compliant → FAIL with filename, rule violated, suggested rename.

7. **Manifest integrity.** Every file listed in `submission_manifest.yaml` exists on disk. Every file on disk in the submission_package directory is listed in the manifest. Hash of each file matches the manifest entry. Discrepancy → FAIL.

8. **Operator signature present.** `operator_signature` is present in the input bundle and `bundle_content_hash` matches the `SubmissionBundle` on disk. Missing or mismatched → FAIL.

9. **Portal field completeness.** Every required field in `portal_fields.yaml` has a non-empty value. Empty required field → FAIL with field label.

10. **Content integrity.** Deterministic text-extraction diff between input `SectionDraft.body_text` and output document text content under the §12.8 tolerance model. Non-tolerable delta → FAIL (content was mutated during format conversion; indicates a rendering bug, not an Uploader logic error). This is the `F-UPLOADER-CONTENT-MUTATION` check at the checklist level.

(At v1.1, an "attachment completeness" FAIL-level item replaces item 2's WARN-level checklist when attachments land.)

**Checklist result schema (`ReadinessChecklist`, frozen, kw_only):**
- `overall_status: Literal["ready", "not_ready"]` — `"ready"` iff zero FAIL items.
- `items: tuple[ChecklistItem, ...]` — one per check above.
- `fail_count: int` / `warn_count: int` / `pass_count: int`.
- `checked_at_utc: datetime`.

**`ChecklistItem`, frozen, kw_only:**
- `check_id: str` — e.g., `"section_completeness"`, `"page_count_compliance"`.
- `status: Literal["pass", "fail", "warn"]`.
- `detail: str` — human-readable detail (e.g., "Section 'Project Narrative' exceeds 15-page limit: 17 pages").
- `source: str | None` — the specific section/attachment/field that triggered the finding.

# §12.8 Format conversion

Uploader owns the docx-to-pdf conversion pipeline for submission package assembly. This resolves the open question from `pipeline/planning/v0_2_agents_punch_list_2026-05-09.md §5.2 OQ-1`: **Uploader owns format conversion** rather than §6 publishing a shared utility. Rationale: format conversion is submission-specific (page-count validation, portal filename conventions are submission concerns); Report Generator (§14, v0.2) will need its own format conversion with different constraints (funder reporting templates, not submission portal rules). Sharing a utility would create coupling between §12 and §14 that violates their independent lifecycle.

**Conversion substrate.** Per ADR-001 substrate frozen at Golden Image:
- **DOCX-to-PDF:** `python-docx` for reading + `pypdf` for validation + LibreOffice headless mode (`soffice --headless --convert-to pdf`) for rendering. LibreOffice is the only reliable DOCX-to-PDF renderer available at the Golden Image substrate level without marketplace access. The conversion is a `subprocess.run(check=True)` call to `soffice` only — no other subprocess targets are permitted by the R-UPLOADER-NO-SUBMIT AST-lint allow-list (§12.9.3).
- **DOCX pass-through:** no conversion needed; Scribe's native output is DOCX per §7.5.
- **DOCX-to-plain-text:** `python-docx` text extraction with formatting stripped.
- **PDF validation:** `pypdf` for page count, file size, and structural integrity checks.
- **XLSX validation:** `openpyxl` for read-only validation (no v1 generation surface — at v1.1 attachments may include operator-provided budget spreadsheets validated under the same model).

**Content-mutation tolerance model (§12.8.1).** Format conversion is a rendering operation that preserves text content under the following tolerance model:
- **Whitespace normalization.** Any whitespace sequence (space, tab, newline, repeated spaces from paragraph reflow) collapses to a single space for diff purposes.
- **Page-break-introduced reflow.** Compare per-paragraph after un-paginating the rendered PDF (concatenate all paragraphs in document order before whitespace normalization). Page-break artifacts (page-number footers, repeated headers) are identified by position and excluded from the body-text diff.
- **Tables.** Compared via structural hash: cell-count tuple + per-cell content-hash tuple, ordered row-major. Cell text content is whitespace-normalized before hashing. Tables are NOT compared via flat-text diff.
- **Embedded images.** Compared via image-bytes hash; alt-text excluded from body-text diff.
- **Mathematical notation / equations.** Compared via the source-DOCX MathML representation; rendered-PDF math layout artifacts (font substitution, kerning) are tolerated.

The `F-UPLOADER-CONTENT-MUTATION` POST-gate enforces this model — if text extraction from the rendered PDF does not match the input DOCX text under the tolerance rules above, the package is blocked.

**Benchmarked test commitment (v1.1).** A benchmarked content-mutation test on a real VAPG fixture lands under `tests/seats/uploader/fixtures/vapg_fy26_full_proposal.docx` at v1.1 — round-trips the full proposal through the conversion pipeline and asserts the tolerance model holds against a fixture the operator has verified manually. Deferred to v1.1 because the fixture-prep step requires operator-approved sample content not blocked at v1 LOCK.

# §12.9 Logician gate family — F-UPLOADER-*

Uploader introduces ten failure codes at v0.1 first ship, all registered in the §4 Logician v2.7 amendment (WS-L). All gates are deterministic (Python predicates or Cedar policies); zero token cost (apart from the small local-LLM portal-field-disambiguation calls per §12.11 — those are routing-gated by F-UPLOADER-FIELD-MAP-CLOUD-ROUTED and bounded; the gate predicates themselves remain deterministic).

> **"Explode pattern" defined.** When a gate family is documented at the §4 blueprint level, two §0.5 row layouts are possible: (a) a single aggregate row that names the family, or (b) one row per gate code (the "explode pattern" — first established at the §10 Red Team v1.1 amendment 2026-05-02). Explode-pattern rows preserve audit-trail granularity at the cost of more index rows. §12 follows the explode pattern at the failure-code layer (one row per F-UPLOADER-* code) and the §4 v2.2 consolidated-check pattern at the gate-check layer (multiple failure codes can share a single check callable when their predicate logic overlaps — e.g., `uploader.pre_gate.input_invariants.v1` backs five PRE failure codes via one bundle-validation pass). The mix preserves audit-trail clarity per code while consolidating execution-path complexity.

**v1 gate roster (10 codes):**

| # | Code | Position | Notes |
|---|------|----------|-------|
| 1 | F-UPLOADER-PACKAGE-INCOMPLETE | POST | §12.9.1 |
| 2 | F-UPLOADER-FORMAT-MISMATCH | POST | §12.9.2 (sub-tags `.format`, `.page_limit`, `.file_size`) |
| 3 | F-UPLOADER-AUTOSUBMIT-ATTEMPTED | PRE structural | §12.9.3 |
| 4 | F-UPLOADER-SIGNATURE-MISSING | PRE | §12.9.4 (sub-tags `.absent`, `.hash_mismatch`) |
| 5 | F-UPLOADER-CONTENT-MUTATION | POST | §12.9.5 |
| 6 | F-UPLOADER-INPUT-INCONSISTENT | PRE | §12.9.5 |
| 7 | F-UPLOADER-RFA-MISSING | PRE | §12.9.5 |
| 8 | F-UPLOADER-SIGNATURE-MISMATCH | PRE | §12.9.5 (audit-trail-clarity subclass of SIGNATURE-MISSING.hash_mismatch) |
| 9 | F-UPLOADER-ORG-CROSS-REF | PRE | §12.9.5 (sub-tags `.multi_org_path`, `.symlink_escape`) |
| 10 | F-UPLOADER-FIELD-MAP-CLOUD-ROUTED | PRE | §12.9.6 (HIGH-5 fix) |

**v1.1 horizon (3 additional codes):** F-UPLOADER-ATTACHMENT-TAMPERED (PRE), F-UPLOADER-ATTACHMENT-MISSING (PRE), F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED (POST-attachment-stage). Not registered at v1.

## §12.9.1 F-UPLOADER-PACKAGE-INCOMPLETE

**Sequence position:** POST (after assembly, before operator surface).
**Trigger:** Any entry in `RfaExtractedRecord.section_structure` has no corresponding document in `submission_manifest.yaml`. (At v1 the `required_attachments` walk is informational/WARN per §12.7 item 2, not a hard-block; at v1.1 it becomes a hard-block.)
**Enforcement:** Hard-block. Package is NOT surfaced to operator until all RFA narrative sections are present.
**Predicate (Python):**
```python
def f_uploader_package_incomplete(
    rfa: RfaExtractedRecord,
    manifest: SubmissionManifest,
) -> GateResult:
    missing_sections = [
        s.section_name for s in rfa.section_structure
        if not manifest.has_section(s.section_name)
    ]
    if missing_sections:
        return GateResult.FAIL(
            code="F-UPLOADER-PACKAGE-INCOMPLETE",
            detail=f"Missing sections: {missing_sections}",
        )
    return GateResult.PASS()
```

## §12.9.2 F-UPLOADER-FORMAT-MISMATCH

**Sequence position:** POST (after format conversion, before operator surface).
**Trigger sub-tags:** `.format` — portal requires format X, staged document is format Y. `.page_limit` — portal page-limit exceeded. `.file_size` — portal file-size exceeded.
**Enforcement:** Hard-block. Format-mismatched files are not staged.
**Predicate (Python):**
```python
def f_uploader_format_mismatch(
    adapter: PortalAdapter,
    manifest: SubmissionManifest,
) -> GateResult:
    mismatches = []
    for entry in manifest.entries:
        expected = adapter.required_format(entry.portal_section)
        if expected and entry.format != expected:
            mismatches.append(("format", f"{entry.file_name}: expected {expected}, got {entry.format}"))
        if adapter.page_limit(entry.portal_section) and entry.page_count:
            if entry.page_count > adapter.page_limit(entry.portal_section):
                mismatches.append(("page_limit", f"{entry.file_name}: {entry.page_count} pages > limit {adapter.page_limit(entry.portal_section)}"))
        if adapter.file_size_limit(entry.portal_section) and entry.file_size_bytes:
            if entry.file_size_bytes > adapter.file_size_limit(entry.portal_section):
                mismatches.append(("file_size", f"{entry.file_name}: {entry.file_size_bytes} bytes > limit {adapter.file_size_limit(entry.portal_section)}"))
    if mismatches:
        return GateResult.FAIL(
            code="F-UPLOADER-FORMAT-MISMATCH",
            sub_tag=mismatches[0][0],  # multi-mismatch case carries highest-severity sub-tag
            detail="; ".join(m for _, m in mismatches),
        )
    return GateResult.PASS()
```

## §12.9.3 F-UPLOADER-AUTOSUBMIT-ATTEMPTED — three-layer architecturally-prohibited defense

**Sequence position:** PRE (fail-closed on any code path that attempts submission). **Structural gate, not operationally gated.** Auto-submit is architecturally prohibited; the architecture (v7.0.6) defines Uploader as "prepare-and-stage discipline only — operator clicks final submit on funder portal."

**Enforcement:** Hard-block. Fail-closed. **No bypass via python -O, no bypass via dataclasses.replace, no M13 escape valve. F-UPLOADER-AUTOSUBMIT-ATTEMPTED is architecturally prohibited, not operationally gated.**

**Three-layer defense (HIGH-1 rewrite, 2026-05-09; Audit-#1 corrections, 2026-05-10):**

**Layer-existence audit (per L-006):**

| Layer | Tag | Where it exists | What carries the correctness load |
|---|---|---|---|
| Layer 1 — AST-lint allow-list | EXISTS | `pipeline/linting/ast_lint.py` lines 1260+ (R-UPLOADER-NO-SUBMIT registered; `_check_uploader_no_submit` predicate at line 1457; fixtures under `tests/linting/fixtures/uploader_no_submit/`) | Static foreclosure of any non-allow-listed callable in Uploader code paths. **Load-bearing for correctness on all platforms.** |
| Layer 2 — Process namespace isolation | Linux: ASPIRATIONAL at v0.1 / macOS: ASPIRATIONAL | Cedar policy file `uploader_no_network_egress.cedar` is NOT yet on disk; Tilth process supervisor's namespace-launch wiring is v0.2 horizon. Linux `unshare(CLONE_NEWNET)` syscall is feasible but not yet invoked. macOS `sandbox-exec` profile not yet authored. | Defense-in-depth hardening. Layers 1 + 3 carry the correctness load until Layer 2 ships. |
| Layer 3 — Runtime invariant in `__post_init__` | EXISTS | `pipeline/orchestrator/seats/uploader.py` lines 177-184 (`raise RuntimeError`, not `assert`) | Runtime foreclosure of any code path that reaches a `UploaderOutput(submitted=True)` construction. **Load-bearing for correctness on all platforms.** |

**Layer 1 — AST-lint rule (R-UPLOADER-NO-SUBMIT) — ALLOW-LIST, not blocklist.** Static analysis of `pipeline/orchestrator/seats/uploader.py` and all files under `pipeline/orchestrator/seats/uploader_adapters/` enumerates `ast.Call` nodes and rejects any callable not in the closed allow-list. Allow-list (frozen at Golden Image build):
- Standard library: `dataclasses.dataclass`, `dataclasses.field`, `dataclasses.replace`, `dataclasses.asdict`, `hashlib.sha3_512` (and other hashlib hashers), `datetime.datetime` (constructors + UTC arithmetic), `pathlib.Path` (constructor + resolve + read_bytes + write_bytes + exists + is_file + iterdir + parent + name + suffix), `subprocess.run` ONLY when called with `check=True` AND first arg is a list whose first element is `"soffice"` (LibreOffice convert is the sole permitted subprocess target — enforced at the AST level via positional-arg shape check, not a string-name match), `re.compile` / `re.match` / `re.search` / `re.sub` (Python regex utility), `json.dumps` / `json.loads`, `yaml.safe_load` / `yaml.safe_dump`, `typing.*`, `collections.abc.*`.
- Third-party document parsing (frozen at Golden Image): `docx.Document` (python-docx), `openpyxl.load_workbook` / `openpyxl.Workbook` (openpyxl), `pypdf.PdfReader` (pypdf), `pydantic.BaseModel` and Pydantic field constructors.
- Tilth-internal modules: anything imported from `pipeline.orchestrator.*`, `pipeline.vault.*`, `pipeline.logician.*`, `pipeline.types.*`, `pipeline.shared.*` (resolved at AST-lint via the import graph snapshot taken at Golden Image build).
- Pydantic AI tool-decorator surface: `@tool` decorator from the pinned Pydantic AI version.

**Explicitly NOT in the allow-list (reject by default; named here for foreclosure clarity):** `eval`, `exec`, `compile`, `__import__`, `importlib.import_module`, `ast.literal_eval`, `pickle.loads` / `pickle.load` / `pickle.Unpickler`, `marshal.loads`, `object.__setattr__`, `object.__new__` on UploaderOutput, `ctypes.*`, `cffi.*`, `socket.socket`, `socket.create_connection`, `multiprocessing.Process`, `os.system`, `os.popen`, `subprocess.Popen` to non-`soffice` targets, `subprocess.call` / `subprocess.check_call` / `subprocess.check_output` (only `subprocess.run` with the soffice positional-shape is admitted), `urllib.request.urlopen` / `urllib.request.Request`, any `requests.*` / `httpx.*` / `aiohttp.*` / `http.client.*`. The AST walker resolves attribute chains — aliased imports (`import subprocess as sp; sp.run([...])` or `from httpx import post as send`) are normalized to their canonical form before allow-list lookup, so they cannot bypass via renaming. Implementation: `_collect_imported_names(tree)` separates import-bound names from locally-assigned names; locality fallback admits only the latter. Per `pipeline/linting/ast_lint.py` lines 1502+ + the daily_log 2026-05-09 fixture inventory (httpx.post, requests.request, aiohttp, urllib3, raw socket, subprocess curl, aliased post all flagged on dirty fixtures).

Anything else → R-UPLOADER-NO-SUBMIT violation → static analysis returns non-zero exit → CI / LOCK ceremony hard-fails.

The allow-list approach is strictly stronger than the prior blocklist (regex on `requests.post`, `httpx.post`, `urllib.request.urlopen`, etc.) because it forecloses arbitrary new HTTP-client packages, arbitrary `socket`-level constructions, `aiohttp.ClientSession`, `http.client.HTTPSConnection`, raw `os.system` / `subprocess.Popen` calls to non-`soffice` targets, `ctypes` access to `libcurl` / `libssl`, `multiprocessing.Process` shells, etc. The blocklist would have missed all of these; the allow-list rejects all of them by default and requires explicit operator amendment to extend.

**Layer 2 — Network-namespace process isolation (Cedar / process-boundary) — defense-in-depth, ASPIRATIONAL at v0.1.** The intent is for Uploader to run in a subprocess launched into a network-namespace-isolated execution context with **no outbound socket capability**: a Linux network namespace (or macOS `sandbox-exec` profile equivalent) created with no veth pair, no loopback bridge to the host's outbound interface, no DNS resolver path; with a Cedar policy `uploader_no_network_egress.cedar` denying network-egress to the Uploader process namespace, consulted at subprocess launch time by the Tilth process supervisor. **The Cedar policy file is not on disk at v0.1; the Tilth process supervisor's namespace-launch wiring is a v0.2 work item.** Layer 2 is therefore tagged ASPIRATIONAL per L-006 — the v1 LOCK does NOT depend on Layer 2 for correctness; Layers 1 + 3 are sufficient. Layer 2 is documented here as the v0.2 horizon hardening so a future contributor knows the design intent. The ASPIRATIONAL tag explicitly acknowledges that on macOS the Linux netns approach does not directly apply (`sandbox-exec` is the closest equivalent and is itself deprecated by Apple); the v0.2 implementation will need a per-platform branch with cross-platform contract verified against the same Cedar policy text.

**Layer 3 — Runtime invariant check.** `UploaderOutput.__post_init__` runs `if self.submitted is True: raise RuntimeError("F-UPLOADER-AUTOSUBMIT-ATTEMPTED: ...")`. **Explicit `raise`, not `assert`** — `python -O` strips assertions silently and the Golden Image launcher could in principle be invoked with `-O`; `raise` always fires. The `submitted` field is always `False` at construction. **`dataclasses.replace` re-fires the invariant.** Per CPython behavior, `dataclasses.replace(output, submitted=True)` calls `__init__` on the new instance, which calls `__post_init__`, which raises — the replace bypass is foreclosed by Layer 3 alone. (The on-disk uploader.py docstring at lines 178-181 already documents this correctly; the prior blueprint claim that "`__post_init__` does not re-fire on `replace`" was a misconception, struck in this Audit-#1 fix.) The companion test `test_dataclasses_replace_with_submitted_true_raises` in `tests/seats/uploader/test_uploader_dataclasses_replace_closure.py` confirms the closure.

**Out-of-Layer-3-scope bypasses (defense via Layer 1, finalization, and architecture).** Three bypass classes do NOT fire the `__post_init__` runtime check:
- `object.__setattr__(instance, "submitted", True)` — circumvents the frozen-dataclass `__setattr__` raise. Defense: `object.__setattr__` is NOT in the Layer 1 allow-list (any uploader-code call to it is rejected at static analysis); attacker code injecting `object.__setattr__` from outside Uploader requires a Layer 1 violation in some other module that imports UploaderOutput, which is itself rejected. `UploaderOutput` is decorated `@typing.final` and overrides `__init_subclass__` to raise, foreclosing the subclass-override bypass (RT-1h closure).
- `pickle.loads` of a hand-crafted UploaderOutput state with `submitted=True` — `pickle.loads` reconstructs without calling `__init__` or `__post_init__`. Defense: pickle is NOT in the Layer 1 allow-list (any uploader-code call to `pickle.loads` is rejected); UploaderOutput is NOT designed to be pickle-persisted in any v1 code path; persistence is exclusively via the `uploader_state.yaml` Vault write through `submission_manifest.yaml` (Pydantic-validated). If an attacker controls a persisted state file, that file ALREADY existed in the operator's Vault, which is itself a Law-3 violation requiring its own attack chain.
- `marshal.loads`, custom subclass with `__post_init__` overridden — Layer 1 rejects both at static analysis; the `@typing.final` + `__init_subclass__` raise on UploaderOutput closes the subclass path even if Layer 1 were bypassed.

**Test surface.** §12.13.1 includes static-AST-lint tests, runtime-RuntimeError tests, dataclasses.replace-bypass test (asserts replace re-fires `__post_init__` and raises), `python -O` test (subprocess invocation with `-O` flag, assert RuntimeError still fires), and the `__init_subclass__`-raises test (asserts subclassing UploaderOutput fails at class-creation time). The network-namespace check is exercised by `test_uploader_zero_network_egress` (§12.13.4) — the v0.1 implementation of that test uses a `socket.socket` monkey-patch to assert zero outbound connections, marked v0.2-upgrade-target for the real namespace check once Layer 2 ships.

**No M13 bypass.** Unlike other Logician gates, `F-UPLOADER-AUTOSUBMIT-ATTEMPTED` has no M13 escape valve. The architecture (v7.0.6) defines Uploader as "prepare-and-stage discipline only — operator clicks final submit on funder portal." Auto-submit is not a degraded mode; it is a prohibited mode. An M13 bypass would contradict the architecture.

## §12.9.4 F-UPLOADER-SIGNATURE-MISSING

**Sequence position:** PRE (before assembly begins).
**Trigger sub-tags:** `.absent` — `UploaderInput.operator_signature` is `None`. `.hash_mismatch` — `operator_signature.bundle_content_hash` does not match the SHA3-512 hash of the `SubmissionBundle` bytes at `submission_bundle_ref` (read via `submission-bundle-read` Vault read intent — see §12.4 MEDIUM-1).
**Enforcement:** Hard-block. Uploader refuses to assemble a package the operator has not signed.
**Predicate (Python):**
```python
def f_uploader_signature_missing(
    uploader_input: UploaderInput,
    submission_bundle_bytes: bytes,  # read via vault intent submission-bundle-read
) -> GateResult:
    if uploader_input.operator_signature is None:
        return GateResult.FAIL(
            code="F-UPLOADER-SIGNATURE-MISSING",
            sub_tag="absent",
            detail="No operator signature on submission bundle.",
        )
    computed_hash = hashlib.sha3_512(submission_bundle_bytes).hexdigest()
    if uploader_input.operator_signature.bundle_content_hash != computed_hash:
        return GateResult.FAIL(
            code="F-UPLOADER-SIGNATURE-MISSING",
            sub_tag="hash_mismatch",
            detail=f"Signature hash mismatch: expected {computed_hash[:32]}..., got {uploader_input.operator_signature.bundle_content_hash[:32]}...",
        )
    return GateResult.PASS()
```

## §12.9.5 Additional v1 codes (PRE-gates + content-mutation POST-gate)

These are Uploader-specific codes registered at v1:

- **`F-UPLOADER-CONTENT-MUTATION`** — POST-gate. Text-layer diff between input `SectionDraft.body_text` and output document extracted text reveals delta exceeding the §12.8 tolerance model. Hard-block. Indicates a format-conversion bug.
- **`F-UPLOADER-INPUT-INCONSISTENT`** — PRE-gate. `claim_evidence_map` is not the union of `section_drafts[*].claim_evidence_map`. Hard-block.
- **`F-UPLOADER-RFA-MISSING`** — PRE-gate. `RfaExtractedRecord` absent or hash mismatch against session manifest pin. Hard-block.
- **`F-UPLOADER-SIGNATURE-MISMATCH`** — PRE-gate. Bundle hash changed after operator signature. Hard-block. (Audit-trail subclass of `F-UPLOADER-SIGNATURE-MISSING.hash_mismatch`; both codes resolve via the same predicate at the check level — `F-UPLOADER-SIGNATURE-MISSING.hash_mismatch` is the single check callable, the `F-UPLOADER-SIGNATURE-MISMATCH` code is preserved as a distinct row in §0.5 + a distinct entry in `pipeline.failures.registry` for audit-trail clarity per the §10 explode pattern.)
- **`F-UPLOADER-ORG-CROSS-REF`** — PRE-gate. Sub-tag `.multi_org_path`: input bundle references paths under more than one `orgs/<slug>/`. Sub-tag `.symlink_escape`: a `submission_bundle_ref` or other input path resolves (via `Path.resolve()`) outside the bundle's declared `org_slug` subtree. Hard-block.

## §12.9.6 F-UPLOADER-FIELD-MAP-CLOUD-ROUTED — HIGH-5 fix

**Sequence position:** PRE (gate fires at every portal-field-disambiguation LLM call site).
**Trigger:** A portal-field disambiguation LLM call routes to a cloud provider rather than the always-local Uploader binding.
**Enforcement:** Hard-block. Fail-closed.
**Rationale:** §12.11 admits that SF-424 family field mapping requires interpretation of RFA prose → portal field labels, and that even the v0.1 4-adapter scope needs disambiguation. The disambiguation is bounded to small local-LLM calls (Mistral 7B class, always-local; ~5–50 calls per submission). Cloud routing is prohibited because Uploader operates on the post-fill draft (Confidential values embedded per v7.0.7 split-context discipline). Without this gate, a future router-template change could silently relax the routing posture.

**`FieldMapCallContext` schema (input shape for the predicate; gate-internal — does NOT carry its own §0.5 row, covered by `uploader.pre_gate.field_map_routing.v1` row 229 per the consolidation pattern):**
```python
@dataclass(frozen=True, kw_only=True)
class FieldMapCallContext:
    """Context object passed to F-UPLOADER-FIELD-MAP-CLOUD-ROUTED at every
    portal-field-disambiguation LLM call site. Every adapter's map_fields()
    implementation that issues an LLM disambiguation call MUST construct
    this context and invoke the gate predicate before issuing the call."""
    portal_field_id: str           # e.g., "sf424.applicant_name"
    portal_field_label: str        # human-readable label being disambiguated
    caller_module: str             # e.g., "pipeline.orchestrator.seats.uploader_adapters.grants_gov"
    routed_to: Literal["local", "cloud"]  # destination of the LLM call
    model_id: str                  # e.g., "ollama/mistral:7b"
    classification_at_call: Literal["public", "shareable", "confidential"]
```

**Wiring discipline.** Every `PortalAdapterProtocol.map_fields()` implementation that issues an LLM disambiguation call MUST construct a `FieldMapCallContext` immediately before the call and invoke `f_uploader_field_map_cloud_routed(ctx)` first; only on PASS does the LLM call proceed. The disambiguation invocation surface is wrapped by a Pydantic AI tool decorator that fires the gate as a `before_model_request` hook so contributors cannot land a new disambiguation call site that bypasses the check. AST-lint Layer 1 (R-UPLOADER-NO-SUBMIT) does not block local LLM calls, but a Cycle 2 hardening item is to extend AST-lint with a sibling rule R-UPLOADER-FIELD-MAP-GATED that flags any `before_model_request`-less disambiguation call site (deferred to v0.1.x; the runtime gate is sufficient for v1).

**Predicate (Python):**
```python
def f_uploader_field_map_cloud_routed(
    field_map_call: FieldMapCallContext,
) -> GateResult:
    if field_map_call.routed_to != "local":
        return GateResult.FAIL(
            code="F-UPLOADER-FIELD-MAP-CLOUD-ROUTED",
            detail=f"Portal-field disambiguation call routed to {field_map_call.routed_to}; uploader requires local routing per §12.11.",
        )
    return GateResult.PASS()
```

# §12.10 Portal adapters

Each portal adapter is a Python module implementing the `PortalAdapterProtocol` (Protocol-DI per existing pipeline pattern). Adapters are frozen at Golden Image build per ADR-001; no marketplace. Adding a new portal adapter is a code change (new module + §12 amendment + §0.5 row), not a runtime configuration.

**v0.1 first ship: four portal adapters** — Grants.gov Workspace, SAM.gov, Common Grant Application, Copy-paste fallback. Foundation-platform adapters (Foundant / Submittable / Fluxx) are deferred per the §12.10 footer below.

**`PortalAdapterProtocol`:**
```python
class PortalAdapterProtocol(Protocol):
    """Contract every portal adapter satisfies."""

    @property
    def portal_id(self) -> str:
        """Unique identifier for this portal (e.g., 'grants_gov')."""
        ...

    def required_format(self, portal_section: str | None) -> str | None:
        """Return the required file format for a given portal section. None = any format accepted."""
        ...

    def page_limit(self, portal_section: str | None) -> int | None:
        """Return the page limit for a given portal section. None = no limit."""
        ...

    def file_size_limit(self, portal_section: str | None) -> int | None:
        """Return the file-size limit in bytes for a given portal section. None = no limit."""
        ...

    def filename_convention(self, portal_section: str | None, original_name: str) -> str:
        """Return the portal-compliant filename for a given section and original name."""
        ...

    def map_fields(
        self,
        rfa: RfaExtractedRecord,
        section_drafts: tuple[SectionDraft, ...],
        project_context: ProjectContext,
    ) -> tuple[PortalField, ...]:
        """Map RFA + draft + PROJECT_CONTEXT fields to portal form fields."""
        ...

    def assemble_package(
        self,
        section_drafts: tuple[SectionDraft, ...],
        rfa: RfaExtractedRecord,
        output_dir: str,
    ) -> SubmissionManifest:
        """Assemble the full submission package into output_dir. Return the manifest."""
        ...
```

## §12.10.1 Grants.gov Workspace adapter

**Portal ID:** `grants_gov`
**Required format:** PDF for all narrative sections.
**Filename conventions:** No spaces (underscores only). Prefix with attachment type code per Grants.gov Workspace naming guide. Max 50 characters.
**Field mapping:** SF-424 family form fields mapped from `RfaExtractedRecord` + `PROJECT_CONTEXT` (organization legal name, EIN, UEI, DUNS, address, authorized representative, project director, budget period, project period, requested amount, match amount). Disambiguation pass per §12.11 invokes a local-LLM call when a portal-field label requires interpretation of RFA prose.
**Page limits:** Per `RfaExtractedRecord.section_structure[i].page_limit` (funder-set, not portal-set; Grants.gov itself does not impose page limits but funders specify them in the RFA).
**File-size limits:** Per-attachment limit per current Grants.gov Workspace guidelines (checked at assembly time; limit value is adapter-configurable for future updates).
**Special handling:** SF-424 form fields are exported as `portal_fields.yaml` with field-by-field instructions for the operator. SF-424A/B/C budget-form generation and any non-narrative attachments are deferred to v1.1 (§12.6) — at v1, operator manually attaches budget forms after reviewing the narrative package.

## §12.10.2 SAM.gov adapter

**Portal ID:** `sam_gov`
**Scope:** Entity registration validation + representations-and-certifications letter staging. SAM.gov is not a grant submission portal — it is a pre-submission requirement. The adapter validates that the organization's SAM.gov registration is current (checks `PROJECT_CONTEXT.sam_registration_status` + `PROJECT_CONTEXT.sam_expiration_date`) and stages any representations-and-certifications documents required by the RFA.
**Output:** Validation report in `portal_fields.yaml` (SAM status, UEI, expiration date, registration gaps if any). No document assembly — SAM.gov documents are uploaded directly on the SAM.gov portal by the operator.

## §12.10.3 Common Grant Application adapter

**Portal ID:** `common_grant_app`
**Required format:** PDF for narrative.
**Field mapping:** Standard CGA fields (organization name, mission statement, project title, request amount, project description, evaluation plan, budget narrative). Mapped from `RfaExtractedRecord` + `PROJECT_CONTEXT` + `SectionDraft` per CGA field definitions; per-field disambiguation per §12.11.
**Filename conventions:** Per CGA guidelines (typically: `OrgName_SectionName.pdf`).

## §12.10.4 Copy-paste fallback adapter

**Portal ID:** `copy_paste`
**Required format:** PDF for all narrative documents (universal portability). DOCX also staged as source.
**Field mapping:** All fields from `RfaExtractedRecord` + `PROJECT_CONTEXT` are exported as `portal_fields.yaml` with generic labels. No portal-specific field IDs — the operator maps fields to the target portal manually.
**Filename conventions:** `<section_order>_<section_name>.pdf` (simple, readable).
**Special handling:** The fallback adapter is the floor — it always works. It produces a clean, organized package that an operator can manually upload to any portal. Every other adapter extends this base package with portal-specific optimizations.

## §12.10.5 Deferred adapters (Foundant / Submittable / Fluxx) — v0.1.x

**Foundant / Submittable / Fluxx require per-funder config curation pipeline (§OQ-12.6 deferred to v0.2 with Archivist curation). Stub adapters without curated per-funder field-mapping tables would mislead the operator.** A bare-stub Foundant adapter that emits "field id unknown — operator paste manually" for every Foundant form field is strictly worse than the copy-paste fallback (it pretends to know the portal but doesn't), and shipping it would create a false impression that Tilth handles Foundant when it actually doesn't. Deferred to v0.1.x pending the curation pipeline.

**v0.1.x plan.** When the per-funder config curation pipeline lands (Archivist-curated, parallel to Funder Intelligence DB curation), Foundant + Submittable + Fluxx adapter sections re-enter §12.10 as full implementations with curated per-portal field-mapping tables stored at `vault_shared/portal_configs/{foundant,submittable,fluxx}/<funder_id>.yaml`. The §0.5 row inventory grows by 3 adapter rows under `uploader.portal_adapter_protocol.v1` aggregation (or per-adapter rows if §0.5 explode-pattern preferred at that round).

# §12.11 Routing posture (per v7.0.7 classification)

**Mostly local; bounded local-LLM calls for portal field disambiguation only; cloud routing prohibited.** Uploader processes post-fill drafts (Confidential values already embedded by the slot-fill agent per §7 v1.1.1 classification-aware-split-context). Per v7.0.7 §1: anything reading a post-fill draft is local-routed structurally. Format conversion, manifest generation, readiness checklist, and gate predicates are deterministic Python (zero LLM calls). Portal-field disambiguation is the sole LLM-touching surface — bounded to one disambiguation pass per portal field needing interpretation, typically 5–50 fields per submission, against a small local model (Mistral 7B class).

**Cloud routing prohibited.** Enforced by `F-UPLOADER-FIELD-MAP-CLOUD-ROUTED` (§12.9.6) at every portal-field-disambiguation call site.

**Classification register entry:** `uploader` → `always_local` (hard-coded, not operator-overridable at Classification Review). Rationale: Uploader sees the complete, final, post-fill proposal with all Confidential values embedded; AND every portal-field disambiguation pass operates on that same post-fill content. No subset of Uploader's input is safely cloud-routable. **Enforcement-binding note:** the no-override constraint relies on architecture v7.0.7 (Beta classification routing, currently SCOPING DRAFT pending WS-B Thesis) supporting an `always_local: hard_coded` flag on per-agent register entries. v7.0.7 §6 reserves this flag; until v7.0.7 LOCKs, the §12 v1 LOCK treats the constraint as a contractual commitment between §12 and the v7.0.7 register schema, and the Uploader wrapper short-circuits any `routed_to != "local"` request locally. F-UPLOADER-FIELD-MAP-CLOUD-ROUTED (§12.9.6) catches any escape from the wrapper.

**Token cost:** Bounded local. ~5–50 small-model calls per submission. Logician gates are deterministic Python predicates; AST-lint is deterministic static analysis. Format conversion is subprocess + library calls.

# §12.12 Pipeline placement

Per v7.0.6 amendment pipeline placement:

```
DRAFTING + REVIEW (council seats under §5 revision-loop control)
  Logician PRE → Scribe → Editor → Scribe revises → Judge → Red Team → Logician POST
  → operator sign-off (Law 5 final gate)

SUBMISSION (§12 Uploader)
  operator_signature on SubmissionBundle
  → Uploader assembles submission package (narrative + portal_fields, v1)
  → Uploader runs readiness checklist (Rule 2)
  → Uploader stages package to vault
  → Uploader surfaces readiness checklist + manual-attach to-do list (v1) to operator
  → operator reviews package, manually attaches non-Tilth files
  → operator clicks final submit on funder portal (OUTSIDE Tilth)
```

Uploader fires ONCE per grant submission cycle. It does not participate in the revision loop. It does not fire on eval_mode runs. It does not fire on report_mode runs (that is Report Generator, §14). Its trigger is: §5 submission_mode terminus reached + operator sign-off signature present.

# §12.13 Test matrix

Tests live at `tests/seats/uploader/`. Each test is a deterministic unit test — no LLM calls (the local-LLM portal-field disambiguation is mocked in unit tests; integration tests stub the local-LLM endpoint), no network calls (enforced by `test_uploader_zero_network_egress`), no portal API calls.

## §12.13.1 Gate tests (v1)

- `test_f_uploader_package_incomplete_missing_section`: construct `RfaExtractedRecord` with 5 sections; manifest with 4 documents; assert `F-UPLOADER-PACKAGE-INCOMPLETE`.
- `test_f_uploader_package_complete`: full manifest matching full RFA; assert PASS.
- `test_f_uploader_format_mismatch_format`: portal requires PDF, staged document is DOCX; assert `F-UPLOADER-FORMAT-MISMATCH` sub-tag `.format`.
- `test_f_uploader_format_mismatch_page_limit`: document has 20 pages, RFA limit is 15; assert `F-UPLOADER-FORMAT-MISMATCH` sub-tag `.page_limit`.
- `test_f_uploader_format_mismatch_file_size`: document is 25 MB, portal limit is 20 MB; assert `F-UPLOADER-FORMAT-MISMATCH` sub-tag `.file_size`.
- `test_f_uploader_autosubmit_attempted_ast_lint_allow_list`: run AST-lint R-UPLOADER-NO-SUBMIT on `uploader.py` + all adapter files; assert no calls outside the allow-list. Includes negative-control fixture file with prohibited `requests.post`, `httpx.post`, `socket.socket`, raw `subprocess.Popen` to non-soffice target — assert all flagged.
- `test_f_uploader_autosubmit_attempted_runtime_raise`: attempt to set `UploaderOutput.submitted = True` via constructor; assert `RuntimeError` (NOT `AssertionError`) in `__post_init__`.
- `test_f_uploader_autosubmit_attempted_python_minus_O`: subprocess invocation of a child Python with `-O` flag attempting `UploaderOutput(submitted=True)`; assert child process exits non-zero with RuntimeError still firing.
- `test_f_uploader_autosubmit_attempted_replace_bypass`: construct `UploaderOutput(submitted=False)`, then `dataclasses.replace(output, submitted=True)`; assert `RuntimeError` raised inside `__post_init__` of the new instance (CPython behavior: `dataclasses.replace` re-fires `__post_init__`). Companion test file `test_uploader_dataclasses_replace_closure.py` confirms.
- `test_f_uploader_autosubmit_attempted_subclass_blocked`: attempt `class Evil(UploaderOutput): ...`; assert `__init_subclass__` raises a `TypeError` at class-definition time (RT-1f / RT-1h closure: subclass override is foreclosed).
- `test_f_uploader_autosubmit_attempted_setattr_blocked`: attempt `object.__setattr__(out, "submitted", True)`; this is NOT blocked by Layer 3 alone but IS rejected by AST-lint R-UPLOADER-NO-SUBMIT inside any uploader-code call site (Layer 1 forecloses); the test asserts that the AST-lint flags `object.__setattr__` as a non-allow-listed callable when invoked from any file under `pipeline/orchestrator/seats/uploader*`.
- `test_f_uploader_signature_missing_absent`: `operator_signature = None`; assert `F-UPLOADER-SIGNATURE-MISSING` sub-tag `.absent`.
- `test_f_uploader_signature_missing_hash_mismatch`: `bundle_content_hash` differs from computed hash; assert `F-UPLOADER-SIGNATURE-MISSING` sub-tag `.hash_mismatch`.
- `test_f_uploader_signature_mismatch_audit_subclass`: same hash-mismatch fixture; assert `F-UPLOADER-SIGNATURE-MISMATCH` audit-trail subclass row appears in failure registry alongside the SIGNATURE-MISSING fail.
- `test_f_uploader_content_mutation_detected`: modify one word in rendered PDF text extraction beyond §12.8 tolerance; assert `F-UPLOADER-CONTENT-MUTATION`.
- `test_f_uploader_content_mutation_whitespace_tolerated`: paragraph-reflow whitespace difference only; assert PASS (tolerance model holds).
- `test_f_uploader_input_inconsistent`: `claim_evidence_map` missing entries from one `SectionDraft`; assert `F-UPLOADER-INPUT-INCONSISTENT`.
- `test_f_uploader_rfa_missing_absent`: `RfaExtractedRecord = None`; assert `F-UPLOADER-RFA-MISSING`.
- `test_f_uploader_rfa_missing_hash_drift`: `rfa_content_sha3_512` does not match session manifest pin; assert `F-UPLOADER-RFA-MISSING`.
- `test_f_uploader_org_cross_ref_multi_org_path`: input bundle references two different `orgs/<slug>/` paths; assert `F-UPLOADER-ORG-CROSS-REF` sub-tag `.multi_org_path`.
- `test_f_uploader_org_cross_ref_symlink_escape`: `submission_bundle_ref` is a symlink to a path outside the declared `org_slug` subtree; assert `F-UPLOADER-ORG-CROSS-REF` sub-tag `.symlink_escape`.
- `test_f_uploader_field_map_cloud_routed`: stub field-map call context with `routed_to="cloud"`; assert `F-UPLOADER-FIELD-MAP-CLOUD-ROUTED`.

## §12.13.2 Adapter tests (v1 — four adapters)

- `test_grants_gov_filename_convention`: assert no spaces, correct prefix, max 50 chars.
- `test_grants_gov_required_format_pdf`: assert all narrative sections rendered as PDF.
- `test_grants_gov_sf424_field_export`: assert SF-424 fields populated from `RfaExtractedRecord` + `PROJECT_CONTEXT`.
- `test_sam_gov_validation_current`: SAM registration current; assert validation PASS.
- `test_sam_gov_validation_expired`: SAM registration expired; assert validation WARN with expiration date.
- `test_common_grant_app_field_mapping`: assert CGA fields populated correctly.
- `test_copy_paste_fallback_always_works`: minimal `UploaderInput`; assert copy-paste adapter produces a valid package with manifest.

## §12.13.3 Readiness checklist tests (v1)

- `test_readiness_all_pass`: complete package with all sections, correct formats, under page/size limits; assert `overall_status == "ready"`.
- `test_readiness_missing_section`: one section missing; assert `overall_status == "not_ready"`, FAIL item with section name.
- `test_readiness_page_limit_exceeded`: one document over page limit; assert FAIL item.
- `test_readiness_manual_attach_warn_surfaced`: `RfaExtractedRecord.required_attachments` non-empty; assert WARN-level checklist items surfaced for each (v1 manual-attach to-do list per §12.6).
- `test_readiness_manifest_integrity_extra_file`: file on disk not in manifest; assert FAIL.
- `test_readiness_manifest_integrity_missing_file`: manifest entry with no corresponding file; assert FAIL.

## §12.13.4 Integration tests (v1)

- `test_end_to_end_grants_gov`: full `UploaderInput` with 5 sections + SF-424 fields; invoke Grants.gov adapter; assert manifest complete, readiness PASS (with manual-attach WARN list surfaced), no content mutation, zero auto-submit code paths exercised, all field-map LLM calls routed local.
- `test_end_to_end_copy_paste_fallback`: same input; invoke copy-paste adapter; assert manifest complete, readiness PASS.
- `test_uploader_zero_network_egress` (MEDIUM-6): v0.1 implementation uses an in-process `socket.socket` monkey-patch raising `OSError` on any non-loopback `connect()`; full Uploader run completes successfully with all field-map calls hitting the localhost-bound local-LLM endpoint and zero non-loopback connections. **v0.2 upgrade target:** when Layer 2 process-namespace isolation ships, this test gets a sibling `test_uploader_zero_network_egress_namespace` that runs Uploader inside a real Linux network namespace (or macOS `sandbox-exec` profile) and asserts via packet-capture that no outbound packets are emitted. The monkey-patch variant remains as cross-platform CI coverage; the namespace variant runs only on platforms where Layer 2 is EXISTS.

## §12.13.5 v1.1 horizon tests (NOT registered at v1)

The following tests land at §12 v1.1 alongside attachments + the v1.1 gate triplet:
- `test_f_uploader_attachment_tampered`: modify attachment file after upload; hash mismatch at assembly; assert `F-UPLOADER-ATTACHMENT-TAMPERED`.
- `test_f_uploader_attachment_missing`: `AttachmentRef.file_path` points to nonexistent file; assert `F-UPLOADER-ATTACHMENT-MISSING`.
- `test_f_uploader_attachment_admin_risk_unflagged`: attachment text contains a Severity ≥ Medium admin-risk-register term without a `[ADMIN-RISK:flag]` in attachment metadata; assert `F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED`.
- `test_uploader_content_mutation_vapg_fixture` (MEDIUM-5 commitment): real VAPG fixture under `tests/seats/uploader/fixtures/vapg_fy26_full_proposal.docx`; full DOCX→PDF round-trip; assert §12.8 tolerance model holds.

# §12.14 Open questions resolved and deferred

## §12.14.1 Resolved

- **Format-conversion responsibility (`pipeline/planning/v0_2_agents_punch_list_2026-05-09.md §5.2 OQ-1`).** RESOLVED: Uploader owns docx-to-pdf conversion. Rationale in §12.8. Report Generator (§14) will own its own conversion at v0.2.
- **Attachment provenance (`pipeline/planning/v0_2_agents_punch_list_2026-05-09.md §5.2 OQ-2`).** PARTIALLY RESOLVED at v1: attachments deferred to v1.1 (§12.6). Schema reintroduced at v1.1 alongside §2 v7.2 `attachments` sub-kind LOCK.
- **Portal adapter scope (decision 8c default — operator confirmation pending).** RESOLVED at v1: four adapters (Grants.gov + SAM.gov + Common Grant App + copy-paste fallback) per §12.10. Foundation-platform adapters (Foundant / Submittable / Fluxx) deferred to v0.1.x per §OQ-12.6.

## §12.14.2 Open questions for next-round attention

- **OQ-12.1: Live portal API integration.** v0.1 is offline assembly only. v0.2+ may add live API adapters for portals that offer submission APIs (Grants.gov Workspace API, Submittable API). Gated on per-portal ToS review and operator-accountability analysis. Auto-submit remains architecturally prohibited regardless of API availability.
- **OQ-12.2: Multi-submission versioning.** v0.1 Uploader assembles one package per `run_id`. If the operator submits, receives feedback, and wants to resubmit, a new council run produces a new `run_id` and Uploader assembles a new package. v0.2+ may add diff-aware resubmission packaging (delta between v1 and v2 submission, tracked in vault).
- **OQ-12.3: Symlink path-resolve invariant — extension to `attachments` directory.** At v1 the path-resolve invariant covers `submission_bundle_ref` only (no attachments at v1). At v1.1, every `AttachmentRef.file_path` is also `Path.resolve()`-normalized and the resolved path is required to sit under `orgs/<org_slug>/vault/grants/<grant_id>/attachments/`. Track at v1.1 amendment.
- **OQ-12.4: Compound-LOCK alternative for §12 v1 + §2 v7.2.** Path (a) per §12.6 — operator may override at LOCK ceremony. If chosen, §12 v1 reverts to including `attachments` field, §2 v7.2 amendment enters the prerequisite-interlock chain, and a paired Thesis round dispatches.
- **OQ-12.5: Cross-org content-surface scanning at vault write time.** Currently `F-UPLOADER-ORG-CROSS-REF` is a path-level check (multi-org-path + symlink-escape). It does NOT scan in-file content for substantive material from another org's PROJECT_CONTEXT or another org's draft having leaked through an upstream bug. Semantic content-surface scanning is out of scope for v0.1 (semantic comparison is expensive; the upstream bug class is rare; the path-level check covers the common drift modes). Track at v0.2.
- **OQ-12.6: Per-funder portal config curation pipeline.** Foundant / Submittable / Fluxx adapters need curated per-funder field-mapping tables (`vault_shared/portal_configs/{foundant,submittable,fluxx}/<funder_id>.yaml`). Curation pipeline lives at v0.2 with Archivist (parallel to Funder Intelligence DB curation). Until curated, these adapters do not ship — copy-paste fallback covers the gap.

# §12.15 Companion edits at LOCK

The following edits land in the same commit as §12 v1 LOCK (compound paired-commit per §6.17 Option-B):

1. **§0.5 §12 amendment** — `pipeline/blueprint/v0.1/section_00_5_section_12_uploader_amendment.md` — final inventory **21 rows at v1** (per the explode-pattern §10 precedent applied to F-UPLOADER-* failure-codes):
   - 1 marker row (kind=`marker`): `blueprint.section_anchor.s12_uploader.v1`
   - 4 schema/contract rows: `uploader.input.v1`, `uploader.output.v1`, `uploader.portal_adapter_protocol.v1`, `uploader.readiness_checklist.v1`
   - 10 failure-code rows (kind=`failure-code`): one per v1 gate code
   - 6 pre-gate-check / post-gate-check rows: consolidated per check-callable per §4 v2.2 pattern
   See the companion amendment file for the full row table with primitive_ids.

2. **§4 Logician v2.7 amendment** — registers F-UPLOADER-* family + R-UPLOADER-NO-SUBMIT AST-lint rule at the Logician (Code session is authoring this in parallel; this blueprint is the authority on the gate codes + sub-tags + allow-list contents).

3. **`orgs/_TEMPLATE/uploader/` scaffold** — template directory for new client orgs:
   - `orgs/_TEMPLATE/vault/grants/_TEMPLATE_GRANT/submission_package/` (empty directory)
   - `orgs/_TEMPLATE/vault/grants/_TEMPLATE_GRANT/uploader_state/` (empty directory; per MEDIUM-4 path move)
   - (`attachments/` template directory deferred to v1.1 per §12.6.)

4. **Module scaffold** — `pipeline/orchestrator/seats/uploader.py` + per-portal adapter modules under `pipeline/orchestrator/seats/uploader_adapters/`:
   - `uploader_adapters/__init__.py`
   - `uploader_adapters/grants_gov.py`
   - `uploader_adapters/sam_gov.py`
   - `uploader_adapters/common_grant_app.py`
   - `uploader_adapters/copy_paste.py`
   - (`foundant.py`, `submittable.py`, `fluxx.py` deferred to v0.1.x per §12.10.5.)

5. **Test suite** — `tests/seats/uploader/` per §12.13.

---

End of §12 Uploader blueprint. Thesis round pending per L-005 two-audit cycle.
