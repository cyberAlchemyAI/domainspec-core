---
module: body-war-ontology-focus-scene-pivot
version: current
status: pass
updatedAt: 2026-07-30
docType: invoke-define-transport
---

# Invoke Define Transport

## Authorization

The user's direct Invoke request authorizes Define, Design, and Plan authoring
for implementation of the accepted black-box findings. It does not authorize
source mutation, ontology mutation, browser acceptance execution, promotion,
release, deployment, or publication.

## Inputs

- `CONTEXT-PACK.md`
- accepted review `findings.md`
- accepted review `synthesis.md`
- current OEW overlay ownership and upstream locks
- frozen Body War presentation graph

## Outputs

- `SPEC.md`
- `GLOSSARY.md`
- `CONCEPT-MAP.md`

## Gate Result

- DomainSpec baseline: selected
- UI concepts typed and bounded: pass
- Glossary consistency: pass
- Acceptance contracts: authored, not executed
- Authority boundary: `authority_effect:none`
- Release admission: `not-granted`
- Design input status: `approved-for-design`
- Result: `pass`

## Design Handoff

Design must:

1. close an exact digest-bound scope manifest;
2. run the independent denominator extractor and two-pass selection validator;
3. include all six baseline architecture views;
4. select UX because a natural person operates a changed semantic surface;
5. specify deterministic projection, session-state, accessibility, degraded
   behavior, and acceptance interfaces;
6. keep every witness in planned/not-run state.

