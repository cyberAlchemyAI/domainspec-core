# Execution Pack: Memory / Knowledge Mesh

Date: 2026-05-31

## Execution Order

1. Run `TASK-MK-001` as a docs-only task-session.
2. Run `TASK-MK-002` validation immediately after `TASK-MK-001`.
3. Stop before `TASK-MK-003` unless a runnable Python test surface is available or substitute validation is explicitly accepted.

## Current Selected Task

Selected task: `TASK-MK-001`
Task-session directory: `docs/strategy/development/task-sessions/2026-05-31-memory-knowledge-index/`

## Operator Constraints

- Law 3: do not read multiple org contexts.
- Do not mutate runtime memory without explicit task scope.
- Do not use the deprecated customer-facing posture term except as a quoted deprecation note.
- Preserve BYOK and local-first assumptions.

## Evidence Rules

Every layer-index row must cite a repository path. If a surface is absent in the current checkout, state that as current truth rather than inferring it from memory.

## Stop Conditions

Stop and record blocker when:

- a planned code change cannot be validated
- a task needs an org context not named by the operator
- current runtime behavior conflicts with the plan
- mutation authority is ambiguous

