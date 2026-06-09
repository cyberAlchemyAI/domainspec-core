# Arcanum Surface Map And Plan

Date: 2026-05-31
Mode: invoke design -> invoke plan
Status: flag
Target: Arcanum capability/runtime surfaces across repository, generated runtime packages, and personal Codex home

## Objective

Map every active Arcanum-adjacent surface that can influence capability discovery or execution, then plan the cleanup so native runtime skills are the primary surface and `tools/arcanum` remains deterministic support rather than the default capability executor.

## Governing Correction

The old sentence is no longer the desired contract:

```text
context-builder, invoke, interrogation, and distill resolve through tools/arcanum
```

The corrected contract is:

```text
context-builder, invoke, interrogation, and distill are selected from the active native runtime skill surface.
tools/arcanum may validate deterministic handles, adapter metadata, provenance, and receipts, but it is not the default execution surface.
```

This means `tools/arcanum --resolve` is compatibility/provenance support, not the primary stage-selection rule. `tools/arcanum --exec` with native adapters prepares handoff/receipt contracts. Model-backed CLI execution remains explicit legacy opt-in through adapters such as `codex-exec` or `codex-bypass`.

## Source Contracts

- `arcanum/spells/invoke/README.md`
- `arcanum/spells/invoke/design.md`
- `arcanum/spells/invoke/plan.md`
- `ops/ARCANUM-RUNTIME-SURFACE-INVOKE-DESIGN-PLAN.md`
- `ops/development/TASK-SESSION-RUNTIME-005.md`
- `ops/development/TASK-SESSION-RUNTIME-006.md`
- `docs/decisions/install-profile-contract.md`
- `docs/decisions/native-runtime-skill-surface.md`
- `arcanum/tools/bootstrap_arcanum.sh`
- `arcanum/tools/install_arcanum.sh`
- `arcanum/tools/arcanum`

## Surface Map

| Surface | Observed shape | Authority class | Current state | Target policy |
| --- | --- | --- | --- | --- |
| Arcanum canonical source | `arcanum/arcana/*`, `arcanum/spells/*`, `arcanum/formulae/*` | canonical source | Source for generated runtime packages. Some files already shifted to native runtime receipt language. | Keep and edit here first. |
| Personal Codex skills | `/mnt/c/Users/vlad_/.codex/skills/*/SKILL.md` | generated native runtime package or hand-maintained wrapper | 34 skills total; Arcanum wrappers include stale command-backed language for `refine`, `invoke`, and `task-session`. | Regenerate through explicit `personal-codex`; aliases must be thin native skill packages. |
| Personal Codex commands | `/mnt/c/Users/vlad_/.codex/commands/*.md` | legacy command compatibility | 82 personal command files exist. | Do not treat as canonical; prune or leave only explicit compatibility bridges after skill refresh. |
| Root `.github/skills` Arcanum | `.github/skills/arcanum-*` | generated GitHub/Copilot package | 145 tracked GitHub skill packages overall. Arcanum skills currently point to `.arcanum/runtimes/github-copilot/...`, an older cache-copy shape. | Regenerate as first-class GitHub/Copilot native packages with inline provenance; stop depending on `.arcanum/runtimes/github-copilot` as canonical. |
| Root `.github/skills` DomainSpec | `.github/skills/domainspec-*` | DomainSpec runtime package | Active DomainSpec skill family, not owned by Arcanum cleanup. | Classify separately; do not delete during Arcanum task. |
| Root `.github/skills` GSD | `.github/skills/gsd-*` and `.github/get-shit-done/*` | third-party/runtime package family | Active GSD package family with workflows and agents. | Out of Arcanum scope except collision/routing notes. |
| GitHub/Copilot instructions and agents | `.github/copilot-instructions.md`, `.github/instructions/*`, `.github/agents/*` | runtime guidance | Active. Contains DomainSpec, GSD, and other agent surfaces. | Keep, but route Arcanum guidance to generated native package policy. |
| Root `.claude` | `.claude/*` | planned native runtime package | Not present at root in current scan. | Generate only through explicit `claude` or `all` profile. |
| Root `.codex/commands` | `.codex/commands/*.md` | legacy command compatibility | 9 tracked files, currently deleted in worktree. | Preserve deletion unless explicit compatibility decision reopens. |
| Root `.arcanum/runtimes/codex/commands` | `.arcanum/runtimes/codex/commands/*.md` | legacy command adapter snapshot | 7 tracked files, currently deleted in worktree. | Preserve deletion; do not regenerate by default. |
| Root `.arcanum/runtimes/github-copilot` | `.arcanum/runtimes/github-copilot/**` | generated runtime cache/snapshot | 83 files observed. Feeds older `.github/skills` wrapper shape. | Convert to either generated cache with manifest or remove after `.github/skills` becomes self-provenanced. |
| Root `.arcanum/observability` | config, ledgers, reflection state, runs, hooks | mixed config and generated evidence | Config plus generated JSONL ledgers and reflection state exist. | Track config/structure; treat ledgers and reflection state as local/generated unless promoted. |
| Root `.arcanum/necronomicon` | README, capabilities, sessions, updates | repo-local harness state | Durable repo-local harness state. | Keep if owner still active; not a skill source. |
| `tools/arcanum` | deterministic resolver, adapter metadata, handoff/receipt generator | deterministic utility | Active and recently updated for native adapters. | Keep, but do not make it the default model execution path. |
| `bootstrap_arcanum.sh` / `install_arcanum.sh` | install profiles | deterministic installer | Supports explicit profiles: `personal-codex`, `repo-local`, `github-copilot`, `claude`, `observability`, `all`, `none`. | Use to regenerate native packages; `all` must exclude personal Codex. |
| Nested repo surfaces | `arcanum/.codex`, `arcanum/.github`, `arcanum/.arcanum`, etc. | sub-repo local state/runtime | Many dirty or historical surfaces exist inside nested Arcanum repo. | Treat as Arcanum-owned; avoid parent cleanup unless task scope enters nested repo. |
| DomainSpec implementation surfaces | `implementation/domainspec/.codex`, `.github`, `.claude`, `.arcanum`, `.agents` | submodule-owned runtime surfaces | Active downstream surfaces. | Do not parent-edit; route through DomainSpec-owned task. |
| Project/demo surfaces | `projects/*/.codex`, `.arcanum`, `.github`, `.agents` | local project runtime state | Present in multiple project folders. | Classify as local/project-owned; do not sweep in Arcanum cleanup. |

