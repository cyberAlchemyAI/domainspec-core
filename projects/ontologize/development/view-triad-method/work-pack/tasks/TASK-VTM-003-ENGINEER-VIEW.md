# TASK-VTM-003 - Engineer-View Decision Inventory

## Objective

Author the engineer-view pilot decision inventory for Ontologize, with one row per system-view stance or branch-boundary decision and verified authority status.

## Layer And Slice

- Layer: L1.
- Slice: S2.
- SWU: SWU-VTM-003.

## Source Contracts

- `implementation/domainspec/.claude/skills/engineer-view/SKILL.md`
- System-view stance table from [TASK-VTM-002](TASK-VTM-002-SYSTEM-VIEW.md)
- Ontologize source matrix from [TASK-VTM-001](TASK-VTM-001-METHOD-BOUNDARY.md)
- [BRANCH-MATERIALIZATION.md](../../BRANCH-MATERIALIZATION.md)

## Implementation Detail

Algorithm:

1. Harvest every `stance:<slug>` from system-view.
2. Create exactly one decision row per stance.
3. Create branch-boundary rows for unresolved B1 meaning, B2 system, B3 run-context, and B4 bridge obligations.
4. Assign status:
   - RESOLVED only when a cited authority decides and enforces the verdict on disk;
   - OPEN when named but not enforced;
   - CRITICAL when OPEN and blocking the core value thesis.
5. Verify each cited authority by reading the file or gate.
6. Strike unverifiable authorities and downgrade the row to OPEN.
7. Record B3 decisions for run boundary, denominator, lifecycle state, scope/posture, stage-vs-outcome separation, and source event authority.
8. Record B4 owner-decision routes and separate raw drift from adjudicated contradiction.
9. Link schemas/contracts and runtime mechanics to the owning decision rows.

## Smallest Working Units

### SWU-VTM-003

- Goal: draft `view-triad/engineer-view.md`.
- Dependencies: SWU-VTM-002.
- Write scope: proposed `projects/ontologize/view-triad/engineer-view.md`.
- Done criteria:
  - decision inventory has one row per stance or branch-boundary decision;
  - each row has verdict, status, and authority;
  - authority verification notes are present;
  - B3 run-context record is complete or publication blocker is explicit;
  - B4 bridge rows separate raw drift, adjudicated contradiction, engineer-view verdict, DAG OwnerDecision, and product approval;
  - orphaned and duplicate stance counts are 0, or blockers are explicit;
  - schemas/contracts and runtime mechanics point back to decision rows.
- Acceptance evidence: authority verification table, stance coverage map, B3 run-context record, and B4 authority map.
- Validation surface: manual review against engineer-view output contract.
- Execution owner: local-fallback.
- Handoff note: never copy GoldenQuill-specific row literals or local tokens into Ontologize.

## Synchronization

Carry decision rows into [TASK-VTM-004](TASK-VTM-004-ONTOLOGY-VIEW.md).
