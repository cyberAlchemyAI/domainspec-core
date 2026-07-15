---
id: ide-extension-domainspec-roadmap-lab-distill-design-validation
status: pass
updatedAt: 2026-07-14
mode: standard
rounds: 2
---

# Distill Design Validation

## Target

Determine whether the Roadmap Lab design is the smallest coherent design unit
that can test newcomer understanding and contribution without creating false
authority.

## Round 1 — Proposer

Proposed unit:

```text
one generated FPR-01 learning packet
  -> explicit boundary acknowledgment
  -> participant restatement
  -> copyable source path / source request
  -> one revision-and-fingerprint-bound proposal
  -> durable Canvas event
  -> owner route preview
```

Why it is coherent: removing the restatement loses evidence of understanding;
removing source inspection makes the proposal ungrounded; removing dual binding
makes review ambiguous; removing persistence makes the contribution ephemeral;
removing owner routing invites false mutation authority.

## Round 1 — Balancer

Pressure applied:

- all-node interactivity is not required to test the product hypothesis;
- review-status synchronization is valuable but not needed to prove event
  submission in L0;
- a browser source resolver is not needed because copyable paths and a source
  request preserve the evidence trail;
- extracting stable presentation-copy fields is acceptance-critical, because
  otherwise a targeted copy proposal has no durable target.

Adjustment: keep stable copy-field identity in the contract foundation, but
make only FPR-01 interactive in the first browser witness.

## Round 2 — Proposer

Recomposed target:

```text
copy and event oracles
  + one-node generated surface
  + existing Canvas publish/event path
  + owner-route preview
  = complete L0 newcomer loop
```

The unit can later expand by data coverage rather than by replacing its state or
authority model.

## Round 2 — Balancer

Hidden-gap checks:

| Check | Result | Reason |
| --- | --- | --- |
| Can review identify what was seen? | pass | Canvas revision, input fingerprint, field/node, and original value are required. |
| Can the UI falsely claim application? | pass | Submitted, accepted, and applied states require distinct evidence. |
| Can source inspection block L0? | pass | Copyable paths remain useful without a source resolver. |
| Does generic workbench Craft state confuse DomainSpec state? | pass | Dedicated route keeps the contexts separate. |
| Is human usefulness reducible to automated tests? | pass | Victor trial is a non-simulatable L3 gate. |
| Is unnecessary hardening pulled forward? | pass | Identity, remote, multi-user, authorization, and generic browsing stay deferred. |

## Verdict

**Pass.** The selected design unit is minimal but not theatrical: it produces a
real, durable proposal that a reviewer can evaluate against the exact displayed
context. It recomposes into all-node coverage and owner-specific routing without
changing the core contract.

No blocker prevents Invoke plan. Planning must preserve the stable-copy-field
foundation, dual binding, explicit owner boundary, dirty-worktree gate, and real
human trial.