## Design Views

### 1. Context View

The repository has three separate runtime audiences:

- machine-global operator runtime: personal Codex skills and commands,
- repository-hosted collaboration runtime: GitHub/Copilot skills, instructions, and agents,
- repo-local deterministic support: `tools/arcanum`, `.arcanum/runtime`, observability, and harness state.

The old shape blurred these by making `tools/arcanum` the route through which stage capabilities were expected to happen. The new shape makes each host runtime receive native package files and lets `tools/arcanum` validate, generate, or record receipts.

### 2. High-Level Structure View

```text
canonical Arcanum source
  -> explicit install profile
    -> native runtime package
      -> Codex / Claude / GitHub-Copilot execution
  -> deterministic utility support
    -> adapter metadata, provenance, validation, handoff receipts
  -> classified repo-local state
    -> config, accepted evidence, generated/private state
```

### 3. Low-Level Components View

- Canonical sources: `arcanum/arcana`, `arcanum/spells`, `arcanum/formulae`.
- Native runtime packages: `$CODEX_HOME/skills`, `.github/skills`, `.claude/skills`.
- Alias packages: unprefixed package names such as `invoke`, `refine`, and `task-session`, pointing to generated canonical packages such as `arcanum-invoke`.
- Runtime guidance: `.github/copilot-instructions.md`, `.github/instructions/*`, `.claude/agents/*`, `CLAUDE.md`, `AGENTS.md`.
- Deterministic support: `tools/arcanum`, adapter profiles, installer profiles.
- Legacy compatibility: `.codex/commands`, `.arcanum/runtimes/codex/commands`, personal Codex commands.
- Generated state/evidence: `.arcanum/observability/*.jsonl`, `.arcanum/observability/reflection-state.json`, runtime run folders.

### 4. Workflow Process View

```text
map surfaces
  -> classify authority
  -> correct contract wording
  -> regenerate native packages
  -> prune legacy command surfaces
  -> consolidate generated caches
  -> validate native-first discovery
```

### 5. Decision Flow View

For every surface:

1. Is it canonical source?
   - Edit source first.
2. Is it a native runtime package?
   - Keep only with provenance and regeneration path.
