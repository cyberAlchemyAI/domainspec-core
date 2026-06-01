---
title: Blueprint §4 Logician — Amendment v2.2 Wave 2 (four new gates: F-AMDT-01 / F-AMDT-06 / F-AMDT-07 / F-AMDT-12)
filed: 2026-04-21
operator: Josh
amendment_status: LOCKED 2026-04-21 (Code Thesis Committee 5/5 PASS cycle-1 on all four gates, zero findings)
parent_lock: pipeline/blueprint/v0.1/section_04_logician.md  (§4 v2.1 LOCKED 2026-04-18, hash e0507e6daaa18676)
wave_1_reference: pipeline/blueprint/v0.1/section_04_v2_2_amendment.md (LOCKED 2026-04-20)
supersedes_relationship: non-disruptive extension. Adds three PRE-gate predicates (F-AMDT-01, F-AMDT-06, F-AMDT-07) and one POST-gate predicate (F-AMDT-12) to the existing §4.5 PRE-gate and §4.6 POST-gate row tables. Leaves wave-1 (F-AMDT-02, F-AMDT-03) and §4.1–§4.13 semantics unchanged. §4.14a (v2.1.1), §4.2.3 (v2.3), §4.2.4 (v2.4), §4.2.5 (v2.5) are orthogonal parallel amendments; wave-2 does not conflict with their ordering.
scope: Wave 2 of the Tier 1 policy-lock Logician v2.2 queue (memory ref project_tier1_lock_sealed_2026-04-20.md). Four predicates that close structural residual-gaps in amendment flow and LOCK-append discipline:
  - F-AMDT-01 F-BOOTSTRAP-REUSE — prevents bootstrap-manifest reuse on amendment rounds post policy-lock
  - F-AMDT-06 F-DEPRECATION-EXEMPTION-REUSE — prevents one-off deprecation exemptions from being re-used in subsequent rounds
  - F-AMDT-07 F-AMENDMENT-SELF-REFERENCE-DETECT — (v1) Judge-primary-family collision detection on committee-modifying amendments + (v1.1) author-family anti-collision against the full committee slot set (C4-NEW-04)
  - F-AMDT-12 F-DAILY-LOG-LOCK-BLOCK-MISSING — every `lock_history.v1.jsonl` append must be paired with a canonical `## LOCK: {module}` block in today's daily log with seven required non-empty fields
companion_code:
  - pipeline/logician/gates/f_bootstrap_reuse.py                    (127 LOC, sha3_512[:16]=cce8a1efd1612a74)
  - pipeline/logician/gates/f_deprecation_exemption_reuse.py        (203 LOC, sha3_512[:16]=477b696121057a58)
  - pipeline/logician/gates/f_amendment_self_reference_detect.py    (269 LOC, sha3_512[:16]=eedd40b7e42502b9)
  - pipeline/logician/gates/f_daily_log_lock_block_missing.py       (253 LOC, sha3_512[:16]=572762b4bd0d9faa)
  - pipeline/logician/gates/_protocols.py                           (152 LOC, sha3_512[:16]=4f1ad18ae93afb9c)
  - pipeline/logician/gates/__init__.py                             (104 LOC, sha3_512[:16]=11ad867f5ac0da5d)
companion_tests:
  - tests/logician/gates/test_f_bootstrap_reuse.py                       (61 collected)
  - tests/logician/gates/test_adv_f_bootstrap_reuse.py                   (13 collected)
  - tests/logician/gates/test_f_deprecation_exemption_reuse.py           (52 collected)
  - tests/logician/gates/test_adv_f_deprecation_exemption_reuse.py       (54 collected)
  - tests/logician/gates/test_f_amendment_self_reference_detect.py       (52 collected)
  - tests/logician/gates/test_adv_f_amendment_self_reference_detect.py   (49 collected)
  - tests/logician/gates/test_f_daily_log_lock_block_missing.py          (41 collected)
  - tests/logician/gates/test_adv_f_daily_log_lock_block_missing.py      (44 collected)
committee_rounds:
  - logician_v2_2_wave_2_f_amdt_01  (cycle-1 all-pass, 5/5, zero findings)
  - logician_v2_2_wave_2_f_amdt_06  (cycle-1 all-pass, 5/5, zero findings)
  - logician_v2_2_wave_2_f_amdt_07  (cycle-1 all-pass, 5/5, zero findings; R2 llama transport-retry documented)
  - logician_v2_2_wave_2_f_amdt_12  (cycle-1 all-pass, 5/5, zero findings; R1 qwen hallucination-retry + R4 gemini-pro transport-retry documented)
