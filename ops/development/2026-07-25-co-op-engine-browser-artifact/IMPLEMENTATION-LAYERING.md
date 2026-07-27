---
module: co-op-engine-browser-app
version: plan-v1-refresh-1
status: active-l0
updatedAt: 2026-07-26
docType: implementation-layering
---

# Implementation Layering: Co-Op Engine Browser App

## Target and Scope

- Target: `projects/co-op-engine/`
- Scope: browser product
- Current state: greenfield
- Current Plan window: L0 only

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included | Deferred | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether one project record can fail closed and whether the complete portfolio/meeting narrative can cohere in one non-authoritative browser artifact. | `SWU-COOP-001` Poker admission contract, then `SWU-COOP-002` self-contained HTML prototype | dependency-light TypeScript contract; one semantic HTML file with fourteen bounded project cards and the 45-minute route | admitted multi-record bundle, JavaScript state, real projection modes, interaction, persistence, final copy, hosting | contract-test receipt, then local black-box browser structure/responsive/network/screenshot receipt | retain, revise, or discard the prototype before L1; promote only after both serial decisions pass |
| L1 | After this layer, we know whether admitted records can drive self-guided and facilitated semantic browser projections. | admitted Poker card plus shared truth digest and two real mode view models | app shell, safe routing, data modules, semantic card/detail, presentation projection, keyboard/history/mobile proof | private submission, receipts, full admitted catalog, final copy | black-box route/DOM/keyboard/history/network/screenshot evidence | harden or stop |
| L2 | After this layer, we know whether visibility, reciprocity, durable submission, failure recovery, and receipts survive every observable surface. | one synthetic/consented candidate pair through terminal receipt | visibility projector, transition machine, gateway, idempotency, persistence, leakage suite | full catalog, public release, efficacy | state, privacy, persistence, failure, and recovery receipts | remediate or proceed |
| L3 | After this layer, we know whether fourteen cards, final copy, the 45-minute route, restricted deployment, and human audits form a coherent recruitable artifact. | full restricted meeting/page witness | admitted portfolio, Whisper copy, UI/copy/coherence audits, meeting run, Sites version/deployment | public access until D-005 and all gates pass | card-ceiling, human-study, audit, meeting, deployment, and publication receipts | pilot, publish, or defer |

## L0 Boundaries

`SWU-COOP-001` owns one primary decision: whether a candidate project record is
admitted under the current Co-Op card policy.

It includes all rules required to make that one decision safely:

- required record structure;
- owner verification and exact source presence;
- claim ceiling and forbidden-claim presence;
- bounded experiment fields;
- 72-hour SLA;
- expiry exactly 30 days after verification;
- current `eligible` state at a fixed `asOf`;
- policy version;
- visibility class for every required field.

It does not implement collaboration transitions or projection leakage checks.
Those are independently executable L1/L2 behaviors and remain deferred.

`SWU-COOP-002` owns a different primary decision: whether one locally opened,
self-contained semantic HTML document can make the event invitation,
45-minute route, and all fourteen claim-bounded opportunities inspectable by a
reader or facilitator.

It includes:

- one low-fidelity responsive document and inline styles;
- semantic landmarks, heading order, skip navigation, and anchor navigation;
- exactly fourteen distinct project cards;
- one current bounded description, limitation, seven-day act, and human ask
  per card;
- the event invitation, experiment-exchange honesty boundary, 45-minute route,
  and participation choices;
- real-browser desktop/mobile structure, overflow, console, network, and
  screenshot evidence.

It excludes JavaScript, forms, offer submission, real mode state, private
presenter notes, admitted-data compilation, final Whisper copy, persistence,
hosting, deployment, and claims that comprehension, privacy, recruitment, or
the meeting mechanism passed.

The HTML content is an internal research-derived fixture. It is not a source
of canonical project truth and must be replaced by admitted data projections
in L1.

## Non-Regression Guardrails

- L1 projections consume only L0-admitted records.
- L1 must not treat the L0 HTML fixture as an admitted catalog or production
  component.
- L2 interaction cannot weaken L0 admission or L1 semantic/privacy boundaries.
- L3 copy cannot override record truth or claim ceilings.
- A later schema version must preserve historical policy interpretation.
- Deferred scope cannot enter `SWU-COOP-001` merely because the same future
  files may be convenient.

## Recommended Next Layer

- Next layer: L0
- Decision unlocked: whether record admission can fail closed before UI work
- Selected unit: `SWU-COOP-001`
- Planned serial candidate after selected-unit closeout:
  `SWU-COOP-002`
- Major deferred scope: real browser projection behavior, interaction, final
  copy, human audits, persistence, and deployment
