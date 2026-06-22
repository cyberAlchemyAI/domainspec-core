# Context Builder Evidence Baseline

Status: `pass`
Capability: `context-builder`
Mode: `standard`
Strict coverage: `pass`
Handoff pack: `runtime`

## Task

Build a compact evidence baseline for refining how `projects/ui-prototyping-studio/`
integrates with the DomainSpec UI pipeline currently being used for BodyWar/TROQAR.

## Obligation Matrix

| ID | Obligation | Status | Evidence |
| --- | --- | --- | --- |
| O1 | Identify Studio's current operational spine. | covered | `README.md`, `SPEC.md`, `ARCHITECTURE.md`, `backend/src/cli/studio.ts` |
| O2 | Identify which Studio capabilities are real versus legacy or deferred. | covered | `README.md`, `SPEC.md`, `WORK-PACK.md`, `backend/e2e/` |
| O3 | Identify BodyWar UI pipeline artifacts that Studio would consume. | covered | BodyWar `UI-SPEC.md`, `TEST-SPEC.md`, `UX-PLAN.md`, `WORK-PACK.md` |
| O4 | Preserve owner boundaries among DomainSpec UI pipeline, Studio, and target app. | covered | Studio `ARCHITECTURE.md`; BodyWar invoke dispatch and work-pack |
| O5 | Produce a non-executed integration plan, not target app mutation. | covered | `REFINE-DISPATCH.json`, `RUNTIME-HANDOFF.md` |

## Selected Context

| Source | Selector | Why Included |
| --- | --- | --- |
| `projects/ui-prototyping-studio/README.md` | lines 3, 30-31, 44-67 | Establishes accountable variant loop, CLI workflow, preview, click-to-annotate, accept/revert, handoff export, and Playwright E2E. |
| `projects/ui-prototyping-studio/SPEC.md` | lines 30-48, 109-116, 292-295 | Defines CLI as current runtime, `data-od-id` as annotation identity, runnable verbs, and L0 acceptance contract. |
| `projects/ui-prototyping-studio/ARCHITECTURE.md` | lines 18-20, 53-58, 83-88, 137-144 | States Studio governs registered variants, while generation is external and durable export is explicitly gated. |
| `projects/ui-prototyping-studio/WORK-PACK.md` | lines 20-26, 85-88, 117-118 | Names the CLI loop, annotation overlay, handoff path, and wave/SWU framing. |
| `projects/ui-prototyping-studio/backend/src/cli/studio.ts` | lines 81-180, 180-351, 421-436 | Confirms concrete CLI commands for sessions, variants, comments, preview, browser accept/discard/revert, and confirmed handoff export. |
| `projects/ui-prototyping-studio/backend/e2e/` | file list | Shows existing Playwright e2e coverage for smoke, governance, human loop, blind naive user, preview accept, and auto cycle. |
| `projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md` | lines 30-39, 61-105, 156-164 | Provides the target presentation contract for anonymous, connected, profile, activity, and safe Strava link states. |
| `projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md` | lines 16-46, 57-60 | Provides browser E2E obligations and records that Playwright is scaffolded but not wired yet. |
| `projects/body-war/development/invoke-runs/20260621T160132Z-troqar-frontend-ui-ux-plan/WORK-PACK.md` | lines 40-44, 63-100 | Establishes SWU order: artifact baseline, Playwright runtime, static UI hardening, browser coverage, visual audit. |
| `projects/body-war/development/task-sessions/20260621T172253Z-swu-tui-001-generated-ui-baseline/CONTEXT-PACK.md` | lines 10-23, 53 | Confirms current BodyWar UI artifacts exist and Playwright runtime remains intentionally excluded. |

## Evidence Interpretation

The studio is not a UI framework and should not replace DomainSpec UI pipeline
authoring. Its live value is a governed prototype session: take an already
authored UI contract, create or register a small set of HTML candidates, stamp
stable `data-od-id` targets, preview and annotate in a browser, accept/revert
only visible changes, then export a handoff.

BodyWar currently has the exact upstream inputs that make that valuable:
`UI-SPEC.md`, `TEST-SPEC.md`, a Playwright scaffold, and a work-pack that still
needs browser runtime wiring plus static UI hardening.

## Excluded Candidates

| Source | Reason Excluded |
| --- | --- |
| `projects/ui-prototyping-studio/provenance/legacy-domainspec-spec/` | Useful as historical residue, but not the current lean Studio spine. |
| External UI prototyping research | Not needed for this integration design; local evidence already resolves the owner boundary. |
| Direct edits to BodyWar app code | Outside refine scope; implementation belongs to a future task-session. |

## Gaps And Resolutions

| Gap | Resolution |
| --- | --- |
| Whether Studio should run before BodyWar Playwright is wired. | Yes, as a prototype session, because Studio has its own preview and Playwright e2e. BodyWar Playwright remains required for target-app validation later. |
| Whether Studio should mutate BodyWar source. | No. Studio produces handoff evidence only; BodyWar implementation remains a task-session. |
| Whether accepted Studio output promotes canonical specs. | No. Any spec update must route through invoke refresh or a bounded task-session. |

## Receipt

```json
{
  "stage": "01-context-builder",
  "status": "pass",
  "artifacts": [
    "stages/01-context-builder.md",
    "stages/01-context-builder.index.json"
  ],
  "validation_result": "pass",
  "blockers": [],
  "residue": [
    "Full integration execution is deferred to task-session."
  ]
}
```
