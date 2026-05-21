---
feature: buyer-registry
version: current
status: draft
updatedAt: 2026-05-20
docType: glossary
---

# Glossary: Buyer Registry

Quick-reference glossary of Buyer Registry language and concepts distilled from the feature specification and aspect documents.

Scope note: This glossary explains feature terms in ordinary product language first, then links each formal concept back to its authoritative source. Authoritative behavior, fields, rules, and lifecycle contracts remain in the linked source documents.

## Feature Language

| Term                    | Meaning in this feature                                                            | Related Concepts                                                                                                                                            |
| ----------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reservation eligibility | Whether a buyer has enough identity data to be used by allocation features.        | [CheckBuyerReservationEligibility](queries.md#checkbuyerreservationeligibility), [Reservation Identity Required](rules.md#r1-reservation-identity-required) |
| Shipping readiness      | Whether a buyer has enough address data to be included in first shipment handling. | [CheckBuyerShippingReadiness](queries.md#checkbuyershippingreadiness), [Shipping Address](domain.md#shipping-address)                                       |
| Retention action        | The operator's manual choice to delete or anonymize inactive buyer PII.            | [Buyer Retention Policy](rules.md#p1-buyer-retention-policy), [DeleteOrAnonymizeBuyer](operations.md#deleteoranonymizebuyer)                                |

## Terms

| Term                             | Concept ID                                        | Type          | Definition                                                                                                   | Source                                                                  |
| -------------------------------- | ------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| Buyer                            | `buyer-registry.Buyer`                            | Entity        | A group participant whose identity and shipping data are managed for reservation and shipment readiness.     | [domain.md](domain.md#buyer)                                            |
| CPF                              | `buyer-registry.CPF`                              | Value Object  | A normalized Brazilian taxpayer identifier required before a buyer can reserve doses.                        | [domain.md](domain.md#cpf)                                              |
| WhatsApp Mention                 | `buyer-registry.WhatsAppMention`                  | Value Object  | The group-visible identifier used to connect a buyer to listings, reminders, and public status text.         | [domain.md](domain.md#whatsapp-mention)                                 |
| Shipping Address                 | `buyer-registry.ShippingAddress`                  | Value Object  | The address data required before a buyer's first shipment, but not before reservation.                       | [domain.md](domain.md#shipping-address)                                 |
| Buyer Status                     | `buyer-registry.BuyerStatus`                      | Enum / Type   | The buyer lifecycle category: active, inactive, anonymized, or deleted.                                      | [domain.md](domain.md#buyer-status)                                     |
| Retention Action                 | `buyer-registry.RetentionAction`                  | Enum / Type   | The operator-selected terminal handling choice for inactive buyer PII.                                       | [domain.md](domain.md#retention-action)                                 |
| BuyerLifecycle                   | `buyer-registry.BuyerLifecycle`                   | State Machine | The lifecycle governing active use, inactive retention handling, and terminal deletion or anonymization.     | [states.md](states.md#buyerlifecycle)                                   |
| ReservationIdentityRule          | `buyer-registry.ReservationIdentityRule`          | Rule          | The rule requiring active status, name, WhatsApp mention, and CPF before reservation eligibility.            | [rules.md](rules.md#r1-reservation-identity-required)                   |
| ShippingAddressRequiredRule      | `buyer-registry.ShippingAddressRequiredRule`      | Rule          | The rule requiring complete shipping address data before shipment readiness.                                 | [rules.md](rules.md#r2-shipping-address-required-before-first-shipment) |
| ActiveBuyerUniquenessRule        | `buyer-registry.ActiveBuyerUniquenessRule`        | Rule          | The rule preventing duplicate active CPF or WhatsApp mention values.                                         | [rules.md](rules.md#r3-active-buyer-uniqueness)                         |
| OperatorManagementRule           | `buyer-registry.OperatorManagementRule`           | Rule          | The v1 access rule limiting Buyer Registry mutations to the operator.                                        | [rules.md](rules.md#r4-operator-management-only-in-v1)                  |
| BuyerRetentionPolicy             | `buyer-registry.BuyerRetentionPolicy`             | Policy        | The policy requiring manual delete or anonymize handling after a buyer is marked inactive.                   | [rules.md](rules.md#p1-buyer-retention-policy)                          |
| RegisterBuyer                    | `buyer-registry.RegisterBuyer`                    | Operation     | The operator action that creates an active buyer with required reservation identity.                         | [operations.md](operations.md#registerbuyer)                            |
| UpdateBuyerIdentity              | `buyer-registry.UpdateBuyerIdentity`              | Operation     | The operator action that changes buyer name, WhatsApp mention, or CPF while preserving required constraints. | [operations.md](operations.md#updatebuyeridentity)                      |
| SetBuyerShippingAddress          | `buyer-registry.SetBuyerShippingAddress`          | Operation     | The operator action that records or replaces the buyer address required for first shipment.                  | [operations.md](operations.md#setbuyershippingaddress)                  |
| MarkBuyerInactive                | `buyer-registry.MarkBuyerInactive`                | Operation     | The operator action that removes a buyer from active eligibility and starts retention handling.              | [operations.md](operations.md#markbuyerinactive)                        |
| DeleteOrAnonymizeBuyer           | `buyer-registry.DeleteOrAnonymizeBuyer`           | Operation     | The operator action that applies the selected terminal retention action to inactive buyer data.              | [operations.md](operations.md#deleteoranonymizebuyer)                   |
| GetBuyer                         | `buyer-registry.GetBuyer`                         | Query         | A read model for the operator-readable buyer profile and derived readiness flags.                            | [queries.md](queries.md#getbuyer)                                       |
| SearchBuyers                     | `buyer-registry.SearchBuyers`                     | Query         | A buyer lookup read model for operator selection and downstream recipient lookup.                            | [queries.md](queries.md#searchbuyers)                                   |
| CheckBuyerReservationEligibility | `buyer-registry.CheckBuyerReservationEligibility` | Query         | A read-only decision contract that tells downstream features whether reservation prerequisites are met.      | [queries.md](queries.md#checkbuyerreservationeligibility)               |
| CheckBuyerShippingReadiness      | `buyer-registry.CheckBuyerShippingReadiness`      | Query         | A read-only decision contract that tells downstream features whether shipment prerequisites are met.         | [queries.md](queries.md#checkbuyershippingreadiness)                    |
| BuyerRegistryAPI                 | `buyer-registry.BuyerRegistryAPI`                 | Interface     | The operator-facing REST boundary for buyer mutations and reads.                                             | [interfaces.md](interfaces.md#external-buyerregistryapi-rest)           |
| BuyerRegistryModule              | `buyer-registry.BuyerRegistryModule`              | Interface     | The internal module boundary consumed by allocation, shipment, and messaging features.                       | [interfaces.md](interfaces.md#internal-buyerregistrymodule-interface)   |
| BuyerRegistered                  | `buyer-registry.BuyerRegistered`                  | Event         | The event emitted when a buyer record is created.                                                            | [events.md](events.md#buyerregistered)                                  |
| BuyerIdentityUpdated             | `buyer-registry.BuyerIdentityUpdated`             | Event         | The event emitted when buyer identity fields change.                                                         | [events.md](events.md#buyeridentityupdated)                             |
| BuyerShippingAddressSet          | `buyer-registry.BuyerShippingAddressSet`          | Event         | The event emitted when a buyer shipping address is set or replaced.                                          | [events.md](events.md#buyershippingaddressset)                          |
| BuyerMarkedInactive              | `buyer-registry.BuyerMarkedInactive`              | Event         | The event emitted when the operator manually marks a buyer inactive.                                         | [events.md](events.md#buyermarkedinactive)                              |
| BuyerDataRemoved                 | `buyer-registry.BuyerDataRemoved`                 | Event         | The event emitted when inactive buyer PII is deleted or anonymized.                                          | [events.md](events.md#buyerdataremoved)                                 |

## Cross-Feature Terms

| Term                               | Concept ID                           | Type             | Definition                                                                            | Source                                                                     |
| ---------------------------------- | ------------------------------------ | ---------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Bottle Listing And Dose Allocation | `bottle-listing-and-dose-allocation` | Feature Boundary | The future feature that consumes reservation eligibility before assigning dose slots. | [PROJECT-DECISIONS.md](../../PROJECT-DECISIONS.md#feature-boundary-sketch) |
| Freight And Shipment Batching      | `freight-and-shipment-batching`      | Feature Boundary | The future feature that consumes shipping readiness before first shipment.            | [PROJECT-DECISIONS.md](../../PROJECT-DECISIONS.md#feature-boundary-sketch) |

## Maintenance Rules

- Derive formal concept rows from [SPEC.md](SPEC.md#concept-registry) and aspect-level concepts.
- Keep each formal concept definition to one domain-level sentence.
- Link every entry to the authoritative source anchor.
- Update this glossary whenever concept names, concept IDs, source anchors, or definitions change.
- Do not introduce new canonical behavior here; update the source aspect document first.
