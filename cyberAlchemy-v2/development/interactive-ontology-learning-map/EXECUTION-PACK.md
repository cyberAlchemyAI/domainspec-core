---
module: interactive-ontology-learning-map
status: blocked
updatedAt: 2026-07-17
docType: execution-pack
---

# Execution Pack

## Applied FPR-02B handoff

This execution pack now expects the BTE consumer-proof handoff and the eventual
integrated manifest. It does not authorize implementation: `G-DSV2-SG` remains
blocked, and one IOLM SWU may be selected only through its existing Task Session
route after exact owner receipts are available.

## Execution rule

This file schedules approved SWUs; it does not authorize them. G-OWNER is recorded and current status is `BLOCKED` on G-DSV2-SG. Prototype SWUs execute sequentially only after the remaining gate passes, unless a task file explicitly proves disjoint write scopes.

## Wave schedule

| Wave | Purpose | Selected unit | Entry gate | Exit |
|---|---|---|---|---|
| [W0](work-pack/waves/W0.md) | independent readiness decisions | 000-A complete; 000B-A pending | upstream work stays with existing FPR owners | persisted G-OWNER handle plus G-DSV2-SG handle |
| [W1](work-pack/waves/W1.md) | import contract and manifest | SWU-IOLM-001-A, then 001-B | G-OWNER and G-DSV2-SG | L0 schema/fixtures pass |
| [W2](work-pack/waves/W2.md) | deterministic read model | 002-A -> 002-B -> 003-A -> 003-B -> 004-A | W1 | immutable witnesses queryable |
| [W3](work-pack/waves/W3.md) | learning UI | 005-A -> 005-B | W2 | parity and journeys pass |
| [W4](work-pack/waves/W4.md) | evidence and private pilot | 006-A -> 006-B | W3 | bounded pilot decision |

## Receipt contract

Every executed SWU returns:

- SWU/task/slice/layer IDs;
- exact files changed;
- validation commands and raw result references;
- acceptance verdict;
- unresolved residue and authority effects;
- non-regression checks;
- next selected SWU or stop reason.

## Stop conditions

- owner or host boundary changes;
- the exact DomainSpec `Sg` is missing, empty, profile/source/graph-mismatched, or lacks its prerequisite receipts;
- a local fixture, feature table, or mapping is used to reconstruct a DomainSpec semantic relation;
- an unapproved local mapping is admitted instead of retained as residue;
- any `Sg -> G -> Sg_canonical` retraction mutant passes;
- candidate vocabulary is treated as canonical without a decision;
- private output enters `arcanum/`;
- rejected relation enters semantic export;
- learning/layout change alters semantic bytes;
- a gate is summarized from another gate's evidence;
- a task needs a wider write scope than its contract;
- public packaging or production integration is pulled into the private witness.

## Recomposition

W0 has returned the G-OWNER handle and still requires the independent G-DSV2-SG handle without mutating the prototype or DomainSpec authority. W1 proves the read-only import/projection contract. W2 imports `Sg` unchanged and builds deterministic derived views around it. W3 proves equivalent learnability surfaces. W4 returns evidence for a private integration/iteration/stop decision. No wave alone constitutes DomainSpec acceptance, publication, or production approval.
