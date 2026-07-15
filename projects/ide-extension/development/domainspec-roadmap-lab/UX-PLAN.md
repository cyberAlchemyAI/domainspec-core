---
id: ide-extension-domainspec-roadmap-lab-ux-plan
status: approved-for-planning
updatedAt: 2026-07-14
---

# Roadmap Lab UX Plan

## Product Promise

A person new to DomainSpec can open one place, learn what the production
roadmap means, prove their understanding in their own words, inspect the source
trail, and submit one reviewable improvement without learning the repository's
whole governance model first.

The interface should reveal authority boundaries when they matter, not turn
them into the opening lecture.

## Primary Journey

| Moment | Participant question | Surface behavior | Evidence produced |
| --- | --- | --- | --- |
| 1. Orient | “What is this roadmap, and what can I safely do here?” | A short boundary card says this is a learning/proposal surface; source truth and acceptance live elsewhere. | `roadmap.orientation.acknowledged` only after explicit Continue. |
| 2. Learn one node | “What does FPR-01 mean, why now, and what blocks it?” | One-node focus shows plain-language meaning, outcome, dependencies, evidence, and a visible “source paths” section. | No passive click events. |
| 3. Restate | “Can I explain this in my own words?” | A compact prompt collects meaning, dependency, and done-evidence answers; the participant can revise before submitting. | `roadmap.restatement.submitted`, bound to revision/fingerprint/node. |
| 4. Inspect | “Where did this claim come from?” | Copyable repo-relative source paths and a Request inspection action. | `roadmap.source.requested` with path, selector, node, and bindings. |
| 5. Propose | “What exactly should improve, and why?” | Targeted form selects proposal class and field, shows observed value, and asks for replacement/claim plus reason/evidence. | `roadmap.improvement.proposed`. |
| 6. Follow | “What happened to my proposal?” | Local proposal inbox shows submitted, stale-review-required, under-review, accepted, rejected, or applied-with-evidence with owner route. | Status projection from owner-provided review receipts; browser cannot self-promote. |

## Dedicated Layout

```text
+------------------------------------------------------------------+
| Roadmap Lab | revision + fingerprint | local participant label    |
+----------------------+-------------------------------------------+
| Roadmap outline      | Learn FPR-01                              |
|  > FPR-01 selected   | plain meaning / why now / dependencies    |
|    FPR-02 locked L0  | evidence and copyable source paths        |
|    ...               |                                           |
|                      | [Restate] [Request source] [Propose]       |
+----------------------+-------------------------------------------+
| Proposal history: submitted -> owner route -> disposition         |
+------------------------------------------------------------------+
```

The first proof may render later nodes as visible but inactive. It must not
pretend full roadmap coverage before coverage checks pass.

## Interaction States

| State | Entry | Required UI | Exit |
| --- | --- | --- | --- |
| orientation | Route opens or revision changes materially. | Boundary, roadmap purpose, participant label, Continue. | Explicit acknowledgment. |
| learning | A node is selected. | Meaning, why-now, dependency, done evidence, source paths. | Begin restatement or request source. |
| restatement-draft | Participant starts comprehension prompts. | Editable answers and visible current bindings. | Submit or cancel. |
| restatement-submitted | Event acknowledged by Canvas API. | Durable local acknowledgment and next action. | Propose or return to learning. |
| proposal-draft | Participant selects class/field. | Observed value, proposed change, reason, evidence, owner preview. | Submit or cancel. |
| proposal-submitted | Event acknowledged. | Immutable submitted payload summary and route owner. | Review updates. |
| stale-review-required | Review bindings differ from current material. | Explain which binding changed; preserve the original proposal; offer a new draft. | New proposal or reviewer disposition. |
| under-review | Owner accepted the review handoff, not the change. | Owner route and receipt reference. | Accepted or rejected. |
| accepted | Owner accepts the proposal. | Acceptance evidence and next mutation route; not yet applied. | Applied-with-evidence or withdrawn. |
| rejected | Owner rejects or supersedes. | Reason and retained original proposal. | Closed or new proposal. |
| applied-with-evidence | Source/projection update has concrete proof. | Before/after and owner receipt references. | Closed. |

## Proposal Classes

| Class | Required fields | Owner preview |
| --- | --- | --- |
| `presentation-copy` | `field_id`, observed text, proposed text, reason | Whisper composition/review, then presentation owner |
| `graph-or-claim` | node/edge/claim target, proposed correction, reason, evidence refs | DomainSpec graph/claim owner |
| `continuation` | roadmap node, gap/decision/next-move proposal, reason | Craft owner; no direct ledger write |
| `research-evidence` | claim target, source/evidence gap, suggested research question | Research owner |
| `protected-or-unsupported` | requested action and reason | Fail closed; explain required external route |

## Comprehension Gate

Within 30 minutes and without repository orientation from the facilitator, the
participant should be able to answer:

1. What is DomainSpec v2 trying to make production-ready?
2. What does FPR-01 unlock?
3. Which dependency or evidence makes FPR-01 incomplete today?
4. What can this Roadmap Lab change directly?
5. What happens after an improvement proposal is submitted?

The gate passes only if the answers are substantially correct and the
participant submits one actionable proposal with a clear target and reason.
Facilitator corrections, time, confusion points, and abandoned attempts are
evidence; they must not be edited out of the trial report.

## Accessibility And Error Principles

- All learning and proposal actions remain keyboard reachable and visibly
  focused.
- Status never relies on color alone.
- The original proposal remains readable after stale or rejected outcomes.
- Network/event failure keeps the draft and gives a retry; it never implies the
  event was stored.
- A revision/fingerprint change is explained in plain language.
- Source paths are text and copyable even when source request handling is
  unavailable.

## Explicitly Deferred UX

Authentication, comments/threads, concurrent reviewers, notifications outside
the active local session, repository-wide source browsing, direct editing,
mobile-first optimization, and generalized onboarding for every DomainSpec
artifact are outside the first proof.

