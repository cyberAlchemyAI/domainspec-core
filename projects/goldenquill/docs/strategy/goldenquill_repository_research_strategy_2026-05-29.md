---
title: GoldenQuill Repository Research Strategy
date: 2026-05-29
dispatch: docs/strategy/goldenquill_repository_research_strategy_2026-05-29.dispatch.json
status: draft-dispatch-validated
purpose: Understand repository architecture, feature/runtime maturity, existing improvement candidates, and new improvement opportunities through a governed multi-subagent research run.
---

# GoldenQuill Repository Research Strategy

## Objective

Run a read-only, path-evidence-first repository research pass that explains:

- what the GoldenQuill / Tilth repository is architecturally,
- which features and workflows exist,
- what is runtime-live versus tested-only, signed-only, documented-only, dormant, or historical,
- which improvement candidates already exist in backlog/audit/roadmap artifacts,
- which new improvement candidates are not already covered by existing backlog, audit, roadmap, issue draft, or patch-queue artifacts,
- which candidates are safe engineering tasks, Josh-decision items, Gate 1/Gate 2 blockers, or architecture/LOCK-process work.

The route is intentionally research-first. Implementation starts only after Josh chooses the first candidate.

## Dispatch Artifact

Machine-readable route:

`docs/strategy/goldenquill_repository_research_strategy_2026-05-29.dispatch.json`

The dispatch uses `dispatch-spec` with:

- mode: `implementation-research`
- pattern: wake-up -> current-truth map -> parallel subagents -> net-new improvement tournament -> synthesis -> ranking -> validation -> handoff
- join policy: `parent_synthesis`
- subagent strategy: `recommended`, authorization `requires_user_permission`
- promotion guardrail: research findings do not become canonical architecture, maturity, memory, or implementation work without owner review.

## First Reading Order

Start with the repo's truth front door before fanning out:

1. `README.md`
2. `PROJECT_STATUS.md`
3. `RUNTIME_MATURITY_MATRIX.md`
4. `pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md`
5. `docs/AGENT_CONTEXT_INDEX.md`
6. `SOUL.md`
7. `USER.md`
8. `router.yaml`
9. `lessons.md`
10. `MEMORY.md`
11. `docs/COLLABORATOR_HANDOFF.md`
12. `docs/TECHNICAL_BACKLOG.md`
13. `docs/LOCAL_DEVELOPMENT.md`
14. `docs/ARCHITECTURE_OVERVIEW.md`

Treat dated snapshots as evidence, not final truth. `PROJECT_STATUS.md` and `RUNTIME_MATURITY_MATRIX.md` are central, but both are dated 2026-05-17 and should be reconciled against current files before acting.

## Subagent Fanout

Each subagent receives file paths only, not pasted file contents. Every material claim must cite a concrete path.

| Agent | Question | Primary evidence zones |
| --- | --- | --- |
| A1 Implementation Architecture | What are the main implementation subsystems and authority boundaries? | `golden_quill_substrate/`, `pipeline/nervous_system/`, `pipeline/orchestrator/`, `pipeline/loop/`, `pipeline/logician/`, `pipeline/sovereignty/`, `pipeline/vault/` |
| A2 Feature / Workflow Surface | What workflows are visible from skills, CLIs, apps, and tests? | `skills/`, `pipeline/cli/`, `pipeline/scout/`, `pipeline/orchestrator/seats/`, `apps/`, `tilth/bin/`, `tests/` |
| A3 Test / Quality Map | Which tests protect which subsystems, and what verification gaps remain? | `tests/`, `.github/workflows/`, `scripts/run_tests.sh`, `pipeline/linting/` |
| A4 Governance / Current Truth | Which docs are current heads, stale snapshots, historical, or LOCK-bound? | `PROJECT_STATUS.md`, `RUNTIME_MATURITY_MATRIX.md`, `pipeline/architecture/`, `pipeline/blueprint/`, `pipeline/engineering/`, `lessons.md`, `MEMORY.md` |
| A5 Data / Security / Org Isolation | Where are client-data, key, provider-boundary, signed-register, and vault constraints enforced? | `pipeline/sovereignty/`, `pipeline/vault/`, `pipeline/orchestrator/provider_boundary.py`, `logician/`, `vault_shared/`, `orgs/` only if one org is explicitly named |
| A6 Product / UI / Journey Surface | Which UI and product docs are production, prototype, generated, or historical? | `apps/`, `landing/`, `docs/whitepapers/`, `docs/FRONTEND_BOUNDARY.md`, UI audit docs |
| A7 Improvement Candidate Scout | What backlog/audit/roadmap items already exist, and how do we avoid duplicating them? | `docs/TECHNICAL_BACKLOG.md`, `docs/github_issues_drafts_2026-05-17.md`, `docs/project_audit_2026-05-18.md`, `pipeline/roadmap/`, card-system research docs |
| A8 Net-New Improvement Scout | What new improvements emerge from architecture gaps, duplicate implementations, stale truth, missing validation, developer friction, product/architecture tension, or simplification opportunities? | Full-repo evidence after A1-A7 findings, checked against backlog/audit/roadmap prior art |

