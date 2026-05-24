---
feature: freight-and-shipment-batching
version: current
status: draft
updatedAt: 2026-05-21
docType: stories
owners:
  - group operator
---

# Freight And Shipment Batching Stories

## Story Set

These stories mirror the Freight And Shipment Batching capabilities in [SPEC.md](SPEC.md#capabilities) and preserve coverage across public, admin/operations, cross-feature integration, and edge-case journeys.

## FS-S1 Identify Paid Waiting Doses

Capability: [Waiting Dose Identification](SPEC.md#capabilities)
Journey type: cross-feature integration
Concept links: [Waiting Dose](domain.md#waiting-dose), [GetWaitingDoseCandidates](queries.md#getwaitingdosecandidates), [ShipmentEligibilityRule](rules.md#r1-shipment-eligibility-rule)

Classic story:
As a group operator, I want to see paid allocated doses that are not shipped or already packaged, so that I can decide what belongs in a shipment wave.

BDD scenario:
Given buyers have allocated doses across listings
When the operator lists waiting dose candidates
Then only active allocated, payment-satisfied, unshipped, unpackaged doses are shown
And buyer shipping readiness blockers are visible.

Acceptance checks:

- Active allocation comes from Bottle Listing And Dose Allocation.
- Paid/satisfied status comes from Dose Payment Tracking.
- Shipping readiness comes from Buyer Registry.
- Unpaid, shipped, or already packaged doses are excluded.

## FS-S2 Create Shipment Batch

Capability: [Shipping Wave Composition](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [Shipment Batch](domain.md#shipment-batch), [CreateShipmentBatch](operations.md#createshipmentbatch), [BatchCompositionPolicy](rules.md#p1-batch-composition-policy)

Classic story:
As a group operator, I want to create a draft shipment batch, so that I can plan a shipping wave before packages are ready.

BDD scenario:
Given the operator is ready to plan shipping
When the operator creates a shipment batch
Then the batch starts as `draft`
And packages can be added by buyer.

Acceptance checks:

- Draft batch is created with optional title/note.
- [ShipmentBatchCreated](events.md#shipmentbatchcreated) is emitted.
- Batch does not require freight amount or freight payment in v1.

## FS-S3 Package Waiting Doses By Buyer

Capability: [Per-Buyer Package Management](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [Buyer Package](domain.md#buyer-package), [AddWaitingDosesToPackage](operations.md#addwaitingdosestopackage), [PackageOwnershipRule](rules.md#r2-package-ownership-rule)

Classic story:
As a group operator, I want to group selected waiting doses into per-buyer packages, so that each package contains only one buyer's paid waiting doses across listings.

BDD scenario:
Given a draft shipment batch exists
And selected waiting doses belong to the same buyer
When the operator adds them to a package
Then a buyer package is created or updated
And package line items preserve listing, allocation, and slot traceability.

Acceptance checks:

- Package contains doses for exactly one buyer.
- Package can include that buyer's paid waiting doses across multiple listings.
- Waiting dose cannot appear in another active package.
- [WaitingDosePackaged](events.md#waitingdosepackaged) is emitted for added doses.

## FS-S4 Validate Shipment Readiness

Capability: [Shipping Readiness Gate](SPEC.md#capabilities)
Journey type: edge-case
Concept links: [Shipping Readiness Check](domain.md#shipping-readiness-check), [ValidateShipmentReadiness](operations.md#validateshipmentreadiness), [ShippingAddressRequiredRule](rules.md#r3-shipping-address-required-rule)

Classic story:
As a group operator, I want package readiness validation to show address and eligibility blockers, so that packages are not shipped before buyer readiness is complete.

BDD scenario:
Given a buyer package exists
When the operator validates shipment readiness
Then the package becomes `ready` if it has eligible waiting doses and buyer shipping readiness
Or becomes `blocked` with reasons when address or eligibility is missing.

Acceptance checks:

- Buyer address readiness comes from Buyer Registry.
- Package with missing address becomes blocked.
- Package with no eligible waiting doses becomes blocked.
- Freight payment is not part of readiness in v1.

## FS-S5 Mark Package Shipped And Close Batch

Capability: [Shipment Progress Tracking](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [MarkPackageShipped](operations.md#markpackageshipped), [CloseShipmentBatch](operations.md#closeshipmentbatch), [PackageShipmentStatusLifecycle](states.md#packageshipmentstatuslifecycle)

Classic story:
As a group operator, I want to mark ready packages shipped and close the batch when all packages are finished, so that shipped doses leave the waiting pool.

BDD scenario:
Given all package blockers are resolved
When the operator marks a package shipped
Then the package becomes `shipped`
And its waiting doses are no longer candidates
And the batch can close after every package is shipped or cancelled.

Acceptance checks:

- Only ready packages can be marked shipped.
- Shipped package line items leave the waiting dose candidate pool.
- Batch cannot close while packages remain planned, blocked, or ready.
- [PackageMarkedShipped](events.md#packagemarkedshipped) and [ShipmentBatchClosed](events.md#shipmentbatchclosed) are emitted.

## FS-S6 Remove Dose From Package Before Shipment

Capability: [Per-Buyer Package Management](SPEC.md#capabilities)
Journey type: edge-case
Concept links: [RemoveWaitingDoseFromPackage](operations.md#removewaitingdosefrompackage), [Waiting Dose](domain.md#waiting-dose), [Package Shipment Status](domain.md#package-shipment-status)

Classic story:
As a group operator, I want to remove an unshipped waiting dose from a package, so that corrections can be made before shipment.

BDD scenario:
Given a package is not shipped
When the operator removes a waiting dose from the package
Then the dose becomes available for future package selection again.

Acceptance checks:

- Shipped packages cannot have waiting doses removed.
- Removing an item does not mutate listing allocation or payment truth.
- Removed waiting dose can appear in candidate selection again if still eligible.

## Story Coverage Matrix

| Capability                   | Stories                                                                                                  | Coverage                    |
| ---------------------------- | -------------------------------------------------------------------------------------------------------- | --------------------------- |
| Waiting Dose Identification  | [FS-S1](#fs-s1-identify-paid-waiting-doses)                                                              | cross-feature integration   |
| Shipping Wave Composition    | [FS-S2](#fs-s2-create-shipment-batch)                                                                    | admin/operations            |
| Per-Buyer Package Management | [FS-S3](#fs-s3-package-waiting-doses-by-buyer), [FS-S6](#fs-s6-remove-dose-from-package-before-shipment) | admin/operations, edge-case |
| Shipping Readiness Gate      | [FS-S4](#fs-s4-validate-shipment-readiness)                                                              | edge-case                   |
| Shipment Progress Tracking   | [FS-S5](#fs-s5-mark-package-shipped-and-close-batch)                                                     | admin/operations            |
| Shipment Transparency        | [FS-S5](#fs-s5-mark-package-shipped-and-close-batch)                                                     | public                      |

## Concept Coverage Matrix

| Concept                                                        | Covered By                        | Notes                                   |
| -------------------------------------------------------------- | --------------------------------- | --------------------------------------- |
| `freight-and-shipment-batching.WaitingDose`                    | FS-S1, FS-S3, FS-S5, FS-S6        | Candidate and package item              |
| `freight-and-shipment-batching.ShipmentBatch`                  | FS-S2, FS-S5                      | Shipping wave                           |
| `freight-and-shipment-batching.BuyerPackage`                   | FS-S3, FS-S4, FS-S5, FS-S6        | Per-buyer package                       |
| `freight-and-shipment-batching.PackageLineItem`                | FS-S3, FS-S5                      | Listing/allocation/slot traceability    |
| `freight-and-shipment-batching.ShippingReadinessCheck`         | FS-S4                             | Address/eligibility gate                |
| `freight-and-shipment-batching.ShipmentBatchStatusLifecycle`   | FS-S2, FS-S5                      | Batch status                            |
| `freight-and-shipment-batching.PackageShipmentStatusLifecycle` | FS-S4, FS-S5, FS-S6               | Package status                          |
| `freight-and-shipment-batching.CreateShipmentBatch`            | FS-S2                             | Batch creation                          |
| `freight-and-shipment-batching.AddWaitingDosesToPackage`       | FS-S3                             | Package composition                     |
| `freight-and-shipment-batching.RemoveWaitingDoseFromPackage`   | FS-S6                             | Correction                              |
| `freight-and-shipment-batching.ValidateShipmentReadiness`      | FS-S4                             | Readiness gate                          |
| `freight-and-shipment-batching.MarkPackageShipped`             | FS-S5                             | Shipment progress                       |
| `freight-and-shipment-batching.CloseShipmentBatch`             | FS-S5                             | Batch closure                           |
| `freight-and-shipment-batching.ShipmentBatchingAPI`            | FS-S2, FS-S3, FS-S4, FS-S5, FS-S6 | Operator API                            |
| `freight-and-shipment-batching.ShipmentBatchingModule`         | FS-S1, FS-S5                      | Operator/rendering/future freight reads |

## Drift Warnings

No story drift warnings identified.

## Unresolved Questions

No unresolved story questions.
