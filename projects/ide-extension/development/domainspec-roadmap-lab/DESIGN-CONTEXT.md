---
id: ide-extension-domainspec-roadmap-lab-design-context
status: bounded
updatedAt: 2026-07-14
profile: context-builder-standard-strict
---

# Roadmap Lab Design Context

## Frame

Design a private-local, newcomer-facing Roadmap Lab inside `projects/ide-extension`.
It must help a person understand one DomainSpec v2 production-roadmap node and
submit a useful improvement proposal without making the browser an authority or
reopening the already accepted product strategy.

This pack selects 10 source files and fewer than 280 source-line selectors. It
is an authoring frame, not an execution-time handoff pack.

## Obligations

| ID | Design obligation |
| --- | --- |
| O-01 | Preserve the accepted proposal-first strategy: learn, restate, inspect, propose; never edit authority from the browser. |
| O-02 | Reuse the existing trusted-local Canvas publication, complete-revision display, named-event return, and cursor-poll path. |
| O-03 | Bind proposals to both the displayed Canvas revision and the input roadmap fingerprint. |
| O-04 | Separate presentation wording from roadmap/graph authority before collecting copy proposals. |
| O-05 | Give a newcomer a dedicated route and an unambiguous five-step path focused on one node. |
| O-06 | Persist only meaningful learning/proposal events; do not add clickstream telemetry. |
| O-07 | Route proposals to their owning lifecycle; submission is neither acceptance nor application. |
| O-08 | Make the Victor comprehension/usefulness trial a real product gate that cannot be simulated. |
| O-09 | Keep authentication, remote collaboration, multi-user identity, direct mutation, generic source browsing, and unnecessary hardening outside the first proof. |

## Selected Evidence

| Source selector | Why selected | Obligations |
| --- | --- | --- |
| `../domainspec-roadmap-lab-strategy/STRATEGY.md#decision-in-one-sentence` through `#smallest-coherent-unit` | Accepted outcome, user, constraints, and smallest useful loop. | O-01, O-05, O-08 |
| `../domainspec-roadmap-lab-strategy/STRATEGY.md#product-surface` through `#newcomer-path` | Dedicated surface and five learning moments. | O-05, O-06 |
| `../domainspec-roadmap-lab-strategy/STRATEGY.md#architecture` through `#source-inspection-boundary` | Reuse/add/defer split, interaction bindings, authority routing, copy and source boundaries. | O-02, O-03, O-04, O-07, O-09 |
| `../domainspec-roadmap-lab-strategy/STRATEGY.md#human-validation-gate` through `#deferred-complexity` | Trial gate, mechanical checks, premortem, and explicit deferrals. | O-08, O-09 |
| `../../ARCHITECTURE.md:146` through `../../ARCHITECTURE.md:185` | Live Canvas flow, complete revisions, owner responsibilities, and authority boundary. | O-02, O-07 |
| `../../SPEC.md:232` through `../../SPEC.md:278` | Live V0 contracts, 16 KiB limit, projected records, idempotency, singleton stream, and deferrals. | O-02, O-03, O-09 |
| `../../schemas/canvas-interaction-request.schema.json` | Current interaction request oracle. | O-02, O-03, O-06 |
| `../../public/demo/l0.html:1390` through `../../public/demo/l0.html:1432` | Exact `postMessage` admission and event POST behavior. | O-02, O-06 |
| `../../src/modules/whisper.manifest.json` | Whisper may read/preview/draft but may not silently publish or rewrite authority. | O-04, O-07 |
| `../../src/modules/craft.manifest.json` | Craft may read/preview/recommend a route but not mutate its ledger or promote authority from this surface. | O-07 |

## Existing Roadmap Projection Inputs

The current presentation is generated from
`projects/domainspec-v2/development/first-production-release/visibility/roadmap-data.json`
by `visibility/tools/build-roadmap.py` and rendered through
`visibility/roadmap.template.html`. These are brownfield inputs, not authority
created by this design. Their current untracked state is an execution-time
ownership concern.

## Authority And State Boundaries

| State | Owner | Allowed crossing |
| --- | --- | --- |
| Production roadmap, graph claims, and Craft continuation | Their DomainSpec/Craft lifecycle | Read by reference; changes require owner review and evidence. |
| Presentation copy | Roadmap presentation contract | Generated into HTML; copy proposals may target stable presentation fields. |
| Canvas surface, revision, and interaction events | `projects/ide-extension` local kernel | Complete HTML publication and append-only, bounded named events. |
| Browser learning/proposal state | Roadmap Lab projection | Restatement draft, proposal draft, and local status display only. |
| Acceptance and source mutation | Target lifecycle owner | Never implied by a submitted browser event. |

## Active Tensions

1. The roadmap is already readable, but its prose is embedded in the template;
   allowing copy proposals before extraction would bind feedback to unstable
   implementation detail.
2. Source paths are valuable teaching evidence, but relative links rendered
   from the Canvas content route do not safely resolve to repository files.
3. The generic workbench already shows Craft state, but that state belongs to
   `projects/ide-extension`, not the DomainSpec production roadmap.
4. The current Canvas is a trusted-local singleton. That is sufficient for one
   participant and one active session, not evidence for collaboration or
   authenticated identity.

## Design Write Boundary

This Invoke run may create only this development package. It must not edit the
roadmap projection, its builder, `SPEC.md`, `ARCHITECTURE.md`, Canvas schemas,
server, browser UI, runtime tests, or either Craft ledger.

