---
module: investor-business-plan-package
version: current
status: flag
updatedAt: 2026-07-10
docType: implementation-layering
---

# Implementation Layering: Investor Business Plan Package

## Purpose

Define the layer decisions for turning accepted research into a private,
claim-bounded investor business plan package.

## Target And Scope

- Target: DomainSpec/CAV2 private investor BP package.
- Scope: business-plan writing workflow and evidence package.
- Current state: research substrate accepted; final BP not drafted.
- Boundary: private `cyberAlchemy-v2/` business-plan development space only.

## Layer Boundary Rule

After each layer, we know whether the next stronger investor claim is supported
by evidence or must stay demoted.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (Evidence Base) | After this layer, we know whether the BP has a reviewable source registry and claim boundary. | Evidence registry plus source trace. | Accepted findings, maturity labels, non-claims, source-to-section map, missing witnesses. | BP prose, investor memo, deck, financial forecast confidence. | `diligence-evidence-registry.md`, `source-trace.md`, no forbidden claims in registry. | Continue only if every intended BP section has evidence, missing witness, and demotion gate. |
| L1 (Economic Skeleton) | After this layer, we know whether the first wedge can be modeled bottom-up without spreadsheet fantasy. | Financial assumptions and operating plan for one paid wedge. | Sprint units, price ranges, delivery hours, direct costs, capacity, cash timing, use-of-funds placeholders, operating loop. | Validated forecast, platform ARR, lender-ready financial statements. | `financial-assumptions.md`, `operating-plan.md`, sensitivity notes, runway gap called out. | Draft BP only if assumptions are driver-based and labeled. |
| L2 (Investor Narrative) | After this layer, we know whether the story is compelling while preserving claim <= proof. | Full BP draft plus visible evidence boundary. | Executive summary, company, problem, offer, market entry, GTM, operations, team, financials, risks, witness queue. | Deck polish, public copy, certification/compliance claims, proven moat claims. | `business-plan.md` and `claim-audit.md` with no unsupported claim promotion. | Draft memo/deck only if the BP body and audit agree. |
| L3 (Investor Compression And Diligence) | After this layer, we know whether the investor-facing package can be used for first conversations without introducing new claims. | Investor memo and deck substrate tied back to BP/data room. | Memo, deck substrate, decision ask, diligence appendix links, 30/60/90 witness queue. | Public launch, production SaaS claims, token/economy claims, formal certification claims. | `investor-memo.md`, `deck-substrate.md`, final `claim-audit.md`. | Use in investor conversations only with unresolved gaps visible. |

## Non Regression Guardrails

- Later layers must preserve the L0 evidence boundary.
- The deck and memo cannot introduce claims absent from the BP or registry.
- DomainSpec/CAV2 stay private substrate unless a separate public-safe promotion path exists.
- Arcanum public-safe evidence may support claims only where it does not leak private mechanisms.
- Financial projections remain assumptions until paid pilots validate pricing, hours, costs, conversion, and repeat work.
- "Verifiable" and "provable" stay scoped to named checks, receipts, validators, or formal witnesses.
- Standards language remains "informed" or "aware" unless a formal external route has been completed.

## Recommended Next Layer

- Next layer: L0.
- Key decision unlocked: whether the accepted research can support a BP source registry and section-by-section claim boundary.
- Major deferred scope: final investor prose, ask/runway precision, paid-pilot evidence, comparator refresh, and independent Distill validation.
