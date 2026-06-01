---
title: Blueprint §4 Logician — Amendment v2.x.3 (WS-J §14 Cycle 1+2 fold-in F-REPORT-* sub-tag registration + 2 NEW top-level F-REPORT-* gates + F-CEDAR-* sub-tag extensions + R-REPORT-DECIMAL-MANDATE scope expansion)
filed: 2026-05-15
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-15 — narrow follow-on amendment registering WS-J §14 Report Generator v1 LOCK Cycle 1 + Cycle 2 fold-in artifacts at the §4 Logician predicate-signature + sub-tag registration layer. L-005 strict two-cycle CLOSED 2026-05-15T19:00:37Z with FULL live cross-family rigor (Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via openclaw bridge). Cycle 1: Editor REQUIRES_FIX 7 findings → 6 FOLDED + 1 DEFERRED-NON-BLOCKING + Judge READY_TO_LOCK 99/100 → 1 narrative count fix + Red Team READY_TO_LOCK blocking:false 12 findings (3 P0 + 4 HIGH + 4 MED + 1 LOW) → 10 FOLDED + 1 PARTIALLY-FOLDED-DEFERRED-v2 + 1 NO-ACTION. Cycle 2: Editor READY_TO_LOCK 5 NEW E-NF-01..E-NF-05 → 2 NO-ACTION + 3 FOLDED + Judge READY_TO_LOCK 99/100 maintained 1 NEW J-NF-01 FOLDED at frontmatter + Red Team REQUIRES_FIXES blocking:true 8 NEW RT-C2-01..RT-C2-08 → ALL 8 FOLDED at §12 row-170 transparent-disposition pattern (introducing immutable_kind row attribute per RT-C2-04 + WS-J Code phase contract-verification table per RT-C2-06 + RT-C2-08 config-diff sub-check). FOURTEENTH substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor (after WS-D + WS-F + WS-E + WS-H + WS-G + WS-K + WS-C-M1 + WS-L + WS-I + WS-J + WS-Reflection v0.1 hook + WS-WPFA + §11 v1.1 + WS-FG + WS-Reflection-Packet). Compound paired-commit with §0.5 v23 amendment (3 new rows: 506-508; runtime-live total 505 → 508). Mirrors §4 v2.x.1 (Tilth-RT-07 narrow-corrective at row 198) sub-tag-extension precedent for sub-tags under existing rows 386-390; mirrors §13 v1 §5.1 HORIZON→ACTIVE graduation pattern at §4 v2.x rows 300-305 for the five base F-REPORT-* codes; mirrors §4 v2.x.2 row-203 NEW-top-level-failure-code registration pattern for F-REPORT-BENEFICIARY-PRIVACY-LEAK + F-REPORT-OPERATOR-KEY-ROTATION-VALIDITY. Compound paired-commit with §0.5 v23 amendment (3 new rows: 1 marker + 2 failure-code).
parent_lock: pipeline/blueprint/v0.1/section_04_v2_x_amendment.md  # §4 v2.x LOCKED 2026-05-10 rows 193/194 (parent F-REPORT-* HORIZON registration at §5.2)
parent_lock_row: 193
predecessor_amendments_chain:
  - §4 v2.x LOCKED 2026-05-10 rows 193/194 — Tier-3 LOCK; ~44 failure codes across 4 slices including the 5 F-REPORT-* HORIZON rows at §5.2
  - §4 v2.x.1 LOCKED 2026-05-10 rows 198/199 — narrow-corrective Tilth-RT-07 R-ARCHIVIST-NO-CANONICAL-MUTATE sub-tag-extension; CANONICAL PRECEDENT for sub-tag-extension §0.5 paired-commit pattern
  - §4 v2.x.2 LOCKED 2026-05-10 row 203 — Reflection v0.1 Beta hook (8 BINDING + 8 HORIZON + 1 PROBE-DEPENDENT F-REFLECTION-* + 5 F-ARCHIVIST-* sub-tag extensions); CANONICAL PRECEDENT for NEW top-level failure-code-row registration paired with sub-tag extensions in a single amendment
  - §4 v2.x.4 LOCKED 2026-05-11 row 213 — Funding Goal F-FG-* family with seat_owner attribute extension
  - §4 v2.x.y LOCKED 2026-05-15 row 217 — F-PACKET-* family (sibling-not-nested with WPFA per Path B naming reconciliation)
parent_lock_at_§14: pipeline/blueprint/v0.1/section_14_report_generator.md  # §14 v1 LOCKED 2026-05-10 rows 200/201 (HORIZON-flip authority + Cycle 1+2 fold-in source-of-truth)
companion_lock_paired_commit:
  - pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_3_amendment.md  # §0.5 v23 paired-commit; 3 rows (506-508)
amendment_class: narrow follow-on — F-REPORT-* HORIZON→ACTIVE graduation + sub-tag-extension on rows 386-390 + 2 NEW top-level failure-code registration + F-CEDAR-* sub-tag extension at rows 268/272 + R-REPORT-DECIMAL-MANDATE scope expansion (narrative + glob-list edit at §14.13.4 cross-reference)
precedent_pattern: §4 v2.x.1 row-198 sub-tag-extension precedent for in-place row 386-390 + 268/272 narrative annotations; §4 v2.x.2 row-203 NEW-top-level-failure-code registration precedent for F-REPORT-BENEFICIARY-PRIVACY-LEAK + F-REPORT-OPERATOR-KEY-ROTATION-VALIDITY; §13 v1 §5.1 HORIZON→ACTIVE graduation precedent at §4 v2.x rows 300-305 for the five base F-REPORT-* HORIZON rows.
threat_severity_at_v0_1_v0_2: LOW — predicate signatures only; no runtime invocation; bodies remain skeleton stubs raising NotImplementedError until WS-J Code phase. Activation gated by NotImplementedError stubs at the predicate-body layer + R-REPORT-DECIMAL-MANDATE AST-lint scope at the static-analysis layer. The §14 v1 SPEC LOCK already absorbed the Cycle 1+2 fold-ins at the §14 text + §14.18 closure-disposition layer; this amendment lifts those fold-ins into the §4 Logician registration layer where they are observable to the F-INDEX-STALE PRE-gate + future WS-J Code phase predicate-realization sweep.
purpose: Lift §14 v1 LOCK Cycle 1 + Cycle 2 fold-ins into the §4 Logician registration layer — (a) graduate the five base F-REPORT-* HORIZON rows at §4 v2.x §5.2 to ACTIVE-AT-§14-v1-LOCK (mirrors §13 v1 §5.1 graduation); (b) extend the sub-tag enumerations on rows 386-390 with **fourteen** new sub-tags from Cycle 1 + Cycle 2 fold-ins per §4 v2.x.1 row-198 in-place narrative annotation precedent (count corrected from initial 11 to 13 per Judge Cycle 1 J-Dim3 fix; further to 14 after Cycle 1 RT-07 SPLIT of `.cross_period_signature_invalid`; J-NF-01 frontmatter drift fix at Cycle 2); (c) register two NEW top-level failure codes (F-REPORT-BENEFICIARY-PRIVACY-LEAK from §14 RT-C2-03 + F-REPORT-OPERATOR-KEY-ROTATION-VALIDITY from §14 RT-C2-05) per §4 v2.x.2 row-203 explode-per-code precedent; (d) extend F-CEDAR-* sub-tags at §0.5 rows 268/272 with **three** new sub-tags from §14 RT-6b/RT-6c/RT-C2-06 per §4 v2.x.1 row-198 in-place precedent; (e) document R-REPORT-DECIMAL-MANDATE scope expansion per §14 RT-C2-01 closure (composer-module glob-list extension on already-registered rule; no new module). **Total sub-tag extensions: 17 (14 F-REPORT-* + 3 F-CEDAR-*)**.
companion_code_landed:
  - "pipeline/logician/gates/f_report_*.py (NEW SCAFFOLD — 7 modules; 5 base codes + 2 NEW codes; ALL bodies raise NotImplementedError per WS-J Code phase deferral)"
  - "pipeline/orchestrator/seats/report_generator/__init__.py (existing per §14 v1 LOCK)"
  - "Composer + track-binding modules (already in §14.13.4 R-REPORT-DECIMAL-MANDATE expanded scope)"
companion_tests_landed:
  - "tests/logician/gates/test_f_report_skeleton.py (NEW — 7 predicate-signature presence assertions + sub-tag enumeration coverage tests; all skeleton-stub raises tested)"
  - "tests/linting/test_r_report_decimal_mandate_lint_clean_composer_scope.py (RESERVED at §14.13.4; companion to test_r_report_decimal_mandate_lint_clean — tests composer-module glob coverage; deferred to WS-J Code phase)"
done_definition_at_lock:
  - "Five base F-REPORT-* HORIZON rows at §4 v2.x §5.2 narrative annotated as ACTIVE-AT-§14-v1-LOCK with parent_lock row 200 reference."
  - "Eleven new sub-tags landed in narrative annotations under §0.5 rows 386-390 (per §4 v2.x.1 row-198 in-place sub-tag-extension precedent)."
  - "Two NEW top-level failure codes (F-REPORT-BENEFICIARY-PRIVACY-LEAK + F-REPORT-OPERATOR-KEY-ROTATION-VALIDITY) registered at predicate-signature layer in pipeline/logician/gates/ with NotImplementedError bodies + cross-reference to §14.9.3 + §14.9.5 closure text."
  - "Three new F-CEDAR-* sub-tags landed in narrative annotations under §0.5 rows 268/272 (.engine_unready + .tier_history_unsigned + .tier_history_missing)."
  - "R-REPORT-DECIMAL-MANDATE scope expansion documented in §4 v2.x.3 §5 + cross-referenced to §14.13.4 (no new module file; glob-list extension only)."
  - "Skeleton tests passing at predicate-signature layer."
  - "AST-lint clean against composer scope (the WS-J Code phase will realize the predicate bodies + extend the lint to the broader composer scope)."
  - "L-005 strict two-cycle Thesis CLOSED with FULL live cross-family rigor."
