# FINAL Findings

Registered dispatch: `2026-07-12-html-builder-architecture-review`

## Scope Resolution

The reviewed V0 contract specifies complete-file publication (`SPEC.md:226`; `IMPLEMENTATION-PLAN.md:5`). It does not specify append, replace, rebuild, region targeting, operation IDs, or operation-level CAS.

Accordingly:

- **Section A** contains demonstrated V0 defects and explicitly labeled V0 clarifications.
- **Section B** contains obligations and recommendations for the proposed HTML-builder evolution.
- Evolution concerns remain because the registered review goal is an **HTML-builder architecture review**, and the submitted attacks explicitly examine the proposed append/replace/rebuild/region architecture.
- Historical snapshots and hostile-HTML containment remain deferred in V0 by `SPEC.md:252-258`.

# A. Current V0 Findings

## 1. `ARCHITECTURE.md`

**Verdict: FIX**

| # | File | Exact evidence | Severity | Proposed fix |
|---|---|---|---|---|
| G1-R | `projects/ide-extension/ARCHITECTURE.md` | Lines 14–16 require every effectful crossing to carry approval and receipts. Receipt-bearing replay branches validate an explicit receipt record, as shown for bridge results at `server.mjs:155-159`. Canvas publication validation at `server.mjs:163-169` contains only publish-request fields, while the committed event contains surface/revision data but no receipt record. | MAJOR | Either define canvas publication as an explicit exception to the receipt boundary or emit and validate a receipt record using the established receipt schema and semantics. |

`canvas.surface_published` is durable evidence that publication occurred. It is not, as currently shaped and validated, a receipt record under the architecture’s existing receipt semantics.

## 2. `SPEC.md`

**Verdict: FIX**

| # | File | Exact evidence | Severity | Proposed fix |
|---|---|---|---|---|
| G1-A | `projects/ide-extension/SPEC.md` | Line 24 places effects beyond preview/read behind approval. Lines 96–97 apply approval and receipt requirements to publication. The current route at `server.mjs:568-611` accepts publication without an approval input or approval-validation step. | MAJOR | Require approval for the existing publication route, or document a narrowly scoped trusted-local exception and align the specification with it. Address receipt handling separately under G1-R. |

This is the approval aspect of the cross-artifact authority finding. It does not depend on hypothetical builder filesystem writes.

Same-byte metadata handling is not retained as a defect. `SPEC.md:250-252` defines equal-content publication as idempotent, so the evidence does not establish that changed `title` or `kind` must create a new publication.

## 3. `src/server.mjs`

**Verdict: FIX**

| # | File | Exact evidence | Severity | Proposed fix |
|---|---|---|---|---|
| G1-I | `projects/ide-extension/src/server.mjs` | Lines 568–611 accept `{path,title,kind}` and durably commit `canvas.surface_published`. The route does not consume or validate approval. Receipt-bearing branches validate a receipt record at lines 155–159, but canvas publication validation at lines 163–169 has no receipt field, and the publication event’s surface/revision data is not shaped as such a record. | MAJOR | Implement the decisions from G1-A and G1-R directly on the publication route: validate approval unless explicitly excepted, and emit a schema-valid receipt unless publication is explicitly exempted from receipt semantics. |

The prior replay-integrity finding is dropped. The reviewed V0 contract does not establish that replay must revalidate every persisted publication field, and no demonstrated V0 failure was proven from the narrower validation.

## 4. `src/kernel/canvas.mjs`

**Verdict: FIX**

| # | File | Exact evidence | Severity | Proposed fix |
|---|---|---|---|---|
| K1 | `projects/ide-extension/src/kernel/canvas.mjs` | Lexical containment is checked with `path.resolve()` around line 31. `stat()` around line 39 and `readFile()` at line 46 subsequently follow symlinks without checking the target’s real path. An in-workspace symlink may therefore resolve outside `workspaceRoot`. | MAJOR | Enforce canonical realpath containment or an equivalent descriptor-based no-follow policy. Account for link replacement between validation and reading. |
| K2 | Same | `stat()` at line 37 and `readFile()` at line 46 are separate observations. They may describe different filesystem states if the file changes between calls. | MINOR clarification/hardening | Clarify that “one complete read” means one `readFile()` result rather than an atomic metadata/content snapshot, or add stable-identity verification if stronger coherence is desired. |

K2 is not a demonstrated V0 correctness failure. A single `readFile()` can reasonably satisfy the current complete-read intent; the concern is imprecise wording and optional hardening.

## 5. `IMPLEMENTATION-PLAN.md`

**Verdict: FIX**

| # | File | Exact evidence | Severity | Proposed fix |
|---|---|---|---|---|
| P1 | `projects/ide-extension/development/session-content-workbench-plan/IMPLEMENTATION-PLAN.md` | Lines 55–58 require the admitted file to remain beneath `workspaceRoot`. The implementation checks only lexical containment before following symlinks (`canvas.mjs:31-46`). | MAJOR | Define containment in terms of the resolved filesystem target and add a regression test for an in-workspace symlink pointing to an external HTML file. |
| P2 | Same | Line 109 describes concurrent change as yielding “one complete read,” while `canvas.mjs:37,46` performs separate metadata and content observations. The surrounding evidence does not promise an atomic snapshot. | MINOR clarification/hardening | Narrow the phrase to the actual `readFile()` guarantee or document and implement a stronger coherent-admission mechanism. |

# B. Proposed Evolution Obligations

These are reviewed conditions for the proposed architecture. They are not current V0 defects.

## Backward-Compatible Boundary

Do **not** promote or change an existing V0 surface in place.

```text
derive_operations_surface(
  source_v0_surface_id,
  source_revision_id
) -> new_operations_v1_surface_id
```

Recommended behavior:

