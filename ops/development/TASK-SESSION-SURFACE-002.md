# Task Session: Personal Codex Skill Refresh

Date: 2026-05-31
Task: `TASK-SURFACE-002`
SWU: `SWU-SURFACE-002`
Result: BLOCK

## Objective

Refresh the machine-global personal Codex Arcanum skill surface by staging generated native packages, comparing them with the active personal surface, then promoting only after the staged packages are safe.

## Context Pack

Controlling sources:

- `ops/ARCANUM-SURFACE-MAP-AND-PLAN.md`
- `docs/decisions/personal-codex-skill-refresh.md`
- `docs/decisions/surface-cleanup-blocker-decisions.md`
- `docs/decisions/native-runtime-skill-surface.md`
- `docs/decisions/install-profile-contract.md`
- `arcanum/tools/bootstrap_arcanum.sh`

Controlling decisions:

- Personal Codex refresh is approved as stage, compare, then promote.
- Promotion must back up replaced Arcanum skill packages first.
- Promotion must be limited to Arcanum-generated packages and aliases.
- Native runtime skills/packages are the primary model-backed surface.
- `tools/arcanum` remains deterministic support, not the default model-backed execution path.

## Work Performed

Generated a staging Codex home with:

```bash
arcanum/tools/bootstrap_arcanum.sh \
  --profile personal-codex \
  --codex-home /tmp/arcanum-personal-codex-stage-20260531T171344Z/.codex \
  --force
```

Staging result:

- staged skill packages: 83
- overlap with active personal Codex skills: 32
- new generated packages/aliases: 51
- staged path: `/tmp/arcanum-personal-codex-stage-20260531T171344Z/.codex/skills`

The staged packages include the required generated provenance fields:

- `surface_kind: generated-native-runtime-package`
- `runtime: codex`
- `canonical_source`
- `alias_of`
- `generated_by`
- `mutation_policy`

## Blocker

Promotion is blocked because the staged `personal-codex` generator output currently emits `SKILL.md` files only.

Several canonical skill packages reference package-local support paths such as:

- `templates/`
- `development/`
- `scripts/`
- `examples/`

Existing personal packages such as `arcanum-refine` and `refine` already contain companion folders. Replacing active package directories with the current staged output would remove those companion assets. Promoting only `SKILL.md` files would preserve old companion folders, but could leave stale assets under newly refreshed package contracts.

That makes direct promotion unsafe until package completeness is resolved.

## Decision Pack

Recommended fix:

1. Update the generator so native runtime packages copy needed package-local support directories from canonical source, excluding noisy generated run evidence by policy.
2. Regenerate the `personal-codex` staging package.
3. Re-run comparison.
4. Back up active overlapping Arcanum packages.
5. Promote the complete generated packages.

Alternative:

- Promote `SKILL.md` only and preserve existing companion folders. This is faster but risks stale package-local assets.

Rejected for this task session:

- Replace active directories with `SKILL.md`-only staged packages.

## Gate Verdict

BLOCK.

No mutation was made to `/mnt/c/Users/vlad_/.codex/skills`.

## Validation

Commands/checks:

```bash
find /tmp/arcanum-personal-codex-stage-20260531T171344Z/.codex/skills -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l
comm -12 <staged package names> <active package names> | wc -l
comm -23 <staged package names> <active package names> | wc -l
rg -n 'surface_kind: generated-native-runtime-package|runtime: codex|canonical_source:|alias_of:' /tmp/arcanum-personal-codex-stage-20260531T171344Z/.codex/skills
find arcanum/arcana arcanum/spells arcanum/transmutations -mindepth 2 -maxdepth 3 -type d \( -name templates -o -name examples -o -name assets -o -name scripts -o -name development \)
```

## Follow-Up

Next route: task-session or small implementation fix for `arcanum/tools/bootstrap_arcanum.sh` package completeness, then resume `TASK-SURFACE-002`.
