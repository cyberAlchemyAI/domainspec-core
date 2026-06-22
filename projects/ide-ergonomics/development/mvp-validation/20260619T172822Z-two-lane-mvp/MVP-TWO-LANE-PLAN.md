# MVP Two-Lane Validation Plan

Status: executed
Dispatch ID: `ide-ergonomics-mvp-two-lane-20260619T172822Z`

## Objective

Understand whether the current IDE Ergonomics MVP is the most valid first proof,
instead of simply elaborating the first attractive idea.

Current MVP candidate:

1. Candidate definition action.
2. Handoff composer popup.
3. Subagent fanout preview.

Underlying problem:

> Arcanum has strong workflow contracts, but users must manually notice when a
> conversation should become a definition, handoff, route, side node, or
> delegated run.

## Lane Z: MVP Validator

Lane Z takes the current three-card MVP seriously and tries to make it work.
Then it must attack that MVP with at least one realistic counterexample.

Required outputs:

- strongest version of the three-card MVP;
- realistic toy scenario;
- at least one counterexample;
- failure interpretation;
- repaired MVP, if repair is possible;
- score against the shared criteria.

Key question:

> If this MVP fails, what does it fail to prove?

## Lane A: Alternative Angles

Lane A holds the underlying problem fixed and proposes different first proofs.
It must not propose a renamed version of the same three-card MVP.

Candidate angles to explore:

- definition-only MVP;
- handoff-first MVP;
- bounded route-menu MVP;
- side-node capture MVP;
- evidence rail MVP;
- generated host-rules package before IDE UI;
- Knowledge Graph side-panel proof.

Required outputs:

- at least two alternatives;
- rejected alternatives and why;
- strongest challenge to the current MVP;
- score against the shared criteria.

Key question:

> Which first proof validates the underlying problem with the least surface area?

## Shared Criteria

| Criterion | What Good Looks Like |
| --- | --- |
| Value signal | A user can feel the workflow improvement quickly. |
| Proof cost | The proof can fail cheaply without building a full IDE plugin. |
| Boundary safety | The proof does not silently promote definitions, spells, sigils, ontology, or runtime behavior. |
| Owner clarity | Each action has a clear Arcanum owner. |
| Implementation surface | The proof is small enough for one bounded `task-session`. |
| Recomposition | If it passes, it naturally composes into the larger IDE Action Surface vision. |

## Adjudication Outcomes

The parent synthesis should choose one:

- keep the three-card MVP;
- narrow it to one card;
- replace it with an alternative angle;
- run a second small toy validation;
- defer because no candidate dominates.

## Dispatch Artifact

Validated route:

- [MVP-TWO-LANE-DISPATCH.json](MVP-TWO-LANE-DISPATCH.json)

Execution artifacts:

- [LANE-RECEIPTS.md](LANE-RECEIPTS.md)
- [research.md](research.md)
- [findings.md](findings.md)
- [MVP-TWO-LANE-SYNTHESIS.md](MVP-TWO-LANE-SYNTHESIS.md)
- [MVP-NEXT-HANDOFF.md](MVP-NEXT-HANDOFF.md)
