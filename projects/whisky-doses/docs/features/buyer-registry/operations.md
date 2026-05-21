# Operations: Buyer Registry

This file defines the operator-triggered mutations owned by Buyer Registry.

## RegisterBuyer

**Type:** Operation (mutation)
**Actor:** [Group operator](../../PROJECT-OVERVIEW.md#actors-and-stakeholders)
**Triggers:** Operator creates a buyer before reservation or later operational use.

### Input

| Field           | Type                                           | Required | Description                                      |
| --------------- | ---------------------------------------------- | -------- | ------------------------------------------------ |
| name            | string                                         | yes      | Maps to [Buyer](domain.md#buyer).name            |
| whatsAppMention | [WhatsApp Mention](domain.md#whatsapp-mention) | yes      | Maps to [Buyer](domain.md#buyer).whatsAppMention |
| cpf             | [CPF](domain.md#cpf)                           | yes      | Maps to [Buyer](domain.md#buyer).cpf             |
| shippingAddress | [Shipping Address](domain.md#shipping-address) | no       | Optional until first shipment                    |

### Rules

| ID  | Rule                     | Formal                                                      |
| --- | ------------------------ | ----------------------------------------------------------- |
| R1  | Identity fields required | `present(name) && present(whatsAppMention) && present(cpf)` |
| R3  | Active buyer uniqueness  | `uniqueActive(cpf) && uniqueActive(whatsAppMention)`        |
| R4  | Operator-only mutation   | `actor.role == group_operator`                              |

### State Transition

`[Buyer](domain.md#buyer): none -> active`

### Postconditions

- A new [Buyer](domain.md#buyer) exists with [Buyer Status](domain.md#buyer-status) `active`.
- [BuyerRegistered](events.md#buyerregistered) is produced.
- [CheckBuyerReservationEligibility](queries.md#checkbuyerreservationeligibility) returns true for the new [Buyer](domain.md#buyer).

### Error States

| Condition                                                                                                        | Result              |
| ---------------------------------------------------------------------------------------------------------------- | ------------------- |
| Missing [Buyer](domain.md#buyer).name, [Buyer](domain.md#buyer).whatsAppMention, or [Buyer](domain.md#buyer).cpf | Reject registration |
| Duplicate active [CPF](domain.md#cpf) or [WhatsApp Mention](domain.md#whatsapp-mention)                          | Reject registration |
| Actor is not the [group operator](../../PROJECT-OVERVIEW.md#actors-and-stakeholders)                             | Reject mutation     |

## UpdateBuyerIdentity

**Type:** Operation (mutation)
**Actor:** [Group operator](../../PROJECT-OVERVIEW.md#actors-and-stakeholders)
**Triggers:** Operator corrects or updates buyer identity data.

### Input

| Field           | Type                                           | Required | Description                                          |
| --------------- | ---------------------------------------------- | -------- | ---------------------------------------------------- |
| buyerId         | [BuyerId](domain.md#buyerid)                   | yes      | Identifies the [Buyer](domain.md#buyer)              |
| name            | string                                         | no       | Replacement [Buyer](domain.md#buyer).name            |
| whatsAppMention | [WhatsApp Mention](domain.md#whatsapp-mention) | no       | Replacement [Buyer](domain.md#buyer).whatsAppMention |
| cpf             | [CPF](domain.md#cpf)                           | no       | Replacement [Buyer](domain.md#buyer).cpf             |

### Rules

| ID  | Rule                                                  | Formal                                                             |
| --- | ----------------------------------------------------- | ------------------------------------------------------------------ |
| R1  | Updated active buyer must remain reservation eligible | `buyer.status == active -> reservationEligible(updatedBuyer)`      |
| R3  | Updated active identity must remain unique            | `uniqueActive(updatedCpf) && uniqueActive(updatedWhatsAppMention)` |
| R4  | Operator-only mutation                                | `actor.role == group_operator`                                     |

### State Transition

`[Buyer](domain.md#buyer): active -> active`

### Postconditions

- The selected [Buyer](domain.md#buyer) identity fields are updated.
- [BuyerIdentityUpdated](events.md#buyeridentityupdated) is produced when any identity field changes.

### Error States

| Condition                                                                                            | Result        |
| ---------------------------------------------------------------------------------------------------- | ------------- |
| [Buyer](domain.md#buyer) is `anonymized` or `deleted`                                                | Reject update |
| Update would remove required identity from active [Buyer](domain.md#buyer)                           | Reject update |
| Update would duplicate active [CPF](domain.md#cpf) or [WhatsApp Mention](domain.md#whatsapp-mention) | Reject update |

## SetBuyerShippingAddress

**Type:** Operation (mutation)
**Actor:** [Group operator](../../PROJECT-OVERVIEW.md#actors-and-stakeholders)
**Triggers:** Operator prepares a buyer for first shipment.

### Input

| Field           | Type                                           | Required | Description                                     |
| --------------- | ---------------------------------------------- | -------- | ----------------------------------------------- |
| buyerId         | [BuyerId](domain.md#buyerid)                   | yes      | Identifies the [Buyer](domain.md#buyer)         |
| shippingAddress | [Shipping Address](domain.md#shipping-address) | yes      | Complete address required before first shipment |

### Rules

| ID  | Rule                               | Formal                                |
| --- | ---------------------------------- | ------------------------------------- |
| R2  | Complete shipping address required | `shippingReady(updatedBuyer) == true` |
| R4  | Operator-only mutation             | `actor.role == group_operator`        |

### State Transition

`[Buyer](domain.md#buyer): active -> active`

### Postconditions

- [Buyer](domain.md#buyer).shippingAddress is set or replaced.
- [BuyerShippingAddressSet](events.md#buyershippingaddressset) is produced.
- [CheckBuyerShippingReadiness](queries.md#checkbuyershippingreadiness) returns true when all [R2](rules.md#r2-shipping-address-required-before-first-shipment) fields are present.

### Error States

| Condition                                                    | Result                |
| ------------------------------------------------------------ | --------------------- |
| [Buyer](domain.md#buyer) is not active                       | Reject address update |
| [Shipping Address](domain.md#shipping-address) is incomplete | Reject address update |

## MarkBuyerInactive

**Type:** Operation (mutation)
**Actor:** [Group operator](../../PROJECT-OVERVIEW.md#actors-and-stakeholders)
**Triggers:** Operator manually decides a buyer should no longer be active.

### Input

| Field   | Type                         | Required | Description                             |
| ------- | ---------------------------- | -------- | --------------------------------------- |
| buyerId | [BuyerId](domain.md#buyerid) | yes      | Identifies the [Buyer](domain.md#buyer) |
| reason  | string                       | no       | Operator note for the inactive decision |

### Rules

| ID  | Rule                                              | Formal                                             |
| --- | ------------------------------------------------- | -------------------------------------------------- |
| P1  | Manual inactive marking starts retention handling | `buyer.status == active -> nextStatus == inactive` |
| R4  | Operator-only mutation                            | `actor.role == group_operator`                     |

### State Transition

`[Buyer](domain.md#buyer): active -> inactive`

### Postconditions

- [Buyer](domain.md#buyer).status is `inactive`.
- [Buyer](domain.md#buyer).inactiveAt is set.
- [BuyerMarkedInactive](events.md#buyermarkedinactive) is produced.
- Reservation and shipment readiness queries return false.

### Error States

| Condition                              | Result                  |
| -------------------------------------- | ----------------------- |
| [Buyer](domain.md#buyer) is not active | Reject inactive marking |

## DeleteOrAnonymizeBuyer

**Type:** Operation (mutation)
**Actor:** [Group operator](../../PROJECT-OVERVIEW.md#actors-and-stakeholders)
**Triggers:** Operator chooses the retention action for an inactive buyer.

### Input

| Field           | Type                                           | Required | Description                                      |
| --------------- | ---------------------------------------------- | -------- | ------------------------------------------------ |
| buyerId         | [BuyerId](domain.md#buyerid)                   | yes      | Identifies the inactive [Buyer](domain.md#buyer) |
| retentionAction | [Retention Action](domain.md#retention-action) | yes      | `delete` or `anonymize`                          |

### Rules

| ID  | Rule                                                 | Formal                                                               |
| --- | ---------------------------------------------------- | -------------------------------------------------------------------- |
| P1  | Retention action applies only after inactive marking | `buyer.status == inactive && retentionAction in {delete, anonymize}` |
| R4  | Operator-only mutation                               | `actor.role == group_operator`                                       |

### State Transition

`[Buyer](domain.md#buyer): inactive -> anonymized | deleted`

### Postconditions

- If action is `anonymize`, original PII fields are no longer readable and [Buyer](domain.md#buyer).status becomes `anonymized`.
- If action is `delete`, retained PII is removed and [Buyer](domain.md#buyer).status becomes `deleted`.
- [BuyerDataRemoved](events.md#buyerdataremoved) is produced.

### Error States

| Condition                                                | Result                                                                         |
| -------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [Buyer](domain.md#buyer) is active                       | Reject retention action until [MarkBuyerInactive](#markbuyerinactive) succeeds |
| [Retention Action](domain.md#retention-action) is `none` | Reject terminal retention action                                               |
