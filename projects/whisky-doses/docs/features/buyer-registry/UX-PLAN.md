---
feature: buyer-registry
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

# Buyer Registry UX Plan

## Invocation Note

Local Arcanum invoke adapter was unavailable in this workspace; this UX plan was authored directly from SPEC.md, STORIES.md, UI-SPEC.md, and UI-ARCHITECTURE.md.

## UX Intent

Make buyer identity management feel like a fast operator lookup and correction tool, not a CRM. The operator should immediately know whether a buyer is reservation-ready, shipping-ready, inactive, anonymized, or deleted.

Primary user: group operator.

Primary outcomes:

- register a buyer before reservation
- find and select a buyer during downstream work
- correct identity safely
- add address only when shipment needs it
- handle inactive buyer retention deliberately

## Experience Principles

- Keep active buyer lookup fast: search, status filters, and readiness badges must be visible on the list page.
- Treat CPF and address as sensitive operational fields: show them only where needed for operator work.
- Make blockers textual, not just colored: missing CPF, missing WhatsApp mention, missing address, inactive status, anonymized/deleted state.
- Keep retention actions slower than ordinary edits: mark inactive first, then choose delete/anonymize with explicit confirmation.

## Primary Flow

1. Operator opens `/buyers`.
2. Operator searches by name or WhatsApp mention.
3. If the buyer does not exist, operator opens `RegisterBuyerDialog`.
4. Operator enters name, WhatsApp mention, CPF, and optionally address.
5. System creates active buyer and shows reservation-ready status.
6. Downstream allocation and messaging flows can select the buyer.

UX success criteria:

- registration form makes required reservation identity obvious
- duplicate CPF/mention errors are specific
- active buyer appears in search immediately after creation

## Secondary Flows

### Identity Correction

1. Operator opens `/buyers/{buyerId}`.
2. Operator edits name, WhatsApp mention, or CPF.
3. UI keeps reservation eligibility visible before and after save.

### Shipping Readiness

1. Operator opens the buyer detail page from shipment context or buyer search.
2. Operator enters full shipping address.
3. UI changes the shipping badge from "Needs address" to "Shipping ready".

### Retention

1. Operator marks an active buyer inactive.
2. UI removes reservation and shipment readiness.
3. Operator chooses anonymize or delete.
4. UI prevents normal edits after terminal retention state.

## Screen Plan

| Screen              | UX Role                            | Key Decisions                                                                         |
| ------------------- | ---------------------------------- | ------------------------------------------------------------------------------------- |
| `/buyers`           | Find, register, and scan readiness | Default filter shows active buyers; include retained inactive only by explicit filter |
| `/buyers/{buyerId}` | Inspect and correct one buyer      | Separate identity, shipping, and retention panels                                     |

## Interaction Details

- Primary action on list: "Register Buyer".
- Row actions: view detail, edit identity.
- Detail actions: edit identity, set address, mark inactive, retention action.
- Use status badges for `active`, `inactive`, `anonymized`, and `deleted`.
- Use readiness badges for reservation and shipping readiness.
- Disable mutation actions on anonymized/deleted buyers.

## Edge And Empty States

| State                        | UX Response                                      |
| ---------------------------- | ------------------------------------------------ |
| No buyers                    | Empty state with "Register Buyer" primary action |
| Duplicate CPF or mention     | Field-level error naming the duplicate field     |
| Missing reservation identity | Show "Missing identity" with missing fields list |
| Missing shipping address     | Show "Needs address" and address action          |
| Deleted/anonymized buyer     | Hide original PII and explain terminal state     |

## Cross-Feature Handoffs

| Handoff                                | UX Contract                                                                               |
| -------------------------------------- | ----------------------------------------------------------------------------------------- |
| To Bottle Listing And Dose Allocation  | Buyer lookup exposes active status and reservation eligibility before any slot allocation |
| To Payment Link And Reminder Messaging | Buyer mention is the canonical copy target for rendered messages                          |
| To Freight And Shipment Batching       | Shipping address readiness is visible and actionable from shipment blockers               |

## UX Validation Checklist

- [ ] Buyer list supports fast lookup by name and WhatsApp mention.
- [ ] Buyer detail separates identity, shipping, and retention concerns.
- [ ] Reservation readiness and shipping readiness are visible as separate states.
- [ ] Inactive, anonymized, and deleted buyers cannot be selected accidentally in downstream work.
- [ ] Sensitive fields are shown only where operator decisions need them.

## Iteration Notes

- Buyer self-service is deferred; do not design buyer-facing account flows.
- Address collection should not block reservation.
- Future UI may add bulk import only if Excel migration scope is reopened.