family_coverage_caveat: Only four non-Anthropic families available (Alibaba / Meta / OpenAI-OSS / Google) after the wave-1 Kimi deprecation; see `pipeline/validation/code_reviews/logician_v2_2_wave_1/synthesis.md`. Cross-family discipline preserved (reviewer family ≠ author family) across all four gates.
version_wording_discipline: "LOCKED" refers to on-disk LOCKED state only. Forward-looking targets use "target-LOCK at" wording.
---

# Amendment intent

Four new gates that close structural residual-gaps in the amendment / LOCK-append flow:

- **F-AMDT-01 (F-BOOTSTRAP-REUSE).** PRE-gate that denies amendment rounds attempting to reuse a bootstrap manifest whose policy-lock window has already closed. A fresh round post policy-lock must produce its own bootstrap — silent reuse would let a retired manifest carry forward into a new committee cycle. Fails closed on manifest absence, stale timestamps, or hash drift.
- **F-AMDT-06 (F-DEPRECATION-EXEMPTION-REUSE).** PRE-gate that prevents one-off deprecation exemptions (HIGH findings closed under an explicit `fix_applied_in_round` scope) from being re-cited in subsequent rounds without a new explicit close. Uses `collections.Counter`-based finding_id matching so duplicate IDs in the staged round must each be closed individually. Rejects homoglyph / Cyrillic-lookalike IDs via exact string equality (no case-fold, no Unicode normalization).
- **F-AMDT-07 (F-AMENDMENT-SELF-REFERENCE-DETECT).** PRE-gate that runs two orthogonal checks on committee-modifying amendments:
  - **v1 Judge-collision:** three-condition test — `modifies_committee is True` AND `added_reviewer_family == judge_primary_family` AND `author_family != judge_primary_family`. When all three fire, `judge_reassigned_to` must differ from BOTH the current judge-primary family AND the added reviewer family. Fails with parent code `F-AMDT-07`.
  - **v1.1 author-family anti-collision (C4-NEW-04):** `author_family` must NOT equal any `code_reviewer_N.primary_family` OR `fallback_family` across all five committee slots. When a collision is detected, `committee_slot_reassigned_away_from_author_family` must escape the entire committee-family set ∪ `{author_family}`. Fails with sub-code `F-AMDT-07-AUTHOR-COLLISION` distinct from the parent code. v1 takes precedence when both fire (unit + adversarial tests cover co-occurrence).
- **F-AMDT-12 (F-DAILY-LOG-LOCK-BLOCK-MISSING).** POST-gate that requires every `lock_history.v1.jsonl` append to be paired with a canonical `## LOCK: {module}` block in today's daily log carrying all seven required non-empty fields (`lock_timestamp_utc`, `committee_round`, `verdict`, `code_sha3_512_prefix`, `tests_added_this_module`, `lines_of_code`, `findings_surfaced_at_lock`). Closes the F-03 residual-gap: authoring discipline becomes structural — a session that LOCKs a module without writing the daily-log block is DENIED at the append, not discovered by an audit weeks later. Narrow backfill carve-out: BOTH `backfilled is True` AND `verdict == "LOCKED-backfilled"` required; half-marked backfills run the full gate.

All four are deterministic, pure-Python, zero-token, fail-closed. All four use injected Protocol dependencies (no direct file I/O, no YAML parsing, no datetime instantiation in gate code). AST-lint R3 (`logician-open-ban`) clean across all four modules.

# Proposed §4.5 PRE-gate-check table additions

Three new rows append to the §4.5 PRE-gate table. Ordering is ordered-but-not-ranked — gate_runner iterates the list and all three can fire on the same staged round; only one denial code is surfaced per dispatch.

| Order | Check ID | Fires at | Failure code | Source |
|---|---|---|---|---|
| PRE-20 | F-BOOTSTRAP-REUSE | pre-dispatch of amendment round post policy-lock | `F-AMDT-01` | §4.5 wave-2 |
| PRE-21 | F-DEPRECATION-EXEMPTION-REUSE | pre-dispatch of any round that cites prior-round exemption | `F-AMDT-06` | §4.5 wave-2 |
| PRE-22 | F-AMENDMENT-SELF-REFERENCE-DETECT | pre-dispatch of amendment with `modifies_committee is True` | `F-AMDT-07` (parent) / `F-AMDT-07-AUTHOR-COLLISION` (v1.1 sub-code) | §4.5 wave-2 |

