---
title: §4 v2.7 Targeted Amendment — Uploader gate family (F-UPLOADER-*)
parent: pipeline/blueprint/v0.1/section_04_logician.md (v2.1 LOCKED 2026-04-19)
companion_blueprint: pipeline/blueprint/v0.1/section_12_uploader.md (§12 v1 SCOPING DRAFT 2026-05-09)
amendment_version: v2.7
status: LOCKED 2026-05-10 — L-005 strict two-cycle PASS per `pipeline/validation/v12_v1_thesis_2026-05-09/audit_v2_synthesis.md` with FULL live cross-family rigor. Path C reconciliation 2026-05-09 narrowed to v1-scope; attachment family deferred to companion §4 v2.7.1 LOCKing with §12 v1.1. Compound-LOCKed with §12 v1 + §0.5 §12 amendment per §6.17 Option-B paired-commit pattern.
ws_slice: WS-L (Uploader-paired slice only). Other WS-L gate families (KFR, Funder Intel, Data Collector, Report Generator, Archivist) stay for the full WS-L cycle.
draft_date: 2026-05-09
operator: Josh
discipline: L-005 two-audit + cross-family rigor; F-INDEX-STALE PRE-gate; Five Laws (Laws 1, 2, 3, 5 primary)
paired_commit_sec00_5: §0.5 v9 — 21 amendment rows (1 marker + 4 schema/contract + 10 failure-code + 3 pre-gate-check + 3 post-gate-check). §4 v2.7 cites 16 of these via the row-citation block in §4.18 below — 10 failure-code rows 1:1 + 1 consolidated `uploader.pre_gate.input_invariants.v1` PRE-check covering 5 failure codes per the §4 v2.2 consolidated-check pattern + 2 distinct PRE-checks (autosubmit_structural, field_map_routing) + 3 POST-checks (package_completeness, format_compliance, content_mutation). Path C reconciliation 2026-05-09 narrows §4 v2.7 to v1-scope (matches §12 v1 path-b decision deferring attachments to v1.1); the attachment family (3 failure codes + 2 PRE-checks + 1 POST-check) is registered separately in §4 v2.7.1 amendment which companion-LOCKs with §12 v1.1.
architecture_ref: v7 A1-A12 LOCKED 2026-04-19; v7.0.6 amendment (Uploader as v0.1 support agent; prepare-and-stage discipline)
predecessor_amendment: section_04_v2_6_deferred_scope_amendment.md (v2.6 SCOPING DRAFT 2026-05-09)
companion_code:
  - pipeline/orchestrator/seats/uploader.py                                       (existing — predicates f_uploader_signature_missing + f_uploader_org_cross_ref already implemented)
  - pipeline/logician/gates/f_uploader_package_incomplete.py                      (NEW — POST)
  - pipeline/logician/gates/f_uploader_format_mismatch.py                         (NEW — POST)
  - pipeline/logician/gates/f_uploader_autosubmit_attempted.py                    (NEW — PRE, no M13 bypass)
  - pipeline/logician/gates/f_uploader_signature_missing.py                       (NEW — PRE; thin wrapper over uploader.py predicate)
  - pipeline/logician/gates/f_uploader_content_mutation.py                        (NEW — POST)
  - pipeline/logician/gates/f_uploader_input_inconsistent.py                      (NEW — PRE)
  - pipeline/logician/gates/f_uploader_rfa_missing.py                             (NEW — PRE)
  - pipeline/logician/gates/f_uploader_signature_mismatch.py                      (NEW — PRE; thin wrapper over uploader.py signature predicate)
  - pipeline/logician/gates/f_uploader_org_cross_ref.py                           (NEW — PRE; thin wrapper over uploader.py predicate)
companion_tests:
  - tests/logician/gates/test_f_uploader_package_incomplete.py
  - tests/logician/gates/test_f_uploader_format_mismatch.py
  - tests/logician/gates/test_f_uploader_autosubmit_attempted.py
  - tests/logician/gates/test_f_uploader_signature_missing.py
  - tests/logician/gates/test_f_uploader_content_mutation.py
  - tests/logician/gates/test_f_uploader_input_inconsistent.py
  - tests/logician/gates/test_f_uploader_rfa_missing.py
  - tests/logician/gates/test_f_uploader_signature_mismatch.py
  - tests/logician/gates/test_f_uploader_org_cross_ref.py
---

# §4 v2.7 Targeted Amendment — Uploader gate family (F-UPLOADER-*)

## Scope

This amendment registers ten Uploader gates: nine specified in §12.9
of the Uploader blueprint v1 (after the path-b deferral of attachments
to §12 v1.1) plus one Cowork-slice addition (F-UPLOADER-FIELD-MAP-
CLOUD-ROUTED) landing in parallel via Cowork's §12 pre-fix slice. The
attachment family (3 failure codes + 2 PRE-checks + 1 POST-check) is
deferred to companion §4 v2.7.1 amendment which LOCKs with §12 v1.1.
Scope:

