---
feature: buyer-registry
version: current
status: draft
updatedAt: 2026-05-21
docType: stories
owners:
  - group operator
---

# Buyer Registry Stories

## Story Set

These stories mirror the Buyer Registry capabilities in [SPEC.md](SPEC.md#capabilities) and preserve coverage across public, admin/operations, cross-feature integration, and edge-case journeys.

## BR-S1 Register Buyer For Reservation

Capability: [Buyer Identity Management](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [Buyer](domain.md#buyer), [RegisterBuyer](operations.md#registerbuyer), [ReservationIdentityRule](rules.md#r1--reservation-identity-required)

Classic story:
As a group operator, I want to register a buyer with name, WhatsApp mention, and CPF, so that the buyer can reserve dose slots.

BDD scenario:
Given the operator has a new buyer's name, WhatsApp mention, and CPF
When the operator registers the buyer
Then the buyer is created as `active`
And reservation eligibility is true
And duplicate active CPF or WhatsApp mention is rejected.

Acceptance checks:

- Registering with all required identity fields creates an active buyer.
- Missing name, WhatsApp mention, or CPF blocks registration.
- Duplicate active CPF or WhatsApp mention blocks registration.
- [BuyerRegistered](events.md#buyerregistered) is emitted.

## BR-S2 Search And Select Buyer

Capability: [Buyer Identity Management](SPEC.md#capabilities)
Journey type: public
Concept links: [SearchBuyers](queries.md#searchbuyers), [WhatsApp Mention](domain.md#whatsapp-mention), [Buyer Status](domain.md#buyer-status)

Classic story:
As a group operator, I want to search buyers by name or WhatsApp mention, so that I can quickly select the right buyer during allocation or messaging work.

BDD scenario:
Given active buyers exist in the registry
When the operator searches by name or WhatsApp mention
Then matching active buyer summaries are shown by default
And inactive retained records are excluded unless explicitly included.

Acceptance checks:

- Search matches buyer name or WhatsApp mention.
- Active buyers are the default search scope.
- Inactive retained buyers require the include-retained option.
- Search results expose enough identity to disambiguate buyers without exposing deleted/anonymized PII.

## BR-S3 Update Buyer Identity

Capability: [Buyer Identity Management](SPEC.md#capabilities)
Journey type: admin/operations
Concept links: [UpdateBuyerIdentity](operations.md#updatebuyeridentity), [ActiveBuyerUniquenessRule](rules.md#r3--active-buyer-uniqueness), [BuyerLifecycle](states.md#buyerlifecycle)

Classic story:
As a group operator, I want to correct buyer identity fields, so that downstream allocation and messaging continue to reference the right person.

BDD scenario:
Given an active buyer exists
When the operator updates name, WhatsApp mention, or CPF
Then the buyer remains active
And the updated identity remains reservation eligible
And uniqueness rules are enforced.

Acceptance checks:

- Active buyer identity can be updated without changing lifecycle status.
- Updates cannot remove required reservation identity fields.
- Updates cannot duplicate active CPF or WhatsApp mention.
- Anonymized or deleted buyers cannot be updated.

## BR-S4 Add Shipping Address Before First Shipment

Capability: [Shipping Readiness](SPEC.md#capabilities)
Journey type: cross-feature integration
Concept links: [Shipping Address](domain.md#shipping-address), [SetBuyerShippingAddress](operations.md#setbuyershippingaddress), [CheckBuyerShippingReadiness](queries.md#checkbuyershippingreadiness)

Classic story:
As a group operator, I want to add a buyer's shipping address before the first shipment, so that shipment batching can include that buyer's paid doses.

BDD scenario:
Given an active buyer has reservation identity
When the operator sets a complete shipping address
Then shipping readiness becomes true
And Freight And Shipment Batching can treat the buyer as shipment ready.

Acceptance checks:

- Complete address fields make shipping readiness true.
- Incomplete address fields block shipping readiness.
- Inactive, anonymized, or deleted buyers are not shipment ready.
- [BuyerShippingAddressSet](events.md#buyershippingaddressset) is emitted.

## BR-S5 Expose Reservation Eligibility To Allocation

Capability: [Reservation Eligibility](SPEC.md#capabilities)
Journey type: cross-feature integration
Concept links: [CheckBuyerReservationEligibility](queries.md#checkbuyerreservationeligibility), [BuyerRegistryModule](interfaces.md#internal-buyerregistrymodule-interface), [Bottle Listing And Dose Allocation](../bottle-listing-and-dose-allocation/SPEC.md)

Classic story:
As Bottle Listing And Dose Allocation, I want to check whether a buyer is reservation eligible, so that slots are allocated only to known buyers.

BDD scenario:
Given a downstream allocation request references a buyer
When the allocation feature calls `checkReservationEligibility`
Then the registry returns whether the buyer is active and has required identity
And missing fields are returned when eligibility is false.

Acceptance checks:

- Active buyer with name, WhatsApp mention, and CPF is eligible.
- Inactive, anonymized, or deleted buyer is not eligible.
- Missing identity fields are reported.
- The query is read-only and does not mutate buyer data.

## BR-S6 Mark Buyer Inactive And Resolve Retention

Capability: [Retention Handling](SPEC.md#capabilities)
Journey type: edge-case
Concept links: [MarkBuyerInactive](operations.md#markbuyerinactive), [DeleteOrAnonymizeBuyer](operations.md#deleteoranonymizebuyer), [BuyerRetentionPolicy](rules.md#p1--buyer-retention-policy)

Classic story:
As a group operator, I want to manually mark a buyer inactive and choose delete or anonymize, so that retained PII is handled deliberately.

BDD scenario:
Given an active buyer no longer participates
When the operator marks the buyer inactive
Then reservation and shipment readiness become false
And the operator can choose to anonymize or delete retained PII.

Acceptance checks:

- Only active buyers can be marked inactive.
- Inactive buyers are not reservation eligible or shipment ready.
- Retention action is available only after inactive status.
- Delete removes readable PII.
- Anonymize removes original PII while preserving non-PII operational references.

## Story Coverage Matrix

| Capability                | Stories                                                                                                                        | Coverage                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------- |
| Buyer Identity Management | [BR-S1](#br-s1-register-buyer-for-reservation), [BR-S2](#br-s2-search-and-select-buyer), [BR-S3](#br-s3-update-buyer-identity) | public, admin/operations  |
| Reservation Eligibility   | [BR-S1](#br-s1-register-buyer-for-reservation), [BR-S5](#br-s5-expose-reservation-eligibility-to-allocation)                   | cross-feature integration |
| Shipping Readiness        | [BR-S4](#br-s4-add-shipping-address-before-first-shipment)                                                                     | cross-feature integration |
| Retention Handling        | [BR-S6](#br-s6-mark-buyer-inactive-and-resolve-retention)                                                                      | edge-case                 |

## Concept Coverage Matrix

| Concept                                           | Covered By                 | Notes                                       |
| ------------------------------------------------- | -------------------------- | ------------------------------------------- |
| `buyer-registry.Buyer`                            | BR-S1, BR-S2, BR-S3, BR-S6 | Core entity                                 |
| `buyer-registry.CPF`                              | BR-S1, BR-S3, BR-S6        | Required identity and PII retention         |
| `buyer-registry.WhatsAppMention`                  | BR-S1, BR-S2, BR-S3, BR-S6 | Required identity and lookup                |
| `buyer-registry.ShippingAddress`                  | BR-S4, BR-S6               | Required before first shipment              |
| `buyer-registry.BuyerStatus`                      | BR-S2, BR-S3, BR-S6        | Active/inactive/anonymized/deleted behavior |
| `buyer-registry.BuyerLifecycle`                   | BR-S3, BR-S6               | Lifecycle transitions                       |
| `buyer-registry.RegisterBuyer`                    | BR-S1                      | Registration mutation                       |
| `buyer-registry.UpdateBuyerIdentity`              | BR-S3                      | Identity mutation                           |
| `buyer-registry.SetBuyerShippingAddress`          | BR-S4                      | Shipment readiness mutation                 |
| `buyer-registry.MarkBuyerInactive`                | BR-S6                      | Retention start                             |
| `buyer-registry.DeleteOrAnonymizeBuyer`           | BR-S6                      | Retention terminal action                   |
| `buyer-registry.SearchBuyers`                     | BR-S2                      | Lookup journey                              |
| `buyer-registry.CheckBuyerReservationEligibility` | BR-S5                      | Allocation integration                      |
| `buyer-registry.CheckBuyerShippingReadiness`      | BR-S4                      | Shipment integration                        |
| `buyer-registry.BuyerRegistryAPI`                 | BR-S1, BR-S3, BR-S4, BR-S6 | Operator API                                |
| `buyer-registry.BuyerRegistryModule`              | BR-S5, BR-S4               | Cross-feature contract                      |

## Drift Warnings

No story drift warnings identified.

## Unresolved Questions

No unresolved story questions.
