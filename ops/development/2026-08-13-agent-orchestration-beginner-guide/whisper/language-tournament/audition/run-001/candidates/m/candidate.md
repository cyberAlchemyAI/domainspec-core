# Candidate M — mechanism-first beginner-language audition

- Dispatch: `2026-08-16-agent-orchestration-language-audition`
- Track: M — computational/procedural mechanism first
- Movement: problem → mechanism → formal term → learner action → explicit limit
- Status ceiling: language-audition candidate only; Human Gate A remains pending
- Counting policy: ASCII alphanumeric tokens, including internal apostrophes and hyphens, between each `AUDIENCE_COPY_BEGIN` and `AUDIENCE_COPY_END` marker. The count includes visible prompts, options, and both feedback states; it excludes authoring metadata below the markers.

## Moment 1 — Route 1 opening choice

- Source selector: `#lesson-choose`
- Source slice: lines `1263-1334`, SHA-256 `50387744892beca209f79f92f73a55d73e4e2c63682355aa07e1fe05b01b74f7`
- Meaning that must survive: choose the smallest responsible shape by asking which real decision needs separation; shape does not create authority or start work.

AUDIENCE_COPY_BEGIN opening_choice

### Protect the decision before you add agents

More agents add more handoffs. Start by asking what must stay separate: a decision, a permission, or a responsibility. If one worker can return one clear result and the parent can inspect it directly, extra roles do not protect anything new.

That needed separation is a **boundary**. One worker with one clearly limited job is a **bounded helper**. A coordinated multi-agent job with separate roles, checks, and stop points is a **governed dispatch**.

Use a bounded helper when one inspectable answer is enough. Use a governed dispatch when the task itself requires independent viewpoints, producer and reviewer separation, parallel results, a dependent decision, or isolated write areas.

**Authority** means permission to make a change or claim. Choosing either shape does not grant authority, register the work, or start it.

#### Connect this lesson to the repository

`arcanum/arcana/subagent-strategy/SKILL.md` describes when a multi-agent route is justified, when material confirmation is needed, and which lifecycle separations must remain visible. Reading that file does not authorize, register, or execute a route.

#### Scenario 1

A parent needs one helper to locate the schema that owns a failing field and report the exact line. The parent will inspect the result.

**What is the smallest responsible shape?**

- One bounded helper
- A governed multi-agent dispatch

**Correct feedback:** Yes. One bounded, inspectable result does not yet justify a dispatch.

**Incorrect feedback:** Look for a real need for independent judgment, parallelism, isolation, or a dependent decision. None is present here.

#### Scenario 2

Two reviewers must challenge a proposal independently. Implementation may begin only after both written results are included in a named decision and that decision allows the next step.

**What shape does this task require?**

- One bounded helper
- A governed multi-agent dispatch

**Correct feedback:** Right. Independent review plus a dependent decision justifies the governed route.

**Incorrect feedback:** One helper would combine independent review and the dependent decision in one responsibility.

Next, learn what must happen to a returned result before a later decision can use it.

AUDIENCE_COPY_END opening_choice

### Moment 1 bindings and checks

- Question `choose-one`: options retain answer IDs `helper` and `dispatch`; correct answer remains `helper`.
- Question `choose-two`: options retain answer IDs `helper` and `dispatch`; correct answer remains `dispatch`.
- Introduced terms: `boundary`, `bounded helper`, `governed dispatch`, `authority`.
- Deferred terms: `gate`, `receipt` (their mechanisms are taught before their names in later lessons).
- Removed plan terms: none.
- Code-only terms: `lesson-choose`, `choose-one`, `choose-two`, `helper`, `dispatch`.
- Answer-leak check: pass. The primer supplies a decision procedure, but neither scenario names its answer or repeats an option label as a clue.
- Learner-facing word count: `337`; baseline combined visible and interaction count: `325`; delta: `+12`.
- Distinct plan terms in learner copy: `4`; baseline distinct plan terms: `6`; new-term delta: `-2`.

## Moment 2 — Route 3 lifecycle tension

- Source selector: `#lesson-relay`
- Source slice: lines `1417-1520`, SHA-256 `c2fd438a2d432ad0b30aaa47a44fe3922f03e1304f0bad620b733aebf4361402`
- Meaning that must survive: each recorded state proves one change and leaves a specific limit; admission, join, gate passage, execution, and closeout never collapse into one another.

