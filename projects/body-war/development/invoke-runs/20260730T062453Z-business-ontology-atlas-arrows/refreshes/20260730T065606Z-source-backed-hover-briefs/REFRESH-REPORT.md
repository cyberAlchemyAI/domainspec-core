# Invoke Refresh Report — Source-Backed Hover Briefs

## Outcome

Status: `pass`  
Mutation mode: `apply-approved`  
Material handoff: `ready`  
Applied targets: 22  
Implementation executed: no

The approved Body War atlas definition, architecture, UX plan, and Work Pack
now specify source-backed reference briefs. The brief content is real escaped
semantic HTML and is planned for hover, keyboard focus, touch/click,
no-JavaScript, and print access.

## Source-backed content contract

- Node: canonical definition, kind/role, status, owner or resolution gate,
  blocking questions, residue, exact incoming/outgoing incidence, and source
  metadata.
- Relation: source → projection wording → target plus predicate, direction,
  authority/value effects, relation ID, and forbidden collapse. Projection
  wording is never called a definition.
- Lens: title, question, description, counts, and directed-flow summary.
- Predicate: token, projection wording, exact count, and bounded examples.
- A blocked item without a recorded question says
  `No blocking question recorded`.
- A zero-incidence item says `No admitted explicit relation`.
- No missing definition, blocker, residue, or relation is invented.

## Plan refresh

The Plan now has five coherent, sequential SWUs:

```text
001 lens-flow projection
  → 002 exact relation arrows
  → 005 source-backed reference briefs
  → 003 overview integration and generation
  → 004 browser/static evidence
```

`SWU-BWAA-005` is independently owned by
`work-pack/tasks/TASK-BWAA-005.md`. The first selectable unit remains
`SWU-BWAA-001`; selected unit remains none.

## Blockers and ceilings

- `BWAA-DRIFT`: preserved, conditional at Task Session preflight.
- `BWAA-PREDECESSOR`: preserved, conditional on every successor.
- `BWAA-RUNTIME`: preserved, conditional for browser evidence.
- `BWAA-SKILL-MIRROR`: the mirror loss observed during Refresh is retained.
  The required generated entrypoints were present at final pre-apply
  verification, so the blocker is resolved-currently and remains conditional
  at Task Session preflight.
- `authority_effect: none`.
- `release_admission: not-granted`.
- implementation, browser acceptance, comprehension, formal accessibility
  conformance, promotion, release, deployment, and production are unclaimed.

## Verification

- material-package verdict: pass; owner, dependency, and publication
  boundaries pass;
- direct-user handoff: ready, zero apply blockers;
- 22 staged outputs applied with exact preimage and output hashes;
- Design extraction and selection rerun against the applied repository and
  matched the staged receipts byte-for-byte;
- Design verdict: pass, fixed point true, zero diagnostics;
- five task specs, five successor rows, and W1 `002 → 005` pass;
- protected renderer, generator, projection, tests, generated atlas, browser
  validator, and coverage receipt hashes are unchanged;
- scoped whitespace validation passes;
- one read-only Refresh helper completed and joined;
- exactly one Distill and one Invoke observability row were recorded.

Observer residue: central telemetry was recorded, but reflection-state update
failed on a structured-workflow-gap formatting mismatch. This is non-blocking
and remains explicit in `observability/OBSERVATION-RECEIPT.md`.

## Next route

Await explicit selection of `SWU-BWAA-001`, then run Context Builder and one
Task Session preflight. Refresh does not select or execute it.
