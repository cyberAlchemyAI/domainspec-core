# Task Contract: Roadmap Lab Contracts

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-RDL-CONTRACTS` |
| Objective | Establish stable presentation-copy and semantic-event oracles before behavior changes. |
| Layer / slice / wave | L0 / S-001 / W0 |
| Dependencies | Approved design/plan; execution-time dirty-scope review |
| Blockers | None inherent; stop on ownership overlap or inability to separate copy from authority. |
| Execution | One selected SWU per Task Session; no concurrent mutation. |
| Status | Completed: SWU-RDL-001 and SWU-RDL-002 passed. |

## Sources

- [Architecture concept/interface views](../../ARCHITECTURE-BUNDLE.md#view-3--concept-and-type)
- [UX proposal classes](../../UX-PLAN.md#proposal-classes)
- [Decision RDL-D04/D05](../../DESIGN-DECISIONS.md)
- Current `visibility/roadmap.template.html` human mappings and
  `visibility/tests/test_build_roadmap.py` copy assertions.
- Existing generic `projects/ide-extension/schemas/canvas-interaction-request.schema.json`.

## SWU-RDL-001 — Presentation-copy oracle

- **Objective:** Define stable, presentation-only fields that can be targeted by
  a copy proposal without touching roadmap identity or claims.
- **Dependencies:** none.
- **Write scope:** new files under
  `projects/domainspec-v2/development/first-production-release/visibility/schemas/`,
  `visibility/tests/fixtures/roadmap-copy/`, and one focused new contract test.
  No builder/template/runtime edit.
- **Rules:** require schema version, unique bounded `field_id`, valid `node_id`,
  enumerated role, nonblank human text, and no additional fields; cover valid,
  duplicate, unknown-node, missing-role, blank, and forbidden authority-field
  fixtures.
- **Done:** the contract distinguishes presentation text from node/claim/Craft
  fields and every invalid fixture fails for its intended reason.
- **Acceptance evidence:** schema path, fixture matrix/count, focused test output,
  and confirmation that no current presentation behavior changed.
- **Validation:**
  `python3 -m unittest discover -s projects/domainspec-v2/development/first-production-release/visibility/tests -p 'test_roadmap_contracts.py'`.
- **Owner:** `local-fallback`.
- **Handoff:** return the precise field roles and unresolved extraction cases;
  enable SWU-RDL-003 only on pass.
- **Result:** [PASS](../../task-sessions/20260714T215441Z-swu-rdl-001/TASK-SESSION-RESULT.md) —
  Draft 2020-12 schema, one valid fixture, six intentional invalid fixtures,
  five focused tests, and unchanged builder/template/manifest inputs.

## SWU-RDL-002 — Semantic-event oracle

- **Objective:** Define strict event-specific payloads inside the existing
  generic Canvas envelope.
- **Dependencies:** none.
- **Write scope:** new visibility event schema(s), fixtures, and focused contract
  tests only. Do not register a DomainSpec schema in the generic IDE kernel.
- **Rules:** cover the five named events in `IMPLEMENTATION-PLAN.md`; require
  immutable dual bindings and participant/node/target fields; use discriminated
  proposal classes; bound strings/arrays; reject extra fields, arrays as payload,
  editable/absent bindings, oversized examples, and disposition without owner
  evidence reference.
- **Done:** valid payloads compose into but do not redefine the current Canvas
  request; invalid variants fail closed in the private contract suite.
- **Acceptance evidence:** positive/negative matrix, serialized-size checks, and
  a documented second-validation requirement for the review adapter.
- **Validation:** same focused contract command plus JSON parse/schema checks.
- **Owner:** `local-fallback`.
- **Handoff:** return schema version/event-name table; enable SWU-RDL-004 only
  after both W0 oracles pass.
- **Result:** [PASS](../../task-sessions/20260714T215923Z-swu-rdl-002/TASK-SESSION-RESULT.md) —
  private Draft 2020-12 semantic event union, nine valid fixtures, eight
  invalid fixtures, total-size guard, generic Canvas composition proof, and no
  runtime registration in IDE public/source/schema/test surfaces.

## Synchronization And Completion

W0 is closed: both oracles pass and `WORK-PACK.md` records receipts.
Changes to event names or copy roles after W0 require explicit downstream
impact review across builder, UI, history, adapter, and traceability.
