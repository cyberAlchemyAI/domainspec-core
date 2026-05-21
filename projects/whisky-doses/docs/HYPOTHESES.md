# Hypotheses

## Hypothesis Register

| ID  | Proposition                                                                                                                                                                                                               | Expected Effect                                                                               | Confidence | Status   |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ---------- | -------- |
| H1  | If listing and dose allocation are modeled as the first core feature, the operator can reduce oversell/stale-slot risk before automating payments or shipments.                                                           | improve allocation accuracy and public list freshness                                         | medium     | proposed |
| H2  | If WhatsApp list rendering is separated from WhatsApp posting automation, the group can gain transparency benefits without integration complexity.                                                                        | reduce delivery cost while preserving group trust                                             | medium     | proposed |
| H3  | If shipment batching is modeled separately from listing and payment contexts, the system can correctly handle multi-listing packages and later freight payment.                                                           | improve shipment completeness and reduce missed waiting doses                                 | high       | proposed |
| H4  | If Excel migration/import-export is delayed until core domain boundaries are stable, migration work will avoid encoding spreadsheet quirks as permanent domain rules.                                                     | reduce long-term model drift                                                                  | low        | proposed |
| H5  | If buyer registry starts with minimum shipping identity data, later freight/shipment workflows can avoid duplicate buyer/address reconciliation.                                                                          | reduce shipment preparation time                                                              | medium     | proposed |
| H6  | If payment links, reminders, and payment reconciliation are modeled with a clean split between messaging and payment truth, the operator can improve payment follow-through without stale or incorrect paid/unpaid state. | improve payment follow-through and reconciliation accuracy while reducing stale reminder risk | medium     | proposed |

## Hypothesis Details

### H1 - Listing Allocation First

- Proposition: If listing and dose allocation are modeled as the first core feature, the operator can reduce oversell/stale-slot risk before automating payments or shipments.
- Decision owner: group operator
- Primary signal: allocation error count per listing
- Expected direction: reduce
- Current evidence: operator described variable total doses, available/filled slots, open/closed status, and buyer slot filling as central workflow.
- Evidence type: stated
- Why this might be true: allocation is the first domain event after a listing is posted and drives payment and shipment obligations.
- Strongest counterargument: buyer registry or Excel import may be a stronger first step if duplicate buyer/shipping data or historical migration is the current bottleneck.
- Confounders: group size, listing popularity, operator discipline, and whether Excel already prevents most allocation errors.
- Disconfirming outcome: listing allocation errors are rare while payment or shipment reconciliation consumes most operator effort.
- Scope notes: applies to bottle listings with numbered dose slots; does not validate payment or freight automation.

### H2 - Rendering Before Integration

- Proposition: If WhatsApp list rendering is separated from WhatsApp posting automation, the group can gain transparency benefits without integration complexity.
- Decision owner: group operator
- Primary signal: time to produce accurate group update
- Expected direction: reduce
- Current evidence: current workflow posts listing text and slot status back to WhatsApp for transparency.
- Evidence type: stated
- Why this might be true: copyable deterministic text can preserve existing group behavior while avoiding API, authentication, and moderation constraints.
- Strongest counterargument: manual copy/paste may still be error-prone enough that direct posting is required for value.
- Confounders: frequency of updates, operator phone/desktop workflow, and WhatsApp formatting limitations.
- Disconfirming outcome: rendered text is rarely reused directly or manual posting still causes frequent mismatch.
- Scope notes: direct WhatsApp API integration remains out of first baseline scope.

### H3 - Shipment Batching As Separate Context

