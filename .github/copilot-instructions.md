# domainspec-core Copilot Scope

This repository is the research orchestration root for the 3-repo DomainSpec topology.

## Primary scope

- Research design and execution planning
- Experiment traceability and analysis
- Cross-repository governance and drift control

## Out of scope

- Direct ownership of reusable Type A implementation pack assets
- Product feature implementation in poker-team

## Ownership model

- Type A canonical DomainSpec pack: `implementation/domainspec/copilot`
- Type A canonical MARS reusable assets: `implementation/mars`
- Type B research orchestration assets: `domainspec-core/.github`
- Type C project-local overlays: consumer repositories (for example `validation/poker-team/.github`)

## Operational checks

Run this before research phase transitions and release checkpoints:

```bash
./tools/check_github_drift.sh
```

Treat failures as blockers until classified and resolved in `ops/AGENT-SKILL-TRIAGE-MATRIX.md`.

## DomainSpec routing policy

- For natural-language DomainSpec requests that do not name a command explicitly, route through `domainspec-orchestrate` as the default user-facing entrypoint.
- If the user explicitly invokes a `domainspec-*` command, run that exact specialist command unchanged (advanced/internal direct mode remains supported).
- Keep DomainSpec routing DomainSpec-only by default; do not invoke `gsd-*` flows unless the user explicitly asks for GSD.

## Terminal execution hardening

- Prefer non-interactive command paths for automation (for example disable git prompts and interactive auth).
- For long-running operations, use bounded execution with timeout + explicit recovery behavior.
- If a terminal execution breaks or stalls, recover deterministically: capture output, kill stale session, rerun once with safer flags, then return BLOCK with remediation if still failing.
- For risky or unknown commands, run a preflight nudge (`./tools/terminal_guard.sh nudge -- <command...>`) and prefer guarded execution (`./tools/terminal_guard.sh run --timeout <sec> -- <command...>`).
- Reconcile delegation telemetry after interruptions so no stale `outcome: started` rows remain unresolved (for example run `./tools/reconcile_delegation_tuning.sh`).
- Never rely on `exit` inside iterative helper loops; propagate status codes to avoid killing reusable shell sessions.
