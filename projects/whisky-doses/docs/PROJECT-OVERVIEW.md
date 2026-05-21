# Whisky Dose Group Operations

## Summary

Whisky Dose Group Operations supports a WhatsApp-based bottle dose group where an operator registers buyers, posts bottle listings, allocates numbered dose slots to buyers, sends payment links, tracks payment and freight, reminds buyers about payment/listing deadlines, and exposes transparent status back to the group. The immediate domain need is to replace manual/Excel-controlled operations without building an Excel migration feature, while preserving the group-facing listing format and trust signals that make the current workflow work.

## Discovery Mode

- Mode: greenfield
- Project state: idea
- Interview date: 2026-05-20
- Operator / owner: group operator

## Problem Framing

- Primary user or customer: group operator managing bottle listings, dose allocation, payment links, reminders, payment status, freight batching, and shipment coordination.
- Secondary user: WhatsApp group buyer reserving doses, receiving payment links/reminders, paying dose and freight amounts, and expecting shipment transparency.
- Core problem: the current workflow spans WhatsApp messages, buyer mentions, numbered slots, Excel controls, payment timing, reminder timing, freight calculation, and batch shipment decisions, which creates operational risk and unclear feature boundaries.
- Value proposition: a domain model and incremental system split that lets the operator automate or migrate the highest-risk parts while keeping WhatsApp as the group-facing channel.
- Business goal: improve operational accuracy, transparency, payment follow-through, and scalability of bottle dose group operations.
- Non-goals: marketplace discovery, public ecommerce checkout, carrier label automation, Excel migration/import, inventory procurement, whisky tasting content, or broad CRM beyond data required for dose/freight/shipping operations.

## Current State

| Item                    | Status  | Evidence Type | Notes                                                                                                                                                                                                       |
| ----------------------- | ------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Product scope           | partial | stated        | Scope centers on buyer registration, WhatsApp bottle dose listings, allocation, payment links, payment/listing reminders, payments, freight, and shipment batching. Excel migration/import is out of scope. |
| Domain boundaries       | partial | hypothesized  | Candidate boundaries are buyer registry, bottle listing/dose allocation, payment tracking, payment link/reminder messaging, public WhatsApp rendering, and freight/shipment batching.                       |
| Existing implementation | none    | observed      | No `docs/` baseline or feature implementation was present in this workspace during discovery.                                                                                                               |
| Metrics baseline        | unknown | stated        | No measured baseline for fill speed, payment delay, freight cycle time, or spreadsheet error rate was provided.                                                                                             |

Evidence type:

- `observed` = seen in repository or artifacts
- `stated` = given by operator
- `hypothesized` = inferred but not yet validated

## Actors And Stakeholders

| Actor                   | Goal                                                                                                                                      | Pain Point                                                                                                    | Frequency                       | Evidence Type |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------- | ------------- |
| Group operator          | Publish listings, allocate doses, send payment links/reminders, collect payment/freight, and coordinate shipments                         | Manual reconciliation across WhatsApp and Excel can create errors, stale public status, and missed follow-ups | Per listing and shipment batch  | stated        |
| Buyer                   | Reserve dose quantities, see allocation status, receive the right payment link/reminder, pay at the right time, and receive shipped doses | Must infer availability and payment/shipment status from group messages                                       | Per desired bottle and shipment | stated        |
| WhatsApp group audience | See which numbered slots are open, filled, or closed                                                                                      | Transparency depends on current rendered list accuracy                                                        | Per listing update              | stated        |
| Shipping coordinator    | Group paid doses into packages and share freight amounts                                                                                  | Shipping is batch-driven and may span multiple past bottle listings                                           | Per shipment batch              | stated        |

## Candidate Bounded Contexts

| Context                             | Responsibility                                                                                                                      | Key Concepts                                                                                 | Status    | Evidence Type |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | --------- | ------------- |
| Buyer Registry                      | Maintain buyer identity needed for reservation and shipping data needed before first shipment                                       | Buyer, WhatsApp Mention, CPF, Shipping Address, Shipping Identity                            | candidate | stated        |
| Bottle Listing And Dose Allocation  | Represent bottle listings, numbered dose slots, buyer dose requests, slot assignment, fill status, and close/open lifecycle         | Bottle Listing, Dose Slot, Dose Size, Price Per Dose, Per-Person Dose Limit, Listing Status  | candidate | stated        |
| Dose Payment Tracking               | Track when payment opens, who owes, who paid, reconcile payment-link results/evidence, and maintain listing-level payment readiness | Payment Opening Rule, Payment Deadline, Dose Payment, Payment Reconciliation, Payment Status | candidate | stated        |
| Payment Link And Reminder Messaging | Generate or send buyer-facing payment links and reminders for payment deadlines, freight payment, and bottle listing activity       | Payment Link, Reminder Schedule, Reminder Trigger, Reminder Message, Delivery Status         | candidate | stated        |
| Public WhatsApp List Rendering      | Produce copy/paste listing, payment-link, and reminder messages from authoritative data, including buyer-level paid/unpaid status   | Listing Render, Slot Line, Buyer Mention, Payment Status Snippet, Reminder Message           | candidate | stated        |
| Freight And Shipment Batching       | Calculate freight later, batch waiting doses across listings, track freight payment, and ship packages                              | Shipment Batch, Package, Waiting Dose, Freight Quote, Freight Payment, Shipment Status       | candidate | stated        |

