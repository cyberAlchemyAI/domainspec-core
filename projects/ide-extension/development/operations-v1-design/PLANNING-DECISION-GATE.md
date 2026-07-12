---
id: ide-extension-operations-v1-planning-decision-gate
project: ide-extension
title: "Operations V1 Planning Decision Gate"
status: closed
node_type: decision-gate
updatedAt: 2026-07-12
result: pass
decisions_resolved: 4
blockers_remaining: 0
---

# Decision Gate: Operations V1 Planning

## Blocked Consequential Work

`invoke plan operations_v1` is blocked until the four implementation-contract
decisions below are explicit. No Operations V1 plan, schema, dependency, route,
storage namespace, or runtime behavior is authorized by this record while its
result is `block`.

## Controlling Context

- `ARCHITECTURE-BUNDLE.md` requires a standards-capable HTML parser/serializer,
  immutable content-addressed revision bodies, operation CAS/idempotency, and a
  navigation boundary separate from content mutation.
- `DECISIONS.md` defers parser/version, body limits, blob retention, and
  navigation durability to the implementation plan.
- `IMPLEMENTATION-LAYERING-SEED.md` starts with derive plus replacement, then
  append/retry, then rebuild/navigation; declared regions remain deferred.
- `DISTILL-VALIDATION.md` rejects mutable workspace rereads and in-place V0
  promotion as dishonest shortcuts.
- The completed V0 repair evidence proves the old complete-file surface remains
  intact; it does not implement any Operations V1 behavior.

## Blocker Inventory

| ID | Decision | Why it blocks planning | Dependency order | Status |
| --- | --- | --- | --- | --- |
| OVG-001 | HTML transformation engine and version | Defines append/replace serialization, dependency shape, script posture, and fixtures. | first | selected: Option 1 |
| OVG-002 | Inline document/fragment size limits | Depends on parser memory behavior and defines HTTP/schema/blob admission tests. | after 001 | selected: Option 1 |
| OVG-003 | Immutable blob retention and garbage collection | Defines storage lifecycle, orphan handling, restart evidence, and disk-growth claims. | after 001; independent of 002 | selected: threshold-and-grace hybrid |
| OVG-004 | Navigation command durability | Defines event/projection schema, restart behavior, acknowledgement, and browser tests. | after content decisions | selected: durable target, ephemeral refresh |

## OVG-001: HTML Transformation Engine

### Why This Is Consequential

The parser is not an internal formatting preference. Every committed revision
is hashed after serialization, so changing the parser later may change emitted
bytes, revision digests, fixtures, and retry results even when the rendered DOM
looks equivalent. The choice also determines how malformed HTML, implied
`html/head/body` elements, fragments, doctypes, scripts, SVG/MathML, and future
declared-region traversal behave.

All viable options keep scripts inert during server transformation. Scripts may
execute later when the trusted-local browser loads the committed result; that
is the existing product boundary, not parser execution authority.

### Option 1: Direct parse5 8.0.1 - Recommended

**What it entails**

- Add `parse5` as the one runtime transformation dependency.
- Wrap document parse, body-context fragment parse, traversal, and serialization
  behind a local `HtmlTransformEngine`.
- Pin the lockfile-selected version and freeze output behavior with golden
  document/fragment fixtures.

**Benefits**

- Narrowest standards-oriented tool matching the architecture.
- Direct document, fragment, and serializer primitives without a simulated
  browser or selector framework.
- ESM fits the current project.
- Current registry metadata is approximately 337 KB unpacked with one direct
  dependency (`entities`).
- Scripts are parsed as nodes and never executed by the transformer.

**Costs and risks**

- Tree traversal and future region lookup need small local helpers.
- Serialization normalizes source formatting; byte-for-byte source formatting
  is not preserved.
- Fragment behavior is context-sensitive, so append fixtures must include
  malformed tags, script/style text, table-like fragments, SVG/MathML, and
  documents with implied body elements.

**When to choose**

Choose when Operations V1 should stay a small transformation kernel and named
regions remain a later layer.

**Downstream impact**

- L0 replacement and L1 append share one deterministic engine.
- No Node upgrade.
- Future regions either use local tree visitors or reopen a selector-helper
  decision without replacing parser semantics.

