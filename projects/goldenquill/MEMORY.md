# Golden Quill / Tilth — Workspace Memory Index

Workspace-wide pointer to where institutional and agent memory lives. This file is read during the wake-up sequence (per AGENTS.md) after router.yaml and before the active agent's overrides.

## Memory layers

**1. Institutional memory (shared across all agents and all clients)**
- [`lessons.md`](lessons.md) — human-readable, canonical. Repeated failures, validated approaches, post-mortems.
- [`pipeline/institutional_memory/lessons.json`](pipeline/institutional_memory/lessons.json) — machine-readable mirror. Frequency-weighted.

**2. Agent-scoped memory**
- Tilth (grant intelligence agent): [`Sovereign_Node_Handoff/memory/`](Sovereign_Node_Handoff/memory/) — agent-level context, self-analysis files, prior-incident recall.
- Sentinel (QA agent): [`HeartbeatQAfiles/`](HeartbeatQAfiles/) — QA-specific lessons and audit history. **Dormant** since 2026-04-14 (last QA report: `SN-QA-REPORT-2026-04-14-MIGRATION.md`). Canonical memory at folder root; no `memory/` subdirectory. Reactivation requires explicit operator decision.

**3. Session-scoped memory (Cowork host)**
- Claude host auto-memory lives outside this workspace at `~/Library/Application Support/Claude/local-agent-mode-sessions/.../spaces/.../memory/`.
- It is the Claude host's perspective on Josh and the project across Cowork sessions; not canonical to Tilth. Tilth's canonical memory is in layers 1 and 2 above.

**4. Daily operational log**
- [`daily_logs/`](daily_logs/) — per-day append-mostly log. Decisions, incidents, the narrative thread of each working day.

**4z. Product-feature roadmap (deferred / future-software-development)**
- [`pipeline/roadmap/README.md`](pipeline/roadmap/README.md) — roadmap index. Landing page for all deferred product features and session exploration records. NOT the engineering spec-card queue; these are items beyond v0.1 scope, awaiting Stage-transition decisions.
- [`pipeline/roadmap/explorations/`](pipeline/roadmap/explorations/) — session dialogue records that generated deferred ideas. First entry: `2026-04-20_variant_fanout_and_temperature.md` (8 items + 1 addendum + combinatorial cross-cut + business-backlog structural observation).
- [`pipeline/roadmap/deferred/`](pipeline/roadmap/deferred/) — per-feature files when explorations are split. Empty until operator splits the first item.
- Business-backlog parallel folder pending operator decision (structural observation noted in 2026-04-20 exploration).

