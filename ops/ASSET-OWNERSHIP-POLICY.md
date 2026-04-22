# Asset Ownership Policy (3-Repo Topology)

This policy defines ownership, synchronization, and pointer propagation for automation assets across:

- `domainspec-core` (research orchestration root)
- `implementation/domainspec` (DomainSpec implementation source of truth)
- `validation/poker-team` (validation harness)

## Asset Classes

### Type A: Canonical DomainSpec Pack

Reusable `domainspec-*` automation intended for distribution to any project using DomainSpec.

Source of truth:
- `implementation/domainspec/copilot/agents`
- `implementation/domainspec/copilot/skills`

Install target(s):
- `implementation/domainspec/.github/agents`
- `implementation/domainspec/.github/skills`
- Optional consumer copies (for example `validation/poker-team/.github/*`) when explicitly required

Rule:
- Never hand-edit Type A assets in consumer repos.
- Edit canonical source in `copilot/`, then install/sync outward.

Conflict resolution rule:

- If consumer and canonical Type A files diverge, verify file-by-file before migration.
- When the consumer version is confirmed newer, promote that content into canonical `copilot/` first, then sync to install targets.

### Type B: Research Orchestration Pack

Research-focused assets (for example `domainspec-research-*`) used to run experiments, inventory work, and synthesis.

Source of truth:
- `domainspec-core/.github`
- `domainspec-core/research/projects/*`
- `domainspec-core/research/shared/*`
- `domainspec-core/research/registry/*`

Rule:
- Type B should not remain as poker-team-only drift.
- Promote to root orchestration ownership when validated.

Project containment rule:

- Each research project under `research/projects/` is self-contained.
- Cross-project reuse is allowed only through declared dependencies and published exports.
- Internal project files are not direct dependency targets for other projects.

Compatibility handling rule:

- Default behavior is canonical-only paths.
- Do not add compatibility aliases, redirect files, duplicate path mirrors, or symlink shims unless explicitly requested.
- Breaking path changes are acceptable when migrating toward canonical ownership boundaries.
- If compatibility handling is explicitly requested, it must be temporary, documented, and removed after the migration window.

### Type C: Project-Local Overlays

Validation or project-specific assets that should remain local to one consumer repository.

Source of truth:
- The local repository where the overlay is used (for example `validation/poker-team/.github`)

Rule:
- Type C must be explicitly marked as local overlay and excluded from canonical drift checks.

## Pointer Propagation Policy (Policy 1)

Update only affected repositories based on changed asset type.

- If Type A changes:
  1. Commit in `implementation/domainspec` canonical source.
  2. Update consumer copies only where needed.
  3. Update parent submodule pointers only for repos that consume updated commits.
- If Type B changes:
  1. Commit in `domainspec-core` root orchestration assets.
  2. Do not force poker-team pointer updates unless it consumes those assets.
- If Type C changes:
  1. Commit only in the local consumer repo.
  2. No mandatory propagation.

## Enforcement

Use `tools/check_github_drift.sh` from `domainspec-core`:

- Fails when Type A or Type B assets are found as poker-team-only drift.
- Allows Type C poker-team overlays via explicit allowlist.
- Runs research structure enforcement via `tools/check_research_structure.sh`.
- Fails when compatibility aliases/symlinks are present under `research/` unless explicitly enabled by `ALLOW_RESEARCH_COMPATIBILITY=1`.

## Workspace Entry Decision

No forced default workspace entrypoint.

- Operators may open any repo directly.
- Optional convenience workspace remains available at:
  - `validation/poker-team/domainspec-unified.code-workspace`
