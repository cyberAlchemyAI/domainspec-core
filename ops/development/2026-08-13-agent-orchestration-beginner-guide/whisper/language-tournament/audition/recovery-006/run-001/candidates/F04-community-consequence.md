# F04 — Community spine × consequence-first

## Candidate card

- Design claim: one familiar community-hall operation can make responsibility visible without software knowledge, then transfer each distinction back to agent work.
- Community spine: Salma coordinates Riverside Community Hall; Jo maintains the building; Ren owns approved follow-on work.
- Proposer evidence: physical objects and public consequences remain concrete across diagnosis, evidence ordering, and owner handoff.
- Assumption: the software transfer sentence is enough to reconnect everyday responsibility to orchestration.

## Route 1 sample — opening, two work cards, shared attempt, branch explanation, formal reveal, transfer, claim limit

### Opening

Riverside Community Hall opens in two hours. The projector will not power on, and the weekend reopening plan still needs both a fire-exit review and a wheelchair-access review. Salma has volunteers available, but adding people is useful only when a responsibility must remain separate.

### Two work cards and shared attempt

**Card A:** Jo must test the socket and cable, photograph the failed part, and report the exact fault. Salma inspects that one diagnosis before approving a repair.

- One investigator returns one evidence report for Salma to inspect before deciding.
- Two reviewers return separate evidence reports for Salma to compare before deciding.

Binding: `choose-one`; values `helper`, `dispatch`; expected `helper`.

**Card B:** one reviewer checks that emergency exits remain clear; another checks that wheelchair users can enter and leave. Salma needs both judgments separately before reopening.

- One investigator returns one evidence report for Salma to inspect before deciding.
- Two reviewers return separate evidence reports for Salma to compare before deciding.

Binding: `choose-two`; values `helper`, `dispatch`; expected `dispatch`.

Shared action: **Check both decisions**.

### Branch explanation

- Card A, correct: Yes. Salma needs one inspectable fault report; a second role would not protect another required judgment.
- Card A, corrective: Ask what separation the extra person would preserve. This card contains one bounded diagnosis.
- Card B, correct: Yes. Fire-exit safety and wheelchair access are distinct responsibilities, so both examinations must remain visible.
- Card B, corrective: One combined review would hide whether each responsibility received its own judgment.

### Formal reveal

1. **boundary** — a decision, permission, or responsibility that must stay separate.
2. **bounded helper** — one person with one clearly limited job whose result the parent can inspect.
3. **governed dispatch** — coordinated work with separate roles, checks, and stop points.
4. **authority** — permission to make a change or claim.

Jo's diagnosis fits a bounded helper. The reopening reviews fit a governed dispatch. The same question applies in software: which decision would become unsafe or unreadable if roles were combined? Work shape alone grants no authority and starts no work.

### Transfer and claim limit

Both reopening reviews later arrive. Before Salma can use them together, what must be true of the complete checked set? Keep `gate` and `receipt` deferred.

`arcanum/arcana/subagent-strategy/SKILL.md` describes the software route boundary. Reading it does not authorize, register, or execute a route. Lesson: `lesson-choose`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 3 sample — concrete returned-result problem, predecessor attempt, branch explanation, exact nine-state reveal, limit attempt, loop and closeout, claim limit

### Concrete returned-result problem and predecessor attempt

The fire-exit review comes back in a signed PDF. Salma's reopening decision also requires the access review. A file on her desk is not yet the complete evidence set.

- The request to begin has a recorded outcome.
- One returned record matches its expected identity and shape.
- Every required checked record is included in the reopening decision's evidence set.

Binding: `relay-predecessor`; values `host-result`, `receipt-admitted`, `receipt-joined`; expected `receipt-joined`.

### Branch explanation

- Correct: Yes. Salma needs every required checked record included together before applying the reopening rule.
- Corrective: A start outcome or one checked review is earlier. The decision needs the complete checked set.

### Exact nine-state reveal

