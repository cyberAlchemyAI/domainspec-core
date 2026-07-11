---
id: ui-prototyping-studio-governed-state-projection-architecture
project: ui-prototyping-studio
docType: architecture-upgrade
invoke_run: invoke-20260710T012443Z-governed-state-projection
status: proposed
phase_status: flag
updatedAt: 2026-07-10T01:24:43Z
---

# Architecture Upgrade: Governed State Projection Spine

## Verdict

Upgrade the Studio around a single **governed-state projection spine**: a small
application-level projection service that derives the browser preview model,
annotation target, before/after panes, diff evidence, action framing, and handoff
evidence semantics from the same current-head state and evidence rules.

This is not a design-generator upgrade. Studio remains a reversible prototype
governance and handoff-evidence harness. Open Design can supply subordinate
evidence/profile patterns only after state projection and diff truth are repaired.

Phase status is `flag`, not `pass`, because this is discovery-mode design from
accepted research findings rather than a normal Invoke design from a freshly
approved define artifact.

## Source Contracts

| Source | Role |
| --- | --- |
| `projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/findings.md` | Accepted UX/UI upgrade findings and ranked witnesses. |
| `projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/research.md` | Explorer transcript with runtime, UX, Open Design, and governance evidence. |
| `projects/ui-prototyping-studio/ARCHITECTURE.md` | Existing architecture and generator/admission seam. |
| `projects/ui-prototyping-studio/SPEC.md` | Existing state machine, surfaces, and acceptance criteria. |
| `projects/ui-prototyping-studio/backend/src/cli/studio.ts` | Current preview rendering, annotation, action, `/state`, and raw HTML routes. |
| `projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/current-html.ts` | Existing current-head resolver. |
| `projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/admission.ts` | Current scope admission and honest diff implementation. |
| `projects/ui-prototyping-studio/backend/e2e/helpers.ts` | Current e2e helper path that shells through `pnpm exec tsx`. |

## Design View 1 - Context

The accepted research found that the core reversible lineage is credible, but
the browser/control surface is not reliable governed-state projection. The
largest failure is not visual polish. It is that accepted state, browser preview,
annotation target, diff evidence, and next-step copy can disagree.

The code already contains part of the missing shape:

- `resolveCurrentHtml(...)` resolves the current head from a committed revision
  or baseline artifact.
- The preview still renders main cards from `listSessionVariants(...)` and
  annotation from `/annotate/variant/${baseline.label}`.
- `/raw/baseline` serves the current head, but it is not the primary inspectable
  artifact after Accept/Revert.
- `diffByOdId(...)` excludes `<style>` nodes from structural fragments, while
  the fence handles CSS separately. This permits visible style changes to have
  no visible diff lane.

## Design View 2 - High-Level Structure

Add one application service and one presentation contract:

```text
StudioSessionStorePort + ArtifactContentPort
          |
          v
resolveCurrentHtml + staged candidate + revisions + handoff evidence
          |
          v
GovernedStateProjectionService
          |
          +-- PreviewProjection
          +-- AnnotationProjection
          +-- DiffEvidenceProjection
          +-- ActionFramingProjection
          +-- HandoffEvidenceProjection
          |
          v
studio preview HTTP adapter
```

The preview adapter should render a projection object. It should not independently
decide what the current head is, what the annotation target is, whether a style
diff is honest, or whether export means implementation-ready.

## Design View 3 - Low-Level Components

| Component | Responsibility | First target |
| --- | --- | --- |
| `GovernedStateProjectionService` | Build a read-only projection from session, current head, staged candidate, revisions, comments, and handoff metadata. | New application module or small internal helper near `current-html.ts`. |
| `PreviewProjection` | Expose primary current-head iframe route, historical variants, state labels, and action state. | Replace preview card source selection in `studio.ts`. |
| `AnnotationProjection` | Point annotation at the current governed head, not the original baseline variant, and expose selected target/comment state. | Replace `/annotate/variant/<label>` as the default annotation source after head exists. |
| `DiffEvidenceProjection` | Include component fragments plus global/style/unattributed visible-change lane. | Extend `DiffSummaryHonest` or add compatible metadata before display/handoff. |
| `ActionFramingProjection` | Name durable reversible actions and required confirmation fields. | Accept/Revert confirmation sheet in preview. |
| `HandoffEvidenceProjection` | Separate `exportConfirmed`, `evidenceComplete`, `integrationReady`, and `implementationReady`. | Handoff bundle/read model and export tests. |
| `e2eCliRunner` | Run local `tsx` deterministically without ambient Corepack dependence. | `backend/e2e/helpers.ts`. |

