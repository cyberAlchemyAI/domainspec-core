# Runtime Surface Inventory

Date: 2026-05-29
Task: `TASK-RUNTIME-001`
SWU: `SWU-RUNTIME-001`
Status: pass

## Objective

Identify active and historical runtime surfaces before migration edits.

This inventory covers references to:

- `codex exec`
- `codex-exec`
- `codex-bypass`
- `CODEX_BIN`
- `run-with-codex`
- `observe-run-with-codex`
- `tools/arcanum --exec`
- `.codex/commands`
- `.arcanum/runtimes/codex/commands`
- `arcanum-runtime-run`

## Controlling Context

- `ops/ARCANUM-RUNTIME-SURFACE-INVOKE-DESIGN-PLAN.md`
- `ops/CODEX-SKILL-SURFACE-POLICY.md`
- `ops/SKILLS-FIRST-RUNTIME-POLICY.md`
- `ops/ARCANUM-RUNTIME-SURFACE-REFRESH-REPORT.md`
- `arcanum/formulae/dispatch-spec/development/ORCHESTRATION-RUNTIME-PLAN.md`

## Inventory Summary

| Surface class | Current evidence | Active? | Target action |
| --- | --- | --- | --- |
| Root Codex command files | `.codex/commands/*.md` tracked but currently deleted in worktree | legacy tracked surface | Preserve deletion unless a runtime compatibility decision reopens it. |
| Root `.arcanum` Codex command adapters | `.arcanum/runtimes/codex/commands/*.md` tracked but currently deleted in worktree | legacy tracked surface | Preserve deletion unless explicit compatibility is proven. |
| Root GitHub/Copilot skills | `.github/skills/*/SKILL.md`, 151 files present | active runtime/distribution surface | Keep as generated GitHub/Copilot-native packages when provenance exists; enrich classification in `TASK-RUNTIME-007`. |
| Root Copilot instructions | `.github/copilot-instructions.md` tracked | active runtime guidance | Preserve and include in Copilot profile/provenance work. |
| Claude surface | `.claude/*` absent | missing planned runtime surface | Generate only through `claude` install profile. |
| Root Arcanum utility | `arcanum/tools/arcanum`, `arcanum/tools/bootstrap_arcanum.sh`, `arcanum/tools/install_arcanum.sh`, `arcanum/tools/arcanum-runtime-run` | active deterministic/runtime tool surface | Migrate adapter metadata and install profiles in `TASK-RUNTIME-003` and `TASK-RUNTIME-004`. |
| DomainSpec bootstrap command generation | `implementation/domainspec/tools/bootstrap_domainspec_codex.sh` generates `.codex/commands/` | active submodule-owned installer | Do not parent-edit; route through DomainSpec-owned task or classify as downstream migration dependency. |
| DomainSpec runtime runner | `implementation/domainspec/tools/arcanum`, `implementation/domainspec/tools/arcanum-runtime-run` | active submodule-owned runtime surface | Do not parent-edit; use as downstream inventory input. |
| DomainSpec observed Codex helpers | `implementation/domainspec/framework/observability/scripts/observe-run-with-codex.sh` and pilot scripts | active submodule-owned observability surface | Do not parent-edit; route through DomainSpec-owned migration task. |
| Arcanum experiment harness Codex runners | `arcanum/arcana/experiment-harness/scripts/run-with-codex.sh`, `find-codex.sh` | active Arcanum lifecycle surface | Migrate in later Arcanum-owned runtime task. |
| Arcanum Refine command-backed contract | `arcanum/arcana/refine/SKILL.md`, `README.md`, `REFINEMENT-LOOP.md`, templates | active Arcanum lifecycle surface | Migrate language to parent-owned dispatch and native receipts in `TASK-RUNTIME-005`. |
| Arcanum sigil runtime installer command model | `arcanum/arcana/sigil-runtime-installer/*` | active Arcanum lifecycle surface | Migrate away from `.codex/commands` default in later runtime task. |
| Historical refinement/task evidence | `*/development/refinement-runs/*`, task session context packs, prior manifests | historical/generated evidence | Preserve by default; do not count as active blockers. |
| Ops policy/planning references | `ops/*` runtime-surface policy and plans | active governance docs | Keep and update as migration proceeds. |

## Root Tracked Command State

Current tracked command paths are already deleted in the worktree:

```text
.codex/commands/arcanum-sigil-experiment-harness.md
.codex/commands/arcanum-sigil-invoke-example-runner.md
.codex/commands/arcanum-spell-invoke.md
.codex/commands/experiment-next.md
.codex/commands/experiment-observe.md
.codex/commands/experiment-run.md
.codex/commands/experiment-validate.md
.codex/commands/invoke-example-next.md
.codex/commands/invoke-example-run.md
.arcanum/runtimes/codex/commands/arcanum-sigil-experiment-harness.md
.arcanum/runtimes/codex/commands/arcanum-sigil-invoke-example-runner.md
.arcanum/runtimes/codex/commands/arcanum-spell-invoke.md
.arcanum/runtimes/codex/commands/experiment-next.md
.arcanum/runtimes/codex/commands/experiment-observe.md
.arcanum/runtimes/codex/commands/experiment-run.md
.arcanum/runtimes/codex/commands/experiment-validate.md
```

Classification:

- `surface_class`: legacy command adapter
- `active_status`: no active file in worktree, tracked deletion pending
- `target_action`: preserve deletion through `TASK-RUNTIME-006`
- `blocker`: none unless a runtime-specific compatibility requirement is introduced

## Active Runtime Code And Installer Surfaces

