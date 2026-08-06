# Stage 02 — Invoke Define

## Definition target

Define one `AKV non-vacuity repair contract` with two jointly mandatory surfaces. The target is not repaired if either surface remains open.

### Surface A — QRY-003 terminal closure

1. The only primary abstention codes are:
   `ABSTAIN_UNKNOWN_VERSION`, `ABSTAIN_RUNTIME_CONTEXT`, `ABSTAIN_CONFLICT`, `ABSTAIN_PERFORMANCE_EVIDENCE`, `ABSTAIN_MISSING_SOURCE`, and `ABSTAIN_AMBIGUOUS_INTENT`.
2. A tie emits `ABSTAIN_AMBIGUOUS_INTENT`; `ABSTAIN_AMBIGUOUS_CHOICE` is not admitted.
3. Missing version maps to `ABSTAIN_UNKNOWN_VERSION`; an understood feature without a binding maps to `ABSTAIN_MISSING_SOURCE`; unrecognized intent maps to `ABSTAIN_AMBIGUOUS_INTENT`.
4. Simultaneous failures choose one primary code in the declared priority order and preserve subordinate gaps.
5. Success requires non-empty `selected_ids` and `abstention_code = null`; abstention requires a declared non-null code.
6. A repair increments `algorithm_version` and never rewrites historical receipts.
7. Eight named fixtures cover positive JS, positive WAAPI, tie, missing version, missing source, conflict, performance evidence, and precedence. They remain planned.

### Surface B — relation behavioral effect

For each relation candidate, the repair contract requires one of:

- `RETAIN`: exact source and target fixture, named consumer, baseline output, edge/property mutant, expected observable delta, and failure assertion;
- `MERGE`: canonical-representation choice or a fail-closed equality validator plus mismatch fixture;
- `DEFER`: no retention until an exact traversal, output field, or view transform is specified;
- `KILL`: remove the candidate when no necessary behavior can be recovered.

Current closed-evidence disposition is 17 `RETAIN`, five `MERGE`, three `DEFER`, and zero `KILL`.

## Acceptance criteria

- The query matrix contains eight terminal paths, no undeclared repair code, and explicit success/abstention receipt invariants.
- The relation matrix contains exactly 25 unique relation IDs, each with one disposition.
- Every `RETAIN` row has a planned discriminating delta.
- No `MERGE` or `DEFER` row is represented as retained.
- All fixtures and witnesses are labelled `planned_not_executed`.
- The closed research artifacts remain unchanged and no ontology package is created.

## Non-goals

This definition does not implement validators, run fixtures, create the knowledge graph, ingest Anime.js documentation, publish artifacts, or establish production readiness.
