---
module: body-war-ontology-focus-scene-pivot
version: current
status: pass-for-selection
updatedAt: 2026-07-30
docType: implementation-layering
---

# Implementation Layering

## Purpose

Reach a browser-testable first working focus-scene/portal prototype without
mixing source ownership, projection semantics, UI integration, reliability, and
packaging claims.

## Target And Scope

- Target: native Body War route in the Ontology Evidence Workbench.
- State: brownfield, with an accepted 237-node/231-edge failing baseline.
- Start layer: L0.
- Current execution authorization: none.
- First selectable SWU: `SWU-OFSP-001`.

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included | Explicitly deferred | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 POC | After this layer, we know whether one exact four-node tour scene can pivot through one literal portal with truthful state and accessible parity in the native dashboard. | `Business capability map` step one plus `Identity and Consent` → `Authentication and Consent` | independent fixture, successor native overlay/build route, tuple join, tour projection, scene reducer, portal/Back, bounded renderer, detail/focus/motion, verified build, browser receipt | generic one-hop scenes, complete tour lifecycle, all-surface vocabulary hardening, degraded modes, optional orientation, human study | exact arrays, unrelated-node absence, tuple/state byte parity, focus/motion assertions, verified build and browser receipts | continue to L1 only if the source/overlay/state boundaries hold |
| L1 | After this layer, we know whether the bounded model repeats across non-tour focus, every tour transition, and source-literal surfaces. | reusable tour + one-hop scene behavior | one-hop selector, tour suspend/change/restore, cross-surface literals, forced-colors and regression receipt | invalid-source UX, receipt hardening, packaging, human study | deterministic regression across fixtures and browser modes | harden in L2 or narrow the model |
| L2 | After this layer, we know whether the projection fails truthfully and its evidence/governance bindings remain reliable. | degraded-source and independent audit proof | ambiguity/missing endpoint/provenance/stale source handling; overlay, build, receipt, authority and claim audit | upstream publication, deployment, scale, human comprehension | negative fixtures plus audit receipts with zero unowned residue | package locally, remediate, or stop |
| L3 | After this layer, we know whether the admitted local prototype can be reproduced and handed off without inflating its claim. | digest-bound local prototype package | reproducibility guide, exact local run entrypoint, evidence index, research handoff | upstream contribution, public release, deployment, production, comprehension result | clean-clone/local reproduction receipt and explicit research handoff | pilot locally or defer |

## L0 Stop Rule

Do not pull L1 concerns into the first working slice. In particular:

- do not implement generic one-hop focus before the named tour fixture passes;
- do not animate orientation before semantic state parity passes;
- do not redesign ontology groups or adapter semantics;
- do not use human-comprehension language for structural acceptance.

## Non-Regression Guardrails

1. Later layers preserve exact source tuple fields and `authority:none`.
2. Focused/tour scenes never silently fall back to the complete graph.
3. Pointer, Enter, Space, and reduced-motion semantic state stay equivalent.
4. Historical locks, receipts, archives, and generated bundles remain
   immutable.
5. Every source-bearing overlay delta is digest-bound before a build.
6. Browser evidence never satisfies human-comprehension, release, deployment,
   or production gates.

## Recommended Next Layer

- Next layer: L0.
- First decision unlocked: whether the bounded projection/atomic pivot
  architecture works in the actual native Body War dashboard.
- First selectable unit: independent, test-owned fixture oracle
  `SWU-OFSP-001`.
- Selected SWU: none.

