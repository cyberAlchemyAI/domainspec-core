# IRO-FULL-STREAM

Status: `goal-authored-not-started`

## Outcome

Complete the intent-route Arcanum add-on objective through one ordered,
owner-routed stream while preserving candidate, canonical, generated,
consumer, and private authority boundaries. Completion requires IRO-VERIFY to
back every lifecycle claim with joined receipts; persistence across turns never
grants an owner approval.

## Ordered units

| Unit | Allowed capabilities | Required receipts | Successor and pause |
|---|---|---|---|
| IRO-001 | `context-builder`, `decision-gate`, `task-session`, `invoke:refresh` | decision bundle, terminal, closeout-owner | IRO-002; pause for candidate-mutation approval |
| IRO-002 | `task-session`, `sigil-development` | terminal, closeout-owner | IRO-003 |
| IRO-003 | `task-session`, `sigil-development`, shared Playwright | terminal, closeout-owner, browser provenance | IRO-004; pause for public owner and clean-worktree receipt |
| IRO-004 | `task-session`, `sigil-development` | canonical acceptance, terminal, closeout-owner | IRO-005 |
| IRO-005 | `task-session`, `arcanum-bootstrap`, shared Playwright | profile-parity/rollback, terminal, closeout-owner | IRO-006; pause for disposable consumer approval |
| IRO-006 | `task-session` | install/rollback, terminal, closeout-owner | IRO-007; pause for ResonantOS planning scope |
| IRO-007 | `task-session`, `invoke:refresh` | planning material, terminal, closeout-owner | IRO-008; pause for orchestrator/catalog/normalization bindings |
| IRO-008 | `task-session` | adapter matrix, terminal, closeout-owner | IRO-009; pause for private owner and field bindings |
| IRO-009 | `task-session` | private admission, terminal, closeout-owner | IRO-VERIFY |
| IRO-VERIFY | `task-session` | verification terminal and closeout-owner | `__complete__` |

The exact capability-to-unit allowlist, commands, outputs, owner material
declarations, dependencies, and successor values are authoritative in
`planning/work-pack/shared/EXECUTION-CONTRACT.json`.

## Budgets

- Task Session requests: 10 maximum, one per unit.
- Repair cycles: one per unit; a second failure pauses.
- Active helpers: one maximum, only after exact owner/operator authorization.
- Browser launches: two maximum, IRO-003 and IRO-005 only.
- Network calls: zero unless a later exact owner contract authorizes one.

## Receipt and closeout law

- Every unit writes a schema-valid immutable terminal receipt and a separately
  joined closeout-owner receipt at its fixed epoch path.
- IRO-001 also writes the four decision-bundle artifacts.
- Closeout targets are exact paths with SHA-256 or `absent` baselines.
- Only `evidence_added`, `blocker_opened`, `blocker_resolved`,
  `status_changed`, and `route_changed` are admitted closeout deltas.
- A pass projects exactly one successor; projection does not select or execute it.

## Pause gates

Pause before IRO-002, IRO-004, IRO-006, IRO-007, IRO-008, and IRO-009.
Resume only when the exact approval/owner receipt named in the execution
contract exists and validates. A missing or ambiguous locator, owner, scope,
field binding, or clean-worktree receipt is a blocker, not an exploration task.

## Epoch and stop rules

Regenerate Context and WPRA after any semantic owner, material, validation,
receipt, closeout, or successor change. Stop and report on stale evidence,
wrong owner, out-of-scope write, failed acceptance validation, private/public
boundary breach, ambiguous successor, a second repair failure, or any request
to infer promotion/release/deployment authority.

## Readiness ceiling

WPRA v2 verdict is `pass`/`PROJECTION_READY`, but `selected_unit=null`,
`mutation_ready=false`, `approval_status=unapproved`, and
`chain_status=not-started`. Starting the native Goal is a separate runtime
action. The first executable frontier after that action is IRO-001 only.

## Runtime evidence matrix

Execution contract v1.1 adds the complete Task Session and outer-chain receipt set. The prior WPRA epoch is stale by the stream's own epoch rule; the next runnable frontier remains IRO-001 only after regeneration and exact Goal-start approval.
