---
module: high-attention-low-parameter-experiment-protocol
version: 0.1.0-draft
status: decision-gated
updatedAt: 2026-07-18
docType: implementation-layering
observedCapability: invoke
invokeMode: plan
---

# Implementation Layering: High-Attention, Low-Parameter Experiment Protocol

## Purpose

Sequence the work from a deterministic offline contract witness to a
stack-specific paired experiment without pulling GPU execution, realistic
datasets, retrieval, 128K, or portability into the minimum proof.

This artifact governs layer boundaries and promotion evidence. The canonical
task/SWU state lives in [WORK-PACK.md](WORK-PACK.md).

## Source Contract

- [Specification](SPEC.md)
- [Architecture bundle](ARCHITECTURE-BUNDLE.md)
- [Auditor-approved methodology](../experiment-protocol-research/findings.md)
- [Plan work-pack](WORK-PACK.md)

## Target And Scope

- Target: a reproducible, resource-bounded experiment protocol and harness.
- Scope: protocol decisions, deterministic fixtures/rendering/scoring,
  stack/capacity admission, paired execution, analysis, and evidence closeout.
- Current state: define/design/plan artifacts exist; no runnable witness,
  admitted stack, generator, scorer, or run exists.

## Layer Boundary Rule

```text
After this layer, we know whether the current experiment claim is contractually
closed, operationally measurable, decision-bearing, or portable enough to
justify the next cost boundary.
```

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 — contract witness | After this layer, we know whether one semantic plan can deterministically recompose into required arms/rotations and a correct score without model inference. | One approved claim/estimand record, schemas, one fixture per primary family, rendered variants, stored valid/invalid outputs, and deterministic score receipts. | Decision records, protocol/trial/receipt schemas, generator, provenance manifest, renderer, scorer, offline witness. | Checkpoint access, GPU runtime, capacity, statistical claim, retrieval, 128K. | Byte-identical rebuild; schema pass; ground-truth and scorer fixture pass; complete trace from fixture to score. | Continue only if the measurement contract closes without hidden defaults. |
| L1 — measurement smoke | After this layer, we know whether one admitted model stack can execute short/long cells with trustworthy systems receipts. | Exact stack manifest, compatibility smoke, capacity witness, and a tiny non-confirmatory single-stack run. | One checkpoint, one dedicated stack, warmup/cache rules, prefill/decode/memory/energy capture, typed failures. | Paired checkpoint inference, broad matrix, external comparator, live retrieval. | Stack/hash receipt; capacity witness; repeat smoke receipts; telemetry completeness. | Continue only if at least one long-bin cell is feasible and measurements repeat within the frozen tolerance. |
| L2 — decision pilot | After this layer, we know whether the admitted 1B/3B pair yields a decision-bearing retention/checkpoint/resource result on the primary procedural matrix. | Paired compact/full/absent/no-answer trial cells across retrieval, two-hop, contradiction, and early/middle/late positions at approved lengths. | Frozen N/repetitions/margins, paired analysis, false support, feasibility, resource frontier, phase gate. | Phi, realistic corpora, retrieval arms, 128K, independent stack portability. | Complete paired receipts; frozen analysis result; uncertainty; frontier; continue/narrow/pivot/stop decision. | Promote only when the result can change a named design/deployment decision. |
| L3 — portability/package decision | After this layer, we know whether the L2 result survives a justified extension or independent stack and can be packaged without overclaim. | Exactly one approved extension with a declared decision target, plus reproducible package and audit. | Selected external comparator, realistic dataset, retrieval arm, 128K, or second stack—not all by default. | Broad benchmark product, parameter causality, mechanism proof, production service. | Extension receipt, non-regression against L0–L2 guarantees, publication/license audit, claim-bound report. | Package, repeat, narrow, or stop; never generalize beyond measured evidence. |

## Layer Value/Cost Heuristic

- L0 unlocks semantic trust at low cost and eliminates expensive invalid runs.
- L1 unlocks systems feasibility before confirmatory allocation.
- L2 spends the primary GPU/statistical budget only after both prior proofs.
- L3 starts only when one extension has greater decision value than additional
  precision on the L2 result.

Stop a layer when its next unit does not improve the layer's decision more than
opening the next distinct decision boundary.

## Non-Regression Guardrails

- Later layers preserve content-addressed identities and exact traceability.
- Later layers cannot weaken deterministic answer/evidence scoring silently.
- Failure/infeasibility receipts remain visible in every layer.
- Full versus compact remains retention/non-inferiority.
- Checkpoint comparison never becomes parameter causality.
- A capacity witness never becomes behavioral evidence.
- Resource axes remain separate and measurement boundaries remain explicit.
- Optional extension mechanisms cannot replace the shared comparator.

## Nested Layer Policy

Each task may use its own tiny proof/hardening sequence, but nested layers must
not relabel unfinished global L0 work as global L1 readiness. Global promotion
is controlled only by this table and the work-pack gate.

## Recommended Next Layer

- Next layer: L0.
- First unit: `SWU-HALP-001`, freeze the claim boundary and primary estimands in
  one approval-bearing decision record.
- Key decision unlocked: whether the rest of the harness has a stable semantic
  target.
- Major deferred scope: every model invocation and resource claim.