3. Is it an alias?
   - Keep only as a thin package with `alias_of`.
4. Is it a deterministic support tool?
   - Keep, but do not make it the default execution authority.
5. Is it legacy command compatibility?
   - Delete or leave only after explicit compatibility decision.
6. Is it generated evidence/state?
   - Ignore/untrack unless promoted as durable evidence.
7. Is it submodule/project-owned?
   - Do not mutate from the parent task.

### 6. Dependency Interface View

| From | To | Interface rule |
| --- | --- | --- |
| Canonical Arcanum source | Install profiles | Source-to-package generation only. |
| Install profiles | Personal Codex | Explicit `personal-codex`; never included in repo `all`. |
| Install profiles | GitHub/Copilot | Explicit `github-copilot` or repo `all`; writes native `.github/skills` and guidance. |
| Install profiles | Claude | Explicit `claude` or repo `all`; writes `.claude/skills`, `.claude/agents`, `CLAUDE.md`. |
| Runtime packages | Stage execution | Native runtime owns model-backed work. |
| `tools/arcanum` | Runtime packages | Validates handles, adapters, provenance, and receipts. |
| `.arcanum` | Observability/state | Stores classified config and evidence; not canonical skill source. |

## Planning Result

Complexity: medium-high.

Reason: the cleanup spans machine-global Codex state, root GitHub/Copilot packages, root repo state, nested Arcanum source, submodule-owned DomainSpec surfaces, and legacy command snapshots.

## Work-Pack

### TASK-SURFACE-001: Freeze Native-First Contract

- Status: pass
- Goal: Make the native-first contract explicit before more generation or deletion.
- Write scope:
  - `ops/ARCANUM-SURFACE-MAP-AND-PLAN.md`
  - optional policy note under `docs/decisions/`
- Actions:
  - Record that `context-builder`, `invoke`, `interrogation`, and `distill` are native runtime capabilities first.
  - Record `tools/arcanum` as deterministic support.
  - Mark command-backed language as stale except explicit legacy adapters.
- Verification:
  - Search active policy/source files for default command-backed wording.
  - Decision recorded in `docs/decisions/native-runtime-skill-surface.md`.

### TASK-SURFACE-002: Refresh Personal Codex Skills

- Status: pass
- Goal: Replace stale personal skill wrappers with generated native packages and thin aliases.
- Write scope:
  - `/mnt/c/Users/vlad_/.codex/skills/*`
- Actions:
  - Run explicit `personal-codex` profile into a staging folder first.
  - Compare staged skills against current personal skills.
  - Promote generated native packages only after reviewing alias names and provenance.
  - Keep `invoke`, `refine`, `task-session`, `context-builder`, `distill`, and `interrogation` as native skill package names or thin aliases.
- Verification:
  - No personal active skill requires `tools/arcanum --exec` for normal stage execution.
  - Alias packages include `alias_of` and canonical source provenance.
- Gate:
  - Decision passed in `docs/decisions/personal-codex-skill-refresh.md`.
  - Approved route: stage, compare, then promote reviewed generated Arcanum packages into the machine-global Codex home.

### TASK-SURFACE-003: Regenerate Root GitHub/Copilot Arcanum Packages

- Status: pass
- Goal: Convert root `.github/skills/arcanum-*` from wrapper-to-cache shape into direct generated native packages with provenance.
- Write scope:
  - `.github/skills/arcanum-*`
  - `.github/instructions/arcanum.instructions.md`
  - `.github/copilot-instructions.md` only if needed
  - `AGENTS.md` only if needed
- Actions:
  - Stage generated packages using `--profile github-copilot` in a temporary target.
  - Compare against current `.github/skills/arcanum-*`.
  - Replace wrappers that only point to `.arcanum/runtimes/github-copilot`.
  - Keep DomainSpec and GSD families out of scope.
- Verification:
  - Each kept Arcanum GitHub skill has `surface_kind`, `runtime`, `canonical_source`, `alias_of`, `generated_by`, and `mutation_policy`.
- Result:
  - Naming decision recorded in `docs/decisions/github-copilot-arcanum-naming-policy.md`.
  - `arcanum/tools/bootstrap_arcanum.sh` now writes GitHub/Copilot packages using current root discovery names: `arcanum-sigil-*`, `arcanum-spell-*`, and selected compatibility aliases.
  - Replaced the 33 existing root Arcanum GitHub/Copilot packages only; DomainSpec, GSD, and staged extra Arcanum packages stayed out of scope.
  - Active root Arcanum `SKILL.md` files no longer point to `.arcanum/runtimes/github-copilot`.

