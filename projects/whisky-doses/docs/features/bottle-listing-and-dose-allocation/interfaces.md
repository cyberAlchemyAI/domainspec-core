---
feature: bottle-listing-and-dose-allocation
version: current
status: draft
updatedAt: 2026-05-21
docType: interfaces
owners:
  - group operator
---

# Bottle Listing And Dose Allocation Interfaces

## External BottleListingAPI REST

Operator-facing REST surface.

| Endpoint                              | Method | Exposes                                                  | Notes                                 |
| ------------------------------------- | ------ | -------------------------------------------------------- | ------------------------------------- |
| `/listings`                           | POST   | [CreateBottleListing](operations.md#createbottlelisting) | Creates draft listing                 |
| `/listings/{listingId}/open`          | POST   | [OpenBottleListing](operations.md#openbottlelisting)     | Opens reservations                    |
| `/listings/{listingId}/allocations`   | POST   | [AllocateDoseSlots](operations.md#allocatedoseslots)     | Allocates slots to one eligible buyer |
| `/allocations/{allocationId}/release` | POST   | [ReleaseDoseSlots](operations.md#releasedoseslots)       | Releases selected allocated slots     |
| `/listings/{listingId}/close`         | POST   | [CloseBottleListing](operations.md#closebottlelisting)   | Closes listing                        |
| `/listings/{listingId}`               | GET    | [GetBottleListing](queries.md#getbottlelisting)          | Reads listing                         |
| `/listings/open`                      | GET    | [ListOpenListings](queries.md#listopenlistings)          | Reads open listing summaries          |

## Internal BottleListingModule Interface

Cross-feature read contract.

| Method                                      | Exposes                                                                   | Consumer                                              |
| ------------------------------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------- |
| `getListingAllocationSummary(listingId)`    | [GetListingAllocationSummary](queries.md#getlistingallocationsummary)     | Public WhatsApp List Rendering, Dose Payment Tracking |
| `getPaymentEligibleAllocations(listingIds)` | [GetPaymentEligibleAllocations](queries.md#getpaymenteligibleallocations) | Dose Payment Tracking                                 |
| `getBuyerAllocatedDoses(buyerId)`           | [GetBuyerAllocatedDoses](queries.md#getbuyerallocateddoses)               | Freight And Shipment Batching                         |

Boundary rules:

- Consumers may read allocation state but cannot mutate slots.
- Payment consumers may derive owed amounts from listing price and allocations but cannot alter listing state.
- Rendering consumers may display buyer-level slot and payment snippets but payment truth comes from Dose Payment Tracking.

## Dependency BuyerRegistryModule Interface

Required upstream interface from [Buyer Registry](../buyer-registry/interfaces.md#internal-buyerregistrymodule-interface).

| Method                                   | Used By                                              | Why                                                                |
| ---------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------ |
| `checkReservationEligibility(buyerId)`   | [AllocateDoseSlots](operations.md#allocatedoseslots) | Buyer must have name, WhatsApp mention, and CPF before reservation |
| `getBuyer(buyerId)` or lookup equivalent | listing reads/rendering preparation                  | Buyer mention is needed for human-readable allocation rows         |
