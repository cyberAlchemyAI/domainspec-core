---
id: ide-extension-v0-canvas-repair-implementation-plan
project: ide-extension
title: "V0 Canvas Repair Implementation Plan"
status: ready
node_type: implementation-plan
updatedAt: 2026-07-12
---

# Implementation Plan: V0 Canvas Repair

## Objective

Close the accepted current-V0 findings while preserving the existing API,
surface identity, workspace-file authority, and trusted-local value posture.

## Source Design References

- `projects/ide-extension/SPEC.md`
- `projects/ide-extension/ARCHITECTURE.md`
- `projects/ide-extension/development/session-content-canvas-design/ARCHITECTURE-BUNDLE.md`
- `projects/ide-extension/development/session-content-canvas-design/DECISIONS.md`
- `projects/ide-extension/development/html-builder-architecture-review/findings.md`

## Delivery Boundary

### Included

- explicit trusted-local canvas preview/display exception;
- precise separation of canvas audit events from execution receipts;
- canonical root and target containment;
- file-handle-based complete read;
- publish and content-route error mapping;
- adversarial symlink and compatibility tests;
- integrated validation and review traceability.

### Excluded

- approval UI/schema for canvas publication;
- Operations V1 implementation;
- HTML parser, blob store, operation records, navigation commands, or regions;
- hostile concurrent filesystem guarantees beyond portable Node primitives;
- snapshots, remote access, multi-user isolation, or effect-completion claims.

## Policy Algorithm

Amend the owner contracts so they say:

1. Approval and execution receipts apply to protected effects.
2. Trusted-local canvas publication and display update only local preview state
   from an operator-controlled workspace HTML file.
3. Canvas publication is a narrow declared exception to approval and execution-
   receipt requirements.
4. `canvas.surface_published` remains an append-only audit event with surface
   and revision evidence. It is not a receipt under the receipt schema.
5. Any source write, shell, network, domain action, export, commit, push,
   provider call, or remote browser action still uses its owning gate.

This resolves the review contradiction without pretending that publication has
an approval or receipt record it does not currently produce.

## Canonical Admission Algorithm

`readWorkspaceHtml(workspaceRoot, requestedPath)` should:

```text
relativePath = normalizeCanvasPath(requestedPath)
lexicalRoot = resolve(workspaceRoot)
lexicalTarget = resolve(lexicalRoot, relativePath)
require lexicalTarget beneath lexicalRoot

canonicalRoot = realpath(lexicalRoot)
canonicalTarget = realpath(lexicalTarget)
require canonicalTarget beneath canonicalRoot using path.relative

handle = open(canonicalTarget, read-only, no-follow-final-link when supported)
try:
  metadata = handle.stat()
  require metadata.isFile()
  bytes = handle.readFile()
finally:
  handle.close()

return original normalized relative path,
       canonical absolute target,
       bytes, length, and SHA-256(bytes)
```

Containment helper rule:

```text
relative = path.relative(canonicalRoot, canonicalTarget)
contained = relative != ".."
         && !relative.startsWith(".." + path.sep)
         && !path.isAbsolute(relative)
```

The exact selected bytes come from one opened handle. This does not claim an
atomic filesystem snapshot against hostile in-place writers. Documentation
must replace the ambiguous phrase "one complete read" with this narrower
guarantee.

## Error Semantics

| Condition | Publish result | Content-fetch result | Event effect |
| --- | --- | --- | --- |
| Invalid lexical path | existing `400 invalid_canvas_path` | not reachable from valid surface | none |
| Missing target/ancestor | existing `404 canvas_file_not_found` | `404 canvas_file_unavailable` | none |
| Canonical target outside root | `400 canvas_path_escape` | `404 canvas_file_unavailable` | none |
| Target not regular file | `400 canvas_not_file` | `404 canvas_file_unavailable` | none |
| In-root symlink to in-root HTML | admitted by canonical target | served when digest matches | normal |
| Published path later retargeted outside | n/a | `404 canvas_file_unavailable` and no bytes | none |

The content route maps containment failures to unavailable rather than leaking
the external canonical path.

## Implementation Tasks

| Task | SWUs | Outcome |
| --- | --- | --- |
| Canvas policy contract | `SWU-VCR-001` | Specification and architecture agree on trusted-local exception and audit semantics. |
| Canonical path admission | `SWU-VCR-002`, `SWU-VCR-003` | Helper and both server paths reject external resolved targets with regression coverage. |
| Integrated verification | `SWU-VCR-004` | Full scoped evidence closes the accepted V0 findings. |

## Validation Strategy

- `npm run test:canvas-publish`
- `npm run test:canvas-replay`
- `npm run test:canvas-contracts`
- focused new path-admission test command or direct `node --test` path
- `npm run test:bridge`
- `npm run validate:schemas`
- documentation phrase and review-ID checks with `rg`
- `git diff --check` scoped to V0 repair files and evidence

No Playwright run is required unless the path change affects browser loading in
the integrated suite. Browser UI behavior is intentionally unchanged.

## Rollback And Failure

- A failed policy SWU leaves source code untouched.
- A failed path-admission SWU must not weaken lexical validation to make tests
  pass.
- If portable Node primitives cannot meet the retained symlink counterexample,
  return `block` with the exact platform gap; do not claim hostile-race safety.
- Existing V0 behavior remains the rollback baseline; no state migration is
  planned.