### TASK-SURFACE-004: Decide `.arcanum/runtimes/github-copilot`

- Status: pass
- Goal: Decide whether the generated runtime cache remains useful after root `.github/skills` is self-provenanced.
- Write scope:
  - `.arcanum/runtimes/github-copilot/**`
  - `ops/ARCANUM-STATE-CLASSIFICATION.md`
- Options:
  - keep as generator cache with manifest,
  - delete after root package regeneration,
  - untrack and regenerate on demand.
- Recommended option:
  - Delete or untrack after `.github/skills` are self-provenanced, unless a tool still reads the cache directly.
- Verification:
  - `rg ".arcanum/runtimes/github-copilot" .github arcanum tools ops` shows no active dependency except migration notes.
- Gate:
  - Cleanup decision passed in `docs/decisions/surface-cleanup-blocker-decisions.md`: untrack and regenerate on demand after root packages are self-provenanced.
- Result:
  - Added `.arcanum/runtimes/github-copilot/` to root `.gitignore`.
  - Untracked 83 generated GitHub/Copilot runtime cache files with `git rm -r --cached`, leaving the files on disk.
  - Confirmed active `.github/**/SKILL.md` files do not reference `.arcanum/runtimes/github-copilot`.

### TASK-SURFACE-005: Finish Legacy Command Adapter Removal

- Status: pass
- Goal: Complete the skills-first cleanup for tracked root command snapshots.
- Write scope:
  - `.codex/commands/*`
  - `.arcanum/runtimes/codex/commands/*`
  - docs that list those as required
- Actions:
  - Preserve current worktree deletions for 9 root `.codex/commands` and 7 `.arcanum/runtimes/codex/commands` files.
  - Remove stale docs that say normal execution requires commands.
  - Leave personal command cleanup for a machine-global task.
- Verification:
  - `git ls-files .codex/commands .arcanum/runtimes/codex/commands` returns no tracked files after cleanup commit.
- Result:
  - Staged removal of 9 root `.codex/commands/*.md` files and 7 `.arcanum/runtimes/codex/commands/*.md` files.
  - Updated active Arcanum source docs so `.codex/commands` is described as explicit legacy compatibility, not the normal installed runtime surface.
  - Confirmed no root command files remain in the worktree and no tracked root command files remain in the index.

### TASK-SURFACE-006: Classify Root `.arcanum` Evidence And State

- Status: pass
- Goal: Separate durable config/harness state from generated evidence.
- Write scope:
  - `.gitignore`
  - `.arcanum/observability/*` tracking state only after review
  - `ops/ARCANUM-STATE-CLASSIFICATION.md`
- Actions:
  - Keep README/config/gitkeep files when useful.
  - Treat JSONL ledgers, hook logs, runtime runs, and reflection state as generated/local by default.
  - Keep `.arcanum/necronomicon` harness state only if still actively used.
- Verification:
  - Generated ledgers are ignored or explicitly promoted.
- Result:
  - Added ignore rules for `.arcanum/observability/**/*.jsonl` and `.arcanum/observability/reflection-state.json`.
  - Untracked generated observability ledgers and reflection state while leaving local files on disk.
  - Kept observability README, config, `.gitkeep`, and scoped ignore files tracked.

### TASK-SURFACE-007: Protect Submodule And Project-Owned Surfaces

- Status: pass
- Goal: Prevent broad cleanup from mutating nested owner surfaces accidentally.
- Write scope:
  - `ops/SURFACE-OWNER-BOUNDARIES.md` or this plan
- Actions:
  - Mark `implementation/domainspec/*`, `projects/*`, `validation/*`, and nested `arcanum/*` runtime folders as owner-scoped.
  - Create separate work-packs if those surfaces need migration.
- Verification:
  - Cleanup tasks list owner scope before mutation.
- Result:
  - Added `ops/SURFACE-OWNER-BOUNDARIES.md`.
  - Classified root-owned, nested Arcanum-owned, DomainSpec-owned, project-owned, validation-owned, machine-global, and generated local state boundaries.
  - Recorded that child runtime surfaces require separate owner-scoped work-packs before mutation.

