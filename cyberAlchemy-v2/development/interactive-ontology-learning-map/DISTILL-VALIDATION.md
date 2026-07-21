---
mode: validate
budget: validate
status: pass
date: 2026-07-20
---

# Distill Validation

## Object under review

[WORK-PACK.md](./WORK-PACK.md), its split task/SWU files, [IMPLEMENTATION-LAYERING.md](./IMPLEMENTATION-LAYERING.md), and [EXECUTION-PACK.md](./EXECUTION-PACK.md).

## Proposer trace

The posture and proof-role decisions changed the optimization points. The core
projection route has three ordered candidate units and a later independent
authority unit:

1. `SWU-IOLM-00C-A` defines the candidate posture/provenance contract and proves that candidate receipts cannot satisfy an authority gate.
2. `SWU-IOLM-00C-B` compiles the smallest meaningful Craft/CyberAlchemy graph from machine sources and returns a deterministic candidate graph receipt.
3. `SWU-IOLM-00C-C` feeds that graph through one shared read model and proves graph/hierarchy/table parity plus visible candidate posture.
4. The later non-mutating L0A readiness unit verifies owner-issued FPR receipts and returns `domainspec-sg-readiness-handle` for rebind.

The added L0D consumer branch has two independently fresh units:

1. `SWU-IOLM-DSC-A` accepts one exact successful EVF L0 handle, verifies
   identity/provenance/digest, deterministic rebuild, semantic/view invariance,
   parity, and negatives, then emits one narrow non-admitting receipt.
2. `SWU-IOLM-DSC-B` later reruns that contract over one exact green BTE core
   handle with 13 kinds and 16 signatures and emits a distinct breadth receipt.

Starting with project data before the posture guard would let implementation conventions smuggle authority assumptions. Starting with UI would hide that error behind presentation. Requiring the whole compiled graph in 00C-A would bundle independently reviewable contract and compiler behaviors. The sequence therefore starts at the joint posture/provenance boundary, stops after its receipt, then permits deterministic compilation and parity as separate units.

## Balancer trace

The candidate contract could become paperwork if it did not include executable reject fixtures; those fixtures are therefore part of 00C-A. A full vertical UI, API, renderer, pilot, or corpus would overbuild L0C, so the selected unit stops before all of them. The future authority verifier remains necessary because candidate conformance cannot prove FPR identity or retraction. Splitting DSC-A input validation from its projection/parity evidence would hide the causal consumption claim, so they remain one SWU. DSC-B stays separate because it has a different upstream gate, breadth denominator, freshness identity, and terminal consumer.

No new subagent dispatch was authorized by the approved refresh. The Proposer/Balancer trace is recorded locally rather than creating an unapproved governed dispatch.

## Resolution

- L0C began with recorded G-OWNER and G-POSTURE handles; 00C-A passed, and 00C-B is now the only selected unit but remains blocked before mutation on its upstream support receipt.
- L0C ends with candidate contract, deterministic graph, and parity evidence; it does not include full UI, API, pilot, or authoritative labels.
- L0A begins only after G-DSV2-SG and ends with a rebind equivalence or explicit migration proof.
- AEO/Financial tables remain learning/source anchors; admitted DomainSpec relations come only from imported `Sg`.
- API is L1 because immutable query behavior is part of the accepted design, but it is one SWU.
- UI is L2 and pilot L3.
- Production website, accounts, scale renderer, and public derivative are deferred.
- Fixed philosophical/Craft content is a witness fixture, not a universal corpus.
- All multi-SWU tasks are sequential and one SWU is selected at a time.
- L0D is a sibling consumer lane. Its failures cannot rewrite EVF/BTE core verdicts, and its narrow receipt cannot satisfy the breadth slot.

## Checks

| Check | Verdict | Evidence |
|---|---|---|
| Smallest coherent unit | pass | 00C-A owns one behavior: fail-closed candidate posture/provenance and authority separation |
| Recomposition proof | pass | [traceability](work-pack/shared/traceability.md) maps every criterion to task/evidence |
| Hidden acceptance gaps | pass with named later gate | G-OWNER and G-POSTURE are resolved; G-DSV2-SG remains explicit for L0A only |
| Deferred complexity | pass | website, public derivative, accounts, scale renderer, editorial lifecycle named outside active window |
| Navigation to current unit | pass | TASK-IOLM-00C -> W0C -> selected/blocking SWU-IOLM-00C-B; 00C-C and both L0D consumer SWUs remain unselected |
| Write-scope collision | pass | sequential waves and distinct prototype subtrees |
| Authority recomposition | pass | Decision Gate owns projection approval; existing FPR owners emit graph authority; verifier imports read-only; Task Session mutates only prototype scope |
| Consumer atomicity | pass | DSC-A joins one exact EVF handle to one IOLM run/receipt; DSC-B is separate because its BTE stage, denominator, freshness, and downstream join differ |
| Core independence | pass | missing or failed IOLM evidence blocks only its combined claim; EVF/BTE core receipts remain valid on their own |

## Premortem

| Failure | Earliest detection | Containment |
|---|---|---|
| Candidate receipt is relabeled authoritative | 00C-A authority-guard negative | reject the envelope and keep G-DSV2-SG blocked |
| Missing/empty `Sg` is treated as success during L0A | EGI-008 in SWU-IOLM-000B-A | keep authoritative rebind blocked |
| Feature table or local fixture recreates an admitted relation | EGI-010 plus compiler route scan | retain mapping as residue and stop mutation |
| Quotient/retraction evidence is self-confirming | EGI-011 independent mutants | reject the handle and route to the existing FPR owner |
| Local owner decision overreaches into DomainSpec authority | owner-task exclusions and Dispatch boundary | keep gates independent; invalidate handoff |
| Learning/layout material changes semantic identity | double-build and view-independence checks | fail L1 promotion |
| IOLM self-authors upstream evidence or substitutes a narrow receipt for breadth | contract owner/stage/digest checks plus DSC-B 13/16 constants | reject the receipt and preserve the upstream core result |

## Frame expiry

Re-run Distill if the candidate source contract, normalized graph boundary, supported DomainSpec profile, `Sg` contract, evidence-consumer contract/schema, upstream stage shape, rebind identity policy, projection owner, prototype root, public/private boundary, or layer decisions change. A new conforming upstream receipt alone does not require re-planning; it requires exact readiness/consumer verification.

## Navigation

- Active blocked unit: [TASK-IOLM-00C](work-pack/tasks/TASK-IOLM-00C-CANDIDATE-SUBSTRATE.md), `SWU-IOLM-00C-B` only after its upstream support receipt.
- Consumer lane: [TASK-IOLM-DOMAINSPEC-EVIDENCE-CONSUMER](work-pack/tasks/TASK-IOLM-DOMAINSPEC-EVIDENCE-CONSUMER.md); both SWUs are unselected.
- Upstream authority work: independent existing DomainSpec FPR work-pack route.
- Consumer readiness: [TASK-IOLM-000B](work-pack/tasks/TASK-IOLM-000B-DOMAINSPEC-SG-READINESS.md).
- Local owner decision: [G-OWNER passed](work-pack/shared/G-OWNER-DECISION.md).
- Later authority mutation after G-DSV2-SG: L0A rebind through the same normalized boundary.

## Verdict

`PASS`: the code-first and two-proof decisions recompose without expanding projection or DomainSpec authority. The smallest coherent consumer unit is `SWU-IOLM-DSC-A`, but it remains blocked/unselected behind the candidate substrate and exact EVF receipt. This is not an implementation receipt, does not lower G-DSV2-SG, and does not change either upstream core verdict.
