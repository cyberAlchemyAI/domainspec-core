# 02 — Invoke Define

## Proposed bounded definition

A **Tower Scene Canvas** is a read-only local interface that presents one or more declared tower descriptors in a navigable spatial field. Selecting a tower or evidence level changes the displayed scene only when the descriptor supplies a locked evidence projection, explicit evidence state, claim ceiling, and refusal copy.

It is not:

- a claim that every research artifact is a tower;
- a real corpus selector or representative-tower decision;
- a runtime-queryable graph, persona system, MOGT policy, adjudicator, or verdict engine;
- an authority, promotion, publication, or deployment surface.

## First scene contract

Each current `tower:toy` level must expose:

| Field | Purpose |
| --- | --- |
| `tower_id` and `level_id` | stable selection and deep-link target |
| `scene_kind` | `corpus-observatory`, `residue-conservatory`, or `closure-workshop` |
| `evidence_state` | `realized`, `candidate`, `blocked`, or `unavailable` — never inferred from decorative art |
| `source_refs` | loader/fixture identifiers and local paths |
| `claim_ceiling` | displayable boundary text |
| `content` | facts already emitted by the verified read model |
| `unavailable_reason` | explicit fallback for an unbound level or future architecture layer |
| `reduced_motion_mode` | semantic content remains visible with decorative motion disabled |

## Definition test

A descriptor is invalid when it has no source refs, no evidence state, no claim ceiling, or its state would imply a real tower, authority effect, promotion, or runtime component unsupported by the locked input.
