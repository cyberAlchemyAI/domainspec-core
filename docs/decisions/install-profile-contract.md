# Install Profile Contract Decision

Date: 2026-05-29
Status: accepted
Decision source: user selected option 1 after `TASK-RUNTIME-004 / SWU-RUNTIME-005` blocked on install profile semantics

## Decision

Use explicit native install profiles.

The bootstrap/install layer must support runtime-native generated packages without silent global mutation.

| Profile | Writes | Default mutation mode |
| --- | --- | --- |
| `personal-codex` | `$CODEX_HOME/skills/<name>/SKILL.md` and alias packages | explicit only; never included in repo-local `all` |
| `repo-local` | `tools/arcanum` or installed equivalent, `.arcanum/runtime/config.json`, adapter profiles | explicit |
| `github-copilot` | `.github/skills/*`, `.github/instructions/*`, `.github/copilot-instructions.md`, `AGENTS.md` | explicit |
| `claude` | `.claude/skills/*`, `.claude/agents/*`, `CLAUDE.md` | explicit |
| `observability` | `.arcanum/observability` config and structure markers only; ledgers local/generated unless promoted | explicit |
| `all` | `repo-local`, `github-copilot`, `claude`, `observability` | explicit; excludes `personal-codex` |
| `none` | no writes; source-only | n/a |

## Rationale

This keeps the canonical source singular while letting each runtime receive its best native package shape.

It also prevents repository bootstrap from silently mutating machine-global Codex state. Global Codex installation remains possible, but only through the explicit `personal-codex` profile.

## Rejected Options

### Convenience all-in

Rejected because including `personal-codex` in `all` would allow repo bootstrap to mutate `$CODEX_HOME` unexpectedly.

### Repo-only strict

Rejected because making `personal-codex` dry-run only would make actual Codex skill installation less useful for the operator.

## Downstream Impact

- `bootstrap_arcanum.sh` should add profile semantics or map profiles to exact surfaces.
- `install_arcanum.sh` should document profile behavior.
- Default install behavior must not generate `.codex/commands`.
- `none` must perform no writes.
- `all` must remain repository-local/runtime-local and must not include `personal-codex`.
- Generated native packages must record canonical source, runtime, generator, mutation policy, and alias status.

## Remaining Decisions

- Exact provenance file shape for generated native packages.
- Whether observability JSONL ledgers are ever promoted to tracked durable evidence by default.
