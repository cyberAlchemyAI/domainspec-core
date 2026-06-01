# Codebase Alignment Audit — 2026-04-20

**Scope:** Full GoldenQuill workspace audit against locked architecture, blueprints, roadmap, and operational docs.
**Auditor:** Cowork session (Opus 4.6)
**Method:** Automated directory walk + file-by-file verification. No changes made.

---

## CLEAN — No action needed

**C-01. Lock history ↔ code on disk.** All 18 lock_history.v1.jsonl entries point to modules that exist at their expected paths. Zero phantom entries.

**C-02. __init__.py coverage.** All 11 pipeline sub-packages have well-formed `__init__.py` files with proper `__all__` exports. Re-export hubs for sovereignty (233 lines), vault (354 lines), logician (390 lines), scout (315 lines), loop (225 lines) are thorough.

**C-03. No circular imports.** Dependency graphs within each section are acyclic. sovereignty → vault → logician → loop dependency chain is one-directional.

**C-04. Test coverage structure.** 12 test subdirectories (sovereignty, vault, logician, scout, loop, linting, gpp, observability, privacy, runtime_integrity, canary, integration) all have `__init__.py` and proper conftest.py injection.

**C-05. Daily log 2026-04-20.** Extensive, current, covers full day's work through ARCH-05. Up to date.

**C-06. lessons.md.** L-001 through L-010, sequential, no gaps, no duplicates. Each covers a distinct failure pattern.

**C-07. scripts/run_tests.sh and scripts/run_lint.sh.** Both exist, properly pin to `.venv/bin/python3`, validate Python ≥ 3.11. Correct.

**C-08. pyproject.toml.** Package `tilth` version `0.1.0.dev0`, `requires-python >= 3.11`, proper `find` discovery with correct excludes for non-code dirs.

**C-09. Client org structure.** 7 client folders + template + ORG_INDEX.md under `orgs/`. All have PROJECT_CONTEXT.md. Weekly briefs present for all active orgs.

**C-10. router.yaml at workspace root.** Canonical model bindings file, referenced by AGENTS.md step 3. Exists and is current.

**C-11. Rubrics.** `pipeline/rubrics/vapg_fy26.json` exists and is referenced in CLAUDE.md.

**C-12. Session bootstrap.** `pipeline/SESSION_BOOTSTRAP.md` exists, is current (dated 2026-04-19), and correctly references all key file locations.

**C-13. Tilth JS tooling.** `tilth/bin/` has `tilth-batch.mjs`, `tilth-infer-cached.mjs`, and `README.md`. Cache-ledger logs exist for smoke orgs. Properly structured.

**C-14. OpenClaw workspace state.** `.openclaw/workspace-state.json` and `sessions/sessions.json` are runtime state files. Correct location.

---

## FIX — Specific problems requiring action

