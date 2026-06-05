# Task Session: Root GitHub/Copilot Arcanum Package Regeneration

Date: 2026-05-31
Task: `TASK-SURFACE-003`
SWU: `SWU-SURFACE-004`
Result: BLOCK

## Objective

Regenerate root GitHub/Copilot Arcanum packages as self-provenanced native packages, replacing old wrappers that point at `.arcanum/runtimes/github-copilot`.

## Context Pack

Sources:

- `ops/ARCANUM-SURFACE-MAP-AND-PLAN.md`
- `docs/decisions/native-runtime-skill-surface.md`
- `docs/decisions/install-profile-contract.md`
- `docs/decisions/surface-cleanup-blocker-decisions.md`
- `arcanum/tools/bootstrap_arcanum.sh`

Controlling constraints:

- Keep DomainSpec and GSD root GitHub skill families out of Arcanum cleanup.
- Root GitHub/Copilot Arcanum packages should become self-provenanced.
- Do not delete `.arcanum/runtimes/github-copilot` until root wrappers no longer depend on it.
- Do not rename runtime discovery packages without an explicit naming decision.

## Work Performed

Generated staged GitHub/Copilot output:

```bash
arcanum/tools/bootstrap_arcanum.sh \
  --target /tmp/arcanum-github-copilot-stage-20260531T234051Z \
  --profile github-copilot \
  --force
```

Staging result:

- staged packages total: 83
- staged `arcanum-*` packages: 43
- current root `.github/skills/arcanum-*` packages: 33
- current root `.github/skills` packages total: 145

## Blocker

The staged package naming shape does not match the current root GitHub/Copilot Arcanum surface.

Current root examples:

- `arcanum-sigil-context-builder`
- `arcanum-sigil-task-session`
- `arcanum-spell-invoke`
- `arcanum-spell-implementation-readiness`

Staged generator examples:

- `arcanum-context-builder`
- `arcanum-task-session`
- `arcanum-invoke`
- `arcanum-implementation-readiness`
- unprefixed aliases such as `invoke`, `refine`, and `task-session`

Replacing now would not merely refresh wrappers. It would rename the GitHub/Copilot discovery surface and add unprefixed aliases into root `.github/skills`, which could collide with non-Arcanum root skill policy.

## Decision Needed

Choose the GitHub/Copilot naming policy before mutation:

1. Preserve current root GitHub/Copilot names: generate `arcanum-sigil-*` and `arcanum-spell-*` packages for Copilot, with optional compatibility aliases only after review.
2. Migrate root GitHub/Copilot to flattened names matching Codex personal packages, and record the rename as an intentional runtime breaking change.
3. Generate both legacy names and flattened aliases temporarily, then prune after runtime confirmation.

Recommended option: 1.

Rationale: it refreshes package content/provenance without changing root GitHub/Copilot discovery names during the same task.

## Gate Verdict

BLOCK.

No mutation was made to `.github/skills`, `.github/instructions`, `.github/copilot-instructions.md`, or `AGENTS.md`.

## Validation

Commands/checks:

```bash
find /tmp/arcanum-github-copilot-stage-20260531T234051Z/.github/skills -mindepth 1 -maxdepth 1 -type d
find .github/skills -mindepth 1 -maxdepth 1 -type d -name 'arcanum-*'
rg -n 'surface_kind: generated-native-runtime-package|runtime: github-copilot|canonical_source:|alias_of:' /tmp/arcanum-github-copilot-stage-20260531T234051Z/.github/skills
```

## Follow-Up

Run a decision gate or refine/invoke refresh for the GitHub/Copilot naming policy, then resume `TASK-SURFACE-003`.
