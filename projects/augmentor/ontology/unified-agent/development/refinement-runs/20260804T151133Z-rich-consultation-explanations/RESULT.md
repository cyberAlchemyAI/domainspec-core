# Refine Result: Rich Consultation Explanations

- Status: flag
- Target: Augmentor ontology consultation and answering-agent experience
- Preset: deep
- External research: not run
- Product changes: none
- Deployment: none
- Authority effect: none

## Outcome

The current system is now understood precisely enough to plan the improvement in one coherent chain. Augmentor already has a working read-only consultation service over a 22-record neutral projection, with source handles, bounded retrieval, fail-closed statuses, cache isolation, and an answer policy. It is not a reasoning engine and it does not generate the answer.

The main explanation gap is concrete: the beginner source already has state, examples, and analogies, but the compiler drops those fields. The API returns only label, summary, process/responsibility, and boundary evidence. It has no glossary or brief/guided/deep support contract.

## Selected Architecture

Use a record-local explanation pack plus a reusable glossary sidecar, bound together with the projection by one atomic bundle manifest and digest. The API returns only bounded support and two to five referenced glossary entries. The answering agent composes the final response.

Every rich answer follows:

1. direct answer;
2. verified, scoped current state;
3. step-by-step process;
4. one labeled scenario when useful;
5. one analogy plus where it stops matching;
6. two to five used terms;
7. boundary and sources.

`guided` is the default profile. Brief and deep vary detail, never truth or authority.

## Important Reasoning Answer

There is no proven integrated Augmentor reasoning engine today. The working consultation service performs deterministic retrieval and returns evidence plus answer guidance. The ontology describes future reasoning-request and judgment-receipt concepts, but the Augmentor adapter, applicability/catalog owner, and protected-action path remain deferred. A future judgment would still be advice, not approval or permission to act.

## Implementation Package

`WORK-PACK.md` defines nine ordered units:

`schema truth -> closed contracts -> structured sources -> atomic bundle -> consumer load/cache -> bounded support -> agent composition -> page -> measured acceptance`

The unique first unit is schema-version reconciliation. The current repository JSON schema says `@0.1.0`, while the compiler and consumer use `@1.0.0`; no rich-field work should begin until that owner decision and regression test are closed.

## Why The Result Is Flagged

The planning work is complete, but implementation and owner admission have not occurred. Profile budgets are targets, not measurements. Final consumer evidence must run under Node `>=22.13.0`; this session's targeted consumer tests passed under local Node `v22.12.0`. Browser acceptance, deployment, release, and human comprehension remain unproven.

## Next Route

Run `implementation-readiness` against the complete Work Pack, including owner decisions G-01 through G-06. Freeze exact bytes and validation for `SWU-RCE-000` first. Do not start with a glossary-only or page-only change, and do not deploy from this Refine result.
