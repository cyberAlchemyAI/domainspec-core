# Precedent review

Verdict: `FAIL`, repairable. The synthesis preserves authority ceilings but introduces new names for responsibilities already owned by Arcanum.

## Existing owner routing

- App Server initialization/thread/turn/item/request operations belong in an App Server runtime-adapter profile under `arcanum/framework/runtime`, with Task Session admission/reconciliation. They do not create gates or a second execution owner.
- Replace standalone `CodingExecutionHost` with an App Server adapter contract inside the existing provider-neutral durable runtime.
- Extend existing runtime handoff and Task Session admission artifacts with App Server protocol/native IDs; do not create a parallel execution envelope authority.
- Put host ID fields into owner-local adapter maps. Do not create a second global identity ledger.
- Extend existing runtime/Orchestrate/Task Session journals and replay protection; do not create a shared second causal store or reducer.
- Translate App Server terminal state at the adapter boundary and submit to existing Task Session/capability-owner validation.
- Treat approval separation as adapter mapping/oracle under Dispatch Spec/Goal/Decision Gate owners, never as a new authority.
- Reuse Task Session touched-path/baseline/output validation; turn diffs are inputs only.
- Missing receipt ingestion, row planning, rendering, and CAS application are missing deterministic implementations inside Craft, not ownerless capabilities.
- Missing Goal journal/no-progress execution belongs to Goal. Preserve the unresolved August 5 finite-series reducer decision; do not introduce a third reducer.
- App Server fixtures, profiles, failure injection, canaries, and denominator regression belong to Experiment Harness.
- Privacy-safe derivation belongs to Observed Invocation Loop/Signal Observer and is partial, not absent.
- Generated attachment belongs to existing bootstrap/generation/sync owners.
- Lifecycle non-promotion is an App Server-specific regression under existing lifecycle/eval owners.
- Do not broaden Orchestrate from spawn-only implicitly. Ordinary Task Session/Refine runtime integration and a future Orchestrate host profile are separate decisions.

August 12 Orchestrate repair already proves owner-held wait replay, opaque native identity, and blocked-wave closeout invariants. App Server work must extend rather than fork them.

Required synthesis repair: re-place every primitive under the existing owner; separate Task Session runtime integration from Orchestrate-host work; keep Craft in Craft and Goal in Goal; preserve the series-owner decision; route canaries and telemetry through the current harness/observation paths.

## Terminal recheck

`PASS`. The repaired synthesis places the App Server profile under the existing durable runtime, preserves all owner boundaries and `DECISION-LOOP-OWNER-001`, and introduces no second planner, reducer, ledger, receipt authority, eval loop, observation truth, lifecycle owner, or promotion path.