AUDIENCE_COPY_BEGIN lifecycle_tension

### Follow one job; do not skip a state

A result can look finished while the workflow is not ready for its next step. Track two things at every stop: what changed, and what still has not happened. Never let one state stand in for the next.

The route has already been chosen, confirmed, validated, and checked for host use. Now one work ticket moves through nine states.

1. **Save the exact job. Formal state: Action persisted.** A **persisted action** is a saved work ticket that binds the role, inputs, outputs, and write limits. The runtime has not been asked to start a worker.
2. **Record the request. Formal state: Attempt recorded.** The parent records an intention to invoke that exact action. The runtime has not accepted it and no worker is established yet.
3. **Record what the runtime did. Formal state: Host result recorded.** The **host** is the runtime that receives the prepared request and tries to start the worker. A started worker has not necessarily finished.
4. **Record how the worker ended. Formal state: Terminally accounted.** **Terminal accounting** records that the worker finished, failed, or stopped. Returned work has not yet entered the evidence set.
5. **Check the returned record. Formal state: Receipt admitted.** A **receipt** is a structured record of one expected agent result. **Admitted** means its expected files, shape, and run and action identity were checked before it entered the evidence set. Its referenced contents are not thereby proved, and it has not joined the decision set.
6. **Add the checked record to the decision set. Formal state: Receipt joined.** **Joined** means the admitted result can participate with the other required results. No decision has necessarily passed, and the result's actual claim is not thereby correct.
7. **Apply the declared decision rule. Formal state: Gate decided.** A **gate** is a rule that may allow one declared next step. A passing gate does not start that step. The tasks it now allows to be planned form an **eligible wave**; they are not running.
8. **Save exact jobs for that wave. Formal state: Dependent plan persisted.** The dependent actions now exist, but none has been attempted. Each returns to the beginning of this lifecycle.
9. **Record a final resolution or explicit stop. Formal state: Terminal closeout recorded.** **Closeout** is the final record of a finished or explicitly stopped route. It does not imply canonical status, publication, deployment, production readiness, or truth.

#### Connect this lesson to the repository

`arcanum/runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl` supplies one complete public example of the required order. A valid order does not prove that the returned claims are correct, and a passing gate does not execute dependent work.

#### Check the transition

**What evidence state must precede the gate decision in this trace?**

- A host result exists
- A receipt was admitted
- Every required receipt was admitted and joined

**Correct feedback:** Correct. The gate reduces the declared receipts only after they have been admitted and joined.

**Incorrect feedback:** A host result and receipt admission are earlier states. The gate consumes joined receipts.

**A gate passed. What is still required before the dependent worker can start?**

- Nothing; gate passage starts the worker
- A fresh persisted action plan for the eligible wave
- Proof that the earlier receipt is semantically true

**Correct feedback:** Yes. Eligibility is not execution; the dependent work still needs exact persisted actions.

**Incorrect feedback:** A passing gate opens one declared transition. It cannot create, attempt, or execute the dependent action by implication.

Next, inspect the saved action that keeps every owner and write limit attached to the same job.

AUDIENCE_COPY_END lifecycle_tension

### Moment 2 bindings and checks

- Timeline state order remains exactly: `Action persisted` → `Attempt recorded` → `Host result recorded` → `Terminally accounted` → `Receipt admitted` → `Receipt joined` → `Gate decided` → `Dependent plan persisted` → `Terminal closeout recorded`.
- Question `relay-predecessor`: option IDs remain `host-result`, `receipt-admitted`, and `receipt-joined`; correct answer remains `receipt-joined`.
- Question `relay-limit`: option IDs remain `nothing`, `new-plan`, and `truth`; correct answer remains `new-plan`.
- Introduced or explicitly redefined terms: `persisted action`, `host`, `terminal accounting`, `receipt`, `admitted`, `joined`, `gate`, `eligible wave`, `closeout`.
- Deferred terms: `causal edge`, `residue`, `semantic truth` (their plain questions carry the meaning here).
- Removed from the visible explanation: `boundary` (already taught in Moment 1 and not needed to follow the sequence).
- Code-only terms: `lesson-relay`, `relay-predecessor`, `relay-limit`, option IDs, and `fixture` as a segment of the exact repository path.
- Answer-leak check: pass. The timeline teaches the rule that the questions ask learners to apply, but neither question embeds the correct option ID or marks an option as correct.
- Learner-facing word count: `596`; baseline combined visible and interaction count: `665`; delta: `-69`.
- Distinct plan terms in learner copy: `9`; baseline distinct plan terms: `14`; new-term delta: `-5`.

