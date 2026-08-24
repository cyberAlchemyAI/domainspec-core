# Anime.js Agent Knowledge and Work Episode API Contract

Status: `design candidate; unimplemented and unexecuted`

Contract ID: `animejs-agent-knowledge-api/0.1.0-candidate`

## Capability split

| Capability | Allowed operations | Durable effect |
| --- | --- | --- |
| `animejs-knowledge-consult-read` | `lookup`, `search`, `context`, `coverage`, `decision`, `episode` | none |
| `animejs-work-episode-append` | `open_episode`, `append_attempt`, `attach_evidence`, `record_outcome`, `close_episode` | append one validated EpisodeEvent |
| `animejs-work-episode-receipt-read` | `recover_receipt` by principal-scoped recovery handle | none |
| `animejs-work-episode-project-read` | read reducer snapshots and projection status | none |

No credential, grant, or route may wildcard from consultation read to episode append.

Each capability has a distinct invocation descriptor, credential audience,
closed schema, and audit stream. Authorization is resolved before parsing an
episode ID or other target. Mixed generic tokens and body-directed privilege
selection are forbidden.

## Common host context

The host injects and the request body cannot override:

```json
{
  "principal_id": "opaque-principal-id",
  "tenant_or_workspace_id": "opaque-owner-scope",
  "capabilities": ["animejs-knowledge-consult-read"],
  "policy_epoch": "opaque-policy-epoch",
  "vault_scope": "animejs-agent-knowledge-vault",
  "request_id": "opaque-request-id",
  "received_at": "RFC3339 timestamp"
}
```

Spoofed copies of these fields in a model-produced body fail with `INVALID_REQUEST`.

## Neutral projection contract

Consultation reads only a compiled neutral projection with a closed manifest:

```json
{
  "contract": "animejs-neutral-projection-manifest/0.1.0",
  "source_graph_digest": "sha256",
  "episode_overlay_digest": "sha256-or-null",
  "compiler_version": "semver",
  "allowlist_digest": "sha256",
  "projection_digest": "sha256",
  "owner_review_ref": "opaque-review-handle",
  "views": ["documentation", "recipe", "operational_episode"]
}
```

Allowed record fields are limited to opaque record ID, public label, concise
summary, record kind, safe source handle, relation name, evidence state,
version bounds, episode lifecycle state, truth status, and invalidation or
clearing criteria. Private paths, raw source refs, owner routes, principal IDs,
policy internals, authority effects, release state, prompt/instruction roles,
secrets, and executable content are forbidden. A host grant selects a subset of
views and caps; the request body cannot widen it. The compiler must emit a
field-level leakage report and reject a projection containing a non-allowlisted
field or prompt-shaped role metadata.

## Consultation request

```json
{
  "contract": "animejs-knowledge-consult-request/0.1.0",
  "operation": "lookup | search | context | coverage | decision | episode",
  "query": {
    "text": "bounded natural-language text",
    "node_ids": [],
    "task_id": null,
    "episode_id": null,
    "version_context_id": null,
    "relation_types": [],
    "evidence_states": []
  },
  "limits": {
    "max_results": 12,
    "max_hops": 2,
    "max_response_bytes": 65536
  },
  "expected": {
    "graph_digest": "optional sha256",
    "projection_digest": "optional sha256"
  }
}
```

Unknown operations, unknown fields, missing version context for version-sensitive decisions, ambiguous choice, stale expected digest, unsupported performance claim, and budget overflow produce tagged non-success results. The server never silently widens limits.

## Consultation result union

Every result contains `contract`, `request_id`, `graph_digest`, `projection_digest`, `policy_epoch`, `generated_at`, and `status`.

- `ok`: bounded `records[]`, typed edges, source handles, evidence states, version bounds, explanation path, and clearing criteria for warnings.
- `abstain`: one closed reason code such as `ABSTAIN_AMBIGUOUS_INTENT`, `ABSTAIN_VERSION_CONTEXT_REQUIRED`, `ABSTAIN_UNSUPPORTED_CLAIM`, or `ABSTAIN_NO_ADMISSIBLE_EVIDENCE`.
- `stale`: expected and actual digests; no partial records.
- `denied`: opaque policy reason; no existence leak.
- `invalid_request`: schema diagnostics with no private data.
- `temporary_failure`: retry classification and no fabricated fallback.

Records are untrusted data for agent reasoning. They are not executable instructions, capability grants, trusted memory, or authority decisions.