| Path | Class | Evidence | Target action |
| --- | --- | --- | --- |
| `arcanum/tools/arcanum` | active runtime utility | Lists `local-skill`, `dry-run`, `codex-exec`, `codex-bypass`; resolves `.codex/commands`; has `CODEX_BIN` execution path. | Migrate to `codex-skill`, `claude-skill`, `copilot-instructions`, abstract `native-skill`, and explicit legacy CLI adapters. |
| `arcanum/tools/bootstrap_arcanum.sh` | active installer | Supports `--surfaces codex,claude,copilot`; still writes `.codex/commands`; default adapter is `local-skill` when Codex surface installed. | Add profile/provenance output and stop default command generation. |
| `arcanum/tools/install_arcanum.sh` | active installer wrapper | Documents `--default-adapter <local-skill|codex-exec|dry-run|none>`. | Update adapter names and install profile docs after `tools/arcanum` changes. |
| `arcanum/tools/arcanum-runtime-run` | active legacy wrapper | Deprecated helper that calls `tools/arcanum --exec`. | Mark deterministic legacy wrapper or replace with runtime-native handoff behavior. |
| `implementation/domainspec/tools/bootstrap_domainspec_codex.sh` | submodule-owned installer | Generates `.codex/commands/`. | DomainSpec-owned follow-up; not parent-edited in this task. |
| `implementation/domainspec/framework/observability/scripts/observe-run-with-codex.sh` | submodule-owned observability runner | Uses Codex runner vocabulary. | DomainSpec-owned follow-up. |

## Active Arcanum Lifecycle Surfaces

| Area | Representative files | Active issue | Target action |
| --- | --- | --- | --- |
| Refine | `arcanum/arcana/refine/SKILL.md`, `README.md`, `REFINEMENT-LOOP.md`, `templates/runtime-handoff.md` | Requires or documents `tools/arcanum --exec` command-backed stages. | Migrate in `TASK-RUNTIME-005`. |
| Sigil Runtime Installer | `arcanum/arcana/sigil-runtime-installer/SKILL.md`, `README.md`, templates | Treats `.codex/commands` as installed runtime surface. | Migrate to generated native runtime packages. |
| Experiment Harness | `arcanum/arcana/experiment-harness/scripts/run-with-codex.sh`, docs | Uses Codex CLI as experiment primitive. | Later Arcanum-owned runtime migration. |
| Invoke examples | `arcanum/spells/invoke/development/run-template-example-with-codex.sh`, validation docs | Uses Codex example runners and template validation evidence. | Later Arcanum-owned runtime migration. |
| Observed Invocation Loop | `arcanum/spells/observed-invocation-loop/*` | Mentions command/Codex attachment surfaces. | Later observability/runtime migration. |

## Generated Or Historical Evidence Classes

Historical files under these roots mention old command surfaces but should not be edited during runtime migration:

```text
arcanum/**/development/refinement-runs/**
arcanum/**/development/task-sessions/**
ops/development/refinement-runs/**
```

Classification:

- `surface_class`: historical/generated evidence
- `target_action`: preserve by default
- `migration_policy`: grep reports should exclude these from active blocker counts, but may cite them as prior evidence

## Root Runtime Package State

| Surface | Count or state | Target action |
| --- | ---: | --- |
| `.codex/commands` files in worktree | 0 | Keep absent unless explicit compatibility reopens. |
| `.arcanum/runtimes/codex/commands` files in worktree | 0 | Keep absent unless explicit compatibility reopens. |
| `.github/skills` files | 151 | Keep pending provenance/alias enrichment. |
| `.github/instructions` files | 0 | Generate only through Copilot/GitHub profile. |
| `.claude` files | 0 | Generate only through Claude profile. |
| `.arcanum/runtimes` files | 83 | Classify in `TASK-RUNTIME-002`. |
| `.arcanum/observability` files | 45 | Classify in `TASK-RUNTIME-002`. |

## Decisions Recorded

- Root command adapters are no longer active worktree files and should remain deleted unless a compatibility task proves they are required.
- `.github/skills` is an active non-Codex runtime package surface, not a Codex install surface.
- DomainSpec runtime/codegen surfaces are active but submodule-owned; parent cleanup must not mutate them.
- Historical refinement evidence is not an active migration blocker.
- `tools/arcanum` is the central active parent-owned implementation surface for adapter migration.

## Follow-Up Work

Immediate next task:

```text
TASK-RUNTIME-002 / SWU-RUNTIME-002
```

Then:

```text
TASK-RUNTIME-003 / SWU-RUNTIME-003
TASK-RUNTIME-003 / SWU-RUNTIME-004
TASK-RUNTIME-004 / SWU-RUNTIME-005
```

Potential blocker to watch:

- `tools/arcanum` in the root repo appears under `arcanum/tools/`, while some policy artifacts name `tools/arcanum`. Before implementation, the selected install/copy/symlink path must be confirmed or normalized.

## Validation

Commands used:

```bash
rg -n "codex exec|codex-exec|codex-bypass|CODEX_BIN|run-with-codex|observe-run-with-codex|tools/arcanum --exec|\\.codex/commands|\\.arcanum/runtimes/codex/commands|arcanum-runtime-run" .codex .arcanum .github arcanum ops tools implementation/domainspec
git status --short .codex/commands .arcanum/runtimes/codex/commands arcanum/tools tools implementation/domainspec/tools
git ls-files .codex/commands .arcanum/runtimes/codex/commands .github/skills .github/instructions .github/copilot-instructions.md AGENTS.md CLAUDE.md .claude tools
find . -maxdepth 4 -path './.github/skills/*/SKILL.md' -print
```

Gate verdict:

- `G-RUNTIME-001`: pass. Active runtime surfaces have been classified enough for the next bounded task.
