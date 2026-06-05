# Runtime Surface Invoke Addition

Date: 2026-05-27
Mode: invoke design + plan companion
Target: repository organization runtime surface layer
Status: FLAG

## Intent

Add a missing repository organization layer for Codex, DomainSpec, Arcanum, GitHub Copilot, and other runtime surfaces.

The current repo does not only have source folders. It also has installed command surfaces, global machine defaults, repo-local runtime surfaces, project-local installed copies, generated observability state, and submodule-owned canonical sources. Without a runtime-surface policy, cleanup can delete the wrong thing or preserve stale installed copies as if they were source.

## Canonical Sources Used

- `arcanum/spells/invoke/README.md`
- `arcanum/spells/invoke/design.md`
- `arcanum/spells/invoke/plan.md`
- `ops/development/refinement-runs/2026-05-27-zone-taxonomy/RESULT.md`
- `ops/development/refinement-runs/2026-05-27-zone-taxonomy/DELETION-CANDIDATE-PASS.md`
- local scans of Codex, DomainSpec, Arcanum, and project runtime surfaces

## Discovery Snapshot

Observed surface counts:

| Surface | Count | Meaning |
| --- | ---: | --- |
| `/mnt/c/Users/vlad_/.codex/commands/*.md` | 82 | machine-global Codex command surface |
| `/mnt/c/Users/vlad_/.codex/skills/arcanum-*` | 29 | machine-global Arcanum skill snapshots |
| `arcanum/.codex/commands/*.md` | 83 | Arcanum repo command surface |
| `implementation/domainspec/.codex/commands/*.md` | 86 | DomainSpec repo-local command surface, including Arcanum command snapshots |
| `projects/body-war/.codex/commands/*.md` | 82 | untracked project-local command surface |
| `projects/sonar-loop/.github/skills/arcanum-*` | 31 | project-local GitHub Copilot Arcanum skill install |

Observed examples:

- Global Codex home: `/mnt/c/Users/vlad_/.codex/commands/invoke.md`, `/mnt/c/Users/vlad_/.codex/skills/arcanum-invoke/SKILL.md`
- Arcanum canonical repo: `arcanum/.codex/commands/invoke.md`, `arcanum/.agents/skills/*`, `arcanum/tools/arcanum`
- DomainSpec repo-local surface: `implementation/domainspec/.codex/commands/invoke.md`, `implementation/domainspec/.arcanum/runtime/config.json`, `implementation/domainspec/.github/skills/*`
- Project-local surface: `projects/sonar-loop/.github/skills/arcanum-*`, `projects/sonar-loop/.arcanum/*`, `projects/body-war/.codex/commands/*`
- Root installed/generated state: `.arcanum/`, `.codex/`, `.github/skills/`

## Design Result

The missing concept is **Runtime Surface Ownership**.

It should sit below repository zones and above deletion cleanup:

```text
canonical capability source
  -> installation recipe / bootstrap owner
    -> installed runtime surface
      -> generated runtime state
        -> local/private runtime state
```

This layer prevents four common mistakes:

1. Treating generated state as source.
2. Treating installed copies as canonical capability definitions.
3. Treating machine-global Codex defaults as repository-owned files.
4. Deleting stale installed surfaces without knowing whether a project still depends on them.

## Runtime Surface Taxonomy

| Surface kind | Examples | Owner | Track in repo? | Cleanup rule |
| --- | --- | --- | --- | --- |
| `canonical-source` | `arcanum/arcana/*`, `arcanum/spells/*`, `implementation/domainspec/copilot/skills/*` | owning source repo | yes, in owning repo only | edit here first; consumers sync from here |
| `command-adapter-source` | `arcanum/tools/arcanum`, Arcanum bootstrap scripts | Arcanum | yes, in Arcanum source | source of install behavior |
| `machine-global-install` | `/mnt/c/Users/vlad_/.codex/commands`, `/mnt/c/Users/vlad_/.codex/skills/arcanum-*` | user machine Codex home | no, outside repo | snapshot/install surface; audit separately |
| `repo-local-install` | root `.codex/commands`, root `.github/skills`, root `.arcanum/runtimes` | consuming repo | maybe | must have install manifest or generated marker |
| `submodule-local-install` | `implementation/domainspec/.codex/commands`, `implementation/domainspec/.arcanum` | submodule repo owner | yes/no per submodule policy | do not mutate from parent cleanup |
| `project-local-install` | `projects/sonar-loop/.github/skills/arcanum-*`, `projects/body-war/.codex/commands` | project owner | only if admitted as fixture/source | untrack if generated install output |
| `generated-observability` | `.arcanum/observability/signals/*.jsonl`, `reflection-state.json`, run folders | runtime surface | no by default | preserve locally, untrack after approval |
| `runtime-config` | `.arcanum/runtime/config.json`, adapter profiles | consuming repo | maybe | track only if it is safe, non-secret, and intended as repo config |
| `local-private-state` | Codex auth, private runtime homes, caches, SQLite runtime DBs | local machine | never | ignore; do not copy into evidence |