## Design View 4 - Workflow Process

1. Preview request loads latest persisted state or a state version.
2. Projection service resolves current head:
   - committed revision artifact when `revisionHeadId` has `candidateHtmlHash`;
   - otherwise selected/committed baseline variant artifact.
3. Projection service declares the primary inspectable artifact:
   - `current-head` for recorded sessions;
   - `staged after` for staged sessions;
   - historical variant cards only as reference.
4. Annotation defaults to current head and records comments against the active
   revision id.
5. Diff evidence presents per-od-id fragments and a global/style lane when raw
   HTML/CSS changes cannot be attributed to components.
6. Accept/Revert require durable reversible-action framing before posting.
7. Handoff export stays terminal-confirmed and does not imply implementation
   readiness when refs or evidence are missing.

## Design View 5 - Decision Flow

| Decision | Default | Rationale |
| --- | --- | --- |
| Projection service vs more preview-local helpers | Projection service | Keeps current-head, annotation, diff, and handoff semantics from drifting across routes. |
| Render current head as primary after Accept/Revert | Yes | The operator must see what is governed now, not the original candidate population. |
| Keep historical variants visible | Collapsed/reference | Useful for lineage but not the primary controlled artifact after revision recording. |
| Treat style/global diff as component diff | No | Avoid false precision. Use a global/style lane or explicit unattributed visible-change marker. |
| Add OD `CraftEvidencePack` now | Not before L2 | OD evidence is useful, but runtime projection and diff truth are prior gates. |
| Use subjective critique as a gate | No | Advisory only until calibrated fixtures exist. |

## Design View 6 - Dependency Interface

| Interface | Contract |
| --- | --- |
| Store -> projection | Read latest session, variants, revisions, staged record, comments, and handoff bundle. Must not mutate. |
| Artifact store -> projection | Resolve current, staged, and historical HTML by artifact ref. |
| Projection -> preview adapter | Return serializable display model with routes, labels, action states, diff lanes, and evidence semantics. |
| Projection -> tests | Provide stable observables for Playwright: current-head text, annotation source, state signature, diff lanes, action confirmation. |
| Projection -> handoff | Use readiness labels that do not collapse export confirmation into implementation readiness. |

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| `sequence` | research findings -> architecture upgrade -> plan -> task-session | Each output consumes the previous evidence handle. | pass |
| `concrete_path_evidence` | all load-bearing claims | Claims cite concrete repo paths or research lines. | pass |
| `owner_boundary_check` | Invoke vs Studio implementation vs Task Session | Invoke authors only design/plan; task-session owns mutation. | pass |
| `artifact_contract_bridge` | projection service and work-pack | Planned artifacts name validation surfaces and do not claim promotion. | pass |
| `validation_loop` | each architecture slice | Each slice has a failing/passing witness. | pass |
| `residue_ledger` | unresolved gaps | Missing define artifact, e2e Corepack fragility, and OD phase-two are carried. | pass |
| `scu_swu_reduction` | plan handoff | First execution unit is `SWU-GSP-001`. | pass |
| `recomposition_proof` | SWUs -> architecture | SWUs recompose into the governed-state projection spine. | pass |
| `execution_receipt_handoff` | task-session route | Each SWU defines receipt shape, files, validation, and blockers. | pass |

Full dispatch JSON is not required for this Invoke run because no subagent fanout,
external protected context, or multi-owner execution is being launched now.

## Distill Design-Unit Check

- Coherent unit: governed-state projection spine.
- Split pressure: high enough to require medium plan output, because diff,
  preview state, action framing, test harness, and docs are separate write
  surfaces.
- Recomposition proof: the first SWU (current-head projection) establishes the
  projection boundary; later SWUs extend it to diff, state refresh, actions, and
  evidence semantics.
- Verdict: `flag`. The design is plan-ready for `SWU-GSP-001`, but broader
  release-readiness remains blocked by fresh checked-in e2e and L1/L2 proof.

## Gaps And Non-Goals

- No production HTML claim.
- No Open Design identity replacement.
- No subjective critique hard gate.
- No human-vs-agent identity gate.
- No fresh checked-in e2e claim until the helper path is fixed.
- No release-readiness claim until current-head projection, visible-change diff,
  preview coherence, and L1/L2 checks have receipts.
