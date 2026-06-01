---
title: Blueprint §4 Logician — Amendment v2.x WS-L (v0.2 gate-family registration — Funder Intel + KFR residuals + F-CLASS-* dormant primitives landed; HORIZON rows for support agents)
filed: 2026-05-10
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-10 — v0.1 Beta architectural gate CLEARED. L-006 dormant-binding ACTIVATED at this LOCK. L-005 strict two-cycle CLOSED with FULL live cross-family rigor (Editor=Llama 3.3 70B/Groq + Judge=Gemini 2.5 Pro/Google + Red Team=GPT-OSS 120B/Groq) — seventh substantive v0.1+v0.2 round at this rigor level. Cycle 2 PARTIAL (RT-04/RT-05) REJECTED with rationale (Red Team premise contradicted by on-disk test file contents); Cycle 2 NEW defense-in-depth notes (NF-DD-01 + NF-DD-02) folded into §16.10.5 v0.2 deferred items. Compound-LOCK sibling 1/2 paired with §0.5 v14 amendment. Audit trail: pipeline/validation/v4_v2_x_thesis_2026-05-10/. (DRAFT history: Code phase Slices 1+2+3+4 LANDED 2026-05-10 — Funder Intel + KFR residuals + F-CLASS-* dormant primitives + v7.0.4-M1 corrective predicates; Cycle 1 closures applied 2026-05-10; Cycle 2 verification CLOSED 2026-05-10; this amendment LOCKED 2026-05-10.)
parent_lock: pipeline/blueprint/v0.1/section_04_logician.md (v2.1 LOCKED 2026-04-19, hash e0507e6daaa18676)
parent_amendment: pipeline/blueprint/v0.1/section_04_v2_2_consolidated_amendment.md (v2.2 LOCKED 2026-04-21 — F-AMDT-01..F-AMDT-12 structural amendment-enforcement gates; the format pattern this amendment mirrors)
companion_amendments:
  - "pipeline/blueprint/v0.1/section_04_v7_0_5_companion.md (Funder Intel family spec — landed at v7.0.5 LOCK 2026-05-10 row 179; this v2.x amendment realizes the gates)"
  - "pipeline/blueprint/v0.1/section_04_v2_x_uploader_gates_amendment.md (§4 v2.7 Uploader family — SCOPING DRAFT 2026-05-09; modules on disk; WS-F Audit #1 in-flight; full LOCK at WS-F re-convergence)"
  - "pipeline/blueprint/v0.1/section_04_v2_7_1_attachment_family_amendment.md (Uploader attachment family — companion-LOCKs with §12 v1.1)"
  - "pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md (KFR family + AWARD-INGEST — LOCKED 2026-05-09 row 178; Slice 2 of this amendment realizes residual gates)"
  - "pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md (Funder Intel + Match Database — LOCKED 2026-05-10 row 179; Slice 1 of this amendment realizes the 7 gates)"
  - "pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md (Beta classification-driven routing — LOCKED 2026-05-10 row 180; Slice 3 of this amendment realizes the 12 F-CLASS-* dormant primitives per L-006 + §5.1 binding)"
ws_dispatch: WS-L per pipeline/planning/v0_2_dispatch_plan_2026-05-09.md §WS-L
session_metrics: pipeline/metrics/session_log.jsonl
companion_code_landed_slice_1:
  - "pipeline/logician/gates/f_match_db_cross_org.py (NEW)"
  - "pipeline/logician/gates/f_vector_ns_mismatch.py (NEW)"
  - "pipeline/logician/gates/f_channel_g_cross_org_leak.py (NEW — includes decode-rescan cascade)"
  - "pipeline/logician/gates/f_channel_g_sanitization_bypass.py (NEW — advisory)"
  - "pipeline/logician/gates/f_match_db_consent_tier_violation.py (NEW)"
  - "pipeline/logician/gates/f_funder_corpus_stale.py (NEW — per-funder-type defaults)"
  - "pipeline/logician/gates/f_funder_corpus_integrity.py (NEW — SHA3-512 per-read; no byte caching)"
  - "pipeline/logician/gates/__init__.py (UPDATED — exports 7 Funder Intel + 11 Uploader gates added to package surface)"
companion_tests_landed_slice_1:
  - "tests/logician/gates/test_f_match_db_cross_org.py (10 tests; PASS)"
  - "tests/logician/gates/test_f_vector_ns_mismatch.py (11 tests; PASS)"
  - "tests/logician/gates/test_f_channel_g_cross_org_leak.py (11 tests; PASS — base64/hex/URL-encoding evasion coverage)"
  - "tests/logician/gates/test_f_channel_g_sanitization_bypass.py (6 tests; PASS)"
  - "tests/logician/gates/test_f_match_db_consent_tier_violation.py (10 tests; PASS)"
  - "tests/logician/gates/test_f_funder_corpus_stale.py (10 tests; PASS)"
  - "tests/logician/gates/test_f_funder_corpus_integrity.py (8 tests; PASS)"
test_suite_state_at_slice_1_close: 1891 logician tests passing (1253 baseline + 68 new from Slice 1 + 570 from broader logician/ scope now properly collected via __init__.py wiring). Full pytest suite has a pre-existing hang at ~96% in non-gate test territory (infrastructure / network test) — flagged for separate triage; outside Slice 1 surface.
companion_code_landed_slice_2:
  - "pipeline/logician/gates/f_extractor_fabrication.py (NEW — substrate-dispatched verbatim-match per WS-E §11.9.1.A/B/C/D)"
  - "pipeline/logician/gates/f_extractor_award_signature_invalid.py (NEW — proposal + award sub-codes)"
  - "pipeline/logician/gates/f_kfr_signature_validation.py (NEW — combined SIGNATURE-INVALID + AUDIT-CHAIN-BROKEN per v2.2 F-AMDT-08/09/10/11 sub-code-collapse precedent)"
  - "pipeline/logician/gates/f_logician_fact_tolerance_drift.py (NEW — widened tolerance without re-confirm)"
  - "pipeline/logician/gates/f_logician_fact_needed_required.py (NEW — SP0 hard-block)"
  - "pipeline/logician/gates/f_benchmark_contains_per_org_ref.py (NEW — path + value sub-codes; workspace-shared canonical-value probes)"
  - "pipeline/logician/gates/__init__.py (UPDATED — exports 6 KFR residual gates added to package surface)"
companion_tests_landed_slice_2:
  - "tests/logician/gates/test_f_extractor_fabrication.py (25 tests; PASS)"
  - "tests/logician/gates/test_f_extractor_award_signature_invalid.py (9 tests; PASS)"
  - "tests/logician/gates/test_f_kfr_signature_validation.py (19 tests; PASS — covers both sub-codes in single module)"
  - "tests/logician/gates/test_f_logician_fact_tolerance_drift.py (18 tests; PASS)"
  - "tests/logician/gates/test_f_logician_fact_needed_required.py (13 tests; PASS)"
  - "tests/logician/gates/test_f_benchmark_contains_per_org_ref.py (14 tests; PASS)"
test_suite_state_at_slice_2_close: 1989 logician tests passing (1891 at Slice 1 close → 1989 = +98 from Slice 2). 1419 logician/gates/ subset green. Pre-existing pytest hang in non-gate test territory still outside WS-L surface.
ast_lint_state_at_slice_2_close: scripts/run_lint.sh pipeline/logician/ exit=0 — clean. Verification at Slice 3 close still expected.
companion_code_landed_slice_3:
  - "pipeline/logician/gates/f_class_register.py (NEW — 4 sub-codes: MISSING/UNSIGNED/SIGNATURE-INVALID/HASH-MISMATCH; combined per shared register-reader + SignatureVerifyCallable + HashBytesCallable injection surface)"
  - "pipeline/logician/gates/f_class_outbound_boundary.py (NEW — 4 sub-codes: SLOT-ID-NON-OPAQUE (PRE) / CLOUD-RECEIVED-CONFIDENTIAL (POST P0) / CLOUD-RECEIVED-OPAQUE-SLOT-FILLED (POST) / HIGH-STAKES-FLAG-LEAK (POST); shared payload-scanner injection surface)"
  - "pipeline/logician/gates/f_class_routing_indeterminate.py (NEW — single per-call PRE; fail-closed-default-local on indeterminate posture)"
  - "pipeline/logician/gates/f_class_new_fact_unclassified.py (NEW — per-cycle PRE; pending_operator_review consumed-fact block)"
  - "pipeline/logician/gates/f_class_per_grant_override.py (NEW — per-grant PRE; per_grant_sp0_signature Ed25519 verify)"
  - "pipeline/logician/gates/f_class_router_template_signature.py (NEW — PRE update; SN-LLC pinned-key Ed25519 verify before router-template apply)"
  - "pipeline/logician/gates/f_class_coverage_incomplete.py (NEW — META PRE-cycle gate; verifies every v7.0.7 §5.1 code has live module + test)"
  - "pipeline/logician/gates/__init__.py (UPDATED — exports 7 F-CLASS-* modules + dataclasses + check functions onto package surface)"
companion_tests_landed_slice_3:
  - "tests/logician/gates/test_f_class_register.py (27 tests; PASS — 6 missing + 8 unsigned + 6 signature-invalid + 7 hash-mismatch)"
  - "tests/logician/gates/test_f_class_outbound_boundary.py (32 tests; PASS — 8 slot-id-non-opaque + 8 cloud-confidential + 7 opaque-slot-filled + 9 high-stakes-leak)"
  - "tests/logician/gates/test_f_class_routing_indeterminate.py (12 tests; PASS — public/shareable + indeterminate variants + fail-closed-local default)"
  - "tests/logician/gates/test_f_class_new_fact_unclassified.py (9 tests; PASS — pending_operator_review × consumed/non-consumed × confidential matrix)"
  - "tests/logician/gates/test_f_class_per_grant_override.py (10 tests; PASS — no-override + signed + missing-sig + raise + non-mapping + truthy-non-True identity check)"
  - "tests/logician/gates/test_f_class_router_template_signature.py (10 tests; PASS — wrong-pubkey + empty-fields + raise + truthy-non-True identity check)"
  - "tests/logician/gates/test_f_class_coverage_incomplete.py (9 tests; PASS — full coverage with real on-disk paths + missing entry/module/test legs + raise + empty + no-M13 detail check)"
test_suite_state_at_slice_3_close: 2097 logician tests passing (1989 at Slice 2 close → 2097 = +108 from Slice 3). 1527 logician/gates/ subset green (1419 → 1527 = +108).
ast_lint_state_at_slice_3_close: scripts/run_lint.sh pipeline/logician/ exit=0 — clean.
version_wording_discipline: "DRAFT" inside this file refers to on-disk DRAFT state at filing time. The Funder Intel family is on disk + tested at Slice 1 close 2026-05-10. KFR residuals on disk + tested at Slice 2 close 2026-05-10. F-CLASS-* dormant primitives on disk + tested at Slice 3 close 2026-05-10. Cowork Thesis dispatch fires next as a separate session.
---

# Amendment v2.x — v0.2 gate-family registration (WS-L)

## §0. Amendment intent + slice plan

This amendment registers the v0.2 gate families that landed via the v7.0.4 (KFR) + v7.0.5 (Funder Intel) + v7.0.7 (Classification routing) + **v7.0.4-M1 (corrective predicates — see §16)** architecture amendments, plus the v2.7 Uploader family that's in-flight at WS-F. It mirrors the §4 v2.2 consolidated amendment format pattern for reading-surface coherence; per-architecture-amendment companion files (`section_04_v7_0_5_companion.md`, `section_04_v2_x_uploader_gates_amendment.md`) remain canonical for the per-family enforcement specs.

> **Slice-count update (Cycle 1 closure E-01):** The Code phase originally planned three slices per L-012 pre-flight scope check; v7.0.4-M1 LOCKED 2026-05-10 row 190 added a fourth slice (M1 corrective predicates) that landed the same day. **Total slice count: four** — see §16 for Slice 4 close. The §0/§10 three-slice framing below is preserved as the historical filing record; §16 documents the post-filing reality.

The Code phase is sliced into three sessions per L-012 pre-flight scope check (~25 new gate modules total exceeds the L-012 N=2 multi-gate dispatch ceiling). This amendment text grows incrementally across the three slices (plus Slice 4 retroactively per the slice-count-update note above); the Cowork Thesis phase fires as a separate dispatch when all four Code slices land.

**Slice 1 (this filing — landed 2026-05-10)**: Funder Intel family (7 gates) + Uploader family wiring (11 gates pre-existing) + amendment skeleton + HORIZON rows for v0.2+ support agents.

**Slice 2 (this filing — landed 2026-05-10)**: 6 new dedicated gate modules realizing the KFR family SIBLING failure codes per v7.0.4 §4 (F-EXTRACTOR-FABRICATION, F-EXTRACTOR-AWARD-SIGNATURE-INVALID, combined F-KFR-SIGNATURE-INVALID + F-KFR-AUDIT-CHAIN-BROKEN per the v2.2 F-AMDT-08/09/10/11 sub-code-collapse precedent, F-LOGICIAN-FACT-TOLERANCE-DRIFT, F-LOGICIAN-FACT-NEEDED-REQUIRED, F-BENCHMARK-CONTAINS-PER-ORG-REF). Existing `f_logician_fact_drift.py` (942 LOC umbrella) keeps the F-LOGICIAN-FACT-DRIFT umbrella code; per the §3.5 inventory pass, the seven F-FACT-DRIFT-* UMBRELLA sub-codes (UNTRACED / OUT-OF-TOLERANCE / EXPIRED / EXPIRED-LANDING / DERIVATION-UNAUTHORIZED / DERIVATION-CHAIN / DERIVATION-KEY-RETIRED) stay forward-pending — splitting them requires schema + claim-extractor + AST-walker work that exceeds Slice 2/3 capacity.

