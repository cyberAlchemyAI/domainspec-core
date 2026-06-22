# Two-Lane MVP Findings

Dispatch ID: `2026-06-19-ide-ergonomics-mvp-two-lane`
Status: resolved
Final approver: parent

## Answer

The current three-card MVP is not the most valid first proof as written. The
better MVP is a single bounded conversation-transition card: detect a
conversation span, show an owner-safe route menu, and preview the action frame
without promotion or runtime execution.

This preserves the useful part of the original MVP - owner-safe action cards -
while testing the real problem first: whether the IDE can recognize and route a
conversation transition. Lane Z showed the three-card MVP misses route
ambiguity and side-node capture, two transition types named by the problem
statement. See [RZ-3](research.md#rz-3-counterexample) and
[RZ-4](research.md#rz-4-failure-interpretation). Lane A independently scored
the bounded route-menu MVP above the current three-card MVP across value,
boundary safety, owner clarity, implementation surface, and recomposition. See
[RA-2](research.md#ra-2-alternative-scores) and
[RA-3](research.md#ra-3-strongest-alternative).

## Verdict Matrix

| Candidate | Evidence | Witnessed? | Sound? | Verdict | Use Mode |
| --- | --- | --- | --- | --- | --- |
| Current three-card MVP | [RZ-1](research.md#rz-1-strongest-current-mvp), [RA-1](research.md#ra-1-strongest-challenge) | Partial | Overfit | Narrow | Keep as source material, not first proof |
| Repaired transition-card MVP | [RZ-5](research.md#rz-5-repaired-mvp), [RZ-6](research.md#rz-6-scores) | Yes | Yes | GO | Next MVP |
| Bounded route-menu MVP | [RA-2](research.md#ra-2-alternative-scores), [RA-3](research.md#ra-3-strongest-alternative) | Yes | Yes | GO | Merge with transition-card MVP |
| Side-node capture MVP | [RA-4](research.md#ra-4-second-strongest-alternative) | Yes | Yes | Keep as first route option | Include as route-menu option or first implemented branch |
| Definition-only MVP | [RA-5](research.md#ra-5-rejected-alternatives) | Yes | Too narrow | Reject as standalone | Keep as one route option |
| Subagent-first or full three-card build | [RA-5](research.md#ra-5-rejected-alternatives), [RZ-6](research.md#rz-6-scores) | Partial | Too costly | Reject as first proof | Defer behind permission-gated route item |

## Decision

Replace the "three widgets" MVP with a route-menu-first transition card MVP.

The MVP should prove this claim:

> A selected or detected conversation span can become an owner-safe transition
> frame, with a bounded route menu and no silent promotion or execution.

Minimum route menu:

- create definition candidate;
- capture side node;
- compose handoff draft;
- open route ambiguity menu;
- preview delegated run;
- park or ignore.

First implementation boundary:

- draft artifacts are allowed for definition candidate and handoff;
- side node may be draft-only or preview-only;
- route ambiguity is menu-only;
- delegated run is preview-only and permission-gated;
- no canonical definition, ontology, spell, sigil, or runtime promotion occurs.

## Residue

- Host feasibility remains unverified. See [RZ-6](research.md#rz-6-scores) and
  [RA-6](research.md#ra-6-residue-and-reroute).
- No browser, IDE, or UI prototype was tested. See
  [RA-6](research.md#ra-6-residue-and-reroute).
- The next route should be an Invoke design packet or Task Session proof, not a
  Spellcraft promotion.