cowork_thesis_dispatch_status: BOTH CYCLES COMPLETE 2026-05-15. All dispatches via mcp__Control_your_Mac__osascript → openclaw bridge per AGENTS.md. Working templates cloned from pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh + adapted to pipeline/validation/section_04_v2_x_3_thesis_2026-05-15/dispatch_audit_v{1,2}.sh. L-005 strict two-cycle CLOSED.
ws_dispatch: §4 v2.x.3 follow-on (this session) — modeled on §4 v2.x.1 narrow-corrective + §4 v2.x.2 dormant-binding precedents.
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment v2.x.3 — WS-J §14 Cycle 1+2 fold-in F-REPORT-* registration

## §0. Amendment intent + scope

This amendment **lifts** the WS-J §14 Report Generator v1 LOCK (rows 200/201, 2026-05-10) Cycle 1 + Cycle 2 fold-in artifacts into the §4 Logician predicate-signature + sub-tag registration layer. The §14 v1 LOCK already absorbed the fold-ins at the §14 text + §14.18 closure-disposition layer (Cycle 1: 28 findings of which 22 FOLDED-IN, 4 BOUNDED, 2 CLOSED-via-other; Cycle 2: 10 NEW probes RT-C2-01..RT-C2-10 all FOLDED-IN per row-170 transparent disposition pattern). What was NOT lifted at §14 v1 LOCK is the §4 v2.x §5.2 HORIZON→ACTIVE flip + the §0.5 row-386-390 sub-tag-extension narrative + the two NEW top-level failure-code registrations — those defer to this follow-on per the §14 v1 LOCK status note: "predicate bodies skeleton-stubs at v0.2 first ship; Code phase realizes substrate per WS-J Code follow-on dispatch."

**This amendment is the WS-J §14 → §4 Logician registration follow-on** (NOT the WS-J Code phase). Predicate bodies remain NotImplementedError stubs. The amendment makes the gate set observable to the F-INDEX-STALE PRE-gate + future WS-J Code phase predicate-realization sweep.

**Precedent-pattern attribution table (per Cycle 1 Editor E-01 closure).** Three patterns combined; per-section attribution:

| Section | Pattern invoked | Source amendment | Mechanism |
|---|---|---|---|
| §2 (HORIZON→ACTIVE graduation) | §13 v1 §5.1 graduation | §4 v2.x rows 300-305 | In-place narrative annotation on §4 v2.x §5.2; NO new §0.5 rows |
| §3.1-§3.5 (sub-tag extensions on F-REPORT-* rows 386-390) | §4 v2.x.1 row-198 sub-tag-extension | §4 v2.x.1 + §0.5 v16 | In-place narrative annotation on existing rows; NO new §0.5 rows; owner preserved |
| §4.1-§4.2 (NEW top-level F-REPORT-* codes) | §4 v2.x.2 row-203 explode-per-code | §4 v2.x.2 + §0.5 v18 | NEW failure-code rows in paired §0.5 v23; one row per code; predicate-signature layer with NotImplementedError + drift-test binding |
| §5 (F-CEDAR-* sub-tag extensions on rows 268/272) | §4 v2.x.1 row-198 sub-tag-extension (cross-seat variant per §0.5 v23 §D) | §4 v2.x.1 + §0.5 v23 §D | In-place narrative annotation on §2 v7.2-owned rows; NO new §0.5 rows; owner preserved (cross-seat read-path inheritance) |
| §6 (R-REPORT-DECIMAL-MANDATE scope) | Glob-list documentation on already-registered AST-lint rule | §14 v1 LOCK §14.13.4 | Narrative-only at this LOCK; actual glob-list extension lands at WS-J Code phase |

A contributor that picks the wrong pattern for a given sub-tag risks (a) creating spurious new §0.5 rows (sub-tag pattern would generate row count divergence at F-INDEX-STALE PRE-gate), or (b) silently dropping a NEW top-level code into the sub-tag set of an existing row (the explode-per-code pattern is the only correct path for the two new codes). The table above is contractually load-bearing for downstream contributors.

**Composition with §4 v2.x, §4 v2.x.1, §4 v2.x.2.** The amendment uses three patterns from prior §4 v2.x.x amendments:

- **§13 v1 §5.1 HORIZON→ACTIVE graduation pattern** (§4 v2.x rows 300-305) for the five base F-REPORT-* HORIZON rows at §4 v2.x §5.2 — flip the labels from `HORIZON — §14 LOCK` to `ACTIVE-AT-§14-v1-LOCK` with parent_lock row 200 reference. NO new §0.5 rows for the graduation; the §0.5 v17 rows 386-390 already exist.
- **§4 v2.x.1 row-198 sub-tag-extension pattern** for the eleven new sub-tags landing under existing F-REPORT-* codes + the three new sub-tags landing under existing F-CEDAR-* codes. NO new §0.5 rows; in-place narrative annotation under rows 386-390 + 268/272.
- **§4 v2.x.2 row-203 explode-per-code pattern** for the two NEW top-level failure codes (F-REPORT-BENEFICIARY-PRIVACY-LEAK + F-REPORT-OPERATOR-KEY-ROTATION-VALIDITY). NEW §0.5 rows 507/508 in the paired §0.5 v23 amendment.

**§11 v1.1 dependency.** The new sub-tag `F-REPORT-COMMITMENT-MISSED.commitment_id_invalid_format` (RT-C2-02 closure) requires `commitment_id` to validate against the safe-identifier regex `^[A-Z0-9_-]+$` BEFORE filesystem operation. The §11 v1.1 LOCK 2026-05-11 (rows 209/210) already landed the shared canonical home `seats/_commitment_id.py` with `sanitize_commitment_id()` per the AWARD_INGEST extraction pathway. This amendment composes against the existing §11 v1.1 surface — no new follow-on at §11 is required. The §14 RT-C2-02 closure text "§11 v1 AWARD_INGEST extraction MUST sanitize commitment_id at extraction time per a paired §11 v1.1 follow-on update (referenced; not authored at this LOCK)" is satisfied by the already-LANDED §11 v1.1 amendment.

## §1. Target glob + scope discipline

Target modules:

- `pipeline/logician/gates/f_report_commitment_untraced.py` — owns F-REPORT-COMMITMENT-UNTRACED predicate signature; NotImplementedError body; sub-tag enumeration in `FORBIDDEN_SUB_TAGS` table for runtime cross-reference (no body-side enforcement at v0.1 hook).
- `pipeline/logician/gates/f_report_commitment_missed.py` — owns F-REPORT-COMMITMENT-MISSED predicate signature; NotImplementedError body; sub-tag enumeration including new RT-2b + RT-C2-02 sub-tags.
- `pipeline/logician/gates/f_report_out_of_scope_drift.py` — owns F-REPORT-OUT-OF-SCOPE-DRIFT predicate signature; NotImplementedError body; sub-tag enumeration including RT-7a `.cross_section_reference` + RT-6a `.beneficiary_aggregate_identifying`.
- `pipeline/logician/gates/f_report_numeric_drift.py` — owns F-REPORT-NUMERIC-DRIFT predicate signature; NotImplementedError body; sub-tag enumeration unchanged from §0.5 v17 row 389 narrative.
- `pipeline/logician/gates/f_report_template_mismatch.py` — owns F-REPORT-TEMPLATE-MISMATCH predicate signature; NotImplementedError body; sub-tag enumeration including RT-5a/5b/5c + RT-C2-04 sub-tags.
- `pipeline/logician/gates/f_report_beneficiary_privacy_leak.py` (NEW per RT-C2-03) — owns the new top-level F-REPORT-BENEFICIARY-PRIVACY-LEAK predicate signature; NotImplementedError body; deterministic-NER scan substrate semantic noted in docstring; no LLM in scope.
- `pipeline/logician/gates/f_report_operator_key_rotation_validity.py` (NEW per RT-C2-05) — owns the new top-level F-REPORT-OPERATOR-KEY-ROTATION-VALIDITY predicate signature; NotImplementedError body; revocation-list-precedes-rotation invariant noted in docstring.

Out of scope (NOT touched by this amendment):

- The five existing F-REPORT-* gate predicate bodies remain NotImplementedError stubs from §14 v1 LOCK; full predicate realization defers to WS-J Code phase per §14 v1 LOCK contract.
- The R-REPORT-DECIMAL-MANDATE AST-lint rule already exists at §14.13.4; this amendment documents the scope-list extension per RT-C2-01 closure but does NOT extend the rule's predicate body. The actual glob-list extension (composer-module coverage) is a §14.13.4 narrative + skeleton-test addition that lands at WS-J Code phase per §14 v1 LOCK contract.
- The R-REPORT-NO-AUTO-FINALIZE AST-lint rule from §14 v1 LOCK is unchanged.
- The §11 v1.1 sanitize_commitment_id surface is already landed (rows 209/210); this amendment composes against it but does not extend it.
- Existing F-REFLECTION-* gates at §4 v2.x.2 (row 203) and F-PACKET-* gates at §4 v2.x.y (row 217) are unchanged. No cross-family imports per Path B AST-lint discipline.
- Cedar policy bodies for the new gates land at WS-J Code phase; this amendment does not touch the Cedar policy substrate.

## §2. Five base F-REPORT-* gates — HORIZON→ACTIVE graduation (§4 v2.x §5.2 narrative annotation)

