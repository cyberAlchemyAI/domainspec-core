# Worked Example: A Reviewed Team Contribution

Status: `conceptual-only`

This example demonstrates the corrected semantics. It is not a conforming VC,
legal instrument, payment model, or live cryptographic implementation.

## Scenario

During a service incident, three team members jointly discover that a failing
deployment can be stabilized by isolating one queue and replaying a bounded set
of events. One person identifies the pattern, another challenges a dangerous
assumption, and a third verifies the safe sequence. The AI assistant summarizes
logs and alternatives but does not choose or execute the production action.

## Local Contribution Record

```yaml
record_id: cognitive-act-example-001
status: asserted
artifact:
  kind: decision-rationale
  digest: sha256:<example-only>
contributors:
  - ref: contributor-A
    fragments: [pattern-identification]
  - ref: contributor-B
    fragments: [assumption-challenge]
  - ref: contributor-C
    fragments: [safe-sequence-verification]
context:
  task: service-recovery
  time_interval: coarse-incident-window
  location: omitted-not-needed
ai_role:
  actions: [log-summarization, alternative-enumeration]
  prohibited_claims: [decision-author, safety-approver]
consent:
  allowed_uses: [incident-learning, internal-attribution]
  prohibited_uses: [employment-score, model-training, public-ledger]
  withdrawal_route: named-governance-owner
evidence:
  - redacted-incident-log-ref
  - reviewed-decision-note-ref
review:
  originality: pending
  causal_contribution: pending
  rights: pending
  value_allocation: pending
```

## What A Digest Could Establish

If the digest is produced correctly and verified against retained bytes, it can
show whether the reviewed artifact matches those bytes. It does not establish:

- who first had the idea;
- whether the idea is true or safe;
- which contributor is a legal author;
- whether the contribution is patentable or confidential;
- how much value each contributor created;
- that the AI did or did not influence the team's beliefs.

## What A Signed Assertion Could Establish

With real keys, a conforming proof, and a trust policy, a signature can establish
that an issuer asserted this record. The reviewer must still evaluate issuer
authority, evidence, claims, conflicts, and status. A later dispute can mark the
record `disputed` without deleting the fact that an earlier assertion existed.

## Privacy Choice

Exact coordinates, biometrics, mood, keystrokes, and raw conversation content
are excluded because this contribution review does not need them. The example
therefore applies data minimization before any permanence choice.

## Allocation Choice

No token or automatic equal split is triggered. The team uses an agreed review
process with evidence, challenge, appeal, and a declared benefit policy. This
preserves equal dignity while allowing contribution claims to differ.

## Evidence-Harness Handoff

A future evidence harness would be needed to test:

- whether reviewers agree on contribution fragments;
- whether attribution survives adversarial co-authorship disputes;
- false-positive/false-negative source attribution;
- privacy leakage from supposedly minimized records;
- whether benefit allocation is perceived as fair;
- whether AI assistance changes agency, stress, or decision quality.

