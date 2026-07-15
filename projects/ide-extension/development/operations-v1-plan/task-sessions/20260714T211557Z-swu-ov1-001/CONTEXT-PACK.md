# Context Pack: SWU-OV1-001

- Task: `SWU-OV1-001` - Versioned Contract And Budget Baseline
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local

This file is session evidence. It is not a canonical planning or contract
source.

## Objective

Add strict Operations V1 request schemas, fixed UTF-8/storage constants,
additive event-version vocabulary, boundary fixtures, and focused tests without
adding runtime routes, events, blobs, parser behavior, or changing V0 APIs.

## Obligation Matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| O1 | Register strict derivation, operation, navigation, acknowledgement, pruning preview, and pruning commit schemas. | Task contract `SWU-OV1-001`; architecture sections 3 and Navigation Boundary. | covered |
| O2 | Permit only `whole_document`; bind append/replace to inline HTML and rebuild to exact-hash workspace HTML. | `DECISIONS.md` OV1-D4/D5; `ARCHITECTURE-BUNDLE.md` Content Operation Contract. | covered |
| O3 | Enforce `additionalProperties: false`, bounded IDs, digest patterns, and discriminated mode/input pairs. | Task contract implementation detail and boundary matrix. | covered |
| O4 | Freeze 5 MiB HTTP, 4 MiB source, 512 KiB fragment, 8 MiB result, 1 GiB soft, 2 GiB hard, seven-day grace, and reclaim-below-soft. | OVG-002/003; cross-task decisions OV1-PD3/PD8; task contract. | covered |
| O5 | Make UTF-8 bytes authoritative with minus-one, exact, plus-one, and multibyte tests. | Task contract boundary matrix and OVG-002. | covered |
| O6 | Freeze additive event version 4 and the declared Operations V1 event names without emitting events. | Task contract; blob/replay task event vocabulary. | covered |
| O7 | Preserve every existing schema, fixture, V0 route, identity, and behavior. | Shared context Preserved V0 Behavior; work-pack gate checks. | covered |
| O8 | Run `validate:schemas`, `test:schemas`, and `test:operations-contracts`. | Task contract Validation. | covered |
| O9 | Do not add routes, event reducers, storage, blobs, parser logic, environment overrides, regions, or protected effects. | Task contract Failure modes; work-pack Delivery Boundary and Gate Checks. | covered |
| O10 | Synchronize status only from passing Task Session evidence. | Task contract Synchronization; work-pack Expected Result Shape. | covered |

## Selected Context

1. `development/operations-v1-plan/WORK-PACK.md`
   - Selectors: SWU manifest, blockers and gaps, gate checks, next route.
   - Covers: O7, O9, O10.
2. `development/operations-v1-plan/work-pack/tasks/TASK-CONTRACT-TRANSFORM.md`
   - Selector: `SWU-OV1-001` and Synchronization.
   - Covers: O1-O10.
3. `development/operations-v1-plan/work-pack/waves/W0.md`
   - Selectors: entry, exit, promotion, stop.
   - Covers: O8, O10.
4. `development/operations-v1-plan/work-pack/shared/context.md`
   - Selectors: Preserved V0 Behavior, Operations V1 Boundary, Worktree Rule.
   - Covers: O7, O9.
5. `development/operations-v1-plan/work-pack/shared/cross-task-decisions.md`
   - Selectors: OV1-PD1 through OV1-PD12.
   - Covers: O2, O4, O7, O9.
6. `development/operations-v1-design/PLANNING-DECISION-GATE.md`
   - Selectors: closed gate and OVG-001 through OVG-004 selections.
   - Covers: O4, O5, O9.
7. `development/operations-v1-design/DECISIONS.md`
   - Selectors: OV1-D1 through OV1-D9.
   - Covers: O2, O7, O9.
8. `development/operations-v1-design/ARCHITECTURE-BUNDLE.md`
   - Selectors: Surface Derivation, Content Operation Contract, Navigation Boundary.
   - Covers: O1-O3, O7.
9. `src/kernel/schema-validation.mjs`
   - Selectors: `SCHEMA_FILES`, validator creation, wrapper export pattern.
   - Covers: O1, O7.
10. `scripts/validate-schemas.mjs`
    - Selectors: registry/file equality and valid/invalid fixture convention.
    - Covers: O1, O8.
11. `tests/session-content-workbench-contracts.test.mjs`
    - Selectors: fixture loading, keyword assertions, existing canvas compatibility.
    - Covers: O3, O7, O8.
12. `development/operations-v1-plan/work-pack/tasks/TASK-REBUILD-NAVIGATION.md`
    - Selectors: navigation interfaces and transient acknowledgement behavior.
    - Covers: O1, O9.
13. `development/operations-v1-plan/work-pack/tasks/TASK-RETENTION.md`
    - Selectors: pruning preview/commit interfaces and candidate digest rule.
    - Covers: O1, O4.

## Decisions And Assumptions

- Selected by prior human gate: direct `parse5` 8.0.1, fixed budgets,
  threshold-and-grace retention, and durable target with transient refresh.
- Schema names follow the existing `<contract>-request` registry convention.
- Derivation uses the architecture field name
  `operation_surface_idempotency_key` rather than inventing a shorter alias.
- Navigation acknowledgement is intentionally minimal:
  `{ schema_version, status: loaded | failed }`. Command identity is carried by
  the route. `SWU-OV1-009` may change this only through an explicit contract
  migration if runtime diagnostics prove another field necessary.
- Pruning preview accepts `{ schema_version, command_id }`; pruning commit adds
  `expected_candidate_digest`, matching the retention task interface.
- Byte limits live in runtime constants and helpers. JSON Schema character
  length is not used as byte authority.

## Write Scope

- New Operations V1 schemas under `schemas/`.
- New valid/invalid fixtures under `tests/fixtures/schemas/`.
- `src/kernel/schema-validation.mjs` registry and wrappers.
- New `src/kernel/operations-contracts.mjs` constants and UTF-8 helpers.
- New focused Operations V1 contract tests.
- `package.json` only for `test:operations-contracts`.
- Task Session evidence and status synchronization after passing validation.

## Excluded

- Server routes and request-body admission.
- Projector/event emission and replay.
- Blob or workspace storage.
- HTML parsing or serialization.
- Region targets, merge/rebase, collaboration, remote control, provider calls,
  and protected effects.

## Validation

1. `npm run validate:schemas`
2. `npm run test:schemas`
3. `npm run test:operations-contracts`
4. Focused scoped diff and whitespace checks.

## Context Builder Result

- Files selected: 13
- Obligation coverage: 10/10, 100 percent
- Strict coverage: pass
- Blockers: 0
- Fallback search: acknowledgement and pruning field names only; resolved above
- Noise: bounded to explicit task handles and two downstream contract selectors