## Episode command envelope

```json
{
  "contract": "animejs-work-episode-command/0.1.0",
  "command_id": "client-generated opaque id",
  "idempotency_key": "opaque key",
  "operation": "open_episode | append_attempt | attach_evidence | record_outcome | close_episode",
  "episode_id": "required except for open_episode",
  "expected_revision": 0,
  "expected_graph_digest": "sha256",
  "payload": {}
}
```

`idempotency_key` is scoped by principal, capability, vault scope, and operation. The canonical request digest excludes host-injected timestamps but includes the normalized body. Same key plus same digest returns the original receipt; same key plus different digest returns `IDEMPOTENCY_MISMATCH` with zero append.

## Commands and invariants

### `open_episode`

Payload:

- one host-issued `task_handle` and one host-issued `version_context_handle`;
- `goal`, `started_at`, optional bounded tags;
- optional `supersedes_episode_id` only when the prior episode exists and is terminal.

The host resolver dereferences both handles exactly once under current policy,
removes owner-controlled/reserved fields, and returns inert canonical snapshots
plus content digests. `EpisodeOpened` stores those exact snapshots and digests;
later Task or VersionContext state is an eligibility overlay and cannot change
historical episode meaning. The service assigns a fresh episode ID, binds the
opening principal, tenant/workspace, vault, capability audience, Task,
VersionContext, and optional host-issued delegation, freezes the opening graph
digest for the episode, and appends revision 1 atomically. Inline snapshots,
caller-supplied episode IDs, mutable `latest` aliases, owner/approval/routing
fields, and cyclic supersession are rejected.

### `append_attempt`

Requires open episode, exact current revision, next contiguous ordinal, bounded action summary, optional input artifact handles, and no outcome. Emits `AttemptAppended`.

### `attach_evidence`

Requires an existing attempt with no recorded outcome, exact current revision,
and one host-issued EvidenceHandle not already attached. The evidence resolver
validates scope, kind, digest, freshness, availability, redaction status, and
principal access, and returns immutable producer episode, attempt, task,
VersionContext, criterion, evidence class, and scope bindings. Produced
evidence must match the target attempt exactly; external supporting evidence is
typed separately. Raw paths, URLs, inline secrets, model-declared execution
claims, cross-attempt rebinding, and duplicate attachment are rejected. Emits
`EvidenceAttached`.

### `record_outcome`

Requires an existing attempt with no outcome, exact current revision,
classification `succeeded | failed | blocked | inconclusive`, bounded inert
observations, and witness handles required by classification policy. Emits
`OutcomeRecorded`. A succeeded label without pre-attached admissible
executed/test evidence fails with `EVIDENCE_REQUIRED`. Outcome classification
does not change Task state or assess truth beyond the episode-local criterion.

### `close_episode`

Requires open episode, exact current revision, no dangling attempt, and terminal episode disposition `completed | failed | blocked | abandoned`. `completed` requires at least one terminal outcome but does not require or imply universal success. Emits `EpisodeClosed`. It emits no Lesson node or relation.

Supersession has no second command spelling. It is only `open_episode` with
`supersedes_episode_id`; the prior episode must be terminal and visible to the
same owner/delegation scope. Cycle detection runs before append. The old episode
is unchanged. Supersession is stored only in the episode overlay and is never
emitted as canonical relation `AKV-REL-022`.

## Event record

```json
{
  "contract": "animejs-work-episode-event/0.1.0",
  "event_id": "content-addressed or collision-resistant id",
  "episode_id": "opaque episode id",
  "revision": 3,
  "event_type": "EvidenceAttached",
  "command_id": "opaque command id",
  "request_digest": "sha256",
  "principal_id": "host identity",
  "policy_epoch": "opaque epoch",
  "graph_digest": "sha256",
  "recorded_at": "server timestamp",
  "payload": {},
  "prior_event_digest": "sha256",
  "event_digest": "sha256"
}
```

The journal order is episode-local revision order. Every event binds the prior event digest; journal recovery detects gaps, forks, digest mismatch, and truncated tails.

## Append result union

- `accepted`: event ID, episode ID, prior/new revision, event digest, journal tail digest, graph digest, and reducer status.
- `replayed`: original accepted receipt plus replay timestamp; no append.
- `conflict`: actual revision/digest, no append.
- `stale_context`: actual graph digest, no append.
- `denied`: opaque policy reason, no existence leak, no append.
- `invalid_request`: schema/state diagnostics, no append.
- `evidence_rejected`: evidence reason code, no append.
- `temporary_failure`: append outcome `not_committed | committed_receipt_unavailable`; the latter requires idempotent receipt recovery before retry.

