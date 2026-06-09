# Task Session Resume: Root GitHub/Copilot Arcanum Package Regeneration

Date: 2026-06-01
Task: `TASK-SURFACE-003`
SWU: `SWU-SURFACE-004`, `SWU-SURFACE-005`
Result: PASS

## Objective

Resume root GitHub/Copilot Arcanum package regeneration after the naming blocker was resolved by `docs/decisions/github-copilot-arcanum-naming-policy.md`.

## Decision Applied

Selected naming policy: preserve current GitHub/Copilot root discovery names.

The GitHub/Copilot profile now generates:

- `arcanum-sigil-*` packages for sigils and transmutations,
- `arcanum-spell-*` packages for spells,
- `arcanum-orchestrate`,
- selected compatibility aliases such as `arcanum-sigil-interrogation`, `arcanum-necronomicon`, `arcanum-necronomicon-session`, and `arcanum-spell-necronomicon-session`.

## Work Performed

Updated `arcanum/tools/bootstrap_arcanum.sh`:

- added `write_copilot_skill_packages`,
- switched `write_copilot_surface` from the generic flattened package writer to the GitHub/Copilot-specific writer,
- set generated Copilot package provenance runtime to `github-copilot`,
- kept personal Codex and Claude package generation behavior unchanged.

Generated staging output:

```bash
arcanum/tools/bootstrap_arcanum.sh \
  --target /tmp/arcanum-github-copilot-stage-20260601 \
  --profile github-copilot \
  --sigils all \
  --spells all \
  --force
```

Promotion:

- current root Arcanum GitHub/Copilot packages before promotion: 33,
- staged packages included all 33 current root names,
- staged packages also included 13 extra Arcanum packages, left staged only,
- replaced only the 33 existing root `.github/skills/arcanum-*` packages,
- temporary backup written to `/tmp/arcanum-root-github-skills-backup-20260601T000000Z`.

## Validation

Commands/checks:

```bash
bash -n arcanum/tools/bootstrap_arcanum.sh
comm -23 /tmp/root-arcanum-github-current.txt /tmp/staged-arcanum-github-copilot.txt
find .github/skills -maxdepth 1 -type d -name 'arcanum-*' -printf '%f\n' | sort | diff -u /tmp/root-arcanum-github-current.txt -
while read -r pkg; do rg -q "\\.arcanum/runtimes/github-copilot" ".github/skills/$pkg/SKILL.md" && echo "$pkg"; done < /tmp/root-arcanum-github-current.txt
while read -r pkg; do rg -q "surface_kind: generated-native-runtime-package" ".github/skills/$pkg/SKILL.md" || echo "$pkg"; done < /tmp/root-arcanum-github-current.txt
```

Validation result:

- syntax check passed,
- no current root Arcanum package was missing from staging,
- root Arcanum package count did not drift,
- all 33 active root Arcanum `SKILL.md` files have generated-native provenance,
- no active root Arcanum `SKILL.md` file references `.arcanum/runtimes/github-copilot`.

## Follow-Up

`TASK-SURFACE-004` is now unblocked. The accepted route is to treat `.arcanum/runtimes/github-copilot` as an untracked regenerate-on-demand cache after confirming no active runtime instructions still depend on it.