# Proposed §4.6 POST-gate-check table additions

One new row appends to the §4.6 POST-gate table, after the existing POST-14 / POST-15 from wave-1:

| Order | Check ID | Fires at | Failure code | Source |
|---|---|---|---|---|
| POST-16 | F-DAILY-LOG-LOCK-BLOCK-MISSING | on `lock_history.v1.jsonl` append | `F-AMDT-12` (parent) / `F-AMDT-12-MISSING` / `F-AMDT-12-MALFORMED` / `F-AMDT-12-READER-FAIL` | §4.6 wave-2 |

# Proposed §6 failure-code family extension

Four new codes + three sub-codes in the `F-AMDT-*` family:

| Code | Tier | Fires at | Detail taxonomy |
|---|---|---|---|
| `F-AMDT-01` | PRE | pre-dispatch of amendment round | `bootstrap_manifest_absent` / `bootstrap_manifest_reader_raised` / `bootstrap_manifest_policy_lock_stale` / `bootstrap_manifest_hash_drift` |
| `F-AMDT-06` | PRE | pre-dispatch of any round | `prior_round_reader_raised` / `exemption_not_closed` / `exemption_fix_shape_invalid` / `fix_applied_in_round_mismatch` |
| `F-AMDT-07` | PRE | pre-dispatch of amendment with `modifies_committee is True` | `router_reader_raised` / `judge_primary_family_missing` / `added_reviewer_family_missing` / `author_family_missing` / `judge_reassigned_to_collision` / `judge_reassigned_to_missing` |
| `F-AMDT-07-AUTHOR-COLLISION` | PRE | pre-dispatch of amendment with `modifies_committee is True` (after v1 clear) | `author_family_in_committee_set` / `committee_slot_reassigned_away_from_author_family_absent` / `committee_slot_reassignment_still_inside_committee_set` / `committee_slot_reassignment_equals_author_family` |
| `F-AMDT-12` | POST | on `lock_history.v1.jsonl` append | `staged_row_module_missing` (parent); see sub-codes below |
| `F-AMDT-12-MISSING` | POST | on `lock_history.v1.jsonl` append | `daily_log_absent_for_today` / `lock_block_heading_not_found` |
| `F-AMDT-12-MALFORMED` | POST | on `lock_history.v1.jsonl` append | `lock_block_required_fields_missing` (detail carries `missing_fields: tuple[str, ...]`) |
| `F-AMDT-12-READER-FAIL` | POST | on `lock_history.v1.jsonl` append | `clock_raised` / `daily_log_reader_raised` |

Naming convention matches wave-1 (`F-AMDT-*` reserved for v2.2+ amendment-landed predicates). All fail-closed semantics.

# §4.9 step-ordering note

Wave 2 adds no new PRE-phase or POST-phase steps. The four new rows register as additional entries the existing §4.9 `gate_runner` PRE / POST orchestrators iterate. No change to pre_gate / between_gate / post_gate / done state machine. No change to §4.12 deep-inspect abort-payload validator. No change to §4.13 cross-org runtime predicate.

# §4.3 no-I/O rule compliance

All four gates use injected Protocols defined in `pipeline/logician/gates/_protocols.py`:

| Gate | Injected Protocols |
|---|---|
| F-AMDT-01 | `AuditArtifactReaderCallable`, `FileExistsCallable` |
| F-AMDT-06 | `AuditArtifactReaderCallable`, `FileExistsCallable` |
| F-AMDT-07 | `RouterConfigReaderCallable` (pre-digested dict — gate never parses YAML) |
| F-AMDT-12 | `DailyLogReaderCallable`, `ClockProtocol` (both `@runtime_checkable`) |

`ClockProtocol` carries `now_utc() -> datetime` returning a UTC-aware datetime; `today_iso` is derived inside the gate via `now.date().isoformat()`. No direct `open()` call in any gate module. AST-lint R3 (`logician-open-ban`) clean at module load for all four modules. Pattern consistent with E-017 (injected-callable Protocol for §2 Vault trust primitives).

# Reviewer / author contract