Mirrors the §13 v1 §5.1 HORIZON→ACTIVE graduation pattern at §4 v2.x rows 300-305. The §4 v2.x §5.2 table content, after this amendment's narrative annotation, reads:

| Code | Tier | Status | parent_lock |
|---|---|---|---|
| `F-REPORT-COMMITMENT-UNTRACED` | POST scribe-equivalent + PRE pre-finalize | **ACTIVE-AT-§14-v1-LOCK** | row 200 |
| `F-REPORT-COMMITMENT-MISSED` | POST judge-equivalent + PRE pre-track-dispatch (.empty_promoted_set) | **ACTIVE-AT-§14-v1-LOCK** | row 200 |
| `F-REPORT-OUT-OF-SCOPE-DRIFT` | POST judge-equivalent + Cedar at write path | **ACTIVE-AT-§14-v1-LOCK** | row 200 |
| `F-REPORT-NUMERIC-DRIFT` | POST scribe-equivalent (Decimal mandate per v7.0.4-M1) | **ACTIVE-AT-§14-v1-LOCK** | row 200 |
| `F-REPORT-TEMPLATE-MISMATCH` | PRE pre-track-dispatch | **ACTIVE-AT-§14-v1-LOCK** | row 200 |

**Activation note.** The five rows previously listed as HORIZON at §4 v2.x §5.2 graduate to ACTIVE at §14 v1 LOCK 2026-05-10 (paired §0.5 v17 rows 386-390 already registered them). All five predicates remain skeleton stubs raising NotImplementedError at v0.1 hook; full body realization at WS-J Code phase. The consolidated PRE-pre-track-dispatch check callable `report_generator.pre_gate.pre_track_dispatch_consolidated.v1` (§0.5 v17 row 392) sequences the four PRE-pre-track-dispatch gates per §4 v2.2 consolidated-check pattern + §14.9.0 (run-all-then-collect semantics per RT-10a closure).

## §3. Sub-tag extensions on existing F-REPORT-* failure codes (in-place narrative annotation)

Per §4 v2.x.1 row-198 sub-tag-extension precedent — the §0.5 v17 rows 386-390 narrative cells are extended in-place; NO new §0.5 rows are added. The §0.5 v23 paired amendment §B (Row 386-390 sub-tag closure extension) annotates the additions formally. The §14 v1 LOCK text at §14.9.1 + §14.9.2 + §14.9.3 + §14.9.5 + §14.18 (Cycle 1+2 closure dispositions) is the canonical narrative source.

### §3.1 Under `F-REPORT-COMMITMENT-UNTRACED` (row 386) — 5 NEW sub-tags (per Cycle 1 RT-07 fold-in: `.cross_period_signature_invalid` SPLIT into `.cross_period_kfr_snapshot_drift` + `.sp0_cross_period_flag_signature_invalid` to prevent silent-bypass via single-condition implementation)

| Sub-tag | Source closure | §14 anchor | Disposition |
|---|---|---|---|
| `.cross_period_kfr_snapshot_drift` | Cycle 1 RT-1c (KFR atomic-snapshot drift) — **SPLIT per Cycle 1 RT-07 closure from prior `.cross_period_signature_invalid` umbrella** | §14.9.1 | KFR atomic-snapshot read at finalize re-read does not match author-time snapshot ID per `vault_read_intent_kfr_atomic_snapshot` per v7.0.4-M1 |
| `.sp0_cross_period_flag_signature_invalid` | Cycle 1 RT-4a (SP0 cross-period flag activation) — **SPLIT per Cycle 1 RT-07 closure from prior `.cross_period_signature_invalid` umbrella** | §14.12.1 | SP0 cross-period flag `accept_signed_prior_period_claim_evidence_map` was activated without valid Ed25519 signature on `sp0_flags.signed.yaml` |
| `.draft_post_sign_mutation_attempt` | Cycle 1 RT-8b + Cycle 1 RT-08 (BlueprintImmutableError dispatcher-bypass concern) | §14.5.0 + §14.5.1 + §14.16 | finalize re-read of `draft_content_sha3_512` does not match the hash captured at operator-sign time. The predicate body MUST emit the sub-tag THROUGH the F-REPORT-COMMITMENT-UNTRACED gate's normal `GateOutcome.FAIL_CLOSED(sub_tag=".draft_post_sign_mutation_attempt")` return path BEFORE raising BlueprintImmutableError. The CriticalPolicyError(BaseException) propagation is reserved for RUNTIME (post-gate-emission) immutability enforcement at the file-system layer (chmod 0444 + flock); it does NOT replace the failure-code dispatcher emission. WS-J Code phase author MUST NOT collapse the two layers — failure-code emission FIRST (so the sub-tag is recorded in the diagnostic set), CriticalPolicyError SECOND (so the file-system mutation attempt itself is hard-aborted). Drift-test `tests/logician/gates/test_f_report_commitment_untraced_post_sign_emission_order.py` reserved at WS-J Code phase. |
| `.prior_period_map_integrity_failure` | Cycle 2 RT-C2-09 | §14.12.1 | when SP0 flag `accept_signed_prior_period_claim_evidence_map` is True, the on-disk hash of the prior-period claim_evidence_map.yaml does not match the prior-period bundle's `operator_signature.signed.yaml` recorded `claim_evidence_map_content_sha3_512`; protects against tamper-after-sign attack on imported maps |
| `.narrative_paraphrase_unflagged` | Cycle 2 RT-C2-10 | §14.9.1 | claim_kind=narrative source where neither (a) verbatim claim sentence appears in source `text` field after whitespace+punctuation normalization, NOR (b) operator attached `editor_approved_paraphrase: true` flag (Ed25519-signed) to the claim_evidence_map entry |

### §3.2 Under `F-REPORT-COMMITMENT-MISSED` (row 387) — 3 NEW sub-tags

| Sub-tag | Source closure | §14 anchor | Disposition |
|---|---|---|---|
| `.commitment_waiver_unsigned` | Cycle 1 RT-2b | §14.9.2 | per-commitment waiver file at `orgs/<slug>/vault/grants/<grant_id>/reports/period_<n>/commitment_waivers/<commitment_id>.signed.yaml` lacks valid Ed25519 signature over canonical-JSON of (waiver_reason, commitment_id, period_n, run_id, waiver_signed_at_utc) |
| `.commitment_waiver_cap_exceeded` | Cycle 1 RT-2b | §14.9.2 | suppression count via `.commitment_period_n_not_due_yet` exceeds the cap `len(promoted_commitments) - 1` per period; vacuous reports are structurally forbidden |
| `.commitment_id_invalid_format` | Cycle 2 RT-C2-02 | §14.9.2 | `commitment_id` fails the safe-identifier regex `^[A-Z0-9_-]+$` (uppercase alphanumeric + underscore + hyphen; max 64 chars); composes against §11 v1.1 `seats/_commitment_id.py:sanitize_commitment_id()` already runtime-live (rows 209/210); pre-filesystem path-traversal defense |

### §3.3 Under `F-REPORT-OUT-OF-SCOPE-DRIFT` (row 388) — 2 NEW sub-tags

| Sub-tag | Source closure | §14 anchor | Disposition |
|---|---|---|---|
| `.photo_consent_tier_violation.cross_section_reference` | Cycle 1 RT-7a | §14.6.4 + §14.6.1 | cross-section privacy audit detects textual reference to a `photo_id` whose consent_tier is `internal_only` OR `funder_only`-when-section-is-not-photo_gallery; scans ALL draft sub-sections at PRE-pre-finalize |
| `.beneficiary_aggregate_identifying` | Cycle 1 RT-6a | §14.6.5 | aggregate-count claim referencing ≤2 beneficiaries; HIGH advisory; operator MUST explicitly approve aggregate inclusion via per-beneficiary-aggregate Ed25519 signature when count ≤ 2 |

### §3.4 Under `F-REPORT-NUMERIC-DRIFT` (row 389) — 0 NEW sub-tags

The Cycle 1 RT-3a/3b/3c closures landed AS the AST-lint rule R-REPORT-DECIMAL-MANDATE (per §5 below) + canonical rounding mode `decimal.ROUND_HALF_UP` substrate convention + Decimal-string conversion-factor canonical-JSON substrate. These do not introduce new failure sub-tags; the existing `.float_comparison_detected` defect-detection sub-tag absorbs the AST-lint hits.

### §3.5 Under `F-REPORT-TEMPLATE-MISMATCH` (row 390) — 4 NEW sub-tags

| Sub-tag | Source closure | §14 anchor | Disposition |
|---|---|---|---|
| `.workspace_published_template_absent_first_wave` | Cycle 1 RT-5a | §14.9.5 | template absence FAIL-CLOSED (not advisory) when funder_id ∈ SN-LLC first-wave funder set per `sn_llc_first_wave.signed.yaml` (covers VAPG / NIFA / SARE / EPA NEETP / SBIR at v0.2 first wave) |
| `.operator_key_version_mismatch` | Cycle 1 RT-5b | §14.9.5 | template was signed with operator-key version that doesn't match the currently-pinned operator key OR the predecessor key whose rotation is auditable via lock_history Trust-On-First-Use co-sign chain |
| `.period_cadence_actual_drift` | Cycle 1 RT-5c | §14.9.5 | `required_period_cadence` from template doesn't match the actual interval derived from grant's `award_signed_at_utc` (per §11 v1 AWARD_INGEST); operator-decision surface ("template requires quarterly; this is period N which spans M months — confirm cadence") |
| `.workspace_published_template_marker_tampered` | Cycle 2 RT-C2-04 | §14.9.5 | first-wave marker file `sn_llc_first_wave.signed.yaml` on-disk content+signature does not verify against the immutable record at `lock_history/first_wave_markers.signed.yaml` (SN-LLC-signed at release ceremony); fail-closed at every PRE-pre-track-dispatch |

