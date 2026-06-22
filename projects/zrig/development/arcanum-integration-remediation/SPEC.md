# Z-Rig Arcanum Integration Remediation Spec

Status: invoke architecture and plan packet
Date: 2026-06-17
Scope: private parent-local artifacts under `projects/zrig/**`

## Purpose

Create a governed remediation architecture for reviewing and improving Z-Rig engine/product-mode readiness without promoting private Z-Rig assumptions into public Arcanum surfaces.

This spec does not create a runtime adapter, public sigil, public spell, generated runtime package, or product-mode trust claim. It prepares the private architecture and implementation plan that a later bounded `task-session` can execute one SWU at a time.

## Evidence Boundary

Primary inputs:

- `projects/zrig/research/2026-06-17-arcanum-integration-handoff/INVOKE-HANDOFF.md`
- `projects/zrig/research/2026-06-17-arcanum-integration-handoff/findings.md`
- `projects/zrig/review/2026-06-17-zrig-engine-product-mode/findings.md`
- `projects/zrig/review/2026-06-17-zrig-engine-product-mode/understanding-map.md`
- Z-Rig source under `projects/zrig/z-rig-turbo-v5.5.3-engine/z-rig-orchestrator/`

The review states that Z-Rig has a coherent product shape, but is not yet product-mode trustworthy. The fastest path is gate coverage/fail-closed behavior, live identity and manifest contracts, deploy/sentinel reachability, residue/dependency fixes, and `AUTO` spec reconciliation.

## Authority Boundaries

Public Arcanum owns only generic lifecycle framing. Private parent/Z-Rig owns product evidence, review material, remediation packs, observed architecture inventories, Craft management state, and future adapter constraints if proofs later exist.

Private product material must remain under `projects/zrig/**` or another private parent path.

## Requirements

| ID | Requirement | Source |
| --- | --- | --- |
| R1 | Store all remediation architecture and plan artifacts under private `projects/zrig/**` paths. | Handoff lines 40-47; findings lines 101-104 |
| R2 | Create `SPEC.md`, `DESIGN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, and `EXECUTION-PACK.md`. | Handoff lines 43-70 |
| R3 | Create an observed architecture/gap inventory for product-mode authority. | Handoff lines 111-130 |
| R4 | Create design-only observability obligations, without claiming wired telemetry. | Handoff lines 132-142 |
| R5 | Map every SWU to F1-F14 or an explicit non-code artifact obligation. | Findings lines 101-108 |
| R6 | Select exactly one first remediation SWU for execution. | Handoff lines 179-193 |
| R7 | Start execution with F1 generic-gate fail-closed behavior unless a later gate blocks it. | Review findings lines 31-37; handoff lines 187-190 |
| R8 | Do not include runtime adapter, Signal Observer bridge, Experiment Harness, or public sigil/spell work as near-term plan items. | Handoff lines 144-155 |
| R9 | Treat validation as artifact discipline or bounded SWU proof only, not product-mode assurance. | Handoff lines 157-177 |
| R10 | Keep dry-run, live bridge, deploy/sentinel, residue, metrics, and public promotion claims separate. | Understanding map lines 91-109 |

## Non-Goals

- No public Arcanum command, sigil, spell, generated package, registry item, or adapter entrypoint.
- No assertion that Arcanum is Z-Rig's inner execution engine.
- No deploy, sentinel, live bridge, product-mode, or runtime observability assurance claim.
- No execution of Z-Rig engine changes in this invoke packet.

## Acceptance

This packet is acceptable when:

- all required private artifacts exist;
- `WORK-PACK.md` maps remediation work to F1-F14;
- `EXECUTION-PACK.md` selects exactly one first SWU;
- `PRODUCT-MODE-AUTHORITY-INVENTORY.md` distinguishes observed behavior, missing proof, remediation, and check surface;
- `OBSERVABILITY-OBLIGATIONS.md` stays design-only;
- parked work remains out of near-term execution;
- validation language does not claim product-mode readiness.

## Next Route

Invoke hands this packet to `task-session` for the selected SWU in `EXECUTION-PACK.md`: `SWU-ZRIG-F1-GATE-PROOF`. Completion of that SWU proves only bounded F1 remediation progress.