### Option 2: Cheerio 1.2.0 With Default parse5

**What it entails**

- Add Cheerio and use its jQuery-like selection/mutation API.
- Keep default HTML parsing through parse5; use fragment mode where needed.

**Benefits**

- Easier selectors and element mutation, especially if declared regions become
  immediate rather than deferred.
- Familiar manipulation API with document and fragment support.
- Compatible with the current Node 22.12 runtime.

**Costs and risks**

- Current registry metadata is approximately 1 MB unpacked with a broad direct
  dependency set, including parse5, htmlparser2, Undici, selectors, serializers,
  and adapters.
- Adds a higher-level tree model before the current whole-document proof needs
  it.
- More configuration and adapter behavior enters serialization fixtures.
- Encourages region/selector work to leak into L0/L1 prematurely.

**When to choose**

Choose when selector-heavy region mutation is intentionally pulled into the
near-term product boundary and the added dependency surface is acceptable.

**Downstream impact**

- Plan should include selector semantics and adapter-specific fixtures sooner.
- Region implementation becomes easier, but whole-document V1 carries that
  cost from day one.

### Option 3: jsdom 29.1.1 With Node Upgrade

**What it entails**

- Upgrade the current Node 22.12 runtime to a jsdom-supported version.
- Use browser-like `Document` APIs for parsing and mutation while keeping script
  execution and subresource loading disabled.

**Benefits**

- Rich DOM APIs closest to browser-side authoring code.
- Natural selectors, elements, attributes, and future complex DOM operations.
- Scripts and subresources are disabled by default unless explicitly enabled.

**Costs and risks**

- Current jsdom registry metadata is approximately 7 MB unpacked with a large
  dependency graph.
- jsdom 29.1.1 requires Node `^20.19.0 || ^22.13.0 || >=24`; the current local
  runtime is Node 22.12.0, so this option forces a runtime upgrade before value
  work begins.
- Browser emulation is much broader than parse/transform/serialize needs.
- Creates future temptation to execute page scripts server-side, which is
  explicitly outside the architecture.

**When to choose**

Choose only when server-side browser-like DOM behavior is itself a confirmed
product requirement, not merely convenient syntax.

**Downstream impact**

- Adds a prerequisite Node/toolchain SWU and broader dependency validation.
- Increases installation, maintenance, and security-review surface.

### Rejected Non-Option: String Or Regex Mutation

This is not offered as a real choice. It conflicts with OV1-D5 and fails on
malformed documents, missing body tags, script/style contents, comments,
foreign content, and parser repair behavior. Choosing it would require
reopening and replacing the accepted architecture.

### Recommendation

Select **Option 1, direct parse5 8.0.1**. It is the smallest dependency that
matches the accepted whole-document-first architecture. The local wrapper keeps
future replacement possible, while golden serialization fixtures make any
later parser change an explicit migration rather than silent digest drift.

### Selection

- Selected option: Option 1, direct `parse5` 8.0.1.
- Source of decision: human operator reply `1` to OVG-001.
- Timestamp: 2026-07-12T18:41:52Z.
- Planning consequence: use one local `HtmlTransformEngine` wrapper, pin the
  lockfile-selected parser version, keep scripts inert during transformation,
  and require golden document/fragment serialization fixtures.

## OVG-002: Inline And Committed HTML Size Limits

### Why This Is Consequential

The existing server reads request bodies into memory before JSON parsing. The
current canvas interaction route demonstrates bounded admission at 16 KiB, but
most other routes default to an unbounded body reader. Operations V1 sends HTML
inside JSON, then parse5 constructs an in-memory tree and serializes another
complete byte sequence before the blob is committed. A single operation may
therefore hold request bytes, decoded strings, parser nodes, current revision
bytes, and result bytes at the same time.

Limits also define product behavior:

- a document limit controls derivation, inline replacement, and workspace
  rebuild sources;
- a fragment limit controls how much one append can add;
- a committed-result limit controls cumulative page growth;
- an HTTP-body limit must leave space for JSON escaping and metadata;
- rejection must occur before event append or blob publication;
- the limits must use UTF-8 byte length, not JavaScript character count.

Measured local evidence gives scale context:

- current interactive fixtures are approximately 3-4 KiB;
- the generated presentation witness is approximately 4 KiB;
- the Craft presentation is approximately 56 KiB;
- the current workbench HTML is approximately 60 KiB;
- generated Playwright HTML reports in the tree reach approximately 560 KiB,
  although they are evidence reports rather than normal workbench surfaces.

The selected parse5 engine is appropriate for bounded local documents, but it
does not make unbounded parsing free. Exact peak memory depends on document
shape, nesting, text, attributes, and the simultaneous current/result bodies.

### Option 1: Tiered Fixed Budgets - Recommended

**Budgets**

- HTTP operation request body: 5 MiB.
- Inline complete document payload: 4 MiB UTF-8.
- V0 derivation or workspace rebuild source: 4 MiB.
- One append fragment: 512 KiB UTF-8.
- One committed complete result: 8 MiB.

**Benefits**

- Gives the current 60 KiB workbench roughly 65x document headroom.
- Supports embedded CSS, JavaScript, diagrams, and moderate inline assets.
- Keeps one append meaningfully smaller than a complete replacement.
- Allows repeated appends to grow a page beyond the source limit while placing
  a hard ceiling on parser/blob growth.
- Fixed values make fixtures, errors, retries, and operational claims
  deterministic across machines.

**Costs and risks**

- A very large self-contained page with base64 media may require externalizing
  assets or a later limit revision.
- Four related limits require careful naming and boundary tests.
- An 8 MiB current document plus append still creates transient memory several
  times larger than the stored body.

**When to choose**

Choose for a value-first local builder that needs generous practical headroom
without turning configuration into a product feature.

**Downstream impact**

- Add constants owned by the Operations V1 service, not global server defaults.
- Add exact limit-minus-one, exact-limit, and limit-plus-one fixtures.
- Return `413 request_too_large` for HTTP overflow and a typed operation error
  for payload/source/result overflow before commit.
- Keep asset files referenced by path/URL when a document would exceed limits.

### Option 2: One Large Shared Budget

**Budgets**

- HTTP and input payload: 8 MiB.
- Committed result: 16 MiB.
- Append uses the same input budget as replacement.

**Benefits**

- Simplest contract and implementation.
- Accommodates large inline images, generated reports, and monolithic HTML.
- Fewer constants and fixture boundaries.

**Costs and risks**

- An append may be as large as a complete page, weakening operation intent.
- Higher peak memory under concurrent or repeated local requests.
- More disk growth before blob retention is decided.
- Makes accidental giant model output easier to accept and persist.
- A shared number hides the difference between transport input and cumulative
  committed state.

**When to choose**

Choose when large self-contained HTML artifacts are already a primary use case
and simplicity matters more than differentiated admission semantics.

**Downstream impact**

- Smaller schema/constant surface, but stronger stress tests are required.
- Blob retention becomes more urgent because each revision may be much larger.

### Option 3: Configurable Local Budgets

**Budgets**

- Use Option 1 defaults, overridable through server configuration or
  environment variables.

**Benefits**

- Operators can admit larger presentations or smaller constrained devices.
- Avoids changing source to test different capacity profiles.
- Provides an escape hatch for unusual local artifacts.

**Costs and risks**

- Behavior and retry outcomes differ between machines.
- Configuration provenance must enter diagnostics and possibly operation
  evidence.
- Requires invalid-value, precedence, startup, and observability tests.
- Makes fixtures and support more complex before real demand exists.
- A permissive override can silently defeat the intended bounded-memory
  posture.

**When to choose**

Choose when multiple known machine profiles or large-artifact workflows already
exist and reproducibility across them is less important than flexibility.

**Downstream impact**

- Adds configuration schema and startup validation to L0.
- Plan must define which limit profile produced an operation result.

### Rejected Non-Option: Unbounded HTML

Unbounded admission is not a viable option. The server materializes the body,
JSON string, parse tree, current revision, serialized result, and blob bytes in
one process. A trusted-local posture removes hostile-input claims; it does not
remove accidental memory exhaustion or deterministic-test requirements.

### Recommendation

Select **Option 1, tiered fixed budgets**. The measured workbench corpus is far
below these limits, so the option preserves substantial creative headroom while
making the operation contract, memory posture, and tests explicit. Configuration
can remain a later response to demonstrated large-document demand.