**Slice 3 (this filing — landed 2026-05-10)**: 12 F-CLASS-* gates per v7.0.7 §5.1 LOCKED row 180 (the dormant binding L-006 ties this amendment's LOCK ceremony to) consolidated into 7 dedicated modules per the v2.2 F-AMDT-08/09/10/11 sub-code-collapse precedent. Module decomposition: `f_class_register.py` (4 sub-codes — MISSING/UNSIGNED/SIGNATURE-INVALID/HASH-MISMATCH; share register-reader + SignatureVerifyCallable + HashBytesCallable injection surface), `f_class_outbound_boundary.py` (4 sub-codes — SLOT-ID-NON-OPAQUE/CLOUD-RECEIVED-CONFIDENTIAL/CLOUD-RECEIVED-OPAQUE-SLOT-FILLED/HIGH-STAKES-FLAG-LEAK; share payload-scanner injection surface), `f_class_routing_indeterminate.py` (single PER-CALL), `f_class_new_fact_unclassified.py` (single PER-CYCLE), `f_class_per_grant_override.py` (single PER-GRANT), `f_class_router_template_signature.py` (single PRE update), `f_class_coverage_incomplete.py` (META PRE-cycle gate; verifies every v7.0.7 §5.1 code has live module + test on disk via injected `FileExistsCallable`). The F-CLASS-COVERAGE-INCOMPLETE PRE-cycle gate prevents Beta deployment shipping until §4 v2.x LOCKs through Cowork Thesis.

**Cowork Thesis phase** fires after all three Code slices land (Slice 3 closed 2026-05-10 — Cowork Thesis dispatch is the next session). L-005 two-audit cycle, cross-family per WS-B. The audit reviews:

- Per-gate semantic correctness (failure code, PRE/POST sequence position, deterministic predicate body, enforcement test coverage)
- Per-family registration completeness (every architecture-amendment-declared code has a corresponding §4 row + module + tests)
- Cross-family composition (Funder Intel + KFR + F-CLASS routing interaction)
- F-AMDT-* structural enforcement extension (this amendment registers ~25 new gates; F-AMDT-12 daily-log gate must accept the bulk add)

## §1. Failure-code table — Slice 1 (Funder Intel; LANDED 2026-05-10)

Per v7.0.5 §5 + companion `section_04_v7_0_5_companion.md`. All seven gates registered in `pipeline/logician/gates/__init__.py` and exported on the package surface.

| Code | Tier | Module | Severity | Cycle |
|---|---|---|---|---|
| `F-MATCH-DB-CROSS-ORG` | PRE | `f_match_db_cross_org.py` | P0 (Law 3) | v7.0.5 Cycle 1 RT-01 |
| `F-VECTOR-NS-MISMATCH` | PRE | `f_vector_ns_mismatch.py` | P0 (Law 3) | v7.0.5 Cycle 1 RT-04 |
| `F-CHANNEL-G-CROSS-ORG-LEAK` | POST-extract | `f_channel_g_cross_org_leak.py` | P0 (Law 3) | v7.0.5 Cycle 1 RT-06 |
| `F-CHANNEL-G-SANITIZATION-BYPASS` | advisory | `f_channel_g_sanitization_bypass.py` | P1 | v7.0.5 Cycle 2 Probe B |
| `F-MATCH-DB-CONSENT-TIER-VIOLATION` | PRE-write + Stage-5-read | `f_match_db_consent_tier_violation.py` | P1 (Law 4 + sovereignty) | v7.0.5 Cycle 1 RT-05 |
| `F-FUNDER-CORPUS-STALE` | POST-cite | `f_funder_corpus_stale.py` | P2 (RFA-truth) | v7.0.5 Cycle 1 RT-07 |
| `F-FUNDER-CORPUS-INTEGRITY` | PRE-load + POST-load | `f_funder_corpus_integrity.py` | P0 (Law 5 — fabrication via tamper) | v7.0.5 Cycle 1 RT-03 |

### §1.1 PRE-gate row additions (Funder Intel)

| Order | Check ID | Fires at | Failure code | Bypass |
|---|---|---|---|---|
| PRE-36 | F-MATCH-DB-CROSS-ORG | every Match DB read at I/O wrapper | `F-MATCH-DB-CROSS-ORG` | M13 (audited; HIGH-severity admin-risk) |
| PRE-37 | F-VECTOR-NS-MISMATCH | every Pydantic AI vector-store tool call | `F-VECTOR-NS-MISMATCH` | M13 |
| PRE-38 | F-MATCH-DB-CONSENT-TIER-VIOLATION | Match DB write wrapper, on consent_tier change | `F-MATCH-DB-CONSENT-TIER-VIOLATION` | M13 |
| PRE-39 | F-FUNDER-CORPUS-INTEGRITY | every funder_intel.load() call (pre-load + post-load per v7.0.5 §5.7) | `F-FUNDER-CORPUS-INTEGRITY` | M13 |

PRE-39 fires twice per load (pre-load AND post-load per v7.0.5 §5.7 strengthening — defense-in-depth against tamper). Process-scope BYTE caching is FORBIDDEN per Cycle 2 Probe C closure; per-`load()` re-hash is required.

### §1.2 POST-gate row additions (Funder Intel)

| Order | Check ID | Fires at | Failure code | Bypass |
|---|---|---|---|---|
| POST-20 | F-CHANNEL-G-CROSS-ORG-LEAK | after Scout Channel G text extraction | `F-CHANNEL-G-CROSS-ORG-LEAK` | M13 |
| POST-21 | F-CHANNEL-G-SANITIZATION-BYPASS | post-transform check on downstream Channel G text transforms | `F-CHANNEL-G-SANITIZATION-BYPASS` | advisory (no bypass needed; non-blocking) |
| POST-22 | F-FUNDER-CORPUS-STALE | after Scout match-reasoning composition AND after Scribe KGIE preflight | `F-FUNDER-CORPUS-STALE` | M13 |

### §1.3 Encoding-evasion guard implementation note (Channel G)

`f_channel_g_cross_org_leak.py` implements the decode-then-rescan cascade per v7.0.5 Cycle 2 Probe B closure. The cascade attempts base-64 decode + hex decode + URL decode on every whitespace-separated token of length ≥8 and concatenates the decoded payloads to the scan target. The regex pass then runs on the combined raw + decoded text. Test coverage validates each encoding mode independently (`test_base64_encoded_match_id_caught`, `test_hex_encoded_match_id_caught`, `test_url_encoded_org_ref_caught`) plus the multi-leak aggregation case.

The companion advisory gate `F-CHANNEL-G-SANITIZATION-BYPASS` covers the architectural-discipline layer: any downstream component that further transforms the Channel G extracted text MUST re-invoke the sanitization wrapper as a POST-transform check. The advisory raises at the next REVIEW gate (does not block) — the blocking surface is `F-CHANNEL-G-CROSS-ORG-LEAK` itself, which fires when sanitization actually fails.

### §1.4 Process-scope byte-cache prohibition (Funder Corpus Integrity)

`f_funder_corpus_integrity.py` enforces the v7.0.5 Cycle 2 Probe C closure: the gate compares SHA3-512 of `doc_bytes` against `recorded_hash` on every call. Process-scope byte caching is FORBIDDEN at the I/O-wrapper layer (the gate itself is stateless — the no-cache discipline is enforced by the wrapper that invokes it). Parsed-content caching is permitted post-verification within a single agent invocation.

The default hash callable is `hashlib.sha3_512` imported lazily inside `_hashlib_sha3_512` to keep module-load surface free of crypto-library imports per the §4 v2.2 `_protocols.py` discipline (matches AST-lint R3 spirit — no `import hashlib` at module load). The `HashBytesCallable` Protocol from `pipeline/logician/gates/_protocols.py` is the production-injection seam; tests use a fake hasher to validate the injection path.

## §2. Failure-code table — Uploader family (v2.7 SCOPING DRAFT; landed 2026-05-09)

Per `section_04_v2_x_uploader_gates_amendment.md` (v2.7 SCOPING DRAFT 2026-05-09 + Path C reconciliation 2026-05-09). 10 failure codes (9 base per §12.9 + 1 Cowork-slice F-UPLOADER-FIELD-MAP-CLOUD-ROUTED). 11 modules on disk + the field-map placeholder pending the Cowork §12 fix slice. Slice 1 of this amendment WIRES the existing 10 modules into `pipeline/logician/gates/__init__.py` (they were not previously exported on the package surface).

| Code | Tier | Module | Status |
|---|---|---|---|
| `F-UPLOADER-PACKAGE-INCOMPLETE` | POST-17 | `f_uploader_package_incomplete.py` | exists; wired Slice 1 |
| `F-UPLOADER-FORMAT-MISMATCH` | POST-18 | `f_uploader_format_mismatch.py` | exists; wired Slice 1 |
| `F-UPLOADER-CONTENT-MUTATION` | POST-19 | `f_uploader_content_mutation.py` | exists; wired Slice 1 |
| `F-UPLOADER-AUTOSUBMIT-ATTEMPTED` | PRE-29 | `f_uploader_autosubmit_attempted.py` | exists; wired Slice 1 (NO M13 bypass — architecturally prohibited) |
| `F-UPLOADER-RFA-MISSING` | PRE-30 | `f_uploader_rfa_missing.py` | exists; wired Slice 1 |
| `F-UPLOADER-SIGNATURE-MISSING` | PRE-31 | `f_uploader_signature_missing.py` | exists; wired Slice 1 |
| `F-UPLOADER-SIGNATURE-MISMATCH` | PRE-32 | `f_uploader_signature_mismatch.py` | exists; wired Slice 1 |
| `F-UPLOADER-INPUT-INCONSISTENT` | PRE-33 | `f_uploader_input_inconsistent.py` | exists; wired Slice 1 |
| `F-UPLOADER-ORG-CROSS-REF` | PRE-34 | `f_uploader_org_cross_ref.py` | exists; wired Slice 1 |
| `F-UPLOADER-FIELD-MAP-CLOUD-ROUTED` | PRE-35 | `f_uploader_field_map_cloud_routed.py` | **MISSING** — placeholder reserved per v2.7 §6; pending Cowork §12 fix slice landing per v2.7 amendment Open-Items 3 |

The companion attachment family per `section_04_v2_7_1_attachment_family_amendment.md` (3 failure codes for ATTACHMENT-MISSING / ATTACHMENT-TAMPERED / ATTACHMENT-ADMIN-RISK-UNFLAGGED) has 2 modules on disk (`f_uploader_attachment_missing.py`, `f_uploader_attachment_tampered.py`) and is wired in Slice 1 — the third (admin-risk-unflagged) is a v1.1 surface per the v2.7.1 amendment.

**WS-F coordination note:** WS-F Audit #1 is in-flight on the v2.7 amendment text. If WS-F surfaces gate-shape changes or rename requests, this v2.x amendment's row table for Uploader must be re-stitched at WS-F LOCK. Per the user prompt's WS-L dispatch directive: "may shift if WS-F Audit surfaces changes; coordinate at re-convergence."

## §3. Failure-code table — KFR family residuals (Slice 2 — LANDED 2026-05-10)

Per v7.0.4 §4 + `section_04_v7_0_5_companion.md` Composition section. Slice 2 lands six new dedicated modules covering the KFR-family enforcement surfaces declared at v7.0.4 §1.1, §3.2, §4.4, §5.2, §5.3, §7.2. The pre-existing umbrella module `f_logician_fact_drift.py` (942 LOC) keeps its umbrella `F-LOGICIAN-FACT-DRIFT` code; sub-code splits stay forward-pending per the §3.5 inventory below.

| Code | Tier | Module | Severity | v7.0.4 §ref |
|---|---|---|---|---|
| `F-EXTRACTOR-FABRICATION` | PRE-pre-queue | `f_extractor_fabrication.py` | P0 (Law 5) | §5.2 |
| `F-EXTRACTOR-AWARD-SIGNATURE-INVALID` (umbrella; sub-codes `.proposal` + `.award`) | PRE-AWARD_INGEST | `f_extractor_award_signature_invalid.py` | P0 (Law 5) | §5.3 |
| `F-KFR-SIGNATURE-INVALID` | PRE-load + draft-time read | `f_kfr_signature_validation.py` | HIGH (TAMPER_EVENT) | §1.1 |
| `F-KFR-AUDIT-CHAIN-BROKEN` | PRE-load + draft-time read | `f_kfr_signature_validation.py` (combined module) | HIGH (TAMPER_EVENT) | §1.1 |
| `F-LOGICIAN-FACT-TOLERANCE-DRIFT` | PRE-draft-read | `f_logician_fact_tolerance_drift.py` | HARD_BLOCK | §4.4 |
| `F-LOGICIAN-FACT-NEEDED-REQUIRED` | PRE-SP0-sign-out | `f_logician_fact_needed_required.py` | HARD_BLOCK (no M13) | §3.2 |
| `F-BENCHMARK-CONTAINS-PER-ORG-REF` (umbrella; sub-codes `.path` + `.value`) | PRE-write + PRE-read | `f_benchmark_contains_per_org_ref.py` | HIGH (Law 3) | §7.2 |

### §3.1 PRE-gate row additions (KFR family residuals)

| Order | Check ID | Fires at | Failure code | Bypass |
|---|---|---|---|---|
| PRE-40 | F-EXTRACTOR-FABRICATION | Intake post-extraction, before `pending_facts.yaml` write | `F-EXTRACTOR-FABRICATION` | M13 |
| PRE-41 | F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal | AWARD_INGEST mode entry, won-proposal artifact verify | `F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal` | M13 |
| PRE-42 | F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award | AWARD_INGEST mode entry, award document verify | `F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award` | M13 |
| PRE-43 | F-KFR-SIGNATURE-INVALID | every KFR entry read at I/O wrapper (session start + draft-time) | `F-KFR-SIGNATURE-INVALID` | M13 |
| PRE-44 | F-KFR-AUDIT-CHAIN-BROKEN | every KFR entry read at I/O wrapper (session start + draft-time) | `F-KFR-AUDIT-CHAIN-BROKEN` | M13 |
| PRE-45 | F-LOGICIAN-FACT-TOLERANCE-DRIFT | draft-time KFR fact read, on widened `tolerance_pct` | `F-LOGICIAN-FACT-TOLERANCE-DRIFT` | M13 |
| PRE-46 | F-LOGICIAN-FACT-NEEDED-REQUIRED | SP0 sign-out, before pipeline advances to KGIE | `F-LOGICIAN-FACT-NEEDED-REQUIRED` | **NO M13** — HARD_BLOCK |
| PRE-47 | F-BENCHMARK-CONTAINS-PER-ORG-REF.path | benchmark write into `vault_shared/benchmarks/` AND every read by Scribe / Editor / Judge | `F-BENCHMARK-CONTAINS-PER-ORG-REF.path` | M13 |
| PRE-48 | F-BENCHMARK-CONTAINS-PER-ORG-REF.value | benchmark write into `vault_shared/benchmarks/` AND every read by Scribe / Editor / Judge | `F-BENCHMARK-CONTAINS-PER-ORG-REF.value` | M13 |

PRE-43 and PRE-44 fire on the same event (KFR entry read), and `f_kfr_signature_validation.py` houses both check functions per the v2.2 F-AMDT-08/09/10/11 shared-Protocol-injection-surface precedent (both consume `SignatureVerifyCallable` and `KeyringEntry` sequences).

PRE-46 (F-LOGICIAN-FACT-NEEDED-REQUIRED) explicitly carries no M13 bypass — it exists to prevent fabrication-by-omission, and the operator must resolve at the source (populate the fact OR drop the funder).

PRE-47 / PRE-48 are sub-codes of the same umbrella `F-BENCHMARK-CONTAINS-PER-ORG-REF` and dispatch in a single module: the path leg fires before the value leg (the module short-circuits on path match — value-hash check is the defense-in-depth catch behind path). Both fire at write AND at read per §7.2's hard-block-at-both-ends discipline.

### §3.2 POST-gate row additions (KFR family residuals)

Slice 2 modules are PRE-gates throughout — no new POST rows. The umbrella `F-LOGICIAN-FACT-DRIFT` POST behavior is unchanged at Slice 2 (umbrella module untouched per inventory below).

### §3.3 Substrate-dispatch implementation note (F-EXTRACTOR-FABRICATION)

`f_extractor_fabrication.py` realizes WS-E §11.9.1.A/B/C/D substrate dispatch via a `CandidateFact` input dataclass with mode + substrate dispatch keys validated at construction (frozen kw_only — mode-immutable post-construction per the dispatch directive). The module routes to substrate-specific check helpers:

* PDF (`§11.9.1.A`): unique-page-match. ±1 page tolerance ONLY when mode == AWARD_INGEST AND `operator_award_page_offset_flag` is True.
* DOCX (`§11.9.1.B`): paragraph-index. No ±1 tolerance; DOCX paragraph indices are stable.
* Markdown (`§11.9.1.C`): single-line. 1-based locator per WS-E spec; the module converts to 0-based at the helper boundary.

Symmetric normalization (Unicode NFC + `[\t\n\r\f\v ]+` → single ASCII space + leading/trailing strip) is applied to BOTH the candidate quote AND the source slice before substring containment check. OCR-substitution (`0 ↔ O`, `1 ↔ l`, `5 ↔ S`) is naturally rejected because OCR-substituted variants do not normalize identically — the verbatim test fails them. Ellipsis tokens (`...` and `…`) in the candidate quote are universally rejected before substrate dispatch per §5.2's "quote must literally span start-to-end of asserted source bytes" clause.

### §3.4 Hard-block-no-M13 invariant (F-LOGICIAN-FACT-NEEDED-REQUIRED)

`f_logician_fact_needed_required.py` enforces §3.2's HARD_BLOCK without an M13 bypass surface. The module's predicate carries no operator-override branch; when at least one required-for-current-funder fact is in NEEDED state at SP0 sign-out, the gate fails the SP0 ceremony and the pipeline cannot advance to KGIE. Architectural intent: the gate exists explicitly to prevent fabrication-by-omission (Scribe rephrasing around an absent fact). Operator must populate the fact (full schema) OR drop the funder from the in-flight grant cycle. This is the single Slice-2 gate without M13 reach.

### §3.5 Inventory pass — F-LOGICIAN-FACT-DRIFT umbrella module sub-code coverage

`pipeline/logician/gates/f_logician_fact_drift.py` (942 LOC; v0.2 spec-card-LOCKED) emits exactly ONE failure code: `F-LOGICIAN-FACT-DRIFT`. The seven sub-codes declared at v7.0.4 §4 (UNTRACED / OUT-OF-TOLERANCE / EXPIRED / EXPIRED-LANDING / DERIVATION-UNAUTHORIZED / DERIVATION-CHAIN / DERIVATION-KEY-RETIRED) are NOT split into dedicated codes at the umbrella module surface. Behaviorally:

| v7.0.4 §4 sub-code | Coverage in umbrella | Notes |
|---|---|---|
| `F-FACT-DRIFT-UNTRACED` | partial — surfaces as umbrella `F-LOGICIAN-FACT-DRIFT` with `reason_tag="kfr_no_match"` | sub-code split forward-pending |
| `F-FACT-DRIFT-OUT-OF-TOLERANCE` | partial — surfaces as umbrella `F-LOGICIAN-FACT-DRIFT` with `reason_tag="kfr_value_drift"` | sub-code split forward-pending |
| `F-FACT-DRIFT-EXPIRED` | NOT covered — `_temporal_overlap` filter silently DROPS expired facts from the candidate pool, so claims against expired facts surface as `kfr_no_match` (UNTRACED-coloured) rather than EXPIRED | requires expired-window surfacing rework + sub-code split |
| `F-FACT-DRIFT-EXPIRED-LANDING` | NOT covered — STALE-ACKNOWLEDGED state doesn't exist in current `KfrFact` schema | requires KFR schema extension + sub-code split |
| `F-FACT-DRIFT-DERIVATION-UNAUTHORIZED` | NOT covered — no `derivation_id` annotation parser in claim extractor | requires `<derivation_id="..."/>` annotation extraction + override-table reader + sub-code split |
| `F-FACT-DRIFT-DERIVATION-CHAIN` | NOT covered — no derivation grammar AST validation | requires Python AST walker per §4.5 grammar + sub-code split |
| `F-FACT-DRIFT-DERIVATION-KEY-RETIRED` | NOT covered — no derivation-signature key-currency check | requires `audit_chain_signature` validation against Section 1 key catalog + sub-code split |

**Slice 2 decision:** the inventory gap is documented but NOT closed at Slice 2 surface. The seven sub-code splits are a coherent unit of follow-up work that would bloat Slice 2 beyond the L-012 N=2 multi-gate dispatch ceiling already accommodated by the original three-slice plan. Splitting the umbrella requires (a) surfacing expired facts as a fail-explicit case rather than silent filter, (b) extending KFR schema with STALE-ACKNOWLEDGED state, (c) adding `derivation_id` annotation parsing, (d) adding override-table reader + signature validation, (e) adding AST-walker for derivation grammar. Each is a meaningful authoring round; together they exceed Slice 2 + Slice 3 capacity. Forward-pending follow-up captured in §13 audit trail.

The Slice 2 modules added (F-EXTRACTOR-FABRICATION, F-EXTRACTOR-AWARD-SIGNATURE-INVALID, F-KFR-SIGNATURE-INVALID, F-KFR-AUDIT-CHAIN-BROKEN, F-LOGICIAN-FACT-TOLERANCE-DRIFT, F-LOGICIAN-FACT-NEEDED-REQUIRED, F-BENCHMARK-CONTAINS-PER-ORG-REF) are the SIBLING failure codes registered at v7.0.4 §4 outside the umbrella — orthogonal to the F-FACT-DRIFT-* sub-code surface. Coverage: 7 of the 7 SIBLING codes land at Slice 2; 0 of the 7 UMBRELLA sub-codes split (forward-pending).

## §4. Failure-code table — F-CLASS-* family (Slice 3 — LANDED 2026-05-10; L-006 dormant binding ready for Cowork Thesis activation)

Per v7.0.7 §5.1 LOCKED row 180 + the L-006 dormant-binding pattern. Twelve F-CLASS-* primitives are named at v7.0.7 LOCK as architectural primitives; the Cedar/Python realization landed at this Slice 3 close 2026-05-10. The dormant binding fires at this amendment's Cowork Thesis LOCK ceremony per v7.0.7 §5.1 binding clause. F-CLASS-COVERAGE-INCOMPLETE (PRE-cycle gate) is on disk + tested + green; the META gate verifies every other F-CLASS-* code has a live module + test in `pipeline/logician/gates/`.

Module decomposition (7 modules realize 12 codes per v2.2 F-AMDT-08/09/10/11 sub-code-collapse precedent):

| Code | Tier | Module | Severity | v7.0.7 §ref |
|---|---|---|---|---|
| `F-CLASS-REGISTER-MISSING` | PRE-onboarding | `f_class_register.py` | HARD_BLOCK (no M13) | §5 + §5.1 |
| `F-CLASS-REGISTER-UNSIGNED` | PRE-onboarding | `f_class_register.py` | HARD_BLOCK (no M13) | §5 + §5.1 |
| `F-CLASS-REGISTER-SIGNATURE-INVALID` | PRE-cycle | `f_class_register.py` | HIGH (M13 audited) | §5 + §5.1 |
| `F-CLASS-REGISTER-HASH-MISMATCH` | PRE-cycle | `f_class_register.py` | HIGH (M13 audited) | §5 + §5.1 |
| `F-CLASS-NEW-FACT-UNCLASSIFIED` | PRE-cycle | `f_class_new_fact_unclassified.py` | MEDIUM (M13) | §3.6 + §5.1 |
| `F-CLASS-ROUTING-INDETERMINATE` | PRE-call | `f_class_routing_indeterminate.py` | MEDIUM (M13) | §5 + §5.1 |
| `F-CLASS-SLOT-ID-NON-OPAQUE` | PRE-call (outbound) | `f_class_outbound_boundary.py` | HARD_BLOCK (no M13 — structural) | §1 + §5.1 |
| `F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL` | POST-call (outbound) | `f_class_outbound_boundary.py` | P0 (M13 audited) | §5 + §5.1 |
| `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` | POST-call (outbound) | `f_class_outbound_boundary.py` | P0 (M13 audited) | §1 + §5.1 |
| `F-CLASS-HIGH-STAKES-FLAG-LEAK` | POST-call (outbound) | `f_class_outbound_boundary.py` | HIGH (M13 audited) | §4.1 + §5.1 |
| `F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED` | PRE-per-grant | `f_class_per_grant_override.py` | HIGH (M13 audited) | §3.7 + §7 + §5.1 |
| `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` | PRE update | `f_class_router_template_signature.py` | HIGH (key-rotation only) | §6.1 + §5.1 |
| `F-CLASS-COVERAGE-INCOMPLETE` | META PRE-cycle | `f_class_coverage_incomplete.py` | HARD_BLOCK (no M13) | §5.1 binding |

### §4.1 PRE-gate row additions (F-CLASS-* family)

| Order | Check ID | Fires at | Failure code | Bypass |
|---|---|---|---|---|
| PRE-49 | F-CLASS-REGISTER-MISSING | Beta-shipping precondition (white-glove sign-off step 5) AND every cycle start (existence check) | `F-CLASS-REGISTER-MISSING` | **NO M13** — Beta cannot ship without an operator-signed register per §5 |
| PRE-50 | F-CLASS-REGISTER-UNSIGNED | white-glove sign-off step 5 AND every cycle start | `F-CLASS-REGISTER-UNSIGNED` | **NO M13** |
| PRE-51 | F-CLASS-REGISTER-SIGNATURE-INVALID | every cycle start, on register read | `F-CLASS-REGISTER-SIGNATURE-INVALID` | M13 audited (HIGH admin-risk) |
| PRE-52 | F-CLASS-REGISTER-HASH-MISMATCH | every cycle start, on register read | `F-CLASS-REGISTER-HASH-MISMATCH` | M13 audited (HIGH admin-risk) |
| PRE-53 | F-CLASS-COVERAGE-INCOMPLETE | every cycle start (META — verifies every other F-CLASS-* code has live module + test) | `F-CLASS-COVERAGE-INCOMPLETE` | **NO M13** — architectural commitment binding |
| PRE-54 | F-CLASS-NEW-FACT-UNCLASSIFIED | per-cycle, on Intake INCREMENTAL fact consumption manifest | `F-CLASS-NEW-FACT-UNCLASSIFIED` | M13 audited (MEDIUM admin-risk) |
| PRE-55 | F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED | per-grant SP0 sign-out, on grant_overrides block read | `F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED` | M13 audited (HIGH admin-risk) |
| PRE-56 | F-CLASS-ROUTING-INDETERMINATE | per-call, before routing decision | `F-CLASS-ROUTING-INDETERMINATE` | M13 audited (MEDIUM admin-risk) |
| PRE-57 | F-CLASS-SLOT-ID-NON-OPAQUE | per-call outbound boundary, before any cloud-routed prompt is sent | `F-CLASS-SLOT-ID-NON-OPAQUE` | **NO M13** — structural per §1 |
| PRE-58 | F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID | router.yaml derivation, before applying SN-LLC template update | `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` | key-rotation only via `tilth router-template rotate-signing-key` (audited) |

### §4.2 POST-gate row additions (F-CLASS-* family)

| Order | Check ID | Fires at | Failure code | Bypass |
|---|---|---|---|---|
| POST-23 | F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL | per-call outbound boundary, on cloud-routed payload bytes (request OR response) | `F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL` | M13 audited (HIGH admin-risk; pipeline halts) |
| POST-24 | F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED | per-call outbound boundary, on cloud-routed response payload | `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` | M13 audited (HIGH admin-risk) |
| POST-25 | F-CLASS-HIGH-STAKES-FLAG-LEAK | per-call outbound boundary, on cloud-routed payload | `F-CLASS-HIGH-STAKES-FLAG-LEAK` | M13 audited (HIGH admin-risk) |

### §4.3 Architectural-primitive realization notes

**§4.3.1 Sub-code collapse rationale (f_class_register.py).** Four PRE gates (MISSING, UNSIGNED, SIGNATURE-INVALID, HASH-MISMATCH) all consume the classification register and the same Protocol injection surface (`FileExistsCallable` + `SignatureVerifyCallable` + `HashBytesCallable`). Each is a distinct check function with its own `F_CLASS_REGISTER_*` constant; failures route to the appropriate sub-code. The dispatch order in production is MISSING → UNSIGNED → HASH-MISMATCH → SIGNATURE-INVALID; an earlier failure short-circuits the chain (no point verifying a hash on a register that's not signed). The HASH-MISMATCH check trims the recomputed SHA3-512 hex digest to a 16-char lowercase prefix to match the §3.7 schema's `sha3_512[:16]` convention; comparison is case-insensitive.

**§4.3.2 Sub-code collapse rationale (f_class_outbound_boundary.py).** Four PRE/POST gates at the cloud-routing boundary share a common payload-scanner shape — input is a string payload (prompt or response) plus a small data-class registry (`ClassifiedValue` for confidential literals; `SlotPosition` for opaque-slot anchors; high-stakes flag values direct). Consolidation halves the module count vs. one-per-code while preserving per-code dispatch via the `F_CLASS_*` constants and dedicated check functions.

**§4.3.3 F-CLASS-COVERAGE-INCOMPLETE META gate** is the load-bearing primitive that prevents Beta-shipping without realized F-CLASS-* enforcement. Implementation: the gate consumes a `Sequence[CoverageEntry]` (one per required code) plus an injected `FileExistsCallable`; it verifies (a) every code in `REQUIRED_F_CLASS_CODES` has an entry, (b) the entry's `module_path` exists on disk, (c) the entry's `test_path` exists on disk. The orchestrator constructs the entry sequence from a registry; the gate never reads the filesystem directly per AST-lint R3. The test suite includes a self-coverage test (`test_full_coverage_passes_with_real_paths`) that asserts the eleven other live module+test files satisfy the META gate when invoked against `os.path.exists`. Exclusion: the gate excludes itself (it's the auditor, not the auditee) — `REQUIRED_F_CLASS_CODES` enumerates twelve non-COVERAGE codes (eleven baseline per v7.0.7 §5.1 + F-CLASS-HIGH-STAKES-FLAG-LEAK twelfth primitive added at Audit #2 narrow-fix per §4.1).

**§4.3.4 Identity-strict signature verification.** All four signature-verifying gates (`F-CLASS-REGISTER-SIGNATURE-INVALID`, `F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED`, `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID`) apply `verified is True` identity-strict checks against the verifier's return value. A truthy non-True return (e.g., `1`, `"yes"`, the integer `42`) fail-closes — a verifier returning anything other than the singleton `True` is treated as failure per the §4 v2.2 F-AMDT-05 / F-AMDT-10 / F-AMDT-11 precedent. Verifier exceptions also fail-close with the exception class name surfaced in the result detail.

**§4.3.5 No structural sovereignty bypass on opaque-slot discipline.** F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate carries no M13 bypass — the regex `\[SLOT_(\d+)\]` defines the structural-sovereignty contract per §1. Any non-numeric slot identifier (e.g., `[SLOT_ANNUAL_REVENUE]`, `[SLOT_001A]`, `[SLOT_]`) fail-closes regardless of operator override. The opaque-ID requirement eliminates the (a) plausible-literal-hallucination + (b) field-name inference leak surfaces that motivated the rev3 narrow-fix at v7.0.7 Audit #2.

**§4.3.6 Defense-in-depth disposition under v7.0.10 LOCK (2026-05-11).** Architecture v7.0.10 LOCKED 2026-05-11 (row 215) deprecates the v7.0.7 §1 "Sanitized" / opaque-slot-token customer-facing posture entirely. The three remaining postures (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign) do not emit `[SLOT_*]` tokens into cloud-routed prompts under any normal-path code path. The two gates that policed the opaque-slot discipline at v7.0.7 are **repurposed as defense-in-depth gates** at v7.0.10:

1. **F-CLASS-SLOT-ID-NON-OPAQUE.** No legitimate trigger path under any v7.0.10 posture (no posture emits slot tokens into cloud routing). Firing = bug, regression, or attempted prompt-injection-via-slot-token-shape. Regex broadened at LOCK from `\[SLOT_(\d+)\]` (numeric-only fail-closed) to `\[SLOT_[^\]]*\]` (any slot-shaped pattern fail-closed — numeric, alphabetic, mixed, empty suffix all match). HARD_BLOCK / no M13 bypass retained.
2. **F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED.** No legitimate trigger path. Firing = bug, regression, or attack. POST-call outbound-boundary scan extended to fail-closed on any `\[SLOT_[^\]]*\]` pattern at any registered anchor or unregistered position. P0 / M13 audited disposition retained.

Both gates remain in the F-CLASS-* family roster (no retirement). The F-CLASS-* family roster after v7.0.10 LOCK: **sixteen primitives total** — ten legitimate-runtime from v7.0.7 §5.1 (rows 1–7, 10–12 in the §4 table) + two defense-in-depth (rows 8–9) + four new at v7.0.10 (§4.4 below). The runtime cost is negligible (regex scan on cloud-routed prompts is cheap). Slot-fill agent module + surrounding gates remain in the runtime tree as defense-in-depth; normal-operation invocation count under any v7.0.10 posture is zero.

**§4.3.7 Posture-signature sub-tag extensions (v7.0.10 §1.4 Classification Review UX flip).** v7.0.10 amends Classification Review step 3 + step 4 to add a deployment-level `selected_posture: Literal["frontier_eligible", "split_context_hybrid", "local_only_sovereign"]` field at the top of the operator-signed register. The four F-CLASS-REGISTER-* gates (rows 1–4 of §4 table) carry sub-tag extensions to verify the posture-signature trail as part of the existing register-signature chain — **no new top-level F-CLASS-* gate added** at this layer per v7.0.10 §1.4. Specifically:

- `F-CLASS-REGISTER-UNSIGNED` sub-tag `.posture_unsigned` — fires when the register's top-level `selected_posture` field is missing OR the operator signature does not cover the field.
- `F-CLASS-REGISTER-SIGNATURE-INVALID` sub-tag `.posture_invalid` — fires when the signature verifies against the field-classifications block but not the extended block including `selected_posture`.
- `F-CLASS-REGISTER-HASH-MISMATCH` sub-tag `.posture_hash_mismatch` — fires when the recomputed hash chain over the extended block (including `selected_posture`) does not match the on-register hash.

The sub-tag-extension realization (predicate signature + three named drift-test bindings + AST-lint enforcement) is bound to this §4 v2.x amendment companion update at v7.0.10 LOCK ceremony — see §4.4 + the §0.5 v22 paired-commit. AST-lint rule `R-CLASS-POSTURE-FIELD-COVERAGE` (registered in DEFAULT_RULES) confirms every register-signature gate inspects the posture field. The sub-tag-extension precedent matches §4 v2.x.1 row 198 (R-ARCHIVIST-NO-CANONICAL-MUTATE enumeration extension under the existing F-ARCHIVIST-AUTO-APPLY-ATTEMPTED owner) — no new top-level row, named drift-test bindings under existing-row ownership.

### §4.4 v7.0.10 new gate row additions (F-CLASS-* family — 4 new primitives)

| Code | Tier | Module | Severity | Authority |
|---|---|---|---|---|
| `F-CLASS-POSTURE-MID-CYCLE-CHANGE` | PRE per-cycle | `f_class_posture_mid_cycle_change.py` (LANDS at v0.2 first-wave realization; signature-stub at v7.0.10 LOCK ceremony) | HIGH (M13 audited; rare-fire boundary) | v7.0.10 §5.3 (closes Cycle 1 RT-4) |
| `F-CLASS-SPLIT-CONTEXT-ALLOWLIST` | PRE per-call outbound | `f_class_split_context_allowlist.py` (LANDS at v0.2 first-wave realization; signature-stub at v7.0.10 LOCK ceremony) | HARD_BLOCK (no M13 — closed-set check structural per §1.3 boundary rule) | v7.0.10 §5.3 |
| `F-CLASS-SPLIT-CONTEXT-LEAK` | PRE per-call outbound | `f_class_split_context_leak.py` (LANDS at v0.2 first-wave realization; signature-stub at v7.0.10 LOCK ceremony) | HIGH (M13 audited; admin-risk HIGH; closes Cycle 1 RT-2) | v7.0.10 §5.3 |
| `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` | PRE per-swap | `f_class_heavy_judge_cloud_download.py` (LANDS at v0.2 first-wave realization; signature-stub at v7.0.10 LOCK ceremony) | HARD_BLOCK (structural — alternative-update-channel ban; closes Cycle 1 RT-10 + Cycle 2 RT-10-PARTIAL) | v7.0.10 §5.3 + §3 retentions |

**Realization discipline.** v7.0.10 names the four primitives at the architectural-primitive layer; predicate bodies land at a follow-on §4 v2.x.y amendment with the v0.2 first-wave Code phase per the dormant-binding pattern + L-006 + the v7.0.7 §5.1 precedent (predicate signatures + named drift-test bindings at LOCK ceremony; bodies realized at runtime amendment). The F-CLASS-COVERAGE-INCOMPLETE META gate scope expands at v7.0.10 to the sixteen-primitive set (the ten legitimate-runtime gates + two defense-in-depth gates + four new gates); absence of any required module or test from the runtime tree fail-closes the cycle. Coverage gate's `REQUIRED_F_CLASS_CODES` constant updates at the same follow-on amendment.

**§4.4.1 F-CLASS-POSTURE-MID-CYCLE-CHANGE — implementation note.** Posture is the deployment-level decision (operator-signed at white-glove Classification Review step 3 + Ed25519-signed step 4 sign-off). The posture flag is atomically locked at `cycle_started_at_utc` for the duration of each cycle via the §2 Vault topology's signed-commit `start_editing_transaction` / `commit_editing_transaction` primitives (LIVE per §2 Vault v7.1 interface registry row 35). Mid-cycle reads of the posture return the locked value regardless of any concurrent posture-change attestation. The new Vault schema field `posture_lock_version: int` ships at LOCK ceremony with the §2 Vault topology companion edit (sub-tag extension on the existing §2 row, not a new top-level row per Cycle 2 RT-C2-2 closure). All readers consult the locked version; the integration test `tests/orchestrator/test_v7_0_10_posture_concurrent_change_fails_closed.py` confirms fail-closed behavior under concurrent posture-change attempts within a cycle. The gate fires inclusive-on-both-ends per Cycle 1 RT-4 closure: any posture-change timestamp `t` where `cycle_started_at_utc ≤ t ≤ cycle_ended_at_utc` fail-closes; posture changes take effect at the *next* cycle's `cycle_started_at_utc`.

**§4.4.2 F-CLASS-SPLIT-CONTEXT-ALLOWLIST — closed-set check.** Under Split-Context Hybrid posture, a cloud-routed prompt's payload contains a field-path NOT in the operator-signed Split-Context-Hybrid allow-list at `orgs/<slug>/vault/classification/split_context_allowlist.yaml`. Closed-set check, not open-set classification check. Allow-list is operator-signed Ed25519 at white-glove + per-grant SP0 extensible; any *extension* post-white-glove requires **dual-sign discipline** (operator Ed25519 + second-tier signature; in v0.1 single-operator deployments the SN-LLC publisher signature on the extension diff acts as second-tier per the same router-template trust mechanism). Allow-list extensions also run through an automated normalization-and-applicant-fact-scan pass at write time (Unicode NFC + base64 decode + URL-decode + whitespace concatenation reverse pass) before the second signature can be applied per Cycle 2 RT-C2-1 closure.

**§4.4.3 F-CLASS-SPLIT-CONTEXT-LEAK — pre-cloud-route applicant-fact scan.** Under Split-Context Hybrid posture, before routing under the closed-set allow-list, the routing layer runs a deterministic scan on the prompt payload for: applicant's legal name + EIN + address strings + applicant-supplied production-metric numerics from KFR + applicant-supplied partnership names from `PROJECT_CONTEXT.partnerships`. Any match → fail-closed with admin-risk ledger entry HIGH severity; operator review required. Catches attackers who push applicant-fact text *into* a Public + Shareable field (e.g., embedding the applicant's EIN in the RFA-keywords section). Closes Cycle 1 RT-2.

**§4.4.4 F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD — pre-loaded-model-binary discipline.** The 200B-class heavy-Judge model binary MUST be **pre-loaded on the Golden Quill at white-glove onboarding** (operator-signed Golden Image build pin). The swap operation is a local-execution-pointer-switch only — no network fetch, no remote download, no cloud-routed binary transfer, **no background-sync service**. The gate fires on any heavy-Judge swap attempt that would trigger a network fetch (model binary missing from local path; hash mismatch with Golden-Image-signed manifest; operator override attempt to fetch from a remote URL; *or any background model-sync daemon attempting to update the binary outside the operator-attested router-template update flow*). Alternative-update-channel ban: any model-sync service, background daemon, or external update channel that would mutate the heavy-Judge binary outside the operator-attested router-template update flow is structurally absent from v0.1 Beta deployments. Closes Cycle 1 RT-10 + Cycle 2 RT-10-PARTIAL.

## §5. HORIZON rows — v0.2+ support agents (forward registration)

Per the WS-L dispatch packet, the following gate families are HORIZON-only at this v2.x — full Cedar/predicate work defers to the corresponding §13 / §14 / §15 LOCK rounds. Rows registered here so future amendments know what to expect.

### §5.1 Data Collector family (per WS-I §13 v1 LOCKED 2026-05-10 rows 196/197)

> **WS-I §13 v1 LOCK 2026-05-10 (rows 196/197) — six HORIZON rows graduated to ACTIVE; two NEW gates added from Cycle 1 + Cycle 2 fold-ins. Predicate bodies realized in WS-I Code phase 2026-05-10 (this LOCK cycle's slice 1) at `pipeline/logician/gates/f_datacollector_*.py`. The data_collector seat's `REGISTERED_GATES` registry now binds canonical failure codes to the realized `check_*` callables; the prior NotImplementedError skeleton stubs are retired.**

| Code | Tier | Status | parent_lock |
|---|---|---|---|
| `F-DATACOLLECTOR-CONSENT-MISSING` | PRE-outbound + module-load + send-time | **ACTIVE-AT-§13-v1-LOCK** | row 196 |
| `F-DATACOLLECTOR-OPT-OUT-ACTIVE` | PRE-outbound | **ACTIVE-AT-§13-v1-LOCK** | row 196 |
| `F-DATACOLLECTOR-FREQUENCY-CAP-EXCEEDED` | PRE-outbound | **ACTIVE-AT-§13-v1-LOCK** | row 196 |
| `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND` | PRE-outbound + POST-inbound + PRE-write | **ACTIVE-AT-§13-v1-LOCK** | row 196 |
| `F-DATACOLLECTOR-KFR-DRIFT` | POST-inbound-write (ADVISORY) | **ACTIVE-AT-§13-v1-LOCK** | row 196 |
| `F-DATACOLLECTOR-INBOUND-CLASSIFICATION-UNSET` | PRE-storage | **ACTIVE-AT-§13-v1-LOCK** | row 196 |
| `F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER` | POST-write | **ACTIVE-AT-§13-v1-LOCK (NEW, Cycle 1 RT-28)** | row 196 |
| `F-DATACOLLECTOR-OPT-OUT-PROPAGATION-FAILED` | PRE-write | **ACTIVE-AT-§13-v1-LOCK (NEW, Cycle 2 RT-C2-02)** | row 196 |

**Activation note.** The six rows previously listed as HORIZON graduate to ACTIVE at §13 v1 LOCK 2026-05-10. The two NEW rows (BENEFICIARY-CONSENT-TIER + OPT-OUT-PROPAGATION-FAILED) are added at the same LOCK per Cycle 1 RT-28 closure + Cycle 2 RT-C2-02 closure dispositions (per §13.16.2 + §13.16.6.2). All eight predicates are deterministic Python (zero LLM token cost); the consolidated PRE-outbound check callable `data_collector.pre_gate.compose_send_validation.v1` sequences the four PRE-outbound gates per §4 v2.2 consolidated-check pattern + §13.9.0.

Compliance basis: TCPA / CAN-SPAM / per-state-rules (PA / CA / FL / TX / NY at v0.2 first wave per dispatch plan §8f default). v0.2 first-wave channels: email + SMS + voice + Telegram + WhatsApp.

### §5.2 Report Generator family (per WS-J §14 — not yet LOCKED)

| Code | Tier (anticipated) | Status |
|---|---|---|
| `F-REPORT-COMMITMENT-UNTRACED` | POST | HORIZON — §14 LOCK |
| `F-REPORT-COMMITMENT-MISSED` | POST | HORIZON — §14 LOCK |
| `F-REPORT-OUT-OF-SCOPE-DRIFT` | POST | HORIZON — §14 LOCK |
| `F-REPORT-NUMERIC-DRIFT` | POST | HORIZON — §14 LOCK (composes with KFR family per v7.0.4) |
| `F-REPORT-TEMPLATE-MISMATCH` | POST | HORIZON — §14 LOCK |

Composition note: F-REPORT-COMMITMENT-* gates consume `proposal_commitments.yaml` populated by Intake AWARD_INGEST mode (per v7.0.4 §5.3); the substrate ships at v7.0.4 LOCK 2026-05-09 row 178.

### §5.3 Archivist family (per WS-K §15 — SPEC-LOCKED 2026-05-10 row 191; v1.x implementation deferred)

> **Cycle 1 closure E-07 update (2026-05-10):** §15 Archivist v1 SPEC-LOCKED 2026-05-10 row 191 with FULL live cross-family rigor. Five owned Logician gate codes registered (the four below plus `F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT` NEW per Cycle 2 RT-11 closure of the §15 round). v0.2 ships SPEC-only; v1.x implementation deferred. Operator-driven cadence in v0.2 interim.

| Code | Tier (anticipated) | Status |
|---|---|---|
| `F-ARCHIVIST-CROSS-ORG-LEAK` | PRE-curation | SPEC-LOCKED row 191 — §15 v1 owned predicate; implementation v1.x |
| `F-ARCHIVIST-LESSON-INSTANCE-LEAK` | PRE-curation | SPEC-LOCKED row 191 — §15 v1 owned predicate; implementation v1.x |
| `F-ARCHIVIST-AUTO-APPLY-ATTEMPTED` | PRE-write | SPEC-LOCKED row 191 — three-layer defense (AST-lint + runtime guard + Cedar policy); proposes-only invariant; implementation v1.x |
| `F-ARCHIVIST-CADENCE-DRIFT` | POST-cycle | SPEC-LOCKED row 191 — informational at v0.2; HIGH+FAIL_CLOSED at v1.x; implementation v1.x |
| `F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT` (NEW per RT-11) | PRE-substrate-read | SPEC-LOCKED row 191 — three-layer enforcement; implementation v1.x |

Per WS-K dispatch directive: spec-only at v0.2; v1.x implementation deferred. Archivist proposes, never auto-applies; operator confirms every change. Realization of the five gate predicates lands at the v1.x Archivist amendment, not in this v2.x.

## §6. Cross-family composition notes

### §6.1 Funder Intel + KFR orthogonality

Per v7.0.5 §0.1 Register Summary + companion `section_04_v7_0_5_companion.md` Composition section. KFR (per-org factual) and Funder Intel (per-funder factual) operate on orthogonal substrates:

- KFR family validates per-org factual claims about THIS client at SP0 + draft-time.
- Funder Intel family validates per-funder corpus integrity AND per-org Scout reasoning trail isolation.

Both fire as POST-gates after Scribe; both fire as PRE-gates before Scout / Scribe / Editor / Judge / Red Team reads. The two families do not share modules — no F-LOGICIAN-FACT-* code references a Funder Intel doc, and no F-MATCH-DB-* / F-FUNDER-CORPUS-* code references a KFR fact.

### §6.2 Funder Intel + Classification routing composition

When Slice 3 lands the F-CLASS-* family:

- Match DB `narrative_summary_classification` per-entry (per v7.0.5 §2 schema) interacts with classification-aware split-context routing per v7.0.7 §1.
- F-MATCH-DB-CONSENT-TIER-VIOLATION + F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL co-enforce that Confidential narrative content stays local-routed regardless of consent tier.
- F-FUNDER-CORPUS-INTEGRITY runs at every load regardless of routing posture; the integrity invariant is orthogonal to classification.

### §6.2.1 F-CLASS register integrity composes orthogonally to KFR + Funder Intel

The classification register lives at `vault_shared/classification/register.yaml` (cross-org defaults + class definitions) plus `orgs/<slug>/vault/classification/register.yaml` (per-client overrides + grant-level overrides). The F-CLASS-REGISTER-* family checks register integrity (existence + signature + hash); it does NOT consume KFR fact rows or Funder Intel corpus bytes. Conversely, KFR + Funder Intel gates do not consume classification register rows. The substrates intersect at routing decisions but the gate predicates remain orthogonal.

### §6.2.2 Slice 4 (v7.0.4-M1 corrective) composition (Cycle 1 closure E-05, 2026-05-10)

Slice 4 introduces five distinct mechanism families that compose orthogonally with the existing slices:

- **Canonicalization stack (KFR canonical-signature, YAML SafeLoader, duplicate-key, tag-mutation, path-symlink, legacy-migration).** All eight Slice-4 KFR-family gates compose with the Slice 2 KFR family at the I/O wrapper layer — `f_kfr_canonical_signature_invalid.py` supersedes `f_kfr_signature_invalid.py` (Slice 2 PRE-43 → Slice 4 PRE-60); the combined `f_kfr_signature_validation.py` module continues to serve `F-KFR-AUDIT-CHAIN-BROKEN` per Slice 2 PRE-44. Both Slice 2 and Slice 4 read paths must canonicalize via `kfr_canonical.py` BEFORE signature verification per M1 §2.2.1; this is the source-of-truth byte stream that all downstream signature-verifying gates consume.
- **AST whitelist (derivation safety).** `F-DERIVATION-AST-FORBIDDEN-NODE` (PRE-65) + `F-DERIVATION-RUNTIME-ARITHMETIC-ERROR` (POST-26) sit between the Scribe-output rendering layer and the Logician deterministic-Python evaluation step. They do not compose with the F-CLASS-* family — derivation eval is local-only by architectural premise (no cloud-routed seat ever computes a fact derivation).
- **Currency Decimal arithmetic.** `F_CURRENCY_*` gates (PRE-69 through PRE-73) enforce the Decimal mandate at every currency comparison. The KFR canonical-JSON serializer in `kfr_canonical.py` REFUSES `float` at canonicalization time (raises `CanonicalizationError` mapped to `F-CURRENCY-FLOAT-IN-COMPARISON` per the gate's docstring) — Slice 4 currency gates and Slice 2 KFR gates share this fail-closed boundary at the canonicalizer level.
- **Benchmark seeding allowlist.** Slice 4 hardens the seeding pipeline with Ed25519 signature verification on canonical-JSON bytes (PRE-67/PRE-68). Composes with Slice 2 `F-BENCHMARK-CONTAINS-PER-ORG-REF` (PRE-47/PRE-48) — the seeding-allowlist load happens BEFORE the per-org-ref check fires; per-org content cannot enter the seeding flow either through (a) the allowlist itself (RT-10 closure: strict-key whitelist `_ALLOWED_ALLOWLIST_KEYS` admits only seven schema keys + signature pair), or (b) the seeded benchmark probe data (Slice 2 gate fires at write AND read).
- **Logfire bootstrap.** Slice 4's `F-INTAKE-TELEMETRY-LEAK` + `F-INTAKE-LOGFIRE-STUB-MISSING` (PRE-75/PRE-76) enforce Sovereignty-Promise discipline at process start. Composes orthogonally with every other gate family — Logfire export is forbidden across the entire pipeline tree, not just Intake.

Cross-slice signature-verification discipline (RT-04 + DC-02 + Cycle 1 fold-in): all five signature-verifying gates across Slices 1–4 — `F-CLASS-REGISTER-SIGNATURE-INVALID` (Slice 3), `F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED` (Slice 3), `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` (Slice 3), `F-KFR-CANONICAL-SIGNATURE-INVALID` (Slice 4), `F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID` (Slice 4) — apply `verified is True` identity-strict checks per the §4 v2.2 F-AMDT-05 / F-AMDT-10 / F-AMDT-11 precedent. A truthy non-True return fail-closes; verifier exceptions also fail-close with the exception class name surfaced. This discipline is canonical across the amendment (re-stated here for cross-slice reading-surface clarity per Judge DC-02 process recommendation).

### §6.3 CIC × CLC orthogonality preservation

Per v7.0.8 LOCKED 2026-05-08 row 175 + CLAUDE.md F-CIC-CLC-COUPLING-VIOLATION discipline: this amendment does NOT introduce any CIC→CLC coupling at the gate layer. Funder Intel gates query funder docs by funder type (federal_agency / private_foundation / etc.) which is independent of customer archetype (food-systems / educator / public-agency / arts-culture / cooperative / ecosystem-intermediary). Match DB entries do not declare a CIC-implied CLC subset. No gate's predicate consumes a CIC value to constrain a CLC value or vice versa.

## §7. F-AMDT-* structural enforcement extension

Per v2.2 consolidated amendment §10 + §11. This amendment's LOCK ceremony will append rows to:

- `pipeline/engineering/lock_history.v1.jsonl` — one row per Slice + one final row at Cowork Thesis LOCK.
- Daily log (per F-AMDT-12) — one canonical `## LOCK: pipeline.blueprint.v0_1.section_04_v2_x_amendment` block per Slice + one at Thesis LOCK.

F-AMDT-12 (`F-DAILY-LOG-LOCK-BLOCK-MISSING`, POST-gate per v2.2 wave 2) fires on every `lock_history.v1.jsonl` append. The bulk add at Slice 3 close (when ~25 new gates' module + test + spec-card SHAs land in one ceremony) tests F-AMDT-12's tolerance for multi-row appends — each module's LOCK row needs its own daily-log block per the gate's discipline.

F-AMDT-07 (`F-AMENDMENT-SELF-REFERENCE-DETECT`) does NOT fire on this amendment because it does not modify the council. Slice 3's F-CLASS-* gates change classification routing but not council seat assignments.

## §8. Test coverage discipline (L-002 pattern)

Per v2.2 consolidated amendment §12 ~928 tests in `tests/logician/gates/`. This amendment adds:

- **Slice 1 (landed):** 68 new tests across 7 Funder Intel modules (10 + 11 + 11 + 6 + 10 + 10 + 8 = 66 listed; 68 actual including the 2 sanity checks).
- **Slice 2 (landed):** 98 new tests across 6 KFR sub-code modules. F-EXTRACTOR-FABRICATION test coverage includes every allowable + rejected normalization mode per v7.0.4 §5.2 (Unicode NFC, whitespace normalization, OCR-substitution rejection, page-off-by-one rejection in BULK/INCREMENTAL + acceptance with operator-flag in AWARD_INGEST, ellipsis-substring rejection).
- **Slice 3 (landed):** 108 new tests across 7 F-CLASS-* modules (12 sub-codes consolidated). F-CLASS-COVERAGE-INCOMPLETE's enforcement test is meta — verifies every v7.0.7 §5.1 code has a live module + test.
- **Slice 4 (landed):** 199 new tests across 16 gate test files + 5 supporting-module test files (107 gate tests + 92 supporting tests). Includes RT-12 Unicode-confusable digit rejection test in `test_f_class_outbound_boundary.py` and RT-10 strict-key allowlist tests in `test_f_benchmark_seeding_allowlist_signature_invalid.py` (Cycle 1 closures).
- **Cycle 1 closures (added 2026-05-10 — Cycle 1 fold-in for E-03 + DC-01 + RT-04 + RT-05 + RT-12 + RT-10):** 24 new tests across 3 currency-context gate test files (`test_f_currency_context_omitted.py` 6 tests + `test_f_currency_context_mismatch.py` 7 tests + `test_f_currency_decimal_context_drift.py` 6 tests = 19 tests) + 3 RT-12 Unicode-digit tests + 2 RT-10 extra-key tests = 24 new tests at Cycle 1 fix-fold time.

**Total at Cowork Thesis LOCK: 497 new tests** in `tests/logician/gates/` and the supporting-module test directories (`tests/logician/canonicalization/`, `tests/logician/derivation/`, `tests/logician/currency/`, `tests/logician/benchmarks/`) attributable to WS-L. 68 + 98 + 108 + 199 + 24 = 497.

Wrapper-test exemption (§16.7 disposition CLOSED at Cycle 1 — operator-confirmable Path B): the three currency-context gate wrappers now have dedicated test files. The §8 discipline is uniform — every gate has a dedicated test file at the gate path (or a documented forwarding pattern with explicit cross-reference, none in scope here). Future wrappers that delegate to a tested helper still author per-gate tests covering: (a) success-path return shape; (b) every failure-leg dataclass-field population; (c) frozen-instance immutability assertion; (d) failure-code constant export alignment.

## §9. §0.5 Interface Index paired-commit rows

Per §0.5 paired-commit discipline + F-INDEX-STALE PRE-gate. This amendment's row set is large; final paired-commit happens at Cowork Thesis LOCK. Slice 1 row inventory:

- 7 failure-code rows (Funder Intel)
- 3 pre-gate-check rows (PRE-36 / PRE-37 / PRE-38 + PRE-39 = 4 PRE rows total since PRE-39 fires twice)
- 3 post-gate-check rows (POST-20 / POST-21 / POST-22)
- 1 amendment marker row (`blueprint.section_04_v2_x_amendment`)

Slice 2 + Slice 3 rows append to this set. Per L-014 faithfulness-consolidation pattern, the §0.5 amendment that pairs with this §4 v2.x LOCK is itself a faithful consolidation of three Code-slice row sets — not a new semantic surface.

## §10. Slice 1 + Slice 2 + Slice 3 LOCK criteria (interim)

This filing is a DRAFT, not a LOCK. Interim Code-phase milestone status:

**Slice 1 (Funder Intel — landed 2026-05-10):**

1. ✅ All 7 Funder Intel gate modules on disk + tested + green.
2. ✅ `pipeline/logician/gates/__init__.py` wires all 7 Funder Intel + 11 Uploader gates.
3. ✅ 68 new gate tests pass; broader logician/ test suite green at 1891 (up from 1253 baseline; +638 = 68 new + 570 from broader scope now properly wired).
4. ⏳ AST-lint R1-R7 verification pending Slice 3 close (Slice 2 close additionally verified — see Slice 2 row 4).
5. ⏳ Daily-log Slice 1 entry written.
6. ⏳ Memory file Slice 1 progress note written.
7. ⏳ Session metrics row written.
8. ✅ Handoff prompt for Slice 2 written + filed at `pipeline/handoffs/ws_l_slice_2_kfr_residuals_2026-05-10.md`.

**Slice 2 (KFR residuals — landed 2026-05-10):**

1. ✅ All 6 new KFR-family residual gate modules on disk + tested + green (one combined module covers F-KFR-SIGNATURE-INVALID + F-KFR-AUDIT-CHAIN-BROKEN per §3 table).
2. ✅ `pipeline/logician/gates/__init__.py` wires all 6 new modules + their dataclasses + check functions onto the package surface.
3. ✅ 98 new gate tests pass (25 + 9 + 19 + 18 + 13 + 14); broader logician/ test suite green at 1989 (1891 → 1989 = +98 from Slice 2; logician/gates/ subset at 1419 green).
4. ✅ AST-lint clean: `scripts/run_lint.sh pipeline/logician/` exit=0 — no LOGICIAN_IMPORT_BAN / LOGICIAN_OPEN_BAN / SCOUT_NO_EVAL violations across the new modules.
5. ⏳ Daily-log Slice 2 entry written (this session's close — see §13).
6. ⏳ Memory file Slice 2 progress note written.
7. ⏳ Session metrics row written (this session's close).
8. ⏳ Handoff prompt for Slice 3 written + filed at `pipeline/handoffs/ws_l_slice_3_class_dormant_2026-05-10.md`.

**Slice 3 (F-CLASS-* dormant primitives — landed 2026-05-10):**

1. ✅ All 7 F-CLASS-* gate modules on disk + tested + green (12 sub-codes consolidated per the v2.2 F-AMDT-08/09/10/11 sub-code-collapse precedent).
2. ✅ `pipeline/logician/gates/__init__.py` wires all 7 new modules + their dataclasses + check functions onto the package surface (~50 new symbols added).
3. ✅ 108 new gate tests pass (27 + 32 + 12 + 9 + 10 + 10 + 9 + 9 — see §15 audit trail for per-file SHAs); broader logician/ test suite green at 2097 (1989 → 2097 = +108 from Slice 3); `tests/logician/gates/` subset at 1527 (1419 → 1527 = +108).
4. ✅ AST-lint clean: `scripts/run_lint.sh pipeline/logician/` exit=0 — no LOGICIAN_IMPORT_BAN / LOGICIAN_OPEN_BAN / SCOUT_NO_EVAL violations across the new modules.
5. ⏳ Daily-log Slice 3 entry written (this session's close — see §15).
6. ⏳ Memory file Slice 3 progress note written.
7. ⏳ Session metrics row written (this session's close).
8. ⏳ Hand-back to dispatch coordinator: Cowork Thesis dispatch fires next.

Cowork Thesis LOCK criteria fire next as a separate dispatch session; all three Code slices have CLOSED and met their interim criteria.

## §11. Hand-back to dispatch coordinator at Slice 3 close

This session lands Slice 3 — the final Code-phase session per L-012. The Code phase is now CLOSED across all three slices; Cowork Thesis dispatch is the next session per the WS-L dispatch packet directive: "When Code phase complete, hand back to dispatch coordinator — Cowork Thesis phase fires as a separate dispatch."

**Coordination notes at Slice 3 close:**

- **WS-L Slice 4 (v7.0.4-M1 corrective predicates) is concurrent.** Per `pipeline/handoffs/ws_l_slice_4_m1_corrective_2026-05-10.md`, Slice 4 authors 19 M1 gate codes in a different namespace; parallel-safe in a different worktree. `__init__.py` merge needs both updates folded — Slice 3 lands first and Slice 4 builds on top.
- **WS-K §15 Archivist (spec-only, Cowork) is concurrent.** Different surface entirely; no merge conflict expected.
- **Cowork Thesis dispatch fires next.** L-005 two-audit cycle, cross-family per WS-B (Editor=`groq/llama-3.3-70b-versatile` + Judge=`google/gemini-2.5-pro` + Red Team=`groq/openai/gpt-oss-120b`). Use `osascript` → `openclaw` bridge with templates from `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`.

## §12. What this amendment does not do

- Does not modify §4 v2.1 base text (parent-LOCK stable at hash `e0507e6daaa18676`).
- Does not modify §4 v2.2 consolidated amendment (parent for F-AMDT-* gate registry).
- Does not re-author the v2.7 Uploader amendment text — that's a separate WS-F authorship round; this amendment registers the v2.7 gates in the package surface.
- Does not LOCK the F-CLASS-COVERAGE-INCOMPLETE binding declared at v7.0.7 §5.1 — that LOCKs at Slice 3 close + this amendment's Cowork Thesis LOCK ceremony.
- Does not author the Cedar policy files for new gates (Cedar policy authorship lives in `pipeline/vault/policies/` per existing pattern; the Python predicates here are the structural floor).
- Does not specify Data Collector / Report Generator / Archivist gate predicates (HORIZON rows only; full work at §13 / §14 / §15 LOCK rounds).

## §13. Slice 1 close — author response log + audit trail

**Slice 1 dispatched 2026-05-10** as Code session against the WS-L packet at `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §WS-L. Author: Cowork Opus 4.7 (this session).

**Decisions surfaced + executed:**

1. Scope-honest per L-012: the WS-L dispatch enumerates ~25 new gate modules + the amendment doc + tests + AST-lint discipline. One session cannot land that volume at v2.2 quality. Slice plan: Funder Intel (Slice 1) + KFR residuals (Slice 2) + F-CLASS-* dormant primitives (Slice 3). Cowork Thesis fires once all three Code slices land.
2. CIC × CLC gate modules use a different export convention (`GATE_ID` + `run()` rather than `F_*` + `check_*`) and are outside WS-L scope; not wired into `__init__.py` here.
3. F-FUNDER-CORPUS-INTEGRITY default `hashlib.sha3_512` import is lazy (inside `_hashlib_sha3_512` helper) to keep module-load surface free of crypto-library imports per the §4 v2.2 _protocols.py spirit.
4. F-CHANNEL-G-CROSS-ORG-LEAK decode-rescan cascade implementation: best-effort base64 + hex + URL decoders run on every whitespace-separated token of length ≥8; decoded payloads concatenate into the regex-scan target. Zero false positives in the 11-test suite.

**Audit trail at Slice 1 close:**

- This amendment file: DRAFT.
- Module SHAs: pending — to be captured in Slice 1 daily-log entry.
- Test pass count: 68 new (Funder Intel) + 1891 logician/ total (1253 baseline → 1891 = +638).
- Pre-existing pytest hang at ~96% on full suite is a non-WS-L concern; flagged for separate triage.

**Slice 2 handoff** (forward dispatch): see daily log entry 2026-05-10 — handoff prompt filed at `pipeline/handoffs/ws_l_slice_2_kfr_residuals_2026-05-10.md` (to be authored at Slice 1 close).

## §14. Slice 2 close — author response log + audit trail

**Slice 2 dispatched 2026-05-10** as Code session against the WS-L Slice 2 handoff at `pipeline/handoffs/ws_l_slice_2_kfr_residuals_2026-05-10.md`. Author: Cowork Opus 4.7 (this session).

**Decisions surfaced + executed:**

1. **Combined-module choice for KFR signature + audit-chain.** F-KFR-SIGNATURE-INVALID and F-KFR-AUDIT-CHAIN-BROKEN both consume the same Protocol injection surface (`SignatureVerifyCallable` + `KeyringEntry` sequences) and fire on the same event (KFR entry read). Per the v2.2 F-AMDT-08/09/10/11 sub-code-collapse precedent, both check functions live in `f_kfr_signature_validation.py` with two distinct `F_*` constants and two distinct check functions. Halves the module count vs. separate files; preserves per-code dispatch via the constant + check-function pair.
2. **F-EXTRACTOR-FABRICATION substrate dispatch via mode-immutable input dataclass.** `CandidateFact` carries mode + substrate as required fields, validated against `PERMITTED_MODES` / `PERMITTED_SUBSTRATES` enums at frozen-kw_only construction time. Substrate dispatch runs inside `check_extractor_fabrication` per the WS-E §11.9.1.A/B/C/D pattern (PDF unique-page-match / DOCX paragraph-index / Markdown single-line). The `operator_award_page_offset_flag` tolerance opens ±1 page ONLY when mode == AWARD_INGEST AND substrate == PDF AND flag is True — three-condition AND keeps the tolerance from leaking into BULK / INCREMENTAL paths.
3. **Ellipsis rejection runs universal pre-dispatch.** `_contains_ellipsis` checks both ASCII `...` and Unicode `…` BEFORE substrate dispatch. Rejecting ellipsis universally simplifies substrate-helper code (each helper assumes the quote contains no ellipsis already) and matches §5.2's "quote must literally span start-to-end" intent regardless of substrate.
4. **F-LOGICIAN-FACT-NEEDED-REQUIRED carries no M13 bypass** — module predicate has no operator-override branch. Per §3.2 the gate exists explicitly to prevent fabrication-by-omission; allowing M13 bypass would defeat the gate's purpose. This is the single Slice-2 gate without M13 reach; documented in §3.4 + §3.1 PRE-46 row (`Bypass: NO M13 — HARD_BLOCK`).
5. **F-BENCHMARK-CONTAINS-PER-ORG-REF probes carry only value+unit+tolerance** — no per-org identifier in the `PerOrgValueProbe` dataclass. The I/O wrapper that materializes the probe sequence is responsible for stripping fact_id / who / what / org_slug; the gate sees only canonical-value pairs. Mirrors §7.2's "no per-org KFR content is exposed cross-org by the gate" closure.
6. **Inventory pass per Step 0 of handoff:** the F-LOGICIAN-FACT-DRIFT umbrella module emits exactly one failure code; seven v7.0.4 §4 sub-codes do NOT split out at the umbrella surface (per §3.5 detailed table). Splitting them requires schema + claim-extractor + AST-walker work that exceeds Slice 2/3 capacity. Inventory result documented; sub-code split work deferred to a follow-up amendment after Cowork Thesis closes Slice 1 + 2 + 3.

**Audit trail at Slice 2 close:**

- This amendment file: DRAFT (Slice 2 increment landed; Slice 3 still pending).
- Module SHAs (sha3_512[:16]):
  - `f_extractor_fabrication.py` — `2cdfbb4fe528e322` (413 LOC)
  - `f_extractor_award_signature_invalid.py` — `03ff5f94c414c0cf` (195 LOC)
  - `f_kfr_signature_validation.py` — `5792795d6e02c83a` (328 LOC)
  - `f_logician_fact_tolerance_drift.py` — `7959a852331ae3c9` (223 LOC)
  - `f_logician_fact_needed_required.py` — `45d994b2ae4c1106` (158 LOC)
  - `f_benchmark_contains_per_org_ref.py` — `68555ed1709f1924` (228 LOC)
- Test SHAs (sha3_512[:16]):
  - `test_f_extractor_fabrication.py` — `80c31a5f76513755` (376 LOC, 25 tests)
  - `test_f_extractor_award_signature_invalid.py` — `c22d81b30357c93d` (163 LOC, 9 tests)
  - `test_f_kfr_signature_validation.py` — `06da2ff04128d576` (370 LOC, 19 tests)
  - `test_f_logician_fact_tolerance_drift.py` — `bffefb6dd27c114c` (222 LOC, 18 tests)
  - `test_f_logician_fact_needed_required.py` — `bc4bed6cd7beab59` (170 LOC, 13 tests)
  - `test_f_benchmark_contains_per_org_ref.py` — `0e61820bb7f76ac4` (215 LOC, 14 tests)
- Test pass counts: 98 new (Slice 2) + 1989 logician/ total (1891 → 1989); 1419 logician/gates/ subset green.
- AST-lint state: `scripts/run_lint.sh pipeline/logician/` exit=0 — clean.
- Pre-existing pytest hang at ~96% on full suite still flagged for separate triage; outside WS-L surface.

**Slice 3 handoff** (forward dispatch): handoff prompt filed at `pipeline/handoffs/ws_l_slice_3_class_dormant_2026-05-10.md` (authored at Slice 2 close — consumed at Slice 3 open).

## §15. Slice 3 close — author response log + audit trail

**Slice 3 dispatched 2026-05-10** as Code session against the WS-L Slice 3 handoff at `pipeline/handoffs/ws_l_slice_3_class_dormant_2026-05-10.md`. Author: Cowork Opus 4.7 (this session).

**Decisions surfaced + executed:**

1. **Module decomposition: 7 modules realize 12 sub-codes.** Per the handoff's likely-shape guidance + the v2.2 F-AMDT-08/09/10/11 sub-code-collapse precedent: `f_class_register.py` collapses the four REGISTER-* sub-codes (shared register-reader + SignatureVerifyCallable + HashBytesCallable injection surface; same per-call event); `f_class_outbound_boundary.py` collapses the four PER-CALL outbound-boundary gates (shared payload-scanner injection surface; same per-call event). The remaining five primitives are single-code modules (RoutingIndeterminate / NewFactUnclassified / PerGrantOverride / RouterTemplateSignature / CoverageIncomplete META).
2. **F-CLASS-COVERAGE-INCOMPLETE META gate excludes itself from REQUIRED_F_CLASS_CODES.** The META gate is the auditor; auditing itself is circular. The constant `REQUIRED_F_CLASS_CODES` enumerates the twelve other F-CLASS-* codes (eleven baseline + F-CLASS-HIGH-STAKES-FLAG-LEAK twelfth primitive added at Audit #2 narrow-fix per §4.1). The self-coverage test (`test_full_coverage_passes_with_real_paths`) asserts the live on-disk module + test files satisfy the META gate when invoked against `os.path.exists` — closing the L-006 dormant-binding loop with on-disk evidence.
3. **F-CLASS-SLOT-ID-NON-OPAQUE carries no M13 bypass — structural sovereignty per §1.** The regex `\[SLOT_(\d+)\]` defines the contract. Any non-numeric payload (e.g., `[SLOT_ANNUAL_REVENUE]`) fail-closes regardless of operator override. This matches §1's explicit "structural sovereignty, not policy" framing — the rule is enforced by the gate predicate, not by an operator decision.
4. **F-CLASS-REGISTER-MISSING + F-CLASS-REGISTER-UNSIGNED carry no M13 bypass.** Per §5: "Classification Review not signed → Beta deployment cannot ship. Operator-signed classification register is a hard precondition." Allowing M13 bypass on these two gates would defeat §5's hard-precondition discipline — operator must populate + sign the register at white-glove before any cycle proceeds.
5. **F-CLASS-COVERAGE-INCOMPLETE carries no M13 bypass.** Per §5.1's "no-cycle-without-coverage gate" clause — bypassing the META gate would bypass the architectural commitment binding L-006 ties this amendment's LOCK ceremony to. The gate is the architectural lever.
6. **Identity-strict signature verification across all four signature gates.** F-CLASS-REGISTER-SIGNATURE-INVALID + F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED + F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID all apply `verified is True` identity-strict checks. A truthy non-True return (1, "yes", 42) fail-closes — matches the §4 v2.2 F-AMDT-05 / F-AMDT-10 / F-AMDT-11 precedent.
7. **F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED scans for opaque-token presence at registered anchor positions.** The gate verifies that for each registered slot, the rendered token `[SLOT_<slot_id>]` is still present at its expected anchor (delimited by optional pre/post markers). When the cloud-routed seat synthesizes a literal value into the slot anchor instead of preserving the opaque token, the slot-fill bypass surfaces here. Detection is "registered slot's opaque token NOT present at anchor" — a synthesized literal is the absence of the opaque token at the registered position.
8. **F-CLASS-HIGH-STAKES-FLAG-LEAK case-insensitive token detection.** Per §4.1: any case variant of `high_stakes` / `high-stakes` / `highstakes` substring fail-closes; optional `high_stakes_flag_values` parameter covers tagged-value variants (e.g., a stringified grant_id appearing in a high-stakes-flagged context).

**Audit trail at Slice 3 close:**

- This amendment file: DRAFT (all three Code-phase slices CLOSED; awaiting Cowork Thesis LOCK).
- Module SHAs (sha3_512[:16]):
  - `f_class_register.py` — `7c7503999bd8fe78` (438 LOC)
  - `f_class_outbound_boundary.py` — `6847f697ab81264d` (407 LOC)
  - `f_class_routing_indeterminate.py` — `f18fac3c9c0439c0` (161 LOC)
  - `f_class_new_fact_unclassified.py` — `61964884356ec801` (132 LOC)
  - `f_class_per_grant_override.py` — `7d663b2e2214c6d9` (174 LOC)
  - `f_class_router_template_signature.py` — `d6981cb77346df7e` (188 LOC)
  - `f_class_coverage_incomplete.py` — `d7e821326791d12c` (202 LOC)
- Test SHAs (sha3_512[:16]):
  - `test_f_class_register.py` — `9e61f77b6145f4ba` (351 LOC, 27 tests)
  - `test_f_class_outbound_boundary.py` — `52f65e77ae84bc4d` (349 LOC, 32 tests)
  - `test_f_class_routing_indeterminate.py` — `c48b5ad309986550` (125 LOC, 12 tests)
  - `test_f_class_new_fact_unclassified.py` — `ace71140072278db` (130 LOC, 9 tests)
  - `test_f_class_per_grant_override.py` — `58bb924ee201c94a` (140 LOC, 10 tests)
  - `test_f_class_router_template_signature.py` — `12df8c7452b82763` (132 LOC, 10 tests)
  - `test_f_class_coverage_incomplete.py` — `31f5114962c47a44` (186 LOC, 9 tests) *(includes self-coverage assertion against live on-disk paths)*
- Test pass counts: 108 new (Slice 3) + 2097 logician/ total (1989 → 2097); 1527 logician/gates/ subset green.
- AST-lint state: `scripts/run_lint.sh pipeline/logician/` exit=0 — clean.
- Pre-existing pytest hang at ~96% on full suite still flagged for separate triage; outside WS-L surface.

**Hand-back to dispatch coordinator** at Slice 3 close: Slice 3 closes the WS-L Code phase as originally planned (3-slice). The v7.0.4-M1 LOCK 2026-05-10 row 190 surfaced a fourth slice — see §16.

## §16. Slice 4 close — v7.0.4-M1 corrective predicates (LANDED 2026-05-10)

**Slice 4 dispatched 2026-05-10** as Code session against `pipeline/handoffs/ws_l_slice_4_m1_corrective_2026-05-10.md`. Author: Cowork Opus 4.7 (this session via paired-Code dispatch). Parent: architecture v7.0.4-M1 LOCKED 2026-05-10 row 190 — narrow corrective amendment closing 5 HIGH/P0 + 2 RECOMMENDED + 4 OPTIONAL paths surfaced by 2026-05-10 cross-family verification.

**Slice 4 module set (per v7.0.4-M1 §11.2 — 19 new failure codes, one renaming + 18 net-new):**

| Code | Tier | Module | Severity | M1 §ref |
|---|---|---|---|---|
| `F-KFR-YAML-CONSTRUCT-FORBIDDEN` | PRE-load | `f_kfr_yaml_construct_forbidden.py` | P0 (Law 5 — anchor/merge-key/tag injection) | §2.2.2 |
| `F-KFR-CANONICAL-SIGNATURE-INVALID` | PRE-load + draft-time read | `f_kfr_canonical_signature_invalid.py` | P0 (TAMPER_EVENT) | §2.2.1 (renames F-KFR-SIGNATURE-INVALID under canonicalization regime) |
| `F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED` | PRE-load | `f_kfr_legacy_accept_re_enabled_unsigned.py` | P0 (legacy migration discipline) | §2.6 |
| `F-KFR-PATH-SYMLINK-FORBIDDEN` | PRE-load | `f_kfr_path_symlink_forbidden.py` | HIGH (atomic-read discipline) | §4.2.2 |
| `F-KFR-TAG-MODIFIED` | PRE-write | `f_kfr_tag_modified.py` | HIGH (Law 5 — required_for_funder removal tamper) | §4 |
| `F-KFR-DUPLICATE-KEY` | PRE-load | `f_kfr_duplicate_key.py` | HIGH (canonicalization integrity) | §2.2.2 |
| `F-DERIVATION-AST-FORBIDDEN-NODE` | PRE-eval | `f_derivation_ast_forbidden_node.py` | P0 (sandbox escape — ast.Index/Slice/float/dunder) | §3.2 + §3.3 |
| `F-DERIVATION-RUNTIME-ARITHMETIC-ERROR` | POST-eval | `f_derivation_runtime_arithmetic_error.py` | LOW (DC-CF-01 fold-in) | §3 |
| `F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING` | PRE-compare | `f_benchmark_cross_check_audit_missing.py` | P0 (DC-CF-04 — boolean-oracle / write-before-compare) | §5.2.2 |
| `F-BENCHMARK-SEEDING-SOURCE-UNAUTHORIZED` | PRE-seed | `f_benchmark_seeding_source_unauthorized.py` | HIGH | §5.2.3 |
| `F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID` | PRE-seed | `f_benchmark_seeding_allowlist_signature_invalid.py` | HIGH (Ed25519 on canonical-JSON) | §5.2.3 |
| `F-CURRENCY-FLOAT-IN-COMPARISON` | PRE-runtime | `f_currency_float_in_comparison.py` | P0 (DC-CF-02 — Decimal mandate) | §6.2.1 |
| `F-CURRENCY-CONTEXT-OMITTED` | PRE-runtime | `f_currency_context_omitted.py` | HIGH (RT-07 leg 1) | §6.2.1 |
| `F-CURRENCY-CONTEXT-MISMATCH` | PRE-runtime | `f_currency_context_mismatch.py` | HIGH (RT-07 leg 2 — identity check on KFR_DECIMAL_CONTEXT) | §6.2.1 |
| `F-CURRENCY-DECIMAL-CONTEXT-DRIFT` | PRE-runtime | `f_currency_decimal_context_drift.py` | HIGH (RT-07 leg 3 — global drift catch) | §6.2.1 |
| `F-CURRENCY-UNIT-MISMATCH` | PRE-compare | `f_currency_unit_mismatch.py` | LOW (CF-RT-06 fold-in) | §6.2.1 |
| `F-AWARD-INGEST-ATTN-UNVERIFIED` | PRE-AWARD_INGEST | `f_award_ingest_attn_unverified.py` | MED (CF-RT-03 attestation) | §5.3 |
| `F-INTAKE-TELEMETRY-LEAK` | PRE-bootstrap | `f_intake_telemetry_leak.py` | LOW (CF-RT-07 fold-in) | §8.4.1 |
| `F-INTAKE-LOGFIRE-STUB-MISSING` | PRE-bootstrap | `f_intake_logfire_stub_missing.py` | LOW (RT-11 closure — process-wide Logfire bootstrap shim) | §8.4.1 |

### §16.1 Supporting modules landed (Slice 4)

5 supporting modules realize the canonicalization + AST-whitelist + currency Decimal + benchmark-hash + Logfire-bootstrap mechanisms specified at v7.0.4-M1:

| Module | LOC | SHA3-512[:16] | Role |
|---|---|---|---|
| `pipeline/logician/canonicalization/kfr_canonical.py` | 245 | `bf215023694a589d` | NFC-FIRST canonicalize() pipeline per M1 §2.2.1 |
| `pipeline/logician/canonicalization/kfr_safe_loader.py` | 277 | `23dc142922379c40` | SafeLoader subclass rejecting anchors/aliases/`<<` per M1 §2.2.2 |
| `pipeline/logician/canonicalization/legacy_migration.py` | 267 | `5f3e80967e7026cb` | Dual-verification mode + `_migration_state.yaml` per M1 §2.6 |
| `pipeline/logician/derivation/ast_whitelist.py` | 400 | `fa297ad5c22bdfdc` | Explicit ast.NodeVisitor whitelist per M1 §3.2 + §3.3 |
| `pipeline/logician/currency/decimal_arithmetic.py` | 340 | `c949de9c910e6314` | KFR_DECIMAL_CONTEXT + to_currency() + tolerance_check_currency() per M1 §6.2.1 |
| `pipeline/logician/benchmarks/cross_check.py` | 217 | `6030445a1f6a98bc` | hmac.compare_digest + audit-log write-before-compare + dummy-pad + fsync per M1 §5.2.2 |
| `pipeline/logician/benchmarks/seeding_allowlist_loader.py` | 274 | `2f2d97cba95db57f` | Ed25519 signature verification on canonical-JSON bytes per M1 §5.2.3 |
| `pipeline/cli/tilth_intake.py` | 186 | `c62f334116bb9148` | LOGFIRE_ENABLED=0 + _LogfireDisabledStub injection BEFORE any import per M1 §8.4.1 |

### §16.2 Cedar policies (Slice 4 — 5 NEW)

`pipeline/vault/policies/kfr_canonical.cedar`, `derivation_ast_whitelist.cedar`, `kfr_tag_mutation.cedar`, `benchmark_seeding.cedar`, `currency_decimal.cedar` — all on disk; complement the Python predicates as defense-in-depth.

### §16.3 AST-lint rules (Slice 4 — 3 NEW)

`pipeline/linting/r_currency_no_float_compare.py`, `r_benchmark_no_short_circuit_compare.py`, `r_intake_no_logfire_import_before_env.py` — extend the AST-lint coverage to refuse the source-level patterns that motivate the corresponding Python gates. Slice 4 also retroactively closed the AST-lint cycle Slice 3 surfaced (currency-helper float-comparison sites in pre-Slice-4 modules) by adopting the new R_CURRENCY_NO_FLOAT_COMPARE rule against the broader pipeline tree.

### §16.4 PRE-gate row additions (Slice 4 family — 14 PRE)

| Order | Check ID | Fires at | Failure code | Bypass |
|---|---|---|---|---|
| PRE-59 | F-KFR-YAML-CONSTRUCT-FORBIDDEN | every KFR YAML load via SafeLoader subclass | `F-KFR-YAML-CONSTRUCT-FORBIDDEN` | M13 (HIGH admin-risk) |
| PRE-60 | F-KFR-CANONICAL-SIGNATURE-INVALID | every KFR entry read at I/O wrapper (renames PRE-43) | `F-KFR-CANONICAL-SIGNATURE-INVALID` | M13 |
| PRE-61 | F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED | legacy-migration KFR load with re-enabled accept | `F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED` | **NO M13** (migration-state file must be operator-signed) |
| PRE-62 | F-KFR-PATH-SYMLINK-FORBIDDEN | every KFR file open (atomic-read fcntl.flock) | `F-KFR-PATH-SYMLINK-FORBIDDEN` | M13 |
| PRE-63 | F-KFR-TAG-MODIFIED | KFR write wrapper, on `required_for_funder` tag mutation | `F-KFR-TAG-MODIFIED` | M13 (audited as TAMPER_EVENT) |
| PRE-64 | F-KFR-DUPLICATE-KEY | every KFR YAML load post-SafeLoader | `F-KFR-DUPLICATE-KEY` | M13 |
| PRE-65 | F-DERIVATION-AST-FORBIDDEN-NODE | every derivation eval, before runtime | `F-DERIVATION-AST-FORBIDDEN-NODE` | **NO M13** — sandbox escape vector |
| PRE-66 | F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING | benchmark cross-check, before compare | `F-BENCHMARK-CROSS-CHECK-AUDIT-MISSING` | M13 |
| PRE-67 | F-BENCHMARK-SEEDING-SOURCE-UNAUTHORIZED | benchmark seeding ingest | `F-BENCHMARK-SEEDING-SOURCE-UNAUTHORIZED` | M13 |
| PRE-68 | F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID | benchmark seeding ingest | `F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID` | M13 (key-rotation only) |
| PRE-69 | F-CURRENCY-FLOAT-IN-COMPARISON | every currency comparison call | `F-CURRENCY-FLOAT-IN-COMPARISON` | **NO M13** — Decimal mandate |
| PRE-70 | F-CURRENCY-CONTEXT-OMITTED | every currency helper invocation, before runtime | `F-CURRENCY-CONTEXT-OMITTED` | **NO M13** |
| PRE-71 | F-CURRENCY-CONTEXT-MISMATCH | every currency helper invocation, before runtime | `F-CURRENCY-CONTEXT-MISMATCH` | **NO M13** — identity check on KFR_DECIMAL_CONTEXT |
| PRE-72 | F-CURRENCY-DECIMAL-CONTEXT-DRIFT | every currency helper invocation, before runtime | `F-CURRENCY-DECIMAL-CONTEXT-DRIFT` | **NO M13** |
| PRE-73 | F-CURRENCY-UNIT-MISMATCH | every currency comparison, after Decimal cast | `F-CURRENCY-UNIT-MISMATCH` | M13 (LOW; CF-RT-06 fold-in) |
| PRE-74 | F-AWARD-INGEST-ATTN-UNVERIFIED | AWARD_INGEST mode entry | `F-AWARD-INGEST-ATTN-UNVERIFIED` | M13 |
| PRE-75 | F-INTAKE-TELEMETRY-LEAK | Intake CLI bootstrap, before any import | `F-INTAKE-TELEMETRY-LEAK` | **NO M13** — process-wide bootstrap discipline |
| PRE-76 | F-INTAKE-LOGFIRE-STUB-MISSING | Intake CLI bootstrap, after stub injection | `F-INTAKE-LOGFIRE-STUB-MISSING` | **NO M13** — RT-11 closure |

### §16.5 POST-gate row additions (Slice 4 family — 1 POST)

| Order | Check ID | Fires at | Failure code | Bypass |
|---|---|---|---|---|
| POST-26 | F-DERIVATION-RUNTIME-ARITHMETIC-ERROR | after derivation eval, on runtime exception | `F-DERIVATION-RUNTIME-ARITHMETIC-ERROR` | M13 (LOW; DC-CF-01 fold-in) |

### §16.6 Test inventory (Slice 4 — 199 new tests)

**Gate tests (16 of 19 — 107 tests):**

| Test file | LOC | SHA3-512[:16] | Tests |
|---|---|---|---|
| `test_f_kfr_yaml_construct_forbidden.py` | 45 | `9988945810a36480` | 5 |
| `test_f_kfr_canonical_signature_invalid.py` | 121 | `1f2265b8bb86406f` | 6 |
| `test_f_kfr_legacy_accept_re_enabled_unsigned.py` | 117 | `eaca7458ba2a2bb0` | 9 |
| `test_f_kfr_path_symlink_forbidden.py` | 58 | `4042eeb1a2f189ef` | 4 |
| `test_f_kfr_tag_modified.py` | 149 | `5a912cc7f119dfe1` | 10 |
| `test_f_kfr_duplicate_key.py` | 76 | `a098bf1cff71265f` | 7 |
| `test_f_derivation_ast_forbidden_node.py` | 52 | `b5dd582b661912ee` | 6 |
| `test_f_derivation_runtime_arithmetic_error.py` | 81 | `6a43597945dba043` | 7 |
| `test_f_benchmark_cross_check_audit_missing.py` | 112 | `c71d6de0a656fb24` | 8 |
| `test_f_benchmark_seeding_source_unauthorized.py` | 63 | `c7b9fc16c9f35e92` | 5 |
| `test_f_benchmark_seeding_allowlist_signature_invalid.py` | 121 | `52f4239a3651462d` | 6 |
| `test_f_currency_float_in_comparison.py` | 52 | `227adb3eb6a37002` | 5 |
| `test_f_currency_unit_mismatch.py` | 71 | `0b3afefd2ed914ad` | 6 |
| `test_f_award_ingest_attn_unverified.py` | 112 | `b3257105a5e38e3b` | 8 |
| `test_f_intake_telemetry_leak.py` | 83 | `42fdf4da29a0142f` | 8 |
| `test_f_intake_logfire_stub_missing.py` | 77 | `2bd1292512a9faf3` | 7 |

**Supporting-module tests (5 files — 92 tests):**

| Test file | Tests | Coverage |
|---|---|---|
| `tests/logician/canonicalization/test_kfr_canonical_differential.py` | 17 | PyYAML/ruamel/hand-written byte-equality round-trip; NFC-FIRST equality |
| `tests/logician/canonicalization/test_kfr_safe_loader_merge_key_reject.py` | 12 | anchor/alias/`<<` merge-key/tag rejection |
| `tests/logician/derivation/test_ast_whitelist.py` | 29 | dunder/Index/Slice/float-Constant rejection |
| `tests/logician/currency/test_decimal_arithmetic.py` | 26 | tolerance boundary; float-input rejection; context discipline (covers `F-CURRENCY-CONTEXT-OMITTED` / `F-CURRENCY-CONTEXT-MISMATCH` / `F-CURRENCY-DECIMAL-CONTEXT-DRIFT` at the helper layer where the actual logic lives) |
| `tests/logician/benchmarks/test_cross_check_constant_time.py` | 8 | timing variance < 1ms across 1000 invocations; audit-log presence |

### §16.7 Test coverage gap — disposition

Three gates from the §16.4 PRE table — `F-CURRENCY-CONTEXT-OMITTED` (PRE-70), `F-CURRENCY-CONTEXT-MISMATCH` (PRE-71), `F-CURRENCY-DECIMAL-CONTEXT-DRIFT` (PRE-72) — do NOT have dedicated `tests/logician/gates/test_f_currency_context_*.py` files at Slice 4 close. The behavioral coverage lives at the helper layer (`tests/logician/currency/test_decimal_arithmetic.py`, 26 tests across `KFR_DECIMAL_CONTEXT` / `to_currency()` / `assert_kfr_context_active()` / `CurrencyContextError`). Each of the three gate modules is a thin (~62 LOC) wrapper that re-raises the helper's `CurrencyContextError` as a structured `*Result` dataclass; the wrapper logic is straightforward dataclass construction with no branching beyond the success/failure split.

**Disposition (operator-confirmable, fold-in pattern per L-014 + WS-D row-170 transparent disposition):** the three missing per-gate test files are flagged as a known coverage gap. The audit may surface this; closure path is either (a) accept the helper-layer coverage as sufficient and document the wrapper-test exemption in §8 test-coverage-discipline, OR (b) author the three test files at Cycle 1 closure (≤30 min wall, low-risk — six tests per file mirroring `test_f_currency_unit_mismatch.py` shape would close the gap). Operator decides at audit synthesis.

### §16.8 Author response log + decisions surfaced (Slice 4)

1. **Renaming + 18 net-new (one renaming = `F-KFR-CANONICAL-SIGNATURE-INVALID` supersedes `F-KFR-SIGNATURE-INVALID` from Slice 2).** The §3 Slice 2 row for `F-KFR-SIGNATURE-INVALID` (PRE-43) is superseded by `F-KFR-CANONICAL-SIGNATURE-INVALID` under the canonicalization regime. The Slice 2 module `f_kfr_signature_validation.py` remains on disk; the Slice 4 module `f_kfr_canonical_signature_invalid.py` is the v7.0.4-M1-pinned successor. Both code constants exist; the §0.5 paired-commit registers both with a supersession pointer.
2. **F-KFR-AUDIT-CHAIN-BROKEN combined-module preservation.** The Slice 2 combined module `f_kfr_signature_validation.py` (housing both `F-KFR-SIGNATURE-INVALID` + `F-KFR-AUDIT-CHAIN-BROKEN`) is preserved; the Slice 4 canonical-signature module is independent. The audit-chain-broken sub-code is still served by the combined module per §3.1 PRE-44.
3. **Three-layer Decimal context discipline (M1 §6.2.1).** Currency arithmetic uses `KFR_DECIMAL_CONTEXT` (singleton context, prec=28, ROUND_HALF_EVEN). Three gates enforce: omitted (PRE-70) / non-identity (PRE-71) / global drift (PRE-72). The decision to leave the per-gate test files unwritten — relying on `test_decimal_arithmetic.py` helper-layer coverage — is documented in §16.7 above for operator disposition at audit.
4. **AST-whitelist (M1 §3.2 + §3.3).** Explicit `ast.NodeVisitor` enumerates allowed nodes; rejects `ast.Index`, `ast.Slice`, `ast.Constant` of float type, and any `__dunder__`-named subscript key. Tests cover dunder/Index/Slice/float vectors (29 tests in `test_ast_whitelist.py`).
5. **Constant-time benchmark cross-check (M1 §5.2.2).** `hmac.compare_digest` replaces `==`; audit-log write-before-compare + dummy-pad + fsync. Test asserts timing variance < 1ms across 1000 invocations.
6. **Logfire bootstrap shim (M1 §8.4.1, RT-11 closure).** `pipeline/cli/tilth_intake.py` sets `LOGFIRE_ENABLED=0` and injects `_LogfireDisabledStub` BEFORE any import. Two PRE gates enforce (PRE-75 telemetry leak; PRE-76 stub missing).
7. **AST-lint cycle Slice 3 flagged.** Slice 3 surfaced an AST-lint discipline question around currency-float comparison sites in pre-Slice-4 modules. Slice 4 lands `r_currency_no_float_compare.py` which formalizes the rule and retroactively closes the cycle. Confirmed via `scripts/run_lint.sh pipeline/logician/` exit=0 at Slice 4 close.

**Audit trail at Slice 4 close:**

- Module SHAs + test SHAs: per §16 tables above (19 gate modules + 5 supporting modules + 16 gate-test files + 5 supporting-test files).
- Test pass counts: 199 new (Slice 4) — 107 gate tests + 92 supporting-module tests.
- AST-lint state: clean per `scripts/run_lint.sh pipeline/logician/` exit=0.
- Cedar policies: 5 NEW on disk under `pipeline/vault/policies/`.
- AST-lint rules: 3 NEW on disk under `pipeline/linting/`.
- Coverage gap: 3 currency context gates (PRE-70/71/72) lack dedicated `tests/logician/gates/test_f_currency_context_*.py` — disposition pending audit synthesis (§16.7).

### §16.9 Slice 4 + L-006 binding interaction

The L-006 dormant-binding pattern at v7.0.7 §5.1 fires at this amendment's Cowork Thesis LOCK (per Slice 3 §4 above). The Slice 4 additions do NOT extend the F-CLASS-COVERAGE-INCOMPLETE META gate's `REQUIRED_F_CLASS_CODES` — Slice 4 codes are F-KFR-* / F-DERIVATION-* / F-BENCHMARK-* / F-CURRENCY-* / F-AWARD-INGEST-* / F-INTAKE-* (none are F-CLASS-*). The META gate's exclusion of itself is preserved.

Composition with v7.0.4-M1 §10 registry: every M1 failure code has a corresponding §16.4/§16.5 row in this amendment plus a live module + test on disk per §16.6 (modulo the §16.7 disposition — closed at Cycle 1 fold-in per §16.10).

## §16.10 Cycle 1 closure log + dispositions (2026-05-10)

L-005 Cycle 1 fired 2026-05-10 with FULL live cross-family rigor: Editor (Llama 3.3 70B / Groq, Meta family) READY_TO_LOCK with 7 advisory findings + Judge (Gemini 2.5 Pro / Google) READY_TO_LOCK 100/100 with 2 LOW DC + Red Team (GPT-OSS 120B / Groq, OpenAI-OSS family) ESCALATE blocking:true with 16 findings (5 HIGH + 9 MED + 2 LOW). Audit trail at `pipeline/validation/v4_v2_x_thesis_2026-05-10/` with `audit_v1_{editor,judge,red_team}.{md,raw.json}` + `audit_v1_synthesis.md`.

### §16.10.1 FOLDED-IN closures (text + code edits)

Eight findings closed via fold-in at Cycle 1 fix time:

- **E-01 (slice plan readability)** — §0 inline note added pointing to §16; §10 framing preserved as historical record per L-014 faithful-consolidation pattern.
- **E-03 + DC-01 + RT-04 + RT-05 (currency context test gap)** — three new test files authored at `tests/logician/gates/test_f_currency_context_omitted.py` (6 tests) + `test_f_currency_context_mismatch.py` (7 tests) + `test_f_currency_decimal_context_drift.py` (6 tests) = 19 new wrapper tests covering success path + every failure-leg dataclass-field population + frozen-instance immutability + failure-code constant export. §16.7 disposition CLOSED via Path B (author the test files at Cycle 1 closure).
- **E-05 (Slice 4 cross-section composition)** — §6.2.2 NEW added covering canonicalization stack + AST whitelist + currency Decimal + benchmark seeding + Logfire bootstrap composition narrative + cross-slice signature-verification discipline (re-statement per Judge DC-02).
- **E-06 (test count §8 stale)** — §8 updated to actual 497 total new tests across all four slices + Cycle 1 closures.
- **E-07 (HORIZON Archivist row)** — §5.3 updated to reflect §15 v1 SPEC-LOCKED 2026-05-10 row 191 with five owned gate codes (the four originally listed plus `F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT` NEW per §15 Cycle 2 RT-11 closure).
- **RT-12 (Unicode-confusable digit bypass)** — `f_class_outbound_boundary.py` `_OPAQUE_SLOT_RE` regex updated to `\[SLOT_([0-9]+)\]` with `re.ASCII` flag; three new tests in `test_f_class_outbound_boundary.py` (Devanagari `१` + Arabic-Indic `١` rejection + ASCII-digit regression).
- **RT-10 (per-org leakage via allowlist schema)** — `seeding_allowlist_loader.py` strict-key whitelist `_ALLOWED_ALLOWLIST_KEYS` enforces seven schema keys + signature pair; extra keys (`org_slug`, `who`, `fact_id`, etc.) fail-closed at load. Two new tests in `test_f_benchmark_seeding_allowlist_signature_invalid.py` (org_slug + who rejection).

### §16.10.2 REJECTED findings (Red Team premise contradicted by on-disk code)

Three Red Team HIGH findings rejected with rationale per L-018 transparent disposition:

- **RT-06 (canonicalization order bug)** — REJECTED. `pipeline/logician/canonicalization/kfr_canonical.py` applies NFC FIRST inside `_encode_string` (every string scalar) AND inside `_encode_mapping` (every mapping key, BEFORE sort). The spec order (NFC → numeric-pin → key-sort → minimal-whitespace → bool/null/array) is preserved by the code structure: NFC normalization on string keys runs in `_encode_mapping` BEFORE the `sorted_items.sort(key=lambda kv: kv[0])` call; numeric pinning operates on numeric types where NFC is a no-op. Spec-to-code order match is exact. Red Team's claim "order is reversed" is contradicted by line-by-line read.
- **RT-07 (SafeLoader merge-key rejection incomplete)** — REJECTED. `kfr_safe_loader.py` has THREE-layer rejection of merge-keys: (1) `KFR_FORBIDDEN_TAGS` includes `tag:yaml.org,2002:merge`; (2) `_check_node_recursive` walks the parsed node tree and refuses any forbidden tag; (3) `KfrSafeLoader.construct_mapping` overrides PyYAML to refuse the literal `<<` mapping-key surface BEFORE PyYAML's merge-key resolution can fire. All three layers fail-closed via `KfrConstructError`. Red Team's claim "loader does not block !!merge tag when explicit" is contradicted by the explicit forbidden-tag set + node-walk + construct_mapping override.
- **RT-08 (legacy-migration unsigned bypass via post-gate file replacement)** — REJECTED. `f_kfr_legacy_accept_re_enabled_unsigned.py` is a PRE-WRITE gate on the legacy_accept_mode TRANSITION (`previous_mode → new_mode`), not a PRE-LOAD gate verifying a `_migration_state.yaml` signature. The gate requires an operator-signed admin-risk-ledger entry (`LEDGER_KIND_LEGACY_RE_ENABLE`) with `signed_at_utc` + `operator_key_id` + `rationale`. Subsequent KFR loads re-run `F-KFR-CANONICAL-SIGNATURE-INVALID` at every read; ledger row creation requires operator key. Red Team's premise ("gate verifies signature of `_migration_state.yaml`") inverts the gate's actual contract.

### §16.10.3 ALREADY-CLOSED findings (closed by existing mechanism)

- **RT-09 (TOCTOU race on symlink check)** — ALREADY-CLOSED by v7.0.4-M1 §4.2.2 atomic-read discipline (LOCKED row 190). `f_kfr_path_symlink_forbidden.py` docstring is explicit: "the gate itself only owns the symlink predicate; the fcntl.flock + O_NOFOLLOW open machinery is implementation detail of the disk-state read helper." TOCTOU is closed at the helper layer (atomic-read leg); the gate is the symlink-rejection leg. M1 LOCK closure RT-05 §4.2.2 already FOLDED-IN at LOCK row 190.

### §16.10.4 BOUNDED-by-A1+A4 (operator-trusted preflight, single-client v0.1)

Four findings dispositioned as bounded by v7 LOCKED A1 (single-client deployment) + A4 (operator-trusted preflight) — real architectural concerns at multi-tenant scale, but out-of-scope-for-v0.1 with v2 Section O.5 mitigation track:

- **RT-01 (META gate FileExistsCallable injection)** — `file_exists` is a kwarg-only Protocol-DI parameter (no default); orchestrator code is operator-controlled at v0.1 single-client trust posture. Multi-tenant injection-surface hardening tracks in v2 Section O.5.
- **RT-02 (META gate self-test broken-symlink loophole)** — self-coverage test runs against operator-trusted on-disk paths. `os.path.exists` returns `False` for broken symlinks (Python stdlib semantics — Red Team's premise inverted). Operator-controlled file-system at v0.1.
- **RT-15 (Logfire stub bypass via `sitecustomize.py`)** — `sitecustomize.py` is operator-controlled; production containers disable user-site by policy. v0.1 bounded by A1+A4.
- **RT-16 (subprocess Logfire-stub propagation)** — subprocess-inheritance hardening is a v0.2 work item; document as known limitation.

### §16.10.5 DEFERRED findings (real but out-of-scope-for-v0.1-Beta)

Three findings deferred to future spin per L-005 strict-two-cycle discipline:

- **RT-11 (audit-log oracle)** — write-before-compare per M1 §5.2.2 is the operator-LOCKED discipline (M1 LOCKED row 190). Tightening to write-after-compare requires a new M1-class corrective amendment. Open question for v0.2 spin: should benchmark cross-check audit-log write happen AFTER compare (rather than before), and should the audit log entry store only `hmac.digest` of the comparison result? Not blocking for v0.1 Beta.
- **RT-13 (opaque-slot omission not detected)** — current `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` detects literal-substitution at the registered anchor (token absence at anchor with surrounding context preserved); does NOT detect full-omission-without-replacement (where the cloud-routed seat rewrites the surrounding sentence to drop the slot context entirely). Closure requires `SlotRegistry` injection with anchor-position metadata + secret-value-presence check — v0.2 work per the F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED anchor-mapping evolution. Document as known limitation.
- **RT-14 (anchor-position mismatch)** — same dependency surface as RT-13; v0.2 work.

### §16.10.6 INFO / process-recommendation findings (no edit)

Five findings noted as INFO without edits at Cycle 1:

- **RT-03 (REQUIRED_F_CLASS_CODES mutability)** — REJECTED in synthesis (the constant is `Final[tuple[str, ...]]`, already immutable; Red Team's "mutable list" premise contradicted by code).
- **E-02 (failure-code table format consistency)** — INFO; format is consistent enough across slices; no edit required.
- **E-04 (renaming/supersession discipline)** — already documented in §16.8 #1; no edit.
- **DC-02 (identity-strict signature explicit re-statement)** — process recommendation; the §6.2.2 cross-slice discipline narrative re-states the principle for cross-slice reading-surface clarity (§6.2.2 last paragraph satisfies the recommendation).
- **DC-01 (test coverage gap formal closure)** — closed via Path B fold-in (§16.10.1 above).

### §16.10.7 Cycle 2 verification scope

Cycle 2 fires on the post-fix amendment (this file) + post-edit code (`f_class_outbound_boundary.py` RT-12 fix; `seeding_allowlist_loader.py` RT-10 fix; three new currency-context test files; two new RT-12/RT-10 test additions). Cycle 2 prompt body confirms FOLDED-IN closures hold + REJECTED findings stay rejected on second look + BOUNDED + DEFERRED items have appropriate disposition language.

L-005 strict-two-cycle: Cycle 2 outcome is either (a) PASS → LOCK, or (b) PARTIAL/NEW → row-170 transparent disposition at LOCK (per WS-D + WS-B + WS-C-M1 + §15 Archivist precedents). No silent third audit round.

## §16.11 Cycle 2 close + LOCK ceremony (2026-05-10)

L-005 Cycle 2 fired 2026-05-10 with FULL live cross-family rigor — same Editor/Judge/Red Team families as Cycle 1. Audit trail at `pipeline/validation/v4_v2_x_thesis_2026-05-10/` with `audit_v2_{editor,judge,red_team}.{md,raw.json}` + `audit_v2_synthesis.md`.

### §16.11.1 Cycle 2 reviewer verdicts

- **Editor (Llama 3.3 70B / Groq, Meta family):** **READY_TO_LOCK.** All five Cycle 1 findings CONFIRMED CLOSED (E-01 + E-03 + E-05 + E-06 + E-07). No regressions detected in §0, §5.3, §6.2.2, §8, §16.10. No new findings.
- **Judge (Gemini 2.5 Pro / Google):** **READY_TO_LOCK 100/100.** Both Cycle 1 design concerns CLOSED (DC-01 via Path B fold-in confirmed at §16.10.1; DC-02 via §6.2.2 cross-slice signature-verification restatement confirmed). Five rubric dimensions re-scored at 20/20. Cycle 1 verdict maintained. Quote: *"the author's synthesis and disposition of the full cross-family audit in §16.10 is rigorous, transparent, and technically sound. The amendment is fit for purpose and ready for LOCK."*
- **Red Team (GPT-OSS 120B / Groq, OpenAI-OSS family):** **REQUIRES_MINOR_FIXES blocking:true.** Of 16 Cycle 1 findings: 9 CONFIRMED_REJECTED + 9 CONFIRMED_CLOSED + 4 BOUND_OK + **2 PARTIAL (RT-04/RT-05)** + 2 NEW defense-in-depth notes.

### §16.11.2 Cycle 2 PARTIAL findings — REJECTED with rationale (row-170 transparent disposition)

Red Team's Cycle 2 PARTIAL claim on RT-04 + RT-05: "the three new test files exercise helper-layer functions rather than gate wrappers; the gate wrappers are thin adapters; they are not directly imported in the new tests, so failure-code constant export and Result dataclass shape are un-validated."

**Verified against on-disk content of `tests/logician/gates/test_f_currency_context_omitted.py` + `test_f_currency_context_mismatch.py` + `test_f_currency_decimal_context_drift.py` — Red Team's premise is contradicted.** Each test file:

1. **Imports the gate module directly** via `from pipeline.logician.gates.f_currency_context_<X> import (Currency<X>Result, check_currency_context_<X>)`.
2. **Invokes the gate's check function** — `check_currency_context_omitted(context=...)`, `check_currency_context_mismatch(context=...)`, `check_currency_decimal_context_drift()`.
3. **Asserts on the Result dataclass shape** — `result.success`, `result.failure_code`, `result.detail` (presence + non-empty + content checks).
4. **Asserts on failure_code constant export alignment** — `assert mod.F_CURRENCY_CONTEXT_OMITTED == F_CURRENCY_CONTEXT_OMITTED` and constant prefix asserts.
5. **Asserts on frozen-instance immutability** — `with pytest.raises(...): result.success = False`.

The Red Team did not inspect the test file contents before issuing PARTIAL; the speculation contradicts on-disk imports + assertions. **REJECTED per L-018 transparent disposition** — pattern-matches the Cycle 1 RT-06 / RT-07 / RT-08 / RT-03 rejections (Red Team premise contradicted by on-disk code).

### §16.11.3 Cycle 2 NEW defense-in-depth notes — FOLDED-IN to §16.10.5 DEFERRED items

Red Team Cycle 2 surfaced two real-but-non-blocking defense-in-depth notes; both fold into the §16.10.5 v0.2-hardening-backlog with explicit closure paths for v2 Section O.5:

- **(NF-DD-01)** Legacy-accept migration gate is PRE-WRITE only. Edge case: a freshly-installed system that never triggers a legacy-accept migration write never invokes the gate, leaving an unsigned migration file unchecked at first read. Bounded by current trust assumptions (operator-trusted preflight; v7 LOCKED A4); defense-in-depth gap, not a blocking defect. **v0.2 closure path:** add a PRE-LOAD signature check on `_migration_state.yaml` at first KFR cycle that also fires `F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED` if the file is present and unsigned.
- **(NF-DD-02)** Intake stub bypass via early third-party-plugin `import logfire`. Mitigated at v0.1 by the frozen Golden Image (no third-party plugin loading on appliance). **v0.2 closure path:** add a process-wide `if "logfire" in sys.modules: raise RuntimeError("Logfire imported before tilth_intake bootstrap")` guard at bootstrap entry; document as v2 Section O.5 multi-tenant hardening line item.

Both notes track in v2 Section O.5 alongside RT-01 + RT-02 + RT-15 + RT-16 (the four Cycle 1 BOUNDED items).

### §16.11.4 LOCK ceremony

L-005 strict two-cycle CLOSED with FULL live cross-family rigor across both cycles. Section E carve-out NOT INVOKED — this is the **seventh substantive v0.1+v0.2 round to LOCK with FULL live cross-family rigor** (precedents: WS-D v7.0.5 row 179 + WS-F §12 v1 row 182 + WS-E §11 v1 row 185 + WS-H §2 v7.2 row 186 + WS-G §5 v8 row 188 + WS-C-M1 v7.0.4-M1 row 190 + §15 Archivist row 191).

**Disposition summary at LOCK:**

- 8 FOLDED-IN Cycle 1 closures (E-01, E-03/DC-01/RT-04/RT-05 [via test files], E-05, E-06, E-07, RT-12, RT-10).
- 4 REJECTED Cycle 1 (RT-06, RT-07, RT-08, RT-03) — premises contradicted by on-disk code.
- 1 ALREADY-CLOSED Cycle 1 (RT-09) — closed by v7.0.4-M1 §4.2.2 atomic-read.
- 4 BOUNDED-by-A1+A4 Cycle 1 (RT-01, RT-02, RT-15, RT-16) — v2 Section O.5 mitigation track.
- 3 DEFERRED Cycle 1 (RT-11, RT-13, RT-14) — v0.2 spin / v0.2 horizon work.
- 5 INFO Cycle 1 (E-02, E-04, DC-02 satisfied via §6.2.2).
- 2 REJECTED Cycle 2 PARTIAL (RT-04, RT-05) — Red Team premise contradicted by on-disk test file contents.
- 2 FOLDED-IN Cycle 2 NEW defense-in-depth notes (NF-DD-01 legacy-accept PRE-WRITE only; NF-DD-02 Intake stub plugin bypass) — v2 Section O.5 mitigation track.

**LOCK status: §4 v2.x amendment LOCKED 2026-05-10.** L-006 dormant-binding ACTIVATED at this LOCK ceremony per v7.0.7 §5.1 binding clause: F-CLASS-COVERAGE-INCOMPLETE PRE-cycle gate has all 12 F-CLASS-* primitives realized + tested + on-disk; the META gate's REQUIRED_F_CLASS_CODES is satisfied. **v0.1 Beta architectural gate FULLY CLEARED.**

Compound-LOCK siblings: §4 v2.x amendment LOCKED (sibling 1/2) + §0.5 v14 paired-commit row appends (sibling 2/2) at the same lock_timestamp_utc per §6.17 Option-B paired-commit pattern.

---

*Slice 1 — Funder Intel LANDED 2026-05-10. Slice 2 — KFR residuals LANDED 2026-05-10. Slice 3 — F-CLASS-* dormant primitives LANDED 2026-05-10. Slice 4 — v7.0.4-M1 corrective predicates LANDED 2026-05-10. All four Code-phase slices CLOSED. Cycle 1 closures applied 2026-05-10. Cycle 2 verification CLOSED 2026-05-10. **§4 v2.x LOCKED 2026-05-10. v0.1 Beta architectural gate FULLY CLEARED.***
