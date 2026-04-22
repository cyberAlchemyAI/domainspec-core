# MARS Dry Run: Foundation Gate Walkthrough (E1)

**Status:** tabletop complete
**Tier:** foundation
**Experiment anchor:** E1 - Derivation Determinism
**Date:** 2026-04-21

## Goal

Validate MARS hard-gate progression (G1-G4) for a foundation-tier experiment before first full execution wave.

## Scope

- No production run executed.
- This is a readiness simulation for the lifecycle chain.
- Output is gate decisions plus remediation notes.

## Claim Mapping

- Primary claim: C2 (deterministic derivation from typed ontology)
- Paper section: 5.1

## Protocol Inputs

- Base protocol: `research/projects/domainspec/experiments/E1-derivation-determinism/protocol.md`
- MARS checklist: `protocols/MARS-PROTOCOL-CHECKLIST.md`
- Source/inventory policy: `definitions/INVENTORY-READINESS-GATE.md`

## Gate Walkthrough

| Gate | Decision | Evidence | Notes |
|---|---|---|---|
| G1 protocol measurable | pass | E1 has measurable criteria and explicit data columns | Ready to proceed to sourcing |
| G2 source quality | pass | Internal repository sources are accessible and version-pinnable by commit SHA | External source selection not required for this dry run |
| G3 inventory readiness | pending | Inventory coverage report not yet generated for selected internal source IDs | Run inventorist lookup and validate before live execution |
| G4 data integrity | pending | No run data generated in tabletop mode | Requires S7 execution output |

## Immediate Actions Before Live Run

1. Produce inventory coverage report for E1 source set.
2. Confirm INVENTORY-INDEX has linked entries for all required source IDs.
3. Execute one foundation-tier live run and complete G4 integrity audit.
4. Update `results/MARS-EVIDENCE-STATUS.md` after analysis.

## Dry-Run Outcome

- Lifecycle chain is coherent.
- Hard gates are actionable.
- Remaining blockers are explicit and limited to inventory/data artifacts.
