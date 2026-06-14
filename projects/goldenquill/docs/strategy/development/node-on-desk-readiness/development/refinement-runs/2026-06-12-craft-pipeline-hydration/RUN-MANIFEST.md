    # Refinement Run Manifest - Golden Quill node-on-desk readiness

    ## Identity

    - Run ID: `2026-06-12-craft-pipeline-hydration`
    - Target: `node-on-desk-readiness`
    - Refine loop: `.agents/skills/refine/SKILL.md`
    - Preset: `standard`
    - Research mode: `research-if-gap-appears`
    - Status: `flag`

    ## Run Artifacts

    - Evidence index: `evidence-index.json`
    - Seed proposal: `REFINE-SEED-PROPOSAL.md`
    - Dispatch route: `REFINE-DISPATCH.json`
    - Runtime handoff: `RUNTIME-HANDOFF.md`
    - Result: `RESULT.md`
    - Invoke first artifacts direction: `INVOKE-FIRST-ARTIFACTS.md`
- Research strategy: `RESEARCH-STRATEGY.md`
- Research dispatch: `RESEARCH-DISPATCH.json`
    - Stage artifacts: `stages/`

    ## Stage Evidence

    | Step | Stage | Capability | Mode/config | Status | Artifact path | Blocked reason |
    | --- | --- | --- | --- | --- | --- | --- |
    | `s01-context-builder` | Context Builder evidence baseline | `context-builder` | `standard; --strict --emit both --handoff runtime` | `not_run` | `stages/01-context-builder.md` | Permission gate pending; stage not executed. |
| `s02-invoke-define` | Invoke Define | `invoke` | `define` | `not_run` | `stages/02-invoke-define.md` | Permission gate pending; stage not executed. |
| `s03-interrogation-review` | Interrogation refine-review | `interrogation` | `refine-review` | `not_run` | `stages/03-interrogation-refine-review.md` | Permission gate pending; stage not executed. |
| `s04-research-decision` | Research decision | `refine` | `research-if-gap-appears` | `not_run` | `stages/04-research-decision.md` | Permission gate pending; stage not executed. |
| `s05-distill` | Distill | `distill` | `standard` | `not_run` | `stages/05-distill.md` | Permission gate pending; stage not executed. |
| `s06-invoke-design` | Invoke Redefine / Design | `invoke` | `design` | `not_run` | `stages/06-invoke-design.md` | Permission gate pending; stage not executed. |
| `s07-interrogation-design-review` | Interrogation refine-design-review | `interrogation` | `refine-design-review` | `not_run` | `stages/07-interrogation-refine-design-review.md` | Permission gate pending; stage not executed. |
| `s08-distill-repair` | Distill Repair | `distill` | `validate` | `not_run` | `stages/08-distill-repair.md` | Permission gate pending; stage not executed. |
| `s09-invoke-plan` | Invoke Plan | `invoke` | `plan` | `not_run` | `stages/09-invoke-plan.md` | Permission gate pending; stage not executed. |
| `s10-final-synthesis` | Final Interrogation and Synthesis | `interrogation + refine` | `refine-final` | `not_run` | `stages/10-final-interrogation-and-synthesis.md` | Permission gate pending; stage not executed. |

    ## Notes

    - This manifest references planned stage artifacts; it does not claim they exist yet.
    - `REFINE-DISPATCH.json` is the route contract and must validate before runtime-backed stages run.
    - Task Session and Sigil Development are not loop stages; they may appear only as recommended next routes after final synthesis.

## Research Strategy Evidence

- Strategy artifact: `RESEARCH-STRATEGY.md`
- Dispatch route: `RESEARCH-DISPATCH.json`
- Execution status: `not_run`; external research and subagents require Josh confirmation.