## Authority Rules

### Rule 1: Arcanum Owns Arcanum Capability Definitions

Canonical Arcanum sigils, spells, command adapters, bootstrap logic, and runtime adapter contracts live in `arcanum/`.

Installed copies under `.codex/`, `.github/skills/`, `.agents/skills/`, or `.arcanum/runtimes/` are surfaces, not new source, unless a local override file explicitly says otherwise.

### Rule 2: DomainSpec Owns DomainSpec Type A Skills

Canonical DomainSpec skills live under `implementation/domainspec/copilot/skills/`.

Installed DomainSpec copies under `implementation/domainspec/.github/skills/` are install targets. Parent repo cleanup must not edit them directly unless the DomainSpec submodule is the active target.

### Rule 3: Codex Home Is Machine Global

`/mnt/c/Users/vlad_/.codex` is not a repository zone. It is a machine-global install target.

It may contain useful defaults, but repo cleanup should only audit it and record drift. Mutation belongs in a separate machine-global Codex task.

### Rule 4: Project Installs Require Admission Metadata

Any `projects/<id>/.codex`, `projects/<id>/.github/skills`, `.Codex`, or `.arcanum` surface must declare whether it is:

- `source-fixture`,
- `generated-install`,
- `local-private`,
- `project-runtime-config`,
- `migration-leftover`.

Without that declaration, it is a cleanup candidate, not a canonical project asset.

### Rule 5: Generated State Is Not Source Unless Promoted

Telemetry, runtime runs, reflection state, SQLite projections, generated command outputs, and installed copies are generated by default.

Promotion requires an explicit reason:

- documentation fixture,
- validation fixture,
- golden snapshot,
- bootstrap contract example,
- durable evidence for a completed task.

## Six Design Views

### 1. Context View

The repository is a parent workspace with multiple execution surfaces:

- Codex desktop/global home,
- Arcanum source repo/submodule,
- DomainSpec implementation submodule,
- root repository surfaces,
- project-local incubator surfaces,
- GitHub Copilot surfaces,
- generated runtime/observability state.

### 2. High-Level Structure View

Runtime surfaces should be governed by a separate overlay:

```text
ops/runtime-surface-policy
  -> source authority map
  -> install target inventory
  -> generated-state policy
  -> drift/audit checks
  -> cleanup work-pack
```

### 3. Low-Level Components View

Components:

- Source authority map: canonical owner for every capability family.
- Install manifest: where commands/skills are installed and why.
- Surface classifier: classifies each `.codex`, `.github/skills`, `.agents`, `.arcanum`, `.Codex` path.
- Drift checker: compares installed copies against source or marks unmanaged.
- Cleanup ledger: records delete/untrack/keep decisions.

### 4. Workflow Process View

```text
scan runtime surfaces
  -> classify source vs install vs generated
  -> resolve owner
  -> compare to canonical source when applicable
  -> decide keep/untrack/delete/regenerate
  -> apply only approved changes
  -> run drift check
```

### 5. Decision Flow View

For each runtime surface:

1. Is it canonical source?
   - yes: keep and protect.
   - no: continue.
2. Is it an installed surface with a manifest?
   - yes: keep or regenerate from owner.
   - no: continue.
3. Is it generated/local/private state?
   - yes: ignore or untrack.
   - no: continue.
4. Is it needed as a fixture/evidence snapshot?
   - yes: mark as source-like fixture.
   - no: delete/untrack candidate.

### 6. Dependency Interface View

Interfaces:

- Arcanum source -> Codex command installs.
- Arcanum source -> GitHub Copilot skill installs.
- DomainSpec copilot source -> DomainSpec `.github/skills` installs.
- Root organization policy -> project admission metadata.
- Runtime surface policy -> deletion-candidate pass.
- Machine-global Codex home -> audit-only surface unless user explicitly requests global mutation.

## Plan Addition

Add this as a new layer before cleanup execution:

### `TASK-ORG-RUNTIME-000`: Runtime Surface Inventory

Goal:

- Inventory all `.codex`, `.github/skills`, `.agents/skills`, `.arcanum`, `.Codex`, and machine-global Codex surfaces relevant to this workspace.

