---
module: body-war-suggested-track-ontology-domainspec-integration
version: current
status: plan-ready
updatedAt: 2026-07-27
docType: implementation-layering
---

# Implementation Layering

## Target and Scope

- Target: Body War SuggestedTrack CT-2 ontology/DomainSpec proof track
- Scope: experimental verification workflow
- Current state: CT-2 is implemented and app-tested; ontology and DS-SFOL
  consumer proofs are not implemented

## Boundary Heuristic

Each layer stops after it unlocks one independently reviewable decision.
Later layers must consume receipts from earlier layers instead of copying their
logic.

| Layer | Decision question | Minimum working unit | Included | Deferred | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether Body War can express and validate the CT-2 vocabulary and creation transition as a local ontology fixture. | SWU-BWOI-001 | entry schema, three entries, allowed transition, invalid-transition control | DomainSpec, bridge, promotion | standalone ontology receipt | continue only if entry IDs and digests are stable |
| L1 | After this layer, we know whether canonical Body War `body.logic` can derive CT-2 and detect backend drift without ontology input. | SWU-BWOI-002 | minted nodes, deterministic build, DS-SFOL case, memory adapter, mutation control | bridge, Postgres parity, full lifecycle | standalone DomainSpec proof receipt | continue only if source-derived observation matches backend |
| L2 | After this layer, we know whether exact ontology meaning and exact DomainSpec logic can be composed without becoming duplicate authorities. | SWU-BWOI-003 | bridge schema/validator, positive composition, stale-digest and insufficient-state controls | native node-schema field, promoted ontology, release | integrated proof receipt | accept only experimental candidate-lane claim |
| L3 | After this layer, we know whether the three receipts are reproducible, non-inflated, and navigable for later execution or review. | TASK-BWOI-VERIFY | two-run byte comparison, residue audit, claim-ceiling check, planning/Craft synchronization proposal | publication, deployment, release, promotion | verification report and refresh receipt | close experiment or route named residue |

## Value and Cost

| Layer | Value unlocked | Main cost |
| --- | --- | --- |
| L0 | validates meanings before compiler work | small schema and fixture validator |
| L1 | proves canonical executable rule and drift detection | consumer-local DS-SFOL runner and adapter |
| L2 | proves the ontology/DomainSpec seam is enforced | bridge contract and negative controls |
| L3 | prevents one-off or inflated success claims | reproducibility and lifecycle closeout |

## Non-Regression Guardrails

- L1 must not depend on ontology.
- L2 must not copy `body.logic`.
- A failed L2 cannot rewrite L0 or L1 receipts.
- No layer changes ontology promotion state.
- No layer grants DomainSpec release admission.
- No layer closes the active Strava or geometry project blockers.

## Recommended Next Layer

- Next layer: L0
- Selected unit: SWU-BWOI-001
- Decision unlocked: whether the local ontology fixture can coherently express
  CT-2 with a useful negative control
- Major deferred scope: DomainSpec execution and integration binding

