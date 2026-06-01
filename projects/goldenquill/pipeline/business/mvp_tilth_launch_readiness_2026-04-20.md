# MVP Tilth — Launch Readiness Checklist

**Filed:** 2026-04-20
**Last updated:** 2026-04-21 (Wave 2 close + Wave 3 Session A F-AMDT-05 LOCK + Scout R7 LOCK)
**Filed by:** Cowork session per Josh's ask ("give me a doc to continue this process with a full list of what's left to being ready to launch MVP Tilth")
**Purpose:** Single-source-of-truth readiness register. Read at session open. Update at session close. Replaces ad-hoc "what's left?" questions.
**Read order:** Section 1 (MVP Scope) → Section 3 (Current State Snapshot) → Section 5 (Task Register) → Section 9 (Ship Gate). Everything else is reference.

---

## 1. MVP Scope Definition

**What v0.1 Tilth IS:**

- Solo-operator grant-intelligence system running on Josh's M1 8GB Mac Mini dev box (production target: 128GB Golden Quill).
- Headless — no UI layer. Operator interacts via terminal + Cowork + OpenClaw dashboard.
- Five council seats (Scout, Scribe, Editor, Judge, Logician) + Code Thesis Committee (5 code reviewers).
- BYOK providers: Anthropic (Scribe primary), Groq Dev tier (Editor/Judge/Red Team), Google (Judge primary + Reasoner Review), OpenAI direct (code reviewer 1 + Red Team escalation), Ollama (Scout local primary).
- Pipeline: Scout → Phase 0 Intake → Scribe → Editor → Judge → Logician → LOCK-sealed artifact.
- Full sovereignty: all keys operator-owned, no phone-home, Cedar-enforced Law 3 org isolation, hash-chained audit ledger.
- Multi-client: Josh serves multiple orgs under `orgs/` folder isolation.

**What v0.1 Tilth is NOT:**

- Not a UI product. Next.js / web dashboard = v0.2+.
- Not a managed service. Metered billing / multi-tenant hosting = REJECT-LOCKED.
- Not MaatAI. Sovereign Node + central brain = Stage 5.
- Not federated. Contractor federation + selective shared posture = Stage 4.
- Not a team product. Multi-Cultivator seats per Tilth = Stage 2.
- Not a replacement for operator judgment. Applicant brings the substance (Law 5). Tilth shapes; operator decides.

**First-run acceptance:** operator dispatches one real grant application end-to-end through the pipeline, with all LOCK gates firing, all Cedar policies enforcing, all signatures landing. Success = applicant signs off on the final draft AND the provisioning manifest reflects the run in lock_history + session_log.

---

## 2. Product Naming Chain (reference)

Per `CLAUDE.md`:
- **Golden Quill** = hardware. 128GB desktop supercomputer in custom gold case.
- **Tilth** = agentic software intelligence on one Golden Quill. "One Tilth per Golden Quill."
- **Cultivator** = per-employee phone interface (Telegram-bot v0.1). Out of scope for Stage 1 solo MVP.
- **MaatAI** = central brain. Stage 5. Out of scope.
- **Sovereign Node** = coop-owned compute where MaatAI lives. Stage 5. Out of scope.

v0.1 MVP delivers Tilth + its headless pipeline. Golden Quill hardware procurement is a parallel track (SKUs: M3 Ultra Mac Studio, AMD GX-10, NVIDIA DGX Spark / ASUS Ascent GX10).

---

## 3. Current State Snapshot (2026-04-21)

### 3.1 Blueprint LOCKs (internal, pending outside audit)

| Artifact | Status |
|---|---|
| Architecture v7 (A1–A12) | LOCKED-internal 2026-04-19 |
| Architecture v7.0.1 amendment | LOCKED-internal |
| §0.5 Interface Index v4 | LOCKED-internal 2026-04-19 |
| §1 Sovereignty Envelope v5/v6 | LOCKED-internal 2026-04-18 |
| §2 Vault Topology v7.1 | LOCKED-internal |
| §3 Scout | LOCKED-internal |
| §4 Logician v2.1 | LOCKED-internal 2026-04-18 |
| §4 v2.3 Privacy Router amendment | LOCKED-internal 2026-04-19 |
| §4 v2.4 + v2.5 Canary + Runtime Integrity | LOCKED-internal 2026-04-19 |
| §5 Pipeline v5 | LOCKED-internal 2026-04-18 |
| §5 v6 amendment | LOCKED-internal 2026-04-19 |
| §5 v6.1 seat-output-schema pin | **PROPOSAL** (this session) — park or dispatch |

### 3.2 Amendments (policy-lock, operator-authorized 2026-04-20)

| Amendment | Status | Hash (SHA3-512 prefix) |
|---|---|---|
| EN-001 SDK Scribe Spike | LOCKED-sealed (policy-lock) | 532f8cc5… |
| EN-002 SDK Lifecycle Vocabulary | LOCKED-sealed (policy-lock) | 1d5cab47… |
| EN-003 Kimi→Gemini Code Thesis Committee | LOCKED-sealed (policy-lock) | 570699c6… |
| TSIP v0.1 | LOCKED-sealed (policy-lock; bootstrap exception CONSUMED) | 367c4756… |

