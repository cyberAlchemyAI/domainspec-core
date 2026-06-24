# Refinement Run Manifest

## Identity

- Run ID: `2026-06-23-per-element-annotate`
- Target: `projects/ui-prototyping-studio` — annotate/preview surface (per-element Figma-like loop)
- Refine loop: canonical ten-stage loop (`.claude/skills/refine/SKILL.md`)
- Preset: `full`
- Research mode: `no-research` (local evidence decisive)
- Status: `flag` — run complete; MVP plan ready, honest-diff (S4) + untagged-apply deferred; 1 open operator scope decision

## Run Artifacts

- Evidence index: `evidence-index.json`
- Seed proposal: `REFINE-SEED-PROPOSAL.md`
- Dispatch route: `REFINE-DISPATCH.json` (dispatch validation: **pass**)
- Runtime handoff: `RUNTIME-HANDOFF.md`
- Result: `RESULT.md` (status: flag)
- Stage artifacts: `stages/`

## Stage Evidence

| Stage | Capability | Capability source | Mode/config | Status | Artifact path | Receipt kind | Verdict | Blocked reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Context Builder evidence baseline | context-builder | native capability | standard; --strict --emit both --handoff runtime | not_run | | blocked | not_run | awaiting confirmation |
| Invoke Define | invoke | native capability | define | not_run | | blocked | not_run | awaiting confirmation |
| Interrogation refine-review | interrogation | native capability | refine-review | not_run | | blocked | not_run | awaiting confirmation |
| Research decision | refine | refine SKILL.md | research-if-gap-appears | not_run | | blocked | not_run | awaiting confirmation |
| Distill | distill | native capability | standard | not_run | | blocked | not_run | awaiting confirmation |
| Invoke Redefine / Design | invoke | native capability | design | not_run | | blocked | not_run | awaiting confirmation + g05 forks |
| Interrogation refine-design-review | interrogation | native capability | refine-design-review | not_run | | blocked | not_run | awaiting confirmation |
| Distill Repair | distill | native capability | validate | not_run | | blocked | not_run | awaiting confirmation |
| Invoke Plan | invoke | native capability | plan | not_run | | blocked | not_run | awaiting confirmation |
| Final Interrogation and Synthesis | interrogation + refine | native capability + refine synthesis | refine-final | not_run | | blocked | not_run | awaiting confirmation |

## Subagent Strategy

- Status: `recommended` (operator permission required before spawn)
- Roles: `ergonomics-advocate`, `governance-integrity-skeptic`, `implementation-cost-realist`
- Anti-bias axis: `ergonomic-freedom <-> governed-integrity`, grounded by implementation-cost
- Parallelism: `fanout`; Join: `parent_synthesis`; Authorization: `pending`

## Notes

- This manifest references stage artifacts; it does not copy or redefine them.
- `REFINE-DISPATCH.json` is the route contract and validated **pass** before any native runtime-backed stage runs.
- A selected stage must have an artifact path or blocked reason; a `pass` stage must reference an existing artifact.
- Task Session and Sigil Development are not loop stages; they may appear only as recommended next routes in `RESULT.md`.