## Smallest Working Units

| SWU | Parent | Goal | Write scope | Verification |
| --- | --- | --- | --- | --- |
| SWU-SURFACE-001 | TASK-SURFACE-001 | Record native-first stage capability contract. | `ops/ARCANUM-SURFACE-MAP-AND-PLAN.md`, optional decision doc | Active policy says native skills first, tools support second. |
| SWU-SURFACE-002 | TASK-SURFACE-002 | Generate personal Codex staging package. | temp directory only | Staged package contains provenance and aliases. |
| SWU-SURFACE-003 | TASK-SURFACE-002 | Promote personal Codex skills after approval. | `/mnt/c/Users/vlad_/.codex/skills` | Stale command-backed wording removed from active personal skills. |
| SWU-SURFACE-004 | TASK-SURFACE-003 | Generate GitHub/Copilot staging package. | temp directory only | Staged `.github/skills` includes direct provenance. |
| SWU-SURFACE-005 | TASK-SURFACE-003 | Replace root Arcanum GitHub wrappers. | `.github/skills/arcanum-*` | No Arcanum root wrapper depends on `.arcanum/runtimes/github-copilot`. |
| SWU-SURFACE-006 | TASK-SURFACE-004 | Decide runtime cache fate. | decision artifact | Keep/delete/untrack decision recorded. |
| SWU-SURFACE-007 | TASK-SURFACE-005 | Remove tracked root command snapshots. | `.codex/commands`, `.arcanum/runtimes/codex/commands` | No tracked root command adapters remain. |
| SWU-SURFACE-008 | TASK-SURFACE-006 | Update generated-state ignore/untrack policy. | `.gitignore`, state classification | Generated logs/ledgers are not default tracked source. |

## Execution Order

1. `TASK-SURFACE-001` - pass
2. `TASK-SURFACE-002` - pass
3. `TASK-SURFACE-003` - pass
4. `TASK-SURFACE-004` - pass
5. `TASK-SURFACE-005` - pass
6. `TASK-SURFACE-006` - pass
7. `TASK-SURFACE-007` - pass

## Gates

| Gate | Condition | On fail |
| --- | --- | --- |
| G-SURFACE-001 | Native-first contract accepted before refresh. | block |
| G-SURFACE-002 | Machine-global Codex mutation explicitly approved. | block personal promotion |
| G-SURFACE-003 | Generated packages have provenance and aliases. | block promotion |
| G-SURFACE-004 | Root GitHub Arcanum packages no longer depend on cache before cache deletion. | block cache deletion |
| G-SURFACE-005 | DomainSpec/GSD/project surfaces are owner-classified. | block broad cleanup |
| G-SURFACE-006 | Historical evidence is preserved unless cleanup is explicit. | flag |

## Validation Strategy

- `bash -n arcanum/tools/arcanum arcanum/tools/bootstrap_arcanum.sh arcanum/tools/install_arcanum.sh`
- Generate profile staging directories for `personal-codex` and `github-copilot`.
- Search active surfaces for stale phrases:
  - `command-backed stage execution`
  - `resolve through tools/arcanum`
  - `tools/arcanum --exec --output`
  - `.codex/commands` as required surface
- Check generated package frontmatter/provenance.
- Check no root Arcanum GitHub skill wrapper points only to `.arcanum/runtimes/github-copilot`.
- Check tracked command snapshots are absent after cleanup.

## Invoke Result

- Mode: design -> plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library/runtime-surface cleanup
- Phase status: flag
- Mode contracts: `arcanum/spells/invoke/design.md`, `arcanum/spells/invoke/plan.md`
- Outputs: `ops/ARCANUM-SURFACE-MAP-AND-PLAN.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Template/profile selection: architecture map plus work-pack/SWU plan
- Implementation layering: inline, native-first surface migration order
- Work-pack: inline tasks and SWUs
- Decisions: native runtime packages are primary capability surfaces; `tools/arcanum` is deterministic support and legacy compatibility only
- Unresolved gaps: explicit approval needed before mutating `/mnt/c/Users/vlad_/.codex/skills`; decision needed for `.arcanum/runtimes/github-copilot`
- Completed route: `TASK-SURFACE-001` through `TASK-SURFACE-007` passed for the parent repository surface cleanup plan.
- Remaining route: child-owned migrations require separate owner-scoped work-packs.
