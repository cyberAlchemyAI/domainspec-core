# Arcanum Runtime Surface Invoke Design And Plan

Date: 2026-05-29
Status: flag
Mode: invoke design -> invoke plan
Target: Arcanum runtime surface, `tools/arcanum`, `.arcanum` state, repository-local installs, and global Codex usage

## Objective

Converge repository organization, skills-first cleanup, orchestration runtime migration, and new-user install behavior into one execution-ready migration plan.

The desired end state is:

```text
canonical source
  -> deterministic repo utility
  -> runtime-specific skill/install adapters
  -> native runtime execution with receipts
  -> classified repo-local state
```

`tools/arcanum` remains, but as deterministic utility and compatibility surface. `.arcanum` remains, but only as a classified runtime/state/evidence namespace. Runtime-facing work uses generated native packages for each host runtime, with thin aliases where useful.

## Source Contracts

- `ops/ARCANUM-TOOLS-AND-STATE-REFINE.md`
- `ops/RUNTIME-SURFACE-CONVERGENCE-REFINE.md`
- `ops/SKILLS-FIRST-RUNTIME-POLICY.md`
- `ops/CODEX-SKILL-SURFACE-POLICY.md`
- `ops/DUPLICATE-SKILL-PRUNING-PLAN.md`
- `ops/REPOSITORY-ORGANIZATION-DESIGN.md`
- `arcanum/formulae/dispatch-spec/development/ORCHESTRATION-RUNTIME-PLAN.md`
- `arcanum/spells/invoke/design.md`
- `arcanum/spells/invoke/plan.md`

## Design Result

### Design Summary

The repository needs a clean separation between:

| Layer | Role | Policy |
| --- | --- | --- |
| Canonical source | `arcanum/arcana`, `arcanum/spells`, `arcanum/formulae`, DomainSpec source | Edit here first. |
| Deterministic utility | `tools/arcanum`, audit/classifier scripts | Resolve, validate, generate, classify, and produce handoff/receipt requirements. |
| Runtime adapters | global Codex skills, `.github/skills`, Claude/Copilot install files, same-checkout facades | Discover and guide native runtime execution. |
| Runtime state | `.arcanum/runtime`, `.arcanum/runtimes`, `.arcanum/observability` | Track only classified config, manifests, adapters, and accepted evidence. |
| Generated/private state | run folders, reflection state, caches, private runtime homes | Ignore or untrack by default. |

The main correction is to remove the old hidden equation:

```text
tools/arcanum --exec == run model-backed orchestration
```

Replace it with:

```text
tools/arcanum resolves, validates, prepares, and records receipt requirements
native runtime skills, agents, instructions, or subagents execute model-backed work
task-session accepts one bounded SWU at a time
```

### Runtime Distribution Approach

Use canonical source plus generated native snapshots.

The repository should not make each runtime jump through another runtime's format. Codex, Claude, and Copilot should each receive the package shape they use best:

| Runtime | Native package shape | Source rule | Alias rule |
| --- | --- | --- | --- |
| Codex | `$CODEX_HOME/skills/<name>/SKILL.md` | Generated from canonical Arcanum/DomainSpec source or a thin wrapper to canonical source when local paths are stable. | Aliases are separate thin skills with their own `name` and canonical target. |
| Claude | `.claude/skills/<name>/SKILL.md`, `.claude/agents/<name>.md`, `CLAUDE.md` guidance | Generated native Claude-facing package from canonical source. | Aliases should be generated only when Claude discovery benefits from alternate names. |
| Copilot/GitHub | `.github/skills/<name>/SKILL.md`, `.github/instructions/*.instructions.md`, `.github/copilot-instructions.md`, `AGENTS.md` guidance | Generated repository-native Copilot/GitHub adapter from canonical source. | Aliases are generated adapter packages only when they match expected user invocation names. |

Generated snapshots are allowed, but only with provenance:

```yaml
surface_kind: generated-native-runtime-package
runtime: codex | claude | copilot
canonical_source: <path>
alias_of: <canonical capability or null>
generated_by: tools/arcanum <profile command>
mutation_policy: regenerate-from-canonical-source
```

