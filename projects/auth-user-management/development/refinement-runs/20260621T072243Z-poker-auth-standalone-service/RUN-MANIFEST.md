# Run Manifest

## Run

- Run id: `20260621T072243Z-poker-auth-standalone-service`
- Dispatch id: `refine-20260621T072243Z-poker-auth-standalone-service`
- Target: `projects/auth-user-management`
- Source: `validation/poker-team/backend/src/domain/auth-access-control`
- Source docs: `validation/poker-team/docs/features/auth-access-control`
- Status: `pass`
- Preset: `standard`
- Research: `no-research`

## Required Artifacts

| Artifact | Status |
| --- | --- |
| `REFINE-SEED-PROPOSAL.md` | pass |
| `REFINE-DISPATCH.json` | pass |
| `RUNTIME-HANDOFF.md` | pass |
| `evidence-index.json` | pass |
| `RESULT.md` | pass |
| `stages/` | created |

Dispatch validation:

```text
VALIDATION=pass
```

## Stage Receipts

| Stage | Capability | Status | Artifact Or Blocked Reason |
| --- | --- | --- | --- |
| Context Builder evidence baseline | `context-builder` | pass | `stages/01-context-builder/CONTEXT-PACK.md` |
| Invoke Define | `invoke` | pass | `stages/02-invoke-define/DEFINE.md` |
| Interrogation refine-review | `interrogation` | pass | `stages/03-interrogation-review/REVIEW.md` |
| Research decision | `refine` | pass | `stages/04-research-decision/DECISION.md` |
| Distill | `distill` | pass | `stages/05-distill/COPY-UNIT.md` |
| Invoke Redefine / Design | `invoke` | pass | `stages/06-invoke-design/DESIGN.md` |
| Interrogation refine-design-review | `interrogation` | pass | `stages/07-interrogation-design-review/REVIEW.md` |
| Distill Repair | `distill` | pass | `stages/08-distill-repair/REPAIR.md` |
| Invoke Plan | `invoke` | pass | `stages/09-invoke-plan/WORK-PACK.md` |
| Final Interrogation and Synthesis | `refine` | pass | `stages/10-final-synthesis/SYNTHESIS.md` |

## Current Evidence Snapshot

- Poker Team domain auth files exist under
  `validation/poker-team/backend/src/domain/auth-access-control/`.
- Poker Team application use cases exist under
  `validation/poker-team/backend/src/use-cases/auth-access-control/`.
- Poker Team Drizzle auth repository exists at
  `validation/poker-team/backend/src/infrastructure/repositories/drizzle-auth.repository.ts`.
- Poker Team Drizzle auth tables exist in
  `validation/poker-team/backend/src/infrastructure/database/schema.ts`.
- Poker Team auth-access-control docs exist under
  `validation/poker-team/docs/features/auth-access-control/`.
- Linked auth documentation and operations evidence exists in
  `validation/poker-team/docs/index/feature-map.md`,
  `validation/poker-team/docs/slos.md`, and
  `validation/poker-team/infra/alerts/auth-access-control.rules.yml`.
- The current target package is untracked and must be treated as replaceable
  work-in-progress until the copy route is confirmed.

## Refresh Receipts

| Refresh | Capability | Status | Artifact |
| --- | --- | --- | --- |
| Docs extraction refresh | `invoke refresh` | pass | `refreshes/20260621T073454Z-docs-extraction/REFRESH-REPORT.md` |

## Implementation Receipts

| Receipt | Capability | Status | Artifact |
| --- | --- | --- | --- |
| Full auth work-pack one-shot | `codex goal` | pass | `IMPLEMENTATION-RESULT.md` |
