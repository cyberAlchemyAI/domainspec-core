# Body War Business View Novice-Comprehension Context Pack

## Objective

Turn the accepted novice-comprehension review into the smallest browser-testable
Body War business-view prototype: an isolated learner task, an
authority-honest journey stimulus, and pinned structural browser evidence.

## Approved design inputs

- `projects/body-war/development/reviews/20260729-business-view-novice-comprehension/findings.md`
- `projects/body-war/development/reviews/20260729-business-view-novice-comprehension/EXECUTION-RECEIPT.json`
- User instruction on 2026-07-29: plan the accepted work, then use Task Session
  to implement everything in the bounded implementation slice.

## Current implementation inputs

- `projects/body-war/ontology/business/authoring/view-catalog.mjs`
- `projects/body-war/ontology/business/scripts/generate-views.mjs`
- `projects/body-war/ontology/business/tests/business-views.test.mjs`
- `projects/body-war/ontology/business/profile.json`
- `projects/body-war/ontology/business/residue.json`
- `projects/body-war/ontology/business/relations/relations.json`
- `projects/body-war/ontology/business/nodes/manifest.json`
- `projects/body-war/ontology/business/receipts/validation-receipt.json`

## Baseline evidence

- `node projects/body-war/ontology/business/scripts/generate-views.mjs --check`
  passed at `2026-07-29T20:12:10Z`.
- `node --test projects/body-war/ontology/business/tests/business-views.test.mjs`
  passed `8/8`.
- `relations/relations.json` SHA-256:
  `234ad4152b731edcb03cd1b45dfa21570bd37df741090ca6ca0940fd98c0ce00`.
- `nodes/manifest.json` SHA-256:
  `3cffc5cea2d5abff02ce1b28e87ed80519795fa3074e47e1ec2030c3214f4fdb`.

## Constraints

- The business ontology remains `candidate-local`,
  `authority_effect: none`, `release_admission: not-granted`.
- The work may project `profile.json` and `residue.json`; it may not change
  ontology nodes, relations, lifecycle policies, or semantic digests.
- Learner bytes may not contain reviewer keys, rubrics, coverage audits,
  correctness results, stall results, or human records.
- The printable gallery is not part of the initial protocol.
- Browser evidence proves only pinned structure and interaction.
- No human witness is authorized.
- A blind agent pretest needs a fresh agent that has not read reviewer-only
  material; it cannot be simulated by this planning/execution context.

## Planning assumption

Invoke Distill uses the Standard budget because no alternate budget was
selected.

