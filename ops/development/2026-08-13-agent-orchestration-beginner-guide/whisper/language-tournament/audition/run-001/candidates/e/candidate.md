# Candidate E: worked-example-first language audition

- Dispatch: `2026-08-16-agent-orchestration-language-audition`
- Candidate: `E`
- Movement: example -> noticed tension -> formal term -> general rule -> transfer
- Transport: repository-local interactive guided class
- Status ceiling: audition only; Human Gate A pending
- Intent state: volatile

This artifact proposes language for exactly three moments. It does not rewrite the
seven-route class, alter its interactions, or establish beginner comprehension.

## Moment 1: opening choice

- Source lesson: `#lesson-choose`
- Source moment: `opening_choice`

<!-- BEGIN AUDIENCE COPY: opening_choice -->
<!-- block_id: e.choose.title -->
### One helper or a coordinated team?

<!-- block_id: e.choose.example -->
A parent needs someone to locate the schema that owns a failing field and report
the exact line. The parent will inspect the result. One helper can do that job;
several roles would add handoffs without protecting a new decision.

<!-- block_id: e.choose.tension -->
Now change the example. Two independent reviewers must challenge a proposal.
Implementation may begin only after both results join and a named gate passes.
One person cannot supply two independent judgments, so separate roles protect
something the smaller setup would lose.

<!-- block_id: e.choose.terms -->
### The names for what changed

One helper with one clearly limited job is a **bounded helper**. A coordinated
multi-agent job with separate roles, checks, and stop points is a **governed
dispatch**. The decision, permission, or responsibility that must stay separate is
a **boundary**.

Each expected agent result has a structured record called a **receipt**. A decision
rule that may allow one declared next step is a **gate**; it does not start that
step. **Authority** means permission to make a change or claim. Adding agents does
not add authority.

<!-- block_id: e.choose.rule -->
### A rule you can reuse

Start with one bounded helper when one limited result can be inspected directly.
Use a governed dispatch when the work requires independent judgment,
parallel results, isolated write areas, or a later step that must wait for named
evidence.

<!-- block_id: e.choose.anchor -->
### Connect this example to the repository

`arcanum/arcana/subagent-strategy/SKILL.md` describes the dispatch trigger,
material confirmation, and lifecycle boundaries. Choosing a shape does not
authorize, register, or execute it. More agents create more explicit
boundaries, not more authority.

<!-- block_id: e.choose.question_one -->
### Try the first decision

**What is the smallest responsible shape?**

- One bounded helper
- A governed multi-agent dispatch

If the choice is correct: Yes. One bounded, inspectable result does not yet justify
a dispatch.

If the choice is incorrect: Look for a real need for independent judgment,
parallelism, isolation, or dependent gates. None is present here.

<!-- block_id: e.choose.question_two -->
### Try the changed decision

**What shape does this task require?**

- One bounded helper
- A governed multi-agent dispatch

If the choice is correct: Right. Independence plus a dependent gate justifies the
governed route.

If the choice is incorrect: One helper would collapse independent review and the
dependent gate into one responsibility.

<!-- block_id: e.choose.transition -->
### Continue

Next: find the proof →
<!-- END AUDIENCE COPY: opening_choice -->

### Moment 1 bindings and checks

| Field | Preserved value |
| --- | --- |
| Question IDs | `choose-one`, `choose-two` |
| Correct answers | `choose-one=helper`; `choose-two=dispatch` |
| Answer labels | `helper=One bounded helper`; `dispatch=A governed multi-agent dispatch` |
| Repository anchor | `arcanum/arcana/subagent-strategy/SKILL.md` |
| Answer-leak check | Pass: the worked examples supply the distinction before a teaching check, but neither prompt marks an option as correct before selection. |
| Audience-copy words | `367` |
| Baseline combined words | `325` |
| Word-count delta | `+42` |
| Distinct introduced terms | `6` |
| Baseline distinct plan terms | `6` |
| New-term delta | `0` |

- Introduced after need: `authority`, `boundary`, `bounded helper`, `gate`,
  `governed dispatch`, `receipt`.
- Deferred: none from this moment's baseline term set.
- Removed: none from this moment's baseline term set.
- Code-only: none.

## Moment 2: lifecycle tension

- Source lesson: `#lesson-relay`
- Source moment: `lifecycle_tension`

<!-- BEGIN AUDIENCE COPY: lifecycle_tension -->
<!-- block_id: e.relay.title -->
### Follow one saved job without skipping a handoff

<!-- block_id: e.relay.example -->
A parent saves one exact job: ask a reviewer to inspect a proposal and return a
result. At that instant, there is only a saved work ticket. The runtime has not
been called, and no worker has started.

Later, the worker can finish while its result is still unavailable to the decision
that needs it. The result must first be checked, then included with the other
required results. Even a passing decision does not start the next worker. These
small gaps are why the sequence needs distinct states.