Authorization ledger at `pipeline/engineering/operator_authorization_ledger.v1.jsonl`. Ed25519 cryptographic seal pending v2.2 gate #5 (`F-ROLLBACK-SCRIPT-INTEGRITY`) + #10 (`F-ROUTER-INTEGRITY-MULTI-SOURCE`) infrastructure.

### 3.3 Section 1 (Sovereignty Envelope) modules

| Round | Module(s) | LOCK status |
|---|---|---|
| A | `_types.py`, `crypto_primitives.py`, `org_slug.py` | LOCKED 2026-04-19 |
| B | `audit.py`, `topology.py` | LOCKED 2026-04-19 |
| C | `keys.py` | LOCKED 2026-04-19 |
| D | `isolation.py` | LOCKED 2026-04-19 |
| E | `session.py`, `interrupted_state.py` | LOCKED 2026-04-19 |
| F | `admin_risk.py`, `degradation_log.py` | LOCKED-backfilled (per F-03 backfill) |
| G | `rfa_envelope.py`, `project_context_envelope.py` | LOCKED-backfilled |
| H | `router_integrity.py` | LOCKED-backfilled |
| I | `boot.py`, `boot_clock.py`, `lockfile.py`, `init_marker.py` | LOCKED-backfilled |
| J | Section 1 integration + BT property tests (BT1/2/3/4/6/8 × ≥12 each; 100-org fuzz; §7 conftest) | **SELF-LOCKED 2026-04-21** — 214 tests / 2318 LOC / 4 test files; §1 promoted from LOCKED-per-module → LOCKED-as-a-whole-section. Aggregate coverage 86% union-drift (per-module Rounds A-I were 100% individually; flagged as union-measurement drift). Awaits operator sign-off. |

### 3.4 Section 2 (Vault), 3 (Scout), 4 (Logician), 5 (Pipeline)

| Section | Modules built | Formal LOCK |
|---|---|---|
| §2 Vault | 17 modules on disk (init_marker, vault_boot, m15_ledger, etc.) | LOCKED-backfilled via F-03; **committee-review dispatch now UNBLOCKED by §1 Round J capstone** — promotes §2 from LOCKED-backfilled to formal committee LOCK |
| §3 Scout | 13 modules — Rounds 1-9 LOCKED (8 channel modules + discover.py capstone dispatcher + verify_stage.py four-verdict VERIFY); R10 REVIEW + entity_research pre-staged (two-module spec with operator-disposition split/bundle question); R11 `run_scout_discover_verify` capstone-of-capstones queued | Rounds 1–9 LOCKED (R9 SELF-LOCKED 2026-04-21 at 142 tests / 1065 LOC / 243 stmts / 100% cov; **§3 Scout at 9 consecutive SELF-LOCK rounds with zero committee-surfaced corrections**) |
| §4 Logician | 9 modules (privacy, runtime_integrity, canary, AST-lint, admin_risk) + **v2.2 gate queue CLOSED 2026-04-21 — all 12 gates LOCKED**. Consolidated §4 v2.2 blueprint DRAFT assembled at `pipeline/blueprint/v0.1/section_04_v2_2_consolidated_amendment_DRAFT.md` — LOCK data populated, Thesis-round dispatch next | **12/12 v2.2 gates LOCKED** + consolidated blueprint DRAFT assembled; Thesis-round dispatch next |
| §5 Pipeline | pipeline.loop foundations (Rounds 1-2 LOCKED; Rounds 3-5 on disk/LOCKED; **Round 6 post_gate_runner SELF-LOCKED 2026-04-21** at 37 tests / 555 LOC / 100% cov / 4 ORIENT-resolved; Round 7 rate_limiter spec pre-staged at `section_05_round_7_rate_limiter.md`) | Rounds 1–6 LOCKED; R7 staged |
| §4 Logician | 9 modules (privacy, runtime_integrity, canary, AST-lint, admin_risk) + **v2.2 gate queue CLOSED 2026-04-21 — all 12 gates LOCKED**: W1 POST×2 (F-AMDT-02/03) + W2 PRE×3+POST×1 (F-AMDT-01/06/07/12) + W3 PRE×5 (F-AMDT-05/10/11/08/09) + W4 PRE×1 (F-AMDT-04). ~928 tests on gate modules; committee 5/5 PASS cycle-1 zero corrections on every dispatch | **12/12 v2.2 gates LOCKED** + v2.1/v2.3/v2.4/v2.5 amendments; consolidated §4 v2.2 blueprint Thesis round next (spec pre-staged at `pipeline/engineering/spec_cards/logician_v2_2_consolidated_blueprint_amendment.md`) |
| §5 Pipeline | pipeline.loop foundations (Rounds 1-2 LOCKED; Rounds 3-4 on disk; Round 5 SELF-LOCKED 2026-04-20; Round 6 spec staged) | Rounds 1–5 LOCKED |

### 3.5 Test suite

