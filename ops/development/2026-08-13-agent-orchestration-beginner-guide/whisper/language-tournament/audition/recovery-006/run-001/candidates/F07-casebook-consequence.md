# F07 — Casebook spine × consequence-first

## Candidate card

- Design claim: each route should use the case that most clearly exposes its own causal distinction; a repeated question supplies continuity without a recurring cast.
- Casebook spine: software defect and review, scholarship evidence, and building-repair handoff.
- Repeated question: **What changed, and what still has not?**
- Proposer evidence: each case minimizes domain explanation and ends by naming the same responsibility split.

## Route 1 sample — opening, two work cards, shared attempt, branch explanation, formal reveal, transfer, claim limit

### Opening

A shop's **Pay now** button fails only on 390-pixel screens. In the same release, account deletion needs a privacy judgment and an accessibility judgment that remain separately visible. What changed between these problems, and what still has not? The first needs a cause; the second needs protected separation. Neither yet has permission to change the product.

### Two work cards and shared attempt

**Card A:** reproduce the narrow-screen failure, return the exact selector, file, line, and screenshot, and make no edit.

- One investigator returns one evidence report for the release lead to inspect.
- Two reviewers return separate evidence reports for the release lead to compare.

Binding: `choose-one`; values `helper`, `dispatch`; expected `helper`.

**Card B:** keep the deletion privacy review and keyboard-access review separate before the release lead decides.

- One investigator returns one evidence report for the release lead to inspect.
- Two reviewers return separate evidence reports for the release lead to compare.

Binding: `choose-two`; values `helper`, `dispatch`; expected `dispatch`.

Shared action: **Check both decisions**.

### Branch explanation

- Card A, correct: Yes. One limited investigation returns the entire inspectable result this decision needs.
- Card A, corrective: A second report does not preserve another required judgment; the problem asks for one traceable cause.
- Card B, correct: Yes. Privacy and accessibility answer different release obligations and must not stand in for each other.
- Card B, corrective: One combined voice would erase the required separation between the two reviews.

### Formal reveal

1. **boundary** — a decision, permission, or responsibility that must stay separate.
2. **bounded helper** — one person with one clearly limited job whose result the parent can inspect.
3. **governed dispatch** — coordinated work with separate roles, checks, and stop points.
4. **authority** — permission to make a change or claim.

What changed? The safeguard the problem needs. What still has not? No shape grants authority, records a route, or starts work.

### Transfer and claim limit

A lab needs one technician to identify a failed sensor, while a grant decision needs two specialist reviews that cannot substitute for each other. Which work shape protects each problem? Keep `gate` and `receipt` deferred.

`arcanum/arcana/subagent-strategy/SKILL.md` connects the distinction to repository work. Reading it does not authorize, register, or execute a route. Lesson: `lesson-choose`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 3 sample — concrete returned-result problem, predecessor attempt, branch explanation, exact nine-state reveal, limit attempt, loop and closeout, claim limit

### Concrete returned-result problem and predecessor attempt

A scholarship committee expects three scored reviews before deciding. One reviewer uploads a correctly named PDF. What changed? One result exists and may pass a shape check. What still has not? The complete checked set is not necessarily available to the committee.

- The request to start has a recorded outcome.
- One returned record matches its expected identity and shape.
- Every required checked record is included in the committee's evidence set.

Binding: `relay-predecessor`; values `host-result`, `receipt-admitted`, `receipt-joined`; expected `receipt-joined`.

### Branch explanation

- Correct: Yes. The committee's rule needs every required checked review included together.
- Corrective: That describes an earlier event. One returned or checked PDF is not the complete decision set.

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

The committee rule passes and makes award-letter preparation eligible. What is still required before the dependent worker can start?

- Nothing; gate passage starts the worker.
- A fresh persisted action plan for the eligible wave.
- Proof that the earlier receipt is semantically true.

Binding: `relay-limit`; values `nothing`, `new-plan`, `truth`; expected `new-plan`.

- Correct: Yes. The eligible work still needs an exact persisted action.
- Corrective: The decision cannot create, attempt, or execute the dependent action by implication.

What changed? One transition became eligible. What still has not? No dependent worker has been asked to start. The **dependent-work loop** returns a new action through attempt, host result, terminal accounting, admission, join, and gate. The **terminal-closeout branch** requires resolution or explicit stop.

`arcanum/runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl` anchors exact software order. Valid order does not prove a review's claim. Lesson: `lesson-relay`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 7 sample — concrete handoff, provisional four-link retell, binary attempt, branch explanation, formal mapping, correction and save, claim limit

### Concrete handoff and provisional four-link retell

A building inspection and accessibility review are checked and included. The owner's decision permits a damaged ramp to be planned for repair. The maintenance manager owns the next move, but no work order names the repair, worker, or evidence to return.

Draft the four links:

1. `exit-situation` / `situation` — received reviews and checked results.
2. `exit-present` / `present` — the decision and what changed.
3. `exit-missing` / `missing` — the permitted plan and missing work order.
4. `exit-human` / `human` — the maintenance manager's move and what remains unproved.

This provisional four-link retell comes before the start judgment.

### Binary start attempt and branch explanation

Planning is permitted. No downstream worker input exists. Is current evidence sufficient for the worker to begin?

- Yes — the owner may use the decision as the worker's start instruction.
- No — the owner must prepare a new bounded work record as the worker's start instruction.

Binding: `transfer-start`; values `yes`, `no`; expected `no`.

- Correct: Yes. The maintenance manager must persist the exact bounded action before a host start request.
- Corrective: The decision made a repair eligible; it did not create the worker's exact input or attempt execution.

### Formal mapping, correction, and save

1. **Receipt** — structured record of an expected result.
2. **Admitted** — expected identity and shape checked.
3. **Joined** — all required admitted results included in the decision set.
4. **Gate** — declared decision rule applied.
5. **Persisted action** — exact saved work record required before a host request.

What changed? Planning eligibility. What still has not? The next action, attempt, execution, and result. Correct the retell in order: provisional four-link retell → binary start attempt → branch explanation → formal mapping → retell correction and save. Local presence and the existing minimum-length rule are machine-checkable; a human reviews meaning.

With expected `no` and four locally sufficient fields, show exactly: **Exit ticket saved; this lesson is complete.** Only lesson `lesson-transfer` closes.

`arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py` connects the case back to runtime ownership. It creates neither the missing action nor authority.

Stored fields establish local presence only. This sample may teach inference; it does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Guide-wide pattern

Choose the clearest literal case for each lesson and repeat one causal question: **What changed, and what still has not?** Use no recurring lore. After the formal reveal, connect the case explicitly to the exact repository surface.

## Known risks

- Three domains reduce lore recall but weaken emotional and narrative continuity.
- A learner may spend effort reorienting to each new setting.
- Case selection becomes an editorial dependency for every remaining lesson.
