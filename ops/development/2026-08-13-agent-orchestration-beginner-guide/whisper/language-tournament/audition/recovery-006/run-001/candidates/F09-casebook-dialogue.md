# F09 — Casebook spine × decision dialogue

## Candidate card

- Design claim: each route can use its clearest short exchange while a repeated causal question provides continuity across otherwise independent cases.
- Casebook spine: support release, newsroom evidence desk, and theatre maintenance handoff.
- Repeated question: **What changed, and what still has not?**
- Proposer evidence: each exchange exposes one tempting leap, then hands the unresolved judgment to the learner.

## Route 1 sample — opening, two work cards, shared attempt, branch explanation, formal reveal, transfer, claim limit

### Opening

“Customers cannot press **Pay now** on narrow screens,” the support lead says. “I want two agents on it.”

“What second judgment must remain independent?” the release lead asks.

The support lead points to another card: privacy and accessibility reviews for account deletion. “On that card, I can name two.”

What changed between the requests, and what still has not?

### Two work cards and shared attempt

**Card A:** reproduce the button failure and return screenshot, selector, file, and line without editing.

- One investigator returns one evidence report for the lead to inspect before deciding.
- Two reviewers return separate evidence reports for the lead to compare before deciding.

Binding: `choose-one`; values `helper`, `dispatch`; expected `helper`.

**Card B:** keep the deletion privacy and accessibility judgments separate before release.

- One investigator returns one evidence report for the lead to inspect before deciding.
- Two reviewers return separate evidence reports for the lead to compare before deciding.

Binding: `choose-two`; values `helper`, `dispatch`; expected `dispatch`.

Shared action: **Check both decisions**.

### Branch explanation

- Card A, correct: “Yes,” the release lead says. “One bounded diagnosis returns the result I can inspect.”
- Card A, corrective: “Name the second protected judgment,” the lead says. The card contains one cause to trace.
- Card B, correct: “Yes,” the support lead says. “Neither specialist report can answer for the other.”
- Card B, corrective: “One combined judgment would erase the separation,” the release lead says.

### Formal reveal

1. **boundary** — a decision, permission, or responsibility that must stay separate.
2. **bounded helper** — one person with one clearly limited job whose result the parent can inspect.
3. **governed dispatch** — coordinated work with separate roles, checks, and stop points.
4. **authority** — permission to make a change or claim.

What changed? The safeguard and responsible shape. What still has not? Neither card is authorized, recorded, or started merely because a shape was chosen.

### Transfer and claim limit

“The two deletion reports returned,” the support lead says. “Does return make them usable together?” What further relation must hold? Keep `gate` and `receipt` deferred.

`arcanum/arcana/subagent-strategy/SKILL.md` anchors route justification. Reading it does not authorize, register, or execute a route. Lesson: `lesson-choose`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 3 sample — concrete returned-result problem, predecessor attempt, branch explanation, exact nine-state reveal, limit attempt, loop and closeout, claim limit

### Concrete returned-result problem and predecessor attempt

“The fact-check came back,” an editor says. “Schedule publication.”

“Our decision also requires legal and attribution reviews,” the evidence editor replies. “What changed, and what still has not?”

- The request to start has a recorded outcome.
- One returned record matches its expected identity and shape.
- Every required checked record is included in the decision's evidence set.

Binding: `relay-predecessor`; values `host-result`, `receipt-admitted`, `receipt-joined`; expected `receipt-joined`.

### Branch explanation

- Correct: “Yes,” the evidence editor says. “The rule needs all required checked records together.”
- Corrective: “That answer names an earlier fact,” the editor says. “One file is not the complete set.”

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

“The decision passed,” the editor says. “Layout is underway.”

What is still required before a dependent worker can start?

- Nothing; gate passage starts the worker.
- A fresh persisted action plan for the eligible wave.
- Proof that the earlier receipt is semantically true.

Binding: `relay-limit`; values `nothing`, `new-plan`, `truth`; expected `new-plan`.

- Correct: “Right,” the evidence editor says. “Eligibility still needs an exact persisted action.”
- Corrective: “A decision cannot write or execute the layout action,” the editor says.

What changed? Eligibility. What still has not? The next action has not been attempted. The **dependent-work loop** repeats the lifecycle; the **terminal-closeout branch** requires final resolution or explicit stop.

`arcanum/runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl` anchors exact order, not semantic truth. Lesson: `lesson-relay`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 7 sample — concrete handoff, provisional four-link retell, binary attempt, branch explanation, formal mapping, correction and save, claim limit

### Concrete handoff and provisional four-link retell

“The electrical and access reviews support replacing the theatre's aisle lights,” the venue manager says.

“Then the contractor starts,” a coordinator replies.

The maintenance owner opens an empty work-order screen. “From which exact instruction?”

Draft:

1. `exit-situation` / `situation` — received work and checked results.
2. `exit-present` / `present` — decision and present change.
3. `exit-missing` / `missing` — permitted move and missing worker input.
4. `exit-human` / `human` — next owner and remaining limit.

This provisional four-link retell comes before the binary choice.

### Binary start attempt and branch explanation

Planning is permitted, and no downstream worker input exists. Is current evidence sufficient for work to begin?

- Yes — the owner may use the decision as the worker's start instruction.
- No — the owner must prepare a new bounded work record as the worker's start instruction.

Binding: `transfer-start`; values `yes`, `no`; expected `no`.

- Correct: “Yes,” the owner says. “I still must persist an exact bounded action.”
- Corrective: “The decision changed what may be planned,” the manager says. “It did not fill the empty work order.”

### Formal mapping, correction, and save

1. **Receipt** — structured record of an expected result.
2. **Admitted** — expected identity and shape checked.
3. **Joined** — all required admitted results included in the decision set.
4. **Gate** — declared decision rule applied.
5. **Persisted action** — exact saved work record required before a host request.

What changed? Planning eligibility. What still has not? The exact action, start attempt, execution, and result. Preserve provisional four-link retell → binary start attempt → branch explanation → formal mapping → retell correction and save. Local presence and the existing minimum-length rule are machine-checkable; a human reviews meaning.

With expected `no` and four locally sufficient fields, say exactly: **Exit ticket saved; this lesson is complete.** Only lesson `lesson-transfer` closes.

`arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py` anchors the software owner boundary. It provides no missing action or authority.

Stored fields establish local presence only. This sample may teach inference; it does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Guide-wide pattern

Choose the clearest domain-specific exchange for each lesson. Limit it to one tempting claim, one boundary question, and the learner's unresolved decision. Repeat **What changed, and what still has not?** for continuity; retire dialogue at the exact reveal.

## Known risks

- New speakers in every lesson reduce cast recall but require repeated orientation.
- Dialogue can leak correctness through status or tone.
- Quoted exchanges add interaction-like text without actual conversation behavior.