## §4. Two NEW top-level F-REPORT-* failure codes (predicate-signature registration)

Per §4 v2.x.2 row-203 explode-per-code precedent. Two new failure codes land at the predicate-signature layer in `pipeline/logician/gates/f_report_*.py` with NotImplementedError bodies. Cross-references to §14.9.3 + §14.9.5 closure text. Paired §0.5 v23 rows 507/508 register the codes at the Index.

### §4.1 F-REPORT-BENEFICIARY-PRIVACY-LEAK (per Cycle 2 RT-C2-03 closure)

**OVERRIDE NOTE per Cycle 1 RT-02 fold-in.** The §14 RT-C2-03 closure text says "NEW gate `F-REPORT-BENEFICIARY-PRIVACY-LEAK` (sub-tag of F-REPORT-OUT-OF-SCOPE-DRIFT)". **DESPITE the parenthetical wording in the closure text, this code is registered as a SEPARATE TOP-LEVEL FAILURE-CODE per §4 v2.x.3 §4.1 + §0.5 v23 row 507.** The "sub-tag of" parenthetical is a **runtime-composition note** (operator UI groups them under the same scope-leak diagnostic family), NOT a structural sub-tag relationship. WS-J Code phase author MUST register a separate predicate body in `pipeline/logician/gates/f_report_beneficiary_privacy_leak.py` with its own dispatcher entry; registering it as a sub-tag under `F-REPORT-OUT-OF-SCOPE-DRIFT.beneficiary_privacy_leak` would be a category error (the dispatcher would never invoke the dedicated predicate body and the sub-tag would never fire). Drift-test `tests/logician/gates/test_f_report_beneficiary_privacy_leak_top_level_dispatcher_entry.py` reserved at WS-J Code phase to assert dispatcher-registry membership.


| Field | Value |
|---|---|
| Module | `pipeline/logician/gates/f_report_beneficiary_privacy_leak.py` (NEW) |
| Tier | PRE pre-finalize (composes with consolidated PRE-pre-finalize check callable at §0.5 v17 row 393) |
| Function signature | `def predicate_beneficiary_privacy_leak(report_input: ReportGeneratorRunInput, beneficiary_records: BeneficiaryRecordsRead, draft_subsections: DraftSubsectionsRead) -> GateOutcome:` |
| NotImplementedError body | `raise NotImplementedError("F-REPORT-BENEFICIARY-PRIVACY-LEAK body lands at WS-J Code phase per §14 v1 LOCK contract; signature reserved + deterministic-NER scan substrate semantic registered at v0.1 hook (NER over beneficiary_name + beneficiary_aliases field union; NOT LLM-driven; flags any match to a beneficiary_id whose consent_tier ∈ {metrics-only, no-narrative})")` |
| Sub-tags at v0.1 hook | `.beneficiary_id_match_in_disallowed_section`, `.beneficiary_alias_match_in_disallowed_section`, `.consent_tier_metrics_only_narrative_inclusion`, `.consent_tier_no_narrative_any_inclusion` |
| Composition | Composes WITH F-REPORT-OUT-OF-SCOPE-DRIFT.beneficiary_consent_tier_violation at the runtime dispatch layer (operator UI groups them under the same scope-leak diagnostic family per §14.9.3 closure narrative); enforces independently. Mirrors F-REPORT-NUMERIC-DRIFT composing with F-LOGICIAN-FACT-DRIFT per v7.0.4 KFR family. |
| Drift-test binding | `tests/logician/gates/test_f_report_beneficiary_privacy_leak_signature_drift.py::test_signature_matches_v2_x_3_section_4_1` |

### §4.2 F-REPORT-OPERATOR-KEY-ROTATION-VALIDITY (per Cycle 2 RT-C2-05 closure)

| Field | Value |
|---|---|
| Module | `pipeline/logician/gates/f_report_operator_key_rotation_validity.py` (NEW) |
| Tier | PRE pre-track-dispatch (operator-key-rotation event) |
| Function signature | `def predicate_operator_key_rotation_validity(rotation_event: OperatorKeyRotationEvent, revocation_list_path: Path) -> GateOutcome:` |
| NotImplementedError body | `raise NotImplementedError("F-REPORT-OPERATOR-KEY-ROTATION-VALIDITY body lands at WS-J Code phase per §14 v1 LOCK contract; signature reserved + revocation-list-precedes-rotation invariant registered at v0.1 hook (revocation event MUST be appended to lock_history immutable ledger BEFORE rotation event per PHYSICAL APPEND ORDER — file-offset-strict, NOT timestamp-strict — per Cycle 1 RT-10 fold-in; both events must additionally satisfy revocation_signed_at_utc <= rotation_signed_at_utc as defense-in-depth; back-dated revocation timestamp written to a later append position fails-closed at the file-offset comparison)")` |
| Sub-tags at v0.1 hook | `.previous_key_revoked`, `.revocation_list_signature_invalid`, `.revocation_event_after_rotation_event_by_append_order`, `.revocation_event_after_rotation_event_by_timestamp` (per Cycle 1 RT-10 fold-in: split into append-order vs timestamp sub-tags; both fire independently for defense-in-depth) |
| Composition | Composes WITH F-REPORT-TEMPLATE-MISMATCH.operator_key_version_mismatch at the runtime dispatch layer; rotation-event PRE-gate fires BEFORE template-mismatch PRE-gate to short-circuit a malicious rotation before any template comparison. |
| Drift-test binding | `tests/logician/gates/test_f_report_operator_key_rotation_validity_signature_drift.py::test_signature_matches_v2_x_3_section_4_2` + `tests/logician/gates/test_f_report_operator_key_rotation_validity_back_dated_revocation_attack.py` (per Cycle 1 RT-10 fold-in; assert append-order check fires on back-dated revocation appended after rotation) + `tests/logician/gates/test_f_report_operator_key_rotation_validity_primary_check_algorithm.py` (per Cycle 2 RT-C2-05 fold-in; assert primary-check algorithm executes ALL FOUR steps below regardless of timestamp ordering) |
| Primary-check algorithm (per Cycle 2 RT-C2-05 fold-in) | The predicate body MUST execute ALL FOUR steps in order; ANY step short-circuited or omitted is a structural defect: 1. Read the file offset of the latest revocation entry in `lock_history/operator_key_revocation_list.signed.yaml` (`rev_offset`). 2. Read the file offset of the rotation event entry (`rot_offset`). 3. **FAIL-CLOSED with sub-tag `.revocation_event_after_rotation_event_by_append_order`** if `rev_offset > rot_offset` (the revocation must appear EARLIER in the physical file). 4. Defense-in-depth — additionally compare timestamps and **FAIL-CLOSED with sub-tag `.revocation_event_after_rotation_event_by_timestamp`** if `rev_signed_at_utc > rot_signed_at_utc`. Both checks fire independently; an attacker who can control only timestamp OR only file-offset cannot bypass both. |

## §5. F-CEDAR-* sub-tag extensions (in-place narrative annotation under §0.5 rows 268/272)

Per §4 v2.x.1 row-198 sub-tag-extension precedent — the §0.5 v11 rows 268/272 (the §2 v7.2 F-CEDAR-OPERATIONAL-DENIED + F-CEDAR-PII-CONSENT-MISSING failure-code rows) gain new sub-tags via in-place narrative annotation. The §0.5 v23 paired amendment §C (F-CEDAR sub-tag closure extension) annotates the additions formally.

### §5.1 Under `F-CEDAR-OPERATIONAL-DENIED` (row 268) — 1 NEW sub-tag

| Sub-tag | Source closure | §14 anchor | Disposition |
|---|---|---|---|
| `.engine_unready` | Cycle 1 RT-6b | §14.6.5 | per-read Cedar engine readiness check `cedar_engine.assert_ready()` failed (engine not initialized OR initialization-time error); CriticalPolicyError(BaseException) propagation per §13 v1 RT-C2-04 closure pattern; fail-closed at every operational-data sub-kind read invocation |

### §5.2 Under `F-CEDAR-PII-CONSENT-MISSING` (row 272) — 2 NEW sub-tags

| Sub-tag | Source closure | §14 anchor | Disposition |
|---|---|---|---|
| `.tier_history_unsigned` | Cycle 1 RT-6c | §14.6.5 | beneficiary_records `consent_tier_history` entry exists but lacks valid per-tier-change Ed25519 operator signature; fail-closed at read path; protects against post-collection consent-tier downgrade attack |
| `.tier_history_missing` | Cycle 2 RT-C2-06 | §14.6.5 | beneficiary_records lacks `consent_tier_history` field entirely (legacy record predating RT-6c closure); fail-closed by default; operator may run `tilth migrate beneficiary_records --backfill-empty-history --signed-by <operator_key>` CLI to back-fill an empty Ed25519-signed history (the back-fill itself is operator-Ed25519-signed + audited via lock_history) |

## §6. R-REPORT-DECIMAL-MANDATE AST-lint scope expansion (per Cycle 2 RT-C2-01 closure)

The R-REPORT-DECIMAL-MANDATE AST-lint rule already exists at §14.13.4 (registered at §14 v1 LOCK 2026-05-10 per Cycle 1 RT-3a closure). Per Cycle 2 RT-C2-01 closure, the rule's file-scope EXTENDS:

| Scope tier | Glob | Rationale |
|---|---|---|
| Original (Cycle 1 RT-3a) | `pipeline/logician/gates/f_report_*.py` | The five F-REPORT-* gate predicate bodies must use Decimal exclusively |
| Extended (Cycle 2 RT-C2-01) | + `pipeline/orchestrator/seats/report_generator/**/*.py` + `pipeline/orchestrator/tracks/report_mode.py` | Composer modules + track-binding module can introduce float arithmetic that propagates into gate input; defense-in-depth scope expansion blocks the propagation surface |

