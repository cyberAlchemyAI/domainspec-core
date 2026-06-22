# Invoke Plan - Studio Prototype Gate Integration

Status: `pass`
Capability: `invoke`
Mode: `plan`
Plan status: `non-executed`

## Objective

Add UI Prototyping Studio as an optional prototype gate for DomainSpec UI
pipeline features, with BodyWar/TROQAR as the first proof.

## Work-Pack Shape

| SWU | Name | Owner | Write Scope | Validation |
| --- | --- | --- | --- | --- |
| `UPS-GATE-001` | Integration Contract Doc | UI Prototyping Studio | `projects/ui-prototyping-studio/docs/` or `development/` | markdown review, `git diff --check` |
| `UPS-GATE-002` | Handoff Export Convention | UI Prototyping Studio | Studio docs/templates plus no source mutation unless needed | export fixture review, Studio e2e if code changes |
| `BW-TUI-PROT-001` | TROQAR Studio Prototype Session | UI Prototyping Studio run evidence | isolated `STUDIO_DATA`, generated variant folder, handoff export | Studio `pnpm test:e2e` or targeted preview smoke; artifact review |
| `BW-TUI-PROT-002` | BodyWar Handoff Consumption Plan | BodyWar docs/work-pack | BodyWar `WORK-PACK.md` or feature docs only | BodyWar build checks unchanged; no Playwright claim until wired |
| `BW-TUI-PROT-003` | Static UI Implementation Consumption | BodyWar app | `projects/body-war/app/**` in later task-session | `npm --prefix projects/body-war/app run check` and `test:ui` after SWU-TUI-002 |

## Recommended Order

1. Execute `UPS-GATE-001` to write the reusable integration contract.
2. Execute `UPS-GATE-002` only if the handoff export path lacks a stable convention.
3. Execute `BW-TUI-PROT-001` as the first real Studio prototype gate for TROQAR.
4. Refresh BodyWar work-pack to reference the prototype handoff as optional input to `SWU-TUI-003`.
5. Keep BodyWar `SWU-TUI-002` as the Playwright runtime gate and `SWU-TUI-003` as static UI implementation.

## `BW-TUI-PROT-001` Task Detail

Inputs:

- `projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md`
- `projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md`
- `projects/body-war/docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md`
- current static app constraints from BodyWar UX plan

Actions:

1. Create an isolated Studio data directory.
2. Open a Studio session with 1-3 variants.
3. Submit an objective for the online runner profile and safe Strava connection state.
4. Generate/register HTML variants from the UI-SPEC.
5. Stamp `data-od-id` targets from UI concepts.
6. Preview and annotate with at least one comment on profile/link/activity/evidence controls.
7. Accept or discard until one baseline is handoff-worthy.
8. Export handoff with explicit confirmation.

Exit criteria:

- handoff cites upstream UI-SPEC/TEST-SPEC paths;
- every accepted prototype component maps to `data-od-id` or is flagged as fallback;
- no real athlete token/private payload appears in HTML or handoff;
- BodyWar app source remains untouched.

## Validation Plan

Current refine validation:

- `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py .../REFINE-DISPATCH.json`
- `python3 -m json.tool .../evidence-index.json`
- `git diff --check -- projects/ui-prototyping-studio`

Future execution validation:

- Studio code unchanged: artifact review plus `git diff --check`.
- Studio code changed: `pnpm --dir projects/ui-prototyping-studio/backend test:e2e`.
- BodyWar docs changed: `git diff --check -- projects/body-war`.
- BodyWar app changed after Playwright wiring: `npm --prefix projects/body-war/app run check` and `npm --prefix projects/body-war/app run test:ui`.

## Handoff To Task Session

The first executable route should be a `task-session` for `UPS-GATE-001`, then
a second `task-session` for `BW-TUI-PROT-001` once the reusable contract exists.

## Verdict

`pass`: plan is execution-ready as a sequence of bounded SWUs. No implementation
should run inside this refine.

## Receipt

```json
{
  "stage": "09-invoke-plan",
  "status": "pass",
  "artifacts": [
    "stages/09-invoke-plan.md"
  ],
  "validation_result": "pass",
  "blockers": [],
  "residue": [
    "Actual prototype session not executed.",
    "BodyWar work-pack not mutated in this refine run."
  ]
}
```
