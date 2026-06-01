---
title: Tilth Full-Surface Audit Prompt — v1
date: 2026-05-16
author: Cowork (Claude Opus 4.7)
status: prompt artifact; no repairs authorized
purpose: a Tilth-specific, runnable audit framework that enumerates every load-bearing surface in the system, with per-surface acceptance question / evidence / failure mode / commands
companion_prompts:
  - pipeline/handoffs/project_wide_reconciliation_audit_prompt_2026-05-16.md (Codex; time-bound reconciliation audit; local vs origin vs PR #3 truth)
relationship_to_companion: |
  The Codex prompt audits *this moment* — the post-surge state at 2026-05-16, reconciling three Git baselines.
  This prompt is the *permanent* per-surface framework — designed to be re-runnable across releases.
  Use the Codex prompt for the immediate post-surge truth check; use this one as the standing audit playbook.
---

# Tilth Full-Surface Audit Prompt — v1

This prompt is a systematic audit playbook tailored to Tilth specifically. It is not a generic code-review template. It enumerates Tilth's load-bearing surfaces — §-numbered blueprints, F-* failure-code families, council seat contracts, posture enforcement paths, the LOCK ledger, the Ed25519 signing chain, the memory layer, the Cards cartridge schema, the Funder Intelligence Database scaffold, the planning-vs-blueprint distinction, the workspace discipline files, the cross-family bridge pattern, and the pinned Python interpreter — and for each surface gives an **acceptance question**, the **evidence to inspect**, and the **failure mode to look for**.

It is designed to be runnable two ways:

- **Long-form single sweep** (one auditor, one session, ~6–12h). Walk every surface in §3 in order. Write all findings to one validation directory.
- **Per-surface dispatch series** (multiple sessions / agents, one surface each, parallelizable). Each §3.x section is a self-contained task spec. Cross-family dispatch is the L-005 default for any surface tagged THESIS-REQUIRED.

Each mode is marked in §3 with the per-surface header.

This is a **no-repair audit**. Do not edit production code, blueprints, lock_history, daily_logs, customer data, or configuration. Write audit artifacts only under a new `pipeline/validation/<audit_name>_<date>/` directory.

---

## 1. Operating rules (non-negotiable)

1. Run the AGENTS.md wake-up sequence first: `SOUL.md` → `USER.md` → `router.yaml` → newest two `daily_logs/` → `lessons.md` → `MEMORY.md` → agent-specific overrides → task-specific PROJECT_CONTEXT.
2. Use path references, not content dumps (L-002).
3. Do not read multiple real org `PROJECT_CONTEXT.md` files in one session. Law 3 (Org Isolation) applies during audit.
4. Do not inspect, print, copy, or move secrets, BYOK files, private keys, `.env` files, or keystores.
5. Do not use network unless authorized. GitHub-connector reads are allowed if the session has an installed GitHub app and the operator asked for repo truth.
6. Every claim needs evidence: a path + line, a command + summarized output, a GitHub run/PR URL, or an explicit "not found" with the search performed.
7. Treat dated assessments as historical. The 2026-05-11 47/80 score is not current truth.
8. Never hardcode model bindings in audit output. Read `router.yaml` for current provider assignments.
9. Use the current three deployment postures only: `Frontier-Eligible`, `Split-Context Hybrid`, `Local-Only / Sovereign`. The "Sanitized" / opaque-slot-token vocabulary is retired (architecture v7.0.10 LOCKED 2026-05-11; supersession-ceremonied 2026-05-16 rows 238–249).
10. Apply L-022 weird/OOD probes per §4 (Phase 7) — surreal framing, role inversion, ambiguous instruction, time-pressure spoof, format spoof.
11. Use the pinned interpreter (`.venv/bin/python3` ≥3.14) for any test run. System `python3` on macOS is 3.9 and cannot collect the suite (per CLAUDE.md "Running tests — PINNED INTERPRETER").
12. Run tests via `scripts/run_tests.sh` or `.venv/bin/python3 -m pytest`. Never via system `python3 -m pytest`.

---

## 2. Output structure

Create:

```
pipeline/validation/<audit_name>_<YYYY-MM-DD>/
├── 00_method.md                # files read, commands run, GitHub state checked, skipped items
├── 01_findings_register.md     # ranked findings with severity + maturity + evidence + owner + remedy
├── 02_per_surface/             # one file per §3.x surface
│   ├── A_blueprint_section_<NN>.md
│   ├── B_failure_code_family_<name>.md
│   ├── C_seat_<name>.md
│   ├── D_posture_<name>.md
│   ├── E_memory_layer_<sublayer>.md
│   ├── F_cards_<aspect>.md
│   ├── G_lock_ledger.md
│   ├── H_ed25519_chain.md
│   ├── I_five_laws.md
│   ├── J_cross_family_bridge.md
│   ├── K_beta_workflow.md
│   ├── L_planning_vs_blueprint.md
│   ├── M_workspace_discipline.md
│   ├── N_pinned_interpreter.md
│   ├── O_github_ci.md
│   ├── P_sovereignty_egress.md
│   ├── Q_fid_scaffold.md
│   └── R_meta_audit.md
├── 03_weird_ood_probes.md      # L-022 probe outcomes
├── 04_remediation_map.md       # findings → tractable remediation batches
└── 99_final_verdict.md         # one-page exec summary
```

Severity tags (use only these): `P0_BLOCKS_GATE_1` · `P1_BLOCKS_GATE_2` · `P2_FIRST_90_DAYS` · `P3_LATER` · `INFO`.

Maturity tags (use only these): `REAL` · `PARTIAL` · `ASPIRATIONAL` · `CONTRADICTED` · `OUT_OF_SCOPE` · `UNKNOWN`.

Per the two-gate framing (canonical per `memory/project_alpha_label_two_gate_2026-05-16.md` — **note: this file is referenced in `pipeline/handoffs/tandem_qa_qc_remediation_decisions_2026-05-16.md` but does NOT exist on disk at 2026-05-16 evening; finding to surface in §3.A.20 + §3.M**):

- **Gate 1 — internal replay with Paul Norton.** PR #2 keepers · CC-003 quarantined · CC-005 doc-fix · TQA-009 + TQA-010 doc surgery · Logfire disabled-by-default.
- **Gate 2 — first paid client.** CC-004 signed-asset-manifest · CC-007 finalization · CC-008 redaction processor (v0.2) · CC-009 M13 end-to-end · Reflection Packet v0.2 first wave · `R-NO-DIRECT-PROVIDER-HTTP` mature · LIVE/DORMANT gate-family manifest.

---

## 3. Audit surfaces

### A. Architecture & Blueprint Layer

Tilth's v0.1 architecture LOCK is `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v7 A1-A12 LOCKED 2026-04-19) with successive v7.0.x amendments. Blueprint sections live at `pipeline/blueprint/v0.1/`. Each section is an audit surface.

#### A.0 — Architecture LOCK trail

Mode: SINGLE-SWEEP.

- **Acceptance question.** Is the architecture v7.0.x amendment trail complete and does every amendment file have a corresponding lock_history row?
- **Evidence.** `ls pipeline/architecture/v0.1/architecture_v7_0_*.md | sort` × `jq 'select(.lock_class | startswith("architecture")) | .module' pipeline/engineering/lock_history.v1.jsonl | sort -u`.
- **Failure mode.** Amendment file on disk but no lock_history row, or vice versa. Phantom architecture version cited in CLAUDE.md / SOUL.md / a §-blueprint but no on-disk amendment file. Multiple amendments with the same version suffix.

#### A.1–A.18 — Per-§ blueprint surface

Mode: PARALLEL-DISPATCH (one §-section per dispatch). Each section is independent unless flagged otherwise.

For each of `§0.5` (Interface Index) · `§1` (Sovereignty Envelope) · `§2` (Vault Topology) · `§3` (Scout) · `§4` (Logician) · `§5` (Pipeline) · `§6` (Operating Envelope) · `§7` (Scribe) · `§10` (Red Team) · `§11` (Intake) · `§12` (Uploader) · `§13` (Data Collector, v0.2 SPEC) · `§14` (Report Generator, v0.2 forward-compat) · `§15` (Archivist, v1.x) · `§16` (Reflection Packet) · `§17` (WPFA / CycleReceipt) · `§18` (Card System):

- **Acceptance question.** Does the on-disk §N blueprint file (latest LOCKed version + every published amendment) match (a) the architecture LOCK row that named it, (b) the lock_history row(s) under its module path, (c) the F-* family entries it references?
- **Evidence.**
  - File: `pipeline/blueprint/v0.1/section_<NN>_*.md` (main + amendment chain).
  - Lock rows: `jq 'select(.module | startswith("pipeline.blueprint.v0_1.section_<NN>"))' pipeline/engineering/lock_history.v1.jsonl`.
  - Predicate bodies for any F-* family it owns.
  - Companion §0.5 paired-commit row (if any).
- **Failure mode.** (1) Header version mismatch (`§N v1.1 LOCKED <date>` in file ≠ latest lock_history row for that module). (2) Forward reference to a v0.2 / v1.x feature that the section narrative treats as live. (3) Amendment-chain skip (v1.x → v1.x.2 with no v1.x.1 on disk). (4) Cited F-* primitive ID does not match the file in `pipeline/logician/gates/`. (5) `NotImplementedError` predicate body for a primitive the section says is enforced today.

#### A.19 — §0.5 Interface Index integrity (special case)

Mode: SINGLE-SWEEP (must hold the full ledger in one pass).

- **Acceptance question.** Does the lock_history-tracked Interface Index row count reconcile with the union of all `section_00_5_*_amendment.md` files? Is every paired-commit row in the lock_history backed by a discoverable amendment file? Does the v4 baseline `section_00_5_interface_index.md` + every amendment together cover every row claimed?
- **Evidence.**
  - `wc -l pipeline/blueprint/v0.1/section_00_5_interface_index.md`
  - `ls pipeline/blueprint/v0.1/section_00_5_*.md | wc -l`
  - `jq 'select(.lock_class | startswith("blueprint-interface-index")) | .row' pipeline/engineering/lock_history.v1.jsonl`
  - For each `§0.5 v<N>` paired-commit row, the amendment-file the row cites in `module` / `amendment_file`.
- **Failure mode.** (1) Paired-commit row references an amendment file that doesn't exist on disk. (2) Amendment file exists but is orphaned (no lock_history row). (3) Claimed runtime-live row count in the latest paired-commit row does not equal the sum of all prior paired-commit row deltas. (4) "Phantom row" — row cited in CLAUDE.md / a §-blueprint / customer-facing doc but absent from both the .md and amendment files. (5) The v4 baseline header still says "LOCKED v4 2026-04-19" — that's fine, but operator/auditor reading it sees v4 / 127 rows and misreads the system as smaller than it is. This is the **governance-theater watchpoint** Josh flagged 2026-05-16.

#### A.20 — Planning-vs-blueprint distinction

Mode: SINGLE-SWEEP.

- **Acceptance question.** Do planning docs (`pipeline/planning/*.md`) and dispatch handoffs (`pipeline/handoffs/*.md`) pre-bind operational decisions that have not been Thesis-reviewed at the §-blueprint layer?
- **Evidence.** For each planning doc dated after the most recent blueprint LOCK for the surface it touches, enumerate operator-pinned decisions in the planning doc and ask: does any of these decisions land in runtime code or in a §-blueprint without a corresponding Thesis-round paired-commit?
- **Failure mode.** Planning doc → handoff → runtime code path that skips §-blueprint Thesis review. Specifically watch the FID Phase 1 path (`pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` + `pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md`): if a future §19 (or §3-extension) blueprint round has to ratify-or-rewrite Phase-1 decisions, that's a planning/blueprint distinction failure surfaced as a re-litigation.

---

### B. Failure-code (F-*) family surfaces

125 `f_*.py` gate modules exist under `pipeline/logician/gates/` (counted 2026-05-16). Each family is a surface.

Universal acceptance question per family: **for each F-* primitive registered, is the predicate body LIVE (runtime-enforcing), DORMANT-pending (`NotImplementedError`), PARTIAL (some branches live, some dormant), or MISSING (registered in a §-blueprint or `__all__` but no module on disk)?**

Universal evidence: predicate body inspection + test-file existence + AST-lint coverage + lock_history rows that introduced the primitive.

Universal failure mode: claim mismatch — a §-blueprint / CLAUDE.md / customer-facing doc says the family is enforced but the bodies are dormant; or the opposite (body is live but no docs say so, so it's invisible to next reader).

Per-family probes:

#### B.1 — F-CLASS-* (Classification + posture routing)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Are all sixteen F-CLASS-* primitives (per architecture v7.0.10 §5.1 + v7.0.10 expansion) registered with LIVE predicate bodies, AST-lint coverage, and test coverage?
- **Evidence.** `ls pipeline/logician/gates/f_class_*.py`; cross-check against architecture v7.0.10 / v7.0.12 enumeration; `tests/logician/gates/test_f_class_*`.
- **Failure mode.** F-CLASS-COVERAGE-INCOMPLETE META-gate doesn't fire when a required module is absent (the META-gate's whole job). Posture-mid-cycle change not fail-closed. Heavy-Judge flag leaks into a cloud payload. Slot-ID non-opaque regex `\[SLOT_[^\]]*\]` doesn't catch the new variant.

#### B.2 — F-CARDS-* + F-CIC-CLC-* (Card system)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Cards lifecycle claims `runtime_load_status: loaded` on 14 YAMLs. Does the loader (`pipeline/cards/loader.py`) actually load? Do F-CARDS-* gates enforce or raise `NotImplementedError`?
- **Evidence.** `cat pipeline/cards/loader.py` + `grep -rn "NotImplementedError" pipeline/logician/gates/f_cards_*.py pipeline/logician/gates/f_cic_clc_*.py pipeline/cards/loader.py pipeline/cards/validators.py`.
- **Failure mode.** Lifecycle field flips to `loaded` but loader and validators are stubs (this is the load-bearing claim-vs-runtime gap flagged in the 5/16 Tandem QA/QC audit + Codex current_state_assessment). The Card-coupling-extension F-CARDS-COUPLING-VIOLATION-EXTENSION gate is critical — verify it fail-closes against any of the seven CIC-side or six CLC-side forbidden coupling field names (per CLAUDE.md "Do not encode any CIC→CLC subset binding").

#### B.3 — F-DIALECT-*

Mode: SINGLE-SWEEP.

- **Acceptance question.** Post the 2026-05-16T18:45:00Z predicate-realization session: are F-DIALECT-POLITICAL-AXIS-LEAK (order 6.55) + F-DIALECT-MIGRATION-INCOMPLETE (order 6.56) bodies LIVE? Is the AST-lint `R-NO-POLITICAL-AXIS-LITERAL` registered against the three target globs (cards / types / logician-gates)?
- **Evidence.** `pipeline/logician/gates/f_dialect_*.py` + `pipeline/linting/r_no_political_axis_literal.py` + `tests/logician/gates/test_f_dialect_*` + `tests/linting/test_r_no_political_axis_literal.py`.
- **Failure mode.** Predicate body raises `NotImplementedError`; AST-lint rule registered but glob doesn't match; political-axis literal slips through because token-based matcher misses a substring variant.

#### B.4 — F-REPORT-*

Mode: PARALLEL-DISPATCH-IF-SINGLE-AUDITOR (substantial surface).

- **Acceptance question.** Is the §14 Report Generator track gated by `F-PIPE-TRACK-NOT-SHIPPABLE` at v0.1 (forward-compat refusal)? Are the three Slice-3 AST-lint rules registered? Is `finalize_operator_signed_report` the SOLE auto-finalize site?
- **Evidence.** `pipeline/orchestrator/tracks/report_mode.py`; `R-REPORT-NO-AUTO-FINALIZE` / `R-REPORT-VAULT-INTENT-REQUIRED` / `R-REPORT-DECIMAL-MANDATE`; `tests/tracks/report_mode/test_end_to_end.py`.
- **Failure mode.** Track shippable in v0.1 when spec says v0.2; auto-finalize path outside the whitelist; Decimal mandate breach (float coercion / float-literal arithmetic / float-literal comparison / `Decimal(float_literal)`).

#### B.5 — F-PACKET-* (Reflection Packet artifact)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Post the 2026-05-15T19:14:53Z first-wave LOCK: 19 F-PACKET-* signatures registered; 1 LIVE (META-gate `F-PACKET-COVERAGE-INCOMPLETE`); 18 NotImplementedError. Is the dormant-vs-live distinction correctly maintained? Is the sub-kind module authored but NOT in `SUB_KIND_REGISTRY`?
- **Evidence.** `pipeline/logician/gates/f_packet_*.py` × 19 expected; `pipeline/vault/sub_kinds/reflection_packets.py` + `pipeline/vault/sub_kinds/registry.py` (verify `reflection_packet` is NOT in the active registry at v0.1).
- **Failure mode.** Sub-kind silently registered at v0.1 (would activate Reflection Packet writes before v0.2 first wave); META-gate body absent or wrong; cross-family-import ban (F-PACKET-* ↔ F-REFLECTION-* ↔ F-ARCHIVIST-* ↔ F-WPFA-*) not AST-lint-enforced.

#### B.6 — F-REFLECTION-* + F-ARCHIVIST-*

Mode: SINGLE-SWEEP.

- **Acceptance question.** Are the producer (F-REFLECTION-*) and substrate (F-ARCHIVIST-*) families orthogonal to F-PACKET-* (artifact)? Does the AST-lint cross-family-import ban fire on any module that imports across these families?
- **Evidence.** `pipeline/logician/gates/f_reflection_*.py` + `pipeline/logician/gates/f_archivist_*.py` + `pipeline/linting/r_*_cross_family_*.py` (if exists).
- **Failure mode.** Cross-family import allowed in production code; producer/substrate/artifact families collapsed back into one.

#### B.7 — F-WPFA-*

Mode: SINGLE-SWEEP.

- **Acceptance question.** Are all 12 F-WPFA-* predicates LIVE at LOCK (the first §4 amendment to ship LIVE bodies, per §17 v1 LOCK row 205)? Does the Decimal-mandate-energy AST-lint rule (`R-WPFA-DECIMAL-MANDATE-ENERGY`) fire on float arithmetic in energy quantities?
- **Evidence.** `pipeline/logician/gates/f_wpfa_*.py` × 12; `pipeline/linting/r_wpfa_*.py`; `pipeline/vault/sub_kinds/cycle_receipt.py` (or similar); `vault_shared/wpfa/coefficient_registry/` (verify signed asset present + publisher pubkey pin).
- **Failure mode.** Buyer-facing PDF emission without operator Ed25519 attestation (M13 NOT permitted); CycleReceipt path violates Law-3 isolation; coefficient registry signature does not verify against pinned publisher pubkey.

#### B.8 — F-FG-* (Funding Goal)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Are F-FG-* predicates LIVE per the §2 v7.5 / §3 v6 / §4 v2.x.4 funding-goal compound LOCK (rows 211–214, 2026-05-11)?
- **Evidence.** `pipeline/logician/gates/f_fg_*.py` + funding-goal blueprint sections + tests.
- **Failure mode.** Predicate bodies dormant; goal-detection logic differs from §3 v6 specification.

#### B.9 — F-PIPE-* (Pipeline / track registry)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Is the track registry (`pipeline/orchestrator/tracks/`) correctly enforcing the v0.1-vs-v0.2 boundary via `F-PIPE-TRACK-NOT-SHIPPABLE` at runtime? At v0.1: `submission_mode` ACTIVE · `eval_mode` ACTIVE · `report_mode` REFUSES.
- **Evidence.** `pipeline/orchestrator/tracks/track_registry.py` (or similar); `tests/tracks/`.
- **Failure mode.** A track marked `shippable_in: v0.1` that should be `v0.2`; the dispatcher dispatching a refused track.

#### B.10 — F-AMDT-* (Amendment process)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Are F-AMDT-* gates enforcing the paired-commit Option-B discipline (every architecture/blueprint amendment LOCK requires its §0.5 paired-commit at the same `lock_timestamp_utc`)?
- **Evidence.** `pipeline/logician/gates/f_amdt_*.py` (if exists); cross-check by grouping lock_history rows by `lock_timestamp_utc` and verifying each amendment row has a paired `blueprint-interface-index` sibling.
- **Failure mode.** Amendment LOCK row without paired §0.5 row; paired rows with different timestamps; `parent_amendment_chain` field broken.

#### B.11 — F-GPP-* (Governance Plan Preflight)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Per `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md`: are all 12 F-GPP-* primitives LIVE? Does the deterministic Tier-1 tool (`gpp_det.py`) run cleanly?
- **Evidence.** `pipeline/logician/gates/f_gpp_*.py`; `pipeline/validation/integration_scope_close_2026-04-19/gpp/`.
- **Failure mode.** Test depends on GROQ_API_KEY env var (per Tandem QA/QC pre-existing failure flag); Tier-3 manifest validity check fails; det tool emits drift.

#### B.12 — Cross-family import ban

Mode: SINGLE-SWEEP.

- **Acceptance question.** Does an AST-lint rule enforce that F-PACKET-* / F-REFLECTION-* / F-ARCHIVIST-* / F-WPFA-* / F-FG-* / F-CARDS-* don't cross-import each other's primitives?
- **Evidence.** `pipeline/linting/r_*_cross_family*.py` if exists; otherwise document as MISSING.
- **Failure mode.** Cross-family import exists in production code; refactor accidentally collapses isolation.

---

### C. Council seat contracts

Six seats per CLAUDE.md "The Council (Six Seats)"; five support agents per "Support Agents". Each is an audit surface.

#### C.1 — Scout

Mode: SINGLE-SWEEP.

- **Acceptance question.** Two-stage discovery (DISCOVER over six parallel channel families A–F; VERIFY fetches live synopsis; REVIEW is the human gate). Does the runtime actually run six parallel channels, or has the implementation collapsed to a subset?
- **Evidence.** `pipeline/orchestrator/seats/scout/`; `router.yaml` (current Scout binding); `pipeline/seats/scout/channels/` (or similar). Smoke-run `tilth scout discover` (if CLI exists) and verify all six channels fire.
- **Failure mode.** Channels B–F silently absent; VERIFIED_FIT label assigned without live endpoint fetch; sub-channel becomes effective primary when others fail.

#### C.2 — Scribe

Mode: PARALLEL-DISPATCH-IF-SINGLE-AUDITOR.

- **Acceptance question.** Under Split-Context Hybrid posture: does Scribe's scaffold composition route cloud-frontier on RFA + section structure + dialect keywords only, while substance composition routes local? No opaque-slot rendering round-trip per v7.0.10 §2.
- **Evidence.** `pipeline/orchestrator/seats/scribe/` + `pipeline/seats/scribe/provider_anthropic.py`; KGIE preflight + SMART outcomes + overlooked-expenses checklist active in the prompt scaffolding.
- **Failure mode.** Sanitized / opaque-slot-token pattern resurfaces; `[SLOT_<anything>]` emitted into cloud-routed prompts (would trigger `F-CLASS-SLOT-ID-NON-OPAQUE` + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED`); substance leaks into the scaffold-cloud path.

#### C.3 — Editor

Mode: SINGLE-SWEEP.

- **Acceptance question.** Does Editor enforce cross-family rigor (does NOT share provider family with Scribe per `router.yaml`)? Does it offer 2-3 concrete replacement options per jargon issue?
- **Evidence.** `router.yaml` (Scribe + Editor bindings); `pipeline/orchestrator/seats/editor/`.
- **Failure mode.** Same provider family as Scribe (e.g., both Anthropic) — would collapse defense-in-depth.

#### C.4 — Judge

Mode: SINGLE-SWEEP.

- **Acceptance question.** Does Judge cross-check the funder's own rubric first, then related rubrics? Does the heavy-Judge swap actually load a 200B-class local model on federal long-form / large award / operator-flagged grants? Is the model pre-loaded on the Golden Quill appliance (no network fetch per `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD`)?
- **Evidence.** `pipeline/orchestrator/seats/judge/` + `pipeline/seats/judge/provider_google.py`; `router.yaml`; verify Judge BLUEPRINT_DEPS hash matches `pipeline/blueprint/v0.1/section_07_scribe.md` (per the Tandem QA/QC flagged pre-existing failure — stale `e793055d257ae56b` vs. live `b33146a4c13a3013`).
- **Failure mode.** Heavy-Judge swap silently downloads; BLUEPRINT_DEPS hash drift (open finding from Tandem QA/QC); cross-family rule violation with Scribe and Red Team.

#### C.5 — Red Team

Mode: SINGLE-SWEEP.

- **Acceptance question.** Does Red Team fire on every draft? Cross-family rigor against Scribe and Judge — never shares provider family with either. Disagreement of ≥10 points between Judge and Red Team triggers a council split (Law 4 tie-breaker; boundary-inclusive at threshold per §10.6).
- **Evidence.** `pipeline/orchestrator/seats/red_team/` + `pipeline/seats/red_team/provider_groq.py`; `router.yaml` for the three-family separation.
- **Failure mode.** Red Team shares family with Scribe or Judge; council-split threshold not enforced; Red Team Groq dual-path resurfaces (collapsed at CC-007 §4 v2.x.6).

#### C.6 — Logician

Mode: SINGLE-SWEEP.

- **Acceptance question.** Deterministic, fail-closed, zero-token. All Five Laws enforced as PRE/POST/COMMIT gates. Cannot be overridden by any prompt, skill, or model.
- **Evidence.** `pipeline/logician/` (Cedar engine + gates); `pipeline/vault/policies/*.cedar`; `pipeline/linting/`; verify no LLM-router invocation paths inside Logician.
- **Failure mode.** Logician calls an LLM (would break zero-token + cross-family-isolation); a gate raises a soft warning instead of fail-closing; Five-Law enforcement missing on one law.

#### C.7 — Intake (support agent v0.1)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Three modes covered: BULK_INGEST (white-glove onboarding bulk doc absorption), INCREMENTAL_INGEST (between-cycle additions; new facts default to `confidential`), AWARD_INGEST (proposal_commitments.yaml extraction at award acceptance). Always-local. KFR provenance with verbatim-quote-with-page.
- **Evidence.** `pipeline/orchestrator/seats/intake/` + `pipeline/cli/tilth_intake.py`; verify `F-CLASS-NEW-FACT-UNCLASSIFIED` defaults to `confidential` pending operator re-classification.
- **Failure mode.** Logfire import before env-bootstrap (R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV); BULK / INCREMENTAL / AWARD modes collapsed; new-fact default not `confidential`; KFR provenance accepts non-verbatim paraphrase.

#### C.8 — Uploader (support agent v0.1)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Four portal adapters covered (Grants.gov Workspace + SAM.gov + Common Grant Application + copy-paste fallback). Prepare-and-stage discipline only — operator clicks final submit. Attachments deferred to v1.1.
- **Evidence.** `pipeline/orchestrator/seats/uploader/`; `pipeline/cli/tilth_uploader.py`.
- **Failure mode.** Auto-submit path exists; Foundant / Submittable / Fluxx adapters silently active at v0.1 (Path-b scope per §12 v1 LOCK).

#### C.9 — Data Collector + Report Generator (v0.2 SPEC LOCKED, NOT shipped at v0.1)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Both are spec-locked but not shipped. Track-registry refuses `report_mode` at runtime via `F-PIPE-TRACK-NOT-SHIPPABLE`. Data Collector's five channels (email + SMS + voice + Telegram + WhatsApp) are NOT live.
- **Evidence.** `pipeline/orchestrator/tracks/report_mode.py` + `pipeline/orchestrator/seats/report_generator/`; `tests/tracks/report_mode/skeleton_tests.py`.
- **Failure mode.** Track flipped to `shippable_in: v0.1` prematurely; Data Collector calls live (would violate v0.1 scope freeze + CAN-SPAM/TCPA compliance).

#### C.10 — Archivist (v1.x SPEC) + Reflection sub-mode (v0.1 hook DORMANT)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Reflection sub-mode hook at v0.1 is DORMANT per OQ-2(a). Sub-kind authored at `pipeline/vault/sub_kinds/reflection_packets.py` but NOT in SUB_KIND_REGISTRY. 18 F-PACKET-* gates raise `NotImplementedError`; only `F-PACKET-COVERAGE-INCOMPLETE` META is LIVE.
- **Evidence.** `pipeline/vault/sub_kinds/reflection_packets.py` + `pipeline/vault/sub_kinds/registry.py` (verify `reflection_packet` NOT in SUB_KIND_REGISTRY).
- **Failure mode.** Silently registered; predicate body activation without §16 v1.1 SPEC LOCK paired-commit.

---

### D. Posture / routing enforcement

Three customer-facing postures per architecture v7.0.10 LOCKED 2026-05-11 row 215. Each is a routing-decision audit surface.

#### D.1 — Frontier-Eligible posture

Mode: SINGLE-SWEEP.

- **Acceptance question.** Public/shareable fields route cloud; confidential/operator_flagged remain local; class-indeterminate fails closed to LOCAL default per `F-CLASS-ROUTING-INDETERMINATE`.
- **Evidence.** `pipeline/orchestrator/router.py` + `pipeline/orchestrator/deployment_posture.py`; `tests/orchestrator/test_router_classification_boundary.py` (in v0.1 smoke suite).
- **Failure mode.** Confidential field routed cloud; operator override silently active without per-grant SP0; class-indeterminate routes cloud.

#### D.2 — Split-Context Hybrid posture

Mode: SINGLE-SWEEP.

- **Acceptance question.** Cloud routing limited to closed-set allow-list at `orgs/<slug>/vault/classification/split_context_allowlist.yaml` (`F-CLASS-SPLIT-CONTEXT-ALLOWLIST` PRE-gate). Applicant-fact PRE-scan fires before any cloud dispatch (`F-CLASS-SPLIT-CONTEXT-LEAK`).
- **Evidence.** `pipeline/logician/gates/f_class_split_context_*.py`; per-org allow-list scaffold at `orgs/_TEMPLATE/vault/classification/split_context_allowlist.yaml`.
- **Failure mode.** Allow-list not enforced (any field routes cloud); applicant-fact PRE-scan absent; allow-list file unsigned.

#### D.3 — Local-Only / Sovereign posture

Mode: SINGLE-SWEEP.

- **Acceptance question.** All drafting / review / routing / evidence use remain local. Performance-dependent / under-validation notice on customer-facing materials. `local_only_validated: bool` field in deployment manifest defaults `false`, write-protected, flips only on SN-LLC quarterly validation outcome signature.
- **Evidence.** `pipeline/orchestrator/deployment_posture.py`; deployment manifest schema; verify the under-validation notice surfaces in `docs/v0_1_beta_deployment_runbook.md` + customer-facing pages.
- **Failure mode.** `local_only_validated: true` claimed without SN-LLC quarterly signature; cloud route silently engaged on a Local-Only posture.

#### D.4 — Posture mid-cycle change refusal

Mode: SINGLE-SWEEP.

- **Acceptance question.** `F-CLASS-POSTURE-MID-CYCLE-CHANGE` fail-closes any attempt to change posture mid-cycle. Re-selection only via `tilth posture select` CLI between cycles.
- **Evidence.** `pipeline/logician/gates/f_class_posture_mid_cycle_change.py` + `pipeline/cli/tilth_posture.py` (or similar).
- **Failure mode.** Mid-cycle posture flip succeeds; CLI accepts a flip without cycle-boundary check.

#### D.5 — Heavy-Judge swap routing

Mode: SINGLE-SWEEP.

- **Acceptance question.** Federal long-form / large award / operator-flagged → Heavy-Judge swap (200B-class local model loaded for cycle). Pre-loaded at white-glove. No network fetch.
- **Evidence.** `router.yaml` (heavy-Judge binding); `pipeline/logician/gates/f_class_heavy_judge_cloud_download.py`; alternative-update-channel ban; boot-time manifest verification.
- **Failure mode.** Heavy-Judge swap triggers a network fetch (would fire `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD`); flag leaks into cloud payload (would fire `F-CLASS-HIGH-STAKES-FLAG-LEAK`).

---

### E. Memory layer

#### E.1 — Institutional memory (`lessons.md` + `lessons.json`)

Mode: SINGLE-SWEEP.

- **Acceptance question.** `lessons.md` is human-readable + canonical; `pipeline/institutional_memory/lessons.json` is the machine-readable mirror with frequency weights. Both updated on repeated failure pattern emergence.
- **Evidence.** `lessons.md`; `pipeline/institutional_memory/lessons.json`; verify the L-001..L-022 lessons surface in both (or document divergence).
- **Failure mode.** Lessons drift between files; high-frequency + high-severity lesson not promoted to mandatory pre-check; new lesson landed in .md but not .json.

#### E.2 — Workspace MEMORY.md + auto-consolidation

Mode: SINGLE-SWEEP.

- **Acceptance question.** Post 2026-05-15 consolidation: MEMORY.md 15 active + 79 archived to `_archive_2026-05-15.md`. `pipeline/memory/consolidate_index.py` + `pipeline/cli/tilth_memory.py` LANDED. Auto-fire at session start is DEFERRED to v1.x (operator-invoked at v0.1 Beta).
- **Evidence.** `MEMORY.md` size; `_archive_2026-05-15.md` presence; `pipeline/memory/consolidate_index.py`; `tests/memory/test_consolidate_index.py`.
- **Failure mode.** Auto-consolidation silently wired to a `schedule` skill at v0.1 (would activate before spec); pointer-line stacks on re-consolidation; archive collision uniquifier absent.

#### E.3 — `tilth memory query` CLI

Mode: SINGLE-SWEEP.

- **Acceptance question.** BM25 Okapi (k1=1.5, b=0.75) over 13 registers (9 workspace + 4 per-org). Law-3 isolation at adapter boundary. 49-test suite green.
- **Evidence.** `pipeline/memory/unified_query.py` + `pipeline/cli/tilth_memory_query.py` + `tests/cli/test_tilth_memory_query.py`.
- **Failure mode.** Cross-org enumerate succeeds in one query (would violate Law 3); reserved-slug `_TEMPLATE` accepted; path-traversal slug accepted.

#### E.4 — Per-org memory + KFR

Mode: PARALLEL-DISPATCH (per-org isolation).

- **Acceptance question.** Per-org memory at `orgs/<slug>/vault/`. KFR (Key Facts Register) with verbatim-quote-with-page provenance. Match Database. Classification register. Reflection Packets (DORMANT at v0.1).
- **Evidence.** `orgs/_TEMPLATE/vault/`; per-org KFR schema; `pipeline/cli/tilth_kfr.py` (or similar).
- **Failure mode.** Cross-org read in one session; KFR fact accepted without verbatim quote; KFR expiry not tracked.

#### E.5 — Funder Intelligence Database (FID) scaffold

Mode: SINGLE-SWEEP. See §Q for full FID audit.

#### E.6 — Reflection Packet (v0.2 first-wave horizon)

Mode: SINGLE-SWEEP. Cross-references B.5 (F-PACKET-* family).

- **Acceptance question.** Schema authored, registry-dormant, gates dormant-pending. v0.2 first-wave handoff at `pipeline/handoffs/ws_reflection_packet_v0_2_first_wave_handoff_2026-05-15.md` pre-staged.
- **Evidence.** `pipeline/vault/sub_kinds/reflection_packets.py` + handoff doc.
- **Failure mode.** Sub-kind silently registered; producer-binding (§16 v1.1) activated before v0.2 LOCK; cross-family naming reconciliation breaks (F-PACKET-* / F-REFLECTION-* / F-WPFA-* / F-ARCHIVIST-*).

---

### F. Cards (§18) — schema, lifecycle, signing, loader

#### F.1 — CIC + CLC schemas

Mode: SINGLE-SWEEP.

- **Acceptance question.** 14 card YAMLs (6 CIC + 8 CLC). All schema-valid against `pipeline/cards/_schema/card_{cic,clc}.schema.json` (Draft 2020-12). Per-Wave LOCK ceremonies preserved.
- **Evidence.** `pipeline/cards/CIC/*.yaml` (6 files) + `pipeline/cards/CLC/*.yaml` (8 files); `python3 -m pipeline.cards.validators` (if CLI exists) or direct jsonschema run.
- **Failure mode.** Schema validation fails on one or more cards; YAML drift from latest schema-amendment shape.

#### F.2 — CIC × CLC orthogonality (coupling ban)

Mode: SINGLE-SWEEP.

- **Acceptance question.** No card carries any of the seven CIC-side or six CLC-side forbidden coupling fields. AST-lint `R-CARDS-NO-COUPLING-FIELD` enforces.
- **Evidence.** `pipeline/linting/r_cards_no_coupling_field.py`; `pipeline/logician/gates/f_cards_coupling_violation_extension.py`; `FORBIDDEN_FIELD_REGISTRY` enumeration.
- **Failure mode.** Card carries `eligible_clc_subset` / `clc_allowlist` / `clc_denylist` / `clc_ranking_preferences` / `clc_win_rate` / `common_clc_patterns_observed` / `preferred_clcs` (CIC) or `eligible_cic_subset` / `cic_allowlist` / `cic_denylist` / `preferred_cics` / `cic_win_rate` / `cic_ranking_preferences` (CLC).

#### F.3 — Lifecycle vs runtime

Mode: SINGLE-SWEEP. **HIGH PRIORITY** — this is the claim-vs-runtime gap flagged at 2026-05-16.

- **Acceptance question.** Lifecycle fields claim `signature_status: signed` + `runtime_load_status: loaded`. Does the loader (`pipeline/cards/loader.py`) actually load? Do the F-CARDS-* gates enforce?
- **Evidence.** `cat pipeline/cards/loader.py` + `cat pipeline/cards/validators.py` + `grep -n NotImplementedError pipeline/logician/gates/f_cards_*.py`.
- **Failure mode.** Lifecycle says loaded but loader raises NotImplementedError. Customer-facing claim that "cards are loaded" is overclaim. Mitigation: either rename lifecycle field to `lock_status` (governance-only) or land loader bodies before any Gate-2 customer claim.

#### F.4 — Card signing chain

Mode: SINGLE-SWEEP. Cross-references H (Ed25519 chain).

- **Acceptance question.** Each LOCKed card carries Ed25519 signature against operator-pinned publisher pubkey. Canonical-JSON via `json.dumps(parsed, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode("utf-8")`. Signature prefix in lock_history row.
- **Evidence.** `vault_shared/cards/publisher_pubkey.pem` (or similar); lock_history rows 226–228 (Wave 1) + 250–262 (Wave 2); per-card signature prefix audit.
- **Failure mode.** Signature does not verify; canonical-JSON producer drifts (whitespace / ordering / encoding); publisher pubkey not pinned at white-glove.

#### F.5 — Card-level admin_risk_term_register

Mode: SINGLE-SWEEP.

- **Acceptance question.** Each card carries `admin_risk_term_register` with severity tiers + substitution_candidates + reviewer_context. `approval_required: true` default per OQ-5. Reconciled with workspace-wide `pipeline/institutional_memory/admin_risk_register.yaml`.
- **Evidence.** Per-card `admin_risk_term_register` block; workspace register; `pipeline/institutional_memory/admin_risk_register_audit_decisions.md` (91 scaffolded term rows pending operator content audit).
- **Failure mode.** Card-level register diverges from workspace register without explicit reconciliation; substitution_candidates silently applied without operator approval (Law 4 violation).

#### F.6 — Vocab-scrub supersession discipline

Mode: SINGLE-SWEEP.

- **Acceptance question.** Vocab-scrub LOCK ceremony 2026-05-16T14:30:00Z retired "cartridge" workspace-wide. Forward surfaces use card-only vocabulary. Historical audit trails (`lock_class=card_cartridge` rows; `pipeline.cards.CLC.<slug>` modules pre-supersession) preserved as audit-only continuity.
- **Evidence.** `grep -rn "cartridge" pipeline/ docs/ CLAUDE.md SOUL.md AGENTS.md README.md` (expect zero in forward surfaces).
- **Failure mode.** "Cartridge" survives in a forward surface (recurrence — third slip recurrence is what triggered the supersession ceremony); historical lock_history row vocabulary "corrected" (would break audit-trail integrity).

---

### G. LOCK ledger integrity (`lock_history.v1.jsonl`)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Every row in `pipeline/engineering/lock_history.v1.jsonl` (264 rows at 2026-05-16) is:
  - Schema-valid (15 required fields).
  - Anchored to an on-disk amendment file (or has an explicit `lock_class` exempting it: `memory_consolidation`, `cards_repin_noop`, `vocab_scrub_supersession`, `card_cartridge`).
  - Sibling-paired (every architecture/blueprint amendment has a `blueprint-interface-index` row at the same `lock_timestamp_utc`).
  - Parent-chain-coherent (`parent_amendment_chain` references resolve to prior rows).
- **Evidence.** `wc -l pipeline/engineering/lock_history.v1.jsonl`; `jq '.' pipeline/engineering/lock_history.v1.jsonl | python3 -c "..."` (schema validation); pairing check by grouping on `lock_timestamp_utc`.
- **Failure mode.** Orphan row (no amendment file). Phantom amendment file (no row). Paired-commit timestamp mismatch. `parent_amendment_chain` reference to nonexistent prior row. Row appended without `lock_class`. Vocab-scrub or NO-OP row that should have been a real LOCK. **Duplicate `row` numbers.** *Seed finding (2026-05-16):* `jq -r '.row' pipeline/engineering/lock_history.v1.jsonl | sort -n | uniq -c | awk '$1 > 1'` surfaces rows **234** and **235** each appearing twice — once at `2026-05-16T14:00:00Z` (apolitical-dialect compound) and once at `2026-05-16T16:30:00Z` (§4 v2.x.6 router-dedup amendment). 198 rows additionally carry `row: null` (legacy schema, pre-`row`-field rollout). Audit must determine whether the duplication is benign (separate sub-LOCKs sharing a row number by intent) or a real ledger-integrity defect, and whether the null-row rows can be back-filled or must remain audit-only.

---

### H. Ed25519 signing chain

Mode: SINGLE-SWEEP.

Tilth has multiple signing roles, each with its own publisher pubkey pinned at white-glove.

- **Acceptance question.** Each signing role has:
  - A pinned publisher pubkey (operator-pinned at white-glove).
  - A canonical signing payload (canonical-JSON, byte-stable).
  - A verification gate that fail-closes on signature invalid.
  - Pubkey separation-of-concerns (cards-publisher ≠ FID-publisher ≠ Coefficient-Registry-publisher ≠ router-template-publisher ≠ operator).
- **Evidence per role.**
  - **SN-LLC publisher pubkey** (Coefficient Registry + WPFA + Heavy-Judge router-template) — pinned at deployment manifest level.
  - **Cards publisher pubkey** — pinned for Wave-1 + Wave-2 LOCK ceremony signatures (`pipeline/cards/PUBLISHER.pubkey` or similar).
  - **FID publisher pubkey** — separation-of-concerns from cards-publisher per FID Phase 1 dispatch plan §0 #11.5 (NOT YET GENERATED at 2026-05-16).
  - **Router-template publisher pubkey** — per architecture v7.0.7 §6.1 byte-for-byte signing.
  - **Operator Ed25519 attestation** — per WPFA buyer-facing PDF emission (`F-WPFA-OPERATOR-SIGNATURE-MISSING`) + Classification Register sign-off (`F-CLASS-REGISTER-UNSIGNED` / `F-CLASS-REGISTER-SIGNATURE-INVALID`) + Reflection Packet decision-observed event + admin_risk audit decisions (`pipeline/scripts/audit_term_signer.py`).
  - **Per-grant SP0 signature chain** — per `F-CLASS-ROUTING-INDETERMINATE` operator overrides.
- **Failure mode.** Pubkey reuse across roles (e.g., cards-publisher used for FID — separation broken). Operator Ed25519 attestation skipped on buyer-facing PDF. Router-template update applied without signature verification (`F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID`). Classification register unsigned but routing proceeds. Cards Wave 2 LOCK ceremony signatures don't verify against pinned pubkey.

---

### I. Five Operating Laws — enforcement

Mode: SINGLE-SWEEP per law.

- **Universal acceptance question.** Is each Law enforced as a PRE/POST/COMMIT Logician gate (deterministic, fail-closed, zero-token)? Backed by Cedar policy + AST-lint where applicable?
- **Universal evidence.** `pipeline/vault/policies/*.cedar`; `pipeline/logician/gates/`; `pipeline/linting/`.

#### I.1 — Law 1 (RFA is the source of truth)

- **Probe.** Every Scribe-generated claim traces to RFA text or PROJECT_CONTEXT. Logician PRE-gate refuses claims without provenance citation.
- **Failure mode.** Claim inserted from training data / generic boilerplate / paraphrase of non-RFA source.

#### I.2 — Law 2 (No boundary drift)

- **Probe.** Scribe stays inside the RFA's defined scope. No silent scope expansion.
- **Failure mode.** Section drift adds work units not in the RFA; Scribe expands eligible activities.

#### I.3 — Law 3 (Org Isolation)

- **Probe.** One PROJECT_CONTEXT.md per session. Never cross-reference data between orgs. Adapter-boundary refusal on cross-org enumerate.
- **Failure mode.** Cross-org KFR read; per-org adapter accepts `None` org or `_TEMPLATE`; `tilth memory query --org X` returns content from org Y.

#### I.4 — Law 4 (Apolitical sector language + admin-risk term scanning)

- **Probe.** Two axes: (a) funder dialect code-switching (conservative/centrist/progressive/soul_fire — though the four-axis enum is retired post-v7.0.12; current state is CLC-keyed register state), (b) admin-risk register with severity tiers. Never silently rewrite; applicant approves each substitution.
- **Failure mode.** Silent rewrite of flagged term; political-axis literal in code (would fire `R-NO-POLITICAL-AXIS-LITERAL`); admin-risk register entry silently applied without `approval_required: true` honored.

#### I.5 — Law 5 (Applicant brings substance)

- **Probe.** No fabrication of credentials, data, partnerships. Shape existing substance into funder-ready form.
- **Failure mode.** Scribe inserts a credential / partnership / metric absent from KFR or RFA; Editor smooths fabricated claim into plausible prose.

---

### J. Cross-family bridge pattern (L-005)

Mode: SINGLE-SWEEP.

- **Acceptance question.** Two-audit cycle (no silent third round per L-005). Cross-family rigor: Editor / Judge / Red Team never share provider family with Scribe or with each other (verify against `router.yaml` current bindings). Bridge templates at `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`.
- **Evidence.** `router.yaml` provider-family enumeration; `pipeline/validation/v7_0_5_thesis_2026-05-09/`; live dispatch via `mcp__Control_your_Mac__osascript` → `openclaw infer model run --gateway`.
- **Failure mode.** Editor + Scribe same provider family; silent third round (L-005 violation); Section E single-Claude carve-out invoked without a logged dispatch failure (per CLAUDE.md "Section E carve-out — invocation discipline").

---

### K. Beta submission workflow end-to-end

Mode: SINGLE-SWEEP (synthetic data only — Law 3 applies; do NOT use a real org's PROJECT_CONTEXT).

- **Acceptance question.** Walk the full v0.1 submission_mode workflow with synthetic inputs:
  1. Customer drops mixed documents → Intake BULK_INGEST runs → KFR populated with verbatim-quote-with-page provenance.
  2. Classification Review orchestrator runs → register signed at operator Ed25519 → posture selected → posture sign-off.
  3. Scout DISCOVER over six channels → VERIFY → REVIEW gate.
  4. Scribe drafts under selected posture → routing decision per-call per `F-CLASS-ROUTING-INDETERMINATE` default LOCAL.
  5. Editor / Judge / Red Team cross-family review.
  6. Logician PRE/POST gates on each seat call.
  7. Uploader prepare-and-stage on portal adapter.
  8. Operator clicks final submit outside the system.
  9. AWARD_INGEST or cycle close → CycleReceipt typed Pydantic artifact at `orgs/<slug>/vault/operational/cycle_receipts/<cycle_id>.json` (WPFA).
  10. Reflection Packet emission — DORMANT at v0.1.
- **Evidence per step.** CLI presence + test presence + audit-event presence.
- **Failure mode.** Step skipped silently. Operator-staged submit becomes auto-submit. CycleReceipt path violates Law 3. Reflection Packet activates before v0.2 first wave.

---

### L. Planning / blueprint / architecture / code separation

Mode: SINGLE-SWEEP.

- **Acceptance question.** Each tier carries its proper authority:
  - `pipeline/planning/` — operator-facing planning surface (not blueprint; not Thesis-reviewed).
  - `pipeline/blueprint/v0.1/` — §-numbered LOCKed contracts (Thesis-reviewed, paired-commit'd).
  - `pipeline/architecture/v0.1/` — top-level architecture LOCK + v7.0.x amendments.
  - Runtime: `pipeline/<seat|orchestrator|logician|vault|cards|memory|cli>/`.
  - Validation trails: `pipeline/validation/<round>/`.
- **Evidence.** `ls pipeline/{planning,blueprint/v0.1,architecture/v0.1}`; cross-check whether any planning doc pre-binds runtime behavior without a §-blueprint paired-commit.
- **Failure mode.** Planning doc → runtime code with no §-blueprint binding. Specifically watch FID Phase 1 (`pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` + `pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md`) for re-litigation when FID grows into a §-numbered surface.

---

### M. Workspace discipline files

Mode: SINGLE-SWEEP.

- **Acceptance question.** Each discipline file is coherent and load-bearing:
  - `CLAUDE.md` — Cowork-specific supplement (50KB at 2026-05-16). Pins canonical naming chain (Golden Quill / Tilth / Cultivator / Sovereign Node), Five Operating Laws, Council, the three deployment postures.
  - `AGENTS.md` — wake-up sequence + cross-family bridge pattern.
  - `SOUL.md` — workspace-wide identity.
  - `USER.md` — operator profile.
  - `router.yaml` — model bindings (single source of truth).
  - `lessons.md` — canonical institutional memory (frequency-weighted in `lessons.json` mirror).
  - `MEMORY.md` — workspace memory index (post-consolidation: 15 active + 79 archived).
  - `pipeline/SESSION_BOOTSTRAP.md` — new-session orientation pointer.
- **Evidence.** Each file present + dated header + version-coherent with the rest.
- **Failure mode.** CLAUDE.md still cites "Sanitized" / opaque-slot-token (would mean post-v7.0.10 retirement not applied). `router.yaml` carries a hardcoded provider that contradicts AGENTS.md cross-family rigor. SOUL.md references retired vocabulary ("cartridge").

---

### N. Pinned Python interpreter

Mode: SINGLE-SWEEP.

- **Acceptance question.** `.venv/bin/python3` is ≥3.14 (per `pyproject.toml >=3.11` floor + Python 3.10+ `@dataclass(frozen=True, kw_only=True)` requirement). `scripts/run_tests.sh` enforces. System `python3` on macOS (3.9) fails collection.
- **Evidence.** `cat scripts/run_tests.sh`; `cat pyproject.toml`; `python3 --version` (host); `.venv/bin/python3 --version`.
- **Failure mode.** An auditor or agent runs `python3 -m pytest` (system) and reports the 8 collection errors as test failures. CI matrix accepts 3.9. `pyproject.toml` Python floor lowered.

---

### O. GitHub / CI infrastructure

Mode: SINGLE-SWEEP.

- **Acceptance question.** Canonical repo `HyphaeNated/GoldenQuill` (private). Initial commit `d3bc8b1` 2026-05-15. PR #3 (`ci: land PR2 keepers and CC003 quarantine`) head `2d68a3f` — CI run `25963750751` SUCCESS across four jobs (quality gate × Py3.11/3.12 + wheel smoke × Py3.11/3.12). `.gitignore` excludes `data/`, `__pycache__`, `orgs/`, prior Replit work.
- **Evidence.** `git status`, `git branch -vv`, `git remote -v`, `git log --oneline -n 12`, PR #3 metadata via GitHub connector, `.github/workflows/`, `.gitignore`.
- **Failure mode.** Local branch diverges from origin/main without reconciliation. PR #3 stalls unmerged. `data/` 4.9 GB still untracked-not-ignored. CI matrix matches Py3.9 (would not match `pyproject.toml` floor).

---

### P. Sovereignty / egress

Mode: SINGLE-SWEEP. Critical surface — the load-bearing customer claim.

- **Acceptance question.** Every data egress path is wrapped through `provider_boundary.py` + `outbound_boundary.cedar` + `R-NO-DIRECT-PROVIDER-HTTP` lint. Logfire is disabled-by-default at v0.1 (CC-008). Scout DISCOVER channels A–F are the only authorized external fetches.
- **Evidence.**
  - `pipeline/orchestrator/provider_boundary.py`
  - `pipeline/vault/policies/outbound_boundary.cedar`
  - `pipeline/linting/r_no_direct_provider_http.py`
  - `pipeline/seats/{scribe,judge,red_team}/provider_*.py` (verify wrapped)
  - `pipeline/observability/logfire_bootstrap.py` (verify disable-by-default contract)
  - Grep for direct HTTP: `rg -n 'api\.anthropic\.com|api\.groq\.com|generativelanguage\.googleapis\.com|requests\.|httpx\.|aiohttp|urlopen' pipeline tests scripts docs -g '*.py' -g '*.md'`
- **Failure mode.** Direct provider HTTP slips past the lint (false-negative regex). Seat-local provider module bypasses the shared wrapper. Logfire upload fires by default. Brain/JIT SaaS path activates without `F-BRAIN-*` / `R-BRAIN-*` enforcement (no such gates exist today — DOCUMENT AS GAP for Gate 2).

---

### Q. Funder Intelligence Database (FID) Phase 1 scaffold

Mode: SINGLE-SWEEP.

- **Acceptance question.** Phase 1 active scope = Pillars 1–3 (Depth Charter + corpus assembly + structured extraction). Pillar 4 DORMANT pending operator grant-drafting reactivation. Anchor start 2026-05-18. FID publisher key separation-of-concerns from cards-publisher. First exemplar USDA-RD-RBDG-FY26.
- **Evidence.**
  - `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md`
  - `pipeline/handoffs/fid_phase_1_dispatch_plan_2026-05-16.md`
  - `pipeline/handoffs/fid_exemplar_usda_rd_rbdg_fy26_dispatch_2026-05-16.md`
  - `pipeline/funder_intelligence/` (directory scaffold)
  - FID publisher pubkey present (NOT YET GENERATED at 2026-05-16; document state).
- **Failure mode.** FID writes occur before publisher key generation (would invalidate signing chain). Pillar 4 silently activates. Smart-pointer migration plan (Week 8) skipped. FID writes use cards-publisher key (separation broken).

---

### R. Meta-audit

Mode: SINGLE-SWEEP. Run **last** — synthesizes findings across §3.A–Q.

#### R.1 — Architecture vs implementation gap (closing or widening?)

- **Acceptance question.** Over the audit window: is the count of `NotImplementedError` predicate bodies decreasing? Are new amendments landing with LIVE bodies (post-v7.0.12 F-DIALECT-* pattern) or with DORMANT-pending (pre-v0.2 F-PACKET-* pattern)?
- **Evidence.** `grep -rn "NotImplementedError" pipeline/logician/gates/ pipeline/cards/ pipeline/vault/` summarized by family + dated against amendment LOCK dates.
- **Failure mode.** Architecture surface area grows faster than implementation depth. Specifically watch `runtime_load_status: loaded` cards claim vs `pipeline/cards/loader.py` NotImplementedError.

#### R.2 — LOCK ledger ↔ disk reconciliation

- **Acceptance question.** Every lock_history row anchors to a file. Every amendment file has a row. No phantom rows, no orphan files.
- **Evidence.** Per §G integrity audit.
- **Failure mode.** Drift between ledger and disk; especially watch §0.5 amendment-file ↔ paired-commit row pairings.

#### R.3 — Orphaned amendments / phantom references

- **Acceptance question.** Any amendment file (architecture v7.0.x.x or blueprint §N v1.x) not referenced by any other surface? Any reference in CLAUDE.md / SOUL.md / a §-blueprint / a customer-facing doc to a version that doesn't exist on disk?
- **Evidence.** Grep CLAUDE.md / SOUL.md / blueprint sections for version strings; cross-check against `ls pipeline/architecture/v0.1/ pipeline/blueprint/v0.1/`.
- **Failure mode.** Phantom version cited (e.g., "v7.0.13" referenced before v7.0.12 amendment file exists). Orphan amendment file with no inbound reference.

#### R.4 — Customer-facing claims defensible?

- **Acceptance question.** Do README / website / SOUL / customer-handoff docs match runtime reality? Specifically: "local-first," "BYOK only," "cards are loaded," "Reflection Packet learns," "memory auto-consolidation," "Golden Quill survives if FIT Farms disappears."
- **Evidence.** Codex's `current_state_assessment_2026-05-16.md` § Hard-probe Claims; per-claim verdict `DEFENSIBLE` / `OVERCLAIM` / `UNDER_SPECIFIED` / `ARCHIVE_ONLY`.
- **Failure mode.** Any OVERCLAIM that lands in a Paul-readable or customer-readable doc.

#### R.5 — Two-gate vocabulary consistency

- **Acceptance question.** Has "Alpha" as a single label been retired throughout? Are Gate 1 (internal replay with Paul) and Gate 2 (first paid client) used consistently?
- **Evidence.** `grep -rn "Alpha" docs/ README.md` — flag uses of plain "Alpha" that should be Gate-1 or Gate-2.
- **Failure mode.** Label drift; "Alpha" survives in customer-facing doc.

#### R.6 — Governance theater accretion

- **Acceptance question.** Across the audit window, what fraction of LOCK ceremonies are paired-commit NO-OPs, signature-only flips, or vocab-scrubs? Is the rate accelerating?
- **Evidence.** Count by `lock_class` over time. Compare to count of LOCKs that introduce new LIVE predicate bodies or new code paths.
- **Failure mode.** Ratio shifts toward ceremony rows. Auditor overhead grows linearly with surface area while system capability grows sub-linearly.

---

## 4. Weird/OOD probes (L-022)

Run at least one of each, per `03_weird_ood_probes.md`:

1. **Surreal framing.** Explain Tilth as if it were a farm tool — a winnowing fan, a seed library, a soil tester. Note which mechanisms become invisible in the metaphor (sovereignty, BYOK, posture routing, cross-family rigor). Those are the load-bearing mechanisms that resist analogy and need their own vocabulary in customer-facing docs.
2. **Role inversion.** Treat Paul / first-paid-client as the security reviewer and Josh as the vendor. List what would be unacceptable. The "cards loaded" lifecycle claim with `NotImplementedError` loader is the canonical example — would the reviewer accept?
3. **Ambiguous instruction.** Ask "is Tilth Alpha-ready?" and detect label drift. Verify the answer disambiguates Gate 1 vs Gate 2.
4. **Time-pressure spoof.** 90-second due-diligence read of the README + landing page. Identify the first misleading claim a hostile reader would surface. (Likely candidates: "local-first" without the runtime evidence; "Reflection Packet learns" without v0.2 first-wave activation.)
5. **Format spoof.** Reduce Tilth to a one-page invoice addendum. Identify which sovereignty / posture / Law-3 claims cannot fit safely. Those are the claims that need their own document linked from the invoice, not collapsed into it.

---

## 5. Final verdict template

End the audit with `99_final_verdict.md` containing:

```md
# Final Verdict

Audit window: <YYYY-MM-DD HH:MM> to <YYYY-MM-DD HH:MM>
Auditor(s): <names + roles>
Verdict:
- Gate 1 — internal replay with Paul: PASS / PASS_WITH_CAVEATS / FAIL
- Gate 2 — first paid client: PASS / PASS_WITH_CAVEATS / FAIL

## Top 5 P0_BLOCKS_GATE_1 findings

## Top 5 P1_BLOCKS_GATE_2 findings

## Top 5 strengths

## Claims to rewrite before Paul reads

## Claims to rewrite before customer reads

## Architecture/implementation gap — closing or widening?

## LOCK ledger reconciliation — clean or drifted?

## Smallest credible next repair batch

## Evidence gaps (where the audit could not verify)
```

Do not end with general encouragement. The output must be directly actionable.

---

## 6. Single-sweep vs per-surface dispatch

### Single-sweep mode

One auditor. ~6–12h. Walk §3.A → §3.R in order. Cross-references resolved by reading prior sections first. The §0.5 ledger reconciliation (§3.A.19) + the LOCK ledger integrity check (§3.G) + the LIVE/DORMANT gate-family inventory (§3.B.* synthesized in §3.R.1) are the three heavyweight passes; reserve ~3h total for them.

### Per-surface dispatch mode

Multiple sessions / agents. Each §3.x.y is a self-contained task spec. Recommended batching:

- **Batch 1 (parallel, fast):** §3.A.1–A.18 per-section blueprint audits (17 surfaces × ~30min each = ~8.5h sequential, ~30min wall-clock if fully parallel). Bridge dispatch via `mcp__Control_your_Mac__osascript` per AGENTS.md.
- **Batch 2 (parallel):** §3.B.1–B.12 per-family failure-code audits (12 surfaces).
- **Batch 3 (parallel):** §3.C.1–C.10 per-seat audits (10 surfaces).
- **Batch 4 (serial; depends on Batch 1/2/3):** §3.D / §3.E / §3.F / §3.G / §3.H / §3.I / §3.K / §3.L / §3.M / §3.N / §3.O / §3.P / §3.Q.
- **Batch 5 (serial; runs last):** §3.R meta-audit + §4 weird/OOD probes + §5 final verdict.

L-005 cross-family dispatch required for any surface tagged THESIS-REQUIRED (none in this prompt — but if findings escalate to amendments, the amendment LOCK round needs L-005 strict two-cycle).

For sub-agent dispatch, each surface spec in §3.x is self-contained: the agent reads this file, walks to §3.x.y, runs the listed evidence collection, writes the per-surface file under `02_per_surface/`, and hands back to the coordinator. Coordinator synthesizes in §3.R.

---

## 7. Reference index

- Companion reconciliation audit prompt (time-bound, post-surge): `pipeline/handoffs/project_wide_reconciliation_audit_prompt_2026-05-16.md`
- Current-state snapshot (Codex, 2026-05-16): `pipeline/planning/current_state_assessment_2026-05-16.md`
- 48-72h retrospective (Cowork, 2026-05-16): `docs/assessment_2026-05-16_72h_retrospective.md`
- v0.1 clearance authority: `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md`
- Tandem QA/QC remediation pack (CC-001..CC-009): `pipeline/handoffs/tandem_qa_qc_remediation_decisions_2026-05-16.md`
- Two-gate canonical: `memory/project_alpha_label_two_gate_2026-05-16.md` (REFERENCED BY tandem_qa_qc_remediation_decisions_2026-05-16.md BUT NOT ON DISK AT 2026-05-16 — open finding; either write the file or remove the reference)
- L-005 bridge templates: `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`
- AGENTS.md (wake-up sequence + cross-family bridge): `AGENTS.md`
- Identity + product naming chain: `CLAUDE.md` (§"The Product Naming Chain: Golden Quill · Tilth · Cultivator · Sovereign Node")
- Five Operating Laws: `CLAUDE.md` (§"The Five Operating Laws")
- Council seat contracts: `CLAUDE.md` (§"The Council (Six Seats)")
- Three-posture routing canonical spec: `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md`
- Apolitical-dialect amendment: `pipeline/architecture/v0.1/architecture_v7_0_12_apolitical_dialect_amendment.md`
- Cards system: `pipeline/blueprint/v0.1/section_18_card_system.md` (+ v1.1 + v1.2 amendments)
- Pinned interpreter wrapper: `scripts/run_tests.sh`
- v0.1 smoke test bar (339 tests): `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md` §"v0.1 Smoke Test Bar"
