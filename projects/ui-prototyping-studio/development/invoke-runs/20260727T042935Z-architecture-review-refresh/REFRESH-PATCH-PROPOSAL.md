# Invoke Refresh Patch Proposal — UI Prototyping Studio

Activation source: `direct-user`

Mutation mode: `apply-approved`

Approval evidence: the user instructed the agent to perform the next steps and
finish implementation. The approved refresh scope is limited to the paths
listed below.

## Source Signals

| Signal | Class | Source | Delta |
| --- | --- | --- | --- |
| UPS-RFR-001 | evidence_added | accepted review and parent approval | Admit the 11 verified change requests as implementation inputs. |
| UPS-RFR-002 | artifact_drift | July README/work-pack | Replace false canonical wording and contradictory proof ordering with a historical marker plus amended plan. |
| UPS-RFR-003 | route_changed | F-02/F-06 | Select shared local-`tsx` evidence-harness repair as the first SWU. |
| UPS-RFR-004 | status_changed | Craft root/extraction next moves | Replace stale extraction routing with one selected GSP execution context. |
| UPS-RFR-005 | blocker_resolved | DEC-026 plus F-07 | Record actor-neutral explicit acknowledgment; do not create a human-only gate. |
| UPS-RFR-006 | blocker_opened | human study and release authority | Preserve both as outside implementation completion. |

## Approved Target Inventory

Create:

- `development/invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md`
- `development/invoke-runs/20260727T042935Z-architecture-review-refresh/EXECUTION-PACK.md`
- `development/invoke-runs/20260727T042935Z-architecture-review-refresh/DISTILL-VALIDATION.md`
- seven task specifications under that run's `work-pack/tasks/`.

Update:

- `development/invoke-runs/20260710T012443Z-governed-state-projection/README.md`
- `.craft/ledger.yml`
- `CRAFT.md`

## Decisions

1. The July package remains historical proposal evidence and is not rewritten
   into a false execution receipt.
2. The amended work-pack is admitted for execution by the direct owner request.
3. `SWU-GSP-001` owns only deterministic, fail-fast browser evidence startup.
4. Task IDs and SWU IDs are one-to-one from `001` through `007`.
5. Confirmation is actor-neutral explicit acknowledgment, consistent with
   existing DEC-026. Identity is recorded but does not itself grant authority.
6. The optional Open Design evidence pack is removed from the current
   completion graph.
7. Release authorization and human-study ergonomics remain explicitly unbound.

## Validation Gates

- Material package schema and exact-byte path validation.
- Material handoff must be `ready`, with empty reasons and matching package
  digest.
- Craft YAML parses; required indexes exist; every added row is indexed.
- Work-pack contains seven unique task/SWU mappings and exactly one selected
  unit.
- Every implementation SWU has one primary behavior, explicit write scope,
  acceptance evidence, and validation command.
- `git diff --check` passes over the approved refresh scope.

No Studio implementation source is part of this Refresh apply. Implementation
begins only after the material receipt admits the amended plan.
