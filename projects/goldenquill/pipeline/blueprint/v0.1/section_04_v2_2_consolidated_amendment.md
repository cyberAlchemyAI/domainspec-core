---
title: Blueprint §4 Logician — Amendment v2.2 CONSOLIDATED (all 12 gates + F-AMDT-07 v1.1 extension)
filed: 2026-04-21
operator: Josh Inklovich
amendment_status: LOCKED 2026-04-21 (initial lock by 5-family Code-Thesis-Committee dispatch — roster-class mismatch vs. Tilth blueprint-class convention; retroactive 3-seat Tilth-Thesis-Team confirmation round in flight at `pipeline/validation/blueprint_section_04_v2_2_consolidated_2026-04-21/`)
committee_round: logician_v2_2_consolidated_2026-04-21 (initial; 5-family roster — code-class convention misapplied to a blueprint-class artifact; cycle-1 all-pass 5/5; Qwen3-32B + Llama-3.3-70B + GPT-OSS-120B + Gemini-2.5-Pro + Gemini-2.5-Flash). Supplementary round `logician_v2_2_consolidated_tilth_thesis_2026-04-21` pending — Tilth 3-seat blueprint-class slate (Editor Llama-3.3-70B / Judge Gemini-2.5-Pro / Red Team GPT-OSS-120B).
roster_class_history: First `lock_class: "blueprint"` row in the entire `lock_history.v1.jsonl` ledger (row 91, 2026-04-21T07:16:35Z). Blueprint-class convention per the "Judge / Thesis Review Board seat design" memory and the Section-1 precedent at `pipeline/validation/blueprint_section_1_2026-04-16/` is the 3-seat Tilth Thesis Team, not the 5-family Code Thesis Committee. The 5-family dispatch that produced the initial LOCK is preserved as supplementary audit evidence; the 3-seat retroactive round restores roster convention without reverting the historic first.
parent_lock: pipeline/blueprint/v0.1/section_04_logician.md  (§4 v2.1 LOCKED 2026-04-18, hash e0507e6daaa18676)
rolls_up:
  - section_04_v2_2_amendment.md            (Wave 1 — F-AMDT-02, F-AMDT-03; LOCKED 2026-04-20)
  - section_04_v2_2_wave_2_amendment.md     (Wave 2 — F-AMDT-01, F-AMDT-06, F-AMDT-07 v1+v1.1, F-AMDT-12; LOCKED 2026-04-21)
  - pipeline/validation/code_reviews/logician_v2_2_wave_3_f_amdt_05/synthesis.md  (Wave 3 — F-AMDT-05; LOCKED 2026-04-21)
  - pipeline/validation/code_reviews/logician_v2_2_wave_3_f_amdt_10/synthesis.md  (Wave 3 — F-AMDT-10; LOCKED 2026-04-21)
  - pipeline/validation/code_reviews/logician_v2_2_wave_3_f_amdt_11/synthesis.md  (Wave 3 — F-AMDT-11; LOCKED 2026-04-21)
  - pipeline/validation/code_reviews/logician_v2_2_wave_3_f_amdt_08/synthesis.md  (Wave 3 — F-AMDT-08; LOCKED 2026-04-21)
  - pipeline/validation/code_reviews/logician_v2_2_wave_3_f_amdt_09/synthesis.md  (Wave 3 — F-AMDT-09; LOCKED 2026-04-21)
  - pipeline/validation/code_reviews/logician_v2_2_wave_4_f_amdt_04/synthesis.md  (Wave 4 — F-AMDT-04; LOCKED 2026-04-21)
supersedes_relationship: consolidation; zero semantic delta vs. the two per-wave amendment files + six per-gate LOCKs. Folds them into a single §4 v2.2 blueprint row set for Group 10 outside-audit intake. §4 v2.1 base semantics unchanged. Per-wave amendment files (Wave 1 + Wave 2) and per-gate synthesis files (Wave 3 + Wave 4) remain canonical on disk as the audit-trail source of truth.
scope: consolidated v2.2 Logician blueprint covering the twelve structural amendment-enforcement gates (F-AMDT-01 through F-AMDT-12) plus the v1.1 author-family anti-collision extension on F-AMDT-07. Rolls up Wave 1/2/3/4 per-wave + per-gate LOCKs into a single LOCK-target artifact. All twelve gates are Python-deterministic, zero LLM, fail-closed, Protocol-injected (E-017), inline-literal rebind-resistant (E-023 pattern), AST-lint R1-R7 clean.
companion_code_complete:
  - pipeline/logician/gates/_protocols.py                           (152 LOC, sha3_512[:16]=4f1ad18ae93afb9c — Wave 2 LOCK; extended in Wave 3 without separate relock row; extensions captured in each Wave 3 per-gate LOCK row)
  - pipeline/logician/gates/__init__.py                             (no standalone lock_history row — live re-export surface; pinned implicitly by the 12 per-gate LOCK rows that populate it; no SHA/LOC claim made here)
  - pipeline/logician/gates/f_verdict_blocking_missing.py           (116 LOC, sha3_512[:16]=ca0d7992ad2cd839 — Wave 1)
  - pipeline/logician/gates/f_verdict_citation_missing.py           (235 LOC, sha3_512[:16]=d405ddd9cb7caf53 — Wave 1)
  - pipeline/logician/gates/f_bootstrap_reuse.py                    (127 LOC, sha3_512[:16]=cce8a1efd1612a74 — Wave 2)
  - pipeline/logician/gates/f_deprecation_exemption_reuse.py        (203 LOC, sha3_512[:16]=477b696121057a58 — Wave 2)
  - pipeline/logician/gates/f_amendment_self_reference_detect.py    (269 LOC, sha3_512[:16]=eedd40b7e42502b9 — Wave 2, v1+v1.1)
  - pipeline/logician/gates/f_daily_log_lock_block_missing.py       (253 LOC, sha3_512[:16]=572762b4bd0d9faa — Wave 2)
  - pipeline/logician/gates/f_rollback_script_integrity.py          (289 LOC, sha3_512[:16]=b1e0c448251c0c73 — Wave 3 LOCKED 2026-04-21)
  - pipeline/logician/gates/f_router_integrity_multi_source.py      (431 LOC, sha3_512[:16]=e2d88d06a624f4b1 — Wave 3 LOCKED 2026-04-21)
  - pipeline/logician/gates/f_degradation_stanza_precedence.py      (392 LOC, sha3_512[:16]=dadbacf61b347d76 — Wave 3 LOCKED 2026-04-21)
  - pipeline/logician/gates/f_committee_degradation_timeout.py      (398 LOC, sha3_512[:16]=e1398bee597153a2 — Wave 3 LOCKED 2026-04-21)
  - pipeline/logician/gates/f_deprecation_register_staleness.py     (425 LOC, sha3_512[:16]=12dd8ed02e20e136 — Wave 3 LOCKED 2026-04-21)
  - pipeline/logician/gates/f_sdk_precedent_reuse.py                (254 LOC, sha3_512[:16]=d66f21d9e1d7c83e — Wave 4 LOCKED 2026-04-21)
