---
tags: [inventory, strategy-result, dispatch, subagents, research, ux-lessons, artifact-governance, operational-evidence, claim-le-proof, body-war]
node_type: synthesis
is_session: false
layer: strategy
nature: synthesis
status: closed
created: 2026-07-09
dispatch_id: 2026-07-09-ui-prototyping-studio-ux-upgrade-research
dispatch_type: research
working_folder: projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/
sources: [projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/research.md, projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/findings.md, telemetry/agents/subagents-dispatch.yaml]
---

# UI Prototyping Studio UX/UI Upgrade Research Strategy Result

This is a non-authority Inventory read model for the resolved governed research
dispatch `2026-07-09-ui-prototyping-studio-ux-upgrade-research`. It records the
strategy, evidence boundary, accepted findings, auditor result, and next
implementation order. It does not mutate the Studio implementation, promote
prototype HTML into production, or turn Open Design into Studio authority.

## Strategy Summary

The dispatch was triggered to research which upgrades are needed inside
`projects/ui-prototyping-studio`, with heavy interaction against the current
runtime and a comparison against the vendored Open Design reference. The run used
isolated `/tmp` `STUDIO_DATA` surfaces for destructive interaction and preserved
Body War/TROQAR as handoff evidence, not as a mutation target.

The explorer fan-out covered four independent lenses:

- `Turing, Alan` inspected runtime, CLI, preview, browser controls, tests, and
  direct TROQAR-style interaction evidence.
- `Alexander, Christopher` compared the Studio model with the vendored Open
  Design skill, mode, craft, tweak, critique, live-artifact, and design-brief
  references.
- `Schon, Donald` ran a reflective UX walkthrough across desktop/mobile preview,
  staged state, accept/revert, annotation, and Body War/TROQAR copies.
- `Beer, Stafford` inspected governance viability, export boundary, stale docs,
  test-count drift, Prototype Gate semantics, and Body War/TROQAR handoff
  consumption.

The reviewer group converged on a correction: the result should be framed as a
governance-truth finding, not a generic feature backlog. Studio has credible
reversible prototype state-machine evidence, but its browser/control projection
is not yet reliable governed-state projection.

## Accepted Findings

The accepted `findings.md` says the immediate work is truth-preserving operator
evidence:

1. Current-head projection after accept/revert/external writes.
2. Visible-change diff integrity for CSS/theme/global/layout changes.
3. Preview state coherence across CLI/server mutation paths.
4. Durable reversible-action framing for Accept/Revert.
5. Deterministic e2e harness as a validation prerequisite.
6. Handoff evidence semantics around `missingRefs` and readiness flags.
7. Mobile before/after and annotation usability.
8. Governance hygiene: docs, test counts, preview wording, and state claims.
9. Minimal OD-inspired `CraftEvidencePack` slice inside Studio gates.

Every recommended upgrade names a smallest runnable witness, likely file/surface,
and validation receipt. The auditor accepted that the recommendations are
actionable and grounded in the transcript.

## Evidence Highlights

- Reversible lineage works: isolated `STUDIO_DATA`, variant registration,
  baseline selection, staged apply, accept, append-only revert, annotation, and
  terminal-only confirmed handoff were observed in the explorer transcript.
- Export confirmation is a stronger boundary than the preview/control surface:
  unconfirmed handoff export refused, and confirmed export is backed by core and
  HTTP route behavior.
- The main defect is governed-state projection: after Accept, `/raw/baseline`
  can reflect the accepted head while visible preview cards and annotation still
  render the original variant.
- Preview state can go stale across external CLI writes while the server is
  running.
- Visible CSS/theme changes can produce zero diff evidence, which falsifies
  "saw the change" confidence.
- Body War/TROQAR is valid precedent for selector/copy obligations flowing into
  app specs/tests, not proof that Studio HTML is production-ready.
- Open Design is useful only as subordinate evidence/profile scaffolding behind
  Studio register/baseline/stage/manifest/export gates.

## Open Design Boundary

Safe Open Design borrowings are limited to Studio-owned structures:

- `CraftEvidencePack` as the first runnable slice, with required/advisory/
  subjective buckets.
- Later `GeneratorProfile`, `DesignObjectiveBrief`, seed/archetype,
  `CritiqueReview`, staged tweak deltas, and source/derived/provenance packaging,
  only after state projection and diff integrity are repaired.

Forbidden moves:

- No direct OD artifact output as final product.
- No subjective critique as an admission gate before calibration.
- No OD live-artifact connector/daemon runtime import into Studio's boundary.
- No Open Design identity replacement.

## Auditor Result

`Brandenburg, Martin` returned `PASS`. The audit found that `findings.md` stays
within the transcript proof, preserves the Studio identity boundary, includes
actual interaction evidence, bounds Open Design comparison to the vendored
snapshot and subordinate evidence/profile use, and gives each ranked upgrade a
smallest witness plus validation receipt.

Residual risks retained by the auditor:

- The audit used the transcript rather than re-running commands or opening `/tmp`
  screenshots/logs.
- Some evidence artifacts are `/tmp` paths and may be ephemeral.
- Current-head projection and preview state coherence overlap slightly, though
  not enough to block the result.
- Fresh checked-in e2e remains explicitly unclaimed.

## Source Refs

- `projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/research.md`
  - strategist-owned explorer transcript and robot-talks positions.
- `projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/findings.md`
  - accepted upgrade findings and implementation order.
- `telemetry/agents/subagents-dispatch.yaml`
  - append-only dispatch row and close row for this research run.

## Residue

- No Studio implementation changes were made by this run.
- The findings do not claim production readiness, release readiness, calibrated
  critique scoring, import integrity, trust-meter readiness, or fresh checked-in
  e2e proof.
- The next implementation run should start with a failing/passing witness for
  current-head projection after Accept/Revert/external writes.