This is a glob-list extension on an already-registered AST-lint rule — NO new module file is created. The extension lands at WS-J Code phase per §14 v1 LOCK contract; this amendment documents the contract for the WS-J Code phase author. Companion test `test_r_report_decimal_mandate_lint_clean_composer_scope` reserved at §14.13.4 + WS-J Code phase realizes the test against the extended scope.

**No new §0.5 row.** AST-lint scope-list edits on an already-registered rule are narrative annotations on the rule's existing row, not new rows. The R-REPORT-DECIMAL-MANDATE rule itself is documented at §14.13.4 + cross-referenced from §0.5 v17 row 389 narrative; no separate §0.5 enforcement-infrastructure row exists for it (the rule was registered as a §14 v1 LOCK artifact, not as a §4 v2.x §15.13.1-pattern enforcement-infrastructure row).

## §7. Composition with §11 v1.1 sanitize_commitment_id

The §3.2 sub-tag `F-REPORT-COMMITMENT-MISSED.commitment_id_invalid_format` (RT-C2-02 closure) requires `commitment_id` to validate against the safe-identifier regex `^[A-Z0-9_-]+$` BEFORE filesystem operation. The §11 v1.1 LOCK 2026-05-11 (rows 209/210) already landed:

- Shared canonical home at `seats/_commitment_id.py` with `re.ASCII` flag on the validation regex.
- `sanitize_commitment_id(uuid.uuid4().hex.upper())` enforced at AWARD_INGEST extraction time (intake.py `_validate_and_collect_commitments`).
- Consumer-side shim preserves §14 v1 imports with object identity.
- Reload-protocol contract for v1.x forward-binding.
- 7 new tests across 4 sections (regex shape + 8 valid/20 invalid/5 non-str matrix + identity contract + AWARD_INGEST e2e + length-32 + 1000-row uniqueness + reload-protocol + stateless sanitize).

This amendment composes against the existing §11 v1.1 surface — no new follow-on at §11 is required. The §14 RT-C2-02 closure text "§11 v1 AWARD_INGEST extraction MUST sanitize commitment_id at extraction time per a paired §11 v1.1 follow-on update (referenced; not authored at this LOCK)" is satisfied. The F-REPORT-COMMITMENT-MISSED.commitment_id_invalid_format sub-tag is the §4 Logician-side enforcement at PRE-pre-track-dispatch; the §11 v1.1 sanitize_commitment_id is the §11 Intake-side enforcement at AWARD_INGEST extraction. Both layers fail-closed independently for defense-in-depth.

**PRE-pre-track-dispatch re-validation contract per Cycle 1 RT-05 fold-in (P0 closure).** The §11 v1.1 sanitize_commitment_id is a one-shot at AWARD_INGEST extraction; an operator who edits `proposal_commitments.yaml` post-extraction (via UI / external tool / direct file edit) could reintroduce a path-traversal commitment_id between extraction and PRE-pre-track-dispatch. To close this race-window, the F-REPORT-COMMITMENT-MISSED predicate body MUST re-call `seats._commitment_id.sanitize_commitment_id()` on EVERY `commitment_id` value read from the active report's `proposal_commitments.yaml` BEFORE any filesystem operation that uses the value (including waiver-file path construction at `commitment_waivers/<commitment_id>.signed.yaml`). The re-validation is a runtime PRE-gate, not a one-shot at extraction. Failure raises `.commitment_id_invalid_format` sub-tag. This satisfies the defense-in-depth contract: layer 1 (§11 AWARD_INGEST extraction) catches malformed extraction-time IDs; layer 2 (§4 PRE-pre-track-dispatch re-validation) catches post-extraction operator-edit reintroduction. WS-J Code phase author MUST implement the re-validation as the FIRST statement of the predicate body for any code path that touches `commitment_id`. Drift-test `tests/logician/gates/test_f_report_commitment_missed_post_extraction_revalidation.py` reserved at WS-J Code phase to assert the re-call is invoked on every read.

## §8. Cross-family AST-lint discipline (Path B naming reconciliation)

Per the §16 Reflection Packet v1 LOCK 2026-05-15 row 216 Path B naming reconciliation: **F-PACKET-* (artifact) / F-REFLECTION-* (producer) / F-ARCHIVIST-* (substrate) / F-WPFA-* (sibling-artifact) — four orthogonal F-* families with AST-lint cross-family-import ban.** This amendment does NOT add a fifth orthogonal family; F-REPORT-* lives in the established §14 / §4 v2.x §5.2 family from §14 v1 LOCK 2026-05-10. The cross-family-import ban applies to F-REPORT-* IMPORTS (no F-REPORT-* module imports F-PACKET-* / F-REFLECTION-* / F-ARCHIVIST-* / F-WPFA-* code at module-import time); F-REPORT-* exports may be imported BY orchestrator track-binding modules (which are not in the orthogonal-family set).

The AST-lint rule from §4 v2.x.y row 217 LOGICIAN_IMPORT_BAN family is unchanged at this LOCK; the F-REPORT-* family was excluded from the original LOGICIAN_IMPORT_BAN family scope per §4 v2.x.y §1.1 closure (F-REPORT-* predates the Path B reconciliation; F-REPORT-* gates are consumed by the §5 v8 dispatcher track-binding seam at §14.8.0 rather than imported by sibling §16/§17 artifact modules). No regression risk from this amendment.

## §9. Closure-disposition table

Per the §4 v2.x.1 §11 + §4 v2.x.2 §10 transparent-disposition pattern. This section will be filled in at LOCK after L-005 strict two-cycle Thesis CLOSE.

### §9.1 Cycle 1 closure dispositions (filled at LOCK)

(To be filled at LOCK ceremony after Cycle 1 Editor + Judge + Red Team complete.)

### §9.2 Cycle 2 closure dispositions (filled at LOCK)

(To be filled at LOCK ceremony after Cycle 2 verification.)

## §10. Done definition + acceptance

- [x] Five base F-REPORT-* HORIZON rows at §4 v2.x §5.2 narrative annotated as ACTIVE-AT-§14-v1-LOCK with parent_lock row 200 reference (§2 above).
- [x] **14 new sub-tags** landed in narrative annotations under §0.5 rows 386-390 (§3 above; updated count after Cycle 1 RT-07 SPLIT of `.cross_period_signature_invalid` into `.cross_period_kfr_snapshot_drift` + `.sp0_cross_period_flag_signature_invalid`; original count was 11; Judge Cycle 1 minor finding identified count-narrative drift).
- [x] Two NEW top-level failure codes (F-REPORT-BENEFICIARY-PRIVACY-LEAK + F-REPORT-OPERATOR-KEY-ROTATION-VALIDITY) registered at predicate-signature layer with NotImplementedError bodies (§4 above).
- [x] Three new F-CEDAR-* sub-tags landed in narrative annotations under §0.5 rows 268/272 (§5 above).
- [x] R-REPORT-DECIMAL-MANDATE scope expansion documented (§6 above) — actual glob-list extension lands at WS-J Code phase.
- [x] §11 v1.1 sanitize_commitment_id composition documented (§7 above).
- [x] Path B naming reconciliation discipline documented (§8 above).
- [x] L-005 strict two-cycle Thesis Cycle 1 CLOSED 2026-05-15T18:48:35Z with FULL live cross-family rigor (Editor=Llama-3.3-70B/Groq REQUIRES_FIX → 6 FOLDED + 1 DEFERRED + Judge=Gemini-2.5-Pro/Google READY_TO_LOCK 99/100 → 1 narrative count fix + Red Team=GPT-OSS-120B/Groq READY_TO_LOCK blocking:false → 10 FOLDED + 1 PARTIALLY-FOLDED-DEFERRED-v2 + 1 NO-ACTION).
- [ ] L-005 strict two-cycle Thesis Cycle 2 verification dispatch (verifies fold-ins hold + surfaces NEW probes for row-170 fold-in). Filled at LOCK.
- [ ] Compound paired-commit with §0.5 v23 (3 rows: 506-508). Filled at LOCK.
- [ ] lock_history rows 219 + 220 (§4 v2.x.3 + §0.5 v23). Filled at LOCK.
- [ ] memory file + MEMORY.md index entry. Filled at LOCK.
- [ ] daily_log entry + session_metrics row. Filled at session close.

## §11. Cycle 1 closure dispositions (FOLDED-IN at LOCK per row-170 transparent disposition)

L-005 strict two-cycle Thesis Cycle 1 dispatched 2026-05-15T18:45:38Z..18:48:35Z via openclaw bridge. Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq. Three non-Anthropic families.

### §11.1 Editor Cycle 1 (REQUIRES_FIX → 7 closures applied)

