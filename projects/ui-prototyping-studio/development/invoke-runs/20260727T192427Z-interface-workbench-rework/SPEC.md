---
artifact: ui-prototyping-studio-interface-workbench-rework
artifact_type: feature-change-spec
status: invoke-authored
define_gate: pass
discovery: present
discovery_artifact: output/playwright/ux-validator/20260727-ui-prototyping-studio-interface-review/findings.md
lifecycle_owner: ui-prototyping-studio
implementation_authority: none
---

# UI Prototyping Studio Interface Workbench Rework

## Purpose

Rework the local loopback preview into a stable governed workbench that keeps
the current task, evidence, and next valid action visible without weakening any
existing admission or authority boundary.

The immediate trust failure is continuity: unchanged polling currently reloads
the whole document in four lifecycle states and destroys local task context.
The rework repairs that boundary before changing hierarchy or visual treatment.

## Problem

The preview is functionally governed but not interaction-safe:

- absent staged identity is rendered as `""` and transported as JSON `null`;
- the browser compares coerced values and reloads every 1.5 seconds;
- the current task is ordered after historical lineage;
- staged frames are unnamed;
- three dynamic feedback nodes lack bounded status semantics;
- sampled muted text fails the normal-text contrast threshold;
- small actions and CLI-shaped copy weaken the workbench surface; and
- current E2E coverage proves eventual projection, not continuity.

This is not evidence that the state machine, current-head projection, or
reversible-action gates should be replaced.

## Scope

Included:

- one canonical server-computed update identity;
- a stable document shell with keyed state-region updates;
- exact unchanged-poll and one-real-transition semantics;
- preservation of selected target, drafts, focus, top-level scroll, annotation
  frame scroll, and state-specific task context;
- a persistent lifecycle and next-action spine;
- a dominant current-head canvas and contextual annotation/batch inspector;
- staged Before/After/Diff review adjacent to acknowledgment and actions;
- collapsed secondary variant/revision history;
- distinct accessible names for comparison frames;
- bounded polite live regions for `cf-msg`, `act-msg`, and `act-msg2`;
- calibrated light-surface text contrast;
- calibrated target sizes for outer workbench actions;
- browser-action copy aligned with the actual local surface;
- 1440×900 and 390×844 acceptance fixtures; and
- current docs/guided-script synchronization only after implementation evidence.

Excluded:

- changing state vocabulary or admission semantics;
- weakening identity-bound acknowledgment;
- advancing the head when a candidate is merely staged;
- destructive history rewrite;
- moving Export into the browser;
- embedding a model, agent loop, or remote service;
- a framework migration as a goal in itself;
- cross-browser certification, broad accessibility certification, or release;
- claims about comprehension, trust, safety, workload, delight, or real-user success;
- automatic SWU selection or implementation during Invoke.

## Actors And Owners

| Owner | Responsibility |
| --- | --- |
| Studio operator | Inspects the current head, selects targets, records intent, reviews evidence, and disposes of reversible actions. |
| Browser workbench | Projects current governed state and preserves local task context between updates. |
| Preview adapter | Computes canonical update identity, serves state and keyed projections, and maps browser actions to existing application gates. |
| Application core | Owns current-head truth, staging, admission, acknowledgment validation, revision append, and handoff predicates. |
| File store and artifact store | Own fresh persisted reads, serialized durable writes, and current HTML bytes. |
| UX Evidence Validator | Owns calibrated later evidence for the named interaction and accessibility contracts. |
| Task Session | Executes exactly one explicitly selected implementation SWU. |
| Studio lifecycle owner | Accepts, narrows, rejects, and eventually closes the rework package. |

## Functional Requirements