This accepts runtime-native copies as install artifacts while rejecting them as independent canonical sources.

### Six Design Views

#### 1. Context View

`domainspec-core` is a multi-family workspace with Arcanum lifecycle source, DomainSpec source, repository governance, runtime installs, and generated evidence. The cleanup should not collapse those into one copied skill tree or one command layer.

Global Codex is an operator surface outside the repository. It can invoke repo work, but repository evidence belongs in the target repo.

#### 2. High-Level Structure View

```text
global Codex skills
  -> target repo cwd
    -> canonical source
    -> tools/arcanum deterministic checks
    -> runtime adapter/profile selection
    -> .arcanum classified state/evidence
```

`tools/arcanum` is optional for source-only use and required only when a repository wants local resolution, validation, adapter generation, manifests, or compatibility checks.

#### 3. Low-Level Components View

Required components:

- `tools/arcanum` adapter metadata with host-native adapters as the orchestration default: `codex-skill`, `claude-skill`, and `copilot-instructions`, plus an abstract `native-skill` selector when the host can be inferred.
- Installer/bootstrap profiles: `personal-codex`, `repo-local`, `github-copilot`, `claude`, `observability`, `all`, `none`.
- `.arcanum` classification ledger.
- Ignore/untracking policy for generated `.arcanum` state.
- Active surface inventory for `codex exec`, `tools/arcanum --exec`, command prompts, and runtime wrappers.
- Runtime receipts for native stage execution.

#### 4. Workflow Process View

```text
inventory active runtime surfaces
  -> classify .arcanum state
  -> update adapter/default semantics
  -> update installer profiles
  -> migrate docs and skill contracts
  -> validate no implicit nested codex exec remains
  -> prune duplicate adapters after owner gates
```

#### 5. Decision Flow View

For each surface:

1. Is it canonical source?
   - Keep and edit there.
2. Is it a runtime adapter or install snapshot?
   - Keep only with provenance and regeneration path.
3. Is it a legacy command adapter?
   - Delete by default or mark explicit compatibility.
4. Is it generated evidence?
   - Track only if accepted as durable evidence.
5. Is it private/local runtime state?
   - Never track.
6. Is owner or runtime need unclear?
   - Route to decision-gate before deletion.

#### 6. Dependency Interface View

- Global Codex skill surface -> target repo cwd -> repo-local artifacts.
- `tools/arcanum` -> canonical source and `.arcanum/runtime/config.json`.
- `tools/arcanum` -> generated native Codex/Claude/Copilot packages and adapter manifests.
- `.arcanum/observability` -> append-only receipts and promoted evidence.
- Runtime adapters -> native execution, not nested Codex CLI by default.

### Design Decisions

- Keep `tools/arcanum`, but shrink authority to deterministic utility plus explicit legacy compatibility.
- Keep `.arcanum`, but classify every subpath before tracking, deleting, or untracking.
- Use generated native runtime packages for Codex, Claude, and Copilot from canonical source.
- Keep personal/global Codex skills as the Codex-facing install surface for this operator.
- Keep root `.github/skills` as Copilot/GitHub-native generated adapters when provenance exists; delete only stale, unproven duplicates.
- Account for aliases as generated thin native packages, not separate full skill bodies.
- Stop generating `.codex/commands` and `.arcanum/runtimes/codex/commands` by default.
- Treat `codex-exec`, `codex-bypass`, and nested `codex exec` as explicit legacy opt-in.

### Design Gaps

- Root `.github/skills` needs provenance/regeneration metadata so generated Copilot/GitHub adapters are distinguished from stale copies.
- DomainSpec `.agents/skills` duplicate cleanup is submodule-owned.
- Current `tools/arcanum` and bootstrap scripts still need adapter/profile changes for runtime-native package generation.
- `.arcanum` tracked state still needs a path-by-path classification pass.

## Plan Result

### Complexity

Medium.