- New §4.18 — Uploader gate family overview, M13 bypass policy, §12 cross-reference.
- Ten new failure codes added to §6 (4 primary + 6 secondary — 5 per §12.9.5 + 1 Cowork-slice).
- §4.5 PRE-gate row table additions (PRE-29 … PRE-35 — seven PRE-gate rows).
- §4.6 POST-gate row table additions (POST-17 … POST-19 — three POST-gate rows).
- §11 Law-map additions (Laws 1, 2, 3, 5 + architectural-invariant classification-discipline for the FIELD-MAP-CLOUD-ROUTED Cowork-slice gate).
- §0.5 paired-commit row citations (16 §0.5 v9 rows — 10 failure-code 1:1 + 1 consolidated `uploader.pre_gate.input_invariants.v1` PRE-check covering 5 failure codes per §4 v2.2 pattern + 2 distinct PRE-checks (autosubmit_structural, field_map_routing) + 3 POST-checks (package_completeness, format_compliance, content_mutation)).
- v2.7.1 horizon stub — 6 deferred attachment-family primitives surfaced for companion-LOCK at §12 v1.1.

No existing §4.1–§4.17, §5–§10, §12, §13 content modified. Surgical addition.

This amendment is the **§12-paired slice of WS-L only**. Other WS-L gate
families (KFR, Funder Intel, Data Collector, Report Generator, Archivist)
are NOT in scope here. Those remain for the full WS-L cycle.

---

## §4.18 (NEW v2.7) — Uploader gate family overview

The Uploader support agent (Blueprint §12) introduces ten Logician
gates that mechanically enforce the prepare-and-stage discipline of v0.1
submission package assembly: nine base gates per §12.9 plus one
Cowork-slice addition landing in parallel (F-UPLOADER-FIELD-MAP-
CLOUD-ROUTED PRE-gate). All ten gates are deterministic Python
predicates; zero LLM tokens; fail-closed; Protocol-DI per existing §4
pattern (E-017 injected-callable). No gate touches the filesystem
directly — bytes / manifest / hash readers are injected.

**Path-C narrowing (2026-05-09):** Three attachment-related failure codes
(F-UPLOADER-ATTACHMENT-TAMPERED, F-UPLOADER-ATTACHMENT-MISSING,
F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED) and their associated PRE/POST
checks are deferred to companion §4 v2.7.1 amendment which LOCKs with
§12 v1.1, matching the §12 v1 path-b decision to defer attachments per
§OQ-12.6. See `section_04_v2_7_1_attachment_family_amendment.md`.

**Primary family (4 gates per §12.9.1–§12.9.4):**

| Code | Tier | Trigger surface |
|---|---|---|
| `F-UPLOADER-PACKAGE-INCOMPLETE` | POST | RFA-required section absent from staged manifest (mandatory-attachment walk informational/WARN at v1; hard-block at v1.1 per §12.7) |
| `F-UPLOADER-FORMAT-MISMATCH` | POST | Wrong file format / page-limit exceeded / file-size limit exceeded |
| `F-UPLOADER-AUTOSUBMIT-ATTEMPTED` | PRE | Any code path that attempts portal submission. **No M13 bypass.** |
| `F-UPLOADER-SIGNATURE-MISSING` | PRE | Operator signature absent on input bundle |

**Secondary family (6 gates — 5 per §12.9.5 + 1 added by Cowork §12 pre-fix slice):**

| Code | Tier | Trigger surface |
|---|---|---|
| `F-UPLOADER-CONTENT-MUTATION` | POST | Text-layer diff between input `SectionDraft.body_text` and rendered output |
| `F-UPLOADER-INPUT-INCONSISTENT` | PRE | `claim_evidence_map` is not the union of `section_drafts[*].claim_evidence_map` |
| `F-UPLOADER-RFA-MISSING` | PRE | `RfaExtractedRecord` absent OR `rfa_content_sha3_512` does not match session manifest pin |
| `F-UPLOADER-SIGNATURE-MISMATCH` | PRE | `bundle_content_hash` differs from on-disk `SubmissionBundle` SHA3-512 (subclass of SIGNATURE-MISSING; distinct code for audit-trail clarity per §12.9.5) |
| `F-UPLOADER-ORG-CROSS-REF` | PRE | Input bundle references paths under more than one `orgs/<slug>/` (sweep covers `org_slug` + every attachment-resolvable path + `submission_bundle_ref` per HIGH-1e) |
| `F-UPLOADER-FIELD-MAP-CLOUD-ROUTED` *(Cowork-slice)* | PRE | Field-map slot-fill stage receives Confidential-classified input while cloud-routed (architecture v7.0.7 classification-discipline) |

