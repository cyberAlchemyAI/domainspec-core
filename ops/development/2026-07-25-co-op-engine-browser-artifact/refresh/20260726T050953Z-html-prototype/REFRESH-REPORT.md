# Invoke Refresh Report: L0 HTML Prototype

## Result

- Mode: `refresh`
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: library
- Phase status: `pass`
- Phase-status basis: the exact Refresh artifact is complete and has zero
  refresh-authoring blockers
- Activation source: `direct-user`
- Mutation mode: `apply-approved`
- Mutation-mode source: `default-direct-user`
- Handoff readiness: `ready` for the refreshed Plan; HTML execution remains
  target-lifecycle gated
- Mutation ready: `true` for the admitted refresh package
- Evidence date: 2026-07-26

## Applied Decision

L0 now contains two serial proofs:

1. `SWU-COOP-001` remains the only selected unit and retains its exact
   four-file record-admission scope.
2. `SWU-COOP-002` is added as planned-unselected. It may later create only
   `projects/co-op-engine/prototype.html`, containing the event invitation,
   45-minute route, and all fourteen claim-bounded project opportunities.

The additive interpretation follows the user’s “add as L0” wording and avoids
invalidating the selected trust proof. The HTML unit cannot execute until
`SWU-COOP-001` passes and closes, an operator explicitly selects
`SWU-COOP-002`, and a fresh strict context pack passes.

## Source Signals

| ID | Type | Claim | Safety |
| --- | --- | --- | --- |
| `RS-HTML-001` | `route_changed` | Direct user requests an HTML prototype using the projects in L0. | safe inside Invoke-authored Plan paths |
| `RS-HTML-002` | `status_changed` | A separate HTML SWU is planned-unselected; the existing selected SWU remains singular. | safe after Distill |
| `RS-HTML-003` | `evidence_added` | Existing UX acceptance and Playwright CLI availability support a real-browser prototype validation contract. | safe as planned evidence only |
| `RS-HTML-004` | `artifact_drift` | Adding the SWU changes manifest, closeout, Distill, and validation bytes selected by the existing strict pack. | safe only with exact digest rebinding |

## Applied Changes

- Core Plan:
  `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, `EXECUTION-PACK.md`,
  `SWU-MANIFEST.json`, `CLOSEOUT-SYNC-CONTRACT.json`,
  `VALIDATION-STRATEGY.md`, and `PLAN-DISTILL-VALIDATION.md`.
- New execution contracts:
  `work-pack/tasks/TASK-COOP-L0-HTML-PROTOTYPE.md` and
  `work-pack/waves/W2.md`.
- Shared work-pack projections:
  `work-pack/shared/context.md`, `traceability.md`,
  `cross-task-decisions.md`, and `cross-task-gaps.md`.
- Existing selected goal handoff:
  `session-evidence/20260726T044915Z-swu-coop-001/CONTEXT-PACK.md` and
  `CONTEXT-PACK.index.json` were re-bound to the four changed selected-source
  digests.

Every applied target maps to at least one `RS-HTML-*` signal in
`refresh-report.json`.

## HTML SWU Boundary

The future prototype:

- is one dependency-free semantic HTML file;
- uses exactly fourteen research-bounded project articles;
- gives each article a current bounded description, limitation, seven-day
  act, and human ask;
- uses the same document for scrolling and projected facilitation;
- includes anchor navigation and inline low-fidelity responsive/print styles;
- is checked in a real browser at desktop and mobile sizes.

It excludes JavaScript, forms, remote resources, storage, network behavior,
admitted-data projection, final Whisper copy, hidden presenter content,
deployment, and every operational exchange transition.

## Distill

- Mode: Standard
- Rounds: two
- Role path: local Proposer/Balancer simulation; no subagent dispatch
- Verdict: `pass`
- Task-shaped count: zero
- Recomposition: record proof → static content/IA probe → admitted L1
  projections → reciprocal L2 behavior → final-copy/audit/deployment L3
- Child evidence: `REFRESH-DISTILL-VALIDATION.md`

## Dispatch and Material Package

- Dispatch: `refresh.dispatch.json`
- Dispatch validation: `pass`, zero flags and blocks
- Material package ID:
  `co-op-engine-l0-html-refresh-20260726T050953Z`
- Canonical package digest:
  `be620fbf3d2105c0857f9fedd72d280e59582ff0f94aa65a0a1b6348998503be`
- Patch verdict: `pass`
- Mutation handoff: `ready`
- Validated paths: 15
- Dependency result: `pass`
- Owner boundary: `pass`
- Publication boundary: `pass`
- Material receipt: `material-receipt.json`
- Handoff result: `handoff-result.json`

## Validation

- Dispatch Spec: pass.
- Material-package identity, digest, sources, outputs, dependencies, paths,
  owner, and internal-publication boundary: pass.
- Refresh handoff: `mutationReady=true`.
- Applied bytes equal every staged output: pass.
- `SWU-MANIFEST.json`, `CLOSEOUT-SYNC-CONTRACT.json`, and selected context
  index parse: pass.
- Exactly one selected SWU remains `SWU-COOP-001`: pass.
- Exactly one planned-unselected SWU exists and its write scope is only
  `projects/co-op-engine/prototype.html`: pass.
- Fourteen project fixture rows: pass.
- Existing strict goal pack: 12/12 obligations, all eight source digests
  current, zero gaps.
- Local links: pass.
- Scoped diff hygiene: pass.
- `projects/co-op-engine/`: still absent and untouched.

## Blockers by Lifecycle Scope

- Refresh authoring: 0
- Apply authorization: 0
- Target lifecycle: 2
  - `SWU-COOP-001` has not executed or closed.
  - `SWU-COOP-002` is not selected and has no strict runtime pack.
- Audit: 2
  - HTML browser evidence and later copy/coherence/comprehension/privacy
    evidence are unexecuted.
  - D-005 naming/publication review remains open before public access.

These later blockers do not lower the complete Refresh artifact.

## Capability Ceilings

This run establishes a validated, applied Invoke Refresh artifact only. It
does not establish registry release, durable mutation-runtime readiness for the
Invoke capability, prototype implementation, passing browser evidence, audit
completion, deployment, or publication.

## Observability

- Invoke Refresh row: recorded at central ledger line 353.
- Linked Distill child row: recorded at central ledger line 354.
- Parent/child dedupe keys: each present exactly once.
- Distill runtime-event emission: not configured; validation artifact retained.
- Reflection trigger: `output-threshold`; recommendation `reflect-now`.

Telemetry is non-authoritative and does not change the `pass` verdict,
mutation receipt, SWU selection, or next route.

## Next Route

`task-session` or an explicitly started native goal for the still-selected
`SWU-COOP-001`. Do not route `SWU-COOP-002` until its dependency, selection,
and strict-pack gates pass.