**4a.1 Tier-1 amendment LOCKs (authorization-ledger'd 2026-04-20)**

All four Tier-1 amendments LOCKED-sealed (policy-lock) with Ed25519 seal ceremony pending. Canonical bytes hashed; authorization token + SHA3-512 recorded at `pipeline/engineering/operator_authorization_ledger.v1.jsonl`. Thesis audit trails preserved at `pipeline/validation/integration_scope_close_2026-04-19/thesis_round_{agent_sdk,tsip,en003}_2026-04-19/` for outside audit.

- EN-001 + EN-002 Agent SDK spike + lifecycle vocabulary — LOCKED-sealed 2026-04-20
- TSIP v0.1 — LOCKED-sealed 2026-04-20; bootstrap exception CONSUMED (F-1 single-use per F-BOOTSTRAP-REUSE gate)
- EN-003 Kimi→Gemini Code Thesis Committee — LOCKED-sealed 2026-04-20 with Cycle 4 disposition folded (4 C4-NEW findings → v2.2 gates #9/#10/#11 + gate #7 v1.1)

**4a. Active integration scope-close**
- [`pipeline/validation/integration_scope_close_2026-04-19/`](pipeline/validation/integration_scope_close_2026-04-19/) — SCOPE-CLOSE 2026-04-19, four items pinned for v0.1 → v0.2. No further items after this set. Six artifacts: `01_scope_pin.md` (verbatim goals) · `02_architecture_amendment_plan.md` (v7 → v7.1/v7.2) · `03_blueprint_amendment_plan.md` (§4 v2.3/v2.4/v2.5 + §5 v6 + §0.5 paired commits) · `04_thesis_round_dispatch_plan.md` (L-005 round assignments) · `05_preflight_existence_audit.md` (L-006 tags) · `06_handoff.md` (handoff contract).

**4b. Governance Plan Preflight (GPP) — mechanism filed 2026-04-19 evening; LOCK-READY 2026-04-19 night**
- Spec: [`pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md`](pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md) — three tiers (DET / COUNCIL / SYNTHESIS), 10 deterministic checks, 12 failure codes (`F-GPP-*`), **27 §0.5 paired-commit rows** (updated from 26 per Thesis-round F-2 — primitive-kind purity). Tier 2 is unconditional; Tier 3 manifest validity defined with 5 criteria.
- Tool: [`pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_det.py`](pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_det.py) — v1 reference implementation (stdlib + PyYAML). Phase 0 tool-hardening queue pinned in `da_vinci_engineer_prompt_v2.md` §7.
- First bootstrap report: [`pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_det_report_2026-04-19.md`](pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_det_report_2026-04-19.md).
- Manifest slot (awaiting Tier 3 signature): same `gpp/` directory; written by future `gpp_manifest.py`.
- Architecture landing (LOCK-READY, 7 fixes applied): [`pipeline/architecture/v0.1/architecture_v7_0_1_amendment.md`](pipeline/architecture/v0.1/architecture_v7_0_1_amendment.md) — Section E.P.
- Blueprint landing (LOCK-READY): [`pipeline/blueprint/v0.1/section_04_v2_1_1_amendment.md`](pipeline/blueprint/v0.1/section_04_v2_1_1_amendment.md) — §4.14a.
- Index landing (LOCK-READY): [`pipeline/blueprint/v0.1/section_00_5_v5_amendment.md`](pipeline/blueprint/v0.1/section_00_5_v5_amendment.md) — 27 paired-commit rows.
- **Thesis round (L-005 two-audit + domain-split):** [`pipeline/validation/integration_scope_close_2026-04-19/thesis_round_gpp_2026-04-19/`](pipeline/validation/integration_scope_close_2026-04-19/thesis_round_gpp_2026-04-19/) — Pass 1 (Editor + Judge), Pass 2 (Red Team + Reasoner), Synthesis + 7 fixes (F-1..F-7), Judge re-score 17/18 = 94%. Thought-experiment voice per L-007 bootstrap exception.

**4c. Engineering persona — LOCK-READY 2026-04-19 night**
- [`pipeline/engineering/da_vinci_engineer_prompt_v2.md`](pipeline/engineering/da_vinci_engineer_prompt_v2.md) — Da Vinci engineering persona prompt for Claude Code, v2 (supersedes v1 at use-time). Read order + read-discipline-across-sessions, voices-in-back-of-head (council-seat survey synthesis with thought-experiment provenance preamble + Committee-voice family mapping), code principles, GPP gating discipline, **nine** standing orders (added memory-hygiene as #9), §13 real-engineer qualifications + §13a revocation sub-section (post-birth kill-switch). Real-engineer-validation gate pinned: Da Vinci does not instantiate as a Tilth seat until a human engineering advisor confirms per `real_engineer_validation_<date>.md`. Future-arc idea (out of current scope-close): Da Vinci as a background Quill character scanning the web for tools/model-landscape and maintaining the network — awaits real-engineer validation + distinct operator reopen-scope decision.
- **Thesis round (L-005 two-audit + domain-split):** [`pipeline/validation/integration_scope_close_2026-04-19/thesis_round_davinci_v2_2026-04-19/`](pipeline/validation/integration_scope_close_2026-04-19/thesis_round_davinci_v2_2026-04-19/) — Pass 1 (Editor + Judge), Pass 2 (Red Team + Reasoner with BLOCKING DVRT-4 kill-switch finding), Synthesis + 12 fixes (DV-F-1..DV-F-12), Judge re-score 18/18 = 100%. Thought-experiment voice per L-007 bootstrap exception.

**5. Run-level telemetry**
- [`pipeline/orchestrator/run_log.json`](pipeline/orchestrator/run_log.json) — seat-call history, scout_scan_live_api records, drafting runs. Machine state, not narrative.
- [`state/`](state/) — transient daemon/agent state that can regenerate.

## Memory hygiene

Per SOUL.md (workspace-wide): "On any new decision, rule, or correction, save to a memory file or daily log IN THE SAME TURN. Do not batch to end-of-session. What isn't written isn't remembered."

Per feedback/topology discipline: before adding a memory file, check whether an existing file can be updated. Duplicates across layers are a bug.

**Auto-consolidation trigger.** A wake-up preflight (`scripts/memory_size_check.sh`, also exposed as `python -m pipeline.cli.tilth_memory auto-trigger`) fires when this file crosses an early-warning threshold (default 200 lines / 12 KiB; overridable via `MEMORY_TRIGGER_LINES` / `MEMORY_TRIGGER_BYTES`). Exit code 10 nudges the agent to invoke the `consolidate-memory` skill — or re-run with `--run` to invoke the engine inline. The engine itself (`pipeline/memory/consolidate_index.py`) still fires at 20 KiB; the trigger sits below it so the operator gets a heads-up before the real consolidation boundary. Every fired event is appended to `pipeline/institutional_memory/memory_consolidation_log.jsonl`.

**5a. Architecture amendment LOCKs (v7.0.x corrective line)**

- v7.0.6 SELF-LOCKED 2026-05-09: [`memory/project_architecture_v7_0_6_locked.md`](memory/project_architecture_v7_0_6_locked.md) — Council and support-agent roster reconciliation. Six seats canonical (adds Red Team). Five support agents named (Intake + Uploader v0.1; Data Collector + Report Generator v0.2; Archivist v1.x). Unblocks WS-B/C/D/F per v0.2 dispatch plan.

## Wake-up read order

AGENTS.md specifies: SOUL → USER → router.yaml → last two daily_logs → lessons.md → **this file** → agent-specific overrides → task-specific PROJECT_CONTEXT.