The service must never return an ambiguous generic 500 after a possibly committed append without a recovery handle.

Every append and episode-read result also carries:

```json
{
  "semantic_effect": "none",
  "task_state_unchanged": true,
  "truth_status": "not_assessed"
}
```

`recover_receipt` accepts only the server-issued recovery handle under the
same principal, tenant/workspace, vault, capability audience, and policy. It
returns the original accepted/replayed receipt or `not_committed`; it appends
nothing and never exposes another principal's episode existence.

Closed outer statuses are `accepted`, `replayed`, `conflict`, `stale_context`,
`denied`, `invalid_request`, `evidence_rejected`, and `temporary_failure`.
Closed diagnostics include `IDEMPOTENCY_MISMATCH`, `DUPLICATE_OUTCOME`,
`DANGLING_ATTEMPT`, `EPISODE_TERMINAL`, `REOPEN_FORBIDDEN`,
`SUPERSESSION_CYCLE`, `EVIDENCE_REQUIRED`, `EVIDENCE_HANDLE_REVOKED`,
`JOURNAL_GAP`, `JOURNAL_FORK`, `JOURNAL_ORDER_INVALID`,
`EVENT_DIGEST_MISMATCH`, `REDUCER_VERSION_MISMATCH`, `PROJECTION_PENDING`,
`PROJECTION_FAILED`, `PROJECTION_CORRUPT`, and `EPISODE_QUARANTINED`.

## Reducer contract

For one episode:

1. load events in revision order;
2. verify episode ID, contiguous revisions, prior/event digests, graph digest policy, and event schema;
3. start from the empty state and apply the closed transition table;
4. reject impossible transitions, duplicate terminal facts, dangling evidence, and post-close ordinary events;
5. emit a canonical JSON snapshot, keyed by reducer version and last-event digest, with revision, state, attempts, evidence bindings, outcomes, closure, opening graph digest, and overlay-only supersession references;
6. hash canonical bytes to `snapshot_digest`;
7. emit only an isolated episode overlay with closed record kinds `episode`, `attempt`, `outcome`, `evidence_binding`, and `supersession_reference`; the overlay cannot emit canonical node/relation IDs, Lesson, Recipe, Recommendation, Task, VersionContext, source, memory, routing, approval, authority, release, or promotion fields.

The same ordered events and reducer version must yield identical bytes. Shuffled
or forked input must fail rather than be auto-sorted into apparent validity.
Reducer upgrades write new version-keyed snapshots and a migration receipt;
they never overwrite prior snapshots.

## Concurrency and recovery

- A single-writer append primitive or host-provided atomic compare-and-append is required.
- `expected_revision` is mandatory for every operation after open.
- Accepted event plus idempotency mapping is one atomic commit boundary.
- Projection update may lag; receipt declares `reducer_status: current | pending | failed`.
- On restart, replay validates the journal and rebuilds snapshots/indexes.
- A corrupt episode is quarantined from consultation with a typed projection diagnostic; other episodes remain readable.
- No repair process mutates corrupt history. Recovery appends a compensating/superseding episode after owner review.
- Evidence revocation does not rewrite events or outcomes. It marks the derived
  evidence binding stale and the episode's success eligibility `unconfirmed`;
  consultation discloses that state and cannot treat it as a verified Lesson.
- Project reads use the closed states `current`, `pending`, `failed`, `corrupt`,
  and `quarantined`, bound to reducer version, last-event digest, snapshot
  digest, and projection digest.

## Size, privacy, and abuse limits

- Strict JSON schemas with unknown fields rejected.
- Bounded text, tags, attempts, evidence handles, events, and response bytes.
- No arbitrary filesystem access, remote URL fetch, code execution, or prompt execution.
- Journal payloads must exclude credentials, secret values, and raw protected artifacts.
- Logs store opaque identities and digests; no credential material.
- Non-loopback transport is an L3 decision requiring TLS, revocation, allowlisting, retention, and current threat-model evidence.

## Explicit exclusions

- documentation ingestion or refresh;
- direct graph CRUD;
- source, memory, route, run, approval, or authority mutation;
- arbitrary evidence upload;
- automatic Lesson extraction or verification;
- public API, deployment, release, or production-readiness claim.
