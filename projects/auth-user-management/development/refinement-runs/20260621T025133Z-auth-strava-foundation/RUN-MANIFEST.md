# Run Manifest - 20260621T025133Z-auth-strava-foundation

- Run id: `20260621T025133Z-auth-strava-foundation`
- Dispatch id: `refine-20260621-auth-strava-foundation`
- Target: `projects/auth-user-management`
- Owner: `refine`
- Preset: `standard`
- Research mode: `research-if-gap-appears`
- Phase: `complete`
- Status: `pass`
- Dispatch validation: `pass`
- Subagent authorization: `approved by operator`
- Subagent lifecycle: `pass`

## Artifacts

| Artifact | Path | State |
|---|---|---|
| Seed proposal | `REFINE-SEED-PROPOSAL.md` | written |
| Dispatch route | `REFINE-DISPATCH.json` | validated `pass` |
| Runtime handoff | `RUNTIME-HANDOFF.md` | complete |
| Context baseline | `stages/01-context-builder/context-pack.md` | pass |
| Define | `stages/02-invoke-define/DEFINE.md` | pass |
| Review | `stages/03-interrogation-review/REVIEW.md` | pass |
| Research decision | `stages/04-research-decision/RESEARCH-DECISION.md` | pass |
| Distill | `stages/05-distill/DISTILL.md` | pass |
| Design | `stages/06-invoke-design/DESIGN.md` | pass |
| Subagent receipts | `stages/06-invoke-design/subagent-receipts.md` | pass lifecycle, flag content residue |
| Design review | `stages/07-interrogation-design-review/DESIGN-REVIEW.md` | pass |
| Repair | `stages/08-distill-repair/REPAIR.md` | pass |
| Plan | `stages/09-invoke-plan/PLAN.md` | pass |
| Final review | `stages/10-final/FINAL-REVIEW.md` | pass |
| Result | `RESULT.md` | final |
| Evidence index | `evidence-index.json` | final |

## Stage Ledger

| # | Stage | Capability | Status | Receipt |
|---|---|---|---|
| 1 | Context Builder evidence baseline | context-builder | pass | `stages/01-context-builder/context-pack.md` |
| 2 | Invoke Define | invoke | pass | `stages/02-invoke-define/DEFINE.md` |
| 3 | Interrogation refine-review | interrogation | pass | `stages/03-interrogation-review/REVIEW.md` |
| 4 | Research decision | refine | pass | `stages/04-research-decision/RESEARCH-DECISION.md` |
| 5 | Distill | distill | pass | `stages/05-distill/DISTILL.md` |
| 6 | Invoke Redefine / Design | invoke | pass | `stages/06-invoke-design/DESIGN.md` plus subagent receipts |
| 7 | Interrogation refine-design-review | interrogation | pass | `stages/07-interrogation-design-review/DESIGN-REVIEW.md` |
| 8 | Distill Repair | distill | pass | `stages/08-distill-repair/REPAIR.md` |
| 9 | Invoke Plan | invoke | pass | `stages/09-invoke-plan/PLAN.md` |
| 10 | Final Interrogation and Synthesis | interrogation -> refine | pass | `stages/10-final/FINAL-REVIEW.md`, `RESULT.md` |

## Delegated Lanes

| Role | Agent id | Join | Content verdict | Receipt |
|---|---|---|---|---|
| auth-domain-porter | `019ee81e-8c50-70f1-89ab-ebfbe83e3969` | completed, closed | flag | `stages/06-invoke-design/subagent-receipts.md` |
| browser-session-security | `019ee81e-8ce7-7980-a8ba-ae5b851dbce8` | completed, closed | flag | `stages/06-invoke-design/subagent-receipts.md` |
| strava-provider-integration | `019ee81e-8e04-74b2-a1f8-63c2f6183f63` | completed, closed | flag | `stages/06-invoke-design/subagent-receipts.md` |

The lane verdicts are `flag` because implementation remains pending and each
lane found anti-patterns or follow-up constraints. The lifecycle verdict is
`pass` because all lanes joined and closed with usable receipts.

## Decisions Closed By Parent Synthesis

- `DEC-AUTH-TRANSPORT-001`: selected
  `hybrid-cookie-for-browser-bearer-for-service-api`.
- `DEC-AUTH-STRAVA-SCOPE-001`: selected
  `link-identity-and-import-recent-activity-summaries`, with
  `read,activity:read` by default and `activity:read_all` only as explicit
  consenting-athlete escalation.

## Source Evidence

- `validation/poker-team/docs/features/auth-access-control/SPEC.md`
- `validation/poker-team/docs/features/auth-access-control/TEST-SPEC.md`
- `validation/poker-team/backend/src/use-cases/auth-access-control/authenticate-request.ts`
- `validation/poker-team/backend/src/use-cases/auth-access-control/authorize-request.ts`
- `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/lib/auth/savvy-auth.ts`
- `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/tests/auth/savvy-auth.test.ts`
- `projects/body-war/.craft/ledger.yml`
- `projects/body-war/docs/features/strava-linked-pilot/WORK-PACK.md`
- Official Strava docs for OAuth scope currentness.

## Final Next Route

Run `task-session` for `SWU-AUTH-001`: reusable auth core domain and ports.
