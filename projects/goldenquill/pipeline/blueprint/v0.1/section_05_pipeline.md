# Blueprint Section 5 — Pipeline (v6 LOCKED 2026-04-19)

**Round 13 capstone LOCKED 2026-04-29 — §5 LOCKED-as-a-whole-section** (self-LOCK single-cycle; lock_history row 131; 5 test files / 3434 LOC / 280 tests at `tests/loop/{conftest_section_5.py, test_section_5_integration.py, test_section_5_invariants.py, test_section_5_bt5_rate_limit.py, test_section_5_fuzz_harness.py}`; concat sha3_512[:16] `b3e83a1e362dc3fc`; promotes §5 from LOCKED-per-module R1-R12.B to LOCKED-as-a-whole-section; 12th consecutive §5 single-cycle self-LOCK R3-R13). Memory: `project_impl_section_05_round_13_capstone_locked.md`.

**Status:** **LOCKED v6 2026-04-19.** L-005 two-audit cycle CLOSED 2026-04-19 on targeted amendment `pipeline/blueprint/v0.1/section_05_v6_amendment.md`. Editor (groq/llama-3.3-70b-versatile) REQUIRES_MINOR_FIXES (F1 success_flag range; F2 session_date sourcing) → fixes applied; Judge (groq/qwen/qwen3-32b) PASS 130/140 (92.9/100); Red Team (groq/openai/gpt-oss-120b) REQUIRES_MINOR_FIXES (RT-2 telemetry-write trust; RT-4 success_flag enforcement timing) → fixes applied; Reasoner (google/gemini-2.5-pro) INFO-only findings all justified in decision journal. Zero unresolved findings. v5 surface preserved; new surface: §3 module addition (pipeline.observability), §5.7 InvocationRecord schema (8 fields), §5.8 STR derivation + rolling-window aggregation, §6 F-PIPE-23, §8 two new constants + module-load integrity asserts, §9 five new tests (§9.36–§9.40), GPP run-lifecycle wiring paragraph. Parent pointer updated v6-r2 → v7 A1-A12. Paired §0.5 commit: 2 rows (per_invocation_telemetry_record_schema, str_derivation_and_aggregation). Item 2 (scope-close 2026-04-19) absorbed.

**v5 status (preserved):** **LOCKED v5 2026-04-18.** L-005 strict two-audit cycle CLOSED unanimous Thesis Team verdict on the verification round: Editor (meta/llama-3.3-70b-versatile) READY_TO_LOCK; Judge (alibaba/qwen3-32b) PASS 100/100 (140/140 raw, all 14 dimensions 10/10); Red Team (openai_oss/gpt-oss-120b) READY_TO_LOCK with zero new Bucket-A/B/C/OUT-OF-MODEL, all 11 v4 Group-1 findings explicitly verified closed, 18 attack vectors enumerated across families A–H all pinned to closing edits. V1 (TAB_ORDERING monkey-patch bypass) STILL CLOSED via §4.11 inline-literal check + §8 module-load assert; all 16 v1 Bucket-A STILL CLOSED; all 12 v2 Bucket-B STILL PRESERVED; all §10 OQ-1..OQ-9 STILL PRESERVED with new OQ-10 closed; all 6 v4 amendments STILL PRESERVED; parent pointers (Section 2 v7 + Section 4 v2) unchanged. Eleven v5 narrow-edits land Group-1 closures (schema-version enforcement + F-PIPE-22, realpath/symlink hardening, pubkey location + write-once + attestation, canonical-bytes exhaustiveness, F-EVAL-CROSS-ORG-READ predicate tightening to `run_state.operator_org_slug`, freshness check, module-load integrity for signing algorithm, OQ-10 ordering) entirely inside v4's existing surface (no new entry points, no new dataclasses, no new mechanisms). v0.2 hardening backlog (multi-tenant / hostile-tenant isolation, supply-chain subclass, snapshot-aware mount-over guard, etc.) captured at `pipeline/validation/blueprint_section_05_2026-04-18/05_synthesis_v5.md`. Audit trail: `pipeline/validation/blueprint_section_05_2026-04-18/{02..05}_*_v[1-5].*`.

**Parent architecture:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v7 A1-A12 LOCKED 2026-04-19). **Parent Section 2:** `pipeline/blueprint/v0.1/section_02_vault_topology.md` (LOCKED v7 2026-04-18; v7.1 parent-backfill pending). **Parent Section 3:** `pipeline/blueprint/v0.1/section_03_scout.md` (LOCKED v5 2026-04-17). **Parent Section 4:** `pipeline/blueprint/v0.1/section_04_logician.md` (LOCKED v2 2026-04-18; v2.1 parent-backfill pending).

