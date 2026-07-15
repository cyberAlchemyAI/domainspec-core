# Task Contract: Coverage, History, And Staleness

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-RDL-HISTORY` |
| Objective | Prove the same learning/proposal contract works across targets, revisions, and restart. |
| Layer / slice / wave | L1 / S-003 / W2 |
| Dependencies | W1 pass |
| Blockers | None inherent; shared IDE files still require live ownership check. |
| Execution | Sequential: coverage before history/stale projection. |

## Sources

- [Proposal state machine](../../ARCHITECTURE-BUNDLE.md#view-5--state)
- [L1 boundary](../../IMPLEMENTATION-LAYERING.md#layer-decision-table)
- [Traceability](../shared/traceability.md)

## SWU-RDL-007 — All-target coverage and representative nodes

- **Objective:** Generalize by data coverage, not per-node UI branches.
- **Dependencies:** SWU-RDL-006.
- **Write scope:** visibility copy data, coverage fixtures/tests, and minimal
  generic template logic only when coverage reveals a real shared need.
- **Rules:** every rendered interactive node/field/source has a stable contract;
  choose representative dependency, frontier, validation, and blocked-state
  nodes; assert the same UI/event shape; do not require every node to be the
  default selected path.
- **Done:** coverage is complete and representative nodes render/emit without
  node-ID conditionals.
- **Acceptance evidence:** machine-readable coverage matrix and browser cases.
- **Validation:** visibility suite and parameterized focused Playwright cases.
- **Owner:** `local-fallback`.
- **Handoff:** provide coverage matrix and representative fixture IDs to 008.

## SWU-RDL-008 — Proposal history, restart, and stale review

- **Objective:** Project durable submitted history honestly across refresh,
  restart, and changed review context.
- **Dependencies:** SWU-RDL-007.
- **Write scope:** focused IDE mode history projection/tests and visibility stale
  fixtures; no new authoritative database or owner effect endpoint.
- **Rules:** derive history from Canvas interactions; deduplicate by event/
  proposal ID; keep original bindings/value; after republish compare fingerprint,
  target, and observed value; show `stale-review-required` without rebasing;
  preserve cursor/restart semantics and current-revision admission.
- **Edge cases:** duplicate cursor poll, out-of-order display, missing current
  surface, same revision/new fingerprint impossible case, new revision/same
  inputs, removed field, interaction from other surface.
- **Done:** refresh/restart preserves submitted projection; all material mismatch
  cases are visibly stale; original proposal remains readable.
- **Acceptance evidence:** replay/restart fixture, before/after republish payloads,
  and browser states.
- **Validation:** focused Node replay/projector tests, existing Canvas replay
  suite, and Playwright republish/restart/stale journeys.
- **Owner:** `local-fallback`.
- **Handoff:** W2 closes with a stable event-to-review input contract for 009.

## Synchronization And Completion

Do not implement authentication, comments, notifications, or multi-user merge.
Any need for them is recorded as new evidence for a separate design.

