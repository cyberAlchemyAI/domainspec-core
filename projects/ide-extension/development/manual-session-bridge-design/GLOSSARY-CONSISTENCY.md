---
id: ide-extension-manual-session-bridge-glossary-consistency
project: ide-extension
title: "Manual Session Bridge Glossary Consistency"
status: approved
node_type: glossary-consistency
updatedAt: 2026-07-12
---

# Manual Session Bridge Glossary Consistency

## Scope

This report checks the bridge design against terminology already used in
`projects/ide-extension/SPEC.md`, `projects/ide-extension/ARCHITECTURE.md`, the
current schemas, and the local Approval Desk. It does not promote terms into
Arcanum definitions or any canonical registry.

## Existing Terms Reused

| Term | Existing meaning | Bridge use | Result |
| --- | --- | --- | --- |
| Agent envelope | Typed proposal for an agent boundary crossing. | Carries task, skill slug, grants, approval, state, and receipt handles. | consistent |
| Approval | Human authorization required before protected execution. | Authorizes read-only claim attempts until terminal result or rejection. | consistent after current implementation is corrected |
| Requested grant | Declared effect/capability requested by an envelope. | `skill.invoke` plus `preview.read` in the first bridge. | extension required |
| Receipt | Kernel-owned durable evidence of an authorization or execution boundary crossing, with a typed kind. | Separate authorization and execution receipts. | accepted extension |
| Evidence ref | Stable handle to bounded evidence. | Links result summary, skill hash, validation, and before/after artifacts. | consistent |
| Agent ref | Identifier for the intended executor class. | `codex.current-session`. | consistent but unattested |
| Typestate | Allowed envelope lifecycle transitions. | Adds `approved`, `ready_for_poll`, `claimed`, and `interrupted` before terminal result. | accepted extension |

## Local Candidate Terms

| Candidate term | Working definition | Owner | Promotion status |
| --- | --- | --- | --- |
| Manual poll | Explicit operator message that instructs the active session to inspect the bridge queue once. | manual session bridge design | local candidate |
| Bridge request | Approved agent envelope eligible for one current-session claim. | ide-extension kernel | local candidate |
| Claim | Atomic kernel record assigning one approved bridge request to one session ref. | ide-extension kernel | local candidate |
| Claim packet | Response returned only after a successful claim; first bridge response that contains the skill slug and task. | bridge API | local candidate |
| Late skill disclosure | Rule that omits the skill from agent-facing pre-claim responses and reveals it only in the claim packet. | bridge protocol | local candidate |
| Session ref | Caller-supplied identifier for the active Codex session. | Codex session/bridge API | local candidate, assurance `unattested` |
| Execution result | Claim-bound terminal status, bounded summary, validation, skill hash, and evidence refs posted by the session. | active session, admitted by kernel | local candidate |
| Execution receipt | Kernel-minted durable receipt created only after a valid execution result is admitted. | ide-extension kernel | local candidate |
| Authorization receipt | Kernel-minted evidence that the human approved a bound task, skill, and effect profile; contains no execution claim. | ide-extension kernel | local candidate |
| Effect profile | Named set of effects the bridge permits for a request. | grant policy | local candidate; first profile is `preview.read` |
| Ready target | The single approved proposal selected by the operator for the next manual poll. | Approval Desk/kernel | local candidate |
| Operator requeue | Human-only release of an interrupted read-only claim back to approved state with attempt history preserved. | Approval Desk/kernel | local candidate |

## Conflicts And Required Deltas

### GC-001: Approval Receipt Versus Execution Receipt

Current behavior calls the approval-stage artifact a receipt with execution
status `passed` and moves the envelope directly to `passed`. The approved bridge
design keeps an approval-stage receipt but types it as authorization evidence,
then creates a separate receipt for actual skill execution.

- Required repair: approval appends an `authorization.receipt` with no execution
  status and changes the envelope to `approved`; `skill.execution` is minted
  only after result admission.
- Owner: ide-extension schema/projector/server implementation route.
- Gate: blocks truthful bridge implementation if not repaired.

### GC-002: `consumed` Approval Timing

Current behavior marks approval consumed during the approve call. The bridge
needs the approved authorization to survive target selection, read-only claim
attempts, and explicit operator release/requeue until a terminal result.

- Required repair: distinguish `approved` from `consumed`; consume atomically
  with an admitted terminal result. Every claim/release attempt remains bound to
  the same authorization receipt in L0.
- Owner: approval-record schema and projector.
- Gate: blocks replay-safe claim behavior if not repaired.

### GC-003: `run` Meaning

The existing run endpoint is a dry-run state query after approval. The bridge
uses execution to mean skill contract execution by the active session.

- Required repair: do not reuse `/run` as a hidden alias for claim. Add explicit
  bridge request/claim/result interfaces.
- Owner: bridge API.
- Gate: naming consistency requirement, not a canonical vocabulary promotion.

### GC-004: Session Identity

`codex.current-session` identifies an intended execution lane but does not prove
which process or chat claimed it.

- Required repair: every claim and receipt says `assurance: unattested`.
- Owner: claim/result schemas and UI content.
- Gate: blocks any authenticated-session claim, but not the local manual proof.

## Consistency Result

- Result: `pass`.
- Canonical conflicts: none; no canonical terms were changed.
- Local implementation deltas: four, all accepted and named above.
- Plan readiness: pass; the plan must make GC-001 and GC-002 part of the first
  implementation slice and preserve GC-003/GC-004 as validation obligations.
