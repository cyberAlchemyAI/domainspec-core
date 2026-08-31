# C02 — Minimal concrete baseline

## Candidate card

- Control role: add names, objects, and consequences without recurring story, dialogue, or analogy.
- Design claim under test: minimum concrete nouns may solve the abstraction problem at lower cost than a narrative architecture.
- Proposer evidence: every route names an actor, artifact, consequence, and decision in two or three sentences.
- Assumption: continuity is optional when each lesson is independently concrete.

## Route 1 sample — opening, two work cards, shared attempt, branch explanation, formal reveal, transfer, claim limit

### Opening

Mara owns a billing release. One customer receives a blank invoice PDF. Separately, the new refund flow needs an amount-accuracy review and a keyboard-access review before release. Mara must choose the smallest setup that preserves each needed decision.

### Two work cards and shared attempt

**Card A:** reproduce invoice `842`, identify the template file and failing line, and return the broken PDF. Do not edit.

- One investigator returns one evidence report for Mara to inspect.
- Two reviewers return separate evidence reports for Mara to compare.

Binding: `choose-one`; values `helper`, `dispatch`; expected `helper`.

**Card B:** keep amount accuracy and keyboard access as separate review reports before Mara's release decision.

- One investigator returns one evidence report for Mara to inspect.
- Two reviewers return separate evidence reports for Mara to compare.

Binding: `choose-two`; values `helper`, `dispatch`; expected `dispatch`.

Shared action: **Check both decisions**.

### Branch explanation

- Card A, correct: Yes. Mara needs one limited cause and one inspectable report.
- Card A, corrective: Another reviewer would add a person but preserve no additional required judgment.
- Card B, correct: Yes. Amount accuracy and keyboard access cannot stand in for each other.
- Card B, corrective: One combined judgment would hide whether both release obligations were examined.

### Formal reveal

1. **boundary** — a decision, permission, or responsibility that must stay separate.
2. **bounded helper** — one person with one clearly limited job whose result the parent can inspect.
3. **governed dispatch** — coordinated work with separate roles, checks, and stop points.
4. **authority** — permission to make a change or claim.

The invoice diagnosis fits a bounded helper; the refund reviews fit a governed dispatch. Neither grants authority or starts work.

### Transfer and claim limit

A lab technician identifies one failed sensor, while two auditors must separately check stock and cash. Which safeguard changes? Keep `gate` and `receipt` deferred.

`arcanum/arcana/subagent-strategy/SKILL.md` anchors route choice. Reading it does not authorize, register, or execute a route. Lesson: `lesson-choose`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 3 sample — concrete returned-result problem, predecessor attempt, branch explanation, exact nine-state reveal, limit attempt, loop and closeout, claim limit

### Concrete returned-result problem and predecessor attempt

Omar's release decision requires review files `A` and `B`. File `A` returns with the expected name and fields. One checked file is not yet the complete evidence set.

- The start request has a recorded outcome.
- One returned record matches the expected identity and shape.
- All required checked records are included in Omar's decision set.

Binding: `relay-predecessor`; values `host-result`, `receipt-admitted`, `receipt-joined`; expected `receipt-joined`.

### Branch explanation

- Correct: Yes. Omar needs both required checked records included together.
- Corrective: A start outcome or one checked file is earlier than the complete set the decision consumes.

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

Omar's decision passes. What is still required before the dependent worker can start?

- Nothing; gate passage starts the worker.
- A fresh persisted action plan for the eligible wave.
- Proof that the earlier receipt is semantically true.

Binding: `relay-limit`; values `nothing`, `new-plan`, `truth`; expected `new-plan`.

- Correct: Yes. The eligible work still needs an exact persisted action.
- Corrective: The decision cannot create, attempt, or execute the next action.

The **dependent-work loop** repeats the lifecycle for each new action. The **terminal-closeout branch** requires final resolution or explicit stop; planning is not terminal.

`arcanum/runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl` anchors exact order, not semantic truth. Lesson: `lesson-relay`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 7 sample — concrete handoff, provisional four-link retell, binary attempt, branch explanation, formal mapping, correction and save, claim limit

### Concrete handoff and provisional four-link retell

Lena receives checked security and accessibility reports. The decision permits a login patch to be planned. Lena owns the next action, but no exact patch work record exists.

Draft:

1. `exit-situation` / `situation` — received reports and checked results.
2. `exit-present` / `present` — decision and present change.
3. `exit-missing` / `missing` — permitted patch planning and missing worker input.
4. `exit-human` / `human` — Lena's next move and remaining limit.

This provisional four-link retell comes first.

### Binary start attempt and branch explanation

Planning is permitted, and no downstream worker input exists. Is current evidence sufficient for the implementation worker to begin?

- Yes — the owner may use the decision as the worker's start instruction.
- No — the owner must prepare a new bounded work record as the worker's start instruction.

Binding: `transfer-start`; values `yes`, `no`; expected `no`.

- Correct: Yes. Lena must persist an exact bounded action before a host start request.
- Corrective: The decision changed eligibility; it did not write the patch action or start a worker.

### Formal mapping, correction, and save

1. **Receipt** — structured record of an expected result.
2. **Admitted** — expected identity and shape checked.
3. **Joined** — all required admitted results included in the decision set.
4. **Gate** — declared decision rule applied.
5. **Persisted action** — exact saved work record required before a host request.

Preserve provisional four-link retell → binary start attempt → branch explanation → formal mapping → retell correction and save. Local presence and the existing minimum-length rule are machine-checkable; a human reviews meaning.

With expected `no` and four locally sufficient fields, say exactly: **Exit ticket saved; this lesson is complete.** Only lesson `lesson-transfer` closes.

`arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py` anchors the owner transfer. It creates neither Lena's missing action nor authority.

Stored fields establish local presence only. This sample may teach inference; it does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Guide-wide pattern

Give each lesson a name, object, consequence, and next decision in the fewest sentences possible. Use no recurring cast, dialogue, or analogy. Preserve exact formal reveal and one changed transfer.

## Known risks

- Minimal concreteness can feel like a sequence of unrelated examples.
- Low narrative investment may weaken recall across seven lessons.
- The control may solve Route 1's abstraction without supplying a guide-wide storytelling architecture.
