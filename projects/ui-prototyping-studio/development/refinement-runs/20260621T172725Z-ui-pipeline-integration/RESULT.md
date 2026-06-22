# Refine Result - UI Prototyping Studio UI Pipeline Integration

Status: `pass`
Generated: `20260621T172725Z`
Target: `projects/ui-prototyping-studio/`
Preset: `standard`
Research: `no-research`

## Final Synthesis

UI Prototyping Studio should integrate with the DomainSpec UI pipeline as a
**Studio Prototype Gate**: an optional stage after `UI-SPEC.md` and
`TEST-SPEC.md`, and before target-app implementation.

```text
DomainSpec feature docs
  -> UI-ARCHITECTURE.md
  -> UI-SPEC.md
  -> TEST-SPEC.md
  -> Studio prototype session
  -> accepted prototype handoff
  -> target-app task-session
  -> Playwright and visual audit
```

The studio should consume UI pipeline artifacts, make the design browser-visible
through 1-3 self-contained HTML variants, capture annotations through stable
`data-od-id` targets, preserve accept/revert control, and export a handoff.
It should not replace the UI pipeline, promote canonical specs, or mutate the
target app.

## Dispatch Strategy

| Field | Value |
| --- | --- |
| Route | `prototype-gate` |
| Rejected route | `pipeline-replacement` |
| Deferred route | `bodywar-only-spike` |
| Subagents | none |
| Join policy | none |
| Research | no external research |
| Dispatch | `REFINE-DISPATCH.json` validated pass |

## Stage Evidence

| Stage | Status | Artifact |
| --- | --- | --- |
| Context Builder evidence baseline | pass | `stages/01-context-builder.md` |
| Invoke Define | pass | `stages/02-invoke-define.md` |
| Interrogation refine-review | pass | `stages/03-interrogation-refine-review.md` |
| Research decision | pass | `stages/04-research-decision.md` |
| Distill | pass | `stages/05-distill.md` |
| Invoke Redefine / Design | pass | `stages/06-integration-design.md` |
| Interrogation refine-design-review | pass | `stages/07-design-review.md` |
| Distill Repair | pass | `stages/08-distill-repair.md` |
| Invoke Plan | pass | `stages/09-invoke-plan.md` |
| Final Interrogation and Synthesis | pass | `stages/10-final-interrogation.md` |

## Integration Contract

| Owner | Owns | Does Not Own |
| --- | --- | --- |
| DomainSpec UI pipeline | UI specs, test specs, visual definitions, source-of-truth docs | Studio session state or prototype acceptance |
| UI Prototyping Studio | Prototype session, variants, annotations, reversible acceptance, handoff export | Canonical spec promotion or target app source mutation |
| Target app task-session | Real app implementation and validation | Studio's prototype session internals |

## First BodyWar/TROQAR Use

Use BodyWar/TROQAR as the first proof:

1. Use `troqar-product-architecture/UI-SPEC.md` and `TEST-SPEC.md` as inputs.
2. Run a Studio session for the online runner profile and safe Strava connection state.
3. Register 1-3 variants with `data-od-id` values such as `auth.connect.cta`,
   `profile.safe-athlete-card`, `profile.strava-link`, and `activity.recent-summary`.
4. Preview, annotate, accept/revert, and export a handoff.
5. Feed the handoff into BodyWar `SWU-TUI-003` static UI hardening after
   `SWU-TUI-002` wires Playwright runtime.

## Recommended Next Routes

| Route | Purpose |
| --- | --- |
| `task-session` for `UPS-GATE-001` | Write the reusable Studio Prototype Gate integration contract. |
| `task-session` for `BW-TUI-PROT-001` | Run the first TROQAR prototype session and produce handoff evidence. |
| `invoke refresh` or `task-session` sync for BodyWar work-pack | Add the prototype handoff as optional input to `SWU-TUI-003`. |

## Residue

- Actual prototype execution did not run in this refine.
- BodyWar work-pack was not mutated in this refine.
- Handoff export destination convention still needs a reusable doc/template.
- BodyWar Playwright runtime remains owned by `SWU-TUI-002`.

## Verdict

`pass`: the integration is production-shaped as a governance and evidence
bridge, not as a source-of-truth replacement. It is ready for bounded
task-session execution.