## Net-New Improvement Tournament

After the first fanout, run a focused candidate-generation tournament. It exists to avoid the common failure mode where "research strategy" only re-lists the backlog.

Tournament roles:

- N1 architecture-gap proposer
- N2 runtime-verification proposer
- N3 developer-experience proposer
- N4 product-journey proposer
- N5 governance-simplification proposer
- N6 duplicate-work challenger

Each proposed new improvement must include:

- concrete path evidence,
- why it is not already covered by `docs/TECHNICAL_BACKLOG.md`, `docs/github_issues_drafts_2026-05-17.md`, `pipeline/roadmap/`, `docs/project_audit_2026-05-18.md`, or card-system patch queues,
- classification as `net-new`, `duplicate`, `partial-overlap`, or `needs-human-call`,
- owner surface,
- validation path,
- likely next route.

## Synthesis Contract

The parent synthesis produces four maps:

1. Subsystem architecture map.
2. Feature/workflow map.
3. Governance and do-not-touch boundary map.
4. Deduped improvement candidate map.
5. Net-new improvement candidate map.

Each improvement candidate must include:

- evidence path,
- maturity status,
- candidate status: existing/recovered, net-new, partial-overlap, duplicate, or uncertain-prior-art,
- existing backlog/roadmap/audit owner if already present,
- category: Gate 1, Gate 2, safe first task, Josh-decision blocked, architecture/LOCK-only, UI-lane, historical/deferred,
- blast radius,
- validation path,
- suggested next route.

Use the repo's maturity vocabulary exactly: `runtime-live`, `gate-live`, `asset-signed`, `spec-locked`, `schema-scaffold`, `dormant`, `historical`.

## Early Findings From This Strategy Pass

These are not full research conclusions; they are seed findings from the initial subagent fanout.

- The implementation has several strong subsystem boundaries: `pipeline/nervous_system/` as API/control boundary, `pipeline/orchestrator/` plus `pipeline/loop/` as council dispatch/runtime lifecycle, `pipeline/logician/` as deterministic gate surface, `pipeline/sovereignty/` plus `pipeline/vault/` as local-first persistence and isolation.
- `golden_quill_substrate/` looks important but may not be install-packaged because `pyproject.toml` package discovery includes `pipeline*` only. This should become a packaging/boundary research question, not an immediate patch.
- Top-level `logician/` and `pipeline/logician/` may be separate generations or distinct interfaces. Classify before consolidating.
- The repo already has a live work queue in `docs/TECHNICAL_BACKLOG.md`. Do not create a fresh backlog before deduping against it.
- UI surfaces need canonical classification: `apps/tilth_demo_v0/` says demo, `apps/tilth_ui/` has local shell/audit material, and `apps/tilth_ui_react/` appears scaffold-like. Treat UI findings as UI-lane unless proven production-path.
- The missing `daily_logs/` directory conflicts with wake-up expectations and docs that cite `daily_logs/2026-05-17.md`. Research should classify this as a stale/missing-state issue.
- `lessons.md` and `USER.md` appear to differ in wording about cached opportunity data. `USER.md` says cached datasets are parallel primary discovery channels and the rule bites at VERIFY; `lessons.md` L-001 says cache is reference-only. This is governance-significant and should be reconciled before Scout research conclusions.

## Gates

- Wake-up gate: read `SOUL.md`, `USER.md`, `router.yaml`, recent daily logs when present, `lessons.md`, and `MEMORY.md` before synthesis.
- Org-isolation gate: do not read `orgs/<slug>/PROJECT_CONTEXT.md` unless exactly one org is named.
- Path-evidence gate: every material claim cites a path or handle.
- Maturity gate: runtime claims use `RUNTIME_MATURITY_MATRIX.md` vocabulary.
- Blueprint-head gate: start from `ACTIVE_BLUEPRINT_INDEX.md` before treating blueprint files as current.
- Do-not-touch gate: no edits to LOCKed amendments, signed cards, `lock_history`, org/client data, root wake-up files, or signed/register surfaces during research.
- Duplicate-work gate: classify candidates against existing backlog, roadmap, issue draft, audit, and patch-queue artifacts before proposing new work.
- Net-new prior-art gate: any candidate marked `net-new` must show the prior-art check and explain why it is not already queued.
- Operator gate: Josh chooses the first implementation candidate.

## Next Route

Recommended next route: run the dispatch as a full research package, then use `decision-gate` to select one first implementation route.

Likely first candidate families:

- `docs/TEST_VERIFICATION_MATRIX.md` first draft.
- Canonical UI/prototype classification.
- Packaging/boundary classification for `golden_quill_substrate/`.
- Top-level `logician/` versus `pipeline/logician/` classification.
- Current-truth reconciliation for missing `daily_logs/` and dated status docs.
- Backlog dedupe pass against `docs/TECHNICAL_BACKLOG.md`, issue drafts, roadmap, audit docs, and card patch queue.
- Net-new improvement tournament focused on architecture simplification, validation gaps, developer experience, and product-journey clarity.
