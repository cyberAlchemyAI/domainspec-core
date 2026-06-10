# Infra-Spec Observability And Residue Ledger

Lane: L5 — Observability And Residue Analyst
Parent dispatch: `infra-spec-research-strategy-20260603`
Date: 2026-06-08
Status: research evidence only; not infra-spec authority.

Question: how should infra-spec expose drift, failure, and reflection?

Classification legend (per strategy non-negotiables, lines 41):
`implementation-backed` = observed in a working artifact/script/config; `documented` = stated in a doc/template; `analogy` = transferred from another domain; `candidate` = proposed, not yet evidenced; `residue` = does not cross cleanly and must be tracked.

All claims cite a path relative to the worktree root `.claude/worktrees/codex+infra-spec/`.

---

## 1. Observability / Residue Map

| Signal kind | Where produced (path) | Class | What it would mean for infra-spec |
| --- | --- | --- | --- |
| Sigil invocation telemetry (one JSON object per run) | `.arcanum/observability/signals/sigil-invocations.jsonl`; schema `arcanum/framework/observability/SIGIL-OBSERVABILITY-HOOK.md` | implementation-backed | The append-only post-run ledger pattern is the model for an infra-spec runtime receipt stream: one record per infra apply/deploy/observe run. |
| Per-capability ledger | `.arcanum/observability/by-sigil/experiment-harness.jsonl` | implementation-backed | Infra-spec should keep a per-deployment-unit (or per-environment) ledger mirroring `by-sigil/`, e.g. `by-environment/` or `by-deploy-unit/`. |
| Reflection counters + thresholds | `.arcanum/observability/reflection-state.json`; `.arcanum/observability/config.json` (`thresholds.meaningful_executions`, `severe_workflow_gaps`, `hook_failures`) | implementation-backed | Drift/failure thresholds that auto-trigger reflection are a proven mechanism; infra-spec needs its own threshold table (e.g. consecutive-deploy-failures, repeated-drift events). |
| Observed-run envelope (long-running work) | `arcanum/framework/observability/templates/observed-run-envelope.json` (`session_id`, `run_id`, `parent_run_id`, `status: opened`, `closed_at`, `execution`, `observer`) | documented | An infra apply is a long-running observed run: open → execute → close, with parent_run_id for orchestrated multi-stage deploys. |
| Invocation envelope contract | `arcanum/framework/observability/templates/invocation-envelope.json`; `.claude/skills/signal-observer/SKILL.md` | documented | Defines the minimal receipt fields (status enum, outputs, files_changed, validation, observer block). Directly portable to an infra runtime receipt. |
| Runtime RUN descriptor | `arcanum/framework/runtime/templates/RUN.json` (`schema_version: arcanum.runtime.run.v1`, `adapter_id`, `loop_role`, `parent_run_id`, `events_path`, `artifacts_dir`, `children_dir`) | documented | The deploy/runtime "what was launched" record: adapter, loop topology, child runs, artifact dirs. Infra-spec topology + run lineage maps onto this. |
| Runtime STATUS descriptor | `arcanum/framework/runtime/templates/STATUS.json` (`status`, `adapter_status`, `validation_grade`, `output_paths`, `blocked_reason`, `error_summary`, `started_at`, `completed_at`) | implementation-backed (real blocked instance below) | The deploy outcome record. Carries blocked_reason + error_summary separately from status — the exact separation infra-spec needs. |
| Real blocked runtime receipt | `arcanum/framework/runtime/development/refinement-runs/arcanum-refine-20260526T222905Z/runtime/codex-exec-smoke/STATUS.json` (`status: blocked`, `blocked_reason: codex-state-unavailable`, `error_summary` points to log) | implementation-backed | Evidence that environment-unavailable is a first-class, non-failure blocked state with a pointer to the raw log artifact. Infra-spec must distinguish "blocked by environment" from "failed deployment". |
| Runtime event stream | `arcanum/.../codex-exec-smoke/events.jsonl` (`created → adapter-started → blocked` each with timestamp/status/message) | implementation-backed | Per-run event log = the deploy timeline. Infra-spec receipts should reference an events stream, not just a terminal status. |
| Production pipeline signal taxonomy | `projects/body-war/domainspec/templates/SIGNAL-SCHEMA.md`; live data `projects/whisky-doses/docs/signals/pipeline-signals.jsonl` | implementation-backed | The richest in-repo failure/drift taxonomy: `step-verdict`, `alignment-gap`, `spec-gap`, `governance-gap`, `rework`, `overhead`, `decision`, `pattern`, `proposal`, `spec-compliance`, `agent-cost`, with severity + category + session-completeness invariants. Most of this transfers directly. |
| Drift signal: `alignment-gap` | `projects/body-war/domainspec/templates/SIGNAL-SCHEMA.md` (`gapType: code-without-spec / spec-without-code / contract-mismatch`) | implementation-backed | Direct model of infra-spec drift: spec-without-deployment, deployment-without-spec, contract-mismatch between spec and runtime realization. |
| Drift signal: `governance-gap` | same (`shouldHaveBeenCaughtBy`, `suggestedFix`, `occurrences`) | implementation-backed | Captures "framework blind spot" — for infra-spec, an observability blind spot or an unowned-state gap the validator failed to catch. |
| Reflection threshold table | `projects/body-war/domainspec/templates/SIGNAL-SCHEMA.md` TH1–TH10 (e.g. TH4 "rework on same step in 5+ signals → flag for hardening"; TH7 "CRITICAL governance-gap → immediate issue") | implementation-backed | A ready failure-to-reflection trigger matrix infra-spec can adapt (e.g. repeated deploy rework → flag deploy unit for hardening). |
| CI drift gate (governance) | `.github/workflows/drift-check.yml`; `tools/check_github_drift.sh` (emits `[ok]/[warning]/[violation]`, exits 1 on violations) | implementation-backed | A real drift detector: inventory snapshot diff between source and install targets, policy classification, fail-on-violation. Model for infra-spec "spec vs deploy reality" drift CI. |
| CI code-tag validation | `.github/workflows/drift-check.yml` step `pnpm run check:code-tags` (in `implementation/domainspec`) | documented (submodule uninitialized here) | Spec-to-code binding check; infra-spec analog would validate spec-to-runtime tags/labels. |
| CI quality gate + failure artifact upload | `projects/goldenquill/.github/workflows/ci.yml` (lint + pytest + AST-lint, `upload-artifact ... if: failure()`, wheel install smoke) | implementation-backed | Failure-residue capture pattern: on failure, persist the diagnostic artifact (pytest cache). Infra-spec receipts should attach failure residue artifacts on a blocked/failed run. |
| Validation ledger (route-level) | `ops/development/domainspec-lean-formalization-validation-ledger.md` | implementation-backed | Demonstrates separating dispatch-shape validation, execution validation, evidence coverage, local checks, build attempts, mutation audit, and explicit "Validation Gaps". Infra-spec validation ledger should keep the same sections. |
| Mutation audit / unexpected-write residue | same ledger, "Mutation Audit" section (toolchain temporarily changed `lean-toolchain`, then restored) | implementation-backed (residue) | Proves "unexpected mutation outside declared write scope" is a real residue class. Infra-spec must record runtime side effects that escape the declared change set. |
| Build/proof/status separation caution | same ledger, "Build Attempts" + "Final Validation Verdict" (build timed out ≠ proof failure; status categories must be separate) | implementation-backed | Confirms strategy thesis (line 34): specified / implemented / deployed / observed / validated / promoted must be distinct status budgets; a tooling timeout is not a deploy failure. |
| Blocker resolution / status-change signal | `ops/development/REFRESH-SURFACE-BLOCKER-DECISIONS.md` (`Type: blocker_resolved`, `status_changed: blocked → accepted`, `route_changed`, `Confidence`, `Mutation safety`) | implementation-backed | A typed blocker lifecycle (raise → decide → resolve → route-change) with confidence + mutation-safety fields. Infra-spec promotion gates need this exact lifecycle. |
| Hook operations / failures / dedupe ledgers | `.arcanum/observability/config.json` (`hook_operations_path`, `hook_failures_path`, `hook_dedupe_path`); `arcanum/framework/observability/HOOK-OPERATIONS-LEDGER.md`; loop-guard in `.claude/skills/signal-observer/SKILL.md` | documented | The observer-of-the-observer layer: telemetry about the telemetry pipeline itself (failures, skips, dedupe). Infra-spec needs a parallel "did the receipt/telemetry pipeline itself run" channel so observability blind spots are themselves observable. |
| Reflection report output | `.claude/skills/workflow-reflect/SKILL.md` (writes to `.arcanum/observability/reflections/`; proposals carry evidence, target section, expected prevention, priority, compatibility impact) | implementation-backed | The outer reflection loop contract: aggregate signals → threshold-backed proposals (never single-anecdote) → report → update reflection state only after report written. Direct template for infra-spec reflection loop. |