<!-- block_id: e.relay.terms -->
### Name each handoff as it becomes necessary

That saved work ticket is a **persisted action**. The runtime that receives the
prepared request and tries to start the worker is the **host**. Its structured
result record is a **receipt**. The remaining formal labels appear at the handoff
where each becomes necessary.

<!-- block_id: e.relay.timeline -->
### Trace the same job through all nine states

1. **Action persisted.** One exact work ticket now binds the role, inputs, outputs,
   and permitted write areas. The host has not been called and no worker has started.
2. **Attempt recorded.** The causal record now says the parent intends to invoke
   this exact action. An attempt is not host acceptance or worker creation.
3. **Host result recorded.** A native worker binding or explicit spawn failure is
   now attributable to the attempt. A started worker has not necessarily
   completed.
4. **Terminally accounted.** **Terminal accounting** records that the worker
   finished, failed, or stopped. Returned work is not yet an admitted or joined
   receipt.
5. **Receipt admitted.** **Admitted** means the expected files, shape, and
   run/action identity were checked and accepted into the evidence set. Referenced
   artifact bytes are not automatically proven, and the receipt has not joined.
6. **Receipt joined.** **Joined** means the admitted result is included in the
   group a decision will evaluate. The gate has not necessarily passed, and the
   content is not semantic truth.
7. **Gate decided.** A **gate** is the declared evidence rule that opens one
   transition or stops it explicitly. A passed gate does not execute dependent
   work; a fresh persisted plan is still required.
8. **Dependent plan persisted.** Exact actions now exist for the newly **eligible
   wave**—tasks allowed to be planned but not yet started. They re-enter the action
   lifecycle rather than flowing directly to closeout.
9. **Terminal closeout recorded.** **Closeout** is the final record of a finished
   or explicitly stopped route. It records the remaining uncertainty or missing
   work—its **residue**—but does not imply canonical status, publication,
   deployment, production, or truth.

**Semantic truth** asks whether a result's actual claim is correct. Lifecycle order
alone cannot prove it.

Dependent work repeats the lifecycle: a newly planned action returns to attempt,
host result, terminal accounting, receipt admission, join, and its declared gate.
Only terminal resolution or an explicit stop reaches closeout. Planning alone is
not a terminal event.

<!-- block_id: e.relay.anchor -->
### Connect this trace to the repository

`arcanum/runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl`
provides a complete public example of the causal order. This lesson compresses a
real wave into one teaching trace. Valid order does not prove semantic truth, and
a passing gate does not execute dependent work.

<!-- block_id: e.relay.question_predecessor -->
### Check the decision's input

**What evidence state must precede the gate decision in this trace?**

- A host result exists
- A receipt was admitted
- Every required receipt was admitted and joined

If the choice is correct: Correct. The gate reduces the declared receipts only
after they have been admitted and joined.

If the choice is incorrect: A host result and receipt admission are earlier
states. The gate consumes joined receipts.

<!-- block_id: e.relay.question_limit -->
### Check what the decision cannot do

**A gate passed. What is still required before the dependent worker can start?**

- Nothing; gate passage starts the worker
- A fresh persisted action plan for the eligible wave
- Proof that the earlier receipt is semantically true

If the choice is correct: Yes. Eligibility is not execution; the dependent work
still needs exact persisted actions.

If the choice is incorrect: A passing gate opens one declared transition. It
cannot create, attempt, or execute the dependent action by implication.

<!-- block_id: e.relay.transition -->
### Continue

Next: read the action →
<!-- END AUDIENCE COPY: lifecycle_tension -->

### Moment 2 bindings and checks

| Field | Preserved value |
| --- | --- |
| Question IDs | `relay-predecessor`, `relay-limit` |
| Correct answers | `relay-predecessor=receipt-joined`; `relay-limit=new-plan` |
| Answer labels | `host-result=A host result exists`; `receipt-admitted=A receipt was admitted`; `receipt-joined=Every required receipt was admitted and joined`; `nothing=Nothing; gate passage starts the worker`; `new-plan=A fresh persisted action plan for the eligible wave`; `truth=Proof that the earlier receipt is semantically true` |
| Lifecycle state order | `Action persisted` -> `Attempt recorded` -> `Host result recorded` -> `Terminally accounted` -> `Receipt admitted` -> `Receipt joined` -> `Gate decided` -> `Dependent plan persisted` -> `Terminal closeout recorded` |
| Repository anchor | `arcanum/runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl` |
| Answer-leak check | Pass: the timeline teaches the distinction before the checks, but option order and feedback do not mark the correct value before selection. |
| Audience-copy words | `683` |
| Baseline combined words | `665` |
| Word-count delta | `+18` |
| Distinct introduced terms | `11` |
| Baseline distinct plan terms | `14` |
| New-term delta | `-3` |