- **Total tests:** 4184 pass, 3 skip, 1 xfail, 0 fail (as of **§1 Round J capstone SELF-LOCK 2026-04-21**; +393 over v2.2 queue close baseline 3791: §5 R6 post_gate_runner +37, Scout R9 verify_stage +142, §1 Round J capstone +214)
- **v2.2 queue:** 12/12 gates LOCKED with ZERO committee-surfaced corrections across every dispatch (Protocol-first + single-gate-scope hypothesis confirmed at n=12)
- **Discipline streak:** §3 Scout 9 consecutive SELF-LOCK rounds zero committee corrections; §4 Logician v2.2 12 consecutive Code Thesis Committee 5/5 PASS cycle-1
- **AST-lint:** clean (R1-R7 on all new modules, exit 0)
- **Coverage highlights:** 100% on scout/channel_c_portals, scout/channel_d_program_pages, scout/_feedparser_adapter, scout/channel_f_websearch, scout/_channel_f_jurisdictions, pipeline/loop/errors, logician/gates/f_rollback_script_integrity; 99% on scout/channel_e_rss (3-stmt defensive dead code documented); 98% on pipeline/loop/revision_loop
- **Full-suite runtime:** ~25s on M1 8GB
- **Lazy-load discipline:** `feedparser` not in `sys.modules` after `import pipeline.scout` (verified per Round 6 E-026 lesson)
- **Engineering-lesson elevations (2026-04-21):** E-024 (1.5× LOC/test-count multiplier when Protocols + V1 rebind-resistance + E-023 deferred-scope trident applies) + E-026 (`__module__` lineage over `is` identity under `sys.modules` reload) formally landed in `pipeline/engineering/review_lessons.v1.md`; spec-card-template (`engineering_process_v0.1.md` §11) amended with clauses for both

### 3.6 Lock history

- `pipeline/engineering/lock_history.v1.jsonl` — 80+ rows (18 original + 44 F-03 backfilled + 3 from Window A T-gap closures + seat_runner backfill + 2 Scout R6 + 3 Scout R7 + 4 Wave 2 gates + 1 Wave 3 F-AMDT-05 + Session A shared-infra row)
- Verdict differentiation: LOCKED vs SELF-LOCKED-pending-committee vs LOCKED-backfilled
- Formal lessons updated 2026-04-21: **L-011** (transport-retry carve-out), **L-012** (scope-honest pushback pre-flight), **E-024** (1.5× LOC/test-count multiplier), **E-026** (`__module__` lineage over `is` identity under sys.modules reload). L-011 + L-012 in `lessons.md`; E-024 + E-026 in `pipeline/engineering/review_lessons.v1.md`.
- F-05 deep-import flags propagated on 5 implicated module records
- Scout R6 canonical daily_log LOCK blocks landed — first live use of gate #12 discipline format ahead of the gate's implementation

### 3.7 Infrastructure

- **OpenClaw:** installed with LaunchAgent daemon + dashboard at http://127.0.0.1:18789
- **Providers:** Anthropic, Groq Dev tier ($20/mo), Google plugin (enabled 2026-04-19), OpenAI direct (enabled 2026-04-19), Ollama (local)
- **Custom skills:** scout-discovery, scribe-ghostwriter, editor, judge-rubric, logician, council-pipeline
- **MemPalace:** v3.1.0 installed with OpenClaw MCP integration (ChromaDB 1.5.7, palace at ~/.mempalace)
- **RTK:** v0.35.0 installed for token compression
- **Venv:** `.venv` pinned to Python 3.14 (per CLAUDE.md; system python3 on macOS is 3.9 and cannot even collect the test suite)

### 3.8 Client orgs

- `orgs/` folder: 7 client folders + template + ORG_INDEX.md
- Active: MycoSymbiotics Cooperative, MycoSymbiotics Inc, Mystic Mamas, Run a Muck Farm, FIT Farms LLC, plus two more per index
- Each carries PROJECT_CONTEXT.md with [NEEDED] fields pending operator fill
- Law 3 isolation enforced via folder boundary (Cedar policies pending per §4)

---

## 4. Dependency Graph (what blocks what)

```
Section 1 modules (Rounds F/G/H/I/J + capstone LOCK)
    ↓
§2 Vault implementation (Group 5)  ←— currently BACKFILLED only, not formal LOCK
    ↓
§4 Logician full implementation (Group 7) ← consumes §2 Vault
    ↓
v2.2 gate implementation × 12 gates (Wave 1 → Wave 4)
    ↓
§4 v2.2 blueprint amendment LOCK (captures gates as blueprint)
    ↓
§5 Pipeline finish (Group 8) ← all remaining §5 rounds
    ↓
Group 9 E2E integration tests
    ↓
Group 10 outside-impartial audit  ←— THE REAL LOCK (no exceptions)
    ↓
Group 11 v0.1 SHIP gate
```

**Parallel-safe tracks (off critical path):**
- Scout Rounds 6 (Channel E RSS) + 7 (if needed for F) — can run parallel with §4/§5 work
- Admin_risk v2.2 register merge + path decision — operator-gated but doesn't block code
- Cedar policy files — parallel Code window (currently drafting)
- Cleanup passes (R-01 through R-11 deletions; S-01 through S-10 doc sync) — parallel with anything
- F-04 structured STATUS field on spec cards — parallel
- F-06 GPP path injection fix — parallel
- F-08 probe launcher shebang — parallel

