# F01 — Product spine × consequence-first

## Candidate card

- Design claim: one recurring product team can make all three lifecycle distinctions concrete through consequences alone, without asking a metaphor to carry semantics.
- Product spine: Priya leads a Lantern booking-app release; Nora is the affected customer; Imani owns later implementation planning.
- Proposer evidence: each route returns to the same release, but each scene contains only the actors needed for its decision.
- Assumption: a beginner recognizes mobile defects, release review, and work tickets.

## Route 1 sample — opening, two work cards, shared attempt, branch explanation, formal reveal, transfer, claim limit

### Opening

At 3:20 p.m., Priya is preparing Lantern's 4 p.m. release. Nora cannot tap **Reserve** on her phone because a consent banner covers the button. The same release also contains a new account-deletion flow. Someone suggests sending a team of agents at both requests. Priya first asks a different question: what safeguard would disappear if the work were handled by one person?

### Two work cards and shared attempt

**Work card A — find Nora's defect.** Reproduce the hidden button, identify the exact component or style rule, and return a screenshot plus file and line. Do not edit. Priya will inspect one report before deciding what happens next.

Which setup is enough?

- One investigator returns one evidence report for Priya to inspect before deciding.
- Two reviewers return separate evidence reports for Priya to compare before deciding.

Control binding, not visible copy: `choose-one`; values `helper`, `dispatch`; expected `helper`.

**Work card B — review deletion.** One reviewer checks whether stored data is removed as promised. Another checks whether a keyboard or screen-reader user can complete or cancel without being trapped. Priya needs both judgments separately before release.

Which setup preserves the needed safeguard?

- One investigator returns one evidence report for Priya to inspect before deciding.
- Two reviewers return separate evidence reports for Priya to compare before deciding.

Control binding, not visible copy: `choose-two`; values `helper`, `dispatch`; expected `dispatch`.

Shared action: **Check both decisions**.

### Branch explanation

- Work card A, correct: Yes. This request asks for one bounded diagnosis Priya can inspect; another role would not protect a different decision.
- Work card A, corrective: Count the judgments Priya must preserve, not the people available. Here she needs one cause and one inspectable report.
- Work card B, correct: Yes. Data removal and accessible escape protect different parts of the release decision, so neither report may stand in for the other.
- Work card B, corrective: If one person supplies both judgments, Priya can no longer see whether each release safeguard received its own examination.

### Formal reveal

1. A decision, permission, or responsibility that must stay separate is a **boundary**.
2. One person with one clearly limited job whose result the parent can inspect is a **bounded helper**.
3. A coordinated job with separate roles, checks, and stop points is a **governed dispatch**.
4. Permission to make a change or claim is **authority**.

Nora's diagnosis fits a bounded helper. The deletion review fits a governed dispatch. Choosing either shape does not grant permission, record a route, or start work. More agents do not create more authority.

### Transfer and claim limit

Priya kept the deletion reports separate. Before a later decision may rely on them, what must be true of both results? Hold the answer for Route 3; the terms `gate` and `receipt` remain deferred here.

`arcanum/arcana/subagent-strategy/SKILL.md` explains when a multi-agent route is justified. Reading it does not authorize, register, or execute one. Runtime bindings remain under lesson `lesson-choose`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 3 sample — concrete returned-result problem, predecessor attempt, branch explanation, exact nine-state reveal, limit attempt, loop and closeout, claim limit

### Concrete returned-result problem and predecessor attempt

At 10:12 a.m., the accessibility reviewer returns Lantern report `A-17`. Priya's release decision requires that report and the separate data-removal report. Seeing `A-17` in the folder proves that one result came back; it does not tell Priya whether the complete checked set is available to her decision.

Which evidence level must the decision have?

- The request to start has a recorded outcome.
- One returned record matches its expected identity and shape.
- Every required checked record is included in the decision's evidence set.

Control binding, not visible copy: `relay-predecessor`; values `host-result`, `receipt-admitted`, `receipt-joined`; expected `receipt-joined`.

### Branch explanation

- Correct: Yes. Priya may apply the decision rule only when every required checked record is included together.
- Corrective: A start outcome or one checked return is earlier. Look for the point where both required records are available to the same decision.

### Exact nine-state reveal

