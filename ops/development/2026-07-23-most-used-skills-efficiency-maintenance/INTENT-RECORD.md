# Intent Record

- Run: `invoke define/design/plan`
- Target: most-used skills efficiency maintenance
- Requested by: repository maintainer
- Authoring approval: explicit request to define, design, and plan
- Implementation authority: not granted
- Target lifecycle owners: `sigil-development`, `spellcraft`, and private DomainSpec tooling maintenance

## Intent

Turn the accepted audit of Task Session, Invoke, DomainSpec Subagents Strategy,
Decision Gate, Inventory, and Whisper into a complete implementation package.
The package must reduce repeated prompts and late blocker discovery without
removing controls that contain a demonstrated unsafe state.

## Source boundary

- `../2026-07-22-most-used-skills-efficiency-review/findings.md`
- `../2026-07-22-most-used-skills-efficiency-review/attacks.md`
- `.arcanum/observability/reflections/20260723T005559Z-most-used-skills-efficiency-review.md`
- current target contracts, validators, generated surfaces, and tests named by
  the accepted findings

The review is frozen evidence. This package may reference it but must not edit
or reinterpret its accepted ten-change boundary.

## Approved authoring decisions

1. Produce Define, Design, and Plan outputs in one authoring run.
2. Keep each accepted change request independently executable and reviewable.
3. Select only the first narrow unit for the next lifecycle route.
4. Do not modify audited skills or execute implementation in Invoke.
5. Do not add another subagent dispatch; automatic Distill uses a labeled local
   Proposer/Balancer trace because no new dispatch sheet was confirmed.

## Success

The result is successful when a lifecycle owner can start `SWU-WFE-001` without
reopening discovery, while every later change has an owner, dependency, write
scope, negative controls, acceptance evidence, and a route that preserves
public/private and canonical/generated boundaries.
