---
surface_kind: generated-native-runtime-package
runtime: github-copilot
canonical_source: spells/arcanum-bootstrap/README.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
---

# Arcanum Bootstrap

## Identity

- Canonical ID: `arcanum-bootstrap`
- Aliases: `Arcanum Install`, `Sigil Forge Install`
- Scope: library

## Purpose

Arcanum Bootstrap installs Arcanum into a consuming repository. It creates `.arcanum/observability/`, optional `.arcanum/necronomicon/` harness state, and Codex slash commands directly under `.codex/commands/`.

When `ontology-harness` is selected, bootstrap can also initialize Necronomicon harness state for durable repository memory, selected capability routing, fallback discovery, and capability update reports.

The spell supports two installation postures:

- generate commands for all sigils and spells,
- generate commands for a selected sigil and spell capability set.

## Trigger Conditions

- A user wants to add Arcanum to another repository.
- A repository should expose Arcanum through Codex.
- A repository needs observability storage, hook-backed envelopes, and local slash-command support.
- A user wants to choose individual sigils rather than install all of Arcanum.
- A repository should use Necronomicon as a persistent harness for session memory and selected capability routing.

## Required Sigils

| Sigil                     | Role In Spell                                             | Required Mode      |
| ------------------------- | --------------------------------------------------------- | ------------------ |
| `sigil-runtime-installer` | Select target runtime and install a thin command adapter. | install or dry-run |
| `observability-setup`     | Ensure local `.arcanum/observability/` folders exist.     | install or verify  |

## Optional Sigils

| Sigil               | Use When                                                            | Notes                                             |
| ------------------- | ------------------------------------------------------------------- | ------------------------------------------------- |
| `inventory`         | The target repository should track installed knowledge entries.     | Useful for larger installs.                       |
| `context-builder`   | The target repository should prove retrieval over installed sigils. | Useful after selected installs.                   |
| `sigil-development` | The user plans to author local sigils.                              | Include in authoring-oriented installs.           |
| `spellcraft`        | The user plans to compose local spells.                             | Include when local workflow recipes are expected. |
| `experiment-harness` | The user plans to validate local spells or sigils with examples.    | Include in authoring-oriented installs.           |

## Prerequisites

- Arcanum source root is known.
- Target repository root is known.
- User chooses command posture: all sigils and spells or selected commands.
- User chooses command runtime: Codex or none.
- User chooses default runtime adapter: `codex-exec`, `dry-run`, or none.
- Existing target files are preserved unless overwrite is explicitly approved.

## Shared State

| State                                 | Owner             | Updated By                              | Consumed By                                                             |
| ------------------------------------- | ----------------- | --------------------------------------- | ----------------------------------------------------------------------- |
| `.arcanum/`                           | target repository | bootstrap script                        | observability, Necronomicon state, users, local agents                  |
| `.arcanum/observability/`             | target repository | `observability-setup`, bootstrap script | runtime commands, sigil and spell runs, reflection workflows            |
| `.arcanum/runtime/config.json`        | target repository | bootstrap script, `tools/arcanum`       | default adapter selection and adapter profile paths                     |
| `.arcanum/runtime/adapters/`          | target repository | bootstrap script                        | non-secret adapter profile snapshots                                    |
| `.arcanum/necronomicon/`              | target repository | bootstrap script, Necronomicon          | session memory, capability manifest, route ledgers, decisions, handoffs |
| artifact-local `development/`         | local artifacts   | `experiment-harness`                    | spellcraft, sigil-development, Codex CLI example runners                |
| `.codex/commands/`                    | target repository | `sigil-runtime-installer`               | Codex command surface                                                   |
| `.codex/hooks.json`, `.codex/hooks/`  | target repository | bootstrap script                        | observer envelope open/enrich/close hooks                               |
| install report                        | spell             | all phases                              | user, observability                                                     |

## Execution Phases

