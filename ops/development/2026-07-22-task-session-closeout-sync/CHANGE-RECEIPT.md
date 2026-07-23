# Sigil Development Change Receipt — Task Session closeout sync

## Decision

- Target: `task-session`
- Mode: `update`
- Tier: `arcana`
- Approved scope: required bounded closeout synchronization after one terminal
  task/SWU result
- Iteration: targeted update
- Core contract: preserved — Task Session still executes exactly one bounded
  task/SWU

## Canonical change

- Version: `0.4.1` to `0.5.0`
- Task Session now assembles a typed closeout record from the source receipt,
  declared target inventory, baselines, delta classes, validation, and expected
  owner receipt.
- When the delta is deterministic and within policy, Task Session derives one
  exact `invoke:refresh:apply-approved` authorization and sends it through
  Continuation Router.
- Invoke remains the mutation owner and returns a separate receipt.
- The synchronized next route is returned but never executed during closeout.

## Preserved boundaries

- Existing decision and validation hardening is preserved.
- `--follow-next-route` remains optional for continuation beyond closeout.
- No authorization is derived for implementation, another task, authority,
  promotion, publication, deployment, destructive cleanup, policy/cost/risk,
  ambiguous successor selection, or unrelated targets.
- A required but incomplete closeout blocks while preserving the execution
  result separately.

## Generated surfaces

The installer was staged outside the checkout and only the generated
`task-session` packages were synchronized into:

- `.agents/skills/task-session/`
- `.claude/skills/task-session/`

No full bootstrap or unrelated skill regeneration ran.

## Validation

- Deterministic fixtures: `19/19` pass.
- Canonical/Codex/Claude contract body parity: pass.
- Canonical/Codex/Claude policy parity: pass.
- JSON syntax: pass.
- Python validator syntax: pass.
- Markdown/diff hygiene: pass.
- Product-neutral wording: pass.
- Real closeout negative control: pass; stale target baselines blocked with no
  mutation and no second approval prompt.

## Lifecycle state

- Observer: local fallback, because a new repository-governed subagent dispatch
  would require a separate confirmation gate.
- Reflection trigger: manual.
- Experiment Harness: pass.
- Next lifecycle step: observe the first passing consuming-project closeout
  after the current target drift is rebased by its owner.
