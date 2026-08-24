# Fresh Plan Distill Review Strategy

## P1 Trigger

Dispatch is warranted by synthesis, isolation, context protection, and
parallelism. The target spans 19 SWUs, four machine inventories, six task
contracts, six waves, 24 Design witnesses, prior verified findings, and
cross-artifact exactness that should be independently attacked.

## Type And Budget

- Dispatch type: `review`
- Distill mode: `validate`
- Budget: one Proposer/Balancer round, one synthesis, one bounded verifier
  zig-zag, one coverage audit
- Deliverable: verified remaining change requests or PASS
- Out of scope: product mutation/tests, SWU selection, Craft, human study,
  release, deployment

## Lanes, Subagents, And Tension

| Group | Mode/purpose | Agents and angles |
| --- | --- | --- |
| proposer-balancer | parallel + robot talks; `methodology` axis | Abramsky — affirmative formal closure/recomposition; Rittel — adversarial execution/hidden-dependency falsification |
| synthesizer | sequential | Noether — cited deduplication and candidate verdict |
| verifier | bounded zig-zag | Schön — literal refutation and read-only checks |
| coverage-auditor | sequential final coverage | Brandenburg — denominator and zero-findings audit |

Predicted disagreement: Abramsky’s affirmative contract proof may accept a
repair whose declared parts line up; Rittel’s adversarial execution simulation
should expose any latent forward dependency, impossible path state, or
acceptance/closeout gap.

## Dependency Flow

```text
proposer-balancer
  -> synthesizer
      <-> verifier (loop cap 1)
            -> coverage-auditor
                  -> parent final approval
```

## Inventory Preflight

- Machine index: current, parse/projection validation PASS,
  `lookup_readiness=ready`.
- Selected: verified Studio architecture/deep-spec review, verified interface
  review, verified split Invoke Plan precedent.
- Excluded: candidate strategies, other-product frontend plans, historical
  Studio plans as authority.
- Concrete effect: the review explicitly attacks 19-unit closure, current
  selector evidence, claim ceilings, first-unit narrowness, and receipt-driven
  closeout.
- Residue: 91 uncontrolled-tag warnings; concurrent unrelated Inventory edits
  prevent a safe post-result Inventory write.
- Authority: Inventory is discovery-only.

## Gate And Ledger State

- Candidate schema: 0.7.0.
- Form validation: pass, schema 0.7.0, digest
  `26fdb030f425635a5ec4373d794113ccc7ec280aad9ff7af41bff551ee59d8df`,
  ledger mutation none.
- Check-tension: PASS / PASS on that exact digest; no apontamentos.
- Human confirmation: required after both gates.
- Registration: not appended.
- Execution: not started.
- Closeout expectation: exactly one dispatch row and one close row if
  confirmed/run.

## Next Human Action

Confirmation readiness is now complete. The required action is the exact word
`confirmed`, a sheet revision request, or decline.
