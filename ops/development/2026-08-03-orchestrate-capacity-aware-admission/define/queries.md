# Queries

## ObserveCapacityEvidence

Returns the exact evidence handle supplied by the active host adapter. The
query may return `unsupported` or `unknown`; it must not synthesize a total from
agent inventory.

Minimum result fields:

- schema version and evidence ID;
- host ID and capacity-scope ID;
- session/tree ID when available;
- run ID and wave ID;
- observed-at and expires-at;
- authority class: `authoritative`, `advisory`, or `unknown`;
- requested units, spawnable units when authoritative, and occupied categories;
- reservation support and reservation handle when present;
- source operation/metadata handle and residue.

## CapacityRouteOptions

Returns zero or more owner-backed revision offers for a blocked decision.

Each option names:

- route option ID and plain label;
- capability owner;
- topology effect;
- evidence prerequisite;
- whether Dispatch validation is required;
- whether renewed user confirmation is required;
- exact next handle or an honest unavailable reason.

## ReadSlotLifecycleObservation

Returns host evidence for a known native agent or `unknown`. It never derives
physical release from Orchestrate's logical close event.