Signals mapped: 24 rows above.

---

## 2. Receipt Requirements (fields an infra-spec runtime receipt should carry)

Synthesized from the runtime RUN/STATUS pair (`arcanum/framework/runtime/templates/RUN.json`, `STATUS.json`), the observed-run envelope (`arcanum/framework/observability/templates/observed-run-envelope.json`), the production signal schema (`projects/body-war/domainspec/templates/SIGNAL-SCHEMA.md`), and the goldenquill `CycleReceipt` model (`projects/goldenquill/CLAUDE.md`, "WPFA cycle-close accounting").

Identity / lineage (from RUN.json):
- `schema_version` (e.g. `infra-spec.receipt.v1`) — versioned, like `arcanum.runtime.status.v1`.
- `run_id`, `parent_run_id`, `loop_role`, `loop_id` — run lineage for multi-stage / child deploys.
- `target_kind` + `target_id` — the deploy unit / environment / service the receipt is about.
- `adapter_id` / `adapter_profile_path` — which runtime realized the spec.

Intent (from invocation-envelope.json `request`):
- `request.summary`, `request.intent` — what the deploy/apply was meant to do (privacy-scrubbed; no secrets, per `signal-observer` privacy-rules).

Execution outcome (from STATUS.json + invocation-envelope):
- `status`: `queued | running | completed | partial | blocked | failed` (union of RUN/STATUS and invocation enums).
- `adapter_status` — runtime-level status, separate from logical status.
- `validation_grade` — graded validation outcome (STATUS.json has this; e.g. `adapter-safety`).
- `outputs[]`, `files_changed[]` / `artifacts_dir`, `output_paths[]`.
- `events_path` — pointer to the per-run event stream (`events.jsonl`).
- `started_at`, `completed_at`.