- Proposition: If shipment batching is modeled separately from listing and payment contexts, the system can correctly handle multi-listing packages and later freight payment.
- Decision owner: group operator
- Primary signal: freight batch completeness
- Expected direction: improve
- Current evidence: user stated shipping is batch-driven and a package may include multiple past doses across multiple bottle listings.
- Evidence type: stated
- Why this might be true: shipment readiness is a cross-listing lifecycle that cannot be represented by a single bottle listing status.
- Strongest counterargument: shipment volume may be low enough that a simple spreadsheet view remains sufficient in early versions.
- Confounders: package frequency, number of buyers with accumulated doses, freight quote complexity.
- Disconfirming outcome: shipments almost always map one-to-one to a listing or buyer with no cross-listing complexity.
- Scope notes: carrier label generation and automated freight provider integration are separate future concerns.

### H4 - Delay Excel Migration Until Boundaries Stabilize

- Proposition: If Excel migration/import-export is delayed until core domain boundaries are stable, migration work will avoid encoding spreadsheet quirks as permanent domain rules.
- Decision owner: group operator
- Primary signal: spreadsheet discrepancy count after import/export prototype
- Expected direction: reduce
- Current evidence: Excel is current control, but the future feature boundary model is not yet selected.
- Evidence type: hypothesized
- Why this might be true: migrating before domain boundaries are agreed can make current spreadsheet layout appear authoritative even where it reflects workaround structure.
- Strongest counterargument: Excel may contain the real operational schema and should be inspected first to avoid inventing a model disconnected from practice.
- Confounders: spreadsheet quality, history volume, and whether the operator needs continuity before any new workflow can be trusted.
- Disconfirming outcome: spreadsheet columns map cleanly to candidate contexts and reveal no major quirks.
- Scope notes: this does not argue against a read-only spreadsheet audit; it argues against making migration the first permanent domain feature without evidence.

### H5 - Minimum Buyer Registry

- Proposition: If buyer registry starts with minimum shipping identity data, later freight/shipment workflows can avoid duplicate buyer/address reconciliation.
- Decision owner: group operator
- Primary signal: duplicate buyer/address correction count during shipment preparation
- Expected direction: reduce
- Current evidence: buyers have basic shipping identity data such as name, CPF, and address.
- Evidence type: stated
- Why this might be true: buyer identity is reused across listings and shipment batches.
- Strongest counterargument: collecting CPF/address too early increases privacy handling before there is shipment value.
- Confounders: repeat buyer rate, number of one-time buyers, and whether address is collected only at shipment time today.
- Disconfirming outcome: most buyers are one-time buyers or shipping identity rarely changes shipment workload.
- Scope notes: requires privacy and retention policy before implementation.

### H6 - Payment Links, Reminders, And Reconciliation Boundary

- Proposition: If payment links, reminders, and payment reconciliation are modeled with a clean split between messaging and payment truth, the operator can improve payment follow-through without stale or incorrect paid/unpaid state.
- Decision owner: group operator
- Primary signal: payment reconciliation accuracy
- Expected direction: improve
- Current evidence: user added payment link sending and reminders for payments and bottle listings as project goals, then clarified that payment links should include reconciliation.
- Evidence type: stated
- Why this might be true: messaging depends on listing/payment/freight state, while reconciliation changes paid/unpaid truth and should remain governed by payment tracking.
- Strongest counterargument: Pix webhooks may make reconciliation straightforward enough that this does not need a large standalone feature early.
- Confounders: buyer payment habits, payment method convenience, reminder tone, channel limits, and whether stale payment data causes false reminders.
- Disconfirming outcome: payment delay is not a real bottleneck, Pix webhook matching is trivial with the chosen provider, or reminders create more confusion/noise than completed payments.
- Scope notes: reconciliation is in scope; Pix API webhook callback is the preferred path, with provider mapping, idempotency, retry, and manual fallback still to define.

## Prioritization

| Hypothesis ID | Value If True | Cost To Test | Risk If Wrong | Priority |
| ------------- | ------------- | ------------ | ------------- | -------- |
| H1            | high          | low          | high          | now      |
| H2            | medium        | low          | medium        | now      |
| H3            | high          | medium       | high          | now      |
| H4            | medium        | low          | medium        | later    |
| H5            | medium        | low          | medium        | later    |
| H6            | high          | low          | high          | now      |
