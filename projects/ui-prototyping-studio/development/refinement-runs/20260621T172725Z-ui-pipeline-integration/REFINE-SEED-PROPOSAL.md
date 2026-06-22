# Refine Seed Proposal - UI Prototyping Studio + DomainSpec UI Pipeline

Status: `executed`
Generated: `20260621T172725Z`
Target: `projects/ui-prototyping-studio/`
Operator intent: refine how `ui-prototyping-studio` can integrate with the UI pipeline currently being executed for BodyWar/TROQAR.

## Refinement Objective

Define the integration between UI Prototyping Studio and the DomainSpec UI
pipeline so the studio becomes a governed prototype/admission phase between
`UI-SPEC.md`/`TEST-SPEC.md` and target-app implementation, without replacing the
existing UI pipeline or silently mutating canonical specs.

## Local Evidence Baseline

| Source | Relevant Evidence |
| --- | --- |
| `README.md` | Studio is standalone and supports accountable UI exploration, preview, click-to-annotate, accept/revert, Playwright E2E, and terminal-only handoff export. |
| `SPEC.md` | Studio governs prompt -> variants -> baseline -> comments -> mutation batch -> accept/revert -> handoff; generation is external through the CLI seam. |
| `ARCHITECTURE.md` | Studio is a governance harness, not the generator; the CLI is the seam and the core enforces admission/gates. |
| `backend/package.json` | Studio already has TypeScript, Playwright, `pnpm studio`, `pnpm test:e2e`. |
| `provenance/legacy-domainspec-spec/UI-SPEC.md` | Full prior UI workbench concept exists but is archival, not current spine. |
| `BodyWar UX plan` | Current UI pipeline generated `UI-ARCHITECTURE.md`, `UI-SPEC.md`, `TEST-SPEC.md`, Playwright scaffold, and `SWU-TUI-*` work-pack. |

## Initial Integration Thesis

Use UI Prototyping Studio as an **optional prototype gate** in the DomainSpec UI
pipeline:

```text
DomainSpec feature docs
  -> UI-ARCHITECTURE.md
  -> UI-SPEC.md
  -> TEST-SPEC.md
  -> Studio prototype session
       - generate/register 1-3 self-contained HTML variants
       - stamp data-od-id from UI concept IDs
       - preview and annotate in browser
       - accept/revert reversible prototype changes
       - export handoff bundle
  -> target-app implementation task-session
  -> Playwright/visual audit
```

The studio should consume UI pipeline artifacts and produce prototype evidence
and handoff artifacts. It should not directly promote UI spec changes, mutate
the target app, or claim production implementation.

## Candidate Outputs For Full Refine

- `INTEGRATION-DESIGN.md`: architecture of the pipeline/studio bridge.
- `INTEGRATION-PLAN.md`: non-executed plan for adding a studio phase to BodyWar/TROQAR UI work.
- `WORK-PACK.md`: executable SWUs if integration is approved.
- Optional patch proposals for `projects/body-war/.../WORK-PACK.md` and UI pipeline docs.

## Preset And Research

- Preset: `standard`.
- Research mode: `no-research`.
- Rationale: local repository evidence is sufficient for the integration question; external research is not needed unless later interrogation identifies a named gap.

## Constraints

- Preserve DomainSpec UI pipeline authority over specs/tests.
- Preserve UI Prototyping Studio authority over prototype governance and handoff.
- Preserve target app authority over implementation.
- Do not turn the studio into a hidden generator or app mutator.
- Do not add real deploy, real Strava secrets, or friend/private data to prototype runs.
- Keep prototype artifacts self-contained and disposable until handoff export is explicitly confirmed.