- The original V0 surface keeps its identity and contract forever.
- Existing `/api/canvas/publish` behavior remains unchanged on that original surface.
- Existing clients continue publishing complete files to the original surface without operation-aware negotiation.
- Creating an operations surface produces a **new identity** derived from an explicitly selected V0 revision.
- The new `operations_v1` surface initially supports `whole_document` operations.
- Declared-region targeting may be added later without changing the original V0 surface.
- Subsequent changes to the V0 source surface do not implicitly overwrite or synchronize the derived operations surface.
- Synchronization, re-derivation, and lineage display remain explicit unresolved decisions.

This recommendation preserves V0 compatibility by isolation, not by teaching old clients new conflict behavior.

## Minimal Operation Envelope

```text
ContentOperation {
  operation_id
  operations_surface_id
  expected_revision_id
  mode: append | replace | rebuild
  target: whole_document
  payload_or_source
}
```

A later region extension may add:

```text
target: declared_region(region_id)
```

Each accepted operation should produce a durable record binding request and outcome:

```text
OperationRecord {
  operation_id
  normalized_request_digest
  source_revision_id
  status
  result_revision_id?
  result_digest?
  result_reference?
}
```

Complete operation-record validation is an evolution obligation. The operation replay path should validate identifiers, request/result binding, digest shape, status transitions, and any receipt required for effectful mutation.

## Transformation Obligations

- Verify `expected_revision_id` inside the serialized mutation boundary.
- Exact retries of an `operation_id` return the original result.
- Reuse of an operation ID with different normalized input fails.
- Whole-document transformation is the initial compatibility target for the new surface.
- Declared regions require stable author-declared IDs, uniqueness, exactly-one cardinality, and stale-target behavior.
- `append` needs a defined preservation rule under an authoritative parser.
- Static parsing does not contain runtime script effects. Trusted HTML, sanitization, browser sandboxing, and explicit deferral are distinct choices.
- `rebuild` requires authoritative inputs and a defined postcondition before implementation.

## Navigation Boundary

Navigation remains separate from content transformation:

```text
NavigationCommand {
  command_id
  destination
  optional_surface_id
  optional_revision_id
}
```

`navigate`, `redirect`, and display `refresh` should not create content revisions. Their durability, acknowledgement, ordering, and restart behavior remain unresolved.

# Attack Coverage

| Attack class | Files examined | Retained outcome | Refuted or evolution outcome |
|---|---|---|---|
| Formal | `ARCHITECTURE.md`, `SPEC.md`, `server.mjs` | Current publication approval and receipt contradiction retained as G1. | Operation CAS, IDs, recovery records, and revision algebra moved to evolution obligations. V0 replay-integrity finding dropped as unproven. |
| Empirical | `server.mjs`, `canvas.mjs`, `IMPLEMENTATION-PLAN.md` | Symlink escape retained as K1/P1. Publication trace retained as G1-I. | `stat`/`readFile` coherence demoted to MINOR clarification because no atomic-snapshot V0 guarantee was proven. |
| Adversarial | `SPEC.md`, `server.mjs`, `canvas.mjs` | External-target symlink counterexample retained. | Region ambiguity, malformed append, duplicate IDs, and script mutation apply only to the proposed evolution or deferred hostile-HTML boundary. |
| Scope | `SPEC.md`, `IMPLEMENTATION-PLAN.md` | Complete-file V0 boundary accepted. | Append, replace, rebuild, region, operation-mode, and historical-body claims rejected as current V0 defects. |
| Counter-example | All five files | Unapproved durable publication and external symlink publication remain demonstrated V0 traces. | Stale mixed-client overwrite and duplicate append remain design counterexamples for a new operations surface; same-byte metadata is only a contract clarification. |

# Refuted, Demoted, and Out of Scope

- **Dropped:** current V0 replay-record integrity as a defect; the cited contract does not prove the stronger invariant.
- **Dropped as V0 defects:** missing CAS, operation IDs, region targeting, append validation, mixed operation/V0 clients, immutable historical bodies, and navigation ordering.
- **Refuted:** an existing surface can be promoted while preserving unchanged legacy behavior. The recommendation now creates a separate derived surface identity.
- **Refuted:** every builder necessarily crosses filesystem authority. Pure candidate generation does not.
- **Demoted:** `stat()`/`readFile()` coherence is MINOR clarification and hardening.
- **Demoted:** same-byte title/kind behavior is an unresolved contract detail, not a demonstrated defect.
- **Out of scope:** ahead-of-server interaction cursor behavior.

# Unresolved Decisions

1. Whether current canvas publication is approval-gated or a documented trusted-local exception.
2. Whether publication requires a receipt record or an explicit receipt exception.
3. Whether V0 admission needs stronger coherence than one `readFile()` result.
4. How lineage between a V0 surface and its derived operations surface is exposed.
5. Whether later synchronization creates another derived surface or an explicit operation.
6. Whether builders return candidates, mutate canonical files, or support both behind approval.
7. Storage and recovery authority for operation results.
8. Parser, HTML trust, region identity, and runtime-containment policy.
9. Exact `rebuild` and navigation semantics.

# Ordered Change Requests

1. Resolve the current publication approval policy and implement it on `/api/canvas/publish`.
2. Resolve receipt semantics and either emit a validated receipt record or document the exception.
3. Enforce realpath-safe workspace containment and add symlink escape tests.
4. Clarify the plan’s complete-read guarantee; harden admission only if stronger coherence is required.
5. Clarify same-byte metadata semantics.
6. Define derivation of a new `operations_v1` surface from a selected V0 revision.
7. Specify whole-document operation CAS, idempotency, durable records, and record validation.
8. Define later region semantics, HTML trust boundaries, and rebuild behavior.
9. Keep navigation and display refresh outside the content-transformation protocol.
