# L0 — Telemetry inventory (candidate, non-authoritative)

Step `inventory-operational-telemetry`. Catalogs telemetry scattered across the repo as
**candidate operational evidence**. By the operational-ontology slice's own rule, *unreviewed
telemetry is not owned by the branch* — it is L0–L2 evidence that may *seed* candidate nodes
(L3) but may not be promoted without owner review. [SB ONTOLOGY-ARCHITECTURE Authority Levels]

## Live counts (measured 2026-06-12)

`arcanum/.arcanum/observability/signals/sigil-invocations.jsonl` — **401 rows**. Sigil
frequency: `invoke` 98 · `task-session` 85 · `context-builder` 56 · `structured-interview-kits`
50 · `refine` 35 · `distill` 34 · `experiment-harness` 16 · `decision-gate` 9 ·
`codex-goal-profile` 7 · `sigil-development` 3 · `workflow-reflect` 2 · `definitions-governance` 2.

**Honest nuance [SB]:** in this repo the flat signals ledger rows are *index-shaped*
(`run_id, dedupe_key, ledger, line, sigil, capability, execution_status, reflection_trigger,
recommendation, target_artifact`) — `execution_status`/`reflection_trigger` are mostly null at
this layer. The **rich** execution detail (request.intent, execution.status, observer.workflow_gaps,
validation) lives in `envelopes/` and `runs/`, not the flat ledger. A derivation route must read
envelopes for outcome/quality fields. → residue R-T1.

## Streams (richest first)

| Stream (path) | Volume | Operational signal it carries |
| ------------- | ------ | ----------------------------- |
| `arcanum/.arcanum/observability/envelopes/{invoke,task-session}/` | full records | `capability`, `mode`, `request.intent`, `execution.{status,outputs,files_changed,validation}`, `observer.{quality_bar_status,workflow_gaps[],reflection_trigger,recommendation}` → **invocation, gap, reflection, validation nodes**. |
| `arcanum/.arcanum/observability/signals/sigil-invocations.jsonl` | 401 | invocation index → **route/sigil invocation count, target_artifact edge**. |
| `arcanum/.arcanum/observability/reflection-state.json` | aggregates | per-sigil execution/output/gap/severe-gap counters, last-reflection → **maturity + reflection-trigger evidence**. |
| `arcanum/.arcanum/observability/by-sigil/*.jsonl` | 17 indexes | per-sigil invocation index. |
| `arcanum/.arcanum/observability/hooks/hook-operations.jsonl` | ~1.2M | pipeline meta-events (`hook`, `action`, `status`, `dedupe_key`) → session→hook→signal edges. |
| `**/*.dispatch.json` | **63 files** | `subagent_strategy.roles[]`, `techniques`, `route_menu`, `native_stage_receipts`, `trace_events` → **route, role-delegation, receipt nodes**. |
| `.arcanum/necronomicon/capabilities.json` | install state | selected sigils/spells/harness commands → **capability inventory node set**. |
| `docs/signals/terminal-guard.jsonl` | aux | command risk + nudges. |
| `docs/signals/delegation-tuning.jsonl` | aux | `skill, stage, delegationProfile, thinkingBudget, outcome` → **delegation-policy evidence**. |
| Root `.arcanum/observability/` + `projects/*/.arcanum/observability/` | sparse | per-project observability roots (sonar-loop, body-war mostly idle). |

## Assessment

Richest derivation source = **`arcanum/.arcanum/observability/` envelopes + reflection-state**
(390+ meaningful executions with observer assessments) and the **63 dispatch files** (route +
delegation topology). These support candidate nodes for: route, sigil/capability, invocation,
workflow-gap, reflection-trigger, decision (via decision-gate signals + dispatch gates),
delegation-policy, and maintenance-trigger.

## Residue

- **R-T1:** flat ledger lacks outcome fields; derivation must read `envelopes/`. [SB]
- **R-T2:** telemetry concentrated in `arcanum/.arcanum/` (the framework subrepo); domainspec-core
  root + project roots are sparse — an operational branch *for domainspec-core* may under-sample
  project-level operation. [T]
- **R-T3:** no existing stream emits "discipline hardened" or "lesson → policy" mutations; those
  would be new operational mutation types, not yet observed. [H]