committee_disposition: each gate independently LOCKED via Code Thesis Committee 5/5 PASS cycle-1 dispatch. Consolidated amendment re-dispatches ONE Thesis round against the §4 v2.2 blueprint reading surface (not 12 separate rounds) — scope is "the consolidation is faithful to the per-wave LOCKs; no new semantic content." Verdict hygiene = faithfulness, not semantic novelty.
family_coverage_caveat: Four non-Anthropic families available (Alibaba / Meta / OpenAI-OSS / Google) post-Kimi deprecation. Cross-family discipline preserved across all twelve per-gate dispatches (reviewer family ≠ author family).
test_suite_state: 3791 pass / 3 skip / 1 xfail (Wave-4 close, F-AMDT-04 LOCK); ~928 tests under `tests/logician/gates/` across the 12 gate modules.
ast_lint_state: R1-R7 exit 0 pipeline-wide at Wave-4 close.
version_wording_discipline: "LOCKED" refers to on-disk LOCKED state only. Forward-looking targets use "target-LOCK at" wording.
---

# Consolidated Amendment — §4 Logician v2.2

## 0. Consolidation intent + scope caveat

This is the single §4 v2.2 blueprint artifact for Group-10 outside-audit intake — a reading-surface consolidation of twelve individually-LOCKed structural amendment-enforcement gates. **Zero semantic delta** vs. the per-wave amendment bodies on disk. Per-wave amendment files (`section_04_v2_2_amendment.md`, `section_04_v2_2_wave_2_amendment.md`) and per-gate synthesis files under `pipeline/validation/code_reviews/` remain canonical as the audit-trail source of truth.

The Thesis round dispatched against this consolidated artifact is a **faithfulness check only** — reviewers are asked whether the consolidation faithfully rolls up the per-wave LOCKs, NOT whether the underlying gate semantics are correct. The 12 gate semantics were independently validated by 12 Code Thesis Committee 5/5 PASS cycle-1 verdicts.

Per the spec card at `pipeline/engineering/spec_cards/logician_v2_2_consolidated_blueprint_amendment.md` §2, reviewers must confirm six criteria: (1) gate-row coverage, (2) failure-code taxonomy, (3) Protocol surface, (4) synthesis pointer continuity, (5) parent-LOCK delta, (6) no hidden scope.

## 1. Amendment intent (same across all 12 gates)

Twelve structural predicates that mechanically enforce seven classes of amendment-flow invariants:

- **Verdict hygiene** — F-AMDT-02, F-AMDT-03: every reviewer verdict carries a blocking-field boolean + citation evidence that resolves against the draft.
- **Single-use amendment mechanisms** — F-AMDT-01, F-AMDT-06: bootstrap exceptions and deprecation-triggered amendments fire exactly once each.
- **Committee self-reference prevention** — F-AMDT-07 (v1 + v1.1): amendments that modify the committee cannot be authored or judged by the family the amendment adds (v1 = Judge-collision; v1.1 = author-family anti-collision across all committee slots).
- **Deprecation-event mechanical ceilings** — F-AMDT-08, F-AMDT-09, F-AMDT-11: time-triggered (14/30/60-day thresholds), stanza-parsing (precedence rules), and register-freshness (72-hour window) gates that bound degradation windows and resolve READ-ONLY deadlocks.
- **Cryptographic integrity** — F-AMDT-05, F-AMDT-10: Ed25519 signatures on rollback scripts and router.yaml pair-commits + external manifest chain; LedgerHashReader pin verification; PriorChainHead continuity.
- **Authoring discipline** — F-AMDT-12: every `lock_history.v1.jsonl` append paired with a canonical `## LOCK: {module}` block in today's daily log carrying seven required non-empty fields.
- **Cross-amendment scope** — F-AMDT-04: SDK-adoption precedent reuse prevention across amendment rounds.

Zero gate performs LLM inference. All are pure Python deterministic predicates behind Protocol-injected dependencies. E-017 injected-callable pattern (§2 Vault trust primitives) applied uniformly. E-023 inline-literal rebind-resistance applied to all failure-code constants. AST-lint R1-R7 clean on every module at its LOCK window.

## 2. Unified §4.5 PRE-gate row table (9 rows)

