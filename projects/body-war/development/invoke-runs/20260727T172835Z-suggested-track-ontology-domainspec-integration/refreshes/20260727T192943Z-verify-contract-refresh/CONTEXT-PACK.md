# Context Pack — BWOI Verify Contract Refresh

## Target

Repair the exact planning contract that blocked whole-frontier preflight for
`TASK-BWOI-VERIFY`. The refresh is planning-only: it does not execute
`SWU-BWOI-003`, execute verification, or mutate proof sources.

## Controlling Evidence

- Blocked frontier:
  `../../../../task-session-chains/20260727T192300Z-bwoi-all/PREFLIGHT.json`
- Owner handoff:
  `../../../../task-session-chains/20260727T192300Z-bwoi-all/CONTINUATION-HANDOFF.json`
- Current work pack:
  `../../WORK-PACK.md`
- Current verification task:
  `../../work-pack/tasks/TASK-BWOI-VERIFY.md`
- Terminal W3 route:
  `../../work-pack/waves/W3.md`

## Obligation Matrix

| ID | Obligation | Selected evidence | Status |
| --- | --- | --- | --- |
| O1 | Declare the verification-report write scope. | blocked preflight; verification task | covered |
| O2 | Declare the exact closeout target inventory. | blocked preflight; work-pack closeout table | covered |
| O3 | Declare allowed delta classes and owner validation. | owner handoff; existing BWOI closeout rows | covered |
| O4 | Use a distinct expected Invoke owner receipt. | owner handoff; existing per-unit receipt convention | covered |
| O5 | Declare a terminal no-successor policy. | W3 terminal route; owner handoff | covered |

## Excluded Context

- Integration implementation sources: `SWU-BWOI-003` has not run.
- Proof receipt content: verification has not run.
- CyberAlchemy ontology sources and DomainSpec v2 sources: read-only owners.
- Promotion, release, deployment, or wider SuggestedTrack formalization.

## Context Builder Result

- Mode: strict
- Obligations: 5
- Covered: 5
- Coverage: 100%
- Runtime handoff: none
- Authoring blocker: none

