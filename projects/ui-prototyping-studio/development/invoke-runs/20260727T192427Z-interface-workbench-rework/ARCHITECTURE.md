---
artifact: ui-prototyping-studio-interface-workbench-architecture
status: design-validator-pass
design_evidence: design-validator-pass
plan_evidence: pending
lifecycle_owner: ui-prototyping-studio
---

# Architecture: Stable Governed Interface Workbench

## Architecture Intent

Keep the Studio’s application-owned governance loop intact while replacing
whole-document poll refresh with a server-versioned stable shell and
state-specific workbench regions.

Continuity is L0. The six named regions are the target Design contract because
their identities bound the context that must survive. Plan may first establish
coherent transport, inert polling, recoverable updates, and action freshness
over the stable shell; it owns when each hierarchy or visual-composition change
enters an L0–L3 SWU.

## Source Contracts

| Contract ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SC-001 | `.craft/ledger.yml` | yes | lifecycle authority; terminal prior frontier |
| SC-002 | root `SPEC.md` | yes | current governance and handoff invariants |
| SC-003 | root `ARCHITECTURE.md` | yes | existing layer and projection ownership |
| SC-004 | verified interface audit | yes | current defects, priorities, claim boundaries |
| SC-005 | Invoke `SPEC.md` and `GLOSSARY.md` | yes | approved Define contract |
| SC-006 | current `studio.ts` and governed projection | yes | current renderer and transport mechanics |
| SC-007 | current projection/action/mobile E2E specs | yes | non-regression floor |
| SC-008 | `WITNESS-CONTRACTS.md` | yes | planned, unexecuted acceptance |

## Closed Scope

- System of interest: `ui-prototyping-studio-interface-workbench`
- Manifest: `DESIGN-SCOPE-MANIFEST.json`
  - input digest:
    `63f1a4bdb9e30a3711db42654d46a7fad91fe1b6b096318122433aa5d6f963df`
- Denominator receipt: `DESIGN-DENOMINATOR-RECEIPT.json`
  - receipt digest:
    `f250f4e6576a4d070794ff108f756b2b99f117c829f8a2d7dc454896d4035098`
- Selection result: `DESIGN-SELECTION-RESULT.json`
  - result digest:
    `7125c8b9c980946a6a5927bafc1e334ca80c47d93ba523aa6525a25ed1695b99`
- Fixed point: pass; pass-one and pass-two digest:
  `74ca227552aa66e934068a6b6fc1e0f7e9e7cb93839e0b609e66d3bde18d8855`
- Required extensions: authority/trust, security/abuse, state/event,
  persistence/concurrency, failure/compensation, integration/versioning,
  quality, UX Plan, and validation contracts

## View 1: Context

```text
external CLI/generator ───────────────┐
                                      v
operator ── local browser shell ── preview adapter
                |                     |
                | keyed projection    | application gates
                v                     v
         browser-local context   application state machine
                                      |
                                      v
                         file store + HTML artifact store
```

The browser shell is a projection and action adapter. It does not become
current-state authority, infer actor authorization, or own readiness.

## View 2: High-Level Structure

| Component | Responsibility | Authority |
| --- | --- | --- |
| Workbench Projection Builder | Acquire one coherent application/store snapshot and derive stable region objects plus compatibility fields from it. | read-model only |
| Projection Versioner | Canonically hash the full projection and each keyed region. | change identity only |
| Stable Shell | Hold landmarks, region mounts, local context, refresh coordinator, and error/status surfaces. | ephemeral browser state |
| Region Renderers | Safely update lifecycle, canvas, inspector, review, history, and action regions. | projection only |
| Context Reconciler | Preserve context whose bound identity remains valid; explicitly invalidate stale context. | local continuity policy |
| Action Adapter | POST current acknowledged actions and trigger one coordinated state refresh. | transport only |
| Application Core | Validate acknowledgment, identity, admission, revision append, and handoff predicates. | governed state authority |
| Existing Stores | Provide fresh reads and serialized durable writes. | persisted state authority |

## View 3: Low-Level Components

### Workbench Projection

Add an application-adjacent projection type whose outer shape is:

```text
WorkbenchProjection {
  schemaVersion
  version
  regionVersions {
    spine
    canvas
    inspector
    review
    history
    actions
  }
  spine
  canvas
  inspector
  review
  history
  actions
}
```

`version` is SHA-256 over canonical JSON of the projection excluding the
version fields. Each region version is the same canonical digest over its exact
region object. The server owns nullability and ordering. The browser never
concatenates nullable identity fields to infer equality.

Canonical JSON is a project-owned deterministic encoding:

- objects are encoded recursively with keys sorted in ascending UTF-16 code
  unit order;
- array order is preserved;
- `null`, strings, booleans, and finite JSON numbers use their exact
  `JSON.stringify` representation;
- `undefined`, functions, symbols, non-finite numbers, and sparse array holes
  are rejected before hashing; and
- SHA-256 consumes the UTF-8 bytes and emits lowercase hexadecimal.

Golden vectors bind these rules. The projection builder and contract validator
recompute every region digest from its exact region object and the whole digest
from the complete projection without version fields. The browser treats both
digest families as opaque and validates only schema compatibility.

