# Context Pack: SWU-SCW-001

## Selection

- Work-pack: `projects/ide-extension/development/session-content-workbench-plan/WORK-PACK.md`
- Task: `TASK-CANVAS-CONTRACT`
- SWU: `SWU-SCW-001`
- Mode: standard, local Task Session
- Runtime handoff: not requested

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Define publish and interaction request contracts. | Task contract and accepted architecture core contracts. | covered |
| O2 | Define projected surface/revision/interaction vocabulary. | Implementation plan data model and glossary. | covered |
| O3 | Preserve current schemas, fixtures, and runtime behavior. | Schema registry, validator, current contract/schema tests. | covered |
| O4 | Reject malformed path, kind, id, event, payload, and additional fields. | Task rules and current strict-schema convention. | covered |
| O5 | Keep exact serialized-size enforcement at the HTTP boundary. | Task plan failure rules and server ownership in SWU-006. | resolved-deferred |
| O6 | Provide deterministic validation and no server/projector mutation. | Work-pack write scope and package test scripts. | covered |

## Controlling Sources

1. `work-pack/tasks/TASK-CANVAS-CONTRACT.md`, SWU-SCW-001 owns exact scope,
   rules, edge cases, done criteria, and validation.
2. `session-content-canvas-design/DECISIONS.md` fixes trusted local HTML,
   complete revisions, and separate publish/event polling.
3. `session-content-canvas-design/ARCHITECTURE-BUNDLE.md` defines the publish,
   surface, revision, and interaction shapes.
4. `SPEC.md` and `ARCHITECTURE.md` are the current project contract authority.
5. `src/kernel/schema-validation.mjs`, `scripts/validate-schemas.mjs`, existing
   schemas/fixtures, and schema tests define the strict brownfield pattern.

## Execution Decisions

- Use independent canvas `schema_version: "1"`; this is a new protocol family,
  not a reinterpretation of bridge schema version 2.
- Require normalized workspace-relative `.html` paths and reject absolute,
  traversal, backslash, percent-encoded, and non-HTML forms at the contract.
- Permit recursive JSON-compatible interaction payloads with bounded members;
  enforce the complete request's 16 KiB serialized cap at the SWU-006 HTTP
  boundary because JSON Schema cannot measure encoded byte length.
- Add no server route, projector branch, CLI behavior, or browser behavior.

## Gates

- Dependency: none, pass.
- Decisions: all product blockers resolved; no task blocker.
- Write scope: complete and bounded.
- Validation: schema validator, focused canvas contracts, existing schema and
  bridge contracts available.
- Strict coverage: pass, six of six obligations covered or explicitly deferred
  to their owning SWU.

## Required Evidence

- New valid fixtures pass and hostile fixtures fail at intended keywords.
- Every existing schema and fixture still validates.
- Focused canvas contract and existing bridge contract/schema suites pass.
- No server, projector, CLI, workbench, or persisted state file changes.