Reason: the work touches runtime semantics, generated state policy, install behavior, repository governance, and multiple runtime surfaces. It is not a single source edit, but it can proceed in bounded SWUs.

### Implementation Layering

| Layer | Question | Work | Promotion evidence |
| --- | --- | --- | --- |
| L0 inventory proof | Do we know every active runtime and `.arcanum` surface before mutation? | Create active surface and state inventories. | No active surface class remains unclassified. |
| L1 deterministic adapter proof | Can `tools/arcanum` express runtime-native execution without spawning Codex? | Add adapter metadata and native package selectors. | Adapter commands show host-native defaults and legacy opt-in. |
| L2 install profile proof | Can new users and repos install the right native surfaces without hand-maintained copies? | Add explicit profile behavior to bootstrap/install docs/scripts. | Dry-run profiles show intended write sets, provenance, aliases, and no default command generation. |
| L3 cleanup rollout | Can duplicate and legacy surfaces be pruned safely? | Remove command adapters, classify `.github/skills`, untrack generated state. | Grep/status reports show only source, adapters, durable config/evidence, or explicit legacy surfaces. |

### Work-Pack

#### TASK-RUNTIME-001: Inventory Active Runtime Surfaces

- Layer: L0
- Owner route: `task-session`
- Write scope:
  - `ops/RUNTIME-SURFACE-INVENTORY.md`
  - optional report under `ops/reports/`
- Goal: Identify every active `codex exec`, `tools/arcanum --exec`, command prompt, runtime adapter, generated skill surface, and installer reference before migration edits.
- Implementation detail:
  - Search active source and policy paths.
  - Separate active runtime code, active installer/config, active docs, validation fixtures, generated historical evidence, and migration notes.
  - Do not rewrite generated historical evidence during this task.
- Verification:
  - Inventory has no unclassified active surface class.
  - Every remaining active class has a target action: migrate, preserve, regenerate, explicit legacy opt-in, or delete candidate.

#### TASK-RUNTIME-002: Classify `.arcanum` State

- Layer: L0
- Owner route: `task-session`
- Write scope:
  - `ops/ARCANUM-STATE-CLASSIFICATION.md`
  - `.gitignore` only if approved by the task
- Goal: Decide what `.arcanum` paths are durable config, runtime adapters, generated evidence, generated run state, private state, or deletion candidates.
- Implementation detail:
  - Include root `.arcanum`, `arcanum/.arcanum`, and `implementation/domainspec/.arcanum` only as classification targets.
  - Do not parent-edit submodule-owned `.arcanum` paths.
  - Mark `.arcanum/runtimes/codex/commands/*` as legacy command adapters unless a compatibility gate says otherwise.
- Verification:
  - Classification table exists.
  - Generated/private classes have ignore/untrack recommendations.
  - Durable classes have provenance or explicit owner.

#### TASK-RUNTIME-003: Add Runtime-Native Adapter Metadata

- Layer: L1
- Owner route: `task-session`
- Write scope:
  - `tools/arcanum`
  - `tools/bootstrap_arcanum.sh`
  - `tools/install_arcanum.sh`
  - `.arcanum/runtime/config.json` only if selected for this repo
- Goal: Make runtime-native adapters the default orchestration family and keep `codex-exec` explicit legacy opt-in.
- Implementation detail:
  - Add adapter ids and metadata for `codex-skill`, `claude-skill`, `copilot-instructions`, and abstract selector `native-skill`.
  - Make `--exec` with a runtime-native adapter produce handoff prompt, output path, and receipt requirement instead of spawning Codex.
  - Treat `local-skill` as a compatibility alias for `codex-skill` only if older artifacts already depend on it.
  - Keep deterministic `--resolve`, `--list-adapters`, `--resolve-adapter`, and validation behavior.