| Order | Check ID | Fires at | Failure code | Wave / Gate |
|---|---|---|---|---|
| PRE-20 | F-BOOTSTRAP-REUSE | pre-dispatch of amendment round post policy-lock | `F-AMDT-01` | Wave 2 / F-AMDT-01 |
| PRE-21 | F-DEPRECATION-EXEMPTION-REUSE | pre-dispatch of any round that cites prior-round exemption | `F-AMDT-06` | Wave 2 / F-AMDT-06 |
| PRE-22 | F-AMENDMENT-SELF-REFERENCE-DETECT | pre-dispatch of amendment with `modifies_committee is True` | `F-AMDT-07` (parent) / `F-AMDT-07-AUTHOR-COLLISION` (v1.1 sub-code) | Wave 2 / F-AMDT-07 (v1+v1.1) |
| PRE-23 | F-ROLLBACK-SCRIPT-INTEGRITY | rollback script execution request | `F-AMDT-05` | Wave 3 / F-AMDT-05 |
| PRE-24 | F-COMMITTEE-DEGRADATION-TIMEOUT | code-LOCK-promotion under deprecation-in-flight | `F-AMDT-08` (parent) / `F-AMDT-08-SUSPEND` / `F-AMDT-08-ESCALATE` / `F-AMDT-08-READER-FAIL` | Wave 3 / F-AMDT-08 |
| PRE-25 | F-DEPRECATION-REGISTER-STALENESS | amendment citing deprecation event | `F-AMDT-09` (parent) / `F-AMDT-09-STALE` / `F-AMDT-09-MISSING` / `F-AMDT-09-AMBIGUOUS` / `F-AMDT-09-READER-FAIL` | Wave 3 / F-AMDT-09 |
| PRE-26 | F-ROUTER-INTEGRITY-MULTI-SOURCE | router.yaml pair-commit promotion | `F-AMDT-10` (parent) / `F-AMDT-10-PAIR` / `F-AMDT-10-EXTERNAL` / `F-AMDT-10-SIGNATURE` / `F-AMDT-10-CHAIN-BREAK` / `F-AMDT-10-READER-FAIL` | Wave 3 / F-AMDT-10 |
| PRE-27 | F-DEGRADATION-STANZA-PRECEDENCE | operator sign-off stanza OR LOCK under SUSPEND/ESCALATE | `F-AMDT-11` (parent) / `F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION` / `F-AMDT-11-PRECEDENCE-EMPTY` / `F-AMDT-11-READER-FAIL` | Wave 3 / F-AMDT-11 |
| PRE-28 | F-SDK-PRECEDENT-REUSE | amendment claiming SDK precedent | `F-AMDT-04` (parent) / `F-AMDT-04-REUSE` / `F-AMDT-04-AMBIGUOUS` / `F-AMDT-04-READER-FAIL` | Wave 4 / F-AMDT-04 |

Placement note: F-AMDT-08 is classified PRE by its spec card (time-triggered PRE-gate on code-LOCK-promotion) and by its `__init__.py` export position; draft skeletons that placed it in POST are corrected here to the authoritative per-gate LOCK classification. No semantic delta — the Wave 3 committee dispatched and PASSed on the PRE-gate semantics.

Existing §4.5 PRE-gate rows (PRE-01 … PRE-19) retain their ordering relative to each other. All nine new rows are ordered-but-not-ranked — `gate_runner` iterates the list and all nine can fire on the same staged round; only one denial code is surfaced per dispatch.

## 3. Unified §4.6 POST-gate row table (3 rows)

| Order | Check ID | Fires at | Failure code | Wave / Gate |
|---|---|---|---|---|
| POST-14 | F-VERDICT-BLOCKING-MISSING | per-iteration close (Judge / RedTeam verdict JSON) | `F-AMDT-02` | Wave 1 / F-AMDT-02 |
| POST-15 | F-VERDICT-CITATION-MISSING | per-iteration close (Editor verdict JSON with `dimensions[*].evidence`) | `F-AMDT-03` | Wave 1 / F-AMDT-03 |
| POST-16 | F-DAILY-LOG-LOCK-BLOCK-MISSING | on `lock_history.v1.jsonl` append | `F-AMDT-12` (parent) / `F-AMDT-12-MISSING` / `F-AMDT-12-MALFORMED` / `F-AMDT-12-READER-FAIL` | Wave 2 / F-AMDT-12 |

Existing §4.6 POST-gate rows (POST-01 … POST-13) retain their ordering relative to each other. The three new rows sit at the tail of the POST phase so they benefit from all prior structural / admin-risk / claim-evidence / dossier-verify floors having cleared first.

## 4. Shared Protocol surface (§4.A)

All twelve gates consume injected Protocols from `pipeline/logician/gates/_protocols.py` (152 LOC, sha3_512[:16]=4f1ad18ae93afb9c at Wave 2 LOCK; extended through Wave 3 via per-gate LOCK rows — no gate imports `hashlib`, `cryptography`, `nacl`, `ed25519`, `yaml`, `nacl.signing`, or `open()` directly). AST-lint R1 + R3 enforce the no-I/O + no-crypto-library rule at module load. E-017 pattern (injected-callable Protocol, runtime-checkable) applied uniformly.

Unified Protocol roster (17 Protocols in `_protocols.py` + 1 module-local `DraftReaderCallable` in `f_verdict_citation_missing.py`):

| Protocol | Module | Consumed by |
|---|---|---|
| `ClockProtocol` | `_protocols.py` | F-AMDT-08, F-AMDT-09, F-AMDT-12 |
| `LockHistoryReaderCallable` | `_protocols.py` | F-AMDT-04, F-AMDT-08, F-AMDT-10, F-AMDT-11 |
| `DailyLogReaderCallable` | `_protocols.py` | F-AMDT-08, F-AMDT-12 |
| `AuditArtifactReaderCallable` | `_protocols.py` | F-AMDT-01, F-AMDT-04, F-AMDT-06 |
| `FileExistsCallable` | `_protocols.py` | F-AMDT-01, F-AMDT-05, F-AMDT-06 |
| `RouterConfigReaderCallable` | `_protocols.py` | F-AMDT-07 |
| `RouterYamlReaderCallable` | `_protocols.py` | F-AMDT-10 |
| `SignatureVerifyCallable` | `_protocols.py` | F-AMDT-05, F-AMDT-10, F-AMDT-11 |
| `HashBytesCallable` | `_protocols.py` | F-AMDT-05, F-AMDT-10 |
| `LedgerHashReaderCallable` | `_protocols.py` | F-AMDT-05 |
| `ScriptMetadataReaderCallable` | `_protocols.py` | F-AMDT-05 |
| `PinnedHashReaderCallable` | `_protocols.py` | F-AMDT-10 |
| `ExternalManifestReaderCallable` | `_protocols.py` | F-AMDT-10 |
| `PriorChainHeadReaderCallable` | `_protocols.py` | F-AMDT-10 |
| `StanzaReaderCallable` | `_protocols.py` | F-AMDT-08, F-AMDT-11 |
| `DeprecationRegisterReaderCallable` | `_protocols.py` | F-AMDT-09 |
| `DeprecationFeedReaderCallable` | `_protocols.py` | F-AMDT-09 |
| `DraftReaderCallable` | `f_verdict_citation_missing.py` (module-local) | F-AMDT-03 |