Failure / residue (from STATUS.json + body-war signals + goldenquill F-* gates):
- `blocked_reason` (e.g. `environment-unavailable`) — distinct from failure.
- `error_summary` + pointer to raw log artifact (never inline the raw log; cf. `signal-observer` privacy-rules).
- `failure_code` — typed, from a closed failure-code family (analog of goldenquill `F-CLASS-*` / `F-WPFA-*`).
- `unexpected_mutations[]` — side effects outside declared change set (from validation-ledger Mutation Audit).
- `rework` block — iterations, root_cause, resolution (from body-war `rework` signal).

Drift (from body-war `alignment-gap` + drift-check CI):
- `drift[]` with `kind: spec-without-deploy | deploy-without-spec | contract-mismatch`, `spec_ref`, `runtime_ref`, `description`.

Observer block (from invocation-envelope `observer`):
- `quality_bar_status`, `anti_pattern_hits[]`, `workflow_gaps[]` (category/severity/summary/evidence), `output_contract_drift`, `reflection_trigger`, `recommendation`.

Provenance / trust (from goldenquill `CycleReceipt`):
- `trace_id` / span provenance (goldenquill links every claim to a `Logfire trace_id`; `F-WPFA-SPAN-PROVENANCE-MISSING` is fail-closed).
- `operator_signature` for promotion-gated receipts (goldenquill `F-WPFA-OPERATOR-SIGNATURE-MISSING` blocks buyer-facing emission without operator Ed25519). Infra-spec promotion of a runtime receipt to authority should require an explicit signed attestation — supports strategy non-negotiable that "runtime evidence cannot become promotion authority by itself" (line 40).