## Proposed Incremental Feature Split

| Slice | Feature Boundary                    | Includes                                                                                                                                   | Excludes                                                                                 | Why This Boundary                                                                                             | Evidence Type |
| ----- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------- |
| 1     | Buyer Registry                      | Buyer name, WhatsApp mention, CPF before reservation; shipping address before first shipment; lookup by buyer                              | Listing allocation, payment balance, freight calculation                                 | Ensures reservations are tied to known buyer identity while delaying shipping address collection until needed | stated        |
| 2     | Bottle Listing And Dose Allocation  | Create listing, dose count/size/price, numbered slots, requests, assignment, open/closed status, per-person limit                          | Payment collection, freight batching, Excel migration/import                             | This is the central group operation and source for most later workflows                                       | stated        |
| 3     | Public WhatsApp List Rendering      | Generate copyable listing/status text, payment-link text, reminder text, and buyer-level paid/unpaid snippets                              | Direct WhatsApp posting automation, buyer registry CRUD, payment reconciliation          | Keeps transparency visible while avoiding premature WhatsApp API integration                                  | stated        |
| 4     | Dose Payment Tracking               | Payment opening rule, deadline, amount owed, paid/unpaid per buyer/listing, payment-link reconciliation, manual/provider evidence matching | Freight payment, payment-link delivery, reminder delivery ownership                      | Payment links create payment obligations that must be reconciled back into payment truth                      | stated        |
| 5     | Payment Link And Reminder Messaging | Payment link generation/sharing, payment reminders, freight payment reminders, bottle listing reminders, reminder delivery state           | Owning payment truth, slot allocation, freight calculation, reconciliation state changes | Reminders cut across listing, payment, and freight contexts, so they need clear trigger ownership             | stated        |
| 6     | Freight And Shipment Batching       | Waiting paid doses, batch package composition across listings, freight amount, freight paid, shipped status                                | Carrier integration, label purchasing, fixed shipping cycles                             | Shipping is explicitly batch-driven and cross-listing, so it should not be hidden inside listing payment      | stated        |

## Core Workflows

| Workflow                       | Trigger                                                                           | Main Steps                                                                                                                                                                                          | Failure Mode                                                                                                                       | Evidence Type |
| ------------------------------ | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| Publish Bottle Listing         | Operator prepares a new bottle offering                                           | Enter bottle details, dose size, price, total slots, payment deadline/rule, optional dose limit, render WhatsApp text, post to group                                                                | Listing text does not match source data or omits a rule                                                                            | stated        |
| Allocate Dose Slots            | Buyer asks for one or more doses                                                  | Validate listing open, validate availability, validate per-person limit if configured, assign numbered slots, update public list                                                                    | Overselling, duplicate allocation, or unfair per-person limit handling                                                             | stated        |
| Open Dose Payment              | Listing fills or configured payment point is reached                              | Mark payments open, expose deadline, create or attach payment links, track who owes, update public transparency                                                                                     | Payment opens too early/late, payment link is wrong/stale, or buyers miss deadline                                                 | stated        |
| Send Payment Link And Reminder | Payment opens, deadline approaches, freight is quoted, or listing needs attention | Select recipients, choose reminder template, include payment link when applicable, send or render message, track delivery/status                                                                    | Reminder spam, wrong recipient, wrong amount/link, or unclear opt-out policy                                                       | stated        |
| Reconcile Dose Payments        | Buyer pays through a generated link or operator manually marks payment            | Match provider callback or operator confirmation to buyer/listing/payment obligation, record payment status, reconcile against owed amount, identify unpaid buyers, stop or adjust future reminders | Payment evidence cannot be matched, wrong amount is paid, stale reminder fires after payment, or partial payment policy is unclear | stated        |
| Build Shipment Batch           | Operator decides which waiting doses/listings/buyers will be sent                 | Select paid/waiting doses across listings, calculate freight, share freight amounts, await freight payment, ship packages                                                                           | Package misses eligible doses or includes unpaid/unready doses                                                                     | stated        |

## Constraints

