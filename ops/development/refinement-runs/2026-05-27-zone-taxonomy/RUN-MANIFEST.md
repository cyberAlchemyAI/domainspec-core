# Run Manifest: 2026-05-27-zone-taxonomy

Target: repository zone taxonomy and best repository shape
Preset: standard
Research mode: research-if-gap-appears
Overall status: FLAG

## Stage Evidence

| Stage | Owner | Command | Mode | Artifact | Status | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Context Builder evidence baseline | context-builder | `context-builder` | standard | `stages/01-context-builder.md` | pass | dry-run evidence |
| 2. Invoke Define | invoke | `invoke` | define | `stages/02-invoke-define.md` | pass | dry-run evidence |
| 3. Interrogation refine-review | interrogation | `interrogation` | refine-review | `stages/03-interrogation-refine-review.md` | pass | dry-run evidence |
| 4. Research decision | refine | n/a | research-if-gap-appears | `stages/04-research-decision.md` | pass | no external research |
| 5. Distill | distill | `distill` | standard | `stages/05-distill.md` | pass | dry-run evidence |
| 6. Invoke Redefine / Design | invoke | `invoke` | design | `stages/06-invoke-design.md` | pass | dry-run evidence |
| 7. Interrogation refine-design-review | interrogation | `interrogation` | refine-design-review | `stages/07-interrogation-design-review.md` | pass | dry-run evidence |
| 8. Distill Repair | distill | `distill` | validate | `stages/08-distill-repair.md` | pass | dry-run evidence |
| 9. Invoke Plan | invoke | `invoke` | plan | `stages/09-invoke-plan.md` | pass | dry-run evidence |
| 10. Final Interrogation and Synthesis | interrogation + refine | `interrogation` | refine-final | `stages/10-final-interrogation.md`, `RESULT.md` | flag | synthesis complete; stage execution was dry-run |

## Command Resolution

Resolved:

- `context-builder`: `arcanum/.codex/commands/context-builder.md`
- `invoke`: `arcanum/.codex/commands/invoke.md`
- `interrogation`: `arcanum/.codex/commands/interrogation.md`
- `distill`: `arcanum/.codex/commands/distill.md`
- `codex-goal-profile`: `arcanum/.codex/commands/codex-goal-profile.md`

## Blocking Or Flagged Conditions

- Model-backed stage execution was not performed; dry-run adapter evidence was used.
- Working tree contains modified `arcanum` and nested modified `implementation/domainspec`.
- `projects/body-war/` is untracked.
- `git submodule status` reports no submodule mapping for `research/projects/hermes-agent/repo`.

## Outputs

- `REFINE-SEED-PROPOSAL.md`
- `GOAL-HANDOFF.md`
- `RESULT.md`
- `DELETION-CANDIDATE-PASS.md`
- `RUNTIME-SURFACE-INVOKE.md`
- `SYMLINK-STRATEGY-REFINE.md`
- `evidence-index.json`
- `stages/`

## Post-Result Correction

After user clarification, `sigils-library/` was reclassified from `capability-library` to `superseded-name` because it was the first name of Arcanum. The final result now treats it as a deletion candidate after preservation review.

## Runtime Surface Addition

After the user identified that Arcanum exists across multiple repository/runtime surfaces, a companion invoke design+plan artifact was added. The final result now includes a `runtime-surface` policy layer that separates canonical source, installed runtime surface, generated runtime state, and local/private runtime state.

## Symlink Strategy Addition

After the user asked whether the cleanest surface should avoid copies through symbolic links, a refine-owned strategy artifact was added. It recommends symlinks for repo-local discovery facades and managed snapshots for global/cross-runtime surfaces.