Privacy invariants (from `.claude/skills/signal-observer/SKILL.md` privacy-rules):
- No secrets/credentials/tokens/keys; prefer paths over content; mark missing evidence `not_checked`, never infer success.

---

## 3. Failure Taxonomy Candidates

Evidence-backed (transfer from `projects/body-war/domainspec/templates/SIGNAL-SCHEMA.md` + STATUS.json + validation-ledger):

1. `deploy-rework` — apply needed retries/correction (body-war `rework`; STATUS `partial`). Fields: iterations, root_cause, resolution. `candidate` for infra.
2. `contract-mismatch` (drift-failure) — runtime realization disagrees with spec (body-war `alignment-gap.contract-mismatch`; CI `drift-check.yml` violations). `implementation-backed` source.
3. `spec-without-runtime` / `runtime-without-spec` — orphan spec or unowned deployed state (body-war alignment-gap `spec-without-code` / `code-without-spec`). `implementation-backed` source.
4. `environment-blocked` — runtime/tooling unavailable, NOT a deploy failure (STATUS `blocked_reason: codex-state-unavailable`; validation-ledger build timeout). `implementation-backed`.
5. `unexpected-mutation` — side effect outside declared write scope (validation-ledger Mutation Audit). `residue` class.
6. `governance/observability blind spot` — a gap the validator/observer should have caught but did not (body-war `governance-gap`, `shouldHaveBeenCaughtBy`). `implementation-backed`.
7. `spec-compliance violation` — the runtime/agent deviated from its own declared contract (body-war `spec-compliance`). `implementation-backed`.
8. `promotion-attestation-missing` — runtime evidence presented as authority without signed promotion (goldenquill `F-WPFA-OPERATOR-SIGNATURE-MISSING`; F-CLASS fail-closed family). `analogy` → strong `candidate`.
9. `provenance-missing` — receipt cannot link to its run/trace evidence (goldenquill `F-*-SPAN-PROVENANCE-MISSING`). `candidate`.

Discipline note (from validation-ledger): a closed failure-code family with explicit severity tiers (body-war `LOW|MEDIUM|HIGH|CRITICAL`) and fail-closed semantics (goldenquill) is preferred over free-text status. Counterexample discipline (strategy line 280): every positive infra pattern should have at least one of these failure codes as its violation fixture.

---

## 4. Reflection-Loop Candidates

All `implementation-backed` from in-repo loops:

1. Threshold-triggered reflection — counters in `.arcanum/observability/reflection-state.json` cross `config.json` thresholds → `workflow-reflect` produces a proposal report in `reflections/`. Infra-spec analog: deploy-failure / drift-event counters cross a threshold → infra reflection report. (`.claude/skills/workflow-reflect/SKILL.md`)
2. Production threshold matrix — body-war TH1–TH10 (`SIGNAL-SCHEMA.md`) give concrete conditions→actions (e.g. TH4 repeated rework → flag for hardening; TH6 alignment-gap > 10 over 5 runs → full alignment audit; TH7 CRITICAL → immediate issue). Adapt as infra-spec deploy/drift thresholds.
3. Evidence-not-anecdote rule — `workflow-reflect` requires `--min-signals` (default 5) and separates threshold-backed findings from weak signals; never mutates the observed thing during reflection (authority-rule). Infra-spec reflection must likewise propose, not directly re-deploy.
4. Reflection packet at cycle close — goldenquill emits a typed `ReflectionPacket` at each cycle close, sibling-not-nested with the `CycleReceipt`, with PENDING→BACKFILL two-phase (decision-observed event). Models an infra "post-deploy reflection" artifact distinct from the deploy receipt. (`projects/goldenquill/CLAUDE.md`, "Reflection Packet v0.1 Beta hook")
5. Observer-of-observer health loop — `reflect-hook-health.sh` / hook-failures ledger (`config.json hook_failures_path`; `HOOK-OPERATIONS-LEDGER.md`). Infra-spec needs reflection over its own telemetry pipeline so observability blind spots surface.

---

