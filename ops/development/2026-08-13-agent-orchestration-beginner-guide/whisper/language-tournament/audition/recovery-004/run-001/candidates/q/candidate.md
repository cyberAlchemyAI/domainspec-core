---
schema_version: whisper.language-audition-candidate.v1
candidate_id: agent-orchestration-language-audition-recovery-004-q-fresh
track_id: Q
track_name: diagnostic-question-first
movement: question -> attempt -> explanation -> formal term -> changed next question
transport: repository_local_interactive_guided_class
transport_proof_status: candidate
intent_state: volatile
draft_status: flag
human_gate: pending
scope: three_moment_audition_only
---

# Candidate Q — diagnostic question first

This fresh candidate auditions one movement across three moments: ask a question
that a beginner can approach from ordinary reasoning, let the learner attempt an
answer, explain the practical distinction, introduce only the formal names that
now earn their place, and end with a better next question.

This pack is authoring-only. Only the blockquoted passages are proposed
learner-facing copy. Stage labels, checks, term ledgers, and source bindings must
not be copied into the guided class.

## Exact input bindings

| Input | SHA-256 |
| --- | --- |
| `q-closed-input.json` | `28ade7b4097c68e07414f6c15c890025136a75840fe7a9d002bc84cfa764bf47` |
| `beginner-language-tournament-plan.md` | `5a4fcc97b199e94de133e5cd8d7ad68276e3a45a5de0453e58145005a805bd65` |
| `guided-class.html` | `59d38eff75024ea95028ed8b455e19a1cec9859e9735a035b58ea3f82db75446` |
| `guided-class.lanes.json` | `73164ccf86dfe54ffb8c47db3bc6ffa72e723ff6a8b8e8449ba822ac4dcc0a3a` |
| `guided-class-intent.yaml` | `07587309bc476bc872fe5056922a03102c15041c28ac354766f56dad9a6435fe` |
| `guided-class-validation-r4.json` | `4a04eedf1c252acfc4e32491703a11af0b1707300ee49596445a2ad6351af313` |
| `baseline-manifest.json` | `81030e081a129d35de874a7bf207500d4b03a1c9af62d8eae4e95ccde6f41b8a` |
| `correction-record.yaml` | `76525acd21cb278421a8219fcc1dc229f838af4b324374bd0fd35c51741e4edd` |
| `term-map.yaml` | `e1508119b18afcad6794a4580132c0d87bbeaad5d694a42e5da9061e046098f7` |
| baseline `result.json` | `9956e3e87db2db7cacc38a5dd90c635a9834dee8eab0fb739a01ca2ceb52aba8` |

## Voice and construction rule

The voice is a calm coding instructor who trusts the learner to reason. Each
question carries enough concrete context to avoid a cold quiz, but the setup
does not state the answer. Formal terms appear only in the post-attempt reveal.
The visible movement is:

1. What must stay independent?
2. What has actually been proved?
3. What must exist before the next worker can start?

## Moment 1 — `opening_choice`

Source target: Route 1 opening and the two coordination choices.

Protected bindings: `lesson-choose`; `choose-one=helper`;
`choose-two=dispatch`; both stable question IDs and answer values; the public
repository anchor; the rule that coordination shape grants neither authority
nor execution.

### Audience-facing audition

<!-- AUDIENCE_COPY_OPENING_START -->

**Question — first visible thought**

> **What must stay independent?**

> One request asks someone to find the file and exact line behind an error; the
> parent will inspect the report. Another asks two reviewers to judge the same
> proposal separately before anyone decides whether implementation may be
> planned. If you removed an extra role, which request would lose an important
> safeguard?

**Attempt**

> For each request, choose the smallest setup that keeps every required
> decision separate:
>
> - one person does one clearly limited job, then the parent checks the result;
> - different roles work separately, then a later decision uses their results.

**Feedback before formal names**

> For the file-and-line request, another worker protects no new decision. One
> clear result and direct inspection are enough.

> For the review request, separate judgment is part of the job. If one person
> performed both reviews, the safeguard would disappear.

**Formal-term reveal**

> A decision, permission, or responsibility that must stay separate is a
> **boundary**. One helper with one clearly limited job whose result the parent
> can inspect is a **bounded helper**. A coordinated multi-agent job with
> separate roles, checks, and stop points is a **governed dispatch**.

> Permission to make a change or claim is **authority**. Choosing either setup
> does not grant that permission, record the dispatch, or start the work. More
> agents do not create more authority.

**Changed next question**

> If the second request keeps its reviewers separate, what must be true of
> their results before the later decision may use them?

<!-- AUDIENCE_COPY_OPENING_END -->

### Interaction and feedback mapping

The visible answer labels may become plain-language labels while the protected
values remain `helper` and `dispatch`.

- `choose-one` correct feedback: “Yes. One limited result that the parent checks
  directly does not need a coordinated team.”
