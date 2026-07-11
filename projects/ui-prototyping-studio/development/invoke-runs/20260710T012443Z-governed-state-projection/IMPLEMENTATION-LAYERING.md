---
id: ui-prototyping-studio-governed-state-projection-layering
project: ui-prototyping-studio
docType: implementation-layering
invoke_run: invoke-20260710T012443Z-governed-state-projection
status: proposed
updatedAt: 2026-07-10T01:24:43Z
---

# Implementation Layering: Governed State Projection

## Target And Scope

- Target: UI Prototyping Studio browser/control projection.
- Scope: brownfield feature architecture and execution plan.
- Current state: reversible state machine exists; browser projection and diff
  evidence are not reliable enough for stronger control-confidence claims.

## Layer Boundary Rule

After this layer, we know whether the named governed-state projection claim is
actually evidenced by a runnable witness.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (projection truth) | After this layer, we know whether accepted/reverted/current head can be the primary browser artifact and annotation target. | `SWU-GSP-001` | Current-head projection, annotation source, external-write witness. | Style diff, action framing, handoff semantics. | Playwright witness: Accept `Go -> Continue`; primary preview + annotation show current head; `/state` reflects external write. | Promote only when the witness passes without manual `/tmp` shims. |
| L1 (diff and action trust) | After this layer, we know whether visible change and durable actions are honestly represented. | `SWU-GSP-002` + `SWU-GSP-003` | Global/style diff lane, Accept/Revert confirmation, mobile/annotation first usability slice. | OD evidence packs, release packaging. | Unit/e2e fixture for CSS/style lane; Playwright action confirmation receipt. | Promote when zero-diff visible mutation is impossible or explicitly marked. |
| L2 (evidence and governance semantics) | After this layer, we know whether validation and handoff semantics preserve claim <= proof. | `SWU-GSP-004` + `SWU-GSP-005` | Deterministic e2e runner, handoff evidence labels, docs/test-count sync. | Human study, trust meter, OD broader profile layer. | Standard e2e command succeeds; handoff missingRefs test; docs match current evidence. | Promote when fresh checked-in proof exists and readiness labels do not overclaim. |
| L3 (profile/evidence extension) | After this layer, we know whether Open Design-inspired evidence can improve candidates without bypassing Studio gates. | `SWU-GSP-006` | Minimal `CraftEvidencePack` behind register/baseline/stage/manifest. | GeneratorProfile, DesignObjectiveBrief, seeds, CritiqueReview, tweak sessions. | Fixture shows required/advisory/subjective buckets and no gate bypass. | Defer broader OD imports until L0-L2 receipts are stable. |

## Non-Regression Guardrails

- Current head is the operator's primary artifact after Accept/Revert.
- Historical variants remain lineage/reference, not the controlled head.
- A visible raw/CSS/style mutation must not be presented as zero change.
- Export confirmation must not imply implementation readiness.
- Open Design structures are evidence/profile helpers, never authority.

## Recommended Next Layer

- Next layer: L0.
- Key decision unlocked: whether the browser can project governed current state.
- First SWU: `SWU-GSP-001`.