- Verification:
  - `bash -n tools/arcanum tools/bootstrap_arcanum.sh tools/install_arcanum.sh`
  - `tools/arcanum --list-adapters`
  - `tools/arcanum --resolve-adapter codex-skill`
  - `tools/arcanum --resolve-adapter claude-skill`
  - `tools/arcanum --resolve-adapter copilot-instructions`
  - `tools/arcanum --resolve-adapter native-skill`
  - `tools/arcanum --get-default-adapter`

#### TASK-RUNTIME-004: Add Install Profiles

- Layer: L2
- Owner route: `task-session`
- Write scope:
  - `tools/bootstrap_arcanum.sh`
  - `tools/install_arcanum.sh`
  - runtime install docs or generated manifest templates
- Goal: Make new-user and repo-local setup explicit, with runtime-native generated packages instead of hand-maintained copies everywhere.
- Profiles:
  - `personal-codex`
  - `repo-local`
  - `github-copilot`
  - `claude`
  - `observability`
  - `all`
  - `none`
- Verification:
  - Dry-run profile output lists exact write targets.
  - Dry-run profile output lists canonical source, generated target, and alias mapping for each runtime package.
  - Default profile does not generate command files.
  - Repo-local profile does not mutate machine-global Codex home.

#### TASK-RUNTIME-005: Migrate Invoke/Refine/Task-Session Runtime Language

- Layer: L3
- Owner route: `task-session`
- Write scope:
  - personal skill wrappers only in a machine-global task
  - repo canonical contracts under `arcanum/` only when the Arcanum lifecycle task owns the change
  - root policy docs under `ops/`
- Goal: Remove default command-backed model execution assumptions from the skills that orchestrate multi-stage work.
- Implementation detail:
  - Replace required nested `tools/arcanum --exec` with parent-owned dispatch, native receipts, and task-session SWU handoff.
  - Preserve deterministic resolver/validator use.
  - Keep lifecycle ownership boundaries: Invoke authors artifacts, Refine refines, Task Session executes bounded SWUs.
- Verification:
  - Search results show no active contract requiring nested Codex CLI by default.
  - Remaining hits are classified as deterministic utility, explicit legacy, migration note, or historical evidence.

#### TASK-RUNTIME-006: Prune Legacy Command Adapters

- Layer: L3
- Owner route: `task-session`
- Write scope:
  - `.codex/commands/*`
  - `.arcanum/runtimes/codex/commands/*`
  - docs referencing those command files
- Goal: Complete the skills-first cleanup for command layers.
- Implementation detail:
  - Keep deletions already staged by the previous cleanup if validation still agrees.
  - Add a compatibility note only if a runtime explicitly requires commands.
- Verification:
  - No tracked root `.codex/commands/*.md` remain.
  - No tracked root `.arcanum/runtimes/codex/commands/*.md` remain.
  - Skill/runtime docs no longer list commands as required.

#### TASK-RUNTIME-007: Resolve Root `.github/skills` Adapter Role

- Layer: L3
- Owner route: `task-session`
- Write scope:
  - `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md`
  - `.github/skills/*` only after runtime/owner confirmation
- Goal: Decide which root skills are generated Copilot/GitHub-native adapters and which are stale duplicates.
- Implementation detail:
  - Confirm `.github/skills/arcanum-*` as a generated Copilot/GitHub-native distribution surface when provenance can be recorded.
  - Confirm DomainSpec duplicate ownership before deleting any `.github/skills/domainspec-*` or `gsd-*`.
  - Add alias classification for root packages whose names are invocation aliases over the same canonical capability.
- Verification:
  - Classification table has no `gate-delete` row without owner/runtime decision.
  - Any kept adapter maps to canonical source, runtime, generator, and alias status.
  - Any deletion maps to a keeper and regeneration/provenance rule.

### Smallest Working Units

