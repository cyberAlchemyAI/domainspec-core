# Context Pack: SWU-WUI-004

- Task: `SWU-WUI-004` - Explicit Request Mode
- Mode: standard
- Runtime: local Node and Playwright Chromium
- Dependency receipt: [SWU-WUI-003 PASS](../20260720T155936Z-swu-wui-003/TASK-SESSION-RESULT.md)
- Gate verdict: pass; the existing prepare endpoint already expresses both modes

## Obligation Matrix

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| A1 | Execute exactly `SWU-WUI-004` after `SWU-WUI-003`. | covered | Work Pack, task contract, dependency receipt |
| A2 | Expose an explicit Agent task/Dry run mode choice with Agent task selected by default. | covered | task contract, WUI-D1, UX plan |
| A3 | Require a valid Skill value for Agent task mode. | covered | task contract, current input constraint, prepare schema |
| A4 | Omit Skill and skill-invoke grants from Dry run payloads. | covered | task contract, existing prepare handler, schema and server behavior |
| A5 | Preserve entered Task and Skill values when validation fails. | covered | task contract, current form behavior, focused browser witness |
| A6 | Keep the existing prepare endpoint and approval/kernel contracts unchanged. | covered | task handoff, architecture bundle, request schema |
| A7 | Prove both selected modes emit their intended payload and do not silently switch when Skill is empty. | covered | independent acceptance, prepare endpoint test surface |
| A8 | Run `npm run test:workbench` and focused Agent task/Dry run Playwright cases. | covered | task contract, package scripts |
| A9 | Do not add lifecycle projection, provider execution, browser control, worker, or IDE-host scope. | covered | Work Pack gates, spec exclusions |

## Selected Context

| Source | Why selected | Selectors / obligations |
| --- | --- | --- |
| `development/workbench-ui-v1/WORK-PACK.md` | authoritative next unit and mode boundary | WUI-004 manifest, gates; A1-A9 |
| `development/workbench-ui-v1/work-pack/tasks/TASK-WUI-002-COMPOSER.md` | exact mode objective, write scope, done criteria, and handoff | SWU-WUI-004 contract; A1-A9 |
| `development/workbench-ui-v1/SPEC.md` | product definition and explicit mode decision | included/excluded, WUI-D1/WUI-D5; A2, A6, A9 |
| `development/workbench-ui-v1/UX-PLAN.md` | mode control and primary action language | segmented Agent task/Dry run interaction; A2-A5 |
| `development/workbench-ui-v1/ARCHITECTURE-BUNDLE.md` | mode selector and endpoint ownership boundary | component/dependency views; A2, A6, A9 |
| `public/demo/l0.html` | current composer DOM, validation, and payload mapping | prepare bar, inputs, click handler; A2-A6 |
| `schemas/prepare-request.schema.json` | existing payload contract and conditional requirements | requested skill/grants conditions; A3-A4, A6 |
| `tests/e2e/l0-approval-desk.spec.mjs` | retained prepare and approval browser oracle | prepare journey and state preservation; A5, A7-A8 |

## Implementation Assumption

Add a text-labeled segmented control with `Agent task` selected initially. Keep
one Skill input in the existing composer, make it required only for Agent task,
and hide it from the visible form for Dry run. The submit handler will derive
the existing payload from the selected mode: Agent task sends the current
schema-v2 fields and grants; Dry run sends the current legacy no-skill shape.
Validation returns before clearing either field, so invalid submissions preserve
entered values. This is reversible within the composer unit and does not require
a server contract change.

## Execution Constraints

- Preserve `/api/envelopes/prepare`, `agent_ref`, `requested_skill`, and
  `requested_grants` semantics already accepted by the server.
- Do not infer mode from an empty Skill value.
- Keep Agent task as the initial/default mode.
- Keep Dry run explicit and ensure its payload omits Skill and `skill.invoke`.
- Keep error messages and entered Task/Skill values available after validation
  failure.
- Do not change approval, bridge, lifecycle, Canvas, Craft, evidence, provider,
  browser, worker, or VSCodium behavior.

## Context Builder Result

- Files selected: 8
- Snippets selected: 8 selector-level excerpts
- Obligation coverage: 9/9
- Strict coverage: pass
- Fallback search: none
- Blockers: 0

## Next Actions

1. Add the explicit mode control and mode-aware Skill presentation.
2. Keep the existing endpoint payload shapes and add focused mode/validation
   browser assertions.
3. Run the workbench suite and both mode journeys, then synchronize WUI-005
   only after the evidence passes.
