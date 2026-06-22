# Studio Prototype Gate

Status: active contract

## Purpose

The Studio Prototype Gate is the reusable interface between a DomainSpec UI
pipeline and UI Prototyping Studio.

It runs after a feature has `UI-SPEC.md` and `TEST-SPEC.md`, and before a
target application mutates production source. The gate makes a UI contract
visible in a browser, captures concrete comments against stable component IDs,
and exports handoff evidence for a later implementation task.

```text
DomainSpec feature docs
  -> UI-SPEC.md
  -> TEST-SPEC.md
  -> studio prototype session
  -> confirmed handoff bundle
  -> target-app task-session
  -> target-app browser validation
```

## Owners

| Owner | Owns | Does Not Own |
| --- | --- | --- |
| DomainSpec UI pipeline | Canonical UI and test specs. | Studio session state or prototype acceptance. |
| UI Prototyping Studio | Prototype variants, annotations, reversible acceptance, and handoff export. | Canonical spec promotion or target app source mutation. |
| Target app task-session | Production source changes and real app validation. | Studio's internal prototype session. |

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| `UI-SPEC.md` | yes | Source presentation contract. |
| `TEST-SPEC.md` | yes | Browser and accessibility obligations. |
| Visual definitions | recommended | Brand, layout, component, and copy constraints. |
| Target app constraints | yes | Current framework/runtime, security posture, and non-goals. |
| Handoff export profile | yes for cross-project use | JSON profile that maps export refs to the target feature docs. |

## Operations

1. Create an isolated `STUDIO_DATA` directory for the feature run.
2. Submit a prompt that names the feature and target state.
3. Register 1-3 self-contained HTML variants.
4. Stamp annotatable elements with stable `data-od-id` values derived from the
   feature UI concepts.
5. Select or commit a baseline.
6. Preview and annotate concrete elements.
7. Synthesize, stage, and accept or discard a prototype revision.
8. Export the handoff with `handoff export --confirm --profile <profile.json>`.
9. Feed the handoff evidence into the target app work-pack or task-session.

## Required Evidence

| Evidence | Stored By | Requirement |
| --- | --- | --- |
| Session JSON | Studio run directory | Contains session, variants, comments, batches, revisions, and handoff bundle. |
| Variant HTML | Studio run directory | Each variant is self-contained and has `data-od-id` coverage. |
| Accepted revision | Studio run directory | At least one revision is recorded before handoff. |
| Handoff profile | Project docs/development | Names target UI spec, test spec, source refs, and profile id. |
| Handoff summary | Target app docs | Links prototype evidence to implementation and browser tests. |

## Invariants

- The gate is optional until a project adopts it in its work-pack.
- A Studio handoff is evidence, not source-of-truth promotion.
- Export is the irreversible downstream edge and must remain explicitly
  confirmed.
- Target app validation must run against the real app, not only Studio preview.
- Real secrets, tokens, OAuth codes, private athlete payloads, and live deploy
  credentials are never prototype inputs.

## Completion Criteria

A feature passes the gate when:

- the handoff bundle cites the target `UI-SPEC.md` and `TEST-SPEC.md`;
- the accepted prototype maps key components to stable `data-od-id` values;
- fallback selectors, missing refs, and unresolved spec deviations are named;
- the target app work-pack names how the handoff will be consumed;
- implementation remains routed to target app task-session.