F-AMDT-02 consumes no Protocol — it is a pure structural predicate over the verdict `dict`. All other eleven gates use one or more injected Protocols; zero gate module imports `open()`, `hashlib`, `cryptography`, `nacl`, `ed25519`, or `yaml` directly.

## 5. Unified §6 failure-code taxonomy extension

Full consolidation across Waves 1–4. Preserves existing `F-POST-*` / `F-PRE-*` families; adds `F-AMDT-*` subfamily for the twelve gates plus event suffixes and sub-codes.

### 5.1 Parent codes (one per gate)

| Code | Tier | Fires at | Detail taxonomy (parent surface) |
|---|---|---|---|
| `F-AMDT-01` | PRE | pre-dispatch of amendment round | `bootstrap_manifest_absent` / `bootstrap_manifest_reader_raised` / `bootstrap_manifest_policy_lock_stale` / `bootstrap_manifest_hash_drift` |
| `F-AMDT-02` | POST | per-iteration verdict close | `verdict_not_dict` / `blocking_key_absent` / `blocking_value_not_bool` |
| `F-AMDT-03` | POST | per-iteration verdict close | `verdict_not_dict` / `dimensions_key_absent` / `dimensions_not_list` / `draft_reader_raised` / per-dimension: `dimension_entry_not_dict` / `evidence_key_absent` / `evidence_not_string` / `evidence_empty` / `evidence_whitespace_only` / `evidence_tokens_unresolved` |
| `F-AMDT-04` | PRE | amendment claiming SDK precedent | `precedent_reader_raised` / parent + 3 sub-codes below |
| `F-AMDT-05` | PRE | rollback script execution request | `script_bytes_absent` / `signature_verify_returned_false` / `ledger_hash_live_mismatches_pin` / `script_metadata_shape_invalid` / `file_exists_raised` |
| `F-AMDT-06` | PRE | pre-dispatch of any round | `prior_round_reader_raised` / `exemption_not_closed` / `exemption_fix_shape_invalid` / `fix_applied_in_round_mismatch` |
| `F-AMDT-07` | PRE | pre-dispatch of amendment with `modifies_committee is True` | `router_reader_raised` / `judge_primary_family_missing` / `added_reviewer_family_missing` / `author_family_missing` / `judge_reassigned_to_collision` / `judge_reassigned_to_missing` |
| `F-AMDT-08` | PRE | code-LOCK-promotion under deprecation-in-flight | `deprecation_window_open` / parent + 3 sub-codes below |
| `F-AMDT-09` | PRE | amendment citing deprecation event | `register_inconsistent` / parent + 4 sub-codes below |
| `F-AMDT-10` | PRE | router.yaml pair-commit promotion | `router_integrity_break` / parent + 5 sub-codes below |
| `F-AMDT-11` | PRE | operator sign-off stanza OR LOCK under SUSPEND/ESCALATE | `precedence_rule_violation` / parent + 3 sub-codes below |
| `F-AMDT-12` | POST | `lock_history.v1.jsonl` append | `staged_row_module_missing` (parent) / parent + 3 sub-codes below |

### 5.2 Sub-codes (distinct from parent)

| Sub-code | Parent | Tier | Detail |
|---|---|---|---|
| `F-AMDT-04-REUSE` | F-AMDT-04 | PRE | prior-round precedent row cited without fresh SDK anchor |
| `F-AMDT-04-AMBIGUOUS` | F-AMDT-04 | PRE | multiple precedent rows resolve the same claim |
| `F-AMDT-04-READER-FAIL` | F-AMDT-04 | PRE | lock_history / audit-artifact reader raised |
| `F-AMDT-07-AUTHOR-COLLISION` | F-AMDT-07 | PRE | v1.1 author-family anti-collision (C4-NEW-04) — `author_family_in_committee_set` / `committee_slot_reassigned_away_from_author_family_absent` / `committee_slot_reassignment_still_inside_committee_set` / `committee_slot_reassignment_equals_author_family` |
| `F-AMDT-08-SUSPEND` | F-AMDT-08 | PRE | 30-day threshold crossed without operator sign-off |
| `F-AMDT-08-ESCALATE` | F-AMDT-08 | PRE | 60-day threshold crossed |
| `F-AMDT-08-READER-FAIL` | F-AMDT-08 | PRE | lock_history / daily_log / clock reader raised |
| `F-AMDT-09-STALE` | F-AMDT-09 | PRE | register row older than 72-hour staleness window |
| `F-AMDT-09-MISSING` | F-AMDT-09 | PRE | cited deprecation event absent from register |
| `F-AMDT-09-AMBIGUOUS` | F-AMDT-09 | PRE | multiple register rows match event ID |
| `F-AMDT-09-READER-FAIL` | F-AMDT-09 | PRE | register / feed / clock reader raised |
| `F-AMDT-10-PAIR` | F-AMDT-10 | PRE | router.yaml + router_integrity.pinned.json not co-committed |
| `F-AMDT-10-EXTERNAL` | F-AMDT-10 | PRE | external_manifest absent or missing entry |
| `F-AMDT-10-SIGNATURE` | F-AMDT-10 | PRE | external_manifest signature invalid |
| `F-AMDT-10-CHAIN-BREAK` | F-AMDT-10 | PRE | prior_chain_head does not extend |
| `F-AMDT-10-READER-FAIL` | F-AMDT-10 | PRE | yaml / pinned / external / prior_chain reader raised |
| `F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION` | F-AMDT-11 | PRE | architectural-Thesis LOCK carve-out claimed without FRESH_ARCHITECTURAL_THESIS precedence |
| `F-AMDT-11-PRECEDENCE-EMPTY` | F-AMDT-11 | PRE | stanza text present but precedence list empty |
| `F-AMDT-11-READER-FAIL` | F-AMDT-11 | PRE | stanza / lock_history / signature reader raised |
| `F-AMDT-12-MISSING` | F-AMDT-12 | POST | `daily_log_absent_for_today` / `lock_block_heading_not_found` |
| `F-AMDT-12-MALFORMED` | F-AMDT-12 | POST | `lock_block_required_fields_missing` (detail carries `missing_fields: tuple[str, ...]`) |
| `F-AMDT-12-READER-FAIL` | F-AMDT-12 | POST | `clock_raised` / `daily_log_reader_raised` |

