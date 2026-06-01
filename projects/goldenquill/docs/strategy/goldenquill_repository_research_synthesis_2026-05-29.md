---
title: GoldenQuill Repository Research Synthesis
date: 2026-05-29
dispatch: goldenquill-repository-research-20260529
status: synthesized
---

# Repository Research Synthesis

## Executive Shape

The repository is not a single application. It is a governed product substrate with several maturity layers:

- Runtime and policy substrate: `pipeline/orchestrator/`, `pipeline/loop/`, `pipeline/logician/`, `pipeline/sovereignty/`, `pipeline/vault/`, `pipeline/nervous_system/`.
- Contract/prototype substrate: `golden_quill_substrate/`.
- Operator surfaces: `pipeline/cli/`, `tilth/bin/`, `skills/`.
- Product and UI surfaces: `apps/`, `landing/`, `docs/whitepapers/`, frontend specs.
- Governance and truth surfaces: `lock_history.v1.jsonl`, architecture/blueprint amendments, `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, `ACTIVE_BLUEPRINT_INDEX.md`.

The dominant risk is not lack of work. The repo has many queued improvements. The dominant risk is current-truth drift: front-door docs and maturity indexes are stale relative to `lock_history.v1.jsonl` row 292, and product surfaces mix production targets, prototypes, archives, demos, and generated artifacts.

## Subsystem Map

| Subsystem | Role | Evidence |
| --- | --- | --- |
| `golden_quill_substrate/` | Strict schemas and contract envelope prototype | `golden_quill_substrate/contracts.py`, `golden_quill_substrate/ingress.py` |
| `pipeline/nervous_system/` | API/control boundary and model/action access surface | `pipeline/nervous_system/api.py`, `model_access_boundary.py` |
| `pipeline/orchestrator/` | Seat routing, provider boundary, classification review, support-seat runtime | `router.py`, `provider_boundary.py`, `classification_review.py` |
| `pipeline/loop/` | Submission lifecycle and seat loop state machine | `run_pipeline.py`, `seat_runner.py`, `revision_loop.py` |
| `pipeline/logician/` | Deterministic PRE/POST policy and gate runner | `pre_gate.py`, `gate_runner.py`, gate modules |
| `pipeline/sovereignty/` | Boot, keys, session, router integrity, org isolation | `boot.py`, `keys.py`, `isolation.py` |
| `pipeline/vault/` | Path-safe open, writes, classification loading, schemas | `gate_and_open.py`, `vault_write.py`, `classification/signed_register_loader.py` |
| `pipeline/scout/` | Discovery, verify, and review stages | `run.py`, `verify_stage.py`, channel modules |
| `apps/` | Demo/prototype/target UI surfaces | `docs/FRONTEND_BOUNDARY.md`, app README files |

## Feature And Workflow Map

| Area | Status From Research | Notes |
| --- | --- | --- |
| Six-seat council | Runtime-oriented and heavily tested | Scout/Scribe/Editor/Judge/Red Team/Logician surfaces exist across router, loop, seats, and tests. |
| Scout | Mixed production architecture + dev bridge | Full Scout architecture exists, but UI/dev bridge bypass is explicitly non-production. |
| Classification/provider boundary | Runtime-significant | Strong provider boundary exists; production wiring must always provide signed register context. |
| Vault/sovereignty | Runtime-significant with stubs | Strong Python gates; Cedar/M15/FD-broker parts have deferred/skeleton elements. |
| FID/WPFA/report/data collector | Mixed scaffold/spec/runtime pieces | Needs maturity classification per surface. |
| UI | Target/prototype/archive mix | `apps/tilth_ui_react/` is target path but scaffolded; `apps/tilth_ui/` archived; `apps/tilth_demo_v0/` demo. |
| Docs/whitepapers/landing | Mixed current/draft/generated | Whitepaper `.md` files appear binary; landing generator brief conflicts with customer-facing vocabulary. |

## Current-Truth Findings

`pipeline/engineering/lock_history.v1.jsonl` is the hard authority for LOCK chronology. It reaches row 292 on 2026-05-18. Several front-door or sidecar docs stop at row 279:

- `PROJECT_STATUS.md`
- `RUNTIME_MATURITY_MATRIX.md`
- `pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md`

This matters because rows 280-292 include card-publisher key rotation and OD-E fix-forward / embedded re-sign state. Front-door docs currently risk telling a new collaborator the wrong card key and card supersession story.

## Existing Work Queues

Do not create a fresh backlog without deduping against:

- `docs/TECHNICAL_BACKLOG.md`
- `docs/github_issues_drafts_2026-05-17.md`
- `docs/project_audit_2026-05-18.md`
- `pipeline/roadmap/`
- `docs/card_system_deep_research_2026-05-17/`
- `logician/registers/architectural_risk_register.json`

## Net-New Improvement Pattern

The strongest net-new improvement is an indexing and reconciliation layer:

1. Current-truth refresh pack.
2. Product surface index.
3. Implementation-status matrix.

These are not glamorous, but they are leverage: they prevent every later engineer/subagent from spending the first hour asking “which thing is real?”

## Residue Ledger

- `daily_logs/` is absent though required by wake-up and cited by docs.
- `architecture_v7_0_11_card_amendment.md` status conflicts with downstream card-system treatment.
- `golden_quill_substrate/` may be omitted from wheels.
- `apps/tilth_ui_react/` imports or references demo/static data that may be incomplete.
- Some enforcement surfaces are intentionally v0.1 stubs.
- Test suite was not executed during research.