### Selection

- Selected option: Option 1, tiered fixed budgets.
- Source of decision: human operator reply `1` to OVG-002.
- Timestamp: 2026-07-12T18:49:40Z.
- Planning consequence: enforce 5 MiB HTTP requests, 4 MiB complete inline or
  workspace sources, 512 KiB append fragments, and 8 MiB committed results in
  UTF-8 bytes; reject before blob/event commit and freeze every boundary with
  limit-minus-one, exact-limit, and limit-plus-one fixtures.

## OVG-003: Immutable Blob Retention And Garbage Collection

### Why This Is Consequential

Operations V1 events store revision metadata and `result_blob_ref`; they do not
copy HTML bodies into `events.jsonl`. The blob is therefore part of the durable
meaning of every committed revision. Deleting a referenced blob makes its
historical content URL unavailable and prevents an exact operation retry from
returning a usable original result, even though the event still claims that
revision committed.

The crash order intentionally writes the content-addressed blob before the
event. This creates two different classes of stored body:

- **referenced committed blob:** at least one valid replayed event/revision
  points to it;
- **orphan blob:** the body write succeeded but no committed event references
  it, commonly because event append failed or the process stopped between the
  two steps.

A projection-write failure after event append does not make the blob orphaned.
The event is authoritative and reconciliation must restore the projection while
preserving the referenced body.

The selected 8 MiB committed-result ceiling bounds one blob, not total storage:

- 100 unique worst-case revisions can consume about 800 MiB;
- 1,000 unique worst-case revisions can consume about 8 GiB;
- at the current approximately 60 KiB workbench size, 100 unique revisions are
  closer to 6 MiB;
- content addressing deduplicates byte-identical results across retries and
  surfaces when they share one blob namespace.

The existing persistence layer already prefers evidence visibility over silent
cleanup: it reports orphan artifacts during reconciliation instead of deleting
them automatically. Operations V1 can follow or intentionally change that
posture.

### Option 1: Retain All Committed Blobs, Report Orphans - Recommended

**Policy**

- Never automatically delete a blob referenced by any valid replayed revision
  or operation record.
- Keep one content-addressed file per digest, deduplicating identical bytes.
- Remove temporary files when an individual atomic write fails.
- Report `orphan_blobs`, referenced blob count, total bytes, and largest blob in
  reconciliation/diagnostics.
- Do not auto-delete orphan blobs in Operations V1; design an explicit cleanup
  action only after storage evidence justifies it.

**Benefits**

- Historical revision URLs remain stable.
- Exact operation retries always have their original body.
- Simplest replay model: event/reference validity implies body availability.
- Matches the append-only local evidence posture.
- No destructive startup behavior or retention timers.
- Content addressing naturally removes duplicate-body multiplication.

**Costs and risks**

- Unique revisions accumulate indefinitely.
- Failed pre-event writes may leave orphan disk residue.
- Operators need diagnostics to notice growth.
- A later cleanup feature must introduce an explicit authority and evidence
  model rather than relying on an existing automatic policy.

**When to choose**

Choose for a local value experiment where semantic integrity and minimum
implementation complexity matter more than automatic disk management.

**Downstream impact**

- L0 includes blob diagnostics and restart/reference checks, but no deletion
  endpoint or scheduled job.
- Tests prove deduplication, event-reference availability, orphan reporting,
  and projection-failure preservation.
- Disk-pressure handling remains a visible future-hardening trigger.

### Option 2: Retain Committed Blobs, Automatically Delete Orphans On Startup

**Policy**

- Retain every referenced committed blob exactly as Option 1.
- After successful full event replay and reference validation, delete every
  unreferenced blob and stale temporary file automatically.

**Benefits**

- Historical revision and retry semantics remain intact.
- Crash residue does not accumulate across restarts.
- Total storage contains only event-reachable bodies.

**Costs and risks**

- Startup becomes destructive.
- Cleanup must never run when event history is missing, malformed, truncated,
  unsupported, or only partially read.
- Requires race, interrupted-cleanup, permission, and deletion-failure tests.
- An implementation bug in reference discovery can irreversibly remove the
  only body for a valid event.
