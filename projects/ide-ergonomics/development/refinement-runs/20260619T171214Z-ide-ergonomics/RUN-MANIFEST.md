# Run Manifest: IDE Ergonomics Refine

Status: strategy-proposal
Run ID: 20260619T171214Z-ide-ergonomics
Dispatch ID: refine-20260619T171214Z-ide-ergonomics
Target: `projects/ide-ergonomics`
Preset: standard
Research: no-research

## Required Artifacts

| Artifact | Status | Notes |
| --- | --- | --- |
| `RUN-MANIFEST.md` | pass | This manifest. |
| `evidence-index.json` | pass | Project-local source evidence index. |
| `REFINE-SEED-PROPOSAL.md` | pass | Seed proposal and route framing. |
| `REFINE-DISPATCH.json` | pass | Validator-passing route strategy. |
| `RUNTIME-HANDOFF.md` | pass | Records deferred runtime and subagent permission state. |
| `RESULT.md` | pass | Initial synthesis from repo inspection. |
| `stages/` | pass | Contains a not-run marker; runtime-backed stage artifacts are deferred. |

## Stage Evidence

| Stage | Capability | Artifact | Status | Verdict |
| --- | --- | --- | --- | --- |
| Context Builder evidence baseline | `context-builder` | future `stages/01-context-builder/` | not-run | deferred until confirmation |
| Invoke Define | `invoke` | future `stages/02-invoke-define.md` | not-run | deferred until confirmation |
| Interrogation refine-review | `interrogation` | future `stages/03-refine-review.md` | not-run | deferred until confirmation |
| Research decision | `refine` | `REFINE-SEED-PROPOSAL.md` | pass | local-only, no web |
| Distill | `distill` | future `stages/05-distill.md` | not-run | deferred until confirmation |
| Invoke Redefine / Design | `invoke` | future `stages/06-invoke-design.md` | not-run | deferred until confirmation |
| Interrogation refine-design-review | `interrogation` | future `stages/07-refine-design-review.md` | not-run | deferred until confirmation |
| Distill Repair | `distill` | future `stages/08-distill-repair.md` | not-run | deferred until confirmation |
| Invoke Plan | `invoke` | future `stages/09-invoke-plan.md` | not-run | deferred until confirmation |
| Final Interrogation and Synthesis | `interrogation` plus parent `refine` | `RESULT.md` | proposal-only | no runtime-backed final interrogation run |

## Subagent Lifecycle

Subagent strategy: recommended, requires user permission, not executed.

| Role | Spawn | Join | Close | Receipt |
| --- | --- | --- | --- | --- |
| `action-card-workflow-mapper` | not-run | not-run | not-run | none |
| `host-surface-constraints-reviewer` | not-run | not-run | not-run | none |
| `governance-boundary-guardian` | not-run | not-run | not-run | none |

## Dispatch Strategy

Selected overlays:

- `baseline_sequence`
- `route_menu_for_ide_action_surface`
- `memory_loop_for_conversation_actions`
- `spell_candidate_for_repeated_composition`
- `subagent_preview_without_runtime_spawn`

Selected route: discipline plus spell candidate, host implementation deferred.

## Validation Log

- Dispatch validation: pass with `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py projects/ide-ergonomics/development/refinement-runs/20260619T171214Z-ide-ergonomics/REFINE-DISPATCH.json`.
- JSON validation: pass for `REFINE-DISPATCH.json` and `evidence-index.json`.
- Markdown link validation: pass with `bash tools/check_markdown_links.sh projects/ide-ergonomics/README.md`.
- Public/private boundary: project is private parent repo; no public Arcanum mutation in this pass.

## Mutation Boundary

Files are intentionally limited to `projects/ide-ergonomics/`.
