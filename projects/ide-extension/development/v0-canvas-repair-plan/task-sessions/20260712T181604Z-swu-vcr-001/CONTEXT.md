# Context Pack: SWU-VCR-001

## Selection

- Work-pack: `projects/ide-extension/development/v0-canvas-repair-plan/WORK-PACK.md`
- Task: `TASK-CANVAS-POLICY`
- SWU: `SWU-VCR-001`
- Mode: lean, strict local Task Session
- Runtime handoff: not requested

## Obligations

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| O1 | Narrow approval and receipt scope to protected effects. | `ARCHITECTURE.md:14-16`, task rule 1. | covered |
| O2 | Declare a narrow trusted-local canvas preview/display exception. | `SPEC.md:224-259`, VCR-D1, G1-A/G1-I. | covered |
| O3 | Distinguish `canvas.surface_published` audit evidence from receipt records. | `SPEC.md:163-194`, G1-R, VCR-D2. | covered |
| O4 | Preserve approval/receipt requirements for source writes and other protected effects. | `SPEC.md:90-99`, task rule 5. | covered |
| O5 | Narrow "one complete read" to bytes from one opened file read, not an atomic snapshot. | `SPEC.md:243-246`, K2/P2, VCR-D4. | covered |
| O6 | Change docs only; preserve schemas and runtime behavior. | Task exact write scope and rule 7. | covered |

## Selected Evidence

1. `work-pack/tasks/TASK-CANVAS-POLICY.md`, SWU-VCR-001: exact scope,
   implementation rules, edge cases, done criteria, and validation.
2. `work-pack/shared/cross-task-decisions.md`, VCR-D1/D2/D4: selected authority
   and read-coherence decisions.
3. `html-builder-architecture-review/findings.md`, G1-A/G1-R/G1-I/K2/P2:
   accepted defects and allowed repair choices.
4. `SPEC.md`, In Scope, Out Of Scope, Receipt Contract, and Session Content
   Workbench V0: current owner clauses that must become non-contradictory.
5. `ARCHITECTURE.md`, One Sentence, Evidence Loop, and Session Content
   Workbench V0: current architecture boundary and event path.

## Execution Decisions

- Treat canvas publication and display as local preview/read behavior over an
  operator-controlled workspace artifact.
- Do not require or synthesize an approval record or receipt for current canvas
  publication.
- Keep `canvas.surface_published` as append-only audit evidence with surface and
  revision bindings, explicitly outside receipt schema semantics.
- Preserve all existing protected-effect gates outside this named exception.
- Describe current V0 admission as one opened-file byte read, without atomic
  snapshot or hostile writer claims.

## Gates

- Dependency: none, pass.
- Human decision: already resolved by VCR-D1/VCR-D2 and operator-confirmed
  value-first V0 direction; no new blocker.
- Write scope: `SPEC.md`, `ARCHITECTURE.md`, and this Task Session evidence.
- Validation: exact phrase checks, accepted-finding mapping, and scoped diff
  check are available.
- Strict coverage: pass, 6/6 obligations covered.

## Excluded Context

- Operations V1 design: excluded because no operation API or storage behavior
  is implemented by this SWU.
- Runtime source and tests: excluded because rule 7 makes them read-only and no
  behavior change is allowed.
- Hostile HTML and remote security: deferred by the accepted V0 contract.
