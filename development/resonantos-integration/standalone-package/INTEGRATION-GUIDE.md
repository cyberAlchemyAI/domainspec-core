# CyberAlchemy Governance Integration Guide

## What This Is

CyberAlchemy is the governance layer for the host archive's write side. It does not replace the host
archive. The host archive owns the read map: what is present, what is still true, how confident it
is, and how useful it is. CyberAlchemy owns the decision layer: whether the archive may rely on a
candidate, who decided, and what promotion state applies.

## Separation Of Responsibilities

- The host archive owns read, lookup, recall importance, temporal validity, supersession, confidence,
  utility, and contradiction handling.
- CyberAlchemy owns governed-write contracts: candidate records, promotion ownership, default-deny
  review, no-promotion guardrails, receipt debt, and host-side trusted-write body rules.

## Host Hooks

Expected host surfaces:

- Read/search tools for lookup and observer measurement.
- Intake-only write or request-ingest tools for candidate capture.
- A Review Queue or equivalent owner-gated review surface.
- A decide step with approve, reject, and escalate outcomes.
- A trusted-write promotion seam that only the host-side provider may execute.

## Round Trip

1. Intake writes a candidate record with exactly one scope tag.
2. The candidate appears in the Review Queue.
3. A responsible owner decides approve, reject, or escalate.
4. On approve, the host-side trusted-write provider body performs the trusted write.
5. The host read path returns promoted content through its existing lookup machinery.

## First Safe Slice

Start with a read-only observer/meter. It attaches to read/search behavior only, emits measurement
receipts, and performs no intake, decide, promote, or trusted-write action.

## Later Slices

After the read-only observer and candidate fixtures are green:

1. Add scope-tagged intake adapters.
2. Add Review Queue candidate fixtures and no-promotion policy.
3. Implement the host-side trusted-write provider body.