## 5. Residue Items (do-not-cross-cleanly; tracked, not deleted)

- R1 `unexpected-mutation residue`: declared write scope can be silently exceeded by tooling/runtime (validation-ledger "Mutation Audit": Lake setup mutated `lean-toolchain`, later restored). Infra-spec must account for runtime side effects beyond the spec'd change set; these never cross cleanly from spec → deployment. `residue`.
- R2 `build/tooling-vs-truth residue`: a tooling/environment block (timeout, state-unavailable) is observably indistinguishable from failure at the status layer unless `blocked_reason` is carried separately (STATUS.json `blocked` vs `failed`; validation-ledger "this is a tooling blocker, not a proof failure"). The interpretation does not cross cleanly into a binary pass/fail. `residue`.
- R3 `telemetry-of-telemetry residue`: the observability pipeline can itself fail/skip (hook failures/dedupe ledgers). Whether a missing infra receipt means "clean run" or "observer failed" is unresolved without the hook-health channel. `residue`.
- R4 `submodule-uninitialized residue`: the deployment-bearing surfaces this lane most needed — `implementation/domainspec/infra/`, `validation/poker-team/infra/` — are git submodules not initialized in this worktree (find returned empty; `tools/check_github_drift.sh` itself guards on their absence with exit 2). The real infra runtime evidence does not cross into this read-only scrub; conclusions about those infra dirs are deferred, not asserted. `residue`.
- R5 `local-only-validated residue`: goldenquill ships a write-protected `local_only_validated: bool` (default false) gating "production-validated" claims (`projects/goldenquill/CLAUDE.md`). "Observed/ran locally" does not cross cleanly into "validated for production" — a dedicated boolean/status is required. `residue`.

---

## 6. Child-Dispatch Proposals

Two triggers from the strategy met (lines 252-259): a project has enough infra material to deserve its own mini-atlas (R4 submodules), and observability schema needs fixture-first validation.

### CDP-L5-1 — Submodule infra observability scrub
- parent_dispatch_id: `infra-spec-research-strategy-20260603`
- scope: scrub `implementation/domainspec/infra/`, `validation/poker-team/infra/`, and `implementation/domainspec` signal/CI surfaces (`check:code-tags`) after `git submodule update --init --recursive`, for runtime receipts, drift detectors, and failure ledgers not visible in this worktree.
- owning lane: L5 (observability/residue), coordinating with L3 (runtime/deployment auditor).
- roles: observability analyst + skeptical reviewer.
- inputs: initialized submodules; this ledger; L3 runtime atlas (when produced).
- expected artifacts: appended rows to this ledger; updated residue R4 resolution.
- stop conditions: submodules cannot be initialized in environment → record as blocked, do not assert.
- join policy: merge findings into this ledger before synthesis.
- validation evidence: every appended row cites an initialized-submodule path.

### CDP-L5-2 — Infra receipt schema fixture validation
- parent_dispatch_id: `infra-spec-research-strategy-20260603`
- scope: turn Section 2 receipt requirements into a `.schema.yml` (YAML-first, validator-backed per strategy line 39) with pass + at least one failure fixture per failure code in Section 3 (counterexample discipline, strategy line 280).
- owning lane: L5 with L4 (schema/taxonomy governor).
- roles: schema author + validator author.
- inputs: Section 2/3 of this ledger; existing schemas (`ops/development/skill-agent-canonical-map.schema.yml`, `.github/skills/arcanum-sigil-inventory/templates/evidence-card.schema.yml`) as form precedents.
- expected artifacts: `infra-spec-receipt.schema.yml` candidate + fixtures (under infra-spec dev scope only; not promoted).
- stop conditions: blocks until L4 minimal viable record shape lands.
- join policy: feed into `infra-spec-schema-taxonomy-ledger.md`.
- validation evidence: schema parses; every failure code has a failing fixture.

Child dispatch proposals: 2 (proposals only; execution stays behind the strategy's approval gate, line 42).

---

## 7. Path Citation Confirmation

Every signal row, receipt field group, failure code, reflection candidate, and residue item cites a concrete worktree-relative path. Confirmed: yes.