**F-01. MEMORY.md broken pointer — HeartbeatQAfiles/memory/**
- **File:** `MEMORY.md` line 13
- **Problem:** References `HeartbeatQAfiles/memory/` as Sentinel agent memory location. That directory does not exist. HeartbeatQAfiles has SOUL.md, MEMORY.md, etc. at root level, but no `memory/` subdirectory.
- **Fix:** Either create `HeartbeatQAfiles/memory/` and move relevant files into it, or update MEMORY.md to point to `HeartbeatQAfiles/` directly, or remove the Sentinel memory pointer entirely if Sentinel is deprecated (last QA report is from 2026-04-14).

**F-02. routing.yaml stale Judge fallback — Kimi K2**
- **File:** `pipeline/orchestrator/routing.yaml`
- **Problem:** Judge fallback lists `moonshotai/kimi-k2-instruct`. Per L-009, Kimi K2 404s on Groq Dev tier (Groq removed Moonshot/Kimi paths 2026-03-23, also documented in AGENTS.md). This fallback will fail silently if triggered.
- **Fix:** Remove or replace the Kimi K2 fallback with an accessible model on Groq Dev tier.

**F-03. Lock history gap — Sections 2, 3, 4 and Section 1 Rounds F-J**
- **File:** `pipeline/engineering/lock_history.v1.jsonl`
- **Problem:** lock_history was introduced mid-build (~Round A, 2026-04-19). These implemented, tested modules have NO lock_history entries:
  - Section 1 Rounds F-J: 9 sovereignty modules (boot, boot_clock, lockfile, init_marker, admin_risk, degradation_log, project_context_envelope, rfa_envelope, router_integrity)
  - Section 2: 17 vault modules (all real implementations)
  - Section 3: 7 scout modules (all with spec cards and real code)
  - Section 4: 9 logician modules (all real implementations)
  - Section 5 Rounds 4-5: seat_runner, revision_loop (daily log mentions seat_runner self-LOCKED)
- **Fix:** Backfill lock_history entries for all modules that have passed committee review or self-LOCK. At minimum, add entries with `"backfilled": true` and the actual lock date from daily logs.

**F-04. Spec cards lack structured STATUS field**
- **Files:** All 26 files in `pipeline/engineering/spec_cards/`
- **Problem:** No spec card uses a machine-readable `STATUS:` header. Status is buried in prose ("LOCKED 2026-04-19 via E3", "pre-staged 2026-04-20"). Makes it impossible to programmatically check completion.
- **Fix:** Add a YAML front-matter or top-line `STATUS: LOCKED | SELF-LOCKED | PENDING-COMMITTEE | PRE-STAGED | SPEC-ONLY` to each spec card.

**F-05. Cross-section deep imports (8 instances)**
- **Problem:** Architecture mandates importing from `pipeline.<section>` public API, not `pipeline.<section>.<module>`. These modules import from internal paths:
  - `pipeline/vault/init_marker.py` → imports from `pipeline.sovereignty.audit`, `.crypto_primitives`, `.keys`
  - `pipeline/vault/vault_boot.py` → imports from `pipeline.sovereignty.keys`
  - `pipeline/logician/admin_risk.py` → imports from `pipeline.sovereignty.admin_risk`, `.audit`
  - `pipeline/loop/state_checkpoint.py` → imports from `pipeline.vault.error_codes`
  - `pipeline/scout/_types.py` → imports from `pipeline.sovereignty.audit`
  - `pipeline/scout/channel_c_portals.py` → imports from `pipeline.sovereignty.org_slug`
- **Severity:** Low. All target symbols ARE re-exported in the section's `__init__.py`. Runtime-correct but creates coupling to internal module paths.
- **Fix:** Refactor to import from `pipeline.sovereignty` / `pipeline.vault` public API instead of deep paths. Can be done incrementally.

**F-06. GPP module path injection fragility**
- **File:** `tests/conftest.py`
- **Problem:** Hardcodes `pipeline/validation/integration_scope_close_2026-04-19/gpp/` into `sys.path` so `gpp_det`, `gpp_council_dispatch`, `gpp_manifest` can be imported as top-level modules. If that directory moves, tests break silently. Coverage config in `pyproject.toml` lists these as top-level sources but they're not installable via `pip install -e .`.
- **Fix:** Either move GPP tools to a proper package location (e.g., `pipeline/gpp/`) or document the fragile path injection prominently.

**F-07. lessons.md L-005 references "Opus 4.7"**
- **File:** `lessons.md`, L-005 entry
- **Problem:** References "Opus 4.7" as synthesis-tier model. Current environment is Opus 4.6. May be forward-looking or a naming drift.
- **Fix:** Verify intended model reference. If L-005 should reference the current model, update. If it's about a future model, add a note.

**F-08. tools/_probe_launcher.sh uses system Python**
- **File:** `tools/_probe_launcher.sh`
- **Problem:** Uses `/usr/bin/python3` (system Python 3.9 on macOS). CLAUDE.md pinned interpreter policy says all execution must go through `.venv/bin/python3`. Low risk since probes use subprocess calls to `openclaw`, not direct imports.
- **Fix:** Update shebang/invocation to use `.venv/bin/python3` for consistency, or document the exception.

---

## REMOVE — Files/artifacts to delete

**R-01. pipeline/orchestrator/routing.yaml.bak.2026-04-14**
- Backup of old routing config. Live config is `router.yaml` at workspace root. Dead weight.

**R-02. pipeline/orchestrator/run_log.json.canonical-stub.bak**
- Empty-runs stub backup (`{"version": 1, "runs": []}`). No value.

**R-03. CODE_REVIEW_BOARD_HEALTH_2026-04-14.json**
- One-time board-health snapshot from 2026-04-14 with stale model references (kimi-k2-instruct). Outdated point-in-time artifact.

**R-04. pipeline/blueprint/01_sovereignty_envelope.md** (outside v0.1/)
- Explicitly marked `STATUS: SUPERSEDED — 2026-04-16`. Replaced by `v0.1/section_1_sovereignty_envelope.md`.

**R-05. pipeline/blueprint/v0.1/section_2_vault_topology.md**
- Stale draft (DRAFT status, v5-r8 arch ref). Superseded by `section_02_vault_topology.md` (v7.1 LOCKED).

**R-06. pipeline/blueprint/v0.1/section_4_logician.md**
- Stale draft (DRAFT status, v5-r8 arch ref). Superseded by `section_04_logician.md` (v2.1 LOCKED).

**R-07. pipeline/blueprint/v0.1/section_5_pipeline.md**
- Stale draft (DRAFT status, v5-r8 arch ref). Superseded by `section_05_pipeline.md` (v6 LOCKED).

**R-08. pipeline/tilth/ directory** (3 files + traces/)
- `tilth_pipeline.py`: Pre-refactor monolithic orchestration script.
- `scout_live.py`: Hardcoded Replit session path (`/sessions/dazzling-keen-curie/mnt/GoldenQuill`). Dead code.
- `db_tools/extend_calendar.py`: Pre-refactor utility.
- `traces/`: 6 JSON trace files from 2026-04-15.
- All superseded by `pipeline/loop/`, `pipeline/scout/`, etc. Entire directory is legacy.

**R-09. logician/ (top-level directory)**
- Pre-pipeline monolith: `logician.py` (CLI tool), `gates/`, `filters/`, `registers/`, `config/`, `tests/`. Contains stale `.cpython-310` pycache files.
- Superseded by `pipeline/logician/` (modular, architecturally locked).
- **Before deleting:** Verify that `workspace_isolation_gate.py` and `client_term_leak_gate.py` logic has been ported to `pipeline/logician/`. The top-level `registers/admin_risk_register.json` and `registers/architectural_risk_register.json` may also contain data not yet migrated.

**R-10. tools/ one-time migration scripts** (6 files)
- `_phase1_consolidate.sh`, `_phase2_harvest.sh`, `_phase3_repoint.sh`
- `_audit_consolidate.sh`, `_audit_harvest_gap.sh`, `_audit_launcher.sh`
- One-time migration/consolidation scripts from skill dedup and workspace reorg. Already ran. Archive or delete.

**R-11. _archive_GoldenQuill_pre-bedrock_2026-04-14/ Replit .bin files**
- `GrantFinderWriter/.local/state/replit/agent/` contains ~60 Replit agent state binary files. Dead weight. The archive itself has value as provenance, but the `.bin` files are garbage.

---

## STALE — Outdated references to update

**S-01. CLAUDE.md references `pipeline/architecture/v0.1/tilth_architecture_locked.md` as "LOCKED 2026-04-16"**
- Architecture is now at v7, LOCKED-internal 2026-04-19. The file still exists (it's the original v4 lock), but the canonical locked architecture is now v7. SESSION_BOOTSTRAP.md already says "v7, A1-A12" — CLAUDE.md should align.

**S-02. CLAUDE.md "Locked architecture" says "unanimous Thesis Team verdict"**
- This described the 2026-04-16 lock. Architecture has been through v5, v6, v7 since then with amendments (v7.0.1). The description is stale for the current state.

**S-03. SESSION_BOOTSTRAP.md locked decisions say "Architecture v7 LOCKED 2026-04-19"**
- Architecture v7.0.1 amendment exists (`architecture_v7_0_1_amendment.md`). SESSION_BOOTSTRAP should note the amendment.

**S-04. MEMORY.md section 4a-extra references "three new thesis rounds" from "2026-04-19 evening"**
- These are no longer "new" — they're 1 day old and integrated. The "extra" label and breathless framing ("three new thesis rounds") should be normalized into the regular memory structure.

**S-05. Multiple architecture versions in pipeline/architecture/v0.1/**
- `tilth_architecture_locked.md` (v4, 2026-04-16)
- `tilth_architecture_locked_v4_2026-04-16.md` (explicit v4 copy)
- `tilth_architecture_locked_v5_r8_2026-04-17.md` (v5)
- `tilth_architecture_locked_v6_r2_2026-04-18.md` (v6)
- `tilth_architecture_locked_v7_a1_a6_2026-04-19.md` (v7 partial)
- `architecture_v7_0_1_amendment.md` (current amendment)
- These are an audit trail but the naming doesn't make it clear which is canonical. Consider adding a symlink or pointer file (e.g., `CURRENT → tilth_architecture_locked_v7_a1_a6_2026-04-19.md + architecture_v7_0_1_amendment.md`).

**S-06. HeartbeatQAfiles/ (Sentinel agent) dormant since 2026-04-14**
- Last QA report is `SN-QA-REPORT-2026-04-14-MIGRATION.md`. No activity in 6 days. MEMORY.md still references it as active. If Sentinel is deprecated for v0.1, say so. If it's paused, note the pause.

**S-07. skill_decisions.yaml in tools/**
- One-time operator input template for skill-drift resolution during workspace migration. Migration is complete. Archive or delete.

**S-08. pipeline/radar/ scan files from 2026-04-14 and 2026-04-15**
- 10 JSON scan files and 2 analysis MDs from early Scout runs. These are pre-pipeline-refactor outputs. If Scout's current pipeline writes to a different location, these are orphaned. If they're still the canonical radar output location, they need a retention policy.

**S-09. pipeline/blueprint/v0.1/ contains versioned copies alongside locked versions**
- e.g., `section_02_vault_topology_v4_2026-04-16.md` and `section_02_vault_topology_v7_2026-04-18.md` alongside `section_02_vault_topology.md` (current).
- Same for `section_00_5_interface_index.v1.json`, `v1_preserved_2026-04-18.json`, `v3.json`, etc.
- These are audit trail, not duplicates. But naming convention makes it ambiguous which is canonical vs historical. The `_locked` suffix on some but not others adds confusion.

**S-10. daily_logs/ gap — no entry for 2026-04-16**
- Entries exist for 04-13, 04-14, 04-15, 04-17, 04-18, 04-19, 04-20. April 16 is missing. May have been a day off, but worth noting since architecture v4 was locked that day (per CLAUDE.md) — that decision should have a daily log entry.

---

## Test Gaps

**T-01. No adversarial tests for pipeline/loop/errors.py**
- `tests/loop/test_errors.py` exists but no `test_adv_errors.py`. Every other loop module with adversarial exposure has both.

**T-02. No adversarial tests for pipeline/loop/revision_loop.py**
- `tests/loop/test_revision_loop.py` exists but no `test_adv_revision_loop.py`. Given revision_loop is the Section 5 capstone orchestrator, adversarial coverage matters.

**T-03. No test for pipeline/scout/channel_c_portals.py channel_d paths**
- `tests/scout/` has rounds 1-4 but no `test_round_5_channel_c_portals.py`. Spec card `scout_round_5_channel_c_d.md` exists and is pre-staged.

---

## Counts

| Category | Count |
|----------|-------|
| CLEAN | 14 |
| FIX | 8 |
| REMOVE | 11 |
| STALE | 10 |
| TEST GAP | 3 |

**Overall assessment:** The codebase is architecturally coherent and well-organized for its complexity. The main systemic issues are: (1) lock_history.v1.jsonl was introduced mid-build and needs backfill for ~42 modules across Sections 1F-J, 2, 3, and 4; (2) a layer of pre-pipeline legacy code (top-level `logician/`, `pipeline/tilth/`) should be archived; (3) blueprint versioned copies need a clearer canonical-vs-historical naming convention. No broken imports, no circular dependencies, no orphaned lock entries. The foundation is solid.
