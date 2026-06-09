# Arcanum Runtime Surface Refresh Report

Date: 2026-05-29
Mode: invoke refresh
Phase status: no-op
Mutation mode: proposal-only

## Target Artifacts

- `ops/ARCANUM-RUNTIME-SURFACE-INVOKE-DESIGN-PLAN.md`
- `ops/CODEX-SKILL-SURFACE-POLICY.md`
- `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md`

## Source Signals

| Signal | Type | Target artifacts | Claim | Evidence | Confidence | Mutation safety |
| --- | --- | --- | --- | --- | --- | --- |
| `SIG-RUNTIME-001` | `blocker_resolved` | `ops/ARCANUM-RUNTIME-SURFACE-INVOKE-DESIGN-PLAN.md`, `ops/CODEX-SKILL-SURFACE-POLICY.md` | Runtime packages should be generated native snapshots from canonical source, not cross-runtime pointers. | User refinement: copying the skill into each runtime expected pattern gives Codex, Claude, and Copilot native use while avoiding canonical drift. | high | safe |
| `SIG-RUNTIME-002` | `status_changed` | `ops/ARCANUM-RUNTIME-SURFACE-INVOKE-DESIGN-PLAN.md` | Root `.github/skills` is no longer a conceptual blocker when treated as generated GitHub/Copilot-native adapter output with provenance. | Plan now records generated native package approach and keeps root `.github/skills` when provenance exists. | high | safe |
| `SIG-RUNTIME-003` | `artifact_drift` | `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md` | Existing classification still says `distribution-adapter`, but does not yet record generated provenance or alias status. | Classification predates the generated-native-package decision. | medium | needs_review |
| `SIG-RUNTIME-004` | `route_changed` | `ops/ARCANUM-RUNTIME-SURFACE-INVOKE-DESIGN-PLAN.md` | Runtime adapter work should target concrete native adapters: `codex-skill`, `claude-skill`, `copilot-instructions`, with `native-skill` only as an abstract selector. | Plan now names concrete runtime-native adapters. | high | safe |

## Delta Summary

| Delta class | Count | Summary |
| --- | ---: | --- |
| `blocker_resolved` | 1 | The root `.github/skills` conceptual role is resolved as generated GitHub/Copilot-native package surface when provenance exists. |
| `status_changed` | 1 | The runtime-surface plan now treats copied runtime packages as valid generated install artifacts, not independent canonical sources. |
| `artifact_drift` | 1 | `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md` needs a future provenance refresh to distinguish generated-native adapters, aliases, root-owned packages, and stale duplicates. |
| `route_changed` | 1 | Adapter implementation should prefer concrete runtime-native adapter IDs over vague local/native naming. |
| `no_op` | 1 | No additional mutation is required in the main plan or Codex policy after the latest decision; the evidence is already represented. |

## Proposed Changes

No new patch is proposed for the main design/plan or Codex policy. The latest decision is already represented.

Future targeted refresh proposal:

- Update `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md` with generated provenance fields:
  - `runtime`
  - `canonical_source`
  - `generated_by`
  - `alias_of`
  - `mutation_policy`
  - `owner`
  - `action`

This should happen inside `TASK-RUNTIME-007` or a narrow task-session focused on root GitHub skill provenance.

## Applied Changes

None in this refresh pass.

The relevant artifact state already exists in:

- `ops/ARCANUM-RUNTIME-SURFACE-INVOKE-DESIGN-PLAN.md`
- `ops/CODEX-SKILL-SURFACE-POLICY.md`

## Skipped Changes

- Did not edit `.github/skills/*`; owner/runtime provenance must be recorded before deletion or regeneration.
- Did not edit `implementation/domainspec/.agents/skills/*`; DomainSpec-owned.
- Did not edit `tools/arcanum`; implementation belongs to the next task-session.
- Did not mutate machine-global Codex home.

## Validation

Review checks performed:

- Confirmed the plan contains `Runtime Distribution Approach`.
- Confirmed the plan records generated native packages, runtime-native adapters, alias handling, and provenance gate `G-RUNTIME-007`.
- Confirmed the Codex policy distinguishes canonical source, generated native packages, and aliases.

No shell validation was required because this refresh did not mutate executable files.

## Remaining Gaps

Invoke gaps:

- None blocking for the refresh itself.

Target artifact gaps:

- `ops/ROOT-GITHUB-SKILLS-CLASSIFICATION.md` still needs provenance/alias enrichment.
- DomainSpec-owned duplicate cleanup remains gated.
- `tools/arcanum` and installer profiles still need implementation.
- `.arcanum` state still needs path classification.

## Next Route

`task-session`

Recommended first SWU:

```text
TASK-RUNTIME-001 / SWU-RUNTIME-001
```

Then:

```text
TASK-RUNTIME-002 / SWU-RUNTIME-002
```

After those inventories are real, run `TASK-RUNTIME-003` and `TASK-RUNTIME-004` to implement runtime-native adapters and install profiles.
