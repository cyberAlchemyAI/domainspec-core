# Sigil Development Change Receipt — Task Session zero-argument resume

## Decision

- Target: `task-session`
- Mode: `update`
- Tier: `arcana`
- Approved scope: no-argument nearest-SWU resolution and durable
  current-session recovery
- Iteration: targeted update
- Core contract: preserved — Task Session executes at most one bounded
  task/SWU

## Canonical change

- Version: `0.5.0` to `0.6.0`.
- A no-argument invocation now enters `resume-nearest`.
- Current-session evidence, an exact native-session cursor, cwd locality, and
  uniquely scope-matched continuity form a strict precedence chain.
- `--list-nearest` previews without mutation.
- `--from <path>` and `--session <id>` provide explicit overrides.
- Closeout writes or updates one schema-valid continuity cursor; the current
  native runtime session id is preferred, with a stable scope-derived fallback.
- The cursor is only a selector. The live work pack remains task/readiness
  authority and must pass the full Task Session gate.

## Preserved boundaries

- No global-latest telemetry selection.
- No fuzzy or cross-project inference.
- No claim that compacted conversational tokens remain accessible.
- No silent fallback from stale or contradictory high-priority evidence.
- No recursive execution: one invocation still executes at most one SWU.
- No consuming-project vocabulary was added to the public canonical package.

## Generated surfaces

The installer was staged outside the checkout and only the generated
`task-session` packages were synchronized into:

- `.agents/skills/task-session/`
- `.claude/skills/task-session/`

Runtime support now includes the policy, cursor schema, resolver script, and
existing adapters.

## Validation

- Existing policy fixtures: `19/19` pass.
- Nearest-resolution fixtures: `11/11` pass.
- Canonical/Codex/Claude contract and support parity: pass.
- Runtime-session no-flag fixture: pass.
- Real IOLM cwd preview: pass.
- Repository-root no-evidence negative control: pass.
- Python and JSON syntax: pass.
- Diff hygiene: pass.
- Product-neutral wording: pass.

## Lifecycle state

- Observer: local fallback; a repository-governed subagent dispatch would have
  required a separate confirmation gate.
- Reflection trigger: manual.
- Experiment Harness: pass.
- Next lifecycle step: observe repeated no-argument executions and revise only
  if their durable cursor evidence shows a recurrent gap.
