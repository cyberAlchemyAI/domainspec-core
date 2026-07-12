---
id: ide-extension-operations-v1-architecture
project: ide-extension
title: "Operations V1 Architecture Bundle"
status: design-ready
node_type: architecture-bundle
updatedAt: 2026-07-12
---

# Architecture Bundle: Operations V1

## Design Intent

Turn the local workbench into a small HTML builder and consolidator without
changing the complete-file V0 protocol.

```text
selected V0 revision
  -> derive a new operations_v1 surface
  -> append | replace | rebuild whole-document content
  -> commit an immutable result revision
  -> notify an already-displayed surface
  -> later target declared regions through the same operation boundary
```

The original V0 surface remains a workspace-file projection. The derived
surface is a distinct object with kernel-owned immutable revision bodies.

## 1. Context View

### Product Boundary

The user can ask an active agent to add a section, replace the page, or rebuild
the workbench from another project HTML source. Each successful operation
produces a complete usable HTML revision. The browser never renders partial
operation bytes.

Operations V1 is still a trusted-local value surface. It does not claim hostile
HTML containment, remote collaboration, arbitrary browser authority, or effect
completion.

### Actors And Ownership

| Actor | Owns |
| --- | --- |
| Human operator | Intent, visible use, and any later protected-effect decision. |
| Active agent/session | Operation proposal, payload/source selection, expected revision, and retry identity. |
| Local kernel | Surface derivation, serialized compare-and-set, immutable body storage, operation records, projection, and notices. |
| Browser workbench | Display pointer, complete-revision reload, navigation acknowledgement, and user interaction forwarding. |
| V0 workspace surface | Mutable project file and its existing complete-file publication behavior. |
| Operations V1 surface | Derived lineage, immutable revision bodies, and ordered committed operations. |

### Authority Boundary

Canvas display mutation is a declared trusted-local preview/display exception,
not authorization for shell, filesystem write, network, Craft execution, or
other protected effects. Operation records are audit evidence for content
construction; they are not `skill.execution` receipts.

## 2. High-Level Structure View

```text
Agent / session CLI or local client
  |
  +-- derive operations surface
  +-- submit ContentOperation
  +-- submit NavigationCommand
  |
  v
Local HTTP server
  |
  +-- OperationsSurfaceService
  +-- HtmlTransformEngine
  +-- CanvasBlobStore
  +-- CanvasProjector / EventStore
  +-- CanvasNotificationStream
  |
  v
Browser workbench
  +-- DisplayTargetController
  +-- complete revision iframe
  +-- refresh / redirect acknowledgement
```

The event log stores metadata, lineage, request digests, and result references.
HTML bodies live in a content-addressed blob store beneath
`.ide-extension/state/`, not in `events.jsonl`.

## 3. Low-Level Component View

### Surface Derivation

```text
derive_operations_surface(
  source_v0_surface_id,
  source_revision_id,
  operation_surface_idempotency_key
) -> new_operations_v1_surface_id
```

Derivation rules:

1. Resolve the exact selected V0 surface and revision.
2. Read its content only if the workspace bytes still match that revision.
3. Fail `source_revision_unavailable` when V0 content drift prevents an exact
   copy; do not silently derive from newer bytes.
4. Write the bytes to the content-addressed blob store.
5. Append `canvas.operations_surface_derived` with source lineage and initial
   result revision.
6. A repeated derivation key with identical normalized input returns the same
   derived surface. Reuse with different input fails.

Derivation does not mutate, promote, synchronize, or redirect the source V0
surface.

### Content Operation Contract

```text
ContentOperation {
  schema_version: "1"
  operation_id
  operations_surface_id
  expected_revision_id
  mode: append | replace | rebuild
  target: { kind: whole_document }
  input: InlineHtml | WorkspaceHtml
}

InlineHtml {
  kind: inline_html
  html
}

WorkspaceHtml {
  kind: workspace_html
  path
  expected_sha256
}
```

Mode semantics:

| Mode | Input interpretation | Deterministic postcondition |
| --- | --- | --- |
| `append` | Parse input as an HTML fragment and append its nodes to the current document body. | Existing document remains; parsed nodes become the final body children in input order. |
| `replace` | Parse input as a complete HTML document. | Result is exactly the transformer serialization of that document. |
| `rebuild` | Read an exact-hash workspace HTML document and parse it as complete HTML. | Result becomes a new revision derived from the named source while preserving operations-surface identity and lineage. |

`append` fails when the current revision cannot produce one document body.
`replace` and `rebuild` fail when complete-document parsing fails. A standards-
capable HTML parser is required; regex and closing-tag string insertion are not
valid implementations.

### Operation Record

```text
OperationRecord {
  operation_id
  operations_surface_id
  normalized_request_digest
  source_revision_id
  mode
  target
  status: committed
  result_revision_id
  result_digest
  result_blob_ref
  committed_at
}
```

The normalized request digest binds all semantic fields plus the input byte
digest. The event log does not copy the HTML payload.

### Compare-And-Set And Retry

Inside the existing serialized mutation boundary:

1. Look up `operation_id`.
2. When it exists with the same normalized digest, return the original result
   with `idempotent: true`.
3. When it exists with a different digest, fail `operation_id_conflict`.
4. Compare `expected_revision_id` with the surface current revision.
5. On mismatch, fail `revision_changed` and report the current revision.
6. Transform the current immutable bytes into candidate complete bytes.
7. Write the content-addressed blob through temporary-file plus atomic rename.
8. Append `canvas.content_operation_committed` referencing the blob.
9. Project the result revision and emit a state-change notice.

An orphan blob after failed event append is safe residue and may be garbage-
collected. An event must never commit before its referenced blob is durable.

### Storage Namespaces

| Namespace | Contents | Authority |
| --- | --- | --- |
| Workspace | V0 source HTML and explicit rebuild sources. | Project/session. |
| `events.jsonl` | Derivation and operation metadata, lineage, digests, result refs. | Kernel append boundary. |
| `workbench.json` | Projected operation surfaces, revisions, records, display target. | Kernel projection. |
| `canvas/blobs/<sha256>.html` | Immutable complete revision bodies. | Kernel blob store. |
| Browser iframe | Currently selected complete revision. | Display only. |

### HTTP Interface

| Interface | Purpose |
| --- | --- |
| `POST /api/canvas/operation-surfaces` | Derive a new operations surface from an exact V0 revision. |
| `GET /api/canvas/operation-surfaces/:surfaceId` | Read lineage, current revision, and operation metadata. |
| `POST /api/canvas/operation-surfaces/:surfaceId/operations` | Apply one CAS-guarded content operation. |
| `GET /api/canvas/operation-surfaces/:surfaceId/revisions/:revisionId/content` | Serve one immutable complete body. |
| `POST /api/canvas/navigation` | Redirect, show a surface revision, or refresh display without a content revision. |

Existing V0 routes, request schemas, surface identities, and current behavior
remain valid and unchanged.

## 4. Workflow Process View

### Derive And Display

1. Agent publishes or selects a V0 surface/revision.
2. Agent derives an operations surface from that exact revision.
3. Kernel copies the exact V0 bytes into immutable storage and records lineage.
4. Agent sends a navigation command selecting the derived revision.
5. Workbench loads it and acknowledges the command.

### Append A Section

1. Agent reads the operations surface current revision.
2. Agent submits `append` with a fresh operation id and expected revision.
3. Kernel parses current document plus fragment under the mutation queue.
4. Kernel stores and commits the complete result revision.
5. If this surface is displayed, the workbench reloads after the commit notice.

### Retry After Ambiguous Response

1. Client repeats the exact request and operation id.
2. Kernel returns the original committed result.
3. The fragment is not appended twice.

### Stale Concurrent Operation

1. Two clients read revision `r1`.
2. First operation commits `r2`.
3. Second operation against `r1` fails `revision_changed`.
4. Client must inspect `r2` and issue a new operation; no automatic merge occurs.

## 5. Decision Flow View