- Diverges from the existing report-orphans persistence posture.

**When to choose**

Choose when automatic crash-residue cleanup is already considered necessary
and the extra destructive validation surface is acceptable.

**Downstream impact**

- Adds a startup cleanup phase after successful reconciliation.
- Requires fail-closed cleanup receipts or diagnostics and stronger recovery
  tests before L0 can pass.

### Option 3: Bounded Revision Retention With Pruning Events

**Policy**

- Keep current plus a selected number or age of historical revisions per
  surface.
- Append an explicit `canvas.revision_pruned` tombstone before removing a
  referenced body.
- Historical content requests return a stable `410 revision_pruned` result.

**Benefits**

- Bounds long-term disk growth.
- Makes storage behavior predictable under sustained high revision counts.
- Preserves an auditable record that a body was intentionally removed.

**Costs and risks**

- Changes immutable-history semantics into retained-metadata semantics.
- Exact retries of old operations can return metadata but not the original
  usable HTML.
- Requires pruning authority, policy parameters, tombstone schemas, route
  behavior, retries, restart ordering, and browser degradation states.
- Count and age choices create another unresolved product decision.
- Considerably enlarges L0/L1 before value is proven.

**When to choose**

Choose only when bounded disk usage is a present requirement strong enough to
accept expiring historical bodies.

**Downstream impact**

- Retention becomes a first-class lifecycle with new events and tests.
- Operation idempotency must explicitly define behavior after result pruning.

### Selected Hybrid: Retain, Ask, Then Automatically Prune

**Policy**

- Retain all committed blobs during normal operation and continuously report
  total bytes, referenced bytes, orphan bytes, and pruning eligibility.
- Crossing a soft storage threshold creates a visible pruning request and a
  grace deadline. During the grace period, the user may preview and explicitly
  prune eligible history.
- Automatic reclamation begins when either the hard storage threshold is
  crossed or the grace deadline expires while usage remains above the soft
  threshold.
- Automatic reclamation first removes stale temporary files and blobs proven
  orphaned by a successful full event replay, then prunes the oldest eligible
  committed revisions until usage returns below the soft threshold.
- Exact soft threshold, hard threshold, and grace duration are fixed,
  reversible plan constants. Changing those values does not change this
  retention contract.

**Pruning invariants**

- The current revision of any surface is never eligible for pruning.
- A referenced body is deleted only after its
  `canvas.revision_pruned` tombstone is durably appended.
- If tombstone append fails, body deletion does not occur.
- A content-addressed blob shared by multiple revisions is deleted only when no
  unpruned revision references it.
- Malformed, partial, or unsupported event history disables all automatic
  reclamation; diagnostics report the blocked cleanup state instead.
- A pruned content route returns stable `410 revision_pruned` metadata.
- An exact retry of an operation whose body was pruned returns the original
  operation/revision metadata plus an explicit unavailable-body result; it
  never silently creates a different revision.

**Why this hybrid was selected**

This preserves complete history without operator work at ordinary project
sizes, gives the user a meaningful chance to choose what is removed, and still
bounds unattended growth. The soft threshold provides agency; the grace and
hard thresholds provide a deterministic fallback. Durable tombstones preserve
an auditable distinction between intentional pruning and missing/corrupt data.

### Rejected Non-Option: Delete Unreferenced Files By Age Without Replay

Filesystem age alone cannot prove that a blob is unreferenced. Cleanup must be
derived from successfully replayed event authority; otherwise a clock or stale
projection can delete valid revision bodies.

### Recommendation

The original recommendation was Option 1 for the smallest initial lifecycle.
The selected hybrid intentionally combines Option 1's retain-and-diagnose
default with Option 3's durable pruning protocol, adding a user-visible grace
period before automatic enforcement. This costs more lifecycle work than pure
retention, but it resolves both operator agency and unbounded-growth concerns
without making deletion silent.

### Selection

- Selected option: custom threshold-and-grace hybrid combining Options 1 and 3.
- Source of decision: human operator direction, `time policy decides, we can
  ask user to prune until a threshold and then automatically prune`.