| Phase | Sigil Or Tool             | Input                                         | Output                                                                                                                                                                         | Gate                                                              | Failure Policy                                         |
| ----- | ------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- | ------------------------------------------------------ |
| 1     | bootstrap script          | target root, sigil selection, spell selection | dry-run plan or install plan                                                                                                                                                   | target root resolved                                              | block on missing target                                |
| 2     | bootstrap script          | command posture                               | selected sigil and spell command list                                                                                                                                          | selections resolve to canonical Arcanum artifacts                 | block on unknown command selection                     |
| 3     | `observability-setup`     | target root                                   | `.arcanum/observability/`                                                                                                                                                      | folders exist                                                     | flag if setup partial                                  |
| 4     | bootstrap script          | selected ontology/session posture             | optional `.arcanum/necronomicon/` harness state and `capabilities.json`                                                                                                        | folder contains harness state only                                | block on obsolete runtime-book files without `--force` |
| 5     | `sigil-runtime-installer` | selected runtime and default adapter          | `.arcanum/runtime/config.json`, adapter profiles, `.codex/commands/` orchestrator, per-sigil commands, per-spell commands, aliases, Necronomicon command, and hook files | commands contain executable instruction snapshots and observer task zero; runtime config contains no secrets | skip command files if runtime is none                  |
| 6     | validation                | installed files                               | command, bridge, syntax, link, and observability validation                                                                                                                    | selected commands can run without copied Necronomicon definitions | block on broken local runtime links                    |
| 7     | spell report              | phase outputs                                 | install report                                                                                                                                                                 | all blockers named                                                | report partial if optional runtime skipped             |

## Bootstrap Script

For consuming repositories, use the curl installer:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --sigils all --spells all --runtime codex --default-adapter codex-exec
```

The curl installer downloads the Arcanum repository archive and delegates to the portable bootstrap script.

When working from a local checkout, run the bootstrap script directly:

```bash
arcanum/tools/bootstrap_arcanum.sh --target <repo> --sigils all --spells all --runtime codex --default-adapter codex-exec
```

Selected install example:

```bash
curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/arcanum/main/tools/install_arcanum.sh | bash -s -- \
  --target . \
  --sigils ontology-vault,context-builder,sigil-runtime-installer \
  --spells ontology-harness \
  --runtime codex \
  --default-adapter codex-exec
```

Dry-run example:

```bash
arcanum/tools/bootstrap_arcanum.sh --target <repo> --sigils all --runtime none --dry-run
```

## Local Customization

- Install root: `.arcanum/`
- Command surface: `.codex/commands/`
- Runtime config: `.arcanum/runtime/config.json`
- Runtime adapter profiles: `.arcanum/runtime/adapters/`
- Runtime adapter interchange: `tools/arcanum --get-default-adapter`, `tools/arcanum --set-default-adapter <adapter-id>`, and one-run `tools/arcanum --exec --adapter <adapter-id> ...`
- Observer hooks: `.codex/hooks.json` and `.codex/hooks/`
- Individual runtime names: `arcanum-sigil-<id>` and `arcanum-spell-<id>`
- Ontology Harness runtime alias: `arcanum-ontology-harness`, installed when `ontology-harness` is selected.
- Necronomicon runtime name: `arcanum-necronomicon`, installed by default for the persistent repository harness unless disabled.
- Necronomicon state root: `.arcanum/necronomicon/`, limited to harness memory, selected capabilities, routes, decisions, handoffs, and capability update reports.
- Observability root: `.arcanum/observability/`
- Gate strictness: strict for overwrites, standard for selected install validation.
- Interaction mode: interactive for selection, dry-run for preview, install for execution.

## Observability

Record spell-level telemetry when `.arcanum/observability/` exists:

- spell name,
- target repository,
- install posture,
- selected sigils,
- selected spells,
- Necronomicon harness status,
- command runtime,
- default runtime adapter,
- files created,
- files skipped,
- validation result,
- follow-up actions.

Runtime commands own the observability handoff. Raw telemetry remains under `.arcanum/observability/`.

## Output Contract

Return:

```markdown
## Spell Result

- Spell: Arcanum Bootstrap
- Canonical ID: arcanum-bootstrap
- Alias used: <alias or none>
- Repository: <target path>
- Install root: .arcanum/
- Sigil commands: all | <list>
- Spell commands: all | none | <list>
- Necronomicon alias command: installed | skipped
- Necronomicon command: installed | skipped
- Necronomicon harness state: initialized | skipped
- Command runtime: codex | none
- Default runtime adapter: codex-exec | dry-run | none
- Phases completed: <count>
- Gates: pass | block | flag
- Outputs: <paths>
- Validation: <checks>
- Follow-up: <items or none>
```
