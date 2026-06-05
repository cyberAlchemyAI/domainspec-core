# GitHub/Copilot Arcanum Naming Policy Decision

Date: 2026-06-01
Status: accepted
Decision source: `refine` over remaining surface migration blockers; user requested `invoke refresh` then task-session continuation

## Scope

This decision controls `TASK-SURFACE-003`, root GitHub/Copilot Arcanum package regeneration.

Mutation is blocked for:

- `.github/skills/arcanum-*`
- `.github/instructions/arcanum.instructions.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`

until a naming policy is selected.

## Evidence

Current root `.github/skills` Arcanum shape:

- 33 root Arcanum packages.
- 22 use `arcanum-sigil-*`.
- 8 use `arcanum-spell-*`.
- selected root names exist, such as `arcanum-orchestrate`, `arcanum-necronomicon`, and `arcanum-necronomicon-session`.

Staged `github-copilot` generator shape:

- 83 staged packages.
- 43 use flattened `arcanum-*` names.
- 40 are unprefixed aliases.

The staged shape does not merely refresh content. It renames the GitHub/Copilot discovery surface and adds unprefixed aliases into a root collaboration runtime that also contains DomainSpec and GSD skills.

## Decision Question

How should GitHub/Copilot Arcanum package names be generated before root package replacement?

## Options

### Option 1: Preserve Current GitHub/Copilot Names

Generate self-provenanced packages using the existing root discovery names:

- `arcanum-sigil-*` for sigils and transmutations,
- `arcanum-spell-*` for spells,
- existing special root names such as `arcanum-orchestrate`, `arcanum-necronomicon`, and `arcanum-necronomicon-session` where still valid.

Benefit: refreshes content and provenance without renaming the GitHub/Copilot runtime surface.

Cost or risk: GitHub/Copilot and personal Codex naming remain different by design.

When to choose it: when avoiding runtime discovery breakage matters more than name uniformity.

Downstream impact: update `github-copilot` profile generation to use Copilot-specific names; replace current wrappers safely; avoid unprefixed aliases unless separately reviewed.

Recommendation: choose this.

### Option 2: Migrate GitHub/Copilot To Flattened Names

Replace current names with flattened names matching personal Codex:

- `arcanum-refine`,
- `arcanum-invoke`,
- `arcanum-task-session`,
- familiar unprefixed aliases such as `invoke`, `refine`, and `task-session`.

Benefit: naming is uniform across Codex and GitHub/Copilot.

Cost or risk: breaks or changes the root GitHub/Copilot discovery surface and may collide with non-Arcanum root skills.

When to choose it: when cross-runtime name uniformity is worth a deliberate breaking migration.

Downstream impact: requires migration notes, compatibility checks, and root `.github/skills` cleanup beyond Arcanum wrappers.

### Option 3: Generate Both Legacy Names And Flattened Aliases Temporarily

Keep current `arcanum-sigil-*` / `arcanum-spell-*` names and also generate flattened aliases.

Benefit: supports transition and discovery experiments.

Cost or risk: increases duplicate surface area and delays cleanup.

When to choose it: when runtime confirmation needs both naming shapes available before pruning.

Downstream impact: requires a temporary compatibility window, explicit alias expiry, and later pruning task.

## Selected Option

Option 1: Preserve Current GitHub/Copilot Names.

Generate self-provenanced GitHub/Copilot packages using existing root discovery names:

- `arcanum-sigil-*` for sigils and transmutations,
- `arcanum-spell-*` for spells,
- selected root names such as `arcanum-orchestrate`, `arcanum-necronomicon`, and `arcanum-necronomicon-session` where still valid.

## Recommended Selection

Option 1.

## Rationale For Recommendation

The current goal is to finish organization and migration cleanly, not introduce a runtime surface rename. Option 1 removes wrapper-to-cache behavior while preserving existing GitHub/Copilot discovery handles.

## Remaining Blockers

None for resuming `TASK-SURFACE-003`.

## Next Route

Resume `TASK-SURFACE-003` by updating the GitHub/Copilot generator profile to preserve current root discovery names, then stage and replace root Arcanum GitHub packages only after validation.

## Deferred Decisions

- Whether flattened aliases should ever be added to root `.github/skills`.
- Whether GitHub/Copilot naming should converge with personal Codex naming in a later breaking migration.

## Assumptions

- DomainSpec and GSD `.github/skills` packages remain out of Arcanum cleanup.
- `.arcanum/runtimes/github-copilot` cache cleanup waits until root Arcanum GitHub packages are self-provenanced.