---

## 5. Task Register (grouped by urgency + scope)

### Tier 0 — In flight this session

| # | Task | Owner | Status |
|---|---|---|---|
| 0.1 | Window A: seat_runner LOCKED-backfilled row | Midas | Closing |
| 0.2 | Window B: v2.2 Wave 1 gates F-AMDT-02 + F-AMDT-03 | Midas | Running |
| 0.3 | Cedar policy files drafting | Another window | Running |
| 0.4 | Admin_risk v2.2 proposal expansion | Cowork (this session) | **Done 2026-04-20** |
| 0.5 | §5 v6.1 proposal doc filed | Cowork (this session) | **Done 2026-04-20** |
| 0.6 | This readiness doc | Cowork (this session) | **Done 2026-04-20** |

### Tier 1 — Operator decisions pending

| # | Decision | Blocks |
|---|---|---|
| 1.1 | Admin_risk v2.2 proposal: approve, revise, or reject | Live register merge; path decision (1.2) |
| 1.2 | Admin_risk path: move register to `pipeline/institutional_memory/admin_risk_register.yaml` OR repoint POST step 6 to current path | POST step 6 validation gate; first-run |
| 1.3 | §5 v6.1 proposal: dispatch Thesis round now OR park to v2.3 post-MVP | §5 v6.1 LOCK; seat-output-schema pin landing |
| 1.4 | F-AMDT-12 (daily-log LOCK-block) wave assignment: keep in v2.2 Wave 2 OR split to v2.3 if Wave 2 gets heavy | v2.2 implementation ordering |
| 1.5 | §4 v2.2 blueprint amendment — draft + dispatch Thesis when v2.2 gates implemented, OR leave as spec-card-only and compile into §4 v3 at v0.2 | v2.2 gates formal LOCK status |
| 1.6 | MaatAI Stage-5 naming discipline — internal only for v0.1, reaffirm | Customer-facing V1 copy |

### Tier 2 — Cowork small-batch (ready to execute)

| # | Task | Estimated effort | Dependency |
|---|---|---|---|
| 2.1 | F-04 add `STATUS:` field to 26 spec cards | 30-60 min | None — mechanical |
| 2.2 | F-06 GPP path injection fix — move GPP tools to proper package OR document + lock path | 60-90 min | Operator decision on package home |
| 2.3 | F-08 `tools/_probe_launcher.sh` shebang fix (`.venv/bin/python3`) | 5 min — DONE 2026-04-20 (pinned via `$PYBIN` with existence check, not bare swap) | None |
| 2.4 | S-01/S-02/S-03 sync CLAUDE.md + SESSION_BOOTSTRAP.md + MEMORY.md → architecture v7.0.1 | 30 min — DONE 2026-04-20 (new `project_tilth_architecture_v7_locked.md` memory file; v6-r2/v5-r8/v4 chain marked superseded) | None |
| 2.5 | S-04 MEMORY.md "4a-extra" normalization — remove "three new thesis rounds" breathless framing; integrate into normal memory structure | 15 min | None |
| 2.6 | S-05 Architecture version canonical-marker — symlink or CURRENT pointer in pipeline/architecture/v0.1/ | 15 min | Operator preference on symlink vs pointer file |
| 2.7 | S-06 HeartbeatQAfiles dormant-status marker | 5 min — DONE via F-01 fix 2026-04-20 | None |
| 2.8 | S-07 tools/skill_decisions.yaml archive/delete (post-migration) | 5 min | Operator confirm migration complete |
| 2.9 | S-08 pipeline/radar/ scan files retention policy | 30 min | Operator decides retention window |
| 2.10 | S-09 blueprint versioned copies canonical-vs-historical naming discipline | 60 min | Partially covered by S-05 |
| 2.11 | S-10 daily_logs/ gap — add 2026-04-16 entry (architecture v4 LOCK day, per CLAUDE.md) | 15 min | None |
| 2.12 | R-01 delete `pipeline/orchestrator/routing.yaml.bak.2026-04-14` | 1 min — DONE 2026-04-20 | None |
| 2.13 | R-02 delete `pipeline/orchestrator/run_log.json.canonical-stub.bak` | 1 min — DONE 2026-04-20 | None |
| 2.14 | R-03 delete `CODE_REVIEW_BOARD_HEALTH_2026-04-14.json` | 1 min — DONE 2026-04-20 | None |
| 2.15 | R-04 delete `pipeline/blueprint/01_sovereignty_envelope.md` (SUPERSEDED) | 1 min — DONE 2026-04-20 | None |
| 2.16 | R-05 delete stale `pipeline/blueprint/v0.1/section_2_vault_topology.md` | 1 min — DONE 2026-04-20 | None |
| 2.17 | R-06 delete stale `pipeline/blueprint/v0.1/section_4_logician.md` | 1 min — DONE 2026-04-20 | None |
| 2.18 | R-07 delete stale `pipeline/blueprint/v0.1/section_5_pipeline.md` | 1 min — DONE 2026-04-20 | None |
| 2.19 | R-08 `pipeline/tilth/` directory archive/delete (pre-refactor monolith) | 10 min — DONE 2026-04-20 (tilth_pipeline.py, scout_live.py, db_tools/, traces/ all removed) | Verify no stale pointers |
| 2.20 | R-09 top-level `logician/` directory archive — verify ported content first | 30 min — IN PROGRESS 2026-04-20 (port-and-repoint pass underway: 5 gate modules + board_health + registers need migration to pipeline/logician before directory can delete; tools/audit_dispatcher.py + tools/code_review_probe.py import top-level paths and must be repointed) | Operator verification of registers/ content |
| 2.21 | R-10 `tools/` one-time migration scripts archive/delete | 5 min — DONE 2026-04-20 (_phase1/2/3 + _audit_consolidate/_audit_harvest_gap/_audit_launcher removed) | None |
| 2.22 | R-11 `_archive_GoldenQuill_pre-bedrock_2026-04-14/` replit .bin files cleanup | 5 min — DONE 2026-04-20 (audit path was wrong; real location was `.../Sovereign_Node_Handoff/prior_work/Supporting_Docs/GrantFinderWriter/.local/state/replit/agent/`, ~60 .bin files purged) | None |
| 2.23 | Admin_risk v2.2 remaining-entry tagging (60+ entries w/o explicit progressive_register; top-15 already tagged) | 2-3 hours | Operator approval of v2.2 taxonomy |
| 2.24 | Admin_risk register "known gaps" entries (progressive, advocacy, oppression/liberation, settler-colonial, capitalism, food apartheid, state-level FL/TX/ID bans, religious-liberty-needle-threading, international-development vocabulary) | 1-2 hours research + draft | Operator approval of scope expansion |

