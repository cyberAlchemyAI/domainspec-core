# Experiment Candidates

## Candidate Register

| ID   | Hypothesis | Intervention                                                                                                                                                                    | Primary Signal                           | Cost   | Priority |
| ---- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | ------ | -------- |
| EX-1 | H1         | Run one recent or simulated bottle listing through a structured listing/allocation sheet using explicit slot states and rules.                                                  | allocation error count                   | low    | now      |
| EX-2 | H2         | Generate copyable WhatsApp text from structured listing data for two listing updates and compare against manual formatting.                                                     | time to produce accurate group update    | low    | now      |
| EX-3 | H3         | Take a real or representative set of waiting doses and build a shipment batch/package model across multiple listings.                                                           | freight batch completeness               | medium | now      |
| EX-4 | H4         | Audit the current Excel workbook columns and map each column to the candidate bounded contexts without importing data yet.                                                      | unmapped or ambiguous column count       | low    | later    |
| EX-5 | H5         | Deduplicate a small buyer sample by WhatsApp mention, name, CPF, and address to estimate registry value and privacy scope.                                                      | duplicate buyer/address correction count | low    | later    |
| EX-6 | H6         | Draft payment-link, reconciliation, and reminder flow for one listing/payment cycle and classify every trigger, recipient, evidence source, stop condition, and channel action. | reconciliation readiness                 | low    | now      |

## Candidate Details

### EX-1 - Listing Allocation Dry Run

- Linked hypothesis: H1
- Decision owner: group operator
- Business question: Should the first feature be bottle listing and dose allocation?
- Intervention: Model one recent or simulated listing with bottle details, dose count, slot numbers, buyer requests, optional per-person limit, and open/closed status.
- Target segment or scope: one representative bottle listing, ideally with multiple buyers and at least one update after initial posting.
- Duration or observation window: one listing lifecycle or a retrospective reconstruction from existing WhatsApp/Excel records.
- Primary signal: allocation error count
- Secondary signals: time to update slots, number of manual corrections, number of ambiguous buyer requests.
- Expected effect: structured allocation surfaces fewer stale or ambiguous slot assignments than manual group/Excel handling.
- Disconfirming outcome: manual Excel already handles allocation with no notable errors or operator effort.
- Risks: retrospective data may be cleaner than live group behavior.
- Preconditions: one representative listing example with slot assignments and buyer mentions.
- Minimum instrumentation needed: record requested quantity, assigned slots, timestamp/order of changes, and final listing status.
- Recommended next step: run now before selecting the first feature pipeline.

### EX-2 - WhatsApp Rendering Prototype

- Linked hypothesis: H2
- Decision owner: group operator
- Business question: Is copyable public list rendering valuable before direct WhatsApp integration?
- Intervention: Generate the known listing format from structured data, including title line, payment line, closed/open status, and numbered buyer slots.
- Target segment or scope: two listing states, such as initial open listing and later filled/closed listing.
- Duration or observation window: one operator review session.
- Primary signal: time to produce accurate group update
- Secondary signals: formatting corrections, missing data fields, buyer comprehension issues.
- Expected effect: operator can produce group-ready text with fewer manual edits.
- Disconfirming outcome: generated text needs so much manual editing that rendering alone has little value.
- Risks: a prototype may underrepresent formatting edge cases from real WhatsApp messages.
- Preconditions: agreed canonical text format for at least one listing type.
- Minimum instrumentation needed: compare generated output against operator-accepted message.
- Recommended next step: run now alongside EX-1.

### EX-3 - Shipment Batch Reconstruction

- Linked hypothesis: H3
- Decision owner: group operator
- Business question: Does shipment batching need its own feature boundary?
- Intervention: Select a representative set of waiting paid doses across listings and model shipment batch, packages, freight amounts, freight payment status, and shipment status.
- Target segment or scope: at least two buyers and two bottle listings if available; otherwise simulate the cross-listing case.
- Duration or observation window: one shipment planning event.
- Primary signal: freight batch completeness
- Secondary signals: missed waiting doses, package changes after freight quote, unpaid freight count.
- Expected effect: explicit shipment batching catches cross-listing package composition needs that listing/payment contexts do not own cleanly.
- Disconfirming outcome: real shipments do not cross listings or can be represented by a simple per-buyer waiting list.
- Risks: simulated data may exaggerate cross-listing complexity.
- Preconditions: sample of waiting doses and buyer shipping data.
- Minimum instrumentation needed: dose source listing, buyer, dose payment status, package inclusion, freight amount, freight paid, shipped flag.
- Recommended next step: run now if shipment errors or delays are already painful.