- Timestamp: 2026-07-12T19:01:35Z.
- Planning consequence: define fixed soft-byte, hard-byte, and grace-duration
  constants; model warning, grace, and automatic-reclamation states; provide a
  manual preview/prune action; and freeze tombstone-before-delete, shared-blob,
  retry-after-prune, fail-closed replay, and reclaim-order behavior in tests.

## OVG-004: Navigation Command Durability

### Why This Is Consequential

V0 couples content publication to one durable `current_surface_id`. Its SSE
stream is only a wake-up signal: reconnecting clients read the durable current
projection and recover after disconnect or restart. Operations V1 intentionally
separates content mutation from display selection, because creating or editing
one surface must not unexpectedly replace what the user is viewing.

The navigation contract therefore needs to decide which intent survives server
restart, what a disconnected browser misses, whether acknowledgements belong in
event history, and whether the first implementation needs browser identities
and pending-command replay.

### Option 1: Durable Display Target, Ephemeral Refresh - Recommended

**Policy**

- One kernel-owned local workbench display target is stored in durable event
  projection.
- An idempotent `redirect` command selects an admitted V0 or Operations V1
  surface revision and durably changes that display target.
- Reconnect and restart recover the selected target from projection; SSE only
  wakes connected browsers to reread it.
- A `refresh` command is transient because it does not change desired display
  state. An online browser reloads the selected target and acknowledges the
  command through short-lived diagnostic state.
- Refresh delivery and acknowledgements are not appended to permanent event
  history. If the browser or server restarts, loading the durable target
  satisfies the useful effect without replaying stale refresh commands.
- A content commit triggers reload only when its surface is the durable display
  target. It never redirects from another surface.
- Per-tab, per-browser, and multi-workbench display targets are deferred.

**Benefits**

- Preserves the prototype's proven durable-truth plus SSE-wake-up behavior.
- Makes agent-directed `create and show` reliable across ordinary reconnects.
- Avoids treating stateless reloads as permanent domain history.
- Requires no browser identity, durable acknowledgement cursor, command expiry
  state machine, or pending-command replay in the first implementation.

**Costs and risks**

- All connected local workbench tabs converge on one selected target.
- A caller can know that a redirect committed, but browser-load acknowledgement
  remains transient and may disappear on restart.
- Durable redirect idempotency and target admission still require event,
  projector, route, reconnect, and failure-path tests.

**Downstream impact**

- Add a versioned display-target selection event and projection field separate
  from content-surface current revisions.
- Keep revision notices and navigation notices distinguishable on the SSE
  transport.
- Return redirect commit state from the HTTP route; expose transient browser
  load/refresh acknowledgement only as runtime diagnostics.
- Test offline redirect recovery, server restart recovery, duplicate command
  identity, same-target redirect, transient refresh, failed iframe load, and
  content commits on selected versus non-selected surfaces.

### Option 2: All Navigation Ephemeral

Both redirect and refresh commands exist only on the live SSE channel. This is
the smallest server change, but redirects sent while the browser is disconnected
are lost, restart forgets the selected target, and the kernel cannot reliably
complete `create and show`. Browser-local storage would move navigation
authority out of the kernel and produce divergent tabs.

### Option 3: Durable Commands And Acknowledgements

Every redirect, refresh, delivery, and browser acknowledgement is appended to
event history. This provides a complete command audit and pending replay, but
requires browser identities, delivery cursors, expiry, retry semantics,
multi-browser completion rules, and stale-refresh suppression before they have
demonstrated value. It turns navigation into a durable job queue rather than a
display pointer.

### Selection

- Selected option: Option 1, durable display target with ephemeral refresh and
  acknowledgement state.
- Source of decision: explicit human operator confirmation `yes` after the
  Option 1 contract and single-workbench boundary were restated.
- Timestamp: 2026-07-12T19:06:02Z.
- Planning consequence: model durable redirect selection separately from
  transient reload delivery; preserve one global local-workbench target; and
  defer browser identity, per-tab targets, durable acknowledgement history, and
  navigation job replay.

## Gate State

- Result: `PASS`.
- Decisions resolved: 4.
- Blockers remaining: 0.
- Deferred decisions: named-region mutation, per-browser display targets,
  durable navigation acknowledgement history, and exact retention threshold
  tuning beyond the fixed plan constants.
- Consequential next route: `invoke plan operations_v1`.