| SWU | Parent task | Goal | Write scope | Verification |
| --- | --- | --- | --- | --- |
| SWU-RUNTIME-001 | TASK-RUNTIME-001 | Build active runtime surface inventory. | `ops/RUNTIME-SURFACE-INVENTORY.md` | No unclassified active surface class. |
| SWU-RUNTIME-002 | TASK-RUNTIME-002 | Classify root `.arcanum` state. | `ops/ARCANUM-STATE-CLASSIFICATION.md` | Each path class has keep/ignore/untrack/delete policy. |
| SWU-RUNTIME-003 | TASK-RUNTIME-003 | Add runtime-native adapter metadata. | `tools/arcanum` | Codex, Claude, Copilot, and abstract native adapters resolve. |
| SWU-RUNTIME-004 | TASK-RUNTIME-003 | Make legacy Codex CLI explicit opt-in. | `tools/arcanum` | Default adapter is runtime-native, `codex-exec` requires explicit selection. |
| SWU-RUNTIME-005 | TASK-RUNTIME-004 | Add profile dry-run behavior. | bootstrap/install scripts | Dry-run lists exact writes, provenance, and aliases for each profile. |
| SWU-RUNTIME-006 | TASK-RUNTIME-005 | Update orchestration skill language. | scoped Arcanum/ops docs | No active default nested CLI requirement remains. |
| SWU-RUNTIME-007 | TASK-RUNTIME-006 | Finish command adapter removal. | command adapter paths | Tracked command files are absent or explicitly legacy. |
| SWU-RUNTIME-008 | TASK-RUNTIME-007 | Resolve root GitHub skill adapter role. | classification and selected `.github/skills` paths | Root skills are adapter, root-owned, or deletion-approved. |

### Validation Strategy

- Shell syntax for touched scripts.
- Adapter resolution commands for Codex, Claude, Copilot, abstract native, and legacy adapters.
- Inventory grep for nested Codex and command-surface references.
- Git status review to distinguish user changes, generated state, and intended deletions.
- Classification review before deleting owner-boundary or submodule-owned surfaces.

### Gates

| Gate | Condition | On fail |
| --- | --- | --- |
| G-RUNTIME-001 | Active runtime surfaces are inventoried before migration edits. | block |
| G-RUNTIME-002 | `.arcanum` generated/private state is classified before untracking/deleting. | block |
| G-RUNTIME-003 | `tools/arcanum` runtime-native adapters have deterministic behavior. | block |
| G-RUNTIME-004 | `codex-exec` remains explicit legacy opt-in, not default. | block |
| G-RUNTIME-005 | Owner-boundary skill deletions have keeper and runtime confirmation. | block |
| G-RUNTIME-006 | Historical generated evidence is preserved unless cleanup is explicitly approved. | flag |
| G-RUNTIME-007 | Generated native packages record canonical source, runtime, generator, and alias status. | block |

## Current Recommended Execution Order

1. `TASK-RUNTIME-001`
2. `TASK-RUNTIME-002`
3. `TASK-RUNTIME-003`
4. `TASK-RUNTIME-004`
5. `TASK-RUNTIME-006`
6. `TASK-RUNTIME-007`
7. `TASK-RUNTIME-005`

This order prevents the most dangerous failure: deleting or rewriting a surface before knowing whether it is active runtime, generated install output, or durable evidence.

## Invoke Result

- Mode: design -> plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: flag
- Mode contracts: `arcanum/spells/invoke/design.md`, `arcanum/spells/invoke/plan.md`
- Outputs: `ops/ARCANUM-RUNTIME-SURFACE-INVOKE-DESIGN-PLAN.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Glossary consistency: n/a
- Implementation layering: inline L0-L3 layer table
- Work-pack: inline split-ready work-pack
- Complexity: medium
- Per-layer planning: layer-mapped tasks
- Implementation detail: task specs complete for current planning depth
- Smallest working units: complete
- Template/profile selection: Invoke design and plan mode contracts; standalone implementation-layering/work-pack structure adapted inline
- Validation strategy: command, grep, status, generated provenance, alias, and classification checks listed above
- Decisions: keep `tools/arcanum` as deterministic utility; classify `.arcanum`; generate native runtime packages from canonical source; account for aliases as thin generated packages; remove command defaults; add install profiles
- Unresolved gaps: DomainSpec-owned duplicate cleanup, provenance format details for generated runtime packages
- Next route: task-session