```text
request arrives
  -> valid operations surface?
  -> operation id already known?
       same digest -> return original result
       different digest -> conflict
  -> expected revision current?
       no -> revision_changed
  -> input source admitted and exact?
  -> parse/transform succeeds?
  -> blob durable?
  -> event append succeeds?
  -> project revision
  -> notify if displayed
```

Rejected operations create no content revision. Whether rejected attempts need
a separate diagnostic log is deferred; they are not represented as committed
operation records.

## 6. Dependency And Interface View

| Dependency | Required contract | Failure behavior |
| --- | --- | --- |
| Existing V0 canvas | Stable surface/revision lookup and exact-byte content admission. | Drifted source fails derivation. |
| HTML parser/serializer | Document and fragment parsing with deterministic project-selected serialization. | Parse/shape error; no blob/event. |
| Blob store | Content-addressed immutable write, read, existence check, atomic publish. | Operation fails before event append. |
| Event store/projector | Versioned derivation and operation events with deterministic replay. | Startup/replay fails closed on invalid committed reference. |
| Mutation queue | CAS check, blob preparation, and event append ordered per operation surface. | Stale operation returns conflict. |
| Notification stream | Complete-revision availability only. | Browser retains old revision and offers refresh. |
| Browser workbench | Display-target selection and command acknowledgement. | Content remains committed even when navigation fails. |

## Navigation Boundary

```text
NavigationCommand {
  schema_version: "1"
  command_id
  action: redirect | refresh
  destination?: {
    kind: surface_revision
    surface_kind: v0 | operations_v1
    surface_id
    revision_id
  }
}
```

- `redirect` changes the workbench display target to an admitted revision.
- `refresh` reloads the current display target.
- A content operation may trigger reload only when its surface is already the
  current display target; it does not redirect the user to another surface.
- Navigation commands do not create content revisions.
- Command acknowledgement and optional durable command history are separate
  from operation receipts.

## Additive Declared Regions

The first schema accepts only `target.kind: whole_document`. A later compatible
schema revision may add:

```text
target: {
  kind: declared_region
  region_id
}
```

Region compatibility rules:

- region identity is author-declared, for example `data-ide-region="summary"`;
- one operation resolves exactly one element;
- missing or duplicate region ids fail without mutation;
- a stale expected revision fails before region lookup;
- whole-document operation behavior remains unchanged;
- region replacement changes element contents or the element itself only after
  a separate design decision selects one stable semantic.

Region operations, scaffolding commands, and merge behavior are not part of
Operations V1 implementation readiness.

## Risks And Degradation

| Risk | Containment |
| --- | --- |
| Duplicate append after timeout | Operation-id replay returns original result. |
| Lost concurrent update | Expected-revision CAS rejects stale input. |
| Mutable V0 source drift | Exact revision derivation fails rather than copying newer bytes. |
| Event references absent body | Blob is durable before append; replay validates references. |
| Parser normalization surprises | Revision digest covers emitted bytes; tests preserve required document structure. |
| Script mutates DOM at runtime | Accepted trusted-local limitation; persisted source revision remains unchanged. |
| Navigation failure | Content commit survives; workbench retains prior display and exposes Refresh. |
| Future region ambiguity | Stable ids and exactly-one resolution gate the additive extension. |

## Validation Strategy

Design handoff requires future planning to cover:

- V0 compatibility and unchanged `/api/canvas/publish` behavior;
- exact-source derivation and drift failure;
- append, replace, and rebuild parser semantics;
- stale revision and duplicate operation-id matrices;
- crash boundaries between blob write and event append;
- mixed V0 and Operations V1 replay/restart;
- complete-revision notification and navigation acknowledgement;
- malformed, missing, and duplicate future region fixtures before region work;
- real browser evidence that appended HTML becomes interactive.

## Honest Claim

Passing an Operations V1 implementation would support:

> A trusted local agent can derive an immutable workbench surface from an exact
> V0 HTML revision, apply retry-safe whole-document HTML operations, and display
> each committed complete revision without changing the original V0 API.

It would not support collaboration, automatic merging, arbitrary HTML safety,
remote control, or region-scoped mutation until those layers are separately
designed and proven.