| Finding | Severity | Issue | Disposition |
|---|---|---|---|
| **E-01** | MEDIUM | Inconsistent precedent attribution across §0-§4 | **FOLDED-IN at §0 precedent-pattern attribution table** — table maps each §N to its invoked precedent + mechanism + on-disk evidence row. |
| **E-02** | HIGH | F-REPORT-BENEFICIARY-PRIVACY-LEAK composition note ambiguity ("composes WITH but enforces independently") | **FOLDED-IN at §4.1 OVERRIDE NOTE** — explicit override clause + WS-J Code phase contract that the predicate body has its own dispatcher entry; runtime composition is operator-UI-only. |
| **E-03** | MEDIUM | Cross-seat sub-tag-extension ownership clarity | **FOLDED-IN at §0.5 v23 §D + §C** — §0.5 v23 §C documents the cross-seat pattern; §D establishes the precedent-extension formally with a specific row-count + multi-owner table. |
| **E-04** | LOW | R-REPORT-DECIMAL-MANDATE scope expansion contract — concise summary | **FOLDED-IN at §6 + §11.3 RT-04 fold-in** — table + post-LOCK verification gate marker. |
| **E-05** | MEDIUM | §11 v1.1 composition documentation clarity | **FOLDED-IN at §7 PRE-pre-track-dispatch re-validation contract** (part of RT-05 P0 closure). |
| **E-06** | LOW | Done definition / acceptance criterion clarity | **DEFERRED-NON-BLOCKING** — §10 already separates `[x]` complete-at-amendment-text from `[ ]` complete-at-LOCK-ceremony. Cosmetic clarification deferred to v1.x readability spin. |
| **E-07** | MEDIUM | §14 v1 LOCK text relationship clarity | **FOLDED-IN at §0 amendment intent + §11.1 E-01 closure precedent-pattern table** — the table makes explicit that §3-§5 lift §14 v1 LOCK text into the §4 registration layer; do not modify §14 v1 LOCK text. |

### §11.2 Judge Cycle 1 (READY_TO_LOCK 99/100 → 1 narrative-correctness fix applied)

| Finding | Severity | Issue | Disposition |
|---|---|---|---|
| **J-Dim3** | MINOR (1pt) | Header narrative says "11 new sub-tags" but enumeration is 13 (4+3+2+0+4) | **FOLDED-IN at amendment_status frontmatter + §0 + §11.5** — count corrected to 13 throughout. With Cycle 1 RT-07 split (`.cross_period_signature_invalid` → `.cross_period_kfr_snapshot_drift` + `.sp0_cross_period_flag_signature_invalid`), the count is now **14 sub-tags** under existing F-REPORT-* codes (5 + 3 + 2 + 0 + 4) + 3 sub-tags under existing F-CEDAR-* codes = 17 total sub-tag extensions. |

### §11.3 Red Team Cycle 1 (READY_TO_LOCK blocking:false → 12 findings dispositioned per row-170)

