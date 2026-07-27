---
id: ui-prototyping-studio-spec
project: ui-prototyping-studio
title: "UI Prototyping Studio — Lean Receipt-Backed Feature Spec"
status: active
node_type: spec
updatedAt: 2026-07-27
---

# UI Prototyping Studio — Lean Feature Spec

> This document describes the locally reproducible implementation floor.
> [The amended 2026-07-27 work-pack](development/invoke-runs/20260727T042935Z-architecture-review-refresh/WORK-PACK.md)
> and its Task Session plus joined closeout receipts own current completion
> evidence. June deep-spec material is historical proposal/design evidence.

## Purpose

UI Prototyping Studio supports accountable UI exploration:

1. capture a prompt and register one to three HTML variants;
2. intentionally select and commit a baseline;
3. annotate actual `data-od-id` targets;
4. synthesize a deterministic mutation batch and explicitly approve it;
5. validate and stage a candidate without advancing the head;
6. inspect and acknowledge the exact Accept or Revert context;
7. append a revision rather than destructively rewriting history; and
8. export a confirmed handoff whose evidence/readiness predicates stay
   separate.

The Studio is the governance harness. It does not contain an LLM. Claude Code
or another external generator may produce HTML, but caller identity does not
create authority. Authorization is a property of the invoking route and its
owner.

## Proven implementation floor

The current receipts establish:

- local CLI and no-build loopback preview operation;
- deterministic, fail-fast Playwright startup with diagnostics;
- fresh persisted reads and serialized file writes, including a
  second-process state witness;
- application-owned current-head preview/annotation projection;
- honest structural, style/global, and unattributed diff lanes;
- actor-neutral, identity-bound acknowledgment for browser Accept/Revert;
- annotation disabled until a real target exists;
- inspectable 390px staged before/after comparison without horizontal
  document overflow; and
- distinct export confirmation, evidence completeness, integration readiness,
  and implementation readiness predicates.

This is a bounded L0 implementation plus selected trust/layout properties. It
does not prove the complete historical L1/L2 ambition, human ergonomics, or
release readiness.

## Runtime and surfaces

- **CLI:** `backend/src/cli/studio.ts` is the scriptable operation surface.
- **Preview:** `studio preview <sessionId>` serves a local loopback page that
  displays the current head, history, staged evidence, annotation, and
  reversible actions.
- **Application core:** owns state transitions, admission, projections, and
  handoff predicates.
- **Store:** persists session JSON plus HTML artifacts under the configured
  `STUDIO_DATA` directory.
- **External generator:** registers variants and proposes candidate HTML across
  the CLI seam.

The preview is not a deployed service and the Studio does not embed a model,
model key, MCP server, or autonomous in-process agent loop.

## Operations

The supported workflow includes:

```text
session open
prompt submit
variants register
baseline select | baseline commit
comment add
synthesize
batch approve
apply
accept | discard
revert
revisions
state
pending
cycle | watch
preview
handoff export --confirm
```

The click-to-annotate preview and `comment add` write the same comment contract.
Export is terminal-only in the documented flow.

## State contract

The session state vocabulary is:

1. `SessionInitialized`
2. `PromptCaptured`
3. `VariantsReady`
4. `BaselineReady`
5. `CommentsCaptured`
6. `MutationDrafted`
7. `MutationApproved`
8. `RevisionApplied`
9. `RevisionRecorded`
10. `SessionCompleted`

`RevisionApplied` means a candidate is staged for inspection; it is not the
accepted head. `RevisionRecorded` means an accepted or reverted append-only
revision is now current.

## Mutation admission

The implemented lane is:

```text
comments → deterministic batch → external proposal
         → pure validation → staged candidate
         → accept exact hash or discard → append revision
```

The core binds approval to a batch, checks staleness and scope, stages admitted
HTML, derives honest before/after evidence, and accepts only the inspected
candidate hash. Required validation failure writes no head revision.

The implementation includes the artifact content port, shared canonicalizer,
scope validation, two-gate staging/acceptance, and append-only revision
recording. It does not claim complete atomic compensation for every
mid-record crash or complete production DOM/CSS attribution semantics.

## Visible-change evidence

`DiffSummaryHonest` contains:

- per-`odId` structural fragments;
- total added/changed/removed counts;
- explicit style/global-unattributed evidence;
- explicit unattributed structural evidence; and
- `visibleChangeCount`.

A CSS-only mutation therefore cannot be represented as no visible change.
This contract is preserved through preview, state/revision responses, and
handoff.

## Browser action contract

Before the browser posts Accept or Revert, it must have:

- a live candidate or revision identity;
- the intended action;
- the expected target state;
- a visible change recap; and
- an explicit acknowledgment of that context.

Controls remain disabled without acknowledgment. The server independently
rejects missing acknowledgment and stale identity/state. The acknowledgment
is actor-neutral: it proves the live context was acknowledged, not who the
caller is and not whether that caller was authorized outside the route.

## Annotation and mobile contract

- Annotation is unavailable without current HTML.
- The annotation form remains disabled until the user selects an element with
  an actual `data-od-id`.
- Severity uses the domain’s constrained values:
  `blocker | high | medium | low`.
- At a 390px viewport, staged before/after evidence stacks vertically and the
  document does not overflow horizontally.

These are bounded interaction/layout assertions, not a comprehensive
accessibility certification.

## Handoff contract

Handoff export requires explicit actor-neutral confirmation in the application
use case, so every adapter inherits the gate. The bundle reports:

| Field | Exact predicate |
| --- | --- |
| `exportConfirmed` | Explicit confirmer was present. |
| `evidenceComplete` | `missingRefs.length === 0`. |
| `integrationReady` | Evidence complete, accepted head hash present, honest diff present. |
| `implementationReady` | Integration-ready, applied tasks present, unresolved comments absent. |

Confirmation is not an input to the other readiness predicates. None of these
fields grants release authorization.

## Acceptance evidence

From `projects/ui-prototyping-studio/backend`:

```bash
./node_modules/.bin/tsc -p tsconfig.json --noEmit
./node_modules/.bin/tsx --test "src/**/*.test.ts"
./node_modules/.bin/playwright test --reporter=list
```

The 2026-07-27 completion audit requires TypeScript to pass, unit/slice
**72/72** to pass, and Playwright **21/21** to pass. The browser suite includes
the current-head, CSS-only, action acknowledgment, annotation, independent
process, and 390px witnesses.

Passing these commands is implementation evidence for the checked-out bytes.
It is not publication, deployment, human-study evidence, or release approval.

## Non-goals and residue

- No claim of release or production authorization.
- No claim that caller identity is inferred or enforced by the Studio core.
- No full human trust/control study.
- No full accessibility certification.
- No complete atomic-design registry, identity DNA, or conformance algebra.
- No learned preference/fitness authority.
- No production-complete DOM reorder/CSS cascade attribution proof.
- No complete crash-compensation proof across all record operations.

Historical research questions remain study inputs, not blockers that silently
reopen the completed implementation chain.

## Authority and next route

Lifecycle authority is [.craft/ledger.yml](.craft/ledger.yml), projected into
[CRAFT.md](CRAFT.md). The governed-state implementation frontier ends when all
seven GSP Task Session receipts and their joined closeout receipts pass.
Human-study and release routes require separately bound owners and evidence;
they are not successor implementation SWUs.