- Introduced after need: `admitted`, `closeout`, `eligible wave`, `gate`, `host`,
  `joined`, `persisted action`, `receipt`, `residue`, `semantic truth`,
  `terminal accounting`.
- Deferred in audience prose: `boundary`, `causal edge`.
- Removed: none; the deferred formal names are represented by their required plain
  relations.
- Code-only: `fixture` appears only inside the exact repository path segment
  `fixtures`.

## Moment 3: transfer reveal

- Source lesson: `#lesson-transfer`
- Source moment: `transfer_reveal`

<!-- BEGIN AUDIENCE COPY: transfer_reveal -->
<!-- block_id: e.transfer.title -->
### A passed review decision is not a running implementation

<!-- block_id: e.transfer.example -->
Scenario: two review receipts were admitted and joined. Their gate passed. The
repository contains no persisted action for the implementation wave.

The reviews changed what may be planned next. They did not create the next job or
ask a worker to begin it. That difference is the part to carry into an unseen
handoff.

<!-- block_id: e.transfer.terms -->
### Name the evidence without enlarging its claim

A **receipt** records one expected agent result. **Admitted** means its identity
and shape were checked; **joined** means it entered the group a decision evaluates.
A **gate** may allow one declared next step, but does not start it. The next worker
still needs a saved work ticket: a **persisted action**.

Remaining uncertainty or missing work is **residue**.
**Semantic truth** asks whether the result's actual claim is correct; stored text
or valid lifecycle order cannot establish it.

<!-- block_id: e.transfer.rule -->
### The general rule

A passing gate allows one declared transition. It does not create, attempt, or
execute the dependent action. The next worker still needs an exact persisted
action.

<!-- block_id: e.transfer.anchor -->
### Connect this handoff to the repository

`arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py` owns receipt
admission and live wave advancement around this gate transition. The source anchor
does not prove the result correct or authorize the next action.

Non-empty fields establish only that text was stored locally. They do not prove
comprehension, independent orchestration ability, authorization, or semantic truth.

<!-- block_id: e.transfer.start_question -->
### Decide whether work may start

**May an implementation worker begin now?**

- Yes; the passing gate starts dependent work
- No; the gate creates eligibility, but an exact action must still be persisted

If the answer is missing or incorrect: The gate creates eligibility. It does not
create or attempt the dependent action.

<!-- block_id: e.transfer.retell -->
### Rebuild the local transition

Use the scenario's evidence to explain four parts without inventing a missing
action.

**Input or situation**

What bounded task and evidence state did you receive?

**Transformation and present state**

What owner-controlled rule changed the state?

**Immediate consequence and missing step**

What became eligible, and what must exist before execution?

**Next owner and later limit**

Who owns the next move, and what would still remain unproved?

If any field contains fewer than eight trimmed characters: Complete all four retell
fields with enough detail for a human reviewer to inspect.

If the answer is correct and all four fields meet the local length check: Saved
locally. The route is complete, but your authored explanation still requires human
review.

Human gate remains: non-empty text proves only that the fields were filled. An
intended-reader review must judge whether your answer preserves state, evidence,
owner, and residue correctly.

<!-- block_id: e.transfer.transition -->
### Continue

Return to lesson 1 ↻
<!-- END AUDIENCE COPY: transfer_reveal -->

### Moment 3 bindings and checks

| Field | Preserved value |
| --- | --- |
| Question ID | `transfer-start` |
| Correct answer | `no` |
| Answer labels | `yes=Yes; the passing gate starts dependent work`; `no=No; the gate creates eligibility, but an exact action must still be persisted` |
| Retell field IDs | `exit-situation`, `exit-present`, `exit-missing`, `exit-human` |
| Repository anchor | `arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py` |
| Answer-leak check | Pass with source-bound premise: the exact scenario states that no action exists, which is evidence required for the taught distinction; the candidate adds no answer label or visual cue before selection. |
| Audience-copy words | `437` |
| Baseline combined words | `322` |
| Word-count delta | `+115` |
| Distinct introduced terms | `7` |
| Baseline distinct plan terms | `9` |
| New-term delta | `-2` |

- Introduced after the worked example: `admitted`, `gate`, `joined`,
  `persisted action`, `receipt`, `residue`, `semantic truth`.
- Deferred in audience prose: `boundary`.
- Removed: none from this moment's baseline term set.
- Code-only: `driver` appears only inside the exact repository path
  `native_dispatch_driver.py`.

## Audition-wide invariants

- Exact lesson IDs, question IDs, option values, correct answers, retell field IDs,
  repository paths, and lifecycle order remain unchanged.
- No command is copied or changed; command surfaces are outside these three moments.
- The worked examples are bounded teaching cases, not universal rules or evidence
  of learner comprehension.
- This audition does not authorize registration, execution, source mutation,
  publication, deployment, production use, or a claim of semantic truth.
- Human Gate A must select, reject, or request revision before any full derivative.
