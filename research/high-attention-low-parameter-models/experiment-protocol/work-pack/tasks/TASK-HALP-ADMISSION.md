---
taskId: TASK-HALP-ADMISSION
docType: work-pack-task
status: blocked-human-resource
layer: L1
slice: S-002
---

# TASK-HALP-ADMISSION — Model Stack And Capacity

## Objective

Admit only exact checkpoint/runtime/length tuples proven compatible and resident
under the approved policy.

Related context: [shared execution context](../shared/context.md),
[cross-task gaps](../shared/cross-task-gaps.md), and
[traceability](../shared/traceability.md).

## Smallest Working Units

### SWU-HALP-009

- Primary behavior: produce model-stack, compatibility, and per-length capacity
  receipts that together admit explicit cells.
- Acceptance boundary: an admission record for each exact cell; no partial
  stack-level assumption.
- Split analysis: compatibility and capacity are distinct probes but neither
  independently authorizes a cell, so they share one admission SWU.
- Dependencies: SWU 003–006; hardware/resource authorization.
- Source anchors: `operations.md#admitmodelstack`, `domain.md#modelstack`,
  `domain.md#capacitywitness`, findings platform section.
- Related context: platform decision record and evidence-state policy.
- Write scope: `src/admission/`, `manifests/model-stacks/`, `capacity/`,
  admission-only smoke outputs.

### Implementation Detail

1. Resolve authorized immutable snapshots and inventory every file/hash.
2. Bind tokenizer and chat-template identity; render a known smoke fixture.
3. Record runtime image, packages, backend/chunk settings, precision, KV policy,
   hardware, driver, and CUDA identities.
4. For each model/length cell, render exact post-template input and verify fit.
5. Execute capacity probe while recording allocation/high-water telemetry.
6. Assert no truncation, offload, preemption, fallback, recomputation, hidden
   retry, or OOM recovery.
7. Emit `admitted` or one typed rejection reason per cell.

Edge cases: gated checkpoint unavailable, tokenizer drift, unsupported
architecture despite documentation, backend silently changes attention path,
hardware contention, long cell fits allocation but fails prefill/decode.

### Acceptance

- Done: every primary candidate cell has admitted/rejected receipt; at least one
  long-bin cell is admitted to proceed to L1 smoke.
- Evidence: stack manifests, smoke receipts, capacity witnesses.
- Validation: `node src/admission/validate-admission.mjs manifests/model-stacks capacity` plus manual telemetry review.
- Execution owner: local fallback on authorized hardware.
- Handoff note: this SWU may download/access models only under the approved
  license/cache boundary; it must not launch the experiment matrix.

## Synchronization

Update matrix eligibility and blockers; never change requested lengths silently
to make admission pass.
