# TASK-TRUSTED-KERNEL

## Objective

Repair the local proposal/disposition state machine and enforce the declared contracts before any authoritative write.

- Layer/slice: L0 / S-002
- Wave: W1
- Dependencies: TASK-REGRESSION-HARNESS
- Source contracts: [SPEC](../../../../SPEC.md), [architecture](../../../../ARCHITECTURE.md), [review findings](../../../architecture-review-2026-07-10/findings.md), [cross-task decisions](../shared/cross-task-decisions.md)
- Blockers: none; attested identity is explicitly deferred.

## State Contract

```text
proposal: awaiting_approval -> approved | rejected
approval: pending -> consumed | rejected
```

At L0, `approved` means the no-op disposition completed and one receipt was committed. It does not represent effectful invocation and does not assert a verified human identity.

## Smallest Working Units

### SWU-IDEAD-002: ID-Addressed Exact-Once Lifecycle

- Goal: replace singleton resolution with immutable envelope/approval IDs and one legal terminal transition.
- Dependencies: SWU-IDEAD-001.
- Write scope: `src/server.mjs`, `src/envelopes/dry-run-envelope.mjs`, one new state/reducer module if needed, focused lifecycle tests.
- Source anchors: `defaultState()`, prepare route, run route, approval route, `approveDryRunEnvelope()`; AR-CAND-002 and AR-CAND-005.
- Related context: current queue/read-model shape and SPEC typestate.

#### Ordered Rules

1. Store envelopes by `envelope_id` and approvals by `approval_id`; preserve deterministic list order separately if needed.
2. Bind approval to exactly one `envelope_id` and `run_id`.
3. Resolve a disposition command by approval ID, never by current selection.
4. Inside one serialized mutation boundary, require `approval.state === pending` and `envelope.state === awaiting_approval`.
5. Transition both records once; conflicting or replayed commands return `409 already_resolved` with no artifact, event, projection, or receipt write.
6. Keep `/api/envelopes/run` ID-addressed or remove its ambiguous singleton semantics; do not infer the target from UI selection.
7. Reconcile L0 prose by treating terminal approval as the no-op completion; reserve `running` for later actual invocation.

- Edge cases: two pending proposals; unknown ID; mismatched run/envelope binding; sequential replay; concurrent replay; approve after reject; reject after approve.
- Done criteria: all pending records remain reachable and exactly one terminal disposition succeeds.
- Acceptance evidence: focused tests show one `201/200` success and one `409` under concurrent replay, with one receipt total.
- Validation: focused Node test command plus `npm run smoke`.
- Execution owner: local-fallback.
- Handoff note: return the final state shape and route signatures for SWU-003 and SWU-006.

### SWU-IDEAD-003: Honest Operator Semantics, Rejection, And Closed Grants

- Goal: remove false identity claims, add rejection, and admit only normalized L0 grants.
- Dependencies: SWU-IDEAD-002.
- Write scope: `src/kernel/grants.mjs`, envelope/approval construction, approve/reject routes, focused tests, affected schema fields when needed.
- Source anchors: AR-CAND-001 and AR-CAND-004; `defaultGrants()`, `requiresApproval()`, browser `approved_by` body.
- Related context: GAP-IDEAD-001 and DEC-IDEAD-001/003.

#### Ordered Rules

1. Define a versioned L0 grant set containing only `preview.read` and `dry-run.noop` unless the approved design already names another no-op grant.
2. Require an array of unique strings; normalize by stable sort; reject unknown or duplicate declarations before persistence.
3. Remove `approved_by` from the request body and ignore/reject it if supplied.
4. Write a kernel-created actor descriptor: `{ kind: "local_operator_action", assurance: "unattested" }`.
5. Add `POST /api/approvals/:id/reject` with optional bounded reason text; rejection is terminal and writes disposition evidence but no success receipt.
6. Return stable machine error codes for invalid grant, unknown approval, and already-resolved disposition.

- Edge cases: empty grants; duplicate grants; unknown grant; caller identity spoof; overlong/non-string rejection reason; repeated rejection.
- Done criteria: records make no proved-human claim; all grant and terminal-state hostile tests pass.
- Acceptance evidence: persisted records contain only normalized grants and the kernel-created unattested descriptor.
- Validation: focused grants/disposition tests.
- Execution owner: local-fallback.
- Handoff note: document final request/response shapes for schema integration and UI.

### SWU-IDEAD-004: Draft 2020-12 Validation Adapter

- Goal: provide one reusable runtime validator for all declared project schemas.
- Dependencies: SWU-IDEAD-001.
- Write scope: `package.json`, package lock, `src/kernel/schema-validation.mjs`, schema fixtures, `tests/l0-schema-validation.test.mjs`.
- Source anchors: schema `$schema` declarations; AR-CAND-008; official Ajv Draft 2020-12 class documentation.
- Related context: DEC-IDEAD-004.

#### Ordered Rules

1. Install and lock Ajv through npm; import the Draft 2020-12 class from its dedicated export.
2. Load schemas from explicit known paths, compile once, and expose named validation functions.
3. Return stable structured errors with instance path, schema path, and keyword; do not leak stack traces to API clients.
4. Keep schema compilation failure fatal at server startup/test setup.
5. Add at least one valid and two hostile fixtures per schema.

- Edge cases: unknown schema name; malformed schema file; additional properties; wrong scalar/array type; missing required fields.
- Done criteria: all three schemas compile and fixtures produce deterministic pass/fail results.
- Acceptance evidence: focused unit-test output and lockfile diff.
- Validation: schema unit tests and `npm run validate:schemas` after SWU-005.
- Execution owner: local-fallback.
- Handoff note: return exported validator API and error shape.

### SWU-IDEAD-005: Runtime Admission And Emission Enforcement

- Goal: enforce schemas and policy at manifest, request, envelope, approval, and receipt boundaries before durable writes.
- Dependencies: SWU-IDEAD-003 and SWU-IDEAD-004.
- Write scope: `src/kernel/registry.mjs`, `src/server.mjs`, schemas, `scripts/validate-schemas.mjs`, focused tests.
- Source anchors: prepare/disposition routes, `loadModuleManifests()`, current parse-only script, AR-CAND-007/008.
- Related context: final request/record shapes from SWU-003.

#### Ordered Rules

1. Validate raw request shape before defaulting or constructing domain records.
2. Apply closed-grant policy after structural validation and before envelope creation.
3. Validate constructed envelope before event/projection persistence.
4. Validate approval/disposition and receipt objects before any authoritative append.
5. Validate every manifest through the same schema adapter; remove or narrow the handwritten duplicate.
6. Make `validate:schemas` compile schemas and validate all shipped manifests/fixtures; name the command honestly in output.
7. On validation failure, return `400 invalid_request` or fail startup for invalid shipped manifests; write nothing.

- Failure modes: defaulting masks malformed input; schema and policy errors collapse into 500; receipt invalidity discovered after artifact/event writes.
- Done criteria: every hostile invalid request/object fails before state, event, or artifact counts change.
- Acceptance evidence: before/after directory snapshots or counts in tests.
- Validation: `npm run validate:schemas`, schema tests, adversarial tests, smoke.
- Execution owner: local-fallback.
- Handoff note: return stable domain-validation API and any schema deltas required for later upstream synchronization.

## Synchronization

Do not update `SPEC.md`, `ARCHITECTURE.md`, or Craft in this task. Record evidence paths for TASK-VERIFY-READINESS.
