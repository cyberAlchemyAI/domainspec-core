# Invoke Design - Integration Architecture

Status: `pass`
Capability: `invoke`
Mode: `design`
Design name: `Studio Prototype Gate`

## Architecture Summary

UI Prototyping Studio should be integrated as an optional prototype gate inside
the DomainSpec UI pipeline. The gate begins only after feature UI artifacts
exist and ends before target-app source mutation begins.

```text
Feature docs
  -> UI-ARCHITECTURE.md / UI-SPEC.md / TEST-SPEC.md
  -> Studio Prototype Gate
       -> run-local Studio session
       -> register 1-3 HTML variants
       -> map data-od-id to UI concepts
       -> preview and annotate
       -> accept/revert visible prototype changes
       -> export handoff with explicit confirmation
  -> target app task-session
  -> target app Playwright/visual audit
```

## Boundary Model

| Edge | Consumed By | Produced By | Contract |
| --- | --- | --- | --- |
| UI pipeline -> Studio | Studio session | DomainSpec UI pipeline | Specs are read-only inputs. |
| Studio -> handoff | Studio export | Studio session | Export includes accepted prototype evidence and traceability. |
| Handoff -> target app | task-session | Studio export | Handoff is implementation context, not source mutation. |
| Target app -> UI pipeline | invoke refresh or task-session sync | target app validation | Only explicit sync changes canonical docs. |

## Studio Gate Inputs

| Input | BodyWar/TROQAR Example |
| --- | --- |
| UI contract | `projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md` |
| Test obligations | `projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md` |
| Visual guide | `projects/body-war/docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md` |
| App constraints | current static TypeScript Node app, no React/Vite requirement |
| Security constraints | safe Strava profile link, no token-like text, session cookie posture |

## Studio Gate Operations

| Operation | Command Shape | Evidence |
| --- | --- | --- |
| Open session | `pnpm studio session open` | session id, variant count |
| Submit objective | `pnpm studio prompt submit <sid> "<objective>"` | prompt state |
| Register variants | `pnpm studio variants register <sid> --from <dir>` | 1-3 HTML variants with `data-od-id` |
| Select baseline | `pnpm studio baseline select <sid> <label>` | baseline decision |
| Preview and annotate | `pnpm studio preview <sid>` | browser comments with `odId` |
| Synthesize/apply | `pnpm studio synthesize`, `pnpm studio apply`, `pnpm studio accept` | accepted revision or discard/revert |
| Export | `pnpm studio handoff export <sid> --confirm` | downstream handoff |

## `data-od-id` Mapping

The prototype should stamp stable IDs from the feature's UI concepts. Suggested
TROQAR examples:

| UI Concept | Suggested `data-od-id` |
| --- | --- |
| online runner shell | `troqar.shell` |
| connect CTA | `auth.connect.cta` |
| account actions | `topbar.account.actions` |
| safe athlete card | `profile.safe-athlete-card` |
| Strava profile link | `profile.strava-link` |
| recent activity summary | `activity.recent-summary` |
| evidence submit CTA | `evidence.submit.cta` |
| privacy/disconnect area | `privacy.session-controls` |

## Gate Criteria

| Gate | Pass Condition |
| --- | --- |
| Input readiness | UI-SPEC and TEST-SPEC exist and cite feature behavior. |
| Variant readiness | 1-3 self-contained HTML variants render in Studio preview. |
| Identity readiness | Annotatable components have stable `data-od-id`; fallback selectors are flagged. |
| Operator control | Accept/revert/discard decisions are visible and reversible until export. |
| Handoff readiness | Export cites source specs, accepted variant/revision, annotation summary, unresolved risks, and target-app next SWU. |
| Implementation readiness | Target app work-pack consumes the handoff but keeps Playwright validation on the real app. |

## BodyWar Placement

Add the prototype gate as a sibling after `SWU-TUI-001` and before or alongside
`SWU-TUI-002`:

- it can run before BodyWar Playwright is installed because Studio has its own
  preview and e2e;
- it should not mark BodyWar UI complete;
- BodyWar `SWU-TUI-003` should consume the handoff for static UI hardening;
- BodyWar `SWU-TUI-004` and `SWU-TUI-005` remain the real browser coverage and
  visual audit gates.

## Design Verdict

`pass`: the architecture preserves authority boundaries and gives the current
UI pipeline a concrete visual evidence phase without broad framework migration.

## Receipt

```json
{
  "stage": "06-integration-design",
  "status": "pass",
  "artifacts": [
    "stages/06-integration-design.md"
  ],
  "validation_result": "pass",
  "blockers": [],
  "residue": [
    "Future execution should decide exact handoff export destination and filename convention."
  ]
}
```