### Tier 3 — Code-window medium (waves, spec-carded, staged)

| # | Task | Wave / Spec | Estimated effort | Dependency |
|---|---|---|---|---|
| 3.1 | v2.2 Wave 1 gates: F-AMDT-02 (F-VERDICT-BLOCKING-MISSING), F-AMDT-03 (F-VERDICT-CITATION-MISSING) | Wave 1 | **In Window B** | None (Wave 1 = no external deps) |
| 3.2 | v2.2 Wave 2 gates: F-AMDT-01 (F-BOOTSTRAP-REUSE), F-AMDT-06 (F-DEPRECATION-EXEMPTION-REUSE), F-AMDT-07 (F-AMENDMENT-SELF-REFERENCE-DETECT v1 + v1.1), F-AMDT-12 (F-DAILY-LOG-LOCK-BLOCK-MISSING) | Wave 2 | 2-3 Code sessions per gate × 4 gates = 8-12 sessions | Wave 1 LOCK |
| 3.3 | v2.2 Wave 3 gates: F-AMDT-05 (F-ROLLBACK-SCRIPT-INTEGRITY), F-AMDT-08 (F-COMMITTEE-DEGRADATION-TIMEOUT), F-AMDT-09 (F-DEPRECATION-REGISTER-STALENESS), F-AMDT-10 (F-ROUTER-INTEGRITY-MULTI-SOURCE), F-AMDT-11 (F-DEGRADATION-STANZA-PRECEDENCE) | Wave 3 | 2-3 Code sessions per gate × 5 gates = 10-15 sessions; #5, #10, #11 share Ed25519 infrastructure (build once, share) | Wave 2 LOCK; Ed25519 infra build |
| 3.4 | v2.2 Wave 4 gate: F-AMDT-04 (F-SDK-PRECEDENT-REUSE) | Wave 4 | 2-3 Code sessions | Wave 3 LOCK |
| 3.5 | Scout Round 6 Channel E RSS | Spec: `scout_round_6_channel_e_rss.md` (pre-staged) | 1-2 Code sessions | None — parallel-safe |
| 3.6 | §5 Pipeline Round 6+ (post-gate runner, provider cascade, telemetry aggregation — remaining §5 v6 content) | Spec cards partially exist (round_6_post_gate_runner) | 3-5 Code sessions | seat_runner regression closed (DONE); Round 5 LOCK (DONE) |
| 3.7 | Section 2 Vault full LOCK (promote from LOCKED-backfilled to committee-reviewed LOCK) | Group 5 in roadmap | 3-4 Code sessions for per-module committee dispatch | Section 1 capstone LOCK |
| 3.8 | Section 4 Logician full committee review (per-module Thesis for 9 modules beyond v2.1 lock) | Part of Group 7 | 4-6 Code sessions | Section 2 LOCK; v2.2 Wave 1-4 LOCK |
| 3.9 | ARCH-05 R6/R7 completion confirmation (alias-tracker + CFG-dominance) | Spec: `arch05_ast_lint_walker_intensive.md` | Status check | Running — confirm LOCK |

### Tier 4 — Critical-path blockers (must close for Group 10)