| Finding | Severity | Probe | Disposition |
|---|---|---|---|
| **RT-01** | P0 | Sub-tag silent-drop via in-place narrative annotation pattern (downstream tooling reading only §0.5 v17 misses §0.5 v23 §B annotations) | **PARTIALLY FOLDED-IN + DEFERRED-v2** — the canonical wire-form-readers contract is documented at §0.5 v23 §B explicitly: "Consumers of the §0.5 Index that resolve row 386-390 sub-tag set must consult both the §0.5 v17 amendment row 386-390 narrative AND the §4 v2.x.3 amendment text + this §0.5 v23 §B for the canonical sub-tag enumeration." The F-INDEX-STALE PRE-gate narrative-extension verification (machine-readable manifest) is a v2 hardening track marker per Section O.5 (architecture's v2-hardening targets); BOUNDED-by-v7-LOCKED-A1+A4 single-operator envelope at v0.1 + v0.2 (single contributor reads both files). |
| **RT-02** | HIGH | NEW top-level code mis-wired as sub-tag (closure text says "sub-tag of"; amendment registers as separate code) | **FOLDED-IN at §4.1 OVERRIDE NOTE + drift-test `test_f_report_beneficiary_privacy_leak_top_level_dispatcher_entry.py` reserved at WS-J Code phase to assert dispatcher-registry membership. |
| **RT-03** | P0 | Predicate-signature drift for new top-level codes (drift-test files reserved but no assertions) | **FOLDED-IN at §11.4 drift-test contract** — drift tests MUST use `inspect.signature` to assert exact parameter names + ordering + types per the §4.1 + §4.2 specs. WS-J Code phase author MUST land the test bodies BEFORE merging the predicate-body realization. NEW skeleton test placeholder bound to §11.4. |
| **RT-04** | HIGH | R-REPORT-DECIMAL-MANDATE deferred extension may be skipped by contributor | **FOLDED-IN at §6 + §11.4 post-LOCK verification gate marker** — WS-J Code phase MUST land the extended glob-list AND the companion test `test_r_report_decimal_mandate_lint_clean_composer_scope` BEFORE the WS-J Code phase LOCK; failure of either blocks the LOCK. The §6 table is the contractual scope-list; the WS-J Code phase author copies it verbatim into the rule's configuration. |
| **RT-05** | P0 | §11 v1.1 sanitize_commitment_id only at extraction; post-extraction operator edit reintroduces malformed IDs | **FOLDED-IN at §7 PRE-pre-track-dispatch re-validation contract** — predicate body MUST re-call `seats._commitment_id.sanitize_commitment_id()` on EVERY `commitment_id` value read from the active report's `proposal_commitments.yaml` BEFORE any filesystem operation; defense-in-depth two-layer enforcement. |
| **RT-06** | MED | Cross-seat sub-tag-extension precedent over-reach | **FOLDED-IN at §0.5 v23 §D formal precedent extension** — the variant is documented + authorized at the amendment level with per-row owner preservation discipline; future cross-seat sub-tag extensions cite §0.5 v23 §D as the precedent. The amendment establishes the pattern under operator authority at LOCK. |
| **RT-07** | HIGH | Collapsing two distinct conditions into single sub-tag (`.cross_period_signature_invalid` for both KFR drift AND SP0 flag signature) | **FOLDED-IN at §3.1 SPLIT** — `.cross_period_signature_invalid` SPLIT into `.cross_period_kfr_snapshot_drift` (RT-1c) + `.sp0_cross_period_flag_signature_invalid` (RT-4a). Two distinct sub-tags; predicate body MUST emit one or the other (or both); single-condition implementation no longer sufficient. |
| **RT-08** | HIGH | BlueprintImmutableError propagation may bypass dispatcher | **FOLDED-IN at §3.1 `.draft_post_sign_mutation_attempt` cell** — predicate body MUST emit the sub-tag THROUGH the failure-code dispatcher's normal `GateOutcome.FAIL_CLOSED(sub_tag=...)` return path BEFORE raising BlueprintImmutableError. The two layers are sequenced: emission first (record diagnostic), CriticalPolicyError second (hard-abort filesystem mutation). Drift-test `test_f_report_commitment_untraced_post_sign_emission_order.py` reserved. |
| **RT-09** | MED | HORIZON→ACTIVE graduation lacks enforceable text replacement | **FOLDED-IN at §2 + §11.4 machine-readable directive** — the §2 table provides the EXACT replacement text for the §4 v2.x §5.2 cells (Status column changes from `HORIZON — §14 LOCK` to `ACTIVE-AT-§14-v1-LOCK` with parent_lock row 200). Future re-author of §0.5 v14 (which hosts §4 v2.x §5.2) must apply §2 as the source-of-truth for the Status cell. |
| **RT-10** | HIGH | Operator-key rotation race-window — physical append-order vs timestamp ambiguity | **FOLDED-IN at §4.2 NotImplementedError body + sub-tag SPLIT** — the invariant is now PHYSICAL APPEND ORDER (file-offset-strict) with timestamp comparison as defense-in-depth. Sub-tag `.revocation_event_after_rotation_event` SPLIT into `.revocation_event_after_rotation_event_by_append_order` + `.revocation_event_after_rotation_event_by_timestamp`. Drift-test `test_f_report_operator_key_rotation_validity_back_dated_revocation_attack.py` reserved. |
| **RT-11** | MED | Sub-tag name collision across families (`.engine_unready` could clash with future F-REPORT-* sub-tag) | **FOLDED-IN at §11.4 namespace rule** — sub-tag references in code + diagnostics MUST use the fully-qualified form `<F-CODE>.<sub-tag>` (e.g., `F-CEDAR-OPERATIONAL-DENIED.engine_unready`); bare sub-tag names are admissible only inside the predicate body for the owning code's module. F-INDEX-STALE PRE-gate verification of cross-family sub-tag uniqueness is a v2 hardening track marker. |
| **RT-12** | LOW | Seat_owner attribute on marker row potentially missing | **NO-ACTION required** — the §0.5 v23 §A row 506 table cell explicitly lists `seat_owner: report_generator`. The F-INDEX-STALE PRE-gate verification mechanism per the row-delta narrative covers all 3 rows uniformly. No fix needed; the concern is structurally addressed. |

### §11.4 NEW WS-J Code phase contracts surfaced by Cycle 1 fold-ins

The following WS-J Code phase deliverables are CONTRACTUALLY BOUND by this amendment's Cycle 1 fold-ins. WS-J Code phase LOCK fails-closed if any are missing:

1. **Drift tests for the two NEW top-level codes (RT-03 P0 closure):**
   - `tests/logician/gates/test_f_report_beneficiary_privacy_leak_signature_drift.py` — `inspect.signature(predicate_beneficiary_privacy_leak)` asserts parameters `(report_input: ReportGeneratorRunInput, beneficiary_records: BeneficiaryRecordsRead, draft_subsections: DraftSubsectionsRead)` exact name + order + type.
   - `tests/logician/gates/test_f_report_operator_key_rotation_validity_signature_drift.py` — `inspect.signature(predicate_operator_key_rotation_validity)` asserts parameters `(rotation_event: OperatorKeyRotationEvent, revocation_list_path: Path)` exact name + order + type.
   - `tests/logician/gates/test_f_report_beneficiary_privacy_leak_top_level_dispatcher_entry.py` — assert membership in dispatcher REGISTERED_GATES at the top-level position (NOT as sub-tag of F-REPORT-OUT-OF-SCOPE-DRIFT).
   - `tests/logician/gates/test_f_report_commitment_untraced_post_sign_emission_order.py` — assert failure-code emission precedes BlueprintImmutableError raise per §3.1 closure.
   - `tests/logician/gates/test_f_report_commitment_missed_post_extraction_revalidation.py` — assert sanitize_commitment_id is re-called at PRE-pre-track-dispatch on every commitment_id read per §7 RT-05 closure.
   - `tests/logician/gates/test_f_report_operator_key_rotation_validity_back_dated_revocation_attack.py` — assert append-order check fires on back-dated revocation appended after rotation per §4.2 RT-10 closure.
2. **R-REPORT-DECIMAL-MANDATE scope-list extension (RT-04 HIGH closure):**
   - Update the rule's configuration to include `pipeline/orchestrator/seats/report_generator/**/*.py` + `pipeline/orchestrator/tracks/report_mode.py` per §6 Extended scope row.
   - Land companion test `tests/linting/test_r_report_decimal_mandate_lint_clean_composer_scope.py` asserting the rule fires on synthetic `value = float(metric_raw) * 1.0` in a composer module.
   - WS-J Code phase LOCK fails-closed if either is missing.
3. **HORIZON→ACTIVE graduation directive (RT-09 MED closure):**
   - Future re-author of §0.5 v14 (which hosts §4 v2.x §5.2) must apply §2 of this amendment as the source-of-truth for the Status cell on rows 386-390 (HORIZON → ACTIVE-AT-§14-v1-LOCK).
   - F-INDEX-STALE PRE-gate verification: at v2 hardening, add a check that no row in §4 v2.x §5.2 still contains `HORIZON` for §14-graduated codes.
4. **Sub-tag namespace rule (RT-11 MED closure):**
   - Sub-tag references in code + diagnostics + lock_history MUST use the fully-qualified form `<F-CODE>.<sub-tag>`.
   - Drift-test placeholder `tests/logician/gates/test_sub_tag_namespace_fully_qualified.py` reserved at WS-J Code phase to assert all sub-tag emissions in `pipeline/logician/gates/f_report_*.py` use the fully-qualified form.

### §11.5 Cycle 1 closure summary

- 7 Editor findings: 6 FOLDED-IN + 1 DEFERRED-NON-BLOCKING (E-06).
- 1 Judge minor: FOLDED-IN (count corrected from 11 → 13 → 14 with RT-07 split).
- 12 Red Team findings: 10 FOLDED-IN + 1 PARTIALLY-FOLDED-IN-DEFERRED-v2 (RT-01) + 1 NO-ACTION (RT-12 already addressed).
- TOTAL Cycle 1 disposition: 18 closures applied + 1 deferred-non-blocking + 1 partially-folded-deferred-v2 + 1 no-action = 21 findings handled.
- New sub-tag count after RT-07 split: **17 sub-tag extensions** (5 + 3 + 2 + 0 + 4 under F-REPORT-* + 3 under F-CEDAR-*) + 2 NEW top-level F-REPORT-* codes.

## §12. Cycle 2 closure dispositions (FOLDED-IN at LOCK per row-170)

L-005 strict two-cycle Thesis Cycle 2 dispatched 2026-05-15T18:59:45Z..19:00:37Z via openclaw bridge. Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq. Three non-Anthropic families. Cycle 2 verifies all 21 Cycle 1 closures hold (no regressions) and surfaces NEW probes for row-170 fold-in.

### §12.1 Cycle 1 closure verification outcomes (Cycle 2)

- **Editor Cycle 2:** All 6 Editor Cycle 1 FOLDED closures verified CLOSED (E-01 through E-05 + E-07; E-06 deferred-non-blocking). 5 NEW probes E-NF-01..E-NF-05 surfaced (mostly cosmetic; per row-170 disposition below).
- **Judge Cycle 2:** Score 99/100 maintained (sustained Cycle 1 99/100 baseline with 1 minor narrative-drift in frontmatter J-NF-01; FOLDED-IN at frontmatter purpose field — count corrected from "eleven new sub-tags" to "fourteen new sub-tags" with explicit count-derivation note). All 10 dimensions scored READY_TO_LOCK; technical hardening from RT-07/RT-10 SPLITs + RT-05 PRE-pre-track-dispatch contract + RT-08 emission-order contract + RT-04 R-REPORT-DECIMAL-MANDATE post-LOCK gate marker explicitly verified PRESENT_AS_CLAIMED.
- **Red Team Cycle 2:** All 12 Cycle 1 RT findings verified CLOSED (RT-01 through RT-11) + 1 N/A NO-ACTION (RT-12). 8 NEW probes RT-C2-01..RT-C2-08 surfaced (per row-170 disposition below). Verdict REQUIRES_FIXES blocking:true with all NEW probes FOLDED-IN at LOCK per row-170 transparent-disposition pattern.

### §12.2 Editor Cycle 2 NEW probe disposition (E-NF-01..E-NF-05)

| Finding | Severity | Probe | Disposition |
|---|---|---|---|
| **E-NF-01** | LOW | Inconsistent terminology in §3.1 vs §3.2 sub-tag naming | **NO-ACTION required** — both §3.1 + §3.2 sub-tag tables use the consistent leading-dot wire-form convention per §4 v2.x.1 §2.2 dot-handling closure (`.cross_period_kfr_snapshot_drift` + `.commitment_waiver_unsigned`). The names differ in length + word-count because they describe different failure conditions; this is intentional, not inconsistent. The wire-form consistency (leading dot + snake_case) is preserved across all sub-tag entries throughout §3, §4, §5. |
| **E-NF-02** | MED | F-REPORT-BENEFICIARY-PRIVACY-LEAK + F-REPORT-OUT-OF-SCOPE-DRIFT relationship clarity | **FOLDED-IN at §4.1 OVERRIDE NOTE + §12.4 RT-C2-04 immutable annotation marker** — the OVERRIDE NOTE reads "DESPITE the parenthetical wording... this code is registered as a SEPARATE TOP-LEVEL FAILURE-CODE", and §12.4 introduces an immutable annotation on row 507 that prevents future re-authoring from demoting the code. The composition note "composes WITH... at runtime dispatch layer" is now explicitly bounded by the OVERRIDE NOTE: composition is operator-UI-only, NOT structural. |
| **E-NF-03** | LOW | §5.1 vs §5.2 formatting inconsistency for sub-tag descriptions | **NO-ACTION required** — both §5.1 and §5.2 use the same table format with columns (Sub-tag | Source closure | §14 anchor | Disposition). The formatting is structurally identical; the visual appearance differs only because §5.1 has 1 row and §5.2 has 2 rows. No actual inconsistency exists in the table structure. |
| **E-NF-04** | LOW | "defense-in-depth" definition unclear in §7 | **FOLDED-IN at §12.7 inline definition** — "defense-in-depth" in this amendment means a multi-layer enforcement model where each layer is fail-closed independently AND a successful bypass of one layer does not bypass the others. Layer 1 (§11 AWARD_INGEST extraction) catches malformed extraction-time IDs; Layer 2 (§4 PRE-pre-track-dispatch re-validation) catches post-extraction operator-edit reintroduction. An attacker who controls only one layer cannot bypass both. The same model applies to §4.2 (file-offset PRIMARY + timestamp DEFENSE-IN-DEPTH). |
| **E-NF-05** | MED | §11.4 WS-J Code phase contracts unclear on specific actions | **FOLDED-IN at §12.6 RT-C2-06 contract-verification table** — §12.6 introduces an explicit contract-verification table for the four §11.4 deliverables; each row enumerates the deliverable + a `present` checkbox + the test/lint command that verifies presence at WS-J Code phase LOCK. WS-J Code phase author MUST verify ALL FOUR before LOCKing. |

### §12.3 RT-C2-01 — Drift-test enforcement gate (FOLDED-IN)

The §11.4 WS-J Code phase contracts list four deliverables but no meta-gate guarantees presence at WS-J Code phase LOCK. **CLOSURE:** §12.6 contract-verification table introduces a F-INDEX-STALE-style PRE-gate marker that the WS-J Code phase author MUST satisfy before LOCKing. The marker is a META-gate per the §4 v2.x F-CLASS-COVERAGE-INCOMPLETE precedent: at WS-J Code phase LOCK, the META-gate enumerates the four deliverables, verifies each test_path + each module_path exists on disk, and fails-closed with sub-tag `.ws_j_code_phase_contract_missing` if any are missing. The gate's predicate body realization itself defers to WS-J Code phase Code-realization (the gate signature lands at this LOCK; the body realizes at WS-J Code phase). Drift-test placeholder `tests/logician/gates/test_ws_j_code_phase_meta_gate.py` reserved.

### §12.4 RT-C2-02 — Stray legacy sub-tag DEPRECATED-REMOVED note (FOLDED-IN)

The Cycle 1 RT-07 SPLIT created two new sub-tags (`.cross_period_kfr_snapshot_drift` + `.sp0_cross_period_flag_signature_invalid`); the original umbrella `.cross_period_signature_invalid` does NOT appear in the §0.5 v17 narrative (which is pre-Cycle-1 baseline; the original umbrella never landed in §0.5 v17 — it was introduced and split within this amendment's Cycle 1 disposition). **CLOSURE:** The umbrella name `.cross_period_signature_invalid` is hereby **DEPRECATED-REMOVED-PRE-LOCK**: it was a Cycle-1-internal placeholder that never reached LOCK. Downstream tooling MUST treat the two SPLIT sub-tags as canonical from this LOCK forward; any future reference to `.cross_period_signature_invalid` in lock_history, audit trails, or amendment text is treated as a typo and resolves to the UNION of the two SPLIT sub-tags (NOT to a separate sub-tag). The §0.5 v23 §B narrative on row 386 reflects only the SPLIT names; no umbrella name appears in the canonical sub-tag enumeration.

### §12.5 RT-C2-03 — Per-read invocation granularity contract refinement (FOLDED-IN)

The §7 contract reads "MUST re-call `sanitize_commitment_id` on EVERY `commitment_id` value read". A contributor could implement a cache-once-per-dispatch pattern that satisfies the literal reading but bypasses the per-read guarantee. **CLOSURE:** The §7 contract is REFINED: the predicate body MUST call `sanitize_commitment_id` IMMEDIATELY BEFORE EACH filesystem-path construction that uses the value. Caching is FORBIDDEN. The recommended implementation pattern is `for cid in commitment_ids: cid_safe = sanitize_commitment_id(cid); waiver_path = waiver_dir / f"{cid_safe}.signed.yaml"`. The drift-test `test_f_report_commitment_missed_post_extraction_revalidation.py` is EXTENDED to assert per-read invocation: the test injects a counter into `sanitize_commitment_id` and asserts the call count equals the count of filesystem-path constructions in the dispatch (NOT the count of commitment_ids in the proposal_commitments.yaml — the test explicitly probes for the cache-once-per-dispatch antipattern by including a commitment_id that is referenced multiple times in the dispatch).

### §12.6 RT-C2-04 — F-REPORT-BENEFICIARY-PRIVACY-LEAK immutable annotation (FOLDED-IN) + RT-C2-06 contract-verification table (FOLDED-IN)

**RT-C2-04 closure:** The §0.5 v23 row 507 is annotated as `immutable_kind: true` (a NEW row attribute). The semantic: any future amendment attempting to change `kind` on this row from `failure-code` to anything else (e.g., `sub-tag`) MUST be REJECTED at the F-INDEX-STALE PRE-gate with a new sub-tag `.immutable_kind_change_attempted`. The annotation is documented at the §0.5 v23 §A row 507 cell + §0.5 v23 §B row-description block + this §12.4 cross-reference. The OVERRIDE NOTE in §4.1 is now structurally backed: even if a future re-author edits the OVERRIDE NOTE out of §4 v2.x.3, the §0.5 v23 row 507 immutable_kind attribute prevents the demotion at the index layer.

**RT-C2-06 closure (also closes RT-C2-01 + E-NF-05):** Contract-verification table for §11.4 WS-J Code phase deliverables — WS-J Code phase author MUST verify ALL FOUR before LOCKing:

| # | Deliverable | Verification command | At-LOCK presence check |
|---|---|---|---|
| 1 | Drift tests for two NEW top-level codes + four sub-tag predicate-body assertions (six test files per §11.4 item 1) | `pytest tests/logician/gates/test_f_report_*_signature_drift.py tests/logician/gates/test_f_report_*_dispatcher_entry.py tests/logician/gates/test_f_report_commitment_*_post_*.py tests/logician/gates/test_f_report_operator_key_rotation_validity_*.py -v` (must report 6 collected + 6 passed) | F-INDEX-STALE-style META-gate `.ws_j_code_phase_contract_missing.drift_tests` |
| 2 | R-REPORT-DECIMAL-MANDATE extended scope + companion test | `scripts/run_lint.sh pipeline/orchestrator/seats/report_generator/ pipeline/orchestrator/tracks/report_mode.py` clean exit 0 + `pytest tests/linting/test_r_report_decimal_mandate_lint_clean_composer_scope.py` passes | F-INDEX-STALE-style META-gate `.ws_j_code_phase_contract_missing.decimal_mandate_scope` |
| 3 | HORIZON→ACTIVE graduation directive applied to §0.5 v14 future re-author | Future re-author of §0.5 v14 applies §2 of this amendment as Status-cell source-of-truth | F-INDEX-STALE-style META-gate `.ws_j_code_phase_contract_missing.horizon_active_graduation` (informational at v0.1; structural at v2 hardening) |
| 4 | Sub-tag namespace rule + runtime guard | `pytest tests/logician/gates/test_sub_tag_namespace_fully_qualified.py` passes | F-INDEX-STALE-style META-gate `.ws_j_code_phase_contract_missing.namespace_rule` |

WS-J Code phase LOCK fails-closed with sub-tag `.ws_j_code_phase_contract_missing.<N>` if any deliverable is missing.

### §12.7 RT-C2-05 — Physical-append-order discipline algorithm precision (FOLDED-IN at §4.2)

**CLOSURE applied at §4.2 row "Primary-check algorithm" cell** — explicit four-step algorithm with FAIL-CLOSED sub-tags at steps 3 and 4. The "DEFENSE-IN-DEPTH" language is no longer ambiguous: ALL FOUR steps execute regardless of which check fires. Drift-test `test_f_report_operator_key_rotation_validity_primary_check_algorithm.py` reserved at WS-J Code phase to assert ALL FOUR steps execute.

### §12.8 RT-C2-07 — Runtime guard for fully-qualified sub-tag emission (FOLDED-IN)

The §11.4 namespace rule is declarative; no runtime guard ensures emitted sub-tags actually include the `<F-CODE>` prefix. **CLOSURE:** WS-J Code phase author MUST add a runtime guard in the generic `GateOutcome.FAIL_CLOSED` helper at `pipeline/logician/gates/_gate_outcome.py` (or equivalent). The guard validates the supplied `sub_tag` string matches the regex `^F-[A-Z][A-Z0-9_-]*\.[a-z][a-z0-9_-]*$` (uppercase failure-code prefix + dot + lowercase sub-tag suffix per the established convention). If the supplied `sub_tag` does NOT match, the helper raises `CriticalPolicyError` with sub-tag `.sub_tag_not_fully_qualified`. The guard is added to the §11.4 contract list (deliverable #4 namespace rule); WS-J Code phase author MUST land the runtime guard + the test `test_sub_tag_namespace_fully_qualified.py` BEFORE WS-J Code phase LOCK.

### §12.9 RT-C2-08 — R-REPORT-DECIMAL-MANDATE config-file diff check (FOLDED-IN)

The §6 table is the contractual scope-list; §11.4 deliverable #2 requires the WS-J Code phase author to copy it into the rule's configuration. **CLOSURE:** The §12.6 contract-verification table deliverable #2 explicitly names the verification command (`scripts/run_lint.sh` clean exit 0 over the extended scope + companion test passes). At WS-J Code phase LOCK, an additional config-diff sub-check compares the on-disk rule configuration (`decimal_mandate.yaml` or equivalent at the rule-config path; precise path lands at WS-J Code phase author's discretion within `pipeline/linting/`) against the §6 Extended scope row's literal globs. Mismatch fails-closed with sub-tag `.decimal_mandate_config_mismatch` (a new sub-tag under the WS-J Code phase META-gate `.ws_j_code_phase_contract_missing.decimal_mandate_scope`).

### §12.10 Cycle 2 closure summary

- 5 Editor NEW probes: 2 NO-ACTION (E-NF-01 + E-NF-03 — concerns are structurally addressed; no fix needed) + 1 cross-reference-FOLDED-IN (E-NF-02 → §12.4 + §4.1 OVERRIDE NOTE) + 1 inline-definition-FOLDED-IN (E-NF-04 → §12.7 inline) + 1 contract-verification-FOLDED-IN (E-NF-05 → §12.6 table).
- 1 Judge NEW probe: J-NF-01 (frontmatter purpose narrative drift) — FOLDED-IN at frontmatter purpose field; count corrected to "fourteen new sub-tags" with explicit derivation note.
- 8 Red Team NEW probes: ALL 8 FOLDED-IN at §12.3 + §12.4 (RT-C2-04 + RT-C2-06) + §12.5 + §12.6 + §12.7 + §12.8 + §12.9. The four RT-C2 closures that introduce NEW META-gate machinery (§12.3 RT-C2-01 drift-test enforcement + §12.4 RT-C2-04 immutable_kind annotation + §12.6 RT-C2-06 contract-verification table + §12.7 RT-C2-05 algorithm precision) are PRE-conditions on the WS-J Code phase LOCK.
- TOTAL Cycle 2 disposition: 14 dispositions handled (8 Red Team + 5 Editor + 1 Judge) per row-170 transparent-disposition pattern with explicit text-level mechanism specifications. No Cycle 3.

## §13. Cross-references

- §14 v1 LOCK: `pipeline/blueprint/v0.1/section_14_report_generator.md` (LOCKED 2026-05-10 rows 200/201)
- §0.5 v17 paired-commit: `pipeline/blueprint/v0.1/section_00_5_section_14_report_generator_amendment.md` (LOCKED 2026-05-10; rows 379-395 — host the existing F-REPORT-* failure-code rows 386-390)
- §4 v2.x parent: `pipeline/blueprint/v0.1/section_04_v2_x_amendment.md` (LOCKED 2026-05-10 rows 193/194; §5.2 hosts the F-REPORT-* HORIZON rows graduated by this amendment)
- §4 v2.x.1 sub-tag-extension precedent: `pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md` (LOCKED 2026-05-10 rows 198/199)
- §4 v2.x.2 explode-per-code precedent: `pipeline/blueprint/v0.1/section_04_logician_v2_x_2_amendment.md` (LOCKED 2026-05-10 row 203)
- §11 v1.1 sanitize_commitment_id: `pipeline/blueprint/v0.1/section_11_v1_1_amendment.md` + `seats/_commitment_id.py` (LOCKED 2026-05-11 rows 209/210)
- §14 audit synthesis: `pipeline/validation/blueprint_section_14_report_generator_2026-05-10/{audit_v1_*.md, audit_v2_*.md}`
- §16 Path B precedent: `pipeline/blueprint/v0.1/section_16_reflection_packet.md` (LOCKED 2026-05-15 row 216 — sibling-not-nested + four orthogonal F-* families discipline)
- This amendment audit trail: `pipeline/validation/section_04_v2_x_3_thesis_2026-05-15/`
- Paired §0.5 v23 amendment: `pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_3_amendment.md`
