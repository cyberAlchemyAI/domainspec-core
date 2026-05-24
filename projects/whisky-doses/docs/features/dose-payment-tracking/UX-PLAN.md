---
feature: dose-payment-tracking
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

# Dose Payment Tracking UX Plan

## Invocation Note

Local Arcanum invoke adapter was unavailable in this workspace; this UX plan was authored directly from SPEC.md, STORIES.md, UI-SPEC.md, and UI-ARCHITECTURE.md.

## UX Intent

Make payment truth inspectable and recoverable. The operator should see who owes, who paid, what exceptions exist, and where manual fallback is needed without confusing payment tracking with payment-link messaging.

Primary user: group operator.

Primary outcomes:

- open payment run from selected listings
- inspect buyer obligations and line items
- see provider correlation state
- understand webhook reconciliation outcomes
- resolve exceptions with manual fallback when needed

## Experience Principles

- Payment truth is authoritative here: statuses must be prominent and consistent across screens.
- Exceptions deserve their own queue: `partial`, `overpaid`, `unmatched`, and `failed` must not be hidden inside generic payment run detail.
- Manual fallback is a recovery path, not the happy path: require audit reason and visible context.
- Keep link text and reminders out of this UI except as references to downstream messaging.

## Primary Flow

1. Operator opens `/payment-runs`.
2. Operator opens payment for selected listings or lands on a run created by an on-fill trigger.
3. Operator opens `/payment-runs/{paymentRunId}`.
4. UI shows selected listings, deadline, buyer obligations, expected amount, received amount, status, and line items.
5. Operator reviews exception count and navigates to `/payment-exceptions` when needed.

UX success criteria:

- each buyer obligation shows expected/received/status without drilling into raw events
- line items preserve why a buyer owes the amount
- exception count is visible from the run summary

## Secondary Flows

### Provider Reconciliation

1. Payment link messaging attaches correlation key.
2. Webhook updates status.
3. UI reflects `processing`, `paid`, `partial`, `overpaid`, `unmatched`, or `failed`.

### Manual Fallback

1. Operator opens exception.
2. Operator reviews obligation, expected amount, received amount, and reason.
3. Operator marks paid with audit reason when operationally correct.
4. UI records manual source and refreshes downstream payment truth.

## Screen Plan

| Screen                         | UX Role                 | Key Decisions                                    |
| ------------------------------ | ----------------------- | ------------------------------------------------ |
| `/payment-runs`                | Payment run entry point | Show run summary, deadlines, exception counts    |
| `/payment-runs/{paymentRunId}` | Obligation truth table  | Focus on buyer obligations, line items, status   |
| `/payment-exceptions`          | Operator recovery queue | Filter by exception status, listing, payment run |

## Interaction Details

- Primary action: "Open Payment Run".
- Obligation row actions: view line items, attach/view correlation key, manual mark paid where allowed.
- Exception row action: open manual fallback dialog.
- Status badges must distinguish matched exceptions (`partial`, `overpaid`) from match failures (`unmatched`, `failed`).

## Edge And Empty States

| State                                        | UX Response                                      |
| -------------------------------------------- | ------------------------------------------------ |
| No payment runs                              | Empty state with "Open Payment Run"              |
| Selected listings have no active allocations | Block opening and explain allocation requirement |
| Missing correlation key                      | Show automatic reconciliation not ready          |
| Duplicate webhook                            | Show no-op processed state, not an error panic   |
| Retry exhausted                              | Promote to exception queue with next action hint |

## Cross-Feature Handoffs

| Handoff                                 | UX Contract                                                                                              |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| From Bottle Listing And Dose Allocation | Payment run creation starts from selected listing allocations and preserves buyer/slot/amount line items |
| To Payment Link And Reminder Messaging  | Unpaid obligations, deadlines, and correlation references are available for link and reminder rendering  |
| To Freight And Shipment Batching        | Paid status becomes the shipment eligibility source for waiting doses                                    |

## UX Validation Checklist

- [ ] Payment run detail shows buyer-level paid/unpaid status next to each obligation.
- [ ] Expected amount, received amount, line items, and status are readable without raw webhook inspection.
- [ ] Exception queue covers partial, overpaid, unmatched, failed, and retry-exhausted states.
- [ ] Manual mark-paid flow requires an audit reason and preserves source as manual.
- [ ] Messaging and freight concepts remain references, not editable responsibilities.

## Iteration Notes

- Do not render buyer-facing payment-link text here.
- Do not implement freight payment tracking here.
- Future observability should surface retry and exception counts.