Write scope:

- `ops/RUNTIME-SURFACE-POLICY.md`
- optional inventory output under `ops/runtime-surface-inventory.json`

Acceptance evidence:

- Inventory lists each surface path, owner, surface kind, tracked status, and cleanup action.

Verification:

```bash
find . -path './.git' -prune -o \( -path '*/.codex/*' -o -path '*/.github/skills/*' -o -path '*/.arcanum/*' -o -path '*/.agents/*' -o -path '*/.Codex/*' \) -print
```

### `TASK-ORG-RUNTIME-001`: Runtime Surface Policy

Goal:

- Create the policy that separates canonical source, installed surface, generated runtime state, and local/private runtime state.

Write scope:

- `ops/RUNTIME-SURFACE-POLICY.md`
- update `ops/REPOSITORY-ZONE-CONTRACT.md` after it exists.

Acceptance evidence:

- Policy includes authority rules for Arcanum, DomainSpec, Codex home, project-local installs, and generated state.

### `TASK-ORG-RUNTIME-002`: Install Manifest Convention

Goal:

- Define a lightweight manifest each repo/project can use to explain installed runtime surfaces.

Suggested manifest:

```yaml
surface_id: arcanum-codex-commands
surface_kind: repo-local-install
installed_from: arcanum/tools/bootstrap_arcanum.sh
source_owner: arcanum
runtime: codex
target_paths:
  - .codex/commands
mutation_policy: regenerate-from-source
tracked_policy: generated-install | source-fixture | repo-config
last_verified: YYYY-MM-DD
```

### `TASK-ORG-RUNTIME-003`: Drift And Cleanup Check

Goal:

- Add or extend a check that flags runtime surfaces with no manifest, generated state tracked as source, and stale installed copies.

Validation:

```bash
git ls-files '*/*.codex/*' '*/*.arcanum/*' '*/*.github/skills/*'
git status --short --ignored
```

### `TASK-ORG-RUNTIME-004`: Approved Cleanup

Goal:

- Apply approved delete/untrack/regenerate decisions.

Initial candidates:

- `sigils-library/`: superseded name for Arcanum.
- `.data/*.sqlite*`: generated projection files.
- `.arcanum/observability/*.jsonl` and `reflection-state.json`: generated telemetry unless promoted.
- `projects/body-war/.codex/commands`: untracked install surface; decide with project admission.
- `projects/sonar-loop/.github/skills/arcanum-*`: duplicate install review.
- `implementation/domainspec/.codex/commands`: submodule-local surface; do not mutate from parent cleanup.
- global `/mnt/c/Users/vlad_/.codex`: audit-only unless explicitly running a machine-global Codex cleanup.

## Decisions

- Add `runtime-surface` as a first-class organization layer.
- Do not collapse runtime surfaces into normal repository zones.
- Treat Codex global defaults as machine-global, not repo-owned.
- Treat DomainSpec repo-local defaults as submodule-owned unless working inside that submodule.
- Treat Arcanum installed copies in projects as generated installs unless the project admits them as fixtures.
- Use symlinks only for repo-local discovery facades where the source and consumer live in the same checkout.
- Use managed snapshots for machine-global Codex, GitHub Copilot, cross-repository installs, and command adapters.

## Gaps

Blocker before cleanup:

- Need approval for whether to create `ops/RUNTIME-SURFACE-POLICY.md` now.
- Need owner decisions for `projects/body-war/` and `projects/sonar-loop/` install surfaces.
- Need a decision on whether root `.agents/skills/arcanum-*` should become the parent repo symlink facade.

Non-blocker:

- A later script can produce a full JSON inventory. The current scan is enough for the design.
- A later installer can refresh managed snapshots and write manifests.

## Invoke Result

- Mode: design + plan companion
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: FLAG
- Mode contracts: `arcanum/spells/invoke/design.md`, `arcanum/spells/invoke/plan.md`
- Outputs: `ops/development/refinement-runs/2026-05-27-zone-taxonomy/RUNTIME-SURFACE-INVOKE.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Template/profile selection: architecture companion plus compact work-pack addition
- Implementation layering: inline runtime-surface layer addition
- Work-pack: companion tasks `TASK-ORG-RUNTIME-000` through `TASK-ORG-RUNTIME-004`
- Complexity: medium
- Decisions: runtime-surface ownership becomes a separate layer under repository organization
- Unresolved gaps: cleanup approvals and project-local runtime surface owner decisions
- Next route: task-session for `ops/RUNTIME-SURFACE-POLICY.md`, then decision-gate for cleanup choices
