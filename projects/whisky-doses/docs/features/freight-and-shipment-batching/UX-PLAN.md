---
feature: freight-and-shipment-batching
version: current
status: draft
updatedAt: 2026-05-21
docType: ux-plan
owners:
  - group operator
sources:
  - SPEC.md
  - STORIES.md
  - UI-SPEC.md
  - ../../UI-ARCHITECTURE.md
invoke_adapter: unavailable
---

# Freight And Shipment Batching UX Plan

## Invocation Note

Local Arcanum invoke adapter was unavailable in this workspace; this UX plan was authored directly from SPEC.md, STORIES.md, UI-SPEC.md, and UI-ARCHITECTURE.md.

## UX Intent

Make shipment planning feel like assembling a clean shipping wave from eligible paid waiting doses, with blockers visible before the operator can mark anything shipped.

Primary user: group operator.

Primary outcomes:

- identify paid waiting doses
- create shipment batch
- group doses into per-buyer packages
- validate address and eligibility blockers
- mark packages shipped and close batch

## Experience Principles

- Eligibility before action: unpaid, unready, already-packaged, or shipped doses should be filtered or clearly blocked.
- Package ownership must be obvious: one package equals one buyer.
- Readiness blockers should be actionable: missing address should point back to Buyer Registry.
- Keep freight out: no freight quote, freight payment, or carrier-label UX in v1.

## Primary Flow

1. Operator opens `/shipments`.
2. UI shows paid waiting dose candidates and readiness blockers.
3. Operator creates a shipment batch.
4. Operator opens batch detail and groups selected waiting doses into per-buyer packages.
5. Operator validates package readiness.
6. Operator marks ready packages shipped.
7. Operator closes batch when packages are shipped or cancelled.

UX success criteria:

- operator can see why a dose is or is not eligible
- package contents preserve listing, allocation, and slot traceability
- blocked packages explain exactly what must be fixed

## Secondary Flows

### Remove Before Shipment

1. Operator opens buyer package.
2. Operator removes unshipped waiting dose.
3. Dose returns to candidates if still eligible.

### Future Freight Preparation

1. UI keeps package content and readiness structured.
2. Future freight quote flow can consume package composition without changing v1 shipment planning.

## Screen Plan

| Screen                         | UX Role                       | Key Decisions                            |
| ------------------------------ | ----------------------------- | ---------------------------------------- |
| `/shipments`                   | Shipment planning entry point | Show waiting candidates above batch list |
| `/shipments/{shipmentBatchId}` | Batch assembly workspace      | Add-to-package panel plus package table  |

## Interaction Details

- Primary action on shipments: "Create Shipment Batch".
- Candidate table shows buyer, listing, slots, paid status, address readiness, and waiting age.
- Add-to-package flow must prevent mixed-buyer selection.
- Package actions: validate readiness, remove item, mark shipped.
- Close batch disabled until all packages are shipped or cancelled.

## Edge And Empty States

| State                 | UX Response                                                  |
| --------------------- | ------------------------------------------------------------ |
| No waiting doses      | Empty state explaining paid unshipped doses will appear here |
| Missing address       | Block package readiness and link to buyer detail             |
| Unpaid dose selected  | Block packaging and identify payment status source           |
| Dose already packaged | Explain active package assignment                            |
| Freight requested     | Explain freight calculation/payment is outside v1            |

## Cross-Feature Handoffs

| Handoff                                 | UX Contract                                                                                |
| --------------------------------------- | ------------------------------------------------------------------------------------------ |
| From Dose Payment Tracking              | Only paid obligations produce shipment candidates; unpaid status remains a blocker         |
| From Buyer Registry                     | Address readiness is checked from buyer data and links back to buyer detail for correction |
| From Bottle Listing And Dose Allocation | Package contents preserve listing, allocation, and slot traceability                       |

## UX Validation Checklist

- [ ] Waiting candidate list includes only paid, unshipped dose obligations or explains why candidates are blocked.
- [ ] Per-buyer package grouping prevents mixed-buyer packages.
- [ ] Missing address blockers link back to Buyer Registry.
- [ ] Mark-shipped is unavailable until package readiness passes.
- [ ] Freight quote, freight payment, and carrier label work are clearly outside v1.

## Iteration Notes

- Do not calculate freight amounts.
- Do not require freight payment before shipped state.
- Do not mutate listing allocation or dose payment truth.
- Future public shipment transparency can consume batch/package status.
