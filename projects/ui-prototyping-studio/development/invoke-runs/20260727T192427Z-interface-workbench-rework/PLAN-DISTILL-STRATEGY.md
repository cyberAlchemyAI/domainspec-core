# Plan Distill Review Strategy

## P1 Trigger

Dispatch is warranted by synthesis, isolation, context protection, and
parallelism. The draft spans 17 SWUs, six task contracts, six waves, shared
context, layering, choreography, closeout synchronization, and 24 witness
contracts. A Proposer and Balancer must independently test closure versus split
pressure before synthesis and verification.

## Type And Budget

- Dispatch type: `review`
- Distill mode: `validate`
- Recursive budget: one proposal/balance round plus one bounded verifier
  zig-zag
- Deliverable: verified Plan change requests and Plan Distill gate
- Not included: source implementation, SWU selection, Craft mutation, human
  study, release, or deployment

## Groups

| Group | Purpose | Agents |
| --- | --- | --- |
| proposer-balancer | parallel whole-plan Distill roles with robot talks on the `methodology` axis | Abramsky, Samson — affirmative closure/recomposition Proposer; Rittel, Horst — adversarial split/hidden-glue/task-shape Balancer |
| synthesizer | single writer of cited Plan change requests and candidate verdict | Noether, Emmy |
| verifier | literal falsification of every candidate finding and Plan ceiling | Schön, Donald |
| coverage-auditor | denominator coverage and accept/reject recommendation | Brandenburg, Martin |

Predicted disagreement: Abramsky runs formal closure and recomposition
analysis, Rittel runs adversarial split falsification on the methodology axis;
a closure-preservation bias in Abramsky would be exposed by Rittel. Abramsky
owns only affirmative closure and recomposition proof. Rittel owns
independent-child splitting, hidden-glue detection, and task-shape attack.

## Dependency Flow

```text
proposer-balancer
  -> synthesizer
      <-> verifier (one bounded zig-zag)
            -> coverage-auditor
```

- `max_loops: 1`
- verifier zig-zag cap: `1`
- final approver: parent

## Inventory Preflight

- Status: ready from machine index.
- Selected: verified Studio architecture-plan review, verified split Invoke
  Plan precedent, and verified current interface audit.
- Excluded: candidate plans, other-product frontend work-packs, and historical
  Studio plans as executable authority.
- Concrete effect: first-unit narrowness, uniquely owned SWUs, receipt
  synchronization, current selector evidence, and claim ceilings are explicit
  attack targets.
- Gaps: no current Plan Distill, witnesses unexecuted, no SWU selected, shared
  Inventory write conflict.
- Authority: discovery only.

## Outputs And Gate

Working folder:
`projects/ui-prototyping-studio/development/invoke-runs/20260727T192427Z-interface-workbench-rework/plan-distill-review/`

- `attacks.md`
- `findings.md`
- `COVERAGE-AUDIT.md`
- parent-updated `PLAN-DISTILL.md`

Registration and execution require current form validation, double PASS
check-tension on the exact sheet digest, and a fresh explicit human
confirmation. Closeout appends one dispatch row and one close row.

Current gate state:

- schema `0.7.0` form validation: pass
- admitted sheet SHA-256:
  `b87f572614b9b312bb34709ba2613b171677bf6fdc2d664d6373c4237b4ab192`
- independent tension checks: PASS / PASS
- human confirmation:
  `human-confirmation:chat:20260727-plan-distill`
- registration: appended
- execution: completed
- review verdict: BLOCK with nine MAJOR and one MINOR verified findings
- coverage audit: ACCEPT
- closeout: appended with `exit_reason: resolved`; five agents; one loop