### M13 bypass policy

- **All Uploader gates support M13 operator-bypass EXCEPT
  `F-UPLOADER-AUTOSUBMIT-ATTEMPTED`.** Auto-submit is an *architecturally*
  prohibited mode per architecture v7.0.6 (Uploader = "prepare-and-stage
  discipline only — operator clicks final submit on funder portal").
  An M13 bypass would contradict the architecture; the gate is fail-closed
  with no escape valve.
- For all nine other v2.7 Uploader gates, the standard M13 audited-bypass
  workflow applies (per §4 v2.1 §4.7) — operator-signed bypass with rationale,
  appended to the admin-risk ledger at HIGH severity.

### Cross-reference

Detailed semantics, predicate reference implementations, attachment provenance
schema, and readiness-checklist mapping are specified in Blueprint §12.9.
This amendment registers the gates with §4 Logician; it does not duplicate
§12 specification.

---

## §4.5 PRE-gate row additions (v2.7)

Seven new rows (PRE-29 … PRE-35 — six base + one Cowork-slice).
Existing PRE-gate rows retain their ordering relative to each other.

| Order | Check ID | Fires at | Failure code | Bypass |
|---|---|---|---|---|
| PRE-29 | F-UPLOADER-AUTOSUBMIT-ATTEMPTED | Uploader module load + every Uploader output `__post_init__` + AST-lint at CI/LOCK | `F-UPLOADER-AUTOSUBMIT-ATTEMPTED` | **NONE — architecturally prohibited** |
| PRE-30 | F-UPLOADER-RFA-MISSING | Uploader pre-assembly | `F-UPLOADER-RFA-MISSING` | M13 |
| PRE-31 | F-UPLOADER-SIGNATURE-MISSING | Uploader pre-assembly | `F-UPLOADER-SIGNATURE-MISSING` | M13 |
| PRE-32 | F-UPLOADER-SIGNATURE-MISMATCH | Uploader pre-assembly (paired with PRE-31) | `F-UPLOADER-SIGNATURE-MISMATCH` | M13 |
| PRE-33 | F-UPLOADER-INPUT-INCONSISTENT | Uploader pre-assembly | `F-UPLOADER-INPUT-INCONSISTENT` | M13 |
| PRE-34 | F-UPLOADER-ORG-CROSS-REF | Uploader pre-assembly | `F-UPLOADER-ORG-CROSS-REF` | M13 |
| PRE-35 | F-UPLOADER-FIELD-MAP-CLOUD-ROUTED | Uploader pre-assembly (field-map slot-fill stage) | `F-UPLOADER-FIELD-MAP-CLOUD-ROUTED` | M13 |

**Ordering rationale.** PRE-29 (autosubmit) runs first as a structural
invariant (module-load-time AST + runtime `__post_init__`; never reaches
Uploader logic). PRE-30 (RFA) before all other inputs because RFA pin
mismatch invalidates everything downstream. PRE-31 / PRE-32 paired
(signature presence then content hash). PRE-33 (input shape) sits before
per-path validation. PRE-34 (org cross-ref) sits among the final PREs as
a Law-3 sweep across all paths, after per-path validation. PRE-35 (field-
map cloud-routed) is the classification-discipline gate added in Cowork's
§12 fix slice — it ensures any cloud-routable field-map slot-fill stage
receives only Public + Shareable input, per the §0.5 classification
register and the architecture v7.0.7 amendment.

**Path-C deferred.** PRE-checks for `F-UPLOADER-ATTACHMENT-MISSING` (file
existence) and `F-UPLOADER-ATTACHMENT-TAMPERED` (hash continuity) are
registered separately in §4 v2.7.1 amendment which LOCKs with §12 v1.1
when the attachment family lands. Their downstream ordering (file
existence → integrity → org-cross-ref attachment-path sweep) is
preserved in v2.7.1.

## §4.6 POST-gate row additions (v2.7)

Three new rows (POST-17 … POST-19 — three base).

| Order | Check ID | Fires at | Failure code | Bypass |
|---|---|---|---|---|
| POST-17 | F-UPLOADER-PACKAGE-INCOMPLETE | Uploader post-assembly, before operator surface | `F-UPLOADER-PACKAGE-INCOMPLETE` | M13 |
| POST-18 | F-UPLOADER-FORMAT-MISMATCH | Uploader post-assembly, after format conversion | `F-UPLOADER-FORMAT-MISMATCH` | M13 |
| POST-19 | F-UPLOADER-CONTENT-MUTATION | Uploader post-assembly, after format conversion (text-layer diff) | `F-UPLOADER-CONTENT-MUTATION` | M13 |

**Ordering rationale.** POST-17 (completeness) before POST-18 (format) —
no point validating format on a missing file. POST-18 before POST-19 —
content-diff validation requires a successfully rendered file to extract
text from.

**Path-C deferred.** POST-check for `F-UPLOADER-ATTACHMENT-ADMIN-RISK-
UNFLAGGED` (attachment admin-risk register sweep, v1.1 engagement) is
registered separately in §4 v2.7.1 amendment which LOCKs with §12 v1.1.

---

## §6 Failure code additions (v2.7)

Ten new codes added to §6 — nine base per §12.9 (after path-b attachment
deferral) + one Cowork-slice addition (F-UPLOADER-FIELD-MAP-CLOUD-ROUTED).
No existing codes modified. The three attachment-related failure codes
(F-UPLOADER-ATTACHMENT-TAMPERED, F-UPLOADER-ATTACHMENT-MISSING,
F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED) are registered separately in
§4 v2.7.1 amendment which LOCKs with §12 v1.1.

### F-UPLOADER-PACKAGE-INCOMPLETE

| Field | Value |
|---|---|
| Family | `F-UPLOADER-*` (new v2.7) |
| Tier | POST |
| Trigger | Any RFA-required narrative section missing from `submission_manifest.yaml`. (At v1 the required-attachments walk is informational/WARN per §12.7 item 2; becomes hard-block at v1.1 when the attachment family lands via §4 v2.7.1 / §12 v1.1.) |
| Routing effect | Hard-block. Package not surfaced to operator. |
| Admin-risk | Appended at MED severity (recoverable: operator adds missing artifact, re-runs). |
| Severity | MED |
| Predicate | `pipeline/logician/gates/f_uploader_package_incomplete.py::check_uploader_package_incomplete` |
| Bypass | M13 |

### F-UPLOADER-FORMAT-MISMATCH

| Field | Value |
|---|---|
| Family | `F-UPLOADER-*` |
| Tier | POST |
| Trigger | Wrong file format vs. portal requirement; OR portal page-limit exceeded; OR portal file-size exceeded |
| Routing effect | Hard-block. Format-mismatched files not staged. |
| Admin-risk | MED |
| Severity | MED |
| Predicate | `pipeline/logician/gates/f_uploader_format_mismatch.py::check_uploader_format_mismatch` |
| Bypass | M13 |

### F-UPLOADER-AUTOSUBMIT-ATTEMPTED

| Field | Value |
|---|---|
| Family | `F-UPLOADER-*` |
| Tier | PRE |
| Trigger | Any code path that attempts portal submission (HTTP POST/PUT to portal endpoint, function annotated `@submission_action`, `UploaderOutput.submitted = True`) |
| Routing effect | Hard-block; fail-closed. |
| Admin-risk | Appended at HIGH severity (architectural-prohibition violation). |
| Severity | HIGH |
| Predicate | `pipeline/logician/gates/f_uploader_autosubmit_attempted.py::check_uploader_autosubmit_attempted` |
| Bypass | **NONE — architecturally prohibited per architecture v7.0.6** |
| Three-layer defense | (1) AST-lint rule R-UPLOADER-NO-SUBMIT (CI + LOCK); (2) Cedar policy `uploader_no_submit.cedar`; (3) `UploaderOutput.__post_init__` runtime assertion. |

### F-UPLOADER-SIGNATURE-MISSING

| Field | Value |
|---|---|
| Family | `F-UPLOADER-*` |
| Tier | PRE |
| Trigger | `UploaderInput.operator_signature is None` |
| Routing effect | Hard-block. |
| Admin-risk | Appended at MED severity. |
| Severity | MED |
| Predicate | `pipeline/logician/gates/f_uploader_signature_missing.py::check_uploader_signature_missing` (thin wrapper over `pipeline/orchestrator/seats/uploader.py::f_uploader_signature_missing`) |
| Bypass | M13 |

### F-UPLOADER-CONTENT-MUTATION

| Field | Value |
|---|---|
| Family | `F-UPLOADER-*` (secondary) |
| Tier | POST |
| Trigger | Deterministic text-extraction diff between input `SectionDraft.body_text` and output document text reveals non-whitespace delta beyond format-artifact normalization |
| Routing effect | Hard-block. Indicates format-conversion bug. |
| Admin-risk | Appended at HIGH severity (Law 2 boundary-drift signal). |
| Severity | HIGH |
| Predicate | `pipeline/logician/gates/f_uploader_content_mutation.py::check_uploader_content_mutation` |
| Bypass | M13 |

### F-UPLOADER-INPUT-INCONSISTENT

| Field | Value |
|---|---|
| Family | `F-UPLOADER-*` (secondary) |
| Tier | PRE |
| Trigger | `claim_evidence_map` is not the union of `section_drafts[*].claim_evidence_map` |
| Routing effect | Hard-block. |
| Admin-risk | MED |
| Severity | MED |
| Predicate | `pipeline/logician/gates/f_uploader_input_inconsistent.py::check_uploader_input_inconsistent` |
| Bypass | M13 |

### F-UPLOADER-RFA-MISSING

| Field | Value |
|---|---|
| Family | `F-UPLOADER-*` (secondary) |
| Tier | PRE |
| Trigger | `RfaExtractedRecord` absent from input OR `rfa_content_sha3_512` does not match session manifest pin |
| Routing effect | Hard-block (Law 1 RFA-is-truth). |
| Admin-risk | HIGH |
| Severity | HIGH |
| Predicate | `pipeline/logician/gates/f_uploader_rfa_missing.py::check_uploader_rfa_missing` |
| Bypass | M13 |

### F-UPLOADER-SIGNATURE-MISMATCH

| Field | Value |
|---|---|
| Family | `F-UPLOADER-*` (secondary) |
| Tier | PRE |
| Trigger | `operator_signature.bundle_content_hash` does not match SHA3-512 of `SubmissionBundle` bytes at `submission_bundle_ref` |
| Routing effect | Hard-block. Bundle was modified after operator sign-off. |
| Admin-risk | HIGH (signature integrity violation). |
| Severity | HIGH |
| Predicate | `pipeline/logician/gates/f_uploader_signature_mismatch.py::check_uploader_signature_mismatch` (thin wrapper over `pipeline/orchestrator/seats/uploader.py::f_uploader_signature_missing` — same predicate, different surface code) |
| Bypass | M13 |

### F-UPLOADER-ORG-CROSS-REF

| Field | Value |
|---|---|
| Family | `F-UPLOADER-*` (secondary) |
| Tier | PRE |
| Trigger | Input bundle references paths under more than one `orgs/<slug>/`. Sweep covers `org_slug`, every `AttachmentRef.file_path`, AND `submission_bundle_ref` (HIGH-1e fix from §4 v2.7 pre-fix dispatch) |
| Routing effect | Hard-block (Law 3 org-isolation). |
| Admin-risk | HIGH (Law-3 violation indicator). |
| Severity | HIGH |
| Predicate | `pipeline/logician/gates/f_uploader_org_cross_ref.py::check_uploader_org_cross_ref` (Protocol-DI wrapper; production binds the seat-side `f_uploader_org_cross_ref` predicate via `pipeline/logician/gates/_uploader_defaults.py`) |
| Bypass | M13 |

### F-UPLOADER-FIELD-MAP-CLOUD-ROUTED

| Field | Value |
|---|---|
| Family | `F-UPLOADER-*` (added by Cowork §12 pre-fix slice) |
| Tier | PRE |
| Trigger | Field-map slot-fill stage receives any input classified as Confidential per the §0.5 classification register; cloud-routed slot-fill is forbidden when Confidential values are in scope (architecture v7.0.7 amendment). |
| Routing effect | Hard-block. Field-map stage must re-route to local-only or operator-fill. |
| Admin-risk | HIGH (classification-discipline violation). |
| Severity | HIGH |
| Predicate | `pipeline/logician/gates/f_uploader_field_map_cloud_routed.py::check_uploader_field_map_cloud_routed` *(predicate file authored as v1-LOCK companion edit per Audit-#1 RT-5c closure; input shape `FieldMapCallContext` defined inline at §12.9.6 of the §12 v1 blueprint and covered by §0.5 row 229)* |
| Bypass | M13 |

---

## §11 Law-map additions (v2.7)

| Law | Mechanism | Gate type | v2.7 addition |
|---|---|---|---|
| Law 1 — RFA is truth | Logician PRE | PRE-30 | F-UPLOADER-RFA-MISSING — bundle blocked if RFA pin mismatch |
| Law 1 — RFA is truth | Logician POST | POST-17 | F-UPLOADER-PACKAGE-INCOMPLETE — every RFA-required section must appear in staged manifest (mandatory-attachment walk informational/WARN at v1 per §12.7; hard-block at v1.1) |
| Law 1 — RFA is truth | Logician POST | POST-18 | F-UPLOADER-FORMAT-MISMATCH — RFA-required format / page-limit / file-size is the truth source for the assembled package |
| Law 2 — No boundary drift | Logician POST | POST-17 | F-UPLOADER-PACKAGE-INCOMPLETE — RFA-required scope is the boundary; missing sections narrow scope |
| Law 2 — No boundary drift | Logician POST | POST-19 | F-UPLOADER-CONTENT-MUTATION — Uploader is renderer, not editor; any text-layer mutation is boundary drift |
| Law 3 — Org isolation | Logician PRE | PRE-34 | F-UPLOADER-ORG-CROSS-REF — input bundle limited to single `orgs/<slug>/` (sweeps `org_slug` + every resolvable attachment-side path + `submission_bundle_ref`) |
| Law 5 — Applicant brings substance | Logician PRE | PRE-31, PRE-32 | F-UPLOADER-SIGNATURE-MISSING + F-UPLOADER-SIGNATURE-MISMATCH — operator must have signed the exact bundle being assembled |
| Law 5 — Applicant brings substance | Logician PRE | PRE-33 | F-UPLOADER-INPUT-INCONSISTENT — `claim_evidence_map` must be the union of `section_drafts[*].claim_evidence_map`; substance traceability requires the union check |
| Architectural invariant — prepare-and-stage discipline | Logician PRE (no bypass) | PRE-29 | F-UPLOADER-AUTOSUBMIT-ATTEMPTED — auto-submit architecturally prohibited |
| Architectural invariant — classification discipline (v7.0.7) *(Cowork-slice)* | Logician PRE | PRE-35 | F-UPLOADER-FIELD-MAP-CLOUD-ROUTED — field-map slot-fill with Confidential input may not be cloud-routed; bound by the §0.5 classification register |

**Path-C deferred Law-map rows** (v1.1 surface, registered in §4 v2.7.1):
Law 5 attachment-substance rows (F-UPLOADER-ATTACHMENT-MISSING +
F-UPLOADER-ATTACHMENT-TAMPERED) and the Law 4 admin-risk row
(F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED) land with §12 v1.1.

---

## §0.5 Interface Index paired-commit row citations (v2.7)

Per §0.5 paired-commit discipline, F-INDEX-STALE PRE-gate fires-closed if
any gate is referenced without its corresponding §0.5 row. Row IDs below
resolve against `pipeline/blueprint/v0.1/section_00_5_section_12_uploader.json`
(§0.5 v9 SCOPING DRAFT 2026-05-09, 21 amendment rows). Path-C reconciliation
2026-05-09 stitched the 15 cleanly-resolvable placeholders to concrete row
IDs and collapsed the 5 many-to-one PRE-check placeholders to the
consolidated `uploader.pre_gate.input_invariants.v1` row per §4 v2.2
consolidated-check pattern (preserves §12.9.5 explode-pattern precedent at
the failure-code layer; consolidates at the check-callable layer).

**Per-gate explode discipline.** Failure codes get one §0.5 row apiece (10
of the 13 originally planned; 3 attachment codes deferred to v2.7.1). PRE
and POST gate-check primitives follow §12 v1's actual implementation: 3
PRE-checks + 3 POST-checks land in v2.7's row set; the consolidated
`input_invariants` PRE-check covers 5 v2.7 failure codes per the §4 v2.2
pattern.

### Failure-code row citations (10 rows — 9 v2.7 base + 1 Cowork-slice)

| Failure code | §0.5 v9 primitive_id |
|---|---|
| `F-UPLOADER-PACKAGE-INCOMPLETE` | `uploader.failure_code.F-UPLOADER-PACKAGE-INCOMPLETE.v1` |
| `F-UPLOADER-FORMAT-MISMATCH` | `uploader.failure_code.F-UPLOADER-FORMAT-MISMATCH.v1` |
| `F-UPLOADER-AUTOSUBMIT-ATTEMPTED` | `uploader.failure_code.F-UPLOADER-AUTOSUBMIT-ATTEMPTED.v1` |
| `F-UPLOADER-SIGNATURE-MISSING` | `uploader.failure_code.F-UPLOADER-SIGNATURE-MISSING.v1` |
| `F-UPLOADER-CONTENT-MUTATION` | `uploader.failure_code.F-UPLOADER-CONTENT-MUTATION.v1` |
| `F-UPLOADER-INPUT-INCONSISTENT` | `uploader.failure_code.F-UPLOADER-INPUT-INCONSISTENT.v1` |
| `F-UPLOADER-RFA-MISSING` | `uploader.failure_code.F-UPLOADER-RFA-MISSING.v1` |
| `F-UPLOADER-SIGNATURE-MISMATCH` | `uploader.failure_code.F-UPLOADER-SIGNATURE-MISMATCH.v1` |
| `F-UPLOADER-ORG-CROSS-REF` | `uploader.failure_code.F-UPLOADER-ORG-CROSS-REF.v1` |
| `F-UPLOADER-FIELD-MAP-CLOUD-ROUTED` *(Cowork-slice)* | `uploader.failure_code.F-UPLOADER-FIELD-MAP-CLOUD-ROUTED.v1` |

### Per-gate-check row citations (6 §0.5 v9 rows — 1 consolidated PRE + 2 distinct PRE + 3 POST)

| Gate scope | §0.5 v9 primitive_id | Consolidated codes (audit-trail clarity) |
|---|---|---|
| PRE-29 (F-UPLOADER-AUTOSUBMIT-ATTEMPTED) | `uploader.pre_gate.autosubmit_structural.v1` | — |
| PRE-30 / PRE-31 / PRE-32 / PRE-33 / PRE-34 (consolidated bundle invariants) | `uploader.pre_gate.input_invariants.v1` | F-UPLOADER-RFA-MISSING; F-UPLOADER-SIGNATURE-MISSING (both sub-tags `.absent` / `.hash_mismatch`); F-UPLOADER-SIGNATURE-MISMATCH (subclass of SIGNATURE-MISSING.hash_mismatch); F-UPLOADER-INPUT-INCONSISTENT; F-UPLOADER-ORG-CROSS-REF (both sub-tags `.multi_org_path` / `.symlink_escape`) — single check callable per §4 v2.2 consolidated pattern. |
| PRE-35 (F-UPLOADER-FIELD-MAP-CLOUD-ROUTED) | `uploader.pre_gate.field_map_routing.v1` | — |
| POST-17 (F-UPLOADER-PACKAGE-INCOMPLETE) | `uploader.post_gate.package_completeness.v1` | — |
| POST-18 (F-UPLOADER-FORMAT-MISMATCH) | `uploader.post_gate.format_compliance.v1` | — |
| POST-19 (F-UPLOADER-CONTENT-MUTATION) | `uploader.post_gate.content_mutation.v1` | — |

(Total v2.7 §0.5 v9 row citations: 10 failure-code + 6 per-gate-check = 16.
The consolidated `input_invariants.v1` row backs 5 of the 7 PRE-29…PRE-35
gate ordering positions per the §4 v2.2 consolidated-check pattern; PRE-29
and PRE-35 retain distinct check callables. The §12.9.5 explode-pattern
precedent for SIGNATURE-MISMATCH-as-distinct-failure-code is preserved at
the failure-code-row layer (10 distinct rows); consolidation occurs at the
check-callable layer only, per §4 v2.2.)

### v2.7.1 horizon stub — attachment family deferred to §12 v1.1

Per Path C reconciliation (2026-05-09) the §12 v1 path-b decision defers
attachments to §12 v1.1 (per §OQ-12.6). The following six §4 primitives
are NOT in v2.7 scope and will register at companion-LOCK with §12 v1.1
via §4 v2.7.1 amendment (`section_04_v2_7_1_attachment_family_amendment.md`):

| Deferred primitive | Tier | Notes |
|---|---|---|
| `uploader.failure_code.F-UPLOADER-ATTACHMENT-TAMPERED.v1` | PRE | Attachment-hash-continuity gate. Requires `AttachmentRef.content_sha3_512` field (lands in §12 v1.1). |
| `uploader.failure_code.F-UPLOADER-ATTACHMENT-MISSING.v1` | PRE | Attachment-file-existence gate. Requires `AttachmentRef.file_path` field (lands in §12 v1.1). |
| `uploader.failure_code.F-UPLOADER-ATTACHMENT-ADMIN-RISK-UNFLAGGED.v1` | POST (v1.1 engagement) | Attachment-admin-risk-register sweep. Requires admin-risk register surface ready in v1.1. |
| `uploader.pre_gate.attachment_existence.v1` *(authored at §0.5 v10)* | PRE-check | Companion check for ATTACHMENT-MISSING; row not present in §0.5 v9, lands with §12 v1.1. |
| `uploader.pre_gate.attachment_integrity.v1` *(authored at §0.5 v10)* | PRE-check | Companion check for ATTACHMENT-TAMPERED; row not present in §0.5 v9, lands with §12 v1.1. |
| `uploader.post_gate.attachment_admin_risk.v1` *(authored at §0.5 v10)* | POST-check | Companion check for ATTACHMENT-ADMIN-RISK-UNFLAGGED; row not present in §0.5 v9, lands with §12 v1.1. |

These primitives intentionally do not appear in §4 v2.7's row-citation
block above — registering them at v2.7 would trip F-INDEX-STALE against
§0.5 v9 (which has no rows for them by design). The §4 v2.7.1 stub
authored as a companion-lock placeholder against §12 v1.1.

## Re-convergence note

This amendment is the §4 slice of a parallel three-session re-convergence:

  - **Cowork session** — §12 v1 Uploader blueprint pre-fix (gate spec
    surface, M13 policy clarification, attachment path-b deferral) +
    §0.5 v9 row authoring (21 amendment rows, final primitive_ids).
  - **Code session** — §4 v2.7 amendment text, uploader.py
    Protocol-DI / assert-to-raise / dataclasses.replace closure / org_slug
    bundle_ref sweep, ast_lint R-UPLOADER-NO-SUBMIT rule + fixtures,
    Logician gate wrapper Protocol-DI refactor, MEDIUM-tier composition
    tests.
  - **Path-C reconciliation pass (2026-05-09, this state)** — §4 v2.7
    narrowed to v1-scope; 15 cleanly-resolvable placeholders stitched
    against §0.5 v9 primitive_ids; 5 many-to-one PRE-checks consolidated
    to `uploader.pre_gate.input_invariants.v1` per §4 v2.2 pattern; 6
    attachment primitives excised + surfaced in v2.7.1 horizon stub.

§4 v2.7 row-citation block now resolves to zero `<§0.5_ROW_ID_PENDING:...>`
strings against §0.5 v9. WS-F Audit #1 cross-family Thesis dispatches
against this post-stitch artifact set the moment WS-A-Review (Tier-0.5,
concurrent) clears.

Companion §4 v2.7.1 attachment-family amendment filed as SCOPING DRAFT
at `pipeline/blueprint/v0.1/section_04_v2_7_1_attachment_family_amendment.md`;
companion-LOCKs with §12 v1.1.

---

## Test reference

Per-gate tests live under `tests/logician/gates/test_f_uploader_*.py` —
one test module per gate. Each module includes:

- **Positive case** — predicate inputs satisfy the contract; assert PASS.
- **Negative case** — predicate inputs violate the contract; assert FAIL
  with the correct `F-UPLOADER-*` code.
- **Targeted edge cases** specific to the predicate's failure modes.

Full integration tests (end-to-end Uploader runs against fixture portals)
are part of the §12 Uploader test suite at `tests/seats/uploader/`, not
duplicated here.

---

## v2.1 LOCKED state preserved

The text of §4 v2.1 is preserved in its entirety. This amendment appends
§4.18, seven PRE-gate rows (PRE-29 … PRE-35), three POST-gate rows
(POST-17 … POST-19), and ten §6 failure-code rows. It does not modify
any text locked at v2.1 / v2.2 / v2.3 / v2.4 / v2.5 / v2.6.

The LOCK sentinel updates from "v2.6 SCOPING DRAFT 2026-05-09" to
"v2.7 SCOPING DRAFT 2026-05-09 (Path C reconciliation 2026-05-09)" upon
publish; "LOCKED 2026-05-09" upon Thesis pass. Companion §4 v2.7.1
amendment registers the deferred attachment family at §12 v1.1
companion-LOCK.

---

## Open items for Thesis

1. ~~**§0.5 row granularity.** Fold per-gate pre-gate-check / post-gate-check
   rows under the family `mechanism` row (current draft) vs. one §0.5 row
   per gate (pattern matches v2.2 consolidated). Operator preference
   needed before LOCK.~~ **RESOLVED via Path C reconciliation 2026-05-09.**
   §0.5 v9 implemented the §4 v2.2 consolidated-check pattern: 5 PRE
   failure codes (RFA-MISSING / SIGNATURE-MISSING / SIGNATURE-MISMATCH /
   INPUT-INCONSISTENT / ORG-CROSS-REF) collapse to single
   `uploader.pre_gate.input_invariants.v1` callable; PRE-29
   (autosubmit_structural) and PRE-35 (field_map_routing) retain distinct
   callables; POST checks one-per-gate. Audit-trail clarity preserved at
   the failure-code-row layer (10 distinct rows in §6 + §0.5).
2. **Whether `F-UPLOADER-SIGNATURE-MISMATCH` should be a sub-code of
   `F-UPLOADER-SIGNATURE-MISSING`.** §12.9.5 specifies "distinct code for
   audit-trail clarity." Current draft preserves distinct codes; both are
   M13-bypass-eligible. Could be folded if Thesis prefers parent-only +
   `.mismatch` sub-tag. (§0.5 v9 row description for SIGNATURE-MISMATCH
   notes "Audit-trail subclass of F-UPLOADER-SIGNATURE-MISSING.hash_mismatch
   — both codes resolve via the same predicate at the check level" —
   formal subclass relationship Thesis-preference-bound.)
3. **AST-lint rule R-UPLOADER-NO-SUBMIT** is referenced as a defense layer
   for PRE-29 but not yet implemented. Tracked as a §12 LOCK companion
   edit (per §12.13.1 `test_f_uploader_autosubmit_attempted_ast_lint`).
   Not blocking this amendment's LOCK. (Note: prior daily_log entry
   2026-05-09 confirms R-UPLOADER-NO-SUBMIT is now registered in
   `pipeline/linting/ast_lint.py::DEFAULT_RULES` — this open item may be
   downgradeable to RESOLVED pending Thesis verification of fixture
   coverage.)

---

## L-005 Audit record (pending)

Awaiting Thesis dispatch. Cross-family roster per WS-B per dispatch plan.