| Constraint                                                 | Type                     | Why It Matters                                                                                                                  | Evidence Type |
| ---------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| WhatsApp remains the primary group-facing channel          | operational              | Public list rendering must preserve familiar message semantics before any direct WhatsApp integration is considered             | stated        |
| Buyer identity includes CPF and address                    | regulatory / operational | PII handling, access control, and data minimization matter from the buyer registry onward                                       | stated        |
| Buyer reservation requires identity                        | operational              | Name, WhatsApp mention, and CPF are required before reservation; full shipping address is required before first shipment        | stated        |
| Buyer inactivity is operator-selected                      | privacy / operational    | Buyer data is retained while active and deleted or anonymized only when the operator manually marks the buyer inactive          | stated        |
| Shipping is batch-driven, not fixed-cycle                  | business                 | Shipment batching must be its own context and cannot assume one shipment per listing or periodic cycle                          | stated        |
| Excel migration is out of scope                            | product / operational    | The system should model new operations directly rather than spend v1 scope importing or reconciling historical spreadsheet data | stated        |
| Payment opening is configurable                            | business                 | Payment tracking must support "after fill" and other configured points without hardcoding one lifecycle                         | stated        |
| Payment links and reminders are part of the operating goal | business / operational   | Link generation and reminder timing need explicit policy so buyers receive correct payment instructions without noisy messaging | stated        |
| Payment links require reconciliation                       | business / operational   | A generated or shared payment link must feed a reconciliation path, even if first-version reconciliation is manual              | stated        |
| Per-person dose limit is optional                          | business                 | Allocation rules must support listings with and without buyer-level dose caps                                                   | stated        |

## Success Signals

| Signal                              | Why It Matters                                                                | Current Baseline                | Target Direction |
| ----------------------------------- | ----------------------------------------------------------------------------- | ------------------------------- | ---------------- |
| Allocation accuracy                 | Prevents overselling and trust loss                                           | Unknown; currently Excel/manual | improve          |
| Public list freshness               | Group transparency depends on up-to-date slot status                          | Unknown                         | improve          |
| Payment reconciliation time         | Operator effort and payment deadline enforcement depend on it                 | Unknown                         | reduce           |
| Payment reconciliation accuracy     | Payment links only help if paid/unpaid truth is updated correctly             | Unknown                         | improve          |
| Payment link/reminder effectiveness | Payment follow-through depends on buyers receiving clear, timely instructions | Unknown                         | improve          |
| Reminder noise rate                 | Trust can drop if buyers receive irrelevant, duplicate, or stale reminders    | Unknown                         | reduce           |
| Freight batch completeness          | Packages should include the intended waiting paid doses across listings       | Unknown                         | improve          |

## Risks And Unknowns

| Risk                                                        | Why Risky                                                                                              | Severity | What Would Reduce It                                                                                                                            |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Feature boundaries hide cross-context shipment needs        | Shipment batches span multiple listings and buyers, so a listing-centric model may break later         | high     | Model waiting doses and shipment batches explicitly before implementation                                                                       |
| Buyer-level payment status can expose social pressure       | Public paid/unpaid display next to buyers/slots is intentional, but accuracy mistakes can affect trust | high     | Keep reconciliation states explicit and ensure rendered status comes from authoritative payment truth                                           |
| CPF/address data increases privacy obligations              | Buyer registry introduces sensitive data handling before core listing automation                       | medium   | Limit v1 management to the operator, require identity before reservation, collect address before shipment, and delete/anonymize inactive buyers |
| WhatsApp rendering may be mistaken for WhatsApp integration | Posting automation is a different boundary from copyable list/payment/reminder rendering               | medium   | Keep v1 copy/paste only and explicitly defer direct WhatsApp posting                                                                            |

## Counter-Positions

| Proposition                                            | Plausible Alternative Or Failure Mode                                                                                 | Invalidation Signal                                                                                              |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Start with buyer registry before listings              | Operator may need listing allocation first, using lightweight buyer labels until identity data is needed for shipping | Most allocation work can proceed safely with WhatsApp mentions only                                              |
| Keep public WhatsApp list rendering as its own feature | Rendering may be too small alone and could be embedded in listing allocation initially                                | No independent template/versioning needs emerge after two to three listing cycles                                |
| Treat shipment batching as a separate bounded context  | Shipment may remain simple enough to manage in Excel for longer than allocation/payment                               | Freight/shipment errors are rare and not a near-term operator bottleneck                                         |
| Treat reminders as a separate communication boundary   | Reminder behavior may be simple enough to remain inside payment tracking at first                                     | Reminders are only manual copy/paste notes and do not need scheduling, delivery state, or cross-context triggers |
| Exclude Excel migration/import from v1                 | Existing spreadsheet data might seem tempting to import, but it would distract from new operational truth             | Operator later decides historical data is needed enough to reopen migration scope                                |

## Recommended Next Artifacts

1. `docs/INITIAL-DEFINITIONS.md`
2. `docs/HYPOTHESES.md`
3. `docs/EXPERIMENT-CANDIDATES.md`

## Open Questions

No project-level open questions remain from discovery/interrogation. Feature-level planning may still introduce implementation questions.

## Implementation Baseline

- Stack: DomainSpec base TypeScript stack.
- Verification: use the verification baseline associated with the DomainSpec base TypeScript stack for the first feature pipeline.
