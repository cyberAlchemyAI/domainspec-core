# TASK-IRO-GATE-001 — Public boundary gate

## SWU-IRO-001

Outcome: one no-code durable decision bundle that either binds or blocks public
extraction, canonical API/name/license/compatibility, catalog projector,
request normalization, ACI reference fields, and the disposable consumer.

Exact execution mechanics are owned by
[`EXECUTION-CONTRACT.json`](../shared/EXECUTION-CONTRACT.json). The unit writes
only the fixed coordinator outputs plus the four decision-bundle artifacts
declared there. The decision bundle, terminal receipt, and closeout-owner
receipt must validate against the shared schemas.

Inputs:

- accepted research closure and validation addendum;
- Define/Design receipts;
- [cross-task gaps](../shared/CROSS-TASK-GAPS.md);
- `.arcanum/profiles/decision-profile.yml`.

Done:

- profile digest and exact evidence digests are recorded;
- each binding names an accountable owner/path/contract or is explicitly unresolved;
- one-question-at-a-time interrogation is used for human-only assignments;
- `pass` requires zero unresolved mutation-critical bindings;
- `block` names repair owners and does not select implementation;
- no source, public, generated, consumer, product, or private runtime file is changed.

Successor projection is exactly `SWU-IRO-002`; it pauses for explicit
candidate-mutation approval and never executes the successor.