### 5.3 Event constants (distinct from failure codes; no deny)

F-AMDT-08 and F-AMDT-11 emit `EVENT_*` constants for observability events that do NOT deny the gate (warnings, clock-skew notices, carve-out grants):

| Event constant | Gate | Semantics |
|---|---|---|
| `EVENT_WARN` | F-AMDT-08 | 14-day threshold crossed — warning only |
| `EVENT_CLOCK_SKEW_WARN` | F-AMDT-08 | clock ahead of most recent lock_history timestamp |
| `EVENT_SUSPEND` | F-AMDT-08 | 30-day threshold crossed — transitions to SUSPEND state |
| `EVENT_ESCALATE` | F-AMDT-08 | 60-day threshold crossed — transitions to ESCALATE state |
| `EVENT_READER_FAIL` | F-AMDT-08 | reader-fail event emission (paired with `F-AMDT-08-READER-FAIL` deny) |
| `EVENT_CARVEOUT_GRANTED` | F-AMDT-11 | architectural-Thesis LOCK carve-out accepted (`FRESH_ARCHITECTURAL_THESIS > TARGET_DATE`) |
| `EVENT_KIND_STANZA` | F-AMDT-11 | stanza-type ingestion notice |
| `EVENT_KIND_PROMOTION` | F-AMDT-11 | LOCK-promotion-type notice |
| `EVENT_PRECEDENCE_MIXED` | F-AMDT-11 | precedence list carries mixed stanza + promotion types |
| `EVENT_STALE` | F-AMDT-09 | register-stale event emission |
| `EVENT_MISSING` | F-AMDT-09 | register-missing event emission |
| `EVENT_AMBIGUOUS` | F-AMDT-09 | register-ambiguous event emission |
| `EVENT_NOT_DEPRECATED_OVERRIDE` | F-AMDT-09 | amendment claims deprecation but feed marks NOT-DEPRECATED |
| `EVENT_CLOCK_SKEW_REGISTER_AHEAD` | F-AMDT-09 | register-row timestamp ahead of clock |
| `EVENT_REUSE` | F-AMDT-04 | SDK-precedent reuse event emission |

### 5.4 Threshold constants (exported from gate modules)

| Constant | Gate | Value | Semantics |
|---|---|---|---|
| `WARN_THRESHOLD_DAYS` | F-AMDT-08 | 14 | warning-event threshold |
| `SUSPEND_THRESHOLD_DAYS` | F-AMDT-08 | 30 | SUSPEND-state threshold |
| `ESCALATE_THRESHOLD_DAYS` | F-AMDT-08 | 60 | ESCALATE-state threshold |
| `STALENESS_WINDOW_HOURS` | F-AMDT-09 | 72 | register-row staleness window |

Naming convention matches existing `F-PRE-*` / `F-POST-*` patterns; category prefix `F-AMDT-` is reserved for v2.2 amendment-landed predicates. All deny codes carry fail-closed semantics. All event constants are observability-only (no deny). All thresholds are inline-literal (E-023 rebind-resistance applied via inline integer literal in predicate body, not module-level constant rebind).

## 6. §4.9 step-ordering note (all 12 gates)

Waves 1–4 add no new PRE-phase or POST-phase steps. All twelve new rows register as additional entries the existing §4.9 `gate_runner` PRE / POST orchestrators iterate. No change to `pre_gate` / `between_gate` / `post_gate` / `done` state machine. No change to §4.12 deep-inspect abort-payload validator. No change to §4.13 cross-org runtime predicate.

## 7. §4.3 no-I/O rule compliance (all 12 gates)

Full compliance matrix in §4 above (Protocol surface). AST-lint R3 (`logician-open-ban`) clean at module load for all twelve gate modules. Pattern consistent with E-017 (injected-callable Protocol for §2 Vault trust primitives).

## 8. Reviewer / author contract (consolidated across 12 gates)

Contracts are verbatim from the per-wave amendment files and per-gate spec cards:

