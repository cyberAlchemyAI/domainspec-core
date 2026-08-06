# Distill validation: pinned npm diagnostic

- Mode: Standard assumed from the default; one proposal track, two labeled
  inline rounds, and one reconciliation. Subagents were not used because the
  active route is a single serial diagnostic and no delegated work was
  authorized.
- Verdict: pass.

## Role trace

| Round | Proposer | Balancer objection | Reconciliation |
| --- | --- | --- | --- |
| 1 | Treat exact tarball fetch, install, and canaries as one opaque-artifact diagnostic. | Fetch integrity, native build, and runtime tests are separately observable. | Keep one SWU because none of those partial stages independently answers whether the npm artifact is usable; preserve stage-level results inside one terminal receipt. |
| 2 | Use one external-timeout harness with basic and concurrency modes. | A reusable runner would add a second product behavior and broaden scope. | Keep the harness attempt-local under `.work`; do not add reusable runtime code. |

## Technique trace

- Abstraction-level guard: artifact diagnostic, not package adoption.
- Recomposition proof: a pass can inform a later separately authorized Craft
  prototype; a block stops without changing the parent architecture.
- Evolution profile: only repeatability is the next natural layer; packaging,
  security, and Craft stay deferred.
- Cognitive-load check: one Work Pack, one SWU, one attempt, one closeout
  target.
- Boundary-object check: tarball digest and terminal receipt are the shared
  handles; neither is authority for source provenance or Craft.
- Premortem: likely failure is install/build incompatibility or the same native
  concurrency livelock; external process timeouts and preserved residue prevent
  false success.
- Navigable result: start at `WORK-PACK.md#SWU-WCND-001`.

## Closure

The SWU owns one primary decision: whether one exact npm artifact works for the
named local Node 26 canaries. Splitting fetch, build, and each canary would
create partial units that cannot independently establish or reject that
decision. The unit recomposes into the broader research only as evidence for a
future decision; it performs no Craft mutation.

Hidden acceptance-critical gaps: none. Exact source correspondence remains a
known out-of-scope contradiction, not a concealed prerequisite for this
opaque-artifact route.
