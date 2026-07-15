---
module: domainspec-v2-foundation-execution
version: current
status: planned
updatedAt: 2026-07-14
docType: invoke-plan
---

# Invoke Plan: DomainSpec v2 Foundation Execution

## Verdict

The route now has an execution-grade, split work-pack for guard repair and `FPR-01..04`. Only the first SWU is currently selectable. The plan does not make the whole roadmap executable and does not authorize mutation.

## Control Decision

| Field | Value |
|---|---|
| Complexity | high |
| Output mode | split |
| Active layer | L0 |
| First selected unit | `SWU-SGRM-006-R1` |
| First execution owner | Task Session, local fallback, SGRM plan-owner review |
| Continuation authority | `projects/domainspec-v2/.craft/ledger.yml` |
| Release state | production unauthorized |

## Delivery Boundary

Included:

- reopen the live SGRM guard proof without replacing its identities;
- ratify one non-contradictory authority baseline;
- freeze one exact backend supported profile;
- resolve ontology/spec direction and emit a governed `B -> Spec` map;
- prove the smallest authoritative `Spec -> Sg -> G -> Sg_canonical` slice.

Excluded:

- FPR-05 onward, broad graph coverage, full DomainSpec UI, hosted/public product, arbitrary generation, universal equivalence, release authorization, and implementation of this plan during Invoke.

## Ordered Route

| Order | Node | Outcome | Entry gate | Exit evidence |
|---:|---|---|---|---|
| 0 | SGRM-006/007 retry | Current guard proves zero active retired-orchestration references | four live violations are reviewable | exact disposition packet, clean report, seeded failure, digest-drift failure |
| 1 | FPR-01 | One owner-ratified authority baseline | guard is green | baseline, deterministic drift validator, owner receipt, count/path/status mutants |
| 2 | FPR-02 | One exact supported profile and stable digest | FPR-01 receipt verifies | product/profile/pilot matrices, validator, stable digest, red fixtures |
| 3 | FPR-03 | One governed business plane and total `B -> Spec` map | FPR-02 digest verifies and direction decision is accepted | decision, BO/BK/B manifests, total map, typed negatives |
| 4 | FPR-04 | One authoritative two-node/one-edge `Sg` and bounded independent retraction | FPR-03 receipt verifies | source manifest, schemas, Sg, G, quotient registry, independent comparator, mutants |

## Lifecycle Ownership

- Invoke owns this plan only.
- Task Session owns one selected SWU at a time and must build its context pack at execution time.
- Decision Gate owns unresolved owner choices in FPR-01, FPR-02, and FPR-03.
- Definitions Governance owns canonical definition/count promotion.
- Ontology Harness plus semantic owners own FPR-03 mapping governance.
- Semantic, validation, and engine owners jointly own FPR-04; the compiler cannot own its own oracle.
- Craft remains the sole continuation state owner. Registration/status mutation is a separate approved action.

## Handoff Rule

Start with `SWU-SGRM-006-R1`. Do not select `SWU-SGRM-007-R1` until every match in the four violating files has a reviewed disposition. Do not start an FPR task merely because an earlier validator happens to be green; require its named receipt.

## Package Navigation

- [Work pack](WORK-PACK.md)
- [Execution pack](EXECUTION-PACK.md)
- [Implementation layering](IMPLEMENTATION-LAYERING.md)
- [Dispatch](DISPATCH.json)
- [Distill validation](DISTILL-VALIDATION.md)
- [Plan transport](PLAN-TRANSPORT.md)
- [Planning context](PLANNING-CONTEXT.md)

