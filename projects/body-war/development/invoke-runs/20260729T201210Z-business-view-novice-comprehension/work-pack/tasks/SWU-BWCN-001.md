# SWU-BWCN-001 — Isolated Learner Instrument

Status: `ready`

## Primary behavior

Generate `BUSINESS-COMPREHENSION-TASK.html` from a learner-only catalog while
enforcing that reviewer keys and run artifacts cannot enter learner bytes.

## Material write scope

- `projects/body-war/ontology/business/authoring/comprehension-task-catalog.mjs`
- `projects/body-war/ontology/business/scripts/generate-comprehension-task.mjs`
- `projects/body-war/ontology/business/BUSINESS-COMPREHENSION-TASK.html`
- `projects/body-war/ontology/business/review/comprehension-protocol.schema.json`
- `projects/body-war/ontology/business/review/comprehension-protocol.json`
- `projects/body-war/ontology/business/tests/fixtures/comprehension-reviewer-leakage.txt`
- `projects/body-war/ontology/business/tests/business-comprehension.test.mjs`

## Acceptance

- generator imports only the learner catalog;
- six preregistered loci are present exactly once;
- reviewer deny markers are absent from learner HTML;
- task/prompt/stimulus metadata is deterministic;
- keyed edge/branch/boundary/invented-sequence rules live reviewer-side;
- zero stalls is valid reviewer data;
- generator `--check` and Node tests pass.

## Validation

```text
node projects/body-war/ontology/business/scripts/generate-comprehension-task.mjs --check
node --test projects/body-war/ontology/business/tests/business-comprehension.test.mjs
```

## Split analysis

Splitting catalog, generator, HTML, protocol, and tests would temporarily create
either an ungenerated task or an unenforced contamination boundary. They are one
atomic behavior.

