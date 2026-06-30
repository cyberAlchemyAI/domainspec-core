---
run_id: 20260629T162639Z-standalone-package-plan
target: development/resonantos-integration/standalone-package-plan
status: pass
created: 2026-06-29T16:26:39Z
owner: refine
---

# Refine Seed Proposal: ResonantOS CyberAlchemy Standalone Package Plan

## Target

Create a refined, non-executed implementation plan for a standalone package that carries the
CyberAlchemy governance integration for ResonantOS without depending on the private parent
checkout or leaking private-only source material.

## Source Context

- `development/resonantos-integration/RESONANTOS-INTEGRATION-GUIDE.md`
- `development/resonantos-integration/findings.md`
- `development/resonantos-integration/owned-base/BASE-FOR-VICTOR.md`
- `development/resonantos-integration/HANDOFF-CARD.md`
- `development/resonantos-integration/standalone-package-plan/`

## Refinement Frame

The package should be standalone in the practical sense: a collaborator can inspect the package,
understand the seam, copy or port the public-safe contracts, run validator checks where runnable,
and know which host-side implementation work remains. It should not claim a turnkey integration.

## Delivery Boundary

Included:

- Package skeleton and manifest for a local staging package.
- Evidence-card and EvidenceSet schema/validator carry-forward plan.
- Review Queue candidate mapping and no-promotion guardrail.
- Read-only observer/meter first runtime slice.
- Host-side promotion provider body contract behind ResonantOS's existing `promote_review_artifact`
  seam.
- Boundary scrub and private-repo handoff plan.

Excluded:

- Direct edits to the external/private handoff repository.
- Runtime implementation in ResonantOS.
- Public Arcanum package promotion.
- Private codenames, engine internals, internal layer maps, or parent-repo provenance.

## Preset And Research Decision

- Preset: `standard`
- Research mode: `no-research`
- Reason: the existing local evidence already names the ResonantOS seam, the runnable/copyable
  base, the honest unbuilt gaps, and the public/private boundary. External research would add
  risk and is not needed for this plan.

## Done Criteria

- Refine evidence folder exists with dispatch route, runtime handoff, manifest, evidence index,
  and result.
- Invoke canonical files exist under `development/resonantos-integration/standalone-package-plan/`.
- Work-pack is split, layer-mapped, and SWU-ready.
- Dispatch route validates with the repository dispatch-spec validator.
- Distill validation records a pass/flag/block verdict and recomposition proof.

## Planned Next Route

After authoring, use `task-session` on one selected SWU, starting with `SWU-RCI-001`.
