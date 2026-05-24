---
feature: bottle-listing-and-dose-allocation
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

# Bottle Listing And Dose Allocation UX Plan

## Invocation Note

Local Arcanum invoke adapter was unavailable in this workspace; this UX plan was authored directly from SPEC.md, STORIES.md, UI-SPEC.md, and UI-ARCHITECTURE.md.

## UX Intent

Make the listing screen feel like the operator's live control board for a WhatsApp bottle split: prepare the offer, open it, assign numbered slots, correct allocations, and close it when appropriate.

Primary user: group operator.

Primary outcomes:

- create draft listing with generated numbered slots
- open listing for reservations
- allocate slots to reservation-ready buyers
- release slots for corrections
- close listing and expose stable allocation state to downstream payment/rendering

## Experience Principles

- The slot grid is the center of the experience: numbered slots must be stable, scannable, and keyboard navigable.
- Filled is derived, not a lifecycle state: show it as an indicator separate from draft/open/closed.
- Allocation blockers must be precise: not open, slot unavailable, buyer not reservation-ready, per-person limit exceeded.
- Avoid payment UI here: payment status and payment links belong to downstream features.

## Primary Flow

1. Operator opens `/listings`.
2. Operator creates a draft listing with bottle, dose size, price, slot count, payment mode, and optional per-person limit.
3. Operator opens the listing when ready.
4. Operator opens detail, selects buyer, and chooses explicit slots or next available quantity.
5. System assigns slots, updates the grid, and recalculates filled.
6. Operator closes listing when reservations should stop.

UX success criteria:

- operator can understand slot availability without reading a long table
- allocation feedback is immediate and tied to selected slot numbers
- close action clearly communicates that normal allocation changes stop

## Secondary Flows

### Release Correction

1. Operator selects an active allocation row.
2. Operator chooses one or more owned slots to release.
3. UI updates slot grid and filled indicator.
4. Release history remains visible enough for audit.

### Downstream Readiness

1. Operator reviews allocation summary.
2. UI shows total, allocated, available, buyer allocation rows, and derived filled flag.
3. Payment/rendering consumers can rely on the read model.

## Screen Plan

| Screen                  | UX Role                    | Key Decisions                                                        |
| ----------------------- | -------------------------- | -------------------------------------------------------------------- |
| `/listings`             | Listing queue and creation | Start with open/draft work; filters for bottle name and fill state   |
| `/listings/{listingId}` | Slot control board         | Slot grid first, allocation controls adjacent, allocation rows below |

## Interaction Details

- Primary list action: "Create Listing".
- Detail primary action depends on state: draft shows "Open"; open shows allocation controls; draft/open show "Close".
- Slot grid cell states: open, allocated, released history.
- Buyer selection should use Buyer Registry lookup and surface reservation eligibility.
- Allocation panel should support explicit slot selection and next-available quantity.

## Edge And Empty States

| State                                  | UX Response                                          |
| -------------------------------------- | ---------------------------------------------------- |
| No listings                            | Empty state with "Create Listing" primary action     |
| Draft listing missing details          | Disable open and list missing fields                 |
| Buyer not eligible                     | Show buyer identity blocker from Buyer Registry      |
| Slot unavailable after stale selection | Clear stale selection and explain slot changed       |
| Closed listing                         | Read-only slot grid with close reason when available |

## Cross-Feature Handoffs

| Handoff                                | UX Contract                                                                                                         |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| From Buyer Registry                    | Allocation controls consume buyer identity and reservation eligibility; ineligible buyers show the upstream blocker |
| To Dose Payment Tracking               | Closed or selected listing allocations expose buyer, slots, amount, and line-item traceability                      |
| To Payment Link And Reminder Messaging | Listing context exposes availability/fill information for rendered listing reminders                                |

## UX Validation Checklist

- [ ] Slot grid is the dominant detail-page affordance and remains stable during allocation changes.
- [ ] Draft, open, and closed lifecycle states are visually distinct from the derived filled indicator.
- [ ] Allocation controls explain buyer eligibility and slot availability blockers.
- [ ] Release actions update slot availability without hiding audit-relevant history.
- [ ] Payment and messaging actions are referenced only as downstream handoffs.

## Iteration Notes

- Do not auto-close when filled; filled is derived.
- Reopen is outside v1.
- Public WhatsApp rendering is a separate feature; this UX may preview allocation state but not own public formatting.