1. **Action persisted** — An exact bounded review job is saved. The runtime has not been asked to start a worker.
2. **Attempt recorded** — Intent to invoke the exact job is recorded. The runtime has not accepted it and no worker is established.
3. **Host result recorded** — The runtime's start result is recorded. A started worker has not necessarily finished.
4. **Terminally accounted** — The worker's finish, failure, or stop is recorded. Returned work has not entered the evidence set.
5. **Receipt admitted** — The expected record's identity and shape were checked. Its contents are not proved and it has not joined the decision set.
6. **Receipt joined** — The admitted result is included with every required decision input. No gate has necessarily passed and its claim is not thereby correct.
7. **Gate decided** — The declared decision rule was applied. A passing decision does not start the eligible wave.
8. **Dependent plan persisted** — Exact actions for the dependent wave now exist. None has been attempted; each action re-enters this lifecycle.
9. **Terminal closeout recorded** — The route has a final resolution or explicit stop. No canonical status, publication, deployment, production readiness, or truth follows.

### Limit attempt, dependent loop, and closeout

The reopening decision permits a repair to be planned. What is still required before Ren's dependent worker can start?

- Nothing; gate passage starts the worker.
- A fresh persisted action plan for the eligible wave.
- Proof that the earlier receipt is semantically true.

Binding: `relay-limit`; values `nothing`, `new-plan`, `truth`; expected `new-plan`.

- Correct: Yes. Ren still needs the exact saved action; eligibility is not execution.
- Corrective: The reopening decision changes what may be planned. It cannot create or execute the next job.

The **dependent-work loop** returns the new action through attempt, host result, terminal accounting, admission, join, and its gate. The **terminal-closeout branch** requires resolution or explicit stop; a repair plan is not terminal.

`arcanum/runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl` transfers this ordering back to software evidence. Order does not prove truth. Lesson: `lesson-relay`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 7 sample — concrete handoff, provisional four-link retell, binary attempt, branch explanation, formal mapping, correction and save, claim limit

### Concrete handoff and provisional four-link retell

The two hall reviews are checked and included. The reopening decision permits an exit-light repair to be planned. Ren owns that next move, but no exact repair ticket exists for a worker.

Draft four links:

1. `exit-situation` / `situation` — received reviews and checked results.
2. `exit-present` / `present` — reopening decision and current change.
3. `exit-missing` / `missing` — permitted repair planning and absent worker ticket.
4. `exit-human` / `human` — Ren's ownership and what remains unproved.

The provisional four-link retell comes first.

### Binary start attempt and branch explanation

The decision permits planning. No downstream worker input exists. Is current evidence sufficient for the worker to begin?

- Yes — the owner may use the decision as the worker's start instruction.
- No — the owner must prepare a new bounded work record as the worker's start instruction.

Binding: `transfer-start`; values `yes`, `no`; expected `no`.

- Correct: Yes. Ren must persist the exact bounded action before a host can be asked to establish a worker.
- Corrective: The decision did not create the repair ticket or ask a worker to start.

### Formal mapping, correction, and save

1. **Receipt** — structured record of an expected result.
2. **Admitted** — expected identity and shape checked.
3. **Joined** — all required admitted results included in the decision set.
4. **Gate** — declared decision rule applied.
5. **Persisted action** — exact saved work record required before a host request.

Correct the retell after the mapping. Preserve provisional four-link retell → binary start attempt → branch explanation → formal mapping → retell correction and save. Local presence and the existing minimum-length rule are machine-checkable; a human reviews meaning.

On expected `no` and four locally sufficient fields, show exactly: **Exit ticket saved; this lesson is complete.** This closes only lesson `lesson-transfer`.

`arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py` is the software connection. Its presence supplies neither Ren's missing action nor execution authority.

Stored fields establish local presence only. This sample may teach inference; it does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Guide-wide pattern

Use one familiar place and carry responsibility forward: Salma decides, Jo diagnoses, Ren owns the eligible next move. At each route, state the everyday consequence first, reveal exact software vocabulary after the attempt, and add one explicit sentence transferring the relation back to agent work.

## Known risks

- Everyday operations can feel safer than software and understate repository-specific failure modes.
- The explicit software transfer adds a second abstraction step at every route.
- Fire and access examples require care so teaching does not imply professional safety assessment.