- **F-AMDT-01 (F-BOOTSTRAP-REUSE):** amendment rounds post policy-lock must emit a fresh bootstrap manifest at the staged path; the gate hashes the live artifact and compares against the staged expectation. Reuse of a prior-round manifest (even same-contents) fails on timestamp stale-check.
- **F-AMDT-02 (F-VERDICT-BLOCKING-MISSING):** Judge / RedTeam verdict JSON must be a `dict` with a top-level `blocking` key whose value is a Python `bool` (not `int`, not `str`, not a duck-typed truthy class). Convergence arithmetic in `pipeline.loop.revision_loop.run_inner_loop` consumes this field; a missing or wrong-typed value is a hard-stop POST failure.
- **F-AMDT-03 (F-VERDICT-CITATION-MISSING):** Editor verdict JSON must be a `dict` with a top-level `dimensions` key whose value is a `list`. Each dimension entry must be a `dict` with a string-valued `evidence` field. Every whitespace-split token of `evidence` must appear as a case-sensitive substring of the draft identified by `draft_path`. Empty `dimensions: []` is vacuously PASS.
- **F-AMDT-04 (F-SDK-PRECEDENT-REUSE):** amendments claiming SDK precedent must cite a prior-round precedent row that resolves uniquely against the lock_history ledger and has a live SDK anchor. Reuse of a retired precedent row, multiple-match ambiguity, or reader failure denies.
- **F-AMDT-05 (F-ROLLBACK-SCRIPT-INTEGRITY):** rollback scripts must carry a valid Ed25519 signature (`SignatureVerifyCallable`), a LedgerHash-pin-matching live hash (`LedgerHashReaderCallable` + `HashBytesCallable`), a well-formed script-metadata shape (`ScriptMetadataReaderCallable`), and a present script file (`FileExistsCallable`). Any of the four checks failing denies.
- **F-AMDT-06 (F-DEPRECATION-EXEMPTION-REUSE):** when a staged round re-cites a prior HIGH finding ID, the prior round's exemption close must name the same ID with a well-formed `fix_applied_in_round` pointer. `collections.Counter`-based matching: if ID `H-12` appears twice in the staged round, the prior round must close it twice. Invalid-fix shape denies. Rejects homoglyph / Cyrillic-lookalike IDs via exact string equality.
- **F-AMDT-07 (F-AMENDMENT-SELF-REFERENCE-DETECT):**
  - **v1 Judge-collision:** on `modifies_committee is True` where the amendment adds a reviewer whose family collides with the current Judge's primary family AND the author family differs from Judge-primary, the amendment MUST provide a `judge_reassigned_to` field whose family differs from BOTH the current judge-primary AND the added reviewer family.
  - **v1.1 author-family anti-collision (C4-NEW-04):** on `modifies_committee is True` where the author family collides with any primary or fallback family across the five committee slots, the amendment MUST provide a `committee_slot_reassigned_away_from_author_family` field whose family escapes the entire committee-family set ∪ `{author_family}`. Sub-code `F-AMDT-07-AUTHOR-COLLISION` distinct from parent.
  - **Strictness:** exact string equality on family names — no case-fold, no Unicode normalization. `modifies_committee` is strict `is True`.
- **F-AMDT-08 (F-COMMITTEE-DEGRADATION-TIMEOUT):** LOCK-promotion under deprecation-in-flight must resolve against the WARN/SUSPEND/ESCALATE threshold ladder (14/30/60 days). SUSPEND and ESCALATE deny LOCK; WARN is observability-only. ClockProtocol + LockHistoryReader + DailyLogReader + StanzaReader injected. Clock-skew (clock ahead of most-recent lock_history timestamp) emits `EVENT_CLOCK_SKEW_WARN` without deny.
- **F-AMDT-09 (F-DEPRECATION-REGISTER-STALENESS):** amendments citing a deprecation event must resolve the event against the register within the 72-hour staleness window (`STALENESS_WINDOW_HOURS = 72`). STALE / MISSING / AMBIGUOUS sub-codes surface per fault mode. DeprecationRegister + DeprecationFeed + Clock injected.
- **F-AMDT-10 (F-ROUTER-INTEGRITY-MULTI-SOURCE):** router.yaml pair-commit promotions must present three integrity proofs: (1) router.yaml + router_integrity.pinned.json co-committed (PAIR), (2) external_manifest present with signature valid (EXTERNAL + SIGNATURE), (3) prior_chain_head continuity (CHAIN-BREAK). Any of the three proofs failing denies. RouterYaml + Pinned + ExternalManifest + PriorChainHead + SignatureVerify + HashBytes + LockHistory Protocols injected.
- **F-AMDT-11 (F-DEGRADATION-STANZA-PRECEDENCE):** operator sign-off stanzas + LOCK-promotion-under-SUSPEND/ESCALATE rows must resolve against the precedence rule `FRESH_ARCHITECTURAL_THESIS > TARGET_DATE`. Empty precedence list denies (PRECEDENCE-EMPTY). Architectural-Thesis LOCK carve-out accepted only when the carve-out claim carries a FRESH_ARCHITECTURAL_THESIS precedence higher than the TARGET_DATE; carve-out violations deny with sub-code `F-AMDT-11-DEADLOCK-CARVEOUT-VIOLATION`. StanzaReader + LockHistory + SignatureVerify Protocols injected.
- **F-AMDT-12 (F-DAILY-LOG-LOCK-BLOCK-MISSING):** every staged `lock_history.v1.jsonl` row must be accompanied (at the time of the append call) by a canonical LOCK block in today's daily log. Block discovery is line-based — the heading `## LOCK: {module}` must appear on a line by itself; body ranges from heading line to next `## ` heading or EOF. Required fields parsed as `` - `{field}`: value `` bullet lines with non-empty post-strip values; first-occurrence-wins on duplicates. Narrow backfill carve-out: BOTH `backfilled is True` AND `verdict == "LOCKED-backfilled"` required; half-marked backfills run the full gate.

## 9. Non-goals (across all 12 gates)

- Does not validate verdict JSON or amendment YAML shape beyond the fields each gate directly consults.
- Does not run semantic similarity / normalization on evidence tokens, finding IDs, or family names. Strict byte/substring / exact-equality is the floor.
- Does not introduce cross-org visibility; all readers are same-round or same-org scope (Law 3 preserved).
- Does not add a CI hook. Operator-run under `gate_runner` PRE / POST phases; §5 v6 pipeline orchestrator invokes the runner.
- Does not introduce a new primitive kind in §0.5. All rows register as `pre-gate-check` / `post-gate-check` + `failure-code` pairs per existing §0.5 v4 schema; shared `_protocols.py` registers as `interface-contract`.

## 10. §0.5 paired-commit rows (consolidated)

This §4 v2.2 consolidated amendment LOCKs atomically with the following §0.5 paired-commit rows. Per-wave amendments already staged rows 1–14; the consolidation adds a pointer row (row 15) to the consolidated artifact itself. The §0.5 LOCK window absorbs the full row set.

