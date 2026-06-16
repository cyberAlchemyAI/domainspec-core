# Arcanum Sigil: sigil runtime installer

<!-- arcanum:capability-id sigil-runtime-installer -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command arcanum-sigil-sigil-runtime-installer -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-sigil-runtime-installer-<UTC timestamp>`.
- `capability.id`: `sigil-runtime-installer`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `sigil-runtime-installer` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `sigil-runtime-installer`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/sigil-runtime-installer/README.md

````markdown
# Sigil Runtime Installer

Sigil Runtime Installer installs explicit legacy Codex command adapters for Arcanum sigils and spells.

Arcanum now treats native runtime skills as the default installed runtime surface. `.codex/commands/` is legacy compatibility only. Generated command files are full executable command contracts with embedded canonical snapshots; there is no `.arcanum/runtimes/` indirection and no GitHub Copilot skill bridge.

For each explicit legacy command install, the installer creates one general `arcanum-orchestrate` command plus individual commands for every selected sigil and spell. Prefixed names use `arcanum-sigil-<id>` and `arcanum-spell-<id>` as stable compatibility names. Bare-id aliases such as `interrogation` or `invoke` are also full command files unless the alias would collide. When `ontology-harness` is selected, it creates `arcanum-ontology-harness`. When Necronomicon harness generation is enabled, it creates `arcanum-necronomicon`.

Generated Codex commands record their installed runtime with `arcanum:runtime codex`. Runtime-sensitive sigils may also declare adapter metadata. For example, `task-session` declares `arcanum:runtime-goal-adapter codex-goal` so it can translate a selected work-pack task or SWU into a native Codex `/goal` through the `codex-goal-profile` transmutation while preserving Task Session as the Arcanum coordinator.

## Problem It Solves

Arcanum stores canonical sigils and spells as framework artifacts, and current runtimes should discover them through generated native skill packages. Some repositories may still need Codex slash-command compatibility from `.codex/commands/`.

Sigil Runtime Installer bridges that legacy gap by generating Codex commands directly from canonical Arcanum artifacts, installing observer hooks, and validating that commands can run without generated `.arcanum/necronomicon/` registry files.

## Use When

- a repository explicitly still needs Arcanum sigils as Codex slash-command style commands,
- a consuming repository should install selected Arcanum capabilities without runtime adapter folders,
- installed commands need observer-envelope-first telemetry,
- command wrappers need validation.

Generated commands use their embedded canonical instruction snapshots and the observer envelope task-zero contract. Necronomicon is the persistent repository harness, not a generated definition-storage folder.

## Do Not Use When

- the user only wants to read the registry,
- the repository should not receive Codex command files,
- the requested install would make local generated commands authoritative over canonical sigils.

## Supported Targets

| Target | Command Surface | Generated Shape |
| --- | --- | --- |
| Codex commands | `.codex/commands/<command>.md` | Legacy command contract with observer task-zero block and embedded canonical snapshot |
| None | n/a | Observability and optional Necronomicon state only |

This sigil owns only the legacy `.codex/commands/` surface. Native runtime skill
surfaces are owned by `tools/bootstrap_arcanum.sh` profiles.

## Claude Code surface (owned by `bootstrap --profile claude`)

`tools/bootstrap_arcanum.sh --profile claude` generates `.claude/skills/<name>/SKILL.md`
for every sigil and spell plus `.claude/agents/arcanum-stage-worker.md`. At generation
time the canonical Arcanum tool vocabulary is mapped to real Claude Code tool names so
the generated `allowed-tools` are valid (sources are never edited):

| Canonical (source) | Claude (generated) |
| --- | --- |
| `Task` | `Agent` |
| `AskQuestions` | `AskUserQuestion` |
| all others (`Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`) | unchanged |

The generated surface is validated by `tools/validate-claude-skills.sh`, which blocks an
install (and fails CI) if any package has a non-Claude tool name, a `name` that does not
match its directory, a missing description, or a dangling `skills:` reference. Regenerate
and validate with `make claude-skills` (optionally `TARGET=<repo>`).

## Output

The sigil can produce:

- target selection report,
- install manifest,
- Codex command files,
- Codex hook files,
- runtime metadata and runtime-goal adapter declarations,
- validation report.

## Why This Is Arcana

The sigil coordinates command generation, local path decisions, canonical snapshot embedding, observer hook installation, validation, and installation reporting across repository boundaries.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/sigil-runtime-installer/SKILL.md

````markdown
---
name: sigil-runtime-installer
description: "Use when installing explicit legacy Arcanum Codex command adapters."
argument-hint: "<codex-commands|none> [--repo <path>] [--command <name>] [--dry-run]"
tier: arcana
domain: sigil-runtime-installation
version: 0.2.0
origin: updated for skills-first runtime policy with legacy command compatibility
allowed-tools: Read, Write, Glob, Grep, Bash, AskQuestions
---

# Sigil: Sigil Runtime Installer

<objective>
Install explicit legacy Codex command adapters for Arcanum sigils and spells while keeping native runtime skills as the default execution surface.
</objective>

<logic-type>
Arcana: legacy command generation, repository-local installation, validation, observer hook installation, and compatibility routing.
</logic-type>

<targets>
- `codex-commands`: create explicit legacy command files directly under `.codex/commands/`.
- `none`: install observability and optional Necronomicon state without command files.

When legacy command compatibility is explicitly selected, install the general `arcanum-orchestrate` command and individual artifact commands for each selected sigil and spell. Prefixed commands use `arcanum-sigil-<id>` and `arcanum-spell-<id>` as stable compatibility names. Bare aliases use the artifact id, such as `interrogation` or `invoke`, unless the alias would collide. When `ontology-harness` is selected, install `arcanum-ontology-harness`. When Necronomicon harness generation is enabled, install `arcanum-necronomicon`.

Generated Codex commands should declare the installed runtime with `arcanum:runtime codex`. Runtime-sensitive sigils may also declare adapter metadata. `task-session` must declare `arcanum:runtime-goal-adapter codex-goal` when installed for Codex so work-pack tasks/SWUs can be delegated through native Codex `/goal` via the `codex-goal-profile` transmutation.
</targets>

<applicability>
Use this sigil only when a repository still needs legacy Codex slash-command style adapters. For normal runtime installs, use generated native skills through the install profiles.

The Claude Code skill surface (`.claude/skills/`, `.claude/agents/`) is owned by `tools/bootstrap_arcanum.sh --profile claude`, which generates the packages, maps tool vocabulary to Claude names, and validates the result via `tools/validate-claude-skills.sh`. This sigil governs only the legacy `.codex/commands/` surface.
</applicability>

<inputs>
Expected inputs, if available:

- target runtime: `codex-commands` or `none`,
- repository root,
- observability path,
- command name,
- selected sigils,
- selected spells,
- dry-run preference.
</inputs>

<default-output>
If legacy command compatibility is selected and no command is provided, install or plan `arcanum-orchestrate` plus individual artifact commands.

Default paths:

```text
codex-commands -> .codex/commands/arcanum-orchestrate.md
                  .codex/commands/arcanum-sigil-<id>.md
                  .codex/commands/<id>.md
                  .codex/commands/arcanum-spell-<id>.md
                  .codex/commands/<id>.md
                  .codex/commands/arcanum-ontology-harness.md
                  .codex/commands/arcanum-necronomicon.md
                  .codex/hooks.json
                  .codex/hooks/arcanum-user-prompt-submit.sh
                  .codex/hooks/arcanum-post-tool-use.sh
                  .codex/hooks/arcanum-stop.sh