- `choose-one` incorrect feedback: “Ask what another role would protect. Here,
  the parent can inspect one clear result directly.”
- `choose-two` correct feedback: “Yes. Separate judgment and a later decision
  justify separate roles.”
- `choose-two` incorrect feedback: “If one helper performed both reviews, two
  independent judgments would become one responsibility.”

### Term treatment

- Introduced after the attempt, in order: `boundary`, `bounded helper`,
  `governed dispatch`, `authority`.
- Deferred from the opening: `gate`, `receipt`.
- New formal terms: none.
- Formal-term count: source `6`; candidate `4`; delta `-2`.

### Density signal

- Source visible-word baseline for the extracted moment: `274`.
- Candidate audience-copy words: `228`.
- Same-surface delta: deferred. This audition proposes only the entry movement;
  protected controls, anchors, and navigation remain source-bound.

## Moment 2 — `lifecycle_tension`

Source target: Route 3 entry tension and the two lifecycle questions.

Protected bindings: `lesson-relay`; all nine timeline states and their order;
`relay-predecessor=receipt-joined`; `relay-limit=new-plan`; both question IDs
and answer values; the public causal-order fixture path; the dependent-work
loop and terminal closeout branch.

### Audience-facing audition

<!-- AUDIENCE_COPY_LIFECYCLE_START -->

**Question — first visible thought**

> **A result came back. What, exactly, has been proved?**

> A returned file shows that something came back. It does not tell you whether
> the worker finished cleanly, whether the expected result was checked, whether
> it was included with every other required result, or whether later work may
> now be planned.

**Attempt**

> Before a decision may use this result, which checkpoint must you be able to
> point to?
>
> - a start was attempted;
> - a result file exists;
> - the expected result was checked and included with every other required
>   result.

**Explanation before formal names**

> Starting, returning, checking, including, and deciding are different facts.
> Keep them separate so a plausible file cannot skip the checks between worker
> activity and the next decision.

**Formal-term reveal**

> The sequence begins with a saved work ticket for one exact job—a **persisted
> action**. The runtime that receives the prepared request and tries to start
> the worker is the **host**. After the worker finishes, fails, or stops, that
> outcome must be recorded before its result moves on.

> The structured record for one expected result is a **receipt**. Once its
> expected identity and shape are checked, it is **admitted**. Once it is
> included with the other results a decision will evaluate, it is **joined**.
> A **gate** is the decision rule that may allow one declared next step.

> A passing gate does not create or start the next job. Correct order also does
> not prove that the result’s actual claim is true.

**Changed next question**

> The gate says the next job may be planned. Can you point to that job’s exact
> saved ticket?

<!-- AUDIENCE_COPY_LIFECYCLE_END -->

### Interaction and feedback mapping

The exact timeline remains intact. The proposed entry teaches the practical
checkpoint ladder before the learner sees its formal labels.

- `relay-predecessor` correct feedback: “Yes. The decision may use the result
  only after the expected record was checked and included with every other
  required result.”
- `relay-predecessor` incorrect feedback: “A start or returned file is earlier.
  Find the checkpoint where the checked result enters the decision set.”
- `relay-limit` correct feedback: “Yes. Permission to plan is not execution;
  the next worker still needs an exact saved job ticket.”
- `relay-limit` incorrect feedback: “The decision opens one next step. It does
  not create, attempt, or execute the next job.”

### Term treatment

- Introduced after the attempt, in order: `persisted action`, `host`, `receipt`,
  `admitted`, `joined`, `gate`.
- Deferred from the entry movement: `boundary`, `causal edge`, `closeout`,
  `eligible wave`, `fixture`, `residue`, `semantic truth`, `terminal accounting`.
- New formal terms: none.
- Formal-term count: source `14`; candidate `6`; delta `-8`.

### Density signal

- Source visible-word baseline for the extracted moment: `365`.
- Candidate audience-copy words: `254`.
- Same-surface delta: deferred. The protected nine-state timeline is referenced,
  not rewritten, by this audition.

## Moment 3 — `transfer_reveal`

Source target: Route 7 transfer scenario, gate question, post-attempt reveal,
and four-part retell handoff.

Protected bindings: `lesson-transfer`; `transfer-start=no`; stable question ID
and answer value; four exit-ticket field names; driver repository anchor; local
storage contract; human review requirement; the rule that a gate creates
eligibility but neither an action nor execution.

### Audience-facing audition

<!-- AUDIENCE_COPY_TRANSFER_START -->

**Question — first visible thought**

> **Two independent reviews cleared the decision point. What would you look
> for before telling an implementation worker to start?**

**Attempt**

> Two reviewers returned their results. Each result passed the expected identity
> and shape checks, and both are included in the decision. The rule says
> implementation may now be planned. In the repository, you can find the
> reviews and the decision, but no exact job file for an implementation worker.

