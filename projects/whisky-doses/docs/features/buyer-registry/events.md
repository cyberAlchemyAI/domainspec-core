# Events: Buyer Registry

This file defines domain events emitted by Buyer Registry operations.

## BuyerRegistered

**Produced by:** [RegisterBuyer](operations.md#registerbuyer)
**Source Entity:** [Buyer](domain.md#buyer)

| Field      | Type                         | Description               |
| ---------- | ---------------------------- | ------------------------- |
| buyerId    | [BuyerId](domain.md#buyerid) | Registered buyer identity |
| occurredAt | timestamp                    | Time the event occurred   |

**Transitions:** [BuyerLifecycle](states.md#buyerlifecycle) from none to `active`.

## BuyerIdentityUpdated

**Produced by:** [UpdateBuyerIdentity](operations.md#updatebuyeridentity)
**Source Entity:** [Buyer](domain.md#buyer)

| Field         | Type                         | Description             |
| ------------- | ---------------------------- | ----------------------- |
| buyerId       | [BuyerId](domain.md#buyerid) | Updated buyer identity  |
| changedFields | string[]                     | Changed identity fields |
| occurredAt    | timestamp                    | Time the event occurred |

**Transitions:** [BuyerLifecycle](states.md#buyerlifecycle) from `active` to `active`.

## BuyerShippingAddressSet

**Produced by:** [SetBuyerShippingAddress](operations.md#setbuyershippingaddress)
**Source Entity:** [Buyer](domain.md#buyer)

| Field      | Type                         | Description                 |
| ---------- | ---------------------------- | --------------------------- |
| buyerId    | [BuyerId](domain.md#buyerid) | Buyer whose address changed |
| occurredAt | timestamp                    | Time the event occurred     |

**Transitions:** [BuyerLifecycle](states.md#buyerlifecycle) from `active` to `active`.

## BuyerMarkedInactive

**Produced by:** [MarkBuyerInactive](operations.md#markbuyerinactive)
**Source Entity:** [Buyer](domain.md#buyer)

| Field      | Type                         | Description             |
| ---------- | ---------------------------- | ----------------------- |
| buyerId    | [BuyerId](domain.md#buyerid) | Buyer marked inactive   |
| reason     | string                       | Optional operator note  |
| occurredAt | timestamp                    | Time the event occurred |

**Transitions:** [BuyerLifecycle](states.md#buyerlifecycle) from `active` to `inactive`.

## BuyerDataRemoved

**Produced by:** [DeleteOrAnonymizeBuyer](operations.md#deleteoranonymizebuyer)
**Source Entity:** [Buyer](domain.md#buyer)

| Field           | Type                                           | Description                                         |
| --------------- | ---------------------------------------------- | --------------------------------------------------- |
| buyerId         | [BuyerId](domain.md#buyerid)                   | Buyer whose retained data was removed or anonymized |
| retentionAction | [Retention Action](domain.md#retention-action) | `delete` or `anonymize`                             |
| occurredAt      | timestamp                                      | Time the event occurred                             |

**Transitions:** [BuyerLifecycle](states.md#buyerlifecycle) from `inactive` to `deleted` or `anonymized`.