| Row | Kind | Pin |
|---|---|---|
| `logician.gates._protocols` | interface-contract | `pipeline/logician/gates/_protocols.py` sha3_512[:16]=4f1ad18ae93afb9c (Wave 2 pin; extensions captured in each Wave 3 per-gate LOCK row) |
| `logician.gates.__init__` | interface-contract | `pipeline/logician/gates/__init__.py` (no standalone lock_history row — live re-export surface pinned implicitly by 12 per-gate LOCK rows) |
| `logician.gates.f_verdict_blocking_missing` | post-gate-check | sha3_512[:16]=ca0d7992ad2cd839 |
| `logician.gates.f_verdict_citation_missing` | post-gate-check | sha3_512[:16]=d405ddd9cb7caf53 |
| `logician.gates.f_bootstrap_reuse` | pre-gate-check | sha3_512[:16]=cce8a1efd1612a74 |
| `logician.gates.f_deprecation_exemption_reuse` | pre-gate-check | sha3_512[:16]=477b696121057a58 |
| `logician.gates.f_amendment_self_reference_detect` | pre-gate-check | sha3_512[:16]=eedd40b7e42502b9 |
| `logician.gates.f_daily_log_lock_block_missing` | post-gate-check | sha3_512[:16]=572762b4bd0d9faa |
| `logician.gates.f_rollback_script_integrity` | pre-gate-check | sha3_512[:16]=b1e0c448251c0c73 |
| `logician.gates.f_router_integrity_multi_source` | pre-gate-check | sha3_512[:16]=e2d88d06a624f4b1 |
| `logician.gates.f_degradation_stanza_precedence` | pre-gate-check | sha3_512[:16]=dadbacf61b347d76 |
| `logician.gates.f_committee_degradation_timeout` | pre-gate-check | sha3_512[:16]=e1398bee597153a2 |
| `logician.gates.f_deprecation_register_staleness` | pre-gate-check | sha3_512[:16]=12dd8ed02e20e136 |
| `logician.gates.f_sdk_precedent_reuse` | pre-gate-check | sha3_512[:16]=d66f21d9e1d7c83e |
| `failure-code.F-AMDT-01`..`F-AMDT-12` (12 parent codes + all sub-codes from §5.2) | failure-code | §4.5 PRE-20..PRE-28 + §4.6 POST-14..POST-16 |
| `blueprint.section_04_v2_2_consolidated_amendment` | blueprint-section | `pipeline/blueprint/v0.1/section_04_v2_2_consolidated_amendment.md` (target LOCK at §4 v2.2 close) |

Forward-looking: F-INDEX-STALE PRE-gate in §0.5 v4 fires-closed if the paired commit is skipped. Authoring discipline: §0.5 v4 target-LOCK absorbs these rows in its next window; the `lock_history.v1.jsonl` rows for the consolidation reference this consolidated amendment path as `blueprint_section` with `lock_class: "blueprint"` per spec-card §6.2.

## 11. Committee round audit trail (12 synthesis pointers preserved)

Each gate's Code Thesis Committee synthesis file is canonical. Consolidated Thesis round is a faithfulness check only; it does NOT supersede the per-gate semantic reviews.

| Gate | Committee round | Synthesis pointer |
|---|---|---|
| F-AMDT-02 + F-AMDT-03 (Wave 1 joint) | `logician_v2_2_wave_1` | `pipeline/validation/code_reviews/logician_v2_2_wave_1/synthesis.md` |
| F-AMDT-01 | `logician_v2_2_wave_2_f_amdt_01` | `pipeline/validation/code_reviews/logician_v2_2_wave_2_f_amdt_01/synthesis.md` |
| F-AMDT-06 | `logician_v2_2_wave_2_f_amdt_06` | `pipeline/validation/code_reviews/logician_v2_2_wave_2_f_amdt_06/synthesis.md` |
| F-AMDT-07 (v1+v1.1) | `logician_v2_2_wave_2_f_amdt_07` | `pipeline/validation/code_reviews/logician_v2_2_wave_2_f_amdt_07/synthesis.md` |
| F-AMDT-12 | `logician_v2_2_wave_2_f_amdt_12` | `pipeline/validation/code_reviews/logician_v2_2_wave_2_f_amdt_12/synthesis.md` |
| F-AMDT-05 | `logician_v2_2_wave_3_f_amdt_05` | `pipeline/validation/code_reviews/logician_v2_2_wave_3_f_amdt_05/synthesis.md` |
| F-AMDT-10 | `logician_v2_2_wave_3_f_amdt_10` | `pipeline/validation/code_reviews/logician_v2_2_wave_3_f_amdt_10/synthesis.md` |
| F-AMDT-11 | `logician_v2_2_wave_3_f_amdt_11` | `pipeline/validation/code_reviews/logician_v2_2_wave_3_f_amdt_11/synthesis.md` |
| F-AMDT-08 | `logician_v2_2_wave_3_f_amdt_08` | `pipeline/validation/code_reviews/logician_v2_2_wave_3_f_amdt_08/synthesis.md` |
| F-AMDT-09 | `logician_v2_2_wave_3_f_amdt_09` | `pipeline/validation/code_reviews/logician_v2_2_wave_3_f_amdt_09/synthesis.md` |
| F-AMDT-04 | `logician_v2_2_wave_4_f_amdt_04` | `pipeline/validation/code_reviews/logician_v2_2_wave_4_f_amdt_04/synthesis.md` |

All twelve committees returned **5/5 PASS cycle-1, zero real HIGH / MEDIUM / LOW findings**. Transport-retry carve-out invoked on:
- F-AMDT-07 R2 llama (tool-call validation error on first attempt; clean PASS on retry).
- F-AMDT-12 R1 qwen (finding-field hallucination — fictional module names; clean PASS on retry).
- F-AMDT-12 R4 gemini-pro (gateway-side "Agent couldn't generate a response" placeholder; clean PASS on retry).
- F-AMDT-11 R5 gemini-flash (503 UNAVAILABLE on first attempt; clean PASS on retry).
- F-AMDT-04 R5 gemini-flash (503 UNAVAILABLE on first attempt; clean PASS on retry).

