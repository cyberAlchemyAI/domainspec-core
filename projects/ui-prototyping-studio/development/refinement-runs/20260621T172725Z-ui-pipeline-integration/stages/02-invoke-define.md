# Invoke Define - Studio Prototype Gate

Status: `pass`
Capability: `invoke`
Mode: `define`
Target artifact: `ui-prototyping-studio-to-domain-spec-ui-pipeline integration`

## Definition

The integration is a **Studio Prototype Gate**: an optional, governed phase
between DomainSpec UI artifacts and target-app implementation.

```text
DomainSpec feature docs
  -> UI-ARCHITECTURE.md
  -> UI-SPEC.md
  -> TEST-SPEC.md
  -> Studio Prototype Gate
  -> target-app task-session
  -> Playwright and visual audit
```

## Purpose

The gate gives the team a browser-visible, reversible, evidence-producing UI
exploration loop before changing the production app. It lets the operator see
1-3 candidate directions, annotate concrete UI components, accept/revert
prototype changes, and export a handoff that implementation can consume.

## Inputs

| Input | Owner | Required |
| --- | --- | --- |
| `UI-SPEC.md` | DomainSpec UI pipeline / feature docs | yes |
| `TEST-SPEC.md` | DomainSpec UI pipeline / feature docs | yes |
| `VISUAL-DEFINITIONS.md` or visual guide | feature docs | recommended |
| Target app constraints | target app owner | yes |
| Existing generated UI scaffold/test status | target app owner | yes |

## Outputs

| Output | Owner | Notes |
| --- | --- | --- |
| Studio session record | UI Prototyping Studio | File-backed session under `STUDIO_DATA` run directory. |
| Registered variant HTML | UI Prototyping Studio | Self-contained HTML, 1-3 variants, stamped with `data-od-id`. |
| Annotation/comment events | UI Prototyping Studio | Captures stable component IDs and selector fallback. |
| Accepted prototype revision | UI Prototyping Studio | Reversible until handoff. |
| Handoff export | UI Prototyping Studio | Irreversible downstream edge; requires explicit confirmation. |
| Implementation context | target app task-session | Consumes handoff evidence; owns real source edits. |

## Owner Boundaries

| Boundary | Rule |
| --- | --- |
| DomainSpec UI pipeline -> Studio | Studio consumes UI specs and tests; it does not replace or promote them. |
| Studio -> target app | Studio exports prototype evidence; it does not mutate target app source. |
| Target app -> UI specs | If implementation discovers spec drift, route through invoke refresh or a bounded sync task. |
| Browser tests | Studio Playwright validates Studio flow; target app Playwright validates final app behavior. |

## Non-Goals

- No React/Vite migration requirement.
- No direct BodyWar app mutation.
- No real Strava secrets, private athlete data, or deployed production traffic in prototype runs.
- No automatic promotion of accepted prototype output into canonical specs.
- No replacement of BodyWar `SWU-TUI-*` work-pack; the gate composes with it.

## Definition Verdict

`pass`: the integration is coherent when scoped as a prototype evidence gate.
It becomes unsafe only if it is promoted into a hidden target-app mutator or a
spec-authority replacement.

## Receipt

```json
{
  "stage": "02-invoke-define",
  "status": "pass",
  "artifacts": [
    "stages/02-invoke-define.md"
  ],
  "validation_result": "pass",
  "blockers": [],
  "residue": [
    "Future execution should decide whether to add a reusable integration template under Studio docs or under DomainSpec UI pipeline docs."
  ]
}
```