1. **Action persisted** — The exact review job is saved. The runtime has not been asked to start a worker.
2. **Attempt recorded** — Intent to invoke that job is recorded. The runtime has not accepted it and no worker is established.
3. **Host result recorded** — The runtime's start result is recorded. A started worker has not necessarily finished.
4. **Terminally accounted** — The worker's finish, failure, or stop is recorded. Returned work has not entered the evidence set.
5. **Receipt admitted** — The expected record's identity and shape were checked. Its content is not proved and it has not joined the decision set.
6. **Receipt joined** — The admitted result is included with every required decision input. No gate has necessarily passed and its claim is not thereby correct.
7. **Gate decided** — The declared decision rule was applied. A passing decision does not start the eligible wave.
8. **Dependent plan persisted** — Exact actions for the dependent wave now exist. None has been attempted; each action re-enters this lifecycle.
9. **Terminal closeout recorded** — The route has a final resolution or explicit stop. No canonical status, publication, deployment, production readiness, or truth follows.

### Limit attempt, dependent loop, and closeout

A gate passed. What is still required before Lantern's dependent worker can start?

- Nothing; gate passage starts the worker.
- A fresh persisted action plan for the eligible wave.
- Proof that the earlier receipt is semantically true.

Control binding, not visible copy: `relay-limit`; values `nothing`, `new-plan`, `truth`; expected `new-plan`.

- Correct: Yes. Eligibility is not execution; Imani still needs an exact persisted action.
- Corrective: The decision opens one declared transition. It cannot create, attempt, or execute Imani's action by implication.

**dependent-work loop:** the new action returns through attempt, host result, terminal accounting, admission, join, and its declared gate. **terminal-closeout branch:** only final resolution or an explicit stop reaches closeout; planning alone is not terminal.

`arcanum/runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl` shows one valid causal order. Valid order does not prove semantic truth. Runtime bindings remain under lesson `lesson-relay`.

This sample may teach inference. It does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Route 7 sample — concrete handoff, provisional four-link retell, binary attempt, branch explanation, formal mapping, correction and save, claim limit

### Concrete handoff and provisional four-link retell

Both Lantern review reports are now checked and included in the release decision. The decision permits a repair to be planned. It does not contain Imani's next work ticket, so no implementation worker has an input to start from.

Before deciding whether work can begin, draft four links:

1. In `exit-situation` / `situation`: what bounded reviews and checked results were received?
2. In `exit-present` / `present`: what decision changed the present state?
3. In `exit-missing` / `missing`: what may be planned and what exact next-worker item is absent?
4. In `exit-human` / `human`: who owns the next move and what will that move still leave unproved?

This is the **provisional four-link retell**. No model answer or formal mapping is visible yet.

### Binary start attempt and branch explanation

The required reviews support a decision that permits planning. No downstream worker input exists. Is the evidence sufficient for the implementation worker to begin?

- Yes — the owner may use the decision as the worker's start instruction.
- No — the owner must prepare a new bounded work record as the worker's start instruction.

Control binding, not visible copy: `transfer-start`; values `yes`, `no`; expected `no`.

- Correct: Yes. Imani must persist an exact bounded action before the runtime can try to establish a worker.
- Corrective: The decision changed what is eligible to be planned. It did not create next-work input or ask a worker to start.

### Formal mapping, correction, and save

1. **Receipt** — the structured record of an expected result.
2. **Admitted** — the receipt passed expected identity-and-shape checks.
3. **Joined** — all required admitted results are included in the decision set.
4. **Gate** — the declared decision rule is applied.
5. **Persisted action** — the exact saved work record needed before a host can be asked to start a worker.

Now correct the four-link retell. The interaction order remains provisional four-link retell → binary start attempt → branch explanation → formal mapping → retell correction and save. Local presence and the existing minimum-length rule are machine-checkable; a human reviews meaning.

When the expected `no` and all four locally sufficient fields are present, the local branch may say exactly: **Exit ticket saved; this lesson is complete.** That closes only lesson `lesson-transfer`.

`arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py` anchors the owner connection. Its presence does not supply Imani's missing action and does not authorize this sample to run work.

Stored fields establish local presence only. This sample may teach inference; it does not establish comprehension, semantic truth, authority, execution, route completion, promotion, publication, deployment, production readiness, or transport proof.

## Guide-wide pattern

Reuse one product and only the actors who own the current decision. Begin with the consequence, let the learner act, name the formal distinction, then return to the same release at a later lifecycle boundary. Prefer literal explanation; add no analogy unless a later review finds that the causal relation remains opaque.

## Known risks

- Product familiarity helps software learners but may exclude readers who cannot picture release work.
- Reusing one release strengthens continuity but can make three different controls feel like one long case.
- Without an analogy, some readers may retain the incidents but not the abstract relation across new domains.