Projection assembly is accepted only from one coherent read:

1. acquire an application/store read epoch or stable input identity;
2. read session, revisions, variants, current HTML identity, staged candidate,
   comments, and handoff inputs;
3. re-read the epoch or input identity;
4. accept only when the before/after identity matches; otherwise retry within a
   bounded limit; and
5. on exhaustion, return a recoverable projection-read failure without
   emitting a new version.

An implementation may use an existing serialized read lock instead of the
read/verify/retry protocol. In either case, legacy `state`, `head`,
`stagedHash`, and `projection` compatibility fields derive from the same
accepted snapshot, never from later independent reads.

Region objects contain data, identity, route, labels, and availability—not
prebuilt outer-shell HTML. Prototype HTML remains inside existing sandboxed
iframe routes.

### Stable Shell

The initial document contains:

- skip link and workbench title;
- lifecycle/action spine landmark;
- current canvas landmark;
- contextual inspector landmark;
- staged/recorded review landmark;
- collapsed history landmark;
- bounded network/recovery status; and
- scripts for safe rendering and coordinated refresh.

The shell remains mounted for the preview lifetime. Region renderers use
`textContent`, explicit element creation, and allowlisted attributes. They do
not write server data through `innerHTML` or `outerHTML`.

### Refresh Coordinator

`refresh(reason)` is single-flight with one bounded trailing-refresh slot:

1. reuse the in-flight request when one exists;
2. when an action completion joins a request that began before its action
   receipt, mark one trailing refresh required;
3. validate schema compatibility and return without side effect when `version`
   is already applied;
4. compare region versions;
5. prepare all changed region nodes in detached fragments using safe sinks;
6. calculate local-context preservation/invalidation without mutating live
   context;
7. commit the prepared regions and context plan through a rollback journal;
8. if any commit fails, restore every already-changed mount and local-context
   snapshot and keep the prior whole/region applied versions;
9. only after the full commit succeeds, mark the new whole and region versions
   applied; and
10. after releasing the flight, run exactly one queued trailing refresh before
    an action handler reports its final observed state.

Polling and action completion call the same coordinator. The action handler no
longer calls `location.reload()`. Poll-only callers coalesce without creating
an unnecessary trailing request. Multiple action completions during one flight
coalesce into one trailing request; a later action arriving during that
trailing flight may queue the next bounded trailing refresh.

### Context Reconciler

Browser-local context binds to server identities:

- annotation target and drafts bind to current-head revision plus `odId`;
- staged acknowledgment binds to candidate hash and target state;
- Revert acknowledgment binds to current revision;
- iframe scroll binds to frame source identity;
- open inspector/history state binds to region identity.

When identities remain valid, context survives. When a changed projection
invalidates one binding, only that context is reset and the matching status
scope explains why.

## View 4: Workflow Process

```text
load shell + projection
  -> apply initial region versions
  -> poll through single-flight refresh
     -> same version: no DOM work
     -> new version:
          validate
          -> prepare changed regions + context plan
          -> commit once or rollback completely
     -> invalid/error:
          preserve current work
          -> show bounded recovery

operator action
  -> acknowledge live identity when required
  -> POST existing action route
     -> rejected: preserve work + scoped error
     -> accepted: call same refresh coordinator
          -> if joined older poll, queue one trailing refresh
          -> apply unseen version once
```

## View 5: State And Event

| Lifecycle state | Primary work | Inspector/review | Next valid action surface |
| --- | --- | --- | --- |
| SessionInitialized | empty current-work canvas | prompt/register guidance | terminal/CLI details secondary |
| PromptCaptured | prompt context | variant-registration guidance | register variants |
| VariantsReady | candidate comparison | baseline selection context | select/commit baseline |
| BaselineReady | current head | target selection + annotation form | comment, then synthesize |
| CommentsCaptured | current head | comment queue bound to revision | synthesize |
| MutationDrafted | current head | batch identity and summary | approve batch |
| MutationApproved | current head | approved batch and proposal seam | apply candidate via CLI |
| RevisionApplied | current head + candidate review | Before/After/Diff, identity, acknowledgment | Accept or Discard |
| RevisionRecorded | accepted current head | revision receipt and Revert context | comment again or Revert; Export stays terminal-only |
| SessionCompleted | final current head | handoff receipt summary | no browser Export |

State vocabulary does not change. The workbench changes presentation and
continuity, not the application transition graph.

## View 6: Deployment And Runtime

- Runtime remains a no-build Node/TypeScript loopback server.
- Binding remains `127.0.0.1`; no remote release service is introduced.
- Current CLI, file store, and artifact store remain.
- The stable shell may remain embedded in the preview adapter for L0/L1.
- L0 may repair coherent projection transport, inert polling, recoverable
  commit, action freshness, and context preservation before later SWUs change
  every region’s visual hierarchy.
- L2 may extract renderer modules for maintainability, but framework adoption
  is not an acceptance condition.
- Existing checked-in local `tsc`, `tsx`, and Playwright binaries remain the
  validation route when Corepack/pnpm is unavailable.

