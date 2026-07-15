---
id: ide-extension-domainspec-roadmap-lab-implementation-layering
status: planned
updatedAt: 2026-07-14
docType: implementation-layering
---

# Implementation Layering: DomainSpec v2 Roadmap Lab

## Target And Rule

- Target: trusted-local Roadmap Lab in `projects/ide-extension`, backed by the
  private DomainSpec v2 roadmap projection.
- Current state: brownfield Canvas and roadmap presentation; Roadmap Lab not
  implemented.
- Readiness target: one-person pilot, not a production multi-user service.

Every boundary uses the same rule:

> After this layer, we know whether the named decision is supported by retained
> evidence. If not, stop, narrow, or redesign before promotion.

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included scope | Deferred scope | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 — useful loop | After this layer, do we know whether a newcomer can understand FPR-01 and submit one durable, reviewable proposal? | Validated copy/event contracts; deterministic FPR-01 learning packet; focused Roadmap Lab route; restatement, source request, proposal, and stored acknowledgment through existing Canvas. | Stable copy fields, dual binding, FPR-01, semantic events, keyboard/error basics, existing Canvas regression. | All-node coverage, history across revisions, owner handoff mechanics, identity, remote operation. | Schema/fixture/build tests, deterministic fingerprint, Node/Playwright one-node round trip, retained event payload. | Continue only if the participant-facing loop is usable and authority boundaries remain intact. |
| L1 — repeatability | After this layer, do we know whether the same model holds across roadmap node classes, revisions, and restart? | Coverage over all rendered nodes/fields plus proposal-history and stale-review projection. | Coverage matrix, representative node fixtures, restart replay, revision/fingerprint mismatch, preserved original proposals. | Owner-specific application, remote/multi-user concurrency, generic source browsing. | Coverage and golden-build tests, mixed-history/restart tests, stale cases, browser evidence across representative nodes. | Harden the route only if repeatability does not require per-node special cases. |
| L2 — governance and failure | After this layer, do we know whether proposals reach the correct owner and fail safely without authority leakage? | Deterministic proposal classification, review packet, unsupported-action denial, disposition evidence projection, retry/degraded paths. | Copy/claim/Craft/research classification; owner handles; evidence reference checks; bounded/retry/stale behavior. | Direct owner execution, production authorization, accounts, notifications, remote collaboration. | Valid/invalid routing fixtures, no-direct-effect assertions, denied/failed/retry browser tests, owner-boundary review. | Enter the human pilot only if submission cannot masquerade as acceptance or application. |
| L3 — human value and closed loop | After this layer, do we know whether a new person can use the lab and whether one accepted copy improvement can close with evidence? | Real Victor trial plus one owner-accepted presentation-copy update, rebuild, republish, and before/after receipt. | 30-minute protocol, truthful confusion/help capture, accepted copy route, new fingerprint/revision, closeout audit. | General release, multi-user service, graph/Craft automated mutation, scale/SLO claims. | Human trial report, retained proposal, owner acceptance, source diff, builder/test pass, new Canvas revision, closeout trace. | Approve a separate productionization/hardening plan, narrow the product, or stop; do not call this general production. |

## Nested Layer Boundaries

The feature contains two independent but ordered decisions:

1. **Roadmap projection contract:** copy IDs and input fingerprints must be
   stable before the UI can make a reviewable proposal.
2. **IDE interaction loop:** the focused route and proposal history must prove
   value before owner automation or broader lifecycle integration.

Neither may skip L0. Owner routing is L2 even if a simple classifier is easy to
write, because its correctness is a governance claim, not merely a parsing
claim.

## Non-regression Guardrails

- Preserve existing Canvas schemas, mixed-history replay, current-revision
  admission, 16 KiB request cap, complete-file publication, restart, and manual
  refresh behavior.
- Keep presentation copy separate from node/claim/Craft authority.
- Never convert a submitted or disposition-reference event into an owner
  receipt.
- Later layers must continue to accept copyable source paths when source request
  processing is unavailable.
- Later coverage must use the same contract rather than per-node UI forks.
- A dirty-worktree ownership review precedes every mutation-capable SWU.

## Recommended Next Layer

- Next layer: L0.
- First unit: `SWU-RDL-001`, the presentation-copy oracle.
- Why: every targeted copy proposal, build coverage check, and round trip needs
  stable field identity before template or UI code changes.
- Major deferral: production authorization and multi-user hardening remain a
  separate post-pilot design problem.