All retries counted as cycle-1 under the transport-retry carve-out (verdict invariant, trigger is transport or finding-field hallucination with top-line verdict unchanged).

## 12. Evidence (consolidated)

- **Spec cards (13):** `pipeline/engineering/spec_cards/logician_v2_2_f_verdict_blocking_missing.md`, `logician_v2_2_f_verdict_citation_missing.md`, `logician_v2_2_f_bootstrap_reuse.md`, `logician_v2_2_f_deprecation_exemption_reuse.md`, `logician_v2_2_f_amendment_self_reference_detect.md`, `logician_v2_2_f_daily_log_lock_block_missing.md`, `logician_v2_2_f_rollback_script_integrity.md`, `logician_v2_2_f_router_integrity_multi_source.md`, `logician_v2_2_f_degradation_stanza_precedence.md`, `logician_v2_2_f_committee_degradation_timeout.md`, `logician_v2_2_f_deprecation_register_staleness.md`, `logician_v2_2_f_sdk_precedent_reuse.md`, and this consolidation spec: `logician_v2_2_consolidated_blueprint_amendment.md`.
- **Code (13 modules):** 12 gate modules + shared `_protocols.py` listed in `companion_code_complete` front-matter.
- **Tests:** ~928 tests in `tests/logician/gates/` across 12 gate modules (per-gate unit + adversarial). **100% coverage** on every gate module and the shared Protocol surface at its LOCK window. Per-gate counts in per-wave amendment bodies + per-gate synthesis files.
- **Full suite regression at Wave-4 close:** 3791 pass / 3 skip / 1 xfail. Green. +928 tests over the pre-Wave-1 baseline attributable to the gate work (plus interleaved Scout / §5 / §6 / §7 work not tracked here).
- **AST-lint:** R1–R7 exit 0 (`scripts/run_lint.sh`) pipeline-wide at Wave-4 close.
- **Committee audit trail:** 11 `synthesis.md` files under `pipeline/validation/code_reviews/logician_v2_2_wave_*_f_amdt_*/` covering the 12 gates — Wave 1 dispatch was a joint F-AMDT-02 + F-AMDT-03 committee (single synthesis at `logician_v2_2_wave_1/synthesis.md`); all subsequent waves dispatched per-gate. Pointers in §11 above.
- **Individual lock_history rows (13):** 12 gate-module rows + 1 `_protocols.py` row appended under respective `committee_round` tags in `pipeline/engineering/lock_history.v1.jsonl` (timestamps 2026-04-20T22:00:00Z through 2026-04-21T11:30:00Z; all `lock_class: "code"`).

## 13. LOCK criteria (consolidated)

1. All 12 gates LOCKED on disk (13 per-module lock_history rows present — 12 gates + `_protocols`).
2. Full pytest green (3791 / 3 / 1 at Wave-4 close).
3. AST-lint R1-R7 exit 0 on the consolidated blueprint-dependency set.
4. Thesis round dispatched against this consolidated artifact returns "faithful consolidation" verdict. Verdict scope is faithfulness to per-wave LOCKs — NOT re-litigating the per-gate semantics. **Blueprint-class roster = Tilth 3-seat Thesis Team** (Editor / Judge / Red Team) per `router.yaml`. Initial lock (ledger row 91) landed via a 5-family Code-Thesis-Committee dispatch (roster-class mismatch); the retroactive 3-seat Tilth-Thesis-Team round at `pipeline/validation/blueprint_section_04_v2_2_consolidated_2026-04-21/` restores convention and seals the faithfulness verdict.
5. Operator signs — `section_04_v2_2_consolidated_amendment_DRAFT.md` renamed to `section_04_v2_2_consolidated_amendment.md` with `amendment_status: LOCKED` + signed front-matter.
6. Paired `lock_history.v1.jsonl` append with `lock_class: "blueprint"` per spec-card §6.2.
7. F-AMDT-12-verified daily-log canonical LOCK block for the consolidated amendment.
8. §0.5 Interface Index paired-commit row for the consolidated amendment (separate LOCK target — not part of this Thesis dispatch).
9. Per-wave amendment files + per-gate synthesis files preserved on disk as audit trail; this consolidated artifact becomes the Group-10-outside-audit intake artifact.

## 14. Out of scope for this Thesis round

- Re-litigating per-gate semantics (all 12 gates LOCKED under `code_merge_rule=all_pass` via independent Code Thesis Committee dispatches).
- §4 v2.1 base-layer changes (parent-LOCK is stable at hash `e0507e6daaa18676`).
- §0.5 Interface Index re-LOCK (separate artefact, separate round — target-LOCK at next §0.5 window).
- New `F-AMDT-*` gate additions (not part of v2.2 scope).
- §4.14a (v2.1.1), §4.2.3 (v2.3), §4.2.4 (v2.4), §4.2.5 (v2.5) — orthogonal parallel amendments; no conflict with this consolidation.

---

*v2.2 consolidated — assembled post Wave-4 close 2026-04-21.*

*LOCK history: Initial LOCK 2026-04-21T07:16:35Z via a 5-family Code-Thesis-Committee dispatch (Groq qwen3-32b / llama-3.3-70b-versatile / openai-gpt-oss-120b + Google gemini-2.5-pro / gemini-2.5-flash); all-pass 5/5, zero findings, zero transport retries. First `lock_class: "blueprint"` row in the ledger (row 91). The 5-family roster is the code-class convention — blueprint-class convention is the Tilth 3-seat Thesis Team (Editor Llama-3.3-70B / Judge Gemini-2.5-Pro / Red Team GPT-OSS-120B). Retroactive 3-seat confirmation round at `pipeline/validation/blueprint_section_04_v2_2_consolidated_2026-04-21/` restores roster convention without reverting the historic first. Supplementary ledger row + daily-log LOCK-CONFIRMED block appended on 3-seat all-pass.*