## Moment 3 — Route 7 transfer reveal

- Source selector: `#lesson-transfer`
- Source slice: lines `1856-1936`, SHA-256 `a34f706b64038a5985cb0c528488c485579b700d3bafa5e9ff1a8917810dd24a`
- Meaning that must survive: rebuild the local handoff as input, state change, immediate consequence, and later owner or limit; a passing gate creates eligibility, not an implementation action.

AUDIENCE_COPY_BEGIN transfer_reveal

### Use four questions to find the next missing action

You do not need to retell the whole runtime. Start with the evidence you were given, identify the rule that changed the state, name what may happen next, and stop at the first missing step.

**Scenario:** Two review receipts were admitted and joined. Their gate passed. The repository contains no persisted action for the implementation wave.

Here, a **receipt** is a structured record of one expected result. **Admitted** means it was checked for the expected identity and shape. **Joined** means it was included in the group of results used by the decision. A **gate** may allow one declared next step; it does not start it. A **persisted action** is the saved work ticket required before the host can try to start a worker.

**May an implementation worker begin now?**

- Yes; the passing gate starts dependent work
- No; the gate creates eligibility, but an exact action must still be persisted

**Incorrect feedback:** The gate creates eligibility. It does not create or attempt the dependent action.

Now rebuild the handoff in four parts. The prompts give you a structure, not a model answer.

**Input or situation**

What bounded task and checked evidence state did you receive?

**Transformation and present state**

What owner-controlled rule changed the state?

**Immediate consequence and missing step**

What became eligible, and what saved action must exist before execution?

**Next owner and later limit**

Who owns the next move, and what would still remain unproved?

**Incomplete-ticket feedback:** Complete all four retell fields with enough detail for a human reviewer to inspect.

**Saved-ticket feedback:** Saved locally. The route is complete, but your authored explanation still requires human review.

#### Connect this lesson to the repository

`arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py` is the **driver**: repository code that prepares host requests, records returned results, admits receipts, and advances live waves around this decision point. The file's existence does not prove that this scenario has a missing action supplied.

Saving non-empty text proves only that the browser stored text locally. It does not prove comprehension, independent orchestration ability, authorization, or that the explanation is correct.

Save the exit ticket for human review, or return to Lesson 1 and test the method on another task shape.

AUDIENCE_COPY_END transfer_reveal

### Moment 3 bindings and checks

- Question `transfer-start`: answer IDs remain `yes` and `no`; correct answer remains `no`; both visible answer labels remain exact.
- Retell fields preserve IDs and names: `exit-situation` / `situation`, `exit-present` / `present`, `exit-missing` / `missing`, and `exit-human` / `human`.
- Conditional feedback preserves all three source conditions: incorrect start answer, incomplete fields, and correct answer plus four locally sufficient fields.
- Introduced term: `driver`.
- Reused with a brief definition: `receipt`, `admitted`, `joined`, `gate`, `persisted action`.
- Deferred terms: `residue`, `semantic truth` (plain limits carry their meaning).
- Removed from the visible explanation: `boundary` (the local decision point is described directly).
- Code-only terms: `lesson-transfer`, `transfer-start`, answer IDs, retell field IDs/names, and the exact repository path.
- Answer-leak check: pass. The scenario provides the evidence state but not the answer; the mechanism explains why eligibility cannot substitute for the missing action. No retell prompt supplies a completed field.
- Learner-facing word count: `373`; baseline combined visible and interaction count: `322`; delta: `+51`.
- Distinct plan terms in learner copy: `6`; baseline distinct plan terms: `9`; new-term delta: `-3`.

## Candidate-wide claim boundary

This candidate changes only proposed language for three representative moments. It preserves lesson and question identities, correct answers, repository paths, ownership separations, lifecycle order, and the source claim ceilings. It does not establish beginner comprehension, candidate voice fitness, transport proof, canonical status, authorization, publication, deployment, production readiness, or semantic truth.
