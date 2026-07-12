---
id: ide-extension-operations-v1-decisions
project: ide-extension
title: "Operations V1 Decision Ledger"
status: design-ready
node_type: decision-record
updatedAt: 2026-07-12
---

# Decision Ledger: Operations V1

## OV1-D1: Compatibility By Separate Identity

- Decision: deriving Operations V1 creates a new surface id.
- Reason: changing an existing V0 surface in place would either break old
  clients or let complete-file writes bypass operation CAS.
- Consequence: the source V0 surface and `/api/canvas/publish` remain unchanged.

## OV1-D2: Kernel-Owned Immutable Bodies

- Decision: derived revision bodies live in a content-addressed kernel blob
  store.
- Reason: operation replay, historical content, and retries cannot honestly
  depend on a mutable workspace path.
- Consequence: V0 remains workspace-canonical; Operations V1 becomes blob-
  canonical after derivation.

## OV1-D3: Complete Revision Is The Commit Unit

- Decision: every operation transforms one committed revision into another
  complete revision.
- Reason: the workbench must never display a half-applied fragment.
- Consequence: streaming means progressive complete revisions, not HTML tokens.

## OV1-D4: Whole-Document First

- Decision: schema version 1 supports only `target.kind: whole_document`.
- Reason: whole-document semantics can prove the operation protocol before
  region identity and merge policy add complexity.
- Consequence: declared regions remain an additive schema target.

## OV1-D5: Operation Semantics

- `append`: parse fragment and append nodes to the document body.
- `replace`: parse and replace with a complete inline document.
- `rebuild`: replace from an exact-hash workspace HTML source while recording
  source lineage.
- Decision: all transformations use an authoritative HTML parser/serializer.
- Consequence: string insertion and regular-expression document mutation are
  forbidden implementation shortcuts.

## OV1-D6: CAS And Idempotency

- Decision: every operation carries `expected_revision_id` and `operation_id`.
- Same id plus same normalized input returns the original result.
- Same id plus different normalized input fails.
- Stale expected revision fails without automatic rebase or merge.

## OV1-D7: Navigation Is Not Content

- Decision: `redirect` and display `refresh` use a separate navigation command.
- Consequence: navigation never creates a content revision. A commit reloads
  only when the mutated surface is already displayed.

## OV1-D8: Trusted-Local Authority

- Decision: canvas publication, operation commits, and workbench display are a
  declared trusted-local preview/display exception.
- Consequence: they create audit events and operation records, not protected-
  effect approvals or `skill.execution` receipts. Any shell, network,
  filesystem write outside the blob namespace, or domain action remains behind
  its owning authority path.

## OV1-D9: No Implicit Synchronization

- Decision: later V0 republish does not update a derived operations surface.
- Consequence: refresh from workspace is an explicit `rebuild` operation or a
  new derivation, both with visible lineage.

## Deferred Decisions

1. Exact parser package and version.
2. Maximum inline HTML and fragment request sizes.
3. Blob garbage-collection retention.
4. Durable versus ephemeral navigation command history.
5. Region replacement semantics and scaffolding commands.
6. Automatic merge or collaboration, if ever justified.

None blocks architecture handoff. Items 1 through 4 must be resolved by an
Operations V1 implementation plan before mutation-capable execution.
