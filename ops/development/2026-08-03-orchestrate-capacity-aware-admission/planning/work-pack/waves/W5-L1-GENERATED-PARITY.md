# W5 — Generated parity

- Unit: `SWU-OCA-005`
- Task: [TASK-OCA-05](../tasks/TASK-OCA-05-GENERATED-PARITY.md)
- Dependency: all canonical SWUs pass
- Concurrency: none

Generate into an isolated temporary target, review the exact package delta,
then sync only `.agents/skills/orchestrate`, `.arcanum/runtime/orchestrate`, and
`.claude/skills/orchestrate`. Do not broad-bootstrap this repository.

Gate on manifest parity, excluded tests/caches, and absence of unrelated
generated changes. This wave proves projection synchronization, not publication.