### EX-4 - Excel Boundary Audit

- Linked hypothesis: H4
- Decision owner: group operator
- Business question: Should Excel import/export be an early feature or a later migration support layer?
- Intervention: Map current spreadsheet tabs/columns to candidate bounded contexts and mark ambiguous fields.
- Target segment or scope: current operational workbook, without moving real data into a new system.
- Duration or observation window: one spreadsheet review session.
- Primary signal: unmapped or ambiguous column count
- Secondary signals: duplicate fields, formula-dependent values, hidden manual notes, data quality issues.
- Expected effect: audit clarifies whether Excel can bootstrap the system or must remain a sidecar until boundaries mature.
- Disconfirming outcome: workbook maps cleanly to the proposed contexts and is the best first source of truth.
- Risks: workbook may contain sensitive buyer data and should be handled carefully.
- Preconditions: access to spreadsheet structure or anonymized column headers.
- Minimum instrumentation needed: tab name, column name, sample-safe meaning, mapped context, strict/tolerant migration classification.
- Recommended next step: refine after first delivery slice decision.

### EX-5 - Buyer Registry Sample

- Linked hypothesis: H5
- Decision owner: group operator
- Business question: Is buyer registry a prerequisite for first shipment or can it wait?
- Intervention: Review a small sample of buyers across listings and shipping events for duplicate mentions, names, CPF/address conflicts, and missing fields.
- Target segment or scope: 10 to 20 recent buyers, anonymized if needed.
- Duration or observation window: one review session.
- Primary signal: duplicate buyer/address correction count
- Secondary signals: missing CPF count, missing address count, repeat buyer rate.
- Expected effect: repeated buyers and shipping data corrections justify an early buyer registry.
- Disconfirming outcome: buyer data is simple, mostly one-time, and does not block listing/payment value.
- Risks: PII exposure if sample is not minimized.
- Preconditions: privacy-safe access to buyer identity examples.
- Minimum instrumentation needed: anonymized buyer key, WhatsApp mention, repeat count, shipping identity completeness.
- Recommended next step: run later unless shipment preparation is the highest current pain.

### EX-6 - Payment Link, Reconciliation, And Reminder Dry Run

- Linked hypothesis: H6
- Decision owner: group operator
- Business question: Should payment links, reconciliation, and reminders be an early feature boundary?
- Intervention: For one representative listing, draft the Pix payment link/instruction message, webhook reconciliation path, and each reminder type, then map trigger, recipient, amount, link source, webhook correlation key, evidence source, send/render channel, repeat cadence, and stop condition.
- Target segment or scope: one listing with at least one unpaid buyer and one listing-status reminder scenario; include freight payment reminder if shipment data is available.
- Duration or observation window: one operator review session or one live listing cycle.
- Primary signal: reconciliation readiness
- Secondary signals: ambiguous trigger count, unmatched payment risk, duplicate webhook risk, stale reminder risk, wrong-recipient risk, manual editing required.
- Expected effect: the operator can identify a small link/reconciliation/reminder set that improves payment follow-through without noisy or stale messages.
- Disconfirming outcome: reminders require too much manual judgment, or payment links cannot be safely generated/shared/reconciled from current data.
- Risks: payment links may expose wrong amount, wrong recipient, stale payment instructions, or webhook evidence that cannot be matched to the correct obligation.
- Preconditions: choose a draft Pix provider/link model for the dry run, even if provisional.
- Minimum instrumentation needed: buyer, obligation amount, payment due date, link/instruction source, webhook correlation key, evidence source, reconciliation result, reminder timestamp, payment status before/after reminder.
- Recommended next step: run now if payment follow-through is a central pain.

## Sequencing Notes

1. Start with EX-1 and EX-2 together because they test whether listing allocation plus public rendering is the smallest valuable slice.
2. Run EX-6 before adding payment-link or reminder automation to avoid wrong-recipient, stale-link, unmatched-payment, and noisy-message behavior.
3. Run EX-3 before committing shipment logic inside listing/payment features.
4. Run EX-4 before any real import/export implementation to avoid making spreadsheet structure the permanent domain model by accident.
5. Run EX-5 before storing CPF/address data in the system so privacy scope is justified by operational value.