**v0.1 NOTE — v7.0.7 LOCKED 2026-05-10 (Beta classification-driven routing) requires §5 next-spin accommodation.** v7.0.7 introduces (a) per-call routing decision based on input classification at every seat dispatch (Scribe / Editor / Judge / Red Team / Scout per channel — not §5's session-level routing); (b) Classification Review stage as a named pipeline stage between Intake (KFR ingestion) and Discovery (first grant cycle); (c) revision-loop accommodation — on revision, the routing layer re-evaluates classification per-call because input may have changed (slot-fill renders may have changed Confidential content into post-fill text). The next §5 spin (WS-G per the v0.2 dispatch plan — track-registry adoption) MUST formalize: (1) Classification Review stage placement in the pipeline phase diagram; (2) per-call routing-decision evaluation point in the seat-runner; (3) post-fill draft transition gate that switches subsequent seats to local-only routing; (4) F-CLASS-ROUTING-INDETERMINATE PRE-gate consumption per cycle start. Until WS-G LOCKs, the operational-today seat-runner uses the classification-aware logic carried in `skills/scribe-ghostwriter/SKILL.md` (per its 2026-05-10 update) and the §6 Operating Envelope's track-registry slot. Architectural commitment to v7.0.7 binds the WS-G LOCK at §5 v6 next-spin per L-006 dormant-binding pattern (matches A6 R.PF1 precedent).

**v5 audit trail (one line per round):**
- v1 driver (2026-04-18) — initial pipeline blueprint, Editor READY, Judge 100/100, Red Team REQUIRES_MAJOR_MITIGATIONS (16 Bucket-A); LOCK gate failed, opened v2.
- v2 verification (2026-04-18) — closed all 16 v1 Bucket-A; Editor READY, Judge 100/100, Red Team READY_TO_LOCK with V1 (TAB_ORDERING monkey-patch) raised; opened v3.
- v3 verification (2026-04-18) — closed V1 via §4.11 inline-literal + §8 module-load assert; Editor READY, Judge 100/100, Red Team READY_TO_LOCK; LOCKED v3 (preserved at `section_05_pipeline_v3_2026-04-18.md`).
- v4 driver (2026-04-19) — added eval_mode as second pipeline entry point; Editor READY, Judge 100/100, Red Team REQUIRES_MAJOR_MITIGATIONS (11 Bucket-A Group-1 + 9 OUT-OF-MODEL Group-2 + 6 process Group-3); LOCK gate failed, opened v5.
- v5 verification (2026-04-18) — closed all 11 Group-1 inside v4's surface; Editor READY, Judge 100/100, Red Team READY_TO_LOCK zero new findings; **LOCKED v5**.

---

## Original v5 verification-round authoring header (preserved for audit trail)

**Status at authoring:** v5 DRAFT — verification round, 2026-04-19. Section 5 v4 driver round (2026-04-19) authored eval_mode as second pipeline entry point; Editor=READY_TO_LOCK, Judge=PASS 100/100, Red Team=REQUIRES_MAJOR_MITIGATIONS surfacing 11 new Bucket-A and 10 new Bucket-B findings. The synthesis triaged findings against the v0.1 trusted-operator scope (A1–A4): Group-1 = 11 genuine spec gaps that warrant v5 narrow-edit; Group-2 = 9 OUT-OF-MODEL findings that assume operator attacks self (captured in v0.2 hardening backlog with same disposition v3 used for its 10 Bucket-B items); Group-3 = process discipline already addressed by sequencing. v5 is the verification round that closes Group-1 inside v4's existing surface area without expanding mechanisms. No new pipeline entry points, no new failure-code families, only spec-tightening + one new failure code F-PIPE-22 + one new constant family + nine new tests.

**Trust model and ownership rules carried forward unchanged from v3/v4:**
- v0.1 trusted-operator single-client-per-Golden-Quill (A1–A4).
- The operator is the only source of golden-set content. There is no central golden set, no shared eval pool, no telemetry of any kind.
- Golden sets and calibration reports are **node-local artifacts only**. They live under `orgs/{operator_org_slug}/vault/golden_set/` and are excluded by Cedar policy from every export, telemetry, or transfer bundle. Calibration reports never leave the Golden Quill they were authored on.

## v4 → v5 changelog (verification round, eleven narrow edits — all inside v4's existing surface)

**Verification scope: close v4 Red Team Group-1 findings.** v4 surfaced eleven genuine Bucket-A/B spec gaps that are real concerns even under A1–A4. v5 applies eleven narrow edits, each scoped tightly to a v4 surface that already exists. No new entry points, no new dataclasses, no new mechanisms beyond the listed eleven. The eleven v4→v5 edits are:

1. **§3.2.1 RunState resume-time schema enforcement.** Add `_assert_runstate_schema_current(rs)` predicate; called at the top of `resume_run` (§4.1). On `rs.schema_version != RUNSTATE_SCHEMA_VERSION` raise `F-PIPE-22.runstate_schema_downgrade` and write `state-failure` checkpoint. Closes MA-07 / Vec-6 / MB-05.
2. **§4.15 step 2 symlink + realpath hardening.** Replace string-prefix check on `golden_set_manifest_path` with `_resolve_golden_set_path(p, vault_prefix) -> Path`: calls `os.path.realpath` on both, rejects if either is symlink crossing the prefix boundary, asserts realpath is a strict child of `realpath(vault_prefix)`. Closes MB-02 / Vec-8 / MB-03 / Vec-9.
3. **§4.15 operator pubkey location specification.** Pubkey lives at `vault/{operator_org_slug}/calibration/keys/operator_pubkey.ed25519`; written exactly once per org via Section 2 v7 §4.6 `state-success` write-if-absent primitive; rotation requires explicit `key-rotation-write` intent (deferred to v0.2). On verify, predicate asserts the verified pubkey hash matches the stored hash recorded at first write (provenance attestation). Closes MA-09 / Vec-11.
4. **§5.6.4 CalibrationReport canonical-bytes enumeration.** New subsection enumerates every CalibrationReport field and its canonical-inclusion status. Default = canonical-included; explicit exclusion list = `{"signature": "the signature itself"}`. Note: `signed_at_iso` IS canonical-included (it must be in the signed payload for freshness). The v4 phrase "excludes signature + signed_at_iso" is corrected to "excludes signature only; signed_at_iso is part of canonical bytes". Closes MA-10 / Vec-13 / MB-07.
5. **§5.6 F-EVAL-CROSS-ORG-READ predicate tightening.** Predicate signature in §5.6 forward-dep contract changes from `assert read_org_slug == manifest_org_slug` to `assert read_org_slug == run_state.operator_org_slug`. The manifest's `org_slug` field is operator-supplied and untrusted; the run_state field was bound at `start_eval_run` against the trusted operator slug. Section 4 v2.1 backfill spec is updated to match. Closes MB-01 / Vec-7.
6. **§6 new failure code F-PIPE-22.** `runstate_schema_downgrade` with two trigger paths: (a) resume_run sees `rs.schema_version < RUNSTATE_SCHEMA_VERSION`, (b) `read_calibration_report` sees `report.schema_version != CALIBRATION_REPORT_SCHEMA_VERSION`. F-PIPE-22 evaluates BEFORE F-PIPE-18 (resume_phase_mismatch) — schema check precedes phase check. Closes MA-07 / MB-05.
7. **§7.16 new invariant — CalibrationReport canonical-bytes exhaustiveness.** Every field defined on CalibrationReport (and on every dataclass it transitively contains) must be either (a) included in the canonical-bytes payload, or (b) explicitly listed in the §5.6.4 exclusion table with a documented rationale. AST-grep test in §9.9 enforces. Closes MA-10 / MB-07.
8. **§8 constants — three additions + one module-load assert + one new frozenset constant.**
   - Add `MAX_CALIBRATION_AGE_DAYS: Final[int] = 90` for signature freshness window.
   - Add `CALIBRATION_KEY_PATH_TMPL: Final[str] = "vault/{operator_org_slug}/calibration/keys/operator_pubkey.ed25519"`.
   - Add `RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED: Final[frozenset[int]] = frozenset({1})` with module-load integrity assert mirroring V1 lesson.
   - Add module-load integrity assert for `CALIBRATION_SIGNING_ALGORITHM`: `assert CALIBRATION_SIGNING_ALGORITHM == "Ed25519", "CALIBRATION_SIGNING_ALGORITHM has been rebound at module load; refusing to load pipeline.config"`. Closes MA-11.
9. **§4.15 verify-time freshness check.** `verify_calibration_report` asserts `(now - datetime.fromisoformat(report.signed_at_iso)) < timedelta(days=MAX_CALIBRATION_AGE_DAYS)`. Stale signatures rejected with new failure subcode `F-PIPE-21.calibration_signature_stale`. Closes MB-06.
10. **§9.9 nine new tests (subsections 27–35):**
    - 9.9.27 `test_golden_set_path_unicode_normalization` — NFC/NFD path-traversal hardening test.
    - 9.9.28 `test_runstate_schema_downgrade_rejected_at_resume` — F-PIPE-22 path (a).
    - 9.9.29 `test_calibration_signing_algorithm_module_load_integrity` — module-load assert for the algorithm constant.
    - 9.9.30 `test_calibration_report_canonical_bytes_exhaustiveness` — AST-grep test that every field is canonical-included or explicitly excluded.
    - 9.9.31 `test_calibration_signature_stale_rejected` — F-PIPE-21.calibration_signature_stale path.
    - 9.9.32 `test_golden_set_symlink_rejected` — `_resolve_golden_set_path` rejects symlinks crossing prefix boundary.
    - 9.9.33 `test_golden_set_path_traversal_rejected` — `..` segment rejection via realpath.
    - 9.9.34 `test_operator_pubkey_write_once_per_org` — Section 2 write-if-absent primitive enforces.
    - 9.9.35 `test_forward_dep_predicate_mock_backfill` — mock-backfill for §5.6 forward-dep predicates so v5 doesn't depend on §2 v7.1 + §4 v2.1 landing first.
11. **§10 OQ-10 opened+closed.** OQ-10: in what order does F-PIPE-22 evaluate relative to F-PIPE-18 at `resume_run`? Closure: F-PIPE-22 evaluates BEFORE F-PIPE-18 — schema-version check is a precondition for phase-validation logic.

**No regression on v4.** All six v4 amendments preserved. V1 (TAB_ORDERING) closure preserved. All 16 v1 Bucket-A closures preserved. All 12 v2 Bucket-B landings preserved. All 9 v2-v4 §10 OQ closures preserved (8 from v2 + OQ-9 from v4). Forward parent-amendment contracts to Section 2 v7.1 + Section 4 v2.1 carry forward (with the v5 §5.6 predicate tightening flowing into the §4 v2.1 contract). No new mechanisms outside the listed eleven edits.

**v5 lock gate (L-005 strict verification round, single audit cycle):**
- Editor: READY_TO_LOCK (the eleven v4→v5 edits land cleanly; zero v4 regression; no scope creep beyond the listed eleven).
- Judge: ≥ 85/100 against the v3/v4 14-dimension rubric with dimension 14 renamed `v5_revision_discipline`.
- Red Team: READY_TO_LOCK with zero new Bucket-A AND explicit reconfirmation that V1 + 16 A-v1-* + 12 v2 Bucket-B + 9 §10 OQ closures + 6 v4 amendments remain unchanged.

If any of the three seat bars fail, v6 verification round opens.

## v3 → v4 changelog (single driver, six narrow edits — all eval_mode-scoped)

**Driver: eval_mode entry point.** v3 covered only `submission_mode` (RFA → council → signed bundle). v4 adds the per-operator local calibration harness as a peer entry point so the operator can score the council against their own past funded work, surface drift, and produce a signed calibration report — without ever shipping their data anywhere or polluting submission_mode pipelines. The six v3→v4 edits are:

1. **§1 Purpose** adds `eval_mode` as a second entry point alongside `submission_mode`. Same envelope discipline, different output contract: a signed `CalibrationReport`, never a `SubmissionBundle`.
2. **§3 Modules** adds module `pipeline.modes.eval_mode` (driver) and the `pipeline.calibration` package (report assembly + signing). Existing modules unchanged.
3. **§4 Mechanisms** adds new subsection §4.12 `eval_mode entry point and calibration-report assembly`. Existing §4.1–§4.11 mechanisms unchanged.
4. **§5 Interfaces** adds calibration-report schema + the two parent-dependency vault intents (`golden-set-read` + `golden-set-write`) declared as forward dependencies on Section 2 v7.1 (with the in-pipeline contract pinned here so the audit can verify the call sites are correct against the planned amendment).
5. **§6 Failure codes** adds `F-PIPE-21.calibration_report_in_submission_bundle` (pipeline-level shield: a calibration artifact appearing in any submission bundle is a hard-fail). Also declares forward dependency on Section 4 v2.1 introducing `F-EVAL-CROSS-ORG-READ` (PRE-gate failure code; Section 5 v4 cites it as the upstream failure that `eval_mode` halts on).
6. **§7 Invariants, §8 Constants, §9 Tests, §11 Law map** add the eval_mode-specific invariants, constants, property tests, and Law 3 + Law 5 enforcement bindings. §10 OQ list and §12 Non-ownership unchanged. §13 Closure updates to enumerate the parent-amendment forward-dependency contract.

**Parent-amendment forward dependencies (sequenced AFTER v4 LOCK):**
- **Section 2 v7.1** — Adds two write-intent allowlist rows: `golden-set-write` (operator-only, append-cas, audit-stamped) and `golden-set-read` (operator-only, read-only, audit-stamped). Backfill round = Editor + Judge only (no Red Team — attack surface for the new intents is fully audited inside Section 5 v4 driver round under the trusted-operator A1–A4 envelope; Section 2 backfill is a substrate amendment, not a behaviour amendment).
- **Section 4 v2.1** — Adds one PRE-gate failure code `F-EVAL-CROSS-ORG-READ` plus its enforcement check (PRE-gate refuses to enter eval_mode if `operator_org_slug ≠ requested_golden_set_org_slug`). Backfill round = Editor + Judge only (same rationale).

**No regression on v3.** All 16 v1 Bucket-A closures, all 12 v2 Bucket-B landings, the V1 (TAB_ORDERING monkey-patch) closure, all 8 §10 OQ closures, the §4.11 inline-literal check, the §8 module-load integrity assert, F-PIPE-01..F-PIPE-20, and parent-pointer upgrades to Section 2 v7 + Section 4 v2 carry forward unchanged. Audit seats verify zero regression.

**v4 lock gate (L-005 strict driver round, single audit cycle):**
- Editor: READY_TO_LOCK (the eval_mode additions land cleanly; zero v3 regression).
- Judge: ≥ 85/100 against the v3 14-dimension rubric with dimension 14 renamed `v4_revision_discipline` (driver discipline — eval_mode-only, no scope creep beyond the six changelog items).
- Red Team: READY_TO_LOCK with zero Bucket-A new findings AND explicit reconfirmation that V1 + all 16 A-v1-* + all 12 v2 Bucket-B + 8 OQ closures remain unchanged.

If any of these fail, v5 verification round opens (per L-005 strict two-audit cycle, a driver round that surfaces new findings opens a verification round; the full L-005 cycle re-engages).

---

**Prior status (carried from v2):** v1 scoping round closed 2026-04-18 with Editor=REQUIRES_MINOR_FIXES, Judge=PASS 98/100, Red Team=REQUIRES_MINOR_MITIGATIONS (16 Bucket-A findings, 20 Bucket-B, 10 Bucket-C). v2 narrow-edited v1 to close each Bucket-A by name, land 12 Bucket-B hardenings, close all §10 OQs, and satisfy the strict LOCK bar.

**Upstream locked context (unchanged from v1):**
- Architecture v5-r8 LOCKED 2026-04-17 → `pipeline/architecture/v0.1/tilth_architecture_locked.md`.
- Section 2 (Vault) v7 LOCKED 2026-04-18 → `pipeline/blueprint/v0.1/section_02_vault_topology.md`.
- Section 3 (Policy/Scout) LOCKED → `pipeline/blueprint/v0.1/section_03_*.md`.
- Section 4 (Logician) v2 LOCKED 2026-04-18 → `pipeline/blueprint/v0.1/section_04_logician.md`.

## v1 → v2 changelog (narrow edits only — every Bucket-A closed by name)

1. **A-v1-01 closure (run-state CAS exhaustion → silent loss of run).** §4.13 adds a `state-quarantine` recovery-marker write that lands BEFORE `F-PIPE-01` is raised; exponential back-off (50ms → 200ms → 800ms) inserted between CAS retries; §8 pins `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS = (50, 200, 800)`. The operator sees a structured quarantine message rather than a generic error.

2. **A-v1-02 closure (cross-family rigor bypass on fallback — ordering race).** §4.3/§4.4/§4.5 seat-invocation return signatures changed from `hash` to `(hash, landed_family, landed_model_id)` tuple. §4.6 revision loop updates `run_iteration_families_so_far` IMMEDIATELY after each seat returns and BEFORE calling the next seat. §4.9 `select_cascade_level` consults the live tuple, not a post-hoc reconstruction. New §9.3 property test forces Scribe fallback + asserts Editor/Judge never land on Scribe's actual family.

3. **A-v1-03 closure (BYOK key cache leakage across runs).** §3.5 banned-patterns adds: "no module-level caches of decrypted BYOK key material anywhere in `tilth/pipeline/`". §4.3 clarifies that seat subprocesses read their keys via Section 2 v7 §3.5 `seat_launch` session-binding, never from in-process caches. New §9.8 test uses `gc.get_objects()` post-run to assert no residual key-shaped bytes in the parent process.

4. **A-v1-04 closure (sign-off ceremony evasion via forced termination before checkpoint).** §4.1 step 8 reordered: transition to `signoff_pending` + atomic checkpoint BEFORE surfacing the operator prompt. If the checkpoint fails, the prompt is never shown and the run aborts with `F-PIPE-01`. §4.14 reaffirms idempotent prompt behaviour on resume.

5. **A-v1-05 closure (cron misfire double-run on stamp-write failure).** §4.10 adds a local flock file at `~/.tilth/cron_locks/{cron_task_id}.lock` that is acquired BEFORE the vault stamp-write. On vault write transient failure, the flock is retained for `CRON_VAULT_RETRY_WINDOW_SEC = 300` and the write is retried. Only on confirmed dedupe or successful stamp is the flock released. Two cron fires cannot both reach the radar-sweep step.

6. **A-v1-06 closure (three-tab envelope ordering violation).** §8 `TAB_ORDERING` declared `typing.Final[tuple[Literal["live_radar"], Literal["deep_brief"], Literal["council_draft"]]]` with a module-load integrity assert (v3 V1 closure). §4.11 envelope construction asserts `envelope.tab_ordering == ("live_radar", "deep_brief", "council_draft")` as an inline-literal comparison (v3 V1 closure) or raises `F-PIPE-16`. §9.7 adds AST-grep tests that scan the codebase for any `TabEnvelope(` call and verify the `tab_ordering=` argument references `TAB_ORDERING`, and that the envelope-ordering invariant check uses an inline literal tuple as the comparison RHS (not the module attribute).

7. **A-v1-07 closure (mid-loop gate call runtime bypass).** §4.6 loop body adds a runtime invariant: at every seat-call boundary, `assert run_state.phase.startswith("inner_loop_iter_")`. Belt-and-braces with Section 4 v2 §4.2.3 F-PRE-19 and the §3.5 banned-import static check.

8. **A-v1-08 closure (save-state-always violation on new-intent vault writes).** §4.13 adds the general rule: every `vault_write` call inside `tilth/pipeline/` is wrapped in a try/except that writes a `state-failure` checkpoint with the raised error code BEFORE re-raising. This applies whether or not the intent is in the Section 2 v7 allowlist. §10 OQ-1/OQ-2/OQ-3 closed by adopting the interim pattern: new intents (`draft-version-write`, `rate-limiter-snapshot`, `cron-fired-stamp`, `tab-envelope-write`) route through Section 2 v7 `state-success` with structured sub-payloads until Section 2 v8 extends the allowlist. A Section-2 v8 amendment proposal is filed as ARCH-07.

9. **A-v1-09 closure (rate-limiter token-bucket cross-process race).** §4.8 replaces in-process `threading.Lock` with a vault-based CAS lock. Reserve is now: `vault_read(rate_limiter/{endpoint}.json)` → compute new balance → `vault_write(write_mode="overwrite", expected_current_file_hash=...)` via Section 2 v7 §4. CAS mismatch triggers re-read and retry up to `CHECKPOINT_CAS_RETRY_MAX = 3`. §9.3 adds a property test simulating two processes reserving tokens concurrently; asserts total consumed never exceeds capacity.

10. **A-v1-10 closure (iteration-counter soft-restart loophole).** §4.6 adds explicit rule: once `run_state.phase` is `inner_loop_iter_N` with N≥1, any transition back to `inner_loop_iter_M` where M<N is rejected. New failure code `F-PIPE-19.soft_restart_forbidden` added to §6. §9.8 adds a test that synthesizes the soft-restart attempt and asserts the rejection.

11. **A-v1-11 closure (operator-interrupt race leaving half-written iteration).** §4.6 moves the interrupt check to AFTER each iteration's success-checkpoint write. The loop invariant becomes: "if the interrupt is observed, the current iteration's state is already checkpointed." Implementation in a helper `_check_interrupt_post_checkpoint(run_state)` — mandatory at every per-iteration boundary.

12. **A-v1-12 closure (resume-phase validation missing on post-gate-passed entry).** §4.1 `resume_run` formalises the allowed re-entry phase set: `{pre_gate_pending, pre_gate_passed, inner_loop_iter_1, inner_loop_iter_2, inner_loop_iter_3, post_gate_pending, signoff_pending, degraded_paused}`. Any other stored phase raises `F-PIPE-18.resume_phase_mismatch` and aborts the resume with a quarantine marker.

13. **A-v1-13 closure (BYOK key leakage via subprocess environment inheritance).** §4.3/§4.4/§4.5 explicitly state that `seat_launch` (Section 2 v7 §3.5) constructs a subprocess with a MINIMAL env (`PATH`, `HOME`, `TILTH_SESSION_ID`, `TILTH_RUN_ID`, `TILTH_ORG_SLUG` only). Keys are read INSIDE the seat subprocess via `vault_read` using the session binding. §9.8 adds a test that inspects the child's `/proc/{pid}/environ` (Linux) or `ps eww` (macOS) to assert no token-like strings are inherited.

14. **A-v1-14 closure (suggest-mode admission bypass when Cedar result missing).** §4.2 PRE-gate handler adds a post-return check: `PreGateResult.cedar_decision_ref` MUST be non-None before transitioning to `pre_gate_passed`. If None, raise new `F-PIPE-20.cedar_decision_missing`, write `state-failure` checkpoint, abort. Added to §6.

15. **A-v1-15 closure (Judge malformed JSON post-checkpoint iteration recorded as success).** §4.6 reorders per-iteration writes: the success checkpoint occurs AFTER Judge parse succeeds. If Judge parse fails after retry, the iteration is written as `state-failure` with `judge_verdict=None, failure_code=F-PIPE-09`. Never recorded as success.

16. **A-v1-16 closure (bypass-authorization loss on crash during graceful-degradation pause).** §4.12 adds: on entering `degraded_paused`, write a `bypass-pending` checkpoint BEFORE surfacing the operator prompt. On resume, the presence of `bypass-pending` is required to continue; if missing, refuse and require a fresh `start_run`.

**Bucket-B closures landed in v2:**

- **B-v1-02** — folded into A-v1-09.
- **B-v1-03** — §4.10 `cron_task_id` extended to `fund_radar_{YYYY-MM-DD}_{UTC_HH_MM}` to absorb DST double-fire; TTL of 36 h on stamp records.
- **B-v1-04** — §4.8 retry path adds exponential back-off + jitter. §8 pins `RATE_LIMIT_JITTER_RANGE_MS = (0, 300)`.
- **B-v1-05** — folded into A-v1-08.
- **B-v1-06** — §4.13 adds retry loop on transient `vault_read` errors (max 3, back-off 50/200/800 ms).
- **B-v1-08** — §3.2.1 `RunState` gains `schema_version: int = 1` field. §4.1 `resume_run` validates against current schema.
- **B-v1-09** — §4.11 adds post-write round-trip verification of tab envelope's `envelope_sha256`.
- **B-v1-10** — §4.8 CAS lock has lease TTL of 30s with explicit lease-holder identity; expired leases auto-release.
- **B-v1-13** — paired with A-v1-10 test in §9.8.
- **B-v1-14** — §4.1 `start_run` normalizes all text to Unicode NFC before hashing.
- **B-v1-15** — §4.13 adds `CHECKPOINT_TOTAL_TIMEOUT_SEC = 10` ceiling; CAS retries cap below that.
- **B-v1-17** — folded into A-v1-06 (`TAB_ORDERING: Final`).
- **B-v1-20** — §9.6 adds cron-during-signoff test.

Deferred (8 Bucket-B not landed, recorded for v0.1.1):
- B-v1-01 (per-org quotas — multi-client scope).
- B-v1-07 (operator-interrupt audit log — observability).
- B-v1-11 (cascade-level metrics — observability).
- B-v1-12 (router.yaml as runtime source — already stated).
- B-v1-16 (partial-write on large artifacts — Section 2 concern).
- B-v1-18 (clock-skew — ULIDs already suffice).
- B-v1-19 (artifact size limit — Section 2 concern, ARCH-08 filed).

All 10 Bucket-C items addressed via documentation polish in §4.8 / §4.9 / §4.10 and as observability TODOs.

**Section 10 OQs closed:**
- **OQ-1/OQ-2/OQ-3** — closed via interim `state-success` routing pattern + Section 2 v8 amendment proposal ARCH-07.
- **OQ-4** — closed by confirming Section 2 v7 §3.5 `seat_launch` returns a PID (and Section 5 owns the pipe-wrapping layer). Documented at §4.3.
- **OQ-5** — closed: `REVIEW_SEAT_OUTAGE_POLL_INTERVAL_MS = 300000` confirmed as v0.1 default; tuning in v0.1.1.
- **OQ-6** — closed: `config.load_overrides()` from `router.yaml` at boot confirmed; defaults in §8 stand as fallback.
- **OQ-7** — closed: "no soft restart" absolute; operator-issued restart requires a fresh `run_id`. F-PIPE-19 enforces.
- **OQ-8** — closed: LaunchAgent plist label set to `tilth.cron.fund_radar`; re-registration is `launchctl load -w` which replaces idempotently.

---

## §1 Purpose and Scope

### §1.1 Purpose

Section 5 is the Pipeline layer — the orchestration code that **runs** a Tilth council round under one of two entry-point modes:

- **`submission_mode`** (v1–v3, the default) — RFA ingestion through a signed rails report and three-tab delivery envelope. Produces a `SubmissionBundle`. This is what the operator runs to actually apply for a grant.
- **`eval_mode`** (v4 driver, the per-operator local calibration harness) — Operator-curated `golden_set` items (the operator's own past funded grants, ingested under their own org_slug) are scored against the live council to produce a signed `CalibrationReport`. eval_mode never produces a SubmissionBundle, never participates in any tab-delivery envelope, never appears in any export or telemetry, and is fully node-local. Its sole purpose is to let the operator measure their own council's drift, dialect alignment, and rubric-score stability against work whose true quality they already know.

Every Tilth output the operator sees passes through Section 5. Section 5 owns nothing the applicant sees directly; it owns the machinery that turns the six-seat council (per v7.0.6 SELF-LOCKED 2026-05-09), the three Logician gates, and the vault primitives into a single coherent run, in either mode.

Concretely, the Pipeline is the layer that:

1. Accepts an RFA + PROJECT_CONTEXT bundle (submission_mode) OR an operator-curated `golden_set` reference (eval_mode), mints a `run_id`, and initialises `RunState` with `mode ∈ {"submission", "eval"}`.
2. Invokes the Logician PRE gate via Section 4 §5.4 `gate_runner.run_pre_gate`. **eval_mode adds an upstream PRE-gate predicate `F-EVAL-CROSS-ORG-READ` (Section 4 v2.1 backfill) that hard-fails if `operator_org_slug ≠ requested_golden_set_org_slug`.**
3. Orchestrates the inner revision loop (Scribe → Editor → Judge) under the three-iteration cap from architecture §J. eval_mode runs the same loop against each golden-set item.
4. Invokes the Logician POST gate via Section 4 §5.4 `gate_runner.run_post_gate`.
5. Collects the operator sign-off via Section 4 §5.4 `gate_runner.operator_signoff`. eval_mode collects a calibration sign-off, not a submission sign-off.
6. **submission_mode only:** Emits the three-tab delivery envelope (Live Radar / Deep Brief / Council Draft) per architecture §J. eval_mode SHALL NOT emit a tab envelope (enforced by `F-PIPE-21.calibration_report_in_submission_bundle` and a Cedar-policy export-bundle exclusion rule).
7. **eval_mode only:** Assembles a signed `CalibrationReport` per §4.15, written to `vault/{org_slug}/golden_set/calibration_reports/` under intent `golden-set-write` (Section 2 v7.1 backfill).
8. Schedules the Monday 8:30 local-time fund-radar cron job per architecture §J. (submission_mode plumbing; eval_mode is operator-triggered, not scheduled.)
9. Enforces cross-family rigor at every provider-cascade level (architecture §E / M5) in both modes.
10. Saves state on every iteration — success or failure — per AR-1 save-state-always.
11. Surfaces graceful degradation when a provider family is exhausted, per architecture §M10 / §M13.

### §1.2 Ownership (the 10 Section-5 surfaces)

Section 5 owns and is the unique author of:

1. **Revision-loop control** (§4.6) — the bounded three-iteration Scribe → Editor → Judge loop, its counter, its convergence detection, its exit paths. v2: soft-restart forbidden (F-PIPE-19); interrupt check is post-checkpoint only.
2. **Council-seat orchestration** (§4.3, §4.4, §4.5) — the code that spawns a seat subprocess, streams its output, enforces its timeout, and parses its structured return. v2: seat invocation returns `(hash, landed_family, landed_model_id)` tuple; subprocess env is minimal; no in-process key caches.
3. **Provider rate limiting** (§4.8) — the BT5-owned `RateLimiterState` and token-bucket algorithm per provider family. v2: CAS-based vault lock with 30s lease TTL; exponential back-off with jitter on 429.
4. **Provider cascade** (§4.9) — the fallback chain that honours cross-family rigor. Judge's cascade MUST NOT land on a Scribe-family model. v2: landed families recorded immediately on seat return; consulted live on next selection.
5. **Cron scheduler** (§4.10) — the Monday 8:30 local-time trigger that runs Scout's fund-radar sweep. v2: local flock + vault stamp two-layer dedupe; DST-safe task-id.
6. **Three-tab delivery** (§4.11) — Live Radar / Deep Brief / Council Draft envelope with a tab-ordering invariant. v2: `TAB_ORDERING: Final`; post-write envelope-hash verification.
7. **Run-state machine** (§4.1, §4.13) — the `RunState` object, its persistence to the vault, and its resume-from-checkpoint semantics. v2: allowed resume phases formalised; schema_version pinned; quarantine-marker on CAS exhaustion.
8. **Graceful degradation** (§4.12) — the Ollama-fallback contract when a review-seat family goes dark; the review-seat-outage escape valve from architecture §M13. v2: `bypass-pending` checkpoint precedes the operator prompt.
9. **Iteration-cap mechanics** (§4.6) — the counter, the overflow rejection, the soft-restart prohibition. v2: F-PIPE-19 enforces.
10. **Run lifecycle** (§4.1) — the end-to-end state transitions from `run_id` minted → report signed → tabs delivered → state vaulted. v2: Unicode NFC normalization at `start_run`; Cedar-decision-ref check before inner loop.

### §1.3 Non-goals (unchanged from v1; v4 adds eval_mode non-goals)

Section 5 does not own, define, or silently re-implement any of: gate logic (Section 4 v2 §5.4), vault reads/writes (Section 2 v7 §4), Cedar policy evaluation (Section 3), seat-internal reasoning (each seat's identity skill), provider keys (Section 2 v7 §5), the Five Operating Laws / Four Autonomy Rules themselves (architecture §L defines; Section 4 enforces; Section 5 calls the gates at the right times).

**v4 eval_mode non-goals (explicit):**
- eval_mode is **not** a benchmark, leaderboard, or shared-dataset mechanism. No golden-set data or calibration report leaves the operator's Golden Quill under any pipeline path.
- eval_mode is **not** a sync layer. There is no central golden set, no cross-operator comparison, no shared rubric tuning in v0.1.
- eval_mode is **not** a submission-mode substitute. A CalibrationReport CANNOT satisfy any funder's submission contract; any code path that would promote a calibration artifact into a submission bundle raises `F-PIPE-21`.
- eval_mode is **not** a training mechanism for any model. The operator reads calibration reports to adjust their own curation + router.yaml choices; no model weights, LoRAs, or fine-tunes are generated.
- eval_mode is **not** exempt from Law 3 org-isolation. Every golden-set read requires `operator_org_slug == requested_golden_set_org_slug`; mismatch raises `F-EVAL-CROSS-ORG-READ` at the PRE-gate (Section 4 v2.1 backfill).

## §2 Acceptance Criteria

Section 5 v0.1 is complete and shippable iff:

1. **End-to-end council round** — given a valid `(RFA, PROJECT_CONTEXT)` pair, Section 5 produces a signed rails report + three-tab envelope + vaulted state without operator intervention beyond the two sign-off prompts.
2. **Three-iteration cap enforced** — no run exceeds `MAX_REVISION_ITERATIONS = 3`; soft-restart raises `F-PIPE-19`.
3. **Cross-family rigor preserved at cascade** — in every provider-cascade path, Judge's landed family differs from both Scribe's and Editor's landed families. Tested in §9.3.
4. **Cron idempotency** — Monday 8:30 cron trigger dedupes via (flock + vault stamp) on `(run_id_date, cron_task_id)`; double-firing never produces two radar sweeps.
5. **Checkpoint atomicity at the envelope layer** — every iteration boundary writes a single atomic CAS-swap via Section 2 v7 §4 primitives; resume-from-checkpoint restores to the last successful envelope boundary; CAS exhaustion writes a `state-quarantine` marker before aborting.
6. **Save-state-always (AR-1)** — every failure path in §6 writes a failure checkpoint with intent `state-failure` before returning the error. Applies regardless of whether the intent is in the Section 2 v7 allowlist — the wrapper catches vault-write-rejection too.
7. **Graceful-degradation escape valve wired** — review-seat outage triggers `bypass-pending` checkpoint, then operator prompt, then `admin_risk.record_bypass_authorization`. Never silently routes to an in-family reviewer.
8. **Banned-import static check passes** — Section 5 does not import Section 4 inner-loop modules; CI lint covers `seat_runner.py` and `revision_loop.py`.
9. **20 failure codes enumerated** — every `F-PIPE-*` code in §6 has a unique trigger, a severity tier, a save-state contract, and a test in §9. v2 added F-PIPE-19 and F-PIPE-20.
10. **Three-tab delivery ordering invariant** — `tab_ordering` is always the `TAB_ORDERING: Final` constant tuple; AST-grep test rejects any inline ordering tuple.
11. **Subprocess env is minimal** — seat subprocesses receive `PATH`, `HOME`, `TILTH_SESSION_ID`, `TILTH_RUN_ID`, `TILTH_ORG_SLUG` only. BYOK material is read inside the subprocess via `vault_read`.
12. **Rate-limiter race-safe** — concurrent processes reserving tokens share a vault-CAS lock with 30s lease TTL; no over-consumption under simulated concurrency.
13. **Operator sign-off ceremony race-safe** — `signoff_pending` checkpoint lands BEFORE the prompt; force-quit always resumes to the prompt.
14. **(v4) eval_mode is mode-isolated** — a run initialised with `mode="eval"` CANNOT at any point produce a `SubmissionBundle`, enter the three-tab delivery path (§4.11), or write under any intent other than `golden-set-write` or `state-success` / `state-failure`. Any such transition raises `F-PIPE-21` and writes a `state-failure` checkpoint.
15. **(v4) eval_mode is org-isolated (Law 3)** — a run with `mode="eval"` fails-closed at PRE-gate if `operator_org_slug ≠ requested_golden_set_org_slug`. The check is the Section 4 v2.1 PRE-gate predicate `F-EVAL-CROSS-ORG-READ`; Section 5 surfaces this by routing eval_mode runs through the same `gate_runner.run_pre_gate` and aborting on any `F-EVAL-*` return.
16. **(v4) CalibrationReport is signed and non-exportable** — every CalibrationReport is BT13-style signed (detached signature in `orgs/{slug}/vault/golden_set/calibration_reports/{run_id}.sig`) and excluded from every export / telemetry / transfer bundle by Cedar policy. The exclusion rule is enforced at the Cedar-policy layer (Section 3) AND by the `F-PIPE-21` pipeline-level shield (defence-in-depth).

## §3 Modules

### §3.1 Owned files

Under `tilth/pipeline/` (unchanged from v1):

| Path | Role |
|------|------|
| `tilth/pipeline/__init__.py` | Package marker + public re-exports |
| `tilth/pipeline/run_lifecycle.py` | §4.1 — `start_run`, `resume_run`, `finalize_run` |
| `tilth/pipeline/revision_loop.py` | §4.6 — bounded inner loop, convergence detection, interrupt post-checkpoint |
| `tilth/pipeline/seat_runner.py` | §4.3/§4.4/§4.5 — subprocess spawn (minimal env), stdout/stderr capture, structured return tuple |
| `tilth/pipeline/rate_limiter.py` | §4.8 — vault-CAS-lock-protected token bucket (BT5) |
| `tilth/pipeline/provider_cascade.py` | §4.9 — fallback chain + live cross-family rigor guard |
| `tilth/pipeline/cron_scheduler.py` | §4.10 — Monday 8:30 fire, flock + vault-stamp two-layer dedupe |
| `tilth/pipeline/three_tab_delivery.py` | §4.11 — tab envelope + ordering invariant + post-write hash verify |
| `tilth/pipeline/graceful_degradation.py` | §4.12 — Ollama-fallback + `bypass-pending` checkpoint + escape valve |
| `tilth/pipeline/state_checkpoint.py` | §4.13 — atomic CAS-swap envelope + quarantine marker + read-retry |
| `tilth/pipeline/signoff_plumbing.py` | §4.14 — operator prompt relay (idempotent on resume) |
| `tilth/pipeline/types.py` | §3.2 — dataclasses with v2 schema_version (v4 adds `mode` field on `RunState`) |
| `tilth/pipeline/errors.py` | §6 — the 21 `F-PIPE-*` exception classes (v4 adds F-PIPE-21) |
| `tilth/pipeline/config.py` | §8 — pinned constants + router.yaml override loader |
| `tilth/pipeline/tests/` | §9 — nine test categories + v2 additions + v4 §9.9 eval-mode tests |
| **(v4)** `tilth/pipeline/modes/__init__.py` | Package marker for the two entry-point drivers |
| **(v4)** `tilth/pipeline/modes/submission_mode.py` | Driver for submission_mode (refactored shell over the existing `run_lifecycle.start_run` happy path; behaviour unchanged from v3) |
| **(v4)** `tilth/pipeline/modes/eval_mode.py` | §4.15 — Driver for eval_mode (golden-set iteration + calibration-report assembly + signing) |
| **(v4)** `tilth/pipeline/calibration/__init__.py` | Package marker |
| **(v4)** `tilth/pipeline/calibration/report.py` | §5.6 — `CalibrationReport` dataclass + canonical-bytes + parse |
| **(v4)** `tilth/pipeline/calibration/signing.py` | §4.15 — BT13-style detached signature for CalibrationReport |
| **(v4)** `tilth/pipeline/calibration/golden_set.py` | §4.15 — `golden_set_iter(org_slug, run_id) -> Iterator[GoldenSetItem]` reading via `vault_read(intent="golden-set-read", ...)` (Section 2 v7.1 forward dep) |
| **(v4)** `tilth/pipeline/tests/test_eval_mode/` | §9.9 — eval-mode property + integration + failure tests |

### §3.2 Owned data structures

#### §3.2.1 `RunState` (v2 adds `schema_version`; v4 adds `mode` + eval-mode phases + calibration_report ref)

```python
@dataclass(slots=True)
class RunState:
    schema_version: int                         # v2: pinned to 1; v4: bumped to 2 (mode field added)
    run_id: str
    mode: Literal["submission", "eval"]         # v4: pipeline entry-point mode; frozen at start_run
    rfa_hash: str | None                        # v4: None when mode == "eval"
    project_context_hash: str | None            # v4: None when mode == "eval"
    golden_set_ref: str | None                  # v4: vault path to operator's golden-set manifest; None when mode == "submission"
    org_slug: str
    session_id: str
    phase: Literal[
        "initialized",
        "pre_gate_pending",
        "pre_gate_passed",
        "inner_loop_iter_1",
        "inner_loop_iter_2",
        "inner_loop_iter_3",
        "post_gate_pending",
        "post_gate_passed",
        "signoff_pending",
        "report_signed",
        "tabs_delivered",                       # NEVER reached in eval_mode (mode-isolation invariant §7.13)
        "finalized",
        "degraded_paused",
        "aborted_trusted_fail",
        "aborted_operator",
        "quarantined",                          # v2: CAS-exhaustion recovery state
        # v4: eval-mode-only phases
        "eval_iter_pending",                    # v4: between golden-set items
        "calibration_assembled",                # v4: CalibrationReport built, awaiting sign
        "calibration_signed",                   # v4: detached signature written
        "eval_finalized",                       # v4: terminal eval-mode success
    ]
    iterations: list[IterationState]
    active_cascade: ProviderCascade
    rate_limiter_snapshot: RateLimiterState
    run_iteration_families_so_far: dict[str, tuple[str, str]]  # v2: {seat_kind: (family, model_id)} live
    started_at_iso: str
    last_checkpoint_iso: str
    pre_gate_result_hash: str | None
    post_gate_result_hash: str | None
    signed_claim_evidence_map_hash: str | None
    three_tab_envelope_hash: str | None         # v4: MUST remain None in eval_mode
    bypass_authorization_ref: str | None
    bypass_pending_checkpoint_ref: str | None   # v2: set on entering degraded_paused
    quarantine_marker_ref: str | None           # v2: set on CAS exhaustion
    calibration_report_ref: str | None          # v4: vault path to signed CalibrationReport; MUST remain None in submission_mode
    calibration_signature_ref: str | None       # v4: vault path to detached signature; MUST remain None in submission_mode
```

**v4 mode-discriminated-union invariants (enforced at `start_run` and at every checkpoint via §4.1 / §4.15):**
- `mode == "submission"` ⟹ `rfa_hash` and `project_context_hash` are non-None; `golden_set_ref`, `calibration_report_ref`, `calibration_signature_ref` are all None.
- `mode == "eval"` ⟹ `golden_set_ref` is non-None; `rfa_hash`, `project_context_hash`, `three_tab_envelope_hash` are all None; calibration fields are populated only after their respective phase transitions.
- A run's `mode` is frozen at `start_run`; no subsequent transition may change it. Attempting a mode change raises `F-PIPE-21`.

#### §3.2.2 `IterationState` (unchanged from v1)

(Carried from v1 §3.2.2; no v2 edit.)

#### §3.2.3 `SeatCharter` (unchanged)

#### §3.2.4 `ProviderCascade` (unchanged)

#### §3.2.5 `RateLimiterState` (v2 adds lease fields)

```python
@dataclass(slots=True)
class RateLimiterState:
    buckets: dict[str, TokenBucket]
    last_refill_iso: str
    lease_holder_id: str | None                 # v2: which process holds the reserve lock
    lease_expires_at_iso: str | None            # v2: 30s TTL
```

#### §3.2.6 `TabEnvelope` (v2: `tab_ordering` typed `Final`)

```python
@dataclass(frozen=True, slots=True)
class TabEnvelope:
    run_id: str
    tab_ordering: tuple[Literal["live_radar"], Literal["deep_brief"], Literal["council_draft"]]
    live_radar_payload_hash: str
    deep_brief_payload_hash: str
    council_draft_payload_hash: str
    assembled_at_iso: str
    envelope_sha256: str
    # post-write verification: assemble_and_deliver re-reads and confirms envelope_sha256 matches
```

### §3.3 Internal entrypoints (unchanged from v1)

### §3.4 Dependency graph (unchanged from v1)

### §3.5 Banned imports and banned patterns (v2 extends v1)

`tilth/pipeline/revision_loop.py` and `tilth/pipeline/seat_runner.py` MUST NOT import:
- `tilth.logician.gate_runner` / `tilth.logician.admin_risk` / `tilth.logician.*`
- `tilth.seats.scribe` / `tilth.seats.editor` / `tilth.seats.judge` Python modules

**v2 banned patterns (CI lint rule, AST-based):**
- No module-level globals named `KEY`, `SECRET`, `TOKEN`, `API_KEY`, `BEARER`, or matching pattern `*_KEY$` / `*_SECRET$` / `*_TOKEN$` anywhere in `tilth/pipeline/`. (A-v1-03 closure.)
- No module-level `dict` or `cache` variable that is mutated from within a function named `*reserve*`, `*load_key*`, `*get_key*`. (Defence-in-depth against cache-leakage refactors.)
- No `TabEnvelope(` call with an inline tuple or list as the `tab_ordering` argument; must reference `TAB_ORDERING`. (A-v1-06 closure.)

These are enforced by `tilth/pipeline/tests/test_banned_patterns.py` at CI time.

## §4 Mechanisms

### §4.1 Run lifecycle (v2 adds NFC normalization, resume-phase validation, ordered signoff checkpoint)

**Trigger:** as v1.

**Sequence (happy path, v2 edits marked):**

1. `start_run` reads the RFA and PROJECT_CONTEXT; **v2: applies Unicode NFC normalization to text content before canonicalization (B-v1-14 closure)**; computes SHA-256 hashes; mints ULID `run_id`; constructs `RunState(schema_version=1, ...)` in phase `initialized`.
2. `state_checkpoint.checkpoint_atomic(run_state, intent="state-success")` via Section 2 v7 §4 `vault_write(write_mode="write-if-absent")`.
3. Transition to `pre_gate_pending` + checkpoint.
4. Call `gate_runner.run_pre_gate(...)` from Section 4 v2 §5.4. **v2: check that `PreGateResult.cedar_decision_ref` is not None (A-v1-14 closure); if None, raise `F-PIPE-20.cedar_decision_missing`.** On PASS, transition to `pre_gate_passed` + checkpoint.
5. Call `revision_loop.run_inner_loop(run_state)` (§4.6).
6. Transition to `post_gate_pending` + checkpoint.
7. Call `gate_runner.run_post_gate(...)` from Section 4 v2 §5.4.
8. **v2 (A-v1-04 closure): transition to `signoff_pending` + atomic checkpoint BEFORE surfacing the operator prompt. If the checkpoint write fails, raise `F-PIPE-01` immediately; do NOT show the prompt.**
9. Call `gate_runner.operator_signoff(...)`.
10. Transition to `report_signed` + checkpoint.
11. `three_tab_delivery.assemble_and_deliver(run_state)` (§4.11) with post-write envelope-hash verification (B-v1-09 closure). Transition to `tabs_delivered` + checkpoint.
12. Transition to `finalized` + final checkpoint.

**Resume path (v2, A-v1-12 closure; v5 MA-07/MB-05 closure adds schema-version enforcement BEFORE phase check):** `resume_run(run_id)` reads the last checkpoint and validates, in this exact order:

1. **(v5, FIRST)** `_assert_runstate_schema_current(rs)`: inline predicate (zero branches, inline-literal comparison mirroring V1 discipline) that raises `F-PIPE-22.runstate_schema_downgrade` if `rs.schema_version != RUNSTATE_SCHEMA_VERSION` OR `rs.schema_version in RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED`. On raise, a `state-failure` checkpoint is written BEFORE re-raise. Schema-version check precedes phase check because a downgraded schema may have renamed or removed the `phase` field itself — you cannot validate `phase` against a schema you don't trust. See §10 OQ-10 closure.
2. `run_state.phase ∈ {pre_gate_pending, pre_gate_passed, inner_loop_iter_1..3, post_gate_pending, signoff_pending, degraded_paused}`. Any other phase raises `F-PIPE-18.resume_phase_mismatch` and writes a `state-quarantine` marker. (v5: eval_mode adds its own phase set — `eval_phase ∈ {eval_pre_gate_pending, eval_pre_gate_passed, eval_item_iter_running, eval_report_assembly, eval_signed}` is accepted in resume validation when `rs.mode == "eval"`.)
3. If `phase == degraded_paused`, the `bypass_pending_checkpoint_ref` MUST be present (A-v1-16 closure); absence raises `F-PIPE-18`.

The helper predicate is defined once in `pipeline.state.schema` and is module-load asserted:

```python
RUNSTATE_SCHEMA_VERSION: Final[int] = 2  # v4 bumped from 1 to 2 for mode/eval-phase extension
RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED: Final[frozenset[int]] = frozenset({1})

def _assert_runstate_schema_current(rs: RunState) -> None:
    # Inline-literal comparison — monkey-patch resistant, V1 discipline
    if rs.schema_version != 2:
        raise PipelineFailure(
            "F-PIPE-22",
            trigger="runstate_schema_downgrade",
            details={"observed": rs.schema_version, "expected": 2},
        )
    if rs.schema_version in frozenset({1}):
        raise PipelineFailure(
            "F-PIPE-22",
            trigger="runstate_schema_downgrade",
            details={"observed": rs.schema_version, "reason": "legacy version explicitly rejected"},
        )
```

(Both checks use inline-literal comparands so a module-attribute rebinding of `RUNSTATE_SCHEMA_VERSION` cannot bypass the runtime assert — V1 discipline applied to the schema-version constant. See §8 module-load integrity asserts.)

**Operator-interrupt semantics (v2, A-v1-11 closure):** the interrupt poll runs every `OPERATOR_INTERRUPT_POLL_INTERVAL_MS = 500` ms, but the interrupt HANDLER is only invoked from a `_check_interrupt_post_checkpoint(run_state)` helper that is called at each per-iteration boundary AFTER the iteration's success-checkpoint has been written. An interrupt observed mid-subprocess still lets the subprocess complete and its results checkpoint; only then is the interrupt consumed and the loop exits with `F-PIPE-11`.

### §4.2 PRE-gate invocation (v2 adds Cedar-decision check)

Per v1 §4.2, with v2 addition: after `PreGateResult` is returned PASS, Section 5 verifies `PreGateResult.cedar_decision_ref is not None`. Missing cedar decision raises `F-PIPE-20.cedar_decision_missing`, writes `state-failure`, aborts to `aborted_trusted_fail`.

### §4.3 Scribe invocation (v2 adds tuple return + minimal-env subprocess)

**Contract (v2):** Scribe takes `(rfa_bundle, project_context, iteration_number, editor_critique_prev | null, judge_score_prev | null)` and returns **`(draft_hash: str, landed_family: str, landed_model_id: str)` tuple** — v2 A-v1-02 closure.

**Mechanism (v2 edits):**

1. Load `SeatCharter` for `seat_kind="scribe"`.
2. Rate-limit check: `rate_limiter.reserve(...)` — now vault-CAS-lock-backed (§4.8 v2).
3. **v2: subprocess spawn via `seat_launch` uses a MINIMAL env: `PATH`, `HOME`, `TILTH_SESSION_ID`, `TILTH_RUN_ID`, `TILTH_ORG_SLUG`, `TILTH_SEAT_KIND`. No decrypted keys, no API tokens in env. The subprocess reads its BYOK inside via `vault_read` using the session binding.** (A-v1-13 closure.)
4. Stream stdout; on exit, parse structured return per v1 clean-output discipline.
5. Write the draft to vault: `vault_write(path=..., intent="state-success", payload=structured_draft_sub_payload, ...)` — **v2: until Section 2 v8 adds `draft-version-write` to the allowlist, Section 5 uses `state-success` with a structured sub-payload** (A-v1-08 / OQ-1 closure interim pattern). On `vault_write` failure, the try/except wrapper writes a `state-failure` checkpoint BEFORE re-raising.
6. Return `(draft_hash, charter.primary_provider_family if level_0 else actual_landed_family, actual_landed_model_id)`.

**Timeout:** `SCRIBE_SUBPROCESS_TIMEOUT_MS = 300_000`. Timeout kills subprocess, checkpoint-failure `F-PIPE-07`, cascade advances.

### §4.4 Editor invocation (v2 mirrors §4.3 v2 edits)

Identical to §4.3 with: `seat_kind="editor"`, `EDITOR_SUBPROCESS_TIMEOUT_MS = 180_000`, cross-family constraint validated at charter-load (mismatch raises `F-PIPE-08`), and minimal-env subprocess launch.

### §4.5 Judge invocation (v2 mirrors §4.3 v2 edits; judge parse checkpoint ordering fixed)

Identical to §4.3 with: `seat_kind="judge"`, `JUDGE_SUBPROCESS_TIMEOUT_MS = 180_000`, three-way cross-family constraint, minimal-env subprocess launch, and **v2 (A-v1-15 closure): the iteration's success-checkpoint is written AFTER Judge parse succeeds. If Judge parse fails after retry, the iteration is written as `state-failure` with `judge_verdict=None, failure_code=F-PIPE-09`.**

### §4.6 Revision-loop control (v2 A-v1-02 / A-v1-07 / A-v1-10 / A-v1-11 / A-v1-15 closures)

```python
def run_inner_loop(run_state: RunState) -> IterationState:
    prev_editor_critique = None
    prev_judge_score = None
    for iter_n in (1, 2, 3):
        # A-v1-10: soft-restart guard
        if any(it.iter_number >= iter_n for it in run_state.iterations):
            raise F_PIPE_19_soft_restart_forbidden(run_state, iter_n)

        # A-v1-07: phase assertion at boundary
        assert run_state.phase.startswith("inner_loop_iter_"), \
            "inner loop body invoked with phase not inner_loop_iter_*"

        run_state.phase = f"inner_loop_iter_{iter_n}"
        checkpoint_atomic(run_state, intent="state-success")

        try:
            # A-v1-02: seat invocations return tuples; record landed families IMMEDIATELY
            scribe_hash, scribe_family, scribe_model = invoke_scribe(
                run_state, iter_n, prev_editor_critique, prev_judge_score
            )
            run_state.run_iteration_families_so_far["scribe"] = (scribe_family, scribe_model)

            editor_hash, editor_family, editor_model = invoke_editor(
                run_state, iter_n, scribe_hash
            )
            run_state.run_iteration_families_so_far["editor"] = (editor_family, editor_model)

            judge_result = invoke_judge(run_state, iter_n, scribe_hash, editor_hash)
            # judge_result.landed_family is consulted by cascade before invocation
            run_state.run_iteration_families_so_far["judge"] = (judge_result.landed_family, judge_result.landed_model)

        except JudgeParseError as err:
            # A-v1-15: parse failure → state-failure, never recorded as success
            iteration_state = IterationState(
                iter_number=iter_n,
                judge_verdict=None,
                failure_code="F-PIPE-09",
                ...,
            )
            run_state.iterations.append(iteration_state)
            checkpoint_atomic(run_state, intent="state-failure")
            raise

        except PipelineError as err:
            iteration_state = IterationState(
                iter_number=iter_n,
                failure_code=err.code,
                ...,
            )
            run_state.iterations.append(iteration_state)
            checkpoint_atomic(run_state, intent="state-failure")
            raise

        # A-v1-15: success-checkpoint AFTER parse success
        iteration_state = IterationState(
            iter_number=iter_n,
            scribe_draft_hash=scribe_hash,
            editor_critique_hash=editor_hash,
            judge_score_hash=judge_result.hash,
            judge_total_score=judge_result.total_score,
            judge_verdict=judge_result.verdict,
            ...,
        )
        run_state.iterations.append(iteration_state)
        checkpoint_atomic(run_state, intent="state-success")

        # A-v1-11: interrupt check is POST-checkpoint
        _check_interrupt_post_checkpoint(run_state)

        # Convergence checks (unchanged from v1)
        if judge_result.verdict == "PASS":
            iteration_state.converged_on = "score_threshold"
            return iteration_state
        if iter_n >= 2 and _delta_plateau(run_state.iterations):
            iteration_state.converged_on = "delta_plateau"
            return iteration_state
        prev_editor_critique = editor_hash
        prev_judge_score = judge_result.hash

    last = run_state.iterations[-1]
    last.converged_on = "cap_reached"
    checkpoint_atomic(run_state, intent="state-failure")
    raise F_PIPE_05_iteration_cap_exceeded(run_state)
```

**Convergence rules (unchanged from v1):** score-threshold PASS, delta-plateau at ≥75, cap-reached FAIL with F-PIPE-05.

**v2 additions:**
- **A-v1-02** landed-family is recorded on the seat-return line, before the next seat is invoked. The provider_cascade's `select_cascade_level` reads `run_state.run_iteration_families_so_far` live.
- **A-v1-07** phase-invariant assertion at every boundary (belt-and-braces with Section 4 §4.2.3 F-PRE-19).
- **A-v1-10** soft-restart guard: if any existing `IterationState.iter_number >= iter_n`, raise F-PIPE-19. (Protects against `run_state.iterations` being reset by an adversary.)
- **A-v1-11** interrupt check is POST-checkpoint — `_check_interrupt_post_checkpoint` only fires after a full iteration has successfully checkpointed.
- **A-v1-15** success checkpoint happens after Judge parse succeeds; parse failure writes `state-failure` with `judge_verdict=None`.

### §4.7 POST-gate invocation (unchanged from v1)

### §4.8 Provider rate limiting (v2: vault-CAS lock, lease TTL, back-off jitter)

**v2 reserve algorithm (A-v1-09 closure + B-v1-02 / B-v1-04 / B-v1-10 closures):**

```python
def reserve(endpoint: str, estimated_tokens: int) -> ReservationResult:
    for attempt in range(CHECKPOINT_CAS_RETRY_MAX):
        # Read current bucket state via vault (single source of truth)
        bucket_bytes, current_hash = vault_read(
            path=f"pipeline/rate_limiter/{endpoint}.json",
            session_id="system", slug="rate_limiter",
            return_hash=True,
        )
        state = RateLimiterState.parse(bucket_bytes)

        # Expired lease auto-release (B-v1-10)
        if state.lease_holder_id and state.lease_expires_at_iso and _is_past(state.lease_expires_at_iso):
            state.lease_holder_id = None
            state.lease_expires_at_iso = None

        # Lease acquisition
        if state.lease_holder_id and state.lease_holder_id != PROCESS_ID:
            time.sleep(_backoff_with_jitter(attempt))  # B-v1-04
            continue

        # Refill
        _refill(state)

        if state.buckets[endpoint].current_tokens < estimated_tokens:
            return InsufficientTokens()

        # Reserve
        state.buckets[endpoint].current_tokens -= estimated_tokens
        state.lease_holder_id = PROCESS_ID
        state.lease_expires_at_iso = _iso_now_plus(30)  # 30s lease TTL

        try:
            vault_write(
                path=..., bytes_=state.canonical(),
                intent="state-success",  # interim pattern until rate-limiter-snapshot intent lands (OQ-2)
                session_id="system", slug="rate_limiter",
                write_mode="overwrite",
                expected_current_file_hash=current_hash,
            )
            return Reserved(tokens=estimated_tokens)
        except VaultCasmismatch:
            time.sleep(_backoff_with_jitter(attempt))
            continue  # another process won the CAS, retry

    raise F_PIPE_06_rate_limit_exhausted(endpoint)

def _backoff_with_jitter(attempt: int) -> float:
    base_ms = (50, 200, 800)[min(attempt, 2)]
    jitter_ms = random.randint(*RATE_LIMIT_JITTER_RANGE_MS)
    return (base_ms + jitter_ms) / 1000.0
```

**Token bucket capacities unchanged from v1 §4.8.**

### §4.9 Provider cascade (v2: live landed-family consulted)

**v2 cascade selection (A-v1-02 closure):**

```python
def select_cascade_level(seat_kind, cascade, run_state):
    # v2: consult LIVE recorded landed families, not post-hoc reconstruction
    landed_so_far = run_state.run_iteration_families_so_far
    excluded_families = set()
    if seat_kind == "editor":
        if "scribe" in landed_so_far:
            excluded_families.add(landed_so_far["scribe"][0])  # family
    elif seat_kind == "judge":
        for other_seat in ("scribe", "editor"):
            if other_seat in landed_so_far:
                excluded_families.add(landed_so_far[other_seat][0])

    for level in cascade.levels[cascade.current_level_index:]:
        if level.family in excluded_families:
            continue
        if rate_limiter.can_reserve(level.provider_endpoint):
            return level

    raise F_PIPE_08_cross_family_exhausted(seat_kind, cascade, excluded_families)
```

**Review-seat exhaustion (§M13 escape valve)** handled by `graceful_degradation.request_bypass_authorization` (§4.12) with a `bypass-pending` checkpoint before the prompt (A-v1-16 closure).

### §4.10 Cron scheduler (v2: flock + vault-stamp two-layer dedupe, DST-safe task-id)

**v2 task-id scheme (B-v1-03 closure):** `cron_task_id = f"fund_radar_{YYYY-MM-DD}_{UTC_HH_MM}"` — includes UTC time to distinguish two 08:30 local firings during DST fall-back. Stamp records have TTL of 36h.

**v2 fire-once (A-v1-05 closure):**

```python
def fire_once(cron_task_id: str) -> None:
    lock_path = Path.home() / ".tilth" / "cron_locks" / f"{cron_task_id}.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with flock_exclusive_noblock(lock_path) as acquired:
        if not acquired:
            log(f"cron dedupe (local flock): {cron_task_id} already in-flight")
            return

        for attempt in range(CRON_VAULT_RETRY_ATTEMPTS):
            try:
                vault_write(
                    path=f"cron/fired/{cron_task_id}.stamp",
                    bytes_=iso_now_bytes(),
                    intent="state-success",  # interim pattern for cron-fired-stamp (OQ-2)
                    session_id="system", slug="cron",
                    write_mode="write-if-absent",
                )
                break
            except VaultWriteExists:
                log(f"cron dedupe (vault stamp): {cron_task_id} already fired")
                return
            except VaultTransientError:
                if attempt + 1 == CRON_VAULT_RETRY_ATTEMPTS:
                    # CRON_VAULT_RETRY_WINDOW_SEC total budget exhausted; flock retained, abort
                    raise F_PIPE_15_cron_dedupe_failure(cron_task_id)
                time.sleep(min(30, 2 ** attempt))

        # Only reached on successful vault write. Flock released by context manager after sweep.
        invoke_scout_fund_radar(...)
```

Two-layer dedupe: local flock survives transient vault outages; vault stamp is the durable truth.

### §4.11 Three-tab delivery (v3: inline-literal runtime check + module-load integrity assert)

**v3 constant (A-v1-06 + B-v1-17 + V1 closure):**

```python
# Static-Final belt (mypy/pyright policies reassignment at analysis time):
TAB_ORDERING: Final[tuple[Literal["live_radar"], Literal["deep_brief"], Literal["council_draft"]]] = \
    ("live_radar", "deep_brief", "council_draft")

# v3 V1 closure: module-load integrity assert. If `pipeline.config` is patched or
# rebound during import (e.g., by a compromised dependency or a late import-hook),
# this assertion fails at import time and the module refuses to finish loading.
assert TAB_ORDERING == ("live_radar", "deep_brief", "council_draft"), \
    "TAB_ORDERING has been rebound at module load; refusing to load pipeline.config"
```

**v3 assembly (V1 closure — inline-literal runtime check replaces module-attribute comparison):**

```python
def assemble_and_deliver(run_state: RunState) -> TabEnvelope:
    live_radar_hash = _hash_file(f"vault/fund_radar/{run_state.run_id_date}/live_radar.json")
    deep_brief_hash = _hash_file(f"vault/deep_brief/{run_state.run_id}/brief.md")
    council_draft_hash = _hash_file(f"vault/pipeline/{run_state.run_id}/iter_{final_N}/scribe_draft.md")

    envelope = TabEnvelope(
        run_id=run_state.run_id,
        tab_ordering=TAB_ORDERING,  # MUST reference the Final constant (policed by §9.7 AST-grep)
        live_radar_payload_hash=live_radar_hash,
        deep_brief_payload_hash=deep_brief_hash,
        council_draft_payload_hash=council_draft_hash,
        assembled_at_iso=iso_now(),
        envelope_sha256="",  # placeholder
    )
    canonical_bytes = envelope.canonical_bytes_without_self_hash()
    envelope = replace(envelope, envelope_sha256=sha256(canonical_bytes).hexdigest())

    # v3 V1 closure: compare against an INLINE LITERAL tuple, not the module attribute.
    # A compromised rebinding of `pipeline.config.TAB_ORDERING` cannot affect this check,
    # because the right-hand side is a fresh tuple literal evaluated at each call site.
    if envelope.tab_ordering != ("live_radar", "deep_brief", "council_draft"):
        raise F_PIPE_16_tab_envelope_ordering_violation(envelope.tab_ordering)

    vault_write(
        path=f"pipeline/{run_state.run_id}/tab_envelope.json",
        bytes_=envelope.canonical_bytes(),
        intent="state-success",  # interim for tab-envelope-write (OQ-3)
        ...,
    )

    # B-v1-09: post-write verification
    stored_bytes, _ = vault_read(f"pipeline/{run_state.run_id}/tab_envelope.json", ...)
    stored = TabEnvelope.parse(stored_bytes)
    if stored.envelope_sha256 != envelope.envelope_sha256:
        raise F_PIPE_01_run_state_corrupt(f"tab envelope hash mismatch after write: {envelope.envelope_sha256} != {stored.envelope_sha256}")

    return envelope
```

### §4.12 Graceful degradation (v2: bypass-pending checkpoint before prompt)

**v2 review-seat outage flow (A-v1-16 closure):**

```python
def request_bypass_authorization(run_state, failed_seat, outage_reason):
    run_state.phase = "degraded_paused"
    run_state.bypass_pending_checkpoint_ref = _make_bypass_pending_record(failed_seat, outage_reason)
    checkpoint_atomic(run_state, intent="state-failure")  # writes bypass-pending with failure code F-PIPE-13

    # NOW surface the prompt
    decision = signoff_plumbing.prompt_bypass_authorization(
        run_state, failed_seat, outage_minutes=_outage_minutes(), recovery_eta=_recovery_eta(),
    )

    if decision == "abort":
        raise F_PIPE_13_review_seat_outage_pending_bypass(run_state)
    elif decision == "wait":
        _poll_recovery_loop(...)
    elif decision == "sign":
        signed_auth = operator_sign_bypass(...)
        admin_risk.record_bypass_authorization(...)  # Section 4 v2 §5.4
        run_state.bypass_authorization_ref = signed_auth.ref
        checkpoint_atomic(run_state, intent="state-success")
```

**Ollama hardware-degraded mode** for author seats unchanged from v1.

### §4.13 State persistence (v2: quarantine marker, back-off, read-retry, total-timeout)

**v2 checkpoint atom (A-v1-01 + A-v1-08 + B-v1-06 + B-v1-15 closures):**

```python
def checkpoint_atomic(run_state: RunState, intent: str) -> None:
    canonical = _canonicalize(run_state)
    new_sha = sha256(canonical).hexdigest()
    deadline = time.monotonic() + CHECKPOINT_TOTAL_TIMEOUT_SEC

    try:
        for attempt in range(CHECKPOINT_CAS_RETRY_MAX):
            if time.monotonic() > deadline:
                break
            try:
                current_sha = _read_current_hash_with_retry(run_state)  # B-v1-06: retry on transient
            except VaultReadFailed as rerr:
                _write_state_failure_wrapper(run_state, rerr)
                raise F_PIPE_01_run_state_corrupt(run_state) from rerr

            try:
                vault_write(
                    path=f"pipeline/{run_state.run_id}/state.json",
                    bytes_=canonical,
                    intent=intent,
                    session_id=run_state.session_id, slug=run_state.org_slug,
                    write_mode="overwrite",
                    expected_current_file_hash=current_sha,
                )
                run_state.last_checkpoint_iso = iso_now()
                return
            except VaultCasmismatch:
                backoff_ms = CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS[min(attempt, 2)]
                time.sleep(backoff_ms / 1000.0)
                continue

    except VaultWriteUnauthorizedIntent as uerr:
        # A-v1-08: even if the intent is rejected by Section 2 v7 allowlist,
        # we still write a state-failure checkpoint before re-raising.
        _write_state_failure_wrapper(run_state, uerr)
        raise

    # A-v1-01: CAS exhausted or total timeout — write quarantine marker before raising
    quarantine_ref = _write_quarantine_marker(run_state, reason="cas_exhausted_or_timeout")
    run_state.quarantine_marker_ref = quarantine_ref
    run_state.phase = "quarantined"
    raise F_PIPE_01_run_state_corrupt(run_state)
```

**`_write_state_failure_wrapper(run_state, error)` (A-v1-08):** a minimal try/except that writes `state-failure` checkpoint with `error.code` before the caller re-raises. Applies to every `vault_write` call inside `tilth/pipeline/`.

**`_write_quarantine_marker(run_state, reason)` (A-v1-01):** writes `vault/pipeline/{run_id}/quarantine.json` via `vault_write(intent="state-success", write_mode="overwrite")` — this is the operator's recovery hook: they can see the run's last-known-good phase and choose to continue, abort, or investigate.

### §4.14 Sign-off plumbing (v2: prompt is idempotent; checkpoint-before-prompt enforced)

**v2 (A-v1-04 closure):**

- `signoff_plumbing.prompt_pre_signoff` / `prompt_post_signoff` are invoked ONLY AFTER the `signoff_pending` checkpoint has landed (caller responsibility; enforced by §4.1 ordering + runtime assertion).
- Prompts are idempotent: on resume, calling the same prompt for the same `(run_id, phase, artifact_hash)` produces the same behaviour. If the operator already signed (signed artifact present in vault), the prompt auto-accepts.

**Bypass-authorization prompt** per §4.12 v2.

### §4.15 eval_mode entry point and calibration-report assembly (v4 driver)

**Purpose.** `eval_mode` is the per-operator local calibration harness. It reads the operator's own curated `golden_set` (past funded grants they wrote, ingested under their own org_slug), runs each item through the same Scribe → Editor → Judge revision loop that submission_mode uses, collects the Judge scores + Editor critiques + rubric-dimension breakdowns, and assembles a signed `CalibrationReport` describing how the live council scores the operator's own reference work. The report is the operator's drift indicator. It is **not** a training signal, **not** a leaderboard submission, and **not** a shareable artifact.

**Trust + sovereignty invariants (declared before mechanism):**
- Every golden-set item is created by the operator under their own org_slug via intent `golden-set-write` (Section 2 v7.1 forward-dependency allowlist row). There is no path by which a golden-set item can be ingested under a different org.
- Every golden-set READ requires `operator_org_slug == requested_golden_set_org_slug`. Mismatch raises `F-EVAL-CROSS-ORG-READ` (Section 4 v2.1 forward-dependency PRE-gate predicate); Section 5 routes the eval_mode run through the same `gate_runner.run_pre_gate` and aborts on any `F-EVAL-*` return code with a `state-failure` checkpoint.
- CalibrationReport writes use intent `golden-set-write`. Writes to any other intent (including `state-success` for a calibration artifact) raise `F-PIPE-21`.
- Cedar policy at Section 3 excludes `vault/{slug}/golden_set/**` from every export, telemetry, and transfer bundle. The `F-PIPE-21` pipeline-level shield is the defence-in-depth layer — the Cedar rule is authoritative, the pipeline code assumes it and reconfirms.

**Entry-point signature (`tilth/pipeline/modes/eval_mode.py`):**

```python
def start_eval_run(
    operator_org_slug: str,
    golden_set_manifest_path: str,    # vault-relative, must resolve under vault/{operator_org_slug}/golden_set/
    session_id: str,
    *,
    subset: list[str] | None = None,  # optional list of golden-set item IDs to run; None = all
) -> RunState: ...

def run_eval_loop(run_state: RunState) -> CalibrationReport: ...
```

**Mechanism (happy path, v5 — hardened):**

1. `start_eval_run` validates `golden_set_manifest_path` via `_resolve_golden_set_path` (v5 hardening, closes MB-02/Vec-8/MB-03/Vec-9):
```python
def _resolve_golden_set_path(p: str, vault_prefix: str) -> Path:
    """Resolve a golden-set path against its vault prefix, rejecting any escape.

    v5 hardening: replaces v4's string-prefix check. Calls os.path.realpath on
    both the candidate and the prefix; rejects symlinks crossing the boundary;
    asserts the resolved path is a strict child of the resolved prefix. Closes
    MB-02 (symlink to other-org golden_set) and MB-03 (`..` traversal).
    """
    cand = Path(os.path.realpath(p))
    prefix = Path(os.path.realpath(vault_prefix))
    if not cand.is_relative_to(prefix):
        raise PipelineFailure("F-PIPE-21", trigger="golden_set_path_escapes_prefix",
                              detail=f"realpath {cand} not under {prefix}")
    # Reject symlinks anywhere on the path (defence-in-depth against subtree symlinks)
    cur = cand
    while cur != prefix and cur != cur.parent:
        if cur.is_symlink():
            raise PipelineFailure("F-PIPE-21", trigger="golden_set_path_traverses_symlink",
                                  detail=f"symlink encountered at {cur}")
        cur = cur.parent
    return cand
```
The literal string check is retained as a fast-path pre-filter; the realpath check is authoritative. Unicode NFC normalization (B-v1-14) runs BEFORE realpath. Tested by §9.9.27 / §9.9.32 / §9.9.33.
2. Mints ULID `run_id`; constructs `RunState(schema_version=RUNSTATE_SCHEMA_VERSION, mode="eval", rfa_hash=None, project_context_hash=None, golden_set_ref=golden_set_manifest_path, org_slug=operator_org_slug, ...)` in phase `initialized`. (v5: `schema_version` reads from the constant rather than a hardcoded literal so future bumps are single-source-of-truth.)
3. `state_checkpoint.checkpoint_atomic(run_state, intent="state-success")`.
4. Transition to `pre_gate_pending` + checkpoint. Call `gate_runner.run_pre_gate(run_state)` — Section 4 v2.1 PRE-gate now includes a mode-aware predicate: if `run_state.mode == "eval"`, it asserts `operator_org_slug == _read_golden_set_org(golden_set_ref)`. Mismatch returns `F-EVAL-CROSS-ORG-READ`; Section 5 writes `state-failure`, transitions `aborted_trusted_fail`, re-raises.
5. On PASS, transition to `pre_gate_passed`.
6. For each golden-set item (in manifest order, or `subset` if specified):
   a. Transition to `eval_iter_pending` + checkpoint with item ID recorded.
   b. Read the item via `vault_read(path=<item_path>, intent="golden-set-read", ...)` — Section 2 v7.1 forward-dependency allowlist row.
   c. Invoke the same `revision_loop.run_inner_loop(run_state_with_item_as_rfa)` used by submission_mode, but with a per-item isolated `run_state` snapshot (item ID + manifest hash + iteration outcomes recorded; no state leakage across items).
   d. Record Judge score + per-dimension breakdown + Editor critique in a per-item result record appended to the in-progress CalibrationReport buffer.
   e. Checkpoint after each item (AR-1 save-state-always).
7. After all items complete, transition to `calibration_assembled`. Call `calibration.report.assemble_from_run(run_state)` to produce a `CalibrationReport` dataclass (schema at §5.6).
8. Write the CalibrationReport to `vault/{operator_org_slug}/golden_set/calibration_reports/{run_id}.json` via `vault_write(intent="golden-set-write", write_mode="write-if-absent")`. Any write using a different intent raises `F-PIPE-21`.
9. Transition to `signoff_pending` + atomic checkpoint BEFORE the prompt (AR-1 ordering, v2 A-v1-04 preserved). Surface a calibration-sign-off prompt: "Sign this CalibrationReport?"
10. On operator sign: `calibration.signing.sign_report(report, operator_signing_key)` produces a detached signature (BT13-style — Ed25519 over canonical bytes per §5.6.4). Write to `vault/{operator_org_slug}/golden_set/calibration_reports/{run_id}.sig` via `vault_write(intent="golden-set-write", write_mode="write-if-absent")`. Transition to `calibration_signed` + checkpoint.

   **Operator pubkey location and provenance (v5 hardening, closes MA-09):** the operator's Ed25519 verification public key lives at `CALIBRATION_KEY_PATH_TMPL.format(operator_org_slug=...)` = `vault/{operator_org_slug}/calibration/keys/operator_pubkey.ed25519`. The pubkey is written exactly once per org via Section 2 v7 §4.6 `state-success` write-if-absent primitive on the operator's first calibration sign-off; subsequent sign-offs verify against the existing on-disk pubkey. A `pubkey_first_write_provenance.json` sibling file records the ULID + ISO-time of the first write. Rotation is deferred to v0.2 (will require a new `key-rotation-write` intent + signed-attestation flow).

   **Verify-time freshness check (v5 hardening, closes MB-06):** `calibration.signing.verify_calibration_report(report, sig, pubkey)` asserts `(datetime.now(timezone.utc) - datetime.fromisoformat(report.signed_at_iso)) < timedelta(days=MAX_CALIBRATION_AGE_DAYS)` BEFORE validating the Ed25519 signature. Stale signatures raise the new failure subcode `F-PIPE-21.calibration_signature_stale`. The default freshness window is 90 days; operator-tunable in v0.2.
11. Transition to `eval_finalized` + final checkpoint. Return the `CalibrationReport`.

**Mode-isolation enforcement (v4, §7.13 enforcement point):** at every checkpoint transition, `_assert_mode_isolation(run_state)` is called; it raises `F-PIPE-21` if any of:
- `run_state.mode == "eval"` AND `run_state.three_tab_envelope_hash is not None`
- `run_state.mode == "eval"` AND the current `intent` being written is not in `{"golden-set-write", "state-success", "state-failure"}`
- `run_state.mode == "submission"` AND the current `intent` is in `{"golden-set-read", "golden-set-write"}`
- `run_state.mode == "submission"` AND `run_state.calibration_report_ref is not None`

**Export-bundle exclusion.** submission_mode's `three_tab_delivery.assemble_and_deliver` (§4.11) includes an assertion `assert run_state.mode == "submission"` at entry. If `run_state.mode == "eval"` somehow reaches assemble_and_deliver, the assertion fires and raises `F-PIPE-21` with a specific trigger string `"eval_run_reached_tab_delivery"`.

**Failure paths:**
- `F-EVAL-CROSS-ORG-READ` returned from PRE-gate → `state-failure` + `aborted_trusted_fail`.
- `F-PIPE-21` raised at any mode-isolation check → `state-failure` + admin-risk CRIT + abort.
- Vault read/write transient failures → normal v3 retry + quarantine semantics (no eval-specific path).
- Operator refuses to sign CalibrationReport → `state-failure` + `aborted_operator` (calibration_report is vaulted but unsigned; recoverable by resume + sign).

**`CalibrationReport` canonical signing target (v5 hardening, closes MA-10/Vec-13/MB-07).** The canonical bytes are computed the same way as `TabEnvelope` (sorted keys, UTF-8, NFC-normalized text, separator `", "`, no trailing whitespace). v5 corrects the v4 phrasing: ONLY the `signature` field is excluded from canonical bytes; `signed_at_iso` IS included (it must be in the signed payload for freshness verification per MB-06). See §5.6.4 for the exhaustive field-level canonicalisation table — every CalibrationReport field is either canonical-included or explicitly listed in the exclusion table with documented rationale (§7.16 invariant). The detached signature covers exactly the canonical bytes produced from this enumeration.

## §5 Interfaces

### §5.1 Consumes Section 1 (Foundation) (unchanged from v1)

### §5.2 Consumes Section 2 (Vault) v7 (unchanged; interim intent-use pattern documented)

Per v1 §5.2 with v2 clarification: until Section 2 v8 extends the allowlist, Section 5 routes the four new intents (`draft-version-write`, `rate-limiter-snapshot`, `cron-fired-stamp`, `tab-envelope-write`) through `state-success` with structured sub-payloads. Section-2 v8 amendment proposal filed as ARCH-07.

### §5.3 Consumes Section 3 (unchanged)

### §5.4 Consumes Section 4 (Logician) v2 (unchanged from v1)

### §5.5 Section 5 publishes (unchanged from v1; v4 publishes CalibrationReport in addition)

### §5.6 (v4) eval_mode interfaces and forward parent-dependency contracts

**Calibration data structures (owned by Section 5):**

```python
@dataclass(frozen=True, slots=True)
class GoldenSetItem:
    item_id: str                        # operator-assigned, unique within org_slug
    org_slug: str                       # MUST equal operator_org_slug at read time (Law 3)
    funded_grant_label: str             # operator's free-text label, e.g., "VAPG FY24 round 2"
    rfa_snapshot_path: str              # vault-relative path to the RFA the operator was applying against
    submitted_artifact_path: str        # vault-relative path to the operator's submitted draft (the reference truth)
    funded_outcome: Literal["funded", "funded_partial", "rejected_with_feedback"]
    operator_curation_iso: str          # when the operator added this item to the golden set
    manifest_hash: str                  # hash of the manifest entry for integrity

@dataclass(frozen=True, slots=True)
class CalibrationReportItem:
    item_id: str
    judge_total_score: int              # /100, normalized
    judge_per_dimension: dict[str, int] # 14 dimensions × 0-10
    editor_critique_summary: str        # whitelist-stripped per AR-4
    iterations_used: int                # 1, 2, or 3
    revision_loop_outcome: Literal["pass_iter1", "pass_iter2", "pass_iter3", "iter_cap_no_pass", "plateau_no_pass"]
    item_run_id: str                    # the per-item nested run_id

@dataclass(frozen=True, slots=True)
class CalibrationReport:
    schema_version: int                 # v4: pinned to 1
    run_id: str                         # the eval-mode run that produced this report
    operator_org_slug: str
    golden_set_manifest_path: str
    golden_set_manifest_hash: str
    items: list[CalibrationReportItem]
    summary_judge_mean: float           # mean across items, /100
    summary_judge_stddev: float
    summary_per_dimension_mean: dict[str, float]
    council_charter_snapshot_hash: str  # hash of the active charter at run time (drift indicator)
    router_yaml_snapshot_hash: str      # hash of router.yaml at run time (drift indicator)
    assembled_at_iso: str
    canonical_sha256: str               # v5: over canonical bytes excluding ONLY `signature`; `signed_at_iso` IS canonical-included — see §5.6.4
    signature: bytes | None             # Ed25519 detached signature; None until §4.15 step 10 lands; the ONLY field excluded from canonical bytes
    signed_at_iso: str | None           # set at signing; v5: canonical-included for freshness verification per §7.15 + MB-06
```

**§5.6.4 CalibrationReport canonical-bytes enumeration (v5, closes MA-10/Vec-13/MB-07, enforces §7.16 exhaustiveness invariant).**

Every field defined on `CalibrationReport` (and on every dataclass it transitively contains: `CalibrationReportItem`, `GoldenSetItem`) is either canonical-included (part of the signed payload) or explicitly listed in the exclusion table with a documented rationale. Adding a new field to any of these dataclasses MUST either (a) default to canonical-included (no code change needed — `canonical_bytes` auto-serialises the sorted dataclass fields), or (b) add an entry to the exclusion table below with a documented rationale and a paired §9.9 AST-grep test update. The §9.9.30 test enforces: it walks the dataclass field set at test time and asserts every field is either serialised by `canonical_bytes()` or listed below.

| Field | Dataclass | Canonical? | Rationale |
|-------|-----------|------------|-----------|
| `schema_version` | `CalibrationReport` | **INCLUDED** | Version of the signed payload; receiver rejects mismatched versions via F-PIPE-22. |
| `run_id` | `CalibrationReport` | **INCLUDED** | Binds the signature to the specific eval run. |
| `operator_org_slug` | `CalibrationReport` | **INCLUDED** | Binds the signature to the operator; prevents cross-org signature reuse. |
| `golden_set_manifest_path` | `CalibrationReport` | **INCLUDED** | The manifest source the report was computed against. |
| `golden_set_manifest_hash` | `CalibrationReport` | **INCLUDED** | Defends against post-hoc manifest tampering. |
| `items` (list of `CalibrationReportItem`) | `CalibrationReport` | **INCLUDED** | Every per-item score field is recursively canonical-included. |
| `summary_judge_mean` / `summary_judge_stddev` / `summary_per_dimension_mean` | `CalibrationReport` | **INCLUDED** | The calibration signal itself. |
| `council_charter_snapshot_hash` | `CalibrationReport` | **INCLUDED** | Drift indicator — binds the signature to the charter at run time. |
| `router_yaml_snapshot_hash` | `CalibrationReport` | **INCLUDED** | Drift indicator — binds the signature to the router config at run time. |
| `assembled_at_iso` | `CalibrationReport` | **INCLUDED** | When the report was assembled (pre-sign timestamp). |
| `signed_at_iso` | `CalibrationReport` | **INCLUDED** | Required for freshness verification per MB-06 / §7.15. Setting to None pre-sign is fine; the canonical bytes for the signing operation itself use the populated value. |
| `canonical_sha256` | `CalibrationReport` | **NOT APPLICABLE** | The field stores the hash OF the canonical bytes; it cannot be part of its own input. Receiver recomputes and compares. |
| `signature` | `CalibrationReport` | **EXCLUDED** | The signature cannot cover itself. This is the only true exclusion. |
| every field on `CalibrationReportItem` | nested | **INCLUDED** | item_id, scores, critique summary, iteration outcomes are all part of the signed payload. |
| every field on `GoldenSetItem` | referenced via manifest | **N/A — not serialised into CalibrationReport directly** | Integrity is provided via `golden_set_manifest_hash`. |

**Tightened F-EVAL-CROSS-ORG-READ predicate (v5 hardening, closes MB-01/Vec-7).** The v4 contract for the Section 4 v2.1 PRE-gate predicate asserted `run_state.org_slug == _read_golden_set_org(run_state.golden_set_ref)` — but `_read_golden_set_org(...)` reads the `org_slug` field FROM the manifest file, and the manifest is operator-supplied content in the vault. Under the v0.1 trusted-operator trust model the operator is not adversarial, but the V1 (TAB_ORDERING) lesson applies: the trusted comparand must be the field bound at `start_eval_run` against the trusted operator slug, not a field read out of a file whose content could drift. v5 tightens the predicate to compare against `run_state.operator_org_slug` (the field bound at `start_eval_run` in §4.15 step 1, which is asserted equal to the caller's authenticated operator identity by the PRE-gate-upstream Cedar check). The Section 4 v2.1 contract signature updates accordingly: the predicate body in the §4 v2.1 backfill row (table directly below) reads `assert read_org_slug == run_state.operator_org_slug`, and the §4 v2.1 backfill itself is amended to use that comparand. The manifest's own `org_slug` field is still read — but only as a redundant cross-check in §4.15 step 2 (`assert manifest.org_slug == run_state.operator_org_slug` raises `F-PIPE-21.golden_set_manifest_org_mismatch` on divergence), never as the authoritative comparand. This is the same discipline as the V1 inline-literal TAB_ORDERING check: trusted identity lives on the run_state, never on a file whose bytes the operator could edit between `start_eval_run` and PRE-gate.

**Forward parent-dependency contracts (these define the contract Section 5 v4 calls; the parent amendments are queued as backfills sequenced AFTER v4 LOCK):**

**Section 2 v7.1 backfill — two new write-intent allowlist rows in §4.10.4:**

| Intent | Authorised callers | Vault path glob | Write mode | Reason-tag enum | Audit-stamp required |
|--------|---------------------|------------------|------------|-----------------|----------------------|
| `golden-set-write` | `tilth.pipeline.modes.eval_mode`, `tilth.pipeline.calibration.signing`, operator-CLI `tilth.cli.golden_set_curate` | `vault/{slug}/golden_set/**` | `write-if-absent` (manifest items + calibration reports + signatures) | `manifest-add`, `manifest-remove`, `calibration-report-write`, `calibration-signature-write` | YES (operator_org_slug must equal vault path's `{slug}`; CAS-stamp records ISO-time + caller module) |
| `golden-set-read` | `tilth.pipeline.modes.eval_mode`, `tilth.pipeline.calibration.golden_set`, operator-CLI `tilth.cli.golden_set_inspect` | `vault/{slug}/golden_set/**` | `read-only` | `manifest-read`, `item-read`, `calibration-report-read` | YES (operator_org_slug must equal vault path's `{slug}` — Law 3 enforcement) |

**Section 4 v2.1 backfill — one new PRE-gate failure code in §6.1 + one PRE-gate predicate in §4.4:**

| Failure code | Trigger | PRE-gate predicate |
|--------------|---------|--------------------|
| `F-EVAL-CROSS-ORG-READ` | An eval_mode run requests a golden-set read where the operator's trusted slug does not match the golden-set source-of-truth org. (v5 tightening, MB-01/Vec-7): the trusted comparand is `run_state.operator_org_slug`, bound at `start_eval_run` against the authenticated operator identity — NOT the manifest's own `org_slug` field (which is operator-supplied file content and must not be treated as authoritative). | At PRE-gate, if `run_state.mode == "eval"`, assert `read_org_slug == run_state.operator_org_slug` where `read_org_slug` is the org slug extracted from the vault-path component (`vault/{slug}/golden_set/…`) of `run_state.golden_set_ref`. Mismatch returns `F-EVAL-CROSS-ORG-READ` with severity CRIT and a `state-failure` checkpoint contract. The manifest's own `org_slug` field is cross-checked in §4.15 step 2 with a divergence raising `F-PIPE-21.golden_set_manifest_org_mismatch` (defence-in-depth), not as the PRE-gate predicate comparand. |

These two parent amendments are non-blocking on v4 LOCK: Section 5 v4 declares the contracts above, audits them at the v4 driver round, and treats them as a forward dependency. The Section 2 v7.1 + Section 4 v2.1 backfill rounds (Editor + Judge only, no Red Team — substrate amendments under trusted-operator) follow v4 LOCK in sequence.

## §6 Failure codes

Eighteen v1 codes retained; v2 added two (F-PIPE-19, F-PIPE-20); v4 added one (F-PIPE-21); v5 adds one more (F-PIPE-22) for a total of 22. v4 declared forward dependency on Section 4 v2.1's `F-EVAL-CROSS-ORG-READ` (PRE-gate failure code, owned by Section 4); Section 5 routes through `gate_runner.run_pre_gate` and aborts on receipt. v5 also adds a new sub-trigger to F-PIPE-21 (`calibration_signature_stale` and `golden_set_manifest_org_mismatch` — see §4.15 step 10 + §5.6 tightened predicate) and enumerates its full trigger set below.

| Code | Name | Trigger | Severity | Save-state | Test |
|------|------|---------|----------|------------|------|
| F-PIPE-01 | run_state_corrupt | CAS exhausted, schema mismatch on resume, quarantine marker write path | CRIT | state-failure + quarantine marker | §9.5.1 |
| F-PIPE-02 | pre_gate_timeout | PRE gate exceeded timeout | HIGH | state-failure | §9.5.2 |
| F-PIPE-03 | post_gate_timeout | POST gate exceeded timeout | HIGH | state-failure | §9.5.3 |
| F-PIPE-04 | judge_convergence_false_positive | Delta-plateau below min-score threshold | MED | state-failure | §9.3.4 |
| F-PIPE-05 | iteration_cap_exceeded | Three iterations, no PASS, no plateau | MED | state-failure | §9.2.5 |
| F-PIPE-06 | rate_limit_exhausted | Cascade exhausts + retries | HIGH | state-failure | §9.5.6 |
| F-PIPE-07 | seat_subprocess_timeout | Seat timeout | HIGH | state-failure | §9.5.7 |
| F-PIPE-08 | cross_family_violation | Cascade can't find cross-family-compatible level | CRIT | state-failure + admin-risk CRIT | §9.3.8 |
| F-PIPE-09 | judge_output_malformed | Judge JSON unparsable after retry | HIGH | state-failure (never success) | §9.5.9 |
| F-PIPE-10 | signoff_cancelled | Operator declined | LOW | state-failure | §9.2.10 |
| F-PIPE-11 | operator_interrupt | Ctrl-C or interrupt flag | LOW | state-failure (post-checkpoint) | §9.5.11 |
| F-PIPE-12 | hardware_degraded_mode_failed | Ollama fallback failed | HIGH | state-failure | §9.5.12 |
| F-PIPE-13 | review_seat_outage_pending_bypass | Review cascade exhausted; escape-valve awaiting | CRIT | state-failure + bypass-pending | §9.5.13 |
| F-PIPE-14 | review_seat_bypass_expired | Bypass not signed in 24h | HIGH | state-failure | §9.5.14 |
| F-PIPE-15 | cron_dedupe_failure | Vault retry window exhausted | HIGH | state-failure | §9.6.15 |
| F-PIPE-16 | tab_envelope_ordering_violation | `envelope.tab_ordering != ("live_radar", "deep_brief", "council_draft")` (inline-literal runtime check, v3 V1 closure) | CRIT | state-failure + admin-risk CRIT | §9.7.16 |
| F-PIPE-17 | bypass_authorization_ledger_write_failed | Admin-risk append failed | CRIT | state-failure | §9.5.17 |
| F-PIPE-18 | resume_phase_mismatch | Resume stored phase not in allowed set OR schema_version mismatch | CRIT | state-failure + quarantine | §9.5.18 |
| **F-PIPE-19** | **soft_restart_forbidden** (v2, A-v1-10) | Transition to `inner_loop_iter_M` when `iter_n ≥ M` already appended | CRIT | state-failure + admin-risk CRIT | §9.8.19 |
| **F-PIPE-20** | **cedar_decision_missing** (v2, A-v1-14) | `PreGateResult.cedar_decision_ref is None` on PRE-gate return | CRIT | state-failure | §9.5.20 |
| **F-PIPE-21** | **calibration_report_in_submission_bundle** (v4, eval_mode driver; v5 extends with stale-signature, path-traversal, symlink, and manifest-org-mismatch sub-triggers) | Any of: `run_state.mode == "eval"` AND `run_state.three_tab_envelope_hash is not None`; `run_state.mode == "eval"` AND vault_write intent ∉ {`golden-set-write`, `state-success`, `state-failure`}; `run_state.mode == "submission"` AND vault_write intent ∈ {`golden-set-read`, `golden-set-write`}; `run_state.mode == "submission"` AND `run_state.calibration_report_ref is not None`; attempted mode change after `start_run`; canonical-path (`os.path.realpath`) resolution of `golden_set_manifest_path` escapes `realpath(vault/{operator_org_slug}/golden_set/)` (`golden_set_path_escapes_prefix`); any ancestor of the manifest path inside the prefix is a symlink (`golden_set_path_traverses_symlink`); `three_tab_delivery.assemble_and_deliver` entered with `run_state.mode == "eval"`; **(v5, MB-06)** `verify_calibration_report` observes `(now - datetime.fromisoformat(report.signed_at_iso)) >= timedelta(days=MAX_CALIBRATION_AGE_DAYS)` (`calibration_signature_stale`); **(v5, MB-01 defence-in-depth)** `manifest.org_slug != run_state.operator_org_slug` at §4.15 step 2 cross-check (`golden_set_manifest_org_mismatch`) | CRIT | state-failure + admin-risk CRIT | §9.9.21 + §9.9.31 + §9.9.32 + §9.9.33 |
| **F-PIPE-22** | **runstate_schema_downgrade** (v5, MA-07/MB-05 closure) | Either: (a) `resume_run` reads a checkpoint and observes `rs.schema_version != RUNSTATE_SCHEMA_VERSION` OR `rs.schema_version in RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED`; (b) `read_calibration_report` reads a report file and observes `report.schema_version != CALIBRATION_REPORT_SCHEMA_VERSION`. Evaluates BEFORE F-PIPE-18 at `resume_run` — schema-version check is a precondition for phase-validation logic (see §10 OQ-10). | CRIT | state-failure + quarantine | §9.9.28 |

**Forward-dependency failure code (owned by Section 4 v2.1, cited here for completeness):**

| Code | Name | Trigger | Severity | Owner |
|------|------|---------|----------|-------|
| **F-EVAL-CROSS-ORG-READ** | `eval_cross_org_read_denied` | PRE-gate: `run_state.mode == "eval"` AND `run_state.org_slug ≠ _read_golden_set_org(run_state.golden_set_ref)` | CRIT | Section 4 v2.1 (backfill) |

Section 5 v4 calls the PRE-gate and aborts on any `F-EVAL-*` return with `state-failure` + `aborted_trusted_fail`. Section 5 owns no `F-EVAL-*` code directly.

## §7 Invariants (v2 carries v1; v4 adds three more for eval_mode)

Per v1 §7.1-§7.9, with additions:

- **§7.10 (L-003 / L-005 strengthening via resume guard):** `resume_run` cannot re-enter at `post_gate_passed` (skipping sign-off) or `tabs_delivered` (skipping anything). Enforced by `F-PIPE-18`.
- **§7.11 (soft-restart prohibition):** `run_state.iterations` is append-only within a run; any code path that would reset or truncate it raises `F-PIPE-19`.
- **§7.12 (Cedar-decision presence):** `pre_gate_passed` requires `PreGateResult.cedar_decision_ref` non-None. Enforced by `F-PIPE-20`.
- **§7.13 (v4) Mode-isolation invariant:** `run_state.mode` is frozen at `start_run`. A run with `mode == "eval"` cannot reach phase `tabs_delivered`, cannot have `three_tab_envelope_hash != None`, cannot write under any intent other than `{golden-set-write, state-success, state-failure}`. A run with `mode == "submission"` cannot have `calibration_report_ref != None`, cannot write under any intent in `{golden-set-read, golden-set-write}`. Enforced at every checkpoint via `_assert_mode_isolation` and at `three_tab_delivery.assemble_and_deliver` entry; raises `F-PIPE-21`.
- **§7.14 (v4) eval_mode org-isolation (Law 3 enforced at eval time):** `run_state.mode == "eval"` requires `run_state.org_slug == _read_golden_set_org(run_state.golden_set_ref)` at PRE-gate. Enforced by Section 4 v2.1's `F-EVAL-CROSS-ORG-READ` PRE-gate predicate; Section 5 routes the failure to `state-failure` + `aborted_trusted_fail`.
- **§7.15 (v4) CalibrationReport non-exportability:** every CalibrationReport is BT13-style detached-signed and lives under `vault/{org_slug}/golden_set/calibration_reports/`. Cedar policy at Section 3 excludes this glob from every export, telemetry, and transfer bundle. The pipeline-level shield is `F-PIPE-21` (any code path that would surface a calibration artifact in a submission bundle raises). Enforced by Cedar (authoritative) + pipeline assertion (defence-in-depth). **(v5 addendum, MB-06):** verify-time freshness is also an invariant — every successful `verify_calibration_report` call asserts `(now - report.signed_at_iso) < MAX_CALIBRATION_AGE_DAYS` (90 days). Stale signatures raise `F-PIPE-21.calibration_signature_stale`. Re-signing requires re-running eval_mode end-to-end (no signature re-use across runs).
- **§7.16 (v5) CalibrationReport canonical-bytes exhaustiveness (MA-10/MB-07 closure):** every field defined on `CalibrationReport`, `CalibrationReportItem`, and `GoldenSetItem` (the three dataclasses that make up the signed payload surface) MUST be either (a) canonical-included (serialised by `canonical_bytes()`), or (b) explicitly listed in the §5.6.4 exclusion table with a documented rationale. The exclusion table currently contains exactly one true exclusion: `{"signature": "the signature cannot cover itself"}`. Adding any new field to any of the three dataclasses without adding either an inclusion (default, automatic) or a table entry is a CI-blocking failure via §9.9.30 AST-grep test. **Invariant rationale:** silent exclusion of a field from the signed bytes creates a forgery surface (the receiver's verification would accept two reports that differ only in the excluded field). The invariant ensures the signed payload is a total function of the dataclass field set — no ghost fields, no drift.

## §8 Constants (v2 adds new + Final-typed)

Carried from v1 §8 with additions:

| Constant (v2 addition) | Value | Rationale |
|------------------------|-------|-----------|
| `TAB_ORDERING: Final[tuple]` | `("live_radar", "deep_brief", "council_draft")` | A-v1-06 + V1: static `Final` (mypy belt) + module-load integrity assert + inline-literal runtime check at envelope construction. A module-attribute rebinding cannot affect the runtime envelope check because the comparison RHS is a fresh tuple literal at every call site (see §4.11). |
| `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS` | `(50, 200, 800)` | A-v1-01: exponential back-off between CAS retries. |
| `CHECKPOINT_TOTAL_TIMEOUT_SEC` | `10` | B-v1-15: ceiling on checkpoint-write total wall time. |
| `CRON_VAULT_RETRY_WINDOW_SEC` | `300` | A-v1-05: 5-min window during which flock is retained across vault transient failures. |
| `CRON_VAULT_RETRY_ATTEMPTS` | `6` | Paired with back-off 2^0..2^5 seconds capped at 30s. |
| `RATE_LIMIT_JITTER_RANGE_MS` | `(0, 300)` | B-v1-04: jitter avoids thundering-herd. |
| `RATE_LIMIT_LEASE_TTL_SEC` | `30` | B-v1-10: auto-release on lease expiry. |
| `SCHEMA_VERSION_RUNSTATE` | `1` | B-v1-08: incremented on breaking RunState schema change. |
| `CRON_STAMP_TTL_HOURS` | `36` | B-v1-03: stamp records expire after 36h; DST fall-back safe. |
| `BYPASS_PENDING_CHECKPOINT_PATH_TMPL` | `"pipeline/{run_id}/bypass_pending.json"` | A-v1-16 |
| **(v4)** `RUNSTATE_SCHEMA_VERSION` | `2` | v4: bumped from 1 by addition of `mode`, `golden_set_ref`, `calibration_*` fields and four eval-mode phases. Resume of a v3-vintage state with `schema_version=1` is upgraded by inserting `mode="submission"` + None for new fields; resume of any state with `schema_version > 2` raises `F-PIPE-18`. |
| **(v4)** `CALIBRATION_REPORT_SCHEMA_VERSION` | `1` | First version of the CalibrationReport contract; bumped on any breaking schema change to §5.6 dataclasses. |
| **(v4)** `CALIBRATION_SIGNING_ALGORITHM` | `"Ed25519"` | Detached-signature algorithm. Matches BT13 signing-key contract (Section 1 BT13). |
| **(v4)** `CALIBRATION_REPORT_PATH_TMPL` | `"{org_slug}/golden_set/calibration_reports/{run_id}.json"` | Vault-relative; `{org_slug}` MUST equal `run_state.org_slug`. |
| **(v4)** `CALIBRATION_SIGNATURE_PATH_TMPL` | `"{org_slug}/golden_set/calibration_reports/{run_id}.sig"` | Detached-signature path; same org-slug constraint. |
| **(v4)** `GOLDEN_SET_VAULT_PREFIX_TMPL` | `"{org_slug}/golden_set/"` | Read/write path prefix; canonical-path resolution outside this prefix raises `F-PIPE-21`. |
| **(v4)** `EVAL_MODE_ALLOWED_INTENTS: Final[frozenset[str]]` | `frozenset({"golden-set-write", "state-success", "state-failure"})` | Inline-literal `frozenset` (NOT a module attribute) is used in the runtime check at `_assert_mode_isolation` — same lesson as V1 (`TAB_ORDERING`): a `Final` declaration is a static-only hint, so the runtime check uses an inline literal at the call site. |
| **(v4)** `SUBMISSION_MODE_FORBIDDEN_INTENTS: Final[frozenset[str]]` | `frozenset({"golden-set-read", "golden-set-write"})` | Same inline-literal rule as above. |
| **(v5)** `MAX_CALIBRATION_AGE_DAYS: Final[int] = 90` | `90` | MB-06 closure: verify-time freshness window. Signatures older than 90 days are rejected with `F-PIPE-21.calibration_signature_stale`. Operators must re-run eval_mode end-to-end to refresh. Value chosen to match typical grant-cycle cadence (one quarter) — shorter than typical calibration drift interval but long enough that routine verification does not force constant re-runs. |
| **(v5)** `CALIBRATION_KEY_PATH_TMPL: Final[str]` | `"vault/{operator_org_slug}/calibration/keys/operator_pubkey.ed25519"` | MA-09/Vec-11 closure: canonical pubkey location. One key per operator_org_slug; written exactly once per org via Section 2 v7 §4.6 write-if-absent primitive; rotation requires explicit `key-rotation-write` intent (deferred to v0.2). |
| **(v5)** `RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED: Final[frozenset[int]]` | `frozenset({1})` | MA-07/MB-05 closure: explicitly-rejected legacy schema versions. Version 1 (pre-v4) is listed here because silent upgrade from v1 to v2 would mask the absence of the `mode` field on legacy state. Resume of a v1-vintage state raises `F-PIPE-22.runstate_schema_downgrade`; the operator must inspect the state and run an explicit migration. |

All rate-limiter bucket capacities unchanged from v1. All other v1/v2/v3 constants unchanged.

**Module-load integrity assertions (v4 carries forward V1 lesson):**

```python
# v3 carryover:
assert TAB_ORDERING == ("live_radar", "deep_brief", "council_draft"), \
    "TAB_ORDERING has been rebound at module load; refusing to load pipeline.config"

# v4 additions:
assert EVAL_MODE_ALLOWED_INTENTS == frozenset({"golden-set-write", "state-success", "state-failure"}), \
    "EVAL_MODE_ALLOWED_INTENTS has been rebound at module load; refusing to load pipeline.config"
assert SUBMISSION_MODE_FORBIDDEN_INTENTS == frozenset({"golden-set-read", "golden-set-write"}), \
    "SUBMISSION_MODE_FORBIDDEN_INTENTS has been rebound at module load; refusing to load pipeline.config"

# v5 additions (MA-11 + MA-07/MB-05 closure):
assert CALIBRATION_SIGNING_ALGORITHM == "Ed25519", \
    "CALIBRATION_SIGNING_ALGORITHM has been rebound at module load; refusing to load pipeline.config"
assert RUNSTATE_SCHEMA_VERSION == 2, \
    "RUNSTATE_SCHEMA_VERSION has been rebound at module load; refusing to load pipeline.config"
assert RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED == frozenset({1}), \
    "RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED has been rebound at module load; refusing to load pipeline.config"
assert MAX_CALIBRATION_AGE_DAYS == 90, \
    "MAX_CALIBRATION_AGE_DAYS has been rebound at module load; refusing to load pipeline.config"
```

All v5 constants carry the same V1 discipline: the `Final` type hint is a static-analysis belt, the module-load assert is a braces check, and every call-site runtime use is an inline-literal comparison (not a module-attribute read). A module-attribute rebinding cannot affect the runtime-enforced behaviour.

## §9 Tests (v2 adds per-Bucket-A closure tests)

Per v1 §9.1-§9.8 with v2 additions:

### §9.1 Unit tests (added)
- `test_run_state_schema_version_check`: mismatched schema_version on resume raises F-PIPE-18.
- `test_tab_envelope_ordering_runtime_assertion`: TabEnvelope with reordered tuple raises F-PIPE-16.

### §9.2 Integration tests (added)
- `test_signoff_checkpoint_before_prompt`: force-quit between checkpoint and prompt → resume re-shows prompt; force-quit before checkpoint → F-PIPE-01 on resume attempt.

### §9.3 Property tests (added)
- `test_cross_family_rigor_with_scribe_fallback`: Scribe forced to fall back to non-primary family; Editor and Judge MUST never land on Scribe's actual family. A-v1-02 closure.
- `test_rate_limiter_concurrent_reserve_no_overconsumption`: two processes reserving tokens concurrently; total consumed ≤ capacity. A-v1-09 closure.
- `test_judge_parse_failure_never_records_success`: Judge malformed JSON; iteration recorded as state-failure only. A-v1-15 closure.

### §9.5 Failure-injection (added)
- `test_cas_exhaustion_writes_quarantine_marker`: simulate CAS retries exhausted; assert quarantine.json exists with run_id + last-good phase. A-v1-01 closure.
- `test_cedar_decision_missing_raises_f_pipe_20`: PreGateResult with cedar_decision_ref=None → F-PIPE-20.
- `test_bypass_pending_checkpoint_precedes_prompt`: interrupt right after `degraded_paused` transition; resume requires bypass-pending checkpoint. A-v1-16 closure.

### §9.6 Cron tests (added)
- `test_cron_flock_survives_vault_transient_failure`: vault fails transiently; flock retained; second cron fire blocked locally; eventual vault write succeeds. A-v1-05 closure.
- `test_cron_dst_fall_back_distinct_task_ids`: two 08:30 local firings on DST-fall Monday produce distinct task_ids. B-v1-03 closure.
- `test_cron_during_signoff_pending_deduplicated`: cron fires during a paused `signoff_pending` run; new fire no-ops on flock. B-v1-20 closure.

### §9.7 Three-tab tests (added)
- `test_tab_envelope_post_write_hash_verify`: corrupt the stored envelope after write; assemble_and_deliver raises F-PIPE-01. B-v1-09 closure.
- `test_tab_envelope_construction_ast_grep`: AST-grep over `tilth/pipeline/three_tab_delivery.py` asserts that (a) `TabEnvelope(` constructor calls pass `tab_ordering=TAB_ORDERING` (the literal module constant, not an inline tuple); (b) the envelope-ordering invariant check uses an **inline literal tuple** as the comparison RHS, not `TAB_ORDERING` (so runtime monkey-patching of the module attribute cannot bypass the check). Running the AST-grep test as CI lint fails on either violation. A-v1-06 + V1 closure.
- `test_tab_ordering_monkey_patch_resistance`: runtime test — inside a subprocess, rebind `pipeline.config.TAB_ORDERING` to a reordered tuple, then call `assemble_and_deliver`; assert `F-PIPE-16` is raised (the inline-literal check is not fooled). V1 closure.
- `test_tab_ordering_module_load_integrity`: write a monkey-patched `pipeline.config` import hook that rewrites `TAB_ORDERING` during module import; assert the `assert TAB_ORDERING == ("live_radar", "deep_brief", "council_draft")` at module-load time raises `AssertionError` and module import fails. V1 closure.

### §9.8 Law-enforcement tests (added)
- `test_banned_pattern_module_keys`: AST-grep for module-level `KEY`/`SECRET`/`TOKEN` names in `tilth/pipeline/`; CI lint fails on match. A-v1-03 closure.
- `test_subprocess_minimal_env`: spawn seat subprocess; inspect child env; assert only PATH/HOME/TILTH_* names present. A-v1-13 closure.
- `test_soft_restart_raises_f_pipe_19`: synthesize a `run_state.iterations` with an already-appended iter_2, attempt to transition to `inner_loop_iter_1`; assert F-PIPE-19. A-v1-10 closure.
- `test_resume_post_gate_passed_requires_signoff_step`: store `run_state.phase=post_gate_passed`, call resume_run; assert the run proceeds through `signoff_pending` re-entry (never skips). A-v1-12 closure.
- `test_mid_loop_gate_call_assertion`: mock a gate_runner call from inside `revision_loop`; assert the phase-invariant assertion fires. A-v1-07 closure.

### §9.9 (v4) eval-mode tests

**§9.9.21 (F-PIPE-21 — mode-isolation)**
- `test_eval_mode_cannot_reach_tab_delivery`: construct a `RunState(mode="eval", ...)`, call `three_tab_delivery.assemble_and_deliver(run_state)`; assert `F-PIPE-21` raised with trigger string `"eval_run_reached_tab_delivery"`.
- `test_eval_mode_rejects_forbidden_intent`: attempt `vault_write(intent="rate-limiter-snapshot", ...)` from inside an eval_mode run; assert `F-PIPE-21`.
- `test_submission_mode_rejects_golden_set_intents`: attempt `vault_write(intent="golden-set-write", ...)` from a submission_mode run; assert `F-PIPE-21`.
- `test_mode_change_after_start_raises`: `run_state.mode = "eval"` after `start_run` returned; assert `F-PIPE-21` at next checkpoint via `_assert_mode_isolation`.
- `test_golden_set_path_traversal_rejected`: attempt `start_eval_run(golden_set_manifest_path="../../other_org/golden_set/manifest.json")`; assert `F-PIPE-21` with canonical-path-escape trigger.
- `test_calibration_ref_in_submission_state_raises`: construct a `RunState(mode="submission", calibration_report_ref="some/path")`; call `_assert_mode_isolation`; assert `F-PIPE-21`.

**§9.9.22 (cross-org read — F-EVAL-CROSS-ORG-READ parent-dependency)**
- `test_eval_cross_org_read_denied_at_pre_gate`: seed operator_org_slug="org_a"; point `golden_set_manifest_path` at `vault/org_b/golden_set/...` (synthetic); call `start_eval_run`; assert PRE-gate returns `F-EVAL-CROSS-ORG-READ` AND Section 5 records `state-failure` + `aborted_trusted_fail`. **This test depends on Section 4 v2.1 landing; prior to v2.1 lock, test is skipped with message `"Section 4 v2.1 not yet landed"` (skip-not-failed per OQ-9 resolution at §10).**
- `test_eval_read_same_org_permitted`: operator_org_slug="org_a", golden_set under `vault/org_a/...`; assert PRE-gate passes and eval loop proceeds.

**§9.9.23 (CalibrationReport signing integrity)**
- `test_calibration_report_canonical_bytes_stable`: build the same `CalibrationReport` twice with the same inputs; assert `canonical_sha256` matches.
- `test_calibration_signature_verifies`: sign a CalibrationReport; verify with the paired public key; assert valid. Tamper one byte of canonical bytes; assert verify fails.
- `test_calibration_signature_excludes_signature_field`: confirm `canonical_sha256` is computed with `signature` and `signed_at_iso` fields excluded from the canonical form (otherwise signing would cycle).
- `test_calibration_unsigned_report_resumable`: simulate operator refuse-to-sign; assert CalibrationReport is written unsigned, run is in `aborted_operator`, resume shows the calibration-sign-off prompt and allows sign.

**§9.9.24 (export-bundle exclusion)**
- `test_cedar_policy_excludes_golden_set_from_export`: construct an export bundle request that includes `vault/{slug}/golden_set/**` glob; assert Cedar decision = DENY with reason `"golden_set_excluded_from_export"`. (Test landed here in Section 5 because the Cedar rule is authoritative at Section 3, but the pipeline asserts it too; dual enforcement.)
- `test_pipeline_shield_catches_calibration_in_submission_bundle`: force-construct a `SubmissionBundle` containing a path under `vault/{slug}/golden_set/calibration_reports/`; assert `F-PIPE-21` raised before bundle is written.

**§9.9.25 (schema_version upgrade)**
- `test_resume_v1_schema_upgrades_to_v2`: write a v3-vintage RunState with `schema_version=1`; call `resume_run`; assert `schema_version` is upgraded to 2 with `mode="submission"`, `golden_set_ref=None`, all calibration fields None, and the run continues.
- `test_resume_future_schema_raises_f_pipe_18`: write a synthetic RunState with `schema_version=99`; call `resume_run`; assert `F-PIPE-18` + quarantine marker.

**§9.9.26 (module-load integrity — new v4 inline-literal constants)**
- `test_eval_mode_allowed_intents_module_load_integrity`: install a pre-import hook that rewrites `EVAL_MODE_ALLOWED_INTENTS`; assert module load fails at the assertion.
- `test_submission_mode_forbidden_intents_module_load_integrity`: same for `SUBMISSION_MODE_FORBIDDEN_INTENTS`.
- `test_eval_mode_assert_mode_isolation_uses_inline_literal`: AST-grep over `_assert_mode_isolation` body; assert the intent-membership check uses an inline literal `frozenset({"golden-set-write", "state-success", "state-failure"})`, NOT the module attribute `EVAL_MODE_ALLOWED_INTENTS`. (Same lesson as V1.)

**§9.9.27 (v5, MB-04) golden-set path unicode normalization (NFC/NFD path-traversal hardening)**
- `test_golden_set_path_unicode_normalization`: craft two byte-distinct paths that reference the same target — one in NFC form (`…/cafe\u0301/…`) and one in NFD form (`…/café/…`) — where the non-NFC variant routes through a symlink the NFC variant does not. Call `_resolve_golden_set_path` on the non-NFC variant; assert the helper calls `os.path.realpath` (which Python's filesystem layer normalises via the underlying syscall on macOS/Linux) AND that the resulting realpath is then compared to the realpath of the prefix using byte-equality. Assert the non-NFC variant resolves to the same realpath as the NFC variant when the filesystem is NFC-normalising, and assert the path-escape rejection fires when the non-NFC variant points outside the prefix. (Rationale: trusted-operator still benefits from unicode-normalisation discipline because misconfigured filesystems on operator hardware are a real failure mode; this test pins the realpath contract.)

**§9.9.28 (v5, MA-07/MB-05) RunState schema downgrade rejected at resume**
- `test_runstate_schema_downgrade_rejected_at_resume`: write a synthetic RunState checkpoint with `schema_version=1`; call `resume_run(run_id)`; assert `F-PIPE-22.runstate_schema_downgrade` raised with `details.observed == 1` AND `state-failure` checkpoint written BEFORE the raise. Repeat with `schema_version=0`; assert same raise. Repeat with `schema_version=2`; assert no raise (current version passes). Repeat with `schema_version=99`; assert `F-PIPE-22.runstate_schema_downgrade` (forward-version rejection — any non-equal value fails). Paired with `test_schema_downgrade_evaluates_before_phase_check`: write a RunState with `schema_version=1` AND `phase="invalid_phase"`; assert `F-PIPE-22` raised (NOT `F-PIPE-18`) — schema-version check precedes phase check per §10 OQ-10 closure.

**§9.9.29 (v5, MA-11) CalibrationReport signing algorithm module-load integrity**
- `test_calibration_signing_algorithm_module_load_integrity`: install a pre-import hook that rewrites `CALIBRATION_SIGNING_ALGORITHM` to `"RSA"`; import `pipeline.config`; assert `AssertionError` with message containing `"CALIBRATION_SIGNING_ALGORITHM has been rebound at module load"`. Paired with `test_runstate_schema_version_module_load_integrity` (same technique for `RUNSTATE_SCHEMA_VERSION`) and `test_runstate_schema_version_legacy_rejected_module_load_integrity` (same for the frozenset constant) and `test_max_calibration_age_days_module_load_integrity` (same for the int constant). All four assertions mirror V1's TAB_ORDERING discipline.

**§9.9.30 (v5, MA-10/MB-07) CalibrationReport canonical-bytes exhaustiveness (AST-grep)**
- `test_calibration_report_canonical_bytes_exhaustiveness`: at test-discovery time, introspect `dataclasses.fields(CalibrationReport)`, `dataclasses.fields(CalibrationReportItem)`, and the referenced `GoldenSetItem` shape; for each field, assert either (a) the field name appears in the `canonical_bytes()` serialisation for that dataclass (via AST-grep of the source: match the function body, extract the sorted field-iteration, assert the field name is in the resulting set) OR (b) the field name appears in the §5.6.4 exclusion table (sourced from a companion `canonical_bytes_exclusion.json` file committed alongside the dataclass). Fail the test if any field is in neither set. This test runs on every CI build. (Rationale: forgery-surface prevention — any new field silently added without the paired canonical-bytes decision is a forgery-surface in waiting.)

**§9.9.31 (v5, MB-06) stale calibration-signature rejected at verify**
- `test_calibration_signature_stale_rejected`: build a CalibrationReport, sign it with a `signed_at_iso` set to `now - timedelta(days=91)`; call `verify_calibration_report`; assert `F-PIPE-21.calibration_signature_stale` raised. Repeat with `signed_at_iso = now - timedelta(days=89)`; assert verify returns success (freshness window is strict-less-than 90 days, NOT less-than-or-equal — the 90th day is the cutoff). Repeat with `signed_at_iso = now`; assert success. Repeat with `signed_at_iso = now + timedelta(days=1)` (clock-skew case); assert `F-PIPE-21.calibration_signature_stale` with a note in the failure details that future-dated signatures are also rejected (freshness range is `[now - 90d, now]`).

**§9.9.32 (v5, MB-02/Vec-8) golden-set symlink ancestor rejected**
- `test_golden_set_symlink_rejected`: create a vault layout where `vault/org_a/golden_set/manifest.json` is a regular file, but one of its ancestors (`vault/org_a/golden_set/` → symlink to `vault/org_b/golden_set/`) is a symlink crossing the prefix boundary. Call `_resolve_golden_set_path("vault/org_a/golden_set/manifest.json", "vault/org_a/")`; assert `F-PIPE-21.golden_set_path_traverses_symlink` raised. Repeat with the manifest-path itself being a symlink outside the prefix; assert same raise. Repeat with all ancestors being regular directories; assert no raise.

**§9.9.33 (v5, MB-03/Vec-9) golden-set path traversal via `..` rejected**
- `test_golden_set_path_traversal_rejected`: call `_resolve_golden_set_path("vault/org_a/golden_set/../../other_org/golden_set/manifest.json", "vault/org_a/")`; assert `F-PIPE-21.golden_set_path_escapes_prefix` raised (because realpath resolves the `..` segments and the resulting path is outside the realpath of the prefix). Repeat with `"vault/org_a/golden_set/./././manifest.json"`; assert no raise (redundant `.` segments are a no-op after realpath). Repeat with `"/etc/passwd"`; assert raise (absolute path outside prefix).

**§9.9.34 (v5, MA-09/Vec-11) operator pubkey write-once per org**
- `test_operator_pubkey_write_once_per_org`: simulate `sign_calibration_report` for `operator_org_slug="org_a"` the first time; assert the pubkey is written to `vault/org_a/calibration/keys/operator_pubkey.ed25519` via Section 2 v7 §4.6 `write-if-absent` primitive AND a companion hash record is written recording the sha256 of the pubkey bytes + timestamp. Simulate a SECOND `sign_calibration_report` call for the same org with a DIFFERENT pubkey (attacker swap scenario); assert the write-if-absent primitive raises `F-VAULT-WRITE-IF-ABSENT-VIOLATED` AND Section 5 catches this and re-raises as `F-PIPE-21.calibration_pubkey_rotation_forbidden` (rotation requires explicit `key-rotation-write` intent deferred to v0.2). Simulate `verify_calibration_report`; assert the verify-side predicate reads the stored hash record and asserts the freshly-loaded pubkey hashes to the same sha256; mismatch raises `F-PIPE-21.calibration_pubkey_attestation_mismatch`.

**§9.9.35 (v5, new) forward-dep predicate mock backfill**
- `test_forward_dep_predicate_mock_backfill`: Section 5 v5 must not depend on Section 2 v7.1 + Section 4 v2.1 landing before the v5 audit. This test installs a mock implementation of the two forward-dep surfaces: `pipeline.state.fakes.mock_section_2_v7_1_allowlist` (adds `golden-set-write`/`golden-set-read` to the allowlist shape) and `pipeline.state.fakes.mock_section_4_v2_1_pre_gate` (implements the tightened `F-EVAL-CROSS-ORG-READ` predicate with the `run_state.operator_org_slug` comparand from §5.6). With the mocks installed, re-run the entire §9.9.22 cross-org-read test set and assert pass; assert the backfill sequencing is a pure-substrate amendment (the mocks match the real backfill row-for-row). Include a `marks=("backfill_mock",)` pytest marker so CI can flag which tests are mock-backed versus real-landing; once the two backfills land, the marker is flipped off in a single PR and the mocks are deleted.

## §10 Open Questions (v2 closes all v1 OQs; v4 adds one ordering-only OQ; v5 adds one ordering-only OQ)

- **OQ-1/OQ-2/OQ-3** — **CLOSED**. Interim pattern: route `draft-version-write` / `rate-limiter-snapshot` / `cron-fired-stamp` / `tab-envelope-write` through `state-success` with structured sub-payloads. ARCH-07 amendment proposal filed against Section 2 v8 to add the four intents to the allowlist.
- **OQ-4** — **CLOSED**. Section 2 v7 §3.5 `seat_launch` returns a PID. Section 5 `seat_runner` owns the pipe-wrapping layer (documented in §4.3).
- **OQ-5** — **CLOSED**. `REVIEW_SEAT_OUTAGE_POLL_INTERVAL_MS = 300000` stands as v0.1 default.
- **OQ-6** — **CLOSED**. `config.load_overrides()` at boot; §8 defaults are fallback.
- **OQ-7** — **CLOSED**. No soft restart; F-PIPE-19 enforces. Restart requires fresh `run_id` from operator.
- **OQ-8** — **CLOSED**. LaunchAgent plist label `tilth.cron.fund_radar`; `launchctl load -w` idempotently replaces.

**v2 ARCH items surfaced:**
- **ARCH-07** — Request Section 2 v8 to add `draft-version-write`, `rate-limiter-snapshot`, `cron-fired-stamp`, `tab-envelope-write` to §4.10.4 allowlist.
- **ARCH-08** — Section 2 v8 candidate: enforce max artifact size (e.g., 10 MiB) on vault_write with `F-VAULT-ARTIFACT-TOO-LARGE`. B-v1-19 deferred.

**v4 OQ (single, ordering-only):**
- **OQ-9 (v4, sequencing)** — **RESOLVED at v4 LOCK as a process decision, not a mechanism gap.** The eval_mode driver calls Section 2 v7.1 and Section 4 v2.1 contracts that will only land in backfill rounds after v4 LOCK. This is intentional: Section 5 v4 is the driver that gives the backfill rounds their shape and audit rationale. Until both backfills land, the two tests `test_eval_cross_org_read_denied_at_pre_gate` and `test_eval_read_same_org_permitted` skip with the message `"Section 4 v2.1 not yet landed"`; all other v4 tests run against mock vault primitives until Section 2 v7.1 lands. The v4 LOCK is not blocked on the backfill rounds; the backfill rounds are scheduled as Editor + Judge only (no Red Team — substrate amendments whose attack surface is already audited in this v4 driver round under trusted-operator A1–A4). **(v5, §9.9.35):** The mock-backfill pattern is formalised as `test_forward_dep_predicate_mock_backfill` — mocks implement the forward-dep surfaces row-for-row so v5 test coverage is not gated on backfill landing; mocks deleted in a single PR once backfills land.

**v5 OQ (single, ordering-only):**
- **OQ-10 (v5, ordering)** — **CLOSED at v5 LOCK.** Question: at `resume_run` entry, in what order do `F-PIPE-22.runstate_schema_downgrade` (v5) and `F-PIPE-18.resume_phase_mismatch` (v2) evaluate? Closure: **F-PIPE-22 evaluates FIRST, BEFORE F-PIPE-18.** Rationale: a downgraded schema may have renamed, removed, or type-shifted the `phase` field itself; validating `phase` against the allowed set is only meaningful on a trusted schema. The evaluation order is pinned by the ordering of predicate calls in §4.1 resume-path list (step 1 = `_assert_runstate_schema_current`, step 2 = phase-set membership). A `test_schema_downgrade_evaluates_before_phase_check` test (companion to §9.9.28) pins the ordering at test time by constructing a RunState that would trigger BOTH F-PIPE-22 (schema_version=1) AND F-PIPE-18 (phase="invalid_phase") — the test asserts F-PIPE-22 is the raised code.

**v4 ARCH items surfaced:**
- None. eval_mode is fully satisfied by the two declared parent amendments (Section 2 v7.1 + Section 4 v2.1); no further architecture-level changes are needed.

**v5 ARCH items surfaced:**
- None. All v5 edits are confined to Section 5 surface (§3.2.1 + §4.1 + §4.15 + §5.6.4 + §6 + §7.16 + §8 + §9.9). No new forward-dep to any other section. The Section 4 v2.1 backfill contract is tightened (predicate comparand change from manifest-field to run_state-field) but not expanded in surface.

## §11 Law map (v2 additions + v4 eval_mode additions)

| Rule | Section-5 invariant | §7 subsection | §6 failure code |
|------|--------------------|-----|-----------------|
| L-001 RFA Source of Truth | Hashes (NFC-normalized v2) through every call; eval_mode substitutes operator's curated golden_set as source-of-truth under Law 3 | §7.1 | (Section 4 owns F-PRE-*) |
| L-002 No Boundary Drift | §3.5 banned imports + patterns + §5 §-cited interfaces | §7.2 | (lint-time) |
| L-003 Org Isolation (v4: **extended to eval time**) | Single-client `org_slug` frozen at boot; resume phase validated; **(v4) eval_mode PRE-gate asserts `operator_org_slug == golden_set_org_slug`** | §7.3 / §7.10 / **§7.14 (v4)** | F-PIPE-01, F-PIPE-18, **F-EVAL-CROSS-ORG-READ (Section 4 v2.1)** |
| L-004 Apolitical + Admin-Risk | Whitelist-only clean-output | §7.4 | (propagation only) |
| L-005 Strict Two-Audit Cycle | PRE + POST gates both called exactly once, resume enforces; eval_mode also runs PRE + POST (same discipline) | §7.5 / §7.10 | F-PIPE-18 |
| AR-1 Save State Always | Every failure path checkpoints; intent-unauthorized too; eval_mode checkpoints per item | §7.6 | (property test + static grep) |
| AR-2 Test Your Own Work | Clean-output parsers + Cedar-decision presence check | §7.7 / §7.12 | F-PIPE-09, F-PIPE-07, F-PIPE-20 |
| AR-3 Be Explicit | `IterationContext` required | §7.8 | (build-time) |
| AR-4 Clean Output | Whitelist stripping pre-vault | §7.9 | F-PIPE-09 |
| **(v2)** Soft-restart prohibition | `iterations` append-only | §7.11 | F-PIPE-19 |
| **(v2)** Cedar-decision presence | PRE-gate result check | §7.12 | F-PIPE-20 |
| **(v4)** Mode-isolation | mode frozen at start_run; intent/phase/envelope/bundle mode-gated | **§7.13** | **F-PIPE-21** |
| **(v4)** CalibrationReport non-exportability | BT13-signed, Cedar-excluded from export bundles, pipeline-shielded | **§7.15** | **F-PIPE-21** |

**Law 5 (Applicant Brings the Substance) — v4 enforcement at eval time:** eval_mode does not synthesize, augment, or fabricate any golden-set item content. The operator curates their own golden_set (via the `golden-set-write` intent's `manifest-add` reason tag); the pipeline only reads and scores. No Tilth code path generates golden-set content.

## §12 Non-ownership (unchanged from v1; v4 adds two eval-mode non-owned surfaces)

**v4 additions to the non-owned list:**
- **Golden-set curation UI / CLI** — `tilth.cli.golden_set_curate` and `tilth.cli.golden_set_inspect` are operator-facing tools, not Section 5 code. Section 5 uses their outputs (manifests) and never drives them.
- **Council model choice for eval_mode** — eval_mode uses whatever charter + router.yaml configuration is active at run time. Section 5 does not re-configure providers for eval vs. submission; the `router_yaml_snapshot_hash` field in the CalibrationReport records the config at run time so drift can be attributed.

## §13 Closure

**v3 LOCKED 2026-04-18** — Editor READY_TO_LOCK, Judge PASS 100/100, Red Team READY_TO_LOCK. All 16 v1 Bucket-A closures, 12 v2 Bucket-B landings, V1 TAB_ORDERING monkey-patch bypass closure, 8 §10 OQ closures, 2 ARCH items, 20 failure codes, 3 new invariants, 18 closure-specific tests + V1 tests. Canonical at `pipeline/blueprint/v0.1/section_05_pipeline.md`.

**v4 is the eval_mode driver round (scope-expansion narrow-edit).** The v3 → v4 changelog landed six edits, all eval_mode-scoped:

- §1 adds `eval_mode` as a second entry point; §1.3 declares five explicit eval_mode non-goals; §2 adds criteria 14–16 (mode-isolation, org-isolation at eval time, non-exportability).
- §3.1 adds 7 new module paths (modes/, calibration/, tests/test_eval_mode/); §3.2 extends `RunState` with `mode`, `golden_set_ref`, `calibration_report_ref`, `calibration_signature_ref`, and four eval-mode phases; adds `GoldenSetItem`, `CalibrationReportItem`, `CalibrationReport` dataclasses.
- §4 adds §4.15 `eval_mode entry point and calibration-report assembly` (entry-point signature, happy-path 11-step mechanism, `_assert_mode_isolation` enforcement, `assemble_and_deliver` mode-check, BT13-style Ed25519 detached-signature discipline).
- §5 adds §5.6 declaring the two forward parent-amendment contracts: Section 2 v7.1 adds `golden-set-write` + `golden-set-read` intents to the §4.10.4 allowlist; Section 4 v2.1 adds `F-EVAL-CROSS-ORG-READ` PRE-gate failure code + enforcement predicate.
- §6 adds one new pipeline-level failure code `F-PIPE-21.calibration_report_in_submission_bundle` and documents the Section 4 v2.1 forward-dependency code.
- §7 adds three new invariants (§7.13 mode-isolation, §7.14 eval-time org-isolation, §7.15 CalibrationReport non-exportability); §8 adds nine new constants including two inline-literal `Final[frozenset]` constants with module-load integrity asserts (V1 lesson carried forward); §9 adds §9.9 eval-mode tests (six subsections, ~18 new tests); §11 extends law map for Law 3 eval-time + Law 5 source-of-substance; §12 lists two new non-owned surfaces.

**Strict v4 LOCK bar (L-005 strict driver round, single audit cycle):**
- Editor: `READY_TO_LOCK` — the six changelog items land cleanly, zero v3 regression, no scope creep beyond eval_mode.
- Judge: `total_score ≥ 85` against the v3 14-dimension rubric with dim 14 renamed `v4_revision_discipline`; `top_3_blockers: []`.
- Red Team: `READY_TO_LOCK` with ZERO Bucket-A new findings AND explicit reconfirmation that V1 + all 16 A-v1-* + all 12 v2 Bucket-B + 8 OQ closures remain unchanged AND explicit attack-vector enumeration against the eval_mode amendments (cross-org read bypass, mode-isolation bypass, calibration-signing bypass, export-bundle leakage, canonical-path traversal, schema_version downgrade attacks).

**Sequencing after v4 LOCK:**
1. Section 2 v7.1 parent-backfill round (Editor + Judge only; two new allowlist rows).
2. Section 4 v2.1 parent-backfill round (Editor + Judge only; one new PRE-gate failure code + predicate).
3. Two currently-skipped v9.9.22 tests go green as soon as Section 4 v2.1 lands; all remaining eval-mode tests go green as soon as Section 2 v7.1 lands.
4. Section 0.5 interface-index doc (bus-factor mitigation) is unblocked once all five Section-1-through-5 parents are locked.

If any of the three seat bars fail, v5 verification round opens (full L-005 cycle re-engages). If all three pass, Section 5 LOCKS at v4 and the canonical file at `pipeline/blueprint/v0.1/section_05_pipeline.md` is updated with a v4 header pointing to this driver round + the forthcoming parent-backfill rounds.

**v5 is the verification round closing v4 Red Team Group-1 gaps.** v4 driver round landed six edits cleanly (Editor=READY_TO_LOCK, Judge=PASS 100/100), but Red Team surfaced eleven Bucket-A and ten Bucket-B findings. Synthesis triaged against the v0.1 A1–A4 trusted-operator trust model: Group-1 = eleven genuine spec gaps (MA-07, MA-09, MA-10, MA-11, MB-01, MB-02, MB-03, MB-04, MB-05, MB-06, MB-07) that warrant v5 narrow edits; Group-2 = nine OUT-OF-MODEL findings that assume operator attacks self (captured in v0.2 hardening backlog with same disposition v3 used); Group-3 = process discipline already addressed by v4 sequencing. v5 applies the eleven narrow edits listed in the v4→v5 changelog (top of document), ALL confined to v4's existing surface area — one new failure code (F-PIPE-22), three new constants + one new module-load assert, one new invariant (§7.16), nine new tests (§9.9.27–§9.9.35), tightened predicate comparand on the §5.6 forward-dep contract, realpath + symlink hardening on §4.15 step 2, pubkey-location specification on §4.15 step 10, verify-time freshness check on §4.15 step 10, resume-time schema-version enforcement on §4.1, and canonical-bytes enumeration on §5.6.4. Zero new mechanisms, zero new entry points, zero scope creep beyond the listed eleven. §10 OQ-10 opened+closed as ordering closure.

**Strict v5 LOCK bar (L-005 strict verification round, single audit cycle):**
- Editor: `READY_TO_LOCK` — the eleven v4→v5 edits land cleanly; zero v4 regression (the six v4 amendments are preserved row-for-row); no scope creep beyond the eleven listed edits; forward-dep contract tightening is a comparand swap, not a surface expansion.
- Judge: `total_score ≥ 85` against the v3/v4 14-dimension rubric with dim 14 renamed `v5_revision_discipline`; `top_3_blockers: []`; all v5 amendment booleans (listed in system_judge_v5.txt) return true; `v4_regression_observed: false`; `scope_creep_observed: false`.
- Red Team: `READY_TO_LOCK` with ZERO Bucket-A new findings AND explicit reconfirmation that V1 + all 16 A-v1-* + all 12 v2 Bucket-B + 9 §10 OQ closures (OQ-1..OQ-8 + OQ-9) + all 6 v4 amendments remain unchanged AND explicit attack-vector enumeration against the eleven v5 edits (schema-downgrade, symlink-ancestor, unicode-path, realpath-escape, algorithm-rebind, stale-signature, pubkey-rotation, canonical-exhaustiveness bypass, manifest-org-mismatch, operator_org_slug comparand bypass, freshness-window off-by-one).

**Sequencing after v5 LOCK (same sequence as v4 would have been, carried forward unchanged):**
1. Section 2 v7.1 parent-backfill round (Editor + Judge only; two new allowlist rows).
2. Section 4 v2.1 parent-backfill round (Editor + Judge only; one new PRE-gate failure code + predicate — **with v5 tightened comparand: predicate body reads `run_state.operator_org_slug`, not `manifest.org_slug`**).
3. Mock-backfill pytest markers on §9.9.22 + §9.9.35 flipped off in a single PR; mocks deleted.
4. Section 0.5 interface-index doc (bus-factor mitigation) is unblocked once all five Section-1-through-5 parents are locked.

If any of the three seat bars fail, v6 verification round opens. If all three pass, Section 5 LOCKS at v5 and the canonical file at `pipeline/blueprint/v0.1/section_05_pipeline.md` is updated with a v5 header pointing to the v3 scoping → v4 driver → v5 verification audit trail + the forthcoming parent-backfill rounds.

— End of Section 5 v5 draft —

---

## §5.NEW (companion edit at v7.0.4 LOCK 2026-05-09) — SP0 stop-point + Intake invocation contract (3 modes)

This subsection is the §5 companion edit landing alongside architecture v7.0.4 LOCK (lock_history row 178; 2026-05-09). The full pipeline refactor consuming the SP0 stop point + Intake invocation contract lives here as a §5 v8 amendment scaffold (formal §5 v8 LOCK is queued under WS-L for v0.2 gate-family registration).

**Authority:** `pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md` LOCKED 2026-05-09. The v7.0.4 amendment specifies KFR schema + SP0 + F-LOGICIAN-FACT-DRIFT family + Intake 3-mode spec + Benchmarks Register. This §5 companion edit is the blueprint-tier reflection of the new pipeline stop-point + Intake invocation contract.

### Revision loop accommodates new stop-point chain

The stop-point chain becomes:

```
Session start
  → Logician PRE-gate (existing rows 1-19 + new rows 20-22 per §4 companion edit)
  → SP0 KFR Freshness Review (NEW — operator-signed sp0_delta required to advance)
  → KGIE Preflight (existing — extended with KFR cross-check per skills/scribe-ghostwriter/SKILL.md companion edit)
  → SP1 spine lock (existing)
  → Drafting (existing — Scribe annotates derived values with `<derivation_id="...">` per v7.0.4 §4.7)
  → SP2 per-section operator review (existing)
  → SP3 pre-Editor (existing)
  → SP4 post-Editor (existing)
  → Logician POST-gate (existing rows + new F-LOGICIAN-FACT-DRIFT family per §4 companion edit)
  → Operator final review + sign-off
```

### SP0 invocation contract

- **Trigger:** session start, after PRE-gate row 22 (F-LOGICIAN-FACT-NEEDED-REQUIRED at SP0) check passes for non-NEEDED state.
- **Input:** RFA dissection's required-fields list; current KFR state (read via Pydantic-validated `orgs/<slug>/vault/kfr/register.yaml`); current admin-risk ledger.
- **Process:** query KFR for `required_for_category` + `required_for_funder` matches; surface stale entries (past expiry) + gap entries (required but absent) + newly-confirmed entries (operator's confirm-current picks); operator reviews three-pane surface per v7.0.4 §3.1.
- **Output:** operator-signed `sp0_delta` per v7.0.4 §3.1 schema (atomic; deterministic `delta_id`; ledger entry `ledger_kind="sp0_delta"`).
- **Failure modes:**
  - Operator does not sign → pipeline halts at SP0 (cannot advance to KGIE).
  - Required-for-RFA fact in NEEDED state at sign-out → F-LOGICIAN-FACT-NEEDED-REQUIRED HARD_BLOCK at SP0; operator must fill the fact or remove the funder from in-flight cycle.
  - KFR signature integrity check failure → F-KFR-SIGNATURE-INVALID / F-KFR-AUDIT-CHAIN-BROKEN HIGH-severity TAMPER_EVENT; pipeline aborts.
- **Idempotent re-entry:** per Rule 1 Save State Always, partial sp0_delta persists; resume reads pending picks.

### Intake invocation contract (3 modes)

Per v7.0.4 §5, Intake operates in three modes. Each mode has a distinct invocation contract:

#### BULK_INGEST (onboarding)

- **Trigger:** white-glove onboarding; operator drops folder of org documents into `orgs/<slug>/intake/inbox/` and invokes:
  ```
  tilth intake bulk-ingest --org <slug> --inbox orgs/<slug>/intake/inbox/
  ```
- **Process:** Intake walks the inbox, indexes each document via FAISS/Chroma + bge-large-en-v1.5 embeddings, extracts candidate facts via local Mistral 7B-class LLM, runs F-EXTRACTOR-FABRICATION pre-queue gate (verbatim source_quote validation per v7.0.4 §5.2 exact-match semantics).
- **Output:** `orgs/<slug>/vault/kfr/pending_facts.yaml` queue.
- **Operator review:** side-by-side display per v7.0.4 §5.1; operator confirms (promotes to KFR), edits, rejects, or merges.

#### INCREMENTAL_INGEST (continuous)

- **Trigger:** operator-explicit only at v0.1 — operator drops single document into `orgs/<slug>/intake/inbox/` and invokes:
  ```
  tilth intake incremental-ingest --org <slug> --doc <path>
  ```
- **Process:** identical to BULK_INGEST but for one document.
- **Output:** appends to `pending_facts.yaml` queue.
- **Filesystem-watcher trigger:** deferred to v0.2 WS-E §11 Intake blueprint round.

#### AWARD_INGEST (award acceptance — pre-LOCK addition per v7.0.4 §5.3)

- **Trigger:** operator-explicit only at v0.1; operator marks a submitted proposal as WON via:
  ```
  tilth intake award-ingest --org <slug> --grant <grant_id> --award-doc <path>
  ```
- **Pre-extraction verification:**
  1. Won-proposal artifact's operator signature MUST verify (per Section 4 §4.5 verify_claim_evidence_map). Failure → `F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal` HIGH severity.
  2. Award document signature, where present, MUST verify against funder's published signing key (operator-curated per `vault_shared/funders/<funder_id>/signing_keys.yaml`). Failure → `F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award` HIGH severity.
- **Output:** `orgs/<slug>/vault/grants/<grant_id>/proposal_commitments.yaml` per v7.0.4 §5.3 schema; commitment-id-keyed structured rows operator-reviewed before promotion.
- **KFR linkage:** explicit commitment ↔ KFR fact references via `kfr_fact_ref: <fact_id>` field; F-LOGICIAN-FACT-DRIFT discipline applies to commitment values during reporting cycles.
- **Consumer:** WS-J Report Generator pulls `proposal_commitments.yaml` as authoritative for commitment-tracking during reporting cycles.

### Forward-dep contract for §4 v2.x (WS-L)

Section 4 Logician v2.x consolidated amendment (WS-L) registers the following Python predicates referenced from this §5 companion edit:

- `pipeline.logician.gates.f_logician_fact_drift` (new module — POST-gate)
- `pipeline.logician.gates.f_kfr_signature_invalid` (new module — PRE-gate row 20)
- `pipeline.logician.gates.f_kfr_audit_chain_broken` (new module — PRE-gate row 21)
- `pipeline.logician.gates.f_logician_fact_needed_required` (new module — PRE-gate row 22 / SP0 hard-block)
- `pipeline.logician.gates.f_logician_fact_tolerance_drift` (new module)
- `pipeline.logician.gates.f_extractor_fabrication` (new module — Intake pre-queue)
- `pipeline.logician.gates.f_extractor_award_signature_invalid` (new module — AWARD_INGEST)
- `pipeline.logician.gates.f_benchmark_contains_per_org_ref` (new module — workspace-shared write/read gate)

The blueprint-tier failure codes are declared in §4 companion edit §6.13–§6.17. WS-L produces the Python implementations + tests per `pipeline/logician/gates/test_f_*.py` pattern.

### v7.0.4 LOCK row reference

`pipeline/engineering/lock_history.v1.jsonl` row 178 (architecture v7.0.4 LOCKED 2026-05-09; Section E carve-out single-Claude Thesis Cycles 1+2).

*End §5 companion edit at v7.0.4 LOCK 2026-05-09.*
