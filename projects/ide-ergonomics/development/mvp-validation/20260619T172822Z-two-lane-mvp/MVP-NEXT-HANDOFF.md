# MVP Next Handoff

Status: ready-for-next-route
From dispatch: `ide-ergonomics-mvp-two-lane-20260619T172822Z`
Registry dispatch: `2026-06-19-ide-ergonomics-mvp-two-lane`

## Outcome

The current three-card MVP was rejected as the first implementation shape. The
winning first proof is a bounded conversation-transition card with a route menu.

## Next Owner

Recommended next owner: `invoke`

Reason: the next move is define/design, not implementation mutation or
Spellcraft promotion. The route needs a compact product contract, fixture set,
owner map, and validation surface before a `task-session` builds anything.

Secondary owners:

- `dispatch-spec` for route-menu shape and permission boundaries;
- `definitions-governance` for definition-candidate packets;
- `necronomicon` for side-node and handoff surfaces;
- `task-session` after Invoke creates the bounded implementation packet.

## Next Prompt

Use this prompt for the next run:

```text
Use invoke to define/design the bounded conversation-transition card MVP for
projects/ide-ergonomics. Source artifacts:
- MVP-TWO-LANE-SYNTHESIS.md
- findings.md
- research.md
- LANE-RECEIPTS.md

Goal: produce an implementation-ready design packet for a toy proof where an
IDE-side card recognizes a selected conversation span and offers an owner-safe
route menu: definition candidate, side node, handoff draft, route ambiguity,
delegated-run preview, and park/ignore.

Constraints:
- no canonical promotion;
- no runtime subagent execution from the UI proof;
- route menu must show owner, boundary, artifact preview, and permission state;
- use static conversation fixtures before building a real IDE extension;
- include validation criteria for deciding whether the MVP proves the problem.
```

## Acceptance Criteria For Next Packet

- Names the selected MVP as `bounded conversation-transition card`.
- Defines the route-menu states and owner boundaries.
- Includes at least three static conversation fixtures:
  - definition candidate;
  - route ambiguity;
  - side node or handoff.
- Explains what artifact, if any, each route may draft.
- Keeps delegated-run preview permission-gated and non-runtime.
- Defines what evidence would make the MVP pass, fail, or need reroute.

## Residue

- Host feasibility remains untested.
- UI design remains untested.
- No canonical Arcanum mutation should happen from this handoff.
