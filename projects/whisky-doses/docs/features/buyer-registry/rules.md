# Rules: Buyer Registry

This file declares the buyer identity, shipment-readiness, uniqueness, access, and retention contracts that downstream feature specs must consume.

## R1 — Reservation Identity Required

A [Buyer](domain.md#buyer) is eligible for reservation only when the buyer is [active](domain.md#buyer-status) and has [Buyer](domain.md#buyer).name, [Buyer](domain.md#buyer).whatsAppMention, and [Buyer](domain.md#buyer).cpf.

**Applies To:** [CheckBuyerReservationEligibility](queries.md#checkbuyerreservationeligibility), [RegisterBuyer](operations.md#registerbuyer), [UpdateBuyerIdentity](operations.md#updatebuyeridentity).

**Formal:**

```text
reservationEligible(buyer) =
  buyer.status == active
  && present(buyer.name)
  && present(buyer.whatsAppMention)
  && present(buyer.cpf)
```

## R2 — Shipping Address Required Before First Shipment

A [Buyer](domain.md#buyer) is shipment-ready only when the buyer is [active](domain.md#buyer-status), reservation eligible under [R1](#r1-reservation-identity-required), and has a complete [Shipping Address](domain.md#shipping-address).

**Applies To:** [SetBuyerShippingAddress](operations.md#setbuyershippingaddress), [CheckBuyerShippingReadiness](queries.md#checkbuyershippingreadiness).

**Formal:**

```text
shippingReady(buyer) =
  reservationEligible(buyer)
  && present(buyer.shippingAddress.recipientName)
  && present(buyer.shippingAddress.streetLine1)
  && present(buyer.shippingAddress.city)
  && present(buyer.shippingAddress.state)
  && present(buyer.shippingAddress.postalCode)
  && present(buyer.shippingAddress.country)
```

## R3 — Active Buyer Uniqueness

No two active [Buyer](domain.md#buyer) records may share the same normalized [CPF](domain.md#cpf) or normalized [WhatsApp Mention](domain.md#whatsapp-mention).

**Applies To:** [RegisterBuyer](operations.md#registerbuyer), [UpdateBuyerIdentity](operations.md#updatebuyeridentity).

**Formal:**

```text
∀ a,b ∈ Buyers:
  a.id != b.id && a.status == active && b.status == active
    -> a.cpf != b.cpf && a.whatsAppMention != b.whatsAppMention
```

## R4 — Operator Management Only In V1

Only the [group operator](../../PROJECT-OVERVIEW.md#actors-and-stakeholders) can execute Buyer Registry mutations in v1. Buyer self-service access is deferred.

**Applies To:** [BuyerRegistryAPI](interfaces.md#external-buyerregistryapi-rest), [RegisterBuyer](operations.md#registerbuyer), [UpdateBuyerIdentity](operations.md#updatebuyeridentity), [SetBuyerShippingAddress](operations.md#setbuyershippingaddress), [MarkBuyerInactive](operations.md#markbuyerinactive), [DeleteOrAnonymizeBuyer](operations.md#deleteoranonymizebuyer).

**Formal:**

```text
mutationAllowed(actor, operation) =
  actor.role == group_operator
  && operation ∈ buyerRegistryMutations
```

## P1 — Buyer Retention Policy

[Buyer](domain.md#buyer) data is retained while the buyer is active. When the operator manually marks a buyer inactive, the operator must choose whether to delete or anonymize the buyer's retained PII before the lifecycle can reach a terminal retention state.

**Applies To:** [MarkBuyerInactive](operations.md#markbuyerinactive), [DeleteOrAnonymizeBuyer](operations.md#deleteoranonymizebuyer), [BuyerLifecycle](states.md#buyerlifecycle).

### Decision Table

| Condition                                        | Selected Behavior                                                                     | Notes                                                   |
| ------------------------------------------------ | ------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| [Buyer](domain.md#buyer).status is `active`      | Retain identity and shipping data                                                     | Buyer remains usable by downstream features             |
| Operator marks [Buyer](domain.md#buyer) inactive | Set status to `inactive` and keep data temporarily                                    | Manual step creates explicit retention decision point   |
| Operator selects `anonymize`                     | Replace PII fields with irreversible anonymized values and set status to `anonymized` | Preserves non-PII operational references when needed    |
| Operator selects `delete`                        | Remove retained buyer PII and set status to `deleted`                                 | Downstream features must not rely on PII after deletion |

## Invariants

| ID  | Invariant                                                                                                                                                                           | Formal                                                                                                           |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| I1  | A `deleted` [Buyer](domain.md#buyer) must not expose [CPF](domain.md#cpf), [WhatsApp Mention](domain.md#whatsapp-mention), or [Shipping Address](domain.md#shipping-address) values | `buyer.status == deleted -> buyer.cpf == null && buyer.whatsAppMention == null && buyer.shippingAddress == null` |
| I2  | An `anonymized` [Buyer](domain.md#buyer) must not expose original PII values                                                                                                        | `buyer.status == anonymized -> originalPIIReadable(buyer) == false`                                              |
| I3  | An inactive [Buyer](domain.md#buyer) is not reservation eligible or shipment ready                                                                                                  | `buyer.status == inactive -> reservationEligible(buyer) == false && shippingReady(buyer) == false`               |