```
</default-output>

<process>
## Step 1 - Select Target

1. If the target runtime is not provided, ask whether to install legacy `codex-commands` or `none`.
2. Resolve repository root and selected Arcanum artifacts.
3. Resolve command name, defaulting to `arcanum-orchestrate`.
4. Detect whether the target install path already exists.

## Step 2 - Build Command Plan

5. Generate `.codex/commands/` files directly only for explicit legacy compatibility; do not generate `.arcanum/runtimes/`.
6. Add runtime metadata to generated Codex commands and adapter metadata to runtime-sensitive commands.
7. Every command starts with observer envelope task zero.
8. Every command embeds or references the canonical sigil/spell snapshot it needs to execute.
9. Do not require generated `.arcanum/necronomicon/` registry files. If Necronomicon state exists there, treat it as harness memory and selected capability state only.
10. Install Codex hooks for `UserPromptSubmit`, `PostToolUse`, and `Stop` so native slash-command usage is hook-backed.

## Step 3 - Install Or Dry Run

11. In dry-run mode, return the files that would be created or updated.
12. In install mode, create or update `.codex/commands/` only when legacy command compatibility is explicitly selected, plus `.codex/hooks.json`, `.codex/hooks/`, `.arcanum/observability/`, and optional `.arcanum/necronomicon/`.
13. For sigil and spell artifact commands, install both the prefixed compatibility command and the bare-id command.
14. If an existing command has unrelated local changes, stop and ask before overwriting unless overwrite was explicitly approved.

## Step 4 - Validate

15. Check that command files exist.
16. Check that each command contains observer task-zero metadata.
17. Check that generated Codex commands include runtime metadata.
18. Check that runtime-sensitive commands include expected adapter metadata.
19. Check that short aliases exist for installed sigil and spell commands unless explicitly conflicted.
20. Check that `.codex/hooks.json` is valid JSON and hook scripts are executable.
21. Check that no `.arcanum/runtimes/` or `.github/skills/` tree is generated.
22. Return pass, flag, or block.
</process>

<quality-bar>
A successful execution must:

- install Codex command adapters only when explicitly requested,
- install bare-id aliases for sigils and spells unless a collision is reported,
- keep Necronomicon as harness state,
- install the Necronomicon command when the repository harness is enabled,
- avoid requiring generated `.arcanum/necronomicon/` definition files,
- install observer hooks,
- preserve runtime metadata and runtime-goal adapter declarations,
- validate command and hook paths,
- preserve unrelated local agent configuration,
- report what was installed and how to invoke it.
</quality-bar>

<anti-patterns>
Avoid:

- this legacy command installer itself generating GitHub Copilot, Claude, or `.arcanum/runtimes/` adapter trees; those native runtime skill surfaces are owned and validated by `tools/bootstrap_arcanum.sh` profiles (`--profile claude`, `--profile github-copilot`), not by this legacy Codex command path,
- overwriting existing command files without checking ownership,
- embedding stale or untraceable copies of sigil instructions in command files,
- making a consuming repository's generated command the canonical sigil source,
- hiding validation failures behind a successful install message.
</anti-patterns>

<observability>
When `.arcanum/observability/` exists, emit telemetry for:

- target runtime,
- repository root,
- command name,
- files created,
- files updated,
- Necronomicon command status,
- hook install status,
- runtime metadata status,
- validation result,
- blockers.
</observability>

<output-contract>
Return:

```markdown
## Sigil Runtime Installer Result

- Target runtime: codex | none
- Repository: <path>
- Command: <name>
- Files created: <paths>
- Files updated: <paths>
- Hooks: installed | skipped
- Dry run: yes | no
- Validation: pass | flag | block
- Invocation: <command or command name>
- Next action: <action>
```
</output-contract>

````