| # | Gate | Blocks |
|---|---|---|
| 4.1 | Section 1 capstone LOCK verdict (Round J integration + BT1–BT8 property tests + §7 test suite) | Group 5 Vault formal LOCK (currently backfilled only) |
| 4.2 | §4 v2.2 blueprint amendment (captures 12 gates + gate #7 v1.1 as LOCKED blueprint rows) | v2.2 gates' formal LOCK status; §4 v2 → v3 roll |
| 4.3 | Cedar policy files: `org_isolation.cedar` + `compound_commit.cedar` + manifest SHA256 | POST step 6; first-run Law 3 enforcement |
| 4.4 | Admin_risk register path + approval | POST step 6 validation |
| 4.5 | §5 capstone LOCK (all rounds LOCK-sealed; §5 v6 + v6.1 decisions landed) | Group 8 close |
| 4.6 | Full suite green + 95%+ coverage on every LOCKed module | Group 9 pre-gate |

### Tier 5 — Ship gates (Groups 9, 10, 11)

#### Group 9 — Integration testing

| # | Test | What it proves |
|---|---|---|
| 9.1 | E2E: Scout → Scribe → Editor → Judge → Logician on VAPG FY26 + one real test org | Pipeline assembled correctly; all seats hand off cleanly |
| 9.2 | Cross-family runtime test: no same-family review paths | A3 cross-family rigor enforced at runtime |
| 9.3 | Sovereignty test: kill all network; pipeline runs local-only on Dev 8GB | BYOK + local-first sovereignty works |
| 9.4 | Law 3 isolation test: attempt cross-org read → fail-closed | Org isolation honored mechanically |
| 9.5 | Canary test: mutate router.yaml → blocks on STR regression | Runtime integrity gate fires |
| 9.6 | Fix + retest cycle | Group 9 green |
| 9.7 | Code Thesis Committee integration review | Integration approved by cross-family committee |

#### Group 10 — Outside-impartial audit (THE REAL LOCK)

| # | Step | Artifact |
|---|---|---|
| 10.1 | Onboard qualified outside engineering advisor per Da Vinci v2 §13 DV-F-10 (10+ yrs distributed systems / AI-ML ops / crypto / LM runtime) | Advisor signed into workspace with NDA |
| 10.2 | Advisor reviews architecture v7 + amendments | `pipeline/engineering/real_engineer_validation_arch_<date>.md` |
| 10.3 | Advisor reviews all blueprints (§0.5, §1, §2, §3, §4 including v2.2, §5) | `real_engineer_validation_blueprint_<date>.md` |
| 10.4 | Advisor reviews Section 1–5 code + test suites | `real_engineer_validation_code_<date>.md` |
| 10.5 | Advisor reviews GPP tool chain + council-dispatch + manifest signing | `real_engineer_validation_gpp_<date>.md` |
| 10.6 | Advisor signs per-section validation docs (pass / needs-revision) | Signed manifest |
| 10.7 | Address any needs-revision findings; re-audit | Close out any findings |
| 10.8 | Promote every LOCK-internal to LOCK-sealed | lock_history.v1.jsonl entries bumped to `seal_class: SEALED` |

#### Group 11 — Final ship

| # | Gate | Artifact |
|---|---|---|
| 11.1 | GPP-DET + GPP-COUNCIL pass on full system state | Green GPP reports |
| 11.2 | Final L-006 existence audit | All referenced files exist |
| 11.3 | Provisioning manifest final review (white-glove install on fresh machine) | Manifest LOCKED |
| 11.4 | GPP-SYNTHESIS: operator + advisor signatures on final manifest (Ed25519 + ML-DSA-65 hybrid) | Dual-signed manifest |
| 11.5 | Full test suite green on Dev tier (M1 8GB) | CI green; live suite run |
| 11.6 | Daily log entry: **v0.1 SHIP** | Last narrative line |
| 11.7 | First-run acceptance: live RFA dispatched end-to-end through pipeline with applicant sign-off | `pipeline/validation/first_run/<grant_id>/acceptance.md` |

---

## 6. Risk Register

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| R1 | L-005 two-audit ceiling violated again (Cycle N+1 spirals) | HIGH | v2.2 gate #12 + structural gates absorb policy iteration; operator disposition at ceiling is mandatory tripwire |
| R2 | Operator burnout / context switching across 5 parallel windows | HIGH | CLAUDE.md Session Efficiency discipline; handoff-under-50-lines rule; pre-stage next tasks; metrics log to catch drift |
| R3 | Groq Dev tier pricing or catalog drift (Kimi K2 already proved this vector) | MEDIUM | Cross-family fallbacks per router.yaml; L-009 catalog-vs-tier check; EN-003 family substitution pattern reusable |
| R4 | Google API quota (Gemini 2.5 Pro is Judge primary) | MEDIUM | Anthropic Opus 4.6 fallback on Judge escalation; rate-limit telemetry via v2.2 Wave 3 gates |
| R5 | Outside-audit advisor unavailable (Group 10 is the real LOCK) | HIGH | Pre-brief Da Vinci §13 requirements; maintain pipeline of candidate advisors; budget for 1-2 months advisor engagement |
| R6 | 8GB dev-box scale — production is 128GB; tests pass on 8GB but pipeline may surface behavioral differences at scale | MEDIUM | v0.1 ship criterion is "runs on 8GB"; 128GB is user production tier; validate-at-scale is a v0.1.x task |
| R7 | Sovereignty leak via third-party dependencies (PyYAML, httpx, feedparser, cryptography) | MEDIUM | EN-001 F-6 sovereignty-test-under-error-states pattern applicable; outbound traffic allowlist during integration tests |
| R8 | Cedar policy enforcement gap until files land + manifest signs | HIGH (Law 3) | Python path-slug fallback in degradation log; operator-review on every degradation entry; close as priority |
| R9 | Admin_risk register flags an applicant's own identity-affirming language because v2.2 dialect-axis tags are incomplete (only top-15 tagged explicitly; default mapping covers rest) | MEDIUM | Complete tagging for remaining 60+ entries as 2.23 task; operator can always override flagging |
| R10 | First-run grant application fails in a visible way | LOW (for MVP; bug → fix cycle is expected) | Group 9 integration tests should catch before first-run; close each failure as a lesson |

---

## 7. What's NOT in MVP scope (explicit non-goals)

Per CLAUDE.md "What NOT to do" + product naming chain:

- LangGraph, vLLM, local 70B models, NemoClaw, Phase 3 orchestration
- Managed Edition or metered billing
- Next.js UI or any UI layer
- PA Ag Innovation Grant as dogfood target (off the table)
- MaatAI operational (Stage 5 only)
- Sovereign Node infrastructure build (Stage 5 only)
- Multi-Cultivator seats per Tilth (Stage 2)
- Contractor federation (Stage 4)
- RESEARCH-BRIEF mode implementation (v1.1 Scout prompt defines it; implementation deferred to v0.1.x or v0.2 based on operator demand)
- Cross-org data sharing (Law 3 inviolate; cross-client research is opt-in Stage 5)

---

## 8. Today's session deliverables (2026-04-20 Cowork, reference)

Logged here for continuity across sessions.

- **F-02 routing.yaml Kimi K2 fallback** → `openai/gpt-oss-20b` (Groq Dev tier accessible, cross-family from Judge primary alibaba)
- **F-01 MEMORY.md HeartbeatQAfiles pointer** → fixed + dormant-since-2026-04-14 note
- **F-07 lessons.md "Opus 4.7" references** → replaced with "synthesis-tier model (per router.yaml escalation binding; never hardcoded)"
- **Logician v2.2 queue:** gate #8 spec card split from pending; 3 new spec cards (#9 F-DEPRECATION-REGISTER-STALENESS, #10 F-ROUTER-INTEGRITY-MULTI-SOURCE, #11 F-DEGRADATION-STANZA-PRECEDENCE); #7 extended to v1.1 (C4-NEW-04 author-family anti-collision); gate #12 F-DAILY-LOG-LOCK-BLOCK-MISSING added (from F-03 residual-gap flag); master gates file updated to v1.3, 12 gates total
- **EN-003 Cycle 4 disposition note** — Option 2 selected; 4 C4-NEW findings mapped to v2.2 queue; READ-ONLY deadlock resolved in gate code via `lock_class` distinction
- **Sig reconciliation (v2.2):** four amendment footers relabeled `Operator signature` → `Operator authorization token` + `Cryptographic seal (Ed25519): pending`; `operator_authorization_ledger.v1.jsonl` written with SHA3-512 content-binding hashes
- **Scout v1.1 narrow-patch:** Section 2.1 Law Stubs added; RESEARCH-BRIEF mode defined; Section 5 worked example + scale-match band (25%-200% of program median award)
- **Admin_risk v2.2 proposal:** 17 → ~75 entries; two-axis dialect discipline added (federal severity + progressive_register); 15 high-divergence entries explicitly tagged; status: operator_review PENDING
- **§5 v6.1 seat-output-schema pin proposal** filed at `pipeline/blueprint/v0.1/section_05_v6_1_seat_output_schema_pin_proposal.md`
- **This readiness doc** filed at `pipeline/business/mvp_tilth_launch_readiness_2026-04-20.md`

---

## 9. Ship Gate Definition (concrete)

**Tilth v0.1 MVP is ready to ship when ALL of the following are true:**

1. Every module in Sections 1–5 is LOCK-sealed (internal + outside audit + operator signature). No LOCKED-internal or LOCKED-backfilled remaining.
2. All 12 v2.2 Logician gates are implemented, tested (≥30 unit + ≥5 adversarial each, ≥95% coverage), AST-lint clean, and LOCK-sealed.
3. `§4 v2.2 blueprint amendment` is LOCK-sealed, codifying all 12 gates as blueprint rows.
4. Full pytest suite green on Dev tier (M1 8GB) with zero flakes across 3 consecutive runs.
5. AST-lint exit 0 across the entire codebase.
6. GPP-DET + GPP-COUNCIL pass on the full system state.
7. Cedar policies `org_isolation.cedar` + `compound_commit.cedar` LOCKed, signed, manifest SHA256 canonical.
8. `admin_risk_register.yaml` at canonical path, v2.2+ approved by operator, POST step 6 passes.
9. Ed25519 cryptographic seal on amendments (promoting PRE-CRYPTO-SEAL ledger rows to signed sidecars per v2.2 gate #5/#10 infrastructure).
10. Outside-audit advisor signatures on architecture + blueprints + code + GPP + Cedar (5 signed validation docs minimum; 8 expected per roadmap).
11. Operator + advisor signatures on final provisioning manifest (Ed25519 + ML-DSA-65 hybrid per GPP-SYNTHESIS).
12. **First-run acceptance** — live RFA end-to-end through pipeline, applicant sign-off, lock_history + session_log entries land, daily_log entry written.
13. Daily-log entry `2026-MM-DD.md` reads: **"v0.1 SHIP. Last character of code outside-audited and sealed."**

Any NO = not ready.

---

## 10. Tactical next-two-weeks plan (execution-ready)

Assumes Josh's bandwidth + 2-3 parallel Code windows + Cowork.

### Week 1

- **Day 1-2 (today + tomorrow):**
  - [x] Window A seat_runner close + backfill row
  - [x] Window B v2.2 Wave 1 (F-AMDT-02, F-AMDT-03)
  - [x] Cedar window draft files
  - [ ] Operator review admin_risk v2.2; approve + merge; decide path (1.1 + 1.2)
  - [ ] File remaining admin_risk v2.2 entry tags (2.23) + known-gaps research expansion (2.24)

- **Day 3-4:**
  - [ ] Window B Wave 2 kickoff: F-AMDT-01 + F-AMDT-06 + F-AMDT-07 v1 + v1.1 + F-AMDT-12 (4 gates)
  - [ ] Cleanup pass: R-01 through R-11 deletions (Cowork, fast)
  - [ ] Stale-doc sync: S-01/S-02/S-03 CLAUDE.md + SESSION_BOOTSTRAP.md + MEMORY.md → v7.0.1
  - [ ] F-08 probe launcher shebang (trivial)
  - [ ] Scout Round 6 Channel E RSS Code window (parallel track)

- **Day 5-6:**
  - [ ] Wave 2 close; Wave 3 kickoff (F-AMDT-05, F-AMDT-09 first — Ed25519 infra build)
  - [ ] F-04 structured STATUS field on 26 spec cards (2.1)
  - [ ] §5 Pipeline Round 6+ Code window

- **Day 7:** Week 1 close; session metrics review; update this readiness doc.

### Week 2

- **Day 8-10:**
  - [ ] Wave 3 continues (F-AMDT-08, F-AMDT-10, F-AMDT-11)
  - [ ] Section 2 Vault committee-review dispatch (promote from LOCKED-backfilled)
  - [ ] Operator decision on §5 v6.1 Thesis dispatch (1.3)

- **Day 11-12:**
  - [ ] Wave 4: F-AMDT-04
  - [ ] §4 v2.2 blueprint amendment draft + dispatch Thesis

- **Day 13:**
  - [ ] Section 1 capstone Round J integration + BT1–BT8 property tests
  - [ ] Ship-gate rehearsal: dry-run ALL 13 ship-gate criteria, identify remaining gaps

- **Day 14:** Week 2 close; advisor onboarding begins for Group 10; update this doc.

After day 14, Group 10 outside audit starts. Audit window is typically 2-4 weeks. Ship gate closes after audit clears. Realistic v0.1 SHIP target: 2026-05-15 to 2026-05-30.

---

## 11. Post-MVP Roadmap (context only)

Per CLAUDE.md five-stage product arc:

- **Stage 2 — Small team:** multi-Cultivator seats per Tilth, one Tilth per org, shared hardware. Next milestone after v0.1 SHIP.
- **Stage 3 — Cooperative org:** multi-orgs share hardware tier; Law 3 extended.
- **Stage 4 — Contractor federation:** independent operators each own Golden Quill; selective shared posture.
- **Stage 5 — MaatAI online on Sovereign Node:** central brain; opt-in cross-client research; v0.1 sovereignty contract preserved.

v0.1 MVP → Stage 2 transition requires: Telegram-bot Cultivator build; multi-seat permission model; Cedar policy extensions for seat-level isolation inside one Tilth.

---

## 12. How to use this doc

**Every session that touches this workspace:**

1. **Read this doc at session open** (after CLAUDE.md / SOUL.md / USER.md / router.yaml per AGENTS.md wake-up sequence).
2. **Check Section 5 Task Register** for your tier's open items.
3. **Identify blockers** — if your work depends on a Tier 1 operator decision, surface it before coding.
4. **On session close:** update this doc if any status changed (Tier-0 moves, Tier-1 decisions landed, Tier-2/3 items closed, new risks surfaced).
5. **Operator review cadence:** weekly, at minimum. Reconcile this doc with `pipeline/metrics/session_log.jsonl` and `daily_logs/` for honesty.
6. **When Section 9 Ship Gate flips from NO to YES across all 13 criteria:** v0.1 ships. Close this doc with a `SHIPPED` banner and start the Stage 2 readiness doc.

**Operator quick-ref:**
- "What's blocking me right now?" → Section 5 Tier 1 (decisions pending)
- "What can run in parallel?" → Section 4 (Parallel-safe tracks)
- "Are we ready?" → Section 9 (13 criteria; count remaining NOs)
- "What's the risk?" → Section 6
- "What did today's session produce?" → Section 8 (reference; this section will grow each session)

---

*Living document. Update on every session close. Archive and reset when v0.1 ships.*
*Filed 2026-04-20 by Cowork session. Read order: §1 → §3 → §5 → §9. Everything else is reference.*
