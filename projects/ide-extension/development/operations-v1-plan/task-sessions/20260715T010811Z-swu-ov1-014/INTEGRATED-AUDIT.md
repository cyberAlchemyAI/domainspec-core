# Integrated Audit: Operations V1

## Verdict

PASS. All fourteen ordered SWUs now have retained evidence, the complete Node
and Playwright matrices pass, schemas and dispatch validate, the human value
gate is closed, and the plan recomposes without an active Operations V1
blocker.

The supported claim is exactly:

> A trusted local agent can derive an immutable workbench surface from an exact
> V0 HTML revision, apply retry-safe whole-document HTML operations, and display
> each committed complete revision without changing the original V0 API.

This does not support regions, collaboration, automatic merge, hostile HTML
safety, remote control, provider execution, protected effects, or IDE
embedding.

## Integrated Validation

| Surface | Result |
| --- | --- |
| Complete serial Node matrix | PASS, 187/187 |
| Complete Playwright matrix | PASS, 18/18 desktop/mobile |
| Deterministic schema validation | PASS, 21 runtime schemas, 6 manifests, 78 fixtures |
| Schema behavior suite | PASS, 6/6 |
| Dispatch validation | PASS, 0 blocks, 0 flags |
| JSON parse audit | PASS, 140 files |
| JSONL parse audit | PASS, 5 files, 14 records |
| Craft pre-close invariant audit | PASS, 1 context, 5 decisions, 5 gaps, 32 artifacts |
| Human usefulness review | PASS, Option 1 |
| Scoped `git diff --check` | PASS |

## Acceptance Regression Repair

The first integrated Node run proved `GAP-OV1-006`: the inherited standalone
surface matrix rejected every `/api/craft/*` literal even though the host's
read-only `/api/craft/frontier` route is already intentional and independently
tested. Only `tests/session-content-workbench-matrix.test.mjs` changed.

The repaired assertion:

- still rejects every decision-specific API route;
- enumerates every Craft API literal in the server;
- permits exactly `/api/craft/frontier`;
- fails if any specialized Craft route is introduced.

The focused repaired test passed 1/1, followed by the complete 187/187 Node
matrix. Runtime behavior did not change.

## Obligation Result

Every `OV1-D1` through `OV1-D9`, `OVG-001` through `OVG-004`, and the honest
user-value claim has direct retained evidence in
[traceability.md](../../work-pack/shared/traceability.md). In particular:

- separate V0 and Operations identities survive restart;
- immutable content bodies fail closed when absent or corrupt;
- whole-document parser operations commit complete revisions only;
- CAS, idempotency, conflict, stale-input, and concurrency behavior pass;
- navigation remains separate from content revision history;
- exact rebuild never creates implicit V0 synchronization;
- retention uses grace, hard limits, tombstone-before-delete, and restart
  recovery without deleting current/shared/un-tombstoned data;
- operations do not mint approval, grant, skill-execution, provider, or
  protected-effect authority.

## Residue

| ID | Final classification |
| --- | --- |
| GAP-OV1-001 | accepted trusted-local limitation; hostile HTML safety is not claimed |
| GAP-OV1-002 | accepted transient acknowledgement semantics |
| GAP-OV1-003 | intentional `410 revision_pruned` retry degradation |
| GAP-OV1-004 | deferred region/scaffolding design |
| GAP-OV1-005 | workspace condition; unrelated dirty changes were preserved |
| GAP-OV1-006 | resolved by the test-only acceptance repair above |

No residue in this table blocks the supported Operations V1 claim.

## Scoped Audit

- Product/design authority files were read-only.
- The only SWU-014 behavioral-file change is the proven test assertion repair.
- Other mutations are Task Session evidence, traceability, plan status, and
  Craft synchronization.
- Existing unrelated and earlier Operations worktree changes were not reverted,
  staged, or normalized.
- Final whitespace and artifact-link checks pass.

