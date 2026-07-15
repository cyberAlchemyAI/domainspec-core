---
mode: validate
budget: validate
status: pass
date: 2026-07-14
---

# Distill Validation

## Object under review

[WORK-PACK.md](./WORK-PACK.md), its split task/SWU files, [IMPLEMENTATION-LAYERING.md](./IMPLEMENTATION-LAYERING.md), and [EXECUTION-PACK.md](./EXECUTION-PACK.md).

## Proposer trace

The smallest coherent route now has two units with different effects:

1. A non-mutating readiness unit verifies exact owner-issued FPR-01/02/03 receipts plus the bounded FPR-04 `Sg`, quotient, and independent retraction, then returns `domainspec-sg-readiness-handle`.
2. The first post-gate mutation unit defines the read-only import/projection contract and discriminating fixtures over that exact two-node/one-edge `Sg`.

Starting with a locally reconstructed graph would test the learning-map schema while bypassing the DomainSpec engine it is meant to dogfood. Starting with UI would hide the same authority error behind presentation. The sequence therefore moves from two independent readiness handles, to import contract, to source-preserving compiler/witness/API, to UI, to independent evidence.

## Balancer trace

The readiness task could become ceremony if it merely restates upstream findings; it remains necessary only because it binds exact identities and runs discriminating consumer-side checks without changing upstream state. The local owner decision could also be confused with graph authority; the task and Dispatch boundaries explicitly forbid that. API, renderer, pilot, and philosophical content would overbuild L0, so they remain later layers or bounded fixtures.

No new subagent dispatch was authorized by the approved refresh. The Proposer/Balancer trace is recorded locally rather than creating an unapproved governed dispatch.

## Resolution

- Pre-L0 has the recorded G-OWNER handle and ends when G-DSV2-SG also passes; neither handle's evidence may waive the other.
- L0 ends at import/projection schema and fixture evidence, not compiler or UI.
- AEO/Financial tables remain learning/source anchors; admitted DomainSpec relations come only from imported `Sg`.
- API is L1 because immutable query behavior is part of the accepted design, but it is one SWU.
- UI is L2 and pilot L3.
- Production website, accounts, scale renderer, and public derivative are deferred.
- Fixed philosophical/Craft content is a witness fixture, not a universal corpus.
- All multi-SWU tasks are sequential and one SWU is selected at a time.

## Checks

| Check | Verdict | Evidence |
|---|---|---|
| Smallest coherent unit | pass | non-mutating exact-`Sg` readiness verification precedes the first mutation unit: import/projection schema plus discriminating fixtures |
| Recomposition proof | pass | [traceability](work-pack/shared/traceability.md) maps every criterion to task/evidence |
| Hidden acceptance gaps | pass with named blocker | G-OWNER and private vocabulary scope are resolved; G-DSV2-SG and exact upstream owner receipts remain explicit |
| Deferred complexity | pass | website, public derivative, accounts, scale renderer, editorial lifecycle named outside active window |
| Navigation to first unit | pass | TASK-IOLM-000 and TASK-IOLM-000B -> two handles -> SWU-IOLM-001-A |
| Write-scope collision | pass | sequential waves and distinct prototype subtrees |
| Authority recomposition | pass | Decision Gate owns projection approval; existing FPR owners emit graph authority; verifier imports read-only; Task Session mutates only prototype scope |

## Premortem

| Failure | Earliest detection | Containment |
|---|---|---|
| Missing/empty `Sg` is treated as success | EGI-008 in SWU-IOLM-000B-A | keep G-DSV2-SG blocked |
| Feature table or local fixture recreates an admitted relation | EGI-010 plus compiler route scan | retain mapping as residue and stop mutation |
| Quotient/retraction evidence is self-confirming | EGI-011 independent mutants | reject the handle and route to the existing FPR owner |
| Local owner decision overreaches into DomainSpec authority | owner-task exclusions and Dispatch boundary | keep gates independent; invalidate handoff |
| Learning/layout material changes semantic identity | double-build and view-independence checks | fail L1 promotion |

## Frame expiry

Re-run Distill if the supported DomainSpec profile, `Sg` contract, quotient/retraction contract, projection owner, prototype root, public/private boundary, or layer decisions change. A new FPR receipt alone does not require re-planning if it satisfies the exact declared handle contract; it requires readiness verification.

## Navigation

- Upstream authority work: existing DomainSpec guard/FPR work-pack route.
- Consumer readiness: [TASK-IOLM-000B](work-pack/tasks/TASK-IOLM-000B-DOMAINSPEC-SG-READINESS.md).
- Local owner decision: [G-OWNER passed](work-pack/shared/G-OWNER-DECISION.md).
- First mutation after both handles: [TASK-IOLM-001](work-pack/tasks/TASK-IOLM-001-CONTRACT.md), `SWU-IOLM-001-A`.

## Verdict

`PASS`: the owner decision recomposes without expanding projection authority, and the plan remains structurally coherent. This is not a readiness pass. `WORK-PACK` correctly remains `BLOCKED` until G-DSV2-SG passes.