- **F-AMDT-01:** amendment rounds post policy-lock must emit a fresh bootstrap manifest at the staged path; the gate hashes the live artifact and compares against the staged expectation. Reuse of a prior-round manifest (even same-contents) fails on timestamp stale-check.
- **F-AMDT-06:** when a staged round re-cites a prior HIGH finding ID, the prior round's exemption close must name the same ID with a well-formed `fix_applied_in_round` pointer. Counter-based matching: if ID `H-12` appears twice in the staged round, the prior round must close it twice. Invalid-fix shape (missing keys, non-string values) denies.
- **F-AMDT-07:**
  - **v1:** on `modifies_committee is True` where the amendment adds a reviewer whose family collides with the current Judge's primary family AND the author family differs from Judge-primary, the amendment MUST provide a `judge_reassigned_to` field whose family differs from BOTH the current judge-primary AND the added reviewer family.
  - **v1.1:** on `modifies_committee is True` where the author family collides with any primary or fallback family across the five committee slots, the amendment MUST provide a `committee_slot_reassigned_away_from_author_family` field whose family escapes the entire committee-family set ∪ `{author_family}`.
  - **Strictness:** exact string equality on family names — no case-fold, no Unicode normalization (composed `café` ≠ decomposed `cafe\u0301` by design). `modifies_committee` is strict `is True` (rejects `"true"`, `1`, custom `__bool__`, `numpy.bool_`).
- **F-AMDT-12:** every staged `lock_history.v1.jsonl` row must be accompanied (at the time of the append call) by a canonical LOCK block in today's daily log. Block discovery is line-based — the heading `## LOCK: {module}` must appear on a line by itself (trailing whitespace tolerated on heading only); body ranges from heading line to next `## ` heading or EOF. Required fields parsed as `` - `{field}`: value `` bullet lines with non-empty post-strip values; first-occurrence-wins on duplicates. Narrow backfill carve-out: BOTH `backfilled is True` AND `verdict == "LOCKED-backfilled"` required to exempt; half-marked backfills run the full gate.

# Non-goals for this wave

- Does not validate amendment YAML schema beyond the fields each gate directly consults. Front-matter shape validation remains with the engineering_process gate harness.
- Does not run semantic similarity on finding IDs or family names. Strict byte-equal match is the floor.
- Does not introduce cross-org visibility; F-AMDT-06 reads only the prior-round audit artifact for the same round-family (Law 3 preserved).
- Does not add a CI hook. Operator-run under `gate_runner` PRE / POST phases; §5 v6 pipeline orchestrator invokes the runner.
- Does not introduce a new primitive kind in §0.5. All four rows register as `pre-gate-check` / `post-gate-check` + `failure-code` pairs per existing §0.5 v4 schema.
- Does not revisit wave-1 (F-AMDT-02, F-AMDT-03) semantics or rows.

# §0.5 paired-commit rows

This §4 v2.2 wave-2 amendment LOCKs atomically with the following §0.5 paired-commit rows (to be appended in the next §0.5 LOCK window; wave-2 itself does not touch §0.5 — the pointer is authored here so the §0.5 LOCK captures them):

| Row | Kind | Pin |
|---|---|---|
| `logician.gates.f_bootstrap_reuse` | pre-gate-check | `pipeline/logician/gates/f_bootstrap_reuse.py` sha3_512[:16]=cce8a1efd1612a74 |
| `logician.gates.f_deprecation_exemption_reuse` | pre-gate-check | `pipeline/logician/gates/f_deprecation_exemption_reuse.py` sha3_512[:16]=477b696121057a58 |
| `logician.gates.f_amendment_self_reference_detect` | pre-gate-check | `pipeline/logician/gates/f_amendment_self_reference_detect.py` sha3_512[:16]=eedd40b7e42502b9 |
| `logician.gates.f_daily_log_lock_block_missing` | post-gate-check | `pipeline/logician/gates/f_daily_log_lock_block_missing.py` sha3_512[:16]=572762b4bd0d9faa |
| `logician.gates._protocols` | interface-contract | shared Protocol surface: `AuditArtifactReaderCallable`, `ClockProtocol`, `DailyLogReaderCallable`, `FileExistsCallable`, `LockHistoryReaderCallable`, `RouterConfigReaderCallable` — sha3_512[:16]=4f1ad18ae93afb9c |
| `logician.gates.__init__` | interface-contract | re-export surface for F_AMDT_01 / F_AMDT_06 / F_AMDT_07 / F_AMDT_07_AUTHOR_COLLISION / F_AMDT_12 / F_AMDT_12_MISSING / F_AMDT_12_MALFORMED / F_AMDT_12_READER_FAIL / four result dataclass families / four check functions / six Protocol aliases — sha3_512[:16]=11ad867f5ac0da5d |
| `failure-code.F-AMDT-01` | failure-code | §4.5 PRE-20 |
| `failure-code.F-AMDT-06` | failure-code | §4.5 PRE-21 |
| `failure-code.F-AMDT-07` | failure-code | §4.5 PRE-22 (v1 parent) |
| `failure-code.F-AMDT-07-AUTHOR-COLLISION` | failure-code | §4.5 PRE-22 (v1.1 sub-code) |
| `failure-code.F-AMDT-12` | failure-code | §4.6 POST-16 (parent) |
| `failure-code.F-AMDT-12-MISSING` | failure-code | §4.6 POST-16 (sub) |
| `failure-code.F-AMDT-12-MALFORMED` | failure-code | §4.6 POST-16 (sub) |
| `failure-code.F-AMDT-12-READER-FAIL` | failure-code | §4.6 POST-16 (sub) |