| ID | Requirement |
| --- | --- |
| FR-01 | `/state` must expose one opaque server-computed update identity whose absent values have one canonical representation. |
| FR-02 | Two unchanged poll intervals must produce zero main-document navigations and zero keyed-region updates. |
| FR-03 | One genuine transition must produce exactly one intended workbench update under the selected transport semantics. |
| FR-04 | Polling and genuine transitions must preserve selected annotation target, draft controls, focus, top-level scroll, annotation-frame scroll, and task context unless the changed state invalidates that exact context. |
| FR-05 | The shell must show lifecycle state and the next valid action persistently at desktop and mobile sizes. |
| FR-06 | Current head must remain the primary inspectable and annotatable artifact; history must be explicitly secondary and non-current. |
| FR-07 | State-specific annotation, batch, staged-review, or recorded-revision context must appear adjacent to the primary canvas and relevant action. |
| FR-08 | `RevisionApplied` must show named Before and After frames, diff evidence, live identity, target state, acknowledgment, and Accept/Discard without advancing the head before Accept. |
| FR-09 | `RevisionRecorded` must show the current revision receipt and append-only Revert context; Export remains terminal-only. |
| FR-10 | Only `cf-msg`, `act-msg`, and `act-msg2` receive the calibrated atomic polite-status contract in this scope; blocking errors may use a separately tested assertive path. |
| FR-11 | Sampled normal-size light-surface instructional/governance text must meet 4.5:1 after real compositing. |
| FR-12 | Outer workbench actions must meet at least the calibrated 24×24 CSS-pixel floor; primary actions should target 40–44px where the layout permits. |
| FR-13 | At 390×844 the document must not overflow horizontally and lifecycle/action context must precede history in task order. |
| FR-14 | Copy must name the action available in the browser while preserving exact CLI details in a secondary disclosure where useful. |
| FR-15 | All changes must preserve the existing application-owned governance invariants and handoff predicate separation. |

## Canonical Update Contract

The server owns an opaque `version` value derived from the exact fields that
change the rendered governed projection. The browser:

1. records the version attached to the current projection;
2. polls `/state`;
3. does nothing when the version is unchanged;
4. requests or applies only the keyed projection required by a changed version;
5. preserves local context whose identity remains valid; and
6. records an explicit invalidation reason when changed state makes local
   context invalid.

The contract does not require a particular frontend framework. It forbids
client-side reassembly through nullable string coercion and forbids
whole-document navigation as the steady-state update mechanism.

## Governance Invariants

1. One current head is authoritative for preview and annotation.
2. A staged candidate remains non-current until exact identity-bound Accept.
3. Accept and Revert remain disabled until the live action context is acknowledged.
4. The server independently rejects missing acknowledgment and stale identity/state.
5. Revert appends a new revision and never rewrites history.
6. Export remains terminal-only and requires explicit confirmation.
7. Export confirmation, evidence completeness, integration readiness,
   implementation readiness, approval, deployment, release, and production
   readiness remain distinct facts.

## Acceptance Criteria

- In each null-staged state `BaselineReady`, `CommentsCaptured`,
  `MutationDrafted`, and `RevisionRecorded`, two unchanged poll intervals cause
  zero main-document navigations at both required viewports.
- The stable-poll matrix preserves focus, selected target, nonempty draft,
  top-level scroll, annotation-frame scroll, and state-specific context.
- `RevisionApplied` browser Accept causes exactly one intended update, with
  main-document and child-frame navigations counted separately.
- A changed state invalidates only context whose bound identity is stale and
  makes that invalidation perceivable.
- Before/current and after/candidate frames have distinct accessible names.
- Positive and negative fixtures bind live announcements only to the three
  specified node/event scopes.
- Computed contrast and target-size checks pass calibrated fixtures.
- Desktop and mobile show the active task before collapsed history and have no
  horizontal overflow at 390px.
- Existing current-head, action acknowledgment, external-process freshness,
  diff, handoff, unit, and E2E contracts remain green.

## Evidence Ceiling

This specification is an Invoke-authored target contract grounded in a
Chromium audit. Planned witnesses are unexecuted. It proves neither the rework,
accessibility conformance, cross-browser behavior, human ergonomics, release
authorization, deployment, nor production readiness.

## Next Owner

Invoke Design owns architecture, UX views, and witness contracts. Invoke Plan
owns layering and one-behavior SWUs. The Studio lifecycle owner must accept the
package and explicitly select one unit before Task Session may mutate source.

