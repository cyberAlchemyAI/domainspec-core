# Scorecard Spec

Status: draft
Pilot: CyberAlchemy Lead Evidence Dogfood Pilot

## Purpose

Define the minimum evidence object for judging CyberAlchemy lead-page and channel experiments.

The scorecard does not prove growth. It makes one marketing decision inspectable.

## Scorecard Header

Required fields:

- `run_id`
- `date_started`
- `date_reviewed`
- `owner`
- `offer`
- `conversion_event`
- `primary_channel`
- `response_window`
- `source_surfaces`
- `variant_count`
- `decision`

Decision values:

- `keep`
- `revise`
- `pause`
- `retest`
- `inconclusive`

## Variant Fields

For each message, creative, or page variant:

- `variant_id`
- `variant_type`
- `source_claim`
- `target_buyer`
- `promise`
- `call_to_action`
- `channel`
- `evidence_source`
- `overclaim_risk`
- `expected_signal`
- `observed_signal`
- `lead_quality_notes`
- `confounds`
- `decision`

## Evidence Fields

Minimum evidence:

- exposure denominator;
- response count;
- conversion count;
- qualified lead count;
- source link or export path;
- response-window dates;
- owner notes;
- confound notes.

Optional evidence:

- impressions;
- clicks;
- CTR;
- page visits;
- form starts;
- replies;
- call bookings;
- query cluster;
- creative hook category.

## Inconclusive Rules

Mark the result `inconclusive` when:

- the denominator is unknown;
- tracking/source evidence is missing;
- traffic is too thin to interpret;
- lead quality cannot be judged;
- the offer changed during the response window;
- a confound dominates the signal;
- owner review cannot happen.

Inconclusive is a valid outcome. It should produce a next action, not be treated as failure.

## Evidence Grade

Use simple grades until a stronger metric spec exists:

- `A`: source-linked, denominator known, lead quality reviewed, owner decision recorded.
- `B`: source-linked, denominator known, lead quality partially reviewed.
- `C`: source-linked but denominator or lead quality weak.
- `D`: anecdotal, useful for language only.
- `F`: no usable evidence.

## Owner Review

Owner review must answer:

1. What did we learn?
2. What remains unknown?
3. What should change next?
4. What should not be claimed?
5. Is the next action keep, revise, pause, retest, or inconclusive?

## Promotion Rule

Do not promote a message, claim, or channel lesson into reusable product knowledge unless:

- the source is linked;
- the evidence grade is `A` or `B`;
- the owner decision is recorded;
- the claim boundary is explicit;
- the result can be reused without implying guaranteed performance.