Forward-looking: F-INDEX-STALE PRE-gate in §0.5 v4 fires-closed if the paired commit is skipped. Authoring discipline: §0.5 v4 target-LOCK absorbs these rows in its next window; the `lock_history.v1.jsonl` rows for wave-2 reference this amendment path (`pipeline/blueprint/v0.1/section_04_v2_2_wave_2_amendment.md`) as `blueprint_section`.

# Evidence

- Spec cards: `pipeline/engineering/spec_cards/logician_v2_2_f_bootstrap_reuse.md`, `pipeline/engineering/spec_cards/logician_v2_2_f_deprecation_exemption_reuse.md`, `pipeline/engineering/spec_cards/logician_v2_2_f_amendment_self_reference_detect.md`, `pipeline/engineering/spec_cards/logician_v2_2_f_daily_log_lock_block_missing.md`.
- Code (per `companion_code` front-matter above).
- Tests (per `companion_tests` front-matter above): **366 new tests** across the four gates — 74 F-AMDT-01 (61 unit + 13 adv) + 106 F-AMDT-06 (52 unit + 54 adv) + 101 F-AMDT-07 (52 unit + 49 adv) + 85 F-AMDT-12 (41 unit + 44 adv). **100% coverage** on all four gate modules and the shared `_protocols.py` surface.
- Full suite regression: **2654 wave-1-post → 3123 wave-2-post** (+366 wave-2 tests + 103 interleaved non-logician work from Scout Rounds 2–6 + §5 Rounds 1–5 not tracked here). 3 skip, 1 xfail (unchanged). Zero failures on any committee dispatch cycle.
- AST-lint: R1–R7 clean (`scripts/run_lint.sh` exit 0) on all four gate modules at LOCK.
- Code Thesis Committee: **four independent 5-family all-pass cycle-1 verdicts**. Zero findings at any severity on any of the four gates. Retry notes:
  - F-AMDT-07 R2 llama: first attempt returned a tool-call validation error (Llama 3.3 attempted to emit verdict via an unexposed tool). Retried with explicit "Do NOT attempt to call any tools" suffix; clean PASS. Transport-retry; substantive verdict invariant.
  - F-AMDT-12 R1 qwen: first attempt returned `{"verdict": "PASS", ...}` with self-contradictory HIGH findings referencing fictional modules (`log_block_check.py`, `lock_checker.py`, `log_validate.py` — none exist in the review packet). Classic finding-field hallucination while the top-line verdict remained PASS. Retried without prompt change; clean PASS with empty findings. Substantive-invariant.
  - F-AMDT-12 R4 gemini-pro: first attempt returned a gateway-side "Agent couldn't generate a response" placeholder (transport artifact). Retried without prompt change; clean PASS. Substantive-invariant.
  - All retries counted as cycle-1 under the transport-retry carve-out (same discipline as wave-1).
- Committee synthesis artifacts:
  - `pipeline/validation/code_reviews/logician_v2_2_wave_2_f_amdt_01/synthesis.md`
  - `pipeline/validation/code_reviews/logician_v2_2_wave_2_f_amdt_06/synthesis.md`
  - `pipeline/validation/code_reviews/logician_v2_2_wave_2_f_amdt_07/synthesis.md`
  - `pipeline/validation/code_reviews/logician_v2_2_wave_2_f_amdt_12/synthesis.md`

# End of amendment
