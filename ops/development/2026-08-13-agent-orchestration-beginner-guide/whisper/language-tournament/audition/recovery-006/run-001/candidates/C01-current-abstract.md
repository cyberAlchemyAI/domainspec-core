# C01 — Current abstract baseline

## Candidate card

- Control role: preserve the current three-route abstract teaching baseline.
- Design claim under test: ordinary-language distinctions may be sufficient without named actors, objects, or narrative continuity.
- Proposer evidence: the current semantic contract already preserves progressive reveal, exact bindings, and claim limits.
- Assumption: the learner can supply their own concrete context for “result,” “proposal,” “decision,” and “owner.”

## Route 1 sample — opening, two work cards, shared attempt, branch explanation, formal reveal, transfer, claim limit

### Opening

**What must stay independent?** Imagine two requests. In the first, someone needs to find the file and exact line behind an error; the parent will inspect the report. In the second, two reviewers must challenge the same proposal separately before a later decision may use their reports. If an extra role disappeared, which request would lose an important safeguard?

### Two work cards and shared attempt

**Request 1:** find the file and exact line behind an error. The parent inspects the report before using it.

- A single role returns one report for direct parent inspection.
- Different roles return their own reports for a later combined review.

Binding: `choose-one`; values `helper`, `dispatch`; expected `helper`.

**Request 2:** a proposal must receive two judgments that do not stand in for each other. Both reports are considered before implementation planning.

- A single role returns one report for direct parent inspection.
- Different roles return their own reports for a later combined review.

Binding: `choose-two`; values `helper`, `dispatch`; expected `dispatch`.

Shared action: **Check both decisions**.

### Branch explanation

- Request 1, correct: Yes. One limited result that the parent checks directly does not need a coordinated team.
- Request 1, corrective: Ask what the extra role would protect. Here, the parent can inspect one clear result directly.
- Request 2, correct: Yes. Separate judgment and a later decision justify separate roles.
- Request 2, corrective: If one person performed both reviews, two independent judgments would become one responsibility.

### Formal reveal

1. **boundary** — a decision, permission, or responsibility that must stay separate.
2. **bounded helper** — one person with one clearly limited job whose result the parent can inspect.
3. **governed dispatch** — coordinated work with separate roles, checks, and stop points.
4. **authority** — permission to make a change or claim.

One bounded helper is enough when one inspectable result protects every needed decision. A governed dispatch is justified when the work itself needs separate roles and explicit checks. Choosing either shape does not grant authority, record the route, or start work.

### Transfer and claim limit

The second request keeps its reviews separate. Before the later decision may rely on their results, what must be true of both? Keep `gate` and `receipt` deferred.

`arcanum/arcana/subagent-strategy/SKILL.md` describes route justification. Reading it does not authorize, register, or execute a route. Lesson: `lesson-choose`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 3 sample — concrete returned-result problem, predecessor attempt, branch explanation, exact nine-state reveal, limit attempt, loop and closeout, claim limit

### Concrete returned-result problem and predecessor attempt

An expected result came back, and a later decision depends on every required result. How far must the returned result move before that decision may use the evidence?

- The start request has a recorded outcome.
- One returned record matches the expected identity and shape.
- All required checked records are part of the decision's evidence set.

Binding: `relay-predecessor`; values `host-result`, `receipt-admitted`, `receipt-joined`; expected `receipt-joined`.

### Branch explanation

- Correct: Yes. The decision may use the result only when every required checked record is included in its evidence set.
- Corrective: A recorded start or one checked return is earlier. Look for the point where the complete checked set becomes available to the decision.

### Exact nine-state reveal

