# Paper Spec

Purpose: define the paper's section-level design contract before evidence-backed prose writing begins.

Authority model:

- `papers/<paper-file>.md` is the narrative synthesis artifact.
- `registry/RESEARCH-GRAPH.md` is the typed graph input authority for section obligations.
- This spec translates the graph into explicit section-writing obligations.

## Paper Objective

[state the paper's main question, contribution target, and intended evidence posture]

## Design Contract

1. The paper must not redefine canonical project semantics.
2. Every section should map to one or more `PSEC-*` graph nodes.
3. Result sections need evidence-backed result and status inputs before making support claims.
4. Narrative references should already exist in `sources/REFERENCE-LEDGER.md`.

## Section Registry

| Section Node | Section Title | Synthesis Role | Required Graph Inputs | Current Readiness | Current Blockers |
| ------------ | ------------- | -------------- | --------------------- | ----------------- | ---------------- |
| PSEC-01      | [title]       | [role]         | [nodes]               | [status]          | [blockers]       |

## Linked Paper Contract Artifacts

- `papers/PAPER-STORIES.md`
- `papers/PAPER-TEST-SPEC.md`
- `papers/PAPER-REVIEW.md`