> May that worker begin now?
>
> - Yes—the decision starts the work.
> - No—the next worker still needs an exact saved job ticket.

**Explanation before formal names**

> The decision changed what may be planned. It did not create the missing job
> file or ask a worker to start.

**Formal-term reveal**

> The review records are **receipts**. The checks made them **admitted**;
> including them in the decision made them **joined**. The decision rule is a
> **gate**. Its passing made later work eligible to be planned. It did not
> create a **persisted action** or call the host.

**Changed next question — the retell**

> Explain the handoff in four links:
>
> 1. What task and checked results did you receive?
> 2. What decision changed the present state?
> 3. What may happen next, and what exact item is still missing?
> 4. Who owns the next move, and what would still remain unproved?

> Save your explanation for a human reviewer. Filled fields prove only that text
> was stored locally; they do not prove understanding, authorization, execution,
> or that the underlying claims are true.

<!-- AUDIENCE_COPY_TRANSFER_END -->

### Interaction and feedback mapping

- `transfer-start` correct feedback remains meaning-equivalent to: “The gate
  creates eligibility. It does not create or attempt the dependent action.”
- An incorrect attempt receives the same distinction without supplying the
  four-part retell.
- The retell fields preserve `situation`, `present`, `missing`, and `human` as
  stored names; only learner-facing labels may use the four plain questions.
- The browser may check presence and minimum length only. A human remains the
  meaning reviewer.

### Term treatment

- Reused after the attempt: `receipt`, `admitted`, `joined`, `gate`,
  `persisted action`.
- Deferred from this visible moment: `boundary`, `driver`, `residue`,
  `semantic truth`.
- New formal terms: none.
- Formal-term count: source `9`; candidate `5`; delta `-4`.

### Density signal

- Source visible-word baseline for the extracted moment: `322`.
- Candidate audience-copy words: `231`.
- Same-surface delta: deferred. The candidate preserves the existing repository
  anchor, form controls, and navigation rather than drafting a full route.

## Cross-moment self-review

| Hard gate | Candidate-Q finding |
| --- | --- |
| Meaning invariant removed or reversed | No. One-helper default, independent-review justification, state separation, gate limit, and missing-action rule remain explicit. |
| Formal term used before practical need | No in proposed audience copy. Terms are confined to the reveal after an attempt. |
| Answer leaked by primer or question | No model answer appears before the choices. Each scenario supplies the evidence needed to reason; the post-attempt reveal is conditional. |
| Admission, join, gate, execution, or truth collapsed | No. Each is named as a different fact. |
| Protected identifier, answer, path, timeline, or storage shape changed | No. Proposed changes are visible language only; protected bindings remain exact. |
| Private material, live operation, or unsupported claim added | No. The candidate contains no command or instruction to start agents. |
| Lesson can no longer stand alone | No. Each opening carries its minimum causal premise. |

Editorial strengths to test independently:

- The same question-led voice advances from coordination, to evidence, to
  transfer without turning the class into a glossary.
- Ordinary-language choices let the learner attempt the distinction before the
  formal names appear.
- Each answer changes the next question rather than merely confirming a label.

Editorial risks to test independently:

- The question-led openings may still feel quiz-first if rendered without the
  short scenario immediately beneath them.
- Route 3 still carries six necessary formal terms; their pacing must be tested
  on the actual visual surface.
- The Route 7 scenario necessarily exposes the missing job file as evidence.
  Reviewers must distinguish an answerable problem from wording that explicitly
  supplies its conclusion.

## Whisper result

- Spell: `whisper`
- Transport: `repository_local_interactive_guided_class`
- Transport proof status: `candidate`
- Objective: audition a calmer diagnostic-question-first path through three
  terminology-friction moments without changing source HTML
- Target public: beginner with basic agent, file, JSON, and terminal familiarity
- Intent state: `volatile`
- SCU cores: calm capable voice; beginner need-before-name relevance; question
  to attempt to explanation to formal name to changed-next-question trajectory
- Candidate selected: `Q-fresh`; authored as one independent audition, with no
  sibling comparison or selection claim
- Composition plan: Route 1 coordination choice; Route 3 evidence checkpoints;
  Route 7 missing-action transfer and retell
- Draft status: `flag`
- Human gate: `pending`
- Delivery flow: `active`
- Validation: author self-review only; independent semantic, beginner-flow, and
  operator voice review remain required
- Learning residue: a diagnostic question needs a concrete scenario immediately
  beneath it; otherwise the Q movement becomes a cold quiz
- Next route: independent audition review, then Human Gate A

## Claim boundary

This artifact is a fresh three-moment candidate draft. It does not compare or
select among candidates, alter HTML, prove beginner comprehension or voice
fitness, authorize full-route fan-out, establish canonical status, publish,
deploy, demonstrate production readiness, or prove semantic truth.
