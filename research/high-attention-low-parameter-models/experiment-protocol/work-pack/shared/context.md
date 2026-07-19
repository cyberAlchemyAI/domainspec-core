# Shared Execution Context

## Objective

Materialize and run the experiment in [SPEC.md](../../SPEC.md) without changing
its claim boundary, typed KILLs, four-surface ownership, or evidence rules.

## Authority Precedence

1. Approved human decision records under future `configs/decisions/`.
2. [SPEC.md](../../SPEC.md) and its aspect docs.
3. [ARCHITECTURE-BUNDLE.md](../../ARCHITECTURE-BUNDLE.md).
4. [IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md).
5. [WORK-PACK.md](../../WORK-PACK.md), then task/SWU contracts.
6. [Auditor-approved research findings](../../../experiment-protocol-research/findings.md).
7. Explorer transcript for source-backed detail.

If two sources conflict, stop and route to the owner of the higher-precedence
artifact. Never repair an upstream artifact silently during task execution.

## Global Constraints

- Experiment execution is currently blocked.
- Full vs compact is retention/non-inferiority, not required improvement.
- Any “uses long context better” claim requires difference-in-retention.
- Present, retained, selected, and successfully used evidence remain distinct.
- Checkpoint comparisons are not parameter causality.
- Every attempt and infeasible cell remains visible through a typed receipt.
- No 128K cell without exact template fit and resident-KV witness.
- Capability/resource axes remain separate.
- No unversioned LLM judge.
- No model run without explicit resource authorization.

## Non-Goals

- Training or fine-tuning models.
- Proving an internal attention mechanism.
- Creating a public benchmark or hosted inference service.
- Generalizing beyond measured checkpoint/runtime/hardware stacks.
- Implementing live retrieval, Phi, realistic corpora, 128K, or second-stack
  portability before an L2 phase decision.

## Execution-Time Context Builder Rule

For each selected SWU, Context Builder must emit a strict runtime handoff pack
under session/run evidence in Markdown and JSON/index form. It must cover:

- one SWU and parent task;
- source selectors and authority precedence;
- dependencies and blockers;
- write scope and non-goals;
- done criteria and validation surface;
- expected receipt shape.

An uncovered obligation or stale model/runtime fact blocks handoff. Invoke plan
does not pre-generate these packs.

## Expected SWU Receipt

```yaml
swu_id: SWU-HALP-NNN
result: pass | flag | block | interrupted
capability_ref: capability-id
receipt_kind: native-stage | subagent | local-fallback | blocked
receipt_artifact: path-or-none
files_touched: []
validation: []
blockers: []
residue: []
reroute: owner-or-none
handoff_note: synchronization note
```