## Extension: Authority And Trust

- Current-head and staging authority remain in the application core and stores.
- Region versions are evidence of projection change, not approval or readiness.
- Acknowledgment remains actor-neutral and exact-identity-bound.
- Browser Accept/Discard/Revert routes must not bypass existing use cases.
- Revert remains append-only.
- Export remains terminal-only.
- Lifecycle acceptance, SWU selection, Task Session execution, evidence
  admission, human-study claims, and release remain separate gates.

## Extension: Security And Abuse

- Outer-shell data uses safe DOM sinks and explicit attribute allowlists.
- Prototype HTML remains in sandboxed frames; annotation keeps its narrowly
  trusted click wrapper.
- No projection field may supply script, event-handler, style, or arbitrary
  outer-shell markup.
- Region route values are server-produced and limited to existing local route families.
- A malformed response blocks patching and preserves the last known projection.
- A stale client identity never weakens server-side acknowledgment validation.
- The design adds no remote origin, auth surface, model key, or telemetry sink.

## Extension: Persistence And Concurrency

- No new durable store is introduced.
- Projection versions and legacy compatibility fields derive from one accepted
  coherent store snapshot.
- Browser context is ephemeral and explicitly non-authoritative.
- External CLI writes and browser writes may race at the existing
  application/store boundary; server-side stale checks remain decisive and a
  torn read is retried or fails recoverably.
- Poll and action refreshes are coalesced in one client single-flight
  coordinator. An action that joins an older flight queues one trailing
  refresh, and every version is applied at most once.

## Extension: Failure And Compensation

| Failure | Required behavior |
| --- | --- |
| unchanged response | no navigation, patch, focus move, or announcement |
| network/poll failure | retain current projection and drafts; show quiet recoverable status |
| malformed response | do not patch; show bounded error; retry safely |
| unstable projection snapshot | emit no new version; return recoverable failure after bounded retry |
| action rejection | preserve acknowledgment context where still live; show matching scoped error |
| state changes during action | server rejects stale identity; refresh and explain invalidation |
| region-render failure | rollback every changed mount and local-context mutation; retain prior whole/region applied versions and retry deterministically |
| child-frame load failure | outer shell survives and offers retry/open-full-preview context |

No failure path may visually imply that Accept, Revert, or Export succeeded
without the application receipt.

## Extension: Integration And Versioning

- `/state` evolves additively to include `schemaVersion`, `version`, and region
  objects/versions.
- During the bounded transition, legacy `state`, `head`, `stagedHash`, and
  `projection` fields may remain until all current consumers move, but all
  derive from the same accepted projection snapshot.
- Canonical whole/region digests are validated at server construction and by
  contract tests; the browser consumes them as opaque identities.
- The new shell validates the declared schema version and blocks unknown major versions.
- Current HTTP action routes and application calls remain compatible.
- E2E helpers consume the new projection version rather than waiting for reload.
- Guided human instructions change only after the new implementation passes.

## Extension: Quality

Required thresholds:

- zero unchanged main-document navigations;
- zero unchanged region patches;
- exactly one application of one unseen real-transition version;
- one mandatory trailing refresh when an action joins an older poll flight;
- zero mixed governed surfaces after a renderer failure;
- compatibility fields coherent with the accepted projection snapshot;
- preserved named local context when its identity remains valid;
- explicit bounded invalidation when identity changes;
- 4.5:1 for sampled normal-size light-surface text;
- calibrated minimum target size;
- named comparison frames;
- exact live-region scopes;
- no horizontal overflow at 390px; and
- current unit/E2E/governance non-regression.

Performance is secondary: a 1.5-second poll may remain for the first repair as
long as unchanged responses are inert. Streaming or push transport is out of
scope until measurements justify it.

## Rejected Alternatives

| Alternative | Reason rejected |
| --- | --- |
| Normalize only `null` to empty string and keep reload | fixes the loop but preserves known context loss on every genuine transition |
| Full SPA/framework migration first | increases scope before continuity semantics are proved |
| Server-sent events/WebSocket first | unnecessary transport expansion for a local polling workbench |
| Persist drafts in the authoritative store | changes data and authority semantics beyond the evidence |
| Put all interface state in one rerendered region | still destroys bounded local context on unrelated changes |
| Move history out of the system | loses required lineage evidence; history should be secondary, not deleted |

## Evidence And Validation

The selected UX Plan is `UX-PLAN.md`; exact automated contracts are
`WITNESS-CONTRACTS.md` and `VALIDATION-STRATEGY.md`. The governed Design
Distill change-request set is `design-distill-review/findings.md`; its accepted
revisions and passing gate are recorded in `DESIGN-DISTILL.md`. Nothing here is
implementation evidence.

## Gate Result

- Design denominator: pass
- Two-pass selection: pass
- Required views/extensions: authored
- UX Plan: authored
- Planned witnesses: authored
- Design Distill review: resolved with DDR-01–DDR-05 accepted and authored
- Design revalidation: pass; unchanged two-pass fixed point
- Plan admission: allowed for non-mutating Invoke Plan authoring only
