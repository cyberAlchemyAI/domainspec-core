---
feature: freight-and-shipment-batching
version: current
status: draft
updatedAt: 2026-05-21
docType: interfaces
owners:
  - group operator
---

# Freight And Shipment Batching Interfaces

## External ShipmentBatchingAPI REST

Operator-facing REST surface.

| Endpoint                                                 | Method | Exposes                                                                    | Notes                                              |
| -------------------------------------------------------- | ------ | -------------------------------------------------------------------------- | -------------------------------------------------- |
| `/shipment-batches`                                      | POST   | [CreateShipmentBatch](operations.md#createshipmentbatch)                   | Creates draft shipping wave                        |
| `/shipment-batches/{shipmentBatchId}/packages`           | POST   | [AddWaitingDosesToPackage](operations.md#addwaitingdosestopackage)         | Adds selected waiting doses to a per-buyer package |
| `/buyer-packages/{buyerPackageId}/items/{waitingDoseId}` | DELETE | [RemoveWaitingDoseFromPackage](operations.md#removewaitingdosefrompackage) | Removes an unshipped item from a package           |
| `/buyer-packages/{buyerPackageId}/validate`              | POST   | [ValidateShipmentReadiness](operations.md#validateshipmentreadiness)       | Checks address and dose eligibility                |
| `/buyer-packages/{buyerPackageId}/shipped`               | POST   | [MarkPackageShipped](operations.md#markpackageshipped)                     | Marks package shipped                              |
| `/shipment-batches/{shipmentBatchId}/close`              | POST   | [CloseShipmentBatch](operations.md#closeshipmentbatch)                     | Closes finished batch                              |
| `/waiting-doses`                                         | GET    | [GetWaitingDoseCandidates](queries.md#getwaitingdosecandidates)            | Lists eligible paid waiting doses                  |
| `/shipment-batches/{shipmentBatchId}`                    | GET    | [GetShipmentBatch](queries.md#getshipmentbatch)                            | Reads batch                                        |
| `/shipment-batches`                                      | GET    | [ListShipmentBatches](queries.md#listshipmentbatches)                      | Lists batches                                      |
| `/buyer-packages/{buyerPackageId}`                       | GET    | [GetBuyerPackage](queries.md#getbuyerpackage)                              | Reads package                                      |

## Internal ShipmentBatchingModule Interface

Cross-feature read contract.

| Method                              | Exposes                                                         | Consumer                                    |
| ----------------------------------- | --------------------------------------------------------------- | ------------------------------------------- |
| `getWaitingDoseCandidates(filters)` | [GetWaitingDoseCandidates](queries.md#getwaitingdosecandidates) | Operator UI                                 |
| `getShipmentBatch(shipmentBatchId)` | [GetShipmentBatch](queries.md#getshipmentbatch)                 | Operator UI, Public WhatsApp List Rendering |
| `getBuyerPackage(buyerPackageId)`   | [GetBuyerPackage](queries.md#getbuyerpackage)                   | Operator UI, future freight calculation     |
| `listShipmentBatches(filters)`      | [ListShipmentBatches](queries.md#listshipmentbatches)           | Operator UI                                 |

## Dependency BuyerRegistryModule Interface

Required upstream interface from [Buyer Registry](../buyer-registry/interfaces.md#internal-buyerregistrymodule-interface).

| Method                            | Used By                                                              | Why                                                                        |
| --------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `getBuyer(buyerId)`               | package display                                                      | Reads buyer name and shipping address fields through allowed operator view |
| `checkShippingReadiness(buyerId)` | [ValidateShipmentReadiness](operations.md#validateshipmentreadiness) | Confirms address exists before shipment                                    |

## Dependency BottleListingModule Interface

Required upstream interface from [Bottle Listing And Dose Allocation](../bottle-listing-and-dose-allocation/interfaces.md#internal-bottlelistingmodule-interface).

| Method                                   | Used By                                                         | Why                                                          |
| ---------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------ |
| `getBuyerAllocatedDoses(buyerId)`        | [GetWaitingDoseCandidates](queries.md#getwaitingdosecandidates) | Reads allocated dose ownership and listing/slot traceability |
| `getListingAllocationSummary(listingId)` | candidate filtering and audit                                   | Resolves allocation/slot context when filtering by listing   |

## Dependency PaymentTrackingModule Interface

Required upstream interface from [Dose Payment Tracking](../dose-payment-tracking/interfaces.md#internal-paymenttrackingmodule-interface).

| Method                                    | Used By                                                         | Why                                                         |
| ----------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------- |
| `getBuyerPaymentStatus(buyerId, filters)` | [GetWaitingDoseCandidates](queries.md#getwaitingdosecandidates) | Confirms payment is satisfied before shipment               |
| `getListingPaymentSummary(listingId)`     | candidate filtering by listing                                  | Reads buyer-level paid/unpaid state for listing allocations |