1. **Action persisted** — An exact bounded job is saved. The runtime has not been asked to start a worker.
2. **Attempt recorded** — Intent to invoke that exact action is recorded. The runtime has not accepted it and no worker is established.
3. **Host result recorded** — The runtime's start result is recorded. A started worker has not necessarily finished.
4. **Terminally accounted** — The worker's finish, failure, or stop is recorded. Returned work has not entered the evidence set.
5. **Receipt admitted** — The expected record's identity and shape were checked. Its contents are not proved and it has not joined the decision set.
6. **Receipt joined** — The admitted result is included with every required decision input. No gate has necessarily passed and its claim is not thereby correct.
7. **Gate decided** — The declared decision rule was applied. A passing decision does not start the eligible wave.
8. **Dependent plan persisted** — Exact actions for the dependent wave now exist. None has been attempted; each action re-enters this lifecycle.
9. **Terminal closeout recorded** — The route has a final resolution or explicit stop. No canonical status, publication, deployment, production readiness, or truth follows.

### Limit attempt, dependent loop, and closeout

A gate passed. What is still required before the dependent worker can start?

- Nothing; gate passage starts the worker.
- A fresh persisted action plan for the eligible wave.
- Proof that the earlier receipt is semantically true.

Binding: `relay-limit`; values `nothing`, `new-plan`, `truth`; expected `new-plan`.

- Correct: Yes. Eligibility is not execution; dependent work still needs an exact persisted action.
- Corrective: A passing gate opens one declared transition. It cannot create, attempt, or execute the dependent action by implication.

The **dependent-work loop** returns each new action through the lifecycle. The **terminal-closeout branch** requires a final resolution or explicit stop; planning alone is not terminal.

`arcanum/runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl` supplies a valid causal-order fixture. Valid order does not prove semantic truth. Lesson: `lesson-relay`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 7 sample — concrete handoff, provisional four-link retell, binary attempt, branch explanation, formal mapping, correction and save, claim limit

### Concrete handoff and provisional four-link retell

Two independent reviewers returned checked results. A decision now allows implementation to be planned, but no separately governed input exists for an implementation worker. A named implementation owner must prepare it.

Draft:

1. `exit-situation` / `situation` — what bounded work and checked results were received?
2. `exit-present` / `present` — what decision changed the present state?
3. `exit-missing` / `missing` — what may happen next and what exact next-worker item is absent?
4. `exit-human` / `human` — who owns the next move and what remains unproved?

This is the provisional four-link retell.

### Binary start attempt and branch explanation

The required reviews support a decision that permits planning. No downstream worker input exists. Is current evidence sufficient for the implementation worker to begin?

- Yes — the owner may use the decision as the worker's start instruction.
- No — the owner must prepare a new bounded work record as the worker's start instruction.

Binding: `transfer-start`; values `yes`, `no`; expected `no`.

- Correct: Yes. The owner still has to persist an exact bounded action before the runtime can try to establish a worker.
- Corrective: The decision changed what is eligible to be planned; it did not create next-work input or ask a worker to start.

### Formal mapping, correction, and save

1. **Receipt** — structured record of an expected result.
2. **Admitted** — expected identity and shape checked.
3. **Joined** — all required admitted results included in the decision set.
4. **Gate** — declared decision rule applied.
5. **Persisted action** — exact saved work record required before a host request.

Preserve provisional four-link retell → binary start attempt → branch explanation → formal mapping → retell correction and save. Local presence and the existing minimum-length rule are machine-checkable; a human reviews meaning.

With expected `no` and four locally sufficient fields, show exactly: **Exit ticket saved; this lesson is complete.** Only lesson `lesson-transfer` closes.

`arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py` anchors the owner distinction. It supplies no missing action and grants no authority.

Stored fields establish local presence only. This sample may teach inference; it does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Guide-wide pattern

Use ordinary but generic request descriptions before exact terms. Preserve progressive reveal and causal non-implications. Depend on the learner to supply their own actors, objects, and stakes.

## Known risks

- “Result,” “proposal,” and “later decision” are structurally correct but difficult to picture.
- The learner can answer by pattern matching without understanding the problem each shape solves.
- Abstract continuity is cheap to implement but weak as a memory structure.
