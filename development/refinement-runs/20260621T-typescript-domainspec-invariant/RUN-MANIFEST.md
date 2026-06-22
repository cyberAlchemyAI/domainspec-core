# Run Manifest

Run ID: `20260621T-typescript-domainspec-invariant`
Target: `domainspec-core` project implementation invariant and auth/user-management correction
Status: `pass`
Preset: `standard`
Research: `no-research`

## Required Artifacts

| Artifact | Owner | Status |
| --- | --- | --- |
| `RUN-MANIFEST.md` | refine | present |
| `evidence-index.json` | refine | present |
| `REFINE-SEED-PROPOSAL.md` | refine | present |
| `REFINE-DISPATCH.json` | refine / dispatch-spec | validated-pass |
| `RUNTIME-HANDOFF.md` | refine | awaiting confirmation |
| `RESULT.md` | refine | pass |
| `IMPLEMENTATION-LAYERING.md` | invoke | present |
| `WORK-PACK.md` | invoke | present |
| `EXECUTION-PACK.md` | invoke | present |
| `work-pack/` | invoke | present |
| `stages/` | stage owners | complete |

## Stage Evidence

| Step | Stage | Owner | Status | Artifact |
| --- | --- | --- | --- | --- |
| 1 | Context Builder evidence baseline | context-builder | pass | `stages/S01-CONTEXT-BUILDER.md` |
| 2 | Invoke Define | invoke | pass | `stages/S02-INVOKE-DEFINE.md` |
| 3 | Interrogation refine-review | interrogation | pass | `stages/S03-INTERROGATION-REFINE-REVIEW.md` |
| 4 | Research decision | refine | pass | `stages/S04-RESEARCH-DECISION.md` |
| 5 | Distill correction unit | distill | pass | `stages/S05-DISTILL-CORRECTION-UNIT.md` |
| 6 | Invoke Redefine / Design | invoke | pass | `stages/S06-INVOKE-DESIGN.md` |
| 7 | Interrogation refine-design-review | interrogation | pass | `stages/S07-INTERROGATION-DESIGN-REVIEW.md` |
| 8 | Distill Repair | distill | pass | `stages/S08-DISTILL-REPAIR.md` |
| 9 | Invoke Plan | invoke | pass | `stages/S09-INVOKE-PLAN.md` |
| 10 | Final Interrogation and Synthesis | interrogation + refine | pass | `stages/S10-FINAL-INTERROGATION-SYNTHESIS.md` |

## Current Evidence Notes

- DomainSpec architecture establishes Functional TypeScript as the implementation baseline.
- Shell scripts remain preferred for deterministic validation, bootstrap, orchestration, and simple repo checks.
- The previous Python auth implementation is now classified as superseded drift.
- Existing unrelated Python projects are legacy surfaces, not proof that new auth/runtime implementation should use Python.
- Dispatch Spec validation passed for `REFINE-DISPATCH.json`.
- The selected next execution route is `task-session` on `SWU-AUTH-001`.

## Next Route

Run `task-session` on `SWU-AUTH-001 - TypeScript Auth Package Baseline`.
